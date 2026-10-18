---
type: system
status: structured
quality:
topics: [rag, knowledge-management]
source: ""
created: 2026-10-19
published:
author: Dom Nasrabadi
flashcards: none
updated: 2026-10-19
---
# Knowledge Vault GraphRAG — Implementation Plan

How and in what order to build what the [[Knowledge Vault GraphRAG - Design Spec|design spec]] describes. The spec says what the system is and why; this plan says what to do next. If they disagree, the spec wins. Status and orientation live in [[GraphRAG - Start Here]].

## Where things stand

As of 2026-10-19 the design is complete and nothing is built. The spec is at `50 Graph/Knowledge Vault GraphRAG - Design Spec.md`. No code exists yet, `50 Graph/.graphrag/` has not been created, and none of the housekeeping diffs below have been applied.

Next steps, in order:

1. Dom reviews and applies the housekeeping diffs (`.gitignore`, `AGENTS.md`, vault-lint, vault-digest).
2. Settle the open decisions that block code (see Before any code). Decide the simplification review first, because it shrinks phases 4–8. A local cost-estimate script gives real numbers for the budget decision.
3. Build phases 0–8 in order, stopping at each exit check for Dom's review.

## Proposed layout

Code goes in a dot-folder inside the graph's own folder: `50 Graph/.graphrag/` (decided 2026-10-19). Obsidian hides dot-folders wherever they are, so the Python files, JSONL and prompt files stay out of search, the graph view and vault-lint's folder rules. It is still tracked and cloned with the vault, which is what the hybrid decision needs, and everything the graph writes sits under `50 Graph/`. The only cost is quoting the space in "50 Graph" in shell commands.

```text
Knowledge Vault/
└── 50 Graph/
    ├── Knowledge Vault GraphRAG - Design Spec.md
    ├── Knowledge Vault GraphRAG - Implementation Plan.md
    ├── GraphRAG - Start Here.md
    ├── Review Queue.md, Review Log.md
    ├── Registry/                   <kind>--<slug>.md, generated: true
    ├── Concepts/                   MOC pages, generated: true
    ├── Reports/<date>/             hub audit, metrics, re-extraction diffs
    └── .graphrag/                  code home (hidden), tracked unless marked
        ├── docs/atlas.html         visual explainer; open in a browser
        ├── pyproject.toml, uv.lock
        ├── config.yaml             every tunable number (spec: Config and defaults)
        ├── prompts/                P1_mention_extraction.md … P14_exhaustiveness.md
        ├── src/vault_graphrag/     parse, chunk, resolve, claims, score,
        │                           communities, writeback, sync, query, eval
        ├── tests/                  unit tests + fixture notes
        ├── eval/                   query set, evidence labels, judge calibration
        ├── export/                 JSONL snapshot of LLM outputs, committed each sync
        ├── store/                  graph + vector store            (gitignored)
        ├── cache/                  LLM response cache, embeddings  (gitignored)
        ├── logs/                   queries.jsonl, run logs         (gitignored)
        └── .env                    API keys                        (gitignored)
```

The spec's query log is `.graphrag/logs/queries.jsonl`, under `50 Graph/`. A plain, non-dot subfolder would not work: its files would show up in Obsidian and fail vault-lint.

## Proposed diffs (not applied)

Five files need changes before phase 0, so that `50 Graph/` and `50 Graph/.graphrag/` don't trip vault tooling or leak secrets. Dom applies them; Claude only proposes. The `.agents/skills/` mirror is handed to Dom's other agent. `AGENTS.md` is not tracked by git, so apply its diffs on each machine.

### 1. `.gitignore`

`50 Graph/` is tracked by default because nothing ignores it. Only runtime state and secrets need excluding. Apply this before phase 0 creates any store or `.env`.

```diff
+# GraphRAG engine: tracked, except runtime state and secrets
+50 Graph/.graphrag/store/
+50 Graph/.graphrag/cache/
+50 Graph/.graphrag/logs/
+50 Graph/.graphrag/.venv/
+50 Graph/.graphrag/.env
+**/__pycache__/
```

