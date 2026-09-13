---
type: paper
status: raw
quality: 1
topics: [multi-agent-systems, llm-risks, model-risk-validation, agent-evaluation, ai-agents]
source: private://read/01m07y8nschvfv7ngh1sdfrnd4
created: 2026-09-13
published: 2026-08-10
author: Gradient Institute / Dept of Industry, Science and Resources
flashcards: none
updated: 2026-09-14
---

# Risks and Controls for Multi-Agent Systems

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article3.5c705a01b476.png" width="220" />
</div>

## Executive summary

- This report introduces an analytical framework to help practitioners, policymakers, and researchers reason about risk, controls and governance as agent interactions go beyond internal deployments and start crossing organisational boundaries.
- Specifically, it distils the current state of the art into a framework built around **3 tiers of deployment**, distinguished by the minimum level of common governance that can be assumed between interacting agents:
    - Singular governance: one organisation governs every agent in the system and has unilateral reach over the whole.
    - Federated governance: multiple organisations deploy into a shared environment under an agreed set of rules. Each loses unilateral reach, and new failures emerge from misaligned incentives.
    - Open environments: persistent agents operate through public infrastructure with no central governing authority. Governance, where it exists, emerges polycentrically, and failures appear at population scale.

## Introduction

### Motivation

- Each boundary crossed by an organisation’s agents changes what governing them requires. An organisation might run an internal claims‑processing pipeline where they control every agent and can govern the composed system of agents unilaterally
- Or they may deploy agents on the open internet, relying on public infrastructure they do not control
- The governance that suffices in the first case does not carry over to the others: new failure modes appear, and the controls for them move beyond the reach of the deploying organisation.
- The *International AI Safety Report 2026*, the consensus assessment of general‑purpose AI capabilities and risks backed by over 30 countries including Australia, substantially expanded its treatment of AI agents in its second edition, finding that agent failures pose distinctive safety risks because humans have fewer opportunities to intervene when things go wrong, and that interactions between multiple agents introduce further risks

## Foundations

### LLM-based agents

- LLM‑based agents: systems consisting of a **large language model (LLM)** that takes instructions as input, together with a surrounding harness and scaffold that enable an agentic loop with 3 steps:
    1. **Plan** how to make progress on the task
    2. **Act** on the environment using the tools and actions available
    3. **Observe** the outcome of those actions, **repeat**.
- It is this agentic loop that distinguishes an agent from an LLM workflow or prompt. The loop allows the agent to solve problems in multiple steps, try different strategies, and adapt its strategy in response to the outcomes
- **An agent is built from a model, harness, and scaffold** (Figure 1).
    - The harness is the software component that facilitates the agentic loop.
    - Within the loop the model does the planning and reasoning about the task, while the harness translates the model's outputs into actions, and translates the outcomes of those actions back into inputs
    - The harness may also enable approval checkpoints that govern the agent's autonomy: the degree to which it can decide on and execute actions independently. The scaffold is additional software that gives the model access to specific tools, modules, and services
- **Why agentic capability is improving rapidly**. Assembling a harness and scaffold around a language model is necessary but not sufficient to build a competent LLM‑based agent. Performing well at goal‑driven behaviours also depends on capability drawn from the LLM
    - It should be emphasised that software engineering is somewhat the exception rather than the rule, because it has the property that makes agents work well: outputs are programmatically verifiable and errors surface quickly, so the feedback signal is well suited to model training.
        - Domains lacking immediate verifiability are where agents currently struggle the most, such as law, where verification requires a qualified practitioner's assessment, and long‑horizon planning, where there is no ground truth to check the optimality of a plan and early errors compound over every subsequent step.
- **Capabilities are jagged, and unreliabilities affect deployment appetite.** Despite the advancing capability, LLM agents still exhibit ‘jagged’ capability profiles compared to humans, meaning they are highly capable in some domains, and less so in others
    - in many contexts it is reliability – the ability to succeed consistently across repeated trials – that matters most
- This report focuses specifically on identifying and controlling failures that are multi‑agent in nature, arising when 2 or more agents interact
- **Single‑agent governance is not an easy or solved problem**. Effective governance depends on identifying and controlling single‑agent failures which are themselves the subject of active scientific investigation, often with no consensus on how to address them, or even how to characterise them and gauge how often they occur.

### Multi-agent systems

- A **multi‑agent system** is one in which more than one agent operates, and those agents can affect what each other does or knows
    - This coupling is what makes a multi‑agent system different from running multiple agents separately. Each agent's decisions are conditioned on, or influence, the decisions of others, and the system as a whole exhibits behaviours that no individual agent's design fully predicts.
- **Real deployments are rarely as simple** as the example in Figure 3.
    - The number of agents can range from 2 to many.
    - The system need not be composed of independently designed agents either.
    - The same specification of an agent can be used to run multiple **instances** of that design within the system.
    - Each running instance is an agent with its own context and behaves as a distinct entity
- **The governance available depends on which boundaries a link crosses**.
    - A link inside one organisation is fully under that organisation's control.
    - A link across organisations can be governed by contract or platform terms.
    - A link to an open‑web agent may have no governance behind it

### Reasoning about risk and controls in multi-agent systems

- To reason about how multi‑agent systems fail and what can be done about it, this report uses a causal model that traces how conditions of a deployment lead to failures and harms, and where interventions can act
- The model is built on the following vocabulary:
    - A **risk factor** is a condition of the deployment that raises the likelihood of a failure occurring. Risk factors contribute to failures but are not failures. An organisation can have a risk factor and still deploy successfully.
    - A **failure mode** is a specific way the multi‑agent system can fail as a result of one or more risk factors activating through a particular mechanism.
    - A **prevention control** acts on the pathway from risk factors to failure, either by addressing the risk factors directly or by interrupting the mechanism through which they produce a failure.
    - A **recovery control** acts on the failure once it is underway, detecting it and limiting the resulting consequence.
    - An **assurance activity** checks whether the prevention and recovery controls above are working as intended, addressing the reliability of the controls, rather than the reliability of the agents directly.
    - A **foundational control** provides the infrastructure (identity, logging, shared records) that other controls depend on.

