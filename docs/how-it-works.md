# How ClipShrink works

ClipShrink is a Python desktop app that runs three bundled programs: **FFmpeg** encodes and measures, **mpv** plays, and **Qt (PySide6)** draws the window.

| File | Job |
|---|---|
| [`scan.py`](../clipshrink/scan.py) | Finds videos and reads their details |
| [`estimate.py`](../clipshrink/estimate.py) | Measures expected savings from samples |
| [`encode.py`](../clipshrink/encode.py) | Runs FFmpeg: encoding, VMAF, quality search, pause |
| [`mp4graft.py`](../clipshrink/mp4graft.py) | Builds the final MP4 |
| [`engine.py`](../clipshrink/engine.py) | Runs the batch and verifies each file |
| [`db.py`](../clipshrink/db.py) | Remembers progress for crash recovery |
| [`trash.py`](../clipshrink/trash.py) | Recycle Bin and rename rules |
| [`player.py`](../clipshrink/player.py) | Side by side playback |
| [`ui.py`](../clipshrink/ui.py) | The window |

## The four stages

### 1. Scan
It walks the folder and every subfolder, skipping the Recycle Bin and Google Drive's temp folders. `ffprobe`, FFmpeg's file inspector, reads each video's codec, resolution, frame rate and length. Files that can't be read are reported rather than hidden.

### 2. Estimate
It groups files by resolution and frame rate, then picks up to 5 across those groups. From each one it copies three 4-second pieces to a temp folder (clips of 18 seconds or less are used whole), encodes them and scores them with VMAF. The measured size ratio is applied to the whole selection, and the time estimate comes from the same test encodes.

### 3. Convert
One file at a time:

1. **Find the quality setting.** A binary search on samples finds the setting that gives the smallest file and still clears the bar by 0.5 points.
2. **Encode.** FFmpeg encodes the video track only, keeping every frame timestamp.
3. **Build the file.** See below.
4. **Verify.** This checks the codec, resolution, frame count, duration and colour, confirms the other tracks are byte-identical, then runs VMAF on every frame.
5. **Deliver or retry.** A pass is copied next to the original with the original's dates. If VMAF fails, it re-encodes at a stricter setting until the settings run out, then keeps the original.

### 4. Compare and clean up
One mpv process decodes both files and joins them into a single picture. Left and right share one clock, so they can't drift apart.

Before deleting, it recalculates the conversion's SHA-256 fingerprint and checks the original hasn't changed since verification. Only then does it call Windows' Recycle Bin function, with the flag that makes Windows warn if a file would be permanently deleted instead.

## Rebuilding the MP4

FFmpeg can't write GoPro's telemetry (`gpmd`), stabilisation (`fdsc`) or timecode (`tmcd`) tracks into an MP4, and it drops the camera info in the `udta` box. So `mp4graft.py` builds the final file itself:

- **Kept from the original, unchanged:** audio, telemetry, timecode, camera info, creation dates and the rotation setting.
- **Replaced:** only the H.264 video, swapped for the new H.265 video.
- **Layout:** tracks are interleaved in half-second chunks and the index sits at the front of the file, which should help it stream from Drive.

This code is the newest and riskiest part of the tool, which is why verification re-reads the finished file rather than trusting it. Files that aren't MP4 or MOV, such as MKV, are written by FFmpeg instead.

## How quality is judged

- **The bar:** VMAF mean of at least 95, and at least 90 on the 1st percentile. Every frame is scored, with no sampling.
- **4K:** it must pass both the standard and the 4K VMAF models, and the lower score counts.
- **Encoders:** NVIDIA's NVENC is chosen automatically when available. x265 on the processor is the fallback. Each has its own list of 9 quality settings.

On one real 26-second 1080p clip, 101.4 MB became:

| Encoder | Size | VMAF mean | Worst 1% | Time |
|---|---|---|---|---|
| NVENC | 25.9 MB | 96.3 | 91.3 | 81 s |
| x265 | 34.2 MB | 96.7 | 90.4 | 152 s |

NVENC has one trap: without a high `-maxrate`, it silently limits itself to around 25 Mbit/s and ignores its quality setting. ClipShrink sets the cap to 800 Mbit/s.

## How your files stay safe

- **Originals** are only ever opened for reading.
- **Temp work** happens in `%LOCALAPPDATA%\ClipShrink\work`, so half-finished encodes don't upload to Drive. The one exception is a short-lived `.part` file beside the original during the final copy.
- **Crash recovery:** every status change is saved to a small database, `%LOCALAPPDATA%\ClipShrink\state.db`, before work moves on. After a crash, finished files are skipped and the interrupted file restarts from the beginning.
- **Pause** freezes the FFmpeg process in place, so no progress is lost unless the app closes.
- **Closing or crashing:** Windows stops FFmpeg along with the app, so no encoder keeps running in the background.

## How the tests stay honest

The tests in [`tests/`](../tests) don't use the app's code to judge results. They have their own VMAF measurement and their own MP4 reader, so an app bug can't vouch for itself. Two tests guard the suite itself: one proves a bad encode fails the VMAF bar, and one proves the test clips really contain telemetry tracks.

The tests also perform a real process kill to test crash recovery, and check the Recycle Bin to prove a deleted file really arrived there.

`check.bat` passes only if every test passes, and a skipped test counts as a failure. The [history of check runs](test-history.md) shows how the project got there.
