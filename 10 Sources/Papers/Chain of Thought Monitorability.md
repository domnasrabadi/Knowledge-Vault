---
type: paper
status: structured
quality:
topics: [llm-risks, model-monitoring]
source: ""
created: 2025-07-17
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Tomek Korbak, Mikita Balesan, Elizabeth Barnes, Joe Benton, Mark Chen, Allan Dafoe, Scott Emmons, David Farhi, Dan Hendrycks, Evan Hubinger, Erik Jenner, Victoria Krakovna, David Lindner, Aleksander Nandy, Neel Nanda, Jakub Pachocki, Mary Phung, J...
- Category: pdf
- Document Tags: good 
- URL: https://readwise.io/reader/document_raw_content/338081212
# 2 Highlights
- chain of thought (CoT) monitoring = inspecting an ai system’s natural-language reasoning traces to uncover intent, goals, or misbehavior
    - ai systems that think in human language make safety monitoring feasible
    - prompting models to “think out loud” boosts capability while shifting more computation into readable text
    - reasoning models (OpenAI 2024; DeepSeek-AI 2025; Anthropic 2024; Yang et al 2025) are explicitly trained for extended CoT before acting
    - like hidden activations, CoTs can reveal information that outputs are rewarded for hiding, e.g. intent to misbehave
- why CoTs can be monitorable
    - necessity to think out loud = some tasks cannot be solved without externalized reasoning
    - propensity to think out loud = models often externalize even when not strictly required
    - long serial cognition inevitably passes through the CoT trace in transformer sampling
        - transformers use CoT as working memory on difficult tasks, and humans can read it by default
    - externalized reasoning property = some (not all) reasoning appears in the CoT, enabling partial monitoring
- practical benefits of CoT monitoring
    - detecting model misbehavior = reasoning traces often state reward hacking, data manipulation, or prompt-injection plans
    - discovering early misalignment signals = hidden goals surface in CoT when models simulate alignment
    - spotting evaluation flaws = reveals memorization, scaffolding bugs, or tool errors that confound benchmarks
- fragility of monitorability
    - drift toward less legible CoT as rl scale increases
        - direct outcome-only rl ignores the reasoning path, so clarity can decay
        - indirect pressure via shared weights with preference-modeled outputs can still warp CoT content
    - latent reasoning models = agents do internal planning without text, forfeiting CoT safety advantages
- research agenda: what makes models monitorable?
    - how should CoT monitorability be evaluated? ?
        - measures of CoT readability = use a separate llm to score clarity and coherence
        - capability evaluations of latent reasoning = test performance when externalization is disabled
        - causal relevance measures = perturb CoT and observe changes in final output
        - end-to-end monitor tests = assess how well automated monitors catch agent misbehavior
    - can models obfuscate reasoning on purpose? ?
        - monitors could themselves be reasoning models or interrogators that ask follow-up questions
        - adversarial training pits monitors against agents that try to hide intentions
- recommended actions for frontier ai developers
    - develop standardized evaluations and metrics for CoT monitorability
    - incorporate monitorability scores into training choices and deployment gating
- figure = transformer diagram illustrating information flow through CoT during autoregressive sampling


![[Screenshot 2025-07-21 at 4.39.11 pm.png| center | 600]]