# HTML: Canvas, Web Pages, Dashboards, Email

Three targets with different constraints. Pick one before writing markup.

| Target                         | Start from                          | CSS delivery                    | Fonts            |
|--------------------------------|-------------------------------------|---------------------------------|------------------|
| Canvas LMS page                | `assets/canvas-page-template.html`  | Inline `style=""` only          | Georgia + Canvas's own sans |
| Standalone page, site, dashboard | `assets/web-page-template.html`   | Inline or linked `duke-alternate.css` | Google Fonts `<link>` |
| Email, newsletter              | `assets/email-template.html`        | Inline `style=""` only          | Georgia + Arial  |

Canvas and email are the same kind of problem: the host strips stylesheets, so every
style is inline with literal hex values. Their templates carry named placeholders, filled by
`python3 scripts/duke_brand.py render <template> --group <slug> > out.html`, which keeps
each color role separate even when two roles share a hex value. The stylesheet, classes and `--format css` are for standalone pages only.

See what finished pieces look like in `assets/examples/` before building.

## Applying the stylesheet (standalone pages only)

1. Read `assets/duke-alternate.css` and inline it into `assets/web-page-template.html`'s
   `<style>` block, replacing the first placeholder comment.
2. For the `primary` theme or any group, run
   `python3 scripts/duke_brand.py tokens [--group <slug>] [--theme primary] --format css`
   and paste the output **after** the stylesheet. Components read `--duke-accent`,
   `--duke-accent-2`, `--duke-accent-text`, `--duke-highlight`, `--duke-on-accent`,
   `--duke-bg-warm`, `--duke-link` and the two font variables, so the override block
   re-themes everything. If the heading or body font changed, update the Google
   Fonts `<link>` to load it.
3. Wrap all content in `<div class="duke">`. Every rule is scoped under `.duke`.
4. Use the bundled components rather than inventing styled elements:
   `.duke-band` (full-width blue header, the pattern real Duke sites use), `.duke-header`
   (lockup on white), `.duke-heading-rule`, `.duke-eyebrow`, `.duke-panel`, `.duke-lead`, `.duke-callout` (`is-info`, `is-success`,
   `is-warn`, `is-navy`), `.duke-cards` / `.duke-card` (`is-copper`, `is-eno`,
   `is-magnolia`, `is-piedmont`, `is-ironweed`), `.duke-btn` (`is-navy`, `is-ghost`, `is-arrow`),
   `.duke-quote`, `.duke-checklist`, `.duke-badge`, `hr.duke-rule`, `.duke-footer`,
   plus styled `table`, `code` and `pre`.

Header markup and lockup rules: `references/logo-and-voice.md`. Wordmark files and
sizing: `assets/logos/README.md`. A browser cannot load a file from the skill folder,
so for a standalone page inline the SVG as a `data:` URI (about 6 KB), for Canvas
upload it to course Files, and for email host the PNG at an `https` URL.

## Canvas

Canvas runs pasted HTML through a sanitizer. This list was checked against its source
(`instructure/canvas-lms`, `gems/canvas_sanitize/lib/canvas_sanitize/canvas_sanitize.rb`),
because guesses here are costly: a page built on a `<style>` block pastes in as
completely unstyled text.

| Canvas does this | So |
|---|---|
| Strips `<style>`, `<link>`, `<script>`, `<svg>`, form controls | No classes, no CSS variables, no web fonts. Inline `style=""` on every element |
| Drops `font-weight`, `text-transform`, `letter-spacing`, `box-shadow`, `opacity`, `filter`, `transition` | Bold is `<strong>`. Type capitals literally. No shadows. The lockup's wide tracking is not achievable, so keep the unit name short and in caps |
| Keeps `color`, `background`, `background-color`, `border` and its sides, `border-radius`, `padding`, `margin`, `font-family`, `font-size`, `font-style`, `line-height`, `text-align`, `text-decoration`, `vertical-align`, `width`, `max-width`, `display`, `flex`, `flex-wrap`, `gap`, `border-collapse` | Enough for bands, callouts, cards and tables |
| Prints the page title as the `<h1>` | Start content at `<h2>`. Do not repeat the title as a heading |
| Cannot load Google Fonts | Georgia for headings (an official Duke face). Let body text inherit Canvas's sans |
| Serves images only from its own Files or an `https` URL | Upload `assets/logos/tight/duke_wordmark_white.png` to course Files (PNG, not SVG) and use that URL. Until the user has done so, leave the wordmark out and say so. A broken image icon is worse than no logo |

Deliver one block the user can paste into HTML view, and tell them to re-open HTML
view once after saving to confirm nothing was stripped. `<header>` and `<footer>`
elements survive but add duplicate landmarks inside Canvas's own page, so use `<div>`.

## Standalone pages and dashboards

- Wrap in a full document with `<meta name="viewport">` and a descriptive `<title>`.
- `.duke` caps width at 860px for reading. For dashboards or landing pages override
  it: `.duke { max-width: 1200px; }`.
- Full-bleed Navy header or hero band: white text, reversed wordmark, a 4px accent
  rule beneath. Do not tint or fade the Navy.
- Charts: order series colors Navy, accent, second accent, then Prussian, Magnolia,
  Ironweed. Pale palette colors (Dandelion, Persimmon, Piedmont) are for fills with
  dark labels, not thin lines on white. Gridlines Limestone, axis text Graphite.
- Favicon: a group `logo.symbol` if one exists. Never crop the wordmark into an icon.

## Email

Email clients drop `<style>` blocks, web fonts, flexbox, grid and CSS variables, so
`assets/email-template.html` uses tables, inline styles and literal hex values.

- Theme with `duke_brand.py render assets/email-template.html --group <slug>`.
- Width 600px. Georgia headings, Arial body, 16px body text.
- Images: absolute `https` URLs, explicit `width`, `alt` on every one,
  `style="display:block;border:0"`. The message must read correctly with images off,
  so never put essential text inside an image.
- Buttons: the padded table-cell pattern in the template. It is the only one Outlook
  renders reliably.
- Navy header band with the reversed wordmark. Keep the preheader line.
- Personal signatures are a separate, simpler thing: see `references/other-media.md`.

## Accessibility checklist for all HTML

- One `<h1>` on a standalone page, none in Canvas (it supplies the title). Headings nested in order.
- Link text describes the destination. No "click here".
- Links are underlined, not distinguished by color alone.
- Body text Cast Iron or Graphite. Check any non-default pairing with
  `python3 scripts/duke_brand.py contrast <fg> <bg>`.
- Tables have `<th>` header cells. Layout tables in email carry `role="presentation"`.
