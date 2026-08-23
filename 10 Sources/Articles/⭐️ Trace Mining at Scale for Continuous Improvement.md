---
type: article
status: raw
quality: 1
topics: [error-analysis, ai-engineering, agent-evaluation]
source: https://www.braintrust.dev/blog/topics-architecture
created: 2026-08-22
published: 2026-06-04
author: Braintrust Team
flashcards: none
updated: 2026-08-23
---

# Trace Mining at Scale for Continuous Improvement

- If you run an agent in production, some part of your day is probably going through the countless production logs to see if anything looks interesting
- Topics is the solution that lets you analyze traces with intelligence at scale
    - In order to find patterns you didn't know to look for, you need to run this intelligence layer over every trace. We call this [active observability](https://www.braintrust.dev/blog/active-observability)
    - The job is to distill it down to the handful of things worth looking at
- The standard NLP toolkit assumes documents that are roughly uniform in shape and size.
    - Topic modeling with LDA wants bag-of-words documents in the hundreds of tokens.
    - Sentiment analysis wants a sentence or a paragraph.
    - Off-the-shelf clustering on embeddings wants inputs that fit inside an embedding model's context window, which today caps out around 8,192 tokens.
- Agent traces don't look like that.
    - A single production trace can be millions of tokens of conversation history, tool calls, intermediate reasoning, retrieved context, and serialized application state.
    - They arrive at high volume, they keep updating after they're "done," and the interesting signal is usually buried in a few spans out of hundreds.
    - If you embed the raw trace, you get noisy clusters dominated by surface features like message length or tool name frequency.
    - If you summarize first with an LLM, you blow your budget.
    - If you sample aggressively, you miss the long tail, which is where the bugs usually live.
- There's also a methodology problem.
    - Teams want to ask three different questions of the same logs: what kinds of requests are coming in, what's going wrong, and how do users feel about the responses?
    - Those are usually three different stacks. Topic modeling for the first, error mining or anomaly detection for the second, and sentiment analysis for the third.
    - Maintaining three pipelines, each with its own preprocessing and its own failure modes, is not a great use of an applied AI team's time.
- The insight that drove Topics is inspired by Anthropic's [Clio paper](https://arxiv.org/abs/2412.13678).
    - Instead of trying to embed or classify the raw trace, you ask an LLM to do one job, which is to summarize the trace along a single dimension in a sentence or two.
    - Then you embed that summary, cluster the embeddings, and name the clusters with a second LLM pass.
    - The trace itself never has to fit in an embedding model's context window.
    - The downstream pipeline never has to know anything about agents or tools or token counts.
- This sounds like a small move and architecturally it is. Operationally it changes everything.
    - Once the LLM summary step exists, the same downstream pipeline works for any dimension you care about.
    - Task, issues, sentiment, custom categories you define for your product, all flow through the same embed, cluster, name, classify stages.
- The expensive part of the pipeline is the LLM summary. Everything downstream is cheap
    - So as long as you do the summary well and only once per trace, you can run classification continuously on every new trace without breaking the bank.
- These two observations, summarize-then-embed and unified downstream pipeline, are the architectural bet behind Topics.
- Three design goals fall out of that bet.
    - First, the LLM summary step has to be tightly scoped, batch-friendly, and cheap enough to run on every trace. The output of that step is a **facet**, and it's the unit of work the whole pipeline is built around.
    - Second, the cluster generation step has to be fast enough to run ad hoc without operator intervention, and the resulting topic map has to be stable enough that trend analysis across runs is meaningful. Generative naming will always drift between runs, so the persistent unit of identity is the cluster, not the name.
    - Third, classification has to be cheap enough to run continuously. That means no LLM call at classification time. The only operation is an embedding lookup against the saved topic map's centroids, which we can do in roughly 100 milliseconds per trace.

![](https://www.braintrust.dev/blog/img/topics-architecture/pipeline.png)

- The preprocessor turns a raw trace into tokens
    - This stage exists for one reason. Raw traces can be enormous, and the facet model has a finite context window.
    - Preprocessing typically runs in well under a second per trace, and the output is hard-capped at 128K tokens before it ever reaches the facet model
    - Clio summarizes conversations that already arrive in a roughly uniform shape, while we have to turn arbitrary, sprawling agent traces into something a single LLM pass can handle.
- The facet stage is where the LLM does its one job.
    - Each facet has a prompt, like "summarize what the user is trying to accomplish in one sentence," and an output schema.
    - The facet model produces a short text blob, typically a sentence or two
    - The built-in facets are Task, Sentiment, and Issue
- After the facet text is produced, we embed it with our embedding model, also served on Baseten. The output is a 1024-dimensional dense vector.
    - The thing to notice here is what we're embedding. It's the facet output, not the raw trace.
    - That's what makes the rest of the pipeline tractable.
    - A consistent, short, on-topic summary embeds cleanly. A million-token agent trace does not.
- Once enough facet embeddings have accumulated, the clustering stage runs on a sample of up to 50,000 facets per generation pass
    - The default algorithm is HDBSCAN with UMAP for dimensionality reduction. K-Means and Hierarchical are available as alternative clustering algorithms, and PCA is available as an alternative dimensionality reduction.
    - We picked HDBSCAN as the default for two reasons.
        1. It doesn't require you to pick the number of clusters up front, which matters because the right number of topics is a function of your data and changes over time.
        2. And it naturally identifies outliers as noise rather than forcing every point into a cluster, which lines up with the way real traffic distributes, namely a long tail of one-off requests around a small number of recurring patterns.
    - For keyword extraction per cluster we use c-TF-IDF, which is the same approach BERTopic popularized. A generation pass over thousands of traces completes in roughly 30 seconds
- The naming stage takes the representative facet exemplars for each cluster and asks an LLM to produce a short name and description.
    - This is generative, which means the same cluster can pick up a slightly different name on the next generation pass even if the underlying membership barely changes.
    - One of the big learnings was that you have to use a large model and name multiple clusters simultaneously, otherwise the names are not very discriminative.
    - That's why we treat the cluster, not the name, as the stable identity.
    - When a new topic map is generated, we automatically match similar clusters to their predecessors and reuse their ids.

![](https://www.braintrust.dev/blog/img/topics-architecture/topic-map.png)

- Classification is the cheap part.
    - For each new trace, we run the preprocess, facet, and embed stages, then look up the nearest cluster centroid in the saved topic map.
    - If the trace is within the configured distance threshold, it gets a label. If it's not, we write `no_match` instead of forcing a bad label.
- There are two thresholds worth knowing about.
    - You need at least 400 traces in a project for Topics to start, and at least 100 unique facet summaries before it will generate a topic map.
    - Below those numbers, the clusters aren't meaningful and we'd rather show you nothing than show you noise.
- The Topics view shows the automated topic map.
    - The same persistent set of clusters, the same names, applied consistently to your logs over time.
    - This is what you want for trend dashboards, alerting, and any analysis that needs to be comparable across days or weeks.
- The "Cluster traces by facet" action on a filtered view runs ad-hoc clustering on whatever subset you're currently looking at, with parameters tuned for exploration.
    - The clusters you get are specific to that slice. Run it on yesterday's failures, on a specific user cohort, on a single experiment.
    - This is what you want when you're investigating, not monitoring.
- Identity stays stable across regenerations.
    - Topic maps regenerate, names drift, but the underlying cluster identity is matched across runs so your dashboards and saved queries keep working.
    - The thing you depend on, the cluster, is stable. The thing that can drift, the name, is treated as a label.
