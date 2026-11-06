# Building

Build the installer `dist\ClipShrink-Setup.exe` from source.

## Prerequisites

- The dev environment from [Set up](setup.md), including the downloaded tools in `vendor/`.
- [Inno Setup 6](https://jrsoftware.org/isinfo.php) installed for your user account. `build.bat` looks for it at `%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe`.

## Build

```bat
build.bat
```

It runs two steps:

1. PyInstaller builds a windowed one-folder app from `app.py` into `dist\ClipShrink\`. It bundles `ffmpeg.exe`, `ffprobe.exe` (with the FFmpeg licence) and `mpv.exe` from `vendor/`, plus `LICENSE` and `THIRD_PARTY_NOTICES.md`. It excludes the Qt modules QtWebEngineCore, QtQml, QtQuick, Qt3DCore and QtMultimedia.
2. Inno Setup compiles `installer\clipshrink.iss` into `dist\ClipShrink-Setup.exe`.

`build.bat` does not run the tests, compute a checksum or sign anything. Run [the check](testing.md#run-the-check) yourself first. `build/`, `dist/` and `*.spec` are git-ignored.

## The installer

The Inno Setup script installs for the current user only (no administrator rights) into `%LOCALAPPDATA%\Programs\ClipShrink`. It is 64-bit only, creates Start menu and desktop shortcuts, and offers to open ClipShrink when it finishes.

!!! warning "The installer is unsigned"
    The installer has no code signature, so Windows SmartScreen may warn when someone runs it. See [Security](../project/security.md).

## Vendor tools

`tools/fetch_vendor.py` (run by `setup_dev.bat`) downloads the two bundled programs into `vendor/` if they are missing:

- FFmpeg: the latest release of `BtbN/FFmpeg-Builds`, the `win64-gpl` build of the 8.1 series.
- mpv: the latest release of `shinchiro/mpv-winbuild-cmake`, the `x86_64` build.

Nothing is pinned to an exact version or checksum: the script asks GitHub for the latest release. If the release layout changes and no asset matches, the script exits with an error. Set `GITHUB_TOKEN` in the environment to avoid GitHub API rate limits. Archives are extracted with `C:\Windows\System32\tar.exe`. `vendor/` is git-ignored.

## Releasing

The version number is kept by hand in three places: `VERSION` in `clipshrink/config.py` (shown in the window title and the About page), `AppVersion` in `installer\clipshrink.iss`, and the newest entry in [CHANGELOG.md](https://github.com/tophe323/ClipShrink/blob/main/CHANGELOG.md). The repository contains no script that publishes a release.

## Next steps

- [Testing](testing.md) before you build.
- [Changelog](../project/changelog.md) for released versions.
