---
type: paper
status: structured
quality:
topics: [llm-risks, banking-ai, model-monitoring, human-in-the-loop]
source: ""
created: 2025-07-13
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Agus Sudjianto, Rafic Fahs, Yu Pan, Krish Swamy
- Category: pdf
- Document Tags: good 
- URL: [link](https://download.ssrn.com/2024/11/30/5039309.pdf?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIC2pjvQak6Pj1Qs2rDiI1ElZnWhnYwbI9jQ%2F5i4UjqHaAiEArb%2FfJPqKq6bZ6fzaqSDTUpoNgtRHPeK94LweDmk%2FrWsqxgUI0P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAEGgwzMDg0NzUzMDEyNTciDDh0DPcvi9Oc1Y19ciqaBd%2B%2B5EjDcwFKDvIuMGZadqzmr0qJsqbSXMy6fJ5OyriO6xz80HZ%2BPPWua8gue2rsiR%2FMSpbz5Z%2Fh0xBQVTOm%2B6OQY7DWMJiowT%2FuAWdYgmKKtkCjEv0lnOWGzZ5y0GTIlaxrHBFi8L6Hw%2FkLZN%2FsTcNCdDw9EZMzLQbx3UQfz7qqeLrZam8h35robt4MWpCniCdirhi50upNnKLby7k9n7yg53EV5wfkne2InQXYFmHp%2BgWjHffEBi4iHrIcaLnOdoKjb4twOPHK%2BE3voxeyXRFM%2BqGdBrlI86Mhsa%2F9fVhhWRkjCxpfVpvfKpP5lsJrxgeYqREF0JG66nlR%2F%2BzxSk8%2Fx1V3tPXZkkNkNGzBRSLeeJB6J%2BXgGddofRFOUO6HVbyW774%2B12VTmSOfOwUhX9wHRtQlqsK4dzGV%2FEFa%2B5l9Yuk8RzPNQALq09XfqVIk9x00CRKhOzy%2F7spOkTM0edydwNX%2BZIoAjrD6xLSb2dBWkCAKMnA5MqLIFXqa8abQn8beRZcvtvAJLU2L7EfrrApy3X9UVXUyBtbBzb7XoDUwumwYyRKuw23D3u1lCusXuFG6hoUTdE6b5vBZimz9M)
## 0.2 Highlights
- proactive approach = addresses zero-shot pitfalls to align LLMs with banking’s precision, compliance, accountability
- conceptual soundness = cornerstone of model risk management (Federal Reserve SR 11-7)
    - built on sound theory, purpose-fit data, and reliable outputs
- allure of zero-shot deployments
    - speed to market = deploy rapidly with minimal prep
    - cost efficiency = sidestep large-scale data collection + training
    - versatility = one model covers diverse tasks
- risks when conceptual soundness is absent
    - complaint categorisation scenario
        - challenges
            - overlooks subtle grievances → false negatives
            - tags benign feedback as complaints → false positives
            - ignores region-specific regulations
        - impact = compliance breaches, delayed resolutions, fines
    - regulatory report drafting scenario
        - challenges
            - outputs plausible yet incomplete or incorrect reports
            - lacks audit-ready structure
        - impact = regulatory scrutiny, penalties, reputational harm
    - customer-service chatbot scenario
        - challenges
            - gives inconsistent or misleading answers
            - omits required financial disclaimers ⇒ UDAAP violations
        - impact = eroded trust, legal liability
    - document verification scenario
        - challenges
            - misclassifies document types
            - misses compliance checks in legal docs
        - impact = non-compliance, operational risk
- 3 pillars of conceptual soundness for LLMs
    - sound model development principles = ensure fitness for purpose
    - data relevance = mitigate risks from inappropriate training data
    - explainability = promote trust via transparent behaviour
- making LLMs bank-ready
    - domain-specific fine-tuning = tailor to banking language + regs
    - retrieval-augmented generation (RAG) = ground answers in trusted knowledge bases for factual accuracy
    - rigorous testing & validation
        - cover all topics + sub-topics (e.g. complaint types)
        - include simple, complex, ambiguous query types
    - continuous monitoring = track performance vs evolving regulations, retrain when needed
    - human oversight = keep experts in the loop for high-stakes decisions
- guiding principle = view LLMs as powerful tools—not magic bullets—whose value emerges when applied with discipline and oversight