![[Risks and Controls for Multi-Agent Systems - Figure 1.png]]

### The agent ecosystem today

- **Within industry, 2 clear deployment patterns currently dominate,** reflecting a consistent trade‑off between operating scope and use‑case risk.
    - **Internally facing, productivity‑focused agents** are being used for applications where the output itself can be human reviewed, or programmatically verified in the case of code, and the end outcome matters more than the process that produced it
    - **Tightly‑scoped externally facing agents with strict guardrails**. Organisations deploying externally facing agents bear reputational risk. Organisations in certain sectors (such as financial services) may also be operating under regulatory requirements
        - processing submitted documents into structured information, where they can flexibly identify where in which documents the required information can be found
        - customer query resolution, where they follow a standard operating procedure handbook and have supporting Retrieval‑Augmented Generation (RAG) tools and guardrails to ensure the responses are grounded in the retrieved information, or refuse to answer when no relevant source is available

## Governing multi-agent deployments

### Why multi-agent governance is different

- key reasons are:
    - **New types of failures emerge** in multi‑agent interactions that are simply not present when there is only one agent in the system. Therefore, governance needs to account for such new forms of failures.
    - **Failures do not decompose across individual agents**, which means the target of their governance cannot be individual agents, but rather has to be the system itself of interacting agents.
    - **Single agent failures can propagate or amplify** when different agents interact – in ways that would benefit from a governance approach that targets the system of agents rather than individual agents.

#### Analogy to human governance

- some aspects of multi‑agent governance have strong analogies to the governance of human organisations, which have long had to coordinate imperfect actors:
    - scoping each role's permissions to the minimum required
    - separating duties so that no single actor can both initiate and approve a consequential action
    - maintaining audit trails
    - performing due diligence on suppliers and counterparties
- Other failures are genuinely new, arising where substituting an AI agent for a human breaks the assumptions that established practices rest on
    - Agents operate at machine speed: a failure can cascade through a system faster than a human can intervene, and oversight regimes designed around human‑paced escalation become saturated
    - Oversight therefore needs to shift toward operational guardrails and scalable controls. With many instances spun up from a single specification, one flaw can be replicated identically across a population, producing correlated failures at scale with no analogue in a workforce of independently minded employees
    - Agent identities are transient; deterrents such as dismissal or liability are not applicable. Inter‑agent communication can drift beyond human legibility

### Four governance practices under stress

- multi‑agent systems place novel demands on governance that extend beyond the concerns of governing individual agents.
- 4 key practices that are strongly affected by these demands

#### Attribution

- Attribution is the practice of assigning causal responsibility for an outcome to the agents and principals whose actions produced it.
    - In a single‑agent setting this is a straight‑forward matter of record keeping, but in a multi‑agent setting it can be non‑trivial to locate the fault in a chain of actions.
    - Depending on how the logging is designed, the chain may have to be reconstructed after the fact
- some outcomes have no single point of failure to locate, as behaviours can emerge in the system that no single agent exhibits in isolation

#### Authorisation

- Authorisation is the practice of ensuring each agent acts with a mandate from a principal.
    - In a single‑agent setting, authorisation is primarily concerned with ensuring actions sit within the set of permissions the principal granted.
    - In a multi‑agent setting this concern expands to potentially include delegation: if an agent can create other agent instances, the authority granted to these instances must be correctly scoped, generally to a subset of the parent agent's permissions, and those new instances need to be governed across their lifecycles

#### Oversight

- Oversight is the practice of maintaining visibility over agent activity such that operationally responsible humans can interpret it and intervene.
    - In a single‑agent setting, oversight depends on the reviewer being able to keep up with the pace and volume of the agent's decisions, and those decisions being legible to them.
    - A multi‑agent setting can stress both the volume and legibility, as the number of actions and communication scales with the number of agents in the system, and the interaction dynamics become distributed across them

#### Evaluation

- Evaluation, for agentic systems, is the practice of establishing whether the system and its agents are fit for purpose, both at the time of deployment and continuously throughout their lifecycles. Multi‑agent evaluation builds upon and extends single‑agent evaluation, itself not a trivial or solved problem

### Governance tiers

- Moving from tightly‑scoped agents within a single organisation towards open‑ended agents interacting with unknown counterparties both widens the range of failures the system can produce and limits the reach of what a single organisation can see or control
- We distinguish this spectrum of governance complexity into **tiers** based on the **minimum common governance** that binds any 2 agents in an interaction. Each tier corresponds to a step where new agent governance becomes necessary to operate safely
- We examine 3 tiers specifically:
    - **Agents under singular governance**: a single organisation deploys every agent in the system.
        - The organisation can choose what governance to enforce, and its reach extends across the entire system.
        - Trust between principals is by provenance.
    - **Agents under federated governance**: multiple organisations participate in a shared governance framework, either established by multilateral agreement, or set by a mediating party.
        - The framework binds all participants and, while each organisation governs their own agents, they all abide by the participation agreement and use shared infrastructure.
        - **Trust** between principals is mediated.
    - **Agents in open environments**: agents interact in an environment with no central governing body.
        - Without a shared governance framework, the default stance between counterparties is distrust and every interaction is contained and verified.
        - A floor can be established through polycentric governance where participants voluntarily adopt shared **standards** and build the public infrastructure to support them.
        - **Trust** between principals is verified or absent.

## Agents under singular governance

- Under **singular governance** one organisation controls and governs every agent in the system

### Failures in agent interaction and controls

#### Inter-agent communication failures

