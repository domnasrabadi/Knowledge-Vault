---
type: paper
status: raw
quality: 2
topics: [llm-judges, llm-evaluation, evaluation-metrics, agent-evaluation]
source: https://arxiv.org/abs/2606.27226v1
created: 2026-08-22
published: 2026-06-25
author: Sangwoo Cho, Kushal Chawla, Pengshan Cai, Zefang Liu, Chenyang Zhu, Shi-Xiong Zhang, Sambit Sahu
flashcards: none
updated: 2026-08-23
---

# Ask, Don't Judge - Binary Questions for LLM Evaluation

### Abstract

- We propose BINEVAL, a framework that decomposes evaluation criteria into atomic binary questions and aggregates the resulting verdicts into interpretable, multi-dimensional scores
    - Given a task prompt, a meta-prompt generates fine-grained evaluation questions, and an LLM answers them independently for each output, yielding transparent question-level feedback together with calibrated overall scores
    - This decomposition makes evaluation easier to inspect, easier to diagnose, and directly usable for prompt improvement
- Beyond competitive correlation with human judgments, BINEVAL better matches human score distributions and avoids the ceiling effects common in prior LLM judges, leading to better discrimination between borderline and clearly flawed outputs
- We further show that the same question-level feedback supports iterative prompt optimization, improving evaluator prompts

### Introduction

- rapid progress of large language models (LLMs) has made generation easy and evaluation hard
    - Human evaluation is slow and expensive, lexical metrics such as ROUGE, BLEU, and BERTScore miss semantic correctness and factuality, and holistic LLM judges often return opaque scores that are difficult to diagnose
    - This bottleneck is especially costly in iterative development.
        - Comparing prompts, models, or decoding strategies requires feedback that is not only accurate but also actionable.
        - A single scalar score is often insufficient: if a summary receives a mediocre rating, it is still unclear whether the problem is factual inconsistency, weak relevance, missing content, or poor fluency.
- Our premise is simple: instead of asking a model for one broad judgment, ask it a set of small, checkable questions
    - We therefore propose BinEval, which decomposes each evaluation criterion into atomic yes/no questions and aggregates the resulting verdicts into interpretable scores
    - This decomposition turns evaluation from a black-box verdict into a structured diagnostic signal, making it easier to inspect, debug, and improve both evaluators and generators
- BinEval has three components
    - First, a meta-prompt decomposes a task prompt into atomic questions organized by evaluation dimension
    - Second, an evaluator answers each question independently and aggregates the answers into per-dimension and overall scores
    - Third, a two-phase optimization loop improves both evaluator prompts and generation prompts using question-level feedback

### Related Work

- Multi-dimensional evaluation aims to decompose quality into interpretable facets such as coherence, faithfulness, informativeness, and relevance
    - Together, these methods reinforce the value of breaking evaluation into smaller, more structured judgments
- **Atomic Decomposition for Evaluation.** FActScore pioneered the “decompose-then-verify” paradigm by breaking long-form generations into atomic facts and verifying them individually
- **Prompt Optimization.** Prompt optimization has increasingly shifted from manual instruction engineering toward automated and programmatic refinement

### Method

- We present BinEval in three parts: binary question generation, binary evaluation and scoring, and iterative prompt optimization
- **Binary Question Generation**
    - Let $T$ denote a task prompt
    - We define a *decomposition function* that maps $T$ to a set of binary questions: $$\mathcal{Q} = \mathcal{F}_{\text{LLM}}(T; M) = \{q_1, q_2, \dots, q_N\}.$$ where $M$ is a meta-prompt that instructs an LLM to perform a two-step decomposition
    - **Step 1 – Summarize.** We first summarize the task prompt $T$ into an explicit set of requirements $\mathcal{R} = \{r_1, r_2, \dots, r_K\}$.
        - Each requirement $r_k$ captures a distinct evaluation criterion, such as whether the output includes a key piece of information or obeys a formatting constraint.
        - This summarization step is intended to help the model form a coherent representation of the full task before attempting finer-grained decomposition
    - **Step 2 – Decompose.** For each requirement $r_k$, we generate one or more binary questions such that answering “yes” indicates the output satisfies the requirement and answering “no” indicates a violation. Requirements that implicitly contain multiple sub-tasks are decomposed into separate questions, and each question is paired with a concise violation example to clarify the negative case
    - the same intuition suggests that evaluation becomes easier when the model answers targeted binary questions about simplified sub-tasks rather than making a single holistic judgment
    - The questions can be organized into evaluation dimensions. For a set of dimensions $\mathcal{D}$, such as coherence, consistency, fluency, and relevance, the questions partition as $$\mathcal{Q} = \bigcup_{d \in \mathcal{D}} \mathcal{Q}_d,$$ where $\mathcal{Q}_d$ contains questions specific to dimension $d$.
        - The meta-prompt $M$ is task-agnostic: the same meta-prompt generates appropriate binary questions for summarization, dialogue, instruction following, or any other task, with only $T$ changing
