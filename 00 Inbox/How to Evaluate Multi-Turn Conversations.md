---
type: article
status: inbox
quality: 
topics: []
source: https://www.braintrust.dev/blog/multi-turn-scoring
created: 2026-08-22
published: 2026-05-14
author: Braintrust Team
flashcards: none
updated: 2026-08-22
---

# How to evaluate multi-turn conversations

<div align="center">
  <img src="https://www.braintrust.dev/og?title=How+to+evaluate+multi-turn+conversations&description=Learn+how+to+score+multi-turn+conversations+by+combining+per-turn+and+per-conversation+evals%2C+then+automating+it+all+in+production.&template=blog&v=3" width="220" />
</div>

- Most evals are designed to score a single AI output at a time. This works for tasks like summarization or classification, but it falls short for conversations with multiple back-and-forth interactions.
- especially important for conversational AI products
- The only way to know if a multi-turn AI product is working as intended is to score conversations as a whole, in addition to scoring individual turns.
- Single-turn evals can be helpful in some instances, but they can't tell you if the bot asked for the same information twice, if it contradicted itself later on in the chat, or if it kept the customer in a polite, professional loop for ten minutes without ever solving anything.
- These are the kinds of failures that only surface when you look at the entire conversation. Doing this properly requires both layers of scoring: one for individual responses, and one for entire conversations.
- Single-turn scoring will help you review brand alignment for individual responses, while multi-turn scoring will measure the quality of an entire conversation.
- It checks three things:
    - Whether the response directly addresses the customer's issue with actionable next steps. A reply that just says "I understand your frustration" without offering to do anything scores poorly.
    - Whether the tone is empathetic and professional, not robotic, overly casual, or dismissive.
    - Whether the response follows company support guidelines, like offering a refund when the customer qualifies for one.
- A four-turn conversation gets four separate Brand Alignment scores, and Braintrust averages them at the trace level so you can see the overall per-turn quality at a glance. But a conversation can be brand aligned while still failing to resolve a customer's issue, which is why you need to score the conversation as a whole.
- A multi-turn scorer ignores individual responses and instead looks at the full conversation thread to answer one question. Did this interaction successfully resolve the customer's issue?
- It runs once per trace, not per turn. It doesn't measure if individual responses were awkward or imperfect, as long as the customer's problem was solved in the end. And conversely, it doesn't matter if every response was beautifully written if the customer walked away without a resolution.
- Neither score alone gives you the full picture. The single-turn scorer catches per-response issues like vague answers, wrong tone, and missing information. The multi-turn scorer catches conversation-level failures like dropped context, unresolved issues, or circular exchanges where nothing progresses.
- You need multi-turn scoring to eval an entire conversation, but you need both multi-turn and single-turn scoring together to fully understand your chatbot's performance and improve it.
- The individual conversation scores are useful for evaluating specific interactions. That's what's needed for debugging, but it doesn't scale as an AI product grows in usage. If you have tens of thousands of conversations a day, you need to aggregate patterns to find critical issues without spending all day reviewing eval scores.
