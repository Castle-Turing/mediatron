# Merged code PRs were never cross-reviewed

**What.** The first org-wide conformance sweep — the merged-without-review
receipt named in castle-turing's `the-corpus-is-never-swept-against-the-conventions`
(castle-turing PR #124) — found 1 code-touching pull request in this
repository that merged with no review round: no cross-vendor
(Codex/OpenCode) review and no formal GitHub review. This repo has no
review automation yet, which is a reason to review retroactively, not
an exemption. The instance:

- #1 (2026-09-07) Milestone-1 elicitation: [m1-links], [m1-provenance], [m1-seam]; task 0001 to cheap tier

**Why it matters.** Retroactive conformance is the point of
castle-turing PR #124: a convention applies to work that predates it.
This PR is the founding code of the reading surface; a cross-model
reviewer earns its keep precisely on work its own model family wrote —
the same sweep's first belated review, on castle-turing PR #132,
caught a one-line fix that was a silent no-op.

**How to review it, cheaply.** Run
`chevaline/scripts/cross-vendor-review.py --reviewer opencode` against
the PR's merged diff (`--base <mergeCommit>^ --head <mergeCommit>`, SHA
from `gh pr view 1 --json mergeCommit`) and post the review verbatim as
a comment on the (closed) PR. Provider policy: OpenCode Zen (Deep Infra
proved too slow — a Kimi-K3 spike timed out at 900s elsewhere in the
sweep); never the metered Codex CLI. Any finding still live against
current `main` becomes its own backlog entry → fix; an empty review is
a receipt on the PR.

**How this would have been caught sooner.** The enumeration is a
scheduled org-wide sweep whose empty result is a receipt rather than
silence — castle-turing PR #124's charge. A review gate on this repo's
PRs (it has none yet — worth its own entry) keeps the set from
regrowing.

**Scope.** A single-review hygiene unit, prioritized with everything
else; record its cost and yield in the task-outcome baseline.
