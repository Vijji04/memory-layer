---
title: Cookie as State Mechanism: cookies were designed for small identifiers (<100 bytes) for session management, not for storing serialized objects or persistent data
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
sources: [extracts/release-it/Chapter-9-Capacity-Antipatterns.json]
contributing_chapters: ["Chapter 9: Capacity Antipatterns"]
confidence: high
---

# Cookie as State Mechanism: cookies were designed for small identifiers (<100 bytes) for session management, not for storing serialized objects or persistent data

> From chapter: *Chapter 9: Capacity Antipatterns*

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
