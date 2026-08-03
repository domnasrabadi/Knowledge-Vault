---
type: article
status: structured
quality:
topics: [ai-agents, prompting, agent-evaluation]
source: ""
created: 2025-05-18
published:
author: ""
flashcards: none
updated: 2025-12-28
---
![[Screenshot 2025-05-22 at 4.18.59 pm.png| center | 600]]


- consistently, most successful implementations didn't use complex frameworks or special libraries
	- instead built w simple, composable patterns
# 1 What are agents
- can be defined several ways, key distinction between workflows vs agents 
	- <mark style="background: #FFB8EBA6;">workflows</mark> = **systems where LLMs + tools orchestrated through predefined code paths** 
	- <mark style="background: #FFB8EBA6;">agents</mark> = **systems where LLMs dynamically direct their own processes and tool usage** 
		- maintaining control over how they accomplish tasks 
## 1.1 When + when not to use agents
- recommend finding simplest solution possible, only increase complexity when needed 
	- workflows offer predictability + consistency for well-defined tasks 
	- agents better option when flexibility + model-driven decision making needed at scale 
## 1.2 When + how to use frameworks 
- many frameworks nowadays e.g. langchain, openai-agents, crewAI etc 
- frameworks often create extra layers of abstraction that can obscure underlying prompts + responses
	- making them harder to debug
- strong suggestion = start w just LLM APIs directly 
	- if you use framework, ensure you understand underlying code 
	- big source of customer error = incorrect assumptions about what happens under the hood 
# 2 Building blocks, workflows and agents 
## 2.1 The Augmented LLM
- most basic building block = the <mark style="background: #FFB8EBA6;">augmented LLM</mark> 
	- an LLM enhanced w augmentations e.g. **retrieval, tools + memory** 
	- recommend focusing on 2 key aspects 
		- tailor the capabilities to use case 
		- ensure they provide an easy + well-documented interface for your LLM 

![[Screenshot 2025-05-22 at 5.56.42 pm.png| center | 500]]

## 2.2 Workflows 
- <mark style="background: #FFB8EBA6;">Prompt chaining</mark> = decomposing task into sequence of steps, each LLM call processing the output of the previous 
	- can add programmatic checks (e.g. gates) on any intermediate steps to ensure progress still on track
	- when to use
		- when tasks can be asily + cleanly decomposed into fixed subtasks 
		- tradeoff = latency for higher accuracy 

![[Screenshot 2025-05-22 at 5.57.46 pm.png| center | 700]]

- <mark style="background: #FFB8EBA6;">Routing</mark> = classifies an input + directs it to specialised follow up task
	- allows for separation of concerns, and more specialised prompts 
	- since optimising for 1 kind of input can hurt performance on other kinds 
	- when to use
		- for complex tasks with distinct categories that are better handled separately 
		- and where classification can be handled accurately (by LLM or regular classification model)
			- e.g. customer service queries
			- also can route harder questions to larger models, easier questions to smaller models

![[Screenshot 2025-05-22 at 5.58.05 pm.png| center | 600]]

- <mark style="background: #FFB8EBA6;">Parallelisation</mark> = work simultabneously on a task and aggregate their outputs
	- can work in 2 key ways 
		- <span style="color:rgb(255, 0, 247)">sectioning</span> = breaking a task into independent subtasks run in parallel 
		- <span style="color:rgb(255, 0, 247)">voting</span> = running same task multiple times to get diverse outputs 
	- when to use 
		- when divided subtasks can be parallelised for speed or
		- when multiple perspectives/attempts needed for higher confidence results 
	- examples of parallelisation being useful
		- sectioning - guardrails where 1 model processes queries, another screens them for 'risk'
		- voting - reviewing code for vulnerabilities, several different prompts review + flag the code
		- voting - guardrails with different prompts evaluating different aspects or requiring different vote thresholds to balance FP + FN 

![[Screenshot 2025-05-22 at 5.59.24 pm.png| center | 600]]

- <mark style="background: #FFB8EBA6;">Orchestrator-workers</mark> = central LLM dynamically breaks down tasks, delegates them to worker LLMs then synthesises their results 
	- when to use
		- complex tasks where you don't know the subtasks needed
	- key difference vs parallelisation = flexibility, subtasks not pre-defined but determined by orchestrator based on specific inputs 

![[Screenshot 2025-05-22 at 5.59.46 pm.png| center | 600]]

- <mark style="background: #FFB8EBA6;">Evaluator-optimiser</mark> = one LLM call generates a response, another provides evaluation and feedback, in a loop 
	- when to use 
		- when we have clear eval criteria + when iterative refinement provides measurable value 
			- especially when responses can be demonstrably improved with human articulating feedback or LLM feedback 

![[Screenshot 2025-05-22 at 6.00.02 pm.png| center | 600]]

## 2.3 Agents
- emerging in prod as LLM key capabilities mature 
	- i.e. understanding complex inputs, reasoning + planning, reliable tool use and recovering from errors 
	- crucial for agents to gain "ground truth" from environment at each step to assess progress
		- e.g. tool call results 
	- agents can then pause for human feedback at checkpoints or when encountering blockers 
- <mark style="background: #FFB8EBA6;">agents</mark> = ***typically just LLMs using tools based on environmental feedback in a loop*** 
	- therefore crucial to design toolsets + documentation clearly and thoughtfully 
- ideal for open-ended problems where it's difficult/impossible to rpedict required number of steps or when you cannot hardcode a fixed path 
	- autonomous nature of agents = higher costs + potential for compounding errors

![[Screenshot 2025-05-22 at 6.00.23 pm.png| center | 600]]

## 2.4 Combining + customising these patterns
- only consider adding complexity if it demonstrably improves outcomes 

![[Screenshot 2025-05-22 at 6.00.40 pm.png| center | 500]]

# 3 Summary 
- when implementing agents, follow 3 core principles
	- 1. mantain simplicity in agent design 
	- prioritise transparency by explicitly showing the agent's planning steps 
	- carefully craft your ACI (agent computer interface) through rigourous tool documentation and testing 
