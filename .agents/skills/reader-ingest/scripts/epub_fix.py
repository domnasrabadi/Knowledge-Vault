#!/usr/bin/env python3
"""Repair an EPUB for Reader, repack it correctly, and prove nothing was lost.

    epub_fix.py book.epub [--out fixed.epub] [--equations] [--no-watermarks]

Default output: ~/Downloads/<name> (fixed).epub. Never modifies the input.
Stdlib only, except --equations, which needs Pillow:
    uv run --with pillow python epub_fix.py book.epub --equations

Fixes, each counted in the report:
  1. Non-XML named entities (&eacute; &deg; ...) -> numeric references. XHTML
     predefines only amp/lt/gt/quot/apos; the rest fail strict XML parsing.
  2. Per-buyer watermarks — ALWAYS stripped (the user's standing decision),
     but only what epub_check.find_watermarks grades PII. A sparse email is an
     author's contact address and is left alone.
  3. Empty or generic alt text ("figure", "equation image" ×900) replaced with
     the adjacent "Figure N ..." caption. Reader surfaces alt text; it is the only
     textual trace an image leaves.
  4. --equations: inline-sized opaque equation PNGs. Recover LaTeX from the PNG's
     text chunks where it survives (-> $...$ text); otherwise strip white to
     transparency and recolour glyphs to #7D7D7D, legible at 4.1:1 on both white
     and Reader's dark background WITH NO CSS — Reader discards publisher CSS, so
     a filter:invert() fix would leave invisible equations.
  5. Repack with mimetype first and stored, then re-run epub_check on the output.

Refuses DRM-protected files: they can be reported on, not repaired.
"""
import re, sys, zlib, struct, pathlib, zipfile, html as htmllib
from html.entities import name2codepoint

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import epub_check  # noqa: E402

XML_OK = {'amp', 'lt', 'gt', 'quot', 'apos'}
MARKUP = ('.xhtml', '.html', '.htm', '.opf', '.ncx')


def words(files):
    return sum(len(re.sub(r'<[^>]+>', ' ', b.decode('utf-8', 'replace').split('<body', 1)[-1]).split())
               for n, b in files.items() if n.endswith(('.xhtml', '.html', '.htm')))


# ---------------------------------------------------------------- 1. entities

def fix_entities(text):
    n = 0
    def sub(m):
        nonlocal n
        name = m.group(1)
        if name in XML_OK or name not in name2codepoint:
            return m.group(0)
        n += 1
        return f'&#{name2codepoint[name]};'
    return re.sub(r'&([A-Za-z][A-Za-z0-9]*);', sub, text), n


# ---------------------------------------------------------------- 2. watermarks

INNER_BLOCK = r'<({t})\b[^>]*>((?:(?!</?\1\b).)*?{pat}(?:(?!</?\1\b).)*?)</\1>'


def strip_watermark(text, value):
    """Remove the innermost short block holding the stamp; else just the text."""
    removed = 0
    pat = re.escape(value)
    for tag in ('p', 'div', 'span', 'footer', 'small'):
        rx = re.compile(INNER_BLOCK.format(t=tag, pat=pat), re.S)
        def drop(m):
            nonlocal removed
            inner = ' '.join(re.sub(r'<[^>]+>', ' ', m.group(2)).split())
            if len(inner) < 250:      # a footer, not a paragraph that mentions it
                removed += 1
                return ''
            return m.group(0)
        text = rx.sub(drop, text)
    if value in text:                  # stamp embedded in real prose: cut the stamp only
        removed += text.count(value)
        text = re.sub(r'(?:Licensed to\s*)?' + pat, '', text)
    return text, removed


def fix_opf_title(text):
    """'Title (for . .)' / 'Title (for Name Email)' -> 'Title'."""
    return re.subn(r'(<dc:title[^>]*>[^<]*?)\s*\(for\b[^)<]*\)', r'\1', text)


# ---------------------------------------------------------------- 3. alt text

