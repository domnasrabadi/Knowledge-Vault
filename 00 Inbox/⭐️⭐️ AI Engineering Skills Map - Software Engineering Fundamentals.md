---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/andrewyng/status/2093388974194872781/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-08-28
author: Andrew Ng
flashcards: none
updated: 2026-09-13
---

# AI Engineering Skills Map: Software engineering fundamentals

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/733174243714682880/oyG30NEH.jpg" width="220" />
</div>

- Even when you use a coding agent to write all your code, understanding software fundamentals is important for steering your agent to make the tradeoffs you want — or to even know what tradeoffs exist to be made.
- A novice who vibe codes without understanding software fundamentals can create simple applications, but this often leads to the coding agent making bad tradeoffs in latency, availability, consistency, reliability, maintainability, simplicity, and/or cost. In such cases, the developer didn’t know such tradeoffs even existed and therefore did not steer the agent to make the right decisions for their application context.
- requires being skilled at:
    - Building full-stack applications
    - Managing data
    - Designing system architectures
    - Making systems secure and reliable
    - Scaling and operating in production
- **Building full-stack applications.** Agentic coding enables many developers who previously played more specialized roles (like front-end developer or mobile developer) to play a broader, full-stack role.
- A coding agent can help with parts of the development process that you might be less familiar with. However, understanding how the full stack actually works is important.
- **Managing data.** Data deserves special attention because it is a foundation that software is built on top of, that is relatively hard to change
- When you know how to manage data, you can think through access patterns and use them to decide what to store and for how long. You can identify the right data models and select the appropriate storage types (such as relational tables, documents, key-value, or graphs) and infrastructure, which in turn affects speed, scalability, availability, reliability, and cost.
- You understand transactions, concurrency, and how to ensure your data is clean, consistent, and fresh.
- Deciding how to manage data requires significant human-provided context. Your AI systems will get their own input context from your data source, so if data architecture is chosen poorly, the AI doesn’t know what it doesn’t know.
- **Designing system architectures.** When you understand the major components of the full stack of software and data, you are then better positioned to decide how to put the pieces together.
- Good system design requires understanding what the software is intended to do (how many users? how important is latency? how important is cost? etc.) so you can make choices about the application platform, the boundary between the frontend and backend, system decomposition, application state placement, and architectural granularity (monolith vs. microservices).
- You will also choose the stack (programming languages, runtimes, component/frontend/backend frameworks, data technologies) — sometimes by running experiments to evaluate options before settling on one.
- Further, the right architecture is a moving target, depending on the phase of the project.
- The simple architecture you choose to build a quick prototype may not be the right architecture to build the first production system, and that too may change as the application scales.
- **Making systems secure and reliable.** To build reliable systems, you should know how to develop testing strategies to verify the correctness of your system: What mix of unit tests and integration tests, what frameworks to use, and what level of coverage.
- You also know how to design around possible failures — how to handle failures (like an API hitting a rate limit), build in graceful degradation, and minimize the blast radius of failures.
- You can now use AI tools to scan your code for vulnerabilities, check dependencies for supply chain injections, and examine your cloud configuration for attack surfaces. But doing this well still requires some knowledge of security.
- **Scaling and operating in production.** To serve real users, you will have to know how to deploy your software to production.
- You will benefit from knowing how to execute the software development lifecycle (SDLC) which, in addition to building and testing, includes configuring the deployment environment, deciding on release strategy, applying deployment automation (CI/CD), and understanding infrastructure as a service (IaaS).
- Operating in production requires putting in place observability tools, setting alerts, and managing incidents.
- Lastly, to scale your application, you should understand the real load and know how to scale servers, load-balance, and adapt your data infrastructure (via sharding, indexing, replication) or make architecture changes to allow your system to adapt to scale.
- Finally, understanding coding best practices like version control, code reviews, dependency maintenance, and how to manage technical debt helps you keep evolving your system over time.
- Some parts of coding knowledge — like memorizing coding syntax — are becoming obsolete. But developers who deeply understand how software works vastly outperform those who vibe code without understanding.
