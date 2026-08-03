---
type: paper
status: structured
quality:
topics: [model-monitoring, human-in-the-loop]
source: ""
created: 2025-07-13
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: arxiv.org
- Category: article
- Document Tags: good 
- URL: https://arxiv.org/html/2407.12003v2
## 0.2 Highlights
- lag metrics = post-deployment success indicators for Assistant
    - user engagement
    - user satisfaction
    - user retention
- lead metrics = pre-deployment proxies chosen to drive lag metrics improvement
- data requirements
    - representative = mirrors real usage patterns
    - high-quality = curated to minimise noise and bias
    - scalable collection = systematic pipelines for continual refresh
- feedback channels
    - explicit feedback = direct user ratings, thumbs-up/down, preference polls
        - limitations
            - sparsity = only a small fraction of sessions include feedback
            - representativeness = skewed toward vocal users → sample bias
            - low detail = users see only final answer, offer minimal context
    - implicit feedback = clicks, scroll depth, dwell time, navigation paths
        - limitations
            - goal ambiguity = actions may not reveal true satisfaction
            - delayed outcomes = many assistant tasks have long latency between query and goal completion
            - weak signal strength compared with conversational search
- metric design principles
    - prioritise metrics directly affected by production changes
    - align metrics with user experience
        - one incorrect citation ≠ full hallucination
    - collect end-to-end and component-wise metrics to localise issues
- evaluation strategy
    - human evaluation > automated evaluation for alignment with real outcomes
        - efficient allocation
            - non-experts handle simple annotation tasks
            - domain engineers tackle complex error analysis + improvement planning
    - error analysis workflow
        - domain experts sample errors → identify patterns → decide remediation
            - prompt engineering
            - in-house model fine-tuning
            - new synthetic-data templates
            - ux adjustments or specialised index optimisation
