---
title: Asymmetric Marriage Model: The relationship between developer and framework is one-sided — you commit fully to the framework, but the framework author commits nothing to you
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-32-Frameworks-Are-Details.json]
contributing_chapters: ["Chapter 32: Frameworks Are Details"]
confidence: high
---

# Asymmetric Marriage Model: The relationship between developer and framework is one-sided — you commit fully to the framework, but the framework author commits nothing to you

> From chapter: *Chapter 32: Frameworks Are Details*

## Core Principle

Frameworks are implementation details, not architectures — they belong in the outermost dependency circles and must never be coupled into core business logic or Entities. The developer-framework relationship is asymmetric: you take on all the risk of coupling while the framework author owes you nothing. The solution is to treat frameworks as late-bound, replaceable plugins by using proxies and adapters, restricting framework knowledge to the Main component and outer layers.

## Key Heuristics

These are the load-bearing rules for this concept.

> Frameworks are not architectures—though some try to be.

> Don't marry the framework!

> Keep it at arm's length. Treat the framework as a detail that belongs in one of the outer circles of the architecture. Don't let it into the inner circles.

> If the framework wants you to derive your business objects from its base classes, say no! Derive proxies instead, and keep those proxies in components that are plugins to your business rules.

> When you marry a framework to your application, you will be stuck with that framework for the rest of the life cycle of that application.

> Perhaps you can find a way to get the milk without buying the cow.

> You should not sprinkle @autowired annotations all throughout your business objects. Your business objects should not know about Spring.

## Anti-Patterns & Fixes

- FrameworkMarriage: Wrapping your entire architecture around a framework by deriving business objects from its base classes, tightly coupling core logic to framework internals. This makes the framework impossible to remove and causes friction as the product matures. Fix: Derive proxies or adapters that live in outer plugin layers, keeping business rules framework-agnostic.
- EntityContamination: Importing framework annotations or base classes directly into Entities or core business objects (e.g., @autowired on business classes). This violates the Dependency Rule and embeds a volatile detail into stable core logic. Fix: Restrict framework coupling to the Main component or outermost plugin layer.
- PrematureFrameworkCommitment: Adopting a framework at the start of a project without evaluating long-term fit, treating its conventions as architecture. Fix: 'Date' the framework first — use it behind an architectural boundary and delay full commitment as long as possible.
- FrameworkEvolutionLockIn: Assuming the framework will evolve in a direction aligned with your needs, leading to forced upgrades or loss of features. Fix: Isolate framework usage behind interfaces so that switching or upgrading affects only the outer layer.

## When To Apply

Load this page when:

- Use this when choosing whether to extend a framework's base class inside a domain model or Entity class.
- Use this when scaffolding a new service and deciding where to place framework-specific annotations (e.g., Spring @autowired, Django models.Model inheritance).
- Use this when a framework upgrade is breaking core business logic, indicating the framework has leaked into inner architectural layers.
- Use this when evaluating whether to adopt a new framework for a greenfield project and determining how deeply to integrate it.
- Use this when a newer, better framework appears and you need to assess migration cost — high cost signals the current framework was over-married.
- Use this when writing dependency injection wiring code and deciding which components should be aware of the DI container.
- Use this when a framework's conventions conflict with clean domain modeling (e.g., ORM requiring anemic entities with no-arg constructors).

## Concrete Examples

- Spring Framework @autowired annotations: the text warns against sprinkling @autowired throughout business objects, recommending injection be confined to the Main component instead.
- C++ STL and Java standard library cited as examples of frameworks you 'must marry' — unavoidable but still a deliberate decision to acknowledge.
- Spring used as a dependency injection framework injecting into Main — acceptable because Main is the 'dirtiest, lowest-level component in the architecture'.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 32: Frameworks Are Details**

An LLM coding agent defaults to idiomatic framework usage as seen in training data — scaffolding code that inherits from framework base classes, sprinkles framework annotations on domain objects, and structures the entire codebase around framework conventions, effectively marrying the framework by default on every generation. This is worse than human over-adoption because the agent has no long-term stake in the project and will not experience the maintenance pain, so it has no self-correcting feedback signal. Agents must be explicitly constrained to treat frameworks as outer-circle plugins and to generate adapter/proxy patterns rather than direct framework inheritance in core domain code.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
