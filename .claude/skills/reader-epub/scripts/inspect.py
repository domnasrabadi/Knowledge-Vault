#!/usr/bin/env python3
"""Audit any EPUB — yours or a publisher's — against the gold-standard profile.

    inspect.py book.epub [--json] [--images] [--spine]
    inspect.py compare a.epub b.epub        # two copies of the same title

Stdlib only. Read-only: never writes to the file it is given.

This is the AUDIT verb. `verify.py` checks a book you just built and knows what
you meant to put in it; `inspect.py` knows nothing about the source and asks
only "is this file sound, and is it good in Reader?". Three sessions rebuilt
this by hand before it existed — every check below came from a real finding.

Findings are graded:
  FAIL  structurally broken — strict-XML failures, dead anchors, missing files
  WARN  degrades reading in Reader — thin alt text, inline opaque equation PNGs
  PII   a per-buyer watermark carrying a real name or email
  NOTE  measured, not a defect

Calibration for what is benign (O'Reilly template residue, NCX deeper than nav,
EPUB 2.0) is in references/gold-standard.md. Read it before reporting, or you
will file false alarms the catalogue already dismissed.
"""
import sys, re, json, zipfile, posixpath, collections
import xml.etree.ElementTree as ET

NS = {'opf': 'http://www.idpf.org/2007/opf',
      'dc': 'http://purl.org/dc/elements/1.1/',
      'ncx': 'http://www.daisy.org/z3986/2005/ntoc/',
      'c': 'urn:oasis:names:tc:opendocument:xmlns:container',
      'x': 'http://www.w3.org/1999/xhtml'}

# XHTML predefines exactly these five. Everything else fails strict XML parsing.
XML_ENTITIES = {'amp', 'lt', 'gt', 'quot', 'apos'}
NAMED_ENTITY = re.compile(r'&([a-zA-Z][a-zA-Z0-9]{1,31});')

# Publisher contact addresses appear in every copy of a title and are NOT
# watermarks. Filtering them is what keeps the PII check believable — an audit
# that cries wolf on support@oreilly.com gets ignored when it finds a real name.
ROLE_ADDRESS = re.compile(
    r'^(?:support|info|corporate|permissions|sales|orders|help|contact|feedback|'
    r'academic|press|rights|bookquestions|errata|noreply|no-reply)@', re.I)
PUBLISHER_DOMAIN = re.compile(
    r'@(?:oreilly|manning|pragprog|apress|packt|wiley|springer|elsevier|'
    r'safaribooksonline)\.[\w.]+$', re.I)

# Per-buyer watermarks. These are a privacy issue and also how you tell two
# copies of the same book apart.
PII_PATTERNS = [
    (re.compile(r'[\w.+-]+@[\w-]+\.[\w.]+'), 'email address'),
    (re.compile(r'Licensed to ([^<\n]{3,60})', re.I), 'licence footer'),
    (re.compile(r'\bThis copy is for\b[^<\n]{0,60}', re.I), 'per-copy notice'),
    (re.compile(r'\b(?:purchased|registered|prepared) (?:by|for) ([A-Z][a-z]+ [A-Z][a-z]+)'), 'named purchaser'),
]

# Provenance traces. Not defects on their own, but they say where a file came
# from, and calibre_bookmarks.txt can hold someone else's reading position.
PROVENANCE = [
    ('calibre_bookmarks.txt', 'Calibre bookmarks — may contain another reader\'s position'),
    ('calibre', 'Calibre residue'),
    ('com.apple.ibooks.display-options.xml', 'opened in Apple Books (benign)'),
    ('iTunesMetadata.plist', 'iTunes/Books metadata'),
]


class Report:
    def __init__(self):
        self.rows = []

    def add(self, grade, label, detail=''):
        self.rows.append((grade, label, detail))

    def fails(self):
        return [r for r in self.rows if r[0] in ('FAIL', 'PII')]

    def dump(self):
        for grade, label, detail in self.rows:
            print(f"  {grade:5} {label}{(' — ' + detail) if detail else ''}")


