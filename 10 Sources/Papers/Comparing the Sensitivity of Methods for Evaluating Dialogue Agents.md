---
type: paper
status: structured
quality: 1
topics: [agent-evaluation, evaluation-metrics, human-in-the-loop]
source: ""
created: 2025-08-10
published:
author: ""
flashcards: none
updated: 2025-12-28
---
# 1 Metadata
- Author: 
- Category: pdf
- Document Tags: ⭐️⭐️ very good 
- URL: https://arxiv.org/pdf/2201.04723
# 2 Highlights
- challenge = finding reliable methods to evaluate conversations for conversational AI
- evaluation dimensions
    - **per-turn evaluation** = rating after every model response
        - fine-grained, highlights small differences
        - detects changes over time but may miss holistic quality
    - **per-dialogue evaluation** = rating only at end of conversation
        - captures overall quality, patterns, and emergent traits
        - may miss mid-dialogue performance changes
- human evaluation variability = different data collection methods yield different levels of agreement, sensitivity, cost, and annotation hours
- **automatic metrics** = useful for specific aspects but cannot replace human judgments for realistic and engaging conversation quality
- **pairwise vs single-model**
    - **pairwise** = annotator compares responses from two models
        - reveals subtle differences
        - reduces distribution-shift issues in absolute scoring
        - works well when differences appear over multiple turns
    - **single-model** = annotator rates one model alone
        - better when direct comparison not needed
        - may underperform when differences are subtle or emerge over time
### 2.1.1 Key findings
- evaluations must cover multiple turns to detect faults like repetitiveness or contradictions
- **pairwise per-turn** = best for spotting performance changes during conversation
- **pairwise per-dialogue** = best for differences that appear only after several turns or in aggregate patterns (e.g., average length)
- Likert-scale ratings can suffer from inconsistent scoring across models
- **single-model methods** = work when models are similar in quality but differ slightly

---

## 2.2 Evaluation Techniques
- **single-model per-turn** (SM-Turn) = annotate each response on engagement, human-likeness, and interest
- **single-model per-dialogue** (SM-Dialog) = end-of-conversation Likert ratings for same metrics
- **pairwise per-turn** (PW-Turn) = choose best model response after each turn
- **pairwise per-dialogue** (PW-Dialog) = choose best conversation after reading full dialogues
- **pairwise per-dialogue self-chat** = models converse with themselves, then rated pairwise

---

## 2.3 Methodology Details
- conversations = between crowdworker (human speaker) and bot (model)
- **PW-Turn** = after every human message, worker picks better of two model responses
- **PW-Dialog** = worker reads two complete dialogues and selects better
- **SM methods** = combine per-turn and per-dialogue in UI
    - per-turn = tag engaging, human-like, interesting
    - per-dialogue = Likert-scale ratings (1–5) for same metrics

![[Screenshot 2025-08-10 at 2.35.31 pm.png| center | 500]]

- quality control
    - exclude low-quality workers using consistent criteria
    - restrict each worker to 1 conversation per model-pair (pairwise) or per model (single-model) per metric

---

## 2.4 Results Overview
- **model win rates by turn** = PW-Turn can track win-rate changes over conversation length, unlike PW-Dialog
- **fine-tuning comparison** = PW-Turn performs best (detects nonsensical replies during live conversation)
- **length comparison** = pairwise methods outperform single-model
- **size comparison** = smaller differences, with dialogue-level methods slightly ahead
- combining techniques
    - no single method works best in all cases
    - combined approach may yield balanced sensitivity
    - ideal method = integrates per-turn sensitivity with global quality assessment

![[Screenshot 2025-08-10 at 2.35.57 pm.png| center | 200]]

![[Screenshot 2025-08-10 at 2.36.19 pm.png| center | 400]]

![[Screenshot 2025-08-10 at 2.36.29 pm.png| center | 400]]
