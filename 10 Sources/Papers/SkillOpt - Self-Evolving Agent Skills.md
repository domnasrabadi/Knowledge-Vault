---
type: paper
status: raw
quality: 
topics: [agent-harnesses, ai-agents, prompting]
source: https://arxiv.org/abs/2605.23904v2
created: 2026-08-23
published: 2026-05-22
author: Yifan Yang et al.
flashcards: none
updated: 2026-08-27
---

# SkillOpt - Self-Evolving Agent Skills

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article0.00998d930354.png" width="220" />
</div>

### Abstract

- Agent skills today are hand-crafted, generated one-shot, or evolved through loosely controlled self-revision, none of which behaves like a deep-learning optimizer for the skill, and none of which reliably improves over its starting point under feedback
- We argue the skill should instead be trained as the external state of a frozen agent, with the same discipline that makes weight-space optimization reproducible
    - a separate optimizer model turns scored rollouts into bounded add/delete/replace edits on a single skill document, and an edit is accepted only when it strictly improves a held-out validation score

### Introduction

- If the recurring object of adaptation is the agent’s procedure, the skill document itself should be trainable. Yet weight adaptation is often unavailable for closed frontier models and expensive for open ones, while manually written or one-shot skills are brittle under a target domain or harness
- Our key idea is to treat skill editing as a controllable domain-adaptation process, with the skill document as the external state, an additional frontier model as the optimizer, and training-style controls over evidence, step size, validation, and update direction.
    - We introduce SkillOpt, a text-space optimizer for agent skills. Given a target domain, an initial skill, and the model being adapted, SkillOpt repeatedly samples trajectory batches, analyzes successes and failures, and asks a frontier optimizer model to propose structured add/delete/replace edits

### Method

- **Problem Setup**
    - A skill $s$ is a natural-language policy inserted into the agent context before execution
    - We use $M$ to denote the frozen target model whose behavior is being adapted through skill optimization. For a harness $h$, task $x$, and skill $s$, execution produces a trajectory $\tau$ and a scalar score $r$: $$\begin{equation} (\tau(s), r(s)) = h(M, x, s), \qquad r(s) \in [0,1]. \end{equation}$$
- **Forward Pass: Rollout Evidence**
    - At each optimization step, the target model runs a rollout batch from $D_{\mathrm{tr}}$ with the current skill. The harness records task metadata, messages, tool calls, observations, command outputs, final answers, verifier feedback, and benchmark-specific context such as spreadsheet previews, document references, or compact execution traces
- **Backward Pass: Minibatch Reflection**
    - The optimizer model turns trajectories into skill edits, following the broader line of trajectory-driven reflection and prompt evolution
        - It first separates failures from successes and partitions each group into reflection minibatches.
            - This matters because single trajectories often produce anecdotal fixes, while minibatches expose reusable procedural errors: the agent consistently searches the wrong source, writes an answer in the wrong format, or fails to verify a tool result.
            - Failure minibatches propose missing or corrective rules; success minibatches preserve behaviors that already work.
            - Each reflection returns structured add/delete/replace edits, or in rewrite mode a small set of rewrite suggestions.
        - Local proposals are merged hierarchically by first consolidating failure- and success-driven edits separately, then combining them with priority on failure corrections.
            - This step filters duplicate, contradictory, and example-specific suggestions before the optimizer selects the final bounded update.
- **Bounded Text Updates**
    - The learning-rate analogue in SkillOpt is the edit budget $L_t$: the maximum number of skill edits applied at step $t$
        - After aggregation, the optimizer model ranks the merged edit pool by expected utility and clips it to the top $L_t$ edits
        - Unbounded rewrites can erase useful rules, introduce incompatible instructions, or overfit to a local failure; bounded updates preserve continuity while still allowing the skill to acquire new procedures
    - The selected edits produce a candidate skill.
        - In patch mode, edits are localized operations such as append, insert, replace, and delete; in rewrite mode, selected suggestions condition a full skill rewrite.
        - Step-level edits cannot overwrite the protected slow-update field, so fast local changes and slower epoch-wise consolidation remain separated.
- **Validation Gate and Rejected-Edit Buffer**
    - Every candidate skill is evaluated on $D_{\mathrm{sel}}$ with the same frozen target model and harness
        - If it improves over the current selection score, it becomes the new current skill; if it also exceeds the best score so far, it becomes `best_skill.md`. Otherwise it is rejected
    - Rejected updates are still useful. The optimizer records an epoch-local buffer containing observed failure patterns and, for rejected steps, the edits that were tried and the score drop they caused
        - Later reflection calls in the same epoch receive this buffer, so the optimizer model can avoid repeating failed edits and focus on unresolved failures. This gives the loop negative feedback during training without adding inference-time cost.

### Baselines

- We compare against seven baselines that span the no-adaptation, hand-written, one-shot, and learning families:
    1. *no skill* (frozen target model run with the benchmark’s default system prompt)
    2. *human skill* (an expert-written skill document curated per benchmark)
    3. *one-shot LLM skill* (a single skill generated from a high-level task description by GPT–5.5 and never updated)
    4. *Trace2Skill* (trajectory-level skill distillation)
    5. *TextGrad* (gradient-style natural-language prompt optimization)
    6. *GEPA* (Pareto reflective prompt evolution)
    7. the harness-side competitor *EvoSkill* (skill-folder evolution under failure analysis)
    - All baselines use the same target model, the same held-out test split
- Taken together, the table supports a strong empirical claim: across direct chat and two tool-execution harnesses, across seven target models, and on procedural and factual benchmarks alike, optimizing a single compact skill artifact under bounded text-space training is the strongest no-weight-update adaptation strategy among the baselines we consider
- The main gains come from feedback-driven skill editing rather than from a better one-shot prompt: human and LLM skills can help when prior instructions happen to match the benchmark, but they cannot correct failures after observing rollouts
