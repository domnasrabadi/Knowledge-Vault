#!/usr/bin/env python3
"""Rasterise vector figures (PDF or SVG) to reader-friendly PNGs.

    rasterize.py pdfs <srcdir> <outdir> [--dpi 170] [--max-width 1600]
    rasterize.py svgs <page.html> <outdir> [--selector svg.chart] [--scale 3]

Needs pymupdf + pillow:  uv run --with pymupdf --with pillow --with beautifulsoup4 --with lxml python rasterize.py ...

Why: LaTeX figures ship as PDF and web charts as inline SVG; neither survives
into an EPUB usefully. Inline SVG in particular is dropped entirely by pandoc's
HTML reader, so charts must become <img> before conversion.
"""
import sys, pathlib


def arg(flag, default, cast=str):
    return cast(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


def shrink(path, max_width):
    from PIL import Image
    im = Image.open(path)
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    im.convert('RGB').save(path, optimize=True)
    return im.size


def pdfs(srcdir, outdir, dpi, max_width):
    import pymupdf
    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    n = 0
    for p in sorted(pathlib.Path(srcdir).rglob('*.pdf')):
        try:
            d = pymupdf.open(p)
            tgt = out / (p.stem + '.png')
            d[0].get_pixmap(dpi=dpi).save(tgt)
            size = shrink(tgt, max_width)
            print(f"  {p.stem}.png  {size[0]}x{size[1]}  {tgt.stat().st_size // 1024}KB")
            n += 1
        except Exception as e:
            print(f"  ! {p}: {e}", file=sys.stderr)
    print(f"rasterised {n} figures -> {outdir}")


def svgs(htmlfile, outdir, selector, scale):
    """Extract inline SVG, resolve CSS custom properties, render to PNG.

    Site charts colour themselves with var(--accent1) etc. Those resolve to
    nothing outside the page, so everything renders black-on-black unless the
    :root palette is substituted in first."""
    import re, pymupdf
    from bs4 import BeautifulSoup
    src = pathlib.Path(htmlfile).read_text()
    soup = BeautifulSoup(src, 'lxml')

    css = '\n'.join(t.get_text() for t in soup.find_all('style'))
    for extra in pathlib.Path(htmlfile).parent.glob('*.css'):
        css += '\n' + extra.read_text(errors='replace')
    palette = {k: v.strip() for k, v in
               re.findall(r'(--[\w-]+)\s*:\s*([^;]+)', ' '.join(re.findall(r':root\s*\{([^}]*)\}', css)))}
    if not palette:
        print("  ! no :root palette found — fetch the site stylesheet next to the html", file=sys.stderr)

    def resolve(t):
        for _ in range(3):
            new = re.sub(r'var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)',
                         lambda m: palette.get(m.group(1), m.group(2) or 'currentColor'), t)
            if new == t:
                return t
            t = new
        return t

    out = pathlib.Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    els = soup.select(selector)
    for i, sv in enumerate(els):
        vb = sv.get('viewBox') or sv.get('viewbox')
        if not vb:
            print(f"  ! chart{i}: no viewBox, skipped", file=sys.stderr)
            continue
        w, h = [float(x) for x in vb.split()[2:]]
        sv['xmlns'] = "http://www.w3.org/2000/svg"
        sv['viewBox'], sv['width'], sv['height'] = vb, str(w), str(h)
        if sv.has_attr('viewbox'):
            del sv['viewbox']
        for el in sv.find_all(True):
            for a in ('fill', 'stroke', 'style', 'font-family', 'font-size', 'stop-color'):
                if el.has_attr(a):
                    el[a] = resolve(el[a])
        f = out / f'chart{i}.svg'
        f.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + str(sv))
        try:
            d = pymupdf.open(str(f))
            png = out / f'chart{i}.png'
            d[0].get_pixmap(matrix=pymupdf.Matrix(scale, scale), alpha=False).save(png)
            # alt text from the chart's own labels keeps the data reachable
            labels = [t.get_text(' ', strip=True) for t in sv.find_all('text')]
            (out / f'chart{i}.alt').write_text(
                ("Chart: " + "; ".join(dict.fromkeys([t for t in labels if t])))[:480])
            print(f"  chart{i}.png  {png.stat().st_size // 1024}KB  ({len(labels)} labels)")
        except Exception as e:
            print(f"  ! chart{i}: {e}", file=sys.stderr)
    print(f"rendered {len(els)} charts -> {outdir}")
    print("  NOTE: open one with Read to confirm it isn't blank before shipping")


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'pdfs':
        pdfs(sys.argv[2], sys.argv[3], arg('--dpi', 170, int), arg('--max-width', 1600, int))
    else:
        svgs(sys.argv[2], sys.argv[3], arg('--selector', 'svg'), arg('--scale', 3, float))
