---
name: reader4-review
description: Review, fix, file, archive, and visually audit notes exported by the reader4 pipeline into 00 Inbox — fidelity check, formatting recovery, title polish, filing via file-note rules, reader4 mark-filed + archive, then a before/after HTML receipt. Use when reader4 export has put new notes in the Inbox.
---

# reader4-review — the one-confirmation-tap filing loop

Wraps the general `file-note` skill with reader4-pipeline-specific stages. **Scope: only notes in `00 Inbox/` that came from the reader4 pipeline** (they appear in `reader4 status` / the manifest at `~/Downloads/reader4/state/manifest.json`; match by note path/title). For any other unfiled note, use plain `file-note` instead.

Process notes one at a time, oldest first, unless the user picks one. All CLI calls run from `/Users/domnasrabadi/Downloads/reader4` via `uv run reader4 ...`.

## Per note

### 0. Snapshot — preserve the actual before state

Before changing the selected note, use the `reader4-diff-review` skill to snapshot it by absolute path and Reader4 `doc_id`. If snapshot creation fails, stop before editing. This snapshot is the evidence source for the final visual receipt; never reconstruct it later from memory or Git.

### 1. Pre-step — fidelity + formatting recovery (reader4-specific)

Open the note and its `source` URL context. Check and, where warranted, **propose** (never silently apply):

- **Fidelity spot-check**: reading order sane, no obvious missing/duplicated highlights, images render.
- **PDF heading promotion**: PDFs export as flat bullets (Reader stores no HTML for them). Bullets that are clearly section titles — outline-numbered (`B.`, `B.1.`, `3.2`) or bare heading words (`Terminology`, `References`) — propose promoting to `##`/`###`.
- **Code-fence restoration**: Readwise's export API flattens `<pre><code>` blocks into glued plain text. If a bullet reads like squashed code (path trees, `├──`, inline syntax), propose reconstructing a fenced code block (consult the source URL if needed).
- **Nesting fixes**: children highlighted individually render top-level. Where the text makes parent/child structure obvious (e.g. "the categories are:" followed by "Category 1/2/3" bullets), propose indenting them.

Show proposed fixes as a short list; apply only what the user accepts. Semantic content is never rewritten — structure only.

### 2. Middle — classify and file (delegate to file-note)

Follow **file-note's Steps 2–4 and its Naming rules** exactly (read `.claude/skills/file-note/SKILL.md` — do not improvise): propose type / topics (ONLY from `40 System/Topic Taxonomy.md`; if none fits, defer to the `add-tag` skill — never invent a tag) / destination / filename in one compact summary with the fix proposals from step 1, get the user's **single confirm**, then move + rename + complete frontmatter (`status: inbox → raw`, `updated` today, ⭐️ prefix synced).

Title polish is part of this: proper Title Case, and if the title is long or unhelpful, propose a shorter more useful one (e.g. "International Network for Advanced AI Measurement, Evaluation and Science Best Practice - Automated Evaluation of Large" → "⭐️⭐️ Automated Evaluation of LLMs (INAAIMES Best Practice).md"). Book-shaped exports (`type: book`) file into `20 Books/<Book>/` as `⭐️ <Book> (Reader4 Highlights).md`.

### 3. Post-step — pipeline state (reader4-specific)

After the note is moved:

```bash
uv run reader4 mark-filed "<title or doc_id>" --path "<new absolute path>"
uv run reader4 archive "<title or doc_id>"
```

`archive` moves the **Reader document** out of Shortlist in Readwise (it refuses unless the doc is marked filed — that guard is intentional). Note: this is the `reader4` CLI, unrelated to the Readwise CLI's `reader-move-documents --location archive` — same word, different tool.

If either command errors, report it and stop — don't leave manifest state half-updated silently.

### 4. Visual receipt — render the real before/after

After the pipeline commands—or after a failure that left a partial state—use `reader4-diff-review` to generate a self-contained HTML report from the snapshot and filed note. Open it in the local browser when available and verify the summary, pipeline order, frontmatter changes, and ordered body diff. Give the user the clickable report path; do not substitute a prose summary for the artifact.

### 5. Wrap-up (after the batch)

Summarize: notes filed (old → new path), fixes applied, docs archived. `uv run reader4 log --limit 20` output can serve as the receipt.
