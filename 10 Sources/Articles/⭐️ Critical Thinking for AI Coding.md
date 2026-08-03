---
type: article
status: raw
quality: 1
topics: [ai-coding]
source: ""
created: 2025-12-29
published: 2023-09-19
author: Andrew Stellman
flashcards: none
updated: 2026-01-10
---

# The Sens-AI Framework: Critical Thinking Habits for Coding with AI

<div align="center">
  <img src="https://learning.oreilly.com/covers/urn:orm:book:0642572243326/" width="220" />
</div>

Source: https://learning.oreilly.com/library/view/critical-thinking-habits/0642572243326/ch01.html#ch01_context_1759972476708469

Exported at: `2026-01-01T05:31:12Z`

- These AI tools can help speed up routine work, encourage exploration of new approaches, and generate ideas that might not have come up otherwise
- **Vibe coding** is an exploratory, prompt-first approach to software development where developers rapidly prompt, get code, and iterate.
- Vibe coding offloads detail to the AI, making exploration and ideation fast and effective,
- Knowing when to slow down, review, and stay engaged can be a challenge, even for experienced developers.
- When AI generates large volumes of code quickly, comprehensive review becomes impractical.
- For new and early-career developers, this can create a critical skill-building gap: *they may* *miss learning essential practices* like readability, separation of concerns, design patterns, architecture, and more generally, getting a feel for writing and reading code.
- Even experienced developers can slip into habits that seem productive but create problems down the line, like accepting AI suggestions without questioning them, skipping design discussions, or pushing unreviewed code too quickly.
- Those experiences led me to design the **Sens-AI Framework**. It consists of five structured habits
- using it successfully means regularly reviewing the generated code, watching for signs of **technical debt**, or the accumulated shortcuts and compromises that make code harder to maintain.
- The signals of AI-accelerated technical debt show up quickly: highly coupled code where modules depend on each other’s internal details; “God objects” with too many responsibilities; overly structured solutions where a simple problem gets buried under extra layers. These are the same problems that typically reflect technical debt in human-built code; the reason they emerge so quickly in AI-generated code is because it can be generated much more quickly and without oversight or intentional design or architectural decisions being made.
- Left to its defaults, AI-assisted development is biased toward adding new code, not revisiting old decisions.
- When developers add features, they usually work with an understanding of the existing architectural patterns, helper functions, and design philosophy.
- An AI, however, doesn’t have that holistic view. It’s trained on a massive dataset of code, but when generating a solution it’s focused mainly on the immediate task. That tight focus often leads to common code generation failures:
- Duplication The AI generates a function that repeats the logic of an existing one. This makes the codebase larger and harder to maintain, and if a bug is found in one version, it has to be fixed everywhere it appears.
- Lack of integration The AI creates new methods, functions, classes, or modules instead of extending existing ones. This misses chances to apply design patterns and principles, resulting in a less cohesive design that becomes rigid and harder to extend.
- Over-abstraction The AI generates extra layers of classes, interfaces, or helper functions that don’t add real value. This increases complexity, makes the code harder to follow, and over time creates the same rigidity and maintenance headaches as duplication or poor integration.
- The discipline to avoid technical debt comes from building design checks into your workflow so AI’s speed works in service of maintainability instead of against it.
- The **rehash loop** is a failure mode in AI-assisted development characterized by repeated prompt-and-response cycles that produce variations without meaningfully addressing the underlying problem.
- One source of the problem is the **context window**: a fixed-size buffer that determines how much text the model can “see” at once.
- The variations you get, like reordered statements, renamed variables, a tweak here or there, aren’t new ideas. They’re just the model nudging things around in the same narrow probability space. It’s still pointing at the same chunk of its training data.
- While rehash loops seem like a frustrating problem, developers can also use them positively by recognizing that *a rehash loop is a signal that the AI ran out of context*. When you’re stuck in a rehash loop, treat it as a signal instead of a problem. All you need to do to break out of the loop and resume productive use of the AI is figure out what context is missing and provide it.
- Developers early in their learning path, however, face what I call the **cognitive shortcut paradox**: they need coding experience to use AI tools well, because experience builds the judgment required to evaluate, debug, and improve AI-generated code, but leaning on AI too much in those first stages can keep them from ever gaining that experience.
- The question isn’t whether to use AI in learning, but how to use it in ways that build rather than bypass the critical thinking abilities that separate effective developers from code generators.
- The Sens-AI Framework is built around **five structured habits** that help developers collaborate effectively with AI while preserving the critical thinking and design judgment that distinguish good software engineering.
- Context Providing the AI with the right background, requirements, and constraints. *Ensure prompts provide the necessary context for the AI.*
- Research Investigating the problem space before prompting. *Do additional research when initial attempts feel shallow or incomplete, or run into problems, like when you hit a rehash loop.*
- Problem Framing Clarifying prompts to define problems precisely. *Reframe the problem when AI responses miss the mark or seem confused.*
- Refining Iterating deliberately on prompts and responses. *Use iteration to break out of rehash loops and improve output quality.*
- Critical Thinking Carefully reviewing and questioning AI-generated code. *Break out of the vibe coding loop regularly, read what the AI produced, and question it as if it came from a teammate’s pull request. Without this deliberate pause, small errors can pile up into long-term problems.*

