# OLTP-vs-OLAP-and-Columnar-Storage

## Column-Oriented Storage: storing each column's values contiguously on disk rather than rows, enabling compression and skipping entire columns irrelevant to a query

---
title: Column-Oriented Storage: storing each column's values contiguously on disk rather than rows, enabling compression and skipping entire columns irrelevant to a query
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-3-Storage-and-Retrieval.json]
contributing_chapters: ["Chapter 3: Storage and Retrieval"]
confidence: high
---


> From chapter: *Chapter 3: Storage and Retrieval*

## Core Principle

Chapter 3 explains how databases physically store and retrieve data by examining two engine families — log-structured (LSM-trees, SSTables, Bitcask) and page-oriented (B-trees) — and the indexing structures that make reads efficient at the cost of write overhead. It establishes the fundamental index trade-off (every index speeds reads but slows writes), the log-structured principle of append-only immutable segments with background compaction, and the critical OLTP vs. OLAP distinction that determines whether row-oriented or column-oriented storage is appropriate. The chapter equips developers to choose and tune storage engines by understanding what happens under the hood rather than treating the database as a black box.

## Key Heuristics

These are the load-bearing rules for this concept.

> well-chosen indexes speed up read queries, but every index slows down writes

> databases don't usually index everything by default, but require you to choose indexes manually, using your knowledge of the application's typical query patterns

> appending to a file is generally very efficient — for writes, it's hard to beat the performance of simply appending to a file, because that's the simplest possible write operation

> An index is an additional structure that is derived from the primary data — this doesn't affect the contents of the database, it only affects the performance of queries

> LSM-trees are typically faster for writes, whereas B-trees are thought to be faster for reads

> the cost of a lookup is O(n): if you double the number of records n in your database, a lookup takes twice as long

> Bitcask is well suited in situations where the value for each key is updated frequently and there are not too many distinct keys

## Anti-Patterns & Fixes

- Full-Scan Lookup: using a linear scan (O(n)) for every key lookup as dataset grows. Fix: add an index structure (hash map, B-tree, or SSTable) to reduce lookup cost to O(1) or O(log n).
- Unbounded Log Growth: appending updates forever without compaction causes disk exhaustion. Fix: segment the log at a fixed size and run background compaction to discard obsolete keys, then merge segments.
- Indexing Everything By Default: adding indexes on all columns increases write overhead for every insert/update. Fix: selectively index only fields matching the application's actual query patterns.
- Using Hash Index for Range Queries: hash indexes cannot efficiently answer range queries (e.g., all keys between X and Y). Fix: use a sorted index structure (B-tree or SSTable/LSM-tree) when range scans are required.
- Row-Oriented Storage for Analytic Workloads: reading entire rows when only a few columns are needed wastes I/O on OLAP queries. Fix: use column-oriented storage so only the relevant columns are read from disk.
- Ignoring Write-Ahead Log (WAL) in B-Trees: writing directly to B-tree pages without a WAL leaves the database unrecoverable after a crash mid-write. Fix: always append changes to a WAL before applying them to the tree pages.

## When To Apply

Load this page when:

- Use this when selecting or recommending a database storage engine for a new service and needing to match engine characteristics to workload access patterns.
- Use this when a key-value store with high write throughput and a bounded key space is needed and all keys can fit in memory (suggesting Bitcask/hash-index architecture).
- Use this when designing a system that must support range queries, indicating a sorted index (B-tree or LSM/SSTable) is required instead of a hash index.
- Use this when a write-heavy workload is causing index maintenance to become a bottleneck, triggering evaluation of log-structured (LSM-tree) storage over B-trees.
- Use this when building or configuring an analytics pipeline that scans large datasets and needs to minimize I/O by reading only relevant columns.
- Use this when a storage system is running out of disk space due to append-only logs, requiring implementation of log segmentation and compaction.
- Use this when evaluating whether to add a secondary index to a table, requiring explicit trade-off analysis between read speedup and write overhead.
- Use this when a system needs crash recovery guarantees on a B-tree storage engine, indicating a write-ahead log must be present.

## Concrete Examples

- Two-function Bash key-value store (db_set/db_get): db_set appends to a file; db_get greps the file — illustrates O(n) read cost and the value of append-only writes.
- Bitcask storage engine: in-memory hash map of keys to byte offsets in an append-only log file, used as the default engine in Riak.
- Cat video play-count workload: URL as key, play count as value updated frequently — used to illustrate the ideal Bitcask use case of high writes per key with bounded key space.
- Log compaction and segment merging diagram: duplicate keys (mew, purr, yawn) across two segments are compacted into a single merged segment retaining only the latest value per key.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 3: Storage and Retrieval**

An LLM coding agent generating data access code will default to the simplest retrieval pattern (linear scan or ORM fetch-all) without considering index design, replicating the O(n) db_get anti-pattern at scale. Agents are also prone to generating schemas that index every column 'to be safe,' incurring unnecessary write overhead — this chapter provides the explicit trade-off rule (reads vs. writes) the agent needs to make a justified, minimal indexing decision. Additionally, when an agent scaffolds a storage layer it may conflate OLTP and OLAP access patterns, producing row-oriented schemas for analytic workloads; the OLTP/OLAP distinction gives the agent a named decision gate to apply before emitting any storage schema.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## OLTP vs OLAP Distinction: two fundamentally different access patterns — transactional (many small random-access reads/writes) vs. analytic (few large sequential scans over aggregate data) — requiring different storage engine designs

