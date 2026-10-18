---
type: article
status: inbox
quality: 1
topics: []
source: https://www.lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix
created: 2026-10-18
published: 2026-09-22
author: Hamel Husain
flashcards: none
updated: 2026-10-18
---

# Advanced evals: How to find (and fix) hidden AI failures in your product

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!0_d7!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f6018cf-fa53-4f40-99d9-b1c9980dd031_1456x970.png" width="220" />
</div>

- “evals are the new PRDs,” and increasingly, leading companies have been talking about how investing in evals has paid off:
    - **[Shopify](https://shopify.engineering/fine-tuning-agent-shopify-flow)** used evals to guide development of an AI workflow builder that was 2.2 times faster and 68% cheaper than the frontier-model system it replaced.
    - **[Cursor](https://cursor.com/blog/how-cursor-router-works)** developed its Auto Balance routing performance with evals, resulting in much higher user satisfaction while reducing costs by 41%.
    - **[Ramp](https://engineering.ramp.com/post/apple-intelligence-receipt-matching)** increased its automatic receipt collection product’s accuracy from 35% to 83% after investing in evals.
    - **[Harvey](https://www.harvey.ai/blog/rebuilding-playbook-review-as-a-multi-agent-system)** rebuilt its AI contract reviewer with evals, nearly doubling the product’s internal quality score.
- AI products are easy to change but hard to predict. A prompt, model, or code change can improve one behavior while breaking another. Evals turn your judgment about what “good” looks like into repeatable tests your team can run before shipping. Production errors flagged by evals can become additional test cases that improve your AI, creating an advantage that compounds over time.
- And now that AI can produce changes faster than people can review them, evals help teams ship quickly by automatically checking if a product still works as intended.
- we’ve found that most teams skip the first stage of error discovery and jump straight to writing metrics
- It is easy to see why. Looking through lengthy user session records to find failures feels slow and hard to scale, whereas metrics are concrete and easy to automate. But if you write metrics too early, you end up making too many assumptions about what’s important—and potentially measuring the wrong thing, or the right thing poorly.
- This is why error discovery is the eval equivalent of product discovery. Just as product discovery shows which problems are worth solving, error discovery reveals which AI failures are worth measuring

### Find the errors that matter to your product

- When you’re building an AI product, you need evals to understand where it makes mistakes. But maintaining evals costs time and money; it doesn’t make sense to measure everything. Good error discovery identifies which failures are worth measuring and tracking over time
- Agents are often faster than humans at spotting obvious issues and can find patterns we might miss. But they are far less reliable when a failure depends on your definition of a good product experience. You can explain those standards to the agent, but you often only discover them in the first place by reviewing the data. This process, where reviewing examples changes your definition of good, is called [criteria drift](https://arxiv.org/abs/2404.12272).
- **Prospect:** “This is out of my budget. Thank you for your business.” **Leasing assistant:** “You’re welcome! If your situation changes or if you have any other questions in the future, feel free to reach out. Have a great day!”
- To most agents, this looks like a success; they wouldn’t identify an error in this trace. But the product goal is to facilitate sales, which includes finding the right property matches for prospects’ different needs. In this situation, the agent should have explored cheaper units or other properties owned by the same company and offered the prospect alternatives.
- If we’d prompted the agent to look for this “objection handling” failure up front when we gave it traces to check, the agent would have caught the error automatically. But we’d only know to add “objection handling” to our criteria *after* seeing this trace ourselves. This is a classic case of criteria drift—and why it’s critical to take a step back to review failures and define success before dispatching an agent to find errors in a stack of traces.
- In [a broader study](https://parlance-labs.com/blog/posts/auto-evals/index.html), we ran automated eval tools and coding agents against 100 production traces from this same apartment-leasing assistant. We found the following: 1. **Agents missed issues requiring product judgment** and context outside the trace such as Markdown formatting in text messages and missed human handoffs (in addition to objection handling). 2. **Agents are good at catching failures that are obvious** inside a trace, like answers that are contradicted by tool output. 3. **Agents also find issues that humans miss**, but they introduce noise by flagging good responses as failures.
- Clearly, automated approaches are still useful for finding some types of errors, and they work especially well in conjunction with human judgment. So how do you benefit from an agent’s automation while keeping a human in the loop? The answer is a process that draws on [active learning](https://en.wikipedia.org/wiki/Active_learning_(machine_learning)), a method for choosing the most informative examples to review given limited time. Start with a diverse sample of traces so you cover the range of your data. When you find a failure, look at a few more instances of it before you decide you understand it. After you’ve reviewed enough examples, let the agent annotate traces that you can then accept or reject.

### Step 1: Start with your traces

- Error discovery requires traces. Each trace consists of the user’s input and system prompt, whatever your system did in between (retrieval, tool calls, intermediate model calls), and the product’s final output. Each trace should contain enough information for a reviewer to reconstruct what happened and decide whether it was good

![](https://substackcdn.com/image/fetch/$s_!Rvcj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01723f03-645b-4635-8cd6-3afbb8d54904_1456x2044.png)


#### Pro tip: How to simulate user queries

- An effective way to simulate user queries is to define a small number of dimensions that you anticipate your product might fail on. For example, dimensions for the leasing assistant might be the task (scheduling a tour, asking about pricing, asking about the pet policy), the type of person asking, and whether the request was clear, ambiguous, or out of scope. Then have the model use these dimensions and turn each combination into a natural-language user query. Using dimensions like this helps steer the AI away from producing homogeneous outputs.
- Create a structured list of test scenarios by combining one value from each dimension. Loop through the scenarios and make a separate model call for each one. Pass only one scenario into each call. Enforce a structured output schema with a single *user_query* field, then save the query alongside its scenario in *synthetic_queries.jsonl.*
- The prompt above recommends separate model calls for each scenario because we’ve found that asking an agent to one-shot it tends to produce less diversity
- After generating synthetic data, review the examples and remove any that are unrealistic. If you notice scenarios that your dimensions don’t cover, update the dimensions and generate new examples covering those gaps.

### Step 2: Review and annotate your data

- point your coding agent at the */evals-start skill* or tell it where your data is: > *“Use the evals-start skill. My traces are in traces/traces.jsonl and I want to find issues occurring in my AI product.”*
- *evals-start* is the entry point for the [evals skills plugin](https://github.com/ai-evals-course/evals-skills). It looks at your situation and sends you to the right workflow. In our case, we have traces we haven’t analyzed yet, so it will route us to *error-discovery*.
- The first thing *error-discovery* does is read a sample of your records to learn their schema. Then it creates a small review app customized for your data and serves it to you locally

![](https://substackcdn.com/image/fetch/$s_!Wbkc!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9da9bd6c-4623-4c4f-a0ae-a971493385a3_1456x1530.png)

- This interface renders the conversation as a message thread, with tool calls and their outputs displayed alongside. You input your annotations into a free-form text box.
- Interface customization is an important part of the plugin’s value. Different types of interfaces are best suited to reviewing different types of data

![](https://substackcdn.com/image/fetch/$s_!oT5M!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1ce6d823-6e2a-4c8a-ad87-44b9158568d1_1456x1104.png)

- In this app, the writing displays as a text block, with flags displayed alongside, which makes it well-suited to reviewing writing.
- There are several design principles embedded in the skill that guide the way an interface will render. The two most important ones are: 1. **Show user-facing output the way the user sees it.** For example, an email should look like an email, a PDF should render as a PDF, etc. 2. **Expose important metadata that may be helpful for navigation or filtering.** In the leasing example, the channel the user comes through is likely important and worth filtering on: SMS, voice, web chat, etc.
- The skill also instructs your agent to cluster your traces so it can build a diverse initial sample. It mixes cluster representatives with random picks. This approach isn’t perfect, but we’ve found it to be a better starting point than naive approaches to looking at data

![](https://substackcdn.com/image/fetch/$s_!-M3H!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa349ef34-5a10-4560-962c-dabab77d7993_1456x871.png)

- In the above example, the annotation app for the writing assistant lets you hover over clusters to review representative documents.
- The biggest advantage of using a coding agent is the ability to change the interface on the fly. If you notice a missing field, want to filter to a slice of traces, or render data differently, all you have to do is ask

#### Annotating traces in the app

- Once the app is running, the skill asks you to review 10 traces before it suggests errors to review. This is a deliberate safeguard against automation bias
- Some rules of thumb for making annotations: 1. **Describe the problem so that a colleague (or agent) could understand what you meant.** “Bad response” is a bad annotation. “The assistant said the unit was available when the tool output showed it was leased” is actionable. 2. **Don’t try to do root cause analysis.** You’re looking for what went wrong from the user’s perspective, not why your system failed internally. For example, don’t try to diagnose retrieval issues. 3. **Stop at the first upstream error.** If a trace has multiple problems, annotate the first one you notice. This heuristic helps you save time and focus on the most impactful issues, since upstream failures in agent trajectories tend to be more important than downstream ones. You can relax this constraint later when you are more efficient at this exercise. 4. **You only need to annotate failures when starting out.** Annotating what makes a trace good might enhance your agent’s understanding but can be skipped if you are short on time.
- After annotating at least 10 traces, the AI will learn from your initial notes and try to find additional issues in your data that you can accept or reject. It’s important not to blindly accept the agent’s early proposals. Review them carefully and use disagreements to correct the agent’s working understanding. You may need several human-agent iterations before the suggestions become useful. We encourage you to keep annotating beyond the first 10 traces until your own learning has plateaued
- As a rule of thumb, aim for 100 traces to make sure you aren’t quitting too early. More traces will also give the AI more signal and improve its suggestions.
- Here is what the interface might look like as you’re reviewing suggestions for the writing assistant (your specific interface will be different, since the AI customizes it for your use case):

![](https://substackcdn.com/image/fetch/$s_!PKVu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F84b12664-2af3-442c-8ab2-32f2ed63a5e4_1456x1114.png)

- Here is another view that groups the suggestions by failure mode:

![](https://substackcdn.com/image/fetch/$s_!Rpad!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d7685c1-85d8-4541-a322-61454435e5d7_1456x1054.png)

- If the AI’s suggestions aren’t right, you can tell your coding agent to fix it—just as you can if you want to change the interface. Your annotations do not have to be perfect. The goal is to find actionable issues in your logs rather than perform an exhaustive search

### Step 3: Turn failure modes into product priorities

- Once you’ve collected at least 100 diverse annotated traces, your next task is to turn them into a prioritized list of product issues. The AI will attempt to cluster your annotations into failure modes and count them so you can spot patterns
