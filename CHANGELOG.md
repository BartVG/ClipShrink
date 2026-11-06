# Changelog

## 1.3 - 2026-11-06

### Changed
- **Below the bar no longer blocks a conversion.** A file that can't reach VMAF average 95 and worst 1% 90 at the best setting is still converted, and gets a warning sign. Its original stays until you choose otherwise, and removing it needs an extra confirmation. A result that isn't smaller still keeps the original.
- The automatic report replaces the Save report button.

### Added
- A report is kept automatically for every batch, in a reports folder.
- **Reports & Statistics** page: space saved since you started using the app, average file reduction and more, with reports you can export as CSV, XLSX or PDF, or delete.
- **About** page.
- **Select All** and **Select Recommended** buttons on the Compare and clean up page.
- Click any column title to sort, by its real value.
- A Folder column showing where each file is.
- Progress bars while deleting and renaming.

### Removed
- The Google Drive trash warnings.

## 1.2 - 2026-11-05

### Changed
- The app's wording now covers any H.264 video, not only GoPro files.
- The Google Drive warning now says it applies only to videos stored in Drive.

### Fixed
- The Convert page no longer says "1 videos".
- If the video player stops unexpectedly, the app now shows a message instead of an error crash.

## 1.1 - 2026-11-05

First public release.

### Added
- H.265 and other non-H.264 videos are listed on the Find videos page, greyed out and marked as skipped.
- **Remove _H265 from names** gives a conversion its original's name once the original is in the Recycle Bin.
- The version number shows in the window title.

### Fixed
- Windows dark theme hid tick boxes, the selected row and the report text. The app now always uses its light look.
- Clicking anywhere in a tick box's cell now ticks it.

## 1.0 - 2026-11-05

Private first version: scan, sample-based savings estimate, batch conversion with pause and crash recovery, VMAF verification, side by side playback and Recycle Bin cleanup.
