---
type: article
status: raw
quality: 1
topics: [ai-coding, context-engineering, ai-agents]
source: https://x.com/systematicls/status/2028814227004395561/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-03-03
author: sysls
flashcards: none
updated: 2026-08-13
---

# How to Be a World-Class Agentic Engineer

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1982988371661336578/b0SV2XPc.jpg" width="220" />
</div>


## Understand That The World Is Sprinting By

- The point of this is to say that the most important principle to hold is the realization that every new generation of agents will force you to rethink what is optimal, which is why less is more.
- When you use many different libraries and harnesses, you lock yourself into a "solution" for a problem that may not exist given future generations of agents.

## Context Is Everything

- You get the idea. You want to give your agents only the exact amount of information they need to do their tasks and nothing more! The better you are in control of this, the better your agents will perform

## Do The Things That Work


### Be Precise About Implementation

- The first way to ensuring that is the case is to separate research from implementation. You want to be extremely precise about what you are asking from your agents.
- Here's what happens when you are not precise: "Go and build an auth system." The agent has to research what is an auth system? What are the available options? What are the pros and cons? Now it has to go scour the web for information it doesn't actually need, and its context is filled with implementation details across a large range of possibilities. By the time it's time to implement, you increase the chances it will get confused or hallucinate unnecessary or irrelevant details about the chosen implementation.
- Of course you won't always have the implementation details. You often won't know what's exactly right - sometimes, you might even want to relegate the job of deciding the implementation detail to the agents. In that case, what do you do? Simple - you create a research task on the various implementation possibilities, either decide it yourself or get an agent to decide on which implementation to go with, and then get another agent with a fresh context to implement.
- Once you start thinking along these lines, you will spot areas in your workflow where your agents are needlessly polluted with context that is not necessary for implementation

### The Design Limitations Of Sycophancy

- So, what do you do? I find that "neutral" prompts work, where I'm not biasing the agent towards an outcome. For example, I don't say "Find me a bug in the database", instead, I say "Search through the database, try to follow along with the logic of each component, and report back all findings."

### How Do You Know What Works Or Is Useful?

- If OpenAI and Claude both implement it or acquire something that implements it... It's probably useful.
- Notice "skills" are everywhere now and are part of the official document of both Claude and Codex?
- How about planning? Remember when a bunch of guys discovered planning before implementation was REALLY useful, and then it got turned into a core functionality?

### Compaction, Context And Assumptions

- he main difference is whether or not the agent has had to make any assumptions or "fill in the gaps". As of today, they are still atrocious at "connecting the dots", "filling in the gaps" or making assumptions
- One of the most important rules in `CLAUDE.md` is a rule on how to deal with grabbing context, and instruct your agent to read that rule the first thing whenever it reads `CLAUDE.md` (which is always after compaction). As part of the grabbing context rule, a few simple instructions that go a long way are: re-reading your task plan, and re-reading the relevant files (to the task) before continuing.

### Letting Your Agents Know How To End The Task

- Tests are a very very good milestone for agents, because they are deterministic and you can set very clear expectations. Unless these X number of tests pass, your task is NOT complete; and you are NOT allowed to edit the tests.
- You know what else has recently become a viable end-point for a task? Screenshots + verification

### Rules

- If you don't want your agent to do something, write it as a rule.
    - Then let your agent know about this rule in your `CLAUDE.md`.
    - Something like: before you code, read "`coding-rules.MD`".
    - Rules can be nested, and rules can be conditional!
    - If you are coding, read "`coding-rules.MD`", and if you are writing tests, read "`coding-test-rules.MD`". If your tests are failing, read "`coding-test-failing-rules.MD`".
    - You can create arbitrary logic branches of rules to follow, and claude (and codex) will happily follow along, provided this is clearly specified in the `CLAUDE.md`.
- In fact, this is the FIRST practical advice I'm giving: treat your `CLAUDE.md` as a logical, nested directory of where to find context given a scenario and an outcome. It should be as barebones as possible, and only contain the IF-ELSE of where to go to seek the context.
- If you see your agent doing something and you disapprove, add it as a rule, and tell the agent to read the rule before it does THAT THING again, and it will most definitely not do it anymore.

### Skills

- Skills are like rules, except rather than encoding preferences, they are better suited to encode recipes. If you have a specific way of how you want something to be done, you want to embed it into a skill.

### Dealing with Rules and Skills

- You definitely want to keep adding rules and skills to your agent. This is how you give it a personality and a memory for your preferences. Almost everything else is overkill.
- And then... You will see performance start to deteriorate again. What gives?! Easy. As you add more rules and skills, they are starting to contradict each other, or the agent is starting to have too much context bloat. If you need the agent to read 14 markdown files before it starts programming, it's going to have the same issue about having a lot of useless information. So, what do you do? You clean up. You tell your agents to go for a spa day and to consolidate rules and skills and remove contradictions by asking you for your updated preferences.
