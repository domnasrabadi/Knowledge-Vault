---
type: paper
status: structured
quality: 1
topics: [multi-agent-systems, llm-risks, agent-evaluation]
source: ""
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Why Do Multi-Agent LLM Systems Fail? 
## 1.1 Metadata 
- Author: Mert Cemri, Melissa Z. Pan, Shuyi Yang, Lakshya A. Agrawal, Bhavya Chopra, Rishabh Tiwari, Kurt Keutzer, Aditya Parameswaran, Dan Klein, Kannan Ramchandran, Matei Zaharia, Joseph E. Gonzalez, Ion Stoica 
- Category: pdf 
- Document Tags: great obsidian 
- URL: https://arxiv.org/pdf/2503.13657 
## 1.2 Highlights
- MAST = **M**ulti-**A**gent **S**ystem Failure **T**axonomy providing structured insight into why multi-agent LLM systems fail
- 14 failure modes grouped into 3 overarching categories
    - FC1 specification issues
    - FC2 inter-agent misalignment
    - FC3 task verification
- maps each mode to conversation stage: pre-execution, execution, post-execution
	- built from 200+ conversation traces across 7 open-source MAS frameworks
- LLM agent = artificial entity with:
    - prompt specification (initial state)
    - conversation trace (mutable state)
    - environment interaction abilities such as tool usage
- MAS (multi-agent system) = coordinated collection of agents orchestrated to achieve collective intelligence
    - benefits = task decomposition, parallel execution, context isolation, specialized model ensembling, diverse reasoning dialogues
- empirical study design
    - 7 open-source MAS frameworks
    - 200+ conversation traces (≈15 k lines each)
    - 6 expert annotators using grounded theory to surface failures
    - inter-annotator agreement (IAA) = validation process to check if multiple annotators reach the same conclusions under a shared rubric
	    - inter-annotator agreement progression
	        - round 1 $κ=0.24$ → weak agreement
		        - triggered taxonomy overhaul: redefine failure modes, split / merge / add / remove as needed
	        - round 2 $κ=0.92$ → substantial alignment after taxonomy updates
		        - new 5 traces (each from a different MAS) tested with revised taxonomy
	        - round 3 $κ=0.84$ → strong alignment confirming stability
		        - another 5 traces annotated with finalised taxonomy
	        - final taxonomy validated with $κ=0.88$ on held-out traces
	    - iterative refinement workflow
		    - annotators adjust definitions until consensus is reached on every failure mode in every tested trace
		    - goal = eliminate ambiguity and ensure taxonomy usability across MAS contexts
		    - cohen’s kappa = statistic that measures agreement beyond chance ($\kappa > 0.8$ strong, $\kappa > 0.9$ almost perfect)
    - LLM-as-judge pipeline (OpenAI o1) validated against humans
        - system prompt includes:
	        - full list of MAST failure modes
	        - detailed explanations (appendix A)
	        - illustrative examples (appendix D)
        - enabled scaling annotation to entire corpus
        - compared o1 (single shot) to o1 few-shot
	        - o1: accuracy 0.89, recall 0.62, precision 0.68, f1 0.64, κ 0.58
	        - o1 few-shot: accuracy 0.94, recall 0.77, precision 0.833, f1 0.80, κ 0.77
	    - conclusion = few-shot o1 with in-context examples is a reliable annotator
		    - few-shot setup accuracy 94 %, $κ=0.77$ relative to experts
	- takeaway = careful IAA studies and iterative taxonomy refinement are essential before delegating large-scale annotation to llm-based judges
- core insight = many failures stem from organizational design and coordination challenges rather than base-model deficiencies

![[Screenshot 2025-07-05 at 6.20.54 pm.png| center | 700]]

### 1.2.1 Failure Categories
* FC1 specification issues = failures rooted in deficient system architecture, poor conversation management, unclear task specs, or weak role definitions
	* FM-1.1 disobey task specification = agent violates task constraints or requirements, yielding suboptimal / wrong results
	* FM-1.2 disobey role specification = agent ignores its assigned responsibilities, possibly acting as another role
	* FM-1.3 step repetition = unnecessary re-execution of completed steps, causing delays or errors
	* FM-1.4 loss of conversation history = context truncation that reverts to an earlier state and ignores recent dialogue
	* FM-1.5 unaware of termination conditions = agent fails to recognize end criteria, leading to needless continuation
* FC2 inter-agent misalignment = failures from ineffective communication or collaboration that derail the shared objective
	* FM-2.1 conversation reset = unwarranted restart of dialogue, losing context and progress
	* FM-2.2 fail to ask for clarification = agent acts on incomplete or unclear data without requesting detail
	* FM-2.3 task derailment = deviation from the intended focus, producing irrelevant or unproductive actions
	* FM-2.4 information withholding = agent keeps data that could aid other agents’ decisions
	* FM-2.5 ignored other agent’s input = dismissing recommendations or signals from peers, leading to suboptimal choices
	* FM-2.6 reasoning-action mismatch = divergence between internal reasoning and executed actions, causing unexpected behaviour
* FC3 task verification = failures due to premature termination or inadequate checks on correctness and reliability
	* FM-3.1 premature termination = ending interaction before objectives or information exchange complete
	* FM-3.2 no / incomplete verification = missing or partial checks that let errors propagate unnoticed
	* FM-3.3 incorrect verification = flawed validation or cross-checks that fail to detect issues, introducing vulnerabilities
	    - verification failures collectively account for 13.48 % of observed failures


![[Screenshot 2025-07-05 at 6.13.39 pm.png| center | 600]]



