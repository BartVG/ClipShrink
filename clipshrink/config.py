"""Fixed rules of the tool. These numbers are the promise made to the user."""
APP_NAME = "ClipShrink"
VERSION = "1.5"
PROJECT_URL = "https://github.com/tophe323/ClipShrink"
VMAF_MEAN_MIN = 95.0     # average score over every frame
VMAF_P1_MIN = 90.0       # the worst 1% of frames must still reach this
SAMPLE_MARGIN = 0.5      # test encodes must clear the bar by this much

STATUS_TEXT = {
    "pending": "Waiting",
    "encoding": "Working…",
    "verified": "Verified",
    "below_bar": "⚠ Below the bar",
    "resized": "Resized",
    "kept_original": "Original kept",
    "failed": "Failed, original kept",
    "original_deleted": "Original in Recycle Bin",
    "renamed": "Done, has the original's name",
}


def status_text(rec):
    """The words shown for a record. A smaller copy never claims to be plain "Verified"."""
    if rec.status == "verified" and rec.resized:
        return STATUS_TEXT["resized"]
    return STATUS_TEXT.get(rec.status, rec.status)


def is_recommended(mean, p1):
    """Clears the bar. Anything else is still converted, but carries a warning."""
    return mean is not None and p1 is not None and mean >= VMAF_MEAN_MIN and p1 >= VMAF_P1_MIN


# Quality settings tried, loosest (smallest file) first. Lower = better quality.
LADDERS = {
    "x265": [26, 24, 22, 21, 20, 19, 18, 16, 14],
    "nvenc": [34, 32, 30, 29, 28, 27, 26, 24, 22],
    "svtav1": [42, 38, 36, 34, 32, 30, 26, 22, 18],
    "av1_nvenc": [44, 42, 40, 38, 36, 34, 32, 28, 24],
}
CODEC_NAMES = {"h265": "H.265", "av1": "AV1"}
CODEC_SUFFIX = {"h265": "_(h265)", "av1": "_(av1)"}
SIZE_SUFFIX = {"4k": "_(4k)", "1080p": "_(1080p)", "720p": "_(720p)"}
OLD_SUFFIXES = ("_H265", "_AV1")     # names used before 1.5
ENCODER_CODEC = {"x265": "h265", "nvenc": "h265", "svtav1": "av1", "av1_nvenc": "av1"}
ENCODER_NAMES = {"x265": "processor", "nvenc": "NVIDIA", "svtav1": "processor", "av1_nvenc": "NVIDIA"}
RESOLUTIONS = {"original": None, "4k": (3840, 2160), "1080p": (1920, 1080), "720p": (1280, 720)}


def output_suffix(codec, size=None):
    """What a conversion adds to its name, for example _(1080p)_(h265)."""
    return SIZE_SUFFIX.get(size, "") + CODEC_SUFFIX[codec]


def target_size(width, height, choice):
    """The size to shrink to, or None to leave it alone. Fits inside the chosen box,
    turned to match portrait video. Never upscales and never changes the shape."""
    box = RESOLUTIONS.get(choice)
    if not box or not width or not height:
        return None
    long_side, short_side = box
    box_w, box_h = (long_side, short_side) if width >= height else (short_side, long_side)
    scale = min(box_w / width, box_h / height)
    if scale >= 1:
        return None
    return (max(2, round(width * scale / 2) * 2), max(2, round(height * scale / 2) * 2))


VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".lrv", ".mts", ".m2ts", ".ts", ".3gp"}
GRAFT_EXTS = {".mp4", ".mov", ".m4v", ".lrv"}
SKIP_DIRS = {"$recycle.bin", "system volume information", ".tmp.drivedownload", ".tmp.driveupload"}

QUALITY_EXPLANATION = (
    "What \"no quality loss\" means here\n\n"
    "Truly lossless H.265, where every pixel stays identical, usually makes files larger than your "
    "the originals, so it would cost you space instead of saving it. This tool uses a measured "
    "definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure "
    "from Netflix of how a video looks to people, scored from 0 to 100. A conversion counts "
    f"as recommended if the average score is at least {VMAF_MEAN_MIN:.0f} and the worst 1% of frames score at least "
    f"{VMAF_P1_MIN:.0f}, a level where differences are very hard to see.\n\n"
    "If a file misses that bar even at the best setting, it is still converted, and it gets a warning "
    "sign so you can decide for yourself. Use Select Recommended to leave those files out when cleaning up. "
    "If the result is not smaller, your original is simply kept and the file is listed in the report. Sound, any GoPro telemetry and capture dates are copied "
    "unchanged, and originals are never touched during conversion.\n\n"
    "If you choose a smaller resolution in Settings, the conversion is compared with a smaller copy of the original "
    "at the same size. So the score shows how clean the encoding is, not the detail lost by shrinking, and those "
    "files are labelled Resized rather than Verified."
)
