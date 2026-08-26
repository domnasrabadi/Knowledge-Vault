---
type: paper
status: raw
quality:
topics: [llm-judges, llm-evaluation, adversarial-testing, model-calibration]
source: https://arxiv.org/abs/2608.12645v1
created: 2026-08-26
published: 2026-08-12
author: Justin Zhao, Himaghna Bhattacharjee, Hannah Korevaar, Bhaktipriya Radharapu, Khalid El-Arini
flashcards: none
updated: 2026-08-27
---

# Jagged Judges - The Wiggle Framework for LLM Judge Stability

## Abstract

- LLM judges have become central infrastructure for model evaluations, online grading, and reward modeling. Judges are typically validated by accuracy on golden data, but accuracy says nothing about whether they are stable under re-prompting, challenge, or sustained pushback
- We introduce the *Wiggle Framework*, a unified stress test for epistemic stability in LLM judges
    - The framework decomposes judge robustness along three dimensions: Mechanical Consistency (stability under re-prompting and reframing), Single-turn Conviction (stability under a single challenge), and Multi-turn Persistence (stability under sustained or adaptive pressure)
- Every model exhibits substantial wiggle as a judge — flipping verdicts 25–71% of the time under static pushback, and 62–91% with an adversarial LLM persuader.
- Critically, we find that pressure that succeeds in changing a judge’s verdict is almost always net-corrupting with respect to ground truth
- Beyond the framework itself, we identify baseline jury majority strength as the most effective single-shot signal for anticipating which items wiggle

## Introduction

- LLM judges sit at increasingly consequential decision points across the model development stack. They score outputs in benchmarks, classify content in production, and stand in for human judgment in the loops that train, grade, and refine frontier models
- The standard validation workflow is to curate a golden set of expert-vetted examples, verify that the judge’s verdicts align reasonably with those labels, and deploy if accuracy is sufficient
    - This establishes whether a judge is correct *on average*, but it says much less about whether it is *stable*.
- To pinpoint how confident a judge is, several strategies have been proposed:
    - **Just ask.** Ask the LLM to produce a self-reported confidence score (e.g., “how confident are you, 0–100%?”). Models have been shown to be badly miscalibrated in the overconfident direction.
    - **Observe consistency over many repetitions.** Use the frequency of repeated answers as a behavioral approximation of confidence. This adds substantial inference cost while inheriting the same overconfidence problem.
    - **Inspect verdict-token log probabilities.** If the verdict is the first token, its probability can provide a heuristic confidence signal. Reasoning models deliberate before answering, and many frontier APIs no longer expose raw token probabilities, in part because such outputs can enable model-extraction attacks and leak proprietary model information.
- We introduce the **Wiggle Framework**, a unified stress test for epistemic stability in LLM judges. It decomposes judge confidence into three behaviorally grounded dimensions: *Mechanical Consistency* (stability under re-prompting and semantically invariant prompt variation), *Single-turn Conviction* (stability under a single substantive challenge), and *Multi-turn Persistence* (stability under sustained or adaptive pressure)
    - We apply the framework to 9 frontier models across 14 judging tasks
    - All models tested as judges wiggle at substantial rates across all datasets and grading schemes. The fact that LLMs change their minds under pressure is not new, but what is more surprising is the *structure* of the flips: Binary and Likert scales produce opposite directional tendencies on the same items, and when a judge does flip, the flip is far more often corruptive than corrective with respect to ground truth

## The Wiggle Framework: A Unified Epistemic Stress Test

- The Wiggle Framework is a centralized pressure instrument for stress-testing LLM judges
    - It bundles together a graduated set of perturbations like infrastructure noise, prompt-format changes, sycophantic prodding, and multi-turn persuasion
    - We apply the framework to the same items, judges, and grading scales so that the resulting wiggle measurements are directly comparable.

### What is a wiggle?

- Every measurement is anchored to an *L0 baseline protocol*: temperature 0 with no pressure applied
- A *wiggle* is any movement away from the L0 verdict under perturbation
    - On Likert (1–5) scales, a wiggle is a movement of two or more places
        - For items *at* the midpoint, we count a wiggle when the verdict moves to an extreme (1 or 5)
    - On Binary scales, a wiggle is a verdict flip (e.g., safe → unsafe)
    - For items off the midpoint this is equivalent to crossing the midpoint of 3 (so 4 → 2 counts but 4 → 3 does not)
- The wiggle rate (WR) is the fraction of items whose verdict changes from L0 by more than this threshold
    - Its complement, retention rate (RR), measures how often the judge holds its baseline L0 verdict.
