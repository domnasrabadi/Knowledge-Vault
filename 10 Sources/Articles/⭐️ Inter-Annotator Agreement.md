---
type: article
status: structured
quality: 1
topics: [human-in-the-loop, evaluation-metrics, error-analysis]
source: ""
created: 2025-12-07
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# Data Annotation: People, Process, and Agreement

## Hiring and Briefing Annotators
- **Task**: Humans read reviews and label them as *positive*, *negative*, or *neutral*.
- **Why this step is critical**: Human judgments are subjective and depend on:
  - Language proficiency (native vs. second-language)
  - Experience and domain knowledge
  - Phenomena that are hard for both people and models (e.g., sarcasm)
- **Guidelines**:
  - Provide **clear annotation guidelines** with **lots of examples**, including **edge cases** (e.g., sarcasm).
  - Consider collecting **extra signals** beyond the main label (e.g., *“Is this sarcastic?”*) to use as:
    - Auxiliary features/signals for the model, or
    - Labels for future/related tasks.

## Reducing Subjectivity with Multiple Annotators
- **Wisdom of crowds**: Have **>1 annotator** label the **same example**.
- **Benefits**:
  - Majority vote often yields a more reliable “gold” label.
  - **Disagreement flags hard examples** worth review; these are valuable edge cases for training.
- **Practical rule used in industry**:
  - With 3 annotators, use **majority vote** (e.g., 2 vs. 1) to select the final label.

## Using Disagreement to Improve Training
- Examples with frequent disagreement are likely **difficult**.
- Optionally **up-weight** such examples in training to help the model learn critical edge cases.

## Measuring Inter-Annotator Agreement (IAA)
- **Metric**: Cohen’s $\kappa$
  - Captures both **observed agreement** and **chance agreement**.
  - **Range**: $-1$ to $+1$ (in practice here, typically $0$ to $1$).
- **Intuition**:
  - $ \kappa = 1 $: perfect agreement
  - $ \kappa = 0 $: agreement equals chance
  - $ \kappa < 0 $: worse than chance (rare in this context)

### Definition
- $\text{Pr}(a)$: observed agreement between annotators (proportion of items where labels match).
- $\text{Pr}(e)$: expected agreement **by chance**, based on annotators’ label marginals.
- **Formula**: $\kappa = \dfrac{\text{Pr}(a) - \text{Pr}(e)}{1 - \text{Pr}(e)}$

### Heuristic Threshold (Industry Practice)
- For this task, a **$\kappa \ge 0.80$** is often treated as **sufficient confidence** that label quality is good enough to proceed.
- Note: A high $\kappa$ **does not** imply **unanimous** agreement on every item.

---

# From lecture notes
- annotation
	- process of creating datasets for specific tasks where input text gets labelled w output 
		- e.g. given annotation guidelines, produce labels
			- "I love being ignored" → `sarcasm = True, sentiment = Negative`
			- "I love being complimented" → `sarcasm = False, sentiment = Positive`
	- evaluation: **inter-annotator agreement (IAA)**
		- estimates the quality of a labelled dataset
		- Cohen's Kappa is one metric to measure IAA 
			- more useful than simple % agreement, factors out agreement that might occur randomly 
			- by compensating for chance agreement, more robust measure of consistency + reliability of labelled data 


