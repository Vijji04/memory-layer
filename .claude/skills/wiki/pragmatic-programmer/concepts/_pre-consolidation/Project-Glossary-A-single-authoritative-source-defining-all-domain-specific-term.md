---
title: Project Glossary: A single authoritative source defining all domain-specific terms to prevent name collisions and vocabulary drift between users and developers
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/36-The-Requirements-Pit.json]
contributing_chapters: ["36. The Requirements Pit"]
confidence: high
---

# Project Glossary: A single authoritative source defining all domain-specific terms to prevent name collisions and vocabulary drift between users and developers

> From chapter: *36. The Requirements Pit*

## Core Principle

Requirements are not pre-formed artifacts to collect but deeply buried truths that must be excavated from assumptions, policy, and politics. The core discipline is separating invariant needs from mutable business rules, avoiding overspecification into design or UI, and tracking all scope changes with their schedule impact. Abstractions (domain concepts, access models) outlast the specific policies and interfaces built on top of them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Gather Requirements—Dig for Them

> Work with a User to Think Like a User

> Abstractions Live Longer than Details

> Use a Project Glossary

> Requirements are not architecture. Requirements are not design, nor are they the user interface. Requirements are need.

> Good requirements documents remain abstract.

> Perfection is achieved, not when there is nothing left to add, but when there is nothing left to take away.

> The key to managing growth of requirements is to point out each new feature's impact on the schedule to the project sponsors.

## Anti-Patterns & Fixes

- RequirementsGathering: Treating requirements as pre-existing artifacts to collect rather than hidden truths buried under assumptions and politics. Fix: Actively dig—immerse yourself in the user's domain, observe actual workflows, and question every stated rule.
- HardcodedPolicy: Encoding current business rules (e.g., 'only supervisors can view records') as absolute requirements baked into logic. Fix: State the invariant requirement generically ('authorized users may access') and move the specific policy to metadata or configuration.
- Overspecification: Letting requirements documents drift into design or UI decisions (list box, gray background, front-end/back-end architecture). Fix: Keep requirements as minimal statements of business need; separate implementation suggestions as non-binding examples.
- RequirementsCreep (Boiled Frog): Accepting 'just one more feature' without tracking cumulative impact. Fix: Log every requirement change with sponsor approval and schedule delta so the fifteenth new feature this month is visible.
- VocabularyAmbiguity: Developers and users using the same word for different things or different words for the same thing. Fix: Maintain a shared project glossary accessible to all stakeholders and enforce consistent usage.
- Y2K-style AbstractionFailure: Automating existing business practices without questioning their embedded assumptions (e.g., two-digit years). Fix: Identify domain abstractions (DATE, CURRENCY) and specify invariant services around them rather than replicating current practice.

## When To Apply

Load this page when:

- Use this when a user or product spec states a requirement as a specific UI element (e.g., 'we need a dropdown') to determine whether the UI is the requirement or merely an example of satisfying the real need.
- Use this when implementing an access control or business rule that could change—separate the policy from the requirement and design for metadata-driven configuration.
- Use this when a spec embeds a domain concept (date, currency, measurement) directly in data formats or logic—extract it into an abstraction with its own services.
- Use this when scope is expanding mid-project to quantify the cumulative schedule and resource impact of each added feature before accepting it.
- Use this when domain terminology is ambiguous or inconsistent across stakeholders—create or consult a project glossary before naming variables, classes, or APIs.
- Use this when generating code from a spec that mixes requirements, policy, and design—decompose them before producing any implementation.
- Use this when producing or consuming a requirements document to verify that each statement is a need, not an architecture or UI decision.

## Concrete Examples

- Employee records access: 'Only supervisors and HR may view records' is policy; 'only authorized users may access' is the requirement—the former leads to hardcoded checks, the latter to a configurable access control system.
- Loan term selection: 'The system must let you choose a loan term' is a requirement; 'we need a list box' may or may not be, depending on whether the UI element is essential or merely illustrative.
- Brian Eno's mixing board (Wired, Jan 1999): A technically comprehensive mixer that failed because its interface ignored recording engineers' tactile, intuitive workflow—demonstrating that interface requirements must reflect existing skill sets.
- Y2K two-digit year: Analysts automated existing business practice without abstracting a DATE type, propagating a policy shortcut into an architectural flaw that violated DRY and failed to see beyond current practice.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**36. The Requirements Pit**

An LLM coding agent is especially prone to conflating policy with requirements because it pattern-matches on literal spec language—if a spec says 'only managers can delete records,' the agent will likely emit a hardcoded role check rather than a metadata-driven permission system. Agents also have no mechanism to push back on overspecified requirements (UI prescriptions, architectural mandates) and will faithfully implement them as constraints, baking in fragility. By explicitly decomposing inputs into requirement/policy/implementation layers before generating code, an agent avoids producing logic that is correct for today's policy but wrong for tomorrow's.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
