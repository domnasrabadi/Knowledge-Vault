---
type: article
status: raw
quality:
topics: [context-engineering, agent-harnesses]
source: https://earendil.com/posts/pi-autoresearch-and-databricks/
created: 2026-08-09
published: 2026-08-04
author: Earendil
flashcards: none
updated: 2026-08-17
---

# Pi, the Minimal Coding Harness

<div align="center">
  <img src="https://earendil.com/static/og/posts/pi-autoresearch-and-databricks.png" width="220" />
</div>

- AI has made code cheap, and as a result many companies are building bigger tools in pursuit of better performance.
    - Larger prompts, more orchestration, more layers, more complexity.
    - This also makes these tools intrinsically more expensive to use.
    - Pi takes the opposite approach.
- Pi is the coding harness that chooses minimalism on purpose. It comes out of the box with only 4 tools, and its [system prompt](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/system-prompt.ts#L121-L159) and tool definitions come in below 1,000 tokens. The idea being that most work can be done with the basics, and if you want more, build it.

### Case Studies


#### Databricks Study: Cost Per Task

- In their words, “...the harness a model is called from dramatically impacts cost and quality,” and, “in many cases, simple harnesses like Pi performed best on our workloads.”

##### Minimal harness, measurable effect

- Pi shines because it doesn’t try to wrap the model in a bunch of defaults and instructions that get lost in the [instruction hierarchy](https://openai.com/index/the-instruction-hierarchy/).

#### Extensible Beats Bloat

- David Cortés describes building `pi-autoresearch` directly as a Pi extension, by simply asking “Pi, [to] create an extension for Autoresearch...”. Pi reads its own extension documentation and starts building a new workflow from there.
- The important point here is that Pi doesn’t ship any of these tools out of the box. Instead, it makes it ridiculously simple for you to build them.

### Why minimal wins now

- About a year ago, an argument could be made for native harnesses having a structural advantage over all others, because models were built around them. However, this argument has gotten weaker.
- [Anthropic recently cutting down Claude Code’s system prompt by 80%](https://x.com/petergyang/status/2078895219534438556?s=20) is a clear sign of this. So the question is becoming less about how native the harness is, and more about how it handles context to avoid redundancy and act with clean primitives.
