---
type: article
status: structured
quality:
topics: [agent-frameworks, ai-agents]
source: ""
created: 2025-06-15
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 overview
- lightweight Python library for building agentic AI applications
- focuses on simplicity with a few core primitives:
    - agents
    - tools
    - handoffs
    - guardrails
    - runner
- provider-agnostic (supports OpenAI models via Chat Completions and Responses API)
---
# 2 agent definition
- agent = LLM-based persona configured with:
    - **instructions**: system prompt defining behavior
    - **model and settings**: specify model (e.g. OpenAI GPT) and optional generation params like temperature, top_p, etc.
    - **tools**: functions or actions the agent can call
    - **handoffs**: optional list of sub-agents for task delegation
    - **guardrails**: optional input/output validation rules
    - **name**: agent identifier
---
# 3 tools
- tools = Python functions the agent can use
    - use `@function_tool` decorator to register
    - SDK auto-generates:
        - name = function name
        - description = docstring
        - parameter schema = from type hints (via `inspect` and Pydantic)
- during agent execution:
    - if the LLM calls a tool, SDK intercepts, executes, and returns result
- control tool usage via `ModelSettings.tool_choice`:
    - `"required"`: force tool usage
    - `"none"`: forbid tool usage
    - specific tool name: force that tool
    - default = `"auto"`
- supports async and sync functions (async tools are awaited automatically)
- tools can access the run context if needed
- built-in tools:
    - `WebSearchTool` = internet search
    - `FileSearchTool` = vector store retrieval
    - `ComputerTool` = code execution
---
# 4 agents as tools
- `agent.as_tool()` = converts an agent into a callable tool
    - allows one agent to call another as a subroutine
    - useful for modular tasks without full handoff
    - on tool-call failure:
        - agent receives error notice and continues
        - customize with `failure_error_function` or propagate errors directly
---
# 5 agent loop and runner
- runner = manages the core agent loop
    - `Runner.run(...)` (or `run_sync`)
    - inputs: agent + initial input (e.g. user query)
    - optional: `max_turns` to limit dialogue rounds
- returns `RunResult`:
    - `final_output`: model’s response
    - full message/action history for debugging or chaining
- supports multi-turn conversations by passing history into subsequent runs
---
# 6 handoffs (multi-agent orchestration)
- handoff = agent delegates to another agent mid-conversation
    - define via `handoffs=[...]` or `handoff()` helper
    - can customize:
        - tool name and description
        - `on_handoff` callback
        - input schema (using Pydantic)
    - receiving agent sees full conversation history by default
        - filter or transform input via input filters
    - SDK provides a system prompt template for handoffs
---
# 7 guardrails
- guardrails = parallel validation checks on agent inputs or outputs
- attach via `guardrails=[...]` or `run_config`
- useful for safety, constraint enforcement, or output checking
---
# 8 context and dependency injection
- `RunContextWrapper` = context object passed into `Runner.run(...)`
    - can include user data, DB connections, etc.
    - accessible to all agents, tools, and hooks
    - not sent to the LLM – used for backend logic only
---
# 9 dynamic instructions
- system prompts can be templated and injected with runtime values
- enables dynamic agent behavior based on context
---
# 10 lifecycle hooks
- attach hooks to observe or modify internal events:
    - logging
    - analytics
    - debugging
- possible hook points:
    - before/after tool call
    - before/after output generation
- `RunResult` includes structured data:
    - actions, inputs, parsed outputs
    - utility methods like `.to_input_list()`
- use `output_type` to enforce structured responses (e.g. JSON) and auto-parse results
---
# 11 orchestration patterns
- **via llm (autonomous)**:
    - single agent uses tools and handoffs to decompose tasks
    - best practices:
        - write clear, example-rich prompts
        - trace execution steps
        - use sub-agents for specialization
        - allow agent reflection and self-evaluation
- **via code (deterministic)**:
    - orchestrate with plain Python
    - sequence or parallelize tasks with `asyncio.gather`
    - combine explicit logic with agent autonomy
---
# 12 installation & setup
- install:
    `pip install openai-agents`
- configure:
    - set API key:
        `set_default_openai_key("sk-...")`
    - for custom endpoints:
        use `set_default_openai_client()` with `AsyncOpenAI`
---
# 13 tracing and model selection
- per-agent model config via model settings
- each run automatically logs:
    - `AgentSpanData`
    - `GenerationSpanData`
    - `FunctionSpanData`
    - `HandoffSpanData`
- disable tracing with:
    `set_tracing_disabled(True)`
---
# 14 best practices
- use multiple small agents/tools instead of one large agent
- give clear, specific instructions with examples
- parallelize independent tasks where possible (via `asyncio.gather`)