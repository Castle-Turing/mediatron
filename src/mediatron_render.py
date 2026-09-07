#!/usr/bin/env python3
"""Mediatron renderer: constrained markdown to a self-contained house-style HTML page.

A port of the founding session's tools/md2page.py, kept faithful to its
conversion rules and its two fixed bugs (bold spans containing italics;
bare URLs swallowing adjacent markers). The port adds three things that
milestone 1 requires ([m1-provenance], [m1-links] in
docs/state/MILESTONE.md):

- a front-matter block declaring title and eyebrow, parsed and stripped;
- link classification: relative/file:// and allowlist-matched links are
  internal, every other http(s) link is tagged class="external" so the
  mediatron wrapper can hand it to the default browser;
- relative links to other .md documents are rendered on the spot and
  rewritten to their .html twins, so castle documents open in the same
  window without a server.
"""
import argparse
import html
import os
import re
import sys

EXTERNAL_SCHEME = "mediatron-external"

CSS = """
  :root {
    --paper: #FAF9F6; --ink: #1C1F22; --muted: #5C636B;
    --accent: #2F7D6D; --accent-soft: #2F7D6D22; --amber: #9A6A1F;
    --amber-soft: #9A6A1F14; --rule: #1C1F2226; --card: #F1EFEA;
    --mono-bg: #1C1F220D;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --paper: #15181B; --ink: #E5E3DC; --muted: #9BA3AB;
      --accent: #63B49E; --accent-soft: #63B49E22; --amber: #D2A45B;
      --amber-soft: #D2A45B1A; --rule: #E5E3DC26; --card: #1C2024;
      --mono-bg: #E5E3DC12;
    }
  }
  :root[data-theme="dark"] {
    --paper: #15181B; --ink: #E5E3DC; --muted: #9BA3AB;
    --accent: #63B49E; --accent-soft: #63B49E22; --amber: #D2A45B;
    --amber-soft: #D2A45B1A; --rule: #E5E3DC26; --card: #1C2024;
    --mono-bg: #E5E3DC12;
  }
  body { background: var(--paper); color: var(--ink);
    font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif;
    font-size: 1.0625rem; line-height: 1.68; margin: 0; }
  main { max-width: 70ch; margin: 0 auto; padding: 3rem 1.25rem 5rem; }
  .eyebrow { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent); margin: 0 0 .75rem; }
  h1 { font-size: 1.85rem; line-height: 1.2; margin: 0 0 1rem;
    text-wrap: balance; font-weight: 600; }
  h1 + h1 { font-size: 1.35rem; color: var(--muted); }
  h2 { font-size: 1.2rem; margin: 2.4rem 0 .75rem; font-weight: 600; text-wrap: balance; }
  h2::before { content: ""; display: block; width: 2.25rem; height: 2px;
    background: var(--accent); margin-bottom: .6rem; }
  h3 { font-size: 1.05rem; margin: 1.8rem 0 .5rem; font-weight: 600;
    color: var(--accent); text-wrap: balance; }
  p { margin: 0 0 1rem; }
  .provenance { background: var(--card); border: 1px solid var(--rule);
    border-radius: 6px; padding: .9rem 1.1rem; margin: 0 0 1.5rem;
    font-size: .92rem; font-style: italic; }
  .provenance em { font-style: italic; }
  hr { border: none; border-top: 1px solid var(--rule); margin: 2rem 0; }
  code { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: .84em; background: var(--mono-bg); border-radius: 3px;
    padding: .08em .3em; }
  ol, ul { padding-left: 1.4rem; margin: 0 0 1rem; }
  li { margin-bottom: .7rem; }
  li::marker { color: var(--accent); font-weight: 600; }
  strong { font-weight: 600; }
  a { color: var(--accent); text-decoration-thickness: 1px; text-underline-offset: 2px;
    word-break: break-word; overflow-wrap: anywhere; }
  .v, .r { font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
    font-size: .74em; border-radius: 3px; padding: .05em .35em; font-weight: 600; }
  .v { color: var(--accent); background: var(--accent-soft); }
  .r { color: var(--amber); background: var(--amber-soft); }
  blockquote { border-left: 3px solid var(--accent); margin: 1rem 0;
    padding: .2rem 0 .2rem 1rem; color: var(--muted); }
"""


