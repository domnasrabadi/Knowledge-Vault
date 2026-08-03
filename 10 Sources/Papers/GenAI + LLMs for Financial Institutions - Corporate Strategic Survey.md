---
type: paper
status: structured
quality:
topics: [llm-risks, model-monitoring, banking-ai]
source: ""
created: 2025-07-13
published:
author: ""
flashcards: none
updated: 2025-12-28
---
## 0.1 Metadata
- Author: Jun Xu
- Category: pdf
- Document Tags: good 
- URL: [link](https://download.ssrn.com/2024/11/19/4988118.pdf?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMf%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDZpLF0iIdNu1VttG2pF4BYPd1V4aK30u%2BVA4rgYXNoSQIhAPzuB8TKvgTdPLCy8kkNT%2F3RfFgGX7wWDzB%2Bri%2FvEvXKKsUFCND%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQBBoMMzA4NDc1MzAxMjU3IgzkDEdjfxaBldScNxgqmQWRP1DlVxf%2BDNxQa%2FtKtZ2rAs0oKlD9yShAfW5ea6IIdlP4Nw%2FOzjpbssfUVj0meumOnin7%2Bqn%2FdnAGK0Z8U%2BSNykwm7KHbP5mWdFBftFfqrbw18LGepmFBogQfrvix0VdkAci2ndSpJpNkDGwSZF7eidvC30un2TAOLDWlo1WxJZ0hCShYc6NyXaEC0yU9GsfTyDcvOxENv6LHzLKy412t0WZ6rrnUOMdkROkMv7gDNduSAqj95vOhMxu5JXC3eWsIEW03X0cps4TJwdYp58oCbnczHymHUKMeGgYrtB0BCftLK%2BQr9R7VXmgiyaSXL%2F6nXsk45l%2BtoPx3Z%2FZOE1D6rDha2s22lEGIiPu%2B1HPXvBVQOUeJg4jMYzfEq0t0uegJUn%2FRV4gZtQUbXHX6KU0bvWjYXZ3ypB%2BY9ywM6vwTdTIiVt8c92tOcv9FOyvoLbHC2NSwzAYcKJb7lfR3KKSE72ZQYXUTgnRy9s%2B3wjjb9Cmkg5%2BMYgaJE5EgjbGaapK15Wdx94aFk7%2BZBBD6urh0bFrgUSxeSIeTq%2FfcOL8HbxyddvUVcj0DCRni%2FI7O3%2Fvc3cjq0UN5XVrWPH%2BuxCT.)
## 0.2 Highlights
- strategic adoption of LLMs within financial institutions (FIs) = explores transformational potential and adoption barriers
- benefits of LLMs
    - enhanced productivity = automate routine linguistic tasks such as email drafting, report generation, statement creation
    - customer value creation = power advanced chatbots and virtual assistants for personalised, multilingual service at scale
    - efficiency gains across business and governance = streamline supply-chain communications, financial forecasting, and other complex processes
    - transformational potential in underserved regions and domains
        - hr transformation = automate resume screening, onboarding, and personalised employee training
- challenges to adoption
    - technical barriers
        - integration complexity = requires continuous learning of evolving ai terminology and frameworks
        - hallucination = fluent yet inaccurate outputs threaten enterprise accuracy standards
        - algorithmic bias = inherited data biases may produce unfair or harmful results
        - need for customization = tailor models to domain jargon, it infrastructure, and regulatory requirements
        - productivity paradox = true gains appear only after process and skill adjustments, prompting revised roi models
    - compliance, regulation, and governance
        - control challenges
            - steerability = direct model toward desired outcomes
            - alignment = match outputs with organisational goals and regulatory rules
            - interpretability = understand model decision pathways
            - observability = monitor impact and compliance in real time
            - testability = evaluate performance across diverse conditions
        - over-dependence risk = diminished human skills and increased workflow complexity
    - data quality issues
        - unstructured, incomplete, or erroneous data introduces delays and inaccuracies
        - qualitative ambiguity complicates interpretation of financial information
        - asynchronous update cycles and evolving reporting practices create temporal mismatches
    - safety concerns
        - corpus viewpoints may conflict with target-country values or legal realities
        - lack of standardised responses for sensitive topics
        - language style may diverge from industry norms
    - fairness and bias mitigation
        - representational harms = stereotypes and performance disparities across social groups
        - allocational harms = inequitable distribution of resources such as credit
- adoption strategy for FIs
    - robust risk management = prioritise trust, accuracy, and reliability in GenAI solutions
    - phased rollout = deploy internally before exposing systems to customers with higher accuracy demands
    - continuous learning culture = equip teams to adapt alongside advancing ai technologies


**Table 1: Types of Bias**

| Type of Bias                      | Description                                                                                                                                                                                                                                                                                                                                           | Potential Solutions                                                                                                                                                                                                                                                                     |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Biases**                   | Encompasses biases arising from the training data, such as non-representative samples, overrepresentation of certain groups, temporal imbalances, or sentiment skew. This includes: - Sample Bias / Selection Bias- Availability Bias- Frequency Bias- Exposure Bias- Recency Bias- Positivity/Negativity Bias                                        | - Use diverse and representative datasets- Balance data to include underrepresented groups and rare instances- Regularly update training data to reflect current and varied information- Apply data augmentation and resampling techniques                                              |
| **Confirmation Biases**           | Biases where the model or users favor information that confirms existing beliefs, ignoring contradictory evidence. This includes: - Confirmation Bias- Confirmation-of-Common-Knowledge Bias                                                                                                                                                          | - Implement mechanisms to challenge assumptions- Use counterfactual reasoning and adversarial examples- Regularly update models with new insights- Encourage critical evaluation of outputs                                                                                             |
| **Social and Demographic Biases** | Biases stemming from stereotypes or prejudices related to social groups, demographics, cultures, or languages, leading to unfair or discriminatory outputs. This includes: - Group Attribution Bias- Social Bias- Implicit Bias- Relational Bias- Gender Bias- Age Bias- Economic/Socioeconomic Bias- Cultural Bias- Geographic Bias- Linguistic Bias | - Include diverse and balanced data representing various social and demographic groups- Use fairness and debiasing techniques in training and post-processing- Regularly audit model outputs for biases- Apply fairness constraints and metrics                                         |
| **Cognitive Biases**              | Biases resulting from the model’s processing strategies, such as overreliance on initial information or failure to correctly interpret context. This includes: - Anchoring Bias- Contextual Bias                                                                                                                                                      | - Design models to consider the full context- Implement mechanisms to reduce overreliance on initial inputs- Improve contextual understanding through advanced training methods- Use reinforcement learning from human feedback (RLHF)- Encourage model transparency and explainability |
| **Automation Bias**               | The tendency of users to overtrust AI-generated outputs without critical evaluation, potentially accepting incorrect or biased results.                                                                                                                                                                                                               | - Educate users to critically assess AI outputs- Implement confidence scores or uncertainty indicators to prompt users to verify results- Provide clear disclaimers and guidance- Encourage model transparency and explainability                                                       |


**Table 2: LLM Drifts**

|Category|Description|Potential Solutions|
|---|---|---|
|**Temporal Drift**|The knowledge base becomes outdated as new information emerges.|- Regularly update the external knowledge sources.|
|**Contextual Drift**|The model fails to retrieve relevant information for specific contexts or domains. Domain difference also falls in this category.|- Improve context-awareness in retrieval mechanisms.- Regularly monitor the stability and resiliency metrics of the pipeline.|
|**Semantic Drift**|The meaning or usage of words and phrases changes over time.|- Incorporate mechanisms to adapt to linguistic changes.|
|**Data Distribution Drift**|The distribution of data the model was trained on differs from the distribution of data it encounters in deployment.|- Use techniques like domain adaptation and continuous learning.|
|**Quality Drift**|The quality of information in the knowledge base degrades, possibly due to the accumulation of errors or low-quality inputs.|- Implement quality control measures and feedback loops for the knowledge base.|
|**Model / Algorithmic Drift**|Changes in the model’s algorithms or parameters over time can lead to performance changes. Over time, the pre-trained language model (LLM) used in RAG may experience drift due to changes in its training data or fine-tuning process.|- Monitor model performance and adjust algorithms as needed.|
|**User Behavior**|User behavior can evolve, leading to different patterns of interaction with the RAG system. This can cause drift in the types of queries and context provided.|- Regularly analyze user interactions and adapt the RAG system to evolving user needs.- Consider retraining the model based on recent user behavior.- Apply internal efficacy metrics on an ongoing basis.|
|**Pipeline Drift**|The pipeline may contain multiple steps (e.g., data parse, text chunk, query intent detection, vector similarity and re-ranking, and prompt engineering), which may cause drift.|- Apply metrics about context efficacy, anti-hallucination scores, answer relevancy, racial bias scores, and so on.- Monitor and refine each pipeline component to maintain end-to-end consistency.|


**Table 7: Challenges and Limitations of RAG**

|Category|Description|Potential Solutions|
|---|---|---|
|**Conflict between LLM’s Internal Knowledge and Retrieved Information**|RAG systems may provide incorrect or misleading responses when retrieved information contradicts the LLM’s knowledge, especially in critical domains.|- Implement consistency-checking mechanisms between retrieved data and the LLM’s internal knowledge.- Prioritize up-to-date, high-confidence sources.|
|**Quality and Accuracy of Retrieved Information**|RAG systems’ effectiveness relies on accurate, relevant documents. Inaccurate or outdated information can cause errors, misinformation, and erode trust.|- Regularly update and vet data sources.- Use filtering algorithms to prioritize the most accurate, reliable documents.|
|**Lack of Retrieval Quality Assessment**|Many RAG systems incorporate retrieved information without assessing its quality or relevance, potentially spreading errors and misinformation.|- Incorporate retrieval quality assessment methods that rank or flag sources based on credibility and relevance before incorporating them into the generation process.|
|**Vulnerability to Biased or Manipulated Information**|RAG systems can produce biased outputs due to biases or manipulation in the retrieved documents.|- Use bias-detection algorithms to identify and filter out biased content.- Diversify data sources to minimize the risk of biased retrieval.|
|**Inefficient Utilization of Retrieved Information**|RAG systems may use entire documents, including irrelevant parts, which introduces noise, reduces output quality, and increases computational costs.|- Implement summarization techniques and document segmentation to extract only the most relevant sections for use in response generation.|
|**Scalability and Efficiency Constraints**|RAG systems struggle with scalability and efficiency when handling large datasets, complex queries, or real-time needs.|- Optimize query algorithms.- Use parallel processing and indexing techniques (e.g., vector or graph databases) to improve scalability and processing speed.|
|**Limited Adaptability to Diverse Domains and Tasks**|RAG systems may have limited adaptability to complex domains, reducing their applicability in real-world scenarios.|- Fine-tune RAG models on domain-specific data.- Employ modular architectures that allow easy adaptation to different tasks or industries.|
|**Evaluation and Benchmarking Challenges**|Evaluating RAG systems is challenging due to dynamic retrieved content and lack of standardized metrics.|- Develop standardized benchmarking metrics and protocols tailored to RAG systems that account for dynamic retrieval and varying content accuracy.|
|**Lack of Transparency and Explainability**|The opaque decision-making process of RAG systems can hinder adoption in sectors valuing trust and accountability.|- Incorporate explainability frameworks such as model interpretability tools or traceability features that show how retrieved data impacts the final response.|
|**Alignment with User Expectations and Interaction**|User expectations may not align with RAG systems’ actual capabilities, risking overreliance or misuse, emphasizing the need for clear communication.|- Clearly communicate system limitations and capabilities.- Set user expectations through detailed user guides or real-time feedback on system performance.|


**Table 12: Industrial Applications of LLMs in Financial Services**

|Application Name|Explanation|Financial Institutions|Reference URL|
|---|---|---|---|
|Automated Financial Processes|Uses LLMs to automate tasks like workflow generation, financial document analysis, and report writing|Various|McKinsey & Company|
|Wealth Management|Leverages LLMs for financial product evaluation, market analysis, investor education, and portfolio management|Morgan Stanley; UBS|Forbes|
|Insurance Services|Applies LLMs to explain insurance products, create plans, and verify claims|Lemonade; Ping An|Lemonade Blog|
|Fraud Detection|Analyzes emails and transactions for signs of fraud using LLMs|JPMorgan Chase|Bloomberg|
|Regulatory Compliance|Uses LLMs to specify information clients must provide to regulators|Wells Fargo|Reuters|
|Customer Service|Implements LLM-powered chatbots and virtual assistants for improved customer interactions|Bank of America; Capital One|Bank of America Newsroom|
|Investment|Assists in investment analysis, information extraction, and content creation|BlackRock; Goldman Sachs|BlackRock Blog|
|Analysis|Extraction and content creation|Sachs||
|Risk Management|Enhances risk assessment and management processes|Various|Deloitte Insights|
|Synthetic Data Creation|Generates synthetic financial data for model training and strategy testing|Various|Synthesis AI|
|Fundamental Analysis|Refines investment theses and uncovers latent relationships between industries|Point72; Bridgewater Associates|Financial Times|
|Market Prediction|Explores the use of LLMs for predicting market trends and stock performance|Various hedge funds|MIT Technology Review|
|Document Processing|Processes and analyzes large volumes of financial documents and reports|KPMG; EY|KPMG Insights|

**Table 16: Criteria Differences for RAI**

|**Criteria**|**LLM-Based Projects**|**Traditional ML Projects**|
|---|---|---|
|**Complexity and Autonomy**|More complex and capable of generating autonomous outputs, raising accountability concerns.|Generally less autonomous with clearer parameters, allowing simpler accountability mechanisms.|
|**Bias and Fairness**|Higher risk of amplifying biases from diverse training data; requires rigorous bias detection and mitigation.|Bias is a concern, but typically focused on specific features or outcomes rather than broader implications.|
|**Transparency and Explainability**|Opacity in decision-making necessitates strong explainability mechanisms for understanding output generation.|Clearer decision pathways make it easier to explain outputs, focusing on feature importance.|
|**Safety and Security**|High potential for misuse (e.g., generating misleading information); requires robust safety protocols.|Safety is important but may not face the same level of risk related to content generation.|
|**User Interaction and Feedback**|Interactive nature leads to dynamic learning from user inputs; requires monitoring for ethical use.|User interaction may be less dynamic, focusing on performance metrics rather than ongoing ethical considerations.|
|**Regulatory Compliance**|Subject to emerging regulations addressing societal impacts of generative AI; requires alignment with these regulations.|Regulatory compliance typically focuses on data handling and model fairness without the same level of adaptation needed for LLMs.|

---

**Table 18: Priority Decision Matrix**

| **Attribute**                      | **Explanation**                                                                                                                                                                             | **Weight** |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------: |
| **Direct Value**                   | Measures the immediate benefits such as profit increase, cost reduction, and efficiency improvements directly attributable to the project. Usually, we shall define a reasonable objective. |         20 |
| **Strategic Value**                | Assesses how well the project aligns with the organization’s long-term strategy, goals, and competitive positioning in the market. Usually, we shall evaluate based on different scenarios. |         20 |
| **Technical Feasibility**          | Evaluates the likelihood of successful technical implementation based on available technology, data quality, and in-house expertise.                                                        |         15 |
| **Implementation Feasibility**     | Considers the ease of implementing the project given existing infrastructure and skill sets, including whether to build in-house or purchase solutions.                                     |         10 |
| **ROI (Long-term vs. Short-term)** | Estimates the potential return on investment and balances projects that offer immediate benefits against those that provide long-term value.                                                |         15 |
| **Risk Tolerance and Management**  | Identifies the potential risks involved, including technical challenges, regulatory compliance issues, and operational obstacles.                                                           |         10 |
| **Market Adoption**                | Gauges the potential for market acceptance or internal adoption, including user readiness and competitive dynamics.                                                                         |         10 |
| **Total**                          |                                                                                                                                                                                             |        100 |
