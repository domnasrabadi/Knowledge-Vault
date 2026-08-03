---
type: article
status: distilled
quality: 2
topics: [llm-judges, evaluation-metrics]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- binary (pass & fail) scores are preferable in most cases vs. likert scales (1-5 ratings)
- likert scales are expensive to align w domain experts
	- annotators often default to middle values to avoid making difficult decisions 
	- they can also encourage too much scope → e.g. overall quality score vs a targeted eval 
- binary scores comples the annotator to make a definitive decision 
	- better aligns w reality that you must decide whether or not the feature is good enough to ship for the AI application 
	- binary scores are also easier to apply during error analysis 

```mermaid
flowchart LR
  %% Layout
  LLM[LLM Output]
  Likert[Likert Scale Judge]
  Score[Score: 3/5]

  LLM --> Likert --> Score

  %% Actionable evals (dashed group)
  subgraph AE [Actionable Evals]
    direction TB
    ISP[is_polite] --> P1[✓ Pass]
    SCHED[scheduling] --> F1[✗ Fail]
    HAND[human_handoff] --> P2[✓ Pass]
  end

  %% LLM output also feeds the actionable evals
  LLM --> ISP
  LLM --> SCHED
  LLM --> HAND

  %% Callout: "Don't Do This!" pointing at the Likert box
  DONT["Don't Do This!"] -.-> Likert

  %% Styling
  style AE fill:#fafafa,stroke:#bdbdbd,stroke-dasharray:5 5

  classDef pass fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;
  classDef fail fill:#ffebee,stroke:#d32f2f,color:#b71c1c,stroke-width:2px;
  classDef callout fill:#fff3e0,stroke:#fb8c00,color:#e65100,stroke-width:2px;

  class P1,P2 pass;
  class F1 fail;
  class DONT callout;
```