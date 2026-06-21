---
title: Agentic Design Patterns
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, foundations, tool-use, rag, planning, reflection]
confidence: high
source_files: 1
---

# Agentic Design Patterns

Every agent system you will ever encounter is built from four core patterns. Sometimes one pattern is enough. Sometimes you combine two or three. Occasionally all four appear in the same system.

This chapter teaches you each pattern with enough depth that you can recognize it in any architecture, implement a basic version, and know when it is the right choice.

---

## The Four Patterns

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   TOOL USE   │  │     RAG      │  │   PLANNING   │  │  REFLECTION  │
│              │  │              │  │              │  │              │
│ Agent calls  │  │ Agent looks  │  │ Agent breaks │  │ Agent checks │
│ external     │  │ up knowledge │  │ complex task │  │ its own work │
│ functions    │  │ before       │  │ into steps   │  │ before       │
│              │  │ answering    │  │ before acting│  │ returning it │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## Pattern 1: Tool Use

### Real-World Analogy

Like a handyman with a toolbox. A handyman knows which tool to grab for each job. Needs to hang a picture? Grab the hammer. Needs to drill a hole? Grab the drill. The handyman does not bring all tools to every job, but knows how to use each one.

An agent with tool use is similar. It has a set of tools available (search, calculator, send_email, run_code). When a task comes in, the agent decides which tool(s) to use and in what order.

### Why This Matters

An LLM by itself cannot check the weather, query a database, run code, or send an email. Tool use is what gives agents hands. Without tools, an agent is just a conversationalist.

### How It Works

The agent receives a request. It decides whether it can answer from its own knowledge or whether it needs to use a tool. If it needs a tool, it generates a structured tool call. The system executes the tool and returns the result. The agent uses the result to continue reasoning or produce its final answer.

---

## Stop and Think

Before looking at code, ask yourself: **How would you solve a complex problem without a computer?** You would probably use external sources — a calculator for math, a phone to call someone, a database to look up information. Tools are your agent's way of doing that.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks an agent "What is 847 × 392?"
>
> **INPUT:** "What is 847 × 392?"
>
> **Step 1:** Agent receives the question.
> **Step 2:** Agent thinks: "This is math. I should not guess — I have a calculator tool."
> **Step 3:** Agent creates a tool call: `{"tool": "calculator", "input": "847 * 392"}`
> **Step 4:** System executes the calculator → returns `331,824`
> **Step 5:** Agent receives the result and formats a response.
> **Step 6:** Agent decides: "I have the answer. No more tools needed."
>
> **OUTPUT:** "847 × 392 = 331,824"
>
> Without the tool, the LLM might have guessed the answer (and possibly gotten it wrong). With the tool, it's guaranteed correct.

Now let's see how this looks in code:

### Simple Function Version

Before diving into a class, let us see tool use as a simple function:

```python
def answer_with_tools(question):
    """Ask the LLM. If it needs a tool, use it. Repeat until done."""
    
    context = []
    
    for step in range(5):  # Max 5 tool calls
        # Ask the LLM what to do
        response = llm.generate(
            prompt=f"Question: {question}. Context so far: {context}."
        )
        
        # Check if it wants to use a tool
        if response.action == "final_answer":
            return response.content
        
        # Otherwise, use the tool
        tool_result = execute_tool(response.tool_name, response.tool_args)
        context.append(f"{response.tool_name}: {tool_result}")
    
    return "Could not answer within 5 tool calls."
```

**What this does:** Loops up to 5 times. Each time, asks the LLM "what do you want to do?" If it says "final answer," return. Otherwise, execute the tool it asked for and loop again.

### Class Version

Now, a full class with proper tool definitions and execution:

```python
# --- TOOL DEFINITION ---
# Each tool is a function with a clear schema that the LLM can understand.

tools = [
    {
        "name": "search_web",
        "description": "Search the web for current information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "num_results": {
                    "type": "integer",
                    "description": "Number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "run_sql",
        "description": "Execute a read-only SQL query against the analytics database",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email to a specified recipient",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    }
]


# --- TOOL USE AGENT ---

class ToolUseAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t["name"]: t for t in tools}
        self.tool_executors = {
            "search_web": self.execute_search,
            "run_sql": self.execute_sql,
            "send_email": self.execute_email,
        }
    
    def run(self, user_request):
        messages = [{"role": "user", "content": user_request}]
        
        for step in range(10):  # Max 10 tool calls
            response = self.llm.generate(
                system_prompt="""You are a helpful assistant with access to tools.
                When you need information you don't have, use a tool.
                When you have enough information, provide your final answer.
                
                Available tools: search_web, run_sql, send_email
                
                To use a tool, respond with:
                TOOL_CALL: {"name": "tool_name", "arguments": {...}}
                
                To give a final answer, respond with:
                FINAL_ANSWER: your answer here""",
                messages=messages,
                tools=list(self.tools.values())
            )
            
            if response.has_tool_call:
                # Extract the tool name and arguments
                tool_name = response.tool_call["name"]
                tool_args = response.tool_call["arguments"]
                
                print(f"  [Step {step+1}] Calling {tool_name}({tool_args})")
                
                # Execute the tool using the right executor function
                result = self.tool_executors[tool_name](**tool_args)
                
                # Add the tool result back to the conversation
                # This is the KEY: the LLM will see the result and decide next steps
                messages.append({"role": "assistant", "content": str(response)})
                messages.append({"role": "tool", "name": tool_name, "content": str(result)})
            else:
                # Agent decided it has enough info — return final answer
                return response.content
        
        return "Could not complete the task within the step limit."
    
    def execute_search(self, query, num_results=5):
        """Simulate a web search. In production, call a real search API."""
        print(f"    [Searching] {query}")
        return f"Search results for '{query}': [result 1, result 2, ...]"
    
    def execute_sql(self, query):
        """Simulate a database query. In production, call a real database."""
        print(f"    [SQL Query] {query}")
        return f"Query results: [row 1, row 2, ...]"
    
    def execute_email(self, to, subject, body):
        """Simulate sending an email. In production, call a real email service."""
        print(f"    [Email sent] to {to} with subject '{subject}'")
        return "Email sent successfully"
```

