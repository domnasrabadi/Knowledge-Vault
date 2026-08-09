---
type: paper
status: structured
quality: 2
topics: [llm-evaluation, evaluation-metrics]
source: https://arxiv.org/abs/2506.13023
created: 2025-07-05
published: 2025-06-16
author: Ethan M. Rudd, Christopher Andrews, Philip Tully
flashcards: none
updated: 2025-12-28
---
1. [[#1 A Practical Guide for Evaluating LLMs and LLM-Reliant Systems|1 A Practical Guide for Evaluating LLMs and LLM-Reliant Systems]]
	1. [[#1 A Practical Guide for Evaluating LLMs and LLM-Reliant Systems#1.1 Metadata|1.1 Metadata]]
2. [[#2 Datasets|2 Datasets]]
3. [[#3 Metrics|3 Metrics]]
4. [[#4 Methodology|4 Methodology]]
5. [[#5 Conclusion|5 Conclusion]]

# 1 A Practical Guide for Evaluating LLMs and LLM-Reliant Systems
---
## 1.1 Metadata
- **Author**: Ethan M. Rudd; Christopher Andrews; Philip Tully
- **Category**: pdf
- **Document Tags**: great
- **URL**: [https://arxiv.org/pdf/2506.13023](https://arxiv.org/pdf/2506.13023)
---
- real-world evaluation challenges = synthetic benchmarks + de-facto metrics fail to capture practical needs
    - de-facto evaluation techniques = commonly used but lack a consistent strategy for real-world goals, system requirements, end-user experience
- practical evaluation framework = proactive process ensuring evaluation aligns with real-world llm system requirements
    - curate representative datasets
    - select meaningful evaluation metrics
    - employ methodologies integrated with development + deployment cycles
- evaluation design pillars
    - **datasets** = representative, high-quality data tailored to evaluation goals
    - **metrics** = quantitative + qualitative measures aligned with objectives
    - **methodology** = overall approach addressing non-determinism, prompt sensitivity, hallucination measurement

![[Screenshot 2025-07-05 at 3.22.33 pm.png| center | 700]]
# 2 Datasets
- evaluation dataset formulation = blueprint for building test data that truly reflects llm production use
    - dataset = prompts + optional ground-truth responses
    - 5 D’s guiding principles
        - **defined scope** = matches tasks the model must perform
        - **demonstrative of production usage** = mirrors real user inputs + scenarios
        - **diverse** = spans problem-space variety to avoid narrow or biased evaluation
        - **decontaminated** = kept separate from training data to prevent inflated scores
        - **dynamic** = treated as a living asset that evolves with the application
- amassing evaluation datasets
    - three approaches
        - **benchmark analysis** = reuse public benchmarks while noting coverage limits
        - **human-annotated golden dataset** = expert-labeled data capturing subtleties like correctness, usefulness, completeness
            - challenges
                - costly, slow, coordination-heavy
                - risk of low-quality or biased labels from limited domain expertise
            - collection workflows
                - in-house SMEs create or label data
                - third-party vendors supply annotations
                - user data + feedback harvested from live products
                - UX research surveys gather fresh prompts
                - clear labeling instructions essential for quality
                - respect privacy constraints + negativity bias in user feedback
        - **synthetically-generated silver dataset** = scalable, cost-effective alternative created by models under human oversight
            - generation techniques
                - frontier-model distillation produces prompt–response pairs
                - Constitutional AI = model self-critiques via principle-based rules
                - Evol-Instruct = iteratively increase prompt complexity or diversity
                - diversity boosting = vary personas or sampling params (temperature, top-p)
            - curate human review to ensure quality, minimize bias, check decontamination
    - metadata curation
        - tags = descriptive categories attached to prompt/response pairs for diversity tracking
        - grounding information = supporting context such as relevant articles
        - expected information = specific facts or steps the model must recall; audit for correctness
    - choosing a curation path
        - bootstrap with benchmarks or golden data, then augment synthetically for broader coverage
        - iterative filtering + enrichment converts silver sets into golden quality
        - automatic domain-text scraping viable if rigorously decontaminated
- adhering to and quantifying the 5 D’s
    - **demonstrative of production usage**
        - classify prompts into representative buckets
        - include user-reported bugs
        - correlate offline metrics with in-product satisfaction; mismatches → dataset not representative
    - **diverse**
        - measure via topic/difficulty tags, lsh or embedding clustering, n-gram or embedding similarity
    - **defined scope**
        - craft component-level datasets akin to unit tests plus end-to-end sets
    - **decontaminated**
        - maintain separate clean eval set
        - detect leakage via continuation tests, log-prob checks, perplexity inspections
    - **dynamic**
        - audit, version-control, update, prune regularly
    - persistent high scores may signal dataset weakness → evolve both data + metrics
- required evaluation set sample sizes
    - sample size formula below 
	    - where $n$ is rough estimate of minimal evat set size to estimate representative + statistically significant outcomes
		    - $z$ = z-score chosen for confidence level
		    - $\hat{m}$ = expected metric score e.g. 80% accuracy
		    - $\epsilon$ = desired margin of error e.g. $z=1.96$ = 5% margin of error
        - example = 95 % confidence (⁠$z = 1.96$⁠), 5 % margin (⁠$\epsilon=0.05$⁠), expected metric $\hat{m}=0.8$ ⇒ $n\approx246$ samples
    - tighter margin → rapidly growing sample requirement

$$
\Large
\text{Required Sample Size: \ \ }
n = z^2 \times \frac{\hat{m}(1 - \hat{m})}{\epsilon^2}
$$

- connecting datasets to the evaluation framework
    - public benchmarks, golden human sets, and synthetic silver sets are complementary tools for achieving the 5 D’s
    - well-curated data aligned with defined scope forms the empirical bedrock for choosing meaningful metrics


![[Screenshot 2025-07-05 at 3.23.04 pm.png| center | 700]]

# 3 Metrics
- metrics selection = chooses quantitative + qualitative measures aligned with evaluation scope + objectives
    - no single metric is a silver bullet → combine several for holistic view
    - datasets must be large enough to support metric computation without heavy compute or quota costs
- **term-overlap metrics**
    - ROUGE = word/phrase overlap for summarisation; surface-level, misses nuance
    - BLEU = n-gram overlap for translation; includes brevity penalty; shares rouge limits
    - keyword selection = run overlap metrics on hand-picked key terms to reduce syntax-over-substance errors
        - effectiveness depends on thoughtful keyword choice + complementary metrics
    - limitations
        - sensitive to length + repetition
        - weak on fluency, factuality, structure
        - paraphrases with identical meaning can score differently
    - recommendation = aggregate scores over multiple diverse, high-quality references per llm response
- **semantic similarity metrics**
    - procedure = embed responses + references, then measure similarity (e.g., cosine)
    - captures syntax, semantics, and structure in one number
    - does not directly evaluate fluency or factual accuracy
- **NLI / entailment metrics**
    - entailment model = fine-tuned classifier judges whether hypothesis follows from premise
	    - useful for factuality checks; quality bound by underlying model
	    - can handle nuance beyond simple metrics
    - combine with statistical tests to assess significance; report effect size for practical impact
	    - i.e. when $p$-value less than chosen sig. level, but low-pval does not indicate magnitude of difference
	    - so consider practical significance 
- **LLM-as-judge/autorater metrics**
    - LLM-as-judge = scalable scoring of fluency, factuality, safety, etc.
        - advantages = quick, covers subjective dimensions humans rate
        - limitations
            - high compute cost, no standardisation
            - biases toward verbosity, position, self-enhancement, list formatting, stylistic cues
            - win/lose tie-break aggregation may distort results
        - performance depends on autorater prompt + grounding context

![[Screenshot 2025-07-05 at 3.23.28 pm.png| center | 600]]

- **perplexity** = negative log-probability of text under a language model; lower $\text{PPL}$ ⇒ higher predicted likelihood
    - loose proxy for real-world quality
    - does not need ground-truth references
- metrics wrap-up
    - no single metric is a "silver bullet"
	    - instead, a holistic understanding of system performance is formed by computing and tracking multiple different metrics
    - balanced scorecard = use multiple metric types to capture multiple quality facets
	    - metric selection = second evaluation pillar, built atop clear objectives + robust datasets

# 4 Methodology 
- robust evaluation methodology & execution = framework for designing evaluation suites that confront real-world LLM challenges
    - confounding factors = inherent non-determinism, input sensitivity, entanglement of grounding data with model prior knowledge
- handling non-determinism + sensitivity
    - sources of non-determinism = stochastic sampling, chained model calls, grounding data or api inconsistencies
    - Self-Consistency = repeat-sampling strategy
        - sample multiple responses with temperature > 0
        - select modal answer to dampen randomness
    - system noise estimation = quantify variability by repeating evaluation nn times (e.g. n≥10n\ge10)
        - compute mean metric + variability band
        - maintain baseline with error bounds to judge future changes
    - prompt sensitivity = small wording, spelling, or spacing tweaks can flip results
        - noise injection techniques
            - case swapping
            - random whitespace insertion
            - random character swapping
            - llm-driven prompt rewrites
        - evaluate impact on
            - overall metrics = which metrics shift most?
            - eval set subgroups = which tasks or topics are fragile?
            - individual data points = which prompts are highly susceptible?
- comprehensive evaluation of LLM system components
    - grounding analysis = determine whether answer correctness stems from provided context or model prior knowledge
        - scoring approaches
            - human annotator rubric
            - llm autorater of context utility
            - automated semantic similarity between prompt and grounding docs
    - ablation evaluation = measure end-to-end performance with and without grounding data
        - drawback = poor at isolating individual component quality when downstream interactions exist
    - grounding module metrics
        - precision (P)
        - recall (R)
        - $F_{\beta}@k$
        - mean reciprocal rank (MRR)
        - normalized discounted cumulative gain (NDCG)
        - mean average P/R/$F_{\beta}$ across retrieval depths
- hallucination & unhelpful responses
    - hallucination probing = pose questions about fictitious entities to see if llm fabricates answers or replies “I don’t know”
        - “I don’t know” detection = heuristic scan or dedicated classifier
    - non-response rate = frequency of unanswered questions when adequate grounding or prior knowledge exists
        - undesirable non-response = LLM fails to answer despite sufficient context
    - trade-off = stricter anti-hallucination prompts can increase undesirable non-response
    - measurement procedure
        - build dataset of prompts about known entities
        - count “I don’t know/does not exist” replies via heuristic or classifier
# 5 Conclusion
- iterative process:
    1. Define clear objectives.
    2. Formulate representative datasets (5 D’s).
    3. Select a balanced suite of metrics aligned with scope.
    4. Apply robust methodology to execute evaluation, addressing non-determinism, prompt sensitivity, hallucinations.
- results serve as actionable guidance for system improvements, not a final grade.
