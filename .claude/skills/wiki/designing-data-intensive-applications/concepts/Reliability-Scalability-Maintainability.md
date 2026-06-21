# Reliability-Scalability-Maintainability

## Chaos Engineering / Deliberate Fault Injection: Intentionally triggering faults (e.g., Netflix Chaos Monkey) to continuously exercise fault-tolerance machinery and surface poor error-handling before natural failures occur

---
title: Chaos Engineering / Deliberate Fault Injection: Intentionally triggering faults (e.g., Netflix Chaos Monkey) to continuously exercise fault-tolerance machinery and surface poor error-handling before natural failures occur
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-1-Reliable-Scalable-and-Maintainable-Applications.json]
contributing_chapters: ["Chapter 1: Reliable, Scalable, and Maintainable Applications"]
confidence: high
---


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

---

## Fault vs. Failure Distinction: A fault is a single component deviating from spec; a failure is the whole system stopping service. Design fault-tolerance mechanisms to prevent faults from cascading into failures

---
title: Fault vs. Failure Distinction: A fault is a single component deviating from spec; a failure is the whole system stopping service. Design fault-tolerance mechanisms to prevent faults from cascading into failures
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-1-Reliable-Scalable-and-Maintainable-Applications.json]
contributing_chapters: ["Chapter 1: Reliable, Scalable, and Maintainable Applications"]
confidence: high
---


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

---

## Reliability-Scalability-Maintainability Triad: The three foundational concerns for data-intensive systems — correctness under adversity, performance under growth, and long-term workability by multiple engineers

---
title: Reliability-Scalability-Maintainability Triad: The three foundational concerns for data-intensive systems — correctness under adversity, performance under growth, and long-term workability by multiple engineers
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-1-Reliable-Scalable-and-Maintainable-Applications.json]
contributing_chapters: ["Chapter 1: Reliable, Scalable, and Maintainable Applications"]
confidence: high
---


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

---

## Reliability-Scalability-Maintainability Triad: The three foundational properties used to evaluate any data system design decision

---
title: Reliability-Scalability-Maintainability Triad: The three foundational properties used to evaluate any data system design decision
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-I-Foundations-of-Data-Systems.json]
contributing_chapters: ["Part I: Foundations of Data Systems"]
confidence: high
---


> From chapter: *Part I: Foundations of Data Systems*

## Core Principle

Part I establishes the conceptual vocabulary and analytical frameworks for reasoning about any data system: reliability, scalability, and maintainability as evaluative lenses; data models, query languages, storage engines, and serialization formats as independently variable design dimensions. The section deliberately addresses single-machine fundamentals before tackling distributed complexity in Part II. Mastery of these foundations is prerequisite to making principled tradeoffs in system design.

## Key Heuristics

These are the load-bearing rules for this concept.

> Different storage engines are optimized for different workloads, and choosing the right one can have a huge effect on performance.

> Different models are appropriate to different situations.

> Schemas need to adapt over time.

> Reliability, scalability and maintainability — examine what we actually mean with these words and how we can try to achieve them.

## Anti-Patterns & Fixes

- One-Size-Fits-All Storage Engine: Defaulting to a single storage engine regardless of workload type. Fix: Evaluate whether the workload is read-heavy, write-heavy, or mixed and select the engine optimized for that pattern.
- Ignoring Schema Evolution in Serialization Choice: Choosing a data encoding format based only on current schema without considering future changes. Fix: Evaluate serialization formats (e.g., Avro, Protobuf, Thrift) explicitly on their schema migration and backward/forward compatibility guarantees.
- Treating Reliability/Scalability/Maintainability as Synonyms: Using these terms loosely or interchangeably leads to vague system requirements. Fix: Define each property precisely and separately when specifying or reviewing a system.
- Conflating Data Model with Query Language: Assuming a given query language implies a specific data model or vice versa. Fix: Evaluate data model and query language as independent dimensions when selecting a database.

## When To Apply

Load this page when:

- Use this when selecting a database for a new service and needing a framework to compare options across model, engine, and encoding dimensions.
- Use this when a system is underperforming and the cause may be a mismatch between storage engine choice and actual workload characteristics.
- Use this when designing a data schema that will need to evolve as application requirements change, requiring evaluation of serialization format compatibility.
- Use this when writing a system design document and needing precise definitions of reliability, scalability, and maintainability to anchor requirements.
- Use this when a distributed system design is being initiated and foundational single-machine concepts need to be established before addressing distributed-specific concerns.
- Use this when reviewing a data pipeline and needing to assess whether the encoding format supports backward and forward compatibility for schema changes.

## Concrete Examples

- Chapter 1 examines the specific meanings of reliability, scalability, and maintainability as concrete engineering goals.
- Chapter 2 compares multiple data models and query languages as the most visible difference between databases from a developer's perspective.
- Chapter 3 examines how databases lay out data on disk as a concrete illustration of storage engine internals.
- Chapter 4 examines how serialization formats handle schema changes over time as a concrete evaluation criterion.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Part I: Foundations of Data Systems**

