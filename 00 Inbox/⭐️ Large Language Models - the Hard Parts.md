---
type: book
status: inbox
quality: 1
topics: []
source: private://read/01ksy3vmf2wwjkvesw5cwc9ysm
created: 2026-08-16
published: 2026-05-13
author: Thrsis T. P. Souza;Jonathan K. Regenstein Jr.;
flashcards: none
updated: 2026-08-16
---

# Large Language Models: The Hard Parts

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/460701139/HMsuDqO45oUMy6-QiPEqYLpO__BVBWVT46tmLTV_37k-cove_CsdZlaR.png" width="220" />
</div>


## Foreword

- I recommend thinking about this book as a guide to the complex areas beyond just getting an LLM up and running. In the first few chapters, you’ll learn the first principles of building with LLMs, methodologies for evaluating these nondeterministic models, real-world strategies for using RAG, and how to generate predictable, structured output.

## Preface


## Acknowledgments


## Chapter 1. First Principles: What to Consider Before We Start Building with LLMs

- 1. First Principles: What to Consider Before We Start Building with LLMs

## Strategic Considerations


### Enterprise Requirements

- Articulating enterprise requirements is the first step toward success with LLMBAs. We need a concrete description of what problem we’re solving and why it matters to our enterprise. Vague aspirations like “We want to use AI” or “Let’s improve efficiency” lack the specificity needed to guide implementation decisions or measure success.
- The “why” must connect directly to enterprise impact: either cost savings through efficiency gains or revenue generation through improved customer experience, faster time-to-market, or enhanced decision-making capabilities.
- Budget and return-on-investment (ROI) considerations are also critical for ensuring the long-term viability of LLMBAs.

### Performance Requirements

- determining the minimum level of accuracy that a model must achieve to be considered successful. This serves as a critical baseline for evaluating model performance and making deployment decisions.
- Establishing clear evaluation metrics, whether through automated measures or human evaluation processes, provides concrete ways to assess if these thresholds are being met. Continuous monitoring of these accuracy metrics ensures the system maintains its performance over time as usage patterns and data distributions evolve.

### Operational Requirements

- Organizations must carefully project their daily and monthly model call volumes while calculating the average number of tokens per request to accurately estimate resource needs. Understanding usage patterns, including seasonal variations, enables proper capacity planning.

## Organizational AI Frameworks


## Organizational AI Frameworks


### Centralized Framework


### Centralized Framework

- responsible for setting and implementing the overall strategy, policies, and standards, as well as monitoring compliance and ensuring quality.
- single core team manages AI development and deployment across the organization. This framework concentrates AI expertise, infrastructure, and decision-making authority in one place, typically under a chief AI officer or within a dedicated AI center of excellence (COE).
- this group is a multidisciplinary team
- For highly regulated industries such as financial institutions, this framework offers streamlined governance, consistent compliance, and clear accountability. It ensures uniform data standards and policies across the enterprise, reducing the risk of fragmented compliance and easing regulatory reporting.
- However, centralization can create bottlenecks as demand for AI solutions grows across business units, potentially slowing innovation and making the central team a constraint rather than an enabler.

### Decentralized Framework


### Decentralized Framework

- A decentralized framework grants complete freedom to individual business units or teams, with each team defining its own rules, selecting its own tools, and managing its own data. In a decentralized approach, AI development and deployment are initiated and managed by the individual lines of business themselves.
- maximizes speed and agility, as there are no bureaucratic hurdles or central approval processes slowing down experimentation.
- Without coordination, organizations experience multiple conflicting definitions for the same key metrics, rampant duplication of data, and inconsistent quality.
- This autonomy can lead to both creativity and AI-driven chaos. In practice, few large institutions operate purely decentralized AI programs precisely because regulatory requirements demand enterprise-wide visibility and control.

### Federated Framework


### Federated Framework

