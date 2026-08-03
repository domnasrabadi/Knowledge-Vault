---
type: book
status: structured
quality:
topics: [llm-fundamentals]
source: ""
created: 2025-02-16
published:
author: ""
flashcards: none
updated: 2025-05-18
---
#books

![[Screenshot 2025-02-16 at 4.48.08 pm.webp| 300]]



> Foreword by Tomas Mikolov (Creator of Word2Vec)

# 1 Notation
- curly brackets = set containing $N$ elements from $x_{1}$ to $x_N$
$$
\Large\{x_i\}^N_{i=1}
$$

- equals by definition or "is defined as"
$$
\Large a \stackrel{\mathrm{def}}{=} b
$$

- a model is often defined as a mathematical function 
	- $w$ = weights of the model (aka slope, coefficients)
	- $b$ = biases (aka intercept, constant term)
	- also known as an affine transformation (not true linear since it requires $b$ = 0)
$$
\Large
f(x) \stackrel{\mathrm{def}}{=} wx + b
$$

- a dataset, where
	- $N$ = size of dataset
	- $\{(x_1, y_1), (x_2, y_2), ..., (x_N, y_N)\}$ = individual training examples
$$
\Large
\{ (x_{i}, \ y_i)\}^{N}_{i=1} \rightarrow \  \{(x_1, y_1), (x_2, y_2), ..., (x_N, y_N)\}
$$


- a prediction from the model 
$$
\Large
f(x_i) = \hat{y_i}
$$

- generalised formula for the squared error function 
	- where $\hat{y_i}$ = predicted value of the model 
	- and $y_i$ = actual value 
- and below, the **MSE (mean squared error)** loss function (common for linear regression)
	- $J(w, b)$ = total error across the dataset aka cost function 
$$
\begin{gather}
\small \text{loss function (for a single example)} \\ \ \\ 
\Large
\text{err}(\hat{y_i}, y_i) \stackrel{\mathrm{def}}{=} (\hat{y_i} - y_i)^2 \\ \ \\
\small \text{cost function (across entire dataset)} \\ \ \\
\Large
J(w, b) \stackrel{\mathrm{def}}{=} \frac{\small{(\hat{y_1} - y_1)^2 + (\hat{y_2} - y_2)^2 + ... + (\hat{y_N} - y_N)^2}}{N} \\ \ \\
\small \text{or expanded as:} \\ \ \\
\Large
J(w, b) \stackrel{\mathrm{def}}{=} \frac{\small{(wx_1 + b - y_1)^2 + (wx_2 + b - y_2)^2 + ... + (wx_N + b - y_N)^2}}{N}
\end{gather}
$$

- partial derivatives of $w, b$ with respect to the loss function $J(w, b)$
	- partial derivatives used for functions of more than 2 variables 
$$
\Large
\frac{\partial J}{\partial w} \text{ and } \frac{\partial J}{\partial b}
$$

- composite function = output of function A, becomes input to function B
	- e.g. for the 2 functions $\rightarrow g(), f()$ 
	- calculate $g()$ first then use the result for $f()$
$$
\Large
f(g(x))
$$


- sum rule of differentiation 
	- derivative of the sum of 2 functions == sum of their derivatives 
$$
\Large
\frac{\partial}{\partial x} \ \big[ f(x) + g(x) \big] = \frac{\partial}{\partial x}f(x) + \frac{\partial}{\partial x}g(x)
$$

- constant multiple rule of differentiation 
	- derivative of a constant multiplied by a function == constant times the derivative of the function 
$$
\Large\{x_i\}^N_{i=1}
$$
- chain rule of differentiation 
	- derivative of a composite function $f(g(x))$ written as $\frac{\partial}{\partial x}[f(g(x))]$ 
	- == product of the derivative of $f$ with respect to $g$ 
	- and the derivative of $g$ with respect to $x$ 
$$
\Large 
\frac{\partial}{\partial x}\ \big[f(g(x))\big] = \frac{\partial f}{\partial g} \cdot \frac{\partial g}{\partial x}
$$


- vector = representing inputs $x$ as feature vectors 
	- also called dimensions, features, components 
	- e.g. for 2 feature vectors and 2 weights of the model
