---
type: article
status: structured
quality:
topics: [agent-evaluation, model-monitoring, llm-evaluation]
source: ""
created: 2025-05-31
published:
author: ""
flashcards: none
updated: 2025-12-28
---
- [[#1 Eval-driven development|1 Eval-driven development]]
	- [[#1 Eval-driven development#1.1 Component level testing|1.1 Component level testing]]
	- [[#1 Eval-driven development#1.2 Software testing vs Agent Testing|1.2 Software testing vs Agent Testing]]
	- [[#1 Eval-driven development#1.3 Tools for agent evals|1.3 Tools for agent evals]]
- [[#2 Decomposing agents|2 Decomposing agents]]
	- [[#2 Decomposing agents#2.1 Example Agent for our code|2.1 Example Agent for our code]]
- [[#3 Tracing agents|3 Tracing agents]]
- [[#4 Adding router and skill evals|4 Adding router and skill evals]]
	- [[#4 Adding router and skill evals#4.1 Evals for components|4.1 Evals for components]]
	- [[#4 Adding router and skill evals#4.2 Lab implementation|4.2 Lab implementation]]
- [[#5 Trajectory Evals|5 Trajectory Evals]]
	- [[#5 Trajectory Evals#5.1 Lab implementation|5.1 Lab implementation]]
- [[#6 Adding structure to evals|6 Adding structure to evals]]
	- [[#6 Adding structure to evals#6.1 Lab implementation|6.1 Lab implementation]]
- [[#7 Monitoring agents|7 Monitoring agents]]

# 1 Eval-driven development
- scope of evaluation 
	- LLM model eval - general language understanding of LLM e.g. benchmarks
	- LLM system eval - how well application w LLM performs or meets business goals
		- uses testing datasets - can be manually created, synthetically created or curated 
## 1.1 Component level testing
- for LLM-based applications, you may have many components
	- inputs → prompt, tools, memory, data sources → output
	- can then test each part and the whole
		- in SWE - unit + integration testing
		- however, you don't get determinism like in SWE
		- also focuses on output quality or open ended metrics 
- agents have 3 broad components
	- reasoning - powered by LLM
	- routing - interpreting request + determining correct tool
	- action - executing code/tools (using APIs, calling other agent)
- 💡 TIP: **think about what can go wrong at each step, and use that to build your evals**
	- e.g. Trip planning agent - "Book me a trip to ...."
	- can use human feedback or HITL or LLM-as-judge

| step                          | eval                  | what could go wrong?                                                             | LLM-judge? |
| ----------------------------- | --------------------- | -------------------------------------------------------------------------------- | ---------- |
| figure out which tool to call | tool selection eval   | <span style="color:rgb(255, 136, 0)">calls wrong tool</span>                     | yes        |
| search API                    | function callign eval | <span style="color:rgb(255, 136, 0)">constructs search incorrectly</span>        |            |
| use context                   | RAG eval              |                                                                                  | yes        |
| construct a response          | tone eval             | <span style="color:rgb(255, 136, 0)">could be jailbroken or inappropriate</span> | yes        |
| overall correctness           | correctness eval      | <span style="color:rgb(255, 136, 0)">unhappy user</span>                         |            |

- remember small changes (e.g. prompt tweak) can cause unexpected test regressions
	- hence make sure test cases are diverse and representative
	- then for each change, you can re-run evals and see impacts

## 1.2 Software testing vs Agent Testing
- software
	- software is **deterministic**
	- unit tests are **deterministic**
	- integration tests rely on existing code + documentation
- agents
	- agents are **non-deterministic**
	- agents can have **multiple paths**
	- improving agents **relies on data** 
## 1.3 Tools for agent evals
- trace instrumentation
- eval runner or harness
- datasets
- human feedback
- playground/synthetic data 

---

# 2 Decomposing agents
- 3 main components
	- <mark style="background: #FFB8EBA6;">router</mark> - responsible for handling user inputs + outputs
		- the main planner of the agent 
		- decides which skill/function to call to answer user query
		- can be an LLM, NLP classifier or even rule-based
		- some agents distribute router logic throughout agent system instead of single router
	- <mark style="background: #FFB8EBA6;">skills</mark> - e.g. the tools or actions available
		- individual logic blocks + capabilities to complete tasks
		- each agent has 1 or more skills
		- made up of individual steps e.g. LLM calls, application code, API calls etc 
			- e.g. RAG skill - handles embedding, vector search, retrieving context 
	- <mark style="background: #FFB8EBA6;">memory and state</mark> - where agents update actions/outputs etc
		- shared state to store and access information 
		- used to store retrieved context, config variables, previous agent execution
			- past agent execution most common - usually in form of dictionary e.g. below

```python
messages = []
messages.append({
	"role": "system", 
	"content": "You are a helpful customer support assistant. Use the supplied tools to assist the user."
})
messages.append({
	"role": "user", 
	"content": "Hi, can you tell me the delivery date for my order?"
})
messages.append({
	"role": "assistant", 
	"content": "Hi there! I can help with that. Can you please provide your order ID?"
})
messages.append({
	"role": "user", 
	"content": "i think it is order_12345"
})
```

## 2.1 Example Agent for our code
- our example will use data analysis agent with 3 skills
	- data lookup skill - query to DB
	- data analysis skill - draw conclusions from data
	- data viz skills - generate graphs + viz on data 

![[Screenshot 2025-05-31 at 4.47.38 pm.png| center | 600]]


---

# 3 Tracing agents
- traces allow for observability/logs for tracking the agent steps, and instrumentation = adding code to allow for tracing 
	- <mark style="background: #FFB8EBA6;">traces</mark> = full run paths of the application through all steps
		- comprised of spans
	- <mark style="background: #FFB8EBA6;">spans</mark> = a single step in the app or pipeline
		- spans can be nested 
		- spans can be colour coded for type e.g. LLM call, tool, chained spans etc 
	- typically represented heirarchically 

![[Screenshot 2025-05-31 at 5.17.32 pm.png| center | 500]]

![[Screenshot 2025-05-31 at 5.20.56 pm.png| center | 500]]


- why observability is important
	- simplifies debugging when developing
	- provides detailed log of all steps - the bedrock for evals
	- helps you understand unpredictable behaviour of LLMs

---

# 4 Adding router and skill evals
- 4 types of evals
	- <mark style="background: #FFB8EBA6;">code-based evals</mark> = regex, JSON parseable, contains keywords 
	- <mark style="background: #FFB8EBA6;">similarity to ground-truth evals</mark> = cosine similarity to human annotations
	- <mark style="background: #FFB8EBA6;">LLM-as-judge evals</mark> = separate LLM with rubric to eval, some tips:
		- strongest models align w human judgement - so use the best available
		- LLM judge is never 100% accurate
		- tuning LLM judge prompt can help close the gap 
		- never use scores e.g. 100%, use discrete classification labels e.g. Pass, Fail
	- <mark style="background: #FFB8EBA6;">human annotations</mark> = annotation queues having human labellers judge the response
		- e.g. critiques, overall pass/fail etc 

![[Screenshot 2025-05-31 at 6.41.43 pm.png| center | 500]]

## 4.1 Evals for components
- router - function choice and parameter extraction 
	- example prompt for LLM-judge to eval router

```python
TOOL_CALLING_PROMPT_TEMPLATE = f"""
You are an evaluation assistant evaluating questions and tool calls to determine whether the tool called would answer the question. The tool calls have been generated by a separate agent, and chosen from the list of tools provided below. It is your job to decide whether that agent chose the right tool to call.

[BEGIN DATA]
************
[Question]: {question}
************
[Tool Called]: {tool_call}
[END DATA]

Your response must be single word, either "correct" or "incorrect", and should not contain any text or characters aside from that word.
"incorrect" means that the chosen tool would not answer the question, the tool includes information that is not presented in the question, or that the tool signature includes parameter values that don't match the formats specified in the tool signatures below.
"correct" means the correct tool call was chosen, the correct parameters were extracted from the question, the tool call generated is runnable and correct, and that no outside information not present in the question was used in the generated question.

[Tool Definitions]: {tool_definitions}
"""
```

- skills/functions - use standard LLM evals
	- see below for popular choices depending on what you are eval-ing

| LLM as judge     | Code-based   |
| ---------------- | ------------ |
| relevance        | regex        |
| hallucination    | JSON parsing |
| QA correctness   |              |
| code readability |              |
| summarisation    |              |

![[Screenshot 2025-05-31 at 6.50.58 pm.png| center | 600]]

- trajectory - most challenging to eval at scale, covered later
## 4.2 Lab implementation

![[Screenshot 2025-06-01 at 11.41.06 am.png| center | 500]]

- setup

```python
import warnings
warnings.filterwarnings('ignore')

import phoenix as px
import os
import json
from tqdm import tqdm
from phoenix.evals import (
    TOOL_CALLING_PROMPT_TEMPLATE, 
    llm_classify,
    OpenAIModel
)
from phoenix.trace import SpanEvaluations
from phoenix.trace.dsl import SpanQuery
from openinference.instrumentation import suppress_tracing

import nest_asyncio
nest_asyncio.apply()

# set name for Arize Project + import agent from last lab
PROJECT_NAME = "evaluating-agent"
from utils import run_agent, start_main_span, tools, get_phoenix_endpoint

# running set of questions to get the traces + spans
agent_questions = [
    "What was the most popular product SKU?",
    "What was the total revenue across all stores?",
    "Which store had the highest sales volume?",
    "Create a bar chart showing total sales by store",
    "What percentage of items were sold on promotion?",
    "What was the average transaction value?"
]

for question in tqdm(agent_questions, desc="Processing questions"):
    try:
        ret = start_main_span([{"role": "user", "content": question}])
    except Exception as e:
        print(f"Error processing question: {question}")
        print(e)
        continue
```

- what the Arize traces look like

![[Screenshot 2025-06-01 at 11.42.27 am.png| center | 500]]

![[Screenshot 2025-06-01 at 11.42.50 am.png| center | 500]]

- 1st eval = LLM-as-a-judge for correctness of the router's function calling choice + correctness of the parameters extracted
	- using the prompt template for LLM-judge as above
	- query the required spans - by selecting only the specific one (`kind = LLM`)

```python
query = SpanQuery().where(
    # Filter for the `LLM` span kind.
    # The filter condition is a string of valid Python boolean expression.
    "span_kind == 'LLM'",
).select(
    question="input.value",
    tool_call="llm.tools"
)

# The Phoenix Client can take this query and return the dataframe.
tool_calls_df = px.Client().query_spans(
	query, 
	project_name=PROJECT_NAME, 
	timeout=None
)
tool_calls_df = tool_calls_df.dropna(subset=["tool_call"])

tool_calls_df.head()
# ---------------------
# context.span_id	question	                                        tool_call
# 9f4aedf8b1afe7bf	{"messages": [{"role": "user", "content": "Wha...	[{'tool': {'json_schema': '{"type": "function"...
# ea6c1209207ccfd9	{"messages": [{"role": "user", "content": "Wha...	[{'tool': {'json_schema': '{"type": "function"...
# ea2f7516c124216f	{"messages": [{"role": "user", "content": "Wha...	[{'tool': {'json_schema': '{"type": "function"...
# 8d7a196b6a418596	{"messages": [{"role": "user", "content": "Wha...	[{'tool': {'json_schema': '{"type": "function"...
# d53f5e3d5ec0ae7e	{"messages": [{"role": "user", "content": "Whi...	[{'tool': {'json_schema': '{"type": "function"...
```

- next we continue to evaluate the tool calling 
	- we suppress tracing since we do not want new traces for the LLM-judge
	- using phoenix method `llm_classify` 
	- adding numeric value for score for later viz 

```python
with suppress_tracing():
    tool_call_eval = llm_classify(
        dataframe = tool_calls_df,
        template = TOOL_CALLING_PROMPT_TEMPLATE.template[0].template.replace(
	        "{tool_definitions}", 
			json.dumps(tools).replace("{", '"').replace("}", '"')
		),
        rails = ['correct', 'incorrect'],
        model=OpenAIModel(model="gpt-4o"),
        provide_explanation=True
    )

tool_call_eval['score'] = tool_call_eval.apply(lambda x: 1 if x['label']=='correct' else 0, axis=1)
tool_call_eval.head()


# context.span_id	label	explanation	            exceptions	execution_status  execution_seconds	score
# 9f4aedf8b1afe7bf	correct	The question asks ...	[]	COMPLETED	0.054214	1
# ea6c1209207ccfd9	correct	The question asks ...	[]	COMPLETED	0.138580	1
# ea2f7516c124216f	correct	The question asks ...	[]	COMPLETED	0.242894	1
# 8d7a196b6a418596	correct	The question asks ...	[]	COMPLETED	0.338056	1
# d53f5e3d5ec0ae7e	correct	The question asks ...	[]	COMPLETED	0.437899	1

```

- we then log these evals back to phoenix 
	- attaches the scores back to the traces we just evaluated 

```python
px.Client().log_evaluations(
    SpanEvaluations(eval_name="Tool Calling Eval", dataframe=tool_call_eval),
)
```

- next we eval the correctness of the code i.e. can it run?

```python
def code_is_runnable(output: str) -> bool:
    """Check if the code is runnable"""
    output = output.strip()
    output = output.replace("```python", "").replace("```", "")
    try:
        exec(output)
        return True
    except Exception as e:
        return False

code_gen_df["label"] = code_gen_df["generated_code"].apply(code_is_runnable).map({True: "runnable", False: "not_runnable"})
code_gen_df["score"] = code_gen_df["label"].map({"runnable": 1, "not_runnable": 0})
```

- lastly evaluating clarity of the analysis

```python
CLARITY_LLM_JUDGE_PROMPT = f"""
In this task, you will be presented with a query and an answer. Your objective is to evaluate the clarity 
of the answer in addressing the query. A clear response is one that is precise, coherent, and directly 
addresses the query without introducing unnecessary complexity or ambiguity. An unclear response is one 
that is vague, disorganized, or difficult to understand, even if it may be factually correct.

Your response should be a single word: either "clear" or "unclear," and it should not include any other 
text or characters. "clear" indicates that the answer is well-structured, easy to understand, and 
appropriately addresses the query. "unclear" indicates that some part of the response could be better 
structured or worded.
Please carefully consider the query and answer before determining your response.

After analyzing the query and the answer, you must write a detailed explanation of your reasoning to 
justify why you chose either "clear" or "unclear." Avoid stating the final label at the beginning of your 
explanation. Your reasoning should include specific points about how the answer does or does not meet the 
criteria for clarity.

[BEGIN DATA]
Query: {query}
Answer: {response}
[END DATA]
Please analyze the data carefully and provide an explanation followed by your response.

EXPLANATION: Provide your reasoning step by step, evaluating the clarity of the answer based on the query.
LABEL: "clear" or "unclear"
"""
```

---

# 5 Trajectory Evals
- can the agent answer the user query in a reasonable number of steps
	- <mark style="background: #FFB8EBA6;">trajectory</mark> = path through the router steps, tool calls, and logic steps agent takes for a given input
- example of 2 simple trajectories
	- note: these can get a lot more complicated over time e.g. multi-agent systems, big tool libraries etc 

![[Screenshot 2025-06-01 at 11.59.51 am.png| center | 500]]


>[!question] Does trajectory matter when the agent final output is correct?
> Yes! since efficiency matter as well as breaking down where things went wrong e.g. 
> - inefficient trajectory
> 	1. user input
> 	2. router
> 	3. database lookup tool
> 	4. router
> 	5. data analyser
> 	6. router
> 	7. database lookup tool
> 	8. router
> 	9. data analyser
> 	10. router
> 	11. output
> - better trajectory 
> 	1. user input
> 	2. router
> 	3. database lookup tool
> 	4. data analyser
> 	5. router
> 	6. output

- <mark style="background: #FFB8EBA6;">convergence</mark> = how closely your agent follows the optimal path for a given query 
	- i.e. what % of time does agent take optimal path
		- always between 0 and 1 
	- how to test for convergence
		- **run agent on a set of similar queries**
			- need to be similar enough that you expect same path to be taken for each
			- $N$ = total number of runs
		- **record number of steps taken for each**
			- $S_{\text{agent},i}$ = steps taken by agent in the $i$'th run
		- **find length of the optimal path** 
			- $S_{\text{optimal}} = min(S_{\text{agent}, 1}, S_{\text{agent}, 2}, ..., S_{\text{agent}, N})$  i.e. minimum steps across all runs
		- **calculate convergence score** 

$$
\large
\text{Overall Convergence Score} = \frac{\sum^N_{i=1} min(1, \frac{S_{optimal}}{S_{agent,i}})}{N}
$$

- note: convergence evals cautions:
	- will not capture situations where unecessary step is taken by agent every time 
	- they must check the agent fully completed a run - not just partially
## 5.1 Lab implementation

![[Screenshot 2025-06-01 at 1.03.29 pm.png| center | 500]]

- creating a dataset of test cases, then creating the task

```python
convergence_questions = [
    "What was the average quantity sold per transaction?",
    "What is the mean number of items per sale?", 
    "Calculate the typical quantity per transaction",
    "What's the mean transaction size in terms of quantity?",
    "On average, how many items were purchased per transaction?",
    "What is the average basket size per sale?",
    "Calculate the mean number of products per purchase",
    "What's the typical number of units per order?",
    "What is the average number of products bought per purchase?",
    "Tell me the mean quantity of items in a typical transaction",
    "How many items does a customer buy on average per transaction?",
    "What's the usual number of units in each sale?",
    "What is the typical amount of products per transaction?",
    "Show the mean number of items customers purchase per visit",
    "What's the average quantity of units per shopping trip?",
    "How many products do customers typically buy in one transaction?",
    "What is the standard basket size in terms of quantity?"
]

convergence_df = pd.DataFrame({
    'question': convergence_questions
})

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
dataset = px_client.upload_dataset(dataframe=convergence_df, 
                                   dataset_name=f"convergence_questions-{now}",
                                   input_keys=["question"])
```

```python
# helper method to format the output returned by the task
def format_message_steps(messages):
    """
    Convert a list of message objects into a readable format that shows the steps taken.

    Args:
        messages (list): A list of message objects containing role, content, tool calls, etc.

    Returns:
        str: A readable string showing the steps taken.
    """
    steps = []
    for message in messages:
        role = message.get("role")
        if role == "user":
            steps.append(f"User: {message.get('content')}")
        elif role == "system":
            steps.append("System: Provided context")
        elif role == "assistant":
            if message.get("tool_calls"):
                for tool_call in message["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    steps.append(f"Assistant: Called tool '{tool_name}'")
            else:
                steps.append(f"Assistant: {message.get('content')}")
        elif role == "tool":
            steps.append(f"Tool response: {message.get('content')}")
    
    return "\n".join(steps)
```

```python
def run_agent_and_track_path(example: Example) -> str:
    messages = [{"role": "user", "content": example.input.get("question")}]
    ret = run_agent(messages)
    return {"path_length": len(ret), "messages": format_message_steps(ret)}
```

---

# 6 Adding structure to evals
- <mark style="background: #FFB8EBA6;">Eval-driven development</mark> = using evals + measurements from agents to guide where you spend time improving your system
	- note - this is often an iterative process e.g. creating more evals, test cases etc 
- steps
	- **curate a dataset of various examples**
		- at least 25+ examples of inputs - should be comprehensive + representative of what you expect
		- e.g. few examples of each type
		- can be sourced from live historic runs, or constructed beforehand 
		- attached expected outputs to these test cases 
			- not always needed (e.g. LLM-judge) but expands number of evaluation methods available to you
	- **run examples through system, tracking changes as an experiment**
		- an experiment is single test with the proposed changes to your agent 
			- prompt iterations
			- tool definitions
			- router logic 
			- skill structure
			- model changes 
	- **evaluate the experiments through evaluators**
		- experiments are the structure you use to run curated test cases through the agent + record results
		- use same evaluators from above
			- <span style="color:rgb(255, 136, 0)">code-based evals</span> 
				- compare to ground-truth
				- is code runnable 
				- convergence
			- <span style="color:rgb(255, 136, 0)">LLM-as-judge evals</span>
				- function calling
				- analysis clarity
				- entity correctness
		- final aggregated output will be scores you can compare to each other 
- example of types of experiments + evals for various components

![[Screenshot 2025-06-01 at 1.19.22 pm.png| center | 600]]

- as you iterate, you can **bring real data back into your datasets for experiments**
## 6.1 Lab implementation
- create dataset of test cases

```python
overall_experiment_questions = [
    {'question': 'What was the most popular product SKU?',
     'sql_result': 'SKU_Coded 6200700 Total_Qty_Sold 52262',
     'sql_generated': 'SELECT SKU_Coded, SUM(Qty_Sold) AS Total_Qty_Sold FROM sales GROUP BY SKU_Coded ORDER BY Total_Qty_Sold DESC LIMIT 1;'},
    {'question': 'What was the total revenue across all stores?',
     'sql_result': 'Total_Revenue 1.327264e+07',
     'sql_generated': 'SELECT SUM(Total_Sale_Value) AS Total_Revenue FROM sales;'},
    {'question': 'Which store had the highest sales volume?',
     'sql_result': 'Store_Number 2970 Total_Sales_Volume 59322.0',
     'sql_generated': 'SELECT Store_Number, SUM(Total_Sale_Value) AS Total_Sales_Volume FROM sales GROUP BY Store_Number ORDER BY Total_Sales_Volume DESC LIMIT 1;'},
    {'question': 'Create a bar chart showing total sales by store',
     'sql_result': 'Store_Number 880 Total_Sales 420302.09; 1650 580443.01; … 1870 401070.99',
     'sql_generated': 'SELECT Store_Number, SUM(Total_Sale_Value) AS Total_Sales FROM sales GROUP BY Store_Number;'},
    {'question': 'What percentage of items were sold on promotion?',
     'sql_result': 'Promotion_Percentage 0.625596',
     'sql_generated': 'SELECT (SUM(CASE WHEN On_Promo=\'Yes\' THEN 1 ELSE 0 END)*100.0)/COUNT(*) AS Promotion_Percentage FROM sales;'},
    {'question': 'What was the average transaction value?',
     'sql_result': 'Average_Transaction_Value 19.018132',
     'sql_generated': 'SELECT AVG(Total_Sale_Value) AS Average_Transaction_Value FROM sales;'},
    {'question': 'Create a line chart showing sales in 2021',
     'sql_result': 'sale_month 2021-11-01 total_quantity_sold 43056.0 total_sales_value 499984.43; 2021-12-01 75724.0 910982.12',
     'sql_generated': 'SELECT MONTH(Sold_Date) AS Month, SUM(Total_Sale_Value) AS Total_Sales FROM sales WHERE YEAR(Sold_Date)=2021 GROUP BY MONTH(Sold_Date) ORDER BY MONTH(Sold_Date);'}
]

overall_experiment_df = pd.DataFrame(overall_experiment_questions)

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# create a dataset consisting of input questions and expected outputs
dataset = px_client.upload_dataset(dataframe=overall_experiment_df, 
                                   dataset_name=f"overall_experiment_inputs-{now}", 
                                   input_keys=["question"], 
                                   output_keys=["sql_result", "sql_generated"])
```

- set up evaluators, evaluators take the following parameters
		- **input**: the input field of your dataset examples, has only one key: `"question"` 
		- **output**: the output field added to your dataset examples, after you apply the task to each example
			- structure of output defined by task which is defined in the code below `run_agent_task`
			- task returns a processed version of agent's messages - as a dictionary that organises messages into the keys
				- "tool_calls", "tool_responses", "final_output", "unchanged_messages" and "path_length"
		- **expected**: the expected output field of your dataset examples 
			- has two keys: "sql_result" and "sql_generated"

```python
CLARITY_LLM_JUDGE_PROMPT = f"""
In this task, you will be presented with a query and an answer. Your objective is to evaluate the clarity 
of the answer in addressing the query. A clear response is one that is precise, coherent, and directly 
addresses the query without introducing unnecessary complexity or ambiguity. An unclear response is one 
that is vague, disorganized, or difficult to understand, even if it may be factually correct.

Your response should be a single word: either "clear" or "unclear," and it should not include any other 
text or characters. "clear" indicates that the answer is well-structured, easy to understand, and 
appropriately addresses the query. "unclear" indicates that the answer is ambiguous, poorly organized, or 
not effectively communicated. Please carefully consider the query and answer before determining your 
response.

After analyzing the query and the answer, you must write a detailed explanation of your reasoning to 
justify why you chose either "clear" or "unclear." Avoid stating the final label at the beginning of your 
explanation. Your reasoning should include specific points about how the answer does or does not meet the 
criteria for clarity.

[BEGIN DATA]
Query: {query}
Answer: {response}
[END DATA]
Please analyze the data carefully and provide an explanation followed by your response.

EXPLANATION: Provide your reasoning step by step, evaluating the clarity of the answer based on the query.
LABEL: "clear" or "unclear"
"""
```

```python
ENTITY_CORRECTNESS_LLM_JUDGE_PROMPT = f"""
In this task, you will be presented with a query and an answer. Your objective is to determine whether all 
the entities mentioned in the answer are correctly identified and accurately match those in the query. An 
entity refers to any specific person, place, organization, date, or other proper noun. Your evaluation 
should focus on whether the entities in the answer are correctly named and appropriately associated with 
the context in the query.

Your response should be a single word: either "correct" or "incorrect," and it should not include any 
other text or characters. "correct" indicates that all entities mentioned in the answer match those in the 
query and are properly identified. "incorrect" indicates that the answer contains errors or mismatches in 
the entities referenced compared to the query.

After analyzing the query and the answer, you must write a detailed explanation of your reasoning to 
justify why you chose either "correct" or "incorrect." Avoid stating the final label at the beginning of 
your explanation. Your reasoning should include specific points about how the entities in the answer do or 
do not match the entities in the query.

[BEGIN DATA]
Query: {query}
Answer: {response}
[END DATA]
Please analyze the data carefully and provide an explanation followed by your response.

EXPLANATION: Provide your reasoning step by step, evaluating whether the entities in the answer are 
correct and consistent with the query.
LABEL: "correct" or "incorrect"
"""
```

```python
# evaluator for the router
def function_calling_eval(input: str, output: str) -> float:
    if output is None:
        return 0
    function_calls = output.get("tool_calls")
    if function_calls:
        eval_df = pd.DataFrame({
            "question": [input.get("question")] * len(function_calls),
            "tool_call": function_calls
        })
            
        tool_call_eval = llm_classify(
            data = eval_df,
            template = TOOL_CALLING_PROMPT_TEMPLATE.template[0].template.replace("{tool_definitions}", 
                                                                                 json.dumps(tools).replace("{", '"').replace("}", '"')),
            rails = ['correct', 'incorrect'],
            model=eval_model,
            provide_explanation=True
        )

        tool_call_eval['score'] = tool_call_eval.apply(lambda x: 1 if x['label']=='correct' else 0, axis=1)
        return tool_call_eval['score'].mean()
    else:
        return 0

# evaluator for tool 1: database lookup
def evaluate_sql_result(output, expected) -> bool:    
    if output is None:
        return False
    sql_result = output.get("tool_responses")
    if not sql_result:
        return True
    
    # Find first lookup_sales_data response
    sql_result = next((r for r in sql_result if r.get("tool_name") == "lookup_sales_data"), None)
    if not sql_result:
        return True
        
    # Get the first response
    sql_result = sql_result.get("tool_response", "")

    # Extract just the numbers from both strings
    result_nums = ''.join(filter(str.isdigit, sql_result))
    expected_nums = ''.join(filter(str.isdigit, expected.get("sql_result")))
    return result_nums == expected_nums

# evaluator for tool 2: data analysis
def evaluate_clarity(output: str, input: str) -> bool:
    if output is None:
        return False
    df = pd.DataFrame({"query": [input.get("question")],
                       "response": [output.get("final_output")]})
    response = llm_classify(
        data=df,
        template=CLARITY_LLM_JUDGE_PROMPT,
        rails=["clear", "unclear"],
        model=eval_model,
        provide_explanation=True
    )
    return response['label'] == 'clear'

# evaluator for tool 2: data analysis
def evaluate_entity_correctness(output: str, input: str) -> bool:
    if output is None:
        return False
    df = pd.DataFrame({"query": [input.get("question")], 
                       "response": [output.get("final_output")]})
    response = llm_classify(
        data=df,
        template=ENTITY_CORRECTNESS_LLM_JUDGE_PROMPT,
        rails=["correct", "incorrect"],
        model=eval_model,
        provide_explanation=True
    )
    return response['label'] == 'correct'

# evaluator for tool 3: data visualization   
def code_is_runnable(output: str) -> bool:
    """Check if the code is runnable"""
    if output is None:
        return False
    generated_code = output.get("tool_responses")
    if not generated_code:
        return True
    
    # Find first lookup_sales_data response
    generated_code = next((r for r in generated_code if r.get("tool_name") == "generate_visualization"), None)
    if not generated_code:
        return True
        
    # Get the first response
    generated_code = generated_code.get("tool_response", "")
    generated_code = generated_code.strip()
    generated_code = generated_code.replace("```python", "").replace("```", "")
    try:
        exec(generated_code)
        return True
    except Exception as e:
        return False
```

```python
def run_agent_task(example: Example) -> str:
    print("Starting agent with messages:", example.input.get("question"))
    messages = [{"role": "user", "content": example.input.get("question")}]
    ret = run_agent(messages)
    return process_messages(ret)
```


---

# 7 Monitoring agents

![[Screenshot 2025-06-01 at 1.30.02 pm.png| center | 600]]
- what's different about production
	- discover new failure modes - e.g. new queries or use-cases
	- higher complexity - e.g. external APIs or other agents
	- making changes to agents - AB testing and evaluating using data which can introduce suprising regressions
- tools for managing agent performance in prod
	- **instrumentation and feedback**
		- crucial to collect user feedback and data for evals - via tracing and annotations
		- define areas of improvement by looking at your results
	- **monitoring metrics**
		- efficiency of your system e.g. convergence evals
			- ensure this does not degrade over time e.g. tweaking a prompt that might cause suprise regression
		- dependencies on external services - latency and cost 
			- ensure you monitor external LLM calls - they can have big downstream impact on user
			- e.g. reasoning model vs smaller model for certain component
	- **CI/CD** - continuous improvement 
		- collect user feedback (human labels) to understand end-to-end agent performance 
		- curate datasets for continuous experimentation as you iterate
			- datasets become representative of specific failure modes + general performance -> golden-truth
				- to make sure you don't break something you've already solved before 
			- experiments act as "gates" for shipping changes

![[Screenshot 2025-06-01 at 1.34.01 pm.png| center | 600]]





---











