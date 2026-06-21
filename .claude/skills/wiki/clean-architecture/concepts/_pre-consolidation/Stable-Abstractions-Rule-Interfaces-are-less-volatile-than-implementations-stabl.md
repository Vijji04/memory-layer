---
title: Stable Abstractions Rule: Interfaces are less volatile than implementations; stable architectures favor depending on abstract interfaces rather than concrete classes
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-11-DIP-The-Dependency-Inversion-Principle.json]
contributing_chapters: ["Chapter 11: DIP: The Dependency Inversion Principle"]
confidence: high
---

# Stable Abstractions Rule: Interfaces are less volatile than implementations; stable architectures favor depending on abstract interfaces rather than concrete classes

> From chapter: *Chapter 11: DIP: The Dependency Inversion Principle*

## Core Principle

DIP states that high-level modules must not depend on volatile low-level concretions; both should depend on stable abstractions, with all source code dependencies pointing toward interfaces rather than implementations. Object creation of volatile types must be handled via Abstract Factories to prevent concrete constructor calls from polluting the abstract side of an architectural boundary. Unavoidable DIP violations should be quarantined in a single concrete component (typically 'main') so the rest of the system remains insulated from change.

## Key Heuristics

These are the load-bearing rules for this concept.

> The most flexible systems are those in which source code dependencies refer only to abstractions, not to concretions.

> It is the volatile concrete elements of our system that we want to avoid depending on.

> Every change to an abstract interface corresponds to a change to its concrete implementations. Conversely, changes to concrete implementations do not always, or even usually, require changes to the interfaces that they implement.

> Don't refer to volatile concrete classes. Refer to abstract interfaces instead.

> Don't derive from volatile concrete classes.

> Don't override concrete functions. To manage those dependencies, you should make the function abstract and create multiple implementations.

> Never mention the name of anything concrete and volatile.

> DIP violations cannot be entirely removed, but they can be gathered into a small number of concrete components and kept separate from the rest of the system.

## Anti-Patterns & Fixes

- Depending on Volatile Concretions: High-level modules import or instantiate concrete classes that are under active development, causing the high-level policy to break whenever implementation details change. Fix: Depend on stable abstract interfaces instead; use Abstract Factories for object creation.
- Overriding Concrete Functions: Subclassing a concrete class and overriding its methods inherits all of the parent's source code dependencies rather than eliminating them. Fix: Make the function abstract in an interface and provide multiple independent implementations.
- Deriving from Volatile Concrete Classes: Inheriting from a concrete class that changes frequently creates the strongest and most rigid coupling in statically typed languages. Fix: Derive from abstract classes or interfaces; never from volatile concretions.
- Instantiating Concretions Directly in High-Level Modules: Using 'new ConcreteImpl()' inside business logic creates a source code dependency on the concrete definition. Fix: Delegate all instantiation of volatile objects to an Abstract Factory accessed through an interface.
- Scattering DIP Violations Throughout the Codebase: Allowing concrete dependencies to appear anywhere in the system makes volatility uncontrollable. Fix: Concentrate all unavoidable DIP violations in a single concrete component (e.g., 'main') isolated from the rest of the system.

## When To Apply

Load this page when:

- Use this when designing a module that must use a class currently under active development, to avoid being broken by its frequent changes.
- Use this when a high-level business rule component needs to create instances of concrete service objects without importing their concrete definitions.
- Use this when deciding whether to use inheritance—check if the parent class is volatile; if so, depend on an abstract interface instead.
- Use this when drawing architectural boundaries to ensure all cross-boundary source code dependencies point toward the more abstract side.
- Use this when a function in a base class needs to be customized—prefer making it abstract over overriding a concrete implementation.
- Use this when reviewing import/use/include statements to audit whether any volatile concrete modules are referenced directly.
- Use this when setting up the application entry point ('main') to identify the correct place to isolate unavoidable concrete dependencies.

## Concrete Examples

- Java's String class is cited as a stable concrete dependency that DIP tolerates because changes to it are rare and tightly controlled.
- Figure 11.1: Application depends on a Service interface; ServiceFactory interface provides makeSvc(); ServiceFactoryImpl (in the concrete component) instantiates ConcreteImpl and returns it as a Service, isolating the concrete dependency behind the architectural boundary.
- The 'main' function as the canonical concrete component that instantiates ServiceFactoryImpl and assigns it to a global variable of type ServiceFactory, containing all unavoidable DIP violations in one place.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 11: DIP: The Dependency Inversion Principle**

An LLM coding agent, when asked to implement a feature quickly, will naturally emit direct instantiation of concrete classes (e.g., 'new ConcreteService()') and concrete imports throughout generated code because it optimizes for immediate compilability rather than long-term stability. DIP awareness prevents the agent from wiring volatile implementation details directly into high-level modules it generates, and forces it to emit factory interfaces and abstract boundaries even when the user prompt does not explicitly request them. Without this principle, agent-generated scaffolding tends to create tightly coupled monoliths where every generated module transitively depends on every other, making the codebase brittle to the incremental changes that follow initial generation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
