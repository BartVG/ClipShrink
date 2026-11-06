# Estimation

The estimate answers "how much space will I free, and how long will it take?" without converting everything. It test-encodes small samples of real files, then scales the result. Nothing beside the originals is created or changed, and its temporary files are deleted afterwards.

## Choosing the files

ClipShrink groups the selected files by resolution and rounded frame rate, sorts each group largest first, and orders the groups by total size. It then picks files round-robin across the groups, taking the next-largest file each round, until it has up to **5 files**. The number is fixed and not a setting.

## Sampling

Each picked file goes through the same search the real conversion uses (see [Quality](quality.md)):

- 3 pieces of 4 seconds, copied from 25%, 50% and 75% of the file, or the whole file if it is 18 seconds or shorter;
- a binary search over the encoder's 9 quality settings, starting from the previous file's result for the same group.

The samples at the chosen setting are what the estimate uses. If no setting clears the bar, the strictest one is used, because a below-bar file is still converted and still saves space.

## The formula

1. **Ratio per file:** encoded sample bytes divided by source sample bytes, capped at **1.0**. The estimate never predicts growth, and refusals for "not smaller" are not modelled.
2. **Ratio per group:** the average of its files' ratios. A group with no sampled file uses the average of all ratios.
3. **Expected saving:** the sum over all selected files of `video bytes × (1 − group ratio)`. Only video bytes count; audio and other tracks are not part of the saving.
4. **Range:** the low end uses the highest group ratio widened by 20%, the high end uses the lowest group ratio reduced by 20%, so the range is about a fifth either way. The expected value always lies inside it, and the high end cannot exceed the total size.
5. **Time:** the measured seconds of encoding plus VMAF per second of sample, multiplied by the total duration of all selected files, plus **15%** for each file's own quality search.

The headline in the app reads "About {saved} saved ({percent}%)", followed by the likely range and the time.

!!! note "Limits"
    Samples are short pieces, so unusual scenes elsewhere in a file can change the real result. The time estimate counts one encode and VMAF pass at the chosen setting plus the flat 15%, so retries at stricter settings are not modelled.

## Accuracy check

The project's test suite checks that on three generated clips the estimate lands within 35% of the real saving, and that the low end is not above the expected value, which is not above the high end, which is not above the total.

## Next steps

- [Reading the estimate in the app](../user-guide/estimates.md)
- [How quality is measured](quality.md)
