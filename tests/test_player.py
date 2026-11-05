"""Side by side playback: proves left and right show the same frame."""
import re, time
from conftest import copy_preserving
from helpers.media import FFMPEG, run, ffmpeg


def psnr(a, b, a_crop, b_crop):
    r = run([FFMPEG, "-hide_banner", "-i", str(a), "-i", str(b), "-lavfi",
             f"[0:v]crop={a_crop}[x];[1:v]crop={b_crop}[y];[x][y]psnr", "-f", "null", "-"])
    m = re.search(r"average:([\d.]+|inf)", r.stderr)
    assert m, r.stderr[-800:]
    return float(m.group(1))


def test_side_by_side_is_in_sync(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.player import SideBySidePlayer
    src = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    out = c.record(src).output
    p = SideBySidePlayer(src, out, mute=True)
    p.start()
    try:
        crop_l, crop_r = "1920:1080:0:0", "1920:1080:1920:0"
        for t in (0.5, 1.5, 3.0):
            p.seek(t)
            shot = workspace / f"shot_{t}.png"
            p.screenshot(shot)
            assert abs(p.position() - t) < 0.1
            same = psnr(shot, shot, crop_l, crop_r)
            # the moving test pattern: frames 5 apart must differ, or this proves nothing
            ref = workspace / f"ref_{t}.png"
            ffmpeg("-ss", t - 5 / 30, "-i", src, "-frames:v", 1, ref)
            off = psnr(shot, ref, crop_l, "1920:1080:0:0")
            assert same > 30, f"left and right differ at {t}s: {same} dB"
            assert same > off + 2, f"test pattern not discriminating: {same} vs {off}"
        # also after it has actually been playing
        p.play()
        time.sleep(1.0)
        p.pause()
        shot = workspace / "shot_play.png"
        p.screenshot(shot)
        assert psnr(shot, shot, crop_l, crop_r) > 30
    finally:
        p.close()


def test_player_has_detail_mode(get_clip, workspace):
    from clipshrink.player import SideBySidePlayer
    src = get_clip("uhd_4k_telemetry")
    p = SideBySidePlayer(src, src, mute=True)
    p.start()
    try:
        p.set_detail(True)
        p.seek(0.5)
        shot = workspace / "d.png"
        p.screenshot(shot)
        assert shot.stat().st_size > 0
    finally:
        p.close()
