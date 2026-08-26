---
type: article
status: raw
quality: 
topics: [agent-harnesses, ai-engineering]
source: https://www.latent.space/p/attention-interface
created: 2026-08-26
published: 2026-08-22
author: Dan McAteer
flashcards: none
updated: 2026-08-27
---

# The Evolution of the Agent Harness

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!bUv7!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F758de9a0-631f-43a0-a331-fd871432a60b_1280x720.png" width="220" />
</div>

- **The model and the harness improving together** and then their curves of improvement crossing at the right moment. And that dynamic helps to explain what comes next: models keep absorbing the harness into their weights, engineers keep deleting what got absorbed, and **what remains is a harness for human attention rather than for the model.**
- The answer to **“What happened?”** isn’t solely in the model weights. It’s in the system that grew up around the weights. **The answer is in the agent harness.**
    - The agent harness is a way for the LLM to **break free from that confinement** and interact with real digital information space.

### What a Harness Actually Is

- **An agent harness is everything besides the model weights that makes the agent work.** The environment, tools, context and guardrails that surround the model.
    - **The harness is like giving the mind of the model a body.** With the harness, the model can perceive (context), act (tools), persist information (memory and compaction), and enforce its boundaries (permissions and guardrails).

![](https://substackcdn.com/image/fetch/$s_!x6zi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fef53f4f0-98b0-43d8-a601-9e1ac5db4380_2048x1752.png)

### Harness 1.0: The Past, “The Bolt-On Era”

- **ReAct, “The Harness on Paper”** (October 2022): [ReAct](https://arxiv.org/pdf/2210.03629) is a prompting technique to get models to reason through prompting.
    - It’s the agentic loop on paper, external to the model weights. It defines the idea of an “agent loop” where a model reasons -> acts -> observes -> repeats.
    - Again, **the ReAct loop exists only as a prompting method.** Prompting is the only reasoning method that exists at this time and no one calls it a “harness.”
    - Toolformer (Meta, Feb. 2023), that same winter, hints that tool use could be trained in rather than prompted. It’s a bit like Alan Turing’s idea of the computer before it was instantiated in a physical substrate. A powerful idea that is only later made manifest
- **AutoGPT/BabyAGI, “Premature Autonomy”** (Spring 2023): With AutoGPT/BabyAGI, the harness curve sprints ahead of the model capability curve.
    - Both hand the model full autonomy, asking the model to act as an “autonomous employee,” but the models at this point are still little more than brittle next-token predictors.
    - **A loop doesn’t add capability to a model.** A loop amplifies the capability a model has, and below some threshold the loop amplifies errors rather than reliability.
    - Consider the power of compounding in the negative: 95% reliability per-step over a 20-step task results in a ~36% average success rate.
    - The harness hands the model an assignment it has no realistic chance of completing
- **Cursor/Copilot, “Retreat to Human in the Loop”** (2023 - 2024): The first AI-powered IDEs recognize the failure-mode of giving the model too much autonomy.
    - They close the gap by pulling the harness curve down below the model curve. **Don’t give the model the loop directly; give the human the loop** and empower the human to orchestrate the loop while the model speeds the human up.
    - The first version of Devin tries to hand the autonomy back to the model. A [test from the team at Answer.AI](https://www.answer.ai/posts/2025-01-08-devin.html) shows that is still premature, with a ~15% success rate.
    - It’s evidence that the move from the IDEs to retreat from full autonomy is not cowardly, but the correct move.
    - However, while the prevailing tactic is to pull the harness down below the model, **models continue to improve**
- **Claude Code, “The Curves Cross”** (February 2025): The inversion at the end of 2024 sets up an opportunity that someone has to seize: if the model is now ahead of the harness, then a harness intentionally riding the brakes of the model is leaving capability on the table.
    - **Claude Code is the first coding agent built to seize that opportunity.** It abandons the IDE for the terminal, gives the model bash and file read/write access, and replaces the need for human approval on every change with **permission rules**.
    - The model is handed the loop again, and this time it understands the assignment.
    - **Boris Cherny and team build Claude Code with the next model’s capabilities in mind, not the current one.**
    - It is such a hit not because it’s the first product to give the model autonomy, but because it’s the first product to do so at the right ***time.*** That time is **the crossover point where the model has gotten reliable enough to succeed with autonomy**

### Harness 2.0: The Present, “The Co-Training Era”

- **Today the harness matters, and in a way we can measure.**
    - [Harness-Bench](https://arxiv.org/html/2605.27922v1) ran the same model over the same 106 tasks in different harnesses, and scores ranged from 52.4 to 76.2: a 23.8-point spread with zero change to the model.
    - **Half the agent is the harness.**

![](https://substackcdn.com/image/fetch/$s_!iOqa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F499ace76-7c55-4467-9a30-144978a3291a_1882x946.png)

- [OpenAI achieved a similar result](https://openai.com/index/how-two-settings-tripled-our-arc-agi-3-scores/) on ARC-AGI-3 with harness changes. Adding only retained reasoning and compaction, GPT-5.6 Sol’s ARC-AGI-3 score tripled from 13.3% to 38.3%.

![](https://substackcdn.com/image/fetch/$s_!_ASf!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F659c86e9-e2fb-40bb-94d0-cdf5509ceaad_2048x1469.png)

- What’s happening under the hood is that Reinforcement Learning (RL) has moved ***inside*** the harness
    - Then, as the models are trained in the environment of the harness, **they start to absorb the harness capabilities into the model weights**, learning how to auto-compact with knowledge of their own context window, for example.
    - **Once the models absorb the harness capabilities, the harness can shed the scaffold.** It’s production by reduction. Thariq Shihipar from Anthropic said that the team [recently deleted 80%](https://x.com/trq212/status/2080710971228918066?s=20) of Claude Code’s system prompt.
- This, then, is the loop of model / harness evolution: **train** -> **absorb** -> **shed** -> **repeat**. The model climbs to the next thing it can’t do yet.

### Harness 3.0: The Future, “The Attention Era”

- Keep deleting everything that the model can absorb.
    - Imagine what your agent looks like at the conclusion of that process. What are you left with in your hand when you’ve deleted everything?
- What do the model weights absorb next? Multi-agent orchestration, tool selection, memory...to name a few possibilities.
    - Researchers are building [self-improving harnesses](https://arxiv.org/html/2606.09498v1) that can themselves be trained in a similar way to models.
- What’s left at the end of this deletion and absorption process are **the human-centric agent capabilities**. Things like **permissions, identity, trust and legibility**
- The harness was born as the human interface to the model. We grew from chatbox to IDE to the terminal.
    - If the model absorbs the computer-facing capabilities, the next stage of evolution becomes one layer of abstraction up.
    - The harness becomes the model’s interface to our human attention.
- Tokens became abundant and reliable, yet **we remain bottlenecked on scarce human attention.**
