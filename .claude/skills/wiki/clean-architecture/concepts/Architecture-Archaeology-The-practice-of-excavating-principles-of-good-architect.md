---
title: Architecture Archaeology: The practice of excavating principles of good architecture by examining real historical systems, tracing how constraints shaped structural decisions over decades
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Appendix-A-Architecture-Archaeology.json]
contributing_chapters: ["Appendix A: Architecture Archaeology"]
confidence: high
---

# Architecture Archaeology: The practice of excavating principles of good architecture by examining real historical systems, tracing how constraints shaped structural decisions over decades

> From chapter: *Appendix A: Architecture Archaeology*

## Core Principle

This appendix uses a 45-year retrospective of real systems to illustrate two foundational boundary types: dependency-normal (control and dependency flow same direction) and dependency-inverted (control crosses opposite to compile-time dependency). The Union Accounting System concretely demonstrates both: an abstract output boundary isolates applications from terminal hardware, while a fixed memory entry-point inverts the supervisor-to-application dependency. The recurring lesson is that good architecture is defined by what each component is prevented from knowing.

## Key Heuristics

These are the load-bearing rules for this concept.

> The boundary prevented the applications from knowing which kind of device the output was going to.

> The boundary prevented the supervisor from knowing anything about the applications other than the starting point.

> Every application was started by jumping to the exact same memory address within the overlay area.

> There was not a single bit in that system that we did not write.

> The applications had no idea that their output was going to a 30-cps terminal. Indeed, the character output was entirely abstract from the applications' point of view.

## Anti-Patterns & Fixes

- Cramming Everything Into One Address Space: The original Union Accounting system crammed the whole application into 16K with no modularity. Fix: Use an overlay system or equivalent partitioning so programs are independently loadable and swappable.
- Compile-Time Coupling Between Supervisor and Applications: If the supervisor has compile-time dependencies on each application, adding or changing applications requires recompiling the supervisor. Fix: Invert the dependency — define a fixed polymorphic entry point (e.g., a fixed memory address or interface) so the supervisor knows nothing about individual applications.
- Hardcoding Output Device Assumptions: Applications that directly reference terminal speed or device characteristics become fragile when hardware changes. Fix: Abstract all output through the supervisor layer so applications pass strings and the supervisor handles buffering and device specifics.

## When To Apply

Load this page when:

- Use this when designing a system where a central coordinator (supervisor/scheduler) must invoke multiple independent modules without being coupled to their internals.
- Use this when output or IO speed is orders of magnitude slower than compute speed, requiring buffering and decoupling between application logic and device drivers.
- Use this when memory is severely constrained and multiple programs must share a single execution environment — apply an overlay/swap pattern.
- Use this when drawing a boundary between a framework/runtime and application code, to decide which direction dependencies should point.
- Use this when determining whether a boundary should be dependency-normal or dependency-inverted based on what each side needs to remain ignorant of.

## Concrete Examples

- Union Accounting System on Varian 620/f: a preemptive overlay supervisor swapped applications in/out of a fixed memory area to serve multiple 30-cps terminals, with two explicit architectural boundaries — one dependency-normal (apps to supervisor) and one dependency-inverted (supervisor to apps via fixed entry-point address).
- Laser Trim system at Teradyne Applied Systems (TAS) on M365: a system controlling positioning tables, laser mirrors, and measurement — built on tape-cartridge-based storage with no disk, illustrating extreme hardware constraint-driven architecture.
- Original GE Datanet 30 Union Accounting system: entire application crammed into 16K of assembly by a consultant, replaced due to cost and inflexibility.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Appendix A: Architecture Archaeology**

An LLM coding agent, when generating a supervisor/coordinator pattern, will default to direct compile-time coupling between the coordinator and each module it manages — exactly the anti-pattern described. Applying the dependency-inverted boundary principle forces the agent to define a fixed polymorphic interface or entry contract so the coordinator remains ignorant of module internals. Additionally, agents tend to skip IO abstraction layers when generating device-interaction code; this chapter's output-boundary pattern explicitly prevents agents from hardcoding device assumptions into business logic.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
