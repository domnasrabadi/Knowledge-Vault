#!/usr/bin/env python3
"""Turn a cleaned body-HTML fragment into a document ready for the Reader API.

    html_for_api.py body.html meta.json out.html [--max-kb 8000]

Stdlib only. Prints the stats the user sees before confirming an upload.

This is the web / PDF / Word route's equivalent of arxiv_to_reader.py's
post-processing, and applies the same hard-won rules to every source:

  - No <h1> in the body. Reader deletes every body <h1> (it owns the title).
    Headings are SHIFTED down a level, not merged, so hierarchy survives.
  - Maths is written as $...$ / $$...$$ — the vault-wide policy. Reader shows it
    as source; highlights reach Obsidian through reader4 already renderable.
  - <img>, never <embed>. Reader strips <embed>, leaving a caption under nothing.
  - Local images become data URIs (Reader cannot see the filesystem); remote
    ones keep their URL. Anything oversized is dropped and counted, never silent.
  - The title is NOT repeated in the body — it travels as API metadata.

meta.json is shared with build.py: title, authors[], date, url, description,
abstract?, subtitle?, tags?
"""
import re, sys, json, base64, pathlib, html as htmllib

MAX_IMAGE_BYTES = 900_000
DEFAULT_MAX_KB = 8_000


def esc(s):
    return htmllib.escape(str(s), quote=True)


# ---------------------------------------------------------------- maths

def to_dollar_math(html):
    """Normalise every maths representation to literal $...$ / $$...$$ text.

    Shared with build.py so the EPUB route writes maths identically. Also strips
    pandoc's <span class="math"> wrappers: pandoc's own HTML reader would otherwise
    re-parse them as maths and render them its own way, losing the delimiters.
    """
    # MathML carrying its TeX source as an annotation: recover the source.
    def from_annotation(m):
        tex = re.search(r'<annotation[^>]*encoding="application/x-tex"[^>]*>(.*?)</annotation>',
                        m.group(0), re.S)
        if not tex:
            return m.group(0)
        src = htmllib.unescape(tex.group(1)).strip()
        display = 'display="block"' in m.group(0) or 'katex-display' in m.group(0)
        return f'$${src}$$' if display else f'${src}$'

    # <math> never nests, so a regex is safe here. KaTeX's deeply nested span
    # soup is NOT — web_extract.py converts it with a real parser before this runs.
    html = re.sub(r'<math\b.*?</math>', from_annotation, html, flags=re.S)
    # MathJax v2 keeps TeX in script tags.
    html = re.sub(r'<script type="math/tex; mode=display">(.*?)</script>', r'$$\1$$', html, flags=re.S)
    html = re.sub(r'<script type="math/tex">(.*?)</script>', r'$\1$', html, flags=re.S)

    # pandoc --mathjax output: \( \) and \[ \], inside <span class="math ...">.
    # Leave code alone — a literal "\(" in a regex example is not maths.
    parts = re.split(r'(<pre\b.*?</pre>|<code\b.*?</code>)', html, flags=re.S)
    for i in range(0, len(parts), 2):
        p = parts[i]
        p = re.sub(r'<span class="math (?:inline|display)">(.*?)</span>', r'\1', p, flags=re.S)
        p = p.replace('\\(', '$').replace('\\)', '$').replace('\\[', '$$').replace('\\]', '$$')
        # A recovered display block sitting loose between blocks is bare text,
        # which readability-style parsers treat as furniture. Give it a <p>.
        p = re.sub(r'(?m)^(\s*)(\$\$.+?\$\$)\s*$', r'\1<p>\2</p>', p)
        parts[i] = p
    return ''.join(parts)


def leftover_mathml(html):
    return len(re.findall(r'<math\b', html))


# ---------------------------------------------------------------- structure

def shift_headings(html):
    """Shift every heading down one level if any <h1> is present. h6 stays h6."""
    if not re.search(r'<h1[\s>]', html):
        return html, 0
    for lvl in range(5, 0, -1):
        html = re.sub(rf'(</?h){lvl}([\s>])', rf'\g<1>{lvl + 1}\2', html)
    return html, 1


def strip_chrome(html):
    if '<body' in html:
        html = html.split('<body', 1)[1].split('>', 1)[1].rsplit('</body>', 1)[0]
    html = re.sub(r'<(script|style|noscript)\b.*?</\1>', '', html, flags=re.S)
    html = re.sub(r'<header\b[^>]*>.*?</header>', '', html, flags=re.S)
    html = re.sub(r'<p[^>]*>(\s|&nbsp;|<br\s*/?>)*</p>', '', html)
    # iframes never work in Reader, and a YouTube one leaves a stray
    # "<h1>An error occurred.</h1>" in the body. Keep the link, drop the frame.
    html = re.sub(r'<iframe[^>]*src="([^"]+)"[^>]*>.*?</iframe>',
                  r'<p><a href="\1">Embedded media: \1</a></p>', html, flags=re.S)
    return html


