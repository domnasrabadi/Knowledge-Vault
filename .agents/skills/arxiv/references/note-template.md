# Output formats: structured notes and contextual reading

Two reading modes produce written artifacts. Ask which the user wants only
if it is genuinely unclear; "summarize this paper" means a structured note,
"read this paper and tell me what it means for my project/repo" means a
contextual reading.

## Mode A: Structured note

A self-contained reference note about the paper. Default location: a
`papers/` directory in the current working directory (create it if absent),
filename `<versioned-id>-<short-slug>.md`, e.g. `2409.03108v2-mamba2.md`.
If the user has a notes system (Obsidian vault, `knowledge/` folder), write
there instead and follow its conventions.

Use exactly this structure; omit a section only if the paper genuinely has
no content for it, and write `not reported` for missing values rather than
guessing (see table-policy.md, which is mandatory reading before filling in
Results):

```markdown
---
arxiv_id: <versioned id actually read, e.g. 2409.03108v2>
title: <title>
authors: [<authors>]
published: <YYYY-MM-DD of v1>
version_read: <version and its date>
categories: [<categories>]
source_quality: latex | pdf-text | pdf-only
---

# <Title>

## TL;DR
2-4 sentences: the problem, the idea, the headline result.

## Contributions
The paper's main contributions, as the paper frames them.

## Method
How it works, at the level of detail the user asked for. Keep the paper's
own notation. Include key equations in $...$ / $$...$$ form.

## Results
The main results table(s), converted per table-policy.md, plus the one or
two ablations that matter. State the evaluation setup in one line.

## Limitations & open questions
What the paper itself concedes, plus anything evidently unaddressed.
Attribute clearly: "the authors note X" vs "not discussed: Y".

## Citation
The BibTeX entry from `bibtex.py`.
```

## Mode B: Contextual reading (paper -> this project)

Used when the paper is being read *for* a codebase or project the user is
working in. Before writing, actually look at the relevant parts of the
project — the files, the model code, the training loop, whatever the paper
touches. The value of this mode comes entirely from specific connections;
generic summaries are a failure here.

Write to the project's `knowledge/` directory if one exists (this mirrors
common practice), else `papers/`. Same filename convention as Mode A.

Structure:

```markdown
# <Title> (<versioned id>) — notes for <project>

## What the paper does
Short factual summary (3-6 sentences).

## Relevance to this project
The specific mapping: which ideas apply, to which files/components, and why.
Name real paths and functions. If an idea does NOT transfer (different
scale, different constraints), say so explicitly — negative findings save
future re-reading.

## Concrete changes we could try
Ranked, each with: what to change, where, expected effect, effort estimate,
and what the paper's evidence actually supports (vs. what would be
extrapolation to our setting).

## What we'd need to verify
Assumptions in the paper that may not hold here; experiments to run first.
```

Faithfulness rules from table-policy.md apply in both modes. In Mode B,
be doubly careful to separate "the paper showed X" from "X might work here" —
the second is a hypothesis, and the note should read that way.