**Line-by-line breakdown of the main loop:**

- `for step in range(10):` — Loop up to 10 times (or until the task is done).
- `response = self.llm.generate(system_prompt=..., messages=messages, tools=list(self.tools.values()))` — Ask the LLM to decide what to do next. Pass the conversation history (messages) and the list of available tools.
- `if response.has_tool_call:` — Check if the LLM decided to use a tool.
- `tool_name = response.tool_call["name"]` — Extract the name of the tool (e.g., "search_web").
- `tool_args = response.tool_call["arguments"]` — Extract the arguments for the tool (e.g., {"query": "Python agents"}).
- `result = self.tool_executors[tool_name](**tool_args)` — Look up the executor function for this tool and run it with the arguments. The `**tool_args` unpacks the dictionary as keyword arguments.
- `messages.append({"role": "tool", "name": tool_name, "content": str(result)})` — Add the tool result to the message history. This is critical. The LLM sees this result and uses it to decide what to do next.
- `else: return response.content` — If the LLM did not want a tool call, it chose to return a final answer.

### Design Questions You Must Answer

1. **What tools does this agent need?** List every external capability. Be specific. "Search" is too vague — is it web search, internal doc search, or database search?

2. **What is the tool schema?** Every tool must have a name, description, and parameter schema. If the LLM does not understand what a tool does, it will misuse it.

3. **What happens when a tool fails?** Does the agent retry? Use a different tool? Give up and tell the user?

4. **Are there dangerous tools?** A `send_email` tool or `run_sql` tool can do real damage. Which tools need human approval before execution?

### Key Risks

- **Hallucinated tool calls:** The LLM invents a tool that does not exist, or passes wrong arguments. Mitigation: validate tool names and arguments before execution.
- **Tool misuse:** The agent calls a write tool when it should only read. Mitigation: separate read-only and write tools, add permission checks.
- **Infinite loops:** The agent keeps calling tools without making progress. Mitigation: step limits, and detect when the agent is repeating the same tool call.

---

## Pattern 2: RAG (Retrieval-Augmented Generation)

### Real-World Analogy

Like a student with an open-book exam. The student does not try to remember everything from class. Instead, they have their notes with them. When the teacher asks a question, the student looks up the relevant section in their notes, reads it, and uses that information to write the answer. The answer is grounded in evidence, not guesswork.

An agent with RAG does the same. Instead of relying only on the LLM's training data, it looks up relevant information from a knowledge base before generating its answer.

### Why This Matters

LLMs have knowledge cutoff dates. They do not know your company's internal docs, your product specs, or your policies. RAG solves this by giving the agent access to your knowledge at query time.

---

## Stop and Think

Before looking at code, imagine this scenario: **You are building a customer support bot for a company. The company just changed its return policy yesterday.** The LLM's training data is from 6 months ago, so it does not know about the new policy. How would you make sure your bot gives the right answer?

That is RAG. You retrieve the current policy from your database and show it to the LLM before it answers.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A customer asks "What is your refund policy for damaged items?"
> The agent has access to a knowledge base with 10,000 document chunks.
>
> **INPUT:** "What is your refund policy for damaged items?"
>
> **Step 1 (Embed the query):** Convert the question into numbers (a vector): `[0.12, -0.34, 0.78, ...]`
> **Step 2 (Search):** Compare this vector against all 10,000 stored chunks.
> **Step 3 (Retrieve top matches):**
>   - Chunk 14 from `policy_doc.md` (score: 0.92): *"Damaged items may be returned within 30 days..."*
>   - Chunk 15 from `policy_doc.md` (score: 0.87): *"Refunds are processed within 5 business days..."*
>   - Chunk 3 from `faq.md` (score: 0.71): *"For damaged items, please include photos..."*
> **Step 4 (Rerank):** A more precise model re-scores them → new order: chunk 14, chunk 3, chunk 15
> **Step 5 (Generate):** Send the top chunks + question to the LLM:
>   *"Using ONLY this context, answer the question..."*
> **Step 6 (Cite sources):** LLM includes references to where it found the information.
>
> **OUTPUT:** "Our refund policy for damaged items: you can return within 30 days. Please include photos of the damage. Refunds are processed within 5 business days. [Sources: policy_doc.md p.14, faq.md p.3]"
>
> Without RAG, the LLM would guess based on its training data (which might be outdated or wrong). With RAG, it answers based on YOUR actual documents.

Now let's look at how this pipeline works:

### RAG in Visual Form

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User Query  │────▶│   Retriever  │────▶│  LLM Agent   │
└──────────────┘     │              │     │              │
                     │ 1. Embed     │     │ Uses chunks  │
                     │    query     │     │ as evidence  │
                     │ 2. Search    │     │ to answer    │
                     │    vectors   │     │              │
                     │ 3. Rerank    │     │ Cites sources│
                     │ 4. Return    │     │              │
                     │    top-k     │     │              │
                     └──────────────┘     └──────────────┘
                            │
                     ┌──────┴──────┐
                     │ Vector DB   │
                     │             │
                     │ Chunked &   │
                     │ embedded    │
                     │ documents   │
                     └─────────────┘
```

The retriever is like a search engine for your knowledge base.

### The Full RAG Pipeline

RAG has multiple steps. It happens in two phases:

**Phase 1: Ingestion (one-time or on a schedule)**
- Get your documents
- Break them into chunks
- Convert chunks to embeddings (numerical vectors)
- Store in a vector database

**Phase 2: Query (every time a user asks a question)**
- Get the user's query
- Convert it to an embedding
- Search for similar chunks in the vector database
- Return the most relevant chunks to the LLM
- LLM reads the chunks and answers based on them

Let us code this step by step:

```python
# --- STEP 1: DOCUMENT INGESTION ---
# This happens ONCE (or on a schedule), not at query time.

class DocumentIngester:
    def __init__(self, embedding_model, vector_store):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
    
    def ingest(self, documents):
        for doc in documents:
            # Parse the document into text
            text = self.parse(doc)
            
            # Chunk the text into smaller pieces
            chunks = self.chunk(text, chunk_size=512, overlap=50)
            
            # Embed each chunk
            for chunk in chunks:
                embedding = self.embedding_model.embed(chunk.text)
                
                # Store chunk + embedding + metadata
                self.vector_store.upsert({
                    "id": chunk.id,
                    "text": chunk.text,
                    "embedding": embedding,
                    "metadata": {
                        "source": doc.filename,
                        "page": chunk.page_number,
                        "section": chunk.section_title,
                    }
                })
    
    def chunk(self, text, chunk_size=512, overlap=50):
        """
        Split text into overlapping chunks.
        
        This is a CRITICAL step. Let's understand why.
        
        Why chunk?
        - An embedding model can only handle ~500 words at a time.
        - If you embed a whole 100-page document, the embedding will be
          diluted. Important details get averaged out.
        - Chunking lets us embed the document in pieces, so each chunk's
          embedding captures its specific meaning.
        
        Why overlap?
        - Important information often spans chunk boundaries.
        - If a sentence is split between chunk 1 and chunk 2, the retriever
          might miss it.
        - A 50-token overlap ensures the retriever can find it.
        
        Chunk size trade-off:
        - Too small (100 tokens): Loses context. Agent gets fragments.
        - Too large (2000 tokens): Dilutes relevance. Retriever returns 
          chunks where only one sentence is relevant. The LLM has to wade
          through lots of noise.
        - Sweet spot: 300-800 tokens for most use cases.
        """
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_text = " ".join(words[i:i + chunk_size])
            chunks.append(Chunk(
                text=chunk_text,
                start_index=i,
                end_index=min(i + chunk_size, len(words))
            ))
        
        return chunks
```

**Understanding the chunk function line-by-line:**

- `words = text.split()` — Split the text into a list of words.
- `for i in range(0, len(words), chunk_size - overlap):` — Loop through the words in steps. Each step moves forward by (chunk_size - overlap). So if chunk_size=512 and overlap=50, we move forward 462 words each iteration. This creates 50-word overlaps between chunks.
- `chunk_text = " ".join(words[i:i + chunk_size])` — Take a slice of words from position `i` to `i + chunk_size` and join them back into text.
- `chunks.append(Chunk(...))` — Create a Chunk object and add it to the list.

---

### Now the Retrieval Step

```python
# --- STEP 2: RETRIEVAL AT QUERY TIME ---

class Retriever:
    def __init__(self, embedding_model, vector_store, reranker=None):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.reranker = reranker
    
    def retrieve(self, query, top_k=5):
        # Dense retrieval: embed the query, find similar chunks
        query_embedding = self.embedding_model.embed(query)
        candidates = self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k * 3  # Retrieve more than needed for reranking
        )
        
        # Optional: Sparse retrieval (BM25/keyword matching)
        # Hybrid = dense + sparse, then merge results
        sparse_candidates = self.vector_store.bm25_search(query, top_k=top_k * 3)
        candidates = self.merge_results(candidates, sparse_candidates)
        
        # Rerank: use a cross-encoder to re-score candidates
        if self.reranker:
            candidates = self.reranker.rerank(query, candidates)
        
        return candidates[:top_k]
    
    def merge_results(self, dense_results, sparse_results):
        """
        Reciprocal Rank Fusion: combine rankings from dense 
        and sparse retrieval.
        
        Why hybrid?
        - Dense retrieval (embeddings) catches semantic similarity. 
          "automobile" matches "car" because the embeddings are similar.
        - Sparse retrieval (BM25) catches exact terms. 
          "PLC-7520" matches "PLC-7520" exactly. It's not semantically 
          similar, it's literally the same product code.
        - Together they cover both cases: semantic matches and exact matches.
        
        How Reciprocal Rank Fusion works:
        - Each retrieval method ranks the results (best to worst).
        - We combine the ranks. A document ranked 1st by dense and 3rd by 
          sparse gets a high combined score.
        - Documents that both methods agree on (high in both rankings) rank 
          highest.
        """
        scores = {}
        k = 60  # Fusion constant (standard value)
        
        # Add scores from dense retrieval
        for rank, doc in enumerate(dense_results):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank)
        
        # Add scores from sparse retrieval
        for rank, doc in enumerate(sparse_results):
            scores[doc.id] = scores.get(doc.id, 0) + 1 / (k + rank)
        
        # Sort by combined score
        all_docs = {d.id: d for d in dense_results + sparse_results}
        sorted_ids = sorted(scores, key=scores.get, reverse=True)
        return [all_docs[doc_id] for doc_id in sorted_ids]
