---
name: data-systems-engineering
description: "Use when designing, evaluating, or debugging data-intensive systems — storage engines, replication, partitioning, transactions, distributed consistency, batch/stream processing, or encoding."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [databases, replication, partitioning, transactions, streaming, encoding, consistency, swe-foundations]
    category: swe-foundations
    related_skills: [distributed-systems, modular-architecture, production-readiness, agentic-swe-master]
---

# Data-Systems Engineering

## When to Load

- Use this when choosing between SQL, document, graph, or column-oriented storage for a new service
- Use this when designing replication topology (leader-follower, multi-leader, leaderless) and quorum configs
- Use this when partitioning or sharding a dataset that outgrows a single node — key-range vs. hash vs. compound key
- Use this when evaluating transaction isolation levels and what race conditions remain at each level
- Use this when debugging intermittent data anomalies (lost updates, phantom reads, stale reads) under concurrency
- Use this when choosing an encoding format (JSON, Protobuf, Avro, Thrift) for data crossing service boundaries
- Use this when designing a batch or stream processing pipeline and reasoning about correctness and fault tolerance
- Use this when evaluating consistency guarantees in a distributed system (linearizability vs. eventual vs. causal)
- Use this when generated system design has no explicit fault-handling — applying resilience patterns
- Use this when keeping secondary data stores (cache, search index) in sync with a primary database

## Core Rules

> A fault is not the same as a failure. A fault is one component deviating from its spec; a failure is when the system stops providing the required service. Design fault-tolerance mechanisms to prevent faults from cascading into failures.

> It is impossible to reduce the probability of a fault to zero. Therefore it is best to design fault-tolerance mechanisms that prevent faults from causing failures — and deliberately triggering faults uncovers poor error-handling before natural failures do.

> Scalability means having strategies for keeping performance good as load increases. Profile load characteristics (fan-out, read/write ratio, key distribution) before choosing architecture — there is no single answer.

> LSM-trees are typically faster for writes; B-trees are typically faster for reads. Well-chosen indexes speed up reads but slow down writes. Never index everything by default.

> All of the difficulty in replication lies in handling changes to replicated data. Asynchronous replication is almost inevitable at scale — a write acknowledged by the leader may be lost on failover if followers haven't caught up.

> If partitioning is unfair (hot spots), scale-out fails. A monotonically increasing key sends all writes to one partition. Use hash partitioning for even distribution, but lose range-query ability.

> ACID has become a marketing term. Understand which race conditions (dirty reads, lost updates, phantoms, write skew) a given isolation level actually prevents. Be precise about what "consistency" means in context.

> In distributed systems, the absence of a response does not mean an operation failed — it may already be applied. Add retry logic only with idempotency. Assume something is always broken at scale.

> Systems with stronger consistency guarantees may have worse performance or lower fault-tolerance. Linearizability prevents split-brain but kills availability during network partitions.

> Immutable inputs and explicit outputs: batch jobs should read input without modifying it and write output to a new location. This makes reruns safe, debugging possible, and correctness provable.

## Concept Map

Wiki root: $AGENTIC_SWE_WIKI_ROOT/designing-data-intensive-applications/concepts/

| Concept | When to read |
|---------|-------------|
| Reliability-Scalability-Maintainability.md | First principles for any data-intensive design |
| Storage-Engines.md | Choosing between LSM-tree and B-tree based engines |
| Replication-Strategies.md | Designing leader-follower, multi-leader, or leaderless topologies |
| Partitioning-Strategies.md | Sharding decision — key-range vs hash, secondary index placement |
| Transactions-and-Isolation.md | Race conditions, isolation levels, ACID guarantees |
| Distributed-Consistency-Models.md | Linearizability, causal consistency, eventual consistency trade-offs |
| Encoding-and-Schema-Evolution.md | Format choice, backward/forward compatibility, schema changes |
| Batch-Processing-Patterns.md | MapReduce model, join strategies, output correctness |
| Stream-Processing-Patterns.md | Event streams, windowing, exactly-once semantics |
| Distributed-Systems-Fault-Model.md | Unreliable networks, clocks, process pauses, Byzantine faults |

## AI-Native Application

LLM coding agents fail on data systems work in three specific ways:

1. Single-node mental model: Agents generate distributed code as if it runs on a single reliable machine — no retry logic, no idempotency, no partial failure handling. Treat the absence of explicit fault handling in any generated network or database code as a required fix, not an optional improvement.

2. Default to strongest consistency: Agents frequently suggest "just use a transaction" or "add a distributed lock" without evaluating whether the use case actually requires linearizability. Audit consistency requirements before recommending solutions.

3. Schema changes treated as atomic: Agents propose field renames or type changes as if all services deploy simultaneously. Any schema change crossing a service boundary must be backward and forward compatible for at least one full deployment cycle.

## Common Pitfalls

- **Single-Tool Assumption**: Using one database for OLTP, analytics, and search. Fix — decompose by access pattern; use specialized tools behind a clean API.
- **Naive Failover**: Nodes independently decide they are leader, causing split-brain. Fix — use a consensus protocol for leader election; fence old leaders before promoting new ones.
- **Ignoring Replication Lag in Read Paths**: Routing reads to any replica surfaces stale data. Fix — route reads after writes to the leader or require monotonic read guarantees.
- **Language-Native Serialization**: Java Serializable, Python pickle — security vulnerabilities, no forward/backward compat. Fix — use language-neutral formats with explicit schema evolution rules.
- **Retry Without Idempotency**: Blind retries cause duplicate side effects. Fix — make all operations idempotent before adding retry logic.
- **Polling a Non-Purpose-Built Store for Events**: Polling a relational DB for new rows as an event bus causes lock contention and latency. Fix — use a purpose-built log with change-data-capture.

## Verification Checklist

- [ ] Storage engine choice matches read/write ratio and access pattern
- [ ] Replication topology chosen with explicit failover and consistency trade-off stated
- [ ] Partitioning strategy avoids hot spots for the expected key distribution
- [ ] Isolation level chosen with explicit list of which race conditions are tolerated
- [ ] All cross-boundary encoding formats have explicit schema evolution rules
- [ ] Retry logic exists only on idempotent operations
- [ ] Batch jobs read immutable input and write to new output locations
