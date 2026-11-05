import os, shutil, sys
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests"))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from helpers.clips import make_clip  # noqa: E402

REAL_DIR = ROOT / "tests" / "real_clip"
CLIP_SPECS = {
    "gopro_like_1080p_telemetry": dict(w=1920, h=1080, fps="30", seconds=4),
    "fullrange_60fps_telemetry": dict(w=1280, h=720, fps="60000/1001", seconds=4, full_range=True),
    "uhd_4k_telemetry": dict(w=3840, h=2160, fps="30", seconds=2, preset="veryfast"),
    "rotated_telemetry": dict(w=1280, h=720, fps="30", seconds=3, rotate=90),
    "no_audio_no_telemetry": dict(w=640, h=360, fps="25", seconds=3, audio=False, telemetry=False, timecode=False),
    "variable_framerate": dict(w=640, h=360, fps="30", seconds=4, vfr=True, telemetry=False, timecode=False),
}


def real_clips():
    return sorted(p for p in REAL_DIR.glob("*") if p.suffix.lower() in (".mp4", ".mov"))


@pytest.fixture(scope="session")
def clip_cache(tmp_path_factory):
    return tmp_path_factory.mktemp("clips")


@pytest.fixture(scope="session")
def get_clip(clip_cache):
    def _get(name):
        p = clip_cache / f"{name}.mp4"
        if not p.exists():
            make_clip(p, **CLIP_SPECS[name])
        return p
    return _get


@pytest.fixture
def workspace(tmp_path):
    (tmp_path / "videos").mkdir()
    (tmp_path / "work").mkdir()
    return tmp_path


def copy_preserving(src, dst):
    from helpers.media import get_times, set_times
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    c, m = get_times(src)
    set_times(dst, c, m)
    return Path(dst)
