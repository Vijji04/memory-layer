---
name: agentic-swe-master
description: "Use when starting, reviewing, or building any production-grade software or AI-native system. Orchestrates the full 20-phase production lifecycle, routes to the right domain skills at each phase, and guides the agent through every engineering layer from cognitive design to continuous learning."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [orchestrator, ai-native, production, lifecycle, routing, swe-foundations, master]
    category: swe-foundations
    related_skills: [engineering-mindset, modular-architecture, production-readiness, distributed-systems, security-engineering, data-systems-engineering, llmops-ai-agents]
trigger_conditions:
  - "Use this when starting a new production-grade software or AI-native project from scratch"
  - "Use this when you need to know which phase of a project you are currently in and what to do next"
  - "Use this when a task spans multiple engineering domains and you need to know which domain skills to load first"
  - "Use this when building a production AI agent that must be secure, observable, and fault-tolerant"
  - "Use this when designing a system that involves both distributed services and LLM reasoning components"
  - "Use this when you need to evaluate whether a production system is ready to ship across all engineering dimensions"
  - "Use this when onboarding onto a codebase and need a structured way to assess its engineering completeness"
  - "Use this when a student or team needs a roadmap for building AI-native software end-to-end"
  - "Use this when a system is failing in production and you need to diagnose which engineering layer is the root cause"
  - "Use this when adding a new major capability to an existing system and need to know which engineering concerns it touches"
---

# Agentic SWE Master Orchestrator

This is the entry point for the agentic-swe-kit. It drives the complete 20-phase
production lifecycle and routes to domain skills at every step. Load this first.
Domain skills load themselves as each phase demands them.

---

## Layer 1: Diagnostic Protocol

Before selecting a phase or routing table entry, answer these 5 questions:

  Q1: Scope — New project, existing system being extended, or production incident?
  Q2: AI components — Does this involve LLM calls, agents, RAG, or evaluation?
  Q3: Distribution — Does this cross network boundaries (multi-service, queues, replicas)?
  Q4: Trust boundary — Does this involve auth, sensitive data, or external actors?
  Q5: Current phase — Which of the 20 phases below matches where the work is happening?

Route based on answers:
  New + AI + Distributed + Trust -> start at Phase 0, walk all 20 phases in order
  Incident -> jump to Phase 10 (Observability) + Phase 12 (Reliability) first
  Existing system extension -> identify which phase the new feature touches, load those skills
  Single-domain task -> use the Fast Routing Table below

---

## Layer 2: 20-Phase Production Lifecycle

Each phase: what it covers, which skills to load, and what gate must pass before leaving.

### Phase 0: Cognitive Design
What thinking should the system perform? This is the most skipped phase and the
most common source of wasted engineering work.
Skills: engineering-mindset
Define: cognitive job, inputs, outputs, reasoning depth, autonomy level, human
involvement points, failure tolerance, trust boundaries.
Gate: Cognitive job is written down. Autonomy level is explicit. Failure modes listed.

### Phase 1: System Architecture Design
Choose architecture style. Draw service boundaries. Decide deployment topology.
Skills: modular-architecture + distributed-systems
Define: monolith vs modular monolith vs microservices vs event-driven. Boundary
types. Component dependency graph. Service communication mechanisms.
Gate: Architecture style chosen with justification. Service graph exists. Boundary
types stated (source / deployment / process / service). No cycles in dependency graph.

### Phase 2: Frontend Engineering
AI-native UX is not forms and dashboards.
Skills: engineering-mindset + modular-architecture
Define: streaming UI, agent transparency, human-in-the-loop checkpoints, approval
queues, agent state visualization, interruptibility.
Gate: UX paradigm chosen. Streaming or SSE strategy defined. HITL touchpoints mapped.

### Phase 3: Backend Engineering & API Layer
The cognitive operating system for the product.
Skills: production-readiness + modular-architecture
Define: service modules (auth, agent runtime, memory, tools, evaluation, campaign).
Explicit state machines for all agent workflows. Request validation. Rate limiting.
Gate: Service modules defined. At least one state machine drawn with explicit states.
Every outbound call has a timeout strategy.

