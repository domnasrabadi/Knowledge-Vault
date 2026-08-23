---
type: paper
status: raw
quality: 1
topics: [ai-agents, model-risk-validation, llm-risks, model-monitoring, multi-agent-systems]
source: https://arxiv.org/abs/2604.05229v1
created: 2026-08-22
published: 2026-04-06
author: Christopher Koch
flashcards: none
updated: 2026-08-23
---

# From Governance to Agentic Controls

### Abstract

- Agentic AI systems plan, use tools, maintain state, and produce multi-step trajectories with external effects. Those properties create a governance problem that differs materially from single-turn generative AI: important risks emerge during execution, not only at model development or deployment time
- This paper proposes a layered translation method that connects standards-derived governance objectives to four control layers: governance objectives, design-time constraints, runtime mediation, and assurance feedback
- standards should guide control placement across architecture, runtime policy, human escalation, and audit, while runtime guardrails are reserved for controls that are observable, determinate, and time-sensitive enough to justify execution-time intervention

### Introduction

- Large language model (LLM) systems are increasingly embedded in agentic applications that can decompose tasks, invoke tools, preserve memory, coordinate with external services, and generate long action sequences with limited human intervention.
    - This transition changes the control problem.
    - A conventional generative model can often be assessed at the level of prompts, outputs, and offline evaluation.
    - By contrast, an agent may look harmless at each individual step while still producing an unacceptable trajectory when its actions are composed over time.
- The real question is therefore not whether standards can be compiled directly into guardrails, but how standards-derived objectives should be translated across design-time, runtime, and assurance layers.
- This paper argues for that narrower and more useful claim. It makes three contributions:
    1. It distinguishes governance objectives, technical controls, runtime guardrails, and assurance evidence as different artifacts with different roles.
    2. It proposes a governance-to-control translation method centered on an explicit control tuple, a runtime-enforceability rubric, and layer assignment.
    3. It demonstrates the method with a procurement-agent case study and derives an evaluation agenda grounded in recent runtime-governance and agent-safety literature.

### Why Direct Translation Is Insufficient

- ISO/IEC 42001, ISO/IEC 23894, ISO/IEC 42005, ISO/IEC 5338, ISO/IEC 38507, and the NIST AI RMF are frameworks for management, risk, lifecycle, impact, and governance.
    - By themselves they do not define a policy language, an action schema, or an execution model.
    - Treating them as direct guardrail specifications conflates governance objectives with technical mechanisms, and an organization can satisfy a governance framework while its deployed agent still lacks meaningful runtime controls.
- Requirements related to fairness, proportionality, human acceptability, or societal impact require contextual judgment that cannot be safely reduced to a deterministic runtime rule without substantial normative simplification, and recent policy-compilation work still depends on interpretation, provenance, and human oversight rather than naive automation
- Dong et al.’s survey of LLM safeguards shows that even non-agentic safety mechanisms are layered, context-sensitive, and incomplete.
    - For agents, the problem is harder because decisions unfold across tool calls and trajectories rather than one-shot outputs.
    - AgentDoG, WebGuard, ToolSafe, and Agent-SafetyBench collectively show both the need for action-level controls and the gap between current guardrail performance and high-stakes reliability
- A poorly scoped agent with broad tool access cannot usually be made safe by runtime filtering alone.
    - Huang et al. argue that pre-execution intervention is often safer than post-execution filtering because some harms become irreversible once actions execute.
    - More broadly, some controls belong in architecture, model choice, network isolation, human workflow design, and post-deployment assurance rather than live policy checks alone; broader assured-autonomy work makes the same point by treating runtime assurance as one element within a larger design-time and operation-time assurance regime.

### Governance-to-Control Translation Method


#### Different Artifacts Need Different Layers

- A stronger argument begins by separating four kinds of artifacts that are often conflated.
    - **Governance objective:** a normative goal such as accountability, least privilege, impact awareness, or risk reduction, often sourced from a standard, regulation, or internal policy.
    - **Technical control:** a mechanism intended to operationalize some aspect of that objective, such as scoped credentials, approval gates, logging, or anomaly detection.
    - **Runtime guardrail:** a subset of technical controls that intervene during execution by allowing, denying, delaying, escalating, or reshaping actions.
    - **Assurance evidence:** artifacts used to demonstrate what controls exist, whether they executed, and with what effect, such as logs, signed attestations, audit traces, incident reports, or validation records.

#### Step 1: Extract the Normative Objective

- Begin with a standards-derived statement or organizational policy objective. Example forms include “ensure access is authorized and auditable,” “assess impacts on affected parties,” or “maintain continual monitoring and improvement”.

#### Step 2: Normalize It into a Control Tuple

- Any candidate control should be rewritten into a structured tuple

$$
\kappa = \langle a, x, r, \phi, \delta, \epsilon, o \rangle
$$

- where $a$ is the acting principal (human, agent, or sub-agent), $x$ is the action class, $r$ is the protected resource or external effect, $\phi$ is the precondition or relevant context, $\delta$ is the control decision (allow, deny, escalate, log-only, or rewrite), $\epsilon$ is the evidence artifact to be produced, and $o$ is the accountable owner
    - makes the proposed control concrete enough to inspect, compare, and audit

