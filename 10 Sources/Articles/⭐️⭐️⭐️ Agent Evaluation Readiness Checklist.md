---
type: article
status: raw
quality: 3
topics: [agent-evaluation, error-analysis, llm-judges, evaluation-metrics]
source: https://blog.langchain.com/agent-evaluation-readiness-checklist/
created: 2026-08-08
published: 2026-03-27
author: LangChain Blog
flashcards: none
updated: 2026-08-10
---

# Agent Evaluation Readiness Checklist

<div align="center">
  <img src="https://blog.langchain.com/content/images/2026/03/23---Agent-Evaluation-Readiness-Checklist-2.svg" width="220" />
</div>

- This post focuses on the ***how,*** a step-by-step checklist for building, running, and shipping agent evals.
- **Start with the simplest eval that gives you signal.** A few end-to-end evals that test whether your agent completes its core tasks will give you a baseline immediately, even if your architecture is still changing

##### Manually review 20-50 real agent traces before building any eval infrastructure

- Before building any infrastructure, spend 30 minutes reading through real agent traces. You'll learn more about failure patterns from this than from any automated system

##### Define unambiguous success criteria for a single task

- If two experts can't agree on pass/fail, the task needs refinement:
- • *Unclear success:* "Summarize this document well." • *Clear success:* "Extract the 3 main action items from this meeting transcript. Each should be < 20 words and include an owner if mentioned."
- You need both because they serve different purposes. Capability evals push your agent forward by measuring progress on hard tasks, while regression evals protect what already works
- • *Capability evals* answer "what can it do?" • Start with a low pass rate and give you a hill to climb. • *Regression evals* answer "does it still work?" • Should have ~100% pass rate and catch backsliding.
- If you can't articulate why something failed, you need more error analysis before building automated evals. This is where you should spend [60-80% of your eval effort](https://hamel.dev/blog/posts/evals-faq/?ref=blog.langchain.com).
- Follow this process: 1. **Gather traces:** Collect representative failures from production or testing 2. **Open coding:** Review traces with a domain expert, noting every issue you see without pre-categorizing (or use our [annotation queue](https://docs.langchain.com/langsmith/annotation-queues?ref=blog.langchain.com) to have subject matter experts review traces on their own) 3. **Categorize:** Group issues into a failure taxonomy (prompt problems, tool design problems, model limitations, tool failures, data gaps, etc.) 4. **Iterate:** Keep reviewing until you stop discovering new failure categories
- Once you've categorized, the fix depends on the root cause:
    - **Prompt problem**: The agent misunderstood because your instructions were unclear → fix the prompt
    - **Tool design problem**: The tool interface made it easy for the agent to make mistakes → redesign parameters, add examples, clarify boundaries
    - **Model limitation**: Instructions were clear but the LLM doesn't generalize to edge cases → add examples, try a different architecture, or use a different model
    - **Don't know yet**: You haven't looked at enough failures to see the pattern → do more error analysis first

##### Assign eval ownership to a single domain expert

- Someone needs to own the eval process: maintaining datasets, recalibrating judges, triaging new failure modes, and deciding what "good enough" means. Ideally one domain expert acts as the quality arbiter for ambiguous cases rather than designing by committee.

### Choose your evaluation level

- Understand the three evaluation levels: single-step (run), full-turn (trace), and multi-turn (thread)
- **Start with trace-level (full-turn) evals, then layer in run-level and thread-level as needed**
- These answer: "Did the agent choose the right tool?" "Did it generate a valid API call?" They're the easiest to automate but require stable agent architecture; if you're still changing your tool definitions, run-level evals may break.
- Grade a full trace across three dimensions:
    - **Final response**: Is the output correct and useful?
    - **Trajectory**: Did the agent take a reasonable path? (Not necessarily the *exact* path you expected, just a valid one)
    - **State changes**: Did the agent create the right artifacts? (files written, database updated, meeting scheduled, etc.)
- State change evaluation is often overlooked but critical for agents that *do* things, not just *say* things. For example, if your agent schedules meetings, don't just check that it said "Meeting scheduled!" Verify the calendar event actually exists with the right time, attendees, and description

- Multi-turn evals
    - Start with trace-level (full-turn) evals, then layer in run-level and thread-level as needed
    - Trace-level gives you the most signal per eval. Run-level is useful for debugging specific steps. Thread-level matters when your agent has multi-turn conversations.

### Dataset construction


##### Ensure every task is unambiguous, with a reference solution that proves it's solvable

- • *Ambiguous:* "Find me good flights to NYC." • *Unambiguous:* "Find roundtrip flights from SFO to JFK, departing Dec 15-17, returning Dec 22, under $400, economy class."
- Include a reference solution for every task so you can prove it's solvable and have a baseline to grade against.
- Test the negative cases too. Include examples designed to falsify your assumptions, not just confirm expected behavior.

##### Ensure dataset structure matches your chosen evaluation level

- • Run-level (single-step) evals need reference tool calls or decisions • Trace-level (full-turn) evals need expected final outputs and/or state changes • Thread-level (multi-turn) evals need multi-turn conversation sequences with expected context retention
- • **Conversational agents**: Include multi-dimensional criteria, task completion *and* interaction quality (empathy, clarity) • **Research agents**: Include groundedness checks (are claims supported by sources?) and coverage checks (are key facts included?)

##### Generate seed examples if you lack production data

- Define the key dimensions of variation for your task (query complexity, topic, edge case type). Manually create ~20 example inputs covering those dimensions, run them through your existing agent, review and modify them to store as reliable ground truths.
- Once you're past the cold start, you need an ongoing pipeline for discovering new evals. Two strategies work well together:
- Dogfood your agent daily and turn every error into an eval. This is different from production monitoring; it's your team intentionally stress-testing the agent across real workflows.
- Write focused tests by hand for specific behaviors you think are important, like "does the agent parallelize tool calls?" or "does it ask clarifying questions for vague requests?"

### Grader Design

- Select specialized graders per evaluation dimension: default to code-based for objective checks, LLM-as-judge for subjective assessments, human for ambiguous cases, and pairwise for version comparison
    - Tip: Rather than trying to create a correctness evaluator, decompose evaluation into specialized graders per dimension rather than one monolithic grader.
    - For example: the Witan Labs team built 5 specialized evaluators (content accuracy, structure, visual formatting, formula scenarios, text quality), each with dimension-appropriate thresholds. This gives you clearer signal about what's actually failing
- Distinguish guardrails (inline, runtime) from evaluators (async, quality assessment)
    - Safety checks and format validation are guardrails, they should run inline. Quality assessment and regression testing are evaluators, they run async. Don't confuse the two.
- Prefer binary pass/fail over numeric scales
    - A 1-5 scale introduces subjective differences between adjacent scores and requires larger sample sizes for statistical significance. Binary forces clearer thinking: either the agent succeeded or it didn't. You can always decompose a complex task into multiple binary checks
- Calibrate LLM-as-a-Judge graders to human preferences
    - Include reasoning in the judge's output; this improves accuracy and lets you audit *why* it scored something
    - Use [few-shot examples](https://docs.langchain.com/langsmith/create-few-shot-evaluators?ref=blog.langchain.com) to improve evaluator consistency
- Grade the outcome, not the exact path, and build in partial credit for incremental progress
    - As Anthropic puts it in [Demystifying Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents?ref=blog.langchain.com): "Don't grade the path the agent took, grade what it produced." If you require "must call tool A → B → C in that order," you'll fail agents that found a smarter route. *Better:* "Did the meeting get scheduled correctly?" not "Did it call `check_availability` before `create_event`?"
    - An agent that correctly identifies the problem but fails at the final step is better than one that fails immediately. Build in partial credit so your metrics reflect incremental progress.
- Use custom evaluators derived from your error analysis, not generic off-the-shelf metrics

### Running & Iterating

- Distinguish between offline, online, and ad-hoc evaluation and use all three
    - Most of this checklist focuses on offline evaluation, and that's intentional. Offline evals are where you improve with: curated datasets, controlled experiments, iterating before you ship. You'll also need online and ad-hoc evaluation once your agent hits production.
- Run multiple trials per task to account for non-determinism
    - Model outputs vary between runs. Use multiple [repetitions](https://docs.langchain.com/langsmith/repetition?ref=blog.langchain.com) if not cost prohibitive. When running multiple trials, compute confidence intervals before declaring improvement—single-run benchmarks are noisy. For non-deterministic agents, consider using pass@k (at least one of k attempts succeeds) or pass^k (all k attempts succeed) metrics depending on your product requirements.
- Manually review traces for failed evaluations to verify grader fairness
    - A "failed" task might actually be a creative valid solution your grader didn't anticipate. Reading traces is how you know if your graders are being fair.
- Ensure each trial runs in a clean, isolated environment with no shared state
- Tag evals by capability category, document what each measures, and track efficiency metrics (step count, tool calls, latency) alongside quality
    - Track operational metrics alongside quality: turns taken, token usage, latency, cost per task.
    - Group evals by what they test, not where they come from. Categories like `file_operations`, `retrieval`, `tool_use`, `memory`, and `conversation` give you a "middle view" of performance between a single aggregate score and individual test results. Add a docstring to each eval explaining how it measures an agent capability. This keeps intent clear as the suite grows and lets you run targeted subsets (e.g., only `tool_use` evals after changing a tool definition).
    - Attach metadata to every experiment so you can [filter, group, and compare runs](https://docs.langchain.com/langsmith/filter-experiments-ui?ref=blog.langchain.com) across dimensions that matter. This makes it easy to answer questions like "did switching from GPT-4.1 to Claude Sonnet improve accuracy?" or "which prompt version regressed on this dataset?" without digging through logs
    - Once quality is established, compare models on efficiency. An agent that's 95% accurate but 10x slower might not be an improvement. Track ratios like observed steps / ideal steps, observed tool calls / ideal tool calls, and observed latency / ideal latency. This doesn't conflict with "grade the outcome, not the exact path": ideal trajectories measure efficiency, not correctness
- Recognize when pass rates plateau and evolve your test suite accordingly
    - When your pass rate plateaus and adding more tasks of the same type stops revealing new failure modes, it's time to evolve: add harder tasks, test new capabilities, or shift to different dimensions. Grinding on a saturated eval set wastes effort.
- Only keep evals that directly measure a production behavior you care about
    - Every eval applies pressure on your system over time. It's tempting to blindly add hundreds of tests, but this creates an illusion of progress
    - Build targeted evals, and periodically prune the ones that no longer give you signal
- Invest in tool interface design and testing, not just prompt optimization
    - Tool design eliminates entire classes of agent errors. Anthropic's team [noted](https://www.anthropic.com/research/building-effective-agents?ref=blog.langchain.com) they spent more time optimizing tools than prompts when building their SWE-bench agent
    - Test how the model actually uses your tools: try different parameter formats (diffs vs full rewrites, JSON vs. markdown), redesign interfaces to make mistakes harder, and invest in clear documentation with examples. The goal is to make mistakes structurally impossible, not just unlikely
- Distinguish between task failures (agent got it wrong) and evaluation failures (grader got it wrong)

### Production Readiness

- Promote capability evals with consistently high pass rates into your regression suite
    - Once you've climbed the hill, protect it. Tasks that used to test "can we do this?" become "can we *still* do this?"
- Integrate regression evals into your CI/CD pipeline with automated quality gates
    - A typical flow:
        1. **Code or prompt change** triggers the pipeline (via `git push`, PromptHub update, or manual trigger)
        2. **Offline evals run** unit tests, integration tests, and evaluation against curated datasets using cheap, fast graders
        3. **Preview deployment** goes up if offline evals pass
        4. **Online evals run** against the preview with live data using LLM-as-judge graders
        5. **Promote to production** only if all quality gates pass, otherwise route failing traces to annotation queues and alert the team
    - Use cheap code-based graders in CI for every commit. Reserve expensive LLM-as-judge evaluations for preview/production evaluation
- Capture user feedback
    - Once your agent is in production, [user feedback](https://docs.langchain.com/langsmith/attach-user-feedback?ref=blog.langchain.com#log-user-feedback-using-the-sdk) becomes one of your most valuable signals. Automated evals can only catch the failure modes you already know about. Users will surface the ones you don't: edge cases your dataset missed, outputs that are technically correct but unhelpful, and workflows that break in ways you never anticipated.
    - Capturing this feedback in a structured way lets you feed it back into your datasets, calibrate your graders against real-world expectations, and prioritize the improvements that actually matter to the people using your agent.
- Schedule regular manual exploration of production traces beyond automated checks
- Version your prompts and tool definitions alongside your code
- Ensure production failures feed back into datasets, error analysis, and eval improvements
### Full Checklist

- **Before you build evals**
    - [ ] Manually review 20-50 real agent traces before building any eval infrastructure
    - [ ] Define unambiguous success criteria for a single task
    - [ ] Separate capability evals from regression evals
    - [ ] Ensure you can identify and articulate why each failure occurs
    - [ ] Assign eval ownership to a single domain expert
    - [ ] Rule out infrastructure and data pipeline issues before blaming the agent

- **Choose your evaluation level**
    - [ ] Understand the three evaluation levels: single-step (run), full-turn (trace), and multi-turn (thread)
    - [ ] Start with trace-level (full-turn) evals, then layer in run-level and thread-level as needed

- **Dataset construction**
    - [ ] Ensure every task is unambiguous, with a reference solution that proves it's solvable
    - [ ] Test both positive cases (behavior should occur) and negative cases (behavior should not occur)
    - [ ] Ensure dataset structure matches your chosen evaluation level
    - [ ] Tailor datasets to your agent type (coding, conversational, research)
    - [ ] Generate seed examples if you lack production data
    - [ ] Source from dogfooding errors, adapted external benchmarks, and hand-written behavior tests
    - [ ] Set up a trace-to-dataset flywheel for continuous improvement

- **Grader Design**
    - [ ] Select specialized graders per evaluation dimension: default to code-based for objective checks, LLM-as-judge for subjective assessments, human for ambiguous cases, and pairwise for version comparison
    - [ ] Distinguish guardrails (inline, runtime) from evaluators (async, quality assessment)
    - [ ] Prefer binary pass/fail over numeric scales
    - [ ] Calibrate LLM-as-a-Judge graders to human preferences
    - [ ] Grade the outcome, not the exact path, and build in partial credit for incremental progress
    - [ ] Use custom evaluators derived from your error analysis, not generic off-the-shelf metrics

- **Running & Iterating**
    - [ ] Distinguish between offline, online, and ad-hoc evaluation and use all three
    - [ ] Run multiple trials per task to account for non-determinism
    - [ ] Manually review traces for failed evaluations to verify grader fairness
    - [ ] Ensure each trial runs in a clean, isolated environment with no shared state
    - [ ] Tag evals by capability category, document what each measures, and track efficiency metrics (step count, tool calls, latency) alongside quality
    - [ ] Recognize when pass rates plateau and evolve your test suite accordingly
    - [ ] Only keep evals that directly measure a production behavior you care about
    - [ ] Invest in tool interface design and testing, not just prompt optimization
    - [ ] Distinguish between task failures (agent got it wrong) and evaluation failures (grader got it wrong)

- **Production Readiness**
    - [ ] Promote capability evals with consistently high pass rates into your regression suite
    - [ ] Integrate regression evals into your CI/CD pipeline with automated quality gates
    - [ ] Capture user feedback
    - [ ] Schedule regular manual exploration of production traces beyond automated checks
    - [ ] Version your prompts and tool definitions alongside your code
    - [ ] Ensure production failures feed back into datasets, error analysis, and eval improvements
