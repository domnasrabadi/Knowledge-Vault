---
type: book
status: inbox
quality: 
topics: []
source: private://read/01m0ec64337kwn57dyzsmkzcw9
created: 2026-08-23
published: 2026-03-28
author: Arif Türkmen, Kaan Efe Keleş
flashcards: none
updated: 2026-08-23
---

# Whom to Trust? User Satisfaction vs LLM-as-a-Judge in E-Commerce RAG

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article4.6bc1851654a0.png" width="220" />
</div>


## Whom to Trust? Analyzing the Divergence Between User Satisfaction and LLM-as-a-Judge in E-Commerce RAG Systems


### Abstract


### Abstract

- Our framework combines user satisfaction labels, *LLM-as-a-judge* scoring, and factor-based diagnostics to separate retrieval from generation errors. We find that judge models broadly reflect user satisfaction trends, though important nuances of dissatisfaction are often missed
- Factor-level analysis highlights systematic error patterns across query types and context quality, demonstrating that hybrid evaluation, combining multiple LLM judges with direct user feedback offers the most reliable assessment strategy for production RAG systems

### Evaluation Framework for User Satisfaction


### Evaluation Framework for User Satisfaction

- A central challenge in evaluating the Trendyol QA Assistant lies in capturing end-user satisfaction at scale. Online A/B tests provide high-quality ground truth but are expensive and slow to iterate, motivating scalable alternatives
- We therefore adopt a three-pronged evaluation methodology, combining direct human feedback with structured LLM-based approaches.

#### Direct User Feedback


#### Direct User Feedback

- Ground-truth performance is obtained from user-reported satisfaction collected during live usage. After each interaction, users are asked in a thumbs-up or thumbs-down fashion whether they were satisfied with the assistant’s answer. If dissatisfied, they may optionally select one of four categorical reasons: *irrelevant* , *insufficient/incomplete* , *unclear* , or *misleading/incorrect* . This feedback provides the most accurate measure of user experience, though it is costly to scale and limited in experimental coverage.

#### LLM-as-a-Judge Simulation


#### LLM-as-a-Judge Simulation

- To complement human feedback, we employ *LLM-as-a-judge* techniques, in which stronger models are prompted to evaluate QA interactions automatically using a fixed, structured judging prompt
- The judge returns (a) a binary satisfaction decision and (b) if dissatisfied, one of the same four standardized reasons provided to users.
- To assess alignment with users, we report two complementary measures. (i) *Satisfaction Agreement* : the exact match rate between the predictions of the judge and the satisfaction of the user in all interactions, contextualized with the expected chance agreement and Cohen’s *κ*
- (ii) *Dissatisfaction Breakdown* : the categorical distribution of dissatisfaction reasons, enabling direct comparison between user-reported and judge-assigned error types.

#### Factor-Based LLM Analysis


#### Factor-Based LLM Analysis

- Finally, we use a granular, multi-prompt technique where the LLM isolates and evaluates specific factors
- Prompts target different aspects to categorize question-answer pairs:
    - Query Classification: It determines the topic of the question. Is the user asking about the product or the seller?
    - Intent Analysis: It identifies the user’s goal. Is the user asking a genuine question or making a demand?
    - Contextual Relevance: Did the information retrieved actually contain the necessary details to address the user’s query?
    - Persona Consistency: Does the answer maintain the assistant’s intended style (formal tone, third-person narration) throughout?

### Results


### Results

- alignment between LLM-as-ajudge predictions and human feedback. The human-reported satisfaction prevalence is 77.2%. The two judges differ in calibration to this baseline (65.0% vs. 76.3%)
- However, agreement with user labels is only modest: exact-match rates are 64.5% (GPT-4o) and 72.5% (o4-mini), which translate to Cohen’s *κ* of 0.15 and 0.23, respectively

### Discussion


### Discussion

- This suggests that using reasoning models in evaluation tasks may help to simulate user judgment patterns, particularly when assessing complex QA interactions
- Our stratified analysis reveals that no single judge model performs uniformly well across all interaction types
