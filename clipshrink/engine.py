"""Stage 3: the batch. One file at a time. Each file goes through
search -> encode -> build -> verify -> deliver, and originals are only read."""
import hashlib, os, shutil, threading, time
from pathlib import Path
from . import config, db, encode, mp4graft, reports, scan, tools

WEIGHTS = {"search": 0.15, "encode": 0.55, "verify": 0.30}


def sha256_file(path, checkpoint=None):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                return h.hexdigest()
            h.update(b)
            if checkpoint:
                checkpoint()


def output_path_for(src):
    src = Path(src)
    ext = src.suffix if src.suffix.lower() in (".mp4", ".mov", ".m4v") else (
        ".mp4" if src.suffix.lower() == ".lrv" else ".mkv")
    return src.with_name(f"{src.stem}{config.OUTPUT_SUFFIX}{ext}")


def fingerprint_matches(rec):
    try:
        st = os.stat(rec.source)
    except OSError:
        return False
    return st.st_size == rec.source_size and st.st_mtime_ns == rec.source_mtime_ns


def output_intact(rec):
    try:
        st = os.stat(rec.output)
    except OSError:
        return False
    return st.st_size == rec.output_size and st.st_mtime_ns == rec.output_mtime_ns


class Verdict(Exception):
    """Conversion finished but must not replace anything. The original stays."""
    def __init__(self, reason, score=None, retry_stricter=False):
        super().__init__(reason)
        self.reason, self.score, self.retry_stricter = reason, score, retry_stricter


