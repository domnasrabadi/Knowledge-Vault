---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/vtrivedy10/status/2066571435871551655/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-06-15
author: Viv
flashcards: none
updated: 2026-08-08
---

# Building a 100x Cheaper Trace Judge with Fireworks

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1805079750873923584/7sTh63Eo.jpg" width="220" />
</div>

- LangSmith processes billions of tokens a day across production traces. One of our core challenges is efficiently mining signals across these traces
- We partnered with Fireworks to build an efficient Trace Judge. We fine-tuned a Qwen model to detect “Perceived Error” on every production trace. It matched or exceeded frontier model performance and runs up to **100x cheaper.**
- As more agents move into production, [traces](https://docs.langchain.com/langsmith/observability-concepts#traces) will become more important as one of the richest sources of data to understand how agentic systems behave with real users.
- how can we **cost-effectively** mine important signals from every single trace, while maintaining **frontier performance**?
- Perceived error is when the user thinks the assistant made a mistake or produced something that needed correction. Perceived Error **is not** judging objective correctness or user happiness
- We usually push for teams to build application specific evaluators, as often the logic to judge a trace needs to have context of that application. We believe, however, that “perceived error” is an example of an evaluator that can be general purpose. We believe the signals that it will look for are universal across applications.
- We infer perceived error from trace signals like user corrections, rejection of an agent action, repeated requests, and assistant acknowledgements of errors. The perceived error evaluator then enriches the trace with information in the format shown below:

### How we created a dataset

- We selected a portion of traces from each tracing dataset as training and holdout sets. When filtering from the pool of traces, we selected multi-turn traces because judging “perceived error” requires a human response to the AI results (for example, correcting the assistant or repeating the request).

### Data Preparation

- we made the choice to only include Human and AI messages, ignoring all tool calls. We did this because we hypothesized that for the signals we were looking for the human and AI messages are the main source of information

### Labels

- To generate labels, we used a mix of model-assisted labeling plus human review to create short JSON labels and rationales for each trace. Specifically, we first asked a panel of models to judge a trace. If they all agreed, we took that as a ground truth label. If they disagreed, we then took all their labels and rationales and passed them to another panel of models, asking them to judge who was right. If that panel agreed, we took that as ground truth. If they still disagreed, we human annotated them manually

### Experiments & results

- We organized experiments around three questions: 1. Does fine-tuning improve baseline judge quality up to frontier model performance? 2. Does a learned judge transfer across datasets? 3. Is serving a fine-tuned model cost-effective? **Fine-tuning open models can exceed or match frontier models**
- A fine-tuned judge transfers well to unseen data
