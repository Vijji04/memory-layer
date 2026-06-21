---
title: HPC vs Cloud Fault Philosophy: Supercomputers escalate partial failure to total failure (crash everything, restart from checkpoint); internet services must tolerate partial failure in-place and keep serving users
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-8-The-Trouble-with-Distributed-Systems.json]
contributing_chapters: ["Chapter 8: The Trouble with Distributed Systems"]
confidence: high
---

# HPC vs Cloud Fault Philosophy: Supercomputers escalate partial failure to total failure (crash everything, restart from checkpoint); internet services must tolerate partial failure in-place and keep serving users

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
