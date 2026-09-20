#!/usr/bin/env python3
"""Extract a PDF to markdown with layout awareness, then clean the usual damage.

    pdf_extract.py paper.pdf out.md [--no-clean]

Run with: uv run --with pymupdf4llm python pdf_extract.py ...

Handles multi-column reading order and reconstructs tables as markdown pipe
tables (a large win over Reader's own PDF handling). The cleanup pass removes
running headers, repairs de-hyphenation damage and rebuilds broken diacritics.

ALWAYS read the output afterwards. Two-column PDFs routinely scramble section
order across a column break and split a paragraph in half — that needs a human
(or model) eye and a manual reorder; no heuristic catches it reliably.
"""
import re, sys, pathlib

# PDF text layers encode accents as separate glyphs; these are what survives extraction
DIACRITICS = [('¸s', 'ş'), ('¸S', 'Ş'), ('¸c', 'ç'), ('¸C', 'Ç'), ('˘g', 'ğ'), ('˘G', 'Ğ'),
              ('¨o', 'ö'), ('¨u', 'ü'), ('¨a', 'ä'), ('´e', 'é'), ('`e', 'è'), ('ˇc', 'č'),
              ('˜n', 'ñ'), ('´o', 'ó'), ('´a', 'á'), ('∆', 'Δ')]

# words broken across a line/column break lose their real hyphen
REJOIN = [('LLMas-a-judge', 'LLM-as-a-judge'), ('LLM-asa-judge', 'LLM-as-a-judge'),
          ('userreported', 'user-reported'), ('humanreported', 'human-reported'),
          ('thumbsup', 'thumbs-up'), ('thumbsdown', 'thumbs-down')]


def clean(t, venue_pat=None):
    for a, b in DIACRITICS + REJOIN:
        t = t.replace(a, b)
    # running headers / footers: the venue line and bare page numbers
    if venue_pat:
        t = re.sub(rf'^.*{venue_pat}.*$', '', t, flags=re.M | re.I)
    t = re.sub(r'^_?Proceedings of .*$', '', t, flags=re.M)
    t = re.sub(r'^\s*\d{1,4}\s*$', '', t, flags=re.M)
    # markdown headings arrive as "## **1 Intro**" — the bold is redundant
    t = re.sub(r'^(#{1,6})\s*\*\*(.+?)\*\*\s*$', r'\1 \2', t, flags=re.M)
    # hyphen left dangling mid-word by a column break
    t = re.sub(r'([a-z])- ([a-z])', r'\1-\2', t)
    return re.sub(r'\n{3,}', '\n\n', t)


def report(t):
    print("--- headings")
    for m in re.finditer(r'^#{1,6} .*$', t, re.M):
        print("   ", m.group(0)[:78])
    print(f"--- tables: {len(re.findall(r'^\|---', t, re.M))}  "
          f"| figures: {len(re.findall(r'!\[', t))}  | chars: {len(t)}")
    nums = [int(n) for n in re.findall(r'^#{1,6} (\d+)[ .]', t, re.M)]
    if nums != sorted(nums):
        print("!!! section numbers OUT OF ORDER:", nums)
        print("    two-column reading order is scrambled — reorder manually and")
        print("    check for a paragraph split across the break")


def main():
    import pymupdf4llm
    pdf, out = sys.argv[1], sys.argv[2]
    md = pymupdf4llm.to_markdown(pdf)
    if '--no-clean' not in sys.argv:
        md = clean(md)
    pathlib.Path(out).write_text(md)
    print(f"wrote {out}")
    report(md)


if __name__ == '__main__':
    main()
