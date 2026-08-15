---
type: article
status: raw
quality: 1
topics: [ai-agents, ai-coding]
source: https://x.com/claudedevs/status/2074208949205881033/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-07-06
author: ClaudeDevs
flashcards: none
updated: 2026-08-13
---

# Getting Started with Loops

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2044472418815893504/xf14RxM8.png" width="220" />
</div>

- On the Claude Code team, we define **loops as agents repeating cycles of work until a stop condition is met**. We categorize a few different types of loops based on:
    - How they are triggered
    - How they are stopped
    - What Claude Code primitive is used
    - What type of task is most appropriate for each.
- main loop types, when to use each, and how to maintain code quality while managing token usag

### Turn-based loops

![](https://pbs.twimg.com/media/HMkOVNybEAAncbL.jpg)

- **Triggered by**: A user prompt.
    - **Stop criteria**: Claude judges it has completed the task or needs additional context.
    - **Best used for:** Shorter tasks that are not part of a regular process or schedule.
    - **Managed usage by:** Write specific prompts and improve verification using skills to reduce the number of turns.
- You can improve the verification step by encoding your manual steps as a `SKILL.md` so Claude can check more of its own work, end-to-end. This should include tools or connectors to allow Claude to *see*, *measure* or *interact* with the result. The more quantitative the checks are, the easier it is for Claude to self-verify.

### Goal-based loop (/goal)


![](https://pbs.twimg.com/media/HMkOlk3bcAAHX46.jpg)

- **Triggered by**: A manual prompt in real-time.
    - **Stop criteria**: Goal achieved OR maximum number of turns reached.
    - **Best used for:** Tasks that have verifiable exit criteria.
    - **Managed usage by:** Setting a specific completion criteria and explicit turn caps, "stop after 5 tries."
- You can extend how long Claude keeps iterating by defining what done looks like with /goal.
- When you define the success criteria, Claude doesn't have to make a determination on what is "good enough" and end the loop early. Each time Claude tries to stop, an evaluator model checks your condition and sends it back to work until the goal is met or a number of turns you define is reached. This is why deterministic criteria, such as number of tests passed or clearing a certain score threshold, are so effective.

### Time-based loop (/loop and /schedule)

- **Triggered by**: A specified time interval.
    - **Stop criteria**: You cancel it, or the work completes (the PR merges, the queue is empty).
    - **Best used for:** For recurring work, or interfacing with external environments / systems.
    - **Managed usage by:** Set longer intervals or react based on events rather than time.
- Some agentic work is recurring: the task stays the same and only the inputs change. For example, summarizing Slack messages every morning
- For these, you can trigger when Claude runs with `/loop` which re-runs a prompt on an interval

### Proactive loops


![](https://pbs.twimg.com/media/HMkPQM8bEAA3RAk.jpg)

- **Triggered by**: An event or schedule, with no human in real time.
    - **Stop criteria**: Each task exits when its goal is met. The routine itself runs until you turn it off.
    - **Best used for:** Recurring streams of well-defined work: bug reports, issue triage, migrations, dependency upgrades, etc.
    - **Managed usage by:** Routing routines to smaller, faster models and using the most capable model for judgment calls.
- The primitives above, along with other Claude Code features like **auto mode** and **dynamic workflows** (research preview) can be composed into a loop for long-running work.
- For example, to handle incoming feedback, you can use:
    1. **`/schedule`** (research preview) to run a routine that checks for new reports
    2. **`/goal`** to define what done looks and **skills** to document how to verify it
    3. **Dynamic workflows** to orchestrate agents that triage each report, fix it, and review the fix
    4. **Auto mode** so the routine runs without stopping to ask for permission

### Maintaining code quality

- The quality of a loop's output depends on the system around it. When designing the system:
- **Give Claude a way to verify its own work**: Encode what good looks like for you and your team with [skills](https://code.claude.com/docs/en/skills)
