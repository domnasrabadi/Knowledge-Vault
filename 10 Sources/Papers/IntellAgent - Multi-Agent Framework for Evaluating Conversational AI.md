---
type: paper
status: structured
quality:
topics: [agent-evaluation, synthetic-data, multi-agent-systems]
source: ""
created: 2025-07-17
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Elad Levi, Ilan Kadar
- Category: pdf
- Document Tags: great 
- URL: https://arxiv.org/pdf/2501.11067
# 2 Highlights
- conversational ai evaluation challenge = traditional static benchmarks fail to capture multi-turn dialogue complexity, policy adherence, and tool usage
- **IntellAgent** = scalable open-source multi-agent framework for comprehensive evaluation of conversational ai systems
    - constructs synthetic yet realistic events across diverse policies, tools, and tasks
    - simulates three roles
        - event generator agent = builds scenario + initial database state
        - user agent = interacts with the tested chatbot using event details
        - critique agent = analyzes chatbot performance against event policies
- related work landscape
    - synthetic benchmarks
        - conditional prompting = vary scenarios via attribute–value pairs
        - multi-step generation = decompose tasks for coherence and coverage
        - prior methods require heavy manual effort and scale poorly
    - conversational ai benchmarks
        - **τ-bench** = customer-service interactions with policies + api calls
        - **ALMITA** = tool-augmented customer support conversations
        - **LTM** = multitasking with interleaved dialogue threads
        - **CURATe** = user-specific safety alignment focus
        - limitations = narrow domains, manual curation, rigid scripts, poor scalability
- policy graph = central data structure underpinning IntellAgent event generation
    - nodes = individual policies
    - node weight = policy complexity
    - edge weight = likelihood of two policies co-occurring
    - construction procedure
        - llm extracts policy set from system prompt or corporate policy document
        - llm assigns complexity rank to each policy
        - llm scores every policy pair $1\text{–}10$ for co-occurrence likelihood
- event generation algorithm
    - sampling objectives
        - uniform event complexity distribution
        - uniform selection of first policy across events
        - realistic distribution of additional policies conditioned on complexity and first policy
    - batch sampling over policy graph ensures criteria satisfaction
    - each **event** contains
        - policy list
        - user request aligned with policies
        - initial chatbot database state
- dialog simulation workflow
    - user agent receives event description + database snapshot
    - chatbot under test interacts, invoking domain tools as needed
    - critique agent scores adherence to all policies and task fulfilment
- evaluation experiments
    - dataset construction = extended **τ-bench** airline + retail settings to 1 000 events each (vs original 50 / 115)
    - benchmark comparison
        - success-rate correlation between IntellAgent and τ-bench
            - airline $r = 0.98$
            - retail $r = 0.92$
        - demonstrates synthetic data faithfully reflects real benchmark difficulty
- advantages of IntellAgent
    - automated synthetic dataset generation = high diversity + faithful policy coverage
    - comprehensive metrics = success rates across varying policy complexity and tool usage patterns
    - scalability = thousands of events per domain without manual annotation
- open questions ?
    - how to extend policy graph methodology to domains with richer, less formal policies ?
    - can critique agent reliability be improved beyond llm judgments ?
    - what is the impact of different user-agent personas on benchmark difficulty ?

![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/300fe73bdf1d31469de37cc47b2313c8.png)
