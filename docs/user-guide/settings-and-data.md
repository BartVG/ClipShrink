# Settings and data

Open **Settings** in the sidebar. The defaults suit most people, so you can leave this page alone. Choices are saved at once and remembered, in `settings.json`. They are locked while a batch is running.

## Encode with

| Choice | What it does |
| --- | --- |
| Graphics card (fast, recommended) | Uses your NVIDIA card. This is the default. If no NVIDIA card can do the job, the page says so and the processor is used. |
| Processor (slow, works on any PC) | Uses the processor, on any computer. |

Other graphics cards aren't supported yet, so those PCs use the processor.

## Video format

| Choice | What it does |
| --- | --- |
| H.265 (recommended) | The default. It plays on most devices from about 2016 onwards. Files end in `_H265`. |
| AV1 | Files are usually smaller, but they play on fewer devices. Files end in `_AV1`, and a `.mov` original becomes `.mp4`. |

On one real 26-second 1080p clip of 101.4 MB, each of these cleared the quality bar:

| Format | Encoded with | Size | Time |
| --- | --- | --- | --- |
| H.265 | Graphics card | 25.9 MB | 81 s |
| H.265 | Processor | 34.2 MB | 152 s |
| AV1 | Graphics card | 23.5 MB | 96 s |
| AV1 | Processor | 17.8 MB | 102 s |

Your results will differ, so check that your TV or phone can play one AV1 file before converting everything.

Whether GoPro's own software accepts AV1 files hasn't been tested.

## Largest size

| Choice | What it does |
| --- | --- |
| Keep the original resolution (recommended) | The default. Nothing is shrunk. |
| 4K, 1080p or 720p | Shrinks anything bigger to fit, keeping its shape. Portrait video is handled too, and videos are never enlarged. |

!!! warning "Shrinking loses detail for good"
    The conversion is compared with a copy of the original shrunk to the same size. So its VMAF score shows how clean the encoding is, not the detail lost by shrinking. These files are labelled **Resized** instead of Verified, and the dialog warns you before you remove their originals.

## Encoding column

Tick this to add an **Encoding** column on the Convert and Compare pages, showing the format, the encoder, the quality setting, the resolution and the bitrate. Conversions made before version 1.4 only show what was recorded then.

Changing any setting except this one clears the current estimate, so run the test encodes again. The quality bar and the number of test pieces are fixed.

A file that is already converted isn't converted again when you change a setting.

## Where ClipShrink keeps its data

Everything stays on your PC; nothing is sent anywhere.

| What | Where | Safe to delete? |
| --- | --- | --- |
| Settings | `%LOCALAPPDATA%\ClipShrink\settings.json` | Yes; you get the defaults again. |
| History database | `%LOCALAPPDATA%\ClipShrink\state.db` | Only with the app closed (delete any `state.db-*` files next to it too). You lose the record of earlier conversions: the statistics, the Compare and clean up list, and the "Continue where you left off?" offer. Videos you already converted show as ready again and would be converted a second time (as `_H265_2`). Your videos themselves are not affected. |
| Working files | `%LOCALAPPDATA%\ClipShrink\work` | Yes, with the app closed. It holds temporary files only. It is emptied after each file and when a conversion batch starts or ends; the test-encode folder is cleared after each estimate. |
| Reports | `%LOCALAPPDATA%\ClipShrink\reports` | Yes; the batch then no longer appears on the Reports & Statistics page. One CSV file per batch, named like `report_2026-11-06_141500.csv`. See [Reports & Statistics](reports.md). |
| Your conversions | Beside each original, ending in `_H265` or `_AV1` | These are your results. Delete them only if you want to lose them. |

If your account has no `LOCALAPPDATA` folder, ClipShrink uses a `ClipShrink` folder in your home folder instead.

To open the data folder, paste this into the address bar of File Explorer:

```text
%LOCALAPPDATA%\ClipShrink
```

!!! tip
    The About page in the app also tells you where your data lives.

## Next steps

- [Reports & Statistics](reports.md)
- [FAQ](faq.md)
