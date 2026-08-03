---
type: article
status: distilled
quality: 2
topics: [llm-evaluation, evaluation-metrics]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
1. code based assertions & deterministic tests
	- check for objective or rule-based failures
	- e.g. matching keywords, confirming tool execution etc 
	- use them whenever possible → they're cheap, deterministic & interpretable 
2. LLM-as-Judge
	- uses an LLM to assess subjective or nuanced criteria that isn't deterministic/code-suitable
	- while powerful, they are slower, more expensive & require verification/alignment (calibration)
	- reserve these for more important failures due their cost 
3. guardrails
	- run in the request/response path to block failures before they reach the user
	- tend to be fast + have a low false-positive rate to avoid blocking valid responses 
	- commonly implemented as code-based checks, small classifiers or LLMs