---
type: paper
status: raw
quality: 3
topics: [llm-evaluation, ai-product, error-analysis, ai-engineering, agent-evaluation, model-risk-validation]
source: https://arxiv.org/abs/2604.16304v1
created: 2026-08-17
published: 2026-01-25
author: Willem van der Maden, Malak Sadek, Ziang Xiao, Aske Mottelson, Q. Vera Liao, Jichen Zhu
flashcards: none
updated: 2026-08-18
---

# How Practitioners Evaluate LLM Products in the Wild

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article2.74d541386bbf.png" width="220" />
</div>


### Abstract

- Through interviews with nineteen practitioners across diverse sectors, we identify ten evaluation practices spanning informal 'vibe checks' to organizational meta-work.
- Beyond confirming four documented challenges, we introduce a novel fifth we call the results-actionability gap, in which practitioners gather evaluation data but cannot translate findings into concrete improvements.
- we contribute strategies to bridge this gap, supporting practitioners' formalization journey from ad-hoc interpretive practices (e.g., vibe checks) toward systematic evaluation.

### Introduction

- we investigate:
    - What are the current evaluation practices for LLM-based products in production settings?
    - What do practitioners describe as their main challenges in evaluating LLM-based products?
- predominantly work with foundation models accessed through APIs rather than training their own models (outside of some experiments with finetuning small local models), building applications that must serve real users with specific needs.
- As such, they evaluate complete systems including user interfaces, retrieval mechanisms, and prompt designs rather than isolated model capabilities.
- these practitioners must assess context-specific, often hard-to-define qualities while navigating production constraints of limited resources, tight deadlines, and diverse stakeholder demands.

### Background and Related Work

#### What do we mean by 'evaluation'?

- Our research takes a sociotechnical position and defines LLM evaluation as the process through which teams assess LLM-based systems' fitness for their products' intended goals—a task of determining whether technology satisfies human needs in deployment contexts
- spans intrinsic approaches (evaluating outputs directly) and extrinsic approaches (measuring effects on task performance) (Gehrmann et al, 2023), from early formative assessments through post-deployment monitoring.

#### Defining 'constructs,' 'measurements,' 'metrics,' and 'criteria'

- **Constructs** define what goals or aspects of LLM-based systems warrant assessment.
    - from technical properties (e.g., retrieval accuracy) to experiential qualities (e.g., usefulness in emergency contexts) to systemic outcomes (e.g., fairness across demographics).
- **Measurements** operationalize these constructs, transforming abstractions into observable data through specific instruments, for instance, automated scoring algorithms, behavioral data, user ratings, or expert assessments
    - For instance, 'helpfulness' might be operationalized through task completion rates, satisfaction scores, or quality ratings, each capturing different facets while potentially missing others.
- **Metrics** are specific quantifiable measurements that produce numerical outputs.
    - For instance, $F_1$-score is a metric (a mathematical function), while expert judgment is a measurement but not a metric.
- **Criteria** establish performance standards or thresholds, determining what counts as 'good' on a given construct.
    - While accuracy is a construct and $F_1$-score is one measurement, requiring "$F_1 > 0.95$" establishes a criterion.

### Findings

- we present our findings of RQ1 in the form of ten main evaluation activities, spanning how practitioners execute evaluations [A1-A4], design their approaches [A5-A7], and navigate organizational meta-work [A8-A10].
    - how practitioners execute evaluations
        - Vibe checks (A1)
        - User feedback (A2)
        - Expert evaluation (A3)
        - Automated evaluation (A4)
    - how they design their approaches
        - Construct extraction (A5)
        - Metric selection (A6)
        - Systematizing ad-hoc toolkits (A7)
    - how they navigate organizational meta-work
        - Alignment work (A8)
        - Documentation and sharing practices (A9)
        - Advocating for evaluation (A10)

#### Why Practitioners Evaluate

- Teams evaluate to understand the capabilities of the specific foundational models their products are built on —e.g., what models "can do, what [they] cannot do," as one practitioner put it.
- And they use these insights to guide technical decisions, make business cases, and manage risks.
- At the technical level, evaluation enables iterative refinement:
    - adjusting prompts based on feedback (two practitioners)
    - comparing whether "magic happens"—i.e., big jumps in capability improvement—when switching between models (one practitioner)
    - informing "trade offs of different training [approaches] or changes in the model architecture"
