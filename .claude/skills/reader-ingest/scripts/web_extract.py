#!/usr/bin/env python3
"""Pull the article out of a saved web page and rescue content Reader would drop.

    web_extract.py audit  <page.html>              # what will readability strip?
    web_extract.py body   <page.html> <out.html> [--base <page url>]   # extract + rescue

Run with: uv run --with beautifulsoup4 --with lxml python web_extract.py ...

THE CORE PROBLEM. Readwise Reader (like every readability parser) scores blocks
by paragraph and text density. A component built purely from <div>/<span> with
no <p> anywhere reads as page furniture and is stripped wholesale — even though
CSS made it look like body text. Custom "card", "callout", "comparison" and
"aside" components are the usual casualties, and they often hold the examples
that carry the argument.

`audit` lists every text-bearing element that has no <p> descendant, biggest
first. Anything substantial in that list is at risk and needs converting.

`body` extracts the article and applies a GENERIC rescue: unknown div/span
components that hold real text get their lines wrapped in <p>. This is a safety
net, not a substitute for reading the audit — bespoke components (a two-column
before/after, a Q/A card with a critique line, a badge + label pair) need a
purpose-written transform to keep their meaning. See references/web-recipes.md.
"""
import re, sys, pathlib
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BOILERPLATE = ['nav', 'script', 'style', 'noscript', 'form', '.site-header', '.site-footer',
               '.share-buttons', '.social-share', '.sharing', '.post-share',
               '.report-nav-header', '[role=navigation]', '[aria-hidden=true]']


def load(path):
    return BeautifulSoup(pathlib.Path(path).read_text(errors='replace'), 'lxml')


def article_of(soup):
    return (soup.find('article') or soup.find('main')
            or soup.find(attrs={'role': 'main'}) or soup.body)


def audit(path):
    art = article_of(load(path))
    for sel in BOILERPLATE:
        for el in art.select(sel):
            el.decompose()

    risky = []
    for el in art.find_all(['div', 'span', 'section', 'aside', 'li', 'dd']):
        # tables/figures stand on their own merit; only loose prose is at risk
        if el.find('p') or el.find(['table', 'img', 'figure']):
            continue
        text = el.get_text(' ', strip=True)
        # innermost text holder only, so one component isn't counted at every level
        if len(text) < 25 or any(not c.find('p') and len(c.get_text(strip=True)) > 25
                                 for c in el.find_all(['div', 'span'], recursive=False)):
            continue
        risky.append((len(text), el.name, ' '.join(el.get('class', [])) or '(no class)', text))

    seen, rows = set(), []
    for n, tag, cls, text in sorted(risky, reverse=True):
        if cls in seen and len(rows) > 40:
            continue
        seen.add(cls)
        rows.append((n, tag, cls, text))

    total = sum(r[0] for r in risky)
    print(f"{len(risky)} text-bearing elements with NO <p> — {total} chars at risk\n")
    for n, tag, cls, text in rows[:40]:
        print(f"  {n:5d}  {tag}.{cls}")
        print(f"         {text[:110]}")
    print(f"\nsurviving <p> in article: {len(art.find_all('p'))}")
    counts = {}
    for _, tag, cls, _ in risky:
        counts[f"{tag}.{cls}"] = counts.get(f"{tag}.{cls}", 0) + 1
    print("component counts:", dict(sorted(counts.items(), key=lambda kv: -kv[1])[:15]))


def resolve_css_vars(art, path):
    """Site charts use var(--x) for colour; that resolves to nothing off-site."""
    css = ''
    for extra in list(pathlib.Path(path).parent.glob('*.css')):
        css += extra.read_text(errors='replace')
    css += '\n'.join(t.get_text() for t in art.find_all('style'))
    palette = {k: v.strip() for k, v in
               re.findall(r'(--[\w-]+)\s*:\s*([^;]+)',
                          ' '.join(re.findall(r':root\s*\{([^}]*)\}', css)))}
    if not palette:
        return
    def sub(t):
        for _ in range(3):
            new = re.sub(r'var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)',
                         lambda m: palette.get(m.group(1), m.group(2) or 'currentColor'), t)
            if new == t:
                return t
            t = new
        return t
    for el in art.find_all(True):
        for a in ('fill', 'stroke', 'style', 'stop-color'):
            if el.has_attr(a) and 'var(--' in el[a]:
                el[a] = sub(el[a])


INLINE = {'a', 'em', 'strong', 'b', 'i', 'u', 's', 'code', 'span', 'sup', 'sub', 'small',
          'mark', 'abbr', 'cite', 'q', 'kbd', 'var', 'time', 'del', 'ins', 'img'}
DISPLAY_MATH = re.compile(r'^\s*(\$\$|\\\[|\\begin\{)')


def wrap_in_paragraphs(soup, el):
    """Give a <p>-less component real paragraphs WITHOUT destroying what's in it.

    The old rescue rebuilt text with get_text('\\n'), which (a) shattered every
    multi-line display equation into one <p> per line — "$$", "\\begin{aligned}",
    each row, "$$" — so no formula survived, and (b) broke a sentence at every
    inline tag, so "text <em>word</em> more" became three paragraphs and lost
    its emphasis. Here the real nodes are MOVED into paragraphs; <br> and block
    children are the only boundaries, and a display-maths block stays whole.
    """
    if DISPLAY_MATH.match(el.get_text()):
        tex = el.get_text().strip()
        el.clear()
        p = soup.new_tag('p')
        p.string = tex
        el.append(p)
        return True

    runs, current = [], []
    for child in list(el.children):
        if getattr(child, 'name', None) == 'br':
            runs.append(current); current = []
        elif child.name is None or child.name in INLINE:
            current.append(child)
        else:                                   # a block child keeps its own shape
            runs.append(current); runs.append([child]); current = []
    runs.append(current)

    made = False
    for run in runs:
        if not run:
            continue
        if len(run) == 1 and run[0].name and run[0].name not in INLINE:
            continue                            # block child: leave in place
        if not ''.join(getattr(n, 'text', str(n)) for n in run).strip():
            for n in run:
                if n.name is None:
                    n.extract()                 # stray whitespace between blocks
            continue
        p = soup.new_tag('p')
        run[0].insert_before(p)
        for n in run:
            p.append(n.extract())
        made = True
    return made


