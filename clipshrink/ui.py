"""The desktop interface: four stages, left to right, one obvious button each."""
import ctypes, html
import os, sys, threading, time
from pathlib import Path
from PySide6.QtCore import QUrl, QObject, QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QDesktopServices, QColor, QKeySequence, QPainter, QPalette, QPen, QShortcut
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox, QDoubleSpinBox, QScrollArea,
                               QButtonGroup, QFileDialog, QFrame, QGridLayout, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QMessageBox,
                               QProgressBar, QPushButton, QSlider, QStackedWidget, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTableWidget, QTableWidgetItem,
                               QTextBrowser, QVBoxLayout, QWidget)
from . import config, db, encode, reports, scan, settings as app_settings, tools, trash
from .encode import Stopped
from .engine import Converter, forget_everything
from .estimate import estimate_savings
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


def human_size(n):
    n = float(n)
    for unit in ("bytes", "KB", "MB", "GB", "TB"):
        if abs(n) < 1000 or unit == "TB":
            return f"{n:.0f} {unit}" if unit == "bytes" else f"{n:.1f} {unit}"
        n /= 1000


def short_time(seconds):
    """For the Time Remaining card: ~3h 32m left."""
    m = max(1, round(seconds / 60))
    if m < 60:
        return f"~{m}m left"
    return f"~{m // 60}h {m % 60:02d}m left"


def human_time(seconds):
    s = int(max(0, seconds))
    if s < 60:
        return "under a minute"
    m = round(s / 60)
    if m < 60:
        return f"about {m} minute{'s' if m != 1 else ''}"
    h, m = divmod(m, 60)
    if h < 48:
        return f"about {h} h {m:02d} min"
    return f"about {h / 24:.1f} days"


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
    """Background and text colour of a status pill."""
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
        back, fore = pill_colours(text)
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


def toggle_tick(t, row):
    it = t.item(row, 0)
    it.setCheckState(Qt.Unchecked if it.checkState() == Qt.Checked else Qt.Checked)


class SortItem(QTableWidgetItem):
    """Sorts by its real value: 900 MB comes before 1.2 GB, and 9.5 before 93.5."""
    def __init__(self, text="", key=None):
        super().__init__(str(text))
        self.key = key

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


def table(headers, stretch=0, ticks=False, wide=None, pills=None, right=()):
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
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
    h.setSectionResizeMode(QHeaderView.ResizeToContents)
    h.setSectionResizeMode(stretch, QHeaderView.Stretch)
    if wide is not None:    # a long folder path needs room, and can be dragged wider
        h.setSectionResizeMode(wide, QHeaderView.Interactive)
        t.setColumnWidth(wide, 200)
    h.setSortIndicator(-1, Qt.AscendingOrder)   # keep the list's own order until a header is clicked
    h.setSortIndicatorShown(True)
    h.setSectionsClickable(True)
    t.setSortingEnabled(True)
    if ticks:
        t.setItemDelegateForColumn(0, TickDelegate(t))
    return t


def cell(text="", tip=None, key=None):
    it = SortItem(text, key)
    if isinstance(key, (int, float)):
        it.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
    if tip:
        it.setToolTip(tip)
    return it


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
BELOW_TIP = "Below the quality target. Compare it with the original before removing the original."


def score_cell(value, minimum):
    if value is None:
        return cell("", key=-1)
    low = value < minimum
    it = cell(f"⚠ {value:.1f}" if low else f"{value:.1f}", BELOW_TIP if low else None, key=value)
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
        bits.append(config.ENCODER_NAMES[rec.encoder])
    if rec.quality is not None:
        bits.append(f"Q{rec.quality:g}")
    if rec.output_width:
        bits.append(f"{rec.output_width}×{rec.output_height}")
    if rec.output_bitrate_mbit:
        bits.append(f"{rec.output_bitrate_mbit:.1f} Mbit/s")
    return ", ".join(bits)


def details_cell(rec):
    return cell(details_text(rec), key=None)


def result_cell(rec):
    renamed = rec.status == "original_deleted" and Path(rec.output).stem.lower() == Path(rec.source).stem.lower()
    text = STATUS_TEXT["renamed"] if renamed else config.status_text(rec)
    converted = rec.status in ("verified", "below_bar", "original_deleted")
    low = converted and rec.vmaf_mean is not None and not rec.meets_target
    if low and "⚠" not in text:
        text = f"⚠ {text}"
    it = cell(text, rec.reason or rec.output)
    if low:
        it.setForeground(AMBER)
    return it


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
        self.setWindowTitle("Send originals to the Recycle Bin?")
        self.resize(540, 280)
        v = QVBoxLayout(self)
        lab = QLabel(text)
        lab.setWordWrap(True)
        v.addWidget(lab)
        self.tick = QCheckBox("I understand. Send these originals to the Recycle Bin.")
        v.addWidget(self.tick)
        box = QDialogButtonBox()
        self.go = box.addButton("Send to Recycle Bin", QDialogButtonBox.AcceptRole)
        self.go.setObjectName("danger")
        self.go.setEnabled(False)
        box.addButton("Keep them", QDialogButtonBox.RejectRole).setDefault(True)
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        self.tick.toggled.connect(self.go.setEnabled)
        v.addWidget(box)


