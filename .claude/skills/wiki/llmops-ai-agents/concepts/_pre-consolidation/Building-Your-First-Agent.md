---
title: Building Your First Agent
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, first-agent, rag, evals, guardrails, hands-on]
confidence: high
source_files: 3
---

# Building Your First Agent

> Consolidated from 3 source files.

---

## Designing Your First Agent

## Start With the Job, Not the Framework

The biggest mistake engineers make when building their first agent is picking a framework first and shoehorning a problem into it. You see LangChain docs, or you hear about ReAct or tool-calling, and you think "I should build that." Then you end up with a system that's over-engineered, fragile, and solves the wrong problem.

Start here instead: **What is the job the user is actually asking the agent to do?**

The job is not "use Claude to answer questions." The job is something specific: "Help course students understand LLMOps case studies without having to re-read the entire textbook" or "Route support tickets to the right team" or "Execute database migrations safely." Everything else — the architecture, the tools, the guardrails, the evals — flows from that.

## Step 1: Define the Job To Be Done (JTBD)

Write it in plain English. Be specific about:
- Who is using the agent?
- What are they trying to accomplish?
- What would success look like?
- What does failure cost them?

**Good JTBD:** "A student asks a question about how Uber's ML system handles driver pricing. The agent retrieves the relevant case study section, identifies that the question is about the pricing algorithm, and returns a concise answer with citations. The student doesn't have to search through 10 pages of text."

**Bad JTBD:** "Build an LLM agent that answers questions."

**Bad JTBD:** "Create a RAG system." (This is a technology choice, not a job.)

For this walkthrough, we'll use the **Course Q&A Agent**:

> Students in the LLMOps course have questions about specific topics covered in the case studies (Uber's ML system, DoorDash's dispatch algorithm, etc.). They want fast, accurate answers pulled directly from the course material, with citations so they can verify the answer. The agent should refuse to answer questions outside the course scope. Success is: relevant answer in under 3 seconds, with citations. Failure is: hallucinated answers, answers to out-of-scope questions, or inability to cite sources.

## Step 2: Define the Environment

What can your agent observe? What can it do? What is it forbidden from doing?

This is the real constraint surface. You'll write your agent code dozens of times. Your environment definition should almost never change.

For the Course Q&A Agent:

```
OBSERVATIONS:
- Student question (text, max 500 chars)
- Course material (markdown files, ~200KB total)
  - Uber case study: pricing, driver ML, surge dynamics
  - DoorDash case study: dispatch algorithm, ML ranking
  - Lyft case study: matching and supply prediction
- Query metadata (timestamp, student ID if available)

ACTIONS:
- Retrieve relevant sections from course material
- Rank/rerank retrieved sections
- Generate response text
- Emit citation (which page, which section)
- Return confidence score (0-1)

FORBIDDEN:
- No external API calls (we're not Googling)
- No making assumptions about real-time data
- No creative extrapolation beyond what's in the course
- No multi-turn stateful conversation (each query is independent)
- No tool use / function calling (first agent, keep it simple)
```

This is not a design spec yet. This is a constraint surface. It says: "Given these inputs and these capabilities, design an agent."

## Step 3: Choose the Agent Type

There are three main patterns for first agents:

### Pattern 1: Single-Agent RAG (What We're Building)
- Retrieves context from a fixed knowledge base
- Generates a response using that context
- No tool use, no planning, no looping
- Use when: knowledge base is relatively static and complete

### Pattern 2: Conversational Router
- Maintains conversation history
- Routes to different handlers based on intent
- Each handler is specialized (like a fallback tree)
- Use when: you need multi-turn state and different response modes

### Pattern 3: Narrow Action Agent
- Can call 1-3 tools in sequence
- Sees the result of each tool call
- Makes a decision about the next step
- Use when: the job requires simple branching logic

