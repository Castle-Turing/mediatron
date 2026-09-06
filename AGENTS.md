# Agent guidance — Mediatron

You are in the public Mediatron repo, part of the Castle Turing
ecosystem. Read `docs/vision.md` once per session. These instructions
are deliberately prescriptive and self-contained: they are the
distilled, binding form of Castle Turing's 2026-09 research series,
and you follow them as written rather than re-deriving them — the
research is that project's record; this file is this project's rule.

## Hard rules

- **Never write personal data into this repo.** No credentials, no
  real correspondents, nothing from the resident's private layer —
  not in code, docs, fixtures, or commit messages. The house *style*
  is public mechanism; the resident's *taste* is private
  configuration that overrides it.
- **Every change passes the mechanism/configuration test**: if a
  feature cannot split into public mechanism plus private
  configuration, the design is not done — say so instead of merging.
- **Docs are written for strangers** who have never seen Castle
  Turing. Cross-project citations name their source ("Castle
  Turing's Proposal 06") and are never load-bearing: a rule this
  repo depends on is restated here in full.

## Truth and records

- `docs/state/` is what is true *now* — maintained, authoritative,
  patched **in the same PR** that changes what is true, with the
  state diff read as part of review. Everything else in `docs/` is a
  record of what was decided or found, cited by task number as a
  name ("task 0003"), never by path. When you catch yourself citing
  a record as current authority, extract the load-bearing content
  into `docs/state/` in that same PR.
- State documents are small structured prose with bracketed clause
  keys. `[stated <date>]` marks the resident's words; `[inferred]`
  marks your reading, held until confirmed. Binding constraints
  carry four explicit fields in prose: prerequisite, authority,
  fallback, consequence. Constraint language is explicit, never
  hedged. Deletions from state get explicit review attention.
- Code comments state constraints the code cannot show, plus a task
  number as a name; the story of how a constraint was learned lives
  in the brief, not the comment.

## Work intake — the elicitation protocol

Binding whenever you take work from the resident's words, before any
brief is written:

1. Transcribe the ask into a state document draft: clauses with
   keys, each `[stated]` or `[inferred]`, each carrying tags for its
   unresolved ambiguities (word-meaning, structure, reference,
   vagueness). An ambiguity is *written down*, never resolved by
   silently picking a reading — silent commitment is the failure
   this protocol exists to prevent.
2. To choose a clarifying question, sketch two or more
   interpretations consistent with the draft and ask what best
   discriminates between them. Never ask yourself "what would a good
   question be?" in the abstract.
3. Every question you ask cites the clause key and ambiguity tag it
   would resolve. A question with no citable tag is a defect.
4. Budget one to two well-targeted questions; ask goal-level
   ambiguities first — they lose almost all value once work starts;
   constraint-level ambiguities may stay as tags in the document.
   Asking nothing is a legitimate exit and must be an explicit
   decision, not a drift.
5. Never use steering question forms: no leading questions, no
   forced choices that presume one of your options is right, no
   declarative "that's correct, right?" framings.
6. Close with the clearinghouse probe — "what have I not asked that
   matters?" — and then exit by **read-back**: restate what you now
   believe is being built (the document, not the transcript) and get
   the resident's verdict on the restatement. The resident's answers
   patch clauses and clear tags; tags still standing carry forward
   into the work as written uncertainty.

## Reporting — the status update

Binding whenever you report on work (end of a task, a PR
description's summary, a session's close). Write it by hand in this
shape; there is no generator here, deliberately.

1. **Intent restated**: the milestone clause this work served, in one
   or two sentences from `docs/state/MILESTONE.md` — never assumed
   held in the reader's head.
2. **Threats and drift before accomplishments**: what could go wrong
   next, and anything that moved away from the milestone.
3. **What changed — receipts only.** Every line is derived from
   artifact state and carries the citation that makes checking
   cheaper than re-deriving: "PR #3 merged, checks green [links]."
   **Completion vocabulary is banned**: never "done," "complete,"
   "finished," "successfully" as your own assertion — a merged PR
   with green checks is a receipt; whether the work is *right* is
   the resident's verdict, and this rule exists because confident
   closure is a trained stylistic default, not an honest signal.
4. **`[unverified]` marked in place** on any line you could not
   ground in an artifact — never smoothed over or omitted.
5. **Verdicts requested**: the decisions only the resident can make,
   cheapest first, each naming what changes depending on the answer.
   A request nothing depends on is a defect.
6. One screenful. More detail raises confidence without raising
   accuracy; when there is more to say, link it.

## Measurement, from task zero

`docs/log/task-outcomes.tsv` is append-only, one row per completed
task attempt, written by whoever completes it (columns in the file
header). It exists so that this repo has a pre-intervention baseline
for every workflow experiment ever run on it — the property no
retrofit can recover. Rows are receipts: counts, dates, outcomes,
never judgments. Do not skip the row because the task felt trivial;
the baseline's value is its completeness.

## Tasks and the queue

`docs/backlog/` holds deferred work, one plain-text file per item,
named as a statement of the problem. `docs/tasks/` holds numbered
briefs; a brief is committed on the branch that implements it, and
every piece of implementation work gets one, sized by
proportionality. Task-file headers: `Title:` (required), `Model:`
with `Model-because:`, `Requires:` with `Requires-because:`,
`Milestone:` naming a `docs/state/MILESTONE.md` clause key or
`none — hygiene`. Keep every single-line key *above* any header
value that wraps: queue parsers stop reading headers at the first
wrapped line, so a key below one silently does not exist.

Do not commit to `main` from an agent session; work merges through
PRs the resident reviews. Merged branches are swept, local and
remote. Before opening a PR, state-changing git sequences begin by
confirming the current branch — a session once wrote forty minutes
of one task onto another task's branch by skipping this.
