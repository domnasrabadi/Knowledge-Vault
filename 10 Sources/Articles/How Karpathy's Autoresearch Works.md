---
type: article
status: raw
quality:
topics: [ai-agents, ai-coding, ai-engineering, agent-harnesses]
source: https://x.com/manthanguptaa/status/2032464949952598152/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-03-13
author: Manthan Gupta
flashcards: none
updated: 2026-08-17
---

# How Karpathy's Autoresearch Works

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1863635937575505920/Lt-tcQz0.jpg" width="220" />
</div>

- Autoresearch is not trying to be a general-purpose AI scientist. It is a small, tightly constrained system for one specific job: let an agent modify a training script, run a bounded experiment, measure the result, keep the change if it helps, and discard it if it does no
    1. Edit the training code
    2. Run an experiment for a fixed amount of time
    3. Measure the result using a fixed metric
    4. Keep the change if it improves the score
    5. Revert it if it does not
    6. Repeat
- The setup is deliberately minimal. The agent is allowed to modify only one file, `[train.py](http://train.py)`. Data preparation, tokenization, and evaluation are kept outside the search space. That one decision does a lot of work. It keeps the harness focused, keeps diffs reviewable, and prevents the agent from "improving" the system by changing the benchmark in the background.
- There is another subtle idea here too. The real control plane of the repo is not just the Python code. It is `[program.md](http://program.md)`, the file that tells the agent how to behave. In other words, the human is not only programming the model. The human is programming the researcher.

![](https://pbs.twimg.com/media/HDSHxaGbwAAsvEc.jpg)

- Autoresearch matters because it demonstrates a broader truth about agents: autonomy gets useful when the harness is tight.
- Lessons
    - Lesson 1: The first lesson is that **constraints make agents better**. The agent edits one file, chases one metric, operates within one fixed harness, and advances only when the score improves. That is not a drawback of the system but the reason the system can run for hours without dissolving into noise. Many agent systems fail because they maximize freedom too early. More freedom usually means a larger error surface.
    - Lesson 2: The second lesson is that **prompts are part of the architecture**. In Autoresearch, `[program.md](http://program.md)` is not fluff around the code. It defines workflow, boundaries, persistence, logging, recovery, and selection criteria
    - Lesson 3: The third lesson is that **you should optimize the harness, not just the model**. A lot of builders focus on model intelligence in isolation. Autoresearch shows that the surrounding machinery matters just as much: how work is launched, how failures are handled, how progress is measured, how bad paths are rolled back, and how state is recorded
    - Lesson 4: The fourth lesson is that **time-bounded evaluation is underrated**. The 5-minute wall-clock budget is one of the best ideas in the repo
    - Lesson 5: The fifth lesson is that **reversibility and observability are non-negotiable**. Autoresearch keeps losers cheap to discard and makes every experiment inspectable through logs, commit history, and `results.tsv`.
- **autonomous systems become much more useful when you reduce them to a tight harness with clear boundaries, a stable metric, reversible experiments, and good operational discipline**.
