---
type: book
status: inbox
quality: 1
topics: []
source: private://read/01m0kpdf0n35wyegamkf0y4gcb
created: 2026-08-22
published: 2026-04-21
author: Ozzie Kirkby, Andy Matuschak
flashcards: none
updated: 2026-08-22
---

# LLM-Based Automation of Spaced Repetition Prompt Generation from Reading Highlights

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/489237453/GXyRi7CvIPrt5ewbwoPWVyIXlFuQ3zzAlEm1R-bpwOY-file_hnHRQ3c.jpg" width="220" />
</div>


## Memory Machines

- Can LLMs create lasting flashcards from readers' highlights?
- Spaced repetition memory systems [make memory a choice](https://augmentingcognition.com/ltm.html)—but only if you write practice prompts that effectively reinforce those ideas
- We explored whether LLMs could convert casual highlights into useful memory prompts.
- Here’s an example. In an article on terraforming, one of us highlighted this passage about Titan: > … gravity is so low that humans could fly simply by flapping their arms, provided they’re equipped with winged space suits. [“Greening the Solar System”](https://asteriskmag.com/issues/09/greening-the-solar-system), *Asterisk* This is exactly the kind of striking detail we want to carry away from an article like this. Yet without reinforcement, we expect we’d soon forget it. When given the full source text and our highlight, frontier models generate flashcards like: > **Q.** On which celestial body could humans theoretically fly by flapping their arms? > > → Question reveals the detail I want to reinforce > **Q.** Why could humans fly on Titan using only winged space suits? > > → Not trying to reinforce gravitational mechanics > **Q.** What makes Titan unique in terms of human flight potential? > > → Will be ambiguous in a few months, and factually wrong (it's not unique)
- These are directionally correct! They are about Titan, about flying, about the highlighted text. But they miss what’s most interesting about the passage. Here’s a prompt that works: > **Q.** On Titan, gravity is so low that humans could fly simply by... > > **A.** ...flapping their arms (in winged space suits)
- We tried to transfer that taste to LLMs through instructions, rubrics, few-shot examples, and training on ~1,500 labeled prompts across 93 sources. We find that models can identify a highlight’s intent, but not whether a prompt will hold up over months of review.

### 1. A Problem with Two Parts


### 1. A Problem with Two Parts


#### Memory Prompts Are Not Flashcards


#### Memory Prompts Are Not Flashcards

- Memory systems—also called spaced repetition systems, or SRS—work by causing you to retrieve a memory near the moment you’re about to forget it
- **A SRS memory prompt must survive a long-horizon review**. A prompt seen today, then again in three months, then again in a year, must reliably cue the same answer each time
- If context is underspecified or the question does not solicit consistent recall of the same detail, recall drifts and the testing effect breaks down.
- A good memory prompt lives in a narrow band. It must be concise enough to read quickly, but detailed enough to cue the same memory months later—yet not so detailed that the question gives away the answer
- Attempting to proceduralize and describe the process of writing good memory prompts is challenging since so much of the knowledge comes from **lived experience**. You learn what works by experiencing what fails. A prompt often seems fine initially, but weeks later forgetting exposes its weaknesses. Forgetting is the feedback which shapes taste.
- When this taste lives entirely in the human, two structural bottlenecks of memory systems appear:
- **Stasis.** Prompts are always the same
- reviews become mechanical
- **Demand.** Writing good prompts takes effort that curiosity can only sometimes justify
- Only a narrow slice of what interests you ever enters the system.
- We could address these bottlenecks by bringing machines into the loop, but only if the prompts they generate survive long-horizon review. We test whether they can, in a minimal setting: highlights from casual reading. You’re interested enough to mark a passage, but not enough to write a memory prompt for it.

#### Grounding the Problem


#### Grounding the Problem

- Before turning to generation, we first needed to check a more basic assumption: can highlights capture what readers want to remember?
- We tested this with 42 experienced memory system users. Each participant read one of three articles, using a digital highlighter to emphasize any passages they found interesting. Afterward, to obtain their preferences directly, we asked them to choose which of 10-13 predefined interests they’d like included in a downloadable set of memory prompts.
- As a naïve baseline, we could skip the highlighting and interest selection. We could just provide memory prompts about every topic in the article—the same prompts for everyone
- But many memory system users feel these collections fit them poorly, and our data validate that. Our average participant would need to delete more than a third of those prompts to match their interest selections.
- That’s not because the prompts are poorly chosen in general. Readers simply care about different details
- The question, then, is whether we can infer what a *particular* reader cared to remember from their highlights. A simple test here produced promising results. Before running the experiment, we mapped each candidate interest to a representative passage in the text. If we predict a user’s interest selections by intersecting those pre-mapped passages with their highlights, we cut the average participant’s unwanted prompts in half, relative to the naïve baseline.
- It seems that highlights can provide a strong signal of readers’ interests. The difficulty now is translating that signal into prompts that will reliably cue the same memory after time has passed.

#### What Makes a Memory Prompt Work


#### What Makes a Memory Prompt Work

- Effective memory prompts satisfy two criteria simultaneously:
    - **Targeting:** whether the prompt captures what the user actually wants to remember.
    - **Construction:** whether the prompt will reliably cue the same memory after long gaps, without significant loss in detail.
- A prompt can fail on either axis
- You read the prompt and immediately recognize that it’s about the wrong thing, or about something you don’t care to retain. Construction failures are harder to see. They often surface during review, when ambiguity, underspecification, and excess abstraction can cause friction and forgetting.
- Construction failures are expensive. They look plausible, so you read them carefully, attempt an answer, and only later discover that the prompt doesn’t support stable recall. Repeated over time, these prompts erode trust in the system.
- To reason about this systematically, we adopted a four-tier taxonomy: > **T3 —** Ready to Review > > **Q.** On Titan, gravity is so low that humans could fly simply by... > > **A.** ...flapping their arms (in winged space suits) > **T2 —** Needs Polish > > **Q.** What fanciful superpower would humans acquire on Titan as a consequence of its low gravity? > > **A.** Humans could fly by flapping their arms, provided they're equipped with winged space suits. > > → Good targeting, but wordy enough to cause friction > **T1 —** Needs Refactor > > **Q.** How does Titan's low gravity and dense atmosphere affect how a human could move there? > > → Decent targeting, but unworkably ambiguous construction (many correct answers possible) > **T0 —** Off-target > > **Q.** What two properties of Titan allow flight? > > **A.** Low gravity and dense atmosphere. > > → Targets the wrong detail, and with ambiguous construction
- T0 prompts are cheap, quickly discernable failures, but T1 prompts are insidious. They look plausible—often even aligned with what you want—but won’t reliably survive long-horizon review.
- A good prompt has to preserve what made the detail worth marking—the novelty, the feeling, the specific angle that struck you—without flattening it into generic trivia. At the same time, it has to be precise enough to cue the same answer months later. Most failures give up one side or the other.
- When an experienced memory system user evaluates a prompt, they draw on thousands of past reviews. They *project themselves forward in time*, into future review sessions, and assess how they’d react to a given prompt. Is it still clear, vivid? Does it still cue the same memory? This is what we call taste! Deploying it is cognitively demanding and rests on the lived experience of spaced repetition usage.

### 2. Models Can’t Judge Quality


### 2. Models Can’t Judge Quality


#### Binary Classification

- One of the simplest tests: can models tell usable prompts from unusable ones? We collapsed the four tiers into a binary decision we call **pluckability**. A prompt is *pluckable* if it would hold up over time in a memory system—T2 or T3. Prompts rated T0 or T1 are *unpluckable*: they’re either off-target or broken in ways that won’t survive long-horizon review.

#### Rubric

- Maybe the model can’t learn the holistic notion of “pluckability,” but it can detect specific failure modes. This is the standard “LLM-as-a-judge” playbook: turn taste into a checklist, then ask the model to apply each item.
- **Lacks Context** *Before* > **Q.** What does excise involve? > > **A.** Effort not directly in pursuit of a goal. *After* > **Q.** What is excise according to Alan Cooper? > > **A.** A cognitive or physical penalty for using a tool. "Excise" means different things in different contexts.
- **Solicits multiple responses** *Before* > **Q.** What causes internal fragmentation in LLM memory allocation? *After* > **Q.** What distinguishes internal fragmentation from external fragmentation in KV cache memory? This has many valid explanations.
- **Shallow** *Before* > **Q.** What are the “factors of production” that economists often discuss? > > **A.** Labor, land, and capital. *After* > **Q.** What does it mean when there are “diminishing marginal returns to labor/land/capital”? > > **A.** These factors are not the limiting factor in production; a 10× increase in capacity yields minimal returns. Asks for a textbook list; the passage’s main insight is about diminishing marginal returns.
- **Wordy** *Before* > **Q.** How does the Stoic philosophy, as summarized by Marcus Aurelius, view obstacles in relation to personal growth and progress? *After* > **Q.** How does Marcus Aurelius’s Stoic philosophy view obstacles? Same question buried under formal qualifiers.
- **Narrow** *Before* > **Q.** What is a common mistake made by AI researchers? > > **A.** They often try to build knowledge into their agents. *After* > **Q.** What is Rich Sutton’s Bitter Lesson (2019)? > > **A.** Human-designed knowledge may offer short-term gains, but scalable methods that rely on computation and general learning algorithms consistently outperform. Captures only the setup (researchers build in knowledge) while missing the main point: that computation dominates human design in the long run. (Separately, this question is vague and will solicit multiple responses)

#### Preference Selection

- If absolute judgment is too hard, maybe relative judgment is easier. We reformulated the task contrastively: for a given highlight, we provided **2–4 candidate prompts** (one T3, the others T1/T2) and asked the model to pick the best one
- Yet models fail to identify it reliably. Models chose the T3 prompt only **~40–50%** of the time. Worse, models pick **T1**—the tier we most want to reject—**~30–40%** of the time

#### Taste Doesn’t Transfer

- We find that models reliably reject T0 prompts. For both language models and human reviewers, off-target prompts are cheap failures: you read them and immediately recognize them as poor fits. The T1/T2 boundary is different. For humans, distinguishing those tiers takes careful reading and judgment formed through thousands of reviews—the accumulated sense of which prompts drift and which hold. Across all our experiments, models failed to reliably distinguish those tiers.

### 3. Training Doesn’t Break Through


### 3. Training Doesn’t Break Through

- If describing taste doesn’t work, maybe we can train it. We have ~1,500 labeled samples—not enormous, but enough to ask whether there’s a learnable signal in this data

#### Matching the Ceiling, but Not Breaking It

- **Training bought efficiency, not capability**. We got cheaper judges, not better ones.

#### Preference Learning Hit the Same Wall


#### Preference Learning Hit the Same Wall

- Our tier structure implies a natural preference ordering, T3 > T2 > T1 > T0, and reward models are explicitly designed to learn this kind of signal. Rather than drawing a hard boundary, they learn to score better options higher than worse ones
- On targeting comparisons, T0 against anything above it, accuracy reached 77%. The reward model reliably learned to prefer prompts that are about the right thing. But on construction comparisons, accuracy dropped to 62%. Supervision reliably captured targeting preferences, but not our taste in construction.

#### Why Reinforcement Learning Doesn’t Save Us


#### Memory Prompt Data Is Expensive

- **Labeling requires simulation, not recognition**. A rater must understand the source material, infer what the highlight signaled as interesting, and then simulate how that prompt would feel to review over time. Construction quality isn’t a surface property. It depends on anticipating ambiguity, drift, and loss of salience across repeated encounters.
- **Review signals are confounded.** Another approach: skip labeling and infer quality from actual review behavior. Leeches (prompts that never stabilize) might indicate construction problems; abandoned prompts might indicate poor targeting. But in our setting, each user creates prompts from different articles. A prompt may be abandoned because it is poorly constructed, or simply because their interest waned.
- **Preferences capture “least wrong,” not “right.”** When choosing between memory prompts, users rarely have a fully specified objective: they’re often reaching for a particular detail or framing they recognize but can’t crisply articulate. Faced with two imperfect options, they select the one that misses by less. The preference signal encodes proximity to an unstated goal, not satisfaction of it. What the user actually wanted appears nowhere in the data.

### 4. Escaping Transfer with Grounding


### 4. Escaping Transfer with Grounding

- Training hit the same ceiling as prompting. Neither approach taught the T1/T2 boundary
- So we changed the question. Instead of asking whether a prompt satisfies a theory of “good prompts,” we can ask how it compares to other prompts for the **same highlight**
- We asked the grounded judge to predict the full four-tier rating, then collapsed its predictions into **pluckability** (i.e. T2/T3 vs. T0/T1). This let us test both whether grounding improves fine-grained discrimination, and also whether those improvements translated into better separation at the boundary that actually matters. > Krumdick et al. use the same strategy: grounding LLM judges with human-written references rather than asking them to evaluate in isolation.
- They did—but with a tradeoff. Using Sonnet 4.5, overall tier accuracy rose from 39% to 49% when grounded. More importantly, **pluckability precision jumped from 56% to 78%, and false positives dropped from 52% to 17%**. The judge became conservative: it approved fewer prompts, but the ones it approved were far more likely to be genuinely usable
- The confusion matrix makes the shift visible. The T1/T2 boundary remains imperfect, but the diagonal sharpens rather than collapses

![](https://readwise.io/reader/pcei/gAAAAABqiRARZhA9PlHJCP1_-11-ZtklABSClC-GovhChYG_48fhVeqk-_v-nc5geAzCR5O_tA7beUsgAwt7hs0rGR2iureoNj1NZyikiGugqwX-bDrtKIo=/file5.png)

- With grounding, models no longer need to learn what makes a prompt good in general. They only have to compare candidates within a local context. Instead of transferring our taste, we encode it in the labeled examples. This approach gives us an evaluation framework that roughly preserves our preferences while we change models, instructions, and other variables.

### 5. How Bad Is Generation?


### 5. How Bad Is Generation?

- **how bad are LLMs at generating prompts?**
- However, even the strongest model we tested (GPT-5.2) still produces **unusable prompts roughly a third of the time.**

### 6. The Arena


### 6. The Arena


#### Cost-Sensitive Scoring


#### Cost-Sensitive Scoring

- To compare pipelines rather than individual prompts, we need a scoring function that accounts for the full set of outputs a model produces—rewarding good prompts while penalizing the burden imposed by the rest.

#### Results


### Conclusion


### Conclusion

- Within our dataset of ~1500 memory prompts, we found that models are generally good at detecting off-target prompts. Targeting largely transfers
- But the highest-ranking model we tested, GPT-5.2, still generates unusable prompts 36% of the time
- The failure appears at the boundary that matters for spaced repetition: distinguishing whether a reasonable-looking prompt will reliably reinforce its target over longer time horizons (T2+), or whether it will produce confusion and friction (T1).
- Both evaluation and generation struggle to discern this T1/T2 boundary. The findings of our rubric study reflect that. Models are best at judging criteria that are apparent without review: missing context, surface ambiguity, shallow phrasing.
- They are weakest at judging the aspects of construction that only emerge through repeated use: clarity and answer stability.
- We tried to bridge this gap with prompting, rubrics, preference data, and training. Grounding had the largest effect: when models are shown labeled prompts for the same highlight, rating judgment precision jumps from 56% to 78%. But even with that impractically helpful grounding, ratings remain unreliable at the T1/T2 boundary.
- Memory system users develop taste for good prompts by reviewing them over time and noticing which ones endure. We can approximate that taste in techniques like rubrics, and we can roughly measure it. But it remains unclear how to more fully transfer the taste we acquire through those review experiences.
