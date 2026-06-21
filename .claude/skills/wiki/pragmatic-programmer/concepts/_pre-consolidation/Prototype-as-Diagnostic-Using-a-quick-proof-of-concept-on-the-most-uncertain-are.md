---
title: Prototype-as-Diagnostic: Using a quick proof-of-concept on the most uncertain area to distinguish genuine blocking concerns from mere procrastination — boredom during prototyping signals procrastination; revelation signals a real problem
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Not-Until-Youre-Ready.json]
contributing_chapters: ["Not Until You're Ready"]
confidence: high
---

# Prototype-as-Diagnostic: Using a quick proof-of-concept on the most uncertain area to distinguish genuine blocking concerns from mere procrastination — boredom during prototyping signals procrastination; revelation signals a real problem

> From chapter: *Not Until You're Ready*

## Core Principle

Experienced developers have trained subconscious instincts that manifest as nagging doubt before a flawed start; these signals should be respected rather than overridden. The practical technique for distinguishing genuine blocking concerns from procrastination is to prototype the most uncertain area: boredom signals procrastination, while a moment of revelation signals a real foundational problem. The goal is to surface wrong premises cheaply before committing to full development.

## Key Heuristics

These are the load-bearing rules for this concept.

> Listen to Nagging Doubts—Start When You're Ready

> He who hesitates is sometimes saved.

> If you sit down to start typing and there's some nagging doubt in your mind, heed it.

> Software development is still not a science. Let your instincts contribute to your performance.

> When you feel a nagging doubt, or experience some reluctance when faced with a task, heed it.

> The last thing you want is to find yourself several weeks into serious development before remembering that you started out writing a prototype.

## Anti-Patterns & Fixes

- BlindStarting: Ignoring nagging doubts and diving into full development, causing wasted effort when a flawed premise is discovered late. Fix: Prototype the uncertain area first to surface fundamental issues early.
- ProcastinationMisread: Treating all hesitation as laziness and forcing a start, missing valid instinctual warnings. Fix: Use the prototype test — if you feel bored quickly, it was procrastination; if you hit a revelation, it was a real concern.
- PrototypeDrift: Beginning a prototype to investigate unease but drifting into treating it as real development, wasting weeks. Fix: Explicitly label and time-box prototypes; abandon them intentionally once the diagnostic purpose is served.
- AnnouncingUnease Without Evidence: Declaring 'I don't feel right about starting' with no tangible output, which is politically unacceptable and unproductive. Fix: Channel the unease into a concrete prototype that can surface actual problems.

## When To Apply

Load this page when:

- Use this when you are about to generate a large implementation but something about the requirements feels underspecified or contradictory.
- Use this when asked to scaffold a new module or project and the architecture or domain model is not yet clear.
- Use this when a task feels straightforward but edge cases or constraints keep surfacing during planning, suggesting a hidden premise is wrong.
- Use this when you have been given a specification and you cannot immediately identify a clean decomposition or starting point.
- Use this when the scope of a request is ambiguous and starting full implementation risks building in the wrong direction for many steps.
- Use this when you feel pressure to produce output quickly but lack confidence that the foundational approach is correct.

## Concrete Examples

- A diver on the high-board waiting for the perfect moment to jump, illustrating readiness calibration before committing.
- A conductor holding raised arms before the orchestra, waiting to sense the right moment to begin the piece.
- 'Inner tennis' coaching: hitting balls while verbalizing where they land relative to a target chair, training subconscious reflexes without conscious understanding — used as an analogy for accumulated developer instinct.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Not Until You're Ready**

An LLM agent lacks the human experience of accumulated instinct but can simulate readiness calibration by explicitly checking for specification gaps, contradictory constraints, or unclear success criteria before generating code — treating these as programmatic 'nagging doubts.' The key agent failure mode this prevents is confident hallucination: agents tend to fill underspecified gaps with plausible-sounding assumptions and proceed at full speed, producing large amounts of coherent but fundamentally wrong code. Applying the prototype-as-diagnostic pattern, an agent should generate a minimal proof-of-concept or ask targeted clarifying questions before committing to a full implementation path.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
