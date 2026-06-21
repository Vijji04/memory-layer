---
title: RAG Architecture
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
confidence: high
consolidated_from: 7 pages
---

# RAG Architecture

> Consolidated from 7 related concept pages.

---

## Citation Grounding Requiring every LLM response to cite exact document section a

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Hybrid RAG Dense Sparse RRF Combines BM25 lexical search with dense vector embed

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Metadata First Filtering Pre filtering a structured corpus by deterministic meta

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Pattern Simple RAG Agents

When agents need to act on domain knowledge—not hallucinate—RAG is the pattern. But "RAG" spans a spectrum: from naive semantic search to sophisticated hybrid retrieval with citation verification. This section shows three real deployments with fundamentally different problem shapes and the retrieval strategies that solved them.

The core insight: **retrieval strategy is problem-specific**. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards. Build RAG systems by understanding what your corpus looks like and what your users actually ask.

---

## Case Study 1: Rio Tinto — Hybrid RAG for Mining Knowledge Assistant

### The Business Problem

Rio Tinto, one of the world's largest mining operations, employs 10,000+ engineers across open-pit mines, underground operations, and metallurgical facilities. Each site has a documentation library:
- **Proprietary technical manuals** (500+ pages each, 50 manuals total)
- **Safety regulations** (OSHA, local mining codes, site-specific rules)
- **Equipment specifications** (CAT, Komatsu, custom rigs)
- **Procedure documentation** (drilling, blasting, ore processing)

Engineers constantly query this corpus. A drilling supervisor needs to know the maximum thrust for the rig on Site XYZ at 1,000 meters depth. A new engineer learning ore processing needs clarification on flotation parameters. The problem: **mining terminology is highly specialized**. A semantic embedding might match "ore grade" to "grading system" (wrong domain). And equipment model numbers (`CAT 390F`) are meaningless to a pure embedding model.

Rio Tinto built a knowledge assistant. The MVP failed—pure semantic search returned irrelevant results for 30% of queries. Equipment specs were buried under procedure docs. Safety-critical queries needed high precision, not novelty ranking.

### Why This Pattern Fits

**Hybrid retrieval** (dense semantic + sparse lexical) addresses the problem:
- **Sparse (BM25)** excels at exact term matching: equipment model numbers, procedure names, safety code references
- **Dense (embeddings)** captures semantic understanding: "maximum thrust at depth" even if phrased differently
- **Reciprocal Rank Fusion (RRF)** merges both results intelligently: if both agree, confidence rises; if only one retrieves, it still ranks

For specialized domains with:
- Mixed structured/unstructured documents
- Heavy use of proper nouns (equipment models, site names, procedure codes)
- High precision requirements (safety-critical)

…hybrid retrieval outperforms pure semantic search.

