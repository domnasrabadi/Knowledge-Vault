# Route: checking and fixing an existing EPUB

For an `.epub` the user already has: a publisher's book, a download, or one of
our own earlier builds. Output: a repaired `.epub` in `~/Downloads`, **checked and
ready for the user to drag into Reader**. This route never uploads; the API
can't take a file.

## The flow

```bash
S="/Users/domnasrabadi/Knowledge Vault/.agents/skills/reader-ingest/scripts"
python3 "$S/epub_check.py" book.epub [--spine] [--images]      # 1. what's wrong
uv run --with pillow python "$S/epub_fix.py" book.epub --equations   # 2. fix + re-check
#   -> ~/Downloads/<name> (fixed).epub
python3 "$S/epub_check.py" compare a.epub b.epub               # two copies of one title
```

`--equations` needs Pillow, hence `uv run`. Leave it off when the check found no
inline equation images, and plain `python3` then works.

**`epub_check.py`** (read-only) grades findings: **FAIL** is structurally broken,
**WARN** degrades reading in Reader, **PII** is a per-buyer watermark, and
**NOTE** is measured, not a defect. Read the benign list below before reporting
anything.

**`epub_fix.py`** never modifies the input. It fixes, counts and re-checks:

| Fix | Why |
|---|---|
| Non-XML named entities → numeric | XHTML predefines only five; the rest fail strict parsing |
| **Watermarks: always stripped** | The user's standing decision. Only what the check grades PII: `Licensed to …`, and emails that recur across 5+ documents or sit in the metadata. A one-off author contact email is left alone. `(for . .)` title residue goes too. |
| Weak alt text ← adjacent `Figure N …` caption | Reader surfaces alt text; `"figure"` ×900 is the same as none |
| `--equations`: LaTeX recovered from PNG text chunks → `$…$` | Real text beats any image treatment |
| `--equations`: inline opaque plates recoloured `#7D7D7D` on transparent | Legible in light and dark **without CSS** (see below) |
| Repack: `mimetype` first and stored | Readers reject the file otherwise |

It then prints the **word accounting**, where every changed word must be explained:
`words: 268 -> 254 (-14) = watermarks -21, recovered LaTeX +7, unexplained +0`.
A non-zero *unexplained* means something was lost; investigate before shipping.

**DRM-protected files can be checked, not fixed.** `epub_fix.py` refuses them.

Anything the fixer doesn't handle (dead anchors, broken references, missing
manifest entries, empty spine stubs) is fixed by hand. Unpack, edit, then repack
exactly like this:

```bash
mkdir out && cd out && unzip -q ../book.epub
#   … edit …
zip -qX0 ../fixed.epub mimetype && zip -qXr9D ../fixed.epub . -x mimetype
```

Re-check after every round; broken-link counts fall in rounds (117 → 26 → 0 on one build).

## Hand-over

Tell the user the fixed file is in `~/Downloads`, **checked and ready to drag into
Reader**. Give the before/after grades, what each fix changed (counts), the word
accounting, and anything left as a WARN, with why it's acceptable or what it
would take to fix.

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
`epub_check.py` or `epub_fix.py` — if a change makes this file report a `FAIL`, or makes `epub_fix.py` change a
single word of it, the change is wrong.

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
  `bookquestions@…`. These ship in every copy. `epub_check.py` filters them, and
  the filter is why a real named-purchaser hit is worth acting on.
- **A one-off personal email** — usually the author's contact address. Graded
  NOTE ("too sparse for a per-buyer stamp") and never stripped.
- **No explicit `width`/`height` on images.** The original profile listed this as
  a gold-standard axis, but the verified O'Reilly baseline above has **0 of 26**
  sized inline — they size via CSS. Treat the `WARN` as information about layout
  shift in Reader, not as evidence the file is badly made.

---

## Genuine findings worth hunting for

- **Per-buyer watermarks with a real name or email.** One audited file carried a
  named person in `dc:title`. This is a privacy issue, and it is also how you
  answer "are these two files the same copy?". Graded `PII`; `epub_fix.py` strips
  them. When comparing two copies, run the comparison **before** fixing.
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
white. `epub_check.py` flags this as `inline-sized image plates` by sampling PNG
headers for colour type 0/2 (no alpha channel).

Why it matters: **Reader reflows EPUBs into its own view and discards most
publisher CSS.** In dark mode the prose reads as

> we use ▮ to denote prompts and ▮ to denote completions

The obvious fix — transparent background plus `filter: invert()` under
`prefers-color-scheme: dark` — is **wrong for Reader**. If the CSS is stripped
you get transparent-background black glyphs on a dark page: *invisible*
equations, which is worse than white boxes.

The right fix, in order. `epub_fix.py --equations` does steps 1 and 2 for
inline-sized plates (under 60×400px), and never touches full-size figures:

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

`epub_check.py compare a.epub b.epub` does the pass that made this answerable:

1. Audit both, so blocking/degrading/watermark counts sit side by side.
2. Diff the file sets — Calibre residue and added title pages show up here.
3. Table per-chapter word counts and first headings, flagging any chapter whose
   lengths differ by more than 2%.

A copy with fewer blocking findings, no Calibre residue and no named watermark
is the one to keep. If word counts differ materially in a chapter, read that
chapter in both before deciding — one of them lost content.
