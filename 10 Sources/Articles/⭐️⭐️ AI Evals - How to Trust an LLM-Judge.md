---
type: article
status: distilled
quality: 2
topics: [llm-judges, model-calibration]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- the ***only*** way to trust an LLM Judge is to measure it against human labels 
	- commonly known as aligning or calibrating the judge 
- split your human labelled data into 3 sets 
	- train → where you draw your few shot examples from 
	- dev → where you use to optimise your judge 
	- test → a final check to ensure you haven't overfit 
- don't report accuracy 
	- it's misleading on imbalanced data 
	- use TPR & TNR → aim for a high TPR & TNR rate e.g. > 90%
		- TPR = when judge says error, what % of time is it right?
		- TNR = when judge says not an error, what % of time is it right?

```mermaid
flowchart TB
  %% Top node
  J[LLM Judge]

  %% Row of datasets directly BELOW (left-to-right layout inside subgraph)
  subgraph DATASETS[ ]
    direction LR
    T([Train<br/><sub>~20% of examples</sub>])
    D([Dev<br/><sub>~40% of examples</sub>])
    E([Test<br/><sub>~40% of examples</sub>])
  end

  %% Keep the subgraph anchored beneath J (no visible lines)
  J ---| | T
  J ---| | D
  J ---| | E

  %% Vertical edges to/from Judge
  T -->|Select few-shot examples for your prompt from here| J
  D -->|Hill climb against evals| J
  J -->|Hill climb against evals| D
  J -->|Final check to ensure no overfitting| E

  %% Styling
  classDef judge fill:#f5f5f5,stroke:#9e9e9e,color:#424242,stroke-width:2px;
  classDef train fill:#e3f2fd,stroke:#1e88e5,color:#0d47a1,stroke-width:2px;
  classDef dev   fill:#fff3e0,stroke:#fb8c00,color:#e65100,stroke-width:2px;
  classDef test  fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20,stroke-width:2px;

  class J judge;
  class T train;
  class D dev;
  class E test;

  %% Arrow/label colours
  %% Link indices: 3 real edges appear AFTER the 3 anchoring edges -> 
  %% 3:T->J, 4:D->J, 5:J->D, 6:J->E
  linkStyle 3 stroke:#1e88e5,color:#1e88e5,labelBackgroundColor:#e3f2fd,stroke-width:2px;
  linkStyle 4 stroke:#fb8c00,color:#fb8c00,labelBackgroundColor:#fff3e0,stroke-width:2px;
  linkStyle 5 stroke:#fb8c00,color:#fb8c00,labelBackgroundColor:#fff3e0,stroke-width:2px;
  linkStyle 6 stroke:#2e7d32,color:#2e7d32,labelBackgroundColor:#e8f5e9,stroke-width:2px;
```

