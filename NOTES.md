# Field test notes

A skill is only as good as its last real use. This file records what happened when
the skill was used on real work, what fell short, and what changed as a result. It is
the "Iterate" step of skill development made visible.

## 2026-09-21: reviewing an existing deck

**Task:** check and enhance `MCP-Servers-Duke-OIT.pptx`, a 25-slide tech talk built by
a python-pptx script. The skill had been written that morning and never used.

**Result:** the deck went from 28 audit problems to 0. Added the official Duke
wordmark and an OIT lockup built to Duke's spec sheet, real slide titles for screen
readers, alt text, a Duke theme in the file, and Roboto Mono in place of Courier New.
All 20 text/fill color pairings already passed WCAG AA, and the deck's own layout was
left alone because it was already on-brand.

### What the skill got wrong or left out

| # | What happened | Root cause | Change made |
|---|---|---|---|
| 1 | Reported "brand fonts are not installed, PowerPoint will substitute them." False. | `typography.md` said Office never carries Google Fonts. In Microsoft 365 every Duke face except Cormorant Garamond is an Office cloud font, fetched on demand. They do not appear in `fc-list`, which is what misled the check. | Rewrote the section. Added how to inspect the Office font cache and catalog, and to confirm with `pdffonts` on a PDF exported by the real app. |
| 2 | The whole audit was improvised. | The skill only described making new things. "Check this" is a different job. | Added step 0 to `SKILL.md` with a decision diagram, and "Reviewing an existing deck" to `powerpoint.md`. |
| 3 | Courier New was missed on a visual pass of all 25 slides. | Eyes are bad at this. It was caught only after the audit script existed. | `scripts/pptx_tools.py audit`: theme, fonts, off-palette colors, contrast on filled shapes, real titles, duplicate titles, alt text, small text, wordmark presence and size. |
| 4 | "Define theme colors", "every slide has a title" and "alt text" each took non-obvious XML work. | The guide said what, not how. python-pptx has no theme API; the Blank layout has no title placeholder; the placeholder is created first so a header band covers it. | `pptx_tools.py theme` does the theme. A python-pptx technique table covers the rest. |
| 5 | Lockup geometry had to be re-derived by hand for slides. | It existed only as CSS. | Added a table to `assets/logos/README.md` with every measure as a fraction of the wordmark image height. |
| 6 | The layout table read as mandatory. Following it would have meant restyling a deck that was already compliant. | Defaults were written as rules. | Marked as defaults for new decks. Added "respect what is already right" and "flag, do not silently change" to the review steps. |
| 7 | A LibreOffice render looked fine but showed the wrong fonts. | No guidance on verifying output. | Added "Verify the render": LibreOffice for layout, PowerPoint's own export plus `pdffonts` for fonts, and the sandbox gotcha (PowerPoint cannot write to `/tmp`). |
| 8 | No profile for the unit in question. | Only three starter groups. | Added `groups/oit/`. |

### What worked

- The group lookup, token resolver and contrast command: 20 pairings checked in one
  command, against numbers that match Duke's published grid.
- The logo sizing table. The title-slide wordmark was sized correctly on the first try.
- Refusing to guess: the font claim was checked against Office's own catalog before it
  went into the skill, and two over-broad sentences were walked back before shipping.

### Still open

- The audit checks contrast only for text inside a filled shape. Text in a plain text
  box over a band or a photo is not checked.
- The audit finds a wordmark by its alt text ("Duke"). A deck using a wordmark with
  different alt text reads as having none.
- Only `.pptx` has an audit. Word and HTML reviews are still by hand.
- Cloud-font availability was verified on macOS only.
- Group accent colors are still editable defaults, not standards confirmed by the units.

## 2026-09-21 (later): first measured evaluation

Ran Anthropic's `skill-creator` process: three realistic prompts, each run by a fresh
agent **with** the skill and **without** it, graded by script. Definitions and grader are
in [`evals/`](evals/). Raw run outputs are kept outside this repository.

| Test | With skill | Without |
|---|---|---|
| New 6-slide deck for Computer Science | 13/13 | 9/13 |
| Audit and fix a seeded off-brand deck | 13/13 | 11/13 |
| Canvas course page | 10/11 | 10/11 |
| **Overall** | **97%** | **82%** |

