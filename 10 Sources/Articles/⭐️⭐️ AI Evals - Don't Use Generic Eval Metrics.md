---
type: article
status: distilled
quality: 2
topics: [evaluation-metrics, llm-evaluation]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- don't use generic scores:
	- ROUGE, BLEU, Faithfulness, Helpfulness, Tone
- instead use application specific metrics (examples below):
	- Calendar scheduling failure
	- Interrupted conversation flow
	- Widget rendering issue
	- Email recipient incorrect 
	- Failure to escalate to human 
- **good eval metrics**:
	- measure an error you have observed
	- relates to a non-trivial issue you will iterate on 
	- are scope to a specific failure 
	- has a binary outcome (not 1-5 score)
	- is verifiable e.g. human annotation or LLM-as-Judge