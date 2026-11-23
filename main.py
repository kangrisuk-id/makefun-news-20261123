#!/usr/bin/env python3
"""Entry program for the make.fun news-image-20261123 bounty.

The front-page image lives beside this file as entry.png. The program
copies it, byte for byte, to the output location the grader provides:
MAKEFUN_OUTPUT_DIR when set, otherwise /output. Standard library
only, no network, fully deterministic — two runs write the same bytes.
"""
import os
import shutil
from pathlib import Path


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        raise SystemExit("entry.png is missing beside main.py")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.read_bytes() != source.read_bytes():
        raise SystemExit("copied image does not match entry.png")


if __name__ == "__main__":
    main()