$$
\Large
\mathbf{x} \stackrel{\mathrm{def}}{=} \begin{bmatrix}
x_1 \\
x_2
\end{bmatrix}, \ 
\mathbf{w} \stackrel{\mathrm{def}}{=} \begin{bmatrix}
w_1 \\
w_2
\end{bmatrix}
$$

- row vector = alternate representation of column vector above 
$$
\Large
\mathbf{x} \ \stackrel{\mathrm{def}}{=} \ \begin{bmatrix}
x_1, 
x_2
\end{bmatrix}, \ \ 
\mathbf{w} \ \stackrel{\mathrm{def}}{=} \ \begin{bmatrix}
w_1, 
w_2
\end{bmatrix}
$$

- transposing a row vector == converts it to column vector 
$$
\Large
\begin{bmatrix}
x_1, 
x_2
\end{bmatrix}^T \equiv
\begin{bmatrix}
x_1 \\
x_2
\end{bmatrix}
$$

- linear model 
	- where $w \cdot x$ is the dot product of 2 vectors (see below)
$$
\Large
y = \mathbf{w \cdot x} + b
$$

- dot product (aka scalar product)
	- combines 2 vectors of same dimensionality to produce a **scalar** (a single number/decimal)
	- $\sum\limits^d_{j=1}$ represents $d$ as dimensionality of the input, and $j$ runs from 1 to $d$ 
$$
\Large
\mathbf{w \cdot x} = \sum\limits^d_{j=1} w^{(j)} x^{(j)}
$$

- sum of 2 vectors
	- both having same dimensionality $D$ 
$$
\Large
\mathbf{a + b} = \big[ a^{(1)} + b^{(1)}, a^{(2)} + b^{(2)}, ..., a^{(D)} + b^{(D)} \big]^T
$$

![[Screenshot 2025-02-22 at 12.12.36 pm.webp| center | 600]]


- element wise product 
	- both having same dimensionality $D$
$$
\Large
\mathbf{a \odot b} = \big[ a^{(1)} \cdot b^{(1)}, a^{(2)} \cdot b^{(2)}, ..., a^{(D)} \cdot b^{(D)} \big]^T
$$

![[Screenshot 2025-02-22 at 12.13.01 pm.webp| center | 500]]

- norm of a vector denoted as $|| x ||$ 
	- represents it's length or magnitude
	- defined as square root of the sum of the squares of it's components 
$$
\begin{gather}
\\ \ \\
\text{general form:}
\\ \ \\ 
\Large ||x|| = \sqrt{\sum\limits^D_{j=1} x_{(i)}^2}
\\ \ \\
\small{\text{e.g. for a 2D vector}}
\\ \ \\
\Large
||x|| = \sqrt{x_{(1)}^2 + x_{(2)}^2}
\end{gather}
$$

- cosine of the angle $\theta$ between 2 vectors 
$$
\Large
\cos(\theta) = \frac{x \cdot y}{||x|| \ ||y||}
$$

- unit vector 
	- a zero vector has all components = 0
	- unit vector has a length of 1
	- can convert any non-zero vector $x$ into a unit vector $\hat{x}$ by dividing vector by it's norm
		- essentially just scaling it 
$$
\Large
\hat{x} = \frac{x}{||x||}
$$


- activation function 
	- represented by $\phi$  - can be ReLU, Sigmoid, Tanh etc 
$$
\Large
y = \phi (wx + b)
$$
$$
\begin{gather}
\text{Sigmoid} \rightarrow \sigma(x) = \frac{1}{1 + e^{-x}} \\ \ \\
\text{ReLU} \rightarrow(x) = \max(0, x)
\end{gather}
$$

![[Screenshot 2025-02-22 at 12.24.18 pm.webp| center | 500]]

- 2 layer nested neural network, with an activation function, where 
	-  $f_1(x) = \phi(ax + b)$
	-  $f_2(z) = \phi(cz + d)$
	- also represented as computational graph below the equation 
		- 2 non linear units = blue rectangles (e.g. neurons)
		- each unit has 2 trainable params $w, b$ or $c, d$ = grey circles 
$$
\Large
y = f_2(f_1(x)) = \phi \ (c \phi \ (ax + b) + d)
$$

![[Screenshot 2025-02-22 at 12.25.00 pm.webp| center | 500]]

