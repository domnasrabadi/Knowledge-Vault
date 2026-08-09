---
type: paper
status: structured
quality: 2
topics: [llm-evaluation, llm-judges, evaluation-metrics]
source: https://eugeneyan.com/writing/llm-evaluators/
created: 2025-07-19
published: 2024-08-18
author: Eugene Yan
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Eugene Yan
- Category: article
- Document Tags: very good 
- URL: https://eugeneyan.com/writing/llm-evaluators/

# 2 Intro to LLM Judges
- LLM-evaluator = large language model that grades another LLM’s response to an instruction or query
    - motivation = conventional n-gram or similarity metrics struggle to separate good and bad responses, and human or finetuned evaluators are costly to scale
    - baseline choice?
        - human annotators = aim for LLM–human agreement ≈ human–human agreement while gaining speed, cost, and reliability advantages
        - small finetuned evaluator = target similar recall + precision but accept slower latency than millisecond-level models
    - **scoring methods**
        - <mark style="background: #FFB8EBA6;">direct scoring</mark> = judge a single response without comparison → versatile for objective checks
        - <mark style="background: #FFB8EBA6;">pairwise comparison</mark> = pick better of two responses or tie → more stable for subjective traits (persuasiveness, tone, coherence)
        - <mark style="background: #FFB8EBA6;">reference-based evaluation</mark> = compare candidate against gold reference with fuzzy matching by the LLM-evaluator
    - **metrics for judging the LLM-evaluator**
        - <mark style="background: #FFB8EBA6;">classification metrics</mark> = recall, precision, ROC, PR when evaluator outputs binary labels (e.g. factual inconsistency, toxicity)
        - <mark style="background: #FFB8EBA6;">correlation metrics</mark> = measure agreement with humans
            - Cohen’s κ = chance-corrected agreement for categorical data, −1 to 1, 0.21-0.40 fair, 0.41-0.60 moderate
            - Kendall’s τ = rank-order correlation, robust to outliers
            - Spearman’s ρ = rank-order correlation sensitive to magnitude differences
        - metric selection guideline
            - use κ for binary/categorical tasks needing chance adjustment
            - prefer τ or ρ for ordinal data such as Likert scales
            - default to binary evaluator outputs when possible to simplify classification analysis

![[Screenshot 2025-07-21 at 4.41.00 pm.png| center | 600]]

![[Screenshot 2025-07-21 at 4.41.26 pm.png| center | 800]]

# 3 Use cases for LLM-judges
- LLM-evaluator use cases = research demonstrations of “LLM-as-a-Judge” across safety, summarization, QA, and hallucination detection
- <span style="color:rgb(255, 0, 247)">Constitutional AI</span>: Harmlessness from AI Feedback (CAI) = applies LLM critic to reduce harmful responses
	- workflow
		- harmful response detected → LLM-evaluator critiques harmful content
		- model regenerates a safer response guided by critique
		- revised answer used for instruction-tuning
		- preferred answer used for preference-tuning
- <span style="color:rgb(255, 0, 247)">Human-like Summarization Evaluation with ChatGPT</span> = assesses summarization quality with gpt-3.5-turbo
	- scoring modes
		- direct Likert scoring = article + summary → 4–5 dimension ratings
		- pairwise comparison = choose better of two summaries
		- pyramid method = mark presence of semantic content units (SCUs)
		- binary factuality = sentence-level support check
	- findings
		- human-human correlation 0.8-0.9 > LLM-human 0.3-0.6
		- gpt-3.5-turbo > ROUGE, BERTScore, MoverScore on correlation with humans
		- better results when scoring one dimension per prompt rather than many

```
%% Direct Scoring %%
Evaluate the quality of summaries written for a news article. Rate each summary on four 
dimensions: {Dimension_1}, {Dimension_2}, {Dimension_3}, and {Dimension_4}. You should 
rate on a scale from 1 (worst) to 5 (best). 

Article: {Article}
Summary: {Summary}
```

