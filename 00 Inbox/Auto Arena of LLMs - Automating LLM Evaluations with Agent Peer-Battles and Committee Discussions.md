---
type: paper
status: inbox
quality: 
topics: []
source: https://arxiv.org/pdf/2405.20267
created: 2026-08-08
published: 2024-05-30
author: Ruochen Zhao, Wenxuan Zhang, Yew Ken Chia, Deli Zhao, Lidong Bing
flashcards: none
updated: 2026-08-08
---

# Auto Arena of LLMs: Automating LLM Evaluations with Agent Peer-battles
  and Committee Discussions

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/398437540/Nr3gnYtA4L85eneG8bnwRAxJ1zExtZUSvx-yKXJ968A-cove_j8umQ6o.png" width="220" />
</div>

- To address this, we propose the Auto-Arena, an innovative framework that automates the entire evaluation process using LLM-powered agents. Firstly, an LLM examiner generates questions. Then, two LLM candidates engage in a multi-round peer battle based on individual questions, aiming at revealing their true performance differences. Finally, a committee of LLM judges collaboratively discusses and decides the winner, reducing bias and enhancing fairness.
- The framework consists of three stages
- Firstly, an LLM examiner agent is tasked with generating questions, mimicking real-life users posting queries.
- Secondly, two LLM candidates interact with each other and engage in a multi-round peer battle by answering the seed question individually, criticizing the opponent's weaknesses, and raising targeted follow-up queries to challenge the opponent further. During the multi-round battle process, the LLM's true capabilities are drawn out and performance gaps become more visible.
- Lastly, a committee of LLM judges collectively discusses and evaluates the ability of the two candidates, mimicking the human voting process.
