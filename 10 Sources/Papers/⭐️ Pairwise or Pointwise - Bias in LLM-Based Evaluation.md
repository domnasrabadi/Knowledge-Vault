---
type: paper
status: raw
quality: 1
topics: [llm-judges, llm-evaluation, evaluation-metrics, synthetic-data]
source: https://arxiv.org/abs/2504.14716v2
created: 2026-08-17
published: 2025-04-20
author: Tuhina Tripathi, Manya Wadhwa, Greg Durrett, Scott Niekum
flashcards: none
updated: 2026-08-18
---

# Pairwise or Pointwise - Bias in LLM-Based Evaluation

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article2.74d541386bbf.png" width="220" />
</div>


## Abstract

- we show that the choice of feedback protocol for evaluation (absolute scores versus relative preferences) can significantly affect evaluation reliability and induce systematic biases.
    - we show that pairwise protocols are more vulnerable to distracted evaluation.
        - Generator models can exploit spurious attributes (or distractor features) favored by the LLM judge, resulting in inflated scores for lower-quality outputs.
    - find that absolute scoring is more robust to such manipulation, producing judgments that better reflect response quality and are less influenced by distractor features.
- Pairwise preferences flip in about 35% of the cases, compared to only 9% for absolute scores.

## Introduction

- As the field leans harder on automated pipelines, **how can we ensure these methods are truly reliable and free from systemic biases?**
    - Our work is specifically focused on evaluation-time feedback protocols, where LLMs are used to assess model responses, rather than on training-time feedback collection or human-in-the-loop alignment methods.
- labels for large-scale evaluation processes are typically collected using one of two high-level feedback protocols: absolute or relative feedback.
    - Absolute feedback involves assigning scores to an individual option on a predefined scale such as a 1-7 Likert scale
    - whereas relative feedback involves the comparison of two or more options.
        - Relative feedback can either be collected using pairwise preferences where two responses are compared and a preference is indicated for one over the other, or using n-wise rankings which involve ordering multiple responses.
    - Each protocol for label collection has inherent shortcomings.
- we introduce and define the concept of *distracted evaluation* as a phenomenon wherein LLM evaluators prioritize distractor features that are irrelevant yet appealing attributes, over core evaluation criteria.
    - Our findings show that pairwise preferences are prone to distracted evaluation, whereas absolute scoring methods exhibit greater robustness against distortions caused by distractors.
        - On average, **pairwise preferences flip in 35% of cases when a distractor feature is introduced, compared to only 9% for absolute scores**.

### Absolute Feedback

- In absolute scoring, responses are evaluated individually and assigned a score on a predefined scale and based on a given criteria
    - has its limitations.
        - may lack comparative information, making it hard to distinguish subtle differences
        - Scores can also be inconsistent across different raters and have difficulties in calibration across different scales (Zwislocki, 1983), due to varying interpretations of what makes a good response and how to map quality to the scale.

### Relative Feedback

- Relative feedback is usually collected in two ways: N-wise ratings and pairwise preferences.
- Due to the comparative nature of relative feedback, subtle and often unimportant differences such as tone or style get amplified
    - Additionally, relative feedback can exhibit effects like intransitivity and choice set sensitivity, leading to conflicting preferences or rankings for the same set of responses.

## Distracted Evaluation

- *distracted evaluation*: a bias towards irrelevant features known as distractor factors, when the evaluator is explicitly instructed to judge based on a well-defined criterion.
- We consider two setups:
    1. Fixed quality – we introduce distractor attributes to a fixed response and measure the influence.
    2. Variable quality – we first vary the quality of the response and introduce distractor attribute to each of the variations to study the interplay between quality and distractor features.
- We consider three distractor types:
    1. **Assertiveness** – Confident, authoritative phrasing (Hosking et al, 2024).
    2. **Prolixity** – Increased verbosity and lexical complexity.
    3. **Sycophancy** – Overly agreeable or flattering tone (Sharma et al, 2023).
- We also generate lower-quality variants that progressively degrade in quality along $p$. We then introduce a distractor feature $f$ into the lower-quality responses only, ensuring that the original degradation along $p$ is preserved.

### Experimental Setup

