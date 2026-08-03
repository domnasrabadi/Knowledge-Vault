---
type: article
status: distilled
quality: 2
topics: [error-analysis, llm-evaluation]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- for AI evals, you can sample traces either more exploratory or by using signals 
	- methods from most exploratory (first) to more signal based (last)
		- random → always do this alongside other strategies to discover unknown issues 
		- clustering → group traces according to semantic similarity or clustering algo & see if you discover new errors 
		- data analysis → analyse statistics on latency, turns, tool calls, tokens etc for outliers 
		- classification → use your existing evals, a predictive model or an LLM to surface problematic traces (use w caution)
		- feedback → use explicit customer feedback to filter traces