"""Version 1.6.1: taskbar icon, resizable columns, VMAF tooltips, Welcome screen."""
import ast
from pathlib import Path
import pytest
from conftest import ROOT


@pytest.fixture
def win(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    w.show()
    yield w
    w.close()


def _col(t, title):
    return next(c for c in range(t.columnCount()) if t.horizontalHeaderItem(c).text() == title)


def _rec(**kw):
    from clipshrink import db
    base = dict(source="C:/Some/Very/Long/Folder/Name/That/Goes/On/And/On/a.mp4", status="verified", source_size=10_000_000,
                output_size=5_000_000, vmaf_mean=97.0, vmaf_p1=92.0)
    base.update(kw)
    return db.Record(**base)


# --- Taskbar icon
def test_built_app_does_not_set_its_own_taskbar_id():
    """Without a matching shortcut, that ID is the leading suspect for the generic taskbar icon."""
    source = (ROOT / "clipshrink" / "ui.py").read_text(encoding="utf-8")
    assert "SetCurrentProcessExplicitAppUserModelID" in source
    before = source.split("SetCurrentProcessExplicitAppUserModelID")[0].rsplit("\n", 2)[1]
    assert 'getattr(sys, "frozen", False)' in before and "not " in before, "only when run from source"


# --- Resizable columns
def test_every_column_on_every_table_can_be_dragged(win):
    from PySide6.QtWidgets import QHeaderView
    for t in (win.scan_table, win.est_table, win.conv_table, win.review):
        h = t.horizontalHeader()
        modes = [h.sectionResizeMode(c) for c in range(t.columnCount())]
        assert all(m == QHeaderView.Interactive for m in modes), t
        assert h.stretchLastSection(), "no gap at the right"


def test_columns_start_fitted_to_their_content(win):
    rec = _rec()
    win._fill_conv_table([rec.source])
    win._show_row(rec)
    t = win.conv_table
    state = _col(t, "State")
    assert t.columnWidth(_col(t, "File")) >= t.fontMetrics().horizontalAdvance("a.mp4")
    assert t.columnWidth(state) >= t.sizeHintForColumn(state)


def test_a_dragged_width_is_kept_as_rows_update(win):
    rec = _rec()
    win._fill_conv_table([rec.source])
    t = win.conv_table
    c = _col(t, "File")
    t.horizontalHeader().resizeSection(c, 333)
    win._show_row(rec)
    win._set_conv_stage(rec.source, "Encoding")
    assert t.columnWidth(c) == 333


def test_a_long_folder_doesnt_push_everything_off_screen(win):
    rec = _rec(source="C:/" + "/".join(["a long folder name"] * 12) + "/a.mp4")
    win._fill_conv_table([rec.source])
    win._show_row(rec)
    t = win.conv_table
    assert t.columnWidth(_col(t, "Folder")) <= 340


def test_start_over_goes_back_to_fitted_columns(win):
    t = win.conv_table
    win._fill_conv_table([_rec().source])
    t.horizontalHeader().resizeSection(_col(t, "File"), 333)
    win.start_over()
    rec = _rec()
    win._fill_conv_table([rec.source])
    win._show_row(rec)
    assert t.columnWidth(_col(t, "File")) != 333


# --- Tooltips
AVG = ("How close this video looks to the original, from 0 to 100. VMAF is a score made by Netflix, based on how people "
       "see video. At 95 or above, most people can't see a difference.")
WORST = ("The score of the worst moments: 1% of the video's frames score lower than this. It catches a short bad patch "
         "that a good average would hide. The target is 90 or above.")


@pytest.mark.parametrize("table, average, worst", [("est_table", "VMAF average", "VMAF worst 1%"),
                                                   ("conv_table", "VMAF average", "Worst 1%"),
                                                   ("review", "VMAF average", "Worst 1%")])
def test_tooltips_explain_vmaf_on_every_page(win, table, average, worst):
    t = getattr(win, table)
    assert t.horizontalHeaderItem(_col(t, average)).toolTip() == AVG
    assert t.horizontalHeaderItem(_col(t, worst)).toolTip() == WORST


def test_tooltips_use_custom_values_without_misusing_the_claim(win):
    t = win.conv_table
    win.advanced_box.setChecked(True)
    win.warn_mean_box.setValue(90)
    win.warn_p1_box.setValue(85)
    avg = t.horizontalHeaderItem(_col(t, "VMAF average")).toolTip()
    worst = t.horizontalHeaderItem(_col(t, "Worst 1%")).toolTip()
    assert "At 95 or above, most people" in avg, "the claim is about 95, whatever the target is"
    assert "Your target is 90." in avg
    assert "The target is 85 or above." in worst
    win.advanced_box.setChecked(False)
    assert t.horizontalHeaderItem(_col(t, "VMAF average")).toolTip() == AVG


# --- Welcome
def test_app_opens_on_welcome_with_the_agreed_text(win):
    assert win.stack.currentWidget() is win.welcome_page
    text = win.welcome_text()
    for bit in ("Welcome to ClipShrink", "Shrink your videos, keep the quality.", "Zero guesswork", "Measured frame-by-frame",
                "You stay in control", "No bitrates or codecs to configure", "right compression balance",
                "Netflix's VMAF visual quality metric", "clearly flagged", "new files alongside your originals",
                "side by side", "Recycle Bin"):
        assert bit in text, bit
    for promise in ("guarantee", "100%", "identical"):
        assert promise not in text, "the app can't promise this"


def test_welcome_is_not_a_numbered_step(win):
    assert len(win.steps) == 4
    assert win.steps[0].text().startswith("1")
    assert win.stage == 0


def test_choose_folder_goes_straight_to_the_scan(win, workspace, monkeypatch):
    from clipshrink import ui
    started = []
    monkeypatch.setattr(ui.QFileDialog, "getExistingDirectory", lambda *a, **k: str(workspace / "videos"))
    monkeypatch.setattr(win, "start_scan", lambda d: started.append(d))
    win.welcome_choose.click()
    assert started == [str(workspace / "videos")]
    assert win.stack.currentIndex() == 0


def test_cancelling_the_folder_picker_stays_on_welcome(win, monkeypatch):
    from clipshrink import ui
    monkeypatch.setattr(ui.QFileDialog, "getExistingDirectory", lambda *a, **k: "")
    win.welcome_choose.click()
    assert win.stack.currentWidget() is win.welcome_page


def test_dont_show_again_is_remembered_and_can_be_undone(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    p, t = workspace / "work" / "s.db", workspace / "work" / "t"
    w = MainWindow(db_path=p, work_dir=t)
    assert not w.welcome_skip.isChecked()
    w.welcome_skip.setChecked(True)
    w.close()
    w = MainWindow(db_path=p, work_dir=t)
    assert w.stack.currentIndex() == 0, "straight to step 1"
    assert not w.show_welcome_box.isChecked()
    w.show_welcome_box.setChecked(True)
    w.close()
    w = MainWindow(db_path=p, work_dir=t)
    assert w.stack.currentWidget() is w.welcome_page
    w.close()


def test_back_to_the_defaults_brings_welcome_back_on(workspace, qapp_instance):
    from clipshrink.settings import load
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    w.welcome_skip.setChecked(True)
    w.settings_reset.click()
    assert load(p).skip_welcome is False and not w.welcome_skip.isChecked() and w.show_welcome_box.isChecked()
    w.close()


def test_start_over_goes_to_step_1_not_welcome(win):
    win.start_over()
    assert win.stack.currentIndex() == 0


def test_resuming_after_a_crash_doesnt_stop_at_welcome(workspace, qapp_instance, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    from clipshrink import db
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    src = workspace / "videos" / "a.mp4"
    src.write_bytes(b"x")
    db.save(p, db.Record(source=str(src), status="pending"))
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    assert w.stack.currentIndex() == 0, "no Welcome while a batch waits"
    w.close()


def test_changing_a_setting_keeps_the_welcome_choice(win):
    win.welcome_skip.setChecked(True)
    win.details_box.setChecked(True)
    assert win.settings.skip_welcome is True


def test_welcome_docs_exist():
    text = (ROOT / "docs" / "getting-started" / "first-batch.md").read_text(encoding="utf-8")
    assert "Welcome" in text
    assert (ROOT / "docs" / "images" / "0-welcome.png").exists()
