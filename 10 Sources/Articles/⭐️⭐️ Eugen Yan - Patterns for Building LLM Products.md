---
type: article
status: structured
quality:
topics: [llm-evaluation, evaluation-metrics, rag, prompting]
source: ""
created: 2025-07-22
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- July 2023 post - https://eugeneyan.com/writing/llm-patterns/


# 1 Evals 
- <mark style="background: #FFB8EBA6;">Evals</mark> = measurements that assess llm system or product performance
    - include benchmark data + metrics
    - differentiate rigorous builders from those shipping low-quality products
    - enable detection of regressions across components (llm, prompt, retrieved context, temperature)
    - without evals we fly blind or manually eyeball outputs
- metric categories
    - context-dependent = tailored to a specific task + its context
    - context-free = compare output to gold references only, task-agnostic
## 1.1 Conventional Metrics
- <mark style="background: #FFB8EBA6;">BLEU</mark> = precision-based n-gram overlap metric
	- compute clipped precision for each n, take geometric mean, apply brevity penalty 
	- risk of favoring short outputs if penalty removed

$$
\begin{gather}
\textcolor{magenta}{\textbf{1. Calculate precision for various values of $n$}} \\ \ \\ 
\mathrm{precision}_n
=
\frac{
  \displaystyle\sum_{p \in \mathrm{output}}
    \sum_{n\text{-gram}\in p}
      \mathrm{Count}_{\mathrm{clip}}(n\text{-gram})
}{
  \displaystyle\sum_{p \in \mathrm{output}}
    \sum_{n\text{-gram}\in p}
      \mathrm{Count}(n\text{-gram})
}

\\ \ \\

\textcolor{magenta}{\textbf{2. Clip max number of times an n-gram appears in a reference}} \\ \ \\ 
\mathrm{Count}_{\mathrm{clip}}(n\text{-gram})
=
\min\Bigl(
  \text{matched $n$‑gram count},
  \;\max_{r\in R}\mathrm{Count}(n\text{-gram in }r)
\Bigr)

\\ \ \\

\textcolor{magenta}{\textbf{3. Account for length, apply Brevity Penalty}} \\ \ \\
\mathrm{BP} =
\begin{cases}
1, & \text{if } |p| > |r|,\\[6pt]
\exp\!\Bigl(1 - \tfrac{|r|}{|p|}\Bigr), & \text{otherwise}.
\end{cases}

\\ \ \\

\textcolor{magenta}{\textbf{4. Calculate final BLEU-N Score as geometric mean of all $precision_n$ scores}} \\ \ \\ 
\mathrm{BLEU\!-\!N}
=
\mathrm{BP}
\;\cdot\;
\exp\!\Biggl(
  \sum_{n=1}^{N} W_n \,\log\bigl(\mathrm{precision}_n\bigr)
\Biggr)

\end{gather}
$$

- <mark style="background: #FFB8EBA6;">ROUGE</mark> = recall-oriented family, also counts # of words in reference that also appear in candidate 
	- variants include
		- ROUGE-N = n-gram recall
		- ROUGE-L = longest common subsequence
		- ROUGE-S = skip-bigram

$$
\mathrm{ROUGE\!-\!N}
=
\frac{
  \displaystyle\sum_{s \in r_{\mathrm{references}}}
    \sum_{n\text{-gram}\in s}
      \mathrm{Count}_{\mathrm{match}}(n\text{-gram})
}{
  \displaystyle\sum_{s \in r_{\mathrm{references}}}
    \sum_{n\text{-gram}\in s}
      \mathrm{Count}(n\text{-gram})
}
$$

- <mark style="background: #FFB8EBA6;">BERTScore</mark> = embedding cosine similarity metric, 3 components
	- recall = average similarity of reference tokens to closest output tokens
	- precision = average similarity of output tokens to closest reference tokens
	- F1 = harmonic mean of recall and precision 
	- accounts for synonyms + paraphrases

$$
\begin{gather}
\textcolor{magenta}{\textbf{Calculate precision and recall}} \\ \ \\
\mathrm{Recall}_{\mathrm{BERT}}
=
\frac{1}{|r|}
\sum_{i \in r}
\max_{j \in p}
\bigl\langle \vec{t}_i^r,\,\vec{t}_j^p \bigr\rangle,
\quad
\mathrm{Precision}_{\mathrm{BERT}}
=
\frac{1}{|p|}
\sum_{j \in p}
\max_{i \in r}
\bigl\langle \vec{t}_j^p,\,\vec{t}_i^r \bigr\rangle

