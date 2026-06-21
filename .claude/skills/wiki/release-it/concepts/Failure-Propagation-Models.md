---
title: Failure Propagation Models
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
confidence: high
consolidated_from: 3 pages
---

# Failure Propagation Models

> Consolidated from 3 related concept pages.

---

## Common Dependency Hypothesis A diagnostic model where simultaneous failures acro

## Core Principle

A single uncaught SQLException in a JDBC finally block — where stmt.close() threw during a post-failover socket error, preventing conn.close() from executing — leaked connections until the entire pool was exhausted, hanging all dependent systems and grounding an airline for three hours with cascading multi-million dollar consequences. The core lesson is that resource cleanup methods must each be independently exception-handled per their API specification, and that bugs must be contained through architectural isolation patterns rather than relying on perfect code. Resilience engineering must assume bugs will escape to production and design systems so that one component's failure cannot propagate to all dependents.

## Key Heuristics

These are the load-bearing rules for this concept.

> Bugs will happen. They cannot be eliminated, so they must be survived instead.

> Restoring service takes precedence over investigation.

> The worst problem here is that the bug in one system could propagate to all the other affected systems.

> Once you know where to look, it's simple to make a test that finds it.

> When the fur flies, improvisation is not your friend.

> How do we prevent bugs in one system from affecting everything else?

> The entire globe-spanning, multibillion dollar airline... was grounded by one programmer's rookie error: a single uncaught SQLException.

## Anti-Patterns & Fixes

- Swallowed Cleanup Exception: In a try/finally block, calling stmt.close() without a nested try/catch means that if close() throws a SQLException, conn.close() is never called, leaking the connection back to the pool. Fix: Wrap each close() call in its own try/catch block so a failure in one cleanup step does not skip subsequent cleanup steps.
- Stale Connection Pool After Failover: JDBC connections created before a database failover retain the old IP/TCP state and will fail on statement execution or close, but the pool does not know they are dead. Fix: Implement connection validation on checkout (e.g., test-on-borrow) and handle SQLExceptions during close() to invalidate and evict stale connections from the pool.
- Shallow Health Monitoring: Monitoring only a static status/health-check URL that does not exercise real application paths gives a false green signal even when all worker threads are blocked. Fix: Health checks must exercise the actual critical code paths (e.g., a real lightweight DB query) to reflect true application health.
- Assuming close() Cannot Fail: Treating resource-release methods as infallible because they 'almost never' throw is a latent reliability bug. Fix: Always handle exceptions from close() methods per the API specification, regardless of how rarely they occur in practice.
- No Fault Isolation Between Dependent Systems: Allowing one downstream service's resource exhaustion to block all threads in every calling system, causing a full cascade. Fix: Use design patterns (circuit breakers, bulkheads, timeouts) to prevent a bug in one system from exhausting resources in callers.

## When To Apply

Load this page when:

- Use this when writing JDBC or any resource-pool access code where cleanup (close/release) must happen in a finally block — ensure each close() call is independently exception-handled.
- Use this when a database failover, network partition, or infrastructure change precedes an application outage — treat all pooled connections as potentially stale and validate before use.
- Use this when diagnosing simultaneous failures across multiple unrelated services — immediately identify and inspect the common upstream dependency.
- Use this when designing health check endpoints — ensure they exercise real transactional paths, not just static pages, to accurately reflect system health.
- Use this when a connection pool or thread pool is exhausted — trace back to whether resource release (close/return) is being skipped due to an unhandled exception in the cleanup path.
- Use this when an application under load shows all threads blocked at resource checkout — suspect a connection leak caused by an exception swallowing a close() call.
- Use this when planning operational runbooks for on-call incidents — pre-script data collection (thread dumps, snapshots) so post-mortem evidence is captured without extending downtime.

## Concrete Examples

- An airline's Core Facilities (CF) service had a FlightSearch EJB whose lookupByCity() method called stmt.close() in a finally block without catching SQLException; after a database failover, close() threw an exception, conn.close() was skipped, and after 40 such calls the entire JDBC connection pool was exhausted, blocking all EJB threads on every CF app server.
- A planned Veritas Cluster Server database failover at 11 p.m. PT invalidated all pre-existing TCP connections in the CF JDBC pool, causing a two-hour delayed failure at 2:30 a.m. PT when the stale connections were finally exercised under load.
- Monitoring only hit a CF HTTP status page, which stayed green even while all EJB worker threads were blocked — demonstrating that shallow health checks provide false confidence during real outages.
- The incident cascaded from CF to check-in kiosks and IVR systems simultaneously, causing 3+ hours of outage, delayed flights nationwide, FAA report card impact, and CEO-level financial consequences — all from a single missing try/catch around stmt.close().

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 2: Case Study: The Exception That Grounded An Airline**

An LLM coding agent is highly likely to reproduce the exact anti-pattern described here: it will generate try/finally resource cleanup blocks that look correct and match common tutorial patterns, but omit per-statement exception handling on close() calls because training data is full of the flawed idiom. Unlike a human reviewer who might recall an obscure driver behavior, an agent will confidently produce the broken pattern unless explicitly prompted to handle exceptions from every cleanup call. Additionally, an agent generating health check endpoints will naturally produce the shallowest possible implementation (returning HTTP 200) rather than one that exercises real downstream dependencies, creating false observability that masks exactly this class of failure.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Impulse vs Stress Framework Impulses are rapid shocks flash traffic bulk queue d

