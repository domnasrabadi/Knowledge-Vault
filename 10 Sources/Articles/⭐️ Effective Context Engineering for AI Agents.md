---
type: article
status: raw
quality: 1
topics: [context-engineering, ai-agents]
source: ""
created: 2025-11-28
published: 2025-09-29
author: anthropic.com
flashcards: none
updated: 2026-01-01
---

# Effective context engineering for AI agents

<div align="center">
  <img src="https://cdn.sanity.io/images/4zrzovbb/website/ea2bf01aa874d7ab776453e97dfeed5d2bf5a116-2400x1260.png" width="220" />
</div>

Source: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Exported at: `2025-12-29T04:28:24Z`

- Building with language models is becoming less about finding the right words and phrases for your prompts, and more about answering the broader question of “what configuration of context is most likely to generate our model’s desired behavior?"
- **Context** refers to the set of tokens included when sampling from a large-language model (LLM). The **engineering** problem at hand is optimizing the utility of those tokens against the inherent constraints of LLMs in order to consistently achieve a desired outcome.
- Prompt engineering refers to methods for writing and organizing LLM instructions for optimal outcomes
- **Context engineering** refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompt
- as we move towards engineering more capable agents that operate over multiple turns of inference and longer time horizons, we need strategies for managing the entire context state
- An agent running in a loop generates more and more data that *could* be relevant for the next turn of inference, and this information must be cyclically refined.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Ffaa261102e46c7f090a2402a49000ffae18c5dd6-2292x1290.png&w=3840&q=75)

