---
type: paper
status: structured
quality:
topics: [agent-evaluation, synthetic-data]
source: ""
created: 2025-08-23
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Sachi Shah
- Category: article
- URL: https://sierra.ai/blog/simulations-the-secret-behind-every-great-agent
## 0.2 Highlights

- agents vs rules-based software = agents don’t follow scripts, so tests can’t either
    - rules-based software = same input → same output, straightforward testing and incremental rollouts 1% → 10% → 50% → 100%
    - agents with AI = same input can yield different outputs, making “works” ambiguous
    - testing focus shifts from instruction-following to goal attainment for the customer
- testing goal for agents = determine whether the agent enables customers to accomplish their goals

- simulation = new testing approach using simulated conversations to ensure reliability at scale
    - anatomy of a simulation = agent, user, judge
        - agent = the system under test
        - user = mock persona varying language, comfort with technology, tone, and task
            - examples: buy a new pair of shoes, exchange a product without a receipt, apply for a mortgage, troubleshoot a technical issue, chat in French late at night, cancel a subscription
        - judge = independent evaluator that grades outcomes
            - assesses goal completion, adherence to standard operating procedure, alignment with brand guidelines, accuracy, helpfulness, and comprehensibility
    - variety principle = create scenarios that reflect real-world diversity, not just obvious cases
    - re-runs = run each simulated conversation multiple times and aggregate judged results

- automation in testing = from zero to tested without heavy manual effort
    - historical constraint = robust manual coverage is time-consuming and tedious, so teams often skip or minimize testing

- great agents require great simulations = top agents are empathic, help customers achieve goals quickly and easily, and are battle-tested
- benefits of simulations = proactive quality assurance without slowing development
    - identify failure modes before they impact customers
    - catch issues early and maintain quality as complexity grows
    - ensure coverage across all known cases, not just some cases
