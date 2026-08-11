---
type: article
status: raw
quality: 1
topics: [ai-agents, model-risk-validation, ai-engineering, context-engineering]
source: https://medium.com/@CommBankTechnology/making-agents-safe-and-reliable-via-data-structures-and-enforcement-205722a4c91d
created: 2026-08-08
published: 2026-07-16
author: CommBank Technology Blog
flashcards: none
updated: 2026-08-11
---

# Making Agents Safe and Reliable via Data Structures and Enforcement

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*ShXllfOtUxLfqOiyf6qNmw.png" width="220" />
</div>

- "Tools should enforce correctness. System prompts should improve consistency. Guardrails should enforce non-negotiables."

#### Seven design anti-patterns

1. Control logic in the prompt
2. Workflows that collapse into form-filling
3. Identity exposed as an agent input
4. Consumer modes as agent switches
5. Opaque tool failures with nowhere to go
6. Idempotency in the description, not the tool
7. Prompt constraints that are not measured

- Make the tool enforce it:

  ```python
  @dataclass
  class WorkflowState:
      verification_passed: bool
      target_resolved: bool
      attempts: int

  agent = Agent("model", deps_type=WorkflowState)

  @agent.tool
  def perform_sensitive_action(ctx: RunContext[WorkflowState]) -> str:
      if not ctx.deps.verification_passed:
          return "Verification has not been completed."
      return _do_sensitive_action()
  ```

- Defensively-designed tools check workflow state before proceeding

#### Collapse deterministic tool chains

- A common challenge is a prompt that says: First call Tool A. Then Tool B. Then Tool C. Never call Tool C before Tool B. Never skip Tool A.
- If those tools must always be called in that exact order, they probably should not be separate agent tools but implementation detail of one operation

#### If everything collapses into one tool, maybe you do not need an agent

- **The question to ask is:** is there actual work for the agent to do? If the job is deterministic data collection followed by one backend call, consider that an agent may not be a good solution. If the job requires conversation, ambiguity handling, search, comparison, refinement and repeated attempts to find the right answer, an agent is justified.

#### Idempotency belongs in the tool, not the description

- "Do not call more than once for the same confirmed details unless the user explicitly requests a new result."
- are instructions to the model, not constraints on the tool. The model can ignore them, miscount or be confused by a long conversation. Idempotency is a systems property and should be enforced in the tool.

#### Prompt constraints that are not measured are not guardrails

- System prompts often contain lines like: Do not provide regulated advice. Do not make unsupported product recommendations. Never reveal internal system details.
- These look like constraints, but they are actually requests. The model either follows them or it does not, silently, with no compliance rate, no regression detection and no alerting. You cannot easily measure whether they hold, you cannot tell when a model change impacts their behaviour, and you cannot report them to a risk team with a confidence interval.
- A real guardrail is a separately evaluated control, not a prompt instruction. It might be a classifier, a policy engine, a deterministic validator or an allowlist, but it must be measured independently of the agent
- Because the classifier is a separate service, it has its own measurement pipeline. Violation rate, false positive rate, latency and model accuracy can be tracked independently of agent evals. The classifier can be retrained, upgraded or replaced without touching the agent, and the agent can be changed without affecting the classifier measurement baseline

#### Don't give an agent a choice if it can't go wrong

- Do not let the agent decide whether verification passed. Do not let it decide whether a caller owns a resource, whether retry limits are exhausted, whether sensitive data should be masked, or whether an approval is valid.
- The agent can decide how to ask a question, summarise a result or help the user choose between ambiguous matches, and the system should decide what is allowed.

#### A practical test

- For every instruction in your system prompt, ask: > "Is this steering, or is this control logic?"
- If it is steering, it can stay in the prompt
- If it is control logic, move it into a tool or a guardrail first
- If tools must always be called in the same order, collapse them. If the collapsed workflow is just input collection, ask yourself why you are building an agent. If the workflow involves uncertainty, search, comparison and iterative narrowing, you're probably building an agent that deserves to be an agent.
