---
type: article
status: raw
quality: 1
topics: [agent-evaluation, error-analysis, multi-agent-systems, evaluation-metrics]
source: https://developers.openai.com/cookbook/examples/partners/macro_evals_for_agentic_systems/macro_evals_for_agentic_systems
created: 2026-08-16
published: 
author: Shikhar Kwatra, Will Thieme, Bradley Strauss
flashcards: none
updated: 2026-08-17
---

# Macro Evals for Agentic Systems

<div align="center">
  <img src="https://developers.openai.com/open-graph.png" width="220" />
</div>

- When an agentic system fails, the problem is often larger than a single bad response.
    - A handoff may happen too late, a specialist agent may miss the same signal across many runs, or a review process may trigger for the wrong class of cases.
    - To improve the system, teams need to see recurring behavior across the whole population of traces.
- You will learn how to:
    1. Generate or collect many traced agent runs;
    2. Run lower-level evals on each completed run;
    3. Turn each trace into a compact document;
    4. Discover recurring behavior patterns across the population; and
    5. Drill into one high-impact pattern to find where a human should inspect the system next.
- The goal is not to build a perfect taxonomy of every trace. The goal is to show how an AI engineering team can move from thousands of agent events to a small number of patterns that are understandable by both technical and business stakeholders.

![](https://developers.openai.com/cookbook/assets/images/agentic-system-architecture.svg)

- Evals are how AI teams measure whether a system is working.
- Multi-agent systems make this harder because a final answer is only the last event in a longer workflow
- This notebook separates the problem into two levels:
    - **Lower-level evals** grade individual agents, handoffs, tools, and completed runs. In this example, Promptfoo stands in for that agent-level eval layer by grading whether a run handled final decision quality, policy correctness, specialist routing, market drift, and review appropriateness.
    - **Macro evals** look across many lower-level findings. They ask: which kinds of problems repeat, where do they concentrate, and which part of the agent workflow should we inspect first?
- In this notebook, a **bundle** is the evidence packet for one simulated customer-order interaction.
- A bundle matters because macro evals need the workflow evidence behind the final answer.
    - They need to know which agents were consulted, which tools were called, which environment signals were active, whether review was required, and where the workflow changed direction.
    - With that evidence, we can move from “what happened in this one run?” to “which workflow patterns repeat across many runs?”
- The typical bundle is a structured record of a simulated business process
- We can evaluate individual decisions, and we can also ask whether repeated workflow patterns emerge across hundreds of rich interaction records.
- A mature multi-agent system should not rely on final-answer inspection alone. Each launched agent usually needs its own evals: did this specialist use the right evidence, call the right tools, respect policy, hand off at the right time, and produce an output that the rest of the system can trust?
- We also build trace documents.
    - The document is the modeling object that the BERTopic-style section will cluster.
    - The notebook uses `doc_structured_summary` because it is compact but still preserves scenario, routing, state transitions, handoffs, findings, and terminal state.
- The public analysis path is: `case_type -> run_outcome -> eval_finding -> behavior_pattern`
    - The first three labels are known before clustering.
    - The fourth appears after discovery.
- The important numbers are:
    - normalized traces: the bundle-backed population we can inspect;
    - normalized events: the event-level evidence behind those traces;
    - case types: the scenario coverage produced by the generator; and
- The first Sankey plot is a pre-clustering view. It shows how generated case types flow into run outcomes and lower-level findings.

## Trace Documents: Turning Runs into Comparable Text

- A raw agent trace is too detailed to cluster directly.
    - It may contain hundreds of events, long model responses, tool payloads, and repeated status updates.
    - The document construction step compresses each run into a comparable view while preserving the information that matters for macro evals.
    - A good trace document includes:
        - the business setup (`case_type`, selected route, active environment signals);
        - the run outcome and severity;
        - the important handoffs and specialist activations;
        - review/finding markers;
        - a short state-transition digest.
- The example document above is a single trace rendered as a compact narrative.
    - It is intentionally denser than prose but easier to compare than a raw event log.
    - When you adapt this workflow, spend real time on document construction
- The discovery pass is inspired by the BERTopic family of methods.
    - The high-level idea is modular:
        1. **Represent each trace document as a vector.** If the document for trace $i$ is $d_i$, the embedding model produces a vector $e_i = f(d_i)$.
        2. **Reduce the vector geometry.** A reducer such as UMAP maps $e_i$ to a lower-dimensional point $z_i$ that preserves useful local neighborhoods.
        3. **Cluster dense regions.** A density clusterer such as HDBSCAN groups nearby points and can mark outliers as noise.
        4. **Represent each topic.** For each cluster, compute terms that distinguish that cluster from the rest of the corpus.
- This notebook uses the helper module to keep the implementation compact, but the major mathematical ideas are visible:
    - A trace belongs to a cluster $k$ when its document vector is near other trace vectors in the reduced space.
    - A term is useful for labeling cluster $k$ when it appears often inside $k$ and less often elsewhere.
    - A simple class-aware term score is: $$ score(t, k) = tf(t, k) \times \log\left(\frac{1 + N}{1 + df(t)}\right) $$
        - where $tf(t, k)$ is the term frequency for term $t$ inside cluster $k$, $df(t)$ is the number of clusters/documents where the term appears, and $N$ is the comparison population size.
        - The exact implementation can vary, but the intuition is stable: labels should describe what makes a cluster distinctive.
- Finally, we rank patterns by a triage metric: $$ impact\_score(k) = prevalence\_share(k) \times severity\_weighted\_prevalence(k) $$
    - This is not a universal risk formula. It is a practical prioritization score: a pattern matters more when it is both common and severe.
- This step appears here because BERTopic-style discovery has just given every risky trace a `behavior_pattern`.
    - Before clustering, we could compare generated cases, outcomes, and lower-level eval findings.
    - After clustering, we can ask a more useful macro-eval question: **where does each discovered behavior pattern concentrate?**
- The idea is to compare two shares:
    - **overall pattern share**: among all clustered traces, what share belongs to this behavior pattern?
    - **slice pattern share**: within one slice, such as `case_type = supplier_substitution_compound`, what share belongs to this behavior pattern?
    - Then we compute: $$ lift = \frac{slice\ pattern\ share}{overall\ pattern\ share} $$
        - A lift of `1.0` means the pattern appears in that slice about as often as it appears overall.
        - A lift above `1.0` means the pattern is concentrated in that slice.
        - A lift below `1.0` means it is less common there.
- In macro evals, this is the bridge from discovery to action. A behavior pattern is easier to investigate when we can say where it shows up: a generated scenario, an agent version, an orchestration mode, a market regime, or a review state.
- A business stakeholder can use this to ask, “Which order scenarios are creating the most repeated operational issues?”
    - An AI engineer can use it to ask, “Which lower-level findings are actually the same routing or decision pattern?”
    - Both views are useful, and the Sankey gives them a shared map.
- Discovery tells us what repeats. Diagnosis asks where to inspect first.
    - For a selected behavior pattern, we reconstruct a lightweight execution graph: $$ G = (V, E) $$ where each node $v \in V$ is a normalized trace event and each edge $e \in E$ links events through temporal order, handoffs, tool calls, and nearby execution context.
    - We then choose a focus event, also called an anchor. In this simulation, a focus event is usually a review/finding marker, failure-related status, or late-stage decision event.
- The more actionable rows are the operational events around that marker: handoffs involving the orchestrator, tool/function calls by monitor or orchestration agents, procurement-planning handoffs, and related specialist responses.
    - Those are the places a human should inspect after the macro eval points to this pattern.
    - From a technical perspective, this output tells an AI engineer where to inspect:
        - agent instructions and tool contracts for the named agents;
        - handoff rules around the repeated transition;
        - whether the system is recording review markers too early or too late;
        - whether a tool output is being ignored or over-weighted.
- Practical next steps for an AI engineering team:
    - promote the clearest lower-level eval failures into a regression suite;
    - review a small sample of automated grades to calibrate rubric strictness;
    - track behavior patterns by model version, prompt version, and orchestration mode;
    - assign business owners to the highest-impact patterns;
    - inspect the top suspect agents, tools, and handoffs before changing the system.
- Practical next steps for a business stakeholder:
    - decide whether the generated case types match the real operating risks;
    - check whether high-impact patterns correspond to important customer or operational outcomes;
    - validate whether review thresholds are producing the intended business behavior;
    - use the Sankey and heatmap views to prioritize which scenarios need better policy or process design.