class Converter:
    def __init__(self, db_path, work_dir, encoder="auto", ladder=None, on_event=None, only=None):
        self.db_path = Path(db_path)
        self.work_dir = Path(work_dir)
        self.encoder = encode.resolve_encoder(encoder)
        self.ladder = list(ladder) if ladder else list(config.LADDERS[self.encoder])
        self.on_event = on_event or (lambda ev: None)
        self.gate = encode.Gate()
        self._scope = {}
        self._hints = {}
        self._recover()
        if only:
            self.add_files(only)

    # --- queue -------------------------------------------------------------
    def _recover(self):
        """After a crash: anything mid-way goes back in the queue, scraps go."""
        for r in db.read_records(self.db_path, "encoding"):
            r.status = "pending"
            db.save(self.db_path, r)
            part = Path(str(output_path_for(r.source)) + ".part")
            part.unlink(missing_ok=True)
        if self.work_dir.exists():
            for d in self.work_dir.glob("job_*"):
                shutil.rmtree(d, ignore_errors=True)

    def add_files(self, paths):
        for p in paths:
            p = str(Path(p).resolve() if not isinstance(p, str) else p)
            st = os.stat(p)
            rec = db.get(self.db_path, p)
            if rec:
                same = rec.source_size == st.st_size and rec.source_mtime_ns == st.st_mtime_ns
                keep = same and (rec.status in ("kept_original", "failed", "pending")
                                 or (rec.status in ("verified", "below_bar") and output_intact(rec)))
                if keep:
                    self._scope[p] = True
                    continue
                if rec.status == "original_deleted":
                    continue
            db.save(self.db_path, db.Record(source=p, source_size=st.st_size, source_mtime_ns=st.st_mtime_ns))
            self._scope[p] = True

    def record(self, source):
        return db.get(self.db_path, str(source))

    def records(self):
        return db.read_records(self.db_path)

    # --- controls ----------------------------------------------------------
    def pause(self):
        self.gate.pause()
        self.on_event({"type": "paused"})

    def resume(self):
        self.gate.resume()
        self.on_event({"type": "resumed"})

    def stop(self):
        self.gate.request_stop()

    @property
    def is_paused(self):
        return self.gate.paused

    # --- batch -------------------------------------------------------------
    def run(self):
        todo = [p for p in self._scope if self.record(p).status == "pending"]
        total_bytes = sum(self.record(p).source_size for p in todo) or 1
        done_bytes = 0
        started = time.time()
        if not os.environ.get("PYTEST_CURRENT_TEST"):
            tools.keep_awake(True)
        self.on_event({"type": "batch_start", "count": len(todo)})
        finished, report = [], None
        try:
            for i, path in enumerate(todo):
                rec = self.record(path)
                size = rec.source_size

                def progress(frac, stage, path=path, done=done_bytes, size=size, i=i):
                    overall = (done + size * frac) / total_bytes
                    took = time.time() - started
                    eta = took * (1 - overall) / overall if overall > 0.002 else None
                    self.on_event({"type": "progress", "path": path, "file_fraction": frac, "stage": stage,
                                   "overall": overall, "eta_seconds": eta, "index": i, "count": len(todo)})

                self.on_event({"type": "file_start", "path": path, "index": i, "count": len(todo)})
                try:
                    self._convert(rec, progress)
                except encode.Stopped:
                    rec.status = "pending"
                    rec.reason = ""
                    db.save(self.db_path, rec)
                    self.on_event({"type": "stopped"})
                    return self._cleanup_and_summary()
                finished.append(path)
                try:
                    report = reports.write_batch_report(reports.reports_dir(self.db_path),
                                                        [self.record(p) for p in finished], report)
                except OSError:
                    pass    # a report that can't be written must never stop the conversions
                self.on_event({"type": "file_done", "path": path, "record": self.record(path)})
                done_bytes += size
        finally:
            tools.keep_awake(False)
        summary = self._cleanup_and_summary()
        self.on_event({"type": "batch_done", "summary": summary})
        return summary

    def _cleanup_and_summary(self):
        if self.work_dir.exists():
            for d in self.work_dir.glob("job_*"):
                shutil.rmtree(d, ignore_errors=True)
        recs = [self.record(p) for p in self._scope]
        return {s: sum(1 for r in recs if r.status == s)
                for s in ("verified", "below_bar", "kept_original", "failed", "pending")}

    # --- one file ----------------------------------------------------------
    def _convert(self, rec, progress):
        src = rec.source
        work = self.work_dir / f"job_{hashlib.sha1(src.encode()).hexdigest()[:12]}"
        shutil.rmtree(work, ignore_errors=True)
        work.mkdir(parents=True)
        rec.status = "encoding"
        rec.reason = ""
        rec.encoder = self.encoder
        db.save(self.db_path, rec)
        try:
            self._convert_inner(rec, work, progress)
        except encode.Stopped:
            raise
        except Verdict as v:
            self._finish_kept(rec, v)
        except Exception as ex:
            rec.status = "failed"
            rec.reason = f"Could not convert, original kept: {ex}"
            db.save(self.db_path, rec)
        finally:
            shutil.rmtree(work, ignore_errors=True)
            Path(str(output_path_for(src)) + ".part").unlink(missing_ok=True)

    def _finish_kept(self, rec, v):
        rec.status = "kept_original"
        rec.reason = v.reason
        if v.score:
            rec.vmaf_mean, rec.vmaf_p1 = v.score.mean, v.score.p1
        db.save(self.db_path, rec)

    def _convert_inner(self, rec, work, progress):
        gate = self.gate
        src = rec.source
        info = scan.probe_file(src)
        if info.codec != "h264":
            raise Verdict(f"This is {info.codec}, not H.264, so it was left alone.")
        progress(0.0, "search")
        tmp_src_stat = (info.size, info.mtime_ns)
        segments = encode.cut_segments(src, info, work, gate=gate)
        steps = max(2, len(self.ladder) // 2)
        done_steps = [0]

        def on_step(_):
            done_steps[0] += 1
            progress(WEIGHTS["search"] * min(1.0, done_steps[0] / steps), "search")

        found = encode.search_quality(segments, self.encoder, self.ladder, info, work,
                                      guess=self._hints.get(info.group), gate=gate, on_step=on_step)
        self._hints[info.group] = found.index
        for at, seg in segments:
            if Path(seg).parent == work:
                Path(seg).unlink(missing_ok=True)

        best = None     # the best conversion so far that is below the bar
        for idx in range(found.index, len(self.ladder)):
            q = self.ladder[idx]
            rec.quality, rec.encode_runs = q, rec.encode_runs + 1
            db.save(self.db_path, rec)
            video = work / "video.mp4"
            base = WEIGHTS["search"]

            def on_enc(t, base=base):
                progress(base + WEIGHTS["encode"] * min(1.0, t / (info.duration or 1)), "encode")

            code, err = encode.encode_video(src, video, self.encoder, q, info, gate, on_enc)
            if code or not video.exists():
                raise RuntimeError(f"the encoder stopped: {err.strip()[-300:]}")
            built = work / f"built{output_path_for(src).suffix}"
            self._build(src, video, built, gate)
            progress(base + WEIGHTS["encode"], "verify")
            base2 = base + WEIGHTS["encode"]

            def on_ver(t, base2=base2):
                progress(base2 + WEIGHTS["verify"] * min(1.0, t / (info.duration or 1)), "verify")

            try:
                score = self._verify(src, built, info, work, gate, on_ver)
            except Verdict as v:
                if v.retry_stricter:
                    kept = work / f"best{built.suffix}"
                    os.replace(built, kept)
                    video.unlink(missing_ok=True)
                    best = (kept, v.score, v.reason)
                    continue
                if best:        # a stricter try grew or didn't match: settle for the best one
                    break
                raise
            self._deliver(rec, built, info, score, tmp_src_stat, gate)
            progress(1.0, "done")
            return
        if best:
            self._deliver(rec, best[0], info, best[1], tmp_src_stat, gate, "below_bar", best[2])
            progress(1.0, "done")

    def _build(self, src, video, built, gate):
        if Path(src).suffix.lower() in config.GRAFT_EXTS:
            mp4graft.graft(src, video, built, gate.checkpoint)
            return
        code, err = encode.run_ffmpeg(["-y", "-i", video, "-i", src, "-map", "0:v", "-map", "1:a?", "-map", "1:s?",
                                       "-map_metadata", "1", "-c", "copy", built], gate)
        if code:
            raise RuntimeError(f"could not write the file: {err.strip()[-300:]}")

    def _verify(self, src, built, info, work, gate, on_time):
        """Every check must pass before the file is delivered. Raises Verdict."""
        out = scan.probe_file(built)
        if out.size >= info.size:
            raise Verdict(f"Conversion is not smaller ({out.size:,} vs {info.size:,} bytes), original kept.")
        problems = []
        if out.codec != "hevc":
            problems.append(f"video is {out.codec}")
        if (out.width, out.height) != (info.width, info.height):
            problems.append("resolution differs")
        if out.pix_fmt.replace("yuvj", "yuv") != info.pix_fmt.replace("yuvj", "yuv"):
            problems.append(f"pixel format differs ({out.pix_fmt} vs {info.pix_fmt})")
        if out.color_range != info.color_range and info.color_range not in ("", "unknown"):
            problems.append("colour range differs")
        if out.audio_codecs != info.audio_codecs:
            problems.append("audio tracks differ")
        frame = 1 / (info.fps or 30)
        if abs(out.duration - info.duration) > frame:
            problems.append(f"duration differs ({out.duration:.3f}s vs {info.duration:.3f}s)")
        nf_a, nf_b = self._packet_count(src), self._packet_count(built)
        if nf_a != nf_b:
            problems.append(f"frame count differs ({nf_b} vs {nf_a})")
        if Path(src).suffix.lower() in config.GRAFT_EXTS:
            if mp4graft.nonvideo_digests(src) != mp4graft.nonvideo_digests(built):
                problems.append("audio or telemetry tracks changed")
            if mp4graft.udta(src) != mp4graft.udta(built):
                problems.append("camera info changed")
        if problems:
            raise Verdict("Conversion did not match the original, original kept: " + "; ".join(problems))
        score = encode.measure_vmaf(built, src, info, work, gate, on_time)
        if score.frames != nf_a:
            raise Verdict(f"VMAF compared {score.frames} frames out of {nf_a}, original kept.")
        if not score.passes():
            raise Verdict(f"VMAF below the recommended bar: average {score.mean:.1f} (recommended "
                          f"{config.VMAF_MEAN_MIN:.0f}), worst 1% {score.p1:.1f} (recommended "
                          f"{config.VMAF_P1_MIN:.0f}). Compare it before removing the original.",
                          score, retry_stricter=True)
        return score

    @staticmethod
    def _packet_count(path):
        r = tools.run([tools.ffprobe(), "-v", "error", "-select_streams", "v:0", "-count_packets",
                       "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", str(path)])
        return int(r.stdout.strip().split(",")[0]) if r.returncode == 0 and r.stdout.strip() else -1

    def _deliver(self, rec, built, info, score, src_stat, gate, status="verified", reason=""):
        """Moves the verified file beside the original. Originals are not touched."""
        st = os.stat(rec.source)
        if (st.st_size, st.st_mtime_ns) != src_stat:
            raise RuntimeError("the original changed while it was being converted")
        digest = sha256_file(built, gate.checkpoint)
        dest = output_path_for(rec.source)
        n = 2
        while dest.exists():
            dest = dest.with_name(f"{Path(rec.source).stem}{config.OUTPUT_SUFFIX}_{n}{dest.suffix}")
            n += 1
        part = Path(str(dest) + ".part")
        with open(built, "rb") as a, open(part, "wb") as b:
            while True:
                data = a.read(4 << 20)
                if not data:
                    break
                b.write(data)
                gate.checkpoint()
        os.replace(part, dest)
        tools.set_file_times(dest, int(st.st_ctime * 1e9), st.st_mtime_ns)
        final = os.stat(dest)
        rec.status = status
        rec.reason = reason
        rec.output = str(dest)
        rec.output_size = final.st_size
        rec.output_mtime_ns = final.st_mtime_ns
        rec.output_sha256 = digest
        rec.vmaf_mean, rec.vmaf_p1 = score.mean, score.p1
        db.save(self.db_path, rec)
