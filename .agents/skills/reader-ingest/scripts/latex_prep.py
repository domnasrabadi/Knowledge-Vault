#!/usr/bin/env python3
"""Prepare an arXiv LaTeX source tree for pandoc, then repair what pandoc loses.

    latex_prep.py prep  <srcdir> <builddir>            # fix up a copy of the source
    latex_prep.py relabel <out.html> <tex...>          # reattach table ids after conversion

`prep` applies the fixes that silently destroy content otherwise:
  - \\resizebox{..}{..}{<tabular>}  -> pandoc emits NOTHING for the table; unwrap it
  - custom verbatim envs (prompt, lstlisting) -> remapped to `verbatim` so they stay <pre>
  - \\textsc{..} inside math -> pandoc's math reader hard-errors; uppercase it
  - figure .pdf includes -> .png (rasterise separately with svg_raster.py / pymupdf)
  - \\bibliography{x} -> \\input{x.bbl} so references survive without bibtex

`relabel` fixes dead "see Table 4" links: pandoc drops \\label inside table
environments, so table ids are matched back by caption text.
"""
import re, sys, shutil, pathlib, difflib

VERBATIM_ENVS = ('prompt', 'lstlisting', 'promptbox', 'systemprompt')


def brace_match(s, i):
    """Return (content, index_after) for the brace group starting at/after i."""
    while i < len(s) and s[i] != '{':
        i += 1
    depth, start = 0, i + 1
    while i < len(s):
        depth += (s[i] == '{') - (s[i] == '}')
        i += 1
        if depth == 0:
            return s[start:i - 1], i
    return s[start:], i


def unwrap_cmd(t, cmd, nargs):
    """Remove \\cmd{a}{b}{CONTENT} wrappers, keeping CONTENT."""
    out, i = [], 0
    while True:
        m = re.search(r'\\' + cmd + r'\b', t[i:])
        if not m:
            out.append(t[i:])
            break
        out.append(t[i:i + m.start()])
        j = i + m.end()
        for _ in range(nargs):
            _, j = brace_match(t, j)
        content, j = brace_match(t, j)
        out.append(content)
        i = j
    return ''.join(out)


def prep(srcdir, builddir):
    src, build = pathlib.Path(srcdir), pathlib.Path(builddir)
    if build.exists():
        shutil.rmtree(build)
    shutil.copytree(src, build)
    changed = []
    for f in build.rglob('*.tex'):
        t = orig = f.read_text(errors='replace')
        t = unwrap_cmd(t, 'resizebox', 2)
        t = unwrap_cmd(t, 'scalebox', 1)
        for env in VERBATIM_ENVS:
            t = t.replace(rf'\begin{{{env}}}', r'\begin{verbatim}') \
                 .replace(rf'\end{{{env}}}', r'\end{verbatim}')
        t = re.sub(r'\\textsc\{([^{}]*)\}', lambda m: m.group(1).upper(), t)
        t = re.sub(r'(\\includegraphics(?:\[[^]]*\])?\{)([^}]+)\}',
                   lambda m: m.group(1) + m.group(2).split('/')[-1].rsplit('.', 1)[0] + '.png}', t)
        t = re.sub(r'\\metadata\[[^]]*\]\{[^}]*\}', '', t)
        t = re.sub(r'\\microtypesetup\{[^}]*\}', '', t)
        t = re.sub(r'\\bibliographystyle\{[^}]*\}', '', t)
        t = re.sub(r'\\bibliography\{([^}]*)\}', lambda m: r'\input{%s.bbl}' % m.group(1), t)
        t = t.replace(r'\beginappendix', r'\section*{Appendix}')
        if t != orig:
            f.write_text(t)
            changed.append(f.relative_to(build))
    # a .bbl named after the main file is what \bibliography{references} needs
    for bbl in build.rglob('*.bbl'):
        for stem in {p.stem for p in build.rglob('*.bib')} | {'references'}:
            tgt = bbl.parent / f'{stem}.bbl'
            if not tgt.exists():
                shutil.copy(bbl, tgt)
    print(f"prepped {build} — modified {len(changed)} tex files")
    for c in changed:
        print("   ", c)
    mains = [f for f in build.glob('*.tex') if r'\documentclass' in f.read_text(errors='replace')]
    print("main file(s):", [str(m.name) for m in mains])


def norm(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'\\[a-zA-Z]+\*?(\[[^]]*\])?', ' ', s)
    s = re.sub(r'[{}$\\|]', ' ', s)
    return ' '.join(s.split()).lower()[:45]


def relabel(htmlfile, texfiles):
    h = pathlib.Path(htmlfile).read_text()
    labs = []
    tex = ''.join(pathlib.Path(f).read_text(errors='replace') for f in texfiles)
    for m in re.finditer(r'\\begin\{table\*?\}(.*?)\\end\{table\*?\}', tex, re.S):
        blk = m.group(1)
        lab = re.search(r'\\label\{(tab:[^}]+)\}', blk)
        cap = re.search(r'\\caption\{', blk)
        if not (lab and cap):
            continue
        text, _ = brace_match(blk, cap.end() - 1)
        labs.append((lab.group(1), norm(text)))

    caps = [(m.start(), norm(m.group(1))) for m in re.finditer(r'<caption>(.*?)</caption>', h, re.S)]
    assign, used, j = [], set(), 0
    for pos, cap in caps:
        best = next((k for k in range(j, len(labs))
                     if difflib.SequenceMatcher(None, cap, labs[k][1]).ratio() > 0.75), None)
        if best is None:
            best = next((k for k, (lb, lc) in enumerate(labs)
                         if lb not in used and difflib.SequenceMatcher(None, cap, lc).ratio() > 0.75), None)
        if best is not None:
            assign.append((pos, labs[best][0]))
            used.add(labs[best][0])
            j = best + 1
    for pos, lab in reversed(assign):
        ts = h.rfind('<table', 0, pos)
        if ts == -1 or 'id=' in h[ts:h.find('>', ts)]:
            continue
        h = h[:ts + 6] + f' id="{lab}"' + h[ts + 6:]
    pathlib.Path(htmlfile).write_text(h)
    ids = set(re.findall(r'id="([^"]+)"', h))
    broken = sorted(set(re.findall(r'href="#([^"]+)"', h)) - ids)
    print(f"labelled {len(assign)}/{len(caps)} tables; broken anchors: {len(broken)} {broken[:8]}")


if __name__ == '__main__':
    if sys.argv[1] == 'prep':
        prep(sys.argv[2], sys.argv[3])
    else:
        relabel(sys.argv[2], sys.argv[3:])
