---
type: article
status: raw
quality: 1
topics: [ai-agents, agent-evaluation]
source: ""
created: 2025-11-28
published:
author: anthropic.com
flashcards: none
updated: 2026-01-04
---

# Writing effective tools for agents — with agents

<div align="center">
  <img src="https://cdn.sanity.io/images/4zrzovbb/website/91df4759f1037fb6073de772278cb71e6e4ee37d-2400x1260.png" width="220" />
</div>

Source: https://www.anthropic.com/engineering/writing-tools-for-agents
Exported at: `2025-12-29T04:28:29Z`


### What is a tool?
- traditional software = like a contract within deterministic systems
- tools for agents = new kind of software, contract between deterministic systems + non-deterministic agents
	- goal of tools = increase surface area for agent's effectiveness by being able to solve wide range of tasks w tools
- how to write tools 
	- stand up quick prototype + test them locally 
	- run comprehensive evals to measure subsequent changes 
- building prototypes 
	- use AI to help write tools
		- give Claude Code documentation for any libraries, APIs, SDKs
		- use agents to analyse eval results + data 
		- use agents to create prompt/response pairs grounded in realistic data sources + usage
	- test tools yourself to identify rough edges or failure modes
	- collect feedback from users to build intuition around use-case + prompts you expect your tools to enable 
- running an evaluation 
	- start w generating lots of eval tasks grounded in real-world usage
		- good eval tasks may need few to dozens of tool calls 
	- each eval prompt needs to be paired w verifiable response/outcome
		- verifier can be simple as exact-match comparisons (ground-truth vs sampled responses)
		- or using LLM-as-judge
		- avoid over-strict verifiers that reject correct responses e.g. spurrious differences, formatting, punctuation, valid alternate phrasings
	- each prompt-response pair also needs the tools you expect agent to use to solve the task
		- ideally, agent need to grasp each tool's purpose during eval
		- but there could be >1 way to solve the task → don't overfit/be too strict 
	- run evals programatically w direct LLM API calls
		- use simple while loops 
		- each agent should be given a single task prompt + the tools 
		- ask agents to output reasoning + feedback loops BEFORE tool calls + responses (COT)
	- collect other metrics 
		- total runtime of individual tool calls + tasks
		- total number of tool calls
		- total token consumption
		- tool errors 
	- agents can help spot issues + provide feedback
		- e.g. contradictory tool descriptions, confusing tool schemas, inefficient tool implementations 
	- what to review
		- read agent reasoning/feedback/COT 
			- helps identify rough edges
		- read raw transcripts (tool calls + tool responses + final responses)
			- to catch any behaviour not explicitly described in agent COT 
			- read between lines → eval agents may not necessarily know correct answers + strategies 


- recommend collecting other metrics like the total runtime of individual tool calls and tasks, the total number of tool calls, the total token consumption, and tool errors.
- Agents are your helpful partners in spotting issues and providing feedback on everything from contradictory tool descriptions to inefficient tool implementations and confusing tool schemas.
- Read through your evaluation agents’ reasoning and feedback (or CoT) to identify rough edges. Review the raw transcripts (including tool calls and tool responses) to catch any behavior not explicitly described in the agent’s CoT. Read between the lines; remember that your evaluation agents don’t necessarily know the correct answers and strategies.
- Analyze your tool calling metrics. Lots of redundant tool calls might suggest some rightsizing of pagination or token limit parameters is warranted; lots of tool errors for invalid parameters might suggest tools could use clearer descriptions or better examples.
- You can even let agents analyze your results and improve your tools for you. Simply concatenate the transcripts from your evaluation agents and paste them into Claude Code.

### Principles for writing effective tools


#### Choosing the right tools for agents

- LLM agents have limited "context" (that is, there are limits to how much information they can process at once), whereas computer memory is cheap and abundan
- if an LLM agent uses a tool that returns ALL contacts and then has to read through each one token-by-token, it's wasting its limited context space on irrelevant informatio
- recommend building a few thoughtful tools targeting specific high-impact workflows
- Tools can consolidate functionality, handling potentially *multiple* discrete operations (or API calls) under the hood. For example, tools can enrich tool responses with related metadata or handle frequently chained, multi-step tasks in a single tool call.
- Instead of implementing a `list_users`, `list_events`, and `create_event` tools, consider implementing a `schedule_event` tool which finds availability and schedules an event.
- Make sure each tool you build has a clear, distinct purpose. Tools should enable agents to subdivide and solve tasks in much the same way that a human would

#### Namespacing your tools

- Namespacing (grouping related tools under common prefixes) can help delineate boundaries between lots of tools;
- We have found selecting between prefix- and suffix-based namespacing to have non-trivial effects on our tool-use evaluations.
- Agents might call the wrong tools, call the right tools with the wrong parameters, call too few tools, or process tool responses incorrectly. By selectively implementing tools whose names reflect natural subdivisions of tasks, you simultaneously reduce the number of tools and tool descriptions loaded into the agent’s context and offload agentic computation from the agent’s context back into the tool calls themselves. This reduces an agent’s overall risk of making mistakes.

#### Returning meaningful context from your tools

- tool implementations should take care to return only high signal information back to agents.
- In some instances, agents may require the flexibility to interact with both natural language and technical identifiers outputs, if only to trigger downstream tool calls (for example, `search_user(name=’jane’)` → `send_message(id=12345)`). You can enable both by exposing a simple `response_format` enum parameter in your tool, allowing your agent to control whether tools return `“concise”` or `“detailed”` responses (images below).
- You can add more formats for even greater flexibility, similar to GraphQL where you can choose exactly which pieces of information you want to receive. Here is an example ResponseFormat enum to control tool response verbosity: enum ResponseFormat { DETAILED = "detailed", CONCISE = "concise" }

#### Optimizing tool responses for token efficiency

- Optimizing the quality of context is important. But so is optimizing the *quantity* of context returned back to agents in tool responses.
- suggest implementing some combination of pagination, range selection, filtering, and/or truncation with sensible default parameter values for any tool responses that could use up lots of context.
- Here’s an example of an unhelpful error response: 

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F2445187904704fec8c50af0b950e310ba743fac2-1920x733.png&w=3840&q=75)

- This image depicts an example of an unhelpful tool response. Here’s an example of a helpful error response: 
 
![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F810661bd44a35fb273806ae95160040155978c3e-1920x850.png&w=3840&q=75)

#### Prompt-engineering your tool descriptions

- one of the most effective methods for improving tools: prompt-engineering your tool descriptions and specs.
- When writing tool descriptions and specs, think of how you would describe your tool to a new hire on your team. Consider the context that you might implicitly bring—specialized query formats, definitions of niche terminology, relationships between underlying resources—and make it explicit.
- refinements to tool descriptions can yield dramatic improvements.
