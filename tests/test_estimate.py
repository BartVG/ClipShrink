"""Savings are estimated from real test encodes, before anything converts."""
from pathlib import Path
from conftest import copy_preserving
from helpers.media import sha256


def test_estimate_uses_real_samples_and_predicts_result(get_clip, workspace):
    from clipshrink.scan import scan_folder
    from clipshrink.estimate import estimate_savings
    from clipshrink.engine import Converter
    v = workspace / "videos"
    srcs = [copy_preserving(get_clip("gopro_like_1080p_telemetry"), v / f"g{i}.mp4") for i in range(2)]
    srcs.append(copy_preserving(get_clip("fullrange_60fps_telemetry"), v / "f.mp4"))
    before = {p: sha256(p) for p in srcs}
    files = scan_folder(v).h264
    est = estimate_savings(files, encoder="x265", work_dir=workspace / "work" / "est")
    assert est.samples, "no test encodes were made"
    for s in est.samples:
        assert s.encoded_bytes > 0 and s.source_bytes > 0
        assert s.vmaf_mean is not None and s.vmaf_p1 is not None
    assert est.total_source_bytes == sum(f.size for f in files)
    assert 0 <= est.low_saved_bytes <= est.expected_saved_bytes <= est.high_saved_bytes <= est.total_source_bytes
    assert est.seconds_estimate > 0
    # nothing converted, nothing touched
    assert sorted(p.name for p in v.iterdir()) == sorted(p.name for p in srcs)
    assert {p: sha256(p) for p in srcs} == before
    # accuracy against a real batch: within 35% of the true saving
    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files(srcs)
    c.run()
    real = sum(Path(c.record(p).source).stat().st_size - Path(c.record(p).output).stat().st_size for p in srcs)
    assert real > 0
    assert abs(est.expected_saved_bytes - real) / real <= 0.35, (est.expected_saved_bytes, real)
