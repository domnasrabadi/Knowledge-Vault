---
type: article
status: raw
quality: 1
topics: [human-in-the-loop]
source: ""
created: 2025-12-17
published: 2021-07-20
author: Robert (munro) Monarch
flashcards: none
updated: 2026-01-04
---

# Human-In-The-Loop Machine Learning: Active Learning and Annotation for Human-Centered AI

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/371460210/ZU81_mEQjy7-aRW6XbFytwyvvvXsaush7nBOPU_8Zr4-cover-cover.jpeg" width="220" />
</div>

Source: private://read/01k6rsbresv9rgrxpe2hp95k07

Exported at: `2025-12-29T04:28:23Z`

- Annotation and active learning are the cornerstones of human-in-the-loop machine learning.

![](https://readwise.io/reader/pcei/gAAAAABo4a-y8ucVrUQaBtvC07DWsqQVj4iSL-wKr_VL-polqramc9JI2f4ebZn87GulGdsbxspMTVa1HetFZXv0k_g9AF2kKQhGBoBH9vkVXpgtnt4CrGA=/CH01_F01_Munro.png)

- Your machine learning algorithm strategy and your data annotation strategy can be optimized at the same time. The two strategies are closely intertwined, and you often get better accuracy from your models faster if you have a combined approach. Algorithms and annotation are equally important components of good machine learning.
- All computer science departments offer machine learning courses, but few offer courses on creating training data.
- Human errors in training data can be more or less important, depending on the use case. If a machine learning model is being used only to identify broad trends in consumer sentiment, it probably won’t matter whether errors propagate from 1% bad training data. But if an algorithm that powers an autonomous vehicle doesn’t see 1% of pedestrians due to errors propagated from bad training data, the result will be disastrous.
- For simple tasks, such as binary labels on objective tasks, the statistics are fairly straightforward for deciding which label is correct when different annotators disagree. But for subjective tasks, or even objective tasks with continuous data, no simple heuristics exist for deciding the correct label.
- *Active learning* is the process of deciding which data to sample for human annotation.

# Three broad active learning sampling strategies: Uncertainty, diversity, and random

- Uncertainty and diversity sampling go by various names in the literature. They are often referred to as *exploitation* and *exploration*,
- *Uncertainty sampling* is the set of strategies for identifying unlabeled items that are near a decision boundary in your current machine learning model. If you have a binary classification task, these items will have close to a 50% probability of belonging to either label; therefore, the model is called uncertain or confused. These items are most likely to be wrongly classified, so they are the most likely to result in a label that differs from the predicted label, moving the decision boundary after they have been added to the training data and the model has been retrained.
- *Diversity sampling* is the set of strategies for identifying unlabeled items that are underrepresented or unknown to the machine learning model in its current state. The items may have features that are rare in the training data, or they might represent real-world demographics that are currently under-represented in the model. In either case, the result can be poor or uneven performance when the model is applied, especially when the data is changing over time. The goal of diversity sampling is to target new, unusual, or underrepresented items for annotation to give the machine learning algorithm a more complete picture of the problem space. Although the term *uncertainty sampling* is widely used, *diversi*
- *Diversity sampling* is the set of strategies for identifying unlabeled items that are underrepresented or unknown to the machine learning model in its current state. The items may have features that are rare in the training data, or they might represent real-world demographics that are currently under-represented in the model. In either case, the result can be poor or uneven performance when the model is applied, especially when the data is changing over time. The goal of diversity sampling is to target new, unusual, or underrepresented items for annotation to give the machine learning algorithm a more complete picture of the problem space.
- Uncertainty sampling and diversity sampling have shortcomings in isolation (figure 1.2). Uncertainty sampling might focus on one part of the decision boundary, for example, and diversity sampling might focus on outliers that are a long distance from the boundary. So the strategies are often used together to find a selection of unlabeled items that will maximize both uncertainty and diversity.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yMl1XGpBcp8v0La-fXDM7n2qVdEcOiBRZJjZNZKMNpn-xCX__AHVGg3uuR3F1IQhLRZ775kP78tAeaNZPyIEl1xgpiGWvGgrXJyoNFq3KDTI=/CH01_F02_Munro.png)

- important to note that the active learning process is iterative. In each iteration of active learning, a selection of items is identified and receives a new human-generated label.
- Figure 1.3 The iterative active learning process. *Top left to bottom right*: Two iterations of active learning. In each iteration, items are selected along a diverse selection of the boundary, which in turn causes the boundary to move after retraining, resulting in a more accurate machine learning model. Ideally, we requested human labels for the minimum number of items as part of our active learning strategy. This request speeds the time to get an accurate model and reduces the overall cost of human annotation.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yWQ9nvp4Ua3LTbarVqq99UbYB6T8fpToMJ4CeutgfjBWe_HjHTuH-8HjFCgXYdFkN2TW59IR6kJscgDLfJrUR19aEAvKfCQCUXbXFGUJ1RL0=/CH01_F03_Munro.png)

- If you can’t define a meaningful random set of evaluation data, you should try to define a *representative* evaluation dataset. If you define a representative dataset, you are admitting that a truly random sample isn’t possible or meaningful for your dataset. It is up to you to define what is representative for your use case, based on how you are applying the data.
- You may also want to have multiple evaluation datasets that are compiled through different criteria. One common strategy is to have one dataset drawn from the same data as the training data and at least one out-of-domain evaluation dataset drawn from a different source.
- The simplest interface—binary responses—is also the best for quality contro
- For anyone who is undertaking a repetitive task such as creating training data, moving a mouse is inefficient and should be avoided if possible. If the entire annotation process can happen on a keyboard, including the annotation itself and any form submissions or navigations, the rhythm of the annotators will be greatly improved. If you have to include a mouse, you should be getting rich annotations to make up for the slower inputs.
- To get accurate training data, you have to take into account the focus of the human annotator, their attention span, and contextual effects that might cause them to make errors or to otherwise change their behavior.
- When the context or sequence of events can influence human perception, this phenomenon is known as *priming* The most important type in creating training data is *repetition priming*, which occurs when the sequence of tasks can influence someone’s perception.
- One way to combine machine learning and ensure quality annotations is to use a simple binary-input form to have people evaluate a model prediction and confirm or reject that prediction. This technique can be a nice way to turn a more complicated task into a binary annotation task. You could ask someone whether a bounding box around an object is correct as a simple binary question that doesn’t involve a complicated editing/selection interface. Similarly, it is easier to ask an annotator whether some word is a location in a piece of text than it is to provide an interface to efficiently annotate phrases that are locations in free text.
- Basic principles for designing annotation interfaces Based on what I’ve covered so far, here are some basic principles for designing annotation interfaces.
- • Cast your problems as binary choices wherever possible. • Ensure that expected responses are diverse to avoid priming. • Use existing interaction conventions. • Allow keyboard-driven responses.
- Evaluating search relevance is the single largest use case for human annotation in machine learning.

