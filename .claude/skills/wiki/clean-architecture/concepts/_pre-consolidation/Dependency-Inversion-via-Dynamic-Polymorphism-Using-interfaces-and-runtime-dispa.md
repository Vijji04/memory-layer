---
title: Dependency Inversion via Dynamic Polymorphism: Using interfaces and runtime dispatch to invert compile-time dependencies against the flow of control so higher-level components remain independent of lower-level details
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-18-Boundary-Anatomy.json]
contributing_chapters: ["Chapter 18: Boundary Anatomy"]
confidence: high
---

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
