# arXiv API and Semantic Scholar reference

Read this when constructing search queries or debugging API behavior.

## arXiv search query syntax

`search.py` passes the query string straight to the arXiv API's `search_query`
parameter. Field prefixes:

| Prefix | Searches | Example |
|--------|----------|---------|
| `ti:`  | Title | `ti:"chain of thought"` |
| `au:`  | Author | `au:hinton` or `au:"del maestro"` |
| `abs:` | Abstract | `abs:distillation` |
| `co:`  | Comment | `co:"accepted at NeurIPS"` |
| `cat:` | Category | `cat:cs.CL` |
| `all:` | All fields | `all:mamba` |

Rules that matter:

- Combine terms with `AND`, `OR`, `ANDNOT` (uppercase). Group with parentheses.
- Quote multi-word phrases: `ti:"state space model"` matches the phrase;
  `ti:state space model` matches the words independently.
- Author names work best as `lastname` or `"lastname, f"` — e.g.
  `au:"vaswani, a"`. Accents and hyphens are inconsistently indexed; if a
  name search returns nothing, try a simplified spelling.
- Category matching includes cross-lists. A paper cross-listed to `cs.LG`
  matches `cat:cs.LG` even if its primary category is `stat.ML`.
- There is no full-text search. `all:` covers title/abstract/authors/
  comments/categories — not the paper body.
- Sorting: `--sort relevance | submittedDate | lastUpdatedDate`. For
  "latest papers in X", use `--sort submittedDate`. The API has no date-range
  filter worth relying on; sort by date and paginate instead, or filter
  results by their `published` field after fetching.
- Pagination: `--start N`. Keep `start + max_results` under ~2000 total; the
  API silently degrades on deep pagination.

Common categories: `cs.CL` (NLP), `cs.LG` (ML), `cs.CV` (vision), `cs.AI`,
`cs.RO` (robotics), `cs.CR` (security), `stat.ML`, `math.OC`, `quant-ph`,
`cond-mat.*`, `astro-ph.*`, `eess.AS` (audio), `eess.IV` (imaging).
Full taxonomy: https://arxiv.org/category_taxonomy

## ID semantics (important for reliability)

- A versionless ID or URL (`2409.03108`) resolves to the **latest** version,
  which can change under you. `fetch.py` therefore pins to an explicit
  version (e.g. `v2`) at download time and caches under the versioned ID.
  When citing or summarizing, always report the versioned ID from the fetch
  manifest — it records what was actually read.
- Old-style IDs look like `cond-mat/0207270` or `math.GT/0309136` (pre-2007).
  All scripts accept them.
- Withdrawn papers: the abs page still exists but the PDF/source of the
  withdrawal version may be a stub. If a fetched "paper" is suspiciously
  tiny or the comment field says "withdrawn", tell the user and check the
  abs page before summarizing.

## Rate limits

- arXiv API and downloads: **1 request per 3 seconds** per client. The
  scripts enforce this automatically (shared limiter keyed on "arxiv") and
  retry 429/5xx with backoff. Do not run multiple fetch scripts in parallel
  against arXiv.
- Bulk needs (dozens of papers): fetch sequentially and expect ~3s per
  request; warn the user about the wait rather than hammering the API.

## Semantic Scholar (s2.py)

Everything arXiv's API cannot do: citation counts, citing papers,
references, recommendations, and corpus-wide relevance search with filters.

- `s2.py info <id>` — citation/reference counts, venue, TLDR.
- `s2.py citations <id>` — who cites this paper (sorted by their citation counts).
- `s2.py references <id>` — what this paper cites.
- `s2.py recommend <id>` — related papers.
- `s2.py search "<query>" [--year 2023-2025] [--min-citations 50]
  [--fields-of-study "Computer Science"] [--max 20]` — relevance search
  over the whole S2 corpus (not just arXiv). Year accepts a single year,
  a range, or open-ended `2023-`. Use this for "important/highly-cited
  papers on X"; use arXiv search for "latest on X" or category browsing.
- `search.py --cite-counts / --rank-by-citations` — enriches arXiv search
  results with S2 citation counts via one batch request.

### API key (optional but recommended)

Detection order: `S2_API_KEY` env var, then `s2_config.json` in the skill
root — copy `s2_config.example.json` and paste the key. Free keys:
https://www.semanticscholar.org/product/api

Without a key: info/citations/references/recommend/search run on the shared
public pool (aggressive throttling; 429s are normal and retried with
backoff), and `--cite-counts` is skipped with a warning since batch lookups
are impractical keyless. With a key: private ~1 req/s quota, dependable
search and batch enrichment.

Coverage caveat: very recent papers (days old) may not be indexed yet, and
citation counts lag reality. Treat counts as estimates, and say so when a
paper is missing rather than concluding it does not exist.
