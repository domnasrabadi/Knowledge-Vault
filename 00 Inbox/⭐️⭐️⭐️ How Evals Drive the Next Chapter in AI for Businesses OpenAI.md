---
type: article
status: inbox
quality: 3
topics: []
source: https://openai.com/index/evals-drive-next-chapter-of-ai/
created: 2026-08-08
published: 2025-11-19
author: openai.com
flashcards: none
updated: 2026-08-08
---

# How evals drive the next chapter in AI for businesses | OpenAI

<div align="center">
  <img src="https://images.ctfassets.net/kftzwdyauwt9/136Vat98FEB3xuRr8VDh78/d3d153d37c3667c6ca966cc0a2052baa/Eval_Blog_SEO_Card_1920x1080.png?w=1600&h=900&fit=fill" width="220" />
</div>

- At OpenAI, our models are our products, so our researchers use rigorous [**frontier evals**⁠](https://evals.openai.com/) [(1)](https://openai.com/index/evals-drive-next-chapter-of-ai/#footnote-1) to measure how well the models perform in different domains. While frontier evals help us ship better models faster, they cannot reveal all the nuances required to ensure the model will perform on a specific workflow in a specific business setting. That is why internal teams have also created dozens of **contextual evals** designed to assess performance within a specific product or internal workflow. It is also why business leaders should learn how to create contextual evals specific to their organization’s needs and operating environment.
- This is a primer for business leaders looking to apply evals in their organizations. Contextual evals, each crafted for a specific organization’s workflow or product, are an active area of development and definitive processes have yet to emerge

### How evals work: Specify → Measure → Improve


![](https://images.ctfassets.net/kftzwdyauwt9/5NnfoyNbQcCkWHbaqG8bMS/d0a168d37e76d73168878675a4d20b1e/Eval_Blog_Diagram_Desktop_Light.svg?w=3840&q=90)

- 1. Specify: Define what “great” means Start with a small, empowered team that can write down the purpose of your AI system in plain terms, for example: “Convert qualified inbound emails into scheduled demos while staying on brand.”
- This team should be a mix of individuals with technical and domain expertise
- They should be able to state the most important outcomes to measure, outline the workflow end-to-end, and identify each important decision point your AI system will encounter. For every step in that workflow, the team should define what success looks like and what to avoid. This process will create a mapping of dozens of example inputs (e.g. inbound emails) to the outputs they want the system to produce. The resulting **golden set** of examples should be a living, authoritative reference of your most skilled experts’ judgement and taste for what “great” looks like.
- The process is iterative and messy. Early prototyping can help immensely. Reviewing 50 to 100 outputs from an early version of the system will uncover how and when your system is failing. This “error analysis” will result in a taxonomy of different errors (and their frequencies) to track as your system improves.
- This process is not purely technical—it’s cross-functional and centered on defining business goals and desired processes. Technical teams should not be asked in isolation to judge what best serves customers or the needs of other teams like product, sales, or HR. Consequently, domain experts, technical leads, and other key stakeholders should share ownership.

##### 2. Measure: Test against real-world conditions

- The next step is to measure. The goal of measurement is to reliably surface concrete examples of how and when the system is failing. To do that, create a dedicated test environment that closely mirrors real-world conditions—not just a demo or prompt playground. Evaluate performance against your golden set and error analysis under the same pressures and edge cases your system will actually face.
- Rubrics can help bring concreteness to judging outputs from your system, but it is possible to over-emphasize superficial items at the expense of your overall goals. Further, some qualities are difficult or impossible to measure. In some cases, traditional business metrics will be important. In others, you’ll need to invent new metrics. Keep your subject matter experts in the loop throughout, and tightly align the process with your core objectives.
- To actually test the system, use examples drawn from real-world situations whenever possible, and include or invent edge cases that are rare but costly if mishandled.
- Some evals can be scaled through the use of an **LLM grader**, an AI model that grades outputs the same way an expert would; yet, it is still important to keep a human in the loop. Your domain expert needs to regularly audit LLM graders for accuracy and should also directly review logs of your system’s behavior.

##### 3. Improve: Learn from errors

- Addressing problems uncovered by your eval can take on many forms: refining prompts, adjusting data access, updating the eval itself to better reflect your goals, and so forth. As you uncover new types of errors, add them to your error analysis and address them. Each iteration compounds upon the last: new criteria and clearer expectations of system behavior help reveal new edge cases and subtle, stubborn issues to correct.
- To support this iteration, build a data flywheel. Log inputs, outputs, and outcomes; sample those logs on a schedule and automatically route ambiguous or costly cases to expert review. Add these expert judgements to your eval and error analysis, then use them to update prompts, tools, or model
- While evals create a systematic way to improve your AI system, new failure modes can arise. In practice, as models, data, and business goals evolve, evals must also be continuously maintained, expanded, and stress-tested.
- Evals are difficult to implement for the same reason that building great products is difficult; they require rigor, vision, and taste. If done well, evals become unique differentiators
- **In a world where information is freely available across the world and expertise is democratized, your advantage hinges on how well your systems can execute inside your context.** Robust evals create compounding advantages and institutional know-how as your systems improve.
