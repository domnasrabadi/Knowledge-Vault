---
type: book
status: structured
quality:
topics: [mlops, data-science]
source: ""
created: 2025-10-21
published:
author: ""
flashcards: none
updated: 2025-11-01
---
# 1 Overview
- ML systems are unique because they are data dependent, and data varies wildly from one use case to the next. 
	- chapters in this book are organized to reflect the problems data scientists might encounter as they progress through the lifecycle of an ML project.
- Machine learning is an approach to (1) *learn* (2) *complex patterns* from (3) *existing data* and use these patterns to make (4) *predictions* on (5) *unseen data*.
	- *1. Learn*: the system has the capacity to learn
	- *2. Complex patterns*: there are patterns to learn, and they are complex
	- *3. Existing data*: data is available, or it’s possible to collect data
	- *4. Predictions*: it’s a predictive problem
	- *5. Unseen data*: unseen data shares patterns with the training data
- In technical terms, it means your unseen data and training data should come from similar distributions. 
	- You might ask: “If the data is unseen, how do we know what distribution it comes from?” 
	- We don’t, but we can make assumptions—such as we can assume that users’ behaviors tomorrow won’t be too different from users’ behaviors today—and hope that our assumptions hold.
- ML solutions will especially shine if your problem has these additional following characteristics:
	1. It’s repetitive
	2. The cost of wrong predictions is cheap
	3. It’s at scale
	4. The patterns are constantly changing

- If your system always processes one query at a time, higher latency means lower throughput. If the average latency is 10 ms, which means it takes 10 ms to process a query, the throughput is 100 queries/second. If the average latency is 100 ms, the throughput is 10 queries/second.
- However, because most modern distributed systems batch queries to process them together, often concurrently, *higher latency might also mean higher throughput*. If you process 10 queries at a time and it takes 10 ms to run a batch, the average latency is still 10 ms but the throughput is now 10 times higher—1,000 queries/second.
- It’s usually better to think in percentiles, as they tell you something about a certain percentage of your requests. The most common percentile is the 50th percentile, abbreviated as p50. It’s also known as the median. If the median is 100 ms, half of the requests take longer than 100 ms, and half of the requests take less than 100 ms.
- Higher percentiles also help you discover outliers, which might be symptoms of something wrong. Typically, the percentiles you’ll want to look at are p90, p95, and p99.
- Higher percentiles are important to look at because even though they account for a small percentage of your users, sometimes they can be the most important users.
- In production, data, if available, is a lot more messy. It’s noisy, possibly unstructured, constantly shifting. It’s likely biased, and you likely don’t know how it’s biased. Labels, if there are any, might be sparse, imbalanced, or incorrect. Changing project or business requirements might require updating some or all of your existing labels.
- ML production would be a much better place if ML experts were better software engineers. Many traditional SWE tools can be used to develop and deploy ML applications.
- However, many challenges are unique to ML applications and require their own tools. In SWE, there’s an underlying assumption that code and data are separated. In fact, in SWE, we want to keep things as modular and separate as possible
- On the contrary, ML systems are part code, part data, and part artifacts created from the two.
- How to know if a data sample is good or bad for your system? Not all data samples are equal—some are more valuable to your model than others. For example, if your model has already trained on one million scans of normal lungs and only one thousand scans of cancerous lungs, a scan of a cancerous lung is much more valuable than a scan of a normal lung.
- ML systems are complex, consisting of many different components. Data scientists and ML engineers working with ML systems in production will likely find that focusing only on the ML algorithms part is far from enough. It’s important to know about other aspects of the system, including the data stack, deployment, monitoring, maintenance, infrastructure, etc.
- One of the reasons why predicting ad click-through rates and fraud detection are among the most popular use cases for ML today is that it’s easy to map ML models’ performance to business metrics: every increase in click-through rate results in actual ad revenue, and every fraudulent transaction stopped results in actual money saved.

## 1.1 Requirements for ML Systems

- The system should continue to perform the correct function at the desired level of performance even in the face of adversity
- How do we know if a prediction is wrong if we don’t have ground truth labels to compare it with?
- handling growth isn’t just resource scaling, but also artifact management. Managing one hundred models is very different from managing one model. With one model, you can, perhaps, manually monitor this model’s performance and manually update the model with new data. Since there’s only one model, you can just have a file that helps you reproduce this model whenever needed. However, with one hundred models, both the monitoring and retraining aspect will need to be automated. You’ll need a way to manage the code generation so that you can adequately reproduce a model when you need to.
- High cardinality problems can be very challenging. The first challenge is in data collection. In my experience, ML models typically need at least 100 examples for each class to learn to classify that class. S
- When the number of classes is large, hierarchical classification might be useful.
- Consider the task of predicting what app a phone user wants to use next. A naive setup would be to frame this as a multiclass classification task—use the user’s and environment’s features (user demographic information, time, location, previous apps used) as input, and output a probability distribution for every single app on the user’s phone. Let *N* be the number of apps you want to consider recommending to a user. In this framing, for a given user at a given time, there is only one prediction to make, and the prediction is a vector of the size *N*.
- This is a bad approach because whenever a new app is added, you might have to retrain your model from scratch, or at least retrain all the components of your model whose number of parameters depends on *N*. A better approach is to frame this as a regression task. The input is the user’s, the environment’s, and the app’s features. The output is a single value between 0 and 1; the higher the value, the more likely the user will open the app given the context. In this framing, for a given user at a given time, there are *N* predictions to make, one for each app, but each prediction is just a number.
- The debate isn’t about whether finite data is necessary, but whether it’s sufficient. The term *finite* here is important, because if we had infinite data, it might be possible for us to look up the answer. Having a lot of data is different from having infinite data.

## 1.2 Label multiplicity

Often, to obtain enough labeled data, companies have to use data from multiple sources and rely on multiple annotators who have different levels of expertise.

to do when there are multiple conflicting labels for a data instance.

