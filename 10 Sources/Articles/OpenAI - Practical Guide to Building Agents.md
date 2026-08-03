---
type: article
status: structured
quality:
topics: [ai-agents, prompting]
source: ""
created: 2025-04-19
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- from the PDF https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- Purpose: provides frameworks for identifying promising use cases, clear patterns for designing agent logic and orchestration, and best practices to ensure your agents run safely, predictably, and effectively

# 1 What is an agent?
- conventional software enables users to streamline and automate workflows
	- agents are able to perform the same workflows on the users’ behalf with a high degree of independence
- <mark style="background: #FFB8EBA6;">agents</mark> = systems that **independently** accomplish tasks on your behalf
	- applications that integrate LLMs but don’t use them to control workflow execution
	- e.g. chatbots, single-turn LLMs, or sentiment classifiers—are not agents
- more concretely, agent possesses core characteristics that allow it to act reliably and consistently on behalf of a user:
	- leverages an LLM to manage workflow execution and make decisions
	- recognises when a workflow is complete + can proactively correct actions if needed
		- in case of failure, can halt execution and transfer control back to the user 
	- has access to various tools to interact w external systems
		- both to gather context + take actions
		- dynamically selects the appropriate tools depending on workflow's current state
		- always operating within clearly defined guardrails 

# 2 When should you build an agent?
- building agents **requires rethinking how your systems make decisions and handle complexity** 
	- unlike conventional automation, agents are uniquely suited to workflows where traditional deterministic and rule-based approaches fall short
	- e.g. payment fraud analysis
		- traditional rules engine works like a checklist, flagging transactions based on preset criteria
		- contrast, an LLM agent functions more like a seasoned investigator, evaluating context, considering subtle patterns, and identifying suspicious activity even when clear-cut rules aren’t violated
		- this nuanced reasoning capability is exactly what enables agents to manage complex, ambiguous situations effectively
- to evaluate where agents can add value, prioritise workflows that previously could not be automated because traditional methods didn't work
	- **complex decision making** - workflows with nuanced judgement, exceptions or context sensitive decisions 
		- e.g. refund approvals in customer service workflows 
	- **difficult to maintain rules** - expensive maintenance systems from intricate rulesets, make updates costly + error prone 
	- **heavy reliance on unstructured data** - scenarios that involve interpreting natural language, extracting meaning from docs or interacting conversationally 
- consider deterministic solutions if the above criteria are not met 

# 3 Agent design foundations 
- fundamentally, an agent has 3 core components 
	- <mark style="background: #FFB8EBA6;">model</mark> = LLM powering the agent's reasoning + decision making
	- <mark style="background: #FFB8EBA6;">tools</mark> = external functions or APIs the agent can use to take action 
	- <mark style="background: #FFB8EBA6;">instructions</mark> = explicit guidelines + guardrails defining how the agent behaves 
## 3.1 Selecting your models 
- different models have different tradeoffs 
	- e.g. task complexity, latency, cost 
	- consider using a variety of different models for different tasks in the workflow 
- not every task needs the smartest model 
	- e.g. simple retrieval or intent classifiers can use smaller/faster models
	- harder tasks e.g. decide to approve refund - might benefit from more capable model 
- 💡 tip approach = build your agent prototype with the most capable model for every task to establish a performance baseline
	- from there, try swap in smaller models to see if they still get acceptable results
	- allows us to see extent of agent's abilities + diagnose if smaller models can replace 
- ***principles for choosing models***
	- set up evals to establish baseline performance 
	- focus on meeting your accuracy target w best models available 
	- optimise for cost/latency by replacing w smaller models where possible 
## 3.2 Defining tools 
- tools extent agent capabilities via using APIs from underlying apps/systems
	- legacy systems can benefit from computer tool use to directly interact via UI 
- each tool should have standardised definition 
	- enables flexibility, many-to-many relationships between tools and agents
	- well documented, thoroughly tested + reusable tools improve discoverability, simplify version management + prevent redundant definitions
- broadly, agents need 3 types of tools 
	- <mark style="background: #FFB8EBA6;">data</mark> = <span style="color:rgb(255, 0, 247)">enables agents to retrieve context + info necessary for executing workflow</span> 
		- e.g. SQL databases, read PDF docs, search the web 
	- <mark style="background: #FFB8EBA6;">action</mark> = <span style="color:rgb(255, 0, 247)">enable agents to interacts w systems to take actions</span> like add new info, update records, send messages
		- e.g. send emails/texts, update CRM record, hand-off customer service ticket to human 
	- <mark style="background: #FFB8EBA6;">orchestration</mark> = <span style="color:rgb(255, 0, 247)">agents themselves can serve as tools for other agents</span>
		- e.g. refund agent, research agent, writing agent
- as the number of required tools increases, consider splitting tasks across multiple agents
## 3.3 Configuring instructions 
- high quality clear instructions especially critical for agents
	- reduce ambiguity + improve agent decision making 
