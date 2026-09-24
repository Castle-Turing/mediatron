# docs/backlog — deferred work, in plain text

One file per item, named as a statement of the problem. Speccing
happens in place: an item's file grows the task header and body as
its spec matures, and stays here while it does. The resident's
approval of a fully specced item is recorded as `Status: ready` in
its header — the resident's act, never inferred.

A ready item reaches docs/tasks/ only by verbatim transfer: headers
and body copied unchanged except the `Status:` line, the number and
filename allocated at transfer, and the backlog file deleted in the
same commit, so an item exists in exactly one place at a time. The
transfer commit lands on the default branch and is pushed: the brief
is the record its number names, and anything resolving that number
reads it from the remote, not from a local checkout. The profile's
work-layout section carries this rule across projects; see it for the
reasoning.
