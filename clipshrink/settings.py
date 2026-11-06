"""The few choices a user can make, kept in a small file beside the app's data."""
import json, os
from dataclasses import asdict, dataclass
from pathlib import Path
from . import config

CHOICES = {
    "hardware": ("gpu", "cpu"),
    "codec": ("h265", "av1"),
    "max_resolution": tuple(config.RESOLUTIONS),
}


@dataclass
class Settings:
    hardware: str = "gpu"
    codec: str = "h265"
    max_resolution: str = "original"
    show_details: bool = False


def path_for(db_path):
    return Path(db_path).parent / "settings.json"


def load(db_path):
    """A missing or damaged file, or an unknown value, simply means the default."""
    out = Settings()
    try:
        data = json.loads(path_for(db_path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return out
    if not isinstance(data, dict):
        return out
    for key, allowed in CHOICES.items():
        if data.get(key) in allowed:
            setattr(out, key, data[key])
    if isinstance(data.get("show_details"), bool):
        out.show_details = data["show_details"]
    return out


def save(db_path, settings):
    path = path_for(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")
    os.replace(tmp, path)
