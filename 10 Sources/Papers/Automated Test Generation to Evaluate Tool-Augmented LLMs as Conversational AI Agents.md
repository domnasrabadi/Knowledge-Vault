---
type: paper
status: structured
quality:
topics: [agent-evaluation, synthetic-data]
source: ""
created: 2025-07-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: arxiv.org
- Category: article
- Document Tags: good 
- URL: https://arxiv.org/html/2409.15934v2
## 0.2 Highlights
- evaluation challenge = conversational agents have vast interaction space; existing datasets cover only single turns + function calls
- framework = automated test generation using llms grounded on user-defined procedures
    - intermediate graphs = flowgraph + conversation graph limit hallucination and enforce high coverage
    - noise injection = adds out-of-procedure or attack messages to test agent resilience
- customer support agent requirements
    - interact with tools + customers to resolve issues
    - strictly follow support procedures and resist customer manipulation

![[Screenshot 2025-07-21 at 4.54.48 pm.png| center | 600]]

- automated test generation pipeline
    - step 1 intent generator = produce task intents (e.g., cancel order) via llm or domain list
    - step 2 procedure generator = llm writes ordered instructions for each intent
    - step 3 api extractor = llm proposes api specs (name, io, description) relevant to procedure
    - step 4 flowgraph generator = directed graph of agent logic built from procedure + apis
        - single start_message root
        - concrete messages on nodes and edges
        - api nodes include explicit outputs on outgoing edges
    - step 5 conversation graph generator = converts flowgraph to dialogue-like graph with agent, customer, api nodes
    - step 6 noise generator = with p≈0.2 inserts customer out-of-procedure or attack nodes to harden tests
    - step 7 path sampler = samples diverse paths for coverage
    - step 8 conversation generator = llm turns each path into full dialogue given graph + apis
    - step 9 test extractor = splits conversation at each user turn, stores context, labels correct agent reply or api call
- dataset = ALMITA
    - 84 intents → 168 initial procedures → 132 retained after manual filtering
    - evaluation metrics
        - reply recall = chooses reply instead of unnecessary api
        - correct reply = reply text matches expected (bert-score ≥ 0.55)
        - api recall = detects need for api vs reply
        - correct api = selects correct api when required
        - correct api parameters = passes accurate arguments
        - test accuracy = all required actions + parameters correct in a single turn
        - conversation accuracy = entire multi-turn sequence correct

![[Screenshot 2025-07-21 at 4.55.03 pm.png| center | 500]]

- comparison to related datasets
    - AgentTuning, AgentBench, qin2023toolllm, basu2024api map utterances to api sequences
        - lack conversational structure + intermediate graphs
        - limited coverage and higher hallucination risk
- limitations
    - diversity of generated tests not quantitatively measured
    - small human-annotation sample for validation
    - pipeline uses single generator model (gpt-4) and single evaluation prompt
    - strict metrics may over-penalise minor errors; future work to weight severity


