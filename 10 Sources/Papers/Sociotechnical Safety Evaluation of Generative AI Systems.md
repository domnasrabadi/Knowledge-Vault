---
type: paper
status: structured
quality:
topics: [llm-risks, human-in-the-loop, llm-evaluation]
source: ""
created: 2025-07-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Laura Weidinger, Maribeth Rauh, Nahema Marchal, Arianna Manzini, Lisa Anne Hendricks, Juan Mateos-Garcia, Stevie Bergman, Jackie Kay, Conor Griffin, Ben Bariach, Iason Gabriel, Verena Rieser, William Isaac
- Category: pdf
- Document Tags: good 
- URL: https://arxiv.org/pdf/2310.11986
## 0.2 Highlights

- evaluation = practice of measuring ai system performance or impact
    - safety evaluation = focuses on risks of harm or actualised impacts on people or broader systems
    - exploratory evaluation = open-ended probing of an ai system to surface unknowns and form new questions
    - directed evaluation = follows set steps: select target risk → operationalise into observable metric → measure → judge against normative baseline (“good”, “fair”, “safe enough”)
    - outcomes
        - predicts and quantifies likelihood of downstream harms
        - guides ai development and offers assurance of safety levels
- three-layered safety evaluation framework
    - layer 1 capability evaluation
        - targets technical components: model behaviour on novel tasks, training data profiles, filters, aggregation mechanisms
        - methods
            - fixed automated tests
            - dynamic probing by human or automated adversaries
            - data visualisation to inspect diversity + representativeness
        - early indicator of harms but insufficient without context
    - layer 2 human interaction evaluation
        - centres real user experience and usability across groups
        - considers externalities: unintended effects on users exposed to ai outputs
        - requires longitudinal studies for time-dependent effects
        - assesses deviations between intended and actual use
    - layer 3 systemic impact evaluation
        - studies effects on society, economy, environment at scale
        - detects harms with small per-user effect sizes that compound system-wide
        - evaluates adoption patterns, perceptions, “cheating” behaviours
    - interactions
        - boundaries between layers are gradual
        - feedback loops: societal context ↔ annotator opinions ↔ system capabilities
- evaluation methods by layer
    - capability methods
        - automated benchmarks on fixed datasets or tasks
        - human annotation for goal-based pass/fail judgments
        - adversarial testing = “red teaming” to expose failure modes
    - human interaction methods
        - behavioural experiments to gauge influence on preferences + behaviour
        - user research for feature- or domain-specific consequences
        - longitudinal designs to capture prolonged interaction effects
    - systemic impact methods
        - staged releases or pilots
        - ex-post impact assessments on institutions, society, environment
        - forecasting + simulation to anticipate downstream harm pathways
- taxonomy of harm (6 areas)
    - representation & toxicity harms
    - misinformation harms
    - information & safety harms
    - malicious use
    - autonomy & integrity harms
    - socioeconomic & environmental harms

![[Screenshot 2025-07-21 at 4.50.56 pm.png| center | 600]]

- current state of sociotechnical safety evaluation
    - multimodal gap = limited evaluations for audio, image, video, mixed modalities
    - coverage gap = several risk areas lack evaluations
    - context gap = few evaluations at human interaction and systemic layers; most cluster at capability layer
    - multimodal risk tools mainly exist at capability layer
- closing evaluation gaps
    - construct novel evaluations via operationalisation = translate rich harm concepts into measurable metrics
    - model-driven evaluation = use pre-trained generative models as flexible evaluators
    - practical pipeline
        - define risk → choose metrics → select methods → collect or synthesize data → analyse → iterate
- human annotation considerations
    - ground truth depends on human judgement for most risk areas
    - challenges
        - unrepresentative annotator pools
        - incentives lowering quality
        - poorly designed interfaces
        - demographic factors influencing ratings → bias risk
        - aggregation schemes may overestimate future model performance
    - quality improvements
        - careful task design inspired by psychology experiments
        - test-retest reliability safeguards
        - use human data to calibrate automated benchmarks
- adversarial testing
    - probes vulnerabilities through intentional attacks on models or deployment environments
    - limits
        - constrained by tester imagination, skill, context knowledge
        - novel failures still emerge post-deployment
    - automated red teaming reuses successful prompts to scale future testing
- open-ended probing = exploratory red teaming to surface unexpected risks (e.g., eating-disorder content)
    - identifies biases and harmful patterns beyond predefined tests
- evaluation is inherently incomplete
    - only covers subset of possible harm manifestations
    - scope shaped by pragmatic and normative priorities
    - especially challenging for general-purpose generative ai with undefined downstream uses