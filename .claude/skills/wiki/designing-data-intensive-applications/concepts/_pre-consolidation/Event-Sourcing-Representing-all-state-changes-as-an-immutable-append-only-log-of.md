---
title: Event Sourcing: Representing all state changes as an immutable, append-only log of events, from which current state can be derived by replaying
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-11-Stream-Processing.json]
contributing_chapters: ["Chapter 11: Stream Processing"]
confidence: high
---

# Event Sourcing: Representing all state changes as an immutable, append-only log of events, from which current state can be derived by replaying

> From chapter: *Chapter 11: Stream Processing*

## Core Principle

Stream processing is the unbounded, continuously-processed complement to batch processing: instead of fixed input files, events arrive incrementally and must be handled with low latency via messaging systems that decouple producers from consumers. Key design decisions involve durability (message broker vs. direct messaging), flow control (backpressure vs. drop vs. queue), and delivery guarantees (at-most-once, at-least-once, exactly-once), each with explicit trade-offs in latency, throughput, and correctness. The chapter establishes that streaming systems must explicitly handle what batch systems get for free—fault tolerance, ordering, and completeness—since the input is never 'done'.

## Key Heuristics

These are the load-bearing rules for this concept.

> A complex system that works is invariably found to have evolved from a simple system that works.

> The more often you poll, the lower the percentage of requests that return new events, and thus the higher the overheads become.

> It is better for consumers to be notified when new events appear [than to poll].

> Whether message loss is acceptable depends very much on the application.

> If a large number of messages is dropped, it may not be immediately apparent that the metrics are incorrect.

> Failed tasks are automatically retried, and partial output from failed tasks is automatically discarded — the output is the same as if no failures had occurred.

## Anti-Patterns & Fixes

- Polling a Non-Purpose-Built Datastore: Using a general database as an event bus and polling it for new events causes high overhead and low freshness. Fix: Use a messaging system or message broker with push-based consumer notification.
- Direct Producer-Consumer Coupling Without a Broker: Direct HTTP/RPC or brokerless messaging assumes both sides are always online; offline consumers silently miss messages. Fix: Route messages through a durable message broker that buffers and replays.
- Unbounded Queue Growth Without Backpressure: Buffering messages in memory without a size limit causes crashes when queues exceed available RAM. Fix: Apply backpressure to block producers, or write overflow to disk with understood performance trade-offs.
- Using UDP/Unreliable Transport for Exact-Count Metrics: StatsD-style UDP drops packets silently, making counters approximate and errors non-obvious. Fix: Use reliable delivery (TCP-backed broker) when exact counts are required; reserve UDP for approximate/lossy metrics where occasional loss is acceptable.
- Ignoring Producer Crash During Retry Buffer: Direct-messaging protocols that store the retry buffer only in producer memory lose messages if the producer crashes. Fix: Persist the outbound message buffer durably or delegate durability to a broker.

## When To Apply

Load this page when:

- Use this when building a pipeline that must process events with latency lower than a full batch cycle (e.g. sub-second or sub-minute freshness requirements).
- Use this when designing a system where multiple independent consumers must each receive every event from a single producer.
- Use this when choosing between polling a database for new rows versus receiving push notifications from a message broker.
- Use this when a consumer service may go offline intermittently and must not lose events that arrived during downtime.
- Use this when producers can burst faster than consumers can process, requiring a decision between dropping, queuing, or backpressure.
- Use this when implementing metrics collection and deciding whether approximate (UDP) or exact (reliable delivery) counting semantics are required.
- Use this when designing fault-tolerant stream processing where failed tasks must be retried without producing duplicate or missing output.
- Use this when integrating a change-data-capture feed from a database into a downstream stream processing topology.

## Concrete Examples

- Web server log processing: each line of an access log treated as an event, analogous to a batch input record.
- StatsD/Brubeck using unreliable UDP to collect machine metrics, where counter correctness depends on zero packet loss.
- UDP multicast for stock market feeds in the financial industry, where low latency outweighs reliability and the application layer handles retransmission.
- Webhooks pattern: a callback URL registered with a service that POSTs an HTTP request to that URL whenever an event occurs.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 11: Stream Processing**

An LLM coding agent generating stream-processing code will default to polling loops (the simplest pattern to emit) rather than broker-push architectures, silently introducing the polling anti-pattern at scale. Agents are also prone to omitting backpressure logic entirely—generating unbounded in-memory queues—because correctness under slow consumers only manifests at runtime load, not in unit tests the agent might reason about. Explicitly invoking this chapter's frameworks forces the agent to choose a durability and flow-control strategy up front rather than deferring it as an implicit design gap.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
