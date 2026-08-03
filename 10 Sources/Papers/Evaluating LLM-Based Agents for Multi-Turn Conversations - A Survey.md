---
type: paper
status: structured
quality:
topics: [agent-evaluation, llm-evaluation, evaluation-metrics]
source: ""
created: 2025-07-12
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Shengyue Guan, Haoyi Xiong, Jindong Wang, Jiang Bian, Bin Zhu, Jian-guang Lou
- Category: pdf
- Document Tags: good 
- URL: https://arxiv.org/pdf/2503.22458v1
## 0.2 Highlights

- survey = examines evaluation methods for LLM-based agents in multi-turn conversational settings
- 2 interrelated taxonomy systems
    - what to evaluate = key components + dimensions of LLM agents
        - task completion
        - response quality
        - user experience
        - memory and context retention
        - planning and tool integration
    - how to evaluate = methodologies applied to those components
        - annotation-based evaluations
        - automated metrics
        - hybrid strategies combining humans + metrics
        - self-judging methods using LLMs

![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/0a7ea4927118e103f47f5d2a8a216454.png)

## 0.3 why evaluation is hard
- evaluation methods must be automated, reproducible, human-aligned to ensure real-world reliability
- techniques improving dialogue evaluation
    - deep-utterance aggregation = refines earlier statements
    - external knowledge integration = enriches dialogue content
## 0.4 taxonomy 1 – what to evaluate
- evaluation goals = four broad areas for multi-turn agents
    - end-to-end experience
    - action & tool use
    - memory capabilities
    - planning functions
#### 0.4.1.1 end-to-end experience
- five dimensions
    - task completion = measures goal fulfilment via completion rate, satisfaction
    - multitask capabilities = probes cross-domain expertise (math, history, coding)
    - interaction patterns = analyses recollection, follow-up, expansion for coherence
    - temporal dimensions = tests context retention over long durations
    - user experience & safety = gauges satisfaction, engagement, and harm avoidance
#### 0.4.1.2 task completion in multi-turn conversations
- objective metrics = completion rates, unrecognised-utterance tracking, usability, likability, conversation quality
- gap = limited analysis of failure causes (e.g. miscommunication, system limits)
#### 0.4.1.3 interaction patterns
- four patterns = recollection, expansion, refinement, follow-up
    - LLM-as-evaluator approaches rate these patterns
#### 0.4.1.4 user experience & safety
- evaluates satisfaction, engagement, harmful-content safeguards, adversarial robustness
#### 0.4.1.5 action & tool use
- multi-step tool selection & reasoning
    - MetaTool evaluates tool awareness with ToolE dataset
    - reveals challenges in choosing appropriate tools
#### 0.4.1.6 memory evaluation
- memory spans = temporal scope
    - turn memory = within a single turn
    - conversation memory = across multiple turns
    - permanent memory = long-term persistence
- memory forms = representation + implementation of memory
- four user-agent interaction types
    - complete interactions = store everything
    - recent interactions = discard after time window
    - retrieved interactions = recall past sessions when relevant
    - external interactions = use external modalities or tools (e.g. image + math)

![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/2f8f5243a93a80b986af46efadaf7d35.png)

![](https://readwise-assets.s3.amazonaws.com/media/reader/pub/b93ab11bbc9b98c86329b9216da657d0.png)

#### 0.4.1.7 planner evaluation
- 4 dimensions
    - task modelling
        - task representation = define objectives, actions, expected outcomes
        - context modelling = capture situational information
    - task decomposition = break complex tasks into subtasks
    - adaptation & control = recalibrate to evolving context + feedback
    - reflection
        - plan verification = check feasibility, safety, correctness
            - methods: React guided reasoning, model checking, self-refine, graph-based reasoning
        - plan selection
            - in-generation selection = choose best plan during generation
            - post-generation selection = tree or graph of thoughts, human-in-loop, RL optimisation
## 0.5 taxonomy 2 – how to evaluate
- evaluation data = two dimensions
    - conversation data generation
        - next-turn response generation = simulate natural dialogue
        - tool-use data = create API/tool interaction traces
        - query-rewritten data = test reformulation capabilities
        - fact-check data = probe factual verification
    - conversation data annotation
        - annotate expected responses
        - mark tool calls & functions
        - label rewritten queries + retrieved items
        - verify facts
#### 0.5.1.1 conversation data generation methods
- automated pipelines reduce manual effort while maintaining turn-level coherence
- tool-oriented dialogue generation = build dialogues from API docs (e.g. ToolDial)
- query rewriting = selective context integration, self-supervised learning
- factual verification = veracity prediction with evidence retrieval, auto-question pipelines
#### 0.5.1.2 conversation data annotation tasks
- next-turn response annotation
- tool-use/function call annotation
- query rewrite + retrieval annotation
- fact-checking labels
#### 0.5.1.3 evaluation metrics
- annotation-based evaluation
    - annotations as reference = BLEU, ROUGE, METEOR, BERTScore, DialogRPT, USL-H, cosine similarity
    - annotations as exact result = intent recognition, entity extraction
    - limitations = high cost, bias, incomplete coverage of subjective qualities
- annotation-free evaluation
    - point-wise scoring = relevance, clarity, topicality per response
    - pair-wise / list-wise comparison = rank multiple responses for accuracy, coherence, helpfulness
    - benefits = scalable, consistent, no manual labels needed, but may require pretraining
## 0.6 challenges & future work
- unified & adaptive evaluation frameworks = need holistic turn-sequence assessment
- test-time self-assessment = inline quality checks via chain-of-thought style reasoning
- dynamic self-correction = prevent error propagation with multi-reasoning trees, feedback loops
- tool-use & action planning over time = track how external-tool capabilities evolve across dialogue
Feel free to let me know if you’d like any part expanded or reorganised further ✨

---
