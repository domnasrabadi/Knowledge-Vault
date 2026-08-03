---
type: paper
status: structured
quality:
topics: [ai-agents, agent-frameworks]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: himanshu
- Category: article
- URL: https://himanshustwts.substack.com/p/why-the-best-ai-agents-built-from?utm_campaign=post&utm_medium=web&triedRedirect=true
## 0.2 Highlights

- **core argument** = scratch-built agents give higher performance ("high alpha") than framework-based ones
    - frameworks assume you already know your problem’s shape — in agent development, the shape emerges through iteration
    - starting from scratch forces deep understanding of why the agent behaves a certain way (e.g., weird tool loop, infinite retries)
        - easier to **trace, log, and rethink** behaviour

### 0.2.1 Recommended approach
1. **start small**
    - use the most basic setup (e.g., direct LLM API calls)
    - explore model interactions, data flow, evaluation, prompt engineering from first principles
    - go deep into internals to master debugging + optimisation
2. **identify pain points**
    - watch for repeating patterns and bottlenecks
    - write boilerplate until it’s clearly slowing you down
3. **add abstractions selectively**
    - switch to libraries/frameworks **only** when:
        - they solve a specific, recurring problem
        - they don’t hide critical mechanics
    - examples: Pydantic, Vercel AI SDK for well-defined needs

### 0.2.2 Benefits of scratch-built agents
- **native integration** = directly tailored to target environment, infra, and user flows
    - no extra adapters, hacks, or glue code
- **full transparency** = you know exactly why the agent makes each decision
- **better execution flow** = fewer hidden dependencies, predictable performance
- **scalable optimisation** = deep knowledge enables later fine-tuning and system-level efficiency

### 0.2.3 Role of frameworks
- good for **exploration** and quick prototyping
- risky for **shipping production agents** if internals are poorly understood
- can introduce hidden complexity and debugging blind spots