def inline(s, roots):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    # any target without whitespace anchors: http(s), relative paths,
    # file:, mailto:. The original md2page.py anchored http(s) only;
    # anchoring relative targets is the extension [m1-links] requires.
    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', s)
    def _bare(m):
        url, trail = m.group(1), ""
        while url and url[-1] in ".;:!?":
            trail = url[-1] + trail
            url = url[:-1]
        return f'<a href="{url}">{url}</a>{trail}'
    s = re.sub(r"(?<![\"(>=])(https?://[^\s)\],*]+)", _bare, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s, flags=re.S)
    s = re.sub(r"(?<!\w)\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", s)
    # verification badges — after escaping, [V] and [R] are literal
    s = re.sub(r"\[V\]", '<span class="v">[V]</span>', s)
    s = re.sub(r"\[R\]", '<span class="r">[R]</span>', s)
    s = re.sub(r"\[(V|R),\s*", lambda m: f'<span class="{m.group(1).lower()}">[{m.group(1)}]</span> [', s)
    s = _tag_external(s, roots)
    return s


def _tag_external(s, roots):
    """Rewrite external http(s) links to the mediatron-external: scheme.

    qutebrowser's unknown-scheme policy then hands the URL to the OS on
    any activation (click, hint, Enter), where mediatron's registered
    per-user handler strips the prefix and xdg-opens the real URL
    ([m1-links], and see webenginesettings in qutebrowser 3.7.0)."""
    def _one(m):
        href = m.group(1)
        external = href.startswith(("http://", "https://")) and not any(
            href.startswith(r) for r in roots
        )
        if external:
            href = EXTERNAL_SCHEME + ":" + href
        return f'<a href="{href}">'
    return re.sub(r'<a href="([^"]+)">', _one, s)


def convert(md, eyebrow, roots):
    blocks = re.split(r"\n\s*\n", md)
    out = [f'<p class="eyebrow">{html.escape(eyebrow)}</p>']
    first_para_done = False
    for b in blocks:
        b = b.strip("\n")
        if not b.strip():
            continue
        lines = b.split("\n")
        if re.match(r"^#{1,3} ", lines[0]):
            level = len(lines[0]) - len(lines[0].lstrip("#"))
            text = " ".join(l.lstrip("# ").strip() for l in lines)
            tag = {1: "h1", 2: "h2"}.get(level, "h3")
            out.append(f"<{tag}>{inline(text, roots)}</{tag}>")
        elif all(re.match(r"^-{3,}$", l) for l in lines):
            out.append("<hr>")
        elif re.match(r"^\d+\.\s", lines[0]):
            items, cur = [], None
            for l in lines:
                m = re.match(r"^\d+\.\s+(.*)$", l)
                if m:
                    if cur is not None: items.append(cur)
                    cur = m.group(1)
                else:
                    cur += " " + l.strip()
            items.append(cur)
            out.append("<ol>" + "".join(f"<li>{inline(i, roots)}</li>" for i in items) + "</ol>")
        elif re.match(r"^[-*]\s", lines[0]):
            items, cur = [], None
            for l in lines:
                m = re.match(r"^[-*]\s+(.*)$", l)
                if m:
                    if cur is not None: items.append(cur)
                    cur = m.group(1)
                else:
                    cur += " " + l.strip()
            items.append(cur)
            out.append("<ul>" + "".join(f"<li>{inline(i, roots)}</li>" for i in items) + "</ul>")
        elif re.match(r"^>", lines[0]):
            text = " ".join(l.lstrip("> ").strip() for l in lines)
            out.append(f"<blockquote><p>{inline(text, roots)}</p></blockquote>")
        else:
            text = " ".join(l.strip() for l in lines)
            cls = ""
            if not first_para_done and text.startswith("*") and text.endswith("*"):
                cls = ' class="provenance"'
                text = text[1:-1]
                first_para_done = True
            out.append(f"<p{cls}>{inline(text, roots)}</p>")
    return "\n".join(out)


