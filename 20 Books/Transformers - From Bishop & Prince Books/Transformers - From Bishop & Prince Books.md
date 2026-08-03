---
type: book
status: structured
quality:
topics: [llm-fundamentals]
source: ""
created: 2025-07-21
published:
author: ""
flashcards: none
updated: 2025-08-04
---


> [!NOTE] Combined notes from the chapters on Transformers in both books below



![[Screenshot 2025-07-21 at 12.31.54 pm.png| center | 600]]

# 1 Intro to Transformers
- <mark style="background: #FFB8EBA6;">transformers</mark> = neural networks built on the attention mechanism
    - adaptively weigh each input by coefficients that depend on other inputs → captures sequential inductive biases
    - convert input vectors into a richer representation space
- evolution
    - achieved state-of-the-art results first in NLP then in vision, speech, reinforcement learning, etc.
    - enable effective transfer learning through large-scale pre-training
    - well suited to GPU parallelism
- foundational models = very large pre-trained transformers
    - trained with self-supervised objectives on vast unlabelled text corpora
    - <mark style="background: #FFB8EBA6;">scaling hypothesis</mark> = increasing model parameters and dataset size yields significant performance gains without changing the architecture
- language vs image parallels
    - both exhibit many input variables with position-invariant statistics
    - parameter sharing across positions avoids relearning word meaning at every location
- ⛔️ processing text sequences with generic neural nets (i.e. fully connected NNs) is impractical
    1. ⛔️ input dimensionality extremely high
    2. ⛔️ sequence length varies
    3. ⛔️ syntax alone cannot capture semantics
    - parameter sharing across positions, as in CNNs and transformers, alleviates these issues
- GPUs excel at transformer workloads due to the high degree of parallel matrix operations
- Bahdanau attention (2014) enhanced RNN translation → Vaswani et al. (2017) removed recurrence entirely, establishing the modern transformer architecture

![[Screenshot_2024-01-10_at_1.05.32_pm.png| center | 200]]

# 2 Attention 
- <mark style="background: #FFB8EBA6;">attention</mark> = linear combination of token vectors weighted by learned coefficients
	- simplest attention formula = linear combination of input vectors weighted by attention coefficients $a_{nm}$
		- $a_{nm} \approx 0$ suppresses influence, $a_{nm} \approx 1$ amplifies influence

$$
\begin{gather}
\textbf{Simple Attention} \text{: Bahdanau, 2014}
\\ \ \\
\Large
y_n = \sum\limits_{m=1}^n a_{nm} x_m
\end{gather}
$$

- <mark style="background: #FFB8EBA6;">self-attention</mark> = attention where ***queries***, ***keys***, and ***values*** derive from the same sequence
    - enables context-dependent embeddings so one word can occupy multiple locations in embedding space
        - example: `“bank”` near `“water”` in `{python}I swam across the river to the bank`, but near `“money”` in `{python}I went to the bank for cash`
    - parallels information-retrieval
        - $\textcolor{green}{query}$ = desired attributes e.g. user preference
        - $\textcolor{red}{key}$ = stored attributes e.g. movie features
        - $\textcolor{blue}{value}$ = retrieved content e.g. actual movie
    - transformers use soft attention (softmax-weighted) rather than hard single choice

$$
\begin{gather}
\textbf{Self-Attention}
\\ \ \\
\Large
\text{Attention(Q,K,V)} = \text{softmax} \left( \frac{QK^T}{\sqrt{d_k}} \right) V
\end{gather}
$$

![[Screenshot_2024-01-10_at_12.51.30_pm.png| center | 500]]

- input data represented as set of vectors = tokens
	- dimensionality $D$
	- tokens represent words, byte pairs, or characters
	- each token contains features as elements
- similarity is measured by the dot-product $Q \cdot K^T$ - determines influence on value vectors
	- benefits = differentiable + trainable
	- also gets extended via scaling + softmax operations
- another useful analogy = self-attention as a routing mechanism 
	- attention determines proportions of each input routed to each output

![[Screenshot_2024-01-10_at_12.51.15_pm.png| center | 500]]

