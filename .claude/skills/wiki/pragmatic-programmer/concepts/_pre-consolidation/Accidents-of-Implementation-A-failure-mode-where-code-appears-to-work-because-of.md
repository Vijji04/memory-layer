---
title: Accidents of Implementation: A failure mode where code appears to work because of undocumented edge behavior in dependencies, not because of correct design
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Programming-by-Coincidence.json]
contributing_chapters: ["Programming by Coincidence"]
confidence: high
---

# Accidents of Implementation: A failure mode where code appears to work because of undocumented edge behavior in dependencies, not because of correct design

> From chapter: *Programming by Coincidence*

## Core Principle

Programming by Coincidence is the dangerous practice of writing code that appears to work without understanding why, relying on accidental successes, undocumented behaviors, and unverified assumptions. The antidote — Programming Deliberately — requires always knowing why code works, relying only on documented interfaces, explicitly testing assumptions, and documenting all contextual dependencies. Code written by coincidence is fragile, unfixable when it breaks, and increasingly dangerous as it accumulates.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Program by Coincidence

> Don't code blindfolded. Attempting to build an application you don't fully understand, or to use a technology you aren't familiar with, is an invitation to be misled by coincidences.

> Rely only on reliable things. Don't depend on accidents or assumptions. If you can't tell the difference in particular circumstances, assume the worst.

> For routines you call, rely only on documented behavior. If you can't, for whatever reason, then document your assumption well.

> Don't just test your code, but test your assumptions as well. Don't guess; actually try it.

> Don't be a slave to history. Don't let existing code dictate future code.

> Always be aware of what you are doing.

## Anti-Patterns & Fixes

- Coincidence-Driven Development: Writing code until it 'seems to work' without understanding why, then shipping it. The code breaks under different conditions and is unfixable because the original success was never understood. Fix: Before moving on, explicitly identify and verify why the code works, not just that it works.
- Spurious Call Accumulation: Adding redundant or incorrectly-ordered API calls (e.g., paint/invalidate/validate/revalidate/repaint/paintImmediately) until something works, then leaving them all in. Fix: Understand the correct calling contract of each API and use only the documented, necessary calls.
- Undocumented Behavior Reliance: Depending on error responses, boundary conditions, or side effects of a routine that its author never intended or documented. Fix: Only rely on the documented interface; if you must use undocumented behavior, explicitly document your assumption in code.
- Untested Assumptions: Treating causal relationships (X causes Y) as proven when they are merely observed. Fix: Write assertions or explicit tests that verify assumptions, making them part of the documented, executable specification.
- Context Lock-In: Writing utility modules that silently require a specific environment (GUI, locale, OS) without documenting or enforcing that requirement. Fix: Identify all environmental dependencies and either eliminate them or make them explicit contract preconditions.

## When To Apply

Load this page when:

- Use this when a code change fixes a bug but you cannot explain the mechanism by which it fixes it
- Use this when calling a third-party or library API and the behavior you are relying on is not in its official documentation
- Use this when code works in one environment but needs to be deployed in another (different OS, locale, resolution, or runtime)
- Use this when adding repeated or varied calls to the same API trying different combinations until output is correct
- Use this when an integration test passes but the reason for passage is unclear or the test only covers one narrow scenario
- Use this when inheriting legacy code and deciding whether to keep existing behavior or refactor, to avoid assuming existing behavior is intentional
- Use this when generating or scaffolding boilerplate code to ensure each generated piece is understood before being relied upon

## Concrete Examples

- A soldier probing a minefield with a bayonet, finding no mines, concluding it is safe, then marching forward and being blown up — illustrating false conclusions from limited probing
- Fred repeatedly adding code that 'seems to work' until the program inexplicably breaks and he cannot fix it because he never understood why it worked
- A sequence of GUI calls (paint, invalidate, validate, revalidate, repaint, paintImmediately) added iteratively until the screen renders, left in place because 'it works now'

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Programming by Coincidence**

An LLM coding agent is especially vulnerable to Programming by Coincidence because it generates plausible-looking code based on statistical pattern-matching rather than causal understanding — it can produce code that passes provided test cases by coincidence, relying on undocumented API behaviors or environment assumptions baked into its training data. Unlike a human who at least experienced the code working in a specific context, an agent may confidently emit spurious call sequences or context-dependent code with no flag that the reasoning is coincidental. This framework instructs an agent to explicitly verify each API call against documented contracts, surface all environmental assumptions as explicit preconditions, and refuse to move forward when the mechanism of correctness is unknown rather than when tests merely pass.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
