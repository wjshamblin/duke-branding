# Duke University Color Palette

Source: https://brand.duke.edu/colors/ and https://brand.duke.edu/color-accessibility-grid/
Machine-readable copy: `assets/duke-tokens.json`.

## Hard rules

- At least one Duke blue (Navy or Royal) must appear in every project.
- Never change the opacity or saturation of the two Duke blues. No tints, no
  transparency, no gradients that fade them. Use Hatteras or Whisper Gray when a
  pale blue-gray is needed.
- Extended-palette colors are secondary and tertiary only. They never replace blue
  as the base.
- Meet WCAG 2.0 AA for all text.

## Primary palette

| Name            | HEX       | RGB         | CMYK            | Pantone     |
|-----------------|-----------|-------------|-----------------|-------------|
| Duke Navy Blue  | `#012169` | 1, 33, 105  | 100, 85, 5, 22  | PMS 280 U/C |
| Duke Royal Blue | `#00539B` | 0, 83, 155  | 100, 53, 2, 16  | PMS 287 U/C |

Navy is the official Duke blue ("Academic Blue"). Royal has been used since 2009
for athletics, apparel and promotional work.

## Extended palette

| Name          | HEX       | RGB           | CMYK            | Pantone                   |
|---------------|-----------|---------------|-----------------|---------------------------|
| Copper        | `#C84E00` | 200, 78, 0    | 0, 76, 100, 0   | PMS 166 U/C               |
| Persimmon     | `#E89923` | 232, 153, 35  | 0, 45, 95, 0    | PMS 1375 U/C              |
| Dandelion     | `#FFD960` | 255, 217, 96  | 0, 8, 70, 0     | PMS 114 U / 121 C         |
| Piedmont      | `#A1B70D` | 161, 183, 13  | 54, 0, 100, 0   | PMS 382 U / 376 C         |
| Eno           | `#339898` | 51, 152, 152  | 81, 0, 39, 0    | PMS 3262 U / 326 C        |
| Magnolia      | `#1D6363` | 29, 99, 99    | 96, 16, 42, 57  | PMS 328 U / 323 C         |
| Prussian Blue | `#005587` | 0, 85, 135    | 100, 45, 0, 45  | PMS 301 U / 7692 C        |
| Shale Blue    | `#0577B1` | 5, 119, 177   | 100, 0, 1, 3    | PMS Process Blue U / 7461 C |
| Ironweed      | `#993399` | 153, 51, 153  | 35, 95, 0, 0    | PMS Purple U / 248 C      |

## Neutrals

| Name         | HEX       | RGB           | CMYK            | Pantone               | Typical use              |
|--------------|-----------|---------------|-----------------|-----------------------|--------------------------|
| Cast Iron    | `#262626` | 38, 38, 38    | 67, 44, 67, 95  | PMS Black 3 U/C       | Body text                |
| Graphite     | `#666666` | 102, 102, 102 | 40, 30, 20, 66  | PMS Cool Gray 10 U/C  | Secondary text           |
| Granite      | `#B5B5B5` | 181, 181, 181 | 13, 8, 11, 26   | PMS 421 U/C           | Disabled, rules          |
| Limestone    | `#E5E5E5` | 229, 229, 229 | 5, 3, 5, 11     | PMS Cool Gray 2 U/C   | Light borders            |
| Whisper Gray | `#F3F2F1` | 243, 242, 241 | 4, 2, 4, 8      | PMS Cool Gray 1 U/C   | Alternate background     |
| Hatteras     | `#E2E6ED` | 226, 230, 237 | 10, 2, 0, 0     | PMS 649 U / 656 C     | Cool background          |
| Ginger Beer  | `#FCF7E5` | 252, 247, 229 | 0, 2, 15, 0     | PMS 9060 U/C          | Warm callout background  |
| Shackleford  | `#DAD0C6` | 218, 208, 198 | 3, 4, 14, 8     | PMS 7527 U / 2527 C   | Warm border              |
| Dogwood      | `#988675` | 152, 134, 117 | 10, 18, 25, 32  | PMS 7530 U/C          | Warm muted accent        |

