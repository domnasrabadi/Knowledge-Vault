---
type: article
status: inbox
quality: 
topics: []
source: https://addyosmani.com/blog/agent-harness-engineering/
created: 2026-09-06
published: 2026-04-19
author: Addy Osmani
flashcards: none
updated: 2026-09-06
---

# Agent Harness Engineering

<div align="center">
  <img src="https://addyosmani.com/assets/images/agent-harness.jpg" width="220" />
</div>

- A decent model with a great harness beats a great model with a bad harness.

### What is a harness, really?

- Agent = Model + Harness. If you’re not the model, you’re the harness.
- A raw model is not an agent. It becomes one once a harness gives it state, tool execution, feedback loops, and enforceable constraints.
- Concretely, a harness includes:
    - System prompts, `CLAUDE.md`, `AGENTS.md`, skill files, and subagent prompts
    - Tools, skills, MCP servers, and their descriptions
    - Bundled infrastructure (filesystem, sandbox, browser)
    - Orchestration logic (subagent spawning, handoffs, model routing)
    - Hooks and middleware for deterministic execution (compaction, continuation, lint checks)
    - Observability (logs, traces, cost and latency metering)
- [Simon Willison](https://simonwillison.net/2025/Sep/30/designing-agentic-loops/) reduces the loop part to its essence: an agent is a system that *“runs tools in a loop to achieve a goal.”* The skill is in the design of both the tools and the loop.
- On Terminal Bench 2.0, Claude Opus 4.6 running inside Claude Code scores far lower than the same model running in a custom harness.
- Models get post-training coupled to the harness they were trained against. Moving them into a different harness, with better tools for your codebase, a tighter prompt, and sharper back-pressure, can unlock capability the original harness was leaving on the floor.

### Working backwards from behaviour

- specific patterns I’ve found worth stealing.

#### Filesystem and Git: durable state

- The filesystem is the most foundational primitive, and it tends to be underrated because it’s boring.
- Once you have a filesystem, the agent gets a workspace to read data, code, and docs;
- surface where multiple agents and humans can coordinate through shared files.

#### Bash and code execution: the general-purpose tool

- main agent loop today is a ReAct loop: the model reasons, takes an action via a tool call, observes the result, and repeats.
- But a harness can only execute the tools it has logic for.
- You can try to pre-build a tool for every possible action, or you can give the agent bash and let it build the tools it needs on the fly.
- agents already excel at shell commands; most tasks collapse to a few well-chosen CLI invocations.
- Harnesses still ship focused tools, but bash plus code execution has become the default general-purpose strategy for autonomous problem solving.

#### Sandboxes and default tooling

- Bash is only useful if it runs somewhere safe. Running agent-generated code on your laptop is risky, and a single local environment doesn’t scale to many parallel agents.
- Sandboxes give agents an isolated operating environment. Instead of executing locally, the harness connects to a sandbox to run code, inspect files, install dependencies, and verify work.
- can allow-list commands, enforce network isolation, spin up new environments on demand, and tear them down when the task is done.
- A good sandbox ships with good defaults: pre-installed language runtimes and packages, Git and test CLIs, a headless browser for web interaction.

#### Memory and search: continual learning

- The filesystem is again the primitive. Harnesses support memory file standards like `AGENTS.md` that get injected on every start. As the agent edits that file, the harness reloads it, and knowledge from one session carries into the next. This is a crude but effective form of continual learning.
- Context rot is the observation that models get worse at reasoning and completing tasks as the context window fills up.
- Three techniques show up repeatedly:
- **Compaction.** When the window gets close to full, something has to give.
- so the harness intelligently summarizes and offloads older context so the agent can keep working.
- **Tool-call offloading.** Large tool outputs (think 2,000-line log files) clutter context without adding much signal. The harness keeps the head and tail tokens above a threshold and offloads the full output to the filesystem, where the agent can read it on demand.
- **Skills with progressive disclosure.** Loading every tool and MCP into context at startup degrades performance before the agent takes a single action.
- Anthropic’s harness post adds one more technique for the really long jobs: full context resets, where the harness tears the session down and rebuilds it from a compact hand-off file.

#### Long-horizon execution: Ralph Loops, planning, verification

- Autonomous long-horizon work is the holy grail and the hardest thing to get right.
- Today’s models suffer from early stopping, poor decomposition of complex problems, and incoherence as work stretches across multiple context windows.
- The harness has to design around all of that.
- autonomous coding loops like the Ralph Loop
- but it’s worth restating in this framing: a hook intercepts the model’s attempt to exit and re-injects the original prompt into a fresh context window, forcing the agent to continue against a completion goal.
- Each iteration starts clean but reads state from the previous one through the filesystem. It’s a surprisingly simple trick for turning a single-session agent into a multi-session one
- **Planning** is when the model decomposes a goal into a sequence of steps, usually into a plan file on disk.
- harness supports this with prompting and reminders about how to use the plan file.
- After each step, the agent checks its work via self-verification: hooks run a pre-defined test suite and loop failures back to the model with the error text, or the model reviews its own output against explicit criteria.

#### Hooks: the enforcement layer

- A hook is a script that runs at a specific lifecycle point: before a tool call, after a file edit, before commit, on session start.
- `AGENTS.md` and tool choice
- The flat markdown rulebook at the root of your repo is still the single highest-leverage configuration point, because it lands in the system prompt every turn.
- Keep it short. HumanLayer keeps theirs under 60 lines.
- Earn each line. Rules should trace to a specific past failure or a hard external constraint.
- Same discipline applies to tools.
- Each tool’s name, description, and schema gets stamped into the prompt every request. Ten focused tools outperform fifty overlapping ones because the model can hold the menu in its head.

### Harnesses don’t shrink, they move

- One of the better observations in the Anthropic write-up is that as models improve, the space of interesting harness combinations doesn’t shrink. It moves.
- If the model is coherent at long horizons, no context resets. And yes, Opus 4.6 largely killed the context-anxiety failure mode
- But the ceiling moved with the model. Tasks that were unreachable are in play, and they have their own failure modes.
- Anthropic puts it cleanly: *“every component in a harness encodes an assumption about what the model can’t do on its own.”* When the model gets better at something, that component becomes load-bearing for nothing and should come out.
- When the model unlocks something new, new scaffolding is needed to reach the new ceiling.
- **A harness is a living system, not a config file you set up once.** And the “best” harness isn’t necessarily the one the model was trained inside; it’s the one designed for your task.

### Harness-as-a-Service

- Claude Agent SDK, the Codex SDK, and the OpenAI Agents SDK all point in the same direction. You get the loop, the tools, the context management, the hooks, and the sandbox primitives out of the box, and you customize them.
