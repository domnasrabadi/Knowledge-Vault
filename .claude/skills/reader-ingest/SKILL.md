---
name: reader-epub
description: "Build, audit or repair an EPUB for Readwise Reader. Use when the user shares a URL, PDF, DOCX or LaTeX source and wants it readable and highlightable in Reader; when Reader parsed something badly, dropped sections or a PDF reads poorly; when they want an existing EPUB checked for defects, watermarks or dark-mode problems; when choosing between two copies of the same book; or when an EPUB needs remediating before reading. For arXiv papers use the arxiv-to-reader skill instead."
argument-hint: "<url, file path or .epub> [notes about what Reader got wrong]"
allowed-tools: Bash, Read, Write, Edit, WebFetch, WebSearch
user-invocable: true
---

# Reader-ready EPUB

One quality bar, three verbs:

| Verb | Input | Output |
|---|---|---|
| **build** | URL, PDF, DOCX, LaTeX | EPUB + standalone HTML twin |
| **audit** | an existing `.epub` | a graded findings report |
| **remediate** | an existing `.epub` + findings | a repaired `.epub` |

The user uploads the result manually: Reader → Add → drag the file in, or
press `U`.

**EPUB is the deliverable.** Reader documents PDF, EPUB, Markdown and OPML as
upload formats — HTML upload usually works but is undocumented, so ship EPUB as
the primary and HTML as the fallback/preview.

**arXiv papers do not belong here.** The `arxiv-to-reader` skill builds from
LaTeX source and uploads via the Readwise API in one command — a better path
than anything below. Use this skill for arXiv only if the user specifically
wants an `.epub` file rather than a document in their queue.

## Prime directive

Reader already accepts the source; the user is here because it *read badly*.
Every choice serves reading and highlighting:

- **Real structure, not visual structure.** Headings must be `<h1>`–`<h4>` in
  unbroken order, prose must be in `<p>`. Anything that only *looks* like a
  heading or paragraph gets stripped.
- **Text stays text.** Tables stay `<table>`, code stays `<pre>`, emphasis stays
  `<em>`/`<strong>`. Never let real content become a picture.
- **Nothing silently vanishes.** Every stage of every toolchain here drops
  content without erroring. Verification is not optional.
- **Reader discards most publisher CSS.** Never make correctness depend on a
  stylesheet surviving. Where you cannot, bake the fix into the pixels.
- **Reduce to a minimal case before fixing.** On a real build the first two TOC
  fixes were both wrong and one *introduced* duplicate IDs. A three-line test
  document found the bug that two rounds of patching had missed.

---

# Verb: build

1. **Get the source.** Prefer the most structured form available, in this order:
   LaTeX source > DOCX > HTML > PDF. Check for a better source before settling:
   - Gov/institutional reports: the landing page usually links a `.docx` next to
     the PDF — `grep -oE 'href="[^"]*\.(pdf|docx)"' page.html`.
   - A paper only on a publisher site: search arXiv by title, then hand it to
     `arxiv-to-reader`.
   - Use `curl -L -A "Mozilla/5.0 ..."` — WebFetch times out on large pages and
     gives you prose, not markup.
2. **Convert** by source type (below), producing a body-HTML fragment.
3. **Audit before building.** Ask what this specific toolchain drops. Compare
   counts against the original: headings, tables, figures, paragraphs.
4. **Build:** `scripts/build.py body.html meta.json <basename> [--cover cover.jpg]`
5. **Verify:** `scripts/verify.py <basename>.epub --probe "..."` — always, with
   probes drawn from content you know was at risk. Fix and rebuild until clean.
6. **Inspect the shipped file:** `scripts/inspect.py <basename>.epub`. Extraction
   can be perfect and the EPUB still broken — entities, anchors, manifest.
7. **Deliver** to `~/Downloads/` and report what was broken and what you fixed.

`meta.json`: `title, authors[], date, venue, url, description, abstract?, subtitle?`

## By source type

### Web page
Save the page and its stylesheet, then:
```
uv run --with beautifulsoup4 --with lxml python scripts/web_extract.py audit page.html
uv run --with beautifulsoup4 --with lxml python scripts/web_extract.py body page.html body.html
```
The audit lists text with no `<p>` around it — exactly what Reader strips. Read it.
Substantial entries need purpose-written transforms; see `references/web-recipes.md`.
Inline `<svg>` charts must be rasterised (`scripts/rasterize.py svgs`) and swapped
to `<img>` — **pandoc's HTML reader discards raw SVG entirely.**

