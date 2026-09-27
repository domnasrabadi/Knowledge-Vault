#!/usr/bin/env python3
"""Pull the article out of a saved web page and rescue content Reader would drop.

    web_extract.py audit  <page.html>              # what will readability strip?
    web_extract.py body   <page.html> <out.html>   # extract + generic rescue

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
from bs4 import BeautifulSoup

BOILERPLATE = ['nav', 'script', 'style', 'noscript', 'form', '.site-header', '.site-footer',
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


def body(path, out):
    soup = load(path)
    art = article_of(soup)
    maths, lost = dollar_math(soup, art)   # before BOILERPLATE: it removes <script>
    for sel in BOILERPLATE:
        for el in art.select(sel):
            el.decompose()
    resolve_css_vars(art, path)
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
        lines = [ln.strip() for ln in re.split(r'\n+', el.get_text('\n', strip=True)) if ln.strip()]
        if not lines or sum(len(l) for l in lines) < 25:
            continue
        el.clear()
        for ln in lines:
            p = soup.new_tag('p')
            p.string = ln
            el.append(p)
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
        body(sys.argv[2], sys.argv[3])
