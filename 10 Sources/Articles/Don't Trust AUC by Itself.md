---
type: article
status: structured
quality:
topics: [evaluation-metrics, model-calibration, model-monitoring]
source: ""
created: 2025-09-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Don't trust a single *global* AUC
- a high overall AUC can hide pockets where your model is bad for specific groups or segments
- action: always pair global AUC with a **cluster-level breakdown**
	- within-cluster AUC (how well you rank _inside_ each group) and **inter-cluster AUC** (how consistently you rank _across_ groups)

# 2 Use the AUC decomposition as well 


>[!question] get gpt to simplify
> 


- the paper shows a clean identity:  
    **AUC_global = Σᵢ Σⱼ wᵢⱼ · AUCᵢⱼ**, where AUCᵢⱼ compares positives from cluster _i_ vs negatives from cluster _j_ (diagonal = intra-cluster, off-diagonal = inter-cluster)    
- action: compute the **AUC matrix** [i, j] each time you evaluate a model; scan rows/columns for low cells to find failure modes (e.g., “positives from seniors rank below negatives from young users”)

# 3 Don't just measure rank - measure probability quality too
- **Brier score** and **log loss** are additive and decompose cleanly by cluster (unlike AUC)
	- so they tell you where calibration is off even when ranking looks fine
- use all 3 metrics together for a more wholistic picture
	- AUC tells you quality of separability 
	- Brier + LogLoss tell you calibration & confidence issues

$$
{\Large
\begin{aligned}
& \textit{for each cluster, log:}\\[0.6ex] \\
& \rightarrow \text{AUC}_{ii} \\
& \rightarrow \text{mean predicted value }\hat{p}\\
& \rightarrow \text{prevalence} \\
& \rightarrow \text{Brier Score, LogLoss} 
\end{aligned}
}
$$

# 4 Make it a habit → "*cluster first*"
- how to choose clusters
    - **business segments:** channel, geography, merchant/MCC, product, thin-file vs thick-file, income bands
    - **behavioural buckets:** recency/velocity features, time-of-day, device types
    - **unsupervised clusters:** k-means / HDBSCAN on feature embeddings to find behaviourally coherent pockets
- action: settle on a **small, stable set** of clusters for _governance_ + allow a _rotating exploratory set_ for discovery each release

# 5 What to do when you find problems 

| failure pattern                              | typical root cause                              | quick fixes                                                       | longer-term fixes                                                                        |
| -------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **low AUCᵢᵢ** (within cluster)               | weak features / wrong transforms for that group | targeted features; cluster-specific thresholds                    | re-spec model with interactions or GAM-like components; ensure coverage in training data |
| **low off-diagonal AUCᵢⱼ** (across clusters) | miscalibration / score scale mismatch           | per-cluster calibration (isotonic/Platt), standardise score bands | multi-task or conditional heads; monotonic constraints; domain shift correction          |
| **good AUC but bad Brier/LogLoss**           | overconfident probabilities                     | calibrate globally and per-cluster; temperature scaling           | recalibrate regularly with drift; loss-aware training                                    |
| **bad AUC but good Brier**                   | well-calibrated but non-separating features     | add discriminative features; cost-sensitive training              | collect new signals; redesign representation                                             |

# 6 Example thresholds + acceptance criteria
- intra-cluster AUCᵢᵢ: target ≥ 0.70; yellow 0.65–0.70; red < 0.65
- inter-cluster AUC heatmap: any cell < 0.60 (red) or drop > 0.05 from baseline triggers investigation
- Brier / LogLoss: track % change vs baseline; >10% relative worsen → calibration review
- drift (PSI/JS) on watch-list features: PSI ≥ 0.2 → check AUC/Brier for affected clusters, consider recalibration/threshold updates
# 7 Operating changes this allows
- cluster-aware thresholds: different decision thresholds per segment where calibration differs
- per-cluster calibration layers: light-weight isotonic or Platt per cluster (or per channel)
- model cards & MRMs: add an “AUC decomposition” section with the heatmap, worst-5 cells, and remediation notes for auditability
- release gate: ship only if all “material” clusters meet minimum AUCᵢᵢ and no inter-cluster cell is red; require a calibration plan if Brier deteriorates in any cluster
# 8 Pitfalls to avoid
- **AUC on one-class clusters:** if a cluster has only positives or only negatives, AUC is undefined; skip or merge
- **false confidence on tiny Ns:** always show counts and CIs; don’t overreact to small-n noise
- **over-segmentation:** too many clusters = sparse cells; prefer a compact, stable scheme for governance and a separate exploratory view for discovery
- **treating AUC as calibration:** great AUC with poor Brier/LogLoss is common; calibrate before thresholding or pricing decisions
