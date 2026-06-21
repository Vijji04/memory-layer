---
title: Data-Intensive Systems Engineering — Overview
created: 2026-05-12
updated: 2026-05-12
type: overview
tags: [phase-1, designing-data-intensive-applications]
---

# Data-Intensive Systems Engineering

> Phase 1 knowledge domain. 69 concept pages.

## What This Wiki Covers

This wiki encodes the core frameworks, heuristics, and agent-applicable patterns
from deep study of the Phase 1 curriculum: **Data-Intensive Systems Engineering**.

It is not a book summary. It is a structured knowledge base — each page is a
named concept with full detail: principle, heuristics, anti-patterns, examples,
and AI-native application guidance.

## Core Themes

- **Part III: Derived Data:** Part III introduces the foundational distinction between systems of record (authoritative, normalized, written first) and derived data systems (recomputable transformations such as caches, indexes, an...

- **Part II: Distributed Data:** Part II introduces the three architectures for scaling data across machines — shared-memory, shared-disk, and shared-nothing — and establishes shared-nothing (horizontal scaling) as the dominant parad...

- **Part I: Foundations of Data Systems:** Part I establishes the conceptual vocabulary and analytical frameworks for reasoning about any data system: reliability, scalability, and maintainability as evaluative lenses; data models, query langu...

- **Chapter 1: Reliable, Scalable, and Maintainable Applications:** Data-intensive applications are built from composable, specialized tools (databases, caches, queues, search indexes) and the engineer's job is to design their combination to satisfy reliability (corre...

- **Chapter 2: Data Models and Query Languages:** Data models are the most consequential architectural decision in software because they shape both implementation and thinking; systems are built from layered abstractions where each layer hides the co...

## Concept Index (quick nav)

All concepts in this wiki:

- [[ACID-Atomicity-Consistency-Isolation-Durability-the-four-safety-guarantees-that-]] — ACID: Atomicity, Consistency, Isolation, Durability — the four safety guarantees that transactions provide, each with distinct meanings and responsibilities (A/I/D are database properties; C is an application property)
- [[B-Tree-Index-page-oriented-mutable-tree-structure-that-overwrites-pages-in-place]] — B-Tree Index: page-oriented mutable tree structure that overwrites pages in-place, using write-ahead logs for crash recovery and offering predictable O(log n) reads and writes
- [[Backpressure-Mechanism-When-consumers-are-slower-than-producers-the-system-block]] — Backpressure Mechanism: When consumers are slower than producers, the system blocks producers rather than dropping messages or growing unbounded queues (as Unix pipes and TCP implement)
- [[BackwardForward-Compatibility-Duality-A-two-directional-compatibility-model-wher]] — Backward/Forward Compatibility Duality: A two-directional compatibility model where backward compatibility means newer code can read older data, and forward compatibility means older code can read data written by newer code — both must be maintained simultaneously during rolling upgrades
- [[Chaos-Engineering-Deliberate-Fault-Injection-Intentionally-triggering-faults-eg-]] — Chaos Engineering / Deliberate Fault Injection: Intentionally triggering faults (e.g., Netflix Chaos Monkey) to continuously exercise fault-tolerance machinery and surface poor error-handling before natural failures occur
- [[Column-Oriented-Storage-storing-each-columns-values-contiguously-on-disk-rather-]] — Column-Oriented Storage: storing each column's values contiguously on disk rather than rows, enabling compression and skipping entire columns irrelevant to a query
- [[Composite-Data-System-Architecture-Breaking-application-requirements-into-tasks-]] — Composite Data System Architecture: Breaking application requirements into tasks handled by best-fit single tools (Redis, Kafka, Elasticsearch, Postgres) stitched together by application code, with the API hiding implementation details
- [[Conflict-Resolution-via-CRDTsLWWVersion-Vectors-Mechanisms-for-reconciling-diver]] — Conflict Resolution via CRDTs/LWW/Version Vectors: Mechanisms for reconciling divergent replica state, including last-write-wins, merge functions, and version vectors to track causal dependencies
- [[Consensus-Abstraction-A-general-purpose-distributed-primitive-requiring-all-node]] — Consensus Abstraction: A general-purpose distributed primitive requiring all nodes to agree on a value, used to implement leader election, atomic commits, and other coordination tasks reliably despite faults
- [[Consistent-Hashing-randomly-chosen-partition-boundaries-to-avoid-central-control]] — Consistent Hashing: randomly chosen partition boundaries to avoid central control, historically misnamed and rarely used correctly in databases — prefer the term 'hash partitioning'
- [[Data-Model-vs-Query-Language-Separation-The-idea-that-the-visible-interface-quer]] — Data Model vs Query Language Separation: The idea that the visible interface (query language) and the underlying model (relational, document, graph) are distinct layers with independent tradeoffs
- [[Data-System-Designer-Pattern-When-you-combine-multiple-specialized-tools-cache-D]] — Data System Designer Pattern: When you combine multiple specialized tools (cache, DB, search index, queue) behind a single API, you become a data system designer responsible for cross-component consistency guarantees
- [[Dataflow-Clarity-Model-Making-explicit-which-system-produces-which-data-and-whic]] — Dataflow Clarity Model: Making explicit which system produces which data and which systems consume it, exposing the dependency graph of the entire architecture
- [[Dataflow-Graph-DAG-Execution-Model-Representing-batch-jobs-as-directed-acyclic-g]] — Dataflow Graph / DAG Execution Model: Representing batch jobs as directed acyclic graphs of operators with explicit data dependencies, enabling optimized scheduling and avoiding unnecessary materialization
- [[Derived-Data-System-Any-store-whose-contents-can-be-recomputed-from-a-system-of-]] — Derived Data System: Any store whose contents can be recomputed from a system of record, including caches, indexes, materialized views, and denormalized tables
- [[Document-Model-Data-stored-as-self-contained-JSONXML-documents-optimized-for-one]] — Document Model: Data stored as self-contained JSON/XML documents, optimized for one-to-many tree-structured data and locality of access
- [[Document-Partitioned-Local-Secondary-Index-secondary-indexes-live-in-the-same-pa]] — Document-Partitioned (Local) Secondary Index: secondary indexes live in the same partition as the primary data, so writes are local but reads require scatter/gather across all partitions
- [[Encoding-Format-Spectrum-A-classification-of-data-serialization-formats-from-lan]] — Encoding Format Spectrum: A classification of data serialization formats from language-specific (most brittle, most convenient) to binary schema-driven (most compact, most evolvable) to human-readable text formats (most interoperable, least efficient)
- [[Event-Sourcing-Representing-all-state-changes-as-an-immutable-append-only-log-of]] — Event Sourcing: Representing all state changes as an immutable, append-only log of events, from which current state can be derived by replaying
- [[Eventual-Consistency-Convergence-A-weak-guarantee-that-all-replicas-will-converg]] — Eventual Consistency (Convergence): A weak guarantee that all replicas will converge to the same value if writes stop, but provides no bound on when convergence occurs or what reads may return in the interim
- [[Fault-vs-Failure-Distinction-A-fault-is-a-single-component-deviating-from-spec-a]] — Fault vs. Failure Distinction: A fault is a single component deviating from spec; a failure is the whole system stopping service. Design fault-tolerance mechanisms to prevent faults from cascading into failures
- [[Fault-Tolerant-Abstraction-Pattern-The-strategy-of-implementing-general-purpose-]] — Fault-Tolerant Abstraction Pattern: The strategy of implementing general-purpose guarantees once (e.g., consensus, transactions) so applications can rely on them without reasoning about underlying failures
- [[Graph-Data-Model-Nodes-and-edges-used-to-represent-data-with-complex-many-to-man]] — Graph Data Model: Nodes and edges used to represent data with complex many-to-many relationships, enabling traversal queries across highly connected entities
- [[HPC-vs-Cloud-Fault-Philosophy-Supercomputers-escalate-partial-failure-to-total-f]] — HPC vs Cloud Fault Philosophy: Supercomputers escalate partial failure to total failure (crash everything, restart from checkpoint); internet services must tolerate partial failure in-place and keep serving users
- [[Hash-Index-in-memory-hash-map-mapping-keys-to-byte-offsets-in-an-append-only-log]] — Hash Index: in-memory hash map mapping keys to byte offsets in an append-only log file, enabling O(1) reads at the cost of requiring all keys to fit in RAM
- [[Hash-Partitioning-apply-a-hash-function-to-keys-so-each-partition-owns-a-range-o]] — Hash Partitioning: apply a hash function to keys so each partition owns a range of hashes, distributing load evenly at the cost of range query efficiency
- [[Isolation-Levels-Hierarchy-A-spectrum-from-weakest-read-uncommitted-to-strongest]] — Isolation Levels Hierarchy: A spectrum from weakest (read uncommitted) to strongest (serializable) isolation, each preventing different classes of race conditions at different performance costs
- [[Key-Range-Partitioning-assign-contiguous-sorted-key-ranges-to-partitions-enablin]] — Key Range Partitioning: assign contiguous sorted key ranges to partitions, enabling efficient range scans but risking hot spots on monotonically increasing keys
- [[Lambda-Streaming-Batch-Duality-Stream-processing-is-the-unbounded-continuously-p]] — Lambda / Streaming-Batch Duality: Stream processing is the unbounded, continuously-processed counterpart to batch processing, with analogous concepts (events ↔ records, topics ↔ files)
- [[Lambda-Architecture-Reprocessing-Pattern-Maintaining-a-batch-layer-for-recomputi]] — Lambda Architecture / Reprocessing Pattern: Maintaining a batch layer for recomputing outputs from raw data alongside a serving layer, enabling correction of bugs and schema changes by replaying immutable input logs
- [[Layered-Data-Model-Abstraction-Each-layer-in-a-system-represents-data-in-terms-o]] — Layered Data Model Abstraction: Each layer in a system represents data in terms of the layer below it, hiding complexity via a clean interface — from real-world objects down to bytes on disk
- [[Leader-Based-Replication-ActivePassive-One-node-accepts-all-writes-and-propagate]] — Leader-Based Replication (Active/Passive): One node accepts all writes and propagates changes to read-only followers via a replication log
- [[Leaderless-Replication-Dynamo-style-Clients-write-to-multiple-replicas-in-parall]] — Leaderless Replication (Dynamo-style): Clients write to multiple replicas in parallel using quorum reads/writes (w + r > n) to tolerate node failures without a single leader
- [[Linearizability-A-consistency-model-that-makes-a-distributed-system-appear-as-if]] — Linearizability: A consistency model that makes a distributed system appear as if there is only one copy of the data, with all operations atomic and reads always returning the most recent write (a recency guarantee)
- [[Log-Structured-Storage-append-only-write-model-using-immutable-segments-with-per]] — Log-Structured Storage: append-only write model using immutable segments with periodic compaction and merging to reclaim space and maintain read performance
- [[MapReduce-Programming-Model-A-two-phase-distributed-batch-pattern-map-to-emit-ke]] — MapReduce Programming Model: A two-phase distributed batch pattern (map to emit key-value pairs, reduce to aggregate by key) enabling fault-tolerant parallel processing across commodity hardware
- [[Message-Broker-Pattern-A-centralized-durable-intermediary-eg-Kafka-RabbitMQ-buff]] — Message Broker Pattern: A centralized, durable intermediary (e.g. Kafka, RabbitMQ) buffers messages between producers and consumers, tolerating client disconnects and providing replay
- [[Multi-Leader-Replication-Multiple-nodes-accept-writes-independently-requiring-co]] — Multi-Leader Replication: Multiple nodes accept writes independently, requiring conflict detection and resolution strategies for concurrent writes to the same record
- [[Non-Byzantine-Fault-Assumption-This-chapter-assumes-nodes-may-crash-or-behave-er]] — Non-Byzantine Fault Assumption: This chapter assumes nodes may crash or behave erratically but do not deliberately lie or send maliciously crafted messages — simplifying the fault model
- [[OLTP-vs-OLAP-Distinction-two-fundamentally-different-access-patterns-transaction]] — OLTP vs OLAP Distinction: two fundamentally different access patterns — transactional (many small random-access reads/writes) vs. analytic (few large sequential scans over aggregate data) — requiring different storage engine designs
- [[OnlineBatchStream-Trichotomy-A-classification-of-data-processing-systems-into-se]] — Online/Batch/Stream Trichotomy: A classification of data processing systems into services (request/response, latency-sensitive), batch processors (offline, throughput-optimized, fixed input), and stream processors (near-real-time, event-driven)
- [[Partial-Failure-Model-In-distributed-systems-some-components-fail-unpredictably-]] — Partial Failure Model: In distributed systems, some components fail unpredictably while others keep working, producing non-deterministic outcomes unlike the binary fail/work model of single-node computers
- [[Polyglot-Persistence-The-architectural-pattern-of-using-multiple-different-data-]] — Polyglot Persistence: The architectural pattern of using multiple different data storage technologies in one application, each chosen for its specific use-case fit
- [[Publish-Subscribe-Model-Producers-emit-events-to-named-topics-multiple-consumers]] — Publish-Subscribe Model: Producers emit events to named topics; multiple consumers independently subscribe and process those events, decoupling producers from consumers
- [[Relational-Model-Data-organized-into-relations-tables-of-unordered-tuples-rows-d]] — Relational Model: Data organized into relations (tables) of unordered tuples (rows), designed to hide internal storage representation behind a clean querying interface
- [[Reliability-Scalability-Maintainability-Triad-The-three-foundational-concerns-fo]] — Reliability-Scalability-Maintainability Triad: The three foundational concerns for data-intensive systems — correctness under adversity, performance under growth, and long-term workability by multiple engineers
- [[Reliability-Scalability-Maintainability-Triad-The-three-foundational-properties-]] — Reliability-Scalability-Maintainability Triad: The three foundational properties used to evaluate any data system design decision
- [[Reliable-Systems-from-Unreliable-Components-Higher-level-reliability-can-be-cons]] — Reliable Systems from Unreliable Components: Higher-level reliability can be constructed from lower-level unreliable primitives (e.g., TCP over IP, ECC over noisy channels), but always with an upper bound on achievable reliability
- [[Replication-Lag-Consistency-Guarantees-A-spectrum-of-consistency-models-read-you]] — Replication Lag Consistency Guarantees: A spectrum of consistency models (read-your-writes, monotonic reads, consistent prefix reads) that provide partial ordering guarantees weaker than full linearizability
- [[Replication-vs-Partitioning-Duality-two-orthogonal-but-complementary-mechanisms-]] — Replication vs. Partitioning Duality: two orthogonal but complementary mechanisms — replication copies data across nodes for redundancy/performance, partitioning splits data across nodes for scale
- [[Rolling-Upgrade-Staged-Rollout-A-deployment-strategy-where-new-code-versions-are]] — Rolling Upgrade / Staged Rollout: A deployment strategy where new code versions are deployed to a subset of nodes at a time, requiring that old and new code versions coexist and interoperate without breaking the system
- [[SSTableLSM-Tree-sorted-string-tables-merged-via-log-structured-merge-strategy-ke]] — SSTable/LSM-Tree: sorted string tables merged via log-structured merge strategy, keeping data sorted by key to enable efficient range scans and merge operations
- [[Schema-Evolution-Compatibility-Matrix-The-set-of-rules-governing-which-field-add]] — Schema Evolution Compatibility Matrix: The set of rules governing which field additions, removals, and type changes are safe under each encoding format (Thrift, Protocol Buffers, Avro), determining what constitutes a backward- or forward-compatible schema change
- [[Schema-Evolution-and-Encoding-Compatibility-The-framework-for-evaluating-data-se]] — Schema Evolution and Encoding Compatibility: The framework for evaluating data serialization formats by how well they handle changing application requirements over time
- [[Schema-on-Read-vs-Schema-on-Write-The-distinction-between-document-databases-sch]] — Schema-on-Read vs Schema-on-Write: The distinction between document databases (schema interpreted at read time) and relational databases (schema enforced at write time)
- [[Semi-Synchronous-Replication-Exactly-one-follower-is-synchronous-guaranteeing-du]] — Semi-Synchronous Replication: Exactly one follower is synchronous (guaranteeing durability on two nodes) while others remain asynchronous, balancing safety and availability
- [[Serializable-Snapshot-Isolation-SSI-An-optimistic-concurrency-control-algorithm-]] — Serializable Snapshot Isolation (SSI): An optimistic concurrency control algorithm that detects write skew and phantom anomalies at commit time, providing full serializability with lower overhead than 2PL
- [[Shared-Disk-Architecture-independent-CPUsRAM-per-machine-but-a-shared-disk-array]] — Shared-Disk Architecture: independent CPUs/RAM per machine but a shared disk array; limited by contention and locking overhead
- [[Shared-Memory-Architecture-all-CPUs-RAM-and-disks-under-one-OS-treated-as-a-sing]] — Shared-Memory Architecture: all CPUs, RAM, and disks under one OS treated as a single machine; scales vertically but at super-linear cost
- [[Shared-Nothing-Architecture-each-node-owns-its-CPU-RAM-and-disk-independently-co]] — Shared-Nothing Architecture: each node owns its CPU, RAM, and disk independently; coordination is purely at the software level via conventional networking
- [[Shared-Nothing-Cluster-Partitioning-distributing-data-across-independent-nodes-s]] — Shared-Nothing Cluster Partitioning: distributing data across independent nodes so each node independently executes queries for its own partition, enabling horizontal scale-out
- [[Snapshot-Isolation-MVCC-Each-transaction-reads-from-a-consistent-snapshot-of-the]] — Snapshot Isolation / MVCC: Each transaction reads from a consistent snapshot of the database at transaction start, using multi-version concurrency control to allow readers and writers to not block each other
- [[Storage-Engine-Workload-Alignment-The-principle-that-storage-engines-are-optimiz]] — Storage Engine Workload Alignment: The principle that storage engines are optimized for specific access patterns and must be matched to the workload rather than used generically
- [[System-of-Record-Source-of-Truth-The-authoritative-normalized-store-where-data-i]] — System of Record (Source of Truth): The authoritative, normalized store where data is first written; discrepancies are resolved in its favor by definition
- [[Term-Partitioned-Global-Secondary-Index-secondary-indexes-are-partitioned-by-the]] — Term-Partitioned (Global) Secondary Index: secondary indexes are partitioned by the indexed term, so reads hit one partition but writes must update multiple index partitions
- [[Transaction-Isolation-vs-Distributed-Consistency-A-conceptual-separation-disting]] — Transaction Isolation vs. Distributed Consistency: A conceptual separation distinguishing race-condition avoidance (isolation) from replica-state coordination under delays and faults (distributed consistency)
- [[Two-Phase-Locking-2PL-A-pessimistic-concurrency-control-mechanism-where-readers-]] — Two-Phase Locking (2PL): A pessimistic concurrency control mechanism where readers block writers and writers block readers, providing serializable isolation by preventing all race conditions via lock acquisition and release phases
- [[Unix-Pipeline-Model-Composing-small-single-purpose-tools-via-stdinstdout-pipes-t]] — Unix Pipeline Model: Composing small, single-purpose tools via stdin/stdout pipes to form powerful data transformations — the philosophical ancestor of distributed batch frameworks
- [[Working-Set-vs-Sort-Merge-Trade-off-Choosing-between-in-memory-hash-aggregation-]] — Working Set vs. Sort-Merge Trade-off: Choosing between in-memory hash aggregation (fast when working set fits in RAM) and sort-based aggregation (disk-friendly, sequential I/O, scales beyond memory)

## How to Use This Wiki

**For agents:** Load the thin skill file (`output/skills/`) first.
The skill's concept map tells you which page to read for a given situation.
Read the concept page when you need depth — not the whole wiki.

**For humans:** Browse in Obsidian. Start here, follow wikilinks.
Use the graph view to see which concepts are most connected.

## Related Wikis

<!-- Populated after all book wikis are built -->
