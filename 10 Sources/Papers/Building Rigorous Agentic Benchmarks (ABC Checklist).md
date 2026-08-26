---
type: paper
status: raw
quality: 
topics: [agent-evaluation, llm-evaluation, evaluation-metrics]
source: https://arxiv.org/abs/2507.02825v5
created: 2026-08-23
published: 2025-07-03
author: Yuxuan Zhu et al.
flashcards: none
updated: 2026-08-27
---

# Building Rigorous Agentic Benchmarks (ABC Checklist)

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article4.6bc1851654a0.png" width="220" />
</div>

### Abstract

- However, we show that many agentic benchmarks have issues in task setup or reward design.
    - For example, SWE-bench Verified uses insufficient test cases, while TAU-bench counts empty responses as successful.
    - Such issues can lead to under- or overestimation of agents' performance by up to 100% in relative terms
- To make agentic evaluation rigorous, we introduce the Agentic Benchmark Checklist (ABC), a set of guidelines that we synthesized from our benchmark-building experience, a survey of best practices, and previously reported issues

### Introduction

- Agentic benchmarks differ fundamentally from traditional AI benchmarks.
    - Multiple-choice datasets (e.g., ImageNet and MMLU) evaluate models by their accuracy on categorical labels, while text-generation benchmarks rely on automatic metrics (e.g., BLEU).
    - By contrast, success is defined by completing end-to-end tasks in agentic settings. Therefore, an agent may perform coherent reasoning, write code, and execute commands to produce a final outcome.
    - Subsequently, the performance of the agent is determined by comparing its final outcome with a ground-truth outcome, using various methods, such as program testing and string matching
- Unfortunately, many existing outcome-based evaluation methods of agentic benchmarks introduce issues that can cause under- or overestimation of agent capabilities by up to 100% in relative terms, compromising the validity of their findings
- Combining insights from the literature with our own experience in developing benchmarks, we identified two major conditions of the validity of benchmark results:
    - *Outcome validity*: the evaluation result (e.g., tests or checks) truly indicates task success. SWE-bench-Verified fails here because an incorrect patch can still pass the test suite.
    - *Task validity*: a task should be solvable if and only if the agent possesses the target capability. Issues in task design or implementation often breaks task validity. For example, $\tau$-bench allows a trivial agent to pass 38% of tasks without knowledge of airline-ticketing rules.
- we formulate our insights into an **A**gentic **B**enchmark **C**hecklist (ABC) to assist benchmark developers and users in critically designing and assessing agentic benchmarks
    - Using ABC, we assessed ten popular agentic benchmarks that span the full range of agent capabilities, resulting in seven benchmarks with flaws in outcome validity, seven with issues in task validity, and all with limitations in the result reporting

### Overview

- **Taxonomy**. We first identify and classify the primary challenges in rigorous agentic evaluation. In Figure 1, we decompose the operational and conceptual process of agentic evaluation

    ![[Agentic Evaluation Overview (ABC Paper).png| center | 700]]
    *Figure 1: Operational and conceptual processes of agentic evaluation.*

- Conceptually, an agentic evaluation is rigorous if and only if:
    1. the target capability is equivalent to task success (i.e., task validity)
    2. the task success is equivalent to a positive evaluation result (i.e., outcome validity)
- However, agentic benchmark presents two unique challenges that makes these two validity conditions difficult to hold:
    1. *Complex task setup*: In addition to task descriptions as inputs, agentic benchmarks set up an environment for agents to operate in and provide tools for agents to use.
    2. *Unstructured task outcome*: Agentic benchmarks expect unstructured data as task outcomes, such as textual responses, code, and file edits. Verifying the correctness of such outcomes are non-trivial and requires specially designed methods.
- First, improper task setup can lead to the violation of task validity. For instance, $\tau$-bench includes intentionally unattainable tasks (e.g., making changes to a non-refundable ticket), which agents are supposed to recognize and reject
    - Yet, a trivial agent that simply returns nothing is considered a successful completion even though it cannot look up information or interpret ticket rules
- Second, failure to rigorously grade unstructured task outcome can break outcome validity.
    - For example, SWE-bench-Verified judges agent-generated patches by handwritten unit tests.
    - Since such tests can be incomplete or not perfectly sound