### Phase 4: Workflow Orchestration
Agents pause, resume, retry, branch, and checkpoint. Design for that.
Skills: llmops-ai-agents + distributed-systems
Define: orchestration topology (orchestrator-worker, sequential pipeline, parallel
fan-out, hierarchical, event-driven). Workflow engine chosen. State persistence strategy.
Gate: Orchestration topology matches task structure. Workflow states are explicit.
Checkpointing strategy defined. Span-of-control <= 7 workers per orchestrator.

### Phase 5: LLM & Reasoning Layer
This is not "call an API." It is a routing, budgeting, and validation system.
Skills: llmops-ai-agents + engineering-mindset
Define: multi-model routing (cheap model for classification, reasoning model for
planning). Prompt infrastructure (versioning, A/B, rollback). Structured output
schemas. Context budget allocation. Context engineering strategy.
Gate: Model routing table defined. All outputs validated against schema. Context
budget explicitly managed. Prompt versioning strategy in place.

### Phase 6: Memory Architecture
Short-term vs long-term vs retrieval. Each is a different engineering problem.
Skills: llmops-ai-agents + data-systems-engineering
Define: short-term memory (session state, Redis), long-term memory (Postgres,
vector DB, graph DB), RAG pipeline (hybrid BM25+dense+RRF, structure-aware chunking,
reranking, citation grounding). Context engineering layer.
Gate: Memory tiers separated explicitly. RAG pipeline uses hybrid retrieval.
Every response cites its source. Freshness strategy defined.

### Phase 7: Tooling Layer & Sandboxing
Agents become useful only through tools. Tools are dangerous without boundaries.
Skills: llmops-ai-agents + security-engineering
Define: tool registry (schema, permissions, auth, rate limits, retries, logging).
Sandboxing strategy (Docker, Firecracker, jailed runtimes). MCP or API layer.
Tool capability scoping per agent role.
Gate: Tool registry exists with schemas and permissions. No tool executes without
explicit capability grant. Sandboxing in place for code execution and browser agents.

### Phase 8: Multi-Agent Systems
Where systems become powerful and also where they fail in new ways.
Skills: llmops-ai-agents + distributed-systems
Define: agent roles (planner, researcher, executor, critic, verifier, memory updater).
Coordination mechanism (task decomposition, shared memory, message bus, arbitration).
Failure management (validators, critics, reflection loops, guardrails).
Gate: Span-of-control verified. Agent roles have defined contracts. Failure path
for every agent type is handled. Consensus mechanism chosen if needed.

### Phase 9: Evaluation Systems
The phase most AI startups skip. The one that kills them.
Skills: llmops-ai-agents + engineering-mindset
Define: offline eval (golden datasets, metrics: accuracy, hallucination rate, tool
correctness, latency, cost). Online eval (failure patterns, user corrections, retries).
LLM-as-judge (calibrated, fairness-checked). Human eval cadence. Regression testing.
Gate: Golden dataset exists. 3-level eval plan written (component / integration /
production). LLM-as-judge calibrated. Regression suite runs on every deploy.

### Phase 10: Observability & Tracing
Without observability you are blind. AI systems need more than logs.
Skills: production-readiness + llmops-ai-agents
Define: traditional observability (logs, traces, metrics). AI observability (prompt
traces, token usage, tool traces, memory injection traces, hallucination detection).
Cost observability (token usage, GPU, cache hits, retrieval costs). Alert thresholds.
Gate: Every agent span captures latency + token count + tool result + cost.
Alerts on p99 latency, error rate, and cost drift. Prompt traces searchable.

