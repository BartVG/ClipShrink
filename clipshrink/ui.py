"""The desktop interface: four stages, left to right, one obvious button each."""
import csv, os, sys, threading, time
from pathlib import Path
from PySide6.QtCore import QObject, QPointF, QRectF, Qt, QTimer, Signal
from PySide6.QtGui import QColor, QPainter, QPalette, QPen
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox, QDialog, QDialogButtonBox,
                               QFileDialog, QFrame, QHBoxLayout, QHeaderView, QLabel, QMainWindow, QMessageBox,
                               QProgressBar, QPushButton, QSlider, QStackedWidget, QStyle, QStyledItemDelegate, QStyleOptionViewItem, QTableWidget, QTableWidgetItem,
                               QTextBrowser, QVBoxLayout, QWidget)
from . import config, db, encode, trash
from .encode import Stopped
from .engine import Converter
from .estimate import estimate_savings
from .player import PlayerError, SideBySidePlayer
from .scan import scan_folder

STYLE = """
QWidget { font-family: 'Segoe UI'; font-size: 10.5pt; color: #1f2933; }
QMainWindow, #page { background: #f6f7f9; }
#rail { background: #1f2933; }
#stepOn  { color: white; font-weight: 600; background: #3a4a5a; border-radius: 6px; padding: 10px; }
#stepOff { color: #9fb0c0; padding: 10px; }
#stepDone { color: #8fd4a8; padding: 10px; }
#title { font-size: 17pt; font-weight: 600; }
#hint  { color: #52606d; }
#big   { font-size: 22pt; font-weight: 600; color: #0b6e4f; }
#card  { background: white; border: 1px solid #dde2e7; border-radius: 8px; }
QPushButton { padding: 7px 14px; border: 1px solid #c4ccd4; border-radius: 6px; background: white; }
QPushButton:hover { background: #eef1f4; }
QPushButton:disabled { color: #a0a8b0; background: #f0f1f3; }
QPushButton#primary { background: #0b6e4f; color: white; border: none; font-weight: 600; padding: 9px 20px; }
QPushButton#primary:hover { background: #095c42; }
QPushButton#primary:disabled { background: #b6c9c2; color: white; }
QPushButton#danger { background: #b42318; color: white; border: none; font-weight: 600; padding: 9px 20px; }
QPushButton#danger:disabled { background: #e0bdb9; color: white; }
QTableWidget { background: white; border: 1px solid #dde2e7; gridline-color: #eef1f4; }
QHeaderView::section { background: #eef1f4; border: none; padding: 6px; font-weight: 600; }
QTableWidget { selection-background-color: #bfe3d4; selection-color: #1f2933; }
QTableWidget::item:selected { background: #bfe3d4; color: #1f2933; }
QTextBrowser { background: white; border: 1px solid #dde2e7; border-radius: 6px; }
QComboBox { background: white; padding: 5px; border: 1px solid #c4ccd4; border-radius: 6px; }
QProgressBar { border: 1px solid #c4ccd4; border-radius: 6px; text-align: center; background: white; height: 22px; }
QProgressBar::chunk { background: #2fa37c; border-radius: 5px; }
"""

STATUS_TEXT = {
    "pending": "Waiting",
    "encoding": "Working…",
    "verified": "Verified",
    "kept_original": "Original kept",
    "failed": "Failed, original kept",
    "original_deleted": "Original in Recycle Bin",
    "renamed": "Done, has the original's name",
}


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


def toggle_tick(t, row):
    it = t.item(row, 0)
    it.setCheckState(Qt.Unchecked if it.checkState() == Qt.Checked else Qt.Checked)


def table(headers, stretch=0):
    t = QTableWidget(0, len(headers))
    t.setHorizontalHeaderLabels(headers)
    t.verticalHeader().setVisible(False)
    t.setEditTriggers(QAbstractItemView.NoEditTriggers)
    t.setSelectionBehavior(QAbstractItemView.SelectRows)
    t.setSelectionMode(QAbstractItemView.SingleSelection)
    h = t.horizontalHeader()
    h.setSectionResizeMode(QHeaderView.ResizeToContents)
    h.setSectionResizeMode(stretch, QHeaderView.Stretch)
    if stretch == 1:    # tables whose first column holds tick boxes
        t.setItemDelegateForColumn(0, TickDelegate(t))
    return t


