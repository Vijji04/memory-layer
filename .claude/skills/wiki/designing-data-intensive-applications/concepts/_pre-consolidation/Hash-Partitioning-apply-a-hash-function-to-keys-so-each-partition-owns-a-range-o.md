---
title: Hash Partitioning: apply a hash function to keys so each partition owns a range of hashes, distributing load evenly at the cost of range query efficiency
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-6-Partitioning.json]
contributing_chapters: ["Chapter 6: Partitioning"]
confidence: high
---

# Hash Partitioning: apply a hash function to keys so each partition owns a range of hashes, distributing load evenly at the cost of range query efficiency

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
