"""QuickTime cameras (Nikon, for one) can list every PCM audio sample in stsz as size 1,
though a 16-bit stereo sample takes 4 bytes. Reading that literally copied a quarter of
the audio and left static in the result."""
import hashlib, struct, subprocess
from pathlib import Path
import pytest
from helpers.media import FFMPEG, NOWIN, run
from clipshrink import mp4graft
from clipshrink.mp4graft import STBL, _box, _boxes, _find, _replace_child


def decoded_audio(path):
    r = subprocess.run([FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a", "-f", "s16le", "-"],
                       capture_output=True, creationflags=NOWIN)
    assert r.returncode == 0, r.stderr
    return hashlib.sha256(r.stdout).hexdigest(), len(r.stdout)


def rewrite_audio_tables(path, version):
    """Rewrites an FFmpeg MOV's sound track the way these cameras write it."""
    data = Path(path).read_bytes()
    start = next(b for k, b, _, _ in _boxes(data, 0, len(data)) if k == b"moov")
    moov = data[start:]
    assert start + len(moov) == len(data), "this needs the index at the end of the file"

    out = bytearray()
    for kind, b, _, e in _boxes(moov, 8, len(moov)):
        trak = moov[b:e]
        if kind == b"trak" and mp4graft._parse_track(trak).handler == b"soun":
            st = _find(trak, 8, len(trak), *STBL)
            z = _find(trak, st[1], st[2], b"stsz")
            real, count = struct.unpack_from(">II", trak, z[1] + 4)
            assert real == 4
            trak = _replace_child(trak, STBL + (b"stsz",), _box(b"stsz", struct.pack(">III", 0, 1, count)))
            st = _find(trak, 8, len(trak), *STBL)
            sd = _find(trak, st[1], st[2], b"stsd")
            entry = bytearray(trak[sd[1] + 8:sd[2]])
            assert entry[4:8] == b"sowt"
            assert struct.unpack_from(">H", entry, 16)[0] == 0
            if version == 1:
                struct.pack_into(">H", entry, 16, 1)
                entry[36:36] = struct.pack(">IIII", 1, 2, 4, 2)
                struct.pack_into(">I", entry, 0, len(entry))
            trak = _replace_child(trak, STBL + (b"stsd",), _box(b"stsd", trak[sd[1]:sd[1] + 8] + bytes(entry)))
        out += trak
    Path(path).write_bytes(data[:start] + _box(b"moov", bytes(out)))


@pytest.fixture
def source_and_encoded(tmp_path):
    src, enc = tmp_path / "camera.MOV", tmp_path / "encoded.mp4"
    r = run([FFMPEG, "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=320x180:r=25:d=2",
             "-f", "lavfi", "-i", "sine=f=440:r=48000:d=2", "-filter_complex", "[1:a]aformat=channel_layouts=stereo[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le", str(src)])
    assert r.returncode == 0, r.stderr
    r = run([FFMPEG, "-v", "error", "-i", str(src), "-an", "-c:v", "libx265", "-x265-params", "log-level=error",
             "-tag:v", "hvc1", str(enc)])
    assert r.returncode == 0, r.stderr
    return src, enc


@pytest.mark.parametrize("version", [0, 1])
def test_size_one_pcm_keeps_every_audio_byte(source_and_encoded, tmp_path, version):
    src, enc = source_and_encoded
    before = decoded_audio(src)
    rewrite_audio_tables(src, version)
    assert decoded_audio(src) == before, "the rewritten source must still say the same thing"

    out = tmp_path / "result.MOV"
    mp4graft.graft(src, enc, out)

    assert decoded_audio(out) == before
    sound = [t for t in mp4graft.parse_tracks(mp4graft.read_moov(out)) if t.handler == b"soun"][0]
    assert sum(sound.chunk_bytes()) == before[1], "the digest has to cover all of the audio"


def test_unknown_size_one_audio_is_refused():
    entry = struct.pack(">I4s6xH", 36, b"mp4a", 1) + struct.pack(">HH4xHH4xI", 0, 0, 2, 16, 48000 << 16)
    with pytest.raises(ValueError):
        mp4graft._quicktime_sample_bytes(entry, 0)
