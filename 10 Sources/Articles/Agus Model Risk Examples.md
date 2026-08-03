---
type: article
status: structured
quality:
topics: [llm-risks, model-monitoring, model-calibration]
source: ""
created: 2025-03-23
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- also see https://ezyang.github.io/ai-blindspots/

- <mark style="background: #FFB8EBA6;">HOLE 1</mark>: high performing models can still be completely wrong
	- e.g. Boosting model to predict credit default
		- great results - 0.9 AUC, 0.64 F1
		- however when plotting credit-score vs default risk - model shows a big hump 
		- not a logical monotonic relationship 
	- i.e. model is making fundamentally flawed performance metrics
- <mark style="background: #FFB8EBA6;">HOLE 2</mark>: weaknesses in the aggregates
	- identify via "failure clustering" analysis - plot residuals by cluster ID 
		- i.e. model performance should be roughly the same across input segments
	- bad case = some clusters exhibit large mean absolute residuals meaning model struggles significantly for some parts of the input space 
- <mark style="background: #FFB8EBA6;">HOLE 3</mark>: harmful variable side effects 
	- some of most predictive variables can also drive most of the errors 
		- e.g. credit score especially when low to medium
			- also interacts with credit utilisation to further amplify errors - shown by main effect + interaction plot 
	- when a variable impacts strongly both model output + errors
		- your model is likely misaligned, unstable or missing critical interactions 
- <mark style="background: #FFB8EBA6;">HOLE 4</mark>: Probability miscalibration by segment 
	- models often struggle w probability miscalibrations 
		- especially for specific segments within the data 
		- absolutely critical to use techniques like <span style="color:rgb(255, 0, 247)">Platt Scaling</span>, <span style="color:rgb(255, 0, 247)">Isotonic Regression</span> or <span style="color:rgb(255, 0, 247)">Venn-Abners Prediction</span>
		- especially for tasks where accurate probabilities directly influence business decisions 
	- even if primary goal is risk ranking (AUC/Gini/KS), maintaining well-calibrated probabilities is crucial 
		- downstream actions depend on this e.g. thresholding or pricing 
	- detect via: cluster input features using absolute/squared residuals
		- to detect segments prone to errors (similar to HOLE 2)
		- calibration performance can be evaluated via <span style="color:rgb(255, 0, 247)">Brier Score</span> (lower = better)
		- this will show you miscalibration issues in segments
- <mark style="background: #FFB8EBA6;">HOLE 5</mark>: Weakness against Distribution Drift (Feature Vulnerability Analysis)
	- distribution drift = when statistical properties of the input data change over time
		- manifests with worse performance or heterogenous performance across input clusters
	- to mitigate - essential to simulate various [drift scenarios](https://modeva.ai/_build/html/_source/user_guide/testing/resilience.html) 
		- involves creating synthetic drift conditions model may encounter in real world applications 
	- metrics to employ to quantify feature drift + assess model stability 
		- Kolmogorov-Smirnov (KS)  
			- The KS test compares the cumulative distributions of two datasets and identifies any significant differences. It helps quantify how the distribution of features has altered over time.  
		- Wasserstein Distance  
			- The Wasserstein Distance, also known as Earth Mover's Distance, measures the minimum amount of work required to transform one distribution into another. It provides a clear indication of feature distribution shifts.  
		- Jensen-Shannon Distance (Population Stability Index, PSI) 
			- The Jensen-Shannon Distance is a symmetric measure of divergence between two probability distributions. The Population Stability Index (PSI) is frequently used to assess the stability of features and detect drift over time.  
	- assessing these can show which features are most vulnerable to drift 
		- + how significant the model performance could worsen in production 
		- can then devise strategies to help resilience + monitoring plan 
- <mark style="background: #FFB8EBA6;">HOLE 6</mark>: finding uncertainty in your model
	- high predictive uncertainty == model unreliability in specific regions of the input space
		- these areas are where model is unsure, decisions based on the outputs here are riskier 
	- finding risky zones in the input space 
		- use conformal prediction intervals across many test samples to find high uncertainty regions
			- typically caused by:
				- sparsity in training data, containing overlapping class distributing, have inconsistent feature patterns
			- CP gives statistically valid uncertainty intervals around predictions 
				- allows us to say "with 90% confidence, true value lies in this range"
				- when the ranges are wide == model is less certain vice versa
		- can again cluster and find regions of most uncertainty 
	- what to do with highly uncertain regions 
		- flag them for manual review 
		- use active learning - highest uncertainty cases prioritised for retraining data collection
		- adjust decision thresholds or fallback rules in uncertain areas 
		- build explainability reports to show which input features drive uncertainty
- <mark style="background: #FFB8EBA6;">HOLE 7</mark>: Benign Overfitting
	- where a model appears to perform well during development but fails in production due to noise and distribution shifts
	- **Fragility Under Noise:** Small changes in inputs can lead to large drops in performance, as shown by the AUC decline under noise perturbations
		- **Sensitive Clusters:** Certain data segments (specifically clusters 0 and 8) are particularly vulnerable to noise, highlighting where the model is most fragile.
		- **Feature Contributions:** Features like “Score,” “Utilization,” and “DTI” play a significant role in the model’s sensitivity, suggesting a need for focused feature engineering.
	- **Importance of Robustness Testing:** The post emphasizes testing under various noise conditions to identify and address weaknesses before production.
- <mark style="background: #FFB8EBA6;">HOLE 8</mark>: Masked Hidden Diversity 
	- relying on a single, all-encompassing machine learning model can be problematic because real-world data is diverse and heterogeneous
		- **Single Models Fall Short:** A monolithic model might pick up misleading relationships in certain data clusters, leading to poor overall performance.
		- **Limitations of Constrained Models:** Models with strict constraints, while logically sound, often lack the flexibility needed to handle varied data patterns.
	- **Advantages of Mixture of Experts (MoE):** By using multiple specialized "expert" models for different sub-populations, the MoE approach dynamically assigns weights based on input features. This results in improved performance, resilience to distribution drift, and better interpretability.
		- **Dynamic Collaboration:** Unlike simple segmentation that creates static groups, MoE allows experts to collaborate and adaptively combine their predictions, effectively capturing subtle variations in the data.


![[Screenshot 2025-04-07 at 8.48.27 am.webp| center | 500]]






