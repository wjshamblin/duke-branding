#!/usr/bin/env python3
"""Resolve Duke brand tokens, optionally layered with a group profile.

Usage:
  duke_brand.py groups
  duke_brand.py logos                 (where the official wordmark files are, if anywhere)
  duke_brand.py tokens [--group SLUG] [--theme alternate|primary] [--format json|css]
  duke_brand.py contrast FG BG [FG BG ...]   (palette names such as cast-iron, or hex values)
  duke_brand.py render TEMPLATE [--group SLUG] [--theme ...]   fill {{placeholders}} in an inline-style template

Group profiles are looked up in ./.duke-branding/groups/ first, then in the
skill's own groups/ folder. Standard library only.
"""
import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TOKENS = json.loads((SKILL_DIR / "assets" / "duke-tokens.json").read_text())
PALETTE = TOKENS["palette"]
GROUP_DIRS = [Path.cwd() / ".duke-branding" / "groups", SKILL_DIR / "groups"]
# Wordmarks live outside the skill when the skill was installed from git (no trademarks in git).
LOGO_DIRS = [Path.cwd() / ".duke-branding" / "logos", Path.home() / ".duke-branding" / "logos",
             SKILL_DIR / "assets" / "logos" / "tight"]
COLOR_KEYS = ["base", "accent", "accent_2", "highlight", "text", "text_muted",
              "background", "background_alt", "background_warm", "border", "link"]


def to_hex(value):
    """Accept a palette name or a hex string; return (hex, is_duke_color)."""
    if value in PALETTE:
        return PALETTE[value], True
    hex_value = value.upper() if value.startswith("#") else "#" + value.upper()
    if len(hex_value) != 7:
        sys.exit(f"error: '{value}' is not a Duke palette name or a #RRGGBB hex value")
    return hex_value, hex_value in PALETTE.values()