- best practices for agent instructions 
	- <span style="color:rgb(255, 0, 247)">use existing documents</span> = for creating routines, use existing SOPs, support scripts, policy docs
		- to create LLM friendly routines 
		- e.g. for customer service, routines can map to individual articles in knowledge base
	- <span style="color:rgb(255, 0, 247)">prompt agents to break down tasks</span> = provide smaller, clearer steps from dense resources
		- to help minimise ambiguity + help model better instruction follow
	- <span style="color:rgb(255, 0, 247)">define clear actions</span> = make sure every step in routine corresponds to specific action/output
		- e.g. step might be instruct agent to ask user for order number or call API to get account details
		- being explicit about the action (+ even wording of user facing message) = less room for interpretation error 
	- <span style="color:rgb(255, 0, 247)">capture edge cases</span> = real world interactions often create decision points e.g. how to proceed based on incomplete info or off-topic question 
		- robust routines anticipate common variations + include instructions how to handle them 
			- includes conditional steps + branches e.g. alternative step if required piece of info is missing 
- 💡 tip: use advanced models (o3, o4 mini) to automatically generate instructions from existing documents 

```jinja2
“You are an expert in writing instructions for an LLM agent. Convert the following help center document into a clear set of instructions, written in a numbered list. The document will be a policy followed by an LLM. Ensure that there is no ambiguity, and that the instructions are written as directions for an agent. The help center document to convert is the following {{help_center_doc}}”
```

## 3.4 Orchestration 
- while tempting to build fully autonomous agent w complex architecture, better success with incremental approaches
- 2 general orchestration categories
	- <mark style="background: #FFB8EBA6;">single-agent</mark> = single model equipped w appropriate tools + instructions executes workflows in a loop 
	- <mark style="background: #FFB8EBA6;">multi-agent</mark> = workflow execution distributed across multiple coordinated agents 
### 3.4.1 Single-agent systems
- single agent can handle many tasks by incrementally adding tools - keeping complexity manageable + simplifying evals + maintenance
	- each new tool expands capability w/o prematurely forcing you to orchestrate multiple agents
- every orchestration approach has the concept of a <mark style="background: #FFB8EBA6;">run</mark>
	- a loop that lets agents operate until an exit condition is reached
	- common exit conditions = 
		- <span style="color:rgb(255, 0, 247)">tool calls</span>
		- <span style="color:rgb(255, 0, 247)">certain structured output</span> 
		- <span style="color:rgb(255, 0, 247)">errors</span>
		- <span style="color:rgb(255, 0, 247)">reaching max number of turns</span> 

![[Screenshot 2025-04-20 at 10.25.36 am.webp| center | 500]]

- concept of loops = fundamental to agents
	- can have sequence of tool calls + handoffs between agents but allow model to run multiple steps until exit condition is met 
- 💡 effective tip to manage complexity w/o multi-agent framework = **use prompt templates**
	- rather than maintain individual prompts for distinct use cases -> use single flexible base prompt which accepts policy variables
	- template approach easier to adapt to various contexts 
	- w new use cases, can update variables rather re-write entire workflows

```jinja2
You are a call center agent. 
You are interacting with {{user_first_name}} who has been a member for {{user_tenure}}. 
The user's most common complains are about {{user_complaint_categories}}. 
Greet the user, thank them for being a loyal customer, and answer any questions the user may have!
```

- 💡 suggested strategy = **maximise single agent capabilities first** 
	- more agents can provide intuitive separation of concepts but add complexity + overhead 
	- for many complex workflows, splitting up prompts + tools across multiple agents -> better performance + scalability 
		- when agents fails to follow complicated instructions or consistently select incorrect tools 
		- then consider to divide system + introduce more distinct agents 
	- practical guidelines to splitting agents:
		- <span style="color:rgb(255, 0, 247)">complex logic</span> = when prompts contain many conditional statements (multiple if-then-else branches) + prompt templates
		- <span style="color:rgb(255, 0, 247)">tool overload</span> = when you have several tools that are similar/overlap 
			- use multiple agents if improving tool clarity (e.g. descriptive names, clear params + detailed descriptions) don't help
### 3.4.2 Multi-agent systems 
- 2 broad categories for how to setup multi-agent
	- <mark style="background: #FFB8EBA6;">manager</mark> (<span style="color:rgb(255, 0, 247)">agent as tools</span>) = **central manager agent coordinates specialised agents via tool calls**
		- each handling specific task or domain 
		- ideal when you want one agent to control workflow execution + have access to the user
	- <mark style="background: #FFB8EBA6;">decentralised</mark> (<span style="color:rgb(255, 0, 247)">agents handing off to agents</span>) = **multiple agents operate as peers, handing off tasks to other agents based on specialisation**
		- Agents SDK - handoffs are a type of tools or function 
			- if agent calls handoff function, immediately starts execution on new agent + transfer latest conversation state 
		- involves many agents on equal footing - optimal when you don't need single agent to maintain control 
			- instead allows each agent to take over execution + interact w user as needed 
- multi-agent systems can be modelled as graphs
	- agents = nodes
	- tool calls/handoffs = edges 
