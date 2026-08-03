---
type: article
status: structured
quality:
topics: [multi-agent-systems, ai-agents, agent-evaluation]
source: ""
created: 2025-06-14
published:
author: ""
flashcards: none
updated: 2025-12-28
---
June 13 2025 - Link to [blog post](https://www.anthropic.com/engineering/built-multi-agent-research-system)

- [[#1 Notes|1 Notes]]
	- [[#1 Notes#1.1 Benefits of a multi-agent system|1.1 Benefits of a multi-agent system]]
	- [[#1 Notes#1.2 Architecture overview for research|1.2 Architecture overview for research]]
	- [[#1 Notes#1.3 Prompt engineering principles|1.3 Prompt engineering principles]]
	- [[#1 Notes#1.4 Effective agent evals|1.4 Effective agent evals]]
	- [[#1 Notes#1.5 Production reliability + engineering challenges|1.5 Production reliability + engineering challenges]]
	- [[#1 Notes#1.6 Miscellaneous tips for agents|1.6 Miscellaneous tips for agents]]
- [[#2 Mindmap summary|2 Mindmap summary]]


# 1 Notes
## 1.1 Benefits of a multi-agent system 
- research work involves open-ended problems, very difficult to predict required steps in advance
	- when people do research, they tend to continuously update their approach based on discoveries, following leads emerging during investigation
- this unpredictability makes AI agents particularly well suited to research tasks
	- linear, one-shot pipeline cannot handle these tasks 
- essence of search = ***compression*** i.e. distilling insights from a vast corpus 
	- subagents facilitate compression by: 
		- operating in parallel w their own context windows
		- exploring different aspects of the question simultaneously 
		- condensing most important tokens for the lead research agent 
	- human societies have become exponentially more capable in information age because of our collective intelligence + ability to coordinate
- multi-agent systems excel especially for breadth-first queries
	- i.e. queries involving pursuing multiple independent directions simultaneously 
- multi-agent systems work mainly because they help spend enough tokens to solve the problem 
	- found that token usage explains 80% of the variance
	- number of tool calls + choice of foundation model are 2 other factors 
- downside of multi-agent systems = burn through tokens fast
	- multi-agent systems consume 15x more tokens than chat conversations 
		- for economic viability, multi-agent systems require tasks where value of task > price for increased performance
	- excel at valuable tasks involving heavy parallelisation, info exceeding context window + interfacing w numerous complex tools
## 1.2 Architecture overview for research
- Claude research uses orchestrator-worker pattern
	- lead agent coordinates process while delegating to specialised subagents that operate in parallel 

![[Screenshot 2025-06-15 at 11.47.02 am.png| center | 600]]

- process
	- 1. user submits query
	- 2. lead agent analyses - `LeadResearcher` agent that enters an iterative research process
	- 3. lead agent developers strategy
		- begins by thinking through the approach and saving its plan to Memory to persist the context, since if the context window exceeds 200,000 tokens it will be truncated and it is important to retain the plan
	- 4. spawns subagents to explore different aspects simultaneously
		- creates specialized `Subagents` with specific research tasks
		- Each `Subagent` independently performs web searches, evaluates tool results using **interleaved thinking**, and returns indings to the `LeadResearcher`
	- 5. `LeadResearcher` synthesizes these results and decides whether more research is needed—if so, it can create additional subagents or refine its strategy
	- 5. Once suficient information is gathered, the system exits the research loop and passes all findings to a `CitationAgent`
		- processes the documents and research report to identify specific locations for citations

![[Screenshot 2025-06-15 at 11.49.23 am.png| center | 700]]

## 1.3 Prompt engineering principles
- since each agent steered by prompts, prompt eng was primary lever for improving behaviours
- principles for prompting agents 
	- <mark style="background: #FFB8EBA6;">think like your agents</mark> = to iterate on prompts, must understand their effects
		- involved watching agents work step by step 
		- revealing failure modes e.g. 
			- agents continuing tasks when already having sufficient results
			- using overly verbose search queries 
			- selecting incorrect tools 
	- <mark style="background: #FFB8EBA6;">teach orchestrator how to delegate</mark>  
		- each subagent needs an: 
			- objective 
			- output format 
			- guidance on tools + sources to use
			- clear task boundaries
		- w/o detailed task descriptions, agents duplicate work/leave gaps/fail to find necessary info 
	- <mark style="background: #FFB8EBA6;">scale effort to query complexity</mark> = agents struggle to judge appropriate effort for different tasks 
		- embedded scaling rules in the prompts to help w this 
			- simple fact finding queries -> use 1 agent w 3-10 tool calls 
			- direct comparisons -> use 2-4 subagents w 10-15 tool calls each
			- complex research -> 10+ subagents w clearly divided responsibilities 
	- <mark style="background: #FFB8EBA6;">tool design + selection are critical</mark> = gave the agents explicit heuristics to prevent failures
		- examine all available tools first 
		- match tool usage to user intent 
		- search web for broad external exploration
		- prefer specialised tools over generic ones
		- each tool needs distinct purpose + clear description 
	- <mark style="background: #FFB8EBA6;">let agents improve themselves</mark> = use metaprompting i.e. agent to help write prompts for other agents 
		- e.g. writing tool documentation, docstrings etc 
	- <mark style="background: #FFB8EBA6;">start wide, then narrow down</mark> = search strategy should mirror expert human research 
		- explore landscape before drilling into specifics 
		- start w short broad queries, eval whats available, then progressively narrow focus 
	- <mark style="background: #FFB8EBA6;">guide the thinking process</mark> = use reasoning models for planning approaches and delegation 
		- subagents can also plan, then use interleaved thinking after tool results
			- to eval quality, identify gaps, refine next query 
		- interleaved thinking = Claude 4 model mode to enable thinking between tool calls + results
	- <mark style="background: #FFB8EBA6;">parallel tool calling transforms speed + performance</mark> = complex tasks naturally involve exploring many sources
		- speed can be achieved through 2 types of parallelisation
			- parallelise subagents 
			- subagents use 3+ tools in parallel
- prompt strategy focused on instilling good heuristics rather than rigid rules
	- studied how skilled humans approach research + encoded the strategies into the prompts
	- examples of heuristics 
		- decomposing difficult questions into smaller tasks
		- carefully evaluating quality of sources
		- adjusting search approaches based on new info 
		- recognising when to focus on depth vs breadth 
## 1.4 Effective agent evals
- traditional evals assume AI follows same steps each time
	- e.g. given input $X$, system should follow path $Y$ to produce output $Z$
	- not applicable to agents 
		- even w identical inputs + starting points, agents can take completely different valid paths to reach their goal 
- because we don't know what right steps are - can't just check if agent followed "correct" steps prescribed in advance
	- **instead need flexible eval methods to judge if agent achieved right outcomes while also following a reasonable process**
- effective eval tips
	- <mark style="background: #FFB8EBA6;">start evaluating immediately w small samples</mark> = early development does not need many samples
		- since many low hanging fruit, a prompt change can give 50% increase in performance
			- hence w effect sizes this large, can spot changes w just a few test cases 
		- best to start w small-scale testing right away w few examples
			- then add more as you develop 
	- <mark style="background: #FFB8EBA6;">LLM-as-judge evals scales when done well</mark> = LLM-judges natural fit for grading outputs 
		- e.g. dimensions used for LLM judges
			- factual accuracy = do claims match sources?
			- citation accuracy = do cited sources match the claims? 
			- completeness = are all requested aspects covered?
			- source quality = did it use primary sources over lower-quality secondary sources?
			- tool efficiency = did it use the right tools a reasonable number of times?
		- experimented w multiple judge setups to eval each component
			- **found single LLM call w single prompt to output scores between 0-1 and a PASS or FAIL grade was most consistent + aligned w human judgements** 
			- this allowed to scalably eval 100s of outputs
	- <mark style="background: #FFB8EBA6;">human eval catches what automated evals miss</mark> = people testing agents find edge cases that evals miss
		- human testers noticed that our early agents consistently chose SEO optimised content farms vs authoritative (but less high ranked) sources like academic PDFs/personal blogs
			- *very similar to what OpenAI found when testing release before Sycophancy problem*
		- adding source quality heuristics to prompts helped resolve this issue 
- success requires understanding interaction patterns between agents
	- not just individual agent behaviour 
## 1.5 Production reliability + engineering challenges
- for agentic systems, minor changes cascade into large behavioural changes
	- makes it difficult to write code for complex agents that must maintain state in a long running process 
- <mark style="background: #FFB8EBA6;">agents are stateful + errors compound</mark> = agents can run for long periods of time, maintaining state across many tool calls 
	- restarts are expensive + frustrating for users, so build such that processes can resume from where errors occured 
	- models can also handle issues gracefully e.g. when tool use fails, letting it adapt - works surprisingly well 
- <mark style="background: #FFB8EBA6;">debugging benefits from new approaches</mark> = debugging is harder due to non-determinism 
	- adding full production tracing lets you diagnose why agents failed + fix systematically 
	- monitor agent decision patterns + interaction structures 
- <mark style="background: #FFB8EBA6;">deployment needs careful coordination</mark> = agent systems are highly stateful webs of prompts, tools + execution logic (that run almost continuously)
	- means whenever we deploy updates, agents might be anywhere in their process - need to prevent code changes from breaking what already works 
	- use rainbow deployments to avoid disruption
		- rainbow deployment = software release strategy that extends blue–green deployments by using multiple, color-labeled environments (“lanes”) 
		- instead of just two, so you can deploy and run many versions in parallel and route traffic selectively to each color
- <mark style="background: #FFB8EBA6;">synchronous (sequential) execution creates bottlenecks</mark> = synchronous programming simplifies coordination but causes bottlenecks in info flow between agents
	- e.g. lead agent can't steer subagents, subagents can't coordinate, entire system can be blocked while waiting for single agent to finish search 
	- async solves for this but adds challenges
		- result coordination 
		- state consistency 
		- error propagation across subagents
## 1.6 Miscellaneous tips for agents
- last mile often becomes most of the journey e.g. pareto principle 
- <mark style="background: #FFB8EBA6;">end-state eval of agents that mutate state over many turns</mark> = agent evals for persistent state across multi-turn convos has challenges
	- e.g. unlike read-only research, each action can change environment for subsequent turns
		- creating dependencies that traditional eval methods struggle with
	- **instead of judging wether agent followed a specific process -> eval wether it achieved the correct final state**
		- for complex workflows, break eval into discrete checkpoints where specific state changes should have occurred 
		- rather than attempting to validate every intermediate step
- <mark style="background: #FFB8EBA6;">long-horizon conversation management</mark> = big multi-turn convos require careful context mgmt strategies
	- necessitates intelligent compression + memory mechanisms 
		- implement patterns where agents summarise completed work phases + store essential info in external memory before proceeding to new tasks 
	- when context limits approach 
		- agents can spawn fresh subagents w clean contexts while maintaining continuity through careful handoffs 
		- can also retrieve stored context (e.g. initial research plan) from memory rather than lose previous work when reaching context limit 
- <mark style="background: #FFB8EBA6;">subagents to a filesystem to minimise "game of telephone"</mark> = some subagent outputs can bypass main lead agent for certain types of results
	- this can improve fidelity + performance
	- rather than communicate everything through lead agent
		- implement artefact systems where specialise agents create outputs that persist independently  
			- e.g. subagent tool calls - store work in external systems, pass lightweight reference back to coordinator 
		- prevents info loss during processing + reduces token overhead (copying large outputs through convo history)
		- works particularly well for structured outputs e.g. code/reports

---

# 2 Mindmap summary


![[Pasted image 20250614133317.png| center | 700]]




