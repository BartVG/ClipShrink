"""What can be checked without eyes. Real ease of use is driven by hand."""
import pytest


@pytest.fixture(scope="session")
def qapp_instance():
    from PySide6.QtWidgets import QApplication
    return QApplication.instance() or QApplication([])


@pytest.fixture
def window(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    yield w
    w.close()


def test_explains_quality_in_plain_words(window):
    t = window.quality_explanation().lower()
    assert "vmaf" in t and "95" in t and "90" in t
    assert "lossless" in t, "must explain why not mathematically lossless"
    assert "larger" in t


def test_convert_is_locked_until_estimate_is_shown(window):
    assert not window.can_estimate()
    assert not window.can_convert()


def test_delete_dialog_names_drive_warning(window):
    t = window.delete_confirmation_text(3, 1_000_000)
    assert "Google Drive" in t and "Recycle Bin" in t and "trash" in t.lower()


# --- Found by hand on a PC using Windows dark theme: tick boxes and the selected
# row were invisible, and the "kept as original" box was dark text on dark.
def _verified_row(workspace, name):
    import os
    from clipshrink import db
    a = workspace / "videos" / f"{name}.mp4"
    b = workspace / "videos" / f"{name}_H265.mp4"
    a.write_bytes(b"x" * 1000)
    b.write_bytes(b"y" * 500)
    sa, sb = os.stat(a), os.stat(b)
    db.save(workspace / "work" / "s.db", db.Record(
        source=str(a), status="verified", source_size=sa.st_size, source_mtime_ns=sa.st_mtime_ns, output=str(b),
        output_size=sb.st_size, output_mtime_ns=sb.st_mtime_ns, vmaf_mean=97.0, vmaf_p1=92.0))
    return a, b


@pytest.fixture
def dark_review(workspace, qapp_instance):
    from PySide6.QtCore import Qt
    from clipshrink.ui import MainWindow, apply_theme
    qapp_instance.styleHints().setColorScheme(Qt.ColorScheme.Dark)
    apply_theme(qapp_instance)
    _verified_row(workspace, "one")
    _verified_row(workspace, "two")
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    w.resize(1100, 700)
    w.show()
    w.go(3)
    qapp_instance.processEvents()
    yield w
    w.close()


def _darkest(image, rect):
    return min(image.pixelColor(x, y).lightness() for x in range(rect.left(), rect.right())
               for y in range(rect.top(), rect.bottom()))


def test_tick_box_is_visible_in_dark_theme(dark_review):
    w = dark_review
    t = w.review
    r = t.visualItemRect(t.item(1, 0))
    img = t.viewport().grab(r).toImage()
    assert _darkest(img, img.rect()) < 170, "no visible tick box"


def test_selected_row_is_visible_in_dark_theme(dark_review):
    t = dark_review.review
    t.selectRow(0)
    QApp = __import__("PySide6.QtWidgets", fromlist=["QApplication"]).QApplication
    QApp.processEvents()
    selected = t.visualItemRect(t.item(0, 3))
    other = t.visualItemRect(t.item(1, 3))
    a = t.viewport().grab(selected).toImage().pixelColor(2, 2)
    b = t.viewport().grab(other).toImage().pixelColor(2, 2)
    assert abs(a.lightness() - b.lightness()) + abs(a.hue() - b.hue()) > 20, "selected row looks like the others"


def test_report_box_is_readable_in_dark_theme(dark_review):
    p = dark_review.problems.viewport().grab().toImage()
    assert p.pixelColor(p.width() - 5, p.height() - 5).lightness() > 200, "dark box"
    assert _darkest(p, p.rect()) < 120, "text not visible"


def test_clicking_anywhere_in_the_cell_ticks_and_unticks(dark_review):
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    t = dark_review.review
    r = t.visualItemRect(t.item(0, 0))
    for x, want in ((r.width() // 2, 1), (r.width() - 4, 0), (4, 1)):
        QTest.mouseClick(t.viewport(), Qt.LeftButton, pos=QPoint(r.x() + x, r.center().y()))
        assert len(dark_review._ticked()) == want
    assert dark_review.delete_btn.isEnabled()


def test_ticked_box_looks_different(dark_review):
    t = dark_review.review
    r = t.visualItemRect(t.item(0, 0))
    before = t.viewport().grab(r).toImage()
    dark_review._cell_clicked(0, 0)
    t.clearSelection()
    t.setCurrentItem(None)
    after = t.viewport().grab(r).toImage()
    assert before != after


def test_scan_list_tick_box_is_visible_and_clicks(dark_review, workspace):
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication
    from clipshrink.scan import MediaInfo, ScanResult
    w = dark_review
    f = MediaInfo(path=str(workspace / "videos" / "x.mp4"), size=10, mtime_ns=1, codec="h264", width=1920, height=1080,
                  fps=30.0, duration=5.0, frames=150, video_bytes=9)
    w.folder = str(workspace / "videos")
    w._scan_done(ScanResult(h264=[f]))
    w.go(0)
    QApplication.processEvents()
    t = w.scan_table
    r = t.visualItemRect(t.item(0, 0))
    assert _darkest(t.viewport().grab(r).toImage(), t.viewport().grab(r).toImage().rect()) < 170
    assert len(w.selected_files()) == 1
    QTest.mouseClick(t.viewport(), Qt.LeftButton, pos=r.center())
    assert w.selected_files() == []
    QTest.mouseClick(t.viewport(), Qt.LeftButton, pos=QPoint(r.x() + 3, r.center().y()))
    assert len(w.selected_files()) == 1


# --- Videos that are already H.265 are shown as skipped, and cannot be picked
def _info(path, codec):
    from clipshrink.scan import MediaInfo
    return MediaInfo(path=str(path), size=10, mtime_ns=1, codec=codec, width=1920, height=1080, fps=30.0, duration=5.0,
                     frames=150, video_bytes=9)


def _scan_page(w, workspace, h264, other):
    from PySide6.QtWidgets import QApplication
    from clipshrink.scan import ScanResult
    w.folder = str(workspace / "videos")
    w._scan_done(ScanResult(h264=[_info(workspace / "videos" / n, "h264") for n in h264],
                            other=[_info(workspace / "videos" / n, c) for n, c in other]))
    w.go(0)
    QApplication.processEvents()
    return w.scan_table


def _row_of(t, name):
    return next(i for i in range(t.rowCount()) if t.item(i, 1).text() == name)


def test_h265_files_are_listed_as_skipped_and_cannot_be_ticked(dark_review, workspace):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    w = dark_review
    t = _scan_page(w, workspace, ["a.mp4"], [("b.mp4", "hevc"), ("c.mp4", "vp9")])
    assert t.rowCount() == 3, "every video in the folder must be visible"
    b = _row_of(t, "b.mp4")
    assert "Already H.265" in t.item(b, 5).text() and "skipped" in t.item(b, 5).text().lower()
    assert "skipped" in t.item(_row_of(t, "c.mp4"), 5).text().lower()
    assert t.item(b, 0).data(Qt.CheckStateRole) is None, "must not offer a tick box"
    QTest.mouseClick(t.viewport(), Qt.LeftButton, pos=t.visualItemRect(t.item(b, 0)).center())
    assert t.item(b, 0).data(Qt.CheckStateRole) is None, "clicking must not create a tick"
    assert [f.path.endswith("a.mp4") for f in w.selected_files()] == [True]
    assert "1 video already in H.265" in w.scan_note.text()


def test_only_h265_files_cannot_move_forward(dark_review, workspace):
    w = dark_review
    t = _scan_page(w, workspace, [], [("b.mp4", "hevc")])
    assert t.rowCount() == 1 and w.selected_files() == []
    assert not w.to_estimate.isEnabled()
    assert "No H.264 videos" in w.scan_note.text()


def test_ticks_stay_on_the_right_files_with_skipped_rows_present(dark_review, workspace):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    w = dark_review
    t = _scan_page(w, workspace, ["a.mp4", "c.mp4"], [("b.mp4", "hevc")])
    QTest.mouseClick(t.viewport(), Qt.LeftButton, pos=t.visualItemRect(t.item(_row_of(t, "a.mp4"), 0)).center())
    assert [f.path.endswith("c.mp4") for f in w.selected_files()] == [True]


def test_version_is_one_place_and_shown(window):
    from pathlib import Path
    from clipshrink import config
    assert config.VERSION == "1.1"
    assert config.VERSION in window.windowTitle()
    iss = (Path(__file__).resolve().parents[1] / "installer" / "clipshrink.iss").read_text(encoding="utf-8")
    assert f"AppVersion={config.VERSION}" in iss
