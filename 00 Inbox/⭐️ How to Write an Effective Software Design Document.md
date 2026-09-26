---
type: article
status: inbox
quality: 1
topics: []
source: https://refactoringenglish.com/excerpts/write-an-effective-design-doc/
created: 2026-09-26
published: 2026-06-24
author: refactoringenglish.com
flashcards: none
updated: 2026-09-26
---

# How to Write an Effective Software Design Document

<div align="center">
  <img src="https://refactoringenglish.com/excerpts/write-an-effective-design-doc/og-cover.webp" width="220" />
</div>

- A good design doc can save you years of development time. Writing a design doc forces you to think through important decisions before you waste time on the wrong implementation. It’s also the best way to coordinate design decisions among teammates and partner teams
- Below, I share my approach to creating effective design docs and explain what belongs in a design doc and what does not.
- Little Moments Design Doc
- The design is more exhaustive than what I’d normally write for a solo hobby project, but this is roughly the length and depth of a design doc I’d create if I were coordinating work with other people on a professional project.

### When should you write a design doc?

- The more complex or risky the project, the more valuable it is to write a design doc.
- Consider these questions:
    - Will multiple people coordinate work to implement the design?
    - Will the project take more than three months of full-time dev work?
    - Will the implementation run in production for several years?
    - Does the project involve cross-team collaboration?
    - Are the goals and requirements of the project ambiguous?
    - Are there catastrophic risks you could prevent at design time (e.g., security flaws, legal risks)?
- If you answered “yes” to two or more, a design doc will almost certainly be worth the effort.

### How much should you invest into your design doc?

- A design doc can be a simple one-pager or a 50-page document that requires signoff from five different teams. You need to decide how much detail makes sense.
- The right investment depends on your team’s goals, risks, deadlines, and culture. Sometimes, the right amount to invest in a design doc is zero.

### What belongs in a design doc?

- If you specify every possible detail in a design doc, you’ve essentially written the implementation during the design phase
- As a rule of thumb, you can ask a simple question to decide whether a decision belongs in your design doc: what’s the penalty for being wrong?
- Not all design decisions are equally important. Some choices are more permanent than others.

### Components of a design doc

- common sections to include in your design doc

#### Title

- It’s the way people will refer to your project in conversation, so aim for something short, distinctive, and evocative

#### Metadata

