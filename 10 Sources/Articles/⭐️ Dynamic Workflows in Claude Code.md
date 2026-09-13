---
type: article
status: raw
quality: 1
topics: [agent-harnesses, context-engineering, ai-coding]
source: https://x.com/trq212/status/2061907337154367865/?s=12&rw_tt_thread=True
created: 2026-09-06
published: 2026-06-02
author: Thariq
flashcards: none
updated: 2026-09-13
---

# Dynamic Workflows in Claude Code

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1976939058741039104/r3GgzqRh.jpg" width="220" />
</div>

- we released [dynamic workflows](https://code.claude.com/docs/en/workflows) in Claude Code.
    - Claude can now write its own [harness](https://code.claude.com/docs/en/glossary#agentic-harness) on the fly, custom-built for the task at hand.
    - there are certain classes of tasks where we have had to build custom harnesses on top of Claude Code to achieve peak performance such as [Research](https://support.claude.com/en/articles/11088861-using-research-on-claude), [security analysis](https://support.claude.com/en/articles/11932705-automated-security-reviews-in-claude-code), [agent teams](https://code.claude.com/docs/en/agent-teams), or [Code Review](https://code.claude.com/docs/en/code-review).
    - You can also share and re-use these workflows with others.
- some example prompts to get you thinking about the possibilities with workflows:
    - "This test fails maybe 1 in 50 runs. Set up a workflow to reproduce it, form theories and adversarially test them in worktrees /goal don't stop until one theory works."
    - "Using a workflow, go through my last 50 sessions and mine them for corrections I keep making and turn the recurring ones into `CLAUDE.md` rules"
    - "Take my business plan and run a workflow where different agents tear it apart from an investor's, a customer's, and a competitor's perspective."
    - "Here's a folder of 80 resumes, use a workflow to rank them for the backend role and double-check the top ten. Interview me using the AskUserQuestion tool for a rubric."
    - "I need a name for this CLI tool. Use a workflow to brainstorm a bunch of options and run a tournament to pick the top 3."
    - "Go through my blog post draft and using a workflow verify every technical claim against the codebase, I don't want to ship anything wrong."

## How dynamic workflows work

- Dynamic workflows execute a javascript file with a few special functions that help spawn and coordinate [subagents](https://code.claude.com/docs/en/sub-agents):

![](https://pbs.twimg.com/media/HJ0t9PDbQAAYqh-.jpg)

- particularly useful to know that dynamic workflows can decide which models an agent uses and whether subagents are run in their own worktree, allowing Claude to choose the intelligence level and isolation needed.

## Why dynamic workflows

- When you ask the default Claude Code harness to do a task, it needs to both plan and execute in the same context window.
    - can sometimes break down over long-running, massively parallel and/or highly structured adversarial tasks.
- the longer Claude works on a complex task in a single context window, the more it becomes susceptible to a few specific failure modes:
    - **Agentic laziness** refers to when Claude stops before finishing a particularly complex, multi-part task and declares the job done after partial progress
    - **Self-preferential bias** refers to Claude's tendency to prefer its own results or findings, especially when asked to verify or judge them against a rubric.
    - **Goal drift** refers to the gradual loss of fidelity to the original objective across many turns, especially after compaction. Each summarization step is lossy, and details like edge-case requirements or "don't do X" constraints can get lost.
- a workflow helps combat these by orchestrating separate Claudes with their own context windows and focused, isolated goals.

## Helpful patterns when using dynamic workflows

- You can start using dynamic workflows just by asking Claude to make one, or by using the trigger word "ultracode" to ensure that Claude Code creates a workflow.
- a few common patterns that Claude might use and compose together when building workflows:

![](https://pbs.twimg.com/media/HJ0u_2cbMAA3ufP.jpg)

- **Classify-and-act**
    - Use a classifier agent to decide on the type of task, and then route to different agents or behavior based on the task. Or, use a classifier at the end to determine output.
- **Fan-out-and-synthesize**
    - Split up a task into many smaller steps, run an agent on each step and then synthesize those results.
    - particularly useful for when there are a large number of smaller steps, or when each step benefits from its own clean context window so they don't interfere or cross-contaminate.
    - synthesize step is a barrier—it waits for all the fan-out agents, then merges their structured outputs into one result.
- **Adversarial verification**
    - For each spawned agent, run a separate spawned agent to adversarially verify its output against a rubric or criteria.
- **Generate-and-filter**
    - Generate a number of ideas on a topic and then filter them by a rubric or by verification, dedupe duplicates and return only the highest quality, tested ideas.
- **Tournament**
    - Instead of dividing the work, have agents compete on it. Spawn N agents that each attempt the same task using different approaches.
    - Prompts or models then judge the results in a pairwise fashion using a judging agent until you have a winner.
- **Loop until done**
    - For tasks with an unknown amount of work, loop spawning agents until a stop condition is met (no new findings, or no more errors in the logs) instead of a fixed number of passes.

## Use cases

- Think creatively of when and how to ask Claude Code to make dynamic workflows.

![](https://pbs.twimg.com/media/HJ018ZjbcAA4nFm.png)

### Deep research

- it fans-out web searches, fetches sources, adversarially verifies their claims, and synthesizes a cited report.

### Deep verification

- if you have a report where you want to check and source every factual claim that it references you may want to generate a workflow which has one agent identify all of the factual claims and then spin off a subagent to check each one in-detail.
    - You could also have a verification agent check the source subagent to make sure its source is high quality.

### Sorting

- You may have a list of items that you want to sort by some qualitative measurement that you believe that Claude Code is good at evaluating
    - Instead run a tournament, a pipeline of pairwise-comparison agents (comparative judgment is more reliable than absolute scoring), or bucket-rank in parallel then merge. Each comparison is its own agent, so the deterministic loop holds the bracket and only the running order stays in context.

### Memory and rule adherence

- If you have a particular set of rules that you find Claude misses or struggles with, even when put into the CLAUDE.mds, create a workflow with a list of rules that must be checked by verifier agents—one verifier per rule.
- mine your recent sessions and code review comments for corrections you keep making, cluster them with parallel agents, adversarially verify each candidate (would this rule have prevented a real mistake?), and then distill the survivors back into a `CLAUDE.md`.

### Root-cause investigation

- Debugging works best when you come up with several independent hypotheses and test them
    - A workflow can structurally prevent this by spinning up agents to generate hypotheses from disjoint evidence.

### Triaging at scale

- A triage workflow classifies each item, dedupes against what's already tracked, and takes action. This could mean attempting the fix or escalating to a human user.

### Exploration and taste

- Workflows can be useful when exploring different approaches to a solution, especially when it is taste based, like design or naming, and would benefit from a rubric.
    - Try asking Claude to explore a bunch of solutions, and give a review agent a rubric for what a good solution looks like.
    - The task is complete when the review agent feels like it has met the criteria. Solutions can also be ordered or selected via a tournament based on the rubric.

### Evals

- spinning off separate agents in a worktree and then spinning off comparison agents to compare and grade the specific outputs against a rubric.
    - For example, evaluating and then refining a skill you've created against a particular criteria.

## When not to use dynamic workflows

- Workflows are new. While there are many use cases where it will create outsized results, they are not needed for every task and may end up using significantly more tokens.

## Tips for building dynamic workflows

- Detailed prompting, using the specific techniques we described above, for dynamic workflows creates the best results.
- When using workflows that can be repeated, for example triage, research, or verification, pair them with `/loop` to be run at regular intervals, and `/goal` to set a hard completion requirement.
- You can set explicit token usage budgets for dynamic workflows to limit how many tokens a task uses.
    - You can prompt it with a budget like: "use 10k tokens," which will set the cap.
- You can save workflows by pressing "s" in the workflow menu.
    - You can check these into `~/.claude/workflows` or distribute them via a skill.
    - To share them via a skill, put your JavaScript workflow files in the skill and folder and reference them in the `SKILL.md`.
