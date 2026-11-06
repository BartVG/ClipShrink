# FAQ and troubleshooting

??? question "Does ClipShrink delete anything without asking?"
    No. During conversion your originals are only read. Removing them is a separate, optional step on the compare page that needs you to tick a box in a dialog, and the originals go to the Recycle Bin, not straight to permanent deletion. See [Compare and clean up](compare-and-clean-up.md).

??? question "Why was a file skipped?"
    The scan only converts H.264 videos. Anything else is shown greyed out, for example "Already H.265, skipped". Files that could not be read are listed in the note under the table. `.lrv` files (GoPro low-res previews) and files you already converted are listed but not ticked by default; tick them if you want them.

??? question "Where did my earlier conversions go on Compare and clean up?"
    That page only lists the videos found or converted since you opened the app. To work on an earlier conversion, choose its folder again on Find videos: a video whose original is still there comes back on the list. Your whole history stays in Reports & Statistics.

??? question "Why was the original kept?"
    ClipShrink refuses a result that is not smaller than the original, or that does not match it (for example different audio or camera info). The exact reason shows as a tooltip in the Result column and in the "Needs your attention" box. See [Warnings and messages](warnings.md).

??? question "What does the warning sign mean?"
    The conversion is smaller and matches the original, but its VMAF quality score is under the bar (average 95, worst 1% 90). It is still saved, and you decide whether to keep it. Play it side by side first. See [the quality bar](../internals/quality.md).

??? question "Can I stop halfway?"
    You can click **Pause** and later **Resume** during a batch. If you close the window while a batch is running, ClipShrink asks "Stop converting?". The file being converted restarts next time, and finished files are kept. If the app or PC crashes, reopen it and choose to continue where you left off.

??? question "Where are my reports?"
    In `%LOCALAPPDATA%\ClipShrink\reports`. The **Reports & Statistics** page has an **Open reports folder** button. See [Reports & Statistics](reports.md).

??? question "Where are the converted files?"
    Beside each original, with `_(h265)` or `_(av1)` added to the name, and the size too if it was shrunk, for example `_(1080p)_(h265)`. Files of any type other than `.mp4`, `.mov`, `.m4v` and `.lrv` are written as `.mkv`, and `.lrv` files become `.mp4`.

??? question "The player shows an error. What now?"
    Messages such as "the video player could not open these files" or "the video player stopped" appear in a box. Close the player window and open the pair again. Both the original and the conversion must still be on disk, and the conversion must be verified or have a warning sign.

??? question "Does it work without an NVIDIA graphics card?"
    Yes. By default ClipShrink uses an NVIDIA card if a test encode on it succeeds, and otherwise uses your processor, which is slower. You can choose in [Settings](settings-and-data.md#encode-with), and the choice is remembered.

??? question "A file shows 'Failed, original kept'. Is my video safe?"
    Yes. Your original is untouched. The reason follows "Could not convert, original kept:". Failed files are not retried automatically in a later run while the original is unchanged.

??? question "Can I compare after I delete an original?"
    No. Once an original has been sent to the Recycle Bin, ClipShrink no longer offers the side-by-side player for that file, even if you restore the original afterwards.

??? question "Will my PC go to sleep during a batch?"
    The Convert page says your computer will not go to sleep while the batch runs.

??? question "Is anything sent over the internet?"
    ClipShrink's About page says nothing is sent anywhere, and that your records and reports stay on your PC in `%LOCALAPPDATA%\ClipShrink`.

## Next steps

- [Warnings and messages](warnings.md)
- [Settings and data](settings-and-data.md)
