# Set up

Set up a development environment, run ClipShrink from source, and optionally preview this documentation site.

## Requirements

- Python 3.12. `setup_dev.bat` creates the virtual environment with `py -3.12`, and CI also uses 3.12.
- Windows. The tool uses the Recycle Bin and other Windows APIs.

## Create the environment

From the repository root:

```bat
setup_dev.bat
```

The script runs these steps and stops at the first one that fails:

1. Creates `.venv` with `py -3.12 -m venv .venv`, only if `.venv\Scripts\python.exe` does not exist yet.
2. Upgrades pip.
3. Installs `requirements.txt` (pinned: PyInstaller, PySide6, pytest, openpyxl).
4. Runs `tools\fetch_vendor.py`, which downloads FFmpeg and mpv into `vendor/` (see [Building](building.md#vendor-tools)).

When it finishes it prints a reminder to add a GoPro clip to `tests\real_clip\` before running `check.bat`. See [Testing](testing.md#the-real-clip).

## Run the app from source

```bat
.venv\Scripts\python.exe app.py
```

`app.py` only calls `clipshrink.ui.main()`. It takes no arguments.

## Docs site

The documentation is built with MkDocs Material. Its dependencies are pinned in `requirements-docs.txt`. The docs are built with Python 3.13:

```powershell
py -3.13 -m venv .venv
```

```powershell
.venv\Scripts\activate
```

```powershell
pip install -r requirements-docs.txt
```

```powershell
mkdocs serve
```

The site is then at <http://127.0.0.1:8000/ClipShrink/> and reloads when you save a page.

!!! warning "Already ran `setup_dev.bat`?"
    `setup_dev.bat` already created `.venv` with Python 3.12 for the app. Do not create `.venv` again. Activate it and install only the docs requirements:

    ```powershell
    .venv\Scripts\activate
    ```

    ```powershell
    pip install -r requirements-docs.txt
    ```

    ```powershell
    mkdocs serve
    ```

Before you push documentation changes, check that the site builds without warnings:

```powershell
mkdocs build --strict
```

## Next steps

- [Architecture](architecture.md) to find your way around the code.
- [Writing docs](docs-authoring.md) to add a page.