### Context

- Context is the foundation of effective AI-assisted development. It defines the information, constraints, and goals you provide to guide the AI’s work. Providing context means giving the AI problem details, requirements, domain knowledge, architecture constraints, and expectations for the code you want to generate.

### Research

- Research is the habit of deliberately investigating the problem space when the AI’s initial response falls short of solving your real problem.
- Research is how *you* notice where responses miss the mark, figure out what’s lacking, and supply the missing insight to steer the AI more precisely.
- Building a Research habit means recognizing that an incomplete response from the AI is often just a step toward getting the right answer. It helps you to see these moments not as failure, but as a signal for you to do the extra work—often just a small amount of targeted research—that gives the AI the information it needs to get to the right place in its massive information space.

### Problem Framing

- Problem Framing is the habit of transforming your understanding into a clear, precise question that the AI can answer.
- Effective Problem Framing involves rewording questions, adding missing context, explicitly stating constraints, or breaking complex problems into clearer sub-problems.
- Problem Framing builds directly on the work you did in Research. It turns the information you gathered into an actionable, targeted question that can steer the AI away from default, safe responses and toward something genuinely useful.

### Refining

- Refining is the habit of iterating deliberately on your prompts and the AI’s responses to move closer to a genuinely useful solution.
- Refining means treating the process as a conversation where you evaluate what the AI produced, identify what’s missing or off-target, and adjust your prompt to steer it more effectively. It turns prompting from a single-shot request into an iterative, collaborative design process where your critical thinking remains in the loop.
- Refining is what ties the other habits together through this cycle of evaluation and improvement. When the AI’s response misses the mark, it helps you consider: Is the context insufficient? Do you need more research? Should you reframe the problem? Refining helps you decide whether to tweak your current prompt or step back to an earlier habit.

### Critical Thinking

