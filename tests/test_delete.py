"""Deletion: explicit confirmation, verified only, to the Recycle Bin."""
import os, subprocess, uuid
from pathlib import Path
import pytest
from conftest import copy_preserving
from helpers.media import NOWIN


def recycle_bin_has(name):
    ps = ("$s=New-Object -ComObject Shell.Application;$b=$s.Namespace(10);"
          f"$b.Items()|?{{$_.Name -like '{Path(name).stem}*'}}|%{{$_.Path}}")
    r = subprocess.run(["powershell", "-NoProfile", "-c", ps], capture_output=True, text=True, creationflags=NOWIN)
    return [x.strip() for x in r.stdout.splitlines() if x.strip()]


def purge_own_test_files(paths):
    """Removes only the $R/$I pair of this test's own uniquely named clip."""
    for p in paths:
        rp = Path(p)
        rp.unlink(missing_ok=True)
        (rp.parent / ("$I" + rp.name[2:])).unlink(missing_ok=True)


@pytest.fixture
def verified(get_clip, workspace):
    from clipshrink.engine import Converter
    name = f"clipshrink_test_{uuid.uuid4().hex}.mp4"
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / name)
    db = workspace / "work" / "s.db"
    c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    c.run()
    assert c.record(src).status == "verified"
    return src, db, c


def test_requires_explicit_confirmation(verified):
    from clipshrink.trash import delete_originals
    src, db, _ = verified
    res = delete_originals(db, [src])
    assert res.deleted == [] and src.exists()
    res = delete_originals(db, [src], confirmed=False)
    assert res.deleted == [] and src.exists()


def test_verified_goes_to_recycle_bin_and_conversion_stays(verified):
    from clipshrink.trash import delete_originals
    src, db, c = verified
    out = Path(c.record(src).output)
    res = delete_originals(db, [src], confirmed=True)
    assert [Path(p) for p in res.deleted] == [src], res.refused
    assert not src.exists() and out.exists()
    found = recycle_bin_has(src.name)
    assert found, "original is not in the Recycle Bin"
    purge_own_test_files(found)
    assert c.record(src).status == "original_deleted"


def test_refuses_unknown_file(workspace):
    from clipshrink.trash import delete_originals
    f = workspace / "videos" / "never_converted.mp4"
    f.write_bytes(b"x")
    res = delete_originals(workspace / "work" / "s.db", [f], confirmed=True)
    assert res.deleted == [] and f.exists() and res.refused


def test_refuses_pending_failed_and_kept(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.trash import deletable, delete_originals
    db = workspace / "work" / "s.db"
    work = workspace / "work" / "t"
    pend = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "pending.mp4")
    Converter(db_path=db, work_dir=work, encoder="x265").add_files([pend])
    bad = workspace / "videos" / "bad.mp4"
    bad.write_bytes(b"garbage" * 50)
    c = Converter(db_path=db, work_dir=work, encoder="x265", only=[bad])
    c.add_files([bad])
    c.run()
    assert c.record(bad).status == "failed"
    from helpers.clips import make_clip
    kept = make_clip(workspace / "videos" / "kept.mp4", w=640, h=360, seconds=3, crf=45, telemetry=False)
    c = Converter(db_path=db, work_dir=work, encoder="x265", ladder=[4], only=[kept])
    c.add_files([kept])
    c.run()
    assert c.record(kept).status == "kept_original"
    for f in (pend, bad, kept):
        res = delete_originals(db, [f], confirmed=True)
        assert res.deleted == [] and f.exists() and res.refused, f
    assert deletable(db) == [], "only verified files may be offered"


def test_refuses_if_conversion_missing_or_altered(verified):
    from clipshrink.trash import deletable, delete_originals
    src, db, c = verified
    out = Path(c.record(src).output)
    assert [Path(r.source) for r in deletable(db)] == [src]
    saved = out.read_bytes()
    # altered: same size, different bytes
    b = bytearray(saved)
    b[len(b) // 2] ^= 0xFF
    out.write_bytes(bytes(b))
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused
    assert deletable(db) == []
    # missing
    out.unlink()
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused


def test_refuses_if_original_changed_since_verification(verified):
    from clipshrink.trash import delete_originals
    src, db, _ = verified
    with open(src, "ab") as f:
        f.write(b"edit")
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused


def test_below_bar_original_needs_its_own_confirmation(get_clip, workspace):
    from clipshrink.engine import Converter
    from clipshrink.trash import deletable, delete_originals
    name = f"clipshrink_test_{uuid.uuid4().hex}.mp4"
    src = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / name)
    db = workspace / "work" / "s.db"
    c = Converter(db_path=db, work_dir=workspace / "work" / "t", encoder="x265", ladder=[51])
    c.add_files([src])
    c.run()
    assert c.record(src).status == "below_bar"
    assert [Path(r.source) for r in deletable(db)] == [src], "below-the-bar originals are offered"
    res = delete_originals(db, [src], confirmed=True)
    assert res.deleted == [] and src.exists() and res.refused, "plain confirmation is not enough"
    res = delete_originals(db, [src], confirmed=True, below_bar_confirmed=True)
    assert [Path(p) for p in res.deleted] == [src]
    purge_own_test_files(recycle_bin_has(src.name))


def test_google_drive_warning_is_gone():
    from clipshrink import trash
    assert not hasattr(trash, "GOOGLE_DRIVE_WARNING")


# --- Removing the added tags from the name, only after the original has gone
def test_rename_refused_while_original_exists(verified):
    from clipshrink.trash import remove_suffix, renamable
    src, db, c = verified
    out = Path(c.record(src).output)
    assert renamable(db) == []
    res = remove_suffix(db, [src], confirmed=True)
    assert res.renamed == [] and res.refused and out.exists() and src.exists()


def _delete_first(src, db):
    from clipshrink.trash import delete_originals
    assert delete_originals(db, [src], confirmed=True).deleted
    purge_own_test_files(recycle_bin_has(src.name))


def test_rename_after_delete_takes_original_name_and_keeps_dates(verified):
    from clipshrink.trash import remove_suffix, renamable
    from helpers.media import get_times, sha256
    src, db, c = verified
    out = Path(c.record(src).output)
    digest, (created, modified) = sha256(out), get_times(out)
    _delete_first(src, db)
    assert [Path(r.source) for r in renamable(db)] == [src]
    assert remove_suffix(db, [src]).renamed == [], "needs confirmation"
    assert out.exists()
    res = remove_suffix(db, [src], confirmed=True)
    assert [Path(new) for _, new in res.renamed] == [src], res.refused
    assert src.exists() and not out.exists() and sha256(src) == digest
    c2, m2 = get_times(src)
    assert abs(c2 - created) < 2 and abs(m2 - modified) < 2
    assert Path(c.record(src).output) == src
    assert renamable(db) == [], "already renamed"


def test_rename_refused_if_name_taken_or_conversion_changed(verified):
    from clipshrink.trash import remove_suffix, renamable
    src, db, c = verified
    out = Path(c.record(src).output)
    _delete_first(src, db)
    src.write_bytes(b"someone restored or made this file")
    res = remove_suffix(db, [src], confirmed=True)
    assert res.renamed == [] and res.refused and src.read_bytes().startswith(b"someone") and out.exists()
    src.unlink()
    out.write_bytes(out.read_bytes() + b"x")
    res = remove_suffix(db, [src], confirmed=True)
    assert res.renamed == [] and res.refused and out.exists() and not src.exists()
    assert renamable(db) == []
