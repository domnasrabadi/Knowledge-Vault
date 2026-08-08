---
name: vault-lint
description: Validate the whole vault against the canonical schema and structure rules — frontmatter fields, enum values, taxonomy compliance, star/quality sync, Title Case filenames, attachment location, broken wikilinks. Use before git commits, after bulk changes, or on request.
---

# vault-lint — schema and structure enforcement

Read `AGENTS.md` for the canonical rules. Scan every `.md` note outside `.obsidian/` and report violations grouped by rule, most severe first. Only auto-fix when the fix is mechanical and unambiguous; otherwise list for the user.

## Checks

1. **Frontmatter present and complete** — every note has the canonical fields (`type`, `status`, `quality`, `topics`, `source`, `created`, `published`, `author`, `flashcards`, `updated`).
2. **Enum values valid** — `type` ∈ article|paper|book|chapter|project|system; `status` ∈ inbox|raw|structured|distilled; `flashcards` ∈ none|candidate|done; `quality` ∈ 1|2|3|empty.
3. **Topics in taxonomy** — every tag in every `topics` list exists in `40 System/Topic Taxonomy.md`. Unknown tags are violations (fix via the add-tag skill, never by silently accepting).
4. **Star/quality sync** — ⭐️ count in filename equals the `quality` field (no stars = unrated). Mechanical fix allowed.
5. **Filename conventions** — Title Case, no snake_case/kebab-case machine names, no dates/topics/status in filenames, chapter notes `N. Title.md` only inside book folders (see file-note skill for the full naming method).
6. **Dates ISO** — `created`/`published`/`updated` are `YYYY-MM-DD`. Mechanical fix allowed.
7. **Location rules** — `10 Sources/Articles|Papers` are flat (no subfolders); notes with `status: inbox` live only in `00 Inbox/` and vice versa; no notes loose at vault root except `AGENTS.md`/`CLAUDE.md`; attachments (non-md files) only in `90 Attachments/`.
8. **Broken wikilinks** — every `[[target]]` resolves to a note or an attachment in the vault. Ignore literal example links inside `40 System/Learning Methods/` PKM notes (e.g. `[[wikilinks]]`).
9. **Duplicate basenames** — flag two notes sharing a basename outside separate book folders (ambiguous wikilink targets).

## Output

A concise report: counts per rule, then the violating paths with the specific problem. Offer to apply the mechanical fixes (4, 6, plus obvious frontmatter gap-fills) in one pass after user confirmation.
