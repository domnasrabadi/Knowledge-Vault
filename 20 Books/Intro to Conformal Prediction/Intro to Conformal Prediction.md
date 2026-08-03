---
type: book
status: structured
quality:
topics: [model-calibration, data-science]
source: ""
created: 2025-02-09
published:
author: ""
flashcards: none
updated: 2025-02-23
---
Book by Cristoph Molnar. #books

- [[#1 Intro to Conformal Prediction|1 Intro to Conformal Prediction]]
	- [[#1 Intro to Conformal Prediction#1.1 Why Uncertainty Quantification is Needed|1.1 Why Uncertainty Quantification is Needed]]
	- [[#1 Intro to Conformal Prediction#1.2 Common Approaches to Uncertainty Estimation|1.2 Common Approaches to Uncertainty Estimation]]
	- [[#1 Intro to Conformal Prediction#1.3 Why Conformal Prediction|1.3 Why Conformal Prediction]]
- [[#2 Conformal Prediction in Python|2 Conformal Prediction in Python]]
	- [[#2 Conformal Prediction in Python#2.1 Finding the Threshold|2.1 Finding the Threshold]]
	- [[#2 Conformal Prediction in Python#2.2 Python Example|2.2 Python Example]]
	- [[#2 Conformal Prediction in Python#2.3 Using the Threshold for New Data|2.3 Using the Threshold for New Data]]
	- [[#2 Conformal Prediction in Python#2.4 MAPIE library|2.4 MAPIE library]]
- [[#3 Full Recipe to Conformal Prediction|3 Full Recipe to Conformal Prediction]]
	- [[#3 Full Recipe to Conformal Prediction#3.1 Step 1: Training|3.1 Step 1: Training]]
	- [[#3 Full Recipe to Conformal Prediction#3.2 Step 2: Calibration|3.2 Step 2: Calibration]]
	- [[#3 Full Recipe to Conformal Prediction#3.3 Step 3: Prediction|3.3 Step 3: Prediction]]
- [[#4 Full Example by Hand|4 Full Example by Hand]]
- [[#5 Intuition behind Conformal Prediction|5 Intuition behind Conformal Prediction]]
	- [[#5 Intuition behind Conformal Prediction#5.1 Data Splits w Conformal Prediction|5.1 Data Splits w Conformal Prediction]]
	- [[#5 Intuition behind Conformal Prediction#5.2 Interpreting prediction regions & coverage|5.2 Interpreting prediction regions & coverage]]
- [[#6 Classification|6 Classification]]
	- [[#6 Classification#6.1 Adaptive Classification Methods|6.1 Adaptive Classification Methods]]
- [[#7 Regression|7 Regression]]
- [[#8 Parting notes|8 Parting notes]]

# 1 Intro to Conformal Prediction
- prerequisite for trusting ML predictions is usncertainty quantification
	- most methods have no guarantee on working w new data
- conformal prediction works well since:
	- guaranteed coverage = prediction regions generated come w coverage guarantees of true outcome 
	- easy to use can be implemented in just few lines of code 
	- model-agnostic 
	- distribution free = makes no distributional assumptions
	- no retraining required 
	- broad application = works for classification, regression, time series etc 
- these notes are for any DS who wants to learn how to quantify uncertainty w conformal prediction
	- CP often not well known since math is complex + lives mostly in academic sphere
## 1.1 Why Uncertainty Quantification is Needed
- to fully trust ML preds, need to know how certain/confident those predictions are 
	- very important for decision making based on model outputs 
	- rule of thumb = **need uncertainty quantification whenever a point prediction isn't informative enough** 
- uncertainty has many sources 
	- ❓training using a random sample of data 
	- ❓models often also have non-deterministic aspects e.g. seeds, initialisation 
	- ❓uncertainty is worse when training datasets are small 
	- ❓hyperparameter tuning, model selection, feature selection 
		- all decisions here based on estimating from random sample of data 
	- ❓data not always perfectly measured 
		- missing values
		- human labellers can disagree, true class can be up for debate 
- models don't allow us to distinguish good predictions from wild guesses
	- both are output the same from the model 
![[Screenshot 2025-02-09 at 4.18.20 pm.webp| center | 500]]

## 1.2 Common Approaches to Uncertainty Estimation 
- there are a number of ways to estimate probabilities - but these have problems
	- <span style="color:rgb(255, 0, 247)">looking at class probabilities</span> - usually not calibrated 
		- e.g. if probability scores are calibrated - for all classifications with a score of 90%
		- we should find true class 9 times out of 10 
	- <span style="color:rgb(255, 0, 247)">bayesian posterior predictive intervals</span> - intervals based on distributional assumptions for the prior + distribution family chosen 
	- <span style="color:rgb(255, 0, 247)">bootstrapping</span> - refitted model with sampled data, but known to underestimate true variance 
		- especially worse for small samples
- none of these come with any reasonable guarantee they cover the true outcome 
	- *Niculescu-Mizil and Caruana 2005; Lambrou et al. 2012; Johansson and Gabrielsson 2019; Dewolf et al. 2022*
## 1.3 Why Conformal Prediction
- CP fills these gaps 
	- <mark style="background: #FFB8EBA6;">conformal prediction</mark> = set of methods that take an uncertainty score and turn it into a rigorous score (i.e. guarantees it covers the true outcome)
- CP changes what a prediction looks like
	- turns point predictions into prediction regions 
	- for multi-class classification - turns class output into a set of classes 

![[Screenshot 2025-02-09 at 4.23.50 pm.webp| center | 400]]

- CP has many advantages that make it a valuable tool
	- ✅ distribution free = no assumptions about data distribution 
	- ✅ model agnostic = can be applied to any predictive model
	- ✅ coverage guarantee = resulting prediction sets come w guarantees of covering true outcome w a certain probability 
- only assumption of CP = exchangeability 
	- data used for calibration should be similar to data you will quantify uncertainty for 
# 2 Conformal Prediction in Python
- for CP, you usually split your data a little differently e.g.
	- 70% for training - `X_train`, `y_train`
	- 10% for model evaluation - `X_test`, `y_test`
	- 10% for calibration - `X_calib`, `y_calib`
	- 10% for conformal prediction step + evaluating the conformal predictor - `X_new`, `y_new`
```python
# Split of training data
X_train, X_rest1, y_train, y_rest1 = train_test_split(
X, y, train_size=10000, random_state=2
)
# From the remaining data, split of test data
X_test, X_rest2, y_test, y_rest2 = train_test_split(
X_rest1, y_rest1, train_size=1000, random_state=42
)
# Split remaining into calibration and "new" data
X_calib, X_new, y_calib, y_new = train_test_split(
X_rest2, y_rest2, train_size=1000, random_state=42
```

- CP uses model probabilities to construct a measure of uncertainty 
	- $s_i$ = measures how unusual a suggested outcome $y$ seems given the model output for $x_i$
		- $s_i$ score = <mark style="background: #FFB8EBA6;">non-conformity score</mark>
	- so for each new data point, you consider each possible label $y$
		- and calculate it's non-conformity score
		- hence lower scores == more confident in prediction
		- higher scores == more uncertain

$$
\large
\begin{gather}
\textbf{Non-Conformity Score} \text{ for a given instance} \\ \ \\ 
s_{i}= 1 - (\text{model's probability for the true class}) \\ \ \\ 
\small{\text{alternatively represented as}} \\ \ \\
s_{i}= 1 - f(x_i)[y_{i}] \\ \small{\text{or...}} \\
\alpha(x_{i}) = 1 - p(y_{i}\mid x_i)
\end{gather}
$$

- then compare these scores to a threshold 
	- only labels with score below this threshold are **conformal**
	- and then included in the prediction set
- threshold is chosen so that it covers a desired percentage (e.g., 95%) of the calibration data
	- i.e. for 95% of the calibration examples, true label's nonconformity score is below this $\hat{q}$
	- then applying it to new data, gives you a prediction set with 95% probability it contains the true label
## 2.1 Finding the Threshold 
1. <span style="color:rgb(255, 0, 247)">Use Calibration Data</span>: dataset not used for training the model 
2. <span style="color:rgb(255, 0, 247)">Compute Nonconformity Scores</span>: using the formula 
```python
scores = 1 - prob_true_class
```
3. <span style="color:rgb(255, 0, 247)">Sort Scores</span>: from lowest (most conforming/certain) to highest (least conforming, most uncertain)
4. <span style="color:rgb(255, 0, 247)">Choose Threshold as a Quantile</span>: 
	- 4.1. *choose target coverage*
		- if you want prediction sets to cover 95% of true labels, you select threshold $\hat{q}$ at 95% quantile
	- 4.2. *in a finite sample, you also apply a slight correction* 
		- simply an adjustment you make to account for the fact that you only have a limited amount of data
		- e.g. for $n$ calibration examples, quantile level calculated as: 
			- where $\alpha = 0.05$ for 95% coverage

$$
\large
q_{level} = \frac{\lceil (n + 1) \times (1 - \alpha) \rceil}{n}
$$
- so for $n = 1000$, we get

$$
q_{level} = \frac{\lceil 1001 \times 0.95 \rceil}{1000} = \frac{951}{1000} = \mathbf{0.951}
$$
- relevant when your calibration dataset is small 
	- e.g. $\alpha = 0.05$ and $n_{cal} = 1000$ then $\hat{q} = 0.951$ 
	- e.g. $\alpha = 0.05$ and $n_{cal} = 50$ then $\hat{q} = 0.97$ 
- this means you set $\hat{q}$ at 95.1% quantile
	- for the calibration nonconformity scores
	- ensures at least 95% of scores below this threshold
> [!NOTE] recall, <mark style="background: #FFB8EBA6;">quantile</mark> = general term for any value that divides dataset into intervals
> e.g. percentile = 1%... decile = 10%... quartile = 25%... quantile = generalisable interval e.g. 95% quantile
- note: later below, we show how to use this w new data

## 2.2 Python Example
- Compute scores 
```python
# Size of calibration data
n = len(X_calib)

# Get the probability predictions
predictions = model.predict_proba(X_calib)

# We only need the probability for the true class
prob_true_class = predictions[np.arange(n), y_calib]

# Turn into uncertainty score (larger means more uncertain)
scores = 1 - prob_true_class
```
- Find the Cut-Off (Threshold)
```python
# Setting the alpha so that we get 95% prediction sets
alpha = 0.05

# Calculate the quantile level with finite sample correction
q_level = np.ceil((n+1) * (1 - alpha)) / n

# Get the threshold from the nonconformity scores
qhat = np.quantile(scores, q_level, method='higher')
```
- Visualising the cutoff
```python
import matplotlib.pyplot as plt

# Get the "probabilities" from the model
predictions = model.predict_proba(X_calib)

# Get for each instance the actual probability of ground truth
prob_for_true_class = predictions[np.arange(len(y_calib)),y_calib]

# Create a histogram
plt.hist(1 - prob_for_true_class, bins=30, range=(0, 1))
plt.xlabel("1 - s(y,x)"); plt.ylabel("Frequency"); plt.show()
```

![[Screenshot 2025-02-09 at 5.49.48 pm.webp| center | 500]]

## 2.3 Using the Threshold for New Data
- once you have found the threshold/cutoff $\hat{q}$ - you can now get prediction sets
	- <mark style="background: #FFB8EBA6;">prediction set</mark> = set of one or more classes for each instance 
	- to generate prediction sets for a new data point, you need to combine all classes below $\hat{q}$ into a set
```python
prediction_sets = (1 - model.predict_proba(X_new) <= qhat)

for i in range(number_instances): 
	print(le.classes_[prediction_sets[i]])
```

- on average, the prediction sets cover the true class with a probability of 95%
	- this is the guarantee we get from the conformal procedure
	- key point = "on average"
## 2.4 MAPIE library
- instead of coding from scratch we can use MAPIE - python library for CP 
	- MAPIE objects have similar style to `{python}sklearn` models e.g. `.fit()` and `.predict()`
	- basically a wrapper around our original model
```python
from mapie.classification import MapieClassifier

cp = MapieClassifier(estimator=model, cv="prefit", method="score")
cp.fit(X_calib, y_calib)

y_pred, y_set = cp.predict(X_new, alpha=0.05)
y_set = np.squeeze(y_set)
```
- using the predict method, we get 2 outputs
	- usual prediction i.e. `y_pred`
	- and prediction sets `y_set`
- relationship between $\alpha$ and prediction set sizes 
	- as you make $\alpha$ smaller i.e. want more certainty - you will get larger prediction sets
		- because the lower the $\alpha$, the more often the sets have to cover the true parameter
		- $\alpha$ = 0.0 will be pointless - just includes all classes for every set
	- so there is tradeoff between set size + coverage

> [!NOTE] **coverage** = percentage of prediction sets that contain the true label

# 3 Full Recipe to Conformal Prediction 
- the only difference between using CP for regression vs classification is: 
	- how to calculate nonconformity score
	- <span style="color:rgb(255, 0, 247)">prediction sets</span> (classification) vs <span style="color:rgb(255, 0, 247)">prediction intervals</span> (regression)
- 3 general steps in CP 
## 3.1 Step 1: Training
- split data into training, test, calibration, holdout calibration 
- train model on training data 
## 3.2 Step 2: Calibration
- compute uncertainty scores (aka nonconformity scores) for calibration data 
- sort scores from certain to uncertain 
- choose confidence level (aka coverage) - $\alpha = 0.1$ == 90% coverage
- find $\hat{q}$ where $1 - \alpha$ (with finite sample correction) of nonconformity scores are smaller 
## 3.3 Step 3: Prediction 
- compute nonconformity scores for new data 
- pick all $y$'s that score below $\hat{q}$ $\rightarrow$ these form your prediction set/interval
# 4 Full Example by Hand
1. <span style="color:rgb(255, 136, 0)">Train Classifier</span>
	- first train your classifier e.g. logistic regression, neural net, random forest 
	- as long as for a given input $x$, model predicts a probability $p(x)$ for class 1
2. <span style="color:rgb(255, 136, 0)">Compute nonconformity scores on calibration set</span>
	- set aside calibration set + compute nonconformity scores e.g. $\alpha(x_{i}) = 1 - p(y_{i}\mid x_i)$
		- where $p(y_i \mid x_i)$ = predicted probability for correct label
		- $\alpha(x_i)$ is high when model is uncertain 
	- example: model predicts the following
		- $p(1 \mid x_1) = 0.95 \rightarrow$ then $\alpha(x_1) = 1 - 0.95 \rightarrow = 0.05$ (very confident)
		- $p(1 \mid x_2) = 0.55 \rightarrow$ then $\alpha(x_2) = 1 - 0.55 \rightarrow = 0.45$ (less confident)
		- $p(0 \mid x_3) = 0.60 \rightarrow$ then $\alpha(x_3) = 1 - 0.60 \rightarrow = 0.40$ (uncertain)
	- then sort all scores in ascending order
3. <span style="color:rgb(255, 136, 0)">Select a quantile for coverage</span>
	- choose a confidence level $1 - \alpha$ e.g. 90%
	- threshold $\hat{q}$ set at the $1 - \alpha^{th}$ quantile of the sorted scores 
	- example: sorted scores and threshold 
		- sorted scores are $[0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95]$
		- for 90% confidence, $\hat{q}$ would be 0.85
4. <span style="color:rgb(255, 136, 0)">Make predictions on new data</span>
	- for a new test sample $x_{new}$, **compute nonconformity scores for both labels** $\{0, 1\}$
		- $\alpha_0 = 1 - p(0 \mid x_{new})$
		- $\alpha_1 = 1 - p(1 \mid x_{new})$
	- if any/either are below your threshold (here, $\hat{q}$ = 0.85), then include in prediction set
		- if $\alpha_0 \le 0.85 \rightarrow$ include **class 0 in prediction set**
		- if $\alpha_1 \le 0.85 \rightarrow$ include **class 1 in prediction set**
	- example: assigning prediction sets to new data points
		- $p(1 \mid x_{new}) = 0.90$ 
			- $\longrightarrow \alpha_1 = 1 - 0.90 \longrightarrow 0.10 \le 0.85$
			- $\longrightarrow$ **include class 1**
		-  $p(0 \mid x_{new}) = 0.50$ 
			- $\longrightarrow \alpha_1 = 1 - 0.50 \longrightarrow 0.50 \le 0.85$
			- $\longrightarrow$ **include class 0**
		-  $p(1 \mid x_{new}) = 0.40$ 
			- $\longrightarrow \alpha_1 = 1 - 0.40 \longrightarrow 0.60 \le 0.85$
			- $\longrightarrow$ **include class 1**
5. <span style="color:rgb(255, 136, 0)">Interpret prediction sets</span>
	- **final output is a prediction set, not a single label**
		- if set is `{1}` $\rightarrow$ model is fairly confident in class 1
		- if set is `{0, 1}` $\rightarrow$ model is uncertain and assigns both classes
		- if set is `{0}` $\rightarrow$ model is fairly confident in class 0

---

# 5 Intuition behind Conformal Prediction
- recall the steps
	- **separate calibration set data**
		- using training data would bias nonconformity scores - coverage would always be lower than true value
		- also assumes exchangeability = new data must follow same distribution to calibration data 
	- **calculate non-conformity scores**
	- **sort data from lowest to highest** (certain to uncertain)
		- rely on this ordering of the images to divide the images into certain (or conformal) and uncertain
	- **calculate threshold based on desired coverage** 
![[Screenshot 2025-02-10 at 6.26.14 pm.webp| center | 500 ]]
- notice, we only calculate threshold based on coverage of positive labels
	- we don't explicitly consider incorrect classifications when choosing $\hat{q}$ 
	- however, wrong classes are naturally filtered out since their probabilities are much lower == higher nonconformity scores
- conformal prediction for new data
	- after the above steps, for a new data point $\rightarrow$ we check all possible classes
		- i.e. **compute the non-conformity score for each class**
		- **and keep the classes where the score < $\hat{q}$** 
	- all scores < $\hat{q}$ are conformal with scores we observed in the calibration data + we consider certain

![[Screenshot 2025-02-10 at 6.35.28 pm.webp| center | 500]]

- a good model should have low probabilities for the wrong classes
	- therefore their nonconformity scores likely > $\hat{q}$ 
## 5.1 Data Splits w Conformal Prediction
- in ML, you don't always just use `train` vs `test`, common to split using 
	- k-fold cross validation 
	- bootstrapping
	- leave-one-out aka jackknife 
![[Screenshot 2025-02-10 at 6.42.40 pm.webp| center | 400]]

- for K-Fold CV
	- split data into k folds
	- take k-1 folds + train model + compute non-conformity scores for the remaining 1 fold 
	- repeat k-1 times - resulting in scores for all the data
	- compute quantile $\hat{q}$ like before
- for LOO/jackknife 
	- train $n$ models, each with $n-1$ data points
		- $n$ = number of data points in `train` + `calibration`
	- then sort + compute threshold 
- which to choose? 
	- <span style="color:rgb(255, 0, 247)">single split</span>: cheapest, higher variance, ignores variance from model refits, preferable for slow model fits
	- <span style="color:rgb(255, 0, 247)">CV</span>: tradeoff between single split and LOO
	- <span style="color:rgb(255, 0, 247)">LOO</span>: expensive, smaller sets, preferable for smaller datasets or fast models

```python
# single split 
cp = MapieRegressor(model, cv="prefit")

# K Fold CV 
cp = MapieRegressor(model, cv=10)

cp.fit(x_calib, y_calib)
```

## 5.2 Interpreting prediction regions & coverage
- recall, classification CP gives prediction sets, regression gives prediction intervals
- nerdy statistics disclaimer
	- the true value is considered fixed, but the prediction region is the random variable 
	- it would be wrong to say that the true value “falls” into the interval
	- because the true value is fixed but unknown
# 6 Classification 
- all methods below work regardless of input feature data types 
	- only requirement is model must output probability score per class 
- recall, CP outputs prediction sets, not single labels 
	- look at average size of prediction set 
		- smaller == better 
		- as long as the coverage is guaranteed 
![[Screenshot 2025-02-10 at 7.11.38 pm.webp| center | 400]]

- in `{python}mapie`, we can use:
	- `MapieClassifier` to conformalize our classification model
	- `classification_coverage_score` and `classification_mean_width_score` to evaluate resulting prediction sets 
```python
from mapie.classification import MapieClassifier
from mapie.metrics import classification_coverage_score
from mapie.metrics import classification_mean_width_score

# 7 Initialize the MapieClassifier
mapie_score = MapieClassifier(model, cv="prefit", method="naive")
# Calibration step
mapie_score.fit(X_train, y_train)
# Prediction step
y_pred, y_set = mapie_score.predict(X_new, alpha=0.05)
# Removing the alpha-dimension
y_set = np.squeeze(y_set)

cov = classification_coverage_score(y_new, y_set)
setsize = classification_mean_width_score(y_set)
print('Coverage: {:.2%}'.format(cov))
print('Avg. set size: {:.2f}'.format(setsize))
# Coverage: 90.32% 
# Avg. set size: 1.41
```
- once you have $\hat{q}$, can use it to create prediction sets for new data
	- get a new sample $x_{new}$
	- compute $s(y, x_{new})$ for all classes $y$
		- compute preds on calibration data, keep only probabilities for true classes
		- compute scores and sort 
	- pick all classes $y$ where $s(y, x_{new}) <= \hat{q}$
- now we have our prediction sets with the following marginal coverage guarantee
$$
\Large \textcolor{red}{1 - \alpha} \le \textcolor{green}{P(Y_{new} \in C(X_{new})} \le \textcolor{blue}{1 - \alpha + \frac{1}{n_{cal} + 1}}
$$
- where 
	- $\textcolor{red}{1 - \alpha}$ = lower bound
	- $\textcolor{green}{P(Y_{new} \in C(X_{new})}$ = probability that true class is within coverage
	- $\textcolor{blue}{1 - \alpha + \frac{1}{n_{cal} + 1}}$ = upper bound
- one problem here is this method lacks adaptivity 
	- i.e. the score is not adaptive to the difficulty of each classification (i.e. each data point or each of the classes)
		- where some samples or classes might just be harder for model to predict correctly 
	- instead the method above just guarantees for coverage **on average** - known as <mark style="background: #FFB8EBA6;">marginal coverage</mark>
		- but it very well might be that coverage for subgroups is different 
	- if we also want coverage for subgroups of data - then we need <mark style="background: #FFB8EBA6;">conditional coverage</mark>

> [!NOTE] conformal prediction algorithm is adaptive if it not only achieves marginal coverage, but also (approximately) conditional coverage

## 6.1 Adaptive Classification Methods
- Adaptive Prediction Sets (APS) for conditional coverage
	- APS uses a different non-conformity score
	- idea is to add up the probabilities, starting with the largest, down to the true class
	- has 3 options for how to use it - TLDR use "randomised" option
```python
# For the randomized option, the classifier draws random numbers - use random_state for reproducibility
mapie_score = MapieClassifier(
	model, 
	cv="prefit",
	method="cumulated_score",
	random_state=1)

mapie_score.fit(X_calib, y_calib)
```
- Top-K method for fixed set sizes 
	- follows the same conformal classification recipe as APS and the score method
		- but uses a different non-conformity score
	- Top-k uses only the rank of the true class instead of the probability outcome
		- higher the rank of the true class, the less certain the model classification was
- Regularised APS (RAPS) for small sets 
	- APS method tends to produce rather large prediction sets, especially if there are more than a handful of possible classes
		- RAPS fixes this via regularisation 
		- introduces a regularisation term that penalises the inclusion of too many classes
- Group balanced CP 
	- APS and RAPS help conditional coverage but don't guarantee, instead we use Group-Balance CP
		- divide the data into groups and perform the conformal prediction separately for each group
	- requires you know groups at inference time
		- and now you need to split calibration data by groups (this is the cost of doing it)
- Class-Conditional APS (CCAPS) for coverage by class
	- an approach to guarantee 1 − $\alpha$ coverage of prediction sets per class
		- main problem of Group-Balanced CP is we do not know true classes at inference time 
	- solution = apply all resulting class-wise conformal predictors, and the prediction set is the union of all conformal classes.
# 7 Regression 
- regression outputs are also point predictions 
	- can turn this into an interval with guarantee of covering true outcome for new data 
		- not groundbreaking, since you can use quantile regression but that has no guarantees
	- 2 strategies to do so 
		- start from point predictions
		- start from (non-conformal) intervals outputted by quantile regression 
- **main difference** between classification and regression is the **non-conformity score** we use
	- otherwise it is the same process
		- Split the data into training and calibration 
		- Train the model on the training data 
		- Compute non-conformity scores 
		- Find threshold $\hat{q}$
		- Create prediction intervals for new data

$$
\begin{gather}
\Large\textbf{Nonconformity Scores for Regression} \\ \ \\ 
\Large s(y, x) = |y - \hat{f}(x)|
\end{gather}
$$

- unfortunately all prediction intervals have the same size 
	- can get adaptive intervals using:
		- K-Fold CV or LOO (jackknife)
		- adaptive conformal regression - use standardised residuals (but needs 2nd model) 

# 8 Parting notes
- choosing calibration data size
	- 1000 is enough
	- anything below, rule = more is better 
- how $\alpha$ affects size prediction regions
	- small $\alpha$ = larger regions
	- big $\alpha$ = smaller regions


