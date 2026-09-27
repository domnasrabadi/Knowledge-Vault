---
name: reader-ingest
description: "The single skill for getting content into Readwise Reader so it reads and highlights well. Takes an arXiv paper, web page, PDF, Word doc, LaTeX source or existing EPUB; fixes what Reader would mangle (lost headings, scrambled two-column text, dropped tables and figures, broken maths); then either uploads it to Reader through the API after the user confirms, or hands over a checked .epub for manual upload. Use whenever something should be read in Reader, whenever Reader parsed something badly or dropped content, or whenever an EPUB needs checking, fixing, de-watermarking or comparing with another copy. For searching, citing or taking notes on papers, use the arxiv skill instead."
argument-hint: "<arXiv id, url, file path or .epub> [what Reader got wrong]"
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch, AskUserQuestion
user-invocable: true
---

# reader-ingest

Content in, a clean Reader document out. The user is usually here because Reader
already accepted the source and it *read badly*. Every choice serves reading and
highlighting in Reader, and then the highlights landing well in Obsidian.

## 1. Identify the source, pick the route

| Source | Route | Ends as | Read |
|---|---|---|---|
| arXiv ID / abs, pdf, ar5iv, alphaxiv link / `10.48550` DOI | LaTeX source → HTML | **API upload** after a yes | `references/route-arxiv.md` |
| Web page | extract + rescue → HTML | **API upload** after a yes | `references/route-web.md` |
| Single PDF (paper, article, short report) | extract + hand-fix → HTML | **API upload** after a yes | `references/route-pdf.md` |
| Word doc, non-arXiv LaTeX | pandoc + fixes → HTML | **API upload** after a yes | `references/route-docx-latex.md` |
| **Long source**: PDF book, several PDFs combined, long multi-part report, web book | extract → chapters → EPUB | `.epub` in `~/Downloads`, user uploads | `references/route-epub-build.md` |
| **Existing `.epub`**: check, fix, de-watermark, compare copies | check → fix → re-check | `.epub` in `~/Downloads`, user uploads | `references/route-epub-check.md` |

Why two exits: the Reader API **cannot take a file**. It saves a URL plus HTML.
Single documents go in automatically as HTML, linked to their source URL.
Anything that needs chapters, or is already an EPUB, has to be dragged in by
the user (Reader → Add → drop the file, or press `U`).

**Look for a better source before settling.** LaTeX > Word > HTML > PDF. A paper
PDF may be on arXiv under the same title. A report's landing page often links a
`.docx` next to the PDF. When a single source is long enough that the route is
unclear, ask: one API document, or an EPUB with chapters?

Work in the session scratchpad (`$BUILD` in the route files). It is wiped between
sessions, so deliverables go to `~/Downloads`.

## 2. Rules for every route

- **Nothing reaches Reader without a yes.** Every API route runs
  build → `reader_api.py check` → **AskUserQuestion** → `reader_api.py save`.
  arXiv included. The question shows the build stats, anything flagged, and any
  existing copy of the source with its **highlight count**, offering replace /
  keep both / cancel. Deleting an old copy destroys its highlights, and it happens
  only after the new copy has verified. Full protocol: `references/reader-api.md`.
- **Maths is `$…$` / `$$…$$` literal text, everywhere.** Reader shows it as
  source. That's deliberate: highlights reach Obsidian through reader4, and
  Obsidian renders it. Never MathML, never equation images where TeX exists.
- **Real structure, not visual structure.** Headings are `<h2>`–`<h4>` in unbroken
  order (Reader deletes body `<h1>`s), prose is in `<p>`, tables stay `<table>`,
  code stays `<pre>`. Text stays text; never let content become a picture.
- **Nothing silently vanishes.** Every tool here drops content without an error.
  Count in, count out (words, headings, tables, figures, code blocks) and explain
  every gap before shipping.
- **Verify the thing you shipped.** API routes: `save` compares Reader's *stored*
  copy with what was sent. EPUB routes: `epub_check.py` on the final file.
- **Reader discards most publisher CSS.** A fix that depends on a stylesheet
  surviving isn't a fix; bake it into the markup or the pixels.
- **Reduce to a minimal case before fixing.** On one build the first two TOC fixes
  were both wrong, and one introduced duplicate IDs. A three-line test document
  found the real bug.

Before any non-trivial build, check, or debugging session, read
**`references/gotchas.md`**. It's the full catalogue of silent failures (PDF
extraction, pandoc, web pages, images, EPUB assembly, Reader itself), each with
its cause, how to detect it, and the fix.

## Scripts (`scripts/`)

| Script | Used by | Does |
|---|---|---|
| `arxiv_to_reader.py` | arXiv | LaTeX source → Reader-ready HTML + `--meta-out` |
| `web_extract.py` | web | `audit` what Reader would strip; `body` extract + rescue + KaTeX/MathJax → `$…$` |
| `pdf_extract.py` | PDF, EPUB build | PDF → markdown, diacritics, running headers, section-order flag |
| `latex_prep.py` | non-arXiv LaTeX | pre-pandoc fixes; `relabel` table ids after |
| `rasterize.py` | web, LaTeX | SVG charts / PDF figures → PNG, colours resolved, alt from labels |
| `html_for_api.py` | web, PDF, Word, LaTeX | body → upload-ready HTML (no h1, `$…$`, `<img>`, embedded images) + stats |
| `reader_api.py` | all API routes | `check` existing copy + highlights, `save` + verify, `delete` safely |
| `build.py` | EPUB build | body → `.epub` + standalone HTML |
| `verify.py` | EPUB build | your own build: structure, images, content probes |
| `epub_check.py` | both EPUB routes | check any EPUB; `compare` two copies |
| `epub_fix.py` | EPUB check | entities, watermarks, alt text, equations, repack, word accounting |

Python deps come via `uv run --with …` as each route shows; `pandoc` is required,
`pdflatex` optional (arXiv dense tables).

## Reporting back

The value is the diagnosis, not the file.

- **Where it went**: the Reader URL and verified word count, or the `.epub` path
  with "checked and ready to drag into Reader".
- **Before and after counts**: "109 → 174 paragraphs", "1 chapter → 12",
  "words: 268 → 254 = watermarks −21, recovered LaTeX +7, unexplained 0".
- **What was actually broken**, named, and **wrong turns** worth knowing about.
- **What is still imperfect**: clipped code, text inside images, maths
  shown as `$…$` source in Reader (by design).
- **Upstream bugs**, attributed to the source rather than the conversion.
- **The judgement calls**, each with an offer to reverse it.

## Related skills

- **`arxiv`**: finding, citing and taking notes on papers (search, Semantic
  Scholar, BibTeX, note templates). This skill borrows its download script
  (`fetch.py`) for the arXiv route and otherwise leaves research to it.
- **`reader4-review`**: after reading. Highlights export into `00 Inbox/`, where
  that skill files them.
