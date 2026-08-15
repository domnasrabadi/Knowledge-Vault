---
type: article
status: raw
quality: 1
topics: [ai-agents, prompting, agent-evaluation]
source: https://x.com/AlphaSignalAI/status/2069064122218717387/?rw_tt_thread=True
created: 2026-08-09
published: 2026-06-22
author: AlphaSignal AI
flashcards: none
updated: 2026-08-13
---

# How Your Agents Can Write and Optimize Their Own Skills

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2014100845189529600/Ff1Xc28-.jpg" width="220" />
</div>

- the quality of the agent hinges largely on the skills that you give them.
- It outlines the instructions, tool-use guidelines, formatting requirements, and failure-recovery logic that the agent should adhere to.
- unlike the underlying model, the skill document can’t be trained like a machine learning model. It lacks differentiable parameters, meaning you cannot calculate an exact gradient to guide updates.

### The fundamental challenge of skill optimization

- Tweaking textual instructions in skill files can also cause downstream problems. When you edit a markdown file to fix a brittle behavior in long-horizon Task A, you might cause a regression in Task B.
- Without systematic tracking, it is nearly impossible to pinpoint the causal effect of individual textual changes.
- Engineers are now building optimization loops that treat the skill document as a trainable external state.

### SkillOpt: a structured text-space optimizer

- Microsoft Research, SkillOpt treats text documents exactly like neural network parameters.
- The SkillOpt training pipeline operates via a structured loop:
    - **Rollout:** The system executes a batch of tasks and records their execution trajectories.
    - **Evaluation:** Trajectories receive a success or failure score from a verifier.
    - **Reflection:** A separate LLM optimizer analyzes the minibatches of these trajectories to identify specific text components driving failures.
    - **Bounded edits:** The optimizer proposes specific add, delete, or replace modifications. A textual learning-rate budget limits the scope of these edits to prevent volatile changes.

### GEPA

- Beyond bounded edits on a single text file, other frameworks approach skill optimization through evolutionary programming and multi-agent synthesis. GEPA (Genetic-Pareto) is an optimization framework that uses evolutionary algorithms to improve the instructions given to LLMs.
- When an agent carries out a task, GEPA uses an LLM (it can be the same one that powers the agent) to reflect on the reasoning trace, diagnose failures, and propose different “mutations” of the original artifact.
- GEPA explores these different paths through “Pareto-based selection,” where it creates a list of top-candidates that perform well on different tasks.

### EvoSkill

- EvoSkill is a new framework that uses the idea of GEPA to discover and synthesize skills for multi-agent coding workflows. EvoSkill uses the same fundamental idea as SkillOpt: an optimization loop that analyzes execution traces, finds error patterns and proposes fixes.
- EvoSkill keeps track of multiple skill candidates simultaneously, keeping them on separate Git branches and using a Pareto frontier to select the highest-performing variants.
- EvoSkill evaluates a branch on a held-out dataset. If the pagination accuracy surpasses the baseline, this version replaces the lowest-performing variant on the active Pareto frontier.

### Trade-offs, costs, and practical considerations

- Automated text-space optimization requires structural prerequisites. Systems like SkillOpt and EvoSkill cannot function on subjective, completely open-ended tasks.
- They require a verifiable feedback signal and a clean, representative held-out evaluation dataset.
- The main idea of loop engineering is to create a repeatable cycle with a well-defined and verifiable goal, and letting an LLM or AI agent repeat the task until it archives optimal performance.
