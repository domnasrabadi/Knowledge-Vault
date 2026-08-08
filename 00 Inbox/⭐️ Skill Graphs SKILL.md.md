---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/arscontexta/status/2023957499183829467/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-02-18
author: Heinrich
flashcards: none
updated: 2026-08-08
---

# Skill Graphs > SKILL.md

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2012958446891536384/neq1Tu46.jpg" width="220" />
</div>

- a skill graph is a network of skill files connected with wikilinks
- instead of one big file you have many small composable pieces that reference each other. each file is one complete thought, technique or skill and **[[wikilinks between them create a traversable graph]]**
- a skill graph applies the same skill discovery pattern recursively inside the graph itself every node has a yaml description the agent can scan without reading the whole file every wiki link carries meaning because its woven into prose so the agent follows relevant paths and skips what doesnt matter progressive disclosure: index → descriptions → links → sections → full content

### the primitives

- • **wikilinks** that read as prose in sentences, so they carry meaning not just references • **yaml frontmatter** with descriptions so the agent can scan without reading full files • **MOCs (maps of content)** that organize clusters of related skills into navigable sub-topics

### how to build one

- the easy way: install the arscontexta claude code plugin, pick the research preset and point it at any topic it sets up the markdown folder structure for you and then you fill it with /learn and /reduce
- skills are context engineering, basically curated knowledge injected where it matters