- hybrid approach combining centralized policy-setting with decentralized execution
- This operating framework fosters collaboration, reusability, and standardization while empowering lines of business to retain control over their AI solutions, promoting a balance between autonomy and governance.
- In practice, the centralized unit establishes enterprise-wide policies on model risk management, data governance, ethical AI principles, and security standards.
- Federated governance enables autonomous teams to function within a unified framework while maintaining their independence, ensuring coordinated management and enhancing consistency and accessibility across diverse systems.
- The central team is responsible for continually evolving the operating framework, refactoring and enhancing AI services to meet the changing needs of lines of business, and keeping up with rapid advancements. The federated approach strikes a balance, mitigating the risks of fully decentralized initiatives while minimizing bottlenecks from overly centralized approaches.

## Small Language Models


## Chapter 2. The Evals Gap

- 2. The Evals Gap

## Conclusion

- LLMs and LLMBAs introduce a realm of nondeterministic and generative behaviors that challenge conventional software engineering paradigms for evaluation.

## Nondeterministic Nature of LLMs


### Source of Nondeterminism

- The primary source of nondeterminism in LLM responses is sampling.

### 10-K LLMBA Temperature Tests

- As a rule of thumb, we can expect roughly 0.75 English words per token

## The Evals Challenge

- LLM evaluation differs from traditional software testing across several key dimensions:
- Capability assessment versus functional testing Traditional software testing validates specific functionality against predefined requirements. LLM evaluation must assess not necessarily just predefined behavior but also “emergent properties” like reasoning, creativity, and language understanding that extend beyond explicit programming.
- Metrics and measurement challenges While traditional software metrics can usually be precisely defined and measured, LLM evaluation often involves subjective qualities like “helpfulness” or “naturalness” that resist straightforward quantification. Even when we try to break these down into numeric scores, the underlying judgment often remains inherently human and context-dependent.
- Human evaluation requirements Traditional software testing automates most validation. LLM evaluation still demands significant human oversight[2](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch02.html#id456) to assess output quality, appropriateness, and potential biases through structured annotation and systematic review processes.

## Methodologies for Evaluation


## Methodologies for Evaluation

- Each approach has its strengths and weaknesses: quantitative metrics are often precise and reproducible but measure surface-level textual overlap rather than meaning, making them brittle for open-ended tasks where many valid responses exist. LLM-as-a-judge captures semantic richness and nuance that metrics simply cannot but introduces cost, latency, and the biases of the judge model itself into the evaluation pipeline.

### Quantitative Metrics

- Common quantitative metrics used for LLM evaluation work by comparing a generated response against one or more human-written or model-written reference answers, measuring the degree of textual overlap through techniques like n-gram matching.
- What makes these metrics particularly valuable is their simplicity and reliability: they are relatively fast and cheap to compute and are deterministic for a fixed implementation and preprocessing pipeline. Because they produce a single numerical score, they integrate cleanly into automated testing pipelines and continuous integration/continuous deployment (CI/CD) workflows, making it straightforward to track model performance over time and catch regressions.
- For tasks with well-defined correct answers, like machine translation, summarization, and question answering against a fixed knowledge base, they remain a robust and trusted tool in the evaluation toolkit.

### Evaluating Evaluators


### Evaluating Evaluators

- important to measure how good our judge models are at evaluating other models.
- the performance of the LLM evaluator can be measured by comparing its scores to either a golden dataset or human reference scores. Higher correlation values may indicate better performance of the LLM evaluator.

![](https://readwise.io/reader/pcei/gAAAAABqG7XNab9AX2HCsDWxNBZyVmRvmLo8wCFDoQqRPD3PIrLAZH1WVy5vfLSmvzogXsdCih8NrhsE27WuGheZ26jeDmUo5cXXC_Sb6GSlmXeLlxglhUg=/llmh_0205.png)

- In a *human-based* approach, we would need to recruit human evaluators who are experts in the target languages we are evaluating. Expert humans would provide scores for a set of samples of the input LLM. We would then calculate the correlation between these scores against those generated by the LLM evaluator. The higher the correlation, the better the LLM evaluator.
- This is the primary way to validate whether an LLM judge is reliable—by comparing its judgments to what human evaluators would decide.
- An alternative to our diagram and the GLIDER approach is to use humans to compare different judge LLMs.

![](https://readwise.io/reader/pcei/gAAAAABqG7XN2twhRq7WPwvb20NmK_85uAaSymr0BYxlB2NZcNhO2ifYg0rhaq3ZoQmAi4AOX8XNxkzxdwL-w-l1oHmv11gGSzZ2VkAfSqKaPXkPojK6zzQ=/llmh_0206.png)

- Judge Arena operates as a crowdsourced benchmarking platform for comparing LLM judges through head-to-head competition.
- Various LLM judge models (like GPT-4, Claude, or specialized judge models) evaluate the same set of outputs.
- Each judge provides its evaluation, typically including scores, reasoning, and specific feedback on criteria
- These evaluations are then presented to human evaluators in a pairwise comparison format.
- human evaluators see two anonymous judge evaluations side by side
- After collecting many human votes across different judges and different types of content, Judge Arena calculates Elo ratings
- Judges that consistently produce evaluations humans find more accurate or insightful rise in the rankings.

## Conclusion


## Chapter 3. Evaluation Tools for LLM-Based Applications

- 3. Evaluation Tools for LLM-Based Applications

## LangSmith


### Scaling LLM-as-a-Judge with LangSmith

- [Promptfoo](https://oreil.ly/qp5Cb) is a lightweight open source framework primarily focused on prompt testing and comparison.[1](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch03.html#id620) It is designed specifically for prompt engineering workflows, allowing developers to quickly test multiple prompts against test cases to identify which variations perform best.

## Promptfoo

- Some of Promptfoo’s most useful features are: Automated testing Promptfoo provides automated testing capabilities, allowing developers to run custom evaluations tailored to their applications. Custom probes Developers can create custom probes to focus on specific use cases—for instance, decoupling prompts from test cases. User-friendly command-line interface (CLI) The framework features a CLI that supports live reloads and caching, facilitating rapid testing and iteration.

## Conclusion


## Chapter 4. From Data to Context

- 4. From Data to Context
- While advances in long-context language models have expanded the amount of information LLMs can process (as we will discuss later in this chapter), significant challenges remain in managing and effectively utilizing extended data inputs:
    - LLMs are sensitive to input formatting and structure, requiring careful data preparation to achieve optimal results.[1](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch04.html#id686)
    - LLMs operate with knowledge cutoffs, providing potentially outdated information that may not reflect current reality and demonstrate problems with temporal knowledge accuracy. [2](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch04.html#id687)
    - LLMs also exhibit a “lost-in-the-middle” effect,[3](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch04.html#id688) where information placed in the middle of long contexts is often ignored, and they struggle to recall less common but important facts, reflecting a systematic weakness in long-tail knowledge.[4](private://read/01ksy3vmf2wwjkvesw5cwc9ysm/ch04.html#id689)

## Conclusion


## Chapter 5. Structured Data Output

- 5. Structured Data Output
- While LLMs excel at generating text, getting structured output that adheres to strict rules, like a binary “yes” or “no” or consistent JSON, remains difficult. The core problem stems from the way LLMs produce output token by token, with each token sampled from a probability distribution across a model’s entire vocabulary.
- Even if a model follows JSON formatting instructions with 99% reliability per token, this small chance of error compounds across all tokens in a response.
- This reliability issue becomes problematic when integrating LLMs into production applications. This has driven the development of constrained generation techniques (CGTs) that can guarantee structurally valid output.
- CGTs solve this problem by changing where control is applied. Instead of prompting an LLM as part of the query, which is akin to giving stern instructions, CGTs intervene in the token sampling process itself. The mechanism works by first allowing the model to compute probability scores for all tokens in its vocabulary—typically around 50,000 options, depending on the tokenizer—then constraining which tokens would be valid.
- A parsing state represents the system’s understanding of where it currently stands within the output being generated.
- In this state, tokens such as (1) quotation marks to start a string value, (2) digits to begin a number, or (3) opening braces for nested objects would be considered valid. However, tokens such as (1) additional colons, (2) closing braces without a value, or (3) unquoted text would violate JSON syntax rules and therefore be invalid.
- CGTs maintain this contextual awareness through finite-state machines (FSMs) that track the grammatical position within the target structure. Each generated token transitions the system to a new state with its own set of valid next tokens.
- Any tokens that would violate the desired structure get masked by setting their probability to negative infinity, making them impossible to sample. Finally, the model samples from only the remaining valid tokens.
- As a result, syntactically malformed output for the specified grammar cannot be generated, while the model’s reasoning capabilities are preserved. The model still “wants” to produce reasonable content, but its options are constrained to only those that maintain structural validity.

## Why Structured Output Matters


## Why Structured Output Matters


### Improving Developer Efficiency and Workflow

- Reliable structured outputs can make this more efficient by reducing trial and error in prompt engineering.
- LLM structured output simplifies this, reducing the need for ad hoc postprocessing code.
- LLM output constraints make this process more efficient and predictable.
- Output constraints are crucial to ensure compatibility and prevent errors.
- Finally, LLMs are increasingly used to generate synthetic data for model training. Constraints can ensure data integrity and prevent the inclusion of unwanted elements that could negatively impact training outcomes.

### Meeting UI and Product Requirements

- LLM-generated content often needs to fit into specific UI elements with size restrictions

### Enhancing User Trust and Experience

- Users expect LLM-powered tools to be reliable and truthful, and that means removing hallucinations.

## Training-Time Constraint Techniques


## Training-Time Constraint Techniques

- Training-time constraint techniques (TTTs) are applied during model training, in either the pretraining or posttraining phase, to guide the model to internalize the patterns and structures required for a specific task.
- When applying a TTT, an LLM is trained on datasets specifically designed to teach the desired output structure. Because this information is incorporated into the LLM’s weights, the model learns to natively produce outputs that follow the target format.
- During SFT, model builders create a training dataset where every example shows the model an input prompt and the corresponding correct output in the target format. For JSON generation, we’d have thousands of examples where the prompt says, “Extract the risk factors from this 10-K section,” and the expected output is valid JSON with a specific schema like `{"risk_factors": [{"category": "market", "description": "…", "severity": "high"}]}`. The model sees these input-output pairs repeatedly during training and learns the statistical patterns of JSON structure—opening braces, key-value pairs, proper nesting, closing braces, and quotation marks around strings.

## Inference-Time Constraint Techniques


## Inference-Time Constraint Techniques

- applied during the inference phase of the LLM’s operation.
- done by LLM users like us, through prompt engineering or logit postprocessing.

### Combining JSON Mode with Pydantic


### Combining JSON Mode with Pydantic

- Pydantic is a Python library for data validation and parsing that enforces type annotations at runtime, ensuring the data matches the structure and types we define in our models.

### Logit Postprocessing

- logit postprocessing offers an even greater level of control by directly manipulating the model’s token probabilities before any text is generated.
- Logit postprocessing intervenes at each generation step to mathematically zero out the probability of any token that would create invalid output—essentially making it impossible for the model to produce malformed structures.
- Where Pydantic validates after generation and may need retries, logit postprocessing prevents invalid outputs from ever being generated in the first place by acting as a real-time filter on the model’s vocabulary at every single token decision.

![](https://readwise.io/reader/pcei/gAAAAABqG7XORQcD7cjSaTM0wlhIZiigV3GglwxBzBT9QfIjU3bf5FwRMiGc-zqT4JZ1XXKdPv1M_dZs14QwvG9Y544opke7B3560veD84tpQbcQreKMg2Y=/llmh_0502.png)


## Conclusion


## Chapter 6. LLM Safety Considerations