- a **Feedforward Neural Network (FFNN)** computational graph with 3 input units
	- and output layer with a single unit
	- also called a **Multilayer Perceptron (MLP)**
	- layers where each unit connects to all units in both adjacent layers = **fully connected/dense layer**

![[Screenshot 2025-02-22 at 12.27.47 pm.webp| center | 600]]

- matrix = two-dimensional array of numbers arranged into rows and columns
	- generalises vectors into higher dimensionalities 
	- shape is always written in order of $m$ rows and $n$ columns 

$$
\Large 
A =
\begin{bmatrix}
a_{1,1} & a_{1,2} & ... & a_{1, n} \\
a_{2,1} & a_{2,2} & ... & a_{2, n} \\ 
\vdots & \vdots & \ddots & \vdots \\
a_{m,1} & a_{m,2} & ... & a_{m,n}
\end{bmatrix}
$$

- sum of 2 matrices = defined element wise as 
$$
\Large
(A + B)_{i,j} = a_{i,j} + b_{i,j}
$$

![[Screenshot 2025-02-22 at 12.33.52 pm.webp| center | 500]]

- product of 2 matrices with dimensions
	- $A_{m \times n}$ and $B_{n \times p}$ gives matrix $C_{m \times p}$ 
	- where number of cols in $A$ must be == number of rows in $B$ 
$$
\Large
C_{i,k} = \sum\limits_{j=1}^n \ a_{i,j} \ b_{j,k}
$$
![[Screenshot 2025-02-22 at 12.36.12 pm.webp| center | 500]]

- transposing a matrix $A$
	- swaps its rows an columns resulting in $A^T$ 
$$
\Large
(A^T)_{i, j} = a_{j, i}
$$

- matrix vector multiplication 
	- special case of matrix multiplication 
	- where matrix $A$ multiplied by vector $x$ of size $n$ 
	- result is a vector $y = Ax$ with $m$ components 
$$
\Large
y_i = \sum\limits^n_{j = 1} \ a_{i, j} \ x^{(j)}
$$
![[Screenshot 2025-02-22 at 12.38.38 pm.webp| center | 500]]

- weights and biases of a FFNN can be compactly represented with matrices & vectors 
	- enables use of highly optimised linear algebra libraries e.g. BLAS, cuBLAS


- binary cross entropy (or logistic loss) of a single example 
	- over 80 years old but still one of most widely used algos today 
	- log function = natural logarithm 
$$
\Large
\text{BCE Loss}(\hat{y_i}, y_i) = - y_i \log(\hat{y}) + (1 - y_i) \log(1 - \hat{y_i})
$$
- example with correct + incorrect predictions using BCE 
	- logarithm of 0 is undefined
	- as $x$ approaches 0, $-\log(0)$ approaches infinity 
		- which means a very severe loss 
		- but sigmoid often used to keep values strictly between 0 and 1 
		- so without reaching them, loss stays finite 

$$
\begin{gather}
\textbf{perfect prediction where } y_i = 0, \hat{y_i} = 0 \\ \ \\ 
loss(0,0) = - 0 \cdot \log(0) + (1 - 0) \cdot \log(1 - 0) = -\log(1) = 0
\\ \ \\ 
\textbf{bad prediction where } y_i = 0, \hat{y_i} = 1 \\ \ \\ 
loss(1, 0) = - 0 \cdot \log(1) + (1- 0) \cdot \log(1 -1) = -\log(0)
\end{gather}
$$

![[Screenshot 2025-02-22 at 12.46.48 pm.webp| center | 400]]

- binary cross entropy i.e. cost function, == average loss for all examples in the dataset 
$$
\Large
\text{loss}_\mathcal{D} = - \frac{1}{N} \sum\limits^N_{i = 1} 
\ y_i \log(\hat{y_i}) + (1 - y_i) \log(1 - \hat{y_i})
$$


> [!NOTE] Elegance of ML Math 
> - activation function of sigmoid, loss function of cross entropy
> 	- both arise from Euler's number $e$
> - their properties make them ideal for binary classification 
> 	- as sigmoid keeps values between 0-1
> 	- while cross entropy spans from 0 to $\inf$
> - when combined, their exponential & logarithmic components elegantly cancel 
> 	- yielding a simpler/stable linear function as the derivation

