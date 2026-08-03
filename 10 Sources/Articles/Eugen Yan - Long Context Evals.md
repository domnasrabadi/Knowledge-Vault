---
type: article
status: structured
quality:
topics: [llm-evaluation, rag, evaluation-metrics]
source: ""
created: 2025-06-29
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- **evaluating long-context question & answer systems**
    - complexity increases as documents get longer
    - key evaluation challenges
        - <mark style="background: #FFB8EBA6;">information overload</mark> = irrelevant details obscure relevant facts, hindering retrieval and answer generation
        - <mark style="background: #FFB8EBA6;">positional variance</mark> = evidence can appear anywhere in the text (start, middle, end), stressing models prone to lost-in-the-middle effects
        - <mark style="background: #FFB8EBA6;">multi-hop reasoning</mark> = correct answers depend on synthesising evidence scattered across the text, challenges model to retain/integrate info far apart
        - <mark style="background: #FFB8EBA6;">hallucinations at scale</mark> = large contexts raise the risk of plausible but incorrect responses - due to poor retrieval/retention
        - <mark style="background: #FFB8EBA6;">open-ended questions</mark> = broad or interpretative queries rarely have a single definitive answer
- key evaluation metrics
    - two orthogonal dimensions guide assessment
        - <mark style="background: #FFB8EBA6;">faithfulness</mark> = answer relies only on the source document and model knows when to say “i don’t know”
            - false positives = hallucinated content absent from the document
            - false negatives = system misses information that actually exists in the context
            - citation accuracy complements faithfulness by checking evidence links
        - <mark style="background: #FFB8EBA6;">helpfulness</mark> = answer is relevant, comprehensive, and concise
            - relevance = directly addresses the query
            - comprehensiveness = includes all necessary details
            - conciseness = avoids unnecessary fluff
    - Xu et al 2023 found domain experts (e.g. biology & economics) preferred answers to be both comprehensive + faithful
	    - hence for QA systems for power users + experts, system should focus on being faithful + comprehensive answers
    - best answers balance both dimensions ✅
        - grounded in the text (faithful)
        - directly answer the question (relevant)
        - provide sufficient context (comprehensive)
        - remain succinct (concise)
- **building an evaluation dataset** 
	- begins with creating a robust eval dataset
	- process
	    1. draft diverse, realistic questions with language-model assistance then refine via human annotators
		    - much faster + practical then humans crafting from scratch 
	    2. use precise prompts to steer useful question generation
		    - need to guide model towards natural, useful questions - don't use vague prompts
		    - be specific and precise 
	    3. ensure question diversity, eval dataset should have mix of: 
	        - fact recall = who, when, what queries testing basic extraction
	        - definitions = explain domain-specific terms found in the text
	        - summarisation = identify and condense core ideas
	        - inference and reasoning = integrate information to answer implicit why or how questions
	        - no-info = questions unanswerable from the document, testing refusal behaviour
	    4. vary evidence position and include multi-hop questions to stress long-context abilities
		    - purposely create questions that need answers from various parts e.g. start, middle, end 
- **methods to assess Q&A performance**
    - human annotation remains the gold standard for ground truth
	    - also useful for calibrating automated evaluators (LLM-as-judge), even training small models if enough data
        - <mark style="background: #FFB8EBA6;">faithfulness annotation</mark> = grade answers on accuracy spectrum, including no-info labels
            - incorrect answer / hallucination = fabricates details
            - incorrect refusal = claims info absent when present
            - correct refusal = declines when info truly missing
        - <mark style="background: #FFB8EBA6;">helpfulness comparison</mark> = pairwise judgement of which faithful answer serves the user better
            - can also use relative/pairwise judgements here - often easier for humans
            - for comparing helpfulness, criteria can include:
	            - relevance = does 1 answer more directly/precisely address the question?
	            - comprehensiveness = does 1 answer include key info other one has missed?
	            - conciseness = is 1 answer more succinct or easier to understand?
        - annotation best practices ✅
            - clear, concise guidelines with examples
	            - include examples for each category + how tohandle edge cases
            - iterate using annotator feedback
	            - collect annotator feedback, improve guidelines on challenging/unclear cases
            - qualification tasks to ensure understanding
	            - provide annotators w practice examples w known correct answers 
	            - ensures they understand guidelines + can apply consistently
            - measure inter-annotator agreement (e.g., cohen’s kappa)
	            - low agreement can indicate unclear guidelines or ambiguous scenarios
            - hire subject-matter experts for specialised domains
	            - specific domains need SMEs for accurate + meaningful evals
    - automated evaluation (“LLM-as-judge”) augments scalability
	    - since humans can be very costly especially for very large documents
        - automated metrics relied on historically fall short in Q&A tasks
	        - n-gram metrics like BLEU or ROUGE poorly correlate with human judgement on open-ended Q&A
        - model-based evaluators calibrated on human-labelled data give finer-grained results + capture nuances
            - claim extraction = break answers into atomic statements and verify each against the text
	            - breaking answers into collections of individual claims helps verification + pinpoint hallucinations
		- when including citations for claims, can perform additional evals
			- this allows us to distinguish between 2 different failure modes (hallucinations vs retrieval failures)
			- done via comparing judgements to human annotations, w 2 key metrics
	            - recall = proportion of unfaithful claims correctly flagged
	            - precision = proportion of flagged claims that are truly unfaithful
        - evaluating helpfulness is more nuanced since "helpfulness" of an answer is a spectrum
	        - different strategies for varying levels of detail/explanation style
	            - reference-based comparison when high-quality answers exist
	            - criteria-based rubrics mirroring human guidelines - works best for clearly defined rubrics
	            - pairwise comparisons for iterative system improvement 
	        - pairwise evals especially reliable for calibrating an LLM-as-judge on helpfulness
		        - present pairs of responses (response A vs response B) to human + LLM-as-judge
		        - measure alignment - how often they agree on the more helpful answer
		        - use correlation metrics e.g. Cohen's Kappa to quantify
- **lessons from existing benchmarks**
    - NarrativeQA = tests narrative comprehension across novels and movie scripts by generating questions from summaries and answering with full texts
    - NovelQA = evaluates understanding of entire novels (〉200 000 tokens) and shows performance drops when evidence appears beyond 100 000 tokens
    - QASPER = targets academic papers, measuring both answer accuracy (answer-f1) and evidence selection (evidence-f1)
    - L-Eval = mixes closed- and open-ended tasks across datasets such as coursera, sfiction, codeu, longfqa; demonstrates llm evaluators align better with humans than traditional metrics
    - HELMET = offers seven task categories with contexts up to 128 000 tokens, emphasising retrieval, reasoning, and instruction following while rejecting purely synthetic tasks
    - LOONG = multi-document benchmark (financial, legal, academic) with spotlight, comparison, clustering, and chain-of-reasoning tasks; reveals that rag can hurt deeper synthesis performance
- **key takeaways**
    - faithfulness and helpfulness are independent qualities; great answers satisfy both
    - faithful systems also recognise when information is absent
    - traditional n-gram metrics fail on long-context q&a; llm-based evaluators work better
    - evidence position affects accuracy; lost-in-the-middle and extreme-length issues persist
    - rag may decrease performance on tasks requiring integrated reasoning across large or multiple documents






