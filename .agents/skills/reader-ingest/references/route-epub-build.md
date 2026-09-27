# Route: building an EPUB (long sources)

For anything too long or chapter-shaped for one API document: a PDF book,
several PDFs combined into one, a long multi-part report, a web book. The
output is an `.epub` (plus a standalone HTML copy for previewing) that the
**user drags into Reader** (Add → drop the file, or press `U`). The API can't
take a file.

Single articles, papers and short reports go through the API instead
(`route-web.md`, `route-pdf.md`, `route-docx-latex.md`).

## Decide these with the user first

In the six-PDF field-guide build, these four questions changed the whole shape of
the work, and none had a safe default. Ask the user and wait for their answers:

1. **What artefact?** EPUB + HTML copy (default) / EPUB only / Markdown.
2. **How to handle overlapping sources?** (There, a reference PDF duplicated five
   others.) Appendix / quick-reference tables only / merge into chapters / include everything.
3. **How much effort on diagrams and tables?** Real `<table>` rebuilt from
   x-coordinates / hand-authored SVG / page snapshots / plain text.
4. **What gets stripped?** Watermarks, promo lines, per-chapter meta lines,
   section landing pages.

Then **flag the consequences you can already see.** Only 7 of 13 technique pages
mapped onto existing chapters, so the other 6 needed a home. Say that up front,
not at the end. When a strip rule destroys something real (the landing pages held
framing prose found nowhere else), say so and offer the original back.

## Build

```bash
S="/Users/domnasrabadi/Knowledge Vault/.agents/skills/reader-ingest/scripts"
cd "$BUILD"
#   extract each source with its route's tools → one body.html with <h2> chapters
python3 "$S/build.py" body.html meta.json "<Book Title>" [--cover cover.jpg]
python3 "$S/verify.py" "<Book Title>.epub" --probe "text you rescued" --probe "..."
python3 "$S/epub_check.py" "<Book Title>.epub" --spine
cp "<Book Title>.epub" "<Book Title>.html" ~/Downloads/
```

- `build.py` splits chapters at `<h2>` (`--split-level=2`), fills gaps in the
  heading levels so the table of contents nests properly, embeds images, and
  writes maths as `$…$` like every other route. It also turns `<embed>` into
  `<img>`, because pandoc's EPUB writer silently drops `<embed>`, figure and all.
- `verify.py` checks your own build: nothing empty, images packaged, probes found.
- `epub_check.py` then checks the file you're about to hand over, as any
  third-party EPUB would be checked. Extraction can be perfect and the EPUB still
  broken (entities, anchors, manifest). Always inspect the shipped file.

`meta.json`: `title`, `authors[]`, `date`, `venue`, `url`, `description`,
`abstract?`, `subtitle?`.

## Combining several sources

1. **Check the file count before trusting the brief.** The "four PDFs" zip had six.
2. **Probe font-size stratification** across the sources to derive heading levels
   from the data. Don't assume the visual hierarchy matches the meaning.
3. **Separate the stages into separate files**: `extract` → `model` → `render`
   → `book` → `fixups`. Every bug in that build was fixed in exactly one stage,
   and that is only possible when they are separate. The scratchpad is wiped
   between sessions, so anything worth keeping goes into this skill or `~/Downloads`.
4. **Decide the cross-reference remap in one pass.** In-scope targets become
   internal anchors; out-of-scope ones point at the live site. One build had 715
   internal links, all dead (a dev-server origin).
5. **Account for every word.** 72,057 source words became 59,631 output, and all
   12,426 missing words were traced to deliberate removals. Don't ship until the
   gap is fully explained.

## Look at it

`file://` URLs don't open in the browser pane, so serve the folder with
`python3 -m http.server 8731`. A 214,000px-tall page breaks the pane. Build a
**sampler page** with one of every block type at the top (paragraph, heading,
table, code, callout, figure, citations), and one screenshot covers the whole
render surface. Check it in light *and* dark. `Read` one rasterised chart to
confirm it isn't blank.

## Hand-over

Tell the user the file is in `~/Downloads`, **checked and ready to drag into
Reader**, and give the counts: chapters, words in and out, tables, figures,
anything stripped. This route never uploads.
