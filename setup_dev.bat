@echo off
rem For developers: creates .venv and downloads FFmpeg and mpv. Needs Python 3.12.
rem People who only want to use ClipShrink should download the installer instead.
cd /d "%~dp0"
if not exist .venv\Scripts\python.exe py -3.12 -m venv .venv || exit /b 1
.venv\Scripts\python.exe -m pip install --quiet --upgrade pip || exit /b 1
.venv\Scripts\python.exe -m pip install --quiet -r requirements.txt || exit /b 1
.venv\Scripts\python.exe tools\fetch_vendor.py || exit /b 1
echo Ready. Add a GoPro clip to tests\real_clip\, then run check.bat
