# How Duke Units Actually Apply the Brand

Observed on live Duke sites, measured from their stylesheets and computed styles.
Use this to make work look like it belongs at Duke, not just like it passes the rules.
These are patterns to follow, not content to copy: never lift text, photos or layouts
wholesale from a Duke site.

Survey date: 2026-09-21. Sites change, so re-check one before leaning hard on a detail.

## What almost every unit does

- **A solid blue band across the top** holding the reversed (white) wordmark, a thin
  separator, and the unit name. Navy for most units. Royal for Trinity and its
  departments.
- **The lockup follows the spec sheet to the letter.** Two lines, caps, wide tracking,
  lower-case italic preposition:
  `OFFICE of / INFORMATION TECHNOLOGY`, `SANFORD SCHOOL of / PUBLIC POLICY`,
  `PRATT SCHOOL of / ENGINEERING`, `TRINITY COLLEGE of / ARTS & SCIENCES`,
  `DEPARTMENT of / COMPUTER SCIENCE`.
- **Dandelion is the workhorse accent on blue.** OIT and HR set the unit name itself in
  gold on the navy band. It is the 10:1 pairing, so it is also the safest.
- **Merriweather headings with Open Sans body** is by far the most common pairing.
- **Body text is Cast Iron on white.** Blue is for bands, panels and headings.
- **Photos are large and real**: students, labs, campus. A solid navy panel carries any
  text, often overlapping the photo's edge rather than sitting on top of it.

## Measured, by site

| Site | Base | Accents seen | Headings / body | Notes |
|---|---|---|---|---|
| duke.edu | Navy | Royal, Copper, Persimmon | Montserrat / Open Sans | Full-bleed photo hero, centered wordmark |
| today.duke.edu | Navy (whole page) | Royal, Prussian, Hatteras | Montserrat / Montserrat | Caps section labels, white text on navy throughout |
| hr.duke.edu | Navy | Dandelion, Shale, Copper | Merriweather / Open Sans | Unit name "Human Resources" in gold, initial caps (design D) |
| oit.duke.edu | Navy | Dandelion, Shale, Copper | Merriweather / Open Sans | Unit name in gold, two-line caps (design E) |
| sanford.duke.edu | Navy | Dandelion, Shale, Copper | Merriweather / Open Sans | Same platform as HR, OIT and Research |
| research.duke.edu | White header, navy text | Dandelion, Shale, Piedmont | Merriweather / Open Sans | Dandelion rule under the page heading |
| trinity.duke.edu | **Royal** | Dandelion, Ginger Beer | Merriweather / Open Sans | Shared Trinity theme |
| cs.duke.edu | **Royal** | Dandelion, Ginger Beer | Merriweather / Open Sans | Parent "Trinity College of Arts and Sciences" in tiny caps under the wordmark |
| pratt.duke.edu | White header, navy text | Copper, Eno, Persimmon, purple imagery | Roboto / Merriweather | Copper call-to-action buttons |

HR, OIT, Sanford and Research run one shared Duke web platform, which is why they
match. A new office, center or lab with no identity of its own should look like them.

## Idioms worth borrowing

| Idiom | How to do it |
|---|---|
| Band header | `.duke-band` in the stylesheet: full-width Navy or Royal, reversed wordmark, lockup. Add `is-gold` to the unit name for the OIT/HR look |
| Heading with a gold rule | `.duke-heading-rule`: a short 3px Dandelion bar under a heading. On white it is decoration only, never text |
| Ghost button with an arrow | `.duke-btn is-ghost is-arrow`: caps, wide tracking, 1px navy border, trailing arrow |
| Overlapping panel | A solid Navy block offset so it overlaps a photo's corner, carrying a short headline and one link |
| Caps section label | Small caps label above a section, wide-tracked, in the accent text color |
| Nested unit | Parent name in very small caps directly under the wordmark, department in the lockup |

## Where practice bends the rules (do not copy these)

Live sites are maintained by many hands over many years, and a few details drift from the
brand guide. Seen in this survey:

- A green button darkened to pass contrast. Piedmont with white text is only 2.2:1, so the
  instinct is right, but the darker green is no longer a palette color. Use Magnolia or
  Navy for that job instead.
- Headings set in tints or browns that are not in the palette.
- Typefaces outside the official nine.

Follow the shared patterns above, not the drift.
