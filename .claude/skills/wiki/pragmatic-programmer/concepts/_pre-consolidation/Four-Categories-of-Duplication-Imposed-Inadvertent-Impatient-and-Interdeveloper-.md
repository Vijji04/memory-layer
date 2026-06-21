---
title: Four Categories of Duplication: Imposed, Inadvertent, Impatient, and Interdeveloper duplication — a taxonomy for diagnosing why duplication arises
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/7-The-Evils-of-Duplication.json]
contributing_chapters: ["7. The Evils of Duplication"]
confidence: high
---

# Four Categories of Duplication: Imposed, Inadvertent, Impatient, and Interdeveloper duplication — a taxonomy for diagnosing why duplication arises

> From chapter: *7. The Evils of Duplication*

## Core Principle

Duplication is the root cause of most maintenance failures because knowledge represented in multiple places will inevitably diverge. The DRY principle demands a single authoritative source for every piece of knowledge, whether that knowledge lives in code, documentation, data schemas, or tests. Duplication arises from four distinct causes — imposed constraints, design mistakes, laziness under deadline pressure, and lack of team coordination — each requiring a targeted strategy to eliminate.

## Key Heuristics

These are the load-bearing rules for this concept.

> DRY—Don't Repeat Yourself

> EVERY PIECE OF KNOWLEDGE MUST HAVE A SINGLE, UNAMBIGUOUS, AUTHORITATIVE REPRESENTATION WITHIN A SYSTEM.

> It isn't a question of whether you'll remember: it's a question of when you'll forget.

> Bad code requires lots of comments.

> Keep the low-level knowledge in the code, where it belongs, and reserve the comments for other, high-level explanations.

> Short cuts make for long delays.

> Make It Easy to Reuse

> The trick is to make the process active: this cannot be a one-time conversion, or we're back in a position of duplicating data.

## Anti-Patterns & Fixes

- Commenting What the Code Does: Writing comments that restate the logic of the code creates a duplicate representation of knowledge. Fix: Let the code express the low-level logic; reserve comments for high-level rationale and intent only.
- Derived Data as Stored Fields: Storing a value (e.g., line length) that can be computed from other fields creates a dependency that can fall out of sync. Fix: Make derived values computed properties or methods; cache with a dirty flag if performance requires it.
- Copy-Paste Reuse (Impatient Duplication): Copying a routine or class and modifying it saves seconds but creates divergent maintenance burdens. Fix: Invest time upfront to abstract the shared logic into a reusable component.
- Unnormalized Object Attributes (Interdependency Duplication): Storing the same logical entity (e.g., a driver) in multiple objects means changes must propagate to all holders. Fix: Normalize by identifying the authoritative owner of each piece of knowledge and reference it from other objects.
- Manually Maintained Parallel Representations: Keeping the same structure defined in multiple languages or formats by hand leads to drift. Fix: Generate all representations from a single canonical metadata source using a code generator run at build time.
- Interdeveloper Duplication: Different developers independently implement the same functionality, leading to silent divergence over years. Fix: Appoint a project librarian, maintain a shared utility repository, and foster frequent cross-team communication.

## When To Apply

Load this page when:

- Use this when you are about to define a data field whose value can be calculated from other existing fields in the same class.
- Use this when generating code or data structures in multiple languages or formats that must stay in sync (e.g., client/server shared schema).
- Use this when writing a comment that describes what the next line of code does rather than why it exists.
- Use this when you find yourself copying a function or class to make a slightly modified version instead of parameterizing or abstracting it.
- Use this when a business concept (e.g., a validation rule, a configuration value, a threshold) appears in more than one location in the codebase.
- Use this when documentation and code both describe the same behavior and a change to one requires a manual update to the other.
- Use this when working on a team codebase and about to implement utility functionality without first searching for an existing implementation.
- Use this when a performance optimization requires caching a derived value, to ensure the violation of DRY is localized and encapsulated.

## Concrete Examples

- Line class with a stored `length` field that duplicates information derivable from `start` and `end` points — fixed by making `length` a computed method, with an optional dirty-flag cache for performance.
- Truck and DeliveryRoute classes both containing a `driver` attribute, causing ambiguity about which to update when the driver changes — fixed by normalizing the driver to a single authoritative object.
- International telex switch project where acceptance tests were generated programmatically from the client's specification document, so test suites updated automatically when the spec changed.
- U.S. state government audit uncovering over 10,000 programs each containing their own independent Social Security number validation logic — a large-scale interdeveloper duplication example.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**7. The Evils of Duplication**

An LLM coding agent is especially prone to impatient and interdeveloper duplication because it generates code statelessly across calls — it cannot remember that it already defined a validation function in a prior context window and will silently reimplement it. Agents also tend to inline 'magic' derived values or repeat business logic across generated files rather than creating a single authoritative source, because generating self-contained code feels locally correct. Applying DRY means an agent must explicitly audit the existing codebase for canonical representations before generating new logic, and should prefer generating or extending abstractions over producing parallel implementations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