```
%% Pairwise %%
Given a new article, which summary is better? Answer "Summary 0" or "Summary 1". You do 
not need to explain the reason.

Article: {Article}
Summary 0: {Summary_0}
Summary 1: {Summary_1}
```

```
%% Pyramid %%
You are given a summary and some semantic content units. For each semantic unit, mark 
"Yes" if it can be inferred from the summary, otherwise mark "No".

Summary: {Summary}
Semantic content units:
1. {SCU_1}
2. {SCU_2} 
......
n. {SCU_n}
```

- <span style="color:rgb(255, 0, 247)">ChatGPT as a Factual Inconsistency Evaluator for Text Summarization</span> = measures gpt-3.5-turbo on factual consistency tasks
	- tasks
		- entailment inference = yes/no consistency
		- summary ranking = pick consistent over inconsistent summary
		- consistency rating = 1-10 scale
	- outcomes
		- matched or exceeded previous SOTA on entailment without task-specific training
		- sensitivity + specificity still limited
		- higher correlation with human judgment than prior metrics for consistency rating
- <span style="color:rgb(255, 0, 247)">HaluEval</span> = large-scale benchmark for hallucination detection in QA, dialogue, summarization
	- dataset creation
		- gpt-3.5-turbo generates 30k hallucinated samples via two-stage sampling
		- second stage selects most plausible but incorrect answers to craft hard cases
	- evaluation insights
		- best model (gpt-3.5-turbo) reached 58.5 % accuracy distinguishing factual vs hallucinated summaries
		- failures often due to hallucinations conflicting with provided context despite being factually correct globally
- <span style="color:rgb(255, 0, 247)">Evaluating Correctness and Faithfulness of Instruction-Following Models for Question Answering</span> = explores metrics and evaluators for QA
	- dimensions
		- correctness = fulfils user informational need
		- faithfulness = grounded in given context
	- human annotations collected for 1.2 k responses across 3 QA datasets
# 4 Techniques for prompting LLM-judges
- prompting techniques for llm-evaluators = strategies that shape how an evaluator llm judges another model’s output
- cross examination = multi-turn dialogue where an examiner llm interrogates the examinee’s answer
	- examiner asks follow-up questions, incorporates previous turns, and finally labels claim true/false
	- single vs majority setting = 1 round or 3 rounds with majority vote
		- majority recall 0.75-0.84, precision 0.82-0.87
		- ablation without follow-ups → 6-10 % recall drop
- <span style="color:rgb(255, 0, 247)">G-EVAL</span> = three-step chain-of-thought + form-filling framework with GPT-4
	- step1 define evaluation task + criteria
	- step2 generate explicit cot reasoning steps
	- step3 fill evaluation form and normalise score via token probabilities
	- spearman ρ ≈ 0.51, surpassing older metrics
- <span style="color:rgb(255, 0, 247)">SelfCheckGPT</span> = zero-resource hallucination detection via sample consistency
	- generate N=20N=20 alternative answers then measure similarity to target answer
	- higher agreement implies factuality; divergence signals hallucination
	- pairwise comparison prompts outperform direct scoring + g-eval style
- preference-bias insight = llm-evaluator judgements sensitive to prompt wording; fairer preference elicitation improves alignment

![[Screenshot 2025-07-21 at 4.43.08 pm.png| center | 600]]

- <span style="color:rgb(255, 0, 247)">UMBRELA</span> = open-source reproduction of bing relevance assessor using dna prompt
	- query + passage → integer score 0-3
		- 0 unrelated
		- 1 tangential
		- 2 partially answers with extra info
		- 3 directly answers and dedicated to topic
	- dna prompt guides assessor: descriptive, narrative, aspects
	- output format ##final score: k with no reasoning