>[!example] Cohen's Kappa
> $$
> \begin{gather}
> \text{Cohen's Kappa} \\ \ \\ 
> \Large \kappa = \frac{\text{Pr}(a) - \text{Pr}(e)}{1-\text{Pr}(e)}
> \end{gather}
> $$
> - where 
> 	- Pr(a) = actual observed agreement between annotators
> 	- Pr(e) = agreement expected purely by chance
> - can observe results into various levels of agreement
> 
> | Value of Kappa | Level of Agreement | % of Data that are Reliable |
> | -------------- | ------------------ | --------------------------- |
> | 0–.20          | None               | 0–4%                        |
> | .21–.39        | Minimal            | 4–15%                       |
> | .40–.59        | Weak               | 15–35%                      |
> | **.60–.79**    | **Moderate**       | **35–63%**                  |
> | **.80–.90**    | **Strong**         | **64–81%**                  |
> | Above .90      | Almost Perfect     | 82–100%                     |

### Full Example
- suppose 2 annotators A & B label the same $N$ items into $K$ classes
	- let $n_{ij}$ = count of items A put in class $i$ AND B put in class $j$
	- define row and col totals
		- $n_{i\bullet}=\sum_{j} n_{ij}$ (A’s total for class (i))
		- $n_{\bullet j}=\sum_{i} n_{ij}$ = B’s total for class (j))
		- $N=\sum_{i}\sum_{j} n_{ij}$

| A \ B | Class 1 | Class 2 | … | Class K | Row total |
|---|---:|---:|---:|---:|---:|
| **Class 1** | $n_{11}$ | $n_{12}$ | … | $n_{1K}$ | $n_{1\bullet}$ |
| **Class 2** | $n_{21}$ | $n_{22}$ | … | $n_{2K}$ | $n_{2\bullet}$ |
| … | … | … | … | … | … |
| **Class K** | $n_{K1}$ | $n_{K2}$ | … | $n_{KK}$ | $n_{K\bullet}$ |
| **Col total** | $n_{\bullet1}$ | $n_{\bullet2}$ | … | $n_{\bullet K}$ | $N$ |

- observed agreement
	- this is just the fraction on the diagonal → where they agreed on the class
		- highlight the diagonal $n_{11}, n_{22}, \ldots, n_{KK}$
		- Compute $\Pr(a) = \dfrac{n_{11}+n_{22}+\cdots+n_{KK}}{N}$

$$
\Large
P(a) = \frac{1}{N}\sum_{i=1}^{K} n_{ii}
$$
- chance agreement
	- assume A & B label independently but keep their marginal propensities for each class 
	- Row proportions: $p^A_i = \dfrac{n_{i\bullet}}{N}$ (Annotator A’s tendency for class $i$)
	- Column proportions: $p^B_i = \dfrac{n_{\bullet i}}{N}$ (Annotator B’s tendency for class $i$)
	- Then $\Pr(e) = \sum_{i=1}^K p^A_i\,p^B_i$

$$
\Large
Pr(e) = \sum_{i=1}^K p^A_i\,p^B_i
$$

### Minimal numeric picture (binary)
| A \ B | Pos | Neg | Total |
|---|---:|---:|---:|
| **Pos** | 40 | 20 | 60 |
| **Neg** | 10 | 30 | 40 |
| **Total** | 50 | 50 | 100 |

- $\Pr(a) = \dfrac{40+30}{100} = 0.70$
- $p^A_{\text{Pos}} = 0.6,\; p^B_{\text{Pos}} = 0.5;\; p^A_{\text{Neg}} = 0.4,\; p^B_{\text{Neg}} = 0.5$
- $\Pr(e) = 0.6 \cdot 0.5 + 0.4 \cdot 0.5 = 0.50$


$$
\Pr(a)=\frac{1}{N}\sum_{i=1}^{K} n_{ii},\qquad
\Pr(e)=\sum_{i=1}^{K}\left(\frac{n_{i\bullet}}{N}\right)\left(\frac{n_{\bullet i}}{N}\right),\qquad
\kappa=\frac{\Pr(a)-\Pr(e)}{1-\Pr(e)}.
$$



- For **ordinal** labels, use **weighted kappa**: 
	- replace the diagonal counts by a weighted sum 
	- $\sum_{i,j} w_{ij} \frac{n_{ij}}{N}$ 
	- and the chance term by $\sum_{i,j} w_{ij}\frac{n_{i\bullet}}{N}\frac{n_{\bullet j}}{N}$ 
	- where $w_{ij}\in[0,1]$ down-weights near-misses less than far-misses