---
title: Temporal Coupling: the design problem of creating hidden time-ordering dependencies between components, forcing sequential execution where parallelism is possible
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Temporal-Coupling.json]
contributing_chapters: ["Temporal Coupling"]
confidence: high
---

# Temporal Coupling: the design problem of creating hidden time-ordering dependencies between components, forcing sequential execution where parallelism is possible

> From chapter: *Temporal Coupling*

## Core Principle

Temporal coupling occurs when software design imposes hidden time-ordering or synchronization constraints that are not logically required, reducing flexibility and scalability. The fix is to actively analyze workflows for parallelism, design components as independent concurrent services communicating via asynchronous interfaces, and ensure objects are always in a valid state regardless of call order. Designing for concurrency from the start is far cheaper than retrofitting it later and produces cleaner, more deployable architectures even when concurrency is not immediately needed.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 39: Analyze Workflow to Improve Concurrency

> Tip 40: Design Using Services

> Tip 41: Always Design for Concurrency

> Instead of components, we have really created services—independent, concurrent objects behind well-defined, consistent interfaces.

> Objects must always be in a valid state when called, and they can be called at the most awkward times.

> Going the other way (trying to add concurrency to a nonconcurrent application) is much harder.

> By planning for concurrency, and decoupling operations in time, you have all these options—including the stand-alone option, where you can choose not to be concurrent.

## Anti-Patterns & Fixes

- Linear Sequential Thinking: designing workflows and APIs as strictly ordered sequences when steps could run in parallel, causing unnecessary bottlenecks. Fix: use activity diagrams to identify which steps truly depend on each other and parallelize the rest.
- Hidden Implicit State (strtok pattern): functions that retain hidden state between calls force single-threaded sequential usage and make parallel or interleaved use impossible. Fix: encapsulate parse/iteration state in an object instance (e.g., Java StringTokenizer) so multiple independent uses can proceed concurrently.
- Invalid Constructor/Initialization Split: objects that require a separate initialization call after construction are in an invalid state between the two calls, which is safe only by coincidence in single-threaded code. Fix: use class invariants and ensure objects are fully valid immediately after construction.
- Monolithic Blocking Architecture: processing pipeline steps that block each other (e.g., DB operation blocking communication layer) create temporal coupling across unrelated concerns. Fix: decouple via asynchronous work queues between independently running processes.
- Global and Static Variables in Shared Code: global/static state creates hidden temporal coupling between callers, causing race conditions in concurrent contexts. Fix: eliminate globals or protect them with proper synchronization; prefer instance-scoped state.

## When To Apply

Load this page when:

- Use this when designing a multi-step processing pipeline where some steps are slower than others and you need to prevent slow steps from blocking fast ones.
- Use this when modeling user workflows during requirements analysis to identify which steps can be parallelized for performance.
- Use this when designing an API where a caller must invoke methods in a specific order (e.g., init() before use()) and you want to eliminate that constraint.
- Use this when a function or module uses static or global state to maintain context between calls, making it unsafe for concurrent or interleaved use.
- Use this when architecting a system that may need to scale from standalone deployment to distributed/client-server deployment without major redesign.
- Use this when a component must interact with a slow external resource (database, network) and you want to prevent that latency from propagating to other components.
- Use this when reviewing generated code that performs sequential operations to check whether any steps could be parallelized or decoupled via queues.

## Concrete Examples

- Piña colada recipe analysis: a 12-step serial recipe is mapped to a UML activity diagram revealing that steps 1, 2, 4, 10, and 11 can all start concurrently, with later steps also parallelizable.
- OLTP three-tier architecture: input tasks, application logic, and database handler run as independent processes communicating via asynchronous work queues, preventing DB latency from blocking communication services.
- C strtok vs. Java StringTokenizer: strtok retains hidden static state making interleaved parsing of two strings impossible; StringTokenizer encapsulates state per instance, enabling concurrent and interleaved use safely.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Temporal Coupling**

An LLM coding agent defaults to generating linear, sequential code because it predicts tokens in sequence and naturally models control flow as ordered steps—directly producing temporal coupling without flagging it. When an agent scaffolds a class with separate init() and setup() methods, generates a pipeline as nested blocking calls, or reuses a stateful utility function across multiple code paths, it silently introduces the exact anti-patterns this chapter warns against. Applying this chapter means an agent should, by default, audit generated architectures for implicit ordering dependencies, prefer object-scoped state over static/global state, and structure multi-step pipelines with queue-based decoupling rather than direct sequential calls.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
