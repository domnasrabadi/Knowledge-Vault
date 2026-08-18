---
type: article
status: raw
quality: 
topics: [ai-engineering, ai-agents, agent-evaluation, human-in-the-loop]
source: https://www.langchain.com/blog/human-judgment-in-the-agent-improvement-loop
created: 2026-08-17
published: 2026-04-09
author: Rahul Verma
flashcards: none
updated: 2026-08-18
---

# Incorporating Human Judgment Into the Agent Improvement Loop

<div align="center">
  <img src="https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69dce8a01c18c14b60cd4372_76.webp" width="220" />
</div>

- AI agents work best when they reflect the knowledge and judgment your team has built over time. Some of that is institutional knowledge that’s already documented and easy for an agent to use as-is. But most great organizations also rely on tacit knowledge that lives inside their employees’ minds.
- Ensuring this wisdom makes its way into an agent requires an improvement loop that incorporates input from domain experts.

### Real-life inspired example: Copilot for traders

- **agent needs context at both the financial services domain level and the technical database layer**.
- The former includes unwritten trading conventions that determine how to interpret requests like “today’s exposure” or “recent volatility.” The latter includes practical knowledge of the database, like which tables are authoritative vs. outdated, or which query patterns tend to be incorrect or inefficient.
- We’ll need to engage with the appropriate subject-matter experts to include all the unwritten context the agent needs.

### How human input improves each component of an AI agent

- Building an agent means deciding when to invoke an LLM and managing what context to provide with each call

#### Workflow Design

- there are benefits to using deterministic code to define parts of the workflow: lower latency, fewer tokens, and the guarantee that critical steps actually run.
- In some regulatory or high-risk settings, you need code to strictly control the sequence of actions.

#### Tool Design

- Developers must implement the tools the agent can use and configure the names, parameters, and descriptions that the LLM relies on to decide when to invoke them.
- A key tradeoff is flexibility vs. control for LLM-generated queries: a general `execute_sql` step allows for flexible queries but increases risk; parameterized query tools are safer but less capable.
- review of your business constraints might give you a sense of which option is right for you
- you’ll need to run evaluations to determine the performance and risk characteristics of your tool design and ship only when all stakeholders are comfortable with the results.

#### Agent Context

- industry has moved toward providing agents with much richer context at the beginning of their execution.
- Instead of cramming everything into one system prompt, your team curates documentation, examples, and domain rules in advance, then lets the agent fetch what it needs at runtime.
- Effective agent design involves deciding what knowledge the agent should access and organizing it so the agent can retrieve the right information at the right moment.
- Choosing and structuring the information available to the agent when it starts up is part of the discipline of context engineering.
- **It’s impossible to know what an AI agent will do until it runs**.
- Putting your agent in front of users is the only way to collect the data you need to make it ultimately successful.

![](https://cdn.prod.website-files.com/65c81e88c254bb0f97633a71/69dce8f18d5f7e336d258f2c_agent-improvement-loop.png)


### The key to high return on human time invested: automated evaluations, aligned with human judgment

- We’ve observed that **teams get more leverage when humans help design and calibrate automated evaluators, rather than manually reviewing large volumes of agent outputs**.
- The scalable approach is to translate expert judgment into [automated evaluations](https://www.langchain.com/resources/llm-evals) that let you test broadly and continuously.

### Development: Curate test suites and evaluators

- Before development starts, **engineers should have at least a small set of use case scenarios and expected behavior as part of the project requirements**.
- initial tests help confirm that the agent performs the core tasks correctly.
- As the agent approaches production readiness, engineers should work with product managers and subject matter experts to build a more comprehensive test suite that evaluates both overall behavior and key subcomponents.
- We can create a mini-flywheel during this phase by augmenting our initial datasets with examples inspired by interesting cases we encounter during manual testing.

### After deployment: Use automated evaluations and monitoring to direct human attention to where it’s most needed

- Automated evaluations running on production data can help monitor the agent and surface situations that warrant human attention.
- Unstructured explorations of live behavior inspire some of the most valuable improvements for AI agents.
- As automated evaluations, human annotations, and aggregate-level insights accumulate, they provide a clear picture of how the agent performs in the real world. Those learnings feed into the final step of the cycle: restarting the iteration loop by building the agent’s next version.

### Continuous refinement: turn today’s production data into tomorrow’s test suites

- When you build the first version of an agent, your evaluation suite is at best educated guesses on what tests you need to validate that it works.
- After launch, you gain access to a much better source of test cases: real production data.
- You need to curate this data into test suites that are comprehensive but not unnecessarily large. Automated systems can help generate candidate datasets, for example, by filtering production traces based on evaluator results.
- But **we often need human judgment to curate balanced, representative evaluation sets.**
- One of the most helpful datasets we can curate is a “golden dataset,” consisting of examples of the copilot’s best work so far, so we can use it as a baseline to ensure future versions perform at least as well.

### Conclusion

- Effective agent development combines human judgment with the scalability of automated evaluations. Human expertise helps define what “good” looks like by shaping workflows, tools, context, and evaluation criteria.
- Human feedback improves evaluators, test suites, and the agent itself
	- the improved agent we deploy gets us more data that tells us how to improve it
	- these insights drive the next development iteration.
