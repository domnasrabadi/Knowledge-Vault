---
type: article
status: inbox
quality: 1
topics: []
source: https://openai.com/index/gdpval/
created: 2026-08-08
published: 2025-09-25
author: openai.com
flashcards: none
updated: 2026-08-08
---

# Measuring the performance of our models on real-world tasks | OpenAI

<div align="center">
  <img src="https://images.ctfassets.net/kftzwdyauwt9/65D5lQ6o5VqRjLuebLijXO/63db445c96aa2ec29d5a4e76fe20169d/GDPval__Art_Card.png?w=1600&h=900&fit=fill" width="220" />
</div>

- We’re introducing GDPval, a new evaluation that measures model performance on economically valuable, real-world tasks across 44 occupations.
- started with the concept of Gross Domestic Product (GDP) as a key economic indicator and drew tasks from the key occupations in the industries that contribute most to GDP.
- This progression has moved from classic academic benchmarks like MMLU (exam-style questions across dozens of subjects), to more applied evaluations like [SWE-Bench](https://openai.com/index/introducing-swe-bench-verified/) (software engineering bug-fixing tasks), [MLE-Bench](https://openai.com/index/mle-bench/) (machine learning engineering tasks such as model training and analysis), and [Paper-Bench](https://openai.com/index/paperbench/) (scientific reasoning and critique on research papers), and more recently to market-based evaluations like [SWE-Lancer](https://openai.com/index/swe-lancer/) (freelance software engineering projects based on real payouts).
- spans 44 occupations selected from the top 9 industries contributing to U.S. GDP.
- meticulously crafted and vetted by experienced professionals with over 14 years of experience on average from these fields. Every task is based on real work products, such as a legal brief, an engineering blueprint, a customer support conversation, or a nursing care plan.
- GDPval tasks are not simple text prompts. They come with reference files and context, and the expected deliverables span documents, slides, diagrams, spreadsheets, and multimedia.
- is limited to one-shot evaluations, so it doesn’t capture cases where a model would need to build context or improve through multiple drafts.
- Each task went through a multi-step review process to ensure it was representative of real work, feasible for another professional to complete, and clear for evaluation. On average, each task received 5 rounds of expert review, including checks from other task writers, additional occupational reviewers, and model-based validation.
- resulting dataset includes 30 fully reviewed tasks per occupation (full-set) with 5 tasks per occupation in our open-sourced gold set, providing a robust foundation for evaluating model performance on real-world knowledge work.

#### Examples of GDPval tasks

- To evaluate model performance on GDPval tasks, we rely on expert “graders”—a group of experienced professionals from the same occupations represented in the dataset. These graders blindly compare model-generated deliverables with those produced by task writers (not knowing which is AI versus human generated), and offer critiques and rankings. Graders then rank the human and AI deliverables and classify each AI deliverable as “better”, “as good as”, or “worse than” one another.
- Task writers also created detailed scoring rubrics for their occupations, which add consistency and transparency to the grading process. We also built an “automated grader”, an AI system trained to estimate how human experts would judge a given deliverable. In other words, instead of running a full expert review every time, the automated grader can quickly predict which output people would likely prefer.
- Other controlled experiments back this up: increasing model size, encouraging more reasoning steps, and giving richer task context each led to measurable gains.
