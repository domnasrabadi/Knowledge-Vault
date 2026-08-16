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
- **Auth**: `READWISE_TOKEN` from the environment, else `~/Downloads/reader4/.env`. Token from <https://readwise.io/access_token>.
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
| `--clean-html` | Let Reader run its readability cleaner (off by default — it deletes content) |
| `--unversioned-url` | Save under the bare abs URL instead of the versioned one |

## How it works

1. **Fetch** — normalises the input to a bare arXiv ID (via the `arxiv` skill's `normalize_arxiv_id`), then calls its `fetch.py`, which pins an explicit version, downloads the e-print tarball, safely extracts it, finds the entry `.tex` and recursively inlines `\input`/`\include` into one `flattened.tex`. Cached under `~/.cache/arxiv-skill/<versioned-id>/`.

   *Why normalise first:* handed a full URL, `fetch.py` caches under an **unversioned** directory and never writes `meta.json`, so metadata lookup fails. Handed a bare ID it pins the version and writes complete metadata. Don't pass raw URLs through to it.
2. **Convert** — `pandoc -f latex -t html --mathjax --wrap=none --shift-heading-level-by=1`.

   *Automatic preamble recovery:* papers that style themselves with `tikz`/`soul`/`pgf` define `@`-internal macros that abort pandoc's parse with `unexpected end of input`, even though the body is fine. On failure the script retries with a **sanitised preamble** — a minimal `\documentclass` plus only the author's simple one-line macros. Macros whose bodies are unparseable but that the text still *calls* (e.g. `\MET` → `\verdicttoken{…}`) get a passthrough stub `\newcommand{\name}[n]{#1}`, so the token renders as text instead of leaving a dangling command that MathJax paints red.
3. **Post-process** — the part that makes Reader render it well:
   - **Headings shifted to `<h2>`.** Reader's HTML cleaner *deletes every `<h1>` in the body* (it treats h1 as the document title, which it stores separately). Sections sent as h1 silently vanish, leaving one undifferentiated wall of text. This is the single most important fix — never send h1s.
   - **Math delimiters** rewritten from pandoc's `\(…\)` / `\[…\]` to `$…$` / `$$…$$`. **Reader displays these literally — it does not render the equations, and that is intentional.** The delimiters are preserved for downstream Obsidian, which renders `$…$` inline and `$$…$$` as blocks natively, so a highlight carried through the reader4 pipeline lands as real maths in the vault. Do **not** "fix" this by switching to MathML or pre-rendered images: that would render in neither place and would destroy the notation on the way to Obsidian. Raw `$…$` in the Reader UI is the correct, intended output.
   - **Citations restored.** Pandoc cannot resolve arXiv's `.bbl`, so it emits empty `<span class="citation">` tags and the prose loses every reference. The script parses `\bibitem[{Author et al.(2025)…}]{key}` entries out of the `.bbl` and substitutes readable `(Author et al., 2025)` labels inline.
   - **Figures inlined** as base64 data URIs (Reader can't see local files). PDF/EPS figures are rasterised via `pdftocairo`; oversized images are downscaled with `sips`; anything still too big is dropped rather than bloating the payload.
   - **References section** appended from the parsed bibliography.
   - **Title block** prepended: authors, a link back to the abs page, and the abstract as a blockquote (pandoc's body output omits all three).
4. **Save** — `POST https://readwise.io/api/v3/save/` with `html`, `should_clean_html: false`, and full metadata (title, authors, abstract as `summary`, `published_date`, tags, location), under the **versioned** abs URL.
5. **Verify** — re-reads the stored document via `/api/v3/list/` and prints the word count and location, confirming what Reader actually kept.

### Three Reader API behaviours this skill works around

These were established by direct experiment against the live API; they are not in the docs, and each one silently costs content if ignored.

1. **`should_clean_html` deletes real content.** With it on, Reader's readability pass strips every `<h1>` in the body *and* drops sections it reads as boilerplate — a controlled probe showed a `Related Work` heading removed, and on the real paper the entire References list vanished (10,035 words stored vs 13,377 with cleaning off). We build clean HTML already, so the cleaner has nothing to gain and plenty to remove. **Caveat:** turning it off makes `title` and `author` mandatory — omit either and the API returns `400 The fields 'author' and 'title' are required when you don't use should_clean_html`.
2. **Reader caches its parsed content per URL.** Deleting a document and re-saving the *same* URL can serve the earlier parse instead of your new HTML — during development a re-save kept showing the old cleaned content, byte-identical, despite corrected input. Saving under the versioned URL (`/abs/2606.00093v2`) is a fresh cache key and fixed it instantly. This is why the versioned URL is the default; if a `--replace` run appears not to take, this cache is why.
3. **`<h1>` never survives in the body**, cleaner on or off — Reader treats h1 as the document title, which it stores separately in metadata. Always ship sections as `<h2>`+.

## Output

A Reader document in the chosen queue (Later by default), printed as a `read.readwise.io/read/<id>` URL, with headings, nested lists, tables, code blocks and figures rendered natively, and maths carried as literal `$…$` / `$$…$$` source (see above — this is deliberate, for Obsidian). Its URL is the versioned `arxiv.org/abs/<id>v<n>`, so highlights flow into Readwise normally and the document records exactly which version was rendered.

Reference point from the validated run on `2606.00093v2`: 13,377 words, 12 `<h2>` sections, 8 tables, 66 references, figures embedded — all confirmed present in Reader's stored copy.

Report back to the user: the paper title, the Reader URL, the verified word count, and the citation/figure counts from the run.

## Judgement calls for the model

- **Report honestly what the script printed.** If figures were dropped or citations came back as `0`, say so — don't imply a clean render.
- **`--replace` on a re-run.** A plain re-save of a URL already in Reader returns HTTP 200 and leaves the old (possibly badly-parsed) content in place. If the user wants the improved render to replace an earlier save, pass `--replace` — but see the per-URL parse cache above if the replacement looks stale.
- **A new version invalidates an old save.** `fetch.py` resolves the *latest* version, so a paper saved months ago may now render as `v2` with different sections. Say which version was rendered; don't assume it matches an earlier save.
- **Interrupted fetches poison the cache.** `arxiv-skill` writes `flattened.tex` non-atomically, so a killed run leaves a truncated file that later runs happily reuse (pandoc then reports `unexpected end of input`). The script detects a missing `\end{document}` and re-fetches automatically; `--force-fetch` is the manual escape hatch.
- **PDF-only papers.** Older or unusual submissions have no LaTeX source; the script exits with a clear message. Don't fake it — tell the user the paper must be read as a PDF in Reader.
- **Pandoc warnings are normal.** Custom macros from a venue's `.sty` often warn without harming output. Only investigate if the final HTML is unexpectedly small or a section is missing.
- **Verifying a render.** To check what Reader really stored (as opposed to what was uploaded), fetch `GET /api/v3/list/?id=<id>&withHtmlContent=true` and grep for section titles. Reader's cleaner is the ground truth, not the local HTML.
- **After reading.** Highlights from these documents export through the normal reader4 pipeline into `00 Inbox/`; file them with the `reader4-review` skill. Papers belong in `10 Sources/Papers/`. Because the maths travels as `$…$` source, highlighted equations arrive in Obsidian already renderable — `reader4-review`'s "math notation restoration" step should have little to do on these notes, and headings/code blocks come through structured rather than as flat bullets.
- **Related skill**: the `arxiv` skill (vendored at `.claude/skills/arxiv/`) covers everything else about a paper — search, citation graphs, BibTeX, structured note templates. This skill only handles the Reader ingestion path.