#### Step 3: Score Runtime Enforceability

- Next, assess whether the objective is actually suitable for runtime enforcement. A control should be considered a strong runtime candidate only when the protected event is observable before execution, the decision rule is sufficiently determinate, the intervention is operationally tolerable, and post hoc review would be too late

**Runtime-enforceability rubric**

| Criterion | High runtime-enforceability | Low runtime-enforceability |
| --- | --- | --- |
| Timing of harm | Harm must be prevented before execution | Harm is mainly evaluable after the fact |
| Pre-action observability | Required state and context are machine-observable | Critical context is absent or only discoverable later |
| Rule determinacy | Policy can be written as a crisp operational rule | Policy requires open-ended interpretation or balancing |
| Judgment load | Limited social or ethical judgment required | Human or contextual judgment is central |
| Reversibility | Mistakes are hard to undo; intervention is urgent | Action can be audited or corrected later |
| Evidence clarity | Control outcomes can be logged and attributed cleanly | Evidence is ambiguous or weakly attributable |

- a control cannot reliably operate online when the trigger is unobservable, the protected object is too diffuse, the required context is unavailable, or the intervention itself is operationally untenable

#### Step 4: Assign the Primary Control Layer

- The objective is then assigned to one or more layers:
    1. **Governance objective layer:** normative intent, ownership, thresholds, and exceptions.
    2. **Design-time layer:** architecture, least-privilege scoping, tool exposure, dataset and prompt boundaries, sandbox design.
    3. **Runtime layer:** action validation, policy checks, approval gates, dynamic authorization, anomaly detection, and containment.
    4. **Assurance layer:** telemetry, audits, incident review, attestation, and performance or drift monitoring.
- Human escalation cuts across the stack and is the default destination for ambiguous, high-impact, or low-determinacy decisions

#### Step 5: Specify Evidence and Ownership

- Every translated control must name both the evidence artifact and the accountable owner

### Worked Case Study: Enterprise Procurement Agent

- To make the method concrete, consider an enterprise procurement agent that can search approved vendor catalogs, retrieve contract data, compare quotes, draft purchase orders, and send requests for approval or vendor communication

| Requirement | Runtime enforceability | Primary implementation layer(s) | Example evidence artifact |
| --- | --- | --- | --- |
| Only approved vendors may receive purchase orders | High | Design-time vendor-directory scoping + runtime vendor-ID allowlist check before PO creation | Signed action trace showing vendor lookup, policy decision, and PO event |
| Purchases above EUR 5,000 require human approval | High | Runtime approval gate with delegated identity and threshold check | Approval token, requester identity, timestamp, and immutable approval log |
| The agent may access only systems necessary for procurement tasks | High to medium | Design-time least-privilege credential scoping + runtime authorization for specific tools and actions | Issued scopes, access logs, denied-action logs |
| Supplier ranking should remain fair, explainable, and contestable | Low | Design-time ranking design + assurance audit + human review for exceptions | Periodic audit report, explanation template, exception register |
| All state-changing actions must be attributable and replayable | Medium to high | Runtime telemetry + assurance retention and replay pipeline | End-to-end trace with actor, tool calls, arguments, results, and policy outcomes |

- This example clarifies the central thesis.
    - The first three requirements are good runtime candidates because the relevant state is available before execution and the rules are crisp.
    - The fourth is not a strong runtime candidate because “fair and contestable” is too open-ended to encode safely as a deterministic pre-action check.
    - The fifth spans runtime and assurance because logging must happen during execution, but replayability and review are post hoc functions.

### Evaluation Criteria

- **Policy Fidelity** — Does the translated control preserve the meaning of the original governance objective, or has it narrowed a broad requirement into a misleading heuristic?
    - This is especially important for standards-derived controls that mix legal, organizational, and technical language.
- **Intervention Quality** — For runtime controls, what are the precision and recall on harmful actions, and what benign actions are wrongly blocked?
    - WebGuard and ToolSafe show both the need for action-level intervention and the difficulty of achieving adequate accuracy.
- **Trajectory Coverage** — Can the control reason over partial paths, delegated sub-agents, tool arguments, and accumulated state, or does it only moderate isolated prompts?
    - Path dependence is central for agentic governance.
- **Safety–Utility Trade-off** — What latency, task-completion loss, false-escalation burden, or additional human review load is introduced by the controls?
    - Runtime safety that destroys usability will be bypassed in practice.
- **Evidence Completeness** — Can a third party later determine which policy fired, whether the declared guardrail actually executed, and which human or service owned the decision?
    - Proof-of-Guardrail shows that even execution claims may require verification mechanisms.

### Limitations and Threats to Validity

- relies on public scope statements and summaries for the ISO documents rather than exhaustive clause-by-clause interpretation
- Sector-specific law, organizational process, and human judgment remain indispensable

### Conclusion

- Directly compiling ISO and NIST standards into runtime guardrails is too strong.
    - Standards define governance intent, management expectations, and risk questions; runtime guardrails are only one family of mechanisms for operationalizing those goals
- The practical implication is simple: each control should be placed in the layer best suited to enforce it
    - Runtime guardrails matter most where events are observable, rules are crisp, and intervention must occur before harm; elsewhere, architecture, review, and assurance should carry the load.
