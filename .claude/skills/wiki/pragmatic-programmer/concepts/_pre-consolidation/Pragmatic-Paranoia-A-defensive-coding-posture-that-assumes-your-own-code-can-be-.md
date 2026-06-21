---
title: Pragmatic Paranoia: A defensive coding posture that assumes your own code can be wrong, and builds in mechanisms to detect those failures at runtime
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Assertive-Programming.json]
contributing_chapters: ["Assertive Programming"]
confidence: high
---

# Pragmatic Paranoia: A defensive coding posture that assumes your own code can be wrong, and builds in mechanisms to detect those failures at runtime

> From chapter: *Assertive Programming*

## Core Principle

Assertive Programming mandates that any condition you believe 'can never happen' must be enforced with an executable assertion rather than trusted as a silent assumption. Assertions should remain enabled in production, must be free of side effects, and must never substitute for legitimate error handling of recoverable conditions. The core discipline is converting mental confidence into machine-verified invariants throughout the codebase.

## Key Heuristics

These are the load-bearing rules for this concept.

> If It Can't Happen, Use Assertions to Ensure That It Won't

> Turning off assertions when you deliver a program to production is like crossing a high wire without a net because you once made it across in practice.

> Don't use assertions in place of real error handling.

> The condition passed to an assertion should not have a side effect.

> Never put code that must be executed into an assert.

> Your first line of defense is checking for any possible error, and your second is using assertions to try to detect those you've missed.

## Anti-Patterns & Fixes

- THIS-CAN-NEVER-HAPPEN Fallacy: Developers mentally dismiss impossible conditions instead of encoding them as assertions, leaving silent assumptions that become production bugs. Fix: Whenever you think 'that could never happen,' add an assertion to enforce it.
- Disabling Assertions in Production: Teams turn off assertions after testing to improve performance, falsely assuming testing found all bugs and production is a safe environment. Fix: Leave assertions on in production; only selectively disable those with proven, critical performance impact.
- Using Assertions for Error Handling: Checking recoverable or expected conditions (like user input) with assertions conflates bugs with runtime errors and can crash on legitimate input. Fix: Use assertions only for impossible/invariant conditions; use real error handling for expected failure modes.
- Side-Effect Assertions (Heisenbug): Placing calls with side effects (e.g., iterator.nextElement()) inside assertion conditions causes the assertion itself to mutate program state, creating new bugs. Fix: Extract the value to a variable first, then assert on the variable.
- Asserting Without Cleanup: Letting assertion failure call exit() directly without freeing resources or notifying error handlers. Fix: Write custom assertion handlers that perform cleanup, throw exceptions, or longjmp to an exit point before termination.

## When To Apply

Load this page when:

- Use this when you are about to write a comment like 'this pointer will never be null' — convert it to an assert(ptr != NULL) instead.
- Use this when implementing an algorithm with invariants (e.g., a sort) that should hold at every step — add post-condition assertions to verify the invariant.
- Use this when reviewing generated code before shipping to production — check that assertions have not been disabled or stripped by build configuration.
- Use this when writing a condition check inside an assert expression — verify the expression has no side effects that would alter iterator state, counters, or shared variables.
- Use this when you make an assumption about numeric ranges (e.g., count >= 0, index < array_length) — assert the assumption explicitly at the point of use.
- Use this when deciding whether to remove assertions for a performance-sensitive release — only disable the specific, profiled assertions causing overhead; leave all others active.
- Use this when a function receives parameters that 'should always' meet certain constraints — assert those constraints at the function entry point.

## Concrete Examples

- C function writeString asserts that the char* string parameter is not NULL before proceeding.
- Post-sort verification loop asserting sorted[i] <= sorted[i+1] for all adjacent elements.
- Java iterator loop where Test.ASSERT(iter.nextElement() != null) incorrectly advances the iterator as a side effect, causing half the elements to be skipped.
- Anti-example of using assert to validate user input (asserting ch == 'Y' || ch == 'N' after getchar), which is flagged as a bad idea.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Assertive Programming**

An LLM coding agent is especially prone to silently encoding optimistic assumptions — generating code that 'looks right' for the happy path without ever asserting invariants, because training data skews toward clean, working examples. Unlike a human who might remember a design assumption days later, an agent has no persistent memory across generation steps, so unasserted assumptions are permanently invisible. Assertive programming disciplines an agent to externalize every assumption as executable code at the moment of generation, making implicit beliefs machine-checkable rather than lost in context.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