def _text(z, name):
    try:
        return z.read(name).decode('utf-8', errors='replace')
    except KeyError:
        return ''


def find_opf(z):
    """container.xml -> the OPF path. Never assume OEBPS/content.opf."""
    try:
        root = ET.fromstring(z.read('META-INF/container.xml'))
    except (KeyError, ET.ParseError):
        cands = [n for n in z.namelist() if n.endswith('.opf')]
        return cands[0] if cands else None
    el = root.find('.//c:rootfile', NS)
    return el.get('full-path') if el is not None else None


def parse_opf(z, opf_path):
    """Return (metadata dict, manifest {id: (href, media-type, properties)}, spine [ids])."""
    root = ET.fromstring(z.read(opf_path))
    base = posixpath.dirname(opf_path)

    meta = {'version': root.get('version', '?')}
    for tag in ('title', 'creator', 'language', 'publisher', 'date', 'identifier'):
        el = root.find(f'.//dc:{tag}', NS)
        if el is not None and el.text:
            meta[tag] = el.text.strip()

    manifest = {}
    for item in root.findall('.//opf:manifest/opf:item', NS):
        href = item.get('href', '')
        full = posixpath.normpath(posixpath.join(base, href)) if base else href
        manifest[item.get('id')] = (full, item.get('media-type', ''), item.get('properties', ''))

    spine = [i.get('idref') for i in root.findall('.//opf:spine/opf:itemref', NS)]
    return meta, manifest, spine, base


def check_container(z, rep):
    """mimetype must be the first zip entry and stored uncompressed."""
    names = z.namelist()
    infos = z.infolist()
    rep.add('FAIL' if z.testzip() is not None else 'NOTE', 'zip integrity',
            'corrupt' if z.testzip() is not None else 'intact')

    if not names or names[0] != 'mimetype':
        rep.add('FAIL', 'mimetype first entry', f'first entry is {names[0] if names else "(empty)"}')
    elif infos[0].compress_type != zipfile.ZIP_STORED:
        rep.add('FAIL', 'mimetype stored uncompressed', 'it is deflated')
    else:
        rep.add('NOTE', 'mimetype first + stored', 'ok')

    if 'mimetype' in names and _text(z, 'mimetype').strip() != 'application/epub+zip':
        rep.add('FAIL', 'mimetype content', repr(_text(z, 'mimetype')[:40]))

    enc = [n for n in names if 'encryption.xml' in n or n.endswith('.xml') and 'rights' in n]
    if any('encryption.xml' in n for n in names):
        rep.add('FAIL', 'DRM / encryption present', ', '.join(enc))


def check_xml(z, rep):
    """Strict-XML parse of every XHTML/OPF/NCX. This is what catches named entities."""
    targets = [n for n in z.namelist()
               if n.endswith(('.xhtml', '.html', '.opf', '.ncx')) and not n.startswith('__MACOSX')]
    bad = []
    for n in targets:
        try:
            ET.fromstring(z.read(n))
        except ET.ParseError as e:
            bad.append(f'{n}: {e}')
    rep.add('FAIL' if bad else 'NOTE', 'strict XML parse',
            f'{len(targets) - len(bad)}/{len(targets)} ok' + (f' | first: {bad[0][:90]}' if bad else ''))

    # The usual cause, reported separately because the fix is mechanical.
    hits = collections.Counter()
    files = set()
    for n in targets:
        for ent in NAMED_ENTITY.findall(_text(z, n)):
            if ent not in XML_ENTITIES:
                hits[ent] += 1
                files.add(n)
    if hits:
        top = ', '.join(f'&{k};×{v}' for k, v in hits.most_common(6))
        rep.add('FAIL', 'non-XML named entities',
                f'{sum(hits.values())} across {len(files)}/{len(targets)} files — {top}')
    else:
        rep.add('NOTE', 'non-XML named entities', '0')
    return bad


