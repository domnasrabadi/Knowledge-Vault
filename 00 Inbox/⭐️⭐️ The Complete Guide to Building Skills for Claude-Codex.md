---
type: article
status: inbox
quality: 2
topics: []
source: https://x.com/rohit4verse/status/2021622526112358663/?rw_tt_thread=True
created: 2026-08-08
published: 2026-02-11
author: Rohit
flashcards: none
updated: 2026-08-08
---

# the complete guide to building skills for claude/codex

<div align="center">
  <img src="https://pbs.twimg.com/profile_images/2005314466255360000/XtVoqVdV.jpg" width="220" />
</div>


### agent skills breakdown:

- a skill is deceptively simple in structure: your-skill-name/├── SKILL.md # Required - main skill file├── scripts/ # Optional - executable code│ ├── process_data.py│ └── validate.sh├── references/ # Optional - documentation│ ├── api-guide.md│ └── examples/└── assets/ # Optional - templates, fonts, icons └── report-template.md
- the heart of every skill is the [skill.md](http://skill.md) file, which contains yaml frontmatter for metadata and Markdown content for instructions:

### how skills actually work:

- the three-level progressive disclosure system
- **level 1 - yaml frontmatter (always loaded):** the skill name and description are injected into claude's system prompt. this provides just enough information for claude to decide when to load the full skill without consuming unnecessary tokens.
- **level 2 - [SKILL.md](http://SKILL.md) body (loaded when relevant):** when claude determines a skill is relevant, it loads the complete instructions from the markdown body. this contains detailed step-by-step guidance, examples, and best practices.
- **level 3 - linked resources (loaded as needed):** additional files in the scripts/, references/, and assets/ directories are accessed only when specifically needed, further minimizing token usage.
- this progressive disclosure approach means skills can be incredibly detailed without overwhelming the context window claude only loads what it needs, when it needs it.
- one of the most ingenious aspects of skills is how they handle visibility. when claude activates a skill, the system sends two types of messages:
    - **user-visible messages** (isMeta: false): these appear in the conversation transcript
    - **meta messages** (isMeta: true): these contain the full skill instructions and are sent to claude's api but never shown to users

### building your first skill:

- step 1: identify your use case
- before writing any code, identify 2-3 concrete scenarios your skill should handle. the most common categories are:
- category 1: document & asset creation
- category 2: workflow automation
- category 3: mcp enhancement
- step 2: define success criteria
- how will you know your skill works? set measurable targets:
    - **triggering accuracy:** skill should load on 90% of relevant queries
    - **tool efficiency:** complete workflows in X tool calls (compared to baseline)
    - **error rate:** zero failed api calls per workflow
    - **consistency:** same task yields similar outputs across sessions
- step 3: write effective descriptions
- the description field is crucial, it's what claude uses to decide when to load your skill. use this structure: [What it does] + [When to use it] + [Key capabilities]Good Example:description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".Bad Example:description: Helps with projects.
- include trigger phrases users would actually say, mention relevant file types, and clearly state what problem the skill solves.
- step 4: structure your instructions
- step 5: test iteratively
- the most effective approach is to iterate on a single challenging task until claude succeeds, then extract that approach into your skill. test for:
    - **triggering:** does it load when it should? does it avoid false positives?
    - **functionality:** does it produce correct outputs consistently?
    - **performance:** is it better than the baseline (no skill)?
- the [SKILLS.sh](http://SKILLS.sh) CLI
- in early 2026, vercel released [skills.sh](http://skills.sh) a command-line tool that has become the npm for ai agents. this cli helps install, and manage skills across different ai platforms.
- basic installation: # Install a skill from GitHubnpx skills add vercel-labs/agent-skills# Install a specific skill from a reponpx skills add vercel-labs/agent-skills@vercel-react-best-practices# Install from a direct pathnpx skills add https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines# List installed skillsnpx skills list# Check for updatesnpx skills check# Update all skillsnpx skills update
- the [skills.sh](http://skills.sh) cli automatically detects which ai coding agents you have installed and configures skills appropriately. It currently supports 35+ agents including claude code, cursor, codex, open code, windsurf and many more.

### advanced Patterns and best practices

- pattern 1: context-aware tool selection
- smart skills adapt based on context. for file storage: Decision Tree:1. Check file type and size2. Determine best storage: - Large files (>10MB): Cloud storage MCP - Collaborative docs: Notion/Docs MCP - Code files: GitHub MCP - Temporary files: Local storage3. Execute with appropriate tool4. Explain choice to user
- pattern 2: domain-specific intelligence
- skills can embed specialized knowledge
- Before Processing (Compliance Check): 1. Fetch transaction details via MCP 2. Apply compliance rules: - Check sanctions lists - Verify jurisdiction allowances - Assess risk level 3. Document compliance decision Processing: IF compliance passed: - Process transaction - Apply fraud checks ELSE: - Flag for review - Create compliance case
- pattern 3: iterative refinement
- for quality-critical outputs: Initial Draft:- Generate first version- Save to temporary fileQuality Check:- Run validation script- Identify issuesRefinement Loop:- Address each issue- Regenerate affected sections- Re-validate- Repeat until quality threshold met

### the future of agent skills

- the ai industry is shifting focus from raw model capabilities to practical utility. skills represent this evolution moving from impressive demos to production workflows that deliver measurable business value.
- based on current trajectories:
- **1. skills as competitive differentiator** companies with robust skill libraries will have a productivity advantage. early movers are building internal skill repositories as strategic assets.
- **2. skill marketplaces** we're already seeing commercial skill marketplaces emerge, similar to app stores, where specialized skills can be purchased for specific industries or use cases.
- **3. ai-assisted skill creation** the skill-creator skill demonstrates ai building ai capabilities. this recursive improvement will accelerate future versions might generate complex skills from natural language descriptions.
- **4. skills for agent orchestration** as multi-agent systems become more common, skills will evolve to coordinate multiple ai agents working in concert on complex projects.
- **5. regulatory and compliance skills** in highly regulated industries (finance, healthcare, legal), skills encoding compliance rules and audit trails will become essential.

### practical recommendations

- for teams and organizations:
- **identify high-value workflows:** where do team members repeatedly explain the same processes to ai? those are prime skill candidates. **create a skills repository:** version control your organizational skills in Git. share them across teams and iterate based on feedback. **standardize on the open spec:** build skills using the open standard to ensure portability as the ai landscape evolves. **invest in skill maintenance:** like any code, skills need updates. assign ownership and establish review processes.
