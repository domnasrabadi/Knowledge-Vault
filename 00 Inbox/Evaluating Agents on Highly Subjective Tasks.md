---
type: article
status: inbox
quality: 
topics: []
source: https://cameronrwolfe.substack.com/p/subjective-evals
created: 2026-10-31
published: 2026-10-21
author: Cameron R. Wolfe, Ph.D.
flashcards: none
updated: 2026-10-31
---

# Evaluating Agents on Highly Subjective Tasks

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!UUg5!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc096499-f61d-408d-819d-184191b06b99_2494x1394.png" width="220" />
</div>

- Agents solve a broad range of tasks that are tough to fully capture in a finite evaluation suite, and evaluation can be expensive because many realistic tasks are long-horizon and complex.
- Combined with the fact that agents are non-deterministic, *these factors make it difficult to draw reliable conclusions from evaluation.*
- When we consider subjective or open-ended tasks, these challenges become even more pronounced. For such tasks, solutions cannot always be verified deterministically. We must rely on human evaluation—*or other imperfect proxies like LLM judges*—to assess quality, which introduces additional sources of noise and subjectivity into an already difficult evaluation process.
- In this overview, we will outline a repeatable, three-part roadmap for evaluating subjective tasks that combines human evaluation, offline evaluation, and production monitoring.
- Additionally, we will cover practical techniques for improving evaluation effectiveness, including statistical methods for reducing noise and quantifying uncertainty, as well as data curation techniques for selecting diverse, realistic, and informative evaluation tasks.

### Why are evals so difficult?

