---
type: paper
status: raw
quality: 
topics: [llm-judges, llm-evaluation, evaluation-metrics, data-science]
source: https://arxiv.org/abs/2605.29800v1
created: 2026-08-23
published: 2026-05-28
author: Guneet Kohli
flashcards: none
updated: 2026-08-27
---

# Nine Judges, Two Effective Votes - Correlated Errors in LLM Judge Panels

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article2.74d541386bbf.png" width="220" />
</div>


### Abstract

- LLM-as-a-judge panels aggregate votes from multiple models, with the expectation that diverse models yield more reliable evaluations. We develop a framework to measure the true informational value of such panels and quantify how far their reliability falls short of the independent-voting ideal
- we find that the 9 judges effectively provide only about 2 independent votes' worth of information. Roughly three-quarters of the panel's nominal independence is lost because the models make the same mistakes on the same items

### Introduction

- To mitigate single-model biases, researchers have turned to multi-model panels — ensembles of diverse LLMs that vote on evaluation items — with the expectation that cross-model diversity yields something approaching independent assessment
    - if each voter is better than chance and votes independently, majority-vote accuracy increases monotonically with panel size and approaches certainty
- But is it? We evaluate a 9-judge panel spanning 7 model families on three natural language inference (NLI) benchmarks
    - The panel provides negligible or negative lift over its single best member
- no prior work has *quantified* the effective independence of LLM judge panels in a way that directly connects to majority-vote reliability, using a ground truth rich enough to validate the measurement
    - Our approach differs fundamentally: we use *cross-model* disagreement and show that this disagreement is itself unreliable due to correlated errors.

### Methodology

- The gold standard for each item is the majority vote of 100 annotators
- Our panel consists of 9 judges from 7 model families. All judges use temperature 0.0 and receive a standardized NLI classification prompt
- The core finding replicates across all three datasets: $n_{\text{eff}}$ remains in the narrow 2.2–2.5 range despite panel accuracy ranging from 72% to 89%, and the best individual judge matches or outperforms the panel in every case.
- To test whether the independence deficit is a prompt or decoding artifact, we re-run all 9 judges on the same 1,000 MNLI items under four variants:
    1. **reframed** wording
    2. **reversed** label order
    3. **chain-of-thought** reasoning
    4. temperature $T = 0.5$
    - Varying prompt wording, label ordering, and temperature has essentially no effect: $n_{\text{eff}}$

### Analysis and Discussion

- Most strikingly, removing Gemini 2.5 Pro — highly correlated with Claude ($\phi = 0.60$) and GPT-4o ($0.52$) — *increases* accuracy by 1.3pp (95% CI $[+0.1, +2.6]$), and 6 of 9 removals improve accuracy.
- **Does Smarter Aggregation Help?**
    - A natural question is whether the Condorcet gap can be closed by replacing naïve majority voting with more sophisticated aggregation
    - We test three established methods
        1. **Dawid-Skene EM**, which estimates per-judge confusion matrices and true label posteriors via expectation-maximization without access to gold labels
        2. **accuracy-weighted voting**, which weights each judge by their individual accuracy (using 5-fold cross-validation to avoid label leakage)
        3. **Markowitz-optimal weighting**, which selects weights to minimize correlated error via the inverse phi correlation matrix (also cross-validated)
    - On MNLI, accuracy-weighted voting (5-fold CV) achieves 72.2% — a gain of just 0.2pp over majority vote, closing less than 1% of the 22.0pp Condorcet gap. Dawid-Skene actually *underperforms* majority vote on MNLI (70.7%), illustrating that unsupervised EM can misestimate error rates when judges are highly correlated

### Conclusion

- The independence deficit ($n_{\text{eff}}\approx 2.0$–$2.5$) is stable across three NLI datasets, three prompt variants, two temperature settings, and a pairwise preference task (RewardBench), confirming that the correlation is structural rather than an artifact of any particular experimental choice
- Adding judges does not help: the panel matches or underperforms the best individual judge across all conditions
- Established stable aggregation methods close at most 11% of the Condorcet gap (unstable correlation-aware weighting reaches 21% on one dataset but hurts on others), confirming that the bottleneck is in the inputs, not the algorithm
- These results have direct practical implications.
    - Paying for 9 opinions but receiving the informational equivalent of $\sim$2 is a substantial inefficiency: a 5-judge panel already captures 90% of achievable independence

### Limitations

- **Classification tasks.**
    - cross-task replication strengthens generalizability, but all four remain classification or binary preference tasks
- **Gold standard validity.**
    - The 100-annotator majority label is our ground truth, but for high-entropy items, the majority label may represent a plurality preference rather than a “correct” answer.
- **Snapshot in time.**
    - Our results reflect a snapshot of current frontier models. Future models may exhibit lower correlation
