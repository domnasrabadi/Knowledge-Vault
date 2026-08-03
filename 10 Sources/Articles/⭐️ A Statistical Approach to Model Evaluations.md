---
type: article
status: raw
quality: 1
topics: [llm-evaluation, evaluation-metrics]
source: ""
created: 2025-12-08
published: 2024-11-19
author: anthropic.com
flashcards: none
updated: 2026-01-01
---

# A statistical approach to model evaluations

<div align="center">
  <img src="https://cdn.sanity.io/images/4zrzovbb/website/c0cfb012481d7748798c00b58aaeb5117d648a6e-2560x1440.png" width="220" />
</div>

Source: https://www.anthropic.com/research/statistical-approach-to-model-evals

Exported at: `2025-12-29T04:27:37Z`


#### Recommendation #1: Use the Central Limit Theorem

- To compute an overall eval score, each question is separately scored, and then the overall score is (usually) a simple average of these question scores.
- we argue that the real object of interest should not be the *observed* average, but rather the *theoretical* average across all possible questions.
- ![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fb34871a36ad66fa0330e3ad6488ee87eb96bddda-2401x1260.png&w=3840&q=75) If we imagine that eval questions were drawn from a “question universe,” then eval scores will tend to follow a normal distribution, centered around the average score of all possible questions.
- we encourage researchers to report the SEM, derived from the Central Limit Theorem, alongside each calculated eval score—and we show researchers how to use the SEM to quantify the difference in theoretical means between two models. A 95% [confidence interval](https://en.wikipedia.org/wiki/Confidence_interval) can be calculated from the SEM by adding and subtracting 1.96 × SEM from the mean score.

#### Recommendation #2: Cluster standard errors

- Many evals violate the above assumption of independently selected questions, and instead consist of groups of closely related questions.
- For these evals, each question’s selection from the “question universe” is no longer independent. Because including several questions about the same passage of text will yield less information than selecting the same number of questions about different passages of text, a naive application of the Central Limit Theorem to the case of non-independent questions will lead us to underestimate the standard error—and potentially mislead analysts into drawing incorrect conclusions from the data.
- Fortunately, the problem of [clustered standard errors](https://en.wikipedia.org/wiki/Clustered_standard_errors) has been extensively studied in the social sciences. When the inclusion of questions is non-independent, we recommend clustering standard errors on the unit of [randomization](https://en.wikipedia.org/wiki/Randomization) (for example, passage of text)
- ![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Ff6f90f93dc66380904709a3ef4d63b92332871fd-2401x1260.png&w=3840&q=75) If questions arrive in related clusters—a common pattern in reading-comprehension evals—eval scores will be more spread-out compared to the non-clustered case.

#### Recommendation #3: Reduce variance within questions

- A key insight of our paper is to decompose a model’s score on a particular question into two terms that are added together: • The mean score (the average score that the model would achieve if asked the same question an infinite number of times—even if the model might produce a different answer each time); and • A random component (the difference between a realized question score and the mean score for that question).
- Our paper highlights two strategies for reducing variance in the random component depending on whether or not the model is asked to think step by step before answering (a prompting technique known as CoT, or chain-of-thought reasoning).
- If an eval uses chain-of-thought reasoning, we recommend resampling answers from the same model several times, and using the question-level averages as the question scores fed into the Central Limit Theorem.
- ![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fefef59a06ddeb530fa15f31dc0937f28f70f655b-2401x1260.png&w=3840&q=75) If a model produces answers non-deterministically, then generating (and grading) several answers per question will result in less spread-out eval scores.
- If the eval does not use chain-of-thought reasoning (i.e., its answers are not “path dependent”), we note that the random component in the score may often be eliminated altogether using next-token probabilities from the language model.

#### Recommendation #4: Analyze paired differences

- Eval scores don’t have any meaning on their own; they only make sense in relation to one another (one model outperforms another model, or ties another model, or outperforms a person).
- But could a measured difference between two models be due to the specific choice of questions in the eval, and randomness in the models’ answers? We can find out with a [two-sample *t*-test](https://en.wikipedia.org/wiki/Student%27s_t-test), using only the standard errors of the mean calculated from both eval scores.
- In practice, we find the correlation of question scores on popular evals between frontier models to be substantial—between 0.3 and 0.7 on a scale of −1 to +1. Put another way, frontier models have an overall tendency to get the same questions right and wrong. Paired-difference analysis thus represents a “free” variance reduction technique that is very well suited for AI model evals. Therefore, in the interest of extracting the clearest signal from the data, our paper recommends reporting pairwise information—mean differences, standard errors, confidence intervals, and correlations—whenever two or more models are being compared.

#### Recommendation #5: Use power analysis

- The flip side of the statistical significance coin is statistical power, which is the ability of a statistical test to detect a difference between two models, assuming such a difference exists. If an eval doesn’t have very many questions, confidence intervals associated with any statistical tests will tend to be wide.
- This means that models will need to have a large underlying difference in capabilities in order to register a statistically significant result—and that small differences will likely go undetected.
- We believe that power analysis will prove helpful to researchers in a number of situations. Our power formula will inform evaluators of models about the number of times to re-sample answers from questions (see Recommendation #3 above), as well as the number of questions that may be included in a random subsample while retaining the desired power properties.