- This unpredictability means evaluation is used as both quality assurance—ensuring "the right file has been referenced" (one practitioner)—and risk management, preventing systems from "blow[ing] in your face" when pushed beyond simple cases (another practitioner).
- As one practitioner summarized, "the right evaluation strategy has to be proportional to what is at stake"

#### What are the Current Evaluation Practices for LLM-based Products in Production Settings? (RQ1)

- Ten evaluation activities emerged from our data. Below, we organize them into three categories, ordered from actual evaluation to its methodological design and organizational meta-work. They include:
    1. how the participants evaluate LLMs [A1-A4]
    2. how they design these evaluations [A5-A7]
    3. what organizational meta-work the participants engage around evaluation [A8-A10]
- These span from initial 'vibe checks' that provide rapid, intuitive assessment [A1], to continuous user feedback collection [A2], ongoing collaboration with domain experts [A3], and attempts at automated testing from existing paradigms [A4].
- **Vibe checks [A1].** Twelve participants described beginning their evaluation with informal "vibe checks." These are formative and exploratory assessments that serve as an essential first line of evaluation.
    - These initial evaluations are intuitive and variable, with participants struggling to articulate their activities exactly.
    - "At the end of the day, we could say that it's based on vibes, but the way of getting to the vibes is very structured and very logically oriented in a spreadsheet. So I had a gigantic spreadsheet where I basically was running the same kind of a prompt [for different characters]. I would see: does that feel right? If I say this out loud, does it sound like a real person speaking? Does it sound like this character that I can hear in my head? [...] I would like test each of those and then like give them a mark. I think is that mark out of ten and then kind of see at the end like [which prompt] is doing best."
    - "It's more like to sort of scope what I should be looking for in the responses when I do the initial vibe checking with a model. I would do some manual prompting to get a feel for how we might generate relevant output for the specific use case. Then I will go back and generate even more samples, but in a more structured manner with different settings and different models [...] where I just specify a bunch of different prompts, some different system prompts, some different parameters for temperature and top[2](https://arxiv.org/abs/2604.16304v1/#fn2) and whatnot. And then that will output an Excel sheet with a bunch of different responses [...] that will be what we finally asked the users to rate."
- **User feedback [A2].**
    - Common mechanisms include in-app "thumbs up, thumbs down" (two practitioners) and star ratings (one practitioner)
    - we find these qualitative approaches reveal something binary signals cannot: misalignments between developer and user expectations.
- **Expert evaluation [A3]** in LLM development is characterized by continuous, collaborative engagement throughout the development lifecycle.
    - teams turn domain experts into a sort of *living benchmarks*—human reference points they repeatedly consult to gauge whether the system is improving or going awry.
    - This engagement often begins with "gut feeling" checks to assess project viability (one practitioner) and evolves alongside the product.
- **Automated evaluation [A4]**, the last main evaluation activity, also takes several forms in practice, though none has achieved the reliability practitioners seek.
    - none reported running comprehensive benchmark suites like MMLU or SuperGLUE for production evaluation
    - More recently, some teams have adopted LLM-as-judge approaches.
        - Three participants actively used LLMs to evaluate their products—for instance, checking whether chatbot answers were "grounded in the retrieved information" (one of them) or scoring outputs for "truthfulness and completeness" (another).
        - Others considered but rejected these approaches, with one practitioner viewing LLM-as-judge as an untraceable "black box."
- **Summary of evaluation types** A1–A4 reveal a notable pattern: while practitioners aspire to automated, scalable evaluation [A4], they currently rely heavily on human judgment—whether through developer/designer intuition [A1], user feedback [A2], or expert assessment [A3].

##### Evaluation Design Activities

- Beyond execution, practitioners must design their evaluation approaches—deciding what to measure and how.
- This involves extracting testable constructs from qualitative observations [A5], selecting measurements that balance rigor with practical constraints [A6], and attempting to codify ad-hoc methods into reusable frameworks [A7].
- **Construct extraction [A5].** Fourteen participants described determining what to evaluate through thematic refinement of qualitative data.
    - we find teams actively work to disentangle them through construct operationalization.
    - For example, "appropriate" becomes "appropriate tone and persona for context" (one practitioner), "useful" becomes "saves money or improves quality" (another), "engaging" becomes "storyline quality and interaction effectiveness" (a third).
    - Teams derive these constructs from multiple sources: user feedback sessions, developer observations, stakeholder discussions, and domain expert input.
    - "we need to be on the same page when we evaluate something. What is it that we're evaluating?"
    - One practitioner elaborated that LLM-based evaluation works best when it "gives examples of how it's strong or weak in that area" rather than numerical scores—"what you're really looking for is where was the specific experience that was subpar and what made it subpar."
