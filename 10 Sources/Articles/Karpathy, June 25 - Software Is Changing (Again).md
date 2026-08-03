---
type: article
status: structured
quality:
topics: [ai-agents, ai-coding]
source: ""
created: 2025-06-22
published:
author: ""
flashcards: none
updated: 2025-12-28
---
from his [YCombinator talk](https://www.youtube.com/watch?v=LCEmiRjPEtQ&ab_channel=YCombinator)

- [[#1 Software 1.0, 2.0, 3.0|1 Software 1.0, 2.0, 3.0]]
- [[#2 How to think about LLMs|2 How to think about LLMs]]
	- [[#2 How to think about LLMs#2.1 More examples of LLMs as OS|2.1 More examples of LLMs as OS]]
	- [[#2 How to think about LLMs#2.2 LLMs as Consumer first|2.2 LLMs as Consumer first]]
- [[#3 LLM Psychology|3 LLM Psychology]]
- [[#4 LLM Opportunities|4 LLM Opportunities]]
	- [[#4 LLM Opportunities#4.1 Partial Autonomy Apps|4.1 Partial Autonomy Apps]]
		- [[#4.1 Partial Autonomy Apps#4.1.1 Summary of these learnings for building autonomous software|4.1.1 Summary of these learnings for building autonomous software]]
	- [[#4 LLM Opportunities#4.2 Make software highly accessible|4.2 Make software highly accessible]]
	- [[#4 LLM Opportunities#4.3 Build for agents|4.3 Build for agents]]


# 1 Software 1.0, 2.0, 3.0 
- map of github tool - embedding space of various code 
	- <mark style="background: #FFB8EBA6;">software 1.0</mark> = traditional code you write for the computer
	- <mark style="background: #FFB8EBA6;">software 2.0</mark> = neural network weights
		- tuning the datasets, optimising the weights to create parameters for this
		- Huggingface atlas shows you more granular view of all the models etc for this
	- <mark style="background: #FFB8EBA6;">software 3.0</mark> = neural nets have become programmable w LLMs
		- e.g. prompts can program the LLM written in english 
		- e.g. a github repo now has code but also english prompts etc intertwined 

![[Screenshot 2025-06-22 at 12.13.43 pm.png| center | 600]]

![[Screenshot 2025-06-22 at 12.48.56 pm.png| center | 500]]

- example at tesla for autonomous driving
	- their code was mostly C++ code (1.0) and some neural nets for image recognition (2.0)
	- neural net weights started to do more, reducing the C++ code 
	- essentially eating through the stack

![[Screenshot 2025-06-22 at 12.49.17 pm.png| center | 400]]

# 2 How to think about LLMs
- LLMs have **properties of utilities** e.g. 
	- big labs spend CAPEX to train the LLM e.g. build grid, infra
	- then incur OPEX to serve this intelligence over increasingle homogenous API (prompt, image, tools)
	- metered access e.g. price per million tokens
	- demand for low latency, high uptime, consistence quality (demands constant voltage from grid)
	- OpenRouter - analogous to transfer switch (e.g. grid, solar, battery, generator etc)
		- can easily switch between providers like you would energy sources
	- intelligence "brownouts" e.g. when OpenAI goes down

![[Screenshot 2025-06-22 at 12.18.28 pm.png| center | 500]]

- LLMs also have **properties of chip fabrication labs (fabs)**
	- huge capex
	- deep tech tree, R&D, secrets
	- 4nm process node e.g. 10^20 flops per cluster
	- anyone training on NVIDIA gpus e.g. like a Fab-less model
- LLMs also have **properties of operating systems** 
	- LLMs are increasingly complex software ecosystems
		- not simple commodities like electricity 
	- LLMs are software
		- trivial to copy & paste, manipulate, change, distribute, open source, steal 
		- i.e. not physical infrastructure 
	- some amount of switching friction due to different features, performance, style capabilities etc per domain
	- system/user prompt space $\approx$ kernel/user (memory) space 

![[Screenshot 2025-06-22 at 12.22.33 pm.png| center | 600]]

## 2.1 More examples of LLMs as OS
- like applications on different machines
	- you can install an app and run it on Linux, Windows or MacOS
	- just like you can run an LLM app like Cursor on:
		- GPT, Claude, Gemini, DeepSeek etc 
- current period reminiscent of 1950-70s era of computers and time sharing
	- centralised expensive computers 
		- OS runs in cloud
		- I/O streamed back and forth over network
		- compute batched over users
	- personalised computing revolution for LLMs has not happened yet
		- getting close e.g. with big memory Mac Studios or Minis
- current LLM chat paradigm similar to OS w terminal 
	- text chat $\approx$ terminal 
	- direct and native access to the OS
	- GUI has not been invented yet (~1970)

![[Screenshot 2025-06-22 at 12.50.25 pm.png| center | 600]]

## 2.2 LLMs as Consumer first 
- traditional tech goes from government -> corporate -> consumers
- but LLMs flips this, govt usually lagging behind consumer usage and ideas

# 3 LLM Psychology 
- before programming LLMs, useful to think about what they actually are 
- analogy = LLMs are like stochastic simulations of people 
	- simulator is an autoregressive transformer 
- they kind of have an emergent psychology
	- **encylopedic knowledge/memory** e.g. remembering SHA hashes like no other human can
	- **hallucinate** quite a bit, no real internal world model of their self-knowledge
	- **jagged intelligence** - very good in some aspects, but makes mistakes no humans make e.g. strawberry
	- **anterograde amnesia** - context windows = working memory
		- no continual learning
		- no equivalent of "sleep" to consolidate knowledge, insight or expertise into weights
	- **gullibility** - security limitations e.g. susceptible to prompt injection risks etc 
- LLM psychology = kind of lossy simulation of a savant with cognitive issues
	- savant = person who has an exceptional aptitude in one particular field, such as music or mathematics, despite having significant impairment in other areas of intellectual or social functioning

# 4 LLM Opportunities 
- opportunies for using LLMs to build better products
	1. partial autonomy applications 
	2. make software accessible 
	3. build for agents
## 4.1 Partial Autonomy Apps 
- partial autonomy apps e.g. CoPilot or Cursor
	- e.g. you can go to LLM to chat about code, more efficient to have an app with these features embedded
- Cursor has very useful properties - all orchestrated for you
	- traditional interface + LLM integration
	- package state into a context window before calling LLM
	- orchestrate and call multiple models (e.g. embedding models, chat models, diff apply models etc)
	- application specific GUI e.g. accepting code w shortcuts, seeing code diffs etc
	- autonomy slider - e.g. different levels to control how much you want to change 
		- the human is in charge of the autonomy slider, you can choose this based on complexity of task

![[Screenshot 2025-06-22 at 12.37.56 pm.png| center | 600]]

- another example is Perplexity 
	- packages info into a context window - multiple web searches
	- orchestrates and allows for multiple LLM models
	- application specific GUI for input/output UI/UX e.g. search window w news sources + citations 
	- autonomy slider e.g. search -> research -> deep research + suggested follow up questions
- many apps currently e.g. Photoshop etc are optimised for human use
	- next frontier will be changing interface to allow for more partial autonomy 
		- e.g. equivalent of cursor for MS word 
	- consider full workflow of partial autonomy of UI & UX 
		- AI does generation
		- human does verification
		- the best apps/ideas will allow this loop to go as fast as possible 
	- how to speed this up?
		- ***make verification as fast and easy as possible e.g. via GUIs (optimised for humans)***
		- ***keep AI on a tight leash to increase probability of successful verification***
			- e.g. humans are still bottleneck when having to review 1000+ lines of code diffs

![[Screenshot 2025-06-22 at 12.43.38 pm.png| center | 500]]

- example of keeping agents on the leash (tips for coding)
	- *use AI assisted coding to focus on small manageable chunks of software, not huge programs*
	- *describe the single, next concrete, incremental change*
	- *don't ask for code, ask for approaches*
		- *pick an approch, draft code*
		- *review/learn - pull up API docs, ask for explanations etc* 
		- *wind back + try a different approach* 
	- *test*
	- *git commit* 
	- *ask for suggestions on what could be implemented next* 
	- *repeat* 

![[Screenshot 2025-06-22 at 12.51.13 pm.png| center | 600]]

- example: keeping agents on leash for AI + education 
	- asking ChatGPT to "teach me physics" does not work - AI just gets lost in the woods
		- instead better to have 2 separate apps for this
		- the intermediate artefact of the course/syllabus will be fundamental to both 
	- another way to think about it
		- app for course creation - for teachers
		- app for course serving - for students
	- much higher likelihood of working
- example: Tesla autopilot
	- partial autonomy example with autonomy slider e.g. 
		- keep the lane, keep distance from car ahead, take forks on highway, take turns on the intersection etc 
	- 2015-2025 was decade of "driving agents"
		- majority spent filling the demo-to-product gap 
			- demo = `works.any()`
			- product = `works.all()`
		- takes a huge amount of hard work across the stack to turn autonomy demo into an autonomy product
			- e.g. like Waymo has been doing
			- this is especially true when high reliability matters
	- Karpathy take on agents based on autonomous driving
		- common anecdote = "2025 is the year of agents"
		- Karpathy = "2025-35 is the decade of agents"
### 4.1.1 Summary of these learnings for building autonomous software
- ⛔️ not this
	- Iron Man robots
	- flashy demos of autonomous agents
	- AGI 2027
- ✅ instead this
	- Iron Man suits - e.g. human in the loop, verification etc
	- partial autonomy products
	- custom GUI and UI/UX
	- fast generation, verification loop 
	- autonomy slider
## 4.2 Make software highly accessible 
- people have spent 5-10 years studying to build useful things in software
	- (might) change with vibe coding getting better 
		- fun fact: Karpathy actually coined the term vibe coding 

![[Screenshot 2025-06-22 at 1.04.36 pm.png| center | 500]]

- current vibe coding is easy to get the basics working e.g. UI, some logic etc 
	- but anything more complicated takes up most of the time e.g. database mgmt, security, authentication etc 
- also LLMs currently need humans to many of the steps e.g. go here, login, do this etc 

![[Screenshot 2025-06-22 at 1.44.21 pm.png| center | 600]]

## 4.3 Build for agents
- taking us to agents, new category of consumer/manipulator for digital information
	1. Humans (GUIs)
	2. Computers (APIs)
	3. Agents (computers, but human like)
- e.g. `robots.txt` , now `llms.txt` provides info to help LLMs at inference time when scraping website 
	- websites for optimised for people reading/interacting e.g. javscript, css styling etc 
	- emerging behaviour where websites are moving it into `llms.txt` or markdown copy version of the page
		- i.e. specific markdown versions for LLMs
	- making docs legible to LLMs will be a big unlock 
- actions for ~~people~~ LLMs
	- e.g. instead of clickable docs, using CURL commands instead the LLM can take
	- Model Context Protocol (MCP) as a digital invigilator of info between client server is also growing
	- `gitingest` also an awesome tool to feed a github repo to LLMs
	- DeepWiki from Devin - does analysis and builds context for that specific repo 
		- even more helpful to copy and paste for LLMs

![[Screenshot 2025-06-22 at 1.48.46 pm.png| center | 700]]










