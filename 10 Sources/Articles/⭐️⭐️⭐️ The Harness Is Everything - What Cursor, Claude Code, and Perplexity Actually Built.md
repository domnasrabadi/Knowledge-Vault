---
type: article
status: raw
quality: 2
topics:
  - ai-coding
  - context-engineering
  - ai-agents
source: https://x.com/rohit4verse/status/2033945654377283643/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-03-17
author: Rohit
flashcards: none
updated: 2026-08-10
---

# The Harness Is Everything: What Cursor, Claude Code, and Perplexity Actually Built

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2005314466255360000/XtVoqVdV.jpg" width="220" />
</div>

- This article is about what that word actually means, technically and philosophically, because the industry has developed a bad habit of using it loosely. A harness is not a system prompt. It is not a wrapper around an API call. It is not an eval framework or a prompt template or a chatbot with memory. A harness is the complete designed environment inside which a language model operates, including the tools it can call, the format of information it receives, how its history is compressed and managed, the guardrails that catch its mistakes before they cascade, and the scaffolding that allows it to hand off work to its future self without losing coherence.
- This is a detailed technical breakdown of how that idea became the defining insight of applied AI engineering in 2025 and 2026. It covers the research, the real implementations, the failure modes that motivated the design decisions, and the patterns that repeat whether you are building a coding agent, a research agent, or a long-running autonomous software engineer. By the end, you will understand not just what a harness is, but why building one correctly is now the most valuable engineering skill in the industry.

### Why Raw Capability Is Not Enough

- In mid-2024, something strange happened in AI benchmarks. Researchers started noticing that the same frontier model could produce wildly different results on identical coding tasks depending entirely on how the task was presented and what tools were made available
- We have known for decades that the right tools make engineers dramatically more productive. A software developer with a modern IDE, debugger, version control, and CI/CD pipeline is orders of magnitude more effective than the same developer working in a raw terminal with only a text editor
- Everything they know in a given moment is determined by what is in that context window, and everything they produce is conditioned on how that context is structured. The format of the input is not decoration. It is the cognitive architecture of the agent. *The interface is not a convenience layer. For an LM agent, the interface is the mind.*

### The Context Window Is Not a RAM Slot

- The context window is actually closer to the agent's entire working consciousness for a given session. Every token in that window costs computation. Every irrelevant piece of information competes for attention with the relevant information. The model does not have a selective attention mechanism that cleanly ignores noise. The noise is in the room, and it affects the reasoning.
- The ACI solution was to build a search tool that returned a **capped, summarized list** of results. If your search returned more than 50 matches, the tool would suppress the output and tell the agent to narrow its query.

### What an Agent-Computer Interface Actually Is

- Search and Navigation
    - The search component replaced standard grep and find commands with purpose-built tools: find_file, search_file, and search_dir. The key difference was not syntax. The key difference was output management. Results were capped at 50. If a query exceeded that limit, the tool returned a message explaining that there were too many results and prompting the agent to refine its search
    - The reason it matters is that agents, like humans under cognitive load, tend to keep doing what they are doing when they feel uncertain. When a human is lost in a large codebase, they search more and more broadly, generating more and more noise. The capped search tool interrupted this pattern by creating a forcing function. You cannot proceed by being vague. You must be specific. This pushed the agent toward more deliberate, targeted behavior.
- The File Viewer
    - The file viewer is where the paper's insights about cognitive architecture get most concrete. The researchers tested multiple viewer configurations and found that showing 100 lines at a time was a Goldilocks number. Fewer lines (they tested 30) caused agents to lose context about the surrounding code and make editing mistakes. More lines (or the full file) caused agents to lose track of where they were and miss important details.
    - The viewer was stateful. It maintained a position in the file across interactions. And critically, it prepended explicit line numbers to every visible line. This last detail sounds cosmetic. It was not. When an agent needs to issue an edit command targeting lines 47 through 52, it needs to be able to read those numbers directly from the view rather than counting them or performing arithmetic.
