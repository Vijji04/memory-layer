---
title: Stability Antipatterns Framework: a set of named patterns that amplify transient failures and accelerate systemic cracks, to be identified and avoided
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
sources: [extracts/release-it/Chapter-6-Stability-Summary.json]
contributing_chapters: ["Chapter 6: Stability Summary"]
confidence: high
---

# Stability Antipatterns Framework: a set of named patterns that amplify transient failures and accelerate systemic cracks, to be identified and avoided

> From chapter: *Chapter 6: Stability Summary*

## Core Principle

At production scale, statistically rare failure combinations become near-certainties; stability antipatterns transform these transient events into catastrophic outages while stability patterns contain the damage. The chapter closes a six-chapter arc on stability by reiterating that failures are inevitable, that paranoid design is rational, and that the goal is not preventing all failures but ensuring the system survives them. Judgment in matching specific stability patterns to specific identified threats — not blanket application — is the key differentiator.

## Key Heuristics

These are the load-bearing rules for this concept.

> Astronomically unlikely coincidences happen daily.

> Failures are inevitable.

> Stability antipatterns amplify transient events. They accelerate cracks in the system.

> Avoiding the antipatterns does not prevent bad things from happening, but it will help minimize the damage when bad things do occur.

> View other enterprise systems with suspicion and distrust—any of them can stab you in the back.

> Paranoia is just good thinking.

> Staying up is more than half the battle.

## Anti-Patterns & Fixes

- Optimism Bias: assuming edge cases or unlikely failure combinations won't occur in production. Fix: calculate actual opportunity count (requests × assets × time) to reframe 'astronomical' odds as near-certainties at scale.
- Stability Antipattern Accumulation: allowing known antipatterns to persist in the codebase because failures haven't happened yet. Fix: proactively identify and eliminate antipatterns before they amplify real transient events.
- Undifferentiated Threat Response: applying stability patterns uniformly or not at all rather than matching patterns to specific threats. Fix: identify each threat explicitly and apply the most appropriate stability pattern to each one.
- Dependency Trust: treating integrated enterprise systems or third-party services as reliably stable. Fix: assume all external dependencies can and will fail; design defensively around every integration point.

## When To Apply

Load this page when:

- Use this when designing integration points with external services, databases, or third-party APIs where a failure could cascade.
- Use this when estimating the risk of an edge case in a high-traffic system — multiply request rate by time to get actual failure opportunity count before dismissing it as unlikely.
- Use this when reviewing generated code for missing error handling, timeouts, retries, or circuit breakers around I/O operations.
- Use this when a system is approaching production and stability patterns have not been explicitly applied to identified threat surfaces.
- Use this when evaluating whether to add defensive code that 'probably won't be needed' — reframe using the scale heuristic.
- Use this when auditing a codebase that has had stability incidents to identify which antipatterns amplified the original transient fault.

## Concrete Examples

- Ten million page views per day over three years with fifty assets per page yields 547,500,000,000 chances for something to go wrong — more than the estimated 400 billion stars in the Milky Way galaxy.
- The survival statistics of software projects: ~50% canceled in development, ~50% of survivors late/overbudget/feature-incomplete, leaving less than 25% reaching production — and of those, most incur major downtime and maintenance costs.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 6: Stability Summary**

An LLM coding agent is especially prone to optimism bias by default: it generates the 'happy path' implementation without spontaneously adding timeouts, bulkheads, or circuit breakers unless explicitly prompted, because training data skews toward functional examples rather than defensive ones. This chapter's scale heuristic is a forcing function an agent can apply mechanically — given request volume and asset count, it can compute actual failure opportunity counts and self-trigger the addition of stability patterns. The agent should treat every external call it generates as a potential stab-in-the-back and default to wrapping it in a stability pattern rather than waiting for a human to notice the gap.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
