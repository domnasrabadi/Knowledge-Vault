---
type: article
status: inbox
quality: 1
topics: []
source: https://developers.openai.com/cookbook/examples/partners/eval_driven_system_design/receipt_inspection
created: 2026-08-16
published: 2025-06-02
author: OpenAI Developers
flashcards: none
updated: 2026-08-16
---

# Eval Driven System Design - From Prototype to Production

<div align="center">
  <img src="https://developers.openai.com/open-graph.png" width="220" />
</div>

- This cookbook provides a **practical**, end-to-end guide on how to effectively use evals as the core process in creating a production-grade autonomous system to replace a labor-intensive human workflow
- Making evals the core process prevents poke-and-hope guesswork and impressionistic judgments of accuracy, instead demanding engineering rigor. This means we can make principled decisions about cost trade-offs and investment.

#### Guiding Narrative: From Tiny Seed to Production System

- • **Start Small:** Begin with a very small set of labeled data (retail receipts). Many businesses don’t have good ground truth data sets. • **Build Incrementally:** Develop a minimal viable system and establish initial evals. • **Business Alignment:** Evaluate eval performance in the context of business KPIs and dollar impact, and target efforts to avoid working on low-impact improvements. • **Eval-Driven Iteration:** Iteratively improve by using eval scores to power model improvements, then by using better models on more data to expand evals and identify more areas for improvement.

### Project Lifecycle

- Not every project will proceed in the same way, but projects generally have some important components in common.

#### 1. Understand the Problem

- Usually, the decision to start an engineering process is made by leadership who understand the business impact but don’t need to know the process details

#### 2. Assemble Examples (Gather Data)

- It’s very rare for a real-world project to begin with all the data necessary to achieve a satisfactory solution, let alone establish confidence.

#### 3. Build an End-to-End V0 System

- We want to get the skeleton of a system built as quickly as possible. We don’t need a system that performs well - we just need something that accepts the right inputs and provides outputs of the correct type

#### 4. Label Data and Build Initial Evals

- We’ve found that in the absence of an established ground truth, it’s not uncommon to use an early version of a system to generate ‘draft’ truth data which can be annotated or corrected by domain experts.

#### 5. Map Evals to Business Metrics

- Before we jump into correcting every error, we need to make sure that we’re investing time effectively. The most critical task at this stage is to review our evals and gain an understanding of how they connect to our key objectives.
    - Step back and assess the potential costs and benefits of the system
    - Identify which eval measurements speak directly to those costs and benefits
    - For example, what does “failure” on a particular eval cost? Are we measuring something worthwhile?
    - Create a (non-LLM) model that uses eval metrics to provide a dollar value
    - Balance performance (accuracy, or speed) with cost to develop and run

#### 6. Progressively Improve System and Evals

- Having identified which efforts are most worth making, we can begin iterating on improvements to the system. The evals act as an objective guide so we know when we’ve made the system good enough, and ensure we avoid or identify regression.

#### 7. Integrate QA Process and Ongoing Improvements

- Evals aren’t just for development. Instrumenting all or a portion of a production service will surface more useful test and training samples over time, identifying incorrect assumptions or finding areas with insufficient coverage

### Initial Evals

- Once we have a minimally functional system we should process more inputs and get domain experts to help develop ground-truth data. Domain experts doing expert tasks may not have much time to devote to our project, so we want to be efficient and start small, aiming for breadth rather than depth at first.

### Connecting Evals to Business Metrics

- The point of the above model is it lets us apply meaning to an eval that would otherwise just be a number

### Spin Up the Flywheel

- Having our business model means we have a map of what’s worth doing and what isn’t. Our initial evals are a road sign that lets us know we’re moving in the right direction; but eventually we’ll need more signag

![](https://developers.openai.com/cookbook/assets/images/partner_development_flywheel.png)

- • Our evals show us where we can improve, and we can immediately use them to guide us in model selection, prompt engineering, tool use, and fine-tuning strategies. • We’re not done once system performs well according to our evals. That’s when it’s time to *improve our evals*. We will process more data, give it to our domain experts to review, and feed the corrections into building better, more comprehensive evals.

#### Further improvements


![](https://developers.openai.com/cookbook/assets/images/partner_model_improvement_waterfall.png)

- • **Model selection:** try smarter models, or increase their reasoning budget. • **Prompt tuning:** clarify instructions and provide very explicit rules. • **Examples and context:** add few- or many-shot examples, or more context for the problem. RAG fits in here, and may be used to dynamically select similar examples. • **Tools use:** provide tools to solve specific problems, including access to external APIs, the ability to query databases, or otherwise enable the model to have its own questions answered. • **Accessory models:** add models to perform limited sub-tasks, to supervise and provide guardrails, or use a mixture of experts and aggregate solutions from multiple sub-models. • **Fine-tuning:** use labeled training data for supervised fine tuning, eval graders for reinforcement fine tuning, or different outputs for direct preference optimization.
