---
type: system
status: structured
quality:
topics: [rag, knowledge-management]
source: "https://claude.ai/code/artifact/3021e58d-e2be-4e4b-8c55-94c6ef089dfb"
created: 2026-10-04
published:
author: Dom Nasrabadi
flashcards: none
updated: 2026-10-04
---
# Knowledge Vault GraphRAG — Design Spec

Oct 4, 2026 · @Dom Nasrabadi

## Goals and scope

Build a claim-centred GraphRAG over Dom's Knowledge Vault. It answers questions with cited evidence, weighted by how strongly the vault supports each claim. The graph is a derived index: it can be rebuilt from the vault at any time, and it never edits Dom's notes. Its only writes go to `50 Graph/`.

**Question types it must answer:**

- **Global:** themes across many sources ("what patterns run through everything on agent evaluation?").
- **Local:** which source said X, with the exact passage.
- **Temporal:** how claims on a topic changed over time, and what Dom read when.
- **Connective:** what links two concepts, entities or sources.

**In scope:** notes in `10 Sources/` (Articles, Papers) and `20 Books/`, about 360 notes. This is a rough estimate, not a count; the real number changes as notes are filed. Build phases 0–8 (see Build phases), including the query pipeline.

**Out of scope for now:** `30 Projects/`, `40 System/`, the separate local personal vault, how Dom invokes the system (MCP server, skill, CLI or UI), and anything that depends on that interface, such as capturing 👍/👎 feedback.

**How to read this spec:** terms in the Glossary have exactly the meaning given there. Every number lives in Config and defaults. Prompt IDs (P1–P14) refer to the LLM prompt inventory.

## Glossary

| Term | Meaning |
| --- | --- |
| Source | One in-scope note: an article, a paper, a book cover page, or a book chapter. |
| Book | A folder in `20 Books/` that contains at least one type: chapter note. Every note in that folder belongs to the Book. Notes in other book folders (e.g. the 23 separate notes in MindBranches) are standalone sources. |
| Passage | A chunk of one source, at most 400 tokens, counted with the embedding model's tokenizer (tiktoken cl100k\_base until phase 0 picks one). Claims cite passages. |
| Voice | Who wrote a passage's text: `highlight` (inside `<mark>`), `mine` (in a `status: distilled` note), or `author` (everything else). |
| Highlight density | The share of a passage's characters inside `<mark>` tags, from 0 to 1. |
| Concept | An abstract idea, e.g. LLM-as-a-Judge or context rot. |
| Entity | A named thing: person, organisation, tool or library, model, benchmark or dataset, or paper. |
| Registry | The list of canonical concepts and entities with their aliases, stored as files in `50 Graph/Registry/`. |
| Mention | A span of passage text that names a concept or entity. |
| Claim | One self-contained assertion plus its qualifiers, extracted from one or more passages. |
| Qualifier | A condition that limits a claim, e.g. "only for pairwise comparisons". |
| Referenced time | The date or period a claim is about, when the text states one. Otherwise, the source's `published` date. |
| Volatility class | `durable`, `evolving` or `ephemeral`. Sets how fast a claim's support decays. |
| Independence group | The unit counted once when adding up support: the Book for notes in a Book folder, otherwise the source note itself. A raw note and its distilled sibling always count as one group. config.yaml can group other notes by hand (e.g. the two notes for Agentic Design Patterns). |
| Support / opposition | A claim's weighted, saturated totals of supporting and contradicting evidence. |
| Saturated | Passed through ln(1 + x), so each extra independence group adds less than the one before. |
| Contested | A claim whose opposition is large relative to its support (thresholds in Config). |
| Superseded | A claim that a newer claim explicitly replaces. It is kept, with `valid_to` set. |
| Orphaned | A claim with no remaining support. It is kept but hidden from retrieval. |
| Concept neighbourhood | All claims that share at least one ABOUT target (concept or entity). |
| NPMI | Normalised pointwise mutual information: how much more often two concepts appear in the same independence groups than chance predicts, scaled to −1 … 1. |
| Community | A cluster of concepts and entities found by graph clustering, with an LLM-written summary. |
| RRF | Reciprocal rank fusion: merges ranked lists by summing 1 / (k + rank) for each item. |
| Sync run | One run of the incremental pipeline. One sync run = one review batch. |
| Shadow graph | A separate full copy of the graph built by a re-extraction. It replaces the live graph only after Dom approves its diff. |
| Review Queue | The markdown file where Dom approves or rejects uncertain decisions. |
| MOC | Map of content: an Obsidian hub note. Here, a generated page per concept or entity. |
| Lineage | Fields on every node and edge recording how, when and by what it was made. |
| add-tag, vault-lint | Existing vault skills in `.claude/skills/`. add-tag gatekeeps the topic taxonomy; vault-lint validates note structure. |

## Source vault facts

The metadata is clean enough to use as weighting signals from day one. Note-to-note links are almost absent, so the graph must be built by extraction. Figures are from the repo as of 2026-09-27.

| Field | Values | What the graph uses it for |
| --- | --- | --- |
| `type` | article 179 · chapter 37 · book 48 · paper 54 | Source node kind; chapters grouped under their Book |
| `quality` | 3: 1 · 2: 43 · 1: 76 · unrated: \~198 | Source weight. Filename stars match `quality` in all but 3 notes |
| `status` | raw 173 · structured 106 · distilled 39 | Voice: text in a distilled note is mine |
| `topics` | \~45 kebab-case tags, closed list gatekept by add-tag | Compared with emergent communities to suggest taxonomy changes. Not an input to clustering (see Communities) |
| `published` | ISO date, often empty for papers and articles | World time: recency decay, temporal queries |
| `created` / `updated` | ISO date | Engagement time: what was read when, revisits |
| `author`, `source` | Often empty (\~half of papers) | Creates author Entity nodes; shown in citations. Not used to merge independence groups |
| `flashcards` | Always `none` today | Not used |