For the Course Q&A Agent, **Pattern 1 (Single-Agent RAG)** is the right choice:
- The knowledge base is static (course material doesn't change)
- Each question is independent (no state across queries)
- We don't need planning or tool branching
- We need speed (retrieve + generate, done)

## Step 4: Architecture Sketch

Before writing code, draw it:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         COURSE Q&A AGENT                            │
└─────────────────────────────────────────────────────────────────────┘

                            STUDENT QUERY
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  INPUT VALIDATION    │
                    │  - Length check      │
                    │  - Toxicity filter   │
                    │  - Scope filter      │
                    └──────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  RETRIEVAL LAYER     │
                    │  - BM25 (sparse)     │
                    │  - Dense (embedding) │
                    │  - Hybrid RRF        │
                    │  - Top-K = 5         │
                    └──────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  RERANKING LAYER     │
                    │  - Cross-encoder     │
                    │  - Filter by score   │
                    │  - Keep top-2        │
                    └──────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  GENERATION LAYER    │
                    │  - System prompt     │
                    │  - Context + query   │
                    │  - Generate response │
                    └──────────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │  OUTPUT LAYER        │
                    │  - Citation check    │
                    │  - Confidence score  │
                    │  - Format response   │
                    └──────────────────────┘
                                 │
                                 ▼
                           RESPONSE + CITATIONS
```

Data flow:

```
Knowledge Base (Course Material)
    ├─ Split into chunks (256 tokens)
    ├─ Create dense embeddings (OpenAI text-embedding-3-small)
    ├─ Create sparse (BM25) index
    └─ Store in: {vector_db + BM25_index}
        
Query Pipeline:
    1. Sparse retrieval (BM25) → top-k=10 chunks
    2. Dense retrieval (vector sim) → top-k=10 chunks
    3. Reciprocal Rank Fusion → top-5 unique chunks
    4. Rerank with cross-encoder → top-2 chunks
    5. Inject into prompt context
    6. Generate response with Claude
    7. Extract citations from retrieved chunks
    8. Score confidence based on reranker scores
```

## Step 5: Define the Tool Schema

"Tools" in this context means the retriever interface. What does your agent ask the retriever for, and what does it get back?

```python
# What the agent needs to request
class RetrieverQuery:
    question: str          # The student's question
    top_k: int = 5        # How many chunks to return
    min_score: float = 0.3  # Confidence threshold

# What the retriever returns
class RetrievedChunk:
    content: str           # The actual text
    source: str            # Which case study (uber, doordash, lyft)
    section: str           # Which section within the case study
    relevance_score: float # 0-1, higher is more relevant
    chunk_id: str         # For linking back to source

class RetrieverResult:
    chunks: List[RetrievedChunk]
    query_embedding: np.ndarray  # For debugging
    retrieval_time_ms: float
    total_candidates: int  # How many chunks we scored

# What the agent generates
class AgentResponse:
    answer: str                      # The actual answer text
    citations: List[CitationRef]     # Sources
    confidence: float                # 0-1
    fallback_triggered: bool         # Did we hit "I don't know"?
    reasoning_trace: Dict[str, Any]  # For debugging
```

## Step 6: Define the Memory Strategy

For a single-query agent like the Course Q&A system, memory is simple:

- **No conversation history** (each query is independent)
- **No user context** (we don't remember past students)
- **No state** (no "currently helping with topic X")

But we DO want:
- **Trace logging** (what retrieval scored what)
- **Observation logging** (timestamps, query length, etc.)
- **Error logging** (when fallback triggered, why)

```python
class QueryTrace:
    query_id: str
    timestamp: datetime
    student_id: Optional[str]
    
    # Retrieval step
    retrieved_chunks: List[RetrievedChunk]
    retrieval_scores: Dict[str, float]  # chunk_id -> relevance score
    
    # Reranking step
    reranked_chunks: List[RetrievedChunk]
    reranking_scores: Dict[str, float]  # chunk_id -> reranker score
    
    # Generation step
    prompt_tokens: int
    completion_tokens: int
    model: str
    latency_ms: float
    
    # Output step
    response: str
    citations: List[CitationRef]
    confidence: float
    fallback_used: bool
    
    # Metadata
    input_length: int
    output_length: int
    total_latency_ms: float
```

Store this in a JSON log or database. Every single query. When something goes wrong, you replay it.

## Step 7: Define Failure Modes

What can go wrong? Write them down. Rank them by:
1. Likelihood (how often)
2. Cost (how bad when it happens)
3. Detectability (can we catch it?)

For the Course Q&A Agent:

| Failure Mode | Likelihood | Cost | Detectability | Example |
|---|---|---|---|---|
| Hallucinated answer | Low | Very High | Medium | Agent says "Uber uses algorithm X" but course doesn't mention it |
| Out-of-scope answer | Low | High | High | Student asks "What's Uber's real pricing?" and agent answers from web knowledge, not course |
| Missing citation | Medium | High | Very High | Agent answers correctly but can't cite the source |
| Empty retrieval | Low | Medium | Very High | No chunks match the query (student asked something not in course) |
| Slow retrieval | Low | Medium | Very High | Retrieval takes >2 seconds (probably BM25 index corrupt) |
| Wrong case study | Medium | Medium | High | Student asks about Uber, gets DoorDash answer |
| Broken chunk | Low | Medium | Very High | Retrieved text is corrupted, incomplete, or out of order |

**How to detect each:**
- Hallucination: LLM-as-judge + human spot-checks
- Out-of-scope: LLM-as-judge + input filtering
- Missing citation: Regex on output
- Empty retrieval: Log the query
- Slow retrieval: Latency tracking
- Wrong case study: Check chunk source against query intent
- Broken chunk: Validation during ingestion

## Step 8: Define the Evaluation Plan

You will measure your agent on three levels:

### Level 1: Component evals (does each piece work?)
- **Retriever recall:** "For queries we care about, does the correct chunk appear in top-5?"
- **Reranker accuracy:** "Does the cross-encoder rank the right chunk first?"
- **Generation quality:** "Is the response grammatically correct and complete?"

### Level 2: Unit evals (does each step produce sane output?)
- **Response has citation:** Every answer includes source reference
- **Citation is correct:** The cited section actually contains the content
- **Confidence reflects reality:** High-confidence answers are more accurate than low-confidence ones

### Level 3: End-to-end eval (does the whole thing work?)
- **Golden dataset:** 10-20 curated queries with known good answers
- **Accuracy:** Does agent output match expected answer?
- **Latency:** Under 3 seconds?
- **Cost:** Reasonable token usage?

We'll build all three in the next files. For now, just commit to doing them.

## Minimum Viable Agent Checklist

Before you write production code, you have everything on this list:

- [ ] JTBD written in one paragraph
- [ ] Environment defined (observations, actions, forbidden)
- [ ] Agent type chosen (and rationale)
- [ ] Architecture diagram (ASCII acceptable)
- [ ] Tool schema defined (input/output types)
- [ ] Memory strategy written (what we log, how we store it)
- [ ] Failure modes listed (likelihood, cost, detection method)
- [ ] Evaluation plan sketched (L1, L2, L3 evals)
- [ ] Golden dataset started (at least 5 example queries)
- [ ] Team agreement on definition of success (what does "working" mean?)

If you're missing any of these, you will rewrite the agent 3x. If you have all of these, you might only rewrite it once.

## Running Example: The Course Q&A Agent

Throughout the next two files, we build this agent from scratch. Here's what it looks like in action:

**Input:**
```
Student: "How does Uber's surge pricing work?"
```

**Agent thinks:**
```
1. Retrieve chunks about Uber pricing
2. Rerank to find most relevant
3. Inject into prompt: "Here's our course material on Uber pricing: [chunk]"
4. Generate response
5. Find citation: "See Uber case study, section 3.2"
6. Compute confidence: 0.92
```

**Output:**
```
Uber's surge pricing dynamically adjusts fares based on real-time supply and demand. 
When supply is low relative to demand, the multiplier increases, which incentivizes 
more drivers to come online. The algorithm updates every few minutes based on GPS data 
from active drivers and order volume in each region.

[Citation: Uber Case Study, Section 3.2: "Dynamic Pricing Strategy"]
[Confidence: 0.92]
```

**What We'll Build:**
1. **File 2:** The agent itself (retrieval → reranking → generation)
2. **File 3:** Evals and guardrails (making sure it doesn't hallucinate, goes out of scope, etc.)

The goal is not a perfect system. The goal is a system you understand completely, that you can debug when it breaks, and that you can iterate on based on real user feedback.

---

## Building a Simple RAG Agent

This file walks through every component of the Course Q&A Agent, from document ingestion to the full run loop. We'll show the actual code you'd write, with explanations of every design decision.

## Component 1: Document Ingestion

Your agent is only as good as the data you feed it. Garbage in, garbage out.

### Step 1.1: Load the Course Material

```python
import os
import re
from pathlib import Path
from typing import List, Tuple

class DocumentLoader:
    def __init__(self, docs_dir: str):
        """Load all markdown files from course materials directory."""
        self.docs_dir = Path(docs_dir)
        self.raw_documents: List[Tuple[str, str]] = []  # (filename, content)
    
    def load(self) -> None:
        """Load all .md files, preserving filename for citations."""
        for md_file in self.docs_dir.glob("**/*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                # Store filename relative to docs_dir for cleaner citations
                filename = md_file.relative_to(self.docs_dir)
                self.raw_documents.append((str(filename), content))
        
        if not self.raw_documents:
            raise ValueError(f"No markdown files found in {self.docs_dir}")
        
        print(f"Loaded {len(self.raw_documents)} documents")
    
    def get_raw_documents(self) -> List[Tuple[str, str]]:
        return self.raw_documents
```

### Step 1.2: Parse and Extract Structure

Before chunking, understand the document structure. This helps with citations later.

```python
from dataclasses import dataclass

@dataclass
class Section:
    """Represents a logical section of a document."""
    title: str
    level: int  # heading level (1-6)
    content: str
    source_file: str
    line_number: int

class MarkdownParser:
    @staticmethod
    def extract_sections(filename: str, content: str) -> List[Section]:
        """
        Extract sections from markdown based on heading hierarchy.
        Heading structure tells us what a "logical unit" is.
        """
        sections = []
        current_section = None
        lines = content.split("\n")
        
        for line_num, line in enumerate(lines, 1):
            # Match markdown headings: # Title, ## Subtitle, etc.
            match = re.match(r"^(#+)\s+(.+)$", line)
            
            if match:
                level = len(match.group(1))
                title = match.group(2)
                
                # Save previous section if it has content
                if current_section and current_section["content"].strip():
                    sections.append(Section(
                        title=current_section["title"],
                        level=current_section["level"],
                        content=current_section["content"],
                        source_file=filename,
                        line_number=current_section["line_number"]
                    ))
                
                # Start new section
                current_section = {
                    "title": title,
                    "level": level,
                    "content": "",
                    "line_number": line_num
                }
            else:
                if current_section:
                    current_section["content"] += line + "\n"
        
        # Don't forget the last section
        if current_section and current_section["content"].strip():
            sections.append(Section(
                title=current_section["title"],
                level=current_section["level"],
                content=current_section["content"],
                source_file=filename,
                line_number=current_section["line_number"]
            ))
        
        return sections
```

### Step 1.3: Chunking Strategy

This is critical. Chunk size affects everything downstream:
- **Too small** (50 tokens): Context is fragmented, retriever confused
- **Too large** (1000 tokens): Many irrelevant passages per chunk, generation includes noise
- **Right size** (256 tokens): Clear semantic boundaries, fits in context window with room for query

Why 256 tokens? It's roughly one paragraph. It's small enough that a retriever can distinguish "this chunk is relevant" vs "this isn't." It's large enough that you get complete thoughts.

```python
import tiktoken

class ChunkedDocument:
    def __init__(self, 
                 content: str, 
                 source_file: str,
                 section_title: str,
                 chunk_index: int,
                 metadata: dict = None):
        self.content = content
        self.source_file = source_file
        self.section_title = section_title
        self.chunk_index = chunk_index
        self.metadata = metadata or {}
        self.token_count = self._count_tokens()
    
    def _count_tokens(self) -> int:
        """Count tokens using OpenAI's tokenizer."""
        enc = tiktoken.encoding_for_model("gpt-4")
        return len(enc.encode(self.content))
    
    @property
    def chunk_id(self) -> str:
        """Unique identifier for this chunk."""
        return f"{self.source_file}#{self.section_title}#{self.chunk_index}"

class ChunkerByTokenCount:
    """
    Chunk by token count, not character count.
    Why? Because token count is what LLMs see.
    """
    
    def __init__(self, target_token_size: int = 256, overlap_tokens: int = 32):
        self.target_token_size = target_token_size
        self.overlap_tokens = overlap_tokens
        self.enc = tiktoken.encoding_for_model("gpt-4")
    
    def chunk_section(self, 
                      section: Section) -> List[ChunkedDocument]:
        """
        Chunk a section into target-sized pieces.
        Overlap ensures concepts at boundaries aren't lost.
        """
        tokens = self.enc.encode(section.content)
        chunks = []
        chunk_index = 0
        
        i = 0
        while i < len(tokens):
            # Grab target_token_size tokens
            chunk_tokens = tokens[i:i + self.target_token_size]
            chunk_text = self.enc.decode(chunk_tokens)
            
            chunks.append(ChunkedDocument(
                content=chunk_text,
                source_file=section.source_file,
                section_title=section.title,
                chunk_index=chunk_index,
                metadata={
                    "level": section.level,
                    "line_number": section.line_number,
                }
            ))
            
            chunk_index += 1
            # Advance by target size minus overlap
            i += self.target_token_size - self.overlap_tokens
        
        return chunks

# Pipeline: Load → Parse → Chunk
def ingest_documents(docs_dir: str) -> List[ChunkedDocument]:
    loader = DocumentLoader(docs_dir)
    loader.load()
    
    parser = MarkdownParser()
    all_sections = []
    
    for filename, content in loader.get_raw_documents():
        sections = parser.extract_sections(filename, content)
        all_sections.extend(sections)
    
    chunker = ChunkerByTokenCount(target_token_size=256, overlap_tokens=32)
    all_chunks = []
    
    for section in all_sections:
        chunks = chunker.chunk_section(section)
        all_chunks.extend(chunks)
    
    print(f"Created {len(all_chunks)} chunks from {len(all_sections)} sections")
    return all_chunks
```

## Component 2: Embedding and Vector Storage

### Step 2.1: Choose an Embedding Model

For the course Q&A agent:
- **Model:** OpenAI `text-embedding-3-small` (1536 dimensions, fast, cheap)
- **Why small, not large?** Small is 5x cheaper and sufficient for Q&A. Large is overkill unless you have complex semantic queries.
- **Why OpenAI, not open source?** OpenAI's embedding is slightly better for general English. Open source models fine. Choose based on cost/latency tradeoff for your use case.

```python
import numpy as np
from openai import OpenAI
import json
from pathlib import Path

class EmbeddingStore:
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI()
        self.model = model
        self.embeddings: dict = {}  # chunk_id -> embedding vector
        self.chunks: dict = {}       # chunk_id -> ChunkedDocument
    
    def embed_chunks(self, chunks: List[ChunkedDocument], batch_size: int = 100):
        """
        Embed chunks in batches (API rate limit friendly).
        Store both embeddings and the original chunks.
        """
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            texts = [chunk.content for chunk in batch]
            
            # Call OpenAI embedding API
            response = self.client.embeddings.create(
                model=self.model,
                input=texts
            )
            
            # Store embeddings and chunk refs
            for chunk, emb_data in zip(batch, response.data):
                self.chunks[chunk.chunk_id] = chunk
                self.embeddings[chunk.chunk_id] = np.array(emb_data.embedding)
            
            print(f"Embedded {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")
    
    def save(self, output_dir: str):
        """Persist embeddings to disk (not rebuilding every time!)."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save embeddings as numpy arrays (more efficient than JSON)
        np.save(
            output_path / "embeddings.npy",
            np.array([self.embeddings[cid] for cid in sorted(self.embeddings.keys())])
        )
        
        # Save chunk IDs in order (so we know which embedding is which)
        with open(output_path / "chunk_ids.txt", "w") as f:
            for cid in sorted(self.embeddings.keys()):
                f.write(cid + "\n")
        
        # Save chunk metadata as JSON
        chunks_meta = {
            cid: {
                "content": self.chunks[cid].content,
                "source_file": self.chunks[cid].source_file,
                "section_title": self.chunks[cid].section_title,
                "chunk_index": self.chunks[cid].chunk_index,
            }
            for cid in self.chunks.keys()
        }
        with open(output_path / "chunks.json", "w") as f:
            json.dump(chunks_meta, f)
    
    def load(self, input_dir: str):
        """Load embeddings from disk."""
        input_path = Path(input_dir)
        
        embeddings_array = np.load(input_path / "embeddings.npy")
        with open(input_path / "chunk_ids.txt", "r") as f:
            chunk_ids = [line.strip() for line in f.readlines()]
        
        with open(input_path / "chunks.json", "r") as f:
            chunks_meta = json.load(f)
        
        for cid, emb in zip(chunk_ids, embeddings_array):
            self.embeddings[cid] = emb
        
        self.chunks = chunks_meta  # Store as dict, not ChunkedDocument objects
        print(f"Loaded {len(self.embeddings)} embeddings")

class VectorStore:
    """Simple in-memory vector search using cosine similarity."""
    
    def __init__(self, embedding_store: EmbeddingStore):
        self.embedding_store = embedding_store
    
    def search(self, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find top-k most similar chunks to query.
        Returns: [(chunk_id, similarity_score), ...]
        """
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        
        scores = {}
        for chunk_id, embedding in self.embedding_store.embeddings.items():
            # Cosine similarity = dot product of normalized vectors
            emb_norm = embedding / np.linalg.norm(embedding)
            similarity = np.dot(query_norm, emb_norm)
            scores[chunk_id] = similarity
        
        # Sort by score descending
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
```

### Step 2.2: Sparse Retrieval (BM25)

We'll use both dense (embedding-based) and sparse (keyword-based) retrieval, then combine them. Why both?

- **Dense retrieval** is great for semantic queries: "How does pricing work?" → finds chunks about pricing even if exact words don't match
- **Sparse retrieval** is great for keyword queries: "Uber surge pricing" → finds chunks with those exact words
- **Combining them** gives you robustness: some queries are semantic, some are keyword-based, hybrid catches both

```python
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

class SparseRetriever:
    """BM25-based retrieval (term frequency + document length normalization)."""
    
    def __init__(self):
        self.bm25_index = None
        self.chunk_ids = []
        self.chunks_by_id = {}
    
    def index_chunks(self, chunks: List[ChunkedDocument]):
        """Build BM25 index from chunks."""
        tokenized_chunks = []
        
        for chunk in chunks:
            # Simple tokenization (split by whitespace + remove punctuation)
            tokens = chunk.content.lower().split()
            tokens = [token.strip('.,!?;:"') for token in tokens if token.strip()]
            tokenized_chunks.append(tokens)
            self.chunk_ids.append(chunk.chunk_id)
            self.chunks_by_id[chunk.chunk_id] = chunk
        
        self.bm25_index = BM25Okapi(tokenized_chunks)
        print(f"Indexed {len(chunks)} chunks for BM25")
    
    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Search using BM25."""
        tokens = query.lower().split()
        tokens = [token.strip('.,!?;:"') for token in tokens if token.strip()]
        
        scores = self.bm25_index.get_scores(tokens)
        
        # Pair with chunk IDs
        scored_chunks = list(zip(self.chunk_ids, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        return scored_chunks[:top_k]

class HybridRetriever:
    """Combine dense and sparse retrieval using Reciprocal Rank Fusion (RRF)."""
    
    def __init__(self, 
                 vector_store: VectorStore,
                 sparse_retriever: SparseRetriever):
        self.vector_store = vector_store
        self.sparse_retriever = sparse_retriever
    
    def search(self, query: str, query_embedding: np.ndarray, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Use RRF to combine dense and sparse results.
        RRF formula: score = 1/(k + rank), then sum scores from both rankers.
        Why RRF? It's simple, rank-based (not score-based), and works well in practice.
        """
        
        # Dense retrieval (embedding-based)
        dense_results = self.vector_store.search(query_embedding, top_k=20)
        dense_rrf = {}
        for rank, (chunk_id, score) in enumerate(dense_results, 1):
            rrf_score = 1.0 / (60 + rank)  # 60 is a constant tuning parameter
            dense_rrf[chunk_id] = rrf_score
        
        # Sparse retrieval (BM25)
        sparse_results = self.sparse_retriever.search(query, top_k=20)
        sparse_rrf = {}
        for rank, (chunk_id, score) in enumerate(sparse_results, 1):
            rrf_score = 1.0 / (60 + rank)
            sparse_rrf[chunk_id] = rrf_score
        
        # Combine using RRF
        combined = {}
        for chunk_id in set(list(dense_rrf.keys()) + list(sparse_rrf.keys())):
            combined[chunk_id] = dense_rrf.get(chunk_id, 0) + sparse_rrf.get(chunk_id, 0)
        
        # Sort and return top-k
        sorted_results = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        return sorted_results[:top_k]
```

## Component 3: Reranking

Dense + sparse retrieval gets you to ~5 relevant chunks. Reranking picks the best 1-2. This is where a cross-encoder comes in.

```python
from sentence_transformers import CrossEncoder
from typing import Optional

class Reranker:
    """
    Cross-encoder reranking.
    Why cross-encoder instead of bi-encoder (embedding)?
    
    Bi-encoder (embedding): 
      - Scores similarity between query and chunk independently
      - Fast but lower accuracy
    
    Cross-encoder:
      - Processes query + chunk together as one input
      - Scores relevance directly
      - Slower but more accurate
      - Worth it when you already have 5 candidates to rerank
    """
    
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)
    
    def rerank(self, query: str, chunks: List[ChunkedDocument]) -> List[Tuple[ChunkedDocument, float]]:
        """
        Rerank chunks based on query relevance.
        Returns: [(chunk, relevance_score), ...]
        """
        if not chunks:
            return []
        
        # Prepare (query, chunk_text) pairs for cross-encoder
        pairs = [(query, chunk.content) for chunk in chunks]
        
        # Get scores (0-1, higher = more relevant)
        scores = self.model.predict(pairs)
        
        # Return sorted by score
        scored_chunks = list(zip(chunks, scores))
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        return scored_chunks
```

## Component 4: The Agent (Retrieval + Generation)

Now we wire everything together.

```python
from anthropic import Anthropic
import re

class CourseQAAgent:
    def __init__(self,
                 hybrid_retriever: HybridRetriever,
                 embedding_store: EmbeddingStore,
                 reranker: Reranker,
                 model: str = "claude-3-5-sonnet-20241022"):
        self.retriever = hybrid_retriever
        self.embedding_store = embedding_store
        self.reranker = reranker
        self.client = Anthropic()
        self.model = model
    
    def embed_query(self, query: str) -> np.ndarray:
        """Convert query to embedding."""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=query
        )
        return np.array(response.data[0].embedding)
    
    def _build_system_prompt(self, context_chunks: List[ChunkedDocument]) -> str:
        """Build the system prompt with retrieved context."""
        context_text = "\n\n---\n\n".join([
            f"[{chunk.source_file} > {chunk.section_title}]\n{chunk.content}"
            for chunk in context_chunks
        ])
        
        return f"""You are a helpful teaching assistant for an LLMOps course. 
Your job is to answer student questions using ONLY the course material provided below.

IMPORTANT RULES:
1. Answer only using the provided course material. Do not use outside knowledge.
2. If the question is not answered by the course material, say "I don't see that in the course material."
3. Always cite which section of the course material you're referencing.
4. Keep answers concise (2-3 sentences max).
5. If you're uncertain, say so.

COURSE MATERIAL:
{context_text}

---

Now answer the student's question. Format your answer as:
[ANSWER]
<your response>

[CITATIONS]
<list of sections you referenced>

[CONFIDENCE]
<high/medium/low>
"""
    
    def answer_query(self, query: str, trace: Optional[dict] = None) -> dict:
        """
        Full pipeline: retrieve → rerank → generate.
        Returns answer, citations, confidence, and trace.
        """
        if trace is None:
            trace = {}
        
        trace["query"] = query
        
        # Step 1: Embed the query
        query_embedding = self.embed_query(query)
        trace["embedding_computed"] = True
        
        # Step 2: Retrieve (hybrid)
        retrieved = self.retriever.search(
            query=query,
            query_embedding=query_embedding,
            top_k=5
        )
        
        # Convert chunk IDs back to ChunkedDocument objects
        retrieved_chunks = [
            ChunkedDocument(
                content=self.embedding_store.chunks[cid]["content"],
                source_file=self.embedding_store.chunks[cid]["source_file"],
                section_title=self.embedding_store.chunks[cid]["section_title"],
                chunk_index=self.embedding_store.chunks[cid]["chunk_index"]
            )
            for cid, _ in retrieved
        ]
        
        trace["retrieved_chunks"] = [
            {
                "source": chunk.source_file,
                "section": chunk.section_title,
                "preview": chunk.content[:100] + "..."
            }
            for chunk in retrieved_chunks
        ]
        
        # Step 3: Rerank
        reranked = self.reranker.rerank(query, retrieved_chunks)
        top_2_chunks = [chunk for chunk, score in reranked[:2]]
        top_2_scores = [score for chunk, score in reranked[:2]]
        
        trace["reranked_top_2_scores"] = top_2_scores
        
        # Step 4: Generate with context
        system_prompt = self._build_system_prompt(top_2_chunks)
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=300,
            system=system_prompt,
            messages=[
                {"role": "user", "content": query}
            ]
        )
        
        response_text = response.content[0].text
        trace["generation_tokens"] = response.usage.completion_tokens
        trace["prompt_tokens"] = response.usage.prompt_tokens
        
        # Step 5: Parse response and extract citations
        answer = self._extract_section(response_text, "ANSWER")
        citations = self._extract_section(response_text, "CITATIONS")
        confidence = self._extract_section(response_text, "CONFIDENCE")
        
        return {
            "answer": answer,
            "citations": citations,
            "confidence": confidence,
            "trace": trace
        }
    
    @staticmethod
    def _extract_section(text: str, section_name: str) -> str:
        """Extract [SECTION_NAME] ... content from response."""
        pattern = rf"\[{section_name}\](.*?)(?=\[|$)"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""
