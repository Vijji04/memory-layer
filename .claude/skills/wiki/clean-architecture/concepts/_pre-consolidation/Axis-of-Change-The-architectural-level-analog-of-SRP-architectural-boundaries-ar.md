---
title: Axis of Change: The architectural-level analog of SRP — architectural boundaries are drawn along the lines of actors whose change requests must be isolated from each other
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-7-SRP-The-Single-Responsibility-Principle.json]
contributing_chapters: ["Chapter 7: SRP: The Single Responsibility Principle"]
confidence: high
---

# Axis of Change: The architectural-level analog of SRP — architectural boundaries are drawn along the lines of actors whose change requests must be isolated from each other

> From chapter: *Chapter 7: SRP: The Single Responsibility Principle*

## Core Principle

SRP is not about functions doing one thing — it is about modules being owned by exactly one actor (stakeholder group), so that change requests from different parts of the organization cannot silently interfere with each other. Its two primary failure modes are accidental duplication (shared helpers modified for one actor break another) and merge collisions (different teams editing the same file). The fix in both cases is to separate code by actor, using plain data structures and the Facade pattern to manage the resulting class proliferation.

## Key Heuristics

These are the load-bearing rules for this concept.

> A module should be responsible to one, and only one, actor.

> A module should have one, and only one, reason to change.

> Cohesion is the force that binds together the code responsible to a single actor.

> Separate the code that different actors depend on.

> A function should do one, and only one, thing — but this is not the SRP.

> The SRP says to separate the code that different actors depend on.

## Anti-Patterns & Fixes

- Accidental Duplication via Shared Algorithm: Two methods serving different actors share a private helper (e.g., regularHours()). A change requested by one actor silently corrupts the behavior relied on by another. Fix: Separate methods serving different actors into distinct classes so shared helpers cannot be inadvertently modified across actor boundaries.
- Multi-Actor Merge Collisions: Multiple developers from different teams modify the same source file for unrelated actor-driven reasons, causing merge conflicts that risk cross-actor breakage. Fix: Split the class by actor so each team owns a separate file with no overlap.
- God Class with Mixed Responsibilities: A single class (e.g., Employee) hosts calculatePay(), reportHours(), and save(), coupling CFO, COO, and CTO concerns. Fix: Extract each actor's methods into its own class sharing a plain data structure (e.g., EmployeeData) with no behavior.
- Naming Confusion of SRP: Interpreting SRP as 'do only one thing' leads to over-decomposition at the function level while missing actor-level coupling. Fix: Always identify the actor (stakeholder group) when evaluating whether a module violates SRP.

## When To Apply

Load this page when:

- Use this when designing a class whose methods will be modified by requests from different business departments or stakeholders.
- Use this when a shared private helper function is called by two methods that serve different business purposes or reporting lines.
- Use this when multiple developers on different teams are likely to concurrently modify the same source file.
- Use this when a bug report reveals that a change requested by one team unexpectedly broke functionality used by a different team.
- Use this when deciding whether to consolidate related-seeming operations (e.g., calculate, report, persist) into one class.
- Use this when refactoring a large class to determine the correct split boundaries — split by actor, not by function type.
- Use this when evaluating merge conflict frequency in a file as a proxy signal for SRP violation.

## Concrete Examples

- Employee class in a payroll application with calculatePay() (CFO/accounting), reportHours() (COO/HR), and save() (CTO/DBAs) — three methods serving three distinct actors in a single class.
- regularHours() shared helper called by both calculatePay() and reportHours(); a CFO-requested tweak to regularHours() silently corrupts HR reports, costing the COO's budget millions.
- EmployeeData plain data structure shared by three separate classes (PayCalculator, HourReporter, EmployeeSaver), each serving one actor with no knowledge of the others.
- EmployeeFacade pattern delegating to PayCalculator, HourReporter, and EmployeeSaver to reduce instantiation complexity while preserving actor separation.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: SRP: The Single Responsibility Principle**

An LLM coding agent is prone to SRP violations because it optimizes for local coherence — grouping methods that seem semantically related (all about 'employees') without modeling the organizational boundaries that determine true actor alignment. When asked to add a feature, an agent will naturally inject new methods into the most relevant existing class, silently coupling new actors to old ones and creating accidental-duplication traps that no test will catch until runtime. Applying SRP explicitly requires the agent to ask 'which actor drives this change?' before placing any method, and to prefer creating a new class over extending an existing one when actors differ.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
