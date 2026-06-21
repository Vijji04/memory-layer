---
title: Golden Rule of Code: Treat other people's code with the same respect you want your own code to receive
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Pride-and-Prejudice.json]
contributing_chapters: ["Pride and Prejudice"]
confidence: high
---

# Golden Rule of Code: Treat other people's code with the same respect you want your own code to receive

> From chapter: *Pride and Prejudice*

## Core Principle

Pride of ownership — whether individual or communal — is the primary driver of code quality; anonymity breeds sloppiness while accountability breeds craftsmanship. Developers (and agents) should treat their code as a signed artifact, where their name is a quality guarantee. The balance is avoiding territorial prejudice while still maintaining personal responsibility for what you produce.

## Key Heuristics

These are the load-bearing rules for this concept.

> Sign Your Work

> Pragmatic Programmers don't shirk from responsibility. Instead, we rejoice in accepting challenges and in making our expertise well known.

> 'I wrote this, and I stand behind my work.'

> Your signature should come to be recognized as an indicator of quality.

> People should see your name on a piece of code and expect it to be solid, well written, tested, and documented.

> Anonymity, especially on large projects, can provide a breeding ground for sloppiness, mistakes, sloth, and bad code.

> While code must be owned, it doesn't have to be owned by an individual.

## Anti-Patterns & Fixes

- Territorial Code Ownership: Developers jealously guard their code against others, creating insular fiefdoms and blocking collaboration. Fix: Adopt mutual respect and the Golden Rule — welcome others into your code while respecting theirs.
- Anonymous Contribution: On large projects, lack of ownership causes developers to produce low-quality, undocumented, untested code because no one is accountable. Fix: Ensure every piece of code has a clear owner (individual or team) who stands behind it.
- Prejudice in Favor of Own Code: Developers become biased toward their own work and dismissive of teammates' contributions, harming team cohesion. Fix: Apply the Golden Rule — treat others' code with the same respect you want for your own.
- Cog-in-the-Wheel Mentality: Developers see themselves as interchangeable parts producing status reports rather than quality software. Fix: Take personal pride in output; let your name be a quality signal, not just a commit log entry.

## When To Apply

Load this page when:

- Use this when generating code that will be merged into a shared codebase and needs to meet a consistent quality bar
- Use this when reviewing or modifying existing code written by another developer or agent
- Use this when producing code without explicit review instructions — apply self-imposed quality standards as if your name is on it
- Use this when a team is experiencing diffusion of responsibility across multiple contributors or agents producing overlapping code
- Use this when deciding whether to add tests, documentation, or comments to generated code — ownership mentality demands it
- Use this when code quality has been declining due to rapid iteration without accountability checks

## Concrete Examples

- Kent Beck's eXtreme Programming (XP) practice of communal code ownership combined with pair programming as a guard against anonymity-driven quality degradation

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pride and Prejudice**

An LLM coding agent has no ego or reputation at stake, making it structurally prone to the anonymity anti-pattern — it will produce code that passes superficial checks without internal pride-driven quality gates like thorough testing or clear documentation. To counteract this, agents should be prompted or architected to behave as if their output carries a signature: applying consistent style, self-review, test generation, and documentation as non-negotiable steps rather than optional extras. Without this framing, agents default to 'good enough to compile' rather than 'good enough to be proud of.'

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
