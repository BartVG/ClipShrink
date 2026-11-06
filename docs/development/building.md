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

1. PyInstaller builds a windowed one-folder app from `app.py` into `dist\ClipShrink\`. It bundles `ffmpeg.exe`, `ffprobe.exe` (with the FFmpeg licence) and `mpv.exe` from `vendor/`, plus `LICENSE`, `THIRD_PARTY_NOTICES.md` and the `licenses` folder. It excludes the Qt modules QtWebEngineCore, QtQml, QtQuick, Qt3DCore and QtMultimedia.
2. Inno Setup compiles `installer\clipshrink.iss` into `dist\ClipShrink-Setup.exe`.

`build.bat` does not run the tests, compute a checksum or sign anything. Run [the check](testing.md#run-the-check) yourself first. `build/`, `dist/` and `*.spec` are git-ignored.

## The installer

The Inno Setup script installs for the current user only (no administrator rights) into `%LOCALAPPDATA%\Programs\ClipShrink`. It is 64-bit only, creates Start menu and desktop shortcuts, and offers to open ClipShrink when it finishes.

!!! warning "The installer is unsigned"
    The installer has no code signature, so Windows SmartScreen may warn when someone runs it. See [Security](../project/security.md).

## Vendor tools

`tools/fetch_vendor.py` (run by `setup_dev.bat`) downloads the two bundled programs into `vendor/`. `tools/vendor.lock.json` names the exact FFmpeg and mpv builds and their SHA-256 checksums, and the script refuses a file whose checksum differs. Upstream deletes old builds, so it falls back to our copy in the `third-party-1.5.1` release. Archives are extracted with `C:\Windows\System32\tar.exe`. `vendor/` is git-ignored.

### Third-party source and license texts

The GPL and LGPL require the matching source of what we ship. `tools/fetch_sources.py` gathers it:

- `dist\third-party-source\`: an archive for each component, to attach to a release.
- `licenses\`: license texts and `COMPONENTS.md`, committed and installed with the app.

Run it after changing `vendor.lock.json`, then commit `licenses\` and rebuild. Needs Git, and several GB of disk space.

## Releasing

The version number is kept by hand in three places: `VERSION` in `clipshrink/config.py` (shown in the window title and the About page), `AppVersion` in `installer\clipshrink.iss`, and the newest entry in [CHANGELOG.md](https://github.com/tophe323/ClipShrink/blob/main/CHANGELOG.md). The repository contains no script that publishes a release. If the bundled builds changed, publish `dist\third-party-source\` and the two pinned builds in a `third-party-<version>` release, with each archive's folder name added to the front of its file name because some names repeat, and update the `mirror` in `tools/vendor.lock.json` and the links in the notices.

## Next steps

- [Testing](testing.md) before you build.
- [Changelog](../project/changelog.md) for released versions.
