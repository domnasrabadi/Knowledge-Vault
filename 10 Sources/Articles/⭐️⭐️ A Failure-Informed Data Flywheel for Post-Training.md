---
type: article
status: raw
quality: 2
topics: [llm-fundamentals, error-analysis, synthetic-data, llm-judges]
source: https://x.com/cyrusasg/status/2097358742950207767/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-09-08
author: Cyrus
flashcards: none
updated: 2026-09-14
---

# A Failure-Informed Data Flywheel for Post-Training

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2087655525408440320/XI3DzpDz.jpg" width="220" />
</div>

- For any model that's fine-tuned and deployed against live traffic, the quality ceiling is often less constricted by the optimizer or the architecture, but rather by the dataset
- Much of the leverage in post-training lives in a few properties of the data and how it's scheduled:
    - **Quality**: are the target outputs/graders perfectly executed and high-signal, or is the model quietly internalizing subtle errors, hallucinations from noisy labels?
    - **Diversity:** does the dataset cover the inputs the model actually sees in production, especially the inputs where it fails?
    - **Complexity:** are the examples hard enough to be worth training on, or is the set dominated by cases the model already gets right?
    - **Scheduling:** is the data constructed once and frozen, or is it rebuilt each cycle against the currently deployed model and fed back into the training loop?
- Getting all four right, with a construction process tightly coupled to the training loop, unlocks gains that a one-shot pipeline can't reach.
    - What ties them together is failure.
    - Mining the current checkpoint's own failures, building datasets targeted at where it's breaking, and feeding those corrections back into the next training cycle allows gains to compound across cycles.
- Most models that are fine-tuned and deployed face the same trajectory.
    - The training distribution is a snapshot, frozen at one moment.
    - The alternative is to treat training as a continuous loop, and to make data curation the thing that loop optimizes
- The rest of this post walks through that loop:
    - how golden labels/graders are produced (a council of LLMs),
    - how failures are surfaced (mining and clustering),
    - how the dataset is rebalanced toward them (upsampling),
    - how the complexity of each example is measured and turned into a training schedule (curriculum),
    - how gaps that real data can't fill are closed (synthetic generation),
    - and how the whole pipeline couples to the training loop to produce a model that is robust across all discovered failure modes.