- gradient of a vector = contains all the partial derivatives 
	- gradient of the loss function denoted as $\Delta\text{loss}$ 
	- when gradient is positive, means increasing the corresponding parameter will increase the loss
	- hence, to minimise loss - we should decrease the parameter 
$$
\Large
\nabla \mathrm{loss} \stackrel{\mathrm{def}}{=} 

\biggl(

  \frac{\partial \mathrm{loss}}{\partial w^{(1)}},

  \frac{\partial \mathrm{loss}}{\partial w^{(2)}},

  \dots,

  \frac{\partial \mathrm{loss}}{\partial w^{(D)}},

  \frac{\partial \mathrm{loss}}{\partial b}

\biggr)
$$

- softmax function 
	- $z$ is a $K$ dimensional vector of logits
		- logits = raw outputs of neural networks, prior to any activation function being applied 
	- $i$ is the index for which softmax is computed 
	- $e$ is Euler's number 
$$
\Large
\text{softmax}(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}, \quad \small \text{for } i = 1, \ldots, K.
$$
- or expanded as 
$$
\text{softmax}(\mathbf{z})

= \left(

  \frac{e^{z_1}}{\sum_{k=1}^K e^{z_k}}, \;

  \frac{e^{z_2}}{\sum_{k=1}^K e^{z_k}}, \;

  \dots, \;

  \frac{e^{z_K}}{\sum_{k=1}^K e^{z_k}}

\right).
$$


---

# 2 ML Basics
- 1950s - earliest neural net was Rosenblatt **perceptron** - used decision boundary (dividing line) to separate classes 
- late 1990s/2000s - AI arose from 2nd winter
	- thanks to incremental hardware improvements + larger datasets (internet usage growing)
	- Leo Breiman Random Forest algorithm (2001) addressed overfitting of decision trees 
- 2012 - more advanced neural networks (deeper) started outperforming other techniques 
	- AlexNet on ImageNet competition 
- ReLU activation function, despite its simplicity, was a breakthrough in machine learning
	- NNs prior to 2012 used smooth activations (tanh + sigmoid) - vanishing gradient problem 
	- making training deeper networks much harder
- increasing model size can vastly improve performance 
	- simple model can be improved just by increasing number of units/neurons 

![[Screenshot 2025-02-22 at 12.54.11 pm.webp| center | 600]]

## Gradient Descent 
- GD algo uses gradient of the loss function to iteratively update weights and bias of the model 
	- aiming to minimise the loss function 
	- i.e. where gradient becomes 0 
- flow of data from input to output through the computational graph constitutes the **forward pass**
	- **backprop**/backward pass = computation of gradients from output to input 
- process 
	1. initialise parameters - start with random values for $w_j, b$ 
	2. compute predictions/forward pass - for each training example, get predicted value
	3. compute gradient - calculate partial derivatives of loss w.r.t each weight and bias 
	4. update weights and bias in decreasing direction, using learning rate as step size 
	5. repeat until convergence 
## Autograd with `torch`
- torch looks after automatically differentiating for us, and applying this to the model
	- example below using the simpler Sequential API 
- Tensors are PyTorch’s core data structure
	- multi-dimensional arrays optimised for computation on both CPU and GPU
	- can also set precision settings when creating tensors 
		- 32 bit is default, but can reduce to 16 or 8 bit depending on machine 

```python
import numpy as np 
import torch 
import torch.nn as nn 
import torch.optim as optim 

# matrix w 12 rows, 2 columns
inputs = torch.tensor([
    [22, 25], [25, 35], [47, 80], [52, 95], [46, 82], [56, 90],
    [23, 27], [30, 50], [40, 60], [39, 57], [53, 95], [48, 88]
], dtype=torch.float32)

# labels w 12 components 
labels = torch.tensor([
    [0], [0], [1], [1], [1], [1], [0], [1], [1], [0], [1], [1]
], dtype=torch.float32)

model = nn.Sequential(
    nn.Linear(inputs.shape[1], 1),       # input layer 
    nn.Sigmoid()                         # activation w sigmoid 
)

optimizer = optim.SGD(
	model.parameters(), lr=0.001         # GD - uses model params + LR as inputs
)
criterion = nn.BCELoss()                 # binary cross-entropy loss
```

- PyTorch accumulates gradients in the .grad attribute of parameters
	- can access all trainable parameters via `model.parameters()`
	- now we can run the training loop 

