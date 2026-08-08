---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/trq212/status/2073100352921215386/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-07-03
author: Thariq
flashcards: none
updated: 2026-08-08
---

# A Field Guide to Fable: Finding Your Unknowns

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1976939058741039104/r3GgzqRh.jpg" width="220" />
</div>

- The map, a representation of the work to be done, is my prompts and skills and context
- The territory is where the work needs to happen, the codebase, the real world, its actual constraints.
- difference between the map and the territory is what I call *unknowns*.
- Importantly, just planning ahead isn’t always enough.
- When I come to Claude with a problem I tend to break it down in 4 ways:
    - **Known Knowns:** This is essentially what is in my prompt. What do I tell the agent that I want?
    - **Known Unknowns:** What haven't I figured out yet, but I’m aware that I haven’t?
    - **Unknown Knowns:** What's so obvious I’d never write it down, but would recognize it if I saw it?
    - **Unknown Unknowns:** What haven't I considered at all? What knowledge am I not aware of? Do I know how good something can be?
- In many ways, reducing and planning for your unknowns is the **skill** of agentic coding. But luckily, this is a skill you can improve at, by working with Claude.
- Instructing Claude is a delicate balance. If you are too specific, Claude will follow your instructions even when a pivot may be more appropriate. If you are too vague, Claude will often make choices and assumptions based on industry best practices that may not be a fit for your task.
- Claude can help you discover your unknowns faster.
- most important part of this process is to give Claude context about your starting point.
- tell it where you are in your thought process; disclose your experience with the problem and codebase; and let it work with you like a thought partner.
- in almost all of these cases, a HTML artifact is the best way to visualize and represent it.

## Pre-implementation


### Blind Spot Pass

- When starting work, one of the most useful things you can do is understand your blindspots.
- You may not know what questions to ask, what good looks like, what historical work has been done or what potholes to avoid.
- To do this, you can ask Claude to help you find your unknown unknowns and explain them to you.

### Brainstorms and prototypes

- extremely valuable to identify and verbalize unknown knowns early during prototyping
- I also start almost every coding session with an exploration or brainstorming phase. This helps me start with intent to define the project’s scope.
- **Example prompts:**
    - "I want a dashboard for this data but I have no visual taste and don't know what's possible. Make me an HTML page with 4 wildly different design directions so I can react to them.”
    - “Before wiring anything up, make a single HTML file mocking the new editor toolbar with fake data. I want to react to the layout before you touch the treal app."
    - "Here's my rough problem: users churn after onboarding. Search the codebase and brainstorm 10 places we could intervene, from cheapest to most ambitious. I'll tell you which ones resonate."

### Interviews

- Once I’ve done sufficient brainstorming, I likely still have unknowns.
- I ask Claude to interview me about any unknowns or ambiguities. When asking Claude to interview you, try and give it context about your problem to guide its questions. Here are some examples. **Example prompts:**
    - "Interview me one question at a time about anything ambiguous, prioritize questions where my answer would change the architecture."

### References

- Sometimes you can’t describe what you want in detail. For example, you might not have the language or it might be so complicated that it would take you quite a while.
- While you can include diagrams, documentation or pictures, the absolute best reference is *source code*.

### Implementation Plans

- Once I am satisfied with my plan, I make a new session and pass any artifacts to the prompt.
- For example, I might pass in a spec file and a prototype and ask an agent to implement it.
- no matter how much planning you do, there are always unknown unknowns lurking.

## Post implementation


### Pitches and explainers


![](https://pbs.twimg.com/media/HMUce7UaEAAegM5.jpg)

- Building pitch and explainer artifacts in the final document helps
- Asking Claude to quiz me about the change after giving me a bunch of context helps me understand what happens. I only merge after I pass the quiz perfectly.
- **Example prompts:**
    - “I want to make sure I understand everything that's happened in this change. Give me a HTML report on the changes for me to read and understand with context, intuition, what was done, etc. and a quiz at the bottom on the changes that I must pass.”
