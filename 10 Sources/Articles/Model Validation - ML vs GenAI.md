---
type: article
status: structured
quality:
topics: [model-risk-validation, llm-evaluation, model-calibration]
source: ""
created: 2025-04-19
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Data & Evaluation Deep‑Dive — Traditional ML vs Gen‑AI

Below is a structured set of talking points **plus probing questions** you can answer as you draft the article. Use them to sharpen each contrast and discover narrative gaps.

|Step|Traditional ML Models|Gen‑AI / RAG / Agentic Systems|Questions to Shape Your Article|
|---|---|---|---|
|**1. Source lineage & governance**|• Tables/views in governed warehouses• Data dictionaries, field‑level lineage in Collibra/Alation• Access via controlled ETL/ELT jobs|• Mix of PDFs, HTML, SharePoint pages, ticket notes, user queries• Often no central metadata or ownership• Continuous ingestion → corpus drift|1. _Does the bank need a “document inventory” governance artefact (version, owner, trust level)?_2. _Who signs off that no copyrighted or confidential info sneaks into RAG?_|
|**2. Feature space**|• Finite, columnar; EDA= distributions, missingness, correlations• Feature engineering tracked in code+documentation• Importance: SHAP, permutation, coefficients|• Feature space = language tokens & retrieval indices → essentially infinite• Prompt tokens, chunk size, embed model act like hidden hyper‑features• “Feature importance” becomes: which passages were retrieved? which prompt phrase triggers behaviour?|3. _Should validators demand retrieval logs + relevance scores as a proxy for feature importance?_|
|**3. Ground‑truth & labelling**|• Stratified train/val/test split; labels often transactional (default flag, churn, etc.)• Limited SME time – but manageable• Label noise addressed with heuristics|• Need _multiple_ test sets: ▸ Knowledge grounding/factuality ▸ Retrieval hit rate ▸ Toxicity / bias guardrails ▸ Adversarial jailbreaks• SME labelling far costlier: must rate _answer quality_, not 0/1 facts|4. _Will you create a “core” dataset of high‑stakes Q&A that business risk accepts as definitive?_5. _How often should labels be refreshed as policies or facts change?_|
|**4. Evaluation metrics**|• Binary: precision, recall, F1, ROC‑AUC• Regression: RMSE, MAE• Well‑defined Type I/II cost trade‑off|• Token overlap (BLEU/ROUGE) too shallow• Semantic similarity (SBERT, BERTScore) ignores hallucination nuances• LLM‑judge or rubric scoring per dimension (truth, relevance, politesse, compliance)• Need _multi‑objective_ dashboards|6. _Which dimensions map to actual bank risks (e.g., factuality → conduct risk; toxicity → reputational)?_7. _Will you weight dimensions or require a pass threshold on each?_|
|**5. Error taxonomy & explainability**|• False positive, false negative easy to illustrate• SHAP plots pinpoint drivers|• Errors can be: hallucination, misretrieval, policy violation, refusal, formatting, latency• Root‑cause tracing requires conversation + trace logs|8. _Can validators replay an answer end‑to‑end (query → retrieval results → final answer)?_|
|**6. Statistical reliability**|• Single model run deterministic• Confidence intervals via cross‑val/bootstrap|• Stochastic decoding: results vary by seed/temperature• Need _n_‑sample evaluation or forced deterministic decoding for tests|9. _Will you enforce temperature = 0 during validation, or evaluate variability explicitly?_|
|**7. Continuous monitoring**|• PSI, KS on features; periodic A/B• Retrain trigger rules|• Detect drift in corpus, embedding recall, answer toxicity spikes• Vendor LLM may update silently|10. _What drift signal should raise an “automatic re‑validation” ticket?_|

---

**Practical Framework Proposal (use/adapt)**

1. **Document Inventory Register**  
    _Fields:_ doc ID, owner, version hash, trust tier, last reviewed.

2. **Evaluation Suite** : _Four buckets:_
	- _Knowledge Grounding_ (100‑200 canonical Q&A, SME‑scored)
	- _Guardrail Stress_ (prompt‑injection, data‑leak attempts)
	- _Adversarial Diversity_ (typos, code‑switching, slang)
	- _User Experience_ (politeness, instruction following)    

3. **Metric Stack**
- Retrieval: Recall@k, MRR
- Generation quality: LLM‑judge rubric (truth, relevance, completeness, tone)
- Safety: toxicity probability, jailbreak detection rate

5. **Validation Playbook**
- Step 1: Pin model & temperature, seed=42.
- Step 2: Run evaluation suite; store raw JSON traces.
- Step 3: SME spot‑check 10% of outputs to verify judge alignment.
- Step 4: Produce multi‑objective scorecard; require pass on _all_ safety metrics, optimise aggregate quality score.
- Step 5: Archive corpus & code hashes for rollback.

---

**Prompting Questions to Refine Your Story**

1. **Proportional Effort** – In scorecards, ~70 % of validation time is data & feature checks. For Gen‑AI, what’s the new split (e.g., 40 % corpus curation, 30 % eval design, 20 % metrics plumbing, 10 % conventional testing)?
2. **Regulatory Language** – Which APRA/BCBS clauses don’t yet map cleanly onto Gen‑AI (e.g., “model transparency”) and need reinterpretation?
3. **Human‑in‑the‑Loop** – Will you argue for an ongoing SME review queue post‑deployment (e.g., 0.5 % of conversations daily)?
4. **Tooling** – Should the validator adopt internal LLM‑powered graders, or insist on purely rule‑based scoring for independence?

  

