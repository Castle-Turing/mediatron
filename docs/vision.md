# Mediatron — vision

*Founding context, 2026-09-06, distilled from the resident's
direction at the close of the Castle Turing research series.*

Castle Turing's trust model runs on its resident actually reading
what the system writes. Dovetail made the text editor that surface
for *working* documents. Mediatron makes a browser window the
surface for *finished* ones: when the castle has a status update, a
brief, or a research review for its resident, it should open as a
beautiful page in the house style — not a markdown buffer — in a
window with no chrome, navigated with vim keys, gone with a
keypress.

Concretely: `mediatron <file>` renders a castle-flavored markdown
document to a typeset page (the house visual system: warm paper and
verdigris, a serif for reading, mono for the machine-facing parts,
verification badges rendered as badges) and shows it chromeless.
Links to other castle documents open in the same window; links to
the outside world open in the resident's default browser. The window
should feel instant — a warm renderer/browser waiting in the
background is anticipated but deferred until slowness is measured,
not assumed.

Two design commitments, inherited from the ecosystem: the engine is
bought, not built — qutebrowser supplies the vim grammar and the
window, Mediatron supplies the renderer, the link policy, and the
house style — and the house style itself is public mechanism with
the resident's taste as overridable configuration, per Castle
Turing's Principle 01. Whether Mediatron eventually becomes a
Dovetail verb is deliberately undecided; it starts as its own small
thing.

This repo is also, deliberately, a greenfield dogfooding ground: the
elicitation, status-update, state-layer, and measurement practices
in `AGENTS.md` ship in the founding commit, so their costs and
payoffs are observable from task one — including the one property no
retrofit can ever recover: a task-outcome baseline that starts
before any workflow experiment does.
