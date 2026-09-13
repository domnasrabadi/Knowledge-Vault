---
type: article
status: raw
quality: 1
topics: [llm-judges, agent-evaluation, ai-agents, ai-engineering]
source: https://x.com/josharosen/status/2097324183428444499/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-09-08
author: Josh Rosen
flashcards: none
updated: 2026-09-14
---

# LLM-as-Judge Architectures (inc. runtime judges)

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1418279052805353474/zn_g71-U.jpg" width="220" />
</div>

- Increasingly, we are seeing products put LLM judges directly inside the agent loop rather than using them as an offline tool.
    - The judge is no longer just evaluating the application. It’s participating in its control flow.
- Here are some common patterns for LLM-as-judge that you should consider adopting as part of your product’s application architecture.

### Start With Another Model

- This is the canonical LLM-as-judge approach.
    - One model does the work and another model judges it.
    - The judge gets some combination of the original request, the generated result, a rubric, reference material, and perhaps an expected answer. It returns a score, label, or explanation
- For high-volume applications, the economics could matter quite a bit. Because cost is more noticeable when you're running these evals constantly at application runtime, a specialized model that is designed to be cheap for this use case is a good option.

### Break the Judgment Apart

- A large amount of LLM judging boils down to one main question: was this output good?
    - An answer can be correct but incomplete.
    - It can be well written but unsupported by the source material.
    - Or an agent can arrive at the right result after taking actions it should never have taken.
- One upgrade to your judging architecture is to break the judgment into a set of smaller decisions.
    - One judge checks whether the answer addresses the request.
    - Another checks whether its claims are supported by the supplied evidence.
    - Another looks at whether the agent completed the required work.

### Compare Instead of Score

- Models are not always particularly good at telling you that something deserves a 7 rather than an 8.
    - They can be much better at deciding which of two things is better.
    - Pairwise judging is an approach that takes advantage of this. If you give the judge two outputs produced from the same input, you can ask which one better satisfies the criteria.
- This is commonly useful for application regression testing. However, the same pattern could move into runtime architectures.
    - An agent could generate several plans and use a judge to choose between them.
    - Alternatively, two agents could independently perform a piece of analysis and another model could compare the results.
    - In short, a proposed action could be compared against an alternative before the system commits to it and proceeds.

### Judge the Work Instead of the Answer

- The final result might look completely reasonable even though the agent retrieved the wrong documents or ignored an important source. It may have called the wrong tool or wandered through a series of unnecessary steps before getting lucky at the end.
- Application evaluation systems are already moving further into the trace.
    - [Phoenix](https://arize.com/docs/phoenix/?utm_source=chatgpt.com) has evaluators for retrieval relevance, tool selection, tool invocation, tool responses, and overall agent performance.
    - [LangSmith](https://docs.langchain.com/langsmith/evaluation-concepts?mode=ui&utm_source=chatgpt.com) can apply evaluators to individual runs as well as larger traces and threads.

### Use More Than One Judge

- One uncomfortable fact about LLM-as-judge is that the judge is still an LLM.
    - It can make mistakes for all the same reasons the model doing the work can.
    - One way to handle this is to stop treating a single judge as authoritative.
- Research on model evaluation has explored panels of judges, evaluator personas, voting, aggregation, and debate between evaluators
    - [MAJ-EVAL](https://aclanthology.org/2026.acl-long.790/?utm_source=chatgpt.com), for example, creates multiple evaluator agents representing different dimensions of the evaluation and lets them deliberate over the result.
- There is not a lot of evidence suggesting applications have adopted this approach in production yet.
    - But the mechanism is interesting above the model layer for a different reason.
    - Even if you don't care whether three judges vote 2–1 that an answer is good, you may care enormously that they disagree.
    - Agreement between independent judgments can increase confidence whereas disagreement could be a reason to retry with a stronger model, collect more evidence, or send the work to a human. You could imagine building a retry or escalation mechanism in your app based on this principle.

### Judge the Judge

- Once a judge can affect what happens in an application, its reliability matters a lot
    - Anthropic’s [Bloom](https://www.anthropic.com/research/bloom?subjects=claude&utm_source=chatgpt.com) provides another useful pattern.
        - Anthropic evaluated a collection of candidate judge models against human-labeled transcripts before choosing its judge.
        - The resulting evaluation pipeline also includes a meta-judge that looks across the broader evaluation results.
    - Application builders can use the simpler version of this idea today: periodically compare the judge against humans.
        - If a judgment controls something important, collect examples of those decisions and have people independently evaluate them.
        - Measure where the judge disagrees, and change the rubric, model, context, or decision boundary when the disagreement is unacceptable.

### Put Determinism Around the Judge

- If something can be checked deterministically, check it deterministically with tests or schema checks or even a database check. You could also consider writing a policy engine for this type of validation.
    - [OpenAI’s grader architecture](https://platform.openai.com/docs/api-reference/graders?api-mode=chat&utm_source=chatgpt.com) reflects this separation. It supports model-based graders alongside deterministic graders such as string checks and Python code, and multiple graders can be combined into a larger evaluation.
- The same pattern makes sense inside applications.
    - An LLM might judge whether the evidence is sufficient, whether a recommendation is well supported, or whether an agent appears to have completed the task.
    - Deterministic code can decide what combination of those judgments and other facts is required before the workflow moves forward.
- This sort of combined deterministic / non-deterministic logic is one of the biggest opportunities available at the application layer.

### Implication: Put the Judge in the Loop

- Many of the above patterns require that we move LLM judges inside the agent loops and put them in the critical path for our applications
    - It means that judgment informs control flow.
        - It can cause the application to continue, retry, route to another model, gather more information, or escalate to a person.
        - This is a much bigger role for LLM-as-judge. The judge is no longer just telling you whether the application worked yesterday. It is helping determine what the application does next.
    - It also means mistakes from the judge become application failures.
        - A judge that is slightly noisy in an offline eval may be annoying.
        - The same judge sitting in front of every important action can create loops, block good work, approve bad work, and add latency to every execution.
