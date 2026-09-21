"""Programmatic grader for the duke-branding evals. Writes grading.json per run.
Usage: grade.py <iteration-dir>   (layout: eval-N-name/<config>/run-1/outputs/)"""
import hashlib, json, re, sys, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
SK = Path(__file__).resolve().parent.parent      # the skill: this repo's root
sys.path.insert(0, str(SK / "scripts"))
import duke_brand as db
PAL = {v.upper() for v in db.PALETTE.values()}; FONTS = set(db.TOKENS["fonts"]) | {"Arial", "Georgia", "Helvetica", "Helvetica Neue", "Menlo", "Consolas", "Lato"}  # Lato is Canvas's own UI font
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"; P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
OFFICIAL = {hashlib.md5(f.read_bytes()).hexdigest() for f in (SK / "assets/logos").rglob("*.png")}

def fam(t):
    for f in sorted(FONTS, key=len, reverse=True):
        if t == f or t.startswith(f + " "): return f
    return t

def deck_facts(path):
    z = zipfile.ZipFile(path); slides = sorted([n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)], key=lambda n: int(re.findall(r"\d+", n)[-1]))
    f = dict(n=len(slides), colors=set(), fonts=set(), titled=0, pics=0, pics_alt=0, text="", low=[])
    for n in slides:
        root = ET.fromstring(z.read(n)); f["text"] += " ".join(t.text or "" for t in root.iter(A + "t")) + " "
        f["colors"] |= {"#" + c.get("val").upper() for c in root.iter(A + "srgbClr")}
        f["fonts"] |= {fam(l.get("typeface")) for l in root.iter(A + "latin") if not l.get("typeface", "+").startswith("+")}
        if any((sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph") is not None and sp.find(f"{P}nvSpPr/{P}nvPr/{P}ph").get("type") in ("title", "ctrTitle")
                and "".join(t.text or "" for t in sp.iter(A + "t")).strip()) for sp in root.iter(P + "sp")): f["titled"] += 1
        for pic in root.iter(P + "pic"):
            f["pics"] += 1; f["pics_alt"] += bool((pic.find(f"{P}nvPicPr/{P}cNvPr").get("descr") or "").strip())
        for sp in root.iter(P + "sp"):
            fill = sp.find(f"{P}spPr/{A}solidFill/{A}srgbClr"); bg = "#" + fill.get("val") if fill is not None else "#FFFFFF"
            if sp.find(f"{P}spPr/{A}solidFill") is None and sp.find(f"{P}spPr/{A}noFill") is None and fill is None: bg = "#FFFFFF"
            for r in sp.iter(A + "r"):
                txt = (r.find(A + "t").text or "").strip() if r.find(A + "t") is not None else ""; rp = r.find(A + "rPr")
                fg = rp.find(f"{A}solidFill/{A}srgbClr") if rp is not None else None
                if not txt or fg is None or fill is None: continue          # only judge text on its own filled shape: unambiguous
                size = int(rp.get("sz", "1800")) / 100; ratio = db.contrast("#" + fg.get("val"), bg)
                if ratio < (3 if size >= 18 or (size >= 14 and rp.get("b") == "1") else 4.5): f["low"].append(f"{fg.get('val')} on {bg} {ratio:.1f}")
    theme = z.read("ppt/theme/theme1.xml").decode(); f["theme"] = re.search(r'clrScheme name="([^"]*)"', theme).group(1)
    media = [hashlib.md5(z.read(n)).hexdigest() for n in z.namelist() if n.startswith("ppt/media/")]
    f["official_wordmark"] = any(m in OFFICIAL for m in media); return f

def strict_audit(deck):
    """The skill's own audit, which since round one judges text against the shape beneath it."""
    import subprocess
    r = subprocess.run([sys.executable, str(SK / "scripts/pptx_tools.py"), "audit", str(deck)], capture_output=True, text=True)
    probs = [l.strip()[9:].strip() for l in r.stdout.splitlines() if l.strip().startswith("PROBLEM")]
    return probs

def E(text, passed, evidence): return {"text": text, "passed": bool(passed), "evidence": str(evidence)[:300]}

POINTS = [["3x", "3×", "tripled", "threefold"], ["capstone"], ["2027"], ["philosophy"], ["faculty"], ["major"]]

