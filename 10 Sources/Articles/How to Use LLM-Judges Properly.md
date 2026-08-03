---
type: article
status: structured
quality: 2
topics: [llm-judges, llm-evaluation, prompting]
source: ""
created: 2026-01-01
published:
author: "https://x.com/manthanguptaa/article/2006222014265393316"
flashcards: none
updated: 2026-01-01
---

>[!abstract] TLDR
> - LLM Judges work well when you:
> 	1. use reference based evaluation instead of pointwise scoring
> 	2. debias pairwise comparisons w position swapping
> 	3. ensemble across multiple models
> 	4. require reasoning before scores
> 	5. calibrate against human judgements 
> - skip LLM Judges when ground truth exists or for safety/high-risk decisions

# Why traditional eval methods fail 
- exact match works great for classification + structured output 
	- fails completely on open ended generation 
	- e.g. "The Capital of France is Paris" vs "Paris is France's capital city" = 0% exact match
- BLEU & ROUGE were designed for MT + summarisation
	- they penalise valid paraphrasing + reward surface level similarity 
- human evals = gold standard but not scalable 
	- expensive, slow and surprisingly inconistent (IA often < 80%)
	- becomes bottleneck in development when needing to eval 1000s of responses
- LLM-as-Judge is a good middle ground 
	- nuanced understanding like humans at speed closer to automated metrics
		- LLM Judges are now de-facto eval for agentic systems
	- i.e. pareto principle → 80% of the bang for 1% of the buck

# Evaluation modes for LLM Judges
1. **Pointwise evaluation** 
	- scores a single response based on the question alone, without any reference to compare against
	- can be binary or using likert scale (quality, moderation)

```text
You are an expert evaluator. Assess the following response based on the question asked.

## Evaluation Criteria
- Correctness: Is the information factually accurate?
- Completeness: Does it fully address the question?
- Helpfulness: Is it clear and actionable?

## Scoring
Rate the response from 1-5 where:
1 = Poor, 2 = Below Average, 3 = Average, 4 = Good, 5 = Excellent

Question: {question}
Response: {response}

Provide your reasoning first, then the final score.
```

2. **Reference based evaluation** 
	- compares the generated response against a known good "gold standard" answer
	- particularly useful when you have ground truth data and want to measure how close your model's outputs are to the ideal answer (accuracy, regression)

```text
You are an expert evaluator. Compare the following response against the reference answer.

## Task
Evaluate how well the response matches the reference in terms of:
- Factual alignment: Does it convey the same information?
- Completeness: Does it cover all key points from the reference?
- Accuracy: Are there any contradictions or errors?

## Scoring
Rate from 1-5 where:
1 = Completely misaligned, 2 = Mostly incorrect, 3 = Partially correct,
4 = Mostly correct, 5 = Fully aligned with reference

Question: {question}
Reference Answer: {reference}
Response to Evaluate: {response}

Provide your reasoning first, then the final score.
```

3. **Pairwise evaluation** 
	- presents two responses side-by-side and asks the judge to pick the better one
	- widely used for model comparison, RLHF preference data collection, and A/B testing
		- Chatbot Arena uses this extensively

```text
You are an expert evaluator. Compare the two responses below and determine which one better answers the question.

## Evaluation Criteria
Consider: accuracy, completeness, clarity, and helpfulness.

Question: {question}
Response A: {response_a}
Response B: {response_b}

## Instructions
1. Analyze both responses against the criteria
2. Explain the strengths and weaknesses of each
3. Declare a winner: A, B, or Tie

Your analysis:
```

4. **Listwise evaluation** 
	- extends pairwise to multiple responses, asking the judge to rank them from best to worst
	- useful for leaderboard generation or selecting the best response from multiple candidates

```text
You are an expert evaluator. Rank the following responses from best to worst.

Question: {question}
Response 1: {response_1}
Response 2: {response_2}
Response 3: {response_3}

## Instructions
Rank all responses from best (1st) to worst (last).
Provide brief reasoning for your ranking.

Ranking:
```

5. Hybrid approaches
	- you can also create variations w multi-dimensional rubrics
		- e.g. pointwise scoring separately for various aspects + binary reference comparisons

# Crafting effective LLM Judge Prompts
- quality of your judge prompt DIRECTLY impacts reliability of your evals 
	- a well structured judge prompt has 4 key components (below)
1. **clear task definition** 
	- state exactly what model should evaluate 
	- be specific not vague e.g. 
		- *"evaluate the factual accuracy of this response compared to the reference using ..."*
2. **detailed evaluation critieria** 
	- define what *"good"* means
	- specify exactly what that aspect entails e.g.
		- *correctness = all factual claims are accurate and verifiable from source documents*
		- *completeness = addresses all atomic claims or parts of the question without omissions*
		- *clarity = well organised, easy to understand for a layman and free of jargon* 
3. **explicit scoring rubric** 
	- provide clear definitions for each score level e.g. likert scale of 1-5
	- without this, a 3/5 can be highly variable between runs 

