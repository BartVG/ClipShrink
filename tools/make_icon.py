"""Builds assets/clipshrink.ico from the artwork: cuts out the rounded square,
makes the corners transparent and stores every size Windows asks for.
Usage: python tools/make_icon.py path/to/artwork.jpg"""
import struct, sys
from pathlib import Path
from PySide6.QtCore import QBuffer, QIODevice, QRectF, Qt
from PySide6.QtGui import QGuiApplication, QImage, QPainter, QPainterPath

# Where the rounded square sits, as a share of the artwork's width and height
LEFT, TOP, RIGHT, BOTTOM = 0.1885, 0.1835, 0.8125, 0.8115
CORNER = 0.17       # corner radius, as a share of the square's side
SIZES = (256, 128, 64, 48, 32, 24, 16)
ROOT = Path(__file__).resolve().parents[1]


def cut_out(art):
    w, h = art.width(), art.height()
    side = round(((RIGHT - LEFT) * w + (BOTTOM - TOP) * h) / 2)
    square = art.copy(round(LEFT * w), round(TOP * h), side, side)
    out = QImage(side, side, QImage.Format_ARGB32_Premultiplied)
    out.fill(Qt.transparent)
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing)
    clip = QPainterPath()
    clip.addRoundedRect(QRectF(0, 0, side, side), side * CORNER, side * CORNER)
    p.setClipPath(clip)
    p.drawImage(0, 0, square)
    p.end()
    return out


def png_bytes(img):
    buf = QBuffer()
    buf.open(QIODevice.WriteOnly)
    img.save(buf, "PNG")
    return bytes(buf.data())


def main(path):
    app = QGuiApplication([])
    art = QImage(str(path))
    if art.isNull():
        sys.exit(f"Could not read {path}")
    icon = cut_out(art)
    pngs = [png_bytes(icon.scaled(s, s, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)) for s in SIZES]
    folder = ROOT / "assets"
    folder.mkdir(exist_ok=True)
    offset = 6 + 16 * len(SIZES)
    with open(folder / "clipshrink.ico", "wb") as f:
        f.write(struct.pack("<HHH", 0, 1, len(SIZES)))
        for s, data in zip(SIZES, pngs):
            f.write(struct.pack("<BBBBHHII", s % 256, s % 256, 0, 0, 1, 32, len(data), offset))
            offset += len(data)
        for data in pngs:
            f.write(data)
    icon.scaled(512, 512, Qt.IgnoreAspectRatio, Qt.SmoothTransformation).save(str(folder / "clipshrink.png"))
    del app


if __name__ == "__main__":
    main(sys.argv[1])