- components of scaled dot-product similarity
	* similarity score $S = \dfrac{Q K^\top}{\sqrt{d_k}}$
	* division by $\sqrt{d_k}$ reduces softmax saturation → maintains gradient signal
* in original encoder-decoder transformer, cross-attention is what links the encoder to the decoder
	* <mark style="background: #FFB8EBA6;">cross attention</mark> = decoder attention that takes queries from one sequence and keys/values from another

![[Screenshot_2024-01-10_at_6.58.43_pm.png| center | 500]]

# 3 Query, Key, Value Matrices
- $\textcolor{green}{query}$/$\textcolor{red}{key}$/$\textcolor{blue}{value}$ projections - independent weight matrices give flexible linear transformations
	* where they are derived using:
		* $Q = X W_Q$
		* $K = X W_K$
		* $V = X W_V$
	* where weight matrices $W_Q, W_K, W_V$ learned in training
	* $Q$ and $K$ share dimensionality for the dot-product similarity and residual connections
	* optional bias terms can be folded into $W_Q, W_K, W_V$

$$
\begin{gather}
\textbf{Q, K, V matrices}
\\ \ \\
\Large
Q = X \cdot W_Q \\ \ \\ 
\Large 
K = X \cdot W_K \\ \ \\ 
\Large 
V = X \cdot W_V \\ \ \\ 
\end{gather}
$$

# 4 Self-attention extended
- multi-head attention = runs $H$ independent self-attention heads in parallel
	- each head $h$ uses its own $W^h_Q, W^h_K, W^h_V$
	* outputs are concatenated then projected via $W_O$

$$
\Large
Y(X)=\operatorname{Concat}(H_1,\dots,H_H) W_O
$$

![[Screenshot_2024-01-08_at_5.04.09_pm.png| center ]]


* pseudo algo

```python
def multihead_attn(tokens, W_q, W_k, W_v, W_o):
	heads = []
	for h in range(H):
		Q_h = tokens @ W_q[h]
		K_h = tokens @ W_k[h]
		V_h = tokens @ W_v[h]
		H_h = Attention(Q_h, K_h, V_h)
		heads.append(H_h)
	H_concat = concatenate(heads, axis=-1)
	return H_concat @ W_o
```

* transformer block (pre-norm variant)
	* $X \leftarrow X + \text{MultiHead}( \text{LayerNorm}(X) )$
	* $X \leftarrow X + \text{MLP}( \text{LayerNorm}(X) )$
* <mark style="background: #FFB8EBA6;">positional embedding</mark> = injects order information lost by permutation-equivariant attention
	* add position vector $r_n$ to each token $x_n$ → same dimension $D$
	* sinusoidal encoding (Vaswani)
	* components are $\sin$ and $\cos$ at exponentially increasing wavelengths → bounded in $[-1,1]$, unique, and extrapolates beyond training length
	* learned positional embeddings work when sequence lengths at train and test match
* computational efficiency
	* dense feed-forward layer of size $N \times D$ has $O(N^2 D^2)$ cost
	* attention layer shares $W_Q, W_K, W_V$ across tokens → $O(N^2 D)$ compute and $O(D^2)$ parameters
	* subsequent MLP adds $O(N D^2)$ compute
* summary of one transformer layer
	* sequence passes through
		1. multi-head self-attention $+$ residual
		2. layer normalization
		3. feed-forward MLP $+$ residual
		4. second layer normalization
	* repeat for depth to build the full transformer

# 5 Transformer layers
- <mark style="background: #FFB8EBA6;">transformer layer</mark> = maps a set of $D$-dimensional token vectors to a new set of the same dimensionality
    - stacking layers yields deeper, richer representations
    - parameters learned with SGD
- <mark style="background: #FFB8EBA6;">tokens</mark> = basic units fed to transformers
    - may correspond to words, byte-pair encodings, or characters
    - each token represented as a $D$-dimensional feature vector
- activations multiplied by data-dependent attention coefficients
    - coefficient near 0 → path ignored, coefficient near 1 → path emphasized
* transformer = stack of attention layers and MLP (Feed Forward Networks, FFNN)
	* each layer includes:
		1. multi-head self-attention
		2. residual connections (input-output bypass)
		3. layer normalisation (`LayerNorm`)
		4. fully-connected FFNN (with ReLU activation)
	* structure in formula:

