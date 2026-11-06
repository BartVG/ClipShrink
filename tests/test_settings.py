"""The Settings page and what it controls."""
import json
from pathlib import Path
import pytest


def test_defaults_when_nothing_is_saved(workspace):
    from clipshrink.settings import load
    s = load(workspace / "s.db")
    assert (s.hardware, s.codec, s.max_resolution, s.show_details) == ("gpu", "h265", "original", False)


def test_saved_choices_come_back(workspace):
    from clipshrink.settings import Settings, load, save
    save(workspace / "s.db", Settings("cpu", "av1", "4k", True))
    s = load(workspace / "s.db")
    assert (s.hardware, s.codec, s.max_resolution, s.show_details) == ("cpu", "av1", "4k", True)


@pytest.mark.parametrize("content", ["not json", "[]", '{"codec":"mpeg2","hardware":7,"max_resolution":"8k","show_details":"yes"}'])
def test_bad_settings_file_falls_back_to_defaults(workspace, content):
    from clipshrink.settings import load, path_for
    path_for(workspace / "s.db").write_text(content)
    s = load(workspace / "s.db")
    assert (s.hardware, s.codec, s.max_resolution, s.show_details) == ("gpu", "h265", "original", False)


def test_gpu_falls_back_to_processor_without_a_card(monkeypatch):
    from clipshrink import encode
    monkeypatch.setattr(encode, "encoder_available", lambda name: False)
    assert encode.resolve_encoder("gpu", "h265") == "x265"
    assert encode.resolve_encoder("gpu", "av1") == "svtav1"
    assert encode.resolve_encoder("auto", "h265") == "x265"


def test_gpu_uses_the_card_when_it_works(monkeypatch):
    from clipshrink import encode
    monkeypatch.setattr(encode, "encoder_available", lambda name: True)
    assert encode.resolve_encoder("gpu", "h265") == "nvenc"
    assert encode.resolve_encoder("gpu", "av1") == "av1_nvenc"
    assert encode.resolve_encoder("cpu", "h265") == "x265"
    assert encode.resolve_encoder("cpu", "av1") == "svtav1"


def test_an_explicit_encoder_is_kept(monkeypatch):
    from clipshrink import encode
    assert encode.resolve_encoder("x265") == "x265" and encode.resolve_encoder("svtav1", "av1") == "svtav1"