```

**Line-by-line breakdown of retrieve:**

- `query_embedding = self.embedding_model.embed(query)` — Convert the user's query to an embedding vector. This is the same kind of vector as the chunks.
- `candidates = self.vector_store.search(embedding=query_embedding, top_k=top_k * 3)` — Find the chunks most similar to the query. Retrieve 3x more than needed (e.g., 15 instead of 5) so we can rerank and filter.
- `sparse_candidates = self.vector_store.bm25_search(query, top_k=top_k * 3)` — Do a keyword search as well. This catches exact matches that embeddings might miss.
- `candidates = self.merge_results(candidates, sparse_candidates)` — Combine the two rankings.
- `if self.reranker: candidates = self.reranker.rerank(query, candidates)` — If we have a reranker, use it to re-score the candidates. A reranker is often a more powerful model that takes both the query and candidate text and gives a relevance score. It is slower but more accurate than embeddings.

---

### The RAG Agent

Now, here is the agent that uses retrieval:

```python
# --- STEP 3: RAG AGENT ---

class RAGAgent:
    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever
    
    def run(self, user_question):
        # Retrieve relevant chunks
        chunks = self.retriever.retrieve(user_question, top_k=5)
        
        # Build the context from retrieved chunks
        context = "\n\n---\n\n".join([
            f"[Source: {c.metadata['source']}, Page {c.metadata['page']}]\n{c.text}"
            for c in chunks
        ])
        
        # Generate answer grounded in retrieved evidence
        answer = self.llm.generate(
            system_prompt="""Answer the user's question using ONLY the 
            provided context. If the context does not contain enough 
            information to answer, say so explicitly.
            
            Rules:
            1. Cite your sources using [Source: filename, Page X] format
            2. Do not make up information not in the context
            3. If you are uncertain, say "Based on the available documents, 
               I'm not confident in this answer"
            4. Prefer direct quotes over paraphrasing when precision matters""",
            messages=[
                {"role": "system", "content": f"Context:\n{context}"},
                {"role": "user", "content": user_question}
            ]
        )
        
        return {
            "answer": answer,
            "sources": [c.metadata for c in chunks],
            "retrieval_scores": [c.score for c in chunks]
        }
```

**Line-by-line breakdown:**

- `chunks = self.retriever.retrieve(user_question, top_k=5)` — Retrieve the top 5 most relevant chunks.
- `context = "\n\n---\n\n".join([...])` — Combine all the retrieved chunks into one big text block. Separate them with `---` so the LLM knows where one chunk ends and another begins.
- `self.llm.generate(system_prompt=..., messages=...)` — Ask the LLM to answer the question using ONLY the retrieved context. The system prompt is strict: "do not make up information."
- `return {"answer": answer, "sources": [c.metadata for c in chunks], ...}` — Return the answer plus metadata about which documents were used. This is important for transparency and debugging.

---

## Stop and Think Again

At this point, you should ask yourself: **What would happen if the retriever returned the wrong chunks?**

The answer: The LLM would not be able to answer correctly, even though it is smart. Garbage in, garbage out.

This is why retrieval quality is critical. A perfect LLM with bad retrieval is useless. A mediocre LLM with good retrieval can be very useful.

---

### Standard RAG vs. Agentic RAG

**Standard RAG** always retrieves before answering. The flow is rigid: retrieve → generate.

**Agentic RAG** lets the agent **decide** when to retrieve, what query to use, and whether to retrieve again if the first results are not good enough.

```python
class AgenticRAG:
    """
    The agent decides when and what to retrieve.
    It can reformulate queries, retrieve multiple times,
    and combine results before answering.
    """
    
    def run(self, user_question):
        messages = [{"role": "user", "content": user_question}]
        
        for step in range(5):
            response = self.llm.generate(
                system_prompt="""You have access to a knowledge base retrieval tool.
                
                You can:
                1. RETRIEVE: {"query": "your search query"} — search the knowledge base
                2. ANSWER: {"answer": "your answer", "confidence": "high/medium/low"}
                
                Strategy:
                - First, think about what information you need
                - Retrieve relevant documents
                - If the results are insufficient, try a different query
                - Only answer when you have enough evidence
                - If after 3 retrievals you still can't answer, say so""",
                messages=messages
            )
            
            if response.action == "RETRIEVE":
                chunks = self.retriever.retrieve(response.query)
                messages.append({"role": "tool", "content": self.format_chunks(chunks)})
            
            elif response.action == "ANSWER":
                return response.answer
