"""Left pane steps, player start and space bar, GoPro LRV clean-up, and output names."""
from pathlib import Path
import pytest
from conftest import copy_preserving
from clipshrink import config, db, engine, scan, trash


@pytest.fixture
def window(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    yield w
    w.close()


def wait_for(check, ms):
    from PySide6.QtTest import QTest
    for _ in range(ms // 20):
        if check():
            return True
        QTest.qWait(20)
    return bool(check())


def click(widget):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    QTest.mouseClick(widget, Qt.LeftButton)


# --- Leaving a side page by clicking the current step
@pytest.mark.parametrize("button", ["settings_btn"])
@pytest.mark.parametrize("stage", [0, 3])
def test_current_step_leaves_a_side_page(window, button, stage):
    window.go(stage)
    getattr(window, button).click()
    assert window.stack.currentIndex() >= 4
    click(window.steps[stage])
    assert window.stack.currentIndex() == stage and window.stage == stage


def test_other_steps_do_not_jump(window):
    window.go(2)
    window.settings_btn.click()
    about = window.stack.currentIndex()
    click(window.steps[0])
    click(window.steps[3])
    assert window.stack.currentIndex() == about and window.stage == 2


# --- The player starts by itself, and space pauses it
class FakePlayer:
    def __init__(self, *a, **k):
        self.paused = True

    def start(self):
        pass

    def play(self):
        self.paused = False

    def pause(self):
        self.paused = True

    def is_paused(self):
        return self.paused

    def position(self):
        return 1.0

    def duration(self):
        return 10.0

    zoom = None
    centre = (0.5, 0.5)
    src_width = src_height = 1920
    conv_width = conv_height = None

    def set_detail(self, on):
        self.set_view(1 if on else None)

    def set_view(self, zoom, centre=None):
        self.zoom = zoom
        if centre is not None:
            self.centre = centre

    def close(self):
        pass


@pytest.fixture
def player_window(monkeypatch, qapp_instance):
    from PySide6.QtTest import QTest
    from clipshrink import ui
    monkeypatch.setattr(ui, "SideBySidePlayer", FakePlayer)
    w = ui.PlayerWindow(None, db.Record(source="a.mp4", output="b.mp4", vmaf_mean=97.0, vmaf_p1=93.0))
    w.show()
    w.activateWindow()
    assert QTest.qWaitForWindowActive(w)
    w.begin()
    yield w
    w.close()


def test_player_is_playing_as_soon_as_it_opens(player_window):
    assert player_window.player.is_paused() is False
    assert player_window.play_btn.text() == "Pause"


@pytest.mark.parametrize("focus", ["detail_btn", "play_btn", "next_btn", "slider"])
def test_space_pauses_and_resumes_whatever_has_the_focus(player_window, focus):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    w = player_window
    target = getattr(w, focus)
    target.setFocus()
    QTest.keyClick(target, Qt.Key_Space)
    assert w.player.is_paused() is True, "space pauses, exactly once"
    QTest.keyClick(target, Qt.Key_Space)
    assert w.player.is_paused() is False
    assert not w.detail_btn.isChecked(), "space must not press the highlighted button"


# --- GoPro LRV files
def touch(path, data=b"x" * 10):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


@pytest.mark.parametrize("preview, original", [
    ("GL010123.LRV", "GH010123.MP4"),
    ("GL010123.LRV", "GX010123.mp4"),
    ("GOPR0123.LRV", "GOPR0123.MP4"),
    ("GP010123.LRV", "GP010123.MP4"),
    ("GL010123.LRV", "GX010123_(h265).mp4"),
    ("GL010123.LRV", "GX010123_(1080p)_(h265).mp4"),
    ("GL010123.LRV", "GX010123_H265.mp4"),
])
def test_lrv_finds_its_original(tmp_path, preview, original):
    lrv = touch(tmp_path / preview)
    touch(tmp_path / original)
    assert Path(scan.lrv_original(lrv)).name == original


@pytest.mark.parametrize("other", ["GL010124.LRV", "GH010124.MP4", "GH0101234.MP4", "GL010123.txt", "GL010123.THM"])
def test_lrv_alone_has_no_original(tmp_path, other):
    lrv = touch(tmp_path / "GL010123.LRV")
    touch(tmp_path / other)
    assert scan.lrv_original(lrv) is None


def test_recycling_keeps_lrv_without_an_original(tmp_path, monkeypatch):
    monkeypatch.setattr(trash, "_send_to_recycle_bin", lambda p: (Path(p).unlink(), True)[1])
    paired = touch(tmp_path / "GL010001.LRV")
    touch(tmp_path / "GX010001.MP4")
    alone = touch(tmp_path / "GL010002.LRV")
    video = touch(tmp_path / "GX010003.MP4")
    res = trash.recycle_previews([str(paired), str(alone), str(video)])
    assert res.deleted == [str(paired)]
    assert not paired.exists() and alone.exists() and video.exists()
    assert (tmp_path / "GX010001.MP4").exists()
    assert {Path(p).name for p, _ in res.refused} == {"GL010002.LRV", "GX010003.MP4"}


def scan_window(window, clip, folder, monkeypatch, answer):
    """A real scan of one video with a preview beside it and one on its own."""
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QMessageBox
    copy_preserving(clip, folder / "GX010001.MP4")
    copy_preserving(clip, folder / "GL010001.LRV")
    copy_preserving(clip, folder / "GL010002.LRV")
    asked = []
    monkeypatch.setattr(QMessageBox, "question", lambda s, title, text, *a: (asked.append(text), answer)[1])
    monkeypatch.setattr(QMessageBox, "information", lambda *a, **k: None)
    monkeypatch.setattr(trash, "_send_to_recycle_bin", lambda p: (Path(p).unlink(), True)[1])
    window.start_scan(folder)
    wait_for(lambda: bool(asked), 30000)
    return asked


def table_names(window):
    return {window.scan_table.item(r, 1).text() for r in range(window.scan_table.rowCount())}


def test_lrv_prompt_explains_and_yes_recycles(window, get_clip, workspace, monkeypatch):
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QMessageBox
    folder = workspace / "videos"
    asked = scan_window(window, get_clip("no_audio_no_telemetry"), folder, monkeypatch, QMessageBox.Yes)
    assert len(asked) == 1
    text = asked[0]
    assert "Found 1 GoPro LRV file" in text and "low-resolution" in text and "original video" in text
    assert "1 other LRV file will stay" in text
    assert wait_for(lambda: not (folder / "GL010001.LRV").exists() and "GL010001.LRV" not in table_names(window), 10000)
    assert (folder / "GL010002.LRV").exists() and (folder / "GX010001.MP4").exists()
    assert table_names(window) == {"GX010001.MP4", "GL010002.LRV"}
    assert wait_for(window.to_estimate.isEnabled, 5000)


def test_lrv_prompt_no_changes_nothing(window, get_clip, workspace, monkeypatch):
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QMessageBox
    folder = workspace / "videos"
    scan_window(window, get_clip("no_audio_no_telemetry"), folder, monkeypatch, QMessageBox.No)
    QTest.qWait(200)
    assert (folder / "GL010001.LRV").exists() and (folder / "GL010002.LRV").exists()
    assert "GL010001.LRV" in table_names(window)
    assert [Path(f.path).name for f in window.selected_files()] == ["GX010001.MP4"], "previews stay unticked"


def test_no_prompt_without_a_paired_lrv(window, get_clip, workspace, monkeypatch):
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QMessageBox
    asked = []
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: asked.append(a))
    clip = get_clip("no_audio_no_telemetry")
    copy_preserving(clip, workspace / "videos" / "GX010001.MP4")
    copy_preserving(clip, workspace / "videos" / "GL010002.LRV")
    window.start_scan(workspace / "videos")
    assert wait_for(lambda: window.result is not None, 30000)
    QTest.qWait(200)
    assert asked == []


# --- Output names
@pytest.mark.parametrize("codec, size, name", [
    ("h265", None, "clip_(h265).mp4"),
    ("av1", None, "clip_(av1).mp4"),
    ("h265", "4k", "clip_(4k)_(h265).mp4"),
    ("h265", "1080p", "clip_(1080p)_(h265).mp4"),
    ("av1", "720p", "clip_(720p)_(av1).mp4"),
    ("h265", "original", "clip_(h265).mp4"),
])
def test_output_names(codec, size, name):
    assert engine.output_path_for("D:/v/clip.mp4", codec, size).name == name


def test_crash_scraps_are_found_under_old_and_new_names(tmp_path):
    src = tmp_path / "clip.mp4"
    names = {p.name for p in engine._part_files(src)}
    assert {"clip_(h265).mp4.part", "clip_(1080p)_(h265).mp4.part", "clip_(720p)_(av1).mp4.part",
            "clip_H265.mp4.part", "clip_AV1.mp4.part"} <= names


def convert(src, ws, max_resolution):
    c = engine.Converter(db_path=ws / "work" / "s.db", work_dir=ws / "work" / "t", encoder="x265",
                         max_resolution=max_resolution)
    c.add_files([src])
    c.run()
    return c.record(src)


def test_shrunk_conversion_has_both_tags(get_clip, workspace):
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    assert config.target_size(640, 360, "720p") is None
    rec = convert(src, workspace, "720p")
    assert Path(rec.output).name == "a_(h265).mp4", "not shrunk, so no size tag"


def test_size_tag_when_really_shrunk(get_clip, workspace):
    src = copy_preserving(get_clip("rotated_telemetry"), workspace / "videos" / "a.mp4")
    rec = convert(src, workspace, "720p")
    assert rec.output.endswith("a_(h265).mp4")
    src = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "b.mp4")
    rec = convert(src, workspace, "720p")
    assert rec.status in ("verified", "below_bar"), rec.reason
    assert Path(rec.output).name == "b_(720p)_(h265).mp4"
    assert rec.output_width == 1280


