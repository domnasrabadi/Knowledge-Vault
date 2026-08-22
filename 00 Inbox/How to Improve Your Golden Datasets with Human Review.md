---
type: article
status: inbox
quality: 
topics: []
source: https://www.braintrust.dev/blog/human-review-golden-datasets
created: 2026-08-22
published: 2026-05-21
author: Braintrust Team
flashcards: none
updated: 2026-08-22
---

# How to improve your golden datasets with human review

<div align="center">
  <img src="https://www.braintrust.dev/og?title=How+to+improve+your+golden+datasets+with+human+review&description=Turn+production+traces+into+golden+datasets+by+adding+human+review+to+your+eval+workflow%2C+then+use+that+ground+truth+to+improve+scorers+over+time.&template=blog&v=3" width="220" />
</div>

- When you're building an eval workflow, it's easy to forget that human expertise is one of the most important inputs. If you don't have some validation of what good looks like for your AI product, then it's impossible to judge whether the quality of what you're building improved or regressed, because you have nothing authoritative to compare outputs against.
- The goal of adding human review to your eval process is to turn your production traces into [golden datasets](https://www.braintrust.dev/docs/annotate/datasets) that are updated over time, and that can help tune your scorers as your data changes.
- At any real production scale, you can't get to the labeling step by browsing every trace yourself. The traces need to be categorized first, by failure mode, intent, sentiment, and so on, so a reviewer can focus on patterns instead of individual events.
- When writing `expected` values, you'll need to:
    - Include the full response the model should produce, or the specific value you want returned.
    - Make sure format, tone, schema, citations, and safety behavior align with what your app expects in production.
    - Use deterministic targets, like "return JSON with keys X/Y/Z" which is easier to score than "a helpful answer."
    - If a single trace exercises multiple behaviors, consider splitting into multiple dataset rows so each has a crisp `expected`.
- The workflow of applying human review to your eval process should follow a pattern that takes traces, puts them into a dataset, and then tests against the `expected` value from the human review.
- The quality bar for human reviewers should be high. If you can't confidently write the `expected` from available sources, it's better to consult additional subject matter experts rather than guessing
- If there are multiple outputs that could be "right," or if the ground truth is complex enough to warrant different correct outputs, you may need to narrow the task and make it more specific, or encode acceptable variance in your scorer, like a [rubric-based judge](https://www.braintrust.dev/docs/evaluate/llm-as-a-judge).
- Pick field types that match the judgment you need:
    - **Pass/fail** for the fastest decisions and cleanest metrics (for example, `is_correct`, `needs_fix`).
    - **Categorical** fields when you want a consistent taxonomy (for example, `failure_type = hallucination | retrieval_miss | tool_misuse | policy | formatting`).
    - **Continuous sliders** for subjective dimensions (for example, `helpfulness`, `tone`, or `groundedness` on a 1 to 5 scale).
    - **Freeform text** fields for `notes` or rationale.
- It's best to keep the rubric short at first, and only expand once reviewers are consistent, since long rubrics reduce throughput and increase inconsistency. To make the rubric usable in practice, add short definitions and examples directly in the field descriptions (what "good" and "bad" look like), and ensure each field maps to an action
- After traces have been reviewed initially through these queues, treat human review scores as the primary lever for curation
- From the filtered set, add these "promoted" traces or spans to a golden dataset of durable test cases. Once promoted, run experiments against this dataset after changes, continuously add new failures, periodically prune duplicates and stale cases, and gradually convert recurring human review patterns into automated scorers so human effort stays focused on the ambiguous and novel.
- Pairing custom trace views with human review lets you expose annotation affordances that a structured rubric can't express. Reviewers can apply corrections, labels, and notes directly from the interface, with those annotations written back to span metadata as queryable signals for filtering logs, curating datasets, triggering [online scorers](https://www.braintrust.dev/docs/evaluate/score-online), and regression testing
- Once you've set up human review and have enough results that meet the `expected` value, you can turn this human-reviewed ground truth into scalable, automated evaluation.
- For objective checks, this often starts with heuristic scorers (exact match, regex, diffs, and schema validation) that catch clear regressions cheaply and deterministically. For more subjective dimensions you can introduce [LLM-as-judge scorers](https://www.braintrust.dev/docs/evaluate/llm-as-a-judge) that follow the same rubric language your reviewers use. Over time, it becomes especially valuable to track judge and human alignment and calibrate prompts or thresholds when they drift, which will help keep automated scoring honest as your product and data evolve.
- As the dataset grows with real labeled failures, your scorers become more meaningful and regressions become easier to catch. Reviewed production failures become test cases, scorers turn those cases into metrics, and experiments and CI runs tell you whether a change improved things or broke something.
- Over time, human review moves from being the primary evaluation mechanism to being a source of high-quality training signal applied to datasets and scorers that are being automatically generated by an existing eval workflow.