@pytest.fixture
def win(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    yield w
    w.close()


def _pick(combo, value):
    combo.setCurrentIndex(combo.findData(value))


def test_sidebar_has_settings_first(win):
    assert win.sidebar_buttons()[0] == "Settings"
    win.settings_btn.click()
    assert win.stack.currentWidget() is win.settings_page


def test_page_opens_by_saying_the_defaults_are_fine(win):
    t = win.settings_intro.text().lower()
    assert "default" in t and "most" in t


def test_encoder_choice_left_the_saving_page(win):
    assert not hasattr(win, "encoder_box")


def test_controls_show_the_defaults(win, monkeypatch):
    from clipshrink import encode
    monkeypatch.setattr(encode, "encoder_available", lambda name: True)     # a PC with a working card
    win._apply_settings_view()
    assert win.hardware_box.currentData() == "gpu"
    assert win.codec_box.currentData() == "h265"
    assert win.resolution_box.currentData() == "original"
    assert not win.details_box.isChecked()


def test_choices_are_saved_at_once(win, workspace, monkeypatch):
    from clipshrink import encode
    from clipshrink.settings import load
    monkeypatch.setattr(encode, "encoder_available", lambda name: True)     # a PC with a working card
    win._apply_settings_view()
    _pick(win.codec_box, "av1")
    _pick(win.hardware_box, "cpu")
    _pick(win.resolution_box, "1080p")
    win.details_box.setChecked(True)
    s = load(workspace / "work" / "s.db")
    assert (s.hardware, s.codec, s.max_resolution, s.show_details) == ("cpu", "av1", "1080p", True)


def test_reopening_the_app_keeps_the_choices(win, workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    _pick(win.codec_box, "av1")
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    assert w.codec_box.currentData() == "av1"
    w.close()


def test_reset_returns_to_defaults(win):
    _pick(win.codec_box, "av1")
    _pick(win.resolution_box, "720p")
    win.settings_reset.click()
    assert win.codec_box.currentData() == "h265" and win.resolution_box.currentData() == "original"


def test_changing_a_setting_clears_the_estimate(win):
    from clipshrink.estimate import Estimate
    win._estimate_done(Estimate(10, 5, 4, 6, 60.0, "x265", [], 1))
    assert win.can_convert() and win.to_convert.isEnabled()
    _pick(win.codec_box, "av1")
    assert not win.can_convert() and not win.to_convert.isEnabled()


def test_settings_are_locked_while_converting(win):
    win.busy = True
    win.go(5)
    assert not win.codec_box.isEnabled() and not win.settings_reset.isEnabled()
    win.busy = False
    win.go(5)
    assert win.codec_box.isEnabled()


def test_plain_warnings_for_the_riskier_choices(win):
    assert win.codec_note.isHidden() and win.resolution_note.isHidden()
    win.show()
    _pick(win.codec_box, "av1")
    _pick(win.resolution_box, "1080p")
    win.go(5)
    assert "fewer devices" in win.codec_note.text() and not win.codec_note.isHidden()
    assert "detail" in win.resolution_note.text().lower() and not win.resolution_note.isHidden()
    win.close()


def test_page_says_what_is_actually_in_use(win, monkeypatch):
    from clipshrink import encode
    monkeypatch.setattr(encode, "encoder_available", lambda name: False)
    win.go(5)
    assert "processor" in win.using_label.text().lower()
    monkeypatch.setattr(encode, "encoder_available", lambda name: True)
    _pick(win.codec_box, "av1")
    assert "graphics card" in win.using_label.text().lower() and "AV1" in win.using_label.text()


def _record(workspace, **kw):
    from clipshrink import db
    base = dict(source=str(workspace / "videos" / "a.mp4"), status="verified", source_size=10_000_000, output_size=5_000_000,
                vmaf_mean=97.0, vmaf_p1=92.0, encoder="nvenc", quality=29, codec="h265", source_width=3840, source_height=2160,
                output_width=1920, output_height=1080, duration=10.0)
    base.update(kw)
    return db.Record(**base)


def test_details_column_is_hidden_until_asked(win, workspace):
    from test_interface import _col
    for t in (win.conv_table, win.review):
        assert t.isColumnHidden(_col(t, "Encoding"))
    win.details_box.setChecked(True)
    for t in (win.conv_table, win.review):
        assert not t.isColumnHidden(_col(t, "Encoding"))


def test_details_text_has_codec_encoder_quality_size_and_bitrate(workspace):
    from clipshrink.ui import details_text
    t = details_text(_record(workspace))
    for bit in ("H.265", "NVIDIA", "Q29", "1920×1080", "4.0 Mbit/s"):
        assert bit in t, t


def test_details_for_an_older_record_show_what_is_known(workspace):
    from clipshrink.ui import details_text
    t = details_text(_record(workspace, codec="", output_width=0, output_height=0, duration=0.0))
    assert "Q29" in t and "Mbit" not in t and "×" not in t


def test_details_empty_when_nothing_was_converted(workspace):
    from clipshrink.ui import details_text
    assert details_text(_record(workspace, status="kept_original", output_size=0)) == ""


def test_convert_and_review_fill_the_details_column(win, workspace):
    from test_interface import _col
    rec = _record(workspace)
    win._fill_conv_table([rec.source])
    win._show_row(rec)
    assert "Q29" in win.conv_table.item(0, _col(win.conv_table, "Encoding")).text()


def test_resized_label_and_delete_warning(win, workspace):
    from clipshrink import config
    assert config.status_text(_record(workspace)) == "Resized"
    assert config.status_text(_record(workspace, output_width=3840, output_height=2160)) == "Verified"
    t = win.delete_confirmation_text(2, 1000, resized=1).lower()
    assert "lower resolution" in t and "1" in t
    assert "resolution" not in win.delete_confirmation_text(2, 1000).lower()


def test_explanation_covers_resizing(win):
    t = win.quality_explanation().lower()
    assert "resolution" in t and "smaller copy" in t


def _darkest_left(widget):
    img = widget.grab().toImage()
    return min(img.pixelColor(x, y).lightness() for x in range(0, 22) for y in range(img.height()))


def test_tick_boxes_in_settings_and_delete_dialog_can_be_seen(win, qapp_instance):
    from clipshrink.ui import DeleteDialog, apply_theme
    apply_theme(qapp_instance)
    win.show()
    win.go(5)
    qapp_instance.processEvents()
    assert _darkest_left(win.details_box) < 170, "no visible tick box"
    d = DeleteDialog(win, "text")
    d.show()
    qapp_instance.processEvents()
    assert _darkest_left(d.tick) < 170, "no visible tick box"
    d.close()
    win.close()


def test_ticked_box_in_settings_looks_different(win, qapp_instance):
    win.show()
    win.go(5)
    qapp_instance.processEvents()
    before = win.details_box.grab().toImage()
    win.details_box.setChecked(True)
    qapp_instance.processEvents()
    assert before != win.details_box.grab().toImage()
    win.close()
