---
title: Orchestrator-Worker Decomposition: one planner agent breaks a complex problem into independent subproblems, dispatches each to a specialist worker, collects results, and synthesizes a final answer
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Pattern-Orchestrator-Worker.json]
contributing_chapters: ["Pattern: Orchestrator-Worker"]
confidence: high
---

# Orchestrator-Worker Decomposition: one planner agent breaks a complex problem into independent subproblems, dispatches each to a specialist worker, collects results, and synthesizes a final answer

> From chapter: *Pattern: Orchestrator-Worker*

## Core Principle

The Orchestrator-Worker pattern addresses problems too complex for a single agent by having one orchestrator decompose the query into typed WorkTasks dispatched to specialist workers, then synthesize their structured outputs into a final answer. The core engineering challenges are managing context economy (give workers only what they need), enforcing output contracts (expected_output_schema per task), and maximizing parallelism (async execution so total latency equals the critical path). A message bus decouples agents from each other, making the system extensible and testable as worker count grows.

## Key Heuristics

These are the load-bearing rules for this concept.

> Each worker needs enough context to solve its problem, but not so much that you blow token budgets.

> Workers operate in isolation (good: parallelizable, modular) but need shared context (bad: must pass state, enforce contracts).

> Total time: max of all paths, not sum.

> Agents are decoupled: don't know about each other. Easy to add new agent (just subscribe to bus).

> Shared context reduces redundancy: one agent fetches data, others read from bus. Saves computation.

> With 5 agents it's simple; with 50 agents, message bus keeps you sane.

> The more complex the problem, the more specialization helps.

## Anti-Patterns & Fixes

- Monolithic Single-Agent Complexity: trying to answer multi-domain questions (data retrieval + news analysis + financial modeling + risk assessment) with a single LLM prompt, causing missing data, biased analysis, or wrong models. Fix: decompose into specialist workers each with a focused scope and defined output schema.
- Unbounded Context Passing: passing the entire shared context to every worker regardless of relevance, blowing token budgets and degrading worker focus. Fix: give each worker only the context keys it needs for its specific subtask.
- Synchronous Sequential Execution: executing all worker tasks one-at-a-time even when tasks are independent, causing total latency to be the sum of all task durations. Fix: use async parallel execution so independent workers run concurrently and total time equals the critical path, not the sum.
- Direct Agent Coupling: having workers call each other directly, creating brittle dependencies and making the system hard to extend. Fix: use a message bus where agents publish results and subscribe to context, remaining unaware of each other.
- Missing Output Schema Contracts: workers returning arbitrary dict structures, causing the orchestrator's synthesis step to fail or produce inconsistent results. Fix: define expected_output_schema per WorkTask and validate worker output against it before synthesis.

## When To Apply

Load this page when:

- Use this when a user query requires data from multiple independent specialized sources (e.g., market data, news, financials, risk) that no single prompt can reliably handle.
- Use this when subtasks are naturally parallel and independent, and total latency matters (async dispatch reduces wall-clock time to the critical path).
- Use this when different parts of a problem require different tools, APIs, or domain expertise that are cleanest as separate agents with isolated responsibilities.
- Use this when you need modular updatability: changing one specialist (e.g., swapping a valuation model) should not require rewriting other workers or the orchestrator.
- Use this when a compliance, validation, or audit step must run after upstream workers complete, enforcing a sequential gate without coupling all agents together.
- Use this when reasoning complexity exceeds what a single context window can handle reliably, and decomposition into subproblems with defined output contracts is feasible.
- Use this when you are building a system that must scale from a small number of agents to many without architectural rework (message bus pattern).

## Concrete Examples

- Yahoo! Finance multi-agent financial research platform: orchestrator decomposes 'Should I buy Apple stock?' into four parallel workers (Data Agent, News Agent, Valuation Agent, Risk Agent), synthesizes into a buy/hold/sell recommendation with confidence score, handling 100,000+ queries per day.
- Financial advisor recommendation system using async message bus: five agents (ClientData, MarketData, RiskProfiling, ProductRecommendation, Compliance) run concurrently with dependency-ordered activation, publishing to a shared ContextBus and completing in parallel rather than sequentially.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Orchestrator-Worker**

An LLM coding agent generating orchestrator-worker systems faces a specific failure mode: it tends to collapse complexity back into a single large prompt rather than maintaining strict inter-agent contracts, because generating one big prompt feels locally easier than defining WorkTask schemas and output contracts. This pattern forces the agent to encode explicit expected_output_schema per task, preventing silent schema drift where a worker returns unexpected keys that corrupt the synthesis step. Additionally, LLM agents are prone to re-fetching or re-computing data already available on a shared bus; the message bus pattern gives the agent an architectural rule—read from bus before generating new tool calls—that prevents redundant token expenditure across parallel workers.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
