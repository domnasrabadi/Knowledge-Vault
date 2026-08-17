---
type: article
status: raw
quality:
topics: [ai-tooling, ai-agents, agent-harnesses]
source: https://theoryvc.com/blog-posts/getting-over-your-skills-issues
created: 2026-08-08
published: 2026-06-17
author: Bryan Bischof
flashcards: none
updated: 2026-08-17
---

# Getting Over Your Skills Issues

<div align="center">
  <img src="https://cdn.prod.website-files.com/6830b8f4d130be6b15dc8f30/6a32b2be72d9ed38a5835f6b_Screenshot%202026-06-17%20at%209.42.57%E2%80%AFAM.png" width="220" />
</div>


### Skills are software whether you like it or not.

- a skill is a reusable context package for recurring work – instructions, examples, preferences, and sometimes files or scripts that tell an AI how something should be done
- Once you've nailed down how an agent can perform a repeatable workflow, you want to minimize the variance in the steps that matter:
  - the format it follows
  - the checklist it runs
  - the preferences it respects
  - the edge cases it handles.
- The catch is that a skill almost never stays a markdown file.
  - The moment it gets shared, starts calling your tools, and becomes part of how a team works, it quietly turns into software – something with owners, versions, dependencies, and the governance questions that come with them
- Spreadsheets complexified to capture and store business logic that colleagues needed to execute their tasks; skills are complexifying for the same reason but for agent colleagues.
  - Spreadsheets became such an explicit representation of the work that needed to be done, that ability to use them was a firm job requirement across many industries and titles.

### The skill complexity matrix

- The first axis is capability: what a skill is actually able to do.
  - The simplest version of a skill is really just a prompt: a block of instructions and context that shapes how the model answers, without reaching outside the conversation.
  - But the value of a skill lies in what it is allowed to reach.
  - Does it have access to files (upload/local/cloud access), and can it write them as well as read them?
  - Can it run code on your machine or a cloud machine?
  - Can it call an external API or query a database?
  - Can it make authorized requests to some system?
  - Every yes widens what the skill can do, and what's necessary to make it work
- The second axis is distribution: how far a skill travels, how many hands shape it, and what it costs to change once it has

![](https://cdn.prod.website-files.com/6830b8f4d130be6b15dc8f30/6a32b181613e38e6884c13e6_The%20Skill%20Complexity%20Matrix.png)

- The farther a skill moves along either axis, the more valuable it can become.
  - The farther it moves along either axis, the more coordination, maintenance, and governance it requires.
- Skills are not just better prompts, they are a new place to encode how work should be done.
  - They're exciting because they let the people closest to the work shape the agent's behavior directly.
  - As skills become shared, connected to tools, and embedded in workflows, they also become infrastructure.
  - The challenge is to let them mature without losing the reason they worked in the first place
