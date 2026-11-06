"""Stage 2: expected savings, measured by test-encoding samples of real files.
Nothing beside the originals is created or changed."""
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from . import config, encode


@dataclass
class Sample:
    path: str
    at_seconds: float
    quality: float
    source_bytes: int
    encoded_bytes: int
    vmaf_mean: float
    vmaf_p1: float
    passed: bool


@dataclass
class Estimate:
    total_source_bytes: int
    expected_saved_bytes: int
    low_saved_bytes: int
    high_saved_bytes: int
    seconds_estimate: float
    encoder: str
    samples: list = field(default_factory=list)
    files_sampled: int = 0


def _pick(files, max_files):
    """At least one file per kind of footage, then the largest, by share of bytes."""
    groups = {}
    for f in files:
        groups.setdefault(f.group, []).append(f)
    for g in groups.values():
        g.sort(key=lambda f: f.size, reverse=True)
    picks, order = [], sorted(groups.values(), key=lambda g: sum(f.size for f in g), reverse=True)
    i = 0
    while len(picks) < min(max_files, len(files)):
        for g in order:
            if i < len(g) and len(picks) < max_files:
                picks.append(g[i])
        i += 1
    return picks


def estimate_savings(files, encoder="auto", work_dir=None, ladder=None, on_progress=None, max_files=5, gate=None,
                     codec="h265", max_resolution="original"):
    encoder = encode.resolve_encoder(encoder, codec)
    ladder = list(ladder) if ladder else list(config.LADDERS[encoder])
    work = Path(work_dir)
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    picks = _pick(files, max_files)
    samples, by_group, speed = [], {}, []
    hints = {}
    try:
        for n, f in enumerate(picks):
            if on_progress:
                on_progress(n, len(picks), f.path)
            job = work / f"f{n}"
            job.mkdir()
            segs = encode.cut_segments(f.path, f, job, gate=gate)
            found = encode.search_quality(segs, encoder, ladder, f, job, guess=hints.get(f.group), gate=gate,
                                          target=config.target_size(f.width, f.height, max_resolution))
            hints[f.group] = found.index
            rows = found.rows.get(found.index)
            if rows is None:
                continue
            src_total = enc_total = secs = 0
            for row in rows:
                whole = Path(row.segment) == Path(f.path)
                src_bytes = f.video_bytes if whole else Path(row.segment).stat().st_size
                src_total += src_bytes
                enc_total += row.encoded_bytes
                seg_seconds = f.duration if whole else 4.0
                secs += seg_seconds
                speed.append((seg_seconds, row.encode_seconds, row.vmaf_seconds))
                samples.append(Sample(f.path, row.at, ladder[found.index], src_bytes, row.encoded_bytes,
                                      row.score.mean, row.score.p1, found.passed))
            ratio = enc_total / src_total     # below the bar is still converted, and still saves space
            by_group.setdefault(f.group, []).append(min(ratio, 1.0))
            shutil.rmtree(job, ignore_errors=True)
        if on_progress:
            on_progress(len(picks), len(picks), "")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    all_ratios = [r for v in by_group.values() for r in v] or [1.0]
    total = sum(f.size for f in files)
    expected = low = high = 0
    for f in files:
        rs = by_group.get(f.group, all_ratios)
        avg = sum(rs) / len(rs)
        expected += f.video_bytes * (1 - avg)
        # A single sample has its own uncertainty: widen by a fifth either way.
        low += f.video_bytes * max(0.0, 1 - min(1.0, max(rs) * 1.2))
        high += f.video_bytes * (1 - min(rs) * 0.8)
    low, expected, high = int(low), int(expected), int(high)
    low = min(low, expected)
    high = min(max(high, expected), total)

    sec_per_media = 0.0
    if speed:
        media = sum(s[0] for s in speed) or 1
        sec_per_media = (sum(s[1] for s in speed) + sum(s[2] for s in speed)) / media
    # +15% for each file's own quality search
    seconds = max(1.0, sum(f.duration for f in files) * sec_per_media * 1.15)
    return Estimate(total, expected, low, high, seconds, encoder, samples, len(picks))
