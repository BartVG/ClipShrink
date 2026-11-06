@echo off
rem Builds dist\ClipShrink-Setup.exe
cd /d "%~dp0"
.venv\Scripts\python.exe -m PyInstaller --noconfirm --windowed --name ClipShrink ^
  --add-binary "vendor\ffmpeg\bin\ffmpeg.exe;vendor\ffmpeg\bin" ^
  --add-binary "vendor\ffmpeg\bin\ffprobe.exe;vendor\ffmpeg\bin" ^
  --add-data "vendor\ffmpeg\LICENSE.txt;vendor\ffmpeg" ^
  --add-binary "vendor\mpv\mpv.exe;vendor\mpv" ^
  --icon "assets\clipshrink.ico" --add-data "assets\clipshrink.ico;assets" --add-data "LICENSE;." --add-data "THIRD_PARTY_NOTICES.md;." --add-data "licenses;licenses" ^
  --exclude-module PySide6.QtWebEngineCore --exclude-module PySide6.QtQml --exclude-module PySide6.QtQuick ^
  --exclude-module PySide6.Qt3DCore --exclude-module PySide6.QtMultimedia ^
  app.py || exit /b 1
"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe" /Q installer\clipshrink.iss || exit /b 1
echo Built dist\ClipShrink-Setup.exe
