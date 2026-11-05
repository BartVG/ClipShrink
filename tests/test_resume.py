"""Crash, resume, and pause, using a real process and a real kill."""
import os, subprocess, sys, threading, time
from pathlib import Path
from conftest import ROOT, copy_preserving
from helpers.media import NOWIN, sha256


def statuses(db):
    from clipshrink.db import read_records
    return {Path(r.source).name: r for r in read_records(db)}


def spawn(folder, db, work):
    return subprocess.Popen([sys.executable, "-m", "clipshrink.cli", "convert", str(folder), "--db", str(db),
                             "--work", str(work), "--encoder", "x265"], cwd=str(ROOT), creationflags=NOWIN,
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_for(cond, seconds=240):
    end = time.time() + seconds
    while time.time() < end:
        v = cond()
        if v:
            return v
        time.sleep(0.05)
    raise AssertionError("timed out waiting")


def test_crash_then_resume_skips_finished_files(get_clip, workspace):
    v = workspace / "videos"
    names = ["a.mp4", "b.mp4", "c.mp4"]
    for n in names:
        copy_preserving(get_clip("gopro_like_1080p_telemetry"), v / n)
    db, work = workspace / "work" / "s.db", workspace / "work" / "t"
    p = spawn(v, db, work)
    try:
        def first_done_and_second_running():
            if not db.exists():
                return False
            s = statuses(db)
            done = [r for r in s.values() if r.status == "verified"]
            running = [r for r in s.values() if r.status == "encoding"]
            return (done, running) if done and running else False
        done, _ = wait_for(first_done_and_second_running)
    finally:
        # Hard crash: no cleanup code runs.
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True, creationflags=NOWIN)
        p.wait()
    assert len(done) == 1
    finished = Path(done[0].source).name
    out = Path(done[0].output)
    stamp = (out.stat().st_mtime_ns, out.stat().st_ctime_ns, sha256(out))

    p2 = spawn(v, db, work)
    assert p2.wait(timeout=400) == 0
    s = statuses(db)
    assert all(r.status == "verified" for r in s.values()), {k: (r.status, r.reason) for k, r in s.items()}
    assert (out.stat().st_mtime_ns, out.stat().st_ctime_ns, sha256(out)) == stamp, "finished file was re-encoded"
    assert s[finished].encode_runs == 1, "finished file was re-encoded"
    outs = sorted(x.name for x in v.iterdir())
    assert len(outs) == 6, f"unexpected files after resume: {outs}"
    assert not any(n.endswith(".part") for n in outs)


def test_resume_requeues_when_output_vanished_or_source_changed(get_clip, workspace):
    from clipshrink.engine import Converter
    a = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "a.mp4")
    b = copy_preserving(get_clip("no_audio_no_telemetry"), workspace / "videos" / "b.mp4")
    mk = lambda: Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c = mk()
    c.add_files([a, b])
    c.run()
    os.remove(c.record(a).output)            # conversion lost
    with open(b, "ab") as f:                 # original edited afterwards
        f.write(b"\0" * 16)
    c = mk()
    c.add_files([a, b])
    assert c.record(a).status == "pending"
    assert c.record(b).status == "pending"


def test_pause_stops_work_and_resume_finishes(get_clip, workspace):
    from clipshrink.engine import Converter
    src = copy_preserving(get_clip("uhd_4k_telemetry"), workspace / "videos" / "a.mp4")
    c = Converter(db_path=workspace / "work" / "s.db", work_dir=workspace / "work" / "t", encoder="x265")
    c.add_files([src])
    t = threading.Thread(target=c.run)
    t.start()
    work = workspace / "work" / "t"
    wait_for(lambda: work.exists() and [p for p in work.rglob("*") if p.is_file() and p.stat().st_size > 0], 120)
    c.pause()
    assert c.is_paused
    time.sleep(1.0)
    snapshot = lambda: sorted((str(p), p.stat().st_size) for p in work.rglob("*") if p.is_file())
    a = snapshot()
    time.sleep(3)
    b = snapshot()
    assert a == b, "encoder kept writing while paused"
    assert t.is_alive(), "pause must not end the batch"
    c.resume()
    t.join(timeout=400)
    assert not t.is_alive()
    assert c.record(src).status == "verified"
