---
type: article
status: structured
quality:
topics: [llm-fundamentals]
source: ""
created: 2025-03-18
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Architecture
- Encoder (BERT) models process input tokens using self-attention 
	- output = contextualised token embeddings 
	- can be finetuned with `[CLS]` summary token to be used for classification tasks
- Embedding Models (sentence transformers) built on encoder but modify network usage
	- instead of token level, optimised to produce fixed-length semantically rich sentence embeddings
	- embeddings are designed so similar sentences are closer in embedding space 

# 2 Training objective
- Encoder models 
	- MLM or NSP or sentence order prediction 
	- focusing on token level accuracy 
- Sentence Transformers (Embedding models)
	- contrastive/triplet loss 
	- typically trained w siamese/bi-encoder architecture - each sentence encoded independently then compared usually w cosine sim 
	- after getting token level outputs from each, a pooling operation gets applied to yield final sentence embedding
		- mean pooling, max pooling, `[CLS]` token pooling

# 3 Use Cases
- Encoder models
	- for detailed token level interactions e.g. classification, QA etc 
	- expensive if used for sentence comparison, need to process pairs jointly 
- SentenceTransformer 
	- designed for semantic similarity, info retrieval, clustering, search to compare sentences

# 4 Technical details
- encoder 
	- excellent for predicting missing tokens or understanding context granularly 
	- simple pooling for sentence embedding may not capture sentence level semantics 
- SentenceTransformer
	- pooling strategy is key component
		- can also be combined with additional finetuning layers specifically designed to shape embedding space 
	- Whenever a Sentence Transformer model is saved, three types of files are generated:
		- `modules.json` = list of module names, paths, types used to reconstruct the model 
		- `config_sentence_transformers.json` = some of the config options of the SentenceTransformer model
			- including saved prompts, similarity function, package version 
		- module specific files - each module saved in separate subfolders named after the module index + name 
			- `1_Pooling`, `2_Normalize`
			- each will also have a `config.json` file to store default values for keyword args passed to that module

https://sbert.net/docs/sentence_transformer/usage/custom_models.html

```python
from sentence_transformers import models, SentenceTransformer

transformer = models.Transformer("sentence-transformers/all-MiniLM-L6-v2", max_seq_length=256)
pooling = models.Pooling(transformer.get_word_embedding_dimension(), pooling_mode="mean")
normalize = models.Normalize()

model = SentenceTransformer(modules=[transformer, pooling, normalize])
```

```
local-all-MiniLM-L6-v2/
├── 1_Pooling
│   └── config.json
├── 2_Normalize
├── README.md
├── config.json
├── config_sentence_transformers.json
├── model.safetensors
├── modules.json
├── sentence_bert_config.json
├── special_tokens_map.json
├── tokenizer.json
├── tokenizer_config.json
└── vocab.txt
```

To load a SentenceTransformer model from a regular Transformer model
- use the below code, which are identical 

```python
from sentence_transformers import models, SentenceTransformer

transformer = models.Transformer("bert-base-uncased")
pooling = models.Pooling(transformer.get_word_embedding_dimension(), pooling_mode="mean")
model = SentenceTransformer(modules=[transformer, pooling])
```