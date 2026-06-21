---
title: Iterative Schedule Refinement: Estimate project schedules by completing increments, then refine estimates based on actual experience from those increments rather than guessing upfront
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Estimating.json]
contributing_chapters: ["Estimating"]
confidence: high
---

# Iterative Schedule Refinement: Estimate project schedules by completing increments, then refine estimates based on actual experience from those increments rather than guessing upfront

> From chapter: *Estimating*

## Core Principle

Estimation is a learnable skill built on explicit modeling: understand what's asked, build a rough model, decompose it, identify high-impact parameters, calculate with sensitivity analysis, and scale units to match true precision. Project schedules specifically should be iterated incrementally rather than committed upfront, since real experience is the only reliable data source. The single best response when asked for an estimate on the spot is always 'I'll get back to you.'

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 18: Estimate to Avoid Surprises

> Tip 19: Iterate the Schedule with the Code

> Estimates given at the coffee machine will (like the coffee) come back to haunt you.

> When asked for an estimate, say 'I'll get back to you.'

> Choose the units of your answer to reflect the accuracy you intend to convey.

> Ask someone who's already done it — before you get too committed to model building.

> If your arithmetic is correct, your understanding of the problem or your model is probably wrong.

> Doubling the effort on the model may give you only a slight increase in accuracy.

## Anti-Patterns & Fixes

- Coffee Machine Estimation: Giving an off-the-cuff estimate immediately when asked, without time to model the problem. Fix: Slow down, say 'I'll get back to you,' then work through the model-decompose-parameterize steps before committing.
- False Precision via Fine Units: Quoting '130 working days' when you mean 'about six months,' implying more accuracy than you have. Fix: Scale units to match true precision — use weeks or months for longer durations.
- Upfront Hard Schedule Commitment: Nailing down a fixed project timeline before any increments are completed, especially with a new team or technology. Fix: Iterate the schedule with the code, refining estimates after each increment.
- Dismissing Strange Results: Quickly discarding surprising calculation outputs. Fix: Treat unexpected results as signals that your model or problem understanding is wrong, and investigate before proceeding.
- Uniform Parameter Effort: Spending equal effort on all parameters regardless of their influence on the result. Fix: Identify multiplicative vs. additive parameters and focus accuracy effort on the high-leverage ones.
- No Estimation Post-Mortem: Shrugging off wrong estimates without analysis. Fix: Record estimates, compare to actuals, and investigate the root cause of significant deviations to improve future estimates.

## When To Apply

Load this page when:

- Use this when asked how long a feature, refactor, or project will take before any code has been written or requirements are fully defined.
- Use this when evaluating whether a proposed technical approach is feasible (e.g., 'can we stream this dataset over this connection in time?').
- Use this when deciding which parts of a system need optimization and which can be left alone.
- Use this when a stakeholder requests a project timeline at the start of a sprint or project with an unfamiliar codebase or team.
- Use this when a back-of-envelope calculation yields a surprising or counterintuitive result during system design.
- Use this when choosing between two architectural options and needing to compare rough performance characteristics without benchmarking.
- Use this when an initial estimate from a prior iteration has proven inaccurate and needs revision based on new evidence.

## Concrete Examples

- Estimating time to send War and Peace over a 56k modem line — illustrates that seemingly vague questions can be answered with scoped assumptions.
- Response time estimate: 'roughly three quarters of a second with SCSI bus and 64MB memory, one second with 48MB' — shows parametric, hedged answer style.
- Pi approximation at different precision levels (3, 22/7, 12 decimal places) for flower bed vs. school vs. NASA — illustrates context-dependent accuracy requirements.
- 130 working days vs. 'about six months' — same duration, different implied accuracy based on units chosen.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Estimating**

An LLM coding agent is prone to generating confident, precise-sounding estimates without flagging uncertainty — the equivalent of coffee machine estimates at scale, repeated across every response. Unlike a human who learns to calibrate intuition over years, an agent must explicitly invoke the model-decompose-parameterize framework and surface key assumptions (scope, parameters, units) in its output to avoid false precision. The agent failure mode this prevents is producing a single deterministic number (e.g., '47 hours') that gets treated as a commitment, when a properly scoped range with stated assumptions (e.g., 'roughly 4–8 weeks, assuming X and Y') would be far more actionable and honest.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
