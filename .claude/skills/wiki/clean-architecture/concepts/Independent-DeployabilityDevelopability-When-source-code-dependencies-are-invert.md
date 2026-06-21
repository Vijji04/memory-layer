---
title: Independent Deployability/Developability: When source code dependencies are inverted so components depend only on abstractions, each component can be compiled, deployed, and developed independently
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-5-Object-Oriented-Programming.json]
contributing_chapters: ["Chapter 5: Object-Oriented Programming"]
confidence: high
---

# Independent Deployability/Developability: When source code dependencies are inverted so components depend only on abstractions, each component can be compiled, deployed, and developed independently

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
