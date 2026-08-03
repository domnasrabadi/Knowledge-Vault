---
type: paper
status: structured
quality:
topics: [llm-evaluation, llm-judges]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
Metadata
- Author: Jiawei Gu, Xuhui Jiang, Zhichao Shi, Hexiang Tan, Xuehao Zhai, Chengjin Xu, Wei Li, Yinghan Shen, Shengjie Ma, Honghao Liu, Saizhuo Wang, Kun Zhang, Yuanzhuo Wang, Wen Gao, Lionel Ni, Jian Guo
- Category: pdf
- URL: https://arxiv.org/pdf/2411.15594

---

![[Screenshot 2025-08-10 at 3.03.22 pm.png| center | 500]]

# 1 LLM-as-a-Judge Overview
- LLM-as-a-judge = using llms to evaluate objects, actions, or decisions based on predefined rules, criteria, or preferences
- advantages over traditional expert-driven evaluations
    - can process diverse data types
    - scalable and flexible assessments
- before llms, balancing comprehensiveness and scalability in evaluation was a persistent challenge
	- classic metrics (BLEU, ROUGE) = rely on surface-level lexical overlap, often miss deeper nuances
	    - poor performance in tasks like story generation or instructional text evaluation
- llm-as-a-judge combines strengths of traditional metrics and human evaluation
- challenges limiting adoption
    - lack of systematic review → no formal definitions, fragmented understanding, inconsistent usage
    - reliability concerns → using llm-as-a-judge doesn’t guarantee alignment with established standards

![[Screenshot 2025-08-10 at 3.03.54 pm.png| center | 500]]


## 1.1 In-Context Learning for LLM-as-a-Judge
- evaluation tasks specified via in-context learning (ICL) = instructions + examples guide model’s reasoning
- 2 key design aspects
    - input design = choose variable type (text, image, video), input manner (single, pair, batch), and position (start, middle, end)
    - prompt design = four main methods
        1. generating scores
            - discrete ranges (e.g., 1–3, 1–5) or continuous (0–1, 0–100)
            - can include detailed scoring criteria
            - likert scale = absolute measure across dimensions (accuracy, coherence, factuality, comprehensiveness)
        2. solving yes/no questions
            - binary judgment on accuracy of a statement
            - common in feedback loops for sparse rewards (success/fail)
            - used for testing factual correctness and alignment with established facts
        3. conducting pairwise comparisons
            - choose better of two options (relative evaluation)
            - useful for ranking or prioritisation
            - more alignment between llm and human judgments than score-based methods
            - can extend to list-wise comparisons using ranking algorithms
            - four-option mode = allows "both good" and "both bad" ties
        4. making multiple-choice selections
            - pick most appropriate option from several choices
## 1.2 Model Selection for LLM-as-a-Judge
- general llm = use strong models like GPT-4 to replace human evaluators
- fine-tuned llm = customised evaluator models for better reproducibility + privacy protection
    - process
        1. data collection = instructions + evaluation targets + evaluations (from GPT-4 or humans)
        2. prompt design = structure based on evaluation scheme
        3. model fine-tuning = instruction fine-tuning paradigm to produce evaluations (with possible explanations)
## 1.3 Post-Processing Methods
- purpose = refine probability distributions from llm-as-a-judge for accurate + consistent evaluations
- methods
    1. extracting specific tokens = rule-match tokens from response (scores, yes/no, selections)
        - challenge: varied response formats hard to parse
    2. constrained decoding = force structured outputs (e.g., JSON)
        - drawbacks: can distort model distribution, engineering overhead
    3. normalising output logits = map outputs (esp. yes/no) to continuous 0–1 scale
        - e.g., self-consistency score $\rho_{\text{Self-consistency}}$ and self-reflection score $\rho_{\text{Self-reflection}}$
    4. selecting sentences = extract relevant sentences/paragraphs for reasoning tasks
## 1.4 Evaluation Pipeline Applications
- for models = strong llms act as automated proxies for human evaluation
- for data = automate annotation
    - risk: diminishing value as models improve
    - self-taught evaluator = generates synthetic data (contrasting outputs) → trains itself iteratively
