---
type: article
status: structured
quality:
topics: [agent-evaluation, model-monitoring, llm-judges]
source: ""
created: 2025-07-06
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- LLM Agent Evaluation: Assessing Tool Use, Task Completion, Agentic Reasoning, and More
	- Author: langchain.com
	- Category: article
	- URL: https://docs.smith.langchain.com/evaluation/concepts
- Applying RAG Evaluation​
	- Author: confident-ai.com
	- Category: article
	- URL: https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide
# 2 Highlights
- agentic evaluation = assessment approach acknowledging that component-level interactions can amplify or mask failures
- two levels of llm agent evaluation
    - end-to-end evaluation = black-box check of overall task completion for a given input
    - component-level evaluation = granular inspection of sub-agents, rag pipelines, api calls to pinpoint failures
- llm agent evaluation vs traditional llm evaluation
    - architectural complexity = agents chain multiple components in intricate workflows
    - tool usage = agents invoke external tools + apis to act on the real world
    - autonomy = agents decide next steps with minimal human input
    - reasoning frameworks = agents employ structured planning (e.g. React) to guide behaviour
- core characteristics of llm agents
    - tool invocation & api calls = enable actions like database updates, restaurant bookings, stock trades, web scraping
        - mis-chosen tools, bad parameters, unexpected outputs can derail workflow
    - high autonomy = multi-step plans magnify impact of any single error
    - intermediate reasoning = deliberate thinking (e.g. React) prevents rash actions but flawed logic can loop indefinitely
- evaluation of tool use
    - primary metrics = Tool Correctness + Tool Efficiency
    - tool correctness = deterministic check that required tools were called properly
        - tool selection = compare called tools vs ideal set
        - input parameters = verify parameter accuracy against ground truth
        - output accuracy = compare tool outputs to expected results
        - flexible scoring
            - order independence = evaluate sets of tools, not sequences
            - frequency flexibility = tolerate repeated calls if harmless
            - partial credit = percentage match for parameters or numeric deviation for outputs
    - tool efficiency = measures cost + latency impact of tool calls
        - redundant tool usage = % of unnecessary tools in total calls
        - tool frequency = penalise calls exceeding threshold (often 1)
- agentic task completion
    - task completion = did the agent fulfil the user’s intent end-to-end
    - DeepEval Task Completion metric = llm-judge determines task, analyses reasoning + tool usage + final answer to decide success
    - G-Eval = llm-as-evaluator with chain-of-thought can assess any custom criterion
- agentic reasoning evaluation metrics
    - reasoning relevancy = each tool call rationale clearly linked to user need ?
    - reasoning coherence = logic flows step-by-step without gaps ?
- component-level evaluations
    - modular agents allow metric attachment to each component for precise failure tracing
    - rag metrics at both levels
        - answer relevancy
        - faithfulness
        - contextual relevancy
        - contextual precision
        - contextual recall
    - tool use metrics apply directly via invocation logs
    - safety metrics (bias, toxicity, harmful content) applicable at llm output or aggregated agent response
    - tracing = record every retrieval, rerank, generation, tool call to locate low-scoring components and target fixes
- LangSmith framework building blocks
    - datasets = collections of test inputs + optional reference outputs
        - example =
            - inputs = dict of variables for the application
            - reference outputs = dict used only by evaluators
            - metadata = extra attributes for filtering views
        - selecting valuable runs to add
            - user feedback = surface datapoints with negative ratings ?
            - heuristics = flag runs with long latency or anomalies ?
            - llm feedback = second llm labels sessions needing rephrase or correction ?
        - dataset augmentation
            - begin with handcrafted seed examples
            - generate synthetic examples that echo seeds for scale
        - dataset partitioning
            - small fast-iterate split
            - large final-eval split
    - evaluators = scoring functions operating on {example, run}
        - heuristic evaluators = deterministic rules (non-empty reply, code compiles, exact class match)
        - llm-as-judge evaluators = llm grades output
            - reference-free = check policy compliance, toxicity, style
            - reference-based = compare to ground truth for factuality
        - pairwise evaluators = rank two outputs when absolute score tough (e.g. summarization)
        - human feedback = highest value qualitative judgment
- evaluation fundamentals
    - evaluation = measures performance via metric, useful relatively
    - testing = asserts correctness, must pass for deploy
    - metrics ⇒ tests = turn fuzzy measures into binary gates
    - offline evaluation = pre-compiled dataset, pre-deployment
    - online evaluation = live traffic, near realtime
- agent evaluation granularity
    - final response = end-to-end success of agent on task
        - pros = holistic check
        - cons = slow, hard to debug internals, metric definition tricky
    - single step = inspect individual action (tool selection + parameters)
        - pros = fast, pinpoints failure, simple heuristics
        - cons = ignores full context, dataset creation tougher with history
    - trajectory = analyse sequence of tool calls
        - exact trajectory = binary match of ordered calls
        - flexible metrics
            - count incorrect steps
            - set coverage of expected tools regardless of order
- rag evaluation modes
    - offline = reference answer available (answer correctness)
    - online = reference-free prompts assessed in realtime
    - pairwise = compare answers from different rag chains on user criteria