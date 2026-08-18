---
type: paper
status: raw
quality: 2
topics: [ai-coding, software-engineering, agent-harnesses]
source: https://arxiv.org/abs/2602.00180v1
created: 2026-08-17
published: 2026-01-30
author: Deepak Babu Piskala
flashcards: none
updated: 2026-08-18
---

# Spec-Driven Development (In the Age of AI Assistants)

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article3.5c705a01b476.png" width="220" />
</div>

### Abstract

- Spec-driven development (SDD) inverts the traditional workflow by treating specifications as the source of truth and code as a generated or verified secondary artifact.
- This paper provides practitioners with a comprehensive guide to SDD, covering its principles, workflow patterns, and supporting tools.
- We present three levels of specification rigor-spec-first, spec-anchored, and spec-as-source-with clear guidance on when each applies.

### Introduction

- For decades, code has been the king of software development.
    - Requirements documents exist, but they drift.
    - Design diagrams are drawn, but they rot.
    - Tests are written, but often after the fact.
    - The code—whatever it actually does—becomes the de facto truth of the system.
- Spec-driven development (SDD) offers an alternative: *make the specification the source of truth, and let code derive from it*.
    - Instead of coding first and documenting later (or never), teams write clear specifications of intended behavior, then generate, implement, or verify code against those specifications.
    - The spec becomes the authoritative description that both humans and machines use to understand, build, and maintain the system.
- AI models are excellent at pattern completion but poor at mind reading.
    - "vibe coding"—relying on loose prompts that lead to inconsistent or erroneous outputs from LLMs.
- **The Core Principle:** In spec-driven development, code is the implementation detail of the specification—not the other way around. The spec declares intent; the code realizes it.

### The Specification Spectrum

- Not all spec-driven approaches are equal. Teams adopt different levels of rigor depending on their needs, tooling, and domain constraints.
- In **spec-first** development, a specification is written before coding to guide the initial implementation.
    - Spec-first represents the entry point to SDD. Before writing code, the developer or team articulates what the code should do, typically as a user story with acceptance criteria
    - The defining characteristic of spec-first development is that the specification is written before implementation begins, ensuring that developers have a clear target before they start coding.
    - Once code exists, the spec may or may not be maintained—the primary value is in the initial clarity it provides.
        - The spec guides implementation, but once the code is written and tests pass, the spec may be discarded or allowed to drift.
        - the spec may become outdated as the code evolves through subsequent iterations.
        - This approach carries a lower maintenance burden than stronger specification disciplines, making it practical for teams that cannot commit to ongoing spec maintenance.
    - Spec-first works particularly well for initial feature development when working with AI coding assistants. The upfront spec prevents the AI from guessing at requirements, dramatically improving the quality of generated code.
        - It is also valuable for prototypes and one-off features where the cost of maintaining a spec alongside code indefinitely is not justified.

#### Spec-Anchored: Living Documentation

- In **spec-anchored** development, the specification is maintained alongside the code throughout the system's lifecycle. Changes to behavior require updating both the spec and the code, keeping them synchronized.
    - Spec-anchored development treats the spec as a living document that evolves with the codebase. When a feature changes, the spec is updated first or simultaneously with the code.
    - Automated checks—typically in the form of tests derived from the spec—ensure that spec and code remain aligned. If they drift, tests fail, providing immediate feedback that the system's documentation no longer reflects its behavior.
        - The spec serves as always-up-to-date documentation that developers and stakeholders can trust. However, maintaining this alignment requires discipline and tooling support—teams must commit to updating specs whenever behavior changes.
- Spec-anchored is the sweet spot for most production systems. It provides the benefits of clear documentation and verifiable requirements without demanding that code be fully generated from specifications.

#### Spec-as-Source: Humans Edit Specs, Machines Generate Code

- In **spec-as-source** development, the specification is the only artifact humans edit directly.
    - Code is entirely generated from the spec and should never be manually modified.
    - Any change to behavior means changing the spec and regenerating.
- Spec-as-source represents the most radical form of SDD.
    - The specification becomes, in effect, the source code—just expressed at a higher level of abstraction.
    - fundamentally inverts the traditional relationship between specs and code: the specification is the primary artifact, and code is entirely derived from it.
    - requires mature, trusted generation tooling—developers must have confidence that generated code correctly implements the spec.
    - drift is eliminated by design: since code is regenerated rather than manually edited, spec and code are always aligned by construction.
- Spec-as-source is already standard practice in domains with well-defined code generation, such as generating API server stubs from OpenAPI specifications

### The SDD Workflow

#### Phase 1: Specify

- The specify phase answers a fundamental question: *What should the software do?* The output is a functional specification describing behavior, requirements, and acceptance criteria
    - During this phase, teams articulate user-facing behavior through user stories, scenarios, and acceptance criteria.
        - They define what success looks like using Given/When/Then format or input-output examples.
    - Business rules and constraints are captured explicitly, and edge cases and error conditions are identified upfront rather than discovered during implementation.
- Good specs share several characteristics:
    1. They are behavior-focused, describing what happens rather than how.
    2. They are testable, with each requirement being verifiable.
    3. They are unambiguous, meaning different readers reach the same interpretation.
    4. They are complete enough to cover essential cases without over-specifying.
- Write specs at the level of detail needed to remove ambiguity.

#### Phase 2: Plan

- The plan phase answers a different question: *How should we build it?*
    - Where the spec declares intent, the plan declares constraints on implementation.
- Planning involves:
    1. selecting technologies and frameworks appropriate to the problem
    2. defining component architecture and boundaries
    3. designing data models and schemas
    4. specifying interfaces including APIs, messages, and contracts
    5. identifying non-functional requirements around performance, security, and scalability

