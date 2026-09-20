---
name: add-tag
description: Gatekeeper for the topic taxonomy — evaluate a proposed new topic tag, and only if justified add it to Topic Taxonomy.md before it is ever used on a note. Use whenever a tag is wanted that isn't already in the taxonomy, or to rename/merge existing tags.
---

# add-tag — controlled-vocabulary gatekeeper

The taxonomy at `40 System/Topic Taxonomy.md` is a **closed list**: a tag not in that file is invalid, full stop. This skill is the only sanctioned way to change the list.

## Evaluating a proposed tag

1. **Check overlap first.** Read the full taxonomy. If an existing tag substantially covers the concept, use that tag instead and say so — most requests end here. Pay attention to the "Deliberately excluded" section: those were rejected on purpose (e.g. `agentic-systems` → use `ai-agents`; `benchmarks` → use `llm-evaluation`).
2. **Apply the 3+ rule.** Search the vault: would the tag genuinely apply to 3+ existing notes? Fewer → reject; the concept belongs in note bodies, not the taxonomy.
3. **Check altitude.** Prefer higher-level abstractions; a tag narrower than its cluster siblings (e.g. per-tool, per-algorithm) is usually wrong.
4. **Format**: kebab-case, concise, consistent with existing names.

## If approved (confirm with the user before editing)

1. Add the tag to the correct cluster table in `Topic Taxonomy.md` with a one-line scope definition.
2. If renaming/merging existing tags: update the scope tables, add a row to the legacy-mapping table, and update `topics` frontmatter in all affected notes.
3. Only then apply the tag to notes.

## If rejected

Tell the user which existing tag to use instead and why, or that the concept is below the 3-note threshold.
