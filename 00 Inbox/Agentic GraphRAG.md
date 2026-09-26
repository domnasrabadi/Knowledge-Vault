---
type: book
status: inbox
quality: 
topics: []
source: private://read/01m13whyk8ssegw20k3a9kfy10
created: 2026-09-26
published: 2026-08-19
author: Anthony Alcaraz
flashcards: none
updated: 2026-09-26
---

# Agentic GraphRAG

<div align="center">
  <img src="https://readwise-assets.s3.amazonaws.com/media/reader/parsed_document_assets/491464752/i2tWXOzgPNntJj7s-hluzfeVph9l_EA8kGp-EFl6_Ck-cove_CSYhSYm.png" width="220" />
</div>


## Preface


## Who Should Read This Book


## Why We Wrote This Book


## Why We Wrote This Book

- we’ve watched team after team pour effort into prompt scaffolding, multi-agent choreography, and ever-longer context windows—only to hit the same wall again and again.
- The wall has five recognizable cracks. We call them the five flaws of traditional architectures: context amnesia, relationship blindness, temporal ignorance, reasoning paralysis, and tool chaos. Each traces back to treating an agent as a model wrapped in a prompt rather than as a process running on top of a model.
- Graph-based architectures address all five, but the existing literature is fragmented across Google’s 2012 “strings to things” pivot, Microsoft’s GraphRAG paper, Neo4j’s design patterns, and a growing body of research on planners and self-evolving systems
- This book is that blueprint. We introduce the dual-graph architecture, which pairs a vertical knowledge graph for what the agent knows with a horizontal workflow graph for how the agent acts, and then we build out the eight pillars that make the architecture work in production. We show the pattern coming together in a single running example: an autonomous DevOps agent that starts as a pile of disconnected monitoring tools and, chapter by chapter, becomes a proactive, self-healing system.

## Acknowledgments


## Part I. Foundations of Graph-Based Agentic Systems

- I. Foundations of Graph-Based Agentic Systems

## Chapter 1. The Crisis of Enterprise Agentic AI

