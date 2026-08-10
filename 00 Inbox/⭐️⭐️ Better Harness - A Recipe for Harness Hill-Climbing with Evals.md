---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/vtrivedy10/status/2041927488918413589/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-04-08
author: Viv
flashcards: none
updated: 2026-08-08
---

# Better Harness: A Recipe for Harness Hill-Climbing with Evals

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1805079750873923584/7sTh63Eo.jpg" width="220" />
</div>


### Evals are training data for Agents

- In classical machine learning, training data guides the model’s learning process. Each training example contributes a gradient that updates the model’s weights toward “correctness.” We have a similar learning loop for agents.
- model + training data + gradient descent → better model
- harness + evals + harness engineering → better agent

![](https://pbs.twimg.com/media/HFWuXCaXEAAI6CA.jpg)

- **Evals encode the behavior we want our agent to exhibit in production.** They’re the "training data" for harness engineering. Each eval case contributes a signal like “did the agent take the right action” or “produce the right outcome?” That signal guides the next proposed edit to the harness.
- Better-Harness is a take on compound systems engineering.

### Sourcing good evals

- Here are the practical ways we source, curate, and use them.
- **Hand-curated.** For any given task, the team manually writes examples that capture what we think the agent should do in production. These are often high value, but difficult to generate at scale.
- **Production traces.** Every agent interaction generates a trace where failures become eval cases. Mining traces for eval material is the leverage, high-throughput way to improve evals over time
- **External datasets.** These datasets are useful but need to be manually curated to make sure the test cases used to improve the agent reflect desired behaviors
- **Tag everything.** Every eval gets tagged to behavioral categories: "tool selection," "multi-step reasoning," etc. Tags enable meaningful holdout sets and targeted experiments. It also saves a lot of money because we can run subsets of evals.

### Building learning systems that generalize

- The ideal outcome for any learning system is **generalization**. We give an input signal that captures the distribution of behaviors we want in the wild. The system fits to it and then “just works” on new inputs it's never seen.
- **The obvious problem:** We don't have unlimited data. **The fix:** Encode important behaviors into curated evals. Quality > quantity, a small set of well-tagged evals covering the behaviors you care about beats thousands of noisy but high-coverage evals.
- Holdout sets become a proxy for true generalization. We’ve seen approaches that We pair with human review as a second signal and we get semi-automated systems can improve scores while avoiding behaviors we don’t want in prod.

### Better-Harness: a recipe for hill climbing your harness

- We created a scaffold for autonomously improving our harness using evals as a signal in each step
- • **Source and tag evals.** This is a mix of hand-writing evals, mining them from production traces, and using/adapting external datasets. We tag each eval to behavioral categories (like multi-step retrieval) and regularly remove evals that are saturated or we longer feel are useful for the agent + current generation of models. • **Split data per category.** Create Optimization and Holdout sets. This is very important! We find that autonomouos hill-climbing has a tendency to overfit to tasks so holdout sets ensure that learned optimizations work on previously unseen data, though the general distirbution should match existing evals. This mirrors what production will look like. • **Run a Baseline.** Run a baseline experiment on the Optimization & Holdout sets before any edits. This grounds all updates in the update steps. • **Optimize.** Each iteration runs autonomously with optional human review. **Diagnose** errors from traces. **Experiment** with a targeted harness change. We scope to one change at a time to avoid confounding but that may mean updating a prompt and tool simultaneously so the system works well together. • **Validate:** In each step, the loop checks to make sure that the proposed change helped pass new evals while avoiding regressions on existing passing cases. It’s common that some change results in a net overall score gain with some regressions. The agent gets context of these regressions so it can try to fix them in the next update without losing the gains from the existing update. • **Human review.** We manually review changes and edge cases metrics miss. This often includes instructions that are overfit to the optimization set and although they don’t hurt generalization, they end up being a waste of tokens. This gives us another sanity check and gate against overfitting.

![](https://pbs.twimg.com/media/HFWuqdyXYAAaEnx.jpg)

### Examples of harness changes

- **Prompt and instruction updates.** The most common change. The agent keeps misinterpreting a tool's output format, or it's too aggressive about calling a tool when it should ask a clarifying question first. The fix is a targeted instruction update addition like "when querying multiple files that have dependent information, offload information to the filesystem and re-aggregate before giving a final answer."
- **Adding or updating a tool or tool description.** The agent may fail contextualizing when to use a new tool. Edits include examples on of how to use, how to chain this tool, an updated tool description, and editing the overall tool suite to disambiguate similar tools

### Evals maintenance & regressions

- Along with hill climbing, evals also explicitly capture and protect against regressions over time. Once our agent handles a case correctly, we don’t want to lose that gain. The eval becomes a regression test.

### The Future: automated error detection & fixes

- This approach works because **traces give us a dense feedback signal**. Evals benefit from traces to compare across versions and numerically ground which changes contribute to a better score (which should be a good proxy for a better user experience).
- Overall, we point agentic compute at traces to:
    - **Derive errors automatically.** We want to constantly monitor our agent traces to classify and cluster failures in production.
    - **Generate evals from production.** A trace where the agent made a mistake is an eval case. A trace where a user corrected the agent is even better. The flywheel: more usage → more traces → more evals → better harness
    - **Compare harness versions.** Side-by-side trace comparisons show what changed in the harness that contributed to new behavior
