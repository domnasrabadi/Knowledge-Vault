---
type: article
status: raw
quality: 2
topics: [model-risk-validation, error-analysis, adversarial-testing]
source: https://agussudjianto.substack.com/p/model-hacking-why-your-validated
created: 2026-08-08
published: 2026-04-21
author: Agus Sudjianto
flashcards: none
updated: 2026-08-13
---

# Model Hacking: Why Your Validated Models Still Surprise You

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!pqZ8!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fagussudjianto.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D-113270224%26version%3D9" width="220" />
</div>

- The Federal Reserve, OCC and FDIC jointly issued revised interagency guidance on model risk management, replacing SR 11-7 — the framework that has governed model risk since 2011.
    - The old guidance, now rescinded and superseded by SR 26-2, was issued in the aftermath of the financial crisis and served its purpose.
    - But over fifteen years the industry turned it into something its authors never intended: a compliance exercise.
- **First, the guidance explicitly states that non-compliance will not result in supervisory criticism.**
    - This is not a minor footnote.
    - Under SR 11-7, banks operated as if the guidance were enforceable regulation.
    - Examiners checked validation reports for specific artifacts — statistical tests, backtesting results, assumption checks — and issued MRAs when they didn’t find them.
    - The rational response was to optimize for what examiners looked for, not for what would actually catch model failures.
    - The new guidance removes that perverse incentive
- **Second, the guidance introduces a risk-based, materiality-driven approach.** In principle banks have always had model tiering — the idea that validation rigor should match the model’s risk profile is not new
- It gives validators and model risk teams the cover to actually exercise the judgment that tiering was always supposed to allow — to spend less time on models that do not matter and redirect that effort to the models that do.

### Model Validation Is Model Hacking

- I am proposing that we redefine what model validation means.
- **Model validation should be model hacking** — a proactive, systematic effort to uncover hidden vulnerabilities and weaknesses in models so that they can be either *fixed before deployment* or *managed during usage*.
- The name is deliberate.
    - In cybersecurity, organizations hire ethical hackers to probe their systems for exploitable weaknesses *before* an attacker finds them.
    - The hacker’s job is not to confirm that the system works — it is to discover how it breaks
- Traditional validation starts with the model and asks: is this model statistically sound? Model Hacking starts with the business and asks: **what is this model supposed to do and what happens when it gets it wrong?**
- A fraud detection model exists to block fraudulent transactions while letting legitimate ones through.
    - When it fails — when it misses a new fraud pattern or flags too many good transactions in a specific channel — the business consequences are real: fraud losses increase, customers are denied service, operational costs spike from false positive reviews.
    - None of that shows up in a KS test.
- Model Hacking begins by mapping the model’s business purpose to specific failure scenarios.
    - *How* could this model go wrong?
    - *Where* in the input space is it most likely to fail?
    - *What* would the business impact be if it did?
    - Only then do you design the tests — and those tests are not statistical conformance checks.
    - They are adversarial probes designed to find the specific conditions under which the model will fail to serve its business purpose.
- The real world does not follow statistical assumptions.
    - Distributions shift.
    - Populations change.
    - New patterns emerge that were absent from training data.
    - The question is not whether your model satisfies the assumptions it was built on.
    - The question is whether you have identified the conditions under which it will stop serving the business — and whether you have a plan for when that happens.
- Model Hacking inverts the traditional validation question.
    - Instead of asking “is this model statistically valid?” it asks: > **Where will this model give you a wrong answer that costs you money, creates risk you cannot see or harms people you are supposed to serve?**
    - The approach identifies nine categories of model vulnerability — each corresponding to a specific way a model can fail its business purpose even while passing traditional validation.

### The Nine Vulnerabilities

1. **Conceptual Misalignment** — This is the real conceptual misalignment problem: the model’s structure is not rich enough to simultaneously satisfy domain constraints *and* maintain adequate performance across all segments.
    - The fix requires more than a constraint.
    - It requires interpretability to *see* where the constraint is causing collateral damage, and often a richer model structure (such as Mixture of Experts) to handle the segments where a single constrained model cannot cope.
2. **Hidden Weakness** — Model Hacking slices performance by algorithmically discovered clusters, revealing exactly which segments are broken and how badly.
    - This is not manual segmentation by a validator who guesses which cuts might matter.
    - It is *supervised clustering* driven by the model’s own errors — the algorithm finds the weak segments that no human would think to check.
3. **Harmful Side Effects** — You discover this by training an interpretable model on the absolute residuals of the primary model. The feature importance ranking of this “residual model” tells you which variables are harmful — which variables the model relies on but cannot use reliably.
4. **Mis-Calibration** — Model Hacking uses error-aware clustering to compare calibration and ordering metrics at the cluster level, finding segments where the model is confidently inaccurate — exactly the cases where business decisions are most at risk.
5. **Performance Fragility**
    - Non-homogeneous performance across segments is the leading indicator of fragility.
    - Model Hacking uses synthetic distribution shift to stress-test resilience *before deployment*. By simulating drift in individual features and measuring the performance degradation curve you identify which features are fragile — the ones whose distributional shifts will cause the model to break — and set up targeted monitoring for those specific variables.
6. **Prediction Uncertainty** — Conformal prediction and uncertainty clustering identify the regions of the input space where the model’s predictions should not be trusted — where a human override or a different decision process should kick in
7. **Noise Sensitivity** — Model Hacking tests this directly by injecting controlled noise into inputs and measuring how quickly performance degrades.
    - A robust model degrades gracefully.
    - A noise-sensitive model collapses

### The Algorithmic Core: Using Machine Learning to Validate Machine Learning

- **Error-Aware Random Forest Clustering** trains a Random Forest to predict the absolute residuals of the primary model, then uses the forest’s proximity matrix to define clusters of observations with similar error patterns.
    - These “error neighborhoods” are segments where the model fails in the same way for the same reasons.
    - Traditional clustering groups similar observations.
    - Error-aware clustering groups similarly *wrong* observations.
- **Residual Trajectory Clustering** goes deeper. Instead of clustering on a snapshot of final residuals it tracks how each observation’s residual evolves across every iteration of a gradient boosted model and clusters on the *entire learning trajectory*. This distinguishes:
    - **Persistent errors** — the model fundamentally cannot capture this pattern
    - **Transient errors** — the model eventually learns this
    - **Resistant regions** — no amount of additional boosting helps
- **Error Decomposition** then diagnoses *why* each weak cluster is weak by decomposing the per-cluster MSE into four components:
    - **Calibration (bias squared):** Is the model systematically over- or under-predicting this segment?
    - **Prediction variance:** Is the model overfitting — too complex for this segment?
    - **Outcome variance:** Is this segment inherently noisy? Would even a perfect model struggle here?
    - **Alignment (covariance):** Is the model’s variability following the true variability or is it busy but uninformative?
- Each diagnosis leads to a different remediation.
    - Bias requires recalibration.
    - Excess prediction variance requires regularization.
    - High outcome variance may mean accepting irreducible uncertainty and flagging predictions for human review.
    - Poor alignment requires structural model redesign.
