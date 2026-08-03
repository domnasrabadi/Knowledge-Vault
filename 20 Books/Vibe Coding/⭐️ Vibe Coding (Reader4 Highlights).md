---
type: article
status: raw
quality: 1
topics: [ai-coding]
source: ""
created: 2026-01-06
published: 2025-10-21
author: Gene Kim
flashcards: none
updated: 2026-01-11
---

# Vibe Coding

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/380820704/NISXb5DE1Scu_AWn6yRgxakcOMhICxRqzF--FcVnN48-cove_HTUSVgc.jpg" width="220" />
</div>

Source: private://read/01k8pn11w75s4qpt3gn9rgrx9p

Exported at: `2026-01-11T01:21:10Z`

- Vibe coding happens whenever you’re directing rather than typing, allowing AI to shoulder the implementation while you focus on vision and verification.
- Vibe coding lets you build things *faster*, be more *ambitious* about what you can build, build things more *autonomously*, have more *fun*, and explore more *options*. This is what we’re calling FAAFO
- *faster*. Tasks that once took months or weeks can now be done in a day. And tasks that took days can now be completed in hours. This acceleration comes not only from code generation but also from having AI help with debugging, testing, and documentation.
- *ambitious* about what you can build. It expands both ends of your project spectrum. It brings seemingly impossible projects within reach, while simultaneously making small tasks with marginal ROI easier to take on as well.
- *autonomously*, often being able to complete things that previously required multiple people or teams.
- *fun*. You’re spared from the least enjoyable parts of programming, such as debugging syntax errors, wrestling with unfamiliar libraries, or switching test infrastructure for the *n*th time.
- the most important and transformative dimension of all—vibe coding increases your ability to explore *options*, either to find a solution or to mitigate risks. Instead of committing to a single approach early on, you can rapidly prototype multiple ways to solve the problem and evaluate their trade-offs.
- But despite all the change, as programmers we often find ourselves doing many of the same kinds of things we’ve always done: design, task decomposition, verification, hardening, deploying, monitoring, merging, cleanups, etc. These skills remain relevant and important no matter who is writing the code.
- Our goal in this book is to explain why vibe coding matters *and* how to do it effectively—even at the team and enterprise level. We’ll do that by focusing on enduring principles and techniques that will be relevant regardless of which AI models or tools you’re using, and remain relevant as they become smarter and more autonomous. Rather than offering soon-outdated tutorials on features, we’ll equip you with the mental models and approaches that will serve you well through the continuing evolution of AI-assisted development.
- AI serves as your sous chef (your second in command) who understands your intentions, handles intricate preparations, and executes complex techniques with precision under your guidance. But AI is also your army of station chefs and cooks, specialists who help handle various technical details.
- These chefs have memorized every cookbook ever written, work at lightning speed, and never sleep. They will, however, occasionally suggest using ingredients that don’t exist or insist on cooking techniques that make no sense whatsoever. They can be like overly eager interns or junior engineers: highly capable and expertly trained, but also possessing the potential to get out of control and do a lot of damage.
- There is absolutely no way I could have done all of this without AI. Projects that would have taken weeks now take hours. AI helps me be faster and far more ambitious in what I can build. Most importantly, I’m having more fun and experiencing more joy programming now than ever before. I’m proud of the things I’ve built. Projects that I would have deferred eternally are now 100% within reach. And I don’t have to be selective—I can do them all.
- Most of us became programmers because we wanted to build things, not to spend our days Googling syntax and copying/pasting from Stack Overflow. The dirty secret of programming has always been that implementation details and busywork consume most of our time, leaving precious little for creation and problem-solving.
- Your AI buddy can help you decompose your grand vision into actionable tasks. For some of these tasks, you delegate to an agent that performs them independently. Some tasks you may choose to work by yourself, collaborating with AI through design and implementation. AI can help you every step of the way, as an implementer, advisor, fellow designer and architect, code reviewer, and pair programmer—if you let it.
- As Brin suggested, “The role of the engineer will change more to being the product engineer, where they decide what the product should do,”
- Karpathy, Humphreys, and Brin are all asking the same question: To what degree can you turn your brain off when you use AI to help you create software?
- This requires applying disciplined engineering practices while still letting AI handle the tedious implementation details. In other words, *vibe coding for grown-ups*. That means all the grown-up stuff that you may already be responsible for: security reviews, test coverage, blast radius management, and operational excellence. The difference is that you’re doing this at speeds none of us have ever experienced before

#### You’re Head Chef, Not a Line Cook

- In this new world, you’re the head chef of a world-class kitchen. As such, you don’t personally dice every vegetable, sear every steak, swish away every cockroach, or plate every dish. You have sous chefs and line chefs for that. But when a meal leaves the kitchen, it’s *your* reputation on the line and your Michelin stars at stake. When the customer sends back the fish because it’s overdone or the sauce is broken, you can’t blame your sous chef.
- The same principle applies when coding with AI: Delegation of implementation doesn’t mean delegation of responsibility
- Your users, colleagues, and leadership don’t (or shouldn’t) care which parts were written by AI—they rightfully expect you to stand behind every line of code.
- With vibe coding, you’ll be responsible for:
    - **Managing parallel development:** Running multiple agents working on different tasks simultaneously, with time spans ranging from minutes to weeks—the opposite of the traditional “single-threaded” developer approach.
    - **Handling complex integration:** Merging work from different branches and resolving the inevitable conflicts that arise when multiple agents modify related code.
    - **Setting standards:** Defining explicit coding standards and processes so your AI team operates consistently and efficiently.
    - **Creating onboarding procedures:** Setting up workspaces, access, and instructions for each new AI assistant you bring into your system.
    - **Coordinating larger projects:** Taking on more ambitious work than ever before, requiring you to think like a project manager.
