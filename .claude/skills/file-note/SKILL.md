---
name: file-note
description: File a note from 00 Inbox (or any unfiled note) into its proper vault location with canonical frontmatter, taxonomy-checked topics, and correct naming. Use whenever a note needs classifying, moving, renaming, or its frontmatter completed.
---

# file-note — file an inbox note into the vault

Read `AGENTS.md` first if you haven't this session. This skill implements the "one confirmation tap per note" filing step.

## Steps

1. **Identify the note.** Default to notes in `00 Inbox/`; the user may name any unfiled/misfiled note.
2. **Read the note** and propose, in one compact summary for the user:
   - `type`: article | paper | book | chapter | project | system
   - **destination** per type: articles → `10 Sources/Articles/`, papers → `10 Sources/Papers/`, book content → `20 Books/<Book Name>/`, project material → `30 Projects/<Project>/`, meta/PKM → `40 System/<subfolder>/`
   - `topics`: 1–5 tags, ONLY from `40 System/Topic Taxonomy.md` — read that file and validate every tag against it. Never invent a tag; if none fits, propose leaving topics sparse or invoke the add-tag skill. After picking the specific tags, re-check whether an umbrella tag (`ai-engineering`, `software-engineering`) also genuinely applies rather than defaulting to the narrowest fit only. The 1–5 cap is a soft default — if a well-justified tag list needs to exceed it, ask the user rather than silently dropping one.
   - `quality`: from Reader ⭐️ tags or existing filename stars (1–3); empty if unrated. Treat this as a proposal to confirm, not a given — once the note is actually read/reconstructed, ask whether it still feels like a keeper rather than silently carrying forward the capture-time star.
   - `author`: as the source states it. If Reader captured a bare domain/URL instead of a name (e.g. `seangoedecke.com`), check the source for the real byline.
   - **filename** per the naming rules below
3. **Wait for the user's confirm/edit** (one tap). Do not move anything before confirmation.
4. **Execute**: move + rename the file; complete the canonical frontmatter (see AGENTS.md schema) — set `status: raw` (or the user's stated level), keep `created`, set `updated` to today; sync the ⭐️ filename prefix to `quality`.
5. If the note references attachments, ensure they exist in `90 Attachments/` (move them there if they're elsewhere).

## Naming rules (mandatory)

- **Title Case, human-readable** — e.g. `Measuring Agents in Production.md`, never `measuring_agents_in_production.md`. Always rename machine-generated snake_case or kebab-case filenames to Title Case.
- Replace characters invalid or awkward in filenames: colons become ` - ` (e.g. `SCORE - Systematic Consistency and Robustness Eval for LLMs.md`).
- ⭐️ prefix mirrors `quality` exactly: 1 → `⭐️ `, 2 → `⭐️⭐️ `, 3 → `⭐️⭐️⭐️ `, unrated → no stars. Filename stars and the `quality` field must never disagree.
- Chapter notes inside a book folder keep the `N. Title.md` convention.
- Reader highlight exports filed into a book folder: `⭐️ <Book Name> (Reader4 Highlights).md`; distilled artifacts: `⭐️ <Name> (Distilled).md`.
- No dates, topics, or status in filenames — frontmatter carries those.
- Keep titles concise: shorten verbose source titles while keeping them recognizable. Default to shortening more aggressively on the first pass, especially for clickbait-shaped or platform-native hook titles — don't wait to be asked.
- If Reader captured no title (the H1/filename is literally the raw source URL), recover the real article title from the source — this is a missing-data case, not a shorten case.
- Retitling to match the note's actual content is a different move from shortening for length: when a catchy source title doesn't reflect the note's real thesis, propose a genuine rewrite and flag it as a judgment call — this is the naming change most worth a second look before filing.
- Before finalizing, check the destination folder for existing files with a near-duplicate title or overlapping subject; flag it rather than filing silently alongside it.
