---
type: article
status: inbox
quality: 3
topics: []
source: https://addyosmani.com/blog/intent-debt/
created: 2026-08-08
published: 2026-06-05
author: Addy Osmani
flashcards: none
updated: 2026-08-08
---

# The Intent Debt

<div align="center">
  <img src="https://addyosmani.com/assets/images/intentdebt.jpg" width="220" />
</div>

- Technical debt lives in your code. Cognitive debt lives in your head. Intent debt lives in the artifacts you may have never wrote: the goals, constraints, and rationale for why the system is the way it is.
- **Technical debt lives in the code.** It’s the accumulation of implementation choices that make the system harder to change later
- **Cognitive debt lives in people.** It’s the erosion of shared understanding, the gap between how much code exists and how much any human understands. I’ve been calling this comprehension debt. It builds up when the system grows faster than the team’s mental model of it
- **Intent debt lives in artifacts.** It’s the absence or erosion of the *externalized* rationale, goals, and constraints that explain why the system is the way it is. The key word is externalized. The rationale has to be written down where a teammate, a future you, or an agent can read it, not held in your head. When intent debt runs high, the system drifts from what you meant it to do, and nobody can say when it diverged or why.
- These three are independent, which took me a while to internalize. You can have low technical debt and high intent debt. You can understand a system completely yourself (no cognitive debt for you) while its intent exists nowhere outside your skull (enormous intent debt for everyone else).
- AI generates code faster than ever, which makes technical debt cheaper to take on and cheaper to pay down. Point an agent at a tangled module and it’ll refactor it.
- Cognitive debt recovers too, more easily than most engineers expect. When you don’t understand a chunk of the system, you ask the agent to explain i
- Intent is different. **An agent can’t generate intent, because intent is the one input that has to come from you.** A model can infer a plausible rationale from the code, the same way you can guess why a previous engineer did something

### Agents make the un-written cost compound much faster

- **An agent starts most sessions cold.** It carries none of the tacit intent your humans built up over years. Whatever you haven’t externalized into an artifact it can read, it doesn’t have.

### The other half of the comprehension debt argument

- I argued that detailed specs aren’t a complete answer. Translating a spec into working code involves a huge number of implicit decisions no spec ever captures, and a spec detailed enough to *be* the program is the program in a slower language
- Being unable to capture *all* intent is no license to capture *none* of it. The implicit decisions an agent now makes on your behalf, the ones a spec will never enumerate, are the decisions whose rationale evaporates if you don’t record at least the load-bearing ones. You can’t write down everything.
- You do have to write down the *why* behind the choices that would be expensive to get wrong, because nobody will reconstruct those later.

### What high intent debt looks like

- shows up as a particular kind of helplessness.
- An agent “fixes” a bug by deleting a guard clause,
- A refactor changes a behavior users depend on
- You ask why two services talk over a queue instead of a direct call, and the honest answer is “an agent suggested it and it seemed fine.”

### Paying it down: externalize intent as a first-class artifact

- Almost everything I’ve been writing about for the last few months turns out to be intent-debt management. I didn’t have the word for it. The move is the same each time: **take the intent out of your head and put it somewhere an agent can read.**
- **Write the spec for the intent, not the implementation.** A [good spec](https://addyosmani.com/blog/good-spec/) captures the goals, the constraints, the non-negotiables, and an explicit definition of *done* (fast, accessible, secure, delightful, beyond “functionally correct”). The spec carries the intent the code can’t carry on its own.
- **Treat AGENTS.md as your intent ledger, not your config.** It’s why I keep saying [stop using /init](https://addyosmani.com/blog/agents-md/). An auto-generated file describes what the code is. An intent file describes what the team means: the conventions, the “we don’t do it this way because,” the constraints invisible in any single file. Agents can’t infer that, and they need it most.
- **Capture decisions where they happen.** Lightweight [decision logs](https://addyosmani.com/blog/automated-decision-logs/) (ADRs) are pure intent-debt paydown. Recording *why* at the moment you decide costs almost nothing. Reconstructing it eight months later, after the person who knew has moved teams, costs a fortune. Agents have made logging cheaper than ever, so the old excuse is gone.
- **Make the learning loop write intent back down.** I’ve argued for [self-improving agents](https://addyosmani.com/blog/self-improving-agents/) that update a learnings file at the end of a session. The same loop is an intent-debt pump running in reverse: every mistake whose root cause you record, every “we tried X and it didn’t work because Y” is intent that would otherwise have lived only in your memory of a bad afternoon.
- AI made code cheap, and comprehension is recoverable. Intent, the goals and constraints and reasons, is the one input that still has to originate with a human
