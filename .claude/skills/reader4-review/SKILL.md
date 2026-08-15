---
name: reader4-review
description: Review, fix, file, archive, and visually audit notes exported by the reader4 pipeline into 00 Inbox — fidelity check, formatting recovery, title polish, filing via file-note rules, reader4 mark-filed + archive, then a before/after HTML receipt. Use when reader4 export has put new notes in the Inbox.
---

# reader4-review — the one-confirmation-tap filing loop

Wraps the general `file-note` skill with reader4-pipeline-specific stages. **Scope: only notes in `00 Inbox/` that came from the reader4 pipeline** (they appear in `reader4 status` / the manifest at `~/Downloads/reader4/state/manifest.json`; match by note path/title). For any other unfiled note, use plain `file-note` instead.

Process notes one at a time, oldest first, unless the user picks one — this is the default single-note "one confirmation tap" flow (steps 0–5 below). For reviewing more than a handful of notes at once, use the batch workflow at the bottom of this file instead. All CLI calls run from `/Users/domnasrabadi/Downloads/reader4` via `uv run reader4 ...`.

## Per note

### 0. Snapshot — preserve the actual before state

Before changing the selected note, use the `reader4-diff-review` skill to snapshot it by absolute path and Reader4 `doc_id`. If snapshot creation fails, stop before editing. This snapshot is the evidence source for the final visual receipt; never reconstruct it later from memory or Git.

### 1. Pre-step — fidelity + formatting recovery (reader4-specific)

Open the note and its `source` URL context. Check and, where warranted, **propose** (never silently apply):

- **Fidelity spot-check**: reading order sane, no obvious missing/duplicated highlights, images render.
- **PDF heading promotion**: PDFs export as flat bullets (Reader stores no HTML for them). Bullets that are clearly section titles — outline-numbered (`B.`, `B.1.`, `3.2`) or bare heading words (`Terminology`, `References`) — propose promoting to `##`/`###`.
- **Code-fence restoration**: Readwise's export API flattens `<pre><code>` blocks into glued plain text. If a bullet reads like squashed code (path trees, `├──`, inline syntax), propose reconstructing a fenced code block (consult the source URL if needed).
- **Math notation restoration**: LaTeX-style math (`$I_0$`, `$s'$`) is sometimes stripped by the export, breaking sentences — restore it the same way as code fences, consulting the source if needed.
- **Broken auto-linked filenames**: X/Twitter's export auto-linkifies bare filenames mentioned in text (`SKILL.md`, `CLAUDE.md`) into dead `http://SKILL.md`-style links. Convert these to inline code.
- **Nesting fixes**: children highlighted individually render top-level. Where the text makes parent/child structure obvious (e.g. "the categories are:" followed by "Category 1/2/3" bullets), propose indenting them.
- **One idea per bullet**: when a bullet bundles 3+ distinct sentences/ideas, split it into a parent bullet (the first sentence) with the rest as indented children, wording untouched. Leave tight 2-sentence bullets alone where the second sentence is a direct continuation — don't over-split. An enumerated aside inside a bullet ("(1)... and (2)...") becomes an indented *numbered* sub-list, not more flat bullets.
- **Enumerated/numbered structure**: a full set of same-pattern items (nine dark arts, seven anti-patterns) each getting its own heading should collapse into one heading + one nested bullet list. A partial/broken numbered sequence that survived export (only items 6–7 of an original 1–7) should demote to plain bullets under the nearest natural heading — don't preserve it as orphaned numbered headings that read as arbitrary out of context.
- **Sequential vs. parallel lists**: a flat sequence of imperative steps ("Edit the training code" → "Run an experiment" → ... → "Repeat") becomes a numbered list nested under its intro line. A set of parallel thematic bullets (lessons, principles, stages) not already labeled as such gets grouped under one new parent bullet with explicit enumeration prefixes ("Lesson 1: ...").
- **Dangling empty sections**: a heading with zero content beneath it (export ended mid-article) should be proposed for removal rather than left dangling.
- **Obsidian-breaking markdown**: numbered lists must start cleanly at "1." with no stray bullet/dash before it, or Obsidian won't auto-render the numbering.

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

## Batch review workflow (multiple notes)

For anything beyond a handful of notes, don't run the single-note loop N times — use this two-stage pattern instead:

1. **Dry-run pass**: for each note, do step 0 (snapshot) and step 1 (fidelity/formatting proposals) plus the classification part of step 2, but write the proposed result to a scratch file (e.g. `~/Downloads/Reader4 Review Batch <date>/proposed/<doc_id>.md`) instead of touching the real vault note. Render the `reader4-diff-review` receipt with `--after` pointing at the scratch file. Never run `mark-filed`/`archive` in this pass.
2. **Collect feedback**: give the user the batch folder and a compact summary table (note, proposed type/topics/destination/filename, fixes applied). Wait for written feedback per note.
3. **Revision pass**: apply only the feedback given, to the scratch files, then re-render each changed receipt in place. When the user gives 2–3 concrete examples of a fix, treat that as a pattern spec, not an exhaustive list — scan the whole note for the same shape of problem and apply it consistently, not just the quoted instances.
4. **Real filing pass**: once approved, run steps 2–4 for real against each scratch file's final content — write to the vault, delete the superseded Inbox note, `mark-filed` + `archive`, then re-render the receipt against the real filed path.

Parallel subagents (one note per agent, independent scratch files) work well for the dry-run and revision passes. Be careful with the real filing pass: the reader4 CLI's manifest write is a read-modify-write of the whole `state/manifest.json` with no locking, so running `mark-filed`/`archive` concurrently across many notes can silently drop another note's update if two writes overlap. If you do run the final pass in parallel, verify every doc's final manifest status afterward and re-run `mark-filed` + `archive` for any that still show `exported` instead of `archived`.
