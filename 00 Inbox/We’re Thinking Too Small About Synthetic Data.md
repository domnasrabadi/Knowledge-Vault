---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/_yuhanluo/status/2111493287085535304/?rw_tt_thread=True
created: 2026-10-31
published: 2026-10-17
author: Yuhan Luo
flashcards: none
updated: 2026-10-31
---

# We’re Thinking Too Small About Synthetic Data

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2103914695396818944/xRSBz5Ev.jpg" width="220" />
</div>


## What are we even synthesizing today?

- That means we need to build *usable* tasks and environments, along with verifiers that judge success *fairly*. Otherwise, **cheap data just ends up consuming expensive training compute with little to no learning value.**
- Take the [customer service agent training example I wrote about earlier](https://x.com/_yuhanluo/status/2104325531982528994).
- The agent’s starting world is the end state of this simulated history.
- It’s tempting to generate the tickets, emails, and refund records separately, then patch the inconsistencies afterward. For example, we might manually change a payment record from $100 to $70 in database, but overlook the email that still says $100. When scenarios get complex, it's even more expensive and unreliable to check after the fact.
- I’d rather generate the payment record from the events that led to it. Things like ticket statuses, balances, and past events would live in a shared state, updated by explicit rules: sₖ₊₁ = F(sₖ, eₖ), where sₖ is the current world state, eₖ the event, and F the transition rule.
- One way to build this is a [discrete-event simulator](https://ocw.mit.edu/courses/2-854-introduction-to-manufacturing-systems-fall-2016/0dc16a918eabd3f47e3f6d573485dccf_MIT2_854F16_Simulation.pdf#page=15) that advances the clock from event to event, using state-dependent rules and distributions for ticket arrivals, refunds, and escalation delays. We generate the records from the history it produces, so their relationships are established during generation. *This isn’t a novel approach; it has been battle tested in real-world professional domains for decades.*
- buys us strong **internal consistency.**

## Humans and synthetic systems better together


![](https://pbs.twimg.com/media/HU2G_rIaYAAoWVn.jpg)

- **Real human knowledge gives us a prior for those choices:**
    - **Distribution design:** human knowledge helps us ground the right set of users and workflows/capabilities to train for.
    - **Realism grounding:** use examples from people doing the work to capture the constraints and details our simulation misses.
    - **Human review:** domain experts can catch answers that pass our checks but would cause trouble in practice, before we reinforce them in training.
