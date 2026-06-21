---
title: Composite Data System Architecture: Breaking application requirements into tasks handled by best-fit single tools (Redis, Kafka, Elasticsearch, Postgres) stitched together by application code, with the API hiding implementation details
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-1-Reliable-Scalable-and-Maintainable-Applications.json]
contributing_chapters: ["Chapter 1: Reliable, Scalable, and Maintainable Applications"]
confidence: high
---

# Composite Data System Architecture: Breaking application requirements into tasks handled by best-fit single tools (Redis, Kafka, Elasticsearch, Postgres) stitched together by application code, with the API hiding implementation details

> From chapter: *Chapter 1: Reliable, Scalable, and Maintainable Applications*

## Core Principle

Data-intensive applications are built from composable, specialized tools (databases, caches, queues, search indexes) and the engineer's job is to design their combination to satisfy reliability (correct behavior under faults), scalability (sustained performance under load growth), and maintainability (productive operability over time by multiple people). Faults are inevitable component deviations; good design prevents them from cascading into system-level failures through explicit tolerance mechanisms rather than hoping for prevention alone. There is no universal solution — the right architecture emerges from understanding load characteristics, performance metrics, and the consistency guarantees required at each component boundary.

## Key Heuristics

These are the load-bearing rules for this concept.

> A fault is not the same as a failure. A fault is one component deviating from its spec; a failure is when the system as a whole stops providing the required service to the user.

> It is impossible to reduce the probability of a fault to zero; therefore it is usually best to design fault tolerance mechanisms that prevent faults from causing failures.

> In fault-tolerant systems, it can make sense to increase the rate of faults by triggering them deliberately — many critical bugs are actually due to poor error handling.

> Scalability means having strategies for keeping performance good, even when load increases.

> Good abstractions can help reduce complexity and make the system easier to modify and adapt for new use cases.

> When you combine several tools in order to provide a service, you have essentially created a new, special-purpose data system from smaller, general-purpose components.

> There is unfortunately no quick answer to making applications reliable, scalable or maintainable.

## Anti-Patterns & Fixes

- Single-Tool Assumption: Assuming one database or tool can satisfy all data processing and storage needs of a complex application. Fix: Decompose requirements into tasks best handled by specialized tools and stitch them together via application code with a clean API.
- Conflating Fault with Failure: Treating any component deviation as a system-level failure, leading to over-aggressive fallbacks or outages. Fix: Design layered fault-tolerance so component-level faults are absorbed before becoming user-visible failures.
- Ignoring Error Handling Paths: Shipping code without exercising fault-tolerance machinery, leaving critical bugs dormant in error-handling branches. Fix: Use deliberate fault injection (chaos engineering) to continuously test recovery paths.
- Preventing Faults Instead of Tolerating Them (where cure exists): Spending all effort on prevention when the fault type is recoverable, leaving no resilience for when prevention fails. Fix: Prefer tolerance mechanisms for recoverable faults; reserve prevention-only strategy for irreversible faults like security breaches.
- Opaque Composite Systems: Combining multiple data tools without clearly defining consistency guarantees at the API boundary, leaving clients exposed to partial-update anomalies. Fix: Explicitly define and enforce cross-component guarantees (e.g., cache invalidation on write) as part of the service contract.

## When To Apply

Load this page when:

- Use this when choosing between multiple database or storage technologies for a new service and need a principled framework for evaluating trade-offs.
- Use this when designing a service that combines a primary database with a cache, search index, or message queue and must define consistency guarantees at the API boundary.
- Use this when a generated system design has no explicit error-handling or fault-recovery logic and needs resilience patterns applied.
- Use this when estimating whether a single tool (e.g., PostgreSQL alone) is sufficient or whether the workload requires composing specialized components.
- Use this when writing integration code that keeps secondary data stores (caches, search indexes) in sync with a primary database.
- Use this when evaluating whether a system design satisfies reliability, scalability, and maintainability requirements before committing to an architecture.
- Use this when a codebase shows signs of the 'Big Ball of Mud' anti-pattern and needs to be decomposed into maintainable, operable components.

## Concrete Examples

- Twitter home timeline fan-out: used as an example of describing load quantitatively when choosing between write-time fan-out vs. read-time aggregation.
- Redis used as both a data store and message queue — illustrating blurred boundaries between traditional tool categories.
- Kafka as a message queue with database-like durability guarantees — another example of tools escaping their original category.
- Application combining memcached/Elasticsearch with a primary database, where application code must keep cache and search index in sync with the main DB.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 1: Reliable, Scalable, and Maintainable Applications**

An LLM coding agent is prone to defaulting to a single-tool solution (e.g., one database for everything) because training data overrepresents simple architectures, missing the composite-system design responsibility described here. The fault-vs-failure distinction is especially critical for agents: LLM-generated code often omits error-handling branches entirely, meaning component faults immediately become user-visible failures with no tolerance layer. Agents should explicitly audit generated data-layer code against the Reliability-Scalability-Maintainability triad before finalizing architecture decisions, treating missing fault-tolerance as a code smell requiring deliberate remediation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
