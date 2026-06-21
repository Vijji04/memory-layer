---
title: Hierarchical Pattern: Nested orchestrators arranged like an org chart for enterprise-scale or security-isolated domains
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Multi-Agent-Orchestration.json]
contributing_chapters: ["Multi-Agent Orchestration"]
confidence: high
---

# Hierarchical Pattern: Nested orchestrators arranged like an org chart for enterprise-scale or security-isolated domains

> From chapter: *Multi-Agent Orchestration*

## Core Principle

Multi-agent systems become necessary when a task exceeds a single agent's context, requires domain specialization, benefits from parallelism, or demands failure isolation. This chapter defines five canonical orchestration patterns — Orchestrator-Worker, Sequential Pipeline, Parallel Fan-Out/In, Hierarchical, and Event-Driven — and provides a decision tree for selecting among them. Every multi-agent design must answer five coordination questions: how to decompose tasks, how agents communicate, what happens on failure, where humans intervene, and how the system is observed.

## Key Heuristics

These are the load-bearing rules for this concept.

> The question is not 'should I use multiple agents?' but 'how should they coordinate?'

> Can you draw the architecture for your own multi-agent system on paper WITHOUT AI help? If not, understand it first before going into production.

> ORCHESTRATOR_WORKER is the safe default — when in doubt, use it.

> Smaller, focused agents are easier to test and evaluate than one monolithic agent.

> If I had to ask three different experts to help me with a task, what specific thing would I ask each one to do? Write that down. That's your worker decomposition.

> When one agent is enough vs when you need multiple is an architectural choice, not a technical detail.

## Anti-Patterns & Fixes

- The LLM Fallacy: You ask AI to build your multi-agent system, it produces code that runs without errors, and you assume the architecture is sound — but at 2am a worker hangs, the orchestrator loops eating tokens, and you have no visibility because you never understood the architecture. Fix: Be able to draw your own multi-agent architecture on paper without AI help before going to production.
- Monolithic Single-Agent Overload: Putting all domain expertise, all tools, and all logic into one agent, causing context window overflow, inability to specialize, and cascading failures. Fix: Decompose into focused workers with clear input/output contracts.
- Missing Dependency Resolution: Dispatching all subtasks in arbitrary order without respecting which tasks depend on outputs from prior tasks, causing workers to run without required context. Fix: Use topological sort to establish execution order based on declared dependencies.
- No Failure Strategy: Assuming all workers succeed and having no recovery path when a worker fails, causing the whole orchestration to hang or produce incomplete results silently. Fix: Explicitly choose a failure strategy per task: retry, fallback, skip, or escalate.
- No Observability: Building a multi-agent system without traces, spans, or cost tracking, making it impossible to debug failures or runaway token consumption. Fix: Instrument every agent with traces, step timings, and per-agent cost tracking from the start.

## When To Apply

Load this page when:

- Use this when a user request naturally decomposes into subtasks requiring different domain expertise (e.g., sentiment analysis + category detection + response drafting)
- Use this when a task exceeds what fits in a single context window across all required knowledge domains simultaneously
- Use this when independent subtasks can be parallelized to reduce latency and each produces a result that must be merged into a final answer
- Use this when you need failure isolation so that one broken capability does not cascade and break unrelated parts of the pipeline
- Use this when building enterprise-scale systems where different domains require security isolation or separate ownership boundaries
- Use this when designing a system that must respond to asynchronous triggers (file uploads, webhooks, database changes) rather than a single synchronous user request
- Use this when you need to test and evaluate agent capabilities independently before integrating them into a larger system
- Use this when an orchestrator must dynamically plan subtask assignment at runtime based on the content of the user request rather than a hardcoded workflow

## Concrete Examples

- Restaurant kitchen analogy: head chef (orchestrator) delegates to grill station, prep station, and fryer (workers) then assembles the final burger
- Customer complaint email analysis: orchestrator dispatches to Sentiment Worker (returns angry/0.85), Category Worker (returns billing/refund_delay), and Response Writer (receives both results to draft reply)
- Stock investment question: plain-function orchestrator calls worker_fetch_data then worker_analyze passing the fetched data, returning a synthesized investment answer

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Multi-Agent Orchestration**

An LLM coding agent generating a multi-agent system is especially prone to the LLM Fallacy — it will produce syntactically valid, runnable code that silently lacks dependency resolution, failure handling, and observability, because those are invisible at test time. Unlike a human developer who feels the pain of debugging a hung orchestrator, an LLM agent will not self-diagnose that its generated architecture has no recovery path or topological execution order unless explicitly prompted with those requirements. To apply this chapter, an LLM agent must be given the 5 Coordination Questions as explicit generation constraints before writing any orchestration code, ensuring failure strategies, human checkpoints, and observability are baked in rather than retrofitted.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
