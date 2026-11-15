---
type: system
status: structured
quality:
topics: [rag, knowledge-management]
source: ""
created: 2026-11-16
published:
author: Dom Nasrabadi
flashcards: none
updated: 2026-11-16
---
# Dry Run — Three Notes

A hand-run of the six drafted prompts on three notes, on 2026-11-16, to see how real text moves through the pipeline before any code exists. Every model call was a Sonnet subagent that saw only the prompt and its input. No store, API key or embedding model was used.

**The notes** (all about LLM judges and evals, each its own independence group):

| ID | Note | Status | Quality | Passages |
| --- | --- | --- | --- | --- |
| n1 | LLM-as-Judge Architectures (inc. runtime judges) | raw | ⭐ | 9 |
| n2 | How to Use LLM-Judges Properly | structured, no `published` date | ⭐ | 13 |
| n3 | Evals for AI Agents (Anthropic) | raw | ⭐⭐ | 28 |

## Result in one paragraph

Extraction works: the three notes produced 193 claims that stand alone, cite real passages and mostly hold up when checked. Matching does not: across three notes on the same subject, P4 found **no** pair of claims it would call `same`, and only 3 of 193 claims (1.6%) ended up supported by a second note, all through `refines`. That is far below the 10% line the spec uses to decide whether support scoring is worth keeping. This is the main finding, and it comes from how claims are written and compared, not from the missing embedding model.

## What happened at each step

| Step | What ran | Result |
| --- | --- | --- |
| Chunk | Script: split on headings, then bullets, 400-token cap (estimated as characters ÷ 4) | 50 passages. 4 are over the cap: 1 code block and 2 tables (allowed), and 2 single bullets with children that the script did not split further |
| P1 mentions | 1 call per note | 213 mentions. All but 1 were found in their passage. **37 had wrong offsets**, and one subagent skipped a mention because the offset was too hard to count |
| P2 adjudication | 1 call per note, in note order, 144 unresolved mentions | 128 new, 10 auto-linked, 6 to review. Registry: 105 entries (96 concepts, 16 entities after P3 added 7) |
| P3 claims | 1 call per whole note | 193 claims (33, 52, 108). None over 40 words, 2 open with a pronoun, 43 of 50 passages cited |
| P4 matching | 15 lexical clusters (68 claims) plus 3 hand-picked clusters (28 claims) | 0 `same` groups, 5 `refines`, 1 `contradicts` |
| Scoring | Script: w = quality × decay, support = ln(1 + sum over groups) | Support ranges 0.26 to 0.92. 3 claims have 2 groups. 2 claims are contested |
| P11 citations | 45 claim–passage pairs, 15 per note | 36 `supports`, 9 `partial`, 0 `no` (80% supports) |
| P14 exhaustiveness | 9 prose passages, 3 per note | 51 claims cite them, 4 misses (1 core): recall 0.93 |

## One claim, start to finish

1. **Passage** `n3-p22`, under "Design the eval harness and graders", includes the bullet that LLM graders should be closely calibrated with human experts.
2. **P1** marked "LLM graders" and "human graders" in it.
3. **P2** linked "LLM graders" to `reg:concept:llm-as-a-judge` at 0.85 (auto-link), and "human graders" to `reg:concept:human-evaluation` as `unsure` at 0.5 (provisional, review item). Both entries had been created from note 1 and note 2.
4. **P3** wrote claim `c165`: "LLM-as-judge graders should be closely calibrated with human experts to confidence that there is little divergence between human grading and model grading, which takes careful iteration to validate." About both entries, relation phrase "should be calibrated against", volatility `evolving`.
5. **P4** compared it with `c038` from note 2: "An LLM-as-a-judge should be calibrated against human judgments before it is trusted." Verdict: `refines`, confidence 0.62, not `same`, because c165 adds a standard of agreement.
6. **Scoring:** c165 has w = 1.5 × 0.744 = 1.116 and support 0.75 from one group. c038 gains qualified support from note 3 at half weight, giving it 2 groups and support 0.83.

A reader would say these two notes agree. The graph records it as a weak, low-confidence link that goes to the review queue.

## Findings, most important first

### 1. Claims almost never match across notes

- **What happened:** no `same` in 18 clusters, including three I built by hand from claims that plainly make the same point (calibrate judges against humans; pairwise beats scoring; use several judges).
- **Why:** P3 writes each claim faithfully, with the source's own details, numbers and reasons. P4's test for `same` is strict ("nothing would be lost by keeping only one"), and I told it to prefer `different` when unsure. Two sources rarely state a point with identical detail, so the test never passes.
- **Subagent feedback said the same:** "several claims point the same direction without asserting the same thing", and `refines` is "hard to apply to claims that bundle several assertions".
- **What it means:** as designed, support counting will separate almost no claims. Either the claim unit or the matching rule has to change. Options are under Recommended changes.

### 2. Character offsets cost accuracy and recall

37 of 213 offsets were wrong, and one mention was dropped because of the offset. The text itself was right in all but one case. Offsets should be computed in code.