- Critical Thinking is the practice of carefully reviewing and questioning the code AI generates before you accept or ship it, and it’s the capstone habit of this framework.
- But under that surface-level polish, there can be subtle bugs, poor design decisions, security risks, or maintainability issues.
- Critical Thinking is about slowing down enough to review, question, and verify: Does this code really solve the problem? Does it handle edge cases? Is it secure, maintainable, and aligned with our design goals?
- AI generates a lot of code, and it’s simply not practical to review every line in detail every time it regenerates. In fact, trying to read all of it can lead to **cognitive overload**, or the mental exhaustion from trying to understand too much code at once, and makes you hesitant to discard code that isn’t working simply because you already spent time reading it.
- A better approach is to use your critical thinking early in the loop
- *Unit tests are a practical tool for enforcing critical thinking*. If you ask the AI to generate a class, also have it generate unit tests. When adding or updating a unit test feels unreasonably difficult, that’s often the first sign the design is too rigid.
- If writing tests for the AI’s code proves difficult, requiring excessive mocking, too many dependencies, or modifications to unrelated parts, that’s a *clear signal the design is too coupled or unclear*.
- Another practical technique is to let the AI help you by generating unit tests that validate the behavior you want, review those tests, and then have the AI lock in that behavior.
- What AI still can’t do is tell you when a design or architecture decision today will cause problems six months from now, or when you’re writing code that doesn’t actually solve the user’s problem. That’s why being a generalist—with skills in architecture, design patterns, requirements analysis, and even project management—is becoming more valuable on software teams.
- Talking about prompt engineering today is really just continuing a much older conversation about how developers spell out what they need built, under what conditions, with what assumptions, and how to communicate that to the team.
- Prompt Engineering *Is* Requirements Engineering
- Prompt engineering and requirements engineering are literally the same skill: using clarity, context, and intentionality to *communicate your intent* and ensure what gets built matches what you actually need.
- Decades later, the points Brooks made in his “No Silver Bullet” essay still hold. There’s no single template, library, or tool that can eliminate the essential understanding what needs to be built.
- Adapting traditional requirements engineering skills to prompt engineering shows up in practice in several ways:
- Context and shared understanding are foundational Good requirements help teams understand what behavior matters and how to know when it’s working, which involves capturing both functional requirements (what to build) and non-functional requirements (how well it should work).
- Scoping takes real judgment Developers who struggle to use AI for code routinely fall into two extremes: providing too little context (a single sentence that produces something that looks right but fails in practice) or pasting in entire files expecting the model to zoom in on the right method.
- Context drifts, and the model doesn’t know it’s drifted With human teams, understanding shifts gradually through check-ins and conversations; without that interaction, the team’s understanding of the problem can slowly drift away from what they’re supposed to be building. With prompting, drift can happen in just a few exchanges. The model might still be generating fluent responses until it suggests a fix that makes no sense. That’s a signal that the context has drifted, and you need to reframe the conversation, perhaps by asking the model to explain the code or restate what it thinks it’s doing.

### Trust but Verify: Learning to Catch What AI Misses

- “Trust but verify” is the cornerstone of an effective approach: trust the AI for a starting point, but verify that the design supports change, testability, and clarity. That means applying the same critical review patterns you’d use for any code: checking assumptions, understanding what the code is really doing, and making sure it fits your design and standards.
- Verifying AI-generated code means reading it, running it, and sometimes even debugging through it line by line. It can involve making sure that it’s readable, for example by asking yourself whether the code will still make sense to you (or anyone else) months from now.
- Verifying also means taking specific steps to check both your assumptions and the AI’s output, like *generating unit tests for the code*,
- AI can help with this verification too: it can suggest refactorings, point out duplicated logic, or help extract messy code into cleaner abstractions.
- Ask the AI to explain the code it just generated. Follow up with questions about why it made specific design choices. The explanation isn’t the same as a human author walking you through their intent; it’s the AI interpreting its own output. But that perspective can still be valuable, like having a second reviewer describe what they see in the code.
- Try generating multiple solutions. Asking the AI to produce two or three alternatives forces it to vary its approach, which often reveals different assumptions or trade-offs.
- Use the AI as its own critic. After the AI generates code, ask it to review that code for problems or improvements. This can be effective because it forces the AI to approach the code as a new task; the context shift is more likely to surface edge cases or design issues the AI didn’t detect the first time.
- There’s also a strong signal in how hard it is to write good unit tests for AI-generated code. I can’t emphasize this enough: *If tests are hard for the AI to generate, that’s a signal to stop and think.*

### Reflective Questions for Teams

- *“What does the AI need to know to do this well?”* (Ask this before writing any prompt.) 
- *“What context or requirements might be missing here?”* (Helps catch gaps early.) 
- *“Do you need to pause here and do some research?”* (Promotes branching out beyond AI.) 
- *“How might you reframe this problem more clearly for the AI?”* (Encourages clarity in prompts.) 
- *“What assumptions are you making about this AI output?”* (Surfaces hidden design risks.) 
- *“If you’re getting frustrated, is that a signal to step back and rethink?”* (Normalizes stepping away.) 
- *“Would it help to switch from reading code to writing tests to check behavior?”* (Shifts the lens to validation.) 
- *“Do these unit tests reveal any design issues or hidden dependencies?”* (Connects testing with design insight.) 
- *“Have you tried starting a new chat session or using a different AI tool for this research?”* (Models flexibility with tools.)