- **Binary Evaluation and Scoring**
    - Given an evaluator LLM $E$, an input $x$ such as a source document, a transcript, or an instruction, an output $y$ such as a generated summary, a dialogue response, or a completion, and a binary question $q_i$, we define the *binary evaluation function* $$f_E(x, y, q_i) \in \{0, 1\},$$ where $f_E(x, y, q_i) = 1$ if the evaluator answers “yes” and $0$ otherwise. Alongside each binary verdict, the evaluator produces a natural-language explanation $e_i$, enabling interpretability
        - The per-dimension score for dimension $d$ is $$S_d(x, y) = \frac{1}{|\mathcal{Q}_d|} \sum_{q_i \in \mathcal{Q}_d} f_E(x, y, q_i).$$
        - The overall score across all $N$ questions is $$S(x, y) = \frac{1}{N} \sum_{i=1}^{N} f_E(x, y, q_i).$$
        - Both scores lie in $[0,1]$, where 1 indicates all criteria are satisfied. To enable comparison with existing evaluation frameworks that use different scales, the scores can be mapped from $[0, 1]$ to any target interval $[a, b]$ via affine scaling: $$S'(x, y) = S(x, y) \cdot (b - a) + a.$$
- **Cross-Model Prompt Update**
    - BinEval’s binary question framework enables cross-model prompt update between evaluators. The key insight is that disagreements between a source evaluator and a target evaluator on specific binary questions provide a fine-grained signal for improvement: unlike holistic score differences, binary question disagreements identify exactly which criteria are being judged inconsistently across models

### Experimental Setup

- Part I evaluates BinEval’s performance on established benchmarks with human annotations
- Part II demonstrates the iterative prompt-updating mechanism on both an unverifiable task and a verifiable task
- **Metrics**
    - For evaluation quality, we report Spearman’s rank correlation ($\rho$), Kendall’s rank correlation ($\tau$), and Pearson correlation ($r$) between method scores and human judgments at the summary level.

### Results

- BinEval(Claude) is the strongest method overall, achieving the best average Spearman and Kendall correlations and leading on coherence, consistency, and fluency.
    - The largest gain is on consistency, where BinEval reaches 0.655 / 0.615, suggesting that decomposing factual quality into multiple targeted checks is especially effective for summary evaluation.
    - Relevance remains the main exception: G-Eval (GPT-4) is best on that dimension, indicating that some broader semantic judgments are still harder to capture with binary decomposition
- Under the same backbone, BinEval(gpt-oss) outperforms both G-Eval (gpt-oss) and UniEval (gpt-oss) on average, driven by large gains on coherence and consistency
- BinEval is visually closest to the human distributions on consistency, where it largely matches the human concentration near the upper end while still retaining some low-scoring mass; this mirrors its largest correlation advantage
- **Why Does Decomposition Work?**
    - *Why* does evaluating through multiple atomic binary questions outperform a single holistic judgment? We identify three contributing mechanisms and examine the evidence for each on SummEval
        - **Complexity Reduction.** Each binary question isolates a single verifiable property, replacing one multi-faceted judgment with many simpler ones—mirroring the benefits of task decomposition in prompting
            - A question like “*Are all named entities accurately represented?*” is easier to answer reliably than “*Rate factual consistency from 1–5*.”
        - **Variance Reduction via Aggregation.** Aggregating $N$ weakly correlated binary classifiers reduces variance proportionally to $1/N$
        - **Coverage of Failure Modes.** Decomposition forces explicit enumeration of criteria, improving recall over holistic judgment
    - From a practical standpoint, practitioners can inspect generated questions for these properties (yes-rate spread, inter-question correlation, pairwise coverage) to anticipate where decomposition will help most and where refinement is needed

### Discussion

- **Failure Modes.** Decomposition works best for concrete criteria such as factual consistency, where errors can be tied to specific claims or entities and can therefore be checked with relatively clear yes/no decisions.
    - It is less reliable for subjective qualities, where human judgments are more holistic and less reducible to a set of binary checks.
    - In such cases, the quality of the evaluation depends heavily on whether the generated questions capture the aspects that humans actually weigh when forming an overall judgment
- **Computational Cost.** BinEval trades efficiency for diagnostic value.
    - Compared with a single holistic judgment, it must generate binary questions and answer each of them. This increases both the number of model calls and the total amount of text processed during evaluation.
    - Prompt updating adds note-taking, lesson deduplication, and meta-prompt rewriting, though batching keeps the first two modest and prompt rewriting is shared by most update methods.
    - The main recurring cost is question-level evaluation
