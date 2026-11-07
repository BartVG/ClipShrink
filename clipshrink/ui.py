"""The desktop interface: four stages, left to right, one obvious button each.

Every text is written in English and passed through tr(). A text that must follow a change
of language is set with MainWindow.live(), or built by a function given to cell(), so that
retranslate() can build it again in the new language."""
import ctypes, html, re
import os, subprocess, sys, threading, time
from pathlib import Path
from PySide6.QtCore import QEvent, QLibraryInfo, QLocale, QUrl, QObject, QPointF, QRectF, Qt, QTimer, QTranslator, Signal
from PySide6.QtGui import QIcon, QCursor, QDesktopServices, QColor, QKeySequence, QPainter, QPalette, QPen, QShortcut
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QScrollArea,
                               QButtonGroup, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QMenu, QMessageBox,
                               QProgressBar, QPushButton, QSlider, QStackedWidget, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTableWidget, QTableWidgetItem,
                               QTextBrowser, QVBoxLayout, QWidget)
from . import config, db, encode, i18n, reports, scan, settings as app_settings, tools, trash
from .encode import Stopped
from .engine import Converter, forget_everything
from .estimate import estimate_savings
from .i18n import N_, g, in_english, ntr, num, reason, tr
from .player import PlayerError, SideBySidePlayer
from .scan import original_stem, scan_folder

STYLE = """
QWidget { font-family: 'Segoe UI'; font-size: 10.5pt; color: #1f2933; }
QMainWindow, #page { background: #f7f8fa; }
#rail { background: #16202b; }
#stepOn  { color: white; font-weight: 600; background: #2c3a48; border-radius: 8px; border-left: 3px solid #2fa37c; padding: 10px; }
#stepOff { color: #9fb0c0; padding: 10px; }
#stepDone { color: #d5dee6; padding: 10px; }
#stepCheck { color: #5fd3a5; font-weight: 700; background: transparent; border: none; padding: 0; }
#title { font-size: 18pt; font-weight: 600; }
#hint  { color: #52606d; }
#big   { font-size: 22pt; font-weight: 600; color: #0b6e4f; }
#card  { background: white; border: 1px solid #e3e7ec; border-radius: 10px; }
#statTitle { color: #3e4c59; font-size: 10pt; background: transparent; border: none; }
#statValue { font-size: 17pt; font-weight: 600; background: transparent; border: none; }
#statGood { font-size: 17pt; font-weight: 600; color: #0b7a55; background: transparent; border: none; }
#barLabel { font-size: 10pt; background: transparent; border: none; }
QPushButton { padding: 7px 14px; border: 1px solid #cdd4db; border-radius: 8px; background: white; }
QPushButton:hover { background: #eef1f4; }
QPushButton:disabled { color: #a0a8b0; background: #f0f1f3; }
QPushButton#primary { background: #0b6e4f; color: white; border: none; font-weight: 600; padding: 9px 20px; }
QPushButton#primary:hover { background: #095c42; }
QPushButton#primary:disabled { background: #b6c9c2; color: white; }
QPushButton#next { background: #16202b; color: white; border: none; font-weight: 600; padding: 9px 20px; }
QPushButton#next:hover { background: #2c3a48; }
QPushButton#next:disabled { background: #b8c0c8; color: white; }
QPushButton#danger { background: #b42318; color: white; border: none; font-weight: 600; padding: 9px 20px; }
QPushButton#danger:disabled { background: #e0bdb9; color: white; }
QPushButton#tab { border: 1px solid transparent; background: transparent; padding: 5px 12px; }
QPushButton#tab:hover { background: #eef1f4; }
QPushButton#tab:checked { background: white; border: 1px solid #cdd4db; font-weight: 600; }
QPushButton#view { padding: 7px 10px; }
QPushButton#view:checked { background: #dcefe7; border: 1px solid #0b6e4f; font-weight: 600; }
QTableWidget { background: white; border: 1px solid #e3e7ec; border-radius: 10px; }
QHeaderView::section { background: white; border: none; border-bottom: 1px solid #e3e7ec; padding: 7px 6px; font-weight: 600; }
QTableWidget { selection-background-color: #bfe3d4; selection-color: #1f2933; }
QTableWidget::item { border-bottom: 1px solid #f0f2f5; }
QTableWidget::item:selected { background: #bfe3d4; color: #1f2933; }
QTextBrowser { background: white; border: 1px solid #e3e7ec; border-radius: 8px; }
QComboBox { background: white; padding: 5px; border: 1px solid #cdd4db; border-radius: 8px; }
QCheckBox { background: transparent; }
QCheckBox:disabled { color: #a0a8b0; }
QDoubleSpinBox { background: white; padding: 4px; border: 1px solid #cdd4db; border-radius: 6px; }
QDoubleSpinBox:disabled { background: #f0f1f3; color: #a0a8b0; }
QScrollArea { background: transparent; border: none; }
QCheckBox::indicator { width: 16px; height: 16px; border: 2px solid #52606d; border-radius: 4px; background: white; }
QCheckBox::indicator:checked { background: #0b6e4f; border-color: #0b6e4f; }
QProgressBar { border: 1px solid #cdd4db; border-radius: 8px; text-align: center; background: white; height: 22px; }
QProgressBar::chunk { background: #2fa37c; border-radius: 7px; }
QProgressBar#barGreen { border: none; background: #dcefe7; border-radius: 5px; height: 10px; max-height: 10px; min-height: 10px; }
QProgressBar#barGreen::chunk { background: #0f9d6f; border-radius: 5px; }
QProgressBar#barBlue { border: none; background: #e1ebfa; border-radius: 5px; height: 10px; max-height: 10px; min-height: 10px; }
QProgressBar#barBlue::chunk { background: #4a90e2; border-radius: 5px; }
"""

STATUS_TEXT = config.STATUS_TEXT
ENGLISH_ROLE = Qt.UserRole + 1      # a cell's words in English, which decide a pill's colour
_qt_translator = None


def apply_theme(app):
    """One light look on every PC. Without this, Windows dark theme draws dark
    tick boxes and selections on this tool's light tables, which hides them."""
    app.styleHints().setColorScheme(Qt.ColorScheme.Light)
    app.setStyle("Fusion")
    pal = QPalette()
    for role, colour in ((QPalette.Window, "#f6f7f9"), (QPalette.WindowText, "#1f2933"), (QPalette.Base, "#ffffff"),
                         (QPalette.AlternateBase, "#f6f7f9"), (QPalette.Text, "#1f2933"), (QPalette.Button, "#ffffff"),
                         (QPalette.ButtonText, "#1f2933"), (QPalette.ToolTipBase, "#ffffff"),
                         (QPalette.ToolTipText, "#1f2933"), (QPalette.Highlight, "#bfe3d4"),
                         (QPalette.HighlightedText, "#1f2933"), (QPalette.PlaceholderText, "#7b8794")):
        pal.setColor(role, QColor(colour))
    app.setPalette(pal)


def use_language(code):
    """Switches the app's own words, and Qt's (the Yes and No buttons)."""
    global _qt_translator
    code = i18n.set_language(code)
    app = QApplication.instance()
    if app is not None:
        if _qt_translator is not None:
            app.removeTranslator(_qt_translator)
            _qt_translator = None
        if code != "en":
            t = QTranslator(app)
            if t.load(f"qtbase_{i18n.QT_NAMES[code]}", QLibraryInfo.path(QLibraryInfo.TranslationsPath)):
                app.installTranslator(t)
                _qt_translator = t
    return code


def qt_locale():
    return QLocale(QLocale.English, QLocale.UnitedStates) if i18n.language() == "en" else QLocale(i18n.QT_NAMES[i18n.language()])


UNITS = (N_("bytes"), N_("KB"), N_("MB"), N_("GB"), N_("TB"))


def human_size(n):
    n = float(n)
    for unit in UNITS:
        if abs(n) < 1000 or unit == "TB":
            return f"{n:.0f} {tr(unit)}" if unit == "bytes" else f"{num(n)} {tr(unit)}"
        n /= 1000


def short_time(seconds):
    """For the Time Remaining card: ~3h 32m left."""
    m = max(1, round(seconds / 60))
    if m < 60:
        return tr("~{m}m left").format(m=m)
    return tr("~{h}h {m}m left").format(h=m // 60, m=f"{m % 60:02d}")


def human_time(seconds):
    s = int(max(0, seconds))
    if s < 60:
        return tr("under a minute")
    m = round(s / 60)
    if m < 60:
        return ntr("about {n} minute", "about {n} minutes", m).format(n=m)
    h, m = divmod(m, 60)
    if h < 48:
        return tr("about {h} h {m} min").format(h=h, m=f"{m:02d}")
    return tr("about {d} days").format(d=num(h / 24))


def clock(t):
    return f"{int(t) // 60}:{int(t) % 60:02d}"


class Bridge(QObject):
    """Carries results from worker threads to the interface thread."""
    call = Signal(object)


class TickDelegate(QStyledItemDelegate):
    """Draws its own tick box in the middle of the cell. The style's own box is
    invisible once this app's stylesheet applies to the table."""
    def paint(self, painter, option, index):
        state = index.data(Qt.CheckStateRole)
        if state is None:
            return super().paint(painter, option, index)
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.features &= ~QStyleOptionViewItem.HasCheckIndicator
        opt.widget.style().drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)
        c = QRectF(option.rect).center()
        box = QRectF(c.x() - 9, c.y() - 9, 18, 18)
        ticked = Qt.CheckState(state) == Qt.Checked
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("#0b6e4f" if ticked else "#52606d"), 2))
        painter.setBrush(QColor("#0b6e4f" if ticked else "#ffffff"))
        painter.drawRoundedRect(box, 4, 4)
        if ticked:
            painter.setPen(QPen(QColor("#ffffff"), 2.4))
            painter.drawPolyline([QPointF(c.x() - 5, c.y()), QPointF(c.x() - 1.5, c.y() + 4), QPointF(c.x() + 5, c.y() - 4)])
        painter.restore()


def pill_colours(text):
    """Background and text colour of a status pill, from its English words."""
    if text.startswith("⚠"):
        return "#fdecc8", "#92400e"
    if text.startswith(("Verified", "Resized", "Ready", "Done", "Original in Recycle")):
        return "#d7f0e4", "#0b6e4f"
    if text.startswith(("Finding", "Encoding", "Measuring", "Working")):
        return "#dbeafe", "#1d4ed8"
    if text.startswith(("Original kept", "Failed")):
        return "#fde2df", "#b42318"
    return "#e8ebef", "#4b5563"


class PillDelegate(QStyledItemDelegate):
    """Draws a status as a rounded coloured label."""
    def paint(self, painter, option, index):
        text = index.data(Qt.DisplayRole) or ""
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.text = ""
        opt.widget.style().drawControl(QStyle.CE_ItemViewItem, opt, painter, opt.widget)
        if not text:
            return
        back, fore = pill_colours(index.data(ENGLISH_ROLE) or text)
        metrics = option.fontMetrics
        r = QRectF(option.rect).adjusted(5, 4, -5, -4)
        width = min(r.width(), metrics.horizontalAdvance(text) + 18)
        pill = QRectF(r.x(), r.y(), width, r.height())
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(back))
        painter.drawRoundedRect(pill, r.height() / 2, r.height() / 2)
        painter.setPen(QColor(fore))
        painter.drawText(pill.adjusted(9, 0, -9, 0), Qt.AlignLeft | Qt.AlignVCenter,
                         metrics.elidedText(text, Qt.ElideRight, int(width - 18)))
        painter.restore()

    def sizeHint(self, option, index):
        hint = super().sizeHint(option, index)
        hint.setWidth(hint.width() + 36)
        return hint


def open_location(path):
    """Explorer on the file's folder with the file highlighted, or just the folder if the file has gone."""
    p = Path(path)
    if p.is_file():
        subprocess.Popen(f'explorer /select,"{p}"')
    elif p.parent.is_dir():
        os.startfile(str(p.parent))


def row_path(t, row):
    """The full path a table row is about: column 0 keeps it, or its tooltip does."""
    it = t.item(row, 0)
    if it is None:
        return None
    return it.data(Qt.UserRole) or it.toolTip() or None


def toggle_tick(t, row):
    it = t.item(row, 0)
    it.setCheckState(Qt.Unchecked if it.checkState() == Qt.Checked else Qt.Checked)


class SortItem(QTableWidgetItem):
    """Sorts by its real value: 900 MB comes before 1.2 GB, and 9.5 before 93.5.
    Its text and tooltip can be functions, built again when the language changes."""
    def __init__(self, text="", key=None, tip=None):
        self.make = text if callable(text) else None
        self.make_tip = tip if callable(tip) else None
        super().__init__(str(text()) if self.make else str(text))
        self.key = key
        if self.make:
            self.setData(ENGLISH_ROLE, in_english(self.make))
        if tip:
            self.setToolTip(self.make_tip() if self.make_tip else tip)

    def refresh(self):
        if self.make:
            self.setText(self.make())
        if self.make_tip:
            self.setToolTip(self.make_tip())

    def rank(self):
        state = self.data(Qt.CheckStateRole)
        if state is not None:
            return (2, Qt.CheckState(state).value)
        if self.key is not None:
            return (1, self.key) if isinstance(self.key, (int, float)) else (3, str(self.key).casefold())
        text = self.text().casefold()
        return (3, text) if text else (0, 0)

    def __lt__(self, other):
        return self.rank() < other.rank() if isinstance(other, SortItem) else super().__lt__(other)


