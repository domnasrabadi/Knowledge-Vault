---
type: book
status: structured
quality:
topics: [data-science]
source: ""
created: 2025-02-23
published:
author: ""
flashcards: none
updated: 2025-03-05
---
#books
![[Screenshot 2025-02-23 at 2.59.50 pm.webp| center | 400]]




---
# 1 Exploratory Data Analysis 
- classic statistics focuses mainly on inference 
	- <mark style="background: #FFB8EBA6;">inference</mark> = complex procedures for drawing conclusions about large populations based on small samples 
	- John W Tukey pioneered EDA - linking engineering, computer science to statistics 
## 1.1 Structured Data Types
- types of data - hierarchy 
	- **numeric**
		- **continuous** (interval, float, numeric) e.g. floating points in a range
		- **discrete** (e.g. counts) e.g. whole integers
	- **categorical** 
		- **binary** (boolean) e.g. 2 possible values only 
		- **ordinal** e.g. categories inherently ordered e.g. shirt sizes
- knowing data types are essential to help decide what model, visualisation or analysis you will use 
	- additionally can help optimise memory and storage 
		- categorical variables can also be enforced in code e.g. `enum`
	- data typing in software acts as signal to the software how to process the data 
## 1.2 Rectangular Data 
- the basic data structure in data science is a rectangular matrix 
	- in which rows are records
	- and columns are the variables/features
- terminology + synonyms
	- dataframe = rectangular data - basic structure for statistical + ML modelling 
	- feature = column in a table (aka attribute, input, predictor, variable )
	- outcome = predicting an outcome using the features (aka dependent variable, response, target, output)
	- records = rows within the table (aka example, sample, observation)
## 1.3 Estimates of Location 
- exploring your data for a "typical value" for each feature 
	- <mark style="background: #FFB8EBA6;">central tendency</mark> i.e. estimating where most of your data is located 
	- several methods to do this 
- terminology on estimates vs statistics 
	- $N$ = full population size, $n$ = sample size 
	- usually call sample statistics *estimates*
- robustness & outliers
	- <span style="color:rgb(255, 136, 0)">robust</span> = not sensitive to extreme values
	- <span style="color:rgb(255, 136, 0)">outlier</span> = a data value that is very different from most of the data - can be subjectively defined
- <span style="color:rgb(255, 0, 247)">mean</span> = most basic estimate, the average value - sum of all values divided by number of values 
	- <span style="color:rgb(255, 0, 247)">weighted mean</span> = multiply each data value $x_i$ by user specified weight $w_i$, and divide sum by sum of weights
		- motivated since some values intrinsically more variable than others - highly variable values given lower weight 
		- and data collected does not equally represent different groups of interest
			- hence can be correct by giving those underrepresented values more weight 
	- <span style="color:rgb(255, 0, 247)">trimmed mean</span> = dropping fixed number of sorted values from each end, to reduce effect of extreme values
		- thought of as compromise between mean and median - robust to extremities, but uses more data to calculate central tendency
		- where $\{x_1, ..., x_n\}$ is sorted values 
		- where $p$ is number of smallest/largest values omitted 

$$
\begin{gather}
\text{Mean} = \bar{x} = \frac{\sum\limits^n_{i=1} x_i}{n} \\ \ \\
\text{Trimmed Mean} = \bar{x} = \frac{\sum\limits^{n-p}_{i=p+1} x_{(i)}}{n-2p} \\ \ \\
\text{Weighted Mean} = \bar{x} = \frac{\sum\limits^{n}_{i=1} w_i x_i}{\sum\limits^{n}_{i=1} w_i}
\end{gather}
$$

- <span style="color:rgb(255, 0, 247)">median</span> = middle number on a sorted list of data 
	- median is much more robust to outliers, as it relies only on the ranked values, not actual values
	- <span style="color:rgb(255, 0, 247)">weighted median</span> = each value has weight associated, however weighted median calculated where sum of weights is equal for lower and upper halves of the sorted list
		- similarly robust to outliers 
```python
# trimmed mean in scipy.stats 
from scipy.stats import trim_mean
trim_mean(values, 0.1)

# weighted median w NumPy
np.average(values, weights = weights)
wquantiles.median(values, weights = weights)
```
## 1.4 Estimates of Variability 
- additional to location, can summarise features with <mark style="background: #FFB8EBA6;">variability</mark> or <mark style="background: #FFB8EBA6;">dispersion</mark> 
	- **how tightly clustered or spread out values are** 
- <span style="color:rgb(255, 0, 247)">percentile</span> or <span style="color:rgb(255, 0, 247)">quantile</span> = value such that $P$% of values take this value or less 
	- and $100 - P$ take this value or more 
	- <span style="color:rgb(255, 0, 247)">IQR</span> = difference between 75th and 25th percentile
- <span style="color:rgb(255, 0, 247)">deviations</span> = difference between observed values + estimate of location (aka residuals, errors)
	- <span style="color:rgb(255, 0, 247)">variance</span> = sum of squared deviations from mean divided by $n-1$ ($n$ = number of values)
	- <span style="color:rgb(255, 0, 247)">standard deviation</span> = square root of variance 
		- easier to interpret since uses same scale as original data 
	- <span style="color:rgb(255, 0, 247)">mean absolute deviation</span> = mean of absolute values of the deviations from the mean 
	- <span style="color:rgb(255, 0, 247)">median absolute deviation from the median</span> = median of absolute values of the deviations from the median 

$$
\begin{gather}
\text{Mean Absolute Deviation} = \frac{\sum\limits^n_{i=1}|x_i - \bar{x}|}{n} \\ \ \\ 
\text{Variance} = s^2 =  \frac{\sum\limits^n_{i=1}(x_i - \bar{x})^2}{n-1} \\ \ \\ 
\text{Standard Deviation} = s = \sqrt{\text{Variance}} 
\end{gather}
$$

- notice most use absolute differences since taking naive sum would give precisely 0 (for variance)
	- or squared values - these are much more convenient to work with mathematically for models 
- degrees of freedom
	- denominator in variance formula $n-1$ accounts for calculating using a sample of data 
	- since we don't know true variance, so $n-1$ makes it unbiased by accounting for that
## 1.5 Exploring the Data Distribution 
- above methods show single objective summarisation of the data - **can also explore how the data is distributed overall**  
- <span style="color:rgb(255, 0, 247)">percentiles</span> = especially useful for summarising the tails (outer range) of distribution 
	- <span style="color:rgb(255, 0, 247)">boxplot</span> = plot from Tukey to quickly visualise data distribution
- <span style="color:rgb(255, 0, 247)">frequency tables</span> = tally of count of numeric data falling into a set of intervals/bins
	- bins are equally spaced segmented, then counts how many fall into each segment 
	- can calculate this in python with `{python}pd.cut(values, breaks = 10, right = True)`
	- <span style="color:rgb(255, 0, 247)">histogram</span> = plot of frequency table 
		- important to balance bin sizes as too granular loses big picture, too high level loses details 
		- `{python}ax = values.plot.hist(figsize = (4,4))`
	- <span style="color:rgb(255, 0, 247)">density plot</span> = smoothed version of histogram, often uses kernel density estimate
		- `{python}ax = values.plot.hist(density = True, bins = range(1,12))`
- <span style="color:rgb(255, 0, 247)">skewness</span> = whether data is skewed to larger or smaller values
	- <span style="color:rgb(255, 0, 247)">kurtosis</span> = propensity of data to have extreme values 
## 1.6 Exploring Binary & Categorical Data 
- categorical data can be described w simple proportions/percentages 
- <span style="color:rgb(255, 0, 247)">mode</span> = most common occurring value in data 
- <span style="color:rgb(255, 0, 247)">expected value</span> = when categories associated with numeric value, gives an average value based on probability of that category's occurrence 
	- a form of weighted mean where weights are probabilities 
	- process 
		- multiply each outcome by it's probability of an occurrence
		- sum these values 
- <span style="color:rgb(255, 0, 247)">bar charts</span> = frequency/proportion for each category plotted as bars 
	- `{python}ax = df['values'].transpose().plot.bar(figsize = (4,4), legend = False)`
## 1.7 Correlation 
- <span style="color:rgb(255, 0, 247)">correlation coefficient</span> = measure of how associated 2 variables are to each other
	- it is a standardised metric so ranges from -1 to +1
		- also sensitive to outliers like mean & standard deviation
		- often visualised with scatterplots 
	- scenarios 
		- when high values of A go with high values of B - positive correlation
		- when high values of A go with low values of B - negative correlation 
		- zero correlation means no relationship, just random 
	- <span style="color:rgb(255, 0, 247)">Pearson's</span> correlation coefficient = multiplies deviations from mean for variable A times those for variable B
		- and divides by product of standard deviations 

