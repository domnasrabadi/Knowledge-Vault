---
type: paper
status: structured
quality:
topics: [agent-evaluation, evaluation-metrics]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Toby Ord
- Category: article
- Document Tags: ⭐️⭐️⭐️ great 
- URL: https://www.tobyord.com/writing/half-life
## 0.2 Highlights
- core idea = AI agent performance on long-duration tasks can be modeled using **constant hazard rate** from survival analysis
    - **hazard rate** = probability of failure in the next time step given survival so far
    - results in **exponentially declining success rate** with task duration
    - each agent characterized by its own **half-life** = time for success probability to drop by 50%

![[Screenshot 2025-08-10 at 2.38.18 pm.png| center | 400]]

- rationale for constant hazard rate in AI tasks
    - tasks = sequence of subtasks, each with independent and constant chance of failure
    - to succeed overall, must succeed at _all_ subtasks
        Pr⁡(Task)=Pr⁡(Subtask1 & Subtask2 & ... & SubtaskN)\Pr(\text{Task}) = \Pr(\text{Subtask}_1 \ \&\ \text{Subtask}_2 \ \&\ ... \ \&\ \text{Subtask}_N)Pr(Task)=Pr(Subtask1​ & Subtask2​ & ... & SubtaskN​)
    - duration measured in **human-equivalent task time**
    - granularity-invariance = success probability depends only on total time, not task segmentation

![[Screenshot 2025-08-10 at 2.38.40 pm.png| center | 400]]

- empirical evidence
    - **Kwa et al. (2025)** assembled 170 tasks (software engineering, cybersecurity, reasoning, ML)
        - designed to represent tasks useful for AI-assisted AI research
        - tasks automatically scorable, no multi-agent interaction, lax resource limits
    - finding: exponential relationship between solvable task length and frontier agent capabilities
        - every **7 months** → **doubling** of longest task duration solved
    - success measured at **50% threshold**
        - large gap between 50% and higher thresholds (80%, 99%, 99.9999%) relevant for real-world use
    - exponential decay fits AI agent data well; human survival curve decays more slowly than constant hazard model predicts
- implications
    - model allows estimation of agent success rate for any task length
    - simple human-time measure does not capture all improvements — task-specific features matter
    - results may not generalize to all real-world settings