---
title: OLTP vs OLAP Distinction: two fundamentally different access patterns — transactional (many small random-access reads/writes) vs. analytic (few large sequential scans over aggregate data) — requiring different storage engine designs
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-3-Storage-and-Retrieval.json]
contributing_chapters: ["Chapter 3: Storage and Retrieval"]
confidence: high
---


> From chapter: *Chapter 3: Storage and Retrieval*

## Core Principle

Chapter 3 explains how databases physically store and retrieve data by examining two engine families — log-structured (LSM-trees, SSTables, Bitcask) and page-oriented (B-trees) — and the indexing structures that make reads efficient at the cost of write overhead. It establishes the fundamental index trade-off (every index speeds reads but slows writes), the log-structured principle of append-only immutable segments with background compaction, and the critical OLTP vs. OLAP distinction that determines whether row-oriented or column-oriented storage is appropriate. The chapter equips developers to choose and tune storage engines by understanding what happens under the hood rather than treating the database as a black box.

## Key Heuristics

These are the load-bearing rules for this concept.

> well-chosen indexes speed up read queries, but every index slows down writes

> databases don't usually index everything by default, but require you to choose indexes manually, using your knowledge of the application's typical query patterns

> appending to a file is generally very efficient — for writes, it's hard to beat the performance of simply appending to a file, because that's the simplest possible write operation

> An index is an additional structure that is derived from the primary data — this doesn't affect the contents of the database, it only affects the performance of queries

> LSM-trees are typically faster for writes, whereas B-trees are thought to be faster for reads

> the cost of a lookup is O(n): if you double the number of records n in your database, a lookup takes twice as long

> Bitcask is well suited in situations where the value for each key is updated frequently and there are not too many distinct keys

## Anti-Patterns & Fixes

- Full-Scan Lookup: using a linear scan (O(n)) for every key lookup as dataset grows. Fix: add an index structure (hash map, B-tree, or SSTable) to reduce lookup cost to O(1) or O(log n).
- Unbounded Log Growth: appending updates forever without compaction causes disk exhaustion. Fix: segment the log at a fixed size and run background compaction to discard obsolete keys, then merge segments.
- Indexing Everything By Default: adding indexes on all columns increases write overhead for every insert/update. Fix: selectively index only fields matching the application's actual query patterns.
- Using Hash Index for Range Queries: hash indexes cannot efficiently answer range queries (e.g., all keys between X and Y). Fix: use a sorted index structure (B-tree or SSTable/LSM-tree) when range scans are required.
- Row-Oriented Storage for Analytic Workloads: reading entire rows when only a few columns are needed wastes I/O on OLAP queries. Fix: use column-oriented storage so only the relevant columns are read from disk.
- Ignoring Write-Ahead Log (WAL) in B-Trees: writing directly to B-tree pages without a WAL leaves the database unrecoverable after a crash mid-write. Fix: always append changes to a WAL before applying them to the tree pages.

## When To Apply

Load this page when:

- Use this when selecting or recommending a database storage engine for a new service and needing to match engine characteristics to workload access patterns.
- Use this when a key-value store with high write throughput and a bounded key space is needed and all keys can fit in memory (suggesting Bitcask/hash-index architecture).
- Use this when designing a system that must support range queries, indicating a sorted index (B-tree or LSM/SSTable) is required instead of a hash index.
- Use this when a write-heavy workload is causing index maintenance to become a bottleneck, triggering evaluation of log-structured (LSM-tree) storage over B-trees.
- Use this when building or configuring an analytics pipeline that scans large datasets and needs to minimize I/O by reading only relevant columns.
- Use this when a storage system is running out of disk space due to append-only logs, requiring implementation of log segmentation and compaction.
- Use this when evaluating whether to add a secondary index to a table, requiring explicit trade-off analysis between read speedup and write overhead.
- Use this when a system needs crash recovery guarantees on a B-tree storage engine, indicating a write-ahead log must be present.

## Concrete Examples

- Two-function Bash key-value store (db_set/db_get): db_set appends to a file; db_get greps the file — illustrates O(n) read cost and the value of append-only writes.
- Bitcask storage engine: in-memory hash map of keys to byte offsets in an append-only log file, used as the default engine in Riak.
- Cat video play-count workload: URL as key, play count as value updated frequently — used to illustrate the ideal Bitcask use case of high writes per key with bounded key space.
- Log compaction and segment merging diagram: duplicate keys (mew, purr, yawn) across two segments are compacted into a single merged segment retaining only the latest value per key.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 3: Storage and Retrieval**

An LLM coding agent generating data access code will default to the simplest retrieval pattern (linear scan or ORM fetch-all) without considering index design, replicating the O(n) db_get anti-pattern at scale. Agents are also prone to generating schemas that index every column 'to be safe,' incurring unnecessary write overhead — this chapter provides the explicit trade-off rule (reads vs. writes) the agent needs to make a justified, minimal indexing decision. Additionally, when an agent scaffolds a storage layer it may conflate OLTP and OLAP access patterns, producing row-oriented schemas for analytic workloads; the OLTP/OLAP distinction gives the agent a named decision gate to apply before emitting any storage schema.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->