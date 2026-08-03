---
type: article
status: structured
quality:
topics: [ai-agents, agent-frameworks]
source: ""
created: 2025-06-15
published:
author: ""
flashcards: none
updated: 2025-12-28
---
> [!NOTE] The source for this note is from a DeepResearch report I requested to compare each of the major Agentic frameworks 
> It covers a brief analysis of each, and then compares them along several dimensions. It's useful since there are many agent frameworks emerging and each has it's own use-case. 


# 1 frameworks
## 1.1 openai agents sdk (`openai-agents`)
- lightweight, Python-first framework with minimal abstractions
- `Agent` = pairs an LLM with a prompt and optional tools
- tool integration:
    - any Python function can become a tool
    - SDK auto-generates:
        - `name`
        - `description` (from docstring)
        - `input schema` (using type hints + Pydantic)
- maintains conversational context in prompt
    - short-term memory handled automatically
    - developers can inject or clear context via API
    - advanced memory must be user-implemented
- interactions use normal Python control flow
    - no rigid framework classes
    - easy to start with defaults
    - production-suitable via custom logic
    - developer responsible for state persistence and planning
    - complex workflows require more manual orchestration
**strengths**
- simple API, easy to learn
- seamless Python function to tool conversion
- flexible, Python-native approach
**weaknesses**
- lacks higher-level features (e.g. multi-agent orchestration, memory modules)
- no built-in multi-agent structure — handled manually
---
## 1.2 `langgraph` (langchain’s langgraph)
- agent orchestration using graphs instead of linear flows
    - nodes = functions/steps
    - edges = define information flow
    - shared agent state (context) across all nodes
- supports advanced structures:
    - cycles, branches, parallel subgraphs
    - low-level primitives + high-level templates (e.g. prebuilt ReAct graph)
- tool integration:
    - supports LangChain tools
    - tools defined via Python callables with docstrings
- memory:
    - stateless by default
    - built-in short-term + long-term memory via `langmem` module
- supports multi-agent setups via:
    - composed subgraphs
    - supervisor agents (`langgraph-supervisor`) for hierarchical control
    - human-in-the-loop nodes for manual approvals
- production-ready, integrates with LangChain connectors
- excels in complex, reliable decision workflows
**strengths**
- granular control over agent logic
- built-in memory, human oversight
- strong tool ecosystem via LangChain
**weaknesses**
- steeper learning curve
- more boilerplate to define graphs
- additional packages required (e.g. `langgraph-swarm`, `langmem`)
- tightly coupled with LangChain (potential vendor lock-in)
---
## 1.3 hugging face smolagents
- minimalist agent framework (~1000 lines of code)
- code-based action = agents generate + execute Python code
    - `CodeAgent` writes logic directly as code
- setup:
    - define tools via `@tool` decorator or subclass `ToolBase`
    - LLM generates code using these tools
    - call `agent.run(prompt)` to execute
- tool sharing via Hugging Face Hub
- can integrate LangChain tools
- memory:
    - simple memory support across steps
    - no built-in vector store for long-term memory
- sandboxed code execution (e.g. E2B, Docker)
- model-agnostic via LiteLLM
- ideal for rapid prototyping and education
**strengths**
- minimal setup, easy to use
- code-based reasoning enables complex logic
- strong sandboxing for safety
- flexible with models and external tools
- community-friendly via tool sharing
**weaknesses**
- lacks multi-agent coordination out of the box
- debugging involves reading generated code
- limited built-in features (e.g. planning, vector memory)
---
## 1.4 crewai
- multi-agent collaboration framework
- main abstractions:
    - **agent** = role-specific unit with tools, goals, and optional persona
    - **crew** = collection of agents working on a task
    - **process** = structured workflow for the crew
    - **task** = unit of work handled by one agent
- agents communicate via:
    - manager-led or peer-to-peer models
    - messaging system under the hood
- tools = defined via `BaseTool` subclass or Python callables
    - supports OpenAI function calling
    - communication can be a tool
- memory:
    - per-agent memory
    - crew-level shared memory (conversation transcript)
    - external knowledge sources (e.g. vector DBs)
- multi-agent patterns supported:
    - round-robin chat
    - manager-worker task delegation
    - conditional or sequential workflows
    - human-in-the-loop interaction
- designed for enterprise use — efficient, no LangChain dependency
**strengths**
- built-in multi-agent coordination
- intuitive role-based structure
- efficient and production-friendly
**weaknesses**
- not explicitly listed but may involve more setup for non-multi-agent tasks
---
## 1.5 microsoft autogen
- open-source multi-agent framework with layered architecture
    - **core api**: message passing, event loop, runtime
    - **agentchat api**: high-level multi-agent constructs
    - **extensions**: add capabilities (web, code execution, external APIs)
