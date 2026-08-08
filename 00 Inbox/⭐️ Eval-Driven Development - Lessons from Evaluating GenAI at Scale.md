---
type: article
status: raw
quality: 1
topics: [llm-evaluation, llm-judges, evaluation-metrics, error-analysis]
source: https://medium.com/airbnb-engineering/eval-driven-development-lessons-from-evaluating-genai-at-scale-e817e5ae5788
created: 2026-08-08
published: 2026-07-28
author: Rohit Girme
flashcards: none
updated: 2026-08-08
---

# Eval-driven development: Lessons from evaluating GenAI at scale

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:1400/1*XK40dh-lXviuXXY_WhUCUA.jpeg" width="220" />
</div>

- How Airbnb teams build trustworthy Generative AI products by treating evaluation as a first-class engineering discipline; not an afterthought.
- At Airbnb, we build LLM-powered features across our product, with recent launches including review highlights, AI customer support, smart communication features for guests and hosts, and more
- Evaluating LLM-based systems is challenging work,
- Without a deliberate strategy, three things tend to happen:
    - **False confidence**: A generic “helpfulness” metric scores well, you ship, but it didn’t capture the failure mode people actually hit.
    - **Undetected regressions**: A prompt change subtly degrades a dimension you weren’t measuring.
    - **Wasted effort:** You build a scaled eval pipeline for metrics that don’t correlate with outcomes.

##### The one rule

- **When in doubt, look at your data.** Manually reviewing your data and building an intuition for what counts as success is always the starting point we recommend to teams. Build your prototype, and run it through 100 examples (synthetic is fine). Then *read the outputs*. Read the traces and find the model’s mistakes. Categorize them and build an eval.

##### Eval-driven development

- Formalized, that habit becomes **eval-driven development (EDD)**
- Rather than predicting every failure upfront, EDD builds the infrastructure and habits to **discover, encode, and continuously test** for failure modes as they appear.
- also forces stakeholders to externalize what “good” means, which shapes the product roadmap
- Five principles anchor EDD: 1. **Define goals and gates upfront.** What are you optimizing for? What must be true before you ship? These answers may not be clear right away; you might discover them as part of your data exploration. 2. **Let real errors guide your metrics.** Co-develop them with cross-functional partners based on observed failures. Don’t invent them in a vacuum. 3. **Keep your evaluator set small and sharp.** 3–5 well-calibrated LLM-as-judge evaluators beat 20–30 noisy ones. Each should target one specific correctness dimension. 4. **Appoint a decision-maker.** While what constitutes correctness should be a team discussion, people will sometimes disagree. Include a final (human) decision-maker who makes the ultimate call on what constitutes good vs. bad system behavior. 5. **Collaborate continuously.** Have your product partner regularly answer: “Is X better or worse than Y?” and “What’s actually wrong with this output?”

#### 2. The three evaluation methods

- Layer 1: Programmatic checks (fast, low resource — catches obvious failures)
- Layer 2: LLM-as-a-Judge (nuanced - catches quality issues)
- Layer 3: Human evaluation (high resource - validates edge cases, calibrates the stack)

##### Programmatic & heuristic metrics


![](https://miro.medium.com/v2/resize:fit:1400/1*Rmao9jN6R1ozbAVaUP7D9A.png)


##### LLM-as-judge (Virtual judges)


![](https://miro.medium.com/v2/resize:fit:1400/1*hAbCLfHCaQNEFYSgfw0LrQ.png)


##### Calibration: Making your virtual judge trustworthy

- A virtual judge that hasn’t been calibrated is worse than no judge at all, because it gives you false confidence
- • Create a golden dataset of 50–100 examples. This MUST include bad examples (not just good ones). • Run your virtual judge against the golden set. • Measure agreement. Target percentages in the high 80s-90s. Possible options to measure disagreement are Cohen’s kappa or Krippendorff’s alpha. (Perfect agreement isn’t achievable — even humans disagree.) • Analyze disagreements. Refine the prompt and update your few-shot examples. Then re-run the loop until you hit the target agreement. • Recalibrate periodically as failure modes evolve.

##### Human evaluation

- Human judgment remains the gold standard for ground truth, high-stakes domains, and resolving disagreements between automated evaluators.
- 4. A practical walkthrough Here’s what the full process looks like end-to-end, using a fictionalized and simplified version of a real use case. **Scenario:** You’re building an AI assistant that answers questions about a travel platform’s support policies. **Step 1: Explore & discover.** Run 100 inputs through your prototype and read every output. You find:15 responses generated policy details not in the source documents (*faithfulness issue*); 8 correct but too verbose (*conciseness*); 5 refused valid questions (*over-refusal*); 3 had broken JSON (*format*). **Step 2: Build evals.** Add programmatic checks for JSON validity and length bounds. Write a virtual judge for faithfulness (separate prompt, different model, chain-of-thought) and another for conciseness. Have your PM or subject matter expert label 60 examples, including failures, as a golden set. **Step 3: Calibrate & iterate.** Your faithfulness virtual judge agrees with the PM 78% of the time. Not good enough. Analysis reveals the judge is penalizing accurate paraphrases as “unfaithful.” Update the rubric and add few-shot examples. Agreement jumps to 88%. Improve the retrieval step; faithfulness failures drop significantly.
- NOTE: Here, we find that when iterating on models and prompts, it’s best to fix one variable at a time. First fix the model and vary the prompt, then fix the prompt and vary the model, then fix both and vary the serving configuration. At each stage, virtual judge results narrow the candidate pool. Then, you can improve the virtual judge(s) using samples from the top candidates. The evaluators and the candidates sharpen each other until both stabilize.
- Key takeaways 1. **Look at your data.** Read outputs and traces before building anything else. 2. **Avoid generic metrics.** Build evaluators for *your* product’s real failure modes. 3. **Start with 50–100 rows.** Fail fast, iterate cheaply. 4. **One evaluator per dimension.** No “God evaluators.” 5. **Calibrate to high 80s-90s% agreement** before trusting your Virtual Judge at scale. 6. **Use all three methods**. Programmatic, Virtual Judge, and human as layered defenses. 7. **Include bad examples** in your Gold Set. You can’t test discernment without them. 8. **Evaluate the system, not just the model.** Test retrieval, tool calls, the full pipeline. For agents, evaluate the trajectory, not only the final answer. 9. **Mirror evals in production.** Pre-production metrics are not one-and-done. 10. **Evaluation is a team sport.** Evaluation is about shaping what product success looks like, and that takes contributions from many people. The teams that succeed with AI aren’t the ones with the best models, they’re the ones with the best communication and clearest product vision.
