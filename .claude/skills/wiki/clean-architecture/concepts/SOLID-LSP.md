---
title: Configuration-Driven Dispatch: When implementations are not substitutable, isolate the variation into a configuration database keyed by identifier rather than embedding conditionals in business logic
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-9-LSP-The-Liskov-Substitution-Principle.json]
contributing_chapters: ["Chapter 9: LSP: The Liskov Substitution Principle"]
confidence: high
---

# SOLID LSP

## Configuration Driven Dispatch

# Configuration-Driven Dispatch: When implementations are not substitutable, isolate the variation into a configuration database keyed by identifier rather than embedding conditionals in business logic

> From chapter: *Chapter 9: LSP: The Liskov Substitution Principle*

## Core Principle

LSP states that subtypes must be fully substitutable for their base types without altering program correctness; violations force callers to perform type-aware branching, polluting the architecture. The principle extends beyond class inheritance to any interface contract — REST APIs, duck-typed services, and plugins — where non-substitutable implementations must be isolated via configuration or adapters rather than inline conditionals. Architectural cleanliness therefore depends on enforcing substitutability at every abstraction boundary, not just in object hierarchies.

## Key Heuristics

These are the load-bearing rules for this concept.

> If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T.

> The only way to defend against this kind of LSP violation is to add mechanisms to the User (such as an if statement) that detects whether the Rectangle is, in fact, a Square.

> Since the behavior of the User depends on the types it uses, those types are not substitutable.

> A simple violation of substitutability can cause a system's architecture to be polluted with a significant amount of extra mechanisms.

> No architect worth his or her salt would allow such a construction to exist in the system — putting a vendor name into the code itself creates an opportunity for all kinds of horrible and mysterious errors, not to mention security breaches.

> The LSP can, and should, be extended to the level of architecture.

## Anti-Patterns & Fixes

