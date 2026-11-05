"""Generates test clips: H.264 with the track layout GoPro cameras write."""
import os, random, struct
from pathlib import Path
from .media import ffmpeg, boxes, child, set_times

CREATED = 1489917792.0   # 2017-03-19 10:03:12 UTC
MODIFIED = 1489918000.0
CREATION_TAG = "2017-03-19T10:03:12.000000Z"


def _box(kind, payload):
    return struct.pack(">I4s", len(payload) + 8, kind.encode("latin1")) + payload


def _full(kind, payload, version=0, flags=0):
    return _box(kind, struct.pack(">I", version << 24 | flags) + payload)


def gpmf_payload(i, rng):
    """One second of real-format GPMF KLV: DEVC > DVID, STRM > GPS5."""
    gps = b"".join(struct.pack(">5i", 487000000 + rng.randrange(9999), 23000000 + rng.randrange(9999),
                               50000, 1200, 300) for _ in range(18))
    strm = (b"STNM" + b"c\x01\x00\x08" + b"GPS test" +
            b"GPS5" + b"l\x14\x00\x12" + gps)
    strm = b"STRM" + b"\x00\x01" + struct.pack(">H", len(strm) // 4) + strm
    dev = b"DVID" + b"L\x04\x00\x01" + struct.pack(">I", 1) + strm
    return b"DEVC" + b"\x00\x01" + struct.pack(">H", len(dev) // 4) + dev


def _trak(tid, handler_name, entry, offs, sizes, sample_ticks, timescale, duration_movie, duration_media):
    n = len(sizes)
    tkhd = _full("tkhd", struct.pack(">IIIII", 0, 0, tid, 0, duration_movie) + b"\0" * 8 +
                 struct.pack(">HHHH", 0, 0, 0, 0) +
                 struct.pack(">9I", 0x10000, 0, 0, 0, 0x10000, 0, 0, 0, 0x40000000) + struct.pack(">II", 0, 0), flags=3)
    mdhd = _full("mdhd", struct.pack(">IIIIHH", 0, 0, timescale, duration_media, 0x55C4, 0))
    hdlr = _full("hdlr", b"\0" * 4 + b"meta" + b"\0" * 12 + handler_name.encode() + b"\0")
    stsd = _full("stsd", struct.pack(">I", 1) + _box(entry, b"\0" * 6 + struct.pack(">H", 1)))
    stts = _full("stts", struct.pack(">III", 1, n, sample_ticks))
    stsc = _full("stsc", struct.pack(">IIII", 1, 1, 1, 1))
    stsz = _full("stsz", struct.pack(">II", 0, n) + b"".join(struct.pack(">I", s) for s in sizes))
    stco = _full("stco", struct.pack(">I", n) + b"".join(struct.pack(">I", o) for o in offs))
    dinf = _box("dinf", _full("dref", struct.pack(">I", 1) + _full("url ", b"", flags=1)))
    minf = _box("minf", _box("gmhd", _box("gmin", struct.pack(">IHHHHHH", 0, 0x40, 0x8000, 0x8000, 0x8000, 0, 0))) +
                dinf + _box("stbl", stsd + stts + stsc + stsz + stco))
    return _box("trak", tkhd + _box("mdia", mdhd + hdlr + minf))


def add_gopro_tracks(path, seconds):
    """Appends telemetry (gpmd), a stabilisation track (fdsc) and camera udta
    the way a GoPro does. moov must already be the last box (FFmpeg default)."""
    data = Path(path).read_bytes()
    rng = random.Random(4242)
    pos = None
    for k, a, b in boxes(data):
        if k == "moov":
            pos = (a - 8, b)
    assert pos and pos[1] == len(data), "moov must be last"
    moov = data[pos[0]:pos[1]]
    head = data[:pos[0]]
    _, ms, me = next(boxes(moov))
    kids = list(boxes(moov, ms, me))
    mvhd = child(moov, ms, me, "mvhd")
    dur = struct.unpack_from(">I", moov, mvhd[0] + 16)[0]
    next_id = struct.unpack_from(">I", moov, mvhd[0] + 96)[0]
    secs = max(1, int(seconds))
    gpmd = [gpmf_payload(i, rng) for i in range(secs)]
    fdsc = [bytes(rng.randrange(256) for _ in range(300)) for _ in range(secs)]
    udta = _box("udta", _box("FIRM", b"HD9.01.00.00") + _box("LENS", b"LAJ9031234") +
                _box("CAME", b"\x11" * 16) + _box("GPMF", gpmf_payload(0, rng)))
    # The new mdat goes where moov was, so FFmpeg's offsets stay valid.
    o = len(head) + 8
    offs_g, offs_f = [], []
    for g in gpmd:
        offs_g.append(o)
        o += len(g)
    for g in fdsc:
        offs_f.append(o)
        o += len(g)
    t1 = _trak(next_id, "GoPro MET", "gpmd", offs_g, [len(x) for x in gpmd], 1000, 1000, dur, 1000 * secs)
    t2 = _trak(next_id + 1, "GoPro SOS", "fdsc", offs_f, [len(x) for x in fdsc], 1000, 1000, dur, 1000 * secs)
    inner = bytearray()
    for k, a, b in kids:
        if k != "udta":
            inner += moov[a - 8:b]
    mv = inner.find(b"mvhd") + 4
    struct.pack_into(">I", inner, mv + 96, next_id + 2)
    new_moov = _box("moov", bytes(inner) + udta + t1 + t2)
    with open(path, "wb") as f:
        f.write(head)
        f.write(_box("mdat", b"".join(gpmd + fdsc)))
        f.write(new_moov)


def make_clip(path, w=1280, h=720, fps="30", seconds=4, crf=16, audio=True, telemetry=True,
              rotate=None, full_range=False, timecode=True, vfr=False, preset="fast"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    src = f"testsrc2=s={w}x{h}:r={fps}:d={seconds},noise=alls=9:allf=t"
    if vfr:
        src += ",select='not(eq(mod(n\\,5)\\,2))'"
    args = ["-f", "lavfi", "-i", src]
    if audio:
        args += ["-f", "lavfi", "-i", f"sine=f=440:r=48000:d={seconds}", "-c:a", "aac", "-b:a", "128k"]
    args += ["-pix_fmt", "yuv420p", "-color_range", "pc" if full_range else "tv"]
    args += ["-c:v", "libx264", "-preset", preset, "-crf", crf, "-colorspace", "bt709",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-metadata", f"creation_time={CREATION_TAG}"]
    if vfr:
        args += ["-fps_mode", "vfr"]
    if timecode:
        args += ["-timecode", "10:02:35:00"]
    tmp = path.with_name("gen_" + path.name)
    ffmpeg(*args, tmp)
    if rotate is not None:
        rot = path.with_name("rot_" + path.name)
        # FFmpeg cannot stream-copy a tmcd track into MP4, so timecode is rewritten here.
        ffmpeg("-display_rotation", rotate, "-i", tmp, "-c", "copy", "-map", "0:v", "-map", "0:a?",
               "-timecode", "10:02:35:00", "-metadata", f"creation_time={CREATION_TAG}", rot)
        os.replace(rot, tmp)
    os.replace(tmp, path)
    if telemetry:
        add_gopro_tracks(path, seconds)
    set_times(path, CREATED, MODIFIED)
    return path