```python
for step in range(500):
	optimizer.zero_grad()                        # clears grads at each step 
	loss = criterion(model(inputs), labels)      # calculates BCE loss 
	loss.backward()                              # calculates gradient + backprop
	optimizer.step()                             # updates param values by subtracting
```

- Backpropagation applies differentiation rules, particularly the chain rule
	- to compute gradients through deep composite functions - Torch does this under the hood 
		- accumulates gradients in the `.grad` attribute of parameters
	- backprop algo forms the backbone of neural network training

---

# 3 Language Modelling Basics 
- <mark style="background: #FFB8EBA6;">bag of words</mark> = one of oldest techniques to transform words into numeric form 
	- you have collection of docs, each doc becomes a feature vector 
	- you find all unique words in the corpus - becomes your **vocabulary** 
	- vectorise each doc, each dimensions represents word from vocab 
		- value indicates word's presence, absence or frequency in the doc 
		- known as **document-term matrix** 
- one problem with BoW is they are very sparse and inefficiently represented 
	- fails to capture token order or context, just literally counts word frequencies 
	- vocabulary expands considerably, increasing the computational cost of model training
	- BoW also unable to handle OOV words 
## Using a neural net on BoW
- recall, ***softmax transforms vector of logits into a discrete probability distribution*** 
	- ensuring the sum of all elements adds to 1 
	- example below shows softmax calculation


$$
\begin{array}{@{}l l l@{}}

% Row 1: Headings

\textbf{1.} \text{ Calculate } e^{z^k} \text{ for each logit} &

\textbf{2.} \text{ Sum these values} &

\textbf{3.} \text{ Use softmax to compute probabilities} \\[6pt]

  

% Row 2: Nested arrays for examples

\begin{array}{@{}l@{}}

e^{z^{(1)}} = e^{2.0} \approx 7.39\\

e^{z^{(2)}} = e^{1.0} \approx 2.72\\

e^{z^{(3)}} = e^{0.5} \approx 1.65

\end{array}

&

\begin{array}{@{}l@{}}

\sum_{j=1}^{3} e^{z_j} = 7.39 + 2.72 + 1.65 = 11.76

\end{array}

&

\begin{array}{@{}l@{}}

\mathrm{Pr}(\text{cinema}) = \frac{7.39}{11.76} \approx 0.63\\

\mathrm{Pr}(\text{music}) = \frac{2.72}{11.76} \approx 0.23\\

\mathrm{Pr}(\text{science}) = \frac{1.65}{11.76} \approx 0.14

\end{array}

\end{array}
$$

- cross-entropy loss measures how well predicted probabilities match true distribution 


>[!danger] COME BACK AND ADD NOTES HERE (PAGE 57)
> 

## PyTorch example 
- this time using module API (more versatile), creating a simple 2 layer network 
	- `{python}self.fc1` = fully connected 1st layer, maps input to 50 outputs
		- input has size `input_dim` - equal to vocab size
		- outputs are size `hidden_dim`
	- `{python}self.relu` = activation function to introduce non-linearity 
	- `{python}self.fc2` = 2nd dense layer, reduces 50 intermediate outputs to `output_dim`
		- where `output_dim` == number of unique labels to predict i.e. classes

```python
input_dim = len(vocabulary)
hidden_dim = 50
output_dim = num_classes

class SimpleClassifier(nn.Module):
	def __init__(self, input_dim, hidden_dim, output_dim):
		super()._init__()
		self.fc1 = nn.Linear(input_dim, hidden_dim)
		self.relu = nn.ReLU()
		self.fc2 = nn.Linear(hidden_dim, output_dim)

	def forward(self, x):          # x = 10,26
		x = self.fc1(x)            # transforms to 10,50
		x = self.relu(x)           # remains 10,50
		x = self.fc2(x)            # transforms to 10,3
		return x

model = SimpleClassifier(input_dim, hidden_dim, output_dim)

# example usage of forward pass 
# model(inputs)
```

- last line shows how you perform forward pass - by passing inputs into model via `model(input)`
	- notice, no explicit softmax layer - torch automatically uses softmax with cross entropy loss under the hood 
	- now we setup training loop 

