---
title: Circuit Breaker
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
confidence: high
consolidated_from: 2 pages
---

# Circuit Breaker

> Consolidated from 2 related concept pages.

---

## Circuit Breaker A stability pattern that trips open to stop cascading failures w

## Core Principle

This appendix and its accompanying index catalog the full set of stability antipatterns (Blocked Threads, Cascading Failures, Chain Reactions, SLA Inversion, Unbounded Result Sets), stability patterns (Circuit Breaker, Bulkheads, Timeouts, Steady State), capacity antipatterns, and transparency frameworks that constitute the book's core reference architecture. The bibliography points to foundational texts in XP, refactoring, design patterns, Theory of Constraints, and lean development that underpin the engineering philosophy throughout. Together they form a navigable knowledge base for building systems that survive production conditions.

## Key Heuristics

These are the load-bearing rules for this concept.

> Cynical software expects bad things to happen and is designed to survive them

> The chain of failure: tight coupling allows failures to cascade across system boundaries

> Zero, one, many — design for the general case from the start

> Shared nothing architecture prevents Chain Reactions by eliminating hidden linkages

> Every integration point is a potential failure point

> A system's SLA cannot exceed the SLA of its dependencies

> Design for transparency: if you can't see it, you can't fix it

## Anti-Patterns & Fixes

- Blocked Threads: Thread pools exhaust when calls block indefinitely on slow or failed integrations, halting the entire application. Fix: Always use Timeouts on every integration point and third-party library call.
- Cascading Failures: A failure in one layer propagates upward through tightly coupled layers until the entire system is down. Fix: Use Circuit Breakers and Bulkheads to isolate failure domains.
- Chain Reactions: Horizontal scaling farms fail node-by-node as load redistributes onto survivors, eventually killing all nodes. Fix: Use Bulkheads to partition load and Circuit Breakers to shed load before nodes collapse.
- AJAX Overkill: Overuse of AJAX causes session thrashing, poor request timing, and bloated responses that degrade performance. Fix: Apply interaction design discipline; use AJAX only where it genuinely improves UX.
- Database Eutrophication: Unbounded data growth causes table scans, index bloat, and query slowdowns over time. Fix: Implement data purging and archival strategies from the start.
- SLA Inversion: A system promises a high SLA but depends on lower-SLA services, making the promise impossible to keep. Fix: Document all dependency SLAs and set your own SLA at or below the weakest dependency.

## When To Apply

Load this page when:

- Use this when designing a service that calls external APIs or databases and needs to handle downstream unavailability without hanging caller threads
- Use this when a system uses a horizontal server farm and a single-node failure could redistribute enough load to trigger a cascade of node failures
- Use this when setting connection pool sizes, timeout values, or thread pool configurations for any integration point
- Use this when a system's advertised uptime SLA needs to be validated against the SLAs of all its dependencies
- Use this when log files, in-memory caches, or database tables can grow without bound and degrade the system over time
- Use this when designing observability for a production system and deciding what metrics, logs, and dashboards to instrument
- Use this when a load test reveals that throughput degrades under concurrency and the bottleneck must be located and addressed

## Concrete Examples

- Core Facilities airline case study: a database failover outage caused by a cascading failure traced through thread dumps to a SQLException that blocked all worker threads
- Retail online store capacity case study: load testing revealed that poorly performing SQL and session mismanagement caused throughput collapse under realistic concurrent user loads
- Eight-way cluster Chain Reaction: a bug with timing caused one node to fail, redistributing load to seven nodes, each of which then failed in sequence
- Online store case study using SiteScope monitoring revealed thread dump evidence of blocked threads during production incident

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Appendix A: Bibliography**

An LLM coding agent is especially prone to generating integration code without timeouts, missing Circuit Breaker wrappers around third-party calls, and producing unbounded database queries — all of which are invisible during unit test generation but cause production failures under load or partial outages. The agent must treat every generated external call site as a mandatory timeout/Circuit Breaker injection point, since it cannot rely on a human reviewer noticing the omission during code review. Transparency instrumentation (logging, metrics emission) is also routinely omitted by agents generating feature code, which must instead be treated as a non-optional cross-cutting concern in every generated service method.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Circuit Breaker Pattern Wrap dangerous remote calls in a stateful component that

## Core Principle

Chapter 5 presents eight stability patterns — including Timeouts, Circuit Breaker, Test Harness, and Decoupling Middleware — as the constructive counterparts to the antipatterns in Chapter 4, each designed to isolate failures and prevent them from propagating through a system. The core philosophy is recovery-oriented design: assume failures will occur, bound all waiting, decouple systems in time and space, and return a response quickly rather than holding callers hostage to downstream problems. Pattern count is not a quality metric; wise, targeted application of these patterns is what separates software that survives production from software that passes QA.

