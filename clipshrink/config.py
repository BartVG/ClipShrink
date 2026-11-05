"""Fixed rules of the tool. These numbers are the promise made to the user."""
APP_NAME = "ClipShrink"
VERSION = "1.1"
VMAF_MEAN_MIN = 95.0     # average score over every frame
VMAF_P1_MIN = 90.0       # the worst 1% of frames must still reach this
SAMPLE_MARGIN = 0.5      # test encodes must clear the bar by this much

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
    "GoPro originals, so it would cost you space instead of saving it. This tool uses a measured "
    "definition instead.\n\n"
    "After each conversion it compares every frame with the original using VMAF, an open measure "
    "from Netflix of how a video looks to people, scored from 0 to 100. A conversion is accepted only "
    f"if the average score is at least {VMAF_MEAN_MIN:.0f} and the worst 1% of frames score at least "
    f"{VMAF_P1_MIN:.0f}, a level where differences are very hard to see.\n\n"
    "If a file misses that bar, or the result is not smaller, your original is simply kept and "
    "the file is listed in the report. Sound, GoPro telemetry and capture dates are copied "
    "unchanged, and originals are never touched during conversion."
)
