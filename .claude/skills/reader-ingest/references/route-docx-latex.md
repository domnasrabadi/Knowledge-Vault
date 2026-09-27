# Route: Word documents and non-arXiv LaTeX

Both go into Reader through the API as clean HTML, after the user confirms.
A long, chapter-shaped document takes `route-epub-build.md` instead. For
**arXiv** LaTeX, always take the arXiv route: `arxiv_to_reader.py` is far more
battle-tested than anything here.

## Word (.docx)

```bash
S="/Users/domnasrabadi/Knowledge Vault/.claude/skills/reader-ingest/scripts"
cd "$BUILD"
pandoc report.docx -f docx+styles -t html5 --mathjax --extract-media=media -s --wrap=none -o out.html
#   fix the styles (below), save the body as body.html
python3 "$S/html_for_api.py" body.html meta.json page-api.html
python3 "$S/reader_api.py" check "<url>" --title "<title>"
#   AskUserQuestion — then:
python3 "$S/reader_api.py" save page-api.html meta.json [--fresh-url]
```

`--extract-media` writes images to disk, and `html_for_api.py` embeds them.
`--mathjax` gives `\(…\)`, which becomes `$…$`.

**Word's custom styles carry no meaning.** `<span data-custom-style="Strong">`
renders as flat text. Convert `Strong` → `<strong>`, `Emphasis` → `<em>` and code
styles → `<code>`; drop empty marker spans; unwrap the rest. Then:

- Rebuild any static table of contents as a list and **strip its stale page numbers**.
- Give the footnotes section a real heading.
- Pandoc emits `<embed>` for some images. `html_for_api.py` converts them, and so
  does `build.py`, because both Reader and pandoc's own EPUB writer drop `<embed>`.

The URL: the document's web address if it came from one; otherwise follow the
placeholder rule in `route-pdf.md`.

## Non-arXiv LaTeX

```bash
python3 "$S/latex_prep.py" prep src/ build/
uv run --with pymupdf --with pillow python "$S/rasterize.py" pdfs src/ build/
cd build && pandoc main.tex -f latex -t html5 --standalone --wrap=none --mathjax \
    --shift-heading-level-by=1 -o out.html
python3 "$S/latex_prep.py" relabel out.html sections/*.tex     # in document order
python3 "$S/html_for_api.py" out.html ../meta.json ../page-api.html
```

What `latex_prep.py` prevents, all of which fail silently:

| pandoc does this | prep does this |
|---|---|
| `\resizebox{}{}{tabular}` emits **no table at all** | unwraps it |
| custom verbatim environments flatten to prose, losing every line break | remaps to `verbatim` |
| `\textsc` inside maths aborts the whole conversion | uppercases it |
| `\label` inside `table` is dropped → dead "see Table 4" links | `relabel` reattaches ids by caption |
| `\bibliography{x}` resolves nothing without bibtex | inputs the `.bbl` |

`--shift-heading-level-by=1` matters: pandoc maps `\section` to `<h1>`, giving
a paper 19 flat h1s. A custom `\abstract{}` in a class file never reaches the
output, so put it in `meta.json` as `abstract`.

**When a LaTeX build is hard**, borrow from `arxiv_to_reader.py`, which solved
harder cases. It has comment-aware scale-box unwrapping (a *commented-out*
`% \resizebox{` once spliced out a live brace), `.bbl`-or-`.bib` citation
recovery, dense tables rendered to images by real `pdflatex`, and automatic
preamble repair. `route-arxiv.md` documents each one.
