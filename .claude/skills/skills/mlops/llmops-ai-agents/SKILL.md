---
name: llmops-ai-agents
description: "Use when designing, building, evaluating, or operating AI agent systems in production — agent architecture, orchestration patterns, RAG pipelines, evaluation, observability, guardrails, and domain-specific deployment."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [llmops, ai-agents, orchestration, rag, evaluation, observability, production, multi-agent]
    related_skills: [distributed-systems, production-readiness, security-engineering, data-systems-engineering]
---

# LLMOps and AI Agents

## When to Load

- Use this when deciding whether a task requires an agent loop (perceive-reason-act-observe) or a plain LLM call
- Use this when choosing between the 7 agent types (simple reflex, model-based, goal-based, utility-based, learning, multi-agent, hierarchical) for a given use case
- Use this when selecting an agentic design pattern (tool use, RAG, planning, reflection) or multi-agent orchestration topology (orchestrator-worker, parallel fan-out, sequential pipeline, hierarchical)
- Use this when designing a RAG pipeline — chunking strategy, hybrid retrieval (BM25+dense+RRF), reranking, citation grounding, and retrieval evaluation
- Use this when building an agent evaluation system — golden datasets, LLM-as-judge, slice evaluation, regression testing, and continuous eval loops
- Use this when adding observability to an agent — trace/span architecture, structured logging, cost attribution, and tiered alerting
- Use this when hardening an agent for production — guardrail layers, circuit breakers, shadow mode, canary deployment, and rollback procedures
- Use this when deploying agents in regulated industries (finance, healthcare, legal, HR, industrial) and need domain-specific architectural patterns
- Use this when an autonomous action agent needs safety guarantees — verification-first architecture, three-gate approval pipelines, blocklist-based validation
- Use this when designing metacognitive or self-improving agents — session analysis loops, hypothesis-driven experimentation, reflection vs. learning separation

## Core Rules

> An agent is not a prompt. An agent observes its environment, reasons about what to do, takes an action, and observes the result — in a loop. If there is no loop, it is a function call.

> Match the pattern to the task. Orchestrator-worker for decomposable tasks, parallel fan-out for independent subtasks, sequential pipeline for quality-gating chains, hierarchical for enterprise-scale routing. Never over-engineer: start with the simplest pattern that satisfies the constraint.

> RAG is retrieval first, generation second. Hybrid retrieval (BM25 + dense + RRF) beats either alone. Structure-aware chunking beats fixed-size chunking. Every response must cite the source it drew from.

> Evaluation is an architecture, not a script. Three levels: component (does each piece work?), integration (does the pipeline produce correct end-to-end outputs?), and production (are real users getting value?). Run golden dataset regression on every deploy.

> LLM-as-judge needs calibration. Match scoring criteria to the use case. Use fairness checks (swapped positions, rephrased prompts) to detect model bias. Never use a single uncalibrated judge as the sole eval signal.

> Observability is not logging. Every agent request is a tree of named spans. Capture latency, token count, tool call result, and cost at each span. Alert on p99 latency, error rate, and cost drift — not just averages.

> Guardrails are a separate layer, not inline logic. Pre-call validators, post-call validators, and hard-coded circuit breakers must be independently testable and independently deployable.

> Shadow mode before canary, canary before full rollout. Run the new agent on real traffic without serving its responses. Compare traces before promoting. A/B test at 1% before 10%. Never skip this sequence under time pressure.

> Regulated domains change the architecture, not just the prompts. Finance needs immutable audit trails. Healthcare needs augment-not-replace framing. Legal needs jurisdiction-aware routing. Industrial needs hard physics/safety constraints before any ML prediction.

> Metacognitive agents must separate reflection from learning. Reflection (session-level, cheap, frequent) adjusts the current run. Learning (pattern-level, expensive, batch) updates the agent's behavior across runs. Conflating them causes instability.

> The span-of-control principle: an orchestrator managing 5 specialists is more reliable than one managing 15. When an orchestrator exceeds 5-7 workers, add a tier.

> Production readiness is a checklist, not a feeling. Guardrails deployed, shadow mode completed, golden dataset passing, cost attribution wired, rollback procedure documented, on-call runbook written. Block deploy until all gates pass.

## Concept Map

For deeper context, load these wiki pages:

