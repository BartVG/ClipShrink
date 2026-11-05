# Put a real GoPro clip here

The check needs at least one untouched GoPro file, straight from the camera, in this folder.
Clips stay on your computer: `.gitignore` keeps them out of the repository, so never force-add one.

- Name: keep the camera's name, such as `GX010123.MP4` or `GOPR1234.MP4`.
- Length: 10 to 60 seconds with some motion keeps the check fast.
- Every clip here is tested with every encoder on your PC, and all of them must pass.

Without a clip, `test_real_clip_supplied` fails, so `check.bat` fails. That is deliberate.
