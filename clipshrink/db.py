"""The batch's memory. Every state change is on disk before work moves on,
which is what makes resume after a crash possible."""
import sqlite3, time
from . import config
from dataclasses import dataclass
from pathlib import Path

_COLS = ["source", "status", "reason", "source_size", "source_mtime_ns", "output", "output_size", "output_mtime_ns",
         "output_sha256", "vmaf_mean", "vmaf_p1", "encoder", "quality", "encode_runs", "updated", "codec", "source_width",
         "source_height", "output_width", "output_height", "duration", "target_mean", "target_p1"]
_ADDED = {"codec": "TEXT DEFAULT ''", "source_width": "INT DEFAULT 0", "source_height": "INT DEFAULT 0",
          "output_width": "INT DEFAULT 0", "output_height": "INT DEFAULT 0", "duration": "REAL DEFAULT 0",
          "target_mean": "REAL DEFAULT 0", "target_p1": "REAL DEFAULT 0"}


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
    codec: str = ""
    source_width: int = 0
    source_height: int = 0
    output_width: int = 0
    output_height: int = 0
    duration: float = 0.0
    target_mean: float = 0.0    # the values this file was judged by. 0 means the defaults.
    target_p1: float = 0.0

    @property
    def warn_mean(self):
        return self.target_mean or config.VMAF_MEAN_MIN

    @property
    def warn_p1(self):
        return self.target_p1 or config.VMAF_P1_MIN

    @property
    def meets_target(self):
        return (self.vmaf_mean is not None and self.vmaf_p1 is not None and self.vmaf_mean >= self.warn_mean
                and self.vmaf_p1 >= self.warn_p1)

    @property
    def resized(self):
        return bool(self.output_width and self.source_width and self.output_width != self.source_width)

    @property
    def output_bitrate_mbit(self):
        return self.output_size * 8 / self.duration / 1e6 if self.duration and self.output_size else None


def _prepare(c):
    c.execute("PRAGMA journal_mode=WAL")
    c.execute("PRAGMA synchronous=FULL")
    c.execute("""CREATE TABLE IF NOT EXISTS files(source TEXT PRIMARY KEY COLLATE NOCASE, status TEXT, reason TEXT,
        source_size INT, source_mtime_ns INT, output TEXT, output_size INT, output_mtime_ns INT, output_sha256 TEXT,
        vmaf_mean REAL, vmaf_p1 REAL, encoder TEXT, quality REAL, encode_runs INT, updated REAL, codec TEXT DEFAULT '',
        source_width INT DEFAULT 0, source_height INT DEFAULT 0, output_width INT DEFAULT 0, output_height INT DEFAULT 0,
        duration REAL DEFAULT 0, target_mean REAL DEFAULT 0, target_p1 REAL DEFAULT 0)""")
    have = {row[1] for row in c.execute("PRAGMA table_info(files)")}
    for name, kind in _ADDED.items():       # older databases gain the new columns
        if name not in have:
            c.execute(f"ALTER TABLE files ADD COLUMN {name} {kind}")


def _connect(path):
    """Several openers can arrive together, as the interface and the batch do. SQLite
    reports "locked" at once while one switches to WAL, ignoring its timeout, and
    two can both add a column. Both are harmless, so try again rather than crash."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(str(path), timeout=30)
    end = time.time() + 30
    while True:
        try:
            _prepare(c)
            return c
        except sqlite3.OperationalError as ex:
            text = str(ex)
            if ("locked" not in text and "duplicate column" not in text) or time.time() > end:
                c.close()
                raise
            time.sleep(0.05)


def save(db, rec):
    rec.updated = time.time()
    c = _connect(db)
    try:
        with c:
            c.execute(f"INSERT OR REPLACE INTO files({','.join(_COLS)}) VALUES({','.join('?' * len(_COLS))})",
                      [getattr(rec, k) for k in _COLS])
    finally:
        c.close()


def clear(db):
    """Forgets every file. Reports are separate and stay."""
    c = _connect(db)
    try:
        with c:
            c.execute("DELETE FROM files")
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
