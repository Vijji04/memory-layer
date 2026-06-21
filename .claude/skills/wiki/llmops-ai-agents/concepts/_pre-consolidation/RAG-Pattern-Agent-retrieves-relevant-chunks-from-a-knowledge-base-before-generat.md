---
title: RAG Pattern: Agent retrieves relevant chunks from a knowledge base before generating an answer, grounding responses in evidence rather than training data alone
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Agentic-Design-Patterns.json]
contributing_chapters: ["Agentic Design Patterns"]
confidence: high
---

# RAG Pattern: Agent retrieves relevant chunks from a knowledge base before generating an answer, grounding responses in evidence rather than training data alone

> From chapter: *Agentic Design Patterns*

## Core Principle

This chapter defines the four foundational agentic design patterns — Tool Use, RAG, Planning, and Reflection — with sufficient depth to recognize, implement, and combine them. Each pattern addresses a specific LLM limitation: Tool Use adds external execution capability, RAG adds private/current knowledge, Planning adds multi-step reasoning, and Reflection adds output quality control. The core engineering skill taught is knowing which subset of patterns a given task requires, since each additional pattern increases capability at the cost of latency and complexity.

## Key Heuristics

These are the load-bearing rules for this concept.

> Without tools, an agent is just a conversationalist.

> Tools are your agent's way of doing that [using external sources like a calculator, phone, or database].

> If the LLM does not understand what a tool does, it will misuse it.

> More patterns = more power but more cost and latency.

> Retrieval grounds answers in evidence, prevents hallucination, handles knowledge cutoff.

> A planning agent explicitly reasons about the sequence of steps before executing. A tool-use agent just loops and tries things. Planning is more efficient.

> If the retriever returns wrong chunks, the agent cannot fix it.

## Anti-Patterns & Fixes

- Hallucinated Tool Calls: The LLM invents a tool name that does not exist or passes wrong argument types, causing silent failures or crashes. Fix: validate tool names and argument schemas against the registered tool list before execution.
- Tool Misuse (Write When Should Read): Agent calls a destructive or side-effecting tool (send_email, run_sql write) when only read access was intended. Fix: separate read-only and write tools explicitly, and add permission checks before execution.
- Infinite Tool Loop: Agent keeps calling tools without making progress, cycling through the same calls repeatedly. Fix: enforce step limits and detect repeated identical tool calls to break the loop.
- Whole-Document LLM Feeding: Passing an entire large document to the LLM instead of retrieved chunks, exceeding context windows and forcing the LLM to search through irrelevant content. Fix: chunk documents, embed each chunk, and retrieve only the 2-3 most relevant chunks.
- Vague Tool Schema: Tool descriptions that are too generic (e.g., 'Search' without specifying web vs. database vs. internal docs) cause the LLM to misroute calls. Fix: write precise descriptions including scope, constraints (e.g., 'read-only', 'SELECT only'), and parameter semantics.
- Single Generic Tool Instead of Specific Tools: One 'run_code' tool used for all execution contexts reduces LLM accuracy in selecting and forming calls. Fix: split into specific tools (run_python, run_sql) so the LLM has unambiguous intent signals.

## When To Apply

Load this page when:

- Use this when building an agent that needs to perform math, query a database, send messages, or call any API that the LLM cannot execute from weights alone — apply the Tool Use Pattern.
- Use this when the agent must answer questions about internal docs, post-cutoff information, or private company knowledge — apply the RAG Pattern.
- Use this when a user task requires multiple dependent steps (e.g., book flight then hotel then car) where order and conditionality matter — apply the Planning Pattern.
- Use this when the agent's output is long-form (legal brief, financial analysis) or accuracy is critical and a single LLM pass is insufficient — apply the Reflection Pattern.
- Use this when designing a tool schema and need to decide required vs. optional parameters and what the description should say to prevent LLM misuse.
- Use this when a RAG agent returns irrelevant results and you need to diagnose whether the problem is chunking strategy, embedding mismatch, or retrieval ranking.
- Use this when choosing which combination of patterns to apply to a new agent task by mapping task properties to pattern requirements.
- Use this when an agent is hitting a step limit repeatedly to determine whether the cause is an infinite loop, insufficient tools, or a planning failure.

## Concrete Examples

- Calculator tool use: user asks '847 × 392', agent generates tool call to calculator, system returns 331824, agent formats final answer — illustrating the full tool-use loop.
- Pattern selection decision tree: 'Answer FAQ about company benefits' maps to RAG only; 'Book flight and hotel' maps to TOOL_USE + PLANNING; 'Write a legal brief' maps to RAG + REFLECTION; 'Analyze quarterly financials' maps to all four patterns.
- Chunking rationale: a 100-page document split into ~40 chunks of 512 tokens each, with only 2-3 retrieved chunks passed to the LLM, versus the failure mode of passing the whole document.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Agentic Design Patterns**

An LLM coding agent generating agent systems faces a compound failure mode: it may write tool schemas with vague descriptions that cause its own downstream tool calls to misfire, or implement loops without step limits that run indefinitely in production. Unlike a human developer who notices a bad schema during manual testing, an LLM agent generating and then immediately executing its own tool definitions has no natural checkpoint — making schema validation, step caps, and explicit error-handling branches non-optional architectural requirements rather than nice-to-haves. The pattern selection framework is especially critical for an LLM agent because it prevents over-engineering (adding PLANNING overhead to a single-step task) or under-engineering (omitting REFLECTION on a legal document generation task).

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
