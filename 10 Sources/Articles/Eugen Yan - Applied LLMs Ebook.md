---
type: article
status: structured
quality:
topics: [prompting, rag, llm-evaluation, model-monitoring]
source: ""
created: 2025-07-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- from the [mini e-book](https://applied-llms.org/)published by 6 key LLM practioners - June 8 2024
	- essentially all their learning in last 18 months of building apps with LLMs

- [[#1 Prompting|1 Prompting]]
	- [[#1 Prompting#1.1 fundamental techniques|1.1 fundamental techniques]]
	- [[#1 Prompting#1.2 structured inputs/outputs|1.2 structured inputs/outputs]]
	- [[#1 Prompting#1.3 small specialized prompts|1.3 small specialized prompts]]
	- [[#1 Prompting#1.4 crafting context tokens|1.4 crafting context tokens]]
- [[#2 RAG|2 RAG]]
	- [[#2 RAG#2.1 RAG quality = relevance, density + detail|2.1 RAG quality = relevance, density + detail]]
	- [[#2 RAG#2.2 Keyword + hybrid search|2.2 Keyword + hybrid search]]
	- [[#2 RAG#2.3 RAG + finetuning for new knowledge|2.3 RAG + finetuning for new knowledge]]
	- [[#2 RAG#2.4 Long Context is not the end of RAG|2.4 Long Context is not the end of RAG]]
- [[#3 Tuning Workflows|3 Tuning Workflows]]
	- [[#3 Tuning Workflows#3.1 Multi-step flows|3.1 Multi-step flows]]
	- [[#3 Tuning Workflows#3.2 Deterministic flows|3.2 Deterministic flows]]
	- [[#3 Tuning Workflows#3.3 Getting better diversity|3.3 Getting better diversity]]
	- [[#3 Tuning Workflows#3.4 Caching|3.4 Caching]]
	- [[#3 Tuning Workflows#3.5 When to finetune|3.5 When to finetune]]
- [[#4 Evals + Monitoring|4 Evals + Monitoring]]
	- [[#4 Evals + Monitoring#4.1 Assertion based unit tests|4.1 Assertion based unit tests]]
	- [[#4 Evals + Monitoring#4.2 LLM-as-Judge|4.2 LLM-as-Judge]]
	- [[#4 Evals + Monitoring#4.3 "Intern" Test|4.3 "Intern" Test]]
	- [[#4 Evals + Monitoring#4.4 Don't overemphasize evals|4.4 Don't overemphasize evals]]
	- [[#4 Evals + Monitoring#4.5 Use binary tasks|4.5 Use binary tasks]]
	- [[#4 Evals + Monitoring#4.6 Reference-free evals|4.6 Reference-free evals]]
- [[#5 Guardrails|5 Guardrails]]
	- [[#5 Guardrails#5.1 Hallucinations|5.1 Hallucinations]]
- [[#6 Operational considerations (brief)|6 Operational considerations (brief)]]
	- [[#6 Operational considerations (brief)#6.1 Data|6.1 Data]]
	- [[#6 Operational considerations (brief)#6.2 Models|6.2 Models]]
	- [[#6 Operational considerations (brief)#6.3 Product|6.3 Product]]
- [[#7 Strategic considerations (brief)|7 Strategic considerations (brief)]]
	- [[#7 Strategic considerations (brief)#7.1 Data|7.1 Data]]
	- [[#7 Strategic considerations (brief)#7.2 AI in the loop, Humans in the center|7.2 AI in the loop, Humans in the center]]


# 1 Prompting
- start with prompting when prototyping new applications
- can get us very far with prompting, but can also take it to complex levels
## 1.1 fundamental techniques
- **in-shot prompts + in-context learning** -> provide LLM examples demonstrating task -> align outputs to expectations
    - n should be between 5-12, too few risks over-anchoring
    - examples should be representative of prod distribution, use same proportion of categories
    - don't always need input-output pairs, desired output examples may be sufficient
    - if LLM will use tools, include examples of tool use
- **Chain-of-Thought (CoT)** -> encourage LLM to explain thought process before returning final output
    - originally started with adding "let's think step by step" but more specificity helps
    - add specificity with extra explicit steps e.g. `meeting transcript summarizer`
    - list key decisions, actions + owners in sketchpad
    - check details in sketchpad are factually consistent with transcript
    - synthesize key points into concise summary
- **providing relevant resources** -> expand model knowledge base by providing relevant snippets (RAG)
    - helps ground agent responses to corpus of resources -> helps reduce hallucinations + increase trust
    - rather than simply including, tell LLM to prioritize docs, refer directly or mention when no resources are available
## 1.2 structured inputs/outputs
- helps model better understand formats + more reliably integrate with downstream systems
- structured input expresses tasks clearly + resembles how training data is formatted -> better output probability
- examples of techniques
    - add serialization formatting to inputs
    - add additional metadata to specific tokens e.g. types
    - relate request to similar examples in training data
	- adding structured schema definitions for Text-to-SQL
	- using prefilled XML or JSON formats
- check out 2 popular packages -> `Outline` and `Instructor`
## 1.3 small specialized prompts
- experience has shown people start with simple prompt then evolve into much lengthier monolithic prompt
    - however, later finding out that another version of the simple prompt works just as well e.g. GoDaddy learnt this
- break the prompt into steps e.g. `meeting transcription summarizer`
    - extract key decisions, action items and owners into a structured format
    - check extracted details against original transcription for consistency
    - generate a concise summary from the structured details
- resulting multiple prompts are all simple, focused and easily understood
    - can then iterate and eval each prompt individually
## 1.4 crafting context tokens
- might realize you don't need to send everything to LLM, try to refine and remove irrelevant details
- you will notice this in the final prompt which might include context construction, meta-prompt, RAG results onto a single page and reading it -> helps you rethink when you find redundant, contradictory or poorly formatted language
- optimize prompt structure, make it readable like you would for humans
---
# 2 RAG
## 2.1 RAG quality = relevance, density + detail
- RAG quality dependent on quality of retrieved docs - some factors contribute to this
    - **relevance** -> quantified via Mean Reciprocal Rank (MRR) or NDCG
        - MRR = how well system places first relevant result in ranked list
        - NDCG = considers relevance of all results + their positions
    - **rank** -> test by running with reshuffling of items (retrieved doc chunks)
    - **density** -> when 2 docs equally relevant, pick the more concise and less extraneous detail one
    - **level of detail** -> additional details may help
## 2.2 Keyword + hybrid search
- embeddings are very powerful - excelling at high level semantic similarity
    - but struggle with more specific, keyword based queries e.g. names, acronyms or IDs
- keyword search is also powerful - since information retrieval field has decades of solutions for this
    - e.g. BM25 algorithm
    - more straightforward to understand why certain doc retrieved with keyword search -> just find matches to query
    - hybrid search often works best
	    - using keyword match for obvious matches and embeddings for synonyms/periphrases/spelling errors    

> *"vector embeddings don't magically solve search; heavy lifting at top belongs to re-rank with semantic similarity search. Making genuine improvements over BM25 or full-text search is hard"* - Aravind Srivinvas


## 2.3 RAG + finetuning for new knowledge
- can use both RAG and finetuning, but RAG much easier to start with
	- RAG also found to have edge vs finetuning in some tests in performance
- other RAG advantages
    - easier + cheaper to keep indices updated than periodic re-finetune
    - easier to drop docs that are toxic or biased
    - finer grained control over how we retrieve docs e.g. segregating info between users
## 2.4 Long Context is not the end of RAG
- Rumors of RAG's demise greatly exaggerated e.g. Gemini 1.5 has 10M context length
    - even in 10M context window, still need to find most relevant context
    - without good retrieval + ranking, can overwhelm LLM with distracting info
- no convincing evidence of model reasoning over large context sizes
    - needle in haystack tests are not foolproof
- time cost -> transformer inference scales linearly with context length
---
# 3 Tuning Workflows
## 3.1 Multi-step flows
- decomposing single big prompt to smaller multiple prompts gives better results
    - sometimes also known as agentic workflow e.g. Andrew Ng
	- single prompt to multi-step workflow improved AlphaCodium performance (pass@5 on CodeContests) from 19% to 44%
- multi-step workflow can include
    - reflect on problem
    - reason on sample tests
    - generate possible solutions
    - generate synthetic tests (if coding)
    - iterate on solutions on sample + synthetic tests
- small tasks + clear objectives = best for agentic/flow prompting, other tips
    - structured outputs help interface with parts of orchestration environment
    - tight specifications + explicit planning + predefined plans to choose from
    - rewriting original user prompts to agent prompts
    - planning validations - instructions on how to eval responses from other agents, evals final assembly of all parts
    - prompt engineering with fixed upstream states
## 3.2 Deterministic flows
- probabilistic (i.e. non-deterministic) nature of LLMs makes them challenging to deploy
	- each step of agent has chance to fail, chances of recovering are poor
	- likelihood agent completes many steps successfully goes down exponentially as # steps increases
- can produce deterministic execution plans -> structured + reproducible way
	- give high level prompt, agent generates plan
	- plan executed deterministically
	- benefits
	    - generated plans serve as few shot samples to later prompt or finetune
	    - more reliable, easier to test + debug
	    - can represent plans as DAGs
## 3.3 Getting better diversity
- often, changing temperature doesn't give better diversity
	- sometimes for product recommendations, you might get handful which are overrepresented
	- only changes probability distribution to be flatter, not guaranteeing LLM samples outputs from same probability distribution you expect
- simplest method = adjust elements within prompt e.g. shuffle order each time they get added as context
- keeping short list of recent outputs also prevents redundancy
    - e.g. instruct LLM to avoid suggesting items from recent list
    - e.g. rejecting + resampling outputs very similar to recent suggestions
- vary the phrasing used in prompts
    - i.e. state similar things with different aspects
## 3.4 Caching
- caching saves cost + reduces need for inference - uses precomputed responses for similar inputs
	- also increases safety if past responses have been guardrails
		- can then serve vetted responses - reduce risk of serving harmful/inappropriate content
- using unique IDs for items processed then checking against cache
## 3.5 When to finetune
- finetuning could help when prompting + RAG fall short, especially for specific domains
	- comes with high costs e.g. annotate FT data, FT + eval model, self host them
- if you do this, consider methods to reduce cost of collecting human-annotated data
    - e.g. generate synthetic data or bootstrap on open source data
---
# 4 Evals + Monitoring
- big minefield topic even top research labs struggle on
- however, rigorous and thoughtful evals are critical -> e.g. 3 managers at OpenAI with big teams doing wrote individual evals or gave low-level feedback on evals that I had written
## 4.1 Assertion based unit tests
- using real input/output samples, can create unit tests (assertions) based on at least 3 criteria
## 4.2 LLM-as-Judge
- using strong LLM to evaluate output of other LLMs
    - decent correlation w humans when implemented well + helps build priors on how new prompts/techniques perform
    - pairwise comparisons usually get direction right but magnitude of win/loss can be noisy
- getting most out of LLM-as-Judge
    - <mark style="background: #FFB8EBA6;">use pairwise comparisons</mark> (more stable) - rather than score independently on Likert scale
    - <mark style="background: #FFB8EBA6;">control for position bias</mark> - swap order of pairs
    - <mark style="background: #FFB8EBA6;">allow for ties</mark> - they might be equally as good
    - <mark style="background: #FFB8EBA6;">use CoT</mark> - ask to explain before final answer (can even do this w weaker LLM)
    - <mark style="background: #FFB8EBA6;">control response length</mark> - LLM bias longer responses, ensure similar length
- useful application of LLM-as-Judge is regression testing for new prompting strategy
    - can re-run collected examples with new strategy and use LLM-as-Judge to assess performance
- simple but effective example of iterating on LLM-as-Judge (image below)
	- log LLM response, judge critique (CoT) and final outcome
	- then review with stakeholders to identify areas for improvement
	- over 3 iterations, agreement w humans went from 68% to 94%
- conventional classifiers can also be better and cheaper e.g. DeBERTA or others
## 4.3 "Intern" Test
- imagine you have an intern, if you gave them the context and input, could they figure it out
- if answer is no because LLM lacks required knowledge, enrich the context
- if answer is no and we cannot improve context to fix, may have hit too hard a task for LLMs as of now
## 4.4 Don't overemphasize evals
- Needle-in-a-Haystack (NIAH) eval has become questionable on truly measuring reasoning and recall in real world
	- Goodhart Law - when measure becomes target, ceases to be good measure
	- lots of providers overemphasize this test now
	- e.g. practical NIAH eval using Doctor + Patient Transcripts
		- LLM queried on patient meds + also challenges by inserting phrase for random pizza topping ingredients
		- Recall was 80% on medical task, 30% on pizza task
- also applies to other tasks e.g. summarization
	- overemphasizing consistency can lead to summaries which are less specific and possibly less relevant
## 4.5 Use binary tasks
- simplify annotation - using open ended feedback or ratings for generated outputs (e.g. Likert Scale) is noisy and more variable among humans
	- simplify task, reduce cognitive burden on annotators -> use binary classifications + pairwise comparisons
- <mark style="background: #FFB8EBA6;">binary classifications</mark> = annotators make simple yes no judgement on model output
	- more precise than Likert, higher consistency, more throughout
	- e.g. DoorDash applied this successfully for tagging menu items through a tree of yes-no questions
- <mark style="background: #FFB8EBA6;">pairwise comparisons</mark> = annotator picks better response from a pair
	- Llama 2 author said pairwise-comparisons are cheaper than collecting SFT data like written responses
	- pairwise = $3.50 while SFT annotation = $25
## 4.6 Reference-free evals
- if evals are reference free, can be used as guardrails
	- reference free eval = do not rely on golden reference (human annotated)
	- can assess quality solely on input prompt + model response e.g. summarization
- if summary scores poorly on factual consistency/relevancy metrics, can choose not to display (like a guardrail)
---
# 5 Guardrails
- LLMs provide output values confidently even when they do not exist
	- try prompt LLM to return "not applicable" or "unknown" response -> not foolproof
	- log probs don't help here because they only show likelihood of next token, not if token/text is correct
		- contrarily, instruct-tuned models may answer queries + coherent text that are not well calibrated
	- high log probs only indicate output is fluent and coherent, not accurate or relevant
- complement prompt engineering with robust guardrails - to detect/filter/regenerate undesired output
	- e.g. DAI content moderation API, other packages for toxicity and detecting PII
	- beneficially, guardrails are largely agnostic of use case
	- with precise retrieval (RAG), system can also deterministically respond "I don't know" if no relevant documents show up (by some similarity measure)
- unfortunately LLMs can fail to produce outputs even when they should - long tail reasons
	- important to consistently log inputs + (lack of) outputs for debugging + monitoring
## 5.1 Hallucinations
- they remain stubborn problem - often occur at baseline of 5-10%, hard to get it below 2%
- can address via combining prompt engineering + factual inconsistency guardrails
	- e.g. upstream retrieval - use CoT
	- e.g. downstream generation - use factual inconsistency guardrail to assess then filter and regenerate
	- might even notice some hallucinations occur deterministically
	- having structured outputs also helps verify if they're sourced from input context
---
# 6 Operational considerations (brief)
## 6.1 Data
- output data is only way to eval these models
- check dev data matches prod data
	- dev-prod skew can come from structural or content based
	- track skew over time e.g. length of inputs/outputs, more advanced clustering embeddings
	- semantic drift for topics not seen before
	- ensure hold-out datasets are current + reflect recent user interactions e.g. include typos
- run pipeline multiple times for reliability
	- increases chance of finding anomalies
- constantly do vibe checks - look at sample inputs + LLM outputs every day
	- input-output pairs are the "real thing" and cannot be substituted
		- must log inputs + outputs
	- research shows devs change their criteria over time (criteria drift) so this helps
	- when we spot new issues, can immediately write assertions + evals for it
## 6.2 Models
- generate structured output for integration - many use-cases will feed LLM downstream
	- e.g. LinkedIn switched to YAML from JSON (worked better)
		- comes from Postel's Law - "be liberal in what you accept, conservative in what you send" - durable principle
	- e.g. allow any natural language inputs, but only output types machine-readable objects
	- Instructor + Outline packages are de facto standards for coaxing structured LLM outputs
- migrating prompts across models can be a pain
	- often can get wildly different results -> make sure to have reliable/automated evals
	- version and pin your models -> allows you to confidently update when ready
- choose smallest model that works
	- benefits of lower latency and cost
	- carefully crafted workflow of small model can match or even beat larger models + faster/cheaper
		- e.g. haiku 10 shot outperformed zero-shot GPT4 + Claude 2 Opus
	- e.g. use 400M DistilBERT for text classification if it works well, much much cheaper
## 6.3 Product
- timeless principles for building great products
	- involve design early + often
	- design UX for human in loop
		- helps get quality annotations from integrating human loop in user experience
		- e.g. allowing them to provide feedback + corrections easily
	- prioritize hierarchy of needs ruthlessly
		- cannot manage reliability, truthfulness, factual consistency, usefulness, cost and scalability all perfectly at once
		- to be able to ship, need to prioritize and ruthlessly -> what is non negotiable
	- calibrate risk tolerance based on use case
---
# 7 Strategic considerations (brief)
## 7.1 Data
- what is a completely infeasible floor demo or research paper today will become a premium feature in a few years and then a commodity shortly after. We should build our systems, and our organizations, with this in1 mind
- **training from scratch almost never makes sense**
	- BloombergGPT trained specifically for financial tasks, done by 18 full time staff for labelling. AI engineering and product research - GPT3.5 turbo and GPT4 outperformed it within the year
	- teams better off finetuning strongest OS model available for their needs
- **don't finetune until it's necessary**
	- many finetune too early, this is hard and requires many examples -> be convinced other approaches won't suffice
	- few have found this to work, need to be very confident you can do it again as base models improve
	- when is finetuning right? if use case data not available on open web and you've built an MVP that shows existing models are insufficient
- **model is not the product, the system around it is**
	- focus efforts on things with lasting value e.g. evals, guardrails, caching, data flywheel
	- all help create thicker moat of product quality than raw model capabilities
	- enable some "strategic procrastination" - build what you 100% need, wait for expansions to capabilities from providers
- **build trust by starting small with specialized users**
	- focus on specific domains + use cases -> go deep, narrow scope, not wide
	- also allows you to be more upfront with system capabilities + limitations to users
- **don't build LLM features you can buy**
	- focus on LLM apps that truly align with your product goals + enhance core ops
	- e.g. building custom text-to-sql or document chatbot all have been superseded by generic capabilities
## 7.2 AI in the loop, Humans in the center
- LLM apps are brittle right now, requires lots of safe-guarding + defensive engineering
	- most effective paradigm is capable humans paired with LLM capabilities tuned for rapid utilisation/productivity/happiness gains
		- e.g. Github Copilot for coders
	- centering humans + asking how LLM can support their workflow leads to you to significant product + design decisions
- **start with prompting, evals + data collection**
	- core idea = start simple, add complexity as needed
		- rule of thumb = each level of sophistication requires at least 10X (1 order magnitude) more effort than prior one
	- prompt engineering comes first, if this does not work, then can try prompt engineer
	- build evals and kickstart data flywheel
		- without evals, won't know how sufficient your prompt engineering or setup is + when to finetune
		- effective evals are specific to your tasks + mirror intended use case
		- start with unit tests + other task-specific evals for classification, summarization etc
		- these don't replace human eval - have people use it + provide feedback
		- and use this annotated data to finetune model or update prompt -> repeat
- **cost vs capabilities over time rapidly decreasing**
	- for a fixed cost, capabilities are rapidly increasing, for fixed capability, costs rapidly decreasing
		- e.g. OAI davinci model went from $20 to 10c