![](https://readwise.io/reader/pcei/gAAAAABo4a-ybybQBKOwOY3aqJPeoEyAC_T4XCBkfDR344_X19Hbf-tIl1yIn8_kTmG0xajljW_ngh07Xjx5cEGbgfWTQrGIqpYWcgX8gZpcUwKzhcOQzbQ=/CH01_F05_Munro.png)

- The four quadrants are • *Known known*—What your machine learning model can confidently and accurately do today. This quadrant is your model in its current state. • *Known unknown*—What your machine learning model cannot confidently do today. You can apply uncertainty sampling to these items. • *Unknown known*—Knowledge within pretrained models that can be adapted to your task. Transfer learning allows you to use this knowledge. • *Unknown unknown*—Gaps in your machine learning model. You can apply diversity sampling to these items.
- The columns and rows are meaningful too, with the rows capturing knowledge of your model in its current state and the columns capturing the type of solutions needed: • The top row captures your model’s knowledge. • The bottom row captures knowledge outside your model. • The left column can be addressed by the right algorithms. • The right column can be addressed by human interaction.

# Getting started with human-in-the-loop machine learning

- active learning is the process of selecting the right data for human review.
- *don’t trust any existing dataset to be representative of data that you encounter in the real world*.
- Because you are probably using filtered data by the time you build a machine learning model, it can be helpful to think of most machine learning problems as already being in the middle of the iteration process for active learning. Some decisions about data sampling have already been made; they led you to the current state of what data is annotated, and they probably weren’t entirely optimal. So one of the first things you need to worry about is how to start sampling the right data as you move forward.

## Interpreting model predictions and data to support active learning

- Almost all supervised machine learning models will give you two things: • A predicted label (or set of predictions) • A number (or set of numbers) associated with each predicted label The numbers are generally interpreted as confidences in the prediction, although this can be more or less true depending on how the numbers are generated. If there are mutually exclusive categories with similar confidence, you have good evidence that the model is confused about its prediction and that human judgment would be valuable. Therefore, the model will benefit most when it learns to correctly predict the label of an item with an uncertain prediction.
- In active learning, however, the numbers associated with the prediction typically are what we care about most.
- it *is* reasonable to assume that the rank order of confidence will correlate with accuracy. This will generally be true of almost all machine learning algorithms and almost all ways of calculating accuracy: you can rank-order the items by the predicted confidence and sample the lowest-confidence items.
- you often want to make sure that you are getting a diverse set of items for humans to label so that the newly sampled items aren’t all like each other.
- As with confidence ranking, we have many ways to ensure that we are maximizing the diversity of the content that is selected for human review. You
- For now, we will focus on a simple metric: the average training data frequency of words in each unlabeled item. Here is the strategy that we will implement in this chapter: 1. For each item in the unlabeled data, count the average number of word matches it has with items already in the training data. 2. Rank the items by their average match. 3. Sample the item with the lowest average number of matches. 4. Add that item to the labeled data. 5. Repeat these steps until you have sampled enough for one iteration of human review.
- If you have worked in machine learning for a while but never in annotation or active learning, you have probably optimized models only for accuracy. For a complete architecture, you may want to take a more holistic approach in which your annotation, active learning, and machine learning strategies inform one another.
- You could decide to implement machine learning algorithms that can give more accurate estimates of their confidence at the expense of accuracy in label prediction.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yDl2BPkq_ZPKcPAHVUDZEzxjnnIpdQ-HFjiyzRFdApoNxqp14VsLoA9BSVbsqg6j2xM0wZmI91CirNDp8SiZCT_bV6J6cYBE-IR2T2YYK7lU=/CH02_F02_Munro.png)

- Figure 2.2 The iterative process in your first human-in-the-loop machine learning system. Initially (top), you are annotating a random sample of unlabeled items to set aside as your evaluation data. Then you are labeling the first items to be used for training data (middle), also starting with a random selection. After this point, you start using active learning (bottom) to sample items that are low-confidence or outliers.
- *Fifth to tenth iterations*—Your models start to reach reasonable levels of accuracy, and you should see more diversity in the headlines. As long as either the F-score or AUC goes up by a few percentage points for every 100 annotations, you are getting good gains in accuracy.

## Building an interface to get human labels

- The right interface for human labeling is as important as the right sampling strategy. If you can make your interface 50% more efficient, that’s as good as improving your active learning sampling strategy by 50%.
- Out of respect for the people who are doing the labeling, you should do as much as you can to ensure that they feel they are as effective as possible.
- In most deployed systems, you need to implement quality control to ensure that annotators are not making mistakes; you will most likely need several iterations of annotation to refine the definitions of the labels and instructions; and you will need a system to track work assigned to multiple people in parallel.
- If you are doing any hyperparameter tuning at all, you should create validation data and use that data to tune your model, as you are already accustomed to doing in machine learning. In fact, you may want multiple kinds of validation datasets, including one drawn from your training data at each iteration, one drawn from your unlabeled data before you use active learning, and one drawn from the remaining unlabeled items at each iteration.
- Evaluation data is often called a test set or held-out data, and for this task, it should be a random sample of headlines that we annotate.
- It is important to get the evaluation data first, as there are many ways to inadvertently bias your evaluation data after you have started other sampling techniques.
- Here are some of the things that can go wrong if you don’t pull out your evaluation data first: • If you forget to sample evaluation data from your unlabeled items until after you have sampled by low confidence, your evaluation data will be biased toward the remaining high-confidence items, and your model will appear to be more accurate than it is. • If you forget to sample evaluation data and you pull evaluation data from your training data after you have sampled by confidence, your evaluation data will be biased toward low-confidence items, and your model will appear to be less accurate than it is. • If you have implemented outlier detection and later try to pull out evaluation data, it is almost impossible to avoid bias, as the items you pulled out have already contributed to the sampling of additional outliers.
- By including new randomly sampled items in each iteration of active learning, you get a baseline in that iteration. You can compare the accuracy from training on the random items with your other sampling strategies, which can tell you how effective your sampling strategies are compared with random sampling.
- Even if your other active learning strategies fail in the iteration, you will still get incremental improvement from the random sample, so random sampling is a nice fallback.
- Therefore, the example code focuses on selecting by confidence and sampling data for each iteration according to the following strategy: • 10% randomly selected from unlabeled items • 80% selected from the lowest confidence items • 10% selected as outliers
- Now that you have your newly annotated items, you can add them to your training data and see the change in accuracy from your model.

## Summary

- Two simple active learning strategies are easy to implement: sampling the least most confident items from predictions and sampling outliers. Understanding the basic goals of each of these strategies will help you dive deeper into uncertainty and diversity sampling later in this book.
- Good data management, such as creating evaluation data as the first task, is important to get right. If you don’t get your evaluation data right, you may never know how accurate your model is.
- Retraining a machine learning model with newly annotated data at regular iterations shows that your model gets more accurate over time. If designed correctly, the active learning iterations are naturally self-correcting, with overfitting in one iteration corrected by the sampling strategy in the following iterations.

# Uncertainty sampling

- In general, unlabeled data that confuses an algorithm is most valuable when it is labeled and added to the training data. If the algorithm can already label an item with high confidence, it is probably correct.
- But it is not always easy to know when a model is uncertain and how to calculate that uncertainty. Beyond simple binary labeling tasks, the different ways of measuring uncertainty can produce vastly different results. You need to understand and consider all methods for determining uncertainty to select the right one for your data and objectives.

## Interpreting uncertainty in a machine learning model

- *Uncertainty sampling* is a set of techniques for identifying unlabeled items that are near a decision boundary in your current machine learning model.
- We explore four approaches to uncertainty sampling in this chapter:
- *Least confidence sampling*—Difference between the most confident prediction and 100% confidence. In our example, if the model was most confident that a pedestrian was in the image, least confidence captures how confident (or uncertain) that prediction was.
- *Margin of confidence sampling* Difference between the two most confident predictions. In our example, if the model is most confident that a pedestrian was in the image and second most confident that the image contained an animal, margin of confidence captures the difference between the two confidences.
- Ratio of confidence—Ratio between the two most confident predictions. In our example, if the model is most confident that a pedestrian was in the image and the second most confident that the image contained an animal, ratio captures the *ratio* (not difference) between the two confidences.
- *Entropy-based sampling* Difference between all predictions, as defined by information theory. In our example, entropy-based sampling would capture how much *every* confidence differed from every other.
- Finally, your model is not telling you in plain language when it is uncertain: even for a single object, the machine learning model gives you a number that might *correspond* to the confidence of the prediction but might not be a reliable measure of accuracy.
- The underlying assumption of all active learning techniques is that some data points are more valuable to your model than others.
- Rank order is important for uncertainty sampling
- One common way to get more accurate confidences from your model is to adjust the base/temperature of softmax by using a validation dataset so that the probability distribution matches the actual accuracy as closely as possible. You might adjust the base/temperature of softmax so that a confidence score of 0.7 is correct 70% of the time, for example.
- You can calculate the success of active learning with accuracy metrics such as F-score and AUC
- Uncertainty sampling is a strategy for identifying unlabeled items that are near a decision boundary in your current machine learning model.