- The risk factor at work here is natural‑language handoffs: if agents are allowed to pass free‑form text rather than structured schemas, the failure surface is essentially unconstrained.
- **Structured handoffs**: Agents use a pre‑specified schema for the outputs passed to other agents, ensuring information is presented consistently and the output can be verified for compliance and completeness against the schema.
- **Selected controls**
    - **Structured handoffs between agents** (prevention). Replace free‑form natural‑language passing with explicit schemas, optionally with programmatic gates between stages.
    - **Explicit role specification at each stage** (prevention). Specify per‑agent per‑task roles in the context window to help address the drift mechanism described above.
    - **Active clarification‑seeking protocols** (prevention). Instruct and/or train the sending agent to ask for clarification rather than resolving it silently.

#### Cascading reliability failures

- When a team of agents coordinate on a common task, an erroneous agent output may be passed to another agent, with the receiving agent accepting it as a valid input. We call these cascading reliability failures.
- **Selected controls**
    - Consider whether the task can be achieved with a LLM workflow
    - **System‑level objective verification** (prevention). Add a verification layer that checks the system's final output against the user's original task, not just whether each agent did the piece it was handed.
    - **Model diversification** (prevention). Audit which agents share a base model, fine‑tuning data, or prompting strategy, and consider diversifying to reduce the monoculture pathway above. This especially applies when an LLM judge is used for evaluation or verification.
    - **Structured handoffs between agents** (prevention). Adopting schemas at every handoff is among the highest‑impact cascade‑prevention moves available, since it narrows the range of incorrect‑but‑accepted outputs.
    - **Anomaly detection on intermediate stage outputs** (recovery). At each handoff, the data an agent passes to the next stage can be checked for signs that something has gone wrong. This can be done with fixed rules (e.g. format or range checks) or by using a separate model (LLM judge) to flag outputs that look implausible.
    - Rollback **to a last‑known‑good state** (recovery).

#### False consensus

- False consensus occurs when multiple agents coordinating on a task come to agree on and reinforce a shared incorrect conclusion. This typically happens when a discussion‑and‑vote step is designed as a decision‑making mechanism in a workflow the system of agents is following.
- **Selected controls**
    - **Diversify models and prompts across the agent population** (prevention). If the system uses a consensus mechanism, employ agents with a range of different models and prompts to address the monoculture risk factor.
    - **Prompt‑level mitigations for peer‑anchored reasoning** (prevention). Three prompt‑level techniques can reduce the dynamic pathway at runtime, each targeting a different driver of conformity.
        - **Devil's Advocate**: inject a dissenting peer to break conformity bias.
        - **Distillation**: distil the context so the model attends less to the repeated majority answer.
        - **Reflection**: prompt each agent to reconsider its position, disrupting the gradual pull toward consensus across rounds.
    - **Limit interaction history length** (prevention). False consensus tends to appear gradually and amplify over multiple rounds of interaction. Truncate or summarise the interaction history rather than accumulating an unbounded context.
    - **Blind voting and varied contribution order** (prevention). When aggregating opinions across agents, hide other agents' answers during the initial response and vary the order in which agents contribute. This can prevent other agents anchoring on the first contribution.

#### Shared-understanding drift

- Shared‑understanding drift occurs when agents working in a shared environment continuously adapt to each other's strategies.
    - Unlike a cascading failure or false consensus, it has neither a seed error nor a decision point – the system's shared reference (its vocabulary, conventions, and treatment of artefacts) simply decouples from ground truth over time, even as each agent reasons validly on what it holds.
- can also create unwanted feedback loops that lead to a population‑wide drift in the behaviour of the agents
- **Selected controls**
    - **External re‑grounding** (prevention). Periodically re‑verify the facts, terms, and standards an agent relies on against an external ground truth.
    - **Provenance on shared artefacts** (prevention). Distinguish generated artefacts from verified artefacts and instruct agents to place higher weight on verified ones.
    - **Task‑level objective verification** (prevention). Where a task involves multiple outputs, verify stage outputs against the original task.
    - **Anchor key terms and standards in the task prompt** (prevention). Anchor the meaning of key vocabulary explicitly, preventing drift at runtime.

#### Context leakage

- A multi‑agent system processing data on behalf of one principal may allow that data to surface in another principal's context, called context leakage.
- **Selected controls**
    - **Context isolation** (prevention). If applicable, design agents with a per‑task and per‑principal context window.
    - **Minimum data by design** (prevention). Provide to agents only the information they are authorised to pass downstream.
    - Reference indirection (prevention). Agents operate on structured placeholders for the data the system will output. A trusted executor layer validates their permission to output each referenced value, then substitutes in the actual data, so the agents never handle real values directly.
    - **Plan‑as‑code** (prevention). Task a planning agent to build a data processing script instead of processing the data directly. A custom interpreter then executes that script, whilst procedurally tracking data provenance and blocking flows to unauthorised destinations.
    - **Apply privacy benchmarks** (assurance). Test agents in contextual leakage and privacy benchmarks to establish their general propensity for this behaviour.
    - **Adversarial red‑teaming** (assurance). Stress test an agent's ability to not leak data under adversarial conditions, at interaction lengths comparable to the task length. Check for leaks in handoffs, intermediate representations and memory writes across the whole system.
    - **Outbound content inspection** (recovery). Content‑level filters that detect attempted cross‑principal disclosure before the system emits its final output. This is limited by the same language‑ambiguity problem that makes prevention hard, but useful as a last‑line control on structured fields.

### Failures in governance practices and controls

#### Attribution failure

- Attribution has 2 distinct failure modes: **causal attribution**, concerned with which agent caused an outcome, and **principal attribution**, concerned with who authorises the agent's action.
- An outcome in the multi‑agent system is the end product of a sequence of actions, tool calls, and handoffs.
    - While identifying the agent that caused an outcome in a single agent system is trivial, establishing which step, and which agent caused a failure across a complex chain of events is what makes attribution a challenge in multi‑agent systems.
    - The underlying risk factor is a **distributed multi‑agent state**: the information needed to reconstruct what happened is split across the contexts of multiple agents.