def parse_front_matter(text):
    """Return (title, eyebrow, rest) from a leading key: value block.

    Recognises `title:` and `eyebrow:` lines at the very top of the file,
    before the first blank line or any other content. Missing keys fall
    back to '' (title is filled in later from the first heading or the
    filename)."""
    title, eyebrow = "", ""
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            break
        m = re.match(r"^(title|eyebrow):\s*(.*?)\s*$", line, re.IGNORECASE)
        if not m:
            break
        if m.group(1).lower() == "title":
            title = m.group(2)
        else:
            eyebrow = m.group(2)
        i += 1
    if i:
        rest = "\n".join(lines[i:]).lstrip("\n")
    else:
        rest = text
    return title, eyebrow, rest


def _title_fallback(title, md, stem):
    if title:
        return title
    m = re.search(r"^#\s+(.+)$", md, re.MULTILINE)
    return m.group(1).strip() if m else stem


def _resolve_relative_md(html_out, out_path, visited, roots):
    """Render relative .md link targets next to the output and rewrite hrefs.

    Renders each unique relative href ending in .md (or file:// pointing at
    one) to its .html twin in the same directory, then rewrites the href.
    Cycles are cut by a visited set; missing targets are left untouched."""
    out_dir = os.path.dirname(out_path)
    src_html = html_out
    hrefs = set(re.findall(r'<a href="([^"]+\.md(?:#[^"]*)?)">', html_out))
    for href in sorted(hrefs):
        if href.startswith(EXTERNAL_SCHEME + ":"):
            continue
        frag = ""
        if "#" in href:
            href, frag = href.split("#", 1)
        target = href
        if target.startswith("file://"):
            target = target[len("file://"):]
        if not os.path.isabs(target):
            target = os.path.normpath(os.path.join(out_dir, target))
        if not target.endswith(".md") or target in visited:
            continue
        visited.add(target)
        if not os.path.exists(target):
            continue
        rel_html = os.path.join(os.path.dirname(href),
                                os.path.splitext(os.path.basename(target))[0] + ".html")
        out = os.path.join(out_dir, rel_html) if os.path.dirname(href) else None
        render(target, out_dir, roots, visited, out_path=out)
        new_href = rel_html + (f"#{frag}" if frag else "")
        src_html = re.sub(rf'<a href="{re.escape(href)}">', f'<a href="{new_href}">', src_html)
    return src_html


def render(src, out_dir=None, roots=(), visited=None, out_path=None):
    if visited is None:
        visited = set()
    src = os.path.abspath(src)
    visited.add(src)
    with open(src) as fh:
        text = fh.read()
    title, eyebrow, body_md = parse_front_matter(text)
    title = _title_fallback(title, body_md, os.path.splitext(os.path.basename(src))[0])
    body = convert(body_md, eyebrow, roots)
    if out_path is None:
        out_path = os.path.join(out_dir or os.path.dirname(src),
                                os.path.splitext(os.path.basename(src))[0] + ".html")
    out_path = os.path.abspath(out_path)
    body = _resolve_relative_md(body, out_path, visited, roots)
    page = "<!DOCTYPE html>\n" + f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n<main>\n{body}\n</main>\n"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as fh:
        fh.write(page)
    sys.stderr.write(f"wrote {out_path} ({len(page)} bytes)\n")
    return out_path


def load_roots(path):
    if not path:
        return []
    with open(path) as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="mediatron-render",
        description="Render constrained markdown to a self-contained house-style HTML page.")
    ap.add_argument("file", help="markdown file to render")
    ap.add_argument("--out", help="output path (default: <file>.html next to the source)")
    ap.add_argument("--roots", help="castle-roots allowlist file (one prefix per line, '#' comments)")
    args = ap.parse_args(argv)
    if not os.path.exists(args.file):
        ap.error(f"no such file: {args.file}")
    render(args.file, roots=tuple(load_roots(args.roots)), out_path=args.out)


if __name__ == "__main__":
    main()
