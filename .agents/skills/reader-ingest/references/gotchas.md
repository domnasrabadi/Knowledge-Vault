# Gotchas: everything that has bitten us

Every entry here destroyed or corrupted content in a real run, and **almost none
of them errored**. That is the through-line: the toolchains in this pipeline fail
silently. Assume every stage lost something until you have counted.

Sources: the Hamel article build, the six-PDF AI Evals Field Guide build, and the
audits of five commercial EPUBs (O'Reilly ×3, Manning ×2).

---

## 0. The three rules that generate all the others

1. **Count in, count out.** Words, headings, paragraphs, tables, figures, code
   blocks, footnotes. A ratio you cannot explain is content you lost. On the
   field guide the final accounting was 72,057 source words → 59,631 output, and
   every one of the 12,426 missing words was traced to a deliberate removal
   (8,026 merged-technique prose, 2,036 duplicate footnote lists, 2,439 covers
   and landing pages). Do not ship until the difference is fully explained.
2. **Reduce to a minimal case before fixing.** On the Hamel build the first two
   TOC fixes were both wrong, and one of them *introduced* duplicate IDs. The
   thing that actually found the bug was a three-line test document. Piling
   fixes on a misdiagnosis costs more than the diagnosis would have.
3. **Verify the thing you shipped, not the thing you built.** Extraction can be
   perfect and the EPUB still broken (entities, anchors, manifest). Always
   re-open the final `.epub`.

---

## 1. Source acquisition

- **`curl -L -A "Mozilla/5.0 ..."`, not WebFetch.** WebFetch returns prose, not
  markup, and times out on large pages. You need the DOM.
- **Look for a better source before settling.** LaTeX > DOCX > HTML > PDF.
  Gov/institutional reports usually link a `.docx` next to the PDF; a
  publisher-only paper is often on arXiv by title — and an arXiv paper takes
  the **arXiv route** (`route-arxiv.md`), which builds from its LaTeX source.
- **PDFs exported from a dev server carry dead links.** The field guide PDFs were
  generated from `127.0.0.1:<port>`, so **all 715 internal links were broken**.
  They still parse as links, so nothing complains. Inventory every `href` early
  and decide the remap policy: in-scope → internal anchors, out-of-scope → the
  live site. (Final split: ~250 internal, 413 glossary + 52 unexported sections.)
- **Check the page count before you trust the brief.** The "4 PDFs" zip had six.
- **Per-buyer watermarks are in the text layer.** 316 `Licensed to <email>`
  footers, one per page. Strip from the body, keep one attribution note.

---

## 2. PDF extraction (PyMuPDF)

This is where the most damage happens and where it is hardest to see.

### Ligatures have zero-width bounding boxes
`fi` and `ft` ligature components report identical or zero-width x-boxes:

```
'f' x0=295.00 x1=302.19
'i' x0=302.19 x1=302.19   <- zero width
'f' x0=302.50 x1=310.08
't' x0=310.08 x1=310.08   <- zero width
```

Sorting **characters** by x therefore scrambles the word: `fifteen` came out as
`fifeten`. **Fix: sort spans, not characters.** Never reorder at char level.

### Inline code sits on a fractionally different baseline
A body span had `origin.y = 181.50`, the `<code>` span inside the same sentence
`181.23`. Grouping by exact baseline splits them into separate lines, and the
code run then sorts to the start:

> `idTwo properties are non-negotiable. First, the  is stable forever…`

**Fix: tolerance band on the baseline, then sort by x within the band.** Same bug
class hits super- and subscripts; they scatter to line start identically.

### Filtering fonts by subtype silently deletes maths
The role classifier keyed off `/Subtype/Type3` font objects. Every maths glyph
used a non-Type3 font, so **all formulas vanished with no error** — the sentence
just ended early. Fix: handle non-Type3 fonts too (fall back to `/BaseFont`).

### Radicals, hats and fraction bars are vector drawings, not text
They are in the page's drawing ops, never in any text extraction. A formula will
come out missing exactly the parts that made it a formula.

### Display formulas fragment into 2-D pieces that cannot be linearised
The Wilson interval extracted as ten fragments at nine different y-positions:

```
y 462.9  '√𝑝(1 −^𝑝)'
y 465.0  '^𝑧𝑧'
y 468.0  '𝑝+± 𝑧+'
y 470.2  '𝑛'      y 471.8 '2𝑛'      y 474.8 '4𝑛'
```

Three options, in order of preference:
1. **Find them all, render them to PNG, read them, and hand-write the HTML.**
   This is what we shipped. There were only **9 display-math clusters in 316
   pages** — cluster candidates with
   `re.compile(r'[\U0001D400-\U0001D7FF√]')` + short line + `x0 > 150`.
2. Inline SVG snapshot — *rejected*: `get_svg_image(text_as_path=True)` produced
   **313 KB per formula**.
3. PNG snapshot — loses scaling and theme adaptation, and is not highlightable.

### Watch for source bugs that look like extraction bugs
A chapter came out as `5𝑝𝑒𝑟𝑚𝑖𝑙𝑙𝑖𝑜𝑛𝑡𝑜𝑘𝑒𝑛𝑠…`. That was **not** our fault: the author
had unescaped `$` signs, so the *site's own* maths renderer swallowed every
dollar amount, and the PDF was generated from the broken page. Detect with
`re.compile(r'[\U0001D400-\U0001D7FF′ℎ]{8,}')` — long runs of mathematical
alphanumerics in prose. Reconstruct from context and tell the user it's upstream.

### Line-end hyphens: check which kind before joining
51 line-final hyphens in the field guide, and **every one was a real compound**
(`TRAJECT-Bench`, `customer-support`, `post-conditions`, `τ-bench`), not soft
hyphenation. Joining with a space, or de-hyphenating, both corrupt the text.
Sample before you decide; `pymupdf4llm` gets this wrong in the other direction.

### Table cells merge when you concatenate runs blindly
Adjacent cells become one cell. **Fix: only merge two runs when
`item.x0 - prev.x1 < 6`.** Same threshold logic rescues the label/value grid in
a reference-style layout.

### Adjacent footnote markers merge into one number
Superscripts `3` and `4` next to each other extract as the run `34`, producing
`href="#c34"` in a chapter with 6 citations → dead anchor. **Fix: split the digit
run greedily against the chapter's actual citation count.** Symptom to look for:
broken anchors whose numbers are concatenations of small valid ones (`#c12`,
`#c123`, `#c45`).

### Code clipped at the page margin is gone for good
**123 of 1,860 code lines (6.6%)** were truncated at the right margin because the
site's code blocks overflowed the print width when the PDF was generated. The
characters were never written to the file. Detect it, annotate each affected
listing, and offer to re-fetch from the live source. **Never ship silently broken
code.**

### Two-column PDFs scramble across column breaks
`pymupdf4llm` reliably reorders sections and splits paragraphs in half at column
boundaries. Read the markdown. The out-of-order section-number flag catches some
of it; the prose you fix by hand.

### Other PDF-layer damage
- Accents split into separate glyphs (`Kele¸s`) — needs a diacritic map.
- A duplicate footnote list (lines ending `↩`) can precede the real Citations
  section. Drop the whole preceding block, not individual lines.
- Empty callouts survive as empty blocks — filter blocks with no text.
- Diagrams get misparsed as tables, and one diagram emits several label runs —
  fuse adjacent figure blocks rather than accepting seven one-label figures.

---

## 3. Pandoc

| Failure | Fix |
|---|---|
| Raw inline `<svg>` is **discarded entirely** by the HTML reader | rasterise to PNG first, alt text built from the SVG's own `<text>` labels |
| Quarto's `<main id="quarto-document-content">` nests every heading → **1-chapter EPUB, no error** | unwrap `<main>`; strip the redundant `<section>` wrappers |
| `<section>` wrappers already own the ids — "promoting" ids onto `<h2>` creates **duplicate IDs** | don't; unwrap instead |
| Unwrapping leaves orphaned closers (1 opener, 10 closers) | count and clean both ends |
| YouTube iframe → stray `<h1>An error occurred.</h1>` polluting the TOC | replace the iframe with a plain link (iframes don't work in EPUB anyway) |
| `\section` → `<h1>`, so a paper becomes 19 flat h1s | `--shift-heading-level-by=1` |
| `\resizebox{}{}{tabular}` emits **no table at all** | unwrap in prep |
| Custom verbatim environments flatten to prose, losing every line break | remap to `verbatim` |
| `\label` inside `table` dropped → dead "see Table 4" links | relabel pass after conversion |
| `\textsc` inside math **aborts the whole conversion** | uppercase in prep |
| Custom `\abstract{}` in a class file never reaches output | inject via `meta.json` |

`--split-level` doing nothing is nearly always the nesting bug above, not a
pandoc version problem. Check `pandoc -t native` to see the real AST before
blaming the writer.

---

## 4. Web pages

- **Reader's readability strips div-only components as furniture.** Anything that
  only *looks* like a paragraph must become a real `<p>`. Run
  `web_extract.py audit` and read the output — that list *is* the list of things
  Reader will delete.
- **CSS `var(--x)` colours resolve to nothing off-site** → black-on-black charts.
  Resolve from `:root` before rasterising.
- **CSS-driven bar charts** (a `<div>` whose `width:%` *is* the bar) cannot be
  rasterised. Keep the numeric cells, drop the bars, say so.
- **Badges and labels nested inside cards** get dropped by converters that only
  read the obvious child selector. Convert innermost-outward and diff the text.
- **Tooltip/hover text is real content the reader can never reach.** Inline it.
- Full recipes: `references/route-web.md`.

---

## 5. Images and transcription

- **Check alt text first.** The Hamel article had **27 images and zero alt
  attributes** — in Reader that is 27 unlabelled pictures and every diagram's
  content locked away, unhighlightable and unsearchable.
- **Read every image before deciding anything.** Classify into: the author's own
  diagrams, third-party screenshots they are quoting, memes, title slides. The
  handling differs per class and the user's preference differs per class — this
  requires asking the user and waiting for their choice.
  Actual split: 8 transcribe / 4 cite+quote / 12 memes / 3 title slides.
- **Transcribe to real markup** — tables, lists, `<pre>` — in visually distinct
  blocks so the transcription is never mistaken for the author's prose. Eight
  diagrams became 2 tables and 54 list items of highlightable text.
- **Account for all N.** "15 dropped, 12 replaced, 0 residual image refs."
- **Flag the judgement calls.** One slide filed as a meme carried real content;
  say so rather than letting it disappear under a rule the user set.
- Third-party screenshots: short attributed quote + description, not a full
  transcription.

---

## 6. EPUB assembly

- **XHTML predefines exactly five named entities**: `amp lt gt quot apos`.
  Everything else — `&uuml;` `&eacute;` `&deg;` `&copy;` — makes the file fail
  strict XML parsing. This bit us on our own build (5 files) *and* was the main
  defect in a shipped Manning title (44 entities across 14 of 36 files).
  **Convert everything else to numeric references.**
- **`mimetype` must be the first zip entry and stored uncompressed.** Repack:
  ```
  zip -qX0 out.epub mimetype && zip -qXr9D out.epub . -x mimetype
  ```
- **Check every internal link after every rebuild.** The field guide went
  117 → 26 → 0 broken links across three fix rounds. Check three classes:
  missing files (including the stylesheet), dead `#anchors`, and back-links to
  entries that were never cited.
- **Ship both nav document and NCX.** Nav for EPUB 3, NCX for compatibility.
- Keep the HTML twin self-contained — no external requests.

---

## 7. Auditing an existing EPUB

`scripts/epub_check.py` performs this audit and `scripts/epub_fix.py` the repairs;
**`references/route-epub-check.md` is the maintained version of everything below**
— profile, benign findings, and the equation-plate remedy. This section is kept
as the narrative account of where those calibrations came from; when the two
disagree, route-epub-check.md wins.

The reference profile, from three O'Reilly titles that pass everything:

| Axis | Gold standard |
|---|---|
| EPUB version | 3.0 |
| `mimetype` first + stored | yes |
| nav doc + NCX | both |
| Broken file references | 0 |
| Dead internal anchors | 0 |
| Strict-XML parse failures | 0 |
| Non-XML named entities | 0 |
| Unmanifested / orphan files | none |
| DRM / encryption | none |
| Empty `alt` | 0% |
| alt text quality | full descriptive sentence, not a label |
| `width`/`height` on images | explicit (no layout shift) |

**Benign — do not report as defects:**
- `title_title` in an O'Reilly preface — their unfilled template placeholder for
  the code-examples URL. Present in most of their builds.
- `(for . .)` in `dc:title` — a per-buyer watermark substitution that ran with a
  blank value. Cosmetic; one `sed` on `content.opf` fixes it.
- NCX deeper than nav (243 vs 162 entries) — normal house pattern.
- EPUB 2.0 — a lower spec, not a defect. The NCX carries the TOC fine.
- Tiny 12×12 PNGs in a technical book — code-callout numbers, not junk.
- `com.apple.ibooks.display-options.xml` — "opened in Books", not identifying.

**Genuine findings worth hunting for:**
- **Per-buyer watermarks with a real name or email.** One file carried a named
  person in `dc:title`. Grep for it explicitly; this is a privacy issue, and it
  is also how you tell two copies of the same book apart.
- **Calibre residue** — `calibre_bookmarks.txt` (which can hold *someone else's*
  saved reading position), Calibre-generated SVG title pages, commented-out XML
  declarations in rewritten files.
- **Empty spine stubs.** One title's `index.html` was literally `<h1>index</h1>`
  — in the spine, so it renders as a blank page and counts toward progress.
- **Orphaned images** no page references.
- **Cover `viewBox` mismatched to the image** (720×900 vs 790×990) → letterboxing
  in the library grid.
- **Equation PNGs.** See below — this is the big one.

**Comparing two copies of the same book:** diff the file sets, grep for calibre
traces, then table per-chapter word counts and first headings side by side. That
is what makes "which is canonical" answerable in one pass.

---

## 8. Readwise Reader specifics

- **Reader reflows EPUBs into its own view and discards most publisher CSS.**
  Never make correctness depend on a stylesheet surviving. Design the fallback
  to be the thing that works.
- **Therefore: bake image fixes into the pixels.** A maths-heavy Manning title
  had 951 equation PNGs, every one opaque RGB white, **93% of them inline-sized**
  (median 36×28px) sitting mid-sentence. In dark mode the prose reads as
  *"we use ▮ to denote prompts and ▮ to denote completions"*.
  - The obvious fix — transparent background + `filter: invert()` under
    `prefers-color-scheme: dark` — is **wrong for Reader**. If the CSS is
    stripped you get transparent-background black glyphs on a dark page:
    *invisible* equations, which is worse than white boxes.
  - The right fix: strip white to true transparency (antialiased edges kept as
    alpha), remap glyphs to a mid-tone around **`#7D7D7D`** — that lands at
    **4.1:1 against both white and Reader's dark background**, so it is legible
    in light, sepia, dark and black *with no CSS at all*. Then additionally ship
    the dark-mode CSS rule as an improvement, not a dependency.
- **Check for recoverable LaTeX before any of that.** Manning generates equation
  PNGs from LaTeX and it sometimes survives in `tEXt`/`iTXt` chunks. Here it had
  been stripped, so real text was impossible. OCR over 951 maths images would
  introduce silent errors in a technical book — don't.
- **Alt text is the only textual trace an image leaves, and Reader surfaces it.**
  1,037 images all labelled `"equation image"` or `"figure"` is equivalent to no
  alt text. Where a `Figure 5.1 …` caption sits next to the image in the markup
  (45 of 46 cases), lift it into `alt`.
- **`word-break: break-all`** in a publisher stylesheet breaks identifiers
  mid-token at narrow widths. `break-word` + horizontal scroll.
- **The API cannot take a file.** It saves a URL plus HTML; `category: epub` is a
  label, not an upload. So single documents go in as HTML through the API
  (automatic, linked to their source), and anything that must be an EPUB (long
  sources, repaired publisher files) is dragged in by hand. See `reader-api.md`.

---

## 9. Verification protocol

Run all of it, on the final file, every rebuild:

1. Zip integrity; `mimetype` first and stored.
2. Every `.xhtml`/`.opf`/`.ncx` parses as **strict XML** (this is what catches
   named entities).
3. Manifest ↔ files both ways: nothing missing, nothing unmanifested.
4. Zero broken `href`/`src`; zero dead `#anchors`; zero dangling back-links.
5. nav entries and NCX navPoints both present, counts sane, depth sane.
6. No empty chapters (a file containing only its own heading = dropped content).
7. Content probes on **everything you rescued or suspect**, matched against
   tag-stripped text (inline `<code>`/`<em>` otherwise splits a phrase across
   tags and a present string reads as missing).
8. Word-count accounting against the source, with every gap explained.
9. **Look at it.** `Read` one rasterised chart to confirm it isn't blank; render
   a chapter and check light *and* dark.

---

## 10. Working-process gotchas

- **`file://` URLs do not open in the browser pane.** Serve the directory:
  `python -m http.server 8731` then navigate to `http://localhost:8731/...`.
- **A 214,000px-tall page breaks the pane.** Scrolling times out. Either render a
  single chapter, use `javascript_tool` with `scrollIntoView({block:'center'})`,
  or — best — build a **sampler page** with one of every block type at the top:
  paragraph, heading, table, code, callout, quick-reference box, figure,
  citations. One screenshot then covers the whole render surface.
- **The scratchpad is wiped between sessions.** Anything worth keeping goes into
  the skill or into `~/Downloads`, not `build/`.
- Structure a big build as separate stages — `extract` → `model` → `render` →
  `book` → `fixups`. Every bug above was fixed in exactly one of them, and that
  is only possible if they are separate files.

---

## 11. Decide these with the user before building

From the field guide, these four questions changed the entire shape of the work
and none of them had a safe default:

1. **What artefact?** EPUB + HTML twin / EPUB only / single HTML / Markdown.
2. **How to handle overlapping sources?** (Here: a reference PDF that duplicated
   five other PDFs.) Appendix / quick-reference tables only / merge into
   chapters / full inclusion.
3. **How much effort on diagrams and tables?** Real `<table>` from
   x-coordinates + captioned label blocks / hand-authored SVG / page snapshots /
   plain text.
4. **What gets stripped?** Watermarks, promo lines, per-chapter meta lines,
   section landing pages.

Then **flag the consequences you can already see**: only 7 of 13 technique pages
mapped onto existing chapters, so the other 6 needed a home — said up front, not
discovered at the end. And when a strip rule destroys something real (the landing
pages contained framing prose that appeared nowhere else), say so and offer the
original back.

---

## 12. Reporting back

The value is the diagnosis, not the file. Give:

- **Before/after counts.** "109 → 174 paragraphs." "1 chapter → 12."
- **What was actually broken**, named. "Quarto wraps everything in `<main>`, so
  pandoc read all ten `<h2>`s as nested."
- **Wrong turns worth knowing about.** The two failed TOC fixes, and that one
  introduced duplicate IDs.
- **What is still imperfect.** Clipped code lines. Text baked into images is not
  highlightable. Maths shows in Reader as `$…$` source by design (it renders in
  Obsidian); say so, so it isn't reported back as a bug.
- **Upstream bugs you found**, clearly attributed to the source.
- **The judgement calls**, with an offer to reverse each one.
