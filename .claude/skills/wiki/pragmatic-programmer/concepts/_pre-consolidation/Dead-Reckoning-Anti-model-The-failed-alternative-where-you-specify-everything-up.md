---
title: Dead Reckoning (Anti-model): The failed alternative where you specify everything upfront, calculate the correct solution once, then fire and hope without feedback
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Tracer-Bullets.json]
contributing_chapters: ["Tracer Bullets"]
confidence: high
---

# Dead Reckoning (Anti-model): The failed alternative where you specify everything upfront, calculate the correct solution once, then fire and hope without feedback

> From chapter: *Tracer Bullets*

## Core Principle

Tracer Bullet Development is an incremental strategy for navigating uncertainty: build the thinnest possible slice of real, production-quality code that connects all system components end-to-end, then use that working skeleton as a feedback mechanism and growth scaffold. It differs from prototyping in that tracer code is kept and extended, not discarded. The approach trades upfront completeness for continuous feedback, lower inertia, and always-demonstrable progress.

## Key Heuristics

These are the load-bearing rules for this concept.

> Use Tracer Bullets to Find the Target

> Tracer code is not disposable: you write it for keeps.

> Prototyping generates disposable code. Tracer code is lean but complete, and forms part of the skeleton of the final system.

> Think of prototyping as the reconnaissance and intelligence gathering that takes place before a single tracer bullet is fired.

> A small body of code has low inertia—it is easy and quick to change.

> Ready, fire, aim

> Once you have achieved an end-to-end connection among the components of your system, you can check how close to the target you are, adjusting if necessary.

## Anti-Patterns & Fixes

- Big-Bang Integration: Coding all modules in isolation then combining them at the end, resulting in no testable system until completion. Fix: Use tracer code to maintain a working end-to-end system at all times, integrating continuously.
- Specify-to-Death (Dead Reckoning): Producing exhaustive specifications upfront to eliminate unknowns before writing any code, leaving no mechanism for feedback or course correction. Fix: Build a tracer slice early to get real feedback from users and the real environment.
- Prototype Confusion: Treating tracer code as throwaway prototype code, or vice versa, leading to either discarding useful architectural skeletons or keeping low-quality exploratory code in production. Fix: Clearly distinguish intent — prototypes explore and are discarded; tracer code is production-quality and retained.
- 95%-Complete Monolith: Reporting large monolithic code blocks as nearly done for weeks with no demonstrable progress. Fix: Use tracer development to tackle discrete use cases one by one, making progress visible and measurable.

## When To Apply

Load this page when:

- Use this when starting a project with vague or uncertain user requirements where no similar system exists for reference.
- Use this when integrating unfamiliar algorithms, libraries, languages, or frameworks where unknowns are high.
- Use this when multiple architectural layers (UI, middleware, database) must communicate and no integration has been validated yet.
- Use this when stakeholders or sponsors need periodic demos and you need something always-demonstrable.
- Use this when the project timeline is long enough that environmental or requirement changes are likely before completion.
- Use this when team members need a shared structural skeleton to hang their individual components on.
- Use this when you need to distinguish whether a planned architecture actually works before investing in full implementation.

## Concrete Examples

- Complex client-server database marketing project with temporal queries: built a tracer connecting Object Pascal GUI, C libraries, Lisp-like query storage, and SQL generation — initially only capable of listing all rows in a table, but proving end-to-end connectivity.
- Container packing application: tracer used a trivial first-come-first-served packing algorithm with a simple working UI to validate full system integration, versus prototypes that explored UI layout or packing algorithms in isolation and were discarded.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Tracer Bullets**

An LLM coding agent is prone to generating large, complete-looking modules in isolation without verifying that they integrate — mimicking the dead-reckoning anti-pattern at high speed. Tracer Bullet thinking forces the agent to first produce a thin, end-to-end slice that actually runs and connects all layers before expanding functionality, preventing the failure mode where hundreds of lines of plausible-but-never-integrated code are delivered. It also gives the agent a concrete feedback loop: if the tracer slice fails at runtime, the agent gets a real error signal rather than hallucinating correctness from static analysis of its own output.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
