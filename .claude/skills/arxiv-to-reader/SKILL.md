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
- **Dependencies**: `pandoc` (`brew install pandoc`); `pdflatex` for the dense-table rendering (TeX Live 2024 **basic** at `/usr/local/texlive/2024basic` is what's installed and is sufficient — the compile preamble is filtered to whatever packages exist); plus the `arxiv` skill vendored alongside this one at `.claude/skills/arxiv/` — the script finds it automatically (override with `ARXIV_SKILL_DIR`, and it still falls back to `~/Downloads/arxiv-skill`). `pdftocairo` and `sips` are optional — used only for PDF-format figures and downscaling.

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
| `--tables dense\|all\|none` | Render tables as images: wide grids only (default), every table, or none |
| `--table-min-cols N` | Column count at which a table becomes an image (default 8) |

## How it works

1. **Fetch** — normalises the input to a bare arXiv ID (via the `arxiv` skill's `normalize_arxiv_id`), then calls its `fetch.py`, which pins an explicit version, downloads the e-print tarball, safely extracts it, finds the entry `.tex` and recursively inlines `\input`/`\include` into one `flattened.tex`. Cached under `~/.cache/arxiv-skill/<versioned-id>/`.

   *Why normalise first:* handed a full URL, `fetch.py` caches under an **unversioned** directory and never writes `meta.json`, so metadata lookup fails. Handed a bare ID it pins the version and writes complete metadata. Don't pass raw URLs through to it.
2. **Convert** — `pandoc -f latex -t html --mathjax --wrap=none --shift-heading-level-by=1`.

   *Scale boxes are unwrapped first (step 2a).* Authors routinely shrink a wide table with `\scalebox{0.75}{\begin{tabular}…}` or `\resizebox{\columnwidth}{!}{…}`. **Pandoc does not understand these commands and silently discards the entire group — every table inside one vanishes**, with no warning and no error. On `2506.22316` this cost all 4 tables (5,415 words; 6,611 after the fix). The script strips `\scalebox` / `\resizebox` / `\adjustbox` / `\makebox` wrappers and keeps their content: the scale factor means nothing in HTML, so nothing of value is lost. This runs *before* the dense-table step, so unwrapped tables are also visible to the column counter.

   **The unwrapper must skip LaTeX comments.** It brace-matches forward from the command, so a *commented-out* `% \resizebox{\textwidth}{!}{%` — dead text authors leave behind constantly — matched, ran on into live code, and spliced out a real closing brace. The document then had balanced braces and balanced environments but was structurally wrong, and pandoc ran to EOF reporting `unexpected end of input / expecting \end{document}` — a message that points at the last line of the file and tells you nothing about the actual cause. On `2606.27226` this made the paper unconvertible while `unwrapped 3 scale/resize box(es)` was printed for three occurrences that were all commented out. `_is_commented` now guards every match. Diagnostic worth reusing: if the raw `flattened.tex` converts but the unwrapped copy doesn't, the unwrapper is the culprit — compare the two directly rather than trusting the reported line number.

   *Dense tables become images (step 2b, before pandoc).* A 21-column results grid is unreadable and unhighlightable in Reader's narrow column, and HTML can't rescue it. Each table float with **≥ 8 columns** (`--table-min-cols`) is compiled by real `pdflatex` into a standalone PDF, rasterised at 200 dpi, and swapped into the LaTeX as `\includegraphics` — so it flows through the normal figure path and ends up inlined as a data URI. Fidelity is exact: booktabs rules, cell shading, `multirow`, and maths in headers all survive, because it is the paper's own LaTeX rendering it. Narrow tables (4–5 columns) stay as real HTML tables and remain highlightable, which is the right trade — you lose selectable text only where it was never usable. **Captions stay as HTML text** outside the image, so they are still searchable and highlightable. Images are cached in `~/.cache/arxiv-skill/<versioned-id>/tables/`, so re-runs are cheap.

   Details that matter if you touch this code:
   - The float is re-emitted as a `figure`, **not** a `table`. Pandoc attaches a `\caption` inside a `table` environment to the tabular it builds; with the tabular replaced by an image there is nothing to attach to and the caption is silently dropped.
   - The compile preamble is the paper's own, minus the venue style file (`iclr2025_conference.sty` and friends — they pull in fonts a minimal TeX lacks and contribute nothing to a table) and minus any `\usepackage` whose `.sty` isn't installed (a missing package is fatal to LaTeX even in `nonstopmode`). Everything else is kept verbatim so the authors' macros still resolve.
   - `\textwidth`/`\columnwidth`/`\linewidth` are given explicit values; tables routinely wrap themselves in `\resizebox{\columnwidth}{!}{…}` and `standalone` has no page, so without this LaTeX aborts with `Dimension too large`.
   - No `-halt-on-error`: leftover calls to the dropped venue style (`\iclrfinalcopy`) are undefined but harmless, and LaTeX still typesets the table after reporting them.
   - Requires `pdflatex`. Without it the step is skipped with a warning and tables stay as HTML — nothing breaks.
   - **Column counting must brace-match the spec.** Reading it with `[^}]*` terminates inside the booktabs `@{}` idiom, so `{@{}cccccccccc@{}}` counted as **0 columns** and the whole feature silently never fired on the most common table style in ML papers. `table_column_count` now brace-matches, drops `@{}`/`>{}`/`<{}`/`!{}` inter-column material, and counts `p{}`/`m{}`/`b{}`/`X` as one column each. Regression shapes worth keeping green: `{@{}cccccccccc@{}}`→10, `{@{}l>{\centering}p{2cm}c@{}}`→3, `tabularx{\textwidth}{@{}lXX@{}}`→3.
   - A compile failure is not a content loss: the table falls back to real HTML. `tables rendered: 0, failed: 2` means two wide tables stayed as HTML — legible, just not pixel-faithful.

   *Automatic LaTeX recovery (only on failure).* When pandoc can't parse the paper at all, the script retries once with a repaired copy. Three distinct causes have shown up in practice:

   - **Preamble plumbing.** Papers styled with `tikz`/`soul`/`pgf` define `@`-internal macros that abort the parse with `unexpected end of input`, even though the body is fine. The retry rebuilds a **sanitised preamble** — a minimal `\documentclass` plus only the author's simple one-line macros. Macros whose bodies are unparseable but that the text still *calls* (e.g. `\MET` → `\verdicttoken{…}`) get a passthrough stub `\newcommand{\name}[n]{#1}`, so the token renders as text instead of leaving a dangling command that MathJax paints red.
   - **`\newcolumntype` after `\begin{document}`.** Legal LaTeX, but pandoc chokes on the `#1` parameter there (seen on `2601.18491`). These are pure table-layout helpers with no meaning in HTML, so `repair_body` deletes the lines outright.
   - **Unbalanced braces.** `2605.12894` opens `{\small` before its bibliography and never closes it; TeX closes the group implicitly at `\end{document}`, pandoc reports `unexpected \end` and gives up. `repair_body` counts brace depth — comment-aware and skipping `verbatim`/`lstlisting`/`minted` — and appends the missing closers before `\end{document}`.
3. **Post-process** — the part that makes Reader render it well:
   - **Headings shifted to `<h2>`.** Reader's HTML cleaner *deletes every `<h1>` in the body* (it treats h1 as the document title, which it stores separately). Sections sent as h1 silently vanish, leaving one undifferentiated wall of text. This is the single most important fix — never send h1s.
   - **Math delimiters** rewritten from pandoc's `\(…\)` / `\[…\]` to `$…$` / `$$…$$`. **Reader displays these literally — it does not render the equations, and that is intentional.** The delimiters are preserved for downstream Obsidian, which renders `$…$` inline and `$$…$$` as blocks natively, so a highlight carried through the reader4 pipeline lands as real maths in the vault. Do **not** "fix" this by switching to MathML or pre-rendered images: that would render in neither place and would destroy the notation on the way to Obsidian. Raw `$…$` in the Reader UI is the correct, intended output.
   - **Citations restored, from `.bbl` *or* `.bib`.** Pandoc cannot resolve either, so it emits empty `<span class="citation">` tags and the prose loses every reference. First choice is the generated `.bbl`: natbib's `\bibitem[{Author et al.(2025)…}]{key}` label *is* the inline citation, so it substitutes directly as `(Author et al., 2025)`. **Many papers ship only a `.bib`** (no `.bbl` in the tarball) — for those a BibTeX fallback parses `@type{key, …}` entries, brace-matching the body, and builds labels from surnames + year (1 author → `Smith, 2024`; 2 → `Smith and Jones, 2024`; 3+ → `Smith et al, 2024`). Without this fallback such papers upload with **every inline citation deleted and an empty References section** — silently, since the empty spans are stripped. It is worth watching: `citations restored: 0` on a paper that obviously cites things means the bibliography wasn't found.
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

Reference points from validated runs, all confirmed against Reader's stored copy:

| Paper | Result |
| --- | --- |
| `2606.00093v2` | 13,377 words, 12 `<h2>` sections, 8 HTML tables, 66 references |
| `2410.03775v3` | 13,099 words, 7 dense tables rendered as images, 31 figures embedded (0 dropped), 6 narrow tables left as HTML, 3.9 MB stored |
| `2504.14716v2` | 8,818 words, 18 HTML tables + 1 rendered as an image, 5 figures, 83 references — the table-heavy case |
| `2601.18491v2` | 14,294 words, exercises `\newcolumntype` body repair + BibTeX fallback (65 citations from 189 entries), 5.6 MB stored |
| `2605.12894v1` | 12,946 words, exercises unbalanced-brace repair + BibTeX fallback (35 citations from 51 entries) |
| `2411.13768v3` | 14,838 words, 3 tables, 9 figures, 183 references, 94 citations — clean run, no recovery needed |

Report back to the user: the paper title, the Reader URL, the verified word count, and the citation/figure counts from the run.

## Judgement calls for the model

- **Report honestly what the script printed.** If figures were dropped or citations came back as `0`, say so — don't imply a clean render.
- **`--replace` cannot be trusted to replace.** Its delete branch only fires when the save returns **HTTP 200** ("already exists"). Reader does not reliably do that: re-saving `2605.07847v1` — byte-identical URL, document already in Later — returned **201** and created a *second* document at the same URL, so `--replace` deleted nothing and quietly left a duplicate pair in the queue. Never assume a `--replace` run cleaned up: list the queue afterwards and check for two documents sharing a `source_url`. To genuinely replace, look the old document up by `source_url` via `/api/v3/list/` and `DELETE /api/v3/delete/<id>/` it explicitly, **after** verifying the new copy stored correctly.
- **Deleting a document destroys its Reader highlights.** Before removing an old copy, check for children with `GET /api/v3/list/?category=highlight&parent_id=<id>` — and note the `parent_id` filter is unreliable, so filter the returned page yourself on `x["parent_id"] == id`. A cheaper account-wide sweep is `GET /api/v2/export/`, which lists every book with its highlights and `source_url` in one paginated call and lives in a **separate rate-limit bucket** from v3 — worth knowing, because v3 `list` with `withHtmlContent=true` exhausts its budget in about a dozen calls and then 429s for minutes.
- **A new version invalidates an old save.** `fetch.py` resolves the *latest* version, so a paper saved months ago may now render as `v2` with different sections. Say which version was rendered; don't assume it matches an earlier save.
- **Interrupted fetches poison the cache.** `arxiv-skill` writes `flattened.tex` non-atomically, so a killed run leaves a truncated file that later runs happily reuse (pandoc then reports `unexpected end of input`). The script detects a missing `\end{document}` and re-fetches automatically; `--force-fetch` is the manual escape hatch.
- **PDF-only papers.** Older or unusual submissions have no LaTeX source; the script exits with a clear message. Don't fake it — tell the user the paper must be read as a PDF in Reader.
- **Figures must ship as `<img>`, never `<embed>`.** Pandoc emits `<embed src="…">` for any graphic whose LaTeX reference has no raster extension — most of them. **Reader strips `<embed>` out of the stored document**, so the figure silently disappeared while its `<figcaption>` stayed, which is exactly what the symptom looks like from the reader's side: a caption under nothing. Confirmed against 10 of 11 saved papers (65 lost figures; `2410.03775v3` alone lost 20). `embed_images` now rewrites every match to `<img>`, carrying over `alt`/`title`/`style`/`width`/`height`. When verifying a stored render, `<embed>` must be **0** — count both tags, not just `data:image`, since a data URI inside an `<embed>` still won't display.
- **Watch the dropped-figure count.** `figures embedded: N, dropped: 0` is the healthy signal. Non-zero drops mean unresolved paths or oversized rasters — worth investigating rather than shipping quietly. Two path traps were fixed here and are easy to reintroduce: `Path.with_suffix()` truncates figure names containing dots (`gpt-3.5-turbo.pdf`), and image refs must be resolved on the **full** src path, since rendered table images live outside the source tree and are referenced absolutely.
- **Payload size.** Table images and inlined figures push papers into the megabytes (3.9 MB for `2410.03775`); the guard is 8 MB. If a paper trips it, `--no-images` or `--tables none` are the escape hatches.
- **Pandoc warnings are normal.** Custom macros from a venue's `.sty` often warn without harming output. Only investigate if the final HTML is unexpectedly small or a section is missing.
- **Verifying a render.** To check what Reader really stored (as opposed to what was uploaded), fetch `GET /api/v3/list/?id=<id>&withHtmlContent=true` and grep for section titles. Reader's cleaner is the ground truth, not the local HTML.
- **After reading.** Highlights from these documents export through the normal reader4 pipeline into `00 Inbox/`; file them with the `reader4-review` skill. Papers belong in `10 Sources/Papers/`. Because the maths travels as `$…$` source, highlighted equations arrive in Obsidian already renderable — `reader4-review`'s "math notation restoration" step should have little to do on these notes, and headings/code blocks come through structured rather than as flat bullets.
- **Count tables against the source before claiming loss.** `grep -c 'begin{tabular}'` over `flattened.tex` counts **commented-out** environments too — on `2411.13768` three of six were `%`-prefixed, and 3 tables was the correct, complete answer. Strip comments before comparing, or you will chase a phantom bug.
- **Related skill**: the `arxiv` skill (vendored at `.claude/skills/arxiv/`) covers everything else about a paper — search, citation graphs, BibTeX, structured note templates. This skill only handles the Reader ingestion path.

## Known gaps

Not a content loss, but real and unfixed — don't rediscover it from scratch.

- **Dense-table image compiles can fail** (`tables rendered: 0, failed: 2` on `2506.22316`) even when the tables are correctly detected. The fallback leaves them as HTML, so nothing is lost, but the standalone-compile preamble hasn't been chased down for this case.