Disagreements among annotators are extremely common. The higher the level of domain expertise required, the higher the potential for annotating disagreement.[8](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch04.html#ch01fn89)

To minimize the disagreement among annotators, it’s important to first have a clear problem definition.

Another common heuristic is based on disagreement among multiple candidate models. This method is called query-by-committee, an example of an ensemble method.[23](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch04.html#ch01fn103) You need a committee of several candidate models, which are usually the same model trained with different sets of hyperparameters or the same model trained on different slices of data. Each model can make one vote for which samples to label next, and it might vote based on how uncertain it is about the prediction. You then label the samples that the committee disagrees on the most.

Table 4-6. Definitions of True Positive, False Positive, False Negative, and True Negative in a binary classification task

Predicted Positive

Predicted Negative

Positive label

True Positive (hit)

False Negative (type II error, miss)

Negative label

False Positive (type I error, false alarm)

True Negative (correct rejection)

Precision = True Positive / (True Positive + False Positive)

Recall = True Positive / (True Positive + False Negative)

F1 = 2 × Precision × Recall / (Precision + Recall)

F1, precision, and recall are asymmetric metrics, which means that their values change depending on which class is considered the positive class.

area under the curve (AUC) measures the area under the ROC curve. Since the closer to the perfect line the better, the larger this area the better, as shown in [Figure 4-9](private://read/01k5ssjwkvre5t1tq4ah3yapeg/#roc_curve).

![](https://readwise.io/reader/pcei/gAAAAABo0dFaY2A63z5CIrkCuInxkDKf9ruFcC8WMTeR9_Hlx01T7rikwWl3CDvCXJfjFlrWhvnZvh2p_XPlx5blVGe_zfOCAy3dN_fTD7DSMz2RTl2-niw=/dmls_0409.png)

- Cost-sensitive learning
	- Elkan proposed cost-sensitive learning in which the individual loss function is modified to take into account this varying cost.[44](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch04.html#ch01fn120) The method started by using a cost matrix to specify *Cij*: the cost if class *i* is classified as class *j*. If *i* = *j*, it’s a correct classification, and the cost is usually 0. If not, it’s a misclassification. If classifying POSITIVE examples as NEGATIVE is twice as costly as the other way around, you can make *C*10 twice as high as *C*01.
- Class-balanced loss
	- we can make the weight of each class inversely proportional to the number of samples in that class, so that the rarer classes have higher weights. In the following equation, *N* denotes the total number of training samples:
- Focal loss
	- In our data, some examples are easier to classify than others, and our model might learn to classify them quickly. We want to incentivize our model to focus on learning the samples it still has difficulty classifying. What if we adjust the loss so that if a sample has a lower probability of being right, it’ll have a higher weight? This is exactly what focal loss does.

- In 2014, the paper [“Practical Lessons from Predicting Clicks on Ads at Facebook”](https://oreil.ly/oS16J) claimed that having the right features is the most important thing in developing their ML models. Since then, many of the companies that I’ve worked with have discovered time and time again that once they have a workable model, having the right features tends to give them the biggest performance boost compared to clever algorithmic techniques such as hyperparameter tuning.
- However, an ML system will likely need data beyond just text and images. For example, when detecting whether a comment is spam or not, on top of the text in the comment itself, you might want to use other information about:
	- The comment = How many upvotes/downvotes does it have?
	- The user who posted this comment = When was this account created, how often do they post, and how many upvotes/downvotes do they have?
	- The thread in which the comment was posted = How many views does it have? Popular threads tend to attract more spam.

- For domain-specific tasks such as predicting whether a transaction is fraudulent, you might need subject matter expertise with banking and frauds to be able to come up with useful features.
	- Instead of having to learn an infinite number of possible incomes, our model can focus on learning only three categories, which is a much easier task to learn. This technique is supposed to be more helpful with limited training data.
	- downside is that this categorization introduces discontinuities at the category boundaries

Discrete and Continuous Positional Embeddings

don’t want to input the absolute positions, 0, 1, 2, …, 7, into our model because empirically, neural networks don’t work well with inputs that aren’t unit-variance (

A way to handle position embeddings is to treat it the way we’d treat word embedding. With word embedding, we use an embedding matrix with the vocabulary size as its number of columns, and each column is the embedding for the word at the index of that column. With position embedding, the number of columns is the number of positions. In our case, since we only work with the previous sequence size of 8, the positions go from 0 to 7

![](https://readwise.io/reader/pcei/gAAAAABo0dFa0Kn7eCZUdXf14ng7U9LLGhby1NLBZBXSh9hayiAGKhxdO5MdzTCVUA18aRpulM9gi15z7EqtZY7inwlp0wey5itdX03LlcaPKGqWju0RrKQ=/dmls_0505.png)Figure 5-5. One way to embed positions is to treat them the way you’d treat word embeddings

In one example, researchers trained their model on a mix of scans taken when patients were lying down and standing up. “Because patients scanned while lying down were more likely to be seriously ill, the model learned to predict serious covid risk from a person’s position.”

In some other cases, models were “found to be picking up on the text font that certain hospitals used to label the scans. As a result, fonts from hospitals with more serious caseloads became predictors of covid risk.”

## 1.3 Feature Generalization

Since the goal of an ML model is to make correct predictions on unseen data, features used for the model should generalize to unseen data.

Overall, there are two aspects you might want to consider with regards to generalization: feature coverage and distribution of feature values.

Coverage is the percentage of the samples that has values for this feature in the data—so the fewer values that are missing, the higher the coverage. A rough rule of thumb is that if this feature appears in a very small percentage of your data, it’s not going to be very generalizable.

For the feature values that are present, you might want to look into their distribution. If the set of values that appears in the seen data (such as the train split) has no overlap with the set of values that appears in the unseen data (such as the test split), this feature might even hurt your model’s performance.

# 2 Chapter 6. Model Development and Offline Evaluation

Model development is an iterative process. After each iteration, you’ll want to compare your model’s performance against its performance in previous iterations and evaluate how suitable this iteration is for production.

## 2.1 Evaluating ML Models

There are many possible solutions to any given problem. Given a task that can leverage ML in its solution, you might wonder what ML algorithm you should use for it.

When selecting a model for your problem, you don’t choose from every possible model out there, but usually focus on a set of models suitable for your problem.

When considering what model to use, it’s important to consider not only the model’s performance, measured by metrics such as accuracy, F1 score, and log loss, but also its other properties, such as how much data, compute, and time it needs to train, what’s its inference latency, and interpretability.

## 2.2 Start with the simplest models

Zen of Python states that “simple is better than complex,” and this principle is applicable to ML as well. Simplicity serves three purposes. First, simpler models are easier to deploy, and deploying your model early allows you to validate that your prediction pipeline is consistent with your training pipeline. Second, starting with something simple and adding more complex components step-by-step makes it easier to understand your model and debug it. Third, the simplest model serves as a baseline to which you can compare your more complex models.

## 2.3 Evaluate good performance now versus good performance later

- The best model now does not always mean the best model two months from now. For example, a tree-based model might work better now because you don’t have a ton of data yet, but two months from now, you might be able to double your amount of training data, and your neural network might perform much better.[1](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch06.html#ch01fn150)
	- A simple way to estimate how your model’s performance might change with more data is to use [learning curves](https://oreil.ly/9QZLa).
	- A situation that I’ve encountered is when a team evaluates a simple neural network against a collaborative filtering model for making recommendations. When evaluating both models offline, the collaborative filtering model outperformed. However, the simple neural network can update itself with each incoming example, whereas the collaborative filtering has to look at all the data to update its underlying matri
	- While evaluating models, you might want to take into account their potential for improvements in the near future, and how easy/difficult it is to achieve those improvements.
- Evaluate trade-offs
	- One classic example of trade-off is the false positives and false negatives trade-off.
	- Following are some of the common assumptions. It’s not meant to be an exhaustive list, but just a demonstration:
		- Prediction assumption = Every model that aims to predict an output *Y* from an input *X* makes the assumption that it’s possible to predict *Y* based on *X*.
		- IID = Neural networks assume that the examples are [independent and identically distributed](https://oreil.ly/hXRr2), which means that all the examples are independently drawn from the same joint distribution.
		- Smoothness = Every supervised machine learning method assumes that there’s a set of functions that can transform inputs into outputs such that similar inputs are transformed into similar outputs. If an input *X* produces an output *Y*, then an input close to *X* would produce an output proportionally close to *Y*.
		- Tractability = Let *X* be the input and *Z* be the latent representation of *X*. Every generative model makes the assumption that it’s tractable to compute the probability *P*(*Z*|*X*).
		- Boundaries = A linear classifier assumes that decision boundaries are linear.
		- Conditional independence = A naive Bayes classifier assumes that the attribute values are independent of each other given the class.
		- Normally distributed = Many statistical methods assume that data is normally distributed.

- calculation only holds if the classifiers in an ensemble are uncorrelated. If all classifiers are perfectly correlated—all three of them make the same prediction for every email—the ensemble will have the same accuracy as each individual classifier. When creating an ensemble, the less correlation there is among base learners, the better the ensemble will be. Therefore, it’s common to choose very different types of models for an ensemble.

- some of the things that might cause an ML model to fail:
	- Theoretical constraints = As discussed previously, each model comes with its own assumptions about the data and the features it uses. A model might fail because the data it learns from doesn’t conform to its assumptions. For example, you use a linear model for the data whose decision boundaries aren’t linear.
	- Poor implementation of model = The model might be a good fit for the data, but the bugs are in the implementation of the model. For example, if you use PyTorch, you might have forgotten to stop gradient updates during evaluation when you should. The more components a model has, the more things that can go wrong, and the harder it is to figure out which goes wrong. However, with models being increasingly commoditized and more and more companies using off-the-shelf models, this is becoming less of a problem.
	- Poor choice of hyperparameters = With the same model, one set of hyperparameters can give you the state-of-the-art result but another set of hyperparameters might cause the model to never converge. The model is a great fit for your data, and its implementation is correct, but a poor set of hyperparameters might render your model useless.
	- Data problems = There are many things that could go wrong in data collection and preprocessing that might cause your models to perform poorly, such as data samples and labels being incorrectly paired, noisy labels, features normalized using outdated statistics, and more.
	- Poor choice of features = There might be many possible features for your models to learn from. Too many features might cause your models to overfit to the training data or cause data leakage. Too few features might lack predictive power to allow your models to make good predictions.

## 2.4 Model Offline Evaluation

- Ideally, the evaluation methods should be the same during both development and production. But in many cases, the ideal is impossible because during development, you have ground truth labels, but in production, you don’t.
- Baselines = Evaluation metrics, by themselves, mean little. When evaluating your model, it’s essential to know the baseline you’re evaluating it against. The exact baselines should vary from one use case to another, but here are the five baselines that might be useful across use cases:
- Random baseline = If our model just predicts at random, what’s the expected performance?
- Simple heuristic = Forget ML. If you just make predictions based on simple heuristics, what performance would you expect? F
- Zero rule baseline = The zero rule baseline is a special case of the simple heuristic baseline when your baseline model always predicts the most common class.
- Human baseline = In many cases, the goal of ML is to automate what would have been otherwise done by humans, so it’s useful to know how your model performs compared to human experts.
- Existing solutions = In many cases, ML systems are designed to replace existing solutions, which might be business logic with a lot of if/else statements or third-party solutions. I

- Ideally, the inputs used to develop your model should be similar to the inputs your model will have to work with in production, but it’s not possible in many cases. This is especially true when data collection is expensive or difficult and the best available data you have access to for training is still very different from your real-world data. The inputs your models have to work with in production are often noisy compared to inputs in development.[41](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch06.html#ch01fn190) The model that performs best on training data isn’t necessarily the model that performs best on noisy data.

## 2.5 Invariance tests
- To get a sense of how well your model might perform with noisy data, you can make small changes to your test splits to see how these changes affect your model’s performance.
	- Certain changes to the inputs shouldn’t lead to changes in the output.
	- To avoid these biases, one solution is to do the same process that helped the Berkeley researchers discover the biases: keep the inputs the same but change the sensitive information to see if the outputs change. 
		- Better, you should exclude the sensitive information from the features used to train the model in the first place.
- Directional expectation tests
	- Certain changes to the inputs should, however, cause predictable changes in outputs. For example, when developing a model to predict housing prices, keeping all the features the same but increasing the lot size shouldn’t decrease the predicted price, and decreasing the square footage shouldn’t increase it.
	- If the outputs change in the opposite expected direction, your model might not be learning the right thing, and you need to investigate it further before deploying it.

## 2.6 Model calibration

- If a model predicts that team A will beat team B with a 70% probability, and out of the 1,000 times these two teams play together, team A only wins 60% of the time, then we say that this model isn’t calibrated. A calibrated model should predict that team A wins with a 60% probability.
	- To quote Nate Silver in his book *The Signal and the Noise*, calibration is “one of the most important tests of a forecast—I would argue that it is the single most important one.”
	- To measure a model’s calibration, a simple method is counting: you count the number of times your model outputs the probability *X* and the frequency *Y* of that prediction coming true, and plot *X* against *Y*. The graph for a perfectly calibrated model will have *X* equal *Y* at all data points.

![](https://readwise.io/reader/pcei/gAAAAABo0dFaFmEnxPYriXOMiqji523m29lOouUVxnO05P9yJ6W-g-fvUbfXTOzZn_X74dkQXcwOs-M6fVVXhQ9zX9obMO3pk_K3zL349yItiFu3FoQwesc=/dmls_0611.png)



- To calibrate your models, a common method is [Platt scaling](https://oreil.ly/pQ0TQ),
- Confidence measurement
	- Confidence measurement can be considered a way to think about the usefulness threshold for each individual prediction.
	- While most other metrics measure the system’s performance on average, confidence measurement is a metric for each individual sample.
- System-level measurement is useful to get a sense of overall performance, but sample-level metrics are crucial when you care about your system’s performance on every sample.

## 2.7 Slice-based evaluation

- Slicing means to separate your data into subsets and look at your model’s performance on each subset separately.
	- A common mistake that I’ve seen in many companies is that they are focused too much on coarse-grained metrics like overall F1 or accuracy on the entire data and not enough on sliced-based metrics. This can lead to two problems.
	- One is that their model performs differently on different slices of data when the model should perform the same.

Table 6-3. Two models’ performance on the majority and minority subgroups 

Majority accuracy Minority accuracy Overall accuracy Model A 98% 80% 96.2% Model B 95% 95% 95%
Note: Table

- The focus on overall performance is harmful not only because of the potential public backlash, but also because it blinds the company to huge potential model improvements.
	- Another problem is that their model performs the same on different slices of data when the model should perform differently. Some subsets of data are more critical.
- To track your model’s performance on critical slices, you’d first need to know what your critical slices are. You might wonder how to discover critical slices in your data. Slicing is, unfortunately, still more of an art than a science, requiring intensive data exploration and analysis. Here are the three main approaches:
	- Heuristics-based = Slice your data using domain knowledge you have of the data and the task at hand.
	- Error analysis = Manually go through misclassified examples and find patterns among them.
	- Slice finder = There has been research to systemize the process of finding slices

# 3 Chapter 7. Model Deployment and Prediction Service

- In reality, companies have many, many ML models. An application might have many different features, and each feature might require its own model.
	- Uber has thousands of models in production.[6](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch07.html#ch01fn203) At any given moment, Google has thousands of models training concurrently with hundreds of billions parameters in size.
	- ML systems aren’t immune to it. On top of that, ML systems suffer from what are known as data distribution shifts, when the data distribution your model encounters in production is different from the data distribution it was trained on.[10](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch07.html#ch01fn207) Therefore, an ML model tends to perform best right after training and to degrade over time.
- People tend to ask me: “How often *should* I update my models?” It’s the wrong question to ask. The right question should be: “How often *can* I update my models?”
	- Since a model’s performance decays over time, we want to update it as fast as possible.
- *Online prediction* is when predictions are generated and returned as soon as requests for these predictions arrive.
- *Batch prediction* is when predictions are generated periodically or whenever triggered.

![](https://readwise.io/reader/pcei/gAAAAABo0dFa4W4X07X4wqt0i8mBbL1ExCH9Im64pgs3nDL1LXh6h_pioOHvVKt7KXqWCilN8qFjOPGPFrwUb233knWSsp7uRyYRa1x2Gr6pw8UFA_v-pL8=/dmls_0704.png)

![](https://readwise.io/reader/pcei/gAAAAABo0dFaSiONa-d5-_-HaQWYpK-haMfY9TWCwv4aPCOt4uvi5Nc2GYvMsR1O6O5BVVH-EWD8u8unTNYOrdQqv1l7kiHbw1qbpKK-3_1LYTSO8sa-QKE=/dmls_0705.png)


’ve heard the terms “streaming features” and “online features” used interchangeably. They are actually different. Online features are more general, as they refer to any feature used for online prediction, including batch features stored in memory.

A very common type of batch feature used for online prediction, especially session-based recommendations, is item embeddings. Item embeddings are usually precomputed in batch and fetched whenever they are needed for online prediction. In this case, embeddings can be considered online features but not streaming features.

Streaming features refer exclusively to features computed from streaming data.

For this reason, batch prediction can also be seen as a trick to reduce the inference latency of more complex models—the time it takes to retrieve a prediction is usually less than the time it takes to generate it.

Batch prediction is good for when you want to generate a lot of predictions and don’t need the results immediately.

However, the problem with batch prediction is that it makes your model less responsive to users’ change preferences.

Another problem with batch prediction is that you need to know what requests to generate predictions for in advance.

Batch prediction is a workaround for when online prediction isn’t cheap enough or isn’t fast enough.

As hardware becomes more customized and powerful and better techniques are being developed to allow faster, cheaper online predictions, online prediction might become the default.

To overcome the latency challenge of online prediction, two components are required:

•   A (near) real-time pipeline that can work with incoming data, extract streaming features (if needed), input them into a model, and return a prediction in near real time. A streaming pipeline with real-time transport and a stream computation engine can help with that.
    
•   A model that can generate predictions at a speed acceptable to its end users. For most consumer apps, this means milliseconds.

Having two different pipelines to process your data is a common cause for bugs in ML production. One cause for bugs is when the changes in one pipeline aren’t correctly replicated in the other, leading to two pipelines extracting two different sets of features. This is especially common if the two pipelines are maintained by two different teams

![](https://readwise.io/reader/pcei/gAAAAABo0dFaeRSX8k-mdY7ptyV7xID75n_ZK3cZi9gY0yw7Z6A1x6JEekG-O3_vQqOYXqheMMEGSBpS0OCCI5ObV_JTSMKUOpZp2TxDAVAZ513-aD1t2vg=/dmls_0707.png)


Model Compression

If the model you want to deploy takes too long to generate predictions, there are three main approaches to reduce its inference latency: make it do inference faster, make the model smaller, or make the hardware it’s deployed on run faster.

The key idea behind *low-rank factorization* is to replace high-dimensional tensors with lower-dimensional tensors.[20](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch07.html#ch01fn217) One type of low-rank factorization is *compact convolutional filters,* where the over-parameterized (having too many parameters) convolution filters are replaced with compact blocks to both reduce the number of parameters and increase speed.

![](https://readwise.io/reader/pcei/gAAAAABo0dFaXQn_2MQVKquGSDox-Du2gNQDHUsJNDgblwPUoUkpAE5UDh6wGjb1pmuliV55u3CUnonXZSV12Tv4C5jLD2s0IN-jqRQzyrXorkqbxYN_iBA=/dmls_0709.png)



*Knowledge distillation* is a method in which a small model (student) is trained to mimic a larger model or ensemble of models (teacher). The smaller model is what you’ll deploy. Even though the student is often trained after a pretrained teacher, both may also be trained at the same time.[23](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch07.html#ch01fn220) One example of a distilled network used in production is DistilBERT, which reduces the size of a BERT model by 40% while retaining 97% of its language understanding capabilities and being 60% faster.

advantage of this approach is that it can work regardless of the architectural differences between the teacher and the student networks. For example, you can get a random forest as the student and a transformer as the teacher. The disadvantage of this approach is that it’s highly dependent on the availability of a teacher network.

*Pruning* was a method originally used for decision trees where you remove sections of a tree that are uncritical and redundant for classification.

Pruning, in the context of neural networks, has two meanings. One is to remove entire nodes of a neural network, which means changing its architecture and reducing its number of parameters. The more common meaning is to find parameters least useful to predictions and set them to 0.

The architecture of the neural network remains the same. This helps with reducing the size of a model because pruning makes a neural network more sparse, and sparse architecture tends to require less storage space than dense structure.

Quantization

Quantization reduces a model’s size by using fewer bits to represent its parameters.

Quantization not only reduces memory footprint but also improves the computation speed. First, it allows us to increase our batch size. Second, less precision speeds up computation, which further reduces training time and inference latency.

There are downsides to quantization. Reducing the number of bits to represent your numbers means that you can represent a smaller range of values. For values outside that range, you’ll have to round them up and/or scale them to be in range.

![](https://readwise.io/reader/pcei/gAAAAABo0dFaCt2lRnCFuLh14qXfC4UMGMQq8LA916E3EBC7Cl3jtdNdb6Z9pLuQulHmonFo3kDEzSJme_7MI1oEQ5yKcJuXN31Y9WijQogkf3pNbGMs-FU=/dmls_0716.png)



# 4 Chapter 8. Data Distribution Shifts and Monitoring

Causes of ML System Failures

ML-Specific Failures

ML-specific failures are failures specific to ML systems. Examples include data collection and processing problems, poor hyperparameters, changes in the training pipeline not correctly replicated in the inference pipeline and vice versa, data distribution shifts that cause a model’s performance to deteriorate over time, edge cases, and degenerate feedback loops.

Production data differing from training data

The test data that we use to evaluate a model during development is supposed to represent unseen data, and the model’s performance on the test data is supposed to give us an idea of how well the model will generalize.

Data shifts happen all the time, suddenly, gradually, or seasonally.

Edge cases

Edge cases are the data samples so extreme that they cause the model to make catastrophic mistakes. Even though edge cases generally refer to data samples drawn from the same distribution, if there is a sudden increase in the number of data samples in which your model doesn’t perform well, it could be an indication that the underlying data distribution has shifted.

Degenerate feedback loops

a feedback loop as the time it takes from when a prediction is shown until the time feedback on the prediction is provided. The feedback can be used to extract natural labels to evaluate the model’s performance and train the next iteration of the model.

A *degenerate feedback loop* can happen when the predictions themselves influence the feedback, which, in turn, influences the next iteration of the model. More formally, a degenerate feedback loop is created when a system’s outputs are used to generate the system’s future inputs, which, in turn, influence the system’s future outputs.

Degenerate feedback loops are especially common in tasks with natural labels from users

This type of scenario is incredibly common in production, and it’s heavily researched. It goes by many different names, including “exposure bias,” “popularity bias,” “filter bubbles,” and sometimes “echo chambers.”

For the task of recommender systems, it’s possible to detect degenerate feedback loops by measuring the popularity diversity of a system’s outputs even when the system is offline. An item’s popularity can be measured based on how many times it has been interacted with (e.g., seen, liked, bought, etc.) in the past.

The first one is to use randomization, and the second one is to use positional features.

Introducing randomization in the predictions can reduce their homogeneity. In the case of recommender systems, instead of showing the users only the items that the system ranks highly for them, we show users random items and use their feedback to determine the true quality of these items. This is the approach that TikTok follows. Each new video is randomly assigned an initial pool of traffic (which can be up to hundreds of impressions). This pool of traffic is used to evaluate each video’s unbiased quality to determine whether it should be moved to a bigger pool of traffic or be marked as irrelevant.[17](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn266)

If the position in which a prediction is shown affects its feedback in any way, you might want to encode the position information using *positional features*. Positional features can be numerical (e.g., positions are 1, 2, 3,...) or Boolean (e.g., whether a prediction is shown in the first position or not).

A more sophisticated approach would be to use two different models.

first model predicts the probability that the user will see and consider a recommendation taking into account the position at which that recommendation will be shown. The second model then predicts the probability that the user will click on the item given that they saw and considered it. The second model doesn’t concern positions at all.

Types of Data Distribution Shifts

Covariate shift

When *P*(*X*) changes but *P*(*Y*|*X*) remains the same. This refers to the first decomposition of the joint distribution.

Label shift

When *P*(*Y*) changes but *P*(*X*|*Y*) remains the same. This refers to the second decomposition of the joint distribution.

Concept drift

When *P*(*Y*|*X*) changes but *P*(*X*) remains the same. This refers to the first decomposition of the joint distribution.[21](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn270)

a covariate is an independent variable that can influence the outcome of a given statistical trial but which is not of direct interest.

In supervised ML, the label is the variable of direct interest, and the input features are covariate variables.

Mathematically, covariate shift is when *P*(*X*) changes, but *P*(*Y*|*X*) remains the same, which means that the distribution of the input changes, but the conditional probability of an output given an input remains the same.

During model development, covariate shifts can happen due to biases during the data selection process, which could result from difficulty in collecting examples for certain classes.

If you know in advance how the real-world input distribution will differ from your training input distribution, you can leverage techniques such as *importance weighting* to train your model to work for the real-world data. Importance weighting consists of two steps: estimate the density ratio between the real-world input distribution and the training input distribution, then weight the training data according to this ratio and train an ML model on this weighted data.[26](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn275)

Label shift, also known as prior shift, prior probability shift, or target shift, is when *P*(*Y*) changes but *P*(*X*|*Y*) remains the same. You can think of this as the case when the output distribution changes but, *for a given output*, the input distribution stays the same.

Remember that covariate shift is when the input distribution changes. When the input distribution changes, the output distribution also changes, resulting in both covariate shift and label shift happening at the same time.

Because label shift is closely related to covariate shift, methods for detecting and adapting models to label shifts are similar to covariate shift adaptation methods.

Concept drift, also known as posterior shift, is when the input distribution remains the same but the conditional distribution of the output given an input changes. You can think of this as “same input, different output.”

There are other types of changes in the real world that, even though not well studied in research, can still degrade your models’ performance.

One is *feature change*, such as when new features are added, older features are removed, or the set of all possible values of a feature changes.[28](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn276) For example, your model was using years for the “age” feature, but now it uses months

*Label schema change* is when the set of possible values for *Y* change. With label shift, *P*(*Y*) changes but *P*(*X*|*Y*) remains the same. With label schema change, both *P*(*Y*) and *P*(*X*|*Y*) change.

With classification tasks, label schema change could happen because you have new classes. For example, suppose you are building a model to diagnose diseases and there’s a new disease to diagnose. Classes can also become outdated or more fine-grained.

Detecting Data Distribution Shifts

first idea might be to monitor your model’s accuracy-related metrics—accuracy, F1 score, recall, AUC-ROC, etc.—in production to see whether they have changed.

Having access to labels within a reasonable time window will vastly help with giving you visibility into your model’s performance.

When ground truth labels are unavailable or too delayed to be useful, we can monitor other distributions of interest instead. The distributions of interest are the input distribution *P*(*X*), the label distribution *P*(*Y*), and the conditional distributions *P*(*X*|*Y*) and *P*(*Y*|*X*).

While we don’t need to know the ground truth labels *Y* to monitor the input distribution, monitoring the label distribution and both of the conditional distributions require knowing *Y*.

Statistical methods

In industry, a simple method many companies use to detect whether the two distributions are the same is to compare their statistics like min, max, mean, median, variance, various quantiles (such as 5th, 25th, 75th, or 95th quantile), skewness, kurtosis, etc.

A more sophisticated solution is to use a two-sample hypothesis test, shortened as two-sample test. It’s a test to determine whether the difference between two populations (two sets of data) is statistically significant. If the difference is statistically significant, then the probability that the difference is a random fluctuation due to sampling variability is very low, and, therefore, the difference is caused by the fact that these two populations come from two distinct distributions.

caveat is that just because the difference is statistically significant doesn’t mean that it is practically important. However, a good heuristic is that if you are able to detect the difference from a relatively small sample, then it is probably a serious difference.

A basic two-sample test is the Kolmogorov–Smirnov test, also known as the K-S or KS test.[32](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn280) It’s a nonparametric statistical test, which means it doesn’t require any parameters of the underlying distribution to work. It doesn’t make any assumption about the underlying distribution, which means it can work for any distribution. However, one major drawback of the KS test is that it can only be used for one-dimensional data. If your model’s predictions and labels are one-dimensional (scalar numbers), then the KS test is useful to detect label or prediction shifts. However, it won’t work for high-dimensional data, and features are usually high-dimensional.[33](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn281) KS tests can also be expensive and produce too many false positive alerts.[34](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch08.html#ch01fn282)

![](https://readwise.io/reader/pcei/gAAAAABo0dFaOO2LnyGuYJM0yI_0XI30YGHX_oUxB1PchUMiCgNxuevMRV5NmlplDYEIlf8wG4kKzlnK-2Ec1mrUiaVXbvgXSjl7wjVBGO9-X7tYmVh7CG0=/dmls_0802.png)Figure 8-2. Some drift detection algorithms implemented by [Alibi Detect](https://oreil.ly/162tf). Source: Screenshot of the project’s GitHub repository

When computing running statistics over time, it’s important to differentiate between *cumulative and sliding statistics*. Sliding statistics are computed within a single time scale window, e.g., an hour. Cumulative statistics are continually updated with more data.

Addressing Data Distribution Shifts

To make a model work with a new distribution in production, there are three main approaches. The first is the approach that currently dominates research: train models using massive datasets. The hope here is that if the training dataset is large enough, the model will be able to learn such a comprehensive distribution that whatever data points the model will encounter in production will likely come from this distribution.

The second approach, less popular in research, is to adapt a trained model to a target distribution *without requiring new labels*.

The third approach is what is usually done in the industry today: retrain your model using the labeled data from the target distribution. However, retraining your model is not so straightforward. Retraining can mean retraining your model from scratch on both the old and new data or continuing training the existing model on new data. The latter approach is also called fine-tuning.

Addressing data distribution shifts doesn’t have to start after the shifts have happened. It’s possible to design your system to make it more robust to shifts. A system uses multiple features, and different features shift at different rates.

You might also want to design your system to make it easier for it to adapt to shifts. For example, housing prices might change a lot faster in major cities like San Francisco than in rural Arizona, so a housing price prediction model serving rural Arizona might need to be updated less frequently than a model serving San Francisco.

However, if you use a separate model for each market, you can update each of them only when necessary.

Monitoring and Observability

Monitoring refers to the act of tracking, measuring, and logging different metrics that can help us determine when something goes wrong. Observability means setting up our system in a way that gives us visibility into our system to help us investigate what went wrong.

Monitoring is all about metrics. Because ML systems are software systems, the first class of metrics you’d need to monitor are the operational metrics. These metrics are designed to convey the health of your systems. They are generally divided into three levels: the network the system is run on, the machine the system is run on, and the application that the system runs.

telemetry basically means “remote measures.” In the monitoring context, it refers to logs and metrics collected from remote components such as cloud services or applications run on customer devices.

When something goes wrong with an observable system, we should be able to figure out what went wrong by looking at the system’s logs and metrics without having to ship new code to the system. Observability is about instrumenting your system in a way to ensure that sufficient information about a system’s runtime is collected and analyzed.

Monitoring centers around metrics, and metrics are usually aggregated. Observability allows more fine-grain metrics, so that you can know not only when a model’s performance degrades but also for what types of inputs or what subgroups of users or over what period of time the model degrades.

# 5 Chapter 9. Continual Learning and Test in Production

Continual Learning

First, if your model is a neural network, learning with every incoming sample makes it susceptible to catastrophic forgetting. Catastrophic forgetting refers to the tendency of a neural network to completely and abruptly forget previously learned information upon learning new information.[1](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch09.html#ch01fn303)

updated model shouldn’t be deployed until it’s been evaluated. This means that you shouldn’t make changes to the existing model directly. Instead, you create a replica of the existing model and update this replica on new data, and only replace the existing model with the updated replica if the updated replica proves to be better.

![](https://readwise.io/reader/pcei/gAAAAABo0dFa1X3JNZ8DsjReD04oZEA3yvQ8CXRGPHrVnxiyBy56GhlgAwOpKOcvP_oPxoeXYLyuRrr0VWMzegPOVCy6bhw8ERj6wSRKkG6kWBrs80qk30Q=/dmls_0901.png)Figure 9-1. A simplification of how continual learning might work in production. In reality, the process of handling the failed challenger is a lot more sophisticated than simply discarding it.

Stateless Retraining Versus Stateful Training

Most companies do *stateless retraining*—the model is trained from scratch each time. Continual learning means also allowing *stateful training*—the model continues training on new data.[2](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch09.html#ch01fn304) Stateful training is also known as fine-tuning or incremental learning.

Figure 9-2. Stateless retraining versus stateful training

we must differentiate two types of model updates:

Model iteration

A new feature is added to an existing model architecture or the model architecture is changed.

Data iteration

The model architecture and features remain the same, but you refresh this model with new data.

The first use case of continual learning is to combat data distribution shifts, especially when the shifts happen suddenly.

Another use case of continual learning is to adapt to rare events.

A huge challenge for ML production today that continual learning can help overcome is the *continuous cold start* problem. The cold start problem arises when your model has to make predictions for a new user without any historical data.

Continuous cold start is a generalization of the cold start problem,[9](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch09.html#ch01fn311) as it can happen not just with new users but also with existing users.

TikTok, for example, has successfully applied continual learning to adapt their recommender system to each user within minutes. You download the app and, after a few videos, TikTok’s algorithms are able to predict with high accuracy what you want to watch next.

Continual Learning Challenges

Fresh data access challenge

The first challenge is the challenge to get fresh data. If you want to update your model every hour, you need new data every hour. Currently, many companies pull new training data from their data warehouses. The speed at which you can pull data from your data warehouses depends on the speed at which this data is deposited into your data warehouses.

Evaluation challenge

First, the more frequently you update your models, the more opportunities there are for updates to fail.

Second, continual learning makes your models more susceptible to coordinated manipulation and adversarial attack.

Algorithm challenge

Compared to the fresh data challenge and the evaluation, this is a “softer” challenge as it only affects certain algorithms and certain training frequencies. To be precise, it only affects matrix-based and tree-based models that want to be updated very fast (e.g., hourly).

It’s much easier to adapt models like neural networks than matrix-based and tree-based models to the continual learning paradigm. However, there have been algorithms to create tree-based models that can learn from incremental amounts of data, most notably Hoeffding Tree and its variants Hoeffding Window Tree and Hoeffding Adaptive Tree

Four Stages of Continual Learning

Stage 1: Manual, stateless retraining

Stage 2: Automated retraining

Stage 3: Automated, stateful training

Stage 4: Continual learning

How Often to Update Your Models

“How often should I update my models?” Before attempting to answer that question, we first need to figure out how much gain your model will get from being updated with fresh data. The more gain your model can get from fresher data, the more frequently it should be retrained.

The question of how often to update a model becomes a lot easier if we know how much the model performance will improve with updating.

One way to figure out the gain is by training your model on the data from different time windows in the past and evaluating it on the data from today to see how the performance changes.

![](https://readwise.io/reader/pcei/gAAAAABo0dFabZHCchyhlvnIP3_Xw7TUlrwmp5rTiS3mD3RwU4YDuOjcPrxEwNhAKy3hVxilg1Df76OGdr_NNSlNAIhV8ovZCexVa6uXESCAhntMH3TSSng=/dmls_0905.png)Figure 9-5. To get a sense of the performance gain you can get from fresher data, train your model on data from different time windows in the past and test on data from today to see how the performance changes

In 2014, Facebook did a similar experiment for ad click-through-rate prediction and found out that they could reduce the model’s loss by 1% by going from retraining weekly to retraining daily, and this performance gain was significant enough for them to switch their retraining pipeline from weekly to daily.

Test in Production

To sufficiently evaluate your models, you first need a mixture of offline evaluation discussed in [Chapter 6](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch06.html#model_development_and_offline_evaluatio) and online evaluation discussed in this section. To understand why offline evaluation isn’t enough, let’s go over two major test types for offline evaluation: test splits and backtests.

These test splits are usually static and have to be static so that you have a trusted benchmark to compare multiple models. It’ll be hard to compare the test results of two models if they are tested on different test sets.

However, if you update the model to adapt to a new data distribution, it’s not sufficient to evaluate this new model on test splits from the old distribution. Assuming that the fresher the data, the more likely it is to come from the current distribution, one idea is to test your model on the most recent data that you have access to. So, after you’ve updated your model on the data from the last day, you might want to test this model on the data from the last hour (assuming that data from the last hour wasn’t included in the data used to update your model). The method of testing a predictive model on data from a specific period of time in the past is known as a *backtest*.

With backtests, you should still evaluate your model on a static test set that you have extensively studied and (mostly) trust as a form of sanity check.

There are techniques to help you evaluate your models in production (mostly) safely. In this section, we’ll cover the following techniques: shadow deployment, A/B testing, canary analysis, interleaving experiments, and bandits.

Shadow Deployment

Shadow deployment might be the safest way to deploy your model or any software update. Shadow deployment works as follows:

1.  Deploy the candidate model in parallel with the existing model.
    
2.  For each incoming request, route it to both models to make predictions, but only serve the existing model’s prediction to the user.
    
3.  Log the predictions from the new model for analysis purposes.
    

Only when you’ve found that the new model’s predictions are satisfactory do you replace the existing model with the new model.

A/B Testing

A/B testing is a way to compare two variants of an object, typically by testing responses to these two variants, and determining which of the two variants is more effective. In our case, we have the existing model as one variant, and the candidate model (the recently updated model) as another variant. We’ll use A/B testing to determine which model is better according to some predefined metrics.

A/B testing has become so prevalent that, as of 2017, companies like Microsoft and Google each conduct over 10,000 A/B tests annually.[27](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch09.html#ch01fn329) It is many ML engineers’ first response to how to evaluate ML models in production. A/B testing works as follows:

1.  Deploy the candidate model alongside the existing model.
    
2.  A percentage of traffic is routed to the new model for predictions; the rest is routed to the existing model for predictions. It’s common for both variants to serve prediction traffic at the same time. However, there are cases where one model’s predictions might affect another model’s predictions—e.g., in ride-sharing’s dynamic pricing, a model’s predicted prices might influence the number of available drivers and riders, which, in turn, influence the other model’s predictions. In those cases, you might have to run your variants alternatively, e.g., serve model A one day and then serve model B the next day.
    
3.  Monitor and analyze the predictions and user feedback, if any, from both models to determine whether the difference in the two models’ performance is statistically significant.

A/B testing consists of a randomized experiment: the traffic routed to each model has to be truly random. If not, the test result will be invalid.

Second, your A/B test should be run on a sufficient number of samples to gain enough confidence about the outcome.

To measure statistical significance, A/B testing uses statistical hypothesis testing such as two-sample tests.

Canary Release

Canary release is a technique to reduce the risk of introducing a new software version in production by slowly rolling out the change to a small subset of users before rolling it out to the entire infrastructure and making it available to everybody.[28](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch09.html#ch01fn330) In the context of ML deployment, canary release works as follows:

1.  Deploy the candidate model alongside the existing model. The candidate model is called the canary.
    
2.  A portion of the traffic is routed to the candidate model.
    
3.  If its performance is satisfactory, increase the traffic to the candidate model. If not, abort the canary and route all the traffic back to the existing model.
    
4.  Stop when either the canary serves all the traffic (the candidate model has replaced the existing model) or when the canary is aborted.
    

The candidate model’s performance is measured against the existing model’s performance according to the metrics you care about. If the candidate model’s key metrics degrade significantly, the canary is aborted and all the traffic will be routed to the existing model.

A plausible scenario is that you first roll out the candidate model to a less critical market before rolling out to everybody.

Interleaving Experiments

Imagine you have two recommender systems, A and B, and you want to evaluate which one is better. Each time, a model recommends 10 items users might like.

What if instead of exposing a user to recommendations from a model, we expose that user to recommendations from both models and see which model’s recommendations they will click on? That’s the idea behind interleaving experiments, originally proposed by Thorsten Joachims in 2002 for the problems of search rankings.

![](https://readwise.io/reader/pcei/gAAAAABo0dFa-K42uho-AkWhkii6bQ96IheQUtphlEha0wsxXq1GEM8rQmAF5zQdJifOILAmTy_Pb8bpfcGEVaEbQzsY9E4paxDSuB_napYr4-yWr6IIGD8=/dmls_0906.png)Figure 9-6. An illustration of interleaving versus A/B testing.

Bandits

For those unfamiliar, bandit algorithms originated in gambling. A casino has multiple slot machines with different payouts. A slot machine is also known as a one-armed bandit, hence the name. You don’t know which slot machine gives the highest payout. You can experiment over time to find out which slot machine is the best while maximizing your payout. Multi-armed bandits are algorithms that allow you to balance between exploitation (choosing the slot machine that has paid the most in the past) and exploration (choosing other slot machines that may pay off even more).

As of today, the standard method for testing models in production is A/B testing. With A/B testing, you randomly route traffic to each model for predictions and measure at the end of your trial which model works better. A/B testing is stateless: you can route traffic to each model without having to know about their current performance. You can do A/B testing even with batch prediction.

When you have multiple models to evaluate, each model can be considered a slot machine whose payout (i.e., prediction accuracy) you don’t know. Bandits allow you to determine how to route traffic to each model for prediction to determine the best model while maximizing prediction accuracy for your users.

Bandit is stateful: before routing a request to a model, you need to calculate all models’ current performance. This requires three things:

•   Your model must be able to make online predictions.
    
•   Preferably short feedback loops: you need to get feedback on whether a prediction is good or not. This is usually true for tasks where labels can be determined from users’ feedback, like in recommendations—if users click on a recommendation, it’s inferred to be good. If the feedback loops are short, you can update the payoff of each model quickly.
    
•   A mechanism to collect feedback, calculate and keep track of each model’s performance, and route prediction requests to different models based on their current performance.

Bandits require less data to determine which model is the best and, at the same time, reduce opportunity cost as they route traffic to the better model more quickly.

However, bandits are a lot more difficult to implement than A/B testing because it requires computing and keeping track of models’ payoffs.

Contextual bandits as an exploration strategy

If bandits for model evaluation are to determine the payout (i.e., prediction accuracy) of each model, contextual bandits are to determine the payout of each action. In the case of recommendations/ads, an action is an item/ad to show to users, and the payout is how likely it is a user will click on it. Contextual bandits, like other bandits, are an amazing technique to improve the data efficiency of your model.

Imagine that you’re building a recommender system with 1,000 items to recommend, which makes it a 1,000-arm bandit problem. Each time, you can only recommend the top 10 most relevant items to a user. In bandit terms, you’ll have to choose the best 10 arms. The shown items get user feedback, inferred via whether the user clicks on them. But you won’t get feedback on the other 990 items. This is known as the *partial feedback* problem, also known as *bandit feedback*. You can also think of contextual bandits as a classification problem with bandit feedback.

Let’s say that each time a user clicks on an item, this item gets 1 value point. When an item has 0 value points, it could either be because the item has never been shown to a user, or because it’s been shown but not clicked on. You want to show users the items with the highest value to them, but if you keep showing users only the items with the most value points, you’ll keep on recommending the same popular items, and the never-before-shown items will keep having 0 value points.

Contextual bandits are algorithms that help you balance between showing users the items they will like and showing the items that you want feedback on.

# 6 Responsible AI

Responsible AI is the practice of designing, developing, and deploying AI systems with good intention and sufficient awareness to empower users, to engender trust, and to ensure fair and positive impact to society.

Irresponsible AI: Case Studies

Case study I: Automated grader’s biases

due to the COVID-19 pandemic. Ofqual, the regulatory body for education and examinations in the UK, sanctioned the use of an automated system to assign final A-level grades to students—without them taking the test.

Ofqual surmised, was to combine previous attainment data and teacher assessment to assign grades, using a particular statistical model—an ‘algorithm.’”

While the model’s accuracy seems low, Ofqual defended their algorithm as being broadly comparable to the accuracy of human graders. When comparing an examiner’s grades with those made by a senior examiner, the agreement is also around 60%.

If you’ve read this book thus far, you know that coarse-grained accuracy alone is nowhere close to being sufficient to evaluate a model’s performance, especially for a model whose performance can influence the future of so many students. A closer look into this algorithm reveals at least three major failures along the process of designing and developing this automated grading system:

•   Failure to set the right objective
    
•   Failure to perform fine-grained evaluation to discover potential biases
    
•   Failure to make the model transparent

Failure 1: Setting the wrong objective

However, the objective that Ofqual seemingly chose to optimize was “maintaining standards” across schools—fitting the model’s predicted grades to historical grade distributions from each school. For example, if school A had historically outperformed school B in the past, Ofqual wanted an algorithm that, on average, also gives students from school A higher grades than students from school B. Ofqual prioritized fairness between schools over fairness between students—they preferred a model that gets school-level results right over another model that gets each individual’s grades right.

Due to this objective, the model disproportionately downgraded high-performing cohorts from historically low-performing schools. A students from classes where students had historically received straight Ds were downgraded to Bs and Cs.[12](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch11.html#ch01fn380)

Failure 2: Insufficient fine-grained model evaluation to discover biases

It also “does not take into consideration the impact of multiple disadvantages for some protected groups [under the] 2010 Equalities Act, who will be double/triple disadvantaged by low teacher expectations, [and] racial discrimination that is endemic in some schools.”

Because the model took into account each school’s historical performance, Ofqual acknowledged that their model didn’t have enough data for small schools. For these schools, instead of using this algorithm to assign final grades, they only used teacher-assessed grades. In practice, this led to “better grades for private school students who tend to have smaller classes.”[14](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch11.html#ch01fn382)

Failure 3: Lack of transparency

For example, they didn’t let the public know that the objective of their system was to maintain fairness between schools until the day the grades were published. The public, therefore, couldn’t express their concern over this objective as the model was being developed.

Further, Ofqual didn’t let teachers know how their assessments would be used by the auto-grader until after the assessments and student ranking had been submitted. Ofqual’s rationale was to avoid teachers attempting to alter their assessments to influence the model’s predictions. Ofqual chose not to release the exact model being used until results day to ensure that everyone would find out their results at the same time.

Any system that operates on the trust of the public should be reviewable by independent experts trusted by the public.

Case study II: The danger of “anonymized” data

However, anonymization may not be a sufficient guarantee for preventing data misuse and erosion of privacy expectations. In 2018, online fitness tracker Strava published a heatmap showing the paths it records of its users around the world as they exercise, e.g., running, jogging, or swimming. The heatmap was aggregated from one billion activities recorded between 2015 and September 2017, covering 27 billion kilometers of distance. Strava stated that the data used had been anonymized, and “excludes activities that have been marked as private and user-defined privacy zones.”[17](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch11.html#ch01fn385)

Since Strava was used by military personnel, their public data, despite anonymization, allowed people to discover patterns that expose activities of US military bases overseas, including the “forward operating bases in Afghanistan, Turkish military patrols in Syria, and a possible guard patrol in the Russian operating area of Syria.”

So where did the anonymization go wrong? First, Strava’s default privacy setting was “opt-out,” meaning that it requires users to manually opt out if they don’t want their data to be collected. However, users have pointed out that these privacy settings aren’t always clear and can cause surprises to users.

However, privacy settings and users’ choices only address the problem at a surface level. The underlying problem is that the devices we use today are constantly collecting and reporting data on us. This data has to be moved and stored somewhere, creating opportunities for it to be intercepted and misused. The data that Strava has is small compared to much more widely used applications like Amazon, Facebook, Google, etc. Strava’s blunder might have exposed military bases’ activities, but other privacy failures might cause even more dangers not only to individuals but also to society at large.

## 6.1 A Framework for Responsible AI
- Discover sources for model biases
	- Training data = Is the data used for developing your model representative of the data your model will handle in the real world? If not, your model might be biased against the groups of users with less data represented in the training data.
	- Labeling = If you use human annotators to label your data, how do you measure the quality of these labels? How do you ensure that annotators follow standard guidelines instead of relying on subjective experience to label your data? The more annotators have to rely on their subjective experience, the more room for human biases.
	- Feature engineering = Does your model use any feature that contains sensitive information? Does your model cause a disparate impact on a subgroup of people? Disparate impact occurs “when a selection process has widely different outcomes for different groups, even as it appears to be neutral.”[23](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch11.html#ch01fn391) This can happen when a model’s decision relies on information correlated with legally protected classes (e.g., ethnicity, gender, religious practice) even when this information isn’t used in training the model directly.
	- Model’s objective = Are you optimizing your model using an objective that enables fairness to all users? For example, are you prioritizing your model’s performance on all users, which skews your model toward the majority group of users?
	- Evaluation = Are you performing adequate, fine-grained evaluation to understand your model’s performance on different groups of users? This is covered in the section [“Slice-based evaluation”](private://read/01k5ssjwkvre5t1tq4ah3yapeg/ch06.html#slice_based_evaluation). Fair, adequate evaluation depends on the existence of fair, adequate evaluation data.

Understand the trade-offs between different desiderata
