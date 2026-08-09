---
type: article
status: structured
quality: 1
topics: [human-in-the-loop, error-analysis]
source: https://lilianweng.github.io/posts/2024-02-05-human-data-quality/
created: 2025-06-29
published: 2024-02-05
author: Lillian Weng
flashcards: none
updated: 2025-12-28
---

# 1 Human Raters ↔ Data Quality
- high-quality data is the fuel for modern data deep learning model training
	- fundamentally human data collection involves attention to details and careful execution
- collecting human data involve a set of operation steps
	- <mark style="background: #FFB8EBA6;">Task design</mark>: design task workflows - focus to improve clarity + reduce complexity
		- detailed guidelines are helpful but very long and complicated guidelines demand a decent amount of training to be useful
	- <mark style="background: #FFB8EBA6;">Select and train a pool of raters</mark>: select annotators w similar skillset + consistency
		- training sessions likely needed
		- have regular feedback + calibrations sessions
	- <mark style="background: #FFB8EBA6;">Collect and aggregate data</mark>: usually ML techniques e.g. filter, clean, aggregate data to identify true labels
- quality assurance = actions to improve quality by acting on the quality attributes identified in the quality model

![[Screenshot 2025-06-29 at 10.02.30 am.png| center | 600]]

# 2 Wisdom of the Crowd
- <mark style="background: #FFB8EBA6;">Vox populi</mark> = Latin phrase, means the voice of people
	- paper named was the same name was published in 1907 on Nature
	- fat ox was selected and people would guess the weight of the ox in order to win a prize if the guess is close to the real number
	- middlemost estimate was treated as “the vox populi” and ended up being very close to the true value
- another experiment on mechanical turk used experts vs random crowdsourced people for labelling MT examples
	- unsurprisingly, there are spammers producing low quality annotation to only optimize the volume
	- so when measuring the agreement between experts and non-experts, different weighting schemes need to be applied to downweight the contribution of spammers: 
		- (1) “weighted by experts”: using agreement rate with experts on a gold set of 10 examples; 
		- (2) “weighted by non-experts”: relying on agreement rate with the rest of turkers on the whole dataset.
	- also found, correlation between experts’ and crowdsourced translations is higher than that between expert and MT system outputs.

# 3 Rater Agreement
- <mark style="background: #FFB8EBA6;">rater agreement</mark> = practice of obtaining reliable ground-truth labels by combining multiple annotators’ judgments
	- **weighted average** = aggregate labels by giving each annotator a proficiency weight estimated from their agreement with others
	- agreement paradigms
	    - <mark style="background: #FFB8EBA6;">majority voting</mark> = select the mode of annotator labels, treating all annotators equally
	    - <mark style="background: #FFB8EBA6;">raw agreement</mark> = percentage of other annotators who share one annotator’s label (Tratz & Hovy 2010)
		- <mark style="background: #FFB8EBA6;">cohen’s kappa</mark> = inter-rater agreement κ = (pᵒ − pᵉ)/(1 − pᵉ) that corrects for chance agreement, but chance term can be inflated when one label dominates (Landis & Koch 1977)
	    - <mark style="background: #FFB8EBA6;">probabilistic graph modeling</mark> = graphical models that jointly capture annotator reliability and true labels

# 4 Rater Disagreement & Two Paradigms
- aggregation process described above depends on an assumption that there exists *one* underlying gold answer and thus we can evaluate annotators’ performance accordingly
	- however, in many topics, especially in safety, social, or cultural areas, people can disagree and often this disagreement is valid  
		- then it comes down to how much we want to apply a strict rule versus embracing diversity.
