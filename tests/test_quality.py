"""Every conversion: VMAF >= 95 mean, >= 90 1st percentile, H.265, matching
duration, frames, resolution, audio, telemetry, dates. Originals untouched."""
import pytest
from fractions import Fraction
from pathlib import Path
from conftest import CLIP_SPECS, copy_preserving, real_clips
from helpers.media import (REQUIRED_VMAF_MEAN, REQUIRED_VMAF_P1, FFMPEG, ffmpeg, get_times, measure_vmaf, probe,
                           rotation, run, sha256, tracks, udta_bytes, vstream)


def nvenc_available():
    return run([FFMPEG, "-hide_banner", "-f", "lavfi", "-i", "color=s=320x240:d=0.1", "-c:v", "hevc_nvenc",
                "-f", "null", "-"]).returncode == 0


ENCODERS = ["x265"] + (["nvenc"] if nvenc_available() else [])


def audio_digest(path):
    r = run([FFMPEG, "-v", "error", "-i", str(path), "-map", "0:a", "-c", "copy", "-f", "streamhash",
             "-hash", "sha256", "-"])
    assert r.returncode == 0, r.stderr
    return r.stdout


def assert_conversion_is_good(src, out, log_dir):
    assert Path(out).exists(), "no conversion was written"
    ps, po = probe(src), probe(out)
    vs, vo = vstream(ps), vstream(po)
    assert vo["codec_name"] == "hevc", f"not H.265: {vo['codec_name']}"
    assert (vo["width"], vo["height"]) == (vs["width"], vs["height"]), "resolution changed"
    assert rotation(vo) == rotation(vs), "rotation changed"
    assert vo["pix_fmt"].replace("yuvj", "yuv") == vs["pix_fmt"].replace("yuvj", "yuv"), "pixel format changed"
    assert vo.get("color_range") == vs.get("color_range"), "colour range changed"
    assert int(vo["nb_read_packets"]) == int(vs["nb_read_packets"]), "frame count changed"
    frame = 1 / float(Fraction(vs["avg_frame_rate"]))
    assert abs(float(vo["duration"]) - float(vs["duration"])) <= frame, "video duration changed"
    assert abs(float(po["format"]["duration"]) - float(ps["format"]["duration"])) <= frame, "file duration changed"
    # every stream decodes with no error
    r = run([FFMPEG, "-v", "error", "-i", str(out), "-map", "0:v", "-map", "0:a?", "-f", "null", "-"])
    assert r.returncode == 0 and not r.stderr.strip(), f"decode errors: {r.stderr[:300]}"
    # audio, as FFmpeg sees it
    a_s = [s for s in ps["streams"] if s["codec_type"] == "audio"]
    a_o = [s for s in po["streams"] if s["codec_type"] == "audio"]
    assert [s["codec_name"] for s in a_s] == [s["codec_name"] for s in a_o], "audio tracks changed"
    if a_s:
        assert audio_digest(src) == audio_digest(out), "audio bytes changed"
    # every non-video track (audio, telemetry, timecode, ...) byte for byte
    summary = lambda p: sorted((t["id"], t["entry"], t["name"], t["samples"], t["digest"])
                               for t in tracks(p) if t["handler"] != "vide")
    assert summary(src) == summary(out), "non-video tracks differ"
    assert udta_bytes(src) == udta_bytes(out), "camera info (udta) changed"
    # capture dates
    tags = lambda p: p["format"].get("tags", {}).get("creation_time")
    assert tags(ps) == tags(po), "capture date changed"
    st = lambda p: {s["index"]: s.get("tags", {}).get("creation_time") for s in p["streams"]}
    assert st(ps) == st(po), "track capture dates changed"
    cs, ms = get_times(src)
    co, mo = get_times(out)
    assert abs(ms - mo) < 2, "file modified date changed"
    assert abs(cs - co) < 2, "file created date changed"
    # the measured bar, on the full file, independent of the app's own number
    v = measure_vmaf(out, src, log_dir)
    assert v["frames"] == int(vs["nb_read_packets"]), "VMAF did not compare every frame"
    assert v["mean"] >= REQUIRED_VMAF_MEAN, f"VMAF mean {v['mean']:.2f}"
    assert v["p1"] >= REQUIRED_VMAF_P1, f"VMAF 1st percentile {v['p1']:.2f}"
    assert Path(out).stat().st_size < Path(src).stat().st_size, "not smaller"


def convert_one(src, work, encoder, **kw):
    from clipshrink.engine import Converter
    c = Converter(db_path=work / "state.db", work_dir=work / "tmp", encoder=encoder, **kw)
    c.add_files([src])
    c.run()
    return c.record(src)


@pytest.mark.parametrize("encoder", ENCODERS)
@pytest.mark.parametrize("name", list(CLIP_SPECS))
def test_generated_clip_conversion(name, encoder, get_clip, workspace):
    src = copy_preserving(get_clip(name), workspace / "videos" / f"{name}.mp4")
    before, times = sha256(src), get_times(src)
    rec = convert_one(src, workspace / "work", encoder)
    assert rec.status == "verified", f"{rec.status}: {rec.reason}"
    assert_conversion_is_good(src, rec.output, workspace)
    assert sha256(src) == before and get_times(src) == times, "original was touched"
    assert rec.vmaf_mean >= 95 and rec.vmaf_p1 >= 90


def test_real_clip_supplied():
    clips = real_clips()
    assert clips, "Put a real GoPro clip in tests/real_clip/"
    for c in clips:
        assert "firmware" in probe(c)["format"]["tags"] or any("GoPro" in t["name"] for t in tracks(c)), \
            f"{c.name} does not look like an untouched GoPro file"


@pytest.mark.parametrize("encoder", ENCODERS)
@pytest.mark.parametrize("clip", real_clips(), ids=lambda p: p.name)
def test_real_clip_conversion(clip, encoder, workspace):
    src = copy_preserving(clip, workspace / "videos" / clip.name)
    before, times = sha256(src), get_times(src)
    rec = convert_one(src, workspace / "work", encoder)
    assert rec.status == "verified", f"{rec.status}: {rec.reason}"
    assert_conversion_is_good(src, rec.output, workspace)
    assert sha256(src) == before and get_times(src) == times, "original was touched"


def test_telemetry_fixture_really_has_telemetry(get_clip):
    """Guards the check itself: the fixture must carry the GoPro tracks."""
    entries = {t["entry"] for t in tracks(get_clip("gopro_like_1080p_telemetry"))}
    assert {"gpmd", "fdsc", "tmcd", "mp4a"} <= entries
    assert b"GPMF" in udta_bytes(get_clip("gopro_like_1080p_telemetry"))


def test_measurement_can_fail(get_clip, workspace):
    """Guards the check itself: a visibly bad encode must fail the VMAF bar."""
    src = get_clip("no_audio_no_telemetry")
    bad = workspace / "bad.mp4"
    ffmpeg("-i", src, "-c:v", "libx265", "-crf", "51", "-x265-params", "log-level=error", bad)
    v = measure_vmaf(bad, src, workspace)
    assert v["mean"] < REQUIRED_VMAF_MEAN and v["p1"] < REQUIRED_VMAF_P1


def test_app_thresholds_are_not_weakened():
    from clipshrink import config
    assert config.VMAF_MEAN_MIN >= 95.0 and config.VMAF_P1_MIN >= 90.0
    assert REQUIRED_VMAF_MEAN == 95.0 and REQUIRED_VMAF_P1 == 90.0
