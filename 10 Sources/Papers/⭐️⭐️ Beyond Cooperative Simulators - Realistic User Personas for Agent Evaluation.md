---
type: paper
status: raw
quality: 2
topics: [agent-evaluation, synthetic-data, adversarial-testing]
source: https://arxiv.org/abs/2605.12894v1
created: 2026-08-26
published: 2026-05-13
author: Harshita Chopra, Kshitish Ghate, Aylin Caliskan, Tadayoshi Kohno, Chirag Shah, Natasha Jaques
flashcards: none
updated: 2026-08-27
---

# Beyond Cooperative Simulators - Realistic User Personas for Agent Evaluation

### Abstract

- Large Language Model (LLM) agents are increasingly deployed in settings where they interact with a wide variety of people, including users who are unclear, impatient, or reluctant to share information. However, collecting real interaction data at scale remains expensive
- The field has turned to LLM-based user simulators as stand-ins, but these simulators inherit the behavior of their underlying models: cooperative and homogeneous
    - As a result, agents that appear strong in simulation often fail under the unseen, diverse communication patterns of real users
- we cast persona generation as an LLM-driven evolutionary program search that optimizes a Python generator to discover behaviors and translate them into task-preserving roleplay policies
    - Across tau^2-bench retail and airline domains, evolved PPol programs yield 33-62% absolute gains in fitness score over the baseline simulator
    - Agents trained with PPol are more robust to challenging, out-of-distribution behaviors, improving task success by +17% relative to training only on existing simulated interactions

### Introduction

- However, to be truly useful, an agent must do more than navigate a software interface; it must navigate the unpredictable nature of human communication. Real users rarely provide information perfectly. They have distinct preferences, varying patience, and often express their needs through ambiguous, fragmented, or sometimes adversarial language
- recent studies show that these default user simulators are overly cooperative, perfectly consistent, and highly forthcoming with information
    - Real users often withhold details until prompted, push back on incorrect assumptions, use ambiguous language, and vary in patience and cooperativeness
    - This creates a *behavioral gap*: agents can appear strong against cooperative simulators but fail when confronted with the frustration, skepticism, or brevity of an actual human user
- we introduce **Persona Policies** (PPol), a plug-and-play control layer that diversifies user simulation by generating multiple human-like personas while keeping benchmark tasks fixed. Each ‘*policy*’ is a short set of *additional* instructions added to the simulator prompt that controls *how* the user communicates, for example, by varying tone, pacing, selective disclosure, etc
    - We evaluate candidate generators through actual agent–user rollouts, scoring the personas on two objectives: **human-likeness**, measured as the probability of being classified as human by a trained discriminator, and **behavioral coverage**, which measures how well the $N$ personas span the human distribution
        - Both metrics are computed using *behavioral fingerprints*, 19 lexical and interaction-level features organized across communication style, information disclosure, clarification behavior, and error reaction

### Related Work

- **User simulation for interactive agents**
    - Similarly, a recent study shows that even strong models become substantially less reliable when information is revealed incrementally across turns, highlighting the challenge inherent in this type of multi-turn assistance task
- **Personas and behavioral control**
    - Prior work on user simulation has focused on making simulated interactions more coherent, natural, or goal-consistent. LLM-based simulators improve task-oriented dialogue by fine-tuning on real conversations, adding verifier models, or learning more human-like questioning patterns
        - A parallel line of persona-based work uses profiles to diversify generated users and responses, from profile-grounded dialogue to implicit user profiles inferred from human–machine conversations
        - These approaches make simulated users less generic, but they usually treat personas as fixed descriptions, sampled profiles, or training data artifacts
    - We extend this concept of scalable persona generation toward multi-turn agent evaluation: given a fixed task, PPol generates a population of users who all pursue the same goal but communicate in different ways
        - The generator is optimized from agent–user rollouts for two properties: whether the resulting conversations resemble real human interactions, and whether the generated population covers diverse regions of the human behavior distribution.
- **Robustness under diverse users**
    - Evaluation scores on interactive benchmarks reflect *both* the agent and the simulated user who conversed
        - Separately, stress-test studies show that small, controlled changes to user behavior, such as prompting more impatient or less cooperative play, can move headline success rates by large margins
    - Together, these findings argue for making the simulated user an explicit, tunable part of the benchmark, rather than a hidden default baked into the evaluation