![](https://pbs.twimg.com/media/HRj7kiWaMAAuflC.png)


### The council of LLMs

- Everything downstream depends on graders/labels, so the scoring method is where the loop starts. The standard setup samples two frontier models and keeps the examples where they agre
    - That carries a quiet bias: strict agreement only retains examples where both models are aligned on the first pass, which are the easier ones
    - The hard examples, which are the most valuable for training, get discarded.
- A council of models, with protocols that resolve disagreement rather than throw it away, flips this. Each model generates a response with reasoning, sees the others' generations, and is asked to critique or defend
    - An arbitrator renders a verdict. Debate can surface correct answers on cases where no individual model succeeds at pass@1, although results depend heavily on the protocol
    - When it works, this provides a mechanism for generating training data that exceeds frontier-model first-attempt accuracy.
- Because so much downstream signal flows from these judgments, the council has to be calibrated against a human-annotated golden set before its verdicts drive anything. A miscalibrated judge corrupts the signal at the source, and that error cascades through every later stage.

### Failure mode mining and clustering

- With a calibrated council in hand, each cycle begins by finding where the current checkpoint is breaking.
    - We pull a stratified sample of representative traffic and run the council of judges over it to score the current checkpoint’s performance
    - Then group the failures into thematic clusters, either by handing failure cases to a strong LLM and asking what the inputs have in common, or by embedding and clustering at larger scales
    - The output is a set of failure hypotheses: concrete claims about input properties that correlate with failure
- A failure hypothesis isn't yet usable as a sampling dimension. To become one it needs two things:
    - a classifier (programmatic or LLM-based) that can label any example with the relevant value;
    - and empirical validation, meaning that when you stratify a held-out sample by the dimension, the model's accuracy actually varies across strata
- a dimension is only promoted into the sampler if it shows a measured accuracy gap across its values, and the size of that gap is correlated to its weight: bigger gap, higher priority.
- The distinction from conventional diversity sampling matters. The default approach samples for variety across language, topic, length, and channel, using inverse-frequency weights over hand-picked dimensions
    - beats random sampling, but variety doesn't guarantee coverage of where the model fails. A rare language might be hard, or it might be trivially easy; a common input pattern might be exactly where the current checkpoint is silently broken.

### Failure mode upsampling

- We map current coverage across the validated dimensions (for each region, roughly how much training data exists and how the current checkpoint performs there), then rebalance toward the regions that are underrepresented or where the model is weak
- Sampling blends three things.
    - The bulk comes from those failure regions, weighted by the size of the accuracy gap and preferring examples the model is uncertain on
    - A steady structural floor across always-on axes like language, channel, and length handles some baseline stratification and guards against blind spots in the judge.
    - And a smaller uniform-random share ensures we maintain full coverage of our production distribution.
- Coverage isn't the whole story, though. A perfectly diverse dataset can still be dominated by trivial cases the model already gets right
    - So upsampling doesn't target rarity alone; it targets the intersection of rarity and difficulty, meaning examples that sit in undercovered regions and that the model also finds hard

### Measuring complexity and scheduling a curriculum

- Diversity tells you what kinds of examples you have, complexity tells you which are particularly worth training on within those clusters.

![](https://pbs.twimg.com/media/HRj7wGDbgAATgRj.jpg)

- **Measuring complexity:** The default measure is pass@k with k = 5–10: sample k completions for an example, score each with the council verifier, and read complexity off the pass rate.
    - The fewer of the k attempts that succeed, the harder the example.
    - Combined with the coverage picture from the previous section, this is what lets upsampling target the genuine high-signal region, the intersection of undercovered and hard regions.
- **Where this matters most:** Under group-relative policy-gradient methods such as GRPO, the learning signal for a prompt comes from the spread of rewards across its sampled rollouts.
    - If every rollout for a prompt succeeds, or every one fails, the advantages are all zero.
    - The prompt contributes no gradient, and the compute spent rolling it out is wasted
- The prompts that actually move the policy are the ones in the intermediate band, where some rollouts succeed and some don't.
    - Pass@k is the measurement that locates that band.
    - Prompts with pass@k near 0 or near 1 yield little signal, and prompts in between are where advantages are nonzero.
- Scheduling by complexity therefore does two jobs in RL.
    - It keeps training concentrated on prompts inside the productive-advantage zone, and as the policy improves and easy prompts saturate toward pass@k ≈ 1, the curriculum advances into harder prompts that have just entered that zone.
    - The result is a frontier that keeps advantages flowing throughout training instead of collapsing as the model improves.
- While prompts with pass@k of 0 may be unlearnable for the current checkpoint under a binary group-relative reward, methods such as on-policy self-distillation (OPSD) can make these examples learnable by providing denser supervision from a privileged teacher

### Synthetic data for underrepresented failure modes

- Some regions of the input space can't be filled from real production data.
    - Either the traffic is genuinely sparse there, or the data exists but sits outside the subset we are permitted to train on.
    - Those constraints don't make the failure mode any less real, they just make it impossible to address with real collected data.
    - Synthetic generation allows us to close the gap.
    - Recent work similarly frames synthetic-data construction as dataset-level mechanism design over coverage, complexity, and quality
- a generator LLM produces new examples for an underfilled region
- Quality control is what separates useful synthetic data from drift, so every synthetic example passes three checks:
    - **Independent judge validation.** A different model or prompt verifies realism, dimension match, and label, so the generator never grades its own work.
    - **Per-example distribution check.** Each example is compared against real examples in the same region.
    - **Aggregate distribution check.** The full synthetic subset is checked for drift that individual examples wouldn't reveal.

### Closing the loop: iteration cycles

- Data curation and training form a continuous cycle. Each checkpoint changes where the model fails, so a round of mining should run against the exact checkpoint being evaluated.
- Each cycle has the same shape: Internal or shadow exposure → Mine failures from the current checkpoint → Construct a failure-informed dataset → Train on the new dataset → Evaluate against frozen benchmarks and regression suites → Update the internal candidate if accepted → repeat
    - Exposure can come from internal users, offline replays, or shadow traffic, the loop does not require serving the candidate checkpoint directly to production users. Evaluation is an iteration gate, and a checkpoint that does not clear that gate does not advance to broader testing.
- **Exploratory direction: behavior anchoring.** Repeated task-specific training may eventually degrade capabilities outside the target distribution. We are exploring how on-policy distillation from an earlier checkpoint on broader datasets could act as a behavioral anchor between cycles

### What we learned applying the loop

- We initially applied this approach internally to evidence-bound response verification: deciding whether a response contains a consequential claim unsupported by the available conversation history, policies, retrieved knowledge, metadata, or tool calls.
    - Initial task training improved evidence coverage but left systematic false positives.
    - Mining those errors from the current checkpoint and constructing targeted hard negatives and contrast pairs helped sharpen the decision boundary more effectively than adding broad or positive-heavy data.
- The application also reinforced the need for independent evaluation.
    - We observed runs where training reward continued to improve while performance on a frozen real-data benchmark regressed.
    - We therefore treated that benchmark as a gate for every intermediate checkpoint and re-mined failures after each accepted checkpoint, since each stage produced a different error distribution.

### Takeaways

- **Mine the checkpoint you are trying to improve.** Internal evaluation, offline replays, and shadow traffic can surface useful failures without requiring a production deployment.
- **Let measured failures shape the dataset.** Promote a sampling dimension only when it predicts an accuracy gap, then prioritize regions that are both undercovered and difficult.
- **Treat disagreement as signal.** Resolve contested labels with additional judgment rather than discarding the hardest examples.
- **Use synthetic data to fill coverage gaps.** Validate examples independently and check both per-example quality and aggregate drift.
- **Keep evaluation outside the flywheel.** Every candidate checkpoint should clear frozen real-data benchmarks before advancing to broader testing.
