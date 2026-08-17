---
type: article
status: raw
quality: 1
topics: [ai-agents, agent-evaluation, mlops, model-monitoring, ai-engineering]
source: https://www.langchain.com/blog/the-agent-development-lifecycle
created: 2026-08-16
published: 2026-05-09
author: Harrison Chase
flashcards: none
updated: 2026-08-17
---

# The Agent Development Lifecycle (ADLC)

<div align="center">
  <img src="https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/6a0572387d90e67612454cde_pic1.avif" width="220" />
</div>

- The best organizations have figured out how to do it repeatedly, safely, and systematically. They ship early, learn from real usage, and iterate quickly
- That lifecycle has four parts: **Build → Test → Deploy → Monitor**
- The order is intentional.
	- Testing should start before an agent reaches production, not after.
	- Teams need to test the agents before deployment, deploy them in a controlled way, monitor how they behave in production, and feed those learnings back into the next build and evaluation cycle.

## Build

- The build phase is where teams decide what kind of agent system they are creating and what level of abstraction they want to use.
	- **Agent frameworks** focus primarily on abstractions. They help developers compose model calls, tools, prompts, retrieval, structured outputs, and agent loops
	- **Agent runtimes** focus on execution. They support agents that need state, control flow, durability, and human intervention
	- **Agent harnesses** focus on doing. They provide the surrounding structure agents need for longer-running tasks: prompts, skills, MCP servers, hooks, middleware, and sometimes a filesystem
- These distinctions matter because “building an agent” can mean different things.
- There is also a no-code and low-code side of the build phase.
	- Tools like LangSmith Fleet, Claude Cowork, and n8n allow more people to participate in agent development.
	- That matters because the person who understands the workflow needed is not always the person who writes the code.
- The best build environments make simple things simple and complex things possible. They let domain experts edit prompts, skills, and context, while still giving engineers control over the parts that need to be reliable, testable, and governed.

## Test

- Before an agent is deployed, teams need a way to determine whether it is actually ready.
- It does mean having enough evals in place to catch obvious failures, compare versions, and avoid shipping changes blindly.
- Most eval workflows start with a small dataset of representative tasks.
	- Some examples come from expected use cases, while others come from manual testing, dogfooding, support tickets, prior traces, or known edge cases.
	- Over time, production traces make these datasets much stronger, but testing should start before production.

### Datasets and Metrics

- Datasets are how teams preserve what they learn. Without them, the same failures tend to reappear after prompt changes, model upgrades, or tool updates. The right metrics depend on the task.
- In some cases, there is a clear ground truth answer.
	- Did the agent extract the right value?
	- Did it choose the right label?
	- Did it update the right field?
	- These tasks can be measured directly for correctness.
- Other times, there is no single ground truth answer.
	- An agent may need to write a response, summarize a conversation, decide whether to escalate, or complete a task with many valid paths.
	- In those cases, teams rely more on criteria-based evaluation.

### Experiments

- Experiments are what connect datasets and metrics to iteration.
	- They allow teams to compare prompts, models,retrieval strategies, tool schemas, and orchestration patterns against the same evaluation set. .
	- Over time, these experiments show whether the agent is improving or regressing

### Simulations

