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

**Short answer.** Re-validate every judge that will score outputs from the new system, which in practice is nearly all of them. Recalibrate only those that fail re-validation. The architecture change doesn't itself invalidate the old calibration. It triggers two mechanisms that can:

- **Output shift.** The responses being judged change, so the judge may no longer apply the rubric accurately.
- **Criteria drift.** SMEs' definition of "good" may change once they see new kinds of output, so the rubric itself may no longer be the right target.

## Mechanism 1: output shift

A judge is a classifier. You trust it because you have compared its decisions with human labels on a held-out test set and measured how many real failures it catches (TPR) and how many good outputs it correctly passes (TNR) ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-do-i-know-if-i-can-trust-my-automated-eval.html)). Those labels were applied to outputs of the _old_ system, so the TPR/TNR figures are evidence about that output distribution only.

Consolidation changes the system prompt, the tools available on each turn, and the context the model reasons over. Any one of these shifts an LLM's outputs, and here all three change together. Some shift is near-certain. Whether it is large enough to change a judge's error rates is uncertain and has to be tested on this system, and only that second question determines whether recalibration is needed. The evals FAQ already recommends re-running error analysis after significant changes such as prompt updates or model switches ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-often-should-i-re-run-error-analysis-on-my-production-system.html)). An architecture change is larger than either.

Not every shift breaks calibration. What matters is the type:

- **Prevalence shift (label shift: P(y) changes).** Failures become more or less common but look the same. TPR/TNR transfer, and error-adjusted estimates stay unbiased _provided_ the judge's conditional error rates are unchanged ([Lee et al.](https://arxiv.org/abs/2511.21140)). The meaning of an alert does change, though. At 90% sensitivity and 95% specificity, precision is about 67% when 10% of outputs fail and about 15% when 1% fail.
- **Failures look different (P(x|y) changes).** This is the shift that breaks calibration, and the one consolidation most plausibly causes. Routing and handoff errors disappear. Tool confusion (for example, peer-cohort data used to answer a savings question) and constraint loss across mode switches appear. Aggregate TPR is a mix of per-subtype TPRs, roughly Σ wₖ·TPRₖ, so it moves when the subtype mix changes even if the judge is equally good at each subtype. Brand-new subtypes have no measured TPR at all. This is exactly the invariance assumption that Lee et al.'s guarantee depends on.
- **Judge-input shift.** Identical answers can arrive wrapped in a different trace structure. Consolidation reduces _total_ tokens by removing inter-agent communication ([Li](https://arxiv.org/abs/2601.04748)). But a judge that used to see one specialist's sub-trace may now see one context spanning every capability. Evidence-grounded judging is already hard: the best model reaches only about 55% consistent accuracy on [ContextualJudgeBench](https://aclanthology.org/2025.acl-long.470/). Extra context can also degrade judges directly ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-much-of-a-trace-should-i-give-an-llm-judge.html)).

## Mechanism 2: criteria drift

Output shift asks whether the judge still applies the existing rubric accurately. Criteria drift asks whether the rubric still captures what SMEs consider acceptable.

In a study of practitioners building evaluators, participants added new criteria when they encountered new types of bad output, and reinterpreted existing criteria as they graded more. The authors conclude that criteria depend on the outputs observed, so any pipeline change can trigger drift and may require re-grading ([Shankar et al.](https://arxiv.org/abs/2404.12272), §7.3.1 and §8.1). The evidence is qualitative: nine practitioners on a tweet named-entity task. It shows the phenomenon exists. It doesn't show how often it occurs after architecture changes.

For this chatbot, a plausible case is responses that combine spending insights with product suggestions. These may make SMEs realise that "relevance" needs an explicit rule about when introducing an overdraft is appropriate. That rule may previously have been tacit, because the old architecture rarely produced such combinations.

In shift terms, this is **concept shift (P(y|x) changes)**: the correct label for a given output changes. It is the hardest shift to see, because a judge can match the old labels well while missing current requirements. In that case it has been validated against the wrong target.

Two cautions:

- **The mechanisms are linked.** Output shift is what exposes SMEs to new output types, which is what triggers criteria drift. Expect both together.
- **Drift can run towards the system's behaviour.** In the same study, participants loosened criteria to fit what the model actually produced. In prompt prototyping that's healthy. In second-line validation it's normalisation. Refinements should be justified by customer or business requirements, never by "the new system does this a lot". Externally anchored standards (responsible lending, disclosure, conduct) stay fixed, and any loosening needs the same approval as changing a validation tolerance.

## Where the burden of proof sits

"Transfer is possible" is true. In second-line validation, though, the default runs the other way. Evidence drawn from a population of outputs that no longer exists, and labelled against a rubric that may no longer reflect SME requirements, doesn't count for the new system until it's re-established.

## Triage by judge type

- **Outcome judges** (the answer is correct and grounded; the customer reached the right overdraft pathway). Keep the criteria, subject to the rubric review below. Re-measure TPR/TNR on freshly labelled outputs, and check which slice of the trace each judge now receives.
- **Architecture-bound judges** (routing correctness, context passed at handoffs, each agent staying in scope). Retire the implementation but keep the objective. Routing correctness becomes capability and tool selection. Handoff fidelity becomes constraint retention across mode switches.
- **New failure modes.** Skill-selection accuracy can hold steady and then fall sharply as libraries grow, driven more by semantic confusability than by library size ([Li](https://arxiv.org/abs/2601.04748)). Test transitions between spending, savings, peer comparison and applications. The priority banking risk is an insight conversation ("your cash flow is tight") drifting into an overdraft suggestion without eligibility and suitability steps. If those gates are enforced in code outside the model, the right control is a deterministic assertion. If the old architecture enforced them structurally and the new one leaves them to the prompt, they become a behaviour you need to measure.
- **Tool and state checks.** Use code assertions on tool name, arguments, result, resulting state, authorisation and preconditions ([Husain & Shankar](https://hamel.dev/blog/posts/evals-faq/how-do-i-evaluate-agentic-workflows.html)). These don't need labels for every execution, but a domain owner still has to define the correct rule.

There are three separate adjustments, each with its own trigger:

- **Revise the rubric or judge prompt** when new failures fall outside the criteria, or when SMEs have refined the criteria themselves.
- **Refit the score mapping** when scores no longer track correctness. For binary Pass/Fail judges, this mostly means bias-correcting aggregate pass rates.
- **Move escalation thresholds** when prevalence, review workload or the cost of errors changes.

## Sample sizes

About 100 traces is a sensible pool for _discovering_ failure modes. It is not enough to show that rare failures are absent. At 1% prevalence, 100 random traces have about a 37% chance of containing none, and you need about 300 to be 95% confident of seeing at least one. Judge test sets need roughly 30–50 labelled failures, so use an enriched challenge set and report its detection rates separately from natural-population estimates.

## Recommended sequence

1. **Run matched scenarios through both architectures** on the same customer-data snapshots. Use unlabelled drift signals for each judge (its own pass rate, tool-call mix, output length, embedding drift) to decide where to spend labelling effort. These signals show where things changed, not whether TPR changed.
2. **Re-run error analysis on the new system** and compare its failure taxonomy with the old one. New failure subtypes call for rubric work, not just re-measurement.
3. **Review the rubric before relabelling.** Have SMEs examine a blinded mix of old and new outputs.
    - Re-label a sample of _old_ outputs blind to the original labels. Disagreement with the originals measures criteria drift, net of a test–retest baseline for labelling noise.
    - Failures concentrated in _new_ outputs measure output shift.
    - Document and agree refinements, justify each against customer or business requirements, hold mandated standards fixed, and version the rubric.
4. **Collect blinded SME labels under the versioned rubric** for each surviving judge, from a natural sample plus an enriched failure set. Measure TPR/TNR with intervals against tolerances set in advance. Compute these only against labels made under the same rubric version. Reassess historical labels affected by any refinement before reusing them.
5. **Decide per judge:** keep it, move its threshold, revise its rubric, re-scope it to its underlying objective, or retire it.
6. **Test reachable actions directly.** Probe application tools with missing preconditions, the wrong business identifier, or no customer instruction. A clean run doesn't prove a path is closed. [AgentArch](https://arxiv.org/abs/2509.10769) is a useful template for scoring tool choice, arguments and the final decision together.

## Suggested wording for a validation report

> _The consolidation is expected to alter the output and error distribution on which the judges were calibrated, and may expose evaluation requirements that were previously tacit. Existing calibration evidence is therefore not presumed to transfer. The evaluation rubric will be reviewed by SMEs against outputs from both systems, with any refinements justified, approved and versioned; mandated standards remain fixed. Judge performance will then be re-established on SME-labelled outputs from the new system under the versioned rubric, and recalibration performed where performance falls outside agreed tolerances._