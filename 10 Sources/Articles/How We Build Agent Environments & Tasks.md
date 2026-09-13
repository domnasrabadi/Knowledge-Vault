---
type: article
status: raw
quality: 
topics: [agent-evaluation, synthetic-data, agent-harnesses, ai-agents]
source: https://x.com/vtrivedy10/status/2092266609838604368/?s=12&rw_tt_thread=True
created: 2026-09-06
published: 2026-08-25
author: Viv
flashcards: none
updated: 2026-09-13
---

# How We Build Agent Environments & Tasks

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1805079750873923584/7sTh63Eo.jpg" width="220" />
</div>

- **TLDR:** This is a practical guide on how we create synthetic agent environments and tasks.
    - By the end, we have a two-step pipeline.
        1. The first step takes traces, code, and/or human input to build a detailed spec.
        2. The second step takes that spec and creates an eval task and an environment for that task.
    - In order to do this, we create a “world spec” to capture shared knowledge, scripts, and important definitions.
- To reliably improve agents, you need a good benchmark to run your agents over.
    - This helps identify regression, find areas for improvement, and generally make sure you can iterate on your agent backed by real metrics.
- Building a good benchmark is hard.
    - Each task in the benchmark needs to have a representative input, an environment that closely aligns to the real world, and an aligned rubric to grade the result on.
    - It takes a lot of time, effort and human alignment to create a single task, let alone a whole dataset.

## What is the ideal end state?

- end state we are working towards is a dataset of **high-quality, vetted tasks.**

## A pipeline to create tasks

- In order to generate a large number of these tasks, we find it is most efficient to build a pipeline to produce these tasks. We find that a core piece of creating this pipeline is the concept of a “spec”.
    - A spec is a markdown file that describes what the task (input, environment, graders) looks like in natural language.
- The benefit of having this concept of a spec is that it separates:
    1. figuring out what each task should look like
        - first step - “figuring out what the task should look like” - can be done in multiple ways, and often requires human iteration to align on what matters to the team and users.
    2. building a task
        - second step - “building the task” - can ideally be more automated with an agent.
- separation allows you to create many of different specs, centralize the human review process there, and then parallelize building them.
- end state is a pipeline that consists of two steps:
    1. A Spec generation step
    2. A Spec2Task creation step
- To do either of those steps well requires gathering specific information about the general dataset you’re trying to create. We call this information “world knowledge” and it lives in “world spec.”
    - This information is NOT specific to a single task - if it was, it would live in the task spec. Rather, it is general knowledge across all potential tasks in a dataset (ie. the “world”).
    - creation Guidance on what pieces of information are helpful to store such as size/shape of data
    - Scripts for parsing traces (or other data) to extract information
    - creation Knowledge of how to create good rubrics for this task (ex: programmatic vs LLM-as-a-judge)
    - Scripts for generating specific data to populate the environment

## Why generating a world spec is an iterative process

- In order to generate specs or transform specs into tasks you need a “world spec”. How do you get this world spec and make it useful?
    - found that the best way to get this spec is work hand in hand with a coding agent to generate a first task, and then have it write up a general world spec that it learned along the way to use in the future.
- What is the coding agent doing in practice when using the `eval-engineering` skill to create a first task and then build a world spec?
    - Scanning the repository with subagents to find the exact prompts, tools, skills, etc that an agent interacts with.
    - Grouping traces to find real world patterns of what users are asking the agent to do. These groups are good for brainstorming potential types of tasks
    - Mapping out what credentials would be needed to run an agent. Does the agent call any live tools via APIs such as web search? Should we simulate this behavior or call it live during a Task?
    - Cataloging all services an agent interacts with and their data schemas. Systems like SalesForce or Gong including the tables + schemas the agent interacts with.
    - Finding relationships/hierarchies in data, and planning how good approaches to do synthetic data generation depending on the types of input data.
- A lot of this knowledge is specific to the agent or domain a user is trying to make Tasks for.
- core part creating a world spec is iteratively gathering user feedback

## What does a task spec contain

- process of generating a single task requires writing down all of the implementation details specific to that task but informed by the overall world knowledge.
- spec we create generally should cover three parts:
    - What the agent environment looks like
    - What the inputs should be
    - How the outputs should be scored
- Some of these may be optional, if they are the same for all tasks and can be covered by the “world spec”. For example:
    - For general QA chatbots, the environment may always be the same (it’s just the inputs/outputs that change). In this case, the environment information could be consolidated in the “world spec” and shared across tasks.

## Spec2Task

- Spec-to-task is the pipeline for taking a spec and generating a task
    - most easily done with a coding agent.
- Some learnings we found on good Spec2Task creation:
    - Have the pipeline refine tasks by running them with real agents and reading trajectories.
        - helps them find any flaws in environment design such as overly specific instructions or leaky abstractions.
    - difficultly of tasks can be calibrated by having the pipeline run each task with different tier models
    - Agents are bad at knowing what method to use for generating different types of data. So we give them overall guidance such as using LLMs with rubrics for free-text data and using scripts with sqlite + specified schemas for tabular data.

## End to end process

1. Use `eval-engineering` to create a first task
    - Make sure the `eval-engineering` skill is loaded
    - **Example Prompt:**

        ```
        Use the eval-engineering skill, the traces from {LangSmith project}, and the {current repository} to help me create an eval Task for {agent}.
        ```

    - This will involve some back and forth, will create (and surface to user) a separate skill for the world spec, and after agreement will create a Task
2. Review the world spec skill and make any adjustments necessary
    - **Example Prompt:**

        ```
        Review the {world spec folder name} skill, tell me the core parts of what it says so I can review it
        ```

3. Use “world spec” and `eval-engineering` to create a second task
    - Switch thread so you can properly validate the world spec skill. Make sure the world spec skill AND eval engineering skill are loaded.
    - **Example Prompt:**

        ```
        Use the {world spec} skill to create a new task. This task should…
        ```

    - This will involve some back and forth, and will update the {world spec} skill
4. Repeat step 2
    - **Example Prompt:**

        ```
        The customers in this task look too similar. Expand the customer set with bigger and smaller customers with varying amounts of revenue, total employees, emails sent, etc.”
        ```

5. Repeat steps 3-4 until confident
6. Scale this process with a coding agent with “world spec” to look at a bunch of traces and generate specs
    - **Example Prompt:**

        ```
        Use {world spec} to create 10 new, different task specs for me to review. Use traces from the last 10 days to find new patterns we’re not capturing today in our tasks.
        ```

7. Run each of those specs through a coding agent with “world spec” to create a bunch of tasks
    - **Example Prompt:**

        ```
        Use {world spec} with {task spec X} to create a new task.
        ```

## Where human judgment is still needed

- Agents still need human guidance in two areas.
    - First, refining specs often requires several rounds of feedback.
        - The agent needs help determining whether a spec accurately reflects the real-world domain, user behavior, and task requirements.
    - Second, agents tend to create tasks that are too easy.
        - This helps validate that the environment works, but a useful benchmark needs tasks across a range of difficulty levels.
        - Calibrating that difficulty usually requires running each task multiple times, reviewing the trajectories, and asking the agent to make the task easier or harder.
