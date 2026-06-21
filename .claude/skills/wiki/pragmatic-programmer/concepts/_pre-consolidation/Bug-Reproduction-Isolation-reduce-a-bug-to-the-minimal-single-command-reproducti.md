---
title: Bug Reproduction Isolation: reduce a bug to the minimal single-command reproduction case before attempting a fix
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/18-Debugging.json]
contributing_chapters: ["18. Debugging"]
confidence: high
---

# Bug Reproduction Isolation: reduce a bug to the minimal single-command reproduction case before attempting a fix

> From chapter: *18. Debugging*

## Core Principle

Debugging is systematic problem-solving, not emotional blame assignment: the core discipline is reproducing bugs minimally, tracing root causes rather than symptoms, and proving assumptions rather than trusting them. Key strategies include data visualization, tracing for time-dependent systems, rubber ducking to surface hidden assumptions, and binary search when no clear starting point exists. The meta-lesson is that surprise at a bug signals a false belief that must be falsified, not defended.

## Key Heuristics

These are the load-bearing rules for this concept.

> Fix the Problem, Not the Blame

> Don't Panic

> Don't Assume It—Prove It

> 'select' Isn't Broken

> If your first reaction on witnessing a bug or seeing a bug report is 'that's impossible,' you are plainly wrong.

> Beware of myopia when debugging. Resist the urge to fix just the symptoms you see.

> Always try to discover the root cause of a problem, not just this particular appearance of it.

> The amount of surprise you feel when something goes wrong is directly proportional to the amount of trust and faith you have in the code being run.

## Anti-Patterns & Fixes

- Blame Culture: spending time identifying who caused a bug instead of fixing it. Fix: treat every bug as your problem to solve regardless of origin.
- Symptom Fixing: patching the visible symptom without finding root cause, allowing the underlying defect to resurface. Fix: trace causality back to the actual fault, not just its current manifestation.
- Third-Party Blame: assuming the OS, compiler, or library is broken before exhausting application-level explanations. Fix: eliminate your own code first; assume the platform is correct until proven otherwise.
- Untestable Reproduction Path: relying on long manual step sequences to reproduce a bug, making verification of fixes unreliable. Fix: reduce the bug to a single reproducible command.
- Assumption Trust: skipping review of 'known good' code because of past confidence in it. Fix: prove correctness in the current context with current data and boundary conditions.
- Coincidence Debugging: treating coincidental correlations as causal. Fix: be accurate in observations and eliminate coincidences before chasing them.

## When To Apply

Load this page when:

- Use this when a bug report cannot be reproduced and you need to determine the minimal conditions that expose it.
- Use this when a test passes locally but fails in another environment and you suspect a platform or library difference.
- Use this when you have no obvious starting point for a bug and need a systematic search strategy (binary search the codebase).
- Use this when a bug appears in code that was previously considered correct or well-tested, requiring re-examination of assumptions.
- Use this when a program's state is hard to reason about abstractly and you need to inspect actual runtime data structures.
- Use this when a bug fix is identified to determine whether the same defect pattern exists elsewhere in the system.
- Use this when compiler warnings exist in code under investigation, as they must be resolved before deeper debugging begins.
- Use this when a bug involves timing, concurrency, or event-driven behavior where a snapshot debugger is insufficient and tracing is required.

## Concrete Examples

- Graphics application crash: tester painted brush strokes upper-right to lower-left causing a crash, while programmer only tested lower-left to upper-right, missing the bug entirely for several days.
- Senior engineer convinced Solaris 'select' system call was broken, spent weeks on workarounds, until reading the documentation revealed the bug was in his own code. 'select is broken' became a team reminder phrase.
- Corrupt variable showing 0x6e69614d examined in surrounding memory revealed a street address ('Main St, Not own, XX') sprayed over a counter, pointing to the source of the corruption.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**18. Debugging**

An LLM coding agent is especially prone to assumption trust—it may treat code it generated moments ago as correct and search for bugs everywhere else first, mirroring the human 'that's impossible' failure mode but with no ego-correction mechanism. Agents also lack the ability to perform rubber ducking naturally and may instead iterate on surface-level symptom fixes without surfacing hidden assumptions in their own generated logic. The 'select isn't broken' heuristic is critical for agents: an LLM may hallucinate platform or library misbehavior as an explanation when the defect is in its own generated code, wasting tool-call cycles on phantom investigations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
