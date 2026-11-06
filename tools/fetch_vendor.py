"""Downloads the two programs ClipShrink bundles (FFmpeg and mpv) into vendor/.
They are not stored in this repository because of their size. Run by setup_dev.bat.

The exact builds and their checksums are in tools/vendor.lock.json, so every
developer and every release gets the same files. To move to newer builds, change
that file and run tools/fetch_sources.py again."""
import hashlib, json, shutil, subprocess, sys, tempfile, urllib.error, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
LOCK = Path(__file__).with_name("vendor.lock.json")
TAR = r"C:\Windows\System32\tar.exe"   # Windows' own tar also reads .zip and .7z
MARKER = ".pinned-sha256"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def urls_for(item, mirror):
    """The upstream address first. Upstream deletes old builds, so our own copy is the fallback."""
    return [item["url"], mirror + item["file"]]


def download_verified(item, mirror, dest):
    """Saves the build to dest, and never accepts a file whose checksum differs from the lock file."""
    problems = []
    for url in urls_for(item, mirror):
        try:
            print(f"Downloading {url}")
            urllib.request.urlretrieve(url, dest)
        except (urllib.error.URLError, OSError) as e:
            problems.append(f"{url}: {e}")
            continue
        actual = sha256_of(dest)
        if actual == item["sha256"]:
            return
        problems.append(f"{url}: checksum {actual}, expected {item['sha256']}")
    sys.exit(f"Could not get {item['file']}:\n  " + "\n  ".join(problems))


def is_current(item, folder):
    marker = folder / MARKER
    return (folder / item["check"]).exists() and marker.exists() and marker.read_text().strip() == item["sha256"]


def install(item, mirror, folder):
    if is_current(item, folder):
        return
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / item["file"]
        download_verified(item, mirror, file)      # before removing anything, so a failure leaves vendor/ intact
        shutil.rmtree(folder, ignore_errors=True)
        folder.mkdir(parents=True)
        cmd = [TAR, "-xf", str(file), "-C", str(folder)]
        if item["strip"]:
            cmd.append("--strip-components=1")
        subprocess.run(cmd, check=True)
    (folder / MARKER).write_text(item["sha256"])


def main():
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    for name in ("ffmpeg", "mpv"):
        install(lock[name], lock["mirror"], VENDOR / name)
    print("FFmpeg and mpv are ready in vendor/.")


if __name__ == "__main__":
    main()