- Boring but useful, metadata helps your reader understand the basic context of your doc:
    - Who is the author? (name + email address)
    - When did you create the doc?
    - What’s the authoritative URL?
    - Especially if your organization uses [shortlink redirects](https://golinks.github.io/golinks/) like `http://go/recency-bank`
    - Who approved this document and when?
    - In cases where your document requires signoff from teammates or partners.

#### Objective


#### Background

- The background section explains the context and motivation for the project. It should answer these questions:
    - Why is the team taking on this project?
    - What problem does this project solve?
    - Were there previous attempts to solve this problem?
- Does your design doc make sense without outside context?
- Imagine what you’d say to a teammate or partner team before they read your design doc.
- Now, realize that some readers will see the doc before hearing any explanation from you, so whatever they need to understand [should be on the first page of your doc](https://refactoringenglish.com/blog/useful-feedback-on-design-docs/#write-an-introduction-that-makes-sense-to-everyone).
- Include links to:
    - Documents from your program manager or testing counterparts on this project (e.g., test plans, functional specs)
    - Design docs for related systems
    - Design docs for previous iterations of this project

#### Goals

- The goals section describes your high-level goals for this project
- Avoid setting goals in terms of implementation details. Your goals should communicate how the project benefits your users, your team, or your company. Bad: Set goals in terms of internal implementation details
    - Add Kubernetes to our infrastructure. Good: Set goals in terms of impact
    - Minimize outages related to deploying new app versions.

#### Non-goals

- While the goals define what’s within your project’s scope, the non-goals section delineates what’s out of scope.

#### Scenarios

- If your goal is something like “Add a ‘Share as URL’ button to charts,” the reader might not understand what that looks like in practice. The scenarios section allows you to paint a picture for your reader of how your completed system works in the real world.
- **Scenario: Share a report via URL** 1. Bob creates a custom report in his KeyMetrics dashboard. 2. Bob navigates to the menu bar and clicks “Share > as URL.” 3. Bob emails the URL to his teammate, Charlie. 4. Charlie clicks the link and sees an exact copy of Bob’s report in read-only mode.

#### Diagrams

- As the design author, you intuitively understand how the pieces of your plan fit together. You can see the architecture in your head. Your reviewers do not have this mental picture, so the fastest way for them to see it is to draw them a picture.
- If you’re not sure what belongs in a diagram, think about these questions:
    - How does data flow through your system?
    - How do the different components of your system fit together?
    - How does your system interact with its dependencies and downstream clients?
    - What communication protocols does your system define?
- [Excalidraw](https://excalidraw.com/), [draw.io](https://www.drawio.com/), and [Google Drawings](https://docs.google.com/drawings/) are popular diagramming tools that facilitate revisions. There are also languages like [Mermaid](https://mermaid.js.org/), [D2](https://d2lang.com/), and [Graphviz](https://graphviz.org/) that allow you to generate diagrams programmatically. I’ve had good experience using an LLM to create diagramming code for me

#### Glossary

- The glossary defines terms that your readers might not recognize.
- When possible, use terms that your audience recognizes without having to refer to a glossary. Defining a term in a glossary is better than not defining it at all, but the best solution is to use recognizable terms or define them inline so that the reader doesn’t have to jump around your document.

#### Constraints

- If there are major constraints imposed on your design by your budget, clients, infrastructure, or dependencies, explain the constraints so the reader understands the context of your design choices.

#### Service level objectives (SLOs)

- An SLO creates a measurable, objective metric for your system’s performance. You’ve probably heard of service level agreements (SLAs). SLAs are just SLOs plus financial penalties for falling short.

#### Monitoring / alerting

- Once you nail down your SLOs ([above](https://refactoringenglish.com/excerpts/write-an-effective-design-doc/#service-level-objectives-slos)), it’s time to think about how you’ll measure them in production.
- When defining your monitoring strategy, ask yourself these questions:
    - If your service goes down, how will you find out?
    - If your service’s performance slows by 100x, how will you know?
    - What other events should trigger an alert?
    - e.g., spikes in CPU usage, authentication failures, system errors

#### Interfaces

- Your project exists to serve people or other software systems, so what do those interactions look like?
    - For graphical systems, what is the user interface?
    - Just simple sketches; don’t get bogged down in precise UI choices.
    - For software interfaces, what are the API or CLI semantics?
    - For file-based interfaces, what is the file format?

#### Dependencies / infrastructure

- The dependencies section should answer questions like:
    - What programming language(s) will you use?
    - On what hardware or service does the code run?
    - Where will persistent data live?

#### Privacy

- The privacy section is an opportunity to think through the sensitive data your system handles and what safeguards you’ll put in place to keep it secure. It should answer these questions:
    - What sensitive data does your system handle?
    - How long will you retain it?
    - Who will have access to it?
    - How will you protect it?
    - e.g., will the data be encrypted at rest and in transit?

#### Legal considerations

- If your system operates in a highly-regulated domain like finance or healthcare, the legal section helps you comply with relevant laws.

#### Logging

- As you think about logging, consider these questions:
    - What critical events does the service log?
    - Are there different log levels?
    - e.g., informational, warning, error, critical
    - Where does the system store its logs?
    - How long do you retain your logs?
    - Who has access to the logs?
    - Is there any sensitive data you must keep out of the logs?

#### Open issues

- As you write your design doc, you’ll likely encounter at least one of the following situations:
    - There’s a flaw in your design, but you’re not sure how to solve it.
    - There’s a gap in your design, but you need to gather more information to close it.
    - You’re torn between multiple solutions. Create an appendix in your design doc called “Open Issues” that documents your outstanding issues. Each entry in the open issues section should explain:
    - What’s the problem that requires more work?
    - What options do you see for resolving the issue?
    - What is the immediate next step for resolving the issue?

#### Resolved issues

- When you resolve an open issue, summarize the decision, and move it from “Open issues” to a “Resolved issues” section in your design doc. Retain the full discussion for posterity.
- **Resolved Issue: Choosing RAM size for cache** **Decision**: Provision 128 GB of RAM to the caching layer. If we’re failing to meet our performance goals and we’re RAM-constrained, we can add more RAM at that point. The dev cost of running tests to discover the perfect RAM size far outweighs the cost of additional RAM. We need to decide… [rest of original open issue goes here]

#### Alternatives considered

- If you anticipate readers asking, “Why didn’t you do X?” it’s helpful to answer that proactively in an “alternatives considered” section. This section is also where you can explain options you rejected, especially if they initially seemed appealing or you researched them extensively. I know some developers who spend hours meticulously documenting their every rejected design idea, but I think that’s overkill. As both a reader and author, all I need in the alternatives section is a few brief lines describing strong alternatives and why they didn’t work.