class PlayerWindow(QDialog):
    def __init__(self, parent, rec):
        super().__init__(parent)
        self.setWindowTitle(f"Side by side: {Path(rec.source).name}")
        self.resize(1320, 800)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 8)
        heads = QHBoxLayout()
        codec = config.CODEC_NAMES.get(rec.codec, "H.265")
        for text in ("Original (H.264), shrunk to match" if rec.resized else "Original (H.264)",
                     f"Conversion ({codec})"):
            lab = QLabel(text)
            lab.setAlignment(Qt.AlignCenter)
            lab.setStyleSheet("font-weight:600; padding:6px;")
            heads.addWidget(lab)
        v.addLayout(heads)
        self.video = QWidget()
        self.video.setAttribute(Qt.WA_NativeWindow)
        self.video.setStyleSheet("background:black;")
        v.addWidget(self.video, 1)
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 10000)
        row = QHBoxLayout()
        row.setContentsMargins(10, 0, 10, 0)
        self.play_btn = QPushButton("Play")
        self.back_btn = QPushButton("◀ Frame")
        self.next_btn = QPushButton("Frame ▶")
        self.detail_btn = QPushButton("Zoom to 100% detail")
        self.detail_btn.setCheckable(True)
        self.time_lab = QLabel("0:00 / 0:00")
        self.score = QLabel(f"VMAF average {rec.vmaf_mean:.1f}, worst 1% {rec.vmaf_p1:.1f}")
        self.score.setObjectName("hint")
        for w in (self.play_btn, self.back_btn, self.next_btn, self.detail_btn, self.time_lab):
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
        self.detail_btn.toggled.connect(self.toggle_detail)
        self.slider.sliderPressed.connect(lambda: setattr(self, "dragging", True))
        self.slider.sliderReleased.connect(self.seek_released)
        QTimer.singleShot(50, self.begin)

    def begin(self):
        try:
            self.player = SideBySidePlayer(self.rec.source, self.rec.output, wid=int(self.video.winId()))
            self.player.start()
            self.player.play()
            self.timer.start()
            self.tick()
        except PlayerError as ex:
            QMessageBox.warning(self, "Could not play", str(ex))

    def do(self, fn):
        if not self.player:
            return
        try:
            fn()
        except (PlayerError, OSError) as ex:
            self.timer.stop()
            QMessageBox.warning(self, "Player", str(ex))

    def toggle(self):
        def fn():
            if self.player.is_paused():
                self.player.play()
            else:
                self.player.pause()
        self.do(fn)
        self.tick()

    def toggle_detail(self, on):
        self.detail_btn.setText("Show whole picture" if on else "Zoom to 100% detail")
        self.do(lambda: self.player.set_detail(on))

    def seek_released(self):
        self.dragging = False
        self.do(lambda: self.player.seek(self.slider.value() / 10000 * (self.player.duration() or 0)))

    def tick(self):
        if not self.player:
            return
        try:
            pos, dur = self.player.position() or 0, self.player.duration() or 0
            self.play_btn.setText("Play" if self.player.is_paused() else "Pause")
        except (PlayerError, OSError):
            self.timer.stop()
            return
        if dur and not self.dragging:
            self.slider.setValue(int(pos / dur * 10000))
        f = lambda t: f"{int(t) // 60}:{int(t) % 60:02d}"
        self.time_lab.setText(f"{f(pos)} / {f(dur)}")

    def closeEvent(self, ev):
        self.timer.stop()
        if self.player:
            self.player.close()
            self.player = None
        super().closeEvent(ev)

    def reject(self):
        self.close()


