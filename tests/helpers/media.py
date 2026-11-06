"""Independent test helpers. Nothing here imports the app: the check must not
trust the code it is checking."""
import ctypes, hashlib, json, os, struct, subprocess
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FFMPEG = str(ROOT / "vendor" / "ffmpeg" / "bin" / "ffmpeg.exe")
FFPROBE = str(ROOT / "vendor" / "ffmpeg" / "bin" / "ffprobe.exe")
NOWIN = 0x08000000

# The required bar. Do not lower these numbers.
REQUIRED_VMAF_MEAN = 95.0
REQUIRED_VMAF_P1 = 90.0


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                          creationflags=NOWIN, **kw)


def ffmpeg(*args, check=True):
    r = run([FFMPEG, "-hide_banner", "-nostdin", "-y", *map(str, args)])
    if check and r.returncode:
        raise AssertionError(f"ffmpeg failed: {args}\n{r.stderr[-1500:]}")
    return r


def probe(path):
    r = run([FFPROBE, "-v", "error", "-count_packets", "-show_streams", "-show_format",
             "-of", "json", str(path)])
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


def vstream(p):
    return next(s for s in p["streams"] if s["codec_type"] == "video")


def rotation(stream):
    for sd in stream.get("side_data_list", []):
        if "rotation" in sd:
            return int(sd["rotation"])
    return 0


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def percentile(values, pct):
    a = sorted(values)
    i = (len(a) - 1) * pct / 100
    lo = int(i)
    hi = min(lo + 1, len(a) - 1)
    return a[lo] + (a[hi] - a[lo]) * (i - lo)


def measure_vmaf(distorted, reference, log_dir, ref_scale=None):
    """Own VMAF measurement. 4K clips must also pass the 4K model. With ref_scale,
    the reference is shrunk to that size first."""
    p = probe(reference)
    tall = max(ref_scale or (vstream(p)["width"], vstream(p)["height"])) >= 2560
    models = "version=vmaf_v0.6.1\\:name=a" + ("|version=vmaf_4k_v0.6.1\\:name=b" if tall else "")
    log = Path(log_dir) / f"vmaf_{os.getpid()}_{abs(hash(str(distorted)))}.json"
    name = log.name
    graph = ("[0:v]setpts=PTS-STARTPTS[d];[1:v]setpts=PTS-STARTPTS" + (f",scale={ref_scale[0]}:{ref_scale[1]}:flags=lanczos" if ref_scale else "") + "[r];"
             f"[d][r]libvmaf=log_fmt=json:log_path={name}:n_threads=16:model='{models}'")
    r = run([FFMPEG, "-hide_banner", "-nostdin", "-noautorotate", "-i", str(distorted), "-noautorotate",
             "-i", str(reference), "-lavfi", graph, "-f", "null", "-"], cwd=str(log_dir))
    assert r.returncode == 0, r.stderr[-1500:]
    frames = json.loads(log.read_text())["frames"]
    log.unlink()
    out = {"frames": len(frames), "mean": 1e9, "p1": 1e9}
    for key in ["a", "b"] if tall else ["a"]:
        vals = [f["metrics"][key] for f in frames]
        out["mean"] = min(out["mean"], sum(vals) / len(vals))
        out["p1"] = min(out["p1"], percentile(vals, 1))
    return out


# --- MP4 reading, written separately from the app's muxer -------------------
def boxes(data, start=0, end=None):
    pos, end = start, len(data) if end is None else end
    while pos + 8 <= end:
        size, kind = struct.unpack_from(">I4s", data, pos)
        head = 8
        if size == 1:
            size = struct.unpack_from(">Q", data, pos + 8)[0]
            head = 16
        elif size == 0:
            size = end - pos
        yield kind.decode("latin1"), pos + head, pos + size
        pos += size


def read_moov(path):
    with open(path, "rb") as f:
        pos, total = 0, os.path.getsize(path)
        while pos + 8 <= total:
            f.seek(pos)
            size, kind = struct.unpack(">I4s", f.read(8))
            if size == 1:
                size = struct.unpack(">Q", f.read(8))[0]
            if size == 0:
                size = total - pos
            if kind == b"moov":
                f.seek(pos)
                return f.read(size)
            pos += size
    raise AssertionError(f"no moov in {path}")


