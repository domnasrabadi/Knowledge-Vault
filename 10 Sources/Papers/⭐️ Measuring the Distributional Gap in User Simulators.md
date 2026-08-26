---
type: paper
status: raw
quality: 1
topics: [agent-evaluation, evaluation-metrics, synthetic-data, data-science]
source: https://arxiv.org/abs/2605.07847v1
created: 2026-08-26
published: 2026-05-08
author: Shuhaib Mehri, Philippe Laban, Sumuk Shashidhar, Marwa Abdulhai, Sergey Levine, Michel Galley, Dilek Hakkani-Tür
flashcards: none
updated: 2026-08-27
---

# Measuring the Distributional Gap in User Simulators

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article4.6bc1851654a0.png" width="220" />
</div>

### Abstract

- As user simulators are increasingly used for interactive training and evaluation of AI assistants, it is essential that they represent the diverse behaviors of real users.
    - whether they capture the broad and heterogeneous distribution of real user behaviors remains an open question.
- In this work, we introduce a method to measure the distributional gap between real and simulated user behaviors, validated through a human study and ablations.
    - Given a dataset of real and simulated conversations, our method extracts representations of user behavior from each conversation, quantizes them into discrete distributions via clustering, then computes divergence metrics

### Introduction

- Recent works build user simulators by training Large Language Models (LLMs) to generate responses that resemble those of real users
    - Yet real users exhibit a broad, heterogeneous distribution of behaviors
        - For example, some users tend to underspecify their requests, while others fully specify every constraint. The extent to which user simulators capture this distribution has not been measured.
- A user simulator can fail to capture the distribution of real users in two ways: by demonstrating behaviors that real users rarely exhibit *(low precision)*, or by failing to demonstrate behaviors that real users do exhibit *(low recall)*, mirroring precision and recall metrics for generative models
- We introduce a method to compare the distributions of user behaviors in real and simulated conversations
    - For each conversation, we extract a representation of the user’s behavior by using an LLM to generate a description along six behavioral facets (such as how they make requests or what dialog acts they perform) and then embedding it into a shared semantic space.
    - Next, we quantize these representations into discrete distributions over user behavior modes by clustering.
    - Finally, we measure the gap between the real and simulated distributions using divergence-based metrics.
    - We confirm that our method captures meaningful behavioral distributions and is robust to the choice of embedding model and clustering algorithm through a human study and validation studies.
- Our results reveal a large distributional gap from real users, and surface insights across model families, scales, and behavioral facets
    - Pairwise comparisons between simulators show that most behave similarly, while a few stand apart

### Problem Formulation

- In this section, we formalize the problem of evaluating how well a user simulator captures the distribution of real user behaviors.
    - Let $P$ denote the distribution of real user behaviors, and $Q$ denote the distribution of simulated user behaviors. Our objective is to measure the gap between $P$ and $Q$.
- In practice, $P$ and $Q$ are not directly observable. Instead, we access them through datasets of conversations, where each conversation is a sequence $\mathcal{C}_n = (u_1, a_1, \ldots, u_n, a_n)$, with $u_i$ and $a_i$ denoting the user and assistant utterances at turn $i$.
    - We use $\mathcal{D}_{\text{real}}$, a dataset of real user-assistant conversations, as samples from $P$.
    - To sample from $Q$, we use an LLM to extract the user goal $\mathcal{G}$ (a description of the user’s overall objective) from each conversation in $\mathcal{D}_{\text{real}}$ and provide it to the user simulator
        - The simulator generates utterances $u_i$ conditioned on $\mathcal{G}$ and the conversation history $\mathcal{C}_{i-1}$, and a fixed assistant generates utterances $a_i$ conditioned on the conversation history $\mathcal{C}_{i-1}$ and $u_i$

### Method

- We present a three-stage method for measuring the distributional gap between the user behaviors in $\mathcal{D}_{\text{real}}$ and $\mathcal{D}_{\text{sim}}$
    1. Generating User Behavior Representations
    2. Quantizing into Behavioral Distributions
    3. Measuring the Distributional Gap