$$
\Large
\begin{aligned}
X &\leftarrow X + \text{Multi-head Self-Attn}(X) \\
&\leftarrow \text{LayerNorm}(X) \\
&\leftarrow X + \text{FFNN}(X) \\
&\leftarrow \text{LayerNorm}(X)
\end{aligned}
$$

* structure repeated for multiple layers, no weight sharing across layers

![[Screenshot_2024-01-10_at_12.55.53_pm.png| center | 500]]

# 6 Computational efficiency 
* attention reduces complexity:
	* fully-connected layer complexity: $O(N^2 D^2)$
	* self-attention complexity: $O(N^2 D)$ due to shared parameters across tokens
	* subsequent FFNN complexity: $O(N D^2)$ linear due to parameter sharing
* significantly more efficient than dense layers
# 7 Positional Embeddings
* transformers permutation equivariant → requires explicit positional embeddings
	* <mark style="background: #FFB8EBA6;">position encodings</mark> = vectors $r\_n$ added to token embeddings
	* same dimensionality as embeddings
* positional embeddings should:
	1. provide unique positional representation
	2. be bounded
	3. generalise to longer sequences
	4. express relative position consistently
* sinusoidal positional encoding (Vaswani):

$$
\Large
r_n[2i] = \sin\left(\frac{n}{10000^{2i/D}}\right), \quad r_n[2i+1] = \cos\left(\frac{n}{10000^{2i/D}}\right)
$$

* learned embeddings another approach but lacks generalisation flexibility

![[Screenshot_2024-01-10_at_7.21.23_pm.png| center | 400]]

# 8 NLP Transformer Pipeline 
- 3 stage process for NLP
	- <mark style="background: #FFB8EBA6;">tokenisation</mark> = splits raw text into tokens drawn from a fixed vocabulary
		* word-level = vocabulary of whole words but fails on novel or misspelled words
		* character-level = tiny vocab (letters, digits, punctuation) but discards word semantics and increases sequence length
		* sub-word tokenisation = compromise that merges frequent character sequences
		* byte-pair encoding (bpe) = iterative merge of most common adjacent symbols until target vocab reached
	* <mark style="background: #FFB8EBA6;">embedding lookup</mark> = maps each token index to a learned $D$-dimensional vector
		* typical $D \approx 1{,}024$ and vocab size $\approx 50{,}000$
	* transformer stack = sequence of attention + feed-forward layers whose flavour depends on task
		* encoder = produces contextual representations of the whole input
		* decoder = autoregressive generator that predicts the next token
		* encoder-decoder = seq2seq model with cross attention for translation and similar tasks
* bag of words = order-agnostic model that counts token occurrences for naïve bayes or logistic regression
* attention masking = technique to restrict what each position sees
	* causal (masked) self-attention = sets attention to future positions to $-\infty$ so decoder cannot peek ahead
	* padding mask = prevents `<pad>` tokens in batched tensors from influencing results
# 9 Sampling strategies
* sampling strategies = algorithms for turning decoder logits into text
	* greedy search = choose arg-max at every step
	* beam search = maintain top $B$ partial hypotheses to optimise global score
	* top-k sampling = sample from highest-probability $k$ tokens to add diversity
	* top-p (nucleus) sampling = sample from minimal set whose cumulative probability ≥ $p$
	* temperature scaling = divides logits by $T$ to sharpen ($T<1$) or flatten ($T>1$) the distribution
# 10 Transformer architecture classes
* decoder-only = generative language model (e.g. gpt)
	* uses masked attention + shifted inputs `<start> x_1\ldots x_{N-1}` to predict $x_2\ldots x_N$
* encoder-only = masked-token learner (e.g. bert)
	* randomly masks $≈15\%$ tokens with `<mask>` and predicts them using bidirectional context
* encoder-decoder = seq2seq transducer (e.g. original transformer, t5)
	* decoder queries encoder outputs via cross attention
* gpt series
	* gpt-1 = 12 layers, 117 M params, seq-len 1 024
	* gpt-2 = 48 layers, 1.5 B params, seq-len 2 048
	* gpt-3 = 96 layers, 175 B params, seq-len 4 096
	* gpt-3.5, gpt-4 = larger yet, parameter counts undisclosed or estimated
