---
type: article
status: raw
quality:
topics: [llm-judges, evaluation-metrics, model-calibration]
source: ""
created: 2025-11-28
published:
author: Chungpa Lee; Thomas Zeng; Jongwon Jeong; Jy-yong Sohn; Kangwook Lee
flashcards: none
updated: 2026-01-01
---

# How to Correctly Report LLM-as-a-Judge Evaluations

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/static/images/article0.00998d930354.png" width="220" />
</div>

Source: https://readwise.io/reader/document_raw_content/392025511

Exported at: `2025-12-29T04:27:41Z`

- However, directly using a point-estimate ˆp (e.g., the raw proportion of answers the LLM judges as ‘correct’) as a quality metric is statistically problematic
- an LLM may incorrectly judge an ‘incorrect’ answer as ‘correct’ or, conversely, mislabel a ‘correct’ answer as ‘incorrect’. Let q0 and q1 denote the probabilities that the LLM makes the right decision in each case

![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/4ff05c9a9573c0dc911644cd77b847ed.png?t=1765917367244)

- In general, whenever the LLM is imperfect (q0 + q1 < 2), the expected value of ˆp deviates from the ground-truth accuracy θ
- Bias and its adjustment in LLM-based judgment under imperfect LLM evaluators (q0 = 0.7 and q1 = 0.9). (a) When the true accuracy θ is low (θ < 0.75), the expected value of the naive estimator E[ˆp] overestimates θ, whereas when θ is high (θ > 0.75), it underestimates θ. (b) By incorporating the judgment accuracies q0 and q1, which can also be estimated from a calibration dataset with ground-truth labels, we obtain the bias-adjusted estimator ˆθ along with its confidence interval. (c) The resulting estimator θˆ is unbiased when the true values of q0 and q1 are known or when a sufficiently large calibration dataset is available.
- Consequently, progress may have been overstated or understated depending on the bias direction, highlighting the need for a principled method for bias adjustment.
- Importantly, this bias can be corrected. When q0 and q1 are known, a classical result from prevalence estimation (Rogan and Gladen, 1978) provides an exact adjustment.
- Even when they are unknown, they can be estimated from a calibration dataset with ground-truth labels, and the resulting estimates ˆq0 and ˆq1 can be substituted into the correction formula
- Correcting the point estimate, however, is only part of the problem. LLM-as-a-Judge evaluation involves two sources of uncertainty: (i) randomness arising from the test dataset, which affects the estimated judgment score ˆp, and (ii) randomness from the calibration dataset, which affects ˆq0 and qˆ1. A principled confidence interval must incorporate both components;
- To evaluate these instances, we assume that there is a human-defined notion of correctness. This is specified by a ground-truth labeler
- Our goal is to measure the true accuracy of the model with respect to human judgment:
- In practice, an LLM is often used to judge correctness instead of human annotators.
- The accuracy reported in practice is the empirical fraction of instances labeled as ‘correct’ by the LLM judge:
- However, the LLM’s judgment Zˆ does not necessarily coincide with the human ground-truth label Z. That is, the LLM may incorrectly reject answers that are truly ‘correct’ or incorrectly accept answers that are truly ‘incorrect’. The accuracy of the LLM’s judgment in these two cases is captured by
- which correspond to the sensitivity (true positive rate) and specificity (true negative rate), respec- tively
- In realistic settings, these accuracies are unknown and must be estimated from a calibration dataset with human-verified labels. Each calibration instance contains both the ground-truth label z ∈ 0, 1 and the corresponding LLM prediction ˆz ∈ 0, 1.
- Substituting these estimates into (3) gives the bias-adjusted estimator
- Adaptive Allocation to Reduce Confidence-Interval Length Motivated by this observation, we introduce an adaptive allocation procedure in Algorithm 1. The algorithm begins by collecting a small pilot calibration sample (e.g., mpilot = 10 for each label type) to obtain preliminary estimates of (˜q0, ˜q1).
