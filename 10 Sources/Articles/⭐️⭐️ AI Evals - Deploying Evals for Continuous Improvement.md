---
type: article
status: distilled
quality: 2
topics: [llm-evaluation, mlops, model-monitoring]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- **CI/CD** 
	- goal → prevent regressions
	- when to do this → pre-merge on pull requests
	- how to do this → unit tests, LLM Judges
	- what data to use → curated test cases
	- what to do on failure → block the merge
- **Online Monitoring** 
	- goal → discover new failures & track performance
	- when to do this → async (post-response)
	- how to do this → unit tests, LLM Judges, A/B testing
	- what data to use → sampled production traffic
	- what to do on failure → trigger an alert
- **Guardrails** 
	- goal → enforce safety & block high impact errors
	- when to do this → synchronous (pre-response)
	- how to do this → unit tests, small classifiers, LLM guardrails
	- what data to use → 100% of live traffic
	- what to do on failure → block response, retry, fallback or escalate 