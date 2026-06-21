---
title: Pain Management Model: Refactoring is an exercise in pain management—small pain now versus catastrophic pain later as dependencies accumulate
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/33-Refactoring.json]
contributing_chapters: ["33. Refactoring"]
confidence: high
---

# Pain Management Model: Refactoring is an exercise in pain management—small pain now versus catastrophic pain later as dependencies accumulate

> From chapter: *33. Refactoring*

## Core Principle

Refactoring is the continuous, disciplined process of reworking code structure as understanding evolves, using the gardening metaphor rather than construction to frame software as organic and always in need of tending. The core discipline requires separating refactoring from feature work, maintaining comprehensive tests, and taking small verifiable steps to avoid net harm. Deferring refactoring is a false economy—dependency accumulation makes later changes exponentially more costly, so the pragmatic rule is to refactor early and often.

## Key Heuristics

These are the load-bearing rules for this concept.

> Refactor Early, Refactor Often

> Don't try to refactor and add functionality at the same time.

> Make sure you have good tests before you begin refactoring. Run the tests as often as possible.

> Take short, deliberate steps... If you keep your steps small, and test after each step, you will avoid prolonged debugging.

> fail to refactor now, and there'll be a far greater time investment to fix the problem down the road—when there are more dependencies to reckon with.

> Don't live with broken windows.

> If it hurts now, but is going to hurt even more later, you might as well get it over with.

## Anti-Patterns & Fixes

- Deferring Refactoring Under Time Pressure: Developers skip refactoring citing deadlines, but this causes dependencies to grow around the problematic code, making future refactoring exponentially more expensive and dangerous. Fix: Schedule refactoring explicitly; treat deferred refactoring as a tracked debt with stakeholder visibility.
- Refactoring and Adding Features Simultaneously: Mixing new functionality with structural changes makes it impossible to isolate the source of bugs or regressions. Fix: Complete refactoring as a separate, isolated commit or phase before adding new behavior.
- Large-Scale Reckless Reworking: Ripping up vast quantities of code with wild abandon risks leaving the codebase in a worse state than before. Fix: Make many small, localized changes that collectively achieve the larger-scale structural improvement, testing after each step.
- Construction Metaphor Thinking: Treating software as a finished artifact after initial build, calling only for maintenance fixes. Fix: Adopt the gardening metaphor—continuously monitor, prune, split, and reorganize code as understanding evolves.
- Silent Refactoring of Shared Interfaces: Changing a module's interface or functionality without signaling breakage to dependent code. Fix: Ensure drastic interface changes break the build so old clients are immediately identified and updated.

## When To Apply

Load this page when:

- Use this when you discover duplicated logic or copy-pasted code blocks that violate the DRY principle.
- Use this when a routine has grown too large or is attempting to accomplish more than one coherent responsibility.
- Use this when requirements have drifted and existing code encodes outdated assumptions about the domain.
- Use this when two separate implementations of similar behavior could be merged into a common abstraction.
- Use this when a design smells non-orthogonal—changes in one module ripple unexpectedly into unrelated modules.
- Use this when performance analysis reveals that functionality must be relocated within the system architecture.
- Use this when a code section feels 'wrong' or produces friction every time it is read or modified.
- Use this when adding a new feature reveals that the existing structure makes the addition unnecessarily complex or duplicative.

## Concrete Examples

- State-based tax calculation code (Texas/Ohio/Maine) with repeated calc formula and mixed rate logic—used as an exercise to demonstrate structural refactoring need.
- Java Shape class with integer constants for SQUARE, CIRCLE, RIGHT_TRIANGLE that needs restructuring before adding more shape types—demonstrates refactoring for extensibility.
- Medical analogy: a code 'growth' that is cheap to remove while small but increasingly dangerous and expensive to remove as it spreads, used to justify early refactoring to management.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**33. Refactoring**

An LLM coding agent is particularly prone to the 'construction metaphor' failure mode: it generates code in a single pass optimized for the immediate prompt, treating the output as a finished artifact rather than a first draft requiring future tending. This means agents will silently propagate duplication and non-orthogonal design across files because they lack continuous awareness of the evolving codebase state. Agents should be explicitly triggered to run a refactoring pass before and after feature additions, treating refactoring as a mandatory, test-gated phase rather than an optional cleanup step.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
