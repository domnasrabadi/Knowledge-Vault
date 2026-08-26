---
type: article
status: raw
quality: 1
topics: [agent-harnesses, ai-coding, context-engineering]
source: https://claude.com/blog/maximizing-the-value-of-your-claude-code-sessions
created: 2026-08-23
published: 2026-08-14
author: Lydia Hallie
flashcards: none
updated: 2026-08-27
---

# Maximizing the Value of Your Claude Code Sessions

<div align="center">
  <img src="https://d34adp677peecb.cloudfront.net/static/images/article1.be68295a7e40.png" width="220" />
</div>

## TL;DR

- **Run `/clear` between tasks.** This prevents prior irrelevant context from being sent back to the model, which can reduce token usage.
- **Set your model and effort level before you start.** Changing either one mid-conversation can bust your prompt cache, which can increase token cost.
- **@-mention files instead of naming them.** The file gets attached to your message directly, which saves a Read call, or a search if Claude has to go find it.
- **Add quiet flags to noisy commands, or run them in a subagent.** Command output is added to the conversation just like a file, and stays there for the rest of the session.
- **Run `/context` once in a fresh session.** It shows what's loaded (`CLAUDE.md`, MCP tool definitions), so you can cut out anything unnecessary.
- **`/compact` before you take a break from your keyboard.** The prompt cache expires after an hour, and summarizing a conversation is much cheaper while it's still cached.

## Maximizing value

- With agentic coding tools like Claude Code, it does. The same completed task can also cost different amounts depending on how you use it.

