"""Reports kept for every batch, lifetime statistics, and exports.
A report is a plain CSV file in the "reports" folder. Statistics come from the
app's own records, so deleting a report never changes them."""
import csv, datetime, html, os, shutil
from dataclasses import dataclass
from pathlib import Path
from . import config, db

COLUMNS = ["Date", "File", "Folder", "Result", "Reason", "Before (bytes)", "After (bytes)", "Saved %",
           "VMAF average", "VMAF worst 1%", "Encoder", "Quality setting", "Conversion"]
INT_COLUMNS = {"Before (bytes)", "After (bytes)"}
FLOAT_COLUMNS = {"Saved %", "VMAF average", "VMAF worst 1%", "Quality setting"}
CONVERTED = ("verified", "below_bar", "original_deleted")


def reports_dir(db_path):
    return Path(db_path).parent / "reports"


def _safe(text):
    """Stops a file name acting as a formula when the report opens in a spreadsheet."""
    text = str(text or "")
    return "'" + text if text[:1] in ("=", "+", "-", "@") else text


def _row(r):
    converted = r.status in CONVERTED and r.output_size
    return {
        "Date": datetime.datetime.fromtimestamp(r.updated or 0).strftime("%Y-%m-%d %H:%M:%S"),
        "File": _safe(Path(r.source).name),
        "Folder": _safe(Path(r.source).parent),
        "Result": config.STATUS_TEXT.get(r.status, r.status),
        "Reason": _safe(r.reason),
        "Before (bytes)": r.source_size,
        "After (bytes)": r.output_size if converted else "",
        "Saved %": round((1 - r.output_size / r.source_size) * 100, 1) if converted and r.source_size else "",
        "VMAF average": round(r.vmaf_mean, 2) if r.vmaf_mean is not None else "",
        "VMAF worst 1%": round(r.vmaf_p1, 2) if r.vmaf_p1 is not None else "",
        "Encoder": r.encoder,
        "Quality setting": r.quality if r.quality is not None else "",
        "Conversion": _safe(r.output) if converted else "",
    }


def write_batch_report(folder, records, path=None):
    """Writes or rewrites one batch's report. Rewriting after each file means a
    crash keeps the report of everything already finished."""
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    if path is None:
        stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        path, n = folder / f"report_{stamp}.csv", 2
        while path.exists():
            path, n = folder / f"report_{stamp}_{n}.csv", n + 1
    tmp = Path(str(path) + ".tmp")
    with open(tmp, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, COLUMNS)
        w.writeheader()
        w.writerows(_row(r) for r in records)
    os.replace(tmp, path)
    return Path(path)


def read_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@dataclass
class ReportInfo:
    path: Path
    when: datetime.datetime
    files: int = 0
    before: int = 0
    after: int = 0
    lowest_vmaf: float = None
    below_bar: int = 0
    not_converted: int = 0
    damaged: bool = False

    @property
    def saved(self):
        return max(0, self.before - self.after)

    @property
    def saved_percent(self):
        return self.saved / self.before * 100 if self.before else 0.0