\\ \ \\
\textcolor{magenta}{\textbf{Calculate final F1 BERTScore}} \\ \ \\
\Large
\mathrm{BERTScore}
=
F_{\mathrm{BERT}}
=
\frac{2 \,\cdot\, \mathrm{Precision}_{\mathrm{BERT}} \,\cdot\, \mathrm{Recall}_{\mathrm{BERT}}}
     {\mathrm{Precision}_{\mathrm{BERT}} + \mathrm{Recall}_{\mathrm{BERT}}}.

\end{gather}
$$

- <mark style="background: #FFB8EBA6;">MoverScore</mark> = soft-alignment distance between token embeddings via optimal transport
	- maps semantically related words many-to-one
- pitfalls of conventional metrics 
    - ⛔️ poor human correlation = low agreement on creative/diverse tasks
    - ⛔️ poor adaptability = exact-match overlap fails for abstractive summarisation or dialogue
    - ⛔️ poor reproducibility = high variance across studies + implementation details
        - example: MMLU scoring differs across original, HELM, EleutherAI leading to inconsistent rankings
## 1.2 LLM-as-Judge trend
- <mark style="background: #FFB8EBA6;">G-EVAL</mark> = uses chain-of-thought + form filling
	- GPT-4 scorer achieves Spearman 0.514 with humans and excels on coherence, consistency, fluency, relevance
- Vicuna authors employ GPT-4 single-answer grading
	- validated on human judgements, found GPT-4gpt-4–human agreement 85 % > human–human 81 %
- QLORA prompts gpt-4 to rate models vs gpt-3.5; model-level Spearman 0.55 with humans
- common llm evaluator biases + mitigations
	- position bias → swap response order and require double wins
	- verbosity bias → keep compared answers similar length
	- self-enhancement bias → never let same llm grade its own responses
- comparison > direct scoring?
- human vibe check remains indispensable for real-world usefulness
## 1.3 EDD
- Eval-Driven-Development (EDD) workflow
    - collect task-specific evals: prompt, context, reference outputs
    - choose or design metrics that summarise performance across runs
    - automate scoring with strong llm where human labels costly or noisy

---

# 2 RAG 
## 2.1 Terminology
- retrieval-augmented generation (<mark style="background: #FFB8EBA6;">RAG</mark>) = fetch external information + prepend to prompt to ground outputs
    - reduces hallucination and boosts factuality
    - cheaper to update retrieval index than continual llm pre-training
    - leverages classic information retrieval ideas within llm pipelines
    - RAG inference = combines original input with retrieved documents during generation
	    - highlights downsides of pre-trained LLMs: inability to expand or revise memory, lack of insight into generated output, hallucinations
	    - process
	        - concatenate input with retrieved document
	        - generate token $t_i$ based on original input, retrieved document, and previous $t_{i-1}$ tokens
- <mark style="background: #FFB8EBA6;">embedding</mark> = fixed-size vector representing text such that similar items cluster in space
    - similar items are close to each other while dissimilar items are farther apart
	    - good embedding = one that does well on a downstream task such as retrieving similar items
	    - Huggingface MTEB = scores various models on diverse tasks such as classification, clustering, retrieval, summarization, etc
    - embeddings can take many modalities
    - original embedding approaches = traditional methods for word representation
	    - word2vec = neural model predicting word contexts
	    - fastText = extends word2vec by incorporating subword information
- limitations of embedding-based search = effective in many cases but falls short for certain queries
    - searching for a person or object’s name (e.g., Eugene, Kaptir 2.0)
    - searching for an acronym or phrase (e.g., RAG, RLHF)
    - searching for an ID
- keyword search = models simple word frequencies and doesn’t capture semantic or correlation information
    - fails to handle synonyms or hypernyms
    - combining semantic and keyword search = complementary approach to improve recall and precision
- metadata = attributes used to refine retrieval results and downstream ranking
    - prioritize documents that are cited more
    - boost products by their sales volume
## 2.2 Advanced Techniques
- dense passage retrieval (DPR) = uses dense embeddings for document retrieval to outperform sparse baselines like Lucene BM25
    - fine-tunes two independent BERT-based encoders on existing question–answer pairs
    - passage encoder $E_p$ embeds text passages into vectors
    - query encoder $E_q$ embeds questions into vectors
    - retrieve top-$k$ passages most similar to the question embedding
    - what if we don’t have relevance judgments for query-passage pairs?
        - without them, training bi-encoders to embed queries and documents in the same space where relevance is the inner product would be impossible