$$
\text{Pearson's r} = \frac{\sum\limits_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum\limits_{i=1}^{n} (x_i - \bar{x})^2} \sqrt{\sum\limits_{i=1}^{n} (y_i - \bar{y})^2}}
$$

- other types of correlation coefficients exist 
	- e.g. Spearman's Rho & Kendall's Tau are both non-parametric i.e. use rank-based values, not actual values 
	- also both are less sensitive to outliers for this reason
- <span style="color:rgb(255, 0, 247)">correlation matrix</span> = table where variables shown on both rows + columns, cell values = correlations between them 
	- in python we use heat-maps often to do this `{python}sns.heatmap(df.corr(), vmin = -1, vmax = 1)`

$$ \begin{array}{c|ccc} & \text{Feature A} & \text{Feature B} & \text{Feature C} \\ \hline \text{Feature A} & 1 & 0.8 & -0.5 \\ \text{Feature B} & 0.8 & 1 & 0.3 \\ \text{Feature C} & -0.5 & 0.3 & 1 \\ \end{array} $$

## 1.8 Exploring 2+ Variables
- correlation is good for 2 variables, but for more than 2, we use other methods
	- aka multivariate analysis 
	- methods below are also very useful to summarise big data - scatterplots won't work here 
- <span style="color:rgb(255, 0, 247)">contingency table</span> = tally of counts between 2 or more categorical variables
	- aka a pivot table, can look at counts but also proportions/percentages 
	- `{python}df.pivot_table(index = 'shirt_size', columns = 'color', aggfunc=lambda x:len(x))`
- visualisation methods 
	- all for 2-dimensional density, natural analogs to histograms + density plots
	- <span style="color:rgb(255, 0, 247)">hexagonal binning</span> = plot of 2 numeric variables with records binned into hexagons 
		- can use colour to indicate number of records in each hex bin 
		- `{python}df.plot.hexbin(x = 'height', y = 'weight', gridsize = 30, sharex = False, figsize=(4,4))`
	- <span style="color:rgb(255, 0, 247)">contour plot</span> = plot showing density of 2 numeric variables like a topographical map 
		- `{python}ax = sns.kdeplot(df['A'], df['B'], ax = ax)`
	- <span style="color:rgb(255, 0, 247)">violin plot</span> = similar to boxplot but shows density estimate 
		- `{python}ax = sns.violinplot(df['A'], df['B'], inner = 'quartile')`
- if we want to expand beyond 2 categorical variables + a numeric variable, we can use faceting
	- <mark style="background: #FFB8EBA6;">facets</mark> = conditioning variables 
![[Screenshot 2025-03-01 at 1.34.52 pm.webp| center | 400]]
---
# 2 Data & Sampling Distributions 
## 2.1 Random Sampling & Sample Bias 
- <mark style="background: #FFB8EBA6;">random sampling</mark> = sampling where each member of pop has equal chance of being picked at each draw
	- <span style="color:rgb(255, 0, 247)">simple random sample</span> = resulting sample from a random sample
	- <span style="color:rgb(255, 0, 247)">with/without replacement</span> = sampling where observations put back into population after each draw, or not 
	- <span style="color:rgb(255, 0, 247)">representativeness</span> = addresses data quality involving completeness, consistency of format, accuracy of individual data points
	- <span style="color:rgb(255, 0, 247)">bias</span> = systematic error resulting from measurement/sampling process
		- can be observable or invisible
		- <span style="color:rgb(255, 0, 247)">sample bias</span> = sample that misrepresents the population
		- i.e. sample was different in some meaningful + nonrandom way from larger pop it is meant to represent 
- terminology 
	- <span style="color:rgb(255, 0, 247)">sample</span> = subset from larger dataset, <span style="color:rgb(255, 0, 247)">population</span> = the larger data set 
		- $N (n)$ = size of population (sample)
		- $x$ = population mean, $\bar{x}$ = sample mean 
	- <span style="color:rgb(255, 0, 247)">stratified sampling</span> = dividing pop into strata and random sampling from each 
		- <span style="color:rgb(255, 0, 247)">stratum</span> (plural: <span style="color:rgb(255, 0, 247)">strata</span>) = homogenous subgroup of pop with common characteristics 
## 2.2 Selection Bias 
- **specifying a hypothesis test, then collecting data following randomisation & random sampling principles → ensures against bias**
- <mark style="background: #FFB8EBA6;">selection bias</mark> = practice of selectively choosing data (conscious or unconsciously) that leads to a misleading/ephemeral conclusion
	- i.e. bias resulting from way in which observations were selected 
	- <span style="color:rgb(255, 0, 247)">data snooping</span> = extensive hunting through data in search of something interesting 
		- aka <span style="color:rgb(255, 0, 247)">vast search effect</span> or p-hacking 
		- e.g. repeatedly run different models and ask different questions on the data, bound to find something
	- important in ML since review of large datasets if key value proposition 
		- can be countered by using holdout sets, target shuffling (permutation tests)
		- to test validity of predictive associations of a model
- <span style="color:rgb(255, 0, 247)">regression to the mean</span> = extreme observations tend to be followed by more central ones 
	- identified by Galton, 1886 studying parents & their children's heights 
## 2.3 Sampling Distribution of a Statistic 
- <mark style="background: #FFB8EBA6;">sampling distribution of a statistic</mark> = the distribution of some sample statistic over many samples drawn from same pop 
	- i.e. metric calculated for a sample drawn from larger pop 
	- samples usually drawn with goal of measuring/modelling something 
		- therefore interested in how different it might be i.e. *sampling variability*
		- with lots of data, can draw additional samples + observe distribution of sample statistic directly 
- terminology 
	- <span style="color:rgb(255, 0, 247)">data distribution</span> = frequency distribution of individual values in the dataset 
		- <span style="color:rgb(255, 0, 247)">sampling distribution</span> = frequency distribution of a sample statistic over many samples/resamples 
	- <span style="color:rgb(255, 0, 247)">central limit theorem</span> = tendency for sampling distribution to be normal as size increases
		- when means are drawn from multiple samples, will resemble bell-shape curve
			- even when original population not normally distributed - assuming sample size large enough 
		- **underlies the machinery of hypothesis testing + confidence intervals**
		- the bootstrap is more commonly used in ML
	- <span style="color:rgb(255, 0, 247)">standard error</span> = *standard deviation of sample statistic* over many samples 
		- not actually standard deviation, instead specifically for sample statistic 
		- standard error decreases as sample size increases 
## 2.4 The Bootstrap 
- <mark style="background: #FFB8EBA6;">bootstrap</mark> = easy/effective way to estimate sampling distribution of a statistic or model parameters
	- **by drawing additional samples w replacement from the sample itself**
	- then recalculating the statistic or model for each sample
- resampling is key to this 
	- process of taking repeated samples from observed data - via bootstrap or permutation/shuffling methods 
	- $R$ = number of iterations of the bootstrap, the more the better 
	- can also be used w multivariate data, rows sampled as units 
		- model can then be run on bootstrapped data to estimate stability/variability of model parameters
		- or improve predictive power (e.g. bagging/boosting)
		- bagging literally stands for bootstrapped aggregating 
- process of bootstrapping
	- 1. draw sample value, record it and then replace it 
	- 2. repeat $n$ times 
	- 3. record the mean of the $n$ resampled values 
	- 4. repeat steps 1-3 $R$ times 
	- 5. use $R$ for calculating:
		- standard deviation (estimated sample mean standard error)
		- produce histogram/boxplot
		- find confidence interval 
- no native python method, however can implement with `{python}sklearn.resample`
```python
results = []
for nrepeat in range(1000):
	sample = resample(df['income'])
	results.append(sample.median())

results = pd.Series(results)
print(f"original: {df['income'].median()}")
print(f"bias = {results.mean() - df['income'].median()}")
print(f"std. error = {results.std()}")
```
- resampling vs bootstrapping 
	- sometimes used interchangeably but resampling also includes permutation procedures
		- i.e. multiple samples combined, and sampling may be done w/o replacement 
	- bootstrap always implies sampling w replacement 
## 2.5 Confidence Intervals
- humans prefer point estimates but a range can better estimate uncertainty 
- <mark style="background: #FFB8EBA6;">confidence interval</mark> = another way to understand potential error in a sample estimate, grounded in statistical sampling principles 
	- <span style="color:rgb(255, 0, 247)">confidence level</span> = % of confidence intervals expected to contain statistic of interest 
	- <span style="color:rgb(255, 0, 247)">interval endpoints</span> = top and bottom of the confidence interval 
- confidence intervals always come with coverage level e.g. 90% or 95% 
	- **intuitively, a $X$% confidence interval around a sample estimate should on average contain similar sample estimated $X$% of the time** 
- process for calculating bootstrap confidence interval (w sample size of $n$)
	- 1. draw random sample of size $n$ w replacement 
	- 2. record statistic of interest for this resample 
	- 3. repeat 1-2 many $R$ times 
	- 4. for a $x$% confidence interval:
		- trim $[(100 - x)/2]$% of the $R$ resample results from either end of the distribution 
	- 5. the trim points are the endpoints of a $x\%$ bootstrap CI
- the bootstrap is a general tool that can be used to generate CI for most statistics or model parameters

![[Screenshot 2025-03-01 at 2.13.07 pm.webp| center | 400]]
- <span style="color:rgb(255, 0, 247)">level of confidence</span> = % associated with the CI 
	- importantly 
		- higher the level of confidence == wider the interval 
		- smaller the sample == wider the interval 
	- likewise, lower confidence levels == narrower the interval
## 2.6 Types of Distributions 
### 2.6.1 Normal Distribution 
- iconic bell-shaped distribution which has nice statistical properties
	- 68% of data lies within 1 SD, 95% within 2 SDs
	- aka the Gaussian distribution - 18th century German mathematician, Carl Friedrich Gauss
- terminology 
	- <span style="color:rgb(255, 0, 247)">error</span> = difference between data point and the predicted or average value
	- <span style="color:rgb(255, 0, 247)">standardise</span> = subtract the mean + divide by the SD 
	- <span style="color:rgb(255, 0, 247)">z-score</span> = result of standardising an individual data point 
	- <span style="color:rgb(255, 0, 247)">QQ plot</span> = visualises how close sample distribution is to specified distribution e.g. normal 
		- orders $z$-scores from low to high 
		- plots each value's $z$-score on the y-axis, x-axis is corresponding quantile of a normal distribution for that value's rank 
		- `{python}scipy.stats.probplot`
- <span style="color:rgb(255, 0, 247)">standard normal</span> = normal distribution with mean = 0, standard deviation = 1
	- where x axis represented as SDs from the mean
	- to compare data to standard normal distribution, you standardise/normalise your data first 

![[Screenshot 2025-03-01 at 2.16.50 pm.webp|center | 400]]

### 2.6.2 Long Tailed Distributions 
- most data not normally distributed by usually has long tails 
- assuming normal distribution can lead to underestimating extreme events "black swans"
### 2.6.3 Student's t Distribution 
- normally shaped, but with thicker and longer tails 
	- used extensively for depicting sample distributions , not as common in ML/AI
	- there is a family of t-distributions depending on how large sample is 
		- larger sample == more normally shaped t-distribution becomes 
- degrees of freedom = parameter that allows t-distribution to adjust to different sample sizes 
	- commonly used as reference basis for:
		- distribution of sample means
		- difference between 2 sample means 
		- regression parameters etc 
### 2.6.4 Binomial Distribution
- <mark style="background: #FFB8EBA6;">binomial distribution</mark> = distribution of number of successes in $x$ trials aka Bernoulli distribution
	- <span style="color:rgb(255, 0, 247)">binomial</span> = having 2 outcomes e.g. yes/no outcomes - very common in ML/DS/AI
	- <mark style="background: #FFB8EBA6;">trial</mark> = an event with 2 possible outcomes with definite probabilities 
		- <span style="color:rgb(255, 0, 247)">binomial trial</span> = trial with 2 outcomes aka Bernoulli trial 
	- <span style="color:rgb(255, 0, 247)">success</span> = outcome of interest for a trial e.g. 1 not 0
- binomial distribution = frequency distribution of:
	- the number of successes $x$ 
	- in a given number of trials $n$
	- with a specified probability $p$ of success in each trial 
- answers questions like "if probability of click leading to sale is 0.02, what is probability of observing 0 sales in 200 clicks"
	- there is a family of binomial distributions depending on values of $n$ and $p$
	- `{python}scipy.stats.binom.pmf` or `{python}scipy.stats.binom.cdf`
### 2.6.5 Chi-Square Distribution 
- chi-square distribution concerned with counts of subjects or items falling into categories 
- chi-square statistic measures extent of departure from what you'd expect in a null model 
### 2.6.6 F Distribution 
- F-distribution used with experiments and linear models involving measured data 
	- e.g. conducting an ANOVA
- F-statistic = compares variation due to factors of interest to overall variation 
### 2.6.7 Poisson & related Distributions 
- many processes produce events randomly at a given overall rate 
	- e.g. visitors arriving to a website, number of customers over a day
- <mark style="background: #FFB8EBA6;">poisson distribution</mark> = distribution of events per unit of time/space when we sample many such units 
	- <span style="color:rgb(255, 0, 247)">lambda</span> $\lambda$ = key parameter in poisson distribution, mean number of events that occur within specified time interval 
		- i.e. rate (per unit of time/space) at which events occur
	- the variance for a poisson distribution is also $\lambda$ 
- variations of poisson 
	- <span style="color:rgb(255, 0, 247)">exponential distribution</span> = frequency distribution of time/distance from one event to next event 
		- i.e. model the distribution of time between events 
		- lambda is also key here, intervals should be divided to be sufficiently homogenous 
	- estimating failure rates - often hard to do for many things 
		- often for rare events when we cannot reliably estimate $\lambda$ 
		- e.g. can make guesses - "have not seen any events last 20 hours, so we can be pretty sure the event rate is not 1 per hour"
		- can use simulations or probabilities to asses hypothetical event rates
	- <span style="color:rgb(255, 0, 247)">weibull distribution</span> = generalisation of exponential, which the event rate is allowed to shift over time 
		- event rate often is not constant over time 
		- naive solution is to calculate exponential distribution for chunks of time you know are similar 
		- alternatively, Weibull allows for a shape parameter $\beta$ 

---
# 3 Statistical Experiments & Significance Testing 
- usually t-tests, p-values etc are discussed in context of classical statistical inference 
	- classical statistical inference pipeline:
		- formulate hypothesis
		- design experiment
		- collect data 
		- inference/conclusions - apply results to larger population 
## 3.1 A/B Testing 
- <mark style="background: #FFB8EBA6;">AB Test</mark> = experiment w 2 groups to establish which of two treatments/products/procedures is superior 
	- includes a <span style="color:rgb(255, 0, 247)">treatment group</span> = group of subjects exposed to something (drug, price, webpage etc)
	- and a <span style="color:rgb(255, 0, 247)">control group</span> = no treatment or standard treatment
	- subjects are then randomly assigned to either group 
- relevant examples of when AB testing is useful - most commonly in web experiements
	- *AI-powered chatbot for customer service might perform an A/B test to compare two different conversational designs*
		- success of each design - assessed by via customer satisfaction scores, resolution times, and # escalations to humans
	- *e-commerce platform could conduct an A/B test to evaluate two different recommendation algorithms*
		- measured by comparing conversion rates, average order value, or user engagement metrics
- proper AB test has subjects that can be assigned to 1 treatment or another
	- subject can be a person, web visitor, plant etc 
		- key is they are exposed to treatment, ideally assigned randomly
	- **this way, you know difference is caused by 2 things**
		- 1. effect of the different treatments (what we want to know)
		- 2. luck of the draw in how subjects assigned to different treatments 
	- also need to pay attention to test statistic or metric you use
		- e.g. for binary outcomes
			- Price A vs Price B
			- then measure Conversion count/rate vs No-Conversion count/rate
		- or for continuous metrics
			- Group A mean and SD
			- Group B mean and SD 
- control groups give you assurance that all other things are equal 
	- so you try to control that any resulting difference is really due to the treatment (or chance)
	- using a naive baseline instead can cause different results
	- metrics should be chosen ahead of time 
- for more than 2 groups, we often use Multi-Arm bandits 
## 3.2 Hypothesis testing 
- <mark style="background: #FFB8EBA6;">hypothesis test</mark> = ubiquitous statistical methods to help learn whether random chance might be responsible for an observed effect 
	- aka significance tests - compares the null to the alternative hypothesis 
		- <span style="color:rgb(255, 0, 247)">null hypothesis</span> = hypothesis that chance is to blame 
			- i.e. assumption that treatments are equivalent, any difference between groups is purely random 
			- ideally we want to prove this wrong 
		- <span style="color:rgb(255, 0, 247)">alternative hypothesis</span> = counterpoint to the null, i.e. what you hope to prove 
			- examples 
				- *null* = "no difference between $A$ and $B$" 🆚  *alternative* = "$A$ is different from $B$" 
				- *null* = "$A$ = $B$" 🆚  *alternative* = "$A$ > $B$" 
				- *null* = "$A$ is not X% greater than $B$" 🆚  *alternative* = "$A$ is X% greater than $B$" 
	- one-way vs two-way test
		- one-way = hypothesis test that counts chance results only in 1 direction
			- fits nature of AB decision making where a decision is required, and one option is typically "default"
		- two-way = counts chance results in two directions
			- i.e. you don't care by being fooled by chance in any specific direction
			- aka bidirectional hypothesis
### 3.2.1 Resampling 
- 2 key types of resampling procedures
	- <span style="color:rgb(255, 0, 247)">permutation tests</span> = used to test hypotheses, typically involving 2+ groups
		- permute = change order of a set of values 
	- <span style="color:rgb(255, 0, 247)">bootstrap</span> = used to assess reliability of an estimate 
- **permutation test process**
	- aka ranom permutation test or randomisation test 
	- steps
		- 1. combine results from different groups into single dataset (e.g. both A and B)
		- 2. shuffle combined data, randomly draw w/o replacement a sample of the same size as group A
		- 3. from remaining data, randomly draw w/o replacement a resample of the same size as group B
		- 4. repeat for additional groups if you have it 
			- essentially giving you one set of resamples mirroring size of original samples 
		- 5. calculate the same metric used for original sample, but for the resamples 
			- record the result, this is one permutation iteration
		- 6. repeat previous step $R$ times to yield permutation distribution of the test statistic 
	- now compare the original observed difference between groups vs the permuted differences
		- if observed difference lies well within set of permuted differences
		- then nothing has been proved i.e. likely up to chance 
		- however if outside of permutation distribution, can conclude it's statistically significant
- 2 variants of the permutation test 
	- exhaustive permutation test = uses all possible ways to divide dataset rather than random shuffle
		- only practical for small datasets 
	- bootstrap permutation test = uses w replacement instead of without 
- overall, permutation tests useful for DS in understanding random variation 
	- resampling is flexible to data types + does not have struct assumptions 
### 3.2.2 Statistical Significance & p-Values 
- <mark style="background: #FFB8EBA6;">statistical significance</mark> = process of measuring if an experiment is beyond realm of chance 
	- <span style="color:rgb(255, 0, 247)">type 1 error</span> (FP) = mistakenly concluding effect is real when it's not
	- <span style="color:rgb(255, 0, 247)">type 2 error</span> (FN) = mistakenly concluding effect is due to chance when it's real 
- <mark style="background: #FFB8EBA6;">p-value</mark> = **probability of obtaining results unusual/extreme as observed given a null hypothesis** 
	- <span style="color:rgb(255, 0, 247)">alpha</span> = probability threshold of "unusualness" that chance results must surpass to be deemed statistically significant 
		- typical alpha levels = 0.01, 0.05
	- p-value i.e. given a chance model, what is the probability of a result this extreme
		- e.g. p-value of 0.308 = expect to observe result as extreme as this/or more, by random chance 30% of the time 
- in 2016, American Statistical Association gave cautionary statement on principles on using p-values
	- p-values can indicate how incompatible the data are with a specified statistical model 
	- p-values do not measure probability that studied hypothesis is true, or probability data was produced by random chance alone
	- scientific conclusions, policy/business decisions should be based only if p-values are significant 
	- p-values give no measure of the effect size or importance of a result 
- additionally, while something may be statistically significant, need to consider if it's practically significant 
	- overall, p-values useful in situations for knowing if model result is useful within range of normal chance variability 
	- but really should be treated as an additional information point to help decision making
### 3.2.3 t-Tests 
- most common type of significance test
	- all significance tests require specifying a test statistic to measure the effect you're interested in 
	- t-test in python - `{python}scipy.state.ttest_ind(values_A, values_B, equal_var = False)`
### 3.2.4 Multiple Testing
- multiplicity (e.g. multiple comparisons, many variables, many models, etc) increases the risk of concluding that something is significant just by chance
	- can use adjustments to account for these situations - essentially divide up the alpha by number of tests 
		- results in smaller alpha for each test
		- e.g. Bonferroni or Tukey's HSD 
	- using a holdout sample also helps here
- <mark style="background: #FFB8EBA6;">multiple testing</mark> = controlling probabilities of type 1 errors (FPs) when conducting many hypothesis tests simultaneously
	- necessary since more variables you add = greater probability something is significant by chance
		- known as <span style="color:rgb(255, 0, 247)">false discovery rate</span>, or <span style="color:rgb(255, 0, 247)">alpha inflation</span>
	- e.g. if you run $m$ individual hypothesis tests at $\alpha = 0.05$
		- probability of at least 1 FP (even if all null is true) is:
		- $1-(1-0.05)^m$ 
		- e.g. for 20 tests - there is a 64% chance of at least 1 FP 
### 3.2.5 Other Concepts + Tests
- degrees of freedom = forms part of the calculation to standardise test statistics so they can be compared to reference distributions 
	- e.g., t-distribution, F-distribution
	- underlies practice of factoring category variable into $n-1$ dummy variables to avoid multicollinearity 
- ANOVA = procedure to analyse experiment w multiple groups 
	- extension of AB tests - assesses if overall variation among groups within range of chance variation 
	- useful outcome of ANOVA = identifying variance components associated w group treatments, interaction effects, errors 
- chi-square test = tests if observed data counts consistent with assumption of independence 
	- chi-square distribution = reference distribution to which observed is compared
## 3.3 Multi-arm Bandit Algorithm 
- <mark style="background: #FFB8EBA6;">multi-arm bandits</mark> = imaginary slot machine w multiple arms for customer to choose from, each w different payoff - analogy to multi-treatment experiment
	- approach to testing (esp. web testing) allowing for explicit optimisation + rapid decision making 
	- <span style="color:rgb(255, 0, 247)">arm</span> = a treatment in an experiment 
	- <span style="color:rgb(255, 0, 247)">win</span> = experiment's analogy of a win at slot machine e.g. customer clicks link
- **allows you to take advantage of prior results and dynamically adjust** 
	- i.e. alter the sampling process to incorporate information learned during the experiment and reduce the frequency of the inferior treatment
		- i.e. **shifting sampling probability away from the inferior treatment(s) and toward the (presumed) superior one**
	- also allows you to test multiple treatments at once - much faster than normal statistical tests 
		- can efficiently handle 3+ treatments
- goal = win as much money as possible + identify/settle on winning arm soon as possible
	- challenge here we don't know overall rate the arms pay out
		- only know individual pulls on the arms 
	- balances explore/exploit 
		- e.g. does not pick best one early using initial trial results
		- also does not continue waiting to discover best process
		- instead allows for more pulls of winner, less pulls of losers but not abandon them
- initially, offers shown random and equally 
	- if one offer starts outperforming others, can be shown/pulled more often 
- <span style="color:rgb(255, 0, 247)">epsilon greedy algorithm</span> for AB test
	- 1. generate uniform distributed random number between 0-1
	- 2. if number between 0 and $\epsilon$, flip fair coin probability 
		- a. if coin heads - show offer A
		- b. if coin tails - show offer B 
	- 3. if number >= $\epsilon$, show offer with highest response rate to date 
	- epsilon is single parameter that governs the algo 
		- if $\epsilon$ = 1, end up w standard AB test 
		- if $\epsilon$ = 0, end up w purely greedy algorithm 
- more complex version available via Thompson's sampling
	- uses bayesian approach - assumes initial distribution 
## 3.4 Power & Sample Size 
- how long to run experiment? 
	- depends mainly on frequency with which goal desired is attained 
	- smaller the difference - more data needed to detect it 
- <mark style="background: #FFB8EBA6;">power</mark> = probability of detecting given effect size with given sample size 
	- <span style="color:rgb(255, 0, 247)">effect size</span> = minimum size of effect you hope to be able to detect 
		- e.g. 20% improvement in click rate
	- helps you plan how much data or how long you need to collect 
- calculating power or required sample size needs 4 parts
	- sample size 
	- effect size to detect 
	- significance level (alpha)
	- power
- having any 3 three of above, lets you calculate the missing one

---
# 4 Regression & Prediction 
- correlation vs regression 
	- correlation = measures association strength 
	- regression = quantifies nature of relationship 
- terminology 
	- <span style="color:rgb(255, 0, 247)">intercept</span> = predicted value when X = 0 (aka $\beta_0$)
	- <span style="color:rgb(255, 0, 247)">regression coefficient</span> = slope of regression line (aka parameter, weights, $\beta_1$) 
	- <span style="color:rgb(255, 0, 247)">fitted values</span> = estimates $\hat{Y}$ obtained from regression line
	- <span style="color:rgb(255, 0, 247)">residuals</span> = difference between observed and fitted values 
	- <span style="color:rgb(255, 0, 247)">least squares</span> = method of fitting regression by minimising sum of squared residuals 
## 4.1 Simple Linear Regression 
- regression equation models the relationship between a response variable $Y$ and a predictor variable $X$ as a line.
	- regression is used both for prediction and for explanation
		- regression does not prove direction of causation - needs to come from broader understanding
	- fitted values given by 

$$
\hat{Y_i} = \hat{b_0} + \hat{b_1} X_1
$$

- notation $\hat{b_0}, \hat{b_1}$ indicates coefficients are estimated vs known 

$$
\begin{gather}
RSS = \sum_{i=1}^n (Y_i - \hat{Y}_i)^2 \\ \ \\
= \sum_{i=1}^n (Y_i - \hat{b}_0 - \hat{b}_1 X_i)^2
\end{gather}
$$

## 4.2 Multiple Linear Regression
- extends the relationship between a response variable $Y$ and multiple predictor variables ($X_1, \dots, X_p$).

$$
Y = b_0 + b_1 X_1 + b_2 X_2 + \dots + b_p X_p + e
$$

- most important eval metrics = <span style="color:rgb(255, 0, 247)">root mean squared error</span> (RMSE) and <span style="color:rgb(255, 0, 247)">R-squared</span> ($R^2$)
	- denominator in $R^2$ is proportional to variance of $Y$

$$
\text{RMSE} = \sqrt{\frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{n}}
$$

$$
R^2 = 1 - \frac{\sum_{i=1}^n (y_i - \hat{y}_i)^2}{\sum_{i=1}^n (y_i - \bar{y})^2}
$$

- <mark style="background: #FFB8EBA6;">standard error of the coefficients</mark> can be used to measure the reliability of a variable’s contribution to a model
	- <span style="color:rgb(255, 0, 247)">t-statistic</span> = coefficient of predictor divided by standard error of coefficient 
	- <span style="color:rgb(255, 0, 247)">p-value</span> = mirror image of t-statistic, measures statistical significance 
		- i.e. extent outside range of what random chance arrangement and target might produce
		- higher t-statistic == lower p-value == more significant 

$$
t_b = \frac{\hat{b}}{SE(\hat{b})}
$$

- interpreting regression coefficients 
	- similar interpretation as simple linear reg
	- predicted value $\hat{Y}$ changes by coefficient $b_j$ for each unit change in $X_j$
		- assuming all other variable $X_k$ for $k \ne j$ remain constant 
	- in python, to get model summary - using `statsmodels`

```python
model = sm.OLS(house[outcome], house[predictors].assign(const=1))
results = model.fit()
results.summary()
```

- classical regression metrics all **"in sample" metrics** e.g. $R^2$, F-statistics, p-values
	- since they are applied to same data used to fit the model 
	- better instead to use out-of-sample metrics i.e. on holdout data with cross validation 
		- however using single holdout allows for some variability that might arise from it
		- i.e. could get different results if you select different holdout 
	- **cross validation extends holdout to multiple sequential holdout samples**
	- <span style="color:rgb(255, 0, 247)">K-Fold CV</span>
		- 1. set aside $1/k$ data as holdout sample
		- 2. train model on remaining data 
		- 3. apply model to holdout, recorded model assessment metrics
		- 4. restore first $1/k$ data, set aside next $1/k$ (no replacement)
		- 5. repeat steps 2 & 3
### 4.2.1 Model Selection for Regression 
- AIC = metric to penalise more predictors, also have MIC and Mallows CP 
- to choose best model we can use several techniques:  
	- <span style="color:rgb(255, 0, 247)">all subset regression</span> = computationally expensive, fits with all permutations of predictors
	- <span style="color:rgb(255, 0, 247)">stepwise regression</span> = method to automatically determine which variables should be included in the model
		- forward selection = start with one constant model, successively add variables
		- backward selection = start w all predictors, successively drop insig. variables
	- successively drop/add predictors to lower AIC or adjusted $R^2$
- <span style="color:rgb(255, 0, 247)">Weighted regression</span> = **give certain records more or less weight when fitting the equation**
	- 2 useful cases for DS/ML
		- *inverse-variance weighting* - observations measured with higher precision (lower variance) receive greater weight, reflecting their greater reliability
		- *aggregated data* - each row represents multiple original observations, a weight variable encodes the number of observations each row represents
## 4.3 Prediction Using Regression
- regression models are only valid for predictor values for which the data has sufficient values
	- extrapolation beyond the range of the data can lead to error
- much of stats is w understanding/measuring variability (uncertainty)
	- e.g. t-statistics + p-values for this formally, but can also use confidence intervals
	- <span style="color:rgb(255, 0, 247)">confidence intervals</span> help **quantify uncertainty for regression *coefficients*** 
	- <span style="color:rgb(255, 0, 247)">prediction intervals</span> help **quantify uncertainty in *individual predictions***
		- pertains to uncertainty around a single value
		- whereas CI pertains to mean or other statistics calculated from multiple values
		- hence prediction intervals often much wider than CI for same value 
- bootstrapping can also produce prediction + confidence intervals
	- with the same interpretation 
	- **bootstrapping for confidence intervals** fro dataset with $P$ predictors, $n$ rows
		- 1. consider each row a single "ticket", place $n$ tickets in a box
		- 2. draw ticket at random, record values, replace it in box 
		- 3. repeat step 2 $n$ times, gives one bootstrap sample
		- 4. fit regression to the bootstrap sample, record estimated coefficients
		- 5. repeat steps 2-4 1000 times
		- 6. now have 1000 bootstrap values for each coefficient
			- find appropriate percentiles for each e.g. 5th & 95th for 90% confidence interval
	- **bootstrapping for prediction intervals**
		- 1. take bootstrap sample from data 
		- 2. fit regression, predict new value 
		- 3. take a single residual randomly from original regression fit, add to predicted value, record result
		- 4. repeat steps 1-3 1000 times
		- 5. find 2.5th and 97.5th percentiles of results 
## 4.4 Factor Variables
- categorical variables i.e. factor variables need to be converted into numeric variables for use in a regression
	- <span style="color:rgb(255, 0, 247)">one-hot encoding</span> = most common method to encode a factor variable with $P$ distinct values 
		- represents them using $P$ dummy variables
		- useful for ML algos, less useful for multiple regression due to multicollinearity
			- since dummies form perfect linear combination - intercept essentially is the sum
	- <span style="color:rgb(255, 0, 247)">reference coding</span> = most common for statisticians, one level of factor used as reference
		- represents them using $P-1$ dummy variables
			- intercept (constant term) represents reference category predicted outcome
			- avoids multicollinearity since sum for remaining dummies never adds to 1
		- all other factors compared to that level 
	- <span style="color:rgb(255, 0, 247)">deviation coding</span> = compares each level against overall mean instead of reference level 
- factor variable with many levels may need to be consolidated into a variable with fewer levels
	- e.g. thousands of zip codes or industry codes 
		- can group these here e.g by sales price 
	- factors with ordered levels can be represented as single numeric variable
		- preserves the info contained in ordering which would be lost if converted to factor
## 4.5 Interpreting the Regression Equation
- <span style="color:rgb(255, 0, 247)">correlated variables</span> - when predictors highly correlated - harder to interpret individual coefficients
	- both sign + value of coefficients more difficult to interpret
		- and inflates standard error of estimates
	- <mark style="background: #FFB8EBA6;">multicollinearity</mark> = predictors have near perfect/perfect correlation - regression becomes unstable or impossible to compute
		- additional predictors become redundant 
		- not a problem for nonlinear regression + other models e.g. trees, clustering, KNN 
- <mark style="background: #FFB8EBA6;">confounding variables</mark> = important predictor, when omitted leads to spurious relationships in regression equation 
- <span style="color:rgb(255, 0, 247)">main effects</span> = relationship between predictor + target, independent of other variables 
- <span style="color:rgb(255, 0, 247)">interactions</span> = interdependent relationship between 2 or more predictors + the response
	- how to decide what interaction terms to include
		- prior knowledge + intuition 
		- stepwise selection 
		- penalised regression - automatically fit to large possible set of interaction terms
		- most common to use tree models - automatically searches for them
## 4.6 Regression Diagnostics
- <span style="color:rgb(255, 0, 247)">outliers</span> = records distant from rest of the data (or predicted values)
	- problematic for small datasets especially 
		- subjective to measure, some people use 1.5 times IQR range
	- <span style="color:rgb(255, 0, 247)">standardised residual</span> = residual divided by standard error of residuals
		- can use this to detect outliers
	- <span style="color:rgb(255, 0, 247)">influential value</span> = value whose presence/absence makes big difference in regression equation
		- common measure is hat-value i.e. values above $2(P+1)/n$ = high leverage data value
		- also Cook's distance - defines influence as combination of leverage + residual size
			- high influence if exceeds $4/(n - P - 1)$ 
		- bubble plots/influence plots show the standardised residuals, hat-value + cook's distance in single viz 
	- <span style="color:rgb(255, 0, 247)">leverage</span> = degree of influence single record has on regression equation 

![[Screenshot 2025-03-03 at 9.53.06 am.webp| center | 400]]

- <span style="color:rgb(255, 0, 247)">non-normal residuals</span> = can invalidate some technical requirements of regression, less important in DS
	- distribution of residuals mainly relevant to validity of formal statistical inference (hypothesis tests + p-values)
		- normally distributed residuals = model is complete
	- <span style="color:rgb(255, 0, 247)">heteroskedasticity</span> = when some ranges of target experience residuals w higher variance
		- could indicate missing predictor
	- <span style="color:rgb(255, 0, 247)">partial residual plots</span> = diagnostic plot showing relationship between outcome variable + single predictor 

![[Screenshot 2025-03-03 at 9.56.39 am.webp| center | 300]]

## 4.7 Nonlinear Regression
- often relationship between predictor & target is nonlinear 
	- several types of ways to fit nonlinear regression 
	- can detect this through outliers - records with large residuals 
	- nonlinear regression also solves for multicollinearity 
- <span style="color:rgb(255, 0, 247)">polynomial regression</span> = fit nonlinear relationships between predictors and the outcome variable
	- including polynomial terms in a regression equation 
	- uses a single polynomial function (e.g., quadratic, cubic) across the entire range of the predictor variable

$$
Y = b_0 + b_1 X + b_2 X^2 + e
$$

- <span style="color:rgb(255, 0, 247)">splines</span> = series of polynomial segments joined at knots
	- on the other hand, break the predictor’s range into segments and fit separate (typically lower‐degree) polynomials within each segment
		- too many polynomials causes very wiggly fits, much better to use splines 
	- technical definition = series of piecewise continuous polynomials 
		- pieces are then joined smoothly at “knots” so there are no abrupt jumps

![[Screenshot 2025-03-03 at 10.03.55 am.webp| center | 400]]

- <span style="color:rgb(255, 0, 247)">generalised additive models (GAMs)</span> = automate the process of specifying the knots in splines
	- can use python package `pyGAM` 

---
# 5 Classification 
- most methods described here can be applied to multiclass classification 
	- **converts multiclass problem to a series of binary problems** 
	- e.g. using One-vs-Rest or One-vs-One
## 5.1 Naive Bayes
- uses probability of observing predictor values given an outcome, to estimate $Y_i$ given set of predictors
	- <span style="color:rgb(255, 0, 247)">conditional probability</span> = probability of observing some event $X = i$ given some other event $Y=i$
		- written as $P(X_i | Y_i)$ 
	- <span style="color:rgb(255, 0, 247)">posterior probability</span> = probability of outcome after predictor info has been incorporated
		- in contrast to prior probability - not taking predictor info into account
- Exact bayesian classification
	- 1. find all records with same predictor values
	- 2. determine what classes those records belong to + which class is most probable 
	- 3. assign new record to that class
- Naive Bayes works with categorical (factor) predictors and outcomes
	- asks, *“Within each outcome category, which predictor categories are most probable?”*
	- then inverted to estimate the probabilities of outcome categories given predictor values
	- **called naive since assumption of using exact conditional probabilities can be estimated by product of individual conditional probs**
- Naive Bayes Classification 
	- 1. for a binary response $Y = i (i = 0$ or $1)$
		- estimate the individual conditional probabilities for each predictor $P(X_j \mid Y = i)$
		- i.e. probabilities that predictor value is in the record when we observe $Y=i$
		- probability is estimated by proportion of $X_j$ values among $Y=i$ records in training set
	- 2. multiply probabilities by each other 
		- then by proportion of records belonging to $Y=i$
	- 3. repeat steps 1 & 2 for all classes
	- 4. estimate probability for outcome $i$ by taking value in step 2 for class $i$
		- and divide by sum of such values for all classes
	- 5. assign record to class w highest prob for this set of predictor values
- can also be stated as equation of probability of observing outcome $Y=i$ given set of predictors $X_1, ..., X_i$ 
	- second is full formula 

$$
P(Y = i \mid X_1, X_2, ..., X_p)
$$

$$
P(Y = i \mid X_1, X_2, \ldots, X_p)
= \frac{P(Y = i)\,P(X_1, X_2, \ldots, X_p \mid Y = i)}{P(Y = 0)\,P(X_1, X_2, \ldots, X_p \mid Y = 0) + P(Y = 1)\,P(X_1, X_2, \ldots, X_p \mid Y = 1)}
$$

## 5.2 Discriminant Analysis
- Discriminant analysis = earliest statistical classifier 
	- works with continuous or categorical predictors, as well as with categorical outcomes
- uses covariance matrix, it calculates a linear discriminant function 
	- to distinguish records belonging to one class from those belonging to another
	- applied to the records to derive weights or scores for each record (one weight for each possible class)
		- which determines its estimated class.
## 5.3 Logistic Regression
- <mark style="background: #FFB8EBA6;">logistic regression</mark> = analogy to multiple regression but for binary categorical targets
	- model centric opposed as opposed to data centric like KNN & Naive Bayes
- terminology 
	- <mark style="background: #FFB8EBA6;">logit</mark> = function that maps class membership from $\pm \inf$ to a range between 0 and 1
		- synonym is log-odds
	- <mark style="background: #FFB8EBA6;">odds</mark> = ratio of success (1) to not success (0)
		- assume $p$ is success, $P = 0.75$
		- odds in favour of that event are $p/(1-p)$ which is $0.75/0.25$ = $\mathbf{3}$
		- **typically stated as "3 to 1" - success is 3x as likely as failure** 
	- <mark style="background: #FFB8EBA6;">log odds</mark> = response in transformed model (now linear) - gets mapped back to probability 
- key to logistic regression == <span style="color:rgb(255, 0, 247)">logistic response function</span> + the logit
	- we estimate outcome by applying logistic response (or inverse logit) function to the predictors 
	- ensures output stays between 0 and 1 

$$
p = \frac{1}{1 + e^{-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \dots + \beta_q x_q)}}
$$
$$
\hat{p} = \frac{1}{1 - e^{-\hat{Y}}}
$$
- to get exponential expression out of denominator
	- we consider odds instead of probabilities 
	- <span style="color:rgb(255, 0, 247)">odds</span> = the probability of an event divided by probability an event will not occur 

