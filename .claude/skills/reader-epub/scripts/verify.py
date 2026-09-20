#!/usr/bin/env python3
"""Verify an EPUB is well-formed and that expected content actually survived.

    verify.py book.epub [--probe "some string"] [--probe "another"] [--probes probes.txt]

Always run this before handing the file over. It catches the two failure modes
that matter: a structurally broken EPUB, and content silently dropped in
conversion (pandoc's HTML reader discards raw SVG, LaTeX \\resizebox tables
vanish, custom environments flatten, etc.).

Exit code 1 if any check fails.
"""
import sys, re, zipfile, pathlib
import xml.etree.ElementTree as ET

FAIL = []

OPF_NS = {'opf': 'http://www.idpf.org/2007/opf',
          'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}


def find_nav(z):
    """Resolve the nav document through container.xml -> OPF properties="nav"."""
    import posixpath
    try:
        rootfile = ET.fromstring(z.read('META-INF/container.xml')).find('.//c:rootfile', OPF_NS)
        opf_path = rootfile.get('full-path')
        base = posixpath.dirname(opf_path)
        for item in ET.fromstring(z.read(opf_path)).findall('.//opf:manifest/opf:item', OPF_NS):
            if 'nav' in (item.get('properties') or '').split():
                href = item.get('href', '')
                return posixpath.normpath(posixpath.join(base, href)) if base else href
    except (KeyError, ET.ParseError, AttributeError):
        pass
    return None


def check(label, ok, detail=''):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}{(' — ' + detail) if detail else ''}")
    if not ok:
        FAIL.append(label)


def main():
    path = sys.argv[1]
    probes = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--probe']
    for i, a in enumerate(sys.argv):
        if a == '--probes':
            probes += [l.strip() for l in pathlib.Path(sys.argv[i + 1]).read_text().splitlines() if l.strip()]

    z = zipfile.ZipFile(path)
    print(f"{path} ({pathlib.Path(path).stat().st_size // 1024} KB)")
    check("zip intact", z.testzip() is None)

    xh = [n for n in z.namelist() if n.endswith(('.xhtml', '.html'))]
    bad = []
    for n in xh:
        try:
            ET.fromstring(z.read(n))
        except ET.ParseError as e:
            bad.append(f"{n}: {e}")
    check("xhtml well-formed", not bad, f"{len(xh) - len(bad)}/{len(xh)}" + (f" | {bad[0]}" if bad else ""))

    # The nav document is whatever the OPF marks properties="nav" — only pandoc's
    # own builds call it nav.xhtml, so matching on the filename reports a false
    # FAIL on any book that names it otherwise (e.g. O'Reilly's toc01.html).
    nav = find_nav(z) or next((n for n in z.namelist() if n.endswith(('nav.xhtml', 'toc.xhtml'))), None)
    entries = len(re.findall(r'href="', z.read(nav).decode(errors='replace'))) if nav else 0
    check("navigation TOC", entries > 1, f"{entries} entries" + (f" in {nav}" if nav else " — no nav document"))

    body = "".join(z.read(n).decode(errors='replace') for n in xh)
    imgs = [n for n in z.namelist() if n.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg'))]
    stats = {t: body.count(f'<{t}') for t in ('p', 'h1', 'h2', 'h3', 'table', 'tr', 'img', 'blockquote', 'pre', 'li')}
    print("  stats:", " ".join(f"{k}={v}" for k, v in stats.items()), f"files={len(imgs)}")

    check("has real paragraphs", stats['p'] > 5, f"{stats['p']}")
    # tags may reuse the same file, so compare distinct references, not tag count
    refs = {re.sub(r'^.*/', '', s) for s in re.findall(r'<img[^>]*src="([^"]*)"', body)}
    check("images packaged", len(refs) <= len(imgs),
          f"{stats['img']} tags / {len(refs)} distinct / {len(imgs)} files")
    icons = [s for s in re.findall(r'<img[^>]*src="([^"]*)"', body) if s.endswith('.svg')]
    if len(icons) > 5:
        print(f"        note: {len(icons)} svg <img> — likely decorative UI icons, consider stripping")

    # A chapter carrying nothing but its own heading means content was dropped in
    # conversion. Heading-only section openers and the cover/nav are legitimate.
    empty = []
    for n in xh:
        if any(k in n for k in ('cover', 'nav', 'title')):
            continue
        c = z.read(n).decode(errors='replace')
        if any(t in c for t in ('<img', '<table', '<pre', '<li')):
            continue
        text = ' '.join(re.sub(r'<[^>]+>', ' ', c.split('<body', 1)[-1]).split())
        text = re.sub(r'^epub:type="\w+">\s*', '', text)
        headings = ' '.join(re.sub(r'<[^>]+>', ' ', h).strip()
                            for h in re.findall(r'<h[1-6][^>]*>.*?</h[1-6]>', c, re.S))
        if len(text) - len(' '.join(headings.split())) < 20:
            empty.append(n)
    check("no empty chapters", not empty, f"{len(empty)} empty" + (f": {empty[:3]}" if empty else ""))

    if probes:
        # match against tag-stripped text: inline <code>/<em> otherwise split a
        # phrase across tags and a present string reads as missing
        flat = ' '.join(re.sub(r'<[^>]+>', ' ', body).split())
        def present(p):
            return p in body or ' '.join(p.split()) in flat
        missing = [p for p in probes if not present(p)]
        check("content probes", not missing, f"{len(probes) - len(missing)}/{len(probes)} found")
        for m in missing:
            print(f"        MISSING: {m[:70]}")

    print("OK" if not FAIL else f"FAILED: {', '.join(FAIL)}")
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
