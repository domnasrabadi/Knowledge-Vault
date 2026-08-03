---
type: article
status: distilled
quality: 2
topics: [synthetic-data, llm-evaluation]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- tips on generating synthetic data for bootstrapping evals 
	- **use structured input for diversity** → define key dimensions (e.g. feature/persona/scenario) & use them as variables in your prompt
	- **seed generation w real logs/traces** → then ask LLM to explicitly inject changes like a new constraint or modified variable 
		- this helps create realistics edge cases
	- **enforce output structure & filter** → define a schema for the output
		- generate many candidates, then filter to retain the highest quality, challenging examples
	- **increase complexity iteratively** → start w simple queries & incrementally ask the LLM to add constraints, complex formatting etc 
- do not:
	- prompt w zero-shot requests lacking structured input
	- e.g. "generate 50 test cases"
	- these generally give generic, repetitive inputs 