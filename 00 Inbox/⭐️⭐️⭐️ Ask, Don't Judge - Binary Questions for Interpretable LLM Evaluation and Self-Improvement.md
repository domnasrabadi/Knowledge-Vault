---
type: paper
status: inbox
quality: 3
topics: []
source: https://arxiv.org/pdf/2606.27226
created: 2026-08-08
published: 
author: Sangwoo Cho; Kushal Chawla; Pengshan Cai; Zefang Liu; Chenyang Zhu; Shi-Xiong Zhang; Sambit Sahu
flashcards: none
updated: 2026-08-08
---

# Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article3.5c705a01b476.png" width="220" />
</div>

- holistic LLM judges often produce opaque scores that are hard to debug
- We propose BINEVAL, a framework that decomposes evaluation criteria into atomic binary questions and aggregates the resulting verdicts into interpretable, multi-dimensional scores
- Given a task prompt, a meta-prompt generates fine-grained evaluation questions, and an LLM answers them independently for each output, yielding transparent question-level feedback together with calibrated overall scores
- decomposition makes evaluation easier to inspect, easier to diagnose, and directly usable for prompt improvement
- BINEVAL better matches human score distributions and avoids the ceiling effects common in prior LLM judges, leading to better discrimination between borderline and clearly flawed outputs
- A single scalar score is often insufficient: if a summary receives a mediocre rating, it is still unclear whether the problem is factual inconsistency, weak relevance, missing content, or poor fluency.
- Our premise is simple: instead of asking a model for one broad judgment, ask it a set of small, checkable questions. We therefore propose BINEVAL, which decomposes each evaluation criterion into atomic yes/no questions and aggregates the resulting verdicts into interpretable scores
- BINEVAL has three components
- First, a meta-prompt decomposes a task prompt into atomic questions organized by evaluation dimension
- Second, an evaluator answers each question independently and aggregates the answers into per-dimension and overall scores
- Third, a two-phase optimization loop improves both evaluator prompts and generation prompts using question-level feedback
- Let T denote a task prompt defining the generation requirements, such as a summarization instruction, a dialogue system prompt, or an instruction-following specification. We define a *decomposition function* that maps T to a set of binary questions:
- Q = \mathcal{F}_{\text{LLM}}(T; M) = \{q_1, q_2, \ldots, q_N\}.
- where M is a meta-prompt that instructs an LLM to perform a two-step decomposition.
- Step 1 – Summarize. We first summarize the task prompt T into an explicit set of requirements
- Each requirement r k captures a distinct evaluation criterion, such as whether the output includes a key piece of information or obeys a formatting constraint
- This summarization step is intended to help the model form a coherent representation of the full task before attempting finer-grained decomposition
- Step 2 – Decompose. For each requirement rk, we generate one or more binary questions such that answering "yes" indicates the output satisfies the requirement and answering "no" indicates a violation
- each question is paired with a concise violation example to clarify the negative case
- same intuition suggests that evaluation becomes easier when the model answers targeted binary questions about simplified sub-tasks rather than making a single holistic judgment
- unlike holistic score differences, binary question disagreements identify exactly which criteria are being judged inconsistently across models
- clear ranking across evaluation paradigms. BINEVAL (Claude) is the strongest method overall, achieving the best average Spearman and Kendall correlations and leading on coherence, consistency, and fluency
- Overall, BINEVAL's main strength is not perfect calibration on every dimension, but its ability to preserve meaningful relative variation, especially for factual consistency