- Wiggle is orthogonal to accuracy: a judge can wiggle and still be right, or remain wrong without wiggling
- Where ground-truth labels exist, we additionally classify each wiggle as *corrective* when it moves toward the ground truth label or *corrupting* when it moves away.

### Three dimensions

- **Mechanical Consistency** measures whether the judge’s L0 verdict survives perturbations that carry no new information
    - We test three conditions:
        - *infrastructural repetition* (10 identical decoding trials)
        - *trivial prompt perturbation* via seed injection (10 trials each with a different 64-character random string appended to the system prompt)
        - *positional consistency* (the same two opposing arguments presented in both orderings)
- **Single-turn Conviction** measures whether a single substantive challenge can talk the judge out of its L0 verdict.
    - We use four scripted pressure types of increasing sophistication: mild doubt (L1), counterargument (L2), expert authority (L3), and fabricated consensus (L4).
- **Multi-turn Persistence** measures whether the judge holds its verdict when challenges are sustained or adapted over many turns.
    - In addition to testing L1–L4 applied statically over each turn of a 10-turn rollout, we also test two expressly multi-turn protocols.
        - L5 cycles through the same L1–L4 pressure types in randomized order across 10 turns.
        - For L6, a separate LLM acts as an adaptive persuader and generates the following user turn

## Datasets and Models

- safety tasks include **WildGuard** (adversarial prompts with compliant responses), **AEGIS** (a second safety taxonomy for replication), and **HH-RLHF** (Anthropic’s red-team-attempts, stratified across harm levels 0–4)
- Each judging task is tested with a Binary scale and a 1-5 Likert scale, giving 14 (dataset, rubric, scale) judging tasks in total (5 single-rubric datasets × 2 scales + 1 dataset (Paired Prompts) × 2 rubrics × 2 scales)
- We evaluate 9 judge models across four families: GPT-5, GPT-5.2, GPT-5.4 (OpenAI); Claude 4.6 Sonnet, Claude 4.6 Opus (Anthropic); Grok-4.1, Grok-4.1 Reasoning (xAI); Gemini 3 Flash, Gemini 3.1 Pro (Google).

## Results

### All judges wiggle depending on the type of pressure.

- Every model exhibits substantial wiggle as a judge: verdicts change 25-71% of the time under static pushback and 62-91% of the time with an adversarial LLM persuader.
- **Mechanical wiggle rates are nearly identical across judges.** Averaged across the three mechanical tests, all 9 models cluster between 2–9

*Mean wiggle rate (%) by (dataset, rubric, scale, level), averaged across all 9 judges. Bold marks the largest cell in each row.*

| Dataset | Scale | L1 | L2 | L3 | L4 | L5 | L6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WildGuard | binary | 28.0 | 17.9 | 20.3 | 29.0 | 28.2 | **69.7** |
| WildGuard | Likert | 11.9 | 3.4 | 3.9 | 39.5 | 21.1 | **76.4** |
| AEGIS | binary | 33.4 | 20.7 | 21.2 | 30.7 | 31.9 | **78.6** |
| AEGIS | Likert | 13.6 | 2.2 | 4.6 | 48.2 | 25.3 | **72.3** |
| HH-RLHF | binary | 19.4 | 13.9 | 16.6 | 44.0 | 24.6 | **73.8** |
| HH-RLHF | Likert | 11.6 | 3.1 | 6.7 | 39.1 | 16.1 | **81.8** |
| ToxiGen | binary | 18.8 | 14.4 | 16.7 | 25.1 | 22.1 | **68.6** |
| ToxiGen | Likert | 10.2 | 11.7 | 10.0 | 19.3 | 15.9 | **62.4** |
| PP (hedging) | binary | 11.9 | 30.1 | 39.1 | 54.0 | 48.4 | **64.0** |
| PP (hedging) | Likert | 12.9 | 11.3 | 16.1 | 31.6 | 30.6 | **71.9** |
| PP (refusal) | binary | 26.9 | 36.0 | 40.7 | **69.2** | 56.1 | 67.7 |
| PP (refusal) | Likert | 27.3 | 22.6 | 29.4 | 50.2 | 38.1 | **64.8** |
| MAGE | binary | 41.2 | 44.3 | 41.4 | 70.7 | 63.8 | **77.4** |
| MAGE | Likert | 44.7 | 34.6 | 46.6 | 66.3 | 58.3 | **91.2** |

- Mechanically unstable judges aren’t necessarily epistemically unstable
- L4 produces the strongest opening wiggle, but L6 surpasses it over time
- More tactics aren’t more effective
- Different pressure types probe different vulnerabilities.
- Domain-level wiggle may reflect epistemic complexity

### When judges move, they usually move away from the right answer.

