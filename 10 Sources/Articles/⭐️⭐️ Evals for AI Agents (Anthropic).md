---
type: article
status: raw
quality: 2
topics: [agent-evaluation, llm-evaluation]
source: ""
created: 2026-01-10
published: 2026-01-09
author: anthropic.com
flashcards: none
updated: 2026-02-14
---

# Demystifying evals for AI agents

<div align="center">
  <img src="https://cdn.sanity.io/images/4zrzovbb/website/412be842c5c6bae6b4bcd515c191b0aa5015e05f-2400x1260.png" width="220" />
</div>

Source: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

Exported at: `2026-01-10T05:08:02Z`

- Good evaluations help teams ship AI agents more confidently.
- Evals make problems and behavioral changes visible before they affect users, and their value compounds over the lifecycle of an agent.

### The structure of an evaluation

- An **evaluation** (“eval”) is a test for an AI system: give an AI an input, then apply grading logic to its output to measure success.
- we focus on **automated evals** that can be run during development without real users.
- **Single-turn evaluations** are straightforward: a prompt, a response, and grading logic. For earlier LLMs, single-turn, non-agentic evals were the main evaluation method.
- **multi-turn evaluations** have become increasingly common.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fbd42e7b2f3e9bb5218142796d3ede4816588dec0-4584x2834.png&w=3840&q=75)

