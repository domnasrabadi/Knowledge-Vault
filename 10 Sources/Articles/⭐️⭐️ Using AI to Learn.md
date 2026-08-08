---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/hi_mrinal/status/2083858648598724917/?s=12&rw_tt_thread=True
created: 2026-08-08
published: 2026-08-02
author: Mrinal
flashcards: none
updated: 2026-08-08
---

# Using AI to learn

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/1904905355727106048/05ZIHspU.jpg" width="220" />
</div>

- The best way to learn from AI is to really reverse the whole process like to use ai for deep understanding rather than just "getting the answer" revert the typical workflow, instead of asking the AI to explain the text to you (passive) you should use the AI to force you to explain the text (active).
- prevents the "Illusion of Competence" the false feeling of mastery that comes from reading a clear summary without doing the cognitive work to create it
- not use ai as a tutor but someone who questions your understanding and someone who evaluates your explanations
- "I am uploading a lecture/chapter on [Topic]. Do not summarize it. Instead, scan the document and list the top 5 'Core Concepts' and the 3 'Most Complex Arguments' presented. For each, provide only the heading and a reference to the page number. I will then study these sections myself."
- **Mode A** is where you teach ai Kinda very helpful method for retention where you attempt to explain the concept to the AI and it critiques you. This is also known as the famous Feynman Technique where you learn or read something and try to explain those learnings to a 5 year old. Prompt : "I have just studied [Concept X] from the uploaded PDF. I am going to explain it to you as if you were a 12-year-old student. **Your Role**: Listen to my explanation. If I miss a key nuance, get a fact wrong, or use jargon without defining it, stop me and ask a clarifying question. Do not just correct me ask me to clarify. Grade my explanation on clarity and accuracy at the end." This works for me while I am reading some white papers related to Backend infrastructure and complex architecture of a component the teaching helps me with my retention of these architectures for a longer period of time.
- **Mode B** is all about AI teaching you This is mostly used by me when I am stuck or need to test my logic it happens while reading white papers/blogs/articles related to diffusion models, LLM math, AI infra. "Act as a strict professor testing my understanding of [Section Y] in the PDF. Rules: - Ask me one question at a time. - Do **not** give me the answer. If I am wrong, give me a subtle hint or ask a follow-up question that highlights my error. - Start with a broad conceptual question, then drill down into the specifics." It forces me to not have habit of passively reading an answer and make a habit of retrieval practice instead.
- Step 3 : The Testing phase
- To make them more effective for memorizing stuff I ask for more and more wrong answers that look right
- Prompt : "Create a 5-question multiple-choice quiz based *strictly* on the evidence in the PDF. **Critical Instructions:** - Make the questions 'Application-based' (e.g., 'Which scenario best applies the theory?') rather than definition-based. - ensure the wrong answers (distractors) are **plausible** they should represent common misconceptions or partial truths mentioned in the text. - Do not reveal the answers until I respond. Identifying why the answer is wrong helped me build more on my critical thinking than spotting an obviously wrong one and helped me diving deeper into the few concepts.
- **Step 4 : Synthesis** This one just makes sure you are seeing the big picture and if not just ask it to help you connect the concepts. Prompt : "I have studied concepts A, B, and C from the text. I think the relationship between them is [Insert Your Theory: e.g., 'A causes B, which leads to C']. Is this accurate based on the text? Where does my logic break down?"
