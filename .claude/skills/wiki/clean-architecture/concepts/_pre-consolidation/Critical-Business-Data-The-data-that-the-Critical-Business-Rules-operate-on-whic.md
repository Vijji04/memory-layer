---
title: Critical Business Data: The data that the Critical Business Rules operate on, which would exist even without an automated system
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-20-Business-Rules.json]
contributing_chapters: ["Chapter 20: Business Rules"]
confidence: high
---

# Critical Business Data: The data that the Critical Business Rules operate on, which would exist even without an automated system

> From chapter: *Chapter 20: Business Rules*

## Core Principle

Business rules divide into Critical Business Rules (Entities — pure domain logic independent of automation) and application-specific rules (Use Cases — orchestration logic that controls Entities). Entities are the highest-level, most reusable artifacts and must have zero knowledge of use cases, UI, or databases; use cases sit below them and communicate only through dependency-free request/response data structures. The entire architecture exists to keep business logic pristine and independently deployable, treating everything else as a pluggable detail.

## Key Heuristics

These are the load-bearing rules for this concept.

> Business rules are rules or procedures that make or save the business money, irrespective of whether they were implemented on a computer.

> The Entity is pure business and nothing else.

> Use cases contain the rules that specify how and when the Critical Business Rules within the Entities are invoked. Use cases control the dance of the Entities.

> Entities have no knowledge of the use cases that control them.

> Use cases depend on Entities; Entities do not depend on use cases.

> The business rules should remain pristine, unsullied by baser concerns such as the user interface or database used.

> The business rules should be the most independent and reusable code in the system.

> If the request and response models are not independent, then the use cases that depend on them will be indirectly bound to whatever dependencies the models carry with them.

## Anti-Patterns & Fixes

- Entity-UI Coupling: Embedding UI, database, or framework logic inside an Entity object, contaminating core business logic with delivery-mechanism concerns. Fix: Keep Entities strictly limited to Critical Business Rules and Critical Business Data, with zero imports or references to frameworks, HTTP, or SQL.
- Entity-as-RequestModel Reuse: Passing Entity objects directly as request/response data structures to avoid duplication. Fix: Create separate plain data structures for input/output; Entities and request/response models change for different reasons and must remain independent.
- Use Case UI Awareness: Designing use cases that encode knowledge of the user interface, web layer, or presentation format. Fix: Use cases should only specify data in and data out, with no reference to how it is displayed or transported.
- Upward Entity Dependency: Having Entities know about the use cases that invoke them, violating the Dependency Inversion Principle. Fix: Dependency must flow one way — use cases depend on Entities, never the reverse.
- Framework-Coupled Request Models: Deriving request/response data structures from framework interfaces such as HttpRequest or HttpResponse. Fix: Use plain data structures with no framework inheritance or imports, so use cases remain independently deployable.

## When To Apply

Load this page when:

- Use this when designing a new domain object to determine whether it should be an Entity (Critical Business Rules + data) or a Use Case (application-specific orchestration logic).
- Use this when a use case class starts importing HTTP, SQL, or UI framework types — that is the trigger to extract a clean request/response model.
- Use this when deciding the dependency direction between domain objects and application-layer orchestrators — Entities must never import use case modules.
- Use this when tempted to reuse an Entity object as the input or output DTO of a use case, to recognize that the two will diverge over time.
- Use this when scoping what belongs in the 'core' of the system versus what belongs in 'plugins' (UI, DB, frameworks) during architectural layering.
- Use this when a business rule change should not require modifying delivery infrastructure, confirming that the rule lives in an Entity or Use Case, not in a controller or presenter.
- Use this when evaluating whether a rule is truly a Critical Business Rule (exists without automation) versus an application-specific rule (only makes sense in the automated system).

## Concrete Examples

- Loan entity: a bank charging N% interest is a Critical Business Rule that exists whether calculated by a computer or an abacus; the Loan entity encapsulates loan balance, interest rate, and payment schedule with methods like makePayment(), applyInterest(), and chargeLateFee().
- Bank loan application use case: a use case enforcing that loan officers cannot access the payment estimation screen until contact information is validated and credit score is confirmed above 500 — a rule that only makes sense in the automated system.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 20: Business Rules**

An LLM agent is prone to collapsing architectural layers when generating code — it will naturally inline database queries, HTTP parsing, or ORM models directly into business rule classes because training data frequently shows this pattern in tutorials and small projects. This framework prevents that by giving the agent explicit named boundaries (Entity, Use Case, Request/Response Model) and a strict dependency rule (use cases depend on Entities, never the reverse) to check generated code against. The agent failure mode this most directly prevents is generating 'god service' classes that mix SQL, HTTP response shaping, and core business logic, which appears locally convenient but destroys the testability and portability of the business rules.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
