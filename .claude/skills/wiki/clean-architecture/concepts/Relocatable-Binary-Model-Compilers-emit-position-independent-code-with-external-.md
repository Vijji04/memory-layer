---
title: Relocatable Binary Model: Compilers emit position-independent code with external reference/definition metadata so a linker can resolve symbols and place code at runtime-determined addresses
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-12-Components.json]
contributing_chapters: ["Chapter 12: Components"]
confidence: high
---

# Relocatable Binary Model: Compilers emit position-independent code with external reference/definition metadata so a linker can resolve symbols and place code at runtime-determined addresses

> From chapter: *Chapter 12: Components*

## Core Principle

Components are the atomic units of deployment—jar files, DLLs, shared libraries—and their defining property is that they must remain independently deployable and therefore independently developable. The chapter traces how 50 years of toolchain evolution (relocatable binaries, linkers, dynamic loading) progressively enabled this property, culminating in the plugin architecture that is now the default. Well-designed components preserve this independence regardless of whether they are ultimately deployed as a single executable, an archive, or dynamically loaded plugins.

## Key Heuristics

These are the load-bearing rules for this concept.

> Well-designed components always retain the ability to be independently deployable and, therefore, independently developable.

> Programs will grow to fill all available compile and link time.

> Components are the granule of deployment.

> These dynamically linked files, which can be plugged together at runtime, are the software components of our architectures.

> Component plugin architecture can be the casual default as opposed to the herculean effort it once was.

## Anti-Patterns & Fixes

- Monolithic Source Compilation: Including all library source directly in the application and compiling everything together. Fix: Separate library source into independently compiled and deployable binary components to reduce compile times and enable reuse.
- Fixed-Address Binary Coupling: Compiling programs to run at hard-coded memory addresses, making relocation impossible and causing fragmentation as programs grow. Fix: Use relocatable binaries with loader-resolved symbol references.
- Merged Link-and-Load Phase: Performing symbol resolution (slow) at load time when programs and libraries are large causes unacceptable startup delays. Fix: Pre-link into a relocatable executable offline; keep the load phase fast.
- Ambition Outpacing Infrastructure: Continuously growing program size erases toolchain speed gains, producing perpetual hour-long turnaround cycles. Fix: Decompose programs into small, independently compilable and linkable components so only changed units need reprocessing.

## When To Apply

Load this page when:

- Use this when deciding what granularity to use for packaging and shipping code (jar, DLL, shared library, gem) to ensure each unit can be deployed independently.
- Use this when a build is taking too long because too many modules are compiled or linked together, signaling the need to split into smaller independently deployable components.
- Use this when designing a plugin or extension system where third-party code must be loaded dynamically at runtime without recompiling the host application.
- Use this when determining the boundary between modules that should be versioned and released together versus modules that need independent release cycles.
- Use this when evaluating whether a proposed code change violates independent deployability by introducing hard compile-time dependencies across component boundaries.
- Use this when generating project scaffolding or build configuration to enforce that each component produces a single deployable artifact with well-defined external interfaces.

## Concrete Examples

- PDP-8 assembly program using *200 origin statement to fix load address at 200 octal, illustrating hard-coded memory layout and non-relocatable code.
- Early memory layout where function library was compiled to a fixed address (e.g., 2000 octal) and applications had to fit in remaining space, leading to fragmentation when apps grew.
- Minecraft .jar mod folder and ReSharper DLLs in Visual Studio as present-day examples of component plugin architecture in casual use.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 12: Components**

An LLM coding agent tends to generate large monolithic files or inline all dependencies into a single compilation unit because it operates on a per-prompt context rather than a deployment topology—mirroring the early 'include all library source' anti-pattern. This chapter's principle forces the agent to explicitly reason about deployment boundaries when generating code: each generated artifact must be independently buildable and releasable, not just syntactically correct. Failing to apply this causes agent-generated codebases to become tightly coupled blobs where a single change requires rebuilding and redeploying everything, eliminating the independent developability that makes component-based systems maintainable.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