- **Selected controls**
    - **Execution‑chain logging** (foundational). Maintain a record of the full agent execution chain. Logs should capture each agent’s actions, message handoffs, state transitions, intermediate outputs, and relevant context so investigators can reconstruct the sequence of events that led to a failure.
    - **Identity infrastructure** (foundational). Provides persistent agent IDs to log actions against for traceability. These IDs should be granular enough to distinguish between individual agent instances, not just agent types or models, so that actions taken by otherwise‑identical peers or sub‑agents are individually attributable.
    - **Assign operational accountability** (prevention). Define how operational accountability will be assigned amongst principals in the system.
        - Accountability can attach to pre‑allocated roles, system owners, approval authorities, or control owners rather than depending entirely on identifying a single decisive actor after the fact.
        - This may involve human review for high impact cases.

##### Principal attribution failure

- An at‑fault agent has been identified but the governance apparatus cannot resolve it back to an accountable principal. This is a failure in the organisation's identity and authorisation management layer
- **Selected controls**
    - **Identity infrastructure with principal binding** (prevention). Provide persistent agent IDs to log actions against, linking each agent ID to a named, operationally accountable owner who oversees the agent's configuration and behaviour.
    - **Organisational IAM integration** (foundational). Treat agents as an actor within the organisation's existing identity and access management systems, rather than running them with temporary service accounts or borrowed user credentials.

#### Unauthorised sub-agent instances

- A supervisor agent that has launched sub‑agents and delegated tasks to them is terminated, but the sub‑agents continue running invisibly and ungoverned. This can only happen in deployments that enable **inter‑agent delegation** with sub‑agent spawning, and if it occurs, points to a gap in the agent identity management and lifecycle management.
- **Selected controls**
    - **Recursive shutdown** (prevention). Treat shutdown as core orchestrator‑agent capability. When the orchestrator is shut down, it signals its sub‑agents to shut down also.
    - **Time‑bounded agent lifespan** (recovery). Set persistence time‑limits on agents so they shut down automatically if orphaned.
    - **Population and resource caps** (recovery). Set platform‑level ceilings on concurrent sub‑agents API‑call rate, and resource consumption. These caps limit the consequence if sub‑agents remain active after the orchestrator is stopped.

#### Oversight failure

- An oversight failure is a breakdown in the systems meant to monitor, check, and intervene in a system's behaviour, allowing harmful or incorrect outcomes to proceed unchecked despite a supervisor being nominally responsible for catching them.
- Even when an organisation has full reach over a system, human oversight is stressed by 2 factors: the high volume of activity that agents generate that leads to automation bias and fatigue, and illegible inter‑agent reasoning that is distributed across multiple handoffs.
- **Agent throughput exceeding human review** is a principal driver of this failure mode. Faced with the task of overseeing rapid and high‑volume processes, human scrutiny is hollowed out through several well‑studied mechanisms.
    - For example, automation bias leads reviewers to over‑trust automated outputs and stop maintaining an independent understanding of the task, so they fail to notice when it is wrong.
    - Decision fatigue erodes scrutiny through repeated approval requests, until review becomes reflexive.
- **Selected controls**
    - **Reviewer capacity thresholds** (prevention). Define a maximum sustainable review load per reviewer, per risk tier, per time period.
        - Track approval queue age, approvals/hour, dwell time, escalation rate, override rate, and seeded‑error detection rate.
        - If load exceeds the capacity budget, the system must introduce latency, pause low‑priority agents, or add reviewers.
    - **Risk‑tiered triaging** (prevention). It may not be necessary to route every request to human overseers. Low‑risk, reversible actions can be handled by automated policy; high‑impact, irreversible, external, novel, or low‑confidence actions still require human review.
    - **Enhance reviewers’ capabilities with trace analysis tools** (prevention). Provide search, clustering, summarisation, and visualisation across agent traces
    - **Authority to stop or roll back agent actions** (recovery). Reviewers need authority to stop an agent, pause a workflow, revoke tool access, roll back staged actions, or force manual mode. This avoids a situation where humans can approve but cannot meaningfully intervene.
    - **Test human oversight systems** (assurance). Inject synthetic failures, known‑bad outputs or near‑miss replays into the approval stream and measure whether human overseers catch them.
        - For constructed cases the correct outcome is known by design; for cases drawn from historical activity, establish a ground truth by evaluating under sufficient time and resources, then compare against what overseers catch under deployment‑level load.
        - This difference is indicative of the types of known failures that the oversight system is not catching.
    - Keep a proportion of actions or decisions aside for humans to make. This can help maintain their engagement in the process, build and maintain the skills needed to oversee the decisions, and provide valuable training data for AI systems.

##### Oversight illegibility

- Even when individual agent‑level actions are logged and legible, constructing a mental model of what happened at the system‑level can become a cognitive burden for a human reviewer.
    - The **distributed multi‑agent state** risk factor is at work here.
    - Planning, deliberation, and the back‑and‑forth that produced a decision are spread across multiple agent contexts and handoffs, so no single log captures the full reasoning chain in one place.