Run time and token cost were not captured: the completion notices that carry them
never reached the orchestrating session.

### What the numbers hid, and the logs showed

- **The skill's main Canvas instruction was wrong.** It said inline `<style>` blocks and
  Google Fonts `<link>` tags survive in Canvas. The with-skill agent did not trust it,
  read Canvas's sanitizer source, and found both are stripped. Verified independently.
  Following the skill as written would have produced an unstyled page. The claim came
  from the original skill and was carried forward unchecked. Fixed: new inline-style
  Canvas template, a verified keep/strip/drop table, and the old template renamed for
  standalone pages.
- **Without the skill, the Canvas page looked more like Duke.** The baseline reached for
  a navy band and serif headings. The skill's page had a plain header and a broken logo
  image. Model knowledge of Duke's look is already good: the skill adds correctness
  (real wordmark, real navy, accessibility), and must not subtract style.
- **My own stylesheet held two off-palette tints** and a navy-to-accent gradient that
  contradicts the skill's "never fade the blues" rule. The grader caught the tints.
- **Three of my eleven Canvas checks were wrong**, not the outputs: "exactly one h1"
  (Canvas supplies it), "loads Google Fonts" (it cannot), and a literal `3x` that both
  decks wrote as `3×`. Corrected because they encoded false facts. A grader is a claim
  about the world and needs checking like any other.
- **The audit tool was blind where it mattered most.** It judged contrast only inside
  filled shapes, so it missed Persimmon and gray text on white, the worst problems in
  the seeded deck. A first fix that assumed a white background produced 142 false
  alarms on a good deck. The working fix looks up which filled shape actually lies
  beneath each text box, in z-order, plus the slide's own background. Also added: typed
  "Duke" detection, file-name alt text, slide numbers on colors, de-duplication.
- **All three deck agents wrote their own build helpers.** That is the signal to bundle
  a helper library. Not done yet.

### What the survey of real Duke sites changed

Measured twelve live sites (stylesheets, computed styles, screenshots). Recorded in
`references/real-world-patterns.md`.

- Trinity and Computer Science use **Royal** as the base, not Navy. Groups can now set
  `base`, limited to the two Duke blues.
- HR, OIT, Sanford and Research share one platform: Merriweather + Open Sans, Navy,
  **Dandelion** accent, unit name in gold on the band. The HR profile was a guess
  (EB Garamond, Royal accent) and was wrong. All four profiles now match their sites.
- CS's real lockup is "DEPARTMENT of COMPUTER SCIENCE".
- New stylesheet idioms taken from practice: blue band header, gold heading rule,
  eyebrow label, overlapping panel, arrow button.

### Added

`assets/showcase/` (pick a look by eye), `assets/examples/` (finished pieces to imitate,
rebuilt from the templates so they double as a template test), and the scripts that
generate both.

### Still open

- Iteration 2 has not been run. The fixes above are untested against the three prompts.
- A python-pptx helper library, since every deck run rebuilt one.
- No audit for HTML or Word. Trigger accuracy of the description is still unmeasured.
- Only one model was tested.

## 2026-09-21 (round two): did the fixes work?

Re-ran the three prompts against the fixed skill. The no-skill baseline and the old
skill's outputs were carried forward from round one, and all three were graded by one
version of the grader, with three checks added from what round one taught (a blue band
header, no image that renders broken, contrast judged against the shape beneath).

| Test | New skill | Old skill | No skill |
|---|---|---|---|
| New deck for Computer Science | 14/14 | 14/14 | 10/14 |
| Canvas course page | **13/13** | 10/13 | 12/13 |
| Audit and fix an off-brand deck | 14/14 | 14/14 | 12/14 |
| **Overall** | **100%** | 93% | 83% |

Canvas went from the skill's worst medium, behind no skill at all, to a clean pass. The
page now looks like cs.duke.edu: Royal band, gold unit name, serif headings over a gold
rule, and no broken logo. Runs took about six minutes, against twelve in round one.

### Read this before trusting those numbers

- **Decks hit the ceiling in both rounds**, so they show no improvement and cannot. The
  evidence for decks is the friction logs, which got shorter and milder.