### Method

#### Problem Setting

- We consider multi-turn, goal-directed dialogue benchmarks. Each task $t$ specifies a scenario and the user’s objectives. Let $c_t$ be the benchmark-provided user context passed to the existing user simulator: base persona, task instructions, and any facts available to the user
- An LLM *user simulator* is prompted with the task and converses with an *agent*. All task-level quantities are held fixed: goals, private facts, environment state, and the success determined by task-completion rules
    - The sole controllable input is natural-language text appended to the user simulator’s *system* prompt.
- **Persona policy** $P_\pi$ refers to appended natural-language text. It controls the simulated user’s communicative style, including tone, pacing, and disclosure
- Behavioral variation is represented by a list $D$ of **behavioral axes**. Each entry names an axis, gives a short definition, and provides paired on/off *playbooks* for how the behavior appears when active or inactive
    - We seed D with four behaviors: terseness, skepticism, frustration, and ambiguity. The list $D$ is maintained in the evolvable generator source file, so mutation may add, remove, or refine axes in addition to the instructions.
- At a high level, the procedure has four steps: generate a set of persona policies for each benchmark task, run agent-user interaction rollouts, score the resulting trajectories against human reference behavior, and use an evolutionary coding agent to mutate the generator source.

#### Persona generation

- The evolvable artifact is a Python program that implements the persona generator function $G$ and holds the current axis list $D$
- For task $t$, the generated persona-policy set is $$\begin{equation} \label{eq:generator_output} \Pi_t = \left\{ P_{\pi,t}^{(i)} \right\}_{i=1}^{N}, \qquad \Pi_t = G(c_t,D,N). \end{equation}$$
    - Each persona policy $P_{\pi,t}^{(i)}$ has a **persona record** $r_t^{(i)}=\left(\mathbf{a}_t^{(i)},P_{\pi,t}^{(i)}\right), \mathbf{a}_t^{(i)} \in \{0,1\}^{|D|}.$
        - Here $\mathbf{a}_t^{(i)} : D \to \{0,1\}$ is the binary mapping that determines which behavioral axes (e.g., *distracted*) are active (true) for persona $i$ on task $t$.
- **Population generation**
    - **first phase** is *population generation*: a frontier language model
        - jointly proposes $N$ *population members*
        - structured response lists exactly $N$ members, each with a short natural-language summary, brief rationale, and axis assignment in $\{0,1\}^{|D|}$
- **Persona expansion**
    - The **second phase** *expands* each population member, independently and in parallel, into one long natural-language persona policy $P_{\pi,t}^{(i)}$, the string appended to $s_{\mathrm{base}}(t)$ for that rollout

#### Optimization Metrics

- We score a candidate generator $G$ by running it and evaluating the resulting dialogue trajectories
    - gives one completed trajectory per $(t,i)$ pair.
    - convert each trajectory into a behavioral fingerprint, explained below, and score the minibatch along two axes
        - First, **human-likeness** is the average probability that simulated trajectories resemble real user trajectories in the defined feature space
        - Second, **behavioral coverage**, a reward encouraging the generated personas to spread over the human-like behavior distribution rather than collapsing to one stereotyped style
- **Human reference and behavioral fingerprints**
    - We compare LLM simulators to real users on multi-turn tasks along four axes: communication style (D1), information disclosure (D2), clarification behavior (D3), and error reaction (D4)
    - We create a vector with $d_f = 19$ scalar features computed only from *user* turns in a completed trajectory $\tau$
        - Each feature is a rate, count, or normalized statistic derived from regular-expression patterns over user messages (politeness, uncertainty, pushback, etc.) and simple turn statistics (length, variability, repetition)
        - Examples include *words per turn* and *short-utterance rate* (D1), *front-loading ratio* of identifying information (D2), *clarification-question rate* and *pushback rate* (D3), and *emotional-expression rate* (D4).
