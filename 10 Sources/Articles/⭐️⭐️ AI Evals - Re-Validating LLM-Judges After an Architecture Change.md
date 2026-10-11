---
type: article
status: distilled
quality: 2
topics: [llm-judges, model-calibration, model-risk-validation, multi-agent-systems, banking-ai, agent-evaluation]
source: ""
created: 2026-10-11
published:
author: Dom Nasrabadi
flashcards: none
updated: 2026-10-11
---
## Do LLM judges need recalibrating after a multi-agent system is consolidated into a single agent?

**The question.** A small business banking chatbot answers customers' questions about their spending, savings and industry peer comparisons, and guides them through product applications such as an overdraft. It was built as a multi-agent system, with specialist agents each holding a few tools. It is being consolidated into a single agent that holds all the capabilities and tools. Do the LLM judges calibrated on the old system need recalibrating?

**Short answer.** Re-validate every judge that will score outputs from the new system, which in practice is nearly all of them. Recalibrate only those whose re-validation shows degraded agreement with SME labels. The architecture change does not itself invalidate the old calibration. It almost certainly changes the output distribution the calibration was measured on, and that is what warrants fresh evidence.

## Why: the calibration describes a population that has changed

A judge is a classifier. Its trustworthiness comes from comparing its decisions with human labels on a held-out test set and measuring how many real failures it catches (TPR) and how many good outputs it correctly passes (TNR) ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-do-i-know-if-i-can-trust-my-automated-eval.html)). Those labels were applied to _outputs of the old system_, so the TPR/TNR figures are evidence about that output distribution only.

Consolidation changes the system prompt, the tools available on each turn and the context the model reasons over. Any one of these shifts an LLM's outputs, and here all three change at once. That some shift occurs is near-certain. Whether the shift is large enough to change a judge's error rates is uncertain and has to be tested for this system. Only the second question decides whether recalibration is needed. The same evals FAQ recommends re-running error analysis after significant changes such as new features, prompt updates or model switches ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-often-should-i-re-run-error-analysis-on-my-production-system.html)), and an architecture change is larger than any of those.

## Not every shift breaks calibration

What matters is the _kind_ of shift:

- **Prevalence shift.** Failures become more or less common but look the same. TPR/TNR transfer. Error-adjusted estimates stay unbiased under this kind of shift _provided_ the judge's conditional error rates are unchanged ([Lee et al.](https://arxiv.org/abs/2511.21140)). The judge doesn't need changing, but the meaning of its alerts does. At 90% sensitivity and 95% specificity, precision is about 67% when 10% of outputs fail and about 15% when 1% fail.
- **Shift in what failures look like.** This is the shift that breaks calibration, and the one consolidation most plausibly causes. Routing and handoff errors disappear. Tool confusion (for example, using peer-cohort data to answer a savings question) and constraint loss across mode switches appear. Aggregate TPR is a weighted mix of per-subtype TPRs (roughly Σ wₖ·TPRₖ). If the subtype mix changes, aggregate TPR moves even when the judge is equally good at every subtype. Brand-new subtypes have no measured TPR at all, which is exactly the invariance assumption Lee et al. rely on.
- **Shift in what the judge receives.** Identical answers can arrive wrapped in a different trace structure. Consolidation reduces _total_ tokens by removing inter-agent communication ([Li](https://arxiv.org/abs/2601.04748)). But a judge that once saw a single specialist's sub-trace may now see one context spanning every capability. Evidence-grounded judging is already hard, with the best model reaching about 55% consistent accuracy on [ContextualJudgeBench](https://aclanthology.org/2025.acl-long.470/), so a change in input presentation can't be assumed harmless. Extra context can also degrade judges directly ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-much-of-a-trace-should-i-give-an-llm-judge.html)).

**Where the burden of proof sits.** "Transfer is possible" is true, but in second-line validation the default should run the other way. Evidence drawn from a population that no longer exists does not count for the new system until it has been re-established.

## Triage by judge type

- **Outcome judges** (the answer is correct and grounded; the customer reached the right overdraft pathway). Keep the criteria, because what a good answer looks like hasn't changed. Re-measure TPR/TNR on freshly labelled outputs, and check which slice of the trace each judge now receives.
- **Architecture-bound judges** (routing correctness, context passed at handoffs, each agent staying in its scope). Retire the implementation but keep the objective. Routing correctness becomes capability and tool selection. Handoff fidelity becomes constraint retention across mode switches.
- **New failure modes.** Skill-selection accuracy can hold steady and then fall sharply as libraries grow, driven by semantic confusability more than library size ([Li](https://arxiv.org/abs/2601.04748)). Test transitions between spending, savings, peer comparison and applications. The banking risk I'd prioritise is an insight conversation ("your cash flow is tight") drifting into an overdraft suggestion without the eligibility and suitability steps. Whether this needs a judge depends on implementation. If those gates are enforced in code outside the model, the right control is a deterministic assertion. If the old architecture enforced them structurally and the new one leaves them to the prompt, that becomes a behaviour you have to measure.
- **Tool and state checks.** Use code assertions on tool name, arguments, result, resulting state, authorisation and preconditions ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html)). These don't need labels for every execution, but a domain owner still has to define the correct rule.

Distinguish three separate adjustments, each with its own trigger:

- **Revise the rubric or prompt** when new failures fall outside the criteria.
- **Refit the score mapping** when scores no longer track correctness. For binary Pass/Fail judges this mostly means bias-correcting aggregate pass rates.
- **Move escalation thresholds** when prevalence, review workload or the cost of errors changes.

## Sample sizes

About 100 traces is a sensible pool for _discovering_ failure modes. It is not enough to show rare failures are absent: at 1% prevalence, 100 random traces have about a 37% chance of containing none, and you need about 300 to be 95% confident of seeing at least one. Judge test sets need roughly 30–50 labelled failures, so use an enriched challenge set, and report its detection rates separately from natural-population estimates.

## Recommended sequence

1. **Run matched scenarios through both architectures** on the same customer-data snapshots. Use unlabelled drift signals for each judge (its own pass rate, tool-call mix, output length, embedding drift) to decide where to spend labelling effort. These signals show where things changed, not whether TPR changed.
2. **Re-run error analysis on the new system** and compare the failure taxonomy with the old one. New subtypes call for rubric work, not just re-measurement.
3. **Collect blinded SME labels** for each surviving judge, from a natural sample plus an enriched failure set. Measure TPR/TNR with intervals against tolerances set in advance.
4. **Decide per judge:** keep, move the threshold, revise the rubric, re-scope it to its underlying objective, or retire it.
5. **Test reachable actions directly.** Probe the application tools with missing preconditions, the wrong business identifier, or no customer instruction. A clean run doesn't prove a path is closed. [AgentArch](https://arxiv.org/abs/2509.10769) is a useful template for scoring tool choice, arguments and final decision together.

### Validation report example wording:

> _The consolidation is expected to alter the output and error distribution on which the judges were calibrated. Existing calibration evidence is therefore not presumed to transfer and will be re-established on SME-labelled outputs from the new system; recalibration will be performed where judge performance falls outside agreed tolerances._