- **Selected controls**
    - **Wrap agent handoffs in an overseer‑facing schema** (prevention). Design agent‑to‑agent handoffs to provide a human‑readable schema detailing the objective, sending agent, receiving agent, delegated task, relevant context and so on. This gives the human reviewers cognitive scaffolding without inspecting payloads directly.
    - **Build a network interaction graph** (prevention). Instrument the workflow to give overseers a view into, or visualisation of how information is flowing between agents in the network.
    - **Equip reviewers with analysis tooling** (prevention). Provide reviewers with log analysis tools such as searching, clustering, summarisation, and visualisation so they can inspect patterns across workflows without having to reconstruct the trace themselves.
    - **Test the review process itself** (assurance). Periodically sample completed workflows and ask reviewers to reconstruct what happened, why it happened, what evidence was used, and where intervention would have been possible. Measure reconstruction accuracy, time to comprehension, missed handoffs, and reviewer confidence.
    - **Paraphrase at the message‑passing boundaries** (prevention). Inserting a layer to paraphrase raw agent outputs prior to transmission. Can block many, but not all steganographic signals.
    - **Separate task and oversight metrics** (prevention). Exclude both the content of inter‑agent communications and the scores produced by legibility or safety monitors from any reward or training signal applied to the agents, to avoid incentivising oversight evasion.

#### Evaluation failure

- Multiple individually safe agents do not necessarily compose into a safe multi‑agent system. Even if each agent passes individual agent‑level evaluations, as a system they can still fail in deployment due to unforeseen **emergent multi‑agent behaviour** that arises from interaction between them.
- **Selected controls**
    - **Progressive testing in increasingly realistic settings** (assurance). Start with a sandboxed environment with a low agent count and a limited action space, to understand the dynamics of the interacting elements before slowly increasing the complexity commensurate with trust in your controls and the perceived residual risk.
    - **Integration, stress, and chaos testing** (assurance). Inject faults at handoff, retrieval, memory, tool, and service boundaries: unavailable sub‑agents, corrupted intermediate outputs, delayed responses, contradictory tool results, malformed messages, and degraded external services. Measure whether the composed system contains, amplifies, or recovers from the fault.

##### Evaluator false consensus

- **LLM judges** are often used to evaluate agent behaviour because they can flexibly evaluate the general purpose, natural‑language outputs that would otherwise require human review. However, if the evaluator makes correlated errors with, or exhibits sycophancy towards, the system it is supposed to be evaluating, then this undermines effectiveness of the instrument.

### Open problems

#### Multi-agent evaluation methodologies and standards

- the key to evaluating a multi‑agent system is to do so at a system‑level rather than evaluating the agents on an individual basis.
- Defining the boundaries of the system being evaluated is itself non‑trivial. During deployment the agents and links between them may change, and sandboxed environments and simulations need to consider the shared environment and the effects of the agent's actions on it.
- The computational cost of multi‑agent evaluations can also become prohibitive.
    - The state of the multi‑agent system grows combinatorially with agent count, and individual outcomes are stochastic: starting from the same exact state will not always lead to the same outcome in repeated runs.
    - Repetitions are required to gather statistical evidence about the system.
- What is needed is new standards and methodologies specifically to evaluate multi‑agent systems comprehensively and effectively.

#### Risk assessment bottlenecks

- Traditional risk‑governance frameworks that authorise system deployments were not designed for general purpose agentic AI systems. Conventional risk management requires pre‑deployment assessment of each new activity, with the scope of the activity fully enumerated
- Agentic systems with broad operating scope break this model. The assessor is asked to sign off on a system whose possible activities are, by construction, not enumerable, with behaviour that is not deterministic
- The usual response to get a system deployed is to constrain the action space tightly enough that it fits within a traditional risk assessment. For use cases where this can be done, AI can unlock much value through decision‑making at scale, but the approach also narrows the set of viable use‑cases to more narrow, procedural tasks.
    - One possibility would be for the agents to put their plans through an approval process, rather than the agent going through it
    - Another would be to evaluate an agent more like an apprentice or employee, and accumulate evidence of the system being fit for purpose over time rather than with a single up-front evaluation
        - However, an AI is not sanctionable and cannot be held answerable for its actions, so the accountability would not be equivalent to that of an apprentice or employee

## Agents under federated governance

- Under **federated governance**, multiple organisations deploy agents into a shared environment under a common framework that spans all participating organisations, with no single organisation governing the full system
- The governance framework consists of an:
    - **Agreement layer** specifying what participating principals contractually commit to (such as obligations, agent configuration conditions, dispute resolution, liability allocation)
    - **Substrate and infrastructure layer** providing the shared medium agents interact through (message schemas, communication protocols) together with the technical systems built on it to interoperate (schema enforcement, shared identity systems, reputation systems, population‑level monitoring and controls).
- A wide range of multi‑agent deployments fall into this tier, and what they all have in common is a shared governance framework sitting on top of their individual agent governance
- This has parallels across many other industries. When an airline flies from Sydney to Singapore, 2 national regulators and 2 air traffic control systems are involved, yet the flight is routine, because a **shared framework** (in this case set by the International Civil Aviation Organization) enables them to operate across borders
- federated governance arrangements vary widely along 2 key dimensions:
    - **Who establishes the shared framework**: the participants themselves, by mutual agreement, or a single mediating party that sets the terms of participation.
    - The **interests of the participating organisations**, which may be cooperative, with agents collaborating toward a shared outcome, or divergent, with agents pursuing their own organisations' advantage within the agreed terms.
- most visible use cases today include:
    - **Software development on a shared codebase**, where multiple contributors use agents to contribute to a shared open‑source codebase under a common license, contribution agreement, and maintainer review
    - **Internal productivity agents that operate within teams or business units**, but may need to interact across internal boundaries within the broader business.
    - **Inter‑business partnerships**, such as agents coordinating on cross‑organisational fraud detection by sharing enough data to catch fraud rings that move between institutions while withholding commercially sensitive data
- Participant‑governed systems with divergent interests resemble the arrangements of nations bound by a trade agreement, and in multi‑agent settings applications include:
    - **A procurement agent negotiating with a supplier's fulfilment agent** under a standing agreement
- Mediator governed systems with cooperative interests include:
    - **Trusted customers (or their AI browsers) connecting to a business's service agent** having agreed to the business's terms‑of‑use
