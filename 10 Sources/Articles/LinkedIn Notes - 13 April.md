---
type: article
status: structured
quality:
topics: [model-monitoring, rag]
source: ""
created: 2025-04-13
published:
author: ""
flashcards: none
updated: 2025-12-28
---
From the posts:
- Rahul Agarwal - [Few lessons from deploying and using LLMs in Production](https://www.linkedin.com/posts/rahulagwl_few-lessons-from-deploying-and-using-llms-activity-7316301476941701120-BxFr/?utm_source=share&utm_medium=member_desktop&rcm=ACoAADOImawBMLLj-bS4dtOrUO43T6G38Uw8kBE)
- Eugene Yan - [Evals for Building a Chatbot for Very Long Documents](https://www.linkedin.com/posts/eugeneyan_if-you-were-building-a-qa-feature-or-chatbot-activity-7315546528368992256-4XLo?utm_source=share&utm_medium=member_desktop&rcm=ACoAADOImawBMLLj-bS4dtOrUO43T6G38Uw8kBE)
- Eugen Yan (Repost) - [Pinterest Optimisation to Embeddings](https://www.linkedin.com/posts/nirant_pinterest-boosted-search-relevance-by-80-activity-7316724508340432896-0WIF?utm_source=share&utm_medium=member_desktop&rcm=ACoAADOImawBMLLj-bS4dtOrUO43T6G38Uw8kBE)
- Eugene Yan - [System Design for Production Recommender Systems](https://www.linkedin.com/posts/eugeneyan_cant-wait-for-when-i-can-vibe-code-a-production-activity-7315229423278952448-Rr2D?utm_source=share&utm_medium=member_desktop&rcm=ACoAADOImawBMLLj-bS4dtOrUO43T6G38Uw8kBE)

# 1 Lessons from Prod 
- <mark style="background: #FFB8EBA6;">Cheap is a lie</mark>: cloud costs seem low, but overall expense of LLM system can skyrocket
	- Cache repetitive queries: Users ask the same thing at least 100x/day  
	- Gatekeep: Use cheap classifiers (BERT) to filter “easy” requests. Let LLMs handle only the complex 10% and your current systems handle the remaining 90%.  
	- Quantise your models: Shrink LLMs to run on cheaper hardware without massive accuracy drops  
	- Asynchronously build your caches — Pre-generate common responses before they’re requested or gracefully fail the first time a query comes and cache for the next time.  
- <mark style="background: #FFB8EBA6;">Guard against hallucinations</mark>: models can give outputs with confidence that is challenging to even human reviewers to verify 
	- use RAG - provide model the knowledge in the prompt via semantic similarity query matching
	- use Guardrails - validate outputs w regex or cross-encoders to establish clear decision boundary
		- between query and generated response  
- <mark style="background: #FFB8EBA6;">You don't always need a full LLM</mark>: discriminative models can do a lot of the work 
	- e.g. knowledge distillation - can use large LLM to label your data, then train smaller discriminative model 
	- w similar performance at a much lower cost 
- <mark style="background: #FFB8EBA6;">not about the model, it's about the training data</mark>
	- smaller LLMs might struggle w domain specialised data - which is normal 
	- fine tune your model on your specific data
		- start w PEFT e.g. LoRA 
		- and use synthetic data generation to bootstrap training 
- <mark style="background: #FFB8EBA6;">prompts are the new features</mark> 
	- version them, run AB tests, continuously refine w online experiments
	- consider bandit algos to automatically promote the best-performing variants 

# 2 Evals for Long Context Chatbots 
- e.g. when you're building a QA system or chatbot to use long documents e.g. books 
- 2 important metrics 
	- <span style="color:rgb(255, 0, 247)">faithfulness</span> = grounding of answers in document's content - aka <mark style="background: #FFB8EBA6;">groundedness</mark>
		- not the same as <span style="color:rgb(255, 0, 247)">correctness</span> - answer can be correct but ungrounded to a document
		- sub metric = **precision of citations**
	- <span style="color:rgb(255, 0, 247)">helpfulness</span> = combination of **usefulness** + **completeness**
		- *usefulness* = directly addresses the question w enough detail and explanation 
		- *completeness* = provides enough detail and not too brief 
		- aka <span style="color:rgb(255, 0, 247)">relevancy</span> to an extent
	- **evaluate them separately** 
		- faithfulness is a binary label → use LLM-as-judge
			- e.g. `grounded` vs `ungrounded`
		- helpfulness can use pairwise comparisons → use reward model
			- e.g. doc A > doc B > doc C
- how to build robust evals 
	- use LLMs to generate questions from the text
	- evals should evaluate positional robustness 
		- i.e., have questions at the beginning, middle, and end of text
- potential challenges
	- **open ended questions may have no single right answer**
		- makes reference based evals tricky 
		- e.g. "*What is the theme of this novel?*"
	- **make sure questions are representative of prod traffic**
		- e.g. mix factual, inferential, summarization and definition questions 
- benchmark datasets for inspiration 

| Name                                                  | Description                                                                                                                  |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| NarrativeQA                                           | Questions based on entire movie scripts or novels. Includes reference answers useful for LLM-eval comparisons.                 |
| NovelQA                                               | Q&A over full novels; includes both MCQ and free-form responses, and includes references.                                    |
| Qasper                                                | Similar to NarrativeQA, but with academic documents that are 5-10k tokens, and includes evaluation of answer spans.          |
| LongBench                                             | Average of 6.7k words across fiction and technical docs.                                                                   |
| LongBench v2                                          | Extension of LongBench, but evals are MCQ only.                                                                              |
| L-Eval                                                | 20 tasks and >500 long documents (up to 200k tokens), with several QA-oriented tasks.                                       |
| HELMET                                                | Includes reference-based evaluation for long-context QA, and includes measures for positional robustness.                    |
| MultiDoc2Dial                                         | Modeling dialogues grounded in multiple documents. Evaluates ability to integrate info over multiple docs.                   |
| Frustratingly Hard Evidence Retrieval for QA Over Books | Reframed NarrativeQA as open-domain task where book text must be retrieved.                                                 |

# 3 How Pinterest Optimised their RecSys
- many search/recsys systems use embedding models to find semantically similar items
	- Pinterest made breakthrough using a single model to embed queries, pins and products
	- called OmniSearchSage 
- how it works 
	- before = trained separate embedding model for each type (queries, pins, products)
	- now = single model learns unified representation across all 3 (queries, pins, products)
		- single embedding space allows same query vector to retrieve relevant pins, shopping items + related queries
			- better performance than task specific models 
- results
	- increased search relevance by 80% vs old model (online)
		- offline evals gave 30% boost
	- increased ad clickthrough rate by 5% 
	- increased engagement (saves + clicks) by 67%
	- serving 300k queries per second, <3ms latency 
		- using hybrid cache/inference system
- why it works 
	- <mark style="background: #FFB8EBA6;">richer content representation</mark> 
		- most pins have missing or low quality text
			- Pinterest generates synthetic caption using BLIP + adds board titles (from user-curated collections)
			- and logs most common queries that led to engagement 
		- these diverse sources are layered into the entity embedding
	- <mark style="background: #FFB8EBA6;">multi-task, multi-entity training</mark> 
		- single DistilBERT encoder learns multilingual query embeddings
			- these are aligned w unified pin/product embeddings trained using 3 types of tokenizers + hash embeddings
		- tasks include 
			- Query → Pin Query → Product Query → Query (for autocomplete + related queries)
	- <mark style="background: #FFB8EBA6;">compatibility encoders</mark> 
		- embeddings trained to be compatible w legacy embedding model outputs
			- to help avoid breaking downstream systems 
		- enables smooth rollout + avoids retraining other models
	- <mark style="background: #FFB8EBA6;">efficient serving</mark> 
		- query embeddings cached w 30 day TTL and only recomputed if missing 

# 4 Article 4 
Can't wait for when I can vibe code a production recommender system.  
  
Until then, here's some system design  
• Retrieval vs. Ranking: [https://lnkd.in/gxcK_ff](https://lnkd.in/gxcK_ff)  
• Real-time retrieval: [https://lnkd.in/g3ZuAVqr](https://lnkd.in/g3ZuAVqr)  
• Personalization: [https://lnkd.in/gBKdKCZE](https://lnkd.in/gBKdKCZE)  
• Bandits: [https://lnkd.in/gW7F4X82](https://lnkd.in/gW7F4X82)  
• Reinforcement learning: [https://lnkd.in/gAqV6bpb](https://lnkd.in/gAqV6bpb)  
• Query Matching: [https://lnkd.in/gHmfzjN4](https://lnkd.in/gHmfzjN4)  
• RecSys × LLMs: [https://lnkd.in/g6SAWv33](https://lnkd.in/g6SAWv33)