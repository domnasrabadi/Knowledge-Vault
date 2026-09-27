---
type: article
status: raw
quality: 1
topics: [ai-agents, context-engineering, multi-agent-systems, ai-engineering]
source: https://rubriclabs.com/blog/everything-we-know-about-good-agent-design
created: 2026-09-26
published: 2026-09-16
author: Sarim Malik
flashcards: none
updated: 2026-09-27
---

# 25 Principles of Good Agent Design (Rubric Labs)

<div align="center">
  <img src="https://rubriclabs.com/blog/everything-we-know-about-good-agent-design/opengraph-image" width="220" />
</div>

### Prompts

- **1. Read your system prompts**
    - Ask yourself: if I were the agent, could I do the task from this prompt?
    - System prompts often include **static and dynamic content**.
        - Dynamic content is information added to the prompt at runtime, such as the current user's details, available tools, or the agent's environment and constraints, etc.
        - Engineers rarely read system prompts in their entirety, even though dynamically built prompts often accumulate **redundancy, contradictions and poor formatting**.
    - For really large prompts, we tend to **visualize the prompt** by assembling both the static and dynamic pieces and read through the overall prompt. This helps us understand the overall context, identify any redundancies or contradictions, and also see the formatting of the actual runtime prompt.
- **2. Keep your system prompts short**
    - Your system prompts should be short enough that your engineers can keep the whole thing in mind. On the higher end, they should be **less than 5,000 tokens** (6–8 pages of text).
    - But generally, models today don't require the long, prescriptive system prompts they did in previous generations, as they have become increasingly capable, execute for longer and stay on track.

### Models

- **3. Aggressively deprecate support for old models**
    - Agents are best co-designed with a generation of models. Supporting old models has a lowest-common-denominator effect: prompts have to be dumbed down and scoped to the level of the weakest model, which wastes the potential of the newest model.
- **4. Use a model selector only if you absolutely need to**
    - Most agents these days expose a model selector to the end user.
    - If your incentives are aligned with the user, your goal is to deliver the **most value while keeping token usage and cost low**.
        - So automatically route requests to the best possible model instead of having the user pick a specific model.
        - This can add latency, though it can be unnoticeable for most use cases.

### Tools

