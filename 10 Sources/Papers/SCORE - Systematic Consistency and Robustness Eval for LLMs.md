---
type: paper
status: raw
quality:
topics: [llm-evaluation, adversarial-testing]
source: "https://arxiv.org/pdf/2503.00137"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# SCORE: Systematic COnsistency & Robustness Eval for LLM

## Metadata
- URL: https://arxiv.org/pdf/2503.00137
## Highlights
- SCORE = systematic consistency and robustness evaluation framework for large language models
    - unifies scattered robustness studies into one open, non-adversarial evaluation suite
    - emphasises multiple scenarios, accuracy-range reporting and consistency-rate tracking for a fuller view of model ability
- robustness dimensions evaluated
    - prompt-robustness = model should answer consistently across semantically equivalent prompts
        - ten neutral prompts per query reveal sensitivity to wording and reduce need for prompt-engineering
    - choice-order-robustness = swapping answer options (while keeping the correct letter constant) should not change predictions
        - exposes internal biases and instability
    - non-greedy inference-robustness = changing random seed during temperature-0 .7 sampling should not affect factual answers
        - tests stability under controlled randomness
- metrics
    - accuracy-range = min-to-max accuracy over all robustness scenarios
    - consistency-rate (cr) = fraction of prediction pairs that match across scenario variations
        - captures stability even when accuracy stays unchanged
    - key observation = higher mean accuracy often correlates with but does not guarantee higher consistency
- findings
    - minor input formatting tweaks (spacing, separators) can alter answers, highlighting fragility
    - accuracy spread and low cr show predictions can shift between wrong answers without affecting aggregate score
    - agieval dataset yields highest mean accuracy and cr, math yields lowest for all tested models
    - model size alone does not reliably predict robustness or consistency
- takeaway = evaluating llms with diverse, low-level robustness checks and reporting both accuracy-range and consistency-rate gives a more realistic picture of true capabilities

---