**❶ New Dimension — People & Skillsets**

|Role Focus|Traditional ML|Gen‑AI / Agentic Systems|Guiding Questions|
|---|---|---|---|
|**Developers**|• Python/SQL, scikit‑learn, XGBoost, pandas• Statistical feature engineering, cross‑validation, SHAP• Occasional model‑ops (Airflow, MLflow)|• Prompt & **RAG** design, vector DBs, embeddings• API orchestration (LangChain, LlamaIndex, OpenAI SDKs) + rate‑limit hygiene• Guardrails & policy filters• Secure handling of PII in chat logs• LLM‑ops pipelines (evaluation harnesses, prompt registries)|1. _Does our bank need an “LLM engineer” job family distinct from data scientist?_2. _Who owns the retrieval layer—data engineering or app dev?_|
|**Validators / Reviewers**|• Strong stats/quant background• EDA, hypothesis testing, error analysis• Familiarity with regulatory docs (SR 11‑7, APRA CPS 220)|• Everything at left **plus**: – Understanding of prompt semantics & injections – Adversarial red‑teaming skills (jailbreak craft, bias discovery) – Systems debugging: trace LLM ↔ tool calls ↔ retrieval – Ability to evaluate _multi‑objective_ scorecards (quality × safety) – Comfort auditing third‑party attestations (model cards, SOC‑2)|3. _Should validators get access to the source prompt library and CI/CD logs?_4. _Do we embed red‑teaming in the validation mandate or in a separate “AI security” team?_|

---

**❷ New Dimension — Thinking Style / Validation Mindset**

|Lens|Traditional ML|Gen‑AI / Agentic Systems|Questions to Prompt Reflection|
|---|---|---|---|
|**Primary Mode**|**Mathematical reasoning**• Pose hypothesis → run experiment → compute metric• Error taxonomy: FP/FN, bias, variance|**Systems & failure‑mode thinking**• Map end‑to‑end graph of components (retriever, LLM, tools, guardrails, UX)• Identify weakest‑link risks (e.g., corpus drift, vendor model change)• Accept _emergent_ behaviour: small prompt tweak → large compliance shift|1. _How do we teach validators to draw sequence diagrams & threat models, not just ROC curves?_|
|**Uncertainty Handling**|• Confidence intervals, p‑values, bootstrap• Sensitivity via perturbing numeric features|• Stochastic decoding, catalogue of _qualitative_ failure modes (hallucination vs. refusal vs. policy breach)• Scenario‑based testing & adversarial prompts rather than parametric sweeps|2. _When does qualitative SME review outrank quantitative scores?_|
|**Decision Rule**|• Optimise a metric (AUC ≥ 0.75) under cost constraint|• **Multi‑objective “gate”**: must _pass_ safety & compliance thresholds before quality is even considered|3. _Do we formalise a veto model—e.g., any red‑team jailbreak blocks go‑live regardless of average helpfulness?_|

---



# 2 Summary 


|                          | ML/Traditional Models                                                                                                            | GenAI Models                                                                                                                                                                                                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| *what's being validated* | static model - maps inputs to a score/category label                                                                             | a system of components <br>(tools, retriever, vec db, guardrails etc)                                                                                                                                                                           |
| *data & inputs*          | mature, well governed, lineage tracked tables                                                                                    | documents, web pages, pdfs, emails<br>usually no formal metadata or rigorous controls                                                                                                                                                           |
| *train/test sets*        | established train/test/(val) split practices                                                                                     | 'gold truth' must imitate real production environment<br>- who authors them?<br>- how many different types should there be?<br>- how big is enough?<br>- do we version control QA pairs like code?                                              |
| *hyperparams*            | well understood/studied for various model families<br>can verify impact via grid search or bayes<br>and settle on final best set | much more range of knobs<br>- temp, top-p, sys + user prompts, tools, retriever options<br>- zero shot, few shot, finetune, distill, COT <br>- LLM chaining, agent patterns<br>how do we check if simpler or alternative approaches considered? |
| *performance metrics*    | F1, MSE, AUC, precision, recall                                                                                                  | many dimensions (often use-case specific)<br>- e.g. helpfulness, groundedness, guardrail categories<br>- which are most defensible + trusted (by regulator) <br>    - e.g. BLEU, LLM Judge, BERTScore...                                        |
| *evaluation sets*        | usually a single test set or cross validation                                                                                    | often multiple e.g. <br>- guardrail test sets<br>- retrieval test sets <br>- full E2E test set                                                                                                                                                  |
| *traceability*           | data construction queries<br>feature attribute methods, surrogate models                                                         | track components via logging intermediate steps<br>- tool calls, parameters, retrieved docs etc                                                                                                                                                 |
| *randomness*             | data construction e.g. fixed periods/conditions<br>setting reproducible seed                                                     | never fully deterministic even with set seed + temperature                                                                                                                                                                                      |
| *monitoring*             | well established metrics<br>- PSI, CSI<br><br>less often retrained                                                               | - regular web content changes<br>- embedding drift<br>- model + prompt versioning <br>- red teaming + periodic sampling<br>- updating ground truths                                                                                             |
| *change materiality*     | - data sources<br>- model use (more fixed generally)                                                                             | - prompt changes?                                                                                                                                                                                                                               |
|                          |                                                                                                                                  |                                                                                                                                                                                                                                                 |