- 1. The Crisis of Enterprise Agentic AI
- A naive approach using simple vector-based retrieval creates five fatal flaws:
- Context amnesia LLMs are amnesia incarnate. Every conversation starts from scratch. There’s no memory of past interactions, no ability to build expertise, and no capacity to learn from mistakes.
- Relationship blindness Information sits in silos. Your agent sees the *customer* and the *purchase* but not how they connect through preferences, history, and behavior.
- Temporal ignorance Static embeddings can’t capture change. Your agent treats outdated configurations as the current truth.
- Reasoning paralysis Vector search finds similar text rather than logical connections.
- Tool chaos Without understanding tool relationships, your agent guesses which API to call instead of orchestrating intelligently.
- They represent an architectural failure that prevents your enterprise AI system from becoming truly agentic.
- Google learned this during a decade of running one of the world’s largest knowledge graphs, powering Search, Maps, and YouTube. Its key insight was the shift from “strings to things” ([Singhal, 2012](https://oreil.ly/uxJaw)).
- Graph-based agents use the following:
- Entities, not keywords They understand that *John Smith (ID:42)* is the same person across the customer relationship management (CRM) system, email, and payroll.
- Relationships, not isolation They trace how a server failure impacts dependent services before taking action.
- Evolution, not snapshots They track how configurations change over time, preventing dangerous rollbacks.
- Reasoning, not just retrieval They navigate cause-and-effect chains to predict outcomes.
- Orchestration, not guessing They understand tool dependencies to execute complex workflows.
- Constructing a knowledge graph can be challenging, and operating it in the real world necessitates iteration and improvements. Here are some of the things you need:
    - Real-time updates as your business evolves
    - Schema flexibility without breaking existing connections
    - Performance at scale (billions of relationships)
    - Governance that doesn’t strangle innovation

## Defining Agentic AI


### Classifying Agentic Systems: The Workflow-Agent Spectrum


### Classifying Agentic Systems: The Workflow-Agent Spectrum

- systems can be “agent-like to different degrees.”
- Rather than conceptualizing agents as either fully autonomous or deterministically scripted, we find it’s more productive to position your AI systems along a continuous spectrum between workflows and agents

![](https://readwise.io/reader/pcei/gAAAAABqkVp8D0Lnstmu5w5ybo76vQzSaleUGF0dhzwwJgPdo7xq5LFOknAsT31Tu8oDCxa0obFXui-oxYmivJzSzL4Y6VZZJ1okIPB7ZGj0GSojYfGJ02I=/agrg_0101.png)

- At the workflow end of this spectrum, you’re implementing systems with predefined execution paths: orchestrated sequences that follow explicit instructions. These provide reliability and deterministic outcomes but offer limited adaptability to novel situations.
- At the agent end, your systems determine processes dynamically, providing flexibility at the cost of predictability. The most common working examples of this end of the spectrum are coding agents and deep research agents.

### The Agent Constraint Triangle


### The Agent Constraint Triangle

- The *agent constraint triangle* represents three interconnected constraints that create an inherently difficult operational problem: complexity management, tool orchestration, and context utilization.
- The *complexity management constraint* concerns your agent’s ability to handle multistep planning and reasoning across complex tasks. As tasks require more steps and deeper analysis, cognitive load increases exponentially. When not managed correctly, agents struggle to maintain coherence across lengthy reasoning chains, resulting in compounding errors as the step count increases.
- The *tool orchestration constraint* involves translating between natural language instructions and precisely structured API calls.
- intensifies as the number and diversity of tools expand, creating additional potential failure points while consuming precious context space.
- The *context utilization constraint* encompasses organizing and efficiently using limited information space. Your agents operate within fixed context windows that must contain all relevant information for the task
- As tasks grow more complex, these finite context resources become increasingly constrained. Research on needle-in-a-haystack benchmarking, such as that by Chroma’s research team ([Hong, Troynikov, and Huber, 2025](https://oreil.ly/MdqMr)), has revealed the phenomenon of *context rot*: as the number of tokens in the context window increases, the model’s ability to accurately recall information from that context decreases.
- When improving performance along one dimension, you typically create additional pressure on the others:
- Complexity → tools → context As task complexity increases, more specialized tools become necessary to handle diverse operations. Each additional tool consumes context space for its definition, increases the cognitive load of tool selection, and adds more potential points of ambiguity in orchestration.
- Tools → context → complexity Expanding your tool set to handle nuanced operations depletes available context for actual task reasoning. This forces either aggressive context management (risking information loss) or simplified task decomposition (limiting capability).
- Context → complexity → tools Aggressive context optimization—through techniques like compaction or selective retrieval—can inadvertently discard subtle but critical context whose importance only becomes apparent later. This loss of nuance forces agents to either operate with incomplete information or require more tool calls to reconstruct missing context.
- The challenge of context engineering is to find the smallest possible set of high-signal tokens that maximizes the likelihood of some desired outcome while navigating these fundamental tensions.

## The Limitations of Vector-Based Retrieval


## The Limitations of Vector-Based Retrieval


### A Brief Overview of Vector Retrieval

- *Vector-based retrieval* finds relevant information by representing queries and documents as numerical vectors in a shared semantic space, usually stored in a vector database.
- uses machine learning models to encode the meaning of text into vector representations called embeddings.
- *Embeddings* capture semantic similarities (though not relationships), so documents about similar concepts will have vectors that are close together in the vector space
- When a user submits a query, it gets converted into the same vector format as the documents, and the system finds the most relevant documents by calculating similarity scores between the query vector and all document vectors in the database.
- The retrieved text chunks are then converted back to text and combined with the original query to provide context to the language model.
- Typically, this is done by constructing a prompt that includes the question and the retrieved reference passages.
- The LLM processes the query along with the injected relevant context and generates an answer. The generation is thus *augmented* (the *A* in RAG) by real-time retrieved information, grounding the LLM’s output in the provided documents.

### Where Vector RAG Succeeds and Fails


### Where Vector RAG Succeeds and Fails

- Vector RAG excels at indexing and searching through large volumes of unstructured text by semantic content.
- does not require a predefined schema, so any text can be embedded.
- makes it very flexible in domains where knowledge isn’t neatly structured.
- Vector search is also highly scalable for the right types of queries. Approximate nearest-neighbor (ANN) algorithms allow fast retrieval even from millions of documents.
- vector RAG can retrieve information that is semantically related to the query even if the exact terms aren’t present.
- Microsoft’s original GraphRAG paper, “From Local to Global: A GraphRAG Approach to Query-Focused Summarization,” ([Edge et al., 2025](https://oreil.ly/6Y7u-)). In the paper, the authors identify a spectrum of queries that delineate exactly when and why vector systems fail in production

![](https://readwise.io/reader/pcei/gAAAAABqkVp8amTH6G--4cht62pZO0VeEp7Ypo-z_fZDyFJGjcCiMKMwz9ZtLbamMdACOpTXW8_eh98fmTgaC0s42Hb6tEq0pZqzy22oHSr6pBibTYIo9Bk=/agrg_0103.png)

- *Local* queries—such as *What was the server configuration during Tuesday’s outage?*—ask about specific facts in a small number of text regions and sometimes even a single region.
- *Global* queries—for example, *What patterns emerge from our infrastructure failures over the past year?*—require reasoning over large portions of the dataset or even the entire dataset. The paper also refers to these as *sensemaking* queries.
- Vector RAG excels at the local query scope
- However, vector RAG catastrophically fails at the global query scope
- some major limitations with vector-based architecture emerge.
- first issue is *semantic gaps*. A fundamental disconnect exists between query vectors and relevant content vectors. When you ask *What is the capital of France?* it may not closely match text stating *Paris is the most populous city in France*, even though the passage contains the correct answer.
- *granularity trade-offs*. When constructing vector embeddings, you must choose between document-level representations that lack precision and sentence-level chunks that fragment context and increase computational overhead.
- *reasoning limitations* in vector-based retrieval. Vector similarity scores struggle to support complex reasoning tasks that require synthesizing information across multiple documents or following intricate logical chains.
- *Contextual amnesia* also plagues vector-based systems. They find it difficult to maintain a coherent understanding across multiple interactions and decision points, and they lack temporal awareness, treating all chunks as eternally present facts.
- *associativity gap*. Vector-based retrieval systems lack the ability to form transitive relationships across multiple documents, failing to construct logical chains when information is distributed across separate entries.

#### Won’t a larger context window solve this?

- Dumping more information into a context window doesn’t create understanding of relationships, temporal evolution, or systematic patterns. Rather, larger context windows make retrieval slower and worsen the lost in the middle problem.
- Vector retrieval forces your agents to be either myopic (focused on local details) or blind (unable to see the bigger picture).

## GraphRAG: The Evolution of Contextual Retrieval Systems


## GraphRAG: The Evolution of Contextual Retrieval Systems

- GraphRAG represents knowledge as a richly interconnected web of concepts, entities, and relationships.

### A Brief Overview of GraphRAG Architecture


### A Brief Overview of GraphRAG Architecture

- *GraphRAG systems* use a knowledge graph to store facts as nodes and edges, and they retrieve information by traversing this graph structure.
- architecture consists of a knowledge graph (often, though not always, managed in a graph database) and mechanisms to query and extract a subgraph relevant to the query.
- Domain knowledge is structured into a graph format, with nodes representing entities or concepts and edges representing relationships between those entities.
- first step in the general methodology is *knowledge graph construction*.
- Each node can also have properties or textual descriptions. Building the graph may involve parsing structured data or extracting entities and relations from text.
- Next is *graph data storage*. The graph is typically (though not always) stored in a graph database, such as Neo4j or Amazon Neptune, that is optimized for storing nodes and edges and executing graph queries.
- After the graph is constructed and stored, the next step is during user interaction, with query interpretation and graph traversal
- The user’s question is mapped to a graph query. This could be done by identifying relevant entities in the query or by using predefined query templates. The system then performs a graph traversal or search: it finds the node(s) matching the query subject and explores connected nodes and edges to gather relevant facts.
- The result of this retrieval is a *subgraph* (a set of related entities and their relations represented as triples) relevant to the query.

![](https://readwise.io/reader/pcei/gAAAAABqkVp8VlccSeHMjq56d7Bh4FGDdV26Y9cmJwAIKOElUtfuXuacgy5fdVfg3h5gUjmZbUz_30ECK0o8ieXY6LdLKJDZHqXckTHT_-pUnXzYw9L-_eg=/agrg_0104.png)

- After the subgraph is retrieved, it is then transformed into a form the LLM can understand in a process known as *context integration*.
- often means converting the graph data into textual statements or a structured context. For instance, if the query is *What is the capital of France?*, the system might query the graph for the `(:Country {name:"France"})-[:HAS_CAPITAL]->(c)` relation and obtain the `node` `c = Paris`. It would then provide the fact that *France’s capital is Paris* as context to the LLM.
- Finally, as with vector-based retrieval, there comes *response generation*. With the query-focused subgraph results available as text, the LLM generates the final answer.
- let’s look at researchers’ methodology for GraphRAG as an example. This involves a two-stage LLM-based pipeline for indexing and querying.
- The first stage is *indexing*, using an LLM to build the graph index in two main parts: 1. Derive an entity knowledge graph. The LLM extracts instances of important entities and relationships from the source documents to construct a knowledge graph, where nodes represent key entities and edges represent relationships. 2. Pregenerate community summaries. The system partitions the resulting knowledge graph into a hierarchy of closely related entities called *communities* (essentially, strongly connected nodes within the knowledge graph). Then, in a bottom-up, recursive manner, the LLM generates community summaries for these groups, which collectively provide global descriptions and insights over the corpus.
- The second stage is the *query*, where GraphRAG answers user queries using a map-reduce process applied to the pregenerated community summaries: 1. Map Given a question, each community summary is used to generate a partial response. 2. Reduce All partial responses are summarized in a final round of query-focused summarization to produce the final global answer returned to the user.

### Where GraphRAG Succeeds and Struggles


### Where GraphRAG Succeeds and Struggles


#### Context control

- key architectural advantage that graphs provide is *context control*—the ability to precisely manage what information reaches your model at each decision point.
- When vector embeddings alone are used, relationships between concepts get flattened into statistical similarities. When working with graphs, you explicitly model these connections, ensuring that your language models receive not just relevant information but also the crucial relationships between information elements.

#### Flexibility

- Graph-based architectures enable you to model this spectrum using nodes and edges, allowing you to calibrate the precise balance required for specific applications:
    - For workflow-like scenarios, you can design explicit, deterministic paths with fixed transitions, providing the reliability that mission-critical applications demand.
    - For agent-like behavior, you can implement conditional edges that adapt based on context, enabling dynamic reasoning without sacrificing structural clarity.

#### Better reasoning

- By representing tasks as directed acyclic graphs (DAGs), your systems decompose complex problems into manageable components with explicit dependencies. Independent subtasks can execute in parallel, dramatically improving efficiency. For particularly complex problems, you can implement recursive decomposition, creating nested subgraphs that encapsulate complexity where needed while maintaining simpler structures elsewhere.

#### Explainability and traceability

- retrieved subgraph or path can effectively serve as an explanation chain for the answer. Users or developers can trace which nodes and relations led the model to an answer.

#### Self-evolution data flywheel

- Each interaction generates valuable data that feeds back into the system, improving entity relationships, refining reasoning pathways, and enhancing tool selection.

#### Where GraphRAG struggles

- important to be aware of some challenges you may encounter.
- First, building and maintaining a knowledge graph requires *significant up-front effort*. The data must either exist in structured form or be extracted and curated into a graph. This often makes GraphRAG most feasible in specific domains (where schema and relationships are known). If your knowledge is broad or constantly changing, creating a comprehensive graph can be impractical.
- Second, graph queries, especially those involving many hops or searching large subgraphs, can be computationally expensive. Traversing a large knowledge graph may introduce latency that grows with graph size and complexity. While graph databases are optimized, they generally don’t match the raw speed of a vector similarity lookup for simple retrieval.
- Additionally, by condensing information into discrete triples or nodes, some contextual nuance can be lost. A graph might tell you that fact A relates to B, but not the full narrative or qualifier around that fact that was present in the source text.
- For example, a graph edge might state *Drug X treats Condition Y*, but the context that this is true only in certain patient populations might be omitted unless modeled.
- Designing the graph schema to include important qualifiers or context is a nontrivial challenge.
- Finally, although graphs excel at maintaining consistent relationships, updating a knowledge graph can be complex if the schema needs to evolve. Each update might need reconciliation with existing ontology.
- If a new relationship type emerges or a concept changes, developers must adjust the graph structure.

### Hybrid GraphRAG


### Hybrid GraphRAG

- This dual representation enables your system to leverage both statistical similarity and structured relational reasoning simultaneously.
- processing pipeline consists of three sequential stages that progressively enrich the context representation:
- • Your journey begins with vector search, employing traditional semantic similarity techniques to identify candidate nodes based on embedding proximity. This statistical foundation establishes initial relevance as the first step in the retrieval process. • From these candidate nodes, the system initiates graph traversal. Each relationship type receives specific traversal parameters, including weight coefficients that prioritize certain relationship types in particular contexts. • The final stage, context synthesis, integrates information gathered through both vector similarity and graph traversal. This harmonization of statistical and structural insights produces a coherent response that reflects the multidimensional nature of the query context.
- `class` `GraphAgent``:` `def` `__init__``(``self``,` `vector_index``,` `graph_db``):` `self``.``vector_index` `=` `vector_index` `# For initial semantic search` `self``.``graph_db` `=` `graph_db` `# For relationship traversal` `self``.``relationship_config` `=` `{` `"depends_on"``:` `{``"weight"``:` `0.8``,` `"max_depth"``:` `2``},` `"precedes"``:` `{``"weight"``:` `0.6``,` `"max_depth"``:` `3``},` `"influences"``:` `{``"weight"``:` `0.7``,` `"max_depth"``:` `2``},` `"contains"``:` `{``"weight"``:` `0.9``,` `"max_depth"``:` `1``},` `}` `def` `process_query``(``self``,` `query``):` `# Stage 1: Vector Search` `initial_candidates` `=` `self``.``vector_search``(``query``)` `# Stage 2: Graph Traversal` `expanded_context` `=` `self``.``graph_traverse``(` `starting_nodes``=``initial_candidates``,` `relationship_types``=``self``.``relationship_config``.``keys``(),` `max_depth``=``3``,` `)` `# Stage 3: Context Synthesis` `return` `self``.``synthesize_response``(``expanded_context``)`

### Learned Graph Reasoning Models


### Learned Graph Reasoning Models

- another emerging direction involves training dedicated neural models to reason over graph structures. These *graph foundation models* (GFMs) learn to traverse knowledge graphs and identify relevant information through training on large-scale graph datasets rather than using heuristic search or multiple LLM calls.

## Summary


## Chapter 2. Agentic Graph Architecture Foundations

- 2. Agentic Graph Architecture Foundations

## From Strings to Things


## From Strings to Things

- When Google launched its knowledge graph in 2012, Amit Singhal described the shift as moving to [“things, not strings”](https://oreil.ly/0bo7p): understanding entities and their relationships rather than matching keywords.
- In a vector store, everything is a string (or more precisely, a numerical projection of a string). A sentence about your payment service, a paragraph from a runbook, a JSON snippet from a config file, a line from a Terraform definition…they all become floating-point vectors in the same high-dimensional space. Their identities are gone. Their relationships to other pieces of information are gone. All that remains is their position in embedding space, measured by cosine similarity to whatever query comes next.
- vector search asks, *What text is similar to my query?* The graph query asks, *What is true about the relationships in my system?*

## The Dual-Graph Architecture


## The Dual-Graph Architecture

- But a knowledge graph alone does not tell the agent how to use that knowledge. The model still has to figure out the sequence of operations, manage dependencies between steps, and recover from failures—all within a single context window.
- The insight behind the dual-graph architecture is that an agentic system needs two complementary kinds of structure: a representation of *what it knows* (the entities, relationships, and constraints in its domain) and a representation of *how it acts* (the steps, decisions, and dependencies in its reasoning process).
- These are different concerns, and they work best as separate graph structures: Vertical knowledge graph This is the agent’s understanding of its world. It is a semantic network of entities and relationships that encodes domain knowledge with the precision that vector stores cannot provide. Horizontal workflow graph This is the agent’s plan of action. It is a DAG of reasoning and execution nodes that structures decision making into inspectable, enforceable steps.
- vertical knowledge graph (left) encodes what the agent knows: entities, relationships, and temporal metadata.
- horizontal workflow graph (right) encodes how the agent acts: reasoning nodes, execution nodes, and the dependencies between them.
- workflow nodes query the knowledge graph for context, and their results update it.

![](https://readwise.io/reader/pcei/gAAAAABqkVp9kKP4zJa67CTLrW6D557X58RaUkHWf_Ybv_N_v0FZl5IaOuDwGivkwyIhNomXhQD2t34z2EESk9dV94yYLUZeQ1f_YSoT2u9cglcQfd_jFBY=/agrg_0201.png)


### The Vertical Knowledge Graph


### The Vertical Knowledge Graph

- The *vertical knowledge graph* is a structured representation of everything the agent knows about its domain.
- The building blocks are straightforward:
- Nodes represent entities. Such as services, databases, configurations, incidents, users, and deployments. Each node has a type and a set of properties (name, version, status, timestamp).
- Edges represent relationships. Such as `DEPENDS_ON`, `DEPLOYED_TO`, `CAUSED_BY`, and `USES_LIBRARY`. Each edge has a type, a direction, and optional properties (weight, confidence, timestamp).
- Properties carry metadata. Metadata may include when a relationship was created, how confident the system is about it, and which source it came from.
- A fragment of an infrastructure vertical knowledge graph
- `// Entities: services, databases, libraries` `CREATE` `(:``Service` `{``name``:` `'checkout-service'``,` `version``:` `'3.2.1'``,` `status``:` `'healthy'``})` `CREATE` `(:``Service` `{``name``:` `'user-service'``,` `version``:` `'2.1.0'``,` `status``:` `'healthy'``})` `CREATE` `(:``Database` `{``name``:` `'payments-db'``,` `engine``:` `'PostgreSQL'``,` `version``:` `'15.2'``})` `CREATE` `(:``Library` `{``name``:` `'stripe-python'``,` `version``:` `'5.4.0'``})` `// Relationships: typed, directed, with temporal metadata` `CREATE` `(``checkout``)``-[``:``DEPENDS_ON` `{``since``:` `'2024-01-15'``}``]->``(``payments_db``)` `CREATE` `(``checkout``)``-[``:``DEPENDS_ON` `{``since``:` `'2024-03-01'``}``]->``(``user_service``)` `CREATE` `(``checkout``)``-[``:``USES_LIBRARY` `{``version``:` `'5.4.0'``}``]->``(``stripe``)`
- A single graph traversal starting from `checkout-service` can reach every service, database, and library it depends on. Two hops out reveals the transitive dependencies: everything that *those* services depend on.
- The choice of graph model matters, and the right choice depends on your reasoning requirements.
- *Property graphs* (the format shown in [Example 2-2](private://read/01m13whyk8ssegw20k3a9kfy10/#ch02_example_2_1783966126511789), used by Neo4j and other graph databases) store nodes with properties connected by labeled edges. They are fast, intuitive, and well-suited to traversal-heavy workloads like dependency analysis.
- The Resource Description Framework (RDF) takes a different approach, representing everything as subject-predicate-object triples with formal logical semantics. RDF enables native reasoning: if you tell the system that `Disease1` causes `Symptom1` and `Patient` exhibits `Symptom1`, it can infer `Disease1` as a potential diagnosis without you writing that logic.
- the schema design—which entity types exist, which relationship types connect them, and which properties they carry—shapes what the agent can reason about.

### The Horizontal Workflow Graph


### The Horizontal Workflow Graph

- The *horizontal workflow graph* structures how the agent acts. It represents the agent’s reasoning and execution process as a DAG: nodes are discrete operations, and edges encode the dependencies between them.
- Each node in the workflow graph has a focused responsibility:
- Reasoning nodes These perform analysis such as interpreting alerts, evaluating evidence, and identifying patterns. They query the vertical knowledge graph for context and produce structured conclusions.
- Execution nodes These take actions; they may call APIs, query metrics databases, or run diagnostic commands. They interact with the outside world through tools.
- Decision nodes These choose paths: based on the output of a reasoning node, the workflow branches to different next steps.
- Validation nodes These check work, verifying that an output conforms to a schema, that a conclusion is supported by evidence, or that an action is permitted.
- The edges between nodes encode which operations must complete before others can begin. This is not a linear sequence. It is a DAG, which means that independent operations can run in parallel while dependent operations wait for their inputs.
- The horizontal workflow graph describes what the agent should do, but it does not execute itself. Execution is the job of the agent’s harness
- The *harness* is a runtime with six surfaces, each with its own responsibility:
    - It holds the workflow graph as an inspectable state.
    - It advances the graph under a *named policy* that chooses which nodes fire next, in what order, under sequential, parallel, or dynamic-replanning execution.
    - It exposes a *typed tool registry* through which nodes invoke side-effectful operations, from API calls to graph writes to model invocations.
    - It mediates a *typed memory interface* through which nodes read from and write to the vertical knowledge graph and any temporal or episodic memory layers.
    - It enforces a *schema validator* that constrains the output of each node to match the input contract of its downstream neighbors.
    - It maintains an *append-only observation record* of every node invocation, every tool call, every input and output, and every timing annotation.
- A horizontal workflow graph for latency investigation
- `# A simplified horizontal workflow graph as a DAG.` `# Each node is an operation; each edge is a dependency.` `investigation` `=` `{` `"nodes"``:` `[` `{` `"id"``:` `"classify"``,` `"type"``:` `"reasoning"``,` `"task"``:` `"Classify alert severity and type"``,` `},` `{` `"id"``:` `"query_kg"``,` `"type"``:` `"retrieval"``,` `"task"``:` `"Find affected services and dependencies"``,` `},` `{` `"id"``:` `"get_metrics"``,` `"type"``:` `"tool_call"``,` `"task"``:` `"Query live metrics API for affected services"``,` `},` `{` `"id"``:` `"analyze"``,` `"type"``:` `"reasoning"``,` `"task"``:` `"Correlate evidence and identify root cause"``,` `},` `{` `"id"``:` `"report"``,` `"type"``:` `"generation"``,` `"task"``:` `"Generate structured incident report"``,` `},` `],` `"edges"``:` `[` `# Severity determines scope of graph traversal` `(``"classify"``,` `"query_kg"``),` `# Dependencies determine which metrics to check` `(``"query_kg"``,` `"get_metrics"``),` `# Graph context feeds into root cause analysis` `(``"query_kg"``,` `"analyze"``),` `# Live metrics feed into root cause analysis` `(``"get_metrics"``,` `"analyze"``),` `# Analysis becomes the incident report` `(``"analyze"``,` `"report"``),` `]` `}`
- Your horizontal workflow graph should follow the same rule. When two nodes need different tool surfaces, split them. When they need the same tool surface, merge them and vary the prompt.

### Where the Two Graphs Meet


### Where the Two Graphs Meet

- the horizontal workflow graph provides the reasoning skeleton, while the vertical knowledge graph supplies the domain knowledge that each operation needs to do its job.
- The interaction goes both ways. When the investigation concludes and identifies a root cause, the result can update the vertical knowledge graph, either adding a new `CAUSED_BY` edge between the incident and its root cause or updating a service node’s status.
- The workflow graph drives the process; the knowledge graph supplies and receives the facts. Each graph makes the other more useful than it could be alone.
- Each traversal narrows the hypothesis space based on structural evidence, not embedding similarity. The workflow graph coordinates the inquiry. The knowledge graph provides the evidence. The result is a diagnosis grounded in verified relationships rather than statistical inference.

### A Note on Context Graphs


### A Note on Context Graphs

- A *context graph* is a knowledge graph optimized for agent use. The underlying data structure is the same one this chapter has already described, with nodes, edges, and properties. What changes is what the graph is built to do. A context graph treats important relationships as first-class objects that carry their own history and provenance, attaches bitemporal metadata to every fact, and captures not just *what* the system knows but *why* it believes it, *when* the belief became true, and *which* source produced it.
- Three ideas distinguish a context graph from a plain knowledge graph:
- Reification as a first-class practice Instead of treating a relationship as a bare edge between two nodes, you promote important relationships into nodes of their own so that metadata, provenance, and temporal bounds can hang off them.
- Bitemporal metadata Every node and edge carry both *valid time* (when the fact was true in the world) and *transaction time* (when the system recorded it).
- Governed memory and decision traces Entities, events, decisions, policies, and evidence all live in the same structure, queryable together.
- why does this book use the term *vertical knowledge graph* instead of *context graph*? First, *context graph* describes a set of capabilities one graph can have, whereas the *dual-graph architecture* describes a relationship between two complementary graphs.
- Second, *context* is the single most overloaded word in agentic AI.

## The Eight Pillars of Agentic Graph Architecture


## The Eight Pillars of Agentic Graph Architecture

- The *eight pillars* are the implementation roadmap: the specific capabilities you need to build to turn that framework into a working system.

![](https://readwise.io/reader/pcei/gAAAAABqkVp9fBSrgtI4UiqPxIjn-YjvyS44Sz8eLLpxO3KybCzZ-pvUuV5Gb4UmheFSt31rGyEgYFmIBfBAzRj2kvPu3OZCwmayUPKxMsrJBCFm79dg5UA=/agrg_0202.png)


### Setup: Building the Digital Twin of a Tech Stack (Part II)


### Action: From Firefighting to Foresight (Part III)


## Summary


## Part II. Setup: Building the Digital Twin of a Tech Stack

- II. Setup: Building the Digital Twin of a Tech Stack

## Chapter 3. Graph-Based Knowledge Modeling for Agentic Systems

- 3. Graph-Based Knowledge Modeling for Agentic Systems

## Knowledge Graph Foundations


## Knowledge Graph Foundations


### Components of GraphRAG Systems


### Components of GraphRAG Systems

- In their 2026 paper [“In-Depth Analysis of Graph-Based RAG in a Unified Framework”](https://oreil.ly/fWpUD), Zhou and colleagues introduce a four-stage framework:
- 1. Graph building Transforms a corpus of knowledge into an appropriate graph structure, laying the foundation for all subsequent processing. This stage determines what information is captured and how it’s organized, with significant implications for downstream retrieval capabilities.
- 2. Index construction Creates efficient lookup mechanisms that enable real-time query performance. This stage bridges the semantic richness of the graph with the practical requirements of production systems, balancing expressiveness against computational efficiency.
- 3. Operator configuration Selects and arranges retrieval operators to implement specific retrieval strategies. This stage determines how the system navigates the graph, combining different operators to extract relevant information based on the query characteristics.
- 4. Retrieval and generation Connects the graph traversal with language model integration, retrieving context and generating coherent responses. This stage synthesizes the structured information from the graph with the generative capabilities of the language model.

![](https://readwise.io/reader/pcei/gAAAAABqkVp-Jwfny7UxyMZw5N6dAwK6AarCtKv3WSWlBL2vrlXqS4GEjfxT8LA9szgob3wxxr9knfaNsqL7uCApLOa0vRagJyHdA542eNYi29E4LO5dxBo=/agrg_0301.png)


## Graph Data Models


## Graph Data Models

- AI agents are only as intelligent as the knowledge structures you give them. When you build production-grade agentic systems, your first foundational challenge is to effectively represent knowledge
- Consider how a typical enterprise knowledge domain contains complex, interconnected entities. A product connects to specifications, which link to manufacturing processes, which relate to supply chain dependencies, which impact financial projections. In conventional storage systems, these connections exist only implicitly (through foreign key relationships, for example), if at all. In graph structures, you explicitly model and leverage these relationships.

### Types of Graph Data Models


### Types of Graph Data Models

- Every decision—from representation choice to schema patterns to optimization strategies—should be evaluated based on whether it enables or constrains the reasoning capabilities your agents need.
- Start with your reasoning requirements, not your data. First ask: *What kind of reasoning do my agents need to perform?*
- Formal *logical inference* (as in medical diagnosis systems) will require a different approach than network analysis and traversals, where speed matters more than inference, or complex events involving many entities (e.g., prescriptions, transactions, meetings)
- Once you have determined your reasoning requirements, you can pick a graph model
- The simplest approach is *labeled property graphs* (LPGs), which store nodes with properties connected by labeled edges. They’re fast and intuitive, but they can only tell you what you’ve explicitly programmed. They work well for queries like *Find all customers who bought product X*, but they can’t infer new knowledge on their own.
- *Resource Description Framework* (RDF) takes a different approach, representing everything as subject-predicate-object triples with formal logical semantics. This enables native reasoning. For example, if you tell an RDF system *Disease1 causes Symptom1* and *Patient exhibits Symptom1*, it can automatically infer *Disease1 is a potential diagnosis* without you writing that logic. Unfortunately, this means that RDF is slower and more complex to work with.
- *Hypergraphs* let you connect multiple entities in a single relationship (like a prescription linking doctor, patient, medication, dosage, date, and condition all at once), avoiding the artificial complexity of forcing everything into binary relationships.

### Evaluating Graph Models


### Evaluating Graph Models

- Every knowledge representation decision you make must take into account the [reasoning-representation trade-off](https://oreil.ly/rfdFi). Property graphs offer flexibility and performance advantages but lack the formal logical semantics required for sophisticated reasoning. RDF, on the other hand, provides formal logical semantics that enable native reasoning capabilities.
- Consider an agent that is tasked with medical diagnosis encountering this simple knowledge:
    - *Disease1 causes Symptom1*
    - *Patient exhibits Symptom1* A graph with proper reasoning capabilities would infer that *Disease1* is a potential diagnosis to consider. Using LPGs, you would need to explicitly code such inference patterns, whereas RDF-based systems would handle this natively through their built-in reasoning capabilities.

#### Formal reasoning

- RDF excels in formal reasoning capabilities due to its strong semantic foundation. It supports complex ontological structures, enabling robust inference, consistency checking, and logical deduction
- first dimension to consider is *formal reasoning capabilities*
- makes it ideal for applications requiring high precision and explainability in their reasoning processes, such as semantic web applications and expert systems
- Property graphs, though excellent for capturing relationships, typically offer limited intrinsic support for formal reasoning
- Reasoning often relies on application-level logic or external engines rather than the graph model itself. This can lead to less standardized and more ad hoc reasoning capabilities, which are suitable for use cases where explicit logical inference is not a primary requirement
- Hypergraphs offer better support for representing complex relationships as they can implicitly facilitate reasoning through the structure of hyperedges
- their ability to model multiway relationships can simplify certain types of inference, especially those involving more than two entities

#### N-ary relations

- Knowledge graphs based on binary relations (*subject-predicate-object* triples) sometimes struggle to represent complex real-world relationships involving multiple entities
- Consider this statement: *Dr. Smith prescribed 50 mg of medication X to patient Jones on Tuesday for condition Y*. This involves at least five entities in a single relationship. Forcing this into binary relations creates artificial complexity and loses the holistic nature of the event.
- RDF inherently models binary relations through triples. To represent n-*ary relations* involving more than two entities requires a technique called *reification*, where the relation itself is treated as an entity with its own properties. While effective, reification adds complexity and can make querying less straightforward.
- Property graphs can represent *n*-ary relations by introducing intermediate nodes that act as the relations themselves, with edges connecting a *relation node* to all participating entities. This approach is similar to reification and adds extra nodes and edges, potentially complicating the graph structure for certain queries.
- Hypergraphs, in contrast, naturally support *n*-ary relations through hyperedges ([Cagle, 2024](https://oreil.ly/MaJjF)). A single *hyperedge* can connect any number of nodes, directly representing relationships involving multiple entities without auxiliary nodes or complex reification patterns. This makes hypergraphs highly intuitive and efficient for modeling complex, multiway interactions
- Hypergraph implementation
- `# Representation of a prescription event as a hyperedge` `prescription` `=` `HyperEdge``(` `type``=``"Prescription"``,` `nodes``=``{` `"doctor"``:` `dr_smith``,` `"patient"``:` `patient_jones``,` `"medication"``:` `med_x``,` `"dosage"``:` `"50mg"``,` `"date"``:` `tuesday``,` `"condition"``:` `condition_y` `},` `attributes``=``{` `"status"``:` `"active"` `}` `)`

#### Performance

- RDF systems can experience performance challenges, especially with very large datasets and complex queries. The overhead associated with semantic reasoning, schema validation, and the triple-store architecture can lead to slower query execution than with other graph models. Optimization often requires specialized indexing and query planning.
- Property graphs are generally recognized for their high performance, particularly in traversal-intensive operations. Their native graph storage and indexing, coupled with optimized algorithms for pathfinding and neighborhood exploration, make them very efficient for querying connected data. This makes them ideal for applications requiring rapid graph traversals and real-time analytics.
- Hypergraphs offer moderate performance. While their ability to represent *n*-ary relations directly can simplify the graph structure and improve certain types of queries, the more complex data structures for hyperedges can sometimes introduce more overhead than with simple binary relations

#### Constraint expressiveness

- While RDF is strong in formal reasoning, it has limited direct support for expressing complex constraints beyond what can be inferred from the ontology itself. Web Ontology Language (OWL) can define classes, properties, and restrictions, but expressing procedural or intricate data integrity constraints often requires additional rule languages or application-level logic.
- Property graphs generally provide limited constraint expressiveness natively. Although unique constraints on properties and relationships can be defined, expressing complex business rules, integrity checks, or conditional constraints typically requires application-level code or external validation frameworks.
- Hypergraphs share similar limitations, focusing primarily on the structural representation of multiway relationships. Defining and enforcing complex data validation or business logic constraints usually falls to the application layer.

#### Putting it all together

- Property graphs are ideal for applications requiring high performance in graph traversals, flexible data modeling, and a rich tool ecosystem, though they lack strong native support for formal reasoning and complex constraints.
- RDF is best suited for scenarios that demand strong formal reasoning, semantic interoperability, and robust ontological representations, though it may suffer from performance trade-offs and complexity in handling *n*-ary relations
- Hypergraphs shine when *n*-ary relations are central to the knowledge representation, offering a natural and efficient way to model complex interactions
- Ultimately, a hybrid approach combining elements from different models, or leveraging specialized tools for specific aspects ... might offer the most robust solution for complex agentic system architectures

#### Open world, closed world, and agent safety

- RDF was designed around the *open-world assumption* (*OWA*), where a fact that is not in the graph is treated as unknown rather than false
- Relational databases, most property graph stores, and anything built around schema-on-write follow the *closed-world assumption* (*CWA*), where absence means negation
- Under OWA, the answer to *Is there a contraindication?* is *unknown*, which is not a decision an agent can act on. Under CWA, the answer is *no*, which is such a decision.
- The practical problem is that the two assumptions coexist inside a single graph system and switch between each other silently
- [SHACL](https://oreil.ly/vidsn) is the W3C standard that makes the problem tractable. A SHACL *shape* specifies what a node of a given type must look like (which properties it must carry, how many values each property may take, what datatypes and values are permitted) and rejects nodes that do not match. Unlike OWL, which infers new facts, SHACL validates against a contract
- Three SHACL usage patterns address the three points at which an agent interacts with the graph:
- Pre-retrieval shapes These validate that the entities a query targets carry the required structure before the agent trusts a result built from them. A shape on a `Service` node might require `:owningTeam`, `:deploymentTarget`, and a recent `:dependencyStatus​Ti⁠mestamp`, so a query that looks up a service runs only after the node has cleared validation. Pre-action shapes These validate the preconditions that a tool requires before the agent invokes it. A `RollbackDeployment` tool might require its target to carry a `:rollback​Ap⁠proved true` triple and a `:lastKnownGoodVersion` property; SHACL runs the check in milliseconds, and the tool call proceeds only if the shape matches. Post-write shapes These validate anything the agent writes back to the graph before the transaction commits, so writer-agents become constrained writers rather than free-form updaters. A post-write shape on a new `CAUSED_BY` edge might require both endpoints to exist and the edge itself to carry provenance metadata.

#### Graph structures

- Graph rdata models reflect how information is represented, structured, and reasoned about inside the graph. They are schema-level or knowledge-representation frameworks defining how nodes, edges, and relationships behave and what kinds of queries and reasoning the system can support
- Several graph structures have emerged, each offering different trade-offs between simplicity and expressiveness:
- Graph *structures* refer to the source and purpose of the content being represented as unstructured text is transformed into structured graph formats that you can efficiently traverse and query
- Passage graphs These are perhaps the simplest approach, where document chunks become nodes connected when they share common entities. This lightweight representation requires minimal processing but captures basic document-to-document relationships.
- Trees Trees introduce hierarchical organization, creating multiresolution representations where higher-level nodes summarize their children. This structure allows your system to match queries at varying levels of detail, retrieving general concepts or specific facts as needed.
- Knowledge graphs Knowledge graphs capture explicit semantic relationships between entities, following the subject-predicate-object pattern common in knowledge representation. These structures excel at supporting reasoning tasks but require more sophisticated extraction techniques.
- Textual knowledge graphs These enhance standard knowledge graphs by attaching descriptive text to entities and relationships. This addition preserves contextual information that might otherwise be lost during the transformation from text to graph.
- Rich knowledge graphs These graphs further extend this approach with additional metadata like entity types, relationship keywords, and edge weights. This rich representation supports nuanced reasoning but increases the complexity of both construction and querying.

## Graph Design Principles for Agentic Systems


## Graph Design Principles for Agentic Systems


### The Three-Graph Architecture for Agent Knowledge


### The Three-Graph Architecture for Agent Knowledge

- Unverified information pollutes trusted data, provenance to source documents is lost, extraction errors cascade through the entire graph, and validation of agent reasoning becomes impossible.

![](https://readwise.io/reader/pcei/gAAAAABqkVp-71P_b8dVsOtSk1gYBHBtsEywwqDFM3BhNKMAkUTz_UXeZeXTG20X9Q15lBdHrFNDMUDp8DFk1OW1Zxuo9HBE8Q1M6oaR163WnNhEKKJzKRs=/agrg_0302.png)


#### Domain graph

- The *domain graph* contains your trusted, curated, validated data as a single source of truth. It’s typically built from structured sources that have undergone entity resolution
- This is where your official entities live, such as the canonical list of products, the definitive organizational hierarchy, and the authoritative supplier relationships.
- Key characteristics include high certainty (data validated through multiple sources), stable identifiers from entity resolution that persist over time, definitive relationships you can rely on for agent reasoning, and protection from contamination by unverified extractions.

#### Lexical graph

- The *lexical graph* holds your original unstructured text in structured format. When processing customer reviews, internal documents, or investigative reports, this graph preserves source material exactly as received.
- Key characteristics include complete provenance (every text chunk links back to source document), immutability (the original text is never modified), enabling RAG (providing the “retrieval” in retrieval-augmented generation), and supporting verification (agents can cite specific passages to support claims).
- The structure is straightforward. Document nodes contain metadata (such as file path, author, and date), chunk nodes contain text segments with embeddings for vector search, and relationships preserve document order and hierarchy.

#### Subject graph

- Finally, the *subject graph* is where the architecture’s sophistication becomes clear. This graph contains entities and facts as extracted by LLMs from the lexical graph but, critically, keeps them separate from the domain graph until entity resolution establishes confident links.
- Key characteristics include acknowledgment that these are extraction artifacts representing what the LLM interpreted. The uncertainty is acknowledged explicitly (these are interpretations, not ground truth), enabling entity resolution by providing candidates for linking to domain entities and maintaining extraction metadata like confidence scores, model versions, and timestamps

#### Why this architecture works

- The critical operation making this architecture work is entity resolution that connects the subject graph to the domain graph
- The system extracts a `Subject_Product` entity with this mention, finds potential matches in the domain graph using similarity search, calculates similarity between the extracted name and domain names, and creates `CORRESPONDS_TO` relationships for matches exceeding the confidence threshold.
- Consider a customer review mentioning *the Stockholm chair*
- This linkage enables powerful cross-graph queries: a query starts from a domain product, finds all customer-reported issues via subject entities, traces back to original review text in lexical chunks, and returns aggregated evidence with full provenance.

#### Why this architecture matters for agents

- The three-graph architecture enables sophisticated agent reasoning patterns that would be impossible with a single graph
- For example, when querying, *What issues do customers report with our products?* agents can start from the domain graph (the official product list), traverse `CORRESPONDS_TO` links to the subject graph (extracted issues), and follow `EXTRACTED_FROM` links to the lexical graph (original review text). This traversal path maintains uncertainty levels, as agents know which information comes from trusted sources versus extraction.
- The architecture also allows for better provenance and explainability. When presenting findings, agents can cite evidence with full traceability: the claim, confidence level based on mention count, specific review excerpts, and links to actual source chunks. Analysts can then audit agent reasoning by checking whether domain entities are correctly identified (entity resolution quality), verifying that extracted facts match source text (extraction quality), and reviewing which chunks the agent retrieved (retrieval quality).
- As extraction models improve, you can re-extract the subject graph from the lexical graph, compare new extractions with old ones, and preserve the domain graph completely. Your trusted data remains unaffected.

### Schema Design Patterns


### Schema Design Patterns

- Effective agent reasoning begins with schema patterns explicitly designed to support machine cognition across temporal, contextual, and perspectival dimensions

#### Event-centric pattern

- Temporal reasoning forms a cornerstone of agent intelligence. The *event-centric pattern* structures knowledge around occurrences rather than static entities

#### Event-centric pattern

- `Event` `[``type``:` `Meeting``]` `|``--` `hasParticipant` `-->` `Person` `[``id``:` `Alice``]` `|``--` `hasParticipant` `-->` `Person` `[``id``:` `Bob``]` `|``--` `hasStartTime` `-->` `Timestamp` `[``value``:` `2026``-``04``-``01``T15``:``00``:``00``Z``]` `|``--` `hasEndTime` `-->` `Timestamp` `[``value``:` `2026``-``04``-``01``T16``:``00``:``00``Z``]` `|``--` `hasLocation` `-->` `Room` `[``id``:` `Conference``-``A``]` `|``--` `hasPrecedingEvent` `-->` `Event` `[``id``:` `Team``-``Standup``]` `|``--` `hasFollowingEvent` `-->` `Event` `[``id``:` `Project``-``Review``]`
- a `Meeting` event is modeled with multiple relationship types that capture temporal and contextual dimensions
- The example defines a `Meeting` event with two participants (`Alice` and `Bob`), precise start and end timestamps (April 1, 2023, 3:00–4:00 p.m.), a physical location (`Conference-A`), and temporal relationships to other events (preceded by a `Team-Standup` and followed by a `Project-Review`).
- This structured approach enables agents to reason about temporal sequences, participation patterns, and cause-effect relationships. By modeling events as first-class entities with explicit temporal connections, agents can answer complex queries like *What meetings did Alice attend before the project review?* or *Which events occurred in conference room A during April 2023?* These capabilities would be difficult to achieve with entity-centric modeling alone.

#### Contextual boundary pattern

- Knowledge validity frequently depends on specific contextual parameters. The *contextual boundary pattern* explicitly encapsulates information within defined scopes,

#### Contextual boundary pattern

- `Context` `[``type``:` `Project``-``X``]` `|``--` `contains` `-->` `Task` `[``id``:` `Task``-``1``]` `|``--` `contains` `-->` `Task` `[``id``:` `Task``-``2``]` `|``--` `validDuring` `-->` `TimeRange` `[``start``:` `2023``-``01``-``01``,` `end``:` `2023``-``06``-``30``]` `|``--` `appliesTo` `-->` `Team` `[``id``:` `Engineering``]`
- This example illustrates how contextual boundaries are represented. The code defines a `Context` entity (`Project-X`) that explicitly establishes boundaries around related information
- Containment relationships that group related tasks (`Task-1` and `Task-2`) within the project context
- Temporal boundaries through the `validDuring` relationship, indicating this context only applies during a specific time frame (January–June 2023)
- Organizational boundaries via the `appliesTo` relationship, limiting relevance to a particular team (`Engineering`)
- This pattern is essential for preventing *context mixing*, a common source of reasoning errors in AI systems. By explicitly modeling contextual boundaries, agents can determine when certain facts or rules apply and when they don’t

#### Multiperspective pattern

- Real-world knowledge often incorporates multiple, sometimes contradictory perspectives. The *multiperspective pattern* explicitly models these viewpoints

#### Multiperspective pattern

- `Statement` `[``id``:` `Revenue``-``Forecast``]` `|``--` `hasValue` `-->` `Value` `[``amount``:` `10``M``,` `currency``:` `USD``]` `|``--` `according``-``to` `-->` `Perspective` `[``source``:` `Finance``-``Dept``,` `confidence``:` `0``.``8``]` `|``--` `according``-``to` `-->` `Perspective` `[``source``:` `Sales``-``Dept``,` `|` `value``:` `12``M``,` `confidence``:` `0``.``7``]`
- example demonstrates sophisticated handling of divergent information
- Rather than forcing a single “correct” value, the pattern explicitly represents:
    - The base statement (`Revenue-Forecast`) and its primary value (`10M USD`)
    - The finance department’s (`Finance-Dept`) perspective with high confidence (`0.8`)
    - The sales department’s (`Sales-Dept`) differing perspective (`12M USD`) with slightly lower confidence (`0.7`)
- This approach enables agents to handle real-world information complexity, where multiple valid perspectives might exist simultaneously

#### Capability model pattern

- Self-aware agents must understand their own capabilities and limitations. The *capability model pattern* explicitly represents operational parameters
- The capability model pattern
- `Agent` `[``id``:` `Customer``-``Support``-``Agent``]` `|--` `hasCapability` `-->` `Capability` `[` `type``:` `Answer``-``Product``-``Question``,` `requires``:` `Product``-``Knowledge``,` `authorization``-``level``:` `Public` `]` `|--` `hasCapability` `-->` `Capability` `[` `type``:` `Process``-``Refund``,` `requires``:` `Financial``-``System``-``Access``,` `authorization``-``level``:` `Supervisor``,` `limit``:` `500``-``USD` `]`
- The code models a `Customer-Support-Agent` with explicitly defined capabilities and limitations. The `Answer-Product-Question` capability specifies the required knowledge domain (`Product-Knowledge`) and authorization level (`Public`), indicating that any agent instance can perform this action.
- Given explicitly modeled capabilities with their requirements and boundaries, agents can make informed decisions about what they can handle independently and when escalation is necessary. During planning, an agent can determine if it has the necessary access, authorization, and operational limits to fulfill a request before attempting it.
- transforms vague operational guidelines into concrete, queryable knowledge structures
- Events, contextual boundaries, multiperspective statements, and capability models all make the same structural move: they take something that would naively be modeled as an edge or a property and promote it to a first-class node so that metadata, provenance, and temporal bounds can hang off it. That move has a name in the semantic web literature, *reification*, and it is the single feature that distinguishes a plain knowledge graph from what the industry has started calling a *context graph*

### Homoiconic Knowledge Representation


### Homoiconic Knowledge Representation

- Beyond schema patterns, agent-friendly knowledge graphs require *homoiconicity*, where code and data share the same representation
- Homoiconicity enables agents to modify their own operational logic
- two approaches to maintain homoiconicity: metaknowledge structures and executable knowledge patterns
- In *metaknowledge structures*, you store knowledge about knowledge using the same graph structures as for the knowledge itself
- Metaknowledge structure
- `# Define a metaschema that describes the schema itself` `metaschema` `=` `{` `"entities"``:` `[` `{` `"type"``:` `"EntityType"``,` `"properties"``:` `[` `{``"name"``:` `"name"``,` `"type"``:` `"string"``,` `"required"``:` `true``},` `{``"name"``:` `"description"``,` `"type"``:` `"string"``},` `{``"name"``:` `"properties"``,` `"type"``:` `"list"``,` `"items"``:` `"PropertyDefinition"``}` `]` `}` `]` `}` `# Now the schema and data use the same representation` `knowledge_graph``.``add_entity``(``"EntityType"``,` `{` `"name"``:` `"Person"``,` `"description"``:` `"A human individual"``,` `"properties"``:` `[` `{``"name"``:` `"name"``,` `"type"``:` `"string"``,` `"required"``:` `true``},` `{``"name"``:` `"birth_date"``,` `"type"``:` `"date"``},` `{``"name"``:` `"occupation"``,` `"type"``:` `"string"``}` `]` `})`
- First, there is a metaschema definition that describes the schema itself:
    - It defines what an `EntityType` is.
    - It specifies that entity types have properties like `name` (required), `description`, and `properties`.
    - The schema itself is represented as a data structure within the knowledge graph.
- Then, the agent uses an application of this metaschema to create actual domain knowledge, using the same representation format to define a `Person` entity type, specifying its properties (`name`, `birth_date`, `occupation`). Note that the syntax and structure for both schema and data are identical.
- This homoiconic approach is powerful for agent systems because it enables agents to inspect and modify their own knowledge structures using the same mechanisms they use for regular data

#### Executable knowledge patterns

- encodes operational rules within the graph structure itself as *executable knowledge patterns*

#### Executable knowledge patterns

- `# Define a rule directly in the knowledge graph` `rule` `=` `knowledge_graph``.``add_entity``(``"Rule"``,` `{` `"name"``:` `"DetermineCustomerSegment"``,` `"description"``:` `"Assigns customer segment based on purchase history"``,` `"condition"``:` `"""` `MATCH (c:Customer)-[:PURCHASED]->(p:Product)` `WITH c, COUNT(p) as purchase_count` `RETURN c, purchase_count` `"""``,` `"action"``:` `"""` `WHEN purchase_count > 20 THEN` `SET c.segment = 'Premium'` `WHEN purchase_count > 10 THEN` `SET c.segment = 'Regular'` `ELSE` `SET c.segment = 'Basic'` `"""` `})`
- showcases how business rules become first-class citizens in the knowledge graph using procedural knowledge and operational logic
- By representing rules within the same graph as domain data, agents gain remarkable capabilities. They can reason about the rules themselves, not just follow them. They can discover, modify, and create new rules dynamically. They can explain their decision-making process by referencing specific rules. They can adapt rule sets based on changing business requirements.

## Integrating with Existing Systems


## Integrating with Existing Systems

- Few organizations build knowledge graphs from scratch. Most need to integrate existing taxonomies, ontologies, and data structures
- as organizations adopt AI platforms, graph-based RAG systems, and semantic layers that depend on accurate entities and well-structured relationships, ontologies and entity resolution have become central to how AI features actually work

### Knowledge Organization and Ontology Fundamentals


### Knowledge Organization and Ontology Fundamentals

- An *ontology* is a form of knowledge organization
- Nearly all enterprises must form some sort of *organizational vocabulary* in order to standardize terminology and understanding around institutional knowledge
- Organizational vocabularies provide essential semantic foundations for agent knowledge graphs for several fundamental reasons: Semantic consistency Without standardized vocabularies, the same concept might be represented with different terms across systems (e.g., *customer* versus *client* versus *patron*). Institutional knowledge preservation Vocabularies encode organizational wisdom about entity relationships, domain hierarchies, and contextual meaning that has evolved over time. Governance and compliance In regulated industries, specific terminology carries legal implications. Organizational vocabularies standardize terminology to ensure compliance.
- All of these benefits to organizations also benefit agents
- Semantic consistency ensures that agents recognize when references point to the same entity type, institutional knowledge is crucial for agent understanding, and standardized vocabularies ensure agents use terms correctly within their proper regulatory context
- All of these capabilities add up to enhanced *reasoning reliability*
- Inconsistent terminology creates false negative paths where relationships aren’t recognized and false positive paths where unrelated concepts appear connected

#### The knowledge organization spectrum

- Knowledge organization systems exist on a spectrum from simple to complex: Pick lists These represent the simplest form—controlled value lists without hierarchical structure. Examples include country lists or currency codes. Taxonomies These introduce parent-child hierarchical relationships with predefined terms and synonyms. For instance, *transportation* (parent) encompasses *bike*, *bus*, *car*, *truck*, *boat*, and *scooter* (children). Thesauruses These extend taxonomies with richer structures, including parent-child hierarchies, predefined terms with synonyms, and generic associated relationships to other structural elements. Ontologies The most sophisticated systems, these are graph or network structures describing combinations of classes with robust relationship descriptors, predefined classes and properties, expanded relationship types, scope notes for context, and inference capabilities.

#### Ontology core components

- Every ontology consists of five fundamental components: Classes Collections of related objects, individuals, or instances that serve as the organizing metadata framework. In healthcare, classes might include `Person`, `Disease`, and `Test`. Classes can inherit attributes from parent classes, establishing hierarchical structure. Subclasses Represent more specific categories within classes, inheriting parent properties. `Person` subdivides into `Patient` and `Oncologist`; `Disease` into `Cancer`, `Glioblastoma`, and `Medulloblastoma`; `Test` into `MRI` and `CT Scan`. Individuals (instances) Specific examples of classes or subclasses as actual data records. `John Doe` represents an instance of `Patient`. From a machine perspective, inference becomes possible: `John Doe` is a `Patient` *and* a `Person`. If `Jane Smith` is an `Oncologist`, metadata automatically applies the title `Doctor`. Axioms These codify domain truths, expressible in class attributes or relationships. They define rules and constraints. For example, `Cancer` is a subclass of `Disease`, since many diseases exist; different types of cancer are subclasses of `Cancer`. A patient can have at most one primary physician, medications have specific dosage information, and treatments have eligibility criteria. Relationships (object properties) These convey meaning by connecting entities, defining how things interact. In healthcare, `personUtilizesFacility` (*patient* → *hospital*), `employsDoctor` (*hospital* → *primary care physician*), `testUsedForDisease` (*MRI* → *glioblastoma*), `diseaseHasSymptom` (*glioblastoma* → *headaches*), `doctorSpecializesIn` (*oncologist* → disease types).

### Creating a Unified Semantic Foundation


### Creating a Unified Semantic Foundation

- Transforming disconnected terminologies into a unified semantic foundation prevents agents from operating with fragmented, contradictory understanding
- Consider this five-step process to build such a foundation: 1. Inventory existing resources Catalog all taxonomies, terminologies, and controlled vocabularies. 2. Assess quality Evaluate completeness, consistency, and currency. 3. Normalize formats Convert to standard formats like OWL and others. 4. Align concepts Establish mappings between overlapping terminologies. 5. Enrich semantics Add missing relationships and constraints. 6. Publish as services Make vocabularies accessible via APIs.
- *Simple Knowledge Organization System* (SKOS) to map between different terminologies
- `# SKOS mapping between different terminology systems` `:``CompanyProduct` `skos``:``exactMatch` `orgVocab``:``Product` `.` `:``CompanyProduct` `skos``:``broader` `industryVocab``:``Offering` `.` `:``CompanyProduct` `skos``:``related` `financeVocab``:``Revenue_Source` `.`
- SKOS mappings that establish precise semantic relationships between terms across different vocabularies
- mapping `:Company​Prod⁠uct` `skos:exactMatch` `orgVocab:Product` establishes an equivalence relationship that allows agents to understand that different organizations are referring to the same concept, even when using different terminology
- Without these controlled vocabulary mappings, your agent would treat identical concepts with different names as entirely separate entities, leading to knowledge fragmentation. Terms like *automobile*, *car*, and *vehicle* would exist as disconnected concepts rather than related entities in a semantic hierarchy.
- Agents need this structure as well, but one that is more explicitly defined, because they don’t bring domain intuition or expertise
- The ontology becomes the playbook: Which entities exist in the business? How do entities connect? Where does authority live for each entity? What actions achieve outcome targets? What are the business rules and constraints?
- Ontologies serve as the semantic backbone for sophisticated agent reasoning, but you may need to integrate multiple ontologies when building a graph-based agentic system
- These independently developed ontologies often contain conflicting axioms or contradictory class definitions that must be harmonized to prevent reasoning errors. Without proper integration, agents cannot make connections between related concepts across boundaries.
- Several techniques can be helpful when merging multiple ontologies
- For example, *class hierarchy alignment* maps class hierarchies using semantic similarity. *Property alignment* establishes equivalence between properties with similar semantics, and *instance matching* links instances that represent the same real-world entities. Finally, *axiom harmonization* is used to resolve conflicts between logical axioms

![](https://readwise.io/reader/pcei/gAAAAABqkVp-mfeMfF4F1OvvXV51C2YRzm_YXeYMJV7sWc0yFsZtP70-kmT32vRWwEMjeN5oPmTpsd-7zk_jB8KZfVFegyFzdsaLxv1mxC7tD7Jw7mi45Y8=/agrg_0303.png)

- Traditional ontologies describe what exists in a domain—the entity types, their properties, and their relationships. But sophisticated agent systems require ontologies that go further: they must also encode how agents should interact with the knowledge graph. This transforms ontologies from passive schema descriptions into active control structures that can guide agent behavior without hard-coded logic.
- The key insight is that behavioral annotations can be used within the ontology itself. Beyond stating that the `Artist` class has an `artist_name` property, you annotate that property as `identifying`—marking it as the unique key agents should use when looking up artists. Rather than just defining a `CREATED` relationship from `Artist` to `Artwork`, you annotate it as contextualizing, signaling that agents should traverse this relationship when gathering relevant context.
- This approach also enables selective traversal. Some relationships carry immediate contextual value for agent reasoning, while others serve different purposes. In a museum catalog, the `CREATED` relationship from `Artist` to `Artwork` provides essential context for recommendations. But the `BROADER` relationship between `Subject` nodes, which organizes topics into taxonomies, typically shouldn’t be traversed automatically during contextualization—it serves navigational purposes rather than contextual enrichment.
- By marking relationships as contextualizing or noncontextualizing, you give agents precise guidance about graph traversal without writing traversal algorithms
- While integrating existing organizational knowledge structures, you’ll inevitably encounter ontologies built using traditional languages like OWL. Understanding their capabilities and limitations is crucial for developing truly effective agentic systems.
- OWL representation
- `:``prescription123` `a` `:``Prescription` `;` `:``hasPrescriber` `:``drSmith` `;` `:``hasPatient` `:``patientJones` `;` `:``hasMedication` `:``medicationX` `;` `:``hasDosage` `"50mg"` `;` `:``hasDate` `:``tuesday` `;` `:``hasCondition` `:``conditionY` `.`
- faces challenges when addressing more complex semantic relationships or higher-order structures needed for sophisticated agent reasoning
- As knowledge graphs evolve, it becomes necessary to manage two change types: data change (structure remains stable while sources refresh) and ontology change (entities and relationships are added as metadata).
- *Basic Formal Ontology* (BFO) or [DOLCE](https://oreil.ly/9ynct) as integration points can provide a more stable semantic foundation
- BFO example
- `# Using BFO as an upper ontology integration point` `:``Person` `rdfs``:``subClassOf` `bfo``:``Object` `.` `:``Event` `rdfs``:``subClassOf` `bfo``:``Process` `.` `:``Location` `rdfs``:``subClassOf` `bfo``:``SpatialRegion` `.`
- • It maps the domain-specific concept `:Person` as a subclass of BFO’s `Object` category, establishing that entities in the local ontology are continuants that maintain identity over time. • It classifies `:Event` as a subclass of BFO’s `Process` category, indicating that events are occurrences that unfold over time with temporal parts. • It defines `:Location` as a subclass of BFO’s `SpatialRegion` category, specifying that locations represent spatial dimensions rather than material entities.
- Modern workflows leverage AI agents to accelerate ontology development while maintaining quality through human oversight. Agents perform initial entity identification from sample data, validate structural requirements (relationships reference existing nodes, property names are unique, entities have identifying properties), and generate visualizations for expert review

### Entity Resolution: The Foundation of Agent Knowledge


### Entity Resolution: The Foundation of Agent Knowledge

- *entity resolution* determines when different data records refer to the same real-world entity
- While this might sound like a technical data-cleaning task, it’s actually the cornerstone that enables agents to maintain coherent understanding across fragmented organizational knowledge
- For agentic systems, the stakes are equally high. An agent making procurement recommendations needs to know that *Acme Corp*, *Acme Corporation*, and *ACME Co., Ltd* all refer to the same supplier
- Simple string matching fails catastrophically here. Fuzzy matching on individual attributes often fails because variations are intentionally designed to evade detection. What’s needed is *channel consolidation*, connecting fragmented identities based on evidence from multiple overlapping features

#### Evidence-based resolution versus generalization-based AI

- In *generalization-based reasoning* (typical of LLMs), the system learns patterns from training data and generalizes to new situations. When asked *Are these two records the same person?*, an LLM considers statistical patterns learned from examples. It might respond *These seem like the same person because the names are similar and they share an address*. The confidence comes from statistical regularities, not specific evidence. This approach has serious limitations for entity resolution: decisions are nondeterministic, explanations are post hoc rationalizations, cultural variations break down on non-Western names, and confidence scores don’t reflect actual accuracy.
- With *evidence-based reasoning* (entity resolution), the system examines specific features from data records, applies domain-specific matching rules, and builds a case based on concrete evidence. The system can explain its conclusions like this: *These records match with 89% confidence because NAME matched at 87%, ADDRESS matched at 100%, and PHONE matched at 95%*.

#### Entity resolution as graph building blocks

- Entity resolution generates the fundamental components of agent knowledge graphs:
- Entities (nodes) Each resolved entity becomes a node with a stable identifier that persists even as new records are added or corrected. This stability is critical for agent memory so that agents maintain consistent references to entities over time. Relations (edges) Entity resolution systems identify several relationship types: `RESOLVED` (strong matches indicating records refer to the same entity), `POSSIBLY_RELATED` (weaker evidence of connection), and `DISCLOSED` (known relationships from data). These relationship types support different reasoning patterns. An agent investigating fraud might traverse `RESOLVED` edges to find all aliases, then follow `POSSIBLY_RELATED` edges to discover associates. Properties The resolved entity aggregates properties from all contributing records, giving agents access to all known information even when it was originally fragmented across systems. Evidence metadata Critically, entity resolution systems preserve evidence for each match decision, such as which features drove the match, their individual scores, and confidence levels. This metadata enables explainable AI. When an agent makes a decision based on entity connections, it can cite the specific evidence that established those connections.

## Building the Knowledge Graph


## Building the Knowledge Graph

- A knowledge graph is only as valuable as the information it contains
- This section reviews techniques for three stages of the knowledge acquisition pipeline: extraction, entity resolution, and validation.

### Extraction Approaches for Heterogeneous Sources


### Extraction Approaches for Heterogeneous Sources

- Structured database integration When incorporating existing relational or NoSQL databases, consider these approaches: Graph materialization Transform database content into actual graph nodes and edges, either through batch processes or change data capture (CDC) streams. Virtual graph views Create mapping layers that expose relational data as virtual graph structures without physical duplication. Hybrid materialization Materialize frequently used information while dynamically mapping less common patterns.

#### LLM-based extraction from unstructured text

- LLMs excel at extracting structured information from unstructured text
- `def` `extract_knowledge_triples``(``text``,` `domain_ontology``):` `"""Extract subject-predicate-object triples from text using LLM."""` `prompt` `=` `f``"""` `Extract knowledge triples from the following text.` `Use only predicates from the domain ontology:` `{``domain_ontology``.``predicates``}` `Format: [(subject, predicate, object), ...]` `Text:` `{``text``}` `"""` `llm_response` `=` `call_llm_with_structured_output``(``prompt``,` `output_format``=``'json'``,` `schema``=``TRIPLE_SCHEMA``)` `validation_results` `=` `validate_against_ontology``(``llm_response``.``triples``,` `domain_ontology``)` `return` `validation_results``.``valid_triples`
- The `extract_knowledge_triples` function constrains LLM extraction to predicates defined in the domain ontology, ensuring consistency with the knowledge graph’s semantic structure. The function constructs a formatted prompt, applies structured output validation, and filters results against ontological constraints. Production enhancements include extraction templates, multistage pipelines, confidence scoring, and human-in-the-loop (HITL) verification for low-confidence extractions.
- The [iText2KG framework](https://oreil.ly/BiCBs) (now enhanced as ATOM, discussed in [“Temporal dynamics: ATOM”](#ch03_temporal_dynamics_atom_1783966130267323)) represents an innovative method for incremental, topic-independent knowledge graph construction without the need for postprocessing
- `def` `extract_entities_for_all_sections``(``self``,` `sections``:` `List``[``str``],` `ent_threshold``=``0.8``):` `all_entities` `=` `[]` `for` `section` `in` `sections``:` `# Extract entities from the current section` `section_entities` `=` `self``.``ientities_extractor``.``extract_entities``(``context``=``section``)` `# Perform entity disambiguation` `if` `all_entities``:` `# Compare with previously extracted entities` `all_entities` `=` `self``.``matcher``.``process_lists``(` `all_entities``,` `section_entities``,` `"entity"``,` `ent_threshold` `)` `else``:` `all_entities` `=` `section_entities` `return` `all_entities`
- Whereas iText2KG focuses on incremental construction, the [Document-level Retrieval Augmented Knowledge Graph Construction (RAKG) framework](https://oreil.ly/KbNNA) takes a different approach, addressing the limitations of traditional sentence-level extraction. RAKG introduces several novel concepts. It uses intermediate representation units that simplify entity disambiguation and address LLM context limitations, and it gathers all text segments where an entity appears, providing comprehensive contextual information
- `def` `extract_relations``(``self``,` `entity``,` `retrieverVT``,` `retrieverVkg``):` `# Retrieve all text segments mentioning the entity` `text_segments` `=` `retrieverVT``(``entity``)` `# Retrieve similar entities from existing knowledge graph` `related_subgraphs` `=` `retrieverVkg``(``entity``)` `# Generate relationships using LLM with retrieved context` `return` `self``.``llm_rel``(``entity``,` `text_segments``,` `related_subgraphs``)`
- While iText2KG and RAKG excel at static knowledge extraction, the ATOM (AdapTive and OptiMized) dynamic temporal knowledge graph construction framework ([Lairgi, 2026](https://oreil.ly/0-ZZz)) addresses a critical limitation: the temporal dimension of knowledge. Many extraction approaches struggle with two fundamental challenges. First, LLMs exhibit a “forgetting effect” where relationship extraction deteriorates significantly as context length increases. This is particularly problematic for extracting temporal information from longer documents. Second, existing methods conflate observation time (when information was recorded) with validity periods (when facts actually occurred), preventing the accurate temporal reasoning that is essential for agent memory and historical analysis. ATOM introduces atomic fact decomposition as its core innovation. Rather than processing entire documents or lengthy paragraphs, the system decomposes text into minimal, self-contained atomic facts—single statements that each convey exactly one piece of information. Empirical evaluation has determined that maintaining chunk sizes below 400 tokens preserves extraction exhaustivity above 0.8, addressing the forgetting effect while maintaining semantic coherence.
- The framework employs a three-module parallel architecture optimized for scalability: Atomic fact decomposition Documents are split into atomic facts through LLM-guided extraction with careful attention to preserving temporal expressions. Each atomic fact is designed to be understood independently, eliminating the ambiguity that causes extraction errors in longer contexts. Parallel 5-tuple extraction Rather than separating entity and relation extraction (requiring multiple LLM calls), ATOM directly extracts complete temporal 5-tuples (`subject`, `predicate`, `object`, `t_start`, `t_end`) from each atomic fact in a single pass. Critically, the system performs temporal preprocessing during extraction, transforming end-validity statements into affirmative counterparts. For example, *John Doe is no longer CEO on 01-01-2026* becomes `(John_Doe, is_ceo, X, [.], [01-01-2026])`, enabling subsequent LLM-independent temporal resolution. LLM-independent merge Atomic temporal knowledge graphs are merged using distance metric–based entity and relation resolution rather than expensive LLM calls. The parallel merge algorithm employs iterative pairwise merging in a binary tree structure, reducing merge complexity to *O*(log *N*) rounds. Temporal resolution extends validity period histories as new observations arrive, tracking how knowledge evolves over time.
- ATOM’s distinguishing feature is *dual-time modeling*, which allows it to maintain separate observation timestamps and validity periods for each fact. Consider a news article published January 23, 2020, stating that *The virus spread to 10 countries*. The observation time records when this information became known (January 23), while the validity period captures when the spread actually occurred (potentially days earlier). This distinction prevents the temporal misattribution that plagues single-timestamp approaches and enables agents to reason about the difference between “when we learned it” versus “when it happened.”

### Automating Knowledge Graph Construction with Multi-Agent Systems


### Automating Knowledge Graph Construction with Multi-Agent Systems

- The pipeline architecture includes: Intent clarification Transforming vague goals into structured objectives File discovery Identifying and proposing relevant data sources Schema proposal Inferring nodes, relationships, and properties from structured or unstructured data using proposer-critic validation Deterministic construction Executing approved schemas through rule-based processes
- Current limitations include how it handles ambiguity (when similar terms require context-aware extraction), complex schema inferences (those requiring domain-specific models), and entity resolution accuracy (addressed through hybrid approaches combining embeddings with string similarity)

### Entity Resolution and Linking Across Graphs


### Entity Resolution and Linking Across Graphs

- *Entity linking* connects entities extracted from unstructured text (subject graph) to trusted entities in structured data (domain graph), creating `CORRESPONDS_TO` relationships that integrate the three-graph architecture.
- Subject entities lack the identifiers and complete attributes of domain entities. For example, `Subject_Product(name="the` `Stockholm` `chair")` must link to `Prod⁠uct​(product_id="PROD_12345",` `product_name="Stockholm Chair")` despite text differences, attribute mismatches, and extraction uncertainty.
- Production-grade entity linking progressively narrows from candidates to confident matches: Property key correlation Normalizes different property names to map concepts (removing prefixes, handling case variations: `"product_name"` → `"name"`). Value similarity matching Compares actual values using Jaro-Winkler distance (0.0–1.0 scores handling typos and prefix matching). Threshold selection balances precision and recall: 0.95 for high-stakes applications, 0.85 as recommended default, 0.75 for exploratory analysis. Context-aware validation Uses graph neighborhood patterns to validate matches through co-occurrence patterns (do both entities appear with the same related entities?), temporal consistency (do review dates align with product availability?), and cross-entity validation (do multiple links form coherent patterns?). Subject and domain neighborhoods naturally differ due to different graph layers, so focus validation on temporal alignment and structural coherence rather than exact neighborhood matching.
- Measure linking rate (target >75%), average confidence (target >0.85), ambiguous subjects (target <5%), and coverage. Handle unmatched entities by reviewing high-mention unlinked subjects to identify catalog gaps, disambiguate vague mentions using context and temporal alignment, and add type validation to prevent false positives between similar entities.

## Knowledge Representation in Practice: DevOps Agent


### Designing the DevOps Ontology


### Homoiconic Knowledge Representation for Agent Adaptability


### Querying the Knowledge Graph: Making the Digital Twin Useful


### Measuring Context Quality: Ensuring the Digital Twin Stays Accurate


### Measuring Context Quality: Ensuring the Digital Twin Stays Accurate

- Implementing continuous measurement of knowledge graph quality across four dimensions—precision, exhaustiveness, freshness, and coverage

## Summary


## Chapter 4. Agentic Graph Memory Systems

- 4. Agentic Graph Memory Systems
- You will move from understanding why current approaches fail to implementing living memory architectures and training your agents to actually use those architectures. Along the way, we will look at production systems like [Cognee](https://cognee.ai), [mem0](https://mem0.ai), and [Zep](https://getzep.com) that are already solving these challenges at scale.

## Architecting Graph Memory Systems


## Architecting Graph Memory Systems

- An effective agent does not just “have” memory; it sits on top of a deliberately designed memory architecture

### The Problem: Why Your Current Memory Approach Fails


### The Problem: Why Your Current Memory Approach Fails

- [Letta Leaderboard for benchmarking agentic memory](https://oreil.ly/ILMc6) describes eight distinct failure modes that tend to show up together
- Models fail to recognize when relevant information is already available and issue unnecessary searches. Memory hierarchies break down, so trivia sits in prime memory while critical facts get archived or dropped. During conversation, agents regularly miss key pieces of information even when they are present. As the volume of data grows, retrieval accuracy degrades and performance drops.
- Conflicts make the situation even messier. New information often overwrites old facts instead of being layered as context, so the system cannot explain how or why things changed. Related pieces of information remain isolated in separate silos, preventing cross-reference and pattern recognition. Event timelines blur together, and agents lose temporal coherence altogether. Systems that work acceptably with hundreds of facts quietly collapse when exposed to thousands.
- Even a one million–token context window will fill faster than you think; a few months of user interactions will exhaust your budget. At that point, either you drop old information and your agent forgets, or you compress everything and lose critical details. Recent work on recursive language models (RLMs) ([Zhang, 2025](https://oreil.ly/852Ca)) demonstrates that even state-of-the-art systems suffer from *context rot*, where performance degrades as context length increases regardless of whether you hit the hard limit
- Things get worse when you consider time. Information changes: users move, change jobs, and develop new preferences. Without temporal awareness, your agent either forgets the past or gets confused by contradictions. It cannot answer *What was the configuration when the outage occurred?* after you have updated everything, because the underlying system has no way to represent *what used to be true*. When multiple agents process information concurrently, the problem compounds. Without coordination, whichever writes last wins, and you have no record that a conflict existed. The agentic memory system must be treated like a Git repository: version every ontological commit, let agents branch when they begin processing and merge when they finish, and run continuous integration (CI) checks before accepting changes. With these safeguards, schema drift becomes visible and reversible rather than silent corruption.
- as contexts grow, retrieval itself starts to fail. The *lost in the middle* problem means that critical facts buried inside huge prompts might as well not exist. The very mechanism you rely on to improve memory (larger context windows) ends up hiding the information you care about most.
- Rigid schemas let you express powerful queries and invariants, but they struggle with messy, real-world text and edge cases. Purely unstructured storage makes it easy to ingest anything but hard to maintain reliability. Practical systems mix both: structured cores for trusted data surrounded by more flexible layers for exploratory or extracted knowledge
- Agent trajectories discover structure through problem-directed traversal. The relationships that are traversed are the relationships that are real. Structural equivalences reveal themselves when different agents solving different problems follow analogous paths
- You also need to think about whose memory you are building. Agents require private, per-user histories as well as shared, global knowledge

#### Cache sharing in multi-agent systems

- Three cache-sharing patterns emerge from distributed systems practice, each with different trade-offs:
- Broadcast This is the simplest pattern: every agent’s cache updates are visible to every other agent. When a planning agent identifies a budget constraint, all execution agents see it immediately. Broadcast works for small agent teams (two to four agents) where coordination overhead is low and all agents operate in the same problem domain. It fails at scale because agents drown in irrelevant updates.
- Publish-subscribe This adds selectivity. Agents declare which cache partitions they care about. A security review agent subscribes to cache updates tagged with “permissions” or “authentication” but ignores updates about UI layout. This is the pattern that multi-agent frameworks like [Agora](https://oreil.ly/JVos3) implement: agents publish findings to named channels, and other agents consume from channels relevant to their role. Overhead is incurred in defining the channel taxonomy, but the payoff is that agents receive only what they need.
- Request-grant This pattern gives the most control. Agent B explicitly requests a specific piece of cached knowledge from Agent A. No data moves until requested. This pattern suits workflows where agents have clear handoff points: a code generation agent finishes a module, and a test generation agent requests its interface signatures before writing tests. Request-grant produces the least cache pollution, but because it requires agents to know what to ask for, it assumes well-defined task boundaries.

![](https://readwise.io/reader/pcei/gAAAAABqkVp8TrZK5j7T11gXy6wnNJUKWDkHPTY_T2AYD1GFF76RLZKyEI2WpG2q9mN0s8cNRxmBJw0lSeIKWIkn7DUMdhb1wjwHmhA6hQk5WE5W_pHqwAg=/agrg_0401.png)


### The Solution: Graph Memory


### The Solution: Graph Memory

- *Graph memory* addresses these failures by enabling what Letta calls *agentic memory management*: agents that actively control their memory through deliberate operations instead of passively relying on whatever happens to be in the context window.
- Production systems like Cognee, mem0, and Zep have each developed strategies to address these specific failure modes
- Cognee Cognee starts from a graph-first architecture, treating memory as interconnected knowledge networks rather than as rows, documents, or vectors. Its *extract-cognify-load (ECL) pipeline* focuses on building semantic relationships during ingestion, not as an afterthought. Benchmarks report high accuracy on memory tasks precisely because Cognee emphasizes how facts relate, not just whether they exist. When your agent needs to reason about complex regulatory documents or analyze code dependencies, this relationship-centric approach becomes a major advantage.
- Mem0 Mem0 approaches the problem through selective storage and consolidation. Instead of trying to keep everything, it preserves salient facts and continuously merges or discards information based on relevance. As a result, it can show higher accuracy than baseline “built-in” memories while substantially reducing latency. Its two-phase pipeline is designed to prevent memory bloat, which is exactly what you need when your agent handles thousands of conversations per day and must still respond quickly.
- Zep Zep focuses on time. It implements temporal knowledge graphs with bitemporal tracking, recording both when events occurred in the domain and when the system learned about them. Built on the [open source Graphiti framework](https://oreil.ly/IX1i_), Zep demonstrates significant gains on preference-based questions by treating temporal history as first-class data. For domains like healthcare, finance, or customer support—where *What did we know, and when did we know it?* is a core question—this design is particularly powerful. This bitemporal approach is the foundation for treating your knowledge graph like a Git repository. Just as Git tracks both the content of files and the history of commits, bitemporal graphs track both what was true in the world and when the system recorded that truth.
- The main lesson from the Letta Leaderboard is straightforward: the quality of memory management directly determines agent performance on long-running tasks
- For your agents, this implies a shift in mindset. They must learn to optimize their own memory patterns through experience rather than relying on fixed heuristics
- when contradictions appear, they must handle them by maintaining versioned, time-aware knowledge instead of blindly overwriting the past
- They need to track *when* facts were true, not just *what* was true, so they can answer temporally grounded questions
- Validate that new facts do not violate constraints, that sources still exist, and that extractions are reproducible

## Representing Memory as Graphs


## Representing Memory as Graphs

- Memory adds a different dimension. Now you care about *when* things happened, *how* they relate across time, and *what* the agent should remember or forget

### Understanding the Architecture Evolution

- In practice, memory architectures tend to evolve through a common progression: Flat storage Each interaction or fact is stored independently. Vector-enhanced storage You add embeddings for semantic search. Structured relationships You explicitly model how things connect. Temporal awareness You track when facts and relationships change. Hierarchical organization You introduce layers and abstractions.
- CPU architecture organizes memory into three layers: registers and I/O buffers for immediate data, cache for active working sets, and persistent storage (RAM, disk) for everything else. Agent memory benefits from the same decomposition.
- The *I/O layer* handles raw inputs and tool outputs as they arrive. When an agent calls a web search API, parses a PDF, or receives a user message, that data lands in the I/O buffer. The data is unstructured, ephemeral, and high volume. Most of it will be discarded. A coding agent running a test suite generates hundreds of lines of standard output; the I/O layer holds all of it, but only the failure traceback matters for reasoning.
- The *cache layer* holds the agent’s active reasoning context—the subset of knowledge the agent is working with right now. This is not the full conversation history; it is the extracted facts, constraints, and intermediate conclusions that bear on the current task. When a research agent is synthesizing three papers, its cache contains the key claims from each paper, the contradictions it has identified, and its emerging thesis. The cache is structured, typically as a subgraph of the full knowledge graph; it is mutable, being updated as reasoning progresses; and it is bounded because an agent that caches everything has cached nothing).
- The *persistent layer* stores the full history—every fact the agent has ever learned, every decision it has made, and every correction it has received—with temporal versioning. This is where the Git metaphor from earlier in this chapter applies most directly. Persistent memory supports branching (exploring alternative reasoning paths), tagging (marking significant state snapshots), and merging (reconciling divergent knowledge). The persistent layer is the only layer that survives across sessions.
- Systems like [Cognee](https://oreil.ly/khEhD), [mem0](https://oreil.ly/dIMAU), [Zep](https://oreil.ly/Pm1qu), and [Letta](https://oreil.ly/UDHpT) each implement these three layers, though they draw the boundaries differently. Cognee emphasizes the persistent layer with its graph construction pipeline. Mem0 optimizes the cache layer with its memory extraction and retrieval. Zep balances both with its temporal knowledge graphs. Letta puts the cache-to-persistent boundary under the agent’s own control, paging facts between a small working set and a larger archive

### Essential Graph Components


### Essential Graph Components

- A graph-based memory system is built from three core pieces: *nodes*, *edges*, and *subgraphs*
- Nodes hold the things you care about. Edges describe how those things relate. Subgraphs bundle related pieces of memory into coherent contexts.

![](https://readwise.io/reader/pcei/gAAAAABqkVp8BG0YAFWry5hcOEv21DBeGbRIseDGeuaxP9lVx5Nx0Tb7h4_Gql4WIMjlJPqkMbiQreg7EmjtQQ0Z9BODznY64zONK7ryMBRzzHAEpoFamkQ=/agrg_0402.png)

- A *node* represents a unit of knowledge: a person, project, incident, decision, or even a specific conversation turn
- `class` `MemoryNode``:` `def` `__init__``(``self``,` `content``,` `node_type``):` `self``.``id` `=` `generate_uuid``()` `self``.``content` `=` `content` `self``.``type` `=` `node_type` `self``.``created_at` `=` `datetime``.``now``()` `self``.``embedding` `=` `generate_embedding``(``content``)` `self``.``metadata` `=` `{}` `self``.``edges` `=` `[]` `def` `add_edge``(``self``,` `target_node``,` `relationship_type``,` `metadata``=``None``):` `edge` `=` `Edge``(` `source``=``self``.``id``,` `target``=``target_node``.``id``,` `type``=``relationship_type``,` `created_at``=``datetime``.``now``(),` `metadata``=``metadata` `or` `{},` `)` `self``.``edges``.``append``(``edge``)` `return` `edge`
- Each field in [Example 4-1](#ch04_example_1_1783966134138599) does real work: `id` This is the stable identity for this node. When you later learn more about “John from marketing,” you want to find and update the same node, not create a new one. Stable identifiers are what make consolidation and entity-centric reasoning possible. `content` This holds the primary text or payload for the node, while `type` distinguishes people from projects, incidents from decisions, and so on. This lets you branch logic: a `person` node might trigger one extraction pipeline, while an `incident` node uses another. `embedding` This is computed when the node is created. That vector representation powers semantic search so you can find relevant memories even when the question uses different wording than the original content. Doing this once at creation time avoids recomputing embeddings on every query. `metadata` This gives you extensibility without constant schema migrations. You can add importance scores, confidence levels, source URLs, or user IDs as your system matures without breaking earlier data. `edges` and `add_edge` These make nodes more than isolated blobs of text. When you learn that *Sarah manages Project X*, you create an edge connecting Sarah’s node to Project X’s node. The relationship is now traversable from either side: *Which projects does Sarah manage?* and *Who manages Project X?* become the same operation in reverse.
- Beyond basic node types like `person` or `incident`, production systems benefit from separating nodes by their *epistemic status*—distinguishing what the agent has observed from what it believes. In their 2025 paper [“Hindsight is 20/20: Building Agent Memory That Retains, Recalls, and Reflects”](https://oreil.ly/H-flJ), Latimer and colleagues organize memory into four networks: World network Objective facts about external reality Experience network The agent’s own actions (first-person) Opinion network Subjective beliefs with confidence scores Observation network Synthesized entity summaries
- This separation enables traceability: when users ask, *How do you know that?* the agent can distinguish evidence (world/experience) from inference (opinion) from summary (observation).
- An *edge* captures how two nodes relate. In a memory system, the edge is usually more interesting than either endpoint on its own.
- At a minimum, edges should record the relationship type (for example, `manages`, `assigned_to`, `caused_by`) so the agent can interpret what the connection means. For production systems, you will typically also track when the relationship was valid, how confident you are in it, and any extra context that will help explain the link later.
- A *subgraph* is a cluster of nodes and edges that work together to answer a particular kind of question. Instead of throwing all memories into a single undifferentiated graph, you group related information into contextual slices.
- Zep’s production architecture is a useful mental model. It separates memory into the following: Episode subgraphs Store raw interactions—the literal conversations and events. Semantic entity subgraphs Store extracted knowledge—what the system has learned about people, projects, and concepts. Community subgraphs Represent higher-level clusters—how entities and ideas group together over time.
- Episodes can be append-only and heavily compressed. Entities can be carefully deduplicated and enriched. Communities can be rebuilt or reclustered as new information arrives

### Temporal Awareness: Making Memory Evolve


### Temporal Awareness: Making Memory Evolve

- Temporal awareness solves this by tracking three different notions of time:
    - When a relationship was valid in the real world
    - When your system ingested or updated that relationship
    - When you want to query the state of the world
- `class` `TemporalEdge``:` `def` `__init__``(``self``,` `source``,` `target``,` `relationship``):` `self``.``source` `=` `source` `self``.``target` `=` `target` `self``.``relationship` `=` `relationship` `self``.``valid_from` `=` `datetime``.``now``()` `self``.``valid_until` `=` `None` `# None means currently valid` `self``.``ingested_at` `=` `datetime``.``now``()` `self``.``invalidation_reason` `=` `None` `# Link type for weighted traversal (Latimer et al., 2025)` `self``.``link_type` `=` `"entity"` `# {temporal, semantic, entity, causal}` `self``.``weight` `=` `1.0` `# Traversal weight for graph search==` `def` `invalidate``(``self``,` `reason` `=` `None``):` `"""Mark this relationship as no longer valid."""` `self``.``valid_until` `=` `datetime``.``now``()` `self``.``invalidation_reason` `=` `reason` `def` `was_valid_at``(``self``,` `timestamp``):` `"""Check if relationship was valid at a specific time."""` `return` `(` `self``.``valid_from` `<=` `timestamp` `and` `(``self``.``valid_until` `is` `None` `or` `timestamp` `<` `self``.``valid_until``)` `)`
- Here is how these fields change what your agent can do:
    - `valid_from` and `valid_until` define when the relationship was considered true. When you first learn “Sarah manages the marketing team,” you set `valid_from` to now and leave `valid_until` as `None`. When Sarah changes roles, you call `invalidate`, which closes the window without deleting history.
    - `ingested_at` reflects when your system found out about the change, which might be days after it became true. This is crucial for debugging: if the agent made a decision on Wednesday based on stale data, `ingested_at` will tell you that the updated information was not yet available.
    - `invalidation_reason` gives you an audit trail. Instead of a mysterious change in state, you see why the relationship ended: perhaps it was a role change, project completion, correction of bad data, or some other reason. This extra line of text can make the difference between a user trusting or distrusting the system.
    - `was_valid_at` lets you reconstruct the world at any point in time. Now, questions like *What did our infrastructure look like right before the outage?* or *Who did the agent think owned this service when it made that prediction?* become first-class queries rather than forensic guesswork.
- Temporal edges turn your memory graph from a static snapshot into a movie you can pause, rewind, and inspect.

### Implementation: Building Your First Graph Memory System


### Implementation: Building Your First Graph Memory System

- We will focus on the core loop: turning raw text into entities and relationships, storing them with temporal awareness, and then querying them effectively. At a minimum, you need four capabilities:
    - A place to store the graph (an in-memory structure is fine to start; a graph database like Neo4j comes later)
    - An embedding model for semantic search over nodes and content
    - An entity and relationship extractor to decide what to remember and how it connects
    - A query layer that can combine vector search, keyword search, and graph traversal
- Memory orchestration class
- `class` `GraphMemory``:` `def` `__init__``(``self``,` `embedding_model``):` `self``.``nodes` `=` `{}` `self``.``edges` `=` `[]` `self``.``embedding_model` `=` `embedding_model` `def` `add_memory``(``self``,` `content``,` `context``=``None``):` `# Extract entities and relationships` `entities` `=` `self``.``extract_entities``(``content``)` `# Create or update nodes` `for` `entity` `in` `entities``:` `node` `=` `self``.``find_or_create_node``(``entity``)` `# Identify relationships` `relationships` `=` `self``.``extract_relationships``(``content``,` `entities``)` `# Create edges with temporal awareness` `for` `rel` `in` `relationships``:` `self``.``create_temporal_edge``(` `rel``[``"source"``],` `rel``[``"target"``],` `rel``[``"type"``],` `context``,` `)` `def` `query``(``self``,` `question``,` `timestamp``=``None``):` `# Generate query embedding` `query_embedding` `=` `self``.``embedding_model``.``embed``(``question``)` `# Find relevant nodes through multiple methods` `semantic_matches` `=` `self``.``semantic_search``(``query_embedding``)` `keyword_matches` `=` `self``.``keyword_search``(``question``)` `# Traverse graph for connected information` `expanded_context` `=` `self``.``expand_search_context``(` `semantic_matches` `+` `keyword_matches``,` `timestamp``,` `)` `return` `self``.``format_memories_for_llm``(``expanded_context``)`
- A critical design choice is extraction *granularity*. Sentence-level extraction produces fragmented facts that lose cross-turn context. The “Hindsight” paper instead extracts two to five comprehensive narrative facts per conversation, each intended to cover an entire exchange rather than a single utterance, be narrative and self-contained, include all relevant participants, and preserve the pragmatic flow.
- So far, every relationship has linked two nodes. Real life is rarely that simple. A single incident can involve many services, multiple people, and a series of decisions. Modeling this as pairwise edges quickly becomes unwieldy: for a meeting with 10 participants, you would need 45 edges just to represent “attended together.” As covered in [Chapter 3](private://read/01m13whyk8ssegw20k3a9kfy10/ch03.html#ch03), a *hypergraph* solves this by allowing edges that connect more than two nodes.
- Hyperedge
- `class` `HypergraphMemory``(``GraphMemory``):` `def` `create_multi_entity_relationship``(` `self``,` `entities``,` `relationship_type``,` `metadata` `):` `# Create a hyperedge connecting multiple nodes` `hyperedge` `=` `HyperEdge``(` `id``=``generate_uuid``(),` `type``=``relationship_type``,` `participants``=``[``e``.``id` `for` `e` `in` `entities``],` `metadata``=``metadata``,` `created_at``=``datetime``.``now``(),` `)` `# Link all participants` `for` `entity` `in` `entities``:` `entity``.``add_hyperedge``(``hyperedge``)` `# Enable efficient queries` `self``.``index_hyperedge``(``hyperedge``)` `return` `hyperedge`
- The bidirectional links make querying natural. Starting from a person, you can traverse to every hyperedge they participate in and then to the other participants and topics. Starting from a hyperedge, you can ask *Who was in the room?* or *What other meetings involved this same group?* Indexing hyperedges by type, time, and participant IDs keeps these queries fast even as the number of events grows.

## Four Essential Memory Operations


## Four Essential Memory Operations


![](https://readwise.io/reader/pcei/gAAAAABqkVp81EGPZGDmRz0guT5s7H0_9AKRuvAcL8MN4dT5FoPji32afC03tN4KeqY5dnX_pfHs66PBZVgo7UuGasA9dyJALiVzOZWxByPUOUoUdLJRqro=/agrg_0403.png)


### Consolidation: From Experience to Knowledge

- Your agent accumulates many interactions, but most of them are redundant, overlapping, or partially inconsistent. *Consolidation* transforms these raw experiences into structured, durable knowledge.
- When multiple queries share the same underlying context, the cost savings compound: precomputed enrichments amortize across every subsequent interaction.

### Indexing: Organizing for Speed

- In practice, you will often layer:
    - Semantic indices for concept-level similarity (what is *about* the same thing)
    - Keyword or lexical indices for exact terms and identifiers
    - Temporal indices keyed by time ranges or event order
    - Relational indices that make it cheap to traverse common patterns in the graph
- *Indexing* creates multiple access paths so queries can find relevant memories regardless of how users phrase their requests.

### Updating: Handling Change Gracefully

- *Updating* is the operation that lets your agent absorb new information without corrupting its understanding of the past.
- key design principle is to preserve history while clearly marking current truth.

### Retrieval: Finding What Matters

- *retrieval* is where memory meets behavior. Retrieval is not just a database query; it is intelligent context assembly under uncertainty. No single retrieval strategy catches everything. Production systems typically combine:
    - Semantic search to find conceptually related memories
    - Keyword search for precise identifiers and error messages
    - Graph traversal to uncover connected entities and events
    - Temporal filters to bias toward recent or time-relevant information
- The magic of merging these signals can be formalized. Hindsight (Latimer et al., 2025) runs all four retrieval channels in parallel, then combines them using reciprocal rank fusion (RRF).

## Production Patterns and Architectures


## Production Patterns and Architectures

- three representative approaches:
    - Hierarchical memory in Letta (MemGPT)
    - Evolving knowledge networks in the A-Mem pattern
    - Real-time incremental updates in Graphiti by Zep

### The Letta (MemGPT) Approach: Hierarchical Memory


### The Letta (MemGPT) Approach: Hierarchical Memory

- Letta popularized *hierarchical memory* ([Packer et al., 2024](https://oreil.ly/LonVK)), which mirrors human cognition. It’s a small, fast working set backed by a much larger searchable archive. The core idea is to make forgetting and archiving explicit parts of the design instead of afterthoughts.
- `class` `HierarchicalMemory``:` `def` `__init__``(``self``,` `core_limit``=``2000``):` `self``.``core_memory` `=` `CoreMemory``(``limit``=``core_limit``)` `self``.``archival_memory` `=` `ArchivalMemory``()` `self``.``recall_memory` `=` `RecallMemory``()` `def` `process_interaction``(``self``,` `user_input``,` `agent_response``):` `# Store in recall memory` `self``.``recall_memory``.``add``(``user_input``,` `agent_response``)` `# Extract important facts for core memory` `facts` `=` `self``.``extract_key_facts``(``user_input``,` `agent_response``)` `for` `fact` `in` `facts``:` `if` `self``.``core_memory``.``is_full``():` `# Move least-used items to archival` `archived` `=` `self``.``core_memory``.``evict_least_used``()` `self``.``archival_memory``.``store``(``archived``)` `self``.``core_memory``.``add``(``fact``)`
- gives each memory layer a clear job: `recall_memory` Keeps raw interaction history so you can answer questions like *What did we talk about yesterday?* `core_memory` Holds the highest-value, most frequently accessed facts that should be instantly available. `archival_memory` Provides effectively unlimited, slower storage for everything else.
- `extract_key_facts` method decides what deserves scarce core space.

### The A-Mem Pattern: Evolving Knowledge Networks


### The A-Mem Pattern: Evolving Knowledge Networks

- the A-Mem pattern ([Xu et al., 2025](https://oreil.ly/0uipl)) focuses on *how new information changes what you already know*. In practice, new facts rarely arrive in isolation. When your agent learns something like *Sarah now leads the product team*, that should ripple through existing beliefs about Sarah, the product team, and the org chart.
- `class` `EvolvingMemory``:` `def` `add_memory``(``self``,` `content``):` `# Create new memory node` `new_node` `=` `self``.``create_node``(``content``)` `# Find related existing memories` `related` `=` `self``.``find_related_memories``(``new_node``)` `# Form connections and trigger evolution` `for` `related_node` `in` `related``:` `relationship` `=` `self``.``determine_relationship``(``new_node``,` `related_node``)` `self``.``create_edge``(``new_node``,` `related_node``,` `relationship``)` `# Evolve the network` `self``.``evolve_connected_memories``(``new_node``,` `related``)`
- `find_related_memories` method Uses semantic similarity (and sometimes structural hints) to locate memories that might be impacted. For *Sarah now leads the product team*, that includes prior nodes about Sarah, the previous leader, the product org, and related projects. `determine_relationship` method Classifies how the new node relates to each existing one: is this an update, a refinement, a contradiction, or a new branch? Those relationship types drive how aggressively you propagate changes. `create_edge` method Ties the new fact into the existing network, but the real work happens in `evolve_connected_memories`. That step revises the context of affected nodes: older memories about Sarah’s previous role may be marked as historical, and nodes about the product team may be updated to reference the new leadership.

### The Graphiti Pattern: Real-Time Performance


### The Graphiti Pattern: Real-Time Performance

- Graphiti by Zep illustrates a pattern for keeping query and update times low ([Rasmussen et al., 2025](https://oreil.ly/Qp75T)): *do everything incrementally*. Instead of recomputing embeddings, entities, or neighborhoods for the entire graph, touch only what the latest change requires.
- `def` `add_episode``(``self``,` `episode_content``):` `# Extract entities without reprocessing entire graph` `new_entities` `=` `self``.``extract_entities``(``episode_content``)` `# Resolve against existing entities` `resolved_entities` `=` `self``.``entity_resolution``(``new_entities``)` `# Update only affected portions` `self``.``incremental_update``(``resolved_entities``)`
- each step is designed to localize work: `extract_entities` method Processes only the new episode content. There’s no backfill over historical data and no full-graph re-embedding. `entity_resolution` method Prevents graph bloat by matching new mentions to existing nodes. If the user refers to *the marketing director* and you already have `Sarah (Director of Marketing)` in the graph, this step ensures these references resolve to the same entity rather than creating duplicates. `incremental_update` method Modifies only the impacted neighborhood: the few nodes and edges touched by the new entities and relationships. The rest of the graph stays untouched, which keeps write operations predictably fast.

## Comparing Production Systems


## Comparing Production Systems


## Production-Ready Features and Operations


## Production-Ready Features and Operations


### Reasoning and Recommendations

- the whole point of memory is to support better reasoning.

#### Multi-hop reasoning

- Instead of answering questions with single lookups, your agent connects information across multiple nodes to build an argument.
- works by decomposing complex queries into sub-questions, gathering evidence for each piece, then finding valid reasoning paths that connect those pieces.

#### Intelligent recommendations

- Graph memory also upgrades recommendations from heuristic guesses to structured analogies. The key idea is that similar situations often share similar solutions, and a graph is a natural way to represent those similarities.
- When generating recommendations, your agent can:
    - Find analogous past situations in the graph
    - Extract what made those past interventions successful
    - Adapt those patterns to the current context, accounting for key differences
    - Weight each recommendation by similarity, recency, and observed success rate

#### Debugging and maintenance

- Production-grade graph memory needs guardrails: health monitoring, visualization, conflict handling, and ongoing performance tuning.
- Start by making the health of your graph visible. A production graph is a living system: nodes and edges are constantly being added, updated, and pruned.
- practical way to begin is with a small dashboard of core metrics that describe how the graph is evolving
- Node growth rate
- Tracks how quickly new entities and events are being added. A steady, domain-aligned growth curve usually signals healthy ingestion. Sudden spikes often mean a broken parser, a runaway source, or an ontology change that is exploding the number of nodes
- Edge density
- Captures how interconnected your graph is. Too few edges, and your agent cannot perform multi-hop reasoning because everything looks isolated. Too many edges, and every traversal turns into a combinatorial explosion. In practice, you monitor average degree and the distribution of high-degree nodes (hubs).
- Cluster balance
- Tells you whether your graph is partitioned in a way that matches reality. Community detection or sharding schemes will naturally create clusters around services, teams, or domains. When a single cluster starts to dominate, it can signal modeling issues, such as overly generic entities that “glue” unrelated areas together, or misconfigured sharding that packs everything into one partition.
- Query latency
- Connects graph structure back to user experience. You care not only about the average but also P95 and P99 latencies for your key query types: retrieval, neighborhood expansion, multi-hop reasoning, and temporal lookups. Rising tail latencies often correlate with increasing edge density or poorly constrained queries. By tying latency metrics back to graph structure metrics, you can decide whether to tune the query layer, prune paths, or adjust schemas
- Memory conflicts
- Measures how often new facts contradict existing ones. This can be as simple as tracking how many updates flip a property’s value, or as complex as logging explicit conflict markers when two sources disagree. A low, steady rate is expected in any dynamic environment. A sudden increase usually means an upstream data-quality issue or a new source with incompatible semantics
- Temporal consistency
- Focuses on whether your time-based data remains logically coherent. Here you look for impossible or overlapping sequences: resources that appear to be in two conflicting states at the same timestamp, events that reference future versions of entities, or validity windows that never close. Simple checks, such as verifying that start times precede end times or that version numbers increase monotonically, go a long way. More advanced systems track temporal invariants (for example, a deployment must precede the errors it causes) and alert when those invariants are violated
- These metrics only become useful when they are wired into action. When health checks cross thresholds, your system should trigger automated maintenance workflows: rebalancing clusters, rebuilding indices, tightening extraction rules, or throttling noisy sources

#### Visualization and debugging tools

- Even with good metrics, graphs can feel opaque in production. Mature systems lean on visualization and debugging tools to make memory behavior inspectable

#### Conflict resolution

- Contradictory information is inevitable as your system ingests more sources and as reality itself changes. A production system needs a consistent approach to conflict resolution
- In practice:
    - When new information is more recent and more credible, you can treat it as the active truth while preserving the older version for history.
    - When sources have different authority levels, you can maintain both facts but assign them different confidence weights.
    - When uncertainty remains high, keep both versions, mark the conflict explicitly, and let downstream reasoning components decide how to use them.

#### Performance optimization

- As your graph grows, performance tuning shifts from a nice-to-have to a survival skill
- Three strategies tend to matter most in production: Path pruning Remove redundant or low-value connections that slow traversal without improving answers. The goal is to keep enough edges for connectivity and reasoning while trimming those that only add noise. Node compression Collapse highly similar nodes into summary or canonical representations, with links back to the original details when full fidelity is needed. This keeps the active graph compact while preserving provenance for debugging and compliance. Cold storage Move rarely accessed memories to cheaper, slower storage tiers. They remain searchable via background processes or batched queries but do not burden your hot query path or primary infrastructure.

### Use Case Optimizations


### Use Case Optimizations

- The right operational and modeling choices depend heavily on your primary use case and the style of interaction you are supporting
- For conversational AI in the spirit of mem0’s approach, you typically prioritize recent context and simplicity of integration
- Recency weighting (for example, exponential decay) keeps the latest interactions front and center. A *one-day integration* story matters so that product teams can experiment quickly
- For complex reasoning in the spirit of Cognee’s approach, you invest more in structure and depth. You build rich ontologies that capture domain knowledge explicitly, optimize for multi-hop traversal instead of just local neighborhoods, and, where appropriate, integrate formal logic
- For temporal applications in the spirit of Zep’s approach, time becomes your organizing principle. You implement bitemporal tracking consistently, not just in a handful of tables. You optimize for time-range and point-in-time queries, maintain complete audit trails that link decisions to the knowledge available at the time, and support reconstructing past states for debugging and compliance reviews

## Training Your Agents to Use Memory


## Training Your Agents to Use Memory

- Out of the box, LLMs have no idea how to:
    - Decide what is worth remembering (*coffee preference* versus *drinking coffee right now*)
    - Choose between creating new memories and updating existing ones
    - Balance retrieval benefits against context pollution
- This is where recent work on learned memory, such as MEM1 ([Zhou et al., 2025](https://oreil.ly/p2_RZ)), becomes important. MEM1 is a research framework that treats memory not as a static database feature but as a behavior that agents learn through reinforcement learning

### The MEM1 Revelation: Let Them Learn, Not Follow Rules


### The MEM1 Revelation: Let Them Learn, Not Follow Rules

- key insight from MEM1 is simple but profound: agents can *learn* effective memory strategies through experience instead of following handcrafted rules. Rather than encoding detailed policies about what to store and when to retrieve, you train the agent and memory system together and let memory behavior emerge.
- reported outcomes are striking:
    - Agents learned to distinguish important information from trivia without explicit heuristics.
    - Memory consolidation strategies emerged from the demands of the task, not from schema diagrams.
    - Smaller 7B models with learned memory behavior outperformed 70B models with manually engineered memory policies.

### From Static Rules to Learned Strategies


### From Static Rules to Learned Strategies

- Most production systems start with rule lists:
    - *Store user preferences but not current activities.*
    - *Update existing nodes when information changes.*
    - *Retrieve only highly relevant memories.*
- These rules work until they do not. They clash, produce edge cases, and become harder to maintain as your system grows

### The Three Phases of Training


### The Three Phases of Training


![](https://readwise.io/reader/pcei/gAAAAABqkVp8J9ixBpTfDgMyo9xdecPYyeV-ycTSO9WqoPZ8QXSeEdk4dMzIwJQb8ieTYMyX9rueZjR4hJhz70e-KW4rZuDdt6G6Xvpf_5wOItU1H9uJl94=/agrg_0404.png)


#### Phase 1: Task-oriented learning

- Do not train memory in the abstract. Train on the tasks your agent actually needs to perform. Instead of generic memory training like *Learn to store and retrieve information effectively*, train with real task rewards. Determine if the agent completed the user’s request.
- In MEM1, agents trained on question-answering tasks. They did not learn generic storage habits; they learned whatever memory behavior improved answer accuracy

#### Phase 2: Consolidation through constraints

- The next step is to force trade-offs. MEM1’s real breakthrough was not just training but training under a memory budget. When agents cannot store everything, they must learn what actually matters

#### Phase 3: Multi-objective mastery

- Finally, MEM1 shows that agents trained on relatively simple, two-objective tasks can generalize to more complex, multi-objective scenarios. They do this by learning general consolidation strategies rather than brittle, task-specific tricks. You can mirror this by gradually increasing task complexity: 1. Single objectives Answer one type of question or complete one kind of action. 2. Dual objectives Balance two goals, such as accuracy and latency. 3. Realistic multi-goal interactions Juggle user satisfaction, cost, latency, and safety.

### Practical Training Strategies


### Practical Training Strategies


#### Reward task success, not memory perfection

- If you reward agents for recalling or storing everything, they will happily overfit to hoarding. Instead, tie rewards to task outcomes and let memory be a means, not an end

#### Use masked training for specialized behaviors

- MEM1 uses masked trajectories to keep training signals clear. You can apply the same idea by separating out learning signals for different memory components:
    - Retrieval modules train only on retrieval decisions and their downstream impact.
    - Storage modules train only on what gets written and how it affects success.
    - Consolidation modules train on how state compression impacts future performance.

#### Implement curriculum learning

- Do not throw your agent into the deep end on day one. Build a curriculum that layers complexity: Week 1 Single facts about single entities Week 2 Relationships between entities Week 3 Temporal changes and before/after states Week 4 Conflicting information that must be reconciled Week 5 Multi-entity, multistep scenarios closer to production reality

### Moving Beyond Traditional Training

- the future of memory in agentic systems is not about inventing ever-smarter policies in configuration files. It is about building environments where agents *must* learn what to remember, what to forget, and how to evolve their internal understanding to succeed.
- a practical progression to start with: 1. Define clear task success metrics that matter for your application. 2. Introduce explicit memory constraints that force trade-offs. 3. Grow task complexity gradually with a curriculum. 4. Use masked training so each memory component gets proper feedback. 5. Allow strategies to emerge from experience rather than encoding them all up front.

## Future-Proofing Your Implementation


## Future-Proofing Your Implementation

- By now, you have the tools to design and operate a robust graph memory system with today’s requirements in mind. Future-proofing is about making sure those decisions do not trap you tomorrow
- Three themes in particular will shape how your memory architecture evolves: neurosymbolic reasoning, distributed scaling, and continual learning.

### Neurosymbolic Integration

