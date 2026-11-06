"""A failed or larger conversion keeps the original and reports it."""
from pathlib import Path
from conftest import copy_preserving
from helpers.clips import make_clip
from helpers.media import get_times, sha256


def only_videos(folder):
    return sorted(p.name for p in Path(folder).rglob("*") if p.is_file())


def run(src, ws, **kw):
    from clipshrink.engine import Converter
    c = Converter(db_path=ws / "work" / "state.db", work_dir=ws / "work" / "tmp", encoder="x265", **kw)
    c.add_files([src])
    c.run()
    return c.record(src)


def test_below_the_bar_is_converted_flagged_and_original_untouched(get_clip, workspace):
    from helpers.media import measure_vmaf, probe, vstream
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    before, times = sha256(src), get_times(src)
    rec = run(src, workspace, ladder=[51])
    assert rec.status == "below_bar"
    assert "VMAF" in rec.reason and rec.vmaf_mean is not None and rec.vmaf_mean < 95
    assert only_videos(workspace / "videos") == ["a.mp4", "a_H265.mp4"]
    assert sha256(src) == before and get_times(src) == times
    # the score shown is the real one, measured independently
    v = measure_vmaf(rec.output, src, workspace)
    assert abs(v["mean"] - rec.vmaf_mean) < 0.5 and v["mean"] < 95
    assert vstream(probe(rec.output))["codec_name"] == "hevc"


def test_tries_stricter_settings_before_settling_below_the_bar(get_clip, workspace):
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    rec = run(src, workspace, ladder=[51, 45])
    assert rec.status == "below_bar" and rec.quality == 45, "must keep the best quality it tried"
    assert rec.encode_runs >= 1


def test_low_worst_frames_alone_also_count_as_below_the_bar():
    from clipshrink import config
    assert config.is_recommended(96.0, 91.0)
    assert not config.is_recommended(94.9, 95.0)
    assert not config.is_recommended(96.0, 89.9)
    assert not config.is_recommended(None, None)


def test_larger_conversion_keeps_original(workspace):
    # A very low bitrate source encoded at near-lossless quality must grow.
    src = make_clip(workspace / "videos" / "small.mp4", w=640, h=360, seconds=3, crf=45, telemetry=False)
    before = sha256(src)
    rec = run(src, workspace, ladder=[4])
    assert rec.status == "kept_original", rec.reason
    assert "not smaller" in rec.reason.lower()
    assert only_videos(workspace / "videos") == ["small.mp4"]
    assert sha256(src) == before


def test_encoder_failure_keeps_original(get_clip, workspace):
    # Truncated file: starts as a valid clip, encode or verification must fail.
    full = get_clip("no_audio_no_telemetry").read_bytes()
    src = workspace / "videos" / "broken.mp4"
    src.write_bytes(full[: len(full) // 3])
    before = sha256(src)
    rec = run(src, workspace)
    assert rec.status in ("failed", "kept_original")
    assert rec.reason
    assert only_videos(workspace / "videos") == ["broken.mp4"]
    assert sha256(src) == before


def test_failure_does_not_stop_the_batch(get_clip, workspace):
    from clipshrink.engine import Converter
    bad = workspace / "videos" / "bad.mp4"
    bad.write_bytes(b"garbage" * 50)
    good = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "good.mp4")
    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([bad, good])
    c.run()
    assert c.record(bad).status == "failed"
    assert c.record(good).status == "verified"


def test_no_temp_files_next_to_originals(get_clip, workspace):
    """Partial files in a Drive folder would upload. Work happens elsewhere."""
    from clipshrink.engine import Converter
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    seen = set()

    def watch(ev):
        seen.update(p.name for p in (workspace / "videos").iterdir())

    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265", on_event=watch)
    c.add_files([src])
    c.run()
    rec = c.record(src)
    assert rec.status == "verified"
    extra = {n for n in seen - {"a.mp4", Path(rec.output).name} if not n.endswith(".part")}
    assert not extra, f"temporary files appeared beside originals: {extra}"


def test_engine_refuses_a_real_h265_file_even_if_asked(workspace):
    from helpers.media import ffmpeg
    src = workspace / "videos" / "already.mp4"
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.5", "-c:v", "libx265", "-x265-params", "log-level=error", src)
    before = sha256(src)
    rec = run(src, workspace)
    assert rec.status == "kept_original" and "not H.264" in rec.reason
    assert rec.encode_runs == 0, "must not spend time encoding it"
    assert only_videos(workspace / "videos") == ["already.mp4"]
    assert sha256(src) == before
