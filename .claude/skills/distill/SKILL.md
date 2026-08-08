---
name: distill
description: Set up or assist a deep-distillation pass on a source note — creating the distilled sibling with correct naming, provenance, status, and the flashcards decision. Use when the user wants to distill a note or asks for help compressing one into their own words.
---

# distill — deep-treatment workflow with provenance rules

Distillation (rewriting/compressing a source into Dom's own words) is deliberately a **human** step — this skill handles the scaffolding and rules around it, and only drafts content when explicitly asked.

## Rules (from AGENTS.md)

- The raw/structured source note is **never replaced or deleted** — the distilled note is a sibling in the **same folder** (provenance stays adjacent).
- Naming: `⭐️ <Name> (Distilled).md` with stars matching `quality` (Title Case, per the file-note skill's naming rules).
- Frontmatter of the distilled note: same `type`/`topics`/`source`/`published`/`author` as the source, `status: distilled`, `created` today.
- Only high-value sources earn distillation (typically `quality` ≥ 2, or direct relevance to active work). If the note is quality 1/unrated, query the choice before proceeding.

## Steps

1. Confirm the source note and that it merits distillation.
2. Create the distilled sibling with correct name + frontmatter, seeded with a skeleton (headings from the source's strongest sections) — or, if asked, a draft distillation clearly marked for the user's rewrite.
3. On the source note: leave `status` as-is (it remains the raw/structured artifact).
4. **The one deliberate decision** — ask: `flashcards: candidate` (cards worth making from this) or `none`? Set it on the distilled note.
5. Timebox reminder: first pass gets one pomodoro; only standout notes earn a second (protects throughput over perfectionism).