def test_same_name_gets_a_number(get_clip, workspace):
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    touch(workspace / "videos" / "a_(h265).mp4", b"someone's file")
    rec = convert(src, workspace, "original")
    assert Path(rec.output).name == "a_(h265)_2.mp4"
    assert (workspace / "videos" / "a_(h265).mp4").read_bytes() == b"someone's file"


def test_rename_removes_every_tag(get_clip, workspace, monkeypatch):
    monkeypatch.setattr(trash, "_send_to_recycle_bin", lambda p: (Path(p).unlink(), True)[1])
    src = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    rec = convert(src, workspace, "720p")
    dbp = workspace / "work" / "s.db"
    assert trash.delete_originals(dbp, [src], confirmed=True, below_bar_confirmed=True, resized_confirmed=True).deleted
    res = trash.remove_suffix(dbp, [src], confirmed=True)
    assert [Path(new) for _, new in res.renamed] == [src]
    assert Path(rec.output).name == "a_(720p)_(h265).mp4" and src.exists()


def test_hint_shows_the_new_names(window):
    from clipshrink import settings as app_settings
    window.settings = app_settings.Settings(codec="av1", max_resolution="1080p")
    window._apply_settings_view()
    assert "_(av1)" in window.conv_hint.text() and "_(1080p)_(av1)" in window.conv_hint.text()
    assert window.rename_btn.text() == "Remove the added tags from names"