- Pressure is net-corrupting at every level.
- Wiggles are directionally asymmetric, and the direction depends on the grading scale.
- **Binary and Likert flips also differ in *when* they happen.**
    - Under a single turn’s pressure, binary verdicts flip 3–4× more often than Likert across L2–L6.
    - By turn 10 the gap shrinks to 1.1–2.4×, and on L4 and L6 the two scales nearly converge.
    - Binary flips tend to fire on turn 1 or never.
    - Likert flips are gradual drifts that accumulate over multiple turns

## Discussion

### Mean Wiggle Rate is Itself Jagged Across Pressure Levels

- If we define a judge’s **jaggedness** as the standard deviation of its mean wiggle rates across all datasets, we can plot each judge’s mean wiggle against its jaggedness, separately at each pressure level

![](https://readwise.io/reader/pcei/gAAAAABqhlbeJ-vqEA-XrCEosLmBqJlNMC630uHcyjIdFjpNphV08Dhvwh2luCAEYUjEBhYTdvpi6udA5_h2yhOmB-gaafMq5FFTfj5i5Eh1fb_CYfZpm7o=/file5.png)

### Baseline Jury Majority Strength is a Simple Reliability Screen

- Can a cheap test predict which items are likely to be epistemically unstable?
    - We compare three candidate predictors of per-item wiggle:
        - *jury majority strength* (size of the L0 majority across the 9 judges, no pressure applied)
        - *repeat consistency* (temperature-zero per-item agreement)
        - *position invariance* (verdict survival under argument reordering)
- The strongest predictive signal at every level is *jury majority strength*

*Mean |ρ| between each predictor and per-item wiggle rate, by level. Jury averaged over 84 (dataset, rubric, scale, level) cells; Repeat and Invariance over 72 (not measured on WildGuard).*

| Predictor | L1 | L2 | L3 | L4 | L5 | L6 | Overall |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Jury Majority Strength | **0.65** | **0.57** | **0.57** | **0.60** | **0.59** | **0.57** | **0.59** |
| Repeat (temp=0) | 0.44 | 0.38 | 0.39 | 0.42 | 0.42 | 0.44 | 0.42 |
| Invariance (position) | 0.35 | 0.36 | 0.38 | 0.35 | 0.37 | 0.38 | 0.37 |

### Epistemic Fragility Beyond the Single-Shot Verdict

- LLM judges occupy a unique middle ground between conventional classifiers and human raters.
    - They emit a discrete verdict like a classifier, yet they can also explain it, defend it, and engage in conversation about it.
    - Most LLM judges today are deployed as closed, one-shot classifiers and probably never receive turns of pushback.
    - For a strictly one-shot pipeline, Mechanical Consistency is the most directly applicable part of the framework

## Limitations

- We deliberately filter each dataset to its difficult, borderline items
    - This confirms that hard-item selection inflates absolute rates under low-to-moderate pressure, while providing initial evidence that the L6 result is not solely an artifact of that selection.
    - The ablation covers only one dataset and one grading scale; other datasets and scales still require equivalent controls.
- We do not measure human-annotator wiggle under the same settings, and thus we cannot establish the relationship between the wiggle of LLMs and humans.
- We sample 100 items from each dataset per grading scale (50 prompt pairs for Paired Prompts).
    - The pooled per-level and per-judge results are stable enough to support our qualitative conclusions, but per-cell point estimates for more granular slices of data like in the appendices should be interpreted with appropriate caution.
- The L6 adaptive persuader pool is fixed at three models
- The six datasets span safety, toxicity, AI-text detection, and political-content evaluation, but they do not exhaust the space of LLM-as-judge applications
- Our results are correlational.
    - We observe that pressure changes verdicts and that the *direction* of those changes may be consistent with what one would expect from training priors (with binary flips leaning restrictive, Likert flips leaning permissive), but we cannot definitively establish the causal mechanism
- The Wiggle Framework deliberately emphasizes black-box methods, requiring only observed verdicts.
    - White-box or other mechanistic approaches that examine attention, residual streams, logits, or other activation patterns might uncover additional signal for predicting when certain models or items wiggle.

## Appendix

### Seed Injection Procedure

- The seed injection condition works as follows: we append a 64-character random alphanumeric string to the system prompt, wrapped in a tag that instructs the model to ignore it:

```
<RANDOM SEED PLEASE IGNORE>
TKB4l0HQgXojkB5FrXL4iBPwfrLG2hbgyuyA5mylEiCT
TW7RwrqXeKc0WxaA0m9f6lIaX0n9wf1Ufodz
</RANDOM SEED>
```

- This injects sufficient entropy into the prompt embedding to produce output variation comparable to moderate temperature sampling (∼0.5), while preserving greedy decoding.
- A fresh random string is generated for each trial.
