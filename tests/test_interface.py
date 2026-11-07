"""What can be checked without eyes. Real ease of use is driven by hand."""
import pytest
from pathlib import Path


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
    assert "Recycle Bin" in t and "Google Drive" not in t


# --- Found by hand on a PC using Windows dark theme: tick boxes and the selected
# row were invisible, and the "kept as original" box was dark text on dark.
def _verified_row(workspace, name):
    import os
    from clipshrink import db
    a = workspace / "videos" / f"{name}.mp4"
    b = workspace / "videos" / f"{name}_(h265).mp4"
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
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    _verified_row(workspace, "one")
    _verified_row(workspace, "two")
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


def _col(t, title):
    return next(c for c in range(t.columnCount()) if t.horizontalHeaderItem(c).text().rstrip(" ▲▼") == title)


def _row_of(t, name):
    return next(i for i in range(t.rowCount()) if t.item(i, 1).text() == name)


def test_h265_files_are_listed_as_skipped_and_cannot_be_ticked(dark_review, workspace):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    w = dark_review
    t = _scan_page(w, workspace, ["a.mp4"], [("b.mp4", "hevc"), ("c.mp4", "vp9")])
    assert t.rowCount() == 3, "every video in the folder must be visible"
    b = _row_of(t, "b.mp4")
    state = _col(t, "State")
    assert "Already H.265" in t.item(b, state).text() and "skipped" in t.item(b, state).text().lower()
    assert "skipped" in t.item(_row_of(t, "c.mp4"), state).text().lower()
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
    assert config.VERSION == "1.7"
    assert config.VERSION in window.windowTitle()
    iss = (Path(__file__).resolve().parents[1] / "installer" / "clipshrink.iss").read_text(encoding="utf-8")
    assert f"AppVersion={config.VERSION}" in iss


# --- ClipShrink is for any H.264 video, and saves disk space anywhere
def test_wording_is_not_only_for_gopro(window):
    from clipshrink import config
    title = window.windowTitle()
    assert "GoPro" not in title and "videos" in title
    assert "GoPro originals" not in config.QUALITY_EXPLANATION
    assert "telemetry" in config.QUALITY_EXPLANATION, "must still promise telemetry is kept"


def test_one_video_is_singular(dark_review, workspace):
    from clipshrink.estimate import Estimate
    w = dark_review
    _scan_page(w, workspace, ["a.mp4"], [])
    w._estimate_done(Estimate(10, 5, 4, 6, 60.0, "x265", [], 1))
    assert w.conv_info.text().startswith("1 video,")
    _scan_page(w, workspace, ["a.mp4", "b.mp4"], [])
    w._estimate_done(Estimate(20, 5, 4, 6, 60.0, "x265", [], 2))
    assert w.conv_info.text().startswith("2 videos,")


# --- Reviewing a batch: sort, folders, selection buttons, warning signs
def _review_with(workspace, qapp_instance, rows):
    """rows: (name, folder, before, after, mean, p1, status)"""
    import os
    from clipshrink import db
    from clipshrink.ui import MainWindow
    dbp = workspace / "work" / "s.db"
    w = MainWindow(db_path=dbp, work_dir=workspace / "work" / "t")
    for name, folder, before, after, mean, p1, status in rows:
        d = workspace / "videos" / folder
        d.mkdir(parents=True, exist_ok=True)
        a, b = d / name, d / f"{Path(name).stem}_(h265).mp4"
        a.write_bytes(b"x" * before)
        b.write_bytes(b"y" * after)
        sa, sb = os.stat(a), os.stat(b)
        db.save(dbp, db.Record(source=str(a), status=status, source_size=sa.st_size, source_mtime_ns=sa.st_mtime_ns,
                               output=str(b), output_size=sb.st_size, output_mtime_ns=sb.st_mtime_ns,
                               vmaf_mean=mean, vmaf_p1=p1, reason="VMAF below the bar" if status == "below_bar" else ""))
    w.resize(1200, 760)
    w.show()
    w.go(3)
    qapp_instance.processEvents()
    return w


ROWS = [("b.mp4", "Trip", 900, 400, 9.5, 8.0, "below_bar"),
        ("a.mp4", "Trip/Day 2", 5000, 1000, 97.0, 92.0, "verified"),
        ("c.mp4", "Other", 12000, 6000, 93.5, 90.5, "below_bar"),
        ("d.mp4", "Other", 800, 700, 96.0, 91.0, "verified")]


def _column_values(t, title):
    c = _col(t, title)
    return [t.item(r, c).text() for r in range(t.rowCount())]


