# GoPro data and metadata

GoPro clips carry more than video and sound: a telemetry track (`gpmd`), a stabilisation track (`fdsc`), a timecode track and camera info in the `udta` box. FFmpeg refuses or drops these when it writes an MP4. So for `.mp4`, `.mov`, `.m4v` and `.lrv` files, ClipShrink does not use FFmpeg to write the final file. FFmpeg encodes the video alone, and ClipShrink's own writer, [`mp4graft.py`](https://github.com/tophe323/ClipShrink/blob/main/clipshrink/mp4graft.py), builds the file.

## What is kept

The final file is the original's structure with only the H.264 video swapped for the new H.265 or AV1 video.

- **Other tracks:** every track other than the main video has its samples copied chunk by chunk, with its track box unchanged except the chunk offsets.
- **Movie-level boxes:** everything in the movie box other than tracks is kept, including `udta` (camera info) and `mvhd`.
- **Main video track:** takes the new encoded media, but keeps the original's track header (track id, rotation matrix, size, flags), timecode reference, creation dates and language. Its duration and edit list are rescaled to the original's timescale.

## What differs

| Part | What happens |
|---|---|
| `ftyp` (file type) | Regenerated, not copied. QuickTime originals get a QuickTime brand; others get major brand `mp42` with compatible brands `mp42`, `isom` and `hvc1`. |
| Video handler name | If the original's handler name starts with "GoPro", the new one is "GoPro H.265" or "GoPro AV1". |
| Layout | The index (`moov`) sits at the front, followed by one `mdat`. 64-bit offsets are used when the file would reach 4 GiB. |
| Chunking | Only the new video is regrouped into about half-second chunks. Other tracks keep their original chunking, and all tracks are interleaved by time. |

ClipShrink does not read GoPro's telemetry content. It treats every non-main-video track as opaque data to copy.

## How it is checked

After the build, ClipShrink computes a SHA-256 digest of each non-video track's sample bytes in the original and in the result, and compares the camera info box. A difference reads "audio or telemetry tracks changed" or "camera info changed", and the original is kept. The digests cover sample data, not the track and header boxes.

If the writer meets something unexpected (for example a damaged file, no index, or an unexpected track layout), there is no fallback to FFmpeg: the file is marked failed and the original is kept.

## Other containers

Files in `.mkv`, `.avi`, `.mts`, `.m2ts`, `.ts` and `.3gp` are remuxed by FFmpeg (repackaged without re-encoding; `-map 0:v -map 1:a? -map 1:s? -map_metadata 1 -c copy`) into `.mkv`. For these, the guarantees above do **not** apply:

- data streams such as `gpmd` are not mapped and are dropped;
- there is no byte-level check of other tracks; only the list of audio codec names is compared.

Output names: `.mp4`, `.mov` and `.m4v` keep their extension, `.lrv` becomes `.mp4`, and everything else becomes `.mkv`.

When a smaller size is chosen in Settings, the video track's display size changes to match, along with the rotation offset that depends on it. Audio, telemetry, timecode and camera info stay byte for byte.

!!! note "Test coverage"
    The test suite uses synthetic `gpmd` and `fdsc` tracks that imitate GoPro's GPMF telemetry format, camera info, and timecode. A real HERO5-or-later clip with GPS is listed as untested in the README's limitations.

## Next steps

- [How a file is verified](quality.md)
- [The pipeline overview](index.md)