$$
\text{Odds}(Y = 1) = \frac{p}{1-p}
$$

- obtain the probability from the odds using the inverse odds function
	- combined with the logistic response function, then logarithm of both sides to get linear function of predictors
	- collectively called the <span style="color:rgb(255, 0, 247)">log-odds function</span> or the <span style="color:rgb(255, 0, 247)">logit function</span>
		- sometimes also called <span style="color:rgb(255, 0, 247)">logit-link</span> function 
			- _link function_ connects the mean of the outcome variable to a linear combination of predictors
		- which maps probability to any value (plus/minus infinity)

$$
\begin{gather}
\text{Get Probability from Odds - using inverse-odds function} \\ 
p = \frac{\text{Odds}}{1 + \text{Odds}} \\ \ \\ 
\text{Odds}(Y = 1) = e^{B_0 + B_1 X_1 + B_2 X_2 + ... + B_q X_q} \\ \ \\ 
\text{log(Odds}(Y=1)) = B_0 + B_1 X_1 + B_2 X_2 + ... + B_q X_q
\end{gather}
$$

| Terminology                 | Synonym                                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------------------- |
| Log odds                    | logarithm of ratio of probability of success to non-success                                               |
| Logit function              | function to transform probability into real number                                                        |
| Logit                       | interchangeable with "logit" function - same concept, logarithm of the odds ratio                         |
| Logit-link function         | the function for logistic regression to connect mean outcome variable to linear combination of predictors |
| Logistic (sigmoid) function | inverse of the logit, transforms any real value to a probability                                          |