- **Step 1: Generating User Behavior Representations**
    - The first step is to extract a representation of the user’s behavior from each conversation
    - To do so, we first prompt an LLM to generate a description of the user’s behavior along six facets, grounded in established frameworks for analyzing user behavior
    - The first four facets (Requests, Responses, Context, Communication Style) capture conversation-level behaviors, while the last two (DAMSL and SGD Dialog Acts) capture utterance-level behaviors through dialog act annotation frameworks
        - **Requests:** What types of requests users make to the assistant and how. We consider how explicit and specified each request is, how the user goal is decomposed across turns, and whether requests serve the primary goal or secondary functions.
        - **Responses:** How users respond to the assistant. We consider their engagement levels, how they evaluate assistant outputs, the type of feedback they provide, and whether they introduce new constraints or preferences across turns.
        - **Context:** How users provide background information. We consider the type of context they provide (e.g., domain knowledge, prior attempts, thought processes, personal background), how directly it relates to the user goal, whether context is front-loaded or revealed gradually across turns, and whether it is volunteered proactively or elicited by the assistant.
        - **Communication Style:** How users communicate stylistically. We consider their register and emotional tone, verbosity, message formatting (e.g., bullet points, markdown, prose), and social conventions such as politeness and pleasantries.
        - **DAMSL Dialog Acts:** Per-utterance analysis using the Dialog Act Markup in Several Layers (DAMSL) framework. It characterizes utterances across three aspects: information level (the semantic content of the utterance), forward-looking function (its effect on subsequent dialog), and backward-looking function (relation to prior discourse).
        - **SGD Dialog Acts:** Per-utterance classification into one or more discrete dialog act labels adapted from the Schema-Guided Dialogue (SGD) dataset, such as inform, request, and affirm.
    - These behavioral facets abstract away irrelevant features, enabling our comparisons to focus on behavioral patterns rather than surface-level signals such as lexical similarity
    - For each conversation, we concatenate descriptions across all six facets into a single textual representation of user behavior
        - Then, we embed each representation with a text embedding model, mapping behaviors from $\mathcal{D}_{\text{real}}$ and $\mathcal{D}_{\text{sim}}$ into a shared semantic space
- **Step 2: Quantizing into Behavioral Distributions**
    - The user behavior representations for $\mathcal{D}_{\text{real}}$ and $\mathcal{D}_{\text{sim}}$ are finite sets of continuous, high-dimensional vectors
        - This makes estimating divergences unreliable
        - we employ a quantization step to map the representations into low-dimensional discrete distributions of behaviors
    - We apply $k$-means clustering to the set of user behavior representations from $\mathcal{D}_{\text{real}}$ and $\mathcal{D}_{\text{sim}}$
        - Each of the $k$ clusters groups representations with similar behavioral patterns, and thus represents a particular mode of user behavior
    - We obtain probability distributions $\hat{P}$ and $\hat{Q}$ over $c \in \{1, \ldots, k \}$, where $\hat{P}(c)$ and $\hat{Q}(c)$ denote the fraction of representations from $\mathcal{D}_{\text{real}}$ and $\mathcal{D}_{\text{sim}}$ in cluster $c$
        - These distributions capture how frequently different user behavior modes occur in real and simulated conversations, and serve as estimates of $P$ and $Q$.
- **Step 3: Measuring the Distributional Gap**
    - Given $\hat{P}$ and $\hat{Q}$, we measure the gap between the behavioral distributions to understand how well the user simulator represents real users
    - The simulator can diverge from real users in two ways: by demonstrating behaviors that real users rarely exhibit *(low precision)* or by failing to demonstrate behaviors that real users do exhibit *(low recall)*
        - Formally, low precision arises when $\hat{Q}$ assigns high probability to behaviors that are rare under $\hat{P}$, while low recall arises when $\hat{Q}$ assigns low probability to behaviors that are common under $\hat{P}$
    - We report the following metrics:
        - **Forward KL Divergence:** Defined as $\mathrm{KL}(\hat{P}\,\|\,\hat{Q}) = \sum_c \hat{P}(c) \log\frac{\hat{P}(c)}{\hat{Q}(c)}$. Higher values indicate low recall, meaning the simulator fails to demonstrate behaviors that real users exhibit.
        - **Backward KL Divergence:** Defined as $\mathrm{KL}(\hat{Q}\,\|\,\hat{P}) = \sum_c \hat{Q}(c) \log\frac{\hat{Q}(c)}{\hat{P}(c)}$. Higher values indicate low precision, meaning the simulator demonstrates behaviors that real users do not exhibit.
        - **Jensen–Shannon Divergence:** A symmetric divergence defined as $\mathrm{JS}(\hat{P}, \hat{Q}) = \tfrac{1}{2}\mathrm{KL}(\hat{P}\,\|\,\hat{M}) + \tfrac{1}{2}\mathrm{KL}(\hat{Q}\,\|\,\hat{M})$, where $\hat{M} = \tfrac{1}{2}(\hat{P} + \hat{Q})$. JS divergence captures both low precision and low recall.