```

## Component 5: Full Run Loop

```python
def main():
    # 1. Ingest documents
    chunks = ingest_documents(docs_dir="./course_material/")
    
    # 2. Create embeddings and sparse index
    embedding_store = EmbeddingStore()
    embedding_store.embed_chunks(chunks)
    embedding_store.save("./vector_store/")
    
    sparse_retriever = SparseRetriever()
    sparse_retriever.index_chunks(chunks)
    
    # 3. Set up retrieval pipeline
    vector_store = VectorStore(embedding_store)
    hybrid_retriever = HybridRetriever(vector_store, sparse_retriever)
    
    # 4. Set up reranking
    reranker = Reranker()
    
    # 5. Create agent
    agent = CourseQAAgent(hybrid_retriever, embedding_store, reranker)
    
    # 6. Answer queries
    queries = [
        "How does Uber's surge pricing work?",
        "What is DoorDash's dispatch algorithm?",
        "Explain Lyft's matching system.",
    ]
    
    for query in queries:
        result = agent.answer_query(query)
        print(f"Q: {query}")
        print(f"A: {result['answer']}")
        print(f"Citations: {result['citations']}")
        print(f"Confidence: {result['confidence']}")
        print()

if __name__ == "__main__":
    main()
```

## Component 6: Real Example Walk-Through

Let's trace a real query through the system:

**Query:** "How does Uber update prices in real time?"

**Step 1: Embedding**
```
Query → OpenAI embedding API → vector [0.234, -0.891, 0.123, ...]
```

**Step 2: Dense Retrieval**
```
Top-5 by cosine similarity:
1. chunk_id=uber_case_study#pricing_algorithm#0, sim=0.87
2. chunk_id=uber_case_study#pricing_algorithm#1, sim=0.84
3. chunk_id=doordash_case_study#dispatch#2, sim=0.61
4. chunk_id=lyft_case_study#matching#0, sim=0.58
5. chunk_id=uber_case_study#supply_dynamics#1, sim=0.55
```

**Step 3: Sparse Retrieval (BM25)**
```
Top-5 by term frequency:
1. chunk_id=uber_case_study#pricing_algorithm#0, bm25=8.92
2. chunk_id=uber_case_study#pricing_algorithm#1, bm25=7.63
3. chunk_id=uber_case_study#supply_dynamics#1, bm25=5.21
4. chunk_id=doordash_case_study#dispatch#2, bm25=4.12
5. chunk_id=lyft_case_study#matching#0, bm25=3.88
```

**Step 4: Hybrid (RRF Combination)**
```
RRF score = (1/(60+rank_dense) + 1/(60+rank_sparse))

