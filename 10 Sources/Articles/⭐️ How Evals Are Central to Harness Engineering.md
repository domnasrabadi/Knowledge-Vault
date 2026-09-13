---
type: article
status: raw
quality: 1
topics: [agent-harnesses, agent-evaluation, error-analysis]
source: https://hugobowne.substack.com/p/how-evals-are-central-to-harness
created: 2026-09-13
published: 2026-09-01
author: Antaripa Saha, Hamel Husain, Hugo Bowne-Anderson
flashcards: none
updated: 2026-09-14
---

# How Evals Are Central to Harness Engineering

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!P6hF!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dc3d9ef-887a-44bf-aa6a-fe63ff77d054_1280x1104.png" width="220" />
</div>


### Agent = Model + Harness.

- The model brings capability. The harness turns that capability into work by giving the model tools, state, memory, execution environments, constraints, and feedback.
    - AI evals should be treated as a first-class harness component
- TLDR: **Harness engineering is how we build systems around models to make them useful. Evals are the feedback mechanism that lets a harness learn, self-correct, and improve.**
- By an **eval**, I mean a way of testing some aspect of model or agent behavior against what we expect.
    - A **harness eval** is narrower. It is meant to tell us whether the system around the model is doing its job: whether the harness is helping the agent complete the task correctly and reliably.
    - A model can be capable while the overall agent still fails because of how the surrounding system is designed.

### What Exactly Is a Harness?

- A harness is everything around the raw model that shapes how the agent behaves.
    - **Tools and execution environment** (bash, filesystem, APIs, sandboxes)
    - **Memory and state management** (short-term context, long-term skills, conversation history)
    - **Constraints and guardrails** (rules about what the agent is allowed to do, when to ask for help, how to validate outputs)
    - **Orchestration logic** (planning loops, sub-agents, retry mechanisms)
    - **Feedback and observability** (logs, traces, validation steps, human approval gates)