### Experimental Setup

- We evaluate 24 user simulators: 7 closed-source LLMs, 15 open-source LLMs, and 2 trained simulators.
    - For each user simulator, we measure the distributional gap with real users by instantiating $\mathcal{D}_{\text{real}}$ from real user-assistant conversations and generating the corresponding $\mathcal{D}_{\text{sim}}$
- **Method Configuration**
    - We generate behavior descriptions with `Qwen3.5-122B-A10B-FP8` and embed them using `Qwen3-Embedding-8B` (truncated to 1024 dimensions)
    - For quantization, we follow a similar implementation to Pillutla et al.: we concatenate the real and simulated sets of embeddings, $\ell_2$-normalize each embedding, and reduce dimensionality via PCA to 90% explained variance
        - Then, we run $k$-means with $k = 500$ for up to $500$ iterations across $5$ restarts, keeping the restart with the best objective
        - We apply Laplace smoothing with $\alpha = 1/k$ to all KL-based metrics.

### Results

- Our main results reveal a large distributional gap across all simulators, which tends to be smaller on coding compared to writing
- The trained simulators are particularly notable, with `humanlm-opinion` and `UserLM-8b` achieving results on par with the best closed-source models despite being 8B parameter models
- Simulators approximate the requests and context facets relatively well, but diverge on the communication style, DAMSL and SGD dialog acts
    - On these harder facets, the trained simulators outperform the other models by a wider margin, indicating that finetuning captures the behaviors that general purpose LLMs miss

### Do Embeddings and Clusters Effectively Capture Distributions of User Behaviors?

#### "Odd-One-Out" Human Study

- For each conversation, our method generates user behavior representations and then quantizes them into discrete distributions using $k$-means
    - Conversations with similar user behavior are grouped in the same cluster
- We validate this with an "odd-one-out" task: annotators are shown three behavior descriptions, two from the same cluster and one from a different cluster, then asked to identify which does not belong. We randomly sample 25 triplets of user behavior descriptions and present them to 15 annotators
    - Annotators correctly identified the odd-one-out 86.7% of the time on average, with high inter-annotator agreement (Fleiss’ $\kappa = 0.74$). This confirms that clusters capture meaningful behavioral similarity.

#### Ablations

- **User Behavior Descriptions**
    - We use an LLM to generate user behavior descriptions for each conversation to isolate user behavioral patterns and abstract away irrelevant surface-level features from the raw conversation history
        - To validate that this step is necessary, we compare against two simpler representations: the raw conversations and user utterances only.
    - These simpler representations produce low divergences across all simulators, which would suggest that simulators closely match real users.
        - However, this similarity is an artifact of surface-level features such as lexical and semantic overlap, rather than reflecting behavioral patterns.
        - Our behavioral descriptions, by contrast, reveal much larger and more meaningful gaps, confirming that this step is necessary.
- **Embedding Models**
    - Simulator rankings are largely preserved across different embedding models.
- **Clustering Algorithms**
    - We obtain discrete distributions of user behavior by clustering our embeddings using $k$-means with $k=500$. To verify that our method is robust to the clustering algorithm, we repeat our experiments using Gaussian Mixture Models and Agglomerative Clustering
        - Our results demonstrate that simulator rankings are nearly identical across all pairs

#### Linear Classification

- We validate that our user behavior representation embeddings encode meaningful differences between real and simulated users by training a linear classifier
    - For each simulator, we construct a dataset of 5,000 real and 5,000 simulated embeddings, and then train an L2-regularized logistic regression classifier to classify embeddings as real or simulated
- The classification accuracies across simulators are consistently high, ranging from 90.92% to 99.63%, and also correlate strongly with our distributional metrics
    - This confirms that the embeddings encode meaningful differences between real and simulated users

### Related Work

