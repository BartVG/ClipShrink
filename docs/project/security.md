# Security

How to report a security problem in ClipShrink, and what to know about the installer.

## How to report

Report security problems privately, through the repository's **Security** tab and **Report a vulnerability**, rather than in a public issue.

Include enough for the problem to be reproduced: the ClipShrink version, what you did, and what happened. For a crafted video file, describe how it was made.

Problems that matter most here:

- anything that could delete or change a file without the confirmation step
- a crafted video file that makes the app misbehave

For ordinary bugs, use a [normal issue](index.md#report-a-bug) instead.

## What to know

According to the project's security policy, ClipShrink makes no network connections of its own and sends no data anywhere.

!!! warning "The installer is not code-signed yet"
    Windows may show a SmartScreen warning when you run it. See [Install](../getting-started/install.md) for what to expect. If the release page lists a SHA-256 checksum, you can compare it with the output of `Get-FileHash`:

    ```powershell
    Get-FileHash "$HOME\Downloads\<installer file name>" -Algorithm SHA256
    ```

    Adjust the path to where you saved the installer.

## Next steps

- [Install ClipShrink](../getting-started/install.md)
- [License and third-party notices](license.md)
