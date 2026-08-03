---
type: article
status: raw
quality:
topics: [llm-evaluation, evaluation-metrics]
source: ""
created: 2025-11-01
published: 2025-09-25
author: Tejal Pathwardhan, Rachel Dias, Elizabeth Proch, Grace Kim, Michele Wang, Olivia Watkins, Simón Posada Fishman, Marwan Ajlouni, Phoebe Thacker, Laurence Faucconet, Natalie S. Kim, Patrick Chao, Samuel Misenerdino, Gildas Chabot, David Li, Michael ...
flashcards: none
updated: 2026-01-01
---

# Gdpval: Evaluating Ai Model Performance On Real-World Economically Valuable Tasks

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/367800533/_8YVCrxWZLox-4WBO49tKvt-i0F-cWGmV72bj0UseZg-cove_CmCgl2U.png" width="220" />
</div>

Source: https://cdn.openai.com/pdf/d5eb7428-c4e9-4a33-bd86-86dd4bcf12ce/GDPval.pdf

Exported at: `2025-12-29T04:28:27Z`


![](https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/367800533/s0Xu9tcdhtYD5dNLj7Ai0M_NkmfcUGOBV5g4XhZ5kQ8-_pa_Ie1nodC.jpeg)

- • Subjectivity: In addition to correctness, expert graders often consider subjective factors such as structure, style, format, aesthetics, and relevance. Our dataset also therefore serves as a helpful testbed to assess automated grader performance. • No "upper limit": Unlike metrics that could saturate quickly, our primary metric is winrate, which allows for continuous evaluation. Currently, we compare model outputs against a human expert baseline, but we could replace our baseline with increasingly strong models over time and keep evaluating.
- Long-horizon difficulty: Tasks require an average of 7 hours of work for an expert professional to complete. On the high end, tasks span up to multiple weeks of work.

![](https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/367800533/x98idU4Q3zHGWaTadowQ82cKu-L_d8_gBVJjZKpZoVk-_pa_l9qRBzk.jpeg)

- Each task's dollar value was estimated by multiplying the average estimated completion time by median hourly wages for the corresponding occupation from OEWS data (U.S. Bureau of Labor Statistics, 2025b).

## TASK QUALITY CONTROL PIPELINE

- Tasks undergo multiple rounds of review to ensure realism and quality.
- Across all stages of review, experts provided detailed comments, and tasks were iteratively revised before subsequent reviews to enhance quality and representativeness
- On average, grading each comparison for the gold subset took over an hour.
- Occupational experts conducting human grading rated the specificity of instructions provided in each prompt. 89.07% of tasks were rated as well-specified, indicating the instructions closely matched real-world expectations of clarity and detail.

![](https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/367800533/-h2WLpLK4eMl3HiAu5UBBuzcSqfqc5cLobe5CLDWHH4-_pa_3AU7D6r.jpeg)

- FURTHER DETAIL ON TASK QUALITY CONTROL
- MODEL-IN-THE-LOOP TASK REVIEW
- Because models can make mistakes, experts were instructed to take model feedback as a suggestion rather than a direction. Experts retained final responsibility for task accuracy and completeness; the model did not autonomously alter tasks.
- Human reviewers conducted multiple rounds of review on each task. Reviewers were primarily sourced from the original expert pool based on demonstrated excellence in task creation.
- The most skilled reviewers were further trained to become lead reviewers, responsible for identifying, mentoring, and promoting additional qualified reviewers from within the expert pool. Throughout the review process, the research team regularly performed quality-control checks on tasks signed off by reviewers, ensuring ongoing alignment and quality standards.
- The iterative review process included at least the following 3 stages: • 1. Generalist initial review: A generalist reviewer confirmed the task adhered to project requirements. • 2. Occupation-specific expert review: An occupation-specific reviewer assessed the representativeness of the task for the occupation, and confirmed that the task was possible for another member of the occupation to complete with the provided context. • 3. Final iterative reviewer feedback loop: A third expert reviewer provided iterative feedback and worked with experts until the task met our rigorous quality standards.
- AUTOMATED GRADER CONSENSUS METRICS
- To measure automated grader performance, we measured the agreement rate between scores given by the automated grader vs. human expert graders for the same sample. We also compared grading agreement between human experts who had graded the same sample.
- A_s^{\text{HA}} = \mathbb{E}\big[1 - |H - A|\big].
- The model-level human–automated grader agreement is the mean of AHA s over all samples for that model.
- Human Inter-Rater Agreement. For a given sample s, let the human scores H 1 and H 2 take values in p ∈ {0, 0.5, 1}. We measure human inter-rater agreement as the following expectation over two randomly sampled human ratings A_s^{\text{HH}} = \mathbb{E}\big[1 - |H_1 - H_2|\big].
- For a given sample, we estimate this quantity by the empirical mean over all pairs of ratings for that sample. The final human inter-rater agreement for a model is the mean of these sample-level scores over all samples with at least two human graders. Existing grader inter-reliability statistics such as Cohen's kappa, Fleiss' kappa, and Krippendorff's alpha are less directly applicable here, since our graders output ordinal scores in {0, 0.5, 1}.
- Over three automated grader sweeps on our dataset10, average human-automated grader agreement was 65.7% and human inter-rater agreement was 70.8%. Plots below show 95% confidence intervals obtained by bootstrapping (resampling with replacement the available automated grader scores or human grades for each sample, computing the mean per sample, and averaging across all samples or for the specified model).
- Both agreement metrics are highest for less capable models, since their outputs are easier to distinguish from human deliverables
- calculate an Adjusted Task Score
- as the simple average of the three normalized task ratings: task frequency, task importance, and task relevance.
