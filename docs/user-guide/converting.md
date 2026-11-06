# Converting

Step 3 converts your videos one at a time, measures each one against its original, and keeps the results beside the originals.

![The Convert page, with overall and per-file progress and the table of results](../images/3-convert.png)

## Start, pause, resume, stop

- **Start converting**, on the See the saving page, opens this page and begins the batch by itself. Coming back to this page later never restarts anything. The line near the top shows how many videos, their total size, and the expected time. While it runs, your computer will not go to sleep.
- **Pause** holds the work; the button becomes **Resume**. Pausing is not saved to disk, so it only lasts while the app stays open.
- **Stop**: there is no stop button. Closing the window while converting asks "Stop converting?" The file in progress is restarted next time, and finished files are kept.

Two progress bars show all files and the current file with its stage: "Finding the right quality", "Encoding", "Measuring every frame", then "Done". The table lists File, Folder, State, Before, After, VMAF average and Worst 1% for each video. When the batch ends, a line such as "Finished: 8 verified, ⚠ 1 below target" appears, and **Next: compare and clean up →** unlocks.

Videos are converted one at a time, never in parallel. A file that fails or is kept as original does not stop the rest of the batch.

Drag the edge of a column title to resize it, and hover over **VMAF average** or **Worst 1%** for a short explanation. Columns fit their content until you drag one, and your widths then stay until you click **Start Over**.

## If your PC crashes

Reopen ClipShrink. It asks "Continue where you left off?" with the number of unfinished videos. Choose Yes to carry on; finished files are not redone. The file that was in progress starts again from the beginning. If you decline, ClipShrink forgets that batch. Its finished conversions stay on disk, and the next scan marks their originals "Already has a conversion".

Files that were already kept as original or failed in that batch are not retried on resume. How this works is described in [How resuming works](../internals/resume.md).

## Where the results go

Each conversion is saved next to its original with `_(h265)` or `_(av1)` added to the name, for example `Holiday.mp4` becomes `Holiday_(h265).mp4`. A video that was shrunk also gets its size first: `Holiday_(4k)_(h265).mp4`, `Holiday_(1080p)_(av1).mp4` or `Holiday_(720p)_(h265).mp4`. A video already within the chosen size gets no size tag. If that name is taken, ClipShrink uses `Holiday_(h265)_2.mp4`, then `_3`, and so on. The original is only ever read.

Conversions made before version 1.5 keep their `_H265` or `_AV1` names.

| Original | Result |
| --- | --- |
| `.mp4`, `.mov`, `.m4v` | Same extension |
| `.lrv` (GoPro preview) | `.mp4` |
| `.mkv`, `.avi`, `.mts`, `.m2ts`, `.ts`, `.3gp` | `.mkv` |

The result gets the original's creation and modified dates.

While a file is being copied into place it has the extra ending `.part`, so a half-written file is never mistaken for a finished one. When the copy finishes, the file is renamed to its final name; a leftover `.part` file is deleted if you stop or after a crash. Everything else ClipShrink needs while working goes in its own folder, `%LOCALAPPDATA%\ClipShrink\work`, which is emptied afterwards. See [Settings and data](settings-and-data.md).

## Graphics card or processor

The **Encode with** setting decides whether your NVIDIA graphics card (fast) or your processor (slow, works on any PC) does the encoding; see [Settings and data](settings-and-data.md#encode-with). If the graphics card's encoder reports an error during a batch, that file fails and the original is kept; ClipShrink does not switch to the processor mid-batch.

## What can go wrong

For every file ClipShrink checks that the result is smaller, matches the original, and meets the quality target. If not, the original is kept or the result is flagged with a warning. [Warnings](warnings.md) explains each case, and [How quality is checked](../internals/quality.md) explains why.

## Next steps

- [Compare and clean up](compare-and-clean-up.md) to play results beside the originals.
- [How resuming works](../internals/resume.md) and [How quality is checked](../internals/quality.md) for the details.