def column_key(t, c):
    """A column's English title, whatever the language."""
    head = t.horizontalHeaderItem(c)
    return head.data(Qt.UserRole) or head.text()


def table(headers, stretch=0, ticks=False, wide=None, pills=None, right=()):
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels([tr(h) for h in headers])
    for c, h in enumerate(headers):
        t.horizontalHeaderItem(c).setData(Qt.UserRole, h)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setSelectionMode(QAbstractItemView.SingleSelection)
    t.setTextElideMode(Qt.ElideMiddle)
    t.setShowGrid(False)
    t.setWordWrap(False)    # a folder path must stay on one line
    t.verticalHeader().setDefaultSectionSize(32)
    h = t.horizontalHeader()
    h.setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    for c in right:
        t.horizontalHeaderItem(c).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    if pills is not None:
        t.setItemDelegateForColumn(pills, PillDelegate(t))
    h.setSectionResizeMode(QHeaderView.Interactive)
    h.setStretchLastSection(True)
    t.setProperty("fitting", False)
    t.setProperty("user_sized", False)

    def resized(col, old, new):
        # Only a drag counts. fit_columns sets widths itself, the last column stretches with
        # the window, and hiding or showing a column goes through a width of 0.
        last = max((c for c in range(t.columnCount()) if not t.isColumnHidden(c)), default=-1)
        if not t.property("fitting") and col != last and old and new:
            t.setProperty("user_sized", True)

    h.sectionResized.connect(resized)
    h.setSortIndicator(-1, Qt.AscendingOrder)   # keep the list's own order until a header is clicked
    h.setSortIndicatorShown(True)
    h.setSectionsClickable(True)
    t.setSortingEnabled(True)
    if ticks:
        t.setItemDelegateForColumn(0, TickDelegate(t))
    return t


def retranslate_table(t):
    for c in range(t.columnCount()):
        t.horizontalHeaderItem(c).setText(tr(column_key(t, c)))
    for r in range(t.rowCount()):
        for c in range(t.columnCount()):
            it = t.item(r, c)
            if isinstance(it, SortItem):
                it.refresh()


MAX_FOLDER_WIDTH = 340


def fit_columns(t, force=False):
    """Fits columns to their content, until the user has dragged one."""
    if t.property("user_sized") and not force:
        return
    t.setProperty("fitting", True)
    t.resizeColumnsToContents()
    for c in range(t.columnCount()):
        if column_key(t, c) == "Folder" and t.columnWidth(c) > MAX_FOLDER_WIDTH:
            t.setColumnWidth(c, MAX_FOLDER_WIDTH)      # a long path shouldn't push everything off screen
    t.setProperty("fitting", False)
    if force:
        t.setProperty("user_sized", False)


def cell(text="", tip=None, key=None):
    """A table cell. text and tip are plain words, or functions that build them in the current language."""
    it = SortItem(text, key, tip)
    if isinstance(key, (int, float)):
        it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    return it


def words(english):
    """A cell's text in the current language, built again when it changes."""
    return lambda: tr(english)


def size_cell(n):
    return cell(lambda: human_size(n), key=n)


def folder_cell(path):
    folder = str(Path(path).parent)
    return cell(folder, folder)


def tick_cell(identity, ticked=None):
    """Column 0. `ticked` True/False shows a tick box, None shows a dash."""
    it = SortItem("" if ticked is not None else "—")
    it.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
    it.setData(Qt.UserRole, identity)
    if ticked is not None:
        it.setCheckState(Qt.Checked if ticked else Qt.Unchecked)
    else:
        it.setTextAlignment(Qt.AlignCenter)
    return it


AMBER = QColor("#b45309")
BELOW_TIP = N_("Below the quality target. Compare it with the original before removing the original.")


def score_cell(value, minimum):
    if value is None:
        return cell("", key=-1)
    low = value < minimum
    it = cell(lambda: f"⚠ {num(value)}" if low else num(value), words(BELOW_TIP) if low else None, key=value)
    if low:
        it.setForeground(AMBER)
    return it


def details_text(rec):
    """The encoding settings of one conversion, as far as they are known."""
    if rec.status not in ("verified", "below_bar", "original_deleted") or not rec.output_size:
        return ""
    bits = []
    if rec.codec in config.CODEC_NAMES:
        bits.append(config.CODEC_NAMES[rec.codec])
    if rec.encoder in config.ENCODER_NAMES:
        bits.append(tr(config.ENCODER_NAMES[rec.encoder]))
    if rec.quality is not None:
        bits.append(f"Q{rec.quality:g}")
    if rec.output_width:
        bits.append(f"{rec.output_width}×{rec.output_height}")
    if rec.output_bitrate_mbit:
        bits.append(f"{num(rec.output_bitrate_mbit)} Mbit/s")
    return ", ".join(bits)


def details_cell(rec):
    return cell(lambda: details_text(rec), key=None)


def result_text(rec):
    renamed = rec.status == "original_deleted" and Path(rec.output).stem.lower() == Path(rec.source).stem.lower()
    text = tr(STATUS_TEXT["renamed"]) if renamed else config.status_text(rec)
    if result_is_low(rec) and "⚠" not in text:
        text = f"⚠ {text}"
    return text


def result_is_low(rec):
    converted = rec.status in ("verified", "below_bar", "original_deleted")
    return converted and rec.vmaf_mean is not None and not rec.meets_target


def result_cell(rec):
    it = cell(lambda: result_text(rec), lambda: reason(rec.reason) or rec.output)
    if result_is_low(rec):
        it.setForeground(AMBER)
    return it


def left_in_place(refused, heading=N_("Left in place:")):
    return "\n\n" + tr(heading) + "\n" + "\n".join(f"{Path(p).name}: {reason(why)}" for p, why in refused)


class StepLabel(QLabel):
    """A step in the left pane. Clicking the current one leaves a side page."""
    clicked = Signal()

    def mouseReleaseEvent(self, ev):
        if ev.button() == Qt.LeftButton and self.rect().contains(ev.position().toPoint()):
            self.clicked.emit()
        super().mouseReleaseEvent(ev)


class DeleteDialog(QDialog):
    """Explicit confirmation: a tick box must be ticked before the button works."""
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setWindowTitle(tr("Send originals to the Recycle Bin?"))
        self.resize(540, 280)
        v = QVBoxLayout(self)
        lab = QLabel(text)
        lab.setWordWrap(True)
        v.addWidget(lab)
        self.tick = QCheckBox(tr("I understand. Send these originals to the Recycle Bin."))
        v.addWidget(self.tick)
        box = QDialogButtonBox()
        self.go = box.addButton(tr("Send to Recycle Bin"), QDialogButtonBox.AcceptRole)
        self.go.setObjectName("danger")
        self.go.setEnabled(False)
        box.addButton(tr("Keep them"), QDialogButtonBox.RejectRole).setDefault(True)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        self.tick.toggled.connect(self.go.setEnabled)
        v.addWidget(box)


class ClickSlider(QSlider):
    """A click on the bar jumps there, then works like grabbing the handle."""
    def mousePressEvent(self, ev):
        if ev.button() == Qt.LeftButton and self.orientation() == Qt.Horizontal:
            self.setValue(QStyle.sliderValueFromPosition(self.minimum(), self.maximum(),
                                                         int(ev.position().x()), max(1, self.width())))
        super().mousePressEvent(ev)


VIEWS = ((None, N_("Whole picture")), (1, "100%"), (2, "200%"), (4, "400%"))


class PlayerWindow(QDialog):
    """Opens over the main window and blocks it, so the language can't change meanwhile."""
    def __init__(self, parent, rec):
        super().__init__(parent)
        self.setWindowTitle(tr("Side by side: {name}").format(name=Path(rec.source).name))
        self.resize(1320, 800)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 8)
        heads = QHBoxLayout()
        codec = config.CODEC_NAMES.get(rec.codec, "H.265")
        for text in (tr("Original (H.264), shrunk to match") if rec.resized else tr("Original (H.264)"),
                     tr("Conversion ({codec})").format(codec=codec)):
            lab = QLabel(text)
            lab.setAlignment(Qt.AlignCenter)
            lab.setStyleSheet("font-weight:600; padding:6px;")
            heads.addWidget(lab)
        v.addLayout(heads)
        self.video = QWidget()
        self.video.setAttribute(Qt.WA_NativeWindow)
        self.video.setStyleSheet("background:black;")
        v.addWidget(self.video, 1)
        self.slider = ClickSlider(Qt.Horizontal)
        self.slider.setRange(0, 10000)
        row = QHBoxLayout()
        row.setContentsMargins(10, 0, 10, 0)
        self.play_btn = QPushButton(tr("Play"))
        self.back_btn = QPushButton(tr("◀ Frame"))
        self.next_btn = QPushButton(tr("Frame ▶"))
        self.view_btns = {}
        views = QButtonGroup(self)
        for zoom, text in VIEWS:
            b = QPushButton(tr(text))
            b.setObjectName("view")
            b.setCheckable(True)
            b.clicked.connect(lambda _, z=zoom: self.set_view(z))
            views.addButton(b)
            self.view_btns[zoom] = b
        self.view_btns[None].setChecked(True)
        self.detail_btn = self.view_btns[1]
        self.drag_hint = QLabel(tr("Drag the picture to look around"))
        self.drag_hint.setObjectName("hint")
        self.drag_hint.hide()
        self.time_lab = QLabel("0:00 / 0:00")
        self.score = QLabel(tr("VMAF average {mean}, worst 1% {p1}").format(mean=num(rec.vmaf_mean), p1=num(rec.vmaf_p1)))
        self.score.setObjectName("hint")
        for w in (self.play_btn, self.back_btn, self.next_btn, *self.view_btns.values(), self.drag_hint, self.time_lab):
            row.addWidget(w)
        row.addStretch(1)
        row.addWidget(self.score)
        v.addWidget(self.slider)
        v.addLayout(row)
        self.player = None
        self.rec = rec
        self.dragging = False
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.tick)
        self.play_btn.clicked.connect(self.toggle)
        # A window shortcut, so space means pause whichever button has the focus.
        self.space = QShortcut(QKeySequence(Qt.Key_Space), self, self.toggle)
        self.back_btn.clicked.connect(lambda: self.do(lambda: self.player.step(False)))
        self.next_btn.clicked.connect(lambda: self.do(lambda: self.player.step(True)))
        # mpv's own window gets the mouse, so a drag is followed by watching the button and the cursor.
        self.drag = None
        self.was_down = False
        self.drag_timer = QTimer(self)
        self.drag_timer.setInterval(30)
        self.drag_timer.timeout.connect(self.poll_drag)
        self.drag_timer.start()
        self.slider.sliderPressed.connect(lambda: setattr(self, "dragging", True))
        self.slider.sliderReleased.connect(self.seek_released)
        QTimer.singleShot(50, self.begin)

    def begin(self):
        if self.player is not None or not self.isVisible():     # already playing, or closed before it started
            return
        try:
            self.player = SideBySidePlayer(self.rec.source, self.rec.output, wid=int(self.video.winId()))
            self.player.start()
            self.player.play()
            self.timer.start()
            self.tick()
        except PlayerError as ex:
            QMessageBox.warning(self, tr("Could not play"), str(ex))

    def do(self, fn):
        if not self.player:
            return
        try:
            fn()
        except (PlayerError, OSError) as ex:
            self.timer.stop()
            QMessageBox.warning(self, tr("Player"), str(ex))

    def toggle(self):
        def fn():
            if self.player.is_paused():
                self.player.play()
            else:
                self.player.pause()
        self.do(fn)
        self.tick()

    def set_view(self, zoom):
        self.view_btns[zoom].setChecked(True)
        self.drag_hint.setVisible(zoom is not None)
        self.drag = None
        self.do(lambda: self.player.set_view(zoom))

    @staticmethod
    def mouse_state():
        """Whether the main mouse button is down, and where the cursor is."""
        user32 = ctypes.windll.user32
        button = 0x02 if user32.GetSystemMetrics(23) else 0x01      # buttons swapped for left-handed use
        return bool(user32.GetAsyncKeyState(button) & 0x8000), QCursor.pos()

    def video_rect(self):
        return QRectF(QPointF(self.video.mapToGlobal(self.video.rect().topLeft())), self.video.size().toSizeF())

    def poll_drag(self):
        p = self.player
        if not p or not getattr(p, "zoom", None):
            self.drag, self.was_down = None, False
            return
        down, pos = self.mouse_state()
        if self.drag is None:
            if down and not self.was_down and self.isActiveWindow() and self.video_rect().contains(QPointF(pos)):
                self.drag = (pos, p.centre, pos)
            self.was_down = down
            return
        start, centre, last = self.drag
        if pos != last:
            self.drag = (start, centre, pos)
            self.do(lambda: p.set_view(p.zoom, self.dragged_centre(start, centre, pos)))
        if not down:
            self.drag, self.was_down = None, False

    def dragged_centre(self, start, centre, pos):
        """Moving the mouse right moves the picture right, so the view's centre moves left."""
        p = self.player
        w, h = p.conv_width or p.src_width, p.conv_height or p.src_height
        cw, ch, _, _ = p.window()
        z = p.zoom
        scale = min(self.video.width() / (2 * cw * z), self.video.height() / (ch * z)) * z   # screen px per video px
        return (centre[0] - (pos.x() - start.x()) / scale / w, centre[1] - (pos.y() - start.y()) / scale / h)

    def seek_released(self):
        self.dragging = False
        self.do(lambda: self.player.seek(self.slider.value() / 10000 * (self.player.duration() or 0)))

    def tick(self):
        if not self.player:
            return
        try:
            pos, dur = self.player.position() or 0, self.player.duration() or 0
            self.play_btn.setText(tr("Play") if self.player.is_paused() else tr("Pause"))
        except (PlayerError, OSError):
            self.timer.stop()
            return
        if dur and not self.dragging:
            self.slider.setValue(int(pos / dur * 10000))
        self.time_lab.setText(f"{clock(pos)} / {clock(dur)}")

    def closeEvent(self, ev):
        self.timer.stop()
        self.drag_timer.stop()
        if self.player:
            self.player.close()
            self.player = None
        super().closeEvent(ev)

    def reject(self):
        self.close()


