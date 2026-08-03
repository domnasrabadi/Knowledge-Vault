---
type: article
status: structured
quality:
topics: [rag, evaluation-metrics, llm-fundamentals]
source: ""
created: 2025-08-16
published:
author: ""
flashcards: none
updated: 2025-12-28
---

# 1 Core takeaways

- **Reranking = fast ROI.** Add a reranker after candidate retrieval to lift recall by ~10–20% without changing your pipeline
	- Biggest gains come from **hard-negative mining** during training.
- **Model roles matter.**
    - **Bi-encoders** (dense embeddings) = cheap, great for _initial_ retrieval over large corpora.
    - **Cross-encoders** = best relevance but too slow for full-corpus search; use only to **rerank top-k**.
    - **ColBERT** = token-level late interaction; strong middle ground (offline doc reps, efficient runtime token matching).
- **Latency is the trade-off.** Expect a few ms to a few hundred ms added by reranking. 
	- Reserve cross-encoders for small k (e.g., 50–200); use GPUs for stricter SLAs.
- **Numbers, geo, popularity ≠ text.** Text encoders **misrepresent numbers and coordinates**; don’t stringify structured fields. 
	- Use **specialised encoders/featurisers** and fuse them with text signals.
- **Biases are curves, not gates.**
	- User intents like “near midtown” are **soft preferences**—apply **distance-decay** or learned weights, not hard filters.
- **Behavioural data is gold.** 
	- Clicks, carts, dwell time dwarf catalog size; use them for **pairwise ranking** and **hard negative mining**.
- **Synthetic data: handle with care.**
	- LLM-generated pairs can be noisy (high hallucination rate); validate aggressively or you’ll poison training.
- **Future is multimodal.** 
	- Build toward **encoder stacking** across text, image, audio, geo, and numerical signals with a learned fusion layer.

# 2 Practical playbook

1. baseline pipeline
	- **Index** with a solid chunker (e.g., ~200-token, 0 overlap) and **dual retrieval** (BM25 + dense).
	- **Candidate set:** retrieve **k₁ = 200–500**.
2. Add Reranker
	- Start with an **off-the-shelf cross-encoder** (e.g., MiniLM/MPNet variant) to **rerank top k₁ → k₂ (e.g., 50)**.
	- **Latency budget:** measure P50/P95; if too high, switch to **ColBERT** or shrink k₁/k₂.
3. Train for your domain
	- **Data:** collect **query → clicked/skipped docs** and mine **hard negatives** (top dense hits that were _not_ clicked).
	- **Fine-tune** the reranker (faster convergence than from scratch) → expect **+2–3%** extra lift.
	- Keep **dev/test** split by time to capture drift.
4. Add specialised agents
	- **Numbers:** bucket/scale numerics; train a **numeric encoder or gradient-boosted scorer** producing a relevance score S_num.
	- **Geo:** compute **distance decay** (e.g., exp(−α·km)) → score S_geo.
	- **Popularity/behaviour:** CTR, conversion, quality signals → score S_pop.
	- **Fusion:** learn weights in a **learning-to-rank** head:
	    `S_final = w_text*S_text + w_colbert*S_colbert + w_num*S_num + w_geo*S_geo + w_pop*S_pop`.
	- Keep **soft constraints** (re-rank by preference) rather than hard filtering where possible.

# 3 Other RAG Components + Considerations

## 3.1 Query handling
- **Decompose complex queries** (“family-friendly hotels with good Wi-Fi near midtown < $400”) into **sub-constraints**, score each with the right encoder, then **fuse**.
- Use **intent templates** to ensure the right encoders fire (geo, budget, amenities, semantics).
## 3.2 Data hygiene & synthetic guardrails
- If you must use synthetic data, **ground** each pair against corpus text, dedupe, and run **LLM critique filters** + **embedding similarity checks**. Keep synthetic to **augmentation**, not the core.
## 3.3 Metrics & monitoring
- Track **Recall@k**, **MRR/nDCG** for ranking quality, and (for RAG) **token-level Precision/Recall/IoU** on downstream answers.
- Monitor **latency** and **cost/query**; alert on drift (embedding/click-mix shifts).
## 3.4 Default configs (safe starting points)
- **Retrieval:** BM25 + dense (k₁=400).
- **Rerank:** Cross-encoder on top-k₁ → **k₂=50** (GPU if P95 > 250 ms).
- **ColBERT** alternative: if traffic is high or latency tight, replace cross-encoder with ColBERT on **k₁=200**.
- **Fusion:** simple weighted sum first; move to learned L2R once you have weeks of feedback data.
- **Bias curves:** exponential distance decay; monotonic constraints for price/ratings.