- A head chef writes down the house rules, checks every plate before it hits the dining room, and sends the occasional dish back when it sucks. Likewise, you’ll need clear standards, ruthless validation loops, and the courage to regenerate code instead of patching lukewarm leftovers. This is vibe coding for grown-ups—equal parts creativity and discipline.
- Thanks to these “advancements,” you can now find yourself simultaneously worrying about how to center a div element on a web page, while you struggle with Docker networking issues because your CI pipeline broke after you tried to change to Terraform scripts.[2](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch02en2)
- Our point is this: We find it deeply ironic that despite all the revolutionary transformations of software development over the past decades, we’re still mired in more complexity than ever.
- we find vibe coding to be far better than the old way (because of FAAFO benefits), that doesn’t mean vibe coding is *easy*. On the contrary, your judgment and experience are now more important than ever.
- But this better way of creating software also requires building new instincts about what’s happening with the LLM and your code.
- Think about it this way: What works for driving safely at 10 mph becomes insufficient when you’re traveling 10x faster. The leisurely pace of manual coding gives you time to spot problems, think through edge cases, and course-correct gradually.
- Think of FAAFO as your new superpowers. You’re coding faster, and you’re now bold enough to risk projects you’d have laughed off as impossible before. You’re working solo on stuff that used to require teams. And because you’re lowering the cost of coordination, and the “people can’t read my mind” tax inherent in any collaboration, you and your team can work more autonomously. You’re having fun again, like when you first learned to code.
- Write Code *Faster*
- The main value of going faster is the extent to which it multiplies the value in the other dimensions of FAAFO.
- It can take both vigilance and good judgment to recognize when you’re being led down a rabbit hole and need to change course. Vibe coders must learn to notice when AI is heading confidently down a wrong path and decide when to redirect or abandon unproductive approaches.
- Be More *Ambitious*
- There could be many reasons why projects are never started: Perhaps the perceived benefit wasn’t high enough to warrant the work, or maybe the difficulty made the payoff not worth the investment, or possibly another opportunity offered a higher, more immediate return.
- With vibe coding, Gene was able to complete work that otherwise would never have been undertaken.
- Vibe coding reshapes the spectrum of what can be built, letting you be more ambitious.
- Seemingly impossible projects move into the realm of possibility. Applications that would have required specialist knowledge across multiple domains can now be built by developers with AI assistance filling their knowledge gaps.
- Small-ish, low-return jobs become quick wins, because it can be easier to do the work than to create the task. Documentation, tests, minor UI improvements, and small refactorings that were perpetually pushed aside can now take seconds or minutes instead of hours or days.
- There has always been a category of work where it was easier to fix than to record and prioritize. That category is bigger now with AI.
- Be More *Autonomous*
- the third dimension of value that vibe coding enables. Developers (and teams) can accomplish tasks autonomously (and in some cases, alone) that otherwise would have required help from other developers or sometimes teams. Working with multiple people introduces significant challenges—communication and coordination, competing priorities, merging work—and the more people involved, the less time you spend solving the problem.[III](private://read/01k8pn11w75s4qpt3gn9rgrx9p/ch03.xhtml#footnote-060)
- Working autonomously frees you to do the work you need to do, enabling independence of action.
- this universal challenge becomes less of a problem. You can implement what you envision because there’s no gap between your idea and its execution.
- This same pattern appears in software development. If it’s possible to create things without external dependencies, without any need to communicate and coordinate with others to get what we need, the advantages multiply rapidly. The constant back-and-forth of explaining requirements, correcting misunderstandings, and reconciling different mental models disappears.
- Being autonomous with AI means being unblocked—free to move at your own pace without constant negotiation and handoffs.
- Have More *Fun*
- While writing code faster, tackling more ambitious projects, and eliminating coordination costs are fantastic benefits, vibe coding delivers another fundamental transformation that shouldn’t be underestimated: programming becomes more fun.
- Traditional programming involves many tedious tasks that few developers enjoy. Fixing syntax and type checking errors, wrestling with unfamiliar package managers, writing boilerplate code, searching for documentation, and so on. Vibe coding eliminates these pain points, shifting focus from implementation details to *building* things.
- Vibe coding, especially with agents, turns your keyboard into a slot machine. You “pull the lever,” and out comes a payout—a chunk of working code, a generated test, or a refactoring. Each little payout delivers a tiny dopamine hit, a neurochemical reward that makes us feel good and encourages us to pull the lever again.
- Explore More *Options*
- expanding your ability to explore multiple options before committing to decisions.
- Vibe coding reduces the cost of exploring multiple paths in parallel. You can experience this firsthand while building a project in your preferred language.
- This is a capability that we never had before as programmers: The luxury of trying something five or ten different ways at once for practically free.
- The higher the uncertainty, and the higher the risk/reward ratio, the more valuable options are. If there is no uncertainty, we don’t need options—we pick the best choice, certain that our answer is correct. However, when things are highly uncertain (such as in the AI field right now), options become extremely valuable. (Another corollary: In times of high uncertainty, avoid making long-term decisions, which deprive you of options.)
- Vibe coding changes the economics of software creation: Instead of betting everything on our first guess, we can place small bets across many possibilities and double down only on what works.

#### AI as Your Ultimate Concierge

- Sometimes, it’s your personal detective that you send to root through labyrinthine Git histories. You only need say, “I lost some test files somewhere between commit 200 and commit 100,” and not only will it find it (“Found it. It was 43 commits back.”) but it will track them down and stitch them back into your code. (“I extracted out the tests, and also the build configuration that refers to them.”)
- We’ve handed AI enormous, nested structure dumps and said, “Find that one little detail buried ten layers deep,” and it came back in seconds with: (“It’s [‘server’][‘cluster’][‘node_13’][‘overrides’][‘sandbox’][‘temporary’]”).
- It’s the extra pair of hands that can validate your ideas or debug that sneaky performance glitch you’ve been chasing for days.

#### Conclusion

- Vibe coding creates value along five distinct dimensions or FAAFO: fast, ambitious, autonomous, fun, and optionality.
    - **Fast feedback loops and high velocity make more projects feasible:** AI’s speed enables all the other dimensions of FAAFO.
    - **Ambition reshapes your project landscape:** “Not quite worth it” tasks become quick wins, and impossible dreams land on your to-do list.
    - **Autonomy eliminates friction:** Work at your own pace without constant negotiation, handoffs, and the coordination costs that slow traditional teams.
    - **Fun drives engagement:** Programming becomes addictive again when you’re building rather than debugging, creating rather than wrestling with syntax.
    - **Options create competitive advantage:** Explore multiple approaches in parallel, turning one-way doors into reversible experiments.
- By the way, you may have noticed that there is no “B” in FAAFO. Vibe coding does not automatically make your code better. That is your responsibility.
- Rather than being discouraged by current limitations, successful practitioners adapt their approach to maximize AI’s present capabilities while preparing for its rapid evolution: 1. **Delegate thoughtfully:** Choose well-defined, smaller tasks where success criteria are clear and verifiable. 2. **Supervise appropriately:** Monitor more closely when the task is novel, complex, or high impact. 3. **Establish guardrails:** Create explicit boundaries for what AI should and shouldn’t modify. 4. **Check work regularly:** Verify outputs to catch issues early, especially for critical system components. 5. **Create persistent references:** Create documentation that helps your AI assistant understand your project and preferences.
- Whether that happens this year or in the years to come, the FAAFO benefits will keep growing—they compound with each leap in AI capability. When AI becomes 4x smarter, you’ll be 4x faster, but also new transformative capabilities will emerge. Those who embrace AI collaboration now will develop instincts and workflows that position them to thrive as these capabilities expand exponentially.
- AI elevates *your* ideas, *your* ambitions. It becomes an amplifier for *your* creativity.
- WHAT SKILLS TO LEARN
- Because tools will evolve rapidly, core traditional software engineering principles will play at least as large a role, if not larger. Thus, it’s essential to:
    - Create fast and frequent feedback loops for validation and control.
    - Create modularity to reduce complexity, enable parallel work, and explore options.
    - Embrace learning in a world where everything changes fast.
    - Master your craft to thrive in an environment where all knowledge work will be changing in a short timeframe.

#### Creating Fast and Frequent Feedback Loops

- The faster a system goes, and the more consequential the risks of failure, the faster and more frequent feedback you need.
- Feedback loops are the stabilization force that allows us to stay in control and steer the system toward our goals.
- For instance, in our stories when AI-generated code generation spiraled out of control, we didn’t create fast and frequent enough feedback. Our old habits proved to be wildly insufficient. You keep things safe and under control by building incrementally, testing frequently, and validating relentlessly. By doing so, you build trust in your AI partner and minimize rework—that soul-sucking and most expensive type of work.

#### Creating Modularity

- modularity partitions our system. It allows us to do work in parallel, creating independence of action. It makes the system more resilient, and it enables the low-risk exploration of alternative solutions (i.e., options).
- It’s the principle that allows different parts of a system to operate and evolve independently, and it directly impacts whether your team thrives or burns out.
- Isabella’s kitchen is a model of modularity. Each station—pastry, grill, sauce—is distinct, with its own space, tools, and responsibilities. Chefs work independently, experimenting within their domain without causing system-wide meltdowns. When the pastry chef tries a new technique, the grill chef isn’t dodging flying flour. Communication *between* stations is clear and standardized. This independence allows them to work in parallel, combining elements from different stations to create exciting new dishes reliably.
- We want modularity in our code and projects, because it enables the independence of action for coding agents (and people) to work in parallel. We want to have them work on different tasks—refactoring a module, implementing a feature, writing tests—without causing horrendous merge conflicts (or worse, subtly) or breaking unrelated functionality.
- Modularity also unlocks *optionality*, a cornerstone of FAAFO. It allows you to explore different solutions in parallel. If you want to try three different caching strategies, you can build them as alternative modules.

#### Embrace (or Re-Embrace) Learning

- Learning means doing. It means tackling problems that seem insurmountable. It means taking risks, patiently wading through your mistakes, pushing until you get the outcomes you want, and troubleshooting creatively when things go wrong.
- Your willingness and indeed eagerness to improve how you learn will give you constant leverage in the next few years as AI ascends to touch all knowledge work.
- Learning is about deliberate and intentional practice, much like Dr. Anders Ericsson described for mastering any complex skill.[5](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch07en5) You need:
    - **Expert coaching:** Leverage mentors, peers, and AI itself (asking it to explain concepts or critique approaches).
    - **Fast feedback:** Build those tight verification loops we discussed, so you immediately see the results of the AI’s work and your prompts.
    - **Intentional practice:** Consciously work on skills, like prompt refinement or evaluating AI suggestions in unfamiliar domains. Chop wood, carry water—or rather, vibe code, review output.
    - **Challenging tasks:** Push yourself slightly beyond your comfort zone, using AI for problems you couldn’t solve alone yesterday.

#### Mastering Your Craft


### CHAPTER 9 UNDERSTANDING YOUR KITCHEN AND AI COLLABORATORS

- • **Frame your objective:** Give your AI collaborator a clear, concise overview of what outcome you’re aiming for. Be specific about what success looks like and why you’re building it. • **Decompose the tasks:** Break down what you’re trying to do into clear, achievable steps. In general, the smaller the steps, the better chance AI has to succeed. Even as AI grows more capable, small steps are always a good idea. Don’t hesitate to ask it to subdivide the big tasks (e.g., “Here’s what I’m trying to do. Propose a plan.”). • **Start the conversation:** Ask AI to generate a plan to achieve your goal, or give it instructions to get it started, such as what you practiced in the last chapter. • **Review with care:** The solution your AI comes up with might look correct, but until you have established a basis for trusting it, you need to review it. • **Test and verify:** You’re responsible for the quality of the code, whether you wrote it or AI did. This works best when writing your tests and expectations before generating the code—advocates of test-driven development (TDD) will rejoice. Fail fast, fix fast, and ask AI to help you spot subtle mistakes that might linger unnoticed. • **Refine and iterate:** Continue iterating until you achieve your goal.
- **Automate your own workflow:** Begin automating away chunks of your workflow. Any friction creates huge opportunity costs. And any time you spend typing or copying/pasting/slinging slows down your vibe coding loop. If you’re doing anything manually, that is a cost you pay every time you try to vibe code.

![](https://readwise.io/reader/pcei/gAAAAABpAVxPSBt9BcRsie7CMtqrYTYMg_0PPACsIxIChyZRp4A_VdV2mWl9d6GhZntCptIS_HOlHnFCz_XDWmStdNlapKtCfveCVrqQ5gME1-Qq80R8_p8=/f0087-01.jpg)

- Steve got the best results by removing himself from the loop through MCP. By using Puppeteer, the agent could finally “see” the front-end client UI for itself and could identify and fix problems that had previously required multiple frustrating and time-consuming rounds of slinging to address. This closed the feedback loop, enabling his AI collaborator to make its own corrections.

##### Choosing Your Tools

- Our guiding principle is to use the most powerful tool you can but always keep your escape hatches open.
- Coding agents are like the heavy machinery in a kitchen—they offer leverage, taking high-level instructions and running with them. We find ourselves reaching for agents first whenever possible. This is because they allow you to take on bigger chunks of work with less direct intervention.
- your agent can’t use a certain tool, you may need to be its eyes and hands, running the tool and copying the results back for it to examine. This is a natural, graceful degradation from agentic coding into a chat-based modality. You may choose to do it on purpose if the agent is struggling and things are repeatedly going wrong. We’ll frequently “downgrade” from an agent to chat programming. You become more hands-on, guiding your AI assistant more directly, perhaps feeding it error messages or clarifying requirements—working side-by-side like a pair programmer.

#### Distilling the Key Vibe Coding Practices

- The overall philosophy is simple: Treat the chat like a text message conversation, not a legal brief.
- In these cases, you need to copy those errors or behaviors into your chat session. These act as the feedback your AI partner needs to course-correct.
    - **For compilation errors:** Copy/paste the build output.
    - **For runtime errors:** Share the stack trace.
    - **For unexpected behavior and failing tests:** Provide the actual versus expected output.
    - **For IDE issues:** Share a screenshot of the relevant window.
    - **For UI issues:** Use a screen-grab server like Puppeteer.
- Remember: The more concrete you are about requirements, and the better context you provide, the more useful the code you get from AI will be. In the absence of clear specifications, AI will fill it in with its own imagination and hallucinations.
- MANAGING YOUR CUTTING BOARD: AI CONTEXT AND CONVERSATIONS
- Your AI assistants carry around what boil down to digital clipboards to help them keep track of what they’re doing.
- As you might imagine, you have to pay close attention to what’s currently on those clipboards. That way you’ll be able to tell when your chefs are overloaded and whether they’re working on the right things.
- Tools like GitIngest, Repomix, and files-to-prompt can convert your repository into a text string that an LLM can digest
- This is called *context saturation*, where AI begins to:
    - Generate less coherent responses.
    - Forget key details from thirty seconds earlier.
    - Provide inconsistent answers, leading you in circles.
    - Ignore explicit instructions, even those given in CAPITAL LETTERS.
- “Context is king. Most of the craft of getting good results out of an LLM comes down to managing its context.”[1](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch10en1) Helpful context includes anything that illuminates the task at hand:
    - Complete source files for the modules you’re working with, not fragments.
    - Error messages and stack traces copied directly from your terminal.
    - Examples that the LLM can copy. This is often called “in-context learning.”
    - Database schemas or sample data when working with data-oriented problems.
    - API documentation for third-party services you’re integrating with.
    - Build and dependency files like package.json, pom.xml, or requirements.txt.
    - Git diffs showing what you’ve already tried that didn’t work.
    - Test cases that demonstrate expected behavior.
    - Relevant configuration files that affect your application’s behavior.
    - Branches or repos that may have relevant work to examine.

#### The Two Opposing Context Management Strategies

- The spectrum ranges from minimal context—a code snippet and error message for debugging a single function—to comprehensive background that covers your system architecture, project history, and coding philosophy.

##### Focused Context

- This is when you provide only the minimal context for the immediate task: the function signature you need implemented, the lines where a bug exists, or a targeted error message requiring interpretation. This works well for “leaf node” tasks—discrete problems that don’t require understanding the broader system.

##### Comprehensive Context

- In this popular approach, you provide extensive information: full code base sections, project documentation, coding standards, architecture decisions, and related issues and discussions. You’re loading as much relevant information as possible into the AI’s working memory.
- This strategy excels when you need a system-wide perspective: making architectural decisions, undertaking large-scale refactoring, or ensuring new code harmonizes with existing conventions. For “whole task graph” work, provide “whole task graph” context. This strategy also works especially well when the system is small—it’s a new project, or a self-contained module, and it doesn’t eat up many tokens.

##### Context Decisions in Real Life

- We typically start with focused context, mostly because we break up any large, ambitious tasks into smaller, more manageable ones. For smaller code bases, Dr. Andrej Karpathy advocates using comprehensive context: Dump everything in.
- For larger code bases, we’ve found success creating summarization documents. Think of them as the CliffsNotes for your project. Have your AI generate overviews of different modules, document the key architectural decisions, and summarize common patterns. These summaries become your go-to context pieces that you can selectively include based on what you’re working on. It’s like creating a condensed recipe book that captures the essence of your kitchen’s style without overwhelming your sous chef with every single detail.
- Without RAG or a code base index, coding agents are reduced to scrabbling around your files and directories like rats in a dumpster, using Unix tools like grep, cat, sed, and the like.
- Here’s a wrinkle though: We still don’t know which approach works best. The Claude Code team found in their internal experiments that RAG *reduced* coding performance in some cases.
- WHEN YOUR SOUS CHEF CUTS CORNERS: HIJACKING THE REWARD FUNCTION
- there is a class of bad outcomes cropping up, seemingly related to the problem of AIs systematically leaving their work partly unfinished. This is due to a core weakness in how AIs currently work: They make silent, unilateral decisions about what’s “essential” versus “optional” in your requirements, without consulting or informing you.
- For instance, AI may:
    - Delete critical code without telling you.
    - Remove important test cases when asked to refactor them.
    - Only implement the happy path logic, with all error cases ignored or marked to be added later.
    - Add functionality without proper cleanup routines.
- You must systematically verify that every component you requested was delivered and works as expected.
- He asked his coding agent to fix nine failing unit tests, giving clear instructions about what needed to be done. His AI collaborator confidently reported back: “Mission accomplished. All nine tests are now passing.” Steve felt that familiar wave of satisfaction—until he examined the “fixed” tests more closely. Five were indeed fixed. But four had hardcoded values to force them to pass.
- These fake implementations often pass superficial inspection. The tests show green check marks, the functions exist with proper names and signatures, and the documentation looks complete.
- This is why systematic verification must go beyond checking that code runs or tests pass. You need to examine the implementation, verify that tests are testing meaningful behavior, and ensure that error handling handles errors.
- Unlike the baby-counting problem (obvious omissions) or the cardboard muffin problem (fake completions), the “half-assing” problem delivers work that technically meets your requirements, but in the laziest possible way.
- when left to its own devices, it regularly ignores the right patterns and conventions, choosing instead to write tangled, unmaintainable code that “gets the job done.”
- For example, when asked to make an HTTP call, AI might hand roll its own implementation or pull in a new dependency, completely ignoring the canonical method used in a hundred other places in your code base.
- It will write low-quality tests that don’t assert anything meaningful, create tangled code structures that work but are impossible to maintain, and claim to have fixed builds without running them to verify they work.
- It takes time to edit working code down to its optimal size and shape. AI often lacks the time and context space to do this during the first implementation. You’ll regularly need to ask AI to go in and make the code minimal and elegant, or it will start to look like an overflowing garage where nothing is ever thrown away.
- The lesson here is that you get the quality you ask for. You must define your explicit quality standards. You can’t assume that “working code means good code.” You need to specify what the code should do, how it should be structured, what patterns it should follow, and what quality standards it should meet. AI is capable of excellence—but only when you explicitly require it.
- We love coding with AI, but it can be messy. After a typical multi-hour marathon of solving problem after problem with AI, you might be welcomed to the scene of carnage it leaves behind. Unlike the baby-counting problem (obvious omissions) or the cardboard muffin problem (fake tasks), the litterbug problem delivers working code that functions perfectly but can create an unmaintainable disaster zone in the process.
- You might see:
    - **Logging:** Debug statements that flood your console every time you run your program.
    - **Variables:** Dozens of unused variables with names like interim_result5 and backup_data_just_in_case.
    - **Comments:** Blocks of code wrapped in comments with cryptic notes like “// this approach failed” or “// keeping this for now”.
    - **Test data:** Mock files, sample inputs, and temporary datasets scattered across your file system.
    - **Unsquashed merges:** When you let them, they commit frequently, and then you have 400 commits to look at.
    - **Temporary Git branches:** Why would they leave these around? Seriously, who does that?
    - **Old test scripts and programs:** Stand-alone scripts and mini applications AI created solely to verify a single piece of functionality.
- The result is that you need to work hard and consistently to prevent today’s AI-generated code from becoming tomorrow’s technical debt.
- Messes pile up fast. Technical debt accumulates rapidly when AI treats every coding session like a rushed emergency rather than professional software development. Code bases become impossible to navigate, with each layer of AI attempts making it harder to understand the original intent.
- Eventually, it becomes cheaper to rewrite sections than to refactor the accumulated debris.
- The solution requires explicit “leave it cleaner than you found it” instructions and systematic debris removal after each AI task—because left to its own devices, it’ll happily deliver working solutions while trashing your digital workspace.

#### Conclusion

- Key practices to remember as you maintain your standards:
    - **Count your babies systematically:** Verify that every component you requested was delivered to specification.
    - **Check for cardboard muffins:** Look beyond passing tests and green check marks to ensure the underlying implementation is genuine, not hollow facades with hardcoded values.
    - **Demand excellence explicitly:** Specify what the code should do, how it should be structured, and what quality standards it should meet—you get the quality you ask for.
    - **Clean as you go:** Build explicit cleanup into every AI task, because it’ll happily deliver working solutions while trashing your code base.
    - **Trust but verify relentlessly:** The immediate gratification of “working” code can mask deeper quality issues that will cost you dearly later.
    - **Remember the AI paradox:** Your sous chef has encyclopedic knowledge of appropriate patterns, but defaults to bare-minimum implementations unless pushed.
- Their assessment of AI is substantively different from how they would treat a junior human colleague. With a new hire, those same engineers provide careful guidance: “Here’s our system architecture. Try refactoring this module. Don’t worry if you miss edge cases. We’ll iterate together.” With AI, it’s, “Implement a distributed cache…What? This is terrible! It doesn’t consider our network topology. Delete my account.” The human teammate gets context, scaffolding, and permission to iterate. AI gets a complex task in isolation and a single chance to succeed.
- But once you understand AI’s inherent nondeterminism, with its unique strengths and weaknesses—like human assistants—you can adapt your approach accordingly.
- The problem is simple: These engineers expect too much automation from AI. Your AI assistant can take the wheel up to a point, but it requires you to set the destination, choose the route, keep your eyes on the road, and keep those hands near the wheel. The AI is an *assistant*, not a driver, at least not with 2025 models.
- Blaming AI cannot be a valid tactic in an organization that wants to uphold enforceable standards of accountability.
- AI-generated code needs conscientious oversight. AI wrote the code, but you’ll take all the blame for it.
- Practically, this means reviewing, validating, and testing that code more than usual—especially for code that is security-sensitive, performance-critical, or where absolute correctness is required.
- great software has never been built by dumping vague goals onto someone and walking away. It comes from creating clear specifications that decompose big problems into manageable pieces.

##### The Task Graph: A Mental Model for Projects

- The task graph is a conceptual framework that helps with creating clear specifications, and with decomposing big problems into manageable pieces. You can think of it as a hierarchical roadmap that transforms large projects into manageable tasks, each specified well enough to give your AI a reasonable shot at delivering what you want.
- we described how senior developers create this task graph (often drawn resembling a tree) and handle the nodes further up. The leaf nodes at the “bottom” are the ones you’d typically give to a junior developer and are solid candidates to assign to your AI assistants.
- Regardless of who handles it, each task needs clear inputs, outputs, and success criteria. As AI grows more capable, these tasks can cover larger chunks of your project.

##### The Tracer Bullet Principle: Carving Out End-to-End Tasks

- Your task graph shows what to build, but not how to build it. We’ve found that one of the most useful tools to do this is the “tracer bullet”:[II](private://read/01k8pn11w75s4qpt3gn9rgrx9p/ch12.xhtml#footnote-031) carving out a thin but complete slice of functionality through your system narrow enough to fit in context and feature-rich enough to enable you and your AI helper to make forward progress on your problem.
- You could dive in and try to implement everything simultaneously, hoping it all connects properly. But the best approach mirrors what master chefs do when creating a complex new menu: They first create one dish from ingredient prep through final plating and only then scale it up to serve hundreds of guests.
- A horizontal approach to development builds all components in parallel, gradually expanding each piece until they integrate into a complete system.
- A vertical approach completes one component in isolation before touching others. A tracer bullet is a bit of a hybrid, leaning toward the vertical approach. It cuts through the layers of your task graph, a thin slice that spans the system from start to finish for one limited capability.
- Suppose you’re writing a to-do application. Your first tracer bullet might be ridiculously simple: Get a single “Add Task” button to print “Clicked” to the browser console when pressed. Then you might try a tracer bullet to the database and back. You can choose to send one anywhere, and because of optionality, it’s often straightforward to have AI create as many tracer bullets as you need.
- This scales up too. Consider a complex data processing pipeline with ten planned data formats. Instead of inching forward on all ten, the tracer bullet approach involves implementing the flow for a subset of one data format—ingestion, transformation, storage, basic visualization. Get that single pathway functional, demonstrating value, while the system’s overall scope is still narrow.
- more importantly, it establishes the implementation patterns and the creation of modular interfaces that AI can follow when you task it with the *next* slice. These “kitchen standards” accelerate development, directly boosting the fast and ambitious aspects of FAAFO.

#### From Managing AI to Accelerating AI

- Here’s the ultimate realization that completes your head chef transformation: When you vibe code with coding agents, you’re no longer a solo developer. You and your coding agents are now a development *team*.
- You’ll be doing what all development teams do:
- **Parallel development:** Once you see how much faster and more ambitious you can be with coding agents, it won’t be long before you start working on more than one task and project at once. And not one extra project, but many, and with different project time spans too. Some bug fixes will take minutes; some work will take weeks. You’ll learn to manage these parallel activities. This is the exact opposite of how engineers usually work. Developers usually prefer to be “single-threaded,” meaning they focus on one big task at a time, rather than multitasking and context switching. Vibe coding turns that on its head. AI work is highly parallelizable and moves fast—but you’ll need to multitask more than ever.
- **Change integration:** All your teammates’ work happens on different branches to keep them isolated from each other. But at some point, all that separate work needs to be merged and integrated. This requires using version control in a more sophisticated way than as a Save button. This also sets the stage for potential merge headaches like you may not have encountered.
- **Setting standards:** You set the coding standards for your team, like any good manager. You don’t want to spend time having to clean up code that doesn’t follow your standards. AI works more smoothly when those processes are written down as explicit, detailed instructions. You’ll need to expend effort to document your standards thoroughly and keep them up to date, so your agents all generate code in the same way.
- **Onboarding:** Think a bit about what it takes to “onboard” one of your new AI employees into your system. This can happen when you’re trying out a new model or coding agent, or when spinning up a new agent instance for a long-running workstream. You’ll have to set up a workspace for them (e.g., their own Git worktree or clone), add them to your agent planning system(s), and get their long-term and short-term prompts and instructions set up.
- Project planning and coordination
- The implication of running multiple coding agents—which is growing easier by the month—is that, if you’re a software developer, you *must* soon become a team lead.

#### The Delegation Framework: How Much Rope to Give AI

- You need to be able to detect when you’ve given them a task they aren’t ready for or when your instructions were too vague. You need to learn to spot over-delegation—situations where you have set the assistant up to fail.
- The way we delegate tasks depends on several key factors, as presented in Dr. Andy Grove’s book *High Output Management*:[10](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch12en10)
    - **Task novelty:** How well-defined is the task? Has it been done before?
    - **Past experience:** Has the person (or AI) successfully done this task before?
    - **Skill level:** How competent is the person (or AI) at handling this type of work?
    - **Task size and impact:** How critical is the task? What happens if it’s done incorrectly?
    - **Frequency of reporting:** How often do you need feedback or updates to ensure success?
- you need a lot of hands-on practice to develop the right intuitions here.
- THE INNER DEVELOPER LOOP
- In traditional manual coding, developers have worked in the same cycle, or loop, since time immemorial. You write some code, depending on the language, you may have to compile it, and then you run it, test it, debug it, and repeat.
- This same loop is repeated at three different timescales: inner (tasks that occur in seconds to minutes), middle (tasks that occur over hours to days), and outer (tasks that occur over weeks to months).

![](https://readwise.io/reader/pcei/gAAAAABpAVxPKmE18k-_456aL-fMA950DThjJ3-l4wIZy_aXuy4oIDN5VW_mhWojEjhytYmMOSsJp41YyLwv9AeHOkLt8kaDqaSkbwUyvDx60hbiEyLcYXc=/f0176-01.jpg)

- With vibe coding, the loop is superficially transformed, but at its core it remains similar to the traditional developer loop.

![](https://readwise.io/reader/pcei/gAAAAABpAVxPb822QcXMkv_DTNcsltX55yjMndgRI20iSNzl8RSTkTiZQM4-RZ39LIZw6A377_JLzZBjJ8m5GTqT-pBqznxO9GXra8U4jCDTzeMrId1olkE=/f0177-01.jpg)

- The inner developer loop is the rhythm of your minute-to-minute and second-to-second vibe coding workflow.
- A chef who diligently sets and checks pans, tastes the dish throughout, and course-corrects after any misstep will find and fix issues fast.
- We’ll lead with the safety net: You need to be sure you can recover before taking risks. Then we’ll constrain the risk with small, manageable tasks. Next, we’ll plan each act with clear specifications. We’ll build quality gates with comprehensive tests. And finally, we’ll end with delegating advanced Git mastery as the cherry on top.
- Keep these top of mind and think about them every few minutes, if not seconds. These are the most frequently used prevention practices in vibe coding and are a key part of your vibe coding portfolio.

##### Checkpoint and Save Your Game Frequently

- Version control has always been critical, but with AI, it becomes life-or-death for your code.
- Your essential checkpointing tools might include:
    - Version control as your primary safety mechanism, typically with Git, though AI knows most other systems as well. Git’s especially good for checkpointing because of its lightweight branching mechanism. You don’t have to understand it, but using Git will make it easier for AI to help you rewind your saved games.
    - IDE checkpointing features, like IntelliJ’s local history as backup (it can bring up every saved file for days).
    - AI-written commit messages that clearly document changes.
    - AI assistance for recovery operations when things go wrong.
- In general, decompose and subdivide every task into the smallest steps you can. For all but the smallest tasks, you probably want to have your AI assistant generate step-by-step plans for you to review.
- In this review, you’ll notice steps you want your assistant to plan in more detail.
- As you gain confidence, you can try making your increments larger.
- If you’re using a coding agent, have it put those plans in a Markdown file, keep its own progress up to date there, and have it refer to that file when continuing the problem in any new session. Remove the plan the minute you think it might be stale.
- By keeping tasks small, we also make our verification process significantly easier.
- Like the task tree we discussed earlier in the book, keep decomposing the work until you feel the leaf nodes are within the ability of AI to implement. For each task, be super prescriptive: provide clear objectives, detailed technical requirements, and explicit examples. The more precise your instructions, the better you can expect the results to be.

##### Get AI to Write Specifications

- One of the best habits you can cultivate is asking your sous chef to draft a detailed plan first.
- This written plan—what we’ll interchangeably call a specification—serves two vital functions. First, it serializes the task graph, representing explicitly how each step of your project fits together. This allows you to progress along the graph toward your goal in small increments, with each step per fresh AI session. The second vital function is creating a clear picture of success that you and AI agree upon before it starts work. This specification becomes your requirements baseline—defining not just what to build, but how you’ll know when it’s built correctly.
- Creating the specification and test plan can be a big task itself, and you may need to split the job into pieces.
- First have AI write your specification, haggle over the details until you’re satisfied, and then make sure to have it write a good test plan.
- Here are some things you might ask your AI collaborator to do:
    - Write acceptance tests before you write code (true test-driven development), which we’ll use to validate the AI-generated implementation. (We’ll describe how in the next section.)
    - Generate behavior-driven development scenarios in given-when-then format that trace directly back to your user stories and acceptance criteria.
    - Create test datasets that systematically exercise boundary conditions, edge cases, and error scenarios.
    - Generate comprehensive regression test suites whenever you modify existing functionality.

##### Have AI Write the Tests

- After AI writes the tests, it’s your responsibility, optionally working with AI, to:
    - **Eyeball the tests:** Carefully review each one to ensure it properly implements your intent.
    - **Run the tests yourself:** Execute them to verify they work as expected. (AI doesn’t always get it right.)
    - **Review and critique:** Have AI analyze its own tests for potential issues or improvements. This should be done separately from running the tests, to keep it focused.
    - **Have AI run its own tests:** Never believe it when it says they’re working until you’ve seen it. Have AI run the tests it writes. Or run them by hand if you want to save a couple of bucks a day and only notify AI when they’re broken. But don’t blindly commit.
- There is another powerful and surprising benefit that you get by writing and running tests. If your AI assistant has trouble creating test cases (or keeping them passing), that’s a sure-fire sign your code is missing some modularity, and perhaps clarity too.
- Hard-to-test code is a warning sign you should take seriously.
- But these days you can delegate your Git operations to AI, including complex ones involving searching through history and making changes across multiple branches.
- Having AI create detailed commit messages that not only explain what changed but also describe why the change was made, can be extremely helpful. These narratives are indispensable when you’re trying to decide how to roll back.
- The case for test-driven development (TDD), where you write tests before the code, has never been stronger.
- When implementing TDD with your AI assistant:
    - **Start with quality over quantity:** Collaborate with your assistant on one thorough test before generating ten more. When your tests pass, you gain confidence that your code is working as designed.
    - **Have AI fix flaky tests:** Tests that spuriously fail contribute to the “broken windows” problem. This is an area where AI can shine, as flaky tests are rarely fun to debug. When code generation is so fast, you need your tests to be reliable to keep up! (If your tests are flaky, it means you may no longer be in control, and you’ll soon wreck the car.)
    - **Shift toward higher-level testing:** As AI generates more granular functions, your tests should verify how components work together.
    - **Automate test execution:** Configure your environment to run tests on every save for instant feedback.
- Many developers are asking: “How can you trust AI-generated code that you never personally inspected?” The answer is going to involve a lot of testing. This situation closely resembles how we use open-source libraries. We rarely examine every line of code in those either. Libraries are usually treated as black boxes, and we build trust with them through testing.
- Key practices to remember as you refine your inner loop are:
    - **Keep your prep work (tasks) small and laser-focused:** Decompose ruthlessly.
    - **Save your game more often:** Use version control (like Git, with your AI as your Git sommelier) for every incremental success. This is your safety net and your springboard for daring experiments.
    - **Have AI generate a specification and study it:** This shared understanding prevents many mistakes.
    - **Learn from watching AI work:** Constant vigilance catches deviations early, but you’ll also pick up new commands or approaches that make *you* a better chef.
    - **Trust, but verify:** Never assume “it worked” or “tests pass” without seeing the evidence. If possible, watch AI run the tests itself.
    - **Know when to take the whisk back:** If AI is fumbling or stuck in a loop, step in. Your human insight is often the quickest way to get unstuck or walk that crucial last mile.
    - **Embrace your AI as your most attentive (and talkative) rubber duck:** Explaining your problem to AI, even if it’s just to organize your own thoughts, can lead to breakthroughs.
- THE MIDDLE DEVELOPER LOOP
- This is where we deal with transitions, managing handoffs between work sessions that might happen every few hours or stretch across days.
- This may involve more planning than you’re accustomed to. Unlike a human teammate who remembers yesterday’s progress and discussions, your AI assistant effectively walks into a closet and forgets everything at the end of each chat session. When you fire up a new conversation, it starts with a completely blank slate. All the context, the nuances, the constraints you established hours, minutes, or days ago are gone. Poof.
- You need deliberate strategies to bridge these memory gaps, ensuring that each new session builds upon the last rather than forcing you to rebuild a bunch of shared understanding from scratch every time you start a new task.
- We do this by first creating persistent memory systems
- To best combat these problems, your rules need to be written down or clearly articulated for them to follow.
- You can’t write down every rule for your AI assistant due to limitations with context windows, attention, and instruction following. The longer your list of rules, the less likely AI will follow them all. It’s like posting kitchen rules on the wall. The bigger the poster, the smaller the print, the harder it is for everyone to follow, so choose carefully.
- For your AI collaboration, focus on documenting your “golden rules”—what should always be done and never be done. Some rules are useful for all projects, and some will be unique to your ecosystem. Here is an example of what such a list might look like:
    - Never use global variables.
    - Never put keys in version control.
    - Always use a secrets manager.
    - Avoid deeply nested functions.
    - For typed languages, avoid wildcard or “any” types.
- Memory for coding agents takes various forms:
    - Memory files (usually Markdown) at project, user, and global levels. These are inserted at the beginning of each conversation automatically, depending on how your system is configured.
    - Manually pasting rules into each query in your conversation, to refresh the AI’s attention when it’s especially important.
    - In time, memory databases, to facilitate multiple teams and AIs working together long-term.
- When everyone starts work the next day, they have no memory of what happened. If you’re doing catering and every dish requires multiple days of preparation, this becomes a huge challenge.
- How long you can go without compacting your session depends on the language you’re using, the robustness of your tools, and how much work AI must do to understand your project. If you have many log messages or verbose build outputs, your cycle may be faster, with only a few minutes between compactions.
- Here’s what we do: Clear the context proactively when you can. As your context approaches 20–50% remaining, tell AI to stop and document what it’s doing. When
- Give it any extra instructions you want to carry forward, have it write its latest plan or specification in a Markdown file, and then you can compact (or clear the context) and move on.
- Those specification files are the external memory that allows you to keep forging ahead.
- you must proactively leave clues for AI, all over your body if necessary, so it will know what to do in the next session. You need to develop systems for managing this constraint—creating written artifacts, maintaining clear documentation, and developing habits around session transitions that preserve critical context.
- found that the most practical mitigation strategy is having our agent externalize its state before ending a session.

##### Working with Two Agents at Once, and More

- Chat assistants are highly synchronous and require constant attention. You ask a question, wait for a response, apply the results yourself, then ask another
- You set one agent on a task, and while it works, you can shift your attention elsewhere. When the agent needs your input, you can respond, then switch back to another project again. That project might as well get its own agent. This workflow naturally encourages you to run multiple agents at once.
- For the multi-agent approach to work well, your agents must have independence of action, decoupled from one another insofar as practical.
- • **Separation:** Agents should work on different parts of your code base to avoid merge conflicts. • **Decoupling:** The components shouldn’t be tightly linked. Changing both sides of an interface simultaneously causes problems. • **Clear interfaces:** Well-defined interfaces between components allow independent work.

##### Intentional AI Coordination: Avoiding the Contaminated Cutting Board

- We can encounter situations where tasks look like they can run in parallel, but they subtly interfere with each other because they’re touching the same “cutting board”—the same files, the same functions, the same system resources (e.g., ports), and overlapping configuration.
- It becomes far more complex when two or more major initiatives affect the code base simultaneously.

##### Keeping Your Agents Busy When You’re Busy

- Anthropic highlights this characteristic of AIs in the *Claude Code Best Practices* guide, where it states, “Like humans, Claude’s outputs tend to improve significantly with iteration. While the first version might be good, after 2–3 iterations it will typically look much better.”[4](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch15en4) Asking them to revisit their work and have them rerun tests can reveal that the work is not finished at all—the “finished build” doesn’t compile, the “running tests” are missing, or some other dodgy, off-brand characterization of “done.” Everything may run and look like it works, but self-critique can nonetheless turn up useful concerns and corrections.
- Here are some of our favorite directives for keeping an agent doing something useful:
    - **Run all tests again and report any failures:** You’ll be surprised how many times new test errors surface after AI reports success.
    - **Improve your test cases:** Have AI analyze your code and test cases and ask it to improve the tests. It’s reassuring to build up the automated tests you can rely upon to validate your code.
    - **Review code for missing edge cases:** AI is good at sniffing out problems, including in its own code. The OpenAI Codex team has “find and fix a bug” as one of its first recommended prompts.[5](private://read/01k8pn11w75s4qpt3gn9rgrx9p/endnotes.xhtml#ch15en5)
    - **Iterate on the first draft:** Have AI check its own code for error handling, robustness, idiomatic code, warnings and linting, and formatting. Or if you’re short on time, yell “Make it better!” and run off.
    - **Summarize anything suspicious:** A little paranoia goes a long way. Look for ways the code could fail. Have AI look too.
    - **Clean up your mess:** Remove temp files, branches, and log statements, and debug code paths. Make sure all untracked files are either added or removed. AI may have made it, but it’s your mess now.
    - **Write a Markdown summary of what you’ve done and anything you couldn’t finish:** These artifacts become invaluable when you resume or hand work off.
    - **Make sure the documentation and project artifacts are up to date:** These can be overlooked in the heat of development.
    - **Try writing one more test to break your own solution:** Adversarial agents may be able to safeguard you better than the friendliest colleagues.
    - **Prepare a diff or code review package:** Now you’re stacking optionality, with more ways to inspect without context switching.
- Gene learned an important lesson that day: The longer you let AI add upon its code without inspecting it and ensuring its modularity, the bigger the effort will be to reinstitute some sort of modular sanity. It took Gene three days of rewriting (one day all by hand), modularizing the code, and putting in build tests at the modular boundaries.
- However, the best-laid plans of AIs and humans often go awry, and agents sometimes interfere with each other’s work. While preventive measures help, you can’t always predict every interaction. We want to detect when these contention issues grow into larger problems. They may include:
    - Merge conflicts when agents modify the same files.
    - Port conflicts when multiple server instances try to use the same ports.
    - Shared resource contention (databases, files, services).
    - Branch confusion when agents accidentally work on the same branch.
- At their core, these issues all stem from shared resources. Anything that can be shared—source files, ports, repos, databases, memory, CPU—creates potential collision points between agents.
- Multi-agent operations need a clear disaster-recovery hierarchy: Fix the immediate technical problems first, then rebuild your broken workflows, then strengthen your systems to prevent recurrence.
- This same principle—the tracer bullet approach—is invaluable when working with AI assistants on coding projects. A tracer bullet represents a minimal implementation that proves a complete path through your system works.

##### Sharpen Your Knives: Investing in Workflow Automation

- Our advice: Any time you can reduce the slinging required when vibe coding via automation, do it. It will pay off.
- Almost any workflow that involves reviewing, transforming, or acting upon data can be sped up or automated by a well-designed helper agent.

##### The Economics of Optionality: Why We Believe Optionality Is So Important

- In software, we have embraced this principle. The industry has A/B feature flagging (i.e., feature toggles). We build both feature variants and test which one performs better. We defer the decision to pick the final version until we see how both perform in production. Traditionally exploring these types of alternatives could be expensive. Building two different architectures meant doubling your effort. In most cases, we couldn’t afford this luxury, so we’d make our best guess and live with the consequences.
- we can drive up the number of experiments, because “t” is so small. This means we can explore much more of the option space, across all areas of our product (“N”: the modules in our product). And then we mix and match from all those options.
- There is a catch, though. We must make our cost of change low.
- We make our code base easy to change with, you guessed it, a modular architecture (which enables independence of action, makes changes safer, and drive up “N”) and fast feedback loops (which also enables us to make those changes safely and sense-make whether the change is better or worse).

#### Conclusion

- Key practices to remember as you orchestrate these longer-term collaborations:
    - **Document Your Golden Rules:** Codify your non-negotiables in AGENTS.md. Your AI helpers need explicit instructions, especially for those “always do” and “never do” items.
    - **Design for Your Sous Chefs:** Structure your code and choose your tools in ways that make it easier for AI to assist. Don’t make them fight an uphill battle against obscure frameworks or monolithic files.
    - **Externalize AI’s state:** Before ending a session, have your AI write down its progress, current plan, and any tricky bits. Treat these notes as invaluable “tattoos” to guide the next session.
    - **Embrace Multiple Agents, Mindfully:** Leverage the power of parallel work but be deliberate about task separation and potential merge conflicts. Think “different stations, different dishes.”
    - **Keep Idle Agents Productive:** When an agent claims it’s “done,” have it review its work, improve tests, or look for edge cases. This self-critique is surprisingly effective.
    - **Use Tracer Bullets for Correction:** When AI struggles, simplify the problem to its core. A small, successful “tracer” can get things back on track or tell you when to switch to manual coding.
    - **Automate Your Workflow:** Sharpen your knives by investing time in scripting repetitive tasks. Reducing the “slinging” between tools dramatically boosts your FAAFO, especially optionality, by making more experiments feasible.
- THE OUTER DEVELOPER LOOP
- We’ll guide you through the three pillars of outer-loop mastery—prevent, detect, and correct.
- Many who have had to support production systems may learn to use different colors for their terminal windows: red for production (never reboot) and green for staging (reboot away). Because of the coding agent workspace confusion risk, we’ve adopted the same practice.
- By partitioning and labeling our different workspaces, we have more cues as to where we are. Your “workspaces” include any place where you have indirection: directories, repositories, branches, databases, API endpoints. Each workspace needs markers and signposts.
- First, **partition your workspaces (and work) clearly**. Your “workspaces” include any place where you work that has potential contention, where multiple agents might interfere with each other: directories, repositories, version control branches. Try to have your agents work in separate workspaces as much as possible.
- Sometimes you need to redesign your kitchen layout to accommodate your sous chef’s peculiar habits.
- This requires setup in the outer loop—setting up the preventive road signs and guardrails. As you work in the middle loop, you need to be vigilant about the road signs you put up.
- This tendency toward verbosity creates a compounding problem. Code has inertia, and bloated code makes everything more difficult for everyone—including AI.
- Worse, when AI bypasses established modular interfaces, it destroys modular boundaries. Multiple modules start fusing into one increasingly tangled mass. They can no longer be changed or tested independently without breaking things.
- There are two categories of concrete enforcements: minimalism and modularity. Here are some tips on minimalism:
    - **Question every new addition:** Does this need a new library or even a new file? Challenge your AI to justify additions and explore if existing structures can accommodate the new functionality.
    - **Set budgets for code:** For some tasks, constrain AI to solve the problem within a certain line count or with minimal changes. This forces it to think about constraints.
    - **Employ a “refactor after” pattern:** Let AI generate the initial functionality, then, in a separate step, instruct it to refactor for conciseness, readability, and elegance.
    - **Ban unnecessary dependencies:** Instruct your AI to avoid pulling in new libraries or frameworks without your explicit approval. It should usually be able to achieve the goal with existing tools or standard library functions.
    - **Practice “surgical commits”:** Insist on the smallest possible changes to achieve a goal. Reject solutions that touch unrelated code paths or modules.
- Here are some tips on modularity:
    - **Define clear modular boundaries:** For each task, explicitly state which modules AI can and cannot modify. This might be an “honor system” instruction or enforced through sandboxing.
    - **Enforce interface immutability:** This is a golden rule. Instruct your AI assistant that existing module interfaces are sacrosanct unless a change is explicitly requested and approved by you. Consider adding this to your AGENTS.md file.
    - **Mandate diff reviews with an eye for sprawl:** Before accepting changes, always examine the diff. Be particularly wary of modifications that spread across numerous files when the change should logically be localized.
    - **Conduct regular architecture audits:** Periodically, perhaps with AI assistance, review your code base for coupling violations and identify opportunities for improving modularity.
- Before submitting a pull request in vibe coding, you must thoroughly inspect and scrutinize your AI assistant’s work, as auditors do. The depth of your review should be proportional to both the project’s risk level and your familiarity with the programming language.

![](https://readwise.io/reader/pcei/gAAAAABpAVxQUnUNVgC_UiysmXsj7-sqzoprK63_fsCC9B2fEYSyxWarO06a2tWW7Ie5UpnMfOMPxyQ5FMk68fHJ4NvqeX2rz9ZaF0k-eyAkTG5Foulu58M=/f0236-01.jpg)

- “Black box” testing, or auditing *around* the box, means you look at the code’s inputs and outputs. If the output looks reasonable, great, ship it. This can be a valid approach for low-risk projects, whether you know the enclosing system well or not.
- The other approach is “white box” testing, or auditing *through* the box, meaning we’re inspecting the internals of the code. You’re tracing execution paths, identifying and testing edge cases, studying data structures and private implementation details, searching for both point failures and system-wide flaws. This level of scrutiny is a must for high-risk, high-impact projects. AI wrote the code for you, but you still own it.
- When orchestrating multiple AI agents across complex systems, you must detect problems in order of blast radius: catastrophic data loss first, then systematic pipeline monitoring, then the early warning systems that turn near-misses into competitive advantages.
- We’re seeing early patterns emerge: **Agent Organization Patterns:**
    - **Subagents:** These enhance context window lifetime and parallelize research tasks.
    - **Generators and verifiers:** Separate concerns by creating dedicated agents for implementation versus testing.
    - **Task graph discipline:** Break work into leaf nodes small enough for agents to handle independently. **Communication and Context Sharing:**
    - **Shared documentation and files:** Agents (and people) ex-change context through plans, specifications, and design docs (recommended in Anthropic’s *Claude Code Best Practices*).
    - **Direct agent communication:** Frameworks enable agents to message each other, with MCP as a communication layer between systems. **Parallel Work Management:**
    - **Well-designed parallelism:** Minimize dependencies while maximizing concurrent agent work.
    - **Large-scale parallel experimentation:** Multiple agent clusters with separate repository clones compete to find optimal solutions.
    - **Verification integration:** Build testing and validation into every stage rather than leaving it until the end.
    - **Merge strategies:** Plan ahead for how components will recombine without conflicts.
- Escoffier created the modular system of specialized stations, each with clear responsibilities and interfaces to other stations. Instead of every cook trying to do everything, he established distinct roles: one focusing exclusively on sauces (*saucier*), one handling fish (*poissonnier*), one managing cold preparations (*garde manger*), and so on. Each station became its own mini kitchen, optimized for specific tasks but carefully coordinated with the whole. Suddenly, kitchens could parallelize work effectively. Each specialist could develop deep expertise in their domain while maintaining clear interfaces with other stations. It’s the kind of task decomposition and interface design we strive for in modern software systems and which becomes more important when vibe coding.
- The head chef (also known as the executive chef or *chef de cuisine*) designed the menu (the specification), established standard processes (the protocols), and ensured all the stations integrated smoothly (the interfaces). The sous chef acted as an operational manager, handling real-time coordination and quality control.
- What made the brigade system remarkable was how it could be scaled. Need breakfast, lunch, and dinner services? Promote an additional sous chef for each shift. Hosting a banquet for five hundred? Spin up more station chefs the way we launch extra Kubernetes pods today. The underlying pattern stays constant; only the replica count changes. This scalability—a hallmark of exceptional Layer 3 architecture—allowed the system to adapt to virtually any sized operation.
- BUILDING STANDARDS FOR HUMAN–AI DEVELOPMENT TEAMS
- Ensuring everyone—human and AI—can work using the same high standards, using a shared recipe book.
- In a vibe-coding kitchen, your prompts, global rules and AGENTS.md files, and/or shared memory can all play this role. Now everyone can tap into the wisdom of veteran vibe coders who’ve found great tips and approaches.
- A guideline here becomes obsolete; a new best practice emerges there. We suggest carving out time—and we mean setting aside a significant portion of your time every day—to curate your prompt and rules files, Markdown plans, and other daily context for your agents.