## Core Principle

Chapter 3 establishes that production stability requires designing systems to expect and contain failures rather than prevent them, using the crack propagation metaphor to explain how small failures amplify through tightly coupled architectures. Stability is defined by resilience under impulses and stresses and longevity over deployment cycles, with the key insight that stable designs cost no more than unstable ones but require deliberate failure mode engineering. The chapter introduces a map of stability antipatterns and countermeasure patterns—including timeouts, circuit breakers, and bulkheads—as the systematic toolkit for stopping cracks from propagating into full system outages.

## Key Heuristics

These are the load-bearing rules for this concept.

> Enterprise software must be cynical. Cynical software expects bad things to happen and is never surprised when they do.

> A highly stable design usually costs the same to implement as an unstable one.

> Denying the inevitability of failures robs you of your power to control and contain them.

> If you do not design your failure modes, then you will get whatever unpredictable—and usually dangerous—ones happen to emerge.

> Run longevity tests. It's the only way to catch longevity bugs.

> The major dangers to your system's longevity are memory leaks and data growth.

> Tight coupling accelerates cracks.

> The less coupled architectures act as shock absorbers, diminishing the effects of this error instead of amplifying them.

## Anti-Patterns & Fixes

- Unbounded Thread Blocking: Connection pools configured to block requesting threads indefinitely when exhausted cause all request-handling threads to pile up, taking down the entire application. Fix: Configure pools with bounded wait timeouts or the ability to create additional connections under load.
- Missing RMI/Remote Call Timeouts: RMI (and similar remote calls) never time out by default, so callers block forever waiting on a failed downstream service. Fix: Always set explicit socket and call timeouts on all remote/external calls.
- Tight Coupling Between Services: Exposing shared services via synchronous RPC (e.g., EJBs) means a resource exhaustion in one service directly causes cascading failures in all callers. Fix: Use request/reply message queues, decoupling middleware, or tuplespace architectures to reduce coupling and act as shock absorbers.
- No Longevity Testing: Applications are restarted so frequently in dev/QA that memory leaks and data growth bugs are never surfaced before production. Fix: Run dedicated longevity tests with continuous low-level load for days or weeks on a reserved machine.
- Optimistic Architecture (No Failure Mode Design): Teams focus on happy-path functionality and neglect designing explicit failure modes, resulting in unpredictable and dangerous emergent failures. Fix: Explicitly ask 'what are all the ways this can go wrong?' for every external call, I/O, resource use, and expected outcome, then design crackstoppers at each layer.
- Ignoring Coupled Event Probability: Treating failure chain events as independent (like coin tosses) leads to underestimating combined failure probability. Fix: Recognize that failure in one layer increases probability of adjacent-layer failures; design for correlated failure scenarios.

## When To Apply

Load this page when:

- Use this when writing code that calls an external service, database, or API—always apply explicit timeouts and handle the case where no response ever arrives.
- Use this when designing a shared service used by multiple callers—partition into service groups or use async messaging to prevent one failure from cascading to all consumers.
- Use this when configuring a connection pool or thread pool—ensure the pool has bounded blocking behavior and does not allow indefinite thread exhaustion.
- Use this when a system must handle sudden traffic spikes (flash crowds, bulk queue dumps)—design impulse-resistant entry points with rate limiting or queue-backed ingestion.
- Use this when a downstream dependency is slow or degraded—detect stress propagation (rising RAM, I/O, latency) and apply backpressure or circuit-breaking before strain reaches other layers.
- Use this when setting up a test environment—include longevity tests under continuous low load to surface memory leaks and data growth bugs that short-running tests miss.
- Use this when reviewing architecture for a new integration—explicitly map failure modes and identify where crackstoppers (timeouts, bulkheads, circuit breakers) should be inserted.
- Use this when a system handles mixed transaction workloads—ensure failure in one transaction type cannot exhaust shared resources and degrade unrelated transaction types.

## Concrete Examples

- Airline Core Facilities (CF) project: An unhandled SQLException caused connection pool exhaustion, which blocked all request-handling threads via RMI calls with no timeouts, cascading into a full airline system outage affecting flight operations.
- Flash mob hitting Xbox 360 product page: 10,000 new sessions arriving within one minute as an example of an impulse that can fracture a system instantly.
- Slow credit card processor: A downstream dependency with insufficient capacity creating sustained stress that propagates strain (higher RAM usage, excess I/O) to unrelated parts of the system.
- Longevity bug scenario: A memory leak that only manifests after seven days of uptime, never caught in dev/QA environments where servers are recycled multiple times daily.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 3: Introducing Stability**

