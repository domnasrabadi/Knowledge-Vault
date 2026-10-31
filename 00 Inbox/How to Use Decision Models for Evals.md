---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/hamelhusain/status/2112588257104216294/?s=12&rw_tt_thread=True
created: 2026-10-31
published: 2026-10-20
author: Hamel Husain
flashcards: none
updated: 2026-10-31
---

# How To Use Decision Models for Evals

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1287206199088173057/ixE4fKy1.jpg" width="220" />
</div>

- Decision models have exploded onto the scene recently,
- Decision models are an appealing low-cost alternative to LLM judges for automated evals. But whether they’re the right choice depends on the cost, performance, and latency requirements of your use case.
- We’ve also noticed people using the default decision threshold of 0.50 without checking whether it works well for their task. This can leave a lot of performance on the table.
- In this post, we’ll start by showing how to tune thresholds to get the best results from decision models. With those thresholds tuned, we’ll compare cost and performance to help you assess which model fits your use case.
- What we tested We used 100 traces, or logs of conversations and actions, from an apartment leasing agent. The task is to identify traces containing an error, such as a failed booking or a missed handoff to a human.

### Understanding decision thresholds

- We assign each trace one of two labels, pass or fail. This is a [binary pass/fail eval](https://hamel.dev/blog/posts/evals-faq/why-do-you-recommend-binary-passfail-evaluations-instead-of-1-5-ratings-likert-scales.html), which we recommend because it encourages clear criteria and is easier to align with human preferences.
- Each decision model returns a score from 0 to 1 that estimates how likely a trace is to contain a failure. The APIs turn this score into a decision using a **default decision threshold of 0.50**. Traces with scores at or above the threshold are flagged as failures. Using this default without checking it against your data can give you subpar results.
- In practice, scores for failures and passing traces will overlap. Lowering the threshold catches more failures but can also raise more false alarms. Choosing a threshold means balancing:
    - **Precision:** The share of flagged traces that contain a known failure.
    - **Recall:** The share of known failures that the model catches.
- The right tradeoff depends on your business goals. For example, criminal trials set a high bar for conviction to avoid convicting innocent people, emphasizing precision. Cancer screening may emphasize recall, accepting more false alarms to miss fewer cases.
- OpenAI separates the two classes best on this task, which is also reflected in its higher F1 score.
- also important not to blindly maximize F1 without thinking about your minimum requirements for the classifier to be useful. For example, if this classifier is used for an automated alerting system, I would want a minimum of 80% on both precision and recall so that I’m minimizing false alarms while catching a sufficient number of failures.
- The chart below shows how precision and recall change at different thresholds. The shaded region marks where both reach at least 80%.

![](https://pbs.twimg.com/media/HVFL9s9bUAAlokt.jpg)

- Tuning the decision threshold
- With labeled traces and saved model scores, you can ask a coding agent to tune the thresholds. Below is an example prompt you can modify for your use case: Using my saved model scores and binary labels (1 means failure), tune a decision threshold to maximize F1 while requiring at least 80% precision and 80% recall. Use stratified five-fold cross-validation, choosing thresholds on the training examples and measuring performance on the remaining examples. If comparing models, use the same splits for each. Only select thresholds that meet both minimums on the training examples. If none qualifies, report that rather than relaxing either requirement. Report validation precision, recall, and F1, along with any splits where no threshold qualified or validation performance fell below my minimums. Compare with the default threshold of 0.50. Reuse the saved scores without making new model calls.
- In practice, it’s unlikely that precision and recall are equally important (as we assumed in this post with F1). For example, the [F-beta score](https://scikit-learn.org/stable/modules/model_evaluation.html#precision-recall-f-measure-metrics) lets you give precision more weight with beta below 1, or recall more weight with beta above 1. Optimizing a different metric could lead to different thresholds and results.

### Performance versus cost


![](https://pbs.twimg.com/media/HVFMFJKagAANEh0.jpg)

- The dashed line shows the **Pareto frontier** among our remaining candidates. For any given F1 score, it identifies the cheapest candidate that meets or exceeds that score. This particular chart is a bit silly as there are only three options, but it’s a useful illustration for how to think about cost vs. performance.

### Can we trust the probabilities?

- Beyond pass/fail evals, you may want to use a decision model’s score as a confidence estimate. But can you take that number literally? For a score of 0.80 to mean an 80% chance of failure, roughly 80% of traces with similar scores should contain failures.
- The chart below shows each model’s **probability calibration**: how closely its predicted probabilities match observed outcomes.
- A point on the diagonal means the predicted probability matches the failure rate in that group. Above the line, the model underestimates the risk of failure. Below it, the model overestimates that risk.
- If the predicted probabilities don’t match the observed outcomes, we can adjust them using another model. The second panel shows one method, **Platt scaling**, which fits a simple curve to make that adjustment.

![](https://pbs.twimg.com/media/HVFMJpoaYAAFhVN.jpg)

- Platt scaling isn’t always the best fit. For example, OpenAI’s probabilities got slightly worse with the version of Platt scaling we used. You can direct your coding agent to perform calibration with the following prompt: Using my saved failure probabilities and binary labels (1 means failure), test whether Platt scaling improves each model’s probabilities. Use stratified five-fold cross-validation with the same splits for every model. Fit the calibration mapping on each training split and apply it to the remaining traces. Fit on log-odds, clipping probabilities away from 0 and 1 first. Plot predicted probabilities against observed failure rates before and after calibration. Report Brier scores (lower is better), and explain which models improved or got worse. Reuse the saved scores without making new model calls.

### Prompt tuning and evaluator scope

- In practice, we recommend building [a separate judge for each failure mode](https://hamel.dev/blog/posts/evals-faq/what-should-i-do-when-i-cant-get-my-llm-judge-to-agree-with-human-reviewers.html). With a narrower task and more specific guidance, we expect the performance gaps between models to shrink.

### Putting these ideas into practice

- We have observed that model performance varies substantially across tasks and datasets, which means it’s important to measure things yourself.
- To recap:
    - Once you’re satisfied with your [judge’s prompt](https://hamel.dev/blog/posts/llm-judge/index.html), set minimum precision and recall requirements for your use case. Rule out models that cannot meet these.
    - Tune each model’s decision threshold before comparing performance. Choose a precision-recall tradeoff that fits your business goals. Be intentional, don’t just use F1 score because this post did!
    - If you want to use scores as confidence estimates, check whether the probabilities match observed outcomes. Calibration can help, but you need to measure whether it improves them.
    - Weigh performance against cost and latency for your workload.
