---
type: article
status: inbox
quality: 1
topics: []
source: https://x.com/akashbajwa96/status/2048656640639996142/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-04-27
author: Akash Bajwa
flashcards: none
updated: 2026-08-08
---

# Evals with Alec Barber, OpenAI

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1924416428519657472/jF95W4af.jpg" width="220" />
</div>

- **The central thesis: build your own eval harness**
- **Defining what a harness is***.* The harness is the layer around the model, e.g. the CLI for Codex or Claude Code are concrete examples. The CLI is the harness sitting on top of the mode

### Evaluating the evals

- **Entropy as a signal.** Run a single test case 10 times against the same model and grader. 10/10 pass or fail = low entropy, good signal. 5/5 split = high entropy, meaning the grader or test case is ambiguous. Costs 10x per case but the diagnostic value is significant.
- **Log-prob confidence scoring.** An attendee spoke about a vertical AI product that uses token-level probabilities from the OpenAI Responses API to compute a heuristic confidence score. Low-confidence outputs route to annotators who improve the dataset on the fly. The confidence-vs-performance curve isn’t perfect but is statistically validated.

### Dataset hygiene

- A useful split:
    - **Regression set.** Stable, broad coverage. Every change is tested against this.
    - **Iteration set.** Small, focused on a current failure mode.
- Fixes migrate from iteration into regression. Critically, **prune the regression set over time**
- **Practical recommendations for founders** 1. **Design your AI harness for testability from day one.** Decomposable, unit-testable, each component inspectable. Don’t build a blob and retrofit evals. 2. **Build your eval harness yourself using Codex or Claude Code.** The coupling to your AI harness is too tight to delegate to a generic platform. 3. **Use observability and dashboards off the shelf.** Langfuse, Grafana — don’t reinvent these. 4. **Find good eval-writing skills online** (he named Hamel Husain) and feed them to the agent as context. 5. **Invest in the domain-expert UX.** Build bespoke interfaces that mirror how experts already work, so you can extract their tacit judgment without training them on eval frameworks. 6. **Maintain the regression/iteration split** and prune stale tests over time. 7. **Use entropy diagnostics** to identify test cases where your grader is ambiguous.