- for agents = assess agent behaviours
- for reasoning/thinking = ensure logical coherence, refine intermediate steps, improve clarity
# 2 Improvement Strategies for LLM-as-a-Judge
- 3 main improvement strategies
    - design strategy of evaluation prompts = in-context learning (ICL)-based
    - improvement strategy of LLMs’ abilities = model-based
    - optimization strategy of final evaluation results = post-processing-based
## 2.1 Design Strategy of Evaluation Prompts
- high-quality evaluation examples in prompts help LLM evaluators grasp task objectives, processes, and rough criteria
- refinement methods
    - decomposition of evaluation steps = break full task into smaller steps, define and constrain each step in prompts
    - decomposition of evaluation criteria = break coarse criteria (e.g., fluency) into sub-criteria (grammar, engagingness, readability) and then aggregate scores
- prompt optimisation to address LLM shortcomings
    - e.g., mitigate position bias in pairwise evaluation by randomly swapping compared contents
- optimising output forms
    - directly asking for results can reduce robustness due to generative randomness
## 2.2 Improvement Strategy of LLMs’ Abilities
- fine-tuning via meta-evaluation datasets = train on datasets designed for evaluation tasks to improve understanding of prompts, boost performance, and address biases
- iterative optimisation from feedback = update model using evaluation feedback from stronger models or human corrections
## 2.3 Optimization Strategy of Final Results
- post-processing refinements to increase stability and reliability of evaluation outputs
# 3 Evaluation of LLM Evaluators
- main goal = align LLM-as-a-judge with human judgments
- metrics
    - percentage agreement = proportion of samples with same label as human annotators
    - correlation metrics = Cohen’s Kappa, Spearman’s correlation
    - classification-based = precision, recall, F1 against human labels
- dataset requirements = need LLM-generated responses with human judgments to build comprehensive meta-evaluation benchmarks
- current meta-evaluation gap = focus is mostly on LLM-as-a-judge for models, less for large-scale automatic annotation
## 3.1 Bias in LLM-as-a-Judge
- 2 categories
    - task-agnostic biases = inherent to LLMs in general
        - diversity bias = against demographic groups (gender, race, sexual orientation)
        - cultural bias = misinterpretations across cultures/regions
        - self-enhancement bias = preference for responses the model itself generated
    - judgment-specific biases = unique to evaluation context
        - position bias = favour responses in certain prompt positions
            - position consistency = how often same choice is made after swapping positions
            - preference fairness = extent of positional preference
            - conflict rate = disagreement rate after swapping
        - compassion-fade bias = altered preference based on names or framing
        - style bias = favour visually appealing style regardless of validity
        - length bias (verbosity bias) = favour longer responses
        - concreteness bias (authority/citation bias) = favour responses with details, citations, numbers, jargon
## 3.2 Adversarial Robustness
- focuses on responses crafted to manipulate scores (e.g., inserting phrases to artificially boost evaluation)
## 3.3 Meta-Evaluation Experiment
- dimensions
    - alignment with human evaluation
    - bias measurement via EVALBIASBENCH (length, concreteness, empty reference, content continuation, nested instruction, familiar knowledge biases)
- metrics
    - percentage agreement (alignment)
    - accuracy (for non-positional bias detection)
    - position consistency (for positional bias)
- findings
    - current strategies only partially effective
    - empirical best practice for pairwise tasks = use stronger LLMs, swap evaluation content positions, take majority voting from multiple rounds to reduce bias
    - alignment with humans still needs more research
## 3.4 Relationship Between LLM-as-a-Judge and Reasoning
- reasoning = cognitive process of applying logic and evidence to reach conclusions
- llm-as-a-judge = judgment tasks (evaluating, scoring, ranking, selecting answers)
- infinite judgments → approximates reasoning and thinking processes
# 4 Challenges
- reliability = both LLM and human judges have biases
- robustness = LLMs vulnerable to adversarial prompts that induce harmful or skewed outputs
- backbone model limitations = performance tied to base model’s strengths and weaknesses
