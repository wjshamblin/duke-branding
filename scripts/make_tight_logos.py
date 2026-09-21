#!/usr/bin/env python3
"""Build assets/logos/tight/ from the official files in assets/logos/original/.

The official wordmark files have a built-in margin about five times Duke's required
clear space. This writes copies with the canvas trimmed to exactly the requirement
(half the width of the capital D on every side). The artwork itself is not touched:
only the SVG viewBox changes.

PNGs are rasterized from the trimmed SVGs with headless Chrome when it is installed.
Without Chrome only the SVGs are produced. Standard library only.

Usage: make_tight_logos.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LOGOS = Path(__file__).resolve().parent.parent / "assets" / "logos"
D_WIDTH = 75.2          # capital D in SVG units: Duke's "x"
PAD = D_WIDTH / 2       # required clear space is 0.5x
# Artwork bounds (x0, y0, x1, y1) in the official 612 x 301.1 canvas.
ART = {
    "duke_wordmark": (195.3, 113.6, 417.8, 190.2),
    "duke_university_wordmark": (195.3, 92.1, 417.8, 187.9),
}
PNG_SCALE = 5           # matches the official PNGs: 5 px per SVG unit
CHROME_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome", "chromium", "chromium-browser",
]


def find_chrome():
    for candidate in CHROME_PATHS:
        if Path(candidate).exists() or shutil.which(candidate):
            return candidate
    return None


def main():
    originals = sorted((LOGOS / "original").glob("*.svg"))
    if not originals:
        sys.exit(f"error: no SVG files in {LOGOS / 'original'} - download them first (see assets/logos/README.md)")
    tight = LOGOS / "tight"
    tight.mkdir(exist_ok=True)
    chrome = find_chrome()

    for src in originals:
        key = "duke_university_wordmark" if src.name.startswith("duke_university") else "duke_wordmark"
        x0, y0, x1, y1 = ART[key]
        width, height = (x1 - x0) + 2 * PAD, (y1 - y0) + 2 * PAD
        view_box = f'viewBox="{x0 - PAD:.1f} {y0 - PAD:.1f} {width:.1f} {height:.1f}"'

        svg, count = re.subn(r'viewBox="[^"]*"', view_box, src.read_text(), count=1)
        if count != 1:
            sys.exit(f"error: no viewBox found in {src.name}")
        svg = re.sub(r'\s*enable-background="[^"]*"', "", svg, count=1)
        dst = tight / src.name
        dst.write_text(svg)

        if chrome:
            w, h = round(width * PNG_SCALE), round(height * PNG_SCALE)
            with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as page:
                page.write(f"<html><body style='margin:0;background:transparent'>"
                           f"<img src='file://{dst}' style='display:block;width:{w}px;height:{h}px'></body></html>")
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--allow-file-access-from-files", "--default-background-color=00000000",
                            f"--window-size={w},{h}", f"--screenshot={dst.with_suffix('.png')}",
                            f"file://{page.name}"], capture_output=True, check=False)
            Path(page.name).unlink()
        print(f"{dst.name}{'  + png' if chrome else ''}")

    if not chrome:
        print("note: Chrome not found, so no PNGs were made. SVGs are complete.")


if __name__ == "__main__":
    main()
