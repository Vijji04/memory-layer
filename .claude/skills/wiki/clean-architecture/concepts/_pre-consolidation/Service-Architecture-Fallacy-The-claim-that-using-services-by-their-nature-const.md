---
title: Service Architecture Fallacy: The claim that using services by their nature constitutes architecture is false; architecture is defined by boundaries and the Dependency Rule, not by process separation
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-27-Services-Great-and-Small.json]
contributing_chapters: ["Chapter 27: Services: Great and Small"]
confidence: high
---

# Service Architecture Fallacy: The claim that using services by their nature constitutes architecture is false; architecture is defined by boundaries and the Dependency Rule, not by process separation

> From chapter: *Chapter 27: Services: Great and Small*

## Core Principle

Services are not architecture by virtue of being services; architecture is defined by Dependency Rule boundaries that may run through services, not merely between them. The popular claims that microservices provide strong decoupling and independent deployability are largely fallacies: shared data schemas couple services tightly, and cross-cutting features force coordinated changes across all functionally decomposed services. The correct approach is to give each service an internal SOLID-compliant component structure so new features are added as new loadable components, satisfying the Open-Closed Principle without modifying existing service code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Services that simply separate application behaviors are little more than expensive function calls, and are not necessarily architecturally significant.

> The architecture of a system is defined by the boundaries drawn within that system, and by the dependencies that cross those boundaries. That architecture is not defined by the physical mechanisms by which elements communicate and execute.

> Architectural boundaries do not fall between services. Rather, those boundaries run through the services, dividing them into components.

> Services do not need to be little monoliths. Services can be designed using the SOLID principles, and given a component structure so that new components can be added to them without changing the existing components within the service.

> To the extent that they are coupled by data or behavior, the development, deployment, and operation must be coordinated.

> Adding new features conforms to the Open-Closed Principle [when services have internal component architectures].

> The number of micro-services will be roughly equal to the number of programmers.

## Anti-Patterns & Fixes

- Mistaking Process Boundaries for Architecture: Assuming that splitting a system into services automatically creates good architecture. Fix: Identify architectural boundaries by applying the Dependency Rule inside each service, not just at the service perimeter.
- Functional Decomposition into Services: Organizing services purely by function (TaxiFinder, TaxiSelector, TaxiDispatcher) makes every cross-cutting feature require changes to all services simultaneously. Fix: Design services with internal polymorphic component structures (Template Method or Strategy patterns) so new features are added as new components, not as modifications to existing ones.
- Assuming Service Interfaces Are Stronger Contracts Than Function Interfaces: Treating service boundaries as inherently more rigorous decoupling than in-process function calls. Fix: Recognize that adding a field to a shared data record still couples all consuming services; treat data schema changes with the same discipline as public API changes.
- Monolithic Services Without Internal Component Design: Building each service as a single undifferentiated deployable unit. Fix: Structure each service internally as a set of abstract base classes with feature-specific implementations in separate loadable components (jar files, DLLs), enabling OCP-compliant feature extension.
- Equating Independent Deployment with Independent Development: Assuming services can be developed in isolation because they are deployed separately. Fix: Map data and behavioral dependencies between services explicitly; any shared schema or protocol change requires coordinated development across all coupled services.

## When To Apply

Load this page when:

- Use this when designing a new microservice system and deciding whether to split functionality across service boundaries or within a service's internal component structure.
- Use this when a new feature request touches multiple existing services simultaneously, signaling a cross-cutting concern that exposes functional decomposition fragility.
- Use this when evaluating whether a proposed service split constitutes a meaningful architectural boundary or is merely an expensive remote function call.
- Use this when adding a new field to a shared data transfer object or message schema and needing to assess the blast radius of the change.
- Use this when a team claims that microservices give them independent deployability but releases still require coordinating multiple teams.
- Use this when refactoring a service to support extensibility: apply OCP by introducing abstract base classes and loading feature implementations as separate deployable components.
- Use this when deciding how many microservices to create for a given team size, recognizing that granularity should follow architectural boundaries, not headcount.

## Concrete Examples

- Taxi aggregator system with TaxiUI, TaxiFinder, TaxiSelector, and TaxiDispatcher services: adding a kitten delivery feature requires changes to all services, demonstrating cross-cutting concern vulnerability in functionally decomposed service graphs.
- Refactored taxi system using OCP-compliant object model: Rides and Kittens components extend abstract base classes via Template Method or Strategy patterns, so the Kitty feature adds a new jar file without modifying existing services.
- Java service modeled as abstract classes in jar files, with each new feature as an additional jar file extending those abstractions, deployed by adding to the service's load path rather than redeploying the service itself.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 27: Services: Great and Small**

An LLM coding agent is especially prone to the functional decomposition anti-pattern because it naturally mirrors the structure of a feature request—generating one service per named concept—without evaluating whether those boundaries follow the Dependency Rule or are architecturally significant. This produces service graphs where every generated feature change cascades across all services, making the agent's output superficially modular but deeply coupled. Agents must be explicitly prompted to design internal component architectures within each service using OCP/SOLID principles, and to distinguish cross-cutting concerns from true architectural boundaries before generating service boundaries.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