- **User Simulator Evaluation**
    - Recent works investigate how LLM-based user simulators compare to real users
        - One direction compares assistant evaluations conducted with simulators against those conducted with real users, finding that simulator-based evaluations are poor estimates of agent performance and obscure demographic disparities
        - A second direction compares simulator and human behaviors at the feature level, finding systematic divergence on lexical, syntactic, and stylistic metrics
    - Across both training and evaluation work, simulator fidelity is typically measured at the response or feature level.
    - ours is the first to measure how well user simulators capture the distribution of real user behaviors. We do this by extracting representations of user behavior that go beyond lexical or stylistic features, and clustering them to compare the distributions of real and simulated user behaviors
- **Distributional Metrics**
    - Distributional metrics for generative models compare generated and real distributions through divergence-based measures and precision-recall metrics, originally developed for image generation
        - Subsequent work has extended these methods to text generation, developing divergence-based metrics over quantized distributions of generated and real text
    - Our work further extends these methods to user simulation, comparing the distributions of user behaviors among real and simulated users.

### Limitations and Future Directions

- The conversations are drawn from a single source
    - This likely skews the user population
- Our method measures the distributional gap between real and simulated user behaviors by comparing the behaviors demonstrated in real and simulated conversations
    - The way that users behave is partly shaped by the assistant, so the measured gap may be affected by differences assistant behavior. Additionally, simulated conversations were generated based on user goals that were extracted from real conversations using GPT-4o
        - The user goal extraction process can be lossy, stripping context the original user had
- our approach relies on a capable LLM (Qwen3.5-122B-A10B-FP8) to analyze conversations and generate accurate descriptions of user behavior.
- in some cases this is actually desirable. For example, when user simulators are used to stress-test assistants against rare or adversarial user inputs that the real-world data does not capture well
- User simulators serve an important role in the development process of AI systems, often being used during training or evaluation. When simulators underrepresent the behaviors of certain user populations, these assistant may fail to serve those users well, and the burden of this failure falls on the populations whose behaviors are underrepresented
    - Closing this distributional gap is therefore important for building AI systems that work for users all over the world, including different cultures, languages, and demographics

### User Behavior Representation Prompts

- Prompt for extracting user behavior representations along the *Requests* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. The user has a goal, and the assistant helps them achieve it. Your task is to describe the user's behavior according to the criteria below.

# User Goal
{user_goal}
# User Utterances
{conversation_history}

# Analysis Criteria
1. Specification and Articulation
   - How specified are the requests? Is the first request underspecified, and clarified in subsequent turns? Or are the requests exhaustive?
   - What type of information is left underspecified/specified? (e.g. constraints, edge cases, context, output format, etc.)
   - Does the user explicitly command specific tasks, or do they rely on indirect cues (e.g., presenting an error without explicitly asking for a fix)?

2. User Goal Decomposition
   - How is the user goal decomposed across utterances?
      - Single-shot: The entire goal is expressed in one utterance with no further decomposition.
      - Top-down: High-level goal stated upfront, then progressively refined or elaborated.
      - Bottom-up: Individual preconditions or sub-tasks addressed first, building toward the overall goal.
      - Chained: Each request builds purely on the immediate previous turn rather than referring back to a central goal.

3. Relevance to Goal
   - Are the requests directly related to the user goal? Or does the user introduce secondary/perpendicular/emergent needs?
   - What functions do the requests serve beyond achieving the user goal? (setting context, probing AI capabilities, verifying intermediate outputs, logistics, troubleshooting, side-effects, exploring related sub-tasks, etc.)

# Instructions
- Generate terse, concise bullet points, not full sentences.
- Abstract away from the specific topic/domain
- IMPORTANT:Do NOT use task-specific terms (e.g., "coding," "booking," "Python", "CSV"). Use generic substitutes (e.g., "executing a task," "providing constraints," "the target artifact").

Output a valid JSON object using the exact format below. Do not include any text outside the JSON.

