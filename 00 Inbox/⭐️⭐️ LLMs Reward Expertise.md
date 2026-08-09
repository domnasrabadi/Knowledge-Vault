---
type: article
status: inbox
quality: 2
topics: []
source: https://www.seangoedecke.com/llms-reward-expertise/
created: 2026-08-09
published: 2026-07-24
author: seangoedecke.com
flashcards: none
updated: 2026-08-09
---

# LLMs reward expertise

<div align="center">
  <img src="https://www.seangoedecke.com/og-image.jpg" width="220" />
</div>

- Today, everyone can write sort-of-okay CSS by delegating the task to an LLM. LLMs make everybody into a generalist.
- The most important skill in prompting is expertise in the domain you’re prompting for.
- A good illustration of this is [Terence Tao’s](https://en.wikipedia.org/wiki/Terence_Tao) [conversation with ChatGPT](https://chatgpt.com/share/6a5fdc7a-d6f8-83e8-bbea-8deb42cfed56) about the recently-discovered counterexample to the Jacobian Conjecture. This is not the same ChatGPT I talk to! I couldn’t get to where Tao gets, even with unlimited tokens to burn
- There’s a lot to learn about good prompting from Tao’s conversation. Here are a few observations:
    - Tao’s messages are very short and to-the-point. He doesn’t respond point-by-point to the model, just to the gist
    - The model outputs are much more concise than when I try and talk to GPT-5.6 Sol about mathematics. By signalling expertise, Tao shunts the model into “talking-to-mathematicians” mode, not “explaining-to-amateurs” mode
    - Tao pushes back when the model’s responses look wrong, but he doesn’t directly contradict; instead, he says things like “this looks more complex than I was hoping for”
    - Tao makes several leaps and suggestions himself. He almost never takes the model’s advice about where to go next
- the idea here — that **domain knowledge makes you better at using LLMs**
- If you have a good [theory of your codebase](https://www.seangoedecke.com/programming-with-ai-agents-as-theory-building/), you can push the LLM *much* harder than if you have no familiarity
- Because you have your own sense of what a good solution might look like, you can say “no, I think it could be simpler here”, or “but don’t we already do X?”, or “can we express this problem in these familiar terms?“.
- system design problems are dominated by concrete specifics, not generic principles
- If you have no domain knowledge, you can cling onto the LLM to at least get *something*. That’s [not bad](https://www.seangoedecke.com/ai-makes-weak-engineers-less-harmful/)! But if you have domain knowledge, you can wring far more value out of the same LLM by steering it hard in the direction you want.
- The usefulness of domain knowledge suggests that human expertise will continue to be useful even as models get stronger. For many tasks, **the human is the bottleneck, not the model**, because the difficult part is in communicating to the model exactly what kind of solution the human wants.