- Square-as-Rectangle Subtype: Making Square extend Rectangle violates LSP because Square's setW/setH are not independently mutable, breaking caller assumptions. Fix: Do not subtype when the subtype cannot honor all behavioral contracts of the parent; prefer composition or a common abstract base that does not promise independent mutability.
- Hardcoded Vendor Conditionals: Adding `if (driver.getDispatchUri().startsWith('acme.com'))` to handle a non-conforming REST interface embeds brittle, security-risky special cases in business logic. Fix: Externalize variation into a configuration database keyed by URI, mapping each provider to its dispatch format.
- Interface Contract Drift: Allowing one implementation (e.g., Acme's `dest` vs `destination`) to silently deviate from the agreed REST interface. Fix: Enforce the interface contract at the boundary; treat any deviation as requiring an adapter or configuration entry, never an inline conditional.
- Type-Checking Callers: Callers that must inspect the runtime type of an object to decide how to behave signal an LSP violation. Fix: Push behavioral differences into the subtypes themselves, restoring substitutability.

## When To Apply

Load this page when:

- Use this when designing a class hierarchy where a subclass overrides methods in ways that could surprise callers expecting parent-class behavior.
- Use this when multiple service implementations (e.g., REST APIs from different vendors) must be called through a shared interface and one implementation uses different field names or semantics.
- Use this when a caller contains an if/switch statement that branches on the concrete type or URI of an object it received through an abstraction.
- Use this when generating a plugin or adapter system where new implementations will be dropped in and must be interchangeable with existing ones.
- Use this when a subclass cannot fully satisfy all postconditions or invariants of the parent class (e.g., a read-only collection subtyping a mutable one).
- Use this when reviewing whether a proposed inheritance relationship is geometrically or conceptually true but behaviorally incompatible.
- Use this when adding a new taxi/payment/auth provider to an aggregator and deciding whether to add a special case or a config entry.

## Concrete Examples

- License hierarchy: PersonalLicense and BusinessLicense both subtype License with calcFee(); Billing application works identically with either — a conforming LSP example.
- Square/Rectangle problem: Square extends Rectangle but cannot independently mutate width and height, causing `r.setW(5); r.setH(2); assert(r.area()==10)` to fail when r is actually a Square.
- Taxi aggregator REST violation: Acme taxi abbreviates `destination` to `dest` in their dispatch URI, forcing either a hardcoded `if (acme.com)` branch or a configuration-database solution mapping URIs to dispatch format templates.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 9: LSP: The Liskov Substitution Principle**

An LLM coding agent is especially prone to LSP violations because it pattern-matches geometric or semantic relationships ('a Square IS-A Rectangle') and generates inheritance hierarchies that feel natural but break behavioral contracts — it will not automatically verify that all parent-class invariants hold in the subclass. When generating multi-provider integrations (APIs, plugins, adapters), an agent may silently emit provider-specific conditionals inline rather than recognizing them as LSP violations demanding a configuration or strategy pattern. Applying LSP checks as a post-generation lint step — flagging any caller that inspects concrete types or any subclass that weakens parent postconditions — prevents the agent from producing architectures that accumulate special-case debt.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Liskov Substitution Principle

# Liskov Substitution Principle (LSP): If S is a subtype of T, then objects of type S must be substitutable for objects of type T without altering the correctness of the program

> From chapter: *Chapter 9: LSP: The Liskov Substitution Principle*

## Core Principle

LSP states that subtypes must be fully substitutable for their base types without altering program correctness; violations force callers to perform type-aware branching, polluting the architecture. The principle extends beyond class inheritance to any interface contract — REST APIs, duck-typed services, and plugins — where non-substitutable implementations must be isolated via configuration or adapters rather than inline conditionals. Architectural cleanliness therefore depends on enforcing substitutability at every abstraction boundary, not just in object hierarchies.

## Key Heuristics

These are the load-bearing rules for this concept.

> If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T.

> The only way to defend against this kind of LSP violation is to add mechanisms to the User (such as an if statement) that detects whether the Rectangle is, in fact, a Square.

> Since the behavior of the User depends on the types it uses, those types are not substitutable.

> A simple violation of substitutability can cause a system's architecture to be polluted with a significant amount of extra mechanisms.

> No architect worth his or her salt would allow such a construction to exist in the system — putting a vendor name into the code itself creates an opportunity for all kinds of horrible and mysterious errors, not to mention security breaches.

> The LSP can, and should, be extended to the level of architecture.

## Anti-Patterns & Fixes

- Square-as-Rectangle Subtype: Making Square extend Rectangle violates LSP because Square's setW/setH are not independently mutable, breaking caller assumptions. Fix: Do not subtype when the subtype cannot honor all behavioral contracts of the parent; prefer composition or a common abstract base that does not promise independent mutability.
- Hardcoded Vendor Conditionals: Adding `if (driver.getDispatchUri().startsWith('acme.com'))` to handle a non-conforming REST interface embeds brittle, security-risky special cases in business logic. Fix: Externalize variation into a configuration database keyed by URI, mapping each provider to its dispatch format.
- Interface Contract Drift: Allowing one implementation (e.g., Acme's `dest` vs `destination`) to silently deviate from the agreed REST interface. Fix: Enforce the interface contract at the boundary; treat any deviation as requiring an adapter or configuration entry, never an inline conditional.
- Type-Checking Callers: Callers that must inspect the runtime type of an object to decide how to behave signal an LSP violation. Fix: Push behavioral differences into the subtypes themselves, restoring substitutability.

## When To Apply

Load this page when:

- Use this when designing a class hierarchy where a subclass overrides methods in ways that could surprise callers expecting parent-class behavior.
- Use this when multiple service implementations (e.g., REST APIs from different vendors) must be called through a shared interface and one implementation uses different field names or semantics.
- Use this when a caller contains an if/switch statement that branches on the concrete type or URI of an object it received through an abstraction.
- Use this when generating a plugin or adapter system where new implementations will be dropped in and must be interchangeable with existing ones.
- Use this when a subclass cannot fully satisfy all postconditions or invariants of the parent class (e.g., a read-only collection subtyping a mutable one).
- Use this when reviewing whether a proposed inheritance relationship is geometrically or conceptually true but behaviorally incompatible.
- Use this when adding a new taxi/payment/auth provider to an aggregator and deciding whether to add a special case or a config entry.

## Concrete Examples

- License hierarchy: PersonalLicense and BusinessLicense both subtype License with calcFee(); Billing application works identically with either — a conforming LSP example.
- Square/Rectangle problem: Square extends Rectangle but cannot independently mutate width and height, causing `r.setW(5); r.setH(2); assert(r.area()==10)` to fail when r is actually a Square.
- Taxi aggregator REST violation: Acme taxi abbreviates `destination` to `dest` in their dispatch URI, forcing either a hardcoded `if (acme.com)` branch or a configuration-database solution mapping URIs to dispatch format templates.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 9: LSP: The Liskov Substitution Principle**

An LLM coding agent is especially prone to LSP violations because it pattern-matches geometric or semantic relationships ('a Square IS-A Rectangle') and generates inheritance hierarchies that feel natural but break behavioral contracts — it will not automatically verify that all parent-class invariants hold in the subclass. When generating multi-provider integrations (APIs, plugins, adapters), an agent may silently emit provider-specific conditionals inline rather than recognizing them as LSP violations demanding a configuration or strategy pattern. Applying LSP checks as a post-generation lint step — flagging any caller that inspects concrete types or any subclass that weakens parent postconditions — prevents the agent from producing architectures that accumulate special-case debt.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Substitutability as Architecture

# Substitutability as Architecture Constraint: LSP extends beyond inheritance to any interface/implementation contract — REST services, duck-typed classes, and plugins must all honor substitutability or force polluting special-case logic into the system

> From chapter: *Chapter 9: LSP: The Liskov Substitution Principle*

## Core Principle

LSP states that subtypes must be fully substitutable for their base types without altering program correctness; violations force callers to perform type-aware branching, polluting the architecture. The principle extends beyond class inheritance to any interface contract — REST APIs, duck-typed services, and plugins — where non-substitutable implementations must be isolated via configuration or adapters rather than inline conditionals. Architectural cleanliness therefore depends on enforcing substitutability at every abstraction boundary, not just in object hierarchies.

## Key Heuristics

These are the load-bearing rules for this concept.

> If for each object o1 of type S there is an object o2 of type T such that for all programs P defined in terms of T, the behavior of P is unchanged when o1 is substituted for o2 then S is a subtype of T.

> The only way to defend against this kind of LSP violation is to add mechanisms to the User (such as an if statement) that detects whether the Rectangle is, in fact, a Square.

> Since the behavior of the User depends on the types it uses, those types are not substitutable.

> A simple violation of substitutability can cause a system's architecture to be polluted with a significant amount of extra mechanisms.

> No architect worth his or her salt would allow such a construction to exist in the system — putting a vendor name into the code itself creates an opportunity for all kinds of horrible and mysterious errors, not to mention security breaches.

> The LSP can, and should, be extended to the level of architecture.

## Anti-Patterns & Fixes

- Square-as-Rectangle Subtype: Making Square extend Rectangle violates LSP because Square's setW/setH are not independently mutable, breaking caller assumptions. Fix: Do not subtype when the subtype cannot honor all behavioral contracts of the parent; prefer composition or a common abstract base that does not promise independent mutability.
- Hardcoded Vendor Conditionals: Adding `if (driver.getDispatchUri().startsWith('acme.com'))` to handle a non-conforming REST interface embeds brittle, security-risky special cases in business logic. Fix: Externalize variation into a configuration database keyed by URI, mapping each provider to its dispatch format.
- Interface Contract Drift: Allowing one implementation (e.g., Acme's `dest` vs `destination`) to silently deviate from the agreed REST interface. Fix: Enforce the interface contract at the boundary; treat any deviation as requiring an adapter or configuration entry, never an inline conditional.
- Type-Checking Callers: Callers that must inspect the runtime type of an object to decide how to behave signal an LSP violation. Fix: Push behavioral differences into the subtypes themselves, restoring substitutability.

## When To Apply

Load this page when:

- Use this when designing a class hierarchy where a subclass overrides methods in ways that could surprise callers expecting parent-class behavior.
- Use this when multiple service implementations (e.g., REST APIs from different vendors) must be called through a shared interface and one implementation uses different field names or semantics.
- Use this when a caller contains an if/switch statement that branches on the concrete type or URI of an object it received through an abstraction.
- Use this when generating a plugin or adapter system where new implementations will be dropped in and must be interchangeable with existing ones.
- Use this when a subclass cannot fully satisfy all postconditions or invariants of the parent class (e.g., a read-only collection subtyping a mutable one).
- Use this when reviewing whether a proposed inheritance relationship is geometrically or conceptually true but behaviorally incompatible.
- Use this when adding a new taxi/payment/auth provider to an aggregator and deciding whether to add a special case or a config entry.

## Concrete Examples

- License hierarchy: PersonalLicense and BusinessLicense both subtype License with calcFee(); Billing application works identically with either — a conforming LSP example.
- Square/Rectangle problem: Square extends Rectangle but cannot independently mutate width and height, causing `r.setW(5); r.setH(2); assert(r.area()==10)` to fail when r is actually a Square.
- Taxi aggregator REST violation: Acme taxi abbreviates `destination` to `dest` in their dispatch URI, forcing either a hardcoded `if (acme.com)` branch or a configuration-database solution mapping URIs to dispatch format templates.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 9: LSP: The Liskov Substitution Principle**

An LLM coding agent is especially prone to LSP violations because it pattern-matches geometric or semantic relationships ('a Square IS-A Rectangle') and generates inheritance hierarchies that feel natural but break behavioral contracts — it will not automatically verify that all parent-class invariants hold in the subclass. When generating multi-provider integrations (APIs, plugins, adapters), an agent may silently emit provider-specific conditionals inline rather than recognizing them as LSP violations demanding a configuration or strategy pattern. Applying LSP checks as a post-generation lint step — flagging any caller that inspects concrete types or any subclass that weakens parent postconditions — prevents the agent from producing architectures that accumulate special-case debt.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