![[Screenshot 2025-03-04 at 1.09.40 pm.webp| center | 400]]

- overall, several transformations are applied to put the model into a form that can be fit as a linear model
	- with the log of the odds ratio as the response variable
	- after linear model is fit, log odds mapped back to a probability 
	- logistic regression is a <span style="color:rgb(255, 0, 247)">generalised linear model (GLM)</span> - developed to extend linear regression to other settings
		- logistic regression is most common GLM 
		- 2 components of any GLM 
			- probability distribution or family (binomial in case of logistic regression)
			- link function (function to map response to predictors, logit for logistic regression)
- very useful since it's fast + can score new data easily 
	- python uses `{python}sklearn.linear_model.LogisticRegression`
	- also has arguments for regularisation - `penalty` and `C` - high `C` means no regularisation 
- linear vs logistic regression 
	- similarities 
		- both assume parametric (actual values not ranks) linear form between predictors + response 
		- can use stepwise regression, fit interaction or spline terms 
	- differences
		- objective function - $MLE$ not $MSE$
		- nature + analysis of residuals from the model
### 5.3.1 MLE (Maximum Likelihood Estimation)
- MLE is the objective function in logistic regression 
	- LR response not 0 or 1 - instead an estimate of the log odds that the response is 1 
	- given dataset $X_1, X_2, \dots, X_n$ and probability model $P_\theta(X_1, X_2, \dots, X_n)$ with parameters $\theta$
	- goal of MLE = find parameters that maximise $P_\theta(X_1, X_2, \dots, X_n)$ - probability of observing the data given the model $P$
		- i.e. tries to find solution such that estimated log odds best describes the observed outcome 