### Phase 11: Security Architecture
AI-native security is harder than traditional security.
Skills: security-engineering + distributed-systems
Define: traditional security (auth, RBAC, encryption, secrets, network isolation).
AI-specific threats (prompt injection, data leakage, tool abuse, jailbreaks).
Tenant isolation. Policy-before-mechanism. Zero Trust posture.
Gate: Threat model exists with specific adversary categories. Prompt injection
mitigated with instruction hierarchy and sanitization. RBAC implemented. Audit
trails are append-only and tamper-evident.

### Phase 12: Reliability Engineering
Production agents fail differently. Design for resumability, not just availability.
Skills: production-readiness + distributed-systems
Define: retry systems (exponential backoff, fallback models, recovery states).
Circuit breakers (prevent cascading failures, runaway loops). Idempotency (agent
retries must not duplicate side effects). Checkpointing (workflow state, memory
snapshot, tool results).
Gate: Every outbound call has circuit breaker + timeout + retry with idempotency.
Checkpointing strategy allows resumption after crash. No operation has side effects
on retry that it didn't have on first execution.

### Phase 13: Infrastructure & Deployment
Skills: production-readiness + distributed-systems
Define: compute (CPU vs GPU workloads). Containerization (Docker). Orchestration
(Kubernetes, ECS, serverless). Model serving (vLLM, Ollama, TGI). Async queues
(Kafka, Redis Queue, RabbitMQ). Caching (semantic cache, retrieval cache, response cache).
Gate: All services containerized. Queue strategy chosen. Model serving decision made.
Semantic caching reduces token spend on repeat queries.

### Phase 14: Data Engineering Layer
AI systems are data systems. Pipelines must be treated as software, not scripts.
Skills: data-systems-engineering + production-readiness
Define: ingestion pipelines (cleaning, embedding, indexing, freshness updates).
Feature stores (personalization). Knowledge graphs (reasoning, entity relationships,
memory grounding). Schema evolution strategy for all data crossing service boundaries.
Gate: Pipelines are idempotent and rerunnable. Schema changes are backward-compatible
for at least one full deployment cycle. Knowledge graph exists if reasoning requires
entity relationships.

### Phase 15: Governance & Compliance
Enterprise requirement. Cannot be bolted on after launch.
Skills: security-engineering + llmops-ai-agents
Define: audit trails (prompts, outputs, decisions, tool calls — all immutable).
Compliance mapping (GDPR, HIPAA, SOC2, ISO27001 as applicable). Explainability
(users must understand why the agent acted). Data residency.
Gate: Audit trail covers every agent action. Compliance requirements mapped to
specific controls. Explainability mechanism exists for user-facing decisions.

### Phase 16: Economics & Cost Control
AI systems are probabilistic economics systems. Ignoring this burns runway.
Skills: llmops-ai-agents + production-readiness
Define: token cost tracking (per request, per user, per feature). GPU utilization.
Cache hit rate (semantic, retrieval, response). Routing efficiency (cheap model
for simple tasks, expensive model only when needed). Cost per successful outcome.
Gate: Cost attribution is wired per span. Model routing reduces cost on at least
20% of requests vs naive single-model approach. Cache hit rate tracked and > 0%.

### Phase 17: Developer Experience
Production AI teams need tooling to iterate safely.
Skills: engineering-mindset + modular-architecture
Define: prompt playground. Eval dashboards. Trace viewers. Replay systems
(replay failed runs with full context). Workflow visualizers. Local development
parity with production agent behavior.
Gate: Failed runs can be replayed locally. Prompt changes can be A/B tested
without full deployment. Eval results visible to the whole team.

### Phase 18: CI/CD for AI Systems
Different from traditional CI/CD. Prompts are deployments.
Skills: production-readiness + llmops-ai-agents
Define: prompt versioning in git. Model versioning. Eval gates (benchmark suite
must pass before deploy). Shadow deployment (new agent on real traffic, not serving).
Canary releases (1% before 10% before full). Rollback procedure documented.
Gate: No prompt or model change deploys without passing eval gates. Shadow mode
ran for >= 24 hours. Rollback takes < 5 minutes.

