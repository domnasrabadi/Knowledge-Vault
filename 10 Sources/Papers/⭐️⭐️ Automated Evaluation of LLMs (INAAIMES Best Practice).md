---
type: paper
status: raw
quality: 2
topics: [llm-evaluation, evaluation-metrics, llm-judges, error-analysis]
source: https://cdn.prod.website-files.com/663bd486c5e4c81588db7a1d/6a61e3fdec2b87a8f5658105_Network%20Best%20Practice.pdf
created: 2026-08-08
published: 2026-07-23
author: International Network for Advanced AI Measurement, Evaluation and Science
flashcards: none
updated: 2026-08-08
---

# International Network For Advanced AI Measurement, Evaluation And Science Best Practice: Automated Evaluation Of Large Language Models

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/480537938/cMNB-RU1QGgyJgtNE2sz3dqyfy7inEWydPa3aHfNlpg-cove_ygHqLd9.png" width="220" />
</div>

- AI evaluation is a broad and rapidly evolving field, encompassing a wide range of methods, objectives, and approaches. This document focuses on one important subset: automated evaluations of AI models.
- Automated evaluations - where model responses are graded automatically, often by an LLM
- offer scalability for large amounts of evaluation results, and consistency for applying similar evaluations to different models,
- Automated evaluations include:
    - Multiple choice evaluations, which are question-answer evaluations which involve the model selecting between several potential answers.
    - Open-ended evaluations, which have many possible correct responses, typically when the evaluation domain cannot be divided into discrete tasks, and/or it is difficult to define objective grading criteria or verification procedures. Testing “rubrics” are often used to assess the validity of model responses.
## B. Defining Evaluation Objectives and Selecting Evaluations

### B.1. Defining Evaluation Objectives

- Evaluations should be done for a well-defined reason. Often, this is to gather evidence to assess claims about AI capabilities in real-world settings. But in all cases evaluators need to specify, before developing or executing their evaluations, what they are evaluating for
- Evaluators should follow three key high-level steps when defining what and how to measure: establishing the overall evaluation objectives, identifying the measurement construct, and ensuring construct validity
- evaluators should clearly set out what they are trying to measure. This is often known as the "measurement construct." A measurement construct is the specific concept or capability the evaluation is intended to measure
- Defining the measurement construct precisely and in advance helps ensure that the evaluation remains focused, that its results can be interpreted clearly, and bounds the scope of the claims that can be made from the results
    - Provide a precise and operational definition for what is being measured
    - Specify the scope of what is being covered and acknowledge any excluded aspects.
    - Identify if what is being measured has sub-components and ensure they are measured separately, or in such a way to not implicitly confound the target construct or skill.
- Evaluators should also consider whether the evaluation measures the intended construct1. More specifically, evaluators should,
    - Justify the relevance of the benchmark for the phenomenon with real- world applications.
    - Provide a clear rationale for the choice of tasks and metrics, connected to the operational definition of the phenomenon.
    - Compare similarities and differences between the benchmark and existing evaluations of similar phenomena. In this case, evaluators should consider using human or AI baselines to provide a point of comparison, depending on the purpose of the evaluation
    - Discuss the limitations and design trade-offs of the benchmark concerning construct validity
    - Consider whether the evaluation is intended to measure or predict a real- world outcome, or to measure an abstract concept.
- Evaluators should also consider potential business and policy objectives, particularly when performing evaluations for private firms; for example, a hiring application might prioritise recall (to avoid missing strong candidates) or precision (to filter out underqualified ones) depending on the specific objectives of the business.

### B.2. Select Evaluations That Meet Objectives
- Document precisely what each candidate benchmark claims to measure, and the accuracy of this claim based on available information about its construction, validation, and usage by others. Where possible, manually inspect test items.
- Relevant details include subject matter, intended difficulty, item format, and how responses are graded
- Document whether the benchmark directly measures the construct of interest, is conceptually related to the evaluation objective, or predicts downstream outcomes of interest. Where the benchmark directly measures the construct, consider coverage across the space of relevant tasks and whether the item format reflects intended use cases.
- Where the evaluation seeks to compare AI performance to alternative approaches, validated baseline measures (e.g., human performance) are beneficial and should themselves be statistically robust. These baselines are useful for grounding the metric (e.g. for saying whether scoring 10% on the evaluation is a strong or poor performance)
- While automated evaluations offer scalability and consistency, evaluators should remain conscious of their limitations.
- Automating judgement can constrain what is measured well: the decision to automate can create selection pressure towards ... constructs that are readily machine-scoreable, unintentionally privileging proxy measures over the construct of genuine interest.
- Evaluators should therefore treat the decision of whether to automate grading as an explicit step in the design process, considering whether automation supports their objective without distorting the identified construct
- Where automated scoring is used, it should be validated against human judgements on a representative sample - one of the most important procedural differences when moving from human-graded to automated approaches.
## C. Implementing and Running Evaluations

### C.1. Design the Evaluation Protocol and Conduct Capability Elicitation Experiments

- first step for evaluators is to design the evaluation protocol: the full set of operational procedures carried out during an evaluation. This includes decisions about what items to include, how prompts are formatted, how models are queried, and how outputs are scored.
- Three common design principles, guided by NIST AI 800-2, can help guide protocol decisions:
    - Comparability: the protocol should support meaningful comparison across models, versions, or time points. It is useful to distinguish between two aspects of comparability: the evaluation of outputs (scoring criteria, rubrics, graders) and, the generation of outputs (prompt format, inference settings)
    - External validity: the protocol should reflect, as far as is practical, the conditions under which the model will be used in practice. For example, if the evaluation is intended to assess a model's usefulness in a customer-facing application, the prompt format, interaction style, and task complexity should approximate real-world usage rather than highly artificial or contrived scenarios.
    - Cost control: evaluations consume computational resources and human time. Evaluators should consider the trade-off between thoroughness and cost when designing their protocol, for example, by selecting an appropriate number of test items and trials that balance statistical power against budget constraints.
