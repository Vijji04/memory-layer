---
title: Test Taxonomy: Six distinct testing types — unit, integration, validation/verification, resource exhaustion, performance, and usability — each targeting different failure modes
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/43-Ruthless-Testing.json]
contributing_chapters: ["43. Ruthless Testing"]
confidence: high
---

# Test Taxonomy: Six distinct testing types — unit, integration, validation/verification, resource exhaustion, performance, and usability — each targeting different failure modes

> From chapter: *43. Ruthless Testing*

## Core Principle

Ruthless Testing argues that automated, adversarial testing starting from the first line of code is the only reliable path to quality — test plans on shelves and manual testing are insufficient substitutes. The chapter defines a taxonomy of six test types, distinguishes state coverage from code coverage, and establishes that every human-discovered bug must become a permanent automated regression test. The core discipline is treating tests as a continuously tightened safety net, not a one-time checkpoint.

## Key Heuristics

These are the load-bearing rules for this concept.

> Test Early. Test Often. Test Automatically.

> Coding Ain't Done 'Til All the Tests Run

> Use Saboteurs to Test Your Testing

> Test State Coverage, Not Code Coverage

> Find Bugs Once

> Once a human tester finds a bug, it should be the last time a human tester finds that bug.

> A good project may well have more test code than production code.

> Tests that run with every build are much more effective than test plans that sit on a shelf.

## Anti-Patterns & Fixes

- Gentle Testing: Developers subconsciously avoid weak spots they know exist, leaving real bugs untested. Fix: Treat testing as adversarial — actively seek out the code's weakest points and stress them deliberately.
- Shelf-Bound Test Plans: Writing elaborate test plans that are rarely executed instead of automated test suites. Fix: Automate test execution and result interpretation so tests run with every build.
- Late Testing: Deferring testing until the end of the project where it gets cut by deadlines. Fix: Write and run tests as soon as any production code exists; adopt 'code a little, test a little'.
- Code Coverage Fixation: Believing 100% line coverage means thorough testing. Fix: Analyze state coverage — identify distinct program states and ensure tests exercise boundary and failure states, not just executed lines.
- Manual Bug Re-Discovery: Relying on human testers to find the same bug category more than once. Fix: After any human-found bug, immediately write an automated regression test that catches it permanently.
- Untested Tests: Assuming test code is correct without verification. Fix: Deliberately introduce the bug the test is meant to catch and confirm the test fails — use a project saboteur role for systematic coverage.

## When To Apply

Load this page when:

- Use this when generating a new function or module — immediately produce corresponding unit tests alongside the production code, not afterward.
- Use this when a bug is reported or discovered — before fixing it, write a failing test that reproduces it, then fix, then confirm the test passes.
- Use this when integrating two subsystems — add integration tests that verify contract compliance between the subsystems, not just internal unit behavior.
- Use this when a function takes multiple numeric or enum parameters — enumerate boundary and failure states (e.g., division by zero, null inputs) beyond simple happy-path coverage.
- Use this when generating code that handles resources (memory, disk, network) — include tests that simulate exhaustion or failure of each resource type.
- Use this when the codebase has no CI or automated test runner — flag this as a critical gap and propose an automated test execution strategy.
- Use this when performance or scalability is a requirement — specify that load/stress tests must be scheduled and run regularly, not just at release.
- Use this when a GUI or interface layer is being built — verify the application logic is decoupled enough to be tested independently of the interface.

## Concrete Examples

- A three-line integer division function `int test(int a, int b) { return a / (a + b); }` has 1,000,000 logical states — 999,999 correct and one divide-by-zero — illustrating that line coverage alone is insufficient.
- A nondeterministic visual simulation that generates different output every run, making bitmap comparison impossible and requiring manual or statistical result interpretation.
- A sort algorithm that slows to a crawl when handed pre-sorted data — exposed only by testing with data in specific statistical orders, not random data alone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**43. Ruthless Testing**

An LLM coding agent is especially prone to the 'gentle testing' anti-pattern because it generates tests based on its model of how the code should work, systematically under-testing edge cases and states it did not reason about during generation. Unlike a human who might accidentally stress a weak path, an agent's tests will mirror its own blind spots — so explicit instructions to generate adversarial, boundary, and failure-state tests are critical. Additionally, agents must be prompted to treat test code as a first-class output equal in volume and rigor to production code, not as an afterthought appended to satisfy a requirement.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
