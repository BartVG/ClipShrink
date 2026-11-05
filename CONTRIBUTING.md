# Contributing

Bug reports and pull requests are welcome. This is a small personal project, so replies may take a while.

## Set up

You need Windows 10 or 11 and Python 3.12.

```bat
setup_dev.bat
```

This creates `.venv` and downloads FFmpeg and mpv into `vendor/`, about 800 MB in total. Then copy a real GoPro clip into `tests/real_clip/`.

## Run it

```bat
.venv\Scripts\python.exe app.py
```

## Run the check

```bat
check.bat
```

It takes about 10 minutes and passes only if every test passes. A skipped test counts as a failure.

## Rules for changes

- **Do not weaken the check.** The bar stays at VMAF mean 95 and 1st percentile 90.
- **Originals are never modified during conversion.**
- **Fix a bug with a test.** Add a test that fails first, then make it pass.
- **Keep tests independent.** `tests/helpers/` must not import the app, so an app bug can't vouch for itself.
- **Never commit video.** Personal clips stay out of the repository. Tests generate their own.

## Build the installer

Install [Inno Setup 6](https://jrsoftware.org/isinfo.php) for your user account, then run:

```bat
build.bat
```

The result is `dist\ClipShrink-Setup.exe`.
