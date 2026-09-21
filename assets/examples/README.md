# Examples gallery

Finished pieces to imitate. All copy is invented; nothing is taken from a Duke site.
The HTML ones are rebuilt from the skill's own templates by
`python3 scripts/make_examples.py`, so they also prove the templates still work.

| Picture | What it shows | Source |
|---|---|---|
| `web-page-oit.png` | Standalone page for OIT: blue band with the gold two-line lockup, overlapping navy panel, gold heading rule, cards, arrow button | `src/web-page-oit.html` |
| `canvas-page-cs.png` | Canvas page for Computer Science on Trinity's Royal base. Inline styles only, starts at `<h2>`, shown inside a simulated Canvas page | `src/canvas-page-cs.html` |
| `email-hr.png` | Email for HR: table layout, inline styles, gold unit name, dark text on the gold button | `src/email-hr.html` |
| `deck-group.png` | Six-slide deck for Computer Science on Trinity's Royal base: official wordmark in a "DEPARTMENT of COMPUTER SCIENCE" lockup, Dandelion accent, Merriweather + Open Sans | built with python-pptx |
| `deck-audit-before-after.png` | An off-brand deck (guessed blue, Comic Sans, typed "DUKE", red and green boxes) and the same deck after a review | `scripts/pptx_tools.py audit` |

The brand showcase (palette, themes, pairings, lockups, every group) is in
`assets/showcase/`.