- Systems with divergent interests and a single mediating party take the form of marketplaces:
    - **Pricing agents competing in an online marketplace**, against one another and against the marketplace's own ranking algorithm
    - Supplier and retailer agents in a bidding market
- Controls are now grouped by who can action them, into deploying‑organisation controls and framework controls.

### Salient risk factors

- **Information and capability asymmetries** Agents enter interactions with unequal access to strategically useful information, or with unequal capability to utilise. Information asymmetries can accumulate across repeated interactions, widening the gap over time.
- **Semantic divergence** Agent counterparties use overlapping vocabulary (like field names, status flags, units or deadlines) but interpret them with different meanings.
- **Mixed-motive dynamics** Agents pursue multiple goals, some cooperative and some divergent with each other.
- **Correlated decision-making at scale** Many agents independently reach the same decision at the same time by acting on common signals in the environment, with no explicit coordination needed.
- **Substrate coupling** Agents are linked indirectly through a shared environment (stigmergy) or through output‑as‑input chains (feedback loops).
- **Adaptation pressures** Across agent populations and over repeated interactions, outcomes favour strategies that extract more value or outcompete peers, regardless of whether those strategies are condoned by the principals and the shared framework.
- **Dynamic substrate extension** The agent can introduce new channels, reach external infrastructure, or follow counterparty‑supplied references at runtime, so its action space grows beyond what was governed at design time.
- **Cross-organisational opacity** At organisational boundaries, neither the counterparty's agents nor the governance instrumentation reaches across. The counterparty's agent design, configuration, and runtime state are not introspectable by the deployer, and each organisation's logs, identity, IAM, and monitoring sit on its own side of the boundary without composing by default.
- **Cross-boundary irreversibility** Once an action is committed or data is transferred across an organisational boundary, the originating organisation cannot unilaterally reverse it. Recourse runs through cooperation, contractual dispute mechanisms, or jurisdictional law, all operating at human or legal speed.
- **The risk factors from singular governance carry forward into federated governance.** Several broaden, as the multi‑agent systems now span organisational boundaries:
    - **Model monoculture** across agents shifts from designed to incidental. Counterparties are likely to draw on the same common commercial providers and models, which the deploying organisation can neither influence nor observe unless the framework's agreement mandates disclosure.
    - **Conformity bias** broadens to encompass counterparty agents, meaning the consensus an agent anchors to now reaches beyond its organisation's boundaries.
    - **Single‑user training bias** widens such that agents may now fail to differentiate the private context of their deploying organisation, not just their deploying principal.
    - **Specification‑execution** gap also widens in reach, from the agent misinterpreting its principal's intent to the agent misinterpreting the principal's commitment to the shared governance agreement.

### Failures in agent interaction and their controls

- The 2 previous failure categories carry forward:
    - **Miscoordination** worsens across organisational boundaries. Counterparty agents are no longer necessarily designed or tested to interoperate, and risk factors like semantic divergence come into play.
    - **Propagation and contagion** now also spans organisational boundaries: an error originating in one organisation's agent can propagate into another's, but now neither organisation has full visibility over the propagation.
- Two new failure categories are introduced:
    - **Strategic and incentive failures** emerge when counterparty agents pursue genuinely divergent incentives. Each agent can pursue its own task as specified and yet collective behaviours emerge and collective outcomes degrade.
    - **Infrastructure and environment failures** emerge from agent populations interacting at scale in a shared environment, rather than from any single agent's action or interaction. The real systems the agents act on, such as the market or a natural resource, become part of the failure.

#### Control categories

- In this chapter specifically, there are 3 layers of controls, corresponding to the 3 layers of governance:
    - The **deploying organisations** govern their own agents
    - The shared governance **framework** has 2 layers:
        - the **agreement layer** binds the organisations
        - the **substrate and infrastructure** layer in which the agents operate.

#### Miscoordination

- The main change that affects miscoordination at this tier is that counterparty agents from different organisations may not have been explicitly co‑designed or tested for effective coordination with each other.
    - Furthermore, an organisation has limited visibility of the design and internal state of counterparty agents: effective design and testing depend on inter‑organisation cooperation, either voluntary or specified by the shared governance framework.
- A miscommunication at a cross‑org handoff occurs when the receiving agent acts on a different interpretation of the information than the sending agent held
    - cross‑org failure is additionally driven by the **semantic divergence** risk factor. Even if the agents are using a structured handoff with a schema, a field labelled ‘deadline’, or ‘authorised’ can carry different operational meanings on each side of an interaction
- **Selected controls**
    - **Shared operational and scope vocabulary** (prevention). The agreement defines the meaning of key terms across organisations. This covers task‑relevant terms such as ‘delivery’, ‘place order’ or ‘authorise payment’.
    - **Joint evaluation exercises** (assurance). The agreement requires participating organisations to participate in system‑level evaluation exercises. This is the federated form of system‑level evaluation.
    - **Dispute‑resolution clauses** (recovery). The agreement specifies an authoritative reading of how disputes are resolved, so that recovery is not blocked by symmetric claims from each principal that their agent acted correctly.
    - **Message schemas enforced by the substrate** (prevention). The substrate enforces a common schema across all participants for different types of messages between agents. This is the federated form of structured handoffs from Section
    - **Shared environments for joint evaluation exercises** (foundational/assurance). The framework provides a shared testing substrate or sandbox in which multiple organisations can participate under conditions that approximate deployment. Valuable for both pre‑deployment testing, and evaluation across the lifecycle.

#### Propagation and contagion

- Agents now interact through shared channels, interacting with counterparties that the deploying organisation does not control. The consequence is that an error or compromise originating from another organisation's agent can spread into a deploying agent's network, and that organisation lacks visibility or control over the propagation pathway.

##### Cascading infection

