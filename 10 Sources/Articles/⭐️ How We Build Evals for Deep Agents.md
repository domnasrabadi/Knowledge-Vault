---
type: article
status: raw
quality: 1
topics: [agent-evaluation, evaluation-metrics]
source: https://blog.langchain.com/how-we-build-evals-for-deep-agents/
created: 2026-08-08
published: 2026-03-26
author: LangChain Blog
flashcards: none
updated: 2026-08-11
---

# How we build evals for Deep Agents

<div align="center">
  <img src="https://blog.langchain.com/content/images/2026/03/32.svg" width="220" />
</div>


## Evals shape agent behavior

- Every eval is a vector that shifts the behavior of your agentic system. For example, if an eval for efficient file reading fails, you’ll likely tweak the system prompt or the `read_file` tool description to nudge behavior until it passes. Every eval you keep applies pressure on the overall system over time.
- More evals ≠ better agents. Instead, build targeted evals that reflect desired behaviors in production.
- we take the following approach to eval curation:
  1. Decide which behaviors we want our agent to follow. Then research and curate targeted evals that measure those behaviors in a verifiable way.
  2. For each eval, add a docstring that explains *how* it measures an agent capability. This ensures **each eval is self-documenting.** We also tag each eval with categories like `tool_use` to enable grouped runs.
  3. Review output traces to understand failure modes and update eval coverage

### We group evals by what they test

- It’s helpful to have a taxonomy of evals to get a middle view of how agents perform (not a single number, not individual runs).
- Here are some categories we define and what they test:

| Category | What It Tests |
| --- | --- |
| `file_operations` | File tools (read, write, edit, ls, grep, glob), parallel invocation, pagination |
| `retrieval` | Finding information across files, search strategies, multi-hop document synthesis |
| `tool_use` | Selecting the right tool, chaining multi-step calls, tracking state across turns |
| `memory` | Recalling seeded context, extracting implicit preferences, persisting durable info |
| `conversation` | Asking clarifying questions for vague requests, sustaining multi-turn dialogue with correct actions |
| `summarization` | Handling context overflow, triggering summarization, recovering info after compaction |
| `unit_tests` | SDK plumbing - do our system prompt passthrough, interrupt config, subagent routing, skill path resolution, etc. all work? |

### Example of useful metrics around evals

- To make model comparisons actionable, we examine *how* models succeed and fail. That requires a concrete reference point for what “good” execution looks like beyond accuracy. One primitive we use is an **ideal trajectory.** This is a sequence of steps that produces a correct outcome with no “unnecessary” actions.
- For simple, well-scoped tasks, the variables are defined tightly enough that the optimal path is usually obvious. For more open-ended tasks, we approximate a trajectory using the best-performing model we’ve seen so far, then revisit the baseline as models and harnesses improve. In this way, observing agent behavior helps us refine our priors about ideal trajectories.
- **Ideal trajectory:** 4 steps, 4 tool calls, ~8 seconds ... Now compare that with a trajectory that is still technically correct, but less efficient. **Inefficient trajectory:** 6 steps, 5 tool calls, ~14 seconds. ... **Correct but inefficient trajectory:** 6 agent steps, 5 tool calls, includes an unnecessary tool call, and doesn’t parallelize tool calls.
