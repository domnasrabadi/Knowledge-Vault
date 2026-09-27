# Route: PDFs

A single PDF (a paper, an article, a short report) goes into Reader through the
API as clean HTML, after the user confirms. **A PDF book, or several PDFs to be
combined, takes `route-epub-build.md`**, since one API document has no chapters.

Before extracting, look for a better source. PDF is the worst input there is:
LaTeX > DOCX > HTML > PDF.

- A research paper → search arXiv by title. If it's there, take the **arXiv route**.
- A gov or institutional report → the landing page usually links a `.docx` next to
  the PDF: `grep -oE 'href="[^"]*\.(pdf|docx)"' page.html`. Take the Word route.

## The flow

```bash
S="/Users/domnasrabadi/Knowledge Vault/.claude/skills/reader-ingest/scripts"
cd "$BUILD"
uv run --with pymupdf4llm python "$S/pdf_extract.py" paper.pdf paper.md
#   READ paper.md and fix it by hand (below)
pandoc paper.md -f markdown -t html5 --mathjax --wrap=none -o body.html
python3 "$S/html_for_api.py" body.html meta.json page-api.html
python3 "$S/reader_api.py" check "<pdf url>" --title "<title>"
#   AskUserQuestion — then:
python3 "$S/reader_api.py" save page-api.html meta.json [--fresh-url]
```

`--mathjax` makes pandoc emit `\(…\)`, which `html_for_api.py` turns into `$…$`.
Formulas extracted from a PDF text layer are Unicode fragments, not TeX, so check
every one (see below).

## Read the markdown; the script cannot fix these

- **Two-column PDFs scramble reading order.** Sections reorder across column
  breaks and paragraphs split in half. `pdf_extract.py` flags out-of-order
  section numbers; the prose has to be fixed by hand.
- **Strip the title and author block** from the body once it's in `meta.json`.
- **Line-end hyphens: check which kind before joining.** In one 316-page build all
  51 were real compounds (`customer-support`, `τ-bench`), not soft hyphenation.
- **Accents split into separate glyphs** (`Kele¸s`). `pdf_extract.py` repairs the
  common ones; check names.
- **Display formulas fragment into 2-D pieces** that cannot be put back into a line
  of text. Find them (short lines dense in `𝑥`-style mathematical alphanumerics),
  render the page region to PNG, read it, and write the TeX by hand as `$$…$$`.
  One 316-page build had only 9, so this is tractable.
- **Long runs of mathematical alphanumerics in prose** (`5𝑝𝑒𝑟𝑚𝑖𝑙𝑙𝑖𝑜𝑛`) can be an
  *upstream* bug: unescaped `$` signs on the source site. Reconstruct the text
  and tell the user the bug is in the source, not the conversion.
- **Code clipped at the page margin is gone for good.** Detect it, annotate the
  listing, offer to re-fetch from the live source. Never ship silently broken code.
- **PDFs exported from a dev server carry dead `127.0.0.1` links** that still
  parse as links. Inventory every `href` early and remap them.
- **Per-buyer watermarks are in the text layer** (`Licensed to <email>` on every
  page). Strip them from the body.

`gotchas.md` §2 has the full PDF catalogue: ligature boxes, baseline tolerance,
fonts that silently delete maths, merged footnote markers.

## meta.json and the URL

`title`, `authors`, `date`, `description` as usual. The API requires a `url`:

- Use the PDF's real web address if it has one. Highlights then link back to it.
- For a local file with no web address, use `https://reader-ingest.invalid/<slug>`.
  The `.invalid` domain is reserved and never resolves, so it's an honest
  placeholder. Tell the user that highlights on this document won't link to a
  source. (Not yet tested against the live API; if Reader rejects it, report the
  error and ask for a real URL.)
- A PDF the user uploaded to Reader before has no matching URL. Find it with
  `check --title`.

Images: see "Images: classify before you decide" in `route-web.md`. It applies here.