- **Limitations.** The method still depends on question quality: if important criteria are missing, the final score will miss them. It also assumes that the fraction of satisfied questions maps approximately linearly to overall quality, which need not always hold.
- **Decomposed Evaluation vs. Holistic Scoring**
    - Holistic scoring conflates local correctness with global consistency, rewarding fluent, topically coherent text even when specific claims are wrong.
    - BinEval avoids this by decomposing consistency into seven targeted binary questions, each probing a distinct claim type: factual support, fabrication, entity accuracy, numerical correctness, causal fidelity, hallucination, and scope representation
    - This example motivates the core design principle of BinEval: fine-grained binary questions act as *claim-level probes*, making errors visible that aggregate scoring systematically obscures
        - Critically, this granularity also makes the feedback actionable, as each failed question directly identifies the error type, enabling targeted corrections to either the summarizer or the evaluator prompt.

### Conclusion

- BinEval, a task-agnostic, training-free framework that evaluates LLM outputs by decomposing criteria into atomic binary questions
    - Because each score is grounded in individual verdicts with explanations, BinEval offers interpretable feedback that helps practitioners diagnose and improve LLM systems, and suggests atomic binary decomposition as a promising direction for broader evaluation tasks
- Looking ahead, we see natural extensions to agentic and multi-turn settings, where fine-grained, claim-level feedback is especially valuable for identifying where and why a system goes wrong

### Binary Questions for SummEval

Binary questions for **Coherence** on SummEval (8 questions).

| ID | Question | Yes-rate |
| --- | --- | --- |
| Q1 | Does the summary have a well-defined structure (e.g., a clear beginning, middle, and/or end) rather than appearing randomly assembled? | 0.66 |
| Q2 | Are the sentences in the summary arranged in a sensible and logical order? | 0.68 |
| Q3 | Does the summary avoid being a mere heap of loosely related facts or information? | 0.43 |
| Q4 | Do the sentences in the summary flow logically from one to the next, with clear transitions or connections between them? | 0.44 |
| Q5 | Does the summary maintain a unified focus on a single main topic rather than drifting across multiple unrelated subjects? | 0.96 |
| Q6 | Does the summary cover the main topic of the news article? | 0.85 |
| Q7 | Does the summary cover the key points of the news article? | 0.10 |
| Q8 | Does the summary present information in a clear manner that is easy to follow and understand? | 0.61 |

Binary questions for **Consistency** on SummEval (7 questions).

| ID | Question | Yes-rate |
| --- | --- | --- |
| Q1 | Are all statements in the summary entailed by or supported by the source article? | 0.75 |
| Q2 | Is the summary free of factual errors when compared to the source article? | 0.82 |
| Q3 | Is the summary free of hallucinated facts (i.e., information that is fabricated and not present in the source article)? | 0.81 |
| Q4 | Are all named entities (people, organizations, locations) in the summary accurately represented as they appear in the source article? | 0.91 |
| Q5 | Are all numerical claims (dates, statistics, quantities, amounts) in the summary consistent with the source article? | 0.95 |
| Q6 | Are the causal relationships and event sequences described in the summary consistent with those in the source article? | 0.87 |
| Q7 | Does the summary avoid misrepresenting or distorting the meaning of information from the source article? | 0.76 |

Binary questions for **Fluency** on SummEval (7 questions).

| ID | Question | Yes-rate |
| --- | --- | --- |
| Q1 | Is the summary free of grammatical errors? | 0.54 |
| Q2 | Is the summary free of spelling errors? | 0.71 |
| Q3 | Is the summary free of punctuation errors? | 0.33 |
| Q4 | Does the summary use appropriate and natural word choices? | 0.81 |
| Q5 | Does the summary have well-structured sentences that are easy to follow? | 0.70 |
| Q6 | Does the summary read smoothly and sound natural overall? | 0.52 |
| Q7 | Is the summary easy to understand without requiring re-reading due to language issues? | 0.76 |

Binary questions for **Relevance** on SummEval (5 questions).

| ID | Question | Yes-rate |
| --- | --- | --- |
| Q1 | Does the summary address the main topic or central event of the source article? | 0.95 |
| Q2 | Does the summary cover at least some of the key points or important details of the source article? | 0.50 |
| Q3 | Is the summary free from significant redundancy, such as repeating the same point multiple times in different words? | 0.64 |
| Q4 | Is the summary free from excessive trivial or unimportant details that dilute the coverage of main points? | 0.72 |
| Q5 | Does the summary prioritize the most newsworthy or significant information from the source rather than focusing on minor or tangential aspects? | 0.49 |