An LLM coding agent is especially prone to generating code that omits timeouts, uses default blocking configurations, and lacks explicit failure mode handling—because training data skews toward happy-path examples and the agent has no runtime feedback from production failures. The Crack Propagation and Cynical Software models are critical guardrails: an agent generating integration code should default to always emitting timeout parameters, bounded resource pools, and fallback branches rather than waiting for a human reviewer to catch omissions. Additionally, agents generating shared-service architectures may default to synchronous RPC patterns (the tightest coupling) without considering that this choice propagates failures; the Chain of Failure model should trigger the agent to prefer async or loosely coupled alternatives by default.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Vicious Cycle Pattern resource contention causes slower transactions which cause

## Core Principle

Chapter 9 catalogs design patterns that waste CPU, memory, and bandwidth by doing more work than necessary: resource pool contention that turns thread time into blocking time, excessive class loading from JSP-as-content, AJAX overuse that multiplies request rates, and bloated cookies that resend serialized state on every HTTP request. The common failure mode is selecting a functionally correct design without analyzing its per-unit cost multiplied across concurrent users and server instances. The core fix in each case is to eliminate unnecessary work at the architectural level—right-size pools, keep code and content separate, use AJAX surgically, and store only identifiers client-side.

## Key Heuristics

These are the load-bearing rules for this concept.

> During 'regular peak' operation, there should be no contention for resources.

> If there's always a resource ready when a request-handling thread needs it, then you have no efficiency loss to overhead.

> Blocking indefinitely when resources are exhausted ensures a stability problem.

> Don't use code for content.

> Use cookies for identifiers, not entire objects. Keep session data on the server, where it can't be altered by a malicious client.

> Nobody deliberately selects a design with the purpose of harming the system's capacity; instead, they select a functional design without regard to its effect on capacity.

> The client can lie, might send back stale or broken cookies, and might not send the cookies back at all.

## Anti-Patterns & Fixes

- Resource Pool Contention: thread pool exceeds connection pool size, causing threads to block indefinitely, destroying throughput and creating a stability risk. Fix: size resource pools equal to request thread pool count; configure pools with a finite timeout (maxWait/blocking-timeout-millis) so exhausted pools return null or throw instead of blocking forever.
- Excessive JSP Fragments: treating JSPs as content rather than code causes thousands of compiled classes to fill the JVM permanent generation, leading to garbage collection thrashing and eventual crash-like degradation. Fix: use static HTML fragments with a caching content repository for static content; remove -noclassgc to allow class unloading if many JSPs must exist.
- AJAX Overkill: overusing AJAX reduces think-time between requests from 5-10 seconds to 1-3 seconds and can multiply total request volume, overwhelming servers not sized for Google-scale infrastructure. Fix: use AJAX selectively for genuinely async interactions; measure actual request volume impact before adopting pervasively.
- Cookie Monsters: storing serialized objects (e.g., shopping carts via Java serialization) in cookies creates security vulnerabilities (client can alter prices), versioning failures (stale serialized forms), bandwidth waste (4KB resent on every request), and referential integrity problems. Fix: store only session identifiers in cookies; keep all session state server-side.

## When To Apply

Load this page when:

- Use this when designing or reviewing database connection pool configuration in an application that handles concurrent requests, to ensure pool size matches or exceeds thread pool size.
- Use this when an application uses a thread pool and any shared resource pool (DB connections, HTTP clients, thread executors), to verify that pool exhaustion has a finite timeout rather than indefinite blocking.
- Use this when generating code that creates JSP files, template classes, or any dynamically loaded class per content item, to avoid unbounded growth in the JVM permanent generation.
- Use this when adding AJAX or polling behavior to a frontend, to calculate the actual increase in requests-per-second before implementation.
- Use this when writing code that stores user state or shopping cart data in HTTP cookies, to redirect that state to server-side session storage instead.
- Use this when a load test shows a 'knee' in the throughput curve (throughput flattens as concurrency increases), to diagnose resource pool contention as the likely cause.
- Use this when scaling a server farm (multiple app server instances connecting to one database), to calculate total database connections and RAM cost at full scale.
- Use this when any code deserializes data received from a client (cookie, request body), to flag the security risk of trusting client-supplied serialized objects.

## Concrete Examples

- A server farm with 20 machines, each running 5 app server instances with 50 DB connections each, forces the database server to handle 5,000 simultaneous connections consuming 5GB RAM minimum.
- A site with 25,000 JSP fragments used for product promotions loaded all of them as classes into the permanent generation over a day's runtime, causing severe GC pressure and near-crash degradation.
- A development team used Java serialization to store anonymous users' shopping carts as HTTP cookies, creating security, versioning, referential integrity, and bandwidth problems to avoid writing a database purge job.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 9: Capacity Antipatterns**

An LLM coding agent is especially prone to these antipatterns because it optimizes locally for functional correctness per request: it will generate connection pool configurations with default sizes, produce cookie-based session storage as a 'simple' stateless solution, or scaffold hundreds of template/JSP files without ever modeling the cumulative runtime cost across concurrent users. Unlike a human who experiences production slowdowns and connects them to design choices, an agent has no feedback loop from runtime capacity metrics, so it will confidently reproduce the exact 'functional design without regard to capacity' failure mode described in this chapter—making the multiplier-effect and vicious-cycle patterns invisible until production load reveals them.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
