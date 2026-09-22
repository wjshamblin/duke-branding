#!/usr/bin/env python3
"""Install the official Duke wordmark files where every copy of this skill can find them.

Usage:
  install_wordmarks.py SOURCE [SOURCE ...] [--to DIR]

SOURCE is an official zip from https://brand.duke.edu/logos/#downloads (duke_wordmark.zip,
duke_wordmark-with_university.zip) or a folder that already holds the digital RGB SVG
files. The default destination is ~/.duke-branding/logos/, a folder outside the skill, so
the files survive marketplace updates and serve every install of the skill on this machine.

The skill looks for wordmarks in: ./.duke-branding/logos, ~/.duke-branding/logos, then its
own assets/logos/tight. Run `duke_brand.py logos` to see which one is in use.
Standard library only; PNG rasterizing needs Chrome, SVGs are written regardless.
"""
import argparse
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_tight_logos import build_tight, find_chrome  # noqa: E402

DEFAULT = Path.home() / ".duke-branding" / "logos"


def collect(source, into):
    """Copy every digital-RGB wordmark SVG from a zip or folder into `into`."""
    source = Path(source).expanduser()
    if not source.exists():
        sys.exit(f"error: {source} not found")
    if source.suffix == ".zip":
        with zipfile.ZipFile(source) as z:
            names = [n for n in z.namelist() if n.endswith(".svg") and "digital_rgb" in n and "__MACOSX" not in n]
            for n in names:
                (into / Path(n).name).write_bytes(z.read(n))
            return len(names)
    found = list(source.glob("duke_*wordmark*.svg"))
    for f in found:
        shutil.copy(f, into / f.name)
    return len(found)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("sources", nargs="+")
    parser.add_argument("--to", default=str(DEFAULT))
    args = parser.parse_args()
    dest = Path(args.to).expanduser()
    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp)
        total = sum(collect(s, staged) for s in args.sources)
        if not total:
            sys.exit("error: no wordmark SVGs found. Expected the official zip, or a folder of duke_wordmark_*.svg files")
        written = build_tight(staged, dest, find_chrome())
    print(f"{len(written)} files written to {dest}")
    if not find_chrome():
        print("note: Chrome not found, so SVGs only (fine for web and PDF; PowerPoint needs PNG)")


if __name__ == "__main__":
    main()