- hypothetical document embeddings (HyDE) = reframes relevance modeling as a generation task by creating and encoding a hypothetical document
    - prompts an LLM to generate a hypothetical document given a query
    - uses an unsupervised encoder such as Contriver to encode the hypothetical document into an embedding vector
    - computes inner product between hypothetical-document embedding and corpus embeddings to retrieve most similar real documents
    - leverages dense bottleneck as a lossy compressor to exclude extraneous, non-factual details
- retrieval-enhanced transformer (RETRO) = integrates retrieval into transformer pre-training using a frozen retriever, differentiable encoder, and chunked cross-attention
    - performs retrieval at every pre-training step, not just during inference
    - for each input chunk $C_u$, retrieve $k$ chunks $\mathrm{RET}(C_u)$
    - encode neighbors as $E_{u,j} = \mathrm{Encoder}(\mathrm{RET}(C_u)_j, H_u) \in \mathbb{R}^{r \times d_0}$
    - encoding of retrieved chunks depends on attended activation of the input chunk
    - use encoded neighbors $E_{u,j}$ to condition generation of the next chunk
- instructor model = prepends task descriptions to text during training to produce task-specific embeddings via prompt tuning
    - customizable prepended prompt such as “represent the `<domain>` `<task_type>` for the `<task_objective>`”
    - example prompt: “represent the wikipedia document for retrieval”
- internet-augmented LMs = augment LLMs with off-the-shelf search engines
    - retrieve relevant documents via Google Search
    - chunk long documents into paragraphs of six sentences each
    - embed query and paragraphs using TF-IDF
    - rank paragraphs by cosine similarity
## 2.3 Nearest Neighbour Search 
- approximate nearest neighbors (ANN) = retrieves approximate top-$k$ similar vectors quickly by partitioning the embedding space
    - build partitions over the embedding space to zoom into relevant regions
- Nearest Neighbour algos
	- locality sensitive hashing (LSH) = create hash functions so that similar items map to the same buckets, enabling efficient ANN queries
	- facebook AI similarity search (FAISS) = use quantization and indexing for efficient retrieval, support both CPU and GPU, handle billions of vectors via efficient memory use
	- hierarchical navigable small worlds (HNSW) = build a hierarchical graph embodying the small-world phenomenon to allow coarse-to-fine search via minimum hops
	- scalable nearest neighbors (ScaNN) = two-step process of coarse quantization followed by fine-grained search, offering best recall/latency trade-off
- evaluating ANN indexes = assess performance based on key factors
    - recall: performance against exact nearest neighbors
    - latency/throughput: number of queries handled per second
    - memory footprint: RAM required to serve the index
    - ease of adding new items: ability to add without full reindexing versus needing index rebuild

---

# 3 Fine-tuning
- fine-tuning = process of taking a pre-trained model and further refining it on a specific task
    - variants
        - continued pre-training = with domain-specific data, apply same pre-training regime (next-token prediction, masked language modeling) on base model
        - instruction fine-tuning = fine-tune pre-trained model on instruction–output pairs to follow instructions, answer questions, be waifu, etc
        - single-task fine-tuning = hone model for a narrow task such as toxicity detection or summarization
        - reinforcement learning with human feedback (RLHF) = combines instruction fine-tuning with RL
            - collect human preferences via pairwise comparisons
            - train reward model on comparisons
            - optimize instructed LLM via RL method such as `PPO`
    - performance & control = can improve an off-the-shelf base model and may surpass a 3rd-party LLM
    - modularization = use an army of smaller models each specialized on tasks like content moderation, extraction, summarization
    - reduced dependencies = fine-tune and host own models to reduce legal concerns about proprietary data exposure
- challenges
    - need significant demonstration data
        - e.g. InstructGPT used 13 k instruction–output samples for supervised fine-tuning, 33 k comparisons for reward modeling, 31 k unlabeled prompts for RLHF
    - alignment tax = potential lower performance on certain critical tasks
- workflow steps
    - target task fine-tuning = fine-tune LM with data from the domain of the specific task
    - classifier fine-tuning = augment model with two linear blocks and fine-tune on classification tasks (sentiment analysis, question classification, topic classification)
- pre-train + fine-tune paradigm examples
    - BERT (encoder only) = pre-trained on masked LM + next sentence prediction on wikipedia and bookscorpus; fine-tuned on classification, tagging, QA
    - GPT (decoder only) = pre-trained on bookscorpus via next-token prediction; fine-tuned on classification, textual entailment, similarity, QA; auxiliary LM objective aids generalization
    - T5 (encoder-decoder) = pre-trained on C4 with denoising objective; fine-tuned on text classification, abstractive summarization, QA, machine translation; represents all tasks as text-to-text
    - InstructGPT = base `GPT-3` pre-trained on common crawl, webtext, books, wikipedia; supervised fine-tuning on demonstrations; reward model trained on comparisons; optimized via `PPO` focusing on alignment
