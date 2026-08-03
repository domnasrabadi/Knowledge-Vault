---
type: book
status: distilled
quality: 1
topics: [ai-agents, agent-evaluation, model-monitoring]
source: ""
created: 2025-12-15
published:
author: ""
flashcards: none
updated: 2025-12-29
---
# Intro to Agents
- key benefits of agents
	- interpret context and make decisions dynamically w/o explicit programming
	- navigate situations, dynamically plan, use tools
- scripts vs workflows vs chatbots vs agents
	- 4 key factors
		- variability of inputs
		- reasoning
		- performance/compliance needs
		- maintenance burden
	- <mark style="background: #ADCCFFA6;">simple code</mark> → fixed, deterministic transformations
	- <mark style="background: #ADCCFFA6;">deterministic workflow</mark> → handful of known branches, explicit error handling
	- <mark style="background: #ADCCFFA6;">chatbot/RAG</mark> → natural language, corpus QA
	- <mark style="background: #ADCCFFA6;">agents</mark> → high variability, reasoning, planning
- agentic or autonomy spectrum 
	- manual → ask → agentic
	- choose level of autonomy based on control, trust, overheads etc
- Anthropic definition of an "agent" → characterised by retrieval, tools, memory

![[Screenshot 2025-05-22 at 5.56.42 pm.png| center | 400]]

# Designing Agent Systems
- 4 core components to agent systems
	- <mark style="background: #ADCCFFA6;">model</mark>
		- model choice depends on performance vs cost + latency 
		- can also finetune for specialised domains 
	- <mark style="background: #ADCCFFA6;">tools</mark>
		- functional building blocks, give ability to execute tasks + interact w other systems
		- agent effectiveness = range + sophistication of tools
		- tools should be self contained + easy to replace/extend
	- <mark style="background: #ADCCFFA6;">memory</mark>
		- short term memory = spans task or conversation 
		- long term memory = store knowledge + experiences over time, for personalisation or learning
		- memory mgmt - organising & indexing for retrieval, needs to filter for relevant vs irrelevant
	- <mark style="background: #ADCCFFA6;">orchestration</mark> 
		- composes + sequences skills into workflows given an objective
		- evaluates tools, paths, forecasts outcomes + selects best path
		- monitors progress, assesses outcomes, reroutes or updates plans as needed
- architecture design patterns
	- <mark style="background: #ADCCFFA6;">single agent</mark>
		- simplest, single agent hands all, easy to deploy and avoids coordination complexity
		- best for narrow & well defined tasks
	- <mark style="background: #ADCCFFA6;">multi-agent</mark>
		- agents collaborate, run async, coordinate
		- improved specialisation, scalability, redundancy
		- however more overhead - communication, coordination, complexity 
- 3 pillars of best practices, designing agents
	- <mark style="background: #BBFABBA6;">iterative design</mark>
		- build small prototypes first, refine them iteratively 
		- allows you to find errors early, make it user-centric, scale as you grow
	- <mark style="background: #BBFABBA6;">evaluation strategy</mark> (perform various types of evals)
		- **functional testing** = verify correctness of each skill/component/feature
		- **boundary testing** = stress testing w edge cases, unusual inputs
		- **task specific metrics** = domain accuracy & compliance
		- **user feedback metrics** 
			- **explicit feedback** = thumbs up/down, star ratings, accept-reject-modify results
			- **implicit feedback** = via interactions in logs → misinterpretations, delay, sentiment, corrections and text feedback
		- **human-in-the-loop testing** = experts review outputs for correctness, compliance etc 
	- <mark style="background: #BBFABBA6;">real-world testing</mark> 
		- eval in environments close to real-world settings, incorporate the following:
			- phased rollouts + pilots before full deployment
			- use continuous monitoring e.g. KPIs like response time, accuracy, satisfaction
			- collect user feedback to refine the design for usability + reliability 
			- iteratively improve using feedback into the development cycle

---

# User experience in Agentic systems
- principles for well-designed agentic experiences
	- durable even as tech evolves
	- empowers users & confidence
	- reduces frustration, clarifies capabilities + limitations
- UX should expose autonomy being adjustable
	- manual → assist → autonomous
	- 4 types of modalities → includes text, graphical interface, speech + voice, video 
- sync vs async 
	- synchronous = real time, back and forth
	- asynchronous = intermittent & independent exchanges 
	- async design principles
		- optimise for flexibility, persistence
		- communicate task status clearly via notifications, summaries, structured reports
		- retain historical context across long gaps
		- set expectations → timelines, progress indicators, follow ups 

![[Screenshot 2025-12-19 at 12.39.08 pm.png| center | 500]]

- consider memory usage 
	- for UX → continuity of conversations, personalisation, better intelligence
	- how to maintain state across interactions?
		- track history, intent, next steps + handoffs
		- use short term + persistent state
	- personalisation & adaptability 
		- learn from prior exchanges to give more relevant responses
		- <mark style="background: #ADCCFFA6;">preference retention</mark> = retain settings or common choices 
		- <mark style="background: #ADCCFFA6;">behavioural adaptation</mark> = adjust tone & flow to user patterns
		- <mark style="background: #ADCCFFA6;">proactive assistance</mark> = anticipate needs, suggest next steps
- feature discoverability → users must understand the agent's capabilities 
	- <span style="color:rgb(62, 143, 249)">suggest queries or offer alternatives for users</span>
		- progressively disclose more advances features contextually based on conversations
	- <span style="color:rgb(62, 143, 249)">communicate uncertainty</span> 
		- using visual cues (icons, meters, colours) or behaviours (suggestive vs assertive)
	- <span style="color:rgb(62, 143, 249)">ask for guidance from the user</span>
		- ask clarifying questions instead of guessing → impossible to perfectly interpret ambiguity
		- ensure follow up Qs are focused & help refine understanding
	- <span style="color:rgb(62, 143, 249)">fail gracefully</span> 
		- acknowledge fails, be transparent, explain briefly and propose next steps
		- anticipate common failures w fallbacks
		- preserve state to avoid losing work, log and analyse failures to improve

---

# Tool use
- <mark style="background: #FFB8EBA6;">tools</mark> = specific capability/actions agent can use to achieve an outcome
	- tools should be modular → developed, tested, optimised independently 
	- then integrated into the system for more complex behaviour 
- tool types
	- <mark style="background: #ADCCFFA6;">local tools</mark> = run locally, based on rules, tailored to specific tasks
		- augment the model weaknesses (math, times/dates)
		- metadata is key! model uses this to choose which + how tools are used
		- common errors + mitigations
			- avoiding wrong tool calls → use precise, narrow scope names
			- avoiding overlapping tool use → write clear + distinct descriptions
			- avoid tool misfires → define strict input/output schemas
	- <mark style="background: #ADCCFFA6;">API-based tools</mark>
		- allow agents to interact w external services → databases, integrations, heavy compute
		- access tools (*fetch info*) vs operation tools (*act on info*) → e.g. read vs write
	- <mark style="background: #ADCCFFA6;">plugin tools</mark> 
		- standard tools from providers, good since added at model-layer, more reliable
		- e.g. Langchain tools, MCP tools etc
	- <mark style="background: #ADCCFFA6;">stateful tools</mark> 
		- tools that retain info between uses or modify environment in permanent way 
			- file systems, local scripts, external APIs → warning: can be destructive
		- mitigations
			- principle of least power = grant minimal permissions, guard ops w boundaries + oversight
			- ensure ops are narrowly scoped → e.g. user specific SQL queries
			- ensure read-only ops barred from modify/delete ops
			- ensure strict sanitisation + access controls 
- use AI to help write tools
	- feed API specs + examples to AI → to generate wrappers + helpers
	- iteratively refine the tools → give them narrow scope & make them testable
		- come up with the unit tests for each too (possibly using mock data)
- modes for tool-use
	- `auto` = model decides tool calls, generally the default option
	- `any/required` = forced to use 1 or more tools, when they are essential
	- `none` = blocks tool calls e.g. controlled outputs or for testing
	- always add fallbacks + post processing logic 
		- after response (post processing): 
			- check tool invocation
			- check valid JSON
			- check runtime success
		- corrective flows
			- missing or invalid fields → use schema validation like `jsonschema` or `pydantic`
			- it tools are skipped → trigger automatically or force
			- if JSON invalid → prompt engineering + schema
			- runtime/transient errors → use exponential backoff
		- graceful fallbacks can include:
			- switching models
			- clarifying questions
			- using cached responses
			- or reverting to safe defaults e.g. human