STEPS = (N_("Find videos"), N_("See the saving"), N_("Convert"), N_("Compare and clean up"))
CARDS = (N_("Files Processed"), N_("Space Saved"), N_("Current Batch"), N_("Time Remaining"))
TABS = (N_("All"), N_("Completed"), N_("Active"), N_("Waiting"))
STAGES = {"search": N_("Finding the right quality"), "encode": N_("Encoding"), "verify": N_("Measuring every frame"),
          "done": N_("Done")}
SHORT_STAGES = {"search": N_("Finding quality"), "encode": N_("Encoding"), "verify": N_("Measuring")}
WELCOME = (
    ("🎯", N_("Zero guesswork"), N_("No bitrates or codecs to configure. ClipShrink automatically finds the right "
                                    "compression balance for every video.")),
    ("👁️", N_("Measured frame-by-frame"), N_("Every result is scored against the original using Netflix's VMAF visual "
                                             "quality metric, and any clip that misses the target is clearly flagged.")),
    ("🛡️", N_("You stay in control"), N_("Conversions are saved as new files alongside your originals. Compare both "
                                         "versions side by side before deciding what to send to the Recycle Bin.")))


class MainWindow(QMainWindow):
    def __init__(self, db_path=None, work_dir=None):
        super().__init__()
        base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / config.APP_NAME
        self.db_path = Path(db_path) if db_path else base / "state.db"
        self.work_dir = Path(work_dir) if work_dir else base / "work"
        self.settings = app_settings.load(self.db_path)
        use_language(self.settings.language)
        self._live = {}
        self._combos = []
        self._syncing = False
        self.conv_count = None
        self._closing = False
        self._forget_if_finished()
        self.folder = None
        self.stage = 0
        self.action_running = False
        self.result = None
        self.estimate = None
        self.converter = None
        self.scope = []
        self.busy = False
        self.bridge = Bridge()
        self.bridge.call.connect(lambda fn: fn())
        self.live(self, lambda: tr("{app} {version}: shrink videos, keep the quality").format(
            app=config.APP_NAME, version=config.VERSION), "setWindowTitle")
        self.setWindowIcon(QIcon(tools.icon_path()))
        self.resize(1320, 800)
        self.setStyleSheet(STYLE)

        root = QWidget()
        lay = QHBoxLayout(root)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)
        rail = QFrame()
        rail.setObjectName("rail")
        rail.setFixedWidth(210)
        rv = QVBoxLayout(rail)
        rv.setContentsMargins(12, 18, 12, 12)
        name = QLabel(config.APP_NAME)
        name.setStyleSheet("color:white; font-size:15pt; font-weight:600; padding:6px 10px 14px 10px;")
        rv.addWidget(name)
        self.steps = []
        self.step_checks = []
        for n, t in enumerate(STEPS):
            lab = StepLabel()
            lab.setWordWrap(True)       # "Vergleichen und aufräumen" needs two lines
            self.live(lab, lambda n=n, t=t: f"{n + 1}  {tr(t)}")
            lab.clicked.connect(lambda n=n: self._step_clicked(n))
            lab.setObjectName("stepOff")
            # The tick sits beside the step, so a long name never runs under it.
            row = QHBoxLayout()
            row.setSpacing(2)
            row.addWidget(lab, 1)
            check = QLabel("✓")
            check.setObjectName("stepCheck")
            check.setFixedWidth(16)
            check.hide()
            row.addWidget(check)
            rv.addLayout(row)
            self.steps.append(lab)
            self.step_checks.append(check)
        rv.addStretch(1)
        side = ("QPushButton { color:#cfd8e0; background:transparent; border:1px solid #52606d; text-align:left; }"
                "QPushButton:hover { background:#3a4a5a; }")
        self.settings_btn = self.live(QPushButton(), N_("Settings"))
        self.settings_btn.setStyleSheet(side)
        self.settings_btn.clicked.connect(lambda: self.go(4))
        rv.addWidget(self.settings_btn)
        lay.addWidget(rail)
        self.stack = QStackedWidget()
        lay.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.stack.addWidget(self._page_scan())
        self.stack.addWidget(self._page_estimate())
        self.stack.addWidget(self._page_convert())
        self.stack.addWidget(self._page_review())
        self.welcome_page = self._page_welcome()
        self.settings_page = self.about_page = self._page_settings()     # Settings and About share a page
        self.stack.addWidget(self.settings_page)
        self.stack.addWidget(self.welcome_page)
        for t in (self.scan_table, self.est_table, self.conv_table, self.review):
            t.setContextMenuPolicy(Qt.CustomContextMenu)
            t.customContextMenuRequested.connect(lambda pos, t=t: self._table_menu(t, pos))
        self.review.installEventFilter(self)
        self._tick_anchor = None
        self._apply_settings_view()
        self.go(0)
        # A waiting batch goes straight to its "Continue where you left off?" question.
        if not self.settings.skip_welcome and not self._unfinished():
            self.go(5)
        QTimer.singleShot(200, self._offer_resume)

    # --- language ---------------------------------------------------------
    def live(self, widget, text, setter="setText"):
        """Shows text now, and again in the new language whenever it changes. text is English,
        or a function that builds the words in the current language."""
        make = text if callable(text) else (lambda: tr(text))
        self._live[(id(widget), setter)] = (widget, setter, make)
        getattr(widget, setter)(make())
        return widget

    def set_language(self, code):
        """Switches every word on screen at once. Nothing else changes."""
        code = use_language(code)
        if self.settings.language != code:
            self.settings.language = code
            app_settings.save(self.db_path, self.settings)
        self.language_box.blockSignals(True)
        self.language_box.setCurrentIndex(self.language_box.findData(code))
        self.language_box.blockSignals(False)
        self.retranslate()

    def retranslate(self):
        for widget, setter, make in list(self._live.values()):
            getattr(widget, setter)(make())
        for box, items in self._combos:
            for i, (text, _) in enumerate(items):
                box.setItemText(i, tr(text))
        for box in (self.warn_mean_box, self.warn_p1_box, self.min_mean_box, self.min_p1_box):
            box.setLocale(qt_locale())
            box.lineEdit().setText(box.textFromValue(box.value()))     # redraws 95.0 as 95,0
        for t in (self.scan_table, self.est_table, self.conv_table, self.review):
            sorting = t.isSortingEnabled()
            t.setSortingEnabled(False)
            retranslate_table(t)
            t.setSortingEnabled(sorting)
            fit_columns(t)
        self._apply_settings_view()
        self._refresh_conv_summary()
        self._tick_changed()

    # --- plain facts other code and the check rely on ---------------------
    def quality_explanation(self):
        return tr(config.QUALITY_EXPLANATION)

    def can_estimate(self):
        return bool(self.result and self.selected_files())

    def can_convert(self):
        return self.estimate is not None and not self.busy

    def sidebar_buttons(self):
        return [self.settings_btn.text().replace("&&", "&")]

    def delete_confirmation_text(self, count, bytes_total, below_bar=0, resized=0):
        text = ntr("{n} original ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, "
                   "and you can restore originals from the Recycle Bin.",
                   "{n} originals ({size}) will go to the Windows Recycle Bin. Each conversion is re-checked first, "
                   "and you can restore originals from the Recycle Bin.", count).format(n=count, size=human_size(bytes_total))
        if below_bar:
            text += "\n\n" + ntr(
                "⚠ {n} of these has a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). "
                "Once the original is gone from the Recycle Bin, that lost quality can't be recovered.",
                "⚠ {n} of these have a conversion below the recommended quality (VMAF average {mean}, worst 1% {p1}). "
                "Once the original is gone from the Recycle Bin, that lost quality can't be recovered.",
                below_bar).format(n=below_bar, mean=f"{config.VMAF_MEAN_MIN:.0f}", p1=f"{config.VMAF_P1_MIN:.0f}")
        if resized:
            text += "\n\n" + ntr(
                "⚠ {n} of these has a conversion at a lower resolution. Once the original is gone from the Recycle "
                "Bin, that detail is gone for good.",
                "⚠ {n} of these have a conversion at a lower resolution. Once the original is gone from the Recycle "
                "Bin, that detail is gone for good.", resized).format(n=resized)
        return text

    # --- layout helpers ---------------------------------------------------
    def go(self, i):
        self.stack.setCurrentIndex(i)
        if i < 4:
            self.stage = i
            for n, lab in enumerate(self.steps):
                lab.setObjectName("stepOn" if n == i else ("stepDone" if n < i else "stepOff"))
                lab.style().unpolish(lab)
                lab.style().polish(lab)
                self.step_checks[n].setVisible(n < i)
        if i == 3:
            self.refresh_review()
        if i == 4:
            self._refresh_settings_page()
        for n, lab in enumerate(self.steps):
            lab.setCursor(Qt.PointingHandCursor if i >= 4 and n == self.stage else Qt.ArrowCursor)

    def _step_clicked(self, n):
        if n == self.stage and self.stack.currentIndex() >= 4:
            self.go(n)

    def _page(self, title, hint):
        p = QWidget()
        p.setObjectName("page")
        v = QVBoxLayout(p)
        v.setContentsMargins(24, 20, 24, 20)
        v.setSpacing(10)
        t = self.live(QLabel(), title)
        t.setObjectName("title")
        v.addWidget(t)
        h = QLabel()
        if hint:
            self.live(h, hint)
        h.setObjectName("hint")
        h.setWordWrap(True)
        h.setVisible(bool(hint))
        v.addWidget(h)
        return p, v

    def _button(self, text, name=None):
        b = self.live(QPushButton(), text)
        if name:
            b.setObjectName(name)
        return b

    # --- stage 1 ----------------------------------------------------------
    def _page_scan(self):
        p, v = self._page(N_("Find your videos"),
                          N_("Pick a folder. This tool looks through it and every folder inside it, and lists the "
                             "H.264 videos it can shrink. Nothing is changed yet."))
        row = QHBoxLayout()
        self.pick_btn = self._button(N_("Choose folder…"), "primary")
        self.pick_btn.clicked.connect(self.choose_folder)
        self.folder_lab = self.live(QLabel(), N_("No folder chosen"))
        self.folder_lab.setObjectName("hint")
        row.addWidget(self.pick_btn)
        row.addWidget(self.folder_lab, 1)
        v.addLayout(row)
        self.scan_bar = QProgressBar()
        self.scan_bar.hide()
        v.addWidget(self.scan_bar)
        self.scan_table = table([N_("Convert"), N_("File"), N_("Folder"), N_("Size"), N_("Picture"), N_("Length"),
                                 N_("State")], 6, ticks=True, wide=2, pills=6, right=(3, 4, 5))
        self.scan_table.itemChanged.connect(self._selection_changed)
        self.scan_table.cellClicked.connect(self._scan_cell_clicked)
        v.addWidget(self.scan_table, 1)
        self.scan_note = QLabel("")
        self.scan_note.setWordWrap(True)
        v.addWidget(self.scan_note)
        row = QHBoxLayout()
        row.addStretch(1)
        self.to_estimate = self._button(N_("Next: see the saving  →"), "next")
        self.to_estimate.setEnabled(False)
        self.to_estimate.clicked.connect(lambda: self.go(1))
        row.addWidget(self.to_estimate)
        v.addLayout(row)
        return p

    def choose_folder(self):
        d = QFileDialog.getExistingDirectory(self, tr("Choose the folder with your videos"))
        if d:
            self.start_scan(d)

    def start_scan(self, folder):
        self.folder = str(Path(folder))
        self.live(self.folder_lab, lambda f=self.folder: f)
        self.scan_table.setRowCount(0)
        self.result = None
        self.estimate = None
        self._reset_estimate_view()
        self.to_estimate.setEnabled(False)
        self.pick_btn.setEnabled(False)
        self.scan_bar.setRange(0, 0)
        self.scan_bar.show()
        self.live(self.scan_note, N_("Reading your videos…"))

        def work():
            def tick(i, n, _):
                self.bridge.call.emit(lambda: (self.scan_bar.setRange(0, n), self.scan_bar.setValue(i)))
            res = scan_folder(folder, on_progress=tick)
            self.bridge.call.emit(lambda: self._scan_done(res))

        threading.Thread(target=work, daemon=True).start()

    def _scan_done(self, res):
        self._show_scan(res)
        QTimer.singleShot(0, lambda: self._offer_lrv_cleanup(res))

    def _offer_lrv_cleanup(self, res):
        """GoPro previews take up space for nothing once the full video is there."""
        if self.result is not res:
            return
        found = scan.lrv_files(res)
        safe = [p for p in found if scan.lrv_original(p)]
        if not safe:
            return
        total = sum(os.path.getsize(p) for p in safe if os.path.exists(p))
        n = len(safe)
        text = (ntr("Found {n} GoPro LRV file ({size}).", "Found {n} GoPro LRV files ({size}).", n).format(
                    n=n, size=human_size(total)) + "\n\n" +
                tr("An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera "
                   "and its phone app can show quick previews. You don't need it if you have the original video, which "
                   "is beside each of these.") + "\n\n" +
                ntr("Send it to the Recycle Bin?", "Send them to the Recycle Bin?", n))
        if len(found) > len(safe):
            other = len(found) - len(safe)
            text += "\n\n" + ntr("{n} other LRV file will stay, because the original video isn't beside it.",
                                 "{n} other LRV files will stay, because the original video isn't beside them.",
                                 other).format(n=other)
        ans = QMessageBox.question(self, tr("Delete GoPro LRV files?"), text,
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ans == QMessageBox.Yes:
            self._recycle_previews(safe)

    def _recycle_previews(self, paths):
        self.to_estimate.setEnabled(False)
        self.pick_btn.setEnabled(False)
        self.scan_bar.setRange(0, len(paths))
        self.scan_bar.show()

        def work():
            def tick(i, n, _):
                self.bridge.call.emit(lambda: (self.scan_bar.setRange(0, n), self.scan_bar.setValue(i)))
            res = trash.recycle_previews(paths, on_progress=tick)
            self.bridge.call.emit(lambda: self._previews_recycled(res))

        threading.Thread(target=work, daemon=True).start()

    def _previews_recycled(self, res):
        gone = set(res.deleted)
        r = self.result
        r.h264 = [f for f in r.h264 if f.path not in gone]
        r.other = [f for f in r.other if f.path not in gone]
        r.unreadable = [u for u in r.unreadable if u[0] not in gone]
        self._show_scan(r)
        n = len(res.deleted)
        text = ntr("{n} LRV file moved to the Recycle Bin.", "{n} LRV files moved to the Recycle Bin.", n).format(n=n)
        if res.refused:
            text += left_in_place(res.refused)
        QMessageBox.information(self, tr("Done"), text)

    @staticmethod
    def scan_note_text(res):
        n = len(res.h264)
        parts = [ntr("{n} H.264 video, {size}.", "{n} H.264 videos, {size}.", n).format(
            n=n, size=human_size(sum(f.size for f in res.h264)))]
        n265 = sum(1 for f in res.other if f.codec == "hevc")
        if n265:
            parts.append(ntr("{n} video already in H.265, skipped.", "{n} videos already in H.265, skipped.",
                             n265).format(n=n265))
        if len(res.other) > n265:
            n = len(res.other) - n265
            parts.append(ntr("{n} video in another format, skipped.", "{n} videos in another format, skipped.",
                             n).format(n=n))
        if res.unreadable:
            names = ", ".join(Path(p).name for p, _ in res.unreadable[:3]) + ("…" if len(res.unreadable) > 3 else "")
            parts.append(tr("{n} could not be read and were skipped: {names}.").format(n=len(res.unreadable), names=names))
        if not res.h264:
            parts = [tr("No H.264 videos found in this folder or its subfolders.") + " " + " ".join(parts[1:])]
        return " ".join(parts)

    def _show_scan(self, res):
        self.result = res
        self.scan_bar.hide()
        self.pick_btn.setEnabled(True)
        self.scan_table.blockSignals(True)
        self.scan_table.setSortingEnabled(False)
        self.scan_table.setRowCount(len(res.h264) + len(res.other))
        known = {r.source.lower(): r for r in db.read_records(self.db_path)}
        for i, f in enumerate(res.h264):
            rec = known.get(f.path.lower())
            ext = Path(f.path).suffix.lower()
            state = (lambda rec=rec: config.status_text(rec)) if rec and rec.source_size == f.size else words("Ready")
            done = rec is not None and rec.status in ("verified", "below_bar") and rec.source_size == f.size
            beside = res.has_conversion.get(f.path)
            if beside and not done:
                state, done = words("Already has a conversion"), True
            vals = [cell(Path(f.path).name, f.path), folder_cell(f.path), size_cell(f.size),
                    cell(f"{f.width}×{f.height} {f.fps:.0f} fps", key=f.width * f.height),
                    cell(clock(f.duration), key=f.duration),
                    cell(words("GoPro low-res preview, off by default") if ext == ".lrv" else state, beside)]
            self.scan_table.setItem(i, 0, tick_cell(f.path, not (done or ext == ".lrv")))
            for c, it in enumerate(vals, 1):
                self.scan_table.setItem(i, c, it)
        # Everything else in the folder stays visible, with no tick box.
        grey = QColor("#7b8794")
        for i, f in enumerate(res.other, len(res.h264)):
            name = "H.265" if f.codec == "hevc" else f.codec.upper()
            mine = bool(original_stem(f.path))
            state = (lambda name=name, mine=mine: tr("Already {codec}, skipped").format(codec=name)
                     + (" " + tr("(converted by this tool)") if mine else ""))
            vals = [cell(Path(f.path).name, f.path), folder_cell(f.path), size_cell(f.size),
                    cell(f"{f.width}×{f.height} {f.fps:.0f} fps", key=f.width * f.height),
                    cell(clock(f.duration), key=f.duration), cell(state, f.path)]
            box = tick_cell(f.path)
            box.setForeground(grey)
            self.scan_table.setItem(i, 0, box)
            for c, it in enumerate(vals, 1):
                it.setForeground(grey)
                self.scan_table.setItem(i, c, it)
        self.scan_table.setSortingEnabled(True)
        self.scan_table.blockSignals(False)
        fit_columns(self.scan_table)
        self.live(self.scan_note, lambda: self.scan_note_text(res))
        self._selection_changed()

    def _scan_cell_clicked(self, row, col):
        it = self.scan_table.item(row, 0)
        if col == 0 and it is not None and it.data(Qt.CheckStateRole) is not None:
            toggle_tick(self.scan_table, row)

    def selected_files(self):
        if not self.result:
            return []
        by_path = {f.path: f for f in self.result.h264}
        out = []
        for row in range(self.scan_table.rowCount()):
            it = self.scan_table.item(row, 0)
            if it and it.data(Qt.CheckStateRole) is not None and it.checkState() == Qt.Checked:
                f = by_path.get(it.data(Qt.UserRole))
                if f:
                    out.append(f)
        return out

    def _selection_changed(self, *_):
        self.to_estimate.setEnabled(self.can_estimate())
        self.estimate = None
        self._reset_estimate_view()

    # --- stage 2 ----------------------------------------------------------
    def _page_estimate(self):
        p, v = self._page(N_("See the saving before anything converts"),
                          N_("This makes short test encodes from a few of your own files and measures them. Your files "
                             "are only read, and nothing appears in your folders."))
        row = QHBoxLayout()
        self.est_using = QLabel("")
        self.est_using.setObjectName("hint")
        row.addWidget(self.est_using)
        row.addStretch(1)
        self.est_btn = self._button(N_("Run the test encodes"), "primary")
        self.est_btn.clicked.connect(self.start_estimate)
        row.addWidget(self.est_btn)
        v.addLayout(row)
        self.est_bar = QProgressBar()
        self.est_bar.hide()
        v.addWidget(self.est_bar)
        card = QFrame()
        card.setObjectName("card")
        cv = QVBoxLayout(card)
        self.est_big = QLabel()
        self.est_big.setObjectName("big")
        self.est_detail = QLabel()
        self.est_detail.setWordWrap(True)
        cv.addWidget(self.est_big)
        cv.addWidget(self.est_detail)
        v.addWidget(card)
        self.est_table = table([N_("Sample from"), N_("Folder"), N_("At"), N_("Original"), "H.265", N_("VMAF average"),
                                N_("VMAF worst 1%"), N_("Meets the quality target?")], 1, right=(2, 3, 4, 5, 6))
        v.addWidget(self.est_table, 1)
        self.est_target_note = QLabel("")
        self.est_target_note.setObjectName("hint")
        self.est_target_note.setWordWrap(True)
        v.addWidget(self.est_target_note)
        row = QHBoxLayout()
        back = self._button(N_("←  Back"))
        back.clicked.connect(lambda: self.go(0))
        row.addWidget(back)
        row.addStretch(1)
        self.to_convert = self._button(N_("Start converting  →"), "next")
        self.to_convert.setEnabled(False)
        self.to_convert.clicked.connect(self._start_converting)
        row.addWidget(self.to_convert)
        v.addLayout(row)
        self.live(self.est_big, N_("Not measured yet"))
        self.live(self.est_detail, N_("Click \"Run the test encodes\" to measure how much space you would save."))
        return p

    def _reset_estimate_view(self):
        if not hasattr(self, "est_big"):
            return
        self.live(self.est_big, N_("Not measured yet"))
        self.live(self.est_detail, N_("Click \"Run the test encodes\" to measure how much space you would save."))
        self.est_table.setRowCount(0)
        self.to_convert.setEnabled(False)

    def start_estimate(self):
        files = self.selected_files()
        if not files:
            return
        self.busy = True
        self.est_btn.setEnabled(False)
        self.est_bar.setRange(0, 0)
        self.est_bar.show()
        self.live(self.est_big, N_("Measuring…"))
        self.live(self.est_detail, N_("Encoding samples of your files and comparing them with the originals."))
        chosen = self.settings

        def work():
            def tick(i, n, path):
                self.bridge.call.emit(lambda: (self.est_bar.setRange(0, n), self.est_bar.setValue(i)))
            try:
                est = estimate_savings(files, encoder=chosen.hardware, work_dir=self.work_dir / "estimate", on_progress=tick,
                                       codec=chosen.codec, max_resolution=chosen.max_resolution,
                                       quality=chosen.policy())
                self.bridge.call.emit(lambda: self._estimate_done(est))
            except Exception as ex:
                msg = str(ex)
                self.bridge.call.emit(lambda: self._estimate_failed(msg))

        threading.Thread(target=work, daemon=True).start()

    def _estimate_failed(self, msg):
        self.busy = False
        self.est_bar.hide()
        self.est_btn.setEnabled(True)
        self.live(self.est_big, N_("Could not measure"))
        self.live(self.est_detail, lambda: tr("The test encode stopped: {error}").format(error=reason(msg)))

    @staticmethod
    def estimate_detail(est):
        card = est.encoder in ("nvenc", "av1_nvenc")
        n = est.files_sampled
        measured = (ntr("Measured on {n} file using your graphics card.", "Measured on {n} files using your graphics card.", n)
                    if card else ntr("Measured on {n} file using your processor.", "Measured on {n} files using your processor.", n))
        return " ".join((tr("Likely between {low} and {high}, out of {total}.").format(
                            low=human_size(est.low_saved_bytes), high=human_size(est.high_saved_bytes),
                            total=human_size(est.total_source_bytes)),
                         measured.format(n=n),
                         tr("Converting everything should take {time}.").format(time=human_time(est.seconds_estimate))))

    def _estimate_done(self, est):
        self.busy = False
        self.estimate = est
        self.est_bar.hide()
        self.est_btn.setEnabled(True)
        pct = est.expected_saved_bytes / est.total_source_bytes * 100 if est.total_source_bytes else 0
        self.live(self.est_big, lambda: tr("About {size} saved ({pct}%)").format(
            size=human_size(est.expected_saved_bytes), pct=f"{pct:.0f}"))
        self.live(self.est_detail, lambda: self.estimate_detail(est))
        policy = self.settings.policy()
        self.est_table.setSortingEnabled(False)
        self.est_table.setRowCount(len(est.samples))
        for i, s in enumerate(est.samples):
            ok = policy.meets_warning(s.vmaf_mean, s.vmaf_p1)
            name = cell(Path(s.path).name, s.path)
            name.setData(Qt.UserRole, s.path)
            vals = [name, folder_cell(s.path), cell(clock(s.at_seconds), key=s.at_seconds),
                    size_cell(s.source_bytes), size_cell(s.encoded_bytes),
                    score_cell(s.vmaf_mean, policy.warn_mean), score_cell(s.vmaf_p1, policy.warn_p1),
                    cell(words("Yes") if ok else words("⚠ No, would get a warning"))]
            for c, it in enumerate(vals):
                self.est_table.setItem(i, c, it)
        self.est_table.setSortingEnabled(True)
        fit_columns(self.est_table)
        self.to_convert.setEnabled(True)
        n = len(self.selected_files())
        self.live(self.conv_info, lambda: " ".join((
            ntr("{n} video, {size}.", "{n} videos, {size}.", n).format(n=n, size=human_size(est.total_source_bytes)),
            tr("Expected time: {time}. Your computer will not go to sleep while this runs.").format(
                time=human_time(est.seconds_estimate)))))

    # --- stage 3 ----------------------------------------------------------
    def _stat_card(self, title, good=False):
        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(14, 10, 14, 12)
        box.setSpacing(2)
        head = self.live(QLabel(), title)
        head.setObjectName("statTitle")
        head.setAlignment(Qt.AlignCenter)
        value = QLabel("–")
        value.setObjectName("statGood" if good else "statValue")
        value.setAlignment(Qt.AlignCenter)
        box.addWidget(head)
        box.addWidget(value)
        return card, value

    def _page_convert(self):
        p, v = self._page(N_("Convert"), "")
        self.conv_hint = p.findChild(QLabel, "hint")
        self.conv_info = QLabel("")
        self.conv_info.setObjectName("hint")
        self.conv_info.setWordWrap(True)
        v.addWidget(self.conv_info)
        cards = QHBoxLayout()
        self.conv_cards = {}
        for title in CARDS:
            card, value = self._stat_card(title, title == "Space Saved")
            self.conv_cards[title] = value
            cards.addWidget(card)
        v.addLayout(cards)
        progress = QFrame()
        progress.setObjectName("card")
        row = QHBoxLayout(progress)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(16)
        self.pause_btn = self._button(N_("Pause"))
        self.pause_btn.setMinimumWidth(110)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.toggle_pause)
        row.addWidget(self.pause_btn)
        bars = QVBoxLayout()
        bars.setSpacing(4)
        self.overall_lab = self.live(QLabel(), N_("Overall Progress"))
        self.overall_lab.setObjectName("barLabel")
        bars.addWidget(self.overall_lab)
        self.overall_bar = QProgressBar()
        self.overall_bar.setObjectName("barGreen")
        self.overall_bar.setRange(0, 1000)
        self.overall_bar.setTextVisible(False)
        bars.addWidget(self.overall_bar)
        bars.addSpacing(4)
        self.file_lab = self.live(QLabel(), N_("Current File"))
        self.file_lab.setObjectName("barLabel")
        bars.addWidget(self.file_lab)
        self.file_bar = QProgressBar()
        self.file_bar.setObjectName("barBlue")
        self.file_bar.setRange(0, 1000)
        self.file_bar.setTextVisible(False)
        bars.addWidget(self.file_bar)
        row.addLayout(bars, 1)
        v.addWidget(progress)
        tabs = QHBoxLayout()
        tabs.setSpacing(4)
        self.conv_tabs = {}
        group = QButtonGroup(p)
        group.setExclusive(True)
        for key in TABS:
            b = QPushButton(tr(key))
            b.setObjectName("tab")
            b.setCheckable(True)
            b.clicked.connect(self._apply_conv_filter)
            group.addButton(b)
            tabs.addWidget(b)
            self.conv_tabs[key] = b
        self.conv_tabs["All"].setChecked(True)
        tabs.addStretch(1)
        v.addLayout(tabs)
        self.conv_table = table([N_("File"), N_("Folder"), N_("State"), N_("Before"), N_("After"), N_("% Saved"),
                                 N_("VMAF average"), N_("Worst 1%"), N_("Encoding")], 1,
                                pills=2, right=(3, 4, 5, 6, 7))
        self.conv_table.horizontalHeader().sortIndicatorChanged.connect(
            lambda *_: QTimer.singleShot(0, self._apply_conv_filter))
        v.addWidget(self.conv_table, 1)
        row = QHBoxLayout()
        back = self._button(N_("←  Back"))
        back.clicked.connect(lambda: self.go(1))
        self.conv_back = back
        row.addWidget(back)
        row.addStretch(1)
        self.to_review = self._button(N_("Next: compare and clean up  →"), "next")
        self.to_review.clicked.connect(lambda: self.go(3))
        self.to_review.setEnabled(False)
        row.addWidget(self.to_review)
        v.addLayout(row)
        return p

    # --- what the Convert page knows about the running batch
    def _fill_conv_table(self, paths):
        self.conv_state = {p: "Waiting" for p in paths}
        self.conv_recs = {}
        self.conv_stage = {}
        self.conv_eta = None
        self.conv_table.setSortingEnabled(False)
        self.conv_table.setRowCount(len(paths))
        for i, pth in enumerate(paths):
            name = cell(Path(pth).name, pth)
            name.setData(Qt.UserRole, pth)
            vals = [name, folder_cell(pth), cell(words("Waiting")), cell(key=-1), cell(key=-1), cell(key=-1),
                    cell(key=-1), cell(key=-1), cell()]
            for c, it in enumerate(vals):
                self.conv_table.setItem(i, c, it)
        self.conv_table.setSortingEnabled(True)
        fit_columns(self.conv_table)
        self._refresh_conv_summary()

    def conv_totals(self):
        recs = list(getattr(self, "conv_recs", {}).values())
        done = [r for r in recs if r.status not in ("pending", "encoding")]
        made = [r for r in recs if r.status in ("verified", "below_bar") and r.output_size]
        before = sum(r.source_size for r in made)
        saved = before - sum(r.output_size for r in made)
        return dict(done=len(done), total=len(getattr(self, "conv_state", {})), saved=saved,
                    percent=saved / before * 100 if before else 0.0, batch=sum(r.source_size for r in recs))

    def _refresh_conv_summary(self):
        t = self.conv_totals()
        self.conv_cards["Files Processed"].setText(f"{t['done']} / {t['total']}" if t["total"] else "–")
        self.conv_cards["Space Saved"].setText(f"{human_size(t['saved'])} (-{t['percent']:.0f}%)" if t["saved"] else "–")
        self.conv_cards["Current Batch"].setText(human_size(t["batch"]) if t["batch"] else "–")
        counts = {k: 0 for k in ("Completed", "Active", "Waiting")}
        for state in getattr(self, "conv_state", {}).values():
            counts[state] += 1
        self.conv_tabs["All"].setText(f"{tr('All')}  {t['total']}" if t["total"] else tr("All"))
        for key, n in counts.items():
            self.conv_tabs[key].setText(f"{tr(key)}  {n}" if n else tr(key))
        self._apply_conv_filter()

    def _apply_conv_filter(self, *_):
        wanted = next((k for k, b in self.conv_tabs.items() if b.isChecked()), "All")
        state = getattr(self, "conv_state", {})
        for row in range(self.conv_table.rowCount()):
            it = self.conv_table.item(row, 0)
            path = it.data(Qt.UserRole) if it else None
            self.conv_table.setRowHidden(row, wanted != "All" and state.get(path) != wanted)

    def _set_conv_stage(self, path, text):
        if self.conv_stage.get(path) == text:
            return
        self.conv_stage[path] = text
        self.conv_state[path] = "Active"
        i = self._conv_row(path)
        if i is not None:
            self.conv_table.setSortingEnabled(False)
            self.conv_table.setItem(i, 2, cell(words(text)))
            self.conv_table.setSortingEnabled(True)
            fit_columns(self.conv_table)
        self._refresh_conv_summary()

    def _start_converting(self):
        if self.busy or not self.can_convert():
            return
        self.go(2)
        self.start_batch()

    def start_batch(self, resume_paths=None):
        paths = resume_paths or [f.path for f in self.selected_files()]
        chosen = self.settings
        self.busy = True
        self.conv_count = None
        self.pause_btn.setEnabled(True)
        self.live(self.pause_btn, N_("Pause"))
        self.conv_back.setEnabled(False)
        self.to_review.setEnabled(False)
        self.overall_bar.setValue(0)
        self.file_bar.setValue(0)
        self.live(self.conv_cards["Time Remaining"], N_("Calculating…"))
        self._fill_conv_table(paths)
        self.converter = Converter(self.db_path, self.work_dir, encoder=chosen.hardware, codec=chosen.codec,
                                   max_resolution=chosen.max_resolution, quality=chosen.policy(), on_event=lambda ev: self.bridge.call.emit(lambda: self._on_event(ev)))
        self.converter.add_files(paths)
        for p in paths:
            self._show_row(self.converter.record(p))

        def work():
            try:
                self.converter.run()
            except Exception as ex:
                msg = str(ex)
                self.bridge.call.emit(lambda: self._batch_crashed(msg))

        threading.Thread(target=work, daemon=True).start()

    def _conv_row(self, path):
        for row in range(self.conv_table.rowCount()):
            it = self.conv_table.item(row, 0)
            if it and it.data(Qt.UserRole) == path:
                return row
        return None

    def _show_row(self, rec):
        i = self._conv_row(rec.source)
        if i is None:
            return
        self.conv_table.setSortingEnabled(False)
        self.conv_table.setItem(i, 2, result_cell(rec))
        self.conv_table.setItem(i, 3, size_cell(rec.source_size))
        if rec.status in ("verified", "below_bar") and rec.source_size:
            saved = (1 - rec.output_size / rec.source_size) * 100
            self.conv_table.setItem(i, 4, size_cell(rec.output_size))
            self.conv_table.setItem(i, 5, cell(f"{saved:.0f}%", key=saved))
        if rec.vmaf_mean is not None:
            self.conv_table.setItem(i, 6, score_cell(rec.vmaf_mean, rec.warn_mean))
            self.conv_table.setItem(i, 7, score_cell(rec.vmaf_p1, rec.warn_p1))
        self.conv_table.setItem(i, 8, details_cell(rec))
        self.conv_table.setSortingEnabled(True)
        fit_columns(self.conv_table)
        self.conv_recs[rec.source] = rec
        if rec.status not in ("pending", "encoding"):
            self.conv_state[rec.source] = "Completed"
        self._refresh_conv_summary()

    def _on_event(self, ev):
        t = ev["type"]
        if t == "batch_start":
            self.conv_count = ev["count"]
        elif t == "progress":
            self.overall_bar.setValue(int(ev["overall"] * 1000))
            self.file_bar.setValue(int(ev["file_fraction"] * 1000))
            name, stage = Path(ev["path"]).name, STAGES[ev["stage"]]
            self.live(self.file_lab, lambda: tr("Current File: {name}: {stage}").format(name=name, stage=tr(stage)))
            totals = self.conv_totals()
            overall = f"{ev['overall'] * 100:.0f}"
            self.live(self.overall_lab, lambda: tr("Overall Progress: {pct}% ({done} of {total} files)").format(
                pct=overall, done=totals["done"], total=totals["total"]))
            if ev.get("eta_seconds") and not self.converter.is_paused:
                eta = ev["eta_seconds"]
                self.live(self.conv_cards["Time Remaining"], lambda: short_time(eta))
            if ev["stage"] != "done":
                self._set_conv_stage(ev["path"], SHORT_STAGES[ev["stage"]])
        elif t == "file_start":
            self._set_conv_stage(ev["path"], SHORT_STAGES["search"])
        elif t == "file_done":
            self._show_row(ev["record"])
        elif t == "paused":
            self.live(self.pause_btn, N_("Resume"))
            self.live(self.conv_cards["Time Remaining"], N_("Paused"))
        elif t == "resumed":
            self.live(self.pause_btn, N_("Pause"))
        elif t == "batch_done":
            self._batch_finished(ev["summary"])
        elif t == "stopped":
            self.busy = False

    def toggle_pause(self):
        if self.converter.is_paused:
            self.converter.resume()
        else:
            self.converter.pause()

    @staticmethod
    def finished_text(s):
        kept = s["kept_original"] + s["failed"]
        return (tr("Finished: {n} verified").format(n=s["verified"])
                + (tr(", ⚠ {n} below target").format(n=s["below_bar"]) if s["below_bar"] else "")
                + (tr(", {n} kept as original").format(n=kept) if kept else "")
                + (" " + tr("(see next page)") if kept or s["below_bar"] else ""))

    def _batch_finished(self, s):
        self.busy = False
        self.pause_btn.setEnabled(False)
        self.conv_back.setEnabled(True)
        self.to_review.setEnabled(True)
        self.overall_bar.setValue(1000)
        self.live(self.file_lab, N_("Current File: none, the batch is finished"))
        self.file_bar.setValue(1000)
        self.live(self.conv_cards["Time Remaining"], N_("Done"))
        self.live(self.overall_lab, lambda: self.finished_text(s))
        if self.conv_count == 0:
            self.live(self.overall_lab, N_("Nothing left to convert: every selected file is already finished."))

    def _batch_crashed(self, msg):
        self.busy = False
        self.pause_btn.setEnabled(False)
        self.conv_back.setEnabled(True)
        self.to_review.setEnabled(True)
        QMessageBox.warning(self, tr("The batch stopped"),
                            reason(msg) + "\n\n" + tr("Files already verified are safe. Reopen the app to continue."))

    def _unfinished(self):
        return [r for r in db.read_records(self.db_path) if r.status in ("pending", "encoding") and os.path.exists(r.source)]

    def _forget_if_finished(self):
        """Files are only remembered while a batch is unfinished, for crash recovery."""
        if not self._unfinished():
            forget_everything(self.db_path, self.work_dir)

    def start_over(self):
        """Forget every file and go back to an empty step 1. Files and reports aren't touched."""
        if self.busy or self.action_running:
            return
        forget_everything(self.db_path, self.work_dir)
        self.converter = None
        self.folder = None
        self.result = None
        self.estimate = None
        self.live(self.folder_lab, N_("No folder chosen"))
        self.live(self.scan_note, lambda: "")
        self.scan_table.setRowCount(0)
        self.to_estimate.setEnabled(False)
        self._reset_estimate_view()
        self._fill_conv_table([])
        for t in (self.scan_table, self.est_table, self.conv_table, self.review):
            fit_columns(t, force=True)
        self.live(self.conv_cards["Time Remaining"], lambda: "–")
        self.overall_bar.setValue(0)
        self.file_bar.setValue(0)
        self.live(self.overall_lab, N_("Overall Progress"))
        self.live(self.file_lab, N_("Current File"))
        self.pause_btn.setEnabled(False)
        self.to_review.setEnabled(False)
        self.go(0)

    def _offer_resume(self):
        if self.busy or self._closing:      # a batch already started, or the window has gone
            return
        left = self._unfinished()
        if not left:
            return
        ans = QMessageBox.question(self, tr("Continue where you left off?"), ntr(
            "{n} video from your last batch is not finished. Files already verified will not be converted again. "
            "Continue now?",
            "{n} videos from your last batch are not finished. Files already verified will not be converted again. "
            "Continue now?", len(left)).format(n=len(left)))
        if ans == QMessageBox.Yes:
            self.go(2)
            self.start_batch([r.source for r in left])
        else:
            forget_everything(self.db_path, self.work_dir)

    # --- stage 4 ----------------------------------------------------------
    def _page_review(self):
        p, v = self._page(N_("Compare and clean up"),
                          N_("Play any original beside its conversion, in sync. When you are happy, you can send originals "
                             "to the Recycle Bin. This step is optional. Click a column title to sort."))
        self.savings_lab = QLabel("")
        self.savings_lab.setObjectName("big")
        v.addWidget(self.savings_lab)
        row = QHBoxLayout()
        self.select_all_btn = QPushButton(tr("Select All"))
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        row.addWidget(self.select_all_btn)
        self.select_rec_btn = QPushButton(tr("Select Recommended"))
        self.live(self.select_rec_btn, N_("Recommended means the conversion met the quality target, with no warning sign."),
                  "setToolTip")
        self.select_rec_btn.clicked.connect(self.toggle_select_recommended)
        row.addWidget(self.select_rec_btn)
        row.addStretch(1)
        v.addLayout(row)
        self.tick_hint = self.live(QLabel(), N_("Tip: Ctrl+click a row to tick it, Shift+click to tick a range, "
                                                "Ctrl+A to tick all. Right-click a row to open its folder."))
        self.tick_hint.setObjectName("hint")
        self.tick_hint.setWordWrap(True)
        v.addWidget(self.tick_hint)
        self.review = table([N_("Delete?"), N_("Original"), N_("Folder"), N_("Before"), N_("After"), N_("% Saved"),
                             N_("VMAF average"), N_("Worst 1%"), N_("Result"), N_("Encoding")], 8, ticks=True, wide=2,
                            pills=8, right=(3, 4, 5, 6, 7))
        self.review.cellClicked.connect(self._cell_clicked)
        v.addWidget(self.review, 3)
        row = QHBoxLayout()
        self.play_btn = self._button(N_("▶  Play selected side by side"), "primary")
        self.play_btn.clicked.connect(self.play_selected)
        row.addWidget(self.play_btn)
        row.addStretch(1)
        self.rename_btn = self._button(N_("Remove the added tags from names"))
        self.rename_btn.setEnabled(False)
        self.rename_btn.clicked.connect(self.rename_done_files)
        row.addWidget(self.rename_btn)
        self.delete_btn = self._button(N_("Send ticked originals to Recycle Bin…"), "danger")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_ticked)
        row.addWidget(self.delete_btn)
        v.addLayout(row)
        self.action_bar = QProgressBar()
        self.action_bar.setRange(0, 1)
        self.action_bar.hide()
        v.addWidget(self.action_bar)
        self.problem_title = self.live(QLabel(), N_("Needs your attention"))
        self.problem_title.setStyleSheet("font-weight:600;")
        v.addWidget(self.problem_title)
        self.problems = QTextBrowser()
        self.problems.setMaximumHeight(120)
        v.addWidget(self.problems)
        row = QHBoxLayout()
        back = self._button(N_("←  Back"))
        back.clicked.connect(lambda: self.go(2))
        row.addWidget(back)
        row.addStretch(1)
        self.start_over_btn = self._button(N_("Start Over"), "next")
        self.live(self.start_over_btn, N_("Forget these files and go back to step 1. Your videos and reports aren't touched."),
                  "setToolTip")
        self.start_over_btn.clicked.connect(self.start_over)
        row.addWidget(self.start_over_btn)
        v.addLayout(row)
        return p

    def _records_for_view(self):
        return sorted(db.read_records(self.db_path), key=lambda r: r.source.lower())

    def refresh_review(self):
        recs = self._records_for_view()
        allow = {r.source for r in trash.deletable(self.db_path)}
        shown = [r for r in recs if r.status in ("verified", "below_bar", "original_deleted", "kept_original", "failed")]
        self.review_by_source = {r.source: r for r in shown}
        self.review_allow = allow
        self.review.setSortingEnabled(False)
        self.review.setRowCount(len(shown))
        saved = 0
        for i, r in enumerate(shown):
            converted = r.status in ("verified", "below_bar", "original_deleted")
            vals = [tick_cell(r.source, False if r.source in allow else None), cell(Path(r.source).name, r.source),
                    folder_cell(r.source), size_cell(r.source_size)]
            if converted and r.source_size:
                vals += [size_cell(r.output_size),
                         cell(f"{(1 - r.output_size / r.source_size) * 100:.0f}%", key=1 - r.output_size / r.source_size)]
                saved += r.source_size - r.output_size
            else:
                vals += [cell(key=-1), cell(key=-1)]
            vals += [score_cell(r.vmaf_mean, r.warn_mean), score_cell(r.vmaf_p1, r.warn_p1), result_cell(r), details_cell(r)]
            for c, it in enumerate(vals):
                self.review.setItem(i, c, it)
        self.review.setSortingEnabled(True)
        fit_columns(self.review)
        self.live(self.savings_lab, lambda: tr("{size} can be saved once originals are removed").format(
            size=human_size(saved)) if saved else "")
        bad = [r for r in shown if r.status in ("kept_original", "failed", "below_bar")]
        self.live(self.problem_title, lambda: tr("Needs your attention ({n})").format(n=len(bad)) if bad
                  else tr("Needs your attention: nothing"))
        self.live(self.problems, lambda: "\n\n".join(f"{Path(r.source).name}\n  {reason(r.reason)}" for r in bad)
                  or (tr("Every conversion passed.") if shown else tr("Nothing converted yet.")), "setPlainText")
        self._tick_changed()
        n = len(trash.renamable(self.db_path))
        self.rename_btn.setEnabled(bool(n))
        self.live(self.rename_btn, lambda: ntr("Remove the added tags from {n} name…", "Remove the added tags from {n} names…",
                                               n).format(n=n) if n else tr("Remove the added tags from names"))
        self.live(self.rename_btn, N_("Available after an original has been sent to the Recycle Bin."), "setToolTip")
        for row in range(self.review.rowCount()):
            rec = self._review_rec(row)
            if rec and rec.status in ("verified", "below_bar"):
                self.review.selectRow(row)
                break

    def _review_rec(self, row):
        it = self.review.item(row, 0)
        return getattr(self, "review_by_source", {}).get(it.data(Qt.UserRole)) if it else None

    def _review_boxes(self, only_recommended=False):
        """Tick cells of the files that may be deleted. Items, so sorting can't confuse them."""
        out = []
        for row in range(self.review.rowCount()):
            rec = self._review_rec(row)
            if rec and rec.source in getattr(self, "review_allow", ()):
                if not only_recommended or rec.meets_target:
                    out.append((self.review.item(row, 0), rec))
        return out

    def _ticked(self):
        return [rec for it, rec in self._review_boxes() if it.checkState() == Qt.Checked]

    def _review_row_of(self, source):
        for row in range(self.review.rowCount()):
            it = self.review.item(row, 0)
            if it and it.data(Qt.UserRole) == source:
                return row
        return None

    def _cell_clicked(self, row, col, mods=None):
        """Like Explorer, but on the tick boxes: the box or Ctrl+click ticks one row, Shift+click
        ticks a range. A plain click elsewhere only picks the row for Play."""
        mods = QApplication.keyboardModifiers() if mods is None else mods
        rec = self._review_rec(row)
        anchor, self._tick_anchor = self._tick_anchor, rec.source if rec else None
        allow = getattr(self, "review_allow", ())
        if mods & Qt.ShiftModifier and anchor is not None:
            start = self._review_row_of(anchor)
            if start is not None:
                lo, hi = sorted((start, row))
                for r in range(lo, hi + 1):
                    other = self._review_rec(r)
                    if other and other.source in allow and not self.review.isRowHidden(r):
                        self.review.item(r, 0).setCheckState(Qt.Checked)
                self._tick_changed()
                return
        if rec is None or rec.source not in allow:
            return
        if col == 0 or mods & Qt.ControlModifier:
            toggle_tick(self.review, row)
            self._tick_changed()

    def tick_every_deletable(self):
        self._set_ticks(self._review_boxes(), True)

    def eventFilter(self, obj, ev):
        if obj is self.review and ev.type() == QEvent.KeyPress and ev.matches(QKeySequence.SelectAll):
            self.tick_every_deletable()
            return True
        return super().eventFilter(obj, ev)

    def _location_of(self, t, row):
        """The file to show in Explorer. Once an original is in the Recycle Bin, its conversion."""
        path = row_path(t, row)
        if t is self.review:
            rec = self._review_rec(row)
            if rec and rec.output and not os.path.exists(rec.source) and os.path.exists(rec.output):
                path = rec.output
        return path

    def table_menu_actions(self, t, row):
        path = self._location_of(t, row)
        return [(tr("Open file location"), lambda: open_location(path))] if path else []

    def _table_menu(self, t, pos):
        row = t.rowAt(pos.y())
        if row < 0:
            return
        menu = QMenu(t)
        for text, fn in self.table_menu_actions(t, row):
            menu.addAction(text).triggered.connect(fn)
        if menu.actions():
            menu.exec(t.viewport().mapToGlobal(pos))

    def _set_ticks(self, boxes, on):
        for it, _ in boxes:
            it.setCheckState(Qt.Checked if on else Qt.Unchecked)
        self._tick_changed()

    def toggle_select_all(self):
        boxes = self._review_boxes()
        self._set_ticks(boxes, not all(it.checkState() == Qt.Checked for it, _ in boxes))

    def toggle_select_recommended(self):
        boxes = self._review_boxes(only_recommended=True)
        self._set_ticks(boxes, not all(it.checkState() == Qt.Checked for it, _ in boxes))

    def _tick_changed(self, *_):
        n = self._ticked()
        self.delete_btn.setEnabled(bool(n) and not self.action_running)
        count = len(n)
        self.live(self.delete_btn, lambda: ntr("Send {n} ticked original to Recycle Bin…",
                                               "Send {n} ticked originals to Recycle Bin…", count).format(n=count)
                  if count else tr("Tick originals above to delete them"))
        every, good = self._review_boxes(), self._review_boxes(only_recommended=True)
        on = lambda boxes: bool(boxes) and all(it.checkState() == Qt.Checked for it, _ in boxes)
        self.select_all_btn.setText(tr("Deselect All") if on(every) else tr("Select All"))
        self.select_rec_btn.setText(tr("Deselect Recommended") if on(good) else tr("Select Recommended"))
        self.select_all_btn.setEnabled(bool(every) and not self.action_running)
        self.select_rec_btn.setEnabled(bool(good) and not self.action_running)
        self.start_over_btn.setEnabled(not self.busy and not self.action_running)

    def play_selected(self):
        r = self._review_rec(self.review.currentRow())
        if r is None:
            QMessageBox.information(self, tr("Pick a video"), tr("Click a row in the list first."))
            return
        if r.status not in ("verified", "below_bar") or not os.path.exists(r.source) or not os.path.exists(r.output):
            QMessageBox.information(self, tr("Cannot compare"),
                                    tr("This row needs both an original and a verified conversion on disk.") + "\n"
                                    + (reason(r.reason) or ""))
            return
        w = PlayerWindow(self, r)
        w.exec()

    def delete_ticked(self):
        recs = self._ticked()
        if not recs:
            return
        below = sum(1 for r in recs if not config.is_recommended(r.vmaf_mean, r.vmaf_p1))
        resized = sum(1 for r in recs if r.resized)
        d = DeleteDialog(self, self.delete_confirmation_text(len(recs), sum(r.source_size for r in recs), below, resized))
        if d.exec() != QDialog.Accepted or not d.tick.isChecked():
            return
        self.start_delete(recs)

    def _action_progress(self, verb, done, total, path):
        self.action_bar.setRange(0, max(1, total))
        self.action_bar.setValue(done)
        name = Path(path).name if path else tr("finishing")
        self.action_bar.setFormat(tr("{action} {i} of {total}: {name}").format(
            action=tr(verb), i=min(done + 1, total), total=total, name=name))
        self.action_bar.show()

    def _action_begin(self):
        self.action_running = True
        for b in (self.delete_btn, self.rename_btn, self.play_btn):
            b.setEnabled(False)
        self._tick_changed()

    def _action_end(self):
        self.action_running = False
        self.action_bar.hide()
        self.play_btn.setEnabled(True)

    def _run_action(self, verb, job, finish):
        """Runs a file job off the interface thread, feeding the progress bar."""
        self._action_begin()

        def tick(done, total, path):
            self.bridge.call.emit(lambda: self._action_progress(verb, done, total, path))

        def work():
            res = job(tick)
            self.bridge.call.emit(lambda: (self._action_end(), finish(res)))

        threading.Thread(target=work, daemon=True).start()

    def start_delete(self, recs):
        # The dialog already named any below-the-bar files before the user confirmed.
        self._run_action(N_("Re-checking and removing"),
                         lambda tick: trash.delete_originals(self.db_path, [r.source for r in recs], confirmed=True,
                                                             below_bar_confirmed=True, resized_confirmed=True,
                                                             on_progress=tick),
                         self._delete_done)

    def _delete_done(self, res):
        self.refresh_review()
        n = len(res.deleted)
        text = ntr("{n} original moved to the Recycle Bin.", "{n} originals moved to the Recycle Bin.", n).format(n=n)
        if res.refused:
            text += left_in_place(res.refused)
        QMessageBox.information(self, tr("Done"), text)

    def rename_done_files(self):
        recs = trash.renamable(self.db_path)
        if not recs:
            return
        n = len(recs)
        ans = QMessageBox.question(self, tr("Remove the added tags from names?"), ntr(
            "{n} conversion whose original is in the Recycle Bin will take the original's name, for example {name}.",
            "{n} conversions whose original is in the Recycle Bin will take the original's name, for example {name}.",
            n).format(n=n, name=Path(recs[0].source).name) + "\n\n" + tr(
            "Only the name changes. If you later restore an original from the Recycle Bin, Windows will ask what to "
            "do about the same name."))
        if ans == QMessageBox.Yes:
            self.start_rename(recs)

    def start_rename(self, recs):
        self._run_action(N_("Renaming"),
                         lambda tick: trash.remove_suffix(self.db_path, [r.source for r in recs], confirmed=True,
                                                          on_progress=tick),
                         self._rename_done)

    def _rename_done(self, res):
        self.refresh_review()
        n = len(res.renamed)
        text = ntr("{n} file renamed.", "{n} files renamed.", n).format(n=n)
        if res.refused:
            text += left_in_place(res.refused, N_("Left as they are:"))
        QMessageBox.information(self, tr("Done"), text)

    # --- Settings ---------------------------------------------------------
    def _page_settings(self):
        p = QWidget()
        p.setObjectName("page")
        page = QVBoxLayout(p)
        page.setContentsMargins(24, 20, 24, 20)
        page.setSpacing(10)
        columns = QHBoxLayout()
        columns.setSpacing(24)
        page.addLayout(columns, 1)
        left = QVBoxLayout()
        left.setSpacing(10)
        columns.addLayout(left, 3)
        right = QVBoxLayout()
        right.setSpacing(10)
        columns.addLayout(right, 2)
        t = self.live(QLabel(), N_("Settings"))
        t.setObjectName("title")
        left.addWidget(t)
        self.settings_intro = self.live(QLabel(), N_("The default settings suit most people, so you can leave this page "
                                                     "alone. Change something only if you have a reason."))
        self.settings_intro.setWordWrap(True)
        left.addWidget(self.settings_intro)
        holder = QWidget()
        holder.setObjectName("page")
        inner = QVBoxLayout(holder)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(holder)
        card = QFrame()
        card.setObjectName("card")
        grid = QGridLayout(card)
        grid.setContentsMargins(16, 14, 16, 14)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_combo(row, title, items, translate=True):
            label = self.live(QLabel(), title)
            label.setStyleSheet("font-weight:600; background:transparent; border:none;")
            box = QComboBox()
            box.setSizeAdjustPolicy(QComboBox.AdjustToMinimumContentsLengthWithIcon)
            box.setMinimumContentsLength(24)
            for text, value in items:
                box.addItem(tr(text) if translate else text, value)
            if translate:
                self._combos.append((box, items))
            grid.addWidget(label, row, 0)
            grid.addWidget(box, row, 1)
            return box

        def add_note(row):
            note = QLabel("")
            note.setObjectName("hint")
            note.setWordWrap(True)
            note.setStyleSheet("background:transparent; border:none;")
            note.hide()
            grid.addWidget(note, row, 1)
            return note

        # Each language by its own name, so anyone can find theirs.
        self.language_box = add_combo(0, N_("Language"), [(name, code) for code, name in i18n.LANGUAGES.items()],
                                      translate=False)
        self.language_box.setCurrentIndex(self.language_box.findData(i18n.language()))
        self.language_box.currentIndexChanged.connect(lambda _: self.set_language(self.language_box.currentData()))
        self.hardware_box = add_combo(1, N_("Encode with"), [(N_("Graphics card (fast, recommended)"), "gpu"),
                                                             (N_("Processor (slow, works on any PC)"), "cpu")])
        self.using_label = add_note(2)
        self.using_label.show()
        self.codec_box = add_combo(3, N_("Video format"), [(N_("H.265 (recommended)"), "h265"), ("AV1", "av1")])
        self.codec_note = add_note(4)
        self.resolution_box = add_combo(5, N_("Largest size"), [(N_("Keep the original resolution (recommended)"), "original"),
                                                                ("4K", "4k"), ("1080p", "1080p"), ("720p", "720p")])
        self.resolution_note = add_note(6)
        self.details_box = self.live(QCheckBox(), N_("Show an Encoding column"))
        grid.addWidget(self.details_box, 7, 1)
        self.details_note = add_note(8)
        self.live(self.details_note, N_("Format, quality setting, resolution and bitrate of each conversion."))
        self.details_note.show()
        self.show_welcome_box = self.live(QCheckBox(), N_("Show the Welcome screen when the app opens"))
        grid.addWidget(self.show_welcome_box, 9, 1)
        inner.addWidget(card)
        inner.addWidget(self._advanced_card())
        inner.addStretch(1)
        left.addWidget(scroll, 1)
        self._about_column(right)
        row = QHBoxLayout()
        back = self._button(N_("←  Back"))
        back.clicked.connect(lambda: self.go(self.stage))
        row.addWidget(back)
        row.addStretch(1)
        page.addLayout(row)
        self._show_settings_values()
        for box in (self.hardware_box, self.codec_box, self.resolution_box):
            box.currentIndexChanged.connect(self._settings_changed)
        for box in (self.details_box, self.show_welcome_box, self.advanced_box, self.aim_box, self.minimum_box):
            box.toggled.connect(self._settings_changed)
        self.welcome_skip.toggled.connect(self._welcome_skip_changed)
        for box in (self.warn_mean_box, self.warn_p1_box, self.min_mean_box, self.min_p1_box):
            box.valueChanged.connect(self._settings_changed)
        return p

    def _advanced_card(self):
        card = QFrame()
        card.setObjectName("card")
        grid = QGridLayout(card)
        grid.setContentsMargins(16, 14, 16, 14)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(2, 1)
        plain = "background:transparent; border:none;"

        def label(text, bold=False):
            lab = self.live(QLabel(), text)
            lab.setStyleSheet(plain + ("font-weight:600;" if bold else ""))
            return lab

        def number():
            box = QDoubleSpinBox()
            box.setRange(0, 100)
            box.setDecimals(1)
            box.setSingleStep(0.5)
            box.setMinimumWidth(90)
            box.setLocale(qt_locale())
            return box

        def hint(text):
            lab = self.live(QLabel(), text)
            lab.setObjectName("hint")
            lab.setWordWrap(True)
            lab.setStyleSheet(plain)
            return lab

        grid.addWidget(label(N_("Advanced"), True), 0, 0)
        self.advanced_note = self.live(QLabel(), lambda: tr(
            "Only change these if you know what you are doing: they can lower the quality of your videos.")
            + f" <a href='{config.ADVANCED_DOCS_URL}'>{tr('Read what each one does')}</a><br>({config.DOCS_URL})")
        self.advanced_note.setWordWrap(True)
        self.advanced_note.setObjectName("hint")
        self.advanced_note.setStyleSheet(plain)
        self.advanced_note.setOpenExternalLinks(True)
        grid.addWidget(self.advanced_note, 0, 1, 1, 2)
        self.advanced_box = self.live(QCheckBox(), N_("I've read this and understand what I'm doing"))
        grid.addWidget(self.advanced_box, 1, 1, 1, 2)

        self.warn_label = label(N_("Warn below"))
        grid.addWidget(self.warn_label, 2, 0)
        self.warn_mean_box, self.warn_p1_box = number(), number()
        pair = QHBoxLayout()
        pair.setSpacing(10)
        pair.addWidget(label(N_("VMAF average")))
        pair.addWidget(self.warn_mean_box)
        pair.addSpacing(16)
        pair.addWidget(label(N_("Worst 1%")))
        pair.addWidget(self.warn_p1_box)
        pair.addStretch(1)
        grid.addLayout(pair, 2, 1, 1, 2)
        self.aim_box = self.live(QCheckBox(), N_("Also aim for these values when choosing quality"))
        grid.addWidget(self.aim_box, 3, 1, 1, 2)
        self.aim_note = hint(N_("Ticked, lower values make smaller files with lower quality, and higher values make "
                                "larger files. Not ticked, your files stay the same and only the warning moves."))
        grid.addWidget(self.aim_note, 4, 1, 1, 2)
        self.minimum_box = self.live(QCheckBox(), N_("Don't keep a conversion below a minimum"))
        grid.addWidget(self.minimum_box, 5, 1, 1, 2)
        self.min_mean_box, self.min_p1_box = number(), number()
        pair = QHBoxLayout()
        pair.setSpacing(10)
        pair.addWidget(label(N_("VMAF average")))
        pair.addWidget(self.min_mean_box)
        pair.addSpacing(16)
        pair.addWidget(label(N_("Worst 1%")))
        pair.addWidget(self.min_p1_box)
        pair.addStretch(1)
        grid.addLayout(pair, 6, 1, 1, 2)
        self.minimum_note = hint(N_("Below the minimum, nothing is kept and your original stays. Off by default, so "
                                    "every result that is smaller and matches is kept, with a warning if needed."))
        grid.addWidget(self.minimum_note, 7, 1, 1, 2)
        self.settings_reset = self._button(N_("Back to the defaults"))
        self.settings_reset.clicked.connect(self._reset_settings)
        grid.addWidget(self.settings_reset, 8, 2, Qt.AlignRight)
        return card

    def _show_settings_values(self):
        s = self.settings
        for box, value in ((self.hardware_box, s.hardware), (self.codec_box, s.codec), (self.resolution_box, s.max_resolution)):
            box.blockSignals(True)
            box.setCurrentIndex(box.findData(value))
            box.blockSignals(False)
        self._syncing = True
        self.details_box.setChecked(s.show_details)
        self.show_welcome_box.setChecked(not s.skip_welcome)
        self.welcome_skip.setChecked(s.skip_welcome)
        self.advanced_box.setChecked(s.advanced)
        self.warn_mean_box.setValue(s.warn_mean)
        self.warn_p1_box.setValue(s.warn_p1)
        self.aim_box.setChecked(s.aim)
        self.minimum_box.setChecked(s.use_minimum)
        self.min_mean_box.setMaximum(s.warn_mean)
        self.min_p1_box.setMaximum(s.warn_p1)
        self.min_mean_box.setValue(s.min_mean)
        self.min_p1_box.setValue(s.min_p1)
        self._syncing = False

    def _settings_changed(self, *_):
        if self._syncing:
            return
        self._syncing = True    # keeping the minimum under the warning values changes them too
        self.min_mean_box.setMaximum(self.warn_mean_box.value())
        self.min_p1_box.setMaximum(self.warn_p1_box.value())
        self._syncing = False
        def key(s):
            return (s.hardware, s.codec, s.max_resolution, s.policy())
        old = key(self.settings)
        # While the card can't do this format, the box shows Processor without changing the user's choice.
        hardware = self.hardware_box.currentData() if self.hardware_box.model().item(0).isEnabled() else self.settings.hardware
        self.settings = app_settings.Settings(hardware, self.codec_box.currentData(), self.resolution_box.currentData(),
                                              self.details_box.isChecked(), self.advanced_box.isChecked(),
                                              self.warn_mean_box.value(), self.warn_p1_box.value(), self.aim_box.isChecked(),
                                              self.minimum_box.isChecked(), self.min_mean_box.value(), self.min_p1_box.value(),
                                              not self.show_welcome_box.isChecked(), self.settings.language)
        app_settings.save(self.db_path, self.settings)
        if old != key(self.settings):
            self.estimate = None        # the measured saving no longer applies
            self._reset_estimate_view()
        self._apply_settings_view()

    def _reset_settings(self):
        """Every choice back to its default, except the language: that isn't about your videos."""
        self.settings = app_settings.Settings(language=self.settings.language)
        self._show_settings_values()
        self._settings_changed()

    def _card_works(self):
        return encode.encoder_available("av1_nvenc" if self.settings.codec == "av1" else "nvenc")

    def _using_text(self):
        s = self.settings
        codec = config.CODEC_NAMES[s.codec]
        card = encode.resolve_encoder(s.hardware, s.codec) in ("nvenc", "av1_nvenc")
        text = (tr("In use: your graphics card, making {codec} video.") if card
                else tr("In use: your processor, making {codec} video.")).format(codec=codec)
        if not self._card_works():
            found = encode.gpu_name()
            text += " " + (tr("{card} was found, but it can't make {codec} video, so the processor is used.").format(
                               card=found, codec=codec) if found
                           else tr("No compatible graphics card was found (only NVIDIA is supported), so the processor "
                                   "is used."))
        return text

    def _show_card(self):
        """Names the card, greys it out if it can't do this format, and picks what will really be used."""
        ok, found = self._card_works(), encode.gpu_name()
        if ok:
            text = tr("Graphics card (fast, recommended) ({card} detected)").format(card=found or tr("NVIDIA card"))
        elif found:
            text = tr("Graphics card ({card} can't make this format)").format(card=found)
        else:
            text = tr("Graphics card (no compatible graphics card detected)")
        box = self.hardware_box
        box.blockSignals(True)
        box.setItemText(0, text)
        box.model().item(0).setEnabled(ok)
        box.setCurrentIndex(box.findData(self.settings.hardware if ok else "cpu"))
        box.blockSignals(False)

    def _apply_settings_view(self):
        s = self.settings
        self._show_card()
        self.using_label.setText(self._using_text())
        unlocked = s.advanced and not self.busy
        for w in (self.warn_label, self.warn_mean_box, self.warn_p1_box, self.aim_box, self.minimum_box):
            w.setEnabled(unlocked)
        for w in (self.min_mean_box, self.min_p1_box):
            w.setEnabled(unlocked and s.use_minimum)
        policy = s.policy()
        average = tr(config.TIP_AVERAGE)
        if policy.warn_mean != config.VMAF_MEAN_MIN:
            average += " " + tr("Your target is {mean}.").format(mean=g(policy.warn_mean))
        worst = tr(config.TIP_WORST).format(p1=g(policy.warn_p1))
        for t, p1_title in ((self.est_table, "VMAF worst 1%"), (self.conv_table, "Worst 1%"), (self.review, "Worst 1%")):
            for c in range(t.columnCount()):
                key = column_key(t, c)
                if key == "VMAF average":
                    t.horizontalHeaderItem(c).setToolTip(average)
                elif key == p1_title:
                    t.horizontalHeaderItem(c).setToolTip(worst)
        self.est_target_note.setText(tr("The target: VMAF average at least {mean}, worst 1% of frames at least {p1}. Every "
                                        "full file is measured again after conversion.").format(
                                            mean=g(policy.warn_mean), p1=g(policy.warn_p1)))
        self.codec_note.setText(tr("AV1 files are usually smaller, but they play on fewer devices. Check that your TV or "
                                   "phone can play one first."))
        self.codec_note.setVisible(s.codec == "av1")
        self.resolution_note.setText(tr("This permanently lowers the detail in the conversions, and videos are never "
                                        "enlarged. They are checked against a smaller copy of the original and labelled "
                                        "Resized. Keep the originals if you might want the full detail later."))
        self.resolution_note.setVisible(s.max_resolution != "original")
        for t, title in ((self.conv_table, 8), (self.review, 9)):
            t.setColumnHidden(title, not s.show_details)
        codec = config.CODEC_NAMES[s.codec]
        self.est_using.setText(tr("{codec}. Change this in Settings.").format(codec=codec) if s.max_resolution == "original"
                               else tr("{codec}, at most {size}. Change this in Settings.").format(
                                   codec=codec, size=self.resolution_box.currentText()))
        self.conv_hint.show()
        suffix = config.CODEC_SUFFIX[s.codec]
        if s.max_resolution == "original":
            hint = tr("Each conversion is saved beside its original with {suffix} added to the name. Originals are only "
                      "read. You can pause at any time, and if the PC crashes, just reopen this app.").format(suffix=suffix)
        else:
            hint = tr("Each conversion is saved beside its original with {suffix} ({shrunk} if it was shrunk) added to "
                      "the name. Originals are only read. You can pause at any time, and if the PC crashes, just reopen "
                      "this app.").format(suffix=suffix, shrunk=config.output_suffix(s.codec, s.max_resolution))
        self.conv_hint.setText(hint)

    def _refresh_settings_page(self):
        for w in (self.hardware_box, self.codec_box, self.resolution_box, self.settings_reset, self.advanced_box):
            w.setEnabled(not self.busy)
        self._apply_settings_view()

    # --- Welcome ----------------------------------------------------------
    def welcome_text(self):
        return " ".join(lab.text() for lab in self.welcome_page.findChildren(QLabel))

    def _page_welcome(self):
        p = QWidget()
        p.setObjectName("page")
        v = QVBoxLayout(p)
        v.setContentsMargins(60, 30, 60, 30)
        v.addStretch(1)
        title = self.live(QLabel(), lambda: tr("Welcome to {app}").format(app=config.APP_NAME))
        title.setStyleSheet("font-size:30pt; font-weight:700;")
        title.setAlignment(Qt.AlignCenter)
        v.addWidget(title)
        head = self.live(QLabel(), N_("Shrink your videos, keep the quality."))
        head.setObjectName("big")
        head.setAlignment(Qt.AlignCenter)
        v.addWidget(head)
        v.addSpacing(18)
        for mark, name, text in WELCOME:
            card = QFrame()
            card.setObjectName("card")
            row = QHBoxLayout(card)
            row.setContentsMargins(18, 14, 18, 14)
            row.setSpacing(16)
            icon = QLabel(mark)
            icon.setStyleSheet("font-family:'Segoe UI Emoji'; font-size:24pt; background:transparent; border:none;")
            row.addWidget(icon)
            lab = self.live(QLabel(), lambda name=name, text=text: f"<b>{tr(name)}:</b> {tr(text)}")
            lab.setWordWrap(True)
            lab.setStyleSheet("font-size:12pt; background:transparent; border:none;")
            row.addWidget(lab, 1)
            v.addWidget(card)
        v.addSpacing(22)
        self.welcome_choose = self._button(N_("Choose folder…"), "primary")
        self.welcome_choose.setStyleSheet("font-size:13pt; padding:12px 40px;")
        self.welcome_choose.clicked.connect(self._welcome_choose)
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.welcome_choose)
        row.addStretch(1)
        v.addLayout(row)
        v.addSpacing(10)
        self.welcome_skip = self.live(QCheckBox(), N_("Don't show this again"))
        row = QHBoxLayout()
        row.addStretch(1)
        row.addWidget(self.welcome_skip)
        row.addStretch(1)
        v.addLayout(row)
        v.addStretch(1)
        return p

    def _welcome_choose(self):
        d = QFileDialog.getExistingDirectory(self, tr("Choose the folder with your videos"))
        if d:
            self.go(0)
            self.start_scan(d)

    def _welcome_skip_changed(self, skip):
        self.show_welcome_box.setChecked(not skip)      # saved through _settings_changed

    # --- About, the right half of the Settings page ---------------------
    def about_text(self):
        """What the About column says, as plain text."""
        raw = "\n".join(lab.text() for lab in self.about_box.findChildren(QLabel))
        raw = re.sub(r"<br>|</p>", "\n", raw)
        return html.unescape(re.sub(r"<[^>]+>", "", raw)).replace("​", "")

    def about_links(self):
        return re.findall(r"href='([^']+)'", "".join(lab.text() for lab in self.about_box.findChildren(QLabel)))

    def _about_link(self, url):
        """Every link leaves the app: the website for the web ones, Explorer for the folder."""
        url = QUrl(url) if isinstance(url, str) else url
        if url.isLocalFile():
            Path(url.toLocalFile()).mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(url)

    def copy_docs_link(self):
        QApplication.clipboard().setText(config.DOCS_URL)

    def _about_column(self, v):
        t = self.live(QLabel(), lambda: tr("About {app}").format(app=config.APP_NAME))
        t.setObjectName("title")
        v.addWidget(t)
        self.about_box = box = QWidget()
        box.setObjectName("page")
        inner = QVBoxLayout(box)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidget(box)
        v.addWidget(scroll, 1)
        plain = "background:transparent; border:none;"

        def text(words, hint=False, bold=False):
            lab = self.live(QLabel(), words)
            lab.setWordWrap(True)
            lab.setTextFormat(Qt.RichText)
            lab.setStyleSheet(plain + ("font-weight:600;" if bold else ""))
            if hint:
                lab.setObjectName("hint")
            lab.linkActivated.connect(self._about_link)
            return lab

        def card(green=False):
            c = QFrame()
            c.setObjectName("card")
            if green:
                c.setStyleSheet("#card { background:#eaf6f0; border:1px solid #b9dfcc; }")
            lay = QVBoxLayout(c)
            lay.setContentsMargins(16, 12, 16, 12)
            lay.setSpacing(8)
            inner.addWidget(c)
            return lay

        def line(lay, mark, words, *extra):
            row = QHBoxLayout()
            row.setSpacing(10)
            icon = QLabel(mark)
            icon.setStyleSheet(plain + "font-family:'Segoe UI Emoji'; font-size:13pt;")
            icon.setFixedWidth(26)
            row.addWidget(icon, 0, Qt.AlignTop)
            row.addWidget(words, 1)
            for w in extra:
                row.addWidget(w, 0, Qt.AlignTop)
            lay.addLayout(row)

        def small_button(mark, tip, fn):
            b = QPushButton(mark)
            self.live(b, tip, "setToolTip")
            b.setStyleSheet("padding:2px 8px;")
            b.clicked.connect(fn)
            return b

        folder = reports.reports_dir(self.db_path)
        folder_url = QUrl.fromLocalFile(str(folder)).toString()
        folder_text = html.escape(str(folder)).replace("\\", "\\​")     # a long path may wrap at each \
        site = config.DOCS_URL.replace("https://", "").rstrip("/")
        repo = config.PROJECT_URL.replace("https://", "")
        inner.addWidget(text(lambda: f"{config.APP_NAME} {config.VERSION}", bold=True))
        inner.addWidget(text(lambda: tr(
            "{app} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion against its "
            "original with VMAF and warns you about any below the quality target. Your originals are only read during "
            "conversion, and nothing is sent anywhere.").format(app=config.APP_NAME), hint=True))
        lay = card()
        self.docs_open = small_button("↗", N_("Open in your browser"), lambda: self._about_link(config.DOCS_URL))
        self.docs_copy = small_button("⧉", N_("Copy the link"), self.copy_docs_link)
        line(lay, "📄", text(lambda: f"<b>{tr('Documentation:')}</b> <a href='{config.DOCS_URL}'>{site}</a>"),
             self.docs_open, self.docs_copy)
        lay = card()
        line(lay, "🔗", text(lambda: f"<b>{tr('Project:')}</b> <a href='{config.PROJECT_URL}'>{repo}</a>"))
        line(lay, "📁", text(lambda: f"<b>{tr('Reports:')}</b> <a href='{folder_url}'>{folder_text}</a><br>" + html.escape(tr(
            "Each batch leaves a CSV report here. They're only for your information. Once a batch is finished and you "
            "exit or click Start Over, the app forgets those files."))))
        lay = card()
        line(lay, "⚖️", text(lambda: f"<b>{tr('Licence:')}</b> " + html.escape(tr(
            "GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace."))))
        line(lay, "🧩", text(lambda: f"<b>{tr('Built with:')}</b> " + html.escape(tr(
            "FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in THIRD_PARTY_NOTICES.md "
            "in the install folder and on the project page."))))
        lay = card(green=True)
        line(lay, "ⓘ", text(lambda: "<b>" + html.escape(tr('What does "no quality loss" mean?')) + "</b>"))
        lay.addWidget(text(lambda: "".join(f"<p>{html.escape(part, quote=False)}</p>"
                                           for part in tr(config.QUALITY_EXPLANATION).split("\n\n"))))
        inner.addStretch(1)

    def closeEvent(self, ev):
        self._closing = True
        if self.busy and self.converter:
            ans = QMessageBox.question(self, tr("Stop converting?"),
                                       tr("The batch is still running. If you close now, the current file is restarted "
                                          "next time and finished files are kept. Close anyway?"))
            if ans != QMessageBox.Yes:
                ev.ignore()
                self._closing = False
                return
            self.converter.stop()
        elif not self.busy:
            self._forget_if_finished()
        super().closeEvent(ev)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    # Only when run from source, as python.exe. The installed app has its own icon, and an ID
    # with no matching shortcut is the leading suspect for a generic taskbar icon.
    if not getattr(sys, "frozen", False):
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ClipShrink.App")
    app.setWindowIcon(QIcon(tools.icon_path()))
    apply_theme(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
