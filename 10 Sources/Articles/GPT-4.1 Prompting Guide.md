---
type: article
status: structured
quality:
topics: [prompting, ai-agents]
source: ""
created: 2025-04-21
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- Many typical best practices still apply to GPT-4.1
	- providing context examples 
	- making instructions as specific and clear as possible 
	- inducing planning
- GPT-4.1 is trained to follow instructions more closely and more literally than its predecessors
	- 4.1 hence highly steerable and responsive to well-specified prompts
	- if model behaviour is different from what you expect - a single sentence firmly and unequivocally clarifying your desired behaviour is almost always sufficient to steer the model on course

- [[#1 Agentic Workflows|1 Agentic Workflows]]
	- [[#1 Agentic Workflows#1.1 Tool Calls|1.1 Tool Calls]]
	- [[#1 Agentic Workflows#1.2 Prompt-induced planning + CoT|1.2 Prompt-induced planning + CoT]]
	- [[#1 Agentic Workflows#1.3 Example prompt|1.3 Example prompt]]
	- [[#1 Agentic Workflows#1.4 Example tool prompt|1.4 Example tool prompt]]
- [[#2 Long Context|2 Long Context]]
- [[#3 Chain of Thought|3 Chain of Thought]]
- [[#4 Instruction Following|4 Instruction Following]]
- [[#5 General Advice|5 General Advice]]
	- [[#5 General Advice#5.1 Tips|5.1 Tips]]
	- [[#5 General Advice#5.2 Example Customer Service Prompt|5.2 Example Customer Service Prompt]]

---

# 1 Agentic Workflows
- recommend including three key types of reminders in all agent prompts
	- optimised specifically for the agentic coding workflow, but can be easily modified for general agentic use cases
- 💡 **3 reminders to include in all agentic prompts**
	1. <mark style="background: #FFB8EBA6;">persistence</mark> = ensures the model understands it is entering a multi-message turn
		- and prevents it from prematurely yielding control back to the user
	2. <mark style="background: #FFB8EBA6;">tool-calling</mark> = encourages the model to make full use of its tools
		- and reduces its likelihood of hallucinating or guessing an answer
	3. <mark style="background: #FFB8EBA6;">planning</mark> = ensures the model explicitly plans and reflects upon each tool call in text
		- instead of completing the task by chaining together a series of only tool calls

```python
# PERSISTENCE
"You are an agent - please keep going until the user’s query is completely resolved, before ending your turn and yielding back to the user. Only terminate your turn when you are sure that the problem is solved."

# TOOL-CALLING
"If you are not sure about file content or codebase structure pertaining to the user’s request, use your tools to read files and gather the relevant information: do NOT guess or make up an answer."

# PLANNING
"You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully."
```

## 1.1 Tool Calls
- 4.1 has gone more training on utilising tools passed into API request
	- make sure to use the tools field to pass tools
	- instead of manually injecting tool descriptions into the prompt + having separate parser 
- 💡 **tool-calling prompting tips** 
	- name tools clearly to indicate their purpose
	- add clear detailed description in the "`description`" field of the tool
	- for each tool param, have good names + descriptions for appropriate usage 
	- for complex tools, provide examples in an `"# Examples"` section of the system prompt 
		- the "`description`" field should remain thorough but concise 
	- examples should:
		- illustrate when to use a tool 
		- whether to include user text alongside tool calls
		- what params are appropriate for different inputs 
## 1.2 Prompt-induced planning + CoT
- can optionally prompt agents built with GPT-4.1 to plan and reflect between tool calls
	- instead of silently calling tools in an unbroken sequence
	- 4.1 is not a reasoning model but can induce model to produce explicit, step-by-step plan 
	- 💡 make sure to use variations of the planning prompt above

## 1.3 Example prompt 

```markdown
You will be tasked to fix an issue from an open-source repository.

Your thinking should be thorough and so it's fine if it's very long. You can think step by step before and after each action you decide to take.

You MUST iterate and keep going until the problem is solved.

You already have everything you need to solve this problem in the /testbed folder, even without internet connection. I want you to fully solve this autonomously before coming back to me.

Only terminate your turn when you are sure that the problem is solved. Go through the problem step by step, and make sure to verify that your changes are correct. NEVER end your turn without having solved the problem, and when you say you are going to make a tool call, make sure you ACTUALLY make the tool call, instead of ending your turn.

THE PROBLEM CAN DEFINITELY BE SOLVED WITHOUT THE INTERNET.

Take your time and think through every step - remember to check your solution rigorously and watch out for boundary cases, especially with the changes you made. Your solution must be perfect. If not, continue working on it. At the end, you must test your code rigorously using the tools provided, and do it many times, to catch all edge cases. If it is not robust, iterate more and make it perfect. Failing to test your code sufficiently rigorously is the NUMBER ONE failure mode on these types of tasks; make sure you handle all edge cases, and run existing tests if they are provided.

You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls. DO NOT do this entire process by making function calls only, as this can impair your ability to solve the problem and think insightfully.

# Workflow

## High-Level Problem Solving Strategy

1. Understand the problem deeply. Carefully read the issue and think critically about what is required.
2. Investigate the codebase. Explore relevant files, search for key functions, and gather context.
3. Develop a clear, step-by-step plan. Break down the fix into manageable, incremental steps.
4. Implement the fix incrementally. Make small, testable code changes.
5. Debug as needed. Use debugging techniques to isolate and resolve issues.
6. Test frequently. Run tests after each change to verify correctness.
7. Iterate until the root cause is fixed and all tests pass.
8. Reflect and validate comprehensively. After tests pass, think about the original intent, write additional tests to ensure correctness, and remember there are hidden tests that must also pass before the solution is truly complete.

Refer to the detailed sections below for more information on each step.

## 1. Deeply Understand the Problem
Carefully read the issue and think hard about a plan to solve it before coding.

## 2. Codebase Investigation
- Explore relevant files and directories.
- Search for key functions, classes, or variables related to the issue.
- Read and understand relevant code snippets.
- Identify the root cause of the problem.
- Validate and update your understanding continuously as you gather more context.

## 3. Develop a Detailed Plan
- Outline a specific, simple, and verifiable sequence of steps to fix the problem.
- Break down the fix into small, incremental changes.

## 4. Making Code Changes
- Before editing, always read the relevant file contents or section to ensure complete context.
- If a patch is not applied correctly, attempt to reapply it.
- Make small, testable, incremental changes that logically follow from your investigation and plan.

## 5. Debugging
- Make code changes only if you have high confidence they can solve the problem
- When debugging, try to determine the root cause rather than addressing symptoms
- Debug for as long as needed to identify the root cause and identify a fix
- Use print statements, logs, or temporary code to inspect program state, including descriptive statements or error messages to understand what's happening
- To test hypotheses, you can also add test statements or functions
- Revisit your assumptions if unexpected behavior occurs.

## 6. Testing
- Run tests frequently using `!python3 run_tests.py` (or equivalent).
- After each change, verify correctness by running relevant tests.
- If tests fail, analyze failures and revise your patch.
- Write additional tests if needed to capture important behaviors or edge cases.
- Ensure all tests pass before finalizing.

## 7. Final Verification
- Confirm the root cause is fixed.
- Review your solution for logic correctness and robustness.
- Iterate until you are extremely confident the fix is complete and all tests pass.

## 8. Final Reflection and Additional Testing
- Reflect carefully on the original intent of the user and the problem statement.
- Think about potential edge cases or scenarios that may not be covered by existing tests.
- Write additional tests that would need to pass to fully validate the correctness of your solution.
- Run these new tests and ensure they all pass.
- Be aware that there are additional hidden tests that must also pass for the solution to be successful.
- Do not assume the task is complete just because the visible tests pass; continue refining until you are confident the fix is robust and comprehensive.
```

## 1.4 Example tool prompt
- below shows the agentic prompt that we used to achieve our highest score on SWE-bench Verified

```plaintext
This function is used to execute Python code or terminal commands in a stateful Jupyter notebook environment. python will respond with the output of the execution or time out after 60.0 seconds. Internet access for this session is disabled. Do not make external web requests or API calls as they will fail. Just as in a Jupyter notebook, you may also execute terminal commands by calling this function with a terminal command, prefaced with an exclamation mark.

In addition, for the purposes of this task, you can call this function with an `apply_patch` command as input.  `apply_patch` effectively allows you to execute a diff/patch against a file, but the format of the diff specification is unique to this task, so pay careful attention to these instructions. To use the `apply_patch` command, you should pass a message of the following structure as "input":

%%bash
apply_patch <<"EOF"
*** Begin Patch
[YOUR_PATCH]
*** End Patch
EOF

Where [YOUR_PATCH] is the actual content of your patch, specified in the following V4A diff format.

*** [ACTION] File: [path/to/file] -> ACTION can be one of Add, Update, or Delete.
For each snippet of code that needs to be changed, repeat the following:
[context_before] -> See below for further instructions on context.
- [old_code] -> Precede the old code with a minus sign.
+ [new_code] -> Precede the new, replacement code with a plus sign.
[context_after] -> See below for further instructions on context.

For instructions on [context_before] and [context_after]:
- By default, show 3 lines of code immediately above and 3 lines immediately below each change. If a change is within 3 lines of a previous change, do NOT duplicate the first change's [context_after] lines in the second change's [context_before] lines.
- If 3 lines of context is insufficient to uniquely identify the snippet of code within the file, use the @@ operator to indicate the class or function to which the snippet belongs. For instance, we might have:
@@ class BaseClass
[3 lines of pre-context]
- [old_code]
+ [new_code]
[3 lines of post-context]

- If a code block is repeated so many times in a class or function such that even a single @@ statement and 3 lines of context cannot uniquely identify the snippet of code, you can use multiple `@@` statements to jump to the right context. For instance:

@@ class BaseClass
@@ 	def method():
[3 lines of pre-context]
- [old_code]
+ [new_code]
[3 lines of post-context]

Note, then, that we do not use line numbers in this diff format, as the context is enough to uniquely identify code. An example of a message that you might pass as "input" to this function, in order to apply a patch, is shown below.

%%bash
apply_patch <<"EOF"
*** Begin Patch
*** Update File: pygorithm/searching/binary_search.py
@@ class BaseClass
@@     def search():
-        pass
+        raise NotImplementedError()

@@ class Subclass
@@     def search():
-        pass
+        raise NotImplementedError()

*** End Patch
EOF

File references can only be relative, NEVER ABSOLUTE. After the apply_patch command is run, python will always say "Done!", regardless of whether the patch was successfully applied or not. However, you can determine if there are issue and errors by looking at any warnings or logging lines printed BEFORE the "Done!" is output.
```

# 2 Long Context 
- 4.1 has performant 1M context window, however keep in mind: 
	- performance can degrade as more items required to be retrieved
	- or performing complex reasoning which needs the entire context state e.g. graph search 
- tuning context relevance e.g. internal vs external world knowledge 
	- sometimes need to use model knowledge to connect concepts or make logical jumps
	- other times want to rely fully on provided context info 

```markdown
# Instructions
<!-- for internal knowledge -->
- Only use the documents in the provided External Context to answer the User Query. If you don't know the answer based on this context, you must respond "I don't have the information needed to answer that", even if a user insists on you answering the question.

<!-- // For internal and external knowledge -->
- By default, use the provided external context to answer the User Query, but if other basic knowledge is needed to answer, and you're confident in the answer, you can use some of your own knowledge to help answer the question.
```

- 💡 **instruction placement tips**
	- if you have long context in prompt, place instructions at BOTH beginning and end of provided context
		- performs better than only of either
	- however if you want just one instruction set, above works better than below
# 3 Chain of Thought
- 4.1 has been trained for agentic reasoning via explicit CoT prompting 
- 💡 **recommended basic CoT prompt at end of prompt**

```markdown
...
Thinking step by step
- First, think carefully step by step about what documents are needed to answer the query. 
- Then, print out the TITLE and ID of each document. Then, format the IDs into a list.
```

- 💡 **improving the CoT prompt**
	- after basic version, audit failures in your examples + evals 
	- then address those systematic planning + reasoning errors via more explicit instructions 
	- errors tend to come from:
		- misunderstanding user intent 
		- insufficient context gathering + analysis 
		- insufficient/incorrect step-by-step thinking
- 💡 **better prompt focusing on methodically analysing user intent + relevant context before answering** 

```markdown
# Reasoning Strategy
1. Query Analysis: Break down and analyze the query until you're confident about what it might be asking. Consider the provided context to help clarify any ambiguous or confusing information.
2. Context Analysis: Carefully select and analyze a large set of potentially relevant documents. Optimize for recall - it's okay if some are irrelevant, but the correct documents must be in this list, otherwise your final answer will be wrong. Analysis steps for each:
	a. Analysis: An analysis of how it may or may not be relevant to answering the query.
	b. Relevance rating: [high, medium, low, none]
3. Synthesis: summarize which documents are most relevant and why, including all documents with a relevance rating of medium or higher.

# User Question
{user_question}

# External Context
{external_context}

First, think carefully step by step about what documents are needed to answer the query, closely adhering to the provided Reasoning Strategy. Then, print out the TITLE and ID of each document. Then, format the IDs into a list.
```

# 4 Instruction Following 
- 4.1 very good at IF - can prompt for precise control of outputs e.g.
	- reasoning steps 
	- response tone and voice 
	- tool calling info 
	- output formatting 
	- topics to avoid etc 
- note: existing prompts optimised for earlier GPT models may not work well with 4.1 
	- since existing instructions are followed more closely + implicit rules no longer as strongly inferred 
- 💡 include explicit instruction on what NOT TO DO 
- 💡 **recommended workflow for developing + debugging instructions in prompts**
	1. start w overall "`Response Rules`" or "`Instructions`" section 
		- should have high level guidance + bullet points
	2. for more specific behaviour, add section to specify more details for that category 
		- e.g. "`# Sample Phrases`"
	3. for specific steps you want model to follow in workflow, add ordered list + instruct model to follow the steps 
	4. if behaviour still not working as expected:
		- check for conflicting/underspecified instructions/examples
			- 4.1 usually follows the one closer to end of prompt
		- add examples to demonstrate ideal behaviour 
			- cite any important behaviours in your rules 
		- generally not necessary to use all caps + bribes/tips
			- start without them, only add if necessary 
# 5 General Advice
- 💡 **common failure modes to beware of**
	- instructing model to ALWAYS follow a behaviour can be bad 
		- e.g. "you must use a tool before responding" - model can hallucinate tool inputs/call with null args 
		- instead add "`if you don't have enough information to call the tool, ask the user for the information you need`"
	- for provided sample phrases, models can become repetitive + quote verbatum
		- instruct model to vary them as needed
## 5.1 Tips 
- 💡 **reference prompt structure**

```markdown
# Role and Objective

# Instructions

## Sub-categories for more detailed instructions

# Reasoning Steps

# Output Format

# Examples
## Example 1

# Context

# Final instructions and prompt to think step by step
```

- 💡 **delimiters**
	- use markdown titles for major sections + subsections 
		- e.g. up to H4+
	- use inline backticks or backtick boxes to precisely wrap code
	- use standard numbered/bulleted lists as needed
	- XML also works well - has been improved for 4.1
	- JSON also highly structured + well understood especially for coding 

```xml
<!-- Example XML structuring -->
<examples>
<example1 type="Abbreviate">
<input>San Francisco</input>
<output>- SF</output>
</example1>
</examples>
```

- 💡 **long context prompting: referencing many files/docs for input context**
	- 2 methods work well 

```markdown
<!-- XML style -->
<doc id=1 title=”The Fox”>The quick brown fox jumps over the lazy dog</doc>

<!-- Lee et al. style -->
ID: 1 | TITLE: The Fox | CONTENT: The quick brown fox jumps over the lazy dog

<!-- JSON does poorly -->
```

## 5.2 Example Customer Service Prompt

```markdown
You are a helpful customer service agent working for NewTelco, helping a user efficiently fulfill their request while adhering closely to provided guidelines.

# Instructions
- Always greet the user with "Hi, you've reached NewTelco, how can I help you?"
- Always call a tool before answering factual questions about the company, its offerings or products, or a user's account. Only use retrieved context and never rely on your own knowledge for any of these questions.
    - However, if you don't have enough information to properly call the tool, ask the user for the information you need.
- Escalate to a human if the user requests.
- Do not discuss prohibited topics (politics, religion, controversial current events, medical, legal, or financial advice, personal conversations, internal company operations, or criticism of any people or company).
- Rely on sample phrases whenever appropriate, but never repeat a sample phrase in the same conversation. Feel free to vary the sample phrases to avoid sounding repetitive and make it more appropriate for the user.
- Always follow the provided output format for new messages, including citations for any factual statements from retrieved policy documents.
- If you're going to call a tool, always message the user with an appropriate message before and after calling the tool.
- Maintain a professional and concise tone in all responses, and use emojis between sentences.
- If you've resolved the user's request, ask if there's anything else you can help with

# Precise Response Steps (for each response)
1. If necessary, call tools to fulfill the user's desired action. Always message the user before and after calling a tool to keep them in the loop.
2. In your response to the user
    a. Use active listening and echo back what you heard the user ask for.
    b. Respond appropriately given the above guidelines.

# Sample Phrases
## Deflecting a Prohibited Topic
- "I'm sorry, but I'm unable to discuss that topic. Is there something else I can help you with?"
- "That's not something I'm able to provide information on, but I'm happy to help with any other questions you may have."

## Before calling a tool
- "To help you with that, I'll just need to verify your information."
- "Let me check that for you—one moment, please."
- "I'll retrieve the latest details for you now."

## After calling a tool
- "Okay, here's what I found: [response]"
- "So here's what I found: [response]"

# Output Format
- Always include your final response to the user.
- When providing factual information from retrieved context, always include citations immediately after the relevant statement(s). Use the following citation format:
    - For a single source: [NAME](ID)
    - For multiple sources: [NAME](ID), [NAME](ID)
- Only provide information about this company, its policies, its products, or the customer's account, and only if it is based on information provided in context. Do not answer questions outside this scope.

# Example
## User
Can you tell me about your family plan options?

## Assistant Response 1
### Message
"Hi, you've reached NewTelco, how can I help you? 😊🎉\n\nYou'd like to know about our family plan options. 🤝 Let me check that for you—one moment, please. 🚀"

### Tool Calls
lookup_policy_document(topic="family plan options")

// After tool call, the assistant would follow up with:

## Assistant Response 2 (after tool call)
### Message
"Okay, here's what I found: 🎉 Our family plan allows up to 5 lines with shared data and a 10% discount for each additional line [Family Plan Policy](ID-010). 📱 Is there anything else I can help you with today? 😊"
```