### 3. P11 marks multi-passage claims as partial

6 of the 9 `partial` verdicts are claims that cite two or three passages. Each passage carries part of the claim, and P11 sees one passage at a time. For single-passage claims the rate is 33 of 36 `supports` (92%). The 3 real partials are dropped hedges or conditions ("could matter" written as "matters").

### 4. Tables hold claims that P3 is told to skip

Three table passages in note 3 (grader types with strengths and weaknesses; methods with pros and cons) produced no claims. The P3 subagent flagged that a careful reader would want them. P14 did not catch this because I sampled prose passages only.

### 5. One Registry entry is a hub already

56 of 193 claims are about `llm-as-a-judge`, and 32 are about `AI evaluation`. In a vault where one topic dominates, "about" a hub entry says little. Narrower subjects (pairwise judging, rubric, panel of judges) were more useful for finding related claims.

### 6. Duplicate Registry entries inside one note

P2 cannot see other mentions in the same batch, so one note produced "evaluation harness" and "eval harness", "evaluation suite" and "eval suite", "self-enhancement bias" and "self-preference bias". The bootstrap clustering step is meant to catch these, and it was not run here.

### 7. Things that worked

- **P3 claims read well on their own.** No pronoun problems worth the name, hedges mostly kept, boilerplate and code blocks skipped.
- **P3 merged repeats inside a note** (17 claims cite more than one passage), such as the TLDR and summary of note 2.
- **Volatility looks sensible:** 71 durable, 101 evolving, 21 ephemeral, with Anthropic-specific anecdotes marked ephemeral.
- **P2 was cautious in the right places:** "reference solution" against "reference response" came back `unsure`.
- **P4 found one real tension:** note 3 says occasional human review is enough once an eval system is robust; note 2 says regular comparison with humans is the only way to know a judge still works.
- **P14 misses were real** and all four quotes were found in the passage.

### 8. Smaller prompt problems the subagents reported

- **P1:** no rule for a term that is defined in the note but is also general vocabulary ("task", "trial"); no entity type for a leaderboard or a metric.
- **P2:** unclear whether `instance_of` is a name or a Registry id; no guidance on confidence for `new` when there are no candidates.
- **P3:** unclear when to merge a summary line with the detailed claim it restates; one output put a bare string in `referenced_time` (the enforced schema would have rejected it), taken from a year in a URL.
- **P4:** an empty answer cannot be told apart from not having looked; the time shown is usually the source date, which is confusing when a claim describes an earlier period.
- **P14:** "core" against "minor" is loose for bullet lists where every bullet is a main point.

## How this differed from the real pipeline

- **No embeddings.** P2 candidates and P4 clusters came from word overlap. This under-finds related claims, which is why I added the three hand-picked clusters.
- **Batched calls.** P2 and P11 ran many items per call, and P4 and P14 ran three calls per subagent. The prompts are written for one item per call.
- **A subagent is not an API call.** It carries its own system prompt, and output was not schema-enforced.
- **P14 used the same model as P3.** The spec asks for a stronger one, so 0.93 recall is likely optimistic.
- **New "about" targets from P3** were added straight to the Registry, not sent through P2.
- **No bootstrap clustering, co-occurrence or communities.**
- **Small samples.** 45 pairs and 9 passages. Treat the percentages as rough.

## Recommended changes

None of these has been applied. Each is a decision for Dom.

1. **Matching (the big one).** Three options, which can be combined:
   - **a. Add an `agrees` label to P4** for claims that make the same point with different detail. It would count as support at a reduced weight, between `same` and `refines`. Smallest change.
   - **b. Have P3 write a short core assertion as well as the full claim**, and match on the core. "LLM judges should be calibrated against human judgment" would then match across all three notes, while the detailed wording stays for citation.
   - **c. Stop counting support at the claim level** and count it per pair of Registry entries plus relation phrase ("LLM-as-a-judge — should be calibrated against — human evaluation"). The two claims in the worked example already share exactly that triple.
   I would test (b) first on these same three notes, because it keeps the rest of the design intact.
2. **P1: drop offsets** from the output and find the text in code.
3. **P11: judge a claim against all of its cited passages together**, and separately flag any cited passage that adds nothing.
4. **P3: extract from tables** when the table states assertions in words (pros, cons, strengths), and keep skipping tables of data.
5. **Hub handling:** leave an entry out of a claim's "about" list when it is the subject of the whole note, or dampen it earlier than the hub audit.
6. **Fix the small prompt gaps** listed in finding 8.

## Where the data is

Everything is under `50 Graph/dry-run/`. Obsidian does not show these files.

- `calls/`: the exact text each subagent was given (system prompt plus user message).
- `out/`: the raw JSON each subagent returned.
- `data/`: `passages.json`, `registry.json`, `claims_scored.json`, `p4_relations.json`, `p11_results.json`, `p14_results.json`, `review.json`.
- `scripts/`: the throwaway scripts for chunking, call building, checks and scoring. They are not the start of the real code.
