"""The batch's memory. Every state change is on disk before work moves on,
which is what makes resume after a crash possible."""
import sqlite3, time
from dataclasses import dataclass
from pathlib import Path

_COLS = ["source", "status", "reason", "source_size", "source_mtime_ns", "output", "output_size", "output_mtime_ns",
         "output_sha256", "vmaf_mean", "vmaf_p1", "encoder", "quality", "encode_runs", "updated"]


@dataclass
class Record:
    source: str
    status: str = "pending"     # pending encoding verified kept_original failed original_deleted
    reason: str = ""
    source_size: int = 0
    source_mtime_ns: int = 0
    output: str = ""
    output_size: int = 0
    output_mtime_ns: int = 0
    output_sha256: str = ""
    vmaf_mean: float = None
    vmaf_p1: float = None
    encoder: str = ""
    quality: float = None
    encode_runs: int = 0
    updated: float = 0.0


def _connect(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(path), timeout=30)
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=FULL")
    c.execute("""CREATE TABLE IF NOT EXISTS files(source TEXT PRIMARY KEY COLLATE NOCASE, status TEXT, reason TEXT,
        source_size INT, source_mtime_ns INT, output TEXT, output_size INT, output_mtime_ns INT, output_sha256 TEXT,
        vmaf_mean REAL, vmaf_p1 REAL, encoder TEXT, quality REAL, encode_runs INT, updated REAL)""")
    return c


def save(db, rec):
    rec.updated = time.time()
    c = _connect(db)
    try:
        with c:
            c.execute(f"INSERT OR REPLACE INTO files({','.join(_COLS)}) VALUES({','.join('?' * len(_COLS))})",
                      [getattr(rec, k) for k in _COLS])
    finally:
        c.close()


def get(db, source):
    c = _connect(db)
    try:
        row = c.execute(f"SELECT {','.join(_COLS)} FROM files WHERE source=?", [str(source)]).fetchone()
    finally:
        c.close()
    return Record(*row) if row else None


def read_records(db, status=None):
    c = _connect(db)
    try:
        q = f"SELECT {','.join(_COLS)} FROM files"
        rows = c.execute(q + " WHERE status=?" if status else q, [status] if status else []).fetchall()
    finally:
        c.close()
    return [Record(*r) for r in rows]
