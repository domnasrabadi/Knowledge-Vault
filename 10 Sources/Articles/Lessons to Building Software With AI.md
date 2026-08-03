---
type: article
status: structured
quality:
topics: [prompting, ai-coding]
source: ""
created: 2025-04-25
published:
author: ""
flashcards: none
updated: 2026-01-01
---

# 1 Start with Structure, Not Code
## 1.1 Summary
Establish a clear project structure first, before writing any code.
## 1.2 Key Insights
- Jumping straight into code often leads to confusion and rework.
- Clear project structure helps AI understand context and organization.
## 1.3 Tips
- Break projects into logical components early.
- Use descriptive, scalable folder names.
- Allocate dedicated spaces for documentation and tests.
## 1.4 Common Mistakes
- Determining structure as you progress.
- Single-directory projects lacking organization.
- Neglecting documentation and testing areas.

---

# 2 Brainstorm Before Coding
## 2.1 Summary
Discuss your solution strategy with AI thoroughly before requesting code.
## 2.2 Key Insights
- Early brainstorming prevents misalignment and unnecessary code.
- Pre-coding dialogues clarify problem understanding and validate solutions.
## 2.3 Tips
- Outline your approach clearly.
- Consider edge cases and potential challenges upfront.
- Document decisions and rationales clearly.
- Leverage AI’s alternative ideas to enhance solutions.
## 2.4 Common Mistakes
- Hastily generating code without thorough planning.
- Overlooking edge cases initially.
- Not documenting decision processes.

---

# 3 Break Down Complex Problems

## 3.1 Summary
Simplify complex tasks by breaking them down into smaller, manageable steps.
## 3.2 Key Insights
- AI excels at addressing clearly defined, smaller problems.
- Isolating tasks simplifies verification and debugging.
## 3.3 Tips
- Clearly delineate distinct sub-tasks.
- Solve and test each sub-task sequentially.
## 3.4 Common Mistakes
- Presenting multiple problems simultaneously.
- Skipping validation of intermediate steps.
- Using overly broad or vague prompts.

---

# 4 Differentiate Chat and Agent Interactions

## 4.1 Summary
Use chat for brainstorming and research, and agent interactions for specific coding tasks.
## 4.2 Key Insights
- Chat mode is ideal for exploration and broad strategy discussions.
- Agent mode suits precise implementation and coding tasks.
- Clear separation optimizes context and reduces LLM API costs.
## 4.3 Tips
- Use chat to clarify concepts and strategies.
- Switch to agent interactions for specific coding instructions.
- Begin new chats for unrelated issues.
## 4.4 Common Mistakes
- Mixing brainstorming and implementation tasks.
- Using agent tabs for open-ended exploration.

---

# 5 Customize Your AI

## 5.1 Summary
Maintain custom AI instructions or a RulesForAI.md file to improve agent efficiency and consistency.
## 5.2 Key Insights
- Regularly refining custom rules based on actual experience enhances AI interaction quality.
## 5.3 Tips
- Clearly document and update rules based on patterns observed.
- Keep rules specific and easy to understand.
## 5.4 Common Mistakes
- Writing vague or conflicting rules.
- Failing to adapt rules as the project evolves.

---

# 6 File Naming and Modularity

## 6.1 Summary
Clear and modular file naming prevents code duplication and improves AI context management.
## 6.2 Key Insights
- Descriptive file names help AI understand and manage code effectively.
- Modular structures facilitate AI’s focus and improve maintainability.
## 6.3 Tips
- Choose descriptive, purpose-specific filenames.
- Group related functionalities logically.
- Ensure single-responsibility for each file.
## 6.4 Common Mistakes
- Generic or unclear filenames.
- Distributing related code across multiple files unnecessarily.
- Overloaded files handling multiple unrelated tasks.

---

# 7 Always Write Tests
## 7.1 Summary
Testing AI-generated code is essential for catching issues early and ensuring code reliability.
## 7.2 Key Insights
- Tests verify correctness and reduce risk from accepting AI suggestions.
- Writing tests upfront significantly aids future project growth and stability.
## 7.3 Tips
- Write tests before integrating AI-generated code.
- Cover key functionality and edge cases thoroughly.
## 7.4 Common Mistakes
- Skipping testing for small projects.
- Ignoring edge-case scenarios.
- Blindly accepting AI-generated code without verification.

---

# 8 Keep Chats Focused
## 8.1 Summary
Use distinct chats for different problems to maintain clarity and effectiveness.
## 8.2 Key Insights
- Clear and focused contexts improve AI accuracy and effectiveness.
- Reduces confusion and enhances clarity of AI responses.
## 8.3 Tips
- Start separate chats for unrelated issues.
- Maintain one primary topic per conversation.
## 8.4 Common Mistakes
- Mixing multiple distinct problems in a single conversation.

---

# 9 Don’t Just Accept Working Code
## 9.1 Summary
Always review and understand AI-generated code, even if it initially appears correct.
## 9.2 Key Insights
- Understanding the rationale behind code ensures easier debugging.
- Better understanding allows for improved AI interactions and future requests.
## 9.3 Tips
- Examine code carefully and ask AI for explanations on complex sections.
- Validate and optimize generated solutions actively.
## 9.4 Common Mistakes
- Accepting code without full understanding.
- Relying solely on AI for debugging and problem-solving.

---

# 10 Getting Unstuck
## 10.1 Summary
Use targeted debugging statements to assist AI when it struggles with identifying issues.
## 10.2 Key Insights
- Providing runtime feedback clarifies program flow for AI.
- Strategic debugging improves AI’s diagnostic abilities.
## 10.3 Tips
- Direct AI to insert debugging logs or print statements.
- Share runtime debugging outputs with AI for precise troubleshooting.
## 10.4 Common Mistakes
- Allowing AI to continue without new, clarifying information.
- Not actively participating in debugging efforts with AI.

---

# 11 AI Struggles with New Tech
## 11.1 Summary
Provide documentation to AI for new technologies or recent updates to ensure accurate code generation.
## 11.2 Key Insights
- AI knowledge is limited by its training data.
- Documentation bridges gaps in AI knowledge.
## 11.3 Tips
- Always supply relevant docs for new or updated technologies.
## 11.4 Common Mistakes
- Assuming AI has knowledge of recent technology updates.

---

# 12 Commit Often!
## 12.1 Summary
Regular commits help safeguard your work and make experimentation safer when using AI.
## 12.2 Key Insights
- Frequent commits provide historical context and easier rollback.
## 12.3 Tips
- Commit after every successful AI-generated change.
- Write clear and descriptive commit messages.
## 12.4 Common Mistakes
- Delaying commits excessively.

---

By applying these comprehensive practices, you will effectively harness AI's capabilities to build robust, maintainable, and clear software solutions.
