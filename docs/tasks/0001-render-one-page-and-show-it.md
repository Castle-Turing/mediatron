Title: Task 0001 — render one page and show it
Model: standard
Milestone: m1-done
Model-because: the load-bearing decisions are already made and recorded in docs/state/MILESTONE.md — the engine is chosen ([m1-constraints]), the visual system exists and is being ported rather than designed, and the link policy is stated in [m1-intent]. What remains is transcription and documented configuration; a deep-tier implementer would add nothing the clause citations do not already bind, and the first task of a conventions-dogfooding repo *should* test whether the conventions carry a standard-tier worker.

# Task 0001 — render one page and show it

**Status: written at the project's founding, 2026-09-06, alongside
the conventions it exercises. The resident approved the founding
scaffold; this brief rides the founding commit as the queue's first
item and is implemented on its own branch.**

**Before starting:** read `AGENTS.md` (binding, especially the
status-update protocol — your PR description's summary follows it)
and `docs/state/MILESTONE.md` (this brief derives from [m1-done] and
is bound by [m1-constraints]).

## What to build

Two pieces, in the flake:

1. **`mediatron-render`** — markdown in, self-contained HTML page
   out, in the house visual system. The renderer is a port, not a
   design: the founding session's `md2page.py` (delivered alongside
   this repo's creation — ask the resident for
   the file if it is not already in `tools/`; its output is the
   eight research artifacts the resident has been reading) carries
   the palette (warm paper `#FAF9F6`, ink `#1C1F22`, verdigris
   accent `#2F7D6D`, amber `#9A6A1F`, and the dark-ground
   equivalents), the type stacks (Iowan/Palatino serif body,
   ui-monospace for machine-facing runs), verification badges for
   `[V]`/`[R]` markers, and the constrained-markdown conversion
   rules including two known fixed bugs (bold spans containing
   italics; bare URLs swallowing adjacent markers). Port it with its
   history: those two bugs stay fixed. Palette and type land as
   tokens a resident override can replace ([m1-out]'s
   mechanism/configuration split).
2. **`mediatron`** — a wrapper that renders FILE and opens it in a
   qutebrowser window configured for reading: no tabs, no status
   bar beyond what navigation needs, vim keys as qutebrowser ships
   them. Link policy per [m1-intent]: URLs under the local castle
   document roots open in the same window; everything else goes to
   `xdg-open`. qutebrowser's per-profile configuration and URL
   interception are documented features — configure, do not patch.

## Verification

Machine: the flake builds both; a fixture markdown file (commit one:
a status-update-shaped page exercising headings, a `[V]` badge, an
internal link, an external link) renders without unconverted
markers (`grep -c '\*\*' output == 0` is the founding session's
check, inherited). Human, and this task's falsifier: the resident
runs `mediatron` on the fixture — j/k scrolls, the internal link
stays in the window, the external link leaves it. If the page does
not feel like the research artifacts they have been reading, the
port missed the point regardless of what passes.

## On completion

Append the row to `docs/log/task-outcomes.tsv` ([m1-constraints]
second clause — the log's first data row is this task's), patch
[m1-now] in the same PR, and write the PR summary as a status
update per AGENTS.md.
