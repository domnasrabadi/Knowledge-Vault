---
type: chapter
status: structured
quality:
topics: [prompting, ai-agents]
source: ""
created: 2025-03-11
published:
author: ""
flashcards: none
updated: 2025-03-13
---
- [[#1 Text Classification|1 Text Classification]]
	- [[#1 Text Classification#1.1 Classification Evals|1.1 Classification Evals]]
	- [[#1 Text Classification#1.2 Task Specific Classification|1.2 Task Specific Classification]]
	- [[#1 Text Classification#1.3 Classification w Embeddings|1.3 Classification w Embeddings]]
	- [[#1 Text Classification#1.4 Lacking Labelled Data|1.4 Lacking Labelled Data]]
	- [[#1 Text Classification#1.5 Classification w LLMs|1.5 Classification w LLMs]]
		- [[#1.5 Classification w LLMs#1.5.1 Encoder-Decoder|1.5.1 Encoder-Decoder]]
		- [[#1.5 Classification w LLMs#1.5.2 Decoder-only|1.5.2 Decoder-only]]
- [[#2 Text Clustering & Topic Modelling|2 Text Clustering & Topic Modelling]]
	- [[#2 Text Clustering & Topic Modelling#2.1 Topic Modelling|2.1 Topic Modelling]]
	- [[#2 Text Clustering & Topic Modelling#2.2 BERTopic|2.2 BERTopic]]
	- [[#2 Text Clustering & Topic Modelling#2.3 Better Representation Models|2.3 Better Representation Models]]
- [[#3 Prompt Engineering|3 Prompt Engineering]]
	- [[#3 Prompt Engineering#3.1 Understanding the Chat/Prompt Template|3.1 Understanding the Chat/Prompt Template]]
	- [[#3 Prompt Engineering#3.2 Controlling Output|3.2 Controlling Output]]
	- [[#3 Prompt Engineering#3.3 Aspects of a Prompt|3.3 Aspects of a Prompt]]
	- [[#3 Prompt Engineering#3.4 Advanced Prompt Engineering|3.4 Advanced Prompt Engineering]]
	- [[#3 Prompt Engineering#3.5 Reasoning|3.5 Reasoning]]
	- [[#3 Prompt Engineering#3.6 Output Verification|3.6 Output Verification]]
- [[#4 Advanced Text Generation & Tools|4 Advanced Text Generation & Tools]]
	- [[#4 Advanced Text Generation & Tools#4.1 Model I/O|4.1 Model I/O]]
	- [[#4 Advanced Text Generation & Tools#4.2 Chains|4.2 Chains]]
	- [[#4 Advanced Text Generation & Tools#4.3 Memory|4.3 Memory]]
	- [[#4 Advanced Text Generation & Tools#4.4 Agents|4.4 Agents]]
- [[#5 Semantic Search & RAG|5 Semantic Search & RAG]]
	- [[#5 Semantic Search & RAG#5.1 Dense Retrieval|5.1 Dense Retrieval]]
		- [[#5.1 Dense Retrieval#5.1.1 Caveats of Dense Retrieval|5.1.1 Caveats of Dense Retrieval]]
		- [[#5.1 Dense Retrieval#5.1.2 Chunking|5.1.2 Chunking]]
		- [[#5.1 Dense Retrieval#5.1.3 ANN Search, Vector DBs, Finetuning|5.1.3 ANN Search, Vector DBs, Finetuning]]
	- [[#5 Semantic Search & RAG#5.2 Reranking|5.2 Reranking]]
	- [[#5 Semantic Search & RAG#5.3 RAG|5.3 RAG]]
		- [[#5.3 RAG#5.3.1 Advanced RAG techniques|5.3.1 Advanced RAG techniques]]
	- [[#5 Semantic Search & RAG#5.4 Retrieval and RAG Evaluation|5.4 Retrieval and RAG Evaluation]]

# 1 Text Classification
- classification goal = train model to assign label or task to some input text 
	- can be applied to both encoder (representation) models or decoder (generative) models

![[Screenshot 2025-03-11 at 3.43.34 pm.webp| center | 400]]

- further, you can use them for classification in 2 ways
	- performing classification directly via classifier head
	- create embeddings and use them as features for another classification model e.g. logistic regression
## 1.1 Classification Evals 
- <mark style="background: #FFB8EBA6;">confusion matrix</mark> = describes 4 types (in binary case) of predictions we can make 
	- <span style="color:rgb(255, 0, 247)">precision</span> = accuracy of the positive labels
		- when the classifier predicts a given class, precision tells you how often it is right
	- <span style="color:rgb(255, 0, 247)">recall</span> = ability to find all positive labels
		- how well the classifier identifies all instances of the class
	- <span style="color:rgb(255, 0, 247)">accuracy</span> = how many correct preds out of all preds
		- $(TP + TN) / \text{num instances}$ 
		- <span style="color:rgb(255, 0, 247)">support</span> = number of actual instances (ground truth) of that class in the dataset
	- <span style="color:rgb(255, 0, 247)">F1 score</span> = balances precision + recall, overall model performance  
		- harmonic mean of precision and recall, especially useful for imbalanced problems 

![[Screenshot 2025-03-11 at 3.48.36 pm.webp| center | 500]]

- using `{python}sklearn.metrics.classification_report` shows some extra fields
	- <mark style="background: #FFB8EBA6;">macro average</mark> = unweighted avg of precision, recall + F1 scores for all instances
		- each class given equal weight regardless of support 
		- e.g. 2 classes with precision scores 0.76 and 0.86 - the macro avg precision = $(0.76 + 0.86)/2$ 
	- <mark style="background: #FFB8EBA6;">weighted average</mark> = takes into account the support for each class 
		- **weights precision, recall, F1 scores by number of instances in each class**
		- most useful for imbalanced problems, gives more importance to classes w more examples

![[Screenshot 2025-03-11 at 3.53.42 pm.webp| center | 600]]

## 1.2 Task Specific Classification 
- most BERT based models are intended to be finetuned on a downstream task
	- common examples include 
		- BERT Base (uncased)
		- RoBERTa base
		- DistilBERT base (uncased)
		- DeBERTa base
		- bert-tiny
		- ALBERT base v2
	- for choosing embedding models, you should look at MTEB leaderboard 
- actually involves finetuning the BERT model with the new classifier head 
- (useful for comparing all approaches at the end) using BERT model on the IMDB data gives us: 
	- F1 weighted avg = 0.80
## 1.3 Classification w Embeddings
- if we cannot finetune the encoder/representation model ourselves, we can leverage pretrained embeddings 
	- embedding model generates features → classifier uses these to predict class
	- much cheaper computationally - just train simple logistic regression or other ML model 
		- can even use an API for embeddings 
- using this approach gives us a weighted average F1 = 0.85
## 1.4 Lacking Labelled Data 
- <mark style="background: #FFB8EBA6;">zero-shot classification</mark> = we know the definitions of labels (their names) but no labelled data to support it 
	- use a model to classify relationship between input to candidate labels 
- e.g. for classifying movie reviews into positive and negative
	- 1. can embed all examples
	- 2. can then use a trick and embed label inputs 
		- e.g. "A Negative Review" and "A Positive Review"
		- i.e. first giving the labels a description which we then embed via embedding model 
	- 3. then apply cosine similarity between all doc-label pairs
		- take most similar label as the prediction class 
- this gets weighted average F1 = 0.78
	- with no labelled data at all!

![[Screenshot 2025-03-11 at 4.12.30 pm.webp| center | 400]]

## 1.5 Classification w LLMs 
- encoder models can be finetuned to become sequence-to-vector models 
	- e.g. take sequence/text input, output single value or vector of possible values
- generative models are instead sequence-to-sequence models 
	- **but can achieve desired result of classification via prompt engineering** 
	- can also use structured outputs e.g. constraining logits to pick from predetermined classes + specifying format in the prompt 
		- e.g. JSON outputs, `outlines` package
### 1.5.1 Encoder-Decoder
- encoder-decoder (OG Transformer) architecture can also be used
	- e.g. T5 architecture - has 2 step training approach
		- **phase 1** = pretrained with MLM, but masks sets of tokens (<span style="color:rgb(255, 0, 247)">token spans</span>) instead of individual tokens
		- **phase 2** = finetuning for many tasks which are all converted to seq2seq format + trained simultaneously 
			- where the magic happens
	- this method was introduced in 2022 paper "Scaling Instruction-Finetuned Language Models"
		- introduced more than 1000 tasks in text-to-text format 
	- using this approach we achieve 0.84 weighted average F1
### 1.5.2 Decoder-only
- GPT models benefit from preference tuning - allow us to capture nuance from instruction data + preference tuning 
	- similar to above, we can prompt engineer to give us the desire classification output 
	- achieves 0.91 F1 !

---
# 2 Text Clustering & Topic Modelling 
- <mark style="background: #FFB8EBA6;">text clustering</mark> = aims to group similar texts based on semantic content, meaning, relationships
	- **helps facilitate efficient categorisation of large volumes of unstructured text** 
	- other objectives + benefits
		- allows for quick EDA
		- finding outliers
		- speedup labelling
		- finding incorrectly labelled data 
- common 3 step pipeline for text clustering
	- 1. **embed documents** w <span style="color:rgb(255, 136, 0)">embedding model</span> 
		- can experiment with many different embedding models in this step 
			- these become the features we eventually cluster 
	- 2. **reduce dimensionality** w <span style="color:rgb(255, 136, 0)">UMAP/PCA</span>
		- as # dimensions increases, exponential growth in # possible values within each dimension
			- finding all subspaces within each dimension becomes too complex
		- clustering techniques often struggle w high dimensional data 
			- can reduce dimensionality = aims to preserve global structure by finding low-dimensional representations 
	- 3. **cluster & find groups of similar documents** w <span style="color:rgb(255, 136, 0)">HDBScan, K-Means</span> etc 
		- density based algorithms don't restrict data points to a clusters, allow for outliers

![[Screenshot 2025-03-11 at 4.32.19 pm.webp| center | 900]]


```python
# STEP 1
from sentence_transformers import SentenceTransformer
# Create an embedding for each abstract
embedding_model = SentenceTransformer("thenlper/gte-small")
embeddings = embedding_model.encode(abstracts, show_progress_bar=True)

# STEP 2
from umap import UMAP
# We reduce the input embeddings from 384 dimensions to 5 dimensions
umap_model = UMAP(
	n_components=5, min_dist=0.0, metric='cosine', random_state=42
)
reduced_embeddings = umap_model.fit_transform(embeddings)

# STEP 3
from hdbscan import HDBSCAN
hdbscan_model = HDBSCAN(
	min_cluster_size=50, metric="euclidean", cluster_selection_method="eom"
).fit(reduced_embeddings)
clusters = hdbscan_model.labels_

# How many clusters did we generate?
len(set(clusters))
# 156
```


![[Screenshot 2025-03-11 at 4.39.57 pm.webp| center | 400]]

 
- UMAP + HDBScan in depth 
	- <mark style="background: #FFB8EBA6;">UMAP</mark> has some hyperparams you generally want to experiment w 
		- `n_components` = shape of the lower dimensional space, generally 5-10 works well
		- `min_dist` = min distance between embedded points 
			- setting to 0 gives tighter clusters 
		- `metric` = usually use cosine - euclidean based metrics struggle in higher dimensions
		- `random_state` = allows for reproducibility using a seed, but disable parallelism 
	- <mark style="background: #FFB8EBA6;">HDBSCAN</mark> = hierarchical variation of DBSCAN
		- DBSCAN allows for dense micro-clusters to be found w/o explicitly specifying number of clusters
			- also allows for outliers to be detected i.e. no assigned cluster
		- `min_cluster_size` = minimum size (number of instances) a cluster can take
			- reducing this creates more clusters
- you should always inspect + analyse your clusters after cluster analysis 
	- visualising them via interactive plots + colouring is very helpful 
## 2.1 Topic Modelling
- <mark style="background: #FFB8EBA6;">topic modelling</mark> = finding themes/latent topics in a collection of textual data
	- often involves finding set of keywords/phrases that best represent each topic
- <mark style="background: #FFB8EBA6;">representation</mark> = keywords/phrases to describe a topic 
	- can be keywords, bi-grams, labels, descriptions etc 
	- user should be able to understand the meaning of the topic through the representation 
	- classical approaches e.g. Latent Dirichlet Allocation (LDA) assume topics to be characterised by probability distribution of vocabulary words

![[Screenshot 2025-03-11 at 4.38.05 pm.webp| center | 400]]

## 2.2 BERTopic
- <mark style="background: #FFB8EBA6;">BERTopic</mark> = modular topic modelling framework using the 2 phases
	- 1. follows text clustering procedure as above (embed, reduce dim, cluster)
	- 2. models distribution over words in corpus vocab with a representation model
		- e.g. Bag of Words, c-TF-IDF 
- <mark style="background: #FFB8EBA6;">class-based term-frequency</mark> (c-TF) = frequency of words calculated within the cluster 
	- as opposed to bag of words which does it at document level 
	- c-TF-IDF is a class based variant of term-frequency inverse-doc-frequency
		- puts more weight on words more meaningful to a cluster
		- less weight on words used across all clusters 
	- each word $\text{c-TF}$ multiplied by the $\text{IDF}$ value of each word 
		- $\text{IDF} = \log (\frac{\text{average frequency}}{CF_x} + 1)$ 
			- log of the average frequency of all words across all clusters
			- divided by $CF_x$ = total frequency of a given word
	- result is a weight (IDF) for each word, we multiply their frequency (c-TF) to get weighted values (c-TF-IDF)

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-11 at 5.01.06 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-11 at 5.00.57 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 2">
</div>

- we use `{python}sklearn.CountVectorizer` to calculate the bag-of-words (TF)
	- which we then use to calculate the c-TF-IDF for topic representations 
- major advantage here is the 2 steps are largely independent of each other
	- step 1: clustering vs step 2: topic representation 
	- so we can try many combinations for each component 

![[Screenshot 2025-03-11 at 5.03.56 pm.webp| center | 500]]

- types of topic modelling supported in BERTopic 

| **Type**                              | **Description**                                                                                           | **When to Use**                                                                                         |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Guided Topic Modeling                 | Uses seed words or domain knowledge to steer topic discovery.                                             | When you have prior knowledge or want topics aligned with specific concepts.                            |
| (Semi-)Supervised Topic Modeling      | Incorporates labeled data to improve topic coherence or steer the model.                                  | When you have some labeled documents and need topics that align with pre-defined categories.            |
| Hierarchical Topic Modeling           | Produces a nested structure of topics (topics and subtopics).                                             | For in-depth analysis where you need to understand broad topics as well as finer subtopics.             |
| Dynamic Topic Modeling                | Captures how topics evolve over time.                                                                     | When analyzing time-series data, such as trends in news articles or social media.                       |
| Multimodal Topic Modeling             | Integrates multiple data types (e.g., text combined with images or metadata) into topic discovery.        | In applications where text is accompanied by other data forms, enhancing context and insights.          |
| Multi-Aspect Topic Modeling           | Discerns multiple dimensions or aspects within the data, often reflecting different facets of a document. | When documents are complex and you want to capture varied perspectives or aspects in a single document. |
| Online and Incremental Topic Modeling | Updates topics continuously as new data arrives, without retraining from scratch.                         | For streaming data or evolving datasets where real-time topic updates are needed.                       |
| Zero-Shot Topic Modeling              | Leverages pre-trained language models to assign topics without any fine-tuning or additional training.    | When you need to quickly infer topics on new data without a domain-specific training phase.             |

- using `bertopic` in python 
	- anything under topic `-1` is an outlier 
	- `{python}topic_model.get_topic_info()` = quick description of detected topics 
	- `{python}topic_model.get_topic(0)` = explore single topic keywords
	- `{python}topic_model.find_topics("attention")` = searches for specific topics based on search term
		- returns topic ids + their similarity to the search term

```python
from bertopic import BERTopic

topic_model = BERTopic(
	embedding_model=embedding_model,
	umap_model=umap_model,
	hdbscan_model=hdbscan_model,
	verbose=True
).fit(abstracts, embeddings)

topic_model.get_topic_info()
# Topic Count  Name                                   Representation
# -1    14520  -1_the_of_and_to                       [the, of, and, to, in, we, that, language, for...
# 0     2290   0_speech_asr_recognition_end           [speech, asr, recognition, end, acoustic, spea...
# 1     1403   1_medical_clinical_biomedical_patient  [medical, clinical, biomedical, patient, healt...
# 2     1156   2_sentiment_aspect_analysis_reviews    [sentiment, aspect, analysis, reviews, opinion...
...

topic_model.get_topic(0)
# [('speech', 0.028177697715245358),
#  ('asr', 0.018971184497453525),
#  ('recognition', 0.013457745472471012),
#  ('end', 0.00980445092749381),
...

topic_model.find_topics("attention")
# ([22, -1, 1, 47, 32],
 # [0.95456535, 0.91173744, 0.9074769, 0.9067007, 0.90510106])
```

- calling `{python}topic_model.visualize_documents()` gives you an interactive 2d scatter plot of topic distribution 
	- many more visualisations available 

```python
# Visualize topics and documents
fig = topic_model.visualize_documents(
	titles,
	reduced_embeddings=reduced_embeddings,
	width=1200, hide_annotations=True
)
fig.update_layout(font=dict(size=16)) # update legend font 

# Visualize barchart with ranked keywords
topic_model.visualize_barchart()
# Visualize relationships between topics
topic_model.visualize_heatmap(n_clusters=30)
# Visualize the potential hierarchical structure of topics
topic_model.visualize_hierarchy()
```

## 2.3 Better Representation Models 
- drawback of c-TF-IDF approach = redundancy in similar words e.g. "Summarisation", "Summaries", "Summary"
	- can tweak it using embedding models to re-rank and improve the representation 
	- re-ranker models also known as representation models 

![[Screenshot 2025-03-11 at 5.24.35 pm.webp| center | 500]]

- you can stack + experiment w many different representation blocks 
	- many of which are LLMs
- <span style="color:rgb(255, 136, 0)">c-TF-IDF</span> = default representation method in BERTopic
- <span style="color:rgb(255, 136, 0)">Maximal Marginal Relevance</span> (<span style="color:rgb(255, 136, 0)">MMR</span>) = balances keyword relevance with diversity
	- generates candidate keywords (using above), reorders them to reduce redundancy 
		- requires setting diversity hyperparameter - how diverse keywords need to be 
	- improves topic coherence + reduces overlap of keywords in a topic
	- generally gives the best combined with LLMs

```python
from bertopic.representation import MaximalMarginalRelevance

# Update our topic representations to MaximalMarginalRelevance
representation_model = MaximalMarginalRelevance(diversity=0.2)
topic_model.update_topics(abstracts, representation_model=representation_model)

# Show topic differences
topic_differences(topic_model, original_topics)
```

- <span style="color:rgb(255, 136, 0)">KeyBERT</span> = extracts keywords by comparing word + doc embeddings via cosine similarity 
	- find most representative docs per topic - via similarity between c-TF-IDF for docs vs topics 
	- typically removes all stop words 

![[Screenshot 2025-03-12 at 8.40.00 am.webp| center | 500]]

```python
from bertopic.representation import KeyBERTInspired

# Update our topic representations using KeyBERTInspired
representation_model = KeyBERTInspired()

topic_model.update_topics(abstracts, representation_model=representation_model)

# Show topic differences
topic_differences(topic_model, original_topics)
```

- <span style="color:rgb(255, 136, 0)">spaCy</span> = industrial-strength NLP library that provides fast tokenization, part-of-speech tagging, lemmatisation, and named entity recognition
	- preprocess text data by cleaning, tokenizing, and extracting noun phrases or entities, which can then serve as refined candidates for topic keywords
- <span style="color:rgb(255, 136, 0)">LLMs</span> =  can be applied for zero-shot topic labelling or even to generate summaries and candidate keywords for clusters
	- generate a short label based on keywords that were previously generated and a small set of representative documents
	- **apply it once for every topic** - gives best results often

![[Screenshot 2025-03-12 at 8.44.02 am.webp| center | 500]]

```python
from transformers import pipeline
from bertopic.representation import TextGeneration
from bertopic.representation import OpenAI

prompt = """I have a topic that contains the following documents:
[DOCUMENTS]
The topic is described by the following keywords: '[KEYWORDS]'.
Based on the documents and keywords, what is this topic about?"""

# USING FLAN T5
generator = pipeline("text2text-generation", model="google/flan-t5-small")
representation_model = TextGeneration(generator, prompt=prompt, doc_length=50, tokenizer="whitespace")
topic_model.update_topics(abstracts, representation_model=representation_model)

# USING OAI API 
client = openai.OpenAI(api_key="YOUR_KEY_HERE")
representation_model = OpenAI(
	client, model="gpt-3.5-turbo", exponential_backoff=True, chat=True, prompt=prompt
)
topic_model.update_topics(abstracts, representation_model=representation_model)
```

- once you've chosen representation blocks, can then visualise the final labelled clusters using `datamapplot` package

```python
# Visualize topics and documents
fig = topic_model.visualize_document_datamap(
	titles,
	topics=list(range(20)),
	reduced_embeddings=reduced_embeddings,
	width=1200, label_font_size=11, label_wrap_width=20,
	use_medoids=True,
)
```

![[Screenshot 2025-03-12 at 8.48.34 am.webp| center | 400]]

---
# 3 Prompt Engineering
## 3.1 Understanding the Chat/Prompt Template
- recall, `{python}transformers.pipeline()` encapsulates both model and tokenizer functions
	- first converts our messages to a specific prompt template - can be access like below
	- useful to understand the special tokens added e.g. `<|user|>`, `<|assistant|>`

```python
prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False)    # Apply prompt template
print(prompt)
# <s><|user|>
# Create a funny joke about chickens.<|end|>
# <|assistant|>
```

![[Screenshot 2025-03-12 at 9.03.41 am.webp| center | 500]]

## 3.2 Controlling Output
- several options available to us to control the diversity of outputs from the model 
- `temperature` = controls randomness (and hence creativity) of generations
	- defines how likely to choose tokens that are less probable - lower temps e.g. 0.2, while higher temps usually between 0.8 to 1.2
		- higher temperature increases the likelihood that less probable tokens are generated and vice versa
	- can use in pipeline : `{python}output = pipe(messages, do_sample=True, temperature=1)`
- `top_p` (<span style="color:rgb(255, 0, 247)">nucleus sampling</span>) = controls subset of tokens (the nucleus) the LLM can consider
	- considers tokens until it reaches their cumulative probability e.g. `top_p = 1` considers all tokens, `top_p = 0.1` considers the top 10% 
	- can use in pipeline `{python}output = pipe(messages, do_sample=True, top_p=1)`
- `top_k` = similar to top_p but controls exactly how many tokens to consider (instead of cum. prob)
	- e.g. `top_p = 100` considers top 100 most probable tokens

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-12 at 9.14.10 am.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-12 at 9.14.21 am.webp" style="width: 48%; object-fit: contain;" alt="Image 2">
</div>

- some use cases for choose both `temperature` & `top_p` values

| Temperature | Top P | Effect                                                                                |
| ----------- | ----- | ------------------------------------------------------------------------------------- |
| High        | High  | high randomness w large pool of potential tokens, very diverse + creative outputs     |
| Low         | Low   | deterministic output w high probable predicted tokens, conservative outputs           |
| High        | Low   | high randomness w small pool of potential tokens, creative but coherent outputs       |
| Low         | High  | deterministic output w high probable predicted tokens, coherent outputs w wider vocab |

## 3.3 Aspects of a Prompt
- instruction based prompting - to get the LLM to answer a specific question or resolve specific task
	- e.g. supervised classification, search, summarisation, code generation, NER
	- **each task requires different prompting format** i.e. different questions to ask the LLM
- some techniques shared across instruction types
	- <span style="color:rgb(255, 136, 0)">specificity</span> = accurately describe what you want to achieve, arguably most important to include 
	- <span style="color:rgb(255, 136, 0)">hallucination</span> = ask LLM to generate answer only if it knows, otherwise respond with "I don't know"
	- <span style="color:rgb(255, 136, 0)">order</span> = begin or end your prompt with the instruction 
		- especially for long prompts, info in the middle often forgotten 

![[Screenshot 2025-03-12 at 9.31.44 am.webp| center | 500]]

## 3.4 Advanced Prompt Engineering
- prompting can grow complex quite quickly - often underestimated component to using LLMs
	- below shows modular nature of prompting 
	- make sure to experiment with ablations by adding/removing components and judging effect on output 
- prompts generally consist of several components 
	- <span style="color:rgb(255, 136, 0)">persona</span> = role LLM should take on 
	- <span style="color:rgb(255, 136, 0)">instruction</span> = task itself, be as specific as possible, don't leave room for interpretation 
	- <span style="color:rgb(255, 136, 0)">context</span> = additional info describing problem context e.g. reason for the instruction
	- <span style="color:rgb(255, 136, 0)">format</span> = output format LLM should give
	- <span style="color:rgb(255, 136, 0)">audience</span> = target of the generated text 
	- <span style="color:rgb(255, 136, 0)">tone</span> = tone of voice should use
	- <span style="color:rgb(255, 136, 0)">data</span> = main data related to the task itself 

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-13 at 1.44.32 pm.webp" style="width: 50%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-13 at 1.44.42 pm.webp" style="width: 45%; object-fit: contain;" alt="Image 2">
</div>

```python
# Prompt components
persona = "You are an expert in Large Language models. You excel at breaking down complex papers into digestible summaries.\n"

instruction = "Summarize the key findings of the paper provided.\n"

context = "Your summary should extract the most crucial points that can help researchers quickly understand the most vital information of the paper.\n"

data_format = "Create a bullet-point summary that outlines the method. Follow this up with a concise paragraph that encapsulates the main results.\n"

audience = "The summary is designed for busy researchers that quickly need to grasp the newest trends in Large Language Models.\n"

tone = "The tone should be professional and clear.\n"

text = "MY TEXT TO SUMMARIZE"

data = f"Text to summarize: {text}"
# The full prompt - remove and add pieces to view its impact on the generated output
query = persona + instruction + context + data_format + audience + tone + data
```

- ICL = providing examples in the prompt 
	- Zero-shot = no examples, Single/One-shot = single example, Few-shot = several examples
- <mark style="background: #FFB8EBA6;">chain of prompting</mark> = take output of one prompt, use as input for next 
	- creating continuous chain of interactions to solve the problem 
	- allows more time to be spent on each individual question instead of tackling entire problem at once 

![[Screenshot 2025-03-13 at 1.47.07 pm.webp| center | 400]]

- benefits of chain-prompting, and use-cases
	- can give each call different parameters e.g. one section can be short + exact, another long and descriptive
	- <span style="color:rgb(255, 136, 0)">response validation</span> = double check previously generated outputs 
	- <span style="color:rgb(255, 136, 0)">parallel prompts</span> = multiple prompts in parallel, final pass to merge them 
	- <span style="color:rgb(255, 136, 0)">writing stories/reports</span> = breaking down problem into components
## 3.5 Reasoning 
- reasoning methods analogous to system 1 and 2 thinking (from *Thinking Fast and Slow*)
	- <span style="color:rgb(255, 136, 0)">system 1 thinking</span> = automatic, intuitive, fast process e.g. generating tokens w/o any self-reflective behaviour
	- <span style="color:rgb(255, 136, 0)">system 2 thinking</span> = conscious, slow and logical process e.g. brainstorming and self-reflection
- <mark style="background: #FFB8EBA6;">chain-of-thought</mark> (<span style="color:rgb(255, 0, 247)">CoT</span>) = model **prompted to think through the problem before answering** 
	- reasoning tokens referred to as thoughts, each additional reasoning token allows LLM to stabilise outputs
	- to prime the LLM for CoT, we add phrases like `"Let's think step-by-step"`
		- or `"Take a deep breath and think step by step"`, `"Let's work this problem through step by step"`
	- also try to add reasoning examples in the prompt

![[Screenshot 2025-03-13 at 1.47.37 pm.webp| center | 500]]

- <mark style="background: #FFB8EBA6;">self-consistency</mark> = **ask LLM same prompt multiple times, take majority result as final answer**
	- allows for diversity if you use different params e.g. temp or top p 
	- however does require $n$ model calls - then collect all samples 

![[Screenshot 2025-03-13 at 1.49.56 pm.webp| center | 400]]

- <mark style="background: #FFB8EBA6;">tree-of-thought</mark> (<span style="color:rgb(255, 0, 247)">ToT</span>) = improves on CoT + self-consistency, allowing it to **expand to further in-depth exploration of several ideas**
	- process:
		- given a problem requiring multiple reasoning steps, model breaks it down to pieces
		- at each step, model is prompted to explore different solutions
		- then votes for best solution + continues to next step 
	- very useful when needing to consider multiple paths
		- however requires many calls to the LLM 

![[Screenshot 2025-03-13 at 1.50.30 pm.webp| center | 400]]

- improved approach to ToT = converts ToT framework into single prompting technique 
	- instead of multiple calls, ask LLM to mimic the behaviour by emulating conversation between multiple experts
	- experts question each other until reaching consensus

```python
# Zero-shot tree-of-thought
zeroshot_tot_prompt = [{
	"role": "user", 
	"content": """Imagine three different experts are answering this question. All experts will write down 1 step of their thinking, then share it with the group. Then all experts will go on to the next step, etc. If any expert realizes they're wrong at any point then they leave. The question is 'The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?' Make sure to discuss the results."""
}]
outputs = pipe(zeroshot_tot_prompt) 
print(outputs[0]["generated_text"])
# Expert 1: Step 1 - Start with the initial number of apples: 23 apples.
# Expert 2: Step 1 - Subtract the apples used for lunch: 23 - 20 = 3 apples remaining.
# Expert 3: Step 1 - Add the newly bought apples: 3 + 6 = 9 apples.
# Expert 1: Step 2 - Confirm the final count: The cafeteria has 9 apples.
# Expert 2: Step 2 - Review the calculations: 23 - 20 = 3, then 3 + 6 = 9. The calculations are correct.
# Expert 3: Step 2 - Agree with the result: The cafeteria indeed has 9 apples.
# All experts agree on the final count: The cafeteria has 9 apples.
```

## 3.6 Output Verification 
- important to verify + control output of model for downstream use + robustness
- reasons for validating outputs:
	- <span style="color:rgb(255, 136, 0)">structured outputs</span> - for structured formats like JSON
	- <span style="color:rgb(255, 136, 0)">valid outputs</span> - e.g. classifying into valid classes 
	- <span style="color:rgb(255, 136, 0)">ethics</span> - to consider safety/ethical considerations, especially when no guardrails used
	- <span style="color:rgb(255, 136, 0)">accuracy</span> - adhere to certain standards or performance e.g. factuality
- 3 ways to control output of LLMs
	- <span style="color:rgb(255, 0, 247)">examples</span> =  **provide number of examples of expected output**
		- e.g. few-shot learning, can also generalise this method to guide output structure 
	- <span style="color:rgb(255, 0, 247)">grammar</span> = **control the token selection process**
		- aka constrained sampling, packages have been developed to constrain + validate outputs e.g. `guidance`, `guardrails.ai`, `LMQL`, `outlines`
		- can use a template for LLM to fill out, rather than fully generating it 
		- can use judge LLM to validate the output structure
		- can use token validation when sampling by **defining grammars or rules LLM needs to adhere to in sampling**
			- e.g. `llama-cpp-python` allows for JSON grammar
	- <span style="color:rgb(255, 0, 247)">fine-tuning</span> =  **tune a model on data of expected outputs**
		- finetuning with many examples of expected behaviour, most costly + intensive 

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-13 at 1.53.20 pm.webp" style="width: 47%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-13 at 1.53.29 pm.webp" style="width: 47%; object-fit: contain;" alt="Image 2">
</div>

- example code for llama.cpp grammars
	- to use internal JSON grammar, only need to specify the `response_format` as "json_object"
		- applies grammars under the hood to adhere to that 
	- can then use `{python}json` library to attempt to process it as such

```python
from llama_cpp.llama import Llama
llm = Llama.from_pretrained(
	repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
	filename="*fp16.gguf",
	n_gpu_layers=-1,
	n_ctx=2048,
	verbose=False
)

# Generate output
output = llm.create_chat_completion(
	messages=[{"role": "user", "content": "Create a warrior for an RPG in JSON format."}],
	response_format={"type": "json_object"},
	temperature=0,
)['choices'][0]['message']["content"]

import json
json_output = json.dumps(json.loads(output), indent=4)      # Format as json
print(json_output)

# {
#  "name": "Eldrin Stormbringer",
#  "class": "Warrior",
#  "level": 10,
#  "attributes": {
# 	 "strength": 18, "dexterity": 12, "constitution": 16, 
# 	 "intelligence": 9, "wisdom": 14, "charisma": 10
#  },
#  "skills": {
# 	 "melee_combat":
# 	 ...
# }
```

---
# 4 Advanced Text Generation & Tools
- 4 methods to improve output quality:
	- Model I/O = loading + working w LLMs
	- Chains = connecting methods + modules
	- Memory = helping LLMs remember
	- Agents = combining complex behaviour w external tools 
- combining all of these techniques can give incredible performance
	- `{python}langchain` integrates all of these methods 
	- newer frameworks also useful e.g. `{python}DSPy`, `{python}Haystack`

![[Screenshot 2025-03-13 at 1.59.06 pm.webp| center | 500]]

## 4.1 Model I/O
- <span style="color:rgb(255, 0, 247)">GGUF format</span> = compressed/quantised version of LLM
	- reduces bits needed to represent LLM params - <span style="color:rgb(255, 0, 247)">bits</span> = series of 0s/1s, representing values encoding them in binary form 
		- more bits = wider range of values, but more memory required to store them
	- quantisation aims to reduce bit representation while trying to maintain most of original info 
		- rule of thumb = look for at least 4-bit quantised models, good balance between compression + accuracy 

```python
from langchain import LlamaCpp
llm = LlamaCpp(...)     # same as before # Make sure the model path is correct for your system!
llm.invoke("Hi! My name is Maarten. What is 1 + 1?")
# ''
```

## 4.2 Chains
- chains are one of LangChain's core functionalities, even named after it 
	- <mark style="background: #FFB8EBA6;">single chain</mark> = most basic form of chain in LangChain, **connects LLM to some tool, prompt or feature** 
		- i.e. connects some modular component (prompt template, external memory etc) to an LLM 
- prompt template - first simple chain, LangChain allows you to create and use prompt templates as a single chain
	- to create first simple chain, need to create prompt template adhering to model's template (Phi-3 in example)

```python
from langchain import PromptTemplate
# Create a prompt template with the "input_prompt" variable
template = """<s><|user|>
{input_prompt}<|end|>
<|assistant|>"""
prompt = PromptTemplate(
	template=template,
	input_variables=["input_prompt"]
)

# create the chain 
basic_chain = prompt | llm
```

- chain w multiple prompts - breaking down complex prompt into smaller subtasks to run sequentially
	- multiple LLM calls but smaller prompts + intermediate outputs 
	- example below creates a story w subtasks - title, description of protagonist, summary 

```python
from langchain import LLMChain
# Create a chain for the title of our story
template = """<s><|user|>
Create a title for a story about {summary}. Only return the title.<|end|>
<|assistant|>"""
title_prompt = PromptTemplate(template=template, input_variables=["summary"])
title = LLMChain(llm=llm, prompt=title_prompt, output_key="title")

title.invoke({"summary": "a girl that lost her mother"})

# Create a chain for the character description using the summary and title
template = """<s><|user|>
Describe the main character of a story about {summary} with the title {title}.
Use only two sentences.<|end|>
<|assistant|>"""
character_prompt = PromptTemplate(
 template=template, input_variables=["summary", "title"]
)
character = LLMChain(llm=llm, prompt=character_prompt, output_key="character")

# Create a chain for the story using the summary, title, and character description
template = """<s><|user|>
Create a story about {summary} with the title {title}. The main character is:
{character}. Only return the story and it cannot be longer than one paragraph.
<|end|>
<|assistant|>"""
story_prompt = PromptTemplate(
 template=template, input_variables=["summary", "title", "character"]
)
story = LLMChain(llm=llm, prompt=story_prompt, output_key="story")

# Combine all three components to create the full chain
llm_chain = title | character | story

llm_chain.invoke("a girl that lost her mother")
# {'summary': 'a girl that lost her mother',
#  'title': ' "In Loving Memory: A Journey Through Grief"',
#  'character': ' The protagonist, Emily, is a resilient young girl who struggles to cope with her 
#   overwhelming grief after losing her beloved and caring mother at an early age. As she 
#   embarks on a journey of self-discovery # and healing, she learns valuable life lessons 
#   from the memories and wisdom shared by those around her.',
# 'story': " In Loving Memory: ..."
```

- can modify and tweak each component as we need 
## 4.3 Memory
- **models are stateless** i.e. no memory of any previous conversation
	- to make models <span style="color:rgb(255, 0, 247)">stateful</span>, can adds types of memory to the chain, 2 common types:
		- conversation buffer 
		- conversation summary 
- <mark style="background: #FFB8EBA6;">conversation buffer</mark> = copying full conversation history + pasting it into our prompt 
	- in LangChain, this memory called a `{python}ConversationBufferMemory`
		- requires us to update previous prompt to hold history of the chat, assigning the `chat_history` to `{python}ConversationBufferMemory`

```python
# Create an updated prompt template to include a chat history
template = """<s><|user|>Current conversation:{chat_history}
{input_prompt}<|end|>
<|assistant|>"""
prompt = PromptTemplate(
	template=template,
	input_variables=["input_prompt", "chat_history"]
)

from langchain.memory import ConversationBufferMemory
# Define the type of memory we will use
memory = ConversationBufferMemory(memory_key="chat_history")
# Chain the LLM, prompt, and memory together
llm_chain = LLMChain(
	prompt=prompt,
	llm=llm,
	memory=memory
)

llm_chain.invoke({"input_prompt": "Hi! My name is Maarten. What is 1 + 1?"})
```

- <span style="color:rgb(255, 0, 247)">windowed conversation buffer</span> = takes sliding window of history, since as context size grows, so does input prompt size (can exceed token limit)
	- involves using last $k$ conversations instead of full chat history 
	- in LangChain, using `{python}ConversationBufferWindowMemory` to decide how many conversations passed to input prompt 

```python
from langchain.memory import ConversationBufferWindowMemory
# Retain only the last 2 conversations in memory
memory = ConversationBufferWindowMemory(k=2, memory_key="chat_history")
# Chain the LLM, prompt, and memory together
llm_chain = LLMChain(
	 prompt=prompt,
	 llm=llm,
	 memory=memory
)
```

- <mark style="background: #FFB8EBA6;">conversation summary</mark> = another method to remedy increasing buffer size but trying to keep concepts discussed earlier 
	- windowed buffer only retains certain amount, however summary is able to distill entire convo to main points 
		- this involves 2 LLM calls - user prompt + summarisation prompt 
		- LangChain function is `{python}ConversationSummaryMemory`
	- can use smaller/cheaper LLM to summarise to help compute
		- after each turn/step, chain will summarise convo up to that point 
	- summarisation helps keep chat history relatively small w/o using too many tokens at inference
		- could also consider this to be form of <span style="color:rgb(255, 0, 247)">query-rewrite</span>

```python
# Create a summary prompt template
summary_prompt_template = """<s><|user|>Summarize the conversations and update with the new lines.

Current summary:
{summary}

new lines of conversation:
{new_lines}

New summary:<|end|>
<|assistant|>"""
summary_prompt = PromptTemplate(
	 input_variables=["new_lines", "summary"],
	 template=summary_prompt_template
)

from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(          # Define the type of memory we will use
	llm=llm,
	memory_key="chat_history",
	prompt=summary_prompt
)
llm_chain = LLMChain(                        # Chain the LLM, prompt, and memory together
	prompt=prompt,
	llm=llm,
	memory=memory
)

# Generate a conversation and ask for the name
llm_chain.invoke({"input_prompt": "Hi! My name is Maarten. What is 1 + 1?"})
llm_chain.invoke({"input_prompt": "What is my name?"})

# {'input_prompt': 'What is my name?',
# 	'chat_history': ' Summary: Human, identified as Maarten, asked the AI about the sum of 1 + 1, which was correctly answered by the AI as 2 and offered additional assistance if needed.',
# 	'text': ' Your name in this context was referred to as "Maarten". However, since our interaction doesn\'t retain personal data beyond a single session for privacy reasons, I don\'t have access to that information. How can I assist you further today?'}

# Check what the summary is thus far 
memory.load_memory_variables({})
```

- tradeoffs between different memory types

| Memory Type                | Pros                                                        | Cons                                                        |
|----------------------------|-------------------------------------------------------------|-------------------------------------------------------------|
| Conversation Buffer         | • Easiest implementation                                     | • Slower generation speed as more tokens are needed         |
|                            | • Ensures no information loss within context window          | • Only suitable for large-context LLMs                      |
|                            |                                                             | • Larger chat histories make information retrieval difficult  |
| Windowed Conversation Buffer | • Large-context LLMs are not needed unless chat history is large | • Only captures the last k interactions                      |
|                            | • No information loss over the last k interactions           | • No compression of the last k interactions                  |
| Conversation Summary        | • Captures the full history                                  | • An additional call is necessary for each interaction       |
|                            | • Enables long conversations                                 | • Quality is reliant on the LLM’s summarization capabilities |
|                            | • Reduces tokens needed to capture full history              |                                                             |

## 4.4 Agents
- <mark style="background: #FFB8EBA6;">agents</mark> = systems that leverage LLM to determine which actions to take + what order
	- agents are extended by <span style="color:rgb(255, 0, 247)">tools</span> (things it needs to do, it cannot do itself), <span style="color:rgb(255, 0, 247)">agent type</span> (plans actions to take or tools to use)
		- e.g. use calculator instead of asking LLM to do the math, use search or weather API etc 
- <mark style="background: #FFB8EBA6;">ReAct</mark> (Reasoning + Acting) = main framework behind most agentic systems
	- ReAct merges reasoning + acting by following 3 iterative steps:
		- 1. <span style="color:rgb(255, 136, 0)">thought</span> - agent describes what it should do 
		- 2. <span style="color:rgb(255, 136, 0)">action</span> - what it will do/chosen to do
		- 3. <span style="color:rgb(255, 136, 0)">observation</span> - results of the actions
	- cycle of thoughts, action, observation give resulting agent outputs

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-13 at 7.43.40 pm.webp" style="width: 50%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-13 at 7.43.57 pm.webp" style="width: 40%; object-fit: contain;" alt="Image 2">
</div>

- ReAct in LangChain can be done using below template 
	- starts with question + generates intermediate thoughts/actions/observations 
	- for tool use, we need to describe the tool library 
	- after creating the ReAct agent, pass it to `{python}AgentExecutor` which handles execution steps 

```python
# Create the ReAct template
react_template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do 
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
prompt = PromptTemplate(
 template=react_template,
 input_variables=["tools", "tool_names", "input", "agent_scratchpad"]
)

from langchain.agents import load_tools, Tool
from langchain.tools import DuckDuckGoSearchResults
# You can create the tool to pass to an agent
search = DuckDuckGoSearchResults()
search_tool = Tool(
	name="duckduck",
	description="A web search engine. Use this to as a search engine for general queries.",
	func=search.run,
)
# Prepare tools
tools = load_tools(["llm-math"], llm=openai_llm)
tools.append(search_tool)

from langchain.agents import AgentExecutor, create_react_agent
# Construct the ReAct agent
agent = create_react_agent(openai_llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
```

![[Screenshot 2025-03-13 at 7.45.58 pm.webp| center | 500]]

- intermediate steps above show how model processes ReAct template + what tools it accesses
	- no human in the loop here to judge output quality or reasoning process
	- agents are double edged swords - need careful design to improve reliability 

---
# 5 Semantic Search & RAG
- months after releasing BERT, Google began using to power search as one of it's biggest advancements
	- <mark style="background: #FFB8EBA6;">semantic search</mark> = ability added by searching by meaning, not just simple keyword matching
- 3 ways to use LLMs for search
	- dense retrieval 
	- reranking
	- RAG
## 5.1 Dense Retrieval
- <mark style="background: #FFB8EBA6;">dense retrieval</mark> = relying on embeddings, turns search problem into nearest neighbour retrieval problem (w.r.t. search query)
	- build process:
		- collect all text you want to search, apply light processing e.g. chunking
		- embed chunks
		- build the search index - optimised for quick retrieval 
	- inference process:
		- embed the user query, project into documents vector space
		- find nearest documents to the query and use as search results
- relies on property that search queries will be close to their relevant results
	- sometimes also desirable to have max threshold of similarity score to filter out irrelevant results 
	- good idea to compare to baseline e.g. text matching algo like BM25 which is competitive 
### 5.1.1 Caveats of Dense Retrieval
- 💡 texts might not contain the answer - can use heuristic of relevance threshold
	- can present results and ask user to decide if it's relevant or not
	- then track results if user clicked on a result (and satisfied by it) for improving model later
- 💡 when user wants exact match for specific phrase
	- perfect use case for keyword matching 
	- consider using <span style="color:rgb(255, 0, 247)">hybrid search</span> here which combines both dense + keyword retrieval 
- 💡 challenging for domains outside of training data 
	- e.g. for niche domains, consider finetuning approaches here 
- 💡 questions which have answers that span multiple sentences or chunks in the documents
	- chunking long text is important design parameter for such retrieval systems (see below)
### 5.1.2 Chunking
- why we need chunking = since very long texts can exceed token limits 
- <span style="color:rgb(255, 136, 0)">one vector per document</span> = single vector to represent entire document text 
	- options:
		- **embed only representative part of doc, ignore the rest**
			- not ideal since leaves out a lot in the index and hence unsearchable 
		- embed document in chunks, embed the chunks, then aggregate chunks into a single vector 
			- **can average to aggregate the vectors but results in highly compressed vector with information loss** 
	- consider how users will interact
		- e.g. they may want specific pieces of info from an article - better if it has it's own vector
- <span style="color:rgb(255, 136, 0)">multiple vectors per document</span> = chunk doc into smaller pieces, the embed the smaller chunks 
	- search index becomes built of chunk embeddings, not doc embeddings
		- better approach since it has full coverage of the text
		- vectors can then capture individual concepts inside the text - more expressive search index
	- options
		- sentence chunks - can be too granular 
		- paragraph chunks - good for text with short paragraphs 
		- contextual chunks - incorporate text around them e.g. title, text before and after
	- consider how you should handle overlapping segments - key to retaining context between segments 

![[Screenshot 2025-03-13 at 7.47.24 pm.webp| center | 500]]

### 5.1.3 ANN Search, Vector DBs, Finetuning
- scaling to many vectors requires optimised retrieval approach 
	- e.g. approximate nearest neighbour search libraries e.g. `annoy`, `faiss`
- can improve performance on retrieval by optimising embedding models
	- need to optimise the text embeddings not just token embeddings 
	- finetuning allows the embeddings to get closer to the embedding of resulting sentences 
## 5.2 Reranking
- <mark style="background: #FFB8EBA6;">reranking</mark> = scoring the relevance of a subset of results against the query, optimising their order based on the scores
	- i.e. changing order of search results based on relevance to search query 
	- can vastly improve performance e.g. Bing used this with BERT 

![[Screenshot 2025-03-13 at 7.48.04 pm.webp| center | 500]]

- example of a reranker w Cohere Rerank
	- takes in search query + number of search results
	- returns optimal ordering of docs so relevant ones to query are higher in ranking
	- <span style="color:rgb(255, 0, 247)">shortlisting</span> = first stage, can use keyword search/dense retrieval or hybrid
	- rerank = second stage
- common to do retrieval + reranking with sentence-transformer models 
	- one approach rerankers use - present query + each result to <mark style="background: #FFB8EBA6;">cross-encoder</mark>
	- i.e. query and possible result presented to model simultaneously allowing model to view both text then assign relevance score
		- all docs processed simultaneously as a batch 
		- but each doc is evaluated against the query independently 
		- scores then determine new order of results (approach known as MonoBERT)
	- essentially a classification problem with 0 (irrelevant) to 1 (very relevant)
## 5.3 RAG
- <mark style="background: #FFB8EBA6;">RAG</mark> = using LLM to respond to query with additional context e.g. can use above steps too 
	- RAG pipelines include search step + grounded generation step 
		- where LLM prompted w question + info retrieved from search step 
	- <span style="color:rgb(255, 0, 247)">grounded generation</span> = since retrieved content provides the LLM with the context needed to answer
- RAG w local models i.e. `llama.cpp`
### 5.3.1 Advanced RAG techniques
- <span style="color:rgb(255, 136, 0)">query rewriting</span> = use LLM to rewrite query to aid retrieval step 
	- can involve expanding, disambiguating, removing redundancy etc 
	- usually done through a prompt 
- <span style="color:rgb(255, 136, 0)">multi-query RAG</span> = extend query rewrite to search multiple queries if > 1 needed to answer a question
	- e.g. "Compare results of NVIDIA between 2020 and 2023"
		- query 1 = "NVIDIA financial results 2020"
		- query 2 = "NVIDIA financial results 2023"
- <span style="color:rgb(255, 136, 0)">multi-hop RAG</span> = advanced questions might need series of sequential queries 
	- e.g. "*Who are biggest car makers in 2023? do they each make EVs or not?*"
		- systems starts by searching "Largest car manufacturers 2023"
		- then should ask follow up questions on each result e.g. 
			- Step 2, Query 1: "Toyota electric vehicles"
			- Step 2, Query 2: "Volkswagen electric vehicles" 
- <span style="color:rgb(255, 136, 0)">query routing</span> = give model ability to search through multiple data sources 
	- i.e. being able to determine and choose between systems/APIs to use 
- <span style="color:rgb(255, 136, 0)">agentic RAG</span> = using the above techniques each add more responsibility delegated to LLM 
	- agentic RAG formalises this - e.g. data sources can now be abstracted into tools 
## 5.4 Retrieval and RAG Evaluation 
- semantic search evaluated using methods from info retrieval field 
	- these evals require good ground truth datasets to perform evals i.e. 
		- text archive
		- queries 
		- relevance judgments (which docs relevant for each query)
	- most retrieval evals also consider rank of relevant results in computing their metrics
- <mark style="background: #FFB8EBA6;">Mean Average Precision</mark> (<mark style="background: #FFB8EBA6;">MAP</mark>) 
- <mark style="background: #FFB8EBA6;">Normalised Discounted Cumulative Gain</mark> (<mark style="background: #FFB8EBA6;">nDCG</mark>) = more nuanced, where relevance of docs is not binary and 1 doc can be labelled as more relevant than another in the test set + scoring
- RAG evaluation is an ongoing research topic, one approach uses 4 axes
	- <span style="color:rgb(255, 0, 247)">fluency</span> = if generated text is fluent + coherent
	- <span style="color:rgb(255, 0, 247)">perceived utility</span> = if generated answer is helpful + informative
	- <span style="color:rgb(255, 0, 247)">citation recall</span> = % of generated statements about external world are fully supported by citations 
	- <span style="color:rgb(255, 0, 247)">citation precision</span> = % of generated citations that support associated statements 
- human evals are preferred, but can also be automated w LLM-Judges 
	- use LLM to score generations along these axes e.g. `ragas`
	- also can measure <span style="color:rgb(255, 0, 247)">faithfulness</span> (answer consistent to context) + <span style="color:rgb(255, 0, 247)">answer relevance</span>

---
