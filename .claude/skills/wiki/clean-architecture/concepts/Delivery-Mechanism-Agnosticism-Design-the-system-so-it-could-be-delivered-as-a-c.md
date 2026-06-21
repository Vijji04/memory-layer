---
title: Delivery-Mechanism Agnosticism: Design the system so it could be delivered as a console app, web app, thick client, or web service without fundamental architectural change
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Screaming-Architecture.json]
contributing_chapters: ["Screaming Architecture"]
confidence: high
---

# Delivery-Mechanism Agnosticism: Design the system so it could be delivered as a console app, web app, thick client, or web service without fundamental architectural change

> From chapter: *Screaming Architecture*

## Core Principle

A system's architecture should make its business domain immediately obvious — it should 'scream' the use cases, not the frameworks or delivery mechanisms used to implement it. Frameworks, databases, and the web are peripheral tools and details that should be decoupled from core use-case structures and deferred as long as possible. A well-structured architecture enables all use cases to be understood and unit-tested without any framework or infrastructure in place.

## Key Heuristics

These are the load-bearing rules for this concept.

> Architectures are not (or should not be) about frameworks. Architectures should not be supplied by frameworks. Frameworks are tools to be used, not architectures to be conformed to.

> If your architecture is based on frameworks, then it cannot be based on your use cases.

> A good architecture allows decisions about frameworks, databases, web servers, and other environmental issues and tools to be deferred and delayed.

> The web is a delivery mechanism—an IO device—and your application architecture should treat it as such.

> Look at each framework with a jaded eye. View it skeptically. Yes, it might help, but at what cost?

> Your architecture should tell readers about the system, not about the frameworks you used in your system.

> You shouldn't need the web server running to run your tests. You shouldn't need the database connected to run your tests.

## Anti-Patterns & Fixes

- Framework-First Architecture: Organizing top-level directory structure and packages around a framework (e.g., Rails, Spring, Hibernate) so that the system screams its toolchain instead of its domain. Fix: Organize top-level packages around business use cases and domain concepts; push framework-specific code to outer layers.
- True-Believer Framework Adoption: Letting framework authors' all-encompassing examples dictate the entire architectural approach, allowing the framework to 'take over' the architecture. Fix: Develop an explicit strategy to use the framework as a tool at arm's length, protecting core use-case logic from framework dependencies.
- Web-as-Architecture Fallacy: Treating the web delivery mechanism as the architectural foundation, causing all layers to depend on HTTP/web concepts. Fix: Treat web delivery as a detail; ensure core use cases have no knowledge of the delivery mechanism.
- Framework-Coupled Tests: Writing tests that require a running web server or connected database because use-case logic is entangled with infrastructure. Fix: Keep Entity and use-case objects as plain objects with no framework or database dependencies so they can be unit-tested in isolation.

## When To Apply

Load this page when:

- Use this when scaffolding a new project and deciding how to name and organize top-level directories and packages.
- Use this when an agent is tempted to generate a Rails, Spring, or Django project structure as the primary architectural skeleton.
- Use this when writing use-case or business-logic classes and deciding whether they should import or extend framework base classes.
- Use this when setting up a test suite and finding that tests require a running server, database connection, or framework context to execute.
- Use this when a stakeholder asks 'should we commit to PostgreSQL/MySQL/MongoDB now?' to justify deferring that decision.
- Use this when evaluating whether a new framework or library should be integrated deeply into core domain logic versus kept at the boundary.
- Use this when a new developer (or agent) reviews the codebase and cannot identify the business domain from the top-level structure.

## Concrete Examples

- Blueprint of a single-family home: the plans scream 'HOME' through rooms like foyer, living room, kitchen, and family room — illustrating how structure should reveal purpose.
- Blueprint of a library: grand entrance, check-in/out clerks area, reading areas, conference rooms, and book galleries scream 'LIBRARY' — reinforcing domain-expressive structure.
- A health care system where new programmers see models but no views or controllers, and are told 'those are details we'll decide later' — illustrating deferred framework decisions.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Screaming Architecture**

An LLM coding agent defaults to framework-idiomatic scaffolding (e.g., generating a full Rails MVC tree or a Spring Boot starter layout) because training data is saturated with framework tutorials written by 'true believers,' making framework-first structure feel like correct architecture. This chapter prevents the agent failure mode of producing code whose top-level organization is unrecognizable as any particular business domain, and whose use-case logic is inseparably entangled with framework base classes, making it untestable without the full stack. Agents should instead be prompted to name packages after domain use cases first, and only introduce framework wiring at the outermost layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
