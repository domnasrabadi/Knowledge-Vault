---
type: book
status: structured
quality:
topics: [llm-evaluation, agent-evaluation]
source: ""
created: 2026-06-06
published:
author: ""
flashcards: none
updated: 2026-06-08
---
![[Screenshot 2026-06-06 at 11.22.33 am.png| center | 500]]

# Intro 
- Unlike traditional software with deterministic outputs, LLM pipelines produce responses that are often subjective, context-dependent, and multifaceted. 
	- A response might be factually accurate yet inappropriate for the context. It might sound persuasive while conveying incorrect information. It might also address most but not all parts of the user’s question. 
	- These ambiguities make evaluation fundamentally different from conventional software testing or even traditional machine learning validation.
- This is the kind of issue that evaluation is designed to surface: a systematic check of the chatbot’s answers on common policy questions could have flagged the discrepancy before the chatbot went live
- Core challenge of evals
	- How do we assess whether an LLM pipeline is performing adequately? 
	- And how do we diagnose where it is failing?
## What is evaluation?
- Evaluation is the _systematic measurement of quality in an LLM application._ A good evaluation produces results that are interpretable and actionable. In some cases evaluation produces a quantitative metric
- In other cases, the “metric” is generated with more judgment involved. A set of experts, or sometimes the product team itself, may review outputs and rate them for qualities such as clarity, tone, or usefulness. Both approaches fall on a spectrum of rigor: from quick, informal checks that guide early iteration, to carefully defined rubrics and systematic sampling that support production systems
- A single application will usually require multiple evaluations, each designed to capture a different dimension of performance
- Evaluations can then be integrated into the application in several ways:
	- Monitoring - continuous checks that run in the background to detect drift or degradation over time.
	- Guardrails - evaluations placed in the critical path, allowing the system to block, retry, or fall back when outputs fail predefined criteria.
	- Improvement mechanisms - evaluations used to generate feedback, such as labeled examples for fine-tuning, curated few-shot prompts, or systematic identification of failure cases that motivate architectural changes.
## Evaluation throughout LLM Lifecycle
- evals occur during each stage of an LLM lifecycle
	- pre-training 
		- largely intrinsic, next-token prediction → assess if model has absorbed statistical patterns from language
		- does not assess usefulness for many downstream tasks
	- post training
		- adapts it for practical use, pre-training can help generalise to many tasks
		- focused on steering model towards desired behaviours → instruction following, task completion, avoiding unsafe responses
		- post-training has 2 phases
			- fine-tune the model on curated prompts + good responses 
				- allows model to learn to produce desirable answers
			- using preference data (pairs of responses, with a preferred/winning response) to steer model further to better responses
		- evals in this stage shift from next-token-prediction to benchmarks focusing on tasks users care about
	- LLM applications
		- model has already been trained, now is to integrate and use it within a concrete workflow
			- e.g. triage emails, customer support, analyse documents
		- evals here should be tailored to the goals of the data + specific application 
			- sometimes post-training evals may overlap with the task e.g. coding assistant
			- however, most of time it isn't 
		- responsibility for evals then on the development team to:
			1. define what success means
			2. design appropriate metrics
			3. implement monitoring to verify system performs reliably for intended use
## Evaluation in Applications
- main goal is to build a system around the model
	- need to decide what the product should achieve
	- translate that into prompts + agent logic
	- then verify that model outputs are acceptable
- challenges of LLM applications
	- objectives are vague at first → can sound simple but ambiguities appear once you inspect outputs e.g. how much detail, what format, what exclusions?
	- instructions might have gaps → hard to express full intent in natural language prompts, leads to inconsistent/incomplete behaviours
	- behaviour changes on new data → may work on handful of test cases but can fail on variability of real inputs
## 3 Gulfs of LLM Application Development
- 3 gulfs = framework to reason and approach these challenges more systematically 
	- they provide a shared vocabulary for LLM application failures → helping you debug and identify what type of failure it is
		- <mark style="background: #FFB8EBA6;">comprehension</mark> = developer didn't systematically understand failures (i.e. what the input/output data actually looks like)
		- <mark style="background: #FFB8EBA6;">specification</mark> = prompt didn't make requirements clear enough
		- <mark style="background: #FFB8EBA6;">generalisation</mark> = LLM isn't applying instructions consistently 
- each gulf has different implications:
	- understanding your data and outputs;
	- making intent explicit;
	- and recognising that LLMs will still misapply instructions in some cases

