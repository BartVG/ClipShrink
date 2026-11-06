"""Downloads the two programs ClipShrink bundles (FFmpeg and mpv) into vendor/.
They are not stored in this repository because of their size. Run by setup_dev.bat."""
import json, os, shutil, subprocess, sys, tempfile, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "vendor"
TAR = r"C:\Windows\System32\tar.exe"   # Windows' own tar also reads .zip and .7z


def latest_assets(repo):
    headers = {"User-Agent": "clipshrink-setup"}
    if os.environ.get("GITHUB_TOKEN"):      # automatic tests share an address, so need their own limit
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest", headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.load(r)["assets"]


def pick(assets, test):
    names = [a for a in assets if test(a["name"])]
    if not names:
        sys.exit("Could not find the expected download. The release layout may have changed.")
    return sorted(names, key=lambda a: a["name"])[0]


def fetch(asset, dest_dir, strip):
    dest_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        file = Path(tmp) / asset["name"]
        print(f"Downloading {asset['name']} ({asset['size'] / 1e6:.0f} MB)")
        urllib.request.urlretrieve(asset["browser_download_url"], file)
        cmd = [TAR, "-xf", str(file), "-C", str(dest_dir)]
        if strip:
            cmd.append("--strip-components=1")
        subprocess.run(cmd, check=True)


def main():
    if not (VENDOR / "ffmpeg" / "bin" / "ffmpeg.exe").exists():
        shutil.rmtree(VENDOR / "ffmpeg", ignore_errors=True)
        fetch(pick(latest_assets("BtbN/FFmpeg-Builds"),
                   lambda n: n.startswith("ffmpeg-n8.1") and n.endswith("win64-gpl-8.1.zip")), VENDOR / "ffmpeg", True)
    if not (VENDOR / "mpv" / "mpv.exe").exists():
        shutil.rmtree(VENDOR / "mpv", ignore_errors=True)
        fetch(pick(latest_assets("shinchiro/mpv-winbuild-cmake"),
                   lambda n: n.startswith("mpv-x86_64-") and "v3" not in n and "dev" not in n and n.endswith(".7z")),
              VENDOR / "mpv", False)
    print("FFmpeg and mpv are ready in vendor/.")


if __name__ == "__main__":
    main()
