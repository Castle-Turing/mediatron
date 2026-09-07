# Mediatron

The surface the castle shows its pages on: part of the
[Castle Turing](https://github.com/Castle-Turing/castle-turing)
ecosystem, alongside [Dovetail](https://github.com/Castle-Turing/dovetail).
Dovetail is where the resident and the agent write together; Mediatron
is where the system *presents* — status updates, task briefs, research
reviews — as typeset pages in a chromeless window with vim navigation,
instead of raw markdown in a buffer.

The name is from *The Diamond Age*: mediatronic paper, the surface
writing appears on.

## What works

Milestone 1 is the first buildable slice (task 0001):

- **`mediatron-render`** — constrained markdown in, self-contained
  house-style HTML page out (the port of the founding session's
  `tools/md2page.py`: warm paper and verdigris, serif for reading,
  mono for the machine-facing parts, verification badges). A leading
  front-matter block (`title:`, `eyebrow:`) is parsed and stripped.
- **`mediatron`** — renders a file and opens it in a chromeless
  qutebrowser window: no tabs, status bar only while navigating, vim
  keys as qutebrowser ships them. Relative links (including relative
  links to other `.md` documents, which are rendered on the spot) stay
  in the window. Links to http(s) URLs matching a prefix in your
  castle-roots allowlist also stay in the window; every other http(s)
  link is external and opens in your default browser however you
  follow it: the renderer rewrites external hrefs to a
  `mediatron-external:` scheme, and the wrapper registers a per-user
  handler (a desktop entry under `~/.local/share/applications` plus a
  `mimeapps.list` entry) that xdg-opens the real URL. Registration
  happens on first run and is idempotent.

qutebrowser is the bought engine: Mediatron supplies the renderer, the
link policy, and the house style.

## Usage

```sh
nix run .#mediatron -- path/to/status-update.md
nix run .#mediatron-render -- path/to/file.md
```

The window opens with the page rendered. `j`/`k` scroll; `f` hints
links (internal ones navigate in the window, external ones leave it);
`q` or `ZZ` quits.

### Configuration

The castle-roots allowlist lives in `~/.config/mediatron/config`
(override with `MEDIATRON_CONFIG`), one URL prefix per line — copy
`share/mediatron/config.example` and edit. Your private roots go there,
in your private configuration; the house palette and type are CSS
tokens in the renderer, the public mechanism a resident override can
replace without touching the repo.

## Repository shape

- `docs/` — working conventions (`AGENTS.md`), vision, backlog, task
  briefs, state; this repo is deliberately a dogfooding ground for the
  practices in `AGENTS.md`.
- `src/` — the renderer and the window wrapper.
- `share/mediatron/` — the external-link userscript and the example
  config.
- `examples/` — the milestone-1 fixture.
- `tools/md2page.py` — the committed source the renderer ports.

Read `docs/vision.md` for what this becomes, and `AGENTS.md` before
working here.