def embed_images(html, search_dirs):
    """<embed>/<img> -> <img>; local files -> data URIs. Returns html, embedded, dropped[]."""
    embedded, dropped = 0, []

    def repl(m):
        nonlocal embedded
        tag, src = m.group(0), m.group(1)
        keep = ''.join(f' {a}="{v}"' for a, v in re.findall(r'\b(alt|title|width|height)="([^"]*)"', tag))
        if src.startswith(('http://', 'https://', 'data:')):
            if src.startswith('data:') and len(src) * 3 // 4 > MAX_IMAGE_BYTES:
                dropped.append('(inline data URI, oversized)')
                return ''
            return f'<img src="{src}"{keep} />'
        for d in search_dirs:
            p = pathlib.Path(d) / src.split('?')[0]
            if p.exists():
                data = p.read_bytes()
                if len(data) > MAX_IMAGE_BYTES:
                    dropped.append(f'{src} ({len(data) // 1024} KB)')
                    return ''
                mime = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                        '.gif': 'image/gif', '.svg': 'image/svg+xml',
                        '.webp': 'image/webp'}.get(p.suffix.lower())
                if not mime:
                    dropped.append(f'{src} (unsupported type)')
                    return ''
                embedded += 1
                return f'<img src="data:{mime};base64,{base64.b64encode(data).decode()}"{keep} />'
        dropped.append(f'{src} (not found)')
        return ''

    html = re.sub(r'<(?:img|embed)\b[^>]*\bsrc="([^"]*)"[^>]*/?>', repl, html)
    return html, embedded, dropped


def header(meta):
    """Byline + source link + abstract. The title itself travels as metadata."""
    bits = []
    authors = ', '.join(meta.get('authors', []))
    src = ' · '.join(x for x in [
        f'<em>{esc(authors)}</em>' if authors else '',
        esc(meta.get('venue', '')),
        f'<a href="{esc(meta["url"])}">{esc(meta["url"])}</a>' if meta.get('url') else '',
        esc(meta.get('date', ''))] if x)
    if meta.get('subtitle'):
        bits.append(f'<p><strong>{esc(meta["subtitle"])}</strong></p>')
    if src:
        bits.append(f'<p>{src}</p>')
    if meta.get('abstract'):
        bits.append(f'<h2>Abstract</h2>\n<blockquote>{meta["abstract"]}</blockquote>')
    return '\n'.join(bits) + '\n'


def stats(html):
    flat = re.sub(r'<[^>]+>', ' ', html)
    return {
        'words': len(flat.split()),
        **{t: len(re.findall(rf'<{t}[\s>]', html))
           for t in ('h1', 'h2', 'h3', 'h4', 'p', 'table', 'pre', 'img', 'embed', 'li', 'blockquote')},
        'inline_math': len(re.findall(r'(?<!\$)\$(?!\$)[^$\n]+?\$(?!\$)', flat)),
        'display_math': flat.count('$$') // 2,
        'kb': len(html.encode()) // 1024,
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if len(args) < 3:
        print(__doc__)
        sys.exit(2)
    body_path, meta_path, out_path = map(pathlib.Path, args[:3])
    max_kb = int(sys.argv[sys.argv.index('--max-kb') + 1]) if '--max-kb' in sys.argv else DEFAULT_MAX_KB
    meta = json.loads(meta_path.read_text())
    for k in ('title', 'url'):
        if not meta.get(k):
            sys.exit(f"meta.json needs '{k}' — the API requires it when Reader's cleaner is off")
    if not meta.get('authors'):
        sys.exit("meta.json needs 'authors' — the API requires an author when Reader's cleaner is off. "
                 "Use the site or publisher name if there is no person.")

    html = strip_chrome(body_path.read_text())
    html = to_dollar_math(html)
    html, shifted = shift_headings(html)
    html, embedded, dropped = embed_images(html, [body_path.parent, pathlib.Path('.')])
    html = header(meta) + html
    html = re.sub(r'\n{3,}', '\n\n', html)

    s = stats(html)
    if s['kb'] > max_kb:
        sys.exit(f"HTML is {s['kb']} KB, over the {max_kb} KB guard. Shrink or drop images, "
                 "or route this source to an EPUB.")
    out_path.write_text(html)

    print(f"wrote {out_path}")
    print(f"  title:    {meta['title']}")
    print(f"  source:   {meta['url']}")
    print(f"  words:    {s['words']:,}   size: {s['kb']} KB")
    print(f"  headings: h2={s['h2']} h3={s['h3']} h4={s['h4']}   (h1={s['h1']}"
          f"{', shifted down a level' if shifted else ''})")
    print(f"  blocks:   p={s['p']} table={s['table']} pre={s['pre']} li={s['li']} blockquote={s['blockquote']}")
    print(f"  images:   {s['img']} ({embedded} embedded from disk)   embed={s['embed']}")
    print(f"  maths:    {s['inline_math']} inline, {s['display_math']} display (as $...$)")
    problems = []
    if s['h1']:
        problems.append(f"{s['h1']} <h1> left — Reader will delete them")
    if s['embed']:
        problems.append(f"{s['embed']} <embed> left — Reader strips them")
    if dropped:
        problems.append(f"{len(dropped)} image(s) dropped: {dropped[:4]}")
    if (n := leftover_mathml(html)):
        problems.append(f"{n} MathML block(s) had no TeX source to recover — they will not reach "
                        "Obsidian as $...$; transcribe by hand if they matter")
    for pr in problems:
        print(f"  ! {pr}")
    if not problems:
        print("  no problems found")


if __name__ == '__main__':
    main()
