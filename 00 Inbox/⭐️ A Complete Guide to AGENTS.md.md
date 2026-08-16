---
type: article
status: inbox
quality: 1
topics: []
source: https://www.aihero.dev/a-complete-guide-to-agents-md
created: 2026-08-16
published: 
author: Matt Pocock
flashcards: none
updated: 2026-08-16
---

# A Complete Guide To AGENTS.md

<div align="center">
  <img src="https://www.aihero.dev/api/og?resource=a-complete-guide-to-agents-md&updatedAt=2026-01-18T15:01:44.364Z" width="220" />
</div>

- Maybe you should be. A bad `AGENTS.md` file can confuse your agent, become a maintenance nightmare, and cost you tokens on every request.
- An `AGENTS.md` file is a markdown file you check into Git that customizes how AI coding agents behave in your repository. It sits at the top of the conversation history, right below the system prompt.
- Think of it as a configuration layer between the agent's base instructions and your actual codebase. The file can contain two types of guidance:
    - **Personal scope**: Your commit style preferences, coding patterns you prefer
    - **Project scope**: What the project does, which package manager you use, your architecture decisions
- Every token in your `AGENTS.md` file gets loaded on **every single request**, regardless of whether it's relevant. This creates a hard budget problem: Scenario Impact Small, focused `AGENTS.md` More tokens available for task-specific instructions Large, bloated `AGENTS.md` Fewer tokens for the actual work; agent gets confused Irrelevant instructions Token waste + agent distraction = worse performance
- this means that **the ideal `AGENTS.md` file should be as small as possible.** Be ruthless about what goes here. Consider this the absolute minimum:
    - **One-sentence project description** (acts like a role-based prompt)
    - **Package manager** (if not npm; or use `corepack` for warnings)
    - **Build/typecheck commands** (if non-standard) That's honestly it. Everything else should go elsewhere.
- The ideal `AGENTS.md` is small, focused, and points elsewhere. It gives the agent just enough context to start working, with breadcrumbs to more detailed guidance. Everything else lives in progressive disclosure: separate files, nested `AGENTS.md` files, or skills. This keeps your instruction budget efficient, your agent focused, and your setup future-proof as tools and best practices evolve.
