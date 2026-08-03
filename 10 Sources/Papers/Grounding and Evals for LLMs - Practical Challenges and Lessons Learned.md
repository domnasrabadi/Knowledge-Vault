---
type: paper
status: raw
quality:
topics: [llm-evaluation, rag]
source: "https://arxiv.org/pdf/2407.12858"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# Grounding & Evals for LLMs: Practical Challenges & Lessons Learned (Survey)

## Metadata
- Author: Oracle
- Category: pdf
- URL: https://arxiv.org/pdf/2407.12858
## Highlights
- generative ai harms = key risk categories needing proactive management
    - hallucination = ungrounded answers not supported by sources
    - jailbreak / prompt injection = attack that circumvents alignment or reveals hidden instructions
    - harmful content = toxic, violent, or manipulative output
    - copyright infringement = generation that reproduces protected material
- risk management framework = identify → measure → mitigate → operationalise
    - identification = iterative red teaming + stress testing to surface potential harms
    - measurement = design test sets and metrics to quantify harm frequency + severity
    - mitigation = four layers
        - model layer = finetune on curated or preference-ranked data, add fairness or safety regularisers
        - safety system layer = classifiers, content filters, watermarking, constrained decoding
        - application layer = prompt engineering, grounding via retrieval-augmented generation (rag), selective prediction with confidence scores
        - positioning layer = user interface choices, rate limits, deployment context controls
    - operationalisation = monitor live traffic, detect distribution drift, update mitigations quickly
- holistic evaluation pillars = decide if llm is fit for enterprise deployment
    - truthfulness = detect + recover from hallucinations, ensure responses are informed and relevant
    - safety & alignment = prevent or flag unsafe output across lifecycle stages (data curation → rlhf → runtime filtering)
    - bias & fairness = find and fix demographic performance gaps using counterfactual data, finetuning, reweighting
    - robustness & security = test against prompt noise, distribution shift, adversarial jailbreaks and injection attacks
    - privacy, unlearning & copyright = minimise pii memorisation, enable forgetting, add watermarking and pii detection
    - calibration & confidence = quantify uncertainty, defer to humans when confidence low (selective prediction, self-evaluation)
    - transparency & causal intervention = explain internal reasoning (chain-of-thought, mechanistic interpretability) and edit factual associations directly
- grounding = ensuring every claim cites a user-specified knowledge base
    - rag workflow = retrieve context → generate answer → verify grounding
        - retrieval improvements = pick right chunk size, decompose queries, supervise via generation quality, use llm as index
        - generation improvements = fine-tune on (prompt, context, answer) triples, use rl to reward grounded answers, constrained decoding or best-of-n sampling
    - grounding verification =
        - nli models check if context entails each claim (cheap, but weak on reasoning)
        - llm-based entailment checks (stronger reasoning, higher cost)
        - sentence-level checks enable claim-level citations
    - iterative revision = automatically rewrite answers when grounding test fails
    - corpus tuning = pretrain on domain corpus to embed niche vocabulary (e.g., medical)
- observability in production = continuous monitoring and response
    - metrics dashboard tracks quality, safety, bias, drift
    - ai safety layer between model and app catches toxicity or policy violations in real time
    - feedback loops combine user reports with automatic detectors to trigger retraining or prompt updates
- evaluation best practices =
    - run robustness tests with prompt perturbations and multiple seeds, average scores, report variance
    - include subgroup analysis to expose under-performing demographics
    - differentiate “unknown unknowns” (unexpected failures) from adversarial attacks, plan for both
    - employ selective prediction and uncertainty estimation to balance automation with human oversight

---
