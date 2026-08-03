---
type: chapter
status: structured
quality:
topics: [llm-fundamentals]
source: ""
created: 2025-03-04
published:
author: ""
flashcards: none
updated: 2025-03-13
---

![[Screenshot 2025-03-05 at 9.49.37 am.png| center | 600]]


- [[#1 Intro to LLMs|1 Intro to LLMs]]
	- [[#1 Intro to LLMs#1.1 Embeddings|1.1 Embeddings]]
	- [[#1 Intro to LLMs#1.2 Attention|1.2 Attention]]
	- [[#1 Intro to LLMs#1.3 Transformer Encoder + Decoder|1.3 Transformer Encoder + Decoder]]
	- [[#1 Intro to LLMs#1.4 Encoder-only Models|1.4 Encoder-only Models]]
	- [[#1 Intro to LLMs#1.5 Decoder-only Models|1.5 Decoder-only Models]]
	- [[#1 Intro to LLMs#1.6 Example Code|1.6 Example Code]]
- [[#2 Tokens & Embeddings|2 Tokens & Embeddings]]
	- [[#2 Tokens & Embeddings#2.1 Comparing Model Tokenizers|2.1 Comparing Model Tokenizers]]
	- [[#2 Tokens & Embeddings#2.2 Tokenizer Properties|2.2 Tokenizer Properties]]
	- [[#2 Tokens & Embeddings#2.3 Token Embeddings|2.3 Token Embeddings]]
	- [[#2 Tokens & Embeddings#2.4 Word2Vec|2.4 Word2Vec]]
- [[#3 Inside LLMs|3 Inside LLMs]]
	- [[#3 Inside LLMs#3.1 Overview of the Transformer|3.1 Overview of the Transformer]]
		- [[#3.1 Overview of the Transformer#3.1.1 Forward Pass|3.1.1 Forward Pass]]
		- [[#3.1 Overview of the Transformer#3.1.2 Sampling & Decoding|3.1.2 Sampling & Decoding]]
		- [[#3.1 Overview of the Transformer#3.1.3 Parallel Token Processing & Context Size|3.1.3 Parallel Token Processing & Context Size]]
		- [[#3.1 Overview of the Transformer#3.1.4 Key-Value Caching|3.1.4 Key-Value Caching]]
		- [[#3.1 Overview of the Transformer#3.1.5 Inside the Transformer Block|3.1.5 Inside the Transformer Block]]
	- [[#3 Inside LLMs#3.2 Recent Improvements to Transformer Architecture|3.2 Recent Improvements to Transformer Architecture]]
		- [[#3.2 Recent Improvements to Transformer Architecture#3.2.1 Attention Efficiency|3.2.1 Attention Efficiency]]
		- [[#3.2 Recent Improvements to Transformer Architecture#3.2.2 Transformer Block|3.2.2 Transformer Block]]
		- [[#3.2 Recent Improvements to Transformer Architecture#3.2.3 Positional Embeddings & RoPE|3.2.3 Positional Embeddings & RoPE]]


# 1 Intro to LLMs
- throughout history of NLP - most focus been to represent language in structured manner
	- so computers can easily process them 
	- common tasks include producing embeddings, text output, classification

![[Screenshot 2025-03-05 at 10.02.19 am.webp| center | 400]]

- earliest approaches represented text as <span style="color:rgb(255, 0, 247)">Bag-of-Words</span> (BoW)
	- vocabulary created by retaining all unique words within the corpus 
		- i.e. count how often each word appears - literally a bag of words 
	- main drawback of BoW = words ignore the semantic nature and context of the text
## 1.1 Embeddings
- word2vec, 2013 was first successful example of capturing meaning in embeddings
	- <mark style="background: #FFB8EBA6;">embeddings</mark> = vector representations of text attempting to capture the meaning
		- features within embeddings are not easily interpretable but express some aspect of the text
	- word2vec generates word embeddings by looking at which other words they tend to appear next to in a given sentence
		- at training, word2vec learns relationships between words + distills that into the embedding 

![[Screenshot 2025-03-05 at 10.06.38 am.webp| center | 400]]

- embeddings also allow for measuring semantic similarity via distance metrics
	- and to find analogies between words e.g. "Man to King" - "Woman to ..."
- types of embeddings 
	- <span style="color:rgb(255, 0, 247)">word embeddings</span> = for individual words
	- <span style="color:rgb(255, 0, 247)">sentence embeddings</span> = for sequences of text e.g. paragraphs 
	- <span style="color:rgb(255, 0, 247)">document embeddings</span> = for entire documents e.g. BoW

![[Screenshot 2025-03-05 at 10.11.59 am.webp| center | 400]]

## 1.2 Attention
- earlier seq2seq models e.g. RNNs maintained a fixed vector state of all past tokens
	- architecture was also <span style="color:rgb(255, 0, 247)">autoregressive</span> = consumes all previous generated words, when generating next word 
- <mark style="background: #FFB8EBA6;">attention</mark> = introduced in 2014, allows a model to focus on parts of the input sequence that are relevant to one another 
	- i.e. “attend” to each other and amplify their signal
	- RNNs used attention (before transformers) in decoder step to get better signals for each input word
- <mark style="background: #FFB8EBA6;">Transformer</mark> - introduced in "*Attention is all you need*" in 2017 proposed this new architecture
	- removed recurrence notion entirely, purely using attention
		- allowing it to be trained in parallel + utilise GPUs most efficiently 
	- however decoding remained autoregressive, needing to consume each generated word before creating new words 
	- 2 key sets of blocks 
		- encoder block 
		- decoder block 
## 1.3 Transformer Encoder + Decoder
- encoder block consists of 2 components 
	- <span style="color:rgb(255, 0, 247)">self-attention</span> = can attend to different positions within a single sequence
	- <span style="color:rgb(255, 0, 247)">feedforward neural network</span> 

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-05 at 10.36.45 am.webp" style="width: 50%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-05 at 10.36.56 am.webp" style="width: 40%; object-fit: contain;" alt="Image 2">
</div>

- decoder is slightly different (3 components)
	- <span style="color:rgb(255, 0, 247)">masked self-attention</span> = masks future positions to prevent leaking info when generating outputs
		- i.e. only attends to earlier positions
	- <span style="color:rgb(255, 0, 247)">encoder attention</span> (<span style="color:rgb(255, 0, 247)">cross attention</span>) = pays attention to the output of the encoder
	- <span style="color:rgb(255, 0, 247)">feedforward neural network</span> 

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-05 at 10.53.03 am.webp" style="width: 50%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-05 at 10.53.14 am.webp" style="width: 40%; object-fit: contain;" alt="Image 2">
</div>

- original transformer was an encoder-decoder architecture
	- suited to machine translation - not easily usable for other tasks
## 1.4 Encoder-only Models
- 2018, Google introduced new architecture BERT
	- <mark style="background: #FFB8EBA6;">BERT</mark> = Bidirectional Encoder Representations from Transformers
	- focuses on representing language - only keeps encoder, removes decoder - aka representation models
- inputs contain additional **classification token** `[CLS]` used to represent entire input 
	- often use this `[CLS]` token as input embedding for finetuning model for classification 
- trained using <mark style="background: #FFB8EBA6;">masked language modelling</mark> 
	- masks random % of inputs for model to predict 
	- very good architecture + training procedure for representing contextual language 
- BERT allowed for being able to use the pretrained model on many downstream tasks via finetuning
	- e.g. classification, NER, paraphrase identification, clustering tasks, semantic search etc 

![[Screenshot 2025-03-05 at 11.01.02 am.webp| center | 400]]

## 1.5 Decoder-only Models 
- proposed in 2018 to target generative tasks - known as <mark style="background: #FFB8EBA6;">GPT</mark> (<span style="color:rgb(255, 0, 247)">Generative Pre-trained Transformer</span>)
	- GPT-1 = 117 million params, trained on 700 books in CommonCrawl
	- GPT-2 = 1.5 billion params 
	- GPT-3 = 175 billion params
	- all else the same, more parameters and data (scaling) led to larger models steadily being released

![[Screenshot 2025-03-05 at 11.03.26 am.webp| center | 400]]

- this same architecture that underpins how LLMs still work 
	- LLMs have <mark style="background: #FFB8EBA6;">context length/context window</mark> = max number of tokens the model can process
		- autoregressive nature causes context length to increase as new tokens get generated
- training paradigms 
	- <span style="color:rgb(255, 0, 247)">pre-training</span> = majority of compute + training time 
		- uses language modelling objective = predict next token 
		- e.g. Llama 2, Meta used A100-80GB GPUs - $1.50 an hour to rent, total cost would be $5 million
	- <span style="color:rgb(255, 0, 247)">fine-tuning or post-training</span> = using pre-trained model, further training on a domain or narrower task 
		- can be fine-tuned to create instruct or chat models - to follow directions 
- apart from Transformers, other promising architectures have been proposed 
	- e.g. Mamba, KWKV - all trying to have transformer performance w more benefits e.g. fast inference or larger context length 
## 1.6 Example Code
- `{python}transformers.pipeline` = encapsulates model, tokenizer and text generation process into single function 

```python
from transformers import pipeline 

generator = pipeline(
	"text-generation", 
	model = model, 
	tokenizer = tokenizer, 
	return_full_text = False,      # prompt not to be returned 
	max_new_tokens = 500,          # max number of tokens model will generate
	do_sample = False              # sampling strategy - use greedy/most probable next token
)

messages = [{"role":"user", "content":"create a funny chicken joke"}]
output = generator(messages)
```

---
# 2 Tokens & Embeddings
- LLMs deal in tokens and embeddings 
	- output of a tokenizer via `{python}tokenizer.decode()` gives `token_ids` - identifiers for each token
- <mark style="background: #FFB8EBA6;">tokenizers</mark> break down input text into smaller pieces called tokens
- tokens can be:
	- complete words (e.g., `"Write"`, `"email"`)
	- parts of words (e.g., `"apolog"`, `"izing"`)
	- punctuation as individual tokens
	- special tokens (e.g., start of text `<s>`)
- tokenization methods:
	- <span style="color:rgb(255, 0, 247)">byte pair encoding</span> (BPE): used by GPT models
	- <span style="color:rgb(255, 0, 247)">WordPiece</span>: used by BERT models
	- **vocabulary size** and **special tokens** are important design choices
	- tokenizers need training on specific datasets to optimise vocabulary
- types of tokens:
	- <span style="color:rgb(255, 136, 0)">word tokens</span>:
		- may struggle with new words not seen during training
		- results in a large vocabulary with minimal differences between tokens (e.g., "apology," "apologize," "apologetic")
	- <span style="color:rgb(255, 136, 0)">subword tokens</span>:
		- can represent full and partial words
		- good at handling new words by breaking them into smaller, known parts
		- advantage over character tokens as they allow more efficient use of transformer's limited context length
	- <span style="color:rgb(255, 136, 0)">character tokens</span>:
		- operate at the letter level, useful for new or rare words
		- simplifies tokenization but makes modelling more complex
	- <span style="color:rgb(255, 136, 0)">byte tokens</span>:
		- break down tokens into individual bytes (tokenization-free encoding)
		- used when characters cannot be otherwise represented
	- <span style="color:rgb(255, 136, 0)">hybrid approach</span>:
		- some subword tokenizers (e.g., GPT-2, RoBERTa) include bytes as a fallback
		- not purely tokenization-free since they use bytes only for a subset of cases

![[Screenshot 2025-03-11 at 11.42.56 am.webp| center | 500]]

## 2.1 Comparing Model Tokenizers
- each model makes design choices around vocab size + special tokens 
- BERT special tokens:
    - `[UNK]` = unknown token for unseen words
    - `[SEP]` = separates inputs in cross-encoder tasks
    - `[PAD]` = padding for fixed-length input requirements
    - `[CLS]` = classification tasks
    - `[MASK]` = masked tokens during training
- GPT-4 and StarCoder2 special tokens:
    - `<|fim_prefix|>`, `<|fim_middle|>`, `<|fim_suffix|>`: support "fill-in-the-middle" text generation
	    - enable the LLM to generate a completion given not only the text before it but also considering the text after it
    - StarCoder2 includes `<filename>` and `<reponame>` for handling code in different files and repositories
- Galactica's unique tokens:
    - `[START_REF]`, `[END_REF]`: wrap scientific references
    - `<work>`: used for step-by-step reasoning and chain-of-thought processes
- Phi-3 (Llama 2) tokens:
    - `<|user|>`, `<|assistant|>`, `<|system|>`: facilitate conversation modelling and multi-turn dialogues

| **Model**           | **Year** | **Method** | **Vocabulary Size** | **Special Tokens**                                                                                                                                                      |
| ------------------- | -------- | ---------- | ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **BERT (uncased)**  | 2018     | WordPiece  | 30,522              | `[UNK]`, `[SEP]`, `[PAD]`, `[CLS]`, `[MASK]`                                                                                                                            |
| **BERT (cased)**    | 2018     | WordPiece  | 28,996              | Same as uncased version                                                                                                                                                 |
| **GPT-2**           | 2019     | BPE        | 50,257              | `<\|endoftext\|>`                                                                                                                                                       |
| **Flan-T5**         | 2022     | -          | 32,100              | `<unk>`, `<pad>`                                                                                                                                                        |
| **GPT-4**           | 2023     | BPE        | ~100,000            | `<\|endoftext\|>`, fill in the middle tokens<br>`<\|fim_prefix\|>`, `<\|fim_middle\|>`, `<\|fim_suffix\|>`                                                              |
| **StarCoder2**      | 2024     | BPE        | 49,152              | `<\|endoftext\|>`, fill in the middle tokens<br>`<\|fim_prefix\|>`, `<\|fim_middle\|>`, `<\|fim_suffix\|>`, `<\|fim_pad\|>`<br>`<filename>`, `<reponame>`, `<gh_stars>` |
| **Galactica**       | 2022     | BPE        | 50,000              | `<s>`, `<pad>`, `</s>`, `<unk>`, `[START_REF]`, `[END_REF]`, `<work>`                                                                                                   |
| **Phi-3 (Llama 2)** | 2024     | BPE        | 32,000              | `<\|endoftext\|>`, chat tokens `<\|user\|>`, `<\|assistant\|>`, `<\|system\|>`                                                                                          |

- an example of a text and all the different ways these models represent the tokens

```python
text = """
English and CAPITALIZATION
🎵鸟
show_tokens False None elif == >= else: two tabs:" " Three tabs: " "
12.0*50=600
"""
```

![[Screenshot 2025-03-11 at 11.53.25 am.webp| center | 700]]

> [!NOTE] Function to colour tokens for comparison if interested
```python
colors_list = ['102;194;165', '252;141;98', '141;160;203', '231;138;195', '166;216;84', '255;217;47']
def show_tokens(sentence, tokenizer_name):
	tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
	token_ids = tokenizer(sentence).input_ids
	
	for idx, t in enumerate(token_ids):
		print(
		f'\x1b[0;30;48;2;{colors_list[idx % len(colors_list)]}m' +
		tokenizer.decode(t) +
		'\x1b[0m',
		end=' '
		)
```

## 2.2 Tokenizer Properties
- three major groups of tokenizer design choices
    - <span style="color:rgb(255, 136, 0)">tokenization method</span> = algorithm that defines how to select an appropriate set of tokens to represent a dataset
	    - e.g. BPE, WordPiece, SentencePiece etc 
    - <span style="color:rgb(255, 136, 0)">tokenizer parameters</span>
        - **vocabulary size** = determines how many tokens to keep in the tokenizer’s vocabulary
            - common sizes include 30K, 50K, and increasingly larger sizes like 100K
        - **special tokens** = additional tokens to help the model handle special cases, commons ones include:
			- beginning of text token (e.g., `<s>`) 
			- end of text token
			- padding token
			- unknown token
			- CLS token
			- masking token
			- custom tokens for domain-specific needs, e.g., Galactica’s `<work>` and `[START_REF]` tokens
		- capitalisation handling = strategy for dealing with capitals, especially in languages like English
			- options include converting everything to lowercase
			- balancing the need to preserve meaningful capitalisation (e.g., names) against conserving vocabulary space
	- <span style="color:rgb(255, 136, 0)">domain of the data</span> = the dataset the tokenizer is trained on influences how it tokenises text
		- for example, a text-focused tokenizer might handle code indentation spaces differently
- overall impact
	- well-chosen tokenization strategies can make the model's job easier + lead to better performance
## 2.3 Token Embeddings
- token embeddings - language is treated as a sequence of tokens
    - training a good model on a large set of tokens can help it capture complex patterns in text
    - **requires finding the best numerical representation for tokens to allow the model to model patterns accurately**
- **language model holds embeddings for the tokenizer's vocabulary**
    - after initialising and training a tokenizer, it is used in the language model's training process
    - a pretrained language model is tied to its tokenizer - **switching tokenizers requires retraining the model**

![[Screenshot 2025-03-11 at 12.04.34 pm.webp| center | 500]]

- <mark style="background: #FFB8EBA6;">contextualised word embeddings</mark>
    - unlike static word vectors, language models create contextualised embeddings
    - these embeddings vary based on the token's surrounding context

![[Screenshot 2025-03-11 at 12.05.02 pm.webp| center | 400]]

```python
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-base")   # Load a tokenizer
model = AutoModel.from_pretrained("microsoft/deberta-v3-xsmall")      # Load a language model
tokens = tokenizer('Hello world', return_tensors='pt')                # Tokenize the sentence
output = model(**tokens)[0]                                           # Process the tokens

output.shape
# torch.Size([1, 4, 384])
```

- e.g. DeBERTa v3 outputs above
	- first dimension is single batch, next is 4 tokens, each being a vector of 384 values (the embedding for the token)
		- i.e. `batch_size, sequence_length, embedding_dimensionality`
	- notice `"Hello World"` became 4 tokens, added special tokens 

```python
for token in tokens['input_ids'][0]:
	print(tokenizer.decode(token))
# [CLS]
# Hello
# world
# [SEP]
```

![[Screenshot 2025-03-11 at 12.08.44 pm.webp| center | 500]]

- text embeddings (for sentences and whole documents)
    - text embedding models **generate a single vector representing the meaning of a text**
    - common method: averaging all token embeddings produced by the model (<span style="color:rgb(255, 0, 247)">mean pooling</span>)
	    - high-quality models are often specifically trained for text embedding tasks
	- <span style="color:rgb(255, 0, 247)">embedding dimensionality</span> for a given token depends on the underlying embedding model

```python
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
vector = model.encode("Best movie ever!")
vector.shape
# (768,)
```

- word embeddings beyond LLMs
    - pretrained word embeddings (e.g., word2vec, GloVe) can be downloaded via `gensim` library
## 2.4 Word2Vec
- <span style="color:rgb(255, 0, 247)">word2vec algorithm</span> and <span style="color:rgb(255, 0, 247)">contrastive training</span>
    - trained on text-generated examples, similar to large language models
    - **embeddings are derived from a classification task to predict if words commonly appear in the same context**
        - context = words appearing together in many sentences in the training data
    - the model takes two words as input:
        - outputs `1` if they are in the same context
        - outputs `0` if not
    - training setup:
        - the center word is the primary input
        - each neighbouring word forms a distinct secondary input
    - to avoid overfitting (e.g., always predicting 1), negative examples are introduced
        - negative examples = words that are not typically neighbors, generated by random sampling
- key concepts of word2vec
    - <mark style="background: #FFB8EBA6;">skip-gram</mark> = method for selecting neighboring words as positive examples
    - <mark style="background: #FFB8EBA6;">negative sampling</mark> = adding randomly generated negative examples to the dataset (NCE)

![[Screenshot 2025-03-11 at 12.14.21 pm.webp| center | 500]]

![[Screenshot 2025-03-11 at 12.14.49 pm.webp| center | 500]]


> [!NOTE] **Noise Contrastive Estimation** (*NCE*) = unreasonably effective, simply trying to detect positive examples from randomly generated ones

![[Screenshot 2025-03-11 at 12.16.54 pm.webp| center | 600]]

---
# 3 Inside LLMs
- LLMs based on decoder architecture
	- they are <span style="color:rgb(255, 0, 247)">autoregressive</span> i.e. output token is appended to the prompt
		- then this new text is presented to the model again for another forward pass to generate the next token
	- LLM software basically runs it in a loop to sequentially expand the generated text until completion
## 3.1 Overview of the Transformer
### 3.1.1 Forward Pass
- transformer is made up of 3 components
	- 1. <span style="color:rgb(255, 136, 0)">tokenizer </span>
	- 2. <span style="color:rgb(255, 136, 0)">stack of transformer blocks</span>
	- 3. <span style="color:rgb(255, 136, 0)">language modelling (lm) head</span>
- other transformers may have different kinds of heads e.g. sequence classification, token classification etc 
	- can display order of layer by printing out model 

![[Screenshot 2025-03-11 at 12.39.46 pm.webp| center | 700]]

- e.g. below, we can see: 
	- various nested layers of the model - majority in the transformer blocks (`model`) followed by `lm_head`
	- embeddings matrix `embed_tokens` has 32,064 tokens each with vector size of 3,072
	- 32 blocks of transformer decoder layers `32 x Phi3DecoderLayer`
		- each containing attention layer `Phi3Attention` and FFNN/MLP `Phi3MLP`
	- lastly, `lm_head` w vector size of 3,072, outputs vector equivalent to number of tokens in vocab (32,064)
		- each output is a probability score for that specific token 

```
Phi3ForCausalLM(
	(model): Phi3Model(
		(embed_tokens): Embedding(32064, 3072, padding_idx=32000)
		(embed_dropout): Dropout(p=0.0, inplace=False)
		(layers): ModuleList(
			(0-31): 32 x Phi3DecoderLayer(
				(self_attn): Phi3Attention(
					(o_proj): Linear(in_features=3072, out_features=3072, bias=False)
					(qkv_proj): Linear(in_features=3072, out_features=9216, bias=False)
					(rotary_emb): Phi3RotaryEmbedding()
				)
				(mlp): Phi3MLP(
					(gate_up_proj): Linear(in_features=3072, out_features=16384, bias=False)
					(down_proj): Linear(in_features=8192, out_features=3072, bias=False)
					(activation_fn): SiLU()
				)
				(input_layernorm): Phi3RMSNorm()
				(resid_attn_dropout): Dropout(p=0.0, inplace=False)
				(resid_mlp_dropout): Dropout(p=0.0, inplace=False)
				(post_attention_layernorm): Phi3RMSNorm()
			)
		)
		(norm): Phi3RMSNorm()
	)
	(lm_head): Linear(in_features=3072, out_features=32064, bias=False)
)
```

### 3.1.2 Sampling & Decoding
- after the model's forward pass, the <mark style="background: #FFB8EBA6;">decoding strategy</mark> = decides which tokens to sample based on the probabilities 
	- greedy decoding = choose highest scoring token every time
		- what happens when using `temperature = 0`
	- see AI Engineering notes for other types of decoding
### 3.1.3 Parallel Token Processing & Context Size
- parallel token processing in transformers
    - transformers enable parallel processing of input tokens, improving computational efficiency
    - each input token has its own computation path, allowing simultaneous processing
- <mark style="background: #FFB8EBA6;">context size</mark> (context length)
    - defines the maximum number of tokens a model can process at once
	    - a 4K context length model can handle up to 4,000 tokens in a single pass
    - each token stream starts with an embedding vector and positional information
- text generation process
	- **only the output of the last token stream is used to predict the next token**
		- previous token streams' calculations contribute to the final stream through the attention mechanism
	- earlier outputs (not final output vectors) are used in attention within each transformer block
### 3.1.4 Key-Value Caching
- <mark style="background: #FFB8EBA6;">Key-Value Caching</mark> = enable faster generation by caching the keys and values of previously computed tokens
	- caching allows reusing previous attention calculations when generating new tokens
		- hence only need to calculate for the last stream
		- aka KV-Caching
	- avoids recalculating all previous token streams
		- enabled by default in Hugging Face transformers
		- example e.g. for 100 tokens - w/o cache is 22 seconds, w cache is 4.5 seconds

![[Screenshot 2025-03-11 at 1.01.20 pm.webp| center | 500]]

### 3.1.5 Inside the Transformer Block
- two main components
    1. **attention layer** = incorporates relevant information from other input tokens and positions
    2. **feedforward layer** = contains most of the model’s processing capacity
- attention layer details
    - <mark style="background: #FFB8EBA6;">attention mechanism</mark> = helps the model use context effectively while processing a specific token
	    - uses an input sequence and focuses on the current position
    - output vector combines information from previous tokens using the attention mechanism
- <mark style="background: #FFB8EBA6;">multi-head attention</mark>
    - duplicates the attention mechanism to run in parallel
	    - each parallel attention mechanism is called an **attention head**
    - improves the model's ability to capture complex patterns by attending to multiple aspects of the input simultaneously
- projection matrices in attention
    - training generates three projection matrices:
        - **query projection matrix**
        - **key projection matrix**
        - **value projection matrix**
    - these matrices project input tokens into three different spaces used in attention
- attention mechanism steps
1. **relevance scoring** = calculating how relevant each input token is to the current token
	- i.e. query by key dot product (and other details e.g. softmax + scaling) i.e. $Q \cdot K^T$ 
2. **combining information** = aggregating relevant information based on the relevance scores
	- i.e. multiplies output of relevance scoring by Values vector i.e. $\text{relevance scoring} \cdot V$ 

![[Screenshot 2025-03-11 at 1.03.32 pm.webp| center | 500]]

- <mark style="background: #FFB8EBA6;">self-attention</mark> = a specific type of attention where the input sequence is compared against itself
    - helps the model determine which parts of the input are most relevant to each token being processed

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-11 at 1.05.46 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-11 at 1.06.45 pm.webp" style="width: 47%; object-fit: contain;" alt="Image 2">
</div>

## 3.2 Recent Improvements to Transformer Architecture
### 3.2.1 Attention Efficiency 
- most research focus is towards attention - since attention calculation is the most computationally expensive part of the process
	- improve inference scalability of larger models by reducing the size of the matrices involved
- as transformers scaled larger, many ideas proposed e.g.
	- <span style="color:rgb(255, 0, 247)">sparse attention</span> = only computing attention for a selected subset of tokens rather than all token pairs
		- GPT-3 interweaved full attention with sparse attention 
	- <span style="color:rgb(255, 0, 247)">sliding window attention</span> = each token only attends to a fixed “window” of neighbouring tokens - efficiently maintains local context
		- as introduced in the paper LongFormer
	- <span style="color:rgb(255, 0, 247)">local attention</span> = similar to sliding window - restricts attention to nearby tokens
		- sometimes with mechanisms to include occasional global tokens to capture broader context
	- <span style="color:rgb(255, 0, 247)">multi-query attention</span> = each attn head shares the $key$ and $value$ matrices for all heads
		- only query matrices are unique for each head
	- <span style="color:rgb(255, 0, 247)">grouped query attention (GQA)</span> = groups $queries$ to share same $key$ and $value$ projections within each group
		- strikes balance between full MHA and multi-query approaches
		- used in Llama 2 and 3

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-11 at 2.57.18 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-11 at 2.57.29 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 2">
</div>

- GQA is useful for larger models since MQA can be too punishing
	- instead of cutting number of keys and value matrices to one of each, allows us to use more (but less than number of heads)

<div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
  <div style="display: flex; justify-content: space-between; width: 100%;">
    <img src="Screenshot 2025-03-11 at 3.02.20 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
    <img src="Screenshot 2025-03-11 at 3.02.33 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 2">
  </div>
  <div style="display: flex; justify-content: center; width: 100%; margin-top: 10px;">
    <img src="Screenshot 2025-03-11 at 3.02.44 pm.webp" style="width: 50%; object-fit: contain;" alt="Image 3">
  </div>
</div>

- <span style="color:rgb(255, 0, 247)">Flash Attention</span> = method to give improved speedup on GPUs
	- calculates attention by optimising what values are loaded + moved onto GPU shared memory (SRAM) & HBM
### 3.2.2 Transformer Block
- very few changes have become established from the original transformer (incredibly resilient)
- 3 key changes
	- <span style="color:rgb(255, 0, 247)">post-norm</span> instead of pre-norm
	- <span style="color:rgb(255, 0, 247)">RMSNorm</span> instead of LayerNorm
	- <span style="color:rgb(255, 0, 247)">SwiGLU</span> and other new variants instead of ReLU

![[Screenshot 2025-03-11 at 3.07.35 pm.webp| center | 500]]

### 3.2.3 Positional Embeddings & RoPE
- positional embeddings are vital component to transformer - keep track of order of words/tokens
	- <span style="color:rgb(255, 0, 247)">rotary positional embeddings</span> (<mark style="background: #FFB8EBA6;">RoPE</mark>) = successful positional encoding scheme common today
	- original transformer used absolute positional embeddings
		- using either static sinusoidal methods or learned in training 
		- challenging when tried to scale up + used w long context 
- RoPE instead encodes positional info to **capture both absolute + relative token positions**
	- based on idea of rotating vectors in their embedding space 
	- note: Rotary embedding computed at each attention step, not at the very start like OG transformer
		- specifically, they get computed with Q, K matrices just before being multiplied together

<div style="display: flex; justify-content: space-between;">
  <img src="Screenshot 2025-03-11 at 3.35.24 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 1">
  <img src="Screenshot 2025-03-11 at 3.36.14 pm.webp" style="width: 48%; object-fit: contain;" alt="Image 2">
</div>


---
