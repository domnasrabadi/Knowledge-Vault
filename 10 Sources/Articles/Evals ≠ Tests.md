---
type: article
status: raw
quality: 
topics: [llm-evaluation, agent-evaluation, software-engineering]
source: https://x.com/ankrgyl/status/2084667136618762550/?s=12&rw_tt_thread=True
created: 2026-09-26
published: 2026-08-04
author: Ankur Goyal
flashcards: none
updated: 2026-09-27
---

# Evals ≠ Tests

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2012286692741558272/5YxTLgKY.jpg" width="220" />
</div>

- Though it’s tempting to conflate evals and tests, doing so confuses the differences between them.
    - A test is about *if* the thing can work
    - An eval is about *what* the thing can and cannot do
    - A mature eval practice is about what the thing *should* be doing, how often, and in what circumstances

### Tests = does it work?

- Correctness captures whether or not your software can work as expected, and performance measures how well your software does that work in the real world
    - For agents, correctness also requires information about how the agent works.
        - Is it calling the right tools?
        - Is it surfacing the right information?
        - Imagine a simple weather app agent. The temperature it returns is correct, but did the agent pull that information from the right datasource, and share it in Fahrenheit when it could have chosen Celsius?
- This is how you measure *if* an agent is working, and tests still have their place here. You shouldn’t replace an eval with a test, but you shouldn’t stop testing altogether either.

### Evals = what can it do?

- Think of evals as like traditional observability, but with new and more complicated things being measured
    - You populate simulated environments, run lots of scenarios, and collect data on what happens. These measurements are similar to the metrics you gather in production to monitor performance, but they also capture data that is novel to LLMs, as well as qualitative things like brand-safety or factuality.
- A mature eval suite should tell you *what* the thing can do, and document what it does when it is exhibiting new behavior
    - Then you can use that data to determine what it *should* be doing, so you can improve the quality of the agent as these new behaviors emerge.

### Mature evals = what should it be doing?

- A healthy eval practice means that each time a user encounters unexpected behavior, teams can save it in a dataset and add it to their eval suit
- A healthy testing practice means that as you update the implementation of an agent based on those evals, you can write tests that assert it's working well. If you make a significant change, like introducing a new weather-data provider in the example above, you’ll want to rerun that test to see how it’s working with this new implementation.
- Ultimately, every engineer should have a workflow that can do both, suited to the needs of their team, production environment, and the specific agents they’re building.