- LLMs, like humans, lose focus or experience confusion at a certain point.
- [context rot](https://research.trychroma.com/context-rot): as the number of tokens in the context window increases, the model’s ability to accurately recall information from that context decreases.
- , therefore, must be treated as a finite resource with diminishing marginal returns. Like humans, who have [limited working memory capacity](https://journals.sagepub.com/doi/abs/10.1177/0963721409359277), LLMs have an “attention budget” that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM.
- This attention scarcity stems from architectural constraints of LLMs. LLMs are based on the [transformer architecture](https://arxiv.org/abs/1706.03762), which enables every token to [attend to every other token](https://huggingface.co/blog/Esmail-AGumaan/attention-is-all-you-need) across the entire context. This results in n² pairwise relationships for n tokens. As its context length increases, a model's ability to capture these pairwise relationships gets stretched thin, creating a natural tension between context size and attention focus.

### The anatomy of effective context

- Given that LLMs are constrained by a finite attention budget, *good* context engineering means finding the *smallest* *possible* set of high-signal tokens that maximize the likelihood of some desired outcome.
- **System prompts** should be extremely clear and use simple, direct language that presents ideas at the *right altitude* for the agent. The right altitude is the Goldilocks zone between two common failure modes.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F0442fe138158e84ffce92bed1624dd09f37ac46f-2292x1288.png&w=3840&q=75)

- We recommend organizing prompts into distinct sections (like `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`, etc) and using techniques like XML tagging or Markdown headers to delineate these sections, although the exact formatting of prompts is likely becoming less important as models become more capable.
- to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing.
- tools define the contract between agents and their information/action space, it’s extremely important that tools promote efficiency, both by returning information that is token efficient and by encouraging efficient agent behaviors.
- tools should be self-contained, robust to error, and extremely clear with respect to their intended use. Input parameters should similarly be descriptive, unambiguous, and play to the inherent strengths of the model.
- we recommend working to curate a set of diverse, canonical examples that effectively portray the expected behavior of the agent. For an LLM, examples are the “pictures” worth a thousand words.

### Context retrieval and agentic search

- Today, many AI-native applications employ some form of embedding-based pre-inference time retrieval to surface important context for the agent to reason over. As the field transitions to more agentic approaches, we increasingly see teams augmenting these retrieval systems with “just in time” context strategies.
- Rather than pre-processing all relevant data up front, agents built with the “just in time” approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools.
- model can write targeted queries, store results, and leverage Bash commands like head and tail to analyze large volumes of data without ever loading the full data objects into context. This approach mirrors human cognition: we generally don’t memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand.
- Folder hierarchies, naming conventions, and timestamps all provide important signals that help both humans and agents understand how and when to utilize information.
- allows agents to incrementally discover relevant context through exploration. Each interaction yields context that informs the next decision: file sizes suggest complexity; naming conventions hint at purpose; timestamps can be a proxy for relevance. Agents can assemble understanding layer by layer, maintaining only what's necessary in working memory and leveraging note-taking strategies for additional persistence
- agents to incrementally discover relevant context through exploration.
- Each interaction yields context that informs the next decision: file sizes suggest complexity; naming conventions hint at purpose; timestamps can be a proxy for relevance.
- note-taking strategies for additional persistence.
- Not only that, but opinionated and thoughtful engineering is required to ensure that an LLM has the right tools and heuristics for effectively navigating its information landscape. Without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information.
- opinionated and thoughtful engineering is required to ensure that an LLM has the right tools and heuristics for effectively navigating its information landscape. Without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information.
- Claude Code is an agent that employs this hybrid model: [CLAUDE.md](http://claude.md) files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time
- Claude Code is an agent that employs this hybrid model: [CLAUDE.md](http://claude.md) files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees
- Given the rapid pace of progress in the field, "do the simplest thing that works" will likely remain our best advice for teams building agents on top of Claude.

#### Context engineering for long-horizon tasks

- Context engineering for long-horizon tasks Long-horizon tasks require agents to maintain coherence, context, and goal-directed behavior over sequences of actions where the token count exceeds the LLM’s context window.
- Long-horizon tasks require agents to maintain coherence, context, and goal-directed behavior over sequences of actions where the token count exceeds the LLM’s context window
- Waiting for larger context windows might seem like an obvious tactic. But it's likely that for the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns
- we've developed a few techniques that address these context pollution constraints directly: compaction, structured note-taking, and multi-agent architectures.
- Compaction
- Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary. Compaction typically serves as the first lever in context engineering to drive better long-term coherence. At its core, compaction distills the contents of a context window in a high-fidelity manner, enabling the agent to continue with minimal performance degradation.
- art of compaction lies in the selection of what to keep versus what to discard, as overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later
- Start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace, then iterate to improve precision by eliminating superfluous content.
- example of low-hanging superfluous content is clearing tool calls and results
- Structured note-taking
- Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes persisted to memory outside of the context window. These notes get pulled back into the context window at later times. This strategy provides persistent memory with minimal overhead. Like Claude Code creating a to-do list, or your custom agent maintaining a NOTES.md file, this simple pattern allows the agent to track progress across complex tasks, maintaining critical context and dependencies that would otherwise be lost across dozens of tool calls.
- Sub-agent architectures
- Sub-agent architectures provide another way around context limitations. Rather than one agent attempting to maintain state across an entire project, specialized sub-agents can handle focused tasks with clean context windows. The main agent coordinates with a high-level plan while subagents perform deep technical work or use tools to find relevant information. Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens).
- This approach achieves a clear separation of concerns—the detailed search context remains isolated within sub-agents, while the lead agent focuses on synthesizing and analyzing the results. This pattern, discussed in [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), showed a substantial improvement over single-agent systems on complex research tasks
- The choice between these approaches depends on task characteristics. For example: • Compaction maintains conversational flow for tasks requiring extensive back-and-forth; • Note-taking excels for iterative development with clear milestones; • Multi-agent architectures handle complex research and analysis where parallel exploration pays dividends.

### Conclusion

- Context engineering represents a fundamental shift in how we build with LLMs. As models become more capable, the challenge isn't just crafting the perfect prompt—it's thoughtfully curating what information enters the model's limited attention budget at each step
- guiding principle remains the same: find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome.
