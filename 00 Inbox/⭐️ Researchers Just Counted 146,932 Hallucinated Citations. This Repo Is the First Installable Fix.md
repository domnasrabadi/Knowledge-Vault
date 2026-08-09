---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/AlphaSignalAI/article/2054617475484938719/?rw_tt_thread=True
created: 2026-08-09
published: 2026-05-13
author: AlphaSignal AI
flashcards: none
updated: 2026-08-09
---

# Researchers Just Counted 146,932 Hallucinated Citations. This Repo Is the First Installable Fix

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2014100845189529600/Ff1Xc28-.jpg" width="220" />
</div>

- Most academic AI workflows live as one-off prompts in private chats. The pipeline from literature search to draft to peer review to citation check to disclosure is rebuilt every time. Academic Research Skills packages that pipeline as four Claude Code skills with mandatory human checkpoints at every stage.
- The suite is four skills with declared data-access tiers, 25 registered modes, and a 10-stage orchestrated pipeline.

![](https://pbs.twimg.com/media/HIN0qgQWUAA3kmI.jpg)

- ***deep-research*** ships **13 agents and 7 modes**. It runs the upstream investigation: literature review, fact-check, systematic review, Socratic question framing. Data access level is raw. Modes include ***full***, ***quick***, ***socratic***, ***lit-review***, ***fact-check***, ***systematic-review***, and ***review***
- ***academic-paper*** ships **12 agents and 10 modes**. It handles drafting, revision, citation checks, format conversion, and the AI-disclosure statement. Data access is redacted. Modes include ***full***, ***plan***, ***outline-only***, ***revision***, ***revision-coach***, ***abstract-only***, ***lit-review***, ***format-convert***, ***citation-check***, and ***disclosure***
- ***academic-paper-reviewer*** ships **7 agents and 6 modes**. It runs multi-perspective peer review with an Editor-in-Chief, three dynamic reviewers, and a Devil's Advocate. Data access is ***verified_only***. The ***calibration*** mode measures the reviewer's own FNR/FPR against a user-supplied gold set.
- ***academic-pipeline*** ships **4 agents** and orchestrates everything above. It runs a 10-stage flow: research, write, Stage 2.5 integrity check, peer review, revision, re-review (max 2 loops), Stage 4.5 final integrity check, format conversion, final output, and process summary.
