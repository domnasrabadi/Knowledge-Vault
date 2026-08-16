---
name: arxiv-to-reader
description: Render an arXiv paper from its LaTeX source into clean, richly-formatted HTML and save it straight into Readwise Reader's Later queue — fixing the bad parsing (mangled two-column text, lost headings, broken math) you get when Reader scrapes an arXiv page or PDF itself. Use whenever an arXiv link/ID should be read in Reader.
---

# arxiv-to-reader — put a properly rendered paper into Reader

Reader's own arXiv ingestion scrapes the abs page or parses the PDF. Both go wrong in familiar ways: two-column PDFs interleave into nonsense, section headings flatten, equations become garbage, code and tables lose structure. This skill sidesteps all of it by building the document from the paper's **LaTeX source** — where columns, headings, math and tables are explicit markup, not a layout to reverse-engineer — and uploading that HTML to Reader via the API.

**One command does the whole job:**

```bash
cd "/Users/domnasrabadi/Knowledge Vault/.claude/skills/arxiv-to-reader/scripts"
python3 arxiv_to_reader.py <arxiv-id-or-url>
```

Default behaviour: saves to **Later**, tagged `arxiv`. That is the intended path — don't hand-roll the steps.

## Inputs

- **Required**: an arXiv ID or URL in any form — `2606.00093`, `arxiv.org/abs/2606.00093v1`, `/pdf/` links, ar5iv/alphaxiv links, old-style `math.GT/0309136`, or a `10.48550/...` DOI. The underlying `arxiv-skill` normalises all of these.
- **Auth**: `READWISE_TOKEN` from the environment, else `~/Downloads/reader4/readwise_highlights_to_notes/.env`. Token from <https://readwise.io/access_token>.
- **Dependencies**: `pandoc` (`brew install pandoc`), plus the `arxiv` skill vendored alongside this one at `.claude/skills/arxiv/` — the script finds it automatically (override with `ARXIV_SKILL_DIR`, and it still falls back to `~/Downloads/arxiv-skill`). `pdftocairo` and `sips` are optional — used only for PDF-format figures and downscaling.

### Flags

| Flag | Effect |
| --- | --- |
| `--location new\|later\|archive\|feed` | Destination queue (default `later`) |
| `--tags a,b` | Reader tags (default `arxiv`) |
| `--dry-run` | Build the HTML, print stats, upload nothing |
| `--out PATH` | Also write the final HTML to disk (pairs well with `--dry-run`) |
| `--replace` | If the paper is already in Reader, delete and re-save it |
| `--no-images` | Skip figure embedding (use if the payload is too large) |
| `--no-refs` | Omit the generated References section |
| `--force-fetch` | Re-download the source, ignoring the cache |

## How it works

1. **Fetch** — normalises the input to a bare arXiv ID (via the `arxiv` skill's `normalize_arxiv_id`), then calls its `fetch.py`, which pins an explicit version, downloads the e-print tarball, safely extracts it, finds the entry `.tex` and recursively inlines `\input`/`\include` into one `flattened.tex`. Cached under `~/.cache/arxiv-skill/<versioned-id>/`.

   *Why normalise first:* handed a full URL, `fetch.py` caches under an **unversioned** directory and never writes `meta.json`, so metadata lookup fails. Handed a bare ID it pins the version and writes complete metadata. Don't pass raw URLs through to it.
2. **Convert** — `pandoc -f latex -t html --mathjax --wrap=none --shift-heading-level-by=1`.
3. **Post-process** — the part that makes Reader render it well:
   - **Headings shifted to `<h2>`.** Reader's HTML cleaner *deletes every `<h1>` in the body* (it treats h1 as the document title, which it stores separately). Sections sent as h1 silently vanish, leaving one undifferentiated wall of text. This is the single most important fix — never send h1s.
   - **Math delimiters** rewritten from pandoc's `\(…\)` / `\[…\]` to `$…$` / `$$…$$`, which is what Reader's LaTeX renderer expects.
   - **Citations restored.** Pandoc cannot resolve arXiv's `.bbl`, so it emits empty `<span class="citation">` tags and the prose loses every reference. The script parses `\bibitem[{Author et al.(2025)…}]{key}` entries out of the `.bbl` and substitutes readable `(Author et al., 2025)` labels inline.
   - **Figures inlined** as base64 data URIs (Reader can't see local files). PDF/EPS figures are rasterised via `pdftocairo`; oversized images are downscaled with `sips`; anything still too big is dropped rather than bloating the payload.
   - **References section** appended from the parsed bibliography.
   - **Title block** prepended: authors, a link back to the abs page, and the abstract as a blockquote (pandoc's body output omits all three).
4. **Save** — `POST https://readwise.io/api/v3/save/` with `html`, `should_clean_html: true`, and full metadata (title, authors, abstract as `summary`, `published_date`, tags, location).
5. **Verify** — re-reads the stored document via `/api/v3/list/` and prints the word count and location, confirming what Reader actually kept.

## Output

A Reader document in the chosen queue (Later by default), printed as a `read.readwise.io/read/<id>` URL, with headings, nested lists, tables, code blocks, math and figures rendered natively. Its canonical URL is the real `arxiv.org/abs/<id>`, so highlights flow into Readwise normally and it will not duplicate an existing save of that page.

Report back to the user: the paper title, the Reader URL, the verified word count, and the citation/figure counts from the run.

## Judgement calls for the model

- **Report honestly what the script printed.** If figures were dropped or citations came back as `0`, say so — don't imply a clean render.
- **`--replace` on a re-run.** A plain re-save of a URL already in Reader returns HTTP 200 and leaves the old (possibly badly-parsed) content in place. If the user wants the improved render to replace an earlier save, pass `--replace`.
- **PDF-only papers.** Older or unusual submissions have no LaTeX source; the script exits with a clear message. Don't fake it — tell the user the paper must be read as a PDF in Reader.
- **Pandoc warnings are normal.** Custom macros from a venue's `.sty` often warn without harming output. Only investigate if the final HTML is unexpectedly small or a section is missing.
- **Verifying a render.** To check what Reader really stored (as opposed to what was uploaded), fetch `GET /api/v3/list/?id=<id>&withHtmlContent=true` and grep for section titles. Reader's cleaner is the ground truth, not the local HTML.
- **After reading.** Highlights from these documents export through the normal reader4 pipeline into `00 Inbox/`; file them with the `reader4-review` skill. Papers belong in `10 Sources/Papers/`.
- **Related skill**: `arxiv-skill` (at `~/Downloads/arxiv-skill`) covers everything else about a paper — search, citation graphs, BibTeX, structured note templates. This skill only handles the Reader ingestion path.
