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
updated: 2026-11-15
---
# Knowledge Vault GraphRAG — Implementation Plan

How and in what order to build what the [[01 GraphRAG - Design Spec|design spec]] describes. The spec says what the system is and why; this plan says what to do next. If they disagree, the spec wins. Status and orientation live in [[00 GraphRAG - Start Here]].

## Where things stand

As of 2026-11-15 the design has been revised after a review against the vault's real numbers, and nothing is built. The spec is at `50 Graph/01 GraphRAG - Design Spec.md`. No code exists yet, `50 Graph/.graphrag/` holds only `docs/atlas.html`, and none of the housekeeping diffs below have been applied.

What the review changed in this plan:

- **A usable tool after phase 1.** Passage search plus an answering agent is both the first tool and the baseline every later layer must beat.
- **The question set comes first**, written from Dom's real questions and the notes, not sampled from the built graph.
- **Phases renumbered 0–6.** The pilot is its own phase and ends in a decision. The query-pipeline and evaluation-harness phases are gone.
- **Simplification trims 1–9 are applied**, so P5, P7, P8, P9, P10, P12 and P13 are deferred.

Next steps, in order:

1. Dom reviews and applies the housekeeping diffs (`.gitignore`, `AGENTS.md`, vault-lint, vault-digest).
2. Run the local cost estimate; Dom picks the model tier and the cost ceiling.
3. Build phases 0–6 in order, stopping at each exit check for Dom's review.

## Proposed layout

Code goes in a dot-folder inside the graph's own folder: `50 Graph/.graphrag/` (decided 2026-10-19). Obsidian hides dot-folders wherever they are, so the Python files, JSONL and prompt files stay out of search, the graph view and vault-lint's folder rules. It is still tracked and cloned with the vault, which is what the hybrid decision needs, and everything the graph writes sits under `50 Graph/`. The only cost is quoting the space in "50 Graph" in shell commands.

```text
Knowledge Vault/
└── 50 Graph/
    ├── 00 GraphRAG - Start Here.md
    ├── 01 GraphRAG - Design Spec.md
    ├── 02 GraphRAG - Implementation Plan.md
    ├── Review Queue.md, Review Log.md
    ├── Reports/<date>/             hub audit, metrics, re-extraction stats diffs
    ├── Concepts/                   MOC pages, generated: true (deferred)
    └── .graphrag/                  code home (hidden), tracked unless marked
        ├── docs/atlas.html         visual explainer; open in a browser
        ├── pyproject.toml, uv.lock
        ├── config.yaml             every tunable number, the exclude list, group overrides
        ├── registry_overrides.yaml Dom's edits to aliases and definitions
        ├── prompts/                P1, P2, P3, P4, P6, P11, P14
        ├── src/vault_graphrag/     parse, chunk, resolve, claims, score,
        │                           communities, sync, tools, eval
        ├── tests/                  unit tests + fixture notes
        ├── eval/                   query set, evidence labels, Dom's grades
        ├── export/                 registry.jsonl + one sorted JSONL per source note,
        │                           committed each sync
        ├── store/                  SQLite store + vectors          (gitignored)
        ├── cache/                  LLM response cache, embeddings  (gitignored)
        ├── logs/                   queries.jsonl, run logs         (gitignored)
        └── .env                    API keys                        (gitignored)
```

The Registry is data in `export/registry.jsonl`, not a folder of notes (changed 2026-11-15). The spec's query log is `.graphrag/logs/queries.jsonl`. A plain, non-dot subfolder would not work: its files would show up in Obsidian and fail vault-lint.

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
+| `50 Graph/` | Output of the GraphRAG index: its design spec, implementation plan, Review Queue and Log, reports, and (later) generated concept pages. Engine code and the Registry live in the hidden `50 Graph/.graphrag/`. | Written by the graph pipeline. Dom edits only Review Queue decisions |
```

Frontmatter rules: add a bullet.

```diff
+- **Generated notes** (`generated: true`, in `50 Graph/Concepts/`) use the graph's own frontmatter, not this schema. Don't hand-edit them.
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
+A claim-centred graph over `10 Sources/` and `20 Books/`. Start at `50 Graph/00 GraphRAG - Start Here.md`. Spec: `50 Graph/01 GraphRAG - Design Spec.md`. Engine: `50 Graph/.graphrag/`.
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
+**Graph exemptions.** Notes with `generated: true` (`50 Graph/Concepts/`) and `50 Graph/Review Queue.md` and `Review Log.md` skip checks 1–5 and 9. Their kebab-case `<kind>--<slug>.md` names are intended. Wikilinks in them are still checked (8).
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

