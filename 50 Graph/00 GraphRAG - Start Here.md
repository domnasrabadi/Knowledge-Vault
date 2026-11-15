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
# GraphRAG — Start Here

The entry point for the Knowledge Vault GraphRAG project, for Dom and for any Claude session picking it up. As of 2026-11-15 the design has been reviewed and revised, and nothing has been built.

## Index: which file to use when

| File | What it is | Use it when | It changes when |
| --- | --- | --- | --- |
| **This note** | Status, decisions so far, open decisions, working rules | Starting a session; checking where things are | After each session or phase |
| [[01 GraphRAG - Design Spec\|Design Spec]] | **What** the system is and **why**: graph model, schema, resolution, scoring, query pipeline, every number, open questions. The source of truth | Deciding how something should behave, or checking a rule or a number | A design decision is made or changed |
| [[02 GraphRAG - Implementation Plan\|Implementation Plan]] | **How and in what order** to build it: folder layout, housekeeping diffs, what to settle before code, phase-by-phase tasks, Dom's part, risks | Deciding what to do next, or working through a phase | Work progresses or a phase is finished |
| `50 Graph/.graphrag/docs/atlas.html` | A visual, interactive explainer of the spec. Not authoritative and may lag behind the spec. Last updated 2026-11-15 | Getting an intuition for the design; open it in a browser (Obsidian hides the folder) | Rarely; regenerate it if it drifts |

**If the spec and the plan disagree, the spec wins.** Fix the plan.

## Reading order for a new session

1. `AGENTS.md` at the vault root: the vault's structure and rules. It is not in git, so each machine has its own copy.
2. This note.
3. The Design Spec, especially the Revision note at the top, Glossary, Graph model and Open questions.
4. The Implementation Plan, from "Where things stand".

## Status

- **Done:** design spec; implementation plan; diagrams in the spec (Graphviz, rendered by the obsidian-graphviz plugin on desktop); a review against the vault's real numbers on 2026-11-15, applied to the spec and plan.
- **Up to date with the 2026-11-15 revision:** the six affected spec diagrams (relabelled) and the Atlas, both the offline copy and the published artifact.
- **Drafted, untested:** two of the seven prompts, in `50 Graph/prompts/`: [[P3 - Claim Extraction]] and [[P11 - Citation Support Judge]] (2026-11-15). Their examples are invented and each lists open points for Dom. The plan's layout still puts prompts in `.graphrag/prompts/`; which folder the code loads from is not decided.
- **Not started:** the housekeeping diffs (plan, Proposed diffs); `50 Graph/.graphrag/` exists only for `docs/atlas.html`; no code, no store, no `.env`.
- **Next:** Dom applies the housekeeping diffs, the cost estimate runs, then phase 0.

## Decided

- **Goal:** tool first. A usable tool early; the more ambitious layers are kept only where they measurably beat plain search (2026-11-15).
- **Code and data location:** hybrid, in the hidden `50 Graph/.graphrag/`. Code, config, prompts, tests, evaluation sets and a JSONL export of LLM outputs are tracked in git. The graph store, caches, logs and `.env` are gitignored. A clone rebuilds the store from the JSONL without LLM calls.
- **Independence groups:** a Book counts once; otherwise each note counts once. A raw note and its distilled sibling are one group. Series (e.g. the AI Evals articles) stay separate unless grouped by hand in config.
- **Voice** is not a scoring factor and is set by note status: raw and structured = `highlight`, distilled = `mine`. Highlight density is dropped (2026-11-15).
- **Data egress:** vault text may go to any hosted API, for LLM calls and embeddings. Embeddings default to a local model (2026-11-15).
- **Storage:** embedded. SQLite with FTS5, vectors in a plain array, igraph and leidenalg (2026-11-15).
- **Simplification review:** trims 1–9 applied (2026-11-15). Deferred: concept pages, relation types, taxonomy suggestions, the P13 judge, and the standalone query prompts.
- **Evaluation:** the question set is written before the graph exists (Dom's 20–30 real questions plus Claude's additions from the notes). Plain passage search is the baseline. Dom grades answers; the P13 judge is deferred (2026-11-15).
- **Review time:** minimal to moderate, and only where it measurably improves the system. New Registry entries are auto-approved, and the bootstrap review is capped at 100 items (2026-11-15).
- **Phases:** renumbered 0–6 (2026-11-15). See the plan.
- **Note count:** 326 in-scope notes, about 1M tokens, on 2026-11-15.

## Open decisions

In the order they block work. Details are in the spec (Open questions) and the plan (Before any code).

1. **Cost ceiling and model tier:** set from the local cost estimate. Blocks phase 2.
2. **Local embedding model:** Claude proposes one in phase 0. Blocks phase 1.
3. **How much scoring to keep, and support in ranking:** decided at the phase 2 exit, from the share of claims supported by 2 or more independence groups. Blocks phase 4.
4. **MindBranches voice:** are the 22 distilled MindBranches summaries Dom's own words? Blocks nothing until the worldview layer.
5. **Backfilling `published`:** 157 of 326 notes have none. Decay falls back to `created` meanwhile. Blocks nothing.
6. **Query interface:** MCP server, skill, CLI or explorer. After phase 6.

## Working rules for Claude on this project

- The spec is the source of truth. When an open decision is settled, update the spec, then the plan, then this note.
- **Ask Dom about open decisions; never guess them.**
- **Stop at every phase exit check** for Dom's review before starting the next phase.
- **Never edit notes** in `10 Sources/` or `20 Books/`. The graph reads them and writes only under `50 Graph/`.
- For `AGENTS.md`, `.gitignore` and anything in `.claude/skills/`, **propose diffs; Dom applies them.** The `.agents/skills/` mirror belongs to Dom's other agent.
- Obsidian Git commits and pushes everything every 15 minutes. **Apply the `.gitignore` diff before creating any store, cache or `.env`**, and never commit secrets.
- Edit the spec in place. It contains hand-tuned Graphviz diagrams and Dom's own edits, so never regenerate or re-export it over itself.
- Links to claude.ai in these notes only open from Dom's main account; elsewhere they are dead links and can be ignored. Everything needed to build is in these three files.
- Keep this note's Status section current at the end of each session.