### 2. `AGENTS.md`

Layout table: add a row after `40 System/`.

```diff
+| `50 Graph/` | Output of the GraphRAG index: its design spec, implementation plan, Registry, Review Queue and Log, generated concept pages, reports. Engine code lives in the hidden `50 Graph/.graphrag/`. | Written by the graph pipeline. Dom edits only Review Queue decisions and Registry aliases and definitions |
```

Frontmatter rules: add a bullet.

```diff
+- **Generated notes** (`generated: true`, in `50 Graph/Registry/` and `50 Graph/Concepts/`) use the graph's own frontmatter, not this schema. Don't hand-edit them, except Registry aliases and definitions.
```

Git section: extend "What git tracks".

```diff
-- **What git tracks** (see `.gitignore`): `00 Inbox`, `10 Sources`, `20 Books`, `90 Attachments`, and the skills in `.claude/` and `.agents/`.
+- **What git tracks** (see `.gitignore`): `00 Inbox`, `10 Sources`, `20 Books`, `50 Graph` (including the GraphRAG engine in `50 Graph/.graphrag/`, except its store, cache, logs and `.env`), `90 Attachments`, and the skills in `.claude/` and `.agents/`.
```

New section before "Other things to know":

```diff
+## GraphRAG index
+
+A claim-centred graph over `10 Sources/` and `20 Books/`. Start at `50 Graph/GraphRAG - Start Here.md`. Spec: `50 Graph/Knowledge Vault GraphRAG - Design Spec.md`. Engine: `50 Graph/.graphrag/`.
+
+- It never edits notes. It writes only to `50 Graph/`, and never reads `50 Graph/` as input.
+- Uncertain decisions go to `50 Graph/Review Queue.md`. Dom writes `approve`, `reject` or `edit: …`; the next sync applies them.
+- The binary store is rebuildable. The committed JSONL in `50 Graph/.graphrag/export/` holds the LLM outputs, so a clone rebuilds without LLM calls.
```

### 3. `vault-lint` (`.claude/skills/vault-lint/SKILL.md`)

```diff
-Read `AGENTS.md` for the canonical rules. Scan every `.md` note outside `.obsidian/` and report violations
+Read `AGENTS.md` for the canonical rules. Scan every `.md` note outside dot-folders (`.obsidian/`, `.claude/`, `.agents/`, `50 Graph/.graphrag/`) and report violations
```

```diff
 ## Checks
+
+**Graph exemptions.** Notes with `generated: true` (`50 Graph/Registry/`, `50 Graph/Concepts/`) and `50 Graph/Review Queue.md` and `Review Log.md` skip checks 1–5 and 9. Their kebab-case `<kind>--<slug>.md` names are intended. Wikilinks in them are still checked (8).
```

```diff
-7. **Location rules** — `10 Sources/Articles|Papers` are flat (no subfolders); …
+7. **Location rules** — `10 Sources/Articles|Papers` are flat (no subfolders); `50 Graph/` holds only the graph's files and `type: system` notes; …
```

### 4. `vault-digest` (`.claude/skills/vault-digest/SKILL.md`)

```diff
 ## Gather
+
+Skip `50 Graph/` for items 1–4 and leave generated notes out of the counts in 5.
+
+6. **Graph review** — open items in `50 Graph/Review Queue.md`, counted by type, oldest first (only once the graph exists).
```

### 5. `.agents/skills/` mirror

After Dom applies diffs 3 and 4, the other agent updates its adapted copies of `vault-lint` and `vault-digest`. Don't copy files over the mirror wholesale.

## Before any code

These open decisions block or reshape the build. They are listed in full under Open questions in the spec. A local cost estimate, which sends no vault text anywhere, gives the cost decision real numbers.

