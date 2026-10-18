---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/lotte_verheyden/status/2100284020831752570?reader-ingest=20261018
created: 2026-10-18
published: 2026-09-16
author: Lotte Verheyden
flashcards: none
updated: 2026-10-18
---

# Your users are already evaluating your AI

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article3.5c705a01b476.png" width="220" />
</div>

- users have 2 choices:
    - set up [online evaluators](https://langfuse.com/academy/evaluate) that measure specific aspects of a trace
    - capture [signals of judgment from your users](https://langfuse.com/docs/observability/features/user-feedback)
- This article talks about the latter
- Unlike traditional online evaluation, capturing signals does not directly evaluate the quality of the agent's work. Instead, it captures things a user did or said that indicate whether the user perceives the agent's work as good or bad: a thumbs down, a retry, a request for a human, etc.
- Signals measure perceived quality at the moment of use.

### Why this is important

- This is a **cheap and scalable way to get quality judgments on production traffic**, compared to other methods such as experts annotating traces (human time) or online LLM-as-a-judge evaluators (LLM cost). Your users judge every output anyway, through what they do next, so you just need to instrument your application to catch these signals.
- While through traditional evaluation you encode what you believe is important, user signals will also **surface behaviors you didn't anticipate but might be worth taking a look at**

![](https://pbs.twimg.com/media/HSWwifyakAAnQ7P.jpg)


### Four kinds of signals


#### Explicit ratings

- Explicit ratings are the only signals where the **user knowingly grades the output**, which makes them unambiguous, but also rare. Explicit rating signal Thumbs up/down reactions Star rating/CSAT question at the end of a conversation Written comment attached to a rating Reason picker on thumbs down (wrong, unsafe, ignored instructions) Choice between two regenerated answers Report or flag button
- *[In Meta's production assistant](https://arxiv.org/abs/2505.14946)**, about 0.1% of model messages receive a positive emoji reaction, and the ratings that do arrive are* *[skewed toward users with strong reactions](https://langfuse.com/academy/monitoring/capturing-signals#biases)**.*

#### Behavioral signals

- Behavioral signals are **actions users take on the output**: accepting, copying, editing, regenerating, skipping, abandoning. They occur inside the normal workflow, so coverage is high: on a copilot-style product, every suggestion produces one.
- Behavioral signalUser regenerates a responseUser stops generation mid-streamUser copies the responseUser clicks a cited sourceUser switches model and retriesSuggestion is acceptedSuggestion is accepted, then undone within secondsSuggestion is dismissed by continuing to typeDraft is inserted into the documentDraft is discardedAI feature is turned off while usage continuesUser interrupts the agent mid-sentence

#### Conversation signals

- In a conversational product, the **user's next message often tells you what they thought of the agent's output**: a rephrased question, a correction, a request for a human, or a *thank you* all say something about the quality of the output they received.
- Conversation signalUser rephrases the same questionUser corrects the agent ("no, I meant the March invoice")User asks for a humanUser repeats an instruction the agent already received, or says "try again"User quotes an error back ("you said X, but...")User expresses frustration ("this is useless", "you are not listening")User confirms success or thanks the agent
- *[Amazon used rephrase and follow-up patterns](https://arxiv.org/abs/2010.12251)* *to curate training data for Alexa's language understanding from live traffic.* *[Microsoft's SPUR goes a step further](https://arxiv.org/abs/2403.12388)**: an LLM learns satisfaction and dissatisfaction patterns from the small slice of thumbs-labeled conversations, condenses them into a rubric, and scores the unlabeled majority with it.*

#### Outcome signals

- Outcome signals tell you what the environment did with the output: a draft was sent unedited, a ticket was closed, etc. **They are the strongest kind because they are grounded in the environment rather than in someone's opinion.**
- also often the most complex to implement.
- Outcome signalDiff between a drafted reply and what was actually sent, classified as none, tone, corrected, or addedExtracted field is corrected in a downstream approval stepSupport ticket stays closed, or reopens within daysEscalated conversation is resolved quickly by a humanAccepted code is still present at commit timeAgent's pull request is merged, closed, or reverted

### How to interpret signals

- Once relevant signals are implemented, you can look at your traces as labeled for that signal: labeled negative, labeled positive, or unlabeled.
- GroupWhat to do with itLabeled negativeLook at each trace individually to debug and decide if something needs fixing.Labeled positiveFocus on the trend instead of single events.UnlabeledTreat this as missing data (don't do anything with it based on this).
- Which polarity is dense depends on the channel. Thumbs may skew positive while conversation signals tend to skew negative, for example.
- **A negative is close to a confirmed bad experience.** Users rarely retry or correct an answer they liked. Each trace with a negative user signal is worth opening, and negatives are the natural entry points for [error analysis](https://langfuse.com/academy/monitoring/error-analysis).
- **A positive signal shows acceptance, but not necessarily quality.** Read positives as a trend, and never make one the [optimization target](https://langfuse.com/academy/monitoring/capturing-signals#which-signal) on its own.

#### Who labels is not random

- Signals can be very useful, but you should also watch out for inherent biases. Often, you won't get a signal from the entire population of users
- You can split these kinds of biases into:
    - **Self-selection.** People rate what they feel strongly about. [When Yahoo! Music surveyed its listeners](https://arxiv.org/abs/1206.5267), 65% said their opinion of a song decides whether they rate it at all, and songs they loved or hated were rated far more often than songs they felt neutral about.
    - **Survivorship.** All your signals are from users who stayed long enough to take the action you're tracking. Keep in mind that it's likely not the full set of users that started an interaction.
    - **Exposure and interface.** Users react only to what the system shows, in the form it is shown. [For example](https://www.cs.cornell.edu/~tj/publications/joachims_etal_05a.pdf), search users will keep clicking top-ranked results disproportionately regardless of whether they are the most relevant for their use case.
    - **Cohorts.** Signal rates vary across users, languages, and time of day without the quality of the output changing.

#### Which signal should you optimize for?

- Signals are slightly different from explicit metrics and quality evaluators. Don't replace your [goal metrics](https://langfuse.com/academy/evaluate/choosing-what-to-evaluate) purely with signals. As for what to optimize for, prefer signals closest to what the product is for. Otherwise you might start optimizing for behavior you don't want.
- Two examples of this:
    - [YouTube ranked recommendations](https://dl.acm.org/doi/10.1145/2959100.2959190) by clicks and got clickbait; ranking by expected watch time fixed it, because watch time is closer to what the product is for.
    - [When OpenAI added a reward signal built from ChatGPT thumbs data](https://openai.com/index/expanding-on-sycophancy/), the model turned sycophantic: user feedback favored agreeable answers and weakened the signal that had been holding sycophancy in check, while offline evaluations and A/B tests looked fine and only expert testers noticed the model felt off.

### What comes next

- Once signals land as scores on your traces, put them to work in four places:
    - Set up [alerts](https://langfuse.com/docs/observability/features/alerts) on the signals that mark a bad experience, so that a spike in them reaches you right away.
    - Create filtered views of negatively labeled traces, so that you can go through them frequently.
    - Add graphs of signal rates to your [dashboards](https://langfuse.com/docs/metrics/features/custom-dashboards) to track how they develop over time.
    - When reviewing flagged traces, use them: run [error analysis](https://langfuse.com/academy/monitoring/error-analysis) on them and add them to [datasets](https://langfuse.com/academy/datasets).