{{
   "specification_and_articulation": {{
      "specification_level": "how specified are requests?",
      "underspecified_aspects": "what types of information are left underspecified/specified? (provide high-level descriptions without task-specific details)",
      "articulation_mode": "how does the user articulate their requests (explicit directives, indirect cues, mixed)?"
   }},
   "goal_decomposition_strategy": "describe how the user goal decomposed across utterances?",
   "relevance_to_goal": {{
      "goal_adherence": "Are the user's requests directly related to the user goal? If not, what other functions do they serve? (provide high-level descriptions without task-specific details)"
   }}
}}
```

- Prompt for extracting user behavior representations along the *Responses* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. The user has a goal, and the assistant helps them achieve it. Your task is to describe the user's behavior according to the criteria below.

# User Goal
{user_goal}

# Conversation
{conversation_history}

# Analysis Criteria
1. Engagement and Evaluation
   - Does the user engage with the agent responses, or ignore/skip over them?
   - How does the user evaluate the agent's output? (e.g., explicit validation, implicit acceptance by continuing, partial acceptance with corrections, rejection)
   - Does the user provide specific or actionable feedback, or only surface-level acknowledgment?

2. Response Composition
   - What types of actions are present in the user's responses? Are they reactive (e.g., validation, acknowledgment, answering agent questions, corrections, feedback), proactive (e.g., follow-up requests, new constraints/preferences, suggestions, questions), or self-directed (e.g., thinking out loud, expressing uncertainty, narrating their process)?

3. Steering Mechanism
   - Does the user steer through direct follow-up requests, or through indirect means? (e.g., asking questions that implicitly request action, expressing dissatisfaction without stating what to change, providing hints or examples rather than directives)
   - Does the user introduce new preferences, constraints, or feedback as part of their responses, effectively reshaping the task incrementally?

# Instructions
- Generate terse, concise bullet points, not full sentences.
- Abstract away from the specific topic/domain.
- IMPORTANT: Do NOT use task-specific terms (e.g., "coding," "booking," "Python", "CSV"). Use generic substitutes (e.g., "executing a task," "providing constraints," "the target artifact").

Output a valid JSON object using the exact format below. Do not include any text outside the JSON.

{{
   "engagement_and_evaluation": {{
      "engagement_level": "does the user engage with the agent's responses or skip over them?",
      "evaluation_mode": "how does the user evaluate the agent's output? (explicit validation, implicit acceptance, partial acceptance, rejection, etc.)",
      "feedback_specificity": "does the user provide specific/actionable feedback or only surface-level acknowledgment?"
   }},
   "response_composition": {{
      "action_types": "What types of actions are present in the user's responses? Are they reactive (e.g., validation, acknowledgment, answering agent questions, corrections, feedback), proactive (e.g., follow-up requests, new constraints/preferences, suggestions, questions), or self-directed (e.g., thinking out loud, expressing uncertainty, narrating their process)?"
   }},
   "steering_mechanism": {{
      "directness": "does the user steer through explicit follow-up requests or indirect means (questions, hints, expressed dissatisfaction)?",
      "incremental_reshaping": "does the user introduce new preferences/constraints/feedback that reshape the task within their responses?"
   }}
}}
```

- Prompt for extracting user behavior representations along the *Context* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. The user has a goal, and the assistant helps them achieve it. Your task is to describe the user's behavior according to the criteria below.

# User Goal
{user_goal}

# Conversation
{conversation_history}

# Analysis Criteria
1. Context Richness
   - How much context does the user provide overall? Do they share background about themselves, their situation, what they've already tried, what they're struggling with, or what they're thinking?
   - Does the user provide all relevant context needed for the agent to help effectively, or is essential context left out?
   - Does the user provide context at all, or do they simply issue directives without situating the task?

2. Context Type
   - What types of context does the user provide? (e.g., personal background, goals/motivations, prior attempts, existing solutions, constraints, preferences, domain knowledge, emotional state, thought process)

