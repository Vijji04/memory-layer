---
title: Crash Early Principle: Terminate a program immediately upon detecting an impossible or unexpected state, before corrupted data or logic propagates further damage
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Dead-Programs-Tell-No-Lies.json]
contributing_chapters: ["Dead Programs Tell No Lies"]
confidence: high
---

# Crash Early Principle: Terminate a program immediately upon detecting an impossible or unexpected state, before corrupted data or logic propagates further damage

> From chapter: *Dead Programs Tell No Lies*

## Core Principle

When a program encounters an error—even one that 'should never happen'—it means something has already gone seriously wrong and the program's state is suspect. The correct response is to crash immediately rather than continue, because a dead program causes far less damage than a crippled one writing corrupted data or triggering cascading failures. Pragmatic Programmers treat every error as meaningful information and build in explicit checks, default clauses, and early termination to surface impossible conditions the moment they occur.

## Key Heuristics

These are the load-bearing rules for this concept.

> Crash Early

> A dead program normally does a lot less damage than a crippled one.

> All errors give you information.

> If there is an error, something very, very bad has happened.

> When your code discovers that something that was supposed to be impossible just happened, your program is no longer viable.

> Each and every case/switch statement needs to have a default clause—we want to know when the 'impossible' has happened.

## Anti-Patterns & Fixes

- It-Can't-Happen Mentality: Ignoring error returns or skipping checks because the failure seems implausible under normal conditions. This allows corrupted state to propagate silently. Fix: Treat every unexpected return as a critical signal and halt or raise immediately.
- Swallowing Exceptions Silently: Catching exceptions or errors and continuing execution without addressing the underlying cause. Fix: Let unexpected exceptions percolate to the top level or explicitly abort with diagnostic information.
- Missing Default Case: Omitting a default clause in switch/case statements, allowing invalid selector values to pass through silently. Fix: Always include a default clause that triggers an abort or error when reached.
- Continuing After Corruption: Allowing a program to keep running after detecting an impossible state, risking writing corrupted data to databases or triggering dangerous repeated actions. Fix: Terminate as soon as the impossible condition is detected, after releasing claimed resources and logging state.

## When To Apply

Load this page when:

- Use this when writing code that calls a library or system function whose failure would indicate upstream memory corruption or logic errors.
- Use this when implementing switch/case logic where only a known set of values should ever be valid.
- Use this when a resource allocation (malloc, file open, DB connection) fails in a context where failure was deemed impossible by design.
- Use this when generating error-handling code and deciding whether to recover, retry, or abort after an unexpected condition.
- Use this when a downstream operation (file close, write, transaction commit) fails and the calling code was not checking its return value.
- Use this when building safety-critical or data-critical systems where silent data corruption is worse than a visible crash.
- Use this when wrapping C-style APIs or other libraries that return error codes rather than throwing exceptions.

## Concrete Examples

- A stray pointer overwrites a file handle; the next read() call catches the corruption rather than the original bad write.
- A buffer overrun corrupts a memory counter; a subsequent malloc() fails, surfacing the earlier error.
- A logic error corrupts a switch/case selector so it no longer holds expected values 1, 2, or 3; the default clause catches it.
- A C macro CHECK() wraps stat('/tmp', &stat_buff) and calls ut_abort() with file, line, and expected vs. actual return codes if it fails.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Dead Programs Tell No Lies**

An LLM coding agent is especially prone to generating plausible-looking code that omits error checks on 'obviously safe' calls—because training data is full of such shortcuts and the agent has no runtime feedback to notice the omission. Without the Crash Early principle, agent-generated code may silently propagate corrupted state across many generated functions before any symptom surfaces, making the root cause nearly untraceable. Agents should be configured to always emit explicit error checks with abort/raise behavior on unexpected returns, and to always include default cases in generated switch statements.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
