---
type: article
status: raw
quality: 1
topics: [model-calibration]
source: ""
created: 2025-12-29
published: 2021-04-19
author: Blogger
flashcards: none
updated: 2026-01-10
---

# Why model calibration matters and how to achieve it

<div align="center">
  <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgev_fY8SWvMJEAeMyZzOkDbUXkO3UY8H3vdIAw8TW2iQctj81Vvx_8C1gVIhnHhqV9KW6sSFqG6JbgLIBX5f3QpqW7KyNxqLtUjcYBRTmDtsDnoYBq5EDKRmUTT8ehe63bKafst8RnqHrO/w1200-h630-p-k-no-nu/blog+1.png" width="220" />
</div>

Source: https://www.unofficialgoogledatascience.com/2021/04/why-model-calibration-matters-and-how.html

Exported at: `2025-12-29T04:27:42Z`

- a quote from Nate Silver’s The Signal and the Noise: > One of the most important tests of a forecast — I would argue that it is the single most important one — is called calibration. Out of all the times you said there was a 40 percent chance of rain, how often did rain actually occur? If, over the long run, it really did rain about 40 percent of the time, that means your forecasts were well calibrated. If it wound up raining just 20 percent of the time instead, or 60 percent of the time, they weren’t.
- miscalibrated models are actually quite common.
- What are the consequences of miscalibrated models?
- Intuitively, you want to have calibration so that you can interpret your estimated probabilities as long-run frequencies.

#### Practical Reason #1: Estimated probabilities allow flexibility

- This expected value can be helpful for simulating the impact of an experiment

#### Practical Reason #2: Model Modularity

- In complex machine learning systems, models depend on each other. Single classifiers are often inputs into larger systems that make the final decisions.
- natural first step is checking whether you have already achieved calibration. Practically speaking, we are interested in whether your model is calibrated enough. We can check this by plotting your predicted probability against your empirical probability for some quantile buckets of your data.

![](https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgev_fY8SWvMJEAeMyZzOkDbUXkO3UY8H3vdIAw8TW2iQctj81Vvx_8C1gVIhnHhqV9KW6sSFqG6JbgLIBX5f3QpqW7KyNxqLtUjcYBRTmDtsDnoYBq5EDKRmUTT8ehe63bKafst8RnqHrO/w636-h640/blog+1.png)

- Miscalibration will be recognizable as a deviation from the diagonal line that represents perfect calibration. Usually an eye-test suffices to diagnose problems (see above) although you could check more formally with hypothesis testing or thresholding calibration specific metrics.
- The model-as-black-box perspective assumes that fixing the model is intractable analytically. Instead, we just ignore the model’s internal structure and fix things with a method-agnostic approach.
- comes at the cost of maintaining a separate step
- Like with global calibration, you can calibrate your model on slices/subsets of data. But if you calibrate across too many slices, things can become as complicated as the original model. To keep things manageable, our recommendation is to calibrate globally, and to calibrate a small number of slices that affect important decisions as needed.

### How calibration functions work

- **The calibration function should minimize a strictly [proper scoring rule](https://sites.stat.washington.edu/raftery/Research/PDF/Gneiting2007jasa.pdf)**. Strictly proper scoring rules are loss functions such that the unique minimizer is the true probability distribution. Log-loss and quadratic loss are two such examples.
- **The calibration function should be strictly monotonic**. It doesn’t feel intuitive to flip predictions if the model suggests one is more likely. Additionally, a monotonic calibration function preserves the ranking of predictions: this means that AUC isn’t affected (indeed you can estimate AUC and train your calibration function on the same data
- **The calibration function should be flexible**. Miscalibration may not fit a specific parametric form so we need a non-parametric model.
- **The calibration function needs to be trained on independent data**. Otherwise you might be vulnerable to extreme overfitting

### Calibration Methods

- The first method is Platt’s scaling which uses a logistic regression as the calibration function. This is easy to fit, but it violates our requirement for flexibility. As a parametric function it doesn’t flexibly adapt to more complicated calibration curves.
- Isotonic regression solves this problem by switching from logistic regression to fully nonparametric regression.
