---
type: paper
status: structured
quality:
topics: [ai-agents, prompting]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Practical tips on building LLM agents

## 1.1 Metadata
- Author: Paras Chopra
- Category: article
- Document Tags: ⭐️ good 
- URL: https://letters.lossfunk.com/p/practical-tips-on-building-llm-agents
## 1.2 Highlights
- **chunk tasks into <10–15 minutes of human-equivalent work**
    - LLM success probability strongly correlated with human task time
    - shorter atomic tasks reduce compounding error risk

![[Screenshot 2025-08-10 at 2.40.48 pm.png| center | 500]]

- **maximise context usage**
    - use long context windows fully; include all relevant files, not just fragments
    - RAG for code often fails → fragments confuse the model
        - better: put entire files in context
        - recent paper: full-file context matches “agentic” flow performance on SWE-bench-Verified
    - earlier Cursor versions used fast-diff models after LLM output → caused compounding errors from initial mistakes
- **handle long-horizon tasks carefully**
    - more steps → higher error accumulation
    - mitigation:
        - keep tasks isolated if possible (stateless functions)
        - add verification step after each task
            - LLM must clearly detect success/failure before proceeding

![[Screenshot 2025-08-10 at 2.41.06 pm.png| center | 500]]

- **manage LLM memory limits**
    - LLMs can “forget” earlier tokens as context grows
    - repeat todo list regularly for long tasks
    - for large file sets: instruct LLM to read important files rather than stuffing them all into context
- **empower with read/write tools**
    - let LLM build its own context via tool use
    - tool-calling now precise; main challenge = **tool design**
        - communicate partial successes clearly
        - summarise large results (e.g., DB query: report count + sample)
        - provide just enough error detail for recovery without bloating context
        - design for interdependent operations (transactions, locks, dependencies)
- **control token costs**
    - cost rises **quadratically** for multi-turn agents
    - **never change context** mid-run → always append
        - preserves KV cache → can drop cost to ~1/10th