```

**Key difference:** In standard RAG, the system decides what to retrieve. In agentic RAG, the LLM decides. It can try multiple queries if the first one did not work.

### When RAG Is Not Enough

RAG breaks down when:
- The answer requires reasoning across 5+ documents (multi-hop reasoning)
- The knowledge base is poorly structured or has conflicting information
- The question requires real-time computation, not just lookup
- The user needs an action taken, not just information retrieved

When RAG breaks down, you need planning (Pattern 3) or a multi-agent system.

---

## Pattern 3: Planning

### Real-World Analogy

Like a project manager who writes a to-do list before starting work. The manager does not just start working randomly. First, they break the big goal into smaller tasks, figure out the order (task B depends on task A), assign resources, and identify risks. Then they execute the plan step by step, checking progress and replanning if something goes wrong.

An agent with planning does the same. It breaks a complex goal into a structured plan before executing any actions.

### Why This Matters

Without planning, an agent with 10 tools will trial-and-error its way through a task. "Maybe I should search? No, maybe I should call the database?" It wastes time and tokens.

With planning, it creates a roadmap, assigns each step the right tool, and can detect when it is off track.

---

## Stop and Think

Imagine you want to book a trip to Paris. Without planning, you might: search for flights, then search for hotels, then search for attractions, then realize you already booked a hotel on a day you want to do a tour. Inefficient. With planning, you would: (1) decide dates, (2) find flights that fit the dates, (3) find hotels near the sites you want to visit, (4) book everything in the right order. Much better.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "Write a research report on electric vehicles."
>
> **INPUT:** "Write a research report on electric vehicles"
>
> **Phase 1 — PLAN (before doing any work):**
> Agent creates a step-by-step plan:
>   - Step 1: Search for EV market size data (tool: search_web)
>   - Step 2: Search for major EV companies (tool: search_web)
>   - Step 3: Search for EV technology trends (tool: search_web)
>   - Step 4: Write introduction (tool: llm — uses data from steps 1-3)
>   - Step 5: Write body sections (tool: llm)
>   - Step 6: Write conclusion (tool: llm)
>
> **Phase 2 — EXECUTE:**
> Step 1 → search_web("EV market size 2024") → returns "$500B market by 2025"  ✓
> Step 2 → search_web("largest EV companies") → returns "Tesla, BYD, VW..." ✓
> Step 3 → search_web("EV technology trends") → returns "solid-state batteries, fast charging..." ✓
> Step 4 → LLM writes intro using data from steps 1-3 ✓
> Step 5 → LLM writes body sections ✓
> Step 6 → LLM writes conclusion ✓
>
> **Phase 3 — VALIDATE:**
> Agent checks each step's output. All passed.
>
> **What if Step 2 had failed?** (Search returned no results)
> → Agent REPLANS: "Use a different query" or "Try a database tool instead"
> → New plan replaces the remaining steps
> → Execution continues from the new plan
>
> **OUTPUT:** Complete 3-page research report with market data, company analysis, and tech trends.

Now let's see how this looks in code:

### How Planning Works

```python
class PlanningAgent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = tools
    
    def run(self, goal):
        # --- PHASE 1: PLAN ---
        plan = self.create_plan(goal)
        print(f"Plan created with {len(plan)} steps")
        
        results = {}
        
        # --- PHASE 2: EXECUTE ---
        for i, step in enumerate(plan):
            print(f"\n--- Step {i+1}: {step['description']} ---")
            
            # Execute the step
            result = self.execute_step(step, results)
            results[step["id"]] = result
            
            # --- PHASE 3: VALIDATE ---
            is_valid = self.validate_step(step, result)
            
            if not is_valid:
                # --- PHASE 4: REPLAN ---
                print(f"Step {i+1} failed validation. Replanning...")
                remaining_plan = self.replan(goal, plan[i+1:], results)
                plan = plan[:i+1] + remaining_plan
        
        # --- PHASE 5: SYNTHESIZE ---
        return self.synthesize(goal, results)
    
    def create_plan(self, goal):
        """
        Ask the LLM to decompose the goal into steps.
        Each step has: id, description, tool, dependencies, expected_output.
        """
        plan_json = self.llm.generate(
            prompt=f"""Create a step-by-step plan to achieve this goal:
            
            Goal: {goal}
            
            Available tools: {[t["name"] for t in self.tools]}
            
            Return a JSON list where each step has:
            - "id": unique step identifier (e.g., "step_1")
            - "description": what this step does
            - "tool": which tool to use (or "llm" for reasoning steps)
            - "arguments": arguments for the tool
            - "depends_on": list of step IDs this step needs completed first
            - "expected_output": what a successful result looks like
            
            Rules:
            1. Break complex tasks into atomic steps
            2. Each step should do ONE thing
            3. Order steps so dependencies are satisfied
            4. Include a final synthesis step"""
        )
        return json.loads(plan_json)
    
    def execute_step(self, step, previous_results):
        """Execute a single step."""
        tool = self.tools[step["tool"]]
        return tool.execute(**step["arguments"])
    
    def validate_step(self, step, result):
        """Check if the result matches the expected output."""
        # In production, this could call a separate validator agent
        return result.success
    
    def replan(self, goal, remaining_steps, completed_results):
        """
        When a step fails, create a new plan from the current state.
        
        This is what makes planning AGENTIC — the plan adapts to reality.
        A static plan just fails. An agentic plan re-routes.
        """
        revised = self.llm.generate(
            prompt=f"""The original goal: {goal}
            
            Work completed so far: {json.dumps(completed_results)}
            
            The remaining steps were: {json.dumps(remaining_steps)}
            But the previous step failed or produced unexpected results.
            
            Create a REVISED plan for the remaining work.
            Take into account what has already been accomplished."""
        )
        return json.loads(revised)
    
    def synthesize(self, goal, results):
        """Combine all results into a final answer."""
        return self.llm.generate(
            prompt=f"""Goal: {goal}
            
            Work completed:
            {json.dumps(results)}
            
            Synthesize all the results above into a final answer."""
        )
