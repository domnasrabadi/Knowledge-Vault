---
type: article
status: raw
quality: 1
topics: [ai-agents, agent-evaluation, mlops]
source: ""
created: 2025-12-08
published:
author: Melissa Z. Pan; Negar Arabzadeh; Riccardo Cogo; Yuxuan Zhu; Alexander Xiong; Lakshya A Agrawal; Huanzhi Mao; Emma Shen; Sid Pallerla; Liana Patel; Shu Liu; Tianneng Shi; Xiaoyuan Liu; Jared Quincy Davis; Emmanuele Lacavalla; Alessandro Basile; Shu...
flashcards: none
updated: 2026-01-01
---

# Measuring Agents in Production

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/static/images/article3.5c705a01b476.png" width="220" />
</div>

Source: https://readwise.io/reader/document_raw_content/395324356

Exported at: `2025-12-29T04:27:38Z`

- AI agents are already operating in production across many industries, yet there is limited public understanding of the technical strategies that make deployments successful.
- We investigate why organizations build agents, how they build them, how they evaluate them, and what the top development challenges are.
- We find that production agents are typically built using simple, controllable approaches: 68% execute at most 10 steps before requiring human intervention, 70% rely on prompting offthe-shelf models instead of weight tuning, and 74% depend primarily on human evaluation.
- Unfortunately, little information is publicly available on how production agents are built. Why do some agents succeed while others fail? What requirements must agents meet for production deployment? We lack a systematic understanding of what methods enable successful agents in the real world. Researchers have little visibility into real-world constraints and practices. Are agents failing because models are not capable enough, or are there other factors at play?
- We study the practices of developers and teams behind successful real-world systems via four research questions (RQs): • RQ *1.* What are the applications, users, and requirements of agents? • RQ *2.* What models, architectures, and techniques are used to build deployed agents? • RQ *3.* How are agents evaluated for deployment? • RQ *4.* What are the top challenges in building deployed agents?
- Our study reveals key findings for each research question:
- RQ *1* : Productivity gains drive agent adoption. We find that 73% of practitioners deploy agents primarily to increase efficiency and decrease time spent on manual tasks
- RQ *2* : Simple methods and workflows dominate. 70% of interview cases use off-the-shelf models without weight tuning (Figure 6), relying instead on prompting. Teams predominantly select the most capable, expensive frontier models available, as the cost and latency remain favorable compared to human baselines.
- Production agents favor well-scoped, static work
- 68% execute at most ten steps before requiring human intervention, with 47% executing fewer than five steps.
- Furthermore, 85% of detailed case studies forgo third-party agent frameworks, opting instead to build custom agent application from scratch. Organizations deliberately constrain agent autonomy to maintain reliability.
- RQ *3* : Human verification remains central to evaluation. The majority of deployed survey agents (74%) rely primarily on human-in-the-loop evaluation, and 52% use LLM-as-a-judge
- Notably, every interviewed team utilizing LLM-as-a-judge also employs human verification.
- RQ *4* : Reliability is an unsolved challenge. Practitioners focus most on ensuring agent reliability, spanning correctness, latency, and security.
- Organizations adopt agents to solve immediate operational problems, such as expert-expensive manual work and insufficient staffing capacity. Productivity gains are straightforward to quantify through human-hour reductions, whereas safety improvements and risk mitigation are harder to verify.
- The top reported reasons for using agents reveal a trend where certain objectives are more verifiable and measurable. For example, time to complete a task (productivity) is concrete and quantifiable, while risk mitigation benefits takes longer to verify.
- internal employees are the primary user base (52.2%), followed by external customers (40.3%). Only 7.5% of deployed systems serve non-human consumers.
- The focus on internal users is a deliberate deployment choice. Detailed case studies reveal that organizations restrict deployments to internal environments to mitigate unsolved reliability and security concerns. Internal users operate within organizational boundaries where agent mistakes have lower consequences and human oversight is readily available.
- This reflects a pattern where agents function as tools that *augment* domain experts rather than replace them. This paradigm also enables human users to serve as the final verifiers of agent outputs

![](https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/395324356/t44tx-iIxcr_Cz0BBA-nCWVvBXutcC2nBO_BCAfuJcA-_pa_daK0NCp.jpeg)

