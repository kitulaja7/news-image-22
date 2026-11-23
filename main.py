#!/usr/bin/env python3
"""news-image-20261122 entrypoint (standard library only).

The image is drawn at build time by render.py (PIL, dev-time only) and
committed as entry.png. This program just copies those exact bytes to
/output/entry.png, so both grader runs produce identical output.

No network, no third-party imports: the grader runs this in
python:3.13-slim with the standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(out_dir, "entry.png")


def main():
    dst = output_path()
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(SRC, dst)
    size = os.path.getsize(dst)
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
