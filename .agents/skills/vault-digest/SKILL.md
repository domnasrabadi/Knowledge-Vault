---
name: vault-digest
description: Generate a status digest of the vault by deriving state from frontmatter — inbox queue, high-quality notes awaiting treatment, stranded flashcard candidates, stale WIP. Use at the start of a PKM session or weekly to get a pre-made agenda.
---

# vault-digest — derived status report

Principle (from AGENTS.md): state is **derived, not maintained**. This skill reads frontmatter across the vault and produces one digest note — the user never bookkeeps.

## Gather

1. **Inbox queue** — notes in `00 Inbox/` (or `status: inbox`), oldest first, with a one-line gist each.
2. **Awaiting treatment** — notes with `quality` ≥ 2 still at `status: raw` (candidates for structuring/distilling), sorted by quality then age.
3. **Flashcards stranded** — notes with `flashcards: candidate` (cards promised, not yet made in RemNote).
4. **Stale WIP** — notes with `status: structured` and quality ≥ 2 whose `updated` is > 6 weeks old (started but possibly abandoned deep treatment).
5. **Vault pulse** — counts per folder and per status; new notes since the last digest (compare `created` to last digest date).

## Output

Write/overwrite `40 System/Status Digest.md` with frontmatter `type: system`, today's date, and the sections above — each item a wikilink so it's clickable in Obsidian. Lead with a 3-line "if you have 30 minutes today, do X" recommendation. Keep the whole digest scannable in under a minute; it is an agenda, not a report.