- gulf of comprehension 
	- developer needs to have solid grasp of the inputs/data to build effective prompts/pipelines
	- also applies to outputs, need a clear sense how LLM behaves on those inputs
		- cannot read every output it generates, but still needs to recognise common ways it succeeds or fails
		- otherwise it's easy to be misled by a few good examples & miss patterns that only show up at scale
	- requires strategies to characterise inputs/outputs at scale
		- so we really know how the data looks + how system behaves without manually inspecting everything

- gulf of specification 
	- i.e. the gap between our intent vs our instructions 
		- what we want vs what we actually tell LLM to do e.g. intent (task in mind) is hard to capture via prompts/pipeline logic
		- natural language is imprecise + has gaps in how we can phrase things → can both lead to large differences in behaviour 
	- e.g. *"Extract the sender's name and summarise the key requests in this email"*
		- should summary be paragraph or bullet list?
		- should sender be full name, display name, full email address or something else?
		- should implicit requests be included or just explicit?
		- how concise should summary be?
	- LLM cannot fill in the choices for you
		- need to make them explicit otherwise the system will guess
		- and 2 runs of the same pipeline would get different formats/detail/edge-case handling
	- closing this gap requires making expectations explicit + aligning them closely w the data the pipeline will see

- gulf of generalisation 
	- the fact that LLMs can behave unpredictably even when comprehension + specification are handled well 
		- i.e. the gap between your data + how the LLM generalises to it
		- even if you have well-scoped + clearly written prompt → LLM is still prone to errors
	- these errors only become visible when the system is exposed to full variety of real-world data 
		- this is unavoidable, no matter how good the models become → there will always be cases of wrong outputs

## Why LLM Evals are Challenging
- evaluation is not once-off, its iterative and requirements become more clear only after seeing real outputs
- start by examining outputs (comprehension), then find mistakes due to either specification or generalisation
	- if prompt doesn't make requirements explicit → can be fixed w better instruction or pipeline design
	- if prompt already well specified but LLM still fails → generalisation failure, automated evals can measure how often that happens
## The LLM Eval Lifecycle
- 3 gulfs = main ways LLMs go wrong
- the `Analyse-Measure-Improve` lifecycle = framework to make gulfs visible + address them 

![[Screenshot 2026-06-07 at 1.45.35 pm.png| center | 500]]

- Analyse
	- addresses gulf of comprehension
	- look at real inputs + outputs to see how the system is behaving
	- goal is to identify failure modes, not quantify them 
- Measure
	- after `Analyse`, you'll know what kind of mistakes system makes (specification vs generalisation)
	- Measure = quantifying the generalisation issues
		- how common they are + what contexts they appear
		- this is done via designing LLM judges that can run at scale on unlabelled data 
- Improve
	- decide how to adjust system based on `Analyse` + `Measure` stages
	- path followed depends on source of errors:
		- specification → fix via tightening the prompt or adjust pipeline logic 
		- generalisation → need stronger interventions e.g. more examples, refining retrieval, fine tuning on labelled data


---

# LLMs & Eval Basics
- 2 main evaluation modes
	- **absolute evaluation** = judging whether one configuration (prompt, model, tool setup etc) is good enough to ship
	- **comparative evaluation** = comparing multiple options to decide which is better (AB tests, pairwise, ranking, leaderboards)
## Components of LLM applications 
- single-step LLM calls
	- 
- conversations (multi-turn)
	- 
- retrieval
	- 
- tools
	- 
- agents
	- 
## Evaluation Setups
- 

---

# Error Analysis
- s

>[!info] Grounded theory
> - Grounded theory = qualitative research method used to build theory from data, rather than start with a fixed theory + test it
> - researcher repeatedly:
> 	- reads the data, 
> 	- identifies patterns, 
> 	- compares examples, 
> 	- and gradually develops categories that explain what is happening
> - data collection & analysis happen at the same time
> 	- you constantly compare pieces of data with each other
> 	- you break data into meaningful pieces and label them
> 	- you write notes about your emerging thoughts, interpretations and possible relationships between concepts
> 	- eventually, categories are linked together in an explanatory model

- A

---

# Evaluation Practices (RENAME)
- 

---

# Building LLM Judges
- 

---

# Evaluating Multi-turn Conversations
- 

---

# Evaluating RAG
- 

---

# Evaluating Tool-use & Agents
- 

---

# CI/CD for Agents
- 

---

# Interfaces for Human Review
- 

---

# Data Analysis for Traces
- 

---

# Improving LLM Agents
- 

---