- Beyond user type, we examine the scale of the user base. We find that end-user counts for deployed systems vary significantly. As shown in Figure 4c, 42.9% of deployments serve user bases in the hundreds. However, we also observe high-traffic deployments (25.7%) serving tens of thousands to over 1 million users daily, representing substantial user impact or possibly mature systems.
- Having established *what* problems practitioners target with agentic systems, we now address *how* these systems are built. We examine five critical implementation decisions: model selection, model weights tuning, prompt construction, agent architectures, and development frameworks.
- Overall, practitioners favor established, straightforward methods over stochastic or training-intensive techniques.
- Instead, teams prioritize control, maintainability, and iteration speed.
- We find that deployed agents rely heavily on proprietary models.
- We find that open-source adoption is rare and is driven by specific constraints rather than general preference. Among the three cases using open-source models, motivations include high-volume workloads where inference costs at scale are prohibitive, and regulatory requirements preventing data sharing with external providers.
- Number of Distinct Models. While a substantial portion rely on a single model, the majority coordinate multiple models to meet functional or operational needs. Survey results show that 40.9% of deployed agents use exactly one model, while 27.3% use two, 18.2% use three, and 13.6% use four or more. Among detailed case studies, 10 out of 20 (50%) combine models to address specific *functional needs*
- We identify two drivers: cost optimization and modality. First, teams combine models of varying sizes to balance latency, cost, and quality. For example, one agent workflow from case study routes simple subtasks like pattern recognition to smaller models while reserving larger models for subtasks requiring higher reasoning capabilities. Second, teams integrate models to handle distinct data modalities.
- We observe a strong preference for prompting over model weight updates in deployed agents.
- Only 5 of 20 detailed case studies actively use SFT. These teams target deployment in business-specific corporate contexts where leveraging highly contextual information improves downstream performance.

![](https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/395324356/--RUTPzS2CuBURRUJOTf_F0k51UjnK9ooKJcIevEh44-_pa_ea2DOQL.jpeg)

