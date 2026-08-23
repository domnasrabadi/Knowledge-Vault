---
type: article
status: raw
quality: 
topics: [agent-harnesses, context-engineering]
source: https://www.anthropic.com/engineering/managed-agents
created: 2026-08-22
published: 2026-04-08
author: anthropic.com
flashcards: none
updated: 2026-08-23
---

# Scaling Managed Agents: Decoupling the brain from the hands

- A common thread across this work is that harnesses encode assumptions about what Claude can’t do on its own. However, those assumptions need to be frequently questioned because they can [go stale](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) as models improve.
- Building Managed Agents meant solving an old problem in computing: how to design a system for “[programs as yet unthought of](http://www.catb.org/esr/writings/taoup/html/ch03s01.html).”
- We virtualized the components of an agent:
    - a session (the append-only log of everything that happened)
    - a harness (the loop that calls Claude and routes Claude’s tool calls to the relevant infrastructure)
    - and a sandbox (an execution environment where Claude can run code and edit files)

- In the pets-vs-cattle analogy, a pet is a named, hand-tended individual you can’t afford to lose, while cattle are interchangeable.
    - In our case, the server became that pet; if a container failed, the session was lost.
    - If a container was unresponsive, we had to nurse it back to health.

### Decouple the brain from the hands

- The solution we arrived at was to decouple what we thought of as the “brain” (Claude and its harness) from both the “hands” (sandboxes and tools that perform actions) and the “session” (the log of session events). Each became an interface that made few assumptions about the others, and each could fail or be replaced independently.
- **The harness leaves the container.** Decoupling the brain from the hands meant the harness no longer lived inside the container.
    - It called the container the way it called any other tool: `execute(name, input) → string`.
    - The container became cattle. If the container died, the harness caught the failure as a tool-call error and passed it back to Claude
- **Recovering from harness failure.** The harness also became cattle.
    - Because the session log sits outside the harness, nothing in the harness needs to survive a crash.
    - When one fails, a new one can be rebooted with `wake(sessionId)`, use `getSession(id)` to get back the event log, and resume from the last event.
    - During the agent loop, the harness writes to the session with `emitEvent(id, event)` in order to keep a durable record of events.

### The session is not Claude’s context window

- Long-horizon tasks often exceed the length of Claude’s context window, and the standard ways to address this all involve irreversible decisions about what to keep
    - We’ve explored these techniques in [prior work](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) on context engineering.
        - For example, compaction lets Claude save a summary of its context window and the memory tool lets Claude write context to files, enabling learning across sessions.
        - This can be paired with context trimming, which selectively removes tokens such as old tool results or thinking blocks.
- But irreversible decisions to selectively retain or discard context can lead to failures. It is difficult to know which tokens the future turns will need
    - If messages are transformed by a compaction step, the harness removes compacted messages from Claude’s context window, and these are recoverable only if they are stored
- In Managed Agents, the session provides this same benefit, serving as a context object that lives outside Claude’s context window. But rather than be stored within the sandbox or REPL, context is durably stored in the session log
    - The interface, `getEvents()`, allows the brain to interrogate context by selecting positional slices of the event stream.
        - The interface can be used flexibly, allowing the brain to pick up from wherever it last stopped reading, rewinding a few events before a specific moment to see the lead up, or rereading context before a specific action.
    - Any fetched events can also be transformed in the harness before being passed to Claude’s context window.
        - These transformations can be whatever the harness encodes, including context organization to achieve a high prompt cache hit rate and context engineering.
        - We separated the concerns of recoverable context storage in the session and arbitrary context management in the harness because we can’t predict what specific context engineering will be required in future models.
        - The interfaces push that context management into the harness, and only guarantee that the session is durable and available for interrogation.

### Conclusion

- Managed Agents is a meta-harness in the same spirit, unopinionated about the *specific* harness that Claude will need in the future. Rather, it is a system with general interfaces that allow many different harnesses
- Meta-harness design means being opinionated about the interfaces around Claude: we expect that Claude will need the ability to manipulate state (the session) and perform computation (the sandbox).
    - We also expect that Claude will require the ability to scale to many brains and many hands.
    - We designed the interfaces so that these can be run reliably and securely over long time horizons.
    - But we make no assumptions about the number or location of brains or hands that Claude will need.
