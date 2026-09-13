---
type: article
status: inbox
quality: 
topics: []
source: https://www.lennysnewsletter.com/p/how-to-turn-your-ai-into-a-world
created: 2026-09-13
published: 2026-09-01
author: Anshu Chimala
flashcards: none
updated: 2026-09-13
---

# How to turn your AI into a world-class designer

<div align="center">
  <img src="https://substackcdn.com/image/fetch/$s_!IeM-!,w_1200,h_675,c_fill,f_jpg,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdf93abba-682d-446b-a21a-5ad935867a1f_1456x970.png" width="220" />
</div>

- AI models are capable of amazing creativity, but that creativity gets stifled by how they’re trained.
- teaches the model to make consistent, safe choices that fit everyone’s preferences.
- This makes typical LLMs great at most tasks but poor designers. To create a design, an LLM has to build it out token by token.
- Great design, on the other hand, starts with feeling and aims to create an emotional response.

## Discover: Explore the space of possibilities

- hardest part of the design process is looking at a blank screen with infinite possibilities. The best way to tackle that moment is to start by going broad before going deep.
- To explore the full potential design space, we want to coax a model to do the opposite: be bold, be varied, and take risks.
- two ways to push it out of its comfort zone.

### Technique 1: Use seed strings to inject variety

- As a simple example, I gave four instances of Claude Code the same prompt:
- Build me a landing page for my productivity app.
- Almost every time, we get a purplish gradient, text on the left, graphic on the right, and the exact same structure. It looks like every AI-designed website ever.
- just asking for variety doesn’t work:
- Build me a landing page for my productivity app. Give me something totally unique. Make every design decision completely at random.
- One technique for this is String Seed of Thought, [published by Sakana AI](https://pub.sakana.ai/ssot/).
- *I want you to build me a landing page for my productivity app.* *Follow this procedure:* 1. *Generate a long, random alphanumeric string using a shell script.* 2. *Define the creative direction (color scheme, layout, typography, etc.) based on the string. Look beyond the surface for subpatterns, special numbers, anything that inspires you.* 3. *Use your judgment to bring this direction to life and make it look great.* *Don’t reveal the string in the design. It’s only for your inspiration.*
- Suddenly the outputs are much more varied!

### Technique 2: Be much more ambitious with your prompts

- Another approach to giving a model a strong push is to get more specific and wild with your prompts.
- some examples:
- “Build me a landing page for my productivity app, with a bold pixel art theme and stunning graphics. Each section should feel like a still from a video game, yet somehow it should all function as a landing page.”
- “Build me a landing page for my productivity app, set in an isometric living 3D city, where different features are somehow represented by neighborhoods or buildings.”
- “Build me a landing page for my productivity app, with a radically asymmetric layout, dissonant colors and typography, and uncomfortable negative space. Break all the rules but still make it look good.”
- Here’s a system I use to find unique prompt ideas with AI:

##### 1. Ask AI to list a bunch of ideas, intentionally lacking detail. The goal is just to inspire your imagination.

- I want to come up with a bold, unique design language for my product. Can you list as many ideas as you can, with short, high-level descriptions? Go broad, not deep.

##### 2. Visualize your favorites and note how you react to different directions. Then ask AI to refine them.

- • *I’m imagining something tactile. Clicky, satisfying buttons, nice sounds.* • *Initially I pictured something cartoony or skeuomorphic, but this feels tacky to me. Avoid that.* • *Instead, want consistent components and little touches that land this look without going overboard.* • *Gray gradients would look boring. Need more texture. Maybe we can incorporate some color, while retaining the control panel feel?* *Can you sharpen this one based on my tastes?*

##### 3. Iterate until you’re satisfied, then ask AI to write the prompt to build it.

- Can you write a concise prompt that an AI agent could use to build an initial POC page with this?
- when you actively steer the design direction, you end up with something only you could have created.

## Define: Deepen your design direction

- Our next goal is to give each design an individual personality through distinct design choices. Below are my favorite techniques to do that.

### Technique 3: Create positive feedback loops with subagents

- We need to iterate on our designs to improve them.
- simply asking our agent to look at the design and improve it won’t work, because the agent isn’t objective: it reviews its own code, past decisions, and previous rationale. AI can’t easily zoom out, look at the big picture, and “think different.”
- have it ask *another* agent—a “design critic.”
- can use a big, expensive model for the critic without breaking the bank, because we’ll only use it for executive decisions. A cheap, fast model can do the grunt work, while the strong critic model provides taste.
- *I want you to improve this design. To figure out what to focus on, use a Fable 5 subagent as a design critic.* *Follow this procedure at each iteration:*
    - *Capture a screenshot of the current design*
    - *Invoke the critic in a fresh context, with just the screenshot, not the code, implementation details, or earlier iterations/critiques*
    - *Ask it to evaluate the aesthetic that the design is going for, imagine how a top design studio would execute this aesthetic, then outline the biggest gaps*
    - *Lastly, it should provide a score out of 10 indicating how close the current design is to that studio-level quality bar* *Provide this guidance to the critic in its prompt:*
    - *It should think high-level about the overall structure and composition as well as look at the fine details*
    - *It should watch out for patterns that feel overdone, excessive, or otherwise obviously AI-generated, and penalize them*
    - *It should provide tight, specific feedback, not vague prose*
    - *It should be bold and opinionated, not rely on what’s safe or easy* *Your work is only complete when the critic independently deems it 9/10 or higher. Do not put that criterion in the critic prompt; keep it objective in its scoring. Use the same critic prompt each time.*
- The way you set these loops up matters a lot. Here are some tips:
- **Make sure the criteria for the critic are as clear and objective as possible.**
    - Bad: “Judge if our design looks beautiful, not AI-generated.” This is too subjective, and the results will vary wildly from run to run.
    - OK: “Review the aesthetic we’re going for, visualize how a top design studio would execute it, then judge our design’s quality against that bar.” The prompt is still mushy, but it provides a consistent framework and quality bar.
    - Great: “Here are 5 designs: 4 professional examples and 1 screenshot of our product. Rank them by polish and taste level.” This instruction is concrete and objective, and gives a visual baseline for judgment.
- **Provide example images to demonstrate the target quality bar.** You can use comparable screenshots or designs you like, or even AI-generated concept art. Instruct the critic to treat these as a baseline or a moodboard, not a target. You don’t want it to copy other designs outright.
- **Set the stopping criteria carefully.** Otherwise, the critic may never consider the design good enough, and your agent will helplessly burn tokens trying to please it. Prompt it to do one or two iterations first, and see if it’s converging before adding more.
- **Choose the right model for each job.** Consider bigger models for the critic role, since more parameters generally translate to better design sense and a wider distribution of ideas. Small models can be effective as the implementer, but don’t go too small. You still need a model that’s capable of executing a design direction well.

## Deliver: Polish your design into something users will love


### Technique 6: Cut out elements that don’t add value

- When polishing AI designs, most of my effort goes into removing things.
- However, despite my asking for minimalism, a lot in the design wasn’t adding value