- core agent = `ConversableAgent`
    - `receive()` method handles incoming messages
    - agent types:
        - `AssistantAgent` = LLM-powered responder
        - `UserProxyAgent` = simulates human or bridges human input
- supports:
    - `GroupChat`, `RoundRobinGroupChat`, `Team`
    - termination conditions for stopping interactions
- tools = often modeled as specialized agents (e.g. browser, executor)
- memory:
    - per-agent history of messages
- ideal for:
    - emergent behavior
    - collaborative problem solving
    - debate, committee, knowledge base building
- still a research project (v0.4 as of early 2025)
**strengths**
- strong multi-agent scaffolding
- supports delegation and team structures
- cross-language support (Python + .NET)
**weaknesses**
- multi-agent complexity requires careful design
- as research software, may lack polish or stable APIs
---
## 1.6 microsoft semantic kernel
- AI orchestration framework integrating AI into apps
- main components:
    - **kernel** = central engine managing models, skills, memory
    - **skill/plugin** = functions the AI can use
        - semantic functions = prompt templates
        - native functions = code/API calls
    - **planner** = LLM chooses which skills to execute for a goal
    - **context** = holds variables, history, and functions (passed through calls)
- tool support:
    - plugins can be:
        - semantic (text)
        - OpenAPI-generated
- memory:
    - **semantic memory** = embedding-based long-term memory
    - supports vector DBs (Azure, Elastic, Chroma, etc.)
- multi-agent supported via Process Framework
- model-agnostic (OpenAI, Azure, HF, NVIDIA)
- enterprise-ready: secure, observable, maintainable
**strengths**
- robust tool/plugin system
- built-in memory integration
- flexible function calling
- enterprise alignment
**weaknesses**
- developer effort needed to define skills/plugins
- broad framework — requires understanding of components
---
# 2 comparative analysis
## 2.1 ease of use & learning curve
- **openai sdk** = easiest to start; more Python logic for complex flows
- **smolagents** = extremely simple; ideal for fast prototyping
- **langgraph** = steeper due to graph abstraction + multiple packages
- **crewai** = balanced; intuitive role/task model
- **autogen** = moderate; easy basics, but complex customization
- **semantic kernel** = requires learning core concepts; feels natural for developers
## 2.2 flexibility & extensibility
- **openai sdk** = interleaves Python logic easily; few built-ins
- **langgraph** = highly customizable, supports advanced flows
- **smolagents** = flexible through code generation; LLM does complex logic
- **crewai** = flexible multi-agent coordination with prebuilt patterns
- **autogen** = layered; can drop to core API if needed
- **semantic kernel** = plugin-based, supports various workflows
## 2.3 llm / provider support
- **openai sdk** = openai + liteLLM for others
- **langgraph** = inherits langchain’s wide model support
- **smolagents** = model-agnostic via liteLLM
- **crewai** = openai + others via plugin interface
- **autogen** = openai-centric but extensible
- **semantic kernel** = supports openai, azure, hugging face, nvidia
## 2.4 safety & guardrails
- **openai sdk** = input/output guardrails included
- **langgraph** = hooks + human-in-loop nodes; no built-in filters
- **smolagents** = sandboxed execution; filtering external
- **crewai** = patterns for compliance + human input
- **autogen** = relies on prompts and external checks
- **semantic kernel** = supports secure plugin usage; moderation must be added
## 2.5 tool abstraction & ecosystem
- **openai sdk** = no central tools; use Python functions
- **langgraph/langchain** = largest tool ecosystem
- **smolagents** = interoperable + community tool sharing
- **crewai** = base tool + defaults (e.g. sandbox, PDF)
- **autogen** = tools as agents (e.g. browser, executor)
- **semantic kernel** = plugin/skill model with semantic + code tools
## 2.6 developer ergonomics & integration
- **openai sdk** = clean, Pythonic, easy debugging
- **langgraph/langchain** = rich features, layered complexity
- **smolagents** = readable code, simple APIs
- **crewai** = observability + production design
- **autogen** = examples available, may need source-level debugging
- **semantic kernel** = structured, maintainable, dev-friendly
## 2.7 experimentation vs production suitability
- **smolagents, openai sdk** = best for rapid prototyping
- **langgraph, autogen** = suited for complex orchestration
- **crewai** = production-ready multi-agent workflows
- **semantic kernel** = enterprise-grade, modular integration