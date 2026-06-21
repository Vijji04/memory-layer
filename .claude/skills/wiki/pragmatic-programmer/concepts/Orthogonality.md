---
title: Orthogonality
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 4 pages
---

# Orthogonality

> Consolidated from 4 related concept pages.

---

## CohesionSingle Responsibility Components should be self contained with a single

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

---

## Layered Architecture Each layer uses only abstractions from layers below it enab

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

---

## Orthogonality Principle Changes in one component should not affect any other unr

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

---

## Orthogonality Trigger Non orthogonal design discovered in code signals that refa

## Core Principle

Refactoring is the continuous, disciplined process of reworking code structure as understanding evolves, using the gardening metaphor rather than construction to frame software as organic and always in need of tending. The core discipline requires separating refactoring from feature work, maintaining comprehensive tests, and taking small verifiable steps to avoid net harm. Deferring refactoring is a false economy—dependency accumulation makes later changes exponentially more costly, so the pragmatic rule is to refactor early and often.

## Key Heuristics

These are the load-bearing rules for this concept.

> Refactor Early, Refactor Often

> Don't try to refactor and add functionality at the same time.

> Make sure you have good tests before you begin refactoring. Run the tests as often as possible.

> Take short, deliberate steps... If you keep your steps small, and test after each step, you will avoid prolonged debugging.

> fail to refactor now, and there'll be a far greater time investment to fix the problem down the road—when there are more dependencies to reckon with.

> Don't live with broken windows.

> If it hurts now, but is going to hurt even more later, you might as well get it over with.

## Anti-Patterns & Fixes

- Deferring Refactoring Under Time Pressure: Developers skip refactoring citing deadlines, but this causes dependencies to grow around the problematic code, making future refactoring exponentially more expensive and dangerous. Fix: Schedule refactoring explicitly; treat deferred refactoring as a tracked debt with stakeholder visibility.
- Refactoring and Adding Features Simultaneously: Mixing new functionality with structural changes makes it impossible to isolate the source of bugs or regressions. Fix: Complete refactoring as a separate, isolated commit or phase before adding new behavior.
- Large-Scale Reckless Reworking: Ripping up vast quantities of code with wild abandon risks leaving the codebase in a worse state than before. Fix: Make many small, localized changes that collectively achieve the larger-scale structural improvement, testing after each step.
- Construction Metaphor Thinking: Treating software as a finished artifact after initial build, calling only for maintenance fixes. Fix: Adopt the gardening metaphor—continuously monitor, prune, split, and reorganize code as understanding evolves.
- Silent Refactoring of Shared Interfaces: Changing a module's interface or functionality without signaling breakage to dependent code. Fix: Ensure drastic interface changes break the build so old clients are immediately identified and updated.

## When To Apply

Load this page when:

- Use this when you discover duplicated logic or copy-pasted code blocks that violate the DRY principle.
- Use this when a routine has grown too large or is attempting to accomplish more than one coherent responsibility.
- Use this when requirements have drifted and existing code encodes outdated assumptions about the domain.
- Use this when two separate implementations of similar behavior could be merged into a common abstraction.
- Use this when a design smells non-orthogonal—changes in one module ripple unexpectedly into unrelated modules.
- Use this when performance analysis reveals that functionality must be relocated within the system architecture.
- Use this when a code section feels 'wrong' or produces friction every time it is read or modified.
- Use this when adding a new feature reveals that the existing structure makes the addition unnecessarily complex or duplicative.

## Concrete Examples

- State-based tax calculation code (Texas/Ohio/Maine) with repeated calc formula and mixed rate logic—used as an exercise to demonstrate structural refactoring need.
- Java Shape class with integer constants for SQUARE, CIRCLE, RIGHT_TRIANGLE that needs restructuring before adding more shape types—demonstrates refactoring for extensibility.
- Medical analogy: a code 'growth' that is cheap to remove while small but increasingly dangerous and expensive to remove as it spreads, used to justify early refactoring to management.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**33. Refactoring**

An LLM coding agent is particularly prone to the 'construction metaphor' failure mode: it generates code in a single pass optimized for the immediate prompt, treating the output as a finished artifact rather than a first draft requiring future tending. This means agents will silently propagate duplication and non-orthogonal design across files because they lack continuous awareness of the evolving codebase state. Agents should be explicitly triggered to run a refactoring pass before and after feature additions, treating refactoring as a mandatory, test-gated phase rather than an optional cleanup step.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
