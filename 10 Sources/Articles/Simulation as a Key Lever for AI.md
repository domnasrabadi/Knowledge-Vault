---
type: article
status: raw
quality: 
topics: [synthetic-data, llm-fundamentals, llm-judges, agent-evaluation]
source: https://www.latent.space/p/ainews-10-worse-100x-cheaper-10000x
created: 2026-08-26
published: 2026-08-22
author: swyx
flashcards: none
updated: 2026-08-27
---

# Simulation as a Key Lever for AI

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article2.74d541386bbf.png" width="220" />
</div>

## 10% worse, 100x cheaper, 10000x faster: Why Simulation is taking over

How LLMs take over — adoption eras at frontier labs, not invention dates. Transcribed from the figure above; **flip** marks the flip moment.

|  | **2022**<br>judge | **2023**<br>write · teach | **2024**<br>practice | **2025**<br>simulate | **2026**<br>experiment |
| --- | --- | --- | --- | --- | --- |
| Reward signal | **RLHF reward models**<br>InstructGPT · Constitutional AI<br>LLM-mediated · flip | RLAIF at scale<br>AI feedback replaces labelers<br>LLM-mediated | LLM-as-judge default<br>MT-Bench · AlpacaEval<br>LLM-mediated | Verifiable rewards<br>RLVR · process reward models<br>LLM-mediated | Synthesized verifiers<br>oracle / no-op / unsolved checks<br>LLM-mediated |
| Training data | Web scrape + filtering<br>C4 · The Pile · heuristics<br>human/real | **Textbook synthesis**<br>Phi: "textbooks are all you need"<br>LLM-mediated · flip | Rephrased web<br>WRAP · Nemotron pipelines<br>LLM-mediated | Reasoning traces<br>R1-style CoT corpora<br>LLM-mediated | Agent trajectories<br>rollout farms as data<br>LLM-mediated |
| Teacher | Human demonstrations<br>SFT on labeler writing<br>human/real | **Frontier distills student**<br>Alpaca · Vicuna · Orca<br>LLM-mediated · flip | On-policy distillation<br>GKD · logit matching<br>LLM-mediated | Open reasoning distills<br>R1 distill family<br>LLM-mediated | Teacher ensembles<br>routing + multi-teacher<br>LLM-mediated |
| Curriculum | Human-curated tasks<br>instruction datasets<br>human/real | Curated + templated<br>FLAN-era mixtures<br>human/real | **Self-generated tasks**<br>Self-Reward · SPIN · STaR<br>LLM-mediated · flip | Hard-task mining<br>difficulty targeting<br>LLM-mediated | Auto-curricula<br>envs propose next task<br>LLM-mediated |
| Human subject | Panels & surveys<br>focus groups · A/B tests<br>human/real | Generative agents demo<br>Smallville (research)<br>human/real | Digital twin research<br>1,000-people paper, 85%<br>human/real | **Synthetic panels ship**<br>Simile · SimGym<br>LLM-mediated · flip | Population sims<br>Fortune 100 · RCT post-training<br>LLM-mediated |
| Researcher | Manual experimentation<br>grad student descent<br>human/real | Autocomplete assist<br>Copilot era<br>human/real | Agentic coding<br>SWE-agents, human-directed<br>human/real | Discovery loops emerge<br>AlphaEvolve · AI Scientist<br>partial | **Autoresearch ratchet**<br>700 expts overnight, kept if better<br>partial · flip |
| Environment | Static benchmarks<br>MMLU · HumanEval<br>human/real | Human-built evals<br>held-out test sets<br>human/real | Hand-built RL gyms<br>code · math · games<br>human/real | Env economy forms<br>startups sell environments<br>partial | **Synthesized end-to-end**<br>z.ai: agents build envs + rewards<br>partial · flip |
| Physical world | Wet lab only<br>in vivo ground truth<br>human/real | Structure prediction<br>AlphaFold matures<br>human/real | Bio foundation models<br>ESM3 · cell atlases<br>human/real | Virtual cell models<br>Biohub · in silico 1000x cheaper<br>partial | Science as the frontier<br>Poolside pivot · Lila · Chai<br>partial |

- Every year since 2022, one more component of the pipeline that produces machine intelligence has flipped from human-made to model-made
    - each flip has a patient zero, a paper or product where the synthetic version first became load-bearing at a frontier lab, and from there on, the future is simply here but not yet productionized
- And if you squint, what we used to call “synthetic data” and “synthetic rubrics” and “AI researcher” and “end to end RL environments” is just **increasingly ambitious human simulation** - 10% worse, but 100x cheaper and 10,000x faster

