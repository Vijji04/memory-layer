---
name: production-readiness
description: "Use when designing, reviewing, or building production systems — architecture decisions, integration points, stability patterns, capacity planning, observability, and operations."
version: 1.0.0
author: Ayush Singh
license: MIT
metadata:
  hermes:
    tags: [phase-1, swe-foundations, ai-native, coding-agent, production, reliability]
    category: swe-foundations
    related_skills: []
---

# Production-Ready Systems

## Overview

Phase 1 engineering skill distilled from "Release It! Design and Deploy Production-Ready Software" by Michael Nygard.

This is a **routing skill** — it tells you when to engage and which concept page to read for depth.

Full knowledge lives in the wiki:
  /Users/ayushsingh/Desktop/ai_native_swe/output/wiki/release-it/

Do not try to hold all concepts in context at once.
Read the specific concept page when the situation calls for it.

## When to Load This Skill

- Use this when designing a new service or system architecture from scratch
- Use this when writing code that makes outbound network calls (HTTP, DB, queue, RPC)
- Use this when choosing between two implementation approaches with different operational cost profiles
- Use this when an availability, uptime, or SLA requirement appears in the spec
- Use this when diagnosing a production incident — cascades, thread exhaustion, pool starvation
- Use this when reviewing infrastructure, deployment, or configuration design
- Use this when planning observability (metrics, logging, health endpoints, dashboards)
- Use this when a capacity or scaling decision needs to be made
- Use this when writing administrative tooling or operational runbooks
- Use this when security isolation, privilege, or credential handling is involved

## Core Rules (always in context)

These load-bearing principles apply without reading any concept page:

> Don't avoid one-time development expenses at the cost of recurring operational expenses.

> Team assignments are the first draft of the architecture.

> Release 1.0 is the beginning of your software's life, not the end of the project.

> Design and architecture decisions are also financial decisions.

> Production is the only place to learn how the software will respond to real-world stimuli.

> Systems spend much more of their life in operation than in development.

> Different alternatives often have similar implementation costs but radically different lifecycle costs.

> Bugs will happen. They cannot be eliminated — they must be survived instead.

> Restoring service takes precedence over investigation during an active outage.

> Integration points are the number-one killer of systems.

## Concept Map

When you need depth, read the specific concept page. Pick the one that matches the situation.
Do not read all pages at once.

Wiki root: /Users/ayushsingh/Desktop/ai_native_swe/output/wiki/release-it/concepts/

### Architecture Anti-patterns
  When: Early design phase — choosing system boundaries, decomposition, team structure
  Covers: Conway's Law, Ivory Tower Architecture, Early Decision Crystallization
  Read: Architecture-Anti-patterns.md

### Availability Framework
  When: SLA or uptime target is specified; cost/benefit of another "9" is being evaluated
  Covers: Feature-Level SLA, Cost-vs-Avoided-Loss, SLA Inversion, Cost/Cost Trade-off
  Read: Availability-Framework.md

### Bulkheads
  When: Designing service that calls external APIs or DBs and must contain downstream failures
  Covers: Bulkhead partitioning, thread pool isolation, connection pool per dependency
  Read: Bulkheads.md

### Caching Patterns
  When: Deciding what to cache, how to size it, how to invalidate, or whether to precompute
  Covers: Cache sizing, CDN traffic governor, precompute vs dynamic, session bloat, cookie state
  Read: Caching-Patterns.md

### Capacity Framework
  When: Designing for a stated scale requirement; choosing horizontal vs vertical scaling
  Covers: Capacity definition (throughput + response time), driving/following variables model
  Read: Capacity-Framework.md

### Capacity Multiplier Effects
  When: Per-request or per-connection cost seems trivial but multiplies across users/instances
  Covers: Multiplier effect leverage, N-times cost identification
  Read: Capacity-Multiplier-Effects.md

### Cascade and Chain of Failure
  When: Diagnosing how a single bug propagated to a full outage; designing crack-stoppers
  Covers: Cascade failure propagation, chain of failure, crack propagation model, cascading capacity mismatch
  Read: Cascade-and-Chain-of-Failure.md

### Circuit Breaker
  When: Writing any outbound network call — HTTP, DB, queue, RPC
  Covers: Circuit breaker state machine (closed/open/half-open), trip thresholds, reset timeouts
  Read: Circuit-Breaker.md

### Code That's Easy to Test
  When: Writing code that calls external services and needs resilience tested in isolation
  Covers: Test harness pattern — fake servers simulating slow responses, drops, garbage data
  Read: Code-Thats-Easy-to-Test.md

### Complexity Patterns
  When: System has many moving parts with hidden internal dependencies; operators' mental models may be wrong
  Covers: Highly interactive complexity, technology frontier, tight coupling acceleration
  Read: Complexity-Patterns.md

### Configuration Management
  When: Designing config file layout; separating environment-specific from internal wiring
  Covers: Configuration separation, override layering, obvious configuration, dynamic reconfiguration
  Read: Configuration-Management.md

### Connection Pool Management
  When: Writing JDBC or any resource-pool access code; diagnosing pool exhaustion
  Covers: Per-page/per-fragment/hybrid strategies, pool-as-throttle, resource pool contention
  Read: Connection-Pool-Management.md

