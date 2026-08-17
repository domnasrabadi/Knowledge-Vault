---
type: article
status: raw
quality: 
topics: [ai-tooling, agent-harnesses]
source: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more
created: 2026-08-09
published: 2026-06-18
author: Michael Segner
flashcards: none
updated: 2026-08-17
---

# Steering Claude Code: When to Use CLAUDE.md, Skills, Hooks, and Subagents

<div align="center">
  <img src="https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a340f852d1f938ab8675599_65a737a9.png" width="220" />
</div>


### The seven methods for delivering instructions

- CLAUDE.md files for always-on project context, rules for hard constraints, skills for reusable procedures, subagents for delegated work, hooks for deterministic automation, and output styles or system-prompt appends for global changes.

#### CLAUDE.md files

- **Always loaded**: The first type is a root CLAUDE.md file, either in a shared repository and/or saved locally for your personal preferences specific to a project.
    - All these files load at session start, and won’t get lost or degraded across long sessions.
    - When Claude Code compacts the conversation, it re-reads these files.
- **Tip:** Keep CLAUDE.md under 200 lines, give it an owner, and review changes to it like code.
- In monorepos, give each team's directory its own subdirectory CLAUDE.md

#### Rules

- [**Rules**](https://code.claude.com/docs/en/memory#organize-rules-with-claude/rules/) are markdown files in `.claude/rules/` that give Claude specific constraints or conventions.

#### Skills

- Only the name and description load at session start; the full body loads when Claude invokes the skill, either through a slash command (/code-review) or by auto-matching the task.
- On compaction, Claude Code re-injects invoked skills up to a total budget across all invoked skills.
- **Tip:** Instructions that are procedural, like deploy workflows, release checklists, or review processes, belong in a skill rather than in CLAUDE.md.

#### Subagents

- [**Subagents**](https://code.claude.com/docs/en/sub-agents) are markdown files in `.claude/agents/` that define isolated assistants for specific side tasks. Each file uses YAML frontmatter (name, description, plus optional fields for model and tool access) followed by a body that becomes that subagent's system prompt.
- Subagents are similar to skills in that the name, description, and tool list load at session start, but the larger context within the body of the agent doesn’t auto-invoke. Claude calls them via the Agent tool, passing in a prompt string.
- it never enters the parent conversation at all.
- The subagent then runs in its own fresh context window, and the only thing that returns to your main session is the subagent’s final message (often the aggregated result of many subtasks) plus metadata.
- **Tip:** That isolation is one of the main reasons to reach for a subagent instead of a skill. Use a subagent when a side task like deep search, a log analysis pass, or a dependency audit would clutter your main conversation with intermediate results you won't reference again.
- Use a skill when you want the procedure to play out inside the main thread so you can see and steer each step.

#### Hooks

- [**Hooks**](https://code.claude.com/docs/en/hooks-guide) are user-defined commands, HTTP endpoints, or LLM prompts that provide more deterministic control over Claude’s behavior by firing on [specific events in Claude’s lifecycle](https://code.claude.com/docs/en/hooks#hook-lifecycle) like file edits, tool calls, or session start.
- All hooks are deterministically triggered.
- Some hooks may have the output saved to the main context window. For example, a blocking hook's standard error is saved within context so Claude knows why the call was denied.
- **Tip:** Use hooks for anything that should happen deterministically
- Skills and hooks are also the building blocks of [designing agent loops](https://claude.com/blog/getting-started-with-loops)—repeating workflows that run until a stop condition is met.

#### Output styles

- [**Output styles**](https://code.claude.com/docs/en/output-styles) are files in `.claude/output-styles/` that inject instructions into the system prompt. They never get compacted, load at the start of every session, and are cached after the first request within a session
- Because they sit in the system prompt, output styles carry the highest instruction-following weight of any method that we've covered so far and should be used judiciously.
- **Changes to the output style will replace the default output style** (unless you set keep-coding-instructions: true in the style's frontmatter).

#### Appending the system prompt

- An alternative to modifying output styles is the `append-system-prompt` flag.
    - Whereas modifying output style files can have large, unintended changes to Claude’s behavior, the append flag is only additive to the original system prompt.
    - It doesn’t modify Claude’s role; it just adds instructions to its default role.
- Appending the system prompt can have a higher context cost compared to other methods of passing instructions. It increases input tokens, though prompt caching reduces this cost after the first request in a session.
