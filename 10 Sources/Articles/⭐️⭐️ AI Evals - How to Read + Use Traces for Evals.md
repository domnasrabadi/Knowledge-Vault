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
1. start with error analysis 
	- when reviewing traces, stop at the first most upstream error you find 
	- this keeps things tracetable (upstream failures tend to be most important)
2. gather traces related to your top failures
	- for each of these traces, minimally reproduce the failure in as few turns with as least amount of complexity as possible
3. $n - 1$ 
	- collect a dataset of minimally reproduced and use the $n-1$ turns before the error as test cases
	- this assumes your system isn't changing rapidly
4. additional test coverage 
	- can modify traces in step 4 in valid ways using an LLM
	- e.g. rephrasing, adding variation etc 
5. simulated LLM user
	- simulating a user with another LLM → doing this well can be challenging