```text
1 = Completely incorrect or irrelevant
2 = Mostly incorrect with minor valid points
3 = Partially correct but missing key information
4 = Mostly correct with minor issues
5 = Fully correct and comprehensive
```

4. **few shot examples**
	- include examples of scored responses → significantly boosts consistency 
	- show examples of good and bad 
		- e.g. show what a "2" looks like versus a "4" for your specific criteria
- an example production grade judge prompt (below)
	- defines exactly what each score means, no ambiguity
	- shows concrete examples of high + low scores
	- forces reasoning before scoring
	- uses a structured output format for easy parsin 

```markdown
You are an expert evaluator assessing the quality of an AI assistant's response.

## Your Task
Evaluate the response below against the reference answer. Your evaluation should be thorough, fair, and consistent.

## Evaluation Criteria

### Correctness (0-2 points)
- 0: Contains factual errors or contradicts the reference
- 1: Partially correct but missing key facts or contains minor inaccuracies
- 2: Factually accurate and aligned with the reference

### Completeness (0-2 points)
- 0: Misses most key points from the reference
- 1: Covers some key points but has significant gaps
- 2: Addresses all major points from the reference

### Clarity (0-1 point)
- 0: Confusing, poorly organized, or difficult to understand
- 1: Clear, well-structured, and easy to follow

## Examples

### Example 1: Score 5/5
Question: What causes seasons on Earth?
Reference: Earth's axial tilt of 23.5 degrees causes seasons. As Earth orbits the Sun, different hemispheres receive more direct sunlight at different times, creating summer and winter.
Response: Seasons occur because Earth's axis is tilted at about 23.5 degrees. This means as our planet orbits the Sun throughout the year, the Northern and Southern hemispheres take turns being tilted toward the Sun, receiving more direct sunlight and experiencing summer.
Analysis: Fully correct (mentions axial tilt and its effect), complete (covers the mechanism), and clearly written.

### Example 2: Score 2/5
Question: What causes seasons on Earth?
Reference: [same as above]
Response: Seasons happen because Earth gets closer to and farther from the Sun during its orbit.
Analysis: Incorrect (this is a common misconception—Earth's distance from the Sun does not cause seasons), incomplete (does not mention axial tilt), though clearly written.

## Input
Question: {question}
Reference Answer: {reference}
Response to Evaluate: {response}

## Instructions
1. Carefully compare the response against the reference answer
2. Score each criterion according to the rubric above
3. Provide specific evidence for each score
4. Calculate the total score (out of 5)

## Output Format

### Analysis
[Your detailed analysis with specific quotes and comparisons]

### Scores
- Correctness: X/2 - [brief justification]
- Completeness: X/2 - [brief justification]
- Clarity: X/1 - [brief justification]

### Total Score: X/5
```

- additional tips
	- prefer discrete scoring, not continuous 
		- LLMs are better at classification than regression 
		- use likert scales 1-5, not 0 to 100 or 0.0 to 1.0 → these tend to cluster around certain values
	- set temperature zero or near-zero (`0.1-0.2`)
		- you want close to deterministic outputs for evals 
	- ask for reasoning before the score
		- this is crucial → autogressive LLMs need to think through the eval systematically 
		- rather than jump to a score/number
		- this reduces arbitrary scoring + makes eval more repeatable + debuggable

# Limitations & Biases of LLM Judges
- inconsistency 
	- even with temp=0, can get different results (due to GPU batching, API side variations, machine epsilon)
		- a 3/5 can be 4/5 tomorrow
	- so beware when trying to detect small improvements between model versions
		- a 0.1 improvement likely can be noise rather than signal 
- criteria ambiguity 
	- each model has its own implicit assumptions + definitions based on training data 
	- so you need to concretely define what you mean by your eval aspect e.g. correctness
	- without this, different models can systematically disagree when you ensemble 
- known biases 
	- position bias 
	- verbosity bias 
	- self-enhancement bias 
	- authority bias 
	- format bias 
- cost
	- frontier models can be expensive, reserve for highest priority evals or meta-evals
	- don't use for rapid iteration, can add up quickly 
	- but beware cheaper models → quality degrades

# When not to use LLM Judges
- situations to avoid using LLM judges (or relying on them completely)
	- **when ground truth exists** 
		- if deterministic eval data exists, use that instead 
			- e.g. tool call evals, structured output evals, tool input evals
		- cheaper, faster & 100% explainable + reliable
	- **safety critical evals** 
		- e.g. content moderation, toxicity detection, anything w severe consequences
		- use judges as 1 signal among multiple + incorporate human review
	- **domain expertise requirements** 
		- LLMs lack deep contextual/domain knowledge e.g. your company policies 
			- they may confidently score incorrect responses highly 
		- expert human evals remain necessary for at least validation + calibration here 
	- **when explainability is needed**
		- e.g. regulated industries - need to know why response was scored what it was
			- LLM judge may not be defendable to regulators or in court
		- LLM responses not completely auditable like rule-based systems
	- **some low-stakes, very high volume scenarios** 
		- e.g. for millions of responses & accuracy matters less than throughput 
		- simpler heuristics could be more effective + fraction of cost
			- e.g. well tuned classifier or embedding similarity
