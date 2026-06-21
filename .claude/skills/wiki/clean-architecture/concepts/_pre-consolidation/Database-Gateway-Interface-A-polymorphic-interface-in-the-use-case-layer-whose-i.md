---
title: Database Gateway Interface: A polymorphic interface in the use-case layer whose implementation (SQL/ORM) lives in the database layer as a humble object, enabling interactors to be tested with stubs
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-23-Presenters-and-Humble-Objects.json]
contributing_chapters: ["Chapter 23: Presenters and Humble Objects"]
confidence: high
---

# Database Gateway Interface: A polymorphic interface in the use-case layer whose implementation (SQL/ORM) lives in the database layer as a humble object, enabling interactors to be tested with stubs

> From chapter: *Chapter 23: Presenters and Humble Objects*

## Core Principle

The Humble Object pattern splits any module into a hard-to-test humble shell (View, DB implementation, service listener) and an easy-to-test logic core (Presenter, Interactor, application service), with a plain data structure (View Model, gateway interface, DTO) crossing the boundary between them. This split is not merely a testing convenience — it reliably marks architectural boundaries throughout Clean Architecture, appearing at the UI, database, and service layers. Testability is therefore a structural property of good architecture, not an afterthought.

## Key Heuristics

These are the load-bearing rules for this concept.

> Split the behaviors into two modules or classes. One of those modules is humble; it contains all the hard-to-test behaviors stripped down to their barest essence.

> Testability is an attribute of good architectures.

> The separation of the behaviors into testable and non-testable parts often defines an architectural boundary.

> Nothing is left for the View to do other than to load the data from the View Model into the screen. Thus the View is humble.

> There is no such thing as an object relational mapper (ORM). The reason is simple: Objects are not data structures.

> ORMs would be better named 'data mappers,' because they load data into data structures from relational database tables.

> At each architectural boundary, we are likely to find the Humble Object pattern lurking somewhere nearby.

> The communication across that boundary will almost always involve some kind of simple data structure, and the boundary will frequently divide something that is hard to test from something that is easy to test.

## Anti-Patterns & Fixes

- LogicInTheView: Placing formatting, conditional display logic, or data transformation inside the View/UI layer makes it untestable and entangles presentation with business rules. Fix: Move all formatting and conditional logic into the Presenter, expose only pre-computed strings/booleans/enums in the View Model.
- SQLInUseCases: Writing SQL or direct database calls inside use-case interactors couples business logic to database technology and makes unit testing impossible without a real database. Fix: Define gateway interfaces in the use-case layer and implement them with SQL in the database layer as a humble object.
- CallingORMAnObjectMapper: Treating ORM-loaded entities as true domain objects conflates data structures with behavior-bearing objects, leading to leaky abstractions. Fix: Recognize ORMs as data mappers residing in the database layer, not domain-object factories.
- BusinessLogicInServiceListener: Putting parsing, validation, or transformation logic in the service communication layer mixes infrastructure with application logic and makes it untestable. Fix: Service listeners should only receive external data and reformat it into a plain data structure passed across the boundary; business logic stays in the application layer.

## When To Apply

Load this page when:

- Use this when designing a UI layer and needing to decide where date/currency/color formatting logic should live.
- Use this when a UI component is difficult to unit test and you need to extract testable logic from it.
- Use this when writing use-case interactors that need database access and you want to avoid coupling to SQL or a specific ORM.
- Use this when defining a service integration layer (inbound or outbound) and deciding how to isolate application logic from wire-format concerns.
- Use this when identifying where to place an architectural boundary between two subsystems with different testability characteristics.
- Use this when an ORM or data-access library is being used and you need to decide which layer it belongs to.
- Use this when a module is proving difficult to unit test and you suspect it mixes infrastructure concerns with business logic.

## Concrete Examples

- Presenter receiving a Date object from the application, formatting it into a string, and placing it in the View Model for the View to display without further processing.
- Presenter receiving a Currency object, formatting it with decimal places and currency markers, and setting a boolean flag in the View Model to turn the value red if negative.
- UserGateway interface with a getLastNamesOfUsersWhoLoggedInAfter(Date) method used by interactors, with the SQL implementation living in the humble database layer.
- Service listeners receiving external service data, reformatting it into a simple data structure, and passing it across the service boundary into the application.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 23: Presenters and Humble Objects**

An LLM coding agent, when generating UI or integration code, will naturally inline formatting logic, conditional rendering, and data transformation directly into the output/rendering layer because that is the most locally coherent way to satisfy a prompt — this is precisely the anti-pattern the Humble Object pattern prevents. By explicitly applying this pattern, an agent should generate a Presenter class that owns all logic and a View/Listener stub that contains only mechanical data-binding, making the generated code testable without any UI or network infrastructure. Agents also tend to embed SQL or ORM calls directly inside generated business-logic classes when asked to 'make it work quickly,' so triggering this pattern enforces the gateway interface boundary and prevents untestable interactors.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
