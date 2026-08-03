---
type: article
status: distilled
quality: 2
topics: [agent-evaluation, error-analysis]
source: ""
created: 2025-12-30
published:
author: ""
flashcards: none
updated: 2025-12-31
---
- for agents with many steps, finding which step it fails the most on can be hard
	- e.g. plan > search > code > finalise etc
	- a ***transition failure matrix*** helps you find hotspots
- how a transition failure matrix works
	1. define states → list all possible steps or states the agent can be in 
	2. create a matrix → create a grid where rows are the `FROM` state and columns are the `TO` state 
	3. count failures → for each failure, identify last successful transition that occurred before the error & populate count of failures in grid cells accordingly

example of a transition matrix

```markdown
|                 | ParseReq | IntentClass | DecideTool | GenSQL | ExecSQL | PlanCal | ExecCal |
| --------------- | :------: | :---------: | :--------: | :----: | :-----: | :-----: | :-----: |
| **ParseReq**    |    0     |      3      |     0      |   0    |    0    |    0    |    0    |
| **IntentClass** |    0     |      0      |     4      |   0    |    0    |    0    |    0    |
| **DecideTool**  |    0     |      0      |     0      |   6    |    0    |    2    |    0    |
| **GenSQL**      |    0     |      0      |     0      |   0    |   12    |    0    |    0    |
| **ExecSQL**     |    0     |      0      |     0      |   0    |    0    |    5    |    0    |
| **PlanCal**     |    0     |      0      |     0      |   0    |    0    |    0    |    7    |
| **ExecCal**     |    0     |      0      |     0      |   0    |    0    |    0    |    0    |
```