- **Eval 3 was contaminated in round two.** The gallery's before/after picture was made
  from eval 3's own input deck, and the agent noticed: "the example is nearly this exact
  deck." Its round-two result is not evidence. Eval 3 needs a new seeded deck.
- **Two agents (evals 1 and 2) opened `eval_metadata.json`**, left in their working folders
  by mistake, which lists round one's checks. Both said so unprompted. The round-two checks
  were not in that file, and both runs passed them, so those stand.
- One run per configuration. No variance estimate, one model.
- **Tested in one agent only.** The skill follows the open Agent Skills standard and passes
  its reference validator, and nothing in it names a product, but every run so far was in
  Claude Code. It has not been loaded in ChatGPT, Codex, Cursor, Copilot or Gemini CLI. The
  "if scripts cannot run" path in `SKILL.md` in particular is untested.

### What round two's logs asked for, and got

- Theming by find-and-replace broke when two roles shared a hex value, which made the
  CS page nearly two-color. Replaced with named placeholders and
  `duke_brand.py render <template> --group <slug>`. The gallery script lost its fix-ups.
- Example sources embedded a 38k-token base64 logo no agent could read. They now
  reference a hosted URL, are 5 KB, and can be committed.
- Stale docs: the inheritance diagrams still described the guessed CS profile; the deck
  guide said "Navy" where it meant the group's base blue.
- New resolver output `rule_on_white`, because a Dandelion accent is invisible as a rule
  on a white slide. Multi-pair `contrast`. Quieter `theme`. In-place title retrofit.

### Asked for twice, still not built

A python-pptx helper library. Both rounds' deck agents wrote their own text, shape,
lockup and footer helpers from scratch. That is the clearest remaining signal.

## 2026-09-21 (evening): packaging for automatic updates

Question: can a skill keep itself current, in ChatGPT as well as Claude? Answer: yes in
both, but only for a **plugin listed in a marketplace**, never for a bare uploaded skill.

- Claude Code's documentation states that a plugin with `SKILL.md` at its root is loaded
  as a single-skill plugin, so this repository needed no restructuring: two small files in
  `.claude-plugin/` made it a plugin and a one-plugin marketplace.
- OpenAI's workspace import lists `.claude-plugin/marketplace.json` among its supported
  formats, so the same file serves both vendors. It reads github.com only, hence a private
  GitHub mirror of the GitLab repository.
- No `version` in the plugin manifest, deliberately: the commit becomes the version, so
  every push is an update and nobody has to remember a release step.
- **Tested:** `claude plugin validate`, then marketplace add and plugin install from the
  local folder, from GitLab over SSH and from the GitHub mirror, each in a throwaway config
  folder. **Not tested:** the ChatGPT workspace import, which needs a workspace admin.
- **The catch:** a marketplace install comes from git, and the official wordmark files are
  not in git. Installing from a local folder hid this, because it copied them. Installing
  from the remotes showed zero wordmark files. The README now says which install route
  keeps the wordmarks. A durable fix would be a wordmark folder outside the skill, the way
  group profiles already have one.

### General lessons for writing skills

1. **Use it on real work the same day.** Every gap above was invisible until then.
2. **A confident, wrong sentence in a reference costs more than a missing one.** The
   model believes its references. State how a fact was verified, or do not state it.
3. **If a step needs judgment from eyes, give it a script.** "Check the fonts" became
   reliable only when it became a command with an exit code.
4. **Say what, and how.** A rule with no mechanism gets skipped or reinvented each time.
5. **Write defaults as defaults.** Otherwise the skill steamrolls good existing work.
6. **Separate making from reviewing.** They share rules but not a workflow.
7. **Measure against no skill at all.** The model already knows a lot. The skill has to
   beat that, and on one task out of three it did not.
8. **Read the logs, not just the scores.** The most important finding of the evaluation
   scored as a tie.
9. **Look at what real practitioners do.** A rules document tells you what is allowed.
   Twelve live sites showed what is normal, and corrected four profiles.
10. **Keep test inputs out of the skill.** An example that doubles as an eval input hands
    the agent the answer. Same for grading files left in a working folder.
11. **When every run passes, the test has stopped measuring.** Add harder checks, or the
    next improvement will be invisible.