- fitting process of MLE uses a metric called deviance
	- lower deviance = better fit 

$$
deviance = -2 \log P_\theta(X_1, X_2, \dots, X_n)
$$

### 5.3.2 Assessing Logistic Regression Models
- interpreting p-values have same caveat as regression 
	- should be viewed as relative indicator of variable importance - not formal measure of statistical significance 
- residuals from logistic regression look very different to those of linear regression 
	- since output is binary - prediction measured as logit (log of odds ratio) which is always finite 

![[Screenshot 2025-03-04 at 1.21.11 pm.webp| center | 400]]

## 5.4 Evaluating Classification Models
- very commonly, DS split dataset into 3 
	- ***train*** = to train the model 
	- ***validation*** = to compare several models or model settings against 
	- ***test*** = holdout sample 2 for final performance
- <span style="color:rgb(255, 0, 247)">accuracy</span> = % predicted classifications that are correct
	- not a great metric especially for imbalanced datasets or understanding types of errors being made
- <mark style="background: #FFB8EBA6;">confusion matrix</mark> = tabular ($n\times n$ where $n$ = number of classes) display of record counts by predicted + actual classification results
	- <mark style="background: #FFB8EBA6;">recall</mark> (aka <span style="color:rgb(255, 0, 247)">sensitivity</span>) = % of all positives correctly classified as positive
	- <mark style="background: #FFB8EBA6;">specificity</mark> = % of all negatives (0s) correctly classified as negative
	- <mark style="background: #FFB8EBA6;">precision</mark> = % of all predicted positives (1s) that are actually positive 