An LLM coding agent is prone to defaulting to the most statistically common technology choice (e.g., PostgreSQL, JSON serialization) without evaluating workload fit, schema evolution needs, or scalability requirements — exactly the failure modes this framework prevents. By anchoring decisions to the RSM triad and explicit model/engine/encoding axes, an agent can be prompted to justify each technology choice against concrete criteria rather than pattern-matching to familiar stacks. This also prevents agents from conflating distinct concerns (e.g., treating a document store as a drop-in for a relational one) when generating infrastructure or data-layer code.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Reliable Systems from Unreliable Components: Higher-level reliability can be constructed from lower-level unreliable primitives (e.g., TCP over IP, ECC over noisy channels), but always with an upper bound on achievable reliability

---
title: Reliable Systems from Unreliable Components: Higher-level reliability can be constructed from lower-level unreliable primitives (e.g., TCP over IP, ECC over noisy channels), but always with an upper bound on achievable reliability
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-8-The-Trouble-with-Distributed-Systems.json]
contributing_chapters: ["Chapter 8: The Trouble with Distributed Systems"]
confidence: high
---


> From chapter: *Chapter 8: The Trouble with Distributed Systems*

## Core Principle

Distributed systems differ fundamentally from single-node systems because partial failures — where some components fail while others keep working — are non-deterministic and unavoidable at scale. Unlike single computers designed to either work perfectly or crash cleanly, distributed systems require engineers to assume failures will occur and build fault tolerance directly into the software design. The chapter establishes the foundational pessimistic mindset: anything that can go wrong will, timeouts leave outcomes ambiguous, and reliable systems must be deliberately constructed from inherently unreliable components.

## Key Heuristics

These are the load-bearing rules for this concept.

> In distributed systems, suspicion, pessimism and paranoia pay off.

> We must accept the possibility of partial failure, and build fault tolerance mechanisms into the software.

> It is important to consider a wide range of possible faults — even fairly unlikely ones — and to artificially create such situations in your testing environment, to see what happens.

> It would be unwise to assume that faults are rare, and simply hope for the best.

> The fault handling must be part of the software design.

> In a system with thousands of nodes, it is reasonable to assume that something is always broken.

> If the error handling strategy consists of simply giving up, such a large system would never work.

## Anti-Patterns & Fixes

- Optimistic Fault Assumption: Assuming faults are rare and hoping for the best, leading to systems that fail catastrophically when partial failures occur. Fix: Design fault handling into the software from the start and test with artificially induced faults.
- Single-Node Mental Model Applied to Distributed Systems: Treating distributed code as if it runs on a reliable, deterministic single computer, ignoring network delays, partial failures, and non-determinism. Fix: Explicitly model partial failure, timeouts, and ambiguous outcomes (operation may have succeeded or failed — you may not know).
- Total-Failure Escalation in Online Services: Using the supercomputer strategy of stopping everything on any node failure, which is acceptable for batch jobs but causes unacceptable downtime for online services. Fix: Build systems that tolerate failed nodes and continue serving users, e.g., via rolling upgrades and node replacement.
- Weakest-Link Reliability Fallacy: Assuming the system can only be as reliable as its least reliable component. Fix: Layer reliability mechanisms (retries, replication, error-correcting codes) to exceed the reliability of individual components, while acknowledging there is always an upper bound.

## When To Apply

Load this page when:

- Use this when writing code that makes a network call and must decide what to do if no response is received — the operation may have succeeded, failed, or be in-flight.
- Use this when designing a service that must remain available while individual nodes are restarted, upgraded, or replaced.
- Use this when adding retry logic to a distributed operation — consider that the request may have already been applied once, requiring idempotency.
- Use this when choosing between failing fast (crash the process) vs. continuing with degraded functionality after a component error in a multi-node system.
- Use this when writing integration or chaos tests — partial failures must be explicitly injected because they will not surface reliably in normal test runs.
- Use this when a distributed operation produces no acknowledgment — the absence of a response does not mean the operation failed; it means the outcome is unknown.
- Use this when estimating system-wide failure rates as node count scales — assume at least one component is always broken in large clusters and code accordingly.

## Concrete Examples

- A hypoglycemic driver smashing a Ford pickup truck into a datacenter's HVAC system — illustrating the extreme real-world physical causes of distributed system failures.
- TCP providing reliable transport over unreliable IP by retransmitting lost packets, eliminating duplicates, and reordering — demonstrating reliable systems built from unreliable components.
- Error-correcting codes enabling accurate data transmission over a noisy wireless channel — another example of reliability layered over an unreliable substrate.
- Supercomputers checkpointing state to durable storage and restarting the entire cluster on any node failure — contrasted with the always-on requirement of internet services.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 8: The Trouble with Distributed Systems**

An LLM coding agent is especially prone to generating code that silently assumes success after a network call — it will write the happy path without modeling the 'response never arrived but operation may have executed' ambiguity, producing systems that corrupt state on retries or hang indefinitely. The agent also tends to copy single-node error handling patterns (try/catch + crash) into distributed contexts where crashing one service propagates failure rather than isolating it. Explicitly prompting the agent with partial-failure semantics and requiring it to handle unknown-outcome states prevents these silent correctness bugs.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->