---
title: Plugin Architecture for Low-Level Components: Lower-level components are designed as plugins to higher-level ones, so the high-level component knows nothing of the low-level implementation
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Policy-and-Level.json]
contributing_chapters: ["Policy and Level"]
confidence: high
---

# Plugin Architecture for Low-Level Components: Lower-level components are designed as plugins to higher-level ones, so the high-level component knows nothing of the low-level implementation

> From chapter: *Policy and Level*

## Core Principle

Every software program is a set of policies, and those policies differ in their level — defined as distance from system inputs and outputs. High-level policies are more stable and important; low-level policies are volatile and urgent. Good architecture separates policies by level, organizes them into a DAG of components, and ensures all compile-time dependencies point toward higher-level components regardless of data flow direction, so that trivial I/O changes never destabilize core business logic.

## Key Heuristics

These are the load-bearing rules for this concept.

> A strict definition of 'level' is 'the distance from the inputs and outputs.'

> In a good architecture, the direction of those dependencies is based on the level of the components that they connect. In every case, low-level components are designed so that they depend on high-level components.

> We want source code dependencies to be decoupled from data flow and coupled to level.

> Higher-level policies—those that are farthest from the inputs and outputs—tend to change less frequently, and for more important reasons, than lower-level policies.

> Lower-level policies—those that are closest to the inputs and outputs—tend to change frequently, and with more urgency, but for less important reasons.

> Keeping these policies separate, with all source code dependencies pointing in the direction of the higher-level policies, reduces the impact of change.

> Lower-level components should be plugins to the higher-level components.

> Policies that change for the same reasons, and at the same times, are at the same level and belong together in the same component.

## Anti-Patterns & Fixes

- High-Level-Depends-on-Low-Level: Writing a top-level function (e.g., encrypt()) that directly calls low-level I/O functions (readChar, writeChar) causes the core business logic to be coupled to peripheral concerns. Fix: Introduce interfaces (CharReader, CharWriter) that the high-level component depends on; let low-level concrete classes (ConsoleReader, ConsoleWriter) implement those interfaces, inverting the dependency.
- Data-Flow-Mirrored-Dependencies: Structuring source code dependencies to follow the data flow direction rather than the level hierarchy entangles stable policies with volatile ones. Fix: Allow data to flow through components in one direction while source code dependencies point in the opposite direction toward higher-level components.
- Mixing Policies of Different Levels in One Component: Grouping policies that change for different reasons and at different times into the same component causes frequent, low-urgency I/O changes to destabilize important business logic. Fix: Separate policies by their rate and reason of change, placing them in distinct components connected by directed dependencies.
- Concrete I/O Coupled to Core Algorithm: Directly referencing concrete I/O classes inside the encryption or business logic layer makes the core policy non-reusable across contexts. Fix: Wrap I/O behind abstractions owned by the high-level component so the encryption policy is usable in any I/O context.

## When To Apply

Load this page when:

- Use this when designing a new module that has both core business logic and I/O handling, to decide which direction dependencies should point.
- Use this when a change to a peripheral concern (file format, UI, device driver) is breaking or requiring modification to core logic.
- Use this when deciding whether two classes or modules should be co-located in the same component or separated into different components.
- Use this when tracing why a stable, rarely-changed algorithm is being forced to recompile or redeploy when low-level infrastructure changes.
- Use this when generating a new feature end-to-end and needing to determine the correct layering so that high-level policy files do not import low-level implementation files.
- Use this when evaluating whether an existing architecture's dependency graph is a valid DAG with correct directional flow.
- Use this when introducing a new I/O mechanism (e.g., switching from file to network input) and needing to ensure zero changes to core business logic.

## Concrete Examples

- Simple encryption program: reads characters from an input device, translates them using a table, and writes translated characters to an output device — used to illustrate incorrect vs. correct dependency direction.
- Incorrect encrypt() function that directly calls readChar() and writeChar(), demonstrating a high-level function incorrectly depending on low-level I/O functions.
- Correct class diagram with Encrypt class depending on CharReader and CharWriter interfaces, while ConsoleReader and ConsoleWriter implement those interfaces — showing all dependencies crossing the boundary pointing inward.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Policy and Level**

An LLM coding agent, when generating end-to-end feature code in a single pass, will naturally mirror data flow in its import/dependency structure — writing high-level functions that directly call low-level I/O utilities — because the shortest, most literal code path matches data flow. This chapter's framework prevents that failure mode by requiring the agent to explicitly invert dependencies through interfaces whenever it identifies a level boundary. Agents must treat 'distance from I/O' as a first-class architectural signal when deciding which module owns an interface definition and which module depends on it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