![](https://readwise.io/reader/pcei/gAAAAABo4a-ymvPUVhB5pZhkjp2eb-u_vxfDbpbopZFdFMookEN7WAGDRUS4Bl9bAf4SyxmgDqi14RllK3dmWAyei0XR2byzm1vyTHKa6vNZoDdEKA0ulB8=/CH03_F02_Munro.png)

- There are many algorithms for calculating uncertainty, some of which we will visit here. They all follow the same principles: • Apply the uncertainty sampling algorithm to a large pool of predictions to generate a single uncertainty score for each item. • Rank the predictions by the uncertainty score. • Select the top *N* most uncertain items for human review. • Obtain human labels for the top *N* items, retrain the model with those items, and iterate on the processes.

## Least confidence sampling

- The simplest and most common method for uncertainty sampling takes the difference between 100% confidence and the most confidently predicted label for each item.

## Margin of confidence sampling

- The most intuitive form of uncertainty sampling is the difference between the two most confident predictions. That is, for the label that the model predicted, how much more confident was it than for the next-most-confident label?
- If you care only about the uncertainty between the predicted label and the next-most-confident prediction for your particular use case, this method is a good starting point. This type of uncertainty sampling is the most common type that I’ve seen people use in industry.

## Ratio sampling

- Ratio of confidence is a slight variation on margin of confidence, looking at the ratio between the top two scores instead of the difference. It is the best uncertainty sampling method for improving your understanding of the relationship between confidence and softmax.

## Entropy (classification entropy)

- One way to look at uncertainty in a set of predictions is by whether you expect to be surprised by the outcome. This concept underlies the entropy technique. How surprised would you be by each of the possible outcomes, relative to their probability?

![](https://readwise.io/reader/pcei/gAAAAABo4a-y1xTNrx591Oeh44oRPKPyBepVZpw622oaylcfXTsKVRwtMGISoufRZDc4U3s0JfJLZK68sx5Wmg06bKRfyiILoK9jnNz-rLi9lNFWi_i_l_M=/CH03_F03_Munro.png)

- Figure 3.3 Example of low entropy (left) and high entropy (right). High entropy occurs when the probabilities are most like one another and there is the most surprise in any one prediction from the distribution.
- Unlike with softmax, calculating the entropy with different bases for uncertainty sampling does *not* change the rank order of scores across a dataset. You will get different entropy scores depending on the base, but the entropy scores will change monotonically for every probability distribution and therefore will not change the rank order

## Identifying when different types of models are confused

- Almost every machine learning library or service will return some form of scores for the algorithms in them, and these scores can be used for uncertainty sampling. In some cases, you will be able to use the scores directly; in other cases, you will have to convert the scores to probability distributions using something like softmax.

## Measuring uncertainty across multiple predictions

- Sometimes, you have multiple models built from your data. You may already be experimenting with different types of models or hyperparameters and want to combine the predictions into a single uncertainty score. If not, you may want to experiment with a few different models on your data to look at the variance.
- Similar to how a random forest is an ensemble of one type of supervised learning algorithm, you can use multiple types of algorithms to determine uncertainty and aggregate across them.
- The simplest way to combine multiple classifiers is to rank-order the items by their uncertainty score for each classifier, give each item a new score based on its rank order, and then combine those rank scores into one master rank of uncertainty.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yLEtJl5kWM-QU7Of6sQa_fLFCs8uyYPfa0C7P4la7TwhpOR0pIVDzpr0Ve7D5noBwwd5I5pxUVyqrhS-owptxfT2PHAte8-8Uo2EC1wNkkHA=/CH03_F06_Munro.png)

- You can calculate uncertainty by how often different models agree on the label of an item. The items with the most disagreement are the ones to sample.
- You can also take the probability distributions of the predictions into account. You can combine the predictions from different models in multiple ways: • Lowest maximum confidence across all models • Difference between minimum and maximum confidence across models • Ratio between minimum and maximum confidence across models • Entropy across all confidences in all models • Average confidence across all models
- Within active learning, the ensemble-based approach is sometimes known as *Query by Committee*, especially when only one type of machine learning algorithm is used for the ensemble.
- Applying dropout to a model to get multiple predictions for a single item. In each prediction, a random set of neurons is dropped (ignored), resulting in different confidences and (possibly) different predicted labels. Then the uncertainty can be calculated as the variation across all predictions: the higher the disagreement, the more uncertainty. This approach to getting multiple predictions from a single model is known as *Monte Carlo* dropouts.
- If your task is multilabeled, allowing multiple correct labels for each item, you can calculate uncertainty by using the same aggregation methods as for ensembles. You can treat each label as though it is a binary classifier.

## Selecting the right number of items for human review

- Uncertainty sampling is an iterative process. You select some number of items for human review, retrain your model, and then repeat the process.
- Two competing forces are at work: • Minimizing the sample size will ensure that the most benefit is gained from each data point at each iteration. • Maximizing the sample size will ensure that more items get labeled sooner and the model needs to be retrained less often.
- If you have a fixed budget for labels, you should try to get as many iterations as possible.
- If your budget is per label, meaning that you are paying a fixed price per label no matter how long the gap is between getting those labels, it is best to optimize for the maximum number of iterations possible.
- If you are time-constrained and need to get an updated model out quickly, you should consider strategies to retrain the models as quickly as possible, as in chapter 2. The quickest way is to use simple models.

## When do I stop if I’m not time- or budget-constrained?

- Lucky you! You should stop when your model stops getting more accurate. If you have tried many strategies for uncertainty sampling and are not getting any more gains after a certain accuracy is reached, this condition is a good signal to stop and think about other active learning and/or algorithmic strategies if your desired accuracy goal hasn’t been met.

## Evaluating the success of active learning

- Always evaluate uncertainty sampling on a randomly selected, held-out test set. If the test data is selected randomly from your training data after each iteration, you won’t know what your actual accuracy is. In fact, your accuracy is likely to appear to be lower than it is.

## Do I need new test data?

- If you already have test data set aside, and you know that the unlabeled data is from more or less the same distribution as your training data, you do not need additional test data. You can keep testing on the same data.
- If you know that the test data has a different distribution from your original training data, or if you are unsure, you should collect additional labels through random selection of unlabeled items and add them to your test set or create a second, separate test set.
- As soon as you have removed some unlabeled items from the pool via uncertainty sampling, that pool is no longer a random selection. That pool is now biased toward *confidently* predicted items, so a random selection from this pool is likely to return erroneously high accuracy if it is used as a test set.
- It is also a good idea to see how well your uncertainty sampling technique is performing next to a baseline of random sampling.
- If you aren’t more accurate than random sampling, you should reconsider your strategy!
- Unlike the evaluation data for your entire model, these items can be added to your training data in the next iteration, as you are comparing the sampling strategy at each step, given what is remaining to be labeled.
- Finally, you may want to include a random sample of items along with the ones chosen by uncertainty sampling.
- If you are not going to implement some of the diversity sampling methods in chapter 4, random sampling will give you the most basic form of diversity sampling and ensure that every data point has a chance of getting human review.
- You should also consider up to four validation sets at each iteration, with data drawn from • The same distribution as the test set • The remaining unlabeled items in each iteration • The same distribution as the newly sampled items in each iteration • The same distribution as the total training set in each iteration
- A validation set will let you tune the accuracy of the model without looking at the test set. Typically, you will have a validation set from the outset. As with your test set, you don’t need to update/replace it if you think that the unlabeled items come from the same distribution as your initial training data. Otherwise, you should update your validation data before the first iteration of your uncertainty sampling, as with your test data.
- You may want to use a second validation set to test how well your active learning strategy is doing within each iteration. After you start active learning iterations, the remaining unlabeled items will no longer be a random sample, so this distribution will not be the same as your existing test set and validation set.
- This dataset acts as a baseline for each iteration. Is uncertainty sampling still giving you better results than selecting from random among the remaining items? Because this dataset set is useful for only one iteration, it is fine to add these items to the training data at the end of each iteration; these labels aren’t human labels that get discarded.
- If you want to evaluate the accuracy of the human-labels created in each iteration, you should do this on a third validation data set drawn from the same distribution as the newly sampled data. Your newly sampled data may be inherently easier or harder for humans to label, so you need to evaluate human accuracy on that same distribution.
- Finally, you should consider a fourth validation set drawn randomly from the training data at each iteration. This validation data can be used to ensure that the model is not overfitting the training data, which a lot of machine learning libraries will do by default. If your validation data and training data are not from the same distribution, it will be hard to estimate how much you are overfitting, so having a separate validation set to check for overfitting is a good idea.
- The downside is the human-labeling cost for up to four validation data sets.
- The figure shows that margin of confidence and ratio sample some items that have only pairwise confusion, which reflects the fact that the algorithms target only the two most likely labels. By contrast, entropy maximizes for confusion among all labels, which is why the highest concentration is between all three labels.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yKaP9LNvBZ_ZMiYcwBAlAwPkV6wtit0kA3GqKEGZGYgkrZho_CsYg7P-u7EIyvFiFaIokY6h7HfWVWg1Y8kJLbnnLZCZmq9bbThi784kxOoU=/CH03_F10_Munro.png)