```python
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

for step in range(3000):
	optimizer.zero_grad()
	loss = criterion(model(vectors), labels)
	loss.backward()
	optimizer.step()
```

- to predict on new inputs (e.g. inference), we do a few things
	- using `{python}torch.no_grad()` disables default gradient tracking 
		- only needed for training, not for testing/inference 
	- `{python}outputs` created by processing all inputs simultaneously - parallel efficiency 
	- `{python}torch.argmax` identifies highest logit's index - corresponding to predicted class 
		- adding 1 to shift to account for the 0 based indexing

```python
with torch.no_grad():
	outputs = model(new_doc_vectors)
	predicted_ids = torch.argmax(outputs, dim=1) + 1
```

## Word Embeddings
- solve for many of the problems of BoW approaches 
	- maps semantically similar words to similar vector representations 
		- which can be exhibited by high cosine similarities 
	- representing words as dense vectors instead of sparse one-hot vectors 
- Word2Vec in 2012 was first breakthrough here, widely used word embedding algorithm with 2 variants 
	- Skip-grams = word sequences w 1 word omitted - can then predict word using neighbouring words
		- e.g. `the big red ` `{python}[MASK]` ` chased the deer` 
		- or alternatively, calculate neighbour words given a context word 
	- captures semantic similarity when words occur in similar contexts, even without direct co-occurrence
	- trains a small feed-forward network to predict the context words that tend to co-occur with a given “center” word
		- skipgram model uses cross entropy as loss function 
		- **once training done, output layer is discarded - embedding layer serves as the new output layer** 
- other variants e.g. GloVe + FastText vary on computing this
	- via capturing global co-occurrence statistics or subword information for more robust embeddings 
- advantages of word embeddings
	- dimensionality reduction - preserves much more useful info than BoW 
	- semantic similarity as a functionality is also very useful 

## Byte-Pair Encoding (BPE)
- tokenization algorithm that addresses the challenges of handling out-of-vocabulary words by breaking words into smaller units called subwords
	- initially a data compressing technique 
	- merges most frequent symbols pairs (characters or subwords) into new subword units 
	- continues to evolve until vocab hits target size 
- BPE algorithm 
	- initialise - use text corpus, split each word into characters 
		- initial vocab = all unique characters in corpus 
	- iterative merging 
		- count adjacent symbol pairs - each character == symbol, count every pair of adjacent symbols 
		- select most frequent symbol pair 
		- merge the selected pair - replacing all occurrences w new single merged symbol 
		- update vocabulary - add new merged symbol to vocab, keeping original characters
	- repeat merging until vocab reaches desired size 

```python
from collections import defaultdict

def initialize_vocabulary(corpus):
	vocabulary = defaultdict(int)
	charset = set()
	for word in corpus:
		word_with_marker = '_' + word 
		characters = list(word_with_marker) 
		charset.update(characters) 
		tokenized_word = ' '.join(characters)
		vocabulary[tokenized_word] += 1
	return vocabulary, charset
```

```python
def get_pair_counts(vocabulary):
	pair_counts = defaultdict(int)
	for tokenized_word, count in vocabulary.items():
		tokens = tokenized_word.split() 
		for i in range(len(tokens) - 1):
			pair = (tokens[i], tokens[i + 1]) 
			pair_counts[pair] += count 
	return pair_counts
```

```python
def merge_pair(vocabulary, pair):
	new_vocabulary = {}
	bigram = re.escape(' '.join(pair)) 
	pattern = re.compile(r"(?<!\s)" + bigram + r"(?i\s)") 
	for tokenized_word, count in vocabulary.items():
		new_tokenized_word = pattern.sub("".join(pair), tokenized_word) 
		new_vocabulary[new_tokenized_word] = count 
	return new_vocabulary
```

```python
def byte_pair_encoding(corpus, vocab_size):
	vocabulary, charset = initialize_vocabulary(corpus)
	merges = []
	tokens = set(charset)
	while len(tokens) < vocab_size: 
		pair_counts = get_pair_counts(vocabulary)
		if not pair_counts: 
			break
		most_frequent_pair = max(pair_counts, key=pair_counts.get) 
		merges.append(most_frequent_pair)
		vocabulary = merge_pair(vocabulary, most_frequent_pair)
		new_token = ''.join(most_frequent_pair) 
		tokens.add(new_token) 
	return vocabulary, merges, charset, tokens
```