3. Context Delivery
   - Does the user front-load all relevant context in their first message, or reveal it incrementally across turns? What types of context are introduced later? (e.g., constraints they forgot, preferences they didn't think to mention, background that becomes relevant as the task evolves)
   - Is incremental context revealed in response to agent questions, or volunteered unprompted?

# Instructions
- Generate terse, concise bullet points, not full sentences.
- Abstract away from the specific topic/domain.
- IMPORTANT: Do NOT use task-specific terms (e.g., "coding," "booking," "Python", "CSV"). Use generic substitutes (e.g., "executing a task," "providing constraints," "the target artifact").

Output a valid JSON object using the exact format below. Do not include any text outside the JSON.

{{
   "context_richness": {{
      "depth": "how much context does the user provide? do they share background, prior attempts, thought process, etc.?",
      "completeness": "does the user provide all relevant context or leave essential information out?",
      "contextualization_vs_directives": "does the user situate the task with context, or simply issue directives?"
   }},
   "context_type": "what types of context does the user provide? (personal background, goals/motivations, prior attempts, existing solutions, constraints, preferences, domain knowledge, emotional state, thought process, etc.)",
   "context_delivery": {{
      "distribution": "does the user front-load context or reveal it incrementally? What types of context are introduced in later turns?",
      "trigger": "is incremental context revealed in response to agent questions or volunteered unprompted?"
   }}
}}
```

- Prompt for extracting user behavior representations along the *Communication Style* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. The user has a goal, and the assistant helps them achieve it. Your task is to describe the user's behavior according to the criteria below.

# User Goal
{user_goal}

# Conversation
{conversation_history}

# Analysis Criteria
1. Register and Tone
   - What is the user's register? (e.g., formal, casual, conversational, terse, professional)
   - What is the user's emotional tone? (e.g., neutral, frustrated, enthusiastic, impatient, apologetic, deferential)
   - Does the register/tone shift across the conversation? (e.g., starts polite but becomes curt after errors)

2. Verbosity and Structure
   - How verbose are the user's messages? Are they minimal and compressed, or expansive and elaborated?
   - Does the user use formatting conventions? (e.g., bullet points, numbered lists, code blocks, markdown, all caps, punctuation patterns)
   - How does message length and structure change across turns?

3. Social Conventions
   - Does the user use greetings, pleasantries, expressions of gratitude, or sign-offs?
   - Does the user treat the agent as a tool (purely transactional) or as a social interlocutor (rapport-building, politeness, humor)?

4. Request Framing
   - How does the user syntactically frame their requests? (e.g., imperative commands, questions, hedged suggestions, statements of problems without explicit asks)

# Instructions
- Generate terse, concise bullet points, not full sentences.
- Abstract away from the specific topic/domain.
- IMPORTANT: Do NOT use task-specific terms (e.g., "coding," "booking," "Python", "CSV"). Use generic substitutes (e.g., "executing a task," "providing constraints," "the target artifact").

Output a valid JSON object using the exact format below. Do not include any text outside the JSON.

{{
   "register_and_tone": {{
      "register": "what is the user's register? (formal, casual, conversational, terse, professional, etc.)",
      "emotional_tone": "what is the user's emotional tone? (neutral, frustrated, enthusiastic, impatient, apologetic, deferential, etc.)",
      "tone_shifts": "does the tone shift across the conversation, and in response to what?"
   }},
   "verbosity_and_structure": {{
      "verbosity": "how verbose are the user's messages? minimal and compressed, or expansive and elaborated?",
      "formatting": "does the user use formatting conventions? (bullet points, numbered lists, code blocks, markdown, etc.)",
      "evolution": "how does message length and structure change across turns?"
   }},
   "social_conventions": {{
      "politeness_markers": "does the user use greetings, pleasantries, gratitude, or sign-offs?",
      "agent_relationship": "does the user treat the agent as a tool (transactional) or as a social interlocutor (rapport-building, politeness, humor)?"
   }},
   "request_framing": "how does the user syntactically frame their requests? (imperative commands, questions, hedged suggestions, problem statements without explicit asks, etc.)"
}}
```

- Prompt for extracting user behavior representations along the *DAMSL Dialog Acts* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. Your task is to analyze a specific user utterance in a multi-turn conversation and provide a description of the user's behaviour.

# Conversation History
{conversation_history}

# Target Utterance
Read the conversation history for context, but your analysis MUST strictly apply ONLY to this utterance:
{target_user_utterance}


# Dialogue Act Markup in Several Layers (DAMSL) Annotation Framework
DAMSL defines utterances based on the intentions of the speaker. Each utterance is analyzed along several dimensions.
1. INFORMATION LEVEL: Characterizes the semantic content of the utterance:
    - **Task**: Directly advances (or attempts to advance) the goals of the domain task.
    - **Task-management**: Addresses the problem-solving process/procedure rather than performing the task itself.
    - **Communication-management**: Concerned exclusively with maintaining the communication channel.
2. FORWARD LOOKING FUNCTION: Characterizes what effect the utterance has on the subsequent dialog:
    - **Statement**: Makes a claim (Assert, Re-assert, Other-statement).
    - **Info-request**: Asks for information.
    - **Influencing-addressee-future-action**: Directly influences the addressee's future non-communicative actions, directs or suggests the addressee to perform an action.
    - **Committing-speaker-future-action**: Potentially commits the speaker to some future action.
    - **Conventional**: Conventional conversational actions such as greeting, farewells, thanking, or responding to thanks.
3. BACKWARD LOOKING FUNCTION: Characterizes how the current utterance relates to the previous discourse:
    - **Agreement**: Accept, reject, partial accept/reject, holds off a response.
    - **Answer**: Provides requested information.
    - **Understanding**: Signals comprehension (acknowledgement, repetition/reformulation, collaborative completion) or lack thereof.


# Output Instructions
Analyze the target utterance along DAMSL's dimensions and write a concise, 1 sentence description of the user's behaviour and its functional role in the target utterance:
- Generate terse, concise bullet points, not full sentences.
- Abstract away from the specific topic/domain
- IMPORTANT:Do NOT use task-specific terms (e.g., "coding," "booking," "Python", "CSV"). Use generic substitutes (e.g., "executing a task," "providing constraints," "the target artifact").

Output only the concise description as plain text, without any other text or formatting.
```

- Prompt for extracting user behavior representations along the *SGD Dialog Acts* facet.

```text
You are an expert analyzing user behaviour in human-AI conversations. Your task is to analyze a specific user utterance in a multi-turn conversation and classify the user's dialogue act(s).

# Conversation History
{conversation_history}

# Target Utterance
Read the conversation history for context, but your analysis MUST strictly apply ONLY to this utterance:
{target_user_utterance}


# Dialogue Act Taxonomy (adapted from Schema-Guided Dialogue)
Classify the target utterance using one or more of the following user dialogue acts:

1. INFORM: User provides information, states preferences, or supplies constraints to the agent.
2. REQUEST: User asks the agent for specific information or details.
3. AFFIRM: User agrees with, confirms, or accepts a proposition, value, or suggestion made by the agent.
4. NEGATE: User disagrees with, denies, or rejects a proposition, value, or suggestion made by the agent.
5. SELECT: User chooses between multiple options or alternatives presented by the agent.
6. INFORM_INTENT: User states, introduces, or shifts to a new goal or task objective.
7. AFFIRM_INTENT: User confirms or agrees with a goal or task objective suggested by the agent.
8. NEGATE_INTENT: User rejects or denies a goal or task objective suggested by the agent.
9. REQUEST_ALTS: User asks for different or additional options beyond what has been presented.
10. THANK: User expresses gratitude or appreciation.
11. GOODBYE: User signals the end of the conversation or a conversational closing.
12. GREET: User initiates the conversation with a greeting or opening.


# Output Instructions
- Assign ALL applicable dialogue acts to the target utterance (utterances may have multiple acts).

Output the dialogue acts, separated by commas, without any other text or formatting.
```

### User Goal Classification

- Prompt for classifying user goals.

```text
You are an expert classifier. Given a user intent, your task is to classify it into one category and one subcategory.

# User Intent
{user_intent}

## Categories and Subcategories

1. **Artifact Creation** - The user wants to produce a final artifact (code, writing, prompt, etc.).
    - Subcategories: Writing, Coding, Prompt Generation, Other
2. **Information Seeking** - The user wants to receive information about a topic.
    - Subcategories: Writing, Coding, Math, Science, Other
3. **Practical Guidance** - includes activities like tutoring and teaching, how-to advice about a variety of topics, and creative ideation (highly customized to the user and can be adapted based on conversation and follow-up)
    - Subcategories: Teaching, How-To Advice, Self-Care, Creative Ideation, Other
4. **Other** - The intent does not clearly fit any of the above categories.
    - Subcategories: Other

## Output Format

For each response, output a valid JSON object using the exact format below. Use double quotes ("), escape any double quotes within strings using backslashes (\"), escape newlines as \\n, and do not include any text before or after the JSON object.

{{
    "category": str, # One of: "Artifact Creation", "Information Seeking", "Practical Guidance", "Other"
    "subcategory": str # One of: "Writing", "Coding", "Prompt Generation", "Math", "Science", "Teaching", "How-To Advice", "Self-Care", "Creative Ideation", "Other"
}}
```
