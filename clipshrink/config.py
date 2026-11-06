"""Fixed rules of the tool. These numbers are the promise made to the user."""
APP_NAME = "ClipShrink"
VERSION = "1.3"
PROJECT_URL = "https://github.com/tophe323/ClipShrink"
VMAF_MEAN_MIN = 95.0     # average score over every frame
VMAF_P1_MIN = 90.0       # the worst 1% of frames must still reach this
SAMPLE_MARGIN = 0.5      # test encodes must clear the bar by this much

STATUS_TEXT = {
    "pending": "Waiting",
    "encoding": "Working…",
    "verified": "Verified",
    "below_bar": "⚠ Below the bar",
    "kept_original": "Original kept",
    "failed": "Failed, original kept",
    "original_deleted": "Original in Recycle Bin",
    "renamed": "Done, has the original's name",
}


def is_recommended(mean, p1):
    """Clears the bar. Anything else is still converted, but carries a warning."""
    return mean is not None and p1 is not None and mean >= VMAF_MEAN_MIN and p1 >= VMAF_P1_MIN


# Quality settings tried, loosest (smallest file) first. Lower = better quality.
LADDERS = {
    "x265": [26, 24, 22, 21, 20, 19, 18, 16, 14],
    "nvenc": [34, 32, 30, 29, 28, 27, 26, 24, 22],
}
VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".lrv", ".mts", ".m2ts", ".ts", ".3gp"}
GRAFT_EXTS = {".mp4", ".mov", ".m4v", ".lrv"}
SKIP_DIRS = {"$recycle.bin", "system volume information", ".tmp.drivedownload", ".tmp.driveupload"}
OUTPUT_SUFFIX = "_H265"

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
    "unchanged, and originals are never touched during conversion."
)