**Body conventions:** numbered headings, deeply nested bullets, Readwise-style `<mark>` highlights, `> [!NOTE]` callouts, code blocks, tables, and screenshot embeds.

**Links:** about 1,150 wikilinks, nearly all `![[Screenshot…]]` embeds or same-note heading links. There are effectively no links between notes.

## Graph model

Claims are the core unit. Passages support or contradict claims. Claims are ABOUT concepts and entities. Communities group concepts and entities.

*Diagram: graph model · 7 node types, claim-centred — see the [live doc](https://claude.ai/code/artifact/3021e58d-e2be-4e4b-8c55-94c6ef089dfb).*

Evidence flows upward: Source → Passage → Claim → Concept or Entity → Community. Fields for each node type are in Data schema.

| Edge | From → To | Meaning | Created by |
| --- | --- | --- | --- |
| HAS\_PASSAGE | Source → Passage | The passage is part of the source | Parser |
| IN\_BOOK | Source → Book | The chapter belongs to the book | Parser |
| MENTIONS | Passage → Concept or Entity | The passage names it | P1 + P2 |
| SUPPORTS | Passage → Claim | The passage asserts the claim | P3 + P4 |
| QUALIFIED\_SUPPORT | Passage → Claim | The passage asserts the claim only under a stated condition | P4 |
| CONTRADICTS | Passage → Claim | The passage asserts the opposite | P4 |
| ABOUT | Claim → Concept or Entity | The claim's subject | P3 |
| REFINES | Claim → Claim | A narrower or qualified version of another claim | P4 |
| SUPERSEDES | Claim → Claim | A newer claim that explicitly replaces an older one | P4 |
| INSTANCE\_OF | Entity → Concept | The entity is an example of the concept | P2 |
| CO\_OCCURS | Concept/Entity ↔ Concept/Entity | NPMI-weighted association (undirected) | Scoring job |
| Typed relation | Concept/Entity → Concept/Entity | An approved relation type, e.g. MITIGATES or ALTERNATIVE\_TO | P5 + Dom's approval |
| CONTAINS | Community → Concept or Entity | Community membership | Clustering |
| AUTHORED\_BY | Source → Entity (person) | The person wrote the source | Parser + P2, from frontmatter author |

**Entities and concepts are never merged.** An entity is linked to the concept it exemplifies by INSTANCE\_OF. For example, Graphiti INSTANCE\_OF temporal graph memory. Both are Registry entries.

**Relation types are discovered, not designed up front.** For each pair of ABOUT targets, P3 also outputs a short relation phrase ("reduces", "is an alternative to"), stored on the claim. Once 200 new phrases have built up (or monthly), phrases are embedded and clustered. A cluster with at least 5 phrases from at least 3 independence groups is named by P5 and proposed in the Review Queue. Once approved, it becomes a typed relation edge. Until then, concepts are linked only by CO\_OCCURS.

**Hierarchy comes from communities.** No broader/narrower edges are curated. Nesting comes from community levels.

**Embeddings are used alongside the graph:**

- **Passages:** entry points for retrieval and for local fact lookups.
- **Registry names and aliases:** candidate generation for mention resolution (P2).
- **Claims:** candidate generation for claim matching (P4), and a retrieval entry point.
- **Community summaries:** choosing which communities answer a global question.

**Generated content is never evidence.** Community summaries and MOC pages are generated from source content. They can steer retrieval, but they never count as support and are never cited as a source.

## Data schema

Every node and edge has a stable `id` and the lineage fields below. IDs never change once assigned, so edits, renames and re-runs don't break references.

| Node | Key fields | ID rule |
| --- | --- | --- |
| Source | path, type, status, quality, topics, source URL, published, created, updated, author, book\_id | `src:` + note path when first seen. Kept on rename (git rename detection) |
| Book | folder path, title, author, published | `book:` + folder path |
| Passage | source\_id, heading breadcrumb, ordinal, text, text\_hash, token\_count, voice, highlight\_density, embedding | `psg:` + hash of (source\_id, text\_hash, n), where n counts earlier passages in the same source with identical text. Edits elsewhere in the note don't change it |
| Concept / Entity | canonical\_name, aliases, definition, kind (`concept` or `entity`), entity\_type (person, org, tool, model, dataset, paper), status (`approved`, `pending`, `rejected`), embedding | `reg:` + kind + slug of the canonical name at creation, e.g. reg:concept:llm-as-a-judge. Renames keep the ID. On a merge, the absorbed entry's ID becomes a redirect to the survivor, its aliases move across, and its file is deleted |
| Claim | text, qualifiers, referenced\_time (start, end), volatility, status (`active`, `superseded`, `orphaned`), valid\_to, relation\_phrases, support, opposition, contested, embedding | `clm:` + UUID. On a merge, the surviving claim keeps its ID and the other ID is stored as a redirect |
| Community | level, member IDs, summary, summary\_embedding, built\_from, stale | `com:` + UUID |

Edges store `from`, `to`, `type` and `confidence`. Passage → Claim edges also store the passage weight w and its factors (see Reinforcement scoring), plus the qualifier text for QUALIFIED\_SUPPORT.

**Lineage fields (every node and edge):**

| Field | Meaning |
| --- | --- |
| `source_commit` | Vault commit the input was read from |
| `processed_at` | When it was created or last changed |
| `model` | Model ID used, if any |
| `prompt` | Prompt ID and version, e.g. `P3@v2`, if any |
| `review_state` | `auto`, provisional (awaiting review), `human_reviewed` or `manually_edited` |
| `decided_by` | Which rule or threshold decided it, or `Dom` |

Source and Book nodes need only `source_commit` and `processed_at`.

## Preprocessing

Each source becomes passages of at most 400 tokens that follow the note's own structure. Claims are extracted from every passage.

1. **Parse:** read the frontmatter. Strip Readwise image URLs and HTML wrappers, but keep `<mark>` tags.
2. **Chunk:** split on headings. If a section is over 400 tokens, split it on its top-level bullets, keeping each bullet with its children. If one bullet with its children is still over 400 tokens, split on its child bullets, then on sentences. Never split inside a code block or table. A code block or table that is over the cap on its own becomes its own passage.
3. **Annotate each passage:**
   - heading breadcrumb (e.g. Agentic GraphRAG › 3. Graph-Based Knowledge Modeling › Entity Resolution)
   - ordinal (its position in the note) and token count
   - **voice**, by precedence: text inside `<mark>` is `highlight`; any other text in a `status: distilled` note is `mine`; everything else is `author`. A passage's voice is the voice of most of its characters.
   - **highlight density**, stored separately
4. **Embed** each passage.
5. **Books:** every note in a Book folder (see Glossary) gets an IN\_BOOK edge to its Book. Notes in other book folders are standalone sources. Every source's frontmatter author is resolved to a person Entity (via P2) and linked with AUTHORED\_BY.

**Handled by the extraction prompt, not by preprocessing:**

- Boilerplate such as Readwise metadata blocks and heading-link tables of contents. P1 and P3 are told to skip it. Revisit this if the hub audit finds boilerplate turning into hubs, because embeddings and co-occurrence counts don't go through the prompt.
- Code blocks, tables and image embeds stay in the passage text as context. P3 is told not to extract claims from them.
- Dom's inline commentary in raw notes is treated as author text. It is not tagged `mine`.

## Resolution and claim matching

Every mention is resolved to a Registry entry (a concept or an entity). Every new claim is matched against existing claims. Confident decisions apply automatically, and uncertain ones go to the Review Queue.

### Mention resolution

For each mention found by P1:

1. **Exact match:** if the normalised text (lowercase; every run of spaces and punctuation other than + and # becomes one space) equals a canonical name or alias, link to it with confidence 1.0.
2. **Candidates:** otherwise, embed the mention with its passage context and take the 5 most similar Registry entries.
3. **Adjudicate (P2):** the LLM returns `match` (with the target), `new` or `unsure`, plus a confidence. It also decides concept or entity and, for an entity, proposes an INSTANCE\_OF concept.
4. **Apply:**
   - `match` at confidence 0.85 or above: link automatically, logged as reversible.
   - `match` between 0.60 and 0.85, or `unsure`: link provisionally and add a Review Queue item.
   - `new`, or below 0.60: create a `pending` Registry entry and add a Review Queue item.

Pending entries can be used straight away (claims can be ABOUT them). Dom later approves, merges or rejects them.

**Bootstrap (phase 2, once):** run mention resolution over all notes, then embed the pending entries (name plus a one-line definition) and group them with agglomerative clustering at cosine distance 0.15 or less. In each cluster, the member with the most mentions becomes the candidate canonical entry, and P2 checks every other member against it. Members matched at 0.85 or above are merged automatically, and the entry becomes approved (review\_state auto). Dom reviews the 100–150 clusters with the most mentions, plus every `unsure` item.

### Claim extraction and matching

**Claim rules (enforced by P3):** one claim is one assertion plus its qualifiers. It must stand alone (no pronouns or "this approach") and be 40 words or fewer. Each claim lists its ABOUT targets, chosen from the passage's resolved mentions (a missing target is output as a new mention and resolved by P2), a relation phrase per target pair, its referenced time, its volatility class and an extraction confidence.

**Referenced time:** when the text states the period a claim is about ("in 2023", "with GPT-4"), P3 records it. Otherwise it falls back to the source's `published` date. Decay and supersession both use referenced time, so a 2026 article reporting 2023 results is dated 2023.

**Matching (P4):** each new claim is compared with the 10 most similar claims in its concept neighbourhood. P4 returns one label plus a confidence:

| Label | What happens |
| --- | --- |
| `same` | The passage gets a SUPPORTS edge to the existing claim. The new claim is discarded. |
| `refines` | Both claims are kept. P4 says which one is narrower. If the new claim is narrower: REFINES from new to existing, and the passage SUPPORTS the new claim and gives QUALIFIED\_SUPPORT to the existing one. If the new claim is broader: REFINES from existing to new, and the passage SUPPORTS only the new claim. |
| `contradicts` | Both claims are kept. The passage SUPPORTS the new claim and CONTRADICTS the existing one. |
| `different` | The new claim is kept as is. |

P4 also returns a `supersedes` flag, which can accompany `contradicts` or `different` (never `same`). It is set when the new claim explicitly replaces the old one ("no longer", "replaced by") and has a later referenced time. It adds a SUPERSEDES edge, sets the old claim's status to `superseded`, and sets its `valid_to` to the new claim's referenced start. With `contradicts`, the CONTRADICTS edge is added as well.

A `same`, `contradicts` or `supersedes` decision with confidence below 0.7 is applied provisionally and added to the Review Queue.

## Reinforcement scoring

A claim's strength is the saturated sum of weighted support from independent source groups. Opposing evidence is kept as a separate score, never subtracted. Concept–concept edges are scored by how surprising their co-occurrence is, so generic hubs don't dominate.

### Source weight (per supporting passage)

```latex
w = q_{\text{quality}} \cdot h_{\text{highlight}} \cdot c_{\text{extract}} \cdot c_{\text{resolve}} \cdot 0.5^{\,\text{age}/T_{1/2}}
```

w is the product of five factors, one per row below. Voice is not a factor: it is shown in answers, can filter retrieval, and seeds the core worldview layer (see Optional extensions). Initial values are in Config and defaults. A claim with no referenced time and a source with no `published` date gets a decay factor of 1.0 and is flagged in answers.

**When decay is applied:** stored support and opposition leave out the decay factor. Decay is applied at query time, so scores never go stale between sync runs. Contested is also checked at query time. CO\_OCCURS weights use the stored, undecayed support.

| Factor | Source | Notes |
| --- | --- | --- |
| Quality | `quality` stars | Unrated gets a neutral default (initially 1.0, the same as ⭐); ⭐⭐ 1.5, ⭐⭐⭐ 2.0 |
| Highlight density | Passage annotation | More of the passage inside `<mark>` = more weight: factor = 1 + highlight density (1.0 to 2.0) |
| Extraction confidence | Claim extractor | How sure the LLM is that the passage asserts the claim |
| Resolution confidence | Concept and claim matcher | How sure the merge into this claim is; exact match, brand-new claim, or human-reviewed = 1.0; otherwise the P2 or P4 confidence |
| Recency decay | Referenced time + volatility class | factor = 0.5^(age / half-life). Age = today minus the referenced time (start) |

### Counting support without double-counting

- **Group weight:** for each independence group, take the largest w among its passages that support the claim. A QUALIFIED\_SUPPORT passage counts at half its w.
- **Support** = ln(1 + sum of group weights). The 10th group adds less than the 2nd.
- Sources by the same author stay separate groups. Author independence is not used. Notes in a series (e.g. the AI Evals articles) also stay separate groups, unless config.yaml groups them by hand. A raw note and its distilled sibling are one group, detected automatically from the distill skill's naming and provenance.

### Disagreement

- **Opposition** is calculated the same way, over CONTRADICTS edges. It is never subtracted from support.
- **Contested** = opposition is at least 0.3 *and* at least half of support.
- QUALIFIED\_SUPPORT edges carry their condition text, which answers show beside the claim.

### Recency decay by claim volatility

| Volatility class | Example | Half-life (initial, tunable) |
| --- | --- | --- |
| Durable | Principles, mental models | None (no decay) |
| Evolving | Practices, methods | \~2 years |
| Ephemeral | Tool or model specifics, benchmarks | \~6 months |

Superseded claims (see Claim extraction and matching) remain available for temporal questions but are left out of default retrieval.

### Hub dampening

Concepts like "LLM" or "AI agents" co-occur with almost everything. Raw co-occurrence counts would make them the strongest neighbour of every concept and swamp every traversal. Concept–concept edges are therefore weighted by **normalised PMI**: how much more often two concepts appear together than chance would predict.

```latex
\mathrm{NPMI}(a,b) = \frac{\ln \dfrac{p(a,b)}{p(a)\,p(b)}}{-\ln p(a,b)} \in [-1, 1]
```

- **Probabilities:** an independence group *mentions* a concept or entity if any of its passages has a MENTIONS edge to it. Each group has a weight g, the largest quality multiplier among its sources. p(a) = (sum of g over groups mentioning a) / (sum of g over all groups). p(a,b) is the same, over groups mentioning both.
- **Rare-pair guard:** a pair needs at least 2 independence groups in common before a CO\_OCCURS edge is created.
- **Edge weight before claims exist (phase 3):** max(0, NPMI).
- **Edge weight once claims exist (phase 4 on):** max(0, NPMI) × (1 + ln(1 + sum of support of claims ABOUT both)). Surprising *and* well-supported links rank highest.
- **Traversal damping:** at query time, the score of a path through a node is multiplied by 1 / ln(e + degree), where degree is its number of CO\_OCCURS edges.
- Hubs stay in the graph and are fully retrievable when a query names them. They are only down-weighted as bridges.

**Hub diagnosis audit (each sync).** List the 20 nodes with the highest degree, plus any node whose degree rose by more than 50% in one sync, then classify each and treat it accordingly. High degree is a diagnostic, never a deletion rule.

| Hub kind | Example | Treatment |
| --- | --- | --- |
| Legitimate central concept | AI agents, LLM evaluation | Keep; filter expansion by query and relation |
| Generic concept | data, system, model | Down-weight as a bridge |
| Category hub | a concept that hundreds of entities are INSTANCE\_OF | Use for classification only, not semantic expansion |
| Over-merged identity | two distinct things merged by mistake | Repair in the registry |
| Boilerplate | a repeated template section | Fix the extraction prompt or filter it out |

## Communities

Communities come purely from graph structure. Topic tags are not used as input; they are only compared afterwards to suggest taxonomy changes.

- **Algorithm:** hierarchical Leiden clustering over concepts and entities, using CO\_OCCURS and typed relation edges with their weights. Up to 3 levels.
- **When to re-cluster:** after any sync run that changes at least 5% of total CO\_OCCURS weight, or monthly. Otherwise the existing communities are kept.
- **Summaries (P6):** written only from the community's top claims (by support) and their passages. Each summary records the claim IDs it used in `built_from`, so it can be marked stale when those claims change.
- **Taxonomy suggestions (P8):** for each level-1 community, find the most common topic tag among its sources. If that tag covers less than 50% of the community's sources, P8 drafts a suggestion (new tag, split or merge) for the Review Queue. Approved suggestions are applied through add-tag.

## Maintenance and lineage

Each sync run processes only the notes that changed since the last indexed commit, and recomputes only what those changes affect.

**Sync run steps:**

1. Read Dom's decisions from the Review Queue and apply them (see Write-back and review).
2. Diff in-scope paths from `last_indexed_commit` to HEAD: added, modified, renamed and deleted notes. Renamed notes keep their Source ID.
3. For each added or modified note, parse and chunk it again. A passage whose `text_hash` still appears in the note keeps its ID, edges and claims, even if its position moved. Passages that no longer appear are deleted along with their edges. New passages go through P1, P2, P3 and P4.
4. For each deleted note, delete its passages and their edges.
5. If only frontmatter changed (e.g. `quality` or `status`), recompute weights. No LLM calls.
6. Mark any claim left with no support as `orphaned`.
7. Recompute support and opposition for claims whose edges changed, and CO\_OCCURS for pairs touched by changed mentions or claims.
8. Mark every derived artifact whose inputs changed as stale (see below), and regenerate it.
9. Write new Review Queue items and reports, export the JSONL snapshot (see Open questions: code and data location), then set `last_indexed_commit` to HEAD.

**Errors:** a failed LLM call is retried 3 times with backoff. If it still fails, the passage goes on a retry list and the run continues. The next sync run processes the retry list first.

**Derived-artifact dependencies:** every derived artifact (embedding, community, community summary, MOC page, cache) records the IDs it was built from. When any of them changes, the artifact is marked stale and regenerated in step 8.

**Full rebuilds** are needed only after a schema change or a new prompt or model version. They can be limited by lineage, e.g. "every claim made with `P3@v1`". They always run into a shadow graph first (see Validation and re-extraction). Lineage fields are defined in Data schema.

## Validation and re-extraction

Nothing enters the graph without passing a shape check, and no re-extraction replaces existing data without a reviewed diff.

**Post-write checks (before commit).** A claim, or a Passage → Claim edge, is rejected unless it has:

- at least one supporting passage
- complete lineage fields
- a valid volatility class
- every ABOUT target is a Registry entry (approved or pending)

Every other edge must connect two existing nodes and carry complete lineage. Rejections are written to a log, never silently dropped.

**Pre-retrieval checks.** Nodes with incomplete metadata stay retrievable but are flagged in answers. For example, about half the papers have no author or publish date. These nodes are excluded from the scoring that depends on the missing fields: for example, a source with no date gets no recency decay.

**Diff before apply.** A re-extraction (new model or prompt) is built as a shadow graph first, while the live graph keeps serving queries. Dom sees a diff (claims added, lost or changed, and support shifts) before it replaces the live graph. Human-reviewed merges and registry entries are never overwritten.

## Write-back and review

The graph writes only into `50 Graph/`, which is tracked in git so every review decision has history. Extraction skips `50 Graph/` entirely, so the graph never ingests its own output.

| Path | Contents | Who edits it |
| --- | --- | --- |
| `Registry/<kind>--<slug>.md` (e.g. `concept--llm-as-a-judge.md`) | One file per concept or entity. Frontmatter: `id`, `kind`, `entity_type`, `canonical_name`, `aliases`, `status`, `generated: true`. Body: definition and a merge-history table. | Graph writes it. Dom may edit aliases and definition; the next sync reads edits as `manually_edited`. |
| `Review Queue.md` | Pending decisions (format below). | Dom fills in decisions; the sync reads them. |
| `Review Log.md` | Decided items, appended by the sync. | Graph only. |
| `Concepts/<kind>--<slug>.md` | Generated MOC page: definition, aliases, top 10 claims by support with citations, contested claims, community, sources. Frontmatter `generated: true`. | Graph only. Overwritten on regeneration. |
| `Reports/<date>/` | Hub audit, quality metrics, and re-extraction diffs for each sync run. | Graph only. |

**Review Queue item format:**

```markdown
- [ ] RQ-0042 · merge-concept · conf 0.72
  proposal:: "LLM evaluators" → [[concept--llm-as-a-judge|LLM-as-a-Judge]]
  evidence:: 3 mentions in 2 sources; example passage psg:9f3a1c
  decision::
```

Dom writes `approve`, `reject`, or `edit: <new value>` after `decision::`. Ticking the box with no decision counts as `approve`. At the start of each sync run, decided items are applied, marked `human_reviewed`, and moved to `Review Log.md`. Undecided items stay in the queue, and their provisional links remain in effect.

**Item types:** `merge-concept`, `new-entry`, `claim-match`, `contradiction`, `supersedes`, `relation-type`, `taxonomy-suggestion`, and `re-extraction-diff` (which links to a diff report).

**What a decision does, by item type:**

| Item type | `approve` | `reject` | `edit: <value>` |
| --- | --- | --- | --- |
| merge-concept | Merge into the target (redirect, aliases move) | Keep separate. The mention is re-resolved next sync with that target excluded | Merge into the entry named in `<value>` |
| new-entry | Entry becomes `approved` | Entry `rejected`. Its mentions are unlinked and its ABOUT edges removed. Claims left with no ABOUT target are listed in the sync report | Approve with `<value>` as the canonical name |
| claim-match | Keep the provisional decision | Undo it and treat the pair as `different` | `<value>` is the correct label |
| contradiction, supersedes | Keep the edge and status change | Remove the edge and restore the old status | — |
| relation-type | Create the typed relation | Don't propose this cluster again | Approve with `<value>` as the type name |
| taxonomy-suggestion | Dom applies it via add-tag | Don't propose it again for 90 days | — |
| re-extraction-diff | Swap the shadow graph in | Discard the shadow graph | — |

vault-lint must be updated to accept `50 Graph/` and notes with `generated: true`.

## Evaluation and quality over time

Evaluation runs at the end of phases 2, 4 and 7, and after every prompt, model or schema change. No text-only retrieval baseline is used: the graph system is judged on its own.

**Datasets (Claude drafts, Dom edits):** drafted once the graph has claims (after phase 5, before phase 7). Claude samples the built graph so the sets cover many question categories and the retrieval pathways each one exercises. Dom rewrites, cuts and adds; nothing is used until Dom has edited it.

- **Fixed query set:** 40 questions spread across the categories below, each tagged with one of the four question types. At least 5 have no answer in the vault, and at least 5 involve sources that disagree.
- **Evidence labels:** for 15 of those questions, Claude proposes the passages a complete answer needs, and Dom confirms or corrects them.
- **Judge calibration set:** 60 query–answer pairs Dom labels good or bad. 40 are used to tune the judge prompt and 20 are held out.

**Question categories, in rough priority order.** Categories 5, 13 and 14 are Claude's additions to Dom's list. Examples are illustrative and not checked against the vault.

| # | Category | Example | Type | Main pathway exercised |
| --- | --- | --- | --- | --- |
| 1 | Direct factual lookup | "What should a judge rubric contain?" | Local | Passage vector + BM25 |
| 2 | Source + passage attribution | "Which source said pairwise beats Likert, and where?" | Local | Claim search → SUPPORTS → read\_source |
| 3 | Unanswerable + partly unanswerable | "What does my vault say about reward hacking in robotics?" | Any | Thin or empty channels; "not in the vault" rule |
| 4 | Disagreement + counterevidence | "Where do sources disagree on LLM judges for safety evals?" | Connective | CONTRADICTS, opposition, contested flag |
| 5 | False premise | A question that assumes a claim the vault contradicts | Any | Claim match → CONTRADICTS; answer corrects the premise |
| 6 | Focused synthesis | "Summarise what the vault says about error analysis." | Local | Concept neighbourhood → top claims |
| 7 | Conditional and scoped | "When do code-based evals beat LLM judges?" | Local | QUALIFIED\_SUPPORT, qualifiers, REFINES |
| 8 | Comparisons and trade-offs | "Graphiti vs GraphRAG for incremental updates?" | Connective | Two entity seeds, typed relations |
| 9 | Multi-hop connections | "What links context rot to agent evaluation?" | Connective | find\_paths, CO\_OCCURS with hub damping |
| 10 | Temporal: how claims changed | "How has advice on eval metrics changed since 2023?" | Temporal | Referenced-time filter, SUPERSEDES |
| 11 | Reinforcement + evidence distribution | "How well supported is X, and by how many independent sources?" | Local | Support, independence groups |
| 12 | Global synthesis | "What themes run through everything on agent evaluation?" | Global | Community summaries → top claims |
| 13 | Own voice vs authors | "What have I concluded about LLM judges, versus the sources?" | Local | Voice filter (mine vs author and highlight) |
| 14 | Alias and entity robustness | The same question asked with a different name for a concept | Local | resolve\_entity, Registry aliases |
| 15 | Temporal: reading history | "What did I read about RAG this summer, and what did I revisit?" | Temporal | created / updated metadata |
| 16 | Filtered discovery + enumeration | "List my ⭐⭐+ papers on evaluation published since 2025." | Local | Metadata filters, enumeration |
| 17 | Coverage and research planning | "Where is my vault thin on agent memory?" | Global | Low-support claims, sparse communities |

| Check | What it measures | When | Pass bar (initial) |
| --- | --- | --- | --- |
| Regression judge (P13) | Answer quality on the fixed queries, compared with the previous build | Every change | Pass rate drops by no more than 5 points. The judge is trusted only once its true-positive and true-negative rates on the held-out set are both 0.8 or higher |
| Citation support (P11) | Whether each cited passage supports its claim, on 200 sampled support edges | Phase 4, and after prompt changes | 90% or more supported |
| Resolution audit | Precision of 50 sampled auto-merges, labelled by Dom | After bootstrap, then monthly | 95% or more correct. If lower, raise the auto-link threshold |
| Exhaustiveness (P14) | Claims missed in 30 sampled passages, found by a stronger model and spot-checked by Dom | Phase 4, and after prompt changes | Recall of 0.8 or more |
| Linking rate | Share of mentions linked to approved Registry entries | Every sync run | 75% or more linked; 5% or fewer `unsure` |
| Complete-evidence recall | Share of the labelled required passages that retrieval returned | Every evaluation run | Tracked, no bar yet |
| Retrieval stats | Duplicate passages in context, context tokens, and hub contribution (share of context tokens reached through the top 1% of nodes by degree) | Every evaluation run | Tracked, no bar yet |
| Absent and conflicting cases | Whether the answer says "not in the vault" or names the disagreement, instead of making something up | Every evaluation run | 90% or more |

**Judge bias controls:** P13 grades each answer on its own (pass or fail), never pairwise. The order of the evidence shown to the judge is randomised, and Dom spot-checks 10 judgements per run.

**Optional, not committed:** a health dashboard (node growth, edge density, cluster balance, conflict rate, temporal consistency per sync run) and automatic maintenance when a metric crosses a threshold.

**Usage feedback (after the interface exists):** 👍/👎 on cited claims adjusts ranking only. It never counts as support, so repeating a claim across generated answers can't inflate it.

## Query answering

Built in phase 7. A question goes through a fixed pipeline with one bounded loop. Every step is appended to `logs/queries.jsonl`.

1. **Decompose (P9):** split the question into sub-questions. Tag each one with a question type and any time range.
2. **Retrieve** candidates for each sub-question from four channels:
   - passage vector search
   - keyword search (BM25) over passages
   - claim vector search
   - graph expansion from the concepts and entities the sub-question names, within the expansion budget in Config

   A time range filters on referenced time. Global sub-questions first search community summaries to choose communities, then take those communities' top claims.
3. **Fuse** the channel lists with RRF (k = 60), remove duplicates, and keep the top 30 items.
4. **Coverage loop (P10):** check what's still missing, such as an unanswered sub-question or a link between two concepts. If something is missing and rounds remain (at most 3), call the tools below and go back to step 3.
5. **Validate citations (P11):** check each claim–passage pair that will be cited. Drop any that fail.
6. **Synthesise (P12)** within a 12,000-token context.

**Coverage-loop tools:**

```text
search_text(query, filters, limit)        # passage search
resolve_entity(name, context)             # name → Registry entry
expand(node_id, relation_types, direction, limit)
find_paths(start_id, end_id, constraints, max_hops)
read_source(source_id, span)              # fetch exact passage text
```

**Every answer contains:**

- **The answer with citations:** each statement links to its claims and to the source note and passage.
- **Evidence labels:** for each claim, its support, number of independence groups, contested or qualified flags, and referenced time.
- **Gaps and tensions:** contradictions, weakly supported claims, and what the vault doesn't cover.

**Answer rules:**

- Absence means "not in the vault", never "false". The vault is a sample of Dom's reading. Write "your vault doesn't cover X", never "X isn't true" or "no source disagrees".
- Superseded and orphaned claims are used only when the question is about history.
- Generated content (community summaries, MOC pages) is never cited.

## LLM prompt inventory

The system needs 14 distinct prompts. Each one is a designed, versioned artifact. It lives in `prompts/<ID>_<name>.md` with a version number, a JSON output schema, and 3–5 worked examples taken from the vault. Changing a prompt bumps its version, which is recorded in lineage.

| ID | Prompt | Input | Output | Phase |
| --- | --- | --- | --- | --- |
| P1 | Mention extraction | Passage text, breadcrumb | Mentions: exact text, character offsets in the passage, concept or entity, entity\_type | 2 |
| P2 | Mention adjudication | Mention + context, top 5 Registry candidates | `match`, `new` or `unsure`; target ID; confidence; INSTANCE\_OF proposal | 2 |
| P3 | Claim extraction | Passage, its section, source metadata, the passage's resolved mentions (Registry IDs and names) | Claims: text, qualifiers, ABOUT targets, relation phrases, referenced time, volatility, confidence | 4 |
| P4 | Claim matching | New claim, top 10 neighbourhood claims | `same`, `refines`, `contradicts` or `different`; `supersedes` flag; qualifier; confidence | 4 |
| P5 | Relation-type naming | A cluster of relation phrases | Type name, definition, direction | 4 |
| P6 | Community summary | Members, top claims, passages | Summary, claim IDs used | 5 |
| P7 | Concept page writer | Registry entry, top claims | MOC page body | 5 |
| P8 | Taxonomy suggestion | Community, its tag counts | Suggested tag change and reason | 5 |
| P9 | Query decomposition | Question | Sub-questions, types, time range | 7 |
| P10 | Coverage check | Question, evidence so far | What's missing, next tool calls | 7 |
| P11 | Citation-support judge | Claim, passage | `supports`, `partial` or `no`, plus a reason | 4, 7 |
| P12 | Answer synthesis | Question, validated evidence | Answer in the format above | 7 |
| P13 | Regression judge | Question, answer, cited evidence | Pass or fail, reasons | 8 |
| P14 | Exhaustiveness check | Passage, its extracted claims | Claims that were missed | 4 |

P1 and P3 may be merged into a single call if extraction quality holds. Decide this in phase 4 by measuring.

## Config and defaults

Every number lives in a versioned `config.yaml`. These values are starting guesses, to be tuned against the evaluation checks.

| Parameter | Initial value |
| --- | --- |
| Passage cap | 400 tokens |
| Quality multiplier | unrated 1.0 · ⭐ 1.0 · ⭐⭐ 1.5 · ⭐⭐⭐ 2.0 |
| Highlight factor | 1 + highlight density |
| QUALIFIED\_SUPPORT weight | 0.5 × w |
| Half-lives | durable: none · evolving: 24 months · ephemeral: 6 months |
| Contested | opposition ≥ 0.3 and ≥ 0.5 × support |
| Mention auto-link | confidence ≥ 0.85; review band 0.60–0.85 |
| Claim-match review | confidence < 0.7 |
| Claim-match candidates | 10 |
| Rare-pair guard | 2 independence groups |
| Traversal damping | 1 / ln(e + degree) |
| Expansion budget | 2 hops · 10 neighbours per node · 5 passages per concept · 3 passages per source |
| Items after fusion | 30 |
| RRF k | 60 |
| Coverage-loop rounds | 3 |
| Synthesis context | 12,000 tokens |
| Community levels | 3 |
| Re-cluster trigger | ≥ 5% of CO\_OCCURS weight changed, or monthly |
| Relation-type promotion | ≥ 5 phrases from ≥ 3 independence groups |
| Hub audit | top 20 by degree; degree rise > 50% in one sync |
| LLM retries | 3, with backoff |

## Build phases

Phases run in order, and each one ends with an exit check. Work inside a phase can be split across subagents, e.g. one subagent per prompt or per pipeline step.

| Phase | Builds | Exit check |
| --- | --- | --- |
| 0. Setup | Choose storage, embedding model and LLMs (see Open questions). Repo layout, `config.yaml`, `prompts/`, logging | One test note runs end to end through a stub pipeline |
| 1. Parse and chunk | Source, Book and Passage nodes; voice; highlight density; passage embeddings | All in-scope notes parsed (\~360, a rough estimate); no passage over 400 tokens except a single code block or table; re-running gives identical IDs |
| 2. Registry bootstrap | P1, P2, Registry files, Review Queue; Dom reviews the top clusters | Linking rate ≥ 75%; resolution audit ≥ 95% |
| 3. Concept graph | CO\_OCCURS edges with NPMI; hub audit report | Dom has reviewed the hub audit; no boilerplate in the top 20 |
| 4. Claims | P3, P4, P5, P11, P14; support and opposition; post-write checks | Exhaustiveness ≥ 0.8; citation support ≥ 90% |
| 5. Communities and write-back | Leiden; P6, P7, P8; `Concepts/` pages | Pages render in Obsidian; vault-lint passes |
| 6. Incremental sync | Git-diff sync, dependency tracking, retry list, shadow graph with diff | Editing, renaming and deleting a test note each update the graph correctly |
| 7. Query pipeline | P9, P10, P12; retrieval channels; coverage loop; query log | All 40 fixed queries answered with valid citations |
| 8. Evaluation harness | P13; judge calibration; metrics and reports | Judge held-out TPR and TNR ≥ 0.8; first scores recorded |

After phase 8: choose the query interface, then add usage feedback.

## Open questions and deferred decisions

- [ ] **Phase 0 choices:** storage (embedded graph + vector store, Neo4j, or a GraphRAG library), the embedding model, and the extraction and judge models.
- [ ] **Data egress:** can vault text be sent to external APIs? Decide separately for (a) the LLM prompts (P1–P14) and (b) the embeddings. The options for each are a hosted API or a local model. Local LLMs would noticeably lower extraction quality.
  - [ ] **Cost ceiling:** the budget for one full extraction run over all in-scope notes, across all phases and prompts. It decides model tiers: Haiku-class for bulk extraction with stronger models only for judging, Sonnet-class for extraction, or the strongest model wherever quality depends on it.
- [ ] **Code and data location (decided 2026-10-04): hybrid.** The code, `config.yaml` and `prompts/` live in the vault and are tracked by git. The binary graph store, embeddings and `logs/` are gitignored, because Obsidian Git commits every 15 minutes and a changing binary store would bloat the repo. At the end of each sync run, the LLM outputs (registry, mentions, claims, edges) are exported as plain JSONL and committed. A fresh clone rebuilds the store from that JSONL without LLM calls, and re-embeds locally or through the API.
- [ ] **Unrated weight:** should unrated sources weigh the same as ⭐ (the current default) or less?
- [ ] **Expansion algorithm:** keep the budgets in Config and choose by evaluation, or fix one now: personalised PageRank from passage and claim seeds (HippoRAG 2), or path retrieval between seeds (PathRAG).
- [ ] **Answer context and global questions:** options are (a) evidence paths plus original passages, never summaries alone; (b) rate community relevance before reading summaries; (c) global-then-local drill-down (DRIFT); (d) spread context across communities for global questions only.
- [ ] **Query interface:** MCP server, Claude Code skill, CLI or visual explorer. Usage feedback depends on this.

**Optional extensions (no decision yet):**

- **Core worldview layer:** a compact, auto-maintained profile of Dom's most reinforced, distilled positions, seeded from passages whose voice is mine, always loaded when writing in Dom's voice.
- **Context nodes:** claims scoped to settings (regulated banking, coding agents, enterprise) as first-class nodes, so queries can be filtered by context.
- **Structured results:** paper findings stored as method × dataset × metric × result, so benchmark-style claims can be compared.
- **Merge evidence:** store why each merge matched (scores, alias hit, LLM rationale), not just a confidence number.
- **Point-in-time state:** transaction time on graph facts, to ask "what did the graph believe on date X".
- **Beliefs and outputs layers:** claims Dom has endorsed or rejected, and Dom's own written outputs, as separate layers.
- **Attribution and certainty:** tag paper sections by role (background, method, result, limitation, related work), so only a paper's own findings count as full support; record modality on each support edge (asserts, hedges, negates, reports); credit cited findings to the cited paper when it's in the vault.
- **Mention layer:** each surface-form span as its own node pointing to what it resolved to, so merge errors are cheap to repair.
- **Resolution cascade:** stable IDs (arXiv, DOI, URL), then normalised exact match, then alias candidates, then contextual LLM disambiguation. Embeddings only propose candidates.
- **Selective or lazy extraction:** full claims only for starred, distilled or highlighted passages, with cheap coverage elsewhere (KET-RAG, LazyGraphRAG). Applies if extraction cost becomes a problem.
- **Separate graph views:** distinct projections for traversal, passage navigation, community detection and category links; IDF on independent-source frequency; per-relation degree damping.

## References

The links below are as given in the literature review and have not been checked here.

- *Agentic GraphRAG*, Anthony Alcaraz (2026). Summarised in the vault at `20 Books/Agentic GraphRAG/`. Source of the claim-centred model, temporal claims, and post-write checks.
- [Microsoft GraphRAG](https://arxiv.org/abs/2404.16130): community summaries for global questions.
- [HippoRAG 2](https://arxiv.org/abs/2502.14802): personalised PageRank retrieval from passage and fact seeds.
- [PathRAG](https://arxiv.org/abs/2502.14902): retrieving relational paths between seeds.
- [Zep / Graphiti](https://arxiv.org/abs/2501.13956): temporal, incremental graph memory.
- [KET-RAG](https://arxiv.org/abs/2502.09304) and [LazyGraphRAG](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/): selective and deferred extraction.
- [DRIFT search](https://microsoft.github.io/graphrag/query/drift_search/): global-then-local drill-down.
- [RAG vs. GraphRAG evaluation](https://arxiv.org/abs/2502.11371): position bias in LLM judges.
- [CatRAG](https://arxiv.org/abs/2602.01965): query-aware edge weighting to stop drift towards hubs.