# 4 Guardrails
- guardrails as a layer defence mechanism 
	- one single guardrail unlikely to provide sufficient protection - using multiple specialised guardrails = more resilient 
	- e.g. below diagram shows combination of:
		- LLM-based guardrails
		- rule based guardrails (e.g. regex)
		- OpenAI moderation API 

![[Screenshot 2025-04-20 at 10.48.56 am.webp| center | 500]]

## 4.1 Types of guardrails
1. <span style="color:rgb(255, 136, 0)">relevance classifier</span> = ensures agent stays within intended scope, flagging off-topic queries
2. <span style="color:rgb(255, 136, 0)">safety classifier</span> = detects unsafe inputs (jailbreaks, prompt injections) to attempt to exploit system vulnerabilities 
3. <span style="color:rgb(255, 136, 0)">PII filter</span> = prevent unnecessary exposure of PII by vetting model outputs for PII
4. <span style="color:rgb(255, 136, 0)">moderation</span> = flags harmful or inappropriate inputs to maintain safe, respectful interactions
5. <span style="color:rgb(255, 136, 0)">tool safeguards</span> = asses risk of each tool available to agent, assigning a rating (L, M, H) based on factors
	- e.g. factors like read-only vs write access, required account permissions, financial impact 
	- use risk ratings to trigger automated actions e.g.
		- pause for guardrail checks or escalate to human before escalating high-risk functions
6. <span style="color:rgb(255, 136, 0)">rules-based protections</span> = simple deterministic measures to prevent known threats (prohibited terms) via blocklists, input length limits, regex filters
7. <span style="color:rgb(255, 136, 0)">output validation</span> = ensure response aligns w brand values via prompt engineering + content checks
## 4.2 Building guardrails
- following heuristics found to be effective 
	- focus on data privacy + content safety 
	- add new guardrails based on real-world edge cases + failures you encounter
	- optimise for both security + user experience, tweak guardrails as your agent evolves 

```python
from agents import (
	Agent, 
	GuardrailFunctionOutput, 
	InputGuardrailTripwireTriggered,
	RunContextWrapper,
	Runner,
	TResponseInputItem,
	input_guardrail,
	Guardrail,
	GuardrailTripwireTriggered
)
from pydantic import BaseModel

class ChurnDetectionOutput(BaseModel):
	is_churn_risk: bool
	reasoning: str

churn_detection_agent = Agent(
	name = "Churn Detection Agent",
	instructions = "Identify if the user messages indicates a potential customer churn risk",
	output_type = ChurnDetectionOutput,
)

@input_guardrail
async def churn_detection_tripwire(
	ctx: RunContextWrapper[None],
	agent: Agent,
	input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
	
	result = await Runner.run(churn_detection_agent, input, context = ctx.context)

	return GuardrailFunctionOutput(
		output_info = result.final_output,
		tripwire_triggered = result.final_output.is_churn_risk,
	)

customer_support_agent = Agent(
	name = "Customer support agent",
	instructions = "You are a customer support agent. You help customers with their questions",
	input_guardrails = [
		Guardrail(guardrail_function=churn_detection_tripwire)
	]
)

async def main()
	# this should be ok
	await Runner.run(customer_support_agent, "Hello!")
	print("Hello message passed")

	# This should trip the guardrail
	try:
		await Runner.run(agent, "I think i might cancel my subscription")
		print("Guardrail didnt trip - this is unexpected")
	except:
		print("churn detection guardrail tripped")
```

- Agents SDK treats guardrails as first-class concepts
	- relies on optimistic execution by default i.e. primary agent proactively generates outputs while guardrails run concurrently
- guardrails can be implemented as functions or agents 
## 4.3 Human Intervention 
- human intervention = critical safeguard to improve agent real-world performance
	- allows agent to gracefully transfer control when it cannot complete a task 
- 2 primary triggers to warrant human intervention 
	- <mark style="background: #FFB8EBA6;">exceeding failure thresholds</mark> = set limits on agent retries or actions
		- if agent exceeds limits, escalate to human intervention 
	- <mark style="background: #FFB8EBA6;">high-risk actions</mark> = actions that are sensitive, irreversible, or have high stakes need human oversight until confident
# 5 Conclusion 
- agents mark a new era in workflow automation
	- where systems can reason through ambiguity, take action across tools, and handle multi-step tasks with a high degree of autonomy
- unlike simpler LLM applications, agents execute workflows end-to-end
	- making them well-suited for use cases that involve complex decisions, unstructured data, or brittle rule-based systems
- to build reliable agents, start with strong foundations: pair capable models with well-defined tools and clear, structured instructions
	- use orchestration patterns that match your complexity level, starting with a single agent and evolving to multi-agent systems only when needed
	- guardrails are critical at every stage, from input filtering and tool use to human-in-the-loop intervention
		- helping ensure agents operate safely and predictably in production
- path to successful deployment isn’t all-or-nothing
	- start small, validate with real users, and grow capabilities over time