- **Stage 1: The reward signal (2022)**
    - [InstructGPT](https://arxiv.org/abs/2203.02155) established the now-canonical trick: collect human preferences once, train a *reward model*, and let the policy optimize against the model rather than the humans
        - first thing to go synthetic was, counterintuitively, the judge
    - [Constitutional AI](https://arxiv.org/abs/2212.08073) pushed further and had the AI critique itself against a set of principles (RLAIF)
    - By the time [LLM-as-judge](https://arxiv.org/abs/2306.05685) became the default eval methodology (MT-Bench, AlpacaEval), the entire approval apparatus — reward, critique, evaluation — ran on models judging models
- **Stage 2: The training data (2023)**
    - Microsoft’s Phi series made the argument in its title: [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644). A small model trained on LLM-synthesized, textbook-quality data punched far above its parameter count
    - [Nemotron-4 340B](https://arxiv.org/abs/2406.11704) shipped with a permissively licensed synthetic data generation pipeline as a headline feature, and by 2025 reasoning-trace corpora (chains of thought generated by strong reasoners) had become a standard pretraining and mid-training ingredient
    - The corpus, the thing that was supposed to be the irreducibly human input, was now substantially model-written
- **Stage 3: The teacher (2023)**
    - Weeks after ChatGPT’s API opened, Stanford’s [Alpaca](https://crfm.stanford.edu/2023/03/13/alpaca.html) demonstrated that a $600 fine-tune on GPT-generated instructions could clone much of a frontier model’s behavior.
        - [Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/) did it with shared conversations; [Orca](https://arxiv.org/abs/2306.02707) did it with rich teacher explanations rather than bare answers
    - [DeepSeek-R1](https://arxiv.org/abs/2501.12948) shipped a family of distilled models alongside the flagship, making “the teacher is a model” the default assumption for every small model release since.
- **Stage 4: The curriculum (2024)**
    - Stages 1–3 made the inputs synthetic; stage 4 is where the loop starts closing on itself, because the model begins deciding *what to learn next*
        - The pieces existed early — [Self-Instruct](https://arxiv.org/abs/2212.10560) (models writing their own instruction sets) and [STaR](https://arxiv.org/abs/2203.14465) (models bootstrapping their own reasoning traces) are both 2022
        - the flip came when Meta’s [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020) and [SPIN](https://arxiv.org/abs/2401.01335) showed a model could generate its own tasks, judge its own outputs, and improve past the ceiling of its human preference data
    - Curriculum design — historically the most artisanal part of ML, the taste-driven choice of what to train on next — became something models do to themselves
- **Stage 5: The researcher (2026)**
    - The assistance era (Copilot, then SWE-agents) kept a human choosing the experiments. The discovery era did not.
        - DeepMind’s [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) evolved genuinely new algorithms in 2025, and Sakana’s [AI Scientist](https://arxiv.org/abs/2408.06292) (now in [Nature](https://www.nature.com/articles/s41586-026-10265-5)!) sketched the full paper-writing pipeline
    - big moment was Karpathy’s [autoresearch](https://github.com/karpathy/autoresearch) in March 2026: a deliberately minimal ratchet loop where a coding agent modifies a real LLM training setup, runs a five-minute experiment, keeps the change only if validation loss improves, and repeats overnight
- **Stage 6: The environment (2026)**
    - RL’s scaling bottleneck moved from the model to the environment: you need thousands of executable, verifiable, professionally realistic task worlds, and humans can’t hand-build them fast enough
        - Research agents mine real work patterns and convert them into long-horizon environments with hidden state, a judge agent attempts each task to confirm it’s solvable, and verifiers are synthesized *without* seeing the reference solution, then stress-tested with oracle, no-op, and unsolved-state checks until their binary reward is reliable enough to train on directly
    - As the [GLM-5.3 release](https://z.ai/blog/glm-5.3) puts it, **the entire environment, judging, and verification stack is synthetic all the way down**
- **Stage 7: The human subject (2025)**
    - If models can be the judge, teacher, and environment, the remaining human role in the loop is *subject* — the source of preferences, behavior, and demand
        - **The big hurdle** to overcome: frontier models are trained toward being agent models, which makes them *bad* simulations of real people — so Simile post-trains on interviews, transaction data, and registered RCTs from the [Open Science Framework](https://osf.io/) specifically to recover human bias, inconsistency, and causal texture, and reports early scaling laws for simulation quality
        - Tencent’s [billion-persona](https://arxiv.org/abs/2406.20094) approach at the crude end of the spectrum, the focus group, the user study, and the A/B test panel are becoming inference workloads.
- **Stage 8: The physical world (2026, in progress)**
    - the world’s problems split into *intelligence-bound* ones (solvable by scaling cognition, soon commoditized by open weights) and *experiment-bound* ones, where “no amount of intelligence substitutes for real-world experimental feedback — 100,000 brilliant minds won’t cure cancer without a wet lab.”
