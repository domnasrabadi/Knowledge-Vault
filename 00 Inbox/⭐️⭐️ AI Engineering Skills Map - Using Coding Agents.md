---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/andrewyng/status/2095890279865721217/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-09-04
author: Andrew Ng
flashcards: none
updated: 2026-09-13
---

# AI Engineering Skills Map: Using coding agents

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/733174243714682880/oyG30NEH.jpg" width="220" />
</div>

- A key AI engineering skill is using coding agents. Your skill at steering them both to write code and to carry out non-code tasks
- allows you to get a lot more done.
- keeping up with how to use coding agents requires a continuous process of experimentation, building, and learning.
- we found a consistent high-level workflow for building software with them.
- key steps are:
- **Planning.** This includes (i) brainstorming, which may include research, experimentation, and understanding the existing codebase (if any) and (ii) writing a spec that captures requirements, technical design, and architecture, followed by generating an execution plan.
- **Execution**, where you build, test, and verify, with the right balance between agent autonomy and human oversight. This involves (i) having the agent build the software, with a calibrated level of agent autonomy and (ii) verifying its output via automated and/or human checks.
- **Deployment and monitoring**, in which you (i) deploy, perhaps gated with a CI/CD pipeline or additional human gates, and (ii) use agents to watch logs, surface issues, and propose and execute improvements.
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
- **Directing the workflow**. You know how to navigate each step of the workflow above.
- This involves deciding how much human and how much agent effort to spend on each and when to go back to an earlier step to iterate.
- requires deeply understanding the tradeoffs of speed, cost, technical risk, and human effort, so you can decide how much to research and plan up front, when to retain human ownership over critical work, how to choose the architecture, how much detail to write into a set of planning artifacts (like a spec), and how to decompose the work into verifiable steps.
- **Enabling agent autonomy**. When applying a coding agent to the steps in the workflow, you choose the autonomy level
- Do you watch it and go back-and-forth interactively or delegate a larger chunk of work to it? And when do you set a clear goal and have it loop until it succeeds?
- As the build proceeds through different phases, you will calibrate when to make sure key learnings, user feedback, and assumptions
- including assumptions that changed partway through the build — are captured for the agent to use downstream.
- you will decide when to set up many agents to run in parallel on a decomposition of the task — either by having a human or a higher-level agent orchestrate these other agents
- **Reviewing the work**. The output of a coding agent is uncertain. We don’t know in advance what good ideas it might come up with and what bugs it will implement.
- Reviewing and verifying the output is a key step to ensure you are getting the result you want and to redirect the agent if not.
- You will design testing and validation that is matched to the task, applying both behavioral and functional verification as needed.
- For qualitative/behavioral evaluation, eval sets, perhaps with LLM-as-a-judge, can be used.
- You also need to decide how much of these tests should be automated.
- Some workflows will have all testing and validation fully automated so the agent can check its work and know when it has succeeded in completing a task.
- When AI review isn’t sufficient, you judiciously insert human reviews of the code behavior (and, infrequently, of code as well) while exploring how to automate this review further.
- **Customizing the agent and its environment**. Your ability to update both the agent and the environment it works in allows your agents to efficiently get the context they need, access tools, and build correctly and efficiently.
- You know how to integrate agent skills, plugins, and MCP servers.
- Occasionally you will prune them when they are no longer necessary (such as when a new model obviates an old skill).
- You can use hooks to automate repeatable parts of the development process, like triggering automated code reviews or CI/CD pipelines.
- You can also maintain the environment the agent works in: updating the standing context (such as [AGENTS.md](http://AGENTS.md) or [CLAUDE.md](http://CLAUDE.md)) with information on the codebase, key architectural assumptions, code style, and data access patterns.
- You know how to preserve state across multiple sessions and across parallel agents, and accumulate agent learnings over time, perhaps by running post-run retrospectives to capture what did and did not work.
- You also know how to set up consistent conventions and structure to make your codebase navigable to the agent, and how to occasionally clear out agent-generated debt.
- **Coding agent foundations**. Finally, to make good decisions throughout, you have a good understanding of how coding agents work
- how they carry out codebase search/retrieval, how they manage their context windows, how different operations (like adding tool calls, MCP servers, etc.) affect context, how agents and subagents interact, and how the agent is built by wrapping a harness around an LLM.
- This makes the agent less of a black box and helps you to recognize failure modes, such as overengineering a simple solution, losing rigor because the agent lacks an explicit verification process, stopping short of the goal, or agent actions that risk destruction of files or production data.
- also helps you reason about the agent’s state and steer it by giving it the right prescription or context.
- this understanding allows you to better spot when the agent goes off-track and requires your intervention.
