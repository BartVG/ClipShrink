# Testing

The check runs the whole test suite and passes only if every test passes. A skipped test counts as a failure.

## Run the check

```bat
check.bat
```

Passing runs in the log took between 8.5 and 13.7 minutes (see [Test history](../test-history.md)).

`check.bat` runs `check.py` with the `.venv` Python. `check.py`:

- runs `pytest tests -q --tb=short` and writes `docs/.last_check.xml`;
- passes only if pytest exits with 0, at least one test ran, nothing failed or errored, and nothing was skipped;
- appends a row to `docs/check_history.md` (when, duration, counts, result, optional note);
- prints `CHECK PASSED` or `CHECK FAILED` and exits 0 or 1.

Anything you pass to `check.bat` becomes the note on the history row. `docs/.last_check.xml` and `docs/check_history.md` are git-ignored, and the history file is excluded from the docs site. The committed history is [Test history](../test-history.md).

## The real clip

The check needs at least one untouched GoPro file in `tests/real_clip/`, with the camera's file name kept. Everything in that folder is git-ignored except its README.

Every clip there is converted with every available encoder, and all must pass. Without a clip, `test_real_clip_supplied` fails on purpose, so `check.bat` fails. That test asserts the clip has a firmware tag or a GoPro track.

## Test layout

| File | Covers |
| --- | --- |
| `test_scan.py` | Scan finds every H.264 video in all subfolders (unicode names, `.mov`, `.m4v`, `.mkv`); empty folder |
| `test_estimate.py` | Savings estimated from real sample encodes predict the result |
| `test_quality.py` | Conversion quality for each generated clip and each encoder; the real clip; self-guards on the test itself |
| `test_failures.py` | Below-target conversions flagged with the original untouched; larger results and encoder failures keep the original; a failure does not stop the batch; no temp files beside originals; H.265 input refused |
| `test_resume.py` | Crash and resume with a real process kill; requeue when output vanished or source changed; pause and resume |
| `test_delete.py` | Explicit confirmation, Recycle Bin, refusal for unknown, pending, failed or kept files, extra confirmation for below-target, rename rules |
| `test_reports.py` | Automatic report per batch, reports stay when files are forgotten, no overwrite, formula-injection safety |
| `test_interface.py` | Qt interface checks run offscreen: theme, tick boxes, skipped H.265 rows, version in title, sorting, Select All/Recommended, warning sign, About, progress bars |
| `test_player.py` | Side-by-side sync, detail mode, player stopping reported as an error |
| `test_settings.py` | Settings saved and restored, bad settings file, encoder fallback, Settings page, Encoding column, Resized label |
| `test_version_1_7.py` | Open file location, Explorer-style ticking, Settings and About on one page, zoom and dragging, the clickable progress bar, every language complete and switching at once, translated reasons and reports, installer languages |
| `test_version_1_6_1.py` | Taskbar ID only when run from source, resizable columns, VMAF tooltips, Welcome screen |
| `test_version_1_6.py` | Quality policy and real conversions with custom values, Advanced section, About, detected card, automatic start, Start Over and forgetting, "Already has a conversion" |
| `test_codec_and_size.py` | AV1 on generated clips and the real clip, each encoder; where a resize lands; downscaling keeps tracks and meets the target against a shrunken copy; never upscales; estimate follows settings; player with different sizes |

### Quality checks

`test_quality.py` asserts that each default conversion is H.265, has a VMAF mean of at least 95 and a 1st percentile of at least 90 over every frame, is smaller than the original, and keeps the dates and tracks. The NVENC encoder is only included when `hevc_nvenc` works on the machine. Two self-guards keep the target honest: one proves a measurement can fail, and one fails if the app's own thresholds drop below 95 and 90.

## Helpers

`tests/helpers/` measures and generates independently of the app. Nothing there imports the app, so the check does not trust the code it is checking.

`media.py`
:   FFmpeg and FFprobe calls from `vendor/ffmpeg/bin`, VMAF measurement, MP4 box reading, and Windows file-time get and set. It holds the required VMAF numbers (mean 95, 1st percentile 90), marked "Do not lower".

`clips.py`
:   `make_clip` generates an H.264 test video with FFmpeg. `add_gopro_tracks` adds hand-built GoPro-style tracks (`gpmd`, `fdsc`) and camera metadata.

## Fixtures

`tests/conftest.py` sets Qt to the offscreen platform and defines:

| Fixture | Purpose |
| --- | --- |
| `get_clip(name)` | Generates a named clip on demand and caches it for the session |
| `clip_cache` | Session temporary folder for generated clips |
| `workspace` | Temporary folder with `videos/` and `work/` |
| `qapp_instance` | One `QApplication` for the session |

Six clips are defined: `gopro_like_1080p_telemetry`, `fullrange_60fps_telemetry`, `uhd_4k_telemetry`, `rotated_telemetry`, `no_audio_no_telemetry` and `variable_framerate`. The tests define no custom pytest markers.

## Continuous integration

`.github/workflows/tests.yml` runs on every push to `main` and on every pull request, on `windows-latest` with Python 3.12. It creates a venv, installs `requirements.txt`, runs `tools\fetch_vendor.py`, and runs pytest with two exclusions:

- `tests/test_quality.py::test_real_clip_supplied`, because CI has no private footage.
- All of `tests/test_player.py` and the side-by-side test in `tests/test_codec_and_size.py`, because the workflow notes that mpv stops responding on the test machines.

NVENC tests are left out automatically when `hevc_nvenc` or `av1_nvenc` is unavailable. CI does not replace the full check, which runs on a developer PC. CI does not build the installer or publish anything.

## Next steps

- [Contributing](contributing.md) for the rules about tests.
- [Test history](../test-history.md) for logged runs.
