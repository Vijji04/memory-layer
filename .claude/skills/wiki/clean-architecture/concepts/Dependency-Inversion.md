---
title: Dependency Inversion: Using polymorphism (interfaces/abstract types) to reverse the direction of source code dependencies so that high-level policy modules do not depend on low-level detail modules
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-5-Object-Oriented-Programming.json]
contributing_chapters: ["Chapter 5: Object-Oriented Programming"]
confidence: high
---

# Dependency Inversion

## Dependency Inversion Using

# Dependency Inversion: Using polymorphism (interfaces/abstract types) to reverse the direction of source code dependencies so that high-level policy modules do not depend on low-level detail modules

> From chapter: *Chapter 5: Object-Oriented Programming*

## Core Principle

OO's most important contribution is not encapsulation or inheritance (both of which existed in C) but safe, convenient polymorphism, which enables dependency inversion: the ability to point any source code dependency opposite to the flow of control. This gives architects absolute control over module boundaries, enabling plugin architectures where high-level business rules are completely independent of low-level details like UI and databases. Independent source code dependencies yield independent deployability and developability — the practical payoff of OO design.

## Key Heuristics

These are the load-bearing rules for this concept.

> OO is the ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system.

> OO imposes discipline on indirect transfer of control.

> The low-level details are relegated to plugin modules that can be deployed and developed independently from the modules that contain high-level policies.

> Any source code dependency, no matter where it is, can be inverted.

> Software architects working in systems written in OO languages have absolute control over the direction of all source code dependencies in the system. They are not constrained to align those dependencies with the flow of control.

> If the modules in your system can be deployed independently, then they can be developed independently by different teams.

> The business rules, the UI, and the database can be compiled into three separate components or deployment units that have the same dependencies as the source code.

## Anti-Patterns & Fixes

- SourceDependencyFollowsControlFlow: Structuring code so that source code dependencies mirror the runtime call chain (main -> high-level -> mid-level -> low-level), which couples every layer to the next and prevents independent deployment. Fix: Insert interfaces at boundaries so high-level modules depend on abstractions, not concrete lower-level modules.
- ManualFunctionPointerPolymorphism: Using raw C-style function pointers to achieve dispatch without enforced conventions, leading to uninitialized pointers and untraceable bugs. Fix: Use OO language polymorphism (virtual functions, interfaces) to make dispatch safe and implicit.
- BusinessRulesDependingOnUI/DB: Writing business logic that directly imports or references UI or database modules, making the core of the system non-deployable without its peripherals. Fix: Invert dependencies so UI and database depend on business rule interfaces, not the reverse.
- WeakEncapsulationReliance: Assuming OO languages provide strong encapsulation by default (e.g., putting private member declarations in headers in C++, or not separating interfaces in Java/C#), exposing implementation details to clients. Fix: Rely on explicit interface types and dependency inversion for information hiding rather than trusting language-level access modifiers alone.

## When To Apply

Load this page when:

- Use this when designing the boundary between business logic and a database or UI layer to decide which direction the dependency should point.
- Use this when a change in a low-level module (e.g., a data store or third-party library) is causing ripple recompilation or redeployment of unrelated high-level modules.
- Use this when adding a new device, service, or implementation variant and you want the existing high-level code to require zero changes.
- Use this when decomposing a system into independently deployable components (e.g., separate JAR files, DLLs, or microservices) and determining which component should own each interface definition.
- Use this when two teams need to develop against a shared boundary concurrently without blocking each other — introduce an interface owned by the high-level module.
- Use this when evaluating whether to use an abstract interface vs. a direct import/dependency in a module that is supposed to represent high-level policy.
- Use this when a calling module must not be recompiled when the called module's implementation changes.

## Concrete Examples

- C point.h/point.c: Perfect encapsulation achieved in C using forward declarations in a header and implementation hidden in a .c file — showing encapsulation predates OO.
- C NamedPoint masquerading as Point: Manually mimicking inheritance in C by ensuring the first two fields of NamedPoint match Point's layout, allowing unsafe casting — showing inheritance predates OO.
- UNIX FILE struct with function pointers (open, close, read, write, seek): Demonstrates polymorphism via explicit function pointer tables in C, showing polymorphism predates OO but is dangerous without language enforcement.
- Copy program reading from STDIN/writing to STDOUT: Illustrates device-independent polymorphic behavior where new IO devices (handwriting recognizer, speech synthesizer) require zero changes to the copy program.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 5: Object-Oriented Programming**

An LLM coding agent, when generating multi-module systems, defaults to following the call graph with its import/dependency graph — high-level modules directly import low-level ones — because that is the most statistically common pattern in training data. This produces architectures where business logic is tightly coupled to database or framework code, making generated systems hard to test, extend, or redeploy independently. Applying dependency inversion as an explicit generation constraint — defining interfaces owned by high-level modules and having low-level modules implement them — prevents the agent from producing the most common but architecturally damaging coupling pattern.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Dependency Inversion via

# Dependency Inversion via Dynamic Polymorphism: Using interfaces and runtime dispatch to invert compile-time dependencies against the flow of control so higher-level components remain independent of lower-level details

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

