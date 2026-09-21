#!/usr/bin/env python3
"""Audit a .pptx against Duke brand rules, or write the Duke theme into one.

Usage:
  pptx_tools.py audit DECK.pptx
  pptx_tools.py theme DECK.pptx [--group SLUG] [--theme alternate|primary]

audit  reports: theme in use, fonts, off-palette colors, low-contrast text on filled
       shapes, slides without a real title, duplicate titles, pictures without alt
       text, small text, and whether a Duke wordmark is present and large enough.
theme  rewrites the file's theme colors and fonts in place, so PowerPoint's pickers
       and hyperlinks are on-brand. It does not restyle existing shapes.

Reads the .pptx as a zip of XML. Standard library only, no python-pptx needed.
"""
import argparse
import re
import shutil
import sys
import zipfile
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent))
import duke_brand  # noqa: E402

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
PALETTE = {v.upper(): k for k, v in duke_brand.PALETTE.items()}
OFFICIAL_FONTS = set(duke_brand.TOKENS["fonts"])
FALLBACK_FONTS = {"Arial", "Helvetica", "Helvetica Neue", "Consolas", "Menlo"}
EMU_PER_INCH = 914400
MIN_WORDMARK_IN = 0.82      # tight wordmark image: makes the capital D 3/8 in tall


def parse(data):
    """Parse OOXML safely. Office XML never carries a DTD, so refuse any that does:
    that shuts out external-entity (XXE) and entity-expansion attacks from a hostile file."""
    if b"<!DOCTYPE" in data or b"<!ENTITY" in data:
        sys.exit("error: XML contains a DTD or entity declaration, refusing to parse")
    return ET.fromstring(data)


