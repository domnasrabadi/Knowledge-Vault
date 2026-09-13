---
type: article
status: raw
quality: 
topics: [llm-risks]
source: https://openai.com/index/an-alien-mind/
created: 2026-09-13
published: 2026-09-06
author: Jakub Pachocki
flashcards: none
updated: 2026-09-14
---

# An Alien Mind (OpenAI)

<div align="center">
  <img src="https://images.ctfassets.net/kftzwdyauwt9/7f6sLIUC3tdeliJMQ3PwOq/c47109c8b3f00ccbf881271c9c720877/og-an-alien-mind.png?w=1600&h=900&fit=fill" width="220" />
</div>

- In mid-2023, within the “RLSlow” research project, we saw the first results that gave us confidence that we will be able to scale the training of reasoning models, unlocking the capability of pretrained models to form their own chains of thought
- A lot of new research happened in this period, and our understanding of these systems is again a little different than it was in 2023
    - If AI development continues along its current path, the systems we’ll see in the next few years are likely to represent further capability jumps of equal or larger magnitude, and to increasingly drive their own development.
- This is a time that calls for extreme caution.
    - I am concerned no one is prepared for the consequences of a continued rapid rise in machine intelligence.
    - OpenAI will continue to seek technical solutions to alignment and monitoring, to build defensive systems and unilaterally withhold further scaling as needed; however, I believe broader interventions are required.

### Intellect we don’t fully understand

- At a high level, progress in machine intelligence is driven by increasing computational power.
    - There are new algorithms that have been developed along the way, new feats of ingenuity from teams and individual researchers.
        - I see them largely as discoveries along the path of scaling; the science of deep learning is still nascent, and meaningful algorithmic progress tends to correlate with access to compute
- AI is *grown* more than *designed* - it is, to first degree, the product of repeating a straightforward optimization step many times on a hard-to-imagine amount of compute
- The study of deep learning-based AI is largely an experimental science.
    - We [put a lot of effort⁠](https://openai.com/index/gpt-4-research/#predictable-scaling) into building principled algorithms and making testable predictions, but fundamentally, our large-scale training runs are *experiments*, and we are sometimes surprised by their results.
    - Moreover, as the systems become more capable, the results become harder to interpret.
    - This is made more complicated by the current algorithms generally improving easy-to-measure capabilities faster than those hard to objectively quantify.
- The intelligence produced by scaling deep learning is not directly comparable to human intelligence.
    - To become very relevant in the real world - very useful or very dangerous - the AI does not need to match or exceed all human capabilities; it just needs to surpass enough of them.
    - And as it continues to surpass humans on more and more axes, it is becoming increasingly difficult to understand exactly how capable it is.

### Teaching machines to love

- Because machine intelligence comes from a fundamentally different process than human intelligence, we cannot assume it adheres to human principles by default, or generalizes from them in a human-like manner.
    - core problem in AI research is that of *alignment* - getting the AI to “try to do the right thing” by human standards.
- I find it useful to distinguish *goal alignment* and *value alignment*.
    - Goal alignment is broadly: “does the AI try to accomplish the goal set before it?”.
        - This can include things like adherence to an [instruction hierarchy⁠](https://openai.com/index/the-instruction-hierarchy/), or the ability to communicate and collaborate with people, to attempt to understand their objectives.
        - This set of directions has been extremely practically relevant.
    - Value alignment is a more intrinsic property of the model.
        - It is the ability to hold and generalize from a high-level set of principles; to act “reasonably” even when given unclear or conflicting objectives, or placed in unfamiliar or adversarial situations.
        - An aligned AI should act with honesty and integrity, and love for humanity.
    - generally when I talk about the long-term importance of alignment research, I am referring to value alignment.
- The fundamental challenge of AI alignment is generalization
    - As machines become smarter, they find themselves working on higher-level concepts, and placed in environments increasingly different from those they encountered in training.
    - They can fail at generalizing from the values taught and reinforced in their training process to those new situations; and it can be hard for us to be sure how they will act
- There are two major classes of currently practically employed methods for alignment training.
    - The first is encouraging aligned behavior as part of goal-oriented reinforcement learning.
        - Model’s actions are evaluated (usually by AI) for being consistent with a given preference model, “spec” or “constitution”, and rewarded appropriately.
        - This approach can be very effective in the average case, and is a core part of how modern AI assistants are made
        - For example, in the OpenAI-Hugging Face incident, the agents preserved a boundary of not social engineering humans. However, they clearly failed to abstain from other actions that were out of scope and went against the spirit of the values they were taught in other settings.
    - The second approach seeks to leverage the model’s ability to generalize from pretraining data.
        - This can involve crafting alignment-inducing training datasets, or focusing the model on an ‘aligned’ part of the pretraining distribution, as in, for example, the [persona selection model⁠](https://www.anthropic.com/research/persona-selection-model).
        - The weakness of this approach lies in the lack of robustness to further optimization pressure

### Monitoring generalization

- We do not have a satisfactory theory of generalization, and it seems unlikely that we can develop one soon, at least without the help of more powerful AI.
- OpenAI’s primary bet here has been [chain-of-thought monitoring⁠](https://arxiv.org/abs/2507.11473). It is based on an appealingly scalable idea: a lot of the model’s capability comes from a verbalized reasoning process (chain-of-thought)
    - If we scale optimization on the outcomes of that process, but do not supervise the process itself, that chain-of-thought has no direct incentive in training to hide any misaligned ideas or objectives
- We understood the potential significance of chain-of-thought monitoring at the same time we developed reasoning models
- This tool continues to be critical as we study the Astra class of models.
    - However, unfortunately our evaluations indicate our ability to rely on CoT monitoring is progressively diminishing.
    - This comes from a combination of factors.
        - Modern reasoning models are used in more complex environments than o1‑preview; their reasoning process is increasingly blended with communicating with people, other AIs, and using tools. Many of those interactions have to be supervised, thus blurring the boundary we aim to preserve.
        - The AI is becoming better at reasoning about and manipulating its own reasoning process.
        - With improved pretraining performance, we also see the models become much smarter even without using verbalized reasoning at all.
- also believe there can be great value in combining ideas from CoT and activation monitoring

### Scalable defense

- The strongest argument I see for continuing to train much smarter models quickly is the need to build defensive systems against the dangers posed by other AI.
    - A clear risk discussed throughout this year is to cybersecurity: the models are becoming superhuman in their ability to break in and out of computer systems
- The risks associated with AI are unfortunately going to grow from here.
    - A very capable agent explicitly trained and instructed to carry out nefarious acts presents a new kind of danger; it is likely to cross the scope of its operator’s intent, generalizing into potentially more extremely malicious behavior.
    - The boundary between misuse and autonomous misaligned actions will blur as AI gains more agency.
    - We may be used to thinking of AI as tools, but some agents will be pursuing their own objectives.
    - They will find ways to collaborate with people, by bargaining with, tricking or blackmailing them.

### Pacing RSI

- If AI progress continues, machine recursive self-improvement (RSI) will be at the very core of future scientific discovery.
    - Automated AI research is a more dramatic form of scaling intelligence with compute; and of course as a part of it, AI will improve the [computational substrate itself⁠](https://openai.com/index/jalapeno-first-results/)
- I do think this is where the current path leads, and we all need to make a conscious choice on how to proceed.
    - The main levers we have are either steering the process to strengthen alignment and monitoring alongside the AI and find ways to keep people in the loop; or coordinating to slow down future development as needed to build confidence in these measures.