```

**Line-by-line breakdown of the main loop:**

- `plan = self.create_plan(goal)` — Ask the LLM to break the goal into steps.
- `for i, step in enumerate(plan):` — Loop through each step.
- `result = self.execute_step(step, results)` — Execute the step using the right tool.
- `results[step["id"]] = result` — Store the result so later steps can use it.
- `is_valid = self.validate_step(step, result)` — Check if the result is good.
- `if not is_valid: remaining_plan = self.replan(...)` — If invalid, ask the LLM to create a new plan from the current state.
- `plan = plan[:i+1] + remaining_plan` — Replace the remaining steps with the new plan.

### Plan Formats

Plans can be structured in different ways depending on the complexity:

```python
# SIMPLE: Linear list of steps
linear_plan = [
    {"step": 1, "action": "search for market data"},
    {"step": 2, "action": "analyze trends"},
    {"step": 3, "action": "write report"}
]

# MEDIUM: Steps with dependencies (DAG)
dag_plan = [
    {"id": "a", "action": "fetch stock prices", "depends_on": []},
    {"id": "b", "action": "fetch news articles", "depends_on": []},
    {"id": "c", "action": "correlate prices with news", "depends_on": ["a", "b"]},
    {"id": "d", "action": "generate insights", "depends_on": ["c"]}
]
# Steps a and b can run in parallel. Step c waits for both.

# COMPLEX: Hierarchical plan with sub-plans
hierarchical_plan = {
    "goal": "Complete quarterly review",
    "phases": [
        {
            "phase": "data_collection",
            "steps": [
                {"action": "pull revenue data", "agent": "data_agent"},
                {"action": "pull customer metrics", "agent": "data_agent"},
            ]
        },
        {
            "phase": "analysis",
            "steps": [
                {"action": "revenue trend analysis", "agent": "finance_agent"},
                {"action": "customer health scoring", "agent": "customer_agent"},
            ]
        },
        {
            "phase": "reporting",
            "steps": [
                {"action": "synthesize findings", "agent": "report_agent"}
            ]
        }
    ]
}
```

---

## Pattern 4: Reflection / Self-Critique

### Real-World Analogy

Like a writer who writes a draft, reads it over, notices mistakes, and rewrites it. The writer does not submit the first draft. They review their own work, ask "Is this clear? Is it accurate? Is anything missing?" and improve it before submitting.

An agent with reflection does the same. It generates a response, then a "critic" (another LLM) evaluates it and the agent revises based on the feedback.

### Why This Matters

LLMs are confident even when wrong. Reflection adds a quality check. The agent catches its own errors, improves its answers, and knows when it is not confident enough.

---

## Stop and Think

Imagine you asked an LLM to write code to calculate the Fibonacci sequence. The LLM writes some code. It looks smart and runs without errors. But does it actually work correctly? Without a reflection step, you would not know. With reflection, a critic could test the code or review it, and ask the LLM to fix any bugs.

---

### 🔄 What Happens When This Runs

> **Imagine this scenario:** A user asks "Write a Python function to check if a number is prime."
>
> **INPUT:** "Write a Python function to check if a number is prime"
>
> **Step 1 (Generate first draft):**
> Generator LLM writes:
> ```python
> def is_prime(n):
>     for i in range(2, n):
>         if n % i == 0:
>             return False
>     return True
> ```
>
> **Step 2 (Critic reviews the draft):**
> Critic LLM evaluates:
>   - "Does it handle n=0? → No, returns True (BUG)"
>   - "Does it handle n=1? → Returns True (BUG — 1 is not prime)"
>   - "Is it efficient? → No, checks all numbers up to n. Could stop at √n"
>   - Score: 4/10 → NOT APPROVED
>
> **Step 3 (Revise based on feedback):**
> Generator reads the critique and rewrites:
> ```python
> def is_prime(n):
>     if n < 2:
>         return False
>     for i in range(2, int(n**0.5) + 1):
>         if n % i == 0:
>             return False
>     return True
> ```
>
> **Step 4 (Critic reviews again):**
>   - "Handles edge cases? → Yes ✓"
>   - "Efficient? → Yes, stops at √n ✓"
>   - "Correct? → Yes ✓"
>   - Score: 9/10 → **APPROVED**
>
> **OUTPUT:** The improved, bug-free function (after 1 revision).
>
> Without reflection, the user would have received the buggy first draft. With reflection, the agent caught its own mistakes.

Now let's see how this looks in code:

### How Reflection Works

```python
class ReflectionAgent:
    def __init__(self, generator_llm, critic_llm):
        self.generator = generator_llm
        self.critic = critic_llm
    
    def run(self, task, max_revisions=3):
        # Step 1: Generate initial response
        draft = self.generator.generate(
            prompt=f"Complete this task:\n{task}"
        )
        
        for revision in range(max_revisions):
            # Step 2: Critique the response
            critique = self.critic.generate(
                prompt=f"""Review this response for quality, accuracy, and completeness.
                
                Task: {task}
                Response: {draft}
                
                Provide specific feedback:
                1. What is correct and should be kept?
                2. What is wrong or inaccurate?
                3. What is missing?
                4. Overall quality score (1-10)
                
                If the score is 8 or above, say "APPROVED".
                Otherwise, provide specific revision instructions."""
            )
            
            # Step 3: Check if approved
            if "APPROVED" in critique:
                print(f"Approved after {revision} revision(s)")
                return draft
            
            # Step 4: Revise based on critique
            draft = self.generator.generate(
                prompt=f"""Revise your response based on this feedback.
                
                Original task: {task}
                Your previous response: {draft}
                Feedback: {critique}
                
                Address every point in the feedback. 
                Keep what was correct. Fix what was wrong. Add what was missing."""
            )
        
        return draft  # Return best effort after max revisions
