---
title: Multi-Leader Replication: Multiple nodes accept writes independently, requiring conflict detection and resolution strategies for concurrent writes to the same record
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-5-Replication.json]
contributing_chapters: ["Chapter 5: Replication"]
confidence: high
---

# Multi-Leader Replication: Multiple nodes accept writes independently, requiring conflict detection and resolution strategies for concurrent writes to the same record

> From chapter: *Chapter 5: Replication*

## Core Principle

Replication keeps copies of data on multiple nodes for latency, availability, and read scalability, but all complexity arises from propagating changes consistently. The chapter contrasts single-leader, multi-leader, and leaderless topologies, each with distinct trade-offs around durability (sync vs. async), consistency guarantees (read-your-writes, monotonic reads, eventual consistency), and conflict resolution (LWW, CRDTs, version vectors). Choosing a replication strategy requires explicitly reasoning about failure modes—leader failover, replication lag, split-brain, and write conflicts—rather than assuming the database handles them transparently.

## Key Heuristics

These are the load-bearing rules for this concept.

> All of the difficulty in replication lies in handling changes to replicated data.

> It is impractical for all followers to be synchronous: any one node outage would cause the whole system to grind to a halt.

> Weakening durability may sound like a bad trade-off, but asynchronous replication is almost inevitable if there are many followers, or if they are geographically distributed.

> If the leader fails and is not recoverable, any writes that have not yet been replicated to followers are lost — a write is not guaranteed to be durable, even if it has been confirmed to the client.

> Eventual consistency is not a single guarantee but a family of weaker guarantees; be precise about which one you actually need (read-your-writes, monotonic reads, etc.).

> The snapshot used to bootstrap a new follower must be associated with an exact position in the leader's replication log — otherwise catch-up is impossible.

## Anti-Patterns & Fixes

- Assuming All-Synchronous Replication Is Safe: Making every follower synchronous means one slow/crashed node blocks all writes system-wide. Fix: Use semi-synchronous (one synchronous follower, rest asynchronous) to guarantee durability on two nodes without full write-blocking.
- Naive File Copy for Follower Bootstrap: Copying data files while the database is live produces an inconsistent snapshot because different parts are captured at different points in time. Fix: Take a consistent snapshot (e.g., via innobackupex for MySQL) tied to a specific replication log position, then replay changes from that position.
- Ignoring Replication Lag in Read Paths: Routing reads to any replica without considering lag can surface stale data, violating user expectations (e.g., user edits a record, immediately re-reads it from a lagging replica and sees old data). Fix: Route reads of recently-written data to the leader, or use read-your-writes / monotonic-reads session guarantees.
- Unbounded Replication Loop in Multi-Leader Setups: A write originating on node A propagates to node B, which re-propagates it back to A, causing infinite replication cycles. Fix: Tag each write with the originating node ID and discard writes that have already been processed by the local node.
- Last-Write-Wins Without Causal Tracking: Using wall-clock timestamps to resolve concurrent writes silently discards data because clocks are unsynchronized across nodes. Fix: Use version vectors or CRDTs to track causality and detect true concurrency before resolving conflicts.
- Treating Eventual Consistency as a Vague Promise: Developers assume 'eventually consistent' means 'probably fine soon' without specifying which guarantees hold. Fix: Explicitly select and enforce a named consistency level (read-your-writes, monotonic reads, consistent prefix reads) appropriate to the application's requirements.

## When To Apply

Load this page when:

- Use this when designing a service that must remain writable during replica failures and you need to choose between synchronous, semi-synchronous, or asynchronous replication modes.
- Use this when bootstrapping a new database replica and you need to avoid downtime or inconsistent state during the initial data copy.
- Use this when a user reports seeing stale data immediately after a write, indicating a replication lag violation of read-your-writes consistency.
- Use this when implementing multi-region writes and you need to decide whether to use multi-leader replication and how to handle write conflicts.
- Use this when selecting a quorum configuration (w, r, n) for a leaderless store to balance between read/write availability and consistency guarantees.
- Use this when a distributed system exhibits split-brain behavior after a leader failover and you need to prevent two nodes from both acting as leader (fencing).
- Use this when an application uses concurrent writes to shared records (e.g., a shopping cart or collaborative document) and you need a conflict resolution strategy.

## Concrete Examples

- User 1234 updates their profile picture: the write goes to the leader, replicates synchronously to Follower 1 (leader waits for ack before confirming to client) and asynchronously to Follower 2 (leader sends but does not wait), illustrating semi-synchronous replication.
- Setting up a new MySQL follower using innobackupex to take a consistent snapshot tied to binlog coordinates, then replaying the change backlog until the follower catches up to the leader.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 5: Replication**

An LLM coding agent generating data-layer code will frequently default to single-node database patterns—issuing writes and immediately issuing reads to any replica—without encoding replication-lag guards, making read-your-writes violations invisible until production. Agents are also prone to generating multi-leader or leaderless configurations without conflict-resolution logic, since the 'happy path' code compiles and passes unit tests even when concurrent-write semantics are broken. Applying this chapter's frameworks forces the agent to explicitly choose a replication topology, wire in the correct consistency guarantees at the session layer, and instrument conflict detection before the code is considered complete.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