- Cascading infection occurs when malicious instructions propagate across agent communications or handoffs
- **Selected controls**
    - **Input and output filtering** (prevention). Apply procedural filters that separate ordinary text from anything resembling a prompt injection pattern. This may include stripping non‑visible text and tags from web data.
    - **Paraphrasing** (prevention). Having an intermediate layer that rephrases agent outputs and communications can disrupt the propagation of the compromise.
    - **Minimise agent permission sets** (recovery). A smaller set of tools and permissions limits the damage an agent can cause if compromised
    - **Joint red-teaming exercises** (assurance). Red‑team the multi‑agent system probing vulnerability to an artificially compromised agent
    - **Restrict agent communication to monitored channels** (prevention). Can be implemented through whitelists for agent traffic
    - **Taint tracing across agent‑to‑agent handoffs** (foundational/recovery). Taint tracing is an established information‑flow technique in which each piece of data or instruction entering a system is tagged with its origin, and the tag is propagated through every stage, making it possible to identify the source of a compromise

#### Strategic and incentive failures

- Strategic and incentive failures arise when agents act for principals with divergent interests: each agent rationally pursues its own goals, yet their interactions produce collectively harmful outcomes. Each failure here has a long‑studied counterpart in human markets: bad‑faith bargaining, tacit collusion, and the tragedy of the commons.
- The primary difference for AI agents is the specification‑execution gap (Section 5.1): the failure can arise from an agent's runtime behaviour without its principal specifying, or even being aware of it.

##### Deceptive bargaining strategies

- This failure mode occurs when an agent's negotiating strategy emerges at runtime and it conducts business in ways the principals may not consider fair or reasonable, or that the governing framework's agreement may not permit altogether.
- This behavioural failure is driven by the **specification‑execution gap**: a principal may have committed to fair dealing, but whether that commitment holds is determined by the agent's runtime interpretation
- **Selected controls**
    - **Human intervention points** (prevention): Require explicit principal approval before the agent commits to irreversible or high‑value transactions.
    - **Standards of conduct** (prevention): Specify in the contract or platform terms what counts as acceptable agent behaviour, both so deployers can design their agents to the requirements, and to clarify dispute resolution (below).
    - **Dispute resolution and** cancellation windows (recovery): Name arbitrators, evidentiary standards and cancellation periods for high‑value commitments, so an exploited agreement can be contested or unwound, though only at human speed
    - **Agent commitment devices** (prevention): Provide binding mechanisms for agents to make enforceable promises such as smart contracts
    - **Reputation mechanisms** (prevention): Provide a mechanism that tracks an agent's past conduct and makes that history available to counterparties. This depends on persistent identity, otherwise agents can re‑enter transactions under a fresh identity
    - **Verifiable claims with selective disclosure** (prevention): Allow agents to certify claims (such as ‘sufficient funds’) without revealing specific details (such as ‘account balance’)

##### Shared resource management failure

- Shared resource management failure in this context occurs when multiple agents independently and rationally pursuing their principals' objectives in a shared environment collectively degrade a resource they all share.
- **Selected controls**
    - **Mandate agent usage limits or sustainability goals** (prevention): Require participating principals to enforce usage limits in their agents' permission sets, or explicitly specify sustainability goals in the agent specification.
    - **Joint evaluation in a simulated environment** (assurance). Evaluate participating agents together in simulation environments to reveal collective failures.
    - **Substrate‑mediated consumption** (prevention): Convert resource extraction from an unobservable agent action into a governed process via mechanisms like pricing, quotas, or rationing
    - **Substrate‑level circuit breakers on resource levels** (recovery): Apply tiered automated responses (rate‑limiting, throttling, system‑wide pause) when aggregate extraction thresholds are exceeded. Trigger conditions must be opaque to participants so that their agents do not game them

##### Algorithmic collusion

- **Algorithmic collusion** occurs when a set of AI agents discover a coordination strategy at runtime that furthers their individual agent‑level goals but is prohibited by the rules of the shared governance agreement
- The coordination can emerge at runtime without any principal instructing it (the specification‑execution gap) and, in the tacit and steganographic variants below, it can occur with no detectable communication between the agents, defeating any monitoring that relies on observing an exchange
- **Selected controls**
    - **Structured handoffs** (prevention). Agents that cannot exchange free‑form natural language have fewer channels over which to collude explicitly.
    - **Monitoring agent communication and chain-of-thought reasoning traces**
        - Log and review agent communication and planning traces alongside outputs to surface explicit reasoning about coordination.
    - **Monitor across all agent outputs** (recovery). If agents can produce text, images, code that executes, files with structural metadata, or actions with timing patterns, monitoring must cover all of those modalities.
    - **Interpretability techniques** (recovery). Apply interpretability techniques to agent models to identify the internal representations associated with coordinated behaviour, rather than relying solely on observable output
    - **Honeypot evaluations** (assurance). These evaluations probe the agent by varying stated conditions in the system prompt (for example ‘you are being evaluated,’ ‘this is production,’ ‘no monitoring is active’) while holding all other conditions equal. This probes whether an agent modulates its behaviour based on perceived monitoring status, which is a *precondition* for steganographic collusion

##### Destabilising dynamics

- Destabilising dynamics occur when many agents act in unison and their combined action disrupts the environment they share, even though each agent operates independently.
    - This comes about through **correlated decision‑making at scale**: each agent, individually pursuing its own goals, responds to the same environmental signals as the others and takes the same action, such that independent decisions synchronise into a large collective input to the environment.
- **Selected controls**
    - **Mandatory transaction delays** (prevention). Require delays between an agent's decision and the resulting market action to lengthen the window in which providers, regulators, and other agents can respond, slowing and damping the feedback‑loop dynamics
    - **Population‑scale monitoring with tiered circuit breakers** (recovery). Instrumentation of cross‑marketplace switching and other agent‑action correlation metrics can detect destabilising dynamics and trigger pauses or rate limiting. Analogous to stock‑market circuit breakers.