$$
\begin{gather}
\textbf{TPR} = \textbf{Sensitivity} = \textbf{Recall} = \frac{TP}{TP + FN} \\ \\
\textbf{Specificity} = \frac{TN}{TN + FP} \\ \\
\textbf{FPR} = 1 - \text{Specificity} = \frac{FP}{TN + FP} \\ \ \\
\textbf{Precision} = \frac{TP}{TP + FP}
\end{gather}
$$

![[Screenshot 2025-03-04 at 2.06.34 pm.webp| center | 500]]

- <mark style="background: #FFB8EBA6;">ROC Curve</mark> (Receiver Operating Characteristic) = **plot of sensitivity versus specificity** 
	- there is a tradeoff between recall and specificity → capturing more 1s == misclassifying more 0s as 1s 
- ROC Curves show trade-off between **TPR/recall/sensitivity** (*x-axis*) vs **FPR/(1-Specificity)** (*y-axis*) across a range of thresholds
	- provides a comprehensive view of model performance over all classification thresholds
	- it is independent of the class distribution i.e. ratio of pos to neg instances
	- `{python}sklearn.metrics.roc_curve`
- process to compute ROC curve
	- 1. sort records by predicted probability of being a 1, most probable to least probable (descending)
	- 2. compute cumulative specificity and recall based on sorted records 