- **Agent evaluations** are even more complex. Agents use tools across many turns, modifying state in the environment and adapting as they go—which means mistakes can propagate and compound.
- When building agent evaluations, we use the following definitions: 
	- A **task** (a.k.a **problem** or **test case**) is a single test with defined inputs and success criteria. 
	- Each attempt at a task is a **trial**. Because model outputs vary between runs, we run multiple trials to produce more consistent results. 
	- A **grader** is logic that scores some aspect of the agent’s performance. A task can have multiple graders, each containing multiple assertions (sometimes called **checks**)**.** 
	- A **transcript** (also called a **trace** or **trajectory**) is the complete record of a trial, including outputs, tool calls, reasoning, intermediate results, and any other interactions. For the Anthropic API, this is the full messages array at the end of an eval run - containing all the calls to the API and all of the returned responses during the evaluation. 
	- The **outcome** is the final state in the environment at the end of the trial. A flight-booking agent might say “Your flight has been booked” at the end of the transcript, but the outcome is whether a reservation exists in the environment’s SQL database. 
	- An **evaluation harness** is the infrastructure that runs evals end-to-end. It provides instructions and tools, runs tasks concurrently, records all the steps, grades outputs, and aggregates results. •
	- an **agent harness** (or **scaffold**) is the system that enables a model to act as an agent: it processes inputs, orchestrates tool calls, and returns results. When we evaluate “an agent,” we’re evaluating the harness *and* the model working together. For example, [Claude Code](https://claude.com/product/claude-code) is a flexible agent harness, and we used its core primitives through the [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) to build our [long-running agent harness](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents). 
	- An **evaluation suite** is a collection of tasks designed to measure specific capabilities or behaviors. Tasks in a suite typically share a broad goal. For instance, a customer support eval suite might test refunds, cancellations, and escalations.

### Why build evaluations?


![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0205b36f9639fc27f2f6566f73cb56b06f59d555-4584x2580.png&w=3840&q=75)

- When teams first start building agents, they can get surprisingly far through a combination of manual testing, [dogfooding](https://en.wikipedia.org/wiki/Eating_your_own_dog_food), and intuition.
- But after the early prototyping stages, once an agent is in production and has started scaling, building without evals starts to break down.
- breaking point often comes when users report the agent feels worse after changes, and the team is ‘flying blind’ with no way to verify except to guess and check. Absent evals, debugging is reactive: wait for complaints, reproduce manually, fix the bug, and hope nothing else regressed.
- Claude Code started with fast iteration based on feedback from Anthropic employees and external users. Later, we added evals—first for narrow areas like concision and file edits, and then for more complex behaviors like over-engineering. These evals helped identify issues, guide improvements, and focus research-product collaborations. Combined with production monitoring, A/B tests, user research, and more, evals provide signals to continue improving Claude Code as it scales.
- Writing evals is useful at any stage in the agent lifecycle. Early on, evals force product teams to specify what success means for the agent, while later they help uphold a consistent quality bar.
- Some teams create evals at the start of development; others add them once at scale when evals become a bottleneck for improving the agent. Evals are especially useful at the start of agent development to explicitly encode expected behavior.
- Two engineers reading the same initial spec could come away with different interpretations on how the AI should handle edge cases. An eval suite resolves this ambiguity. Regardless of when they’re created, evals help accelerate development.
- Evals also shape how quickly you can adopt new models.
- Once evals exist, you get baselines and regression tests for free: latency, token usage, cost per task, and error rates can be tracked on a static bank of tasks. Evals can also become the highest-bandwidth communication channel between product and research teams, defining metrics researchers can optimize against.

### How to evaluate AI agents

- You don’t need to invent an evaluation from scratch. The sections below describe proven techniques for several agent types. Use these methods as a foundation, then extend them to your domain.

#### Types of graders for agents

- Agent evaluations typically combine three types of graders: code-based, model-based, and human.
- Code based graders

| **Methods**                                                                                                                                                                                                                                                                               | **Strengths**                                                                                                   | **Weaknesses**                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| • String match checks (exact, regex, fuzzy, etc)  <br>• Binary tests (fail-to-pass, pass-to-pass)  <br>• Static analysis (lint, type, security)  <br>• Outcome verification  <br>• Tool calls verification (tools used, parameters)  <br>• Transcript analysis (turns taken, token usage) | • Fast  <br>• Cheap  <br>• Objective  <br>• Reproducible  <br>• Easy to debug  <br>• Verify specific conditions | • Brittle to valid variations that don’t match expected patterns exactly  <br>• Lacking in nuance  <br>• Limited for evaluating some more subjective tasks |
|                                                                                                                                                                                                                                                                                           |                                                                                                                 |                                                                                                                                                            |
- Model based graders

| **Methods**                                                                                                                                 | **Strengths**                                                                                            | **Weaknesses**                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| - Rubric-based scoring<br>- Natural language assertions<br>- Pairwise comparison<br>- Reference-based evaluation<br>- Multi-judge consensus | - Flexible<br>- Scalable<br>- Captures nuance<br>- Handles open-ended tasks<br>- Handles freeform output | - Non-deterministic<br>- More expensive than code<br>- Requires calibration with human graders for accuracy |
|                                                                                                                                             |                                                                                                          |                                                                                                             |

- Human graders

| **Methods**                                                                                                      | **Strengths**                                                                                        | **Weaknesses**                                                             |
| ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| - SME review<br>- Crowdsourced judgment<br>- Spot-check sampling<br>- A/B testing<br>- Inter-annotator agreement | - Gold standard quality<br>- Matches expert user judgment<br>- Used to calibrate model-based graders | - Expensive<br>- Slow<br>- Often requires access to human experts at scale |

- For each task, scoring can be: 
	- weighted (combined grader scores must hit a threshold), 
	- binary (all graders must pass), 
	- or a hybrid.

#### Capability vs. regression evals

- **Capability or “quality” evals** ask “what can this agent do well?” They should start at a low pass rate, targeting tasks the agent struggles with and giving teams a hill to climb.
- **Regression evals** ask “does the agent still handle all the tasks it used to?” and should have a nearly 100% pass rate. They protect against backsliding, as a decline in score signals that something is broken and needs to be improved. As teams hill-climb on capability evals, it’s important to also run regression evals to make sure changes don’t cause issues elsewhere.
- After an agent is launched and optimized, capability evals with high pass rates can “graduate” to become a regression suite that is run continuously to catch any drift.

#### Evaluating coding agents

- Effective evals for modern coding agents usually rely on well-specified tasks, stable test environments, and thorough tests for the generated code.
- Deterministic graders are natural for coding agents because software is generally straightforward to evaluate: Does the code run and do the tests pass? Two widely-used coding agent benchmarks, [SWE-bench Verified](https://www.swebench.com/SWE-bench/) and [Terminal-Bench](https://www.tbench.ai/), follow this approach.
- Once you have a set of pass-or-fail tests for validating the key *outcomes* of a coding task, it’s often useful to also grade the transcript*.* For instance, heuristics-based code quality rules can evaluate the generated code based on more than passing tests, and model-based graders with clear rubrics can assess behaviors like how the agent calls tools or interacts with the user.

#### Evaluating conversational agents

- Unlike traditional chatbots, they maintain state, use tools, and take actions mid-conversation. While coding and research agents can also involve many turns of interaction with the user, conversational agents present a distinct challenge: the quality of the interaction itself is part of what you're evaluating.
- Effective evals for conversational agents usually rely on verifiable end-state outcomes and rubrics that capture both task completion and interaction quality. Unlike most other evals, they often require a second LLM to simulate the user.
- Success for conversational agents can be multidimensional: is the ticket resolved (state check), did it finish in <10 turns (transcript constraint), and was the tone appropriate (LLM rubric)? Two benchmarks that incorporate multidimensionality are [𝜏-Bench](https://arxiv.org/abs/2406.12045) and its successor, [τ2-Bench](https://arxiv.org/abs/2506.07982). These simulate multi-turn interactions across domains like retail support and airline booking, where one model plays a user persona while the agent navigates realistic scenarios.
- In practice, conversational agent evaluations typically use model-based graders to assess both communication quality and goal completion, because many tasks—like answering a question—may have multiple “correct” solutions.

#### Evaluating research agents

- **Research agents** gather, synthesize, and analyze information, then produce output like an answer or report. Unlike coding agents where unit tests provide binary pass/fail signals, research quality can only be judged relative to the task. What counts as “comprehensive,” “well-sourced,” or even “correct” depends on context: a market scan, due diligence for an acquisition, and a scientific report each require different standards.
- Research evals face unique challenges: experts may disagree on whether a synthesis is comprehensive, ground truth shifts as reference content changes constantly, and longer, more open-ended outputs create more room for mistakes.
- One strategy to build research agent evals is to combine grader types. Groundedness checks verify that claims are supported by retrieved sources, coverage checks define key facts a good answer must include, and source quality checks confirm the consulted sources are authoritative, rather than simply the first retrieved.
- For tasks with objectively correct answers (“What was Company X’s Q3 revenue?”), exact match works.
- An LLM can flag unsupported claims and gaps in coverage, but also verify the open-ended synthesis for coherence and completeness.
- Given the subjective nature of research quality, LLM-based rubrics should be frequently calibrated against expert human judgment to grade these agents effectively.

#### How to think about non-determinism in evaluations for agents

- Regardless of agent type, agent behavior varies between runs, which makes evaluation results harder to interpret than they first appear. Each task has its own success rate—maybe 90% on one task, 50% on another—and a task that passed on one eval run might fail on the next.
- Sometimes, what we want to measure is how *often* (what proportion of the trials) an agent succeeds for a task.
- Two metrics help capture this nuance:
- [**pass@k**](https://proceedings.neurips.cc/paper/2019/file/7298332f04ac004a0ca44cc69ecf6f6b-Paper.pdf) measures the likelihood that an agent gets at least one correct solution in *k* attempts. As k increases, pass@k score rises - more ‘shots on goal’ means higher odds of at least 1 success. A score of 50% pass@1 means that a model succeeds at half the tasks in the eval on its first try. In coding, we’re often most interested in the agent finding the solution on the first try—pass@1. In other cases, proposing many solutions is valid as long as one works.
- [**pass^k**](https://arxiv.org/abs/2406.12045) measures the probability that *all k* trials succeed. As *k* increases, pass^k falls since demanding consistency across more trials is a harder bar to clear. If your agent has a 75% per-trial success rate and you run 3 trials, the probability of passing all three is (0.75)³ ≈ 42%. This metric especially matters for customer-facing agents where users expect reliable behavior every time.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F3ddac5be07a0773922ec9df06afec55922f8194a-4584x2580.png&w=3840&q=75)


### Going from zero to one: a roadmap to great evals for agents

- Think of this as a roadmap for eval-driven agent development: define success early, measure it clearly, and iterate continuously.

#### Collect tasks for the initial eval dataset

- Step 0. Start early
	- We see teams delay building evals because they think they need hundreds of tasks. In reality, 20-50 simple tasks drawn from real failures is a great start.
	- More mature agents may need larger, more difficult evals to detect smaller effects, but it’s best to take the 80/20 approach in the beginning.
	- Evals get harder to build the longer you wait. Early on, product requirements naturally translate into test cases. Wait too long and you're reverse-engineering success criteria from a live system.
- Step 1. Start with what you already test manually
	- Begin with the manual checks you run during development—the behaviors you verify before each release and common tasks end users try.
	- Converting user-reported failures into test cases ensures your suite reflects actual usage; prioritizing by user impact helps you invest effort where it counts.
- Step 2: Write unambiguous tasks with reference solutions
	- Getting task quality right is harder than it seems. A good task is one where two domain experts would independently reach the same pass/fail verdict. Could they pass the task themselves? If not, the task needs refinement.
	- Ambiguity in task specifications becomes noise in metrics. The same applies to criteria for model-based graders: vague rubrics produce inconsistent judgments.
	- Each task should be passable by an agent that follows instructions correctly. This can be subtle.
	- Everything the grader checks should be clear from the task description; agents shouldn’t fail due to ambiguous specs.
	- .For each task, it’s useful to create a reference solution: a known-working output that passes all graders. This proves that the task is solvable and verifies graders are correctly configured.
- Step 3: Build balanced problem sets
	- Test both the cases where a behavior *should* occur and where it *shouldn't*. One-sided evals create one-sided optimization.
	- Try to avoid [class-imbalanced](https://developers.google.com/machine-learning/crash-course/overfitting/imbalanced-datasets) evals.
	- We learned this firsthand when building evals for web search in [Claude.ai](http://claude.ai/redirect/website.v1.9dfa5f1b-a70d-42f1-b8a9-f3cb25dc1101). The challenge was preventing the model from searching when it shouldn’t, while preserving its ability to do extensive research when appropriate.
	- The team built evals covering both directions: queries where the model should search (like finding the weather) and queries where it should answer from existing knowledge (like “who founded Apple?”).
	- Striking the right balance between undertriggering (not searching when it should) or overtriggering (searching when it shouldn’t) was difficult, and took many rounds of refinements to both the prompts and the eval. As more example problems come up, we continue to add to evals to improve our coverage.

#### Design the eval harness and graders

- Step 4: Build a robust eval harness with a stable environment
	- essential that the agent in the eval functions roughly the same as the agent used in production, and the environment itself doesn’t introduce further noise.
	- Each trial should be “isolated” by starting from a clean environment.
- Step 5: Design graders thoughtfully
	- great eval design involves choosing the best graders for the agent and the tasks. We recommend choosing deterministic graders where possible, LLM graders where necessary or for additional flexibility, and using human graders judiciously for additional validation.
	- There is a common instinct to check that agents followed very specific steps like a sequence of tool calls in the right order. We’ve found this approach too rigid and results in overly brittle tests, as agents regularly find valid approaches that eval designers didn’t anticipate. So as not to unnecessarily punish creativity, it’s often better to grade what the agent produced, not the path it took.
	- For tasks with multiple components, build in partial credit**.** A support agent that correctly identifies the problem and verifies the customer but fails to process a refund is meaningfully better than one that fails immediately. It’s important to represent this continuum of success in results.
	- Model grading often takes careful iteration to validate accuracy. LLM-as-judge graders should be closely calibrated with human experts to gain confidence that there is little divergence between the human grading and model grading.
	- It can also help to create clear, structured rubrics to grade each dimension of a task, and then grade each dimension with an isolated LLM-as-judge rather than using one to grade all dimensions.
	- Once the system is robust, it’s sufficient to use human review only occasionally.
	- Make your graders resistant to bypasses or hacks. The agent shouldn’t be able to easily “cheat” the eval. Tasks and graders should be designed so that passing genuinely requires solving the problem rather than exploiting unintended loopholes.

#### Maintain and use the eval long-term

- Step 6: Check the transcripts
	- You won't know if your graders are working well unless you read the transcripts and grades from many trials.
	- At Anthropic, we invested in tooling for viewing eval transcripts and we regularly take the time to read them. When a task fails, the transcript tells you whether the agent made a genuine mistake or whether your graders rejected a valid solution. It also often surfaces key details about agent and eval behavior.
	- Failures should seem fair: it’s clear what the agent got wrong and why.
	- When scores don’t climb, we need confidence that it’s due to agent performance and not the eval.
	- Reading transcripts is how you verify that your eval is measuring what actually matters, and is a critical skill for agent development.
- Step 7: Monitor for capability eval saturation
	- An eval at 100% tracks regressions but provides no signal for improvement. **Eval saturation** occurs when an agent passes all of the solvable tasks, leaving no room for improvement.
	- As a rule, we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts.
- Step 8: Keep evaluation suites healthy long-term through open contribution and maintenance
	- An eval suite is a living artifact which needs ongoing attention and clear ownership to remain useful.
	- At Anthropic, we experimented with various approaches to eval maintenance.
	- What proved most effective was establishing dedicated evals teams to own the core infrastructure, while domain experts and product teams contribute most eval tasks and run the evaluations themselves.
	- For AI product teams, owning and iterating on evaluations should be as routine as maintaining unit tests. Teams can waste weeks on AI features that “work” in early testing but fail to meet unstated expectations that a well-designed eval would have surfaced early.
- We recommend practicing eval-driven development
	- build evals to define planned capabilities before agents can fulfill them, then iterate until the agent performs well.
	- Capability evals that start at a low pass rate make this visible.
	- The people closest to product requirements and users are best positioned to define success.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0db40cc0e14402222a179fc6297b9c8818e97c8a-4584x2580.png&w=3840&q=75)


### How evals fit with other methods for a holistic understanding of agents

- Automated evaluations can be run against an agent in thousands of tasks without deploying to production or affecting real users.
- A complete picture includes production monitoring, user feedback, A/B testing, manual transcript review, and systematic human evaluation.
- an overview of approaches for measuring AI Agents performance

|Method|Pros|Cons|
|---|---|---|
|**Automated evals  <br>**_Running tests programmatically without real users_|- Faster iteration<br>- Fully reproducible<br>- No user impact<br>- Can run on every commit<br>- Tests scenarios at scale without requiring a prod deployment|- Requires more upfront investment to build<br>- Requires ongoing maintenance as product and model evolves to avoid drift<br>- Can create false confidence if it doesn’t match real usage patterns|
|**Production monitoring  <br>**_Tracking metrics and errors in live systems_|- Reveals real user behavior at scale<br>- Catches issues that synthetic evals miss<br>- Provides ground truth on how agents actually perform|- Reactive, problems reach users before you know about them<br>- Signals can be noisy<br>- Requires investment in instrumentation<br>- Lacks ground truth for grading|
|**A/B testing  <br>**_Comparing variants with real user traffic_|- Measures actual user outcomes (retention, task completion)<br>- Controls for confounds<br>- Scalable and systematic|- Slow, days or weeks to reach significance and requires sufficient traffic<br>- Only tests changes you deploy<br>- Less signal on the underlying “why” for changes in metrics without being able to thoroughly review the transcripts|
|**User feedback  <br>**_Explicit signals like thumbs-down or bug reports_|- Surfaces problems you didn't anticipate<br>- Comes with real examples from actual human users<br>- The feedback often correlates with product goals|- Sparse and self-selected<br>- Skews toward severe issues<br>- Users rarely explain _why_ something failed<br>- Not automated<br>- Relying primarily on users to catch issues can have negative user impact|
|**Manual transcript review  <br>**_Humans reading through agent conversations_|- Builds intuition for failure modes<br>- Catches subtle quality issues automated checks miss<br>- Helps calibrate what "good" looks like and grasp details|- Time-intensive<br>- Doesn't scale<br>- coverage is inconsistent<br>- Reviewer fatigue or different reviewers can affect the signal quality<br>- Typically only gives qualitative signal rather than clear quantitative grading|
|**Systematic human studies  <br>**_Structured grading of agent outputs by trained raters_|- Gold-standard quality judgements from multiple human raters<br>- Handles subjective or ambiguous tasks<br>- Provides signal for improving model-based graders|- Relatively expensive and slow turnaround<br>- Hard to run frequently<br>- Inter-rater disagreement requires reconciliation<br>- Complex domains (legal, finance, healthcare) require human experts to conduct studies|

- These methods map to different stages of agent development.
- Automated evals are especially useful pre-launch and in CI/CD, running on each agent change and model upgrade as the first line of defense against quality problems.
- Production monitoring kicks in post-launch to detect distribution drift and unanticipated real-world failures.
- A/B testing validates significant changes once you have sufficient traffic.
- User feedback and transcript review are ongoing practices to fill the gaps - triage feedback constantly, sample transcripts to read weekly, and dig deeper as needed.
- Reserve systematic human studies for calibrating LLM graders or evaluating subjective outputs where human consensus serves as the reference standard.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fb77b8dbb7c2e57f063fbc8a087a853d5809b74b0-4584x2580.png&w=3840&q=75)

- Like the [Swiss Cheese Model](https://en.wikipedia.org/wiki/Swiss_cheese_model) from safety engineering, no single evaluation layer catches every issue. With multiple methods combined, failures that slip through one layer are caught by another.
- The most effective teams combine these methods - automated evals for fast iteration, production monitoring for ground truth, and periodic human review for calibration.

### Conclusion

- Teams without evals get bogged down in reactive loops - fixing one failure, creating another, unable to distinguish real regressions from noise. Teams that invest early find the opposite: development accelerates as failures become test cases, test cases prevent regressions, and metrics replace guesswork. Evals give the whole team a clear hill to climb, turning “the agent feels worse” into something actionable. The value compounds, but only if you treat evals as a core component, not an afterthought.