## Key Heuristics

These are the load-bearing rules for this concept.

> Hope is not a design method.

> Expect failures. Apply these patterns wisely to reduce the damage done by an individual failure.

> Well-placed timeouts provide fault isolation; a problem in some other system, subsystem, or device does not have to become your problem.

> It is essential that any resource pool that blocks threads must have a timeout to ensure threads are eventually unblocked whether resources become available or not.

> Immediate retries are liable to hit the same problem and result in another timeout. That just makes the user wait even longer for his error message.

> Tightly coupled middleware amplifies shocks to the system. Synchronous calls are particularly vicious amplifiers that facilitate cascading failures.

> Done well, middleware simultaneously integrates and decouples systems.

> Decoupling Middleware is an architecture decision. It ripples into every part of the system. This is one of those nearly irreversible decisions that should be made early rather than late.

## Anti-Patterns & Fixes

- Infinite Wait on Network Calls: Code blocks indefinitely waiting for a response from a remote system that may never reply, causing thread exhaustion. Fix: Always set explicit timeouts on all outbound network calls and resource pool checkouts.
- Immediate Retry After Timeout: Retrying a failed operation instantly compounds user wait time and likely hits the same underlying failure. Fix: Queue the operation for delayed retry and return a response (success, failure, or queued-acknowledgment) immediately.
- Hiding Sockets in Vendor Libraries: Client libraries that wrap socket communication prevent the application from setting timeouts on the underlying socket. Fix: Use or build a Gateway/template class (e.g., Spring JdbcTemplate) that exposes timeout configuration and centralizes error handling.
- No-Argument wait() / poll() / offer(): Using blocking concurrency primitives without a timeout argument risks permanent thread blocking. Fix: Always use the overload that accepts a timeout argument for Object.wait(), poll(), offer(), and tryLock().
- Synchronous RPC as Default Integration: Using request/reply RPC couples systems in time, so one system's slowness or failure cascades directly to the caller. Fix: Prefer message-oriented middleware to decouple systems in both space and time where the business process permits.
- Repeating Timeout-Handling Logic Inline: Coding timeout and error handling for DB connections in dozens of call sites leads to inconsistency and omissions. Fix: Encapsulate the interaction pattern in a QueryObject and a Gateway template class so timeout logic is written once and reused.

## When To Apply

Load this page when:

- Use this when writing any code that makes an outbound network call, HTTP request, database query, or RPC to an external system — add an explicit timeout.
- Use this when checking out resources from any connection pool or thread pool — ensure the checkout call has a bounded timeout.
- Use this when a remote dependency has been returning errors or timeouts repeatedly — wrap the call in a Circuit Breaker to stop hammering the failing system.
- Use this when a failed operation needs to be retried — queue the work for delayed retry rather than retrying inline and making the caller wait longer.
- Use this when designing integration between two services and choosing a communication protocol — evaluate whether asynchronous message-passing can replace synchronous RPC to avoid cascading failures.
- Use this when writing Java concurrency code using Object.wait(), BlockingQueue.poll(), or Lock.tryLock() — always supply a timeout argument.
- Use this when testing resilience of a service client — build or use a Test Harness that simulates slow responses, dropped connections, and malformed payloads rather than only testing the happy path.
- Use this when making an early architecture decision about inter-system communication — choose middleware style before detailed design, because switching later is extremely costly.

## Concrete Examples

- Porting the BSD sockets library to a mainframe UNIX environment, where the networking code was 'riddled with error handling for different flavors of timeouts', illustrating the pervasiveness of timeout concerns at low levels.
- Database interaction sequence (checkout connection, run query, map ResultSet, return connection) with at least three points that can hang indefinitely — solved by using a QueryObject plus a Gateway template like Spring's JdbcTemplate.
- Credit card authorization via RPC vs. async message: RPC lets the app decide immediately whether to proceed or show an error page; async messaging requires designing for late/missing responses, exception queues, and callbacks.
- Email store-and-forward as the canonical example of queue-and-retry: requiring every mail server to be online simultaneously would make email fragile; delayed retry makes the overall system robust to partial failures.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 5: Stability Patterns**

An LLM coding agent generating integration code will almost always omit timeouts, retry logic, and circuit breakers because training examples rarely include them and the agent optimizes for the happy path that passes functional tests. This is especially dangerous because an agent may generate dozens of call sites each missing timeouts, making the omission systemic rather than accidental — the fix is to enforce a code-generation rule that every outbound call, resource pool checkout, and concurrency primitive must include an explicit timeout argument, and that retries must use a queue-and-delay pattern rather than an immediate loop. Agents should also default to suggesting asynchronous messaging over synchronous RPC when generating inter-service integration scaffolding, since they have no intuition for cascading failure modes that only appear under production load.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
