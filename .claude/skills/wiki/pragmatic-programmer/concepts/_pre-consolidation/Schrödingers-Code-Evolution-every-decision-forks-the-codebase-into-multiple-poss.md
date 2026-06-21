---
title: Schrödinger's Code Evolution: every decision forks the codebase into multiple possible futures; design to keep as many viable futures open as possible
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Reversibility.json]
contributing_chapters: ["Reversibility"]
confidence: high
---

# Schrödinger's Code Evolution: every decision forks the codebase into multiple possible futures; design to keep as many viable futures open as possible

> From chapter: *Reversibility*

## Core Principle

Reversibility is the practice of ensuring that critical architectural, vendor, and deployment decisions can be changed cheaply by keeping them abstract, configuration-driven, and decoupled. The core thesis is that no decision is final—requirements, vendors, and platforms all change—so code must be designed to support multiple futures rather than locking into one. The primary techniques are DRY, decoupling, abstraction layers over third parties, and metadata-driven configuration.

## Key Heuristics

These are the load-bearing rules for this concept.

> There Are No Final Decisions

> Nothing is more dangerous than an idea if it's the only one you have.

> Think of decisions more as being written in the sand at the beach. A big wave can come along and wipe them out at any time.

> Enable your code to rock-n-roll: to 'rock on' when it can, to roll with the punches when it must.

> With every critical decision, the project team commits to a smaller target—a narrower version of reality that has fewer options.

> If you really abstracted the idea of a database out—to the point where it simply provides persistence as a service—then you have the flexibility to change horses in midstream.

> Make it reversible. If something is added automatically, it can be taken out automatically as well.

## Anti-Patterns & Fixes

- Stone-Carved Decisions: assuming any architectural or vendor decision is permanent, causing massive rework when requirements change. Fix: abstract dependencies behind interfaces and treat all decisions as provisional.
- Direct Third-Party Entanglement: calls to third-party products scattered throughout the codebase with no abstraction layer, making vendor replacement catastrophically expensive. Fix: hide every third-party product behind a well-defined, abstract interface.
- Single-Solution Myopia: believing there is only one way to implement something, leaving no fallback when that approach fails. Fix: design for multiple implementation paths and keep at least one alternative viable.
- Hard-Coded Deployment Assumptions: baking client-server or stand-alone logic directly into code rather than configuration, making deployment model changes require re-architecture. Fix: externalize deployment decisions into metadata or configuration files.
- Deferred Reversibility Thinking: only considering flexibility after the system is 85% built, when change is prohibitively expensive. Fix: address reversibility up front by applying DRY, decoupling, and metadata-driven design from the start.

## When To Apply

Load this page when:

- Use this when selecting a database, ORM, or data-persistence layer at the start of a project, to ensure the choice can be swapped without cascading code changes.
- Use this when integrating a third-party API or SDK, to determine whether to wrap it in an abstraction layer before writing any consuming code.
- Use this when choosing a deployment architecture (standalone vs. client-server vs. n-tier), to ensure the decision lives in configuration rather than business logic.
- Use this when a stakeholder presents a requirement as fixed and non-negotiable, as a reminder to still design the surrounding code for future change.
- Use this when adding vendor-specific statements or annotations that must appear in multiple files, to evaluate whether a code-generation or aspect-oriented mechanism can centralize and later reverse them.
- Use this when evaluating how long a deployment or platform change would take, as a diagnostic—if the answer is 'weeks,' reversibility has been neglected.
- Use this when scaffolding a new service or module, to decide which dependencies should be injected or configured rather than hard-coded.

## Concrete Examples

- Project coded 85% against database XYZ is forced by company policy to switch to database PDQ, requiring full recode and weekend overtime—illustrating the cost of non-reversible database coupling.
- A relational database from vendor A proves too slow in performance testing; an abstracted persistence layer allows switching to object database vendor B without broad codebase changes.
- A client-server product must produce a stand-alone version (and vice versa) due to late-stage marketing decisions; if deployment is configuration-only, this should take only days.
- A CORBA architecture allows replacing a slow Java client with C++ or a C++ rules engine with Smalltalk, affecting only the replaced component.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Reversibility**

An LLM coding agent is especially prone to non-reversibility because it optimizes for the most direct, concrete solution to the immediate prompt—hardcoding vendor SDKs, specific DB drivers, or deployment assumptions inline without prompting for abstraction. Unlike a human who accumulates pain from past rewrites, an agent has no memory of prior costly changes and will repeat the anti-pattern every session unless reversibility is an explicit constraint in its instructions. Applying this chapter means an agent should default to generating adapter interfaces, configuration-driven deployment flags, and dependency-injected third-party calls rather than direct inline usage, treating every external dependency as a seam that may need to be cut later.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
