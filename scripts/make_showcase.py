#!/usr/bin/env python3
"""Build the visual showcase: palette, themes, type pairings, lockups and every group.

Writes assets/showcase/showcase.html (self-contained) and, when Chrome is installed,
showcase.png and showcase.pdf beside it. Show the PNG or PDF to a user who is choosing
a theme, an accent or a group look, instead of describing hex codes.

Re-run after adding or editing a group. Standard library only.
Usage: make_showcase.py
"""
import base64
import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import duke_brand as db  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
OUT = SKILL / "assets" / "showcase"
CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium", "chromium-browser"]
EXTENDED = ["copper", "persimmon", "dandelion", "piedmont", "eno", "magnolia", "prussian", "shale", "ironweed"]
NEUTRALS = ["cast-iron", "graphite", "granite", "limestone", "whisper", "hatteras", "ginger-beer", "shackleford", "dogwood"]
PAIRINGS = [("EB Garamond", "Open Sans", "Classic Duke editorial. primary theme"), ("Playfair Display", "Open Sans", "Sharp, magazine-like. alternate theme"),
            ("Merriweather", "Open Sans", "What most Duke units use"), ("Montserrat", "Open Sans", "duke.edu and Duke Today"),
            ("Playfair Display", "Roboto", "Modern news site"), ("Open Sans", "Georgia", "Safe everywhere: email, old Office")]


def data_uri(name):
    path = SKILL / "assets" / "logos" / "tight" / name
    if not path.exists():
        return ""
    return "data:image/svg+xml;base64," + base64.b64encode(path.read_bytes()).decode()


def swatch(name):
    hex_value = db.PALETTE[name]
    on_white = db.contrast(hex_value, "#FFFFFF")
    ink = "#FFFFFF" if on_white >= 4.5 else db.PALETTE["cast-iron"]
    use = "text + fills" if on_white >= 4.5 else ("large text only" if on_white >= 3 else "fills + decoration only")
    return (f'<div class="sw" style="background:{hex_value};color:{ink}"><b>{name.replace("-", " ").title()}</b>'
            f'<span>{hex_value}</span><em>{on_white:.1f}:1 on white<br>{use}</em></div>')


def lockup_html(lines, reverse, gold=None, initial_caps=False):
    mark = data_uri("duke_wordmark_white.svg" if reverse else "duke_wordmark_navyblue_012169.svg")
    wordmark = f'<img class="wm" src="{mark}" alt="Duke">' if mark else '<span class="wm-missing">[wordmark]</span>'
    words = []
    for line in lines:
        words.append(" ".join(f"<em>{w}</em>" if w.lower() in ("of", "the", "for", "and") else w for w in line.split()))
    style = f' style="color:{gold}"' if gold else ""
    cls = "unit" + (" two" if len(lines) > 1 else "") + (" ic" if initial_caps else "")
    divider = "" if gold else '<span class="div"></span>'
    return f'{wordmark}{divider}<span class="{cls}"{style}>{"<br>".join(words)}</span>'


def group_card(slug):
    t = db.resolve(slug, None)
    c, g = t["colors"], t["group"]
    lk = g.get("lockup") or {}
    gold = db.to_hex(lk["color"])[0] if lk.get("color") else None
    chips = "".join(f'<i style="background:{c[k]}" title="{k}"></i>' for k in ("base", "accent", "accent_2", "highlight"))
    lineage = ("child of " + " › ".join(g["lineage"][:-1])) if len(g["lineage"]) > 1 else "top-level group"
    head, body = t["fonts"]["heading"]["family"], t["fonts"]["body"]["family"]
    return f'''<div class="card">
      <div class="band" style="background:{c['base']}">{lockup_html(lk.get("lines", [g["name"]]), True, gold, lk.get("style") == "initial-caps")}</div>
      <div class="cardbody">
        <h4 style="font-family:'{head}',serif;color:{c['base']}">{g['name']}</h4><div class="rule" style="background:{c['accent']}"></div>
        <p style="font-family:'{body}',sans-serif">{head} + {body}. Theme <code>{t['theme']}</code>. <a style="color:{c['link']}">A link looks like this</a>.</p>
        <p><span class="btn" style="background:{c['accent']};color:{c['on_accent']}">Primary action</span>
           <span class="btn ghost" style="border-color:{c['base']};color:{c['base']}">SECONDARY →</span></p>
        <div class="chips">{chips}<small><code>{slug}</code> &nbsp;{lineage}</small></div>
      </div></div>'''


