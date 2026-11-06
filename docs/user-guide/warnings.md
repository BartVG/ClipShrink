# Warnings and messages

A reference of the statuses, warning signs and messages you may see, grouped by page. VMAF is the quality score each conversion gets; the bar is an average of 95 and a worst 1% of 90. How it is decided is explained in [Quality measurement](../internals/quality.md).

## Result statuses

These appear in the **State** column while converting and in the **Result** column on the compare page.

| Status | Meaning | What to do |
|---|---|---|
| Verified | The conversion matched the original and cleared the quality bar. | Compare if you like, then clean up. |
| Resized | Shrunk as you asked in Settings. It matched the original and cleared the bar against a shrunken copy of it. | Compare if you like. Its original still holds more detail. |
| ⚠ Below the bar | The conversion is smaller and matches, but its VMAF score is under the bar (average 95, worst 1% 90), even at the strictest setting tried. | Play it side by side before removing its original. |
| Original kept | ClipShrink refused the result and left your original alone. The reason is in the tooltip and in "Needs your attention". | Nothing. Your original is untouched. |
| Failed, original kept | Something went wrong while converting. | Nothing is lost. See the reason. |
| Original in Recycle Bin | You sent the original to the Recycle Bin. | Restore it from there if needed. |
| Done, has the original's name | The conversion was renamed to the original's name. | Nothing. |

## Find videos

| Message | When it appears | What to do |
|---|---|---|
| Already H.265, skipped (or "Already <CODEC>, skipped") | The video is not H.264. | Nothing. Only H.264 is converted. |
| (converted by this tool) | A skipped video is a conversion made by ClipShrink. | Nothing. |
| GoPro low-res preview, off by default | An `.lrv` file, left unticked. | Tick it if you want it converted. |
| N could not be read and were skipped | Some files could not be read by the scan. The first three names are shown. | Check that those files open elsewhere. |
| No H.264 videos found in this folder or its subfolders. | The scan found nothing to convert. | Choose another folder. |

Files you already converted are listed with their earlier result and are not ticked again.

## See the saving

| Message | When it appears | What to do |
|---|---|---|
| ⚠ No, would get a warning | In "Clears the bar?": a test sample scored under the bar. | Expect a warning sign on similar files. |
| Could not measure: "The test encode stopped: …" | The test encodes failed. | Try again, or change **Encode with** in Settings. |

## Convert

| Message | When it appears | What to do |
|---|---|---|
| Finished: N verified, ⚠ N below the bar, N kept as original | The batch ended. | Continue to the compare page. |
| Continue where you left off? | At startup, when files from your last batch were not finished. | Click Yes to continue. Finished files are not converted again. |
| Stop converting? | You closed the window while a batch was running. | If you close, the current file restarts next time and finished files are kept. |
| The batch stopped: "…" | An unexpected error ended the batch. | Reopen the app to continue. Files already verified are safe. |

## Why an original was kept

These reasons appear on the compare page and in reports.

| Reason | When it appears |
|---|---|
| This is <codec>, not H.264, so it was left alone. | The video is not H.264. |
| Conversion is not smaller (X vs Y bytes), original kept. | The finished file was not smaller than the original. |
| Conversion did not match the original, original kept: … | The check found a difference, for example "audio or telemetry tracks changed" or "camera info changed". |
| VMAF compared N frames out of M, original kept. | The quality check did not cover every frame. |
| VMAF below the recommended bar: average X (recommended 95), worst 1% Y (recommended 90). Compare it before removing the original. | The reason shown with "⚠ Below the bar". |
| Could not convert, original kept: … | The status is "Failed, original kept". The error follows, for example that the encoder stopped, a file could not be written, or the original changed while it was converted. |

## Compare and clean up

| Message | When it appears | What to do |
|---|---|---|
| Pick a video: "Click a row in the list first." | You clicked play without a selected row. | Click a row. |
| Cannot compare | The row needs both an original and a verified conversion on disk. | Nothing to compare once an original is gone. |
| Send originals to the Recycle Bin? | You started a delete. | Tick the box to confirm, or click **Keep them**. |
| ⚠ N of these have a conversion below the recommended quality… | Extra paragraph in that dialog when a ticked file has a warning sign. | Compare those files first. |
| Left in place | After a delete, files that were not removed, with a reason each. | Read the reason. |
| Remove the added tags from names? | You started the rename. | Answer Yes or No. |
| Delete GoPro LRV files? | A scan found LRV files with their original video beside them. | Answer Yes to send them to the Recycle Bin, or No to keep them. See [GoPro LRV files](finding-videos.md#gopro-lrv-files). |
| Left as they are | After a rename, files that were not renamed, with a reason each. | Read the reason. |

Reasons a delete is refused, all shown next to the file name:

- this file was never converted by this tool
- its conversion is not verified (status: …)
- the original has changed since it was verified
- the converted file is missing
- the converted file has changed since it was verified
- the converted file's content does not match what was verified
- the converted file cannot be read: …
- the converted file is not H.265 or AV1
- its conversion is below the quality bar, and that was not confirmed
- its conversion has a lower resolution, and that was not confirmed
- Windows did not move it to the Recycle Bin, so it was left in place

Reasons a rename is refused:

- this file was never converted by this tool
- its original has not been sent to the Recycle Bin
- the converted file is missing
- it already has the original's name
- the converted file has changed since it was verified
- another file already has that name
- Windows refused the rename: …

## Player errors

| Message | What it means |
|---|---|
| the video player did not start | The player did not become ready within 20 seconds, or exited immediately. |
| the video player could not open these files | The player did not open the pair in time, or exited. |
| the video player is closed | The player was already closed. |
| the video player stopped | The player stopped while playing. |
| could not switch view: … | The zoom toggle failed. |

They appear in a box titled "Could not play" when the player starts, or "Player" later. Close the player and open the pair again.

## Reports page

| Message | When it appears |
|---|---|
| Could not read | A report file in the table could not be read. |
| Exported | Reports were exported; it names the folder. |
| Could not export | An export failed. |
| Delete reports? | You asked to delete reports; they go to the Recycle Bin. |

## Next steps

- [FAQ and troubleshooting](faq.md)
- [Compare and clean up](compare-and-clean-up.md)
