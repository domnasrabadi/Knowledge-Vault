---
name: reader4-diff-review
description: Generate a self-contained HTML audit report for one Reader4-reviewed vault note, comparing the snapshotted Inbox original with the filed result and showing ordered content diffs, frontmatter/path changes, fidelity signals, and Reader4 pipeline status. Use alongside reader4-review whenever a note is about to be changed, moved, marked filed, and archived, or when the user wants a visual receipt instead of a prose summary.
---

# reader4-diff-review — visual before/after receipt

Use `scripts/generate_diff_review.py` as the deterministic audit layer around `reader4-review`. The script only reads notes and the Reader4 manifest; it never edits vault notes or pipeline state. Its presentation is a single wide **Full Document Diff** view (no sidebar, no separate frontmatter table, no pipeline timeline, no fidelity gate — those are gone): a badge/title/subtitle header, a summary pill row (change groups, lines added/removed, before/after line counts, raw token similarity), then one full-width viewer with a toolbar (legend + previous/next-change navigation + sync-scroll toggle), two synchronized line-aligned before/after panes with line- and character-level highlighting, and a footer. Frontmatter changes are visible as ordinary diffed lines within the two panes, same as any other content change.

## Workflow

1. **Snapshot before mutation.** As soon as the Reader4 note is selected—and before changing frontmatter, formatting, or path—run:

   ```bash
   python3 .claude/skills/reader4-diff-review/scripts/generate_diff_review.py snapshot \
     --note "<absolute Inbox note path>" \
     --doc-id "<Reader4 doc_id>"
   ```

   Stop before editing if snapshot creation fails. Re-running `snapshot` for the same `doc_id` refuses to overwrite the original unless `--force` is explicitly supplied.

2. **Complete the approved Reader4 review.** Apply only the user-confirmed changes, move the note, then run `reader4 mark-filed` and `reader4 archive` per the `reader4-review` skill.

3. **Render the receipt.** Run this even if a pipeline command failed, so the report records the partial state:

   ```bash
   python3 .claude/skills/reader4-diff-review/scripts/generate_diff_review.py render \
     --doc-id "<Reader4 doc_id>" \
     --after "<absolute filed note path>" \
     --manifest "/Users/domnasrabadi/Downloads/reader4/state/manifest.json"
   ```

   By default the report is written to the platform temp directory under `reader4-diff-review/<doc_id>/review.html`. Pass `--output "<path>.html"` only when the user wants a persistent report; vault-persistent HTML belongs under `90 Attachments/Reader4 Reviews/`.

4. **Open and hand off.** If a local browser capability is available, open the generated `file://` URL and visually verify the summary pills, both complete document panes, the first and last change groups, exact-character highlighting, previous/next navigation, and synchronized scrolling in both directions. Confirm the two-pane layout stacks cleanly on narrow screens when responsive inspection is available. Otherwise provide the clickable HTML path. Keep the report available until the user moves to the next note.

## Report interpretation

- Read top to bottom: summary pills → complete synchronized before/after documents. Frontmatter and path changes show up as ordinary diffed lines inside the panes — there's no separate table for them.
- Read soft red/green backgrounds as line-level changes and stronger inline marks as the exact changed characters. Blank aligned rows preserve correspondence when a line exists on only one side.
- Treat the raw similarity pill as a warning signal, not proof of fidelity. Investigate unexpected drops rather than rationalizing them.
- Preserve the original snapshot. Never regenerate it from memory or from the edited note.

## Optional commands

- Use `--force` on `snapshot` only when the existing snapshot is known to be invalid and the vault note is still untouched.
- Use `show-path --doc-id "<id>"` to print the deterministic report path without rendering.
