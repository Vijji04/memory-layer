---
title: Hybrid Retrieval Pipeline (BM25 + Dense + RRF): Combine sparse (BM25) and dense (embedding) retrieval with Reciprocal Rank Fusion and cross-encoder reranking to maximize recall and precision before generation
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Building-Your-First-Agent-Design-RAG-Evals-Guardrails.json]
contributing_chapters: ["Building Your First Agent (Design, RAG, Evals, Guardrails)"]
confidence: high
---

# Hybrid Retrieval Pipeline (BM25 + Dense + RRF): Combine sparse (BM25) and dense (embedding) retrieval with Reciprocal Rank Fusion and cross-encoder reranking to maximize recall and precision before generation

> From chapter: *Building Your First Agent (Design, RAG, Evals, Guardrails)*

## Core Principle

This chapter provides an eight-step methodology for building a first agent that begins with defining the Job To Be Done in plain English — not with framework selection — and progresses through constraint surface definition, agent pattern selection, architecture sketching, tool schema design, memory strategy, failure mode enumeration, and a three-level evaluation plan. The Course Q&A Agent (single-agent RAG over static course material) serves as the running example, demonstrating hybrid retrieval, cross-encoder reranking, QueryTrace logging, and LLM-as-judge evaluation. The core thesis is that stable problem definition and per-query trace logging are more durable investments than any particular implementation, because they enable deterministic debugging and regression testing when production failures inevitably occur.

## Key Heuristics

These are the load-bearing rules for this concept.

> Start here instead: What is the job the user is actually asking the agent to do?

> You'll write your agent code dozens of times. Your environment definition should almost never change.

> This is not a design spec yet. This is a constraint surface. It says: 'Given these inputs and these capabilities, design an agent.'

> Everything else — the architecture, the tools, the guardrails, the evals — flows from [the job].

> Store this in a JSON log or database. Every single query. When something goes wrong, you replay it.

> Traces make it possible.

> If this detail is not in the context, say 'I don't see that'

> Only answer if you have relevant context retrieved.

## Anti-Patterns & Fixes

- Framework-First Design: Picking a framework (LangChain, ReAct, tool-calling) before defining the job leads to over-engineered, fragile systems that solve the wrong problem. Fix: Write the JTBD in plain English first, then choose the simplest pattern that satisfies it.
- Technology-as-JTBD: Defining the job as 'Create a RAG system' or 'Build an LLM agent that answers questions' conflates implementation with purpose. Fix: Define JTBD by specifying user, goal, success criteria, and failure cost — never by naming a technology.
- Silent Hallucination Without Detection: Agent returns confident-sounding but incorrect information with no mechanism to catch it. Fix: Add LLM-as-judge scoring, explicit 'I don't know' prompting, lower confidence thresholds, and manual spot-checks of traces.
- No Fallback on Component Failure: When one component (e.g., embedding API) fails, the whole agent hangs because there is no timeout, fallback, or circuit breaker. Fix: Add timeouts on all external calls, fallback to sparse-only retrieval if dense fails, and circuit breakers after repeated failures.
- Context Window Overflow: Retrieving too many chunks causes prompt size to balloon (e.g., 8K to 80K tokens), spiking latency and cost. Fix: Reduce top-k, improve reranking to keep only top 1-2 chunks, and enforce token limits with truncation.
- Out-of-Scope Leakage: Agent answers questions outside its defined scope by drawing on LLM training knowledge instead of retrieved context. Fix: Add input guardrails for scope filtering, output guardrails requiring citation presence, and confidence penalties for zero-retrieval queries.

## When To Apply

Load this page when:

- Use this when starting a new agent project and unsure what to build — apply the JTBD framework before writing any code or choosing any library.
- Use this when the agent architecture needs to be chosen — match the job against the three patterns (Single-Agent RAG, Conversational Router, Narrow Action Agent) to pick the simplest fit.
- Use this when defining what the agent is allowed to do — write a formal Constraint Surface with OBSERVATIONS, ACTIONS, and FORBIDDEN sections before implementation.
- Use this when implementing retrieval for a static knowledge base — apply the hybrid BM25 + dense embedding + RRF + cross-encoder reranking pipeline with top-k=5 retrieval and top-2 reranking.
- Use this when the agent returns wrong or uncited answers in production — replay the failed QueryTrace to isolate whether the failure is in retrieval, reranking, or generation.
- Use this when preparing to ship an agent to production — run through the Production Readiness Checklist including recall >80%, accuracy >80%, latency <3s, cost <$0.05, and SLO agreement.
- Use this when an agent's answer quality degrades over time without obvious cause — check for retrieval drift by comparing current retriever recall against historical baselines and re-embed the knowledge base if needed.
- Use this when designing the logging strategy for an agent — implement QueryTrace logging for every query capturing all pipeline stages to enable deterministic debugging and regression testing.

## Concrete Examples

- Course Q&A Agent: A single-agent RAG system where students ask questions about LLMOps case studies (Uber pricing, DoorDash dispatch, Lyft matching) and receive cited answers from static course material in under 3 seconds.
- Good vs. Bad JTBD: 'A student asks about Uber's driver pricing algorithm; agent retrieves relevant section and returns concise answer with citations' (good) vs. 'Build an LLM agent that answers questions' (bad).
- Failed query replay: Debugging a failed trace for 'How does Uber's pricing work?' by sequentially re-running embedding, retrieval, reranking, and generation steps to isolate which stage degraded.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Building Your First Agent (Design, RAG, Evals, Guardrails)**

An LLM coding agent building another agent is especially prone to framework-first design because its training data is saturated with framework tutorials — it will default to scaffolding LangChain or ReAct before the JTBD is defined, producing plausible-looking but misaligned architectures. The QueryTrace schema and component-level evals are critical for an LLM agent because it cannot manually inspect intermediate outputs; structured traces and automated recall/accuracy checks are the only reliable signal that retrieval and generation are working correctly. Without explicit Constraint Surface definitions fed into the agent's context, an LLM coder will silently add tool use, external API calls, or stateful memory that violates the design requirements, creating scope creep that is hard to detect until production failures occur.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
