# History of check runs

Every completed full run while building versions 1.1 to 1.5. A "full run" is one execution of `check.bat` (or `python check.py`), which runs the whole test suite and passes only if every test passes; a skipped test counts as a failure. Each run appends a row to `docs/check_history.md`. Your own runs are logged there, and that file stays on your PC.

For how the tests are organized and how to run them, see [Testing](development/testing.md).

| When | Took | Tests | Passed | Failed | Skipped | Result | Note |
|---|---|---|---|---|---|---|---|
| 2026-11-05 19:57 | 4.2 min | 41 | 3 | 38 | 0 | FAIL | baseline: tests only, app not written |
| 2026-11-05 20:26 | 9.2 min | 41 | 41 | 0 | 0 | PASS | attempt 1: engine, UI, packaging in place |
| 2026-11-05 22:01 | 8.5 min | 50 | 50 | 0 | 0 | PASS | after hand test: dark theme display, whole-cell ticks, remove _H265 |
| 2026-11-05 22:21 | 8.8 min | 55 | 55 | 0 | 0 | PASS | version 1.1: H.265 files listed as skipped |
| 2026-11-05 22:43 | 9.7 min | 55 | 55 | 0 | 0 | PASS | clean copy of the repo, set up from scratch |
| 2026-11-05 22:21 | 8.8 min | 55 | 55 | 0 | 0 | PASS | version 1.1: H.265 files listed as skipped |
| 2026-11-05 23:13 | 13.0 min | 57 | 57 | 0 | 0 | PASS | version 1.2: wording for any H.264 video |
| 2026-11-05 23:27 | 13.7 min | 58 | 58 | 0 | 0 | PASS | version 1.2: player failure reported cleanly |
| 2026-11-06 08:26 | 9.1 min | 91 | 91 | 0 | 0 | PASS | version 1.3: reports, statistics, below-bar conversions, sorting, folders, selection |
| 2026-11-06 08:38 | 9.1 min | 91 | 91 | 0 | 0 | PASS | version 1.3: final build |
| 2026-11-06 13:02 | 27.6 min | 161 | 161 | 0 | 0 | PASS | version 1.4: settings, AV1, downscaling, encoding column, new look |
| 2026-11-06 14:03 | 22.5 min | 163 | 163 | 0 | 0 | PASS | 1.4 fix: several openers of the database no longer clash |
| 2026-11-06 17:48 | 17.3 min | 213 | 213 | 0 | 0 | PASS | version 1.5: full MOV sound, LRV clean-up, new names, session-only compare, player autostart |
