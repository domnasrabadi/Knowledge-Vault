---
type: book
status: structured
quality:
topics: [spaced-repetition, knowledge-management]
source: ""
created: 2025-08-04
published:
author: ""
flashcards: none
updated: 2025-08-04
---
- from the 1999 article https://supermemo.guru/wiki/20_rules_of_knowledge_formulation

# 1 Intro 
- speed of learning = depends on formulation; well-formulated items can be learned many times faster
	- assumption = learning proceeds using spaced repetition
- use simple and specific statements, not complex and wordy 

>[!failure] What are the characteristics of the dead sea?
> salt lake located on the border between Israel and Jordan; its shoreline is the lowest point on the Earth’s surface, averaging 396 m below sea level; it is 74 km long; it is seven times as salty (30 % by volume) as the ocean; its density keeps swimmers afloat; only simple organisms can live in its saline waters

>[!success] Instead, break it down into atomic flashcards
> - Q: where is the Dead Sea located? A: **on the border between Israel and Jordan**
> - Q: what is the lowest point on the Earth’s surface? A: **the Dead Sea shoreline**
> - Q: what is the average level on which the Dead Sea is located? A: **400 meters** (below sea level)
> - Q: how long is the Dead Sea? A: **70 km**
> - Q: how much saltier is the Dead Sea compared with the oceans? A: **7 times**
> - Q: what is the volume content of salt in the Dead Sea? A: **30 %**
> - Q: why can the Dead Sea keep swimmers afloat? A: **due to high salt content**
> - Q: why is the Dead Sea called Dead? A: **because only simple organisms can live in it**
> - Q: why only simple organisms can live in the Dead Sea? A: **because of high salt content**

- break statements into minimal fill-in prompts, not verbose historical overviews 

>[!failure] Q: what was the history of the Kaleida company?
> A: kaleida, funded to the tune of $40 million by apple computer and ibm in 1991; mission to create a multimedia programming language; finally produced script X after three years; meanwhile macromedia and asymetrix had snapped up all the business; kaleida closed in 1995

>[!success] well formulated knowledge (cloze deletion)
>- Q: kaleida was funded to the tune of …(amount) by apple computer and ibm in 1991 A: **$40 million**
>- Q: kaleida was funded to the tune of $40 million by …(companies) in 1991 A: **apple and ibm**
>- Q: kaleida was funded to the tune of $40 million by apple computer and ibm in …(year) A: **1991**
>- Q: …(company) mission was to create a multimedia programming language. It finally produced one, called script X. But it took three years A: **kaleida’s**
>- Q: kaleida’s mission was to create a … It finally produced one, called script X. But it took three years A: **multimedia programming language**
>- Q: kaleida’s mission was to create a multimedia programming language. It finally produced one, called … But it took three years A: **script X**
>- Q: kaleida’s mission was to create a multimedia programming language. It finally produced one, called script X. But it took …(time) A: **three years**

- do not use cloze deletion that is to wordy, fewer words will speed up learning 

>[!failure] Q: aldus invented desktop publishing in 1985 with pagemaker. aldus had little competition for years, and so failed to improve. then denver-based … blew past. pagemaker, now owned by adobe, remains no 2 A: **quark**

>[!success] fewer words = faster learning
>- Q: aldus invented desktop publishing in 1985 with pagemaker but failed to improve. then … blew past (pagemaker remains no 2) A: **quark**
>- Q: aldus invented desktop publishing with pagemaker but failed to improve. it was soon outdistanced by … A: **quark**
>- Q: pagemaker failed to improve and was outdistanced by … A: **quark**
>- Q: pagemaker lost ground to … A: **quark**

# 2 The 20 Rules
## 2.1 Do not learn if you do not understand 
- flashcards are powerful **only after** you grasp the ideas they compress
- consequences of not understanding
	- shallow recognition without ability to transfer
	- error-prone reasoning
	- inability to debug 
- example
	- Q: "*What is the gradient descent update rule*"? A: `θ ← θ − η ∇J(θ)` 
	- What you memorise = the exact symbol sequence 
	- What you cannot do = explain why subtracting the gradient lowers the loss
		- predict how changing the learning rate effects convergence 
		- or recognise when momentum would be helpful 
