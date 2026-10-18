---
type: article
status: inbox
quality: 
topics: []
source: https://x.com/josharosen/status/2101645894818857272/?s=12&rw_tt_thread=True
created: 2026-10-18
published: 2026-09-20
author: Josh Rosen
flashcards: none
updated: 2026-10-18
---

# Jev in the Wild: Early Architecture Patterns for System One Models

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1418279052805353474/zn_g71-U.jpg" width="220" />
</div>

- Jev has been out for less than a week, but we’re already starting to see patterns in how people are building with it.
- Here are some of the early architecture patterns showing up across Jev projects.
- Model routing was one of the most obvious Jev use cases from the start. If you give Jev the request and a set of models, it can decide which model should handle the work.
- Another group of projects uses Jev to decide what information should make it through to the next stage.
- [Winnow](https://github.com/nicobailon/winnow) judges tool results before they enter a coding agent’s context. [jev-sift](https://github.com/jkudish/jev-sift) scores files, URLs, and snippets so an agent only opens the ones that matter. [fast-jev-compaction](https://github.com/tamaratran/fast-jev-compaction) uses Jev to decide what survives Claude Code context compaction while keeping the selected content verbatim. There are similar experiments around search and RAG. [reranker](https://github.com/joelhooks/jev-reranker) gives each candidate document a relevance probability
- [jev-guard](https://github.com/andrewgcodes/jev-guard) evaluates tool calls from coding agents and turns the result into allow, ask, or deny decisions. It can also inspect tool results for prompt injection before they return to the agent. [pi-warden](https://github.com/badlogic/pi-warden) puts a similar decision layer directly into the Pi coding agent, checking actions against project rules and feeding the resulting guidance back into the worker.
- I built [Foreman](https://github.com/thruwire/foreman) around this pattern. A Codex worker does the software engineering while Foreman independently watches the work. Jev continuously assesses the evidence coming off the factory floor, including worker output, Git changes, tests, previous assessments, and the original job.
- [Browser Use’s Jev Ultrafast](https://github.com/browser-use/jev-ultrafast) constructs a set of possible browser operations and DOM targets, then has Jev pick one. A small language model is only needed when the browser actually has to generate text. [jev-browser](https://github.com/jkudish/jev-browser) uses a similar architecture and uses Jev to choose an action on each step.
- same architecture is showing up in computer use. [typesafe-computer-use](https://github.com/TypeSafeAI/typesafe-computer-use) reads the screen, constructs possible actions, and uses Jev to decide what to do, such as where to move the mouse or what to click on.
- [pg-jev](https://github.com/realZachi/pg-jev) puts Jev directly inside Postgres. A SQL query can filter rows based on whether a customer sounds angry, rank products by how luxurious they seem, or classify a ticket by which team should handle it.
- There’s an [ad blocker](https://github.com/realZachi/typesafe-adblock) that asks Jev whether something actually looks like an ad, [Unclutter](https://github.com/kitze/unclutter) deciding what parts of a webpage are unnecessary, and [Every](https://github.com/AnotiaWang/awesome-jev) asking a semantic question against every function in a codebase.