![](https://readwise.io/reader/pcei/gAAAAABqiVHFrR-L4T2IqqvIbuPuYzQb-n4AgumoNRfmqhMTu6nAx8h3JXk85r_6PjHibbYP5sCU-wct80yV90L1b2PHlTAs_P1HtNCP8XQFy90VU_OlTMw=/file0.png)

- Being efficient with tokens doesn't mean using fewer of them overall. It means making sure the ones you do use go towards the thing you actually asked for.

## What decides the price of a token

- You're billed per token, but what you're actually paying for is inference: the time it takes a GPU (or a TPU, or whatever the model happens to be running on) to run the model over your tokens.
    - Three things decide how much of that time a token takes: which model you're running, whether it's an input token (going in) or an output token (coming out), and whether it was cached.
- **Model**
    - A bigger model does more work on both input and output tokens
- **Input and output tokens**
    - A request goes through the GPU in two phases, and they cost different amounts.
        - First, during prefill, the model reads your request and context: the system prompt, your `CLAUDE.md`, your message, and everything that's been added to the conversation since (the files Claude has read and the output of the commands it ran). Those are your input tokens.
        - Then, during decode, it writes output tokens: its thinking, the tool calls it makes, and the text you see. This happens one token at a time; a 200-token response is 200 runs of the model, one after the other. Per token, decode keeps the GPU busy for a lot longer, which is why output is priced at roughly 5x input.

    ![](https://readwise.io/reader/pcei/gAAAAABqiVHFisygNlnQ87yK154AokGarLBiBsRdg1AHa-NfLimvtDiSdRb4nSzBzUyKv4TUBkjczqbPGrrCh0HlZKd6oXrPBeICVjfBBoA1AQ8vgfluCG0=/file2.png)

    - A lot of the output tokens in a session are thinking tokens, and how much thinking the model does per turn is what the effort level controls
- **Prompt caching**
    - If a request starts with exactly the same tokens as a request the server just saw, the state for that shared beginning comes out the same, so the server can keep it around from last time and only prefill whatever comes after it. This is called prompt caching.
        - Reading from the cache costs 0.1x the input price, because the server loads the state instead of computing it
    - Claude Code manages the prompt cache on every request, there's nothing to turn on. However you can break it, so it's important to know how to avoid these cost spikes.
    - Say we type "fix the failing test in `utils.test.ts`". Here's what Claude Code sends for it:
        1. Claude Code assembles the first request out of the system prompt (tool definitions included), your `CLAUDE.md`, and your message, and sends it off (input tokens). Nothing is in the cache yet, so all of it gets prefilled and written into the cache.
        2. The model can't fix a test it hasn't seen, so it thinks for a moment and responds with a Read call for `utils.test.ts` (output tokens). Claude Code reads the file, appends it to the conversation, and sends the whole thing again (input tokens). This time everything from request 1 is read back out of the cache at a tenth of the price, and the only thing prefilled at full price is what's new: the Read call and the file.
        3. Now the model wants the file under test (output). Another Read, another append, and everything goes out again: requests 1 and 2 from the cache, the second file at full price (input).
        4. The model responds with an Edit (output). Claude Code applies it, appends the result, and sends everything again. Same story: the Edit and its result are new, everything in front of them is a cache read (input).
        5. The model runs `npm test` (output). Claude Code appends the test output and sends everything again, with the test output as the only new part (input).
        6. The tests pass, and the model responds with a short summary (output). No tool call means nothing to append and no request 6, so we're done.
    - A typical turn is lopsided: tens of thousands of tokens going in, a few hundred coming out. But only what's new in that turn gets prefilled at full price.
    - The cache has to match from the very start of the request forward, and requests always go out in the same order: tool definitions, then the system prompt, then the conversation (with `CLAUDE.md` at the front of it).
        - **`/model`**: every model has its own cache, so on the next turn the entire conversation gets prefilled again at full price
        - **`/effort:`** the effort level is part of what the cache is keyed on too, so it's the same story. It's why both `/model` and `/effort` ask you to confirm when you switch in the middle of a conversation
        - **`/compact`**: the conversation gets replaced with a shorter one, so nothing in it matches anymore (the system prompt in front of it survives). Writing the summary itself is cheap as long as the old conversation is still in the cache, so it's a lot cheaper before a long break than after one
        - **Time:** every turn resets the clock, but the cache expires after an hour on a subscription or five minutes on an API key (`ENABLE_PROMPT_CACHING_1H=1` makes it an hour). Come back later than that, and the next turn prefills the whole conversation again. Resuming an old session almost always does too
    - None of this means you should never switch models or effort. It means there are cheap moments to do it, the start of a session or right after a `/clear`, and expensive ones, the middle of a long conversation.

## What decides how many tokens a session sends

- The main thing to know here is that nothing gets sent just once. Everything that ends up in the conversation, a file Claude read or the output of a command it ran, gets sent again on every turn after it, for the rest of the session.
    - That's really the whole cost model of a session: how many tokens end up in the context, how many turns they stay there, and how many contexts you're running at the same time.
- **What ends up in the context**
    - Part of what's in the context is there before you type anything: the tool definitions, the system prompt, `CLAUDE.md`, and whatever else gets loaded at startup.
    - Nearly everything else that gets added during the session is tool results: the files Claude reads, and the output of the commands it runs.
        - How much Claude reads mostly comes down to how much it has to figure out on its own. If you say "the tests are failing", it first has to find out which tests: a grep or two, a few files opened to see which one is relevant, and all of those results stay in the context long after they've stopped being useful.

        ![](https://readwise.io/reader/pcei/gAAAAABqiVHFPJjUlnHZeVOtCxL4BviHY5vfBHeCUGr1JFybJK26eLnJYFvjoBYmBbeL0dCg7ojZ2lo2WG5SrBxa37fUy-DrKAr25yYpvMVYnPung51X_u8=/file3.png)

        - **Tip:** when you're referring to a file, @-mention it instead of typing the path. Claude Code attaches the file to your message before anything gets sent, so it's in the very first request and there's no Read call for it
        - The other thing that fills up the context is the output of the commands Claude runs. Every time it runs your tests, a build, or a git log, whatever that prints gets appended to the conversation just like a file it read, and stays there for the same number of turns.
- **How many turns it stays there**
    - One long session costs more than the same work spread over a few short ones, and by more than you'd think, because turn 40 is also re-reading the 39 turns before it
        - You want the context in your session to be short and relevant, so don't carry one task's context into the next: `/clear` when you start something new, and `/compact` when the earlier part of the same task is done.

    ![](https://readwise.io/reader/pcei/gAAAAABqiVHFb7Z-cRauakQiJ8StVpRKT3WP_CIBFq0OPb3iDsDPDwTLr4YB5aAtkN0i85gipMbJazCmpiESQoEWGAXm_nqyp7o9cpVFC_vzD_yudJrkrOg=/file4.png)

- **Subagents**
    - The other way to keep something out of your context is to have it happen in a different one, which is what subagents are for. A subagent gets its own context window, with its own system prompt, the tools, and your `CLAUDE.md`, but not your conversation
        - only thing that comes back to the main session is its answer. Everything else is thrown away once it's done
    - The downside of not having your conversation is that a subagent sometimes has to re-read things the main session already had, and it's paying for its own turns while it does. For a small job it's just overhead
        - It pays off when a job produces a lot of output you don't need to keep, like going through a log

    ![](https://readwise.io/reader/pcei/gAAAAABqiVHFiFegoWobLLPQURXiMAc2o3d1x1b2c3jQWHClgJc7AOOiB_4nj-mX9XctEZRqT3crtyNGaZYHJ3zqVS2QB9RQi-xsMZGPQzMH_p1rG6BCGpE=/file5.png)

## Where to look first

- Of everything above, four things are worth keeping an eye on, roughly in order of how much they cost:
    - **Long sessions —** Every re-send includes everything before it, so this is where most of a session's tokens go.
    - **Too much in the context —** Files Claude didn't need, noisy command output, leftovers from the previous task, MCP servers you're not using: all of it gets re-sent (and thought about) on every turn.
    - **A bigger model or higher effort level than the task needs —** Everything else gets multiplied by it, and both settings stick between sessions.
    - **Breaking the prompt cache —** Changing model, effort, or fast mode mid-conversation, or coming back after the cache has expired, prefills the whole conversation again at full price.
