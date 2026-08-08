---
type: article
status: inbox
quality: 1
topics: []
source: https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html
created: 2026-08-08
published: 2025-10-15
author: Birgitta Böckeler
flashcards: none
updated: 2026-08-08
---

# Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl

<div align="center">
  <img src="https://martinfowler.com/articles/exploring-gen-ai/donkey-card.png" width="220" />
</div>


### Definition

- Spec-driven development means writing a “spec” before writing code with AI (“documentation first”). The spec becomes the source of truth for the human and the AI.
- [GitHub](https://github.com/github/spec-kit/blob/main/spec-driven.md): “In this new world, *maintaining software means evolving specifications*. […] The lingua franca of development moves to a higher level, and code is the last-mile approach.” [Tessl](https://docs.tessl.io/introduction-to-tessl/concepts): “A development approach where *specs — not code — are the primary artifact*. Specs describe intent in structured, testable language, and agents generate code to match them.”
- in reality, there are multiple implementation levels to it:
- • **Spec-first**: A well thought-out spec is written first, and then used in the AI-assisted development workflow for the task at hand. • **Spec-anchored**: The spec is kept even after the task is complete, to continue using it for evolution and maintenance of the respective feature. • **Spec-as-source**: The spec is the main source file over time, and only the spec is edited by the human, the human never touches the code.

### What is a spec?

- A spec is a structured, behavior-oriented artifact - or a set of related artifacts - written in natural language that expresses software functionality and serves as guidance to AI coding agents. Each variant of spec-driven development defines their approach to a spec’s structure, level of detail, and how these artifacts are organized within a project.
- There is a useful difference to be made I think between specs and the more general context documents for a codebase. That general context are things like rules files, or high level descriptions of the product and the codebase

![](https://martinfowler.com/articles/exploring-gen-ai/sdd-overview.png)


### The challenge with evaluating SDD tools

- turns out to be quite time-consuming to evaluate SDD tools and approaches in a way that gets close to real usage. You would have to try them out with different sizes of problems, greenfield, brownfield, and really take the time to review and revise the intermediate artifacts with more than just a cursory glance

### Kiro

- **Workflow:** Requirements → Design → Tasks
- **Requirements:** Structured as a list of requirements, where each requirement represents a “User Story” (in “As a…” format) with acceptance criteria (in “GIVEN… WHEN… THEN…” format)
- **Tasks:** A list of tasks that trace back to the requirement numbers, and that get some extra UI elements to run tasks one by one, and review changes per task.

### Spec-kit

- [Spec-kit](https://github.com/github/spec-kit) is GitHub’s version of SDD. It is distributed as a CLI that can create workspace setups for a wide range of common coding assistants. Once that structure is set up, you interact with spec-kit via slash commands in your coding assistant. Because all of its artifacts are put right into your workspace, this is the most customizable one of the three tools discussed here.
- **Workflow:** Constitution → 𝄆 Specify → Plan → Tasks 𝄇
- Spec-kit’s memory bank concept is a prerequisite for the spec-driven approach. They call it a [**constitution**](https://github.com/github/spec-kit/blob/main/spec-driven.md#the-constitutional-foundation-enforcing-architectural-discipline). The constitution is supposed to contain the high level principles that are “immutable” and should always be applied, to every change. It’s basically a very powerful rules file that is heavily used by the workflow.
- In each of the workflow steps (specify, plan, tasks), spec-kit instantiates a set of files and prompts with the help of a bash script and some templates. The workflow then makes heavy use of checklists inside of the files, to track necessary user clarifications, constitution violations, research tasks, etc. They are like a “definition of done” for each workflow step (though interpreted by AI, so there is no 100% guarantee that they will be respected).

### Tessl Framework

- Tessl is the only one of these three tools that explicitly aspires to a spec-anchored approach, and is even exploring the spec-as-source level of SDD
- A Tessl spec can serve as the main artifact that is being maintained and edited, with the code even marked with a comment at the top saying `// GENERATED FROM SPEC - DO NOT EDIT`. This is currently a 1:1 mapping between spec and code files, i.e. one spec translates into one file in the codebase. But Tessl is still in beta and they are experimenting with different versions of this, so I can imagine that this approach could also be taken on a level where one spec maps to a code component with multiple files
- Putting the specs for spec-as-source at a quite low abstraction level, per code file, probably reduces amount of steps and interpretations the LLM has to do, and therefore the chance of errors. Even at this low abstraction level I have seen the non-determinism in action though, when I generated code multiple times from the same spec. It was an interesting exercise to iterate on the spec and make it more and more specific to increase the repeatability of the code generation

### Observations and questions


#### One workflow to fit all sizes?

- When I asked Kiro to fix a small bug ([it was the same one I used in the past to try Codex](https://martinfowler.com/articles/exploring-gen-ai/autonomous-agents-codex-example.html)), it quickly became clear that the workflow was like using a sledgehammer to crack a nut. The requirements document turned this small bug into 4 “user stories” with a total of 16 acceptance criteria, including gems like “User story: As a developer, I want the transformation function to handle edge cases gracefully, so that the system remains robust when new category formats are introduced.”
- I had a similar challenge when I used spec-kit, I wasn’t quite sure what size of problem to use it for.
- With the amount of steps spec-kit took, and the amount of markdown files it created for me to review, this again felt like overkill for the size of the problem. It was a bigger problem than the one I used with Kiro, but also a much more elaborate workflow. I never even finished the full implementation, but I think in the same time it took me to run and review the spec-kit results I could have implemented the feature with “plain” AI-assisted coding, and I would have felt much more in control.
- An effective SDD tool would at the very least have to provide flexibility for a few different core workflows, for different sizes and types of changes.

#### Reviewing markdown over reviewing code?

- can see in the description of the tool above, spec-kit created a LOT of markdown files for me to review. They were repetitive, both with each other, and with the code that already existed
- In Kiro it was a little easier, as you only get 3 files, and it’s more intuitive to understand the mental model of “requirements > design > tasks”
- An effective SDD tool would have to provide a very good spec review experience.
- Even with all of these files and templates and prompts and workflows and checklists, I frequently saw the agent ultimately not follow all the instructions
- The past has shown that the best way for us to stay in control of what we’re building are small, iterative steps, so I’m very skeptical that lots of up-front spec design is a good idea, especially when it’s overly verbose. An effective SDD tool would have to cater to an iterative approach, but small work packages almost seem counter to the idea of SDD.

#### How to effectively separate functional from technical spec?

- underlying aspiration I guess is that ultimately, we could have AI fill in all the solutioning and details, and switch to different tech stacks with the same spec.
- In reality, when I was trying spec-kit, I frequently got confused when to stay on the functional level, and when it was time to add technical details