- RQ *2 Finding #3:* Practitioners rarely post-train models. When they do, they selectively apply SFT/RL to specific subtasks or clients, typically in combination with general LLMs. Teams find prompt engineering with frontier models sufficient for *many* target use-cases already.
- We find that humans dominate system-prompt construction in production systems. Our survey data reveals that 33.9% of deployed agents use *fully manual* methods with hardcoded strings. Another 44.6% use a hybrid approach where humans manually draft prompts and then use an LLM to augment or refine them, and 3.6% rely on utilizing predefined prompt templates. Only 8.9% of respondents use a prompt optimizer (e.g., DSPy [77]) to improve their agent systems, and just 3.6% report letting agents autonomously generate their own prompts.
- RQ *2 Finding #5:* Deployment prompt lengths vary widely: while half are short (<500 tokens), a significant long tail (12%) exceeds 10,000 tokens to handle complex contexts.
- Number of Steps. We find that production agents tend to follow *structured workflows* with bounded autonomy.
- Practical constraints drive this design choice. Case study participants identify problem complexity, non-determinism in agent self-planning, and latency requirements as key limiting factors. Practitioners intentionally impose limits on reasoning steps to maintain reliability and manage computational time and costs.
- Number of Model Calls. While distinct from logical steps (which often include non-inference actions like tool execution), we specifically analyze *model calls* to gauge the inference intensity of deployment systems. We observe that within a single subtask, deployment systems typically execute model calls on the order of tens or less. The majority (66.7%) of deployed survey agents use fewer than 10 calls per subtask, with 46.7% using fewer than 5 calls. This is followed by 33.3% using tens of calls, 9.0% in the hundreds, and 6.1% in the thousands.
- Despite the pattern of limited model calls, 31% of deployed survey agents already use various inference-time scaling techniques, compared to 44% in experimental sys- tems. While this figure currently includes simpler methods like composing outputs from multiple models
- RQ *2 Finding #6:* Agents operate with tightly bounded autonomy: 68% of systems execute fewer than ten steps and 46.7% with less than 5 model calls before requiring human intervention.
- Agent Control Flow. We observe that production agents favor predefined static workflows over full open-ended autonomy. We find that 80% of our detailed case studies utilize a structured control flow. These agents operate within well-scoped action spaces rather than freely exploring the environment to self-determine objectives.
- RQ *2 Finding #8:* Framework adoption varies significantly between survey and case study. While third-party frameworks get broad adoption in the survey (61%), interviewed teams predominantly build custom in-house implementations (85%) to maximize control and minimize dependency bloat.
- RQ *3 Results:* How Are Agents Evaluated For Deployment?
- Specifically, we examine two aspects: what practitioners compare their systems against (baselines and benchmarks), and what methods they use to verify system outputs (evaluation methods).
- During development, teams conduct offline evaluation to assess agent performance before deployment. Figure 10a shows that 38.7% of survey respondents compare their deployed agentic systems against non-agentic baselines such as existing software systems, traditional approaches, or human execution.
- RQ *3 Finding #1:* Many agentic systems lack standardized benchmarks or baselines. Teams build custom evaluation frameworks from scratch, often creating ground truth data for the first time.
- Evaluation Methods
- Four methods dominate responses: human-in-the-loop evaluation, model-based evaluation, rule-based evaluation (heuristics or syntactic checks), and cross-referencing evaluation (verification against knowledge bases or reference datasets).
- Human-in-the-loop verification. The majority (74.2%) rely on manual, human-in-the-loop evaluation
- These evaluations typically involve domain experts, operators, or end-users directly inspecting, testing, or validating system outputs to ensure correctness, safety, and reliability.
- Human experts play a critical role during development for offline evaluations. Agent developers work directly with domain experts or target users to validate system responses.
- Human experts also serve as verifiers during agent execution for online evaluation. Teams commonly have human experts perform final actions based on agent output, serving as a layer of guardrails.
- Model-based evaluation. Model-based evaluation methods such as LLM-as-a-judge are the second most common approach, used by 51.6% of respondents
- Model-based evaluation does not eliminate human involvement.
- co-occurrence of different evaluation strategies, revealing that among the 51.6% of survey respondents who use model-based evaluation, a substantial portion (38.7%) also employ Human-in-the-Loop verification. In detailed case studies, all interviewed teams using LLM-as-a-judge combine it with human review. Specifically, these teams use LLM judges to evaluate confidence in every final response, combined with human subsampling.
- Additionally, human experts sample a preset percentage (e.g., 5%) of production runs even when the LLM judge expresses high confidence, verifying correctness to ensure consistent alignment at runtime.
- Other methods. Rule-based evaluation methods and cross-referencing strategies show comparable adoption rates (41.9% and 38.7% respectively). Rule-based evaluation consists of simple logic checks such as grammar and syntax verification or domain-specific rules.
- Cross-referencing evaluation uses external sources for grounding and fact-checking to verify the accuracy and quality of generated answers or solutions. This includes retrieving supporting evidence from trusted knowledge bases or comparing outputs against reference datasets.
- Evaluation method patterns. Co-occurrence analysis reveals that human-in-the-loop evaluation is the most common method used together with other evaluation strategies (Figure 10c). Practitioners anchor automated, rule-based, and cross-referencing methods around human judgment rather than relying on them in isolation.
- RQ *3 Finding #2:* Human judgment dominates evaluation (74.2%). LLM-as-a-judge emerges as a complementary automated approach (51.6%), typically combined with human verification.
- RQ *4 Results:* What Are The Top Challenges In Building Production Agents?
- Our survey and detailed case studies reveal that *reliability remains the primary bottleneck.*
- RQ *4 Finding #1:* Reliability remains unsolved. It represent the top development focus for agents in all stages including ones in deployment.
- Agent behavior breaks traditional software testing. Three case study teams report attempting but struggling to integrate agents into existing CI/CD pipelines. The challenge stems from agent nondeterminism and the difficulty of judging outputs programmatically. Despite having various forms of existing regression tests from baseline systems, these teams have not yet identified effective methods to adapt them for nondeterministic agent behavior to create test set that cover sufficient runtime scenarios with different nuances.
- many agents operate in settings without robust and fast verification. For example, insurance agents receive true signals only through real consequences such as financial losses or delayed patient approvals. These signals arrive slowly and in forms difficult to automate for evaluation. Second, the final benefits of using agents are not always easy to measure.
- This raises a critical question: how do agents reach production if reliability remains an unsolved challenge? We observe that practitioners ensure reliability via deploying agents with strict constraints on both execution environments and agent autonomy, often combined with close human supervision.
- Our in-depth case studies reveals several deployment environment patterns.
- Some agents operate in read-only mode, never modifying production state directly.
- Other agents serve internal users where errors carry lower consequences and human experts remain readily available to correct mistakes
- Some teams combine read-only access with sandboxes mirroring production environments to further mitigate risk.
- This data pattern demonstrates that practitioners enable substantial deployment by leveraging existing model capabilities within well-scoped applications rather than waiting for model improvements.
- Beyond the directions we highlight in prior sections, we identify additional research questions based on deployment patterns in RQ1–4.
- We analyze data from agent practitioners across 26 domains to answer four research questions regarding the state of realworld agent development: • RQ1: Why build agents? Productivity drives adoption. Organizations deploy agents primarily to automate routine tasks and reduce human task hours, prioritizing measurable efficiency gains over novel capabilities. • RQ2: How are agents built? Simplicity and controllability dominate. Production systems favor closed-source models utilizing manual prompting rather than weight tuning. Architecturally, these systems rely on structured workflows with bounded autonomy and typically execute limited steps before human intervention. • RQ3: How are agents evaluated? Human verification remains the primary method. Practitioners rely heavily on human-in-the-loop evaluation because clean baselines and ground truth datasets are scarce. Automated techniques like LLM-as-a-judge complement human review rather than replace it. • RQ4: What are the challenges? Reliability represents the central development focus. The difficulty of ensuring correctness and evaluating non-deterministic agent outputs drives this friction. Latency and security typically act as manageable constraints rather than hard blockers as engineering workarounds and restricted environments currently manage them.

