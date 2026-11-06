# Advanced settings

The Advanced part of [Settings](settings-and-data.md) lets you choose your own VMAF values. The defaults suit almost everyone.

!!! warning "Only change these if you know what you are doing"
    Lower values can visibly lower the quality of your videos, and once an original has left the Recycle Bin, that quality can't be recovered. Compare a few files side by side before removing any originals.

The section is greyed out until you tick **I've read this and understand what I'm doing**. Untick it to go back to the defaults for new conversions. The app remembers the values you typed, and files already converted keep their results.

## Warn below

**VMAF average** and **Worst 1%**, 95 and 90 by default. A conversion under either value gets a ⚠ warning sign, and [Select Recommended](compare-and-clean-up.md#choose-what-to-delete) leaves it out.

## Also aim for these values when choosing quality

This box decides whether your values change the files themselves. It's off by default.

| Aim box | Example: values lowered to 90 / 85 | Example: values raised to 98 / 96 |
|---|---|---|
| **Off** | The same files as with the defaults, and the warning only appears below 90 / 85. | The same files as with the defaults, and more of them get a warning. |
| **On** | The app compresses harder: smaller files with lower quality. | The app compresses less: larger files with higher quality. |

Very high values may not be reachable. The app then delivers its best attempt with a warning, unless the result isn't smaller.

These early trial encodes of one real 101.4 MB clip, on the processor, show the size of the trade-off:

| Setting | Size | VMAF average | Worst 1% |
|---|---|---|---|
| CRF 18 | 47.1 MB | 97.9 | 91.9 |
| CRF 22 | 24.3 MB | 95.2 | 88.7 |
| CRF 26 | 12.6 MB | 90.3 | 83.6 |

Your footage will behave differently, so run the test encodes on [See the saving](estimates.md) after changing a value.

## Don't keep a conversion below a minimum

Off by default, which means every result that is smaller and matches the original is kept, with a warning if needed.

Tick it and set a **VMAF average** and **Worst 1%**. A conversion under either one isn't kept. Your original stays, the file shows **Original kept**, and the report gives the reason. The minimum can't be higher than the warning values.

## What changes in the app

- **Labels:** a file judged by other values says so, for example **Verified at 90 / 85** or **Resized at 90 / 85**. Later changes to these settings don't relabel it.
- **Reports:** each report lists the target values used for every file.
- **Removing originals:** if a conversion is below the default 95 / 90, the confirmation warns you, even if it met your lower values.
- **Estimate:** changing a value clears the current estimate, so run the test encodes again.

## Next steps

- [How quality is measured and decided](../internals/quality.md)
- [Settings and data](settings-and-data.md)
