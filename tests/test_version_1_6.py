"""Version 1.6: custom quality values, a simpler sidebar and About, the detected
graphics card, automatic start, and forgetting files when a batch is finished."""
import os, time
from pathlib import Path
import pytest
from conftest import copy_preserving
from helpers.clips import make_clip
from helpers.media import ffmpeg, measure_vmaf, sha256


@pytest.fixture
def win(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    yield w
    w.busy = False
    w.close()


def _wait(app, w, seconds=180):
    end = time.time() + seconds
    while w.busy and time.time() < end:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    assert not w.busy


def _save(db_path, **kw):
    from clipshrink import db
    base = dict(source="C:/Videos/a.mp4", status="verified", source_size=1000, output_size=400, vmaf_mean=97.0, vmaf_p1=92.0)
    base.update(kw)
    rec = db.Record(**base)
    db.save(db_path, rec)
    return rec


# --- The quality values, as rules
def test_default_policy_is_the_promise_and_cannot_drift():
    from clipshrink.config import DEFAULT_QUALITY as d
    assert (d.warn_mean, d.warn_p1, d.aim, d.min_mean, d.min_p1) == (95.0, 90.0, False, None, None)
    assert d.search_bar() == (95.0, 90.0)
    assert d.meets_warning(95, 90) and not d.meets_warning(94.9, 95) and not d.meets_warning(96, 89.9)
    assert d.keeps(0, 0), "by default nothing is refused for quality"


def test_aim_decides_what_the_search_looks_for():
    from clipshrink.config import QualityPolicy
    assert QualityPolicy(90, 85).search_bar() == (95.0, 90.0), "unticked: the same files as today"
    assert QualityPolicy(90, 85, aim=True).search_bar() == (90, 85)
    assert QualityPolicy(98, 95, aim=True).search_bar() == (98, 95)


def test_aiming_widens_the_settings_and_the_default_list_does_not_change():
    from clipshrink import config
    for enc, normal in config.LADDERS.items():
        assert config.ladder_for(enc, config.DEFAULT_QUALITY) == normal
        wide = config.ladder_for(enc, config.QualityPolicy(90, 85, aim=True))
        assert wide[0] > normal[0] and wide[-1] < normal[-1] and set(normal) <= set(wide)
        assert wide == sorted(wide, reverse=True), "loosest first"


def test_minimum():
    from clipshrink.config import QualityPolicy
    p = QualityPolicy(95, 90, min_mean=85, min_p1=75)
    assert p.keeps(85, 75) and not p.keeps(84.9, 90) and not p.keeps(90, 74.9)


# --- Saved settings
def test_advanced_values_are_locked_until_unlocked(workspace):
    from clipshrink.config import DEFAULT_QUALITY
    from clipshrink.settings import Settings
    s = Settings(warn_mean=80, warn_p1=70, aim=True, use_minimum=True, min_mean=50, min_p1=40)
    assert s.policy() == DEFAULT_QUALITY, "not unlocked, so the defaults apply"
    s.advanced = True
    p = s.policy()
    assert (p.warn_mean, p.warn_p1, p.aim, p.min_mean, p.min_p1) == (80, 70, True, 50, 40)
    s.use_minimum = False
    assert s.policy().min_mean is None


def test_advanced_values_are_saved(workspace):
    from clipshrink.settings import Settings, load, save
    db = workspace / "s.db"
    save(db, Settings(advanced=True, warn_mean=91.5, warn_p1=80, aim=True, use_minimum=True, min_mean=70, min_p1=60))
    s = load(db)
    assert (s.advanced, s.warn_mean, s.warn_p1, s.aim, s.use_minimum, s.min_mean, s.min_p1) == (True, 91.5, 80, True, True, 70, 60)


@pytest.mark.parametrize("bad", ['{"advanced":true,"warn_mean":500}', '{"advanced":true,"warn_mean":"x"}',
                                 '{"advanced":true,"warn_mean":90,"warn_p1":80,"use_minimum":true,"min_mean":95,"min_p1":50}'])
def test_impossible_saved_values_fall_back_to_the_defaults(workspace, bad):
    from clipshrink.config import DEFAULT_QUALITY
    from clipshrink.settings import load, path_for
    path_for(workspace / "s.db").write_text(bad)
    assert load(workspace / "s.db").policy() == DEFAULT_QUALITY


# --- What it does to real conversions
def _convert(src, ws, quality, **kw):
    from clipshrink.engine import Converter
    c = Converter(db_path=ws / "work" / "state.db", work_dir=ws / "work" / "tmp", encoder="x265", quality=quality, **kw)
    c.add_files([src])
    c.run()
    return c.record(src)


def test_lower_warning_without_aim_makes_the_same_file_and_no_warning(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    rec = _convert(src, workspace, QualityPolicy(10, 5), ladder=[51])
    assert rec.status == "verified" and (rec.target_mean, rec.target_p1) == (10, 5)
    assert rec.vmaf_mean < 95, "this encode is poor, and the low warning values accept it"


def test_aiming_low_makes_a_smaller_file_than_the_default(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    a = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    b = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "b.mp4")
    normal = _convert(a, workspace, QualityPolicy())
    low = _convert(b, workspace, QualityPolicy(85, 75, aim=True))
    assert low.status == "verified", low.reason
    assert low.output_size < normal.output_size * 0.9
    v = measure_vmaf(low.output, b, workspace)
    assert v["mean"] >= 85 and v["p1"] >= 75, "it must still meet the values asked for"


def test_aiming_high_makes_a_larger_file_than_the_default(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    a = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    b = copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "b.mp4")
    normal = _convert(a, workspace, QualityPolicy())
    high = _convert(b, workspace, QualityPolicy(98, 96, aim=True))
    assert high.output_size > normal.output_size


def test_high_warning_without_aim_warns_on_the_same_file(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    a = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    rec = _convert(a, workspace, QualityPolicy(99.9, 99.9))
    assert rec.status == "below_bar" and "target" in rec.reason.lower()
    assert 95 <= rec.vmaf_mean


def test_below_the_minimum_keeps_the_original_and_writes_nothing(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    before = sha256(src)
    rec = _convert(src, workspace, QualityPolicy(95, 90, min_mean=90, min_p1=80), ladder=[51])
    assert rec.status == "kept_original" and "minimum" in rec.reason.lower()
    assert rec.vmaf_mean < 90 and not rec.output
    assert sorted(p.name for p in (workspace / "videos").iterdir()) == ["a.mp4"]
    assert sha256(src) == before


def test_above_the_minimum_is_delivered_with_its_warning(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    rec = _convert(src, workspace, QualityPolicy(95, 90, min_mean=1, min_p1=0), ladder=[51])
    assert rec.status == "below_bar" and Path(rec.output).exists()


def test_estimate_follows_the_aim(get_clip, workspace):
    from clipshrink.config import QualityPolicy
    from clipshrink.estimate import estimate_savings
    from clipshrink.scan import scan_folder
    copy_preserving(get_clip("gopro_like_1080p_telemetry"), workspace / "videos" / "a.mp4")
    files = scan_folder(workspace / "videos").h264
    normal = estimate_savings(files, encoder="x265", work_dir=workspace / "e1")
    low = estimate_savings(files, encoder="x265", work_dir=workspace / "e2", quality=QualityPolicy(85, 75, aim=True))
    assert low.expected_saved_bytes > normal.expected_saved_bytes


# --- Labels and safety
def test_labels_are_honest_about_custom_values(workspace):
    from clipshrink import config, db
    label = lambda **k: config.status_text(db.Record(source="a", status="verified", **k))
    assert label() == "Verified"
    assert label(target_mean=95.0, target_p1=90.0) == "Verified"
    assert label(target_mean=90.0, target_p1=85.0) == "Verified at 90 / 85"
    assert label(target_mean=98.0, target_p1=96.5) == "Verified at 98 / 96.5"
    assert label(target_mean=90.0, target_p1=85.0, source_width=3840, output_width=1920) == "Resized at 90 / 85"


def test_later_changes_never_relabel_a_finished_file(win, workspace):
    from clipshrink import db
    from clipshrink.ui import result_cell
    p = workspace / "work" / "s.db"
    rec = _save(p, target_mean=90.0, target_p1=85.0, vmaf_mean=92.0, vmaf_p1=86.0)
    assert result_cell(db.get(p, rec.source)).text() == "Verified at 90 / 85"
    win.advanced_box.setChecked(True)
    win.warn_mean_box.setValue(99)
    assert result_cell(db.get(p, rec.source)).text() == "Verified at 90 / 85"


def test_warning_sign_follows_the_values_stored_with_the_file():
    from clipshrink import db
    r = db.Record(source="a", status="verified", vmaf_mean=92.0, vmaf_p1=86.0, target_mean=90.0, target_p1=85.0)
    assert r.meets_target
    assert not db.Record(source="a", status="verified", vmaf_mean=92.0, vmaf_p1=86.0).meets_target


def test_deleting_below_the_default_needs_the_extra_confirmation_even_if_it_met_a_lower_target(get_clip, workspace):
    import uuid
    from clipshrink.config import QualityPolicy
    from clipshrink.trash import delete_originals
    from test_delete import purge_own_test_files, recycle_bin_has
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / f"clipshrink_test_{uuid.uuid4().hex}.mp4")
    rec = _convert(src, workspace, QualityPolicy(10, 5), ladder=[51])
    assert rec.status == "verified"
    db = workspace / "work" / "state.db"
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused
    assert delete_originals(db, [src], confirmed=True, below_bar_confirmed=True).deleted == [str(src)]
    purge_own_test_files(recycle_bin_has(src.name))


def test_report_records_the_values_used(get_clip, workspace):
    import csv
    from clipshrink.config import QualityPolicy
    from clipshrink.reports import reports_dir
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    _convert(src, workspace, QualityPolicy(10, 5), ladder=[51])
    rep = next(reports_dir(workspace / "work" / "state.db").glob("*.csv"))
    with open(rep, newline="", encoding="utf-8-sig") as f:
        row = next(csv.DictReader(f))
    assert float(row["Target average"]) == 10 and float(row["Target worst 1%"]) == 5


# --- The Advanced section
def test_advanced_section_starts_locked_with_its_disclaimer(win):
    from clipshrink import config
    assert not win.advanced_box.isChecked()
    for w in (win.warn_mean_box, win.warn_p1_box, win.aim_box, win.minimum_box, win.min_mean_box, win.min_p1_box):
        assert not w.isEnabled(), w
    text = win.advanced_note.text()
    assert "know what you" in text and config.DOCS_URL in text and win.advanced_note.openExternalLinks()
    assert "read" in win.advanced_box.text() and "understand" in win.advanced_box.text()


def test_unlocking_enables_the_section_and_relocking_keeps_the_values(win, workspace):
    from clipshrink.config import DEFAULT_QUALITY
    from clipshrink.settings import load
    win.advanced_box.setChecked(True)
    assert win.warn_mean_box.isEnabled() and win.aim_box.isEnabled() and win.minimum_box.isEnabled()
    assert not win.min_mean_box.isEnabled(), "the minimum has its own switch"
    win.warn_mean_box.setValue(90)
    win.warn_p1_box.setValue(85)
    win.aim_box.setChecked(True)
    assert win.settings.policy().search_bar() == (90, 85)
    win.minimum_box.setChecked(True)
    assert win.min_mean_box.isEnabled()
    win.advanced_box.setChecked(False)
    assert win.settings.policy() == DEFAULT_QUALITY
    assert not win.warn_mean_box.isEnabled()
    saved = load(workspace / "work" / "s.db")
    assert (saved.warn_mean, saved.warn_p1, saved.aim) == (90, 85, True)


def test_minimum_can_never_go_above_the_warning_values(win):
    win.advanced_box.setChecked(True)
    win.minimum_box.setChecked(True)
    win.warn_mean_box.setValue(80)
    win.warn_p1_box.setValue(70)
    win.min_mean_box.setValue(95)
    win.min_p1_box.setValue(95)
    assert win.min_mean_box.value() <= 80 and win.min_p1_box.value() <= 70
    win.warn_mean_box.setValue(60)
    assert win.min_mean_box.value() <= 60


def test_changing_advanced_values_clears_the_estimate(win):
    from clipshrink.estimate import Estimate
    win._estimate_done(Estimate(10, 5, 4, 6, 60.0, "x265", [], 1))
    assert win.can_convert()
    win.advanced_box.setChecked(True)
    win.warn_mean_box.setValue(90)
    assert not win.can_convert()


def test_note_on_the_saving_page_shows_the_values_in_use(win):
    assert "95" in win.est_target_note.text() and "90" in win.est_target_note.text()
    win.advanced_box.setChecked(True)
    win.warn_mean_box.setValue(88)
    assert "88" in win.est_target_note.text()


def test_advanced_doc_page_exists():
    from conftest import ROOT
    assert (ROOT / "docs" / "user-guide" / "advanced-settings.md").exists()


# --- Sidebar and About
def test_sidebar_is_settings_then_about_at_the_bottom(win):
    assert win.sidebar_buttons() == ["Settings", "About"]
    assert not hasattr(win, "reports_btn") and not hasattr(win, "why_btn")


def test_about_has_the_docs_link_quality_explanation_and_reports_folder(win):
    from clipshrink import config
    from clipshrink.reports import reports_dir
    win.about_btn.click()
    text = win.about_text()
    assert config.DOCS_URL in win.about_browser.toHtml()
    assert 'What does "no quality loss" mean?' in text
    assert "lossless" in text.lower() and "VMAF" in text
    assert str(reports_dir(win.db_path)) in text
    assert "openpyxl" not in text


def test_about_links_open_outside_the_app_including_the_folder(win, monkeypatch):
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QDesktopServices
    from clipshrink.reports import reports_dir
    opened = []
    monkeypatch.setattr(QDesktopServices, "openUrl", lambda u: opened.append(u.toString()) or True)
    win._about_link(QUrl.fromLocalFile(str(reports_dir(win.db_path))))
    assert opened and opened[0].startswith("file:")
    assert reports_dir(win.db_path).exists(), "the folder must exist when it's opened"


def test_reports_are_still_written_and_the_statistics_are_gone():
    import clipshrink.reports as r
    assert hasattr(r, "write_batch_report")
    for gone in ("statistics", "export_reports", "list_reports", "delete_reports"):
        assert not hasattr(r, gone)


# --- The detected graphics card
def _gpu(monkeypatch, name, works):
    from clipshrink import encode
    monkeypatch.setattr(encode, "gpu_name", lambda: name)
    monkeypatch.setattr(encode, "encoder_available", lambda enc: enc in works)


def test_card_is_named_when_it_works(win, monkeypatch):
    _gpu(monkeypatch, "NVIDIA GeForce RTX 5080", {"nvenc", "av1_nvenc"})
    win._apply_settings_view()
    assert "NVIDIA GeForce RTX 5080 detected" in win.hardware_box.itemText(0)
    assert win.hardware_box.model().item(0).isEnabled()
    assert win.hardware_box.currentData() == "gpu"


def test_no_card_greys_it_out_and_selects_the_processor(win, monkeypatch):
    _gpu(monkeypatch, None, set())
    win._apply_settings_view()
    assert not win.hardware_box.model().item(0).isEnabled()
    assert win.hardware_box.currentData() == "cpu"
    assert "no compatible graphics card" in win.hardware_box.itemText(0).lower()
    assert "only NVIDIA" in win.using_label.text()
    assert "no gpu" not in win.using_label.text().lower()


def test_card_found_but_unable_says_so(win, monkeypatch):
    _gpu(monkeypatch, "NVIDIA GeForce GTX 750", set())
    win._apply_settings_view()
    assert "NVIDIA GeForce GTX 750" in win.using_label.text() and "can't" in win.using_label.text()
    assert win.hardware_box.currentData() == "cpu"


def test_check_is_per_format_and_the_choice_comes_back(win, monkeypatch, workspace):
    from clipshrink.settings import load
    _gpu(monkeypatch, "NVIDIA GeForce RTX 2060", {"nvenc"})
    win._apply_settings_view()
    assert win.hardware_box.currentData() == "gpu"
    win.codec_box.setCurrentIndex(win.codec_box.findData("av1"))
    assert win.hardware_box.currentData() == "cpu" and not win.hardware_box.model().item(0).isEnabled()
    assert "AV1" in win.using_label.text()
    win.codec_box.setCurrentIndex(win.codec_box.findData("h265"))
    assert win.hardware_box.currentData() == "gpu", "the choice wasn't overwritten by the fallback"
    assert load(workspace / "work" / "s.db").hardware == "gpu"


def test_gpu_name_reads_the_driver_tool_and_copes_without_it(monkeypatch):
    from types import SimpleNamespace
    from clipshrink import encode, tools
    encode._GPU_NAME.clear()
    monkeypatch.setattr(tools, "run", lambda cmd, **k: SimpleNamespace(returncode=0, stdout="NVIDIA GeForce RTX 5080\nNVIDIA Other\n"))
    assert encode.gpu_name() == "NVIDIA GeForce RTX 5080"
    encode._GPU_NAME.clear()

    def missing(cmd, **k):
        raise FileNotFoundError()
    monkeypatch.setattr(tools, "run", missing)
    assert encode.gpu_name() is None
    encode._GPU_NAME.clear()


# --- Wording
def test_the_word_is_target_not_bar(win):
    from clipshrink import config
    from test_interface import _col
    assert _col(win.est_table, "Meets the quality target?") is not None
    assert config.STATUS_TEXT["below_bar"] == "⚠ Below target"
    assert "bar" not in win.quality_explanation().lower().replace("barely", "")


# --- Automatic start
def test_step_2_button_starts_the_work_and_there_is_no_second_start_button(win, workspace, qapp_instance, get_clip):
    from clipshrink.estimate import Estimate
    from clipshrink.scan import scan_folder
    copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    assert not hasattr(win, "start_btn")
    assert "Start converting" in win.to_convert.text() and not win.to_convert.isEnabled()
    win.folder = str(workspace / "videos")
    win._show_scan(scan_folder(workspace / "videos"))
    win._estimate_done(Estimate(10, 5, 4, 6, 60.0, "x265", [], 1))
    win.to_convert.click()
    assert win.stack.currentIndex() == 2 and win.busy
    _wait(qapp_instance, win)
    assert win.conv_cards["Files Processed"].text() == "1 / 1"


def test_returning_to_step_3_does_not_restart(win, workspace, qapp_instance, get_clip):
    from clipshrink.estimate import Estimate
    from clipshrink.scan import scan_folder
    copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    win.folder = str(workspace / "videos")
    win._show_scan(scan_folder(workspace / "videos"))
    win._estimate_done(Estimate(10, 5, 4, 6, 60.0, "x265", [], 1))
    win.to_convert.click()
    _wait(qapp_instance, win)
    first = win.converter
    win.go(3)
    win.go(2)
    win.go(4)
    win.go(2)
    assert win.converter is first and not win.busy


def test_nothing_left_to_convert_is_said_plainly(win, workspace, qapp_instance, get_clip):
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    win.start_batch([str(src)])
    _wait(qapp_instance, win)
    win.start_batch([str(src)])
    _wait(qapp_instance, win)
    assert "nothing left to convert" in win.overall_lab.text().lower()


# --- Start Over and forgetting
def test_start_over_forgets_everything_and_returns_to_step_1(win, workspace, qapp_instance, get_clip):
    from clipshrink import db
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    win.folder = str(workspace / "videos")
    win.start_batch([str(src)])
    _wait(qapp_instance, win)
    out = Path(db.get(win.db_path, src).output)
    win.go(3)
    assert win.review.rowCount() == 1
    assert win.start_over_btn.isEnabled()
    win.start_over_btn.click()
    assert win.stack.currentIndex() == 0
    assert db.read_records(win.db_path) == []
    assert win.scan_table.rowCount() == 0 and win.folder_lab.text() == "No folder chosen"
    assert win.conv_table.rowCount() == 0 and win.conv_cards["Files Processed"].text() == "–"
    assert src.exists() and out.exists(), "Start Over never touches files"
    win.go(3)
    assert win.review.rowCount() == 0
    assert list(win.db_path.parent.joinpath("reports").glob("*.csv")), "reports stay"


def test_start_over_is_off_while_a_batch_runs(win):
    win.busy = True
    win.go(3)
    assert not win.start_over_btn.isEnabled()
    win.busy = False
    win.go(3)
    assert win.start_over_btn.isEnabled()


def test_exit_forgets_a_finished_batch(workspace, qapp_instance, get_clip):
    from clipshrink import db
    from clipshrink.ui import MainWindow
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    p = workspace / "work" / "s.db"
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    w.start_batch([str(src)])
    _wait(qapp_instance, w)
    assert db.read_records(p)
    w.close()
    assert db.read_records(p) == []


def test_starting_the_app_forgets_a_finished_batch_after_an_unclean_exit(workspace, qapp_instance):
    from clipshrink import db
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    _save(p, status="verified")
    _save(p, source="C:/Videos/b.mp4", status="original_deleted")
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    assert db.read_records(p) == []
    w.close()


def test_your_restored_file_case_is_no_longer_confused(workspace, qapp_instance):
    """An H.264 original restored over its conversion must simply be convertible."""
    from clipshrink import db
    from clipshrink.scan import scan_folder
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    src = make_clip(workspace / "videos" / "a.mp4", w=320, h=240, seconds=0.5, telemetry=False, timecode=False)
    _save(p, source=str(src), status="original_deleted")
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    w.folder = str(workspace / "videos")
    w._show_scan(scan_folder(workspace / "videos"))
    assert [f.path for f in w.selected_files()] == [str(src)]
    from test_interface import _col
    assert w.scan_table.item(0, _col(w.scan_table, "State")).text() == "Ready"
    w.close()


def test_unfinished_batch_survives_exit_and_start(workspace, qapp_instance):
    from clipshrink import db
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    src = workspace / "videos" / "a.mp4"
    src.write_bytes(b"x")
    _save(p, source=str(src), status="pending")
    _save(p, source=str(workspace / "videos" / "done.mp4"), status="verified")
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    assert len(db.read_records(p)) == 2, "crash recovery still needs them"
    w.close()
    assert len(db.read_records(p)) == 2


def test_declining_to_continue_forgets_and_clears_scraps(workspace, qapp_instance, monkeypatch):
    from PySide6.QtWidgets import QMessageBox
    from clipshrink import db
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    src = workspace / "videos" / "a.mp4"
    src.write_bytes(b"x")
    scrap = workspace / "work" / "t" / "job_123"
    scrap.mkdir(parents=True)
    part = workspace / "videos" / "a_(h265).mp4.part"
    part.write_bytes(b"half")
    _save(p, source=str(src), status="encoding")
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.No)
    w._offer_resume()
    assert db.read_records(p) == [] and not scrap.exists() and not part.exists() and src.exists()
    w.close()


def test_accepting_to_continue_lists_the_whole_batch_in_step_4(workspace, qapp_instance, monkeypatch, get_clip):
    from PySide6.QtWidgets import QMessageBox
    from clipshrink import db
    from clipshrink.ui import MainWindow
    p = workspace / "work" / "s.db"
    a = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    st = os.stat(a)
    _save(p, source=str(a), status="pending", source_size=st.st_size, source_mtime_ns=st.st_mtime_ns, output_size=0)
    _save(p, source=str(workspace / "videos" / "done.mp4"), status="verified")
    w = MainWindow(db_path=p, work_dir=workspace / "work" / "t")
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.Yes)
    w._offer_resume()
    _wait(qapp_instance, w)
    w.go(3)
    assert w.review.rowCount() == 2
    w.close()


# --- "Already has a conversion", decided from the folder alone
@pytest.mark.parametrize("beside", ["a_(h265).mp4", "a_(av1).mp4", "a_(1080p)_(h265).mp4", "a_(h265)_2.mp4", "a_H265.mp4", "a_AV1.mp4"])
def test_conversion_beside_is_recognised_without_any_memory(workspace, beside):
    from clipshrink.scan import scan_folder
    v = workspace / "videos"
    src = make_clip(v / "a.mp4", w=320, h=240, seconds=0.3, telemetry=False, timecode=False)
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", v / beside)
    res = scan_folder(v)
    assert res.has_conversion[str(src)] == str(v / beside)


def test_a_name_alone_is_not_enough(workspace):
    from clipshrink.scan import scan_folder
    v = workspace / "videos"
    tiny = dict(w=320, h=240, seconds=0.3, telemetry=False, timecode=False)
    src = make_clip(v / "a.mp4", **tiny)
    make_clip(v / "a_(h265).mp4", **tiny)    # named like a conversion, but it's H.264
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", v / "ab_(h265).mp4")
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", v / "other.mp4")
    assert str(src) not in scan_folder(v).has_conversion


def test_same_name_in_another_folder_does_not_count(workspace):
    from clipshrink.scan import scan_folder
    v = workspace / "videos"
    src = make_clip(v / "one" / "a.mp4", w=320, h=240, seconds=0.3, telemetry=False, timecode=False)
    (v / "two").mkdir()
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", v / "two" / "a_(h265).mp4")
    assert str(src) not in scan_folder(v).has_conversion


def test_listed_unticked_with_a_clear_label_and_can_be_ticked(win, workspace, qapp_instance):
    from clipshrink.scan import scan_folder
    from test_interface import _col
    v = workspace / "videos"
    src = make_clip(v / "a.mp4", w=320, h=240, seconds=0.3, telemetry=False, timecode=False)
    ffmpeg("-f", "lavfi", "-i", "testsrc2=s=320x240:d=0.3", "-c:v", "libx265", "-x265-params", "log-level=error", v / "a_(h265).mp4")
    win.folder = str(v)
    win._show_scan(scan_folder(v))
    t = win.scan_table
    r = next(i for i in range(t.rowCount()) if t.item(i, 1).text() == "a.mp4")
    assert t.item(r, _col(t, "State")).text() == "Already has a conversion"
    assert win.selected_files() == []
    win._scan_cell_clicked(r, 0)
    assert [f.path for f in win.selected_files()] == [str(src)]
    other = next(i for i in range(t.rowCount()) if t.item(i, 1).text() == "a_(h265).mp4")
    assert "converted by this tool" in t.item(other, _col(t, "State")).text()


# --- The icon
def test_icon_file_is_a_real_windows_icon_with_every_size():
    import struct
    from clipshrink import tools
    data = Path(tools.icon_path()).read_bytes()
    reserved, kind, count = struct.unpack_from("<HHH", data)
    assert (reserved, kind) == (0, 1) and count >= 5
    sizes = {data[6 + i * 16] or 256 for i in range(count)}
    assert {16, 32, 48, 256} <= sizes


def test_window_uses_the_icon(win):
    assert not win.windowIcon().isNull()
    assert {(s.width(), s.height()) for s in win.windowIcon().availableSizes()} >= {(16, 16), (256, 256)}


def test_icon_has_transparent_corners():
    from PySide6.QtCore import QSize
    from PySide6.QtGui import QIcon
    from clipshrink import tools
    img = QIcon(tools.icon_path()).pixmap(QSize(256, 256)).toImage()
    assert img.pixelColor(1, 1).alpha() == 0 and img.pixelColor(254, 254).alpha() == 0
    assert img.pixelColor(128, 128).alpha() == 255


def test_exe_and_installer_are_told_about_the_icon():
    from conftest import ROOT
    assert '--icon "assets\\clipshrink.ico"' in (ROOT / "build.bat").read_text(encoding="utf-8")
    assert '"assets\\clipshrink.ico;assets"' in (ROOT / "build.bat").read_text(encoding="utf-8")
    assert "SetupIconFile=..\\assets\\clipshrink.ico" in (ROOT / "installer" / "clipshrink.iss").read_text(encoding="utf-8")
