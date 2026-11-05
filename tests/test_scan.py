from pathlib import Path
from helpers.clips import make_clip
from helpers.media import ffmpeg


def test_scan_finds_every_h264_in_all_subfolders(workspace):
    from clipshrink.scan import scan_folder
    root = workspace / "videos"
    tiny = dict(w=320, h=240, seconds=0.3, telemetry=False, timecode=False)
    wanted = [root / "GX010001.MP4", root / "a" / "GH010002.mp4", root / "a" / "b" / "c" / "d" / "e" / "deep.mov",
              root / "été été" / "vidéo 日本語.mp4", root / "x" / "UPPER.MOV", root / "x y" / "with space.m4v",
              root / "mk" / "clip.mkv"]
    for w in wanted:
        make_clip(w, **tiny)
    # must NOT be listed as H.264
    hevc = root / "a" / "already.mp4"
    hevc.parent.mkdir(exist_ok=True)
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", hevc)
    (root / "a" / "notes.txt").write_text("not video")
    (root / "a" / "photo.jpg").write_bytes(b"\xff\xd8\xff")
    # Drive's own temp and the Recycle Bin are never candidates
    make_clip(root / ".tmp.drivedownload" / "partial.mp4", **tiny)
    make_clip(root / "$RECYCLE.BIN" / "deleted.mp4", **tiny)
    bad = root / "b" / "corrupt.mp4"
    bad.parent.mkdir()
    bad.write_bytes(b"this is not a video" * 100)

    res = scan_folder(root)
    assert sorted(Path(f.path) for f in res.h264) == sorted(wanted)
    assert [Path(f.path) for f in res.other] == [hevc]
    assert [Path(p) for p, _ in res.unreadable] == [bad], "unreadable video must be reported, not hidden"
    assert all(f.codec == "h264" and f.size > 0 and f.width == 320 for f in res.h264)


def test_scan_empty_folder(workspace):
    from clipshrink.scan import scan_folder
    res = scan_folder(workspace / "videos")
    assert res.h264 == [] and res.other == [] and res.unreadable == []
