---
title: Production Readiness Checklist: An executable, gate-keeping checklist that blocks deployment if any of ~20 codified criteria fail
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Production-Hardening.json]
contributing_chapters: ["Production Hardening"]
confidence: high
---

# Production Readiness Checklist: An executable, gate-keeping checklist that blocks deployment if any of ~20 codified criteria fail

> From chapter: *Production Hardening*

## Core Principle

Production hardening wraps an agent in three independent guardrail layers (input, agent/tool, output) and adds operational infrastructure—circuit breakers, rate limiting, shadow/canary deployment, tenant isolation, and load testing—to ensure the agent degrades gracefully under adversarial inputs, concurrent load, and partial failures. The core principle is defense in depth: each layer can block independently, PII is redacted rather than just blocked, and circuit breakers prevent cascading failures when the agent misbehaves. A codified, executable production readiness checklist gates deployment on all criteria being met, preventing the common failure mode of shipping a demo-quality agent to real users.

## Key Heuristics

These are the load-bearing rules for this concept.

> Guards on the input side. Guards on the output side. Guards around tool calls.

> Each guardrail is independent. Each can block.

> Redact before block (apply redactions first).

> When an agent starts misbehaving, you don't want it to fail millions of users. Circuit breakers trip automatically and route traffic elsewhere.

> Before launch, stress test. Can your agent handle 1000 concurrent users? 10,000?

> Shadow mode: new agent validated against production

> Rollback plan: know which actions are reversible

## Anti-Patterns & Fixes

- No Input Guardrails: Agent receives raw user input including SSNs, credit card numbers, jailbreak attempts, and absurdly long strings, causing data leaks and prompt injection. Fix: Implement InputGuardrails with length check, PII detection, and topic filter before input reaches the agent.
- No Output Guardrails: Agent returns hallucinated, PII-containing, or toxic responses directly to users. Fix: Implement OutputGuardrails that redact PII first, then check groundedness and toxicity before returning any response.
- Blocking on PII in Output Instead of Redacting: Blocking outputs containing PII prevents all responses even when the PII can simply be removed. Fix: Redact PII (replace with tokens like [SSN]) rather than blocking the entire response.
- Big-Bang Deployment: Shipping a new agent directly to all users without validation risks widespread failure. Fix: Use shadow mode to validate agreement rate (>95%), then canary deployment with gradual traffic shifting and automatic rollback.
- No Circuit Breaker: A failing agent continues to receive and fail requests, cascading failures across the system. Fix: Wrap agent calls in a CircuitBreaker that opens after N consecutive failures and attempts recovery after a timeout.
- Missing Load Testing Before Launch: An agent that works in a notebook may collapse under concurrent production load. Fix: Run load_test_agent with concurrent workers before deployment, requiring >99% success rate and P99 latency <5000ms.

## When To Apply

Load this page when:

- Use this when shipping an agent from a prototype or notebook environment to a production system with real users
- Use this when implementing a new agent endpoint and needing to decide what validation to run on incoming requests
- Use this when an agent is calling external tools or APIs and you need to prevent runaway failures from cascading
- Use this when handling user data that might contain PII (SSNs, credit cards, emails) in either direction of the agent pipeline
- Use this when deploying an updated agent and needing to validate it against the existing production agent before full rollout
- Use this when building a multi-tenant SaaS product where agent data access must be strictly scoped per customer
- Use this when defining a go/no-go deployment gate that must pass programmatic checks before production release
- Use this when stress-testing an agent to establish baseline performance benchmarks and surface concurrency bugs

## Concrete Examples

- InputGuardrails class with three sequential checks: length (max 5000 chars), PII (regex for SSN and credit card patterns that block), and topic filter (keyword-based block list)
- OutputGuardrails class that redacts SSNs and credit cards with placeholder tokens, then checks hallucination via LLM judge score threshold (0.7), then checks toxicity via keyword list
- CircuitBreaker class with CLOSED/OPEN/HALF_OPEN state machine, failure_threshold=5, recovery_timeout=60s, and a _should_attempt_recovery method based on elapsed time
- load_test_agent function using ThreadPoolExecutor with configurable num_workers, measuring P50/P99 latency and asserting >99% success rate and <5000ms P99 before deployment

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Production Hardening**

An LLM coding agent generating production agent code is especially prone to omitting guardrail layers entirely—it will produce functional demo-quality code that passes happy-path tests but has no PII detection, no circuit breakers, and no multi-tenant isolation, because these concerns are rarely in the immediate prompt context. The circuit breaker and output guardrail patterns are particularly critical for agents: unlike a human developer who notices cascading failures in staging, an LLM agent executing tool calls can silently generate and deploy broken code that then fails millions of requests before anyone intervenes. The production readiness checklist as executable code is the most agent-applicable pattern here—it gives an LLM agent a concrete, verifiable exit criterion that prevents shipping without the full safety layer stack.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