```
Given a query and a passage, you must provide a score on an integer scale of 0 to 3 with
the following meanings:

0 = represent that the passage has nothing to do with the query, 
1 = represents that the passage seems related to the query but does not answer it, 
2 = represents that the passage has some answer for the query, but the answer may be a 
bit unclear, or hidden amongst extraneous information and 
3 = represents that the passage is dedicated to the query and contains the exact answer.

Important Instruction: Assign category 1 if the passage is somewhat related to the 
topic but not completely, category 2 if passage presents something very important 
related to the entire topic but also has some extra information and category 3 if the 
passage only and entirely refers to the topic. If none of the above satisfies give it 
category 0. 

Query: {query}
Passage: {passage}

Split this problem into steps: 
Consider the underlying intent of the search. 
Measure how well the content matches a likely intent of the query (M). 
Measure how trustworthy the passage is (T). 
Consider the aspects above and the relative importance of each, and decide on a final 
score (O). Final score must be an integer value only.
Do not provide any code in result. Provide each score in the format of: ##final score: 
score without providing any reasoning.
```

- <span style="color:rgb(255, 0, 247)">POLL</span> (panel of llms) = ensemble of smaller evaluators instead of single large judge
	- models: command-r, gpt-3.5-turbo, haiku
	- aggregation = max voting or average pooling
	- yields higher human-correlation than single gpt-4, lowers cost and mitigates intra-model bias

![[Screenshot 2025-07-21 at 4.45.05 pm.png| center | 500]]


# 5 LLM-judge Alignment to Human Judgement
- aligning llm-evaluators = approaches for tailoring evaluator prompts and criteria to domain-specific needs
    - <span style="color:rgb(255, 0, 247)">EvalLM</span> = interactive refinement loop for user-defined evaluation criteria
        - workflow
            - llm-evaluator scores response against criteria and reveals chain-of-thought explanation
            - criteria reviewer suggests merges, splits, or edits to improve clarity
        - outcomes
            - specific criteria → highest agreement with humans, general criteria → lowest
            - user study (with EvalLM vs control)
                - ↑ self-confidence in judging quality (6.71 vs 4.96)
                - ↑ unique outputs evaluated (20.42 vs 10.08)
                - ↓ mental burden (3.92 vs 5.58) and effort (3.50 vs 5.25)
                - ↑ frequency of criteria revisions (22.67 vs 13.33)
    - structured output constraints taxonomy = two tiers of rules for generated text
        - low-level constraints = enforce output format, json validity, length, multiple-choice options
        - high-level constraints = semantic style guides, avoidance lists, hallucination prevention
        - user preference findings
            - gui preferred for low-level constraint specification
            - natural language prompts preferred for high-level constraints
    - criteria drift = inevitable evolution of evaluation standards while grading outputs
        - observations from practitioner study
            - grading a sample of ≥20 outputs first helps refine initial criteria
            - users comfortable labeling outputs during llm-evaluator runtime and then reusing those labels to calibrate the evaluator
            - emergence of new error types → users add new criteria
            - llm-evaluator trust < code-based assertions because code can be directly inspected and edited
# 6 Finetuning LLM-Judges
- <span style="color:rgb(255, 0, 247)">shepherd</span> = llama-2-7b-chat model finetuned as an llm critic for generation feedback
    - training data = community critiques + human annotations
    - performance
        - outperforms alpaca-7b and selfee on feedback helpfulness
        - parity with chatgpt on critique tasks, superior on critiqueeval
        - gpt-4 vs human rating mismatch exposes biases (higher scores, verbosity preference)
- <span style="color:rgb(255, 0, 247)">cappy</span> = 360 M-param roberta evaluator with regression head scoring instruction-response pairs 0 – 1
    - goal = rank and boost outputs on well-defined tasks (accuracy, rouge)
    - results = beats opt-175b on 11 classification tasks, approaches t0-11b performance
- <span style="color:rgb(255, 0, 247)">prometheus</span> = llama-2-chat finetuned for fine-grained rubric-based evaluation
    - preferred over gpt-4 58.6 % and over gpt-3.5-turbo 79.6 %
    - highest correlation with gpt-4 on feedback bench, even surpasses gpt-4 self-agreement
    - ablation insights
        - reference answer = critical; removing it causes largest drop
        - indicates heavy reliance on fuzzy reference matching → reference-free evaluation still challenging