![[Screenshot 2025-03-04 at 2.24.54 pm.webp| center | 500]]

- alternatively, can also use <mark style="background: #FFB8EBA6;">Precision-Recall Curves</mark> (<span style="color:rgb(255, 0, 247)">PR-Curves</span>)
	- PR-curve = computed similarly except ordered from least to most probable (ascending)
	- and calculates cumulative precision + recall stats - most useful for highly unbalanced outcomes

![[Screenshot 2025-03-04 at 2.40.08 pm.webp| center | 400]]

- <mark style="background: #FFB8EBA6;">Area Under the ROC Curve</mark> (<mark style="background: #FFB8EBA6;">AUC</mark>) = summarises ROC curve into single number
	- ✅ AUC = 1.00 → perfect classifier, ⛔️ AUC = 0.5 → classifier w no discriminative power (equivalent to random guessing)
	- useful to have single scalar number to compare performance, threshold independent too
- <mark style="background: #FFB8EBA6;">Lift</mark> = measures how effective model is identifying positive cases
	- AUC might not fully capture performance when positive cases are rare
		- lift more focuses on model ability to rank instances - rank records by their predicted probability of being positive
		- e.g. if overall positive rate = 0.1%, but in top 10% your positive rate = 0.3%, then lift is 3
			- 3 times as effective at targeting potential positives as random selection 
	- calculation
		- rank all instances by their predicted probability of being positive
		- for given segment e.g. deciles, compare proportion of actual positives in segment to overall positive rate in dataset
	- <span style="color:rgb(255, 0, 247)">lift curves</span> (aka <span style="color:rgb(255, 0, 247)">gain charts</span>) help choose a good probability cutoff by showing how much more concentrated the positives are in the top segments of the ranked list
		- particularly useful in business/marketing contexts to identify most promising subset of cases 
		- + helps quantify improvement in targeting efficiency provided by the model 

## 5.5 Imbalanced Data
- imbalance = rare class problem, one class much more prevalent than the other 
	- more challenging for classification algorithms - can be addressed in several ways 
- how to address imbalanced data 
	- <span style="color:rgb(255, 136, 0)">metrics</span> - prioritise precision, recall, F1 score 
	- <span style="color:rgb(255, 136, 0)">data</span> - under sample abundant class, or oversample rare class, or SMOTE for synthetic rare data
		- under-sampling throws away data - loss of info that could be useful
		- oversampling is essentially bootstrapping rare cases
	- <span style="color:rgb(255, 136, 0)">algorithm</span> - incorporating weights for examples/classes into the loss function directly 
		- most classification algos allow for a weighting factor - discount errors for records w low weights, favour higher weights
			- e.g. `{python}sklearn.linear_model.LogisticRegression.fit(X, y, sample_weight = weights)`
		- <span style="color:rgb(255, 0, 247)">cost-based classification</span> = directly incorporates business impact of errors into model training process
			- evaluates whether the expected return (or loss) of an action is positive
			- especially useful for scenarios with asymmetric costs associated to FPs vs FNs

---
# 6 Statistical Machine Learning 
## 6.1 K-Nearest Neighbours (KNN)
- <span style="color:rgb(255, 0, 247)">KNN</span> = simple data-centric approach, classifies records by assigning to class which most similar records belong to 
	- uses distance metrics (e.g. euclidean distance) where set of predictors are the vector you find similar vectors for
	- $K$ = number of nearest neighbours, tradeoff in picking high vs low $K$
		- often choosing between 1 to 20, too low == overfitting risk, too high == over-smooth, high bias risk 
		- for highly structured data w little noise - smaller $K$ works best 
		- for noisy data w less structure - higher $K$ can work better 
	- importantly, predictor values need to be standardised so large scale values don't dominate distance metric 
		- e.g. using z-score normalisation where $z=\frac{x-\bar{x}}{s}$
- KNN can also give probability for predictions
	- using % of certain class within $K$ neighbour classes
- KNN can be very good as a feature engine - i.e. to add "local knowledge" in a staged process w other classification models
	- predicted value often used for new predictor value in 2nd stage model
	- process
		- 1. KNN to predict either a class label or a quasi-probability for each record
			- KNN bases its prediction on the values of a few nearby (or similar) records, it captures local patterns that might be missed by a global model
		- 2. Create new feature - add to your dataset as new predictor 
		- 3. Second stage modelling - apply another model w the enriched feature set, can improve performance  
## 6.2 Decision Trees
- <mark style="background: #FFB8EBA6;">CART</mark> = Classification And Regression Trees - developed by Leo Breiman et al. in 1984
	- more commonly known as <span style="color:rgb(255, 0, 247)">Decision trees</span> = produce a set of rules to classify or predict an outcome
	- rules correspond to successive partitioning of the data into sub-partitions 
		- each split based on specific value of predictor variable 
		- dividing data into records where predictor value greater than or lower than that split threshold
- trees are powered by algorithm to minimise the impurity of outcomes with resulting leaves (sub-partitions)
	- when no further split made, each terminal node in the tree contains records with a majority class for which new predictions will be 
		- fully grown trees can be pruned to avoid overfit 
		- trees are also very interpretable on their own - you can print out all the decision rules to inspect 
### 6.2.1 Recursive Partitioning 
- 1. for each predictor variable $X_j$
	- 1a. for each value $s_j$ of $X_j$
		- i. split records where $X_j$ values $< s_j$ as one partition, then remaining rows where $X_j \ge s_j$ into another partition
		- ii. measure homogeneity of each class in each partition
	- 1b. select value $s_j$ that produces maximum within-partition homogeneity 
- 2. select variable $X_j$ and the split value $s_j$ that produces maximum within-partition homogeneity 
- 3. recursively repeat this now for your 2 new sub-partitions 
	- applying same process until no further partition can be made that improves homogeneity 
- tree methods also the basis for most powerful bagging + boosting models
	- sacrifice interpretability for performance 
### 6.2.2 Measuring Homogeneity/Impurity 
- impurity or class purity can be measured in several ways for a given partition 
	- impurity/purity can range from 0 (perfect) to 0.5 (random guessing)
![[Screenshot 2025-03-04 at 4.44.46 pm.webp| center | 300]]
- 2 common metrics 
	- <mark style="background: #FFB8EBA6;">gini impurity</mark> = used for splitting criteria - measured for each resulting partition from the split
	- <mark style="background: #FFB8EBA6;">entropy</mark> = weighted average calculated to decide best overall split 
- when to decide to stop growing the tree
	- `min_samples_split` = default is 2, avoid splitting a partition if resulting partitions are too small
	- `min_samples_leaf` = default is 1, avoid splitting if terminal leaf is too small 
	- `max_depth` = default = None, how many overall splits to allow - i.e. tree depth 
	- `min_impurity_decrease` = limits splitting based on weighted impurity decrease value
	- ideally you should tune this with grid search CV 
## 6.3 Bagging and Random Forest
- Sir Francis Galton, 1906 statistician found a phenomenon "The Wisdom of the Crowds"
	- averaging or majority vote of many models and combining results improves accuracy - i.e. ensembles 
- <span style="color:rgb(255, 0, 247)">bagging</span> = general ensemble technique to form collection of models using bootstrapped data, then averaging predictions 
	- i.e. using diverse replicates of the initial dataset, can build very strong ensemble 
	- Random forest = type of bagging using trees for weak learners
		- additional to resampling data, algorithm also samples a subset of predictor variables during splits 
			- rule of thumb for number of variables to sample = $\sqrt{P}$ where $P$ = number of predictors
		- RFs output measure of variable importance - ranks predictors based on contribution to model accuracy 
