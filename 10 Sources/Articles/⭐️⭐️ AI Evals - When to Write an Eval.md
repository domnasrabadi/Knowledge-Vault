---
type: article
status: distilled
quality: 2
topics: [llm-evaluation, error-analysis]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- use the following decision tree
	1. have you observed the failure mode with analysis?
		- (no to 1) → do error analysis first, your evals should target errors you observe or induce 
	2. (yes to 1) how much iteration is required to fix? 
	3. (low effort to 2) unclear value → consider inexpensive eval like deterministic assertion, or just fix and move on
	4. (high effort to 2) high value → evals are most valuable here, e.g. LLM-as-judge
- notes/tips
	- evals provide more value when you need to hill climb against an error
	- you don't always need to write an eval


```mermaid
flowchart LR
  %% Layout
  A{Have you observed the failure<br/>w/ error analysis?}
  B{How much iteration<br/>is required to fix?}

  A -- No --> SA[Stay Away]
  A -- Yes --> B
  B -- Little --> UV[Unclear Value]
  B -- Lots --> HV[High Value]

  %% Side guidance + footnotes (dashed helpers)
  SA_note[Do error analysis first.<br/>Your evals should target errors you observe or induce.]
  UV_note[Consider:<br/>• Can an inexpensive eval like a code-based assertion work?<br/>• Does it make sense to just fix and move on?]
  HV_note[Evals are most valuable here.<br/>Expensive evals like an LLM-as-a-judge may be feasible.]

  SA -.-> SA_note
  UV -.-> UV_note
  HV -.-> HV_note

  %% Styling: keep decision nodes default/grey; color only the answer boxes
  classDef danger fill:#ffebee,stroke:#d32f2f,color:#b71c1c,stroke-width:2px;
  classDef warn   fill:#fff8e1,stroke:#f9a825,color:#6d4c00,stroke-width:2px;
  classDef ok     fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
  classDef note   fill:#f5f5f5,stroke:#bdbdbd,color:#616161,stroke-dasharray:4 2;

  class SA danger;
  class UV warn;
  class HV ok;
  class SA_note,UV_note,HV_note,side note;
```
