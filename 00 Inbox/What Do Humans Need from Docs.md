---
type: article
status: inbox
quality: 
topics: []
source: https://www.dbreunig.com/2026/05/31/what-do-humans-need-from-docs.html
created: 2026-08-22
published: 2026-05-31
author: Drew Breunig
flashcards: none
updated: 2026-08-22
---

# What Do Humans Need From Docs?

<div align="center">
  <img src="https://www.dbreunig.com/img/textbooks.jpg" width="220" />
</div>


#### When an agent can explain anything, should we keep writing docs for humans?


#### Why do people write skills, but not docs?

- The agent does most of the work
- You can iterate as you use it
- A skill is immediately valuable
- A skill doesn’t have to be aggressively edited
- But on the whole, writing skills is much easier than writing documentation. And better yet: skills double as documentation.

#### Do we need docs that are just for humans?

- If skills are great docs, is there still a need to write docs specifically for *humans* to read? If so, *what is the job of human-centric docs*?
- After many conversations, I arrived at the following: 1. **Build mental models, not a reference.** Humans don’t require exhaustive documentation, they require *mental models*. Agents can find the details. 2. **Teach the art of the possible.** We need to arm them with an understanding of what a tool enables. Help them ask better questions and write better instructions. 3. **Explain the why.** Readers who understand a tool’s intent can reason beyond the obvious. 4. **Detail the design decisions.** What did the tool deliberately choose *not* to do or include? Great docs always shared this. It remains valuable. 5. **Don’t optimize for completeness.** This will be the hardest for most devs, who are excited to talk about the nuances. But only introduce what you need to build an effective mental model and trust the agent to facilitate the rest.
- The goal is to prepare your audience to prompt an agent effectively.
- `scaffold-docs` is opinionated about organization, and rigidly adheres to a three-tier structure: 1. **Getting Started:** a narrative tutorial covering a single representative use case 2. **Diving Deeper:** one file per topic, organized around intent and design decisions 3. **Reference:** per-module API spec, lookup-oriented