* bert = bidirectional encoder representations from transformers
	* 24 layers, 16 heads per layer, embedding dim 1 024, \~340 M params
* Training & usage
	* pre-training = masked language modelling on 3.3 B words, max sequence 512
	* fine-tuning = add small task-specific head and update all weights
	* text classification = use `<cls>` embedding → logistic sigmoid
	* token classification = map each token embedding → softmax over entity types
	* span prediction = output start + end logits for each token
* language modelling objective
	* joint probability factorisation
	* decoder maximises log-likelihood via cross entropy

$$
P(t_1,\dots,t_N)=P(t_1)\prod_{n=2}^{N}P(t_n\mid t_1,\dots,t_{n-1})
$$


* few-shot (in-context) learning = large decoder models learn new tasks from a handful of examples given in the prompt without gradient updates
* tokenisation trade-offs
	* smaller tokens → longer sequences but fewer unknowns
	* larger tokens → shorter sequences but risk of out-of-vocabulary
* large language model (LLM) = transformer with billions–trillions of parameters trained on hundreds of billions of tokens
	* self-supervised pre-training enables transfer learning
	* fine-tuning techniques
		* lora = low-rank adaptation that inserts trainable $A B^{\top}$ matrices into frozen weights
		* rlhf / rlaif = align model outputs with human preferences via reinforcement learning
	* vision transformer (VIT) = encoder that tokenises an image into fixed-size patches then applies the same attention machinery
* scaling challenges
	* vanilla attention complexity = $\mathcal{O}(N^{2})$ with sequence length $N$
	* long-sequence research directions
	* sparse or local attention patterns (sliding window, dilution)
	* global tokens that attend to all positions
	* convolutional or linear-attention approximations
* summary of key takeaways
	* transformers rely on self-attention over token embeddings
	* three canonical architectures: decoder, encoder, encoder-decoder
	* positional information injected via learned or sinusoidal embeddings
	* masked attention enables autoregressive generation
	* llms leverage enormous scale and self-supervision for emergent abilities
	* efficiency improvements focus on sequence length, fine-tuning cost, and cross-modal extensions



---

# 11 Summary
- Intro to Transformers
	- Historical context & evolution
	- NLP & extensions to other domains
	- Transformers as foundational models
	- Scaling hypothesis and implications
	- Parallelisation & GPU suitability
- Text Data Processing & Challenges
	- Limitations of MLPs
	- Sequential data handling & param sharing analogy with CNNs
- Core Transformer Concepts
	- Conceptual foundations
	- Routing mechanism analogy
	- Dot-product self-attention
	- Queries, keys, values clearly explained
	- Linear complexity & parameter sharing advantages
- Extensions to Basic Attention
	- Positional embeddings
	- Scaled dot-product attention
	- Multi-head attention
- Transformer Architecture & Layers
	- Layer structure summary
	- Residual connections, LayerNorm vs BatchNorm
	- Complexity & computational efficiency
	- NLP Transformer Pipeline
		- Tokenisation
		- Embeddings
		- Transformer layer integration
- Transformer Model Architectures & LLMs (Large Language Models)
	- Encoder-only transformers
	- Decoder-only transformers
	- Encoder-Decoder transformers
	- LLM characteristics

















![[Screenshot_2024-01-10_at_6.53.18_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.27.12_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_12.52.01_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.00.23_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_12.55.42_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_12.54.50_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_12.55.04_pm.png| center | 600]]

![[Screenshot_2024-01-10_at_12.55.23_pm.png| center | 600]]

![[Screenshot_2024-01-10_at_7.35.04_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_6.43.26_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.25.20_pm.png| center | 500]]

![[Screenshot_2024-01-08_at_5.03.32_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.34.45_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.23.04_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.33.36_pm.png| center | 200]]



![[Screenshot_2024-01-08_at_5.02.47_pm.png| center | 500]]

![[Screenshot_2024-01-08_at_5.03.07_pm.png| center | 500]]

![[Screenshot_2024-01-10_at_7.21.11_pm.png| center | 300]]




