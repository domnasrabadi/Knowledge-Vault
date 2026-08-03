---
type: book
status: structured
quality:
topics: [mlops]
source: ""
created: 2025-07-20
published:
author: ""
flashcards: none
updated: 2025-08-24
---


![[Screenshot 2025-07-20 at 10.43.49 am.png| center | 500]]
- [[#1 Preface|1 Preface]]
- [[#2 Introduction to Large Language Models|2 Introduction to Large Language Models]]
	- [[#2 Introduction to Large Language Models#2.1 Evolution of LLMs|2.1 Evolution of LLMs]]
	- [[#2 Introduction to Large Language Models#2.2 LLMs in the Enterprise|2.2 LLMs in the Enterprise]]
- [[#3 Intro to LLMOps|3 Intro to LLMOps]]
	- [[#3 Intro to LLMOps#3.1 What is MLOps/LLMOps/DevOps etc|3.1 What is MLOps/LLMOps/DevOps etc]]
	- [[#3 Intro to LLMOps#3.2 LLM Ops vs MLOps|3.2 LLM Ops vs MLOps]]
	- [[#3 Intro to LLMOps#3.3 LLMOps intro|3.3 LLMOps intro]]
- [[#4 LLM-Based Applications|4 LLM-Based Applications]]
	- [[#4 LLM-Based Applications#4.1 Agents|4.1 Agents]]
	- [[#4 LLM-Based Applications#4.2 LLM Applications in the Enterprise|4.2 LLM Applications in the Enterprise]]
- [[#5 Data Engineering for LLMs|5 Data Engineering for LLMs]]
	- [[#5 Data Engineering for LLMs#5.1 Importance of Data for LLMs|5.1 Importance of Data for LLMs]]
	- [[#5 Data Engineering for LLMs#5.2 Data preprocessing for LLMs|5.2 Data preprocessing for LLMs]]
	- [[#5 Data Engineering for LLMs#5.3 Other data manipulation + preparation techniques|5.3 Other data manipulation + preparation techniques]]
- [[#6 Domain Adaptation for LLM Applications|6 Domain Adaptation for LLM Applications]]
	- [[#6 Domain Adaptation for LLM Applications#6.1 Prompt Eng, RAG + Fine-tuning|6.1 Prompt Eng, RAG + Fine-tuning]]
	- [[#6 Domain Adaptation for LLM Applications#6.2 Model Ensembling|6.2 Model Ensembling]]
	- [[#6 Domain Adaptation for LLM Applications#6.3 Finetuning vs Prompt Eng|6.3 Finetuning vs Prompt Eng]]
	- [[#6 Domain Adaptation for LLM Applications#6.4 Model Optimisation|6.4 Model Optimisation]]
	- [[#6 Domain Adaptation for LLM Applications#6.5 Lessons for Effective LLM Development|6.5 Lessons for Effective LLM Development]]
- [[#7 API-First LLM Deployment|7 API-First LLM Deployment]]
	- [[#7 API-First LLM Deployment#7.1 API strategies|7.1 API strategies]]
	- [[#7 API-First LLM Deployment#7.2 Optimising RAG pipelines|7.2 Optimising RAG pipelines]]
- [[#8 LLM Evaluations|8 LLM Evaluations]]
	- [[#8 LLM Evaluations#8.1 Why Evaluation is a Hard Problem|8.1 Why Evaluation is a Hard Problem]]
	- [[#8 LLM Evaluations#8.2 Evaluating Performance|8.2 Evaluating Performance]]
	- [[#8 LLM Evaluations#8.3 General Eval Considerations|8.3 General Eval Considerations]]
	- [[#8 LLM Evaluations#8.4 Traditional Metrics aren't Enough|8.4 Traditional Metrics aren't Enough]]
	- [[#8 LLM Evaluations#8.5 Observability Pipeline|8.5 Observability Pipeline]]
- [[#9 Governance: Monitoring, Privacy and Security|9 Governance: Monitoring, Privacy and Security]]
	- [[#9 Governance: Monitoring, Privacy and Security#9.1 LLM Security Threats|9.1 LLM Security Threats]]
	- [[#9 Governance: Monitoring, Privacy and Security#9.2 Model/LLM Audit/Validation|9.2 Model/LLM Audit/Validation]]
- [[#10 Scaling: Hardware, Infra and Resource Management|10 Scaling: Hardware, Infra and Resource Management]]
- [[#11 The Future of LLMs and LLMOps|11 The Future of LLMs and LLMOps]]



---

# 1 Preface
- pace of change = by early 2025, new models, techniques, and best practices emerge every few days
- LLM Ops = orchestration of people, processes, and technology to keep models secure, robust, reliable in production
    - differs from traditional "deployment-only" view of operationalizing
- software 2.0 analogy
    - software development engineers = build the system
    - reliability engineers = maintain and operate it
    - implication = LLM teams need similar role separation for effective operations

---

# 2 Introduction to Large Language Models
## 2.1 Evolution of LLMs
- LLMs came about via series of incremental innovations that address prior limitations
	- foundation model = advanced ml architecture pretrained on large data to serve as base for task-specific fine-tuning
		- encodes statistical relationships + linguistic structures for robust starting point
	- vanishing gradient problem = gradients shrink in long recurrent sequences so learning stalls
	- transformer = architecture using self-attention + parallel processing to capture long-range dependencies without vanishing gradients
		- self-attention = each token weighs every other token in sequence regardless of position
- model classes
	- discriminative model = estimates $P(y\mid x)$ to draw class boundaries e.g. BERT (2018)
	- generative model = models joint $P(x,y)$ and can produce new data similar to training corpus e.g. GPT models
- transformer variants
	- **encoder-only** model = processes input into embedding capturing syntax + context for comprehension tasks
	- **decoder-only** model = generates coherent text from prompt using language-model objective
	- **encoder-decoder** model = encoder builds embedding then decoder produces output sequence for complex input→output mappings
- attention complexity challenge
	- quadratic complexity = self-attention cost grows with square of sequence length
	- state space architecture = replaces attention with state-space representations for linear complexity but higher error rate
	- small language model (SLM) = compact model with ≤ millions of parameters tuned for narrow tasks
		- high efficiency trade-off against reasoning + memory capability
## 2.2 LLMs in the Enterprise
- model selection considerations
    - alignment with objectives = chosen model must suit business goals
    - performance + efficiency = latency, throughput, resource use
    - training data + bias = assess coverage and fairness of pretraining corpus
    - customization + adaptability = ease of fine-tuning or prompt adaptation
    - integration + support = tooling, documentation, vendor stability
    - closed-source LLM = optimized for large-scale deployment with performance guarantees

![[Screenshot 2025-07-20 at 10.43.03 am.png| center | 500]]

- enterprise LLM use cases
    - conversational retrieval = dynamic dialogue replacing keyword search
    - zero-shot / few-shot translation = coverage of low-resource languages
    - text-to-speech generation = natural human-like audio
    - personalization systems = deeper user preference modeling
- autonomous AI agents = task-oriented systems that use LLMs for real-time pattern recognition + decision making
    - integration challenges
        - workflow alignment = ensure agents complement human teams
        - management + monitoring = establish oversight + guidelines
- the challenges of building with LLMs
    - size + complexity
    - training scale + duration
    - prompt engineering = compounded when multiple interdependent prompts in orchestration framework
    - inference latency + throughput
    - resource scaling + orchestration
    - integrations + toolkits
    - broad applicability
    - privacy + security

---

# 3 Intro to LLMOps
## 3.1 What is MLOps/LLMOps/DevOps etc
- productionizing = deploying a model **and** continuously monitoring, evaluating, and optimising its behaviour in production
    - encompasses data pipelines, dynamic prompt storage, user-interaction monitoring, and misinformation prevention
- operational framework = structured set of tools + practices that automate complex ML workflows to ensure consistency + quality
    - DecOps = software development + operations for conventional code
    - MLOps = devops variant for non-generative ml models
    - LLMOps = ops discipline for generative language models
        - handles greater model scale, data complexity, evaluation difficulty, user-facing latency, and unpredictability
## 3.2 LLM Ops vs MLOps

| Dimension                | MLOps                                                           | LLMOps                                                                     |
| ------------------------ | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Data preprocessing       | Fix missing values & outliers                                   | Deduplication; toxicity filtering; diversity management; quantity control  |
| Model size & training    | Models ≲ 200M parameters → single-node experiments              | Models ≳ 100B parameters → weeks of distributed GPU/TPU training           |
| Domain adaptation        | Full fine-tuning affordable                                     | Prompt engineering; RAG; knowledge graphs; parameter-efficient fine-tuning |
| Evaluation difficulty    | Discriminative, bounded probability space, well-defined metrics | Generative, unbounded output, hard-to-score quality                        |
| Robustness in production | Behaviour static post-deploy                                    | Behaviour shifts with user interaction → constant alignment monitoring     |

## 3.3 LLMOps intro
- four goals of LLMOps
    - <span style="color:rgb(0, 176, 80)">security</span> = protect data, guard against adversarial attacks, comply with GDPR/HIPAA
    - <span style="color:rgb(0, 176, 80)">scalability</span> = meet latency + throughput targets while optimising cost
    - <span style="color:rgb(0, 176, 80)">robustness</span> = maintain performance despite data/model drift or third-party updates
    - <span style="color:rgb(0, 176, 80)">reliability</span> = minimise downtime via inference monitoring, error handling, redundancy
- metrics framework
    - SLO = internal service-level objective defining target quality (e.g. ≤ 200 ms p95 latency)
    - SLA = contract with customers specifying required service level + remedies
    - KPI = business indicator tracking strategic success (e.g. CSAT, cost per request)
    - using SLO-SLA-KPI trio aligns stakeholders and automates expectation management

![[Screenshot 2025-07-20 at 10.45.57 am.png| center | 500]]


- LLMOps engineering skill set
    - convert models across PyTorch/JAX
    - measure accuracy, precision, recall, PR-AUC
    - detect data + concept drift
    - benchmark computational graphs on GPU/CPU/neural engines
    - deploy at scale on AWS / GCP / Azure
        - latency optimisation = kernel fusion, quantisation, dynamic batching
    - build data + infra pipelines with Terraform, vector dbs, ETL
    - design red-teaming interfaces + guidelines
    - containerisation with Docker, orchestration with Kubernetes
    - collaborate across LLM engineers, data scientists, ml/nlp engineers
- LLMOps maturity model
    - level 0 = no LLMOps
    - level 1 = MLOps but no dedicated LLMOps
    - level 2 = full LLMOps
        - documentation = up-to-date business goals, kpis, team roles, cost comparisons, api specs, architecture diagrams
        - performance + evaluation = guardrails for knowledge limits, automated i/o storage, regular A/B tests, full logging + health monitoring, toxicity/bias pipelines, compliance processes, advanced anonymisation, scheduled security audits

---

# 4 LLM-Based Applications
- user-facing application = interface provided by model-building companies that wraps user prompts, appends internal instructions, tracks conversation context, rewrites input for quality, and enforces safety + politeness
    - simplest form is a chat-like web UI that forwards prompts to the model
    - extra layers mean answers differ between API access and the default web app
- model-name ≈ app-name confusion = when the model and the user-facing application share (almost) the same name users conflate them
- current LLM infrastructure wave = tools that make LLMs faster, more programmable, more modular
	- single-prompt ceiling = beyond trivial tasks we need memory, planning, tools, and ultimately agents
## 4.1 Agents
- agent = loop that **observe → decide → act** repeatedly
    - typical acts: read instruction, inspect state, fetch resource, call tool, decompose task
    - agentic system = model runs code, manages steps, adapts on the fly unlocking complex workflows
- major agent types
    - <mark style="background: #FFB8EBA6;">single-step agent</mark> = one-shot wrapped prompt without memory or iteration
        - suited to bounded tasks
    - <mark style="background: #FFB8EBA6;">chain-of-thought agent</mark> = writes reasoning steps then the answer in the same prompt
        - step-wise logic improves multi-hop problem solving
    - <mark style="background: #FFB8EBA6;">plan-and-act agent</mark> = first drafts a high-level plan then executes it sequentially
        - planning + acting may share one model or be split across agents
        - explicit progress tracking enables retries + self-correction
    - <mark style="background: #FFB8EBA6;">reflective agent</mark> = self-improving agent that scores its own output or consults another model to learn from past actions
    - <mark style="background: #FFB8EBA6;">recursive decomposition agent</mark> = recursively splits a goal into subtasks until each is solvable
        - parent instance delegates subtasks to child agents or specialised workers
    - <mark style="background: #FFB8EBA6;">multi-agent collaborators</mark> = several agents with distinct roles share messages or task queues to parallelise work
        - effective when tasks are parallelisable or demand domain expertise
- scaling challenges ⛔️
    - ⛔️ coordination overhead rises with more agents
    - ⛔️ must set roles, communication boundaries, fallback plans
    - ⛔️ require logging, observability, memory management, and failure handling when an agent crashes or errors
- control flow = architectural layer deciding which decisions run inside the model versus in external orchestration logic
    - agentic design hinges on clear control flow choices
- shared protocols (MCP, A2A) = common messaging standards that enable inter-agent coordination

![[Screenshot 2025-07-21 at 10.08.11 am.png| center | 500]]

- <mark style="background: #FFB8EBA6;">model context protocol (MCP)</mark> = contract that cleanly separates **host**, **client**, and **server**, giving each a role and a shared language for capabilities
    - **origin** = response to brittle, hand-crafted, monolithic integrations of early LLM apps
    - **host** = ai application (desktop assistant, chatbot) that owns the session context
    - **server** = external tool or system exposing capabilities
    - **client** = messenger that mediates host ↔ server traffic
    - benefits
        - models discover tools, data, and prompts at runtime instead of guessing
        - enables real-time queries, safe tool invocation, agentic reasoning across systems
- MCP components
    - **tools** = model-controlled functions with clear input/output schema registered at runtime
        - used for actions that cause side effects or require computation (retrieve doc, call api, trigger workflow)
    - **resources** = application-controlled read-only data endpoints the model can look up for context enrichment
        - examples: file lists, user profiles, metadata
    - **prompts** = user-controlled templates that guide model behaviour or encode common workflows
- MCP lifecycle
    - *handshake phase* = client and server exchange version + capability metadata
    - *discovery phase* = client enumerates available tools, resources, prompts
    - *interaction phase* = model emits structured function calls (e.g., JSON) when it decides to act
        - asynchronous + incremental; model queries only what it needs as conversation evolves
- agentic implication = instead of stuffing the model with all knowledge, MCP lets it **seek → ask → call** the right capability at the right moment
- <mark style="background: #FFB8EBA6;">agent-to-agent protocol (A2A)</mark> = open standard for multi-agent interoperability that extends MCP to groups
    - each agent publishes an **agent card** describing identity + capabilities
    - one agent need not understand another’s internals—only its advertised interface
    - A2A interaction steps
        - discovery = calling agent fetches target agent card
        - validation = verifies identity + credentials
        - capability matching = inspects listed functions to decide delegation
        - task delegation = sends structured request; callee may accept, reject, or propose alternative
        - execution = callee performs task, possibly invoking sub-agents or tools
        - response = returns result, logs, metrics, follow-up options
## 4.2 LLM Applications in the Enterprise
- LLMops core question = **does the application perform well at a reasonable cost?** ?
    - once answered **yes**, teams iterate on optimisations for max performance vs min cost
- monitoring application performance
    - MLOps vs LLMOps metrics are largely identical; most are domain dependent
    - metric computation tech-agnostic—same formulas whether results come from ML, LLM, or manual processes
    - LLMs introduce added challenges
        - lower determinism → higher variance in outputs
        - greater susceptibility to _drift_ compared with traditional ml models
- measuring consumer LLM application performance = adapting classic ml evaluation to nondeterministic LLM behaviour
    - spam detection example = binary classification task requiring accuracy, precision, recall
        - accuracy = $\frac{tp+tn}{tp+fp+tn+fn}$ proportion of all correctly classified emails
        - precision = $\frac{tp}{tp+fp}$ fraction of predicted spam that is truly spam
        - recall = $\frac{tp}{tp+fn}$ fraction of actual spam correctly flagged
        - precision–recall curve = plots precision (y) vs recall (x) at varied thresholds to visualise trade-off
            - high-quality model curve approaches top-right
            - assumes stable probability scores → problematic for LLMs
        - ROC curve + AUC = standard ml metrics relying on deterministic scoring become noisy with LLMs
    - champion / challenger test = compare production model (champion) vs new version (challenger)
        - variability solution = run multiple passes per sample to build score distributions
            - record mean, std dev, confidence intervals
            - significance testing = two-sample $t$-test below
            - tiny $p$-value → challenger truly better ?
    - ranking + recommendation metrics
        - MAP = mean average precision rewards relevant items ranked higher
        - NDCG = normalized discounted cumulative gain discounts lower-ranked relevance
        - Hit Rate / Top-$k$ Accuracy = proportion of queries with ≥1 relevant item in top k
        - Coverage = catalog proportion surfaced, indicates diversity

$$
\begin{gather}
\textbf{Two-Sample t-Test w/ unequal variances} \\ \ \\
\Large t=\frac{\bar{x}_c-\bar{x}_n}{\sqrt{\frac{s_c^2}{n_c}+\frac{s_n^2}{n_n}}}
\end{gather}
$$

- controllable LLM generation parameters
    - <span style="color:rgb(255, 0, 247)">temperature</span> = controls randomness by flattening or sharpening token probability distribution
    - <span style="color:rgb(255, 0, 247)">top-k sampling</span> = choose next token only from k most likely
    - <span style="color:rgb(255, 0, 247)">top-p (nucleus) sampling</span> = choose from smallest token set whose cumulative prob ≥ p
    - <span style="color:rgb(255, 0, 247)">frequency penalty</span> = down-weights tokens repeated many times
    - <span style="color:rgb(255, 0, 247)">presence penalty</span> = down-weights tokens that have appeared at least once
- out-of-spec handling
    - unknown class = extra label for answers outside expected schema
        - metric = out-of-spec error percentage, target kept low
- precision comparison case study
    - prompt A vs prompt B both achieve recall = 100 % but precision differs
        - $p$-value ≪ 0.05 → prompt A significantly better in precision
- complexity beyond single prompts
    - orchestrated LLMs systems = memory + tools + feedback + goals ⇒ complex control flow
    - agentic failure modes
        - brittle memory retrieval → latency + accuracy bottlenecks
        - lack of unit-test equivalents for agents
        - messy plans or unsynced protocols cause silent breakdowns
    - observability necessity = layered structured logging + metrics across agents and sessions

![[Screenshot 2025-07-21 at 10.09.09 am.png| center | 600]]

---

# 5 Data Engineering for LLMs
- definitions
	- <span style="color:rgb(255, 0, 247)">vector database</span> = storage + indexing system for high-dimensional embeddings using approximate nearest-neighbor search
	    - serves queries by distance in vector space, not exact keyword match
	- <span style="color:rgb(255, 0, 247)">bag of words (BoW)</span> = sparse matrix representation where each cell counts term frequency
	- <span style="color:rgb(255, 0, 247)">TF-IDF</span> = BoW weighted by inverse document frequency to down-weight common words
	- <span style="color:rgb(255, 0, 247)">embedding</span> = algorithm that maps text, code, images, audio, or chat into dense numeric vectors encoding semantic similarity
	    - breakthrough enabling large language models (LLMs)
- data engineering for LLMs
    - shift from batch ETL of structured tables to continuous pipelines for heterogeneous unstructured content
        - stages: tokenize → chunk → embed → version → filter pii/toxicity/licensing → index in vector store
        - run re-embedding loops so retrieval-augmented generation (RAG) stays current
        - log prompt–response pairs for evaluation and reinforcement
    - data quality now judged by grounding, factuality, bias, and toxicity rather than schema conformance
## 5.1 Importance of Data for LLMs
- conventional ML feature engineering = manual crafting of numeric predictors
    - embeddings reduce need for handcrafted features by encoding semantics automatically
- scaling laws
    - <mark style="background: #FFB8EBA6;">Kaplan's law</mark> = model loss decreases predictably when model parameters PP and training tokens TT scale together 
	    - if compute budget fixed ⇒ parameters must grow faster than data to maximise performance

$$
loss∝P−0.076 T−0.095\text{loss} \propto P^{-0.076}\,T^{-0.095} (approx)
$$

- <mark style="background: #FFB8EBA6;">Chinchilla scaling law</mark> = for fixed compute, scale data more and parameters less; many models (e.g., GPT-3) are undertrained
    - multi-epoch degradation = repeated passes over same data yield diminishing or negative returns as model size grows
- dataset curation techniques
    - <mark style="background: #ADCCFFA6;">deduplication</mark> = remove duplicates to curb memorisation + train–test overlap
    - <mark style="background: #ADCCFFA6;">toxicity filtering</mark> = exclude rude or hateful content via heuristics, n-gram filters, or classifiers
        - risk: over-filtering harms representation for marginalized groups
    - <mark style="background: #ADCCFFA6;">quality filtering</mark> = drop low-quality or off-domain text
    - <mark style="background: #ADCCFFA6;">global deduplication</mark> = remove duplicates across domains to balance corpus composition
- data diversity = include many linguistic styles, cultures, domains to reduce bias and improve generalisation
- temporal freshness = newer data mitigates evaluation mismatch caused by shifting world knowledge
- interdependent factors
    - domain mix, quantity, quality, and deduplication interact non-linearly
        - optimising one dimension can unexpectedly degrade another
        - requires empirical tuning and ongoing monitoring

![[Screenshot 2025-07-21 at 10.16.48 am.png| center | 1000]]

## 5.2 Data preprocessing for LLMs
- general data-preprocessing pipeline = 10-step workflow for preparing text corpora for LLM training and fine-tuning
    - core metrics = small smoke-test prompt set whose answers you know
        - examples = “2 + 2 ?”, “capital of France ?”, “yes/no: picture of a bird ?”
        - purpose = quick detection of pipeline regressions
        - also run periodic benchmark suites (e.g., MMLU) + safety / bias checks
    - evaluation rule = expect minor metric noise but ensure long-term upward trend
- 10 preprocessing steps
    1. <span style="color:rgb(255, 136, 0)">step 1 catalog data</span>
        - define data types, language, domain, quality standard
        - register source metadata in a lookup database
    2. <span style="color:rgb(255, 136, 0)">step 2 privacy and legal compliance</span>
    3. <span style="color:rgb(255, 136, 0)">step 3 filter data</span>
        - cleaning rules
            - remove incomplete sentences, pii, harmful content, abnormal symbols
            - strip technical clutter (html, css, js ids) + placeholders in {curly braces}
            - drop overly short sentences, redundant ui text, disallowed words
    4. <span style="color:rgb(255, 136, 0)">step 4 deduplication</span> = eliminate repeated or near-duplicate content
        - choose time frame + scope + frequency of dedupe
        - techniques
            - tf-idf similarity → remove high-overlap pair
            - consecutive duplicate sentence removal
            - url match removal
            - minhashlsh with n-grams threshold≈0.8
    5. <span style="color:rgb(255, 136, 0)">step 5 collect data</span>
        - crawl web, call apis, parse html/pdf while honouring terms of service
        - attach metadata from previous steps
    6. <span style="color:rgb(255, 136, 0)">step 6 detect encoding</span> = ensure correct text byte representation
    7. <span style="color:rgb(255, 136, 0)">step 7 detect languages</span> = run language id (e.g., lingua-py) and split subsets
    8. <span style="color:rgb(255, 136, 0)">step 8 chunking</span> = break text into model-sized units
        - strategies
            - fixed size
            - sentence-based
            - paragraph-based
            - use llm to tag chunk sentiment + topic or apply agentic chunking for faq-style slices
    9. <span style="color:rgb(255, 136, 0)">step 9 back up data</span>
    10. <span style="color:rgb(255, 136, 0)">step 10 maintenance + updates</span> = continuous ingestion, source refresh, strategy tweaks
## 5.3 Other data manipulation + preparation techniques 
- vectorisation = convert text chunk into high-dimensional embedding vector capturing semantics
    - simplest start = numpy implementation per karpathy advice
    - indexing = insert vectors + metadata into vector database enabling nearest-neighbor search
        - metadata filters narrow search space before similarity lookup
- fine-tuning dataset types
    - general instruction fine-tuning datasets
    - domain-specific instruction fine-tuning datasets
- automatic instruction dataset generation workflow
    1. step 1 preprocessing + vectorization of corpus
    2. step 2 retrieval mechanism = index + search api
    3. step 3 question generation = create synthetic qa prompts
    4. step 4 best-answer selection
        - query index with each question → retrieve relevant chunks
        - send question + chunks to existing llm → choose best chunk → craft complete answer
        - loop until desired sample count reached
    - hygiene checks
        - deduplicate near-identical qa pairs via cosine similarity
        - filter hallucinated answers lacking grounding in retrieved text
        - manual spot-check calibration
    - enrichment = ask llm follow-up questions or output constrained formats (e.g., json)

---

# 6 Domain Adaptation for LLM Applications
- model adaptation = refining a pretrained model for better performance on specific tasks or in unique contexts
	- 3 primary adaptation techniques:
	    1. <mark style="background: #BBFABBA6;">prompt engineering</mark>
	    2. <mark style="background: #BBFABBA6;">fine-tuning</mark>
	    3. <mark style="background: #BBFABBA6;">RAG</mark> (retrieval-augmented generation)
	- benefits of model adaptation
		- enhances LLM performance in underrepresented domains (e.g. medical or legal)
		- reduces need for large domain-specific labeled datasets
		- broadens LLM accessibility for non-experts in specific domains
		- domain-specific vocabulary can be incorporated via updated tokenizers and embedding layers

![[Screenshot 2025-07-30 at 7.56.37 am.png| center | 500]]

## 6.1 Prompt Eng, RAG + Fine-tuning
- prompt engineering = designing prompts to elicit desired model behaviors
	- key is understanding how different structures impact outputs
	- strategies:
	    - <mark style="background: #ADCCFFA6;">one-shot prompting</mark> = provide a single example of desired output
	    - <mark style="background: #ADCCFFA6;">few-shot prompting</mark> = provide multiple examples to offer pattern/context
	    - <mark style="background: #ADCCFFA6;">chain-of-thought prompting</mark> = encourage explicit step-by-step reasoning
	    - combining strategies can improve effectiveness:
	        - few-shot for context + chain-of-thought for reasoning
- <mark style="background: #FFB8EBA6;">RAG</mark> = combines information retrieval with generation to enhance response accuracy
    - retrieves relevant documents from external sources → retrieved content conditions the generation process
	- especially useful for knowledge-heavy or fact-based tasks
	- viewed as dynamic prompt engineering via retrieval systems
- fine-tuning techniques 
	- <span style="color:rgb(255, 136, 0)">general fine-tuning</span> 
		- fine-tuning = adapt a pretrained model by updating its parameters on task-specific data
		- improves specialization (e.g. industry terms, tone, style)
	- <span style="color:rgb(255, 136, 0)">adaptive fine-tuning</span>
		- adapt model on a dataset closely aligned to task requirements
	- <span style="color:rgb(255, 136, 0)">adapters</span> = small task-specific modules added to a frozen pretrained model
		- only adapter layers are trained
		- allows efficient fine-tuning
		- configurations:
			- single adapter per task
			- multiple parallel adapters for multi-tasking
			- scaled adapters for complex tasks
	- <span style="color:rgb(255, 136, 0)">behavioural fine-tuning</span>
		- modifies output behavior (e.g. more ethical, polite, or helpful)
	- <span style="color:rgb(255, 136, 0)">prefix-tuning</span> = appends a learnable prefix to input sequences
	    - core model remains unchanged
	    - lightweight and efficient
	    - specialized adaptation without full retraining
	- <span style="color:rgb(255, 136, 0)">PEFT</span> = fine-tune large models with minimal compute/memory overhead, types include:
		- LoRA = low-rank adaptation of weights
		- qLoRA = quantized LoRA for greater efficiency
	- <span style="color:rgb(255, 136, 0)">instruction-tuning</span>
		- instruction tuning = fine-tune models to follow explicit user instructions more reliably
	- <span style="color:rgb(255, 136, 0)">RLHF</span>
		- RLHF = uses human feedback to iteratively improve model responses
## 6.2 Model Ensembling
- <mark style="background: #FFB8EBA6;">ensembling</mark> = combining multiple models to outperform individual models
	- traditional in smaller ML models, increasingly useful in LLMs due to response variability
	- can be optimized via:
		- quantized models
		- prediction caching
		- selective use based on low confidence
- model averaging = compute and average softmax probability distributions across models
- blending = straightforward combination of outputs for prediction
- weighted ensembling = assign different weights to models based on:
	- empirical performance
	- domain expertise
	- improves prediction relevance per task
- stacked ensembling (2 stage model)
	- stacked ensembling = use a secondary model (metamodel) to combine outputs from base models
	- metamodel learns patterns in LLM output space
- diverse ensembles for robustness
	- use varied model architectures (e.g. encoder–decoder + transformer-based)
	- improves coverage of edge cases and response diversity
- multi-step decoding + voting
	- voting mechanisms = models vote on next token/phrase
		- types: majority, weighted, ranked voting
		- ensures frequent tokens dominate; filters out outliers
	- useful in high-latency, high-accuracy contexts
- composability 
	- composability = flexibly chain or combine model outputs
	- avoids retraining a single, massive model for multi-step tasks
	- enables pipelines of smaller, specialized models
		- e.g. summarization → translation → sentiment analysis
## 6.3 Finetuning vs Prompt Eng
- primary factor = **cost**
	- prompt engineering
		- faster to iterate
		- low cost (few hours of experimentation)
	- fine-tuning
		- expensive (can cost thousands)
		- better for highly specialized tasks

![[Screenshot 2025-07-30 at 8.06.12 am.png| center | 600]]

## 6.4 Model Optimisation
- mixture of experts (MoE)
    - MoE = architecture with many specialized subnetworks (experts) inside one large model
    - uses conditional computation to activate only relevant experts per input
    - uses a gating network to score experts per token
        - softmax scores produce probabilities over experts
        - top 2 experts per token are selected and receive weighted token representation
    - benefits
        - internal specialization across tasks without retraining the full model
        - only activated experts receive gradient updates during backpropagation
        - enables efficient scaling due to sparse computation
    - challenge: load balancing
        - without constraints, gating overloads some experts and neglects others
        - solution: load-balancing loss
            - measures fraction of tokens and gating mass per expert
            - added to training objective to encourage even distribution
- model optimization for resource-constrained devices
    - <mark style="background: #FFB8EBA6;">compression techniques</mark> = reduce compute + memory needs while preserving performance
    - <span style="color:rgb(255, 136, 0)">prompt caching</span>
        - stores previously computed outputs for frequent prompts
        - avoids recomputation
    - <span style="color:rgb(255, 136, 0)">KV caching</span>
        - stores key–value attention tensors from previous tokens
        - reduces redundancy in transformer-based models
    - <span style="color:rgb(255, 136, 0)">quantization</span>
        - reduces model weight precision (e.g. 32-bit → 8-bit or 4-bit)
        - lowers memory usage and speeds inference with minimal accuracy loss
    - <span style="color:rgb(255, 136, 0)">pruning</span>
        - removes unnecessary weights or neurons
        - structured pruning = removes entire components like layers or neurons
        - unstructured pruning = removes individual weights based on importance
    - <span style="color:rgb(255, 136, 0)">model distillation</span>
        - smaller student model learns to mimic a larger teacher model
        - uses teacher logits or intermediate representations as supervision
        - produces faster, lighter models with similar behavior
## 6.5 Lessons for Effective LLM Development
- scaling laws
	- model performance scales with data, model size, and compute
	- diminishing returns appear beyond certain scale thresholds
	- doubling both model size and data leads to stronger performance than doubling one alone
- chinchilla models
	- prioritize training on more data with a fixed-size model
	- smaller models with more data outperform larger models trained on less data for same compute budget
- learning rate strategy
	- key for training stability and performance
	- warm-up: slowly increase learning rate at start
	- decay: gradually reduce learning rate to stabilize convergence
- overtraining and regularization
	- overtraining = model becomes too fit to training data, hurting generalization
		- signs: validation loss increases while training loss decreases
		- also: confident but incorrect outputs on test data
	- mitigation
		- early stopping = monitor validation metric and stop when it deteriorates
		- regularization = add penalties to discourage overly complex fits (e.g. weight decay)
- speculative sampling
	- speeds up autoregressive decoding during inference
	- uses smaller model to generate token candidates
	- larger model verifies and accepts or rejects the predictions

---

# 7 API-First LLM Deployment
## 7.1 API strategies
- developing APIs for LLMs
    - APIs = standardized interfaces for clients to interact with LLM services and models
    - allow developers to integrate and consume LLM functionalities from different sources
- principles of web APIs
    - high cohesion = API components are focused and related, making them easier to understand and maintain
    - loose coupling = components are independent, allowing changes without affecting others
    - results in more flexible and maintainable systems
- API-led architecture strategy
    - design approach using APIs to build LLM-based systems that are:
        - scalable
        - reusable
        - flexible
        - accessible from anywhere
        - capable of handling large volumes of traffic and data
- types of web APIs
    - stateful APIs
        - maintain client or user session state
        - allow personalized and context-aware responses
    - stateless APIs
        - treat each request independently
        - no information stored between requests
        - failure in one request doesn't affect others
- step 1: define your API’s endpoints
    - common endpoints include:
        - `/generate` = generate text from prompts
        - `/summarize` = perform text summarization
        - `/embed` = return embeddings for input data
- step 2: choose an API development framework
    - framework selection depends on requirements like language, scalability, and deployment preferences
## 7.2 Optimising RAG pipelines
- crucial for efficient information retrieval and generation with low latency
- asynchronous querying
	- processes multiple queries concurrently
	- reduces wait times by sending requests in parallel to the vector store
- retrieval techniques
	- <span style="color:rgb(255, 136, 0)">dense retrieval</span> = uses embeddings in vector space for semantic similarity
	- <span style="color:rgb(255, 136, 0)">sparse retrieval</span> = uses term-based methods like TF-IDF for exact keyword matching
	- combining both = leverages strengths of semantic and keyword relevance
- embedding caching
	- stores computed embeddings for repeated queries
	- avoids recomputation, speeds up retrieval
- key–value (KV) caching
	- stores intermediate or final query–response results
	- if the key (query) repeats, retrieves the precomputed value
	- used in both retrieval and generation phases to reduce latency
	- especially useful in high-traffic RAG systems
- distributed inference orchestration
	- enables scalable infrastructure
	- distributes incoming requests across multiple nodes
	- essential for large-scale systems to maintain responsiveness and throughput


---

# 8 LLM Evaluations
## 8.1 Why Evaluation is a Hard Problem
- developing and deploying ML solutions
    - requires new forms of testing and evaluation beyond traditional software
    - ML models involve randomness during training
        - must be tested:
            - in aggregate across datasets
            - on atomic, targeted examples to validate training success
    - most trained ML models are deterministic at inference i.e. same input → same output
- pre-deployment requirements
    - ML systems must demonstrate expected performance before production
    - need monitoring tools to detect and resolve issues post-deployment
- challenges in evaluating LLMs
    - <mark style="background: #FF5582A6;">language complexity</mark> - human language is difficult to quantify
        - hard to create accurate, generalizable evaluation metrics
    - <mark style="background: #FF5582A6;">data overlap</mark> - models trained on massive corpora
        - difficult to find evaluation data not already seen by the model
    - <mark style="background: #FF5582A6;">bias</mark> - LLMs may replicate social, legal, or ethical biases present in training data
    - <mark style="background: #FF5582A6;">input space</mark> - infinite number of possible inputs
        - exhaustive testing is impossible hence must evaluate across representative *categories* of scenarios
- evaluation categories

| Dimension                    | Key questions                                                                                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Informativeness & factuality | Is the output factually accurate?<br>Does it include all relevant information?<br>Is it a complete answer to the prompt?                                             |
| Fluency & coherence          | Are outputs grammatically correct and readable?<br>Is there logical flow and structure?<br>Is the language appropriate for the context?                              |
| Engagement & style           | Is the output interesting and engaging?<br>Does it match the desired tone or writing style?                                                                          |
| Harm & bias                  | Does the model produce harmful or dangerous content?<br>Could the content be used maliciously or put people at risk?<br>Does it reflect biased language or concepts? |
| Grounding                    | Is the output grounded in real-world facts?<br>Are references accurate and relevant?<br>Does it avoid hallucinations?                                                |
| Efficiency                   | How much compute is required for inference?<br>What is the response latency?<br>How long does full generation take?                                                  |

- ensemble of LLM evaluators
    - used to assess multiple factors like fluency, grammar, and factuality - no single metric captures all evaluation dimensions
- metric conflicts
    - “good performance” is multidimensional, improving one factor (e.g. factuality) may harm another (e.g. style or fluency)
- interpretability limitations
    - LLMs lack traditional interpretability tools, too many parameters + non-deterministic behavior limit transparency
## 8.2 Evaluating Performance
- evaluation methods
	- <mark style="background: #ADCCFFA6;">manual evaluation</mark> = labor-intensive and depends on human judgment
	- <mark style="background: #ADCCFFA6;">automatic evaluation</mark> = uses tools or LLMs to assess outputs
	- <mark style="background: #ADCCFFA6;">user feedback</mark> = identifies weak performance areas
- metric types
	- n-gram-based metrics = check overlap with ground-truth sequences
	- similarity-based metrics:
		- BERTScore = measures content and fluency similarity
		- SemScore = evaluates semantic equivalence
		- MoverScore = measures transformation distance between texts
	- LLM-based metrics = use LLMs to detect hallucinations and assess quality
	- benchmarks useful for comparison but must be applied with caution

| Failure mode          | Where to evaluate            | Tools/signals                            |
| --------------------- | ---------------------------- | ---------------------------------------- |
| Hallucinations        | Retrieval, prompt, inference | Similarity to source, factual checks     |
| Prompt regressions    | Orchestration                | Prompt diffing, quality degradation logs |
| Latency spikes        | Inference, retrieval         | p95/p99 latency metrics, tracing         |
| Data drift            | Input, retrieval             | Embedding shifts, cluster distribution   |
| Inconsistent behavior | Inference                    | Session-level tracing, repeat queries    |
| Safety violations     | Output                       | Toxicity filters, PII detection          |

- evaluating what breaks before it breaks everything
	- failure modes = recurring, explainable breakdowns in model behavior
		- often subtle or silent (fluent but factually wrong)
	- proactive evaluation is essential to catch early indicators
	- common failure modes:
		- hallucinations
			- arise from prediction-based generation
			- require longitudinal monitoring + output logging
			- in RAG, linked to retrieval quality
		- prompt regressions
			- subtle prompt changes cause degraded output
			- requires prompt diffing and version control
		- latency spikes
			- especially impactful at p95/p99 percentiles
			- causes include long inputs, retrieval delays, API bottlenecks
		- data drift
			- retriever drift = returned documents lose relevance
			- embedding drift = similarity metrics degrade
			- use clustering, token length histograms, and similarity monitoring
			- metrics:
				- mean average precision (MAP)
				- mean reciprocal rank (MRR)
				- F1-score (harmonic mean of precision + recall)
		- inconsistent behavior
			- stems from LLM nondeterminism
			- monitor session logs, sampling settings, prior interactions
			- can enforce consistency with greedy or beam decoding
	- evaluation frameworks must allow metric customization and CI/CD integration

![[Screenshot 2025-07-30 at 6.51.38 pm.png| center | 600]]

- metrics for RAG applications
	- prompt augmentation
		- combines developer-crafted prompt + retrieved text + user input
		- sent to LLM to generate context-aware output
	- key retrieval metrics:
		- recall = percentage of relevant documents retrieved
		- MRR = how early useful docs appear in the results
		- MAP = relevance consistency across retrieved results
	- LangSmith tool
		- define test datasets + evaluators
		- supports metric or rubric-based scoring
		- usable in dev and CI/CD pipelines
		- supports drift detection over time using fixed test sets

![[Screenshot 2025-07-30 at 5.58.06 pm.png| center | 500]]

- metrics for agentic systems
	- agentic system = modular AI that autonomously plans and acts toward goals
		- composed of LLMs, tools, and sub-agents
		- adds complexity to evaluation
	- challenges:
		- dynamic behavior = emergent, context-dependent responses
		- integration = real environments surface unseen issues
		- variability = environmental changes or agent interactions alter behavior
	- evaluation approaches:
		- human evaluators
		- LLM evaluators = cost-efficient, but potentially biased
	- four core evaluation objectives:

| Dimension               | Key metrics / focus                                                                         |
| ----------------------- | ------------------------------------------------------------------------------------------- |
| Internal properties     | Adaptation speed; agent cooperation; coherence; responsiveness; logs & longitudinal testing |
| Engineering performance | Stress testing; fault injection                                                             |
| Interaction quality     | Session length; latency; engagement surveys; real-world user studies                        |
| User satisfaction       | Feedback signals (thumbs up/down); sentiment analysis; Net Promoter Score (NPS)             |

- system lifecycle stages:
	- stage 1: model development = test agent routing, prompt orchestration
	- stage 2: deployment = trust, user relationship, sandbox A/B tests
	- stage 3: production monitoring = agent utilization, session length, churn indicators
## 8.3 General Eval Considerations
- success = defined by user satisfaction and real-world performance
- auto-metrics support fast experimentation and A/B testing
	- especially useful for optimizing prompts and reducing cost
- user feedback (thumbs, ratings, retries) helps identify blind spots
	- examples of signals = dwell time, abandonment rate, retry frequency signal user experience
- feedback becomes a driver of improvement
	- used in human-in-the-loop tuning and reward modeling
	- integrated feedback closes loop between deployment and iteration
- the value of automated metrics
	- enable scalable, fast testing of new prompts or models
		- allow systematic comparison in A/B tests
		- used to balance performance and compute cost
- model drift
	- can result from version updates - sometimes model improves; other times performance drops
	- drift detection helps surface unexpected regressions
	- important to test before and after version shifts
## 8.4 Traditional Metrics aren't Enough
- metrics like accuracy/loss miss real-world failure modes
	- e.g. hallucinations, ethical violations, structural inconsistency
	- production demands real-time, observability-first evaluation e.g. detect anomalies, track drift, trace failures
- <mark style="background: #FFB8EBA6;">observability</mark> = traceability across the full pipeline

![[Screenshot 2025-07-30 at 7.07.07 pm.png| center | 600]]

## 8.5 Observability Pipeline

- enables root-cause detection and continuous monitoring
- preprocessing and prompt construction
	- dynamic, template-based prompts increase complexity
	- must be syntactically correct and semantically clear
	- monitor prompt versions, token length, formatting
	- malformed or truncated prompts cause downstream errors
- retrieval in RAG pipelines
	- assess relevance, freshness, and timeliness
	- log retrieved docs for reproducibility
	- monitor similarity to ground-truth + latency
	- detect embedding drift by tracking embedding distribution stats
- LLM inference
	- track:
		- factuality
		- hallucination rate
		- fluency
		- latency
	- log:
		- token counts (input/output)
		- sampling parameters
		- model versioning
		- abrupt length changes
	- deeper tools:
		- self-consistency checks
		- confidence scores from classifiers
		- trace visualization + structured logging

![[Screenshot 2025-07-30 at 7.07.25 pm.png| center | 400]]

- postprocessing and output validation
	- ensures outputs meet required format (e.g. valid JSON)
	- schema validators enforce structural integrity
	- automated checks catch anomalies like empty completions
- capturing feedback
	- collect:
		- explicit ratings
		- behavioral indicators (dwell time, retries, escalation)
	- feedback reveals blind spots missed in static benchmarks
	- feedback becomes training data for updates
- four feedback-based monitoring stages:
	- stage 1: threshold-based alerts
		- static limits on key metrics (e.g. response time > 2s)
	- stage 2: statistical anomaly detection
		- use rolling metrics (z-scores, moving averages)
	- stage 3: drift detection
		- monitor query patterns, embedding similarity, data shifts
	- stage 4: feedback signal monitoring
		- track rating trends, fallback frequency, satisfaction metrics

---

# 9 Governance: Monitoring, Privacy and Security 
- privacy vs security
    - privacy = control over who can access personal information
    - security = protection of that information from unauthorized access, leaks, or theft
- data handling in traditional vs LLM models
    - traditional ML models
        - operate on structured, labeled data
        - domain-specific, tightly scoped
        - governed by straightforward evaluation (precision, recall, F1)
        - easier to comply with regulations like GDPR
    - LLMs
        - trained on vast, unstructured data scraped from the internet
        - datasets may include PII, medical records, private messages
        - impossible to fully audit training data
        - data is encoded in distributed parameters, not as records
        - very difficult to “unlearn” data once it's absorbed
- interpretability challenges
    - LLMs are massive, complex, and non-transparent
    - specific outputs can’t be easily traced to specific training data
    - they infer and extrapolate rather than simply classify or predict
## 9.1 LLM Security Threats
- two broad categories:
	- <mark style="background: #FFB8EBA6;">adversarial attacks</mark> = manipulate the model’s behavior
	- <mark style="background: #FFB8EBA6;">data breaches</mark> = models unintentionally leak sensitive training data
- adversarial attacks
    - <mark style="background: #FFB8EBA6;">prompt injection</mark>
        - occurs via manipulation of prompts submitted to the model
        - models typically use *metaprompts* with placeholders for user inputs
        - two types:
            - direct prompt injection = user embeds malicious instruction directly
            - indirect prompt injection = third-party content introduces the malicious prompt
    - <mark style="background: #FFB8EBA6;">jailbreaking</mark>
        - tricks model into bypassing safeguards
        - often exploits reward alignment mechanisms (human preference scoring)
- other security risks
    - data poisoning = malicious data introduced during training, biases or corrupts model outputs
    - model inversion = attackers infer sensitive training data by probing model outputs
    - membership inference = attacker determines whether a data point was in training set
    - model stealing = reverse engineer or replicate a model via queries or output probing
    - supply chain attacks = compromise occurs during data collection, training, or deployment
        - includes attacking dependencies like tokenization libraries
    - resource exhaustion = denial-of-service (DoS) attacks via traffic floods or bot queries → degraded performance/outages

![[Screenshot 2025-08-01 at 9.37.35 pm.png| center | 500]]

## 9.2 Model/LLM Audit/Validation
- security audit = structured and systematic process to evaluate safety, fairness, privacy, and robustness of an llm system across training data, model behavior, deployment context, and downstream tasks
	- audit steps
	    - define scope and objectives
	    - gather information
	    - risk analysis and threat assessment
	    - evaluate security controls and compliance
	    - perform penetration testing (red teaming)
	    - review model training data
	    - assess model performance and bias
	    - monitor and review
	    - document findings and recommendations
	    - communicate results and remediation plan
- audit team composition
    - ML engineers, security specialists, software developers = understand technical vulnerabilities
    - SMEs, data scientists = domain relevance and data quality
    - product managers, risk managers = strategic alignment and risk management
    - legal and compliance officers = legal compliance
    - external auditors, end users = external validation and user experience
- audit timeline
    - simple app + simple model = 2–4 weeks
    - enterprise-scale llm applications = 1–3 months depending on complexity, log access, data volume, integrations

![[Screenshot 2025-08-01 at 9.38.00 pm.png| center | 600]]

- 1. define scope and objectives
    - goal = define minimum acceptable behaviour under normal and adversarial conditions to set baseline for privacy, security, and robustness evaluations
    - test technical readiness and resilience by measuring code maturity
    - patch known and unknown risks
        - known risks = documented in internal issue logs or known to engineering team
        - unknown risks = untested behaviours, addressed via penetration testing
    - code maturity = levels of robustness, reliability, and security in code powering the llm system and its infrastructure, demonstrated by rigorous testing, best practices, and regular updates
    - vulnerability management = process of identifying, assessing, mitigating, and monitoring security vulnerabilities in the llm system and its deployment environment
    - security controls table

| category                       | description                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| authentication/access controls | robust mechanisms for identification and authorization to ensure safe interactions             |
| complexity management          | clear modular structure separating system logic into well-defined functions                    |
| cryptography/key management    | safe use of cryptographic primitives and secure mechanisms for key generation and distribution |
| testing and verification       | comprehensive unit tests, integration tests, and verification methods with sufficient coverage |

- 2. gather information
    - collect documentation to assess vulnerabilities, design, and compliance
        - architecture diagrams to reveal structural and integration vulnerabilities
        - training data details to identify biases and data quality issues
        - access control policies to review security and authorization practices
        - monitoring and logging procedures to ensure active tracking of irregularities
    - deliverables
        - model inventory sheet listing all models, purposes, and ownership
        - model risk scorecards based on internal evaluations
        - data provenance documentation
        - signed system architecture and policy plan
- 3. risk analysis and threat modeling
    - goal = evaluate how the system can fail, be attacked, or be misused by internal or external actors, and recommend mitigation strategies
    - internal vs external threats and risks

| actor           | threats                                                                                       | risks                                                                |
| --------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| internal actors | accidental misuse <br> data tampering <br> insider access abuse <br> poor security hygiene    | biased outputs <br> data breaches <br> reputational damage           |
| external actors | hacking attacks <br> data poisoning <br> social engineering attacks <br> supply chain attacks | model manipulation <br> financial losses <br> operational disruption |

- 4. evaluate security controls and compliance
    - review access control measures to ensure only authorized individuals can access model weights, prompts, logs, datasets, and fine-tuning instructions
    - verify absence of misconfigurations that could expose sensitive assets
- 5. perform penetration testing (red teaming)
    - penetration testing = controlled hacking simulations to find vulnerabilities before real attackers
        - simulate prompt injection, data poisoning, and social engineering
        - attempt unauthorized access to the llm system or its training data
        - analyze llm outputs for biases under specific prompts
        - identify insecure llm-related apis that expose vector databases or retrieval systems
    - red teaming = advanced, goal-oriented simulation mimicking real attackers (white-hat hacking)
        - multistep attacks: indirect prompt injection, data poisoning, social engineering, jailbreaking, privilege escalation, data exfiltration
        - covers model exfiltration in multitenant or federated environments and fine-tuning pipeline attacks
        - stress-tests monitoring, detection, and incident response procedures
- 6. review training data
    - understand sources and risk profile of data used for training
    - identify vulnerabilities such as pii exposure or bias
    - monitor vendor patch notes and model updates for new risks
    - verify embedding inputs do not reintroduce pii or exploitable patterns
    - deliverable = signed document mapping potential risks based on model provenance
- 7. assess model performance and bias
    - periodic internal evaluation of llm behaviour in intended use case
    - identify if model favours or disadvantages specific groups
    - flag performance gaps across geographies and languages
    - document benchmark scope limitations and domain-specific edge tests required
    - note geographic gaps as privacy and security blind spots, with bias toward english and western conventions
- 8. document findings and recommendations
    - consolidate audit outcomes into a structured report for transparency and stakeholder alignment
    - include numerical ratings for severity, implementation difficulty, or other criteria
    - provide clear prioritization for remediation actions
- 9. plan ongoing monitoring and review
    - define continuous monitoring frameworks, change management protocols, disclosure processes, update cadence
    - commit to documenting prompt changes, model version updates, and access control modifications
- 10. communicate results and remediation plan
    - clarify ownership and timelines for remediation tasks
    - tailor communication to stakeholder groups

| stakeholder role        | key information                                            | communication style                                                         |
|-------------------------|------------------------------------------------------------|------------------------------------------------------------------------------|
| technical team          | detailed vulnerabilities, code changes, security patches  | technical language with tool references and feasibility focus               |
| management/executives   | high-level risk overview, impact, remediation timeline     | focus on cost-effectiveness, brand protection, and strategic priorities     |
| security team           | exploit potential, monitoring enhancements, policy alignment | emphasize risk reduction and collaborative mitigation planning             |
| nontechnical stakeholders | user safety, privacy implications, high-level remediation overview | clear, benefit-oriented language linking security to organizational goals |

- human-in-the-loop reviews
    - inject human checkpoints at critical stages to review outputs and flag biased, unsafe, or contextually inappropriate content
- guardrails = policies, checks, and automated tools that keep llm applications aligned with intended safe, compliant, and ethical behaviour
    - types of technical guardrails
        - real-time filters to block harmful content
        - rate limiters to prevent abuse
        - prompt validation systems to detect malformed or malicious inputs
        - output classifiers to enforce content policies
        - model quantization or distillation to meet performance targets
        - automated testing pipelines for continuous real-time evaluation
    - operational guardrails
        - human-in-the-loop review cycles for high-stakes scenarios
        - escalation workflows for incident management
        - model version controls and prompt change logging
        - anomaly alerts for sudden shifts in output quality or response times
    - governance guardrails
        - clear documentation of policies and procedures
        - defined incident response plans
        - regular regulatory compliance audits



![[Screenshot 2025-08-01 at 9.38.21 pm.png| center | 500]]

---

# 10 Scaling: Hardware, Infra and Resource Management
- third-party API-based approach = start by using models directly from the cloud before building your own solution
- scaling and resource allocation
    - monitoring = track key performance indicators to understand application behavior and resource needs
    - automating deployments = adjust resources automatically based on monitored metrics
    - scaling techniques:
        - sharding = split model weights or layers across multiple GPUs
            - trade-off: increased synchronization complexity
        - activation checkpointing = save only essential activations during backprop and recompute others
            - trade-off: extra compute time
        - dynamic batching = group incoming requests on the fly to maximize GPU utilization
            - trade-off: slight increase in response latency
        - model offloading = move unused model parts to CPU or disk, fetch when needed
            - trade-off: slower inference due to data transfers
        - mixed precision training = use lower precision (e.g., FP16) for weights and activations
            - trade-off: negligible loss in numerical accuracy
        - quantization = compress model weights to 8-bit or lower
            - trade-off: potential accuracy degradation if not tuned
        - gradient accumulation = split large batches into smaller chunks and accumulate gradients
            - trade-off: slower overall iteration time
        - ZeRO optimizer = partition optimizer states and gradients across devices
            - trade-off: increased communication overhead
        - operator fusion = combine multiple operations into one to reduce intermediate memory usage
            - trade-off: requires advanced compiler/tool support
        - paged attention = stream key–value cache in/out like virtual memory for long contexts
            - trade-off: needs smart scheduling
- monitoring metrics
    - latency = response time for user queries; goal is to minimize
    - throughput = number of requests processed per second; indicates capacity under load
    - resource utilization = CPU, GPU, memory, disk I/O, network bandwidth
    - error rates = server errors, token-limit breaches, safety-triggered responses
- A/B testing vs shadow testing
    - A/B testing = deploy two models (“champion” vs “challenger”) live and compare performance
    - shadow testing = run challenger on real inputs in background without affecting live outputs
        - benefit: identify issues and fine-tune challenger before public rollout
- compute-optimal argument = balance between model size (parameters) and training data volume to maximize use of compute resources
    - models trained at compute-optimal balance require less downstream fine-tuning
- memory optimization techniques

| Technique                | Problem solved                        | How it works                                     | Trade-off                            |
| ------------------------ | ------------------------------------- | ------------------------------------------------ | ------------------------------------ |
| sharding                 | model too big for one GPU             | split weights/layers across GPUs                 | syncing and communication complexity |
| activation checkpointing | high memory during backprop           | save key activations, recompute others           | extra compute time                   |
| dynamic batching         | wasted compute on small requests      | group inputs dynamically                         | slight response delay                |
| model offloading         | GPU memory insufficient               | move unused parts to CPU/disk, fetch when needed | transfer-induced slowdown            |
| mixed precision training | activations and weights too large     | use FP16 instead of FP32                         | minor loss in numerical precision    |
| quantization             | model too large for deployment        | compress weights to lower bit-width              | potential accuracy loss              |
| gradient accumulation    | batch size too big for GPU            | split batch into chunks, accumulate gradients    | slower iteration                     |
| ZeRO optimizer           | redundant optimizer state across GPUs | partition optimizer state and gradients          | communication overhead               |
| operator fusion          | many small intermediate tensors       | merge operations to reduce memory ops            | needs compiler/tool support          |
| paged attention          | memory spikes from long contexts      | stream KV cache like virtual memory              | requires smart scheduling            |

- backup and restore testing
    - test restore process regularly = verify backups are recoverable
    - hot storage = immediate access (e.g., cloud folder)
    - cold storage = cost-effective but slower access (e.g., archived disk)

---

# 11 The Future of LLMs and LLMOps
- scalability by design = architectures built from the ground up for efficient, targeted scaling rather than simply increasing parameter count
- hierarchical attention networks = multi-layer models with each layer optimized for a specific domain (reasoning, emotion, creativity)
- modular llms = collections of expert submodels delegated to handle specialized tasks instead of one monolithic model
- neurosymbolic ai = hybrid architectures combining neural network pattern-matching with symbolic, rule-based reasoning for traceable, consistent outputs
- sparse models = activate only the most relevant parameters or neurons per query to reduce resource consumption
	- mixture of experts (MoE) = sparse architecture using a gating network to select a subset of expert subnetworks for each input
- memory-augmented architectures = models with persistent memory layers that store and retrieve long-term user interactions and evolving knowledge
- retrieval-augmented generation evolution = hybrid systems with real-time retrieval mechanisms to integrate up-to-date information dynamically
- data curation = automated cleaning, augmentation, and validation techniques to ensure training datasets are diverse, accurate, and representative
- synthetic data = machine-generated data supplementing real-world corpora to speed up training, enhance privacy, and mitigate data scarcity
	- Microsoft phi-4 small language model = example of a compact llm using synthetic data to achieve strong benchmarks at low cost

---
