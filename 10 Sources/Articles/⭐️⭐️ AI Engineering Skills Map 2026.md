---
type: article
status: raw
quality: 2
topics: [ai-engineering, software-engineering, ai-coding, career-development]
source: https://x.com/andrewyng/status/2090840747738374568/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-09-11
author: Andrew Ng
flashcards: none
updated: 2026-09-16
---

# AI Engineering Skills Map 2026

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/733174243714682880/oyG30NEH.jpg" width="220" />
</div>

- I previously [wrote](https://x.com/AndrewYNg/status/2088302050706686198) about our AI Engineering Skills Map, with the highest level skills being (i) Building and deploying AI applications, (ii) Software engineering fundamentals, (iii) Using coding agents, and (iv) Shaping the build

# 1. Building and Deploying AI Applications

- Being skilled at building and deploying AI applications means knowing:
    - LLM foundations
    - Grounding models with data
    - Building agentic systems
    - Evaluation-driven development
    - Operating in production
    - Machine learning foundations
- The key difference between AI applications and non-AI software is that the former’s output is less predictable. You don’t know in advance what an LLM will output, or what predictions a supervised learning algorithm will make.
    - Because of this uncertainty, building AI systems is a much more iterative process than building traditional software — it is harder to plan the process in advance
    - Skilled AI engineers repeatedly build a piece of software, examine it, and decide what to try next, taking a sequence of steps that are highly influenced by the intermediate results

### LLM foundations

- Understanding how large language models tokenize input and generate output allows you to understand when to count on them and when they may fail.
    - It also allows you to understand when to use a multimodal model, how to make tradeoffs on what to include in the context window, and reason about cache hits, knowledge cutoff, reasoning effort level, sampling parameters, and when to use special features such as tool calling.
    - Understanding these foundations helps you choose the right model or mix of models and apply specialized techniques when needed, such as fine-tuning or self-hosting models.

### Grounding models with data

- LLMs require good input context to produce useful outputs.
    - RAG using vector search was an early attempt to give LLMs relevant context, but the set of techniques for grounding models with data has grown significantly.
    - For example, you will have to decide what to include in a prompt vs. what to let an LLM retrieve on demand using tools, and which representation fits the data and search queries: a vector index, a knowledge graph, or a semantic layer over structured data (such as customer records).
    - You’ll also turn documents (text, PDFs, HTML, images) into LLM-ready inputs and engineer pipelines to keep data clean and fresh.
    - When you understand the menu of techniques available to get data, you are better able to give your LLM relevant context.

### Building agentic systems

- Agentic systems range from workflows that execute a predefined sequence of LLM calls to ones based on an agent harness that lets an LLM repeatedly decide its own next step.
    - You’ll have to choose the architecture — what steps to chain, what to parallelize, when to use code and when to use an LLM — and engineer the workflow or harness, with fallbacks.
    - When designing the agent loop, you will also decide what tools the model can call (including MCP, CLI and sandbox execution environments), what memory architecture to use, how to manage context over long sessions, and when a task needs multi-agent orchestration instead of a single-agent architecture.
    - You’ll also want to turn promising prototypes into reliable, safe and secure agents for production; this requires understanding guardrails, adversarial inputs, and identifying and working around key risks (such as data exfiltration), and governance.
    - Agentic workflows are evolving rapidly, and you will also benefit from understanding any cutting-edge techniques relevant to your application area

### Evaluation-driven development

- In my experience, the most important trait that distinguishes someone great at building AI systems is whether you can drive a disciplined evals/error analysis loop to drive development.
    - This allows you to repeatedly focus your effort on directions that are more likely to be fruitful.
    - I’ve found this to be a tricky skill to master, because the right approach varies significantly by project and even according to the stage of the project.
    - Building good evals is a deep technical skill. You might look at a system’s traces and outputs, carry out exploratory data analysis, and combine that with product and business insight to decide what to measure
    - You should also understand the menu of options for evals, such as when to use deterministic (code-based) evaluations, when to use an LLM-as-a-judge, and when to have a human in the loop, and how to evaluate your evals so as to keep evolving them

### Operating in production

- Operating AI software is different from traditional software because of its unpredictability, cost, and latency.
    - First, you should know how to build observability mechanisms to understand the system’s performance on real usage.
    - You’ll track performance, detect drift, and respond quickly to model failures and security incidents such as adversarial prompt injections.
    - Putting in place regression testing and CI/CD requires more statistical evaluations than traditional software, and the testing effort should be calibrated relative to the risk of a mistake
    - Additionally, it’s important to know how to select the right mix of techniques — such as model choice optimization, distillation and fine-tuning, and agentic workflow simplifications — to optimize for cost and latency, especially if your application reaches many users.

### Machine learning foundations

- Modern LLMs are built using machine learning techniques including supervised learning and reinforcement learning.
    - Every engineer I know that’s good at building with LLMs also understands machine learning and deep learning at some depth.
    - Additionally, many applications still require knowing how to use machine learning – either a model someone else trained or one you train yourself
    - This requires knowing the popular machine learning and deep learning models and tradeoffs in accuracy, training speed, inference speed, and so on, and understanding how to engineer the data needed to train and evaluate these models.
    - The machine learning concepts of bias/variance, error analysis, and engineering your data — all of which are core mental frameworks for navigating how to work with systems with uncertain output — also remain key to making a wide range of decisions in AI system development.

# 2. Software Engineering Fundamentals

- Even when you use a coding agent to write all your code, understanding software fundamentals is important for steering your agent to make the tradeoffs you want — or to even know what tradeoffs exist to be made.
    - A novice who vibe codes without understanding software fundamentals can create simple applications, but this often leads to the coding agent making bad tradeoffs in latency, availability, consistency, reliability, maintainability, simplicity, and/or cost.
    - In such cases, the developer didn’t know such tradeoffs even existed and therefore did not steer the agent to make the right decisions for their application context.
- requires being skilled at:
    - Building full-stack applications
    - Managing data
    - Designing system architectures
    - Making systems secure and reliable
    - Scaling and operating in production

### Building full-stack applications

- Agentic coding enables many developers who previously played more specialized roles (like front-end developer or mobile developer) to play a broader, full-stack role.
    - A coding agent can help with parts of the development process that you might be less familiar with. However, understanding how the full stack actually works is important.

### Managing data

- Data deserves special attention because it is a foundation that software is built on top of, that is relatively hard to change
    - When you know how to manage data, you can think through access patterns and use them to decide what to store and for how long.
    - You can identify the right data models and select the appropriate storage types (such as relational tables, documents, key-value, or graphs) and infrastructure, which in turn affects speed, scalability, availability, reliability, and cost.
    - You understand transactions, concurrency, and how to ensure your data is clean, consistent, and fresh.
    - Deciding how to manage data requires significant human-provided context. Your AI systems will get their own input context from your data source, so if data architecture is chosen poorly, the AI doesn’t know what it doesn’t know.

### Designing system architectures

- When you understand the major components of the full stack of software and data, you are then better positioned to decide how to put the pieces together.
    - Good system design requires understanding what the software is intended to do (how many users? how important is latency? how important is cost? etc.) so you can make choices about the application platform, the boundary between the frontend and backend, system decomposition, application state placement, and architectural granularity (monolith vs. microservices).
    - You will also choose the stack (programming languages, runtimes, component/frontend/backend frameworks, data technologies) — sometimes by running experiments to evaluate options before settling on one.
    - Further, the right architecture is a moving target, depending on the phase of the project.
        - The simple architecture you choose to build a quick prototype may not be the right architecture to build the first production system, and that too may change as the application scales.

### Making systems secure and reliable

- To build reliable systems, you should know how to develop testing strategies to verify the correctness of your system: What mix of unit tests and integration tests, what frameworks to use, and what level of coverage.
    - You also know how to design around possible failures — how to handle failures (like an API hitting a rate limit), build in graceful degradation, and minimize the blast radius of failures.
    - You can now use AI tools to scan your code for vulnerabilities, check dependencies for supply chain injections, and examine your cloud configuration for attack surfaces. But doing this well still requires some knowledge of security.

### Scaling and operating in production

- To serve real users, you will have to know how to deploy your software to production.
    - You will benefit from knowing how to execute the software development lifecycle (SDLC) which, in addition to building and testing, includes configuring the deployment environment, deciding on release strategy, applying deployment automation (CI/CD), and understanding infrastructure as a service (IaaS).
    - Operating in production requires putting in place observability tools, setting alerts, and managing incidents.
    - Lastly, to scale your application, you should understand the real load and know how to scale servers, load-balance, and adapt your data infrastructure (via sharding, indexing, replication) or make architecture changes to allow your system to adapt to scale.
    - Finally, understanding coding best practices like version control, code reviews, dependency maintenance, and how to manage technical debt helps you keep evolving your system over time.
- Some parts of coding knowledge — like memorizing coding syntax — are becoming obsolete. But developers who deeply understand how software works vastly outperform those who vibe code without understanding.

# 3. Using Coding Agents

- A key AI engineering skill is using coding agents. Your skill at steering them both to write code and to carry out non-code tasks allows you to get a lot more done.
    - keeping up with how to use coding agents requires a continuous process of experimentation, building, and learning.
- we found a consistent high-level workflow for building software with them. key steps are:
    1. **Planning.** This includes (i) brainstorming, which may include research, experimentation, and understanding the existing codebase (if any) and (ii) writing a spec that captures requirements, technical design, and architecture, followed by generating an execution plan.
    2. **Execution**, where you build, test, and verify, with the right balance between agent autonomy and human oversight. This involves (i) having the agent build the software, with a calibrated level of agent autonomy and (ii) verifying its output via automated and/or human checks.
    3. **Deployment and monitoring**, in which you (i) deploy, perhaps gated with a CI/CD pipeline or additional human gates, and (ii) use agents to watch logs, surface issues, and propose and execute improvements.
- Now, we focus much less on code and instead focus on deciding what to build, designing the architecture, writing the spec, and verifying outputs.
- The duration of each step can vary significantly between projects, and steps can be omitted.
    - the spec for a greenfield (meaning built-from-scratch) prototype might be loosely described in a quickly written prompt
    - the spec for a brownfield (pre-existing) project with many users might require much more effort to write and verify.
    - Further, the workflow is highly iterative, and skilled developers know when feedback from a later step should lead them back to an earlier one.
- To use coding agents effectively in this workflow, the key skills are:
    - Directing the workflow
    - Enabling agent autonomy
    - Reviewing the work
    - Customizing the agent and its environment
    - Coding agent foundations

### Directing the workflow

- You know how to navigate each step of the workflow above.
    - This involves deciding how much human and how much agent effort to spend on each and when to go back to an earlier step to iterate.
    - requires deeply understanding the tradeoffs of speed, cost, technical risk, and human effort, so you can decide how much to research and plan up front, when to retain human ownership over critical work, how to choose the architecture, how much detail to write into a set of planning artifacts (like a spec), and how to decompose the work into verifiable steps.

### Enabling agent autonomy

- When applying a coding agent to the steps in the workflow, you choose the autonomy level
    - Do you watch it and go back-and-forth interactively or delegate a larger chunk of work to it? And when do you set a clear goal and have it loop until it succeeds?
    - As the build proceeds through different phases, you will calibrate when to make sure key learnings, user feedback, and assumptions — including assumptions that changed partway through the build — are captured for the agent to use downstream.
    - you will decide when to set up many agents to run in parallel on a decomposition of the task — either by having a human or a higher-level agent orchestrate these other agents

### Reviewing the work

- The output of a coding agent is uncertain. We don’t know in advance what good ideas it might come up with and what bugs it will implement.
    - Reviewing and verifying the output is a key step to ensure you are getting the result you want and to redirect the agent if not.
    - You will design testing and validation that is matched to the task, applying both behavioral and functional verification as needed.
    - For qualitative/behavioral evaluation, eval sets, perhaps with LLM-as-a-judge, can be used.
    - You also need to decide how much of these tests should be automated.
        - Some workflows will have all testing and validation fully automated so the agent can check its work and know when it has succeeded in completing a task.
        - When AI review isn’t sufficient, you judiciously insert human reviews of the code behavior (and, infrequently, of code as well) while exploring how to automate this review further.

### Customizing the agent and its environment

- Your ability to update both the agent and the environment it works in allows your agents to efficiently get the context they need, access tools, and build correctly and efficiently.
    - You know how to integrate agent skills, plugins, and MCP servers.
        - Occasionally you will prune them when they are no longer necessary (such as when a new model obviates an old skill).
    - You can use hooks to automate repeatable parts of the development process, like triggering automated code reviews or CI/CD pipelines.
    - You can also maintain the environment the agent works in: updating the standing context (such as `AGENTS.md` or `CLAUDE.md`) with information on the codebase, key architectural assumptions, code style, and data access patterns.
    - You know how to preserve state across multiple sessions and across parallel agents, and accumulate agent learnings over time, perhaps by running post-run retrospectives to capture what did and did not work.
    - You also know how to set up consistent conventions and structure to make your codebase navigable to the agent, and how to occasionally clear out agent-generated debt.

### Coding agent foundations

- Finally, to make good decisions throughout, you have a good understanding of how coding agents work — how they carry out codebase search/retrieval, how they manage their context windows, how different operations (like adding tool calls, MCP servers, etc.) affect context, how agents and subagents interact, and how the agent is built by wrapping a harness around an LLM.
    - This makes the agent less of a black box and helps you to recognize failure modes, such as overengineering a simple solution, losing rigor because the agent lacks an explicit verification process, stopping short of the goal, or agent actions that risk destruction of files or production data.
    - also helps you reason about the agent’s state and steer it by giving it the right prescription or context.
    - this understanding allows you to better spot when the agent goes off-track and requires your intervention.

# 4. Shaping the Build

- Before modern AI tools accelerated and expanded what a single developer could do, tech companies established the practice of having product managers (PMs) and designers specify what should be built and then developers build it.
    - Perhaps a project manager additionally drives the timeline. However, these roles are blurring
    - When you know how to shape the build, you can move faster without waiting for a PM to figure out what to do.
- The key skills for shaping the build are:
    - Driving the build loop
    - Making product decisions
    - Communicating and leading
    - High-agency ownership

### Driving the build loop

- Most software is built via a loop in which you write some code, then get some feedback, and decide what to do next.
    - As a skilled AI engineer, you play a key role in driving this loop, repeatedly deciding on the next step to move your project forward.
    - You have a bias for action, and drive this loop at the high velocity that AI has made possible.
    - you might decide to build a quick prototype to test a technical concept or user feature
    - uild an MVP (minimum viable product) to take to users to demonstrate value, add features, or invest
    - You frequently ship in small batches to keep up velocity
    - You know when to get feedback from users or other stakeholders, or when to run a technical experiment (such as train a model) to gather information to decide the next step
    - You make these decisions taking into account the product vision, stage of the project, technical feasibility, key risks, effort, and budget
    - For more mature projects, you know how to define key metrics and project-manage to drive improvements to those metrics

### Making product decisions

- Developers don’t have to become PMs, but you will make decisions the product spec doesn’t cover. If you are asked to build without a spec, you know how to develop one.
    - You have product sense that enables you to pick a product direction that meets real user needs, without having to wait for a PM to make every decision
    - You also have at least a basic design sense, and can build things that aren’t just functional but pleasing to use.
    - Your ability to make product decisions is rooted in your user empathy
        - Further, you continually hone this empathy using a wide range of methods, such as quick informal interviews with 2-3 users, surveys of hundreds of users, large-scale A/B tests, or analyzing the behaviors of thousands or millions of users
        - You use the resulting input to improve your understanding of users

### Communicating and leading

- Your skills in AI Engineering enable you to participate in a broader scope of work than traditional software development allowed
    - You might participate in other functions that affect your project like marketing, finance, legal, and so on
    - This makes your ability to communicate with these other functions more important than before — you can play a key role moving your project forward by aligning and coordinating among stakeholders. (Communication skills also form an important foundation for speaking with users to hone user empathy.)
    - you can explain why certain initiatives may be technically feasible or not. This allows you to help lead your broader organization forward

### High-agency ownership

- many people — including some executives — do not yet understand what AI can do and therefore do not know what are good project directions. This creates an opening for someone with technical skill to bridge this gap
- You can spot problems, propose solutions, and execute on them — being respectful of the organization’s priorities and constraints, but without waiting for precise top-down direction
- This skill requires a high degree of agency, in which you identify opportunities, prioritize what matters, and act on them
- you know how to own an initiative end-to-end, take accountability for issues that arise, act in the face of ambiguity, persist through setbacks, and measure your work not just by task completion, but according to the value you create
- you invest in improving your skills. You track the technology frontier, pick up new tools, tune your workflows, and keep on learning — so you become better over time

## Sources

This note merges the four parts of Andrew Ng’s AI Engineering Skills Map series, published on X between 21 August and 11 September 2026:

1. [Building and deploying AI applications](https://x.com/andrewyng/status/2090840747738374568) — 2026-08-21
2. [Software engineering fundamentals](https://x.com/andrewyng/status/2093388974194872781) — 2026-08-28
3. [Using coding agents](https://x.com/andrewyng/status/2095890279865721217) — 2026-09-04
4. [Shaping the build](https://x.com/andrewyng/status/2098459474608672916) — 2026-09-11