def cell(text, tip=None):
    it = QTableWidgetItem(str(text))
    if tip:
        it.setToolTip(tip)
    return it


class HelpDialog(QDialog):
    def __init__(self, parent, text):
        super().__init__(parent)
        self.setWindowTitle("What \"no quality loss\" means")
        self.resize(560, 420)
        v = QVBoxLayout(self)
        b = QTextBrowser()
        b.setPlainText(text)
        v.addWidget(b)
        k = QDialogButtonBox(QDialogButtonBox.Close)
        k.rejected.connect(self.reject)
        v.addWidget(k)


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
        self.resize(1280, 760)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 8)
        heads = QHBoxLayout()
        for text in ("Original (H.264)", "Conversion (H.265)"):
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
            self.timer.start()
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
        self.folder = None
        self.result = None
        self.estimate = None
        self.converter = None
        self.scope = []
        self.busy = False
        self.bridge = Bridge()
        self.bridge.call.connect(lambda fn: fn())
        self.setWindowTitle(f"{config.APP_NAME} {config.VERSION}: shrink GoPro videos, keep the quality")
        self.resize(1080, 720)
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
        for t in ("1  Find videos", "2  See the saving", "3  Convert", "4  Compare and clean up"):
            lab = QLabel(t)
            lab.setObjectName("stepOff")
            rv.addWidget(lab)
            self.steps.append(lab)
        rv.addStretch(1)
        why = QPushButton()
        why.setStyleSheet("QPushButton { color:#cfd8e0; background:transparent; border:1px solid #52606d; text-align:left; }"
                          "QPushButton:hover { background:#3a4a5a; }")
        why.setMinimumHeight(52)
        why.clicked.connect(lambda: HelpDialog(self, self.quality_explanation()).exec())
        rv.addWidget(why)
        why.setText("What does \"no quality\nloss\" mean?")
        lay.addWidget(rail)
        self.stack = QStackedWidget()
        lay.addWidget(self.stack, 1)
        self.setCentralWidget(root)
        self.stack.addWidget(self._page_scan())
        self.stack.addWidget(self._page_estimate())
        self.stack.addWidget(self._page_convert())
        self.stack.addWidget(self._page_review())
        self.go(0)
        QTimer.singleShot(200, self._offer_resume)

    # --- plain facts other code and the check rely on ---------------------
    def quality_explanation(self):
        return config.QUALITY_EXPLANATION

    def can_estimate(self):
        return bool(self.result and self.selected_files())

    def can_convert(self):
        return self.estimate is not None and not self.busy

    def delete_confirmation_text(self, count, bytes_total):
        return (f"{count} verified original{'s' if count != 1 else ''} ({human_size(bytes_total)}) will go to the "
                f"Windows Recycle Bin. Each one's conversion was measured and re-checked just now, and you can restore "
                f"them from the Recycle Bin.\n\nImportant: {trash.GOOGLE_DRIVE_WARNING}")

    # --- layout helpers ---------------------------------------------------
    def go(self, i):
        self.stack.setCurrentIndex(i)
        for n, lab in enumerate(self.steps):
            lab.setObjectName("stepOn" if n == i else ("stepDone" if n < i else "stepOff"))
            lab.style().unpolish(lab)
            lab.style().polish(lab)
        if i == 3:
            self.refresh_review()

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
        self.scan_table = table(["Convert", "File", "Size", "Picture", "Length", "State"], 1)
        self.scan_table.setColumnWidth(0, 60)
        self.scan_table.itemChanged.connect(self._selection_changed)
        self.scan_table.cellClicked.connect(self._scan_cell_clicked)
        v.addWidget(self.scan_table, 1)
        self.scan_note = QLabel("")
        self.scan_note.setWordWrap(True)
        v.addWidget(self.scan_note)
        row = QHBoxLayout()
        row.addStretch(1)
        self.to_estimate = QPushButton("Next: see the saving  →")
        self.to_estimate.setObjectName("primary")
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
        self.result = res
        self.scan_bar.hide()
        self.pick_btn.setEnabled(True)
        self.scan_table.blockSignals(True)
        self.scan_table.setRowCount(len(res.h264) + len(res.other))
        known = {r.source.lower(): r for r in db.read_records(self.db_path)}
        for i, f in enumerate(res.h264):
            box = QTableWidgetItem()
            box.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            rec = known.get(f.path.lower())
            ext = Path(f.path).suffix.lower()
            state = STATUS_TEXT.get(rec.status, "") if rec and rec.source_size == f.size else "Ready"
            done = rec is not None and rec.status == "verified" and rec.source_size == f.size
            box.setCheckState(Qt.Unchecked if done or ext == ".lrv" else Qt.Checked)
            self.scan_table.setItem(i, 0, box)
            rel = os.path.relpath(f.path, self.folder)
            self.scan_table.setItem(i, 1, cell(rel, f.path))
            self.scan_table.setItem(i, 2, cell(human_size(f.size)))
            self.scan_table.setItem(i, 3, cell(f"{f.width}×{f.height} {f.fps:.0f} fps"))
            self.scan_table.setItem(i, 4, cell(f"{int(f.duration) // 60}:{int(f.duration) % 60:02d}"))
            self.scan_table.setItem(i, 5, cell("GoPro low-res preview, off by default" if ext == ".lrv" else state))
        # Everything else in the folder stays visible, with no tick box. Rows
        # come after the H.264 ones, so selected_files() still lines up.
        ours = {r.output.lower() for r in known.values() if r.output}
        grey = QColor("#7b8794")
        for i, f in enumerate(res.other, len(res.h264)):
            name = "H.265" if f.codec == "hevc" else f.codec.upper()
            state = f"Already {name}, skipped" + (" (converted by this tool)" if f.path.lower() in ours else "")
            box = QTableWidgetItem("—")
            box.setFlags(Qt.ItemIsEnabled)
            box.setTextAlignment(Qt.AlignCenter)
            self.scan_table.setItem(i, 0, box)
            vals = [os.path.relpath(f.path, self.folder), human_size(f.size), f"{f.width}×{f.height} {f.fps:.0f} fps",
                    f"{int(f.duration) // 60}:{int(f.duration) % 60:02d}", state]
            for c, val in enumerate(vals, 1):
                it = cell(val, f.path)
                it.setForeground(grey)
                self.scan_table.setItem(i, c, it)
            box.setForeground(grey)
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
        if col == 0 and self.result and row < len(self.result.h264):
            toggle_tick(self.scan_table, row)

    def selected_files(self):
        if not self.result:
            return []
        out = []
        for i, f in enumerate(self.result.h264):
            it = self.scan_table.item(i, 0)
            if it and it.checkState() == Qt.Checked:
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
        lab = QLabel("Speed:")
        self.encoder_box = QComboBox()
        self.encoder_box.addItem("Automatic (recommended)", "auto")
        self.encoder_box.addItem("Graphics card: fast (NVIDIA only)", "nvenc")
        self.encoder_box.addItem("Processor: slow, works on any PC", "x265")
        self.encoder_box.currentIndexChanged.connect(lambda _: self._selection_changed())
        row.addWidget(lab)
        row.addWidget(self.encoder_box)
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
        self.est_table = table(["Sample from", "At", "Original", "H.265", "VMAF average", "VMAF worst 1%", "Clears the bar?"], 0)
        v.addWidget(self.est_table, 1)
        note = QLabel("The bar: VMAF average at least 95, worst 1% of frames at least 90. "
                      "Every full file is measured again after conversion.")
        note.setObjectName("hint")
        note.setWordWrap(True)
        v.addWidget(note)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(0))
        row.addWidget(back)
        row.addStretch(1)
        self.to_convert = QPushButton("Next: convert  →")
        self.to_convert.setObjectName("primary")
        self.to_convert.setEnabled(False)
        self.to_convert.clicked.connect(lambda: self.go(2))
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
        self.start_btn.setEnabled(False) if hasattr(self, "start_btn") else None

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
        encoder = self.encoder_box.currentData()

        def work():
            def tick(i, n, path):
                self.bridge.call.emit(lambda: (self.est_bar.setRange(0, n), self.est_bar.setValue(i)))
            try:
                est = estimate_savings(files, encoder=encoder, work_dir=self.work_dir / "estimate", on_progress=tick)
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
        speed = "graphics card" if est.encoder == "nvenc" else "processor"
        self.est_detail.setText(
            f"Likely between {human_size(est.low_saved_bytes)} and {human_size(est.high_saved_bytes)}, out of "
            f"{human_size(est.total_source_bytes)}. Measured on {est.files_sampled} file"
            f"{'s' if est.files_sampled != 1 else ''} using your {speed}. "
            f"Converting everything should take {human_time(est.seconds_estimate)}.")
        self.est_table.setRowCount(len(est.samples))
        for i, s in enumerate(est.samples):
            ok = s.vmaf_mean >= config.VMAF_MEAN_MIN and s.vmaf_p1 >= config.VMAF_P1_MIN
            vals = [Path(s.path).name, f"{int(s.at_seconds) // 60}:{int(s.at_seconds) % 60:02d}",
                    human_size(s.source_bytes), human_size(s.encoded_bytes), f"{s.vmaf_mean:.1f}", f"{s.vmaf_p1:.1f}",
                    "Yes" if ok else "No"]
            for c, val in enumerate(vals):
                self.est_table.setItem(i, c, cell(val))
        self.to_convert.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.conv_info.setText(f"{len(self.selected_files())} videos, {human_size(est.total_source_bytes)}. "
                               f"Expected time: {human_time(est.seconds_estimate)}. Your computer will not go to sleep "
                               f"while this runs.")

    # --- stage 3 ----------------------------------------------------------
    def _page_convert(self):
        p, v = self._page("Convert",
                          "Each conversion is saved beside its original with _H265 added to the name. Originals are "
                          "only read. You can pause at any time, and if the PC crashes, just reopen this app.")
        self.conv_info = QLabel("")
        self.conv_info.setObjectName("hint")
        self.conv_info.setWordWrap(True)
        v.addWidget(self.conv_info)
        row = QHBoxLayout()
        self.start_btn = QPushButton("Start converting")
        self.start_btn.setObjectName("primary")
        self.start_btn.setEnabled(False)
        self.start_btn.clicked.connect(self.start_batch)
        self.pause_btn = QPushButton("Pause")
        self.pause_btn.setEnabled(False)
        self.pause_btn.clicked.connect(self.toggle_pause)
        row.addWidget(self.start_btn)
        row.addWidget(self.pause_btn)
        row.addStretch(1)
        self.overall_lab = QLabel("")
        row.addWidget(self.overall_lab)
        v.addLayout(row)
        self.overall_bar = QProgressBar()
        self.overall_bar.setRange(0, 1000)
        self.overall_bar.setFormat("All files: %p%")
        v.addWidget(self.overall_bar)
        self.file_bar = QProgressBar()
        self.file_bar.setRange(0, 1000)
        self.file_bar.setFormat("This file")
        v.addWidget(self.file_bar)
        self.conv_table = table(["File", "State", "Before", "After", "VMAF average", "Worst 1%"], 0)
        v.addWidget(self.conv_table, 1)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(1))
        self.conv_back = back
        row.addWidget(back)
        row.addStretch(1)
        self.to_review = QPushButton("Next: compare and clean up  →")
        self.to_review.setObjectName("primary")
        self.to_review.clicked.connect(lambda: self.go(3))
        self.to_review.setEnabled(False)
        row.addWidget(self.to_review)
        v.addLayout(row)
        return p

    def start_batch(self, resume_paths=None):
        paths = resume_paths or [f.path for f in self.selected_files()]
        encoder = self.estimate.encoder if self.estimate else "auto"
        self.busy = True
        self.start_btn.setEnabled(False)
        self.pause_btn.setEnabled(True)
        self.pause_btn.setText("Pause")
        self.conv_back.setEnabled(False)
        self.to_review.setEnabled(False)
        self.overall_bar.setValue(0)
        self.file_bar.setValue(0)
        self.conv_rows = {}
        self.conv_table.setRowCount(len(paths))
        for i, pth in enumerate(paths):
            self.conv_rows[pth] = i
            self.conv_table.setItem(i, 0, cell(Path(pth).name, pth))
            self.conv_table.setItem(i, 1, cell("Waiting"))
        self.converter = Converter(self.db_path, self.work_dir, encoder=encoder,
                                   on_event=lambda ev: self.bridge.call.emit(lambda: self._on_event(ev)))
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

    def _show_row(self, rec):
        i = self.conv_rows.get(rec.source)
        if i is None:
            return
        self.conv_table.setItem(i, 1, cell(STATUS_TEXT.get(rec.status, rec.status), rec.reason))
        self.conv_table.setItem(i, 2, cell(human_size(rec.source_size)))
        if rec.status == "verified":
            self.conv_table.setItem(i, 3, cell(human_size(rec.output_size)))
        if rec.vmaf_mean is not None:
            self.conv_table.setItem(i, 4, cell(f"{rec.vmaf_mean:.1f}"))
            self.conv_table.setItem(i, 5, cell(f"{rec.vmaf_p1:.1f}"))

    def _on_event(self, ev):
        t = ev["type"]
        if t == "progress":
            self.overall_bar.setValue(int(ev["overall"] * 1000))
            self.file_bar.setValue(int(ev["file_fraction"] * 1000))
            stage = {"search": "Finding the right quality", "encode": "Encoding", "verify": "Measuring every frame",
                     "done": "Done"}[ev["stage"]]
            self.file_bar.setFormat(f"{Path(ev['path']).name}: {stage}")
            eta = f", {human_time(ev['eta_seconds'])} left" if ev.get("eta_seconds") else ""
            self.overall_lab.setText(f"File {ev['index'] + 1} of {ev['count']}{eta}")
        elif t == "file_start":
            i = self.conv_rows.get(ev["path"])
            if i is not None:
                self.conv_table.setItem(i, 1, cell("Working…"))
        elif t == "file_done":
            self._show_row(ev["record"])
        elif t == "paused":
            self.pause_btn.setText("Resume")
            self.overall_lab.setText("Paused")
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
        self.file_bar.setFormat("Finished")
        self.file_bar.setValue(1000)
        kept = s["kept_original"] + s["failed"]
        self.overall_lab.setText(f"Finished: {s['verified']} verified"
                                 + (f", {kept} kept as original (see next page)" if kept else ""))

    def _batch_crashed(self, msg):
        self.busy = False
        self.pause_btn.setEnabled(False)
        self.conv_back.setEnabled(True)
        self.to_review.setEnabled(True)
        QMessageBox.warning(self, "The batch stopped", f"{msg}\n\nFiles already verified are safe. Reopen the app to continue.")

    def _offer_resume(self):
        left = [r for r in db.read_records(self.db_path) if r.status in ("pending", "encoding") and os.path.exists(r.source)]
        if not left:
            return
        ans = QMessageBox.question(self, "Continue where you left off?",
                                   f"{len(left)} video{'s' if len(left) != 1 else ''} from your last batch "
                                   f"{'are' if len(left) != 1 else 'is'} not finished. Files already verified will "
                                   "not be converted again. Continue now?")
        if ans == QMessageBox.Yes:
            self.go(2)
            self.start_batch([r.source for r in left])

    # --- stage 4 ----------------------------------------------------------
    def _page_review(self):
        p, v = self._page("Compare and clean up",
                          "Play any original beside its conversion, in sync. When you are happy, you can send verified "
                          "originals to the Recycle Bin. This step is optional.")
        self.savings_lab = QLabel("")
        self.savings_lab.setObjectName("big")
        v.addWidget(self.savings_lab)
        self.review = table(["Delete?", "Original", "Before", "After", "Saved", "VMAF average", "Worst 1%", "Result"], 1)
        self.review.cellClicked.connect(self._cell_clicked)
        v.addWidget(self.review, 3)
        row = QHBoxLayout()
        self.play_btn = QPushButton("▶  Play selected side by side")
        self.play_btn.setObjectName("primary")
        self.play_btn.clicked.connect(self.play_selected)
        row.addWidget(self.play_btn)
        self.report_btn = QPushButton("Save report…")
        self.report_btn.clicked.connect(self.save_report)
        row.addWidget(self.report_btn)
        row.addStretch(1)
        self.rename_btn = QPushButton(f"Remove {config.OUTPUT_SUFFIX} from names")
        self.rename_btn.setEnabled(False)
        self.rename_btn.clicked.connect(self.rename_done_files)
        row.addWidget(self.rename_btn)
        self.delete_btn = QPushButton("Send ticked originals to Recycle Bin…")
        self.delete_btn.setObjectName("danger")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_ticked)
        row.addWidget(self.delete_btn)
        v.addLayout(row)
        self.problem_title = QLabel("Kept as original")
        self.problem_title.setStyleSheet("font-weight:600;")
        v.addWidget(self.problem_title)
        self.problems = QTextBrowser()
        self.problems.setMaximumHeight(120)
        v.addWidget(self.problems)
        warn = QLabel(trash.GOOGLE_DRIVE_WARNING)
        warn.setWordWrap(True)
        warn.setStyleSheet("background:#fff4e5; border:1px solid #f2c078; border-radius:6px; padding:8px;")
        v.addWidget(warn)
        row = QHBoxLayout()
        back = QPushButton("←  Back")
        back.clicked.connect(lambda: self.go(2))
        row.addWidget(back)
        row.addStretch(1)
        v.addLayout(row)
        return p

    def _records_for_view(self):
        recs = db.read_records(self.db_path)
        if self.folder:
            pref = self.folder.lower().rstrip("\\") + "\\"
            mine = [r for r in recs if r.source.lower().startswith(pref)]
            if mine:
                recs = mine
        return sorted(recs, key=lambda r: r.source.lower())

    def refresh_review(self):
        recs = self._records_for_view()
        allow = {r.source for r in trash.deletable(self.db_path)}
        shown = [r for r in recs if r.status in ("verified", "original_deleted", "kept_original", "failed")]
        self.review_recs = shown
        self.review.setRowCount(len(shown))
        saved = 0
        for i, r in enumerate(shown):
            box = QTableWidgetItem()
            if r.source in allow:
                # Not "user checkable": _cell_clicked toggles it, so the whole cell is the target.
                box.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                box.setCheckState(Qt.Unchecked)
            else:
                box.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                box.setText("—")
            self.review.setItem(i, 0, box)
            self.review.setItem(i, 1, cell(Path(r.source).name, r.source))
            self.review.setItem(i, 2, cell(human_size(r.source_size)))
            if r.status in ("verified", "original_deleted"):
                self.review.setItem(i, 3, cell(human_size(r.output_size)))
                self.review.setItem(i, 4, cell(f"{(1 - r.output_size / r.source_size) * 100:.0f}%"))
                saved += r.source_size - r.output_size
            if r.vmaf_mean is not None:
                self.review.setItem(i, 5, cell(f"{r.vmaf_mean:.1f}"))
                self.review.setItem(i, 6, cell(f"{r.vmaf_p1:.1f}"))
            renamed = r.status == "original_deleted" and Path(r.output).stem.lower() == Path(r.source).stem.lower()
            self.review.setItem(i, 7, cell(STATUS_TEXT["renamed" if renamed else r.status], r.reason or r.output))
        self.savings_lab.setText(f"{human_size(saved)} can be saved once originals are removed" if saved else "")
        bad = [r for r in shown if r.status in ("kept_original", "failed")]
        self.problem_title.setText(f"Kept as original ({len(bad)})" if bad else "Kept as original: none")
        self.problems.setPlainText("\n\n".join(f"{Path(r.source).name}\n  {r.reason}" for r in bad)
                                   or "Every conversion passed.")
        self.review_allow = allow
        self._tick_changed()
        n = len(trash.renamable(self.db_path))
        self.rename_btn.setEnabled(bool(n))
        self.rename_btn.setText(f"Remove {config.OUTPUT_SUFFIX} from {n} name{'s' if n != 1 else ''}…"
                                if n else f"Remove {config.OUTPUT_SUFFIX} from names")
        self.rename_btn.setToolTip("Available after an original has been sent to the Recycle Bin.")
        if shown:
            first = next((i for i, r in enumerate(shown) if r.status == "verified"), 0)
            self.review.selectRow(first)

    def _ticked(self):
        out = []
        for i, r in enumerate(getattr(self, "review_recs", [])):
            it = self.review.item(i, 0)
            if it and r.source in getattr(self, "review_allow", ()) and it.checkState() == Qt.Checked:
                out.append(r)
        return out

    def _cell_clicked(self, row, col):
        recs = getattr(self, "review_recs", [])
        if col != 0 or row >= len(recs) or recs[row].source not in getattr(self, "review_allow", ()):
            return
        toggle_tick(self.review, row)
        self._tick_changed()

    def _tick_changed(self, *_):
        n = self._ticked()
        self.delete_btn.setEnabled(bool(n))
        self.delete_btn.setText(f"Send {len(n)} ticked original{'s' if len(n) != 1 else ''} to Recycle Bin…"
                                if n else "Tick originals above to delete them")

    def play_selected(self):
        i = self.review.currentRow()
        recs = getattr(self, "review_recs", [])
        if i < 0 or i >= len(recs):
            QMessageBox.information(self, "Pick a video", "Click a row in the list first.")
            return
        r = recs[i]
        if r.status != "verified" or not os.path.exists(r.source) or not os.path.exists(r.output):
            QMessageBox.information(self, "Cannot compare",
                                    "This row needs both an original and a verified conversion on disk.\n" + (r.reason or ""))
            return
        w = PlayerWindow(self, r)
        w.exec()

    def delete_ticked(self):
        recs = self._ticked()
        if not recs:
            return
        d = DeleteDialog(self, self.delete_confirmation_text(len(recs), sum(r.source_size for r in recs)))
        if d.exec() != QDialog.Accepted or not d.tick.isChecked():
            return
        self.delete_btn.setEnabled(False)
        self.delete_btn.setText("Re-checking conversions…")

        def work():
            res = trash.delete_originals(self.db_path, [r.source for r in recs], confirmed=True)
            self.bridge.call.emit(lambda: self._delete_done(res))

        threading.Thread(target=work, daemon=True).start()

    def _delete_done(self, res):
        self.refresh_review()
        text = f"{len(res.deleted)} original{'s' if len(res.deleted) != 1 else ''} moved to the Recycle Bin."
        if res.refused:
            text += "\n\nLeft in place:\n" + "\n".join(f"{Path(p).name}: {why}" for p, why in res.refused)
        text += f"\n\n{trash.GOOGLE_DRIVE_WARNING}"
        QMessageBox.information(self, "Done", text)

    def rename_done_files(self):
        recs = trash.renamable(self.db_path)
        if not recs:
            return
        ans = QMessageBox.question(self, f"Remove {config.OUTPUT_SUFFIX} from names?",
                                   f"{len(recs)} conversion{'s' if len(recs) != 1 else ''} whose original is in the "
                                   f"Recycle Bin will take the original's name, for example "
                                   f"{Path(recs[0].source).name}.\n\nOnly the name changes. If you later restore an "
                                   "original from the Recycle Bin, Windows will ask what to do about the same name.")
        if ans != QMessageBox.Yes:
            return
        res = trash.remove_suffix(self.db_path, [r.source for r in recs], confirmed=True)
        self.refresh_review()
        text = f"{len(res.renamed)} file{'s' if len(res.renamed) != 1 else ''} renamed."
        if res.refused:
            text += "\n\nLeft as they are:\n" + "\n".join(f"{Path(p).name}: {why}" for p, why in res.refused)
        QMessageBox.information(self, "Done", text)

    def save_report(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save report", f"{config.APP_NAME} report.csv", "CSV (*.csv)")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["Original", "Result", "Reason", "Before (bytes)", "After (bytes)", "VMAF average", "VMAF worst 1%",
                        "Conversion"])
            for r in self._records_for_view():
                w.writerow([r.source, STATUS_TEXT.get(r.status, r.status), r.reason, r.source_size, r.output_size or "",
                            r.vmaf_mean or "", r.vmaf_p1 or "", r.output])

    def closeEvent(self, ev):
        if self.busy and self.converter:
            ans = QMessageBox.question(self, "Stop converting?",
                                       "The batch is still running. If you close now, the current file is restarted "
                                       "next time and finished files are kept. Close anyway?")
            if ans != QMessageBox.Yes:
                ev.ignore()
                return
            self.converter.stop()
        super().closeEvent(ev)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(config.APP_NAME)
    apply_theme(app)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
