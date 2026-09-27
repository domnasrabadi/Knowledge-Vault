# Reader API: uploading, duplicates, highlights, verifying

Every API route (arXiv, web, PDF, Word, non-arXiv LaTeX) ends here. The EPUB
routes never touch the API; the user drags the file in. That split exists because
**the API cannot take a file upload**: it saves a URL plus optional HTML, and
`category: epub` is only a label.

`scripts/reader_api.py` does all of it. Token: `$READWISE_TOKEN`, else
`~/Downloads/reader4/.env` (<https://readwise.io/access_token>).

## The order is the safety mechanism

```
1. build        → page.html + meta.json, stats printed      (route-specific)
2. check        → reader_api.py check <url> [--title "..."]
3. ASK          → AskUserQuestion, always
4. save         → reader_api.py save page.html meta.json [--fresh-url]   (verifies itself)
5. delete old   → reader_api.py delete <old-id> --yes [--yes-lose-highlights]
```

**Nothing is uploaded without a yes from the user**. That's a standing decision
for every route, arXiv included. The question shows what they are agreeing to:

- title, source URL, words, headings, tables, figures, maths count (from the build)
- anything the build flagged: dropped images, MathML with no TeX source
- **if `check` found an existing copy**: its location, word count and highlight
  count, with three choices:
  - **Replace**: `save --fresh-url`, confirm it verified, then `delete` the old
    copy. Deleting destroys the old copy's highlights, so say the number.
  - **Keep both**: `save --fresh-url`, delete nothing.
  - **Cancel**.

Step 5 runs only after step 4 printed `✓ verified`. Never delete first. If
verification fails, stop, report what Reader dropped, and leave the old copy.

## `check`: finding an existing copy

The list endpoint has **no URL filter** and allows **20 calls per minute**, so
`reader_api.py` keeps an index of the library at
`~/.cache/reader-ingest/library.json`: documents in `article`/`pdf`/`epub`, plus
every highlight's parent. The first run pages the whole library once and may take
a few minutes on a large account; later runs fetch only what changed
(`updatedAfter`), usually in one or two calls. `429` responses are retried after
`Retry-After`.

Matching normalises URLs. It ignores scheme, `www.`, trailing slashes,
fragments and tracking parameters, and any arXiv abs/pdf/version collapses to
the paper id. Pass `--title` for sources without a stable URL, such as a local
PDF the user uploaded before.

Incremental sync never hears about deletions, so each match is re-confirmed
with a direct lookup before it's reported. Highlight counts come from the
index and can include highlights deleted since the last full pass. Use
`--full-sync` if a count looks wrong.

## `save`: what gets sent

- `should_clean_html: false`, always, which makes `title` and `author` mandatory.
  `html_for_api.py` refuses a `meta.json` without them. If there is no person,
  the author is the site or publisher name.
- `category: article`, `saved_using: reader-ingest`, location `later` by default.
- `published_date` only if `meta.date` is ISO; `summary` from `description` or
  the abstract.
- `--fresh-url` appends `reader-ingest=YYYYMMDD` as a query parameter. It still
  opens the right page on click-through, and gives Reader a new cache key (see 2
  and 4 below). Use it whenever `check` found an existing copy.

A `200` response means Reader **kept its old copy and ignored the new HTML**.
`save` exits with code 3 and says so; re-run with `--fresh-url`.

## Five Reader behaviours, all observed, none documented

Each one silently costs content or highlights if ignored.

1. **`should_clean_html` deletes real content.** With it on, Reader's readability
   pass strips every `<h1>` in the body *and* drops sections it reads as
   boilerplate. A controlled probe showed a `Related Work` heading removed, and on
   a real paper the entire References list vanished (10,035 words stored vs 13,377
   with cleaning off). We send clean HTML already, so the cleaner has nothing to
   gain. **Caveat:** off makes `title` and `author` mandatory, otherwise
   `400 The fields 'author' and 'title' are required when you don't use should_clean_html`.
2. **Reader caches its parsed content per URL.** Deleting a document and re-saving
   the *same* URL can serve the earlier parse instead of the new HTML. During
   development a re-save kept showing the old content byte for byte. A distinct URL
   is a fresh cache key: arXiv's versioned URL (`/abs/2606.00093v2`), or
   `--fresh-url` for everything else.
3. **`<h1>` never survives in the body**, whether the cleaner is on or off. Reader treats it
   as the document title, stored separately. Every route ships sections as
   `<h2>` or lower. `html_for_api.py` shifts the whole hierarchy down a level rather
   than merging h1 into h2.
4. **Re-saving an existing URL is unpredictable.** It can return `200` and ignore
   the new HTML, *or* return `201` and create a silent duplicate. Re-saving
   `2605.07847v1` (byte-identical URL, already in Later) returned `201` and left
   two documents at one URL. That's why the old `--replace` flag was retired: its
   delete branch only fired on `200`. Replace explicitly with check → save
   `--fresh-url` → verify → delete.
5. **Deleting a document destroys its highlights.** They are child documents
   (`category=highlight`, `parent_id=<doc>`). The list endpoint's `parent_id`
   filter is unreliable, so `reader_api.py` filters the highlight index itself
   and `delete` refuses a document with highlights unless given
   `--yes-lose-highlights`. Pass it only when the user explicitly accepted
   losing that many highlights.

And one general rule: **Reader strips `<embed>`**, so a figure sent that way
vanishes while its caption stays. Always send `<img>`. `html_for_api.py` and
`arxiv_to_reader.py` both convert.

## Verifying a render

`save` re-reads the stored document (`withHtmlContent=true`, retried while Reader
finishes parsing) and compares it with what was sent: words, and counts of `h2`,
`h3`, `table`, `pre` and `img`. Anything lost is flagged `<-- LOST`; below 97% of
the words is a failure. **Reader's stored copy is the ground truth, not the local
HTML.**

`reader_api.py verify <id> page.html --probe "..."` re-runs it later, with
content probes for anything that was at risk. `withHtmlContent` is expensive:
it exhausts the list budget in about a dozen calls, then returns 429 for minutes.
Verify once per upload, not in a loop.

## After reading

Highlights export through the normal reader4 pipeline into `00 Inbox/`; file them
with the `reader4-review` skill. Because maths travels as `$…$` source on every
route, highlighted equations arrive in Obsidian already renderable.