Most of the decisions that blocked code were settled on 2026-11-15. The full list is under Open questions in the spec.

| Decision | State | Blocks |
| --- | --- | --- |
| Simplification review | **Decided:** trims 1–9 applied | — |
| Storage stack | **Decided:** embedded. SQLite with FTS5, vectors in a plain array, igraph and leidenalg | — |
| Highlight density and voice | **Decided:** density dropped; voice set by note status | — |
| Data egress | **Decided:** any hosted API is allowed. Embeddings still default to a local model | — |
| Cost ceiling and model tier | Open. Set from the estimate below | Phase 2 |
| Local embedding model | Open. Claude proposes one in phase 0 | Phase 1 |
| MindBranches voice | Open. Are the 22 distilled MindBranches summaries Dom's own words? | Nothing until the worldview layer |
| Backfilling `published` | Open. 157 of 326 notes have none; decay falls back to `created` meanwhile | Nothing; improves decay and temporal queries |
| How much scoring to keep | Open. Decided at the phase 2 exit from the multi-group support share | Phase 4 |
| Support in ranking | Open. Decide after the pilot | Phase 4 |
| Expansion algorithm, answer context | Open. Leave until phase 5 evaluation | Phase 5 |
| Unrated weight | Open. Keep the default (1.0) and tune in evaluation | Nothing |
| Query interface | Open. Leave until after phase 6 | Nothing |

**Cost estimate (step 0):**

1. A script parses and chunks every in-scope note, using the phase 1 chunker in draft form. Nothing leaves the machine.
2. It counts notes, passages and tokens, and the expected calls per prompt:
   - P1: one call per passage.
   - P2: one call per mention that has no exact match. This is highest at the start, when the Registry is empty; the rate is an assumption in config, refined after the pilot.
   - P3: one call per note, or per top-level section for long notes.
   - P4: one call per claim cluster on the first build (per claim on incremental sync). Claims per note is an assumption in config, refined after the pilot.
   - P6, P11 and P14 on their samples and communities.
3. It prices one full run at three model tiers, using current prices checked at the time and batch pricing where the step can be batched, and adds one re-extraction.
4. Dom picks the tier and sets the ceiling. The ceiling goes into `config.yaml` as a hard stop: a run halts when spend reaches it.

The corpus is about 1M tokens, so the expectation is tens to low hundreds of dollars for a full run at a mid-tier model. That figure is a guess until the script runs.

## Step-by-step build

Each phase ends at its spec exit check, and Claude stops there for Dom's review before starting the next. From phase 4 on, a layer must beat the previous one on the fixed queries. If it doesn't, Dom decides whether to fix it or drop it.