class MainWindow(QMainWindow):
    def __init__(self, db_path=None, work_dir=None):
        super().__init__()
        base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / config.APP_NAME
        self.db_path = Path(db_path) if db_path else base / "state.db"
        self.work_dir = Path(work_dir) if work_dir else base / "work"
        self.settings = app_settings.load(self.db_path)
        self._syncing = False
        self.conv_count = None
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
        self.setWindowTitle(f"{config.APP_NAME} {config.VERSION}: shrink videos, keep the quality")
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
        for n, t in enumerate(("1  Find videos", "2  See the saving", "3  Convert", "4  Compare and clean up")):
            lab = StepLabel(t)
            lab.clicked.connect(lambda n=n: self._step_clicked(n))
            lab.setObjectName("stepOff")
            row = QHBoxLayout(lab)
            row.setContentsMargins(0, 0, 12, 0)
            row.addStretch(1)
            check = QLabel("✓")
            check.setObjectName("stepCheck")
            check.hide()
            row.addWidget(check)
            rv.addWidget(lab)
            self.steps.append(lab)
            self.step_checks.append(check)
        rv.addStretch(1)
        side = ("QPushButton { color:#cfd8e0; background:transparent; border:1px solid #52606d; text-align:left; }"
                "QPushButton:hover { background:#3a4a5a; }")
        self.settings_btn = QPushButton("Settings")
        self.settings_btn.setStyleSheet(side)
        self.settings_btn.clicked.connect(lambda: self.go(5))
        rv.addWidget(self.settings_btn)
        self.about_btn = QPushButton("About")
        self.about_btn.setStyleSheet(side)
        self.about_btn.clicked.connect(lambda: self.go(4))
        rv.addWidget(self.about_btn)
        lay.addWidget(rail)
        self.stack = QStackedWidget()
        lay.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.stack.addWidget(self._page_scan())
        self.stack.addWidget(self._page_estimate())
        self.stack.addWidget(self._page_convert())
        self.stack.addWidget(self._page_review())
        self.about_page = self._page_about()
        self.stack.addWidget(self.about_page)
        self.settings_page = self._page_settings()
        self.stack.addWidget(self.settings_page)
        self._apply_settings_view()
        self.go(0)
        QTimer.singleShot(200, self._offer_resume)

    # --- plain facts other code and the check rely on ---------------------
    def quality_explanation(self):
        return config.QUALITY_EXPLANATION

    def can_estimate(self):
        return bool(self.result and self.selected_files())

    def can_convert(self):
        return self.estimate is not None and not self.busy

    def sidebar_buttons(self):
        return [b.text().replace("&&", "&") for b in (self.settings_btn, self.about_btn)]

    def delete_confirmation_text(self, count, bytes_total, below_bar=0, resized=0):
        text = (f"{count} original{'s' if count != 1 else ''} ({human_size(bytes_total)}) will go to the "
                f"Windows Recycle Bin. Each conversion is re-checked first, and you can restore "
                f"originals from the Recycle Bin.")
        if below_bar:
            text += (f"\n\n⚠ {below_bar} of these {'have' if below_bar != 1 else 'has'} a conversion below the "
                     f"recommended quality (VMAF average {config.VMAF_MEAN_MIN:.0f}, worst 1% {config.VMAF_P1_MIN:.0f}). "
                     "Once the original is gone from the Recycle Bin, that lost quality can't be recovered.")
        if resized:
            text += (f"\n\n⚠ {resized} of these {'have' if resized != 1 else 'has'} a conversion at a lower "
                     "resolution. Once the original is gone from the Recycle Bin, that detail is gone for good.")
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
        if i == 5:
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
        t = QLabel(title)
        t.setObjectName("title")
        v.addWidget(t)
        h = QLabel(hint)
        h.setObjectName("hint")
        h.setWordWrap(True)
        h.setVisible(bool(hint))
        v.addWidget(h)
        return p, v

    # --- stage 1 ----------------------------------------------------------
    def _page_scan(self):
        p, v = self._page("Find your videos",
                          "Pick a folder. This tool looks through it and every folder inside it, and lists the "
                          "H.264 videos it can shrink. Nothing is changed yet.")
        row = QHBoxLayout()
        self.pick_btn = QPushButton("Choose folder…")
        self.pick_btn.setObjectName("primary")
        self.pick_btn.clicked.connect(self.choose_folder)
        self.folder_lab = QLabel("No folder chosen")
        self.folder_lab.setObjectName("hint")
        row.addWidget(self.pick_btn)
        row.addWidget(self.folder_lab, 1)
        v.addLayout(row)
        self.scan_bar = QProgressBar()
        self.scan_bar.hide()
        v.addWidget(self.scan_bar)
        self.scan_table = table(["Convert", "File", "Folder", "Size", "Picture", "Length", "State"], 6, ticks=True, wide=2, pills=6, right=(3, 4, 5))
        self.scan_table.itemChanged.connect(self._selection_changed)
        self.scan_table.cellClicked.connect(self._scan_cell_clicked)
        v.addWidget(self.scan_table, 1)
        self.scan_note = QLabel("")
        self.scan_note.setWordWrap(True)
        v.addWidget(self.scan_note)
        row = QHBoxLayout()
        row.addStretch(1)
        self.to_estimate = QPushButton("Next: see the saving  →")
        self.to_estimate.setObjectName("next")
        self.to_estimate.setEnabled(False)
        self.to_estimate.clicked.connect(lambda: self.go(1))
        row.addWidget(self.to_estimate)
        v.addLayout(row)
        return p

    def choose_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Choose the folder with your videos")
        if d:
            self.start_scan(d)

    def start_scan(self, folder):
        self.folder = str(Path(folder))
        self.folder_lab.setText(self.folder)
        self.scan_table.setRowCount(0)
        self.result = None
        self.estimate = None
        self._reset_estimate_view()
        self.to_estimate.setEnabled(False)
        self.pick_btn.setEnabled(False)
        self.scan_bar.setRange(0, 0)
        self.scan_bar.show()
        self.scan_note.setText("Reading your videos…")

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
        s = "s" if len(safe) != 1 else ""
        text = (f"Found {len(safe)} GoPro LRV file{s} ({human_size(total)}).\n\n"
                "An LRV file is a small, low-resolution copy that a GoPro records alongside each video, so the camera "
                "and its phone app can show quick previews. You don't need it if you have the original video, which "
                f"is beside each of these.\n\nSend {'them' if len(safe) != 1 else 'it'} to the Recycle Bin?")
        if len(found) > len(safe):
            n = len(found) - len(safe)
            text += f"\n\n{n} other LRV file{'s' if n != 1 else ''} will stay, because the original video isn't beside {'them' if n != 1 else 'it'}."
        ans = QMessageBox.question(self, "Delete GoPro LRV files?", text,
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
        text = f"{len(res.deleted)} LRV file{'s' if len(res.deleted) != 1 else ''} moved to the Recycle Bin."
        if res.refused:
            text += "\n\nLeft in place:\n" + "\n".join(f"{Path(p).name}: {why}" for p, why in res.refused)
        QMessageBox.information(self, "Done", text)

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
            state = config.status_text(rec) if rec and rec.source_size == f.size else "Ready"
            done = rec is not None and rec.status in ("verified", "below_bar") and rec.source_size == f.size
            beside = res.has_conversion.get(f.path)
            if beside and not done:
                state, done = "Already has a conversion", True
            vals = [cell(Path(f.path).name, f.path), folder_cell(f.path), cell(human_size(f.size), key=f.size),
                    cell(f"{f.width}×{f.height} {f.fps:.0f} fps", key=f.width * f.height),
                    cell(f"{int(f.duration) // 60}:{int(f.duration) % 60:02d}", key=f.duration),
                    cell("GoPro low-res preview, off by default" if ext == ".lrv" else state, beside)]
            self.scan_table.setItem(i, 0, tick_cell(f.path, not (done or ext == ".lrv")))
            for c, it in enumerate(vals, 1):
                self.scan_table.setItem(i, c, it)
        # Everything else in the folder stays visible, with no tick box.
        grey = QColor("#7b8794")
        for i, f in enumerate(res.other, len(res.h264)):
            name = "H.265" if f.codec == "hevc" else f.codec.upper()
            state = f"Already {name}, skipped" + (" (converted by this tool)" if original_stem(f.path) else "")
            vals = [cell(Path(f.path).name, f.path), folder_cell(f.path), cell(human_size(f.size), key=f.size),
                    cell(f"{f.width}×{f.height} {f.fps:.0f} fps", key=f.width * f.height),
                    cell(f"{int(f.duration) // 60}:{int(f.duration) % 60:02d}", key=f.duration), cell(state, f.path)]
            box = tick_cell(f.path)
            box.setForeground(grey)
            self.scan_table.setItem(i, 0, box)
            for c, it in enumerate(vals, 1):
                it.setForeground(grey)
                self.scan_table.setItem(i, c, it)
        self.scan_table.setSortingEnabled(True)
        self.scan_table.blockSignals(False)
        parts = [f"{len(res.h264)} H.264 video{'s' if len(res.h264) != 1 else ''}, "
                 f"{human_size(sum(f.size for f in res.h264))}."]
        n265 = sum(1 for f in res.other if f.codec == "hevc")
        if n265:
            parts.append(f"{n265} video{'s' if n265 != 1 else ''} already in H.265, skipped.")
        if len(res.other) > n265:
            n = len(res.other) - n265
            parts.append(f"{n} video{'s' if n != 1 else ''} in another format, skipped.")
        if res.unreadable:
            names = ", ".join(Path(p).name for p, _ in res.unreadable[:3])
            parts.append(f"{len(res.unreadable)} could not be read and were skipped: {names}"
                         f"{'…' if len(res.unreadable) > 3 else ''}.")
        if not res.h264:
            parts = [f"No H.264 videos found in this folder or its subfolders. {' '.join(parts[1:])}"]
        self.scan_note.setText(" ".join(parts))
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
        p, v = self._page("See the saving before anything converts",
                          "This makes short test encodes from a few of your own files and measures them. Your files "
                          "are only read, and nothing appears in your folders.")
        row = QHBoxLayout()
        self.est_using = QLabel("")
        self.est_using.setObjectName("hint")
        row.addWidget(self.est_using)
        row.addStretch(1)
        self.est_btn = QPushButton("Run the test encodes")
        self.est_btn.setObjectName("primary")
        self.est_btn.clicked.connect(self.start_estimate)
        row.addWidget(self.est_btn)
        v.addLayout(row)
        self.est_bar = QProgressBar()
        self.est_bar.hide()
        v.addWidget(self.est_bar)
        card = QFrame()
        card.setObjectName("card")
        cv = QVBoxLayout(card)
        self.est_big = QLabel("Not measured yet")
        self.est_big.setObjectName("big")
        self.est_detail = QLabel("Click \"Run the test encodes\" to measure how much space you would save.")
        self.est_detail.setWordWrap(True)
        cv.addWidget(self.est_big)
        cv.addWidget(self.est_detail)
        v.addWidget(card)
        self.est_table = table(["Sample from", "Folder", "At", "Original", "H.265", "VMAF average", "VMAF worst 1%", "Meets the quality target?"], 1, right=(2, 3, 4, 5, 6))
        v.addWidget(self.est_table, 1)
        self.est_target_note = QLabel("")
        self.est_target_note.setObjectName("hint")
        self.est_target_note.setWordWrap(True)
        v.addWidget(self.est_target_note)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(0))
        row.addWidget(back)
        row.addStretch(1)
        self.to_convert = QPushButton("Start converting  →")
        self.to_convert.setObjectName("next")
        self.to_convert.setEnabled(False)
        self.to_convert.clicked.connect(self._start_converting)
        row.addWidget(self.to_convert)
        v.addLayout(row)
        return p

    def _reset_estimate_view(self):
        if not hasattr(self, "est_big"):
            return
        self.est_big.setText("Not measured yet")
        self.est_detail.setText("Click \"Run the test encodes\" to measure how much space you would save.")
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
        self.est_big.setText("Measuring…")
        self.est_detail.setText("Encoding samples of your files and comparing them with the originals.")
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
        self.est_big.setText("Could not measure")
        self.est_detail.setText(f"The test encode stopped: {msg}")

    def _estimate_done(self, est):
        self.busy = False
        self.estimate = est
        self.est_bar.hide()
        self.est_btn.setEnabled(True)
        pct = est.expected_saved_bytes / est.total_source_bytes * 100 if est.total_source_bytes else 0
        self.est_big.setText(f"About {human_size(est.expected_saved_bytes)} saved ({pct:.0f}%)")
        speed = "graphics card" if est.encoder in ("nvenc", "av1_nvenc") else "processor"
        self.est_detail.setText(
            f"Likely between {human_size(est.low_saved_bytes)} and {human_size(est.high_saved_bytes)}, out of "
            f"{human_size(est.total_source_bytes)}. Measured on {est.files_sampled} file"
            f"{'s' if est.files_sampled != 1 else ''} using your {speed}. "
            f"Converting everything should take {human_time(est.seconds_estimate)}.")
        policy = self.settings.policy()
        self.est_table.setSortingEnabled(False)
        self.est_table.setRowCount(len(est.samples))
        for i, s in enumerate(est.samples):
            ok = policy.meets_warning(s.vmaf_mean, s.vmaf_p1)
            vals = [cell(Path(s.path).name, s.path), folder_cell(s.path),
                    cell(f"{int(s.at_seconds) // 60}:{int(s.at_seconds) % 60:02d}", key=s.at_seconds),
                    cell(human_size(s.source_bytes), key=s.source_bytes), cell(human_size(s.encoded_bytes), key=s.encoded_bytes),
                    score_cell(s.vmaf_mean, policy.warn_mean), score_cell(s.vmaf_p1, policy.warn_p1),
                    cell("Yes" if ok else "⚠ No, would get a warning")]
            for c, it in enumerate(vals):
                self.est_table.setItem(i, c, it)
        self.est_table.setSortingEnabled(True)
        self.to_convert.setEnabled(True)
        self.conv_info.setText(f"{len(self.selected_files())} video{'s' if len(self.selected_files()) != 1 else ''}, {human_size(est.total_source_bytes)}. "
                               f"Expected time: {human_time(est.seconds_estimate)}. Your computer will not go to sleep "
                               f"while this runs.")

    # --- stage 3 ----------------------------------------------------------
    def _stat_card(self, title, good=False):
        card = QFrame()
        card.setObjectName("card")
        box = QVBoxLayout(card)
        box.setContentsMargins(14, 10, 14, 12)
        box.setSpacing(2)
        head = QLabel(title)
        head.setObjectName("statTitle")
        head.setAlignment(Qt.AlignCenter)
        value = QLabel("–")
        value.setObjectName("statGood" if good else "statValue")
        value.setAlignment(Qt.AlignCenter)
        box.addWidget(head)
        box.addWidget(value)
        return card, value

    def _page_convert(self):
        p, v = self._page("Convert", "")
        self.conv_hint = p.findChild(QLabel, "hint")
        self.conv_info = QLabel("")
        self.conv_info.setObjectName("hint")
        self.conv_info.setWordWrap(True)
        v.addWidget(self.conv_info)
        cards = QHBoxLayout()
        self.conv_cards = {}
        for title, good in (("Files Processed", False), ("Space Saved", True), ("Current Batch", False),
                            ("Time Remaining", False)):
            card, value = self._stat_card(title, good)
            self.conv_cards[title] = value
            cards.addWidget(card)
        v.addLayout(cards)
        progress = QFrame()
        progress.setObjectName("card")
        row = QHBoxLayout(progress)
        row.setContentsMargins(14, 12, 14, 12)
        row.setSpacing(16)
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setMinimumWidth(110)
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.toggle_pause)
        row.addWidget(self.pause_btn)
        bars = QVBoxLayout()
        bars.setSpacing(4)
        self.overall_lab = QLabel("Overall Progress")
        self.overall_lab.setObjectName("barLabel")
        bars.addWidget(self.overall_lab)
        self.overall_bar = QProgressBar()
        self.overall_bar.setObjectName("barGreen")
        self.overall_bar.setRange(0, 1000)
        self.overall_bar.setTextVisible(False)
        bars.addWidget(self.overall_bar)
        bars.addSpacing(4)
        self.file_lab = QLabel("Current File")
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
        for key in ("All", "Completed", "Active", "Waiting"):
            b = QPushButton(key)
            b.setObjectName("tab")
            b.setCheckable(True)
            b.clicked.connect(self._apply_conv_filter)
            group.addButton(b)
            tabs.addWidget(b)
            self.conv_tabs[key] = b
        self.conv_tabs["All"].setChecked(True)
        tabs.addStretch(1)
        v.addLayout(tabs)
        self.conv_table = table(["File", "Folder", "State", "Before", "After", "% Saved", "VMAF average", "Worst 1%",
                                 "Encoding"], 1,
                                pills=2, right=(3, 4, 5, 6, 7))
        self.conv_table.horizontalHeader().sortIndicatorChanged.connect(
            lambda *_: QTimer.singleShot(0, self._apply_conv_filter))
        v.addWidget(self.conv_table, 1)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(1))
        self.conv_back = back
        row.addWidget(back)
        row.addStretch(1)
        self.to_review = QPushButton("Next: compare and clean up  →")
        self.to_review.setObjectName("next")
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
            vals = [name, folder_cell(pth), cell("Waiting"), cell(key=-1), cell(key=-1), cell(key=-1), cell(key=-1),
                    cell(key=-1), cell()]
            for c, it in enumerate(vals):
                self.conv_table.setItem(i, c, it)
        self.conv_table.setSortingEnabled(True)
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
        self.conv_tabs["All"].setText(f"All  {t['total']}" if t["total"] else "All")
        for key, n in counts.items():
            self.conv_tabs[key].setText(f"{key}  {n}" if n else key)
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
            self.conv_table.setItem(i, 2, cell(text))
            self.conv_table.setSortingEnabled(True)
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
        self.pause_btn.setText("Pause")
        self.conv_back.setEnabled(False)
        self.to_review.setEnabled(False)
        self.overall_bar.setValue(0)
        self.file_bar.setValue(0)
        self.conv_cards["Time Remaining"].setText("Calculating…")
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
        self.conv_table.setItem(i, 3, cell(human_size(rec.source_size), key=rec.source_size))
        if rec.status in ("verified", "below_bar") and rec.source_size:
            saved = (1 - rec.output_size / rec.source_size) * 100
            self.conv_table.setItem(i, 4, cell(human_size(rec.output_size), key=rec.output_size))
            self.conv_table.setItem(i, 5, cell(f"{saved:.0f}%", key=saved))
        if rec.vmaf_mean is not None:
            self.conv_table.setItem(i, 6, score_cell(rec.vmaf_mean, rec.warn_mean))
            self.conv_table.setItem(i, 7, score_cell(rec.vmaf_p1, rec.warn_p1))
        self.conv_table.setItem(i, 8, details_cell(rec))
        self.conv_table.setSortingEnabled(True)
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
            stage = {"search": "Finding the right quality", "encode": "Encoding", "verify": "Measuring every frame",
                     "done": "Done"}[ev["stage"]]
            self.file_lab.setText(f"Current File: {Path(ev['path']).name}: {stage}")
            totals = self.conv_totals()
            self.overall_lab.setText(f"Overall Progress: {ev['overall'] * 100:.0f}% "
                                     f"({totals['done']} of {totals['total']} files)")
            if ev.get("eta_seconds") and not self.converter.is_paused:
                self.conv_cards["Time Remaining"].setText(short_time(ev["eta_seconds"]))
            if ev["stage"] != "done":
                self._set_conv_stage(ev["path"], {"search": "Finding quality", "encode": "Encoding",
                                                  "verify": "Measuring"}[ev["stage"]])
        elif t == "file_start":
            self._set_conv_stage(ev["path"], "Finding quality")
        elif t == "file_done":
            self._show_row(ev["record"])
        elif t == "paused":
            self.pause_btn.setText("Resume")
            self.conv_cards["Time Remaining"].setText("Paused")
        elif t == "resumed":
            self.pause_btn.setText("Pause")
        elif t == "batch_done":
            self._batch_finished(ev["summary"])
        elif t == "stopped":
            self.busy = False

    def toggle_pause(self):
        if self.converter.is_paused:
            self.converter.resume()
        else:
            self.converter.pause()

    def _batch_finished(self, s):
        self.busy = False
        self.pause_btn.setEnabled(False)
        self.conv_back.setEnabled(True)
        self.to_review.setEnabled(True)
        self.overall_bar.setValue(1000)
        self.file_lab.setText("Current File: none, the batch is finished")
        self.file_bar.setValue(1000)
        self.conv_cards["Time Remaining"].setText("Done")
        kept = s["kept_original"] + s["failed"]
        self.overall_lab.setText(f"Finished: {s['verified']} verified"
                                 + (f", ⚠ {s['below_bar']} below target" if s["below_bar"] else "")
                                 + (f", {kept} kept as original" if kept else "")
                                 + (" (see next page)" if kept or s["below_bar"] else ""))
        if self.conv_count == 0:
            self.overall_lab.setText("Nothing left to convert: every selected file is already finished.")

    def _batch_crashed(self, msg):
        self.busy = False
        self.pause_btn.setEnabled(False)
        self.conv_back.setEnabled(True)
        self.to_review.setEnabled(True)
        QMessageBox.warning(self, "The batch stopped", f"{msg}\n\nFiles already verified are safe. Reopen the app to continue.")

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
        self.folder_lab.setText("No folder chosen")
        self.scan_note.setText("")
        self.scan_table.setRowCount(0)
        self.to_estimate.setEnabled(False)
        self._reset_estimate_view()
        self._fill_conv_table([])
        self.conv_cards["Time Remaining"].setText("–")
        self.overall_bar.setValue(0)
        self.file_bar.setValue(0)
        self.overall_lab.setText("Overall Progress")
        self.file_lab.setText("Current File")
        self.pause_btn.setEnabled(False)
        self.to_review.setEnabled(False)
        self.go(0)

    def _offer_resume(self):
        if self.busy:       # a batch already started: nothing to offer
            return
        left = self._unfinished()
        if not left:
            return
        ans = QMessageBox.question(self, "Continue where you left off?",
                                   f"{len(left)} video{'s' if len(left) != 1 else ''} from your last batch "
                                   f"{'are' if len(left) != 1 else 'is'} not finished. Files already verified will "
                                   "not be converted again. Continue now?")
        if ans == QMessageBox.Yes:
            self.go(2)
            self.start_batch([r.source for r in left])
        else:
            forget_everything(self.db_path, self.work_dir)

    # --- stage 4 ----------------------------------------------------------
    def _page_review(self):
        p, v = self._page("Compare and clean up",
                          "Play any original beside its conversion, in sync. When you are happy, you can send originals "
                          "to the Recycle Bin. This step is optional. Click a column title to sort.")
        self.savings_lab = QLabel("")
        self.savings_lab.setObjectName("big")
        v.addWidget(self.savings_lab)
        row = QHBoxLayout()
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.toggle_select_all)
        row.addWidget(self.select_all_btn)
        self.select_rec_btn = QPushButton("Select Recommended")
        self.select_rec_btn.setToolTip("Recommended means the conversion met the quality target, with no warning sign.")
        self.select_rec_btn.clicked.connect(self.toggle_select_recommended)
        row.addWidget(self.select_rec_btn)
        row.addStretch(1)
        v.addLayout(row)
        self.review = table(["Delete?", "Original", "Folder", "Before", "After", "% Saved", "VMAF average", "Worst 1%",
                             "Result", "Encoding"], 8, ticks=True, wide=2, pills=8, right=(3, 4, 5, 6, 7))
        self.review.cellClicked.connect(self._cell_clicked)
        v.addWidget(self.review, 3)
        row = QHBoxLayout()
        self.play_btn = QPushButton("▶  Play selected side by side")
        self.play_btn.setObjectName("primary")
        self.play_btn.clicked.connect(self.play_selected)
        row.addWidget(self.play_btn)
        row.addStretch(1)
        self.rename_btn = QPushButton("Remove the added tags from names")
        self.rename_btn.setEnabled(False)
        self.rename_btn.clicked.connect(self.rename_done_files)
        row.addWidget(self.rename_btn)
        self.delete_btn = QPushButton("Send ticked originals to Recycle Bin…")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_ticked)
        row.addWidget(self.delete_btn)
        v.addLayout(row)
        self.action_bar = QProgressBar()
        self.action_bar.setRange(0, 1)
        self.action_bar.hide()
        v.addWidget(self.action_bar)
        self.problem_title = QLabel("Needs your attention")
        self.problem_title.setStyleSheet("font-weight:600;")
        v.addWidget(self.problem_title)
        self.problems = QTextBrowser()
        self.problems.setMaximumHeight(120)
        v.addWidget(self.problems)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(2))
        row.addWidget(back)
        row.addStretch(1)
        self.start_over_btn = QPushButton("Start Over")
        self.start_over_btn.setObjectName("next")
        self.start_over_btn.setToolTip("Forget these files and go back to step 1. Your videos and reports aren't touched.")
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
                    folder_cell(r.source), cell(human_size(r.source_size), key=r.source_size)]
            if converted and r.source_size:
                vals += [cell(human_size(r.output_size), key=r.output_size),
                         cell(f"{(1 - r.output_size / r.source_size) * 100:.0f}%", key=1 - r.output_size / r.source_size)]
                saved += r.source_size - r.output_size
            else:
                vals += [cell(key=-1), cell(key=-1)]
            vals += [score_cell(r.vmaf_mean, r.warn_mean), score_cell(r.vmaf_p1, r.warn_p1), result_cell(r), details_cell(r)]
            for c, it in enumerate(vals):
                self.review.setItem(i, c, it)
        self.review.setSortingEnabled(True)
        self.savings_lab.setText(f"{human_size(saved)} can be saved once originals are removed" if saved else "")
        bad = [r for r in shown if r.status in ("kept_original", "failed", "below_bar")]
        self.problem_title.setText(f"Needs your attention ({len(bad)})" if bad else "Needs your attention: nothing")
        self.problems.setPlainText("\n\n".join(f"{Path(r.source).name}\n  {r.reason}" for r in bad)
                                   or ("Every conversion passed." if shown else "Nothing converted yet."))
        self._tick_changed()
        n = len(trash.renamable(self.db_path))
        self.rename_btn.setEnabled(bool(n))
        self.rename_btn.setText(f"Remove the added tags from {n} name{'s' if n != 1 else ''}…" if n
                                else "Remove the added tags from names")
        self.rename_btn.setToolTip("Available after an original has been sent to the Recycle Bin.")
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

    def _cell_clicked(self, row, col):
        rec = self._review_rec(row)
        if col != 0 or rec is None or rec.source not in getattr(self, "review_allow", ()):
            return
        toggle_tick(self.review, row)
        self._tick_changed()

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
        self.delete_btn.setText(f"Send {len(n)} ticked original{'s' if len(n) != 1 else ''} to Recycle Bin…"
                                if n else "Tick originals above to delete them")
        every, good = self._review_boxes(), self._review_boxes(only_recommended=True)
        on = lambda boxes: bool(boxes) and all(it.checkState() == Qt.Checked for it, _ in boxes)
        self.select_all_btn.setText("Deselect All" if on(every) else "Select All")
        self.select_rec_btn.setText("Deselect Recommended" if on(good) else "Select Recommended")
        self.select_all_btn.setEnabled(bool(every) and not self.action_running)
        self.select_rec_btn.setEnabled(bool(good) and not self.action_running)
        self.start_over_btn.setEnabled(not self.busy and not self.action_running)

    def play_selected(self):
        r = self._review_rec(self.review.currentRow())
        if r is None:
            QMessageBox.information(self, "Pick a video", "Click a row in the list first.")
            return
        if r.status not in ("verified", "below_bar") or not os.path.exists(r.source) or not os.path.exists(r.output):
            QMessageBox.information(self, "Cannot compare",
                                    "This row needs both an original and a verified conversion on disk.\n" + (r.reason or ""))
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
        name = Path(path).name if path else "finishing"
        self.action_bar.setFormat(f"{verb} {min(done + 1, total)} of {total}: {name}")
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
        self._run_action("Re-checking and removing",
                         lambda tick: trash.delete_originals(self.db_path, [r.source for r in recs], confirmed=True,
                                                             below_bar_confirmed=True, resized_confirmed=True,
                                                             on_progress=tick),
                         self._delete_done)

    def _delete_done(self, res):
        self.refresh_review()
        text = f"{len(res.deleted)} original{'s' if len(res.deleted) != 1 else ''} moved to the Recycle Bin."
        if res.refused:
            text += "\n\nLeft in place:\n" + "\n".join(f"{Path(p).name}: {why}" for p, why in res.refused)
        QMessageBox.information(self, "Done", text)

    def rename_done_files(self):
        recs = trash.renamable(self.db_path)
        if not recs:
            return
        ans = QMessageBox.question(self, "Remove the added tags from names?",
                                   f"{len(recs)} conversion{'s' if len(recs) != 1 else ''} whose original is in the "
                                   f"Recycle Bin will take the original's name, for example "
                                   f"{Path(recs[0].source).name}.\n\nOnly the name changes. If you later restore an "
                                   "original from the Recycle Bin, Windows will ask what to do about the same name.")
        if ans == QMessageBox.Yes:
            self.start_rename(recs)

    def start_rename(self, recs):
        self._run_action("Renaming",
                         lambda tick: trash.remove_suffix(self.db_path, [r.source for r in recs], confirmed=True,
                                                          on_progress=tick),
                         self._rename_done)

    def _rename_done(self, res):
        self.refresh_review()
        text = f"{len(res.renamed)} file{'s' if len(res.renamed) != 1 else ''} renamed."
        if res.refused:
            text += "\n\nLeft as they are:\n" + "\n".join(f"{Path(p).name}: {why}" for p, why in res.refused)
        QMessageBox.information(self, "Done", text)

    # --- Settings ---------------------------------------------------------
    def _page_settings(self):
        p, v = self._page("Settings", "")
        self.settings_intro = QLabel("The default settings suit most people, so you can leave this page alone. "
                                     "Change something only if you have a reason.")
        self.settings_intro.setWordWrap(True)
        v.addWidget(self.settings_intro)
        holder = QWidget()
        holder.setObjectName("page")
        inner = QVBoxLayout(holder)
        inner.setContentsMargins(0, 0, 0, 0)
        inner.setSpacing(10)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(holder)
        card = QFrame()
        card.setObjectName("card")
        grid = QGridLayout(card)
        grid.setContentsMargins(16, 14, 16, 14)
        grid.setVerticalSpacing(10)
        grid.setColumnStretch(1, 1)

        def add_combo(row, title, items):
            label = QLabel(title)
            label.setStyleSheet("font-weight:600; background:transparent; border:none;")
            box = QComboBox()
            for text, value in items:
                box.addItem(text, value)
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

        self.hardware_box = add_combo(0, "Encode with", [("Graphics card (fast, recommended)", "gpu"),
                                                         ("Processor (slow, works on any PC)", "cpu")])
        self.using_label = add_note(1)
        self.using_label.show()
        self.codec_box = add_combo(2, "Video format", [("H.265 (recommended)", "h265"), ("AV1", "av1")])
        self.codec_note = add_note(3)
        self.resolution_box = add_combo(4, "Largest size", [("Keep the original resolution (recommended)", "original"),
                                                            ("4K", "4k"), ("1080p", "1080p"), ("720p", "720p")])
        self.resolution_note = add_note(5)
        self.details_box = QCheckBox("Show an Encoding column with format, quality setting, resolution and bitrate")
        grid.addWidget(self.details_box, 6, 1)
        inner.addWidget(card)
        inner.addWidget(self._advanced_card())
        inner.addStretch(1)
        v.addWidget(scroll, 1)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(self.stage))
        row.addWidget(back)
        row.addStretch(1)
        self.settings_reset = QPushButton("Back to the defaults")
        self.settings_reset.clicked.connect(self._reset_settings)
        row.addWidget(self.settings_reset)
        v.addLayout(row)
        self._show_settings_values()
        for box in (self.hardware_box, self.codec_box, self.resolution_box):
            box.currentIndexChanged.connect(self._settings_changed)
        for box in (self.details_box, self.advanced_box, self.aim_box, self.minimum_box):
            box.toggled.connect(self._settings_changed)
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
            lab = QLabel(text)
            lab.setStyleSheet(plain + ("font-weight:600;" if bold else ""))
            return lab

        def number():
            box = QDoubleSpinBox()
            box.setRange(0, 100)
            box.setDecimals(1)
            box.setSingleStep(0.5)
            box.setMinimumWidth(90)
            return box

        grid.addWidget(label("Advanced", True), 0, 0)
        self.advanced_note = QLabel(
            "Only change these if you know what you are doing: they can lower the quality of your videos. "
            f"<a href='{config.ADVANCED_DOCS_URL}'>Read what each one does</a> ({config.DOCS_URL}).")
        self.advanced_note.setWordWrap(True)
        self.advanced_note.setObjectName("hint")
        self.advanced_note.setStyleSheet(plain)
        self.advanced_note.setOpenExternalLinks(True)
        grid.addWidget(self.advanced_note, 0, 1, 1, 2)
        self.advanced_box = QCheckBox("I've read this and understand what I'm doing")
        grid.addWidget(self.advanced_box, 1, 1, 1, 2)

        self.warn_label = label("Warn below")
        grid.addWidget(self.warn_label, 2, 0)
        self.warn_mean_box, self.warn_p1_box = number(), number()
        pair = QHBoxLayout()
        pair.setSpacing(10)
        pair.addWidget(label("VMAF average"))
        pair.addWidget(self.warn_mean_box)
        pair.addSpacing(16)
        pair.addWidget(label("Worst 1%"))
        pair.addWidget(self.warn_p1_box)
        pair.addStretch(1)
        grid.addLayout(pair, 2, 1, 1, 2)
        self.aim_box = QCheckBox("Also aim for these values when choosing quality")
        grid.addWidget(self.aim_box, 3, 1, 1, 2)
        self.aim_note = QLabel("Ticked, lower values make smaller files with lower quality, and higher values make "
                               "larger files. Not ticked, your files stay the same and only the warning moves.")
        self.aim_note.setObjectName("hint")
        self.aim_note.setWordWrap(True)
        self.aim_note.setStyleSheet(plain)
        grid.addWidget(self.aim_note, 4, 1, 1, 2)
        self.minimum_box = QCheckBox("Don't keep a conversion below a minimum")
        grid.addWidget(self.minimum_box, 5, 1, 1, 2)
        self.min_mean_box, self.min_p1_box = number(), number()
        pair = QHBoxLayout()
        pair.setSpacing(10)
        pair.addWidget(label("VMAF average"))
        pair.addWidget(self.min_mean_box)
        pair.addSpacing(16)
        pair.addWidget(label("Worst 1%"))
        pair.addWidget(self.min_p1_box)
        pair.addStretch(1)
        grid.addLayout(pair, 6, 1, 1, 2)
        self.minimum_note = QLabel("Below the minimum, nothing is kept and your original stays. Off by default, so "
                                   "every result that is smaller and matches is kept, with a warning if needed.")
        self.minimum_note.setObjectName("hint")
        self.minimum_note.setWordWrap(True)
        self.minimum_note.setStyleSheet(plain)
        grid.addWidget(self.minimum_note, 7, 1, 1, 2)
        return card

    def _show_settings_values(self):
        s = self.settings
        for box, value in ((self.hardware_box, s.hardware), (self.codec_box, s.codec), (self.resolution_box, s.max_resolution)):
            box.blockSignals(True)
            box.setCurrentIndex(box.findData(value))
            box.blockSignals(False)
        self._syncing = True
        self.details_box.setChecked(s.show_details)
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
                                              self.minimum_box.isChecked(), self.min_mean_box.value(), self.min_p1_box.value())
        app_settings.save(self.db_path, self.settings)
        if old != key(self.settings):
            self.estimate = None        # the measured saving no longer applies
            self._reset_estimate_view()
        self._apply_settings_view()

    def _reset_settings(self):
        self.settings = app_settings.Settings()
        self._show_settings_values()
        self._settings_changed()

    def _card_works(self):
        return encode.encoder_available("av1_nvenc" if self.settings.codec == "av1" else "nvenc")

    def _using_text(self):
        s = self.settings
        codec = config.CODEC_NAMES[s.codec]
        name = "graphics card" if encode.resolve_encoder(s.hardware, s.codec) in ("nvenc", "av1_nvenc") else "processor"
        text = f"In use: your {name}, making {codec} video."
        if not self._card_works():
            found = encode.gpu_name()
            text += (f" {found} was found, but it can't make {codec} video, so the processor is used." if found
                     else " No compatible graphics card was found (only NVIDIA is supported), so the processor is used.")
        return text

    def _show_card(self):
        """Names the card, greys it out if it can't do this format, and picks what will really be used."""
        ok, found = self._card_works(), encode.gpu_name()
        if ok:
            text = f"Graphics card (fast, recommended) ({found or 'NVIDIA card'} detected)"
        elif found:
            text = f"Graphics card ({found} can't make this format)"
        else:
            text = "Graphics card (no compatible graphics card detected)"
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
        self.est_target_note.setText(f"The target: VMAF average at least {policy.warn_mean:g}, worst 1% of frames at least "
                                     f"{policy.warn_p1:g}. Every full file is measured again after conversion.")
        self.codec_note.setText("AV1 files are usually smaller, but they play on fewer devices. "
                                "Check that your TV or phone can play one first.")
        self.codec_note.setVisible(s.codec == "av1")
        self.resolution_note.setText("This permanently lowers the detail in the conversions, and videos are never "
                                     "enlarged. They are checked against a smaller copy of the original and labelled "
                                     "Resized. Keep the originals if you might want the full detail later.")
        self.resolution_note.setVisible(s.max_resolution != "original")
        for t, title in ((self.conv_table, 8), (self.review, 9)):
            t.setColumnHidden(title, not s.show_details)
        size = "" if s.max_resolution == "original" else f", at most {self.resolution_box.currentText()}"
        self.est_using.setText(f"{config.CODEC_NAMES[s.codec]}{size}. Change this in Settings.")
        self.conv_hint.show()
        shrunk = "" if s.max_resolution == "original" else f" ({config.output_suffix(s.codec, s.max_resolution)} if it was shrunk)"
        self.conv_hint.setText(f"Each conversion is saved beside its original with {config.CODEC_SUFFIX[s.codec]}{shrunk} added to "
                               "the name. Originals are only read. You can pause at any time, and if the PC crashes, "
                               "just reopen this app.")

    def _refresh_settings_page(self):
        for w in (self.hardware_box, self.codec_box, self.resolution_box, self.settings_reset, self.advanced_box):
            w.setEnabled(not self.busy)
        self._apply_settings_view()

    # --- About ------------------------------------------------------------
    def about_text(self):
        return self.about_browser.toPlainText()

    def _about_link(self, url):
        """Every link leaves the app: the website for the web ones, Explorer for the folder."""
        if url.isLocalFile():
            Path(url.toLocalFile()).mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(url)

    def _page_about(self):
        p, v = self._page(f"About {config.APP_NAME}", "")
        folder = reports.reports_dir(self.db_path)
        folder_url = QUrl.fromLocalFile(str(folder)).toString()
        site = config.DOCS_URL.replace("https://", "").rstrip("/")
        repo = config.PROJECT_URL.replace("https://", "")
        explain = "".join(f"<p>{html.escape(t, quote=False)}</p>" for t in config.QUALITY_EXPLANATION.split("\n\n"))
        self.about_browser = QTextBrowser()
        self.about_browser.setOpenLinks(False)
        self.about_browser.anchorClicked.connect(self._about_link)
        self.about_browser.setHtml(
            f"<p><b>{config.APP_NAME} {config.VERSION}</b></p>"
            f"<p>{config.APP_NAME} shrinks H.264 videos to H.265 or AV1 to free up disk space. It measures every conversion "
            "against its original with VMAF and warns you about any below the quality target. Your originals are "
            "only read during conversion, and nothing is sent anywhere.</p>"
            f"<p><b>Documentation:</b> <a href='{config.DOCS_URL}'>{site}</a><br>"
            f"<b>Project:</b> <a href='{config.PROJECT_URL}'>{repo}</a></p>"
            f"<p><b>Reports:</b> each batch leaves a CSV report in "
            f"<a href='{folder_url}'>{html.escape(str(folder))}</a>. They're only for your information. Once a batch "
            "is finished and you exit or click Start Over, the app forgets those files.</p>"
            "<p><b>Licence:</b> GPL-3.0. It comes with no warranty, so keep a backup of footage you can't replace.</p>"
            "<p><b>Built with:</b> FFmpeg, x265, SVT-AV1, VMAF, mpv and Qt. Their licences and source code links are in "
            "THIRD_PARTY_NOTICES.md in the install folder and on the project page.</p>"
            f"<h3>What does \"no quality loss\" mean?</h3>{explain}")
        v.addWidget(self.about_browser, 1)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(self.stage))
        row.addWidget(back)
        row.addStretch(1)
        v.addLayout(row)
        return p

    def closeEvent(self, ev):
        if self.busy and self.converter:
            ans = QMessageBox.question(self, "Stop converting?",
                                       "The batch is still running. If you close now, the current file is restarted "
                                       "next time and finished files are kept. Close anyway?")
            if ans != QMessageBox.Yes:
                ev.ignore()
                return
            self.converter.stop()
        elif not self.busy:
            self._forget_if_finished()
        super().closeEvent(ev)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    # Windows groups a Python-built app under its own taskbar entry only with an ID of its own.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("ClipShrink.App")
    app.setWindowIcon(QIcon(tools.icon_path()))
    apply_theme(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
