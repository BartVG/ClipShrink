# Install

ClipShrink installs like any Windows program and needs no administrator password.

## Download

1. Open the [GitHub Releases page](https://github.com/tophe323/ClipShrink/releases).
2. Download `ClipShrink-Setup.exe` from the latest release.

## Run the installer

Double-click `ClipShrink-Setup.exe`. The installer asks no questions about folders or components, it just installs. At the end it offers "Open ClipShrink now".

!!! warning "The installer is not code-signed"
    Windows may show a "Windows protected your PC" screen (SmartScreen) because the installer is not code-signed. If you downloaded it from the official Releases page above and want to continue, choose **More info**, then **Run anyway**. If you are unsure where the file came from, do not run it.

### Check your download (optional)

If the release page lists a SHA-256 checksum, you can compare it with the one Windows calculates for your file:

```powershell
Get-FileHash .\ClipShrink-Setup.exe -Algorithm SHA256
```

## Where it installs

ClipShrink installs for your user only, into `%LOCALAPPDATA%\Programs\ClipShrink`. The installer does not let you pick another folder. It adds a Start menu entry and a Desktop shortcut.

## Uninstall

The installer is built with Inno Setup, which registers an uninstaller for the app. Remove ClipShrink from Windows' list of installed apps like any other program.

## Next steps

Continue with [Your first batch](first-batch.md).
