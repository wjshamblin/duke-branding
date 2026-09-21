# Word Documents and PDFs

Reports, memos, letters, one-pagers, flyers, posters, handouts, syllabi. This guide
supplies the brand specification. Build the file with whatever document tooling is
available (a docx or pdf skill, python-docx, HTML-to-PDF, LaTeX, reportlab). Get
exact values from `python3 scripts/duke_brand.py tokens [--group <slug>] [--theme ...]`.

## Official templates first

University letterhead in Word: https://communicators.duke.edu/digital/powerpoint-and-letterhead/.
For formal correspondence use that letterhead rather than drawing one. Printed
stationery and business cards are ordered through Universal Printing, not designed.

## Choosing a route to PDF

| Need                                        | Route                                                         |
|---------------------------------------------|---------------------------------------------------------------|
| User will keep editing                      | Build .docx, user exports PDF                                 |
| Designed one-pager, flyer, newsletter, report | Build HTML with `assets/duke-alternate.css` plus a print block, render to PDF. Best fidelity and embeds the web fonts |
| Long structured or technical document       | LaTeX or a PDF library, colors and fonts from the tokens      |

Print block for HTML-to-PDF:

```css
@page { size: Letter; margin: 0.75in; }
@media print {
  .duke { max-width: none; padding: 0; font-size: 10.5pt; }
  .duke h1, .duke h2, .duke h3 { break-after: avoid; }
  .duke-card, .duke-callout, .duke table, .duke-quote { break-inside: avoid; }
  .duke-card { box-shadow: none; }
  .duke a { color: inherit; text-decoration: none; }
}
```

Set `print-color-adjust: exact` on elements with background fills, or Navy bands and
callout backgrounds vanish in the PDF. Confirm fonts rendered before delivering.

## Page setup

- US Letter, 1 in margins for letters and memos, 0.75 in for designed pieces.
- Single column body at 10.5 to 11pt, line spacing 1.3 to 1.4. Left aligned, ragged right.
- Wordmark from `assets/logos/tight/`, image at least 0.82 in tall (that makes the
  capital D the required 3/8 in), and at least 1/2 in from the top and edges.
- For commercial print use the CMYK or Pantone values in `references/colors.md`
  and supply vector logos. For desktop printing and screen PDFs, RGB/HEX is fine.

## Styles

Define these as real named styles (Heading 1, Heading 2, ...) so the document gets a
navigable outline and users' edits stay consistent. Never fake a heading with bold.

| Style        | Spec                                                                  |
|--------------|-----------------------------------------------------------------------|
| Title        | Heading font, 26 to 30pt bold, Navy. 3pt accent rule beneath          |
| Heading 1    | Heading font, 18 to 20pt bold, Navy, 18pt space before                |
| Heading 2    | Heading font, 14pt bold, Magnolia or Navy                             |
| Heading 3    | Body font, 11pt bold caps, letter-spaced, `accent_text` color         |
| Body         | Body font, 10.5 to 11pt, Cast Iron                                    |
| Lead / intro | Body font, 13pt, Graphite                                             |
| Callout      | Warm/soft fill from the theme, 3pt accent left border, 8pt padding    |
| Pull quote   | Heading font italic 16pt, Magnolia, second-accent left border         |
| Table        | Navy header row with white bold text, Whisper Gray banding, Limestone rules |
| Caption      | Body font, 9pt, Graphite                                              |
| Hyperlink    | Prussian Blue, underlined                                             |
| Header/footer | Body font, 9pt, Graphite. Footer: group `footer` line left, page number right |

Fonts: see "Office files and PDFs" in `references/typography.md`. In Microsoft 365
Word the brand fonts are Office cloud fonts and render for every recipient. Use the
`office_fallback` fonts only when readers are on LibreOffice, Pages or old Office. A
PDF embeds its fonts, so the brand fonts are always safe there.

## Document types

- **Letter:** official letterhead. Body in the body font, no color beyond the
  letterhead itself. `primary` theme.
- **Memo:** lockup top left, then a TO / FROM / DATE / RE block with bold caps labels,
  a Limestone rule, then body. `primary` theme unless the group says otherwise.
- **Report:** cover page with a solid Navy band or full Navy page, white title,
  accent rule, reversed wordmark and group logo at the bottom. Interior pages white
  with running footer. Executive summary in a callout.
- **One-pager / fact sheet:** Navy header band with title, two or three columns of
  short sections with Heading 3 labels, one big-number row in the accent, contact
  block and logos along the bottom edge.
- **Flyer / poster:** one dominant image or a solid Navy field, headline 48pt and up,
  what / when / where in a high-contrast block, logos along the bottom on one baseline.
  For research posters, check whether the school has its own template first.
- **Syllabus / course handout:** `alternate` theme, course lockup, table styles for
  schedules, callouts for policies.

## Accessibility (required for anything distributed as PDF)

- Tagged PDF with a real heading structure, document title and language set.
- Alt text on every image. Decorative shapes marked as artifacts.
- Tables have header rows and no merged cells where avoidable.
- Contrast per `references/colors.md`. Links are underlined and have meaningful text.
- When exporting from Word: Save As PDF with "Document structure tags for
  accessibility" on. Printing to PDF strips the tags.