### ABC: Agentic Benchmark Checklist

- **Assessing Task Validity**

    ![[ABC Checklist - Task Validity.svg| center | 700]]
    *Figure 2: Checks in ABC to assess the task validity of an agentic benchmark.*

    - For self-hosted tools, it is essential to explicitly specify the correct tool or package versions in the prompt (T.1)
    - In terms of API-based tools, ensuring service availability and managing rate limits is crucial (T.2)
    - If API interruptions occur, we recommend detecting them and terminating the evaluation to keep benchmark users informed (T.3)
    - First, to ensure the independence of tasks, we need to ensure that any legacy data and states are fully cleaned up before starting a new task (T.4)
    - to avoid cheating by peeking at ground truth, it is important to fully isolate agents from the ground truth results (T.5)
    - the environment setup should be fully reproducible and frozen at the time of benchmark release (T.6)
    - we recommend verifying the correctness of ground truth annotation and the task setup (T.7-8)
    - Providing an automatic oracle solver can help demonstrate the correctness of the task configuration (T.9)
    - inspecting outliers in pilot experiments is crucial for identifying implementation bugs (T.10)
        - For example, if agents consistently fail on easy tasks, this may indicate that tasks are impossible, whereas if agents only succeed on difficult tasks, it may indicate shortcuts.
- **Assessing Outcome Validity**

    ![[ABC Checklist - Outcome Validity.svg| center | 700]]
    *Figure 3: Checks in ABC to assess the outcome validity of an agentic benchmark.*

    - we recommend manually verifying the correctness and quality of test cases (O.d.1)
        - and providing quality guarantees using objective metrics (O.d.2) such as coverage and cyclomatic complexity
    - We should tailor the input generator to the target program, covering different data values, types, memory layouts, and edge cases (O.e.1-2)
        - the inputs must affect the output (O.e.3)
    - *End-to-end (E2E) Testing* simulates complete user workflows, providing comprehensive testing of system functionality
        - In addition to ensuring the general quality of test cases, it should also cover all possible branches of user workflows (O.f.1)
        - Because of their complexity, E2E tests require extra safeguards to eliminate non-determinism and ensure repeatable results (O.f.2)
    - We identify three key checks for rigorous state matching.
        - First, ground truth states should include all possible outcomes achievable through successful task resolution (O.g.1)
        - state space should contain both relevant and irrelevant states (O.g.2), such as including both changed and unchanged files, to help detect if agents affect the environment outside the target scop
        - the state space should be complex enough (O.g.3)—for instance, involving multiple variables or dependencies—so that random or trivial changes are unlikely to result in a correct outcome
    - We find that parsers in existing benchmarks may make implicit assumption about the agent’s output (O.h.1). For example, the MATH dataset assumes the answer of the agent starts with “Answer:”
        - to ensure that a single final answer reflects a genuine reasoning process, we recommend designing tasks in a way that avoid success by guessing (O.h.2)
    - *Quality Measure* evaluates agent using customized metrics against a baseline when ground truth is impossible to achieve
        - To avoid metric hacking—achieving high metrics without resolving tasks, we recommend ensuring that the selected metrics are strongly correlated with the reasoning process (O.i.1).
- **Assessing the Benchmark Reporting**

    ![[ABC Checklist - Benchmark Reporting.svg| center | 700]]
    *Figure 4: Checks in ABC to assess the benchmark reporting.*

    - *Transparency and Validity*. We encourage open-sourcing both the datasets and evaluation harness (R.1-2)
        - while including measures to prevent data contamination (R.3-4)
        - We also recommend clearly specifying the capabilities to evaluate and articulating construct validity (R.5-6).
    - *Mitigation*. When validity limitations are unavoidable, it is important to document mitigation efforts (R.7)
        - and provide both qualitative and quantitative evidence regarding the impact of those limitations (R.8-9)
    - *Result Interpretation*. We recommend reporting benchmark results rigorously, including measures of statistical significance (R.10)
        - clear interpretation guidelines (R.11)
        - and appropriate baseline comparisons (R.12-13)
