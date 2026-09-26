---
type: book
status: inbox
quality: 1
topics: []
source: private://read/01m2m2ac12h9k6w880rg0vf1n3
created: 2026-09-26
published: 2026-03-26
author: Hamel Husain
flashcards: none
updated: 2026-09-26
---

# The Revenge of the Data Scientist

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article1.be68295a7e40.png" width="220" />
</div>


### The Harness Is Data Science


### The Harness Is Data Science

- Years ago, practitioners spent hours examining data, checking label alignment, and designing metrics. Today, we build on “vibes,” ask the model if it did a good job, and grab off-the-shelf metric libraries without looking at the data.
- This shows up most around retrieval and evals. Without a data background, engineers fear what they don’t understand
- The rest of this post walks through five eval pitfalls I see repeatedly, and what a data scientist would do differently in each case.

### Generic Metrics


### Generic Metrics

- It is tempting to reach for an eval framework and use its metrics off the shelf. The problem: you have no idea what is actually broken
- These sound reasonable. They are also generic enough to be useless for diagnosing your application’s failures.
- A data scientist would not adopt metrics off the shelf. They would explore the data, explore the traces, ask “what is actually breaking here?”, and figure out the highest-value thing to start measuring. There are infinite things to measure. You have to form hypotheses and iterate.
- Annotating traces this way rolls up into a ranked count of failure modes: Failure mode Count Failed to transfer to human 8 Inappropriate tour rescheduling 7 Excessive confirmation requests 4 Misunderstood inquiry type 4 Claimed unavailable data access 3
- What does “looking at the data” mean in practice? It means reading traces. Code your own custom trace viewer so you can remove friction and customize the display for your domain’s quirks. Take notes on problems you find. Do error analysis: categorize failures, figure out what to prioritize, decide what to work on.
- Diagram: Generic scores vs. application-specific metrics Generic Scores — don’t do this Application Specific Metrics — do this Rouge Calendar Scheduling Failure Bleu Interrupted Conversation Flow Faithfulness Widget Rendering Issue Helpfulness Email recipient incorrect Tone Failure to Escalate To Human

### Unverified Judges


### Unverified Judges

- The second pitfall is unverified judges. A lot of teams use an LLM as a judge to figure out whether their AI is working. Most of the time, nobody has a good answer to “how do you trust the judge?”
- The default: ask an LLM to rate outputs on a scale and use the numbers. A data scientist would treat the judge like a classifier. You have a black box giving you a prediction. How do you trust it? Get human labels, partition the data into train/dev/test, and measure whether the classifier is trustworthy.
- Diagram: Treat the judge like a classifier — train / dev / test
    - **Train — ~20% of examples.** Select few-shot examples for your prompt from here.
    - **Dev — ~40% of examples.** Hill climb against evals.
    - **Test — ~40% of examples.** Do a final check against this to make sure you didn’t overfit.
- Footnote on the slide: the percentages are different from conventional ML because we aren’t “training” anything — we are just using data to inform the judge’s prompt.
- Source few-shot examples from your training set. Hill-climb your judge’s prompt against a dev set. Keep a test set aside to confirm you haven’t overfit. If you have done machine learning before, this is boring. But people are not doing it. Verifying classifiers has become a lost art in modern AI.
- Treat your judge like a classifier in how you report results, too. Everywhere I go I see accuracy reported. If a failure mode occurs 5% of the time, accuracy hides the system’s true performance. Use precision and recall.

### Bad Experimental Design


### Bad Experimental Design

- many dimensions to this. Here are two that come up most.
- The first is constructing test sets. Most teams generate synthetic data by prompting an LLM: “Give me 50 test queries.” They get generic, unrepresentative data. A data scientist would look at real production data first, use hypotheses to determine which dimensions matter, then generate synthetic examples along those dimensions.
- Synthetic data generation — three principles
    - **Use structured input for diversity.** Define key dimensions (e.g., Feature, Persona, Scenario) and use them as variables in your prompt.
    - **Seed your generation with real logs or traces** when possible. Then ask the model to explicitly inject changes, like a new constraint or a modified variable, to create realistic edge cases.
    - **Enforce output structure & filter.** Define a schema for the output. Generate many candidates, then filter to retain the highest-quality, challenging examples.
- Ground synthetic data in real logs or traces. Figure out what dimensions to vary. Inject edge cases. Base the synthetic data off real data.
- Try to use binary scores One LLM output can be routed two ways:
    - **Likert Scale Judge → “Score: 3/5”** — labelled on the slide “Don’t Do This!”
    - **Actionable evals** — a set of scoped binary checks, each returning pass or fail:
    - `is_polite` → Pass
    - `scheduling` → Fail
    - `human_handoff` → Pass
- The second is metric design. Teams bundle entire rubrics into a single LLM call and default to 1-5 Likert scales. A data scientist would reduce complexity, make each metric actionable, and tie it to a business outcome. Replace subjective scales with binary pass/fail on scoped criteria. Likert scales hide ambiguity and kick the can down the road on hard decisions about system performance.

### Bad Data and Labels


### Bad Data and Labels

- Data scientists don’t trust the data. They don’t trust the labels. They don’t trust anything. They are skeptical by training. AI engineers at large have not built this muscle yet.
- When it comes to labeling, most teams make it someone else’s problem. Labeling seems unglamorous, so it gets delegated to the dev team or outsourced. A data scientist would insist that domain experts label the data, stay skeptical of the labels, and look at the data.
- the phenomenon *criteria drift*: “users need criteria to grade outputs, but grading outputs helps users define criteria.” It adds that some criteria appear dependent on the specific LLM outputs observed, rather than being definable *a priori*.
- But labeling matters for a deeper reason than label quality. It is impossible to know what you want unless you look at the data. There is a concept called “criteria drift,” validated in a [paper by Shreya Shankar and colleagues](https://arxiv.org/abs/2404.12272): users need criteria to grade outputs, but grading outputs helps users define their criteria. People don’t know what they want until they see the LLM’s outputs. The labeling process itself surfaces what matters.

### Automating Too Much


### Automating Too Much

- The fifth pitfall is automating too much. All of this is human work. The temptation is to automate it away.
- LLMs can help wire things up, write the plumbing, generate boilerplate for evaluations. They cannot look at the data for you, for the exact reason we just discussed: you don’t know what you want until you see the outputs.

### Other Pitfalls


### Other Pitfalls

- • Misusing similarity scores • Asking the judge “is this helpful?” • Making annotators read raw JSON • Reporting uncalibrated scores without confidence intervals • Ignoring data & criteria drift • Overfitting judges to data • Not sampling data effectively • Dashboards with low signal • Logging traces and saying “that’s evals”

### The Mapping


### The Mapping

- If you zoom out, every pitfall above has the same root cause: missing a data science fundamental.
- • **Error analysis** — Read outputs, find patterns. *(EDA)* • **Metric design** — evals aligned to what matters. • **Validation** — Prove evaluators match human judgment. *(Model evaluation)* • **Test data** — Generate diverse inputs. *(Experimental design)* • **Monitoring** — Detect drift. *(Production ML)* • **Iteration** — Measure, improve, experiment. *(The scientific method)*
