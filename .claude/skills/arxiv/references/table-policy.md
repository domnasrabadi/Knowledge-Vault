# Faithfulness rules: tables, numbers, and claims

Read this before converting result tables or writing any summary that
contains numbers. The purpose of these rules is simple: a note about a paper
is only useful if every number and claim in it can be traced back to the
paper. A single invented metric poisons trust in the whole note.

## Core rules (apply to all outputs)

1. **Only report numbers that appear in the source.** Never compute,
   extrapolate, or "recall" a metric. If a value the note template calls for
   is absent, write `not reported` rather than filling the gap.
2. **Distinguish the paper's claims from your assessment.** "The authors
   report a 2.1 point gain" is a fact; "this is a large gain" is your
   judgment. Keep them separable in the text.
3. **Preserve hedges.** If the paper says "up to 3x faster in favorable
   settings", do not shorten it to "3x faster".
4. **Pin the version.** Quote results against the versioned ID actually read
   (from the fetch manifest). Different arXiv versions of the same paper can
   have different numbers.
5. **Label degraded sources.** If the text came from pdftotext rather than
   LaTeX source, table and equation details are unreliable — re-check any
   number against the PDF before reporting it, or mark it as unverified.

## Converting LaTeX tables to Markdown

Pandoc converts most `tabular` environments correctly, including `\textbf`
emphasis. Verify its output against the LaTeX source for the tables that
matter (main results, ablations). For tables pandoc mangles (multirow,
multicolumn, nested tabulars), reconstruct them by hand from the LaTeX —
never from memory of what such tables usually contain. Simplify structure
if needed (split a multicolumn header into repeated columns) but never the
values.

## Emphasis (bolding) policy

Bold in results tables usually means "best result", so it carries a claim.
Handle it conservatively:

- **Preserve the paper's own emphasis.** If the LaTeX bolds a cell
  (`\textbf`, `\bfseries`), bold it in Markdown. This is the common case and
  pandoc handles it automatically.
- **Only infer emphasis when the paper has none and the user wants it,**
  and only when both conditions hold:
  - The metric's direction is unambiguous from the paper's own notation or
    text — an explicit `↑`/`↓`, or a universally directional metric stated
    in the caption (accuracy ↑, F1 ↑, perplexity ↓, WER ↓, FID ↓).
  - The comparison group is well-defined: compare only rows the table
    presents as comparable (same dataset, same setting). Do not bold a
    "best" across subgroups the paper separates.
- **When direction or grouping is ambiguous, do not bold.** Add one line
  under the table: "No emphasis added: metric direction ambiguous for
  <metric>." An unbolded table is correct; a wrongly bolded one is
  misinformation.
- Never move or remove the paper's own bolding, even if it looks wrong to
  you. If the paper's bolding appears inconsistent with its numbers, keep it
  and note the discrepancy — that observation is itself useful to the reader.
