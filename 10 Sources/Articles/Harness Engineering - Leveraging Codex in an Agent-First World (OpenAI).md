---
type: article
status: raw
quality:
topics: [ai-coding, context-engineering]
source: https://openai.com/index/harness-engineering/
created: 2026-08-09
published: 2026-02-11
author: openai.com
flashcards: none
updated: 2026-08-13
---

# Harness engineering: leveraging Codex in an agent-first world | OpenAI

<div align="center">
  <img src="https://images.ctfassets.net/kftzwdyauwt9/2TjayW57xam6dBbbV28sae/887861e21b8d205c2c392ec5315d3681/SEO.png?w=1600&h=900&fit=fill" width="220" />
</div>

- our team has been running an experiment: building and shipping an internal beta of a software product with **0 lines of manually-written code**.
- every line of code—application logic, tests, CI configuration, documentation, observability, and internal tooling—has been written by Codex.
- Humans steer. Agents execute.

### We started with an empty git repository

- There was no pre-existing human-written code to anchor the system. From the beginning, the repository was shaped by the agent.
- Five months later, the repository contains on the order of a million lines of code across application logic, infrastructure, tooling, documentation, and internal developer utilities.
    - Over that period, roughly 1,500 pull requests have been opened and merged with a small team of just three engineers driving Codex.
    - This translates to an average throughput of 3.5 PRs per engineer per day, and surprisingly the throughput has *increased* as the team has grown to now seven engineers.

### Redefining the role of the engineer

- The lack of hands-on human coding **introduced a different kind of engineering work, focused on systems, scaffolding, and leverage**.
- Early progress was slower than we expected, not because Codex was incapable, but because the environment was underspecified. The agent lacked the tools, abstractions, and internal structure required to make progress toward high-level goals.
- In practice, this meant working depth-first: breaking down larger goals into smaller building blocks (design, code, review, test, etc), prompting the agent to construct those blocks, and using them to unlock more complex tasks.

### Increasing application legibility

- As code throughput increased, our bottleneck became human QA capacity.
- Because the fixed constraint has been human time and attention, we’ve worked to add more capabilities to the agent by making things like the application UI, logs, and app metrics themselves directly legible to Codex.

### We made repository knowledge the system of record

- We tried the “one big [`AGENTS.md`⁠](https://agents.md/)” approach. It failed in predictable ways:
    - **Context is a scarce resource.** A giant instruction file crowds out the task, the code, and the relevant docs—so the agent either misses key constraints or starts optimizing for the wrong ones.
    - **Too much guidance becomes** ***non-guidance*****.**
        - When everything is “important,” nothing is.
        - Agents end up pattern-matching locally instead of navigating intentionally.
    - **It rots instantly.**
        - A monolithic manual turns into a graveyard of stale rules.
        - Agents can’t tell what’s still true, humans stop maintaining it, and the file quietly becomes an attractive nuisance.
    - **It’s hard to verify.** A single blob doesn’t lend itself to mechanical checks (coverage, freshness, ownership, cross-links), so drift is inevitable.
- So instead of treating `AGENTS.md` as the encyclopedia, we treat it as **the table of contents**.
- The repository’s knowledge base lives in a structured `docs/` directory treated as the system of record. A short `AGENTS.md` (roughly 100 lines) is injected into context and serves primarily as a map, with pointers to deeper sources of truth elsewhere.
- Plans are treated as first-class artifacts. Ephemeral lightweight plans are used for small changes, while complex work is captured in [execution plans⁠](https://cookbook.openai.com/articles/codex_exec_plans) with progress and decision logs that are checked into the repository.
- This enables **progressive disclosure**: agents start with a small, stable entry point and are taught where to look next, rather than being overwhelmed up front.

### Agent legibility is the goal

- our human engineers’ goal was making it possible for an agent to reason about the full business domain **directly from the repository itself.**

![](https://images.ctfassets.net/kftzwdyauwt9/7uWHsJIC6o3uQPsnQ2Avz9/8be3e321892054bd215afb2b250a176a/OAI_Harness_engineering_The_limits_of_agent_knowledge_desktop-light.png?w=3840&q=90&fm=webp)

- We learned that we needed to push more and more context into the repo over time.
- Giving Codex more context means organizing and exposing the right information so the agent can reason over it, rather than overwhelming it with ad-hoc instructions.

### Enforcing architecture and taste

- Agents are most effective in environments with [strict boundaries and predictable structure⁠](https://bits.logic.inc/p/ai-is-forcing-us-to-write-good-code), so we built the application around a rigid architectural model. Each business domain is divided into a fixed set of layers, with strictly validated dependency directions and a limited set of permissible edges.
- In practice, we enforce these rules with custom linters and structural tests, plus a small set of “taste invariants.” For example, we statically enforce structured logging, naming conventions for schemas and types

### Throughput changes the merge philosophy

- As Codex’s throughput increased, many conventional engineering norms became counterproductive.
- The repository operates with minimal blocking merge gates.
    - Pull requests are short-lived.
    - Test flakes are often addressed with follow-up runs rather than blocking progress indefinitely.

### What “agent-generated” actually means

- When we say the codebase is generated by Codex agents, we mean everything in the codebase. Agents produce:
    - Product code and tests
    - CI configuration and release tooling
    - Internal developer tools
    - Documentation and design history
    - Evaluation harnesses
    - Review comments and responses
    - Scripts that manage the repository itself
    - Production dashboard definition files
- When the agent struggles, we treat it as a signal: identify what is missing—tools, guardrails, documentation—and feed it back into the repository, always by having Codex itself write the fix.

### Entropy and garbage collection

- **Full agent autonomy also introduces novel problems.**
    - Codex replicates patterns that already exist in the repository—even uneven or suboptimal ones.
    - Over time, this inevitably leads to drift.
- Initially, humans addressed this manually.
    - Our team used to spend every Friday (20% of the week) cleaning up “AI slop.”
    - Unsurprisingly, that didn’t scale.
- Instead, we started encoding what we call “golden principles” directly into the repository and built a recurring cleanup process.
- These principles are opinionated, mechanical rules that keep the codebase legible and consistent for future agent runs.
- For example:
    1. we prefer shared utility packages over hand-rolled helpers to keep invariants centralized
    2. we don’t probe data “YOLO-style”—we validate boundaries or rely on typed SDKs so the agent can’t accidentally build on guessed shapes
    - On a regular cadence, we have a set of background Codex tasks that scan for deviations, update quality grades, and open targeted refactoring pull requests.
- Technical debt is like a high-interest loan: it’s almost always better to pay it down continuously in small increments than to let it compound and tackle it in painful bursts. Human taste is captured once, then enforced continuously on every line of code.