- make sure to log everything → makes debugging possible
	- prompts, tool calls, errors, retries, fallbacks etc 
	- validation + fallbacks convert random failures into predictable prod-grade behaviour

---

# Orchestration
- <mark style="background: #FFB8EBA6;">orchestration</mark> = constructing the right context for effective/grounded responses
	- incorporates planning, memory & retrieval, dynamic context assembly 
	- ultimate goal is to properly sequence workflows
- types of agents (each has distinct approaches + impacts to perf/capabilities/cost)

| Agent type                      | Core idea                                                                            | Best for                                                         | Strengths                                                                | Trade-offs / Risks                                                          | Use when…                                                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **Reflex**                      | Direct input → action rules (no memory or planning).                                 | Keyword routing, lookups, simple UI automations, guards.         | Fastest latency, deterministic, cheap, easy to verify.                   | No multi-step reasoning; brittle outside known triggers.                    | You need millisecond responses and fixed behaviours; the action is obvious given the input. |
| **ReAct**                       | Loop: reason → act (tool) → observe → repeat.                                        | Troubleshooting, dynamic analysis, multi-source data pulls.      | Transparent step-by-step reasoning; adaptable; auditable traces.         | Higher latency and API cost; can meander without constraints.               | The path isn’t known up-front and you want visible tool/think steps. Add caps/timeouts.     |
| **Planner–Executor**            | Plan once (often with a bigger model), then execute sub-steps (smaller model/tools). | Projects with clear end states and repeatable sub-tasks.         | Decomposes work, easier to debug; cost control by splitting plan vs. do. | Plan may go stale; needs schema for tasks/dependencies.                     | You can outline the steps before doing; you want predictable runs across similar jobs.      |
| **Query-Decomposition**         | Break a question into sub-questions; answer + synthesise (“self-ask with search”).   | Fact-finding, QA over external knowledge, citations.             | Fine-grained grounding; parallelisable; traceable evidence.              | Can over-split; synthesis quality varies with sub-answer quality.           | You need defensible answers with sources; queries map cleanly to sub-queries.               |
| **Reflection (ReAct + critic)** | Adds meta-review to catch errors, re-plan, and reinforce good tactics.               | High-stakes or irreversible actions; compliance-sensitive flows. | Error recovery; quality lift without human in the loop.                  | Extra tokens/time; risk of loops without guardrails.                        | You need “second-look” safety before committing changes/spend.                              |
| **Deep Research**               | Orchestrates plan → decompose → ReAct → reflect → synthesize into living report.     | Open-ended investigations, literature reviews, competitor intel. | Handles long horizons; adaptive; highly auditable outputs.               | Highest cost/latency; sensitive to tool/data quality; needs robust retries. | You’re doing multi-day/multi-source research that must evolve and be reviewed.              |

- agent type considerations
	- latency vs control
		- Reflex < ReAct < Planner–Executor < Reflection < Deep Research
	- cost management
		- for planning → use large models
		- for execution → use smaller models
		- for ReAct/Reflection agents → cap number of times they run
		- cache sub-answers for Query-Decomposition
	- reliability
		- add timeouts, workflow step limits and success criteria
		- log tool inputs/outputs for audits
		- use retries w backoff
		- validate pre-commit steps in Reflection/DR agents
	- common hybrids 
		- *Planner-Executor + ReAct* = plan workflow, allow adaptive ReAct within each task
		- *Query-Decomp + Reflection* = decompose for grounding, critic re-checks synthesis + citations
		- *Reflex front-door/router* = fast path obvious cases, fallback to ReAct/Planner for mismatches
- how to select tools (3 broad options)
	- <mark style="background: #ADCCFFA6;">standard tool selection</mark> 
		- provide tool definitions, model chooses best tool
		- some tips
			- use concise tool names
			- give one sentence summary on tool's purpose
			- example invocations w inputs + outputs
			- specify input constraints (types, ranges), reduce ambiguity
			- iterate w test prompts + refine descriptions
	- <mark style="background: #ADCCFFA6;">semantic tool selection</mark> 
		- similar to RAG vector search
			- embed tool name/description → store in vector DB
			- embed context at runtime → retrieve top-k tools → pass to model for choice
		- much more scalable for large tool sets
	- <mark style="background: #ADCCFFA6;">hierarchical tool selection</mark> 
		- group tools + add group descriptions
		- model picks a group, then within the group for best tool
		- improves accuracy, but increases latency/complexity 
	- tradeoffs between 3 options (standard vs semantic vs hierarchical tool selection)
		- standard → simplest, but scales poorly
		- semantic → scalable + low latency, but poorer performance (semantic collisions)
		- hierarchical → scalable, but slower
- executing tools 
	- best practice is to define & validate parameters before execution 
		- use parser to check data types
		- instruct the model to correct on validation fails
- tool topologies 
	- <mark style="background: #FFB8EBA6;">topology</mark> = shape of the workflow, how tool calls are arranged, ordered & connected
		- e.g. single tool execution = query → model selects a tool → receives tool output → composes response
	- 3 main topologies
		- <mark style="background: #ADCCFFA6;">parallel tool execution</mark> = multiple actions on same input
			1. retrieve candidate tools 
			2. a second model filters the tools
			3. parameterise + execute independently
			4. aggregate & formulate response
		- <mark style="background: #ADCCFFA6;">chained tool execution</mark> = sequential workflow
			- tip = plan dependencies carefully & cap the chain length
				- need to balance efficiency w compounding errors 
			- can also loop with reasoning → model observes results & decides
		- <mark style="background: #ADCCFFA6;">graphs</mark> = non-linear workflows w branching & merging
			- tool calls are `nodes`, transitions are `edges`
			- consolidate branches w shared nodes e.g. summarisation
			- flexible but more overhead due to LLM calls + risk of cycles
				- sketch topology first → nodes, transitions, merge points
- context engineering 
	- most important thing for orchestration → assembling the right info at each step
	- <mark style="background: #FFB8EBA6;">context engineering</mark> = deciding **what** to include + how to **structure** it + how to fit it **efficiently**
	- typical inputs for managing within context 
		1. *user query*
		2. *retrieved chunks*
		3. *summaries of past dialogues*
		4. *system instructions*
		5. *workflow state/context*
	- best practices 
		- conserve tokens, keep just the information needed
			- trim context to remove irrelevant tokens
			- summarise context to retain relevant tokens
		- partition context across multiple agents (if needed)
		- assemble context dynamically at each step to match the goal
