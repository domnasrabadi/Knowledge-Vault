---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/mardehaym/status/2087086419491647589/?s=12&rw_tt_thread=True
created: 2026-08-16
published: 2026-08-11
author: Mark Ajzenstadt
flashcards: none
updated: 2026-08-16
---

# No Process, No Agent

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1217178205863514112/73FfYSrY.jpg" width="220" />
</div>


### What skipping documentation costs you

- When you deploy an agent against an undocumented process, the agent doesn't pause and ask questions. It fills the gaps with assumptions about handoff points, decision criteria, and escalation rules.
- Documentation means writing down what your team runs today
- Three weeks for a 10-person team's core workflow is normal. Companies skip this because it's tedious and because "we'll figure it out during implementation" feels faster. An agent configured during implementation inherits assumptions about edge cases the implementation team never asked about.
- Documentation also forces decisions. When you write down "if variance exceeds 10%, auto-send standard language," you've made a business decision. Before that sentence exists, three account managers handle the same variance three different ways and an agent can't choose between them.

### The Process Void

- 86% of AI agent pilots never reach production scale.
- I call this the AI bolt-on trap. AI gets added as a feature instead of used to reengineer a process. Companies bolt agents onto broken workflows and wonder why the agent breaks. The gap between intent and outcomes opens from there.
- Unless it's written, it's unreal. Documenting the process is step zero. Before models. Before vendors. Before agent code. And most companies skip it.
- **Why coding agents went vertical**
- Coding agents work because software engineering is the most documented, structured, observable workflow in a company.
- Developers share a common language (code), common tools (Git, CI/CD, IDEs), and common metrics.
- Most enterprise work doesn't have this property. A sales rep needs a feedback loop with the customer before doing additional work on a specific account. A lawyer needs to talk to the client. A doctor needs to interact with the patient. These domains hit a wall that coding never hits: a human has to respond before the agent can continue.
- To get there, you can't bolt agents onto a 15-step manual process. You reengineer that process into 5 steps. AI handles 4. But the reengineering requires documented processes as the starting point, and most companies don't have them.

### Sidekicks vs. background agents

- The enterprise value ratio between AI sidekicks and AI background agents is 1 to 10.
- AI sidekicks require you to prompt them. They handle tasks on the fly and help you move faster through your work, but they don't take work off your plate. Sidekicks bring 10-20% efficiency for the average desk worker, and can cost a fortune if mismanaged.
- AI background agents run on their own. They surface for exceptions, judgments, and other human-in-the-loop events. They remove work from your plate, and the workflows we take on see 60-90% efficiency gains. Production-ready thing versus prompting your way into it is life and day.
- Building a background agent means going deep into a company and mapping how processes run today, including how exceptions get handled. You reengineer those processes for an AI-native future.

### The fix is boring

- **Step 1.** Write down your top 10 workflows. The way they work today, exceptions and workarounds included
- **Step 2.** Connect agents to the system of record
- **Step 3.** Build observability. Once agents run, you need tracing, logging, and telemetry. What the agent decided, why, what it got wrong
