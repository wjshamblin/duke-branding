# Duke Typography

Source: https://brand.duke.edu/typography/
Download links for every family: `references/brand-resources.md`.

## Official typefaces

| Family             | Weights                           | Use                                                        | Avoid                              |
|--------------------|-----------------------------------|------------------------------------------------------------|------------------------------------|
| EB Garamond        | 400, 500, 600, 700, 800 + italics | Headlines, subheads, body. Closest to the wordmark's Garamond 3 | Small sizes; recreating the wordmark |
| Open Sans          | 300, 400, 600, 700, 800 + italics | Body text, bold headlines, UI. Required for unit names in lockups | —                             |
| Roboto             | 100, 400, 500, 600, 700, 900      | Dense digital text, web and app UI                          | —                                  |
| Georgia            | 400, 700 + italics (system)       | Email, Word docs going to unknown machines, legacy browsers | —                                  |
| Montserrat         | 100 to 900 + italics              | Headlines and display                                       | Long body text                     |
| Merriweather       | 300, 400, 700, 900 + italics      | Long-form body on screen, stays legible small               | —                                  |
| Cormorant Garamond | 300, 400, 500, 600, 700           | Large headings, stylised pull quotes                        | Below 16px / 14pt, dense settings  |
| Playfair Display   | 400, 700, 900 + italics           | Headlines, subheads, large blockquotes                      | Below 16px / 14pt, body text       |
| Roboto Mono        | 100, 300, 400, 500, 700           | Code, statistics, tabular figures                           | —                                  |

Legacy typefaces exist for older materials and are issued by request form on the
typography page. Do not use them for new work.

## Pairings

The first four are the sample pairings Duke publishes. The last is this skill's
default for the `alternate` theme, built from two official families.

| Pairing                       | Character                 | Good for                                |
|-------------------------------|---------------------------|-----------------------------------------|
| EB Garamond + Open Sans       | Classic Duke editorial    | `primary` theme default, formal documents |
| Playfair Display + Roboto     | Modern news site          | Web features, dashboards                |
| Merriweather + Open Sans      | Readable long-form        | Reports, articles, course readings      |
| Open Sans + Georgia           | Safe everywhere           | Email, files opened on unknown machines |
| Playfair Display + Open Sans  | Sharp, magazine-like      | `alternate` theme default               |

Use one pairing per piece. Headline family first, body family second.

## Web

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;1,400&family=EB+Garamond:wght@400;500;700&display=swap" rel="stylesheet">
```

When only CSS is editable: `@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap');`

Official fallback stacks:

```css
font-family: 'EB Garamond', Garamond, Georgia, 'Times New Roman', Times, serif;
font-family: 'Playfair Display', Garamond, Georgia, 'Times New Roman', Times, serif;
font-family: 'Merriweather', Georgia, 'Times New Roman', Times, serif;
font-family: 'Open Sans', 'Helvetica Neue', 'Segoe UI', Helvetica, Arial, sans-serif;
font-family: 'Roboto', 'Helvetica Neue', Helvetica, Arial, sans-serif;
font-family: 'Montserrat', 'Helvetica Neue', Helvetica, Arial, sans-serif;
```

## Office files and PDFs: font availability

**Microsoft 365 (PowerPoint, Word, Excel; Mac, Windows, web):** every Duke typeface
except Cormorant Garamond is an *Office cloud font*. Office downloads it on demand the
first time a file uses it, on the author's machine and on every recipient's. Name the
brand font and it renders. Nothing to install, nothing to embed. They will NOT show up
in `fc-list` or the system font folders, so do not conclude from those that a font is
missing. (Verified against the Office font catalog on macOS, September 2026. Cloud
fonts are a Microsoft 365 subscription feature on every platform, but check when the
audience is unusual.)

| Renders the brand fonts                          | Substitutes silently                                |
|--------------------------------------------------|-----------------------------------------------------|
| Microsoft 365 apps, online or previously cached  | LibreOffice, Keynote                                |
| Any PDF (fonts are embedded on export)           | Office 2019 and earlier, or M365 with no network on first open |
| Google Slides / Docs, native or imported         | Cormorant Garamond everywhere in Office             |

To check a Mac: `ls ~/Library/Group\ Containers/UBF8T346G9.Office/FontCache/4/CloudFonts`
lists cloud fonts already downloaded. `Catalog/listall_hier.json` beside it lists every
font Office can fetch.

Decide per deliverable:

| Situation                                                  | Do this                                              |
|------------------------------------------------------------|------------------------------------------------------|
| Audience uses Microsoft 365 (the normal case at Duke)      | Use the brand fonts                                  |
| File will be opened in Keynote, LibreOffice or old Office  | Use the `office_fallback` fonts (Georgia + Arial), or have those users install from Google Fonts |
| Presenting from an offline or unfamiliar machine           | Open the file once while online first, or carry a PDF |
| HTML to PDF                                                | Load fonts by `<link>` or `@font-face` and confirm they rendered |

Weight names are separate font names in Office: `Open Sans SemiBold`, `Open Sans Light`,
`Montserrat Medium`. Setting "bold" on `Open Sans` gives Bold (700), not Semi-Bold.

`scripts/duke_brand.py tokens` returns an `office_fallback` for each font role.

**Verifying what actually rendered:** export to PDF from the real application and run
`pdffonts file.pdf`. The list names the fonts truly used. A LibreOffice render is good
for checking layout but proves nothing about fonts, because it substitutes.
A stray Arial or Courier New in that list is usually glyph fallback, not a mistake:
Open Sans and Roboto Mono have no arrow characters, so Office borrows "→" from
another font. Judge by the named runs (`pptx_tools.py audit`), not by that alone.

## Type scale

Screen sizes in rem (16px base). Print and Office sizes in pt.

| Element         | Web       | Word / PDF | PowerPoint (16:9) | Weight     | Family role |
|-----------------|-----------|------------|-------------------|------------|-------------|
| Title / h1      | 2.5rem    | 26 to 30pt | 40 to 44pt        | 700        | Heading     |
| h2              | 1.85rem   | 18 to 20pt | 28 to 32pt        | 700        | Heading     |
| h3              | 1.35rem   | 14pt       | 22 to 24pt        | 600 to 700 | Heading     |
| h4 / label      | 1.05rem   | 11pt caps  | 14 to 16pt caps   | 700        | Body        |
| Lead paragraph  | 1.2rem    | 13pt       | 22 to 24pt        | 400        | Body        |
| Body            | 1.0625rem | 10.5 to 11pt | 18 to 20pt      | 400        | Body        |
| Caption / small | 0.875rem  | 9pt        | 12 to 14pt        | 400        | Body        |
| Pull quote      | 1.4rem    | 16pt italic | 28 to 32pt italic | 400 italic | Heading     |

## Rules

- Never type "Duke" in EB Garamond, or any font, as a stand-in for the wordmark in
  a finished piece. Use an official logo file.
- Body line-height 1.5 or more on screen; 1.3 to 1.4 in print.
- Anything under 14px / 10pt is set in the body sans, never a display serif.
- Left-align body text. No justified text on screen. No all-caps beyond short labels.
- Unit names in a lockup follow their own rule: see `references/logo-and-voice.md`.
