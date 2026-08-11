---
type: article
status: raw
quality: 1
topics: [career-development, error-analysis, learning-science]
source: https://x.com/itsreallyvivek/status/2064686372737454155/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-06-10
author: Vivek
flashcards: none
updated: 2026-08-11
---

# how to be good at research

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2061456169491951616/MktnuLGE.jpg" width="220" />
</div>


### pick your own problems

- richard hamming had a habit at bell labs that made him unpopular at lunch. he'd ask whoever sat near him what the important problems in their field were, then ask why they weren't working on them. people changed tables. the question stings because most of us have no good answer. we don't choose problems, we absorb them, from an advisor, from whatever a big lab announced last quarter, from the paper everyone is quote-tweeting
- the trouble with an absorbed problem is that you hold the conclusion without the reasoning. you know some famous lab cares about a direction, but not why
- john schulman's guide to ml research splits the work into two modes. in one, you read the literature and hunt for things to improve. in the other, you choose an outcome you genuinely want to exist and reason backwards to the experiments
- taste, meanwhile, gets discussed like a gift. it behaves more like a muscle. predict the result of every experiment before you run it

### upgrade your inputs

- shared reading lists produce shared ideas
- old material is criminally underpriced. this field reruns its own past on a delay: mixture of experts dates to 1991, lstms to 1997, backprop went mainstream in 1986. rich sutton needed about a thousand words in 2019 to write the bitter lesson, and it predicts the shape of the field better than surveys ten times its length
- range matters as much as depth. interpretability borrows shamelessly from neuroscience. eval design is mechanism design wearing a lab coat
- one more thing. read the paper itself, not the thread summarizing it

### write everything down

- paul graham points out that an idea can feel fully formed right up until you try to put it into words. the page finds gaps your head papers over: the assumption you never tested, the step that doesn't actually follow, the two claims that quietly contradict each other.
- feynman's rule was that the first person you must avoid fooling is yourself, because you're the easiest target. writing is the cheapest defense ever invented.

### tighten the loop

- the stories about alec radford rarely involve a single stroke of genius. they involve volume. more runs per day, more wrong ideas discarded per week, a model of reality that updated faster than anyone else's. that's the actual game. research speed is mostly the speed at which you discover you're wrong.
- which makes tooling a first-class research activity. launching a run should be one command. plotting it should be one more. every experiment should be reproducible from its config, and comparing two runs should take seconds

### stare at the outputs

- a descending loss curve is not analysis, it's reassurance. your experiments throw off far more information than you consume: transcripts, failure cases, the strange tail of the distribution. most of it dies unread in a logs folder.
- andrew ng has taught the same unglamorous move for over a decade because nothing beats it. pull a hundred failures, read all of them, sort them into piles, attack the biggest pile

### wander on purpose

- somewhere in this field is a corner where your specific weirdness is an unfair advantage, and the only way to locate it is to pay tuition in several places. nobody waives the tuition.

### find your people

- hamming noticed a pattern in who ended up doing important work. colleagues with closed office doors got more done in any given year, and colleagues with open doors did the work that mattered, because the interruptions carried information about what the world actually needed. your open door is probably an inbox. keep it that way.