- The File Editor With Linting
    - The file editor's key innovation was immediate feedback with guardrails. The edit command accepted a start line, end line, and replacement text as a single operation. After every edit, the tool automatically ran a linter on the modified file and reported the result. If the edit introduced a syntax error, the edit was rejected before it was applied, and the agent received a clear error message showing both the original code and the failed edit.
- **Context Management**
    - The fourth component addressed a problem that compounds over long sessions: the accumulation of stale context. As an agent works through a task, its history fills up with old observations, intermediate states, and exploratory steps that no longer reflect the current state of the environment. All of that history takes up space in the context window and can actively mislead the agent by providing outdated information.
    - The ACI's context management system collapsed older observations, those beyond the last five turns, into single-line summaries
    - The researchers also ran ablation studies, removing one component at a time to isolate the contribution of each design decision. The linter integration was consistently among the highest-leverage components. The capped search was critical for preventing context flooding. The stateful file viewer with line numbers meaningfully outperformed both the raw cat command and simpler viewer designs.

### Why the Context Window Boundary Is the Hard Problem

- what happens when a task is too large to complete in a single context window?
- The naive solution is compaction, and it works to a point
- The failures clustered around two patterns, and both of them are instructive.
- The first failure pattern was attempting to do too much at once
- It would begin implementing feature after feature without completing or testing any of them, run out of context window in the middle of implementation, and leave the next session to start with a half-implemented application, no documentation of what had been done, and no clear indication of what state the code was in. The next agent instance would spend most of its context budget trying to understand the mess rather than making progress.
- The second failure pattern appeared later in projects. After some features had been built, a subsequent agent instance would look around, see that progress had been made, and conclude that the job was done. It would declare victory on a partially-completed application and stop working. This is not stupidity. It is a reasonable inference from incomplete information. The agent had no structured way to know what "done" actually meant for this project.

### The Two-Agent Architecture: Initializer and Coding Agent

