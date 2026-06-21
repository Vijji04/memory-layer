---
title: Hexagonal Architecture (Ports and Adapters): An architecture by Alistair Cockburn that separates concerns by defining explicit ports for external interaction and adapters that implement them
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-22-The-Clean-Architecture.json]
contributing_chapters: ["Chapter 22: The Clean Architecture"]
confidence: high
---

# Hexagonal Architecture (Ports and Adapters): An architecture by Alistair Cockburn that separates concerns by defining explicit ports for external interaction and adapters that implement them

> From chapter: *Chapter 22: The Clean Architecture*

## Core Principle

The Clean Architecture unifies Hexagonal, DCI, and BCE approaches into a single concentric-layer model governed by one absolute rule: all source code dependencies must point inward toward higher-level policy, never outward. The four canonical layers — Entities, Use Cases, Interface Adapters, and Frameworks/Drivers — are crossed only via simple data structures and Dependency Inversion, ensuring business rules are testable and completely independent of databases, UIs, and frameworks. The payoff is that any external component can be replaced with minimal disruption to the core system.

## Key Heuristics

These are the load-bearing rules for this concept.

> Source code dependencies must point only inward, toward higher-level policies.

> Nothing in an inner circle can know anything at all about something in an outer circle.

> The name of something declared in an outer circle must not be mentioned by the code in an inner circle.

> When we pass data across a boundary, it is always in the form that is most convenient for the inner circle.

> The web is a detail. The database is a detail. We keep these things on the outside where they can do little harm.

> The innermost circle is the most general and highest level.

> By separating the software into layers and conforming to the Dependency Rule, you will create a system that is intrinsically testable.

## Anti-Patterns & Fixes

- Passing Row Structures Inward: Returning a database framework's native row/result object and passing it into inner layers, which forces inner circles to know about outer-circle data formats. Fix: Convert database results into simple, self-contained data structures before crossing the boundary inward.
- Direct Use Case to Presenter Call: A use case directly calling a presenter by name, which names an outer-circle entity inside an inner circle, violating the Dependency Rule. Fix: Define a 'use case output port' interface in the inner circle and have the presenter implement it via Dependency Inversion.
- Framework-Coupled Business Rules: Embedding business logic inside framework constructs (e.g., Rails models, Spring beans) so that entities cannot exist without the framework. Fix: Keep entities as plain objects with no framework imports; treat frameworks as tools in the outermost layer only.
- SQL Leaking Into Use Cases: Writing SQL queries or importing database libraries in the use case or entity layers. Fix: Restrict all SQL and persistence code to the Interface Adapters layer behind a DataAccessInterface abstraction.
- Passing Entity Objects Across Boundaries: Sending full Entity objects across architectural boundaries, coupling outer layers to inner-layer structures. Fix: Construct simple data transfer objects or plain structs containing only the data needed by the receiving layer.

## When To Apply

Load this page when:

- Use this when designing a new system and deciding how to organize code into packages, modules, or services so that business logic is not coupled to a framework.
- Use this when a use case needs to trigger a presenter or view update without the use case layer naming or importing any UI class.
- Use this when swapping a database engine (e.g., SQL to MongoDB) and needing to ensure business rules require zero changes.
- Use this when writing unit tests for business logic and needing to isolate rules from web servers, databases, and external APIs.
- Use this when a framework upgrade is breaking business logic, indicating that business rules were improperly coupled to framework internals.
- Use this when determining where in the codebase to place MVC components, SQL queries, or external API adapters.
- Use this when deciding what data shape to pass between a controller, a use case interactor, and a presenter in a web application.
- Use this when an external service or library becomes obsolete and you need to replace it with minimal impact on the rest of the system.

## Concrete Examples

- A web-based Java system where the Controller packages input into a plain Java object, passes it through InputBoundary to UseCaseInteractor, which calls DataAccessInterface and Entities, then passes OutputData through OutputBoundary to the Presenter, which builds a ViewModel of Strings and flags for the View.
- A use case that needs to call a presenter uses a 'use case output port' interface declared in the inner circle, with the outer-circle Presenter implementing that interface, so the dependency points inward despite the flow of control pointing outward.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 22: The Clean Architecture**

An LLM coding agent is highly prone to violating the Dependency Rule because it generates code by pattern-matching common framework idioms, which typically embed database models, ORM rows, or framework annotations directly into business logic. Without explicit architectural constraints, an agent will naturally produce the shortest path — e.g., passing a Django ORM object straight into a use case function — creating hidden coupling that is invisible in a single generation pass but catastrophic at replacement time. Agents should be instructed to define boundary interfaces and DTOs explicitly before generating any cross-layer calls, treating the Dependency Rule as a hard lint constraint rather than a stylistic preference.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