#### Phase 3: Implement

- The implement phase produces working code that realizes the spec according to the plan. In traditional development, this is where most effort concentrates. In SDD, particularly with AI assistance, this phase may be substantially automated—but it still requires human oversight.
    - Implementation begins by breaking the plan into discrete, reviewable tasks.
    - Code is reviewed against both spec and plan to verify alignment. Unit tests are written to encode spec requirements as executable assertions.
- A key SDD principle is working in small, validated increments. Rather than implementing the entire spec at once, teams break work into tasks where each delivers a testable piece of functionality.
    - enables frequent checkpoints where humans verify alignment, catching drift early before it compounds.

#### Phase 4: Validate

- *Does the code actually meet the spec?* Validation closes the loop, ensuring that what was specified is what was built. This phase combines automated verification with human judgment.
- If validation reveals gaps—the code doesn't meet the spec—the team faces a decision: fix the code or revise the spec.
    - If the original spec was wrong or incomplete, updating it is the right choice.
    - If the code simply doesn't meet a valid spec, fixing the code is required.
    - Either way, the spec remains the authority.

### How SDD Boosts AI Coding Agents

- Specifications act as super-prompts that break down complex problems into modular components aligned with agents' context windows.
    - This boosting effect is particularly evident in scalable scenarios: specifications enable parallel agent execution on non-overlapping tasks, with orchestration for dependencies.
        - Teams can partition work at the spec level, allowing multiple AI agents to implement different components simultaneously
- Challenges remain, including LLM non-determinism—even structured specs can lead to varying outputs.
- An emerging approach involves "self-spec" methods where LLMs author their own specifications before generating code. The agent first produces a spec from a high-level prompt, which is then reviewed and refined by humans before the same or another agent implements against it.

#### Behavior-Driven Development (BDD) Frameworks

- BDD frameworks allow teams to write specifications in near-natural language that can be executed as tests.
    - The canonical format is Gherkin, which uses structured scenarios with Given/When/Then clauses:

      ```gherkin
      Feature: Shopping Cart
        Scenario: Adding item to empty cart
          Given the cart is empty
          When I add item "Widget" to the cart
          Then the cart should contain 1 item
          And the item should be "Widget"
      ```

#### API Specification Tools

- In API development, spec-driven approaches have been standard practice under the names "design-first" or "API-first" for years.
    - The benefit of API specification tools is clear: once the API spec is agreed upon, frontend and backend teams can work in parallel with confidence.

#### AI-Assisted SDD Tools

- Emerging tools structure AI coding workflows explicitly around specifications, recognizing that multi-step prompting with explicit artifacts yields better results than single-shot "just code this" prompts.
    - GitHub Spec Kit is an open-source toolkit providing commands for spec-driven AI development. The workflow follows four explicit phases:
        1. `/specify` generates a detailed spec from a prompt.
        2. `/plan` creates technical architecture.
        3. `/tasks` breaks the plan into implementation tasks.
        4. Implementation generates code task by task.

### The Redefinition of Developer Work

- Work is being redefined as developers shift from manual coding to orchestrating specifications, reviewing AI outputs, and focusing on high-level design.
    - This transition potentially increases efficiency but introduces new challenges around spec maintenance, tool mastery, and the judgment required to know when AI outputs are correct.
- In greenfield projects, developers become architects who design systems through specifications rather than code.
    - They focus on requirements elicitation, constraint definition, and acceptance criteria—the "what" rather than the "how." AI agents handle the translation from spec to implementation, but humans remain responsible for ensuring specs capture actual requirements.
- In brownfield projects and legacy systems, SDD enables a different kind of work: encoding existing behavior as specifications before making changes.
    - By extracting specs from legacy code, teams can verify that modernization efforts preserve required functionality while eliminating undocumented behaviors. The spec becomes the bridge between old and new implementations.

### When to Use SDD

- Spec-driven development is not universally applicable. Like any practice, it has costs—upfront spec effort, tooling investment, and discipline requirements—and benefits—clarity, quality, and maintainability.
- SDD adds clear value when using AI coding assistants, as specifications dramatically improve output quality by removing the ambiguity that forces AI to guess.
    - Complex requirements benefit from SDD because stakeholders can validate that the system meets their needs before code
    - Integration-heavy systems gain from API specs that enable parallel development and prevent integration failures.
    - Regulated domains often mandate traceability from requirements to implementation
- However, SDD may be overkill in certain situations. Throwaway prototypes don't justify spec investment that will be discarded.
    - Solo, short-lived projects may find the overhead exceeds benefits when there's only one developer and no long-term maintenance.
- **The Golden Rule:** Use the minimum level of specification rigor that removes ambiguity for your context.
    1. Spec-first for AI-assisted initial development.
    2. Spec-anchored for long-lived production systems.
    3. Spec-as-source only when generation tooling is mature and trusted.

### Common Pitfalls

- Over-specification occurs when teams write specs that are too detailed, essentially becoming pseudo-code.
- Specification rot affects spec-anchored approaches when teams fail to update specs as code changes. The spec drifts from reality, losing its value as documentation and eroding trust.
- Specification as bureaucracy emerges when specs become forms to fill out rather than tools for clarity. If the specification process adds overhead without improving understanding or quality, teams will game the system or abandon i
- Tooling complexity can overwhelm teams, particularly with AI-assisted tools that generate elaborate artifacts. Teams may drown in generated plans, task lists, and intermediate documents.
    - solution is to start simple and add tooling complexity only when it demonstrably helps
- False confidence is perhaps the subtlest pitfall.
    - A passing spec test doesn't guarantee correct software—it only guarantees that the software matches the spec.
    - If the spec is wrong, the code will faithfully implement the wrong thing.
