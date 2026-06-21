---
title: Stone Soup / Boiled Frog Duality: Strategy for instigating gradual change in organizations, paired with a warning about ignoring gradual negative change
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/A-Pragmatic-Philosophy.json]
contributing_chapters: ["A Pragmatic Philosophy"]
confidence: high
---

# Stone Soup / Boiled Frog Duality: Strategy for instigating gradual change in organizations, paired with a warning about ignoring gradual negative change

> From chapter: *A Pragmatic Philosophy*

## Core Principle

The Pragmatic Philosophy chapter establishes that great developers are defined by attitude and context-awareness rather than technical skill alone: they own their outcomes, think beyond the immediate problem, resist both entropy and complacency, and calibrate quality to actual requirements. The chapter introduces named frameworks — responsibility, entropy control, good-enough calibration, knowledge portfolio, and change strategy — that serve as the operating philosophy for all subsequent practices. Pragmatism is not cutting corners; it is making intelligent, informed trade-offs grounded in a clear understanding of the larger system.

## Key Heuristics

These are the load-bearing rules for this concept.

> Think beyond the immediate problem, always trying to place it in its larger context, always trying to be aware of the bigger picture.

> Without this larger context, how can you be pragmatic? How can you make intelligent compromises and informed decisions?

> Take responsibility for everything they do.

> Pragmatic Programmers won't sit idly by and watch their projects fall apart through neglect.

> Sometimes near-perfection is the only option, but often there are trade-offs involved.

> Learning is a continuous and ongoing process.

## Anti-Patterns & Fixes

- Tunnel Vision: Solving the immediate problem without considering broader context, leading to solutions that conflict with system-wide goals or introduce downstream debt. Fix: Always ask what larger system or goal the current problem sits inside before writing a line of code.
- Blame Deflection (Cat Ate My Source Code): Attributing failures to external causes instead of owning outcomes, which blocks learning and erodes trust. Fix: Accept responsibility, communicate honestly about mistakes, and course-correct proactively.
- Neglect-Driven Entropy: Allowing small code quality issues to accumulate unchecked until the codebase becomes unmaintainable. Fix: Address broken windows (small defects, bad designs) immediately before entropy spreads.
- Boiled Frog Syndrome: Ignoring gradual negative change — creeping scope, slow performance degradation, incremental security weakening — because each step seems minor. Fix: Periodically step back to evaluate cumulative drift, not just the latest delta.
- Perfectionism Misapplication: Applying near-perfection standards uniformly regardless of context, wasting resources where good-enough is sufficient. Fix: Explicitly determine the required quality level for each deliverable based on its context and trade-offs.
- Static Knowledge Base: Relying on a fixed set of skills and knowledge acquired at one point in time. Fix: Treat knowledge as a portfolio requiring active, continuous investment and diversification.

## When To Apply

Load this page when:

- Use this when a coding agent is asked to fix a small bug and must decide whether to also flag or address surrounding code smells it encounters.
- Use this when generating a solution that technically satisfies the immediate requirement but may conflict with stated architectural principles or long-term maintainability.
- Use this when an agent-generated change introduces a minor quality regression and the agent must decide whether to flag it or silently proceed.
- Use this when determining how much test coverage, error handling, or documentation to include — calibrate to the stated context and stakes of the software.
- Use this when an agent is operating across multiple iterations of a codebase and must assess whether incremental changes are collectively drifting the system in a bad direction.
- Use this when an agent must communicate a failure or limitation honestly rather than producing a plausible-sounding but incorrect output.
- Use this when evaluating whether a proposed shortcut or trade-off is a legitimate pragmatic decision or a false economy that increases long-term cost.

## Concrete Examples

- The Cat Ate My Source Code: named section illustrating the failure mode of not taking responsibility for outcomes.
- Stone Soup and Boiled Frogs: a dual example — the stone soup story as a strategy for instigating change, and the boiled frog as a cautionary tale about ignoring gradual negative change.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**A Pragmatic Philosophy**

An LLM coding agent is especially prone to narrow-context optimization — it will produce code that perfectly satisfies the literal prompt while silently violating architectural intent, accumulating entropy, or over-engineering for the wrong quality target. The Radical Responsibility and Bigger Picture frameworks force the agent to treat each generation as an accountable act with downstream consequences, not a stateless token prediction. Specifically, the Boiled Frog anti-pattern maps directly to multi-turn agent sessions where each individual change looks acceptable but cumulative drift is invisible unless the agent is explicitly prompted to audit it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
