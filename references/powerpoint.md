# PowerPoint, Keynote and Google Slides

This guide supplies the brand specification. Build the file itself with whatever
presentation tooling is available (a pptx skill, python-pptx, pptxgenjs, or the host
agent's own slide feature). Get exact values from
`python3 scripts/duke_brand.py tokens [--group <slug>] [--theme ...]`.

## Start from an official template when one exists

Duke publishes branded PowerPoint themes in light and dark variants:
https://communicators.duke.edu/digital/powerpoint-and-letterhead/. If the user has
one (or a unit template), open it and fill it rather than rebuilding. Apply group
accents through the theme colors. Build from the spec below only when there is no
template to start from.

## Setup

- 16:9, 13.333 x 7.5 in. Use 4:3 only on request.
- Safe margin 0.5 in on all sides. Nothing but full-bleed fills crosses it.
- Define brand colors as the file's **theme colors** and fonts as **theme fonts**, so
  users' later edits stay on-brand. Suggested mapping: Dark 1 = Cast Iron,
  Light 1 = White, Dark 2 = Navy, Light 2 = Whisper Gray, Accent 1 = accent,
  Accent 2 = second accent, Accent 3 = highlight, Accent 4 = Prussian Blue,
  Accent 5 = Magnolia, Accent 6 = Ironweed, Hyperlink = Prussian Blue.
- Fonts: heading and body family from the tokens. In Microsoft 365 the brand fonts
  are Office cloud fonts and just work. Use the `office_fallback` fonts only for
  Keynote, LibreOffice or old Office audiences. Details: "Office files and PDFs" in
  `references/typography.md`.

## Slide layouts

Where this table says Navy, read **the base blue**: `colors.base` from the tokens, which is
Royal for Trinity and its departments. These are defaults for a **new** deck. An existing deck with a different layout that
satisfies the core rules is already on-brand: see "Reviewing an existing deck".

| Layout          | Background          | Content                                                                 |
|-----------------|---------------------|-------------------------------------------------------------------------|
| Title           | Solid Navy          | Title 40 to 44pt white, heading font. Subtitle 20 to 24pt Whisper Gray or Dandelion. 0.08 in accent rule under the title. Reversed wordmark bottom left, reversed group logo bottom right |
| Section divider | Solid Navy, or the accent if white text passes on it | Section name 36 to 40pt. Optional large numeral in the highlight color |
| Content         | White               | Title 28 to 32pt Navy, top left. 0.04 in accent rule beneath, about 1.5 in wide. Body 18 to 20pt Cast Iron. Footer strip |
| Two-column      | White               | As content. 0.4 in gutter. Optional Whisper Gray panel behind one column |
| Big number / stat | White or Whisper  | Figure 72 to 96pt in Navy or the accent (accent only if it is AA on the background). Label 18pt Graphite |
| Quote           | Ginger Beer or Hatteras | Quote 28 to 32pt italic heading font, Magnolia or Navy. 0.06 in second-accent bar at left. Attribution 16pt Graphite |
| Image           | Full-bleed photo    | Solid Navy caption band along the bottom, white text. No text directly on the photo |
| Closing         | Solid Navy          | Thanks or call to action, contact block from the group profile, URL, reversed wordmark and group logo. On a mostly white closing slide use the navy wordmark instead: the file color follows the background |

Footer strip on content slides: a 0.5pt Limestone rule, and beneath it the group
`short_name` at left and the slide number at right in 10 to 12pt Graphite. The Duke wordmark appears on title,
divider and closing slides only, not on every slide. With no group logo, the lockup
(wordmark, separator, unit name) goes bottom left or top left and the other side stays
empty. When the slide count is tight, the closing slide may carry the final ask.

## Rules

- Navy backgrounds are solid. No gradients, no transparency, no tints of Navy or Royal.
- The accent has two jobs and may need two colors. On the blue band use
  `colors.accent_on_base`. For a rule or border on a white slide use `colors.rule_on_white`
  (a Dandelion accent is 1.4:1 on white and vanishes). For small accent-colored text on
  white use `colors.accent_text`.
- Lockup on the base blue: white unit name with a white separator, or the unit name in
  `colors.accent_on_base` with no separator (what OIT and HR do). Follow the group's
  `lockup.color` when it sets one.
- One accent does most of the work. The second accent and highlight are for charts,
  callouts and one-off emphasis.
- On Navy, never set Copper text (3.1:1). Use white, Dandelion or Persimmon.
- At most about 6 bullets, or 40 words, per slide. Left-aligned. No text under 14pt
  except footers and source notes.
- Charts: recolor to theme colors in the order Navy, accent, second accent, Prussian,
  Magnolia, Ironweed. Gridlines Limestone, labels Graphite or Cast Iron. Direct-label
  series where possible instead of a legend.
- Tables: Navy header row with white bold text, Whisper Gray banding, Limestone rules.
- Wordmark: insert from `assets/logos/tight/` (SVG, or PNG if the tooling rejects SVG).
  White version on Navy slides. Make the image at least 0.82 in tall; about 1 in
  tall works well on a 16:9 title slide. Sizing table: `assets/logos/README.md`.
  Placement with a group logo: see "Placing a group logo" in
  `references/group-branding.md`.
- Accessibility: every image has alt text, every slide has a unique title, reading
  order is set, and meaning never depends on color alone.

## Reviewing an existing deck

Run the audit first. It is faster and more reliable than reading slides by eye:

```
python3 scripts/pptx_tools.py audit deck.pptx
```

It reports the theme in use, fonts, off-palette colors (with slide numbers), low-contrast
text (judged against the shape beneath it, with slide, shape and the words), a typed
"Duke" standing in for the wordmark, slides with no real title, duplicate titles,
pictures with missing or file-name alt text, text under 14pt, and whether a wordmark is
present and big enough. It cannot see inside pictures: check charts and screenshots by
eye for off-brand colors. Then:

1. **Find how the deck is made.** If a script generates it (look for `build_*.py`,
   pptxgenjs, a Makefile), change the script and rebuild. Editing the .pptx is lost on
   the next build. Back up first if the folder is not under version control.
2. **Respect what is already right.** Fix rule violations and gaps. Do not restyle a
   compliant deck toward this guide's default layouts, and do not change the author's
   accent or official font pairing.
3. **Fix** in this order: wordmark and lockup, theme, real titles and alt text, contrast,
   off-palette colors, non-Duke fonts (Courier New to Roboto Mono is the usual one).
4. **Flag, do not silently change,** anything that reflows content or is an editorial
   call: small text, a missing closing slide, placeholder text, photos of real people
   or names.
5. Re-run the audit, then verify the render.

## Building or patching with python-pptx

| Need | How |
|---|---|
| Duke theme colors and fonts in the file | `python3 scripts/pptx_tools.py theme deck.pptx [--group slug]` after every save. A build script overwrites the file, so call it as the script's last step (`subprocess.run`) rather than by hand. python-pptx has no theme API and leaves the Office default (Calibri, Office blues, bright-blue hyperlinks) |
| A real title on every slide | Use the "Title Only" layout (`prs.slide_layouts[5]`) and fill `slide.shapes.title`. A styled text box is not a title: screen readers and outline view see nothing. The Blank layout has no title placeholder |
| Title hidden behind a full-width band | The title placeholder is created with the slide, so a band added later is drawn on top of it. Send the band to the back instead of bringing the title forward: `tree = slide.shapes._spTree; tree.remove(band._element); tree.insert(2, band._element)`. The band is decoration, so it does not matter that it now comes first; what matters is that the title is still the first *text* a screen reader meets |
| Alt text | `pic._element.nvPicPr.cNvPr.set("descr", "...")`. The wordmark's alt text is just "Duke" |
| Wordmark | python-pptx cannot insert SVG. Use the PNG from `assets/logos/tight/` and set only `height` so the ratio stays locked |
| Wide tracking for lockup caps | `run.font._element.set("spc", "150")` (hundredths of a point) |
| Semi-Bold | `run.font.name = "Open Sans SemiBold"`, not `bold = True` |
| Lockup geometry | Fractions of the wordmark image height: see `assets/logos/README.md` |
| Retrofit a real title onto an existing slide | In place, about 8 lines: point the slide's layout relationship at Title Only, then give the text box's `<p:nvPr>` a `<p:ph type="title"/>` child. This keeps pictures, z-order and notes. The heavier alternative is a new Title Only slide with the shapes moved across |
| Shadows that will not go away | Autoshapes carry a theme effect reference. `shape.shadow.inherit = False` fixes PowerPoint. LibreOffice may still draw one in a verification render: ignore it |
| Self-contained project | Copy the logo files into the deck's own folder (for example `brand/`). Do not make a build script depend on the skill's install path |

## Verify the render

- **Layout:** `soffice --headless --convert-to pdf deck.pptx`, then `pdftoppm -r 40 -png`
  and look at a contact sheet. LibreOffice substitutes fonts, so judge positions and
  overflow only.
- **Text fit without PowerPoint:** measure with the real fonts. Office's downloaded cloud
  fonts are ordinary TTFs under
  `~/Library/Group Containers/UBF8T346G9.Office/FontCache/4/CloudFonts/`, usable with Pillow.
- **Colors inside pictures:** the audit cannot see them. List a chart or screenshot's
  dominant colors with Pillow (`Image.getcolors`) and compare them with the palette.
- **True fonts (Mac with PowerPoint):** export through PowerPoint itself, then check
  `pdffonts`:
  ```
  osascript -e 'tell application "Microsoft PowerPoint"' -e 'open POSIX file "/abs/deck.pptx"' \
    -e 'delay 4' -e 'set d to active presentation' -e 'if name of d is not "deck.pptx" then error "wrong deck in front"' \
    -e 'save d in (POSIX file "/abs/out.pdf") as save as PDF' -e 'close d saving no' -e 'end tell'
  ```
  The name check matters: if the open fails, "active presentation" is whatever the user
  already had open, and the script would save and close *their* work. Save inside the user's own folders: PowerPoint is sandboxed and cannot write to `/tmp`.
  Quit PowerPoint afterwards if it was not already running.

## Keynote and Google Slides

Same spec. Google Slides loads Google Fonts natively, so the brand fonts are safe
there. For Keynote, fonts must be installed locally (Keynote has no cloud fonts). Duke's
official backgrounds are also offered as images for use in these tools.
