---
type: article
status: inbox
quality: 1
topics: []
source: https://agussudjianto.substack.com/p/governance-is-not-a-prompt
created: 2026-08-08
published: 2026-04-22
author: Agus Sudjianto
flashcards: none
updated: 2026-08-08
---

# Governance Is Not a Prompt

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!pqZ8!,f_auto,q_auto:best,fl_progressive:steep/https%3A%2F%2Fagussudjianto.substack.com%2Ftwitter%2Fsubscribe-card.jpg%3Fv%3D-113270224%26version%3D9" width="220" />
</div>

- On April 17, 2026, the Federal Reserve, OCC and FDIC issued revised interagency guidance on model risk management, replacing SR 11-7 after fifteen years
- It explicitly excludes agentic AI from the scope of model risk management.
- That is a remarkable admission. MRM was built to govern *models* — statistical artifacts that transform inputs into outputs. Its tools assume that governing the model is enough, because the model is the thing that makes the decision. For agentic AI, that assumption breaks. The agent is not a model. The agent is a system that uses models to perceive, reason, plan, call tools, act and evaluate — often across many steps, often across many systems and often without a human in sight.
- Governing the model is necessary. It is no longer sufficient.
- Governance answers questions such as these: What is the system allowed to do? Under what conditions? According to which policy? Which policy version applied at the time? What evidence was checked? What actions are blocked automatically? What requires escalation? Who owns the decision? Who reviews the logs? What happens after a failure?
- A system is governed when those questions have clear, external and durable answers.
- This distinction becomes sharper in agentic AI because the system does not merely answer questions. It can decompose tasks, navigate ambiguity, select tools, interact with enterprise systems and keep going. The governance burden therefore moves from single outputs to end-to-end behavior.

### Human in the Loop Is Not Governance

- Human in the loop is a control. Governance is the system that defines when, why, how and by whom that control is used.
- A person reviewing an output does not by itself establish authority, policy precedence, evidence requirements, escalation paths, traceability or accountability
- This matters because human review often collapses into ceremony. Reviewers get overloaded. They see only a summary, not the full chain of reasoning or tool use. They may not understand the relevant policy. They may approve mechanically because the system usually “looks fine.”
- In that setting, the human is not governing the system. The human is absorbing the residual risk of a system that is not truly governed.

### Why the Standard Harness Fails

- The dominant pattern in today’s agentic systems is what might be called the standard harness. The agent operates with a governing prompt, some flat-file memory and an LLM-based evaluator or judge. Each mechanism tries to steer or inspect behavior. None of them provides governance-grade assurance.
- Prompts are useful, sometimes extremely useful. They can shape behavior, establish tone, provide instructions, constrain role and improve consistency. But they do not impose hard boundaries.
- A prompt is just text presented to a probabilistic model. It can be ignored, diluted, reinterpreted or crowded out by other context. In a complex multi-step task, the model may drift from the original instruction. In a retrieval-heavy or tool-using system, the prompt can compete with user content, retrieved content and tool-returned content. Under adversarial conditions, it can be attacked directly through prompt injection. Even under benign conditions, it remains non-deterministic.
- Governance cannot depend on a fuzzy retrieval layer over prose files. It needs controlled state, version discipline, provenance and explicit precedence.
- The LLM-as-judge pattern is perhaps the most misleading of the three. It sounds rigorous. A second model reviews the first. There is evaluation, reflection, maybe even scoring. But in high-risk settings, what matters is often not whether the answer sounds plausible. What matters is whether it is correct.
- This is the core failure of LLM judge in governance contexts: **it tends to evaluate in semantic space while the risk often lives in logical, numerical and procedural exactness.**
- Worse, the judge often shares the same basic representational weaknesses as the actor. One probabilistic system produces the answer. Another probabilistic system declares it acceptable. Internal agreement is then mistaken for control. But shared failure modes are not independence. They are correlated error.
- Governance is not achieved by stacking more text around a model. **Governance requires external structure that the model cannot override.**

### What a Governed Agentic Architecture Actually Requires

- It means that verification must be typed. Not every claim should be handled the same way. A factual claim, a threshold claim, a policy claim, a tool-use claim and a semantic claim do not belong to one vague “judge” function. They require different verifiers:
    - Some need deterministic threshold checks
    - Some need exact lookup
    - Some need contradiction detection
    - Some may still use semantic evaluation — but only where semantics is actually the thing being judged
- It means behavioral contracts must exist for workflows. An agent should not be able to skip required stages simply because the language model decided they were unnecessary. Certain steps should be structurally mandatory. Certain actions should be blocked at the tool gateway if prerequisites are missing, permissions are insufficient or contradictions are detected.
