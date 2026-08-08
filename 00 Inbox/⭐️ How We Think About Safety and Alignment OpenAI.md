---
type: article
status: inbox
quality: 1
topics: []
source: https://openai.com/safety/how-we-think-about-safety-alignment/
created: 2026-08-08
published: 
author: openai.com
flashcards: none
updated: 2026-08-08
---

# How we think about safety and alignment | OpenAI

<div align="center">
  <img src="https://images.ctfassets.net/kftzwdyauwt9/h7gAyQVf8jgNJLBqd3Lr4/99f3cefc4bb20e7f25a74180f0bbc260/Safety_SEO_16.9.png?w=1600&h=900&fit=fill" width="220" />
</div>

- Our understanding of how to advance safety has evolved a lot over time, and this post is a current snapshot of the principles that guide our thinking
- In the continuous world, the way to make the next system safe and beneficial is to learn from the current system. This is why we’ve adopted the principle of [iterative deployment⁠](https://openai.com/index/language-model-safety-and-misuse/), so that we can enrich our understanding of safety and misuse, give society time to adapt to changes, and put the benefits of AI into people’s hands
- From today’s AI systems, we see three broad categories of failures:
- **Human misuse**: We consider misuse to be when humans apply AI in ways that violate laws and democratic values. This includes suppression of free speech and thought, whether by political bias, censorship, surveillance, or personalized propaganda. It includes phishing attacks or scams. It also includes enabling malicious actors to cause harm at a new scale.
- • **Misaligned AI**: We consider misalignment failures to be when an AI’s behavior or actions are not in line with relevant human values, instructions, goals, or intent. For example an AI might take actions on behalf of its user that have unintended negative consequences, influence humans to take actions they would otherwise not, or undermine human control. The more power the AI has, the bigger potential consequences are.
- **Societal disruption**: AI will bring rapid change, which can have unpredictable and possibly negative effects on the world or individuals, like increasing social tensions and inequality, or shifts in dominant values and societal norm

### Our core principles

- • **Embracing uncertainty:** *We treat safety as a science, learning from iterative deployment rather than just theoretical principles.* • **Defense in depth:** *We stack interventions to create safety through redundancy.* • **Methods that scale:** *We seek out safety methods that become more effective as models become more capable.* • **Human control**: *We work to develop AI that elevates humanity and promotes democratic ideals.*
- Because we conduct pre- and post-deployment assessments, we gain a deeper, empirical understanding of both capabilities and hazards as they emerge in real-world contexts.
- Safety research requires science: standardizable measurement, open-minded experimentation, and testing. Being able to quantify risks effectively guides research direction and prioritization. We thus [build⁠](https://openai.com/index/mle-bench/) [evaluations⁠](https://openai.com/index/introducing-swe-bench-verified/) starting with measurement goals, often guided by a [threat⁠](https://openai.com/index/building-an-early-warning-system-for-llm-aided-biological-threat-creation/) model, and focus on capabilities that unlock potentially harmful behaviors. We iteratively expand and refine our evaluation suites to capture capability increases and evolving usage
- Even if we can’t observe these behaviors in the real world, we seek out opportunities for empirical observation, such as safely testing models in secure environments with restricted capabilities
- Defense in depth *We stack interventions to create safety through redundancy.*
- It’s likely that no single intervention is the “solution” for safe and beneficial AI. Instead, we draw from the layered approaches in other safety-critical fields such as aerospace, nuclear power, and autonomous vehicles. This involves “layering” multiple defenses such that all of them would need to fail for a safety incident to occur.
- First, in training our models for safety we apply multiple layers of support: [teaching models to understand⁠](https://openai.com/index/deliberative-alignment/) and [to adhere to core safety values⁠](https://openai.com/index/improving-model-safety-behavior-with-rule-based-rewards/), teaching them to follow user instructions and [navigate conflicting instructions from different sources⁠](https://openai.com/index/the-instruction-hierarchy/), training them to be reliable even in the face of uncertainty, and making it robust to adversarial inputs. Our models are supported by complementary systemic defenses: [continuous monitoring post-deployment⁠](https://openai.com/index/a-holistic-approach-to-undesired-content-detection-in-the-real-world/), [open-source intelligence⁠](https://openai.com/global-affairs/an-update-on-disrupting-deceptive-uses-of-ai/) ([OSINT⁠](https://en.wikipedia.org/wiki/Open-source_intelligence)), and [information security.⁠](https://openai.com/index/reimagining-secure-infrastructure-for-advanced-ai/) Each safeguard has unique strengths and gaps, but by stacking multiple layers, we reduce the odds that an alignment failure or adversarial attack will slip through all defenses.

![](https://images.ctfassets.net/kftzwdyauwt9/11cqEzkCP3m2xgaTNwj5q5/923c88040c8478f76b82645fdf48aee6/oai_safety_Diagram_Light.svg?w=3840&q=90)


### Methods that scale

- Our approach to alignment centers humans. We aim to develop mechanisms that empower human stakeholders to express their intent clearly and [supervise⁠](https://openai.com/index/introducing-the-model-spec/) AI systems effectively - even in complex situations, and as AI capabilities scale beyond human capabilities. Decisions about how AI behaves and what it is allowed to do should be determined by broad bounds set by society, and evolve with human values and contexts. AI development and deployment must have human control and empowerment at its core.
- We create transparent, auditable, and steerable models by integrating explicit policies and “case law” into our model training process. We facilitate transparency and democratic input by inviting public engagement in policy formation and incorporating feedback from various stakeholders
- Not all human values, preferences, and intents can be explicitly codified into policies or rules, because there is no *single* moral or social norm. Many are nuanced, context-sensitive, and culture-dependent
- Grounding our models in these deeper principles helps them remain resilient to the imperfections of human feedback, preventing “reward hacking” and other exploitations of human error. While there often is no single right or wrong, we think that by teaching our models understanding in addition to compliance, we can develop tools to better adapt AI systems to diverse contexts, make informed decisions, and align with the moral and social norms of the communities they serve.