def _ticked_names(w):
    return sorted(Path(r.source).name for r in w._ticked())


def test_columns_sort_by_their_real_value(workspace, qapp_instance):
    from PySide6.QtCore import Qt
    w = _review_with(workspace, qapp_instance, ROWS)
    t = w.review
    assert t.isSortingEnabled()
    t.sortItems(_col(t, "VMAF average"), Qt.AscendingOrder)
    assert [v.strip("⚠ ") for v in _column_values(t, "VMAF average")] == ["9.5", "93.5", "96.0", "97.0"], "numbers, not text"
    t.sortItems(_col(t, "Before"), Qt.DescendingOrder)
    assert _column_values(t, "Original") == ["c.mp4", "a.mp4", "b.mp4", "d.mp4"], "12 KB above 900 bytes"
    t.sortItems(_col(t, "Original"), Qt.AscendingOrder)
    assert _column_values(t, "Original") == ["a.mp4", "b.mp4", "c.mp4", "d.mp4"]
    w.close()


def test_clicking_a_header_sorts(workspace, qapp_instance):
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    w = _review_with(workspace, qapp_instance, ROWS)
    h = w.review.horizontalHeader()
    c = _col(w.review, "Original")
    x = h.sectionViewportPosition(c) + 5
    QTest.mouseClick(h.viewport(), Qt.LeftButton, pos=QPoint(x, 5))
    first = _column_values(w.review, "Original")
    QTest.mouseClick(h.viewport(), Qt.LeftButton, pos=QPoint(x, 5))
    assert sorted(first) == sorted(_column_values(w.review, "Original"))
    assert first != _column_values(w.review, "Original") and first[0] in ("a.mp4", "d.mp4")
    w.close()


def test_ticks_and_play_follow_the_file_after_sorting(workspace, qapp_instance):
    from PySide6.QtCore import Qt
    w = _review_with(workspace, qapp_instance, ROWS)
    t = w.review
    name = _col(t, "Original")
    row = next(r for r in range(4) if t.item(r, name).text() == "a.mp4")
    w._cell_clicked(row, 0)
    t.sortItems(_col(t, "Before"), Qt.DescendingOrder)
    assert _ticked_names(w) == ["a.mp4"], "the tick must stay on its own file"
    row = next(r for r in range(4) if t.item(r, name).text() == "d.mp4")
    assert Path(w._review_rec(row).source).name == "d.mp4"
    w._cell_clicked(row, 0)
    assert _ticked_names(w) == ["a.mp4", "d.mp4"]
    w.close()


def test_every_table_has_sortable_columns(window):
    for t in (window.scan_table, window.est_table, window.conv_table, window.review):
        assert t.isSortingEnabled()


def test_folder_column_shows_where_each_file_is(workspace, qapp_instance):
    w = _review_with(workspace, qapp_instance, ROWS)
    t = w.review
    r = _row_of_named(t, "a.mp4", "Original")
    assert Path(t.item(r, _col(t, "Folder")).text()) == workspace / "videos" / "Trip" / "Day 2"
    w.close()


def _row_of_named(t, name, column):
    c = _col(t, column)
    return next(r for r in range(t.rowCount()) if t.item(r, c).text() == name)


def test_scan_and_convert_lists_also_show_the_folder(dark_review, workspace):
    t = _scan_page(dark_review, workspace, ["a.mp4"], [("b.mp4", "hevc")])
    c = _col(t, "Folder")
    assert all(Path(t.item(r, c).text()) == workspace / "videos" for r in range(2))
    assert _col(dark_review.conv_table, "Folder") is not None
    assert _col(dark_review.est_table, "Folder") is not None


def test_select_all_button_toggles(workspace, qapp_instance):
    w = _review_with(workspace, qapp_instance, ROWS)
    assert w.select_all_btn.text() == "Select All"
    w.select_all_btn.click()
    assert _ticked_names(w) == ["a.mp4", "b.mp4", "c.mp4", "d.mp4"]
    assert w.select_all_btn.text() == "Deselect All"
    w.select_all_btn.click()
    assert _ticked_names(w) == [] and w.select_all_btn.text() == "Select All"
    w.close()


def test_select_recommended_leaves_below_the_bar_out(workspace, qapp_instance):
    w = _review_with(workspace, qapp_instance, ROWS)
    assert w.select_rec_btn.text() == "Select Recommended"
    w.select_rec_btn.click()
    assert _ticked_names(w) == ["a.mp4", "d.mp4"]
    assert w.select_rec_btn.text() == "Deselect Recommended"
    w.select_rec_btn.click()
    assert _ticked_names(w) == [] and w.select_rec_btn.text() == "Select Recommended"
    w.close()