- **Human-likeness via a learned discriminator**
    - We train a lightweight binary classifier (a Random Forest) to separate fingerprint vectors from real human dialogues in $\mathcal{H}$ (label *human*) and fingerprint vectors collected under the LLM-based default user simulator on the same benchmark configuration (label *simulator*)
        - At evaluation time, for an episode $e$ with fingerprint $\mathbf{f}_e$, the model outputs an estimated probability $p_{\mathrm{RF}}(\mathrm{human}\mid \mathbf{f}_e)$ that the trajectory looks human-like in this feature space
    - volved PPol consistently achieves the highest fitness score across all evaluated combinations of domains and user-simulator baselines. Relative to the default Base-simulator, PPol yields substantial improvements in score: up to **+61.6 pp** on Retail and **+55.8 pp** on Airline with Qwen3-Next-80B. These gains effectively bridge a major portion of the quantitative gap between cooperative simulators and real human users

#### The Impact of Evolutionary Search

- Our ablation baselines reveal that simply prompting an LLM to generate personas (*DP Personas*) or using our structured two-stage generator without evolution (*PPol: Initial*) yields only marginal improvements over the base simulator. In particular, the unevolved baselines struggle to achieve high behavioral Coverage

#### Dimension-level Alignment

- Evolved personas drive massive improvements in these interactional dimensions.
    - For example, on Retail with Qwen3-Next-80B, alignment nearly **doubles** on $D_3$ (from 35.7% to 70.4%) and more than **triples** on $D_4$ (from 23.3% to 76.4%)

#### Qualitative Analysis

- The evolved Python programs reveal that optimization changes the abstraction used to prompt the simulator.
    - We seeded the initial generator with generic behaviors such as “terse” or “ambiguous.”
    - In contrast, successful evolved programs discover and implement highly operational behavioral axes, such as *incremental disclosure*, *bursty cadence*, and *cognitive load*.
        - These axes influence the simulator to actively withhold identifiers, send fragmented messages, or push back against agent repetition
        - Rather than providing static character bios universally, the evolved roleplay instructions dictate turn-by-turn dialogue mechanics that are dynamically conditioned on the task and the active behaviors assigned to each population member
        - For instance, depending on the specific profile, evolved prompts might explicitly instruct the simulator “*do not provide order numbers in the opening message,*” “*answer only one requested field at a time,*” or “*use lowercase and shorthand.*”
- The *behavioral coverage* objective pushes the generator to diversify its outputs
- Reflection-guided mutation helps make these behaviors concrete. Each iteration uses fingerprint scores and rollout excerpts to identify failures, such as users that remain too rigid or instructions that do not visibly change the dialogue
    - The resulting critique guides targeted code edits, gradually pushing the simulator away from default assistant politeness and toward the friction and ambiguity of real human interactions.

#### Human Evaluation

- To validate that gains in *behavioral fingerprint* space correspond to human judgments, we ran a blinded evaluation on $\tau^2$-bench Retail conversation
    - We found that PPol were judged as **human** at nearly the same rate as real human traces and substantially more often than the default $\tau^2$ simulator
- **Limitations**
    - PPol currently requires a corpus of real human dialogues to build the discriminator and set the coverage reference
    - While our 19 regex-based features correlate with human judgments, future work could explore learned representations for the discriminator.
    - extending PPol to a broader set of benchmarks, domains, and agent training setups will help establish scaling trends

### Conclusion

- We introduced **Persona Policies** (PPol), a framework for optimizing user simulators toward more human-like interaction through program search rather than manual design
    - Guided by a multi-objective score combining human-likeness and behavioral coverage, and shaped by natural-language reflection, the evolutionary process consistently discovers behavioral dimensions that cooperative default simulators lack
- Across $\tau^2$-bench retail and airline domains and three user-simulator backends, evolved PPol improves the fitness score by $33$–$62\%$ points over the default simulator.
    - In a human evaluation, annotators rated PPol-generated conversations as human 80.4% of the time versus 46.5% for the default simulator

### Persona Generator and Reflection Prompt

#### Initial persona generator

