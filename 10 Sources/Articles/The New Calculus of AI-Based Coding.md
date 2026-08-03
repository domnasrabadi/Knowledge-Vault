---
type: article
status: raw
quality:
topics: [ai-coding, software-engineering]
source: ""
created: 2026-01-02
published: 2025-10-19
author: joemag.dev
flashcards: none
updated: 2026-01-10
---

# The New Calculus of AI-based Coding

<div align="center">
  <img src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEg0Ko_HfgsgHZCIIbQddBTTVrGcFC2QEu7h8UJDmFaGqhFQ_qJzIQivqwT5RwSHKehkNkRwqpCbgPcPJFYDhoasKRlgO7ulFZfqFM9mXIjdqHyYjc7Z4A9NsA6rE735nuWbVpi192DzFcJqK92sHVHptZHh36-KxbO8yPUSA2E9KA9sjR-DgaRzypvZqQ0/w1200-h630-p-k-no-nu/Screenshot%202025-10-22%20at%206.38.56%E2%80%AFPM.png" width="220" />
</div>

Source: https://blog.joemag.dev/2025/10/the-new-calculus-of-ai-based-coding.html

Exported at: `2026-01-10T05:19:49Z`

- we use an approach where a human and AI agent collaborate to produce the code changes. For our team, every commit has an engineer's name attached to it, and that engineer ultimately needs to review and stand behind the code. We use steering rules to setup constraints for how the AI agent should operate within our codebase
- For me, roughly 80% of the code I commit these days is written by the AI agent. My personal workflow: break down the task until I have clarity in my own head (often using AI to explore approaches), prompt the AI agent, review its output, iterate with it until I like the results, and occasionally take over the change set and finish it myself. I pay attention to every line of code the agent produces, and don't accept them until I am fully satisfied with the quality of what is being produced - no different than if I wrote every line myself.
- My team is no different—we are producing code at 10x of typical high-velocity team. That's not hyperbole - we've actually collected and analyzed the metrics.

### Driving at 200mph

- AI assisted code is no different, it may contain bugs even when thoroughly reviewed by a human, and I suspect the probabilities are not significantly different. However, when teams ship commits at 10x the rate, the overall math changes. What used to be a production impacting bug once or twice a year, can become a weekly occurrence
- Once again, this is not just hyperbole—our team sees signs that these are the challenges that pop up with a step function increase in throughput.
- I am increasingly convinced that in order for agentic development to increase engineering velocity by an order of magnitude, we need to decrease the probability of problematic commits by an order of magnitude too.

### The Cost-Benefit Rebalance

- As an example, I've always liked "wind tunnel" style tests, that test fully assembled system in a controlled environment. To achieve that, one pattern I've used is implementing high fidelity "fake" versions of external dependencies that can be run locally. If you do that, you can then write build-time tests that run locally and verify end-to-end behavior of the whole system. You can even inject unexpected behaviors and failures into fake dependencies, to test how the system handles them. Such tests are easy to write and execute because they run locally, and they are great at catching those sneaky bugs in the seams between components.
- Unfortunately, faking all the external dependencies isn't always easy for a service with moderate level of complexity. And even if you do, you now have to own keeping up with the real dependencies as they evolve. For those reasons, in my experience most teams don't write such tests.
- I think we are seeing early signs that agentic coding can change the calculus here. AI agents are great at spitting out large volumes of code, especially when the desired behavior is well known and there's little ambiguity. Ideas that were sound in principle, but too expensive to implement and maintain just had their costs decrease by an order of magnitude
- Our project (with the help of an AI agent) maintains fake implementations of external dependencies like authentication, storage, chain replication, and inference engine to be used in tests. We then wrote a test harness that uses those fakes to spin up our entire distributed system, including all the micro-services, on developers' machines. Build-time tests then spin up our canaries against that fully assembled stack verifying the system as a whole works. I'm really bullish on this approach catching a category of bugs that in the past could only be caught once the change was committed and made it to the test environment

### Driving Fast Requires Tighter Feedback Loop

- In the amount of time it takes to build, package, and test one set of commits, another dozen might be waiting to go out. By the time a change set is ready to deploy to production, it may contain 100 or more commits. And if one of those commits contains a problem, the deployment needs to be rolled back grinding the pipeline to a halt. In the meantime, even more changes accumulate, adding to the chaos and the risk.
- When teams are moving at the speed of dozen of commits per hour, problematic issues will need to be identified, isolated, and reverted in minutes instead of hours or days
- I believe that achieving similar increase in velocity for a software team requires constraints on how teams communicate. When your throughput increases by an order of magnitude, you're not just writing more code - you're making more decisions
- Should we use this caching strategy or that one? How should we handle this edge case? What's the right abstraction here? At normal velocity, a team might make one or two of these decisions per week. At 10x velocity, they are making multiple each day.
- I find that traditional coordination mechanisms introduce too much latency here. Waiting for a Slack response or scheduling a quick sync for later in the day means either creating a bottleneck - the decision blocks progress - or risking going down the wrong path before realizing the conflict. At high throughput, the cost of coordination can dominate!
- But here's the critical part: these gains won't materialize if we simply bolt AI agents onto our existing development practices. Like adding a turbocharger to a car with narrow tires and old brakes, the result won't be faster lap times - it will be crashes. At 10x code velocity, our current approaches to testing, deployment, and team coordination become the limiting factors. The bottleneck just moves.
