# Third-party software

The ClipShrink installer bundles the programs below. ClipShrink is released under the GNU GPL version 3 (see `LICENSE`), which is compatible with them.

| Software | Used for | Licence | Source code |
|---|---|---|---|
| [FFmpeg](https://ffmpeg.org) n8.1, GPL build from [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds) | Encoding, VMAF, reading files | GPL | [FFmpeg source](https://ffmpeg.org/download.html), [build scripts](https://github.com/BtbN/FFmpeg-Builds) |
| [x265](https://www.videolan.org/developers/x265.html), inside FFmpeg | H.265 encoding on the processor | GPL 2 or later | [x265 source](https://bitbucket.org/multicoreware/x265_git) |
| [VMAF](https://github.com/Netflix/vmaf), inside FFmpeg | Quality measurement | BSD+Patent | [VMAF source](https://github.com/Netflix/vmaf) |
| [mpv](https://mpv.io), build from [shinchiro/mpv-winbuild-cmake](https://github.com/shinchiro/mpv-winbuild-cmake) | Side by side playback | GPL 2 or later | [mpv source](https://github.com/mpv-player/mpv), [build scripts](https://github.com/shinchiro/mpv-winbuild-cmake) |
| [Qt 6 / PySide6](https://www.qt.io/qt-for-python) | The window and buttons | LGPL 3 | [PySide source](https://code.qt.io/cgit/pyside/pyside-setup.git/) |
| [Python](https://www.python.org) | Runs the app | PSF | [Python source](https://www.python.org/downloads/source/) |
| [PyInstaller](https://pyinstaller.org) | Packages the app | GPL 2 with bootloader exception | [PyInstaller source](https://github.com/pyinstaller/pyinstaller) |

**Exact versions in release 1.1:**

- FFmpeg `n8.1.3-34-ga35157abb9-20261105`
- mpv `v0.42.0-1-g3138fc8ee`, built 2026-11-05

`tools/fetch_vendor.py` shows exactly where the bundled builds come from.

GoPro, Google Drive, NVIDIA and Netflix are trademarks of their owners. ClipShrink is an independent project, not affiliated with or endorsed by any of them.