- [Aroyo & Welty (2015)](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/2564) discussed a set of “myths” in the practice of human annotation collection and found all of them somewhat inaccurate, key findings including:
	- Often there is more than one correct interpretation for some samples. We need diverse perspectives via e.g. having multiple people to review annotation quality.
	- Disagreement is not always bad. We should reduce disagreements caused by errors or poorly designed process but other disagreements can give us rich information.
		- If it is caused by a task not well defined, we should enhance the instruction. However, a more detailed guideline does not resolve innate diversity among opinions.
	- Experts may not always be better than lay people, but they would have a big gap in terms of considering what’s important.
	- Ground truth annotations can change in time, especially those related to timely events or news.
- two annotation paradigms (Rottger et al 2021)
    - <mark style="background: #FFB8EBA6;">descriptive</mark> = embrace subjectivity, model many beliefs
        - pros = flags subjective items, preserves diversity
        - cons = rater disagreement unusable for quality metrics, unsuitable for single-output models
    - <mark style="background: #FFB8EBA6;">prescriptive</mark> = enforce one consistent belief via strict guidelines
        - pros = matches standard nlp pipelines, simplifies qc through aggregation
        - cons = costly guidelines, difficult annotator training, loses belief diversity

- topic effect = agreement higher on extreme or benign conversations, lower on nuanced ones
- [Zhang et al. (2023)](https://arxiv.org/abs/2311.04345) proposed a taxonomy of rater disagreement to analyze the root causes. Among the listed causes, disagreement due to stochastic errors or inconsistency on the individual level should be avoided
	- disentangles stable opinions from errors by anchoring each individual’s opinion to their own primary label and thus encouraging *intra*-rater consistency.
- To capture systematic disagreement among annotators when learning to predict labels, [Davani et al. (2021)](https://arxiv.org/abs/2110.05719) experimented with a multi-annotator model where predicting each annotator’s labels is treated as one sub-task
	- say classification task on annotated dataset $D = (X, A, Y)$
		- $X$ = text instances
		- $A$ = set of annotators
		- $Y$ = annotation matrix
		- $y_{i,j} \in Y$ = binary label assigned by $a_j \in A$ to the sample $x_i \in X$
		- $\bar{y_i}$ = majority vote of annotators for sample $x_i$
	- the experiment is to train a classification head on top of a pre-trained BERT model and compares 4 setups:
		- baseline = directly predict majority vote, not full annotation matrix
		- ensemble = train one model per annotator separately to predict each voter's pred, then results aggregated by majority vote
		- multi-label = learn to predict all annotator labers per sample w shared MLP layer then aggregate outputs
		- multi-task = similar to multi-label but each annotator's prediction head is learned from a seperated MLP layer such that we allocate extra compute to learn difference among annotators 

![[Screenshot 2025-06-29 at 10.04.22 am.png| center | 500]]

- <mark style="background: #FFB8EBA6;">Jury Learning</mark> (Gordon et al 2022) = simulate juries by predicting each annotator’s label conditioned on demographics, then sample chosen juror panels and aggregate their votes
	- starting with a dataset with labels and demographic characteristics of each labeler, we train a model to learn to predict labels made by every individual annotator, each as a potential juror
	- at decision time, practitioners can specify the composition of a group of jurors to determine a sampling strategy 
	- final decision is made by aggregating labels from jurors from multiple trials

# 5 Data Quality ↔ Model Training
- Once a dataset is constructed, many methods can help identify mislabels according to the training dynamics
	- influence functions = robust-statistics tool measuring parameter change when a training example’s weight is infinitesimally increased (Hampel 1974)

# 6 Prediction Changes during Training[#](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/#prediction-changes-during-training)
- Data Maps (Swayamdipta et al 2020)
    - confidence = mean model probability of the true label across epochs
    - variability = standard deviation of that probability
    - hard-to-learn = low confidence + low variability, often mislabeled
    - ambiguous = high variability, informative for out-of-distribution generalization
    - unforgettable examples = never forgotten once learned; noisy or visually uncommon samples are most forgotten
- NCV (noisy cross-validation) = split data in half, mark a sample “clean” if its label matches prediction from a model trained on the opposite half (Chen et al 2019)
    - INCV = iterative extension that gradually expands the trusted clean set and prunes noisy samples