| Phase | Tasks | Dom's part | Exit check |
| --- | --- | --- | --- |
| 0. Setup | `uv` project in `50 Graph/.graphrag/`; `config.yaml` with every spec default; SQLite store with FTS5; local embedding model; prompt file template (version, JSON schema, examples); `runs` table and logging; LLM client with retries, response cache and the spend cap; stub pipeline | Apply the diffs; add API keys to `.env`; pick the tier and ceiling from the estimate | One test note runs end to end through the stub |
| 1. Parse, chunk and baseline | Frontmatter parser; heading, bullet and sentence chunker that keeps code blocks and tables whole; voice by note status; exclude list; Book detection and IN\_BOOK; independence groups (Book, raw + distilled pairs, config overrides); stable IDs; passage embeddings and BM25; `search_text` and `read_source` as CLI tools; the fixed query set; baseline answers from an agent using only those two tools | Write 20–30 real questions; edit Claude's additions; spot-check 10 notes' passages; grade the baseline answers | All in-scope notes parsed; no passage over 400 tokens except a lone code block or table; re-runs give identical IDs; baseline graded |
| 2. Pilot | Pick 20 notes from one topic cluster (e.g. LLM evaluation), so claims from different sources can overlap, covering raw, structured and distilled notes and at least one Book; P1 and P2 with vault examples; P3 per note; P4; tune prompts; P11 and P14 samples; measure the multi-group support share | Spot-check P14 misses; decide how much scoring to keep and whether support enters ranking | Exhaustiveness ≥ 0.8 and citation support ≥ 90% on the pilot; scoring decision made |
| 3. Registry, full corpus | Exact-match normaliser; candidate search; full P1 and P2 run; clustering and auto-merge; Registry export; `registry_overrides.yaml` reader; Review Queue writer and reader; resolution audit sampler; `resolve_entity` tool | Review up to the review budget (100 items, biggest first); label 50 auto-merges | Linking rate ≥ 75%; resolution audit ≥ 95% |
| 4. Claims, full corpus | P3 over every note; claim embeddings; cluster-then-adjudicate matching with P4; supersession; support and opposition; post-write checks and rejection log; claim search tool; rerun the fixed queries | Grade the answers against the baseline | Exhaustiveness ≥ 0.8; citation support ≥ 90%; beats the baseline |
| 5. Concept graph and communities | Section-level co-occurrence; weighted NPMI with the rare-pair guard of 3; CO\_OCCURS edges; one hub audit; one-level Leiden; P6 summaries with `built_from`; `expand`, `find_paths` and community search tools; rerun the fixed queries | Classify the top-20 hubs; grade the connective and global answers | Hub audit reviewed; no boilerplate in the top 20; beats phase 4 on connective and global queries |
| 6. Sync | Git-diff sync (adds, edits, renames, deletes); passage reuse by `text_hash`; sequential P4 for new claims; full recompute of non-LLM steps; retry list; rebuild into a new store file with a stats diff; per-source JSONL export; one `sync` command | Approve a test re-extraction diff | Edit, rename and delete of a test note each update the graph correctly |

After phase 6: choose the query interface. Then, as needed, the deferred items: concept pages (P7), relation types (P5), taxonomy suggestions (P8), the P13 judge, standalone query prompts (P9, P10, P12) and usage feedback.

## Risks and mitigations

The biggest risk is Obsidian Git pushing whatever is on disk every 15 minutes, including half-finished code and anything not ignored.

| Risk | Mitigation |
| --- | --- |
| The graph layers don't beat plain search | The phase 1 baseline and the "beats the baseline" exit checks. A layer that fails is fixed or dropped before anything is built on it |
| Support separates too few claims to matter | The multi-group support share is measured in the pilot, before the full run is paid for |
| Auto-commit pushes half-finished code or broken JSONL | Write the JSONL export atomically (temp file, then rename) and only at the end of a successful sync. Code in progress is acceptable in a private repo |
| API keys committed | `.env` gitignored before the first key exists; a check in the sync command refuses to run if `.env` is tracked |
| Store or cache ends up in git | Ignore rules applied in step 1, before phase 0 creates any store; a size check in the sync command warns if a tracked file under `50 Graph/.graphrag/` exceeds 5 MB. The export is one file per source note, so no single file should come near that |
| Extraction costs more than expected | Cost estimate first; spend cap in `config.yaml`; response cache so re-runs don't re-pay; pilot before the full run |
| Generated notes clutter Obsidian search and graph | The Registry is data, not notes; concept pages are deferred and limited to entries with 3 or more groups; optionally add `50 Graph/Reports` to Obsidian's Excluded files |
| Review load is too heavy | New entries are auto-approved; only merges and `unsure` links are queued; the bootstrap review is capped by the review budget; the Review Queue is sorted by impact (mentions affected) |
| Two machines sync mid-run | Sync takes a lock file in `50 Graph/.graphrag/` and checks HEAD hasn't moved before writing |

## Extra proposals

These are not in the spec. Each is small, and Dom can drop any of them.

- **Cost estimate before phase 0** (see Before any code): turns the budget question into numbers without sending any vault text out.
- **Spend cap and response cache** in the LLM client: re-runs after a crash or a config change cost nothing for unchanged inputs.
- **One CLI entry point:** `uv run graphrag <estimate|build|sync|search|review|eval>`, so the later query interface (MCP or skill) wraps a single tool.
- **Fixture notes in `tests/`:** small synthetic notes for each chunking edge case (nested bullets, a long code block, a table), so phase 1 is tested without depending on real notes.
- **Review Queue counts in `vault-digest`** (diff 4): pending graph reviews appear in the weekly agenda.
- **Spec housekeeping:** whenever an open decision is settled, update the spec so it stays the source of truth.