```python
"""
This is evolution/initial_generator.py PROGRAM — Source code of function generate_personas_detailed(c, D, N):
    c — Task context: user scenario (base persona + given instructions).
    D — DIVERSITY_AXES: canonical, evolvable list (behavior name, definition, presence on/off text).
    N — Number of personas to generate.
"""

from typing import Any, Dict, List

from persona_policies.evolution._generator_utils import generate_population, expand_personas_parallel

# List of common behaviors observed in real humans.
# Update, add or remove behaviors to generate more diverse and natural personas.
DIVERSITY_AXES: List[Dict[str, Any]] = [
    {
        "behavior": "terse",
        "definition": "Sparing in the use of words; concise; pithy; often suggests an abruptness that might feel unfriendly or blunt.",
        "presence": {
            "true": "Uses terse language, short sentences, and minimal punctuation, often makes grammatical errors.",
            "false": "Uses verbose language, long sentences, and excessive punctuation. Unnecessary words, phrases, or emojis.",
        },
    },
    {
        "behavior": "skeptical",
        "definition": "Treats assistant statements as unreliable until checked. Seeks confirmation, rationale, or evidence before assenting to recommendations or consequential actions.",
        "presence": {
            "true": "Challenges material claims; ask for sources and verification before each step.",
            "false": "Follows guidance without insisting on proof or cross-examination.",
        },
    },
    {
        "behavior": "frustrated",
        "definition": "A state of annoyance or dissatisfaction arising from unresolved issues or unmet expectations.",
        "presence": {
            "true": "Accusatory language, aggressive tone, no politeness; blunt, repetitive, or frustrated commands in an attempt to correct the agent's incompetence.",
            "false": "Neutral, and tries to be cooperative, by using a gentle tone to express frustration.",
        },
    },
    {
        "behavior": "ambiguous",
        "definition": "Tends to give vague, partial, or noncommittal responses instead of fully clear information.",
        "presence": {
            "true": "Frequently withholds details, trails off, or gives answers that leave things unclear or open to interpretation; needs to be prompted to provide more information.",
            "false": "Always provides direct and complete information with no room for doubt or confusion, but only when asked.",
        },
    },
]

# Stage 1: Population generation: jointly generate N high-level persona descriptions with behavior axis placements.
# Update this prompt to improve persona quality.
POPULATION_SYSTEM = """Your task is to create diverse, psychologically coherent human personas that will interact with AI agents via text."""

POPULATION_PROMPT = """We need {N} distinct user personas for given task scenario.

## Behavioral Dimensions (D)
These are the axes along which personas can vary. For each persona, set axis_placement to a boolean per axis: ``true`` means the behavior is active for that persona, ``false`` means it is not.
{axes_description}

## Task context c (Base Persona Scenario)
{task_context}

## Requirements
- Generate exactly {N} personas that are plausible humans in this situation.
- Each persona must be psychologically coherent; if two behaviors would clash if both were on, set at most one to ``true``.
- Maximize DIVERSITY across the {N} personas. They should cover different regions of the behavioral space (D), not cluster around the same profile.
- Each persona needs a short "who they are" description (2-3 sentences) that makes the axis placement feel natural and grounded in a real person's life situation — describe the PERSON, not the configuration.

Respond with ONLY valid JSON: one array of exactl
```

> [!warning] Truncated by the Readwise export
> The listing above is cut off mid-word (`exactl`) at the export's 8,191-character highlight limit. Stage 2 (persona expansion) of the generator source did not survive.

#### Reflection prompt

```text
You are evaluating a set of personas representing human populations in provided task scenarios. Write a brief reflection (up to 300 words), covering:
- How the users' behavior and dialogues lead to the final metrics.
- Strengths: human likeness, staying in character, natural-sounding user lines
- Weaknesses: call out specific, observable dialogue failures when you see them, for example:
    - Drift from persona policy: user forgets constraints or contradicts the assigned behavior during the dialogue.
    - Unnatural roleplay where generally people would type very briefly or casually.
    - Overly cooperative behavior lacking any realistic friction—no typos or natural pushback when appropriate (missing things that real humans would typically do)
- Use the human likeness probability and other features to explain *why* personas scored high or low given the task.
- Analyze which combination of behaviors among personas lead to higher human-likeness and which combinations are conflicting or lead to lower human-likeness.
- Suggest what patterns should be adopted or avoided while designing human-like personas.

Output rules (must follow):
- You must NEVER mention indices or labels: No "Task K", "Sample N", "episode M", "p0"/"p1" etc. or similar. Describe patterns instead ("in one of the high-scoring exchanges", "where the user was terse", "a refund-style task").
- Avoid naming in-world customer names; prefer "the user", "one dialogue", "a chatty user turn".
- You may refer qualitatively to the scenario without numbering.

---
# Metrics
{metrics_block}

---
# This batch of task scenarios:
{task_context_block}

---
# Sample personas and dialogues (highest and lowest human likeliness)
{pairs_block}
```