- Anthropic's solution was a two-part architecture that has since become a template for how serious teams approach long-running agentic work.
- The first part is an initializer agent. This is a specialized first session with a distinct system prompt whose entire purpose is to set up the environment that all future coding agents will operate in. It does not write features. It creates the scaffolding that makes feature development possible across many subsequent sessions.
- The initializer agent produces three key outputs. First, it creates an [init.sh](http://init.sh) script that can reliably start the development environment. This sounds mundane, but it has significant leverage. Every coding agent session that follows can begin by running [init.sh](http://init.sh) rather than spending tokens figuring out how to start the servers, set up the database, and get the application into a testable state. Saving that overhead in every session accumulates.
- Second, the initializer creates a comprehensive feature list file
- Every feature was initially marked as failing. This file serves as the project's ground truth. A coding agent starting a new session reads this file and immediately knows, with certainty, what has been built and what has not. It cannot look around, see some code, and conclude the job is done. The feature list tells it the truth.
- Third, the initializer creates a claude-progress.txt file and makes an initial git commit. The progress file is a human-readable log that agents update at the end of every session, documenting what they worked on, what they completed, and what state they left things in. Combined with git history, this gives every future coding agent a fast way to orient itself without burning through its context budget on archaeology.
- The second part is the coding agent. Every session after initialization uses a different prompt: work on one feature at a time, leave the environment in a clean state, and update the progress file and git history before the session ends. Incremental progress, documented state, clean handoffs.

### The Feature List as a Cognitive Anchor

- The feature list makes completeness explicit and unambiguous. Each feature has a passes field that is either true or false. An agent either updates this field after verifying a feature works end-to-end, or it does not
- Anthropic made a deliberate decision to store this list as JSON rather than Markdown. The reason is behavioral. Empirically, models are less likely to inappropriately modify or overwrite JSON files compared to Markdown files. JSON has a rigid structure that resists casual editin

### Incremental Progress and the Clean State Requirement

- One of the hardest problems in multi-session agentic work is ensuring that each session ends in a state that the next session can safely build on
- Anthropic's solution was to make clean state a first-class requirement rather than a nice-to-have. Every coding agent session ended with a git commit (with a descriptive message), an update to the progress file, and a reversion to a working state if needed. By "clean state" they meant code that would be appropriate for merging to a main branch: no major bugs, well-documented, in a state where a developer could reasonably begin a new feature without first untangling someone else's half-finished work.
- The git commit was not just a checkpoint. It was a recovery mechanism. When an agent made a change that broke something, it could use git to revert to the last known-good state and try agai

### Testing: The Failure Mode Nobody Likes to Talk About

- solution was to give agents access to the Puppeteer MCP server, a browser automation tool that allowed Claude to actually navigate the application, click buttons, fill forms, and verify that features worked end-to-end. The performance improvement was dramatic. Bugs that were invisible from the code alone became obvious when the agent could see what a user would see.
- This is a concrete illustration of a general principle: the quality of an agent's work is bounded by the quality of its feedback loops

### The Startup Sequence: Getting Up to Speed Fast

- Every coding agent session in Anthropic's harness began with a standardized startup sequence designed to orient the agent as quickly as possible without burning tokens unnecessarily. The sequence was:
- Run pwd to confirm the working directory. Read the progress file and git log to understand recent work. Read the feature list and choose the highest-priority incomplete feature. Run the [init.sh](http://init.sh) script to start the development environment. Run the basic end-to-end test to verify the application was in a working state.

## Part Four: OpenAI's Harness Engineering (Zero Lines of Manual Code)

- In late August 2025, OpenAI's Codex team started a git repository with a single constraint: no human-written code
- Five months later, the repository contained approximately one million lines of code across all of those categories. Roughly 1,500 pull requests had been opened and merged. A small team of three engineers had driven most of this, averaging 3.5 pull requests per engineer per day
- The most important observation in OpenAI's harness engineering article is about how the engineering job itself changed. When your primary job is no longer to write code, what are you doing instead? You are designing environments. You are specifying intent. You are building feedback loops. You are asking, constantly, not "how do I fix this bug?" but "what capability is missing from the environment that is causing this bug to appear?"
- In practice, this meant decomposing large goals into smaller building blocks, building the tools and abstractions that make those building blocks achievable, and using failures as signals about what the environment needed to better support. The human engineers worked depth-first: when an agent got stuck, they did not try to write the code themselves. They asked what was missing, built it into the environment, and let the agent try again.

### Repository Knowledge as the System of Record

- Knowledge that lives in Google Docs, Slack threads, or people's heads is invisible to the system.
- Early in the project, the team tried the "one big [AGENTS.md](http://AGENTS.md)" approach. A single large instruction file containing everything the agent needed to know about the project, the architecture, the conventions, the constraints. It failed predictably, in four ways that are worth understanding.
- First, context is a scarce resource. A giant instruction file crowds out the task, the code, and the relevant documentation. The agent either misses key constraints or starts optimizing for the wrong things. Second, too much guidance becomes non-guidance. When everything is marked as important, nothing is. The agent starts pattern-matching locally instead of navigating intentionally. Third, it rots instantly. A monolithic manual becomes a graveyard of stale rules as the codebase evolves. Fourth, it is hard to verify. A single blob does not lend itself to coverage checks, freshness tracking, or cross-linking. Drift is inevitable.
- The solution was a structured docs/ directory treated as the system of record, with a short [AGENTS.md](http://AGENTS.md) file (roughly 100 lines) serving as a map that pointed to deeper sources of truth elsewhere. Design documentation was catalogued and indexed. Architecture documentation provided a top-level map of domains and package layering. Plans were treated as first-class artifacts with progress and decision logs checked into the repository.
- enabled what the team called progressive disclosure: agents started with a small, stable entry point and were taught where to look next, rather than being overwhelmed upfront

### Enforcing Architecture Without Micromanaging

- One of the most interesting challenges in a fully agent-generated codebase is maintaining architectural coherence over time. Codex replicates patterns that already exist in the repository, including uneven or suboptimal ones. Over time, this leads to drift. Bad patterns spread. Inconsistencies accumulate
- OpenAI's solution was to enforce invariants mechanically, not through human code review. The application was structured around a rigid architectural model: each business domain divided into a fixed set of layers with strictly validated dependency directions and a limited set of permissible edges.

## Part Five: The Awesome Agent Harness Taxonomy

- the ability of AI to write code is effectively a commodity. Foundation models can produce functional code. That is no longer the differentiating capability. The differentiating capability is coordination and environment design.
- Layer 1: Human Oversight
    - At the top is the human oversight layer, where humans approve proposals, review pull requests, and set priorities.
    - The key design principle here is that engineers should be designing environments and reviewing outcomes, not writing code directly. Their leverage comes from steering, not from executing.
- Layer 2: Planning and Requirements (Spec Tools)
    - This layer translates human ideas into structured specifications and task DAGs (Directed Acyclic Graphs) that agents can consume reliably
    - Spec tools force precision at the requirements stage, before any code is written.
- Layer 3: Full Lifecycle Platforms
    - These tools manage the end-to-end process from initial requirements to delivery, integrating AI proposals with human verification gates and sub-agent orchestration
- Layer 4: Task Runners
    - Task runners bridge the gap between issue trackers (GitHub Issues, Linear) and coding agents. The flow is: a human or PM agent creates an issue, the task runner spawns a workspace, the agent delivers a pull request, and the human reviews
- Layer 5: Agent Orchestrators
    - Orchestrators solve the throughput problem by enabling parallel execution of multiple agents while isolating their work in separate git worktrees
- Layer 6: Agent Harness Frameworks and Runtimes
    - Frameworks provide composable primitives for building custom environments: progressive disclosure mechanisms, sub-agent spawning, structured context delivery. Runtimes provide persistent infrastructure: long-running memory, scheduled execution, multi-channel communication between sessions.
- Layer 7: Coding Agents
    - At the bottom is the execution layer: Claude Code, Codex, and similar systems that write, test, and debug code

## Part Six: The Design Patterns That Repeat

- Across all of these systems and all of these organizations, several design patterns appear repeatedly.

### Pattern 1: Progressive Disclosure

- Do not give the agent everything it might need upfront. Give it the minimum it needs to orient itself and the pointers to find more when it needs it
- pattern appears in the SWE-agent's capped search (do not return all results, force the agent to refine), in OpenAI's docs/ architecture (a short map pointing to deeper truth), in Anthropic's startup sequence (read the progress file first, then the feature list), and in the harness frameworks that implement structured context layering.
- The cognitive reason for this pattern is that context is a finite resource, and the agent's attention is not uniformly distributed across it. Information presented at the beginning of a prompt has disproportionate influence. A short, focused entry point that points to richer context elsewhere is more effective than a comprehensive dump that dilutes attention across everything.

### Pattern 2: Git Worktree Isolation

- One agent, one worktree. This pattern appears in every serious orchestration system. The reasoning is straightforward: when you have multiple agents working in parallel (or when a single agent is running tasks in sequence), you need isolation between work streams. Without isolation, parallel agents will step on each other's changes

### Pattern 3: Spec First, Repository as System of Record

- Agents are blind to informal knowledge. Anything that lives in a Slack thread, a Google Doc, or someone's head is invisible to the agent. The only thing the agent can work with is what is in its context window, and the only reliable source for that context is the repository.
- This pattern shows up as the feature list file in Anthropic's harness, as the structured docs/ directory in OpenAI's system, as [AGENTS.md](http://AGENTS.md) files in various open-source frameworks, and as the spec tools layer in the awesome-agent-harness taxonomy. The common thread is that specifications, requirements, architectural decisions, and constraints must be encoded into machine-readable files in the repository before execution begins. If the agent cannot read it from the repo, it does not exist.
- This has an important implication for how engineering teams should document their work. Documentation is no longer just for human readers. It is the mechanism through which human intent becomes legible to agents

### Pattern 4: Mechanical Architecture Enforcement

- Human code review does not scale to agent-driven development. When an agent can open 3.5 pull requests per engineer per day, review cannot be the primary mechanism for maintaining code quality and architectural integrity. The solution is to encode architectural constraints as mechanical checks that run automatically.
- Custom linters, structural tests, and CI pipelines replace much of what code review does in human-driven development. The advantage is that mechanical checks are consistent, fast, and provide immediate feedback at the point of violation
- The key design principle is to enforce invariants, not implementations. You care deeply about dependency directions, boundary crossing, data validation at interfaces, and consistency in naming and structure. You do not care which specific library the agent uses or exactly how a function is decomposed, as long as it satisfies the behavioral contract. This gives agents significant autonomy within a well-defined structure.

### Pattern 5: Integrated Feedback Loops

- Every high-performing harness architecture closes the feedback loop as tightly as possible. Syntax errors caught by linters at edit time. Runtime errors surfaced through observability tools the agent can query. UI bugs caught through browser automation the agent can drive. Test failures returned with context about what broke and where.

## Part Seven: What This Actually Means for Engineers


### The Skill That Transfers

- The harness engineering discipline is, at its core, systems thinking applied to agent environments. It requires you to understand the cognitive architecture of language models well enough to design environments that work with it rather than against it. It requires you to think about state management, feedback loops, error recovery, and context optimization in ways that are familiar from distributed systems engineering but applied to a new domain
- The engineers who are most effective in this emerging paradigm are not the ones with the best prompting skills, though prompting matters. They are the ones who understand how the whole system works: how context flows, where it gets corrupted, how feedback loops can be tightened, how state can be preserved across sessions, and how constraints can be enforced without micromanaging the agent's behavior.

### The Questions You Should Be Asking

- When you are building an agent system and something is not working, the harness engineering mindset produces a different set of questions than the naive mindset.
- Instead of "how do I write a better prompt?" you ask "what information does the agent need that it currently cannot access?" Instead of "why is the model making this mistake?" you ask "what feedback loop is missing that would catch this mistake before it propagates?" Instead of "why is the agent not doing what I told it to?" you ask "what constraint in the environment is preventing the agent from doing what I told it to?"

### The Commoditization of Execution

- If the execution layer is a commodity, then the long-term competitive moat in AI-driven development is not in the model. It is in the harness.
- This means that organizations and individuals who invest in harness engineering, in building the scaffolding, the feedback loops, the observability, the spec tooling, and the orchestration that allows agents to do reliable work at scale, will have a durable advantage over those who are focused primarily on which model to use or how to prompt it.

## Part Eight: Building Your Own Harness


### The Minimal Harness

- The minimal effective harness for a coding agent on a real project has a small number of essential components.
- Start with a persistent progress file. Something the agent reads at the beginning of every session to understand what was done last time, and writes at the end of every session to document what it did. This single change prevents the "declare victory too early" failure mode and ensures continuity across context window boundaries.
- Add a structured task list. Not a vague description of the project, but a specific, enumerated list of verifiable completion criteria. Each item should describe a user-visible behavior that can be tested end-to-end. Mark each item with a status that the agent updates only after verification. This prevents the "partially done looks done" failure mode.
- Add version control with descriptive commit messages as a first-class part of every session. Every session ends with a commit. The agent should not consider its work done until the code is committed and the progress file is updated. This creates the clean handoff that makes multi-session work coherent.

### The Environment Audit

- Ask: what information does the agent need that it does not currently have access to? Where are the points in the task flow where the agent regularly gets stuck or makes mistakes? What feedback is missing that would allow the agent to catch those mistakes itself? Where is context getting polluted with irrelevant information? What constraints need to be enforced that are currently relying on agent judgment?
- Each of these questions points to a specific harness improvement. Missing information becomes a new tool or a new document in the repository. Missing feedback becomes a new test, linter, or observability integration. Context pollution becomes a new context management strategy. Unenforced constraints become new mechanical checks.

## The Last Thing

- Getting the harness right is not a prompt engineering problem. It is a systems engineering problem. And it is the most important engineering problem in applied AI right now.