def grade_deck(out, kind):
    decks = [p for p in out.glob("*.pptx") if not p.name.startswith("~")]
    if kind == "audit": decks = [p for p in decks if "fixed" in p.name] or decks
    if not decks: return [E("A .pptx file was produced", False, "none found")]
    f = deck_facts(decks[0]); off = sorted(c for c in f["colors"] if c not in PAL); badf = sorted(x for x in f["fonts"] if x not in FONTS)
    ex = [E("A .pptx file was produced", True, decks[0].name),
          E("Uses the real Duke Navy #012169 or Royal #00539B (not a guessed blue)", f["colors"] & {"#012169", "#00539B"}, sorted(f["colors"] & {"#012169", "#00539B"})),
          E("Every color in the deck is from Duke's official palette", not off, f"off-palette: {off}" if off else f"{len(f['colors'])} colors, all official"),
          E("Every font is an official Duke typeface (or the sanctioned Georgia/Arial fallback)", not badf, f"non-Duke: {badf}" if badf else sorted(f["fonts"])),
          E("Carries the official Duke wordmark image file (not typed text or a drawn logo)", f["official_wordmark"], "official PNG found in ppt/media" if f["official_wordmark"] else "no official wordmark file in the deck"),
          E("Every slide has a real title placeholder (screen readers, outline view)", f["titled"] == f["n"], f"{f['titled']} of {f['n']} slides"),
          E("Every picture has alt text", f["pics"] == f["pics_alt"], f"{f['pics_alt']} of {f['pics']} pictures"),
          E("No low-contrast text on filled shapes (WCAG AA)", not f["low"], f["low"][:4] or "none"),
          E("File theme is not the default Office theme (pickers and links stay on-brand)", not f["theme"].lower().startswith("office"), f["theme"])]
    probs = [x for x in strict_audit(decks[0]) if "contrast" in x or ":1 at" in x]
    ex.append(E("No low-contrast text anywhere, including text boxes over bands and the slide background (added in round 2)", not probs, probs[:3] or "none"))
    t = f["text"].lower()
    if kind == "new":
        ex += [E("Has exactly the 6 slides requested", f["n"] == 6, f["n"]),
               E("Identifies Computer Science as the unit on the deck", "computer science" in t, "found" if "computer science" in t else "missing"),
               E("Includes the presenter's name and role", "rivera" in t and "undergraduate studies" in t, ""),
               E("Covers all six requested points", all(any(a in t for a in alts) for alts in POINTS), [alts[0] for alts in POINTS if not any(a in t for a in alts)] or "all present")]
    else:
        keep = ["october 19", "october 30", "vision plan", "legacy dental", "684-5600", "hr.duke.edu"]
        ex += [E("Keeps all of the original content (dates, plan changes, contact info)", all(k in t for k in keep), [k for k in keep if k not in t] or "all kept"),
               E("Keeps the original 5 slides", f["n"] == 5, f["n"]),
               E("Original file left unmodified", hashlib.md5((out.parents[1] / "open-enrollment-2027.pptx").read_bytes()).hexdigest() == hashlib.md5((out.parents[4] / "inputs/open-enrollment-2027.pptx").read_bytes()).hexdigest(), "")]
        resp = (out / "response.md").read_text().lower() if (out / "response.md").exists() else ""
        seeded = {"wrong blue (#003087 is not Duke Navy)": ["003087", "wrong blue", "not duke navy", "isn't duke navy", "incorrect blue", "off-brand blue"],
                  "non-Duke fonts (Comic Sans / Calibri)": ["comic sans"], "typed/fake wordmark": ["wordmark", "logo"],
                  "off-palette red and green": ["ff0000", "red", "00b050", "green"], "low-contrast text": ["contrast"],
                  "missing alt text": ["alt text", "alt-text", "alternative text"], "no real slide titles": ["title placeholder", "real title", "slide title", "no title", "titles"]}
        found = [k for k, keys in seeded.items() if any(x in resp for x in keys)]
        ex.append(E("Findings report names at least 6 of the 7 seeded defects", len(found) >= 6, f"{len(found)}/7 named; missed: {[k for k in seeded if k not in found]}"))
    return ex

