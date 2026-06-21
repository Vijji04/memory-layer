---
title: CCP (Common Closure Principle): Classes that change for the same reasons and at the same times belong in the same component; classes that change for different reasons belong in different components
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-13-Component-Cohesion.json]
contributing_chapters: ["Chapter 13: Component Cohesion"]
confidence: high
---

# Common Closure Principle

## CCP Common Closure

# CCP (Common Closure Principle): Classes that change for the same reasons and at the same times belong in the same component; classes that change for different reasons belong in different components

> From chapter: *Chapter 13: Component Cohesion*

## Core Principle

Component cohesion is governed by three competing principles: REP (classes must share a releasable theme), CCP (classes that change together stay together, analogous to SRP at the component level), and CRP (classes not jointly reused must not share a component, analogous to ISP at the component level). REP and CCP push components to be larger and more change-stable; CRP pushes them to be smaller and reuse-clean, creating an inherent tension that architects must balance based on project maturity. Early projects should favor CCP for develop-ability; mature projects consumed by others should shift toward CRP for clean reuse boundaries.

## Key Heuristics

These are the load-bearing rules for this concept.

> The granule of reuse is the granule of release.

> Gather into components those classes that change for the same reasons and at the same times. Separate into different components those classes that change at different times and for different reasons.

> Don't force users of a component to depend on things they don't need.

> Gather together those things that change at the same times and for the same reasons. Separate those things that change at different times or for different reasons.

> Don't depend on things you don't need.

> When we depend on a component, we want to make sure we depend on every class in that component.

> Early in the development of a project, the CCP is much more important than the REP, because develop-ability is more important than reuse.

## Anti-Patterns & Fixes

- RandomHodgepodgeComponent: Grouping unrelated classes into a component with no overarching theme or shared purpose, making it impossible to reason about what belongs together. Fix: Apply REP — ensure all classes in a component share a cohesive purpose and can be meaningfully released together.
- ChangeScatter: Spreading classes that always change together across multiple components, forcing multi-component redeployment for every requirement change. Fix: Apply CCP — co-locate classes that change for the same reasons into the same component.
- OverbloatedComponent: Combining classes that are not tightly coupled into one component, forcing consumers to depend on and redeploy classes they never use. Fix: Apply CRP — split components so that all classes within a component are inseparable and jointly needed by consumers.
- PrematureReusability: Optimizing component structure for reuse too early in a project, before usage patterns are known, at the cost of develop-ability. Fix: Start on the CCP/REP side of the tension triangle and migrate toward CRP as the project matures and external consumers emerge.
- StaticComponentStructure: Treating component boundaries as permanent architectural decisions rather than evolving them as project maturity and usage patterns change. Fix: Periodically re-evaluate component composition as the project shifts focus from develop-ability to reusability.

## When To Apply

Load this page when:

- Use this when deciding which classes or modules to place into a shared library or package during initial project structuring.
- Use this when a single requirement change causes modifications across many components, signaling a CCP violation.
- Use this when a consumer of a component only uses one class but is forced to import, compile, or redeploy the entire component.
- Use this when versioning or releasing a component and needing to decide whether two classes should share the same release cycle.
- Use this when splitting a monolith into components or microservices and determining the correct boundaries for each unit.
- Use this when a component's changelog contains changes unrelated to each other, suggesting it has multiple unrelated reasons to change.
- Use this when designing a reusable library that will be consumed by multiple downstream projects with different needs.
- Use this when evaluating whether a container class and its iterator (or similar tightly coupled abstractions) should be co-located in the same module.

## Concrete Examples

- A container class and its associated iterators are given as an example of classes that are always reused together and therefore belong in the same component under CRP.
- Maven, Leiningen, and RVM are cited as module management tools that embody the REP by providing release tracking, versioning, and release documentation for reusable components.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 13: Component Cohesion**

An LLM coding agent is prone to grouping classes by superficial similarity (e.g., same domain noun, same file type) rather than by change frequency or reuse coupling, producing components that violate CCP and CRP simultaneously — classes that change independently end up together, and classes that are reused together end up apart. Unlike a human who gets feedback from painful multi-component deploys over time, an agent generating code in a single pass has no deployment pain signal, making it critical to explicitly prompt the agent with REP/CCP/CRP rules when generating module or package boundaries. The tension triangle is especially important for agents: without knowing project maturity, an agent will default to premature reusability optimization, producing over-split components that increase coupling overhead instead of reducing it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Common Closure Principle

