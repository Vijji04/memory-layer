---
title: Open-Closed Principle (OCP): A software artifact should be open for extension but closed for modification — behavior should be extendible without altering the artifact itself
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-8-OCP-The-Open-Closed-Principle.json]
contributing_chapters: ["Chapter 8: OCP: The Open-Closed Principle"]
confidence: high
---

# Open-Closed Principle (OCP): A software artifact should be open for extension but closed for modification — behavior should be extendible without altering the artifact itself

> From chapter: *Chapter 8: OCP: The Open-Closed Principle*

## Core Principle

The Open-Closed Principle states that software components should be extendible without being modified, achieved architecturally by separating responsibilities (SRP) and arranging components in a unidirectional dependency hierarchy where lower-level components depend on higher-level ones. Business rules (Interactors) sit at the top of this hierarchy and are maximally protected; UI and database concerns sit at the bottom and absorb change. Interfaces are used both to invert dependency direction and to hide internals, preventing transitive coupling from undermining the protection hierarchy.

## Key Heuristics

These are the load-bearing rules for this concept.

> A software artifact should be open for extension but closed for modification.

> If simple extensions to the requirements force massive changes to the software, then the architects of that software system have engaged in a spectacular failure.

> If component A should be protected from changes in component B, then component B should depend on component A.

> Higher-level components in that hierarchy are protected from the changes made to lower-level components.

> The goal is to make the system easy to extend without incurring a high impact of change.

> Software entities should not depend on things they don't directly use.

> Architects separate functionality based on how, why, and when it changes, and then organize that separated functionality into a hierarchy of components.

## Anti-Patterns & Fixes

- Bidirectional Dependencies: Components depend on each other in both directions, making it impossible to change one without affecting the other. Fix: Ensure all component relationships are unidirectional, with arrows pointing toward the components you want to protect.
- Monolithic Report Generator: Mixing data calculation and data presentation in a single component so that changing output format requires modifying business logic. Fix: Apply SRP to separate reporting responsibilities into distinct components (data computation vs. presentation).
- Transitive Dependency Leakage: A controller or high-level component gains indirect knowledge of low-level internals through a chain of dependencies, coupling it to changes it should not care about. Fix: Introduce interface boundaries (e.g., FinancialReportRequester) to hide internals and break transitive chains.
- Flat Component Architecture: All components exist at the same level with no protection hierarchy, so any requirement change can ripple everywhere. Fix: Partition components into a dependency hierarchy ordered by conceptual level, with business rules at the top.

## When To Apply

Load this page when:

- Use this when adding a new output format (e.g., PDF, CSV, print report) to an existing system and you need to avoid modifying the core business logic.
- Use this when a stakeholder requirement change in a UI or database layer is cascading into changes in business rule classes.
- Use this when designing the dependency graph between architectural components and deciding which direction interfaces should point.
- Use this when a new feature can be implemented by adding new classes/modules rather than editing existing ones — confirm the architecture allows this before proceeding.
- Use this when you notice a high-level policy class importing or referencing low-level implementation details directly.
- Use this when two components need to communicate but you want to prevent one from knowing about the internals of the other.
- Use this when evaluating whether a proposed architecture change requires modifying stable, heavily-depended-upon components.

## Concrete Examples

- Financial summary displayed on a web page (scrollable, red negatives) extended to a black-and-white printed report (paginated, parenthesized negatives) — used to illustrate how OCP-compliant architecture achieves zero changes to existing code.
- Component diagram with Controller, Interactor, Database, Presenters, and Views — showing unidirectional dependencies that protect the Interactor (business rules) from all changes in peripheral components.
- FinancialDataGateway interface inverting the dependency between the Interactor component and the Database component — illustrating directional control via interface insertion.
- FinancialReportRequester interface protecting the FinancialReportController from transitive dependencies on FinancialEntities inside the Interactor.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 8: OCP: The Open-Closed Principle**

An LLM coding agent, when asked to add a feature, will default to the path of least resistance — directly modifying existing classes rather than extending through interfaces or new components, violating OCP at every iteration. Because agents generate code in response to prompts without a persistent architectural model, they are especially prone to creating bidirectional dependencies and leaking internals across component boundaries, since each code generation call lacks awareness of the protection hierarchy. Applying OCP explicitly in agent instructions — specifying which components are closed for modification and requiring new behavior to be added only via extension points — prevents the agent from accreting coupling silently across generations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
