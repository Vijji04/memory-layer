---
title: Golden Dataset Regression Testing: A curated set of verified input/output pairs run on every system change to detect regressions before deployment
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/LLMOps-Essentials.json]
contributing_chapters: ["LLMOps Essentials"]
confidence: high
---

# Golden Dataset Regression Testing: A curated set of verified input/output pairs run on every system change to detect regressions before deployment

> From chapter: *LLMOps Essentials*

## Core Principle

LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability & Guardrails. Every layer has specific implementation patterns — token budget allocation, memory type selection, golden dataset regression testing, and trace-span instrumentation — and skipping any layer creates a production liability. The non-negotiable principle is that developers must define correctness criteria for their domain before writing evals; AI tooling can implement but never substitute for that definitional work.

## Key Heuristics

These are the load-bearing rules for this concept.

> What is not in the context does not exist for the agent.

> More context is not always better — irrelevant context dilutes the signal and increases cost.

> LLMs pay more attention to the beginning and end of the context (primacy and recency effects). Put the most important information first and last.

> Skip any of these [4 layers], and your car becomes a liability.

> Can you write down on paper what 'correct' means for your system WITHOUT AI help? If not, you don't understand the problem yet.

> AI can help you implement evals, but YOU have to define what good looks like.

> Run evals every time you change the system.

> 10 requests/second × $0.01/request × 24 hours = $8,640/day. This happens to real companies.

## Anti-Patterns & Fixes

- Naive Context Stuffing: Concatenating all available context without token budgeting causes context window overflow, irrelevant signal dilution, and wasted cost. Fix: Use a ContextBuilder with explicit percentage budgets per component type and relevance-sorted truncation.
- Skipping Evals: Deploying without a golden dataset or defined correctness criteria means regressions and edge-case failures are discovered by users, not tests. Fix: Define what 'correct' means before deployment and run automated evals on every system change.
- AI-Generated Evals Without Human Ownership: Letting an LLM generate test cases without the developer understanding what is being tested produces a 90%-passing eval suite that misses real failure modes. Fix: The developer must define correctness criteria manually before using AI to expand test coverage.
- Amnesiac Agent (No Memory Architecture): Without persistent memory, every session starts from zero, making agents unable to reference prior interactions or user context. Fix: Implement all four memory types (in-context, episodic, semantic, procedural) appropriate to the use case.
- Unmonitored Production: Running agents without traces, cost tracking, or guardrails means failures are invisible until they cause user harm or budget overruns. Fix: Instrument every pipeline stage with spans, set cost budgets with hard stops, and attach input/output guardrail checks.

## When To Apply

Load this page when:

- Use this when building an agent that will make repeated LLM calls in production and you need to control token spend per request.
- Use this when a user's conversation history plus retrieved documents together risk exceeding the model's context window.
- Use this when an agent needs to reference information from previous sessions or remember user-specific facts across conversations.
- Use this when a production agent returns wrong, hallucinated, or out-of-scope outputs and you need to detect and block them automatically.
- Use this when you need to diagnose why an agent is slow and must isolate whether the bottleneck is retrieval, LLM latency, or guardrail processing.
- Use this when preparing to deploy an agent and you need to define a regression test suite that runs on every code or prompt change.
- Use this when costs are scaling unexpectedly and you need to route cheaper models for low-complexity queries.
- Use this when an agent handles sensitive user data and you must redact PII before it enters or exits the LLM.

## Concrete Examples

- Password reset query for 'Jane' (premium user): A 16,000-token budget is allocated across system prompt (200 tokens), user profile (50 tokens), retrieved docs (800 tokens), and conversation history (10 most recent messages), demonstrating context prioritization and budget arithmetic.
- ContextBuilder class with fit_docs and fit_history methods: Shows relevance-sorted doc inclusion with truncation fallback and recency-first history pruning in Python code.
- ContextCompressor with summarize_old_messages: Replaces old messages with a 3-5 bullet LLM-generated summary while keeping the N most recent messages verbatim.
- Full integrated agent run() method: Wires all 4 layers together — input guardrails, memory retrieval, context building, cost check, LLM generation, output guardrails, and memory storage — each wrapped in a named trace span.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**LLMOps Essentials**

An LLM coding agent generating agent infrastructure faces a specific failure mode: it will produce syntactically correct, plausible-looking eval suites and context builders without any grounding in what 'correct' actually means for the target domain, creating false confidence. The agent also cannot self-monitor costs or latency — without instrumented spans and budget checks baked into generated code, it will silently generate runaway-cost or slow pipelines with no observable signal. Critically, an LLM agent must treat context budget management as a first-class code constraint, not an afterthought, because it is itself subject to the same context window limits it is building around.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