| Open decision | Options | Claude's suggestion | Blocks |
| --- | --- | --- | --- |
| Simplification review (10 trims) | Apply some, all or none | Decide first: trims 1, 2, 3 and 5 alone remove P9, P10 and P12 and shrink phases 6–7 | Phases 4–8 |
| Storage stack | Embedded (SQLite + a vector extension, igraph and leidenalg for clustering) · Neo4j server · a GraphRAG library | Embedded: one file, no server, easy to rebuild from JSONL. A library would fight the claim-centred model | Phase 0 |
| Highlight density and voice | Keep as specified · drop highlight density and set voice by note status | Drop it: the vault rarely uses `<mark>`, so the factor is about 1.0 everywhere | Phase 1 |
| Data egress: embeddings | Hosted embedding API · local model | Decide after the cost estimate. Local is free and private; hosted is usually stronger | Phase 1 |
| Data egress: LLM prompts | Claude API · local LLM | Claude API: P2–P4 quality drives everything downstream | Phase 2 |
| Cost ceiling | A budget for one full run | Set it from the estimate below | Phase 2 |
| Support in ranking | Rerank fused results by query-time support · tie-break only · evidence labels only | Decide in phase 7 against the fixed queries | Phase 7 |
| Expansion algorithm, answer context | See the spec | Leave open until phase 7 evaluation | Phase 7 |
| Unrated weight | Same as ⭐, or less | Keep the default (1.0) and tune in evaluation | Nothing |
| Query interface | MCP, skill, CLI, explorer | Leave until after phase 8, as the spec says | Nothing |

**Cost estimate (step 0):**

1. A script parses and chunks every in-scope note, using the phase 1 chunker in draft form. Nothing leaves the machine.
2. It counts passages, tokens per passage, and expected calls per prompt: P1, P3 and P4 per passage; P2 per mention not matched exactly, at an assumed rate set in config and refined after the phase 2 pilot; P11 and P14 on their samples.
3. It prices one full run at three model tiers, using current prices checked at the time, and adds re-extraction and evaluation runs.
4. Dom picks the tier and sets the ceiling. The ceiling goes into `config.yaml` as a hard stop: a run halts when spend reaches it.

## Step-by-step build

Each phase ends at its spec exit check, and Claude stops there for Dom's review before starting the next. Phases 2 and 4 run on a 20-note pilot set first: prompts get tuned while runs are cheap, before the full corpus. If simplification trims are applied, remove the matching tasks below.