```

**Line-by-line breakdown:**

- `draft = self.generator.generate(prompt=f"Complete this task:\n{task}")` — Generate the initial response.
- `for revision in range(max_revisions):` — Loop up to 3 times (or however many revisions).
- `critique = self.critic.generate(prompt=...)` — Ask the critic to evaluate the response.
- `if "APPROVED" in critique:` — Check if the critic approved the response (score 8+).
- `return draft` — If approved, return it. No more revisions needed.
- `draft = self.generator.generate(prompt=f"Revise your response based on...")` — Ask the generator to revise based on the feedback.

### Reflection Variations

```python
# VARIATION 1: Self-reflection (same model critiques itself)
# Cheaper but less effective — the model may not catch its own blind spots
critique = same_llm.generate(
    prompt=f"Review your own response and identify 3 potential issues: {response}"
)

# VARIATION 2: Cross-model reflection (different model critiques)
# More expensive but catches more errors — different models have different biases
critique = critic_model.generate(  # e.g., use Claude to critique GPT-4's output
    prompt=f"Review this response for accuracy: {response}"
)

# VARIATION 3: Tool-grounded reflection (verify against external sources)
# Most reliable — uses real data to check claims
critique = self.verify_claims(response)  # Checks each claim against a database

# VARIATION 4: Multi-aspect reflection (separate critics for different dimensions)
factual_critique = fact_checker.generate(f"Check facts in: {response}")
tone_critique = tone_checker.generate(f"Check tone and clarity: {response}")
compliance_critique = compliance_checker.generate(f"Check regulatory compliance: {response}")
```

### When Reflection Helps Most

- Tasks where accuracy is critical (legal, medical, financial)
- Long-form generation where errors compound
- Code generation (the critic can actually run the code)
- Any task where a wrong output is worse than a slow output

### When Reflection Hurts

- Real-time applications where latency matters (each reflection pass = another LLM call)
- Simple factual lookups (the answer is either right or wrong, no nuance to improve)
- When the critic is not actually better at judging than the generator (both are wrong in the same way)

---

## Combining Patterns

In practice, production systems combine multiple patterns. Here is a common combination:

```
RAG + Tool Use + Reflection

User asks a question
    → Agent retrieves documents (RAG)
    → Agent calls a calculator tool to verify numbers (Tool Use)  
    → Agent generates a response
    → Critic agent checks response against retrieved docs (Reflection)
    → Final answer returned
```

```python
class CombinedAgent:
    """
    A production-ready agent that combines RAG, tool use, and reflection.
    This is closer to what real systems look like.
    """
    
    def __init__(self, llm, retriever, tools, critic_llm):
        self.agent = ToolUseAgent(llm, tools)
        self.retriever = retriever
        self.critic = critic_llm
    
    def run(self, question):
        # Pattern 2: RAG — retrieve relevant context
        chunks = self.retriever.retrieve(question)
        context = "\n\n".join([c.text for c in chunks])
        
        # Pattern 1: Tool Use — agent decides if it needs additional tools
        response = self.agent.run(f"Context:\n{context}\n\nQuestion: {question}")
        
        # Pattern 4: Reflection — critique the response
        critique = self.critic.generate(
            prompt=f"""Evaluate this response.
            Question: {question}
            Retrieved context: {context}
            Response: {response}
            
            Is the response accurate and well-grounded? Score 1-10."""
        )
        
        score = int(critique.split("Score:")[-1].strip()[0])
        
        if score < 7:
            # Revise and try again
            response = self.agent.run(
                f"Context:\n{context}\n\nQuestion: {question}\n\nPrevious response was criticized as: {critique}\n\nPlease revise."
            )
        
        return response
```

---

## In Production, This Looks Like

**For a Tool Use Agent:**

```
my-tool-agent/
├── agents/
│   ├── tool_use_agent.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── calculator.py
│   │   ├── email.py
│   │   └── database.py
│   └── schemas/
│       └── tool_schemas.json   # Tool definitions
├── main.py
└── requirements.txt
```

**For a RAG Agent:**

```
my-rag-agent/
├── agents/
│   └── rag_agent.py
├── retrieval/
│   ├── ingester.py            # Chunk and embed documents
│   ├── retriever.py           # Retrieve at query time
│   ├── reranker.py            # Optional: rerank results
│   └── embeddings.py          # Embedding model wrapper
├── storage/
│   ├── vector_store.py        # Interface to vector DB
│   └── documents/             # Raw documents to ingest
├── config/
│   ├── chunk_config.yaml      # Chunk size, overlap
│   └── retrieval_config.yaml  # Top-k, reranker settings
├── main.py
└── requirements.txt
```

Key principle: **Chunking strategy is config, not code.** If you hardcode chunk_size=512, changing it later requires code changes. Instead, define it in a config file.

---

## Pattern Selection Guide

Use this to decide which pattern(s) your system needs:

```python
def select_patterns(task):
    patterns = []
    
    if task.needs_external_data or task.needs_private_knowledge:
        patterns.append("RAG")
    
    if task.needs_to_call_apis or task.needs_to_run_code or task.needs_to_write:
        patterns.append("TOOL_USE")
    
    if task.has_multiple_steps or task.is_complex:
        patterns.append("PLANNING")
    
    if task.accuracy_is_critical or task.output_is_long_form:
        patterns.append("REFLECTION")
    
    return patterns