Additionally, Rio Tinto needed **citation grounding**: every response must cite the exact document section and page number. Engineers need to verify the source and update it if outdated.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                       Query from Engineer                       │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐       ┌───────▼────────┐
        │  BM25 Index    │       │  Dense Vector  │
        │  (Sparse)      │       │  Index         │
        │                │       │  (Semantic)    │
        │  • Equipment   │       │                │
        │    models      │       │  • Embeddings  │
        │  • Procedure   │       │    of chunks   │
        │    codes       │       │  • Learned on  │
        │  • Safety      │       │    mining      │
        │    references  │       │    corpus      │
        └───────┬────────┘       └───────┬────────┘
                │                        │
                │ (Top 50)          (Top 50)
                │                        │
                └────────────┬───────────┘
                             │
                ┌────────────▼──────────────┐
                │  Reciprocal Rank Fusion   │
                │                          │
                │  • Combine rankings      │
                │  • Score = 1/(k+rank)    │
                │  • Merge and deduplicate │
                └────────────┬──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Top 10 chunks  │
                    │  with metadata  │
                    └────────┬────────┘
                             │
        ┌────────────────────▼──────────────────────┐
        │  LLM Context Injection                    │
        │                                           │
        │  System: You are a mining expert...      │
        │  Context:                                │
        │  Chunk 1 (CAT_390F_Manual.pdf#p47)      │
        │  Chunk 2 (Safety_Code_Site_A#section_4.2) │
        │  ...                                      │
        │  Query: ...                              │
        └────────────┬───────────────────────────────┘
                     │
        ┌────────────▼─────────────┐
        │  LLM Response Generation │
        │                          │
        │  ✓ Cite sources by doc   │
        │    and page number       │
        │  ✓ Mark confidence level │
        │  ✓ Suggest manual update │
        │    if info is stale      │
        └────────────┬─────────────┘
                     │
                ┌────▼────────────┐
                │ Response to User │
                └─────────────────┘
```

### Implementation: Key Components

#### 1. Document Chunking Strategy for Dense Technical Manuals

Rio Tinto's manuals are structured: chapters, sections, diagrams, tables. Naive chunking on token limits destroys this structure.

```python
import os
from typing import List, Tuple
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import json

class MiningDocumentChunker:
    """
    Smart chunking for dense technical manuals.
    
    Preserves structure and metadata for traceability.
    """
    
    def __init__(self):
        # Mining docs have specialized structure
        self.separators = [
            "\n## ",      # Main section headers
            "\n### ",     # Subsections
            "\n#### ",    # Sub-subsections
            "\n\n",       # Paragraphs
            "\n",         # Lines
            " ",          # Words
            "",           # Characters
        ]
        
    def chunk_pdf(
        self, 
        pdf_path: str, 
        chunk_size: int = 500,
        overlap: int = 100
    ) -> List[dict]:
        """
        Extract and chunk a PDF, preserving metadata.
        
        Returns:
            List of dicts with:
            - content: text chunk
            - source_doc: filename
            - page_numbers: list of pages
            - section_hierarchy: [chapter, section, subsection]
        """
        reader = PdfReader(pdf_path)
        chunks = []
        
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text()
            
            # Parse page structure
            lines = text.split('\n')
            current_hierarchy = []
            current_chunk = []
            current_pages = set([page_idx + 1])
            
            for line in lines:
                # Detect header levels (rough heuristic)
                if line.startswith('## '):
                    # New section: save previous chunk if exists
                    if current_chunk:
                        chunks.append({
                            'content': '\n'.join(current_chunk),
                            'source_doc': os.path.basename(pdf_path),
                            'page_numbers': sorted(list(current_pages)),
                            'section_hierarchy': current_hierarchy.copy(),
                            'chunk_type': 'section_body'
                        })
                        current_chunk = []
                    current_hierarchy = [line.replace('## ', '').strip()]
                    
                elif line.startswith('### '):
                    if current_chunk and len(current_chunk) > 10:  # Avoid tiny chunks
                        chunks.append({
                            'content': '\n'.join(current_chunk),
                            'source_doc': os.path.basename(pdf_path),
                            'page_numbers': sorted(list(current_pages)),
                            'section_hierarchy': current_hierarchy.copy(),
                            'chunk_type': 'subsection_body'
                        })
                        current_chunk = []
                    if len(current_hierarchy) >= 1:
                        current_hierarchy = current_hierarchy[:1] + [line.replace('### ', '').strip()]
                    
                else:
                    current_chunk.append(line)
                    
                    # Flush chunk if it hits size limit
                    if sum(len(l) for l in current_chunk) >= chunk_size:
                        chunks.append({
                            'content': '\n'.join(current_chunk),
                            'source_doc': os.path.basename(pdf_path),
                            'page_numbers': sorted(list(current_pages)),
                            'section_hierarchy': current_hierarchy.copy(),
                            'chunk_type': 'body'
                        })
                        # Overlap: keep last few lines
                        current_chunk = current_chunk[-(overlap // 50):]
        
        # Final chunk
        if current_chunk:
            chunks.append({
                'content': '\n'.join(current_chunk),
                'source_doc': os.path.basename(pdf_path),
                'page_numbers': sorted(list(current_pages)),
                'section_hierarchy': current_hierarchy.copy(),
                'chunk_type': 'body'
            })
        
        return chunks

# Usage
chunker = MiningDocumentChunker()
chunks = chunker.chunk_pdf('CAT_390F_Manual.pdf', chunk_size=500, overlap=100)
print(f"Created {len(chunks)} chunks")
# Example output:
# {
#   'content': 'Maximum thrust at 1000m depth: 45,000 PSI...',
#   'source_doc': 'CAT_390F_Manual.pdf',
#   'page_numbers': [47, 48],
#   'section_hierarchy': ['Equipment Specs', 'Drilling Parameters'],
#   'chunk_type': 'body'
# }
```

#### 2. Hybrid Retrieval with Reciprocal Rank Fusion

```python
from typing import List, Dict, Tuple
import numpy as np

class HybridRetriever:
    """
    Hybrid dense + sparse retrieval with RRF fusion.
    """
    
    def __init__(self, sparse_index, dense_index, k=60):
        """
        sparse_index: BM25 searcher (e.g., from Elasticsearch or rank_bm25)
        dense_index: Vector DB (e.g., Chroma, FAISS)
        k: Number of results to retrieve from each before fusion
        """
        self.sparse_index = sparse_index
        self.dense_index = dense_index
        self.k = k
        
    def retrieve(self, query: str, top_n: int = 10) -> List[Dict]:
        """
        Retrieve using both sparse and dense methods.
        Combine with Reciprocal Rank Fusion.
        
        Returns:
            Sorted list of chunks with fusion score
        """
        
        # 1. Sparse retrieval (exact matching)
        sparse_results = self.sparse_index.search(query, k=self.k)
        # Expected format: [(doc_id, score), ...]
        sparse_ranked = {
            doc_id: {'rank': rank, 'score': score, 'method': 'sparse'}
            for rank, (doc_id, score) in enumerate(sparse_results)
        }
        
        # 2. Dense retrieval (semantic matching)
        dense_results = self.dense_index.search(query, k=self.k)
        # Expected format: [(doc_id, similarity), ...]
        dense_ranked = {
            doc_id: {'rank': rank, 'score': score, 'method': 'dense'}
            for rank, (doc_id, score) in enumerate(dense_results)
        }
        
        # 3. Reciprocal Rank Fusion (RRF)
        # Formula: RRF_score = Σ (1 / (k + rank))
        rrf_scores = {}
        all_doc_ids = set(sparse_ranked.keys()) | set(dense_ranked.keys())
        
        for doc_id in all_doc_ids:
            rrf_score = 0.0
            
            if doc_id in sparse_ranked:
                sparse_rank = sparse_ranked[doc_id]['rank']
                rrf_score += 1.0 / (self.k + sparse_rank)
            
            if doc_id in dense_ranked:
                dense_rank = dense_ranked[doc_id]['rank']
                rrf_score += 1.0 / (self.k + dense_rank)
            
            rrf_scores[doc_id] = rrf_score
        
        # 4. Sort by RRF score and fetch top_n
        sorted_docs = sorted(
            rrf_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        # 5. Fetch full chunk content and metadata
        results = []
        for doc_id, rrf_score in sorted_docs:
            chunk = self.dense_index.get(doc_id)  # Get full chunk
            
            # Determine how we found it
            retrieval_methods = []
            if doc_id in sparse_ranked:
                retrieval_methods.append(f"sparse (rank {sparse_ranked[doc_id]['rank']})")
            if doc_id in dense_ranked:
                retrieval_methods.append(f"dense (rank {dense_ranked[doc_id]['rank']})")
            
            results.append({
                'doc_id': doc_id,
                'content': chunk['content'],
                'metadata': chunk.get('metadata', {}),
                'rrf_score': rrf_score,
                'retrieval_methods': retrieval_methods
            })
        
        return results

# Example usage
# Assuming we have sparse and dense indices set up
hybrid = HybridRetriever(
    sparse_index=bm25_searcher,
    dense_index=chroma_db
)

results = hybrid.retrieve(
    "maximum thrust CAT 390F at 1000 meters depth", 
    top_n=10
)

for i, result in enumerate(results):
    print(f"\n{i+1}. Score: {result['rrf_score']:.3f}")
    print(f"   Methods: {', '.join(result['retrieval_methods'])}")
    print(f"   Source: {result['metadata'].get('source_doc')} p{result['metadata'].get('page_numbers')}")
    print(f"   Preview: {result['content'][:200]}...")
```

#### 3. Citation-Grounded Response Generation

```python
from typing import List, Dict
import anthropic

class CitationGroundedResponder:
    """
    Generate responses that cite retrieved chunks.
    Verify citations are actually in the source text.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        
    def generate_response(
        self, 
        query: str, 
        retrieved_chunks: List[Dict],
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict:
        """
        Generate response grounded in retrieved chunks.
        
        Args:
            query: User question
            retrieved_chunks: Results from hybrid retriever
            
        Returns:
            {
                'answer': str,
                'citations': List[Dict],
                'confidence': str,
                'unknown_parts': str (if answer is partial)
            }
        """
        
        # Build context with explicit chunk markers
        context_text = ""
        chunk_references = {}
        
        for idx, chunk in enumerate(retrieved_chunks):
            ref_id = f"[SOURCE_{idx+1}]"
            chunk_references[ref_id] = {
                'doc': chunk['metadata'].get('source_doc'),
                'pages': chunk['metadata'].get('page_numbers'),
                'section': chunk['metadata'].get('section_hierarchy'),
                'content': chunk['content']
            }
            
            context_text += f"\n\n{ref_id}\nDocument: {chunk['metadata'].get('source_doc')}\n"
            context_text += f"Pages: {chunk['metadata'].get('page_numbers')}\n"
            context_text += f"Section: {' > '.join(chunk['metadata'].get('section_hierarchy', ['Unknown']))}\n"
            context_text += f"Content:\n{chunk['content']}"
        
        # Prompt that enforces citation
        system_prompt = """You are a mining operations expert assistant.

Your task is to answer the user's question using ONLY the provided source documents.

CRITICAL RULES:
1. Every fact must be cited using [SOURCE_N] where N is the source number
2. If the answer spans multiple sources, cite each one
3. If the sources don't fully answer the question, clearly state what's unknown
4. Quote relevant parts of the source when citing
5. Do NOT use knowledge outside the provided sources
6. Rate your confidence: HIGH (sources directly address query), MEDIUM (sources partially address), LOW (sources tangentially related)

Format your response as:
- Answer with citations
- Confidence level
- Any caveats or unknown aspects"""
        
        user_message = f"""User Query: {query}

Sources:
{context_text}

Please answer the query, citing all sources used."""
        
        response = self.client.messages.create(
            model=model,
            max_tokens=1500,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        
        answer_text = response.content[0].text
        
        # Post-process: verify citations reference actual sources
        verified_answer = self._verify_citations(answer_text, chunk_references)
        
        return {
            'answer': verified_answer,
            'sources': chunk_references,
            'model': model,
            'tokens_used': response.usage.output_tokens
        }
    
    def _verify_citations(self, answer: str, chunk_references: Dict) -> str:
        """
        Check that all citations in answer match provided sources.
        Warn if citations are broken.
        """
        import re
        
        cited_sources = set(re.findall(r'\[SOURCE_\d+\]', answer))
        available_sources = set(chunk_references.keys())
        
        invalid = cited_sources - available_sources
        if invalid:
            warning = f"\n\n⚠️ WARNING: Answer cites sources {invalid} which were not in retrieval results."
            return answer + warning
        
        return answer

# Usage in a RAG pipeline
def answer_mining_question(query: str, hybrid_retriever, responder):
    """
    End-to-end: retrieve -> respond -> cite
    """
    # Step 1: Hybrid retrieval
    retrieved = hybrid_retriever.retrieve(query, top_n=10)
    
    # Step 2: Generate grounded response
    response = responder.generate_response(query, retrieved)
    
    return response

# Example
result = answer_mining_question(
    query="What is the maximum thrust for CAT 390F at 1000m depth?",
    hybrid_retriever=hybrid,
    responder=CitationGroundedResponder()
)

print(result['answer'])
# Output:
# According to the CAT 390F technical manual [SOURCE_1], the maximum thrust at 
# 1000 meters depth is 45,000 PSI (page 47, Equipment Specs > Drilling Parameters).
# This assumes standard operating conditions and fluid pressure of 2,500 PSI [SOURCE_1].
# 
# Confidence: HIGH
# Sources used:
# - SOURCE_1: CAT_390F_Manual.pdf pages 47-48
```

### Design Decisions & Why

**1. Why Hybrid Instead of Pure Semantic?**
- Mining equipment has model numbers (CAT 390F, Komatsu D375) that are meaningless to embeddings
- Safety regulations reference legal codes that need exact matching
- Hybrid gives both precision (BM25) and understanding (embeddings)
- Fallback: if one method fails, the other still helps

**2. Why Structure-Preserving Chunking?**
- Equipment specs have tables and lists—naive token splitting breaks them
- Safety procedures are sequential—order matters
- Keeping section hierarchy lets us filter by procedure type later
- Allows better audit trails (cite the exact section)

**3. Why Reciprocal Rank Fusion?**
- Simple average of scores doesn't work (BM25 and embedding scores have different scales)
- RRF is scale-invariant: a document's rank matters, not the absolute score
- If both methods agree, confidence rises naturally
- Easy to implement and explainable to engineers

**4. Why Citation Verification?**
- Safety-critical domain: wrong citations could lead to accidents
- LLMs hallucinate citations, so we verify they actually exist
- Engineers need to follow up and update outdated docs
- Audit trail: track what source was used for each decision

### Key Takeaways

1. **Retrieval strategy is problem-dependent**: pure semantic search fails on specialized domains with terminology constraints.

2. **Hybrid retrieval solves the mismatch**: combine sparse (exact matching) and dense (semantic understanding). Use RRF to fuse them intelligently.

3. **Preserve document structure**: don't just chunk on token limits. Mining manuals have sections, procedures, diagrams—honor that in chunking.

4. **Citations are not optional**: especially for safety-critical domains. Verify that citations match the sources and let users audit the reasoning.

5. **Metadata is valuable**: section hierarchy, page numbers, and source doc names are cheap to track and essential for traceability.

---

## Case Study 2: Core Marine — Production RAG On-Premise with Local LLMs

### The Business Problem

Core Marine provides offshore engineering services. Their 1TB documentation library includes:
- Subsea installation procedures (BOP stacks, manifolds, umbilicals)
- Structural analysis reports for jacket platforms
- Compliance guides (DNV, ABS, API standards)
- Historical failure analysis and lessons learned
- Design drawings and CAD specifications

**The constraint**: Data cannot leave the premises. Regulatory requirements (offshore energy standards, client contracts, NDAs) forbid cloud storage. Engineers need instant access to this knowledge during field operations, often with poor internet.

Core Marine initially considered a cloud RAG pipeline but hit a wall: regulatory compliance made it impossible. They pivoted to **on-premise, local LLM-based RAG** using:
- **Ollama** for running open-weight LLMs locally (Llama 2, Mistral)
- **ChromaDB** for vector storage
- **Azure Blob** for document storage (on-premise Azure Stack)

The tradeoff: local LLMs are slower (inference latency ~3-5s vs 0.5s for cloud) and lower quality than frontier models, but they work offline and satisfy compliance.

### Why This Pattern Fits

When data sovereignty and compliance are absolute requirements, on-premise RAG with local inference is the only option. The pattern answers:

- **Where do I store vectors?** Local database (ChromaDB, Milvus, Weaviate)
- **What LLM do I run?** Open weights: Llama 2 13B/70B, Mistral 7B, Qwen
- **How do I accept the quality/latency tradeoff?** Domain-specific fine-tuning, careful prompt engineering, asynchronous processing

The RAG quality gap closes when:
- Your domain is well-defined (offshore engineering, not general knowledge)
- You fine-tune retrieval (domain-specific chunking, metadata filtering)
- You prompt carefully (few-shot examples from your domain)

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    On-Premise Infrastructure                  │
│                                                               │
│  ┌────────────────┐         ┌──────────────────────┐        │
│  │  Azure Blob    │         │  ChromaDB            │        │
│  │  (On-Premise   │         │  Vector Database     │        │
│  │   Stack)       │         │                      │        │
│  │                │         │  • Embeddings        │        │
│  │  • .pdf files  │         │  • Metadata indexes  │        │
│  │  • .docx docs  │         │  • Similarity search │        │
│  │  • Drawings    │         │                      │        │
│  │  • CAD specs   │         └──────────────────────┘        │
│  └────────────────┘                                         │
│         ▲                              ▲                     │
│         │ (fetch doc)                  │ (vector search)     │
│         │                              │                     │
└─────────┼──────────────────────────────┼────────────────────┘
          │                              │
          └──────────────┬───────────────┘
                         │
              ┌──────────▼───────────┐
              │   Ollama Server      │
              │   (Local Inference)  │
              │                      │
              │  • Llama 2 70B       │
              │  • Running on GPU    │
              │  • Port 11434        │
              └──────────┬───────────┘
                         │
         ┌───────────────▼───────────────┐
         │   Engineer Query              │
         │   (Field or Office)           │
         │                               │
         │  "What's the procedure for    │
         │   BOP stack installation?"    │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼────────────────────┐
         │  RAG Pipeline                      │
         │                                    │
         │  1. Embed query (Ollama emb)       │
         │  2. Search ChromaDB (~100ms)       │
         │  3. Fetch full docs from Blob      │
         │  4. Generate response (Ollama)     │
         │     (inference time: ~3-5s)        │
         │  5. Return to engineer             │
         └────────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Local Vector Embedding Pipeline

```python
import requests
import json
from typing import List
import time

class OllamaEmbedder:
    """
    Generate embeddings using Ollama running locally.
    
    Ollama exposes a REST API for embedding generation.
    Model: Llama 2 or embedding-specific model (e.g., nomic-embed-text)
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        base_url: Ollama server URL (default local)
        """
        self.base_url = base_url
        self.model = "nomic-embed-text"  # Smaller, efficient embedder
        self.embedding_dim = 768
        
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text chunk.
        
        Returns:
            768-dimensional embedding vector
        """
        payload = {
            "model": self.model,
            "prompt": text
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['embedding']
            
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"Cannot connect to Ollama at {self.base_url}. "
                "Ensure Ollama is running: ollama serve"
            )
        except requests.exceptions.Timeout:
            raise RuntimeError("Embedding request timed out (>30s)")
    
    def embed_batch(self, texts: List[str], batch_size: int = 10) -> List[List[float]]:
        """
        Embed multiple texts, with progress tracking.
        
        Batching avoids overwhelming local resources.
        """
        embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            
            for text in batch:
                embedding = self.embed_text(text)
                embeddings.append(embedding)
            
            # Progress
            completed = min(i + batch_size, len(texts))
            print(f"Embedded {completed}/{len(texts)} chunks")
            
            # Small delay to avoid resource spike
            time.sleep(0.5)
        
        return embeddings

# Usage during document ingestion
class DocumentIngestionPipeline:
    """
    End-to-end: read -> chunk -> embed -> store
    """
    
    def __init__(self, chroma_db, ollama_embedder):
        self.db = chroma_db  # ChromaDB collection
        self.embedder = ollama_embedder
        
    def ingest_pdf(self, pdf_path: str, document_type: str = "procedure"):
        """
        Load PDF, chunk it, embed chunks, store in ChromaDB.
        """
        import pypdf
        
        reader = pypdf.PdfReader(pdf_path)
        chunks = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            
            # Simple chunking (production would be more sophisticated)
            for i in range(0, len(text), 500):
                chunk_text = text[i:i+500]
                chunks.append({
                    'text': chunk_text,
                    'source': pdf_path,
                    'page': page_num + 1,
                    'type': document_type
                })
        
        print(f"Created {len(chunks)} chunks from {pdf_path}")
        
        # Embed all chunks
        chunk_texts = [c['text'] for c in chunks]
        embeddings = self.embedder.embed_batch(chunk_texts)
        
        # Store in ChromaDB
        for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            self.db.add(
                ids=[f"{document_type}_{idx}"],
                embeddings=[embedding],
                documents=[chunk['text']],
                metadatas=[{
                    'source': chunk['source'],
                    'page': chunk['page'],
                    'type': chunk['type']
                }]
            )
        
        print(f"Stored {len(chunks)} chunks in ChromaDB")

# Setup
import chromadb

chroma_client = chromadb.HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection(
    name="offshore_engineering",
    metadata={"hnsw:space": "cosine"}
)

embedder = OllamaEmbedder()
pipeline = DocumentIngestionPipeline(collection, embedder)

# Ingest a procedure document
pipeline.ingest_pdf(
    "docs/BOP_Installation_Procedure.pdf",
    document_type="procedure"
)
```

#### 2. Local LLM Inference with Response Streaming

```python
import requests
import json
from typing import Generator

class OllamaResponder:
    """
    Generate responses using local LLM via Ollama.
    
    Supports streaming for better UX during 3-5s inference time.
    """
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama2"  # 70B for quality, 13B for speed
        
    def query(
        self, 
        query: str, 
        context: str,
        temperature: float = 0.3
    ) -> str:
        """
        Generate response to query given context.
        Blocks until complete (non-streaming).
        """
        prompt = f"""You are an offshore engineering expert. Answer the user's question 
based ONLY on the provided context. If the context doesn't answer the question, 
say "I don't have information about this in the available documents."

Context:
{context}

User Query: {query}

Answer:"""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['response']
            
        except requests.exceptions.Timeout:
            return "ERROR: Response generation timed out (>30s). Local LLM may be overloaded."
    
    def query_streaming(
        self, 
        query: str, 
        context: str,
        temperature: float = 0.3
    ) -> Generator[str, None, None]:
        """
        Stream response tokens as they're generated.
        
        Yields:
            Individual tokens as strings
        
        Usage:
            for token in responder.query_streaming(query, context):
                print(token, end='', flush=True)
        """
        prompt = f"""You are an offshore engineering expert. Answer the user's question 
based ONLY on the provided context. If the context doesn't answer the question, 
say "I don't have information about this in the available documents."

Context:
{context}

User Query: {query}

Answer:"""
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=120,
                stream=True
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    yield chunk['response']
                    
        except requests.exceptions.Timeout:
            yield "ERROR: Response generation timed out."

# RAG with local inference
class OnPremiseRAG:
    """
    Complete on-premise RAG: retrieve from ChromaDB, respond via Ollama.
    """
    
    def __init__(self, chroma_collection, ollama_responder, embedder):
        self.collection = chroma_collection
        self.responder = ollama_responder
        self.embedder = embedder
    
    def answer(self, query: str, num_results: int = 5) -> str:
        """
        Full RAG loop: embed query -> search -> generate -> return
        """
        # 1. Embed query
        query_embedding = self.embedder.embed_text(query)
        
        # 2. Search ChromaDB
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=num_results
        )
        
        # 3. Build context from results
        context_parts = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            source = metadata.get('source', 'Unknown')
            page = metadata.get('page', '?')
            context_parts.append(f"[{source}, p{page}]\n{doc}")
        
        context = "\n\n".join(context_parts)
        
        # 4. Generate response
        answer = self.responder.query(query, context)
        
        return answer

# Setup and test
rag = OnPremiseRAG(
    chroma_collection=collection,
    ollama_responder=OllamaResponder(),
    embedder=embedder
)

# Example query
response = rag.answer("What is the procedure for installing a BOP stack subsea?")
print(response)
```

#### 3. Document Ingestion Pipeline for Massive Volumes

```python
import os
import glob
from pathlib import Path
from typing import List
import json

class MassDocumentIngestion:
    """
    Handle 1TB+ of documents:
    - PDFs, DOCXs, drawings
    - Parallel processing to speed up ingestion
    - Checkpoint/resume for fault tolerance
    """
    
    def __init__(self, rag_pipeline, checkpoint_file: str = "ingestion_checkpoint.json"):
        self.rag = rag_pipeline
        self.checkpoint_file = checkpoint_file
        self.processed_files = self._load_checkpoint()
        
    def _load_checkpoint(self) -> set:
        """
        Resume from previous run if interrupted.
        """
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file) as f:
                data = json.load(f)
                return set(data.get('processed_files', []))
        return set()
    
    def _save_checkpoint(self):
        """
        Periodically save progress.
        """
        with open(self.checkpoint_file, 'w') as f:
            json.dump({
                'processed_files': list(self.processed_files),
                'total_processed': len(self.processed_files)
            }, f, indent=2)
    
    def ingest_directory(self, directory: str, num_workers: int = 4):
        """
        Ingest all documents in a directory.
        
        Uses multiprocessing for parallel embedding.
        """
        from multiprocessing import Pool
        import time
        
        # Find all documents
        file_patterns = ['**/*.pdf', '**/*.docx', '**/*.txt']
        all_files = []
        
        for pattern in file_patterns:
            all_files.extend(glob.glob(os.path.join(directory, pattern), recursive=True))
        
        # Filter already processed
        files_to_process = [
            f for f in all_files 
            if f not in self.processed_files
        ]
        
        print(f"Found {len(all_files)} total files, {len(files_to_process)} to process")
        
        # Process in parallel
        start_time = time.time()
        
        for idx, file_path in enumerate(files_to_process):
            try:
                self._process_file(file_path)
                self.processed_files.add(file_path)
                
                # Checkpoint every 100 files
                if (idx + 1) % 100 == 0:
                    self._save_checkpoint()
                    elapsed = time.time() - start_time
                    rate = (idx + 1) / elapsed
                    remaining = (len(files_to_process) - idx - 1) / rate if rate > 0 else 0
                    print(f"Processed {idx+1}/{len(files_to_process)} "
                          f"({rate:.1f} files/sec, ~{remaining/60:.0f}min remaining)")
                
            except Exception as e:
                print(f"ERROR processing {file_path}: {e}")
                continue
        
        self._save_checkpoint()
        print(f"Ingestion complete. Processed {len(self.processed_files)} files.")
    
    def _process_file(self, file_path: str):
        """
        Extract text from file and ingest into RAG.
        Handles PDFs, DOCX, and plain text.
        """
        import PyPDF2
        from docx import Document
        
        if file_path.endswith('.pdf'):
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = "".join(page.extract_text() for page in reader.pages)
                doc_type = "pdf"
                
        elif file_path.endswith('.docx'):
            doc = Document(file_path)
            text = "\n".join(p.text for p in doc.paragraphs)
            doc_type = "docx"
            
        elif file_path.endswith('.txt'):
            with open(file_path) as f:
                text = f.read()
            doc_type = "txt"
        else:
            return
        
        # Ingest
        if len(text) > 100:  # Skip empty files
            self.rag.ingest_document(
                content=text,
                source=file_path,
                doc_type=doc_type
            )

# Usage: ingest entire directory
ingestion = MassDocumentIngestion(rag)
ingestion.ingest_directory("/data/offshore_engineering_docs")
```

### Design Decisions & Why

**1. Why On-Premise Instead of Cloud?**
- Regulatory compliance (data sovereignty) is non-negotiable in offshore energy
- Client NDAs forbid data transmission outside premises
- Field operations often have poor internet (local-first is safer)
- Tradeoff: latency (3-5s vs 0.5s) and quality (Llama 2 vs Claude) are acceptable

**2. Why ChromaDB?**
- Lightweight, no external dependencies (vs Pinecone, Weaviate)
- Runs on modest hardware (engineers' laptops or edge servers)
- HTTP API for easy integration
- Supports metadata filtering (by document type, source, etc.)

**3. Why Ollama for Inference?**
- Single command to run any open-weight model
- Handles VRAM management and offloading
- REST API makes it language-agnostic
- Can switch models (Llama 2 → Mistral) without code changes

**4. Why Stream Responses?**
- 3-5s latency is noticeable. Streaming shows progress immediately.
- Engineers see tokens appearing in real-time, reducing perceived wait.
- Can display partial answers while generation completes.

**5. Why Checkpoint/Resume for Ingestion?**
- 1TB of documents = 8+ hours of embedding on modest hardware
- Network/power failures can interrupt. Checkpoints let you resume.
- Don't re-embed files you've already processed.

### Key Takeaways

1. **On-premise RAG is viable when compliance demands it**: local embeddings (Ollama) + vector DB (ChromaDB) + local LLM gives a working system.

2. **Embrace the quality/latency tradeoff**: Llama 2 is 5x slower than Claude but works offline and keeps data local. Domain-specific fine-tuning and prompt engineering close the gap.

3. **Streaming is essential for UX**: 3-5s inference is acceptable if users see progress. Non-streaming feels broken.

4. **Checkpointing saves your sanity**: Ingesting 1TB is slow. Crashes kill momentum. Save progress every 100 files.

5. **Metadata filtering is cheap and powerful**: filter by doc type, source, page number. Lets you build specialized RAG (e.g., safety-only mode).

---

## Case Study 3: eSpark — Teacher Assistant for K-5 Curriculum Alignment

### The Business Problem

eSpark Learning provides adaptive K-5 instruction. Teachers assign activities to students; the system tracks progress and recommends next steps. Teachers also need curriculum guidance:

- "Which activities align with 3rd grade math standards for division?"
- "What's a good scaffolding sequence for fractions (6-step progression)?"
- "Which activities meet Common Core and Texas essential knowledge?"

Each US state publishes different standards. Common Core applies to ~45 states; others (Texas, California, Virginia) have unique standards. **The corpus is structured**: standards documents are organized by grade, domain, and standard code (e.g., `CCSS.Math.3.OA.A.1`).

eSpark built RAG over this structured corpus. But standard semantic search fails: "division by groups" is semantically different from "3.OA.A.2" (the actual standard code), yet they mean the same thing. The retrieval strategy had to account for structure.

### Why This Pattern Fits

When your corpus is **highly structured** (standards documents, specification tables, taxonomies), pure semantic search breaks down. You need:

1. **Metadata filtering**: fast, deterministic filtering by grade/domain
2. **Hybrid retrieval**: semantic understanding + exact code matching
3. **Structured query parsing**: decompose "Which activities for division in grade 3?" into:
   - Grade: 3
   - Domain: Math
   - Standard code: 3.OA.A (not 3.OA.B)

This is different from Rio Tinto (mining docs are semi-structured) and Core Marine (open-ended queries). Here, the structure is the retrieval backbone.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│        Teacher Query                                │
│   "Activities for division, grade 3?"               │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼──────────────┐
         │  Query Parser            │
         │                          │
         │  Extract:                │
         │  - grade: 3              │
         │  - domain: Math          │
         │  - concept: division     │
         │  - state: (default)      │
         └───────────┬──────────────┘
                     │
        ┌────────────▼────────────────────┐
        │  Metadata Filter                │
        │  (Deterministic)                │
        │                                 │
        │  SELECT standards WHERE         │
        │  grade = 3 AND                  │
        │  domain = 'Math' AND            │
        │  state = 'Common Core'          │
        │  → Reduces search space 100x    │
        └────────────┬───────────────────┘
                     │
        ┌────────────▼─────────────────────┐
        │ Semantic Search (limited set)    │
        │                                  │
        │ Search for "division" in         │
        │ 3rd grade math standards         │
        │ → Top 5 standards                │
        └────────────┬────────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │ Combine with Exact Matching   │
        │                               │
        │ Standards containing:         │
        │ - "3.OA.A.2" (direct code)    │
        │ - "division" (semantic)       │
        │ - "groups" (concept)          │
        │ → Deduplicate & rank          │
        └────────────┬──────────────────┘
                     │
        ┌────────────▼──────────────────────┐
        │ Fetch Full Standard Context      │
        │                                  │
        │ Standard Code: 3.OA.A.2          │
        │ Domain: Operations & Algebraic  │
        │ Grade: 3                        │
        │ Standard: "Interpret whole-     │
        │  number quotients..."           │
        │ Learning Progressions: [2.OA.X, │
        │  3.OA.A.2, 4.OA.A.1]           │
        └────────────┬──────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │ Search Activities Database     │
        │                               │
        │ Find activities tagged with   │
        │ standard 3.OA.A.2            │
        │ → Return top activities      │
        └────────────┬──────────────────┘
                     │
        ┌────────────▼──────────────────┐
        │ Generate Response             │
        │                               │
        │ Synthesize: which activities  │
        │ meet the standard, what's the │
        │ learning progression          │
        └──────────────────────────────┘
```

### Implementation: Key Components

#### 1. Structured Standards Ingestion

```python
import json
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Standard:
    """
    Represents a single curriculum standard.
    """
    code: str                    # e.g., "CCSS.Math.3.OA.A.2"
    state: str                   # e.g., "Common Core", "Texas", "California"
    grade: int                   # e.g., 3
    domain: str                  # e.g., "Operations & Algebraic Thinking"
    cluster: str                 # e.g., "Represent and solve problems..."
    standard_text: str           # Full standard description
    components: List[str]        # Key concepts (e.g., ["division", "quotients"])
    learning_progression: List[str]  # Related standards (prior/next grades)

class StandardsCorpusLoader:
    """
    Load structured standards data from JSON.
    
    Expected format:
    {
        "state": "Common Core",
        "standards": [
            {
                "code": "CCSS.Math.3.OA.A.2",
                "grade": 3,
                "domain": "Operations & Algebraic Thinking",
                ...
            }
        ]
    }
    """
    
    def __init__(self):
        self.standards_by_state = {}
        self.standards_by_grade = {}
        self.standards_by_code = {}
        self.all_standards: List[Standard] = []
    
    def load_from_json(self, json_path: str) -> List[Standard]:
        """
        Load standards from JSON file.
        Build indexes for fast lookup.
        """
        with open(json_path) as f:
            data = json.load(f)
        
        state = data['state']
        standards = []
        
        for std_dict in data.get('standards', []):
            standard = Standard(
                code=std_dict['code'],
                state=state,
                grade=std_dict['grade'],
                domain=std_dict['domain'],
                cluster=std_dict.get('cluster', ''),
                standard_text=std_dict['standard_text'],
                components=std_dict.get('components', []),
                learning_progression=std_dict.get('learning_progression', [])
            )
            standards.append(standard)
            
            # Index for fast lookup
            self.standards_by_code[standard.code] = standard
            
            if state not in self.standards_by_state:
                self.standards_by_state[state] = []
            self.standards_by_state[state].append(standard)
            
            if standard.grade not in self.standards_by_grade:
                self.standards_by_grade[standard.grade] = []
            self.standards_by_grade[standard.grade].append(standard)
        
        self.all_standards.extend(standards)
        return standards
    
    def get_by_metadata(
        self,
        state: str = None,
        grade: int = None,
        domain: str = None
    ) -> List[Standard]:
        """
        Fast metadata-based filtering.
        
        Returns standards matching all specified criteria.
        """
        results = self.all_standards
        
        if state:
            results = [s for s in results if s.state == state]
        
        if grade is not None:
            results = [s for s in results if s.grade == grade]
        
        if domain:
            results = [s for s in results if s.domain == domain]
        
        return results

# Usage
loader = StandardsCorpusLoader()
loader.load_from_json("standards/common_core_math.json")
loader.load_from_json("standards/texas_math.json")

# Fast lookups
grade_3_math = loader.get_by_metadata(grade=3, domain="Operations & Algebraic Thinking")
print(f"Found {len(grade_3_math)} standards for grade 3 operations")
```

#### 2. Hybrid Query Parsing

```python
import re
from typing import Optional, Dict, List

class StructuredQueryParser:
    """
    Parse natural language queries into structured metadata filters.
    
    Example:
        "Activities for division in grade 3, Common Core"
        → {
            'grade': 3,
            'domains': ['Operations & Algebraic Thinking'],
            'concepts': ['division'],
            'state': 'Common Core'
        }
    """
    
    GRADE_PATTERN = r'\b(?:grade|level)\s+([K1-5]|kindergarten|[1-5](?:st|nd|rd|th)?)\b'
    GRADE_MAP = {
        'k': 0, 'kindergarten': 0,
        '1': 1, '1st': 1,
        '2': 2, '2nd': 2,
        '3': 3, '3rd': 3,
        '4': 4, '4th': 4,
        '5': 5, '5th': 5,
    }
    
    DOMAIN_KEYWORDS = {
        'operations': 'Operations & Algebraic Thinking',
        'algebraic': 'Operations & Algebraic Thinking',
        'number sense': 'Number & Operations in Base Ten',
        'fractions': 'Number & Operations - Fractions',
        'measurement': 'Measurement & Data',
        'geometry': 'Geometry',
    }
    
    STATE_MAP = {
        'common core': 'Common Core',
        'texas': 'Texas',
        'california': 'California',
    }
    
    def __init__(self):
        pass
    
    def parse(self, query: str) -> Dict:
        """
        Extract metadata from query.
        
        Returns:
            {
                'grade': int or None,
                'domains': List[str],
                'concepts': List[str],
                'state': str or None
            }
        """
        query_lower = query.lower()
        
        # Extract grade
        grade = None
        grade_match = re.search(self.GRADE_PATTERN, query_lower)
        if grade_match:
            grade_str = grade_match.group(1).lower()
            grade = self.GRADE_MAP.get(grade_str)
        
        # Extract state
        state = None
        for state_query, state_name in self.STATE_MAP.items():
            if state_query in query_lower:
                state = state_name
                break
        
        # Extract domains
        domains = []
        for keyword, domain_name in self.DOMAIN_KEYWORDS.items():
            if keyword in query_lower:
                domains.append(domain_name)
        
        # Extract concepts (remaining important nouns)
        # For simplicity, use a static list; production would use NLP
        concept_keywords = [
            'division', 'multiplication', 'addition', 'subtraction',
            'fractions', 'decimals', 'geometry', 'area', 'perimeter',
            'measurement', 'graphs', 'data', 'patterns'
        ]
        
        concepts = []
        for concept in concept_keywords:
            if concept in query_lower:
                concepts.append(concept)
        
        return {
            'grade': grade,
            'domains': domains,
            'concepts': concepts,
            'state': state or 'Common Core',  # Default to Common Core
            'original_query': query
        }

# Usage
parser = StructuredQueryParser()

parsed = parser.parse("Activities for division in grade 3, Common Core")
print(parsed)
# {
#   'grade': 3,
#   'domains': ['Operations & Algebraic Thinking'],
#   'concepts': ['division'],
#   'state': 'Common Core',
#   'original_query': '...'
# }
```

#### 3. Metadata-Filtered Semantic Search

```python
from typing import List
import numpy as np

class StructuredStandardsRetriever:
    """
    Retrieve standards using metadata filters + semantic search.
    
    Dramatically reduces search space before semantic matching.
    """
    
    def __init__(self, embedder, standards_loader, query_parser):
        self.embedder = embedder
        self.loader = standards_loader
        self.parser = query_parser
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ) -> List[Dict]:
        """
        End-to-end: parse -> filter -> search -> rank
        """
        
        # 1. Parse query into structured metadata
        parsed = self.parser.parse(query)
        print(f"Parsed query: {parsed}")
        
        # 2. Metadata filtering (deterministic, fast)
        candidates = self.loader.all_standards
        
        if parsed['grade'] is not None:
            candidates = [s for s in candidates if s.grade == parsed['grade']]
            print(f"After grade filter: {len(candidates)} standards")
        
        if parsed['state']:
            candidates = [s for s in candidates if s.state == parsed['state']]
            print(f"After state filter: {len(candidates)} standards")
        
        if parsed['domains']:
            candidates = [
                s for s in candidates
                if s.domain in parsed['domains']
            ]
            print(f"After domain filter: {len(candidates)} standards")
        
        # 3. Semantic search within filtered candidates
        if len(candidates) == 0:
            print("No candidates after filtering. Expanding search...")
            candidates = self.loader.all_standards
        
        # Embed query
        query_embedding = self.embedder.embed_text(query)
        
        # Score each candidate
        scored = []
        for standard in candidates:
            # Combine standard code and text for matching
            standard_embedding_text = f"{standard.code}: {standard.standard_text}"
            standard_embedding = self.embedder.embed_text(standard_embedding_text)
            
            # Cosine similarity
            similarity = np.dot(query_embedding, standard_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(standard_embedding)
            )
            
            # Bonus if exact concept match
            concept_bonus = 0.0
            for concept in parsed['concepts']:
                if concept in standard_embedding_text.lower():
                    concept_bonus += 0.2
            
            final_score = similarity + concept_bonus
            
            scored.append({
                'standard': standard,
                'semantic_score': similarity,
                'concept_bonus': concept_bonus,
                'final_score': final_score
            })
        
        # 4. Sort and return top_k
        results = sorted(scored, key=lambda x: x['final_score'], reverse=True)[:top_k]
        
        return [
            {
                'code': r['standard'].code,
                'grade': r['standard'].grade,
                'domain': r['standard'].domain,
                'text': r['standard'].standard_text,
                'components': r['standard'].components,
                'score': r['final_score'],
                'learning_progression': r['standard'].learning_progression
            }
            for r in results
        ]

# Usage
retriever = StructuredStandardsRetriever(
    embedder=embedder,
    standards_loader=loader,
    query_parser=parser
)

results = retriever.retrieve("Activities for division in grade 3")
for result in results:
    print(f"{result['code']}: {result['text'][:100]}...")
    print(f"  Score: {result['score']:.3f}\n")
```

#### 4. Learning Progression & Activity Mapping

```python
from typing import List, Dict

class CurriculumAlignmentService:
    """
    Map standards to activities.
    Show learning progressions.
    """
    
    def __init__(self, standards_loader, activity_db):
        self.loader = standards_loader
        self.activities = activity_db  # Dict: standard_code → List[Activity]
    
    def get_learning_progression(self, standard_code: str) -> Dict:
        """
        Show how a standard builds across grades.
        
        Returns:
            {
                'prior': List[Standard],   # Previous grade/level
                'current': Standard,
                'next': List[Standard]     # Next grade/level
            }
        """
        current = self.loader.standards_by_code.get(standard_code)
        if not current:
            return None
        
        # Parse progression from standard's learning_progression field
        prior = []
        next_standards = []
        
        for related_code in current.learning_progression:
            related = self.loader.standards_by_code.get(related_code)
            if related:
                if related.grade < current.grade:
                    prior.append(related)
                else:
                    next_standards.append(related)
        
        return {
            'prior': sorted(prior, key=lambda s: s.grade),
            'current': current,
            'next': sorted(next_standards, key=lambda s: s.grade)
        }
    
    def get_activities_for_standard(
        self,
        standard_code: str,
        limit: int = 10
    ) -> List[Dict]:
        """
        Return activities aligned to a standard.
        """
        activities = self.activities.get(standard_code, [])
        return activities[:limit]
    
    def generate_curriculum_guide(
        self,
        standard_code: str
    ) -> str:
        """
        Generate teacher-friendly guide for a standard.
        Includes progression, activities, scaffolding.
        """
        progression = self.get_learning_progression(standard_code)
        if not progression:
            return f"Standard {standard_code} not found."
        
        guide = f"""
## {progression['current'].code}
**Standard**: {progression['current'].standard_text}

### Learning Progression
"""
        
        if progression['prior']:
            guide += "\n**Prior Grade(s)**:\n"
            for std in progression['prior']:
                guide += f"  - Grade {std.grade}: {std.code}\n"
        
        guide += f"\n**This Grade**: Grade {progression['current'].grade}\n"
        
        if progression['next']:
            guide += "\n**Next Grade(s)**:\n"
            for std in progression['next']:
                guide += f"  - Grade {std.grade}: {std.code}\n"
        
        ### Activities
        activities = self.get_activities_for_standard(standard_code)
        if activities:
            guide += f"\n### Recommended Activities ({len(activities)})\n"
            for activity in activities[:5]:  # Show top 5
                guide += f"  - **{activity['title']}** (Level {activity['level']})\n"
        
        return guide

# Usage
alignment = CurriculumAlignmentService(loader, activity_database)

guide = alignment.generate_curriculum_guide("CCSS.Math.3.OA.A.2")
print(guide)
```

### Design Decisions & Why

**1. Why Metadata Filtering Before Semantic Search?**
- Standards corpus is highly structured. Grade and domain are deterministic.
- Filtering reduces search space 10-100x before embedding (much faster).
- Avoids cross-grade confusion (division in grade 3 is different from grade 4).

**2. Why Parse Query to Structured Form?**
- Teachers think in metadata: "grade 3 math". Parsing extracts that naturally.
- Allows fallback: if semantic search fails, metadata still guides you.
- Explainable: shows teacher what filters were applied.

**3. Why Learn Progressions Matter?**
- Teachers need context: "What did they learn last year? What comes next?"
- Shows scaffolding sequence (prerequisites and follow-up).
- Prevents assigning activities misaligned with prior knowledge.

**4. Why Activity Mapping?**
- Standards without activities are useless. Link them immediately.
- Activities are the real artifact teachers use; standards are reference.
- Closing the loop: standard → activities → assign to student.

### Key Takeaways

1. **Structured corpus needs structured retrieval**: metadata filtering is faster and more accurate than pure semantic search.

2. **Query parsing bridges natural language and structure**: parse "grade 3 division" to `{grade: 3, concepts: ['division']}` then filter deterministically.

3. **Hybrid: metadata + semantic**: combine fast filtering with semantic understanding. If metadata filtering fails, semantic search expands the result set.

4. **Learning progressions are essential context**: show teachers what came before and comes next. Prevents gaps and misalignment.

5. **Link standards to artifacts**: a standard without activities is just reference material. Make the connection explicit and bidirectional.

---

## Query to Structure Parsing Extracting structured metadata grade level domain con

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Reciprocal Rank Fusion RRF A rank merging algorithm scoring each document as 1kr

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Structure Aware Chunking Chunking strategy that respects document hierarchy chap

## Core Principle

Simple RAG agents must match retrieval strategy to corpus shape: hybrid BM25 + dense retrieval with RRF for specialized domains with exact-term requirements, metadata-first filtering for structured corpora, and structure-aware chunking to preserve traceability. The central principle is that retrieval strategy is problem-specific — no single approach generalizes across corpus types. Citation grounding, query parsing, and learning progressions are not optional enhancements but core requirements for agents operating in safety-critical or high-precision domains.

## Key Heuristics

These are the load-bearing rules for this concept.

> Retrieval strategy is problem-specific. What works for general questions breaks for domain terminology. What works for unstructured prose fails on structured standards.

> Sparse (BM25) excels at exact term matching: equipment model numbers, procedure names, safety code references.

> Dense (embeddings) captures semantic understanding: 'maximum thrust at depth' even if phrased differently.

> If both agree, confidence rises; if only one retrieves, it still ranks.

> Structured corpus needs structured retrieval: metadata filtering is faster and more accurate than pure semantic search.

> Query parsing bridges natural language and structure: parse 'grade 3 division' to {grade: 3, concepts: ['division']} then filter deterministically.

> A standard without activities is just reference material. Make the connection explicit and bidirectional.

> Naive chunking on token limits destroys structure.

## Anti-Patterns & Fixes

- Pure Semantic Search on Specialized Domains: Embedding models conflate domain-specific terms (e.g., 'ore grade' matched to 'grading system'), returning irrelevant results for 30% of queries. Fix: Use hybrid retrieval (BM25 + dense embeddings + RRF) so exact terms are matched lexically while semantic understanding handles paraphrasing.
- Token-Limit Chunking: Splitting documents purely on character/token count destroys section hierarchy, making it impossible to trace answers to their source location. Fix: Use structure-aware chunking that respects headers, sections, and subsections and preserves page numbers and hierarchy metadata.
- Semantic-Only Search on Structured Corpora: Using pure vector search on a corpus with deterministic metadata fields (grade, domain, code) causes cross-grade confusion and is unnecessarily slow. Fix: Apply metadata filtering first to reduce search space, then apply semantic search only within the filtered set.
- Uncited LLM Responses in Safety-Critical Domains: Generating answers without source attribution leaves engineers unable to verify or update information, creating liability. Fix: Require the LLM to cite exact document name, section, and page number for every factual claim.
- Ignoring Learning Progressions in Educational RAG: Returning a standard in isolation without prior/next grade context causes teachers to assign activities misaligned with student prior knowledge. Fix: Model and surface learning progressions explicitly, showing what standards precede and follow the retrieved one.
- Standards Without Activity Links: Returning curriculum standards without connected activities makes the system academic-only and unusable in practice. Fix: Maintain a bidirectional mapping from standard codes to concrete activities and surface them alongside the standard.

## When To Apply

Load this page when:

- Use this when building a knowledge retrieval agent over a domain-specific corpus that contains both proper nouns (model numbers, codes, procedure names) and conceptual prose, where pure semantic search returns irrelevant results.
- Use this when the corpus consists of dense structured documents (manuals, standards, regulations) and users need traceable, citable answers rather than synthesized summaries.
- Use this when a retrieval system must serve safety-critical queries where precision is more important than recall and every answer must be verifiable by a human expert.
- Use this when users express queries in natural language that contains implicit metadata (grade level, domain, equipment type) that could be parsed and used for deterministic pre-filtering.
- Use this when chunking PDFs or structured technical documents and naive token-based splitting is destroying the logical structure needed for accurate retrieval.
- Use this when two retrieval signals (sparse and dense) are available and need to be merged without discarding results that only one method found.
- Use this when building an educational or curriculum-aligned agent that needs to show context about what comes before and after a retrieved item in a learning sequence.
- Use this when a RAG MVP has already failed on a specialized corpus and the diagnosis is that semantic embeddings do not capture domain-specific terminology accurately.

## Concrete Examples

- Rio Tinto mining knowledge assistant: hybrid RAG over 50+ technical manuals, safety regulations, and equipment specs for 10,000+ engineers, using BM25 + dense embeddings + RRF with citation grounding to page number.
- Educational curriculum alignment system: metadata-filtered retrieval over structured standards (e.g., CCSS.Math.3.OA.A.2) with query parsing to extract grade/domain/concept, learning progression mapping, and activity linking for teachers.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Simple RAG Agents**

An LLM coding agent generating RAG pipelines will default to pure semantic search with uniform token chunking — the simplest implementation — which systematically fails on specialized corpora with proper nouns, codes, or structured documents, causing silent precision degradation rather than obvious errors. The agent must be explicitly triggered to select retrieval strategy based on corpus shape (structured vs. unstructured, domain-specific terminology vs. general prose) rather than defaulting to a single embedding-based approach. Citation grounding is especially critical for agents: without it, an agent composing answers from retrieved chunks has no mechanism to propagate source provenance to the user, making hallucinations and stale data indistinguishable from verified facts.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
