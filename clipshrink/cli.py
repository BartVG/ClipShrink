"""Headless batch, used by the check to test a real crash."""
import argparse, sys
from .engine import Converter
from .scan import scan_folder


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("convert")
    c.add_argument("folder")
    c.add_argument("--db", required=True)
    c.add_argument("--work", required=True)
    c.add_argument("--encoder", default="auto")
    a = ap.parse_args(argv)
    files = scan_folder(a.folder).h264
    conv = Converter(a.db, a.work, encoder=a.encoder)
    conv.add_files([f.path for f in files])
    print(conv.run())
    return 0


if __name__ == "__main__":
    sys.exit(main())