### PDF (no better source)
```
uv run --with pymupdf4llm python scripts/pdf_extract.py paper.pdf paper.md
```
Then **read the markdown**. Two-column PDFs reliably scramble section order across
column breaks and split paragraphs in half; the script flags out-of-order section
numbers but you must fix the prose by hand. Strip the title/author block from the
body once it's in `meta.json`. Then `pandoc paper.md -f markdown -t html5 -s -o body.html`.

PDFs exported from a dev server carry dead `127.0.0.1` links that still parse as
links, so nothing complains — inventory every `href` early. Code clipped at the
page margin is gone for good; detect it, annotate the listing, and offer to
re-fetch from the live source rather than shipping silently broken code.

### DOCX
```
pandoc report.docx -f docx+styles -t html5 --embed-resources -s --wrap=none -o out.html
```
Word's custom styles carry no semantics: `<span data-custom-style="Strong">` renders
as flat text. Convert `Strong`→`<strong>`, `Emphasis`→`<em>`, code styles→`<code>`;
drop empty marker spans; unwrap the rest. Rebuild any static TOC as `<nav><ul>` and
strip its stale page numbers. Give the footnotes section a real heading.

### Non-arXiv LaTeX
```
scripts/latex_prep.py prep src/ build/
uv run --with pymupdf --with pillow python scripts/rasterize.py pdfs src/ build/
cd build && pandoc main.tex -f latex -t html5 --standalone --wrap=none --mathml \
    --shift-heading-level-by=1 -o out.html
scripts/latex_prep.py relabel out.html sections/*.tex     # in document order
```
`--shift-heading-level-by=1` matters: pandoc maps `\section` to `<h1>`, giving a
document with 19 h1s and no hierarchy. Figures commented out in the source are not
in the published paper — don't chase them.

## Composing many sources into one book

Different shape from the single-document recipes, and it earned its own section
after a six-PDF build. Before writing any extractor:

1. **Probe font-size stratification** across the sources to derive heading levels
   empirically. Do not assume the visual hierarchy matches the semantic one.
2. **Separate the stages into separate files** — `extract` → `model` → `render`
   → `book` → `fixups`. Every bug in that build was fixed in exactly one stage,
   and that is only possible if they are separate.
3. **Decide the merge policy with the user up front** and name the orphans.
   In that build only 7 of 13 technique pages mapped onto existing chapters; the
   other 6 needed a home. Said at the start, not discovered at the end.
4. **Check the page count before trusting the brief.** The "four PDFs" zip had six.

Then decide the cross-reference remap policy in one pass: in-scope targets become
internal anchors, out-of-scope ones point at the live site.

## Images: classify before you decide

`AskUserQuestion` territory, not a judgement call — the right handling differs
per class, and so does the user's preference.

1. **Check alt text first.** One article had 27 images and zero `alt` attributes:
   in Reader that is 27 unlabelled pictures with their content unhighlightable
   and unsearchable.
2. **Read every image**, then classify: the author's own diagrams / third-party
   screenshots they are quoting / memes / title slides. One real split was
   8 transcribe, 4 cite-and-quote, 12 memes, 3 title slides.
3. **Transcribe to real markup** — tables, lists, `<pre>` — in visually distinct
   blocks so a transcription is never mistaken for the author's prose. Eight
   diagrams became 2 tables and 54 list items of highlightable text.
4. **Third-party screenshots** get a short attributed quote plus a description,
   not a full transcription.
5. **Account for all N** in the report, and **flag the judgement calls** — one
   slide filed as a meme carried real content. Say so rather than letting it
   disappear under a rule the user set.

---

# Verb: audit

```
scripts/inspect.py book.epub [--spine] [--images] [--json]
scripts/inspect.py compare a.epub b.epub
```

Read-only, stdlib only. Where `verify.py` checks a book you just built and knows
what you meant to put in it, `inspect.py` knows nothing about the source and asks
only "is this file sound, and is it good in Reader?".

Findings are graded **FAIL** (structurally broken) / **WARN** (degrades reading
in Reader) / **PII** (a watermark carrying a real name or email) / **NOTE**
(measured, not a defect).

**Read `references/gold-standard.md` before reporting.** It holds the profile
being measured against and — more useful — the catalogue of findings that look
like defects and are not: `title_title` and `(for . .)` are O'Reilly template
residue, NCX deeper than nav is a normal house pattern, EPUB 2.0 is a lower spec
rather than a fault, publisher role addresses are in every copy. An audit that
reports those trains the user to ignore the audit.

`compare` answers "which of these two copies is canonical?" — it diffs the file
sets, surfaces Calibre residue and watermarks, and tables per-chapter word counts
side by side, flagging any chapter that differs by more than 2%.

---

# Verb: remediate