def _num(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


def _summarise(path):
    info = ReportInfo(Path(path), datetime.datetime.fromtimestamp(os.path.getmtime(path)))
    try:
        rows = read_rows(path)
        for r in rows:
            after, before = _num(r["After (bytes)"]), _num(r["Before (bytes)"])
            mean, p1 = _num(r["VMAF average"]), _num(r["VMAF worst 1%"])
            info.files += 1
            if after is None:
                info.not_converted += 1
            else:
                info.before += int(before or 0)
                info.after += int(after)
            if mean is not None:
                info.lowest_vmaf = mean if info.lowest_vmaf is None else min(info.lowest_vmaf, mean)
            if after is not None and not config.is_recommended(mean, p1):
                info.below_bar += 1
    except (OSError, UnicodeDecodeError, KeyError, csv.Error):
        info.damaged = True
    return info


def list_reports(folder):
    folder = Path(folder)
    if not folder.exists():
        return []
    return sorted((_summarise(p) for p in folder.glob("*.csv")), key=lambda r: r.when, reverse=True)


def _free_path(dest, stem, suffix):
    path, n = dest / f"{stem}{suffix}", 2
    while path.exists():
        path, n = dest / f"{stem}_{n}{suffix}", n + 1
    return path


def _export_xlsx(src, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    from openpyxl.utils import get_column_letter
    book = Workbook()
    sheet = book.active
    sheet.title = "Report"
    sheet.append(COLUMNS)
    for row in read_rows(src):
        out = []
        for c in COLUMNS:
            v = row.get(c, "")
            if c in INT_COLUMNS and v != "":
                v = int(float(v))
            elif c in FLOAT_COLUMNS and v != "":
                v = float(v)
            out.append(v if v != "" else None)
        sheet.append(out)
    sheet.freeze_panes = "A2"
    sheet.auto_filter.ref = sheet.dimensions
    for i, c in enumerate(COLUMNS, 1):
        sheet.column_dimensions[get_column_letter(i)].width = {"File": 26, "Folder": 44, "Reason": 44, "Date": 20,
                                                               "Conversion": 44}.get(c, 14)
    for c in sheet[1]:
        c.font = Font(bold=True)
    book.save(path)


def _export_pdf(src, path):
    from PySide6.QtGui import QPageLayout, QPageSize, QPdfWriter, QTextDocument
    shown = ["File", "Folder", "Result", "Before (bytes)", "After (bytes)", "Saved %", "VMAF average", "VMAF worst 1%"]
    rows = read_rows(src)
    head = "".join(f"<th>{html.escape(c)}</th>" for c in shown)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(r.get(c, '')))}</td>" for c in shown) + "</tr>" for r in rows)
    info = _summarise(src)
    doc = QTextDocument()
    doc.setHtml(f"<h2>{config.APP_NAME} report</h2><p>{info.when:%Y-%m-%d %H:%M}: {info.files} files. "
                f"Saved {info.saved:,} of {info.before:,} bytes ({info.saved_percent:.0f}%).</p>"
                f"<table border='1' cellspacing='0' cellpadding='3' width='100%'>"
                f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>")
    writer = QPdfWriter(str(path))
    writer.setPageSize(QPageSize(QPageSize.A4))
    writer.setPageOrientation(QPageLayout.Landscape)
    writer.setTitle(f"{config.APP_NAME} report")
    doc.print_(writer)


def export_reports(paths, fmt, dest):
    """Copies each report into `dest` as csv, xlsx or pdf. Never overwrites."""
    dest = Path(dest)
    dest.mkdir(parents=True, exist_ok=True)
    made = []
    for src in paths:
        src = Path(src)
        out = _free_path(dest, src.stem, f".{fmt}")
        if fmt == "csv":
            shutil.copyfile(src, out)
        elif fmt == "xlsx":
            _export_xlsx(src, out)
        elif fmt == "pdf":
            _export_pdf(src, out)
        else:
            raise ValueError(f"unknown format {fmt}")
        made.append(out)
    return made


def delete_reports(paths):
    """To the Recycle Bin, so a mistake can be undone."""
    from .trash import _send_to_recycle_bin
    return [Path(p) for p in paths if _send_to_recycle_bin(p)]


@dataclass
class Statistics:
    files_converted: int = 0
    files_below_bar: int = 0
    files_kept: int = 0
    bytes_before: int = 0
    bytes_after: int = 0
    average_reduction_percent: float = 0.0
    average_vmaf: float = 0.0
    originals_removed: int = 0
    bytes_freed: int = 0

    @property
    def bytes_saved(self):
        return self.bytes_before - self.bytes_after


def statistics(db_path):
    s = Statistics()
    cuts, scores = [], []
    for r in db.read_records(db_path):
        if r.status in ("kept_original", "failed"):
            s.files_kept += 1
        if r.status not in CONVERTED or not r.output_size or not r.source_size:
            continue
        s.files_converted += 1
        s.bytes_before += r.source_size
        s.bytes_after += r.output_size
        cuts.append((1 - r.output_size / r.source_size) * 100)
        if r.vmaf_mean is not None:
            scores.append(r.vmaf_mean)
        if not config.is_recommended(r.vmaf_mean, r.vmaf_p1):
            s.files_below_bar += 1
        if r.status == "original_deleted":
            s.originals_removed += 1
            s.bytes_freed += r.source_size - r.output_size
    s.average_reduction_percent = sum(cuts) / len(cuts) if cuts else 0.0
    s.average_vmaf = sum(scores) / len(scores) if scores else 0.0
    return s
