---
type: book
status: structured
quality:
topics: [interview-prep, ai-engineering]
source: ""
created: 2025-10-19
published:
author: ""
flashcards: none
updated: 2025-10-20
---
![[Screenshot 2025-10-19 at 2.08.48 pm.png| center | 400]]

1. [[#1 ML System Design Interview|1 ML System Design Interview]]
	1. [[#1 ML System Design Interview#1.1 Visual Search System|1.1 Visual Search System]]
	2. [[#1 ML System Design Interview#1.2 Object Detection System|1.2 Object Detection System]]
	3. [[#1 ML System Design Interview#1.3 YouTube Video Search|1.3 YouTube Video Search]]
	4. [[#1 ML System Design Interview#1.4 Harmful Content Detection|1.4 Harmful Content Detection]]
	5. [[#1 ML System Design Interview#1.5 Video Recommender|1.5 Video Recommender]]
	6. [[#1 ML System Design Interview#1.6 Eventbrite Recommender|1.6 Eventbrite Recommender]]
	7. [[#1 ML System Design Interview#1.7 Ad Click Prediction|1.7 Ad Click Prediction]]
	8. [[#1 ML System Design Interview#1.8 Airbnb Similar Listings|1.8 Airbnb Similar Listings]]
	9. [[#1 ML System Design Interview#1.9 Personalised News Feed|1.9 Personalised News Feed]]
2. [[#2 GenAI System Design Interview|2 GenAI System Design Interview]]
	1. [[#2 GenAI System Design Interview#2.1 Foundations|2.1 Foundations]]
		1. [[#2.1 Foundations#2.1.1 Transformer|2.1.1 Transformer]]
		2. [[#2.1 Foundations#2.1.2 Training large-scale models|2.1.2 Training large-scale models]]
	2. [[#2 GenAI System Design Interview#2.2 Parallelism|2.2 Parallelism]]
	3. [[#2 GenAI System Design Interview#2.3 Sampling|2.3 Sampling]]
	4. [[#2 GenAI System Design Interview#2.4 Evaluation|2.4 Evaluation]]
	5. [[#2 GenAI System Design Interview#2.5 Gmail Smart Compose|2.5 Gmail Smart Compose]]
	6. [[#2 GenAI System Design Interview#2.6 Google Translate|2.6 Google Translate]]
	7. [[#2 GenAI System Design Interview#2.7 ChatGPT Personal Assistant|2.7 ChatGPT Personal Assistant]]
	8. [[#2 GenAI System Design Interview#2.8 Image Captioning (Image2Text)|2.8 Image Captioning (Image2Text)]]
	9. [[#2 GenAI System Design Interview#2.9 Retrieval-Augmented Generation (RAG)|2.9 Retrieval-Augmented Generation (RAG)]]


# 1 ML System Design Interview

>[!note] Structure: for each use-case → how the ML system is designed/trained/evaluated (*like a case study*)

## 1.1 Visual Search System
- purpose → given an image, find matching/similar images
    - compute similarities between query image vs vec db image embeddings
- tips on development
    - use pretrained contrastive model (already has good representations)
    - fine tune using relevant training data → reduced training time vs from scratch
- how to perform evals
    - mean reciprocal rank (MRR)
        - rank of the first relevant item in model output, then average them
        - bad for considering just the best/most relevant & ignoring others
    - recall@k
        - number of relevant items among top k items in output/total relevant items
        - bad for search engines where total # relevant items can be massive
        - does not measure ranking quality
    - precision@k
        - number of relevant items among top k items in output/k
        - how precise output is but does not consider ranking quality
    - mean average precision (MAP)
        - consider overall ranking quality
        - good for binary relevances (item = relevant or irrelevant)
        - use nDCG if relevance score is continuous not discrete
    - normalised discounted cumulative gain (nDCG)
        - ranking quality of the output list

## 1.2 Object Detection System
- purpose → blur faces/plates in street view imagery with high recall + precision
	- predict location of each object in image: regression to location (x, y)
	- predict class of each bounding box (dog, cat): multi-class classification
- architecture options
    - one-stage network → single conv net outputs boxes + classes for realtime speed
    - two-stage network →  (RPN + classifier), better accuracy for regulated content
	    - RPN = region proposal network → scan image, process candidate regions likely to be objects
	    - classifier → process each region + classify into object class
- data pipeline
	- feature engineering + data augmentation
		- random crop, saturation, horizontal/vertical flips, rotation/translation, brightness/contrast
		- offline = augment images before training (need additional storage for augmented images)
		- online = augment images on fly during training (doesn't use additional storage)
    - 2 stage network
	    - stage 1 = `[input image -> convolutional layers -> feature map -> region proposal network -> candidate regions]`
	    - stage 2 = `[classifier -> object classes]`
- training signals
    - bounding-box regression with MSE to maximise IOU overlap
	    - regression loss w MSE = bounding boxes of objects predicted should have high overlap w ground-truth bounding box
    - classification cross-entropy per region to label faces/plates/background
	    - classification loss w cross-entropy = how accurate pred probs are for each detected object
    - forward/backward loop tunes shared backbone plus detection heads
- evaluation + serving
    - intersection over union (IOU)
	    - overlap between 2 bounding boxes
    - average precision & per-class precision
	    - precision tracking safeguards against false blur masks
	    - mean average precision MAP
		    - overall precision for all object classes
    - serving
	    - non-maximum suppression (NMS) 
		    - keeps the highest-confidence boxes before applying blur
		    - removes overlapping bounding boxes
- deployment flow
    - batch inference: CPU preprocess → GPU blur service + NMS → publish obscured tiles

## 1.3 YouTube Video Search
- purpose → retrieve relevant clips for text queries by blending visual + lexical signals
- core representation
    - text encoder turns normalised/tokenised queries into embeddings (TF-IDF, learned lookups, transformer sentence reps)
    - video encoder samples frames, extracts embeddings (frame-level ViT or 3D convs), then pools into clip vectors; trades temporal nuance for serving speed
- training loop
    - text/video embeddings → similarity scores → softmax → cross-entropy against clicked/watch pairs
    - hard-negative sampling boosts discrimination between near-duplicates
- evaluation focus
    - precision@k & MAP → not helpful here
    - recall@k → for coverage across huge catalogues
    - mean reciprocal rank (MRR) → to account for first relevant hit where recall alone fails
- prediction pipeline/serving
	- visual search → ANN to find most similar video embeddings to text embedding
	- text search → BM25, find videos w title + tags matching query
    - fusion layer → take 2 lists of relevant videos from previous steps
	    - combine them into new list
	    - reranker → modify new list w business heuristics

## 1.4 Harmful Content Detection
- purpose → flag policy-violating text/image/modal combinations before exposure
- fusion strategies
    - late fusion: independent modality models whose logits blend downstream for modular iteration
    - early fusion: embed modalities jointly so classifier learns cross-modal toxicity patterns
- model architecture (options considered)
    - options
	    - single binary classifier → not easy to identify harmful classes
	    - one binary classifier per class → each model determines if violent, hate, nudity etc
	    - multi-label classifier → single shared model 
	    - multi-task classifier → learns multi tasks simulatenously
			- can learn similarities between task 
		    - no unnecessary computations
    - multi-label/multi-task backbone shares feature extractor with per-class heads (hate, violence, etc.) to exploit inter-class structure
	    - mitigate any modality dominating learning by using gradient blending or focal loss weighting
- training workflow
    - curate balanced batches across classes
	    - supplement with hard negatives from human moderation queues
    - grid-search critical hyperparameters (learning rate, encoder depth) while monitoring per-label lift
- evaluation
    - precision-recall curves to pick thresholds aligned with moderation SLAs
    - ROC + ROC-AUC for overall separability as prevalence shifts
    - inspect confusion matrices per modality to catch over-reliance on single channel

## 1.5 Video Recommender
- purpose → maintain engagement by pairing each session with fresh yet relevant videos
- hybrid retrieval
    - collaborative filtering first pass exploits interaction history with minimal feature engineering
    - content-based filtering second pass injects video metadata to capture sparse interests
- feature blocks
    - video features: language embeddings, duration bucket, BERT title vectors, CBOW tag aggregations
    - user features: id embedding, demographic one-hots, locale embeddings
    - interaction features: search-query encoders, watched/liked video embeddings aggregated over recency windows
- model choices
    - matrix factorisation → fast latent factors optimised via SGD or WALS; struggles with cold-start and ignores side info
    - two-tower neural net: user encoder vs video encoder optimised with cross-entropy; ANN retrieval brings top-k neighbours at inference
- training
    - treat implicit feedback (watch, like, share) as labels; mine hard negatives
    - regularise via dropout + weight decay to stabilise across billions of examples
- evaluation
    - precision@k + mAP to gauge ranking lift
    - diversity metrics ensure list coverage across genres/topics
- serving stack
    - candidate generation ANN narrows to k videos per user in milliseconds
    - scoring/ranking harnesses richer features and heavier models
    - reranking injects business logic like freshness, policy compliance, fairness
- operational challenges
    - serving latency → rely on multi-stage pipelines and cached embeddings
    - cold-start → bootstrap new users with feature-driven tower; seed new videos via exploration buckets

## 1.6 Eventbrite Recommender
- purpose → rank upcoming events per user by balancing relevance, logistics, and social proof
- ranking paradigms
    - pointwise: predict relevance score per `<user, event>` 
	    - simple but ignores list structure
	    - inputs = `item + query`
	    - outputs `relevance score`
    - pairwise: compare event pairs to enforce ordering constraints
	    - inputs = `<item x, item y> + query`
	    - outputs `item y > item x`
    - listwise: optimise entire ranked list, aligns best with downstream metrics
	    - inputs `<item 1, ..., item N> + query ->`
	    - outputs `item 5 > item 2 > item 8`
- feature engineering
	- location
		- walkable score, walk score similarity vs user avg walkable score
		- transit score
		- concatenated features e.g. accessibility + geography + distance
	- time
		- time-to-start, day/hour alignment
		- concatenated features e.g. remaining time + event day/hour
		- decay-weighted recency signals
			- decay factor - for features that rely on user's recent X interactions
	- social
		- friend attendance counts, invites, co-attendance rates
	- user
		- age, gender, historical categories
	- event
		- price, price similarity
- model selection
    - logistic regression/decision trees 
	    - efficient + interpretable
	    - bad for nonlinear + multicollinearity
	- bagging (random forest)
		- ensemble, reduces for variance/overfit quickly but can still have high bias
	- boosting (XGBoost, GBDT)
		- sequential ensemble, reduces bias + variance, slightly slower for train/inference
    - neural nets
	    - can learn nonlinearity + finetune on new data (good for continual learning + unstructured data)
- training considerations
    - severe class imbalance (few RSVPs vs many impressions) → focal or class-balanced loss, plus undersampling negatives
    - binary cross-entropy objective across candidate labels
- evaluation + ops
    - ranking metrics like nDCG, precision@k after discounting by position
    - monitor latency budget since feature fusion spans batch + streaming stores
    - reranking layer can inject fairness, freshness, or business constraints before serving

## 1.7 Ad Click Prediction
- purpose → estimate click-through probability so ranking balances revenue and user experience
- modelling stack
    - sparse categorical inputs embed via per-feature lookup layers before fusion
	- logistic regression
		- what: linear classifier over engineered numeric + one-hot features
		- pros: fast training + scoring; coefficients easy to interpret and monitor
		- cons: can’t capture nonlinear effects or feature interactions without manual crosses; brittle when the feature space is extremely sparse
	  - feature-crossed logistic regression
	      - what: augment linear model with manually defined crosses (products, sums) of base features
	      - pros: keeps inference cheap while adding specific interaction terms; leverages domain intuition
	      - cons: hand-crafted crosses don’t scale; still misses higher-order or unexpected interactions; requires heavy feature-engineering effort
	  - gradient-boosted decision trees (GBDT)
	      - what: ensemble of shallow trees trained sequentially to reduce residual errors
	      - pros: strong out-of-the-box accuracy on tabular data; automatically models nonlinearities and interactions
	      - cons: expensive to retrain or fine-tune continually; doesn’t learn dense embeddings for huge categorical vocabularies; latency can spike with large ensembles
	  - GBDT plus logistic regression
	      - what: use GBDT to select/transform features, then feed into logistic regression
	      - pros: boosts linear model with tree-discovered signals; keeps deployment simple once features are generated
	      - cons: pipeline adds complexity; still struggles with rich interactions; retraining both stages for drift is slow
	  - two-tower neural network
	      - what: separate user and ad encoders map sparse inputs to embeddings, then compute similarity
	      - pros: handles cold-start users via side features; ANN retrieval enables scalable candidate generation
	      - cons: sparse categorical explosion still painful; dot-product limits explicit cross-feature reasoning; harder to debug than linear baselines
	  - deep & cross network (DCN)
	      - what: shared embedding layer feeding parallel deep stack and explicit cross layers
	      - pros: captures high-order feature interactions automatically; keeps inference relatively lightweight compared with massive towers
	      - cons: tuning cross-depth vs deep depth is tricky; still needs solid regularisation to avoid overfitting sparse inputs
	  - factorization machine (FM)
	      - what: learns embedding vector per feature and sums pairwise dot-product interactions
	      - pros: compact way to model all pairwise feature crosses; proven workhorse for CTR tasks with sparse categorical data
	      - cons: limited to pairwise effects; can underfit when higher-order structure matters; training needs careful regularisation
	  - deep factorization machine (DeepFM)
	      - what: combines FM interaction branch with deep neural branch over shared embeddings
	      - pros: captures both low-order (FM) and high-order (DNN) interactions; end-to-end training with shared embeddings
	      - cons: heavier model and tuning overhead; still benefits from feature-store hygiene; variants like xDeepFM or FFM add extra complexity to maintain
- training dynamics
    - positive = click, negative = impression without click; strong class imbalance demands weighting or focal loss
    - binary cross-entropy remains primary objective; monitor normalised CE against baseline CTR model
    - continual learning loop refreshes weights with fresh logs while guarding against concept drift
- feature pipelines
    - batch computation for slow-moving signals (user demographics, creative metadata)
    - streaming computation for rapid counts (recent impressions, cross-device activity)
    - feature store exposes consistent offline/online views to training and serving paths
- evaluation + serving
    - track AUC, logloss, calibration curves; drill into per-segment lift to avoid fairness regressions
    - online ranking: candidate generation service narrows inventory, scoring service applies model, reranking injects policy + pacing constraints
    - latency budget → cache hot embeddings, shard feature lookups, precompute batch scores where feasible

## 1.8 Airbnb Similar Listings
- purpose → surface alternatives close to the currently viewed listing, tuned for short-lived session intent
- modelling approach
    - session-based embedding model treats listing sequences like word windows; sliding window forms positive (co-viewed) and negative pairs
    - shallow neural net learns listing embeddings optimised via dot-product similarity passed through sigmoid with cross-entropy loss
    - augment positives with eventually-booked listings; sample hard negatives from same region to sharpen localisation
- training + evaluation
    - iterate over browse sessions to update embeddings; negative sampling keeps batches balanced
    - monitor average rank of the eventual booking among retrieved candidates as key metric
- serving pipelines
    - training pipeline outputs updated embeddings on cadence aligned with inventory churn
    - indexing pipeline feeds embeddings into ANN index for millisecond retrieval
    - prediction pipeline: take active listing → embed (fallback if unseen) → query ANN → rerank layer enforces business logic, availability, diversity
- challenges
    - cold-start listings handled via metadata-derived fallback vectors until behaviour accrues
    - drift in seasonal travel patterns → retrain cadence plus decay factors on historical windows

## 1.9 Personalised News Feed
- purpose → rank posts per user to maximise engagement while respecting wellbeing and policy guardrails
- modelling strategy
    - single multi-task DNN shares base layers then branches into heads for click, like, share, dwell-time, skip
    - captures correlations between explicit and implicit signals so sparse labels transfer across tasks
    - optionally add calibration layers per head to align raw scores with probability targets
- features
    - user profile: demographics, device, long-term interests
    - content attributes: creator embeddings, topic tags, media type, freshness
    - interaction context: session time, scroll depth, recent actions with decay weighting
    - social graph signals: friend engagement, mutual groups
- training
    - optimise binary cross-entropy for classification heads, regression loss (MAE/MSE/Huber) for dwell-time
    - handle label imbalance via per-task sampling or loss reweighting; inject regularisation and dropout to stabilise shared trunk
- evaluation & serving
    - offline: precision/recall, ROC-AUC per head; simulate ranking lift via nDCG across blended objectives
    - online: guardrail metrics like time spent, complaint rate, quality scores
    - serving pipeline: retrieval service pulls candidate pool, ranking service applies multi-task model, final rerank enforces diversity, freshness, civic integrity

# 2 GenAI System Design Interview 
## 2.1 Foundations
### 2.1.1 Transformer
- self-attention
	- each element in input sequence can attend to every other element
	- converts each token's input embeddings into 3 vectors
		- query $Q$
		- key $k$
		- value $V$
- attention score uses scaling factor to prevent dot-product blowing up
- softmax function ensures normalised scores (sum to 1)
	- produces weighted sum of the value vectors
	- where weights determined by relevance of each input token (using attention scores)
- multi-head attention 
	- projects $Q, K, V$ into multiple heads instead of a single one
		- each with its own learnable matrices
		- results of different heads are concatenated + linearly transformed using a separate output weight matrix $W_O$
		- allows model to jointly attend to info from different representation subspaces + richer dependencies
	- formula → $MultiHead(Q,K,V) = Concat(h_1, h_2, ...) \cdot W_O$
- while transformers are parallelisable, attention has $O(n^2)$ (quadratic) complexity
	- since attention scores calculated between every pair of tokens in sequence
### 2.1.2 Training large-scale models
- gradient checkpointing 
	- reduce memory usage during model training by saving only a selected subset of activations. During the backward pass, missing activations are recomputed. This reduces memory usage
- Automatic Mixed Precision (AMP)
	- 
## 2.2 Parallelism
- pipeline parallelism (PP)
	- slices the network by depth so micro-batches stream through stages; cuts idle time on very deep stacks but needs careful scheduling
- tensor parallelism (TP)
	- partitions individual matrix multiplies across devices; vital when a single layer exceeds device memory yet demands fast all-reduce
## 2.3 Sampling
- deterministic decoding
	- greedy search picks the argmax token each step → fastest but lowest diversity
	- beam search tracks top-k hypotheses to improve coherence, at the cost of computation + remaining conservatively repetitive
- stochastic decoding
	- top-k sampling restricts draws to the k most likely tokens to balance randomness vs fluency
	- top-p (nucleus) sampling accumulates probability mass ≥ p so token set adapts to distribution shape, boosting adaptability for open-ended prompts
## 2.4 Evaluation
- offline evaluation
	- discriminative tasks: precision/recall/F1, accuracy, confusion matrix, MSE/MAE/RMSE, MRR/nDCG/mAP for ranking
	- generative tasks: perplexity, BLEU, ROUGE, METEOR, CIDEr, FID, IS, KID, LPIPS, FVD depending on modality
- online evaluation
	- production guardrails: CTR, conversion rate, engagement, latency, revenue per user, churn, retention, satisfaction, completion rate
	- monitor generative safety alongside quality to avoid silent regressions

## 2.5 Gmail Smart Compose
  - purpose → accelerate drafting by suggesting the next few words as users type inside Gmail
  - system pipeline
      - trigger service watches for compose-context signals (cursor moves into body, user begins typing)
      - phrase generator runs beam search over the transformer decoder, filters out long or low-confidence completions, and enforces product heuristics
      - post-processing cleans punctuation, applies safety/policy filters, then surfaces the suggestion with accept/ignore affordances
  - positional encodings
      - sin–cosine encodings add no parameters and extrapolate to longer sequences yet may underfit positional nuance
      - learned encodings optimise positional cues for Gmail traffic but introduce extra parameters and risk poorer generalisation
  - transformer stack
      - encoder blocks pair multi-head self-attention with feed-forward layers; cross-entropy loss trains next-token prediction on historical emails
      - inference leans on beam search to maintain coherent phrasing while staying responsive
  - evaluation focus
      - offline: perplexity for next-token accuracy, ExactMatch@N to gauge top-N coverage vs ground truth completions
      - online: observe suggestion acceptance, engagement lift, latency budgets, error fallbacks for safety handling

## 2.6 Google Translate
  - purpose → deliver accurate, fluent sentence-level translation across language pairs
  - encoder–decoder architecture
      - encoder embeds source tokens, adds positional signals, and applies stacked self-attention to capture whole-sentence context
      - decoder consumes shifted target tokens, combines masked self-attention with cross-attention over encoder outputs, and projects to vocabulary probabilities
      - cross-attention ensures every generated token can reference the full source sentence, enabling faithful translations
  - training regimen
      - masked language modelling pretraining avoids information leakage found in naive next-token pretraining for encoder–decoder setups
      - decoder input is right-shifted with a start token; cross-entropy loss covers each target position
      - supervised fine-tuning on parallel corpora, then beam search decoding for accuracy/coherence balance
  - evaluation
      - offline: BLEU (n-gram precision + brevity penalty), ROUGE (recall-oriented n-grams), METEOR (weighted harmonic mean with synonym/semantic matching)
      - online: user engagement, explicit feedback, complaint volume across locales

## 2.7 ChatGPT Personal Assistant
  - purpose → provide conversational assistance while staying on-brand, safe, and aligned with user intent
  - positional encodings
      - relative encodings represent token distance to capture order-invariant reasoning
      - rotary positional encodings (RoPE) rotate embeddings for translation invariance and robust extrapolation to longer contexts
  - training pipeline
      - pretraining on large corpora establishes broad language modelling ability
      - supervised fine-tuning (SFT) reformulates prompts/responses into dialogue format
      - RLHF trains a reward model with human preference rankings, then applies PPO/DPO to optimise the SFT policy under reward while maintaining stability via clipping/margins
  - decoding controls
      - temperature rescales logits to tune randomness vs determinism
      - repetition penalty discourages overused phrases to improve variation
  - production pipeline
      - training stack: pretrain → SFT → RLHF with staged safety reviews
      - inference stack: safety filtering + prompt enhancer → candidate response generator → safety evaluator for outputs → rejection response generator that explains refusals → session manager for
  conversation memory

## 2.8 Image Captioning (Image2Text)
  - purpose → describe images with accurate, fluent natural-language captions
  - encoder choices
      - CNN encoders produce 3×3×C feature grids that are flattened to sequences for the decoder; strong local pattern capture but weaker global relationships
      - transformer encoders patchify images, append positional encodings (1D or 2D, fixed or learned), and leverage self-attention for both local and global context
  - attention rationale
      - attention enables the decoder to focus on salient regions per token generation, improving descriptive relevance
  - training + inference
      - supervised fine-tuning on hundreds of millions of image–caption pairs with cross-entropy loss for next-token prediction
      - beam search inference balances fluency and coverage
  - evaluation + system operations
      - CIDEr uses TF–IDF weighted consensus across reference captions, offering robustness to paraphrasing
      - system pipeline: image preprocessing → caption generator with beam search → post-processing for fairness and inclusivity checks

## 2.9 Retrieval-Augmented Generation (RAG)
  - purpose → ground LLM answers in enterprise knowledge by fusing retrieval and generation
  - ingestion + indexing
      - document parsing handles OCR for PDFs, tables, and diagrams
      - chunking strategies include length-based (RecursiveCharacterTextSplitter), regex/semantic boundaries, and code-aware splitting (PythonCodeTextSplitter)
      - indexing options: vector stores for semantic matching, knowledge graphs for relational queries
  - retrieval architecture
      - shared embedding space via text encoder + image encoder (CLIP) supports cross-modal retrieval; RAFT fine-tunes models to down-weight irrelevant docs
      - ANN techniques: tree partitioning, LSH hashing, clustering (two-stage coarse-to-fine), and graph-based HNSW for low-latency recall
  - generation workflow
      - query expansion refines intent before retrieval
      - prompt engineering (chain-of-thought, few-shot, role conditioning) steers grounded answers; top-p sampling balances coherence and diversity
  - evaluation
      - context relevance: hit rate, MRR, nDCG, Precision@k
      - faithfulness: human review, automated fact-checking, consistency checks
      - answer quality: BLEU, ROUGE, METEOR vs references; monitor hallucination rates