- **Metric selection [A6].** Once teams know *what* to evaluate, they must decide *how* measure it.
    - Our participants responded differently to this uncertainty: rather than adding more metrics, they selected fewer based on actionability.
    - To make these selections, teams blend multiple influences: adapting measurements from prior non-LLM systems (one practitioner), consulting external sources (two practitioners), or inventing "what would be the most valid criteria" for their specific context (another practitioner).
- **Systematizing ad-hoc toolkits [A7].** Eleven participants described attempts to codify their evaluation approaches into reusable infrastructure, moving from informal "trial and error" methods (one practitioner) and individual vibe checks toward structured, repeatable approaches.
    - "I personally really like system theoretic process analysis. You basically identify the things you don't want to happen, then you create a set of hazards. Those constraints become your requirements, which become the specific requirements for the product. [...] Creating tests and a requirement matrix so that every test aligns to a set of requirements. [...] If the test fails, you know which requirement did not function, and you can immediately intervene." — a practitioner
    - Participants pursued systematization for several reasons: avoiding the inefficiency of "reinvent[ing] the wheel" (one practitioner) and escaping the cost of remaining reactive.
    - Timing also proved critical. One practitioner stated: "you have to have the [evaluation] tooling in place before you start creating the functionality. Then you get the benefit of the tooling all the way."
    - We refer to this progression from ad-hoc practices toward systematic evaluation as a *formalization journey*, a concept we return to in the discussion.
- **Summary of evaluation design practices [A5–A7]** These activities reveal practitioners caught between pragmatic necessity and systematic aspiration.
    - They transform intuitive quality judgments into measurable constructs, select measurements for stakeholder communication over technical rigor, and attempt to codify these discoveries into reusable frameworks

##### The 'Meta' Activities That Shape Evaluation

- The design and execution of evaluations does not happen in isolation and is shaped by forces at the organizational level.
- **Alignment work [A8].** Thirteen participants described disambiguation sessions and collaborative workshops (formal or informal) where teams surface different perspectives and negotiate shared evaluation constructs
    - Without alignment, teams risk measuring different things and ending up with in-actionable results
- **Documentation and sharing practices [A9]**
    - forms varied:
        - One practitioner's team developed "AI performance metrics cards" standardizing definitions across products
        - Another built ground-truth datasets with "guidelines for evaluators as to how you would rate"
        - A third designed a human feedback system explicitly as "a blueprint... that could also be transferable across teams"
        - And a fourth maintains "prompt chains" in a Google doc
- **Advocating for evaluation [A10]** emerged as essential organizational work. Ten participants described extensively advocating to secure resources and legitimacy for evaluation activities.
    - One practitioner framed the work as "95% communication... people who can communicate well are the ones who win at the end of the day."
- **Summary of evaluation meta-work [A8–A10]** These activities reveal that evaluation extends far beyond technical measurement to encompass essential organizational work.

#### What do Practitioners Describe as Their Main Challenges in Evaluating LLM-based Products? (RQ2)

- Throughout the range of evaluation activities (A1–A10), our participants consistently encounter challenges that complicate or undermine their efforts. Many of these challenges have been documented before: aligning stakeholders, establishing constructs, choosing methods, and overcoming technical barriers all appear in prior work
- the "results-actionability gap" [C5], where teams gather evaluation data but cannot translate findings into concrete improvements.

##### Documented challenges: why designing and executing evaluations remains hard

- **Aligning on evaluation objectives [C1]** emerged as a major struggle for ten participants.
    - These groups struggle to translate between their framings: a technical improvement from "80% to 95%" may be "a cool technical achievement," but "the relationship between the technical scores and the user, like the UX, is not clear" (one practitioner).
    - Without shared language, teams settle for compromise—adopting constructs like "groundedness" not because it best captures quality, but because it was "the [construct] they were rejecting the least" (one practitioner).
    - However, agreeing to measure "groundedness" still leaves open what groundedness means—which poses the next challenge.
- **Establishing clear and meaningful constructs [C2]** proved difficult for thirteen participants with one practitioner calling it "the toughest part" of evaluation.
    - Our analysis points to a specific source of this difficulty: the absence of reference points.
    - "I don't know what good looks like before we start kind of release it into the wild."
    - This challenge is compounded by context-dependency; constructs that seem straightforward shift meaning across domains:
    - Faced with this complexity, teams often retreat: "they said, oh, it's too hard to measure relevance. It's too hard to measure" (one practitioner). Without clear constructs, extracting evaluation criteria from qualitative data [A5] becomes guesswork rather than systematic refinement.
