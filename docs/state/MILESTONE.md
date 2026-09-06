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

### Position [m1-now] — patched per PR

- Scaffolding: this founding commit.
- Renderer: not ported (task 0001; the source system exists in the
  founding session's tooling and lands with the task).
- qutebrowser wrapper and link policy: not built (task 0001).
- Outcome log: header row only; first data row lands with task
  0001's completion.
