# FAQ and troubleshooting

??? question "Does ClipShrink delete anything without asking?"
    No. During conversion your originals are only read. Removing them is a separate, optional step on the compare page that needs you to tick a box in a dialog, and the originals go to the Recycle Bin, not straight to permanent deletion. See [Compare and clean up](compare-and-clean-up.md).

??? question "Why was a file skipped?"
    The scan only converts H.264 videos. Anything else is shown greyed out, for example "Already H.265, skipped". Files that could not be read are listed in the note under the table. `.lrv` files (GoPro low-res previews) and files you already converted are listed but not ticked by default; tick them if you want them.

??? question "Where did my earlier conversions go on Compare and clean up?"
    That page only lists the batch you just ran. Once you exit or click **Start Over**, ClipShrink forgets those files. The conversions stay on disk, each batch's report stays in the reports folder, and you can remove earlier originals yourself.

??? question "What's VMAF?"
    A score from 0 to 100 made by Netflix, for how close a video looks to the original, based on how people see video. At 95 or above, most people can't see a difference. **Worst 1%** is the score of the worst moments: 1% of the video's frames score lower than this, so it catches a short bad patch that a good average would hide. Hover over either column title in the app for a reminder.

??? question "Why does a file say Already has a conversion?"
    An H.265 or AV1 file with the same name and a tag such as `_(h265)` is in the same folder. It isn't ticked, so it isn't converted twice. Tick it if you do want to convert it again.

??? question "Why was the original kept?"
    ClipShrink refuses a result that is not smaller than the original, or that does not match it (for example different audio or camera info). The exact reason shows as a tooltip in the Result column and in the "Needs your attention" box. See [Warnings and messages](warnings.md).

??? question "What does the warning sign mean?"
    The conversion is smaller and matches the original, but its VMAF quality score is under the target (average 95, worst 1% 90). It is still saved, and you decide whether to keep it. Play it side by side first. See [the quality target](../internals/quality.md).

??? question "Can I stop halfway?"
    You can click **Pause** and later **Resume** during a batch. If you close the window while a batch is running, ClipShrink asks "Stop converting?". The file being converted restarts next time, and finished files are kept. If the app or PC crashes, reopen it and choose to continue where you left off.

??? question "Where are my reports?"
    In `%LOCALAPPDATA%\ClipShrink\reports`. The **About** page has a link that opens the folder. See [Reports](reports.md).

??? question "Where are the converted files?"
    Beside each original, with `_(h265)` or `_(av1)` added to the name, and the size too if it was shrunk, for example `_(1080p)_(h265)`. Files of any type other than `.mp4`, `.mov`, `.m4v` and `.lrv` are written as `.mkv`, and `.lrv` files become `.mp4`.

??? question "The player shows an error. What now?"
    Messages such as "the video player could not open these files" or "the video player stopped" appear in a box. Close the player window and open the pair again. Both the original and the conversion must still be on disk, and the conversion must be verified or have a warning sign.

??? question "Does it work without an NVIDIA graphics card?"
    Yes. By default ClipShrink uses an NVIDIA card if a test encode on it succeeds, and otherwise uses your processor, which is slower. Settings shows which card was detected, and you can choose in [Settings](settings-and-data.md#encode-with). The choice is remembered.

??? question "A file shows 'Failed, original kept'. Is my video safe?"
    Yes. Your original is untouched. The reason follows "Could not convert, original kept:". If you scan it again in a later session, it's offered again.

??? question "Can I compare after I delete an original?"
    No. Once an original has been sent to the Recycle Bin, ClipShrink no longer offers the side-by-side player for that file, even if you restore the original afterwards.

??? question "Will my PC go to sleep during a batch?"
    The Convert page says your computer will not go to sleep while the batch runs.

??? question "Is anything sent over the internet?"
    ClipShrink's About page says nothing is sent anywhere, and that your records and reports stay on your PC in `%LOCALAPPDATA%\ClipShrink`.

## Next steps

- [Warnings and messages](warnings.md)
- [Settings and data](settings-and-data.md)
