"""FFmpeg commands: encode, measure VMAF, and find the right quality setting."""
import json, os, subprocess, threading, time
from dataclasses import dataclass, field
from pathlib import Path
from . import config, tools


class Stopped(Exception):
    """The user stopped the batch."""


class Gate:
    """Pause and stop for whatever FFmpeg process is running right now."""
    def __init__(self):
        self.paused = False
        self.stop = False
        self._proc = None
        self._lock = threading.Lock()
        self._ev = threading.Event()
        self._ev.set()

    def pause(self):
        with self._lock:
            self.paused = True
            self._ev.clear()
            if self._proc and self._proc.poll() is None:
                tools.suspend(self._proc)

    def resume(self):
        with self._lock:
            self.paused = False
            self._ev.set()
            if self._proc and self._proc.poll() is None:
                tools.resume(self._proc)

    def request_stop(self):
        with self._lock:
            self.stop = True
            self._ev.set()
            if self._proc and self._proc.poll() is None:
                tools.resume(self._proc)
                self._proc.kill()

    def checkpoint(self):
        self._ev.wait()
        if self.stop:
            raise Stopped()

    def attach(self, proc):
        with self._lock:
            self._proc = proc
            if self.stop:
                proc.kill()
            elif self.paused:
                tools.suspend(proc)

    def detach(self):
        with self._lock:
            self._proc = None


def run_ffmpeg(args, gate=None, on_time=None, cwd=None):
    """Runs FFmpeg with a progress feed. Returns (returncode, stderr tail)."""
    if gate:
        gate.checkpoint()
    cmd = [tools.ffmpeg(), "-hide_banner", "-nostdin", "-v", "error", "-progress", "pipe:1", "-nostats"]
    cmd += [str(a) for a in args]
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         encoding="utf-8", errors="replace", creationflags=tools.NOWIN, cwd=cwd)
    tools.bind_to_us(p)
    if gate:
        gate.attach(p)
    err = []
    t = threading.Thread(target=lambda: err.extend(p.stderr.readlines()), daemon=True)
    t.start()
    try:
        for line in p.stdout:
            if on_time and line.startswith("out_time_us="):
                v = line.split("=")[1].strip()
                if v.lstrip("-").isdigit():
                    on_time(int(v) / 1e6)
        p.wait()
    finally:
        if gate:
            gate.detach()
    t.join(5)
    if gate:
        gate.checkpoint()
    return p.returncode, "".join(err)[-1500:]


_TESTED = {}


def encoder_available(name):
    """A short real encode, because a card can be present but unable to do it."""
    if name not in _TESTED:
        ff = {"nvenc": "hevc_nvenc", "av1_nvenc": "av1_nvenc", "x265": "libx265", "svtav1": "libsvtav1"}[name]
        r = tools.run([tools.ffmpeg(), "-hide_banner", "-v", "error", "-f", "lavfi", "-i", "color=s=1280x720:d=0.1",
                       "-c:v", ff, "-f", "null", "-"])
        _TESTED[name] = r.returncode == 0
    return _TESTED[name]


def resolve_encoder(name, codec="h265"):
    """gpu and auto use the NVIDIA card if it works, otherwise the processor."""
    card, processor = ("av1_nvenc", "svtav1") if codec == "av1" else ("nvenc", "x265")
    if name in ("gpu", "auto"):
        return card if encoder_available(card) else processor
    if name == "cpu":
        return processor
    return name


def encoder_args(encoder, q, info):
    color = []
    for flag, val in (("-color_range", info.color_range), ("-colorspace", info.color_space),
                      ("-color_primaries", info.color_primaries), ("-color_trc", info.color_trc)):
        if val and val != "unknown":
            color += [flag, val]
    if encoder == "nvenc":
        v = ["-c:v", "hevc_nvenc", "-preset", "p7", "-tune", "hq", "-rc", "vbr", "-cq", q, "-b:v", "0",
             # Without a high cap NVENC silently limits itself near 25 Mbit/s and ignores -cq.
             "-maxrate", "800M", "-bufsize", "1600M",
             "-spatial_aq", "1", "-temporal_aq", "1", "-rc-lookahead", "32", "-bf", "3"]
    elif encoder == "x265":
        v = ["-c:v", "libx265", "-crf", q, "-preset", "medium", "-x265-params", "log-level=error"]
    elif encoder == "av1_nvenc":
        # Unlike H.265, this one misbehaves with a high -maxrate: it ignores -cq and makes huge files.
        v = ["-c:v", "av1_nvenc", "-preset", "p7", "-tune", "hq", "-rc", "vbr", "-cq", q, "-b:v", "0",
             "-spatial-aq", "1", "-temporal-aq", "1", "-rc-lookahead", "32", "-bf", "3"]
    elif encoder == "svtav1":
        v = ["-c:v", "libsvtav1", "-crf", q, "-preset", "6", "-svtav1-params", "enable-qm=1"]
    else:
        raise ValueError(f"unknown encoder {encoder}")
    return v + color + (["-tag:v", "hvc1"] if config.ENCODER_CODEC[encoder] == "h265" else [])


def _scale(target):
    return f"scale={target[0]}:{target[1]}:flags=lanczos"


