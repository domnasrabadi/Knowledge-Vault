---
type: article
status: raw
quality: 1
topics: [context-engineering]
source: https://research.trychroma.com/context-rot
created: 2026-01-10
published: 2025-07-14
author: trychroma.com
flashcards: none
updated: 2026-01-11
---

# Context Rot: How Increasing Input Tokens Impacts LLM Performance

<div align="center">
  <img src="https://www.trychroma.com/img/context_rot/card.png" width="220" />
</div>

Source: https://research.trychroma.com/context-rot

Exported at: `2026-01-11T01:21:15Z`


![99](https://www.trychroma.com/img/context_rot/hero_plot.png)

- Because these models achieve near-perfect scores on widely adopted benchmarks like Needle in a Haystack (NIAH) [[1](https://research.trychroma.com/context-rot#niah)], it’s often assumed that their performance is uniform across long-context tasks.
- While scalable, this benchmark typically assesses direct lexical matching, which may not be representative of flexible, semantically oriented tasks.
- We extend the standard NIAH task, to investigate model behavior in previously underexplored settings. We examine the effects of needles with semantic, rather than direct lexical matches, as well as the effects of introducing variations to the haystack content.
- Additionally, we include a conversational question-answer evaluation using LongMemEval [[2](https://research.trychroma.com/context-rot#longmemeval)], as well as a synthetic task in which models replicate a series of repeated words. Each task remains intentionally simple and is deliberately controlled to isolate the impact of context length alone.
- Real applications, such as agent tasks or summarization, demand significantly more processing and reasoning over broader, often more ambiguous information.
- Designing realistic long context benchmarks is challenging. Tasks often grow in complexity as input length increases, making it difficult to isolate whether performance drops are due to longer inputs or inherently harder problems. To address this, our experiments hold task complexity constant while varying only the input length—allowing us to directly measure the effect of input length alone.
- Additionally, long context tasks often involve disambiguating amongst distractors as part of the task
- An important factor in long-context tasks is how input length is scaled
- Various ways to fill irrelevant context are tested, which reveal non-uniform impact on model performance
- This highlights how the type of 'irrelevant content' matters, as some may introduce increasing complexity with input length.
- • Distractors are topically related to the needle, but do not quite answer the question • Irrelevant content is unrelated to the needle and question

![](https://www.trychroma.com/img/context_rot/niah/distractor_irrelevance.png)

- We design four controlled experiments to investigate the influence of these factors:
- Taking a high-similarity needle-question pair, we write four distractors. We have the following setups:
    - Baseline: needle only, no distractors
    - Single distractor: needle + one randomly positioned distractor
    - Multiple distractors: needle + all four distractors randomly positioned We test the impact of distractors on model performance as input length increases to measure non-uniformity amongst distractors and input lengths.
- We demonstrate the following:
    - Across all experiments, model performance consistently degrades with increasing input length.
    - Lower similarity needle-question pairs increases the rate of performance degradation.
    - Distractors have non-uniform impact on model performance with regards to how distracting they are relative to each other. We see this impact more prominently as input length increases, and observe distinctions in how various models respond to them.
    - Needle-haystack similarity does not have a uniform effect on model performance, suggesting the need for further investigation.
    - The structural pattern of the haystack consistently shows an impact on how models process long inputs.
- We write a corresponding question for each topic: > PG essays: "What was the best writing advice I got from my college classmate?" > > arXiv papers: "Which low-latency reranker is preferred for scientific domains?" Before writing our needles, we verify that answers to these questions do not exist in the haystack content: 1. We store our previously computed haystack chunk embeddings in a vector database. 2. Query top-10 results from that vector database with our question embedding. 3. Manually examine these results to verify that they do not answer the given question. This sets up a fair testing environment as it ensures that alternative answers do not exist, and any incorrect answers are due to model hallucinations.
- For each question, we write 8 needles that each belong to the large cluster which we verify using approximate predictions. Needles that belong to the writing/retrieval cluster with >0.9 probability are considered to topically blend into the haystack. We manually write these needles to avoid data contamination. For the 8 needles, we also vary the level of ambiguity, quantified through the following method: 1. Using an embedding model, we compute embeddings for needle and question and their cosine similarity. 2. Repeat across five embedding models (text-embedding-3-small, text-embedding-3-large, jina-embeddings-v3, voyage-3-large, and all-MiniLM-L6-v2).
- At short input lengths, the models perform well even on low-similarity pairs. We see this most clearly in the high/medium-performance models, demonstrating that these models are capable of succeeding at this task for all needle-question pairs.
- The observed performance degradation at longer input lengths is not due to the intrinsic difficulty of the needle-question pairing. By holding the needle-question pair fixed and varying only the amount of irrelevant content, we isolate input size as the primary factor in performance decline.
- Our experiments reveal that the impact of distractors and their non-uniformity amplifies as input length grows across models, including the latest state-of-the-art models. We also observe distinct behaviors across model families in how they deal with ambiguity.

![](https://www.trychroma.com/img/context_rot/niah/distractors_ind.png)

- These failures also reveal model-specific differences in handling ambiguity. Claude models consistently exhibit the lowest hallucination rates. Specifically, Claude Sonnet 4 and Opus 4 are particularly conservative and tend to abstain when uncertain, explicitly stating that no answer can be found. In contrast, GPT models show the highest rates of hallucination, often generating confident but incorrect responses when distractors are present.

![](https://www.trychroma.com/img/context_rot/niah/hallucinations.png)

- However, a natural question arises: does the needle-haystack similarity influence task difficulty at all? Intuitively, if the needle blends in with the content of the haystack, the model may have greater difficulty in extracting the needle.
- On each haystack, we test semantically similar needles against unrelated needles
- Testing across only two topics is insufficient to draw a generalizable conclusion that higher needle-haystack similarity degrades model performance on this task. This does highlight, however, the non-uniform nature of long-context processing. Even when task structure and needle-question similarity are held constant, changing the semantic similarity between the needle and the haystack can influence results
- Aside from needle-haystack similarity, we also consider the structural pattern of the haystack. If the haystack is composed of coherent essays, a randomly inserted needle may disrupt the logical flow of ideas, making it more noticeable. In contrast, in a shuffled haystack of randomly ordered sentences, the needle may blend in more easily since the overall context lacks structure. This follows the assumption that models are sensitive to the logical flow of context—processing it in a structured, order-sensitive manner. Surprisingly, we find that structural coherence consistently hurts model performance.
- Although it seems counterintuitive, models perform worse when the haystack preserves a logical flow of ideas. Shuffling the haystack and removing local coherence consistently improves performance.
- These results may have some implications for the model’s internal processing: structural patterns of inputs could influence how the attention mechanism is applied, particularly as input length increases.
- In an ideal case, the model would be given only the relevant parts so it can focus solely on reasoning. Adding irrelevant context adds the additional step of identifying what is relevant, forcing the model to perform two tasks simultaneously. We systematically test the effect of adding this additional step with increased input length through two conditions: 1. Focused input, containing only the relevant parts and so the model just has to do simple reasoning. 2. Full input, which utilizes the full 113k token LongMemEval input that includes irrelevant context. In this case, the model has to perform retrieval across the long context in addition to reasoning. We verify that the models are highly capable of succeeding on the focused inputs, then observe consistent performance degradation with the full inputs. This performance drop suggests that adding irrelevant context, and thereby adding an additional step of retrieval, significantly impacts a model’s ability to maintain reliable performance.
- The Claude models exhibit the most pronounced gap between focused and full prompt performance. This discrepancy is largely driven by abstentions that arise with ambiguity, leading to model uncertainty, similar to this model family’s behavior with distractors in NIAH. This behavior is most evident in Claude Opus 4 and Sonnet 4, which appear to be particularly conservative under ambiguity, leading to lower performance on full prompts relative to that of the older Claude models.
- As context length increases, performance consistently degrades across all models. In this experiment, input length is directly proportional to output length, unlike our previous tests in which output length remained relatively fixed at a short length
