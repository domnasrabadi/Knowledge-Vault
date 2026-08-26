---
type: article
status: raw
quality: 
topics: [agent-harnesses, ai-agents, context-engineering]
source: https://x.com/samzliu/status/2090977607219396771/?s=12&rw_tt_thread=True
created: 2026-08-23
published: 2026-08-22
author: Sam Z Liu
flashcards: none
updated: 2026-08-27
---

# Four Problems Skills Solve for Agents

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1968757781865062400/AsKWETmb.jpg" width="220" />
</div>

### What is a skill exactly?

- This means that the boundaries between what is a skill and what is not a skill has become unclear.
- three examples that test the limits of where a skill begins and where it ends
    - [Last30days](https://github.com/mvanhorn/last30days-skill) - is a skill that keeps you updated on the comings and goings of HackerNews, Reddit, X, etc. This resembles less a traditional skill and more a mini-program that is executable by agents. Beyond markdown files, it includes code and tools for the agent to call
    - [Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/) - This is just a markdown file. However, it contains the full spec for a multi-agent orchestrator where the recommended installation pathway is to have codex build it from scratch. Here, we see that a markdown file isn't just a markdown file. Some of Andrej Karpathy's viral skills like his LLM Wiki also fall into this category. They become schelling points for a class of products, all built custom to each user
    - Plugins - They contain not just skills but also things like hooks and tools which all integrate with agent harnesses at different points
- The general definition of skills then, is that they are folders of information which help an agent perform tasks. This is intentionally vague because a skill is not a cleanly defined object

### What problems do skills actually solve?

1. **The recall vs recognition gap.**
    - There is nothing that a GUI can do that a terminal cannot, but it is hard to remember terminal commands
    - A GUI solves this problem by clearly enumerating what actions can be taken, turning a recall problem into a recognition one
2. **Consistency**
    - Skills solve this problem by providing standard SOPs in cases where there may look like there is more than one way to complete a task
    - Think of them like a pilot handbook. For critical or frequent tasks, we don't want the agent to be rediscovering things on the fly.
3. **Portable Expertise**
    - These skills solve the problem of a specific set of expertise that the user may not have
4. **Reasoning Checkpoint**
    - These are personalized skills which accumulate specific knowledge about a user over time
    - The key is that they represent a consolidation of information from both previous agent traces as well as user feedback.

### How to build good skills

- Overall, skills enable us to compound and scale agentic systems in token space. It's not enough that models are intelligent. They also need the procedural knowledge and context of how to work within a larger system