- **5. Design tools around use cases**
    - Identify **flagship use cases** that you want your agent to accomplish and design tools that allow your agent to fulfill those use cases.
        - For example, if you're building an agent that helps you book flights, ask yourself: what do you want your agent to accomplish? Roughly, this might include:
            - Find available flights
            - Compare fares
            - Track price changes
            - Hold a fare
            - Make a booking
            - Modify an existing booking
            - Cancel and request refunds
    - You might be tempted to design your tools to fulfill each use case with a specialized tool, whereas the better strategy is to **design a unique set of [primitives](https://rubriclabs.com/blog/primitives-over-pipelines)** that your agent can assemble dynamically to solve each use case.
- **6. Pick the smallest subset of tools**
    - After you understand your use cases, your goal is to design a **small set of really powerful tools** that allow you to fulfill all the use cases.
        - For example, **cost sensitivity** is a major driver for booking flights.
            - One agent designer might decide to create a tool called `find_cheapest_flight`, which takes a date range and recommends the cheapest itinerary in that interval.
            - Another agent designer might give autonomy to the agent and expose a single tool called `search_flights`, allowing the agent to call this tool **in parallel** multiple times and compare the prices on its own to find the cheapest fare.
            - The advantage of the latter is that it can help you find the cheapest flight, but it can also provide a primitive that can be used to fulfill other use cases such as searching for flights in general or to look up a specific flight.
- **7. Avoid overlapping capabilities across tools**
    - If you give the agent a GitHub push tool and a shell with GitHub already signed in, it has two ways to push the same change. Avoid overlapping tools so the agent has a **clear path** to execute a capability.
- **8. Don't leave agents with missing capabilities**
    - As you design your tools, if you feel there is a gap or **missing capability** that prevents the agent from fulfilling a use case, don't expect the agent to magically solve it.
        - You need to [unblock your agents](https://rubriclabs.com/blog/unblocking-agents) by putting yourself in the shoes of your agent and ask yourself, if I had access to these tools, would I be able to solve this problem? If the answer is no, you need to **rethink the tools** that you have selected.
- **9. Name tools and parameters literally**
    - Models use names and descriptions to decide what a tool does. You want to use the most **unambiguous, clear, and literal** way of explaining that tool.
        - For example, `send_sms` tells the agent precisely what the tool does, whereas `process_action` is ambiguous and confuses the model.
- **10. Let tools enforce permissions**
    - return a **clear, graceful error** when an agent calls a tool without suitable permission
- **11. Treat errors as useful feedback**
    - Tools should return **precise errors** and tell the agent what failed and why, so the agent can potentially recover and correct its course.
- **12. Distinguish between different types of errors**
    - Distinguish expected errors the agent can recover from, like a bad argument or a slug that's already taken, from unexpected failures, like a bug in the tool itself.

### Context

- **13. The agent only knows what's in its context**
    - Agents don't know what they don't know. Just because tacit knowledge exists in memory, or the answer to a database design question exists in a skill, doesn't mean the agent knows it's there if it's not discoverable.
    - Make sure hints are in context, not just technically available to the agent.
        - The agent only knows what's in its context.
        - Keep a **small index of available files, memories, and skills** in context.
- **14. Give the agent visibility into its environment**
    - Give the agent visibility into its rate limits, tool restrictions, expectations, weird gotchas, errors, what has happened, if it was recently compacted, if it was rate limited, if there was a change to a tool, if a memory got written, etc.
    - You want your agent to understand its **environment and constraints** so it can make better decisions.
- **15. Avoid compacting mid-task**
    - [Compaction](https://rubriclabs.com/blog/what-is-an-agent-harness#compaction) lobotomizes the agent if done at the wrong time. It kills momentum, so you should keep compaction to a minimum, at natural logical boundaries, not under pressure.
- **16. Allow the agent to compact on its own**
    - We've found that giving the agent [visibility into its context window](https://rubriclabs.com/blog/everything-we-know-about-good-agent-design/#14-give-the-agent-visibility-into-its-environment) and tools to manage it allows the agent to compact at **better checkpoints** than if an external service were forcing it to compact.

### Skills

- **17. Use skills for procedural knowledge**
    - you want to give the agent strong primitives (tools), and bake procedural knowledge modularly in skill files.

### Subagents

- **18. Delegate context-heavy work to subagents**
    - Spinning up subagents to take on **context-heavy work** and return their findings to the main agent is a great way to manage the context window of your primary agent.
        - For example, a user might ask your flight booking agent to recommend three completely different vacations, including flights and hotels.
            - You could **spawn three subagents** to research one itinerary each and return their findings to the core agent.
            - This could help the core agent give a higher-quality response than if it researched all three on its own.
- **19. Give subagents enough context to own a task**
    - Whereas in our experience, you want the subagent to own a larger piece of the work and give it enough context to own it end-to-end. **Onboard subagents like employees**, with objectives, priorities, project context, and success criteria.
- **20. Reuse subagents**
    - Agents tend to treat subagents ephemerally: dispatch a subagent to do a task, then another subagent to review it, then another subagent to implement the feedback. You get all these "waves" and "dead subagents."
    - Instead, dispatch subagents with **high ownership** to do entire, complete pieces of work, and give them follow-ups or feedback. They become the **owner of that scope**, and their context gets ripe.
- **21. Let one primary agent coordinate subagents**
    - In some multi-agent workflows, several agents work in parallel as peers. In our experience, we prefer **one primary agent running in a single thread** that delegates work to sub-agents and uses their findings to stay on course.

### Guardrails

- **22. Run your guardrails outside the agent's control**
    - You want to separate your guardrails from the core agent so they can run **outside the agent's control**. Run them outside the agent's container, with permissions that prevent the agent from modifying or disabling them.
- **23. Separate trusted instructions from untrusted data**
    - Clearly label which information is **untrusted data** pulled from external sources and which information includes **trusted instructions** from the user or the system.
        - For example, web search results or the contents of a file uploaded by the user may be treated as untrusted data, not as instructions.
        - The model needs clear visibility into what the trusted instructions are and what is untrusted information.
        - This allows the model to protect itself from unwanted behavior.

### Observability

- **24. Log everything**
    - Log your conversation turns, tool calls, skill retrievals, everything. This is a prerequisite to debugging.
- **25. Give your agent a tool to report its own failures**
    - Allow your agent to identify its **unexpected failure modes** and log them to your feedback tool of choice
