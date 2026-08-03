---
type: article
status: structured
quality:
topics: [data-science]
source: ""
created: 2026-07-05
published:
author: ""
flashcards: none
updated: 2026-07-05
---
A **Markov chain** is a way of modelling a system that moves between different **states**, where the next state depends only on the **current state**, not the full history of how it got there.

The core idea is:

> **Given where you are now, the past no longer matters for predicting what happens next.**

This is called the **Markov property**.

Mathematically, it is often written as:

$P(X_{t+1} \mid X_t, X_{t-1}, X_{t-2}, \dots) = P(X_{t+1} \mid X_t)$

Meaning:

> The probability of the next state depends only on the current state.

## Simple example

Imagine the weather can be one of three states:
- Sunny
- Cloudy
- Rainy
A Markov chain might say:
If today is **Sunny**:
- 70% chance tomorrow is Sunny
- 20% chance tomorrow is Cloudy
- 10% chance tomorrow is Rainy
If today is **Rainy**:
- 30% chance tomorrow is Sunny
- 30% chance tomorrow is Cloudy
- 40% chance tomorrow is Rainy

The model does **not** care whether it was sunny three days ago, raining last week, or cloudy yesterday except insofar as that history has led to the current state.

So the logic is:

> Today’s weather is enough information to estimate tomorrow’s weather.

That is the Markov chain idea.

## Why people describe it differently

People describe Markov chains in different ways because they appear in different fields.

A beginner-friendly way:

> A Markov chain is a probability-based flow between possible states.

A technical way:

> A Markov chain is a stochastic process where future state probabilities depend only on the present state.

A decision-tree-ish way:

> It is like a branching path where each branch has probabilities attached, and every step depends only on the current node.

That last explanation is not wrong, but it can be misleading.

A **decision tree** usually branches outward and often represents a fixed sequence of choices or outcomes. A **Markov chain** usually allows the system to move around repeatedly between the same set of states over time.

For example:

```text
Sunny → Sunny → Cloudy → Rainy → Cloudy → Sunny
```

The system keeps transitioning between states. It is not just a one-way tree.

## The most generally useful definition

The best general definition is:

> A Markov chain is a model of a system that changes state over time, where each next state is chosen probabilistically based only on the current state.

The essential components are:
1. **States**
    The possible conditions the system can be in.
    Example: Sunny, Cloudy, Rainy.
2. **Transitions**
    The movement from one state to another.
    Example: Sunny → Rainy.
3. **Transition probabilities**
    The probability of each possible next state.
    Example: If Sunny today, there is a 10% chance of Rainy tomorrow.
4. **Memorylessness**
    The next step depends only on the current state, not the entire past.

## Another intuitive example
Imagine someone’s mood can be:
- Happy
- Neutral
- Sad
If they are currently **Happy**, maybe tomorrow they are likely to stay Happy.
If they are currently **Sad**, maybe tomorrow they have a higher chance of staying Sad or becoming Neutral.
A Markov chain models the probability of moving between these states.

It does **not** ask:

> What happened every day for the last month?

It asks:

> What state are they in now, and what are the probabilities of moving from here?

## Why it matters

Markov chains are useful when you want to model systems that evolve over time, especially when the future is uncertain but somewhat predictable from the present.

They are used in:
- weather modelling
- finance
- queueing systems
- board games
- search engines
- genetics
- reinforcement learning
- language modelling
- customer behaviour
- disease progression models
    

For example, in a health context, you could model a patient as moving between states such as:

```text
Healthy → Mild disease → Severe disease → Recovery
```

Each transition has probabilities attached.

## Important distinction: Markov chain vs Markov decision process

This is probably where some of the confusion comes from.

A **Markov chain** usually describes a system where transitions happen according to fixed probabilities.

A **Markov decision process** includes **actions or decisions**.

So:

```text
Markov chain:
Current state → probabilistic next state
```

```text
Markov decision process:
Current state + chosen action → probabilistic next state + reward
```

So when people describe Markov chains as a “decision-making framework”, they may actually be talking about **Markov decision processes**, which are common in reinforcement learning.

## The simplest mental model

Think of a Markov chain as:

> A map of possible states, with probability arrows between them, where the next step only depends on where you are now.

Example:

```text
      0.7
Sunny ───→ Sunny

Sunny ───→ Cloudy
      0.2

Sunny ───→ Rainy
      0.1
```

Every state has outgoing probabilities to the next possible states.

## Bottom line

A **Markov chain** is not just a decision tree, and it is not necessarily a decision-making model.

It is best understood as:

> A probabilistic state-transition model with limited memory.

Or even simpler:

> A model where the future depends on the present state, not the full past.