def fix_alts(files):
    alts = {}
    for n, b in files.items():
        if n.endswith(('.xhtml', '.html', '.htm')):
            for a in re.findall(r'<img\b[^>]*\balt="([^"]*)"', b.decode('utf-8', 'replace')):
                alts[a.strip()] = alts.get(a.strip(), 0) + 1
    generic = {a for a, c in alts.items() if c > 5 and len(a) < 30}

    def weak(alt):
        return alt is None or not alt.strip() or len(alt.strip()) < 15 or alt.strip() in generic

    total = 0
    block = re.compile(r'<(figure|div)\b([^>]*)>((?:(?!</?\1\b).)*?<img\b(?:(?!</?\1\b).)*?)</\1>', re.S)
    for n in [n for n in files if n.endswith(('.xhtml', '.html', '.htm'))]:
        text = files[n].decode('utf-8', 'replace')

        def lift(m):
            nonlocal total
            if m.group(1) == 'div' and 'figure' not in m.group(2):
                return m.group(0)
            inner = m.group(3)
            cap = (re.search(r'<figcaption\b[^>]*>(.*?)</figcaption>', inner, re.S)
                   or re.search(r'<h6\b[^>]*>(.*?)</h6>', inner, re.S)
                   or re.search(r'<p\b[^>]*>((?:<[^>]+>)*\s*(?:Figure|Fig\.|Table)\s+[\d.-]+.*?)</p>', inner, re.S))
            imgs = re.findall(r'<img\b[^>]*>', inner)
            if not cap or len(imgs) != 1:
                return m.group(0)
            alt_m = re.search(r'\balt="([^"]*)"', imgs[0])
            if not weak(alt_m.group(1) if alt_m else None):
                return m.group(0)
            caption = ' '.join(htmllib.unescape(re.sub(r'<[^>]+>', ' ', cap.group(1))).split())[:480]
            new_alt = htmllib.escape(caption, quote=True)
            new_img = (re.sub(r'\balt="[^"]*"', f'alt="{new_alt}"', imgs[0]) if alt_m
                       else imgs[0].replace('<img', f'<img alt="{new_alt}"', 1))
            total += 1
            return m.group(0).replace(imgs[0], new_img, 1)

        files[n] = block.sub(lift, text).encode('utf-8')
    return total


# ---------------------------------------------------------------- 4. equations

def png_text_chunks(data):
    """tEXt / iTXt / zTXt payloads — where Manning-style LaTeX sometimes survives."""
    out, i = [], 8
    while i + 8 <= len(data):
        length, kind = struct.unpack('>I4s', data[i:i + 8])
        chunk = data[i + 8:i + 8 + length]
        if kind == b'tEXt':
            out.append(chunk.split(b'\0', 1)[-1].decode('latin-1', 'replace'))
        elif kind == b'zTXt':
            try:
                out.append(zlib.decompress(chunk.split(b'\0', 1)[-1][1:]).decode('latin-1', 'replace'))
            except zlib.error:
                pass
        elif kind == b'iTXt':
            parts = chunk.split(b'\0', 5)
            if len(parts) == 6:
                try:
                    out.append((zlib.decompress(parts[5]) if parts[1:2] == [b'\x01'] else parts[5]).decode('utf-8', 'replace'))
                except zlib.error:
                    pass
        i += 12 + length
    return out


def latex_in(chunks):
    for c in chunks:
        if re.search(r'\\[a-zA-Z]+|[_^]\{|\$', c) and len(c) < 2000:
            return c.strip().strip('$').strip()
    return None


def fix_equations(files):
    """Returns (latex_recovered, recoloured). Needs Pillow for the recolour."""
    try:
        from PIL import Image
        import io
    except ImportError:
        print('  ! --equations needs Pillow: uv run --with pillow python epub_fix.py ...')
        return 0, 0

    recovered = recoloured = 0
    replaced = set()
    by_base = {pathlib.PurePosixPath(n).name: n for n in files if n.lower().endswith('.png')}
    for n in [n for n in files if n.endswith(('.xhtml', '.html', '.htm'))]:
        text = files[n].decode('utf-8', 'replace')

        def handle(m):
            nonlocal recovered, recoloured
            tag = m.group(0)
            src = re.search(r'\bsrc="([^"]+)"', tag).group(1)
            png = by_base.get(pathlib.PurePosixPath(src).name)
            if not png:
                return tag
            data = files[png]
            if data[12:16] != b'IHDR':
                return tag
            w, h = struct.unpack('>II', data[16:24])
            if not (h < 60 and w < 400):            # plates only, never real figures
                return tag
            tex = latex_in(png_text_chunks(data))
            if tex:
                recovered += 1
                replaced.add(png)
                return f'${htmllib.escape(tex, quote=False)}$'
            if data[25] not in (0, 2):              # already has alpha: leave it
                return tag
            im = Image.open(io.BytesIO(data)).convert('L')
            alpha = im.point(lambda v: 255 - v)     # white -> transparent, ink -> opaque
            out = Image.new('RGBA', im.size, (0x7D, 0x7D, 0x7D, 0))
            out.putalpha(alpha)
            buf = io.BytesIO()
            out.save(buf, 'PNG', optimize=True)
            files[png] = buf.getvalue()
            recoloured += 1
            return tag

        files[n] = re.sub(r'<img\b[^>]*>', handle, text).encode('utf-8')
    return recovered, recoloured, replaced


