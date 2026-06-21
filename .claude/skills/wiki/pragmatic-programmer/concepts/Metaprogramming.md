---
title: Metaprogramming
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 3 pages
---

# Metaprogramming

> Consolidated from 3 related concept pages.

---

## Cooperative Configuration Systems that configure each other at runtime adapting

## Core Principle

Metaprogramming is the practice of moving volatile details — business rules, technology choices, behavioral parameters — out of compiled code and into external metadata that can be changed without recompilation. The core principle is to code the general-purpose abstraction and configure the specifics, enabling systems to adapt to change without touching the codebase. This decoupling reduces bug risk, enables runtime reconfiguration, and allows a single engine to serve multiple contexts.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 37: Configure, Don't Integrate

> Tip 38: Put Abstractions in Code, Details in Metadata

> Program for the general case, and put the specifics somewhere else—outside the compiled code base.

> We want to defer definition of most details until the last moment, and leave the details as soft—as easy to change—as we can.

> Think declaratively (specifying what is to be done, not how) and create highly dynamic and adaptable programs.

> No amount of genius can overcome a preoccupation with detail.

> Without metadata, your code is not as adaptable or flexible as it could be.

## Anti-Patterns & Fixes

- HardcodedBusinessLogic: Embedding business rules, policies, and thresholds directly in code means every rule change requires recompilation and risks introducing bugs. Fix: Encode rules in external configuration, a rule-based system, or a mini-language that can be changed without touching compiled code.
- StartupOnlyConfiguration: Reading configuration only at startup forces application restarts to apply any change. Fix: Design long-running processes to reload and apply metadata while running.
- IntegratingInsteadOfConfiguring: Making technology choices (database engine, middleware, UI style) hard-wired via integration rather than configuration options. Fix: Implement these as metadata-driven configuration options switchable at runtime.
- Dodo-Code: Writing inflexible code that cannot adapt to environmental or business changes, leading to project failure. Fix: Extract all volatile details into metadata so the core engine remains stable while behavior evolves.

## When To Apply

Load this page when:

- Use this when business rules or policies are likely to change frequently and embedding them in code would require repeated recompilation and deployment.
- Use this when the same application logic needs to run in multiple different configurations or for multiple clients with different requirements.
- Use this when choosing between technology options (database, middleware, UI style) that may need to be swapped without code changes.
- Use this when implementing complex, changing workflow logic that would otherwise require constant code edits.
- Use this when building a long-running server process that must remain available while configuration updates are applied.
- Use this when a system needs to adapt itself to its runtime environment, such as available hardware or installed library versions.

## Concrete Examples

- Netscape browser preferences evolving from simple key/value pairs (SHOW_TOOLBAR: False) in Version 3 to JavaScript-style expressions (user_pref(...)) in Version 4.
- Enterprise Java Beans (EJB): transaction handling, thread allocation, and load balancing are all specified as metadata in a deployment descriptor, not in the bean code itself.
- A purchasing application where supplier type definitions and payment time periods (45 days vs. 90 days) are stored as configurable metadata rather than hardcoded values.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**27. Metaprogramming**

An LLM coding agent defaults to generating self-contained, fully specified code with constants, thresholds, and logic baked in — because it optimizes for producing working code in one pass rather than designing for future change. This produces brittle, Dodo-code architectures where every business rule change requires the agent to regenerate and re-review large code sections, compounding hallucination and regression risk. Applying this chapter, an agent should instead generate a thin engine with explicit configuration hooks and externalize all volatile details to metadata files, reducing the surface area that must be regenerated when requirements shift.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Dynamic Configuration Moving runtime behavior algorithms and business rules out

## Core Principle

Metaprogramming is the practice of moving volatile details — business rules, technology choices, behavioral parameters — out of compiled code and into external metadata that can be changed without recompilation. The core principle is to code the general-purpose abstraction and configure the specifics, enabling systems to adapt to change without touching the codebase. This decoupling reduces bug risk, enables runtime reconfiguration, and allows a single engine to serve multiple contexts.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 37: Configure, Don't Integrate

> Tip 38: Put Abstractions in Code, Details in Metadata

> Program for the general case, and put the specifics somewhere else—outside the compiled code base.

> We want to defer definition of most details until the last moment, and leave the details as soft—as easy to change—as we can.

> Think declaratively (specifying what is to be done, not how) and create highly dynamic and adaptable programs.

> No amount of genius can overcome a preoccupation with detail.

> Without metadata, your code is not as adaptable or flexible as it could be.

## Anti-Patterns & Fixes

- HardcodedBusinessLogic: Embedding business rules, policies, and thresholds directly in code means every rule change requires recompilation and risks introducing bugs. Fix: Encode rules in external configuration, a rule-based system, or a mini-language that can be changed without touching compiled code.
- StartupOnlyConfiguration: Reading configuration only at startup forces application restarts to apply any change. Fix: Design long-running processes to reload and apply metadata while running.
- IntegratingInsteadOfConfiguring: Making technology choices (database engine, middleware, UI style) hard-wired via integration rather than configuration options. Fix: Implement these as metadata-driven configuration options switchable at runtime.
- Dodo-Code: Writing inflexible code that cannot adapt to environmental or business changes, leading to project failure. Fix: Extract all volatile details into metadata so the core engine remains stable while behavior evolves.