![](https://readwise.io/reader/pcei/gAAAAABo4a-yiW75zG-xgKvCYg_sTPse7d0vkFsYP6BZ7XRZSS8XuHJM9umwdfXl8nxlABXfJ2azFSEc8YmY15-_khqzXi_KCtVdmNEfCIFZcnSiZpwpxXc=/CH03_F11_Munro.png)


## Summary

- Four common algorithms are used for uncertainty sampling: least confidence, margin of confidence, ratio of confidence, and entropy. These algorithms can help you understand the different kinds of “known unknowns” in your models.
- You can get different samples from each type of uncertainty sampling algorithm.
- Different types of scores are output by different supervised machine learning algorithms, including neural models, Bayesian models, SVMs, and decision trees. Understanding each score will help you interpret them for uncertainty.
- Ensemble methods and dropouts can be used to create multiple predictions for the same item. You can calculate uncertainty by looking at variation across the predictions from different models.
- There is a trade-off between getting more annotations within each active learning cycle and getting fewer annotations with more cycles. Understanding the trade-offs will let you pick the right number of cycles and size of each cycle when using uncertainty sampling.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yCzZbaZ18yJMG6bqOqK4qJpwN2KUArK-23Isef1D84e8ISbh-hVv0VdJ7uhEX6au1r13AmFg2gYGknEavYEtQEiGlh6i6-U_0kr8tJQPaeP0=/CH04_F08_Munro.png)


# Diversity sampling


## Knowing what you don’t know: Identifying gaps in your model’s knowledge

- We explore four approaches to diversity sampling in this chapter:
- *Model-based outlier sampling*—Determining which items are unknown to the model in its current state (compared with uncertain, as in chapter 3)
- *Cluster-based sampling*—Using statistical methods independent of your model to find a diverse selection of items to label.
- *Representative sampling*—Finding a sample of unlabeled items that look most like your target domain, compared with your training data.
- *Sampling for real-world diversity*—Ensuring that a diverse range of real-world entities are in our training data to reduce real-world bias.
- may have seen diversity sampling referred to as stratified sampling, representative sampling, outlier detection, or anomaly detection.
- *diversity sampling* goes by different names in different fields
- Chances are that your unlabeled data is biased toward the most privileged demographics
- If you build models only on randomly sampled raw data, you could amplify that bias.
- Figure 4.1 Diversity sampling, showing items selected to be labeled that are maximally different from the existing training items and from one another. You want to sample items that are not like the items that are currently in your training data and are also not like one another.

![](https://readwise.io/reader/pcei/gAAAAABo4a-y7-DV1CP9YOUo6ue34qxJwOlWfp8vuGHV-iXB-Z1mN69ts_48kRMYm4eFXH7H-9hLX3U0uHSBu2iX6Z7UGZFhkDFzzZcJcK6q_8ojXYqUL9Q=/CH04_F01_Munro.png)


## Model-based outlier sampling

- Now that we can interpret our model, we can query our model to find outliers. A *model outlier* in a neural model is defined as the item with the lowest activation in a given layer. For our final layer, this activation is the logits.
- The biggest barrier to choosing the right metric for determining an outlier is knowing the distribution of values from your neurons.
- You were taught in high school that any data point greater than three standard deviations from the mean is an outlier, but this is true only for normal distributions. Unfortunately, your linear activation functions are not creating normal distributions: they should be bimodally distributed if they are modeling your task accurately. If you’ve investigated models in the past, you’ll also know that some of the neurons might be modeling noise or simple passing through values and can vary even when you train a model twice on identical data. Furthermore, unless you have a simple architecture, you will have different activation functions for different parts of your network, so they will not be directly comparable.
- Just like we couldn’t trust the absolute values for confidence for uncertainty sampling, we can’t trust the absolute values of our neurons to determine outliers. But just like we could trust the ranked order confidence to find the most uncertain predictions, we can trust the ranked order of neuron activation to find the least activated. Rank order is a robust method that lets us avoid determining the actual distribution of activation in every neuron.

## Cluster-based sampling

- Clustering can help you target a diverse selection of data from the start. The strategy is fairly straightforward: instead of sampling training data randomly to begin with, we also divide our data into a large number of clusters and sample evenly from each cluster.
- So clustering is saving time and increasing diversity.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yilKFIM2gk3ZLNwRLOmUAIQjK0hDX_tOZQulTlQsalrLrIvOEDnBTpf55aJi6kg2qcdMbnnh9ATEgNxjigeSlHwTlx3K7xnMJpmKjQsR4XDk=/CH04_F04_Munro.png)

- We will sample from clusters in three ways:
- • *Random*—Sampling items at random from each cluster. This strategy is close to random sampling but will spread out our selection across our feature space more evenly than purely random sampling. • *Centroids*—Sampling the centroids of clusters to represent the core of significant trends within our data. • *Outliers*—Sampling the outliers from our clustering algorithm to find potentially interesting data that might have been missed in the clusters. Outliers within clustering are sometimes known as *proximity-based* outliers.

## Representative sampling

- *Representative* *sampling* refers to explicitly calculating the difference between the training data and the application domain where we are deploying the model.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yCzZbaZ18yJMG6bqOqK4qJpwN2KUArK-23Isef1D84e8ISbh-hVv0VdJ7uhEX6au1r13AmFg2gYGknEavYEtQEiGlh6i6-U_0kr8tJQPaeP0=/CH04_F08_Munro.png)


## Summary

- This chapter covered four common approaches to diversity sampling: model-based outlier sampling, cluster-based sampling, representative sampling, and sampling for real-world diversity. These techniques can help you understand the kinds of “unknown unknowns” in your models.
- Model-based outlier sampling allows you to sample items that are unknown to your model in its current state, helping you expand your model’s knowledge where there are currently gaps.
- Cluster-based sampling allows you to sample items that are statistically representative of the entire distribution of your data, helping you expand your model’s knowledge to capture all the meaningful trends in your data, including the rarer ones that would likely be missed with random sampling.
- Representative sampling can be used to sample items that are maximally representative of where you are going to deploy your model, helping you adapt your model to domains that are different from your current training data, which is a common problem in real-world machine learning.
- Interpreting the layers of a neural model for diversity sampling lets you access as much information as possible for active learning, giving you more options for calculating model outliers and providing a building block for advanced transfer learning techniques.
- The strategies for deciding how many items should be reviewed by humans when implementing diversity sampling is different from uncertainty sampling, because in some cases, they can be adaptive within each iteration of active learning. Adaptive sampling methods allow you to make the human-in-the-loop machine learning feedback loop more efficient because you don’t have to wait for your model to retrain.

# Advanced active learning


## Combining uncertainty sampling and diversity sampling