- **Identifying viable evaluation approaches [C3]** proved equally difficult ($N=13$).
    - there is "no systematic" way to choose among methods (one practitioner).
        - When teams look for guidance, they encounter a gap: "You find all these frameworks that are all academic and none of them have been tested in product. And you're like, I don't know which is best" (another practitioner).
        - As a result, "we end up just kind of building our own things" (the same practitioner), but without confidence these approaches are sound.
    - The uncertainty has consequences: some teams "launch without evaluating" entirely (one practitioner), while others remain stuck, unable to systematize their ad-hoc toolkits [A7] into reusable approaches.
- Finally, **technical and operational barriers [C4]** prevent evaluations from occurring at all ($N=10$).
    - Human evaluation offers no escape from these constraints: "humans don't scale" (one practitioner), specialized domain expertise is expensive to recruit (three practitioners), and internal testers resist evaluation tasks they view as "actually quite boring and [time consuming]" (one of them).

##### Novel challenge: The Results-Actionability Gap

- **"results-actionability gap" [C5]**: the difficulty of translating evaluation outcomes into concrete, actionable steps for product improvement ($N=17$).
    - "How do we actually then use the information to inform the decisions going forward?" — a practitioner
    - This actionability gap is caused by two primary factors.
        - First, the evaluation results themselves are often ambiguous. Practitioners find that qualitative feedback, such as a subjective "vibe... does it feel right?" (one practitioner) or a context-dependent user preference (another), does not easily translate into a deterministic plan where "if outcome X then we take action Z" (a third).
            - The team knows there is a problem but not which component to change.
        - Second, even when a result is specific (such as a low score on a metric) it is often difficult to trace it back to a root cause. LLM-based systems involve many interacting variables—prompt wording, model selection, temperature settings, retrieval parameters, embedding models, context windows—any of which could be responsible for a poor outcome.
            - One practitioner framed this as a parameter problem without guidance: "There are tons of parameters that you can tune... Which dials do I change?"
            - "There are all these degrees of freedom that stack up and make the evaluation very unclear. You don't necessarily know what you have to do next. When you have an evaluation scale and you end up with a 4.6 out of ten, if you don't know what caused that, then it's very difficult to iterate on making it better." — a practitioner
    - But often, neither refinement nor rebuilding happens. One practitioner described what occurs when evaluation findings arrive late in development: "You're just pointing out a problem without a solution... [and] everybody just goes: Nope! We're pushing it live and we'll deal with it later."

### Discussion

- This study investigated how practitioners evaluate LLM-based products in production settings.
    - We interviewed 19 practitioners who develop LLM-based products across diverse sectors.
    - Our analysis identified ten evaluation practices [A1–A10] spanning evaluation execution, evaluation design, and the organizational meta-work that shapes both.
    - We also identified five challenges that complicate these practices.
- revealing a persistent pattern: across all three studies, practitioners rely on manual testing and interpretive methods rather than metric-based evaluation.
- these practices may not be problems to solve, but necessary adaptations to LLM characteristics that warrant support rather than replacement.
- We observed teams attempting to systematize their practices [A1–A10], progressing from ad-hoc vibe checks toward reusable evaluation approaches. We call this the *formalization journey*.
- the results-actionability gap: practitioners gather evaluation data but cannot translate findings into concrete improvements.

#### Situating Our Findings in the Practical LLM Evaluation Literature

- **Reframing manual testing as an inherent heuristic.**
    - our analysis reveals these "vibe checks" serve as essential first-line evaluation.
    - Participants described them as "irreplaceable" (one practitioner) assessments that capture qualities that formal metrics miss.
- **From "better" metric selection to actionable construct extraction.**
    - Prior work identified that practitioners conflate quality criteria with measurements
    - Responses vary, from "kitchen sink" approaches where teams try every available metric (Zhou et al, 2022), to structured research phases for defining custom metrics that combine subjective measures with objective ones
    - Our participants take a further step: they accept that metrics often fail for their contexts and use qualitative inquiry not as a complement to measurement, but as the source from which evaluation constructs emerge.
- **The overlooked role of organizational meta-work.**
    - Alignment, documentation, and advocacy are not unique to LLMs—they characterize complex technology development generally
    - However, prior LLM evaluation studies treat these activities as background noise, even though they are entangled with evaluation itself—shaping what gets measured and how.
        - Without alignment, stakeholders within a team may be evaluating different constructs without realizing it.
        - Without documentation, teams risk repeating discoveries others have already made.
        - Without advocacy, evaluation may get deprioritized or sidelined entirely.
        - Therefore, efforts to improve LLM evaluation should account for this organizational layer.