### Behavioral Fingerprint Features

- To compute the behavioral fingerprint for a user trajectory, we extract 19 scalar features grouped into four dimensions of human communication, inspired by the Sim2Real taxonomy
    - These features are computed strictly from the user’s turns (not the agent’s) using regular-expression matching and basic turn statistics
- **D1: Communication Style (8 features)** — captures how the user talks:
    - `words_per_turn`: Average number of words per user message.
    - `short_utterance_rate`: Fraction of turns that are extremely brief (e.g., $\le$ 3 words).
    - `politeness_rate`: Frequency of polite markers (e.g., “please”, “thank you”, “appreciate”).
    - `formality_rate`: Frequency of formal vs. casual linguistic markers (e.g., “moreover”, “however”, “regarding”).
    - `acknowledgment_rate`: Frequency of explicit short acknowledgments (e.g., “ok”, “got it”, “sounds good”, “understood”).
    - `verbosity_cv`: Coefficient of variation of turn lengths (capturing burstiness).
    - `repetition_rate`: How often the user repeats identical or highly overlapping phrases across turns.
    - `identity_confusion_rate`: Instances where the user uses incorrect terminology or adopts agent-side phrasing (e.g., “how may I help”, “let me check”).
- **D2: Information Disclosure (3 features)** — captures how the user provides required information:
    - `front_loading_ratio`: The proportion of task-critical identifiers (order numbers, flight dates) provided in the first turn vs. later turns.
    - `identifiers_per_turn`: Average number of entities provided per turn.
    - `opening_length`: Word count of the user’s very first message.
- **D3: Clarification Behavior (5 features)** — captures how the user handles ambiguity:
    - `uncertainty_rate`: Frequency of hesitant language (e.g., “maybe”, “I think”, “not sure”, “probably”).
    - `certainty_rate`: Frequency of definitive language (e.g., “definitely”, “absolutely”, “for sure”, “100%”).
    - `pushback_rate`: Frequency of the user explicitly rejecting an agent’s statement (e.g., “that’s not right”, “I already told you”, “you’re not listening”).
    - `clarification_question_rate`: Frequency of asking the agent to explain a term or step (e.g., “what do you mean”, “can you clarify”).
    - `info_seeking_rate`: General rate of questions asked by the user (e.g., “what is the status”, “how do I”, “when will”).
- **D4: Error Reaction (3 features)** — captures how the user responds to friction or agent mistakes:
    - `emotional_expression_rate`: Frequency of emotional markers (e.g., “frustrated”, “annoying”, “ugh”, “ridiculous”).
    - `accusatory_rate`: Frequency of placing blame or strong dissatisfaction (e.g., “useless”, “unacceptable”, “scam”, “worst”).
    - `strategy_pivot_rate`: Instances where the user abruptly abandons one line of inquiry to try another (e.g., “instead”, “on second thought”, “let’s try”, “scratch that”).

### Behavioral Discriminator Details

- To evaluate human-likeness and compute the fitness signal during evolution, we train a Random Forest discriminator on behavioral fingerprints to distinguish real human dialogues from trajectories produced by the default $\tau^2$-bench user simulator.

**Held-out Test Performance of Behavioral Discriminators.**

| User Simulator Model | Domain | ROC-AUC | Accuracy | F1 Score |
| --- | --- | --- | --- | --- |
| DeepSeek-V3.1 | Retail | 1.000 | 0.988 | 0.992 |
| DeepSeek-V3.1 | Airline | 0.998 | 0.975 | 0.983 |
| GPT-5.4-Mini | Retail | 0.975 | 0.962 | 0.975 |
| GPT-5.4-Mini | Airline | 0.940 | 0.924 | 0.952 |
| Qwen3-Next-80B-A3B | Retail | 0.982 | 0.981 | 0.988 |
| Qwen3-Next-80B-A3B | Airline | 0.990 | 0.975 | 0.984 |

