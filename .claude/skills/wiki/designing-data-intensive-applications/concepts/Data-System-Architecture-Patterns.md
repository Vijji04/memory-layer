# Data-System-Architecture-Patterns

## Composite Data System Architecture: Breaking application requirements into tasks handled by best-fit single tools (Redis, Kafka, Elasticsearch, Postgres) stitched together by application code, with the API hiding implementation details

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

## Data System Designer Pattern: When you combine multiple specialized tools (cache, DB, search index, queue) behind a single API, you become a data system designer responsible for cross-component consistency guarantees

---
title: Data System Designer Pattern: When you combine multiple specialized tools (cache, DB, search index, queue) behind a single API, you become a data system designer responsible for cross-component consistency guarantees
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

## Shared-Disk Architecture: independent CPUs/RAM per machine but a shared disk array; limited by contention and locking overhead

---
title: Shared-Disk Architecture: independent CPUs/RAM per machine but a shared disk array; limited by contention and locking overhead
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-II-Distributed-Data.json]
contributing_chapters: ["Part II: Distributed Data"]
confidence: high
---


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

---

## Shared-Memory Architecture: all CPUs, RAM, and disks under one OS treated as a single machine; scales vertically but at super-linear cost

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

---

## Shared-Nothing Architecture: each node owns its CPU, RAM, and disk independently; coordination is purely at the software level via conventional networking

---
title: Shared-Nothing Architecture: each node owns its CPU, RAM, and disk independently; coordination is purely at the software level via conventional networking
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-II-Distributed-Data.json]
contributing_chapters: ["Part II: Distributed Data"]
confidence: high
---


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

---

## Shared-Nothing Cluster Partitioning: distributing data across independent nodes so each node independently executes queries for its own partition, enabling horizontal scale-out

---
title: Shared-Nothing Cluster Partitioning: distributing data across independent nodes so each node independently executes queries for its own partition, enabling horizontal scale-out
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-6-Partitioning.json]
contributing_chapters: ["Chapter 6: Partitioning"]
confidence: high
---


> From chapter: *Chapter 6: Partitioning*

## Core Principle

Partitioning breaks a large dataset into smaller independent shards distributed across nodes to achieve horizontal scalability; the two core strategies are key-range partitioning (preserves sort order, enables range scans, risks monotonic hot spots) and hash partitioning (uniform distribution, destroys range order). Secondary indexes add a second partitioning decision — local (document-partitioned) indexes keep writes cheap but reads expensive via scatter/gather, while global (term-partitioned) indexes make reads cheap but spread writes across multiple partitions. Rebalancing and request routing complete the picture, ensuring partitions move cleanly as cluster topology changes and queries reach the correct node.

## Key Heuristics

These are the load-bearing rules for this concept.

> If the partitioning is unfair, so that some partitions have more data or queries than others, we call it skewed. A partition with disproportionately high load is called a hot spot.

> The simplest approach of avoiding hot spots would be to assign records to nodes randomly — but when you're trying to read a particular item, you have no way of knowing which node it is on, so you would have to query all nodes in parallel.

> A good hash function takes skewed data and makes it uniformly distributed.

> By using the hash of the key for partitioning, we also lost a nice property of key-range partitioning: the ability to do efficient range queries.

> The partition boundaries need to adapt to the data [to distribute data evenly].

> Because [consistent hashing] is so confusing, it's best to avoid the term consistent hashing, and just call it hash partitioning instead.

> By design, every partition operates mostly independently — that's what allows a partitioned database to scale to multiple machines.

> The main goal of partitioning is to spread the data and the query load evenly across multiple machines, avoiding hot spots.

## Anti-Patterns & Fixes

- MonotonicKeyHotSpot: Using a monotonically increasing key (e.g., timestamp) as the partition key causes all writes to funnel into the single 'latest' partition, leaving other partitions idle. Fix: prefix the key with a high-cardinality field (e.g., sensor name) so writes are spread across partitions, then perform per-sensor range queries.
- RandomAssignmentPartitioning: Assigning records to nodes randomly distributes data evenly but makes reads require querying all nodes in parallel because there is no way to locate a specific record. Fix: use key-range or hash partitioning so queries can be routed to the correct partition directly.
- MisnamedConsistentHashing: Calling hash-based partitioning 'consistent hashing' introduces confusion with replica consistency and ACID consistency, and the original algorithm doesn't work well for databases. Fix: call it 'hash partitioning' and implement fixed-number-of-partitions or dynamic splitting instead.
- ScatterGatherOnLocalSecondaryIndex: Using document-partitioned secondary indexes means every secondary-index read must scatter to all partitions and gather results, causing high latency and fan-out. Fix: if read performance on secondary indexes is critical, use a term-partitioned (global) index so a single partition can serve the read.
- IgnoringRebalancingOnClusterChange: Adding or removing nodes without rebalancing leaves partitions unevenly distributed, recreating hot spots. Fix: use dynamic partition splitting (for key-range) or move whole pre-created partitions between nodes (for hash partitioning) when cluster topology changes.

## When To Apply

Load this page when:

- Use this when designing a data storage schema for a dataset that will exceed the capacity of a single node and must be distributed across multiple machines.
- Use this when choosing a primary key or shard key for a distributed database and the key candidate is a timestamp or other monotonically increasing value.
- Use this when a distributed system exhibits a 'hot spot' where one node handles disproportionately high read or write load while others are idle.
- Use this when adding secondary indexes to a partitioned database and deciding whether to store them locally (per-partition) or globally (term-partitioned).
- Use this when planning cluster topology changes (adding or removing nodes) and needing a strategy to redistribute data without full re-hashing.
- Use this when a query pattern requires range scans and you must choose between key-range partitioning (range-friendly) and hash partitioning (skew-resistant).
- Use this when evaluating whether a compound key strategy can satisfy both even distribution and range-query requirements simultaneously.
- Use this when an application writes sensor, log, or time-series data at high throughput and the natural key ordering would concentrate writes on one partition.

## Concrete Examples

- Print encyclopedia partitioned by key range: each volume covers an alphabetical range (e.g., vol 1: A–Bayes, vol 12: Trudeau–Zywiec), with uneven letter-frequency requiring adaptive boundaries rather than fixed two-letters-per-volume splits.
- Sensor network with timestamp keys: prefixing each timestamp with the sensor name distributes writes across partitions by sensor, then a per-sensor range query retrieves time-bounded readings.
- MD5 hash of similar timestamp strings producing uniformly distributed 16-bit values mapped to eight partitions (p0–p7), illustrated with six consecutive second-granularity timestamps.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 6: Partitioning**

An LLM coding agent generating data models or ORM schemas will often default to auto-increment IDs or timestamp-based keys as the natural primary key, inadvertently creating monotonic hot spots in any partitioned store — this chapter provides the named pattern (MonotonicKeyHotSpot) and explicit fix the agent should apply proactively. When an agent scaffolds secondary indexes on a sharded collection it must explicitly choose between local (document-partitioned) and global (term-partitioned) index strategies rather than accepting framework defaults, because the scatter/gather cost of local indexes is invisible at code-generation time but catastrophic at query time. Agents should also avoid generating code that references 'consistent hashing' as an API or configuration term, since the misnomer causes misconfiguration in real database drivers.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->