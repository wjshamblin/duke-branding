# Official Duke wordmark files

Downloaded from https://brand.duke.edu/logos/#downloads (Duke NetID required).
These are registered trademarks of Duke University. **Do not redistribute this
folder outside Duke**: exclude it when sharing or publishing the skill.

```
logos/
├── tight/                     USE THESE. Same artwork, canvas trimmed to exactly the
│                              required clear space (half the width of the capital D)
├── original/                  Untouched official files, very large built-in margin
└── subbranding-reference/     Official lockup option sheets and spec sheets (PDF)
```

Each folder holds both wordmarks (`duke_wordmark_*`, `duke_university_wordmark_*`)
in four colors (`navyblue_012169`, `royalblue_00539B`, `black`, `white`) as SVG and
transparent PNG.

## Which file

| Background                          | File color            |
|-------------------------------------|-----------------------|
| White, pale neutrals                | `navyblue_012169` (default) or `black` |
| Duke Navy, Royal, any dark solid    | `white`               |
| One-color black-and-white printing  | `black`               |

SVG for web, PowerPoint, Word (recent versions) and PDF. PNG for email and anything
that rejects SVG. For commercial print use the CMYK/Pantone EPS files from the
official zip, which are not bundled here because of their size.

## Sizing: read this before placing a wordmark

Minimum size is set by the capital D: at least 3/8 in tall in print, 24px on screen.
The D is only a fraction of the image height, so size the **image** as follows:

| File                              | D height as share of image height | Image height for a 24px D | Image height for a 3/8 in D |
|-----------------------------------|-----------------------------------|---------------------------|-----------------------------|
| `tight/duke_wordmark_*`           | 46%                               | 52px                      | 0.82 in                     |
| `tight/duke_university_wordmark_*`| 41%                               | 59px                      | 0.92 in                     |
| `original/*` (both)               | 23%                               | 104px                     | 1.62 in                     |

Aspect ratios (width : height): tight Duke 1.96, tight Duke University 1.74,
original 2.03. Always scale with the ratio locked.

The `tight/` files already include the mandatory clear space, so they may sit flush
against a layout edge or another element. With `original/` files the built-in margin
is about five times the requirement, which makes the mark look small and misaligned.

## Lockup geometry for slides, documents and graphics

Everything as a fraction of the **tight Duke wordmark image height** (h), so a lockup
can be built in any tool. Horizontal two-line design (E) from Duke's spec sheet:

| Element                                   | Value                              |
|-------------------------------------------|------------------------------------|
| Built-in margin on every side             | 0.248 h                            |
| Wordmark height (Duke's "y")              | 0.505 h, vertically centered       |
| Capital D width (Duke's "x")              | 0.495 h                            |
| To align the D with other content         | place the image 0.248 h further left |
| Separator position                        | image right edge minus 0.085 h     |
| Separator size                            | 0.505 h tall, 0.01 h thick (at least 0.75pt) |
| Unit name starts                          | separator plus 0.163 h             |
| Unit name starts, no-separator designs    | at the image's right edge (0.5x after the ink) |
| Two-line name: font size of each line     | 0.255 h (cap height 0.36 y)        |
| Two-line name: baseline to baseline       | 0.323 h, block centered on the wordmark |
| One-line name: font size                  | about 0.32 h                       |

Example: a 1.0 in tall image gives an 18pt two-line name on 23pt leading.

`tight/` is generated from `original/` by `python3 scripts/make_tight_logos.py`. Run
it again after replacing the originals.

If a file is missing, fall back to the placeholder in `references/logo-and-voice.md`
and tell the user. Group logos do not belong here. They live in `groups/<slug>/`.
