"""A plain CSV report for every batch, kept in the "reports" folder for the user's
information. The app writes them and never reads them back."""
import csv, datetime, os
from pathlib import Path
from . import config

COLUMNS = ["Date", "File", "Folder", "Result", "Reason", "Before (bytes)", "After (bytes)", "Saved %",
           "VMAF average", "VMAF worst 1%", "Encoder", "Quality setting", "Conversion", "Codec", "Output resolution",
           "Output bitrate (Mbit/s)", "Target average", "Target worst 1%"]
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
        "Result": config.status_text(r),
        "Reason": _safe(r.reason),
        "Before (bytes)": r.source_size,
        "After (bytes)": r.output_size if converted else "",
        "Saved %": round((1 - r.output_size / r.source_size) * 100, 1) if converted and r.source_size else "",
        "VMAF average": round(r.vmaf_mean, 2) if r.vmaf_mean is not None else "",
        "VMAF worst 1%": round(r.vmaf_p1, 2) if r.vmaf_p1 is not None else "",
        "Encoder": r.encoder,
        "Quality setting": r.quality if r.quality is not None else "",
        "Conversion": _safe(r.output) if converted else "",
        "Codec": config.CODEC_NAMES.get(r.codec, "") if converted else "",
        "Output resolution": f"{r.output_width}x{r.output_height}" if converted and r.output_width else "",
        "Output bitrate (Mbit/s)": round(r.output_bitrate_mbit, 2) if converted and r.output_bitrate_mbit else "",
        "Target average": r.warn_mean if converted else "",
        "Target worst 1%": r.warn_p1 if converted else "",
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
