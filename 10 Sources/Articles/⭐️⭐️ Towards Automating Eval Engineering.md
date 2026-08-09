---
type: article
status: raw
quality: 2
topics: [agent-evaluation, error-analysis, ai-agents]
source: https://x.com/vtrivedy10/status/2079976006644072796/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-07-22
author: Viv
flashcards: none
updated: 2026-08-09
---

# Towards Automating Eval Engineering

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1805079750873923584/7sTh63Eo.jpg" width="220" />
</div>

- Today we’re releasing our **Eval Engineering Skill**, a skill that helps coding agents build evals using context from a repository and agent traces
- **The skill is designed to interview the user** who can give feedback on proposals and iteratively approve each eval
- The skill first reads the repository and maps the agent surface including prompts, models, tools, skills, hooks, etc
- Traces show how tools behave in practice such as their arguments, results, and errors. These observed contracts help the skill reproduce relevant production behavior in a controlled environment.
- Crawling the repo and traces gives the agent knowledge of a which abilities are important for the agent as it proposes eval tasks. We found that **interviewing the user,** leads to much better eval acceptance than one-shot generation. The user chooses from the proposed eval directions, and gives guidance on questions such as which tools & dependencies should run live or need to be simulated. For example, tool calls that incur costs or require writes to production can be simulated instead of being run on every eval invocation.

![](https://pbs.twimg.com/media/HNztw2oWUAAsqbP.png)

## Eval Design Is Iterative

- We found that while agents are sometimes able to one-shot evals, the best evals came from users providing feedback and specifying which capabilities were worth measuring in agents
- A useful way to improve it was to run the eval and inspect both sides of the result:
    - the agent trajectory, including its messages, tool calls, and actions.
    - the verifier trajectory, evidence, reasoning, and final score.

## Why This Matters

- [Continual learning can be thought of as a continuous data mining problem](https://www.langchain.com/blog/improving-agents-is-a-data-mining-problem) where production data is used to build evals that improve agents over time. Teams mine traces to find recurring user requests, errors, failed tool calls, and incorrect state changes. which become evals so the same behavior can be measured and prevented in the future.
- Evals are training data for agents. Teams can fit agent behavior to them through harness engineering such as changing prompts & tools or fine-tuning. The eval provides a fixed target for deciding whether those changes improved the intended capability.
- The resulting loop is: mine traces -> identify a failure -> build an eval -> improve the agent -> rerun