![](https://substackcdn.com/image/fetch/$s_!pnDu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7f9c1031-4e3c-4e2f-b714-5069952c4ef4_1024x771.png)

- the hard problem shifted from “Can the model answer?” to “Can we design the environment around the model so it can act safely and reliably?”
    - Harness engineering is the practice of designing that surrounding system. It asks: what should the model be allowed to do, what context should it receive, what tools should it have, how should it recover from mistakes, and how should humans understand what happened?

### Different Flavors of Harnesses

- **Test Harness:** The older software meaning. A controlled setup for running and testing code with test data, mocks, stubs, drivers, scripts, and reporting
- **General Agent Harness:** This is the complete runtime environment that lets a model operate as an agent. It includes memory, tool orchestration, permissions, guardrails, execution environments, and observability
- **Coding and workflow harnesses:** This is where harnesses become specific to the job. A coding harness might include repo access, terminals, tests, logs, CI, and review flows; a support or research harness might include policies, retrieval, escalation paths, source constraints, and human handoff.
- **Evaluation harness:** The measurement and feedback layer of the harness. It includes traces, eval datasets, scoring logic, failure taxonomies, custom metrics, LLM judges, human labels, and regression checks.

### Why Evals Are the Feedback Mechanism of the Harness

- A harness without strong evals can make an agent do more things
    - But doing more is not the same as getting better.
- The hard part of harness engineering is not only deciding what the agent can access. It is knowing whether those design choices actually improved the system.
    - Did the new tool help, or did it create another way to fail?
    - Did the new memory rule reduce repeated mistakes, or did it introduce stale context?
    - Did the stricter guardrail make the agent safer, or did it make the product less useful?

![](https://substackcdn.com/image/fetch/$s_!b7Ba!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe45b369a-f3ba-417d-9e99-d46f221b655c_1177x650.png)

- In classical machine learning, training data gives the model a learning signal; in agent development, evals give the harness a learning signal.
    - They tell us whether a change to prompts, tools, memory, routing, permissions, or orchestration actually made the agent better.
- core pattern is simple:

> 💡 agent behavior → traces → error analysis → evals → harness changes → regression checks → better agent behavior

### What should a Good Harness Eval Measure?

- A useful way to think about harness evals is in two layers
    - First, measure end-to-end task success: did the agent actually accomplish the job?
    - Then, once you know which workflows fail, add step-level diagnostics: where did the failure happen, and which part of the harness should be inspected?

![](https://substackcdn.com/image/fetch/$s_!P6hF!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5dc3d9ef-887a-44bf-aa6a-fe63ff77d054_1280x1104.png)

1. **Agent Outcome.** This is the most honest signal of whether the agent accomplished its job.
    - Did the code pass tests. Did the booking actually happen. Did the deploy succeed.
    - Outcome signals keep the harness grounded in the real-world result.
2. **Action Correctness.** Outcome matters most, but for agents the outcome often depends on whether the right action actually happened.
    - A support agent can say “your refund has been processed,” but if the refund tool was never called and the account balance never changed, the agent did not complete the task.
3. **Trajectory and Recovery.** Most evals only check the end state. The agent either reached the goal or it didn’t.
    - A good harness eval should tell us whether the agent noticed it was off track and corrected.
4. **Regression signals.** These are evals we keep around to make sure the agent does not get worse at things it used to do well.
    - Vivek Trivedy’s *[Better Harness](https://www.langchain.com/blog/better-harness-a-recipe-for-harness-hill-climbing-with-evals)* post leans on this idea: every fixed bug should become part of the eval suite, so the harness cannot silently break old capabilities while improving new ones.
    - This is how evals become a safety net for harness iteration.
5. **Criteria freshness.** The metrics that mattered three months ago aren’t necessarily the ones that matter now.
    - The agent has gotten better, the use cases have shifted, and looking at the outputs has changed your sense of what good even means.

### How to Approach Building an Eval-Centric Harness

- The default approach is to build the agent first, ship it, and bring evals in later to measure how it is doing.
- An eval-centric approach works in the opposite direction: start with the behaviors you need to measure, then let those measurements shape the harness.
    1. Start with one workflow, not the whole agent.
        - Pick one job the agent should perform reliably: fixing a failing test, answering a refund-policy question, booking a meeting, researching a topic, or analyzing a dataset.
        - A harness eval becomes useful only when it is grounded in a specific job.
    2. Then read traces from that workflow before writing metrics.
        - Look at what the agent saw, what it retrieved, what tools it called, what came back, where it recovered, and where it drifted.
        - This is the least glamorous part of eval work, and probably the most important one

        ![](https://substackcdn.com/image/fetch/$s_!qHO9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c9cc09b-41a0-4ff6-92b6-23f0e84e227d_1224x1050.png)

    3. Once you have seen enough traces, label them. Ideally, by hand at first, and with someone who understands the domain.
        - Start by naming the failure modes: retrieval failure, tool-selection failure, tool-execution failure, citation failure, policy failure, escalation failure, completion failure. LLM-judge failure, etc.
        - These names do not need to be perfect, they need to point to a harness lever
- Nobody wants to hand-grade traces forever, and LLM-as-a-judge is often the only practical way to scale evals beyond a small pile of hand-labeled examples. The danger is an unverified judge.
    - The judge will always give you a score. The question is whether that score reflects your product’s standards or just the judge’s own preferences.
    - judges can scale evaluation, but only after humans have done the work of defining what good looks like.
- So the first job of an LLM judge is to earn the right to be trusted.
    - Treat it like a classifier. Compare it against human labels, inspect disagreements, and check whether it catches the failure modes you actually care about.
    - If the judge is wrong, the harness will optimize toward the wrong behavior.

![](https://substackcdn.com/image/fetch/$s_!Hy3-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4647fd5c-6084-4f5f-81fe-552d6a81890b_1176x788.png)
