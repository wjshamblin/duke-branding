#!/usr/bin/env python3
"""Build the examples gallery in assets/examples/ from the skill's own templates.

Each example is filled from a template exactly the way the guides tell a user to do it,
so the gallery doubles as a test that the templates and group theming still work.
Sources go to assets/examples/src/, PNG previews (when Chrome is installed) beside them.
All copy is invented. Nothing is taken from a Duke site.

Re-run after changing a template, the stylesheet or a group. Standard library only.
Usage: make_examples.py
"""
import base64
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import duke_brand as db  # noqa: E402

SKILL = Path(__file__).resolve().parent.parent
ASSETS, OUT = SKILL / "assets", SKILL / "assets" / "examples"
CHROME = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "google-chrome", "chromium", "chromium-browser"]
FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700'
         '&family=Open+Sans:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">')


def logo(name):
    path = ASSETS / "logos" / "tight" / name
    if not path.exists():
        sys.exit(f"error: {path} missing. Download the wordmarks first (assets/logos/README.md)")
    mime = "image/svg+xml" if name.endswith(".svg") else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def fill(text, pairs):
    """Replace each placeholder once, in order, and fail loudly if a template drifted."""
    for old, new in pairs:
        if old not in text:
            sys.exit(f"error: placeholder not found (template changed?): {old[:60]}")
        text = text.replace(old, new, 1)
    return text