## When To Apply

Load this page when:

- Use this when business rules or policies are likely to change frequently and embedding them in code would require repeated recompilation and deployment.
- Use this when the same application logic needs to run in multiple different configurations or for multiple clients with different requirements.
- Use this when choosing between technology options (database, middleware, UI style) that may need to be swapped without code changes.
- Use this when implementing complex, changing workflow logic that would otherwise require constant code edits.
- Use this when building a long-running server process that must remain available while configuration updates are applied.
- Use this when a system needs to adapt itself to its runtime environment, such as available hardware or installed library versions.

## Concrete Examples

- Netscape browser preferences evolving from simple key/value pairs (SHOW_TOOLBAR: False) in Version 3 to JavaScript-style expressions (user_pref(...)) in Version 4.
- Enterprise Java Beans (EJB): transaction handling, thread allocation, and load balancing are all specified as metadata in a deployment descriptor, not in the bean code itself.
- A purchasing application where supplier type definitions and payment time periods (45 days vs. 90 days) are stored as configurable metadata rather than hardcoded values.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**27. Metaprogramming**

An LLM coding agent defaults to generating self-contained, fully specified code with constants, thresholds, and logic baked in — because it optimizes for producing working code in one pass rather than designing for future change. This produces brittle, Dodo-code architectures where every business rule change requires the agent to regenerate and re-review large code sections, compounding hallucination and regression risk. Applying this chapter, an agent should instead generate a thin engine with explicit configuration hooks and externalize all volatile details to metadata files, reducing the surface area that must be regenerated when requirements shift.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Metadata Driven Applications Architecting a general purpose engine whose specifi

## Core Principle

Metaprogramming is the practice of moving volatile details — business rules, technology choices, behavioral parameters — out of compiled code and into external metadata that can be changed without recompilation. The core principle is to code the general-purpose abstraction and configure the specifics, enabling systems to adapt to change without touching the codebase. This decoupling reduces bug risk, enables runtime reconfiguration, and allows a single engine to serve multiple contexts.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 37: Configure, Don't Integrate

> Tip 38: Put Abstractions in Code, Details in Metadata

> Program for the general case, and put the specifics somewhere else—outside the compiled code base.

> We want to defer definition of most details until the last moment, and leave the details as soft—as easy to change—as we can.

> Think declaratively (specifying what is to be done, not how) and create highly dynamic and adaptable programs.

> No amount of genius can overcome a preoccupation with detail.

> Without metadata, your code is not as adaptable or flexible as it could be.

## Anti-Patterns & Fixes

- HardcodedBusinessLogic: Embedding business rules, policies, and thresholds directly in code means every rule change requires recompilation and risks introducing bugs. Fix: Encode rules in external configuration, a rule-based system, or a mini-language that can be changed without touching compiled code.
- StartupOnlyConfiguration: Reading configuration only at startup forces application restarts to apply any change. Fix: Design long-running processes to reload and apply metadata while running.
- IntegratingInsteadOfConfiguring: Making technology choices (database engine, middleware, UI style) hard-wired via integration rather than configuration options. Fix: Implement these as metadata-driven configuration options switchable at runtime.
- Dodo-Code: Writing inflexible code that cannot adapt to environmental or business changes, leading to project failure. Fix: Extract all volatile details into metadata so the core engine remains stable while behavior evolves.

## When To Apply

Load this page when:

- Use this when business rules or policies are likely to change frequently and embedding them in code would require repeated recompilation and deployment.
- Use this when the same application logic needs to run in multiple different configurations or for multiple clients with different requirements.
- Use this when choosing between technology options (database, middleware, UI style) that may need to be swapped without code changes.
- Use this when implementing complex, changing workflow logic that would otherwise require constant code edits.
- Use this when building a long-running server process that must remain available while configuration updates are applied.
- Use this when a system needs to adapt itself to its runtime environment, such as available hardware or installed library versions.

## Concrete Examples

- Netscape browser preferences evolving from simple key/value pairs (SHOW_TOOLBAR: False) in Version 3 to JavaScript-style expressions (user_pref(...)) in Version 4.
- Enterprise Java Beans (EJB): transaction handling, thread allocation, and load balancing are all specified as metadata in a deployment descriptor, not in the bean code itself.
- A purchasing application where supplier type definitions and payment time periods (45 days vs. 90 days) are stored as configurable metadata rather than hardcoded values.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**27. Metaprogramming**

An LLM coding agent defaults to generating self-contained, fully specified code with constants, thresholds, and logic baked in — because it optimizes for producing working code in one pass rather than designing for future change. This produces brittle, Dodo-code architectures where every business rule change requires the agent to regenerate and re-review large code sections, compounding hallucination and regression risk. Applying this chapter, an agent should instead generate a thin engine with explicit configuration hooks and externalize all volatile details to metadata files, reducing the surface area that must be regenerated when requirements shift.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