- how to mitigate 
	1. **Learn the concept first**
	    - Work through a visual or code-based derivation (e.g., plot the loss surface and watch gradient arrows).
	2. **Break complex ideas into atomic Q-A pairs**
	    - “Why does subtracting the gradient reduce the loss in convex regions?”
	    - “What happens if `η` is too large?”
	    - “How does L2 regularisation influence variance?”
	3. **Add application prompts**
	    - Turn definitions into micro-scenarios:
	    - e.g. _Scenario:_ Validation loss rises while training loss falls. **Action? Explain why.**
	4. **Periodically connect cards**
	    - After reviewing “cross-entropy,” immediately review “soft-max gradient” and “label-smoothing,” forcing retrieval in a web of meaning.
## 2.2 Learn before you memorise 
- build an overall picture of the learned knowledge before splitting it into questions and answers
    - only when individual pieces fit into a coherent structure will learning time be dramatically reduced
    - avoid memorizing loosely related facts before reading a chapter that integrates them
## 2.3 Build upon the basics 
- picture of the learned whole = initial model need not be complete; simpler and shorter is better; refine later
## 2.4 Stick to the minimum information principle
- minimum information principle = material must be as simple as possible without losing essential content
- reasons for simplicity:
	- simple is easy
		- easier for the brain to process consistently
	- simple items easier to schedule in spaced repetition
		- splitting complex items into sub-items allows each to be repeated at its optimal interval, saving time
		- long-term retention benefits more from simplified items
- objective: retrieve the minimum amount of information per repetition; keep answers as short as possible
## 2.5 Cloze deletion is easy and effective 
- cloze deletion = sentence with parts replaced by three dots for fill-in practice
    - example: `bill …[name] was the second us president to go through impeachment`
    - recommendation: beginners use cloze deletion to adhere to the minimum information principle
    - integral to incremental reading techniques
- incremental reading = fast reading and learning technique using cloze deletion to incrementally extract and learn knowledge
## 2.6 Use imagery 
- use imagery = leverage visual cortex strength; one picture is worth a thousand words; graphic representations are less volatile
## 2.7 Use mnemonic techniques 
- mnemonic techniques = techniques that facilitate memory (e.g., peg lists, mind maps)
    - effective with training; initial conscious use in 1–5 % of items, eventually automatic
## 2.8 Graphic deletion is as good as cloze deletion 
- graphic deletion = image-based cloze deletion; hide parts of an image and ask to identify the missing area; one illustration can yield 10–20 items
## 2.9 Avoid sets 
- set = collection of objects; enumeration = ordered list of members
    - avoid sets whenever possible; convert necessary sets into enumerations to leverage order for easier recall
## 2.10 Avoid enumerations
- if enumerations are unavoidable, apply cloze deletion or grouping techniques
## 2.11 Combat interference
- memory interference = when learning one item impedes recall of another
    - prevention tips:
        - make items unambiguous
        - apply the minimum information principle
        - detect and eliminate interference as soon as it arises
## 2.12 Optimise wording, refer to other notes, personalise them, rely on emotions + context cues 
- optimize wording = craft items so the correct memory cue fires immediately; reduces errors, response time, and cognitive load
    - strategies:
        - refer to other memories for context and reduced interference
        - link to personal life for stronger encoding
        - use vivid or shocking examples to evoke strong emotions
## 2.13 Redundancy does not contradict the minimum information principles
- redundancy = inclusion of additional or duplicate information; does not contradict the minimum information principle and can be beneficial
    - examples:
        - passive vs active approach in language learning: add swapped question-answer pairs for recognition even if redundant
        - reasoning cues: provide solution steps in the answer to guide reasoning
        - derivation steps: memorize individual steps for complex problem solving
        - multiple semantic representations: learn different angles of the same fact to boost recall
        - flexible repetition: accept any valid equivalent response (e.g., blot/blob/blotch) to simplify grading
## 2.14 Provide sources
- provide sources = cite origins of knowledge (except well-tested facts) to aid updates, assess reliability, and track volatility
## 2.15 Provide data stamping
- knowledge stability = stable knowledge (e.g., basic math) versus volatile knowledge (e.g., economic indicators)
## 2.16 Prioritise
- prioritize = select and sequence what to learn based on importance and impact
    - prioritizing sources: identify which sources and topics yield the best learning outcomes
    - extracting knowledge: focus on the most impactful parts of texts rather than entire books
    - use incremental reading tools to manage the flow of knowledge
    - formulating items: place explanatory or optional components in parentheses so main answers remain concise
    - forgetting index = use retention settings to prioritize important items with higher repetition frequency and deemphasize less critical ones

