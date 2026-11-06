"""AV1 output and downscaling, measured by the check's own code, not the app's."""
from pathlib import Path
import pytest
from conftest import copy_preserving, real_clips
from helpers.clips import make_clip
from helpers.media import FFMPEG, get_times, measure_vmaf, probe, rotation, run, sha256, tracks, udta_bytes, vstream
from test_quality import assert_conversion_is_good


def av1_nvenc_available():
    return run([FFMPEG, "-hide_banner", "-f", "lavfi", "-i", "color=s=1280x720:d=0.1", "-c:v", "av1_nvenc",
                "-f", "null", "-"]).returncode == 0


AV1 = ["svtav1"] + (["av1_nvenc"] if av1_nvenc_available() else [])


def convert(src, ws, encoder="x265", codec="h265", max_resolution="original", **kw):
    from clipshrink.engine import Converter
    c = Converter(db_path=ws / "work" / "state.db", work_dir=ws / "work" / "tmp", encoder=encoder, codec=codec,
                  max_resolution=max_resolution, **kw)
    c.add_files([src])
    c.run()
    return c.record(src), c


# --- AV1
@pytest.mark.parametrize("encoder", AV1)
@pytest.mark.parametrize("name", ["gopro_like_1080p_telemetry", "fullrange_60fps_telemetry", "rotated_telemetry",
                                  "uhd_4k_telemetry", "no_audio_no_telemetry"])
def test_av1_conversion_passes_every_check(name, encoder, get_clip, workspace):
    src = copy_preserving(get_clip(name), workspace / "videos" / f"{name}.mp4")
    before, times = sha256(src), get_times(src)
    rec, _ = convert(src, workspace, encoder, "av1")
    assert rec.status == "verified", f"{rec.status}: {rec.reason}"
    assert Path(rec.output).name == f"{name}_(av1).mp4"
    assert_conversion_is_good(src, rec.output, workspace, codec="av1")
    assert sha256(src) == before and get_times(src) == times


@pytest.mark.parametrize("encoder", AV1)
@pytest.mark.parametrize("clip", real_clips(), ids=lambda p: p.name)
def test_av1_on_real_clip(clip, encoder, workspace):
    src = copy_preserving(clip, workspace / "videos" / clip.name)
    rec, _ = convert(src, workspace, encoder, "av1")
    assert rec.status == "verified", f"{rec.status}: {rec.reason}"
    assert_conversion_is_good(src, rec.output, workspace, codec="av1")


def test_av1_from_mov_is_written_as_mp4(workspace):
    src = make_clip(workspace / "videos" / "a.mov", w=640, h=360, seconds=2, telemetry=False)
    rec, _ = convert(src, workspace, "svtav1", "av1")
    assert rec.status == "verified", rec.reason
    assert Path(rec.output).suffix == ".mp4", "AV1 isn't a dependable fit for a .mov file"
    assert vstream(probe(rec.output))["codec_name"] == "av1"


def test_h265_is_still_the_default(get_clip, workspace):
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    from clipshrink.engine import Converter
    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    assert Path(c.record(src).output).name == "a_(h265).mp4" and c.record(src).codec == "h265"


def test_av1_original_can_be_deleted_and_renamed(get_clip, workspace):
    import uuid
    from clipshrink.trash import delete_originals, remove_suffix
    from test_delete import purge_own_test_files, recycle_bin_has
    name = f"clipshrink_test_{uuid.uuid4().hex}.mp4"
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / name)
    rec, _ = convert(src, workspace, "svtav1", "av1")
    db = workspace / "work" / "state.db"
    assert delete_originals(db, [src], confirmed=True).deleted == [str(src)]
    purge_own_test_files(recycle_bin_has(src.name))
    assert remove_suffix(db, [src], confirmed=True).renamed
    assert src.exists() and vstream(probe(src))["codec_name"] == "av1"


def test_scan_treats_av1_as_already_converted(get_clip, workspace):
    from clipshrink.scan import scan_folder
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    rec, _ = convert(src, workspace, "svtav1", "av1")
    res = scan_folder(workspace / "videos")
    assert [Path(f.path) for f in res.h264] == [src]
    assert [Path(f.path) for f in res.other] == [Path(rec.output)]


# --- Where the resize target lands
@pytest.mark.parametrize("size,choice,want", [
    ((5312, 2988), "4k", (3840, 2160)),        # GoPro 5.3K
    ((3840, 2160), "4k", None),                # already there
    ((1920, 1080), "4k", None),                # never upscale
    ((3840, 2160), "1080p", (1920, 1080)),
    ((1280, 720), "1080p", None),
    ((1920, 1080), "720p", (1280, 720)),
    ((2704, 2028), "1080p", (1440, 1080)),     # GoPro 4:3 keeps its shape
    ((1080, 1920), "720p", (720, 1280)),       # portrait
    ((5312, 2988), "original", None),
])
def test_target_size(size, choice, want):
    from clipshrink.config import target_size
    assert target_size(*size, choice) == want


def test_target_size_is_always_even_and_keeps_the_shape():
    from clipshrink.config import target_size
    for w, h in ((5312, 2988), (2704, 1520), (4000, 3000), (1921, 1081), (3840, 1644)):
        for choice in ("4k", "1080p", "720p"):
            t = target_size(w, h, choice)
            if t:
                assert t[0] % 2 == 0 and t[1] % 2 == 0
                assert abs(t[0] / t[1] - w / h) < 0.02


