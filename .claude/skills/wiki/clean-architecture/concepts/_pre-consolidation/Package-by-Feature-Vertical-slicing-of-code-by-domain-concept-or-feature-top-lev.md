---
title: Package by Feature: Vertical slicing of code by domain concept or feature; top-level structure screams business domain but still suboptimal for enforcing boundaries
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-34-The-Missing-Chapter.json]
contributing_chapters: ["Chapter 34: The Missing Chapter"]
confidence: high
---

# Package by Feature: Vertical slicing of code by domain concept or feature; top-level structure screams business domain but still suboptimal for enforcing boundaries

> From chapter: *Chapter 34: The Missing Chapter*

## Core Principle

Chapter 34 argues that high-level architectural intentions (Clean Architecture, ports and adapters, SOLID) are routinely undermined by mundane implementation decisions: how packages are named, how types are grouped, and what access modifiers are applied. The author compares four packaging strategies — by layer, by feature, by ports-and-adapters, and by component — and concludes that the compiler, not discipline or post-build tooling, is the most reliable enforcer of architectural rules. The core recommendation is to minimize public visibility and align package boundaries with component boundaries so that illegal dependencies simply cannot compile.

## Key Heuristics

These are the load-bearing rules for this concept.

> The devil is in the implementation details.

> Your best design intentions can be destroyed in a flash if you don't consider the intricacies of the implementation strategy.

> A layered architecture doesn't scream anything about the business domain.

> The fewer public types you have, the smaller the number of potential dependencies.

> I'd personally like to use the compiler to enforce my architecture if at all possible.

> Think about using your compiler to help you enforce your chosen architectural style.

> We enforce this principle through good discipline and code reviews, because we trust our developers — [but] we all know what happens when budgets and deadlines start looming ever closer.

## Anti-Patterns & Fixes

- Relaxed Layered Architecture: A developer bypasses the service/business-logic layer and injects a repository directly into a controller. Dependency arrows still point downward so the graph looks clean, but business logic (e.g., authorization) is silently skipped. Fix: Use package-level access modifiers or static analysis rules to make repositories inaccessible from outside their component.
- Package by Layer at Scale: Three large horizontal buckets (web, services, repositories) become unwieldy as the system grows; the structure reveals nothing about the business domain. Fix: Migrate to package-by-feature or package-by-component organization.
- Périphérique Anti-Pattern of Ports and Adapters: Consolidating all infrastructure code in one source tree lets a web controller call a database repository directly without passing through the domain. Fix: Either split infrastructure into per-component source trees or rigorously apply access modifiers to prevent cross-infrastructure calls.
- Trust-Based Architectural Enforcement: Relying on developer discipline or post-compilation static analysis to enforce rules leads to violations under deadline pressure and long feedback loops. Fix: Encode architectural constraints in package structure and access modifiers so the compiler rejects violations at compile time.
- Over-Public Types in Layered Packages: Marking interfaces and classes public because they cross package boundaries exposes them as unintended extension points throughout the codebase. Fix: Use package-protected (or internal in .NET) visibility for all types that don't need to be consumed outside their component.

## When To Apply

Load this page when:

- Use this when organizing a new codebase and deciding how to group classes into packages or modules.
- Use this when a code review reveals that a controller is directly injecting a repository, bypassing service/business-logic classes.
- Use this when the top-level package structure of a project gives no indication of the business domain it serves.
- Use this when choosing between compile-time enforcement (access modifiers, module systems) versus runtime or post-build static analysis for architectural rules.
- Use this when splitting a monolith into source trees or modules and deciding how many source trees are needed.
- Use this when adding a new use case and needing to determine which existing classes are appropriate entry points.
- Use this when a ports-and-adapters project consolidates all infrastructure in one package and you need to assess cross-infrastructure coupling risk.

## Concrete Examples

- Online bookstore 'view orders' use case implemented four ways (package by layer, package by feature, ports and adapters, package by component) using OrdersController, OrdersService, OrdersServiceImpl, OrdersRepository, and JdbcOrdersRepository.
- A new hire implements an orders use case by injecting OrdersRepository directly into OrdersController, creating a relaxed layered architecture that bypasses business logic.
- Paris's Boulevard Périphérique ring road as an analogy for infrastructure code that routes around the domain when all infrastructure lives in a single source tree.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 34: The Missing Chapter**

An LLM coding agent, when asked to implement a new use case quickly, will naturally reuse the most visible and accessible existing classes — exactly like the 'new hire' anti-pattern — injecting repositories directly into controllers because those types are public and discoverable. Unlike a human who might remember an architectural discussion, the agent has no memory of intent: it enforces only what the type system and compiler enforce, making access-modifier-based architectural constraints critically important. Generating code with overly broad public visibility is a default agent failure mode; structuring packages so that the compiler rejects illegal dependencies removes the need for the agent to 'know' the rules.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
