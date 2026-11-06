# ClipShrink

ClipShrink is a Windows app that batch converts H.264 videos to H.265, or to AV1 if you choose, to free up disk space. H.265 is the newer video format: it holds the same picture in a smaller file. Every conversion is compared with its original, frame by frame, and any that miss the quality bar get a warning sign so you decide what to keep. It works on any H.264 video and takes special care of GoPro files, keeping their built-in sensor data (the telemetry).

![The Compare and clean up page, listing verified conversions with sizes and quality scores](images/4-compare-and-clean-up.png)

## Real results

These numbers come from the measured batch in the project README: 34 real 1080p GoPro clips, converted with an NVIDIA graphics card.

| | |
|---|---|
| Before | 10.41 GB |
| After | 4.99 GB |
| Saved | 5.42 GB (52%) |
| Clips that cleared the bar | 34 of 34 |
| Lowest VMAF average | 95.5 (required: 95) |
| Lowest worst-1% score | 90.3 (required: 90) |

VMAF is the score used to compare a conversion with its original, from 0 to 100 (see [How quality is checked](internals/quality.md)). Individual clips saved between 9% and 77%. Your results depend on your footage, so the app measures your own files before you commit.

## Download

Get `ClipShrink-Setup.exe` from the [GitHub Releases page](https://github.com/tophe323/ClipShrink/releases). The current version is 1.5, as listed in the changelog. See [Install](getting-started/install.md) for the steps.

## Where to go next

- [Getting started](getting-started/index.md): install ClipShrink and run your first batch.
- [User guide](user-guide/index.md): each page of the app, warnings, reports and FAQ.
- [How it works](internals/index.md): how the quality bar, estimates and safety checks work.
- [Development](development/index.md): set up, test and build the project.
