---
type: book
status: distilled
quality:
topics: [data-science]
source: ""
created: 2025-08-02
published:
author: ""
flashcards: none
updated: 2025-08-02
---

1. **Core Philosophy: Statistics as a Way of Thinking**
    - Statistics is a _mindset_ for making sense of uncertainty, not just formula application.
    - Focus on understanding data in context; question assumptions, interpret evidence, and avoid cognitive biases.
    - Aim to develop critical thinking: interrogate claims, weigh evidence, and be comfortable with uncertainty.
2. **Understanding Uncertainty**
    - **Descriptive vs. Inferential Statistics**
        - Descriptive: summarise observed data (mean, median, variability).
        - Inferential: draw conclusions about a broader population from a sample.
    - **Sources of Uncertainty**
        - Variability, measurement error, sampling error, and model limitations.
        - Statistical methods quantify and reduce—but do not eliminate—uncertainty.
3. **Foundational Concepts**
    - **Distributions**
        - Understand how data are distributed (normal, skewed, multimodal); probability distributions model expected behaviour under uncertainty.
    - **The Law of Large Numbers**
        - Larger sample sizes yield more stable, reliable estimates.
    - **Central Limit Theorem**
        - Sampling distributions of the mean approach normality as sample size grows—a cornerstone for many inferential techniques.
4. **Modeling and Inference**
    - **Hypothesis Testing**
        - Compare observed data to what would be expected under a null hypothesis.
        - P-values reflect how incompatible the data are with the null—not the probability the null is true.
        - Avoid binary “significant vs. not” thinking; consider effect sizes and confidence intervals.
    - **Confidence Intervals**
        - Provide a range of plausible values for parameters; more informative than p-values alone.
5. **Bayesian Thinking**
    - **Bayesian Inference**
        - Update prior beliefs in light of new data using Bayes’ Theorem.
        - Offers a coherent, flexible framework for reasoning under uncertainty.
        - Emphasises transparency about assumptions and interpretability of results.
    - **Contrast with Frequentist Approach**
        - Frequentist methods rely on long-run properties and fixed hypotheses; Bayesian methods allow direct probability statements about hypotheses.
6. **Data and Causality**
    - **Correlation vs. Causation**
        - Statistical association does not imply causality.
        - Use graphical models (e.g., DAGs) and causal inference frameworks to assess causal claims.
    - **Confounding and Bias**
        - Identify and adjust for variables that distort associations.
        - Randomised experiments are ideal; observational data can still be useful with proper controls.
7. **Statistical Pitfalls and Misinterpretation**
    - **P-Hacking and Data Dredging**
        - Repeated testing inflates false positives; avoid cherry-picking.
        - Pre-register hypotheses and apply correction methods when needed.
    - **Overfitting and Model Complexity**
        - Overly complex models may capture noise rather than signal.
        - Use model comparison and cross-validation to assess generalisability.
    - **Misleading Visualisations**
        - Visual summaries must be accurate, contextually framed, and clearly labelled.
        - Be sceptical of graphs without proper axes, scales, or framing.
8. **Best Practices in Data Analysis**
    - **Transparency and Reproducibility**
        - Share data, code, and analytic workflows; use version control and document decisions clearly to uphold scientific integrity.
    - **Exploratory Data Analysis (EDA)**
        - Essential for understanding data structure, generating hypotheses, and spotting anomalies before formal modelling.
    - **Modeling as an Iterative Process**
        - Models are simplifications; continuously evaluate, refine, validate, and return to the underlying research question.
9. **Final Insights**
    - **Statistics Is Not Just Math**
        - It’s a toolkit grounded in logic and scientific philosophy for learning from data.
    - **Humility in the Face of Uncertainty**
        - Good analysis seeks what the data honestly suggest—not to prove preconceived points.
        - Encourage doubt, rigor, and openness to being wrong.