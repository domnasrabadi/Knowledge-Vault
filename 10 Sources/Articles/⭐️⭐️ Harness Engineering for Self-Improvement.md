---
type: article
status: raw
quality: 2
topics: [context-engineering, ai-agents]
source: https://lilianweng.github.io/posts/2026-07-04-harness/
created: 2026-08-09
published: 2026-07-04
author: Lilian Weng
flashcards: none
updated: 2026-08-13
---

# Harness Engineering for Self-Improvement

<div align="center">
  <img src="https://lilianweng.github.io/posts/2026-07-04-harness/openai-agent-loop.png" width="220" />
</div>


## Harness Design Patterns

- Compared with [early agent frameworks](https://lilianweng.github.io/posts/2023-06-23-agent/), “agent = LLM + memory + tools + planning + action”, harnesses engineering additionally include *workflow design (e.g. loop engineering), evaluation, permission controls, and persistent state management*.
- The design should be deliberately simple and generic to enable generalization

### Pattern 1: Workflow Automation

- Defining a workflow in which the model can operate, test, and iterate is a key design for automation.
- Karpathy’s autoresearch repo ... common workflow follows a goal-oriented loop of plan, execute, observe/test, improve, and execute again *until* the goal is achieved.

### Pattern 2: File System as Persistent Memory

- A harness should not carry the entire workflow and all logs in context; instead, it should keep durable state in files.
- Learning how to read, write, and edit the file system (commonly via `bash` commands) is a foundation skill for LLMs

### Pattern 3: Sub-agent and Backend Jobs

- A harness can spawn multiple subagents to execute in parallel and monitor backend jobs. This is useful when the main agent needs to search multiple hypotheses, run experiments concurrently, or delegate isolated subtasks without polluting the main context.
- key design choice is to make parallelism explicit and inspectable.

### Harness Layer vs Core Intelligence?

- My prediction of a practical near-term path is:
    1. Harness engineering will evolve in the direction of meta-methodology (i.e. improving the machinery for getting better answers, not just improving the answer itself). The harness system itself becomes an optimization target, with fewer heuristic rules and more general mechanisms.
    2. In turn, mature harnesses enable auto-research for model self-improvement loop and smarter models prevents harnesses from overengineering and keep the system sustainable.
- Eventually it is possible that many harness improvements will be *internalized* into core model behavior, but the interface with external context and tools should remain.
- We have seen a softer version of this pattern with [prompt engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/): manual prompt tricks became less central as instruction tuning and model reasoning improved, but *the need to specify goals, constraints, context, and evaluation did not disappear*.

## Harness Optimization


### Context Engineering

- Context management is a layer to construct a more structed and concise context for LLM and manage persistant states.
- **Agentic Context Engineering** (ACE; [Zhang et al. 2025](https://arxiv.org/abs/2510.04618)) treats context as an evolving playbook rather than an increasingly lengthening prompt.
    1. *Generator*: produces task trajectories, with reference to bullet points.
    2. *Reflector*: distills insights from successful and failed trajectories.
    3. *Curator*: updates the structured context with incremental, itemized entries.
- **Meta-Harness** ([Lee et al. 2026](https://arxiv.org/abs/2603.28052)) moves another level deeper: the optimized object is the *code* that determines and optimizes what information should be stored, retrieved, and presented to the model.
- The proposer for creating a new harness is itself a coding agent and the final output is a collection of harness candidates on the Pareto frontier.
    - The entire execution history is accessible via a file system, and thus the coding agent uses commands like `grep` or `cat` to read through it instead of shoveling everything into a single prompt context.
    - The proposed harness is a dictionary in the file system containing its own source code, scores, rollout trajectories, and state updates.
    - The mete-harness loop iteratively creates new harnesses, and only qualified ones are kept.

### Workflow Design

- The **AI Scientist** system ([Lu et al. 2026](https://www.nature.com/articles/s41586-026-10265-5)) builds a pipeline to propose research ideas, write code, run experiments, analyze results, write a manuscript, and perform peer review.
- **ScientistOne**, where every claim (citation, numerical, methodological, conclusion) must trace to an evidence source and is audited by Chain-of-Evidence checks.

![](https://lilianweng.github.io/posts/2026-07-04-harness/ai-scientist.png)

- The **Autodata** agent ([Kulikov et al. 2026](https://arxiv.org/abs/2606.25996)) is designed to work as a data scientist for generating training and evaluation data. The main agent manages a *challenger* that proposes problems, a *weak solver*, a *strong solver*, and a *verifier/judge*, aiming to synthesize data at the “just right” level of difficulty, meaning that the strong solver succeeds but the weak solver fails.
- In Autodata, the challenger prompt is updated iteratively according to feedback from the solvers and verifier. The limitation here is that synthesized tasks are used to fine-tune weak solvers but not strong solvers; if the loop cannot iteratively improve the strong model, it is more like indirect distillation over a generated prompt distribution, with less RSI flavor.

![](https://lilianweng.github.io/posts/2026-07-04-harness/autodata.png)

- **Automated Design of Agentic Systems** (ADAS; [Hu et al. 2025](https://arxiv.org/abs/2408.08435)) formulates agent design itself as an optimization problem, “meta-agent search” where a meta-agent proposes new designs of agentic workflows.
    1. Initialize an archive of agentic workflows with simple agents such as CoT and self-refine.
    2. Ask a meta-agent to program new agents, all in *code*, inspired by existing solutions in the archive.
        - The meta-agent first generates a high-level description of the new workflow, and then implements it in code.
        - The draft program then goes through two self-refine steps (i.e. ask the model to provide feedback and then ask the same model to refine the previously generated outputs based on the feedback; [Madaan et al. 2023](https://arxiv.org/abs/2303.17651)) by the meta-agent to check its novelty.
    3. Evaluate each new candidate and add successful ones back to the archive.
    4. Repeat steps 2-3 until the maximum iteration count is reached.

### Self-Improving Harness

- Either context engineering or workflow design is only one part of a harness.
- We need to search through the entire design space and optimize context-management logic, workflow, permissions, and many other harness components together.
- In simple words, a harness is code that programs how prompts, tool calls, subagents, control flow, memory, and workflow logic work together.
- **Self-Taught Optimizer** (STOP; [Zelikman et al. 2023](https://arxiv.org/abs/2310.02304)) is one of the early examples of recursive scaffolding improvement. A seed improver $I_0$ at step $t=0$ takes an initial solution $s$, a utility function $u$, and a black-box language model $M$, and returns an improved solution $s'$, that is, $s' = I(u, s; M)$.
- The base model must be *capable enough* to improve the mechanism. This implies that harness improvement enables better deployment of the model but intelligence is still the core.
- more recent work, **Self-Harness** ([Zhang et al. 2026](https://arxiv.org/abs/2606.09498)), relies on LLM agents to improve their own harness via a propose-evaluate-accept loop.
- The loop in Self-Harness has three stages:
    - *Weakness mining*: cluster failures into verifier-grounded failure patterns.
    - *Harness proposal*: propose bounded harness edits based on mined failure patterns.
        - The model is provided with a bounded proposal context:
            1. the editable surfaces of the current harness
            2. the verifier-grounded failure patterns from the evaluation system
            3. records of passing behaviors that should be preserved
            4. summaries of previously attempted edits
        - Harness edits should prefer recurrent error patterns that are addressable (e.g. not task-specific difficulty) and can be resolved by narrow changes.
    - *Proposal validation*: validate and merge qualified edits to create a new harness $h_{t+1}$.
        - Candidate edits are evaluated by regression tests on held-in $D_{\text{in}}$ (for testing whether the weakness is resolved) and held-out $D_{\text{out}}$ (for checking whether other unknown issues were introduced) splits.
        - Candidates are accepted only if they have no regression on both held-in and held-out data.
        - Accepted candidates are merged to update the harness to $h_{t+1}$, while rejected candidates are logged without changing the active harness.

### Evolutionary Search

- Evolutionary search is an optimization method inspired by natural selection
- It evolves a population of solutions by mutating them and only keeping those with high “fitness” in the crowd.
- Evolutionary search comes in handy when:
    1. the search space is extensive or weirdly shaped
    2. it is hard to optimize directly with gradients but easy to evaluate solutions
- Harness search seems to be a good fit here.
- **GEPA** ([Agrawal et al. 2025](https://arxiv.org/abs/2507.19457)) combines [reflection](https://lilianweng.github.io/posts/2023-06-23-agent/#self-reflection)-based prompting with evolutionary search and uses natural language reflection over trajectories of trial and error to propose prompt updates.
- **AlphaEvolve** as a coding-agent evolutionary search system, which stores a pool of candidate programs and prompts frozen LLMs to generate diffs for improvement. As the system repeatedly evaluates child programs and keeps successful ones, it discovers better solutions in time.
- **ThetaEvolve** ([Wang et al. 2025](https://arxiv.org/abs/2511.23473)) combines evolutionary search with RL and in-context learning.
- **ShinkaEvolve** ([Lange et al. 2025](https://arxiv.org/abs/2509.19349)), on the other hand, introduced three new components to improve LLM sampling efficiency
- **Darwin Gödel Machine** (DGM; [Zhang et al. 2025](https://arxiv.org/abs/2505.22954)) explicitly targets the evolution of an editable harness-code repository with an LLM-based coding agent. Precisely, this agent is allowed to modify its own harness.

### Joint Optimization with Model Weights

- Harness evolution changes the non-parametric system around the model.
    - To enable full self-improvement, the model can totally be allowed to update its own weights at the same time.
    - The weight update can be implemented via improvements in the model training pipeline or continual learning at test time.

## Future Challenges

- [Trehan & Chopra (2026)](https://arxiv.org/abs/2601.03315) tested whether LLMs can go from a research idea to a paper with minimal scaffolding and basic tools (i.e., `read_file`, `write_file`, `llm_search`, `list_files`).
    - Each idea had a dedicated workspace where agents could generate and read documents as part of context.
    - They experimented in three domains (world models, multi-agent RL, AI safety & alignment), with each domain containing 45-50 high-quality seed documents to inspire new ideas.
- They observed six recurring failure modes in the experiments:
    - *Bias toward training-data defaults*: use old libraries, stale commands, standard formats, or assumptions not grounded in the actual repository or dataset.
    - *Implementation drift under execution pressure*: when implementation becomes technically complex, the model may move toward a common simpler solution rather than the proposed method.
    - *Memory and context degradation*: long-horizon projects lose critical details unless logs are written as persistent artifacts.
    - *Over-optimism*: the model declares success despite noisy or failed experiments, similarly observed as “p-hacking and eureka-ing” pattern by [Bubeck et al. (2025)](https://arxiv.org/abs/2511.16072) where models can introduce “numerical duct tape” and declare victory when signals are still noise.
    - *Insufficient domain intelligence*: the model lacks tacit craft knowledge, e.g. predicting implementation complexity, judging whether an experimental result is plausible, or knowing which baselines matter.
    - *Weak scientific taste*: experiments may be executable but fail to answer the right question.
- Toward full RSI, researchers have made real progress, but several bottlenecks remain.
    - **1. Weak and fuzzy evaluators.** Many research claims do not have a fast and precise verifier, and the same is true for many real-world tasks. Current self-improvement loops work best for tasks when evaluation metrics are measurable and objective, similar as [how RL works](https://lilianweng.github.io/posts/2018-02-19-rl-overview/).
        - Research taste, novelty, and long-term scientific value are much harder to measure.
    - **2. Context and memory lifecycle.** Memory grows as AI agents become more autonomous and independent. A useful harness needs to manage context and memory to complement existing limitation in long-context generation while still maximizing the success of long-horizon tasks.
    - **3. Negative results.** Researchers are incentivized to publish successful results and thus literature is biased toward successes. LLMs trained on a vast amount of data (mostly human created, at least for now, lol) may be bad at deciding when to abandon a hypothesis, report a negative result, or even acknowledge a failure due to the imablance of success vs failure cases in data.
    - **4. Diversity collapse.** Evolutionary and RL loops tend to exploit known high-reward patterns. We need [mechanisms](https://lilianweng.github.io/posts/2020-06-07-exploration-drl/) to prevent the population from collapsing into variants of the same solution.
    - **5. [Reward hacking](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/).** A self-improvement loop optimizes whatever signal it is given. If the reward comes from unit tests, the agent may overfit to tests; if it comes from a judge model, it may learn reward hacking tricks specific to this judge;
    - **6. Long-term success.** An extrinsic loop of optimization works on rewards outside of individual rollouts that we can simulate in training sandbox.
    - **7. The role of humans.** Humans should move up the stack, not be removed from the loop, meaning that human should provide oversight at the right time, at the right abstraction level and our system design should consider when and how to set up such touch points.
