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
# GraphRAG — Start Here

The entry point for the Knowledge Vault GraphRAG project, for Dom and for any Claude session picking it up. As of 2026-10-19 the design is complete and nothing has been built.

## Index: which file to use when

| File | What it is | Use it when | It changes when |
| --- | --- | --- | --- |
| **This note** | Status, decisions so far, open decisions, working rules | Starting a session; checking where things are | After each session or phase |
| [[Knowledge Vault GraphRAG - Design Spec\|Design Spec]] | **What** the system is and **why**: graph model, schema, resolution, scoring, query pipeline, every number, open questions. The source of truth | Deciding how something should behave, or checking a rule or a number | A design decision is made or changed |
| [[Knowledge Vault GraphRAG - Implementation Plan\|Implementation Plan]] | **How and in what order** to build it: folder layout, housekeeping diffs, what to settle before code, phase-by-phase tasks, Dom's part, risks | Deciding what to do next, or working through a phase | Work progresses or a phase is finished |
| `50 Graph/.graphrag/docs/atlas.html` | A visual, interactive explainer of the spec. Not authoritative and may lag behind the spec | Getting an intuition for the design; open it in a browser (Obsidian hides the folder) | Rarely; regenerate it if it drifts |

**If the spec and the plan disagree, the spec wins.** Fix the plan.

## Reading order for a new session

1. `AGENTS.md` at the vault root: the vault's structure and rules. It is not in git, so each machine has its own copy.
2. This note.
3. The Design Spec, especially Glossary, Graph model and Open questions.
4. The Implementation Plan, from "Where things stand".

## Status

- **Done:** design spec; implementation plan; diagrams in the spec (Graphviz, rendered by the obsidian-graphviz plugin on desktop).
- **Not started:** the housekeeping diffs (plan, Proposed diffs); `50 Graph/.graphrag/` exists only for `docs/atlas.html`; no code, no store, no `.env`.
- **Next:** Dom applies the housekeeping diffs, settles the blocking decisions below, then phase 0.

## Decided

- **Code and data location:** hybrid, in the hidden `50 Graph/.graphrag/`. Code, config, prompts, tests, evaluation sets and a JSONL export of LLM outputs are tracked in git. The graph store, caches, logs and `.env` are gitignored. A clone rebuilds the store from the JSONL without LLM calls.
- **Independence groups:** a Book counts once; otherwise each note counts once. A raw note and its distilled sibling are one group. Series (e.g. the AI Evals articles) stay separate unless grouped by hand in config.
- **Voice** is not a scoring factor. Passages in Dom's own words will seed the optional worldview layer.
- **Evaluation sets:** Claude drafts them after phase 5 by sampling the built graph; Dom edits them.
- **Note count:** "about 360" is a rough estimate; 319 in-scope notes were on disk on 2026-10-19.

## Open decisions

In the order they block work. Details and options are in the spec (Open questions) and the plan (Before any code).

1. **Simplification review:** ten candidate trims to the spec. Decide first, because it shrinks phases 4–8.
2. **Storage stack:** blocks phase 0.
3. **Highlight density and voice:** the vault rarely uses `<mark>`; the proposal is to drop highlight density and set voice by note status. Blocks phase 1.
4. **Data egress:** whether vault text may go to external APIs, decided separately for LLM calls and for embeddings. Blocks phases 1 and 2.
5. **Cost ceiling:** set from the local cost estimate. Blocks phase 2.
6. **Support in ranking:** whether claim support reranks retrieval results. Phase 7.

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
