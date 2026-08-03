---
type: paper
status: raw
quality:
topics: [llm-evaluation, llm-risks]
source: "https://arxiv.org/pdf/2410.12974"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# BenchmarkCards: Large Language Model and Risk Reporting

## Metadata
- Author: Anna Sokol, Nuno Moniz, Elizabeth Daly, Michael Hind, Nitesh Chawla
- URL: https://arxiv.org/pdf/2410.12974
## Highlights
- benchmark = dataset + evaluation metrics + pre- and post-processing steps used to assess specific llm behaviour
    - lack of standard documentation makes comparison, selection, and result interpretation hard
    - especially problematic for high-impact applications where risks and biases must be clear
- benchmarkcards = structured documentation framework for benchmarks
    - inspired by datasheets for datasets, model cards, factsheets, etc
    - captures essential metadata across dimensions like factual accuracy, toxicity, bias detection
- research questions
    - rq1 = what template elements are essential to describe objectives, limitations, biases of a benchmark
    - rq2 = how to communicate strengths and weaknesses so users can choose benchmarks and interpret results correctly
- benchmarkcard sections
    - benchmark details
        - name, overview, data type, domains, languages, similar benchmarks, resources
    - purpose & users
        - goal, audience, specific tasks, appropriate uses, limitations, out-of-scope uses
    - data
        - source, size, format, annotation method, validation process
    - methodology
        - evaluation techniques, metrics, calculation formulas, interpretation guidance, baseline results
    - targeted risks
        - risk categories mapped to ai risk atlas, demographic analysis, potential harm if model fails
    - ethical & legal considerations
        - privacy and anonymity safeguards, data licensing, consent procedures, regulatory compliance
- design principles
    - transparency = clearly state objectives, assumptions, data origins, and limitations
    - comparability = shared structure enables side-by-side review of multiple benchmarks
    - usability = concise but comprehensive fields help policymakers, researchers, practitioners and public readers
- example entry: bias benchmark for question answering (bbq)
    - overview = measures social biases in qa models
    - data = 58 492 synthetic qa pairs in english plus some multilingual extensions
    - metrics = accuracy and bias score (sdis, samb)
    - risks = age, gender, race, religion stereotyping
    - ethical notes = synthetic data, no personal info, cc-by-4.0 licence
- recommended customisation
    - card template may be tailored per domain or stakeholder needs
    - optional additions include interpretability methods, stakeholder explanations, privacy techniques
- outcome = benchmarkcards aim to standardise benchmark reporting, highlight biases and risks, and support informed llm evaluation

---
