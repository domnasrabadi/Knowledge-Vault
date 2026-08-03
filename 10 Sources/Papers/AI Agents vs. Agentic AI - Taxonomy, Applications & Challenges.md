---
type: paper
status: structured
quality:
topics: [ai-agents, multi-agent-systems]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: arxiv.org
- Category: article
- Document Tags: ⭐️⭐️⭐️ great 
- URL: https://arxiv.org/html/2505.10468v4
## 0.2 Highlights

### 0.2.1 Definitions
- **AI Agent** = modular, autonomous software entity (often LLM/LIM-powered) for goal-directed, task-specific automation
    - perceives structured/unstructured inputs, reasons over context, initiates actions
    - uses tool invocation + result integration to extend capabilities beyond internal knowledge
    - features:
        - **autonomy** within bounded scope
        - **task-specificity**
        - **reactivity/adaptation** to dynamic inputs
- **Agentic AI** = paradigm shift to multi-agent, coordinated systems
    - specialized agents collaborate via dynamic task decomposition, persistent memory, and coordinated autonomy
    - goal decomposition + multi-step planning allow adaptation to environmental changes or failures
    - uses distributed communication (queues, shared memory, intermediate outputs) for coordination
    - incorporates reflective reasoning + memory for strategy refinement

---

### 0.2.2 Evolutionary context
- **classical AI agents** (pre-modern expert systems, scripted NPCs)
    - predefined rules, limited autonomy, no generative reasoning, poor adaptability
- **modern AI agents**
    - leverage deep learning, RL, foundation models
    - support self-learning, contextual awareness, and generalization
    - integrate tool use, API calls, sequential reasoning
- **Agentic AI**
    - orchestrated multi-agent workflows
    - higher autonomy + ability to manage complex, distributed processes

---

### 0.2.3 Structural differences (Table I summary)
- AI Agents = single-agent, tool-assisted, narrow task execution
- Agentic AI = multi-agent, collaborative, handles complex multi-step workflows
- Autonomy: task-bounded vs broad, multi-task
- Applications: customer support, virtual assistants vs supply chain mgmt, project orchestration

---

### 0.2.4 Conceptual taxonomy (Tables II–IX condensed)

- **Generative AI** = stateless, prompt-driven, content generation only
- **AI Agent** = tool-based executor, medium autonomy, short-term continuity
- **Agentic AI** = goal-initiated orchestrator, high autonomy, persistent multi-agent memory
- **Generative Agent** (inferred) = sub-task generative component within larger workflows
- Key distinctions span:
    - **planning horizon** (single-step → multi-step)
    - **learning/adaptation** (static → meta-learning)
    - **coordination strategy** (none → hierarchical/decentralized)
    - **memory scope** (none → shared episodic memory)
    - **workflow handling** (single-step → coordinated multi-step)
    - **interaction style** (reactive → proactive/collaborative)

---

### 0.2.5 Challenges & limitations
#### 0.2.5.1 AI Agents
- lack causal reasoning → cannot model cause–effect
- inherit LLM weaknesses: hallucinations, brittleness
- incomplete agentic properties (autonomy, proactivity, social ability)
- poor long-horizon planning + recovery due to stateless prompt–response nature
#### 0.2.5.2 Agentic AI
- **amplified causality gaps** = inter-agent distributional shifts hinder coordination
- **communication bottlenecks** = natural language protocols cause ambiguity + drift
- **emergent behaviour risks** = instability from loops, deadlocks, contradictions
- **scalability & debugging difficulty** = nested, opaque interactions across agents/tools/memory
- **trust, explainability, verification** = compounded opacity, no formal verification methods
- **security risks** = larger attack surface, single point of compromise
- **ethical/governance** = accountability gaps, fairness, value alignment challenges
- **immature foundations** = lack of standard architectures, evaluation frameworks

---

### 0.2.6 Key design implications

- taxonomy clarifies **when to use AI Agents** (modular, tool-assisted tasks) vs **Agentic AI** (complex, coordinated workflows)
- avoids misapplication of multi-agent design to single-agent contexts
- supports targeted benchmarking, safety protocols, and resource allocation strategies