def theme_panel(name):
    t = db.resolve(None, name)
    c = t["colors"]
    head, body = t["fonts"]["heading"]["family"], t["fonts"]["body"]["family"]
    return f'''<div class="theme">
      <div class="slide" style="background:{c['base']}"><img class="wm" src="{data_uri('duke_wordmark_white.svg')}" alt="Duke">
        <div class="bar" style="background:{c['highlight'] if name == 'alternate' else '#FFFFFF'}"></div>
        <h3 style="font-family:'{head}',serif">Title slide</h3><p style="font-family:'{body}',sans-serif">{name} theme · {head} + {body}</p></div>
      <div class="slide light"><div class="tbar" style="background:{c['base']}"><span style="font-family:'{head}',serif">Content slide</span></div>
        <div class="tline" style="background:{c['accent']}"></div>
        <ul style="font-family:'{body}',sans-serif"><li>Body text in Cast Iron</li><li>One accent does most of the work</li></ul>
        <span class="pill" style="background:{c['accent']};color:{c['on_accent']}">ACCENT</span>
        <span class="pill" style="background:{c['accent_2']};color:#fff">SECOND</span>
        <div class="note" style="background:{c['background_warm']};border-color:{c['accent']}">Callout fill</div></div>
      <p class="cap"><b>{name}</b>: {db.TOKENS['themes'][name]['description']}</p></div>'''


def main():
    groups = sorted({p.parent.name for d in db.GROUP_DIRS for p in d.glob("*/group.json") if not p.parent.name.startswith("_")})
    families = sorted({f for pair in PAIRINGS for f in pair[:2]} | {"Merriweather", "Open Sans"} - {"Georgia"})
    fonts = "&".join("family=" + f.replace(" ", "+") + ":ital,wght@0,400;0,600;0,700;1,400" for f in families)
    pairs = "".join(f'''<div class="pair"><h3 style="font-family:'{h}',serif">{h}</h3><p style="font-family:'{b}',sans-serif">{b}: the quick brown fox
      jumps over the lazy dog. 0123456789</p><small>{note}</small></div>''' for h, b, note in PAIRINGS)
    lockups = [("Design A · caps, one line", ["Human Resources"], None, False), ("Design B · initial caps", ["Human Resources"], None, True),
               ("Design C · contrasting color, no separator", ["Human Resources"], db.PALETTE["eno"], False),
               ("Design E · two lines", ["Office of", "Information Technology"], None, False)]
    lock = "".join(f'<div class="lk"><div class="lkrow">{lockup_html(l, False, g, ic)}</div><small>{label}</small></div>' for label, l, g, ic in lockups)
    html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Duke brand showcase</title>
