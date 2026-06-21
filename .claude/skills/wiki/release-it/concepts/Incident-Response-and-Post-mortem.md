---
title: Incident Response and Post-mortem
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
confidence: high
consolidated_from: 3 pages
---

# Incident Response and Post-mortem

> Consolidated from 3 related concept pages.

---

## Automated Data Collection for Post Mortem A pattern of pre scripted non intrusiv

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

## Cynical Requirements Examination the practice of viewing system requirements and

## Core Principle

At production scale, statistically rare failure combinations become near-certainties; stability antipatterns transform these transient events into catastrophic outages while stability patterns contain the damage. The chapter closes a six-chapter arc on stability by reiterating that failures are inevitable, that paranoid design is rational, and that the goal is not preventing all failures but ensuring the system survives them. Judgment in matching specific stability patterns to specific identified threats — not blanket application — is the key differentiator.

## Key Heuristics

These are the load-bearing rules for this concept.

> Astronomically unlikely coincidences happen daily.

> Failures are inevitable.

> Stability antipatterns amplify transient events. They accelerate cracks in the system.

> Avoiding the antipatterns does not prevent bad things from happening, but it will help minimize the damage when bad things do occur.

> View other enterprise systems with suspicion and distrust—any of them can stab you in the back.

> Paranoia is just good thinking.

> Staying up is more than half the battle.

## Anti-Patterns & Fixes

- Optimism Bias: assuming edge cases or unlikely failure combinations won't occur in production. Fix: calculate actual opportunity count (requests × assets × time) to reframe 'astronomical' odds as near-certainties at scale.
- Stability Antipattern Accumulation: allowing known antipatterns to persist in the codebase because failures haven't happened yet. Fix: proactively identify and eliminate antipatterns before they amplify real transient events.
- Undifferentiated Threat Response: applying stability patterns uniformly or not at all rather than matching patterns to specific threats. Fix: identify each threat explicitly and apply the most appropriate stability pattern to each one.
- Dependency Trust: treating integrated enterprise systems or third-party services as reliably stable. Fix: assume all external dependencies can and will fail; design defensively around every integration point.

## When To Apply

Load this page when:

- Use this when designing integration points with external services, databases, or third-party APIs where a failure could cascade.
- Use this when estimating the risk of an edge case in a high-traffic system — multiply request rate by time to get actual failure opportunity count before dismissing it as unlikely.
- Use this when reviewing generated code for missing error handling, timeouts, retries, or circuit breakers around I/O operations.
- Use this when a system is approaching production and stability patterns have not been explicitly applied to identified threat surfaces.
- Use this when evaluating whether to add defensive code that 'probably won't be needed' — reframe using the scale heuristic.
- Use this when auditing a codebase that has had stability incidents to identify which antipatterns amplified the original transient fault.

## Concrete Examples

- Ten million page views per day over three years with fifty assets per page yields 547,500,000,000 chances for something to go wrong — more than the estimated 400 billion stars in the Milky Way galaxy.
- The survival statistics of software projects: ~50% canceled in development, ~50% of survivors late/overbudget/feature-incomplete, leaving less than 25% reaching production — and of those, most incur major downtime and maintenance costs.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 6: Stability Summary**

An LLM coding agent is especially prone to optimism bias by default: it generates the 'happy path' implementation without spontaneously adding timeouts, bulkheads, or circuit breakers unless explicitly prompted, because training data skews toward functional examples rather than defensive ones. This chapter's scale heuristic is a forcing function an agent can apply mechanically — given request volume and asset count, it can compute actual failure opportunity counts and self-trigger the addition of stability patterns. The agent should treat every external call it generates as a potential stab-in-the-back and default to wrapping it in a stability pattern rather than waiting for a human to notice the gap.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Cynical Software Model Enterprise software must expect bad things to happen neve

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