#### Incompatibility of Metrics-based Evaluation with LLM Realities: Factors Driving Interpretation

- From our analysis, we identify four factors that we argue are typical to evaluating LLM products.
    - **The mismatch between general-purpose models and specific contexts.**
        - Unlike traditional workflows where AI/ML models are trained for specific tasks, off-the-shelf LLMs function as general-purpose engines.
        - creates a structural misalignment: model providers optimize for broad capabilities, while practitioners require reliability in specific contexts.
        - standardized benchmarks capture only "a small part of the probability distribution," leaving teams with no guarantee that a passing score on a general benchmark implies reliability for their specific use case. Consequently, teams are forced to ignore established benchmarks and build bespoke test suites from scratch.
    - **Non-determinism combined with absent ground truth.**
        - creates what participants experienced as a dual epistemological problem: establishing adequate test data and determining "correctness."
        - Unlike traditional ML where teams could derive test sets directly from the same source of training data (Nigenda et al, 2022; Shergadwala et al, 2022), practitioners here must generate test data *out of nothing*.
        - This is complicated by the fact that "correctness" is often perspectival rather than objective; different users legitimately disagree on quality, making the search for universal evaluation criteria conceptually problematic
        - Consequently, "success" ceases to be a static, pre-agreed threshold (e.g., "$F_1$ must exceed 0.9") that persists across iterations. Instead, it becomes a negotiated agreement that must be debated and recalibrated within each project context—a dynamic made even more volatile by the rapid pace of model advancement.
    - **The failure of familiar quantitative approaches.**
        - Traditional software testing relies on clear diagnostic signals, an assumption that practitioners found violated by LLMs.
        - Prior to this era, organizations utilized ML evaluation infrastructure where specific signals (e.g., drift detection alerts) triggered clear actions (e.g., retraining on new data)
        - However, practitioners found that such pipelines now yield numbers without clear next steps for improvement.
        - familiar metrics (like accuracy) fail to correlate with user experience in open-ended contexts (e.g., LLM conversations or LLM-supported coding), the established feedback loop breaks down.
        - This forces a methodological pivot: practitioners turn to qualitative methods (vibe checks, expert judgment) out of necessity, yet often dismiss these practices as "not scientific"
    - **Adoption barriers for emerging frameworks.**
        - proliferation of new evaluation platforms. However, one practitioner noted the "cost of learning" them often outweighs the perceived benefit.
        - This complicates evaluation by forcing teams to prioritize local, expedient solutions (like manual spreadsheets) that become unmaintainable at scale. The result is "technical debt" (Cunningham, 1992), preventing the formalization of their evaluation practices.

##### For Practice: Strategies for Confronting the Results-Actionability Gap

- **Evaluation-by-design.** When evaluation is considered from the outset, it becomes an integral part of the design process rather than a post-hoc checkpoint. This does not mean rigidly adhering to initial goals, but iteratively refining both system and evaluation criteria together.
    - This integration does not just make evaluation more actionable; it also streamlines stakeholder communication (you already have shared success criteria), accelerates iteration cycles (you know what to measure after each change), and prevents costly late-stage pivots (problems surface during development, not after launch).
    - for each component, document:
        - "What's the most likely LLM failure?" (Hallucination? Wrong tone?)
        - "How will we detect it?" (User complaints? Expert review?)
        - "What can we adjust if it fails?" (Prompt? Model? Retrieval window?)
- **Build continuous sense-making throughout development.** Transform informal observations into institutional knowledge through lightweight documentation. Successful teams in our study maintained shared logs converting "vibes" into testable hypotheses (one practitioner's "prompt chains"), held weekly 30-minute synthesis meetings to update evaluation criteria, engaged domain experts as diagnostic partners who explain why outputs fail rather than just marking them incorrect, and documented what worked with specific changes, impacts, and decisions.
    - The payoff is clear—your tenth LLM project takes a fraction of the evaluation effort of your first. Make every observation count by asking "What would we want to know about this next time?" and documenting the answer.
- **Evaluate through incremental changes.** When evaluation reveals problems, resist overhauling everything.
    - Change one variable at a time (e.g., just the prompt or the temperature) and measure impact before the next change.
    - Document each micro-experiment simply: change, date, impact, keep/revert.
