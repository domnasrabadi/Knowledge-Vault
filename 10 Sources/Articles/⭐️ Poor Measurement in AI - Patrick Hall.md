---
type: article
status: structured
quality: 1
topics:
  - evaluation-metrics
  - model-monitoring
  - llm-risks
  - model-risk-validation
source: ""
created: 2025-06-21
published:
author: Patrick Hall
flashcards: none
updated: 2025-12-28
---
From his slides pack

# 1 Poor measurement and other malpractice
- "evals are surprisingly often all you need" - Greg Brockman 2023
- however big difference between evals + scientific measurement 

| Evals                                                         | Scientific Measurement                                          |
| ------------------------------------------------------------- | --------------------------------------------------------------- |
| massive batteries of computational tests                      | acknowledges error and variance, conducts multiple measurements |
| based on test data + some (sometimes poor) human annotations  | calibrates to ground truth, informed by SMEs                    |
| focused on simulation, not real environment risks             | uses designed experiments                                       |
| test questionable capabilities e.g. self-awareness            | demands reproducibility                                         |
| lack standardisation + consitency, problems w reproducibility | focus on real world outcomes                                    |
| suffer from task contamination                                |                                                                 |

- Goodhart's law = "when a measure becomes a target, it ceases to be a good measure"
	- without checking in w SMEs + real world outcomes, any data-driven measurement can become a counterproductive proxy game 
	- often we need to use proxy objectives - since we know how to measure and optimise those
		- but need to be careful to use SME + business context 
- task contamination 
	- AI systems can be trained on data that should be witheld for eval purposes
		- often unintentional
	- some AI companies withold training data info + perform extremly well on public benchmarks
		- sometimes, models perform better on benchmarks available before release data
		- versus worse performance on newer benchmarks after release
- real risks of AI vs existential risk 
	- salient risks are not yet:
		- acceleration, acquiring resources, avoiding being shut down, replication 
	- worst real risks today
		- addition, wellbeing, automated surveillance, deep fakes, disinformation, social credit scoring
	- realistic risks 
		- abuse/misuse for disinformation
		- automation complacency 
		- data privacy violations 
		- errors (hallucinations)
		- IP infringements
		- systematically biased or toxic outputs 
		- traditional and ML attacks
		- workforce displacement
$$
\large risk \approx \text{likelihood of harm} \times \text{cost of harm}
$$
- be realistic about LLMs
	- hype + marketing != scientific resuts
	- LLMs are often wrong, LLMs can inflict harm, LLMs are hacked and abused
	- acknowledge human biases
		- confirmation bias 
		- dunning-kruger effect
		- funding bias 
		- groupthink 
		- mcnamara fallacy 
# 2 Emerging AI Measurement science
## 2.1 data science vs science 
- **data science method**
	- assume big payoff, install gpu + download python
	- collect wrong or biased data
		- often from internet or exhaust of most available business process
	- surrender to confirmation bias 
		- study collected data to form hypothesis 
		- use same data from hypothesis generation to test our hypothesis 
		- test hypothesis with high-capacity learning algorithm 
			- e.g. can fit almost any loosely correlated X and y well 
		- change hypothesis until results are "good"
	- don't bother reproducing
- **scientific method**
	- develop a credible hunch based on prior experiments or literature review 
	- record a socio-technical hypothesis that is falsifiable
		- what is intended real world effects for users?
		- what is the null hypothesis?
	- collect data
		- appropriate, not just available 
		- design of experiment
	- test hypothesis 
		- structured experiments, baselines, controls, randomisation, blinding, multiple measurements
		- significance of treatment effects 
	- formal validation 
	- independent replication of results 
## 2.2 NIST ARIA: Assessing risk + impacts of AI 
- [see link here](<https://ai-challenges.nist.gov/uassets/7#:~:text=ARIA%20(Assessing%20Risks%20and%20Impacts,AI%20risk%20and%20impact%20assessments.>)
- the NIST Assessing Risks and Impacts of AI (ARIA) program = a testing, evaluation, validation and verification (TEVV) initiative 
	- designed to measure how AI systems behave “in the wild,” beyond controlled laboratory benchmarks
	- goal = develop standardized guidelines, tools, methodologies and metrics 
		- so that organizations can evaluate AI for validity, reliability, safety, security, privacy and fairness once deployed
	- 1st iteration (ARIA 0.1) = pilot evaluation focusing on large language models (LLMs)
		- using three proxy scenarios drawn from the NIST AI Risk Management Framework
		- coupled with “test packets” that define permitted and prohibited behaviors
		- test packets = structured datasets of permitted vs. prohibited model behaviors
- objectives
	- **Quantify real-world behavior** = move beyond accuracy and bias metrics to measure how AI systems perform in complex, social environments
	- **Standardize methodologies** Produce repeatable guidelines and tools for evaluating AI risks and impacts, enabling cross-organization comparability
	- **Inform decision-making** provide metrics and insights that can guide developers, deployers and regulators in choosing, configuring or restricting AI systems
- what is it about and how it works?
	- focused on real-world impacts
	- exclusively uses human labelling/annotation
	- designed experiments involving human subjects
	- 3 measurement levels
		- <mark style="background: #FFB8EBA6;">model testing</mark> = assess raw model outputs against a risk criteria 
		- <mark style="background: #FFB8EBA6;">red teaming</mark> = simulate adversarial or stress inputs to probe for failure modes
		- <mark style="background: #FFB8EBA6;">field testing</mark> = observe system behaviour in user-like scenarios
	- currently being piloted 
- NIST ARIA - contextual robustness index 
	- graph based risk + performance assessment instrument - incorporates real world context
	- uses signals from model testing, red teaming, field testing + user questionnaries for each tested model
	- enables
		- assessing + visualising results at various scales + levels
		- debugging of the CoRIx instrument itself
	- presents aggregate results across testing levels
		- for dimensions such as physical safety, bias, accessibility + other real-world desirata 
## 2.3 H20.ai Human-calibrated Automated Testing (HCAT)
- from Agus, focusing on RAG systems (input control)
- strikes balance between full human labelling + automation
	- which is crucial for adoption 
- uses embeddings to ensure analysis occurs on your data 
	- uses clusters + viz in embedding space to enhance testing coverage + explainability
	- automatically generates test cases across a cluster of documents
- uses conformal classification to calibrate automated results to human labelling









