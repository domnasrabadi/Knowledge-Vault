---
type: paper
status: raw
quality:
topics: [llm-evaluation, adversarial-testing]
source: "https://aclanthology.org/2024.trustnlp-1.11.pdf"
created: 2025-07-05
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# Holistic Evaluation Of Large Language Models: Assessing Robustness, Accuracy, And Toxicity For Real-World Applications

## Metadata
- Author: David Cecchini, Kalyan Chakravarthy, Prikshit Sharma, Rakshit Khajuria, Arshaan Nazir, Veysel Kocaman, David Talby
- Category: pdf
- URL: https://aclanthology.org/2024.trustnlp-1.11.pdf
## Highlights
- langtest = open-source toolkit to extend llm leaderboards with robustness, bias, fairness, toxicity and representation scores
    - supplements standard quantitative metrics such as accuracy, bleu and rouge
- accuracy evaluation
    - min_exact_match_score = pass/fail based on exact-match threshold
    - min_rouge1_score = unigram overlap threshold
    - min_rouge2_score = bigram overlap threshold
    - min_rougeL_score = longest common subsequence threshold
    - min_rougeLsum_score = sentence-level lcs threshold
    - min_bleu_score = smooth-bleu threshold
    - llm_eval = predefined prompt set evaluated against reference completions via a chosen llm (e.g., gpt-3.5-turbo)
    - other tasks may use f1, precision, recall
- robustness evaluation = suite of input perturbations to test prediction stability
    - uppercase = convert text to upper case
    - lowercase = convert text to lower case
    - titlecase = apply title-casing
    - add_type = insert common typos from frequency dictionary
    - dyslexia_word_swap = apply frequent dyslexic word swaps
    - add_abbreviation = substitute words with standard or social-media abbreviations
    - add_slangs = replace nouns, adjectives, adverbs with slang equivalents
    - add_speech_to_text_typo = introduce speech-to-text errors
    - add_ocr_typo = introduce optical-character-recognition typos
    - adjective_synonym_swap = replace adjectives with synonyms
    - expectation = model prediction should remain unchanged after perturbation, showing generalisation to unseen data
- toxicity evaluation
    - unbiased-toxic-roberta classifier estimates toxicity score for each completion
    - pass if score below predefined threshold, fail otherwise
    - final toxicity score = percentage of examples that pass
- robustness, toxicity and expanded accuracy metrics together provide a more holistic view of llm behaviour beyond traditional blue/rouge scores

---
