# How your files stay safe

The safety model is simple: ClipShrink never changes an original, and it never removes one unless you confirm and a final re-check passes.

## While converting

- **Originals are only read.** The conversion is written beside the original as `<name>_(h265)` or `<name>_(av1)`, with a size tag such as `_(1080p)` first if it was shrunk, plus an extension: the same for `.mp4`, `.mov` and `.m4v`, `.mp4` for `.lrv`, and `.mkv` for other types. With AV1, `.mov` also becomes `.mp4`. If that name exists, a number is added (`_(h265)_2`, and so on), so nothing is overwritten.
- **Delivery is staged.** The file is copied to a `.part` file and renamed only when complete, then given the original's created and modified times.
- **The original is re-checked.** If its size or modified time changed while it was being converted, the file is marked failed and nothing is delivered.
- **Bad results are refused.** A result that is not smaller, or does not match the original, is never delivered. See [Quality](quality.md).
- **No orphan encoders.** FFmpeg runs in a Windows Job Object that kills it if ClipShrink exits or crashes. This covers FFmpeg encode and measure runs and the mpv player, not the short ffprobe and encoder-test probes.

## Removing originals

Originals are never deleted permanently by ClipShrink. They are sent to the Windows Recycle Bin through the shell with the undo flag, so you can restore them. The only code that removes an original is this one, and success requires that Windows reports no error and the file is gone. If Windows does not move a file, it is left in place and listed with a reason.

Only conversions with status `verified` or `below_bar` can be removed. Before each file, ClipShrink checks that:

1. the record exists;
2. the original's size and modified time are unchanged since verification;
3. the converted file exists, with the recorded size and modified time;
4. the converted file's SHA-256 matches the one stored at verification;
5. `ffprobe` reports the converted file's codec as `hevc` or `av1`.

The original is checked by size and modified time, not by a hash. Only the conversion is hashed.

### Confirmation

A single dialog, "Send originals to the Recycle Bin?", must be accepted: its "Send to Recycle Bin" button stays disabled until the "I understand" box is ticked, and the default button is "Keep them". If any ticked file is below the bar, or at a lower resolution, the same dialog adds a warning paragraph for each. The steps as you see them are in [Compare and clean up](../user-guide/compare-and-clean-up.md#send-originals-to-the-recycle-bin).

!!! warning "Below-bar originals"
    Once an original is also gone from the Recycle Bin, any quality lost in a below-bar conversion cannot be recovered.

### Renaming

The optional "Remove the added tags" step renames a conversion to its original's file name once the original is in the Recycle Bin. It uses a plain rename that never overwrites, and refuses if the conversion changed or the target name is taken.

## Next steps

- [Comparing and cleaning up in the app](../user-guide/compare-and-clean-up.md)
- [Pause, resume and crash recovery](resume.md)

## GoPro LRV files

The optional LRV clean-up only touches files ending in `.lrv`, sends them to the Recycle Bin, and checks just before each one that its full video is still beside it. If that video has gone, the preview stays. See [GoPro LRV files](../user-guide/finding-videos.md#gopro-lrv-files).