# --- Downscaling, for real
def assert_resized_is_good(src, out, want, ws, codec="hevc"):
    ps, po = probe(src), probe(out)
    vs, vo = vstream(ps), vstream(po)
    assert vo["codec_name"] == codec
    assert (vo["width"], vo["height"]) == want
    assert rotation(vo) == rotation(vs)
    assert vo.get("color_range") == vs.get("color_range")
    assert int(vo["nb_read_packets"]) == int(vs["nb_read_packets"]), "frames must not be dropped"
    summary = lambda p: sorted((t["id"], t["entry"], t["name"], t["samples"], t["digest"])
                               for t in tracks(p) if t["handler"] != "vide")
    assert summary(src) == summary(out), "sound and telemetry must be untouched"
    assert udta_bytes(src) == udta_bytes(out)
    assert abs(get_times(src)[1] - get_times(out)[1]) < 2
    r = run([FFMPEG, "-v", "error", "-i", str(out), "-map", "0:v", "-f", "null", "-"])
    assert r.returncode == 0 and not r.stderr.strip()
    v = measure_vmaf(out, src, ws, ref_scale=want)
    assert v["mean"] >= 95 and v["p1"] >= 90, v
    assert Path(out).stat().st_size < Path(src).stat().st_size


def test_downscale_keeps_tracks_and_clears_the_bar_against_a_scaled_copy(get_clip, workspace):
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    before = sha256(src)
    rec, _ = convert(src, workspace, "x265", "h265", "1080p")
    assert rec.status == "verified", rec.reason
    assert rec.resized and (rec.output_width, rec.output_height) == (1920, 1080)
    assert (rec.source_width, rec.source_height) == (3840, 2160)
    assert_resized_is_good(src, rec.output, (1920, 1080), workspace)
    assert sha256(src) == before


def test_downscale_5k_to_4k(workspace):
    src = make_clip(workspace / "videos" / "GX5K.MP4", w=5312, h=2988, fps="30", seconds=1, preset="ultrafast")
    rec, _ = convert(src, workspace, "x265", "h265", "4k")
    assert rec.status == "verified", rec.reason
    assert_resized_is_good(src, rec.output, (3840, 2160), workspace)


def test_downscale_with_av1(get_clip, workspace):
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    rec, _ = convert(src, workspace, AV1[-1], "av1", "1080p")
    assert rec.status == "verified", rec.reason
    assert_resized_is_good(src, rec.output, (1920, 1080), workspace, codec="av1")


def test_downscale_keeps_full_colour_range_and_rotation(workspace):
    src = make_clip(workspace / "videos" / "a.mp4", w=1920, h=1080, seconds=2, full_range=True, rotate=90)
    rec, _ = convert(src, workspace, "x265", "h265", "720p")
    assert rec.status == "verified", rec.reason
    assert_resized_is_good(src, rec.output, (1280, 720), workspace)
    assert rotation(vstream(probe(rec.output))) != 0


def test_never_upscales(get_clip, workspace):
    src = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    rec, _ = convert(src, workspace, "x265", "h265", "4k")
    assert rec.status == "verified" and not rec.resized
    assert_conversion_is_good(src, rec.output, workspace)


def test_estimate_follows_the_settings(get_clip, workspace):
    from clipshrink.estimate import estimate_savings
    from clipshrink.scan import scan_folder
    copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    files = scan_folder(workspace / "videos").h264
    full = estimate_savings(files, encoder="x265", work_dir=workspace / "e1")
    small = estimate_savings(files, encoder="x265", work_dir=workspace / "e2", max_resolution="1080p")
    assert small.expected_saved_bytes > full.expected_saved_bytes
    av1 = estimate_savings(files, encoder="svtav1", codec="av1", work_dir=workspace / "e3")
    assert av1.encoder == "svtav1" and av1.samples


def test_resized_original_needs_its_own_confirmation(get_clip, workspace):
    import uuid
    from clipshrink.trash import delete_originals
    from test_delete import purge_own_test_files, recycle_bin_has
    name = f"clipshrink_test_{uuid.uuid4().hex}.mp4"
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / name)
    rec, _ = convert(src, workspace, "x265", "h265", "1080p")
    db = workspace / "work" / "state.db"
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused
    assert "resolution" in res.refused[0][1]
    assert delete_originals(db, [src], confirmed=True, resized_confirmed=True).deleted == [str(src)]
    purge_own_test_files(recycle_bin_has(src.name))


def test_side_by_side_works_when_sizes_differ_and_stays_in_sync(get_clip, workspace):
    from clipshrink.player import SideBySidePlayer
    from test_player import psnr
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    rec, _ = convert(src, workspace, "x265", "h265", "1080p")
    p = SideBySidePlayer(src, rec.output, mute=True)
    p.start()
    try:
        p.seek(1.0)
        shot = workspace / "s.png"
        p.screenshot(shot)
        assert psnr(shot, shot, "1920:1080:0:0", "1920:1080:1920:0") > 28
    finally:
        p.close()


def test_report_lists_codec_resolution_and_bitrate(get_clip, workspace):
    import csv
    from clipshrink.reports import list_reports, reports_dir
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    convert(src, workspace, "x265", "h265", "1080p")
    rep = list_reports(reports_dir(workspace / "work" / "state.db"))[0].path
    with open(rep, newline="", encoding="utf-8-sig") as f:
        row = next(csv.DictReader(f))
    assert row["Codec"] == "H.265" and row["Output resolution"] == "1920x1080" and float(row["Output bitrate (Mbit/s)"]) > 0
    assert row["Result"] == "Resized"