### Decoupling and Middleware
  When: Choosing between synchronous and asynchronous integration patterns
  Covers: Message-oriented middleware, temporal decoupling, spatial decoupling
  Read: Decoupling-and-Middleware.md

### Design for Production
  When: Initial architecture design; evaluating whether QA passage implies production readiness
  Covers: Design for production philosophy, pragmatic architecture, QA-production topology gap
  Read: Design-for-Production.md

### Fail Fast
  When: Writing request handlers — validate preconditions before accepting work you cannot complete
  Covers: Precondition validation, immediate error return, not accepting half-feasible requests
  Read: Fail-Fast.md

### Failure Propagation Models
  When: Diagnosing simultaneous failures across multiple systems; identifying common upstream dependency
  Covers: Common dependency hypothesis, vicious cycle (contention -> slowdown -> more contention), impulse vs stress
  Read: Failure-Propagation-Models.md

### Incident Response and Post-mortem
  When: Planning on-call runbooks; post-mortem evidence collection; cynical requirements review
  Covers: Restore-first priority, automated data collection, cynical requirements examination
  Read: Incident-Response-and-Post-mortem.md

### Integration Points
  When: Designing or reviewing any socket, pipe, process, or remote call
  Covers: Integration points as stability risk, route-per-integration tracking, tight coupling propagation
  Read: Integration-Points.md

### JVM and Runtime Internals
  When: Tuning JVM heap ratios; diagnosing GC-induced slowdowns in Java services
  Covers: Generational GC model (eden/survivor/tenured), heap tuning
  Read: JVM-and-Runtime-Internals.md

### Load Balancing and Clustering
  When: Choosing between active/active and active/passive; selecting load balancing approach
  Covers: DNS round-robin, reverse proxy, hardware LB, active/active vs active/passive, virtual IP migration
  Read: Load-Balancing-and-Clustering.md

### Network Architecture
  When: Designing server socket binding; separating backup/admin/production network traffic
  Covers: Network traffic segmentation, multihomed server architecture, VLAN isolation
  Read: Network-Architecture.md

### Operations Patterns
  When: Writing admin tooling or startup sequences; designing for operability
  Covers: Scriptable operations mandate, clean startup sequence
  Read: Operations-Patterns.md

### Recovery Patterns
  When: Designing for inevitable failure — damage containment, automatic recovery, fault isolation
  Covers: Recovery-oriented computing, restore-first, queue-and-retry, crumple zones
  Read: Recovery-Patterns.md

### SLA Inversion
  When: A stated SLA is higher than what any dependency in the call chain can actually deliver
  Covers: SLA inversion principle, effective SLA bounded by weakest dependency
  Read: SLA-Inversion.md

### Security Patterns
  When: Generating Dockerfiles, service config, credential handling, or privilege design
  Covers: Per-application user isolation, principle of least privilege, privilege separation, password vaulting
  Read: Security-Patterns.md

### Stability Antipatterns
  When: Reviewing integration code for patterns that amplify transient failures
  Covers: Named antipattern framework, antipatterns-to-patterns interaction map
  Read: Stability-Antipatterns.md

### Stability Patterns
  When: Selecting countermeasures to apply against identified stability threats
  Covers: Stability patterns framework overview and selection guide
  Read: Stability-Patterns.md

### Steady State
  When: Designing systems that must run without human intervention for log/data/cache growth
  Covers: Steady state pattern — systems manage their own resource lifecycle
  Read: Steady-State.md

### Systems Thinking for Capacity
  When: Capacity analysis requires reasoning about dynamic variables and causal chains, not linear projection
  Covers: Senge systems thinking applied to capacity, change-over-time reasoning
  Read: Systems-Thinking-for-Capacity.md

### Theory of Constraints
  When: Optimizing throughput — find the bottleneck before optimizing anything else
  Covers: Goldratt's ToC — exactly one constraint limits system capacity at any time
  Read: Theory-of-Constraints.md

### Timeouts
  When: Writing any outbound call that could hang indefinitely
  Covers: Timeout pattern — stop waiting after threshold; prevent blocked threads and cascades
  Read: Timeouts.md

### Transparency and Observability
  When: Designing metrics, logs, health endpoints, dashboards, or operational instrumentation
  Covers: Four perspectives of transparency, environmental awareness, pulse monitoring, OpsDB
  Read: Transparency-and-Observability.md

### Zero-One-Many Principle
  When: Designing QA topology — ensure test environments mirror production cluster counts
  Covers: Zero-one-many — only sensible multiplicities in computer science; QA must run clusters if production does
  Read: Zero-One-Many-Principle.md

## Verification Checklist

Before completing any non-trivial implementation, check:

- [ ] Does every outbound call have a timeout?
- [ ] Are connection pools sized per downstream dependency (not shared globally)?
- [ ] Are resources (connections, streams, locks) released in finally blocks?
- [ ] Can the system observe itself in production? (logs, metrics, health endpoint)
- [ ] Does the QA topology match production in terms of cluster counts and network topology?
- [ ] Are availability SLAs stated per feature and bounded by dependency SLAs?
- [ ] Can all administrative operations be scripted (not just GUI)?
- [ ] Does the system manage its own resource lifecycle (logs, caches, sessions)?

## Related Skills

<!-- Populated after all book wikis are complete -->