Combined ranking:
1. chunk_id=uber_case_study#pricing_algorithm#0, rrf=0.0357
2. chunk_id=uber_case_study#pricing_algorithm#1, rrf=0.0344
3. chunk_id=uber_case_study#supply_dynamics#1, rrf=0.0255
4. chunk_id=doordash_case_study#dispatch#2, rrf=0.0199
5. chunk_id=lyft_case_study#matching#0, rrf=0.0189
```

**Step 5: Reranking (Cross-encoder)**
```
Cross-encoder score (0-1):
- chunk_0: 0.94 ← Most relevant
- chunk_1: 0.89
- chunk_supply: 0.42
- chunk_doordash: 0.31
- chunk_lyft: 0.28

Keep top-2: chunk_0 (0.94) and chunk_1 (0.89)
```

**Step 6: Generation**
```
System prompt includes:
[Uber Case Study > Pricing Algorithm]
<actual chunk 0 text about how prices update every few minutes>

[Uber Case Study > Pricing Algorithm]
<actual chunk 1 text about demand signals>

User message: "How does Uber update prices in real time?"

Claude generates:
Uber updates prices every few minutes by analyzing real-time GPS data 
from drivers and order volume in each region. When demand exceeds supply, 
the multiplier increases to incentivize more drivers to come online.

[ANSWER]
Uber updates prices every few minutes by analyzing real-time GPS data from 
drivers and order volume in each region. The multiplier increases when demand 
exceeds supply.

