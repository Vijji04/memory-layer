---
title: Shared-Memory Architecture: all CPUs, RAM, and disks under one OS treated as a single machine; scales vertically but at super-linear cost
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-II-Distributed-Data.json]
contributing_chapters: ["Part II: Distributed Data"]
confidence: high
---

# Shared-Memory Architecture: all CPUs, RAM, and disks under one OS treated as a single machine; scales vertically but at super-linear cost

> From chapter: *Part II: Distributed Data*

## Core Principle

Part II introduces the three architectures for scaling data across machines — shared-memory, shared-disk, and shared-nothing — and establishes shared-nothing (horizontal scaling) as the dominant paradigm requiring the most developer awareness. Data distribution is decomposed into two orthogonal mechanisms: replication (redundancy and performance) and partitioning/sharding (scale). The central thesis is that distributed systems expose irreducible complexity and trade-offs that no database can fully abstract away from the application developer.

## Key Heuristics

These are the load-bearing rules for this concept.

> Reality must take precedence over public relations, for nature cannot be fooled.

> A machine with twice as many CPUs, twice as much RAM and disk typically costs significantly more than twice as much.

> A machine twice the size cannot necessarily handle twice the load.

> In some cases, a simple single-threaded program can perform significantly better than a cluster with over 100 CPU cores.

> If your data is distributed across multiple nodes, you need to be aware of the constraints and trade-offs that occur in such a distributed system — the database cannot magically hide these from you.

> No special hardware is required by a shared-nothing system, so you can use whatever machines have the best price/performance ratio.

## Anti-Patterns & Fixes

- Reflexive Vertical Scaling: assuming that buying a bigger machine is the right solution to load growth. Fix: evaluate shared-nothing horizontal scaling first, especially when cost grows super-linearly or fault tolerance across geographic regions is required.
- Distribution Complexity Underestimation: treating a distributed system as equivalent to a single-machine system and expecting the database to hide trade-offs. Fix: explicitly design for distributed constraints — partition tolerance, replication lag, split-brain scenarios — at the application level.
- Premature Clustering: adding distributed infrastructure when a single-threaded program would outperform a 100-node cluster. Fix: benchmark single-machine solutions before distributing; distribute only when load or fault-tolerance requirements demonstrably exceed single-machine capacity.
- Conflating Replication and Partitioning: treating replication and partitioning as the same mechanism or assuming one implies the other. Fix: design each independently — replication for redundancy/read performance, partitioning for write/storage scale — then compose them deliberately.

## When To Apply

Load this page when:

- Use this when designing a data storage layer that must survive the failure of one or more nodes or an entire datacenter.
- Use this when a user's read/write load is projected to exceed what a single machine can handle and a cost-effective scaling strategy is needed.
- Use this when generating database schema or infrastructure code and needing to choose between vertical scaling, shared-disk, or shared-nothing topology.
- Use this when an application serves users across multiple geographic regions and low latency requires data placement decisions.
- Use this when evaluating whether to introduce a distributed datastore versus keeping a single-node solution with a simpler codebase.
- Use this when architecting replication and sharding strategies together, needing to understand their interaction (as in Figure II-1).
- Use this when a generated system design assumes the database abstracts away all consistency or availability trade-offs in a distributed setting.

## Concrete Examples

- Figure II-1: A database split into two partitions, each with two replicas, showing records (e.g., 'Four score and seven years ago') duplicated across nodes per partition.
- Non-Uniform Memory Access (NUMA) in large single machines as an example of partitioning being necessary even within a single ostensibly unified machine.
- Cloud VM multi-region deployments as a concrete case where shared-nothing distributed architecture is now feasible even for small companies, not just Google-scale operators.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Part II: Distributed Data**

An LLM coding agent is likely to generate distributed system code (e.g., microservices, multi-region configs) without explicitly modeling the failure modes and trade-offs that shared-nothing architectures impose, effectively assuming the database 'magically hides' consistency and availability issues. Unlike a human who reads error logs iteratively, an agent generating infrastructure-as-code or ORM layers in one shot may silently produce designs that assume single-machine semantics (e.g., synchronous cross-node transactions, global mutable state) in a distributed context. This framework forces the agent to gate any distributed data design decision through explicit replication-vs-partitioning decomposition and to surface — not suppress — the trade-offs to the requesting developer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