- subword tokenization is not ideal for all languages 
	- e.g. Chinese has no spaces, should be done at character level
	- code also uses spaces for indentation smartly 

## Language models 
- <mark style="background: #FFB8EBA6;">language models</mark> predict next token in a sequence by estimating conditional probabilities based on previous tokens 
	- <mark style="background: #FFB8EBA6;">conditional probability</mark> quantifies the likelihood of one event occurring given that another has already occurred
	- sequence often known as input sequence, context or prompt 
- for a sequence $s$ of $L$ tokens $t_1, t_2, ...,t_L$ a language model computes:
	- where $\Pr$ = conditional probability distribution over vocab for next token 
$$
\Large \Pr(t = t_{L + 1} | s = (t_1, t_2, ..., t_L))
$$
equivalently represented/simplified as 
$$
\Large \Pr(t = t_{L + 1} | t_1, t_2, ..., t_L) \ \text{ or } \ \Pr(t = t_{L + 1} | s)
$$
- language models known as <span style="color:rgb(255, 0, 247)">autoregressive</span> language model, or <span style="color:rgb(255, 0, 247)">causal language model</span>
	- autoregression = predicting an element in a sequence using only it's predecessors 
	- another type of language model = <span style="color:rgb(255, 0, 247)">masked language model</span>
		- e.g. BERT, predicts intentionally masked tokens within sequences
		- using both directions to predict the missing word (bidirectional)
		- particularly suited to classification tasks 

## Evaluating LMs
- <mark style="background: #FFB8EBA6;">perplexity</mark> = measures how well a model predicts text 
	- lower = better/more confident model
	- If a language model assigns equal probability to every token in a vocabulary of size $V$, its perplexity equals $V$
	- defined as exponential of the average <span style="color:rgb(255, 0, 247)">negative log-likelihood</span> per token in test set 
$$\textbf{Perplexity:} \text{ sum of log-probs version}$$

$$
\Large \text{Perplexity}(\mathcal{D},k) 

= \exp\!\Bigl(

  -\frac{1}{D} 

   \sum_{i=1}^{D} 

     \log \Pr\!\bigl(

       t_i \mid 

       t_{\max(1, i-k)}, 

       \ldots, 

       t_{i-1}

     \bigr)

\Bigr).
$$
- where:
	- $\mathcal{D}$ = test set, $D$ = number of tokens in it 
	- $t_i$ = $i$'th token 
	- $\Pr\!\bigl(t_i \mid t_{\max(1, i-k)}, \ldots, t_{i-1} \bigr)$ = probability model assigns to token $i$ 
	- $k$ = preceding context window size 
	- $\exp$ is equivalent to $e$ - Euler's number 
- NLL (negative log-likelihood) = negative logarithm of probabilities the model assigns 
	- e.g. `"Language models are ..."` the next word `"cool"` gets probability of 0.77
	- NLL would be $-\log(0.77)$ 

> [!NOTE] Negative Log-Likelihood (NLL)
> - the likelihood is basically the probability the model assigns it 
> 	- i.e. likelihood == probability e.g. $p$
> - it is negative since the probability $p$ is usually between 0 and 1 
> 	- and log of numbers between 0 and 1 are negative 
> - so taking **negative of that log likelihood transforms it to always be positive** 

- NLL serves 2 purposes 
	- acts as loss function during training to learn better probability distributions 
	- used in perplexity to evaluate how well models predict text 
- how Perplexity can also be understood differently 
	- can be intuitively understood through geometric mean formulation 
		- geometric mean of a set of numbers = $D$'th root of their product 
		- perplexity = geometric mean of the inverse probabilities 
	- **exponential/sum of log-probs form is computationally more convenient**
		- since it transforms products into sums through the logarithm, making calculations more numerically stable

$$\textbf{Perplexity:} \text{ product of inverse probs version}$$
$$
\text{Perplexity}(D,k)

= \biggl(

  \prod_{i=1}^{D}

    \frac{1}{\Pr\!\bigl(

      t_i \mid 

      t_{\max(1, i-k)}, 

      \dots, 

      t_{i-1}

    \bigr)}

\biggr)^{\tfrac{1}{D}}.
$$
### Calculating Perplexity (by hand)
- first find conditional probabilities of each token 
$$
\begin{array}{l@{\quad}c@{\quad}r}

