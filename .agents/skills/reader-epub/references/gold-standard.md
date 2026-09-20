# The gold-standard profile, and what is benign

What `inspect.py` measures, what a sound EPUB looks like, and — the part that
actually saves time — the list of findings that *look* like defects and are not.

Derived from three O'Reilly titles and two Manning titles that were audited in
full, plus the builds we shipped ourselves.

**Read the "benign" section before reporting anything.** Every entry there cost
a real investigation once. An audit that reports template residue as a defect
trains the user to ignore the audit.

---

## The profile

| Axis | Gold standard | Check |
|---|---|---|
| EPUB version | 3.0 | `EPUB version` |
| `mimetype` first zip entry, stored uncompressed | yes | `mimetype first + stored` |
| Strict-XML parse of every XHTML/OPF/NCX | 0 failures | `strict XML parse` |
| Non-XML named entities | 0 | `non-XML named entities` |
| Navigation | nav document **and** NCX | `nav document`, `NCX` |
| Manifest ↔ files, both directions | nothing missing, nothing unmanifested | `manifest -> files` |
| Broken `href`/`src` | 0 | `broken file references` |
| Dead internal anchors | 0 | `dead internal anchors` |
| Empty spine documents | 0 | `empty spine documents` |
| DRM / encryption | none | `DRM / encryption present` |
| Empty `alt` | 0% | `alt coverage` |
| alt text quality | a descriptive sentence, not a repeated label | `alt text is a repeated label` |
| Per-buyer watermarks | none carrying a real name or email | `watermark:` |

A title that passes all of these is sound. Two `WARN`s and no `FAIL`s is a
normal, good result.

### Verified baseline

`Agentic GraphRAG` (O'Reilly, 2026) audits as: EPUB 3.0, mimetype correct,
23/23 strict-XML, 0 entities, nav 240 entries / NCX 411 navPoints, 0 broken
references, 0 dead anchors, 0 empty spine documents, 126,405 words across 20
documents, 26/26 images with alt. Use it as the reference run when changing
`inspect.py` — if a change makes this file report a `FAIL`, the change is wrong.

---

## Benign — do not report these as defects

- **`title_title`** in an O'Reilly preface. Their unfilled template placeholder
  for the code-examples URL. Present in most of their builds.
- **`(for . .)` in `dc:title`.** A per-buyer watermark substitution that ran with
  a blank value. Cosmetic; one `sed` on `content.opf` fixes it if it bothers you.
- **NCX deeper than the nav document** (411 navPoints at depth 5 vs 240 entries
  at depth 3, above). Normal house pattern — the NCX carries the finer-grained
  TOC. Not a mismatch.
- **EPUB 2.0.** A lower spec, not a defect. The NCX carries the TOC fine.
- **Tiny 12×12 PNGs in a technical book.** Code-callout numbers, not junk.
- **`com.apple.ibooks.display-options.xml`.** Says "was opened in Apple Books",
  not who opened it.
- **Publisher role addresses** — `support@oreilly.com`, `permissions@…`,
  `bookquestions@…`. These ship in every copy. `inspect.py` filters them, and
  the filter is why a real named-purchaser hit is worth acting on.
- **No explicit `width`/`height` on images.** The original profile listed this as
  a gold-standard axis, but the verified O'Reilly baseline above has **0 of 26**
  sized inline — they size via CSS. Treat the `WARN` as information about layout
  shift in Reader, not as evidence the file is badly made.

---

## Genuine findings worth hunting for

- **Per-buyer watermarks with a real name or email.** One audited file carried a
  named person in `dc:title`. This is a privacy issue, and it is also how you
  answer "are these two files the same copy?". Graded `PII`, never suppressed.
- **Calibre residue.** `calibre_bookmarks.txt` can hold *someone else's* saved
  reading position. Also Calibre-generated SVG title pages and commented-out XML
  declarations in rewritten files.
- **Empty spine stubs.** One title's `index.html` was literally `<h1>index</h1>`
  — in the spine, so it renders as a blank page and counts toward reading
  progress.
- **Orphaned images** that no document references.
- **Cover `viewBox` mismatched to the image** (720×900 against a 790×990 file)
  → letterboxing in the library grid.
- **Non-XML named entities.** `&uuml;` `&eacute;` `&deg;` — 44 across 14 of 36
  files in a shipped Manning title. Bit our own build too. Numeric references
  are the fix.
- **Inline-sized opaque equation PNGs.** The big one — see below.

---

## Equation plates and the `#7D7D7D` rule

A maths-heavy Manning title carried **951 equation PNGs, 93% of them
inline-sized** (median 36×28px) sitting mid-sentence, every one opaque RGB
white. `inspect.py` flags this as `inline-sized image plates` by sampling PNG
headers for colour type 0/2 (no alpha channel).

Why it matters: **Reader reflows EPUBs into its own view and discards most
publisher CSS.** In dark mode the prose reads as

> we use ▮ to denote prompts and ▮ to denote completions

The obvious fix — transparent background plus `filter: invert()` under
`prefers-color-scheme: dark` — is **wrong for Reader**. If the CSS is stripped
you get transparent-background black glyphs on a dark page: *invisible*
equations, which is worse than white boxes.

The right fix, in order:

1. **Check for recoverable LaTeX first.** Manning generates these from LaTeX and
   it sometimes survives in the PNG's `tEXt`/`iTXt` chunks. Real text beats any
   image treatment. Do **not** fall back to OCR on a technical book — it
   introduces silent errors in exactly the content that can least afford them.
2. **Otherwise bake the fix into the pixels.** Strip white to true transparency,
   keeping antialiased edges as alpha, and remap glyphs to a mid-tone around
   **`#7D7D7D`**. That lands at **4.1:1 against both white and Reader's dark
   background**, so it is legible in light, sepia, dark and black *with no CSS
   at all*.
3. **Then** ship the dark-mode CSS rule as an improvement, never as a dependency.

That reasoning generalises: anything you would otherwise fix in a stylesheet has
to survive the stylesheet being thrown away.

---

## Comparing two copies of the same title

`inspect.py compare a.epub b.epub` does the pass that made this answerable:

1. Audit both, so blocking/degrading/watermark counts sit side by side.
2. Diff the file sets — Calibre residue and added title pages show up here.
3. Table per-chapter word counts and first headings, flagging any chapter whose
   lengths differ by more than 2%.

A copy with fewer blocking findings, no Calibre residue and no named watermark
is the one to keep. If word counts differ materially in a chapter, read that
chapter in both before deciding — one of them lost content.