![](https://readwise.io/reader/pcei/gAAAAABo4a-yZioFjI9nv2xUYVQJYZ88kJ1dPL97oWHsaQATBYt-w_Kvyk9TZEnA2t4Erd84m3mvgWohQYaHxiE6SseldmRYMY1MXt01duzDLqoiQEuFVGk=/CH05_F01_Munro.png)

- Figure 5.1 One possible result of combining uncertainty sampling and diversity sampling. When these strategies are combined, items near diverse sections of the decision boundary are selected. Therefore, we are optimizing the chance of finding items that are likely to result in a changed decision boundary when they’re added to the training data.
- The most common way that uncertainty sampling and diversity sampling are combined in industry is takes a large sample from one method and further filter the sample with another method.
- If you sampled the 50% most uncertain items with least confidence sampling and then applied cluster-based sampling to sample 10% of those items, you could end up with a sample of 5% of your data more or less like those in figure 5.1: a near-optimal combination of uncertainty and diversity.

![](https://readwise.io/reader/pcei/gAAAAABo4a-ys5JLsW6Pgoq0dw4d9Sj629tMUZrees7BxITyqqJgddV7D4IZvT4pS-Ioh54tZVyWEB9A806V7wL0AH_jiulnKJSVFckvln4RutMUVHk-DYA=/CH05_F02_Munro.png)

- There are too many possible combinations of active learning techniques to cover in this book, but by this stage, you should have a good idea of how to combine them. Here are some starting points
- *Combining uncertainty sampling and representative sampling*—You can sample items that are most representative of your target domains and are also uncertain. This approach will be especially helpful in later iterations of active learning. If you used uncertainty sampling for early iterations, your target domain will have items that are disproportionately far from the decision boundary and could be selected erroneously as representative.
- *Combining model-based outliers and representative sampling*—This method is the ultimate method for domain adaptation, targeting items that are unknown to your model today but are also relatively common in your target domain.
- *Combining sampling from the highest-entropy cluster with margin of confidence sampling (or some other uncertainty metrics*—You can find the cluster with the highest entropy and then sample all the items within it that fall closest to a decision boundary.
- *Combining ensemble methods or dropouts with individual strategies*—You may be building multiple models and decide that a Bayesian model is better for determining uncertainty, but a neural model is better for determining model-based outliers. You can sample with one model and further refine with another.

## Applying active transfer learning to representative sampling

- We can apply the same active transfer learning principles to representative sampling. That is, we can adapt our models to predict whether an item is most like the application domain of our model compared with the current training data.
- To summarize those strengths and weaknesses again: representative sampling is effective when you have all the data in a new domain, but if you’re adapting to future data that you haven’t sampled yet, your model can wind up being stuck in the past.
- also the most prone to noise of all the active learning strategies in this book.
- Finally, active transfer learning for representative sampling can do more harm than good if you apply it in iterations after you use uncertainty sampling

## Active transfer learning for adaptive sampling

- The final algorithm for active learning in this book is also the most powerful; it is a form of uncertainty sampling that can be adaptive within one iteration of active learning.
- *Active transfer learning for adaptive sampling* (ATLAS) is an exception, allowing adaptive sampling within one iteration without also using clustering to ensure diversity.

![](https://readwise.io/reader/pcei/gAAAAABo4a-yBEuMkNanIdtbOZYIM86j3aqpwsuwjc9nZodUO-UFC3aXz-c6UOmp2PemKSp8lijx81k9n9prkV0nQKopou5zccNySjHC3E-5z7JASvZC21o=/CH05_F12_Munro.png)


## Summary

- You have many ways to combine uncertainty sampling and diversity sampling. These techniques will help you optimize your active learning strategy to sample the items for annotation that will most help your model’s accuracy.
- Combining uncertainty sampling and clustering is the most common active learning technique and is relatively easy to implement after everything that you have learned in this book so far, so it is a good starting point for exploring advanced active learning strategies.
- Active transfer learning for uncertainty sampling allows you to build a model to predict whether unlabeled items will be labeled correctly, using your existing model as the starting point for the uncertainty-predicting model. This approach allows you to use machine learning within the uncertainty sampling process.
- Active transfer learning for representative sampling allows you to build a model to predict whether unlabeled items are more like your target domain than your existing training data. This approach allows you to use machine learning within the representative sampling process.

# Applying active learning to different machine learning tasks

- This chapter covers • Calculating uncertainty and diversity for object detection • Calculating uncertainty and diversity for semantic segmentation • Calculating uncertainty and diversity for sequence labeling • Calculating uncertainty and diversity for language generation • Calculating uncertainty and diversity for speech, video, and information retrieval • Choosing the right number of samples for human review

## Applying active learning to sequence labeling

- *Sequence* *labeling* is machine learning applied to labeling spans within a sequence and is one of the most common tasks in NLP

## Choosing the right number of items for human review

- For advanced active learning techniques, the principles that you have already learned apply. You can make some of the active learning strategies, such as representative sampling, adaptive within an active learning iteration, but most combinations of techniques still produce the most benefit when you retrain the model with the newly annotated data.
- You probably need to sample a minimum number of items as a result of drawing from a certain number of clusters or stratification to real-world demographics. Your maximum number of items per iteration will vary depending on data type.
- If your machine learning models can learn from partially annotated data, you are going to make your systems a lot more efficient.
- You might have thousands of images of bicycles and animals, but each image has dozens of cars and pedestrians on average too. Ideally, you’d like to be able to annotate only the bicycles and animals in those images and not spend more than 10 times the resources to make sure that all the cars and pedestrians are also labeled in those same images. A lot of machine learning architectures don’t allow you to partially annotate data, however; they need to have every object annotated, because otherwise, those objects will erroneously count toward the background. You might sample the 100 bicycles and animals that maximize confusion and diversity, but then spend most of your resources annotating 1,000 cars and pedestrians around them for relatively little extra gain. There is no shortcut: if you sample only images without many cars or pedestrians, you are biasing your data toward certain environments that are not representative of your entire dataset.
- If you are stuck with systems that need full annotation for every image or document, you want to be extra-careful to ensure that you are sampling the highest-value items every time.
- Increasingly, it is easier to combine different models or have heterogeneous training data. You might be able to train separate models for pedestrians and cars, and then have a model that combines them via transfer learning.
- The best solution to the problem of needing to annotate only a few objects/spans in a large image/document is to incorporate machine learning into the annotation process. It might take an hour to annotate an entire image for semantic segmentation, but only 30 seconds to accept/reject every annotation.

## Working with the people annotating your data

- The type of workforce you need will depend on your task, scale, and urgency.
- *Annotation* is the process of creating training data for your models. For almost all machine learning applications that are expected to operate autonomously, you will need more data labels than it is practical for one person to annotate, so you will need to choose the right workforce(s) to annotate your data and the best ways to manage them.
- *Data annotation* is the process of creating unlabeled data, either by labeling unlabeled data or reviewing labels generated from a model.
- One piece of advice: start your data strategy with your algorithm strategy. It takes as long to refine your annotation strategy and guidelines as it does to create your algorithm architecture and tune your hyperparameters, and your choice of algorithm and architecture should be informed by the type and volume of annotations that you expect.
- If you can get your data labels for free from your end users, you have a powerful business model! The ability to get labels from end users might even be an important factor in deciding what products you need to build.
- For many applications, users provide feedback that can power your machine learning models. Many applications that seem to rely on end users for training data, however, still use large numbers of annotators. The most obvious, widespread example is search engines. Whether you are searching for a website, a product, or a location on a map, your choice from the search results helps that search engine become smarter about matching similar queries in the future.
- best way to start thinking about the amount of data needed for your project is in terms of orders of magnitude. In other words, the number of annotations needed to grow exponentially to hit certain milestones in model accuracy.
- • 100 (10N) annotations—Meaningful signal • 1,000 (10N+1) annotations—Stable accuracy • 10,000 (10N+2) annotations—Deployed model • 100,000 (10N+3) annotations—State-of-the-art model

![](https://readwise.io/reader/pcei/gAAAAABo4a-yZthKT4egkdz6UaXjmyaLdswGN-PKuOwvhSBy1xakmBa9ZQlykPkFZLdVg-jisGjj66sawtDTv1Mww8o-H7UOo_UqLGEzYXeBrnilA3scxpk=/CH07_F07_Munro.png)


## Quality control for data annotation

- how do you decide on the right threshold for majority agreement among annotators when all those annotators have seen different combinations of tasks? How do you know when your overall agreement is so low that you need to change your guidelines or the way you define your task?
- This chapter and the next two chapters use the concepts of *expected* and *actual* annotation accuracy. If, for example, someone guessed randomly for each annotation, we would expect them to get some percentage correct, so we adjust the actual accuracy to account for a baseline of random chance.

## Comparing annotations with ground truth answers

- The simplest method for measuring annotation quality is also one of the most powerful: compare the responses from each annotator with a set of known answers, called *ground truth answers.* An annotator might annotate 1,000 items, of which 100 have known answers. If the annotator gets 80 of those known answers correct, you can estimate that they are 80% accurate over the 1,000 items.
- If you are creating your evaluation data and training data at the same time and don’t have good quality controls, you will end up with the same kinds of errors in both your training data and evaluation data.
- The most common cause of errors is wrong items sampled for ground truth. Three general sampling strategies identify the items that should become ground truth data:
- *A random sample of data*—You should evaluate the accuracy of your individual annotators on random data. If a random selection isn’t possible, or if you know that a random sample is not representative of the population that your application is serving, you should try to get a sample that is as close to representative as possible.
- *A sample of data with the same distribution of features and labels as the batch of data that is being annotated*—If you are using active learning, this sample should be a random sample from your current iteration of active learning, which allows you to calculate the (human) accuracy of each sample of data and, by extension, the accuracy of the dataset as a whole.
- *A sample of data found during the annotation process that is most useful for annotation guidelines*—These guidelines often exemplify important edge cases that are useful for teaching the annotators to be as accurate as possible.
- You must be confident that your ground truth items have few errors; otherwise, you will create misleading guidelines and won’t have reliable accuracy metrics, resulting in bad training data.
- The basic math for agreement with ground truth data in labeling tasks is simple: the percentage of known answers that an annotator scored correctly.
- you are familiar with the literature on quality control for annotation, you know that a metric that is normalized according to the expected behavior is often called *chance-corrected* or *chance-adjusted*.
- When a person is first working on a task, they will not have intuition about which label is more frequent, so they are more likely to be closer to random labeling. But after some time, they realize that one label is much more frequent than the others and may feel safe guessing that label when they are uncertain.

## Interannotator agreement

- The “wisdom of the crowd” produces data that is more accurate than any one human. For more than a century, people have studied how to aggregate the judgments of multiple people into a single, more accurate result.
- So when data scientists brag that their model is more accurate than humans, they often mean that their model is more accurate than the agreement among the annotators, which is called *interannotator agreement*. Model accuracy and annotator agreement are two different numbers that shouldn’t be compared directly, so try to avoid making this common mistake.
- Interannotator agreement is typically calculated on a –1 to 1 scale, where 1 is perfect agreement, –1 is perfect disagreement, and 0 is random-chance labeling.

![](https://readwise.io/reader/pcei/gAAAAABo4a-zu7_nhZzEpxicvZbl8rFPRnaIcqObdPPj1uVEDf1DwA1nAdShV1qdFMlsjdWlVOsKVPznQLwZ9qRHMG0L3bbgMXYNqs5aDNPJ2ei1KsnFhwQ=/CH08_F06_Munro.png)

- Agreement is typically on a –1 to 1 scale, where 1 is perfect agreement, –1 is perfect disagreement, and 0 is random distribution. The resulting agreement is variously known as *actual agreement, adjusted agreement*, or *agreement adjusted for random chance*.
- Benefits from calculating interannotator agreement You can use interannotator agreement as part of your human-in-the-loop machine learning strategy in multiple ways:
- *The reliability of your dataset*—Do the annotators agree with one another often enough that you can rely on the labels that have been created? If not, you may need to redesign your instructions or the task as a whole.
- *The least reliable annotators*—Do any individual annotators disagree with the others too often? They may have misunderstood the task or may not be qualified to keep taking part. Either way, you may want to ignore their past annotations and potentially get new judgments. Alternatively, an unreliable annotator may in fact have valid but underrepresented annotations, especially for subjective tasks
- *The most reliable annotators*—The annotators with high agreement are likely to be the most accurate for your task, so identifying these people for potential reward and promotion is helpful.
- *Collaboration between annotators*—Do any annotators agree nearly perfectly? They might be sharing notes innocently because they sit near one another, in which case you need to remove those responses from any calculations of agreement that assumes independence. On the other hand, this result may be evidence that a bot is duplicating one person’s work so that the person wrongly gets paid twice. Regardless of the underlying cause, it is helpful to know when two sets of answers are only one set that has been repeated.
- *An annotator’s consistency over time*—If you give the same task to the same person at different times, do they give the same result? This metric, known as *intra-annotator agreement* can be evidence that an annotator is not paying attention, that your task has ordering effects, and/or that the task is inherently subjective. Also, the annotator may be genuinely changing their mind as they see more data, which is known as *concept evolution.*
- *Creating examples for the instructions*—You can assume that items with high agreement among a large number of annotators are correct and let these items become examples in the guidelines for new annotators. Because you run two risks with this strategy—some errors will still get through and propagate, and only easier tasks will get through with higher agreement—you should not use it as your only strategy for creating ground truth data.
- *Evaluating the inherent difficulty of a machine learning problem*—In general, if the task is hard for humans, it will be hard for your model. This information is especially helpful for adapting to new domains. If your data historically has 90% agreement, but data from a new source has only 70% agreement, this result tells you to expect your model to be less accurate on data from that new source.
- *Measuring the accuracy of your dataset*—If you know the individual reliability of each annotator and how many people have annotated each item, you can calculate the probability that any given label will be annotated incorrectly. From this result, you can calculate the overall accuracy of your data. Taking individual annotator accuracy into account gives you a better upper boundary for the accuracy of a model that is trained on the data, compared with simple interannotator agreement. Models can be more or less sensitive to noise in the training data, so the limit is not a hard one. The limit *is* a hard limit on how precisely you can measure your model’s accuracy, because you can’t calculate your model’s accuracy to be higher than your dataset’s accuracy.
- *Measuring natural variation*—For some datasets, lack of agreement is a good thing because it can indicate that multiple annotation interpretations are valid. If you have a task that is subjective, you may want to ensure that you have a diverse selection of annotators so that no one set of social, cultural, or linguistic backgrounds is inadvertently resulting in biased data.
- *Escalating difficult tasks to experts*—This example was covered in chapter 7, and we return to it again in section 8.5. Low agreement between less-qualified workers might mean that the task should be routed to an expert automatically for review.
- Don’t use agreement as the only measure of accuracy You should not rely on interannotator agreement alone to find the correct label for your data; always use interannotator agreement in combination with ground truth data.
- *Krippendorff’s* *alpha* is a method that aims to answer a simple question: what is the overall agreement in my dataset?
- The simple interpretation of Krippendorff’s alpha is that it is a [–1,1] range, which can be read as follows: • *>0.8*—This range is reliable. If you apply Krippendorff’s alpha to your data, and you get a result of 0.8 or higher, you have high agreement and a dataset that you can use to train your model. • *0.67–0.8*—This range has low reliability. It is likely that some of the labels are highly consistent and others are not. • *0–0.67*—At less than 0.67, your dataset is considered to have low reliability. Something is probably wrong with your task design or with the annotators. • *0*—Random distribution. • *–1*—Perfect disagreement.
- Krippendorff’s alpha also has the nice property that it can be used for categorical, ordinal, hierarchical, and continuous data.
- The expected agreement for Krippendorff’s alpha is the data frequency: the sum of the squares of the frequency of each label for a labeling task. The actual agreement for Krippendorff’s alpha comes from the average amount that each annotation agrees with the other annotations for the same task. Krippendorff’s alpha makes a slight adjustment to the average, epsilon, to account for the loss of precision given the finite number of annotations.
- You may encounter alternatives to Krippendorff’s alpha in the literature, such as Cohen’s kappa and Fleiss’s kappa. Krippendorff’s alpha is generally seen as being a refinement of those earlier metrics. The differences are details such as whether all errors should be punished equally, the correct way to calculate the expected prior, the treatment of missing values, and how to aggregate the overall agreement (aggregating per annotation, like Krippendorff’s alpha, or per task/annotator, like Cohen’s kappa).
- Agreement at individual annotator level can be useful in multiple ways. For one thing, it can tell you how reliable each annotator is. You can calculate agreement at the macro level, calculating an annotator’s reliability across every response they made, or you may want to see whether they have higher or lower agreement for certain labels or segments of the data. This result might tell you that the annotator is more or less accurate or may highlight a diverse set of valid annotations.
- The simplest metric for agreement between annotators is to calculate how often each annotator agrees with the majority of people for a given task.
- The per-annotator agreement with the most common annotation for each task (majority agreement).
- This method is the simplest way to calculate agreement between annotators; it can be effective when you have a large number of annotators per task but is rarely used for creating training data due to budget constraints.
- Majority agreement, as shown in figure 8.11, looks at the number of times a person agrees with the most commonly annotated label for each task. This result can also be calculated as a count of the fraction of times that a person agrees with the majority, but it is a little more accurate when normalized for agreement on a per-annotation basis.
- Ideally, you have some ground truth labels for your dataset, so you can use these labels to plot the errors in a confusion matrix. This confusion matrix is identical to the kind that you use for machine learning models, except that it is the pattern of human errors in place of model errors.
- The ground truth data allows you to calculate the following: for each incorrect annotation, what % of annotations for the task are also incorrect?
- When annotators disagree, you are essentially converging a probability distribution across all the potential labels.
- Let’s assume that we’re calculating confidence for task 3 and that we have 90% confidence in every annotator: Pedestrian = 3 * 0.9 = 2.7 Cyclist = 2 * 0.9 = 1.8 Confidence in Pedestrian = 2.7 / (2.7 + 1.8) = 0.6 Confidence in Cyclist = 1.8 / (2.7 + 1.8) = 0.4 Another way to think of this calculation is that because we’re equally confident in everyone in this example, three-fifths of the annotators agree, so we are 3/5 = 60% confident.
- When you have the probability distribution for your labels for a given task, you need to set a threshold for when not to trust a label and decide what to do if you don’t trust the label. You have three options when you don’t trust the label: • Assign the task to an additional annotator, and recalculate the confidence to see whether the confidence is high enough. • Assign the task to an expert annotator to adjudicate on the correct label (more on this topic in section 8.4). • Exclude this item from the dataset so that a potential error won’t produce errors in the model.
- One of the most common methods of quality control is to engage SMEs to label the most important data points. Generally, experts are rarer and/or more expensive than other workers, so you typically give some tasks only to experts, often for one of these reasons: • To annotate a subset of items to become ground truth examples for guidelines and quality control • To adjudicate examples that have low agreement among nonexpert annotators • To annotate a subset of items to become machine learning evaluation items, for which human label accuracy is more important • To annotate items that are known to be important for external reasons. If you are annotating data from your customers, for example, you may want expert annotators to focus on examples from the customers who generate the most revenue for you
- One of the most effective ways to get higher-quality labels is to break a complicated task into smaller subtasks. You can get several benefits from breaking your task into simpler subtasks: • People generally work faster and more accurately on simpler tasks. • It is easier to perform quality control on simpler tasks. • You can engage different workforces for different subtasks.

## Summary

- Ground truth examples are tasks that have known answers. By creating ground truth examples for the dataset, you can evaluate the accuracy of annotators, create guidelines for those annotators, and better calibrate other quality control techniques.
- You have many ways to calculate agreement in a dataset, including overall agreement, agreement between annotators, agreement between labels, and agreement at task level. Understanding each type of agreement will help you calculate the accuracy of your training and evaluation data and better manage your annotators.
- For any evaluation metric, you should calculate an expected result that would occur by random chance as a baseline. This approach allows you to normalize your accuracy/agreement metric to a score adjusted for random chance, which makes the score more easily comparable across different tasks.
- You will get the best results when using both ground truth data and interannotator agreement, because ground truth agreement allows you to better calibrate your agreement metrics, and agreement metrics can be applied to more annotations than is practical with ground truth alone.
- You can aggregate multiple annotations to create a single label for each task. This approach allows you to create the training data for your machine learning models and calculate the likelihood that each label is correct.
- Quality control by expert review is one common method of resolving disagreements between annotators. Because experts tend to be rare and/or expensive, they can focus mostly on the tough edge cases and the cases that will become part of the guidelines for other annotators.
- Multistep workflows allow you to break an annotation task into simpler tasks that flow into one another. This approach can create annotations faster and more accurately and allow easier-to-implement quality control strategies.

# Advanced data annotation and augmentation

- Because most quality control strategies for data annotations are statistically driven decision processes, machine learning can be used for the quality control process itself.
- Four types of machine learning-driven quality controls are introduced here, all of which use the annotator’s performance on ground truth data and/or agreement as training data: • Treating the model predictions as an optimization task. Using the annotator’s performance on the ground truth data, find a probability distribution for the actual label that optimizes a loss function. • Creating a model that predicts whether a single annotation by an annotator is correct or incorrect. • Creating a model that predicts whether a single annotation by an annotator is likely to be in agreement with other annotators. • Predicting whether an annotator is actually a bot.

## Model predictions as annotations

- The simplest approach to semi-automating annotation is to treat the model’s predictions as though the model was an annotator. This process is often called *semi-supervised learning*, although that term has been applied to pretty much any combination of supervised and unsupervised learning.
- You can trust a model’s predictions or incorporate the model’s predictions as one annotator among many. The two approaches have different implications for how you should treat model confidence and the workflows that you might implement to review the model’s output, so they are explored separately.
- There are two common problems with many academic papers about automated labeling, whether it is using model confidence, a rule-based system, or some other method. First, they almost always compare the auto-labeling methods with random sampling.
- Second, the papers typically assume that the evaluation data already exists, which is true for academic datasets. In the real world, however, you still need to set up annotation processes to create your evaluation data, manage the annotators, create the annotation guidelines, and implement quality control on the annotations. If you are doing all this for your evaluation data, why not put in the extra effort in the annotation component to create training data too?
- The simplest way to use a model as an annotator is to trust the model predictions as labels, trusting predictions beyond a certain confidence threshold as labels.
- If you have an existing annotated dataset and are not certain that all the labels are correct, you can use the model to find candidates for human review. When your model predicts a different label from the ones that have been annotated, you have good evidence that the label might be wrong and that a human annotator should review that label.

## Search-based and rule-based systems

- Among the biggest advantages of rule-based systems are the senses of ownership and agency that they give annotators, especially ones who are SMEs, making them feel as though they are in the driver’s seat. I have built rule-based systems on top of machine learning systems specifically because the analysts using the system wanted a way to input their expert knowledge directly into the system.

## Light supervision on unsupervised models

- There are other ways to convert this type of model to a fully supervised one: • Recursively cluster for the clusters containing items with more than one label. • Switch to uncertainty sampling after initially using the methods in figure 9.16. • De-weighting or removing the auto-labeled items over time.
- “Learning from Noisy Singly-Labeled Data,” by Ashish Khetan, Zachary C. Lipton, and Anima Anandkumar, gives a detailed method for estimating confidence in annotations by using both annotator performance and model predictions
- For current research on rule-based systems, see “Snorkel: Rapid Training Data Creation with Weak Supervision,” by Alexander Ratner, Stephen H. Bach, Henry Ehrenberg, Jason Fries, Sen Wu, and Christopher Ré
- For a nonfree resource that dives deep into these technologies, see Russell Jurney’s upcoming (at the time of publication) book *Weakly Supervised Learning: Doing More with Less data* (O’Reilly).

## Summary

- Subjective tasks have items with multiple correct annotations. You can elicit the set of valid responses that people might give from the annotators and then use methods such as BTS to discover all the valid responses and avoid penalizing correct but rarer annotations.
- Machine learning can be used to calculate the confidence of a single annotation and to resolve disagreements among annotators. For many annotation tasks, simple heuristics are not enough to accurately calculate annotation quality or to aggregate the annotations of different people, so machine learning gives us more powerful ways to create the most accurate labels from human annotations.
- The predictions from a model can be used as the source of annotations. By using the most confident predictions from a model or by treating a model as one annotator among other annotators, you can reduce the overall number of human annotations that are needed. This technique can be especially helpful when you want to take the predictions from an old model and use them in a new model architecture and when annotation is a time-consuming task compared with accepting or rejecting model predictions.
- Embeddings and contextual representations allow you to adapt the knowledge from existing models into your target model as feature embeddings or tuning pretrained models. This approach can inform your annotation strategy. If you can find a related task that is 10 times or 100 times faster to annotate than your target task, for example, you might get a more accurate model if you devote some resources to the simpler task and use the simpler task as an embedding in the actual task.
- Search-based and rule-based systems allow you to quickly filter and possibly label your data. These systems are especially useful for annotating a model quickly with noisy data and finding important low-frequency data to annotate.
- Light supervision on unsupervised models are common ways that annotators, especially SMEs, bootstrap a model from a small number of labels or perform exploratory data analysis when the goal is improved human understanding of the data, not necessarily a supervised model.
- Synthetic data, data creation, and data augmentation are related strategies that create novel data items, especially useful when the available unlabeled data does not contain the required diversity of data, often because data is rare or sensitive.
- There are several ways to incorporate annotation uncertainty into a downstream model: filtering out or de-weighting items with uncertain label accuracy, including the annotator identities in the training data, and incorporating the uncertainty into the loss function while training. These methods can help prevent annotation errors from becoming unwanted biases in your models.
- Figure 10.4 For wisdom of the crowds, you need the crowds. This graph shows how often the average score of the annotators is closer to the ground truth score than most annotators. If there are three annotators, about 70% of the time, the average score of those annotators will be closer to the actual score than at least two of those annotators. It is rare to have more than ten annotators for each item when creating training data, and this graph shows that the average annotation is better than most annotators about 90% of the time when there are ten annotators.

![](https://readwise.io/reader/pcei/gAAAAABo4a-zwJOQYINScx9O3n-Lk9MPEc4aY3h1qZbNbZIU3DK6PU90rNg9I6kF5fclzDvvjMTFahjg7bMiFAP6-Uzo1-BdMpo2ETfnRwYMr34Jdyl5Bn8=/CH10_F04_Munro.png)


# Interfaces for data annotation

- For any interface, the wrong design can affect the quality and efficiency of the annotation process as a whole.

## Basic principles of human–computer interaction

- Do annotators feel that the interface allows them to annotate or express all the information that they think is important?
- For simple labeling tasks, good affordance and feedback require using existing components according to their recommended purposes. Any framework you are using should have elements for single or multiple selections, text inputs, drop-down menus, and so on.
- Autocomplete, for example, has gained popularity only recently. Many websites that used large menu systems or radio buttons five years ago now use autocomplete. Your annotation interfaces should build on current conventions, whatever those conventions are when you are building the interface.
- Try to keep all the components of an annotation task on the screen so that annotators don’t have to scroll. Also, try to keep all the elements (instructions, input fields, item being annotated, and so on) in the same place for each annotation.
- The instructions and guidelines for annotation can create a problem with fitting all information on the screen. You want detailed instructions for the annotators, but the instructions will take up a lot of the screen. Also, the instructions become redundant after an annotator has completed enough tasks to remember them, so it can be frustrating for annotators to keep scrolling past instructions that they no longer need. The simplest solution is to make the instructions collapsible so that they can be expanded when needed.
- Keyboard shortcuts are central to almost all annotation projects but are easy to overlook. Keyboard shortcuts help with navigation and inputs.

## Priming in annotation interfaces

- In addition to deciding on the right interface, you need to consider how order effects and other contextual factors might influence the annotations.
- The most significant priming problem for annotation is repetition. Annotators might change their interpretation of an item based on the items that they have seen previously.
- With a large amount of repetition, attention and fatigue also become issues. Lack of diversity in data can lead to mindlessly clicking the same annotation even when it might be the wrong one. In many ordered datasets, the items nearest one another come from the same source and/or time, so randomizing the order of items is a simple way to minimize this effect.
- For a task such as sentiment analysis, you might ask annotators to look at thousands of examples before beginning to annotate so that they have calibrated their ratings decisions first.
- Priming hurts most when annotation requires subjective or continuous judgments.

## Combining human and machine intelligence

- You should always provide a mechanism for annotators to give you feedback about the specific tasks on which they are working. Annotators can give feedback on many aspects of the task, such as the intuitiveness of the interface, the clarity and completeness of the instructions, the ambiguity of some data items, the limitations of their knowledge of certain items, and other patterns and trends in the data that you may not have noticed.
- Ideally, you should include the option for annotators to give feedback about a task within that task, perhaps via a simple free-text field.
- Feedback goes both ways: you should give feedback to annotators about how the annotations are being used.
- Annotators’ accuracy will improve if they have a better idea of the task that the machine learning model will be performing downstream.
- If you are annotating sentiment, you can ask the annotator to highlight which words contribute to their interpretation of positive or negative sentiment. An interesting extension to highlighting is to ask the annotator to edit those words to express the opposite sentiment. This process—changing the label with the fewest possible edits—is known as *adversarial annotations.*

## Recasting continuous problems as ranking problems


![](https://readwise.io/reader/pcei/gAAAAABo4a-z1PDkaXFM5TV0S1gw2bxbp0J5ctsRhVyXIQO87FittSmYOfwSpankolvbVeoypeI5rmVmxumTnKAIWju591e4Lu_WKLMJM9RZFyYjcnEM6Vg=/CH11_F04_Munro.png)

- a simple interface can turn a continuous task into a ranking task, which generally results in more consistent annotations. There are pros and cons attached to using ranking rather than absolute values. The benefits include: • More consistent results. Results will vary depending on your data and task but are fairly easy to test; you can implement both techniques and compare them. • Per-task time is faster. Checking a box is quicker than typing, sliding, or selecting on a continuous scale. • Performing quality control is easier for a binary classification task than a continuous task, for both objective tasks and subjective tasks with BTS.
- drawbacks:
- You get only rankings, not the actual scores, so you need some items with absolute scores.
- You need to resolve circular rankings
- Ranking every items takes more tasks. You need *N log(N)* judgments to rank every item in a dataset with *N* items.
- A binary classification task, however, is faster and more consistent.
- For a worked example, imagine that we are annotating 100,000 items. For a numerical score interface, assume that we want an average of four annotators per task and that it takes 15 seconds each on average for each task: 100,000 tasks × 4 annotators × 15 seconds = 1,667 hours For pairwise rankings, let’s assume that on average, each task needs only two annotators and takes 5 seconds: 100,000 × log(100,000) tasks × 2 annotators × 5 seconds = 1,389 hours So for around the same budget, you are likely to have a much more accurate dataset if you use a ranking approach, even though there are many more annotations in total.

## Smart interfaces for maximizing human intelligence


![](https://readwise.io/reader/pcei/gAAAAABo4a-zLqRJPU1tPdQYOMb4qUYA2TDpBy0kE9l0XLH4gQnNoPBGnnGeGHXAfLU778fb-sB5SAEkSR3F2l5xqfpMy_4fH47nthB7RhJqvgLG5TDqSbE=/11_T1.png)


![](https://readwise.io/reader/pcei/gAAAAABo4a-z5yNWpuzTXfnJ78qojrY2tZNwnq6xYi4Xz5hvDyB2VtHMOm4XM53f4N7lC9MDdSPGN2nOwiIhlW8cDRkpm8SLrB1CKigiqJDGEOXBoMxdR80=/CH11_F05_Munro.png)


![](https://readwise.io/reader/pcei/gAAAAABo4a-zxedUeltxyC1ke_7in6UWwurmQ28pIK_7Yg9MgFShK9kWAitHtVMOAgD2jRb_o4f-IWw01kAKXJbZdbQBrWPCdOQz7O3du5CH4CsYR4wFVPM=/CH11_F08_Munro.png)



