"""Builds the final file: the original's every box and track, byte for byte,
with only the H.264 video swapped for the new H.265 video.

FFmpeg alone cannot do this. When it writes MP4 it refuses or drops GoPro's
telemetry (gpmd), stabilisation (fdsc) and timecode tracks and the camera info
in udta. So FFmpeg encodes the video alone, and this file does the muxing.
"""
import hashlib, os, struct
from bisect import bisect_right
from dataclasses import dataclass


def _boxes(buf, start, end):
    pos = start
    while pos + 8 <= end:
        size, kind = struct.unpack_from(">I4s", buf, pos)
        head = 8
        if size == 1:
            size = struct.unpack_from(">Q", buf, pos + 8)[0]
            head = 16
        elif size == 0:
            size = end - pos
        if size < head or pos + size > end:
            raise ValueError(f"damaged MP4 box {kind!r}")
        yield kind, pos, pos + head, pos + size
        pos += size


def _find(buf, start, end, *path):
    for kind, b, s, e in _boxes(buf, start, end):
        if kind == path[0]:
            return (b, s, e) if len(path) == 1 else _find(buf, s, e, *path[1:])
    return None


def _box(kind, payload):
    return struct.pack(">I4s", len(payload) + 8, kind) + payload


def read_moov(path):
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        pos = 0
        while pos + 8 <= size:
            f.seek(pos)
            s, k = struct.unpack(">I4s", f.read(8))
            if s == 1:
                s = struct.unpack(">Q", f.read(8))[0]
            elif s == 0:
                s = size - pos
            if s < 8:
                raise ValueError("damaged MP4 file")
            if k == b"moov":
                f.seek(pos)
                return f.read(s)
            pos += s
    raise ValueError("this file has no index (moov), it may be cut off")


