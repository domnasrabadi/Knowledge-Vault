---
type: paper
status: structured
quality:
topics: [agent-evaluation, ai-agents, evaluation-metrics]
source: ""
created: 2025-07-17
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: Frank F. Xu, Yufan Song, Boxuan Li, Yuxuan Tang, Kritanjali Jain, Mengxue Bao, Zora Z. Wang, Xuhui Zhou, Zhitong Guo, Murong Cao, Mingyang Yang, Hao Yang Lu, Amaad Martin, Zhe Su, Leander Maben, Raj Mehta, Wayne Chi, Lawrence Jang, Yiqing Xie, Shu...
- Category: pdf
- Document Tags: great 
- URL: https://arxiv.org/pdf/2412.14161
# 2 Highlights
- TheAgentCompany = extensible benchmark that measures how well ai agents perform digital-worker tasks by browsing the web, writing code, running programs, and collaborating with coworkers
    - motivation = assess real-world task automation potential amid rapid month-by-month llm progress
    - current frontier best (Gemini-2.5-Pro) completes ≈30 % of tasks autonomously and scores 39 % with partial credit
- benchmark desiderata
    - coverage of multiple work-related tasks = spans diverse job categories (SDE, PM, DS, Admin, HR, Finance, Other)
    - interaction requirement = agents must communicate with simulated coworkers; most prior benchmarks ignore this
    - long-horizon tasks with checkpoints = include multistep goals that mirror extended human workflows
    - versatile environment interface = supports web browsing, command-line, jupyter ipython, and corporate communication tools
    - self-hosted + reproducible = tasks, data, and evaluators run locally for consistent results
- task structure
    - task intent = english description clear enough for a human worker
    - checkpoints = intermediate milestones with point values
        - action completion = verifies tool use, url navigation, data collection
        - data accuracy = checks correctness and completeness of outputs
        - collaboration = scores interactions with coworkers or sharing results
    - evaluators = programs (deterministic or llm-based) that judge each checkpoint
- evaluation metrics
    - full completion score $S_{\text{full}}$ = 1 if all checkpoints passed, else 0
    - partial completion score $S_{\text{partial}} = 0.5 \cdot \frac{\text{Result}}{\text{Total}} + 0.5 \cdot S_{\text{full}}$
        - linear credit for progress plus a bonus that strongly rewards full task completion
    - number of steps = total llm calls used, measuring agent efficiency
- task creation pipeline
    - choose job categories then concrete tasks with clear goals
    - curate each task: write intent, checkpoints, evaluators, and initialization scripts
    - involve domain experts; 20 contributors spent ≈3 000 person-hours over 2 months
- environment architecture
    - interfaces
        - bash shell through sandboxed os
        - jupyter ipython server
        - chromium browser via BrowserGym primitives (navigate, click, type, scroll)
    - actions = `IPythonRunCellAction`, `CmdRunAction`, browser actions
    - observations = terminal output, ipython results, browser snapshots + accessibility trees
    - workflow = backbone llm receives history + current observation → outputs next action
- experimental results
    - overall performance
        - Gemini-2.5-Pro tops leaderboard yet fully solves only 30 % of tasks
        - long-horizon and ui-heavy tasks remain hard for all agents
    - platform analysis ?
        - complex web-based office suites cause high failure rates
    - task-type analysis ?
        - DS, Admin, Finance tasks show lowest success
        - SDE tasks surprisingly easier for llms, likely due to coding-centric pretraining and benchmarks
- common agent failures
    - lack of social skills = misinterpret coworker goals and implications
    - incompetence in browsing = struggle with modern web uis and distractions
    - self-deception = fabricate shortcuts when unsure, skipping hard steps
- implications + limitations
    - benchmark focuses on tasks with programmatic evaluation; creative tasks (ideation, architecture design) omitted
    - only two agent scaffolds evaluated; other designs may perform differently
    - tasks devised via introspection; may not fully reflect real enterprise workloads
    - no human performance baseline collected due to cost
- future directions
    - expand task diversity, especially creative and open-ended work
    - compare additional agent frameworks and fine-tuning strategies
    - investigate methods to improve social reasoning, web navigation, and long-horizon planning



![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/0abb103129a6fd12e7b2a425dfb7343b.png)



![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/6d7305bfcfd98542e62c6d5022e19fc9.png)

![[Screenshot 2025-07-17 at 7.31.46 pm.png]]

