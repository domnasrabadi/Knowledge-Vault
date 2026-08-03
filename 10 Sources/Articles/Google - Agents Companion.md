---
type: article
status: structured
quality:
topics: [ai-agents, agent-evaluation, model-monitoring, rag]
source: ""
created: 2025-05-18
published:
author: ""
flashcards: none
updated: 2025-12-28
---
![[Screenshot 2025-05-18 at 5.55.47 pm.png| center | 400]]

- [[#1 MLOps and AgentOps|1 MLOps and AgentOps]]
- [[#2 Agent Success Metrics|2 Agent Success Metrics]]
- [[#3 Agent Evaluation|3 Agent Evaluation]]
	- [[#3 Agent Evaluation#3.1 Assessing agent capabilities|3.1 Assessing agent capabilities]]
	- [[#3 Agent Evaluation#3.2 Evaluating trajectory and tool use|3.2 Evaluating trajectory and tool use]]
	- [[#3 Agent Evaluation#3.3 Evaluating final response|3.3 Evaluating final response]]
	- [[#3 Agent Evaluation#3.4 Human-in-the-loop (HITL) Evaluation|3.4 Human-in-the-loop (HITL) Evaluation]]
	- [[#3 Agent Evaluation#3.5 Evaluation Summary|3.5 Evaluation Summary]]
- [[#4 Multi-agent Systems|4 Multi-agent Systems]]
	- [[#4 Multi-agent Systems#4.1 Multi-agent architectures|4.1 Multi-agent architectures]]
	- [[#4 Multi-agent Systems#4.2 Multi-agent design patterns|4.2 Multi-agent design patterns]]
	- [[#4 Multi-agent Systems#4.3 Components of Agents|4.3 Components of Agents]]
	- [[#4 Multi-agent Systems#4.4 Challenges in Multi-agent systems|4.4 Challenges in Multi-agent systems]]
	- [[#4 Multi-agent Systems#4.5 Multi-agent evaluation|4.5 Multi-agent evaluation]]
- [[#5 Agentic RAG|5 Agentic RAG]]
- [[#6 Agents as Contractors|6 Agents as Contractors]]
	- [[#6 Agents as Contractors#6.1 Google's Co-Scientist|6.1 Google's Co-Scientist]]


- <mark style="background: #FFB8EBA6;">agent</mark> = application engineered to achieve specific objectives by perceiving its environment and strategically acting upon it using the tools at its disposal
	- fundamental principle of an agent = synthesis of reasoning, logic, and access to external information
	- enabling it to perform tasks and make decisions beyond the inherent capabilities of the underlying model
- architecture of an agent is composed of three essential elements that drive its behavior and decision-making:
	- <span style="color:rgb(255, 0, 247)">Model</span>: pertains to the language model (LM) that functions as the central decision-making unit, employing instruction-based reasoning and logical frameworks
		- model can vary from general-purpose to multimodal, fine-tuned, depending on the agent's specific requirements
	- <span style="color:rgb(255, 0, 247)">Tools</span>: bridge the divide between the agent's internal capabilities and the external world, facilitating interaction with external data and services
		- can include extensions, functions, and data stores
			- extensions bridge the gap between an API and an agent, enabling agents to seamlessly execute APIs
			- functions are self-contained modules of code that accomplish specific tasks
			- data stores provide access to dynamic and up-to-date information, ensuring a model’s responses remain grounded in factuality and relevance
	- <span style="color:rgb(255, 0, 247)">Orchestration layer</span>: dictates how the agent assimilates information, engages in internal reasoning, and leverages that reasoning to inform its subsequent action or decision
		- layer is responsible for maintaining memory, state, reasoning, and planning
		- employs prompt engineering frameworks to steer reasoning and planning, facilitating more effective interaction with the environment and task completion
		- techniques e.g. ReAct, Chain-of-Thought (CoT), and Tree-of-Thoughts (ToT) 

---

# 1 MLOps and AgentOps
- Quality and Reliability are the most cited concerns for deploying to production
	- “*AgentOps*” process is a solution to optimize agent building
- Agent and Operations (<mark style="background: #FFB8EBA6;">AgentOps</mark>) = subcategory of GenAIOps, focuses on the efficient operationalization of agents
	- main additional components include 
		1. internal and external tool management
		2. agent brain prompt (goal, profile, instructions) 
		3. orchestration
		4. memory 
		5. task decomposition
- each system often implements some form of optimization based on metrics 
	- measuring what your system is and isn’t doing
	- measuring the outcomes and business metrics
	- automating the processes for more holistic metrics, and incrementally improving step by step
- <mark style="background: #FFB8EBA6;">Ops</mark> = Machine Learning & Operations 
	- i.e. **combination of people, processes and technology to productionise ML solutions efficiently**
- different types of Ops
	- Development and Operations (<mark style="background: #FFB8EBA6;">DevOps</mark>) 
		- practice of efficiently productionizing deterministic software applications by integrating the elements of people, processes, and technology. DevOps serves as the foundation for all the following terms.
	- Machine Learning Operations (<mark style="background: #FFB8EBA6;">MLOps</mark>) 
		- builds on DevOps, concentrates on the efficient productionization of ML models
		- distinction is that the output of an ML model is non-deterministic and relies on the input data GI-GO 
	- Foundation Model Operations (<mark style="background: #FFB8EBA6;">FMOps</mark>) 
		- builds on MLOps, focuses on the efficient productionization of pre-trained (trained from scratch) or customized (fine-tuned) FMs.
	- Prompt and Operations (<mark style="background: #FFB8EBA6;">PromptOps</mark>) 
		- subcat of GenAIOps, focuses on operationalizing prompts effectively 
		- main additional capabilities include 
			- prompt storage
			- lineage
			- metadata management (including evaluation scores) 
			- a centralized prompt template registry
			- prompt optimizer
	- RAG and Operations (<mark style="background: #FFB8EBA6;">RAGOps</mark>) 
		- subcat of GenAIOps, focuses on efficiently operationalizing RAG solutions
		- primary additional capabilities include 
			- the retrieval process through offline data preparation 
				- (encompassing cleaning, chunking, vectorization, similarity search, and re-ranking) 
			- the generation process through prompt augmentation and grounding.
	- Agent and Operations (<mark style="background: #FFB8EBA6;">AgentOps</mark>) is a 
		- subcat of GenAIOps, focuses on the efficient operationalization of Agents
		- additional components include 
			- internal and external tool management
			- agent brain prompt (goal, profile, instructions) 
			- orchestration
			- memory
			- task decomposition

---

# 2 Agent Success Metrics
- imagine setting up an A/B experiment in production for your new agent 
	- treatment arm gets your new agent and the control arm does not
		- in that scenario, what metrics are you measuring to determine if the treatment arm is doing better? 
		- What metrics are you measuring to determine ROI for the project? 
		- Is it a goal being accomplished, or sales totals, or a set of critical steps in a user journey? 
	- the metrics must be understood, instrumented and easily analyzed + more detail agent evals 
- metrics critical for building, monitoring + comparing revisions of agents
	- business metrics likely out of scope of agent, but should be north star metric for the agents
	- most agents designed around accomplishing goals
		- <mark style="background: #FFB8EBA6;">goal completion rate</mark> = key metric to track 
	- goals can be broken down into few critical tasks or user interactions
		- **each task/interactions should be independently instrumented + measured** 
- each business metric, goal, or critical interaction, will be aggregated in a familiar fashion: 
	- **attempts, successes, rates, etc**
	- **telemetry metrics** also very important to track e.g. latency, errors, etc
	- metrics like these become much more important for agents 
		- can think of them like KPIs for your agent 
		- allow you to have observability in aggregate for higher level perspective of your agents 
- human feedback one of most critical metrics to track
	- simple thumbs up/down or user feedback text can help alot to understand pros/cons
	- feedback can come from customers, employees, QA testers or SMEs reviewing the agent 
- more detailed observability is very important for agents 
	- i.e. seeing + understanding what the agent is doing + why it is doing that 
	- agents can be instrumented with traces to log all inner workings 
		- most useful to use these traces to debug or do manual testing 

---

# 3 Agent Evaluation 
- unlike LLM evals (focus on primary output), agent evals need deeper understanding of decision making process
- agent evals can be broken into 3 components
	- <span style="color:rgb(255, 136, 0)">assessing agent capabilities</span> = eval agent core capabilities e.g. instruction following + reasoning
	- <span style="color:rgb(255, 136, 0)">evaluating trajectory + tool use</span> = analyse steps taken to solution 
		- includes tool choices, strategies and efficiency of approach 
	- <span style="color:rgb(255, 136, 0)">evaluating final response</span> = assessing quality, relevance, correctness of agent final output 
## 3.1 Assessing agent capabilities
- first consider **public agentic benchmarks** - model performance, hallucinations, tool calling + planning 
	- valuable starting point, to assess common failure modes
		- and guide you to setup your own use-case specific eval framework
	- examples = Berkeley Function-Calling Leaderboard (BFCL), $\tau$-Bench, PlanBench and AgentBench
- you want to eval behaviour across variety of scenarios to ensure proper performance
	- i.e. simulating interactions + evaluating how it responds 
	- involves eval-ing the **final response + steps taken (trajectory)**
- curating the eval data is extremely important for accurately representing your agents encounters
## 3.2 Evaluating trajectory and tool use 
- agents perform several actions before responding
	- each eaction is a step on the trajectory 
	- **comparing trajectory you expect to actual taken trajectory is useful** 

![[Screenshot 2025-05-18 at 9.10.54 pm.png| center | 500]]

- 6 ground-truth based trajectory evals 
	- <span style="color:rgb(255, 136, 0)">exact match</span> = agent produces a sequence of actions (trajectory that perfectly mirrors the ideal solution
		- most rigid metric, allowing no deviation from the expected path
	- <span style="color:rgb(255, 136, 0)">in-order match</span> = agent's ability to complete the expected trajectory, accomodates extra, unpenalized actions
		- success = completing core steps in order, flexibility for additional actions
	- <span style="color:rgb(255, 136, 0)">any-order match</span> = same as in-order but no regard for order
		- asks if agent completed all necessary steps, allowing also for extra steps
	- <span style="color:rgb(255, 136, 0)">precision</span> = how many tools calls in predicted trajectory are actually relevant/correct according to reference trajectory
	- <span style="color:rgb(255, 136, 0)">recall</span> = how many of the essential tool calls from reference trajectory are actually captured in predicted trajectory
	- <span style="color:rgb(255, 136, 0)">single-tool use</span> = if specific action is within agent's trajectory 
		- useful for understanding if agent has learned to utilise particular tool yet 
- each metric offers different lens to analyse/debug
	- not all are relevant, i.e. different use cases will prioritise different metrics 
	- limitation of this approach = need reference trajectory (ground truth basd)

![[Screenshot 2025-05-18 at 9.09.20 pm.png| center | 500]]

## 3.3 Evaluating final response 
- final response objective = does your agent achieve its goals? 
	- can define custom success criteria tailored to use case to measure this
	- can also use LLM judge with user-provided criteria - need to be very precise in marking criteria 
## 3.4 Human-in-the-loop (HITL) Evaluation 
- challenges of evals for agents 
	- ⛔️ defining clear objectives
	- ⛔️ designing realistic environments 
	- ⛔️ managing stochastic behaviour 
	- ⛔️ ensuring fairness + bias mitigation 
- hence crucial to incorporate a human-in-the-loop approach alongside the automated evals (metrics + judges) 
	- HITL valuable for tasks needing subjective judgement or creative problem solving 
	- can also be used to calibrate + align automated eval approaches 
- benefits of HITL
	- <span style="color:rgb(0, 176, 80)">subjectivity</span>: Humans can evaluate qualities that are difficult to quantify, such as creativity, common sense, and nuance.
	- <span style="color:rgb(0, 176, 80)">contextual understanding</span>: Human evaluators can consider the broader context of the agent's actions and their implications.
	- <span style="color:rgb(0, 176, 80)">iterative improvement</span>: Human feedback provides valuable insights for refining the agent's behavior and learning process.
	- <span style="color:rgb(0, 176, 80)">evaluating the evaluator</span>: Human feedback can provide a signal to calibrate and refine your autoraters
- HITL methods
	- **direct assessment**: Human experts directly rate or score the agent's performance on specific tasks
	- **comparative evaluation**: Experts compare the agent's performance to that of other agents or your previous iterations
## 3.5 Evaluation Summary  
- challenges to evals for agents
	- hard to find eval data -> bootstrap synthetic data to start
	- LLM judges often prioritse final outcomes instead of reasoning + intermediate actions
		- can miss key insights 
	- complexity over multi-turn interactions
	- multi modal generations - need their own eval methods 
- key trends in agent evals
	- shift towards process-based evaluation - prioritizing the understanding of agent reasoning 
	- increase in AI-assisted evaluation methods for improved scalability 
	- stronger focus on real-world application contexts
	- development of new standardized benchmarks is also gaining traction, facilitating objective comparisons between agents
	- increased emphasis on explainability and interpretability aims to provide deeper insights into agent behavior

| Eval Method       | Pros                                                | Cons                                                         |
| ----------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Human Evaluation  | captures nuanced behaviour, considers human factors | subjective, time-consuming, expensive, difficult to scale    |
| LLM-as-Judge      | scalable, efficient, consistent                     | may overlook intermediate steps, limited by LLM capabilities |
| Automated Metrics | objective, scalable, efficient                      | may not capture full capabilities, susceptible to gaming     |

---

# 4 Multi-agent Systems
- multiple specialised agents collab to achieve more complex objectives
	- each agent = independent entity, it's own LLM, unique context + role 
	- agents must communicate + collaborate to work 
- benefits of multi agents vs single agent
	- <span style="color:rgb(0, 176, 80)">enhanced accuracy</span> - can cross check each others work
	- <span style="color:rgb(0, 176, 80)">improved efficiency</span> - can work in parallel, speed up task completion
	- <span style="color:rgb(0, 176, 80)">better handling of complex tasks</span> - can break down into smaller manageable tasks, each agent focusing on specific aspect 
	- <span style="color:rgb(0, 176, 80)">increased scalability</span> - can scale by adding more specialised agents
	- <span style="color:rgb(0, 176, 80)">improved fault tolerance</span> - if one agent fails, others can take over
	- <span style="color:rgb(0, 176, 80)">reduced hallucinations and bias</span> - can combine multiple perspectives reducing hallucination + bias
## 4.1 Multi-agent architectures
- multi-agent architectures break down problems into distinct tasks
	- so each subtask is handled by specialised agent
		- each agent operates w defined roles, dynamically interacting with others
	- core principles = modularity, collaboration + hierarchy 
- types of agents based on function
	- <mark style="background: #FFB8EBA6;">planner agents</mark> = break down high level objectives into structured sub-tasks 
	- <mark style="background: #FFB8EBA6;">retriever agents</mark> = optimise knowledge acquisition by dynamically fetching relevant data from external sources
	- <mark style="background: #FFB8EBA6;">execution agents</mark> = perform computations, generate responses or interact w APIs
	- <mark style="background: #FFB8EBA6;">evaluator agents</mark> = monitor + validate responses, ensure coherence + alignment to objectives 
## 4.2 Multi-agent design patterns
- <mark style="background: #FFB8EBA6;">sequential</mark> = agents work sequentially, each agent completes task before passing to next
- <mark style="background: #FFB8EBA6;">hierarchical</mark> = structured with "manager" coordinating workflow + delegating to "worker" agents
- <mark style="background: #FFB8EBA6;">collaborative</mark> = agents work collaboratively, share info + resources towards common goal
- <mark style="background: #FFB8EBA6;">competitive</mark> = agents compete w each other to achieve best outcome 
## 4.3 Components of Agents
- <span style="color:rgb(255, 0, 247)">interaction wrapper</span> = interface between agent + environment
	- manages communication + adapts to various input/output modes 
- <span style="color:rgb(255, 0, 247)">memory management</span> = includes short term, long term memory + reflection 
	- short term = necessary for immediate context, cache + sessions 
	- long term storage = for learned patterns, experiences, examples, skills or reference data 
	- reflection = decide which short term items should be copied into long term memory to share across agents, tasks, sessions
		- e.g. user preference -> user profile
- <span style="color:rgb(255, 0, 247)">cognitive functionality</span> = using CoT, ReAct, reasoning, thinking or planning subsystem
	- allows agents to decompose complex tasks into logical steps + engage in self correction 
- <span style="color:rgb(255, 0, 247)">tool integration</span> = ability to utilise external tools 
- <span style="color:rgb(255, 0, 247)">flow/routing</span> = governs connections w other agents
	- facilitating dynamic neighbour discovery, efficient communication with the multi-agent system 
- <span style="color:rgb(255, 0, 247)">feedback loops/RL</span> = enables continuous learning + adaptation 
	- via processing interaction outcomes + refining decision-making strategies
- <span style="color:rgb(255, 0, 247)">agent communication</span> = crucial for success in multi-agents
	- e.g. Agent-to-Agent protocol, OpenAI handoffs vs tool calls etc 
- <span style="color:rgb(255, 0, 247)">agent + tool registry</span> = robust system to discover, register, administer, select and utilise from tools or agents
	- critical is the ontology + description of the tools and agents
		- including their capabilities, requirements + performance metrics 
## 4.4 Challenges in Multi-agent systems
- ⛔️ task communication = agent frameworks today communicate via text, not structured async tasks
- ⛔️ task allocation = efficiently dividing complex tasks
- ⛔️ coordinating reasoning = debating + reasoning together effectively, need sophisticated coordination 
- ⛔️ managing context = keeping track of all info, tasks, conversations between agents
- ⛔️ time and cost = compute + time expensive 
- ⛔️ complexity = system as a whole becomes more complex 
## 4.5 Multi-agent evaluation
- clear progression of single-agent evals vs multi-agent evals
	- i.e. success metrics unchanged, business metric is north star, critical task success metrics + telemetry 
		- can diagnose trajectories of actions through one or all agents
	- for multi-agents, <mark style="background: #FFB8EBA6;">traces</mark> become invaluable to debug + understand what is happening in complex interactions
- for multi-agents, can now drill down + evaluate at every step 
	- e.g. eval each agent in isolation (component-level) and system as a whole (end-to-end)
- multi-agent unique aspects 
	- <mark style="background: #FFB8EBA6;">co-operation + co-ordination</mark> : how well do agents work together + coordinate actions
	- <mark style="background: #FFB8EBA6;">planning + task assignment</mark> : did we come up w right plan, did we stick to it, did any agents deviate or get stuck
	- <mark style="background: #FFB8EBA6;">agent utilisation</mark> : how effectively do agents select other agents + tools, delegate or transfer to user
	- <mark style="background: #FFB8EBA6;">scalability</mark> : does system quality improve w more agents? do we become more efficient or less?

---

# 5 Agentic RAG
- traditional RAG often fails w ambiguous, multi-step or multi-perspective queries 
	- <mark style="background: #FFB8EBA6;">Agentic RAG</mark> adds autonomous agents to actively refine the search via iterative reasoning 
		- <span style="color:rgb(255, 136, 0)">context-aware expansion</span> = instead of single search pass, generate multi query refinements 
		- <span style="color:rgb(255, 136, 0)">multi-step reasoning</span> = decomposes complex queries to smaller logical steps, retrieves info sequentially to build structural response
		- <span style="color:rgb(255, 136, 0)">adaptive source selection</span> = fetches data from various and best suited data sources
		- <span style="color:rgb(255, 136, 0)">validation + correction</span> = evaluator agents cross-check for hallucinations + consistency 

---

# 6 Agents as Contractors
- Google proposes <mark style="background: #FFB8EBA6;">Contracts</mark> - protocol to use agents in high-stakes situations 
- key ideas 
	- standardise + specify contracts between requestor + agents
	- define outcomes as precise as possible 
		- allows for validation against desired outcomes + iterate until achieved 
	- makes possible to negotiate the task
		- including clarifying, refining + filling gaps 
	- defines rules for contractors to generate new subcontracts needed to solve the bigger problem 
- initial contract definition 

| Fields                            | Description                                                                                                                                                                                                                                                 | Required |
|-----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------:|
| **Task/Project description**      | Provide a detailed description of what we expect the contractor to achieve. It should be as specific and as unambiguous as possible.                                                                                                                       | Yes      |
| **Deliverables & Specifications** | Describe precisely the expected outcomes and deliverables from the contractor's task, including a list of specifications clarifying what makes the deliverable acceptable as outcome and details on how to verify that the deliverable is fulfilling the expectation. | Yes      |
| **Scope**                         | Clarify the scope of the tasks that the contractor is responsible for completing, going into separate detail about every aspect of the task. Also used to clarify what is out of scope.                                                                     | No       |
| **Expected Cost**                 | Gives expectation in terms of cost for the task completion. This is usually a function of the complexity of the task combined with what tools will be used.                                                                                                  | Yes      |
| **Expected Duration**             | Gives expectation in terms of duration for the task completion.                                                                                                                                                                                             | Yes      |
| **Input Sources**                 | Specify what input sources can be used and considered to be useful to complete the task.                                                                                                                                                                     | No       |
| **Reporting and Feedback**        | Specifies how the feedback loop should look like: how often we expect updates on the progress, and what mechanism/surface is used to provide feedback (emails, APIs, etc.).                                                                                   | Yes      |

- example data model for iteration between contractors 

| Fields                      | Description                                                                                         | Required |
| --------------------------- | --------------------------------------------------------------------------------------------------- | :------: |
| **Underspecification**      | Highlight aspects that are underspecified or need clarification from the task initiator.            |    No    |
| **Cost negotiation**        | Cost considered too high to complete the task.                                                      |    No    |
| **Risk**                    | Highlights potential risks in fulfilling the contract.                                              |    No    |
| **Additional input needed** | Expresses the kinds of additional data or information that would be useful to fulfill the contract. |    No    |

- contract lifecyle 

![[Screenshot 2025-05-22 at 7.40.32 pm.png| center | 500]]



## 6.1 Google's Co-Scientist 
- similar to AlphaFold, CoScientist employes "generate - debate - evolve" approach 
	- draws inspiration from scientific method 
		- 1. generates diverse hypotheses 
		- 2. critically evaluates their potential
		- 3. refines them through ongoing feedback + analysis 
- components of CoScientist 
	- <span style="color:rgb(255, 136, 0)">data processing agents</span> = aggregate + structure large volumes of experiment data
	- <span style="color:rgb(255, 136, 0)">hypothesis generators</span> = propose potential explanations based on existing research + new findings 
	- <span style="color:rgb(255, 136, 0)">validation agents</span> = run simulations + verify results before presenting to researchers
	- <span style="color:rgb(255, 136, 0)">collaboration agents</span> = communicate findings across different research teams, enhance cooperation 