- fine-tuning techniques
    - soft prompt tuning = prepend trainable tensor to input embeddings; soft prompts learned via backprop
    - prefix tuning = prepend trainable parameters to hidden states of all transformer blocks; LM parameters frozen
    - adapter technique = add fully connected layers after attention + feed-forward in each transformer block; adds 3.6 % parameters per task; within 0.4 % of full fine-tuning on GLUE
    - low-rank adaptation (LoRA) = adapters as product of two low-rank matrices; weight updates have low intrinsic rank; implicit regularization; outperforms full fine-tuning and other baselines
    - QLoRA = extend LoRA to 4-bit quantized models
        - innovations: 4-bit normalfloat, double quantization, paged optimizers to prevent OOM
- how to apply fine-tuning
    - collect demonstration data/labels via
        - experts or crowdsourced annotators with clear guidelines
        - user feedback (thumbs up/down, attribute selection, logs)
        - query larger open models via prompt engineering
        - reuse open-source data (e.g. MNLI for NLI then internal data)
    - define evaluation metrics
    - select pre-trained model e.g. 7B model or small encoder if possible
    - update model architecture if needed (e.g. adjust classification heads or match task)
    - pick fine-tuning approach (`LoRA`, `QLoRA` for parameter-efficient; full fine-tuning for domain pre-training)
    - hyperparameter tuning = learning rate, batch size, number of epochs, LoRA rank, input sequence length, loss type, data ratios

---

# 4 Caching
- caching = technique to store data that has been previously retrieved or computed
    - popularized approach: cache the LLM response keyed on the embedding of the input request
        - for each new request, if a semantically similar request is received, serve the cached response
    - key to adopting pattern: figuring out how to cache safely instead of relying solely on semantic similarity
    - benefits:
        - reduces latency for previously served responses
        - lowers number of LLM requests, saving cost