def drop_unreferenced(files, candidates):
    """Remove images that recovered text made redundant — from the zip AND the
    manifest. Checks markup and CSS, so nothing a stylesheet needs is touched."""
    refs = ' '.join(b.decode('utf-8', 'replace') for n, b in files.items()
                    if n.endswith(MARKUP + ('.css',)) and not n.endswith('.opf'))
    gone = [c for c in candidates if pathlib.PurePosixPath(c).name not in refs]
    for c in gone:
        del files[c]
        name = re.escape(pathlib.PurePosixPath(c).name)
        for n in [n for n in files if n.endswith('.opf')]:
            files[n] = re.sub(rf'\s*<item\b[^>]*href="[^"]*{name}"[^>]*/>', '',
                              files[n].decode('utf-8', 'replace')).encode('utf-8')
    return len(gone)


# ---------------------------------------------------------------- main

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        print(__doc__)
        sys.exit(2)
    src = pathlib.Path(args[0])
    out = pathlib.Path(sys.argv[sys.argv.index('--out') + 1]) if '--out' in sys.argv else \
        pathlib.Path.home() / 'Downloads' / f'{src.stem} (fixed).epub'
    if out.resolve() == src.resolve():
        sys.exit('refusing to overwrite the input; choose a different --out')

    z = zipfile.ZipFile(src)
    if any('encryption.xml' in n for n in z.namelist()):
        sys.exit('DRM / encryption present — this file can be checked but not repaired.')
    meta = epub_check.parse_opf(z, epub_check.find_opf(z))[0]
    stamps = [(label, v) for label, v, _, grade in epub_check.find_watermarks(z, meta) if grade == 'PII']

    names = [n for n in z.namelist() if n != 'mimetype' and not n.endswith('/')]
    files = {n: z.read(n) for n in names}
    before = words(files)
    report = {}

    ent = 0
    for n in [n for n in files if n.endswith(MARKUP)]:
        t, k = fix_entities(files[n].decode('utf-8', 'replace'))
        files[n] = t.encode('utf-8')
        ent += k
    report['named entities -> numeric'] = ent

    w_before_wm = words(files)
    if stamps and '--no-watermarks' not in sys.argv:
        wm = 0
        for n in [n for n in files if n.endswith(MARKUP)]:
            t = files[n].decode('utf-8', 'replace')
            if n.endswith('.opf'):
                t, k = fix_opf_title(t)
                wm += k
            for _, v in stamps:
                if v in t:
                    t, k = strip_watermark(t, v)
                    wm += k
            files[n] = t.encode('utf-8')
        report['watermark stamps removed'] = wm
        report['watermark values'] = ', '.join(sorted({v[:40] for _, v in stamps}))

    w_wm = w_before_wm - words(files)
    report['alt text lifted from captions'] = fix_alts(files)

    w_before_eq, w_eq = words(files), 0
    if '--equations' in sys.argv:
        rec, col, replaced = fix_equations(files)
        report['equation LaTeX recovered -> $...$'] = rec
        report['equation plates recoloured #7D7D7D'] = col
        report['redundant equation images removed'] = drop_unreferenced(files, replaced)
        w_eq = words(files) - w_before_eq
        names = [n for n in names if n in files]

    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, 'w') as o:
        o.writestr(zipfile.ZipInfo('mimetype'), 'application/epub+zip', compress_type=zipfile.ZIP_STORED)
        for n in names:
            o.writestr(n, files[n], compress_type=zipfile.ZIP_DEFLATED)

    after = words(files)
    print(f'{src.name} -> {out}')
    for k, v in report.items():
        print(f'  {k}: {v}')
    # Count in, count out: every changed word must be accounted for by a stage.
    unexplained = (after - before) + w_wm - w_eq
    print(f'  words: {before:,} -> {after:,} ({after - before:+,}) = '
          f'watermarks -{w_wm:,}, recovered LaTeX +{w_eq:,}, unexplained {unexplained:+,}')
    if unexplained:
        print('  ! words changed that no fix accounts for — inspect before shipping')
    print('\n--- re-check of the fixed file ---')
    rep, _, _ = epub_check.audit(str(out))
    sys.exit(1 if rep.fails() else 0)


if __name__ == '__main__':
    main()