- Many agents are multi-turn systems.
	- They do not just answer one question; they have a conversation, gather information, call tools, update state, and recover from ambiguity.
	- For those agents, single-turn evals are not enough.
	- Teams need [multi-turn evals and simulated end-to-end interactions](https://docs.langchain.com/langsmith/multi-turn-simulation).
- Good testing practices help teams improve agents systematically without relying on vibes.
	- They turn expected behavior into datasets, datasets into experiments, and experiments into better versions of the system.
	- After deployment, monitoring supplies the real-world examples that make those evals stronger.

## Deploy

- For simple agents, deployment may look similar to deploying a traditional application.
	- But many agents need more than a stateless server.
	- They run over longer periods of time, call tools, wait for human input, write files, recover from interruptions, and maintain state across multiple interactions or tasks.
- A production agent runtime typically needs to support durable execution and human-in-the-loop patterns.
	- Durable execution means the agent can checkpoint progress and resume instead of losing work when something fails.
	- Human-in-the-loop means the agent can pause when it needs approval, clarification, or review.

## Monitor

- This is where monitoring agents differs from monitoring traditional software.
	- Metrics like latency, cost, error rates, and uptime still matter, but they are only part of the picture.
	- An agent can return a technically successful response and still fail the task itself.
	- It may call the wrong tool, rely on the wrong context, skip a required approval step, or produce an answer that sounds plausible but is wrong.
- To understand those failures, teams need traces.

### Signals

- Monitoring should also include harvesting signals from those traces.
- Some of those signals can come from [LLM-as-judge evaluators](https://docs.langchain.com/langsmith/llm-as-judge).
	- For example, a judge can score whether the agent answered the user’s question, followed policy, used the right tone, or completed the task.
	- Other signals can be simpler.
	- A regex can catch whether a required phrase appeared, whether a forbidden tool was called, or whether a known failure pattern occurred.
- These signals are useful for more than just quality checks.
	- They can also become a form of product analytics.
	- They can tell you which tasks users are asking agents to do, where agents are getting stuck, how often users correct them, and where users perceive errors.

### Feedback

- It is not enough to store traces alone.
	- Teams also need to store feedback with those traces.
	- That feedback can come from LLM judges, regex-based signals, human reviewers, or direct user feedback collected through an API

### Dashboards

- Finally, teams need dashboards and alerts that can surface trends over time.
- A useful [agent dashboard](https://docs.langchain.com/langsmith/dashboards) tracks metrics like usage, feedback, latency, cost, tool calls, evaluator scores, and recurring failure patterns. [Alerts](https://docs.langchain.com/langsmith/alerts) should trigger when important thresholds are crossed, such as rising latency, increasing costs, failing tools, declining user feedback, or spikes in policy violations.
- Good monitoring is not just about knowing whether the system is up. It is about understanding whether the agent is doing the right work, in the right way, and improving over time.

## Iterate

- The best organizations move through the agent development lifecycle quickly and systematically.
- They do not wait for a perfect agent before shipping. Instead, they build something useful, test it enough to understand its behavior, deploy it in a controlled way, monitor how it performs in production, and feed those learnings back into the next version.
- Teams with datasets, experiments, tracing, feedback, and dashboards can learn directly from real real usage. They can test changes before rolling them out broadly, identify what broke in production, turn failures into evals, and improve the agent without relying on guesswork.
- This is how teams hill-climb, and how agent systems improve over time.
- The most effective teams find the hard examples, understand why the agent failed, and adjust the prompt, tool configuration, retrieval strategy, model, middleware, or workflow. They re-run the evals, deploy the better version, and monitoring gives them the next edge cases and failures.
- Inside an enterprise, the challenge is making that loop repeatable across teams.

## Govern

- Governance sits around the entire agent development lifecycle.
- As organizations deploy more agents, governance becomes necessary. Without it, teams quickly end up with agents that are difficult to discover, difficult to monitor, expensive to run, and unclear in what they are allowed to do.

### Cost

- Agents can become expensive because they may involve multiple model calls, long context windows, repeated tools usage, retries, or run for a long time. Organizations need ways to [track and manage that spend](https://docs.langchain.com/langsmith/cost-tracking) through budgets, usage monitoring, alerts, and visibility into which agents, teams, models, or tools are driving costs.

### Tool Access

- Agents are useful because they can take action, but that also introduces risk. Teams need clear controls around which tools an agent can access, under what conditions, and on behalf of which users.
- This is where [audit trails](https://docs.langchain.com/langsmith/audit-logs) become important.
	- If an agent calls a tool, organizations should be able to inspect which agent made the call, what inputs it used, what outputs it produced, and what user or policy authorized the action.
	- Tool calls are often where agent behavior drives business impact, so they need to be observable and reviewable.
- Not every tool call should be fully automated.
	- Some operations should pause for human review, especially when they involve customers, financial systems, sensitive data, or production infrastructure.
	- Human-in-the-loop workflows work best when they are designed into the system from the beginning.

### Discoverability

- As organizations build more agents, they also accumulate more reusable assets such as prompts, skills, tools, retrieval sources, policies, and even other agents.
	- Without good discovery and governance mechanisms, teams tend to recreate these components repeatedly, leading to inconsistency.
	- Shared context and shared agents need to be findable, reusable, and governed.
- This is especially important for skills.
	- A skill can encode a workflow, a writing style, a domain-specific procedure, or instructions for using a tool.
	- If one team has already built a good skill, another team should be able to find it rather than write a new version from scratch.

## Conclusion

- The best organizations have already started to operate this way.
	- They ship early, but they do not ship blindly.
	- They evaluate before deploying, monitor behavior after deployment, and continuously use what they learn to make the next version better
