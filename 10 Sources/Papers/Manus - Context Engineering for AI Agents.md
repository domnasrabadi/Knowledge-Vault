---
type: paper
status: structured
quality:
topics: [ai-agents, context-engineering, prompting]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: manus.im
- Category: article
- Document Tags: ⭐️ good 
- URL: https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
## 0.2 Highlights

- **core principle** = context engineering enables faster iteration, keeps product design independent of underlying LLM choice
    - can ship improvements in hours, not weeks

---
### 0.2.1 KV-cache optimisation
- **KV-cache hit rate** = most important metric for production AI agents (affects latency + cost)
- how cache works = contexts with identical prefixes reuse stored key–value states, lowering time-to-first-token and inference cost
- practices for high hit rate:
    - keep prompt prefix stable (avoid changing even 1 token)
        - e.g., do **not** include dynamic timestamps
    - explicitly mark cache breakpoints if framework doesn’t auto-handle incremental caching
    - avoid changing action/tool definitions mid-run — this breaks prefix continuity

---

### 0.2.2 Action space design
- avoid dynamically adding/removing tools unless absolutely necessary
    - dynamic changes often break cache and destabilise behaviour
- instead, constrain available actions without redefining tools
    - use consistent naming conventions (e.g., `browser_*`, `shell_*`) so subsets can be activated/deactivated by prefix filtering
- use **response prefill** to guide model towards intended tool choices without altering definitions

---

### 0.2.3 Context window limits & external memory
- large context windows (128K+ tokens) still insufficient for long agent loops
    - risk: can’t predict which past observation will be needed later
- **solution**: treat file system as unlimited, persistent, structured memory
    - agent writes/reads files on demand
    - common pattern: maintain `todo.md` file, updating it step-by-step to keep plan fresh in short-term attention

---

### 0.2.4 Long-loop task management
- average Manus task = ~50 tool calls → high risk of goal drift or forgetting
- **todo list repetition** = keeps global plan in recent context, avoiding “lost-in-the-middle” failures

![[Screenshot 2025-08-10 at 2.43.32 pm.png| center | 500]]

- retain failure evidence in context
    - leaving failed actions + stack traces helps model adapt and avoid repeat errors
    - supports true agentic error recovery

![[Screenshot 2025-08-10 at 2.43.14 pm.png| center | 500]]

![[Screenshot 2025-08-10 at 2.43.51 pm.png| center | 500]]

- prevent repetitive drift
    - introduce structured variation in actions and observations
        - alter phrasing, serialization format, or ordering to maintain diversity
        - prevents brittleness from uniform contexts

![[Screenshot 2025-08-10 at 2.44.05 pm.png| center | 500]]

---

### 0.2.5 Key takeaways
- shaping context is as critical as model choice for scaling agent behaviour
- context engineering impacts:
    - speed (via KV-cache efficiency)
    - resilience (via preserved history + variation)
    - scalability (via external memory structures)
    - adaptability (via visible errors for learning)

