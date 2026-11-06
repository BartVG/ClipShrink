"""Stage 1: walk a folder and its subfolders, list every H.264 video."""
import json, os, re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from fractions import Fraction
from pathlib import Path
from . import config, tools


@dataclass
class MediaInfo:
    path: str
    size: int
    mtime_ns: int
    codec: str
    width: int
    height: int
    fps: float
    duration: float
    frames: int
    video_bytes: int
    pix_fmt: str = ""
    color_range: str = ""
    color_space: str = ""
    color_primaries: str = ""
    color_trc: str = ""
    audio_codecs: list = field(default_factory=list)

    @property
    def group(self):
        return (self.width, self.height, round(self.fps))


@dataclass
class ScanResult:
    h264: list = field(default_factory=list)
    other: list = field(default_factory=list)
    unreadable: list = field(default_factory=list)
    has_conversion: dict = field(default_factory=dict)  # H.264 path -> the conversion beside it


def probe_file(path):
    r = tools.run([tools.ffprobe(), "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)])
    if r.returncode:
        raise ValueError((r.stderr.strip().splitlines() or ["cannot read file"])[-1])
    data = json.loads(r.stdout)
    video = [s for s in data.get("streams", []) if s["codec_type"] == "video"
             and not s.get("disposition", {}).get("attached_pic")]
    if not video:
        raise ValueError("no video track found")
    v = video[0]
    st = os.stat(path)
    try:
        fps = float(Fraction(v.get("avg_frame_rate", "0/1")))
    except (ValueError, ZeroDivisionError):
        fps = 0.0
    dur = float(v.get("duration") or data["format"].get("duration") or 0)
    if "bit_rate" in v:
        video_bytes = int(int(v["bit_rate"]) * dur / 8)
    else:
        other = sum(int(s.get("bit_rate", 0)) for s in data["streams"] if s is not v)
        video_bytes = max(0, st.st_size - int(other * dur / 8))
    return MediaInfo(path=str(path), size=st.st_size, mtime_ns=st.st_mtime_ns, codec=v.get("codec_name", "?"),
                     width=int(v.get("width", 0)), height=int(v.get("height", 0)), fps=fps, duration=dur,
                     frames=int(v.get("nb_frames") or 0) or round(fps * dur), video_bytes=min(video_bytes, st.st_size),
                     pix_fmt=v.get("pix_fmt", ""), color_range=v.get("color_range", ""),
                     color_space=v.get("color_space", ""), color_primaries=v.get("color_primaries", ""),
                     color_trc=v.get("color_transfer", ""),
                     audio_codecs=[s.get("codec_name") for s in data["streams"] if s["codec_type"] == "audio"])


_TAGS = re.compile(r"^(?P<stem>.+?)(?:_\((?:4k|1080p|720p)\))?_\((?:h265|av1)\)(?:_\d+)?$|"
                   r"^(?P<old>.+?)_(?:H265|AV1)(?:_\d+)?$", re.IGNORECASE)


def original_stem(path):
    """The original's name if this file is named like a conversion, otherwise None."""
    m = _TAGS.match(Path(path).stem)
    return (m.group("stem") or m.group("old")) if m else None


def find_conversions(res):
    """Matches H.264 files with a real H.265 or AV1 file beside them, by name. No memory is involved."""
    beside = {}
    for f in res.other:
        stem = original_stem(f.path)
        if stem and f.codec in ("hevc", "av1"):
            beside[(str(Path(f.path).parent).lower(), stem.lower())] = f.path
    for f in res.h264:
        hit = beside.get((str(Path(f.path).parent).lower(), Path(f.path).stem.lower()))
        if hit:
            res.has_conversion[f.path] = hit


def walk_videos(root):
    stack = [str(root)]
    while stack:
        d = stack.pop()
        try:
            with os.scandir(d) as it:
                entries = list(it)
        except OSError:
            continue
        for e in entries:
            if e.is_dir(follow_symlinks=False):
                if e.name.lower() not in config.SKIP_DIRS:
                    stack.append(e.path)
            elif e.is_file(follow_symlinks=False) and Path(e.name).suffix.lower() in config.VIDEO_EXTS:
                yield e.path


def lrv_files(res):
    """Every GoPro preview a scan came across, whatever could be read of it."""
    paths = [f.path for f in res.h264 + res.other] + [p for p, _ in res.unreadable]
    return sorted(p for p in paths if Path(p).suffix.lower() == ".lrv")


def lrv_original(path):
    """The full video beside a GoPro preview, or None. GL010123.LRV belongs to
    GH010123 or GX010123, older cameras use the same name, and either may
    already be a conversion such as GX010123_(h265).mp4."""
    p = Path(path)
    stem = p.stem.lower()
    wanted = {stem}
    if stem.startswith("gl"):
        wanted |= {"gh" + stem[2:], "gx" + stem[2:]}
    try:
        with os.scandir(p.parent) as it:
            names = [e.name for e in it if e.is_file()]
    except OSError:
        return None
    for name in names:
        n = Path(name)
        if n.suffix.lower() in config.VIDEO_EXTS and n.suffix.lower() != ".lrv":
            other = n.stem.lower()
            if other in wanted or any(other.startswith(w + "_") for w in wanted):
                return str(p.with_name(name))
    return None


def scan_folder(root, on_progress=None, should_stop=None):
    res = ScanResult()
    paths = sorted(walk_videos(root))

    def one(p):
        if should_stop and should_stop():
            return p, None, "stopped"
        try:
            return p, probe_file(p), None
        except Exception as ex:
            return p, None, str(ex)

    with ThreadPoolExecutor(8) as pool:
        for i, (p, info, err) in enumerate(pool.map(one, paths), 1):
            if info is None:
                res.unreadable.append((p, err))
            elif info.codec == "h264":
                res.h264.append(info)
            else:
                res.other.append(info)
            if on_progress:
                on_progress(i, len(paths), p)
    find_conversions(res)
    return res
