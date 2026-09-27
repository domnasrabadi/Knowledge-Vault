---
type: article
status: raw
quality: 
topics: [ai-coding, career-development]
source: https://x.com/posthog/status/2099576313216422349/?s=12&rw_tt_thread=True
created: 2026-09-26
published: 2026-09-14
author: Ian Vanagas
flashcards: none
updated: 2026-09-27
---

# What Engineers Do When AI Writes the Code

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2098100373403938817/bzPJAKYT.jpg" width="220" />
</div>


## So what will engineers be doing?

### 1. Monitoring the situation

- Engineers spend a lot of time monitoring running agents, fixing errors, responding to customer requests, evaluating competitors, checking dashboards, strategizing on their role in company priorities, learning new workflows, and babysitting outstanding PRs.
    - This means engineers can’t be waiting for the right information to come to them.
        - The best ones now create systems to get the information they need at the right time.
        - This is part [loop engineering](https://posthog.com/newsletter/loops?utm_source=posthog-newsletter&utm_medium=post&utm_campaign=ai-writes-all) and part [context engineering](https://posthog.com/newsletter/fix-your-agents?utm_source=posthog-newsletter&utm_medium=post&utm_campaign=ai-writes-all)
- Why is doing all this important?
    - Because without this information, you will likely end up working on the wrong thing and not know it.
    - Knowing all the possible things you could be working on enables you to prioritize and pick the right one.

### 2. Setting direction

- Software might be [increasingly driving itself](https://posthog.com/blog/what-if-your-product-built-itself?utm_source=posthog-newsletter&utm_medium=post&utm_campaign=ai-writes-all), but you still need to say where you want it to go. This requires synthesizing and analyzing what you observed to figure out what is valuable and worth acting on.
    - Based on the input an engineer receives, there will be hundreds of potential paths. In the past, product managers or execs might have been responsible for picking the best ones, but it’s now increasingly up to engineers.
- Without a clear direction, you can feel productive without actually making progress.
    - AI makes this worse by enabling you to add anything you can think of easily.
    - The direction and experience of your entire product can become clouded by features that aren’t what users actually want or you can be quickly led down the wrong path that’s hard to reverse.

### 3. Deciding how to build and implement

- Engineers might not be writing code, but they are still deciding what code gets written.
    - A direction leads to many smaller decisions.
    - Each decision is a hypothesis of what can be built to make progress towards the direction you're going.
    - What this often looks like is deciding on scope. This requires knowing the codebase, what’s possible, what agents are capable of, and their blind spots.
- It’s this understanding of the problem area, implementation details, and structure that enables engineers to ask the right questions and follow up to get a solution shipped.

### 4. Evaluating the work of your agents

- Engineers still need to evaluate whether it was **built right**.
    - This is done through [code reviews](https://posthog.com/newsletter/code-review-tips?utm_source=posthog-newsletter&utm_medium=post&utm_campaign=ai-writes-all) and asking questions like:
        - Did the agent actually follow directions?
        - How is the code quality of this change?
        - Did the tests pass? If not, how do I make them pass?
- With the volume of changes coming from agents, this quickly becomes a bottleneck.
    - If you are generating 20 PRs per day, reading every line and running them by hand is unrealistic.
    - You need new systems, like review and testing agents, to keep up while ensuring the code you ship is good.
        - Systems like these are necessary when engineers are seeing a dramatic increase in the amount of pull requests they need to review. At PostHog, we went from 1,441 PRs merged in January to 4,869 in August while only growing engineering headcount 10%.

### 5. Improving the entire loop

- This process doesn't just end.
    - It loops repeatedly.
    - What you build and ship leads to new observations like “are people using what we built?”
- The loop isn’t just linear either. Stages feed back on each other:
    - The information you find valuable while **setting direction** informs how you **monitor the situation**: what information you pay more attention to and what you ignore.
    - How well a **decision** gets built informs the scope of **what you’ll decide for agents to build** **next**. Seeing an agent flail and make mistakes leads you to reduce the scope of its future tasks.
    - The functionality and usage of **what you built** informs whether it was the **right direction**, giving you experience and updating your knowledge on agent capabilities, technical feasibility, and customer demand.
- It’s not just one big loop, but many smaller loops as well.
    - The consequence of this is engineers doing more work on the system that builds the product than the product itself.
    - They build the [software factory](https://posthog.com/newsletter/software-factories?utm_source=posthog-newsletter&utm_medium=post&utm_campaign=ai-writes-all) rather than the software.
- The growing capability of agents means there are cases where you can skip much of the loop too.
    - Agents often only really need direction and the right tools to ship a valuable fix.
    - With these, they can then figure out what to build, how to build it, and evaluate whether it actually worked.

![](https://pbs.twimg.com/media/HSMgm4mWIAAjpjN.png)