- best practice hybrid approach (combines multiple methods) 
	- deterministic checks first → validate structure, format + any computable criteria 
	- LLM as judge for subjectivity/nuance → use for subjective qualities 
	- human review + calibration → sample 5-10% for expert eval + calibration
	- escalation for edge cases → flag low confidence or borderline scores for human review 

# LLM Judge Optimisations 
1. calibrate against humans/SMEs
	- before trusting the judge in production, validate it against human annotations
	- sample 100-200 responses, get human labels, compare to LLM scores
	- calculate metrics:
		- correlation - does LLM's ranking match human ranking?
		- Cohen's Kappa - how often does the Judge agree w humans beyond chance?
		- systematic bias - does LLM consistently score higher or lower than humans?
	- if LLM Judge disagrees w humans > 20-30% of the time, revisit the prompt or criteria
2. ensembling judges 
	- use multiple model families to eval each response + aggregate their score
		- can increase your cost but highly worth it for the reliability in high-stakes evals 
	- reduces impact/bias of any single model + improves reliability & consistency 

```python
def ensemble_evaluate(question, response):
    scores = {
        'claude-opus': evaluate_with_claude_opus(question, response),
        'gpt5_2': evaluate_with_gpt5_2(question, response),
        'gemini': evaluate_with_gemini(question, response)
    }
    # Weighted average
    weights = {'claude-opus': 0.4, 'gpt5.2': 0.4, 'gemini': 0.2}
    return sum(scores[m] * weights[m] for m in scores)
```

3. down-weight the generator model (in ensembling)
	- due to self-preference bias, rely less in overall aggregated results when reviewing the same model family 

```python
def get_weights(generator_model):
    base_weights = {'claude-opus': 0.33, 'gpt5_2': 0.33, 'gemini': 0.33}
    if generator_model in base_weights:
        # Reduce generator's weight, redistribute to others
        base_weights[generator_model] = 0.15
        others = [m for m in base_weights if m != generator_model]
        for m in others:
            base_weights[m] = 0.425
    return base_weights
```

4. use reference responses where possible 
	- pointwise scoring is often isolated + less reliable than reference-based
	- always use ground-truth or expected responses if you have them 
		- gives the judge concrete standard to compare against rather than open to interpretation
5. de-bias pairwise comparisons 
	- position bias remains real + measureable 
	- run all pairwise comparisons multiple times w swapped positions 

```python
def debiased_pairwise(question, response_a, response_b):
    # Run A vs B
    result_ab = judge(question, response_a, response_b)
    # Run B vs A (swapped)
    result_ba = judge(question, response_b, response_a)
    
    # Aggregate
    if result_ab == "A" and result_ba == "B":
        return "A"  # A wins in both positions
    elif result_ab == "B" and result_ba == "A":
        return "B"  # B wins in both positions
    else:
        return "Tie"  # Inconsistent results = no clear winner
```

6. require reasoning before scores 
	- always structure your prompt to elicit reasoning before the final score 
	- genuinely improves eval quality
		- forces model to systematically think throught the eval assessment

```text
## Output Format
First, provide your detailed analysis of the response.
Then, based on your analysis, provide the final score.

Analysis: [Your reasoning here]
Score: [X/5]
```

# Summary/Conclusion of LLM Judges
1. Never trust a single judge
	- Whether it is position bias, self-enhancement bias, or simple inconsistency, single-model evaluation is inherently unreliable. 
	- Ensemble across models, de-bias pairwise comparisons, and always validate against human judgments.
2. Reference responses are your anchor. 
	- Pointwise evaluation ("rate this response 1-5") is the least reliable mode. 
	- When you have ground truth, use it. 
	- Reference based evaluation grounds the LLM in something concrete rather than its own subjective interpretation of "good."
3. Design for transparency
	- Require reasoning before scores. 
	- Log everything. When an evaluation seems wrong, you need to understand why. 
	- Black-box scores are useless for debugging.
4. Build a hybrid pipeline. 
	- Deterministic checks first, LLM judges for nuance, human review for calibration and edge cases. 
	- No single method is sufficient.
5. Calibrate continuously. 
	- Your LLM judge will drift as models update and your use cases evolve. 
	- Regular comparison against human judgments is not optional, it is the only way to know if your evaluations still mean anything.
- LLM as a judge will not replace human evaluation entirely. But implemented correctly, it gets you 80% of the accuracy at 1% of the cost, which is often exactly the tradeoff you need during rapid development.
- The teams that struggle with LLM as a judge are the ones who treat it as a black box. The teams that succeed are the ones who understand its failure modes and design around them.