- example: `GPTCache` ([github.com/zilliztech/GPTCache](https://github.com/zilliztech/GPTCache))
- when a new request is received:
    - embedding generator = embeds the request via models such as OpenAI’s `text-embedding-ada-002`, fastText, sentence-transformers, etc
    - similarity evaluator = computes similarity via the vector store, providing a distance metric
        - vector store options: local (`FAISS`, `Hnswlib`) or cloud-based
        - can also compute similarity via a model
    - cache storage = if the request is similar, the cached response is fetched and served
    - LLM = if the request isn’t similar enough, pass to LLM, generate the result, then serve and cache it
- Redis approach ([video](https://www.youtube.com/live/9VgpXcfJYvw?feature=share&t=1517)): precompute anticipated queries, set a similarity threshold for cached responses
- important considerations:
    - understand user request patterns = design cache thoughtfully for reliable application
    - evaluate caching effectiveness = compute cache hit rate (percentage of requests served from cache)
    - if usage follows a power law (small proportion of unique requests account for majority of traffic, e.g., search queries, product views), caching is effective
- alternative caching keys:
    - item IDs = precompute summaries of product reviews ([link](https://www.cnbc.com/2023/06/12/amazon-is-using-generative-ai-to-summarize-product-reviews.html)) or generate summary for a movie trilogy
    - pairs of item IDs = e.g., comparisons between two movies
        - although this is $O(N^2)$, in practice a small number of combinations drive most traffic
    - constrained input = variables like movie genre, director, or lead actor
        - if a user requests movies by a specific director, run a structured query then refine via LLM for an eloquent response
        - example: generating code from drop-down options ([cheatlayer.com](https://cheatlayer.com)); if verified, cache for reuse
- caching strategy:
    - on-the-fly = cache responses as they are served
    - offline/pre-compute = generate LLM outputs in batch asynchronously before serving
        - batch pre-computing can further reduce cost compared to real-time serving


---

# 5 Guardrails
- guardrails = validate output of LLMs, ensuring syntactic correctness, factuality, safety, and resistance to adversarial input
    - ensure outputs are reliable and consistent enough for production use
    - provide syntactic validation and an additional layer of safety/quality control
- approaches
    - prompt-based control = guide model responses via prompts (e.g. Anthropic’s HHH: helpful, harmless, honest)
    - output validation = enforce structural, type, and quality requirements on LLM outputs (e.g. `Guardrails` package)
        - **single output value validation** = one of predefined choices; length within range; numeric within expected range; complete sentence
        - **syntactic checks** = generated URLs valid & reachable; Python/SQL code is bug-free
        - **semantic checks** = output aligned with reference document or source via cosine similarity or fuzzy matching
        - **safety checks** = free of inappropriate language; high quality of translated text
- NeMo-Guardrails = semantic guardrails for conversational systems (relies on LLMs to validate outputs, inspired by SelfCheckGPT)
    - fact-checking example = ask the LLM if its response is true based on retrieved context
- schema-based steering = enforce specific grammar/format by injecting structure tokens (e.g. Microsoft’s `Guidance`)
    - executes linearly to maintain token order, ensuring the model outputs the exact required structure
- how to apply guardrails
    - **structural guidance** = use tools like `Guidance` to directly control output format
    - **syntactic guardrails** = check categorical outputs against allowed sets; numeric outputs within ranges; verify SQL/code syntax
    - **content safety guardrails** = filter against profanity lists; run moderation classifiers; use profanity-detection models
    - **semantic/factuality guardrails** = validate summaries via semantic similarity or LLM evaluators
    - **input guardrails** = restrict or block inappropriate/adversarial prompts via lists or moderation classifiers

---

# 6 Defensive UX
- defensive UX = design strategy acknowledging inaccuracies or hallucinations can occur in ML/LLM products, anticipating and managing errors gracefully by guiding user behavior and averting misuse
    - benefits
        - increased accessibility = helps users understand ML/LLM features and limitations, making them more accessible and user-friendly
        - increased trust = graceful handling of difficult scenarios and harmful output builds user confidence
        - better UX = handles ambiguous situations and errors, resulting in smoother experience
- guidelines
    - Microsoft’s guidelines for human-ai interaction
        - style = succinct action rules (3–10 words) beginning with a verb, each with a clarifying one-liner
        - organized by interaction stage
            - initially
                - G1 = make clear what the system can do
                - G2 = make clear how well the system can do it
            - during interaction
                - G3 = time services based on context
                - G6 = mitigate social biases
            - when wrong
                - G8 = support efficient dismissal
                - G9 = support efficient correction
            - over time
                - G13 = learn from user behavior
                - G17 = provide global controls
    - Google’s People + AI Guidebook
        - 23 patterns around product-development questions
            - getting started = determine if AI adds value, invest early in good data practices
            - onboarding users = make it safe to explore, anchor on familiarity, automate in phases
            - building trust = set right expectations, be transparent, automate where risk is low
    - Apple’s human interface guidelines for machine learning
        - practitioner knowledge–based, focuses on UI design rather than model internals
        - start by defining ML role: critical vs complementary, proactive vs reactive, dynamic vs static
        - inputs = explicit feedback, implicit feedback, calibration, corrections
        - outputs = mistakes, multiple options, confidence, attribution, limitations
- defensive UX patterns
    - set the right expectations = describe system capabilities & limitations clearly
    - enable efficient dismissal = make it easy to dismiss or ignore undesired AI services
    - provide attribution = explain why the system behaved as it did
    - anchor on familiarity = use familiar UX patterns when introducing AI features


---

# 7 Collect User Feedback 
- collect user feedback = to build our data flywheel
    - data as moat = corpus for pre-training, expert-crafted demonstrations, human preferences for reward modeling
    - deliberate UX design = think about collecting user feedback during UX design
    - feedback types
        - explicit feedback = information users provide in response to a request by our product
        - implicit feedback = information learned from user interactions without requiring deliberate input
    - benefits of feedback = helps models improve and adapt to individual preferences
    - make it easy to provide feedback
        - Microsoft = encourage granular feedback by enabling preferences during regular interaction with AI system
        - Google = let users give feedback via real-time teaching, feedback, and error correction
        - Apple = provide actionable information your app can use to improve content and experience it presents
    - consider implicit feedback
        - arises as users interact and provides wide data on behavior and preferences
        - signals of suggestion helpfulness
            - strong positive = user wholly accepts suggestion
            - positive = user accepts and makes minor tweaks
            - neutral/negative = user ignores suggestion
            - edit-based feedback = user updates comment that led to generated code indicating initial output didn’t meet needs
- other patterns common in ML
    - data flywheel = continuous data collection improves model and user experience, driving more usage and further data to fine-tune models, creating a virtuous cycle
    - cascade = split a complex task into smaller problems so LLM handles tasks it excels at (e.g. reasoning, communication), RAG is an example by augmenting LLM with external knowledge and focusing on reasoning
    - monitoring = track model performance and misbehavior in production, demonstrating AI value or lack thereof
        - example = A/B test of LLM-based customer support showed 12× more losses than human support, leading to discontinuation


---