1. Unpack: `mkdir out && cd out && unzip -q ../book.epub`
2. `scripts/inspect.py ../book.epub` and fix what it graded FAIL or PII.
3. Repack — **`mimetype` must be the first entry and stored uncompressed**:
   ```
   zip -qX0 ../fixed.epub mimetype && zip -qXr9D ../fixed.epub . -x mimetype
   ```
4. `scripts/inspect.py ../fixed.epub` again. Link counts move in rounds; one
   build went 117 → 26 → 0 broken links across three passes.

**Reader discards most publisher CSS**, so the fix has to survive the stylesheet
being thrown away. For opaque inline equation plates that means stripping white
to true transparency and remapping glyphs to roughly `#7D7D7D` — 4.1:1 against
both white and Reader's dark background — rather than `filter: invert()`, which
gives *invisible* equations once the CSS is gone. Check for recoverable LaTeX in
the PNG's `tEXt`/`iTXt` chunks first; real text beats any image treatment. Do not
OCR maths in a technical book.

Where a `Figure 5.1 …` caption sits next to an image in the markup, lift it into
`alt` — Reader surfaces alt text, and it is the only textual trace an image
leaves. 1,037 images all labelled `"equation image"` is equivalent to none.

---

## Known silent-failure catalogue

Each of these destroyed content in a real run and errored on nothing. This table
is the short list — **read `references/gotchas.md` before any non-trivial build
or audit**, which has the full catalogue with causes, detection and fixes.

| Toolchain | Failure | Fix |
|---|---|---|
| pandoc html→epub | raw inline `<svg>` dropped entirely | rasterise to PNG first |
| pandoc html→epub | Quarto `<main>` wrapper nests every heading → **1-chapter EPUB** | unwrap `<main>`, don't promote ids |
| pandoc latex→html | `\resizebox{}{}{tabular}` emits **no table at all** | `latex_prep.py prep` unwraps it |
| pandoc latex→html | custom verbatim envs flatten to prose, losing all line breaks | remapped to `verbatim` |
| pandoc latex→html | `\label` inside `table` dropped → dead "see Table 4" links | `latex_prep.py relabel` |
| pandoc latex→html | `\textsc` inside math aborts the whole conversion | uppercased in prep |
| pandoc latex→html | `\section`→`h1`, destroying hierarchy | `--shift-heading-level-by=1` |
| readability (Reader) | div-only components stripped as furniture | wrap real text in `<p>` |
| web CSS | `var(--x)` colours resolve to nothing off-site → black-on-black charts | resolve from `:root` |
| pymupdf | ligature glyphs have zero-width boxes → sorting chars by x scrambles words | sort spans, never characters |
| pymupdf | filtering fonts by `/Subtype/Type3` silently deletes every formula | fall back to `/BaseFont` |
| pymupdf4llm | column-break scrambling; de-hyphenation joins real hyphens | read and fix by hand |
| pdf text layer | accents split into separate glyphs (`Kele¸s`) | `pdf_extract.py` diacritic map |
| docx | `data-custom-style` spans lose all bold/italic | remap to `<strong>`/`<em>` |
| epub assembly | XHTML predefines only `amp lt gt quot apos` | numeric references |

The lesson generalises: **after every conversion, count what came out and compare
it to what went in.** Tables, figures, headings, paragraphs, code blocks.

## Verification

`verify.py` checks your own build: zip integrity, XHTML well-formedness, a real
navigation TOC, packaged images, no empty chapters, and content probes. Pass
`--probe` for anything you rescued or suspect — especially text the user reported
missing. Probes match against tag-stripped text, because inline `<code>`/`<em>`
otherwise splits a phrase across tags and present content reads as missing.

Then `inspect.py` on the file you are about to hand over. **Look at it too**:
`Read` one rasterised chart to confirm it isn't blank, and render a chapter in
light *and* dark.

Working around the browser pane: `file://` URLs don't open — serve the directory
with `python -m http.server 8731`. A 214,000px-tall page breaks the pane, so build
a **sampler page** with one of every block type at the top (paragraph, heading,
table, code, callout, figure, citations) and one screenshot covers the whole
render surface.

## Reporting back

The value is the diagnosis, not the file:

- **Before/after counts.** "109 → 174 paragraphs." "1 chapter → 12."
- **What was actually broken**, named. "Quarto wraps everything in `<main>`, so
  pandoc read all ten `<h2>`s as nested."
- **Wrong turns worth knowing about**, including fixes that made things worse.
- **What is still imperfect.** Clipped code lines, text baked into images is not
  highlightable, MathML rendering in Reader varies.
- **Upstream bugs you found**, clearly attributed to the source rather than to
  the conversion.
- **The judgement calls**, with an offer to reverse each one.