def child(data, s, e, kind):
    for k, a, b in boxes(data, s, e):
        if k == kind:
            return a, b
    return None


def udta_bytes(path):
    m = read_moov(path)
    moov = next(boxes(m))
    u = child(m, moov[1], moov[2], "udta")
    return m[u[0]:u[1]] if u else b""


def tracks(path):
    """Return a list of dicts: track id, handler, sample entry, sample digest."""
    m = read_moov(path)
    _, ms, me = next(boxes(m))
    out = []
    with open(path, "rb") as f:
        for k, ts, te in boxes(m, ms, me):
            if k != "trak":
                continue
            ms2, me2 = child(m, ts, te, "mdia")
            hs, he = child(m, ms2, me2, "hdlr")
            handler = m[hs + 8:hs + 12].decode("latin1")
            name = m[hs + 24:he].replace(b"\x00", b"").decode("latin1").strip()
            mi = child(m, ms2, me2, "minf")
            ss, se = child(m, mi[0], mi[1], "stbl")
            sd = child(m, ss, se, "stsd")
            entry = m[sd[0] + 12:sd[0] + 16].decode("latin1")
            stsz = child(m, ss, se, "stsz")
            fixed, n = struct.unpack_from(">II", m, stsz[0] + 4)
            sizes = [fixed] * n if fixed else list(struct.unpack_from(f">{n}I", m, stsz[0] + 12))
            co = child(m, ss, se, "stco")
            if co:
                c = struct.unpack_from(">I", m, co[0] + 4)[0]
                chunks = struct.unpack_from(f">{c}I", m, co[0] + 8)
            else:
                co = child(m, ss, se, "co64")
                c = struct.unpack_from(">I", m, co[0] + 4)[0]
                chunks = struct.unpack_from(f">{c}Q", m, co[0] + 8)
            sc = child(m, ss, se, "stsc")
            cnt = struct.unpack_from(">I", m, sc[0] + 4)[0]
            stsc = [struct.unpack_from(">III", m, sc[0] + 8 + i * 12) for i in range(cnt)]
            h = hashlib.sha256()
            idx = 0
            total = 0
            for ci, off in enumerate(chunks, 1):
                per = next(e[1] for e in reversed(stsc) if e[0] <= ci)
                f.seek(off)
                for _ in range(per):
                    b = f.read(sizes[idx])
                    assert len(b) == sizes[idx]
                    h.update(b)
                    total += sizes[idx]
                    idx += 1
            assert idx == n, "sample table does not add up"
            tk = child(m, ts, te, "tkhd")
            version = m[tk[0]]
            tid = struct.unpack_from(">I", m, tk[0] + (20 if version else 12))[0]
            out.append(dict(id=tid, handler=handler, name=name, entry=entry, samples=n,
                            bytes=total, digest=h.hexdigest()))
    return out


# --- Windows file times -----------------------------------------------------
_k = ctypes.WinDLL("kernel32", use_last_error=True)
_k.CreateFileW.restype = wintypes.HANDLE
_k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p,
                           wintypes.DWORD, wintypes.DWORD, wintypes.HANDLE]
_k.SetFileTime.argtypes = [wintypes.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
_k.CloseHandle.argtypes = [wintypes.HANDLE]


def set_times(path, created, modified):
    def ft(t):
        v = int((t + 11644473600) * 10**7)
        return wintypes.FILETIME(v & 0xFFFFFFFF, v >> 32)
    h = _k.CreateFileW(str(path), 0x100, 3, None, 3, 0x02000000, None)
    assert h != wintypes.HANDLE(-1).value
    a, b = ft(created), ft(modified)
    assert _k.SetFileTime(h, ctypes.byref(a), None, ctypes.byref(b))
    _k.CloseHandle(h)


def get_times(path):
    st = os.stat(path)
    return st.st_ctime, st.st_mtime
