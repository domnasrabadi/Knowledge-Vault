---
type: article
status: raw
quality:
topics: [llm-evaluation, evaluation-metrics]
source: ""
created: 2025-11-01
published: 2025-10-05
author: Sebastian Raschka, PhD
flashcards: none
updated: 2026-01-01
---

# Understanding the 4 Main Approaches to LLM Evaluation (From Scratch)

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!c7Za!,w_1200,h_600,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1748fa24-e946-47fb-bf1b-e488d08547fd_1764x1244.png" width="220" />
</div>

Source: https://magazine.sebastianraschka.com/p/llm-evaluation-4-approaches

Exported at: `2025-12-29T04:28:21Z`

- the four categories introduced here fall into two groups: *benchmark-based evaluation* and *judgment-based evaluation*, as shown in the figure above. (There are also other measures, such as *training loss,* *perplexity*, and *rewards*, but they are usually used internally during model development.)

![](https://substackcdn.com/image/fetch/$s_!nwaB!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc26764a9-6a26-4467-bb03-74b6cd1ed72b_1050x363.png)

- **Method 1: Evaluating answer-choice accuracy** We begin with a benchmark‑based method: multiple‑choice question answering. Historically, one of the most widely used evaluation methods is multiple-choice benchmarks such as *MMLU* (

![](https://substackcdn.com/image/fetch/$s_!WmmA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8d5f7998-21be-4144-bfc2-57b2e0a4b1c4_1040x608.png)


## Method 2: Using verifiers to check answers

- verification-based approaches quantify the LLMs capabilities via an accuracy metric.
- verification methods allow LLMs to provide a free-form answer. We then extract the relevant answer portion and use a so-called verifier to compare the answer portion to the correct answer provided in the dataset,
- we can employ external tools, such as code interpreters or calculator-like tools/softwar
- downside is that this method can only be applied to domains that can be easily (and ideally deterministically) verified, such as math and code.
- allows us to generate an unlimited number of math problem variations programmatically and benefits from step-by-step reasoning, it has become a cornerstone of reasoning model evaluation and development.

![](https://substackcdn.com/image/fetch/$s_!P2NG!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74860b8a-d12a-4781-8362-d5eb06feb389_1406x656.png)

- use another LLM with a pre-defined grading *rubric* (i.e., an evaluation guide) to compare an LLM’s response to a reference response and judge the response quality based on a pre-defined rubric,
- One of the reasons why judges work so well is also that evaluating an answer is often easier than generating one.