- Random forest process
	- 1. **Initialise** 
		- Decide on the number of trees in the forest, $M$
		- Determine the number of records, $n$, to sample for each tree (with $n < N$, where $N$ is the total number of training records)
		- Set the number of predictors to consider at each split, $p$, where $p < P$ (with $P$ being the total number of predictors)
	- 2. **For each tree** $m = 1, 2, \dots, M$:
		- Draw a bootstrap sample (with replacement) of $n$ records from the training dataset to form the bag for tree $m$
	- 3. **At each node of the tree:**
		- Randomly select a subset of $p$ predictors from the full set of $P$ predictors
		- For each of the $p$ predictors
			- Consider all possible split points (or a set of candidate splits) for that predictor
			- For each candidate split, partition into 2 groups based on split value + calculate split quality 
		- Choose the predictor and split point that maximises the improvement in homogeneity (i.e., minimises impurity) across the two partitions
	- 5. **Grow the tree fully** (or until a stopping criterion is reached, such as a minimum node size or maximum tree depth)
## 6.4 Boosting
- <mark style="background: #FFB8EBA6;">boosting</mark> = ensemble method that fits a sequence of models, larger weights given to larger errors in successive rounds
	- also uses trees as base learners, however requires much more care than RFs - many more settings 
		- i.e. much more prone to overfit - hyperparams need careful tuning 
		- regularisation can help e.g. including penalty terms on tree size of the model 
		- also consider cross-validation to find best grid 
	- several variants exist e.g. stochastic GB, LightGBM, AdaBoost, XGBoost
- **boosting algorithm** 
	- 1. init $M$ models to be fit, set iteration counter $m=1$
		- init observation weights $w_i = 1/N$ for $i = 1,2,..., N$ 
		- init ensemble model $\hat{F_0} = 0$
	- 2. using observation weights $w_1, w_2, ..., w_N$
		- train a model $\hat{f}_m$ that minimises weighted error $e_m$ defined by summing weights for misclassified observations 
	- 3. add the model to the ensemble 
		- $\hat{F}_m = \hat{F}_{m-1} + \alpha_m \hat{f}_m$ where $\alpha_m = \frac{\log 1-e_m}{e_m}$
	- 4. update the weights $w_1, w_2, ..., w_N$ 
		- so weights for misclassified observations increases
		- size of increase depends on learning rate i.e. `eta` aka $\alpha_m$
	- 5. increment the model counter $m = m + 1$
		- if $m \le M$, repeat from step 2 
- the boosted estimated is then given by
$$
\large \hat{F} = \alpha_1 \hat{f_1} + \alpha_2 \hat{f_2} + ... + \alpha_M \hat{f_M}
$$
- intuition for weighting misclassified examples
	- model trained more heavily on poor performing predictions, $\alpha_m$ ensures models with lower error have bigger weight 
	- gradient boosting fits models not to actual values but their <span style="color:rgb(255, 0, 247)">pseudo-residual</span> 
		- has the effect of training more heavily on larger residuals 
- most important XGBoost hyperparams 
	- `subsample` = fraction of obs to sample at each iteration
	- `eta` = shrinkage factor applied to $\alpha_m$ in boosting - smaller == more regularised, less likely to overfit 
	- `reg_alpha` = manhattan distance (L1 regularisation) parameter - higher == more regularisation
	- `reg_lambda` = squared euclidean distance (L2 regularisation) parameter - higher == more regularisation

---
# 7 Unsupervised Learning 
- many of unsupervised techniques here are great for extended data analysis 
	- unsupervised techniques allow you to sift through + analyse the variables + discover relationships 
	- e.g. clustering especially helpful for cold-start problem where you lack knowledge of labelled areas of data 
		- or being able to identifier outliers for further analysis 
## 7.1 PCA (Principal Component Analysis)
- <mark style="background: #FFB8EBA6;">PCA</mark> = technique to reduce dimensionality by finding which numeric variables covary 
	- <span style="color:rgb(255, 0, 247)">PCs</span> =  linear combinations of the predictor variables (numeric data only)
	- <span style="color:rgb(255, 0, 247)">loadings</span> = weights that transform the predictors into the components 
- for 2 variables $X_1, X_2$, there are 2 principal components $Z_i$ where $i = \{1, 2\}$
	- $Z_i = w_{i,1} X_1 + w_{i, 2} X_2$
	- where $w_{i,1}, w_{i,2}$ are the weights or loadings - which transform original variables into PCs
	- each successive PC is orthogonal to others - explains as much of remaining variance as it can 

![[Screenshot 2025-03-05 at 9.07.46 am.webp| center | 400]]

- how PCs are calculated  
	- calculated to minimize correlation among components, thereby reducing redundancy
	- limited number of principal components will typically explain most of the variance in the outcome variable
	- process
		- 1. create first PC, using linear combination of predictors to maximise % of total variance explained
		- 2. this linear combination becomes first new PC $Z_i$
		- 3. PCA repeats process, using same variables w different weights to create 2nd new predictor $Z_2$
			- weighting is done such that $Z_1$ and $Z_2$ are uncorrelated
		- 4. process continues until you have as many PCs as original variables
		- 5. choose to retain $n$ number of PCs to account for most of variance
	- <span style="color:rgb(255, 0, 247)">screeplot</span> = visualisation to help see relative importance of each PC 
- <span style="color:rgb(255, 0, 247)">correspondence analysis</span> = similar technique for categorical data
	- less useful for big data context 

## 7.2 K-Means Clustering
- clustering = identify significant and meaningful groups of data
	- groups can be used directly/analysed/or used as feature to another model 
	- K-Means was the first clustering algorithm - still popular due to simplicity + ability to handle big data 
- <mark style="background: #FFB8EBA6;">K-Means</mark> = iteratively assigning records to the nearest cluster mean until the assignments stabilise
	- $K$ = number of desired clusters specified by user - often needs to be tweaked
		- can be helped through elbow plot viz - measured using inertia
	- sensitive to scaling, so standardisation/normalisation should be applied prior 
	- K-Means does not ensure clusters have same size - instead finds clusters that are best separated 
		- according to <span style="color:rgb(255, 0, 247)">within-cluster sum of squares</span>
		- <span style="color:rgb(255, 0, 247)">cluster mean</span> = center of each cluster $\bar{x_k}, \bar{y_k}$ 

$$
\begin{gather}
SS_k = \sum_{i \in k} (x_i - \bar{x}_k )^2 + (y_i - \bar{y}_k )^2 \\ \ \\ 
\text{Cluster Means} \\ \\ 
\bar{x}_k = \frac{1}{n_k} \sum_{i \in \text{Cluster } k} x_i \\ \ \\ 
\bar{y}_k = \frac{1}{n_k} \sum_{i \in \text{Cluster } k} y_i
\end{gather}
$$
- 2 most important outputs of K-Means 
	- size of clusters
		- imbalanced clusters can be caused by outliers or groups of outliers 
	- cluster means
		- can visualise like below or using heat-map

![[Screenshot 2025-03-05 at 9.16.11 am.webp| center | 400]]

## 7.3 Hierarchical Clustering
- Hierarchical clustering starts with each record in its own cluster
	- clusters are progressively merged into larger clusters until all records belong to a single cluster 
		- aka agglomerative algorithm
	- <span style="color:rgb(255, 0, 247)">dendrogram</span> = agglomeration history is retained and visualised
		- from the greek words "*dendro*" = tree, "*gram*" = visualisation
		- can observe the number and structure of clusters at different stages without pre-specifying the number of clusters

![[Screenshot 2025-03-05 at 9.21.05 am.webp| center | 300]]

- how hierarchical clustering works 
	- using dataset with $n$ records and $p$ variables
	- distance metric $d_{i,j}$ to measure distance between 2 records $i$ and $j$
	- dissimilarity metric $D_{A,B}$ to measure distance between 2 clusters $A$ and $B$ based on distances $d_{i,k}$ between members of each cluster
- 4 commonly used measures of dissimilarity - all rely on set of pairwise record distances
	- <span style="color:rgb(255, 0, 247)">complete linkage</span> = **maximum** distance between any point in one cluster and any point in the other
		- produces more compact clusters 
	- <span style="color:rgb(255, 0, 247)">single linkage</span> = **minimum** distance between any point in one cluster and any point in the other
		- leads to chaining, clusters strung together by points that happen to be close - gives elongated clusters
	- <span style="color:rgb(255, 0, 247)">average linkage</span> = **average** distance between all pairs of points (one from each cluster)
		- balance between single + complete, more robust against outliers but avoids excessive chaining 
	- <span style="color:rgb(255, 0, 247)">minimum variance</span> =  **minimises the increase** in within-cluster sum of squares (variance)
		- tends to produce clusters relatively spherical or compact 

$$
\begin{gather}
&\textbf{Single Linkage:} \quad
d_{\mathrm{single}}(A, B) 
= \min_{x \in A,\, y \in B} d(x,y). \\

&\textbf{Complete Linkage:} \quad
d_{\mathrm{complete}}(A, B) 
= \max_{x \in A,\, y \in B} d(x,y). \\

&\textbf{Average Linkage:} \quad
d_{\mathrm{average}}(A, B) 
= \frac{1}{|A|\cdot|B|}
\sum_{x \in A} \sum_{y \in B} d(x,y). \\

\end{gather}
$$