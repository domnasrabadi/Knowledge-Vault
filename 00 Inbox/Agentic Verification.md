---
type: article
status: inbox
quality: 
topics: []
source: https://addyo.substack.com/p/agentic-verification
created: 2026-10-31
published: 2026-10-14
author: Addy Osmani
flashcards: none
updated: 2026-10-31
---

# Agentic Verification

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!9coI!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52129609-d334-4303-924e-2a7089486f91_2754x1536.jpeg" width="220" />
</div>

- If you give an AI agent a way to independently verify its work, that can heavily improve the quality of output.
- The stuff that made “Good Code” expensive (tests, benchmarks, specs, real e2e runs) is now a cheap thing you can ask an agent for. You can improve the checks.
- So our work is less “review every line” and more “build loops the agent can run itself”. Give the agent a way to verify the work. That loop is where quality comes from.
- And make taste compound. When the agent gets something wrong, write it down (shared config, a hook, a test) so it doesn’t happen twice.
- **To make your agent produce high-quality output, equip it with a way to check its work. Tests are part of that.** Here are some of the ones I think are worth investing in. - Write end-to-end tests that simulate real user flows and act as the ground truth - Use property-based testing to specify what should never happen and generate thousands of test cases that attempt to break those constraints - If replacing a system, compare the old and new versions using randomly selected inputs - Require tests to run quickly and deterministically, which reinforces the agent to retry when the loop is slow or unreliable (the agent may learn to retry, not fix the problem)

![](https://substackcdn.com/image/fetch/$s_!uAH-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc410f959-0f40-422c-b4d9-f64fbd3a9ada_3200x3200.png)


### Verification is the bottleneck

- Today’s models are good enough that the major bottleneck is not code-writing but the ability to verify that the code they’ve written is correct.
- if your agent can test its own output, it’ll write a change, run the check, read the output, and try again over and over until it can pass the check.
- It’s hard to overstate the improvement in quality that you can get out of a self-verifying agent vs a feedback loop dominated by humans. I would always prefer a much better feedback loop to a slightly better model.

![](https://substackcdn.com/image/fetch/$s_!zlOU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a6d4992-3ab1-4ff1-b6a6-f5a31fbd3725_3200x3200.png)


### There’s a whole spectrum of tests


#### E2E tests

- If you had to choose only one test to use, it would be E2E tests. They describe what a real user does.
- An E2E test is what a human would do: sign up, add an item to the cart, checkout, and see a confirmation. It ignores the internal structure of your code and sees only what the user can see.
- This is the kind of oracle you want for your agent. Machines will often write code that passes checks but misses the big picture. A mock-based unit test might pass, and the feature could be broken because the agent and your test share a misunderstanding. An E2E test, on the other hand, is very hard to trick. Either the whole thing works, or it doesn’t.

![](https://substackcdn.com/image/fetch/$s_!QbKk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c0a7e46-ac45-4147-b076-8b8058405b79_3200x3200.png)

- - They cover only important, meaningful user flows, not all possible paths. - They tell you what’s wrong: Screenshots, tracing, and an explanation of which step failed tells the agent what went wrong, rather than making it flail in the dark. “Timeout after 30s” tells you nothing. - They work on the agent’s local configuration as well as its deployment environment. - They define “done”: “Implement this feature” is too vague. “Make this E2E test pass” is a target the agent can chase on its own.

#### Property-tests: constraints that can’t break

- Property tests are about what a human doesn’t consider: the cases where agents go wrong.
- Much of what humans write in tests is about examples: “If this is the input, then the output should be this.” These tests are good at ensuring that something should work, but they’re poor at ensuring that something should never fail: Humans can’t think of all possible inputs that would fail.

![](https://substackcdn.com/image/fetch/$s_!oqca!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F275a7703-566a-45e1-a775-e36fa8d19499_3200x3200.png)

- Property-based tests reverse the premise: You create a rule that should hold, and a tool will generate hundreds or thousands of inputs to break it.
- • Invariants: sorting doesn’t change the number of elements or the contents of the collection. A balance never becomes a negative number. Money in is money out. • Idempotency: migrating, normalizing, or retrying the same thing twice has the same effect as doing it once. • Equivalence: the optimized function yields the same result as the simple, correct one.
- Properties are a great way to specify your requirements. If I say that the total for a cart must always be the same as the sum of its line items, that’s a great specification.
- How to start without boiling the ocean:
    - Start with a small, essentially pure function, like a parser, a formatter, a pricing calculation.
    - Write the property in plain English before implementing it in code.
    - When your test library finds a problem, save the minimized test case so you can use it for regression testing.
    - Ask the agent for properties instead of test examples when making new code. It’s very good at it, once you tell it to.
    - When replacing an old system with a new one, generate a diff between them.
    - When doing a rewrite or migration, treat the old system as the oracle.

#### Differential tests: the old system is the oracle

- Differential testing bridges that gap. Instead of relying on your new test suite, run the old and new systems side by side with the same inputs. If there’s a discrepancy in the outputs, you’ve either introduced a bug in the new system, or you’ve deliberately made a change you should document as a breaking change.

![](https://substackcdn.com/image/fetch/$s_!gAxS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fae5ae9de-9850-48b5-983e-44ff02104f2b_3200x3200.png)

- Randomly generate inputs, replay a sample of live traffic, or both. This is equivalent to property-based testing, with the property that your new system’s outputs match the old system’s outputs.
- Differential testing is brilliant for agent-assisted large-scale migrations.
- A few practical notes:
    - Normalize everything that doesn’t matter and ordering that doesn’t carry any semantic weight. Stripping those differences out before comparing makes sure that you never get an infinite stream of false diffs.
    - Track intended changes in a list of approved changes: every change you want to make is noted with a reason why. This keeps “different” from becoming an acceptable state.
    - The secret to confidence is just getting every last bit moved: the diff harness gives you the confidence to wipe the old system away. Keeping both systems running is twice the work of understanding either one, and it introduces two different ways your migration can break.

### Make the loop fast and deterministic


##### What good looks like

- Here are a few ideas of what I think “good” might look like - the agent should learn from the incentives of the loop.

![](https://substackcdn.com/image/fetch/$s_!St6s!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7c0036b-40ac-4bdd-8f15-90a9e4e87205_3200x3200.png)

- • Test suite produces the same results every time. Use seeded randomness, frozen clocks, controlled networking, and isolated state. If it fails, the system is broken. • Flaky tests are isolated from the main suite, and removed immediately. A flaky test in the main suite is worse than no test at all, because it breaks trust in every other result. • Output is short and to the point. Specific messages about what failed are better than voluminous logs about what passed. • Unwanted output costs the agent attention and mental bandwidth on every turn. • Quick first loop for the agent, and run the heavy E2E and diff tests before integrating changes. • Treat the testing infrastructure as one of the components that the agent depends on. Improving it has compounding positive effects on all tasks.

### Write the check before the code

- Before telling your agent to make something, you have to know what it’s supposed to succeed at. That could be an end-to-end workflow, a specific property, or a comparison to a prior system. Whatever it is, make sure that it’s fast and deterministic, and you can let the agent iterate over a solution.
