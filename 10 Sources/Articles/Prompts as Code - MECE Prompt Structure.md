---
type: article
status: raw
quality: 
topics: [prompting, ai-engineering, agent-evaluation]
source: https://x.com/wulfie_bain_/status/2098060386813566990/?s=12&rw_tt_thread=True
created: 2026-09-13
published: 2026-09-10
author: Wulfie Bain
flashcards: none
updated: 2026-09-14
---

# Prompts as Code - MECE Prompt Structure

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1953500654338478080/JJXqBaD5.jpg" width="220" />
</div>

## TLDR

1. Most prompts are bad because prompt evolution tends to be *accretive*: we only add, never remove, over time. This leads to spaghetti prompts, with contradictions and ambiguity. This has real business impact.
2. We need to treat prompt changes as product changes (because agent behaviour *is* product), and treat prompts as code (modularised, MECE, and all your other favourite acronyms; refactored if need be & actively maintained).
3. Well structured prompts enable teams to move faster, prevent regressions, and have better agents. I propose a very simple structure at the end.

- Prompting decisions *are* product decisions, and using structure to make unambiguous, maintainable prompts is critical for making great agents
    - This is not about being beautifully written prose, or nicely formatted; it's about logical errors that lead to the mistakes their agents make.

## Bad prompts

- The two key issues are contradictions and ambiguity
    - Our current process for prompting is *accretive* & leads to contradictions
        - As the startup grows, and the agent is required to do more things, they add to the prompt. Errors occur, so they add a few lines to fix those.
        - The prompt only gets longer. And no-one reviews the entire prompt end to end. Almost always, that leads to contradictions in the prompt, because as you add new content, old content saying something else is kept.

### Implicit knowledge leads to ambiguity

- Even if an engineer does review a prompt end to end, they often don't *truly* read it
    - When you read & interpret a sentence, you don't only use the words on the page.
        - You use all of the knowledge you already have to make sense of those words.
        - And that's a problem, because you often know what you want the sentence to say; and you read that, rather than what it actually does say
- This is the problem of *specificity*: the prompt doesn't *actually* say what we want the agent to do, because we haven't unambiguously specified it.

### Conditional prompts compound this

- The above problems are compounded by *conditional* prompts, where additional prompt content is injected depending on the scenario.
    - Different engineers work on various parts in separate files.
    - And that means that even if *each* team/engineer reviews their prompt for contradictions & specificity, no-one reviews the whole.

### The outcome?

- We get spaghetti prompts. Thousands of lines, with interaction effects between many paragraphs, and it's almost impossible to review them because by the final sentence, most humans have totally forgotten the first line. Or got bored and stopped.
- My principles: start treating prompting as product, and prompting as code. The solution: making MECE, structured prompts that are maintainable.
    - Each time your engineers add to a prompt, or don't add to a prompt and so leave it ambiguous, they are making product choices. So making *specific* choices is critical for coherent product experience.

## Prompting as code

- We use human readable language to get a computer to do what we want. That was true of programming languages, and it's also true of prompting current LLMs

### Structure with MECE prompt sections

- MECE stands for mutually exclusive (ME), collectively exhaustive (CE), and basically means you're covering everything relevant (CE) without duplication (ME)
    - Collectively Exhaustive: together, your prompt sections comprehensively cover (specify) the behaviour you want.
    - Mutually Exclusive: each prompt section should be self contained, with no overlap.
- This leads to DRY (Don't Repeat Yourself) prompts, which are easier to maintain & review. When you make changes, you change one specific section without worrying it will interact with content elsewhere
- Separate concerns where possible. Modular code is good code; modular prompts are good prompts.
- **Aim for the specificity of programming**
    - When engineers write code, they are precise in their desires. If this, then that.
        - But as soon as it is prose, these same people stop being precise.
        - Instead, think of it like code.
    - For example, you might wish to still employ IF ELSE logic.
        - For example, when describing how your agent uses a web search tool, you might want it to only use websearch on certain topics.
        - If topic X, use web_search; Else just use internal knowledge.
        - Or perhaps you always want it to search.
        - Whatever your desire, specify that.
    - The aim is NOT to 'program' every eventuality - otherwise you wouldn't use an LLM. But you do want to specify the behaviours you desire in the core branches on the tree of user requests, or the rubric for when to do certain things.

### Separation of backend and frontend

- I like to think of this like separating concerns of backend and frontend.
    - Behaviour: this is how the agent should act whilst preparing its output.
        - It's the way it uses tools, the way it interacts with broader systems, the way it plans (or doesn't).
        - In other words, it's like the backend; it covers the logic, and the user shouldn't see this.
    - Output: this is the frontend, the user facing part of the agent.
        - What the agent outputs could be totally independent of how it thinks.
        - For example perhaps we want it to think in very rational, structured ways; but output in beautiful prose.
        - Or always use code to do data analysis, but never show code to the user.

### Refactor every so often

- Even with the best intentions, prompts can get messy. Dedicate some time to paying down your prompt debt. If new sections are relevant, add them; if some sections are getting large, split them.

## Template of a good prompt: Background, Behaviour, Output

- So we want a nicely structured, MECE prompt, that separates concerns where possible

![](https://pbs.twimg.com/media/HRzUeBSWMAU0W8h.png)

- You'll notice this is hierarchically organised, like a tree. This helps it be MECE, and means you can find sections much faster.
- When you make an eval, whether with deterministic ground truth or a rubric for a judge, you have to *specify the desired behaviour*.
    - And half the time you realise you literally just never specified that desire in your prompt, it was latent context in your brain, not explicit in the prompt, OR you actually hadn't clarified it even to yourself.
    - Evals force clarity, and so they force clear product decisions.

## Benefits of structured prompts

### Fewer contradictions

- With MECE sections, reviewing the prompt is easy. Each section is self contained, and instead of having to keep hundreds of lines in your memory to find contradictions, you just review that section

### Faster & safer iteration

- Separating concerns lets you iterate incredibly fast. When you find an issue, you just add a line to one specific section, knowing that it should have minimal interaction with other parts

### Faster search

- In spaghetti prompts, you have to remember key phrases in your prompt or the filenames to find the section to change. With hierarchically organised prompts, the search process for the relevant sections is much faster (it's a tree search)

### Faster Model Upgrades

- When a new model comes out, it's much easier to test its defaults.
    1. Perhaps all the 'examples' are no longer needed because the new model is just smarter. It now takes 5 seconds to find the examples section and delete it.
    2. Perhaps whilst a previous model always used to output em dashes, so you needed a line in your Output section about that, the new one doesn't. That's a one line deletion and a few tokens saved.
- **As models get smarter doesn't this become irrelevant?**
    - it proves the point: higher intelligence cannot automatically solve ambiguity and contradictions in *your preferences*