- Evaluating modern LLM agents is difficult for several reasons;
- Agents have a broad scope of capabilities, which necessitates building evals for many tasks or domains.
- the tasks being solved by these agents are realistic and—*in many cases*—long-horizon, which can make the evaluation process [surprisingly expensive](https://huggingface.co/blog/evaleval/eval-costs-bottleneck).
- Combined with the non-deterministic nature of agents—*these models produce different outputs across repeated executions*—
- An improvement in a benchmark score does not automatically mean that our agent is “better.” A benchmark may not accurately reflect how the agent is used in practice, and the achieved score could fluctuate between trials due to non-determinism.

![](https://substackcdn.com/image/fetch/$s_!xwEe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe4377fa5-6896-43ea-9443-879354d53cf2_2324x760.png)


##### Anatomy of an Agent Evaluation

- evaluation suite is composed of a finite number of tasks on which we evaluate the agent. For each of these tasks, we execute our agent, yielding a rollout and a final solution.
- The rollout or final solution is then passed into a grader for verification, yielding a pass-fail result for that task.
- Put simply, we are executing our agent on a set of tasks and measuring the proportion of tasks it successfully completes.

![](https://substackcdn.com/image/fetch/$s_!J-sI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4dbcc7fc-a06b-4960-b1fe-8ad6b1ed52c1_1672x941.png)

- Structure of the evaluation process
- Usually, the number of tasks in our evaluation suite is kept relatively small to limit costs. Combined with agent non-determinism, these factors make evaluation results highly variable—*we evaluate our agent on a limited set of tasks, and its behavior often changes between executions*.
- Whether we can derive useful information from this evaluation process is largely dependent upon:
    - Whether tasks in the evaluation are realistic and representative of the diverse tasks that the agent will encounter in the real world.
    - Properly accounting for noise and uncertainty to determine whether observed performance improvements are statistically meaningful.

##### Evaluating Subjective Tasks

- on tasks with objectively verifiable outcomes. For these tasks, we can often implement a deterministic grader (e.g., [executable test cases](https://arxiv.org/abs/2310.06770), [string matching](https://arxiv.org/abs/2402.03300), or [symbolic verification](https://github.com/huggingface/Math-Verify)) to verify solutions.
- when we look at the set of tasks agents are expected to solve in the real world, they lie on a spectrum of verifiability
- However, even getting a reliable verification signal from a human or LLM for an open-ended task is difficult.
- Disagreement—*between both humans and LLMs*—is common when evaluation criteria are subjective.
- Attempting to evaluate open-ended tasks introduces additional sources of noise and subjectivity into an evaluation process that was already difficult to begin with.
- Therefore, we need to take explicit steps to reduce noise, quantify uncertainty, and provide confidence signals during evaluation that distinguish meaningful capability improvements from variability introduced by agents, judges, or the evaluation data itself.

### Techniques for Effective Evaluation

- Before introducing our evaluation roadmap, we will cover several techniques that are particularly useful for evaluating subjective tasks.
- include LLM judges, statistical methods for quantifying uncertainty, and data curation techniques for constructing reliable evaluation sets.

##### Judges and Rubrics

- Generally, **LLM judges** are provided with quality criteria that they apply consistently across different evaluation tasks—*similarly to how evaluation is performed by humans*.
- **Rubrics**, on the other hand, decompose solution quality into a checklist of specific criteria. These criteria are usually tailored to each individual task, and each criterion can be independently evaluated using an LLM judge.
- Structuring evaluation in this way allows us to verify concrete aspects of solution quality rather than relying solely on a holistic, higher-level assessment of quality.
- the rubric contains detailed checks that are executed by an LLM judge to verify a solution.
- LLM judges and rubrics provide a scalable way to evaluate solution quality.
- For open-ended tasks, these methods can be an automatic proxy for human evaluation when deterministic verification is not possible.
- However, we must be aware that LLM judges are imperfect and can exhibit systematic biases—*we should carefully calibrate and validate their predictions before trusting the evaluation scores*[](https://cameronrwolfe.substack.com/p/subjective-evals/#footnote-1)
- Meta-evaluation
- Given that LLM judges and rubrics are imperfect proxies for human evaluation, we need to meta-evaluate these components—*or measure if their predictions accurately reflect solution quality*.
- To do this, we can collect a golden dataset of human-created evaluation examples and measure if the LLM judge's predictions agree with these samples.
- Depending on the scoring setup, we can use metrics like correlation, classification accuracy, or many other [inter-rater reliability metrics](https://en.wikipedia.org/wiki/Inter-rater_reliability).

##### Statistics for Agent Evaluations

- Given that LLM and agent evaluations are inherently noisy, we need techniques for quantifying uncertainty and drawing reliable conclusions from evaluation results.
- we will cover three key ideas—*power analysis, confidence intervals, and re-sampling*—that can be used to: 1. Provide clear confidence signals along with our evaluation result. 2. Reduce the variance of the evaluation process so that we are more likely to reach a statistically significant conclusion.
- These techniques lay the foundation for handling noise and drawing useful conclusions even when evaluating especially noisy or subjective tasks.
- **Power analysis.** Before running an evaluation, we need to determine how much data is needed to produce a reliable result. [Power analysis](https://cameronrwolfe.substack.com/i/188458832/power-analysis-for-llm-evals-1) [[2]](https://cameronrwolfe.substack.com/p/subjective-evals/#footnote-2) is a statistical tool that can be used to estimate this required sample size based on:
    - The minimum performance improvement we want to detect (i.e., effect size).
    - The expected variability of evaluation scores.
    - Our desired level of statistical significance and power.
- In practice, we usually derive quantities like the variability of evaluation scores by empirically estimating them from sampled evaluation data.
- quantities like the minimum detectable effect and significance level are chosen by us
- Once these quantities are available, we can put them into a formula to solve for the required number of samples;
- Larger effect sizes and lower variance require fewer samples to draw reliable conclusions and vice versa. *Power analysis allows us to estimate the number of evaluation samples needed to detect a meaningful performance improvement*.
- **Confidence intervals.** An evaluation score is only an estimate of a model’s true performance on an underlying distribution of tasks. Because we estimate performance with a finite set of tasks, the result is subject to sampling uncertainty—*we can obtain a different score by evaluating the agent on a different set of tasks*.
- To quantify this uncertainty, we can construct a [confidence interval](https://en.wikipedia.org/wiki/Confidence_interval) around the evaluation score. The [Central Limit Theorem (CLT)](https://en.wikipedia.org/wiki/Central_limit_theorem) tells us that, given sufficiently many [independent](https://en.wikipedia.org/wiki/Independence_(probability_theory)) samples, the sampling distribution of the mean is approximately normal. We can estimate the [standard error](https://en.wikipedia.org/wiki/Standard_error) of this mean by dividing the standard deviation of evaluation scores by the square root of the sample size.
- Then, we can construct a 95% confidence interval using this standard error with the following form: `mean ± 1.96 × standard_error`;
- Narrower confidence intervals indicate more precise estimates. However, *we should keep in mind that the tasks used for evaluation are not always independent.*
- we can have multiple tasks that are derived from the same codebase or document. In these cases, we can use [clustered standard errors](https://cameronrwolfe.substack.com/i/188458832/clustered-errors) to account for correlations between tasks and avoid underestimating the level of uncertainty in our evaluation.
- When comparing two agents, we can also consider evaluating them on the same tasks and constructing a confidence interval over their [paired performance differences](https://cameronrwolfe.substack.com/i/188458832/model-comparisons) to (potentially) yield narrower confidence intervals
- **Re-sampling** is another simple trick that can be used to reduce uncertainty. Agent evaluations are non-deterministic. Given a single task, our agent can produce multiple different outcomes when we re-run it on this task. Additionally, the LLM judge or rubric used to verify the agent’s solution can also produce multiple different results when re-run. Rather than executing each task once, we can reduce the impact of non-determinism by running the agent multiple times and evaluating the resulting solutions, potentially with repeated grading as well.
- By repeating the same evaluation multiple times and averaging the results, we provide a more stable estimate of expected performance on each task. This approach reduces within-task variance and can yield narrower confidence intervals.
- However, re-sampling only reduces within-task noise and does not address variability across tasks, so higher confidence is not guaranteed.
- We use *power analysis* to determine how much evaluation data we need, *confidence intervals* to quantify uncertainty and determine whether observed improvements are statistically meaningful, and *re-sampling* to reduce noise in our results.
- The primary takeaway is quite simple: *evaluation results should always be accompanied by clear confidence signals*. Without these signals, we risk mistaking noise for meaningful capability improvements.

##### Sampling Useful Evaluation Tasks

- Beyond accounting for noise, we also need to carefully consider the tasks used to evaluate our agent. Both the amount and quality of evaluation data are important for drawing reliable conclusions.
- However, choosing the right type of evaluation data requires considering several additional factors
- **Diverse.** To comprehensively characterize and measure agent behavior, we need an evaluation set that covers the diverse set of tasks our agent is expected to solve in the real world. Otherwise, we risk artificially inflating evaluation scores by evaluating the agent primarily on tasks where it performs well and excluding areas where it struggles. Put differently, *we need to ensure that our evaluation suite is diverse and tests agent behavior across all (or most) use cases that are relevant*.
- One useful approach for handling diversity is to construct a structured taxonomy of the tasks an agent must solve, which allows us to more systematically measure and improve the coverage of our evaluation suite.
- GDPval [3] organizes tasks into a hierarchical taxonomy that considers the economic sector, occupation, and exact work activity being tested by each task; see below.

![](https://substackcdn.com/image/fetch/$s_!uWS0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8f86789b-5a17-49ec-9741-a1135420f5eb_1376x880.png)

- Many other popular benchmarks (e.g., [Terminal-Bench](https://cameronrwolfe.substack.com/i/195454629/terminal-bench-12), [SWE-Bench](https://arxiv.org/abs/2509.16941?utm_source=chatgpt.com), [Agents’ Last Exam](https://arxiv.org/abs/2606.05405), [OSWorld](https://arxiv.org/abs/2404.07972), etc.) organize tasks into categories or taxonomies as well, though the level of detail and structure varies between benchmarks.
- Organizing evaluation tasks into a taxonomy is useful for several reasons:
    - Simplifies verification of benchmark diversity and coverage.
    - Allows performance to be analyzed granularly in each taxonomy area.
    - Enables extension into new domains by expanding the taxonomy.
    - Creates a modular setup in which we can improve specific areas of the benchmark without impacting others.
- **Realistic.** We want the tasks used for evaluation to be an accurate reflection of how the agent is used in the real world. When curating evaluation data, we should aim to find realistic tasks, ideally sourced from actual production usage of the agent.
- By sourcing tasks from the real world, we can reduce the gap between evaluation and how an agent is actually used, *increasing the likelihood that benchmark results reflect true capabilities*.
- **Difficult.** To meaningfully distinguish agent capability levels, evaluation tasks must be sufficiently challenging
- In other words, *if every agent solves almost every task, the benchmark provides little useful information for comparing their capabilities*.
- Several techniques can be used to assess difficulty:
- Infer the difficulty from the source of the questions;
- Ask humans to assess question difficulty;
- Use model-based difficulty filtering by executing one or more agents on candidate tasks and estimating their success rates.
- Additionally, the benchmark creators use targeted failure analysis to identify and resolve quality issues.
- **Discriminative.** In addition to being difficult, problems in a benchmark should be discriminative—*meaning that they differentiate between the capabilities of different models*. Importantly, difficult tasks are not always discriminative.
- **Accurate.** Finally, we want to ensure that the tasks and grading criteria used for evaluation are accurate. To do this, *we usually use some combination of human and model-based auditing*. As described above, one useful approach is failure analysis—*executing agents on evaluation tasks and examining failure patterns to identify any issues that exist with the task*.
- We can perform these checks with an LLM auditor, as described in the quote below, or with a human auditor. Usually, model-based auditing is used to scale the quality validation process, while human auditors perform in-depth checks on a select number of difficult or ambiguous cases.

### A Roadmap for Subjective Evaluation

- This roadmap consists of three main components: *human evaluation, offline evaluation, and production monitoring*.

##### Human Evaluation


![](https://substackcdn.com/image/fetch/$s_!pXD4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6a6320cd-af1c-41ee-a463-a80307b55c9d_1934x886.png)

- Human evaluation serves as our North Star for defining, measuring, and improving quality on subjective tasks over time.
- In order for humans to evaluate a task reliably, however, *we need to create a clear definition of quality*.
- To do this, we usually partner with a small number of subject-matter experts [[3]](https://cameronrwolfe.substack.com/p/subjective-evals/#footnote-3) to create [quality](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/) [guidelines](https://eugeneyan.com/writing/labeling-guidelines/) for our task.
- These quality guidelines include:
    - A small set of quality criteria (e.g., coherence, accuracy, and clarity).
    - Scoring instructions for each criterion, *typically using a binary or Likert scale*.
    - Details on how to properly score each criterion, along with several concrete evaluation examples and corresponding explanations.
- goal is to create clear evaluation guidelines that minimize unnecessary subjectivity and make the evaluation process as consistent and reliable as possible.
- **Calibration.** Even if we create the best-possible quality guidelines, we should not simply assume that the human evaluation process is reliable—*we need to calibrate extensively*.
- Concretely, this means that we should:
    - Sample multiple human evaluations for the same data.
    - Measure the level of agreement between these samples (e.g., using metrics like [Fleiss’ kappa](https://en.wikipedia.org/wiki/Fleiss%27s_kappa) or [Krippendorff's alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha)).
    - Update guidelines based on observed sources of disagreement.
- Put simply, calibration is an iterative, human-centric process. We test our evaluation guidelines on real data, identify sources of disagreement, and address them through clearer explanations or additional examples.
- Over time, this process helps to improve agreement between human evaluators—*calibration improves the clarity of our quality guidelines and, in turn, benefits agreement.*
- However, *what if agreement remains low despite repeated calibration?* In such cases, we may need to reconsider the quality criteria themselves. Our goal is to define criteria that are clear, sufficiently objective, and possible for humans to evaluate reliably. Some aspects of quality are inherently subjective or difficult to assess consistently, even with detailed guidelines. Rather than trying to evaluate everything, we need to be selective—*focusing on criteria that are both meaningful and possible to measure reliably*.
- If a criterion yields consistent disagreement, we can simplify it, break it into more specific checks, or even remove it entirely.
- **Continual monitoring.** Calibration is also not a one-time investment—*we must continually monitor agreement levels during evaluation to avoid drift*. Agreement can degrade over time due to various factors, such as onboarding new human evaluators or simply forgetting guideline details over time.
- To address these issues, we can continue computing agreement throughout the human evaluation process—*by having multiple people evaluate a subset of tasks, setting up intermittent calibration exercises, or even re-evaluating tasks that already have known results*—and continue to address any sources of disagreement as they arise.
- **Running human evaluation.** Once we have clear quality guidelines and have calibrated the evaluation process, we are ready to perform human evaluation.
- First, we sample tasks for our evaluation using the concepts we have covered before—*power analysis to estimate volume and several methods to ensure diversity and quality*. Then, we sample rollouts for these tasks from our agent and pass them into the human evaluation process. Here, human evaluators serve as the grader, assessing the quality of each generated solution according to our guidelines.

##### Offline (Automatic) Evaluation


![](https://substackcdn.com/image/fetch/$s_!ZG0G!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9e3ed892-4b7a-4607-ac7a-0fe7e414d2d9_1776x1286.png)

- Human evaluation provides useful quality signals, but manually evaluating every new agent or model quickly becomes a bottleneck—*we want to test new ideas and iterate on model quality as quickly as possible*.
- To enable this, we can invest in offline (automatic) evaluations. The key idea here is that instead of verifying the quality of a solution with a human, we use an automatic proxy—*usually an LLM judge or rubric-based judge*.
- This allows us to evaluate new models and experiments more efficiently and reserve human evaluation for the most promising candidates.
- **Meta-evaluation.** Automatic metrics can be used to verify solution quality similarly to a human, but they are still only an imperfect proxy—*human evaluation results remain our North Star in terms of quality*.
- Therefore, we need to meta-evaluate these components using golden data derived from the human evaluation process. Put simply, this golden data includes task solutions paired with validated human quality judgments that serve as high-quality reference evaluation results.
- We can measure and improve the agreement of our judge with these golden evaluation samples and iterate upon the judge to improve agreement.
- The level of agreement we should aim for depends upon the task being solved—*subjective tasks often exhibit lower levels of agreement*.
- **Creating benchmarks.** Once our automatic verifiers have been created and meta-evaluated, we can begin to build benchmarks around them. To do this, we sample tasks using the same principles outlined earlier, execute our agent on these tasks, and verify solutions with our LLM judge or rubric.
- our goal is to measure agent performance across a diverse set of tasks—*the difference is that solution quality is now assessed automatically*.
- **Handling noise.** As mentioned before, we are working with subjective tasks in which both the agent and the verification process are non-deterministic.
- Concretely, we can address evaluation noise by adopting a combination of statistical techniques:
    - Power analysis can be used to estimate the proper benchmark size.
    - Confidence intervals can be reported along with all evaluation results.
    - Re-sampling of both agent and judge completions can be used to reduce the variance of the evaluation result.

##### Production Monitoring


![](https://substackcdn.com/image/fetch/$s_!LNPP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae4fc6b3-dce2-4dd9-9352-878a5c4b9285_1728x760.png)

- **Production monitoring** allows us to define and track key metrics as our agent is used in production. There are a variety of metrics that could be used:
    - *Implicit*: session length and abandonment rate.
    - *Explicit*: thumbs up or down and user preference feedback.
- These metrics provide quality signals that can be used to evaluate our agent based upon how users are interacting with it. [Production monitoring](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) provides a complementary perspective on agent quality—*rather than evaluating an agent on a curated set of tasks, we measure its performance through real-world interaction*.
- **A/B testing.** We can measure these production metrics in an [A/B test](https://en.wikipedia.org/wiki/A/B_testing) to better understand the capabilities of our new agent relative to an existing baseline. By doing this, we can perform a kind of “soft” model rollout, in which we vet the quality of our agent before fully deploying it to production. This allows us to evaluate the agent on real-world traffic before committing to a full rollout
- **Monitoring and improvement.** Even after we have A/B tested and deployed a new model, we can continue to monitor production metrics over time so that any concerning trends can be detected and addressed. Production monitoring can also be used to find realistic and difficult tasks to add into other phases of the evaluation process. By analyzing production interactions, we can identify new use cases, difficult tasks, and recurring failure modes that are not yet represented in our existing benchmarks. We can then incorporate these tasks into our human and offline evaluations, *creating a feedback loop that continually improves benchmark coverage and grounds the evaluation process in real-world usage of the agent*.

##### Continual Evolution

- Even after establishing this evaluation framework, we should continually improve each component by:
    - Defining new or better evaluation criteria.
    - Improving human or judge calibration.
    - Sourcing new evaluation tasks.
- we can even repeat this entire framework in another domain to build an entirely new evaluation set.
- *evaluation is a continually evolving process*. As agents become more capable, we need more informative evaluations that can measure performance with greater precision and detect meaningful improvements.
- there are several common methods or directions that are often targeted, such as:
    - *Difficulty-based refinement*: curating more difficult tasks or data to use for evaluation within a benchmark.
    - *Quality-based refinement*: identifying and fixing issues in the benchmark (e.g., mislabeled data, vague or unrealistic questions, poor format, etc.).
    - *Diversity-based refinement*: expanding the scope of questions and topics covered by a particular benchmark.

### Putting It All Together


![](https://substackcdn.com/image/fetch/$s_!0vx5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc08322a8-5386-488c-abfc-62c9f9dd39d3_1356x398.png)

- Evaluation is already difficult, and it becomes even harder when working with subjective tasks due to the additional noise and uncertainty involved.
- Our roadmap consists of three main components:
    - *Human evaluation* serves as our North Star by providing a clear definition of quality that human evaluators can consistently apply.
    - *Offline evaluation* uses calibrated LLM judges or rubrics as an automatic proxy for human evaluation, allowing us to scale experimentation.
    - *Production monitoring* provides additional quality signals from real-world agent usage and enables A/B testing before a full deployment.
- At every step, we can leverage the statistical techniques covered in this overview—*power analysis, confidence intervals, re-sampling, and more*—to reduce noise and provide clear confidence signals alongside evaluation results.
- these components form a multi-layer evaluation strategy that allows us to comprehensively measure agent performance and reliably improve quality over time.
- Further reading
- • Human Evaluation • [Annotation](https://lilianweng.github.io/posts/2024-02-05-human-data-quality/) [guidelines](https://eugeneyan.com/writing/labeling-guidelines/) and [setup](https://hamel.dev/blog/posts/evals-faq/) • Calibration metrics *(*[Fleiss’ kappa](https://en.wikipedia.org/wiki/Fleiss%27s_kappa), [Krippendorff’s alpha](https://en.wikipedia.org/wiki/Krippendorff%27s_alpha)) • LLM Judges & Rubrics • LLM-as-a-Judge [concepts](https://cameronrwolfe.substack.com/p/llm-as-a-judge) and [best](https://hamel.dev/blog/posts/llm-judge/index.html) [practices](https://eugeneyan.com/writing/llm-evaluators/) • [Rubric-based](https://cameronrwolfe.substack.com/p/rubric-rl) [judges](https://arxiv.org/abs/2603.00077) • Useful Statistics for Evaluation • [General](https://cameronrwolfe.substack.com/p/stats-llm-evals) [overviews](https://www.anthropic.com/research/statistical-approach-to-model-evals) • [Power analysis](https://cameronrwolfe.substack.com/i/188458832/power-analysis-for-llm-evals-1) • [Confidence intervals](https://cameronrwolfe.substack.com/i/188458832/standard-errors-and-the-clt) • [Re-sampling](https://cameronrwolfe.substack.com/i/188458832/reducing-variance) • [Pairwise comparison](https://cameronrwolfe.substack.com/i/188458832/model-comparisons) • LLM Evaluation Guides • [Deep dive on building benchmarks](https://cameronrwolfe.substack.com/p/llm-bench) • [Evaluating](https://cameronrwolfe.substack.com/p/agent-evals) [agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