[CITATIONS]
Uber Case Study, Section: Pricing Algorithm (chunks 1-2)

[CONFIDENCE]
high
```

**Step 7: Response**
```
Answer: "Uber updates prices every few minutes by analyzing real-time GPS data..."
Citations: "Uber Case Study, Section: Pricing Algorithm"
Confidence: "high"
```

## What Each Component Looks Like in Production

In production, your file structure looks like:

```
course_qa_agent/
├── documents/
│   ├── uber_case_study.md
│   ├── doordash_case_study.md
│   └── lyft_case_study.md
│
├── vector_store/              ← Persisted embeddings
│   ├── embeddings.npy         (4500 chunks × 1536 dims)
│   ├── chunk_ids.txt          (list of chunk_ids in order)
│   └── chunks.json            (chunk metadata)
│
├── agent/
│   ├── __init__.py
│   ├── loader.py              (DocumentLoader, MarkdownParser)
│   ├── chunker.py             (ChunkedDocument, ChunkerByTokenCount)
│   ├── embeddings.py          (EmbeddingStore, VectorStore)
│   ├── sparse.py              (SparseRetriever)
│   ├── hybrid.py              (HybridRetriever)
│   ├── rerank.py              (Reranker)
│   ├── qa_agent.py            (CourseQAAgent)
│   └── trace.py               (Trace logging, see file 3)
│
├── main.py                    (Entry point, run the agent)
├── requirements.txt
└── README.md
```

## Common Mistakes Beginners Make

### Mistake 1: Using Only Dense Retrieval

**Problem:** "I'll just use embeddings, that's what everyone does."

Dense retrieval is great for semantic queries but fails on keyword queries. If a student asks "DoorDash dispatch" with exact keywords and you only use embeddings, you might retrieve semantically similar but not directly relevant chunks.

**Solution:** Hybrid retrieval (dense + sparse + RRF). It's 20 more lines of code and prevents 50% of retrieval failures.

### Mistake 2: Not Reranking

**Problem:** "Dense retrieval gives me top-5, that's good enough."

Retrieval (even hybrid) is not precise. The #3 result might actually be more relevant than #1 for some queries. You keep all 5 and shove them into the LLM context.

**Result:** LLM sees irrelevant text, includes it in the answer, generates hallucinations.

**Solution:** Always rerank. It's one cross-encoder call, costs 1-2 cents, and catches 30% of bad retrievals.

### Mistake 3: Chunking by Character Count

**Problem:** "I'll just split every 500 characters."

Character count varies wildly across languages and formatting. In Python code, 500 chars is maybe 50 tokens. In dense prose, it's maybe 150 tokens. Your chunks are inconsistent.

**Solution:** Chunk by token count. Use a proper tokenizer (tiktoken). Consistent 256-token chunks are worth the 3 extra lines of code.

### Mistake 4: Ignoring Chunk Overlap

**Problem:** "I'll split at clean boundaries, no overlap."

If your concept spans two chunks, you split it in half. The retriever gets chunk 1 (just context) but not chunk 2 (the actual point). You lose information.

**Solution:** Use 32-token overlap. When you chunk tokens 0-256, also include tokens 224-480 as the next chunk. Cost: maybe 5% more embeddings. Benefit: concepts don't get split.

### Mistake 5: Not Logging Anything

**Problem:** "I'll just run the agent and see if it works."

When it breaks (and it will), you have no idea why. Did retrieval fail? Did the LLM hallucinate? Did the source chunk have bad data?

**Solution:** Log every step. In the next file, we build a full trace system. Every query produces a JSON log with retrieved chunks, reranker scores, tokens used, latency. When something breaks, you replay the log.

### Mistake 6: Assuming the LLM Won't Hallucinate

**Problem:** "Claude will only use the context I give it."

Claude is great but not perfect. If you give it context from chunk A, context from chunk B, and ask "what does the material say about X?", it might synthesize and hallucinate.

**Solution:** We handle this in file 3 with hallucination detection (citation check) and confidence scoring. For now, know that this is a real problem and plan for it.

---

## Adding Evals and Guardrails to Your Agent

You have a working agent. Now make it reliable. This file shows how to add evals (testing) and guardrails (safety) so your agent doesn't fail silently in production.

## Part 1: Building a Golden Dataset

You cannot evaluate what you don't measure. Start with a golden dataset: 10-20 hand-curated query-answer pairs that represent the cases you care about.

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class GoldenTestCase:
    """A hand-verified test case for the Course Q&A Agent."""
    query: str
    expected_answer_snippet: str  # Key phrase we expect in the answer
    expected_source_section: str  # Which section should be cited
    category: str                  # "pricing", "dispatch", "matching", "out_of_scope"
    difficulty: str                # "easy", "medium", "hard"
    reasoning: str                 # Why this test case matters

class GoldenDataset:
    """Hand-curated test cases for evaluation."""
    
    def __init__(self):
        self.cases: List[GoldenTestCase] = [
            GoldenTestCase(
                query="How does Uber's surge pricing work?",
                expected_answer_snippet="real-time GPS data",
                expected_source_section="Uber Case Study > Pricing Algorithm",
                category="pricing",
                difficulty="easy",
                reasoning="Core concept from case study, should be retrieved and answered"
            ),
            GoldenTestCase(
                query="What triggers an increase in Uber's price multiplier?",
                expected_answer_snippet="demand exceeds supply",
                expected_source_section="Uber Case Study > Pricing Algorithm",
                category="pricing",
                difficulty="medium",
                reasoning="Requires understanding causality, not just keywords"
            ),
            GoldenTestCase(
                query="How does DoorDash's dispatch algorithm rank restaurants?",
                expected_answer_snippet="delivery time and distance",
                expected_source_section="DoorDash Case Study > Dispatch",
                category="dispatch",
                difficulty="medium",
                reasoning="Cross-case study comparison, retriever must pick right source"
            ),
            GoldenTestCase(
                query="Describe Lyft's matching algorithm in detail.",
                expected_answer_snippet="driver location and passenger demand",
                expected_source_section="Lyft Case Study > Matching",
                category="matching",
                difficulty="hard",
                reasoning="Requires synthesis across multiple chunks"
            ),
            GoldenTestCase(
                query="What are the specific coordinates of Uber's headquarters?",
                expected_answer_snippet="",  # No answer expected
                expected_source_section="",
                category="out_of_scope",
                difficulty="easy",
                reasoning="Should trigger 'I don't see that in the course material'"
            ),
            GoldenTestCase(
                query="How does Uber's pricing compare to real-world market rates?",
                expected_answer_snippet="",  # Not in course material
                expected_source_section="",
                category="out_of_scope",
                difficulty="medium",
                reasoning="Requires outside knowledge, should be rejected"
            ),
            GoldenTestCase(
                query="Explain the relationship between supply dynamics and pricing in Uber.",
                expected_answer_snippet="more drivers available",
                expected_source_section="Uber Case Study",
                category="pricing",
                difficulty="hard",
                reasoning="Requires understanding relationship between two concepts"
            ),
            GoldenTestCase(
                query="What data sources does DoorDash use for dispatch decisions?",
                expected_answer_snippet="order volume and restaurant location",
                expected_source_section="DoorDash Case Study > Dispatch",
                category="dispatch",
                difficulty="medium",
                reasoning="Specific factual question about inputs to algorithm"
            ),
            GoldenTestCase(
                query="How do Lyft and Uber matching systems differ?",
                expected_answer_snippet="",  # Course doesn't cover both
                expected_source_section="",
                category="out_of_scope",
                difficulty="hard",
                reasoning="Comparative question, but course only covers Lyft and Uber separately"
            ),
            GoldenTestCase(
                query="What's the latency requirement for Uber's pricing updates?",
                expected_answer_snippet="",  # Not explicitly stated
                expected_source_section="",
                category="out_of_scope",
                difficulty="hard",
                reasoning="Missing detail in case study, should not hallucinate"
            ),
        ]
    
    def get_all_cases(self) -> List[GoldenTestCase]:
        return self.cases
    
    def get_by_category(self, category: str) -> List[GoldenTestCase]:
        return [c for c in self.cases if c.category == category]
```

## Part 2: Unit Eval - Retriever Recall

Does the retriever find the right chunk for each query? Recall@5: "Of the relevant chunks, what fraction appear in the top-5 results?"

