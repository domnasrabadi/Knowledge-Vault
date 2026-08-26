---
type: article
status: raw
quality: 1
topics: [llm-evaluation, evaluation-metrics, error-analysis]
source: private://read/01m0m6et9rttgx89yckkyf3fy4
created: 2026-08-23
published: 2026-08-19
author: Langfuse Academy
flashcards: none
updated: 2026-08-27
---

# Choosing what to evaluate

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article4.6bc1851654a0.png" width="220" />
</div>


### Three kinds of metrics

| Role | Question it answers | Typical source |
| --- | --- | --- |
| **Goal metrics** | Is quality improving on the things we are building for? | Error analysis, product goals |
| **Guardrails** | Did we regress on something that must never break? | Requirements, compliance, past incidents |
| **Operational metrics** | What does it cost, and how many requests per hour? | Tracing, for free |

- A good setup uses a mix of the three together
    - Goal metrics are the ones you actively push up, guardrails catch the failures you can't afford even once, and operational metrics give you more insight into the system
- **The fewer metrics you can keep without feeling like you're missing visibility, the better:**
    - every metric is an extra evaluator/dataset to run and maintain
    - when everything is important, nothing is
- Your north star changes over time.
    - Even if you have your evals set up, it's important to keep a recurring process of looking at a sample of your traces manually.
    - You'll discover failures your evals didn't cover yet, or notice that some metrics became less important over time.

### Where candidate metrics come from

- come from two places:
    - **1. Observed failures**
        - Most of your metrics will come from you going through your traces, discovering how your agent behaves and how you'd like it to behave instead.
        - There's a structured process for translating what you see into metrics to evaluate, called [Error analysis](https://langfuse.com/academy/monitoring/error-analysis).
        - This should, in most cases, be your default way of deciding on metrics: **write evaluators for errors you discover; don't focus on imaginary ones**
    - **2. Goals and hard constraints**
        - There are requirements you know you need to monitor before seeing your agent in action.
        - Compliance rules, safety requirements, and format contracts get an evaluator from day one, even if you have never seen them break. These are often guardrail metrics.
        - **Metric catalogs are good for exploration, but tailor them to your product**

### Which candidates deserve a metric?

- Not all criteria candidates should be tracked.
- **One-time fix or generalization problem?**
    - Only keep a metric when a simple prompt change doesn't solve your problem, and you need to continuously track a failure mode over time
    - Likely one time fixes
        - The output isn't valid JSON
        - The reply uses the wrong date format
        - The response uses markdown on a plain-text channel
        - The bot doesn't disclose it's an AI assistant
    - Generalization problems
        - whether the answer is supported by the retrieved context
        - whether the right context was fetched to answer the question
        - whether the response actually answered the user's request
        - whether the agent picked the right tool and passed the right arguments
- **Tie every metric to a decision**
    - For each metric candidate, determine what the action changes when the metric moves: block the deploy, roll back the prompt, open an investigation. If no action changes, the metric would be noise, and should not be tracked
    - **Conversation length is not specific enough**
        - Conversation length rises both when users are engaged and when they are stuck, so the number moves for unrelated reasons and you can't act on it alone

### Starting from zero

- Before you have your metric set, you'll need to determine your agent's failure modes. This will help you derive metrics.
    - To start, bootstrap with two generic [scores](https://langfuse.com/docs/evaluation/scores/overview): a free-text note describing what happened and what seems wrong, and an overall pass/fail.
    - Read 30 to 50 traces with only those, cluster the notes into named failure categories, and then create one boolean score per category.
    - This process is called [error analysis](https://langfuse.com/academy/monitoring/error-analysis).

### Keeping the set alive

- **Retire metrics that stopped catching things.** With the exception of guardrail checks, a score that sits at 100% for months carries no information and you can most likely drop it
- **Watch the metrics you optimize.** Goodhart's law applies here: when you tune prompts against certain metrics, you can overfit at some point. It's important to [re-validate against new human labels](https://langfuse.com/guides/llm-as-a-judge-calibration-skill) from time to time