def check_nav(z, manifest, rep):
    """Ship both: nav document for EPUB 3, NCX for compatibility."""
    nav = next((h for h, _, p in manifest.values() if 'nav' in (p or '').split()), None)
    if nav is None:
        nav = next((n for n in z.namelist() if n.endswith(('nav.xhtml', 'toc.xhtml'))), None)
    ncx = next((h for h, mt, _ in manifest.values() if mt == 'application/x-dtbncx+xml'), None)
    if ncx is None:
        ncx = next((n for n in z.namelist() if n.endswith('.ncx')), None)

    nav_n = ncx_n = 0
    nav_depth = ncx_depth = 0
    if nav:
        body = _text(z, nav)
        nav_n = len(re.findall(r'<a[^>]+href=', body))
        nav_depth = _max_nest(body, 'ol')
    if ncx:
        body = _text(z, ncx)
        ncx_n = len(re.findall(r'<navPoint', body))
        ncx_depth = _max_nest(body, 'navPoint')

    rep.add('NOTE' if nav else 'WARN', 'nav document',
            f'{nav_n} entries, depth {nav_depth}' if nav else 'absent (EPUB 3 requires it)')
    rep.add('NOTE' if ncx else 'WARN', 'NCX',
            f'{ncx_n} navPoints, depth {ncx_depth}' if ncx else 'absent (older readers lose the TOC)')
    if nav and nav_n <= 1:
        rep.add('FAIL', 'navigation usable', f'only {nav_n} entry — the TOC is flat or empty')
    # NCX deeper than nav is a normal house pattern; see gold-standard.md.
    return nav, ncx


def _max_nest(body, tag):
    depth = best = 0
    for m in re.finditer(rf'</?{tag}\b', body):
        depth += 1 if m.group(0)[1] != '/' else -1
        best = max(best, depth)
    return best


def check_manifest(z, manifest, spine, rep):
    """Both directions: nothing declared-but-missing, nothing present-but-undeclared."""
    files = {n for n in z.namelist() if not n.endswith('/') and not n.startswith('__MACOSX')}
    declared = {h for h, _, _ in manifest.values()}
    skip = {'mimetype', 'META-INF/container.xml'}

    missing = sorted(declared - files)
    unmanifested = sorted(f for f in files - declared
                          if f not in skip and not f.endswith(('.opf',))
                          and 'META-INF' not in f)
    rep.add('FAIL' if missing else 'NOTE', 'manifest -> files',
            f'{len(missing)} declared but absent' + (f': {missing[:3]}' if missing else ''))
    rep.add('WARN' if unmanifested else 'NOTE', 'files -> manifest',
            f'{len(unmanifested)} unmanifested' + (f': {unmanifested[:3]}' if unmanifested else ''))

    dangling = [i for i in spine if i not in manifest]
    if dangling:
        rep.add('FAIL', 'spine -> manifest', f'{len(dangling)} idrefs with no item: {dangling[:3]}')
    return missing, unmanifested


def check_links(z, manifest, rep):
    """Three classes of breakage: missing files, dead #anchors, dangling back-links."""
    files = {n for n in z.namelist()}
    docs = [h for h, mt, _ in manifest.values() if 'html' in mt]
    if not docs:
        docs = [n for n in files if n.endswith(('.xhtml', '.html'))]

    ids_by_doc = {}
    for d in docs:
        ids_by_doc[d] = set(re.findall(r'\bid="([^"]+)"', _text(z, d)))

    broken_file, dead_anchor = [], []
    for d in docs:
        body = _text(z, d)
        base = posixpath.dirname(d)
        for ref in re.findall(r'(?:href|src)="([^"]*)"', body):
            # Split on the FIRST '#'. A greedy path group swallows the fragment and
            # every internal cross-reference then reads as a missing file.
            path, _, frag = ref.partition('#')
            frag = ('#' + frag) if frag else ''
            if path.startswith(('http:', 'https:', 'mailto:', 'data:', 'tel:')):
                continue
            if path:
                tgt = posixpath.normpath(posixpath.join(base, path))
                if tgt not in files:
                    broken_file.append(f'{d} -> {path}')
                    continue
            else:
                tgt = d
            if frag and frag[1:] and frag[1:] not in ids_by_doc.get(tgt, set()):
                dead_anchor.append(f'{d} -> {frag}')

    rep.add('FAIL' if broken_file else 'NOTE', 'broken file references',
            f'{len(broken_file)}' + (f' | e.g. {broken_file[0][:80]}' if broken_file else ''))
    rep.add('FAIL' if dead_anchor else 'NOTE', 'dead internal anchors',
            f'{len(dead_anchor)}' + (f' | e.g. {dead_anchor[0][:80]}' if dead_anchor else ''))

    # Anchors whose number is a concatenation of smaller valid ones are the
    # merged-footnote-marker bug: superscript 3 and 4 extract as the run "34".
    suspect = [a for a in dead_anchor if re.search(r'#\w*?(\d{2,})\b', a)]
    if suspect:
        rep.add('NOTE', 'merged-marker suspects',
                f'{len(suspect)} dead anchors end in multi-digit runs — check for merged footnote markers')
    return broken_file, dead_anchor


