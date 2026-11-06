"""Stage 4: optional cleanup. Only originals with a checked conversion, only with
explicit confirmation, only to the Recycle Bin. Originals of conversions below the
quality bar need a second confirmation."""
import ctypes, os
from ctypes import wintypes
from dataclasses import dataclass, field
from pathlib import Path
from . import db, engine, scan

@dataclass
class DeleteResult:
    deleted: list = field(default_factory=list)
    refused: list = field(default_factory=list)


class _SHFILEOPSTRUCTW(ctypes.Structure):
    _fields_ = [("hwnd", wintypes.HWND), ("wFunc", wintypes.UINT), ("pFrom", wintypes.LPCWSTR),
                ("pTo", wintypes.LPCWSTR), ("fFlags", ctypes.c_ushort), ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", ctypes.c_void_p), ("lpszProgressTitle", wintypes.LPCWSTR)]


@dataclass
class RenameResult:
    renamed: list = field(default_factory=list)   # (old path, new path)
    refused: list = field(default_factory=list)


def _clean_name(rec):
    """The original's name, with the conversion's file type."""
    return str(Path(rec.source).with_suffix(Path(rec.output).suffix))


def why_not_renamable(rec):
    if rec is None:
        return "this file was never converted by this tool"
    if rec.status != "original_deleted":
        return "its original has not been sent to the Recycle Bin"
    if not rec.output or not os.path.exists(rec.output):
        return "the converted file is missing"
    if Path(rec.output).name == Path(_clean_name(rec)).name:
        return "it already has the original's name"
    if not engine.output_intact(rec):
        return "the converted file has changed since it was verified"
    if os.path.exists(_clean_name(rec)):
        return "another file already has that name"
    return None


def renamable(db_path):
    return [r for r in db.read_records(db_path, "original_deleted") if why_not_renamable(r) is None]


def remove_suffix(db_path, paths, confirmed=False, on_progress=None):
    """Gives a conversion its original's name, once the original has gone."""
    res = RenameResult()
    paths = list(paths)
    for i, p in enumerate(paths):
        p = str(p)
        if on_progress:
            on_progress(i, len(paths), p)
        if confirmed is not True:
            res.refused.append((p, "renaming was not confirmed"))
            continue
        rec = db.get(db_path, p)
        reason = why_not_renamable(rec)
        if reason:
            res.refused.append((p, reason))
            continue
        old, new = rec.output, _clean_name(rec)
        try:
            os.rename(old, new)     # never overwrites on Windows
        except OSError as ex:
            res.refused.append((p, f"Windows refused the rename: {ex}"))
            continue
        rec.output = new
        rec.output_mtime_ns = os.stat(new).st_mtime_ns
        db.save(db_path, rec)
        res.renamed.append((old, new))
    if on_progress:
        on_progress(len(paths), len(paths), "")
    return res


def _send_to_recycle_bin(path):
    FO_DELETE, FOF_ALLOWUNDO, FOF_NOCONFIRMATION, FOF_SILENT, FOF_WANTNUKEWARNING = 3, 0x40, 0x10, 0x4, 0x4000
    op = _SHFILEOPSTRUCTW(None, FO_DELETE, str(Path(path).resolve()) + "\0", None,
                          FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT | FOF_WANTNUKEWARNING)
    code = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
    return code == 0 and not op.fAnyOperationsAborted and not os.path.exists(path)


def recycle_previews(paths, on_progress=None):
    """Sends GoPro previews to the Recycle Bin, only while their full video is still beside them."""
    res = DeleteResult()
    paths = list(paths)
    for i, p in enumerate(paths):
        if on_progress:
            on_progress(i, len(paths), p)
        if Path(p).suffix.lower() != ".lrv":
            res.refused.append((p, "it is not an LRV file"))
        elif not scan.lrv_original(p):
            res.refused.append((p, "its full video is not beside it"))
        elif _send_to_recycle_bin(p):
            res.deleted.append(p)
        else:
            res.refused.append((p, "Windows did not move it to the Recycle Bin, so it was left in place"))
    if on_progress:
        on_progress(len(paths), len(paths), "")
    return res


def why_not_deletable(rec, deep=False):
    """Returns the reason the original must stay, or None if it may go."""
    if rec is None:
        return "this file was never converted by this tool"
    if rec.status not in ("verified", "below_bar"):
        return f"its conversion is not verified (status: {rec.status})"
    if not engine.fingerprint_matches(rec):
        return "the original has changed since it was verified"
    if not rec.output or not os.path.exists(rec.output):
        return "the converted file is missing"
    if not engine.output_intact(rec):
        return "the converted file has changed since it was verified"
    if deep:
        if engine.sha256_file(rec.output) != rec.output_sha256:
            return "the converted file's content does not match what was verified"
        try:
            info = scan.probe_file(rec.output)
        except Exception as ex:
            return f"the converted file cannot be read: {ex}"
        if info.codec not in ("hevc", "av1"):
            return "the converted file is not H.265 or AV1"
    return None


def deletable(db_path):
    """The only files that may be offered for deletion."""
    recs = db.read_records(db_path, "verified") + db.read_records(db_path, "below_bar")
    return [r for r in recs if why_not_deletable(r) is None]


def delete_originals(db_path, paths, confirmed=False, below_bar_confirmed=False, on_progress=None,
                     resized_confirmed=False):
    """on_progress(done, total, path) is called before each file and once at the end."""
    res = DeleteResult()
    paths = list(paths)
    for i, p in enumerate(paths):
        p = str(p)
        if on_progress:
            on_progress(i, len(paths), p)
        if confirmed is not True:
            res.refused.append((p, "deletion was not confirmed"))
            continue
        rec = db.get(db_path, p)
        reason = why_not_deletable(rec, deep=True)
        if not reason and rec.status == "below_bar" and below_bar_confirmed is not True:
            reason = "its conversion is below the quality bar, and that was not confirmed"
        if not reason and rec.resized and resized_confirmed is not True:
            reason = "its conversion has a lower resolution, and that was not confirmed"
        if reason:
            res.refused.append((p, reason))
            continue
        if _send_to_recycle_bin(p):
            rec.status = "original_deleted"
            db.save(db_path, rec)
            res.deleted.append(p)
        else:
            res.refused.append((p, "Windows did not move it to the Recycle Bin, so it was left in place"))
    if on_progress:
        on_progress(len(paths), len(paths), "")
    return res