def test_selection_buttons_skip_files_that_cannot_be_deleted(workspace, qapp_instance):
    rows = ROWS + [("e.mp4", "Other", 800, 0, None, None, "kept_original")]
    w = _review_with(workspace, qapp_instance, rows)
    w.select_all_btn.click()
    assert "e.mp4" not in _ticked_names(w) and len(_ticked_names(w)) == 4
    assert w.select_all_btn.text() == "Deselect All"
    w.close()


def test_below_the_bar_has_a_warning_sign(workspace, qapp_instance):
    w = _review_with(workspace, qapp_instance, ROWS)
    t = w.review
    bad = _row_of_named(t, "c.mp4", "Original")
    good = _row_of_named(t, "a.mp4", "Original")
    assert "⚠" in t.item(bad, _col(t, "VMAF average")).text()
    assert "⚠" in t.item(bad, _col(t, "Result")).text()
    assert "⚠" not in t.item(good, _col(t, "VMAF average")).text()
    assert "⚠" not in t.item(good, _col(t, "Result")).text()
    w.close()


def test_delete_dialog_warns_when_below_the_bar_files_are_included(window):
    plain = window.delete_confirmation_text(3, 1000)
    extra = window.delete_confirmation_text(3, 1000, below_bar=2)
    assert "VMAF" not in plain or "below" not in plain.lower()
    assert "2" in extra and "below" in extra.lower() and "VMAF" in extra


def test_explanation_says_below_the_bar_is_flagged_not_refused(window):
    t = window.quality_explanation().lower()
    assert "warning" in t and "recommended" in t
    assert "95" in t and "90" in t


def test_no_google_drive_storage_warning_anywhere_in_the_window(workspace, qapp_instance):
    from PySide6.QtWidgets import QAbstractButton, QLabel, QTextBrowser
    w = _review_with(workspace, qapp_instance, ROWS)
    w.go(3)
    texts = [x.text() for x in w.findChildren(QLabel)] + [x.text() for x in w.findChildren(QAbstractButton)]
    texts += [x.toPlainText() for x in w.findChildren(QTextBrowser)]
    assert not [x for x in texts if "Google Drive" in x or "drive.google" in x]
    w.close()


# --- Sidebar: About, and Reports & Statistics
def test_about_page_says_what_this_is(window):
    window.settings_btn.click()
    t = window.about_text().replace("\n", " ")
    assert window.stack.currentWidget() is window.about_page
    assert "ClipShrink" in t and "1.7" in t and "GPL" in t and "github.com/tophe323/ClipShrink" in t
    assert "FFmpeg" in t and "mpv" in t


# --- Progress bars while deleting and renaming
def _wait(qapp_instance, w):
    import time
    end = time.time() + 30
    while w.action_running and time.time() < end:
        qapp_instance.processEvents()
        time.sleep(0.01)
    assert not w.action_running


