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
    advanced: bool = False
    warn_mean: float = config.VMAF_MEAN_MIN
    warn_p1: float = config.VMAF_P1_MIN
    aim: bool = False
    use_minimum: bool = False
    min_mean: float = 80.0
    min_p1: float = 70.0
    skip_welcome: bool = False

    def policy(self):
        """The defaults apply until the user has unlocked the advanced values."""
        if not self.advanced:
            return config.DEFAULT_QUALITY
        return config.QualityPolicy(self.warn_mean, self.warn_p1, self.aim, self.min_mean if self.use_minimum else None,
                                    self.min_p1 if self.use_minimum else None)


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
    for key in ("show_details", "advanced", "aim", "use_minimum", "skip_welcome"):
        if isinstance(data.get(key), bool):
            setattr(out, key, data[key])
    numbers = {k: data.get(k, getattr(out, k)) for k in ("warn_mean", "warn_p1", "min_mean", "min_p1")}
    fine = all(isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v <= 100 for v in numbers.values())
    if fine and numbers["min_mean"] <= numbers["warn_mean"] and numbers["min_p1"] <= numbers["warn_p1"]:
        for k, v in numbers.items():
            setattr(out, k, float(v))
    else:                       # impossible values: back to the defaults, locked
        out.advanced = out.aim = out.use_minimum = False
    return out


def save(db_path, settings):
    path = path_for(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = Path(str(path) + ".tmp")
    tmp.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")
    os.replace(tmp, path)
