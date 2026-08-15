---
type: article
status: raw
quality:
topics: [llm-evaluation, error-analysis]
source: https://x.com/annabellschfr/status/2085381643687047434/?s=12&rw_tt_thread=True
created: 2026-08-09
published: 2026-08-06
author: Annabell
flashcards: none
updated: 2026-08-13
---

# Scoping and curating eval datasets

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2011353913790787584/iPsZOGFe.jpg" width="220" />
</div>

- An eval dataset is a repeatable set of examples that represent the scope of your application, and that you use to measure and improve your system
- This guide focuses on the design work that happens before and while you create datasets and dataset items
- Dataset design is iterative.
    - A good starting point is a minimally complete dataset: about 15-30 rows that can run through your application, cover the most important input slices, and have an evaluator or review rubric.
    - Run that version early, fix the schema and evaluator, then expand into the gaps you see from those runs or from production input.
- Your application will very likely have more than one evaluation dataset. Datasets are often scoped to a specific part of the system or to one sub-step the agent takes.

### 1. Start with the goal of the dataset

- Before writing rows, define the smallest useful goal the dataset should support
- good early starting point for a dataset is looking at the most common examples end to end
- end-to-end datasets use the payload the application receives, while step-level datasets use the structured state a step sees in production
- If two jobs need different inputs, evaluators, or release decisions, split them. A stable regression dataset and an adversarial-input dataset can both be useful, but combining them without a clear split makes aggregate scores harder to interpret.

### 2. Inspect available sources

- inspect a small sample of the material you could use
- Start with three source types:
    - **Production traces:** show realistic usage, common paths, and observed failures. Scores, user feedback, tickets, and complaints are discovery signals for useful traces; they are not a separate source type.
    - **Existing assets:** old datasets, FAQs, policies, docs, support macros, CSVs, JSON files, and benchmarks can bootstrap known coverage quickly.
    - **Synthetic cases:** expert-written and AI-generated examples can fill gaps and give you an idea of what your application is expected to face.
- For each source, review input topics, input and output shapes, and failure modes

### 3. Choose the input distribution

- **Scenario type:** the main jobs, intents, routes, or task families
- **Difficulty or risk:** routine, ambiguous, hard, adversarial, or business-critical cases. Include more than happy paths, but do not make the first dataset all edge cases.
- **Dataset role:** why the row exists: typical case, known regression, observed failure, or synthetic gap-fill.
- For a support-routing dataset, the first version might use a simple scenario-by-difficulty matrix:

![](https://pbs.twimg.com/media/HPBmSWoWwAANxPH.jpg)

- the coverage plan that helps you interpret experiment results by slice.

### 4. Decide how evaluation will work

- Use [reference-based evaluation](https://langfuse.com/academy/evaluate#reference-based-vs-reference-free) when each item has a known target: a correct label, expected tool call, required fact, structured output, reference answer, or expected next action. This is the best fit for regression tests and CI gates because failures are easier to inspect
- Use [reference-free evaluation](https://langfuse.com/academy/evaluate#reference-based-vs-reference-free) when there is no stable expected output, but every item can be judged against the same rule or rubric

### 5. Design the item schema

- The [three dataset item fields](https://langfuse.com/academy/datasets#the-dataset-item) are flexible JSON. Here, define them as a concrete contract that your experiment runner, evaluators, and reviewers can all consume.
- Define:
    - input: the object you will pass into the system boundary
    - expectedOutput: only the reference data the evaluator or reviewer needs; omit it for deliberate reference-free evaluation
    - metadata: stable slice and provenance fields such as source, scenario type, difficulty, dataset role, and review status

### 6. Draft a first version

- For a minimally complete first version, choose enough rows to test the whole contract along your input distribution:
    - common scenarios that should work reliably
    - a few ambiguous or high-risk scenarios
    - known failures or regressions you want to prevent
    - synthetic gap fills only where production traces or existing assets do not cover the distribution

### How datasets evolve over time

- By [monitoring production](https://langfuse.com/academy/monitoring) and frequently reviewing data through structured [error analysis](https://langfuse.com/academy/monitoring/error-analysis), your datasets can evolve over time to represent the production scope of your system
- There are three useful expansion patterns:
    - **Production-mirroring**: add interesting cases from production no matter if good or bad, to expand the coverage of your dataset over time.
    - **Bad-trace expansion:** add a reviewed dataset item whenever you find a serious production failure. This works well once the system is live and you can continuously mine traces.
    - **Purpose-specific datasets:** build separate datasets for stable regression, adversarial inputs, single-step evaluations.
