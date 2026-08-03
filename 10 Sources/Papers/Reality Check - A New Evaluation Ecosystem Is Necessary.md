---
type: paper
status: raw
quality:
topics: [llm-evaluation]
source: "https://arxiv.org/pdf/2505.18893"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# Reality Check: A New Evaluation Ecosystem Is Necessary to Understand AI's Real World Effects

## Metadata
- Author: Reva Schwartz, Rumman Chowdhury, Akash Kundu, Heather Frase, Marzieh Fadaee, Tom David, Gabriella Waters, Afaf Taik, Morgan Briggs, Patrick Hall, Shomik Jain, Kyra Yee, Spencer Thomas, Sundeep Bhandari, Lee Wan Sie, Qinghua Lu, Matthew Holmes, The...
- URL: https://arxiv.org/pdf/2505.18893
## Highlights
- evaluation = interpretation of measurement results to understand an ai system in context
    - current practice centred on computational-ml frame, rarely accounts for human, organisational or societal factors
- real-world evaluation ecosystem = coordinated processes, data and institutions that capture second-order effects, drive fit-for-purpose datasets, spur innovation and improve ai functionality
- orders of effect
    - first-order = immediate model performance in-silico
    - second-order = performance and user impact in-vitro or in-situ
    - third-order = long-term societal change
- benchmarking = dominant first-order method
    - relies on curated datasets and controlled tasks (often single-turn)
    - outputs ranked on leaderboards
    - limitations
        - static design and task contamination
        - narrow english-centric coverage and cultural blind spots
        - lacks internal + external validity, encourages leaderboard over-fitting
        - cannot capture human–ai inter-dependencies or emergent capabilities
- broader evaluation approaches
    - testing-and-evaluation plus verification-and-validation = combine first + second-order checks in-silico, in-vitro, in-situ
    - program evaluation = targets second + third-order efficacy in real deployments
- contextual awareness = knowledge of what matters in a given setting
    - needs systematised descriptions of real-world concepts to guide models, prompt design, content moderation
- stakeholder engagement = qualitative methods applied across the project lifecycle
    - surfaces potential harms, emergent risks, hidden assumptions
    - informs mitigation before issues become entrenched
- field testing = controlled pre-deployment studies of human–ai interaction
    - multi-session experiments with randomisation + blinding
    - collect surveys, logs, behavioural data alongside system metrics
    - balance naturalistic scenarios and participant safety under human-subject protocols
- red teaming = adversarial evaluation to uncover failures and boundary conditions
    - expert red teaming = specialists craft sophisticated attacks
    - public red teaming = diverse users expose off-label failures
    - automated red teaming = large-scale generation of adversarial prompts
    - especially vital in high-stakes domains (education, healthcare, employment)
- improving red teaming
    - scoping = include multi-turn dialogue, multi-lingual + multi-modal tasks
    - tester-bias mitigation = widen recruitment, capture positionality, survey perceptions of harm
    - automation = develop shared criteria for diverse high-quality test cases
    - resource balance = mix manual depth with scalable automation for small organisations
    - transparency = responsible sharing of findings and metrics for progress tracking
- common attack strategies
    - complex or leading prompts reveal reasoning errors, hallucinations, code faults, fake citations
    - counterfactual + persona-shift prompting uncovers demographic bias
    - honest-looking fill-in-the-blank prompts probe guardrails
    - membership-inference and privacy probes expose memorised data
    - multilingual jailbreaks test cultural + linguistic safety gaps
    - data-poisoning, indirect prompt-injection and embedded harmful content test integrity
    - availability or sponge attacks flood the system to stress performance + cost
    - chaos testing with random prompts explores unknown failure modes
    - requests for copyrighted or obscene content test policy compliance
- contextual work versus benchmarks
    - deeper, slower and resource-intensive
    - requires cross-disciplinary actors, processes and skills yet yields higher measurement validity and societal relevance

---
