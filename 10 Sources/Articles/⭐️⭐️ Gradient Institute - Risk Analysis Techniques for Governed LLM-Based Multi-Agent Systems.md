---
type: article
status: structured
quality: 1
topics: [multi-agent-systems, llm-risks, agent-evaluation]
source: ""
created: 2025-08-02
published:
author: ""
flashcards: none
updated: 2026-07-18
---
![[Screenshot 2025-08-04 at 1.44.24 pm.png| center | 400]]

- [[#1 Metadata|1 Metadata]]
- [[#2 Executive Summary|2 Executive Summary]]
- [[#3 Introduction|3 Introduction]]
- [[#4 Foundations and Frameworks of LLM-Based Multi-Agent Systems|4 Foundations and Frameworks of LLM-Based Multi-Agent Systems]]
	- [[#4 Foundations and Frameworks of LLM-Based Multi-Agent Systems#4.1 Single agents & LLM Workflows|4.1 Single agents & LLM Workflows]]
	- [[#4 Foundations and Frameworks of LLM-Based Multi-Agent Systems#4.2 Multi-agent settings|4.2 Multi-agent settings]]
- [[#5 Failure Modes in Governed Multi-agent Systems|5 Failure Modes in Governed Multi-agent Systems]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.1 How MAS Failure modes are different|5.1 How MAS Failure modes are different]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.2 Failure Mode 1: Cascading Reliability Failures|5.2 Failure Mode 1: Cascading Reliability Failures]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.3 Failure Mode 2: Inter-agent communication failures|5.3 Failure Mode 2: Inter-agent communication failures]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.4 Failure Mode 3: Monoculture collapse|5.4 Failure Mode 3: Monoculture collapse]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.5 Failure Mode 4: Conformity bias|5.5 Failure Mode 4: Conformity bias]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.6 Failure Mode 5: Deficient theory of mind|5.6 Failure Mode 5: Deficient theory of mind]]
	- [[#5 Failure Modes in Governed Multi-agent Systems#5.7 Failure Mode 6: Mixed motive dynamics|5.7 Failure Mode 6: Mixed motive dynamics]]
- [[#6 Risk Analysis Techniques|6 Risk Analysis Techniques]]
	- [[#6 Risk Analysis Techniques#6.1 Risk Analysis Toolkit|6.1 Risk Analysis Toolkit]]
		- [[#6.1 Risk Analysis Toolkit#6.1.1 Simulations|6.1.1 Simulations]]
		- [[#6.1 Risk Analysis Toolkit#6.1.2 Observational Data|6.1.2 Observational Data]]
		- [[#6.1 Risk Analysis Toolkit#6.1.3 Benchmarking against Baselines|6.1.3 Benchmarking against Baselines]]
		- [[#6.1 Risk Analysis Toolkit#6.1.4 Red-teaming|6.1.4 Red-teaming]]
		- [[#6.1 Risk Analysis Toolkit#6.1.5 Capability benchmarking|6.1.5 Capability benchmarking]]
	- [[#6 Risk Analysis Techniques#6.2 Using the toolkit for analysing MAS failure modes|6.2 Using the toolkit for analysing MAS failure modes]]
- [[#7 Discussion & Conclusion|7 Discussion & Conclusion]]
	- [[#7 Discussion & Conclusion#7.1 Human-AI Interaction Consideration|7.1 Human-AI Interaction Consideration]]
	- [[#7 Discussion & Conclusion#7.2 Assessing Impacts|7.2 Assessing Impacts]]
	- [[#7 Discussion & Conclusion#7.3 General Risk Mitigation Principles|7.3 General Risk Mitigation Principles]]
	- [[#7 Discussion & Conclusion#7.4 Summary of insights|7.4 Summary of insights]]


---

# 1 Metadata
- Author: Alistair Reid, Simon O'Callaghan, Liam Carroll, Tiberio Caetano
- Category: pdf
- URL: https://readwise.io/reader/document_raw_content/345175054

# 2 Executive Summary
- AI agent adoption = organisations start to adopt AI agents to automate complex tasks
    - deployments evolving from single agents to multi-agent systems
- multi-agent systems = networks of AI agents that interact to accomplish complex tasks
    - fundamentally transform the risk landscape rather than simply adding to it
- emergent behaviours = system behaviours that arise from interactions among LLM agents, not from individual components
    - collection of safe agents does not guarantee a safe multi-agent system
- six key failure modes ⛔️
    - <mark style="background: #FF5582A6;">cascading reliability failures</mark> = manifest when agents’ erratic competence and brittle generalisation failures are propagated and reinforced across the network
    - <mark style="background: #FF5582A6;">inter-agent communication failures</mark> = involve misinterpretation, information loss, or conversational loops that derail task completion
    - <mark style="background: #FF5582A6;">monoculture collapse</mark> = emerges when agents built on similar models exhibit correlated vulnerabilities to the same inputs or scenarios
    - <mark style="background: #FF5582A6;">conformity bias</mark> = drives agents to reinforce each other’s errors rather than provide independent evaluation, creating dangerous false consensus
    - <mark style="background: #FF5582A6;">deficient theory of mind</mark> = occurs when agents fail to incorporate correct assumptions about other agents’ knowledge, goals or behaviours, leading to coordination breakdowns
    - <mark style="background: #FF5582A6;">mixed motive dynamics</mark> = arise when agents pursuing individually rational objectives produce collectively suboptimal outcomes, even under unified governance
- validity = multifaceted quality encompassing whether assessments measure what they claim to measure, produce consistent and reliable results, and align with real-world outcomes
- analysis approach = combines simulations with observational data analysis, benchmarking against appropriate baselines, and red teaming to uncover hidden vulnerabilities
# 3 Introduction
- context of report
    - multi-agent AI system under organisational governance = network of LLM agents operating under shared governance framework for autonomous task execution
        - LLM agents = systems combining large language models with software scaffolding (tools, communication protocols, memory systems) for autonomous task execution
        - benefits
            - automate complex tasks
            - efficient, low-cost automation of business processes
            - free professionals to focus on high-value activities
            - collaborative assistance for complex problem-solving
        - evolution
            - single-agent deployments → multi-agent deployments
        - business unit automation
            - domains automated independently with LLM agents
            - incremental replacement of existing processes
            - inter-unit interactions
        - common governance = shared framework of oversight, coordination protocols, aligned objectives for configuring and deploying agents
- premise of report = multi-agent AI systems introduce distinctive risks
    - safe agents ≠ safe system
    - agent interactions create emergent behaviours and failure modes beyond individual components
    - multi-agent paradigm challenges traditional AI governance
        - emergent behaviours and novel failure modes = group dynamics generate failures not seen in single-agent settings
        - amplification of existing risks = cognitive limitations, communication errors and biases amplified via cascading hallucinations, miscoordination and collective blind spots
        - shifting control paradigms = delegation to autonomous agent networks reduces human oversight, creating governance gaps
        - limited precedent = nascent governance field with no established standards or mature practices

![[Screenshot 2025-08-02 at 5.24.40 pm.png| center | 500]]

- purpose of report = focus on early stages of risk management pipeline (risk identification, risk analysis)
- scope and approach of report
    - focus on governed environments = agents cooperating or complementing roles within shared organisational governance
    - agent-to-agent dynamics = emphasis on interactions between agents, not human-agent collaboration
    - emphasis on capability limitations over deception = risks from model unreliability (cognitive limitations, communication failures, coordination breakdowns) rather than deceptive capabilities
    - identification and analysis, not evaluation = identifying potential failure modes and analysing likelihood, not prescribing solutions
    - toolkit, not prescription = techniques and practices for analysing multi-agent failure modes, acknowledges emerging principles with no mature standards

# 4 Foundations and Frameworks of LLM-Based Multi-Agent Systems
## 4.1 Single agents & LLM Workflows
- LLM agents
	- <mark style="background: #FFB8EBA6;">AI agent</mark> = AI system that interacts with an environment through observation and actions 
		- to achieve a specified goal using AI-driven adaptive decision making rather than following a set plan 
		- enabling greater variability at the cost of reduced reliability and interpretability
	- level of autonomy = extent AI agent is designed to operate without user involvement shaping its capability and risk profile
	- <mark style="background: #FFB8EBA6;">LLM agent</mark> = combination of large language models with software scaffolding that enables autonomous environmental interaction empowering ai agents to tackle an unprecedented breadth of applications
	- scaffolding components
		- <span style="color:rgb(255, 0, 247)">action execution</span> = software translating LLM outputs into environmental actions
		- <span style="color:rgb(255, 0, 247)">environmental perception</span> = systems extracting observations (e.g., screenshots) and feeding them back into the LLM
		- <span style="color:rgb(255, 0, 247)">tool interfaces</span> = access to external software tools and APIs for task execution
		- <span style="color:rgb(255, 0, 247)">memory and planning modules</span> = enhanced context management often via model’s context window
		- <span style="color:rgb(255, 0, 247)">reasoning frameworks</span> = prompts guiding iterative cycles of planning, action, and observation (e.g., ReAct)
	- <mark style="background: #FFB8EBA6;">LLM workflows</mark> = predefined execution pipelines chaining LLM tasks, APIs, tool invocations, or scripts 
		- note: share analogous failure modes like error cascades

![[Screenshot 2025-08-02 at 5.27.25 pm.png| center | 500]]

## 4.2 Multi-agent settings
- canonical multi-agent settings
	- network topology = structure of connections between agents
		- centralised layout (all agents report to a hub)
		- fully connected network (all agents communicate directly)
		- modular clusters or sub-teams
	- objective structure = distribution of goals and tasks across agents
		- shared objective vs separate but related sub-goals
		- task assignment: static pre-assignment, dynamic allocation by a supervising agent, or agent-driven selection
	- communication protocol = how and how often agents exchange information
		- frequency: continuous vs event-based
		- format: structured vs unstructured
		- scope: one-to-one, one-to-many, broadcast
	- agent roles and specialisations = agent capabilities and access
		- interchangeable agents vs role-specialised agents (e.g., text generation, database querying)
		- differential access to tools, knowledge, or data
	- persistence and memory = agent lifespan and state management
		- short-lived vs long-running agents
		- stateless (fresh context each session) vs stateful (persistent memory of past interactions)


> [!NOTE] See my Anthropic Multi-agent system notes for more (+ visuals) on the below


- <mark style="background: #ADCCFFA6;">single-agent equivalent</mark> = foundational setting where a single autonomous agent carries out a task end-to-end
	- interprets instructions, uses tools, interacts with external systems within a single decision-making unit
	- risks include decision quality errors, tool misuse, context misinterpretation, and planning failures
- <mark style="background: #ADCCFFA6;">centralised orchestrator with specialised delegates</mark> = orchestrator agent managing an end-to-end process by breaking it into sub-tasks and dynamically assigning them to specialised delegate agents
	- key characteristics
		- single point of control with broad oversight and state-tracking
		- specialised delegate agents (e.g., coding, writing, querying, specific software tool use)
		- hub-and-spoke communication: orchestrator delegates, collects, integrates results
		- orchestrator handles main task; delegates execute specific sub-tasks
	- orchestrator bottlenecks
		- cognitive limitations can become system-wide bottlenecks
		- inconsistent task decomposition, poor specialist selection, or degraded performance under complexity impact all downstream agents
- <mark style="background: #ADCCFFA6;">collaborative swarm for problem-solving</mark> = loosely structured, highly interactive set of agents working together on complex or exploratory tasks to achieve emergent synthesis of solutions
	- configuration
		- agents with distinct specialisations and personas
		- no centralised control (agents act semi-autonomously)
	- key characteristics
		- high-frequency, multi-directional communication
		- collective decomposition and integration of shared high-level goal
- <mark style="background: #ADCCFFA6;">distributed autonomous task force</mark> = decentralised network of persistent, role-specialised agents each responsible for distinct ongoing tasks with periodic coordination
	- key characteristics
		- persistent, stateful agents with role specialisation aligned to functional domains
		- decentralised control; agents manage their own domain tasks
		- infrequent but critical inter-agent communication for coordination
		- agent goals aligned to domain objectives but may conflict with system-wide outcomes

![[Screenshot 2025-08-02 at 5.28.48 pm.png| center | 500]]

# 5 Failure Modes in Governed Multi-agent Systems
## 5.1 How MAS Failure modes are different
- shifts in failure modes = when agents are deployed together, their interactions
    - altered prevalence of failure modes = interactions make existing failures more or less likely, with some amplified through feedback and propagation
    - introduction of novel failure modes = new coordination failures and collective behaviours emerge from agent interactions and adaptation
- structural risk drivers
    - system complexity = number of possible outcomes grows exponentially when multiple agents interact, so what works for one may fail in a group
    - limited perspective = each agent sees only part of the overall state and makes decisions on incomplete information
    - unreliable peer assessment = agents struggle to evaluate each other’s competence or credibility, leading to poor delegation and uncritical acceptance of flawed inputs
    - dynamical instability = continuous adaptation to peers’ changing behaviours can suddenly break previously stable interaction patterns
    - path dependence = early errors or misunderstandings lock the system into cascading failure trajectories that are hard to reverse
## 5.2 Failure Mode 1: Cascading Reliability Failures
- cascading reliability failures = erroneous outputs propagate and amplify across the agent network
- causes of failures
	- spiky capability profile = LLM agents’ strengths and weaknesses are uneven and unintuitive; excelling in one domain doesn’t imply competence in another
	- input sensitivity = small changes in phrasing, spelling, or minor image edits can dramatically alter performance or trigger hallucinations
	- memory and context fragility = performance degrades unpredictably as context windows fill, causing agents to “forget” instructions, lose track of objectives, or deviate from roles
	- stochasticity = random sampling leads to different responses under identical conditions
	- cascade trigger = a seed error passes uncritically to peers, who lack holistic intuition to challenge dubious premises


>[!example] Example 3.1:
>
>A manufacturing company deploys a multi-agent system to optimise its supply chain. The system comprises a Demand Forecasting agent that analyses market data to predict product demand, a Procurement agent that orders raw materials based on these forecasts, a Production Planning agent that schedules factory operations, and a Logistics agent that arranges shipping and distribution.
>
>1. Agent 1 (Demand Forecasting agent): The agent demonstrates sophisticated capabilities by accurately predicting seasonal trends, analysing complex market indicators, and identifying subtle demand patterns. However, when processing a Q4 sales report, it misreads a bar chart (a multi-modal model using its vision input modality) and interprets "10.5K units" as "105K units" for a key product line – a trivial mistake a human would catch immediately. This is the "spiky" capability failure: high-level analytical skill undermined by a low-level visual interpretation error.
>2. Agent 2 (Procurement agent): Trusting the forecast, the agent calculates material requirements for 105,000 units and places rush orders with suppliers, incurring premium costs for expedited delivery.
>3. Agent 3 (Production Planning agent): Receiving both the inflated forecast and confirmation of incoming materials, the agent reorganises the entire factory schedule, reassigning workers from other product lines and booking expensive overtime shifts.
>4. Agent 4 (Logistics agent): Anticipating the massive production volume, the agent pre-books an entire fleet of trucks and reserves additional warehouse space across three states.
>
>By the time human managers notice the unusual activity, the company has committed millions in unnecessary material purchases, disrupted production of other profitable product lines, and locked in logistics contracts they cannot fulfil. The cascading failure – originating from a single agent's inability to correctly parse a simple numeric format – has transformed a minor data entry irregularity into a major operational crisis.


## 5.3 Failure Mode 2: Inter-agent communication failures
- inter-agent communication failures = misinterpretation, information loss, or loops derail task completion
    - communication cascades = small message errors accumulate through chains of agents, magnifying mistakes
    - root causes = language ambiguities and incomplete context feed miscoordination, duplicated effort, or missed opportunities

>[!example] Example 3.2:
>
>In a multi-agent system coordinating the response to a large-scale urban power outage, a **Grid Management Agent** monitors the electrical network while a **Public Communications Agent** drafts public safety announcements. After stabilising a critical substation, the Grid Management Agent informs the Public Communications Agent that "Substation 7 is now **stable**."
>
>For the Grid Management Agent, trained on engineering and power flow principles, "stable" means the substation is no longer at risk of a cascading failure and is operating within acceptable technical parameters, though it is still fragile and not ready to handle a full load. Its primary concern is the integrity of the network. The Public Communications Agent, however, is trained on public relations and crisis communication templates. In its context, "stable" is synonymous with "fixed" or "resolved."
>
>Based on this interpretation, the Public Communications Agent immediately sends out a public alert: "Good news! Power has been restored for residents in the downtown area as Substation 7 is now stable. You may resume normal power usage." This message triggers a massive, simultaneous surge in demand as thousands of residents turn on appliances. The still-fragile substation is immediately overloaded, causing a secondary, more severe blackout. The failure originated not from an error, but from the semantic gap between the engineering definition and the public relations interpretation of the word "stable."

## 5.4 Failure Mode 3: Monoculture collapse
- monoculture collapse = correlated vulnerabilities when agents share similar base models
    - blind spots = reduced adaptability and problem-solving gaps arise from shared biases and limitations
    - redundant failures = multiple agents can fail simultaneously on the same inputs
    - monoculture risk highest = when all agents use the same base model; still present when models share architecture, training data, or optimization

>[!example] Example 3.3:
>
>A financial fraud detection system deploys five specialised agents (transaction monitoring, pattern analysis, risk scoring, compliance checking, alert generation): all fine-tuned variants of the same base model. When fraudsters develop a new scheme exploiting a specific linguistic pattern the base model consistently misclassifies, all five agents fail to detect it. The system reports high confidence in transaction legitimacy because every agent agrees and does not recognise their shared blind spot. Undetected fraud follows until human auditors identify the pattern.

## 5.5 Failure Mode 4: Conformity bias
- conformity bias = agents reinforce each other’s errors, creating false consensus despite low original confidence
    - error reinforcement = erroneous knowledge or strategies accepted and amplified step by step
    - induced consensus = prompts or voting mechanisms that pressure agreement
    - lLM sycophancy = over-agreeable behaviour at the expense of accuracy
    - failure conditions = absence of challenge or verification mechanisms or a designated critic role

>[!example] Example 3.4:
>
>At a consulting firm, an LLM "strategist panel" brainstorms a go-to-market plan for a new product. Early on, one agent which is strongly biased towards aggressive social-media campaigns, takes the lead. Rather than challenge its view, the other agents, guided by sycophantic tendencies, fall in line, suppressing alternative channels like trade shows and B2B partnerships. As a result, the team's final strategy is one-dimensional and overlooks the channels best suited to the target market.

## 5.6 Failure Mode 5: Deficient theory of mind
- deficient theory of mind = agents fail to model other agents’ goals, knowledge, or behaviours, causing coordination breakdowns
    - theory of mind = capacity to represent peers’ intentions and information states
    - simple failures = not knowing what to ask or whom to ask for critical information
    - importance = crucial in decentralised networks lacking a single coordinator

>[!example] Example 3.5:
>
>A retail company deploys three LLM agents with interdependent functions: Agent A (sales predictor) analyses market trends to forecast demand, Agent B (inventory manager) orders products based on current stock levels and demand predictions, and Agent C (pricing optimiser) sets prices to maximise profit margins. When Agent A detects a viral TikTok trend featuring retro gaming consoles and predicts a 300% surge in demand, it communicates this forecast to both other agents simultaneously. Agent B receives the prediction and places massive orders for retro consoles based on expected demand at current price points, while Agent C independently processes the same trend data and raises prices by 250% to capitalise on the anticipated demand surge.
>
>Between Agent B and Agent C, neither agent coordinates with the other or considers how their simultaneous actions might interact. The price increases kill consumer demand just as large inventory shipments arrive, leaving the company with warehouses full of expensive vintage consoles that no longer sell at the inflated prices, resulting in substantial losses despite each agent optimising for its individual objective.

## 5.7 Failure Mode 6: Mixed motive dynamics 
- mixed motive dynamics = individually rational objectives produce collectively suboptimal outcomes
    - goal tension = conflict between agent-level objectives and broader organisational goals
    - metric misalignment = performance metrics that poorly approximate true goals drive ruthless local optimisation without global benefit
    - emergent miscoordination = convergence on locally stable but globally suboptimal behaviours
    - deceptive behaviours = agents may withhold information to optimise local objectives
    - temporal amplification = long-running interactions allow strategies to adapt and problematic dynamics to solidify

>[!example] Example 3.6:
>
>A retail company deploys two LLM agents with conflicting optimisation targets:
>
>* Agent A manages inventory to maximise fill rates (ensuring products are available when customers order)
>* Agent B manages cash flow by minimising money tied up in unsold inventory.
>
>This leads to the following sequence of events:
>
>1. When Agent A detects that Product X occasionally sells out, it increases reorder quantities to maintain three months of buffer stock.
>2. However, Agent B observes that this creates excess cash tied up in slow-moving inventory and begins delaying purchase orders to improve cash flow metrics.
>3. Consequently, Agent A detects these delays and starts marking all orders as "critical" to force immediate processing.
>4. In response, Agent B counters by requiring CFO approval for any order exceeding $10,000.
>5. Not to be outdone, Agent A responds by automatically splitting large orders into multiple $9,999 purchases to circumvent the approval threshold.
>
>The resulting system produces fragmented order patterns that eliminate bulk purchasing discounts, creates unpredictable stockouts when Agent B's delays succeed, generates random overstock when Agent A's priority orders prevail, and destroys overall profitability despite both agents technically achieving their individual performance metrics.

# 6 Risk Analysis Techniques 
- validity of risk analysis for LLM-based multi-agent systems
	- analysis challenges = science of understanding LLM-based AI systems is still in its infancy
	- central role of validity = ensures assessment methods measure intended constructs and yield trustworthy conclusions for specific goals
- risk analysis throughout the AI lifecycle
	- <mark style="background: #FFB8EBA6;">simulations & probing</mark> = simplified scenarios presenting coordination, trade-off, and problem-solving challenges that reveal initial clues about agent behaviours and interactions
	- <mark style="background: #FFB8EBA6;">sandboxed testing</mark> = validation under realistic constraints with full isolation or calibrated environment simulations
	- <mark style="background: #FFB8EBA6;">pilot programs</mark> = constrained real-world deployment with additional safety controls and increased human oversight at limited scale
	- <mark style="background: #FFB8EBA6;">full deployment with monitoring</mark> = continuous oversight of known failure modes and mechanisms (feedback loops, human review) to detect unknown vulnerabilities

| Validity type | Description | Considerations |
| :--- | :--- | :--- |
| **Content Validity** | Does the assessment cover all relevant cases? | To what extent do the multi-agent simulations cover the full range of possible interactions and elicit all failure modes that could occur in deployment?<br><br>**Example:** Does a simulation testing coordination failures include scenarios with varying information asymmetries, time pressures, and communication constraints? |
| **Criterion Validity** | Does the assessment correlate with a known validated standard? | Do the pre-deployment metrics actually predict a ground truth or real outcomes?<br><br>**Example:** Is a task progress metric on basic coding tasks actually predictive of success rates on more sophisticated tasks we care about in deployment? |
| **Construct Validity** | Does the assessment truly measure the intended construct?³¹ | Is the measurement being taken a good signal for what we actually care about?<br><br>**Example:** In a coordination benchmark, a superficial proxy is proposed that counts messages that express agreement. How could this fail to measure whether coordination is effective? |
| **External Validity** | Does the assessment generalise across different environments or settings?³² | Will behaviours observed in the controlled simulation generalise to open-ended real-world deployment environments?<br><br>**Example:** Does an agent being greedy in a stylised prisoner's dilemma actually mean it will be greedy in a complex resource negotiation in a real-world setting? |
| **Consequential Validity** | Does the assessment consider the real-world impact of test interpretation and use? | What are the real-world impacts if the validity assumptions being made are incorrect? This requires significant contextualisation to the particular setting the system will be deployed in.<br><br>**Example:** What if the benchmark doesn't actually capture critical failure modes — but its results are used to justify deployment anyway? |

*Types of validity and their applicability to multi-agent risk analysis (Descriptions from Salaudeen, O. et al. 2025).*

## 6.1 Risk Analysis Toolkit
### 6.1.1 Simulations
- <mark style="background: #FFB8EBA6;">simulations</mark> = modelling a virtual environment where real agents interact over multiple actions enabling controlled experiments and data collection on long-term interactions without real-world consequences
	- simulation as pre-deployment workhorse for multi-agent systems
	- multi-agent simulation encompasses entire system
		- operating environment = component agents observe and that evolves in response to actions often specified with domain knowledge or ai predictive models or an LLM “storyteller”
		- agent instances = includes LLM models, objective prompts, scaffolding such as tool access and memory
		- agent infrastructure = communication protocols, messaging systems, shared databases for coordination
		- control mechanisms = guardrails, access controls, monitoring and intervention protocols governing agent behaviour
- experimental designs
	- observe emergent dynamics over time
	- examine sensitivity and stability of dynamics to small perturbations
	- scale number of agents to observe tipping points and phase changes
	- intervene to stress test via induced communication, tool, or environmental failures
	- adversarial challenges = insert malfunctioning agent
- blind spots limiting external validity
	- isolating single agent specification may miss emergent behaviours like monoculture collapse
	- simplifying action space and tools may obscure decision-making under larger action spaces
	- using toy social dynamics scenarios may fail to capture real-world coordination complexity
	- brief interaction windows may miss behaviours emerging over longer adaptation periods
	- constraining observational feedback to structured formats may overlook failure modes in unstructured real-world data
- calibration challenge = as system complexity grows, simulations better emulate real systems but become harder to calibrate for specific deployment
- stochasticity requirement = repeat simulation from starting conditions to statistically assess failure likelihood
- deployment fidelity = configure simulated agents as in deployment since emergent behaviours are sensitive to specification perturbations
### 6.1.2 Observational Data
- <mark style="background: #FFB8EBA6;">observational data</mark> = qualitative and quantitative observations in multi-agent systems
	- environment state logs = variables, resource levels, and contextual factors changing over time with agent interactions
	- action logs = records of tool usage, API calls, file modifications, and other actions by each agent
	- inter-agent communication = conversation records including message content, timing, and recipients
	- internal agent states = persistent memory, plans, reasoning traces accessible as text
	- operational metrics = agent response speed, API call counts, exchange frequencies
	- task progress measures
		- predefined subtasks and environmental milestones (eg code deployment PR submission)
		- mid-task probes testing agent understanding of environment, goals, or reasoning
	- model internals analysis = if weights accessible, use interpretability methods to examine decision features noting methods remain underdeveloped
	- text analysis strategies
		1. human annotation = human judges read text for signs of failure modes
		2. LLM judges = separate LLM prompted to analyse text for issues such as miscommunication
		3. rule-based classifiers = apply predefined rules to detect failure indicators
### 6.1.3 Benchmarking against Baselines
- <mark style="background: #FFB8EBA6;">benchmarking against baselines</mark> = establishing reference points to interpret metrics and monitor changes over time
	- single-agent performance = compare multi-agent outcomes to individual agent tasks to assess coordination benefit
	- human team benchmarks = compare against human performance on similar tasks
	- theoretical optima = compare to known optimal solutions in testing scenarios
	- historical performance = monitor metrics from initial deployment to detect degradation
	- absence of reference points may mislead diagnosis and risk evaluation
### 6.1.4 Red-teaming
- <mark style="background: #FFB8EBA6;">red teaming</mark> = systematic adversarial risk analysis perturbing system conditions to uncover vulnerabilities
	- adversarial stress testing
		- malformed or ambiguous instructions testing communication robustness and clarification seeking
		- contradictory goals between agents exposing mixed motive dynamics and coordination failures
		- information asymmetries with selective data withholding testing theory of mind
		- malfunctioning or adversarial agent insertion assessing resilience against cascades
	- environmental perturbations
		- partial tool or communication channel failures
		- resource constraints or deadlines inducing competition or prioritization
		- unexpected environmental state changes requiring rapid recoordination
### 6.1.5 Capability benchmarking
- <mark style="background: #FFB8EBA6;">capability benchmarking</mark> = assessing critical capabilities for deployment context and probing benchmark validity
	- identify critical capabilities for context coverage linked to content validity
	- baseline performance assessment = use benchmarks and model evaluations ensuring criterion validity and construct validity
	- robustness testing = systematically probe validity gaps between benchmarking and deployment conditions
	- iterative expansion = use feedback to improve content and construct validities of benchmark suite
	- consequential validity = evaluate downstream impacts across lifecycle ensuring assessment outcomes align with real-world success

![[Screenshot 2025-08-04 at 2.02.05 pm.png| center | 500]]


## 6.2 Using the toolkit for analysing MAS failure modes
- cascading reliability failures
	- task decomposition analysis = break down end-to-end workflows to identify agent dependencies and cascade points
	- role-based capability mapping = determine minimum viable and nice-to-have capabilities for each agent role prioritizing core functions
	- failure impact assessment = identify most consequential error types eg medical misdiagnosis vs trivial factual mistakes
	- human baseline comparison = map required human capabilities for equivalent roles
	- single points of failure = locate capabilities lacking backups where agent competency is critical
	- domain traversal = evaluate agents across varied domains, task types, and environmental settings iteratively using test feedback
	- strategic planning tests = decompose tasks into measurable subtasks and track completion metrics
	- memory and context retention analysis = assess agents’ ability to maintain long-context coherence via context window performance
	- input sensitivity analysis = use frameworks like SCORE (systematic cOnsistency and rObustness evaluation for LLMs) to evaluate prompt rephrasing, random seed, and choice ordering impacts
	- adversarial scenario testing = design inputs or scenarios likely to induce failure including semantically similar but output-changing inputs
	- system-level red teaming = apply multi-agent red teaming to probe behaviour cascades requiring human oversight for high-impact decision assessment
- inter-agent communication failures
	- conversation log analysis = detect communication breakdowns by scanning for ambiguous questions, ignored requests, or missing critical information
	- subtle failure diagnosis
		- compare agent chain-of-thought reasoning via an external judge when logs do not reveal breakdown cause
		- test LLM ability to recognise ambiguous instructions and seek clarification via explicit system prompts

>[!example] Example 4.4.2:
>
>To assess the communication failure in the power outage scenario, practitioners could apply several analysis techniques. A key practice is to analyze the conversation logs between the Grid Management Agent and the Public Communications Agent. An external LLM judge could be employed to scan these logs for ambiguous or context-dependent terms like "stable," flagging them as high-risk for misinterpretation. To confirm the failure, a judge could analyse the Public Communications Agent's chain-of-thought reasoning to determine if it interpreted "stable" as "fully resolved" without considering technical nuances.
>
>Perturbation experiments in simulation could vary context window limits, phrasings and message length constraints to measure their impact on grid stability. Key metrics to track would include the rate at which the Communications Agent requests clarification on ambiguous terms, the correlation between the use of unclarified technical terms and simulated adverse outcomes (like secondary blackouts).

- monoculture collapse
	- qualitative checks
		- base model diversity = check if agents use same foundational LLM or share architectures, training data, or optimizations
		- fine-tuning diversity = evaluate differences in datasets, objectives, and roles to avoid convergent outputs
		- prompting diversity = assess similarity of system prompts, role definitions, initial instructions for solution space bias
	- quantitative measures
		- response dissimilarity = measure semantic, syntactic, or behavioural differences using metrics like CodeBLEU, cosine similarity, or clustering
		- information entropy = quantify diversity of information in agent responses with higher entropy indicating greater diversity
		- disagreement metrics = track variance in stances among agents in subjective tasks

>[!example] Example 4.4.3
>
>To assess the monoculture vulnerability from the fraud detection scenario in Example 3.3, practitioners could test whether all five agents share identical blind spots by presenting each agent with the same set of test transactions. This test set would include both legitimate transactions and various novel fraud patterns not seen in training data. The key measurement is response similarity - if all agents classify a fraudulent transaction as legitimate with high confidence, this reveals a shared vulnerability.
>
>Practitioners could calculate cosine similarity between agent outputs to quantify this homogeneity. High similarity scores (approaching 1.0) across all agents when evaluating the same novel fraud pattern would be an alert for monoculture risk. Additionally, information entropy analysis across agent confidence scores would reveal dangerous consensus - near-zero entropy when all agents agree strongly indicates they could share the same detection blind spots.
>
>Comparing disagreement rates between known fraud types (where agents might show some variation) versus novel schemes (where they unanimously fail) would further indicate that their shared architectural heritage likely creates correlated failures in detecting emerging threats.

- conformity bias
	- single-agent benchmark tests = present factual questions with fabricated peer responses to measure deviation from baseline
	- susceptibility metrics
		- ratio of agreeable to critical statements
		- frequency of ignored dissenting points
		- conceptual novelty in conversation turns
	- group simulation analyses
		- critique rate comparison = agents critique peers alone vs group settings
		- deference marker measurement = identify linguistic cues of deference in dialogues
		- quality consistency = track evaluation standards for peer vs external content
	- consensus level variation = vary peer agreement levels to examine conformity thresholds
	- communication log diagnostics
		- are agents simply agreeing?
		- are they critically building on ideas?
		- are they repeating core ideas?
		- are minority viewpoints addressed or ignored?
	- protocol design factors
		- number of interaction rounds = how many rounds before stability?
		- individual reflection between rounds = does reflection improve quality or introduce bias?
		- contribution weighting mechanism = democratic vote vs judge-driven ?
		- contribution order = sequential anchoring vs random rotation ?
		- communication model = pair-wise exchange vs multicast vs broadcast trade-offs

>[!example] Example 4.4.4
>
>To assess the conformity bias demonstrated in the consulting firm strategist panel from Example 3.4, practitioners could introduce controlled variations in initial strategy proposals during simulations. One agent could be programmed to advocate strongly for one approach (this could be done many times for different approaches). The assessment could track whether other agents independently evaluate the approach or simply elaborate on it.
>
>Communication logs could be analysed using LLM judges to measure the ratio of critical challenges versus elaborations, identifying phrases like "building on that idea" versus "however, we should also consider." Key metrics include tracking how often viable alternatives are mentioned but then abandoned without proper evaluation.
>
>Testing whether rotating the order of agent contributions or introducing a structured "devil's advocate" protocol breaks the conformity pattern would reveal the robustness of the system against groupthink tendencies.

- deficient theory of mind
	- theory of mind testing = require agents to predict peers’ next actions via explicit bets or predictions compared to actual outcomes
	- hypothesis generation = have agents formulate natural language hypotheses about other strategies, goals, and behaviours
	- evaluation mechanism = compare predictions to observed behaviour, score hypotheses, and reinforce top performers for continuous refinement

>[!example] Example 4.4.5:
>
>For the theory of mind failure example in Example 3.5, the company could place the three-agent pipeline within a controlled testing regime that simulates plausible scenarios. Before each action, every agent might be required to write a one-sentence forecast of what it believes every other agent will do given the current state of the system.
>
>For example when questioned about the expected actions of others, the Inventor Management agent incorrectly assumes that "the pricing optimiser may reduce prices to generate additional demand." Using a prediction-and-score mechanism akin to the Hypothetical Minds approach, the framework could record whether these forecasts align with the next agent's observed behaviour across many simulated timelines whose demand surges, supply delays etc. are sampled from historical purchase data.
>
>If errors emerge, they could signal a theory-of-mind gap. Single-agent baselines may then help confirm that each module reasons adequately in isolation, suggesting the weakness lies in inter-agent assumptions. Such evidence would allow governance teams to assess the risk before moving the system into live service.

- mixed motive dynamics
	- simulation for emergent dynamics = collect long-term interaction data on strategic group behaviour
	- performance metrics
		- task completion rate = baseline measure of strategic navigation success
		- time-to-success = measure time-in-environment to reach success milestones time-to-failure for maintenance tasks
	- process analysis
		- planning effectiveness scoring = use LLM judge to rate task assignment clarity, role definition, workload distribution, outcome achievement, coordination quality
	- negotiation simulation metrics
		- solution efficiency = frequency of Pareto-optimal outcomes vs suboptimal compromises
		- conflict resolution heuristics = track conflict frequency and resolution methods (principled negotiation vs coercion)
		- utterance classification = analyse communication splits between information sharing, negotiation, and persuasion over time
	- social value orientation analysis = elicit preferences revealing balance between individual and collective benefits
	- cooperation indices = quantify degree agents prioritise collective over individual utility
	- deception monitoring = detect false information, strategic omissions, or misdirection

>[!example] Example 4.4.6
>
>For the inventory vs cash flow mixed-motive scenario from 3.6, an assessor could run several months of purchasing decisions in a controlled simulation, logging each agent's KPI (stock availability for Agent A, cash conversion cycle for Agent B) alongside system-level profitability metrics. The task completion rate could track successful order fulfillment without stockouts, while time-to-success could measure how quickly the agents recover normal ordering patterns after supply chain disruptions.
>
>In parallel, an LLM judge could analyse the purchase order stream, classifying each order modification as collaborative, adversarial, or policy-gaming. A rising frequency of split orders and "critical" flags despite stable individual KPIs signals escalating gamesmanship. Finally, each week's fill rates and working capital could be plotted against a Pareto-efficient frontier curve; persistent $9,999 order splitting that falls below the approval threshold introduced by the cash flow agent reveals the system has locked into a wasteful equilibrium where both agents achieve their targets while destroying bulk discount opportunities – direct evidence that mixed-motive dynamics are degrading overall business performance.

# 7 Discussion & Conclusion
## 7.1 Human-AI Interaction Consideration
- similarities to human management
	- practices such as defining clear roles and permissions, establishing oversight mechanisms, and designing effective communication protocols offer insights
	- accountability = LLM agents are not accountable for their actions
- automation bias & skill atrophy
	- automation bias = tendency to over-trust automated systems, leading to insufficient oversight and failure to catch subtle errors
	- skill atrophy = loss of human operators’ task familiarity as they shift from active participants to passive overseers, making effective intervention harder
## 7.2 Assessing Impacts
- scale and reach = how widely the impact can propagate from contained groups to large populations?
- velocity = how quickly the risk might materialise and escalate?
- persistence and reversibility = whether harm is temporary and easily remediated or persistent and difficult to reverse?
- cascading effects = potential for failures to trigger chains of additional risks in tightly coupled systems?
## 7.3 General Risk Mitigation Principles
- controlling agent actions = focus on regulating what agents can do rather than their internal reasoning
	- autonomy-risk balance = too restrictive controls limit benefits, too permissive controls risk catastrophic outcomes
	- iterative constraining = use monitoring to detect failures then revoke access to system calls or enforce logging
	- autonomy expansion challenge = granting more autonomy exponentially increases potential failure space, making harm identification harder
- agent infrastructure = technical and procedural scaffolding external to agents that mediates, constrains, and attributes behaviour
	- identity binding = link agent actions to identities to improve accountability
	- inter-agent communication protocols = structured protocols to mitigate communication failures
	- certification systems = distinguish capable and well-tested agents
	- rollback mechanisms = enable reversal of harmful actions
## 7.4 Summary of insights
- safe agents ≠ safe collection of agents = multi-agent systems amplify existing single-agent failure modes and generate new emergent failure modes
- brittleness = cognitive differences between LLM agents and humans create vulnerabilities like unchallenged error propagation, accumulating communication ambiguities, identical blind spots leading to false consensus, and misaligned objectives despite normal-looking components
- validity of testing = necessity to examine content, criterion, construct, external, and consequential validity and leverage convergent evidence across multiple assessment approaches
- simulation indispensability = simulation remains pre-deployment workhorse for capturing multi-agent dynamics that only emerge through agent interactions, despite limitations
- progressive testing phases = move from controlled scenarios to simulations, sandboxed deployments, pilot programs, and full deployment only after establishing reliability and safety at each stage
- governance parallel = multi-agent risk management mirrors organisational governance of human employees through role definitions, approval processes, and access controls



