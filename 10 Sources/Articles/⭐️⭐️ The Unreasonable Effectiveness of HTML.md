---
type: article
status: raw
quality: 2
topics: [ai-coding, ai-tooling, mental-models]
source: https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html
created: 2026-08-09
published: 2026-05-20
author: Claude
flashcards: none
updated: 2026-08-11
---

# The Unreasonable Effectiveness of HTML

<div align="center">
  <img src="https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a0cce59a622f528451f4830_og_using-claude-code-the-unreasonable-effectiveness-of-html.jpg" width="220" />
</div>


## Why use HTML?


### Information density


![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a0cc2df7520821249c2495c_image10.png)

- It can, of course, do simple document structure like headers and formatting, but it can also represent all sorts of other information such as:
    - Tabular data using tables
    - Design data with CSS
    - Illustrations with SVG
    - Code snippets with script tags
    - Interactions using HTML elements with javascript + CSS
    - Workflows using SVG and HTML
    - Spatial data using absolute positions and canvases
    - Images using image tags
- makes it a highly efficient way for the model to communicate in-depth information to you and for you to review it.

### Visual clarity and ease of reading


![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a0cccd2c085977fc720eb48_343de6c4.png)

- I’ve found that I tend to not actually read more than a 100-line Markdown file, and I certainly am not able to get anyone else in my organization to read it.
- HTML documents are much easier to read because Claude can organize the structure visually to be ideal to navigate with tabs, illustrations, and links.

### Ease of sharing

- Markdown files are fairly hard to share since most browsers do not render them natively well.
- As long as you upload the HTML file, you can share the link easily.

### Two-way interactions

- HTML can also allow you to [interact with the document](https://x.com/trq212/status/2017024445244924382); for example, you might want to ask it to add sliders or knobs to adjust a design or allow you to tweak different options in the algorithm to see what happens.
- One thing worth noting: you don't need to do much to get Claude to generate HTML like this. You can simply prompt it to "*make an HTML file*" or "*make an HTML artifact*."
- Over time, it may make sense to build a skill around recurring patterns

### Use cases


#### Specs, planning, and exploration

- HTML is a rich canvas for Claude to dive into a problem. When I start working on a problem instead of a simple Markdown plan I expect to make a web of HTML files.
- Finally, when I feel good I’ll ask it to write an implementation plan. When I’m happy with the plan I’ll create a new session and pass in all of these files for it to implement.

#### Code review and understanding

- Code can be difficult to read in a Markdown file, but with HTML, we can render diffs, annotations, flowcharts, and modules.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a0cccd2c085977fc720eb5f_ce1ada20.png)

- Help me review this PR by creating an HTML artifact that describes it. I'm not very familiar with the streaming/backpressure logic, so focus on that. Render the actual diff with inline margin annotations, color-code findings by severity and whatever else might be needed to convey the concept well.

#### Design and prototypes

- You can also prototype interactions, such as animations, actions, etc. Consider asking Claude to make sliders, knobs, etc. to tune in exactly what you’re looking for.

#### Reports, research, and learning

- Claude Code is very effective at synthesizing information across multiple data sources and converting it into a report for readability.
- You could assemble this in the form of a long HTML document, an interactive explainer or even a slideshow/deck. Ask Claude to use SVG for diagrams to help visualize it.
- I don't understand how our rate limiter actually works. Read the relevant code and produce a single HTML explainer page: a diagram of the token-bucket flow, the 3–4 key code snippets annotated, and a "gotchas" section at the bottom. Optimize it for someone reading it once.
- **Use this for:**
    - Writing feature summarizations
    - Generating explainers
    - Drafting weekly status reports
    - Creating incident reports
    - Producing SVG illustrations, flowcharts, and technical diagrams,

#### Custom editing interfaces

- Sometimes it’s hard to describe what you want purely in a text box. For this use case, I'll often ask Claude to build me a throwaway editor for the exact thing I'm working on: not a product, or a reusable tool, but a single HTML file, purpose-built for this one piece of data.
- The trick is always to end with an export: a "copy as JSON" or "copy as prompt" button that turns whatever I did in the UI back into something I can paste into Claude Code or commit to a file.

![](https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/6a0cccd2c085977fc720eb57_0e3ace42.png)

- **Example prompts:**
    - *I need to reprioritize these 30 Linear tickets. Make me an HTML file with each ticket as a draggable card across Now / Next / Later / Cut columns. Pre-sort them by your best guess. Add a "copy as Markdown" button that exports the final ordering with a one-line rationale per bucket.*
    - *Here's our feature flag config. Build a form-based editor for it, group flags by area, show dependencies between them, warn me if I enable a flag whose prerequisite is off. Add a "copy diff" button that gives me just the changed keys.*
    - *I'm tuning this system prompt. Make a side-by-side editor: editable prompt on the left with the variable slots highlighted, three sample inputs on the right that re-render the filled template live. Add a character/token counter and a copy button.*
- • Reordering, triaging, or bucketing anything (tickets, test cases, feedback) • Editing structured config (feature flags, env vars, JSON/YAML with constraints) • Tuning prompts, templates, or copy with live preview
- Annotating a document, transcript, or diff and exporting the annotations