def check_images(z, manifest, rep, verbose=False):
    """Alt coverage, and the inline-opaque-equation-PNG profile that ruins dark mode."""
    files = {n for n in z.namelist()}
    docs = [n for n in files if n.endswith(('.xhtml', '.html'))]
    imgs_on_disk = {n for n in files if n.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'))}

    tags, referenced = [], set()
    for d in docs:
        base = posixpath.dirname(d)
        for m in re.finditer(r'<img\b([^>]*)>', _text(z, d)):
            attrs = m.group(1)
            src = (re.search(r'src="([^"]*)"', attrs) or [None, ''])[1]
            alt = re.search(r'alt="([^"]*)"', attrs)
            w = re.search(r'width="(\d+)"', attrs)
            h = re.search(r'height="(\d+)"', attrs)
            if src and not src.startswith('data:'):
                referenced.add(posixpath.normpath(posixpath.join(base, src)))
            tags.append({'src': src, 'alt': alt.group(1) if alt else None,
                         'w': int(w.group(1)) if w else None,
                         'h': int(h.group(1)) if h else None, 'doc': d})

    if not tags:
        rep.add('NOTE', 'images', 'none')
        return tags

    no_alt = [t for t in tags if not t['alt'] or not t['alt'].strip()]
    # Alt text that is the same label on hundreds of images is equivalent to none.
    alts = collections.Counter(t['alt'].strip() for t in tags if t['alt'] and t['alt'].strip())
    generic = [(a, n) for a, n in alts.most_common(3) if n > 5 and len(a) < 30]
    thin = [t for t in tags if t['alt'] and 0 < len(t['alt'].strip()) < 15]

    pct = 100 * len(no_alt) // len(tags)
    rep.add('FAIL' if pct > 20 else ('WARN' if no_alt else 'NOTE'), 'alt coverage',
            f'{len(tags) - len(no_alt)}/{len(tags)} have alt ({100 - pct}%)')
    if generic:
        rep.add('WARN', 'alt text is a repeated label',
                '; '.join(f'"{a}" ×{n}' for a, n in generic) + ' — Reader surfaces alt, so this reads as nothing')
    elif thin:
        rep.add('WARN', 'alt text very short', f'{len(thin)} under 15 chars')

    sized = [t for t in tags if t['w'] and t['h']]
    if len(sized) < len(tags) // 2:
        rep.add('WARN', 'explicit width/height', f'only {len(sized)}/{len(tags)} — expect layout shift')

    # The Manning finding: 951 equation PNGs, 93% inline-sized, all opaque white.
    # In Reader's dark mode those are white boxes mid-sentence.
    if sized:
        inline = [t for t in sized if t['h'] and t['h'] < 60 and t['w'] and t['w'] < 400]
        if len(inline) > 20 and len(inline) > len(sized) // 2:
            med = sorted(t['w'] for t in inline)[len(inline) // 2], sorted(t['h'] for t in inline)[len(inline) // 2]
            opaque = _count_opaque_png(z, [t['src'] for t in inline], docs)
            rep.add('WARN', 'inline-sized image plates',
                    f'{len(inline)}/{len(sized)} images are inline-sized (median {med[0]}×{med[1]}px)'
                    + (f', {opaque} sampled as opaque RGB' if opaque else '')
                    + ' — likely equation PNGs; see gold-standard.md for the #7D7D7D remedy')

    orphans = sorted(imgs_on_disk - referenced)
    if orphans:
        rep.add('WARN', 'orphaned images', f'{len(orphans)} never referenced: {orphans[:3]}')

    if verbose:
        print('\n  image size histogram (w×h):')
        hist = collections.Counter(f"{t['w']}×{t['h']}" for t in sized)
        for k, v in hist.most_common(12):
            print(f'    {k:>12}  {v}')
    return tags


def _count_opaque_png(z, srcs, docs):
    """Sample PNG headers: colour type 0/2 means no alpha channel at all."""
    n = 0
    names = {posixpath.basename(x): x for x in z.namelist()}
    for s in [x for x in srcs if x][:40]:
        f = names.get(posixpath.basename(s))
        if not f or not f.lower().endswith('.png'):
            continue
        try:
            head = z.read(f)[:26]
            if head[12:16] == b'IHDR' and head[25] in (0, 2):  # greyscale / truecolour, no alpha
                n += 1
        except KeyError:
            continue
    return n


def check_spine(z, manifest, spine, rep, verbose=False):
    """Per-spine word counts and first heading. Empty stubs render as blank pages."""
    rows, empty = [], []
    for idref in spine:
        if idref not in manifest:
            continue
        href = manifest[idref][0]
        body = _text(z, href)
        if not body:
            continue
        head = re.search(r'<h[1-6][^>]*>(.*?)</h[1-6]>', body, re.S)
        head = ' '.join(re.sub(r'<[^>]+>', ' ', head.group(1)).split()) if head else ''
        inner = body.split('<body', 1)[-1]
        words = len(re.sub(r'<[^>]+>', ' ', inner).split())
        has_media = any(t in inner for t in ('<img', '<table', '<pre'))
        rows.append((href, words, head))
        if words - len(head.split()) < 12 and not has_media:
            empty.append((href, words, head))

    rep.add('WARN' if empty else 'NOTE', 'empty spine documents',
            f'{len(empty)} carry nothing but a heading' + (f': {[e[0] for e in empty][:3]}' if empty else ''))
    total = sum(r[1] for r in rows)
    rep.add('NOTE', 'body length', f'{total:,} words across {len(rows)} spine documents')

    if verbose:
        print('\n  spine:')
        for href, words, head in rows:
            print(f'    {words:>7,}  {posixpath.basename(href):<34} {head[:44]}')
    return rows


def check_provenance(z, meta, rep):
    """Watermarks, Calibre residue, template placeholders."""
    names = z.namelist()
    for needle, note in PROVENANCE:
        hit = [n for n in names if needle in n.lower()]
        if hit:
            grade = 'WARN' if 'calibre_bookmarks' in needle else 'NOTE'
            rep.add(grade, 'provenance', f'{note} ({hit[0]})')

    # Scan metadata and body text for per-buyer watermarks.
    blob = json.dumps(meta) + ' '.join(
        _text(z, n) for n in names if n.endswith(('.xhtml', '.html', '.opf'))
    )[:4_000_000]
    for pat, label in PII_PATTERNS:
        found = collections.Counter(
            m if isinstance(m, str) else m[0] for m in pat.findall(blob))
        real = {k: v for k, v in found.items()
                if k and 'example.com' not in k
                and not (label == 'email address'
                         and (ROLE_ADDRESS.match(k) or PUBLISHER_DOMAIN.search(k)))}
        if real:
            top = list(real.items())[:2]
            rep.add('PII', f'watermark: {label}',
                    '; '.join(f'"{k[:48]}" ×{v}' for k, v in top)
                    + (f' (+{len(real) - len(top)} more)' if len(real) > len(top) else ''))

    title = meta.get('title', '')
    if re.search(r'\(for\s*\.\s*\.\)|title_title', title):
        rep.add('NOTE', 'template placeholder in dc:title',
                f'{title!r} — benign publisher residue, see gold-standard.md')


def audit(path, as_json=False, images=False, spine=False):
    z = zipfile.ZipFile(path)
    rep = Report()
    opf_path = find_opf(z)
    if not opf_path:
        print(f'{path}: no OPF found — not a readable EPUB')
        return rep, {}, []

    meta, manifest, spine_ids, _ = parse_opf(z, opf_path)

    print(f'\n{path}')
    print(f"  {meta.get('title', '(untitled)')} — {meta.get('creator', '(no creator)')}")
    print(f"  EPUB {meta.get('version', '?')} · {meta.get('publisher', 'no publisher')}"
          f" · {meta.get('date', 'no date')} · {len(manifest)} manifest items\n")

    if meta.get('version', '').startswith('2'):
        rep.add('NOTE', 'EPUB version', '2.0 — a lower spec, not a defect; the NCX carries the TOC')
    else:
        rep.add('NOTE', 'EPUB version', meta.get('version', '?'))

    check_container(z, rep)
    check_xml(z, rep)
    check_nav(z, manifest, rep)
    check_manifest(z, manifest, spine_ids, rep)
    check_links(z, manifest, rep)
    rows = check_spine(z, manifest, spine_ids, rep, verbose=spine)
    check_images(z, manifest, rep, verbose=images)
    check_provenance(z, meta, rep)

    rep.dump()
    bad = rep.fails()
    warns = [r for r in rep.rows if r[0] == 'WARN']
    print(f"\n  {len(bad)} blocking, {len(warns)} degrading."
          f" {'Sound.' if not bad else 'Needs remediation.'}")
    if as_json:
        print(json.dumps({'file': path, 'meta': meta,
                          'findings': [{'grade': g, 'label': l, 'detail': d} for g, l, d in rep.rows]},
                         indent=2))
    return rep, meta, rows


def compare(a, b):
    """Which of two copies of the same title is canonical?"""
    ra, ma, rowsa = audit(a)
    rb, mb, rowsb = audit(b)

    za, zb = zipfile.ZipFile(a), zipfile.ZipFile(b)
    na, nb = set(za.namelist()), set(zb.namelist())
    print('\n=== file sets ===')
    print(f'  only in A: {len(na - nb)} {sorted(na - nb)[:5]}')
    print(f'  only in B: {len(nb - na)} {sorted(nb - na)[:5]}')

    print('\n=== per-chapter word counts ===')
    print(f"  {'A':>8} {'B':>8}   heading")
    wa = {posixpath.basename(h): (w, hd) for h, w, hd in rowsa}
    wb = {posixpath.basename(h): (w, hd) for h, w, hd in rowsb}
    for k in sorted(set(wa) | set(wb)):
        x, y = wa.get(k, (0, '')), wb.get(k, (0, ''))
        flag = '  <-- differs' if abs(x[0] - y[0]) > max(20, x[0] // 50) else ''
        print(f'  {x[0]:>8,} {y[0]:>8,}   {k[:30]:<32}{(x[1] or y[1])[:30]}{flag}')

    print('\n=== verdict inputs ===')
    for label, rep in (('A', ra), ('B', rb)):
        print(f'  {label}: {len(rep.fails())} blocking, '
              f'{len([r for r in rep.rows if r[0] == "WARN"])} degrading, '
              f'{len([r for r in rep.rows if r[0] == "PII"])} watermark findings')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        sys.exit(2)
    if args[0] == 'compare':
        compare(args[1], args[2])
        return
    rep, _, _ = audit(args[0], '--json' in sys.argv, '--images' in sys.argv, '--spine' in sys.argv)
    sys.exit(1 if rep.fails() else 0)


if __name__ == '__main__':
    main()