@dataclass
class Track:
    raw: bytes
    handler: bytes
    entry: bytes
    track_id: int
    sizes: list
    chunk_offsets: list
    samples_per_chunk: list
    chunk_starts: list      # seconds, used for interleaving
    timescale: int
    media_duration: int
    sample_bytes: tuple = (1, 1)    # what one listed size really covers, as a fraction

    def chunk_bytes(self):
        out, i = [], 0
        num, den = self.sample_bytes
        for n in self.samples_per_chunk:
            listed = sum(self.sizes[i:i + n]) * num
            if listed % den:
                raise ValueError("audio chunk is not a whole number of packets")
            out.append(listed // den)
            i += n
        return out


_PCM_ENTRIES = {b"sowt", b"twos", b"raw ", b"in24", b"in32", b"fl32", b"fl64", b"lpcm", b"NONE"}
_LOG_PCM_ENTRIES = {b"alaw", b"ulaw"}


def _quicktime_sample_bytes(raw, entry):
    """QuickTime audio may list every sample in stsz as size 1, whatever it really
    takes up. The true size is in the sound description at `entry`, the stsd entry."""
    fourcc = raw[entry + 4:entry + 8]
    version = struct.unpack_from(">H", raw, entry + 16)[0]
    channels, bits = struct.unpack_from(">HH", raw, entry + 24)
    if version == 1:
        per_packet, _, per_frame, _ = struct.unpack_from(">IIII", raw, entry + 36)
        num, den = per_frame, per_packet
    elif version == 2:
        num, den = struct.unpack_from(">II", raw, entry + 64)
    elif fourcc in _PCM_ENTRIES:
        num, den = channels * bits // 8, 1
    elif fourcc in _LOG_PCM_ENTRIES:
        num, den = channels, 1
    else:
        num, den = 0, 0
    if not num or not den:
        raise ValueError(f"audio format {fourcc!r} does not say how big its samples are")
    return num, den


def _parse_track(raw):
    te = len(raw)
    hd = _find(raw, 8, te, b"mdia", b"hdlr")
    handler = raw[hd[1] + 8:hd[1] + 12]
    md = _find(raw, 8, te, b"mdia", b"mdhd")
    if raw[md[1]]:
        timescale, media_dur = struct.unpack_from(">IQ", raw, md[1] + 20)
    else:
        timescale, media_dur = struct.unpack_from(">II", raw, md[1] + 12)
    st = _find(raw, 8, te, b"mdia", b"minf", b"stbl")
    if st is None:
        raise ValueError("track has no sample table")
    s, e = st[1], st[2]
    sd = _find(raw, s, e, b"stsd")
    entry = raw[sd[1] + 12:sd[1] + 16]
    z = _find(raw, s, e, b"stsz")
    fixed, cnt = struct.unpack_from(">II", raw, z[1] + 4)
    sizes = [fixed] * cnt if fixed else list(struct.unpack_from(f">{cnt}I", raw, z[1] + 12))
    co = _find(raw, s, e, b"stco")
    if co:
        c = struct.unpack_from(">I", raw, co[1] + 4)[0]
        offs = list(struct.unpack_from(f">{c}I", raw, co[1] + 8))
    else:
        co = _find(raw, s, e, b"co64")
        if co is None:
            raise ValueError("track has no chunk table")
        c = struct.unpack_from(">I", raw, co[1] + 4)[0]
        offs = list(struct.unpack_from(f">{c}Q", raw, co[1] + 8))
    sc = _find(raw, s, e, b"stsc")
    rows = struct.unpack_from(">I", raw, sc[1] + 4)[0]
    stsc = [struct.unpack_from(">III", raw, sc[1] + 8 + i * 12) for i in range(rows)]
    firsts = [r[0] for r in stsc]
    per = [stsc[bisect_right(firsts, i) - 1][1] for i in range(1, c + 1)]
    if sum(per) != cnt:
        raise ValueError("sample table does not add up")
    # Time of each chunk's first sample
    tt = _find(raw, s, e, b"stts")
    n_rows = struct.unpack_from(">I", raw, tt[1] + 4)[0]
    stts = [struct.unpack_from(">II", raw, tt[1] + 8 + i * 8) for i in range(n_rows)]
    starts, tick, r, left, delta = [], 0, 0, 0, 0
    for n_in_chunk in per:
        starts.append(tick / (timescale or 1))
        todo = n_in_chunk
        while todo:
            if left == 0:
                if r < len(stts):
                    left, delta = stts[r]
                    r += 1
                else:
                    left, delta = todo, 0
            if left == 0:
                continue
            step = min(todo, left)
            tick += step * delta
            left -= step
            todo -= step
    tk = _find(raw, 8, te, b"tkhd")
    tid = struct.unpack_from(">I", raw, tk[1] + (20 if raw[tk[1]] else 12))[0]
    sample_bytes = _quicktime_sample_bytes(raw, sd[1] + 8) if handler == b"soun" and fixed == 1 else (1, 1)
    return Track(raw, handler, entry, tid, sizes, offs, per, starts, timescale, media_dur, sample_bytes)


def parse_tracks(moov):
    return [_parse_track(moov[b:e]) for k, b, s, e in _boxes(moov, 8, len(moov)) if k == b"trak"]


def _replace_child(raw, path, new_box):
    """Rewrites nested box sizes down `path`. new_box None removes the target."""
    def rec(s, e, p):
        out = bytearray()
        for kind, cb, cs, ce in _boxes(raw, s, e):
            if kind == p[0]:
                if len(p) == 1:
                    if new_box is not None:
                        out += new_box
                else:
                    out += _box(kind, rec(cs, ce, p[1:]))
            else:
                out += raw[cb:ce]
        return bytes(out)
    return _box(raw[4:8], rec(8, len(raw), path))


STBL = (b"mdia", b"minf", b"stbl")


def _set_chunks(raw, offs, wide):
    kind = b"co64" if wide else b"stco"
    fmt = f">{len(offs)}{'Q' if wide else 'I'}"
    new = _box(kind, struct.pack(">II", 0, len(offs)) + struct.pack(fmt, *offs))
    had = b"co64" if _find(raw, 8, len(raw), *STBL, b"co64") else b"stco"
    if had == kind:
        return _replace_child(raw, STBL + (kind,), new)
    raw = _replace_child(raw, STBL + (had,), None)
    st = _find(raw, 8, len(raw), *STBL)
    return _replace_child(raw, STBL, _box(b"stbl", raw[st[1]:st[2]] + new))


def _handler_name(raw):
    hd = _find(raw, 8, len(raw), b"mdia", b"hdlr")
    return raw[hd[1] + 24:hd[2]].replace(b"\0", b"").replace(b"\r", b"").decode("latin1", "replace").strip()


def _build_video_trak(orig, enc, movie_ts, enc_movie_ts, groups, resized=False):
    """Encoded media, but the original's identity: track id, matrix (rotation),
    dimensions, timecode reference and dates."""
    o, e = orig.raw, enc.raw
    otk = _find(o, 8, len(o), b"tkhd")
    tkhd = bytearray(o[otk[0]:otk[2]])
    tv = tkhd[8]
    etk = _find(e, 8, len(e), b"tkhd")
    ev = e[etk[1]]
    enc_dur = struct.unpack_from(">Q" if ev else ">I", e, etk[1] + (28 if ev else 20))[0]
    struct.pack_into(">Q" if tv else ">I", tkhd, 8 + (28 if tv else 20), round(enc_dur * movie_ts / enc_movie_ts))
    if resized:     # the new display size, and the rotation offset that depends on it
        old_w = struct.unpack_from(">I", tkhd, len(tkhd) - 8)[0]
        new_w, new_h = struct.unpack_from(">II", e, etk[2] - 8)
        for at in (len(tkhd) - 20, len(tkhd) - 16):
            value = struct.unpack_from(">i", tkhd, at)[0]
            struct.pack_into(">i", tkhd, at, round(value * new_w / old_w) if old_w else value)
        struct.pack_into(">II", tkhd, len(tkhd) - 8, new_w, new_h)

    parts = [bytes(tkhd)]
    tref = _find(o, 8, len(o), b"tref")
    if tref:
        parts.append(o[tref[0]:tref[2]])
    ed = _find(e, 8, len(e), b"edts", b"elst")
    if ed:
        ver = e[ed[1]]
        cnt = struct.unpack_from(">I", e, ed[1] + 4)[0]
        rows = bytearray()
        for i in range(cnt):
            fmt, step = (">QqI", 20) if ver else (">IiI", 12)
            sd, mt, rate = struct.unpack_from(fmt, e, ed[1] + 8 + i * step)
            rows += struct.pack(">QqI", round(sd * movie_ts / enc_movie_ts), mt, rate)
        parts.append(_box(b"edts", _box(b"elst", struct.pack(">II", 1 << 24, cnt) + bytes(rows))))
    mdia = _find(e, 8, len(e), b"mdia")
    trak = _box(b"trak", b"".join(parts) + e[mdia[0]:mdia[2]])

    omd = _find(o, 8, len(o), b"mdia", b"mdhd")
    ov = o[omd[1]]
    created, modified = struct.unpack_from(">QQ" if ov else ">II", o, omd[1] + 4)
    lang = o[omd[1] + (32 if ov else 20):omd[1] + (34 if ov else 22)]
    new_mdhd = _box(b"mdhd", struct.pack(">IQQIQ", 1 << 24, created, modified, enc.timescale, enc.media_duration) +
                    lang + b"\0\0")
    trak = _replace_child(trak, (b"mdia", b"mdhd"), new_mdhd)

    if _handler_name(o).startswith("GoPro"):
        hd = _find(trak, 8, len(trak), b"mdia", b"hdlr")
        label = b"GoPro AV1\0" if enc.entry == b"av01" else b"GoPro H.265\0"
        trak = _replace_child(trak, (b"mdia", b"hdlr"), _box(b"hdlr", trak[hd[1]:hd[1] + 24] + label))

    rows = []
    for i, n in enumerate(groups, 1):
        if not rows or rows[-1][1] != n:
            rows.append((i, n, 1))
    stsc = _box(b"stsc", struct.pack(">II", 0, len(rows)) + b"".join(struct.pack(">III", *r) for r in rows))
    return _replace_child(trak, STBL + (b"stsc",), stsc)


def _ftyp(original, entry=b"hvc1"):
    with open(original, "rb") as f:
        _, kind = struct.unpack(">I4s", f.read(8))
        major = f.read(4) if kind == b"ftyp" else b""
    if entry == b"av01":
        return _box(b"ftyp", b"mp42" + struct.pack(">I", 1) + b"mp42isomav01")
    if major == b"qt  ":
        return _box(b"ftyp", b"qt  " + struct.pack(">I", 0x20050300) + b"qt  ")
    return _box(b"ftyp", b"mp42" + struct.pack(">I", 1) + b"mp42isomhvc1")


def graft(original, encoded, output, checkpoint=None, chunk_seconds=0.5, resized=False):
    """Writes `output`. Raises ValueError on anything it does not understand,
    in which case nothing is delivered and the original is kept."""
    omoov, emoov = read_moov(original), read_moov(encoded)
    otracks = parse_tracks(omoov)
    ev_tracks = [t for t in parse_tracks(emoov) if t.handler == b"vide"]
    ovids = [i for i, t in enumerate(otracks) if t.handler == b"vide" and t.entry in (b"avc1", b"avc3")]
    if len(ev_tracks) != 1 or not ovids:
        raise ValueError("unexpected track layout")
    ov_idx = ovids[0]
    ev = ev_tracks[0]

    def movie_timescale(m):
        mv = _find(m, 8, len(m), b"mvhd")
        return struct.unpack_from(">I", m, mv[1] + (20 if m[mv[1]] else 12))[0]
    movie_ts, enc_ts = movie_timescale(omoov), movie_timescale(emoov)

    # Sample positions in the encoded file, regrouped into short chunks so the
    # result stays interleaved and plays well when streamed from Drive.
    samples, i = [], 0
    for off, n in zip(ev.chunk_offsets, ev.samples_per_chunk):
        for _ in range(n):
            samples.append((off, ev.sizes[i]))
            off += ev.sizes[i]
            i += 1
    seconds = ev.media_duration / (ev.timescale or 1) or 1.0
    per = max(1, round(len(samples) / seconds * chunk_seconds))
    video_chunks, groups = [], []
    for idx in range(0, len(samples), per):
        take = samples[idx:idx + per]
        video_chunks.append((idx / len(samples) * seconds, sum(s for _, s in take), take))
        groups.append(len(take))

    items = []  # (seconds, track index, chunk index, bytes)
    for ti, t in enumerate(otracks):
        if ti == ov_idx:
            items += [(c[0], ti, ci, c[1]) for ci, c in enumerate(video_chunks)]
        else:
            items += [(t.chunk_starts[ci], ti, ci, b) for ci, b in enumerate(t.chunk_bytes())]
    items.sort(key=lambda x: x[:3])
    total = sum(x[3] for x in items)
    wide = total + len(omoov) + (1 << 22) >= 1 << 32

    vid_trak = _build_video_trak(otracks[ov_idx], ev, movie_ts, enc_ts, groups, resized)

    def build_moov(offsets):
        blob = bytearray()
        for ti, t in enumerate(otracks):
            blob += _set_chunks(vid_trak if ti == ov_idx else t.raw, offsets[ti], wide)
        out, wrote = bytearray(), False
        for kind, b, s, e in _boxes(omoov, 8, len(omoov)):
            if kind != b"trak":
                out += omoov[b:e]
            elif not wrote:
                out += blob
                wrote = True
        return _box(b"moov", bytes(out))

    offsets = {ti: [0] * (len(video_chunks) if ti == ov_idx else len(t.chunk_offsets))
               for ti, t in enumerate(otracks)}
    ftyp = _ftyp(original, ev.entry)
    head = 16 if wide else 8
    pos = len(ftyp) + len(build_moov(offsets)) + head
    for _, ti, ci, size in items:
        offsets[ti][ci] = pos
        pos += size
    moov = build_moov(offsets)

    with open(output, "wb") as out, open(original, "rb") as fo, open(encoded, "rb") as fe:
        out.write(ftyp)
        out.write(moov)
        out.write(struct.pack(">I4sQ", 1, b"mdat", total + 16) if wide else struct.pack(">I4s", total + 8, b"mdat"))
        for done, (_, ti, ci, size) in enumerate(items):
            if ti == ov_idx:
                for off, n in video_chunks[ci][2]:
                    fe.seek(off)
                    data = fe.read(n)
                    if len(data) != n:
                        raise ValueError("encoded video is short")
                    out.write(data)
            else:
                fo.seek(otracks[ti].chunk_offsets[ci])
                left = size
                while left:
                    data = fo.read(min(left, 1 << 20))
                    if not data:
                        raise ValueError("original is shorter than its index says")
                    out.write(data)
                    left -= len(data)
            if checkpoint and done % 64 == 0:
                checkpoint()


def nonvideo_digests(path, skip_video=True):
    """Digest of every track except the main video, to prove nothing changed."""
    moov = read_moov(path)
    out = {}
    vid_seen = False
    with open(path, "rb") as f:
        for t in parse_tracks(moov):
            if t.handler == b"vide" and t.entry in (b"avc1", b"avc3", b"hvc1", b"hev1", b"av01") and not vid_seen:
                vid_seen = True
                continue
            h = hashlib.sha256()
            for off, size in zip(t.chunk_offsets, t.chunk_bytes()):
                f.seek(off)
                left = size
                while left:
                    d = f.read(min(left, 1 << 20))
                    if not d:
                        raise ValueError("file is shorter than its index says")
                    h.update(d)
                    left -= len(d)
            out[t.track_id] = (t.entry, len(t.sizes), h.hexdigest())
    return out


def udta(path):
    moov = read_moov(path)
    u = _find(moov, 8, len(moov), b"udta")
    return moov[u[1]:u[2]] if u else b""
