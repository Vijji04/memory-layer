---
title: General Contractor Model: A module should perform services on behalf of its caller by delegating to subcontractors internally, never forcing the caller to deal with subcontractors directly
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Decoupling-and-the-Law-of-Demeter.json]
contributing_chapters: ["Decoupling and the Law of Demeter"]
confidence: high
---

# General Contractor Model: A module should perform services on behalf of its caller by delegating to subcontractors internally, never forcing the caller to deal with subcontractors directly

> From chapter: *Decoupling and the Law of Demeter*

## Core Principle

The Law of Demeter mandates that methods only interact with their immediate neighbors (self, parameters, created objects, direct components), preventing the combinatorial explosion of dependencies that arises from traversing object graphs. Violations manifest as long method chains, cascading changes across unrelated modules, and codebases too fragile to modify safely. The cost is additional delegation/wrapper methods, but the benefit is modular resilience where replacing or changing one module does not ripple unpredictably through the system.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 36: Minimize Coupling Between Modules

> Writing 'shy' code that honors the Law of Demeter as much as possible

> 'Shy' works two ways: don't reveal yourself to others, and don't interact with too many people.

> Traversing relationships between objects directly can quickly lead to a combinatorial explosion of dependency relationships.

> We do not want the object to give us a third-party object that we have to deal with to get the required service.

> Classes in C++ with larger response sets are more prone to error than classes with smaller response sets.

> By reversing the Law of Demeter and tightly coupling several modules, you may realize an important performance gain — as long as it is well known and acceptable for those modules to be coupled.

## Anti-Patterns & Fixes

- Train Wreck / Method Chaining: Calling aSelection.getRecorder().getLocation().getTimeZone() creates hidden coupling to Selection, Recorder, and Location simultaneously. Fix: Add a delegation method (e.g., aSelection.getTimeZone()) so the caller only depends on Selection.
- Reaching Through Objects: Accessing a third party's methods by traversing object graphs rather than asking directly for what is needed. Fix: Ask for the data or service you need directly via parameters or delegation methods.
- Fearful Codebase: Developers afraid to change code because they aren't sure what might be affected — a symptom of excessive coupling. Fix: Apply Law of Demeter to reduce response sets and make change impact predictable.
- Explosive Dependency Linking: Build commands for unit tests longer than the test itself, indicating the entire system is dragged in as support code. Fix: Enforce logical and physical decoupling in tandem; avoid cyclic dependencies.
- Unchecked Dependency Growth: Simple changes to one module propagate through unrelated modules. Fix: Organize code into cells/modules with strictly limited inter-module interactions.

## When To Apply

Load this page when:

- Use this when a method accesses a chain of objects (a.getB().getC().doSomething()) and you need to assess or reduce coupling.
- Use this when a change to one class requires cascading changes in multiple seemingly unrelated classes.
- Use this when designing a new method signature and deciding whether to pass in a complex object or just the specific data needed.
- Use this when a unit test requires importing or instantiating a large portion of the system to run.
- Use this when a module is being replaced or refactored and you need to assess blast radius across the codebase.
- Use this when generating wrapper or delegation methods to satisfy Law of Demeter without exposing subcontractors to callers.
- Use this when evaluating whether a performance optimization justifies intentional tight coupling between specific modules.

## Concrete Examples

- plotDate method retrieving TimeZone via aSelection.getRecorder().getLocation().getTimeZone() — refactored to accept TimeZone directly as a parameter and add getTimeZone() to Selection.
- C++ Demeter class diagram showing which calls are legal: calls to self, passed-in parameters (B& b), locally created objects (C c), and directly held components (A *a).
- Person1.h vs Person2.h physical coupling comparison: Person1 includes date.h directly (tighter coupling) vs Person2 uses a forward declaration of Date (looser coupling).
- BankAccount/processTransaction exercise where who = acct.getOwner() followed by who->name() violates Law of Demeter by reaching through to a third-party object.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Decoupling and the Law of Demeter**

An LLM coding agent naturally generates fluent method chains and deeply nested object traversals because they are syntactically valid and locally coherent at the point of generation — the agent has no persistent awareness of the growing coupling debt accumulating across a file or codebase. This causes agent-generated code to silently build fragile dependency webs that only break visibly during integration or refactoring. Applying Law of Demeter as a generative constraint — checking each generated method call against the four permitted targets (self, parameters, created objects, held components) — directly prevents the agent from emitting train-wreck chains that a human reviewer would catch but that automated tests may miss.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
