---
type: article
status: inbox
quality: 1
topics: []
source: https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills
created: 2026-08-09
published: 2026-06-03
author: Claude
flashcards: none
updated: 2026-08-09
---

# Lessons from building Claude Code: How we use skills

<div align="center">
  <img src="https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a2058f7af91f02cff0a6187_og-lessons-from-building-claude-code.jpg" width="220" />
</div>

- Skills have become one of the most used extension points in Claude Code. They’re flexible, easy to make, and easy to distribute.

### What are skills?

- Skills are folders of instructions, scripts, and resources that agents can discover and use to do things more accurately and efficiently.

### Types of skills

- skills that explain how to correctly use a library, CLI, or SDKs
- kills that describe how to test or verify that your code is working
- Verification skills have had the most measurable impact on Claude’s output quality internally. It can be worth having an engineer spend a week just making your verification skills excellent.

#### 6. Code quality and review

- `adversarial-review` — spawns a fresh-eyes subagent to critique, implements fixes, iterates until findings degrade to nitpicks
- **7. CI/CD and deployment** These are skills that help you fetch, push, and deploy code inside of your codebase. These skills may reference other skills to collect data. Examples include:
    - `babysit-pr` — monitors a PR → retries flaky CI → resolves merge conflicts → enables auto-merge
    - `deploy-<service>` — build → smoke test → gradual traffic rollout with error-rate comparison → auto-rollback on regression
    - `cherry-pick-prod` — isolated worktree → cherry-pick → conflict resolution → PR with template
- **8. Runbooks** These are skills that take a symptom (such as a Slack thread, alert, or error signature), walk through a multi-tool investigation, and produce a structured report.

### Tips for making skills

- If you’re publishing a skill that is primarily about knowledge, focus on information that pushes Claude out of its normal way of thinking.

#### Build a gotchas section

- The highest-signal content in any skill is the Gotchas section. These sections should be built up from common failure points that Claude runs into when using your skill. Ideally, you will update your skill over time to capture these gotchas.

#### Use the file system and progressive disclosure

- Like we said earlier, a skill is a folder, not just a markdown file. You should think of the entire file system as a form of context engineering and progressive disclosure. Tell Claude what files are in your skill, and it will read them at appropriate times.
- The simplest form of progressive disclosure is to point to other markdown files for Claude to use. For example, you may split detailed function signatures and usage examples into `references/api.md`.
- Another example: if your end output is a markdown file, you might include a template file for it in `assets/` to copy and use.

#### Avoid railroading Claude

- Claude will generally try to stick to your instructions, and because skills are so reusable you’ll want to be careful of being too specific in your instructions. Give Claude the information it needs, but give it the flexibility to adapt to the situation.

#### Think through the setup


![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a1f3a763cec27e2f02643a8_d5e89124.png)

- Some skills may need to be set up with context from the user.
- A good pattern to do this is to store this setup information in a config.json file in the skill directory like the above example. If the config is not set up, the agent can then ask the user for information.
- If you want the agent to present structured, multiple choice questions you can instruct Claude to use the AskUserQuestion tool.

#### Write descriptions for the model, not for humans

- When Claude Code starts a session, it builds a listing of every available skill with its description. This listing is what Claude scans to decide "is there a skill for this request?" Which means the description field is not a summary, it's a description of when to trigger this skill.

#### Help Claude remember

- Some skills can include a form of memory by storing data within them.
- For example, a `standup-post` skill might keep a standups.log with every post it's written, which means the next time you run it, Claude reads its own history and can tell what's changed since yesterday.

#### Store scripts and generate code

- Giving Claude scripts and libraries lets Claude spend its turns on composition, deciding what to do next rather than reconstructing boilerplate.

#### Use on-demand hooks

- Skills can include hooks that are only activated when the skill is called, and that only last for the duration of the session. Use this for more opinionated hooks that you don’t want to run all the time, but are extremely useful sometimes.

### Distributing skills

- two ways you might want to share skills with others:
- • check your skills into your repo (under `./.claude/skills`) • make a **plugin** and have a Claude Code Plugin marketplace where users can upload and install plugins
- As you scale, an internal plugin marketplace allows you to distribute skills and let your team decide which ones to install, as well as include a setup flow.

### Managing a skills marketplace

- At Anthropic, we don't have a centralized team that decides; instead we try to find the most useful skills organically. If someone has a skill that they want people to try out, they can upload it to a sandbox folder in GitHub and point people to it in Slack or other forums. Once a skill has gotten traction (which is up to the skill owner to decide), they can put in a PR to move it into the marketplace.

### Composing skills

- You may want to have skills that depend on each other. For example, you may have a file upload skill that uploads a file, and a CSV generation skill that makes a CSV and uploads it. This sort of dependency management is not natively built into marketplaces or skills yet, but you can just reference other skills by name, and the model will invoke them if they are installed.