def slide_files(z):
    names = [n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
    return sorted(names, key=lambda n: int(re.search(r"\d+", n.split("/")[-1]).group()))


def family(typeface):
    """'Open Sans SemiBold' -> 'Open Sans': weight names are part of the family."""
    for name in sorted(OFFICIAL_FONTS | FALLBACK_FONTS, key=len, reverse=True):
        if typeface == name or typeface.startswith(name + " "):
            return name
    return typeface


def audit(path):
    problems, notes = [], []
    with zipfile.ZipFile(path) as z:
        theme = z.read("ppt/theme/theme1.xml").decode("utf-8")
        match = re.search(r'<a:clrScheme name="([^"]*)"', theme)
        scheme = match.group(1) if match else "unknown"
        theme_fonts = re.findall(r'<a:(?:major|minor)Font>\s*<a:latin typeface="([^"]*)"', theme)
        if scheme.lower().startswith("office"):
            problems.append(f"theme is the default '{scheme}' scheme: run `pptx_tools.py theme` so pickers and hyperlinks are on-brand")
        notes.append(f"theme '{scheme}', theme fonts {theme_fonts}")

        fonts, colors, titles, small, where = Counter(), Counter(), [], Counter(), {}
        wordmarks = []
        for number, name in enumerate(slide_files(z), 1):
            root = parse(z.read(name))
            # The slide's own background fill, then shapes in z-order with bounds and solid fill.
            bgc = root.find("p:cSld/p:bg/p:bgPr/a:solidFill/a:srgbClr", NS)
            slide_bg = "#" + bgc.get("val", "FFFFFF") if bgc is not None else "#FFFFFF"
            layers = []
            for sp in root.iter(f"{{{NS['p']}}}sp"):
                off, ext = sp.find("p:spPr/a:xfrm/a:off", NS), sp.find("p:spPr/a:xfrm/a:ext", NS)
                fillc = sp.find("p:spPr/a:solidFill/a:srgbClr", NS)
                box = (int(off.get("x", 0)), int(off.get("y", 0)), int(ext.get("cx", 0)), int(ext.get("cy", 0))) if off is not None and ext is not None else None
                layers.append((sp, box, "#" + fillc.get("val", "") if fillc is not None else None))

            def backdrop(shape):
                """Fill of the nearest shape beneath this one that covers its center. None if unknown."""
                index = next(i for i, (sp, _, _) in enumerate(layers) if sp is shape)
                box = layers[index][1]
                if box is None:
                    return None                         # position inherited from the layout: cannot tell
                cx, cy = box[0] + box[2] / 2, box[1] + box[3] / 2
                for _, under, fill in reversed(layers[:index]):
                    if fill and under and under[0] <= cx <= under[0] + under[2] and under[1] <= cy <= under[1] + under[3]:
                        return fill
                return slide_bg

            title = None
            for sp in root.iter(f"{{{NS['p']}}}sp"):
                ph = sp.find("p:nvSpPr/p:nvPr/p:ph", NS)
                if ph is not None and ph.get("type") in ("title", "ctrTitle"):
                    title = "".join(t.text or "" for t in sp.iter(f"{{{NS['a']}}}t")).strip()
            if not title:
                problems.append(f"slide {number}: no real title (a text box is not a title for screen readers or outline view)")
            titles.append(title)

            for pic in root.iter(f"{{{NS['p']}}}pic"):
                props = pic.find("p:nvPicPr/p:cNvPr", NS)
                descr = (props.get("descr") or "").strip() if props is not None else ""
                if not descr:
                    label = props.get("name") if props is not None else "unnamed"
                    problems.append(f"slide {number}: picture '{label}' has no alt text")
                elif re.fullmatch(r"[\w .()-]+\.(png|jpe?g|gif|svg|bmp|tiff?)", descr, re.I):
                    problems.append(f"slide {number}: alt text '{descr}' is just a file name: describe what the picture shows")
                ext = pic.find("p:spPr/a:xfrm/a:ext", NS)
                if descr.lower() in ("duke", "duke university") and ext is not None:
                    wordmarks.append((number, int(ext.get("cy", "0")) / EMU_PER_INCH))

            for clr in root.iter(f"{{{NS['a']}}}srgbClr"):
                where.setdefault("#" + clr.get("val", "").upper(), set()).add(number)
            for latin in root.iter(f"{{{NS['a']}}}latin"):
                fonts[family(latin.get("typeface", ""))] += 1
            for clr in root.iter(f"{{{NS['a']}}}srgbClr"):
                colors["#" + clr.get("val", "").upper()] += 1

            for sp in root.iter(f"{{{NS['p']}}}sp"):
                fill = sp.find("p:spPr/a:solidFill/a:srgbClr", NS)
                props = sp.find("p:nvSpPr/p:cNvPr", NS)
                name = props.get("name", "shape") if props is not None else "shape"
                for r in sp.iter(f"{{{NS['a']}}}r"):
                    words = "".join(t.text or "" for t in r.iter(f"{{{NS['a']}}}t")).strip()
                    run = r.find("a:rPr", NS)
                    if not words or run is None:
                        continue                        # empty runs are invisible: nothing to judge
                    size = int(run.get("sz", "1800")) / 100
                    if size < 14:
                        small[number] += 1
                    if size >= 28 and words.lower() in ("duke", "duke university"):
                        problems.append(f"slide {number}: '{words}' typed as text at {size:g}pt in '{name}' looks like a hand-made wordmark: use the official file")
                    fg = run.find("a:solidFill/a:srgbClr", NS)
                    if fg is None:
                        continue
                    # No fill of its own: judge against whatever filled shape lies underneath it.
                    bg, sure = ("#" + fill.get("val", ""), True) if fill is not None else (backdrop(sp), False)
                    if bg is None:
                        continue
                    ratio = duke_brand.contrast("#" + fg.get("val", ""), bg)
                    large = size >= 18 or (size >= 14 and run.get("b") == "1")
                    if ratio < (3 if large else 4.5):
                        on = "fill" if sure else "(the shape beneath it, or the slide background)"
                        problems.append(f"slide {number}: #{fg.get('val')} text on {bg} {on} is {ratio:.1f}:1 at {size:g}pt in '{name}': \"{words[:28]}\"")

        for title, count in Counter(t for t in titles if t).items():
            if count > 1:
                problems.append(f"title '{title}' is used on {count} slides: titles should be unique")

        for font in sorted(fonts):
            if font in OFFICIAL_FONTS:
                continue
            kind = "an accepted fallback" if font in FALLBACK_FONTS else "NOT a Duke typeface"
            (notes if font in FALLBACK_FONTS else problems).append(f"font '{font}' ({fonts[font]} runs) is {kind}")
        notes.append("Duke fonts in use: " + (", ".join(f for f in sorted(fonts) if f in OFFICIAL_FONTS) or "none"))

        off = {c: n for c, n in colors.items() if c not in PALETTE}
        for color, count in sorted(off.items(), key=lambda kv: -kv[1]):
            problems.append(f"color {color} ({count} uses, slides {sorted(where.get(color, []))}) is outside the Duke palette")
        if not any(PALETTE.get(c) in ("navy", "royal") for c in colors):
            problems.append("no Duke Navy or Royal anywhere: at least one Duke blue is required")
        notes.append(f"{len(colors) - len(off)} palette colors in use, {len(off)} off-palette")

        if not wordmarks:
            problems.append("no Duke wordmark found (looked for a picture with alt text 'Duke'): expected on title, divider and closing slides")
        for number, height in wordmarks:
            state = "ok" if height >= MIN_WORDMARK_IN else f"TOO SMALL, minimum {MIN_WORDMARK_IN} in for a tight/ file"
            (notes if height >= MIN_WORDMARK_IN else problems).append(f"slide {number}: wordmark image {height:.2f} in tall ({state})")

        if small:
            worst = ", ".join(f"{n} ({c})" for n, c in small.most_common(6))
            notes.append(f"text under 14pt on {len(small)} slides, most on: {worst}. Fine for footers, code and source notes. "
                         "Otherwise flag it to the author: resizing reflows layouts, so do not change it silently")

    problems = list(dict.fromkeys(problems))            # same finding on several runs: say it once
    print(f"{path}: {len(titles)} slides")
    for line in notes:
        print(f"  note     {line}")
    for line in problems:
        print(f"  PROBLEM  {line}")
    print(f"{len(problems)} problem(s)")
    return 1 if problems else 0


def apply_theme(path, group, theme_name):
    tokens = duke_brand.resolve(group, theme_name)      # warnings belong to `tokens`; repeating them on every build is noise
    c, p = tokens["colors"], duke_brand.PALETTE
    slots = {"dk1": c["text"], "lt1": c["background"], "dk2": c["base"], "lt2": c["background_alt"],
             "accent1": c["accent"], "accent2": c["accent_2"], "accent3": c["highlight"],
             "accent4": p["prussian"], "accent5": p["magnolia"], "accent6": p["ironweed"],
             "hlink": c["link"], "folHlink": p["ironweed"]}
    scheme = '<a:clrScheme name="Duke">' + "".join(
        f'<a:{slot}><a:srgbClr val="{value.lstrip("#")}"/></a:{slot}>' for slot, value in slots.items()) + "</a:clrScheme>"
    fonts = (("majorFont", tokens["fonts"]["heading"]["family"]), ("minorFont", tokens["fonts"]["body"]["family"]))

    tmp = Path(str(path) + ".tmp")
    with zipfile.ZipFile(path) as src, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as dst:
        for item in src.infolist():
            data = src.read(item.filename)
            if re.fullmatch(r"ppt/theme/theme\d+\.xml", item.filename):
                xml = re.sub(r"<a:clrScheme .*?</a:clrScheme>", scheme, data.decode("utf-8"), flags=re.S)
                for block, font in fonts:
                    xml = re.sub(rf'(<a:{block}>\s*<a:latin typeface=")[^"]*', rf"\g<1>{font}", xml)
                data = xml.encode("utf-8")
            dst.writestr(item, data)
    shutil.move(tmp, path)
    print(f"{path}: Duke theme applied ({tokens['theme']}, accent {c['accent']}, {fonts[0][1]} + {fonts[1][1]})")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("audit").add_argument("deck")
    p_theme = sub.add_parser("theme")
    p_theme.add_argument("deck")
    p_theme.add_argument("--group")
    p_theme.add_argument("--theme")
    args = parser.parse_args()
    if not Path(args.deck).exists():
        sys.exit(f"error: {args.deck} not found")
    if args.command == "audit":
        sys.exit(audit(args.deck))
    apply_theme(args.deck, args.group, args.theme)


if __name__ == "__main__":
    main()
