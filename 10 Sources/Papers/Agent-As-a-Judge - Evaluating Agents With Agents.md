---
type: paper
status: structured
quality:
topics: [agent-evaluation, llm-judges, llm-evaluation]
source: ""
created: 2025-07-13
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Mingchen Zhuge, Changsheng Zhao, Dylan Ashley, Wenyi Wang, Dmitrii Khizbullin, Yunyang Xiong, Zechun Liu, Ernie Chang, Raghuraman Krishnamoorthi, Yuandong Tian, Yangyang Shi, Vikas Chandra, Jürgen Schmidhuber
- Category: pdf
- URL: https://arxiv.org/pdf/2410.10934
# 2 Intro & Methodology
- evaluation gap = traditional methods fail for agentic systems
    - focus only on final outcomes, ignoring step-by-step reasoning
    - require heavy manual labour
- <mark style="background: #FFB8EBA6;">Agent-as-a-Judge</mark> = agentic evaluator for agentic systems
    - extends LLM-as-a-Judge by adding intermediate feedback across the full task trajectory
	    - evaluates like a human, examining thought + action sequence rather than end product alone
	    - cost-effective like llm-based judging, yet richer in signals
	- human-style feedback = continuous, granular evaluation akin to grading coursework rather than multiple-choice tests
	- DevAI dataset = 55 real-world AI-app development tasks
	    - designed to benchmark multi-step code-generation agents
	    - tasks follow standard ai/ml pipeline order
	        - data processing precedes modelling
	        - performance reporting occurs last
	    - topology aids monitoring and signal extraction for agentic evaluation
	- empirical results
	    - alignment rate = Agent-as-a-Judge matches human consensus 90 % vs 70 % for LLM-as-a-Judge
	    - surpasses average single human evaluator in agreement with consensus
	    - cost savings = 97.7 % time and 97.6 % monetary cost compared with three human experts

![[Screenshot 2025-07-13 at 6.07.59 pm.png| center | 500]]

- <mark style="background: #FFB8EBA6;">Human-as-a-Judge</mark> = manual evaluation protocol on DevAI
    - goal = validate DevAI and gauge code-generation ability of baseline agentic systems
    - setup
        - three expert evaluators = 231a, 38bb, cn90
        - two rounds of review per requirement
            - round 1 = independent scoring under minimal instructions (58 h total)
            - round 2 = debate to reach consensus (28.5 h)
	- disagreement analysis
	    - pairwise disagreement rate = 10–30 % across evaluators
	        - causes
	            - missed environment feedback revealing subtle bugs
	            - differing interpretations of ambiguous requirements
	    - single human evaluation deemed unreliable
	- error analysis
	    - debate round = evaluators present evidence and correct personal errors
	        - majority vote after debate better approximates ground truth than any individual score
	        - ensemble classifier principle = aggregated judgment surpasses lone evaluator
	- consensus evaluation
	    - not absolute ground truth but closer approximation (Clemen 1989)
	    - majority alignment with consensus > individual alignment
	- bias mitigation guidelines
	    - introduce debate round after each judgment ?
	    - expand panel size > 5 experts when individual accuracy > 50 % ?
	        - larger groups reduce variance (Grofman 1983; Hastie & Kameda 2005; Larrick & Soll 2006)
	- conclusion
	    - human judgment errors inevitable
	    - combining debate and sizable expert panels lowers error risk and inductive bias
# 3 Architecture
- Agent-as-a-Judge = agentic evaluation framework that replaces human judges with an autonomous agent
    - addresses manual-labour burden and preserves evaluation thoroughness
    - designed to mimic human step-by-step assessment rather than end-point scoring
- modular architecture (8 components)
    - `graph` module = builds a dependency graph of files, modules, and folders
    - `locate` module = pinpoints the file or directory referenced by each requirement
    - `read` module = parses and interprets multimodal data across 33 formats
    - `search` module = retrieves contextually relevant code snippets and nuances
    - `retrieve` module = extracts pertinent segments from long execution trajectories
    - `ask` module = judges whether a requirement is satisfied
    - `memory` module = stores past judgments for reuse (later found harmful due to error propagation)
    - `planning` module = sequences future actions to meet project goals
- ablation results
    - `ask` alone → 65.03 % alignment rate
        - + `graph` → 75.95 %
        - + `read` → 82.24 %
    - adding `retrieve` produced negligible gains
    - `memory` inclusion degraded performance by cascading prior errors
- evaluation metrics
    - judge shift = deviation from Human-as-a-Judge consensus (lower better)
    - alignment rate = proportion of evaluations matching human consensus
        - Agent-as-a-Judge = 92.07 % (Dev-T), 90.44 % (Dev-V)
        - LLM-as-a-Judge = 70.76 %, 60.38 %
    - agent judge consistently outperforms llm judge, especially on tasks with dependencies
    - pr curves advised for class-imbalanced nature where success cases are rarer
- cost analysis
    - Human-as-a-Judge = 86.5 h of expert time
    - Agent-as-a-Judge = 118.43 min + $30.58 api cost
        - 2.36 % of the time and 2.29 % of the cost of human evaluation

![[Screenshot 2025-07-13 at 6.07.28 pm.png| center | 400]]

# 4 Discussion & Appendix
- outlook 1 = intermediate feedback enables agentic self-improvement
    - Agent-as-a-Judge provides step-level signals so agents can detect + fix issues during multistage tasks
    - contrasts with delayed-feedback systems that only assess final outputs
- outlook 2 = flywheel effect driven by Agent-as-a-Judge
    - continuous interaction between judge and developer agents yields iterative co-evolution
        - resembles self-play systems (Zelikman 2022; Chen 2024e; Wang 2024b)
        - successive incremental improvements reinforce one another → compounding performance gains
- experiment hierarchy
    - level 1
        - experiment 1a = baseline performance stats for developer agents (sec 2.3)
        - experiment 1b = human evaluations (sec 3.1)
    - level 2
        - experiment 2a = error analysis of human evaluations (sec 3.2)
    - level 3
        - experiment 3a = AI judge baselines comparison (sec 4.2)
        - experiment 3b = ablation studies for Agent-as-a-Judge (sec 4.3)
- DevAI dataset creation
    - E.1 draft user queries = craft prompts that demand multi-step reasoning and adaptation
    - E.2 judging criteria = assign explicit, binary requirements as milestones
        - meeting all requirements ⇒ task solved
        - explicitness removes ambiguity and captures multi-step nature
    - E.3 dependency graph = seven-stage AI-development flow
        - data preprocessing → feature engineering → model selection → hyperparameter tuning → metrics recording → report generation → interactive application
    - E.4 refine dataset = two rounds of manual review by different participants
        - ensure logical consistency, clarity, domain relevance
        - detected + fixed moderate number of errors
    - E.5 analyse dataset = label each requirement focus
        - categories = dataset, method, visualization, metrics, HCI, data processing
- human evaluation procedure (section H)
    - recruited three AI experts from author team
    - first round = independent scoring with minimal instructions
        - hours spent = 16.5, 19.5, 22.0
        - unanimous agreements considered trustworthy
    - second round = group discussion of disagreements
        - peers present evidence, correct errors, reduce bias
        - consensus trusted since simultaneous shared mistake unlikely
- key takeaway = Agent-as-a-Judge delivers crucial intermediate feedback, fosters a self-reinforcing improvement loop, and offers a scalable alternative to labour-intensive human evaluation

![[Screenshot 2025-07-13 at 6.08.26 pm.png| center | 700]]


---

