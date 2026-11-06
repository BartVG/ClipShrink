# FAQ and troubleshooting

??? question "Does ClipShrink delete anything without asking?"
    No. During conversion your originals are only read. Removing them is a separate, optional step on the compare page that needs you to tick a box in a dialog, and the originals go to the Recycle Bin, not straight to permanent deletion. See [Compare and clean up](compare-and-clean-up.md).

??? question "Why was a file skipped?"
    The scan only converts H.264 videos. Anything else is shown greyed out, for example "Already H.265, skipped". Files that could not be read are listed in the note under the table. `.lrv` files (GoPro low-res previews) and files you already converted are listed but not ticked by default; tick them if you want them.

??? question "Why was the original kept?"
    ClipShrink refuses a result that is not smaller than the original, or that does not match it (for example different audio or camera info). The exact reason shows as a tooltip in the Result column and in the "Needs your attention" box. See [Warnings and messages](warnings.md).

??? question "What does the warning sign mean?"
    The conversion is smaller and matches the original, but its VMAF score is under the bar (average 95, worst 1% 90). It is still saved, and you decide whether to keep it. Play it side by side first. See [the quality bar](../internals/quality.md).

??? question "Can I stop halfway?"
    You can click **Pause** and later **Resume** during a batch. If you close the window while a batch is running, ClipShrink asks "Stop converting?". The file being converted restarts next time, and finished files are kept. If the app or PC crashes, reopen it and choose to continue where you left off.

??? question "Where are my reports?"
    In `%LOCALAPPDATA%\ClipShrink\reports`. The **Reports & Statistics** page has an **Open reports folder** button. See [Reports and statistics](reports.md).

??? question "Where are the converted files?"
    Beside each original, with `_H265` added to the name. Containers other than MP4, MOV, M4V and LRV are written as `.mkv`, and `.lrv` files become `.mp4`.

??? question "The player shows an error. What now?"
    Messages such as "the video player could not open these files" or "the video player stopped" appear in a box. Close the player window and open the pair again. Both the original and the conversion must still be on disk, and the conversion must be verified or have a warning sign.

??? question "Does it work without an NVIDIA graphics card?"
    Yes. With the default **Automatic (recommended)** speed, ClipShrink uses an NVIDIA card if a test encode on it succeeds, and otherwise uses your processor, which is slower. You can also choose between the two in the **Speed:** menu on the "See the saving" page. The choice is not remembered between runs.

??? question "A file shows 'Failed, original kept'. Is my video safe?"
    Yes. Your original is untouched. The reason follows "Could not convert, original kept:". Failed files are not retried automatically in a later run while the original is unchanged.

??? question "Can I compare after I delete an original?"
    No. The player needs both files on disk. Restore the original from the Recycle Bin first.

??? question "Will my PC go to sleep during a batch?"
    The Convert page says your computer will not go to sleep while the batch runs.

??? question "Is anything sent over the internet?"
    ClipShrink's About page says nothing is sent anywhere, and that your records and reports stay on your PC in `%LOCALAPPDATA%\ClipShrink`.

## Next steps

- [Warnings and messages](warnings.md)
- [Settings and data](settings-and-data.md)