### D.1. Interview Outline

- • 1. The root problem (benefit) the system is addressing (providing): What is the ultimate benefit? What is the system replacing and why? • 2. Key success metrics and evaluation mechanism: What tools, techniques, systems, etc. are used to ensure the system meets user and stakeholder objectives? Is data corresponding to the expected or past system behavior available for the evaluation? • 3. Key aspects of the system design and implementation: What programming framework was used? What is the general architecture? What are the steps, stages, and cycles? How are common components (e.g. routers, LLM-as-a-Judge, other verifiers, HIL) combined and why? What is the ratio of automation to human interaction and why—by design or limitation?
- • 4. The state of the system or its development: Is the system in production, or was it never meant for production (purely for AI research, learning, upskilling)? Was the system prototyped for production but abandoned—why, and what were the critical limitations? Were there surprises in the development or evaluation process? Did some things work better or worse than expected, and if so, what? • 5. Known constraints or requirements of end-users and stakeholders: What are the security, confidentiality, regulatory, latency, SLO/SLA, or other requirements? • 6. Advantage of an agentic AI system solution over alternative approaches: Do reasonable alternative solutions exist for this problem, or is this a novel solution made possible with Agentic AI? Against existing alternatives, has comparative analysis been conducted? What are the comparative benefits, costs, and return on investment (ROI)? • 7. System dependencies and complexity: what is the quantity, quality, and availability of tools and data for verification and generation? • 8. End-user quantity, expertise levels, and organizational domains. is it a product for internal-use only or public external use? Does it support multiple institutions? Are there institution-specific or regulatory boundaries limiting the quantity of users? Are target users domain experts or novices? How many of each user group are there and how many are targeted (order of magnitude)?... • 9. Estimated cost versus value or benefit: What is the estimated cost (sunk and expected ongoing costs) of developing and operating the system versus the estimated value or benefit? Is the respondent aware? What is the value, how is ROI being calculated? • 10. System stakeholders: Who ultimately benefits from deployment? Who is impacted by safety, security, etc. failures and limitations? What is the expected impact on the company/institution (e.g. reduced hiring, retraining, broader user-base etc.)? • 11. Your role and activities: What is your role in the development of the agentic AI system(s) you are describing?