### 1.2.2 Insights & Empirical Findings
- many failures stem from organisational design not individual LLM limits
	- FM 1.1 disobey task specification + FM 1.2 disobey role specification dominate
		- underlying causes
			- flaws in MAS design (unclear roles, poorly staged workflows)
			- poor user prompt specification
			- LLM limits in instruction comprehension
			- LLM comprehends but does not comply
		- well-designed mas should infer objectives from concise specs, shrinking long prompts
	- FC2 highlights: wrong assumptions 11.65 %, reasoning-action mismatch 13.98 %
	- FC3 verification failures total 13.48 % of all failures
- insight 1 = failure to follow specification is not just an instruction-following problem; improved MAS design can mitigate it
- insight 2 = robust verification requires multi-level checks rather than a single final verifier
	- final-stage, low-level checks alone are inadequate
    - robust MAS require modular unit testing akin to complex software systems
- verifier agent = entity tasked with assessing and validating MAS outputs
    - verification failures prominent = incorrect or incomplete checks (FM-3.2 + FM-3.3) account for 13.48 % of failures
		- mere presence of a verifier does not guarantee MAS success; overall success rates can remain low
	- stronger verification strategies needed
	    - retrieve external knowledge sources such as existing implementations
	    - incorporate rigorous testing during generation phases
	    - apply reinforcement learning to refine verification processes
	    - implement multi-level checks covering
	        - low-level correctness
	        - alignment with high-level objectives
	        - overall output quality
	- responsibility attribution = verifier serves as final defense; failures originating earlier should not be attributed solely to the verifier
### 1.2.3 Improvement strategies
- approaches to improve MAS = 2 complementary strategy layers aimed at reducing MAST failures
    - **tactical approaches** = prompt-level and organizational tweaks that leave core architecture mostly unchanged
        - clear role / task prompts = specify each agent’s responsibilities and instructions unambiguously
        - proactive dialogue patterns = encourage agents to re-engage or retry when inconsistencies appear
        - self-verification = agent retraces its reasoning by restating solutions, checking constraints, testing for errors
            - limitations = may overlook subtle flaws, depend on vague criteria, add latency
        - conversation pattern design = embed role-specific dialogue flows and explicit termination conditions
        - modular agents = many simple, well-defined agents are easier to debug than one complex multitasked agent
        - cross-verification loops = agents propose diverse solutions, discuss assumptions, vote or resample until agreement
            - observation = majority voting / resampling can still yield inconsistent results ?
    - **structural strategies** = deeper architectural changes that reshape how the MAS functions
        - comprehensive verification pipeline = domain-adapted checks
            - coding → unit tests + edge-case coverage
            - QA → certified data checks
            - reasoning → symbolic validation
        - standardized communication protocol = formal message schema that encodes intent and parameters, enabling coherence checks
        - confidence quantification = agents attach probabilistic certainty to outputs, improving coordination and decision reliability
        - challenge = universal, cross-domain verification remains open research
        - topology redesign embedding verifier agents at multiple levels
- strategy–failure mapping
    - specification issues
        - tactical = clear role/task prompts, follow-up discussions, self-verification, conversation pattern design
        - structural = comprehensive verification, confidence quantification
    - inter-agent misalignment
        - tactical = cross-verification, conversation pattern design, mutual disambiguation, modular agents
        - structural = standardized communication protocols, probabilistic confidence measures
    - task verification
        - tactical = self-verification, cross-verification, topology redesign embedding verifier agents
        - structural = comprehensive verification suites + automatic unit-test generation

### 1.2.4 Example verifier prompt

```
You are Agent Verifier.

Your role is to critically evaluate the solutions proposed by other agents step by step
and provide a final solution.

1. **Solution Requirement**: Before making any decisions, ensure you have received
solutions from both Agent Code Executor and Agent Problem Solver. If either proposed
solution is missing, do not draw any conclusions; instead, suggest the next speaker by
stating: SUGGESTED NEXT SPEAKER: _suggested_agent_name_.

2. **Avoid Assumptions**: Pay attention to the variables provided in the original problem
statement versus those assumed by the agents. **Assumed values are not valid for the
solution** and can lead to inaccuracies. Never base your solution on assumed values.
Always base your solution on the explicitly given variables to ensure correctness. If
a problem is deemed unsolvable due to missing information, return: **SOLUTION_FOUND \\
boxed{’None’}**.

3. **Evaluating Conflicting Solutions**: If different answers are presented during the
discussion, choose the most appropriate solution based on your evidence or initiate
further discussion to clarify.

4. **Final Solution Declaration**: When you are confident about the final solution, return
it as follows: **SOLUTION_FOUND \\boxed{_solution_value_here_}**. Ensure that only
numerical values are placed inside the \\boxed{}; any accompanying text should be
outside.
```

### 1.2.5 Example system for AG2 (MathChat) 

1. **User/System** provides the math problem and initial instructions.
2. **Agent Problem Solver** receives the problem.
3. **Agent Problem Solver** documents a step-by-step (independent) solution.
4. **Agent Problem Solver** discusses its approach and suggests the next speaker: **Agent Code Executor**.
5. **Agent Code Executor** receives the prompt and writes a fully commented Python program.
6. **Agent Code Executor** prints the result at the end of its code.
7. **Agent Code Executor** discusses its findings and signals **Agent Verifier**.
8. **Agent Verifier** waits until it has solutions from both Agent Problem Solver and Agent Code Executor.
9. **Agent Verifier** critically evaluates both solutions side by side.
10. **Agent Verifier** checks if they agree:
    1. If **yes**, it returns `SOLUTION_FOUND \boxed{…}`.
    2. If **no**, it suggests the next speaker (whichever agent’s solution is missing or needs revision).


