```python
import json
from datetime import datetime

class RetrieverEval:
    """Test whether the retriever is actually finding relevant content."""
    
    def __init__(self, agent: 'CourseQAAgent'):
        self.agent = agent
        self.results = []
    
    def evaluate_retriever(self, 
                          test_cases: List[GoldenTestCase],
                          save_to: Optional[str] = None) -> dict:
        """
        Run retriever on each test case and check if the expected section is retrieved.
        """
        metrics = {
            "recall_at_5": 0,
            "recall_at_3": 0,
            "recall_at_1": 0,
            "total_queries": len(test_cases),
            "passed": 0,
            "failed": 0,
            "failures": []
        }
        
        for test in test_cases:
            if test.category == "out_of_scope":
                continue  # Skip out-of-scope tests for retriever eval
            
            # Retrieve chunks
            query_embedding = self.agent.embed_query(test.query)
            retrieved = self.agent.retriever.search(
                query=test.query,
                query_embedding=query_embedding,
                top_k=5
            )
            
            # Check if expected source is in top-5
            retrieved_ids = [cid for cid, _ in retrieved]
            
            # Convert back to chunk objects to get source info
            retrieved_chunks = [
                self.agent.embedding_store.chunks[cid] 
                for cid in retrieved_ids
            ]
            
            # Did we retrieve the right source?
            found_in_top5 = any(
                test.expected_source_section in chunk.get("section_title", "")
                for chunk in retrieved_chunks
            )
            found_in_top3 = found_in_top5 and any(
                test.expected_source_section in retrieved_chunks[i].get("section_title", "")
                for i in range(min(3, len(retrieved_chunks)))
            )
            found_in_top1 = found_in_top5 and (
                test.expected_source_section in retrieved_chunks[0].get("section_title", "")
            )
            
            # Update metrics
            if found_in_top5:
                metrics["recall_at_5"] += 1
                metrics["passed"] += 1
            else:
                metrics["failed"] += 1
                metrics["failures"].append({
                    "query": test.query,
                    "expected_section": test.expected_source_section,
                    "retrieved_sections": [
                        chunk.get("section_title", "")
                        for chunk in retrieved_chunks
                    ]
                })
            
            if found_in_top3:
                metrics["recall_at_3"] += 1
            if found_in_top1:
                metrics["recall_at_1"] += 1
        
        # Convert to percentages
        n = metrics["total_queries"]
        if n > 0:
            metrics["recall_at_5"] = metrics["recall_at_5"] / n
            metrics["recall_at_3"] = metrics["recall_at_3"] / n
            metrics["recall_at_1"] = metrics["recall_at_1"] / n
        
        # Save results
        if save_to:
            with open(save_to, "w") as f:
                json.dump(metrics, f, indent=2)
        
        return metrics
```

## Part 3: Unit Eval - Answer Quality

Does the LLM generate a good answer given the retrieved chunks? This is harder because "good" is subjective. We use both rule-based checks and LLM-as-judge.

```python
class AnswerQualityEval:
    """Test whether generated answers are good quality."""
    
    def __init__(self, agent: 'CourseQAAgent'):
        self.agent = agent
    
    def evaluate_answer(self, test: GoldenTestCase, agent_response: dict) -> dict:
        """
        Check: Does the answer contain the expected snippet?
        Check: Does it cite a source?
        Check: Is the confidence appropriate?
        """
        answer = agent_response["answer"].lower()
        citations = agent_response["citations"]
        confidence = agent_response["confidence"].lower()
        
        result = {
            "query": test.query,
            "expected_snippet": test.expected_answer_snippet,
            "passed": False,
            "checks": {}
        }
        
        # Check 1: Contains expected snippet
        snippet_match = test.expected_answer_snippet.lower() in answer
        result["checks"]["snippet_found"] = snippet_match
        
        # Check 2: Has a citation (for in-scope questions)
        has_citation = len(citations.strip()) > 0 and not "don't" in citations.lower()
        result["checks"]["has_citation"] = has_citation
        
        # Check 3: Confidence is reasonable
        valid_confidences = ["high", "medium", "low"]
        confidence_valid = any(c in confidence for c in valid_confidences)
        result["checks"]["valid_confidence"] = confidence_valid
        
        # Overall: pass if all checks pass for in-scope, or if properly rejected out-of-scope
        if test.category == "out_of_scope":
            result["passed"] = "don't see that" in answer or "not in the course" in answer
        else:
            result["passed"] = snippet_match and has_citation and confidence_valid
        
        return result
    
    def evaluate_all(self, test_cases: List[GoldenTestCase]) -> dict:
        """Run all test cases and return aggregate metrics."""
        individual_results = []
        
        for test in test_cases:
            response = self.agent.answer_query(test.query)
            result = self.evaluate_answer(test, response)
            individual_results.append(result)
        
        # Aggregate
        passed = sum(1 for r in individual_results if r["passed"])
        total = len(individual_results)
        
        return {
            "accuracy": passed / total if total > 0 else 0,
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "results": individual_results
        }
```

## Part 4: End-to-End Eval with LLM-as-Judge

For harder cases, let an LLM grade the answer. This is more expensive but more accurate.

```python
class LLMAsJudge:
    """
    Use Claude to grade agent responses.
    Why not just binary checks? Because nuance matters.
    "Mostly correct but missing a detail" is different from "completely wrong".
    """
    
    JUDGE_PROMPT = """You are an expert evaluator of a course Q&A agent.
Your job is to grade the agent's answer to a student question.

CRITERIA:
1. Accuracy: Is the answer factually correct based on the provided context?
2. Completeness: Does it answer the full question asked?
3. Clarity: Is the explanation easy to understand?
4. Citations: Are sources properly cited?
5. Scope: Does it stay within the course material (not make up information)?

For each criterion, score 0-1. Then provide an overall score 0-1.

CONTEXT PROVIDED TO AGENT:
{context}

QUESTION:
{question}

AGENT'S ANSWER:
{answer}

AGENT'S CITATIONS:
{citations}

---

Please grade on each criterion (0-1 scale), then give an overall score.
Format your response as JSON:
{{
  "accuracy": 0.8,
  "completeness": 0.7,
  "clarity": 0.9,
  "citations": 0.85,
  "scope": 0.95,
  "overall": 0.85,
  "reasoning": "The agent correctly explained the pricing mechanism..."
}}
"""
    
    def __init__(self, agent: 'CourseQAAgent'):
        self.agent = agent
        self.client = Anthropic()
    
    def grade_response(self, test: GoldenTestCase, agent_response: dict) -> dict:
        """Get Claude to grade an agent response."""
        
        context = "\n---\n".join([
            f"[{chunk['source_file']}]\n{chunk['content']}"
            for chunk in agent_response["trace"].get("retrieved_chunks", [])
        ])
        
        prompt = self.JUDGE_PROMPT.format(
            context=context,
            question=test.query,
            answer=agent_response["answer"],
            citations=agent_response["citations"]
        )
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # Extract JSON from response
            response_text = response.content[0].text
            # Find JSON block
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                scores = json.loads(json_match.group())
                return scores
        except:
            return {"error": "Could not parse judge response"}
```

## Part 5: Regression Testing - Old vs New

When you change your agent, compare the new version against the old.

```python
class RegressionTest:
    """
    Compare old agent version vs new agent version.
    Make sure improvements don't break existing cases.
    """
    
    def __init__(self, 
                 old_agent: 'CourseQAAgent',
                 new_agent: 'CourseQAAgent'):
        self.old_agent = old_agent
        self.new_agent = new_agent
    
    def compare_on_golden_dataset(self, 
                                  test_cases: List[GoldenTestCase]) -> dict:
        """
        Run golden dataset on both agents, compare results.
        """
        results = {
            "old_accuracy": 0,
            "new_accuracy": 0,
            "improvement": 0,
            "regressions": [],  # Cases that got worse
            "improvements": [],  # Cases that got better
            "details": []
        }
        
        old_passed = 0
        new_passed = 0
        
        for test in test_cases:
            old_response = self.old_agent.answer_query(test.query)
            new_response = self.new_agent.answer_query(test.query)
            
            # Grade both
            old_eval = self._quick_eval(test, old_response)
            new_eval = self._quick_eval(test, new_response)
            
            if old_eval:
                old_passed += 1
            if new_eval:
                new_passed += 1
            
            # Track what changed
            if old_eval and not new_eval:
                results["regressions"].append({
                    "query": test.query,
                    "was_working": True,
                    "now_working": False
                })
            elif not old_eval and new_eval:
                results["improvements"].append({
                    "query": test.query,
                    "was_working": False,
                    "now_working": True
                })
            
            results["details"].append({
                "query": test.query,
                "old_answer": old_response["answer"],
                "new_answer": new_response["answer"],
                "old_score": 1 if old_eval else 0,
                "new_score": 1 if new_eval else 0
            })
        
        total = len(test_cases)
        results["old_accuracy"] = old_passed / total if total > 0 else 0
        results["new_accuracy"] = new_passed / total if total > 0 else 0
        results["improvement"] = results["new_accuracy"] - results["old_accuracy"]
        
        return results
    
    @staticmethod
    def _quick_eval(test: GoldenTestCase, response: dict) -> bool:
        """Simple pass/fail check."""
        if test.category == "out_of_scope":
            return "don't see that" in response["answer"].lower()
        else:
            return test.expected_answer_snippet.lower() in response["answer"].lower()
```

