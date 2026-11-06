# License and third-party notices

## ClipShrink

ClipShrink is released under the GNU General Public License version 3. The full text is in the [LICENSE file on GitHub](https://github.com/tophe323/ClipShrink/blob/main/LICENSE). This license is compatible with the bundled software listed below.

## Bundled third-party software

The ClipShrink installer bundles these programs.

| Component | Used for | License | Source |
|---|---|---|---|
| [FFmpeg](https://ffmpeg.org) n8.1, GPL build from [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds) | Encoding, VMAF, reading files | GPL 3 or later | [FFmpeg source](https://ffmpeg.org/download.html), [build scripts](https://github.com/BtbN/FFmpeg-Builds) |
| [SVT-AV1](https://github.com/AOMediaCodec/SVT-AV1), inside FFmpeg | AV1 encoding on the processor | BSD-3-Clause-Clear | [SVT-AV1 source](https://github.com/AOMediaCodec/SVT-AV1) |
| [x265](https://www.videolan.org/developers/x265.html), inside FFmpeg | H.265 encoding on the processor | GPL 2 or later | [x265 source](https://bitbucket.org/multicoreware/x265_git) |
| [VMAF](https://github.com/Netflix/vmaf), inside FFmpeg | Quality measurement | BSD+Patent | [VMAF source](https://github.com/Netflix/vmaf) |
| [mpv](https://mpv.io), build from [shinchiro/mpv-winbuild-cmake](https://github.com/shinchiro/mpv-winbuild-cmake) | Side by side playback | GPL 2 or later | [mpv source](https://github.com/mpv-player/mpv), [build scripts](https://github.com/shinchiro/mpv-winbuild-cmake) |
| [Qt 6 / PySide6](https://www.qt.io/qt-for-python) | The window and buttons | LGPL 3 | [PySide source](https://code.qt.io/cgit/pyside/pyside-setup.git/) |
| [Python](https://www.python.org) | Runs the app | PSF | [Python source](https://www.python.org/downloads/source/) |
| [PyInstaller](https://pyinstaller.org) | Packages the app | GPL 2 with bootloader exception | [PyInstaller source](https://github.com/pyinstaller/pyinstaller) |

### Exact versions in release 1.6

- FFmpeg `n8.1.3-34-ga35157abb9-20261105`
- mpv `v0.42.0-1-g3138fc8ee`, built 2026-11-05

[`tools/vendor.lock.json`](https://github.com/tophe323/ClipShrink/blob/main/tools/vendor.lock.json) records exactly which builds these are, with their checksums.

### Source code

The exact source of FFmpeg, mpv, Qt and the libraries inside them is in the [third-party-1.5.1 release](https://github.com/tophe323/ClipShrink/releases/tag/third-party-1.5.1), along with the build recipes.

### License texts

The `licenses` folder installed with ClipShrink holds them. `licenses/COMPONENTS.md` lists every library inside FFmpeg and mpv, with the commit it came from. mpv's build follows each project's newest code, so apart from mpv, FFmpeg and libplacebo, its commits are the newest ones when that build started.

Qt also ships `opengl32sw.dll` (Mesa, MIT license), and Python needs Microsoft's Visual C++ runtime files, which Microsoft allows to be redistributed with apps.

## Trademarks

GoPro, Google Drive, NVIDIA and Netflix are trademarks of their owners. ClipShrink is an independent project, not affiliated with or endorsed by any of them.

## Next steps

- [Changelog](changelog.md)
- [Security](security.md)