<link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:'Open Sans',Arial,sans-serif;color:#262626;background:#fff;width:1400px;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
header{{background:#012169;color:#fff;padding:22px 40px;display:flex;align-items:center;gap:14px}} header h1{{font-family:'Merriweather',serif;font-size:26px;margin:0 0 0 auto;font-weight:700}}
section{{padding:26px 40px 8px}} h2{{font-family:'Merriweather',serif;color:#012169;font-size:22px;margin:0 0 4px}} h2+p{{margin:0 0 14px;color:#666;font-size:13px}}
.wm{{height:56px;display:block}} .wm-missing{{font-size:12px;border:1px dashed #B5B5B5;padding:14px}}
.grid{{display:grid;gap:10px}} .g2{{grid-template-columns:repeat(2,1fr)}} .g9{{grid-template-columns:repeat(9,1fr)}} .g3{{grid-template-columns:repeat(3,1fr)}} .g4{{grid-template-columns:repeat(4,1fr)}}
.sw{{height:104px;padding:9px 10px;border-radius:3px;font-size:11px;display:flex;flex-direction:column;border:1px solid #E5E5E5}} .sw b{{font-size:12.5px}} .sw em{{margin-top:auto;font-style:normal;opacity:.9;font-size:10px;line-height:1.3}}
.sw.big{{height:120px}} .sw.big b{{font-size:17px}}
.theme .slide{{height:150px;border-radius:3px;padding:16px 20px;color:#fff;position:relative;margin-bottom:8px;border:1px solid #E5E5E5;overflow:hidden}} .theme .slide .wm{{height:38px;margin:-6px 0 4px -9px}}
.theme .bar{{width:54px;height:5px;margin:6px 0}} .theme h3{{margin:0;font-size:24px}} .theme p{{margin:4px 0 0;font-size:12px}} .theme .light{{background:#fff;color:#262626;padding:0}}
.tbar{{padding:9px 16px;color:#fff;font-size:17px;font-weight:700}} .tline{{height:4px}} .theme ul{{font-size:12.5px;margin:10px 0 8px;padding-left:34px}}
.pill{{font-size:10px;font-weight:700;padding:4px 9px;border-radius:3px;margin-left:16px;letter-spacing:.05em}} .note{{position:absolute;right:16px;top:62px;width:150px;font-size:11.5px;padding:9px 11px;border-left:4px solid}}
.cap{{font-size:12.5px;color:#262626 !important}}
.pair{{border:1px solid #E5E5E5;border-radius:3px;padding:12px 16px}} .pair h3{{margin:0;font-size:25px;color:#012169}} .pair p{{margin:4px 0 6px;font-size:13.5px;line-height:1.5}} .pair small,.lk small{{color:#666;font-size:11px}}
.lk{{border:1px solid #E5E5E5;border-radius:3px;padding:6px 12px 10px}} .lkrow,.band{{display:flex;align-items:center;gap:9px}} .lkrow .wm{{margin-left:-12px}}
.div{{width:1px;height:28px;background:currentColor;flex:none}} .lkrow .div{{background:#012169}} .band .div{{background:#fff}}
.unit{{font-weight:600;text-transform:uppercase;letter-spacing:.08em;font-size:14px;line-height:1.27;color:#012169;white-space:nowrap}} .unit.two{{font-size:12px}} .unit.ic{{font-weight:400;text-transform:none;letter-spacing:0;font-size:20px}}
.unit em{{font-weight:400;font-style:italic;text-transform:none;letter-spacing:0}} .band .unit{{color:#fff}} .band{{padding:4px 14px 4px 4px}}
.card{{border:1px solid #E5E5E5;border-radius:3px;overflow:hidden}} .cardbody{{padding:12px 16px 14px}} .card h4{{margin:0;font-size:18px}} .rule{{width:60px;height:3px;margin:7px 0 8px}} .card p{{font-size:12.5px;margin:0 0 9px;line-height:1.5}}
.btn{{display:inline-block;font-size:11.5px;font-weight:700;padding:7px 13px;border-radius:3px;margin-right:6px}} .btn.ghost{{border:1px solid;letter-spacing:.07em;font-size:10.5px}}
.chips{{display:flex;align-items:center;gap:5px}} .chips i{{width:22px;height:22px;border-radius:50%;border:1px solid #E5E5E5}} .chips small{{margin-left:6px;color:#666;font-size:11px}}
code{{background:#F3F2F1;padding:1px 4px;border-radius:2px;font-size:11.5px}} footer{{padding:14px 40px 26px;color:#666;font-size:11px}}
</style></head><body>
<header><img class="wm" src="{data_uri('duke_wordmark_white.svg')}" alt="Duke"><h1>Brand showcase</h1></header>
<section><h2>Primary palette</h2><p>At least one of these in every piece. Never tinted, faded or made transparent.</p>
  <div class="grid g2">{swatch('navy').replace('class="sw"', 'class="sw big"')}{swatch('royal').replace('class="sw"', 'class="sw big"')}</div></section>
<section><h2>Extended palette</h2><p>Accents. The note on each swatch says whether it can carry text on white.</p><div class="grid g9">{''.join(swatch(n) for n in EXTENDED)}</div></section>
<section><h2>Neutrals</h2><p>Text, borders and soft fills.</p><div class="grid g9">{''.join(swatch(n) for n in NEUTRALS)}</div></section>
<section><h2>Themes</h2><p>Both are fully on-brand. The theme decides which colors do which job.</p><div class="grid g2">{theme_panel('alternate')}{theme_panel('primary')}</div></section>
<section><h2>Type pairings</h2><p>All official Duke typefaces. Headline family first, body second.</p><div class="grid g3">{pairs}</div></section>
<section><h2>Unit lockups</h2><p>Four of Duke's sanctioned designs. Wordmark, thin separator, unit name in Open Sans.</p><div class="grid g4">{lock}</div></section>
<section><h2>Groups</h2><p>Each group layered on Duke. Circles: base, accent, second accent, highlight. Generated from <code>groups/*/group.json</code>.</p><div class="grid g4">{''.join(group_card(g) for g in groups)}</div></section>
<footer>Generated by scripts/make_showcase.py from assets/duke-tokens.json and groups/. Colors and rules: brand.duke.edu. Not an official Duke publication.</footer>
</body></html>'''
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "showcase.html").write_text(html)
    print(f"wrote {OUT / 'showcase.html'} ({len(groups)} groups)")
    chrome = next((c for c in CHROME if Path(c).exists() or shutil.which(c)), None)
    if not chrome:
        print("note: Chrome not found, so no PNG or PDF. Open the HTML in a browser instead.")
        return
    common = [chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=8000"]
    subprocess.run(common + ["--window-size=1400,2120", f"--screenshot={OUT / 'showcase.png'}", f"file://{OUT / 'showcase.html'}"], capture_output=True)
    subprocess.run(common + ["--no-pdf-header-footer", f"--print-to-pdf={OUT / 'showcase.pdf'}", f"file://{OUT / 'showcase.html'}"], capture_output=True)
    print("wrote showcase.png and showcase.pdf")


if __name__ == "__main__":
    main()