\Pr(\text{We}) & = & 0.10\\

\Pr(\text{are} \mid \text{We}) & = & 0.20\\

\Pr(\text{evaluating} \mid \text{We}, \text{are}) & = & 0.05\\

\Pr(\text{a} \mid \text{We}, \text{are}, \text{evaluating}) & = & 0.50\\

\Pr(\text{language} \mid \text{are}, \text{evaluating}, \text{a}) & = & 0.30\\

\Pr(\text{model} \mid \text{evaluating}, \text{a}, \text{language}) & = & 0.40\\

\Pr(\text{for} \mid \text{a}, \text{language}, \text{model}) & = & 0.15\\

\Pr(\text{English} \mid \text{language}, \text{model}, \text{for}) & = & 0.25

\end{array}
$$
- using these probabilities, compute NLL for each token 
$$
\begin{array}{l@{\quad}c@{\quad}r}
-\log P(\text{We}) 
  & = & -\log(0.10) \approx 2.30\\
-\log P(\text{are}\mid \text{We}) 
  & = & -\log(0.20) \approx 1.61\\
-\log P(\text{evaluating}\mid \text{We}, \text{are}) 
  & = & -\log(0.05) \approx 3.00\\
-\log P(\text{a}\mid \text{We}, \text{are}, \text{evaluating}) 
  & = & -\log(0.50) \approx 0.69\\
-\log P(\text{language}\mid \text{are}, \text{evaluating}, \text{a}) 
  & = & -\log(0.30) \approx 1.20\\
-\log P(\text{model}\mid \text{evaluating}, \text{a}, \text{language}) 
  & = & -\log(0.40) \approx 0.92\\
-\log P(\text{for}\mid \text{a}, \text{language}, \text{model}) 
  & = & -\log(0.15) \approx 1.90\\
-\log P(\text{English}\mid \text{language}, \text{model}, \text{for}) 
  & = & -\log(0.25) \approx 1.39
\end{array}
$$
- next, sum the values and divide by number of words (8) to get average 
$$
\frac{(2.30 + 1.61 + 3.00 + 0.69 + 1.20 + 0.92 + 1.90 + 1.39)}{8} \approx 1.63
$$
- finally, exponentiate the average NLL to get perplexity 
$$
e^{1.63} \approx 5.10
$$
- model’s perplexity on this text, using a 3-word context, is about 5.10
	- means on average, model acts as if it selects from ~5 equally likely options for each prediction 
### Perplexity (in Python)
- first need `get_probability` function to return probability of our next token 
	- `context_n` matches n-gram counts 
	- function retrieves token counts, if no match found, backs off to lower-order n-grams, then finally unigrams 
	- `total` is the sum of counts for tokens in the context i.e. the denominator 

```python
def get_probability(self, token, context):
    for i in range(self.n, -1, -1):
        if len(context) >= i:
            context_n = tuple(context[-i:])
            counts = self.ngram_counts[i].get(context_n, {})
            if counts:
                total = sum(counts.values())
                count = counts.get(token, 0)
                if count > 0:
                    return count / total
                # Fallback to unigram
                unigram_counts = self.ngram_counts[0].get((), {})
                count = unigram_counts.get(token, 0)
                V = len(unigram_counts)
                return (count + 1) / (self.total_unigrams + V)
    # If no context-based counts found, also fall back to unigram
    unigram_counts = self.ngram_counts[0].get((), {})
    count = unigram_counts.get(token, 0)
    V = len(unigram_counts)
    return (count + 1) / (self.total_unigrams + V)
```

```python
def compute_perplexity(model, tokens, context_size):
	if not tokens:
		return float('inf')
	total_log_likelihood = 0
	num_tokens = len(tokens)
	for i in range(num_tokens): 
		context_start = max(0, i - context_size)
		context = tuple(tokens[context_start:i]) 
		word = tokens[i]
		probability = model.get_probability(word, context)
		total_log_likelihood += math.log(probability) 
	average_log_likelihood = total_log_likelihood / num_tokens
	perplexity = math.exp(-average_log_likelihood) 
	return perplexity
```



---

# 2 Recurrent Neural Nets 

---

# 3 Transformer 

---

# 4 Large Language Models