- <span style="color:rgb(255, 0, 247)">criticgpt</span> = llm critic specialised for code generation bugs
    - input = (question, code answer)
    - output = pinpointed critique highlighting potential errors
# 7 Pros & Cons of LLM-Judges
- empirical support for llm-evaluators
    - mt-bench results = gpt-4 evaluator with direct + pairwise scoring reached 85 % agreement with humans (ties excluded), surpassing human-human 81 %
        - humans considered gpt-4 judgments reasonable 75 % and switched their own choices ⅓ of the time
- observed evaluator biases
    - position bias = preference for candidate in first slot during pairwise comparison
    - verbosity bias = higher scores awarded to longer answers even when quality inferior
    - self-enhancement bias = evaluator favors responses produced by its own model family
- limitations of finetuned judge models (judgeLM, pandaLM, auto-J, prometheus)
    - behave as task-specific classifiers; correlation higher with each other than with gpt-4
    - deberta-classification = matches vicuna models → small discriminative models suffice on same task
    - vicuna-generation > vicuna-classification → next-token training objective yields stronger evaluator
    - strong in-domain accuracy yet weaker than gpt-4 on
        - generalizability
        - fairness
        - aspect-specific evaluation
    - scheme transfer failure = models trained for pairwise collapse on direct scoring and vice-versa
- blind-spot analysis = interpretable checklist framework probes evaluator skill across
    - LF coherence
    - factuality
    - instruction following
    - reasoning proficiency
# 8 Summary 
- applying llm-evaluators
    - task nature
        - objective tasks = factuality, toxicity, instruction-following
            - direct scoring = preferred because each single answer may still carry defects
            - binary simplification = convert to true/false when possible to ease evaluation
        - subjective tasks = tone, persuasiveness, writing style
            - pairwise comparison = more reliable than absolute scores
    - scoring scheme selection
        - direct scoring binary → classification metrics = recall, precision, roc, cohen’s κ
        - pairwise comparison → agreement metrics
            - cohen’s κ = default for rater agreement
            - if certain of ground truth, treat pairwise as binary classification and report recall / precision
    - prompting best practices
        - cot + n-shot examples improve reliability during development
        - minimise biases: randomise candidate order to combat position bias, limit token budget to reduce verbosity bias
        - instruct evaluator to output constrained labels (e.g. “correct”, “incorrect”) for easier parsing
- evaluating llm-evaluators
    - alignment measurement = compare with human experts not just crowd workers
        - non-expert correlation tends to overstate performance
    - metrics
        - percentage agreement = quick sanity check
        - cohen’s κ adjusts for chance agreement
        - rank correlations (kendall’s τ, spearman’s ρ) for ordinal scores
    - robustness checks
        - cross-dataset variance reveals blind spots; models often fail on some tasks even when strong overall
        - test for biases
            - position bias = fixed-slot preference
            - verbosity bias = longer answers over-scored
            - self-enhancement bias = evaluator prefers its own model family outputs
    - stress tests = adversarial prompts, interpretable checklists for coherence-factuality-reasoning
- operating llm-evaluators
    - dev-time evaluator
        - few hundred samples acceptable → tolerate api latency and cost
        - use chain-of-thought, multi-step prompting, and detailed rubrics
    - production guardrail
        - low latency, high throughput required → finetune small classifier or reward model
            - bootstrap on open-source corpora + internal labelled data
            - monitor drift and periodically refresh labels via active learning
    - finetuned evaluator considerations
        - reference answer inclusion critical for performance (prometheus ablation)
        - models act like task-specific classifiers; scheme transfer (direct ↔ pairwise) may fail
        - generation-objective evaluators (next-token) can outperform pure classification heads
    - reliability ceiling
        - gpt-4 evaluator cohen’s κ ≈ 0.84 < human-human 0.97 → human review still needed for high-stakes use
- takeaway = llm-evaluators provide scalable, fast judgements but must be matched to task type, carefully prompted, bias-controlled, and regularly benchmarked against expert humans for trustworthiness

---