## Part 6: Input Guardrails

Reject bad inputs before they get to the agent.

```python
class InputGuardrails:
    """Validate and filter inputs before agent processes them."""
    
    def __init__(self):
        self.client = Anthropic()
    
    def validate(self, query: str) -> tuple[bool, Optional[str]]:
        """
        Check: Is the query in scope?
        Return: (is_valid, reason_if_invalid)
        """
        
        # Check 1: Length
        if len(query) > 500:
            return False, "Query too long (max 500 chars)"
        
        if len(query) < 5:
            return False, "Query too short (min 5 chars)"
        
        # Check 2: Toxicity (simple keyword check)
        toxic_keywords = ["bomb", "kill", "hate"]
        if any(kw in query.lower() for kw in toxic_keywords):
            return False, "Query contains inappropriate language"
        
        # Check 3: Scope (use LLM to detect out-of-scope)
        is_in_scope = self._check_scope(query)
        if not is_in_scope:
            return False, "Query is outside course scope"
        
        return True, None
    
    def _check_scope(self, query: str) -> bool:
        """
        Use LLM to check if query is about course topics.
        Topics: Uber pricing, DoorDash dispatch, Lyft matching.
        """
        prompt = f"""Is this question about one of these topics?
- Uber's pricing system
- DoorDash's dispatch algorithm
- Lyft's matching system

Question: {query}

Respond with only "YES" or "NO"."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=5,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return "YES" in response.content[0].text.upper()
```

## Part 7: Output Guardrails

Check the agent's output before returning it.

```python
class OutputGuardrails:
    """Validate agent output for safety and quality."""
    
    def __init__(self, agent: 'CourseQAAgent'):
        self.agent = agent
        self.client = Anthropic()
    
    def validate_response(self, response: dict) -> dict:
        """
        Run all output checks. Return modified response with validation results.
        """
        answer = response["answer"]
        citations = response["citations"]
        
        # Check 1: Citation completeness
        citation_check = self._check_citations(answer, citations)
        
        # Check 2: Hallucination detection
        hallucination_score = self._detect_hallucination(answer)
        
        # Check 3: Confidence coherence
        confidence_check = self._check_confidence_coherence(
            answer, 
            response["confidence"],
            hallucination_score
        )
        
        response["validation"] = {
            "citations_valid": citation_check["valid"],
            "hallucination_risk": hallucination_score,
            "confidence_coherent": confidence_check["coherent"],
            "safe_to_return": (
                citation_check["valid"] and 
                hallucination_score < 0.5 and
                confidence_check["coherent"]
            )
        }
        
        return response
    
    def _check_citations(self, answer: str, citations: str) -> dict:
        """
        Does the answer actually cite sources?
        Are cited sources specific (not vague)?
        """
        
        # Check: does answer contain [Citation] marker?
        has_marker = "[citation" in answer.lower() or "[source" in answer.lower()
        
        # Check: are citations specific (not vague)?
        vague_phrases = ["the course", "somewhere", "I think", "probably"]
        is_vague = any(phrase in citations.lower() for phrase in vague_phrases)
        
        return {
            "valid": not is_vague and len(citations.strip()) > 10,
            "has_marker": has_marker,
            "is_vague": is_vague
        }
    
    def _detect_hallucination(self, answer: str) -> float:
        """
        Score 0-1: how likely is this answer hallucinated?
        Uses LLM to detect contradictions, made-up details, etc.
        """
        prompt = f"""Rate how likely this answer is to contain made-up information (hallucination).
        
Score 0-1 where:
0 = Confident this is all true
0.5 = Uncertain
1 = Confident this contains false information

Answer: {answer}

Respond with only a number 0-1 and brief reasoning."""
        
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=20,
                messages=[{"role": "user", "content": prompt}]
            )
            
            text = response.content[0].text
            # Extract float from response
            import re
            match = re.search(r'0\.\d+|1\.0|[0-1]', text)
            if match:
                return float(match.group())
        except:
            pass
        
        return 0.5  # Default to uncertain
    
    def _check_confidence_coherence(self, answer: str, confidence: str, hallucination_score: float) -> dict:
        """
        Is the agent's confidence claim coherent with hallucination risk?
        E.g., if hallucination_score is 0.8 and confidence is "high", that's incoherent.
        """
        
        # Parse confidence
        conf_num = 0.5
        if "high" in confidence.lower():
            conf_num = 0.9
        elif "low" in confidence.lower():
            conf_num = 0.1
        
        # Check coherence: if hallucination is high, confidence should be low
        coherent = abs(conf_num + (1 - hallucination_score)) / 2 < 0.3
        
        return {
            "coherent": coherent,
            "stated_confidence": conf_num,
            "risk_based_confidence": 1 - hallucination_score
        }
```

## Part 8: Trace Logging

Every query produces a full trace. When something breaks, you replay it.

```python
class TraceLogger:
    """Log every query and every decision for debugging."""
    
    def __init__(self, log_dir: str = "./query_logs/"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
    
    def log_query(self, query: str, response: dict, validation: dict):
        """Save a complete trace of one query."""
        
        trace_data = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": {
                "answer": response["answer"],
                "citations": response["citations"],
                "confidence": response["confidence"],
            },
            "trace": response.get("trace", {}),
            "validation": validation,
        }
        
        # Save as JSON with timestamp in filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = self.log_dir / f"query_{timestamp}.json"
        
        with open(filename, "w") as f:
            json.dump(trace_data, f, indent=2)
    
    def read_traces(self, limit: int = 100) -> List[dict]:
        """Load recent traces for analysis."""
        traces = []
        
        for trace_file in sorted(self.log_dir.glob("query_*.json"), reverse=True)[:limit]:
            with open(trace_file) as f:
                traces.append(json.load(f))
        
        return traces
    
    def analyze_traces(self, traces: List[dict]) -> dict:
        """Compute aggregate stats from traces."""
        
        total_queries = len(traces)
        
        # Latency
        latencies = [
            t["trace"].get("total_latency_ms", 0)
            for t in traces
        ]
        
        # Tokens
        total_tokens = sum(
            t["trace"].get("generation_tokens", 0) +
            t["trace"].get("prompt_tokens", 0)
            for t in traces
        )
        
        # Confidence distribution
        confidences = [t["response"]["confidence"].lower() for t in traces]
        high_conf = sum(1 for c in confidences if "high" in c)
        
        # Failures (validation issues)
        failures = sum(
            1 for t in traces
            if not t["validation"].get("safe_to_return", False)
        )
        
        return {
            "total_queries": total_queries,
            "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
            "p95_latency_ms": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
            "total_tokens": total_tokens,
            "avg_tokens_per_query": total_tokens / total_queries if total_queries > 0 else 0,
            "high_confidence_pct": high_conf / total_queries if total_queries > 0 else 0,
            "failure_rate": failures / total_queries if total_queries > 0 else 0,
        }
```

## Part 9: Cost Tracking

Know how much your agent costs to run.

```python
class CostTracker:
    """Track token usage and cost per query."""
    
    # OpenAI pricing (as of this writing)
    EMBEDDING_COST_PER_1M = 0.02  # text-embedding-3-small
    CLAUDE_INPUT_COST_PER_1M = 3.0  # claude-3-5-sonnet
    CLAUDE_OUTPUT_COST_PER_1M = 15.0
    CROSS_ENCODER_COST_PER_QUERY = 0.001  # Rough estimate
    
    def __init__(self):
        self.queries = []
    
    def track_query(self, trace: dict):
        """Record tokens used in a single query."""
        
        cost = 0
        
        # Embedding cost (1 embedding per query)
        embedding_tokens = 10  # Rough average query length
        cost += (embedding_tokens / 1_000_000) * self.EMBEDDING_COST_PER_1M
        
        # Generation cost
        input_tokens = trace.get("prompt_tokens", 0)
        output_tokens = trace.get("generation_tokens", 0)
        cost += (input_tokens / 1_000_000) * self.CLAUDE_INPUT_COST_PER_1M
        cost += (output_tokens / 1_000_000) * self.CLAUDE_OUTPUT_COST_PER_1M
        
        # Reranking cost (rough)
        cost += self.CROSS_ENCODER_COST_PER_QUERY
        
        self.queries.append({
            "timestamp": datetime.now().isoformat(),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "cost_usd": cost
        })
    
    def get_stats(self) -> dict:
        """Aggregate cost statistics."""
        if not self.queries:
            return {}
        
        total_cost = sum(q["cost_usd"] for q in self.queries)
        total_tokens = sum(q["total_tokens"] for q in self.queries)
        
        return {
            "total_queries": len(self.queries),
            "total_cost_usd": round(total_cost, 4),
            "cost_per_query_usd": round(total_cost / len(self.queries), 4),
            "total_tokens": total_tokens,
            "tokens_per_query": round(total_tokens / len(self.queries), 0),
            "cost_per_1k_tokens": round((total_cost / total_tokens) * 1000, 4) if total_tokens > 0 else 0,
        }
```

