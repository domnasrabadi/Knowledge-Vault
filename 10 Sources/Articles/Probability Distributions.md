---
type: article
status: structured
quality:
topics: [data-science]
source: ""
created: 2025-03-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- 100s of statistical distributions to choose from when modelling data 
- <mark style="background: #FFB8EBA6;">discrete distributions</mark> - when data only takes specific, distinct values 
	- e.g. integers like counts 
	- <mark style="background: #FFB8EBA6;">Probability Mass Functions (PMF)</mark>
		- discrete distributions described by PMF 
		- gives probability that a discrete random variable equal to some value 
		- often represented as a bar chart - each bar = probability of each discrete outcome
- <mark style="background: #FFB8EBA6;">continuous distributions</mark> - can take any value within range/interval 
	- e.g. real numbers, %, forecasted $
	- <mark style="background: #FFB8EBA6;">Probability Density Functions (PDF)</mark>
		- continuous distributions described by PDFs
		- probability of variable falling w/i particular range given by area under curve of PDF w/i that range
		- often represented as a KDE plot or smooth histogram 
- <mark style="background: #FFB8EBA6;">parametric models</mark> = models that assume specific distribution 
	- linear regression = assumes normally distributed errors 
	- logistic regression = assumes binomial distribution of response variable 
- <mark style="background: #FFB8EBA6;">non parametric models</mark> = no strong assumptions about form of the data distribution 
	- decision trees, KNN, SVMs
- loss functions - involve distributions, and need to select right loss function given that 
	- <span style="color:rgb(255, 0, 247)">poisson</span> used for count data 
	- <span style="color:rgb(255, 0, 247)">tweedie</span> used for mixed continuous data w many zeros