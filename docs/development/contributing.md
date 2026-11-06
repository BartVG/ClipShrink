# Contributing

Bug reports and pull requests are welcome. This is a small personal project, so replies may take a while.

## Docs site commands

To preview the documentation locally (Python 3.13):

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

The site is at <http://127.0.0.1:8000/ClipShrink/>. Check that it builds cleanly before you open a pull request:

```powershell
mkdocs build --strict
```

!!! warning "Already ran `setup_dev.bat`?"
    It created `.venv` with Python 3.12 for the app. Do not create `.venv` again. Run `.venv\Scripts\activate`, then `pip install -r requirements-docs.txt` and `mkdocs serve`. Details in [Set up](setup.md#docs-site).

## Set up the app

You need Windows and Python 3.12. See [Set up](setup.md) for the steps.

```bat
setup_dev.bat
```

This creates `.venv` and downloads FFmpeg and mpv into `vendor/`. Then copy a real GoPro clip into `tests/real_clip/`. Run the app with `.venv\Scripts\python.exe app.py`.

## Run the check

```bat
check.bat
```

It takes roughly 10 minutes and passes only if every test passes. A skipped test counts as a failure. See [Testing](testing.md).

## Rules for changes

- **Do not weaken the check.** The bar stays at VMAF mean 95 and 1st percentile 90.
- **Originals are never modified during conversion.**
- **Fix a bug with a test.** Add a test that fails first, then make it pass.
- **Keep tests independent.** `tests/helpers/` must not import the app, so an app bug can't vouch for itself.
- **Never commit video.** Personal clips stay out of the repository. Tests generate their own.

## Build the installer

Install Inno Setup 6 for your user account (`build.bat` looks in `%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe`), then run `build.bat`. The result is `dist\ClipShrink-Setup.exe`. See [Building](building.md).

## Next steps

- [Architecture](architecture.md) to learn the code layout.
- [Writing docs](docs-authoring.md) to add or change a page.
