#!/usr/bin/env python3
"""Wrap a body-HTML fragment in a Reader-friendly standalone page, then build the EPUB.

    build.py body.html meta.json out-basename [--cover cover.jpg]

meta.json keys: title, authors[], date (YYYY-MM-DD), venue, url,
                description, abstract (HTML, optional), subtitle (optional)

Writes <out-basename>.html and <out-basename>.epub.
"""
import re, sys, json, base64, pathlib, subprocess, html as htmllib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from html_for_api import to_dollar_math, strip_chrome  # noqa: E402  (shared with the API route)
CSS = (HERE.parent / 'references' / 'style.css').read_text()


def esc(s):
    return htmllib.escape(str(s), quote=True)


def clean_body(body):
    """Normalise a body fragment: no page chrome, no skipped heading levels, no div soup."""
    body = re.sub(r'<header[^>]*>.*?</header>', '', body, flags=re.S)
    body = re.sub(r'<(script|style)\b.*?</\1>', '', body, flags=re.S)
    # keep semantic wrappers, drop purely presentational divs
    body = re.sub(r'<div class="(references|csl-bib-body)"[^>]*>',
                  '<section id="refs" class="references">', body)
    body = re.sub(r'</?div[^>]*>', '', body)
    body = re.sub(r'<p[^>]*>(\s|&nbsp;| |<br\s*/?>)*</p>', '', body)
    body = re.sub(r'\sstyle="[^"]*"', '', body)
    return re.sub(r'\n{3,}', '\n\n', body)


def fix_heading_gaps(body):
    """Collapse skipped levels (h3 -> h5 becomes h3 -> h4) so the TOC nests correctly."""
    for _ in range(4):
        present = sorted({int(m) for m in re.findall(r'<h([1-6])[\s>]', body)})
        gap = next((lvl for prev, lvl in zip(present, present[1:]) if lvl - prev > 1), None)
        if gap is None:
            break
        for lvl in range(gap, 7):
            body = re.sub(rf'(</?h){lvl}([\s>])', rf'\g<1>{lvl - 1}\g<2>', body)
    return body


def embed_images(body, search_dirs):
    """Inline local images as data URIs so the HTML is self-contained."""
    def sub(m):
        src = m.group(1)
        if src.startswith(('data:', 'http://', 'https://')):
            return m.group(0)
        for d in search_dirs:
            p = pathlib.Path(d) / src
            if p.exists():
                ext = p.suffix.lstrip('.').lower().replace('jpg', 'jpeg')
                return 'src="data:image/%s;base64,%s"' % (
                    ext, base64.b64encode(p.read_bytes()).decode())
        print(f"  ! image not found: {src}", file=sys.stderr)
        return m.group(0)
    return re.sub(r'src="([^"]+)"', sub, body)


def page(body, meta):
    authors = ', '.join(meta.get('authors', []))
    parts = [f'<h1>{esc(meta["title"])}</h1>']
    if meta.get('subtitle'):
        parts.append(f'<p class="subtitle">{esc(meta["subtitle"])}</p>')
    if authors:
        parts.append(f'<p class="authors">{esc(authors)}</p>')
    src = ' · '.join(x for x in [esc(meta.get('venue', '')),
                                 f'<a href="{esc(meta["url"])}">{esc(meta["url"])}</a>' if meta.get('url') else '',
                                 esc(meta.get('date', ''))] if x)
    parts.append(f'<p class="source-note">{src}</p>')
    if meta.get('abstract'):
        parts.append(f'<section class="abstract"><h2>Abstract</h2>{meta["abstract"]}</section>')
    return f'''<!doctype html>
<html lang="{esc(meta.get('lang', 'en'))}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(meta['title'])}</title>
<meta name="author" content="{esc(authors)}">
<meta name="description" content="{esc(meta.get('description', ''))}">
<meta name="date" content="{esc(meta.get('date', ''))}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(meta['title'])}">
<meta property="og:site_name" content="{esc(meta.get('venue', ''))}">
<meta property="article:published_time" content="{esc(meta.get('date', ''))}">
<link rel="canonical" href="{esc(meta.get('url', ''))}">
<style>{CSS}</style>
<article>
{chr(10).join(parts)}
''' + body + '\n</article>\n</html>\n'


def build_epub(html_path, meta, out_epub, cover=None):
    cmd = ['pandoc', str(html_path), '-f', 'html', '-t', 'epub3',
           '--toc', '--toc-depth=3', '--split-level=2',
           '--metadata', f'title={meta["title"]}',
           '--metadata', f'author={", ".join(meta.get("authors", []))}',
           '--metadata', f'date={meta.get("date", "")}',
           '--metadata', f'lang={meta.get("lang", "en")}',
           '-o', str(out_epub)]
    if cover:
        cmd.insert(-2, f'--epub-cover-image={cover}')
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr, file=sys.stderr)
        sys.exit(1)
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    cover = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--cover'), None)
    body_file, meta_file, base = args[0], args[1], args[2]
    meta = json.loads(pathlib.Path(meta_file).read_text())
    body = pathlib.Path(body_file).read_text()
    if '<body' in body:
        body = body.split('<body', 1)[1].split('>', 1)[1].rsplit('</body>', 1)[0]
    # $...$ literal text, same as the API routes: highlights reach Obsidian renderable.
    # pandoc emits <embed> for most figures it converts from DOCX/LaTeX, and its
    # HTML reader then DROPS <embed> when building the EPUB: figure gone, no error.
    body = re.sub(r'<embed\b', '<img', body)
    body = fix_heading_gaps(clean_body(to_dollar_math(strip_chrome(body))))
    body = embed_images(body, [pathlib.Path(body_file).parent, '.'])
    out_html = pathlib.Path(f'{base}.html')
    out_html.write_text(page(body, meta))
    build_epub(out_html, meta, f'{base}.epub', cover)
    print(f"wrote {out_html} ({out_html.stat().st_size // 1024} KB) "
          f"and {base}.epub ({pathlib.Path(base + '.epub').stat().st_size // 1024} KB)")


if __name__ == '__main__':
    main()