def grade_html(out):
    p = out / "page.html"
    if not p.exists(): return [E("page.html was produced", False, "missing")]
    h = p.read_text(); low = h.lower(); cols = {("#" + c.upper()) if len(c) == 6 else "#" + "".join(x * 2 for x in c.upper()) for c in re.findall(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b", h)}
    off = sorted(c for c in cols if c not in PAL); fams = {x.split(",")[0].strip().strip("'\"") for x in re.findall(r"font-family\s*:\s*([^;}\"]+)", h)}
    badf = sorted(x for x in fams if x and not x.startswith("var(") and fam(x) not in FONTS | {"inherit"})
    content = ["hash", "sedgewick", "3.4", "apt", "11:59", "quiz 2", "midterm", "lsrc d309", "zoom", "the link"]
    return [E("page.html was produced", True, f"{len(h)} bytes"),
            E("No <script>, <html>, <head> or <body> tags (Canvas strips them)", not re.search(r"<\s*(script|html|head|body)\b", low), re.findall(r"<\s*(script|html|head|body)\b", low)[:4] or "clean"),
            E("Uses the real Duke Navy #012169 or Royal #00539B", cols & {"#012169", "#00539B"}, sorted(cols & {"#012169", "#00539B"})),
            E("Every color is from Duke's official palette", not off, f"off-palette: {off}" if off else f"{len(cols)} colors, all official"),
            E("Every font is an official Duke typeface (or sanctioned fallback)", not badf and fams, f"non-Duke first-choice fonts: {badf}" if badf else sorted(fams)),
            E("Styling does not depend on <style> or <link> (Canvas's sanitizer strips both): styles are inline", not re.search(r"<\s*(style|link)\b", low) and low.count("style=") >= 10, f"<style>/<link> tags: {len(re.findall(r'<\s*(style|link)\b', low))}, inline style attributes: {low.count('style=')}"),
            E("Avoids CSS that Canvas drops (font-weight, text-transform, letter-spacing, box-shadow)", not re.findall(r"(font-weight|text-transform|letter-spacing|box-shadow)\s*:", low), sorted(set(re.findall(r"(font-weight|text-transform|letter-spacing|box-shadow)\s*:", low))) or "none used"),
            E("No <h1>: Canvas supplies the page title as the H1, so content starts at <h2>", len(re.findall(r"<h1\b", low)) == 0 and "<h2" in low, f"h1: {len(re.findall(r'<h1', low))}, h2: {len(re.findall(r'<h2', low))}"),
            E("Office hours are a real table with header cells", "<table" in low and "<th" in low, ""),
            E("Does not fake the Duke wordmark silently: uses an official file, or flags the placeholder to the user", ("wordmark" in (out / "response.md").read_text().lower() or "logo" in (out / "response.md").read_text().lower()) if (out / "response.md").exists() else False, "response mentions wordmark/logo handling" ),
            E("Opens with a solid Duke-blue band, the header pattern real Duke sites use (added in round 2)", bool(re.search(r"background(-color)?\s*:\s*#(012169|00539b)", low[:3000])), "band found near the top" if re.search(r"background(-color)?\s*:\s*#(012169|00539b)", low[:3000]) else "no navy/royal band in the first part of the page"),
            E("No image that will show as broken: every <img> has an https or data: source (added in round 2)", all(re.match(r"(https://|data:)", x) for x in re.findall(r"<img[^>]+src=[\"']([^\"']*)", h)), re.findall(r"<img[^>]+src=[\"']([^\"']{0,60})", h) or "no images"),
            E("Contains all requested content", all(k in low for k in content), [k for k in content if k not in low] or "all present")]

it = Path(sys.argv[1])
for ev in sorted(p for p in it.iterdir() if p.is_dir()):
    for cfg in sorted(d.name for d in ev.iterdir() if d.is_dir() and (d / "run-1").is_dir()):
        out = ev / cfg / "run-1" / "outputs"
        if not out.exists() or not any(out.iterdir()): print(f"{ev.name}/{cfg}: no outputs yet"); continue
        ex = grade_html(out) if "canvas" in ev.name else grade_deck(out, "new" if "new-deck" in ev.name else "audit")
        n = sum(e["passed"] for e in ex)
        (ev / cfg / "run-1" / "grading.json").write_text(json.dumps({"expectations": ex, "summary": {"passed": n, "failed": len(ex) - n, "total": len(ex), "pass_rate": round(n / len(ex), 3)}}, indent=2))
        print(f"{ev.name}/{cfg}: {n}/{len(ex)}")