def luminance(hex_value):
    channels = [int(hex_value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast(fg, bg):
    lighter, darker = sorted([luminance(fg), luminance(bg)], reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def rating(ratio):
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA18 (large text only: 18pt+, or 14pt+ bold)"
    return "FAIL (decorative use only)"


def find_group(slug):
    for directory in GROUP_DIRS:
        path = directory / slug / "group.json"
        if path.exists():
            return path
    searched = ", ".join(str(d) for d in GROUP_DIRS)
    sys.exit(f"error: no group profile '{slug}' (looked in {searched})")


def load_group(slug, seen=()):
    """Load a profile and merge it over its parent chain. Child values win."""
    if slug in seen:
        sys.exit(f"error: group parent loop: {' -> '.join(seen + (slug,))}")
    path = find_group(slug)
    profile = {k: v for k, v in json.loads(path.read_text()).items() if not k.startswith("_")}

    # Logo paths are relative to the profile that declares them.
    logos = {k: str(path.parent / v) for k, v in (profile.get("logo") or {}).items() if v}
    profile["logo"] = logos

    parent_slug = profile.pop("parent", None)
    if not parent_slug:
        profile["lineage"] = [slug]
        return profile

    merged = load_group(parent_slug, seen + (slug,))
    lineage = merged["lineage"] + [slug]
    for key, value in profile.items():
        if value in (None, "", {}, []):
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    merged["lineage"] = lineage
    return merged


IN_SANDBOX = Path.home() == Path("/root") or str(SKILL_DIR).startswith("/mnt/")


def wordmark_dir():
    """First folder that holds an official wordmark file, or None.

    In a hosted sandbox (Claude Desktop, claude.ai, ChatGPT) the user's own machine is out
    of reach, so the only other place the files can be is a folder the user connected or
    attached, mounted somewhere under /mnt. Search that, shallowly, before giving up."""
    for directory in LOGO_DIRS:
        if list(directory.glob("duke_wordmark_*.svg")) or list(directory.glob("duke_wordmark_*.png")):
            return directory
    if IN_SANDBOX and Path("/mnt").exists():
        for depth in range(1, 6):
            for hit in Path("/mnt").glob("/".join(["*"] * depth) + "/duke_wordmark_*.*"):
                if "/mnt/skills" not in str(hit) and hit.suffix in (".svg", ".png"):
                    return hit.parent
    return None


MISSING_WORDMARKS = """No official Duke wordmark files are available to this copy of the skill.
Say so in the FIRST line of the reply, then offer the user these, in order:
  1. Attach the file to this chat: duke_wordmark_white.png for a dark background,
     duke_wordmark_navyblue_012169.png for a light one. Download (Duke NetID):
     https://brand.duke.edu/logos/#downloads
  2. Claude Desktop / Cowork: connect a folder that holds the files (Add folder).
     A machine set up with the installer has them in ~/.duke-branding/logos.
  3. On a machine with a shell (Claude Code, a terminal), install them once:
     python3 scripts/install_wordmarks.py ~/Downloads/duke_wordmark.zip
Until then use a labelled placeholder. Never redraw, type or generate the wordmark."""


def resolve(group_slug, theme_name):
    warnings = []
    group = load_group(group_slug) if group_slug else None
    theme_name = theme_name or (group or {}).get("theme") or "alternate"
    if theme_name not in TOKENS["themes"]:
        sys.exit(f"error: unknown theme '{theme_name}' (choose: {', '.join(TOKENS['themes'])})")
    theme = dict(TOKENS["themes"][theme_name])
    theme.pop("description")

    if group:
        for key in ("accent", "accent_2", "highlight"):
            if group.get(key):
                theme[key] = group[key]
        if group.get("base"):
            if group["base"] not in ("navy", "royal"):
                sys.exit("error: group base must be 'navy' or 'royal': every piece needs a Duke blue as its base")
            theme["base"] = group["base"]
        for key, font_key in (("heading", "heading_font"), ("body", "body_font")):
            if (group.get("fonts") or {}).get(key):
                theme[font_key] = group["fonts"][key]
        for kind, logo_path in group["logo"].items():
            if not Path(logo_path).exists():
                warnings.append(f"logo '{kind}' not found at {logo_path} - use the text lockup instead")
        if not group["logo"]:
            warnings.append("group has no logo files - use the text lockup (see references/group-branding.md)")

    colors = {}
    for key in COLOR_KEYS:
        colors[key], is_duke = to_hex(theme[key])
        if not is_duke:
            warnings.append(f"{key} {colors[key]} is outside the Duke palette - confirm the group is approved to use it")

    white = PALETTE["white"]
    on_accent = white if contrast(white, colors["accent"]) >= 4.5 else PALETTE["cast-iron"]
    colors["on_accent"] = on_accent
    if on_accent != white:
        warnings.append(f"white text fails on accent {colors['accent']} - dark text is used on accent fills")
    # The accent is used two ways: on the blue band (rules, unit name) and on white (small labels).
    colors["accent_on_base"] = colors["accent"] if contrast(colors["accent"], colors["base"]) >= 4.5 else white
    # Borders and rules on white are UI components: WCAG asks 3:1, not the 4.5:1 of text.
    colors["rule_on_white"] = colors["highlight"] if contrast(colors["highlight"], colors["background"]) >= 3 else colors["base"]
    colors["accent_text"] = colors["accent"]
    if contrast(colors["accent"], colors["background"]) < 4.5:
        colors["accent_text"] = colors["base"]
        warnings.append(f"accent {colors['accent']} on {colors['background']} is below AA - headings 18pt+ and decoration only, never body text or small links")

    fonts = {}
    for role, family in (("heading", theme["heading_font"]), ("body", theme["body_font"])):
        info = TOKENS["fonts"].get(family)
        if not info:
            warnings.append(f"{role} font '{family}' is not an official Duke typeface")
            info = {"fallback": "Georgia, serif" if role == "heading" else "Arial, sans-serif",
                    "office_fallback": "Georgia" if role == "heading" else "Arial"}
        fonts[role] = {"family": family, "css_stack": f"'{family}', {info['fallback']}",
                       "office_fallback": info["office_fallback"]}

    logos = wordmark_dir()
    if logos is None:
        warnings.append(MISSING_WORDMARKS.replace("\n", " "))
    return {"theme": theme_name, "colors": colors, "fonts": fonts, "wordmarks": str(logos) if logos else None,
            "group": group, "warnings": warnings}


def as_css(tokens):
    c, f = tokens["colors"], tokens["fonts"]
    label = tokens["group"]["name"] if tokens["group"] else "Duke"
    lines = [
        f"/* {label} - {tokens['theme']} theme. Paste AFTER duke-alternate.css. */",
        ":root {",
        f"  --duke-accent:      {c['accent']};",
        f"  --duke-accent-2:    {c['accent_2']};",
        f"  --duke-accent-text: {c['accent_text']};",
        f"  --duke-base:        {c['base']};",
        f"  --duke-accent-on-base: {c['accent_on_base']};",
        f"  --duke-highlight:   {c['highlight']};",
        f"  --duke-on-accent:   {c['on_accent']};",
        f"  --duke-bg-warm:     {c['background_warm']};",
        f"  --duke-link:        {c['link']};",
        f"  --duke-link-hover:  {c['accent_text']};",
        f"  --duke-font-serif:  {f['heading']['css_stack']};",
        f"  --duke-font-sans:   {f['body']['css_stack']};",
        "}",
    ]
    return "\n".join(lines)


PREPOSITIONS = {"of", "the", "for", "and", "in", "at"}


def render(template, tokens):
    """Fill {{name}} placeholders in an inline-style template (Canvas, email).

    Stylesheets and CSS variables are stripped by those hosts, so colors must be literal.
    Named placeholders keep each role separate even when two roles share a hex value."""
    group = tokens["group"] or {}
    lines = (group.get("lockup") or {}).get("lines") or [group.get("name", "Unit name")]
    words = " ".join(lines).split()
    values = dict(tokens["colors"])
    values["unit_caps"] = " ".join(f"<em>{w.lower()}</em>" if w.lower() in PREPOSITIONS else w.upper() for w in words)
    values["unit_name"] = group.get("name", "[Unit name]")
    values["footer"] = group.get("footer", "[Unit] · Duke University")
    text = Path(template).read_text()
    unknown = sorted(set(re.findall(r"{{(\w+)}}", text)) - set(values))
    if unknown:
        sys.exit(f"error: template uses unknown placeholders: {unknown}. Known: {sorted(values)}")
    return re.sub(r"{{(\w+)}}", lambda m: values[m.group(1)], text)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("groups")
    sub.add_parser("logos")
    p_tokens = sub.add_parser("tokens")
    p_tokens.add_argument("--group")
    p_tokens.add_argument("--theme")
    p_tokens.add_argument("--format", choices=["json", "css"], default="json")
    p_contrast = sub.add_parser("contrast")
    p_contrast.add_argument("pairs", nargs="+", metavar="COLOR", help="FG BG [FG BG ...]")
    p_render = sub.add_parser("render")
    p_render.add_argument("template")
    p_render.add_argument("--group")
    p_render.add_argument("--theme")
    args = parser.parse_args()

    if args.command == "groups":
        found = {}
        for directory in reversed(GROUP_DIRS):  # project-local entries override skill entries
            for path in sorted(directory.glob("*/group.json")):
                if not path.parent.name.startswith("_"):
                    found[path.parent.name] = path
        for slug, path in sorted(found.items()):
            data = json.loads(path.read_text())
            parent = f"  (parent: {data['parent']})" if data.get("parent") else ""
            print(f"{slug:24} {data.get('name', '')}{parent}")
    elif args.command == "logos":
        directory = wordmark_dir()
        if directory is None:
            looked = "\n  ".join(str(d) for d in LOGO_DIRS) + ("\n  /mnt/** (connected or attached folders)" if IN_SANDBOX else "")
            sys.exit(f"Looked in:\n  {looked}\n\n{MISSING_WORDMARKS}")
        print(directory)
        for f in sorted(directory.iterdir()):
            if f.suffix in (".svg", ".png"):
                print(f"  {f.name}")
    elif args.command == "contrast":
        if len(args.pairs) % 2:
            sys.exit("error: give colors in pairs: FG BG [FG BG ...]")
        for fg_name, bg_name in zip(args.pairs[::2], args.pairs[1::2]):
            fg, bg = to_hex(fg_name)[0], to_hex(bg_name)[0]
            ratio = contrast(fg, bg)
            print(f"{fg} on {bg}: {ratio:.2f}:1  {rating(ratio)}")
    elif args.command == "render":
        tokens = resolve(args.group, args.theme)
        for warning in tokens["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        print(render(args.template, tokens))
    else:
        tokens = resolve(args.group, args.theme)
        for warning in tokens["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
        print(as_css(tokens) if args.format == "css" else json.dumps(tokens, indent=2))


if __name__ == "__main__":
    main()
