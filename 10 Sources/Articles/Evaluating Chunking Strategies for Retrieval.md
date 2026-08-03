---
type: article
status: structured
quality:
topics: [rag, evaluation-metrics]
source: ""
created: 2025-08-16
published:
author: ""
flashcards: none
updated: 2025-12-28
---
by Chroma Research
---
tags:
  - rag
  - evaluation-metrics
  - experiment-design
  - model-algorithms
creation_date: 2025-08-16
---

![[Screenshot 2025-08-16 at 12.21.56 pm.png| center | 500]]

# 1 Key findings (what actually moved the needle)

- **Measure retrieval at the token level, not document rank.** IoU (token-wise Jaccard), token-precision, and token-recall better reflect RAG needs than nDCG/MAP because LLMs mostly care _that_ the right tokens are present, not where they sit in the list.
- **Chunk size and overlap materially change performance and cost.**
    - With OpenAI `text-embedding-3-large`, **smaller chunks (~200 tokens) with zero overlap** deliver strong, consistent token-efficiency (higher IoU/precision) and competitive recall.
    - **Large chunks with heavy overlap (e.g., 800 size / 400 overlap—common defaults)** give _the worst_ precision/IoU and only middling recall → wasteful context and more distractors.
- **Heuristic RecursiveCharacterTextSplitter (RCTS) can be very good—if tuned.** At **200 tokens, 0 overlap**, RCTS outperforms TokenTextSplitter on ≤400 token settings for precision/IoU and stays competitive on recall. Reducing overlap helps IoU by cutting redundancy.
- **Semantic, embedding-aware chunkers help:**
    - **ClusterSemanticChunker** (global similarity packing):
        - **400-token max:** very high recall (~0.913).
        - **200-token max:** **best precision/IoU** (most efficient) with average recall.
    - **LLM-driven chunking** (LLMSemanticChunker): **highest recall (~0.919)** but only average efficiency and is slower/costlier to run.
    - **KamradtSemanticChunker (default)** underperforms; **size-bounded modification** improves metrics notably.
- **Embedding model matters:** With **MiniLM-L6**, some **overlap (~50%)** improved recall (e.g., 250/125). With stronger embeddings, overlap was less helpful and often harmful to efficiency.

# 2 Practical suggestions (drop-in guidance)

1. **Start with a solid default (most RAG apps, strong embeddings):**
    - **Chunker:** RecursiveCharacterTextSplitter
    - **Chunk size:** **200 tokens**
    - **Overlap:** **0**
    - **Separators:** include punctuation (`["\n\n","\n",".","?","!"," ",""]`) to avoid tiny fragments.
        This maximises token-efficiency and keeps recall competitive.
2. **If you need more recall (answers straddle boundaries / long facts):**
    - Try **ClusterSemanticChunker (max 400)** for higher recall without exploding context, or
    - Increase size to **400, 0 overlap** with RCTS as a lighter-weight step.
3. **If you’re on a smaller/shallower embedding (e.g., MiniLM-L6):**
    - Use **moderate overlap (~50% of chunk size)** to recover recall (e.g., 250/125).
    - Re-evaluate if/when you upgrade embeddings—overlap may become counterproductive.
4. **Avoid these anti-patterns:**
    - **Huge chunks (≥800) + heavy overlap (≥50%)** as global defaults → poor precision/IoU and unnecessary cost.
    - Blindly using library defaults; tune for your corpus and embedding model.
5. **Evaluate like you mean it (fast loop):**
    - Track **IoU, token-precision, token-recall** on your **own corpus**.
    - Add **PrecisionΩ** (precision assuming perfect recall) to understand the best-case efficiency of your chunking.
    - Test with **k≈5 retrieved chunks** (as in the paper) and then sweep k to match your app’s tolerance for context size.
6. **When to try advanced chunkers:**
    - **ClusterSemanticChunker:** when you want **higher efficiency (200)** or **higher recall (400)** with an embedding-aware method; plan for **re-chunking** when the corpus grows (global optimisation).
    - **LLM chunking:** when **max recall** is paramount and you can tolerate **slower, costlier indexing**; keep it for offline build pipelines, not hot paths.
7. **Operational tips:**
    - Keep chunk sizes **within** your embedding/LLM context headroom (account for metadata).
    - Prefer **0 overlap by default**; add overlap only when your evals show recall gaps.
    - Re-run the eval after major **embedding/model** or **domain** changes.
8. **Know the limits:**
    - The study’s dataset is modest and partially synthetic; treat the **patterns** as starting points and **validate on your data**.
    - Runtime wasn’t benchmarked; LLMSemanticChunker is notably slower.
