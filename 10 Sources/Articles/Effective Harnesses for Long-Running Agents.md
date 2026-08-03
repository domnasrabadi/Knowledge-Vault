---
type: article
status: raw
quality:
topics: [ai-agents, ai-coding, context-engineering]
source: ""
created: 2025-12-12
published: 2025-11-26
author: anthropic.com
flashcards: none
updated: 2026-01-01
---

# Effective harnesses for long-running agents

<div align="center">
  <img src="https://cdn.sanity.io/images/4zrzovbb/website/32ea71b3e8e87a990f6df4c4def2b9e52815e977-2400x1260.png" width="220" />
</div>

Source: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

Exported at: `2025-12-29T04:27:39Z`

- The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before.
- Because context windows are limited, and because most complex projects cannot be completed within a single window, agents need a way to bridge the gap between coding sessions.
- We developed a two-fold solution to enable the Claude Agent SDK to work effectively across many context windows: an **initializer agent** that sets up the environment on the first run, and a **coding agent** that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session.

### The long-running agent problem

- Claude’s failures manifested in two patterns. First, the agent tended to try to do too much at once—essentially to attempt to one-shot the app. Often, this led to the model running out of context in the middle of its implementation, leaving the next session to start with a feature half-implemented and undocumented. The agent would then have to guess at what had happened, and spend substantial time trying to get the basic app working again. This happens even with compaction, which doesn’t always pass perfectly clear instructions to the next agent.
- A second failure mode would often occur later in a project. After some features had already been built, a later agent instance would look around, see that progress had been made, and declare the job done.
- This decomposes the problem into two parts. First, we need to set up an initial environment that lays the foundation for *all* the features that a given prompt requires, which sets up the agent to work step-by-step and feature-by-feature
- Second, we should prompt each agent to make incremental progress towards its goal while also leaving the environment in a clean state at the end of a session. By “clean state” we mean the kind of code that would be appropriate for merging to a main branch: there are no major bugs, the code is orderly and well-documented, and in general, a developer could easily begin work on a new feature without first having to clean up an unrelated mess.
- The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history.
