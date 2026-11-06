# Settings and data

ClipShrink has one option and no settings file. There is no preferences dialog and nothing to configure by hand.

## The Speed option

On the **See the saving** page, the **Speed** drop-down chooses what does the encoding:

| Choice | What it does |
| --- | --- |
| Automatic (recommended) | Uses your graphics card if it supports it, otherwise your processor. This is the default. |
| Graphics card: fast (NVIDIA only) | Uses the NVIDIA hardware H.265 encoder. |
| Processor: slow, works on any PC | Uses the CPU encoder, which works on any computer. |

ClipShrink does not remember your choice: it returns to "Automatic (recommended)" each time you open the app. Changing it clears the current estimate, so run the test encodes again. The conversion then uses the same choice as the estimate.

The quality bar, the number of test pieces and the other rules are fixed and cannot be changed in the app.

## Where ClipShrink keeps its data

Everything stays on your PC; nothing is sent anywhere.

| What | Where | Safe to delete? |
| --- | --- | --- |
| History database | `%LOCALAPPDATA%\ClipShrink\state.db` | Only with the app closed (delete any `state.db-*` files next to it too). You lose the record of earlier conversions: the statistics, the Compare and clean up list, and the "Continue where you left off?" offer. Videos you already converted show as ready again and would be converted a second time (as `_H265_2`). Your videos themselves are not affected. |
| Working files | `%LOCALAPPDATA%\ClipShrink\work` | Yes, with the app closed. It holds temporary files only. It is emptied after each file and when a conversion batch starts or ends; the test-encode folder is cleared after each estimate. |
| Reports | `%LOCALAPPDATA%\ClipShrink\reports` | Yes; the batch then no longer appears on the Reports & Statistics page. One CSV file per batch, named like `report_2026-11-06_141500.csv`. See [Reports & Statistics](reports.md). |
| Your conversions | Beside each original, ending in `_H265` | These are your results. Delete them only if you want to lose them. |

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
