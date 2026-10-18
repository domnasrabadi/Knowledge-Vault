---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/satyanadella/status/2108931348857827686/?s=12&rw_tt_thread=True
created: 2026-10-18
published: 2026-10-10
author: Satya Nadella
flashcards: none
updated: 2026-10-18
---

# Models as Insider Risks in the Super Intelligence Era

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1221837516816306177/_Ld4un5A.jpg" width="220" />
</div>

- As traditional software systems were being deployed across the economy over the last few decades, we had the tools and capability to trace behaviors to a specific code path.
- We can’t attribute model behaviors and outputs to specific inputs of training data or configurations of model weights. And yet we are deploying these complex agentic systems and models, with access to our most sensitive data and giving them the ability to take mission-critical actions on our behalf!
- We simply can't outsource responsibility for what intelligence does on our behalf. A model provider’s assurances do not relieve us of that responsibility.
- We can’t treat Super Intelligence as a set of nested black boxes and simply accept or reject its recommendations, answers, and actions. We must build contained systems whose behavior we can observe, limits we can test, and actions we can always contain.
- Setting aside the hard problem of alignment, we need to start with an engineering approach to containment and governance. We need to surround non-deterministic models with strong, deterministic system design, human controls, and reliable operating procedures, and establish industry standards where existing ones are insufficient.
- This isn’t new! We’ve established best practices and refined them over decades (establish identity, limit privileges, log activity, create containment boundaries, etc.) And we are now beginning to apply these same principles to SI inside the enterprise. It starts with model CoT transparency as a non-negotiable. “Neuralese” cannot be a justification for model reasoning to be opaque. But CoT transparency alone is not sufficient or dependable, because we don’t yet know how to make model outputs themselves consistently faithful or transparent! You can and you should use models to adversarially test and verify each other. However, you can then end up with an opaque model inside an opaque orchestration layer, watched by another opaque model. Essentially nested black boxes.
- It’s why the controls that govern what a model can access and what actions it can take must sit outside the model. This builds on an information security principle dating back to the 1970s that a program must not be able to bypass or tamper with the mechanisms that enforce its permissions.
- Today this means separating the model from the harness that orchestrates its work, as well as the action space that defines what it can do. It also means externalizing controls and safeguards.
- **Observe everything:** Every meaningful model action must leave tamper-proof human readable evidence. If it can’t be observed, it can’t be trusted! We need to be able to reproduce how an outcome was achieved without relying on the model to attest to it.
- **Verifiability:** We need to continuously test the entire system, including failures, attacks, edge cases, system changes, etc. not just successful tasks.
- **Independent controls:** Orgs should be able to independently determine what a model can access and what actions it can take.
- **Independent auditability:** Validation must be independent of the intelligence being validated. No single model should control both a system’s behavior and the evidence required to determine whether that behavior is aligned with the original intent.
- **Incident disclosure:** When these systems do fail or are compromised, we need timely disclosure to those affected and mechanisms to share what went wrong, which controls failed, and how to prevent it from happening again and share learnings industrywide.
