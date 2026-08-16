---
name: arxiv
description: Fetch, read, search, and take notes on arXiv papers reliably. Use this skill whenever the user mentions an arXiv ID, link (arxiv.org, ar5iv, alphaxiv, huggingface.co/papers), or DOI (10.48550/...); asks to read, summarize, explain, or compare a research paper; wants to find papers on a topic, by an author, or in a category; asks what cites a paper, how influential it is, or for related work; wants a BibTeX citation; or wants paper notes written for their notes system or codebase. Use it even for casual phrasings like "check out this paper" or "what's the latest on X" — do not improvise curl commands or read arXiv PDFs directly when this skill is available.
---

# arXiv

Scripts and rules for working with arXiv papers. The scripts live in
`scripts/` (stdlib-only Python; pandoc/pdftotext used if present) and handle
the deterministic parts — fetching, caching, extraction, conversion — so
never hand-roll curl/wget calls against arXiv. Judgment-based parts
(summarizing, table emphasis, relevance) are yours, governed by the
references.

Run scripts from the skill directory (they import siblings):
`cd <skill-dir>/scripts && python3 <script>.py ...`. Every script supports
`--help` and most support `--json`.

## Which workflow?

| User wants | Do |
|---|---|
| Read/summarize/explain a specific paper | Workflow 1 |
| Find papers on a topic/author; "latest on X" | Workflow 2 |
| Reference note, "add to my notes", full writeup | Workflow 3 |
| "What does this paper mean for my project/code" | Workflow 4 |
| Citations, influence, related work | `s2.py` (see Workflow 2) |
| BibTeX | `python3 bibtex.py <id-or-url>` |

## Workflow 1: Fetch and read a paper

1. `python3 fetch.py <anything> --json` — accepts bare IDs, any arXiv URL
   form, ar5iv/alphaxiv/HF links, DOIs, old-style IDs. It normalizes,
   pins the version, downloads LaTeX source (PDF only as fallback), safely
   extracts, finds the main .tex, and flattens all `\input`/`\include` into
   `flattened.tex`. Idempotent; cached under `~/.cache/arxiv-skill/`.
2. Read the **flattened LaTeX directly** — it is the highest-fidelity form
   (math, tables, structure all intact) and usually the right thing to load
   into context. Run `python3 to_markdown.py <id>` only when the user wants
   a Markdown file or the LaTeX is unreadably macro-heavy.
3. Check the manifest's `notes` field. If the paper was PDF-only, the text
   came from `pdftotext` and is **degraded**: do not trust equation/table
   details from it without checking the PDF itself (which you can read
   directly as a fallback).
4. When reporting anything from the paper, use the **versioned ID** from the
   manifest (e.g. `2409.03108v2`) — that is what was actually read.

Long papers: the flattened tex can exceed what you should load wholesale.
Skim structure first (`grep -n '\\\\section' flattened.tex`), then read the
sections that matter for the user's question.

## Workflow 2: Search and discover

Two search backends; pick by intent:

- **arXiv metadata search** (`search.py`) — categories, authors-on-arXiv,
  "latest papers on X" (`--sort submittedDate`):
  `python3 search.py 'ti:"state space" AND cat:cs.LG' --max 10`
  Add `--cite-counts` to attach Semantic Scholar citation counts, or
  `--rank-by-citations` to sort by them (both need the API key below; one
  batch request, skipped with a warning if keyless).
- **Semantic Scholar relevance search** (`s2.py search`) — "important papers
  on X", filtering by year or citation floor, venue-published work:
  `python3 s2.py search "state space models" --year 2023-2025 --min-citations 50`
- Citation data for one paper, "how influential", related work:
  `python3 s2.py info|citations|references|recommend <id>`.

Before writing a non-trivial arXiv query, read `references/api-syntax.md` —
field prefixes, phrase quoting, category taxonomy, and sorting have sharp
edges. Zero results usually means query syntax, not absence — simplify to
`all:<terms>` and retry once before concluding nothing exists.

**Semantic Scholar API key (optional):** detected from the `S2_API_KEY` env
var or `s2_config.json` in the skill root (copy `s2_config.example.json`).
Keyless, S2 features still work on the shared public pool but throttle
hard, and `--cite-counts` is skipped. If an S2 call keeps failing and no
key is configured, suggest adding one to the user.

Give the user versioned IDs and titles so any paper can be fetched next.

## Workflow 3: Structured note

Fetch (Workflow 1), then read `references/note-template.md` (Mode A) for
the exact note structure and file placement, and
`references/table-policy.md` **before converting any results table or
writing any number** — it defines the emphasis policy and the
no-invented-numbers rules. Generate the citation with `bibtex.py`.

## Workflow 4: Contextual reading (paper -> project)

Fetch (Workflow 1), then read `references/note-template.md` (Mode B).
The defining step: inspect the actual project files the paper relates to
before writing, and name real paths/functions in the note. Keep "the paper
showed X" strictly separate from "X might help here".

## Reliability rules (always)

- Respect rate limits: the scripts enforce arXiv's 1-request-per-3s; do not
  parallelize arXiv downloads or bypass the scripts.
- Never report a number that is not in the source; write "not reported"
  instead (full rules in `references/table-policy.md`).
- Surface manifest `notes` (withdrawn paper, missing source, degraded
  extraction) to the user instead of papering over them.
- If a script errors, show the user the actual error and what you tried;
  network failures against arXiv/Semantic Scholar are usually transient
  rate limiting.
