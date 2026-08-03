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
- don't make these common eval mistakes:
	1. an automated eval is useless if it doesn't measure your specific failures
		- best way to find these is by looking at your data first 
		- off-the-shelf metrics like "helpfulness score" are a bad idea for this reason → not tailored to your use-case or data
	2. when using an LLM Judge, you must measure the judge against a human label (or do calibration!)
		- not doing so creates an untrustworthy and misaligned metric
	3. AI evals are most valuable when they find new failures
		- a perfect score on all evals often means they are saturated or too easy 
		- add hard test cases to keep guiding improvement