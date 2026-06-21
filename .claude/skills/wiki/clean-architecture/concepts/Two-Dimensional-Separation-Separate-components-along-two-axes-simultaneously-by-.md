---
title: Two-Dimensional Separation: Separate components along two axes simultaneously — by actor (SRP) and by policy level (Dependency Rule) — to isolate both reasons and rates of change
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-33-Case-Study-Video-Sales.json]
contributing_chapters: ["Chapter 33: Case Study: Video Sales"]
confidence: high
---

# Two-Dimensional Separation: Separate components along two axes simultaneously — by actor (SRP) and by policy level (Dependency Rule) — to isolate both reasons and rates of change

> From chapter: *Chapter 33: Case Study: Video Sales*

## Core Principle

This chapter applies SRP and the Dependency Rule to a concrete video-sales system by first identifying four actors as the primary sources of change, then partitioning components so each actor's code is isolated, and finally structuring dependencies so all cross-boundary arrows point toward higher-level policy. Component granularity is established at the build level for maximum flexibility, while deployment grouping remains a separate, adjustable decision. The two axes of separation — actor identity and policy level — together ensure that changes in one part of the system do not ripple unpredictably into others.

## Key Heuristics

These are the load-bearing rules for this concept.

> According to the Single Responsibility Principle, these four actors will be the four primary sources of change for the system.

> We want to partition the system such that a change to one actor does not affect any of the other actors.

> All dependencies cross the boundary lines in one direction, and they always point toward the components containing the higher-level policy.

> The using relationships (open arrows) point with the flow of control, and the inheritance relationships (closed arrows) point against the flow of control.

> I would certainly break the compile and build environment up this way, so that I could build independent deliverables like that. I would also reserve the right to combine all those deliverables into a smaller number of deliverables if necessary.

> Once you have structured the code this way, you can mix and match how you want to actually deploy the system.

> The different reasons correspond to the actors; the different rates correspond to the different levels of policy.

## Anti-Patterns & Fixes

- MonolithicActorBlob: Mixing code that serves different actors in the same component so that a change for one actor (e.g., Viewer pricing logic) forces redeployment or risks breaking another actor (e.g., Admin catalog management). Fix: Partition components per actor at the compile/build level, even if you later combine them into coarser deployment units.
- PrematureDeploymentCollapsing: Deciding too early to ship everything as one deployable, losing the ability to independently deploy components that change at different rates. Fix: Build at fine-grained component granularity first; only merge deliverables as a deliberate, reversible deployment decision.
- SkippingAbstractUseCases: Duplicating nearly identical use case logic (e.g., View Catalog as Viewer vs. View Catalog as Purchaser) instead of recognizing shared structure. Fix: Introduce an abstract use case and corresponding abstract classes in a shared component; concrete use cases inherit and extend.
- DependencyDirectionViolation: Allowing low-level detail components (views, controllers) to be depended upon by high-level policy components (interactors), causing detail changes to ripple into business rules. Fix: Apply the Dependency Rule — all cross-boundary arrows must point toward higher-level policy; use inheritance inversion (OCP) where flow of control opposes the required dependency direction.
- IncompleteActorIdentification: Beginning component design before identifying all primary actors, leading to partitions that do not align with real sources of change. Fix: Perform explicit use-case analysis first, name all actors, then derive component boundaries from those actors.

## When To Apply

Load this page when:

- Use this when designing the initial architecture of a multi-stakeholder system and you need to decide how to partition components.
- Use this when two use cases appear nearly identical and you must decide whether to unify them or keep them separate.
- Use this when choosing how many .jar/.dll/.whl deployment artifacts to produce from a codebase that has already been logically partitioned.
- Use this when a change requested by one user role (e.g., business license pricing) risks breaking or requiring redeployment of code used by a different role (e.g., individual streaming).
- Use this when drawing or reviewing a component dependency diagram to verify that all arrows across architectural boundaries point toward higher-level policy.
- Use this when scaffolding a new feature and you need to determine which existing component it belongs to based on which actor it serves.
- Use this when refactoring a system that has grown monolithic and you need a principled way to identify seams for splitting it.

## Concrete Examples

- A video sales website (modeled on cleancoders.com) with four actors — Viewer, Purchaser, Author, and Administrator — each with distinct use cases such as streaming/downloading videos, uploading content, and managing catalog and pricing.
- View Catalog as Viewer and View Catalog as Purchaser both inherit from an abstract View Catalog use case, implemented as abstract classes in a shared Catalog View / Catalog Presenter component.
- A preliminary component architecture (Figure 33.2) partitioned into per-actor views, presenters, interactors, and controllers, each as a potential separate .jar or .dll, with options to merge into 5, 3, or 2 deployment artifacts.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 33: Case Study: Video Sales**

An LLM coding agent, when asked to implement a feature, will typically generate code into the most convenient existing file or class rather than respecting actor-based component boundaries — silently coupling, say, Viewer logic with Admin logic. This chapter's actor-partitioning discipline gives the agent an explicit decision rule: before writing any code, identify which actor the feature serves and place it in that actor's component. Additionally, agents tend to flatten dependency graphs (importing whatever is convenient), so the Dependency Rule must be stated as a hard constraint in the agent's instructions to prevent low-level detail modules from being imported by high-level policy modules.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