def dollar_math(soup, art):
    """KaTeX / MathJax -> literal $...$ text, recovered from the TeX source.

    Done here with a real parser because KaTeX nests dozens of spans per formula
    and no regex unpicks that reliably. The $...$ form is the vault-wide policy:
    Reader shows it as source, Obsidian renders it once highlights arrive.
    Returns (converted, unrecoverable)."""
    done = lost = 0
    for el in art.select('.katex-display, .katex'):
        if el.parent is None or el.find_parent(class_='katex'):
            continue
        ann = el.find('annotation', attrs={'encoding': 'application/x-tex'})
        if not ann:
            lost += 1
            continue
        tex = ann.get_text().strip()
        block = 'katex-display' in el.get('class', []) or el.find_parent(class_='katex-display')
        el.replace_with(soup.new_string(f'$${tex}$$' if block else f'${tex}$'))
        done += 1
    # MathJax v2 keeps TeX in script tags; v3 renders <mjx-container> with
    # assistive MathML, which html_for_api.py recovers when it has an annotation.
    for sc in art.find_all('script', attrs={'type': re.compile(r'^math/tex')}):
        tex = sc.get_text().strip()
        sc.replace_with(soup.new_string(f'$${tex}$$' if 'display' in sc['type'] else f'${tex}$'))
        done += 1
    for mj in art.select('.MathJax, .MathJax_Preview, .MathJax_Display'):
        mj.decompose()
    return done, lost


def page_url(soup, override=None):
    """Where relative links resolve from: --base, else <base>, canonical, og:url."""
    if override:
        return override
    for sel, attr in (('base[href]', 'href'), ('link[rel=canonical]', 'href'),
                      ('meta[property="og:url"]', 'content')):
        el = soup.select_one(sel)
        if el and el.get(attr, '').startswith('http'):
            return el[attr]
    return None


def absolutise(art, base):
    """Relative src/href -> absolute. A saved page has no server behind it, so
    every relative image would otherwise be 'not found' and dropped — 15 of 15
    on the first real test. Lazy-loading attributes are promoted to src."""
    n = 0
    for img in art.find_all('img'):
        for lazy in ('data-src', 'data-lazy-src', 'data-original'):
            if img.get(lazy) and (not img.get('src') or img['src'].startswith('data:image/gif')):
                img['src'] = img[lazy]
    for tag, attr in (('img', 'src'), ('a', 'href'), ('source', 'src')):
        for el in art.find_all(tag):
            v = el.get(attr)
            if v and not v.startswith(('http:', 'https:', 'data:', 'mailto:', '#', 'javascript:')):
                el[attr] = urljoin(base, v)
                n += 1
    return n


def body(path, out, base=None):
    soup = load(path)
    base = page_url(soup, base)
    art = article_of(soup)
    # Icons inside links and buttons (share buttons, theme toggles) carry no
    # content and would otherwise be counted as charts needing rasterising.
    for sv in art.select('a svg, button svg'):
        sv.decompose()
    maths, lost = dollar_math(soup, art)   # before BOILERPLATE: it removes <script>
    for sel in BOILERPLATE:
        for el in art.select(sel):
            el.decompose()
    resolve_css_vars(art, path)
    if base:
        print(f"  resolved {absolutise(art, base)} relative links/images against {base}")
    elif art.find('img', src=re.compile(r'^(?!https?:|data:)')):
        print("  ! relative image paths and no page URL found — pass --base <url> or they will be dropped")
    if maths or lost:
        print(f"  maths: {maths} formulas -> $...$" + (f", {lost} with no TeX source (check by hand)" if lost else ""))

    rescued = 0
    for el in art.find_all(['div', 'span']):
        if el.find('p') or not el.get_text(strip=True):
            continue
        # never flatten a wrapper around structured content — it would be destroyed
        if el.find(['table', 'img', 'svg', 'figure', 'pre', 'ul', 'ol']):
            continue
        if any(not c.find('p') and len(c.get_text(strip=True)) > 25
               for c in el.find_all(['div', 'span'], recursive=False)):
            continue
        if len(el.get_text(strip=True)) < 25:
            continue
        if wrap_in_paragraphs(soup, el):
            el.name = 'div'
            rescued += 1

    pathlib.Path(out).write_text(str(art))
    print(f"wrote {out} — rescued {rescued} components, "
          f"{len(art.find_all('p'))} paragraphs, {len(art.find_all('svg'))} inline svg, "
          f"{len(art.find_all('table'))} tables")
    if art.find_all('svg'):
        print("  NOTE: inline SVG is dropped by pandoc — rasterize.py svgs, then swap to <img>")


if __name__ == '__main__':
    if sys.argv[1] == 'audit':
        audit(sys.argv[2])
    else:
        base = sys.argv[sys.argv.index('--base') + 1] if '--base' in sys.argv else None
        body(sys.argv[2], sys.argv[3], base)
