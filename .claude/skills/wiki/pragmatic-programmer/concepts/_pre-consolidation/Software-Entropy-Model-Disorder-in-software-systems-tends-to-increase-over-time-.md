---
title: Software Entropy Model: Disorder in software systems tends to increase over time, analogous to thermodynamic entropy, and is primarily driven by team psychology and culture rather than technical factors alone
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/2-Software-Entropy.json]
contributing_chapters: ["2. Software Entropy"]
confidence: high
---

# Software Entropy Model: Disorder in software systems tends to increase over time, analogous to thermodynamic entropy, and is primarily driven by team psychology and culture rather than technical factors alone

> From chapter: *2. Software Entropy*

## Core Principle

Software entropy — the tendency of codebases to decay into disorder — is primarily a psychological phenomenon triggered by the first unrepaired defect, which signals abandonment and lowers the threshold for further degradation. The Broken Window Theory prescribes immediate repair or explicit 'boarding up' of every defect to prevent cascading decay. A pristine codebase creates its own protective culture, while a neglected one accelerates rot faster than any technical factor.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Live with Broken Windows

> Don't leave 'broken windows' (bad designs, wrong decisions, or poor code) unrepaired. Fix each one as soon as it is discovered.

> If there is insufficient time to fix it properly, then board it up.

> Neglect accelerates the rot faster than any other factor.

> Don't let entropy win.

> One broken window—a badly designed piece of code, a poor management decision that the team must live with for the duration of the project—is all it takes to start the decline.

> If you find yourself working on a project with quite a few broken windows, it's all too easy to slip into the mindset of 'All the rest of this code is crap, I'll just follow suit.'

## Anti-Patterns & Fixes

- AcceptingBrokenWindows: Leaving bad designs, wrong decisions, or poor code unrepaired causes a psychological cascade where standards collapse and rot accelerates. Fix: Repair immediately; if time is short, 'board it up' with a comment, stub, or placeholder that signals awareness and intent to fix.
- EntropyDefeatism: Believing no one has time to clean up broken glass leads to abandoning quality standards entirely. Fix: Treat each broken window as a discrete, fixable item rather than surrendering to systemic decay.
- FirehoseRecklessness: Introducing additional mess (e.g., hacks, shortcuts) to a previously clean codebase under deadline pressure. Fix: Preserve the existing quality standard even in emergencies, like firefighters rolling out a mat before entering an immaculate house.
- ContagionByContext: Matching the low quality of surrounding code because 'everything is crap anyway.' Fix: Evaluate each contribution independently; do not let existing rot justify new rot.

## When To Apply

Load this page when:

- Use this when discovering a poorly designed function or module while working on an unrelated task — flag or fix it rather than ignoring it.
- Use this when asked to add a feature to a codebase that already contains known technical debt — avoid compounding the debt.
- Use this when generating code under a tight scope constraint and tempted to skip error handling, type hints, or documentation — use a placeholder or TODO rather than omitting entirely.
- Use this when reviewing a pull request or existing code and noticing a naming inconsistency, anti-pattern, or design smell — surface it explicitly.
- Use this when a codebase has inconsistent style or structure and there is pressure to 'just match the existing pattern' — distinguish between adopting conventions versus perpetuating defects.
- Use this when a quick fix or workaround is the only immediate option — ensure it is visibly marked as temporary so it is not treated as permanent.
- Use this when evaluating whether to refactor during a feature addition — the presence of broken windows is a trigger to pause and assess decay risk.

## Concrete Examples

- A building with one broken window left unrepaired leads to littering, graffiti, and eventual structural ruin — the origin of the Broken Window Theory from criminology research [WK82].
- An abandoned car sat untouched for a week, but once one window was broken, it was stripped and overturned within hours.
- Firefighters responding to a fire in an immaculate, antique-filled house stopped to roll out a protective mat before dragging hoses in — preserving quality even during an emergency.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**2. Software Entropy**

An LLM coding agent is particularly susceptible to the 'contagion by context' failure mode: when prompted with or given access to low-quality code, it tends to pattern-match and perpetuate those defects (bad naming, missing error handling, inconsistent style) rather than raising quality. Unlike a human who must consciously decide to cut corners, an agent silently inherits broken windows through in-context learning. Applying this chapter means an agent should explicitly flag detected defects, refuse to propagate anti-patterns even when they dominate the surrounding code, and insert visible markers (TODOs, stubs, comments) when a proper fix is out of scope.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