- orchestration best practices
	- balance latency & accuracy tradeoff
	- estimate the average action count → complexity will inform your planning method
	- gauge adaptability needed
		- for high adaptability, use incremental replanning
	- create representative test cases to compare planning approaches 
	- pick the simplest approach that works (Ockham's Razor)

---

# Knowledge & Memory 
- knowledge vs memory 
	- <mark style="background: #FFB8EBA6;">knowledge</mark> = factual or domain content injected at generation time (outside model weights)
	- <mark style="background: #FFB8EBA6;">memory</mark> = agent's history (exchanges, tool I/O, state updates), continuous and informs decisions
- memory, context windows & context engineering
	- memory enables context engineering
		- memory stores information → while context engineering assembles the right pieces
	- managing context windows
		- context window = info passed into an LLM call (1 token $\approx$ $\frac{3}{4}$ word)
		- rolling context window approach (FIFO) = eject oldest, keep most recent
- foundational memory approaches 
	- <mark style="background: #ADCCFFA6;">traditional keyword search</mark> 
		- fast lookup, ranked w BM25
		- good for precise keyword matches
		- poor as it misses paraphrases, higher level themes or abstractions
	- <mark style="background: #ADCCFFA6;">semantic search & RAG</mark>
		- retrieves using meaning (using embeddings) not exact text matches
			1. embed documents/context into embeddings
			2. embed query
			3. search nearest neighbour vectors + retrieve top-k
			4. inject into context
			5. augment the generated response w fetched evidence
	- <mark style="background: #ADCCFFA6;">semantic experience memory</mark> 
		- solves problem of blank-slate conversations + long tasks w dropping context
			1. embed each input → search prior interactions
			2. reserve context space for top matches
			3. add system message, latest input + recent turns
		- enables personalisation + adaptation using accumulated experiences
- <mark style="background: #ADCCFFA6;">GraphRAG</mark> (advanced method 1)
	- extends RAG w knowledge graphs to capture relationships + dependencies for better retrieval/synthesis
		- knowledge graph = nodes (entities) & edges (relationships) - optimised for multi-hop queries
		- retrieval system = queries graph to extract right subgraphs/clusters
		- LLM synthesises retrieved subgraphs into coherent responses
		- process involves collecting & preprocessing data → entity recognition + extract relationships → design ontology → populate graph 
	- how GraphRAG solves RAG weaknesses
		- connects dots across many docs 
		- identifies higher level themes & concepts across docs
		- better on long context? e.g. large, messy or narrative datasets 
	- challenges + tradeoffs
		- hybrid RAG still outperforms on long enterprise tasks
		- maintenance complexity + resource intensive
- <mark style="background: #ADCCFFA6;">Note-Taking approach</mark> (advanced method 2)
	- technique to improve RAG (2023 Nvidia paper) by prompting model to take margin notes on context first
		1. model generates notes based on the context
		2. model generates a note on the question
		3. model responds based on both
	- distinct from COT → emphasises structured self notes interleaved w context

![[Screenshot 2025-09-07 at 11.48.51 am.png| center | 500]]


---

# Learning in Agentic systems
- 2 types of learning
	- <mark style="background: #FFB8EBA6;">nonparametric</mark> learning = no change to model weights
	- <mark style="background: #FFB8EBA6;">parametric</mark> learning = updates model weights (fine-tuning)
- non-parametric learning
	- <mark style="background: #ADCCFFA6;">Few-shot (exemplar) learning</mark>
		- involves using successful previous examples as demonstrations in prompts
	- <mark style="background: #ADCCFFA6;">Dynamic few-shot prompting</mark>
		- retrieve most relevant examples from VecDB at inference
		- not all examples are equal or fit → select most relevant
	- <mark style="background: #ADCCFFA6;">Case-based reasoning</mark>
		- build a memory bank of `context`, `actions`, `outcomes` & `feedback`
		- retrieve similar past cases & adapt their solutions
	- <mark style="background: #ADCCFFA6;">Reflexion</mark>
		- after failures, agent writes reflections on what went wrong + how to improve
			1. perform actions 
			2. log trial (actions, observations, outcome) to persistent storage
			3. generate reflection into a concise plan
			4. update memory w the new reflection
			5. inject reflections into next attempt by prepending into prompt
		- reflections live in memory buffer alongside actions + observations
		- reflection prompt - ask model to re-plan based on a failed task
	- <mark style="background: #ADCCFFA6;">Experiential learning</mark>
		- extends exemplar learning by aggregating insights & rules across many experiences
			- ultimately to improve policy → maintains a living ruleset as evidence changes
			- operations = `AGREE`, `REMOVE`, `EDIT`, `ADD`
- parametric learning
	- <mark style="background: #ADCCFFA6;">fine-tuning & SFT</mark>
		- goal of FT = tailor general models to a specific domain/task while keeping broad capabilities
			- used for domain specialisation, consistent styling + formatting, precise tool calling
			- avoid when prototyping, usually as advanced option 
		- SFT precisely steers behaviours e.g. tool-calling (when, how, recovery from errors)
			- lowers error rates, improves judgement on scenarios + reduces token wastage
			- can also use reasoning `<think>` within `<tool_call>`
		- minimal SFT pattern
			1. preprocess conversations into chat templates w special tokens
			2. apply LORA for target adaptation
			3. train on `prompt, response` pairs w SFT trainer
	- <mark style="background: #ADCCFFA6;">SLMs</mark>
		- smaller models for fast + small compute constraints + well-defined narrow tasks
		- can outperform large models on bounded tasks + quicker
		- may need more frequent retrains
	- <mark style="background: #ADCCFFA6;">DPO</mark>
		- direct preference optimisation → train on ranked pairs, model learns to prefer higher quality outputs
			- complements SFT & aligns w nuanced human preferences
	- <mark style="background: #ADCCFFA6;">RL w verifiable rewards</mark>
		- optimises against explicit & measurable reward functions
			- measurable reward functions like automated metrics, rule-based validators, scoring models, human evaluators 
		- pros = flexible objectives, generalise via value prediction, scalable 
			- most effective when ranked preference data or reliable scoring is available

![[Screenshot 2025-12-20 at 2.11.24 pm.png| center | 400]]


---

# Multi-agent systems (MAS)
- single to multi-agents
	- MAS can become necessary as number of tools + size of problem space grows 
	- always start simple, then add complexity if it meaningfully improves performance
- single agents
	- best for modest task difficulty, small toolsets, low complexity, latency requirements
	- benefits: simpler to build + maintain, faster to respond
	- challenges begin with larger toolsets (~16+ tools)
		- system prompt then needs to enumerate various capabilities → can confuse the model → suboptimal choices
	- optimise before moving to MAS via hierarchical + semantic tool selection 
- multi-agents (MAS)
	- MAS = involves multiple agents collaborating on a task together
		- useful for complex tasks, larger toolsets, parallelism needs, dynamic environments
		- can have specialised agents, overcomes single agent overflow problem
	- <mark style="background: #FFB8EBA6;">swarms</mark> = type of MAS, decentralised & self-organising groups of simple agents w local rules
		- can have emergent intelligence from interactions → when centralised control is not needed
		- ✅ pros: scales to hundreds/thousands, many redundancies, highly flexible
			- good for distributed problem solving (exploration, monitoring, consensus, search)
		- ⛔ cons: less predictable, less observable/explainable, possibly less efficient
- principles when adding more agents
	- task decomposition: decompose & simplify responsibilities
	- specialisation: align agent roles to specific tasks, improve speed + performance 
	- parsimony: add minimum necessary agents, each adds comms + coordination overhead
	- coordination: need robust way to communicate, share info + resolve conflicts
	- robustness: design for resilience, fault tolerance & redundancy
	- efficiency: weigh up tradeoffs - functionality vs compute/coordination costs
- type of coordination (for multi-agents)
	- <mark style="background: #ADCCFFA6;">democratic coordination</mark> 
		- core idea: peer to peer consensus, no central controller
		- ✅ strengths: resilient to single agent failure, flexible and adaptable, encourages diverse ideas
		- ⛔️ trade offs: high communication overhead, slower convergence, needs strong conflict resolution
		- use when: 
			- resilience and fairness matter more than speed
			- heterogeneous experts must collaborate without a boss
		- tips: 
			- cap rounds and time 
			- use structured ballots and scoring 
			- add tie break protocols 
			- log rationales for audit
	- <mark style="background: #ADCCFFA6;">manager coordination</mark> 
		- core idea: a manager agent assigns tasks, integrates results, resolves conflicts
		- ✅ strengths: faster decisions, clear ownership, reduced duplicate work, simpler communication paths
		- ⛔️ trade offs: single failure/bias point, throughput bottleneck at manager, less adaptable to surprises
		- use when: 
			- you need velocity and clarity 
			- workloads map well to top down tasking like support, ops, triage
		- tips: 
			- add manager redundancy and failover 
			- rate limit the manager 
			- define SLAs and escalation rules
	- <mark style="background: #ADCCFFA6;">hierarchical coordination</mark> 
		- core idea: multi tier structure where upper layers plan and route, lower layers execute with local autonomy
		- ✅ strengths: scales to many agents, fault tolerance via layers, clear authority and handoffs
		- ⛔️ trade offs: design and ops complexity, latency across layers, upstream delays can stall downstream action
		- use when: large multi domain programs need global strategy with local execution like supply chains or multi market research
		- tips: define interfaces and okrs per layer, share cached context downward, monitor per layer kpis and queue health
	- <mark style="background: #ADCCFFA6;">actor-critic</mark> (coordination by evaluation)
		- core idea: actor proposes plans or outputs, critic evaluates against rubrics, iterate to acceptance
		- ✅ strengths: quality improves via iterative feedback, transparent criteria like correctness, completeness, tone, risk
		- ⛔️ trade offs: extra inference cycles increase cost and latency, rubric quality becomes a hard dependency
		- use when: 
			- generative or fuzzy tasks where one shot fails
			- quality is worth extra compute such as reports, code review, policy
		- tips: 
			- freeze rubrics
			- cap review rounds
			- diversify critics with heuristics and models 
			- require evidence and citations where applicable
	- considerations between the 4 options 
		- throughput + latency speed ranking: 
			- (FAST) manager → hierarchical → democratic → actor–critic (SLOW)
		- failure modes: 
			- manager overload or bias
			- democratic deadlock
			- hierarchical queueing delays
			- critic overfitting to rubric
		- mitigations: 
			- limit step numbers
			- quorum and tie break rules
			- backpressure and queues
			- partial results with timeouts
			- redundancy for managers and critics
		- observability: 
			- log proposals, votes, assignments, critiques, attach confidence and risk scores
			- track KPIs like time-to-decision, revision count, error rate
		- consider hybrid approaches

![[Screenshot 2025-09-08 at 8.58.18 am.png| center | 500]]

- designing for redundancy 
	- idea = intentionally building additional ways to achieve something, so system still works when parts fail
		- e.g. rocket science → they use triple-redundant flight computers, engine-out capabilities etc
		- for agents it can be: extra agents, duplicate/similar planning, overlapping paths
	- failure modes & design targets → dictate the redundancy method(s) you use
		- <mark style="background: #FFB8EBA6;">failure modes</mark>: bad plans or tool choices, timeouts, hallucinations & inconsistencies, model biases
		- <mark style="background: #FFB8EBA6;">design targets</mark>: availability (uptime); correctness/performance; latency budget; failure tolerance
	- types of redundancies
		- <span style="color:rgb(62, 143, 249)">agent redundancy</span> = more agents than strictly needed, others can pickup failures
		- <span style="color:rgb(62, 143, 249)">functional redundancy</span> = different ways to do the same job e.g. multiple planning approaches
		- <span style="color:rgb(62, 143, 249)">information redundancy</span> = multiple tools or data sources to use, replicating the state
		- <span style="color:rgb(62, 143, 249)">temporal redundancy</span> = retries, 2nd passes, incremental planning or re-planning
		- <span style="color:rgb(62, 143, 249)">communication redundancy</span> = alternate channels or topologies, so no 1 link causes failure
	- using adjudication or voting
		- use when you expect some noise or occasional failures and want one trusted decision from many
		- <mark style="background: #ADCCFFA6;">run-many-and-vote</mark>: run multiple copies, take majority answer
			- try use at least 3 voters
	    - <mark style="background: #ADCCFFA6;">agree-to-accept</mark>: start many, accept the result once a chosen number agree or pass tests (best for verifiable tasks)
	    - <mark style="background: #ADCCFFA6;">weighted votes</mark>: give more influence to workers with stronger past accuracy or trusted models
	- continuity & shared state fails
		- useful for keeping system working even when a key agent fails or agents disagree/conflict
		- scenarios when it is useful:
			- manager or router fails & can't afford downtime
			- when agents write to same resource & cannot overwrite/duplicate (e.g. task list, memory, DB)
		- <mark style="background: #ADCCFFA6;">primary with backup</mark> (hot/warm/cold)
		    - when one agent is the dispatcher or API gateway and is a single point of failure
		    - mitigates: downtime, stuck pipelines, missed SLAs
		    - idea: a standby automatically takes over if health checks fail
		- <mark style="background: #ADCCFFA6;">leader election</mark>
		    - when any peer can coordinate but there must be exactly one coordinator at a time
		    - mitigates: deadlock, “multiple leaders” chaos, split-brain control
		    - idea: peers agree on a temporary leader after a failure, then proceed
		- <mark style="background: #ADCCFFA6;">quorum/consensus</mark>
		    - when many agents read/write a shared queue, memory, or database
		    - mitigates: lost updates, conflicting writes, race conditions, split-brain state
		    - idea: only approve state changes after majority agreement, partial or stale nodes can’t corrupt truth
		- <mark style="background: #ADCCFFA6;">supermajority checks</mark> for untrusted/malicious peers
		    - when some workers may be adversarial, low-quality, or non-deterministic
		    - mitigates: poisoned outputs, coordinated bad votes, subtle corruption
		    - idea: require larger agreement and cross-checks before accepting a result
		- <mark style="background: #ADCCFFA6;">readiness levels</mark> (hot/warm/cold backups)
		    - when you need predictable takeover times after failure
		    - mitigates: long recovery windows, data loss during failover
		    - idea: keep backups pre-loaded to shorten or bound recovery time
- communication & interaction patterns
	- become increasingly critical as number of agents/tools/complexity grows 
		- local communication vs distributed communication 
			- local = direct tool calls, sharing memory or DB → simplest but least scalable
			- distributed = ???
	- A2A protocol by Google (distributed example)
		- standard to discover, collaborate, exchange structured requests between agents
		- using agent cards, registry & handshakes
	- other interaction patterns
		- routing/workflows
			- simplest, involves tight coupling of agent functionality + handoffs, hand crafted usually
		- pub/sub for async messaging
			- decouples sender from receivers, more loosely coupled, independent scaling
		- actor frameworks
			- stateful agents that handle messages 1-at-a-time to avoid races
			- use when many concurrent agents need isolated state + safe updates
		- orchestration & workflow engines
			- for running multi-step jobs w built-in retries, timeouts, dependencies & recovery
			- used for long running or multi-tool processes, that need durable & auditable outcomes
	- managing state & persistence
		- MAS need to manage shared state, agent memory, task metadata
			- need to ensure workflows are durable → resilient to step failures, checkpoint progress + state
		- memory approaches
			- episodic = short-lived, task-specific, in-context
			- semantic = long-term, across interactions, persistent storage w search + indexing

---

# Evaluating Agents
- why evals
	- building rigourous evals == long term dividends + agility
		- requires defining clear objectives, relevant metrics, employing systematic processes
	- without evals:
		- making decisions to ship features becomes harder
		- impossible to know if changes improve the system
		- impossible to know performance in realistic & adversarial scenarios
		- cannot guard against regression or find bugs before production
- measurement & metrics
	- effective measurement
		- starts w clear + actionable metrics → align w goals/requirements of the system
		- requires representative examples to measure against
	- metrics
		- provide benchmarks to iterate against, need to reflect realistic demands of the system
		- should encompass both qualitative + quantitative factors
			- <span style="color:rgb(62, 143, 249)">accuracy or task success</span> = did agent complete intended task completely?
			- <span style="color:rgb(62, 143, 249)">latency or throughput</span> = responsiveness under realistic loads
				- track percentiles e.g. P50, P95, P99
			- <span style="color:rgb(62, 143, 249)">reliability or robustness</span> = behaviour under noisy inputs, outages & edge cases
			- <span style="color:rgb(62, 143, 249)">precision & recall</span> = missing or over-triggering specific behaviours (e.g. tool use)
			- <span style="color:rgb(62, 143, 249)">user satisfaction</span> (quant + qual) = ratings, complaints, acceptance/edits of outputs
		- try to automate & aggregate scoring across many scenarios → allows for scaling
			- beware traditional exact-match metrics → often miss real utility, good outputs come in many forms
- evals in the development loop
	- crucial to incorporate evals into all stages of agent development
		- trigger automated offline evals for new code merges or model updates
		- eval sets should expand with scope of the system e.g. new test cases for new tools/orchestration
	- automated evals don't tell the whole story 
		- esp. in high-stakes/novel domains, need regular sampling + human review for subtle issues + qual measure
	- why we need to continuously curate/extend evals
		- allows us to assess legacy vs new features
		- ensures system still progressing on key objectives/goals → better UX ultimately
- evaluation datasets
	- **high-quality eval sets** = living spec for what agent system must handle, foundational to measuring performance
		- high-quality = reflects diversity, ambiguity, edge-cases the system will face in production
			- static/manual test suites often insufficient → risk overfitting, miss long-tail failure modes, don't scale w changes
		- supports reproducibility + regression detection as system grows
			- via tracking historical performance after changes or improvements
		- start w exhaustive enumeration of use-cases + possible pathways
			- encompassing not just typical/happy-path, but rare/adversarial/malformed scenarios that can reveal hidden assumptions or brittle components
	- a good eval set
		- <span style="color:rgb(62, 143, 249)">should define both input state + expected outcomes</span>
			- allows for automated validation (ground-truth) testing
		- <span style="color:rgb(62, 143, 249)">examples should be in a structured format</span>
			- with input state, conversation history, expected final state
		- <span style="color:rgb(62, 143, 249)">should include many examples</span>
			- enough of the distribution + edge-cases to give comfort & probability of how often it goes wrong
		- <span style="color:rgb(62, 143, 249)">should test multiple aspects</span> 
			- e.g. multi-turn, multi-input, consider conversation context, relevant + grounded responses
		- <span style="color:rgb(62, 143, 249)">should include metadata</span>
			- for downstream failure analysis e.g. failure type tagging or coverage tracking
- methods for creating eval examples
	1. <span style="color:rgb(62, 143, 249)">manually by SMEs</span>
	2. <span style="color:rgb(62, 143, 249)">mined from historical data or production logs/traces</span>
	3. <span style="color:rgb(62, 143, 249)">synthetically generated w LLMs</span>
- creating synthetic eval examples w LLMs
	- try to leverage sample/real seed data 
	- add variations → introduce ambiguity, inject rare idioms, mutate working examples to edge cases
	- have SMEs review and refine before adding to final test set 
	- apply targeted generation techniques
		- adversarial prompting = *"Find a user message that causes the agent to contradict itself"*
		- counterfactual editing = *"Change one word in the prompt and see if the agent fails"*
		- distributional interpolation = *"Blend two intents to create a deliberately ambiguous request"*

- component-level vs end-to-end evaluation 
	- similar to unit testing vs integration testing in SWE
	- <mark style="background: #FFB8EBA6;">component testing</mark> = validating individual components of the agentic system
		- effective unit tests = ensure each part of the system works as intended
		- contributes to overall reliability & performance of the system + sub-agents
	- <mark style="background: #FFB8EBA6;">end-to-end testing</mark> = validate ability to perform complete realistic tasks start-to-finish
		- requires full-stack of representative workflows + user journeys
			- e.g. perception, planning, tool use, communication, exception paths
	- tips + cautions on end-to-end testing
		- automated tests only as good as their eval datasets + metrics
		- narrow or edge cases can pass evals but fail in production
		- treat evals as a living process, not a static checklist
		- regularly expand & refine test sets - reflect new features, real user behaviour or emerging failure modes
		- incorporate feedback from SMEs + pilot users to identify blind spots

- <mark style="background: #ADCCFFA6;">tool-use evals</mark>
	- mature tool evals define suite of tests for all tools *(or combination of tools)*
		- e.g. data retrieval tool → test across data formats, network conditions, various data sources
	- <span style="color:rgb(62, 143, 249)">checks & tests</span>:
		- tools are *(almost)* always deterministic → identical inputs should give identical outputs
			- deterministic tests + classification metrics (precision, recall, F1) can be used
			- e.g. tool recall, tool precision, parameter accuracy
			- for stochastic tools → check output's statistical properties
		- for external calling tools (APIs, SQL queries) → use mock data or simulators
			- reproduce edge cases, rare but catastrophic potential consequences
		- regression testing is critical → full suite of tool evals should run for each tool change
			- to verify capabilities haven't broken 

- <mark style="background: #ADCCFFA6;">planning + orchestration evals</mark>
	- <mark style="background: #FFB8EBA6;">planning</mark> = translating goals/objectives into actionable sequence of steps
		- might involve sequencing tool calls, coordinating conditionals, stopping based on environment output
		- can be related to tool-use → planner may be the one invoking the tools
			- depends on segragation of duties
			- <span style="color:rgb(62, 143, 249)">tool recall</span> = did planner include all expected tool invocations?
			- <span style="color:rgb(62, 143, 249)">tool precision</span> = did it avoid calling tools that were unnecessary? 
			- <span style="color:rgb(62, 143, 249)">parameter accuracy</span> = for each tool, did it supply the correct args?
	- <span style="color:rgb(62, 143, 249)">start with canonical workflows</span>
		- canonical workflows = common, well understood user intents + gold responses (golden QA pairs)
			- this corpus should grow over time + more complex for full range of pathways/actions
			- becomes backbone for e2e testing too
		- for each scenario, encode:
			1. starting environment
			2. conversation history
			3. expected outcomes (tool usage + responses)
		- for systematic plan evals, run agent e2e + extract actions
			- capture tool invocations, tool arguments, responses
			- then compare against ground truth expectations
	- <span style="color:rgb(62, 143, 249)">edge cases for planning</span>
		- extended multi-turn, multiple intents/items, out-of-scope intents/items, ambiguity, contradiction
		- should test if agent can recover from intermediate failures
	- <span style="color:rgb(62, 143, 249)">consistency of planning</span>
		- for deterministic cases → same outputs for same inputs
		- for probabilistic cases → range of plans should fall within expected bounds
		- check for:
			- reproducibility 
			- sensitivity to small input changes
			- graceful handling of unexpected conditions (missing fields, failed tool calls)

- <mark style="background: #ADCCFFA6;">memory evals</mark>
	- <mark style="background: #FFB8EBA6;">memory</mark> → needed for continuity & contextual awareness (multi-turn, long running tasks, persistent user profiles)
	- <span style="color:rgb(62, 143, 249)">correctness tests for memory</span>
		- verify correct data written, stored and retrievable
		- test immediately + over time, sessions, various actions too
		- test boundary cases
			- maximum capacity or context
			- unusual data types
			- rapid read & write cycles
			- stress with malformed, duplicate or ambiguous entries
	- <span style="color:rgb(62, 143, 249)">relevance tests for memory</span>
		- shouldn't surface stale/old/irrelevant info
		- confirm outdated/incorrect preferences aren't returned → indicates data leakage or indexing errors
		- avoid retrieval of irrelevant but similar data → indicates superficial similarity 
	- <span style="color:rgb(62, 143, 249)">resilience tests for memory</span>
		- simulate:
			- database unavaibility
			- data corruption
			- version migrations
		- verify graceful recovery or controlled failures (ideally minimising user impact)

- <mark style="background: #ADCCFFA6;">learning evals</mark> 
	- learning is hardest to test (stochastic + data dependent)
	- <span style="color:rgb(62, 143, 249)">checks & tests</span>:
		- basic test = verify agent updates parameters/cache/rules based on responses or feedback
			- for SFT, verify accuracy & loss change over training & can generalise
		- generalisation & adaptability tests
			- evaluation novel or OOD scenarios → challenges brittle heuristics or memorised responses
				- use holdout sets, synthetic data, adversarial cases
			- simulate distribution shifts 
				- e.g. new user inputs, unseen tool failures, changing objectives
			- for SFT, confirm no catastrophic forgetting

- overall eval dimensions
	- <mark style="background: #ADCCFFA6;">consistency</mark>
		- idea: 
			- outputs align with inputs & remain coherent over extended turns & address questions/tasks reliably
			- even despite model's nondeterminism
		- <span style="color:rgb(62, 143, 249)">checks & tests</span>:
			- validate responses stay aligned w diverse scenario inputs
			- assess relevance + accuracy → directly addresses user query, detect deviations
			- cross check outputs against conversation context → flag inconsistencies
			- assess logical progression for long running MT convos
			- assess contradictions or topic straying for long running MT convos
		- risks & human review
			- automated evals can do well on test distribution but miss rare edge cases
			- ongoing manual inspection & periodic eval refreshes are key
				- humans should asses nuanced inconsistencies 
		- using LLM judges
			- can be very useful for checking consistency/relevance → use few-shot examples
			- combine LLM judges, rationale & human feedback for proper detection + remediation
	- <mark style="background: #ADCCFFA6;">coherence</mark>
		- idea:
			- ensure outputs are logical & contextually relevant for an interaction
		- <span style="color:rgb(62, 143, 249)">checks & tests</span>:
			- retain & properly use context → responses should build on context (esp. in MT)
				- e.g. user preferences & previous actions/responses
				- user shouldn't have to repeat themselves
			- simulate extended interactions → verify consistent understanding of workflow state
			- assess contradictions or lapses → like conflicting recommendations or missed dependencies
			- assess professional + clear tone → for customer facing agents
	- <mark style="background: #ADCCFFA6;">hallucinations & groundedness</mark>
		- outputs should be grounded & verifiable, using trusted sources not fabrications
			- output reliability is tied to quality of data sources for the agent
				- should be accurate, relevant and up-to-date
			- outdated, incomplete or poorly vetted sources increase erroneous information
		- regular audits & feedback
			- regularly sign-off knowledge base + busines process to maintain standards
			- monitor responses for groundedness triggers → review and correct w SMEs
			- more advanced check is to identify/categorise discrepancies & trigger updates to KB/model
	- <mark style="background: #ADCCFFA6;">robustness</mark>
		- idea:
			- real-world environments are unpredictable & agents must handle various or malicious inputs
			- agents should gracefully fail → ask clarifying Qs, decline or escalate as appropriate
		- <span style="color:rgb(62, 143, 249)">checks & tests</span>:
			- intentionally supply inputs OOD/assumptions → weird data formats, slang & typos, API fails
			- systematic adversarial variations → cover random fuzzy variants + systematic exploration
				- via historical fails or adversarial SMEs
			- check reproducibility
				- e.g. rerun 3–5 times; failure rate > 80% indicates systematic bug to fix
				- for irreproducible runs, quantify the confidence/variance

- moving from development to production
	- establish clear performance baselines & thresholds → using proper & representative evals
	- document & use structured checklists for component evals
		- e.g. planning, memory, learning, tools, integration → should all be rigourously tested & reviewed
	- use gating mechanisms for deployments
		- automated or manual checks to promote to prod if all requirements satisfied
- evals & governance
	- the product is the model, the tools, the logic, the fallbacks, the infra etc
		- ownership is shared by more than just the data scientists → RACI matrix

| Metric/Activity                                  | Product team                                                        | ML engineers                                                       | Infra/SRE team                                                     |
| ------------------------------------------------ | ------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **Latency** (e.g., planning or tool call delays) | **A** (Owns user impact) / **C** (Consults on UX thresholds)        | **R** (Optimizes prompts/models) / **I** (Informed on regressions) | **R** (Monitors infra causes) / **C** (Consults on scaling)        |
| **Hallucination rates**                          | **C** (Provides user feedback context) / **I** (Informed on trends) | **A/R** (Owns detection/mitigation via evals)                      | **I** (Informed for alerting setup)                                |
| **Task success rate**                            | **A** (Owns product goals) / **R** (Defines success criteria)       | **C** (Consults on model improvements)                             | **I** (Informed for system reliability ties)                       |
| **Token usage/cost**                             | **C** (Consults on business impact)                                 | **R** (Optimizes generations) / **I** (Informed on spikes)         | **A** (Owns budgeting/scaling) / **R** (Monitors infra efficiency) |
| **Distribution shifts** (e.g., input drift)      | **I** (Informed for product adjustments)                            | **A/R** (Detects via embeddings/evals)                             | **C** (Consults on data pipeline stability)                        |
| **Fallback/Retry frequency**                     | **C** (Consults on UX fallbacks)                                    | **R** (Refines planning logic)                                     | **A** (Owns reliability) / **I** (Informed on patterns)            |
| **User feedback/sentiment**                      | **A/R** (Owns aggregation and prioritization)                       | **C** (Consults on model ties)                                     | **I** (Informed for ops alerts)                                    |
| **Dashboard maintenance & triage rituals**       | **C** (Provides product context)                                    | **C** (Provides ML insights)                                       | **A/R** (Owns platform and cross-team reviews)                     |


---

# Monitoring 
- why monitoring 
	- real challenges begin once agents operate in dynamic, high-stake & unpredictable environments
		- unlike normal software → rely on probabilistic models, chained tools, unbounded user inputs
			- observability is absolutely essential
		- the best agentic systems improve over time w feedback
			- successful cases *(& traces)* should become golden eval examples
			- likewise production failures should become tests cases → become regression tests
	- metrics & instrumentation needs thoughtful scope
		- too many logs/alerts/metrics → too noisy; too little → makes debugging hard/slow
- examples of monitoring metrics 
	- <mark style="background: #ADCCFFA6;">infrastructure related</mark>
		- <span style="color:rgb(62, 143, 249)">CPU/memory usage</span> → monitor system health and scaling pressure
		- <span style="color:rgb(62, 143, 249)">uptime/availability</span> → track service availability and failure recovery
		- <span style="color:rgb(62, 143, 249)">request latency (p50, p95, p99)</span> → ensure responsiveness under load
	- <mark style="background: #ADCCFFA6;">workflow related</mark>
		- <span style="color:rgb(62, 143, 249)">task success rate</span> → determine how often agents complete intended workflows
		- <span style="color:rgb(62, 143, 249)">token usage</span> → measure token consumption at the workflow level
		- <span style="color:rgb(62, 143, 249)">tool call success/failure rate</span> → detect degraded integrations or misuse of tools
		- <span style="color:rgb(62, 143, 249)">tool use rate limit exceeded</span> → track tool calls surpassing predefined limits within periods
		- <span style="color:rgb(62, 143, 249)">request distributions for KB or vector DB</span> → identify most/least common docs/data sources
		- <span style="color:rgb(62, 143, 249)">retry frequency</span> → identify instability or flakiness in plans or tools
		- <span style="color:rgb(62, 143, 249)">fallback frequency</span> → surface failures in primary workflows
	- <mark style="background: #ADCCFFA6;">output quality related</mark>
		- <span style="color:rgb(62, 143, 249)">token usage (input/output)</span> → track verbosity, cost, and generation efficiency
		- <span style="color:rgb(62, 143, 249)">hallucination rates</span> → measure semantic accuracy of generations
		- <span style="color:rgb(62, 143, 249)">embedding drift from baseline</span> → detect distribution shifts in user inputs or task framing
	- <mark style="background: #ADCCFFA6;">user feedback related</mark>
		- <span style="color:rgb(62, 143, 249)">requery/rephrasing rate</span> → measure whether users are understood on the first try
		- <span style="color:rgb(62, 143, 249)">task abandonement rate</span> → identify workflows that confuse or frustrate users
		- <span style="color:rgb(62, 143, 249)">explicit ratings</span> (👍🏼, 👎🏼) → collect qualitative assessments of system helpfulness
- debugging & mitigations 
	- questions to ask when debugging possible errors
		- *Was the user's intent understood?* 
		- *Was the right tool selected?* 
		- *Did the system produce hallucinated content?* 
		- *Did the user abandon the task halfway through?*
	- mitigations may include:
		- tweaking agent prompts (pruning, more examples, extra context) or retraining SLMs
		- adjusting planning logic
		- modifying tool composition
		- guardrail modifications 
		- tuning semantic caching
		- modifying retry logic
		- adjust step caps or retry limits
		- improving escalation process or logic 
		- improving intent classification or simplifying workflows
		- changes to LLM judges

- distribution shifts & drift 
	- <mark style="background: #FFB8EBA6;">drift</mark> = when statistical properties of the agent's environment change over time
		- e.g. evolving user language, new products, API changes, foundation model updates
		- shifts may not trigger actual errors, may show as:
			- degraded performance, irrelevant or ungrounded responses, higher fallback/escalation rates
		- dashboard + metrics (like above) can show early signals
- quantitative metrics for drift 
	- general idea = compare distributions of input features or outputs
	- <span style="color:rgb(62, 143, 249)">Model or agent behavior monitors</span> (downstream drift proxies)
		- what they do: track output score distributions e.g. relevance, pass@k, tool call mix, error codes
		- use when: you need practical impact signals alongside input drift
			- inputs: time-bucketed metrics for baseline vs current
			- outputs: deltas, control-chart signals, KL/JS over score buckets
		- interpretation: sustained shifts beyond control limits → investigate upstream data or policies
	- <span style="color:rgb(62, 143, 249)">Kolmogorov–Smirnov (KS) test</span>
		- what it does: compares ECDFs of two samples; flags if they likely come from different distributions
		- use when: continuous features with unknown shape (e.g., query length, latency, numeric scores)
			- inputs: two numeric samples (historical vs current)
			- outputs: KS statistic (max vertical ECDF gap), p-value
		- interpretation: common heuristic KS > 0.1 with p < 0.05 → meaningful shift; adjust for sample size
	- <span style="color:rgb(62, 143, 249)">Kullback–Leibler (KL) divergence</span>
		- what it does: measures how much the current probability distribution diverges from a baseline
		- use when: token/term frequencies, tool/type frequencies, binned numerics where direction matters
			- inputs: two discrete distributions $P$ (baseline), $Q$ (current) as probabilities with $\epsilon$-smoothing
			- outputs: scalar ≥ 0 (0 = identical; larger = more drift)
		- interpretation: higher $D_{\mathrm{KL}}$ = more drift; 
			- rule of thumb $D_{\mathrm{KL}}>0.2\text{–}0.5$ → investigate (tune to your data)
	- <span style="color:rgb(62, 143, 249)">Jensen–Shannon (JS) divergence</span>
		- what it does: symmetric, bounded version of KL via midpoint averaging
		- use when: you want a stable, comparable 0–1-like drift score for discrete distributions
			- inputs: two discrete probability distributions 
			- outputs: scalar in $[0, \log_2]$ but often normalized to $[0, 1]$
		- interpretation: closer to $0$ → stable; example alert $\mathrm{JS}>0.15$
	- <span style="color:rgb(62, 143, 249)">Population Stability Index (PSI)</span>
		- what it does: compares binned category/continuous distributions 
			- via $\sum (\text{actual \%} - \text{expected \%}) \cdot \ln!\big(\tfrac{\text{actual \%}}{\text{expected \%}}\big)$
		- use when: categorical features (route/tool types) or binned continuous features
			- suitable for agent invocation frequencies → e.g. tool use categories `"refund"`, `"cancel"` etc
			- inputs: expected% (baseline) vs actual% (current) per bin
			- outputs: scalar ≥ 0
		- interpretation: < 0.1 stable; 0.1–0.25 minor drift (monitor); > 0.25 major drift (intervene)
			- note: quality depends on binning; keep bins stable over time
	- <span style="color:rgb(62, 143, 249)">Cosine similarity of embeddings</span>
		- what it does: compares current text/query vectors to baseline to detect semantic or topic drift
		- use when: language or intent semantics may shift (new jargon, intents)
			- inputs: embedding vectors for baseline vs current (per item or aggregated centroids)
			- outputs: similarity in $[-1, 1]$ (often $[0, 1]$)
		- interpretation: drop in mean similarity or larger centroid shift beyond thresh (e.g., $> 3\sigma$) → drift
			- notes: monitor both center shift (centroid distance) and spread (variance)
	- <span style="color:rgb(62, 143, 249)">Wasserstein (earth mover’s) distance</span>
		- what it does: measures the “work” to morph one continuous distribution into another
		- use when: you care about magnitude and direction of numeric shifts (e.g., cost, latency)
			- inputs: two numeric samples
			- outputs: non-negative distance in feature units
		- interpretation: larger distance = more drift; set feature-specific thresholds (e.g., $0.2 \times$ baseline std)
	- <span style="color:rgb(62, 143, 249)">Chi-square test for independence</span> (categorical alternative)
		- what it does: tests if category frequencies changed beyond chance
		- use when: purely categorical features with adequate counts per cell
			- inputs: contingency table of counts (baseline vs current)
			- outputs: $\chi^2$ statistic, p-value
		- interpretation: small $p$ → distribution changed; pair with effect size to gauge impact
- implementation & interpretation tips
	- compare recent window (e.g. last $24$–$48$ h) to baseline (prior $2$–$4$ weeks same day/hour)
	- minimum counts: enforce $n_{\min}$ per bin/cell; merge sparse categories before testing
	- alerting heuristics (examples):
	    - $\text{KS} > 0.1$ and $p < 0.05$ → warn; $\text{KS} > 0.2$ → alert
	    - $\mathrm{PSI} > 0.25$ for $\ge 2$ consecutive windows → trigger mitigation
	    - mean embedding similarity drops $> 3\sigma$ from baseline → alert
	    - $\mathrm{JS} > 0.15$ over intent buckets for $24$ h → review routing
	- responding to shifts (use realtime observability + feedback loops)
		- transient spikes → change thresholds, widen bounds or adapt parsing logic
		- persistent drift → retrain, refresh prompts/tools, or re-bin features
		- validate fixes via A/B or backtesting

- monitoring stack & instrumentation 
	- observability should capture range of metrics (see above) from infra to model performance
		- but also metrics for drift/shift in inputs or outputs
		- use alerts to find regressions/anomalies in real time
	- example dashboard can show:
		- token usage per agent, per hour → to detect model verbosity regressions
		- p95 latency → for tool calls + planning regressions
		- task success rate → sliced by workflow or prompt template version
		- fallback frequency → sliced by tool or sub-agent
		- drift indicators → based on embedding sim. of queries over time

- deployment patterns 
	- <span style="color:rgb(62, 143, 249)">shadow deployment</span>
		- mirrors live traffic to a new model/service in the background, shows user current model though
		- use when: you want real-world signal on a candidate without user risk or side effects
	- <span style="color:rgb(62, 143, 249)">AB testing</span>
		- randomly splits traffic into groups and exposes each group to a different variant for causal measurement
	- <span style="color:rgb(62, 143, 249)">canary release</span> (or ramp-up pilot)
		- rolls out a new version to a small percentage or a safe segment first, then ramps if healthy
		- use when: production safety is critical and you need early warning before full rollout
	- <span style="color:rgb(62, 143, 249)">interleaving experiments</span>
		- for ranking/search, mixes two systems’ results into one list per query and infers the better system from user interactions
	- <span style="color:rgb(62, 143, 249)">bandits</span>
		- adaptively allocates traffic to better-performing variants while still exploring alternatives
		- use when: environment changes, you want to maximize reward during testing, or traffic is scarce

![[Screenshot 2025-12-29 at 1.44.14 pm.png| center | 500]]

- other monitoring patterns & tips 
	- regression trace collection 
		- use production failures (bad tool calls, ungrounded responses) into new test cases
		- once fixed, it should pass these test cases → over time strengthening our eval sets w real-world cases
	- self healing agents
		- monitoring not just for detecting fails, but allowing agents to heal from it
		- via having agents read their own telemetry 
	- user feedback as an observability signal
		- feedback in 2 forms; explicit vs implict → both give signals to use in monitoring
			- e.g. implicit: users rephrasing inputs, abandoning tasks, hesitating during interactions
			- e.g. explicit: thumbs-down icon, star rating, free-text comment
		- user feedback can drive improvement loops
			- e.g. traces with low user ratings exported directly to evaluation set for post hoc review
			- e.g. if multiple users abandon a specific flow, revisit planning strategy or tweak prompts

---

# Feedback Loops
- failures are inevitable (dynamic world, diverse users, changing data sources)
	- continuous improvement therefore necessary & follows a cycle
		1. feedback pipelines to diagnose issues
			- failures need to be observed, understood & categorised to be actionable
		2. experiments to validate changes
			- pipelines need automated analysis + HITL review to extract meaningful insights
		3. learning to consolidate gains 
			- proposed improvements need to be validated in controlled deployments (shadow, canary, AB etc)
	- requires more than just DS/engineering
		- also needs systems for documenting insights & prioritising fixes
- feedback pipelines
	- core function = systematically identify recurring issues in agentic system
		- automated pipelines are essential due to immense volume + complexity (not without risks though)
		- leverages a combination of rule-based triggers, anomaly detection algorithms and clustering 
	- clustering failures
		- can be very useful to have an LLM judge assign failure labels/categories to first understand types
		- or using embedding models and then clustering to identify common failure types + volumes
		- other ML techniques to detect subtle trends can also be employed
			- e.g. gradual drifts in agent decision patterns
			- e.g. correlations between user inputs + downstream failures
	- feedback loops can surface issues like:
		- ⛔️ ambiguous instructions leading to inconsistent or irrelevant responses
		- ⛔️ overly broad prompts causing hallucination or off-task outputs
		- ⛔️ rigid, narrow prompts failing to generalise to real-world variability
		- ⛔️ lack of clarity around task boundaries, escalation, or error handling
		- ⛔️ incorrect or suboptimal tool selection for a given user task
		- ⛔️ parameter mismatches or malformed inputs to tool calls
		- ⛔️ toolset gaps e.g. tasks the agent cannot accomplish due to missing or incomplete tools
		- ⛔️ tool chaining failures where output of a step is not properly formatted for the next
	- effective root cause analysis
		- <span style="color:rgb(62, 143, 249)">workflow tracing</span> = reconstruct e2e agent plans, tool calls, user inputs leading to fail
		- <span style="color:rgb(62, 143, 249)">localise faults</span> = isolate the component (prompt, tool etc) responsible
		- <span style="color:rgb(62, 143, 249)">recognise patterns</span> = identify if isolated or part of recurring trend
			- could be linked to cohorts of input queries, data inputs or system states
		- <span style="color:rgb(62, 143, 249)">impact assessment</span> = evaluate frequency + severity of issue to determine priority
- automatic prompt optimisation
	- allow for backprop of text-based feedback directly into:
		- system prompts
		- tools + skills parameters
		- reasoning + planning strategies
	- can involve tightening wording, adjusting constraints or reordering reasoning steps
		- e.g. tools like GEPA, DSPy and Tracex
	- however limited since they cannot fully understand nuances or broader strategy 
		- need human oversight to review, validate and approve or override recommendations
- HITL review
	- certain cases need human intuition, contextual judgement & domain expertise
		- e.g. ambiguous user intents, conflicting goals or novel edge cases
	- HITL complements automated pipelines & root cause analysis → so they remain effective + aligned
		- automated pipelines can flag incidents & route to SME review
		- escalation criteria can include
			- when monitoring thresholds are breached
			- anomalies or failures in high-value workflows or regulatory implications
			- persistent errors w no technical explanation
			- conflicting recommendations
		- HITL review should prioritise most uncertain or consequential outcomes
			- e.g. high uncertainty in agent responses or response logits, high variance in ensemble/voting, LLM judge rubric

![[Screenshot 2025-10-26 at 3.27.05 pm.png| center | 600]]

- the value of HITL data
	- review process typically involves:
		1. analyse context = reproduce failure in controlled environment, understand sequence & decisions causing 
		2. inspect traces = examine logs/traces and decisions to see how agent interpreted intent & actions
		3. impact assessment = eval scope & severity, consider technical + UX aspects
		4. resolution plan = recommend targeted interventions (prompt fix, workflow design, new tools or features)
	- effective HITL protocols need documentation & reproducibility to resolve future incidents + track systemic issues
		- includes: decisions to be logged, rationales captured, outcomes tracked
	- each reviewed case becomes an example for an evolving KB 
		- can be used in evals, documentation or reasoning bank
- prompt & tool refinement
	- <mark style="background: #FFB8EBA6;">prompts + tools</mark> = most impactful + direct levers to an agentic system
		- prompts = the instructions & context to the agents
		- tools = the functions, data & APIs the agent can use
	- form the bridge between user intent & the agent's actions
		- subtle word/structure/context changes → can dramatically impact interpretation, reasoning & responses
	- refinement & improvement options
		- prompts
			- <span style="color:rgb(62, 143, 249)">clarity rewrite</span> = more explicit instructions, reduce ambiguity, specify formatting
			- <span style="color:rgb(62, 143, 249)">add examples</span> = provide positive & negative examples to anchor
			- <span style="color:rgb(62, 143, 249)">decompose tasks</span> = split into smaller steps, break up into sequential prompts/reasoning
			- <span style="color:rgb(62, 143, 249)">expand/refine context</span> = incorporate more context or constraints
		- tools
			- <span style="color:rgb(62, 143, 249)">refine logic</span> = optimise agent prompts & the tool descriptions, args etc
			- <span style="color:rgb(62, 143, 249)">expand tools</span> = enhance tools to cover more situations
			- <span style="color:rgb(62, 143, 249)">improve integration</span> = ensure tool outputs are reliable & actionable
	- prompt/tool refinements should be documented
		- allow traceability + repeatability & audit log of what works & why → should include:
			- clear rationale of what the problem was
			- what was the change made
			- how effectiveness will be measured
		- refinments should be validated w offline evals + controlled deployments 
- aggregating & prioritising improvements
	- helps avoid noise overwhelm, low impact fixes or missing broader systemic issues
	- aggregation 
		- collect from dashboard, tracing, issue trackers → collate into coherent backlog
		- dedupe (cluster), tag & categorise, link to context + data
	- prioritisation 
		- balance dimensions like 
			- frequency of issue
			- severity or impact
			- feasibility of fix 
			- strategy, recurrence & risk
- continuous learning
	- = system adapts, improves over time based on real world use & feedback
	- 2 mechanisms
		- <mark style="background: #FFB8EBA6;">in-context learning</mark>
			- fastest + most flexible way of adaptation 
				- often used for testing or 1st attempt before later methods
			- by embedding examples, reasoning steps or new context into prompts → agents learn on fly
		- <mark style="background: #FFB8EBA6;">online learning</mark>
			- draws on accumulated batches of data → structured & periodic approach
				- more durable & scalable but higher resources/cost
			- curate data → update model → validate

---

# Agent Security 
- unique risks for agentic systems
	- goal misalignment (may interpret objectives differently)
	- probabilistic reasoning (unintended behaviours)
	- dynamic adaptation (hard to predict/control, sensitive to input changes)
	- limited visibility (due to complex + large data they produce & use)
	- HITL vulnerabilities → automation bias, alert fatigure, skill decay, misaligned incentives
- defences to jailbreaking + prompt injection
	- <span style="color:rgb(62, 143, 249)">clear escalation paths & alerting</span> → get SME review when needed
	- <span style="color:rgb(62, 143, 249)">input sanitsation & validation</span> → filter attack patterns, enforce syntax, reject bad queries
	- <span style="color:rgb(62, 143, 249)">stronger prompting</span> → instruction anchoring, templates, govern input interpretation
	- <span style="color:rgb(62, 143, 249)">operational defences</span> → authentication, rate limits, logging & tracing, guardrails
	- <span style="color:rgb(62, 143, 249)">data minimisation</span> → least privilege
	- <span style="color:rgb(62, 143, 249)">pseudo/masking</span> → obscure identifiers 
	- <span style="color:rgb(62, 143, 249)">environment isolation</span> → sandboxing + containerise
	- <span style="color:rgb(62, 143, 249)">fallback + fail-safe mechanisms</span> → graceful degradation, escalate or manual workflows, trigger alerts 
- red teaming 
	- essential to understand vulnerabilities (via simulation) & build resilience 
		- attack → evaluate → mitigate → harden 
	- using LLMs for red-teaming
		- can help create synthetic adversarial datasets for testing robustness
			- anamolous patterns, noisy inputs, biased distribution, OOD examples
		- combine these w human creativity for nuanced vulnerabilities 

![[Screenshot 2025-10-26 at 4.42.00 pm.png| center | 500]]



---

# Humans & Agents Collaboration
- human role gradually changing over time
	- progression = executor → reviewer → collaborator → governor 
	- in mature workflows, humans collaborate in real time 
		- by sharing context, guiding priorities & refining outputs 
- progression of human involvement 
	- <span style="color:rgb(62, 143, 249)">executor</span> → human forms tasks, reviews outputs, tight feedback
	- <span style="color:rgb(62, 143, 249)">reviewer</span> → human checks key outputs, agent handles more routine work
	- <span style="color:rgb(62, 143, 249)">collaborator</span> → human guides priorities, annotates jointly, shares planning
	- <span style="color:rgb(62, 143, 249)">governor</span> → human sets policy & audits decisions, oversees escalation
- agentic systems scope + governance needs + risk ratings
	- personal → user-managed preferences, optional explainability, minimal oversight
		- <mark style="background: #FFF3A3A6;">low risk</mark>
	- team → shared memory boundaries, peer escalation, calibration of trust
		- <mark style="background: #FFB86CA6;">medium risk</mark>
	- project → cross functional visibility, logging, conflict resolution mechanisms
		- <mark style="background: #FFB86CA6;">medium risk</mark>
	- functional → role based access control, audit logs, compliance alignment
		- <mark style="background: #FF5582A6;">high risk</mark>
	- enterprise → multi-tier signoff, governance committee review, ongoing audits + monitoring
		- <mark style="background: #FF5582A6;">high risk</mark>
- traceability & logging 
	- helps reconstruct behaviours in specific scenarios 
		- why was this action/outcome performed?
		- what data influenced this decision? 
		- what external factors (API fails, bad instructions) were involved?
	- logging & traceability 1st class
		- <span style="color:rgb(62, 143, 249)">decision logs</span> → inputs, intermediate reasoning, outputs, rationale
		- <span style="color:rgb(62, 143, 249)">user interaction logs</span> → user inputs, agent responses, timestamps 
		- <span style="color:rgb(62, 143, 249)">error & failure logs</span> → when/why tasks failed, if outputs were unintended