def web_page():
    css = (ASSETS / "duke-alternate.css").read_text() + "\n" + db.as_css(db.resolve("oit", None))
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Research Computing | Duke OIT</title>{FONTS}<style>{css}
.duke {{ max-width: 1040px; }} .hero {{ display: flex; align-items: stretch; margin: 0 0 2.5rem; }}
.hero .photo {{ flex: 1.3; min-height: 260px; background: var(--duke-hatteras); display: flex; align-items: center; justify-content: center; color: var(--duke-graphite); font-size: .85rem; }}
.hero .duke-panel {{ flex: 1; margin: 2rem 0 -1.5rem -3rem; }}
</style></head><body style="margin:0"><div class="duke">
<header class="duke-band"><img class="duke-wordmark-img" src="../../logos/tight/duke_wordmark_white.svg" alt="Duke"><span class="duke-unit is-two-line is-gold">Office <em>of</em><br>Information Technology</span></header>
<div class="hero"><div class="photo">[ real Duke photo: people first, natural light ]</div>
<div class="duke-panel"><p class="duke-eyebrow" style="color:var(--duke-dandelion)">Research computing</p><h2>Bring your analysis to the cluster.</h2>
<p>Request an allocation, get onboarded in a week, and keep your data where policy says it belongs.</p>
<a class="duke-btn is-arrow" style="background:transparent;border-color:#fff;color:#fff !important" href="#">Request an allocation</a></div></div>
<h1 class="duke-heading-rule">Getting started</h1>
<p class="duke-lead">Three steps take most research groups from first question to first job.</p>
<div class="duke-cards"><div class="duke-card"><p class="duke-eyebrow">Step 1</p><h3>Tell us about the work</h3><p>Data size, sensitivity and software. Ten minutes.</p></div>
<div class="duke-card is-eno"><p class="duke-eyebrow">Step 2</p><h3>Get your allocation</h3><p>Most requests are approved within three working days.</p></div>
<div class="duke-card is-magnolia"><p class="duke-eyebrow">Step 3</p><h3>Run your first job</h3><p>Office hours every Tuesday, in person and on Zoom.</p></div></div>
<div class="duke-callout"><p class="duke-callout-title">Working with sensitive data?</p><p>Tell us before you upload. We will place the project on a protected partition.</p></div>
<p><a class="duke-btn" href="#">Request an allocation</a> <a class="duke-btn is-ghost is-arrow" href="#">Read the guide</a></p>
<footer class="duke-footer"><p>Office of Information Technology · Duke University</p></footer></div></body></html>"""


HOSTED = "https://YOUR-HOST/duke_wordmark_white.png"      # sources stay readable; previews swap in the real file


def canvas_page():
    tokens = db.resolve("computer-science", None)
    page = re.sub(r"<!--.*?-->\s*", "", db.render(ASSETS / "canvas-page-template.html", tokens), count=1, flags=re.S)
    link = tokens["colors"]["link"]
    img = f'<img src="{HOSTED}" alt="Duke" width="110" height="56" style="vertical-align: middle;"> '
    body_old = re.search(r"\[Body copy\..*?\]", page, re.S).group(0)
    return fill(page, [
        ("<!-- WORDMARK IMAGE GOES HERE, followed by a space -->", img),
        ("[Page or week title]", "Week 3: Hash Tables"), ("[Course code and name]", "COMPSCI 201 · Data Structures &amp; Algorithms"), ("[Instructor]", "Dr. Priya Nair"),
        ("[One-sentence lead: what this page is for.]", "How to find almost anything in constant time, and what it costs you."),
        (body_old, f'So far our structures have kept data in order. This week we give up order to gain speed. Start with the <a style="color: {link}; text-decoration: underline;" href="#">lecture notes</a>.'),
        ("[Heads up]", "Heads up: the midterm is in two weeks"), ("[One or two sentences the reader must not miss.]", "Hash tables will be on it. Bring questions to office hours while there is still time."),
        ("[Objective]", "Explain how a hash function maps keys to positions."), ("[Objective]", "Compare separate chaining with linear probing."),
        ("[LABEL]", "ASSIGNMENT"), ("[Item]", "APT Set 3"), ("[day, date, time]", "Friday, Sept. 25, 11:59 p.m."), ("[LABEL]", "QUIZ"), ("[Item]", "Quiz 2"), ("[day, date]", "Thursday, Sept. 24"),
        ("[What this table shows]", "Weekly office hours for COMPSCI 201"), ("[Name]", "Dr. Nair"), ("[Day, time]", "Monday, 2 to 4 p.m."), ("[Place]", "LSRC D309"),
        ("[Name]", "TAs"), ("[Day, time]", "Tuesday and Thursday, 6 to 8 p.m."), ("[Place]", "The Link"), ("[date]", "September 2026")])


def canvas_simulation(page):
    """Wrap the pasteable block the way Canvas shows it: its own H1 title and Lato UI font."""
    return ('<html><body style="margin:0;background:#f5f5f5;font-family:Lato,Helvetica,Arial,sans-serif"><div style="max-width:1000px;margin:0 auto;'
            'background:#fff;padding:22px 36px 40px"><div style="color:#666;font-size:12px">Simulated Canvas page. The title below is Canvas\'s own H1.</div>'
            '<h1 style="font-weight:400;font-size:2em;margin:.5em 0 .7em">Week 3: Hash Tables</h1>' + page + "</div></body></html>")


def email():
    tokens = db.resolve("hr", None)
    page = db.render(ASSETS / "email-template.html", tokens)
    typed = re.search(r'<span style="font-family:Georgia[^>]*>Duke</span>', page).group(0)
    second = re.search(r'<p style="margin:0 0 16px;">\[Second paragraph.*?</p>', page, re.S).group(0)
    gold = tokens["colors"]["accent_on_base"]
    return fill(page, [(typed, f'<img src="{HOSTED}" alt="Duke" height="56" width="110" style="display:block; border:0;">'),
                       ("padding:20px 28px; border-bottom", "padding:10px 14px; border-bottom"),
                       (second, f'<p style="margin:0 0 16px;">Compare plans and costs in the <a href="#" style="color:{tokens["colors"]["link"]}; text-decoration:underline;">2027 benefits guide</a>.</p>'),
                       ("[SUBJECT LINE]", "Open enrollment starts Monday"), ("[One-line preview of the message]", "Review your benefits by October 30."),
                       ("[Unit Name]", f'<span style="color:{gold}; font-weight:normal; font-size:20px;">Human Resources</span>'),
                       ("[Section label]", "Benefits"), ("[Headline]", "Open enrollment starts Monday"),
                       ("[Opening paragraph. Lead with what the reader needs to know or do.]", "From October 19 to October 30 you can review and change your health, dental and vision elections for 2027."),
                       ("[Key date or action]", "Closes October 30 at 6 p.m."), ("[One or two sentences.]", "If you take no action, your current elections roll over, except reimbursement accounts."),
                       ("[Call to action]", "Review my benefits"), ("[Address]", "705 Broad St., Durham, NC 27705"), ("[unit.duke.edu]", "hr.duke.edu")])


def main():
    (OUT / "src").mkdir(parents=True, exist_ok=True)
    canvas = canvas_page()
    jobs = [("web-page-oit", web_page(), "1120,1180", None), ("canvas-page-cs", canvas, "1080,1240", canvas_simulation(canvas)), ("email-hr", email(), "700,760", None)]
    chrome = next((c for c in CHROME if Path(c).exists() or shutil.which(c)), None)
    for name, html, size, preview in jobs:
        src = OUT / "src" / f"{name}.html"
        src.write_text(html)
        if chrome:
            local = "file://" + str(ASSETS / "logos" / "tight" / "duke_wordmark_white.png")
            shot = OUT / "src" / f"_{name}-preview.html"
            shot.write_text((preview or html).replace(HOSTED, local))
            subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--virtual-time-budget=7000",
                            f"--window-size={size}", f"--screenshot={OUT / (name + '.png')}", f"file://{shot}"], capture_output=True)
            shot.unlink()
        print(f"{name}: source{' + png' if chrome else ''}")
    if not chrome:
        print("note: Chrome not found, so no PNG previews.")


if __name__ == "__main__":
    main()
