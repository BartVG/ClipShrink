"""Reports are kept automatically for every batch, for the user's information.
The app writes them and never reads them back."""
import csv
from pathlib import Path
from conftest import copy_preserving
from clipshrink import db as database


def rows_of(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def reports_in(db):
    from clipshrink.reports import reports_dir
    folder = reports_dir(db)
    return sorted(folder.glob("*.csv")) if folder.exists() else []


def test_batch_writes_a_report_automatically(get_clip, workspace):
    from clipshrink.engine import Converter
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    db = workspace / "work" / "s.db"
    c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    found = reports_in(db)
    assert len(found) == 1
    row = rows_of(found[0])[0]
    assert row["File"] == "a.mp4" and Path(row["Folder"]) == src.parent
    assert float(row["VMAF average"]) >= 95 and row["Result"] == "Verified"
    assert int(row["After (bytes)"]) == Path(c.record(src).output).stat().st_size


def test_each_batch_gets_its_own_report_and_old_ones_stay(get_clip, workspace):
    from clipshrink.engine import Converter
    db = workspace / "work" / "s.db"
    for n in ("a.mp4", "b.mp4"):
        src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / n)
        c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
        c.add_files([src])
        c.run()
    found = reports_in(db)
    assert len(found) == 2 and {rows_of(r)[0]["File"] for r in found} == {"a.mp4", "b.mp4"}


def test_batch_with_nothing_to_do_writes_no_report(get_clip, workspace):
    from clipshrink.engine import Converter
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    db = workspace / "work" / "s.db"
    for _ in range(2):
        c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
        c.add_files([src])
        c.run()
    assert len(reports_in(db)) == 1


def test_forgetting_files_keeps_the_reports(get_clip, workspace):
    from clipshrink.engine import Converter, forget_everything
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    db = workspace / "work" / "s.db"
    c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    forget_everything(db, workspace / "work" / "t")
    assert database.read_records(db) == [] and len(reports_in(db)) == 1


def test_hostile_file_name_cannot_become_a_spreadsheet_formula(workspace):
    from clipshrink.reports import write_batch_report
    rec = database.Record(source="C:/Videos/=cmd.mp4", status="verified", source_size=10, output_size=5)
    rep = write_batch_report(workspace / "r", [rec])
    assert rows_of(rep)[0]["File"].startswith("'=")


def test_reports_never_overwrite_each_other(workspace):
    from clipshrink.reports import write_batch_report
    rec = database.Record(source="C:/Videos/a.mp4", status="verified", source_size=10, output_size=5)
    a = write_batch_report(workspace / "r", [rec])
    b = write_batch_report(workspace / "r", [rec])
    assert a != b and a.exists() and b.exists()