| Phase | Tasks | Dom's part | Exit check |
| --- | --- | --- | --- |
| 0. Setup | `uv` project in `50 Graph/.graphrag/`; `config.yaml` with every spec default; prompt file template (version, JSON schema, examples); lineage and logging helpers; LLM client with retries, response cache and the spend cap; stub pipeline; pick the pilot set (20 notes covering all four types, a Book, raw and distilled notes, structured notes with `<mark>`, and unrated notes) | Apply the diffs; approve the stack; add API keys to `.env` | One test note runs end to end through the stub |
| 1. Parse and chunk | Frontmatter parser; heading, bullet and sentence chunker that keeps code blocks and tables whole; voice and highlight density (as decided); Book detection and IN\_BOOK; independence groups (Book, raw + distilled pairs, config overrides); stable IDs; passage embeddings and BM25 index; JSONL export | Spot-check 10 notes' passages | All in-scope notes parsed; no passage over 400 tokens except a lone code block or table; re-runs give identical IDs |
| 2. Registry bootstrap | P1 and P2 with vault examples; exact-match normaliser; candidate search; pilot run, tune, then full run; clustering and auto-merge; Registry files; Review Queue writer and reader; resolution audit sampler | Review the top 100–150 clusters and every `unsure` item; label 50 auto-merges | Linking rate ≥ 75%; resolution audit ≥ 95% |
| 3. Concept graph | Weighted NPMI with the rare-pair guard; CO\_OCCURS edges; degree and degree-change tracking; hub audit report | Classify the top-20 hubs | Dom has reviewed the audit; no boilerplate in the top 20 |
| 4. Claims | P3, P4, P5, P11 and P14; claim matching in neighbourhoods; supersession; support and opposition; post-write checks and rejection log; relation-phrase clustering; pilot first | Spot-check P14 misses; decide whether to merge P1 and P3 | Exhaustiveness ≥ 0.8; citation support ≥ 90% |
| 5. Communities and write-back | Hierarchical Leiden; P6 summaries with `built_from`; P7 MOC pages; P8 taxonomy suggestions; Concepts pages; then draft the evaluation sets (40 queries, 15 evidence labels, calibration pairs) | Check pages in Obsidian; run vault-lint; edit the drafted evaluation sets | Pages render; vault-lint passes |
| 6. Incremental sync | Git-diff sync (adds, edits, renames, deletes); passage reuse by `text_hash`; frontmatter-only reweighting; staleness tracking; retry list; shadow graph and diff report; one `sync` command | Approve a test re-extraction diff | Edit, rename and delete of a test note each update the graph correctly |
| 7. Query pipeline | P9, P10 and P12; retrieval channels (passage vectors, BM25, claim vectors, graph expansion, community summaries); RRF; coverage loop with its five tools; P11 citation filter; answer format; query log | Read the answers to all 40 queries | All 40 answered with valid citations |
| 8. Evaluation harness | P13 judge; calibration on 40 pairs and held-out check on 20; metrics and per-run reports; a regression gate for prompt or model changes | Label 60 calibration pairs; spot-check 10 judgements | Held-out TPR and TNR ≥ 0.8; first scores recorded |

## Risks and mitigations

The biggest risk is Obsidian Git pushing whatever is on disk every 15 minutes, including half-finished code and anything not ignored.

| Risk | Mitigation |
| --- | --- |
| Auto-commit pushes half-finished code or broken JSONL | Write the JSONL export atomically (temp file, then rename) and only at the end of a successful sync. Code in progress is acceptable in a private repo |
| API keys committed | `.env` gitignored before the first key exists; a check in the sync command refuses to run if `.env` is tracked |
| Store or cache ends up in git | Ignore rules applied in step 1, before phase 0 creates any store; a size check in the sync command warns if a tracked file under `50 Graph/.graphrag/` exceeds 5 MB |
| Extraction costs more than expected | Cost estimate first; spend cap in `config.yaml`; response cache so re-runs don't re-pay; pilot set before the full run |
| Generated notes clutter Obsidian search and graph | `generated: true` on every page; optionally add `50 Graph/Registry` and `50 Graph/Reports` to Obsidian's Excluded files |
| Review load is too heavy | Thresholds in config; the bootstrap review is capped at 100–150 clusters; the Review Queue is sorted by impact (mentions affected) |
| Two machines sync mid-run | Sync takes a lock file in `50 Graph/.graphrag/` and checks HEAD hasn't moved before writing |

## Extra proposals

These are not in the spec. Each is small, and Dom can drop any of them.

- **Cost estimate before phase 0** (see Before any code): turns the budget question into numbers without sending any vault text out.
- **Pilot set of 20 notes:** prompt tuning on cheap runs before the full corpus.
- **Spend cap and response cache** in the LLM client: re-runs after a crash or a config change cost nothing for unchanged inputs.
- **One CLI entry point:** `uv run graphrag <estimate|build|sync|review|eval>`, so the later query interface (MCP or skill) wraps a single tool.
- **Fixture notes in `tests/`:** small synthetic notes for each chunking edge case (nested bullets, a long code block, a table, `<mark>` across bullets), so phase 1 is tested without depending on real notes.
- **Review Queue counts in `vault-digest`** (diff 4): pending graph reviews appear in the weekly agenda.
- **Spec housekeeping:** once phase 0 picks the tokenizer and store, and whenever an open decision is settled, update the spec so it stays the source of truth.
