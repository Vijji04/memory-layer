---
title: Trace/Span Architecture: every agent request is a tree of named spans capturing latency, token counts, and cost at each operation node
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Observability-and-Cost-Control.json]
contributing_chapters: ["Observability and Cost Control"]
confidence: high
---

# Trace/Span Architecture: every agent request is a tree of named spans capturing latency, token counts, and cost at each operation node

> From chapter: *Observability and Cost Control*

## Core Principle

Observability and cost control must be designed as infrastructure, not retrofitted: every agent request should produce a trace tree of named spans with latency and cost attached, every event should emit machine-parseable structured JSON logs, and alerting rules should be evaluated continuously against captured baselines. Without this foundation, production agent systems are undiagnosable, unoptimizable, and financially unsustainable. The chapter provides concrete Python implementations of TraceContext, StructuredLogger, tiered AlertRules, and compliance AccessLog patterns, plus a pre-launch checklist to ensure all instrumentation is in place before traffic arrives.

## Key Heuristics

These are the load-bearing rules for this concept.

> You cannot improve what you cannot see.

> You cannot sustain what you cannot afford.

> Trace everything. Yes, it's overhead. But you can't optimize what you can't see.

> Not all metrics are equal. Focus on metrics that answer business questions.

> Build observability first.

> Traces are for the happy path. When things go wrong, you need logs.

> Sample spans in high-volume systems (trace 1% of requests in detail).

## Anti-Patterns & Fixes

- ObservabilityAsAfterThought: adding logging and tracing after a production incident means you have no baseline and cannot diagnose what changed. Fix: instrument traces, structured logs, dashboards, and alerting before going live.
- UnstructuredFreeTextLogs: human-readable log strings cannot be queried, aggregated, or alerted on programmatically. Fix: emit every log entry as a JSON object with a consistent schema including trace_id, span_id, level, and typed tag fields.
- NoBaselineCapture: without knowing what 'normal' looks like, drift and regressions are invisible. Fix: capture baseline metrics at launch and configure drift detection (e.g., alert when tokens-per-query exceed 130% of baseline).
- FlatCostVisibility: knowing total spend without per-query or per-model attribution makes cost optimization impossible. Fix: attach cost_usd and token counts as span tags on every LLM call, then aggregate by model, user, and query type.
- UniformModelRouting: sending all queries to the most capable (and expensive) model wastes money on simple tasks. Fix: implement model routing that assigns cheap models to simple queries and expensive models only when needed.
- MissingComplianceTrail: in regulated industries, agents accessing sensitive data without immutable audit logs creates legal exposure. Fix: log every data access with user_id, agent_name, resource_id, classification, and approved flag to an immutable backend.

## When To Apply

Load this page when:

- Use this when building any agent that will serve production traffic and you need to diagnose latency, cost, or correctness issues after deployment.
- Use this when an LLM agent makes multiple sequential tool calls and you need to attribute total request cost and latency to individual operations.
- Use this when designing a multi-agent system and you need to correlate logs and spans across agents that all share a single user request.
- Use this when token costs are growing unexpectedly and you need to identify which prompt, user segment, or tool call is responsible.
- Use this when deploying an agent in a regulated industry (finance, healthcare, legal) and you need an immutable audit trail of data access.
- Use this when setting up alerting and you need to distinguish between conditions that require immediate paging versus ticket creation versus passive logging.
- Use this when an agent's behavior degrades silently over time and you need early-warning drift detection on token counts, error rates, or latency.

## Concrete Examples

- Account balance request trace: a fully annotated span tree for 'What's my account balance?' showing input_validation, agent_reasoning, llm_call (400ms, $0.00089), tool_execution, database_query, and output_validation with total latency 465ms
- StructuredLogger with log_llm_call helper: JSON log entry capturing model, input_tokens, output_tokens, cost_usd, and latency_ms for a claude-3-5-sonnet call (2300 input, 150 output, $0.00089)
- AlertRule examples: PAGE on error_rate > 0.5, URGENT on p99_latency > 10s, WARNING on token_inflation > 130% of baseline, INFO on cache_hit_rate < 20%
- agent_read_customer_record function: compliance check via OPA policy engine followed by immutable access log write before fetching a CONFIDENTIAL-classified customer record

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Observability and Cost Control**

An LLM coding agent generating agent infrastructure is especially likely to omit observability entirely—it will produce functional-looking code with no spans, unstructured print statements instead of structured logs, and no cost attribution, because those concerns are orthogonal to correctness and tests won't catch their absence. This chapter's patterns give the agent concrete, nameable structures (TraceContext, StructuredLogger, AlertRule, AccessLog) to emit rather than leaving instrumentation as an implicit responsibility. The compliance logging pattern is particularly critical for LLM-generated code because agents accessing sensitive data without audit trails create invisible legal risk that neither unit tests nor code review will surface.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