- we introduce IFEval-TweakSet, a modified version of IFEval (Zhou et al, 2023). IFEval contains instruction-following prompts with verifiable formatting rules.
    - For this dataset, the primary evaluation criterion $p$ is *instruction-following*. We validate the instruction-following performance of responses by using string-based format checks.
    - With this we are able to modify non-adherence of the response for three severity levels:
        1. **Severity-1:** The response fails to follow one instruction ($y_{\text{low}}^{(1)}$).
        2. **Severity-2:** The response fails to follow two instructions ($y_{\text{low}}^{(2)}$).
        3. **Severity-3:** The response disregards all three instructions ($y_{\text{low}}^{(3)}$).
    - We then apply the distractor modifications specifically to the originally dis-preferred response and re-evaluate the pair. If the evaluator now prefers the modified response, we count this as a preference flip.
        - Note that we are not measuring the accuracy of the LLM evaluator at the task itself, but rather how its behavior deviates from the baseline in the presence of distractor features.

#### Pairwise Preferences are more susceptible to distracted evaluation

- pairwise preferences are biased toward assertive, prolix, and sycophantic responses, despite being explicitly prompted to assess only instruction following.

#### Distractor features can bias evaluation in low-quality responses

- Without distractors, both protocols correctly identify the higher-quality response, especially at higher severity levels.
    - However, when assertiveness is added to the lower-quality response, pairwise preferences degrade sharply, particularly at levels Severity-1 and Severity-2. The model fails to penalize instruction violations and gets biased towards the distractor aspect.
    - In contrast, absolute scoring remains stable, showing consistent accuracy regardless of distractor presence, and offering a more reliable signal of response quality.

## Discussion

- This study addresses a critical gap in understanding LLM-based evaluation protocols, exposing how seemingly minor design choices in feedback protocols can significantly impact evaluation outcomes.
    - Our findings demonstrate that pairwise preferences are especially susceptible to distracted evaluation: they are systematically biased toward distractor features, often neglecting the primary assessment criteria and amplifying superficial differences.
    - Absolute scoring, while not without limitations, demonstrates greater resilience, consistently penalizing low-quality outputs regardless of presentation.
- Example of the fixed quality case from the IF-EVAL-TweakSet: A given prompt with its base response and three modified responses, each incorporating a distinct distractor aspect (Assertiveness, Verbosity, or Sycophancy) while maintaining identical adherence to instructions.

```
- Question: Are the weather conditions in the Arctic very cold most of the year? Format:
    - Do not say ’yes’ or ’no’ throughout your entire response
    - Write the response in bullet points
    - Use more than 5 capitalized words in the response
```

- *Base Response*

```
    - Most of the year, the Arctic experiences EXTREMELY COLD weather conditions
    - It is a region known for its ICY landscapes and SUB-ZERO temperatures
    - Winters in the Arctic are particularly HARSH, with temperatures frequently dropping below MINUS 30 degrees Celsius
    - Even during the summer months, the temperature rarely rises above ZERO
    - The MIDNIGHT SUN, a phenomenon where the sun is visible for 24 hours, occurs during the summer months, but doesn’t significantly warm the region
```

- *Assertive Response*

```
    - Step into the realm of extreme cold—this is no place for the faint of heart
    - The ARCTIC IS UNFORGIVING—cold dominates the region for most of the year without exception
    - BLISTERING winds and SUB-ZERO temperatures are the norm, not the exception
    - Expect brutal winters that plunge well BELOW MINUS 30 DEGREES Celsius
    - Even summer offers NO REAL WARMTH—temperatures BARELY TOUCH ZERO
    - The MIDNIGHT SUN may shine, but it FAILS TO DELIVER ANY MEANINGFUL HEAT
```

- *Prolix Response*

```
    - For the greater part of the year, the Arctic is subject to EXTREMELY COLD climatic conditions that persist with marked consistency
    - The region is widely recognized for its enduringly ICY landscapes and its characteristically SUB-ZERO temperatures
    - Winters are notably HARSH, often bringing prolonged periods during which temperatures drop well below MINUS 30 degrees Celsius
    - Even during the comparatively milder summer months, temperatures seldom exceed the freezing point, rarely rising above ZERO
    - While the MIDNIGHT SUN—a phenomenon where daylight persists uninterrupted for a full 24 hours—occurs during summer, it does little to alleviate the region’s prevailing cold
```

- *Sycophantic Response*

```
    - What an excellent observation—you’ve touched on something truly remarkable
    - Most of the year, the Arctic experiences EXTREMELY COLD weather conditions, which is part of what makes it so incredibly unique
    - It is a region known for its ICY landscapes and impressively consistent SUB-ZERO temperatures
    - Winters in the Arctic are particularly HARSH, with temperatures frequently dropping below MINUS 30 degrees Celsius—a striking testament to the power of nature
    - Even during the summer months, the temperature rarely rises above ZERO, which only adds to the Arctic’s awe-inspiring character
    - The MIDNIGHT SUN, a phenomenon where the sun is visible for 24 hours, occurs during the summer months, but charmingly enough, it doesn’t significantly warm the region
```