def encode_video(src, out, encoder, q, info, gate=None, on_time=None, target=None):
    """Video track only. Every timestamp is kept: no frames added or dropped."""
    args = ["-y", "-noautorotate", "-i", src, "-map", "0:v:0", "-an", "-sn", "-dn", "-map_metadata", "-1",
            "-fps_mode", "passthrough", "-enc_time_base", "demux"]
    if target:
        args += ["-vf", _scale(target)]
    args += encoder_args(encoder, q, info) + [out]
    return run_ffmpeg(args, gate, on_time)


def percentile(values, pct):
    a = sorted(values)
    i = (len(a) - 1) * pct / 100
    lo = int(i)
    hi = min(lo + 1, len(a) - 1)
    return a[lo] + (a[hi] - a[lo]) * (i - lo)


@dataclass
class Score:
    mean: float
    p1: float
    frames: int

    def passes(self, margin=0.0):
        return self.mean >= config.VMAF_MEAN_MIN + margin and self.p1 >= config.VMAF_P1_MIN + margin


def measure_vmaf(distorted, reference, info, work_dir, gate=None, on_time=None, target=None):
    """Scores every frame, no skipping. 4K must also pass the 4K VMAF model.
    With a target size, the comparison is against a copy of the original shrunk to it."""
    big = max(target or (info.width, info.height)) >= 2560
    models = "version=vmaf_v0.6.1\\:name=hd" + ("|version=vmaf_4k_v0.6.1\\:name=uhd" if big else "")
    log = "vmaf.json"
    threads = max(2, (os.cpu_count() or 4) - 2)
    graph = ("[0:v]setpts=PTS-STARTPTS[d];[1:v]setpts=PTS-STARTPTS" + (f",{_scale(target)}" if target else "") + "[r];"
             f"[d][r]libvmaf=log_fmt=json:log_path={log}:n_threads={threads}:model='{models}'")
    code, err = run_ffmpeg(["-noautorotate", "-i", Path(distorted).resolve(), "-noautorotate", "-i",
                            Path(reference).resolve(), "-lavfi", graph, "-f", "null", "-"], gate, on_time,
                           cwd=str(work_dir))
    path = Path(work_dir) / log
    if code or not path.exists():
        raise RuntimeError(f"the VMAF comparison could not run: {err.strip()[-300:]}")
    frames = json.loads(path.read_text())["frames"]
    path.unlink()
    if not frames:
        raise RuntimeError("the VMAF comparison returned no frames")
    worst = Score(1e9, 1e9, len(frames))
    for key in ["hd", "uhd"] if big else ["hd"]:
        vals = [f["metrics"][key] for f in frames]
        worst.mean = min(worst.mean, sum(vals) / len(vals))
        worst.p1 = min(worst.p1, percentile(vals, 1))
    return worst


def cut_segments(src, info, work_dir, count=3, seconds=4.0, gate=None):
    """Copies short pieces of the file, untouched, to the work folder.
    Short files are used whole."""
    if info.duration <= count * seconds * 1.5:
        return [(0.0, Path(src))]
    out = []
    for i in range(count):
        at = info.duration * (i + 1) / (count + 1)
        seg = Path(work_dir) / f"seg_{i}.mp4"
        code, err = run_ffmpeg(["-y", "-ss", f"{at:.3f}", "-i", src, "-t", f"{seconds:.3f}", "-map", "0:v:0",
                                "-c", "copy", "-an", "-sn", "-dn", "-map_metadata", "-1", seg], gate)
        if code:
            raise RuntimeError(f"could not read a sample from the file: {err.strip()[-300:]}")
        out.append((at, seg))
    return out


@dataclass
class SampleRow:
    at: float
    segment: Path
    encoded_bytes: int
    score: Score
    encode_seconds: float
    vmaf_seconds: float


@dataclass
class SearchResult:
    index: int
    passed: bool
    rows: dict = field(default_factory=dict)  # ladder index -> [SampleRow]


def search_quality(segments, encoder, ladder, info, work_dir, guess=None, gate=None, on_step=None, target=None):
    """Finds the loosest setting (smallest file) whose samples clear the bar.
    Falls back to the strictest setting, passed=False, if none clears it."""
    res = SearchResult(index=len(ladder) - 1, passed=False)

    def try_rung(i):
        rows, ok = [], True
        for n, (at, seg) in enumerate(segments):
            out = Path(work_dir) / f"try_{i}_{n}.mp4"
            t0 = time.time()
            code, err = encode_video(seg, out, encoder, ladder[i], info, gate, target=target)
            t1 = time.time()
            if code or not out.exists():
                raise RuntimeError(f"the encoder failed: {err.strip()[-300:]}")
            s = measure_vmaf(out, seg, info, work_dir, gate, target=target)
            rows.append(SampleRow(at, Path(seg), out.stat().st_size, s, t1 - t0, time.time() - t1))
            out.unlink()
            ok = ok and s.passes(config.SAMPLE_MARGIN)
        res.rows[i] = rows
        if on_step:
            on_step(i)
        return ok

    lo, hi, best = 0, len(ladder) - 1, None
    if guess is not None and 0 <= guess < len(ladder):
        if try_rung(guess):
            best, hi = guess, guess - 1
        else:
            lo = guess + 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if try_rung(mid):
            best, hi = mid, mid - 1
        else:
            lo = mid + 1
    if best is not None:
        res.index, res.passed = best, True
    return res
