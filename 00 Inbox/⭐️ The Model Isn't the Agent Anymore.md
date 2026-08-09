---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/AlphaSignalAI/article/2060028227285135594/?rw_tt_thread=True
created: 2026-08-09
published: 2026-05-28
author: AlphaSignal AI
flashcards: none
updated: 2026-08-09
---

# The Model Isn't the Agent Anymore

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2014100845189529600/Ff1Xc28-.jpg" width="220" />
</div>

- **The paper** names this work "scaling the harness" and decomposes any agent into six interacting components, with three of them already at saturation.
- The research is authored by **Shangding Gu (UC Berkeley)** and titled "**From Model Scaling to System Scaling: Scaling the Harness in Agentic AI**"

### The idea

- An agent is six things, not one. The model reasons. The harness around it picks what to remember, what context to assemble, which tool to call, how to verify each step, and what trace to record.

![](https://pbs.twimg.com/media/HJWA7aIXMAMOrdM.jpg)


### Bottleneck 1: context governance

- Gu factors context quality into four subaxes: **relevance** (matches the current subproblem), **compactness** (no more than the minimum sufficient set), **traceability** (provenance can be inspected), and **refresh policy** (stale context gets rechecked).
- Failure mode: **exposure without access**. As context grows, the model sees more tokens but does not necessarily attend to the right ones. Relevant evidence competes with low-value padding.
- Attention dilutes over long inputs.

### Bottleneck 2: trustworthy memory

- Four subaxes again: **precision** (the claim has a narrow scope), **durability** (the target has not silently changed), **retrievability** (the memory can be found at acceptable cost), **verifiability** (the claim can be checked against the live environment).
- Failure mode: **stale-but-confident**.
- System move: trust is a runtime decision, not a property of the stored item. Store confidence, source, age. Penalize staleness in retrieval.
- Treat retrieved memory as a hypothesis until verified.

### Bottleneck 3: dynamic skill routing

- The hard problem of skill is not having skills. It's routing and checking them.
- Four subaxes: **specificity** (each skill states what it can and cannot do), **selectivity** (the router invokes the right skill at the right time), **composability** (one skill's post-conditions feed the next), **verifiability** (every skill output has an explicit check).
- Failure mode: **confident-but-unchecked**. As specialized subagents multiply, the risk shifts from missing capability to present-but-unverified capability.
- System move: routing as a learned policy, not a fixed rule set, paired with post-condition checks at every step.

### What's missing in evaluation

- Outcome metrics answer whether the task was solved. Process metrics answer how.
