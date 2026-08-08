---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/braintrust/status/2039356267949445230/?rw_tt_thread=True
created: 2026-08-08
published: 2026-04-01
author: Braintrust
flashcards: none
updated: 2026-08-08
---

# Evals are the new PRD

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2023446233713700868/2kunzppe.png" width="220" />
</div>

- Traditional product development follows a well-worn loop.

![](https://pbs.twimg.com/media/HEq1_mXbEAAd7Qt.jpg)

- For AI products, a better development loop looks like this.

![](https://pbs.twimg.com/media/HEq2JG8WAAAznPG.jpg)

- The PM defines what "good" looks like through structured, repeatable tests. The eval becomes the spec, the acceptance criteria, and the roadmap all at once. It defines the target, measures pass or fail, and shows where to improve next. The team then hillclimbs against that target: the PM sets the bar in evals, and the team iterates on prompts, retrieval, tools, models, and system design until the product clears the quality bar.

### What an eval actually is

- An eval is a structured, repeatable test that answers one question. Does my AI system do the right thing? Think of it as a unit test for AI behavior. You define a set of inputs along with expected outputs, run them through your AI system, and score the results using algorithms or AI judges

### A concrete example

- Say you're building a recipe generation feature from cooking videos. The PRD says "be helpful and accurate." What does that actually mean? Break it into three measurable signals. **Is the recipe formatted correctly?** Ingredients should come first, then steps. An AI judge can evaluate structural formatting against a rubric. **Are all video-mentioned ingredients included?** This is a deterministic check. A string match algorithm can verify that every ingredient mentioned in the video transcript appears in the generated recipe. **Are instructions written in short, scannable sentences?** Another AI judge, calibrated against examples of good and bad instructional writing. That gives you three measurable signals and one hill to climb. Instead of telling engineering to "make it better," you hand them an eval and say "make this number go up."

### The flywheel matters more than the first eval

- First, **observe** by logging every input, output, trace, and failure so you have full visibility into what your system is doing in production. Then **analyze** to find patterns. What's breaking, for whom, and why? This is where observability turns into product intelligence. Next, **evaluate** by turning those failure patterns into new eval cases, because every production failure is a candidate for your eval suite. Finally, **improve** by hillclimbing against your updated eval suite, shipping the improvement, and repeating. This cycle accelerates over time. More production data feeds better evals, which drive better AI, which creates a better product, which attracts more people and generates more production data.

### Three types of eval judges

- Different eval criteria call for different measurement approaches. There are three types of judges, and knowing when to use each one matters.
- **Algorithmic judges** handle quantitative, deterministic checks like string matching, format validation, and length constraints. These are fast, cheap, and perfectly reliable.
- **AI judges** handle fuzzy quality assessments where you have clear golden examples, evaluating subjective dimensions like tone, helpfulness, and coherence. They scale instantly but require calibration against human judgment to be trustworthy.
- **AI judges with human alignment** handle deeply subjective evaluations where human review provides the ground truth and the AI judge learns to approximate it. These are deceptively hard to get right, but they're the only way to handle complex quality dimensions where reasonable people might disagree.
