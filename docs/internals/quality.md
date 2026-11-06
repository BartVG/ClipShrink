# Quality measurement

ClipShrink judges every conversion with **VMAF**, a score that compares the converted video with the original frame by frame. This page explains what is measured, when, and what happens when the score is too low.

!!! note "How the quality bar works"
    A conversion is **recommended** when its VMAF **average is at least 95** and its **worst 1% of frames score at least 90**. Both are measured on every frame of the finished file. Test encodes on samples must clear both numbers by a further **0.5 points** (95.5 and 90.5). For 4K, the lower of two models' scores counts.

## What is measured

- **Average:** the arithmetic mean of the per-frame scores.
- **Worst 1%:** the 1st percentile of the per-frame scores, linearly interpolated. It is a floor for the bad moments, not the mean of the worst frames.
- **Models:** `vmaf_v0.6.1` always. If the video is 2560 pixels or more in width or height, `vmaf_4k_v0.6.1` is also run, and the lower average and the lower worst 1% each count. Both models are built into FFmpeg.

## With a smaller size chosen

If **Largest size** in Settings shrinks a video, the reference is shrunk to the same size with the same scaler before VMAF runs, on both the samples and the finished file. The score therefore measures the encoding only. The file is labelled Resized rather than Verified, and the original's extra detail isn't counted. The larger 4K model is used according to the shrunken size.

## Two measurements

| Stage | What is scored | Margin |
|---|---|---|
| Quality search | Up to 3 sample pieces of 4 seconds each (the whole file if it is 18 seconds or shorter) | 0.5 |
| Final check | Every frame of the finished file, no sampling | 0 |

The search tries the 9 quality settings of the chosen encoder by binary search. It takes the loosest (smallest-file) setting for which all samples clear the bar plus the margin. If the previous file of the same resolution and frame rate used a setting, that one is tried first. If no setting passes, the strictest one is used.

## The decision

```mermaid
flowchart TD
    A["Built file"] --> B{"Smaller than the original?"}
    B -- no --> R{"Earlier below-bar attempt held?"}
    R -- no --> K["Kept original"]
    R -- yes --> W
    B -- yes --> C{"Properties and tracks match?"}
    C -- no --> R
    C -- yes --> D{"VMAF frames = source frames?"}
    D -- no --> R
    D -- yes --> E{"Average ≥ 95 and worst 1% ≥ 90?"}
    E -- "yes, original size" --> V["Verified"]
    E -- "yes, smaller size" --> Z["Resized"]
    E -- no --> F{"Stricter setting left?"}
    F -- yes --> G["Remember as best, encode stricter"]
    G --> B
    F -- no --> W["Below the bar: delivered with a warning"]
    A -. "encoder or VMAF error" .-> X["Failed, original kept"]
```

In words:

- **Verified:** everything matches and both numbers meet the bar.
- **Resized:** the same as Verified, for a video shrunk as chosen in Settings. The numbers compare it with a copy of the original at the same size.
- **Below the bar:** everything matches and the file is smaller, but the score misses the bar even at the strictest setting. The file is delivered with a warning sign. There is no lower VMAF limit in the code.
- **Kept original:** the video was not H.264, the result was not smaller, the result did not match the original, or VMAF did not compare the same number of frames as the source has. Nothing is delivered.
- **Failed:** an error stopped the file (for example the encoder stopped, VMAF could not run, or the original changed during conversion). The original is kept.

### Details worth knowing

- The "smaller" check runs before the VMAF check. A file that is both bigger and low quality is refused, never warned about.
- If a stricter retry turns out not to be smaller or not to match, the earlier below-bar attempt is delivered with its warning.
- The "best" attempt is the most recent (strictest) one, not the highest-scoring one.
- "Properties and tracks match" covers: HEVC codec, resolution, pixel format, colour range, audio codec list, duration (within one frame), and video packet count. For `.mp4`, `.mov`, `.m4v` and `.lrv` it also compares the other tracks and camera info; see [GoPro data](gopro-data.md).
- The estimate's "Clears the bar?" column uses the plain 95 and 90 without the 0.5 margin.

## Measured example

Measured by the project author on one real 26-second 1080p clip of 101.4 MB (from the original How it works page); not reproduced by the automated tests:

| Encoder | Size | VMAF average | Worst 1% | Time |
|---|---|---|---|---|
| NVENC | 25.9 MB | 96.3 | 91.3 | 81 s |
| x265 | 34.2 MB | 96.7 | 90.4 | 152 s |

## Next steps

- [What the warnings mean](../user-guide/warnings.md)
- [How the estimate is made](estimation.md)
