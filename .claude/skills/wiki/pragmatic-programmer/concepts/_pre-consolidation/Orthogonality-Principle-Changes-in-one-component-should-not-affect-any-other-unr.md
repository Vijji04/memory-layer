---
title: Orthogonality Principle: Changes in one component should not affect any other unrelated component — independence and decoupling as a first-class design goal
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Orthogonality.json]
contributing_chapters: ["Orthogonality"]
confidence: high
---

# Orthogonality Principle: Changes in one component should not affect any other unrelated component — independence and decoupling as a first-class design goal

> From chapter: *Orthogonality*

## Core Principle

Orthogonality means designing components so that changes in one have zero effect on others — independence and decoupling as explicit goals, not accidental outcomes. Orthogonal systems yield multiplicative productivity gains, localized bug containment, easier testing, and reduced vendor lock-in. The principle applies equally to code structure, team organization, toolkit selection, and documentation, and is best enforced by asking: how many modules must change for a single requirement change?

## Key Heuristics

These are the load-bearing rules for this concept.

> Eliminate Effects Between Unrelated Things

> If I dramatically change the requirements behind a particular function, how many modules are affected? In an orthogonal system, the answer should be 'one.'

> When components are isolated from one another, you know that you can change one without having to worry about the rest.

> If a module is sick, it is less likely to spread the symptoms around the rest of the system.

> Building unit tests is itself an interesting test of orthogonality. What does it take to build and link a unit test? Do you have to drag in a large percentage of the rest of the system just to get a test to compile or link?

> Don't rely on the properties of things you can't control.

> Your code is easier to understand and maintain if you explicitly pass any required context into your modules.

> If you use the principle of orthogonality, combined closely with the DRY principle, you'll find that the systems you develop are more flexible, more understandable, and easier to debug, test, and maintain.

## Anti-Patterns & Fixes

- GlobalDataCoupling: Referencing global data ties a component to every other component that shares it, creating hidden dependencies. Fix: Explicitly pass required context as parameters or constructor arguments instead of reading from globals or singletons.
- NonOrthogonalToolkitAdoption: Importing a library that forces you to access or create objects in special ways (e.g., RMI throwing location-aware exceptions everywhere) contaminates your codebase with third-party coupling. Fix: Choose toolkits that are transparent to calling code; isolate third-party interfaces to small boundary layers.
- OverlappingTeamResponsibilities: When multiple team members own the same code area, every change requires a whole-team meeting and creates confusion. Fix: Assign well-defined, non-overlapping responsibilities per subteam; measure orthogonality by counting people needed per change discussion.
- DuplicatedSimilarFunctions: Functions sharing start/end code with different central algorithms indicate structural problems and hidden coupling. Fix: Apply the Strategy pattern to extract the varying algorithm as an injectable component.
- ExternalPropertyAsIdentifier: Using an externally controlled value (e.g., phone number as customer ID) as an internal key couples your schema to outside change. Fix: Use internally controlled identifiers; isolate external identifiers behind an abstraction.
- ScatteredBugFixes: A bug fix that requires changes across multiple modules signals non-orthogonal design. Fix: Refactor to localize responsibility before or during the fix; track fix spread using source control metrics.

## When To Apply

Load this page when:

- Use this when adding a new feature requires modifying more than one unrelated module (e.g., changing a UI button also requires a database schema change).
- Use this when a bug fix causes other unrelated problems to appear elsewhere in the system.
- Use this when writing a unit test requires importing or instantiating a large portion of the rest of the system just to compile.
- Use this when integrating a third-party library that forces callers to handle implementation-specific concerns (e.g., network location, transaction boundaries) throughout the codebase.
- Use this when designing a new module and deciding what state it should own versus receive as parameters.
- Use this when a system needs to support a new interface (e.g., voice response added alongside GUI) and you want to avoid rewriting business logic.
- Use this when refactoring code that has grown complex and where every change seems to require compensating changes elsewhere.
- Use this when evaluating whether a singleton or shared object is appropriate for passing shared state between components.

## Concrete Examples

- Helicopter controls: lowering the collective pitch lever causes nose drop and left spiral, requiring simultaneous compensating inputs on stick and pedals — every control has secondary effects, illustrating non-orthogonal system complexity.
- Heating plant monitoring system: an orthogonal design allows adding voice/touchtone control alongside a GUI by changing only the UI modules, leaving plant-control logic untouched.
- RMI vs CORBA for distributed Java: RMI forces every caller to handle RemoteException (location-aware), violating orthogonality; CORBA hides location from calling code, preserving it.
- EJB transaction metadata: transaction boundaries declared as metadata outside application code, allowing the same code to run in different transaction environments — an orthogonal design for cross-cutting concerns.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Orthogonality**

An LLM coding agent is especially prone to orthogonality violations because it generates code by pattern-matching across the entire visible context, making it natural to reach for global state, copy logic across functions, or wire components together directly rather than through clean interfaces. Unlike a human who feels the pain of tangled code over time, an agent has no such feedback loop — it will confidently produce a deeply coupled system in one pass without noticing the helicopter problem it just created. Applying orthogonality explicitly as a generation constraint (e.g., 'each function may only access state passed to it as arguments'; 'no module may import more than one layer below it') forces the agent to produce components that are testable and changeable in isolation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
