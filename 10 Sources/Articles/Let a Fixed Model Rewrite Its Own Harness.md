---
type: article
status: raw
quality:
topics: [ai-agents, agent-evaluation, error-analysis, agent-harnesses]
source: https://x.com/AlphaSignalAI/article/2067347896497000515/?rw_tt_thread=True
created: 2026-08-09
published: 2026-06-17
author: AlphaSignal AI
flashcards: none
updated: 2026-08-17
---

# Let a Fixed Model Rewrite Its Own Harness

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2014100845189529600/Ff1Xc28-.jpg" width="220" />
</div>

- The paper is from **Shanghai Artificial Intelligence Laboratory** and titled "**Self-Harness: Harnesses That Improve Themselves**." It went up on arXiv on June 8, 2026
- A harness is the system layer between a model and its environment. Different models have different habits, so a harness tuned for one can underperform on another, and today that tuning is manual work.
- Start with the harness. It is everything wrapped around the model: the system prompt, the tools, the runtime rules, the checks that decide pass or fail, and the recovery steps for when something breaks.
- The loop runs in three stages:
    1. **Weakness Mining** — The fixed model runs the task set under the current harness, and every run is logged as a trace with a pass or fail verdict. Failed runs get clustered by a verifier-grounded signature: what the verifier rejected, how the agent's behavior caused it, and the reusable mechanism behind it. Two timeouts only group together if the behavior underneath them matches.
    2. **Harness Proposal** — The same model, now in a proposer role, gets a bounded brief: the editable parts of the harness, the failure patterns, the behaviors worth keeping, and a record of past edits. From that it writes several distinct candidate edits at once, each tied to one failure mechanism and one surface. Every edit has to stay minimal and leave the rest of the control flow alone.
    3. **Proposal Validation** — Each candidate is tested on a held-in split and a held-out split. The held-in split is what the proposer saw. The held-out split is the regression gate it never saw.

### The same harness breaks differently for every model

- This is the part that makes the loop more than a prompt tweak. All three models started from the same minimal harness, and each one broke in its own way.
- **MiniMax M2.5** kept edits for:
    - creating required outputs early
    - handling malformed tool content
    - cutting off stalled tool-use loops
- **Qwen3.5-35B-A3B** kept edits for:
    - prechecking dependencies
    - not retrying failed commands blindly
    - breaking exploration loops
    - recovering artifacts after a tool error
- **GLM-5** kept edits for persisting environment changes across shell commands and pushing the agent from exploring into building and testing.

### Three ways to improve a harness

- Self-improving agents have a long line behind them:
    1. **Reflexion** replays verbal feedback into the next attempt.
    2. **Agentic context engineering** evolves the context across calls.
    3. **STOP** recursively rewrites code-generation programs.

### How to apply it to your agent harness

- You do not need the paper's setup to use the idea. Run the same loop by hand over your own agent logs:
    1. Log every run as a trace with a pass or fail result from a real verifier, not a guess.
    2. Split your tasks into a held-in set you study and a held-out set you never look at while editing.
    3. Cluster failures by cause, not symptom: what the verifier rejected, and the agent behavior behind it.
    4. Propose one minimal harness edit per recurring cause, and touch only the surface that cause needs.
    5. Promote the edit only if one split improves and neither gets worse. Otherwise log it and move on.

### Harness rules that survived the gate

- Every rule below is an edit Self-Harness proposed from a real failure, then kept only because it held on both held-in and held-out tasks. They read as plain harness guidance you can lift into your own system prompt or runtime policy.
    - Create the required output artifact early, before deep exploration.
    - Precheck dependencies before running the thing that needs them.
    - Do not retry a failed command unchanged. Change the strategy first.
    - Break the loop after repeated unproductive actions.
    - Persist environment changes across shell commands.
    - Verify the required artifact exists before finishing.

### AlphaSignal Take

- The headline is that an agent edits its own harness. The part worth copying is the rule that decides what stays.
- **The gate is the real contribution.**
    - "No harness edit ships unless a held-out set holds or improves" is good practice whether the editor is a model, an optimizer, or you.
    - Self-Harness wires it into the loop.
