---
type: article
status: structured
quality: 1
topics: [llm-evaluation, evaluation-metrics, synthetic-data]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- [[#1 Metadata|1 Metadata]]
- [[#2 Foundations of LLM Evaluation|2 Foundations of LLM Evaluation]]
	- [[#2 Foundations of LLM Evaluation#2.1 Understanding Traces|2.1 Understanding Traces]]
	- [[#2 Foundations of LLM Evaluation#2.2 Minimum Viable Evaluation Setup|2.2 Minimum Viable Evaluation Setup]]
	- [[#2 Foundations of LLM Evaluation#2.3 Budget Allocation for Evals|2.3 Budget Allocation for Evals]]
	- [[#2 Foundations of LLM Evaluation#2.4 Long-Term Relevance of Evaluation Methods|2.4 Long-Term Relevance of Evaluation Methods]]
- [[#3 Error Analysis as the Core of Evaluation|3 Error Analysis as the Core of Evaluation]]
	- [[#3 Error Analysis as the Core of Evaluation#3.1 Purpose and Importance|3.1 Purpose and Importance]]
	- [[#3 Error Analysis as the Core of Evaluation#3.2 Step-by-Step Process|3.2 Step-by-Step Process]]
		- [[#3.2 Step-by-Step Process#3.2.1 Dataset Creation|3.2.1 Dataset Creation]]
		- [[#3.2 Step-by-Step Process#3.2.2 Open Coding|3.2.2 Open Coding]]
		- [[#3.2 Step-by-Step Process#3.2.3 Axial Coding|3.2.3 Axial Coding]]
		- [[#3.2 Step-by-Step Process#3.2.4 Iterative Refinement|3.2.4 Iterative Refinement]]
	- [[#3 Error Analysis as the Core of Evaluation#3.3 Advanced Sampling Strategies|3.3 Advanced Sampling Strategies]]
	- [[#3 Error Analysis as the Core of Evaluation#3.4 Frequency of Re-Running Error Analysis|3.4 Frequency of Re-Running Error Analysis]]
- [[#4 Data for Evaluation|4 Data for Evaluation]]
	- [[#4 Data for Evaluation#4.1 Generating Synthetic Data|4.1 Generating Synthetic Data]]
	- [[#4 Data for Evaluation#4.2 When Synthetic Data May Be Unreliable|4.2 When Synthetic Data May Be Unreliable]]
- [[#5 Evaluation Strategies|5 Evaluation Strategies]]
	- [[#5 Evaluation Strategies#5.1 Evaluating Diverse User Queries|5.1 Evaluating Diverse User Queries]]
	- [[#5 Evaluation Strategies#5.2 Efficient Production Trace Sampling|5.2 Efficient Production Trace Sampling]]
	- [[#5 Evaluation Strategies#5.3 Binary vs Likert Scale Evaluations|5.3 Binary vs Likert Scale Evaluations]]
	- [[#5 Evaluation Strategies#5.4 Eval-Driven Development – Pros and Cons|5.4 Eval-Driven Development – Pros and Cons]]
	- [[#5 Evaluation Strategies#5.5 Building Automated Evaluators|5.5 Building Automated Evaluators]]
	- [[#5 Evaluation Strategies#5.6 Avoiding Ready-to-Use Generic Metrics|5.6 Avoiding Ready-to-Use Generic Metrics]]
	- [[#5 Evaluation Strategies#5.7 Role of Similarity Metrics|5.7 Role of Similarity Metrics]]
- [[#6 People and Collaboration in Evaluation|6 People and Collaboration in Evaluation]]
	- [[#6 People and Collaboration in Evaluation#6.1 Choosing Annotators and Managing Agreement|6.1 Choosing Annotators and Managing Agreement]]
	- [[#6 People and Collaboration in Evaluation#6.2 Engineer–PM Collaboration|6.2 Engineer–PM Collaboration]]
	- [[#6 People and Collaboration in Evaluation#6.3 Outsourcing Annotation – Risks and Exceptions|6.3 Outsourcing Annotation – Risks and Exceptions]]
- [[#7 Tooling for Evaluation|7 Tooling for Evaluation]]
	- [[#7 Tooling for Evaluation#7.1 Automating Parts of the Evaluation Workflow with LLMs|7.1 Automating Parts of the Evaluation Workflow with LLMs]]
	- [[#7 Tooling for Evaluation#7.2 Manual vs Automated Prompt Writing|7.2 Manual vs Automated Prompt Writing]]
	- [[#7 Tooling for Evaluation#7.3 Custom vs Off-the-Shelf Annotation Tools|7.3 Custom vs Off-the-Shelf Annotation Tools]]
		- [[#7.3 Custom vs Off-the-Shelf Annotation Tools#7.3.1 Designing Effective Annotation Interfaces|7.3.1 Designing Effective Annotation Interfaces]]
	- [[#7 Tooling for Evaluation#7.4 Gaps in Existing Evaluation Tooling|7.4 Gaps in Existing Evaluation Tooling]]
- [[#8 Operationalizing Evaluation|8 Operationalizing Evaluation]]
	- [[#8 Operationalizing Evaluation#8.1 CI/CD vs Production Evaluation|8.1 CI/CD vs Production Evaluation]]
	- [[#8 Operationalizing Evaluation#8.2 Guardrails vs Evaluators|8.2 Guardrails vs Evaluators]]
	- [[#8 Operationalizing Evaluation#8.3 Using Evaluators as Guardrails – Decision Criteria|8.3 Using Evaluators as Guardrails – Decision Criteria]]
	- [[#8 Operationalizing Evaluation#8.4 Model Selection – When to Consider Switching|8.4 Model Selection – When to Consider Switching]]
- [[#9 Specialised Evaluation Scenarios|9 Specialised Evaluation Scenarios]]
	- [[#9 Specialised Evaluation Scenarios#9.1 Evaluating RAG Systems|9.1 Evaluating RAG Systems]]
	- [[#9 Specialised Evaluation Scenarios#9.2 Choosing Document Chunk Size|9.2 Choosing Document Chunk Size]]
	- [[#9 Specialised Evaluation Scenarios#9.3 Debugging Multi-Turn Conversation Traces|9.3 Debugging Multi-Turn Conversation Traces]]
	- [[#9 Specialised Evaluation Scenarios#9.4 Evaluating Sessions with Human Handoffs|9.4 Evaluating Sessions with Human Handoffs]]
	- [[#9 Specialised Evaluation Scenarios#9.5 Evaluating Complex Multi-Step Workflows|9.5 Evaluating Complex Multi-Step Workflows]]
	- [[#9 Specialised Evaluation Scenarios#9.6 Evaluating Agentic Workflows|9.6 Evaluating Agentic Workflows]]


# 1 Metadata
- Author: Hamel Husain, Shreya Shankar
- Category: pdf
- URL: https://readwise.io/reader/document_raw_content/348803024

---

# 2 Foundations of LLM Evaluation
## 2.1 Understanding Traces
* trace = complete record of all actions, messages, tool calls, and data retrievals from a single initial user query to the final response
	* includes all steps across agents, tools, and system components in a session
	* covers multiple user messages, assistant responses, retrieved documents, and intermediate tool interactions
## 2.2 Minimum Viable Evaluation Setup
* minimum viable evaluation setup
	* start with error analysis, not infrastructure
	* spend \~30 minutes manually reviewing 20–50 LLM outputs after significant changes
	* have one domain expert (who understands users) act as quality decision maker
	* use notebooks to review traces and analyze data
## 2.3 Budget Allocation for Evals
* budget allocation for evals
	* always perform error analysis
		* many discovered issues are straightforward bugs fixed immediately without extra eval infrastructure
	* automated evaluators require cost–benefit analysis
		* simple assertion/regex check → minimal cost, often worth it
		* aligning LLM-as-judge → only if failure mode warrants investment
	* expect **60–80% of development time** on error analysis + evaluation
		* majority of effort spent understanding failures, not building automated checks
	* passing 100% of evals likely means evaluations are too easy
		* \~70% pass rate can indicate meaningful stress testing
		* focus on catching real issues, not inflating metrics
## 2.4 Long-Term Relevance of Evaluation Methods
* long-term relevance of today’s evaluation methods
	* systematic error analysis, domain-specific testing, and monitoring will remain important
	* prompt engineering tricks may become obsolete, but understanding failure modes will still be essential
# 3 Error Analysis as the Core of Evaluation
## 3.1 Purpose and Importance
* error analysis = core activity in LLM evaluation
	* purpose: identifies unique failure modes in application/data and informs what evals to create
	* never skip error analysis
## 3.2 Step-by-Step Process
* process:
	1. dataset creation = gather representative traces of user–LLM interactions (synthetic data can be used initially)
	2. open coding = domain expert annotator reviews traces, writes open-ended notes about issues
		- adapted from qualitative research “journaling”
		- often focus on first failure in a trace to avoid noise from downstream errors
	3. axial coding = categorize notes into failure taxonomy and count failures per category
		- can use LLM assistance here
	4. iterative refinement = continue reviewing until reaching theoretical saturation (no new failure modes found)
		- aim to review at least 100 traces
### 3.2.1 Dataset Creation
* dataset creation = gather representative traces of user–LLM interactions (synthetic data can be used initially)
### 3.2.2 Open Coding
* open coding = domain expert annotator reviews traces, writes open-ended notes about issues
	* adapted from qualitative research “journaling”
	* often focus on first failure in a trace to avoid noise from downstream errors
### 3.2.3 Axial Coding
* axial coding = categorize notes into failure taxonomy and count failures per category
	* can use LLM assistance here
### 3.2.4 Iterative Refinement
* iterative refinement = continue reviewing until reaching theoretical saturation (no new failure modes found)
	* aim to review at least 100 traces
## 3.3 Advanced Sampling Strategies
* revisit regularly; use advanced sampling (clustering, feedback sorting, high-probability failure patterns)
* develop “nose” for where failures hide
* surfacing problematic traces beyond user feedback
	* random sampling = review random traces; if low issue count, escalate to stress testing with challenging queries
	* use evals for screening = find problematic traces via automated evals, then start error analysis
	* efficient sampling strategies = outlier detection, metric-based sorting, stratified sampling to locate interesting traces
		* generic metrics can still signal traces worth review even without direct quality measure
## 3.4 Frequency of Re-Running Error Analysis
* frequency of re-running error analysis
	* run after major changes (features, prompts, models, major bug fixes)
	* review at least 100+ fresh traces per major cycle
	* between major cycles: 10–20 traces weekly focusing on outliers (long conversations, multiple retries, flagged sessions)
	* mature systems: monthly review unless usage patterns change
	* always analyze after incidents, spikes in complaints, or metric drift
	* scaling usage → expect new edge cases
# 4 Data for Evaluation
## 4.1 Generating Synthetic Data
* generating synthetic data
	* avoid unstructured “give me test queries” prompts (leads to generic repetition)
	* structured approach using **dimensions** works better
		* dimensions = categories capturing variation in user behavior
			* recipe app example: dietary restriction, cuisine type, query complexity
			* customer support bot example: issue type, customer mood, prior context
	* start with **failure hypotheses** based on application use or targeted testing
	* create **tuples manually first** (e.g., 20 combinations of one value from each dimension)
		* e.g., (Vegan, Italian, Multi-step)
	* scale with **two-step generation**:
		1. generate structured tuples (e.g., (Gluten-free, Asian, Simple))
		2. convert tuples to natural language queries
	* generation methods:
		* cross product + filter → guarantees coverage, including edge cases; best when most combos valid
		* direct LLM generation → more realistic phrasing but misses rare scenarios; better when many combos invalid
	* fix obvious issues before generating synthetic queries
	* run synthetic queries through system to capture traces
		* sample 100 traces for error analysis to find failure patterns without excessive volume
## 4.2 When Synthetic Data May Be Unreliable
* when synthetic data may be unreliable
	* complex domain-specific content = LLMs often fail to capture structure, nuance, and quirks of specialized documents without real examples
	* low-resource languages/dialects = generated samples often unrealistic; evals won’t reflect real performance
	* no validation possible = without ground truth or domain knowledge, realism can’t be confirmed
	* high-stakes domains (medicine, law, emergency response) = synthetic data lacks subtlety and edge cases, making errors risky
	* underrepresented user groups = risk of misrepresentation and bias reinforcement
# 5 Evaluation Strategies
## 5.1 Evaluating Diverse User Queries
* evaluating diverse user queries
	* rely on error analysis to reveal real failure patterns
	* avoid creating huge evaluation matrices in advance
	* group discovered query categories by shared failure patterns
	* let actual system behavior guide evaluation priorities
## 5.2 Efficient Production Trace Sampling
* efficient production trace sampling
	* outlier detection = sort by metrics like length, latency, tool calls; review extremes
	* user feedback signals = prioritize negative feedback, support tickets, escalations
	* metric-based sorting = use generic metrics to explore both high/low scores for clues
	* stratified sampling = sample across user type, feature, query category
	* embedding clustering = cluster queries, sample proportionally, oversample small clusters for edge cases
## 5.3 Binary vs Likert Scale Evaluations
* binary (pass/fail) vs Likert scale evaluations
	* binary evals = clearer, more consistent labeling; faster to annotate; avoids subjective middle scores
	* Likert scales = subjective, inconsistent, require larger sample sizes, often default to middle values
* for gradual improvement tracking → measure subcomponents as multiple binary checks
	* e.g., “4 out of 5 expected facts included” instead of 1–5 factual accuracy rating
## 5.4 Eval-Driven Development – Pros and Cons
* eval-driven development - generally not recommended
	* start with error analysis → write evaluators for observed failures, not imagined ones
	* exception: strict known constraints (e.g., “never mention competitors”) may justify pre-built evaluator
	* always apply cost–benefit analysis before building evals
## 5.5 Building Automated Evaluators
* building automated evaluators
	* focus on persistent failures that remain after prompt fixes
	* cost hierarchy:
		* cheap: simple assertions, reference-based checks
		* expensive: LLM-as-Judge (needs 100+ labeled examples, weekly upkeep, coordination)
	* reserve costly evaluators for persistent generalization failures, not trivial fixable issues
* using the same model for task + evaluation
	* fine for LLM-as-Judge since judging is a different task
	* focus on high TPR/TNR on held-out labeled test set
	* start with most capable models to match human judgment well
## 5.6 Avoiding Ready-to-Use Generic Metrics
* using ready-to-use evaluation metrics
	* avoid generic prefab metrics (helpfulness, coherence, quality) → may waste time, create false confidence
	* instead:
		* perform error analysis
		* define binary failure modes from real problems
		* create custom evaluators and validate against human judgment
## 5.7 Role of Similarity Metrics
* similarity metrics (BERTScore, ROUGE, etc.)
	* generally not useful for most LLM application evaluation
	* exceptions:
		* search/recommendation optimization
		* retrieval debugging (cosine similarity for semantic closeness, diversity analysis)
# 6 People and Collaboration in Evaluation
## 6.1 Choosing Annotators and Managing Agreement
* number of annotators
	* single expert = eliminates conflicts, avoids paralysis from too many opinions
	* multiple annotators needed in multi-domain/multicultural contexts
		* measure agreement (e.g., Cohen’s Kappa) and align interpretations
* in many cases, one expert is still sufficient
## 6.2 Engineer–PM Collaboration
* engineer–PM collaboration in error analysis
	* engineers catch technical issues
	* PMs catch product expectation failures
	* shared context at start ensures broader coverage
## 6.3 Outsourcing Annotation – Risks and Exceptions
* outsourcing annotation & labeling
	* generally a bad idea for error analysis
	* risks: superficial labeling, loss of tacit domain knowledge, misalignment
	* recommended: build internal capability
		* collaborative multi-annotator workflow with rubric alignment and IAA measurement
		* smart sampling = analyze small representative set deeply
		* “think-aloud” protocol = experts verbalize review process for richer insight
		* lightweight custom tools = increase annotation throughput
	* outsourcing exceptions:
		* purely mechanical tasks (e.g., phone number extraction)
		* tasks without product context (e.g., translation)
		* hiring external SMEs as internal domain experts (e.g., medical students for RAG evals)
# 7 Tooling for Evaluation
## 7.1 Automating Parts of the Evaluation Workflow with LLMs
* useful for:
	* first-pass axial coding after 30–50 manually open-coded traces
	* mapping annotations to defined failure modes
	* suggesting prompt improvements for recurring issues
	* analyzing annotation data for patterns (e.g., spikes in lag during peak hours)
* not suitable for:
	* initial open coding (must be done by human to discover new failures)
	* validating failure taxonomies (LLM groupings need expert review)
	* ground truth labeling for evaluator validation (must be hand-checked)
	* root cause analysis (requires workflow/context awareness)
## 7.2 Manual vs Automated Prompt Writing
* manual vs automated prompt writing
	* manual prompts force clarity in requirements and assumptions
	* evaluation is iterative and human-driven; automated prompt optimizers risk missing nuanced errors early in development
## 7.3 Custom vs Off-the-Shelf Annotation Tools
* custom vs off-the-shelf annotation tools
	* build custom tools for maximum iteration speed (\~10× faster)
	* advantages:
		* integrate all system context in one view
		* render data in product-specific ways
		* tailor filters, sorting, and workflow
### 7.3.1 Designing Effective Annotation Interfaces
* good custom interfaces:
	- render traces intelligently
	- show progress + keyboard navigation
	- enable clustering, filtering, search
	- prioritize suspected-problematic traces
	- keep UI minimal to reduce maintenance cost
## 7.4 Gaps in Existing Evaluation Tooling
* gaps in existing eval tooling
	* automated error clustering/pattern discovery
	* AI assistance throughout the workflow
	* custom evaluators over generic metrics
	* APIs for custom annotation app integration
# 8 Operationalizing Evaluation
## 8.1 CI/CD vs Production Evaluation
* CI evaluation:
	* small, curated datasets (100+ examples)
	* covers core features, regressions, known edge cases
	* favor deterministic checks for speed
* production evaluation:
	* sample live traces, run evaluators asynchronously
	* often use reference-free evaluators like LLM-as-judge
	* track confidence intervals; investigate if lower bound crosses threshold
* feedback loop: add new production failure examples to CI to prevent regressions
## 8.2 Guardrails vs Evaluators
* guardrails = synchronous, deterministic checks in request path (fast, explainable, prevent high-impact failures like PII leaks)
* evaluators = asynchronous quality assessments (factual accuracy, completeness) that don’t block output
## 8.3 Using Evaluators as Guardrails – Decision Criteria
* evaluator as guardrail only if:
	1. latency/cost fits request path
	2. false positive/negative trade-off is acceptable
## 8.4 Model Selection – When to Consider Switching
* model selection time allocation
	* don’t default to model switching
	* run error analysis to confirm model is the root cause before changing
# 9 Specialised Evaluation Scenarios
## 9.1 Evaluating RAG Systems
* evaluating RAG systems
	* retrieval = IR metrics like Recall@k, Precision@k, MRR
	* generation = check context relevance (C|Q), faithfulness (A|C), answer relevance (A|Q)
	* perform error analysis to find domain-specific failure modes and create targeted evaluators
	* validate LLM-as-judge accuracy against human labels before use
## 9.2 Choosing Document Chunk Size
* choosing document chunk size
	* fixed-output tasks → larger chunks
	* expansive-output tasks → smaller chunks
	* chunk size affects attention distribution (middle often neglected in large chunks)
	* treat chunk size as a tunable hyperparameter
## 9.3 Debugging Multi-Turn Conversation Traces
* debugging multi-turn conversation traces
	* log all messages with source, trace ID, sequence position
	* annotate first failure only at start
	* reproduce failures with simplest possible test case
	* test case generation:
		* synthetic LLM conversations
		* N-1 testing using real conversation prefixes
## 9.4 Evaluating Sessions with Human Handoffs
* evaluating sessions with human handoffs
	* log until final resolution, including handoff details and outcomes
	* evaluate necessity, context sufficiency, and quality of handoffs
	* track handoff rate and quality; aim to reduce unnecessary handoffs
## 9.5 Evaluating Complex Multi-Step Workflows
* evaluating complex multi-step workflows
	* log all usage, approvals, database writes
	* outcome metrics = final result quality
	* process metrics = step count, time, resource use
	* segment error analysis by workflow stage
	* use transition failure matrices to locate hotspots
## 9.6 Evaluating Agentic Workflows
* evaluating agentic workflows
	* phase 1: end-to-end task success (black box, upstream failure noted)
	* phase 2: step-level diagnostics (tool choice, parameter extraction, error handling, context retention, efficiency, goal checkpoints)
	* use transition matrices for failure pattern analysis
	* create test cases for agent failures using minimal reproduction steps

![[Screenshot 2025-08-10 at 12.36.04 pm.png| center | 500]]