### Phase 19: Human-in-the-Loop Systems
Real enterprise AI is supervised autonomy, not full automation.
Skills: llmops-ai-agents + security-engineering
Define: approval workflows (which actions require human sign-off). Escalation
systems (low-confidence triggers human SDR). Uncertainty detection. Feedback
loops (user edits feed back into system as training signal).
Gate: Every high-stakes action has an approval gate. Confidence threshold for
escalation is defined and tested. Feedback mechanism routes corrections to eval system.

### Phase 20: Continuous Learning Systems
The system improves from production outcomes, safely.
Skills: llmops-ai-agents + data-systems-engineering
Define: feedback loop (corrections, outcomes, user behavior). Reflection vs
learning separation (reflection = session-level, cheap; learning = batch, pattern-level).
Convergence criteria before any behavioral update. Safety guardrails on updates
(no model update without regression test passing).
Gate: Reflection and learning are separate pipelines. Convergence threshold is
explicit. No learning update ships without regression suite passing.

---

## Layer 3: Fast Routing Table

For known problem types — skip the diagnostic, go straight to skills.

| Problem Scenario | Load These Skills (in order) |
|---|---|
| New service from scratch | modular-architecture -> engineering-mindset -> production-readiness |
| Production AI agent | llmops-ai-agents -> production-readiness -> security-engineering |
| Distributed service design | distributed-systems -> production-readiness -> modular-architecture |
| Security-sensitive data pipeline | data-systems-engineering -> security-engineering -> production-readiness |
| New codebase architecture | modular-architecture -> engineering-mindset |
| Agent evaluation & reliability | llmops-ai-agents -> production-readiness -> distributed-systems |
| Multi-agent system design | llmops-ai-agents -> distributed-systems -> security-engineering |
| RAG pipeline design | llmops-ai-agents -> data-systems-engineering |
| Production incident diagnosis | production-readiness -> distributed-systems -> llmops-ai-agents |
| Auth or access control | security-engineering -> modular-architecture |
| Data store selection & replication | data-systems-engineering -> distributed-systems |
| Compliance / audit trail | security-engineering -> llmops-ai-agents -> data-systems-engineering |
| Cost overrun on LLM system | llmops-ai-agents -> production-readiness |
| Refactoring a monolith | modular-architecture -> production-readiness -> engineering-mindset |
| AI system CI/CD pipeline | llmops-ai-agents -> production-readiness |
| Memory architecture for agents | llmops-ai-agents -> data-systems-engineering |
| Onboarding onto existing system | engineering-mindset -> modular-architecture -> production-readiness |

---

## Cross-Domain Core Rules

These 9 heuristics apply regardless of domain. Violations are the most common
root cause of cross-domain failures.

1. Observability is never optional. A system you cannot observe is one you cannot
   fix. The cost of adding observability after the fact is 5x the cost of building
   it in. In AI systems, this includes prompt traces, not just application logs.

2. Security policy before mechanism. Generating encryption, tokens, or ACLs before
   defining who can do what to whom produces mechanisms that cannot be audited.
   Define the policy as a structured artifact first. Then implement.

3. Test the system at the boundaries, not at the center. Bugs live in integration
   points, not in isolated functions. Every network call, every schema crossing, every
   service boundary is a potential failure. Test harnesses must simulate those boundaries.

4. Stability under partial failure is a design requirement, not a nice-to-have.
   The question is not "will this fail?" but "what happens when it fails?" Circuit
   breakers, timeouts, bulkheads, and idempotent retries must be designed in from
   the start. They cannot be retrofitted cheaply.

5. The architecture must defer decisions, not make them early. The database is a
   detail. The framework is a detail. The model provider is a detail. Locking any
   of these in before domain logic is stable costs more than it saves.

6. Evaluation is an architecture, not a script. You cannot know if a probabilistic
   system is improving without a structured evaluation system that runs continuously
   — component level, integration level, and production level. Adding eval after
   shipping is like adding tests after a bug hits production.

