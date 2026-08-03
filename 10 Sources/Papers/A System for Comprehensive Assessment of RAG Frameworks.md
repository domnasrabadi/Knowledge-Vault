---
type: paper
status: raw
quality:
topics: [rag, llm-evaluation]
source: "https://arxiv.org/pdf/2504.07803"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# A System for Comprehensive Assessment of RAG Frameworks

## Metadata
- Author: Mattia Rengo; Senad Beadini; Domenico Alfano; Roberto Abbruzzese
- Category: pdf
- URL: https://arxiv.org/pdf/2504.07803
## Highlights
- retrieval-augmented generation (rag) = technique that improves factual accuracy and context relevance of large language models by retrieving external information before generation
    - dual nature makes evaluation harder than for standalone llms
- scarf = low-level, extremely modular evaluation framework for rag systems
    - enables holistic black-box testing suited to real-world deployments
- key components
	- context relevancy = checks if retrieved passages are both relevant to the input query and sufficiently focused to support accurate response generation
	- retrieval metrics = precision, recall and other scores that judge the quality of retrieved documents
	- generation metrics = overlap-based scores such as BLEU and ROUGE plus llm-based metrics that assess output quality
	- faithfulness = measures whether the generated answer is fully supported by the retrieved context
	- answer relevancy = evaluates how directly and completely the response addresses the user’s query
	- synthetic-data generation = automatic creation or augmentation of test datasets (e.g. new question–answer pairs) to extend evaluations without manual labeling
	- multi-rag testing = side-by-side benchmarking of several rag pipelines under identical conditions
	- external rag support = ability to evaluate third-party rag endpoints through black-box interfaces
- key evaluation gap addressed
    - traditional metrics like perplexity or human annotation poorly capture the interplay between retrieval and generation
    - scarf adds specialised metrics and tooling that link retrieval performance to downstream answer quality

---