- output/wiki/llmops-ai-agents/concepts/Agent-Fundamentals.md — agent loop (PRAOR), 7 agent types, agent anatomy, agent vs LLM call distinction
- output/wiki/llmops-ai-agents/concepts/Agentic-Design-Patterns.md — tool use, RAG, planning, reflection patterns; pattern selection framework
- output/wiki/llmops-ai-agents/concepts/Multi-Agent-Orchestration.md — orchestrator-worker, sequential pipeline, parallel fan-out, hierarchical, event-driven; 5 coordination questions
- output/wiki/llmops-ai-agents/concepts/LLMOps-Essentials.md — 4-layer LLMOps stack, context budget model, memory architecture, evaluation at scale, observability primitives, guardrails
- output/wiki/llmops-ai-agents/concepts/Building-Your-First-Agent.md — JTBD definition, constraint surface, agent pattern selection, hybrid retrieval, three-level eval plan
- output/wiki/llmops-ai-agents/concepts/RAG-Architecture.md — hybrid RAG (BM25+dense+RRF), structure-aware chunking, metadata filtering, citation grounding, reciprocal rank fusion
- output/wiki/llmops-ai-agents/concepts/Conversational-Agents.md — intent classification pipeline, handler registry, policy compliance gate, escalation thresholds, audit trail
- output/wiki/llmops-ai-agents/concepts/Autonomous-Action-Agents.md — three-gate approval, blocklist-based safety, autonomous coding loop, verification-first architecture
- output/wiki/llmops-ai-agents/concepts/Orchestrator-Worker-Architecture.md — decomposition pattern, context bus, work/task contracts, sequential gate, span-of-control
- output/wiki/llmops-ai-agents/concepts/Parallel-and-Fan-Out-Agents.md — fan-out/fan-in, confidence-weighted voting, safety threshold rule, partial results doctrine, per-agent timeout
- output/wiki/llmops-ai-agents/concepts/Sequential-Pipeline-Architecture.md — linear DAG, graph RAG, short-circuit logic, quality gates, state persistence per stage
- output/wiki/llmops-ai-agents/concepts/Hierarchical-Agent-Systems.md — three-layer hierarchy, DAG workflow, client isolation, tier-based resource allocation
- output/wiki/llmops-ai-agents/concepts/Metacognitive-Agents.md — session analysis loop, hypothesis-driven experimentation, convergence threshold, reflection vs learning separation
- output/wiki/llmops-ai-agents/concepts/Domain-Tech-Finance-Healthcare.md — code correctness, audit trails, fraud detection, HIPAA, clinical decision support, augment-not-replace
- output/wiki/llmops-ai-agents/concepts/Domain-E-commerce-Legal-HR.md — latency budgets, jurisdiction routing, bias mitigation, employment law compliance
- output/wiki/llmops-ai-agents/concepts/Domain-Media-Telecom-Gov-Industrial.md — content moderation, network complexity, multilingual, safety-critical, IoT, physics-ML hybrid
- output/wiki/llmops-ai-agents/concepts/Regulated-Industry-Patterns.md — parallel screening, decision gates, bias detection, counterfactual training, multi-tier latency, confidence-gated escalation
- output/wiki/llmops-ai-agents/concepts/Evaluation-Frameworks.md — parallel eval architecture, golden datasets, LLM-as-judge calibration, slice evaluation, continuous eval
- output/wiki/llmops-ai-agents/concepts/Observability-and-Cost-Control.md — trace/span architecture, structured logging, tiered alerts, compliance access logs, cost attribution
- output/wiki/llmops-ai-agents/concepts/Production-Hardening.md — guardrail layer, circuit breaker, shadow mode, canary deployment, production readiness checklist, tenant isolation

## Common Pitfalls

- Treating a single LLM call as an agent: Fix — check for the loop. If there is no observe-act-observe cycle, it is a pipeline step, not an agent. Design accordingly.
- Choosing orchestration topology before understanding task structure: Fix — apply the pattern selection framework. Map task properties (decomposable? parallelizable? quality-gated?) to the appropriate topology.
- Fixed-size chunking for RAG: Fix — use structure-aware chunking that respects chapter/section/paragraph boundaries. Fixed-size chunks split concepts across boundaries and degrade retrieval quality.
- Single-metric evaluation: Fix — slice eval results by difficulty, domain, and user segment. A model that averages 90% may fail catastrophically on edge cases that matter most.
- Deploying guardrails as inline code: Fix — guardrails must be an independent layer with their own tests and deployment lifecycle. Inline guardrails cannot be updated without touching core agent logic.
- Skipping shadow mode: Fix — run every new agent version in shadow mode for at least 24 hours before canary. Shadow mode catches regressions that golden datasets miss.
- Using one-size-fits-all orchestration in regulated domains: Fix — finance, healthcare, and legal each require domain-specific architectural primitives (audit trails, augment-not-replace, jurisdiction routing). Load the domain page before designing.
- Metacognitive loop without convergence criteria: Fix — define explicit convergence thresholds before running iterative improvement loops. Without them, agents over-iterate and never converge.

## Verification Checklist

- [ ] Agent has explicit perceive-reason-act-observe loop (not just a chain of LLM calls)
- [ ] Orchestration topology matches task structure (not chosen by familiarity)
- [ ] RAG pipeline uses hybrid retrieval + structure-aware chunking + citation grounding
- [ ] Evaluation covers component + integration + production levels
- [ ] LLM-as-judge has calibration and fairness checks
- [ ] Every agent span captures latency, token count, tool call result, and cost
- [ ] Guardrails are an independent layer with separate tests
- [ ] Shadow mode completed before any canary rollout
- [ ] Domain-specific constraints applied (if regulated industry)
- [ ] Production readiness checklist passed before deploy