7. Consistency models are explicit choices, not defaults. Assuming strong consistency
   everywhere is expensive and fragile. Assuming eventual consistency everywhere
   produces incorrect systems. Every replicated data path must have an explicit
   consistency model with justification.

8. Cross-service schema changes must be backward and forward compatible for one
   full deployment cycle. Old code must read new data. New code must read old data.
   Violating this is the most common cause of silent data corruption in distributed
   systems — and in AI memory pipelines.

9. Human-in-the-loop is an architecture decision, not a fallback. The decision about
   which actions require human approval must be made at design time, not added when
   something goes wrong in production. Escalation thresholds are system parameters,
   not afterthoughts.

---

## Skill Index

| Skill | Installed Path | Purpose |
|---|---|---|
| engineering-mindset | swe-foundations/engineering-mindset | Quality decisions, trade-offs, honesty, pragmatism |
| modular-architecture | swe-foundations/modular-architecture | Boundaries, dependency direction, SOLID, clean layers |
| production-readiness | swe-foundations/production-readiness | Stability patterns, timeouts, circuit breakers, operability |
| distributed-systems | swe-foundations/distributed-systems | Consistency, fault tolerance, naming, coordination, clocks |
| security-engineering | swe-foundations/security-engineering | Threat modeling, crypto, access control, privacy, assurance |
| data-systems-engineering | swe-foundations/data-systems-engineering | Storage, replication, partitioning, transactions, streaming |
| llmops-ai-agents | mlops/llmops-ai-agents | Agent architecture, RAG, evaluation, observability, guardrails |

---

## Anti-Patterns

1. **Phase Skipping**
   Team jumps straight to implementation (Phase 3-4) without cognitive design (Phase 0)
   or architecture decisions (Phase 1). Result: AI system built on wrong agent class,
   wrong orchestration topology, wrong memory architecture.
   Fix: Run Phase 0 diagnostic first. Define the cognitive job before writing code.
   The 30 minutes spent in Phase 0 saves weeks of rearchitecting later.

2. **Siloed Domain Thinking**
   Security added at the end. Observability added after first incident. Evaluation
   added after first hallucination ships to a customer. Each domain team thinks their
   layer is someone else's problem.
   Fix: Load this master skill at project start. Every phase has a gate. No phase
   is optional. Cross-domain concerns are baked into each phase's checklist.

3. **Agent Architecture Mismatch**
   Using a multi-agent orchestration system for a task that is a deterministic DAG.
   Or using a single ReAct loop for a task that requires parallel execution.
   Fix: Phase 4 diagnostic matches task properties (decomposable? parallel? quality-gated?)
   to orchestration topology before any workflow code is written.

4. **Mechanism Without Policy**
   Encrypting data, adding JWTs, implementing RBAC — all without a written security
   policy that defines who can do what to whom. The mechanisms exist but cannot be
   audited because there is nothing to audit against.
   Fix: Phase 11 gate requires a threat model artifact before any security mechanism
   is implemented. Policy is the input; mechanism is the output.

5. **Evaluation Debt**
   Shipping prompts and models without a golden dataset, without LLM-as-judge
   calibration, without regression gates. Every deploy is a coin flip.
   Fix: Phase 9 gate blocks deploy until golden dataset exists and 3-level eval
   plan is written. Phase 18 CI/CD gate blocks every subsequent deploy until eval
   passes. Never skip this. It compounds.

6. **Observability Retrofit**
   Instrumentation added after a production incident. Traces missing context that
   would have diagnosed the problem. Cost attribution non-existent.
   Fix: Phase 10 is non-negotiable. Every agent span must capture latency, token
   count, tool result, and cost from day one. Retrofitting is 5x more expensive.

7. **Infinite Autonomy Assumption**
   Agent designed to act fully autonomously in all scenarios including high-stakes
   actions. No escalation path. No approval gates. No uncertainty detection.
   Fix: Phase 0 defines autonomy level explicitly. Phase 19 builds approval workflows
   and escalation systems. The decision of what requires human approval is made at
   design time, not discovered in production.
