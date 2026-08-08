---
type: article
status: inbox
quality: 3
topics: []
source: https://eugeneyan.com/writing/working-with-ai/
created: 2026-08-08
published: 2026-05-03
author: Eugene Yan
flashcards: none
updated: 2026-08-08
---

# How to Work and Compound with AI

<div align="center">
  <img src="https://eugeneyan.com/assets/og_image/default.jpg" width="220" />
</div>

- Every finished artifact—code, docs, analysis, decisions—becomes context for the next session.
- I believe the underlying principles apply broadly: provide good context, encode your taste as config, make verification easy, delegate bigger tasks, and close the loop.

### Context as infrastructure

- **Help models nagivate your context.** For example, all my code lives in `~/src` and all my knowledge work lives in `~/vault` (organized into `projects/`, `notes/`, `kb/` and so on). When our work is organized, it makes it easier for the model to retrieve context using `grep` or `glob`. And by having a clean directory tree, it’s more straightforward to navigate the directory
- Connect models to your organization’s context.
- I also maintain a `INDEX.md` per project. It’s an annotated index of the relevant docs and channels, and each entry includes the URL, owner, and a brief paragraph explaining what’s inside and when to read it. The annotation helps a lot.
- **Onboard each new session like a new hire.** With each new session, the model starts with a blank slate. Thus, it helps to treat the per-project `CLAUDE.md` like the onboarding doc we’d hand to a new teammate on day one.
- **Build your memory layer.** By default, models don’t remember what happened in the last session, so anything worth persisting should be written to disk. I split my memory layer into two buckets. `~/vault` holds facts such as project state, artifacts, and domain knowledge; `~/.claude` (along with its `CLAUDE.md`, `skills/`, `guides/`) contains my preferences, workflows, and personal taste. The former provides context while the latter provides configuration.

### Taste as configuration

- **When CLAUDE.md gets too long, split it out.** A long `CLAUDE.md` can become a context tax. It loads everything every session even if the session doesn’t need it. To fix this, refactor chunks into guides that load lazily
- Instead, tell your `CLAUDE.md` to read them when relevant
- I tend to keep `SKILL.md` small and focused on the workflow and routing. The knowledge, like templates and scripts, are separate files that the model reads and runs only when needed, just like lazy-loaded guides.
- **Bootstrap skills by doing the task once and then asking the model to make it a skill.** This is how I build most skills. First, I do the task once, interactively, in a normal session. Then, I ask the model to turn what we just did into a skill. Next, I run the skill on the same or similar task. Inevitably, I’ll need to correct the output, which I do in the same session so feedback is logged in the session transcript. Finally, I ask the model to update the skill based on the corrections and feedback.
- **Refine skills via the transcript, not the file directly.** The first version of the skill rarely works perfect because it overfits the original session. This is normal. When you run it and need to update the output, correct it within the session. Try not to open and edit `SKILL.md` directly. Providing feedback in the session gives the model before-and-after pairs which accumulate in the transcript—here’s what we did, here’s what I wanted, and why

### Verification for autonomy

- **Shift verification left; catch errors at write time.** I think of verification as a ladder. The bottom is cheap and deterministic; the top is expensive and requires judgement. We want to address issues at the lowest possible rung
- **Make it easy for the model to verify the work.** Give the model feedback loops to improve its output. If the system produces a metric, let the model run the eval and optimize it
- **For long-running tasks, have models watch models.** Long sessions can drift as errors build up. One fix is to run a secondary session with fresh context to read the original spec and the recent turns of the primary session

### Scaling via delegation

- with increasingly stronger models, we should aim to delegate bigger tasks. Explain your intent, constraints, and success criteria upfront, then let the model work. You can’t delegate what you can’t verify, so this requires first defining success criteria and metric
- The bottleneck has shifted from doing the work to writing clear specs and reviewing outputs fast enough to keep the pipeline moving—the middle is hollowing out.
- When running multiple sessions, I need to know their state and which one needs attention. On my mac, a stop hook plays a sound when a session finishes (example below). My tmux window titles use a status emoji (⏳ working; 🟢 complete) and a short Haiku-generated label so I know what each pane is doing

### Closing the loop

- **Keep the context rich by working in the open.** When we do our work in shared docs, repos, and channels, it makes it easier for everyone—including models—to retrieve and benefit from the context
- **Mine your transcripts for config updates.** Have the model read past session transcripts to find gaps. When I scanned ~2,500 of my past user turns, a sizable percentage contained phrases like *“can you also…“*, *“did you check…“*, *“still wrong”*, etc. These suggest that the model should have done something unprompted, and I should update the `CLAUDE.md` or skill, or that a verification step is missing or broken
- **Refactor and prune periodically.** As configs grow, they can overlap or conflict with each other. As a result, if the model ignores a rule, it can be because another rule contradicts it. Fix this by refactoring periodically.
