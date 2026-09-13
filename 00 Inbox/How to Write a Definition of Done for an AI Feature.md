---
type: article
status: inbox
quality: 
topics: []
source: https://jeffgothelf.com/blog/how-to-write-a-definition-of-done-for-an-ai-feature/
created: 2026-09-13
published: 2026-09-07
author: Jeff Gothelf
flashcards: none
updated: 2026-09-13
---

# How to write a definition of done for an AI feature

<div align="center">
  <img src="https://i0.wp.com/jeffgothelf.com/wp-content/uploads/2026/09/ai_definition_of_done_illustration.png?fit=1200%2C896&quality=80&ssl=1" width="220" />
</div>


![](https://i0.wp.com/jeffgothelf.com/wp-content/uploads/2026/09/ai_definition_of_done_illustration.png?w=1200&quality=80&ssl=1)

- Product managers are being pushed to redefine what a PRD is in the AI era. Consensus seems to be growing that [evals](https://www.producttalk.org/ai-evals/) are the new PRD
- He’s quoted in the Braintrust piece as saying, “*Writing evals is the most important thing a PM can do in the AI era.*” This makes sense. Trying to predict the right requirements in advance for a system that delivers different outputs per user, prompt and model in a PRD is nearly impossible. Evals, however, can do this and should
- I do want to cover what should be attached to that eval suite to ensure that we don’t lose the customer in the conversation and, in turn, build more useful AI customer experiences

##### Why an eval is a definition of done and not a product spec

- Evals are tests with pass/fail criteria. This makes them an excellent part of the definition of done conversation. They are executable, run each time you commit new code, catch any regression issues and help settle quality arguments with data rather than opinion. Every one of those properties, though, focuses on the system’s behaviour. None of them is about the customer using that system.
- An eval suite scoring 94% tells you the feature behaves the way you specified 94% of the time. What it doesn’t tell you is whether anybody wants the feature or if the workflow to get to that part of the user experience improved or if the person paying for your service is spending more or less on average and why.
- Eval scores, ultimately, are an output. Or, at least, passing your evals is an output. It’s a feature of a system that is behaving more predictably and on brand. It’s still not measuring whether you’re delivering value or helping your customers make sure they have everything they need

##### What to attach to your eval suite before you call an AI feature done

- So, how do we take the very useful eval suite you created and ensure it gives us a complete picture of “done” for our AI features?
- • **The specific eval compliance score you will tolerate**. This is more than just “the eval passes.” It’s a specific, written score that we agree is required to ship. • **The outcome the feature is supposed to move**. Add at least one sentence to each eval that names a specific customer behavior you expect your customers to be doing differently. Without this, the eval is measuring the quality of something that doesn’t necessarily add any value to the end user. • **The person that will fix the eval/outcome failure**. Name a specific individual who will take a look at why the bot isn’t hitting both its eval targets and its outcome goals and determine who should work on the fix. It may be a model issue, a ux issue or content problem. Put someone in the position to route those concerns properly. • **The date the eval set gets refreshed from production**. The eval dataset along with the desired outcomes reflect what you thought users would do. Live systems reflect what they actually do. Be clear when the data coming in from production will be used to update the existing eval and outcome set.
- **adding in the user outcome** that makes this a product-ready definition of done
