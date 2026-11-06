"""Reports kept automatically, lifetime statistics, exports and deletion."""
import csv, os, time
from pathlib import Path
import pytest
from conftest import copy_preserving
from clipshrink import db as database


def rows_of(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def saved_record(db, name, status="verified", before=1000, after=400, mean=97.0, p1=92.0, folder="C:/Videos/Trip"):
    database.save(db, database.Record(source=f"{folder}/{name}", status=status, source_size=before, output_size=after,
                                      vmaf_mean=mean, vmaf_p1=p1, output=f"{folder}/{name}_(h265).mp4"))


def write_report(workspace, names=("a.mp4",)):
    from clipshrink.reports import write_batch_report, reports_dir
    db = workspace / "work" / "s.db"
    for n in names:
        saved_record(db, n)
    return write_batch_report(reports_dir(db), [database.get(db, f"C:/Videos/Trip/{n}") for n in names])


def test_batch_writes_a_report_automatically(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.reports import list_reports, reports_dir
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    db = workspace / "work" / "s.db"
    c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    found = list_reports(reports_dir(db))
    assert len(found) == 1 and found[0].files == 1
    row = rows_of(found[0].path)[0]
    assert row["File"] == "a.mp4" and Path(row["Folder"]) == src.parent
    assert float(row["VMAF average"]) >= 95 and row["Result"] == "Verified"
    assert int(row["After (bytes)"]) == Path(c.record(src).output).stat().st_size


def test_each_batch_gets_its_own_report_and_old_ones_stay(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.reports import list_reports, reports_dir
    db = workspace / "work" / "s.db"
    for n in ("a.mp4", "b.mp4"):
        src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / n)
        c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
        c.add_files([src])
        c.run()
    found = list_reports(reports_dir(db))
    assert len(found) == 2 and {rows_of(r.path)[0]["File"] for r in found} == {"a.mp4", "b.mp4"}


def test_batch_with_nothing_to_do_writes_no_report(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.reports import list_reports, reports_dir
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    db = workspace / "work" / "s.db"
    for _ in range(2):
        c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
        c.add_files([src])
        c.run()
    assert len(list_reports(reports_dir(db))) == 1


def test_statistics_cover_all_use_of_the_app(workspace):
    from clipshrink.reports import statistics
    db = workspace / "s.db"
    saved_record(db, "a", before=1000, after=500, mean=96, p1=91)            # 50%
    saved_record(db, "b", before=3000, after=2250, mean=98, p1=95)           # 25%
    saved_record(db, "c", status="below_bar", before=1000, after=400, mean=93, p1=88)   # 60%
    saved_record(db, "d", status="original_deleted", before=2000, after=1000, mean=97, p1=92)  # 50%
    saved_record(db, "e", status="kept_original", before=500, after=0, mean=None, p1=None)
    saved_record(db, "f", status="failed", before=500, after=0, mean=None, p1=None)
    saved_record(db, "g", status="pending", before=500, after=0, mean=None, p1=None)
    s = statistics(db)
    assert s.files_converted == 4 and s.files_below_bar == 1 and s.files_kept == 2
    assert s.bytes_before == 7000 and s.bytes_after == 4150 and s.bytes_saved == 2850
    assert s.average_reduction_percent == pytest.approx(46.25)
    assert s.average_vmaf == pytest.approx(96.0)
    assert s.originals_removed == 1 and s.bytes_freed == 1000


def test_statistics_with_no_use_yet(workspace):
    from clipshrink.reports import statistics
    s = statistics(workspace / "s.db")
    assert s.files_converted == 0 and s.bytes_saved == 0 and s.average_reduction_percent == 0


def test_export_csv_and_xlsx_match_the_report(workspace, qapp_instance):
    import openpyxl
    from clipshrink.reports import export_reports
    rep = write_report(workspace, ("a.mp4", "b.mp4"))
    dest = workspace / "out"
    made = export_reports([rep], "csv", dest) + export_reports([rep], "xlsx", dest)
    assert [p.suffix for p in made] == [".csv", ".xlsx"]
    assert rows_of(made[0]) == rows_of(rep)
    sheet = openpyxl.load_workbook(made[1]).active
    values = list(sheet.values)
    assert values[0][1] == "File" and values[1][1] == "a.mp4" and values[2][1] == "b.mp4"
    assert values[1][5] == 1000 and values[1][8] == 97.0, "numbers must be real numbers in Excel"


PDF_SCRIPT = """
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtPdf import QPdfDocument
from clipshrink.reports import export_reports
app = QApplication([])
pdf = export_reports([sys.argv[1]], "pdf", sys.argv[2])[0]
d = QPdfDocument()
d.load(str(pdf))
print(pdf.read_bytes()[:4].decode(), d.pageCount())
print("".join(d.getAllText(i).text() for i in range(d.pageCount())))
"""


def test_export_pdf_contains_the_report(workspace):
    """Run on Windows' real text system: the test mode has no fonts, so PDFs come out blank."""
    import subprocess, sys
    from conftest import ROOT
    rep = write_report(workspace, tuple(f"clip{i:03}.mp4" for i in range(60)))
    env = {k: v for k, v in os.environ.items() if k != "QT_QPA_PLATFORM"}
    r = subprocess.run([sys.executable, "-c", PDF_SCRIPT, str(rep), str(workspace / "out")], cwd=ROOT, env=env,
                       capture_output=True, text=True, encoding="utf-8", timeout=60)
    assert r.returncode == 0, r.stderr
    assert r.stdout.startswith("%PDF"), r.stdout[:40]
    assert "clip000.mp4" in r.stdout and "clip059.mp4" in r.stdout, "every row must be in the PDF"


def test_export_never_overwrites(workspace):
    from clipshrink.reports import export_reports
    rep = write_report(workspace)
    dest = workspace / "out"
    a = export_reports([rep], "csv", dest)[0]
    b = export_reports([rep], "csv", dest)[0]
    assert a != b and a.exists() and b.exists()


def test_hostile_file_name_cannot_become_a_spreadsheet_formula(workspace):
    import openpyxl
    from clipshrink.reports import export_reports
    rep = write_report(workspace, ("=cmd.mp4",))
    assert rows_of(rep)[0]["File"].startswith("'=")
    x = export_reports([rep], "xlsx", workspace / "out")[0]
    cell = openpyxl.load_workbook(x).active.cell(2, 2)
    assert cell.data_type == "s" and cell.value.startswith("'=")


def test_delete_report_goes_to_recycle_bin_and_statistics_stay(workspace):
    from clipshrink.reports import delete_reports, list_reports, reports_dir, statistics
    from test_delete import purge_own_test_files, recycle_bin_has
    rep = write_report(workspace)
    unique = rep.with_name(f"report_cs_test_{os.getpid()}_{int(time.time())}.csv")
    os.replace(rep, unique)
    db = workspace / "work" / "s.db"
    before = statistics(db).bytes_saved
    assert delete_reports([unique]) == [unique]
    assert not unique.exists() and list_reports(reports_dir(db)) == []
    found = recycle_bin_has(unique.name)
    assert found, "report should be recoverable from the Recycle Bin"
    purge_own_test_files(found)
    assert statistics(db).bytes_saved == before > 0


def test_a_damaged_report_file_does_not_break_the_list(workspace):
    from clipshrink.reports import list_reports, reports_dir
    db = workspace / "work" / "s.db"
    rep = write_report(workspace)
    (reports_dir(db) / "report_broken.csv").write_bytes(b"\xff\xfe\x00not a report")
    found = list_reports(reports_dir(db))
    assert len(found) == 2 and rep in [r.path for r in found]
