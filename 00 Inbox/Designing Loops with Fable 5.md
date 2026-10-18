---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/RLanceMartin/article/2064397389189071163/?rw_tt_thread=True
created: 2026-10-18
published: 2026-06-09
author: Lance Martin
flashcards: none
updated: 2026-10-18
---

# Designing loops with Fable 5

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1999948423018221568/s2XL2-On.jpg" width="220" />
</div>

- Self-correction loops
- Letting models hillclimb on an evaluation is a common recipe for improving task performance: [/goal](https://code.claude.com/docs/en/goal) in Claude Code and [Outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes) in Claude Managed Agent are primitives that let you apply this general recipe for your specific task.
- As mentioned in our [prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5), Fable 5 is good at self-correcting in a loop. A well designed goal or rubric adds feedback to the environment that Claude is running in. This let’s Claude run, collect feedback via the goal or rubric, self-correct, and proceed until the goal or rubric is satisfied.

![](https://pbs.twimg.com/media/HKYoS3maMAoXYHR.jpg)

- We’ve found that a verifier sub-agent [tends to outperform](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5) self-critique with Fable 5, because grading is done in an independent context window. [Outcomes](https://platform.claude.com/docs/en/managed-agents/define-outcomes) in CMA handles this by spawning a grader sub-agent for you.
- For each test, I supplied a rubric (a file) with the nine checkable criteria (e.g., run a baseline, run 20 experiments, etc). Then, I ran Parameter Golf for up to 8 hours. The Outcomes grader confirmed that all experimental criteria were met before allowing Claude to stop the work.
- Memory is [another area where Fable excels](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices). We can think about this as a outer loop that spans across sessions: Claude writes to memory during a session and those memories can be retrieved in future sessions.
- Rather than directly prompting and steering Fable 5, it's often better to design loops that let the model to self-correct in response to environment feedback (e.g., /goal or Outcomes) and manage its own context (e.g., via memory).