# Common Closure Principle: The component-level analog of SRP — components should be closed to changes from the same set of actors

> From chapter: *Chapter 7: SRP: The Single Responsibility Principle*

## Core Principle

SRP is not about functions doing one thing — it is about modules being owned by exactly one actor (stakeholder group), so that change requests from different parts of the organization cannot silently interfere with each other. Its two primary failure modes are accidental duplication (shared helpers modified for one actor break another) and merge collisions (different teams editing the same file). The fix in both cases is to separate code by actor, using plain data structures and the Facade pattern to manage the resulting class proliferation.

## Key Heuristics

These are the load-bearing rules for this concept.

> A module should be responsible to one, and only one, actor.

> A module should have one, and only one, reason to change.

> Cohesion is the force that binds together the code responsible to a single actor.

> Separate the code that different actors depend on.

> A function should do one, and only one, thing — but this is not the SRP.

> The SRP says to separate the code that different actors depend on.

## Anti-Patterns & Fixes

- Accidental Duplication via Shared Algorithm: Two methods serving different actors share a private helper (e.g., regularHours()). A change requested by one actor silently corrupts the behavior relied on by another. Fix: Separate methods serving different actors into distinct classes so shared helpers cannot be inadvertently modified across actor boundaries.
- Multi-Actor Merge Collisions: Multiple developers from different teams modify the same source file for unrelated actor-driven reasons, causing merge conflicts that risk cross-actor breakage. Fix: Split the class by actor so each team owns a separate file with no overlap.
- God Class with Mixed Responsibilities: A single class (e.g., Employee) hosts calculatePay(), reportHours(), and save(), coupling CFO, COO, and CTO concerns. Fix: Extract each actor's methods into its own class sharing a plain data structure (e.g., EmployeeData) with no behavior.
- Naming Confusion of SRP: Interpreting SRP as 'do only one thing' leads to over-decomposition at the function level while missing actor-level coupling. Fix: Always identify the actor (stakeholder group) when evaluating whether a module violates SRP.

## When To Apply

Load this page when:

- Use this when designing a class whose methods will be modified by requests from different business departments or stakeholders.
- Use this when a shared private helper function is called by two methods that serve different business purposes or reporting lines.
- Use this when multiple developers on different teams are likely to concurrently modify the same source file.
- Use this when a bug report reveals that a change requested by one team unexpectedly broke functionality used by a different team.
- Use this when deciding whether to consolidate related-seeming operations (e.g., calculate, report, persist) into one class.
- Use this when refactoring a large class to determine the correct split boundaries — split by actor, not by function type.
- Use this when evaluating merge conflict frequency in a file as a proxy signal for SRP violation.

## Concrete Examples

- Employee class in a payroll application with calculatePay() (CFO/accounting), reportHours() (COO/HR), and save() (CTO/DBAs) — three methods serving three distinct actors in a single class.
- regularHours() shared helper called by both calculatePay() and reportHours(); a CFO-requested tweak to regularHours() silently corrupts HR reports, costing the COO's budget millions.
- EmployeeData plain data structure shared by three separate classes (PayCalculator, HourReporter, EmployeeSaver), each serving one actor with no knowledge of the others.
- EmployeeFacade pattern delegating to PayCalculator, HourReporter, and EmployeeSaver to reduce instantiation complexity while preserving actor separation.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: SRP: The Single Responsibility Principle**

An LLM coding agent is prone to SRP violations because it optimizes for local coherence — grouping methods that seem semantically related (all about 'employees') without modeling the organizational boundaries that determine true actor alignment. When asked to add a feature, an agent will naturally inject new methods into the most relevant existing class, silently coupling new actors to old ones and creating accidental-duplication traps that no test will catch until runtime. Applying SRP explicitly requires the agent to ask 'which actor drives this change?' before placing any method, and to prefer creating a new class over extending an existing one when actors differ.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