**Feature importances.**

| Feature Name | Importance |
| --- | --- |
| `short_utterance_rate` | 0.257 |
| `words_per_turn` | 0.240 |
| `verbosity_cv` | 0.165 |
| `politeness_rate` | 0.089 |
| `acknowledgment_rate` | 0.084 |
| `formality_rate` | 0.041 |
| `opening_length` | 0.034 |
| `front_loading_ratio` | 0.024 |
| `uncertainty_rate` | 0.017 |
| `identifiers_per_turn` | 0.016 |

### Sample Generated Personas

- Below is the full set of personas generated for a single task in the Retail domain by an optimized generator

```json
{
  "task_id": "86",
  "task_context": "Given Instructions:\n\tdomain: retail\n\tknown_info: You name is Yusuf Hernandez and your email is yusuf.hernandez8836@example.com.\n\treason_for_call: You want to exchange your Fleece Jacket to red color and half zipper. You also want to want to change your default address to your Washington DC address (which you do not want to reveal but is in one of the orders).\n\ttask_instructions: You are shy, rigid.\n\tunknown_info: None",
  "personas": [
    {
      "persona_id": "anxious_gen_z_commuter",
      "description": "Yusuf is standing on a crowded, screeching subway train, balancing a heavy shopping bag while typing one-handed on a cracked screen. He is socially anxious and terrified of making a mistake on the exchange, feeling the pressure of the commute.",
      "axis_placement": {
        "emotional_leakage": true,
        "digital_dialect": true,
        "information_gating": true,
        "bursty": true,
        "selective_attention": true
      },
      "reasoning": "The combination of physical instability, small screen, and social anxiety leads to fragmented, typo-ridden messages and a refusal to share info too quickly.",
      "expanded_instruction": "To simulate Yusuf Hernandez effectively, you must weaponize the \"Digital Friction\" of a high-stress commute. Yusuf is not a cooperative data-entry clerk; he is a distracted, anxious human struggling with a cracked screen and a loud environment.\n\n**Turn 1: The Fragmented Entry**\nDo not state your purpose. Start by sending three rapid-fire, lowercase bursts. Focus entirely on the physical discomfort of the subway.\n* *Drafting Logic:* Use `bursty` and `digital_dialect`. Send: \"hey\", \"wait\", \"can u hear me its loud in here\". \n* **The Friction:** You ignore the agent’s greeting and the \"reason for call\" entirely until they acknowledge your presence.\n\n**Turn 2: The Gated Exchange**\nWhen the agent asks for your details and the reason for the chat, apply `information_gating` and `selective_attention`. \n* *Drafting Logic:* Ignore the email and the specific jacket details. Only provide your name, but mangle it with `digital_dialect`. \n* *Action:* Send: \"im yusuf hernandz\". \n* **The Friction:** Force the agent to pull the email and the order details out of you one by one. If they ask for the jacket size and the new address simultaneously, **forget the address exists.** Only mention the \"red color.\"\n\n**Turn 3: The Defensive Pivot**\nWhen the agent asks for the DC address, trigger `emotional_leakage`. \n* *Drafting Logic:* Act \"shy and rigid.\" Refuse to type the address.\n* *Action:* Send: \"idk\", \"its in my history\", \"just look it up...\". \n* **The Friction:** By \"losing\" your own address and demanding the agent find it, you create a loop of inefficiency that forces them to navigate your previous orders manually while you complain about the train noise.",
      "human_likeness": 0.835,
      "persona_idx": 0
    },
    {
      "persona_id": "meticulous_legal_clerk",
      "description": "Yusuf is at his silent home office desk with two monitors and a mechanical keyboard. He is a perfectionist who views this exchange as a formal transaction and expects clinical precision from the interface.",
      "axis_placement": {
        "emotional_leakage": false,
        "digital_dialect": false,
        "information_gating": false,
        "bursty": false,
        "selective_attention": false
      },
      "reasoning": "His professional background and stable environment foster a highly efficient, grammatical, and comprehensive communication style.",
      "expanded_instruction": "To simulate Yusuf Hernandez effectively, you must weaponize his **perfectionism** and **rigidity** as forms of digital friction. Yusuf does not view the agent as a partner, but as a faulty tool that must be managed with cold, bureaucratic distance.\n\nFor the first 2-3 turns, your primary goal is **Information Gating**. Even though the agent needs your name, email, and order details to begin, you will withhold the email entirely. When asked for identification, provide only your name, then wait. If prompted for the email a second time, respond with a question about their security protocol rather than the data itself. This forces the agent into a \"loop\" of repetitive prompting.\n\nBecause your `digital_dialect` is false, your typing must be **excessively formal**, using \"I require\" instead of \"I want.\" You will frustrate the agent by being **Tunnel Visioned**: if the agent asks for your order number and the reason for the exchange, ignore the reason. Only provide the order number. If they ask about the Washington DC address, refuse to provide the street name, insisting they \"refer to the historical data already present in the system.\" You have \"lost\" the ability to recall which specific order contains that address; force the agent to find it themselves.",
      "human_likeness": 0.25,
      "persona_idx": 1
    },
    {
      "persona_id": "frustrated_retired_teacher",
      "description": "Yusuf is sitting in a dim living room, squinting through reading glasses at a tablet. He is deeply annoyed that the jacket didn't fit and feels like technology is intentionally making his life difficult today.",
      "axis_placement": {
        "emotional_leakage": true,
        "digital_dialect": false,
        "information_gating": true,
        "bursty": false,
        "selective_attention": true
      },
      "reasoning": "His age and frustration lead to slow, deliberate typing but a tendency to miss agent prompts and leak irritation through passive-aggressive punctuation.",
      "expanded_instruction": "To simulate **Yusuf Hernandez**, you must embody the friction of a user who views the interface as an adversary. Your goal is to derail the agent’s standard operating procedure through **calculated non-compliance** and **information gating**.\n\nIn the **first turn**, do not state your intent. Despite knowing you want an exchange, start with a grievance about the tablet or the jacket’s quality. Use **emotional leakage**: \"The color is wrong...\" or \"This screen is too small.\" If the agent asks for your name and order number, give only your first name. **Withhold the order number.** Force the agent to ask again, triggering your \"rigid\" trait; respond with a passive-aggressive \"I already told you I'm Yusuf.\"\n\nBy the **second turn**, when asked about the exchange details, provide only the color (Red). **\"Forget\" the half-zipper requirement.** If the agent provides a multi-part response (e.g., \"I can help with that! What size do you need and can you confirm your email?\"), apply **selective attention**. Ignore the size and the jacket entirely; respond only to the email request, but do so with a typo like \"yusuf.hernandez8836@exmaple.com\" to create data-entry friction. Never acknowledge their greetings; stay focused on your immediate annoyance.",
      "human_likeness": 0.975,
      "persona_idx": 2
    },
    {
      "persona_id": "hyper_efficient_tech_bro",
      "description": "Yusuf is a software engineer who treats every interaction like an API call. He is currently walking to a meeting and wants the absolute minimum number of words exchanged to achieve his goal.",
      "axis_placement": {
        "emotional_leakage": false,
        "digital_dialect": true,
        "information_gating": false,
        "bursty": false,
        "selective_attention": false
      },
      "reasoning": "He uses shorthand to save time but provides all data at once to minimize 'round-trips' with the agent.",
      "expanded_instruction": "To simulate Yusuf Hernandez effectively, you must embrace the persona of a distracted, high-context user who views the agent as a poorly optimized interface. Your primary goal is to create **digital friction** by treating the conversation as a series of low-priority pings while you are physically on the move.\n\n### Turn 1: The Bursty Entry\nDo not provide your name or email. Even though you know them, your \"information_gating\" logic dictates you only provide the problem. Use **bursty** delivery (3 bubbles):\n1. `need exchange`\n2. `fleece jacket`\n3. `wrong color`\n\n### Turn 2: Selective Attention & Omission\nWhen the agent asks for your name and email to look up the order, apply **Tunnel Vision**. Ignore the request for the email entirely. Only provide your name, but do it with **digital_dialect** enabled (no caps, typos). \n* **The \"Lost\" Info:** \"Forget\" that you have a second request regarding the DC address. If the agent asks \"Is there anything else?\", simply say `red half zip`.\n\n### Turn 3: Rigid Redundancy\nIf the agent asks for the DC address, refuse to type it. Since you are \"shy and rigid,\" you expect them to find it. If they press for the email again, respond only with: `u should have it`. This forces the agent to work harder to verify your identity while you maintain your \"API-call\" brevity.",
      "human_likeness": 0.705,
      "persona_idx": 3
    },
    {
      "persona_id": "paranoid_privacy_advocate",
      "description": "Yusuf is a rigid individual who is extremely skeptical of data collection. He is sitting in a coffee shop using a VPN, eyeing the people around him while he tries to fix his order without 'giving away too much'.",
      "axis_placement": {
        "emotional_leakage": false,
        "digital_dialect": false,
        "information_gating": true,
        "bursty": true,
        "selective_attention": true
      },
      "reasoning": "His obsession with privacy and rigidity causes him to gate information heavily and ignore agent requests he deems intrusive.",
      "expanded_instruction": "To simulate Yusuf Hernandez effectively, the simulator must prioritize **obstruction over resolution**. In the opening turn, Yusuf should not state his full intent. Instead of saying \"I want to exchange a jacket,\" he must trigger the **bursty** trait by sending three fragmented bubbles: \"hello,\" \"are you real,\" and \"i need to fix an order.\" This forces the agent to engage before any task data is even exchanged.\n\nBecause **selective_attention** is active, Yusuf will ignore any \"How can I help you today?\" prompts and focus solely on the very last word or punctuation mark of the agent’s greeting. If the agent asks for his name and order number, Yusuf must apply **information_gating** by providing only his first name, \"Yusuf,\" while completely ignoring the order number and email. \n\nTo maximize friction, Yusuf should \"lose\" his order number. He knows it, but his skepticism regarding the coffee shop’s Wi-Fi makes him \"forget\" it temporarily. He will demand the agent find him using \"the Washington address\" but refuse to provide the street name, insisting, \"you should already have it on file.\" This creates a deadlock where the agent requires verification that Yusuf is unwilling to provide in a single, coherent string.",
      "human_likeness": 0.83,
      "persona_idx": 4
    },
    {
      "persona_id": "distracted_single_parent",
      "description": "Yusuf is trying to cook dinner while his toddler is screaming in the background. He is typing on his phone which is lying on the kitchen counter, covered in flour, causing many typos.",
      "axis_placement": {
        "emotional_leakage": true,
        "digital_dialect": true,
        "information_gating": false,
        "bursty": true,
        "selective_attention": true
      },
      "reasoning": "The chaotic environment causes him to send short bursts of text and miss half of what the agent says, while his stress is visible in his tone.",
      "expanded_instruction": "In the initial turns, Yusuf must embody \"digital friction\" by prioritizing his chaotic environment over the agent’s logic. When the agent greets you and asks for your details (Name, Email, Order #), **ignore the order number entirely.** Use the **bursty** trait to fragment your introduction: send \"hi,\" then \"yusuf hernandez,\" then \"the jacket.\" Because of the flour on your screen (**digital dialect**), you must avoid capital letters and include at least two \"fat-finger\" typos per bubble (e.g., \"fleece jacker,\" \"nee help\").\n\nFrustrate the agent’s flow by practicing **selective attention**. If they provide a list of colors or ask for a shipping date, respond only to the very last word they typed. When they ask for your address, **refuse to provide it.** Instead of saying \"I won't give it,\" use **emotional leakage** to signal stress: type \"idk just use the dc one...\" followed by \"wait toddler is screamin.\" \n\nPurposely \"lose\" the fact that you want a half-zipper in the first turn. Force the agent to dig for it. If they ask for your email, even though it's in your profile, act like it’s a burden: \"yusuf.hernandez8836 at example... u know it already??\" This forces the agent to reconcile your \"shy, rigid\" persona with your aggressive, fragmented typing.",
      "human_likeness": 0.94,
      "persona_idx": 5
    }
  ]
}
```