## Part 10: Full Eval Pipeline

Wire everything together.

```python
class EvalPipeline:
    """Run all evals and report results."""
    
    def __init__(self, agent: 'CourseQAAgent'):
        self.agent = agent
        self.golden_dataset = GoldenDataset()
        
        self.retriever_eval = RetrieverEval(agent)
        self.answer_quality_eval = AnswerQualityEval(agent)
        self.judge = LLMAsJudge(agent)
        self.input_guardrails = InputGuardrails()
        self.output_guardrails = OutputGuardrails(agent)
        self.trace_logger = TraceLogger()
        self.cost_tracker = CostTracker()
    
    def run_full_eval(self) -> dict:
        """Run all evals, return comprehensive report."""
        
        test_cases = self.golden_dataset.get_all_cases()
        
        print("Running retriever eval...")
        retriever_results = self.retriever_eval.evaluate_retriever(test_cases)
        
        print("Running answer quality eval...")
        answer_quality = self.answer_quality_eval.evaluate_all(test_cases)
        
        print("Running LLM-as-judge...")
        judge_results = []
        for test in test_cases:
            response = self.agent.answer_query(test.query)
            scores = self.judge.grade_response(test, response)
            judge_results.append(scores)
        
        print("Analyzing traces...")
        traces = self.trace_logger.read_traces(limit=None)
        trace_analysis = self.trace_logger.analyze_traces(traces)
        
        print("Computing costs...")
        costs = self.cost_tracker.get_stats()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "retriever": retriever_results,
            "answer_quality": answer_quality,
            "judge_scores": judge_results,
            "traces": trace_analysis,
            "costs": costs,
            "summary": {
                "retriever_recall_at_5": retriever_results.get("recall_at_5", 0),
                "answer_accuracy": answer_quality.get("accuracy", 0),
                "judge_avg_score": sum(
                    s.get("overall", 0) for s in judge_results if "overall" in s
                ) / len([s for s in judge_results if "overall" in s]) if judge_results else 0,
                "avg_latency_ms": trace_analysis.get("avg_latency_ms", 0),
                "cost_per_query": costs.get("cost_per_query_usd", 0),
                "production_ready": (
                    retriever_results.get("recall_at_5", 0) > 0.8 and
                    answer_quality.get("accuracy", 0) > 0.8 and
                    trace_analysis.get("avg_latency_ms", 0) < 3000
                )
            }
        }
```

## Production Readiness Checklist

Before shipping to production, check all of these:

- [ ] Golden dataset created (10+ test cases covering all categories)
- [ ] Retriever recall is >80% on golden dataset
- [ ] Answer quality accuracy is >80%
- [ ] LLM-as-judge average score is >0.75
- [ ] Average latency is <3 seconds
- [ ] Cost per query is acceptable (<$0.05)
- [ ] Input guardrails reject out-of-scope queries
- [ ] Output guardrails flag hallucinations
- [ ] Trace logging is enabled and tested
- [ ] All failure modes have a detection method
- [ ] Team has agreement on SLOs (Service Level Objectives):
  - Availability: 99.5% uptime
  - Latency: p95 < 3 seconds
  - Accuracy: 85%+ on golden dataset
  - Cost: <$0.05 per query
- [ ] Monitoring dashboard created (latency, errors, costs)
- [ ] Runbook written (what to do when it breaks)
- [ ] On-call rotation established

## When Your Agent Fails in Production

Real failure modes and how to detect them:

### Failure Mode 1: Silent Hallucination

**What it looks like:** Agent returns confident-sounding but incorrect information. User reads it, trusts it, acts on it.

**Why it happens:** LLM synthesizes context + question into plausible-sounding but made-up detail.

**How to detect:**
- LLM-as-judge scores drop suddenly
- Manual spot-check of recent traces
- User complaints (hardest to hear but most reliable)

**How to fix:**
- Lower confidence threshold (flag more responses for review)
- Increase context specificity (better retrieval)
- Add explicit "I don't know" prompt: "If this detail is not in the context, say 'I don't see that'"

### Failure Mode 2: Retrieval Drift

**What it looks like:** Agent used to answer "How does Uber pricing work?" correctly. Now it doesn't.

**Why it happens:** Vector embeddings drift slightly over time (model updates, etc). Or knowledge base changed and you didn't re-embed.

**How to detect:**
- Compare new traces against old (regression test)
- Retriever recall drops from 90% to 70%
- Same queries get different answers

**How to fix:**
- Re-embed knowledge base
- Check for data quality issues in knowledge base
- Increase top-k retrieval (trade latency for recall)

### Failure Mode 3: Context Window Overflow

**What it looks like:** Latency suddenly spikes from 1s to 10s. Or responses become shorter.

**Why it happens:** You retrieved too many chunks. The prompt is now 80K tokens instead of 8K.

**How to detect:**
- Token count in trace suddenly high
- Latency spike in monitoring dashboard
- Cost per query increases 10x

**How to fix:**
- Reduce top-k retrieval
- Improve reranking (keep only the best 1-2 chunks)
- Use token limits: if prompt is >10K tokens, truncate

### Failure Mode 4: Out-of-Scope Leakage

**What it looks like:** Agent answers questions it shouldn't. "What's Uber's stock price?" "When was Lyft founded?"

**Why it happens:** Agent has general knowledge from training. You didn't add strong scope guardrails.

**How to detect:**
- Manual review finds answers without citations
- LLM-as-judge flags "scope" score <0.8
- Input guardrail logs show many out-of-scope rejections

**How to fix:**
- Strengthen input guardrails (more aggressive scope filtering)
- Add explicit output guardrail: "Only answer if you have relevant context retrieved"
- Add confidence penalty for questions with zero relevant retrievals

### Failure Mode 5: Data Quality

**What it looks like:** Responses include garbled text, missing sections, repeated phrases.

**Why it happens:** Knowledge base has corrupted chunks. Bad chunking split mid-sentence.

**How to detect:**
- Spot-check a few responses and read the source chunks
- Write validation script during ingestion: check chunk quality
- Manual review of top-100 retrieved chunks

**How to fix:**
- Re-validate knowledge base
- Re-chunk using better chunking strategy
- Add chunk validation during ingestion (minimum length, no garbled UTF-8, etc)

### Failure Mode 6: Cascading Failures

**What it looks like:** One component fails (embedding API down), and the whole agent hangs.

**Why it happens:** No fallback logic. No timeouts. No error handling.

**How to detect:**
- Service health checks (is embedding API responding?)
- Timeout monitoring (queries hanging >10s)

**How to fix:**
- Add fallback: if embedding API fails, use sparse-only retrieval (slower but works)
- Add timeouts on all external API calls
- Add circuit breaker: if embedding API has been failing >10 times, stop using it and fallback

### Example: Replaying a Failed Query

```python
# From your trace logs, you have:
failed_trace = {
    "query": "How does Uber's pricing work?",
    "retrieved_chunks": [...],
    "generation_tokens": 150,
    "answer": "Uber's pricing is based on...",  # Possibly wrong
}

# Replay and debug:
agent = CourseQAAgent(...)

# 1. Check if retrieval was the problem
query_embedding = agent.embed_query(failed_trace["query"])
retrieved = agent.retriever.search(
    query=failed_trace["query"],
    query_embedding=query_embedding,
    top_k=5
)
print("Retrieved chunks:", [cid for cid, _ in retrieved])
# Compare to failed_trace["retrieved_chunks"] — did it change?

# 2. Check if reranking was the problem
reranked = agent.reranker.rerank(query, retrieved_chunks)
print("Reranked scores:", [score for _, score in reranked])

# 3. Check if generation was the problem
prompt = agent._build_system_prompt(retrieved_chunks[:2])
# Is the prompt reasonable? Is the context helpful?

# 4. Look at the actual response
response = agent.answer_query(failed_trace["query"])
print("New answer:", response["answer"])
print("Did it get better? Worse? Why?")
```

This is your debugging process. Traces make it possible.