def test_delete_and_rename_show_a_progress_bar(workspace, qapp_instance, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    from clipshrink import db, trash
    from clipshrink.engine import sha256_file
    monkeypatch.setattr(QMessageBox, "information", lambda *a, **k: None)
    w = _review_with(workspace, qapp_instance, ROWS)
    dbp = workspace / "work" / "s.db"
    for r in db.read_records(dbp):
        r.output_sha256 = sha256_file(r.output)
        db.save(dbp, r)
    monkeypatch.setattr(trash, "_send_to_recycle_bin", lambda p: (Path(p).unlink(), True)[1])
    from types import SimpleNamespace   # these small test files aren't real videos
    monkeypatch.setattr(trash.scan, "probe_file", lambda p: SimpleNamespace(codec="hevc"))
    assert w.action_bar.isHidden()
    w._action_progress("Deleting", 1, 4, "x.mp4")
    assert not w.action_bar.isHidden() and w.action_bar.maximum() == 4 and w.action_bar.value() == 1
    assert "x.mp4" in w.action_bar.format() and "Deleting" in w.action_bar.format()
    seen = []
    real = w._action_progress
    w._action_progress = lambda *a: (seen.append(a[1:3]), real(*a))
    w.select_all_btn.click()
    w.start_delete(w._ticked())
    assert not w.delete_btn.isEnabled() and not w.select_all_btn.isEnabled(), "no clicks while it works"
    _wait(qapp_instance, w)
    assert w.action_bar.isHidden()
    assert len(seen) == 5 and seen[-1] == (4, 4)
    assert sum(1 for r in db.read_records(dbp) if r.status == "original_deleted") == 4
    seen.clear()
    w.start_rename(trash.renamable(dbp))
    _wait(qapp_instance, w)
    assert len(seen) == 5 and seen[-1] == (4, 4)
    assert (workspace / "videos" / "Other" / "c.mp4").exists()
    w.close()


def test_delete_and_rename_report_progress_for_each_file(workspace):
    from clipshrink import trash
    calls = []
    trash.delete_originals(workspace / "s.db", ["a", "b"], confirmed=False, on_progress=lambda *a: calls.append(a))
    assert [c[:2] for c in calls] == [(0, 2), (1, 2), (2, 2)]
    calls.clear()
    trash.remove_suffix(workspace / "s.db", ["a"], confirmed=False, on_progress=lambda *a: calls.append(a))
    assert [c[:2] for c in calls] == [(0, 1), (1, 1)]


# --- The Convert page: cards, thin bars, filter tabs, status pills
def _conv_records(workspace, w):
    from clipshrink import db
    made = []
    for name, status, before, after in (("a.mp4", "verified", 1000, 400), ("b.mp4", "below_bar", 1000, 500),
                                        ("c.mp4", "kept_original", 500, 0), ("d.mp4", "pending", 700, 0),
                                        ("e.mp4", "pending", 300, 0)):
        made.append(db.Record(source=str(workspace / "videos" / name), status=status, source_size=before,
                              output_size=after, vmaf_mean=97.0 if after else None, vmaf_p1=92.0 if after else None))
    w._fill_conv_table([r.source for r in made])
    for r in made:
        w._show_row(r)
    return made


def _visible_names(t):
    return [t.item(r, 0).text() for r in range(t.rowCount()) if not t.isRowHidden(r)]


def test_convert_cards_show_real_totals(window, workspace):
    made = _conv_records(workspace, window)
    c = window.conv_cards
    assert c["Files Processed"].text() == "3 / 5"
    assert c["Space Saved"].text() == "1.1 KB (-55%)", "1,100 saved of the 2,000 bytes converted"
    assert c["Current Batch"].text() == "3.5 KB"
    t = window.conv_table
    assert t.item(_row_of_named(t, "a.mp4", "File"), _col(t, "% Saved")).text() == "60%"
    assert t.item(_row_of_named(t, "a.mp4", "File"), _col(t, "After")).text() != t.item(
        _row_of_named(t, "a.mp4", "File"), _col(t, "Before")).text()


def test_convert_filter_tabs(window, workspace):
    made = _conv_records(workspace, window)
    window._set_conv_stage(made[3].source, "Encoding")
    assert window.conv_tabs["Completed"].text() == "Completed  3"
    assert window.conv_tabs["Active"].text() == "Active  1"
    assert window.conv_tabs["Waiting"].text() == "Waiting  1"
    t = window.conv_table
    window.conv_tabs["Completed"].click()
    assert sorted(_visible_names(t)) == ["a.mp4", "b.mp4", "c.mp4"]
    window.conv_tabs["Active"].click()
    assert _visible_names(t) == ["d.mp4"]
    window.conv_tabs["Waiting"].click()
    assert _visible_names(t) == ["e.mp4"]
    window.conv_tabs["All"].click()
    assert len(_visible_names(t)) == 5


def test_filter_survives_sorting(window, workspace, qapp_instance):
    from PySide6.QtCore import Qt
    _conv_records(workspace, window)
    t = window.conv_table
    window.conv_tabs["Waiting"].click()
    t.sortItems(_col(t, "Before"), Qt.DescendingOrder)
    window._apply_conv_filter()
    assert sorted(_visible_names(t)) == ["d.mp4", "e.mp4"]


def test_time_remaining_wording():
    from clipshrink.ui import short_time
    assert short_time(12720) == "~3h 32m left"
    assert short_time(600) == "~10m left"
    assert short_time(5) == "~1m left"


def test_status_pills_use_meaningful_colours():
    from clipshrink.ui import pill_colours
    good, active, warn, bad, idle = [pill_colours(x)[0] for x in
                                     ("Verified", "Encoding", "⚠ Below the bar", "Failed, original kept", "Waiting")]
    assert len({good, active, warn, bad, idle}) == 5


def test_sidebar_ticks_finished_steps(window):
    window.show()
    window.go(2)
    assert [not c.isHidden() for c in window.step_checks] == [True, True, False, False]
    window.go(0)
    assert not any(not c.isHidden() for c in window.step_checks)