# Examples:
# "Answer questions about our product docs" → [RAG]
# "Book a flight and hotel for my trip"     → [TOOL_USE, PLANNING]
# "Write a legal brief for this case"       → [RAG, REFLECTION]
# "Analyze this quarter's financials"       → [RAG, TOOL_USE, PLANNING, REFLECTION]
```

---

## Developing Your AI Capability

This section is about understanding what AI can do for you now, and what you must learn yourself.

### What AI Can Help You With At This Stage

- **Design tool schemas.** Ask an LLM: "I want my agent to use a database tool. What should the schema look like?"
- **Write chunking functions.** Ask: "Write a function that chunks text with a 512-token size and 50-token overlap."
- **Draft system prompts.** Ask: "Write a system prompt for a RAG agent that should cite sources."
- **Debug retrieval.** Ask: "My RAG agent keeps returning irrelevant chunks. Why might that happen?"
- **Review your architecture sketches.** Ask an LLM to critique your design.

### What YOU Must Understand Yourself

- **Why RAG works.** Not just how to implement it, but WHY we use retrieval. "Because the LLM might not know the information" is the answer, but do you understand the deeper reason? (Retrieval grounds answers in evidence, prevents hallucination, handles knowledge cutoff.)
- **When retrieval beats the LLM's own knowledge.** You should know: "I would use RAG if the answer requires information that was created after the LLM's knowledge cutoff, or if the information is private/internal."
- **What happens when retrieval fails.** If the retriever returns wrong chunks, the agent cannot fix it. Understanding this helps you design better chunking and retrieval strategies.
- **Tool design trade-offs.** Why have one generic "run_code" tool vs. separate "run_python" and "run_sql" tools? (Specificity. The LLM knows exactly what each tool does.)
- **Why planning is different from just looping tool calls.** A planning agent explicitly reasons about the sequence of steps before executing. A tool-use agent just loops and tries things. Planning is more efficient.

### The LLM Fallacy Check: Chunking Edition

Here is a critical question you should be able to answer:

**Why do we chunk documents instead of feeding the whole document to the LLM?**

Try to answer this in your own words before reading below.

**The real answer:** 

Embeddings have a limit on context length (typically 512 tokens). A 100-page document would be chunked into ~40 chunks. Each chunk gets its own embedding, which captures the meaning of that chunk specifically. When the user asks a question, we search for the chunks whose embeddings are most similar to the question's embedding. This retrieves the relevant 2-3 chunks out of the 40.

Then we pass those 2-3 chunks to the LLM. The LLM has enough space to read them carefully and reason about them.

If instead we passed the whole 100-page document to the LLM:
- We would exceed the LLM's context window (unless it is a super-expensive, long-context model).
- Even if we fit it, the LLM would have to search through 100 pages for the relevant parts. This is noisy and wastes LLM reasoning on irrelevant content.

**Can you explain this back?** If not, read it again and ask an LLM to explain it differently.

---

## Exercises: Practice Your Understanding

Try these exercises. Use AI to help verify your work, but do the thinking yourself first.

**Exercise 1: Design a tool schema**

You are building an agent that needs to query a SQL database. Design the tool schema:

```python
{
    "name": "query_database",
    "description": "???",
    "parameters": {
        "type": "object",
        "properties": {
            # What parameters should this tool take?
        },
        "required": [???]
    }
}
```

Think about:
- What should the description say so the LLM knows how to use this tool?
- What parameters are required? Optional?
- What constraints should we put in the description (e.g., "read-only", "SELECT queries only")?

Now ask an LLM to review your design. Did they suggest anything you missed?

**Exercise 2: Chunk and retrieve manually**

Take a short article (2-3 paragraphs). Manually chunk it:

1. Split it into chunks of roughly 50 words each.
2. Add a 10-word overlap between chunks.
3. Now, ask a question about the article.
4. Which chunks would you retrieve (manually search) to answer that question?

Write your answer down. Then ask an LLM to read the article and chunks, and tell you which chunks it would retrieve. Did you get the same ones? Why or why not?

**Exercise 3: Pattern selection**

For each of these tasks, decide which pattern(s) you would use:

1. "Answer frequently asked questions about our company's benefits."
2. "Book me a flight, hotel, and rental car for next weekend."
3. "Summarize my emails from the past week."
4. "Generate a legal contract based on my templates and requirements."
5. "Monitor my AWS account and alert me if I'm approaching the spending limit."

For each, write: "I would use [PATTERNS] because [REASON]."

Now ask an LLM to review your answers. Did you miss any patterns? Would a different pattern have been better?

---

## What You Should Be Able to Do Now

After reading this chapter, you should be able to:

1. Describe all 4 agentic design patterns and give an example of each
2. Implement a basic tool-use agent with a tool schema
3. Explain the full RAG pipeline (ingest → chunk → embed → retrieve → rerank → generate)
4. Understand why we chunk (context limits on embeddings and LLMs)
5. Know the difference between standard RAG and agentic RAG
6. Implement a planning agent with replanning on failure
7. Implement a reflection loop with a critic
8. Decide which patterns to combine for a given problem
9. Understand the tradeoffs: more patterns = more power but more cost and latency

---

Next: [Multi-Agent Orchestration Patterns →](./03-multi-agent-orchestration.md)
