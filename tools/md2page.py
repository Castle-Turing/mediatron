#!/usr/bin/env python3
"""Convert the constrained markdown of the research reports to a styled HTML page."""
import html, re, sys

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

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)
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
    return s

def convert(md, eyebrow):
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
            out.append(f"<{tag}>{inline(text)}</{tag}>")
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
            out.append("<ol>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ol>")
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
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
        elif re.match(r"^>", lines[0]):
            text = " ".join(l.lstrip("> ").strip() for l in lines)
            out.append(f"<blockquote><p>{inline(text)}</p></blockquote>")
        else:
            text = " ".join(l.strip() for l in lines)
            cls = ""
            if not first_para_done and text.startswith("*") and text.endswith("*"):
                cls = ' class="provenance"'
                text = text[1:-1]
                first_para_done = True
            out.append(f"<p{cls}>{inline(text)}</p>")
    return "\n".join(out)

if __name__ == "__main__":
    src, dst, title, eyebrow = sys.argv[1:5]
    md = open(src).read()
    body = convert(md, eyebrow)
    page = f"<title>{html.escape(title)}</title>\n<style>{CSS}</style>\n<main>\n{body}\n</main>\n"
    open(dst, "w").write(page)
    print(f"wrote {dst} ({len(page)} bytes)")
