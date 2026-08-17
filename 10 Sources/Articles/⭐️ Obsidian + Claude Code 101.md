---
type: article
status: raw
quality: 1
topics: [knowledge-management, ai-tooling, agent-harnesses]
source: https://x.com/arscontexta/status/2013045749580259680/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-01-19
author: Heinrich
flashcards: none
updated: 2026-08-17
---

# obsidian + claude code 101

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2012958446891536384/neq1Tu46.jpg" width="220" />
</div>

- the markdown files know everything ive discovered, nicely structured and with automatic situational context injection for in-context learning
- i use a vault index that helps the agent decide what notes to pull in, same pattern as how claude code decides which skills to load
- i realized: knowledge bases and codebases have a lot in common theyre both folders of text files with relationships between them, they both have conventions and patterns, and they both benefit from agents that can navigate and operate them
- files connect using [[wiki links]] which build a network of ideas

### how to write good notes

- how you write those links matters
- dont write "this relates to quality, see: quality-note". write "because [[quality is the hard part]] we need to focus on curation" the link becomes part of your thought, and the agent can follow your reasoning by following the links
- also write notes that stand alone and are composable
- each one is complete on its own, but they connect to build bigger structures when your notes work this way, the network itself becomes valuable
- a work vault might emphasize:
    - capture first, structure later
    - project folders with meetings and outputs
    - client context for ai consumption
- a research vault might emphasize:
    - source tracking and citations
    - literature notes
    - claim verification
- a creative vault might emphasize:
    - idea capture and incubation
    - draft progression
    - reference organization
- these are the rules that work for my thinking vault. other vault types might need different ones:
    1. can this note be linked from elsewhere and still make sense? if linking to it forces you to explain three other things first, split it up. thats composability
    2. i stopped naming notes like topics and started naming them like claims. instead of "thoughts on ai slop" you write "quality is the hard part". when you link to it, the title becomes part of your sentence naturally (this also forces claude to think differently when building sentences, which i believe is beneficial because it requires understanding)
    3. insight that individual notes matter less than their relationships. a note with many incoming links is more valuable than an isolated note because every link creates a new reading path. the network is the knowledge

### how to start

- create a folder with subfolders that match your purpose. think about what you actually need to organize
- write a claude md that explains your system. start simple and evolve it as you learn what works
- let claude operate. capture something and ask claude to find connections. let it navigate and discover relationships and suggest where things belong
- ALWAYS review what it produces and edit for quality