- Evaluators should also check for the bias and calibration of the grader. Where iterative optimisation is used, evaluators should document each iteration, including what was changed, why it was changed, and how the change affected results
- Evaluators can iterate on prompts either manually or using LLM-based prompt optimisation. Relevant iterations may include refining task instructions to reduce ambiguity, adjusting formatting to match model expectations, or tuning inference-time settings such as reasoning effort.
- When evaluators iterate on prompts, inference settings, or other aspects of the protocol, they should do so using data that is distinct from the set used to report final results.
- Where possible, evaluators should adopt a three-way split of the evaluation data
    - An exploratory set of a small number of items (e.g., 2-5), used for manual experimentation and initial qualitative analysis of model behaviour.
    - A tuning set, used for iterating over prompts, parameters, and other elicitation choices. This should typically be 70-80% of the items.
    - An evaluation set, used only for the final reported evaluation after tuning is complete. This should typically be 20-30% of the items.
- These three sets should be disjoint, meaning that they should be composed of completely separate data. Evaluators should not look at the evaluation set during tuning.
- Evaluators should also consider how tasks are presented to models and how outputs are scored. Poorly designed task or scoring settings can limit an evaluator's ability to accurately measure model capabilities
- evaluators should consider the following:
    - LLM-as-a-judge: when items lack programmatically verifiable answers, LLM judges with detailed rubrics can be used to score outputs. Evaluators should ensure that judge outputs are validated against human judgements on a representative sample. Evaluators may also consider using multiple judges or multiple rubrics, computing inter-rater agreement, and applying techniques such as prediction-powered inference to improve reliability.
    - Number of test items: Evaluators should attempt to balance statistical power against cost. Where possible, evaluators should use power analysis to determine an appropriate number of items.
    - Aggregate statistics: Evaluators should select metrics aligned with the evaluation objective (e.g., mean accuracy for typical-case performance, or worst-case statistics for risk assessment).
    - Item-level scoring and aggregation: Evaluators should note that the choice of per-item aggregation method (e.g., pass@k, majority-of-N, mean across trials) affects what is being measured. Evaluators should select aggregation methods that reflect the intended construct and should clearly document both the metric and the aggregation method used.

### C.2. Write the Evaluation Code

- Evaluators should also design evaluations so that components are separated into distinct, interchangeable modules.
- Finally, evaluators should include clear documentation alongside evaluation code, describing what the evaluation measures, how it is structured, and any known limitations.

### C.3. Run the Evaluation and Track Results

- Once the evaluation protocol has been designed and the evaluation code has been written, evaluators are ready to execute their evaluations. How evaluations are run - and how their outputs are captured and organised - has significant downstream implications for the reliability, reproducibility, and interpretability of results
- In particular, evaluators should pay attention to the following areas when conducting their evaluations,
    - Summary statistics (e.g., mean accuracy) are useful for headline comparisons but are insufficient on their own. Full evaluation logs - including model inputs, outputs, and environment interactions - should be retained. These should include task logs (logs of the evaluated model performing the evaluation tasks) and judge logs (logs of the LLM-as-a-judge assessing the evaluated model’s outputs).
    - Logs should be tagged with metadata that makes clear the purpose of each run, the settings used, and the relationship between different runs
    - Rather than launching a full evaluation run immediately, evaluators should begin with small runs on subsets of data to verify that the evaluation is functioning as intended. Incremental runs allow evaluators to catch bugs early, verify that logs are being captured correctly, and confirm that results are broadly in the expected range before committing significant compute.

### C.4. Debug the Evaluation

- Debugging should be approached as an iterative activity that runs alongside evaluation execution rather than as a single step at the end. Evaluators should expect to uncover issues through a combination of manual transcript review, automated checks, and comparison to existing evidence
- The following are common issues that evaluators are likely to face.
    - Results should be reported with appropriate uncertainty quantification, such as standard errors, confidence intervals, or credible intervals.
    - To search for these issues, evaluators should read transcripts - particularly transcripts of failed runs or anomalous outputs - to look for unexpected model behaviours. While most relevant for agentic evaluations, manual review of automated evaluations enables the identification of failure modes that may not be visible in aggregate metrics, such as models misinterpreting instructions, producing formatting errors, or exhibiting subtle refusal behaviours4
        - At scale, manual review is not always feasible. Evaluators can supplement manual review with automated checks, including programmatic pattern detection (e.g. keyword matching for refusal phrases) and LLM-based scanners that assess transcripts for specific behaviours such as evaluation cheating or verbalised evaluation awareness.
    - Multiple scanners or rubrics may be used in combination to improve accuracy.

## Terminology
- Automated evaluation: Evaluations where scoring is performed without direct human judgement of correctness for individual test items.
- Evaluation: A set of tasks presented to a model. Capability evaluations are aimed at measuring its capabilities in a certain area.
- LLM-as-a-judge: the use of LLMs as graders of evaluations, rather than human graders. Sometimes referred to as “autograders”.
- Transcript/logs: Refers to any records generated when using an AI system. Logs can include model inputs (user messages, prompts, instructions), model outputs (model responses, internal commentary, chain-of-thought reasoning, tool calls), environment interactions (tool outputs, API responses, terminal commands) and metadata (timestamps, token usage, error codes). Logs can also include task descriptions and scores from previous analyses (e.g., in agentic evaluations where agents are prompted to solve specific tasks and receive pass/fail scores).
