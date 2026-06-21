---
title: True vs. Accidental Duplication: A distinction between duplication that must be unified (true duplication) and superficially similar code that will diverge over time (accidental duplication) and must not be merged
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-16-Independence.json]
contributing_chapters: ["Chapter 16: Independence"]
confidence: high
---

# True vs. Accidental Duplication: A distinction between duplication that must be unified (true duplication) and superficially similar code that will diverge over time (accidental duplication) and must not be merged

> From chapter: *Chapter 16: Independence*

## Core Principle

Good architecture achieves independence by decoupling the system both horizontally (into layers: UI, business rules, database) and vertically (into use cases), so that each axis of change is isolated. The decoupling mode—source, deployment, or service level—should be treated as an open option that evolves with the system rather than a fixed early decision, with the preference to stay at the cheapest sufficient level. True duplication should be consolidated, but accidental duplication that will diverge over time must be left separate even when it feels wasteful.

## Key Heuristics

These are the load-bearing rules for this concept.

> A good architecture makes the system easy to change, in all the ways that it must change, by leaving options open.

> A good architecture will allow a system to be born as a monolith, deployed in a single file, but then to grow into a set of independently deployable units, and then all the way to independent services and/or micro-services.

> Resist the temptation to commit the sin of knee-jerk elimination of duplication. Make sure the duplication is real.

> The decoupling mode of a system is one of those things that is likely to change with time, and a good architect foresees and appropriately facilitates those changes.

> A shopping cart application with a good architecture will look like a shopping cart application.

> My preference is to push the decoupling to the point where a service could be formed, should it become necessary; but then to leave the components in the same address space as long as possible.

> Dealing with service boundaries where none are needed is a waste of effort, memory, and cycles.

## Anti-Patterns & Fixes

- Monolith Lock-In: Writing a system that structurally depends on being a monolith, making it impossible to transition to processes, threads, or services when operational needs change. Fix: Maintain proper component isolation and avoid assuming the means of communication between components from the start.
- Premature Service-Level Decoupling: Defaulting to micro-services from the beginning, incurring expensive coarse-grained decoupling, development overhead, and resource waste before the need is proven. Fix: Decouple at source level first, promote to deployment or service level only when development, deployment, or operational pressure demands it.
- Knee-Jerk Duplication Elimination: Merging two use cases or UI screens because they look similar at a point in time, creating tight coupling that is painful to undo when they inevitably diverge. Fix: Verify duplication is true (changes together forever) before unifying; leave accidental duplicates separate.
- Passing Database Records Directly to the UI: Skipping a view model because the DB schema and screen structure look identical, coupling the persistence layer to the presentation layer. Fix: Create a separate view model and copy elements across to maintain horizontal layer decoupling.
- Invisible Use Cases in Architecture: Burying behavioral intent inside implementation details so developers must hunt for use cases. Fix: Make use cases first-class, prominently named elements at the top level of the system structure so the architecture screams its intent.

## When To Apply

Load this page when:

- Use this when designing the top-level structure of a new system and deciding how to partition components across files, packages, or services.
- Use this when a system initially built as a monolith needs to scale and you must decide which components to extract into separate deployment units or services.
- Use this when two use cases share a similar screen layout, algorithm, or database schema and you are deciding whether to share or duplicate the code.
- Use this when adding a new use case and you want to ensure it does not interfere with existing use cases already in production.
- Use this when teams are growing and you need the architecture to allow parallel, independent development without merge conflicts or cross-team blocking.
- Use this when evaluating deployment complexity and determining whether the architecture enables immediate deployment after build or requires manual configuration steps.
- Use this when choosing between source-level, deployment-level, or service-level decoupling for a component that may need to scale independently later.
- Use this when the business rules of a domain need to be separated from application-specific validation logic to allow them to evolve at different rates.

## Concrete Examples

- Shopping cart application: used to illustrate that a well-architected system should visibly look like its domain—use cases named and prominent at the top level.
- Add-order vs. delete-order use cases: used to show that two use cases in the same system change for different reasons and must be decoupled vertically through all layers.
- Interest calculation vs. input field validation: used to distinguish application-independent business rules (domain logic) from application-specific business rules, which change at different rates.
- Single server growing to multi-server: used to illustrate that a system initially needing only source-level decoupling may later require deployment-level or service-level decoupling as operational needs grow.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 16: Independence**

An LLM coding agent is especially prone to accidental duplication elimination—when generating multiple use cases or screens, it will naturally factor out similar-looking code into shared abstractions because pattern-matching toward DRY is a strong training signal, even when the duplication is accidental and the components will diverge. Similarly, an agent generating a full system scaffold tends to pick a single decoupling mode (often either a flat monolith or full micro-services) and bake it into every generated file, foreclosing the option to migrate; the chapter's framework of progressive, reversible decoupling must be explicitly prompted into the agent's design instructions to avoid this lock-in.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
