---
type: article
status: raw
quality: 2
topics: [agent-evaluation, evaluation-metrics]
source: https://x.com/neural_avb/status/2031417353666441266/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-03-10
author: AVB
flashcards: none
updated: 2026-08-13
---

# How to Design Experiments to Evaluate Your Agentic Systems

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2015375309147611136/WKvfQ-oV.jpg" width="220" />
</div>

- Evaluation is not only about collecting logs and success metrics of the current system you have in place. It is also about validating your hypothesis and comparing your approach against alternative methods through frequent experiments.
- How can you design experiments? How do you pick eval metrics? How do you interpret your results?

## Step 1:

- Decide what you want to evaluate
- A good rule of thumb I follow is to treat each agent as a separate harness.
- Depending on your use-case, you may want to set up a system-level evaluation harness, or a module/unit-level harness.
- *Your first task is to make a decision -* *what are you evaluating?***
- Generally you can't evaluate an entire pipeline at once and expect actionable insights. There may be way too many moving variables!
- suggest you to ask yourself these questions:
    1. Where in the pipeline have I made the most egregious assumptions? *( the whole point of an experiment is to validate hypothesis/assumptions, so may as well start here) *
    2. What part of my pipeline happens EARLIEST in the the chain? *( the earlier things are in the pipeline, the more impactful they tend to be coz errors propagate downstream! So prioritize these first! ) *
    3. What is my goal here - what *vector* am I trying to *optimize*? *( I have an entire section for this one coming up)*

## Step 2:

- Decide your end goal
- When we run experiments, we always have a goal in mind. A hypothesis we want to test, or a suspicion we want to rest. What does success look like? What will you do with the information once you have it? It is best to have a clear hypothesis and a threshold for action.

## Step 3:

- Isolate the black box and your knobs
- You picked a module in Step 1 to test. Now it's time to isolate it from the rest of the system. You need a clean function where you shove your inputs in, and it spits the outputs out, without worrying about any internal plumbing.
- **Independent variables.** This is basically the "knobs" of your experiment. The **hyperparameters** (in a machine learning sense). These are the specific configuration parameters you are controlling from the outside to see how they affect the performance of the black box.
- Isolate your independent variables from the rest of your program. I will suggest to keep the number of independent variables to like maximum of 2 or 3 so you can study their effects afterwards before adding more variables! Examples:
    1. Suppose you just want to test quality of different LLMs. Put your module as a function and make it accept a parameter (the model name) as input.
    2. Suppose you want to test different system prompts. Pass the prompts as input.
    3. You want to test new tools, hide these tools behind a feature flag that you can toggle on or off.

## Step 4:

- Design your test-cases
- Your evaluation is only as good as your dataset. If you test on garbage, you'll optimize for garbage.
- Every test-case has 2 components: the input and the expected output. The most simple experiments can just be some kind of a CSV file containing literally those two columns as inputs.
- some examples:
    - production logs, that is the best place to begin.
    - should be able to find the exact inputs where your target module was invoked.
- If you don't have production logs, I encourage you to quit experimenting and set up your analytics first.
- Come back to the experiment later.
- If none of the above apply to you, your best shot is to either write test-cases yourself, or generate synthetic cases with an LLM. I encourage you to decide which route (or a combination) is best for your use-case.
- How does quality test-case data look like?
- important that your test-case have the following properties:
    - **Deduplicated and diverse:** Since we will be aggregating the performance across these test cases, it is super important for your test cases to be diverse. If you oversample a single subdomain, you stand the risk of biasing your entire experiment.
    - **Ground truth responses are preferred:** If you are logging the inputs of your production system in the logs, you are probably also logging outputs as well. Having access to this is handy coz in the minimum, it tells you how much your new solution is expected to *drift* from your current solution.

## Step 5:

- Design one or more evaluation metrics
- Next step: you need a way to score the system's output automatically. There are deterministic metrics and probabilistic metrics. Deterministic metrics are exact: did the output contain a specific string? Was the output a valid JSON? Was the length under 500 characters? Probabilistic metrics usually involve "LLM-as-a-judge", where you prompt a smarter model to grade the output on a scale of 1-5 for helpfulness, tone, or accuracy.
- You should use deterministic metrics wherever possible because they are cheaper, faster, and 100% reliable.
- **Examples of eval metrics:**
    - If you are evaluating a retrieval agent, use precision, recall, or IOU scores.
    - If you are evaluating a full response agent, use LLM-as-judge
    - If you are evaluating a task agent, evaluate tool call statistics
    - Most task agent also work in verifiable environments - meaning there is a clear way to distinguish if the work succeeded or not. Use this design!
    - For citation agents, you would often have system prompts that ask them to respond in a specific format. Use regex to find malformed formatting. This is also true for coding agents, or structured output generators.
    - **Whatever you do, always record atleast 3 additional things: total walltime, completion token usage, and total cost.**

![](https://pbs.twimg.com/media/HDEGZf9aMAIb2xV.jpg)

## Step 6:

- Draw graphs and plots *Visualizations are a window to your experiment's soul.*
