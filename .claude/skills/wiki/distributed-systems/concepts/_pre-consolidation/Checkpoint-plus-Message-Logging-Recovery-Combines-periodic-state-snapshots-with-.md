---
title: Checkpoint-plus-Message-Logging Recovery: Combines periodic state snapshots with communication logs to enable replay-based recovery after crashes
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, distributed-systems, concept]
sources: [extracts/distributed-systems/Fault-tolerance.json]
contributing_chapters: ["Fault tolerance"]
confidence: high
---

# Checkpoint-plus-Message-Logging Recovery: Combines periodic state snapshots with communication logs to enable replay-based recovery after crashes

> From chapter: *Fault tolerance*

## Core Principle

Fault tolerance in distributed systems centers on surviving partial failures — where some components fail while others continue operating — through four dependability properties (availability, reliability, safety, maintainability) and the foundational technique of redundancy. Process groups with consensus algorithms (Paxos), atomic multicast, distributed commit protocols (2PC/3PC), and checkpoint-plus-log recovery are the primary mechanisms, each with precise resource requirements and well-defined failure-mode trade-offs. The chapter provides a unified taxonomy of failure types from crash through Byzantine, enabling systematic selection of the appropriate tolerance mechanism for each class.

## Key Heuristics

These are the load-bearing rules for this concept.

> Redundancy is the key technique needed to achieve fault tolerance.

> By using 2k + 1 servers, Paxos can establish k-fault tolerance. However, we need a total of 3k + 1 servers if it is needed to deal with arbitrary failures.

> A highly available system is one that will most likely be working at a given instant in time; a highly reliable system is one that will most likely continue to work without interruption during a relatively long period of time. The two are not the same.

> A message [in atomic multicast] is delivered to all nonfaulty processes in a group, or to none at all.

> The key issue in achieving scalability [of reliable multicasting] is to reduce the number of feedback messages by which receivers report the (un)successful receipt of a multicasted message.

> Taking a checkpoint is an expensive operation. To improve performance, many distributed systems combine checkpointing with message logging.

> The most difficult failures to handle are those by which a process exhibits any kind of failure, called arbitrary or Byzantine failures.

## Anti-Patterns & Fixes

- Conflating Availability with Reliability: Treating high availability (working at a given instant) as equivalent to high reliability (working continuously over time). A system down 1ms/hour is 99.9999% available but unreliable. Fix: define and test both metrics independently; use MTBF-based reliability targets alongside uptime SLAs.
- Single-Coordinator Commit (2PC without 3PC): In two-phase commit, a coordinator crash blocks all participants indefinitely waiting for resolution. Fix: use three-phase commit protocol to allow participants to proceed without the coordinator, or use a consensus algorithm like Paxos.
- Under-Replicating for Byzantine Faults: Using 2k+1 replicas which only tolerates crash failures, not arbitrary/Byzantine failures. Fix: provision 3k+1 replicas when Byzantine fault tolerance is required.
- Scalability-Blind Reliable Multicast: Implementing naive ACK-based reliable multicast that generates O(n) feedback messages per transmission, causing feedback implosion in large groups. Fix: use negative acknowledgment (NACK) schemes or hierarchical feedback suppression to reduce message overhead.
- Checkpoint-Only Recovery Without Log: Relying solely on periodic checkpoints forces full re-execution from the last checkpoint on failure, losing all intermediate work. Fix: combine checkpointing with message logging so intermediate steps can be replayed without redoing the entire interval.
- Ignoring Partial Failure: Designing distributed components as if failures are total (all-or-nothing), missing partial failure scenarios where some nodes operate correctly while others fail silently. Fix: explicitly model and test partial failure modes; use process groups and atomic multicast to maintain consistent state.

## When To Apply

Load this page when:

- Use this when designing a distributed service that must continue operating while one or more backend nodes fail, to choose the correct replication factor (2k+1 vs 3k+1).
- Use this when implementing a multi-node transaction coordinator and needing to decide between two-phase and three-phase commit to avoid blocking on coordinator crash.
- Use this when building a message-delivery subsystem that must guarantee all-or-nothing delivery to a process group, signaling the need for atomic multicast.
- Use this when a distributed system's SLA specifies both uptime percentage and continuous-operation duration, requiring separate availability and reliability metrics.
- Use this when adding fault recovery to a stateful distributed service, to decide whether to implement checkpointing alone or combine it with message logging for replay.
- Use this when a process group experiences membership changes (node joins/leaves) and consistent agreement on the new member list is required.
- Use this when a large-scale multicast system shows performance degradation under load due to ACK storms, triggering application of feedback-suppression or NACK-based reliability.
- Use this when classifying an observed failure mode (crash vs. omission vs. timing vs. Byzantine) to select the appropriate fault-tolerance mechanism.

## Concrete Examples

- A system that crashes for one random millisecond per hour has >99.9999% availability but is still unreliable — illustrating the availability/reliability distinction.
- A system shut down for two specific weeks every August has high reliability but only 96% availability — further illustrating the distinction.
- Nuclear power plant and space-vehicle control systems cited as examples requiring high safety, where even brief failures could be catastrophic.
- Two-phase commit: coordinator polls all processes for commit agreement in round one, then multicasts the outcome in round two — used for group membership changes.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Fault tolerance**

An LLM coding agent is itself a stateless, single-shot process and may generate distributed-system code that implicitly assumes a single reliable coordinator or ignores partial failure, because it has no runtime experience of nodes silently disappearing. This chapter's failure taxonomy and replication formulas give the agent concrete, parameterized rules (e.g., '3k+1 for Byzantine tolerance') it can apply mechanically when scaffolding fault-tolerant services, preventing the common agent error of under-replicating or omitting commit-protocol coordinator-crash handling. Additionally, agents generating recovery logic often default to full-state snapshots; the checkpoint-plus-log pattern provides an explicit alternative the agent can select when performance constraints are specified.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
