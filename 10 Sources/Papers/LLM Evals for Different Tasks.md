---
type: paper
status: structured
quality: 1
topics: [llm-evaluation, evaluation-metrics, human-in-the-loop]
source: ""
created: 2025-07-19
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Eugene Yan
- Category: article
- Document Tags: great 
- URL: https://eugeneyan.com/writing/evals/

# 2 Tasks & Metrics
- evaluation toolbox = task-specific sets of metrics and diagnostics for language model outputs
## 2.1 classification / extraction
- <mark style="background: #FFB8EBA6;">recall</mark> = proportion of ground-truth positives retrieved
- <mark style="background: #FFB8EBA6;">precision</mark> = proportion of predicted positives that are correct

> [!NOTE] Accuracy is often too coarse a metric to be useful - instead separate it into recall & precision, ideally across thresholds

- <mark style="background: #FFB8EBA6;">ROC curve</mark> = plot of true-positive rate vs false-positive rate across thresholds
	- ROC-<mark style="background: #FFB8EBA6;">AUC</mark> = aggregate of ROC performance from 0 to 1
	- advantages = threshold-agnostic, robust to class imbalance, scale-invariant
- <mark style="background: #FFB8EBA6;">PR curve</mark> = plot showing precision–recall trade-off across thresholds
	- higher threshold → ↑ precision & ↓ recall
		- lower threshold → opposite
	- PR-AUC = area under PR curve summarising performance
	- twin-line variant = precision and recall drawn separately for clarity

![[Screenshot 2025-07-20 at 10.13.45 am.png| center | 700]]

- distribution of predicted probabilities = histogram for each class
	- ideal shape = two distinct peaks at 0 and 1 indicating confident separation
	- can quantify separation of distributions via <mark style="background: #FFB8EBA6;">Jensen-Shannon divergence</mark> = symmetric measure of separation
		- low separation warns that threshold choice in production will be unstable	

$$
\Large
JSD(P\parallel Q)=\tfrac12\bigl[KL(P\parallel M)+KL(Q\parallel M)\bigr],\;M=\tfrac{P+Q}{2}
$$

![[Screenshot 2025-07-20 at 10.17.33 am.png| center | 700]]


## 2.2 summarization
- abstractive summarization = generate condensed paraphrase of source document
- factual consistency = finetuned NLI model judges if summary is entailed by source
	- premise = source, hypothesis = summary
	- contradiction ⇒ hallucination
	- few-hundred labelled pairs can lift ROC-AUC from 0.56→0.85
- relevance = learned metric via finetuned NLI or reward model scoring preference pairs
	- reward model = language model with linear head outputting scalar quality score
		- adopted by Stiennon et al 2020, updated summarisation LLM to output numeric score instead of text summary
		- via adding linear head to output scalar value, trained on pairs of summary preferences to give higher scores to better summaries
		- for pair of summaries $y_0, y_1$, the minimise the loss function
			- encourages RM to give higher to preferred summary 
			- sigmoid function $\sigma$ squashes difference in rewards to between 0 and 1 

$$
\Large
loss(r_\theta) = -\mathbb{E}_{(x,y_0,y_1,i)\sim D}\bigl[\log\bigl(\sigma\bigl(r_\theta(x,y_i) - r_\theta(x,y_{1-i})\bigr)\bigr)\bigr]
$$

- length checks = ensure summary within required token span
- human review remains essential as automated metrics are trained on human judgements
## 2.3 translation
- <mark style="background: #FFB8EBA6;">chrF</mark> = character n-gram FF-score capturing lexical overlap
	- computes precision and recall of character n-grams between candidate vs reference translation 
		- Precision $chrP$ measures % of character n-grams in candidate that match the reference
		- Recall $chrR$ measures % character n-grams in reference and captured by candidate
		- done for various values of $n$ up to 6
	- then uses harmonic mean w $\beta$ as parameter to control relative importance of Precision & Recall (similar to F-Beta score)

$$
\Large
\text{chrF}\beta = (1 + \beta^2) \frac{chrP \cdot chrR}{\beta^2 \cdot chrP + chrR}
$$

- sacreBLEU = standardised implementation of chrF - ensures consistent results across systems/tasks 
- <mark style="background: #FFB8EBA6;">BLEURT</mark>, <mark style="background: #FFB8EBA6;">COMET</mark>, <mark style="background: #FFB8EBA6;">COMETKiwi</mark> = learned quality metrics leveraging pretrained models
	- BLEURT introduced by Google Research, 2020 - improves on BLEU by using BERT
## 2.4 toxicity
- RealToxicityPrompts & BOLD = adversarial prompt sets for stress testing
- metric = proportion of toxic generations for benign vs toxic prompts
## 2.5 copyright
- exact regurgitation = verbatim reproduction of protected text
- near-exact reproduction = lightly altered yet recognisable copies
# 3 Human Annotation
- most automated evals rely on human annotations - classification tasks need gold references from labelled human data 
	- also even after initial evals, active learning = iterative sampling of instances for new human labels
    - increase precision = label high-probability positives to expose false positives
    - increase recall = label low-probability negatives to surface false negatives
    - increase confidence = label uncertain predictions (probability 0.4–0.6)
- human annotation dimensions (Chang et al.)
    - accuracy = factual correctness
    - relevance = pertinence to task and input
    - fluency = grammatical readability
    - transparency = clarity of model reasoning (e.g. chain-of-thought)
    - safety = absence of toxicity, bias, misinformation
    - human alignment = adherence to human values and preferences
# 4 Calibrate to level of risk 
- calibration of evaluation bar
    - risk-adjust scores to match application stakes
    - balance potential benefit vs harm
    - avoid perfection paralysis; start small, collect feedback, iterate
- task-specific recommended evals
    - classification = recall, precision, ROC-AUC, separation of distributions
    - summarization = factual consistency (NLI), relevance (reward model)
    - translation = chrF, BLEURT, COMET, COMETKiwi
    - toxicity = RealToxicityPrompts, BOLD
    - copyright = regurgitation checks with popular books & code