Use HEX/RGB for screen (web, PowerPoint, Word, video), CMYK for process print,
Pantone for spot print and merchandise. U = uncoated stock, C = coated.

## Themes

Both themes are fully on-brand. The theme decides which palette colors do which job.

| Role              | `alternate` (default)  | `primary` (classic)  |
|-------------------|------------------------|----------------------|
| Base              | Navy                   | Navy                 |
| Accent            | Copper                 | Royal Blue           |
| Second accent     | Eno                    | Prussian Blue        |
| Highlight         | Persimmon              | Shale Blue           |
| Warm/soft fill    | Ginger Beer            | Hatteras             |
| Headings font     | Playfair Display       | EB Garamond          |
| Body font         | Open Sans              | Open Sans            |

Choose `alternate` for teaching material, events, newsletters, student-facing and
promotional work. Choose `primary` for formal and institutional work: leadership
memos, policy, HR and finance notices, legal, anything sent in the university's
name. A group profile can set its own default theme and accents.

Other accent pairs that work on a Navy base: Magnolia + Persimmon, Shale Blue +
Piedmont, Ironweed + Dandelion, Prussian Blue + Copper. Limit any single piece to
Navy plus two accents and neutrals.

## Accessibility

Ratios below are from Duke's official grid. AA = 4.5:1 for normal text.
AA18 = 3:1, acceptable only for large text (18pt+, or 14pt+ bold).

### Text color on a white background

| Color         | Ratio | Rating | Use for text?                         |
|---------------|-------|--------|---------------------------------------|
| Cast Iron     | 15.1  | AAA    | Yes, default body                     |
| Navy          | 14.7  | AAA    | Yes                                   |
| Prussian Blue | 7.9   | AAA    | Yes, default link                     |
| Royal Blue    | 7.7   | AAA    | Yes                                   |
| Magnolia      | 6.9   | AA     | Yes                                   |
| Ironweed      | 6.3   | AA     | Yes                                   |
| Graphite      | 5.7   | AA     | Yes, secondary text                   |
| Shale Blue    | 4.9   | AA     | Yes                                   |
| Copper        | 4.6   | AA     | Yes, but narrow margin: avoid below 14px and never on Whisper/Ginger Beer (4.1 to 4.3) |
| Dogwood       | 3.5   | AA18   | Large text only                       |
| Eno           | 3.4   | AA18   | Large text only                       |
| Persimmon     | 2.3   | fail   | Decorative only                       |
| Piedmont      | 2.2   | fail   | Decorative only                       |
| Granite       | 2.0   | fail   | Decorative only                       |
| Dandelion     | 1.3   | fail   | Decorative only                       |

### White text on a colored fill (buttons, banners, slide backgrounds)

Same ratios as above. White text is safe on Navy, Royal, Prussian, Magnolia,
Ironweed, Shale, Cast Iron, Graphite and Copper. On Persimmon, Dandelion, Piedmont,
Eno, Dogwood and all pale neutrals use Cast Iron or Navy text instead.

### Text on Duke Navy

| Color        | Ratio | Rating |
|--------------|-------|--------|
| White        | 14.7  | AAA    |
| Ginger Beer  | 13.7  | AAA    |
| Whisper Gray | 13.2  | AAA    |
| Hatteras     | 11.7  | AAA    |
| Limestone    | 11.7  | AAA    |
| Dandelion    | 10.0  | AAA    |
| Shackleford  | 9.7   | AAA    |
| Granite      | 7.2   | AAA    |
| Piedmont     | 6.5   | AA     |
| Persimmon    | 6.3   | AA     |
| Eno          | 4.2   | AA18   |
| Copper       | 3.1   | AA18   |

Copper text on Navy fails for normal sizes. On Navy use Persimmon or Dandelion for
warm emphasis and keep Copper for rules, bars and shapes.

### Any other pairing

Run `python3 scripts/duke_brand.py contrast <fg> <bg>` with palette names or hex
values. It prints the ratio and rating. Do this for every group-supplied color.
