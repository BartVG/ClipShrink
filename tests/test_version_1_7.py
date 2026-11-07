"""Version 1.7: Open file location, Explorer-style ticking, Settings and About on one page,
zoom with dragging, a progress bar that jumps where it's clicked, and seven languages."""
import csv, string
from pathlib import Path
import pytest
from conftest import ROOT
from test_interface import ROWS, _col, _review_with, _ticked_names

LANGS = ("fr", "nl", "de", "es", "it", "pt")


@pytest.fixture
def win(workspace, qapp_instance):
    from clipshrink.ui import MainWindow
    w = MainWindow(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t")
    w.show()
    yield w
    w.set_language("en")
    w.close()


@pytest.fixture
def review(workspace, qapp_instance):
    w = _review_with(workspace, qapp_instance, ROWS)
    yield w
    w.set_language("en")
    w.close()


def _row(t, name):
    c = _col_key(t, "Original")      # by its English key, so it works in any language
    return next(r for r in range(t.rowCount()) if t.item(r, c).text() == name)


# --- Open file location
def test_every_table_offers_open_file_location(review, workspace):
    from clipshrink import scan
    from clipshrink.ui import cell
    w = review
    src = workspace / "videos" / "Trip" / "b.mp4"
    w._show_scan(scan.ScanResult(h264=[_info(src)]))
    w._fill_conv_table([str(src)])
    w.est_table.setRowCount(1)
    w.est_table.setItem(0, 0, cell("b.mp4", str(src)))
    for t in (w.scan_table, w.est_table, w.conv_table, w.review):
        assert [a for a, _ in w.table_menu_actions(t, 0)] == ["Open file location"], t
        assert Path(w._location_of(t, 0)).parent.parent == workspace / "videos" or t is w.review
    assert w._location_of(w.est_table, 0) == str(src), "the sample's file, from its tooltip"


def _info(path):
    from clipshrink.scan import MediaInfo
    return MediaInfo(path=str(path), size=900, mtime_ns=0, codec="h264", width=1920, height=1080, fps=30.0,
                     duration=10.0, frames=300, video_bytes=900)


def test_open_file_location_highlights_the_file_in_explorer(monkeypatch, workspace):
    from clipshrink import ui
    seen = []
    monkeypatch.setattr(ui.subprocess, "Popen", lambda cmd, *a, **k: seen.append(cmd))
    f = workspace / "videos" / "a b.mp4"
    f.write_bytes(b"x")
    ui.open_location(str(f))
    assert seen == [f'explorer /select,"{f}"'], "quoted, so a space or comma in the path is fine"


def test_a_missing_file_opens_its_folder(monkeypatch, workspace):
    from clipshrink import ui
    opened = []
    monkeypatch.setattr(ui.os, "startfile", lambda p: opened.append(p), raising=False)
    ui.open_location(str(workspace / "videos" / "gone.mp4"))
    assert opened == [str(workspace / "videos")]


def test_once_the_original_is_in_the_recycle_bin_the_conversion_is_shown(review):
    w = review
    row = _row(w.review, "a.mp4")
    rec = w._review_rec(row)
    Path(rec.source).unlink()
    assert w._location_of(w.review, row) == rec.output


# --- Ticking like Explorer
def test_a_plain_click_on_a_row_only_picks_it_for_play(review):
    from PySide6.QtCore import Qt
    w = review
    w._cell_clicked(_row(w.review, "a.mp4"), 1, Qt.NoModifier)
    assert _ticked_names(w) == []


def test_the_box_and_ctrl_click_tick_and_untick_one_row(review):
    from PySide6.QtCore import Qt
    w = review
    w._cell_clicked(_row(w.review, "a.mp4"), 0, Qt.NoModifier)
    w._cell_clicked(_row(w.review, "d.mp4"), 3, Qt.ControlModifier)
    assert _ticked_names(w) == ["a.mp4", "d.mp4"]
    w._cell_clicked(_row(w.review, "a.mp4"), 5, Qt.ControlModifier)
    assert _ticked_names(w) == ["d.mp4"]
    w._cell_clicked(_row(w.review, "d.mp4"), 0, Qt.ControlModifier)
    assert _ticked_names(w) == [], "Ctrl+click on the box itself toggles once, not twice"


def test_shift_click_ticks_the_range_from_the_last_click(review):
    from PySide6.QtCore import Qt
    w = review
    t = w.review
    t.sortItems(_col(t, "Original"), Qt.AscendingOrder)      # a, b, c, d
    w._cell_clicked(_row(t, "b.mp4"), 2, Qt.NoModifier)
    w._cell_clicked(_row(t, "d.mp4"), 2, Qt.ShiftModifier)
    assert _ticked_names(w) == ["b.mp4", "c.mp4", "d.mp4"]


def test_ctrl_a_ticks_every_deletable_row(review):
    from PySide6.QtCore import Qt
    from PySide6.QtTest import QTest
    w = review
    w.review.setFocus()
    QTest.keyClick(w.review, Qt.Key_A, Qt.ControlModifier)
    assert _ticked_names(w) == ["a.mp4", "b.mp4", "c.mp4", "d.mp4"]
    assert "4" in w.delete_btn.text()


def test_rows_that_cant_be_deleted_are_never_ticked(workspace, qapp_instance):
    from PySide6.QtCore import Qt
    rows = ROWS + [("e.mp4", "Other", 700, 0, None, None, "failed")]
    w = _review_with(workspace, qapp_instance, rows)
    t = w.review
    t.sortItems(_col(t, "Original"), Qt.AscendingOrder)
    w._cell_clicked(_row(t, "e.mp4"), 2, Qt.ControlModifier)
    assert _ticked_names(w) == []
    w._cell_clicked(_row(t, "a.mp4"), 2, Qt.NoModifier)
    w._cell_clicked(_row(t, "e.mp4"), 2, Qt.ShiftModifier)
    assert "e.mp4" not in _ticked_names(w) and len(_ticked_names(w)) == 4
    w.tick_every_deletable()
    assert "e.mp4" not in _ticked_names(w)
    w.close()


# --- Settings and About together
def test_one_sidebar_entry_opens_settings_with_about_beside_it(win):
    from clipshrink import config
    assert win.sidebar_buttons() == ["Settings"]
    win.settings_btn.click()
    assert win.stack.currentWidget() is win.settings_page is win.about_page
    text = win.about_text()
    assert f"{config.APP_NAME} {config.VERSION}" in text and "GPL-3.0" in text and "FFmpeg" in text
    assert config.DOCS_URL in win.about_links() and config.PROJECT_URL in win.about_links()


def test_docs_link_can_be_opened_and_copied(win, monkeypatch, qapp_instance):
    from PySide6.QtGui import QDesktopServices
    from clipshrink import config
    opened = []
    monkeypatch.setattr(QDesktopServices, "openUrl", lambda u: opened.append(u.toString()) or True)
    win.docs_open.click()
    win.docs_copy.click()
    assert opened == [config.DOCS_URL]
    assert qapp_instance.clipboard().text() == config.DOCS_URL


def test_language_is_the_first_setting(win):
    from PySide6.QtWidgets import QGridLayout
    grid = win.language_box.parentWidget().layout()
    assert isinstance(grid, QGridLayout)
    assert grid.itemAtPosition(0, 1).widget() is win.language_box


# --- Zoom and dragging
def _player(zoom=None, w=3840, h=2160):
    from clipshrink.player import SideBySidePlayer
    p = SideBySidePlayer("a.mp4", "b.mp4", width=w, height=h)
    p.zoom = zoom
    return p


@pytest.mark.parametrize("zoom, size", [(1, (960, 1080)), (2, (480, 540)), (4, (240, 270))])
def test_each_zoom_shows_a_smaller_window_enlarged_into_blocks(zoom, size):
    p = _player(zoom)
    cw, ch, x, y = p.window()
    assert (cw, ch) == size and (x, y) == ((3840 - cw) // 2, (2160 - ch) // 2), "starts in the middle"
    graph = p._graph()
    assert f"crop={cw}:{ch}:{x}:{y}" in graph
    if zoom > 1:
        assert f"scale={cw * zoom}:{ch * zoom}:flags=neighbor" in graph, "pixels as blocks, not a blur"
    assert graph.count(f"crop={cw}:{ch}:{x}:{y}") == 2, "the same spot on both sides"


def test_the_window_stays_inside_the_picture():
    p = _player(4)
    assert p.clamp_centre(-5, 9) == (240 // 2 / 3840, 1 - 270 // 2 / 2160)
    p.centre = p.clamp_centre(-5, 9)
    cw, ch, x, y = p.window()
    assert x == 0 and y == 2160 - ch


def test_whole_picture_has_no_crop():
    assert "crop" not in _player(None)._graph()


@pytest.fixture
def player_window(monkeypatch, qapp_instance):
    from PySide6.QtTest import QTest
    from clipshrink import db, ui
    from test_version_1_5 import FakePlayer

    class Fake(FakePlayer):
        seeks = []

        def seek(self, t):
            self.seeks.append(t)

        def window(self):
            return 480, 540, 0, 0

    monkeypatch.setattr(ui, "SideBySidePlayer", Fake)
    w = ui.PlayerWindow(None, db.Record(source="a.mp4", output="b.mp4", vmaf_mean=97.0, vmaf_p1=93.0))
    w.resize(1000, 700)
    w.show()
    w.activateWindow()
    QTest.qWaitForWindowActive(w)
    w.begin()
    yield w
    w.close()


def test_zoom_buttons_are_next_to_each_other_and_exclusive(player_window):
    w = player_window
    assert [b.text() for b in w.view_btns.values()] == ["Whole picture", "100%", "200%", "400%"]
    w.view_btns[4].click()
    assert w.player.zoom == 4 and w.view_btns[4].isChecked() and not w.view_btns[None].isChecked()
    assert w.drag_hint.isVisibleTo(w)
    w.view_btns[None].click()
    assert w.player.zoom is None and not w.drag_hint.isVisibleTo(w)


def test_dragging_moves_both_sides_the_way_the_mouse_goes(player_window):
    from PySide6.QtCore import QPoint
    w = player_window
    w.view_btns[2].click()
    start = w.video.mapToGlobal(w.video.rect().center())
    states = iter([(True, start), (True, start + QPoint(100, 0)), (False, start + QPoint(100, 0))])
    w.mouse_state = lambda: next(states)
    w.was_down = False
    for _ in range(3):
        w.poll_drag()
    assert w.player.centre[0] < 0.5, "dragging right shows what is further left"
    assert abs(w.player.centre[1] - 0.5) < 1e-9
    assert w.drag is None, "letting go ends the drag"


def test_a_press_outside_the_picture_is_not_a_drag(player_window):
    from PySide6.QtCore import QPoint
    w = player_window
    w.view_btns[1].click()
    outside = w.play_btn.mapToGlobal(QPoint(2, 2))
    w.mouse_state = lambda: (True, outside)
    w.poll_drag()
    assert w.drag is None


def test_clicking_the_progress_bar_jumps_there(player_window):
    from PySide6.QtCore import QPoint, Qt
    from PySide6.QtTest import QTest
    w = player_window
    s = w.slider
    QTest.mouseClick(s, Qt.LeftButton, pos=QPoint(int(s.width() * 0.75), s.height() // 2))
    assert w.player.seeks, "a click must seek"
    assert abs(w.player.seeks[-1] - 7.5) < 0.4, "75% of a 10 second video"


def test_real_player_zooms_400_percent(get_clip, workspace):
    from clipshrink.player import SideBySidePlayer
    src = get_clip("gopro_like_1080p_telemetry")
    p = SideBySidePlayer(src, src, mute=True)
    p.start()
    try:
        for zoom, centre in ((4, (0.2, 0.3)), (2, (0.9, 0.9)), (1, None), (None, None)):
            p.set_view(zoom, centre)
        p.set_view(4, (0.2, 0.3))
        p.seek(1.0)
        shot = workspace / "z.png"
        p.screenshot(shot)
        import struct
        head = shot.read_bytes()[:24]
        assert struct.unpack(">II", head[16:24]) == (2 * 240 * 4, 270 * 4), "two 240x270 windows, 4 times larger"
    finally:
        p.close()


# --- Languages
def _fields(s):
    return sorted({f for _, f, _, _ in string.Formatter().parse(s) if f})


@pytest.mark.parametrize("code", LANGS)
def test_every_text_is_translated_with_the_same_placeholders(code):
    from i18n_keys import keys
    from clipshrink import i18n
    messages, plurals = keys()
    m, p = i18n.catalogue(code)
    assert sorted(k for k in messages if k not in m) == [], "missing"
    assert sorted(k for k in m if k not in messages) == [], "no longer used"
    assert [k for k in m if _fields(k) != _fields(m[k])] == []
    singular = {a: b for a, b in plurals}
    assert sorted(set(singular) - set(p)) == [] and sorted(set(p) - set(singular)) == []
    assert [a for a, forms in p.items() if len(forms) != 2 or any(_fields(f) != _fields(singular[a]) for f in forms)] == []


def test_seven_languages_by_their_own_names():
    from clipshrink import i18n
    assert i18n.LANGUAGES == {"en": "English", "fr": "Français", "nl": "Nederlands", "de": "Deutsch", "es": "Español",
                              "it": "Italiano", "pt": "Português"}


def test_english_is_the_default_whatever_windows_uses(win):
    from clipshrink import i18n, settings
    assert settings.Settings().language == "en"
    assert i18n.language() == "en" and win.language_box.currentData() == "en"
    assert win.settings_btn.text() == "Settings"


def test_switching_changes_every_word_at_once_and_back(review):
    from PySide6.QtWidgets import QAbstractButton, QLabel
    w = review
    w.go(3)
    def visible():
        texts = [x.text() for cls in (QLabel, QAbstractButton) for x in w.findChildren(cls) if x.text()]
        texts += [w.review.horizontalHeaderItem(c).text() for c in range(w.review.columnCount())]
        texts += [w.review.item(r, c).text() for r in range(w.review.rowCount()) for c in range(w.review.columnCount())
                  if w.review.item(r, c)]
        return texts + [w.windowTitle(), w.hardware_box.itemText(1)]
    english = visible()
    w.language_box.setCurrentIndex(w.language_box.findData("fr"))
    assert w.settings_btn.text() == "Paramètres"
    assert w.steps[3].text() == "4  Comparer et nettoyer"
    assert w.review.horizontalHeaderItem(_col_key(w.review, "Original")).text() == "Original"
    assert w.review.horizontalHeaderItem(_col_key(w.review, "Folder")).text() == "Dossier"
    assert "Vérifiée" in [w.review.item(r, _col_key(w.review, "Result")).text() for r in range(4)]
    assert "Corbeille" in w.delete_btn.text() or "Cochez" in w.delete_btn.text()
    assert "Paramètres" in w.windowTitle() or "réduisez" in w.windowTitle()
    assert w.hardware_box.itemText(1) == "Processeur (lent, fonctionne sur tout PC)"
    assert "," in w.review.item(_row(w.review, "a.mp4"), _col_key(w.review, "VMAF average")).text(), "97,0"
    w.language_box.setCurrentIndex(w.language_box.findData("en"))
    assert visible() == english, "back to exactly the same English"


def _col_key(t, key):
    from clipshrink.ui import column_key
    return next(c for c in range(t.columnCount()) if column_key(t, c) == key)


def test_ticks_and_sorting_survive_a_change_of_language(review):
    from PySide6.QtCore import Qt
    w = review
    w._cell_clicked(_row(w.review, "c.mp4"), 0, Qt.NoModifier)
    w.review.sortItems(_col(w.review, "Before"), Qt.DescendingOrder)
    order = [w.review.item(r, 1).text() for r in range(4)]
    w.set_language("de")
    assert [w.review.item(r, 1).text() for r in range(4)] == order
    assert _ticked_names(w) == ["c.mp4"]
    assert w.delete_btn.text() == "1 angekreuztes Original in den Papierkorb…"


@pytest.mark.parametrize("code", LANGS)
def test_each_language_shows_on_every_page(win, code):
    from PySide6.QtWidgets import QLabel
    from clipshrink import i18n
    win.set_language(code)
    m, _ = i18n.catalogue(code)
    for i in range(6):
        win.go(i)
    labels = " ".join(x.text() for x in win.findChildren(QLabel))
    for english in ("Find your videos", "See the saving before anything converts", "Compare and clean up",
                    "Shrink your videos, keep the quality.", "Language", "Advanced"):
        assert m[english] in labels, (code, english)


def test_the_choice_is_remembered_and_back_to_the_defaults_keeps_it(workspace, qapp_instance):
    from clipshrink import settings
    from clipshrink.ui import MainWindow
    p, t = workspace / "work" / "s.db", workspace / "work" / "t"
    w = MainWindow(db_path=p, work_dir=t)
    w.set_language("nl")
    w.settings_reset.click()
    assert settings.load(p).language == "nl", "the language isn't about your videos"
    w.close()
    w = MainWindow(db_path=p, work_dir=t)
    assert w.settings_btn.text() == "Instellingen" and w.language_box.currentData() == "nl"
    w.set_language("en")
    w.close()


def test_an_unknown_language_in_the_file_means_english(workspace):
    import json
    from clipshrink import settings
    p = workspace / "work" / "s.db"
    settings.path_for(p).write_text(json.dumps({"language": "xx"}), encoding="utf-8")
    assert settings.load(p).language == "en"


def test_numbers_use_the_languages_decimal_comma():
    from clipshrink import i18n
    from clipshrink.ui import human_size
    try:
        i18n.set_language("fr")
        assert human_size(1_234_000_000) == "1,2 Go" and i18n.num(95.5, 1) == "95,5"
        i18n.set_language("de")
        assert human_size(1_234_000_000) == "1,2 GB"
    finally:
        i18n.set_language("en")
    assert human_size(1_234_000_000) == "1.2 GB"


def test_plurals_follow_each_language():
    from clipshrink import i18n
    try:
        i18n.set_language("fr")
        assert i18n.ntr("{n} file renamed.", "{n} files renamed.", 0).format(n=0) == "0 fichier renommé."
        assert i18n.ntr("{n} file renamed.", "{n} files renamed.", 2).format(n=2) == "2 fichiers renommés."
        i18n.set_language("nl")
        assert i18n.ntr("{n} file renamed.", "{n} files renamed.", 0).format(n=0) == "0 bestanden hernoemd."
    finally:
        i18n.set_language("en")


def test_stored_reasons_are_shown_in_the_language_even_nested():
    from clipshrink import i18n
    below = ("VMAF below the target: average 93.2 (target 95), worst 1% 88.0 (target 90). "
             "Compare it before removing the original.")
    nested = "Could not convert, original kept: the encoder stopped: x265 [error]: oops"
    problems = "Conversion did not match the original, original kept: resolution differs; frame count differs (10 vs 12)"
    try:
        i18n.set_language("fr")
        assert i18n.reason(below).startswith("VMAF sous l'objectif : moyenne 93,2 (objectif 95), pire 1 % 88,0")
        assert i18n.reason(nested) == "Conversion impossible, original conservé : l'encodeur s'est arrêté : x265 [error]: oops"
        assert i18n.reason(problems).endswith(": la résolution diffère; le nombre d'images diffère (10 contre 12)")
        assert i18n.reason("something FFmpeg said") == "something FFmpeg said"
    finally:
        i18n.set_language("en")
    assert i18n.reason(below) == below


def test_every_reason_the_engine_writes_has_a_template():
    """Each message in engine.py and trash.py must match one of i18n.REASONS, or it would stay in English."""
    import ast, re
    from clipshrink import i18n
    for name in ("engine.py", "trash.py", "encode.py"):
        tree = ast.parse((ROOT / "clipshrink" / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", "")) in (
                    "Verdict", "RuntimeError", "append") and node.args:
                arg = node.args[-1] if getattr(node.func, "attr", "") == "append" else node.args[0]
                if isinstance(arg, ast.Tuple):
                    arg = arg.elts[-1]
                if isinstance(arg, ast.BinOp):
                    arg = arg.left
                if isinstance(arg, ast.JoinedStr):
                    text = "".join(v.value if isinstance(v, ast.Constant) else "X" for v in arg.values)
                elif isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    text = arg.value
                else:
                    continue
                if name == "encode.py" and not text.startswith(("the ", "could not")):
                    continue
                assert any(rx.fullmatch(text) or rx.fullmatch(text + "X") for _, rx in i18n._PATTERNS), (name, text)
    for node in ast.walk(ast.parse((ROOT / "clipshrink" / "trash.py").read_text(encoding="utf-8"))):
        if isinstance(node, ast.Return) and isinstance(node.value, (ast.Constant, ast.JoinedStr)):
            v = node.value
            text = v.value if isinstance(v, ast.Constant) else "".join(
                x.value if isinstance(x, ast.Constant) else "X" for x in v.values)
            if isinstance(text, str):
                assert any(rx.fullmatch(text) for _, rx in i18n._PATTERNS), text


def test_reports_are_written_in_the_language(workspace):
    from clipshrink import db, i18n, reports
    rec = db.Record(source=str(workspace / "a.mp4"), status="kept_original", source_size=10,
                    reason="Conversion is not smaller (12 vs 10 bytes), original kept.")
    try:
        i18n.set_language("es")
        path = reports.write_batch_report(workspace / "r", [rec])
    finally:
        i18n.set_language("en")
    with open(path, encoding="utf-8-sig") as f:
        head, row = list(csv.reader(f))
    assert head[:5] == ["Fecha", "Archivo", "Carpeta", "Resultado", "Motivo"]
    assert row[3] == "Original conservado" and row[4].startswith("La conversión no es más pequeña")


def test_the_pill_colour_doesnt_depend_on_the_language(review):
    from clipshrink.ui import ENGLISH_ROLE, pill_colours
    w = review
    w.set_language("it")
    c = _col_key(w.review, "Result")
    it = w.review.item(_row(w.review, "a.mp4"), c)
    assert it.text() == "Verificato" and it.data(ENGLISH_ROLE) == "Verified"
    assert pill_colours(it.data(ENGLISH_ROLE)) == pill_colours("Verified")


def test_qt_yes_and_no_buttons_are_translated_too(win):
    from PySide6.QtCore import QCoreApplication
    win.set_language("fr")
    assert QCoreApplication.translate("QPlatformTheme", "&Yes") != "&Yes" or \
        QCoreApplication.translate("QDialogButtonBox", "&Yes") != "&Yes"
    win.set_language("en")
    assert QCoreApplication.translate("QPlatformTheme", "&Yes") == "&Yes"


def test_in_english_on_one_thread_leaves_the_others_alone():
    import threading
    from clipshrink import i18n
    seen = []
    try:
        i18n.set_language("fr")
        ready, done = threading.Event(), threading.Event()

        def other():
            ready.wait()
            seen.append(i18n.tr("Folder"))
            done.set()

        threading.Thread(target=other).start()
        with i18n.english():
            ready.set()
            done.wait(5)
            assert i18n.tr("Folder") == "Folder"
    finally:
        i18n.set_language("en")
    assert seen == ["Dossier"]


def test_installer_offers_the_seven_languages_english_first():
    iss = (ROOT / "installer" / "clipshrink.iss").read_text(encoding="utf-8-sig")
    names = [line.split('"')[1] for line in iss.splitlines() if line.startswith("Name: ") and "MessagesFile" in line]
    assert names == ["en", "fr", "nl", "de", "es", "it", "pt"]
    assert "LanguageDetectionMethod=none" in iss, "English unless the person picks another"
    assert "{cm:OpenNow}" in iss and iss.count(".OpenNow=") == 7


def test_translations_say_they_are_unchecked():
    for code in LANGS:
        head = (ROOT / "clipshrink" / "locales" / f"{code}.py").read_text(encoding="utf-8").splitlines()[0]
        assert "Not yet checked by a native speaker" in head


def test_version_is_1_7():
    from clipshrink import config
    iss = (ROOT / "installer" / "clipshrink.iss").read_text(encoding="utf-8-sig")
    assert config.VERSION == "1.7" and "AppVersion=1.7\n" in iss
