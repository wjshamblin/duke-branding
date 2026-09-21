# Wordmark, Lockups, Imagery and Voice

Sources: https://brand.duke.edu/logos/, https://brand.duke.edu/branding/,
https://brand.duke.edu/duke-identity/, https://brand.duke.edu/imagery/

The identity graphics are registered trademarks of Duke University.

## The wordmark

Two versions, both acceptable: **Duke** and **Duke University**. Set in Garamond
LT 3. Used on stationery, print, websites and digital properties, alone or combined
with an entity name under the sub-branding rules below.

Rules:

1. Always use an official wordmark file. Never recreate it.
2. No alterations of any kind: no recolor, stretch, outline, shadow, or effects.
3. Never place it on, or surround it with, a pattern or busy image.
4. Never rotate it or render it in 3D.
5. Add no copy, images or other elements to it without approval.
6. Resize with the aspect ratio locked.
7. **Clear space:** half the height of the capital D, on all four sides.
8. **Minimum size:** capital D at least 3/8 in (9.5 mm) tall in print. On screen keep
   the D at least 24px tall.
9. **Print placement:** at least 1/2 in from the top and edges of the page.

### Files

Official files are bundled in `assets/logos/`. **Read `assets/logos/README.md` before
placing one**: it has the color-to-background table and the sizing table. Two things
catch people out:

- Use the `tight/` files. The `original/` files have a huge built-in margin.
- The capital D is only 46% of the tight image height (41% for Duke University).
  Size the image, not the D: at least 52px / 0.82 in tall (59px / 0.92 in for Duke
  University).

Navy or black version on white and pale neutrals. White (reversed) version on Navy,
Royal or another dark solid.

### When no official file is available

If `assets/logos/tight/` is empty (for example the skill was shared without it):

- **HTML:** use the `.duke-wordmark` text placeholder from `assets/duke-alternate.css`.
- **PowerPoint / Word / PDF:** leave a labelled placeholder box sized for the wordmark.
- Always tell the user the placeholder must be replaced with the official file before
  the piece goes out, and give them the download link from
  `references/brand-resources.md`.

## Sub-branding: school and department marks

A unit's mark = Duke wordmark + separator + unit name. Seven horizontal and seven
stacked designs are sanctioned. The spec sheets and option sheets are in
`assets/logos/subbranding-reference/`. Read the relevant PDF when building a lockup
as a standalone graphic. A unit's own finished lockup file always beats a typeset one.

Units of measure on the spec sheets: **x** = width of the capital D.
**y** = height of the wordmark. Clear-space margin around the whole mark = 0.5x.

**Unit name typography** (two sanctioned styles):

| Style                  | Spec                                                        | Designs |
|------------------------|-------------------------------------------------------------|---------|
| Caps (most common)     | Open Sans Semi-Bold, all caps, wide tracking                | A, C, E, F, G |
| Initial caps           | Open Sans Regular, initial caps, normal tracking            | B, D    |
| Prepositions, articles | Open Sans Regular Italic, lower case (`of`, `the`, `for`, `and`) | E, F, G |

The brand website words this as "nouns in Open Sans Bold, prepositions and articles
in Open Sans Regular Italic". The spec sheets are the detailed source, so use
Semi-Bold.

**Horizontal marks**

- Separator: vertical rule, height y, thickness 0.02x, same color as the wordmark,
  with 0.33x of space on each side (0.4x after it for a single-line name).
- Single-line name: vertically centered on the wordmark.
- Two-line name: each line's cap height 0.36y with a 0.28y gap, so the block is
  exactly y tall and aligns top and bottom with the wordmark.
- **Contrasting color:** when the unit name is set in a color that contrasts with the
  wordmark (for example Eno), omit the separator entirely and leave 0.5x of space.
- With an entity symbol: the symbol replaces the separator, 1.2y to 1.4y tall,
  0.4x to 0.5x after the wordmark, then 0.3x before the name.

**Stacked marks**

- Separator: horizontal rule, thickness 0.02y, 0.33y of space above and below.
- A single-word name is scaled to justify exactly with the wordmark's width.
- A longer name may overhang the wordmark equally on both sides, and the rule extends
  with it.
- Contrasting color: no rule, 0.5y of space.
- With a symbol: symbol to the left, 1.5y to 1.75y tall, vertically centered or
  aligned to the text baseline.

HTML, using the bundled stylesheet (geometry above is already encoded in the CSS):

```html
<header class="duke-header">
  <img class="duke-wordmark-img" src="[duke_wordmark_navyblue_012169.svg]" alt="Duke">
  <span class="duke-lockup-divider"></span>
  <span class="duke-unit is-two-line">Trinity College <em>of</em><br>Arts &amp; Sciences</span>
</header>
```

Variants: `is-initial-caps` for the Regular initial-caps style. `is-contrast` for a
contrasting-color name, and then delete the divider span. A nested unit may add
`<span class="duke-unit-parent">` for its parent on a small second line. That is a
web-header convenience, not one of Duke's fourteen designs, so never use it when
producing a logo file.

## Co-branding: Duke wordmark beside another Duke entity's logo

When a group has its own logo and it appears in the same design as the wordmark:

- The wordmark sits on the **same plane** as the other mark (same baseline or row).
- The wordmark is **never locked up** with the other mark. Keep them visibly
  separate: opposite ends of a header, or a gap of at least the wordmark's full height.
- The wordmark follows its own size, color and clear-space rules regardless.
- The wordmark is **never larger** than the other mark.

## Dual branding with outside institutions and partners

Do not design this unaided. Direct the user to the Office of Trademark Licensing:
https://communicators.duke.edu/design/trademark-licensing/. The same applies to
merchandise, apparel and any athletic mark. This skill does not cover the Blue Devil
or athletics identity.

## Imagery

Duke is "a vibrant, diverse and ambitious community" and imagery should show that.
That sentence is the whole of the public guidance; the detailed mood boards are
behind NetID. The points below are working defaults, so defer to the mood boards
for anything high-profile.

- Prefer real Duke photography over generic stock: photo library and mood boards are
  linked in `references/brand-resources.md` (NetID).
- People first, candid over posed, natural light, real campus and Durham settings.
- Never set the wordmark over a busy part of a photo. Use a solid Navy band or a
  clear, quiet region of the image.
- Text over photos needs a solid or near-solid panel behind it to hold AA contrast.
- Every image in a digital piece gets alt text.
- Never generate or imply images of real, identifiable Duke people.

## Voice and tone

Shared values: **respect, trust, inclusion, discovery, excellence.**

Tone words Duke uses for itself: strength, community, confident, bold, engage,
curious, partner, purpose, transform, pride.

Five strategic tenets, useful as framing for institutional messages: empower the
boldest thinkers; transform teaching and learning; strengthen the campus community;
partner with purpose; engage the global network.

In practice (working defaults derived from the above, not quoted Duke rules):

- Confident and warm. State things plainly. Active voice.
- Plain language over jargon. Short sentences. Lead with what the reader needs.
- People first and inclusive. Humble about Durham and community partnerships:
  Duke "partners with" and "learns from", it does not "help" or "save".
- No hype: avoid "world-class", "revolutionary", "cutting-edge", "synergy".
- First reference "Duke University", then "Duke". Units: full name first, then the
  short name from the group profile.
