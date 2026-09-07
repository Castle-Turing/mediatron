Title: Task 0001 — render one page and show it
Model: cheap
Milestone: m1-done
Model-because: the load-bearing decisions are made and recorded in docs/state/MILESTONE.md — the engine is chosen ([m1-constraints]), the visual system exists and is being ported rather than designed, link classification and title provenance were resolved at elicitation 2026-09-06 ([m1-links], [m1-provenance]), and the only remaining open shape is the override seam, carried as written uncertainty ([m1-seam]). What remains is transcription and documented configuration; a deeper tier would add nothing the clause citations do not already bind, and the first task of a conventions-dogfooding repo *should* test whether the conventions carry a cheap-tier worker — Model: cheap rides this machine's emcee roster to DeepSeek Flash, per [m1-ambig-subagent]'s resolution.

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
   design: the founding session's `md2page.py` (in `tools/`; its
   output is the eight research artifacts the resident has been
   reading) carries the palette (warm paper `#FAF9F6`, ink `#1C1F22`,
   verdigris accent `#2F7D6D`, amber `#9A6A1F`, and the dark-ground
   equivalents), the type stacks (Iowan/Palatino serif body,
   ui-monospace for machine-facing runs), verification badges for
   `[V]`/`[R]` markers, and the constrained-markdown conversion
   rules including two known fixed bugs (bold spans containing
   italics; bare URLs swallowing adjacent markers). Port it with its
   history: those two bugs stay fixed. Palette and type land as
   tokens a resident override can replace ([m1-seam]: tokens plus a
   documented attachment point in this milestone — the override
   loading mechanism itself is later work, not this task).
   Provenance per [m1-provenance]: the input file carries a small
   front-matter block at its top declaring `title:` and `eyebrow:`;
   the renderer parses it, strips it, and feeds both to the page —
   `md2page.py`'s two extra argv slots are gone for this package.
   Relative links pass through untouched (they stay relative in the
   HTML), so the page remains navigable from its file location.
2. **`mediatron`** — a wrapper that renders FILE and opens it in a
   qutebrowser window configured for reading: no tabs, no status
   bar beyond what navigation needs, vim keys as qutebrowser ships
   them. Link policy per [m1-links]: relative and file:// links
   resolve against the rendered file's location and stay in the
   window; http(s) links whose URL matches a prefix in a configured
   castle-roots allowlist also stay in the window; everything else
   goes to `xdg-open`. The allowlist lives in a small configuration
   file the wrapper reads (ship it with an example and a documented
   default location; the resident's private roots are never
   committed). qutebrowser ships both the per-profile configuration
   and URL interception this needs — configure, do not patch. The
   flake's `packages.mediatron` must close over qutebrowser itself
   so `nix run` works on a host that has not installed it any other
   way.

## Verification

Machine: the flake builds both; a fixture markdown file lives in
`examples/` (commit one, per [m1-ambig-fixture]): a
status-update-shaped page carrying the front-matter block
([m1-provenance]), headings, a `[V]` badge, one relative internal
link (its target also committed, rendered to the same directory),
and one plain external link. It renders without unconverted markers
(`grep -c '\*\*' output == 0` is the founding session's check,
inherited) and with the front-matter block gone from the output.
Human, and this task's falsifier: the resident runs `mediatron` on
the fixture — j/k scrolls, the internal link stays in the window,
the external link leaves it. If the page does not feel like the
research artifacts they have been reading, the port missed the
point regardless of what passes.

## On completion

Append the row to `docs/log/task-outcomes.tsv` ([m1-constraints]
second clause — the log's first data row is this task's), patch
[m1-now] in the same PR, and write the PR summary as a status
update per AGENTS.md.
