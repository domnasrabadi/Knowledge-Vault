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
- error analysis = allows you to quickly find patterns of failures in your AI products' logs & traces
- process
	1. **collect traces** → gather diverse sample of 100+ traces from production or real/synthetic usage of your own
	2. **annotate traces** → review each trace, write brief/unstructured notes on the problem e.g. "hallucination", "misread user name", "failed calculator tool"
	3. **group & categorise** → group similar notes into clusters e.g. "failed tool call", "tone violation"
	4. **prioritise** → count frequency of each category, this informs priority 
- tips
	- keep looking at data until you feel like you're not leaning anything new 
		- aka "*theoretical saturation*"
	- rule of thumb: need ~100 high quality & diverse traces
		- can be using real data, synthetic data
		- needs to have both pass & fail cases
		- and ideally a variety of failure modes