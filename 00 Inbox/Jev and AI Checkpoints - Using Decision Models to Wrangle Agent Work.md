---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/josharosen/status/2102107649705734413/?s=12&rw_tt_thread=True
created: 2026-10-18
published: 2026-09-21
author: Josh Rosen
flashcards: none
updated: 2026-10-18
---

# Jev and AI Checkpoints: Using Decision Models to Wrangle Agent Work

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1418279052805353474/zn_g71-U.jpg" width="220" />
</div>

- Then Jev showed up, and it fit this architecture almost perfectly. Checkpoints already give us a place to inspect the work before it moves forward. Jev lets us add fast semantic processing right at that boundary. It’s quick enough to understand something about the work, make decisions about it, record what we learn, and feed those observations back into what happens next without slowing down the agent.

### How We Try to Keep Agents on Track Today

- We already have a growing toolbox for keeping agents under control. Before production, evals and simulations test whether they behave correctly across known and adversarial tasks. During execution, sandboxes, permissions, approval gates, and deterministic checks constrain what they can do
- We can also watch and evaluate the execution. Tracing systems like ⁠[LangSmith](https://www.langchain.com/langsmith-platform) record what happened inside the run, while deterministic evaluators, LLM-as-a-judge, and human review decide whether particular behavior or output looks right. These checks can happen offline or ⁠[against production traces](https://docs.langchain.com/langsmith/online-evaluations-llm-as-judge).
- Or we can reduce the problem by giving the agent less freedom in the first place. Workflows and orchestration encode more of the path ourselves: chains, routers, approval nodes, evaluator loops, and other predefined transitions. Anthropic draws this line explicitly between ⁠[workflows that follow predefined code paths and agents that dynamically direct their own process](https://www.anthropic.com/engineering/building-effective-agents).
- All of these approaches have a place, and most serious systems will combine them. But we’re usually either watching the execution, checking it, or constraining it

### Checkpoint But Don’t Smother

- A checkpoint defines a state the work needs to reach without defining exactly how the worker gets there. A research checkpoint might require a set of claims grounded in evidence. A software checkpoint might require an implementation tied back to its requirements with verification attached. A customer workflow might require an extracted requirement connected to the exact conversation from which it was derived.
- Between those checkpoints, the agent can cook

### Jev Adds Semantic Processing to the Checkpoint

- Jev arrived at just the right time for this architecture
- What we didn’t have was a true decision model that couldco evaluate every artifact against the fuzzier parts of that contract without turning the checkpoint into another expensive LLM step.
- Jev fits naturally into that job. Now we can establish that an artifact comes from the right upstream work and carries the required evidence, while also asking to what degree that evidence supports the claim, whether an implementation satisfies its requirement, or whether something extracted from a conversation really represents a requirement.
- Importantly, this lets the checkpoint model express gray areas without giving up the contract. Before, the semantics around advancing the work were mostly absolute: this artifact exists, this relationship is valid, this evidence is present. Now the model can also say that an artifact should advance only if there is sufficient probability that the evidence supports the claim, or that an implementation satisfies its requirement.

### Checkpoints Generate Useful Data

- Validation and interpretation are close cousins. Once a checkpoint can semantically validate work and reject it when necessary, it can just as easily ask what else is true about that work without making the answer part of the gate.
- That makes checkpoints useful for much more than validation
- Every checkpoint can now generate new data about the work while the work is passing through. The same semantic processing we use to govern whether work moves forward can also help a human, or another agent, understand what is happening. The more work that passes through checkpoints, the richer that data becomes.

### The Real Work Is the Connective Tissue

- The more I work with Jev, the more convinced I am that the interesting architecture isn’t System 1 or System 2 on its own. It’s everything we build between them. We now have frontier models capable of doing increasingly open-ended work and decision models capable of making fast semantic judgments around that work. Neither tells us how to put the whole system together.
- The checkpoints, contracts, artifacts, context, policies, feedback loops, and other deterministic connective tissue are what let System 1 and System 2 work together. I suspect a lot of the hard engineering in the next generation of AI systems happens right there.