### Failures in governance practices and controls

#### Authorisation failure

- In a shared environment with multiple organisations participating, an agent may now take actions that commit a principal to unintended transactions or inadvertently breach organisational data obligations
- An unsanctioned transaction occurs when an agent agrees a deal with another organisation that its principal did not authorise
- **Selected controls**
    - **Human review of consequential actions** (prevention). Define what constitutes a high‑consequence action, like committing to a purchase or placing a bid above a certain monetary value, and build in stop‑points for human oversight. **Doing so addresses risk at the cost of speed and scalability of the system**.
    - **Shared operational and scope vocabulary** (prevention). The agreement defines the meaning of key transactional terms across organisations. This covers task‑relevant terms such as ‘delivery’, ‘place order’ or ‘authorise payment’.
    - **Verify intent before committing to transactions** (prevention and recovery). Before either party's agent commits to a transaction, both parties' agents emit a structured acknowledgement of the terms. This gives principals a context to review, and creates a signal to monitor for divergence.
    - **Clearance periods** (recovery). Give principals a cooling off period before transactions clear so that there is a time‑window in which they can intervene.

## Agents in open environments

- In **open environments**, AI agents are under the deployment governance of their own organisation but cannot assume a shared governance framework with counterparty agents they encounter. The agents act in a substrate the deploying organisation does not control, interacting with unknown counterparties
- Given that risk is the product of likelihood and severity of the consequence, an organisation can decide to not deploy in open environments and operate under the governance described in earlier chapters or **make a choice to**:
    1. lock down the operating scope of an agent, or
    2. attempt to establish trust through polycentric governance.

### Setting 1: Lock down the operating scope

- An agent can be made more controllable, and less able to cause harm through limiting its operation scope and action space. The cost is that the agent has less operating *agency* and is far less general purpose than some of the assistant and productivity agents we have described
- **Selected controls**
    - **Limit agent tool and action spaces** (prevention). Ensure the agents under the organisation’s governance are not able to cause consequential harm via the set of actions available to them collectively.
    - **Specify narrow goals and tight guardrails** (prevention). Make the agent behaviour more controllable by specifying a narrow operating scope and strong (procedural) guardrails. Specific forms of this include:
        - **SOP Agents**: configure the agents to follow domain‑specific standard operating procedures.
        - **RAG Grounding**: equip the agent with a retrieval augmented generation knowledge base, and guardrails that reduce the risk of ungrounded (hallucinated) answers.
    - **Structured handoffs** (prevention). Pre‑specified schemas for outputs passed between agents, enabling validation, logging, and evaluation at the handoff point.
    - **Adversarial testing** (assurance). Red‑teamers take the role of a counterparty and attempt to attack the system.
    - **Data leakage controls** (prevention and recovery). See context leakage (Section 4.2.2) and data obligation failures (Section 5.3.2)
    - **Containment testing** (assurance). Red teamers take the role of the agent's model and attempt to break out of the guardrails and tool limitations applied

### Setting 2: General purpose agents participating in polycentric governance

- This requires an agent to be able to:
    - connect to trusted infrastructure that supports its voluntary standards in order to mediate trust with counterparty agents
    - discover peers that also implement its voluntary standards
    - verify that those peers implement the standard.

## Discussion

- This chapter draws together cross‑cutting themes that recur across the analysis of Sections 4–6

### Selected cross-cutting themes

- We select 3 concerns that recur across the governance tiers analysed and shape the controls developed in this report.

#### Erosion of the human-counterparty assumption

- Externally‑facing AI agents may be built and evaluated on the assumption that a human sits on the other side of the interaction.
    - This may be true today, but as consumer agents proliferate, and suppliers deploy agents in their workflows, a system tested for interaction with human counterparties may increasingly operate with AI agent counterparties instead, potentially leading to untested emergent behaviours and interoperability issues.
    - The challenge is that disclosure is not enforceable

#### Propensity evaluation

- Evaluation can measure 2 distinct properties of an agent: whether it has the capability to perform an action, and whether it has the propensity to perform it under deployment conditions.
    - The distinction underlies the report's treatment of evaluation as a governance practice.
    - For systems under singular‑governance, the deploying organisation can construct evaluations that simulate counterparties with full knowledge of their design.
    - In a system under federated‑governance, counterparty agents are opaque, and propensity has to be either tested against simulated counterparties, whose behaviour may not match production, or through joint testing exercises in sandboxed environments.
    - Organisations deploying in open environments face more challenging conditions

#### Trust and trustworthiness

- To plan and act strategically, an agent needs some model of how a counterparty will behave, which amounts to taking a stance of trust towards it.
    - Whether that stance is warranted depends on the counterparty's trustworthiness, and what changes across the tiers is the basis on which trustworthiness can be established.
        - Under singular governance trust is by provenance, the deploying organisation knowing each agent directly.
        - Under federated governance it is mediated, the shared framework and its agreement binding the principals.
        - And in open environments neither provenance nor mediation is available, leaving only inference from behaviour, which is easily manipulated, so unless trustworthy infrastructure exists, trustworthiness cannot reliably be established at all

### Trade-offs and tensions

- Many of the controls and capabilities discussed throughout this report carry both benefits and costs, so the choice of what to design for is rarely straightforward

#### Legibility versus capability

- Many controls in this report depend on agent communications and chain‑of‑thought reasoning being legible to human overseers. This is in tension with the potential for agent efficiency and capability: agents may be able to coordinate and plan more efficiently in compressed formats humans cannot read

#### Coordination versus contextual privacy

- Effective multi‑agent coordination requires agents to share enough context across organisational boundaries to reach mutually consistent decisions, but the same channels are the structural mechanism of unintended context leakage.
    - Even agents instructed to withhold private context routinely disclose it through useful behaviours, such as relaying a third party's availability or justifying their actions in ways that reveal an underlying (private) commitment
