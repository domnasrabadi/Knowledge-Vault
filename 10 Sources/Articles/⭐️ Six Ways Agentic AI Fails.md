---
type: article
status: raw
quality: 1
topics: [ai-agents, agent-evaluation, llm-risks, model-risk-validation]
source: https://agussudjianto.substack.com/p/six-ways-agentic-ai-fails
created: 2026-08-08
published: 2026-04-23
author: Agus Sudjianto
flashcards: none
updated: 2026-08-11
---

# Six Ways Agentic AI Fails

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!XODT!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7219ab5d-89f3-46f9-bf4f-7a6753004cac_1267x454.png" width="220" />
</div>

- The shift from generative AI to agentic AI changes what “wrong” means. A language model that hallucinates a date produces an incorrect sentence. An agent that hallucinates a capital ratio produces an incorrect regulatory filing. The error is the same at the model layer. The consequence is categorically different at the system layer, because the agent’s output feeds into a decision pipeline that was designed to trust it.
- Traditional model validation asks: *does the model produce accurate outputs?* Agentic validation must ask a broader question: *does the agent behave correctly across its full operational scope?*
- That scope includes not just the quality of the agent’s reasoning but also the correctness of its actions — which tools it calls, in what order, under what authority and with what degree of justified confidence.

### Two Kinds of Failure: Execution and Reasoning

- **Execution failures** occur in the agent’s interaction with the external world — the tools it calls, the policies it follows and the state it maintains across turns.
	- These failures may produce plausible-sounding output.
	- The text reads well. The actions behind it are wrong.
- **Reasoning failures** occur in the agent’s internal inference — the facts it asserts, the chains of logic it constructs and the confidence it assigns to its conclusions.
	- These failures produce output that is wrong in substance, even when the execution pathway was correct.
	- The agent called the right tools, followed the right workflow and then drew the wrong conclusion from the data it retrieved.
- The two categories are not always separable in practice.
	- A tool misuse (execution) can cause a hallucination (reasoning) when the wrong data is retrieved and then presented as fact.
	- A reasoning error can cascade into an execution failure when flawed analysis leads the agent to call an inappropriate tool.
- Execution failures require trace-level inspection — what did the agent *do*?
	- Reasoning failures require output-level verification — what did the agent *claim*?

![](https://substackcdn.com/image/fetch/$s_!XODT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7219ab5d-89f3-46f9-bf4f-7a6753004cac_1267x454.png)


#### FM-1: Factual Hallucination

- **Definition:** The agent asserts a fact that is not in the source material, or asserts a fact that contradicts it.
- This is the most insidious form of hallucination: the *near miss*. The answer is a real number from the real document, attached to the right model, for the wrong evaluation split
- **What makes it hard to detect:** The error is *locally plausible*. The number is real. The model is correct. Only the binding between the question and the value is wrong. Detection requires a ground-truth system that stores not just values but the full relational context in which each value is valid.

#### FM-2: Tool Misuse

- **Definition:** The agent calls the wrong tool, passes incorrect arguments or sequences tools in the wrong order.
- **What makes it hard to detect:** The final output looks reasonable. The agent talked about MDL-001 and fairness. It called tools. It produced a result. Every evaluation method that examines only the output text will mark this as acceptable. Only trace-level inspection — examining the sequence of tool calls against the expected action — reveals the failure.

#### FM-3: Policy Violation

- **Definition:** The agent performs an action that violates an organizational policy — either by doing something forbidden or by skipping a required authorization step.
- **What makes it hard to detect:** Policy violations require testing against rules that live outside the agent’s code. The agent’s behavior is a function of its prompt, its tools and its context. The policy is a function of the organization’s governance framework. Testing for policy violations requires encoding those rules in a form the test harness can check — not just verifying that the output is factually correct.

#### FM-4: Inconsistent Multi-Hop Reasoning

- **Definition:** The agent fails to chain information correctly across multiple tables, documents or reasoning steps.
- **What makes it hard to detect:** Single-hop evaluation cannot reveal multi-hop failure. If you only test questions that require one lookup, the agent will look competent. Multi-hop failure is exposed only by questions that *require* chaining, and those questions must be designed to distinguish “the agent got the right answer by luck” from “the agent followed the correct reasoning path.” This requires testing the *path*, not just the *destination*.

#### FM-5: Confidence Miscalibration

- **Definition:** The agent expresses a level of confidence that does not correspond to its actual accuracy.
- What it changes is the *actionability* of the agent’s output. If downstream systems or human reviewers use the confidence signal to decide how much scrutiny to apply, a uniformly overconfident agent will cause wrong answers to be accepted without review.
- **What makes it hard to detect:** Accuracy metrics cannot detect miscalibration. A model that is 70% accurate and reports 70% confidence on every answer is perfectly calibrated in aggregate but useless at the individual-prediction level. Detecting miscalibration requires *per-prediction* comparison of stated confidence against realized accuracy — typically through reliability diagrams, Expected Calibration Error (ECE) and Maximum Calibration Error (MCE). These require large enough test sets to populate confidence bins meaningfully.

#### FM-6: State Corruption Across Turns

- **Definition:** In multi-turn interactions, the agent’s memory or internal state degrades, causing it to forget, confuse or contradict information from earlier turns.
- **Why it matters in practice:** Agentic workflows are inherently multi-turn. A model validation agent that interviews a model developer collects information across many turns before synthesizing a finding. If facts asserted in turn 3 are forgotten by turn 15, the synthesis is built on incomplete information. Unlike a factual hallucination, where the agent asserts something wrong, state corruption causes the agent to *omit* something it once knew — a failure of absence rather than a failure of assertion.
- State corruption also enables *cross-turn contradiction*
- **What makes it hard to detect:** Single-turn testing cannot reveal state corruption. The agent may answer every individual question correctly in isolation. The failure emerges only in multi-turn sequences where earlier information must persist. Testing requires a *teach-delay-recall* protocol: introduce a fact, interpose distractor turns and then probe for recall. The delay length, the nature of the distractors and the similarity between taught and probed terms all affect whether the failure manifests.
