# The current milestone

`docs/state/` truth. Clause keys in brackets; `[stated <date>]` is
the resident's words, `[inferred]` is the system's reading held
until confirmed.

## Milestone 1 — one page, shown

Declared by the resident 2026-09-06 at the project's founding.

### Intent [m1-intent]

[stated 2026-09-06] Documents like a status update should open as a
beautiful web page in the house style and colors — not a text
editor — in a browser window with no chrome, navigated with basic
vim keybindings. External links open in the default browser; links
to other castle documents open in the same chromeless window.

### Done looks like [m1-done]

[inferred, sized deliberately small to force the plumbing] Running
`mediatron <file>` on one status-update-shaped markdown file renders
it with the house visual system and shows it in a chromeless window
where `j`/`k` scroll; one link to another castle document opens in
the same window; one external link opens in the resident's default
browser.

Extended at elicitation 2026-09-06 by [m1-links] (link
classification), [m1-provenance] (front-matter title and eyebrow),
and [m1-seam] (the override boundary).

### Explicitly out [m1-out]

[stated 2026-09-06] The warm always-waiting browser — anticipated
for speed, deferred until slowness is measured. The Dovetail-verb
question — deliberately undecided. [inferred] Any generator for
status updates: they are written by hand here (AGENTS.md's
reporting protocol); the single generator effort lives in Castle
Turing, and where a shared one would live is an open question the
resident holds.

### Constraints binding this milestone [m1-constraints]

- **The engine is bought.** Prerequisite: milestone-1 work builds on
  qutebrowser for the window and vim grammar. Authority: the
  resident chose this 2026-09-06 and may reverse it. Fallback: a
  custom minimal shell is the recorded backlog alternative.
  Consequence of violation: hand-building vim navigation repeats the
  exact effort the choice exists to avoid. [stated 2026-09-06]
- **The baseline starts before the experiments.** Prerequisite:
  every completed task attempt appends its row to
  `docs/log/task-outcomes.tsv`, from task 0001 onward. Authority:
  the resident may waive for a given task, knowingly. Fallback:
  none — the row is one line; write it. Consequence of violation:
  the pre-intervention baseline this greenfield uniquely offers is
  forfeit for every measure missing its rows. [inferred from the
  founding direction; endorsed by the resident 2026-09-06]

### Decided at elicitation, 2026-09-06 [m1-elicited]

The resident's answers to the founding brief's open ambiguities
([m1-elicit]); the [inferred] readings below were chosen among the
readings written down beforehand, none were defaulted.

- [m1-links] [stated 2026-09-06] Link classification for [m1-done]:
  relative links and file:// links are internal and resolve against
  the rendered file's location; additionally a configured allowlist
  of URL prefixes names castle roots, and http(s) links matching a
  listed prefix stay in the window. All other links leave it. Tag
  link-classification cleared.
- [m1-provenance] [stated 2026-09-06] The markdown file declares its
  own title and eyebrow in a small front-matter block the renderer
  parses and strips; no title/eyebrow arguments on the milestone-1
  command line. Tag provenance-sourcing cleared.
- [m1-seam] [inferred, tag override-seam carried] Milestone 1 ships
  palette and type as replaceable tokens with a documented
  attachment point; the override loading mechanism itself is later
  work, not this milestone. Carried into task 0001 as written
  uncertainty.
- [m1-ambig-done] [inferred, tag completion-definition carried]
  "Milestone 1 complete" reads as PRs-merged-plus-resident-run: the
  closing status update reports merged PRs as receipts and the
  resident's own falsifier run on the fixture as the open gate,
  never "complete" as this project's assertion.
- [m1-ambig-subagent] [stated 2026-09-06] Implementation is
  dispatched through emcee with task briefs at `Model: cheap`,
  which this machine's roster maps to
  opencode/deepseek-v4-flash. Task 0001's founding `Model:
  standard` is flipped to cheap with the reasoning rewritten, in the
  same change. The sprint's cap passes this session's declared
  budget, 25 USD. Tag subagent-reference cleared.
- [m1-ambig-fixture] [inferred, carried] The fixture markdown lives
  in an `examples/` directory riding the task 0001 change; its
  internal link is relative, exercising [m1-links]'s file side.

### Position [m1-now] — patched per PR

### Position [m1-now] — patched per PR

- Scaffolding: founding commit; elicitation PR #1 merged 2026-09-06
  (records [m1-links], [m1-provenance], [m1-seam]; pin flake.lock).
- Renderer: implemented as `src/mediatron_render.py` on task 0001's
  branch — the md2page.py port plus front-matter title/eyebrow and
  relative-`.md` link rendering (PR #2, awaiting review).
- qutebrowser wrapper and link policy: implemented as `src/mediatron`
  with a generated reading profile (chromeless, `F` hands external
  links to xdg-open via a shipped userscript) and the castle-roots
  allowlist in `~/.config/mediatron/config` (example committed; PR
  #2, awaiting review). Real-display behavior unverified until the
  resident's falsifier run.
- Outcome log: first data row appended with task 0001's completion
  (PR #2).
