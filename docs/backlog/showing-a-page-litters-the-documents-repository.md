# Showing a page litters the document's repository

`mediatron file.md` writes the rendered `.html` twin next to the
source, and linked `.md` documents render next to their sources too.
Inside the castle's own tree that is the design — twins are what keep
relative links working in the window. But `mediatron` is also pointed
at documents in repositories it does not own (a task brief in another
project's `docs/`), and there the twin is harness bookkeeping left
inside a foreign checkout: an untracked file the reader must notice
and sweep, or accidentally commit.

The renderer already has `--out`; the wrapper does not expose it, and
`--out` alone would not carry the linked-document twins. Whoever specs
this decides the real shape: render the document graph into a cache
directory (XDG cache, hashed by source path) and serve links from
there, or expose an output root and rewrite relative links against
it. Either way, showing a page should leave the source tree exactly
as it found it.
