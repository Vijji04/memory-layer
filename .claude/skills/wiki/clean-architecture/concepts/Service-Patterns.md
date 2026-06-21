---
title: Component-Based Services: Services designed with internal SOLID-compliant component architectures allow new features to be added via new components (jar files, DLLs) without modifying existing service code, conforming to the Open-Closed Principle
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-27-Services-Great-and-Small.json]
contributing_chapters: ["Chapter 27: Services: Great and Small"]
confidence: high
---

# Service Patterns

## Component Based Services

# Component-Based Services: Services designed with internal SOLID-compliant component architectures allow new features to be added via new components (jar files, DLLs) without modifying existing service code, conforming to the Open-Closed Principle

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


## Cross Cutting Concern

# Cross-Cutting Concern Vulnerability: Functionally decomposed service graphs are inherently fragile when new features must touch every service; OCP-compliant polymorphic component design is the countermeasure

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


## Decoupling Fallacy Services

# Decoupling Fallacy: Services are not strongly decoupled merely because they run in separate processes; they remain coupled through shared data schemas and behavioral contracts

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


## Independent Development Fallacy

# Independent Development Fallacy: Services cannot always be independently developed and deployed because data or behavioral coupling forces coordinated changes across service boundaries

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


## Service Architecture Fallacy

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


## Service Boundary Strongest

# Service Boundary: Strongest boundary; network-based communication assumed, high latency, location-independent

> From chapter: *Chapter 18: Boundary Anatomy*

## Core Principle

Architectural boundaries exist in four physical forms — monolith, deployment component, local process, and service — each with different communication costs that dictate how chatty cross-boundary interactions can be. In all cases, source code dependencies must point toward higher-level components, with dynamic polymorphism used to invert the dependency when the flow of control runs the other way. Real systems typically combine multiple boundary types, requiring architects to consciously apply the correct latency and coupling rules at each level.

## Key Heuristics

These are the load-bearing rules for this concept.

> The trick to creating an appropriate boundary crossing is to manage the source code dependencies.

> Managing and building firewalls against this change is what boundaries are all about.

> Even when statically linked into a single executable, the ability to independently develop and marshal the various components for final assembly is immensely valuable.

> The architectural goal is for lower-level processes to be plugins to higher-level processes.

> The source code of higher-level services must not contain any specific physical knowledge (e.g., a URI) of any lower-level service.

> Communications across service boundaries are very slow compared to function calls. Care must be taken to avoid chatting where possible.

> Chattiness should be carefully limited [for local process boundaries].

> A service is often just a facade for a set of interacting local processes.

## Anti-Patterns & Fixes

- ChattyServiceCommunication: Treating service or local-process boundaries like cheap function calls and making frequent fine-grained calls across them, ignoring latency costs. Fix: Batch calls, use coarse-grained interfaces, and design for high latency at service and local-process boundaries.
- Higher-Level Component Knowing Lower-Level Addresses: High-level source code contains names, physical addresses, URIs, or registry lookup keys of lower-level components or services, creating tight coupling. Fix: Depend only on abstractions/interfaces; let lower-level components register or be injected as plugins.
- Abandoning Component Partitioning Without Polymorphism: Without OO or equivalent dynamic polymorphism, architects resort to function pointers for decoupling, which is too risky and leads to abandoning partitioning entirely. Fix: Use dynamic polymorphism (interfaces, abstract classes) to invert dependencies and maintain component boundaries.
- Ignoring Boundaries in a Monolith: Treating a single executable as having no meaningful boundaries because none are physically visible at deployment. Fix: Enforce disciplined source-level partitioning and dependency rules even inside a monolith to enable independent development and testing.

## When To Apply

Load this page when:

- Use this when deciding whether to split a feature into a separate service, local process, or keep it in-process, to reason about communication cost and latency trade-offs.
- Use this when a high-level module's source code references a concrete class, URI, or address of a lower-level module, signaling a boundary direction violation.
- Use this when designing how two components should communicate (function call vs. IPC vs. network) to select the appropriate boundary type and chattiness limit.
- Use this when a team is independently developing components within a monolith and needs to enforce that compile-time dependencies always point toward higher-level components.
- Use this when evaluating whether to use dynamic linking (deployment components) vs. static linking (monolith) to understand the trade-offs in recompilation, redeployment, and coupling.
- Use this when a service is calling another service in a tight loop or with fine-grained requests, to identify a chatty boundary anti-pattern that needs coarse-graining.
- Use this when generating or reviewing code that wires together components, to verify the dependency arrows point in the correct direction (toward higher-level abstractions).

## Concrete Examples

- Figure 18.1: A low-level Client calls function f() on a higher-level Service, passing a Data structure defined on the called side — flow of control and dependency point in the same direction.
- Figure 18.2: A high-level Client calls f() on a lower-level ServiceImpl through a Service interface, inverting the compile-time dependency against the flow of control; Data is defined on the calling side.
- Deployment components as .NET DLLs, Java JAR files, Ruby Gems, or UNIX shared libraries delivered in binary form without recompilation.
- A monolith as a statically linked C/C++ project, a set of Java class files in an executable JAR, or a set of .NET binaries in a single EXE.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 18: Boundary Anatomy**

An LLM coding agent is prone to ignoring boundary types entirely — generating code that makes synchronous, fine-grained calls across what should be a high-latency service boundary (chatty service anti-pattern) or directly embedding service URIs and process addresses into high-level modules rather than depending on abstractions. Unlike a human who feels the pain of latency in production, an agent has no runtime feedback loop, so it must apply boundary anatomy rules structurally at code-generation time: checking dependency direction, enforcing interface abstractions at every boundary, and selecting communication granularity based on boundary type before any code is written.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

