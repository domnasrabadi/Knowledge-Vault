---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/googlecloudtech/status/2090248297214525569/?s=12&rw_tt_thread=True
created: 2026-08-22
published: 2026-08-20
author: Google Cloud Tech
flashcards: none
updated: 2026-08-22
---

# 5 design patterns for long-horizon agent harness

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2047008659629391872/BfLTYOuh.jpg" width="220" />
</div>

- "Long horizon" means the agent keeps going across days and dozens of sessions instead of answering once and forgetting you
- A one-shot agent breaks in front of you and stops. A long-horizon agent breaks quietly, hides the problem, and keeps running
- You need five design patterns that stop an agent from silently drifting off the rails.

### Pattern 1: Stable prefix

- Prefix caching is supposed to be an easy win: keep the front of your prompt identical, and the provider serves it from cache at a fraction of the cost and latency. We turned it on, and our cache hit rate stayed at 0%.
- The problem was our memory preloader. Every turn, it fetched past conversations and injected them right into the system prompt at the top. Because recalled memories change every turn, the prefix hash changed every turn. The cache never formed.
- To fix it, we sorted the prompt by how fast each piece changes:
    - **Frozen (top):** System instructions, persona, and tool definitions. Byte-identical across every turn.
    - **Slow (middle):** User profile and active tools.
    - **Volatile (tail):** Step counters, runtime warnings, and recalled memories.

![](https://pbs.twimg.com/media/HQIMK4kXwAATfnq.jpg)

- Moving dynamic memories to the tail was the entire fix. Turn one warms the cache; every turn after serves 95% of the prompt from it.

### Pattern 2: Background learning

- An agent that learns over time has to extract memories and write them down. At first, we did this inline, right before replying. Every turn slowed down to extract memories the user wouldn't need until next week.
- The fix is write-behind caching: send the reply to the user first, then run memory extraction in the background under the same user identity so the writes land where the next turn will find them

![](https://pbs.twimg.com/media/HQIMUeUXkAAGrAS.jpg)

- To make this safe in production, you need three safeguards: 1. **Hold a strong task reference.** In async runtimes like Python's asyncio, an unreferenced background task can get garbage-collected mid-write, silently losing data without throwing an error. 2. **Use an isolated sibling agent.** Give the background learner a minimal tool list, restrict its file writes to the memory directory, and give it no post-response hooks of its own so it cannot accidentally recurse. 3. **Throttle runs.** Wait 120 seconds between background consolidation passes so a burst of quick user messages doesn't trigger dozens of redundant extraction runs.

### Pattern 3: Persistent workspace

- Hours or days pass between messages from the same user. When the agent wakes back up, everything it built in the meantime has to still be there.
- Standard web code assumes stateless request handlers. A long-horizon agent is a long-lived process that the same user keeps returning to.
- Files, installed tools, and half-finished work must outlive the individual turn. Tool calls should go through an execution interface that owns that state rather than executing against the host directly

![](https://pbs.twimg.com/media/HQIMhbAXYAAlaE6.jpg)

- Scope it to the user, not the conversation, keep it warm, and let later messages reattach. Keep reattachment version-agnostic so a new backend doesn't wipe yesterday's tools.

### Pattern 4: Explicit failure

- When one agent's output becomes another agent's input, the parent decides whether the child succeeded based on the shape of the return envelope.
- Don't rely on conventions or empty strings. Give every terminal state a name and make the parent branch on it. Ours has four: completed, timeout, halted for a step limit or crash, and pending for a child waiting on a human.
- The companion problem is a loop that runs forever while looking productive

### Pattern 5: Guard chain

- An agent with shell access can reach anything the machine can reach, including the cloud provider's metadata endpoint and the credentials it serves.
- We blocked 169.254.169.254 by string matching. Then curl http://2852039166/ walked straight past the filter, because that integer resolves to the exact same IP address.
- Evaluate guards like a short-circuit expression: run cheap, deterministic checks first, and escalate to expensive ones only when necessary.
- Our chain uses three stages:
    - **Exfiltration guard.** Blocks dangerous destinations like metadata IP addresses outright. No session setting can loosen this.
    - **Policy guard.** Returns allow, ask, or deny based on declarative rule sets.
    - **Interactive prompt.** Asks the user, last, because a human's attention is the most expensive thing you can spend.
- A guard that asks about everything teaches people to approve without reading. To relax common commands safely, parse the command and resolve the underlying binary rather than substring matching raw text.

### What to take away

- Making an agent survive over weeks isn't about building a massive framework. It's about catching the silent failures before they burn your budget or corrupt your state.
