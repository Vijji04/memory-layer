---
title: Architectural ISP: The dependency-on-excess-baggage problem scales beyond code to system and framework dependencies, causing cascading redeployment and failure risk
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-10-ISP-The-Interface-Segregation-Principle.json]
contributing_chapters: ["Chapter 10: ISP: The Interface Segregation Principle"]
confidence: high
---

# Architectural ISP: The dependency-on-excess-baggage problem scales beyond code to system and framework dependencies, causing cascading redeployment and failure risk

> From chapter: *Chapter 10: ISP: The Interface Segregation Principle*

## Core Principle

The Interface Segregation Principle states that no user should be forced to depend on methods or features it does not use; splitting interfaces by consumer role eliminates unnecessary recompilation, redeployment, and failure propagation. While most visible in statically typed languages at the code level, the principle extends architecturally: depending on a framework or module that carries unneeded baggage creates hidden coupling that can destabilize an entire system. The core lesson is that excess dependency — at any level — is a liability, not a neutral cost.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is harmful to depend on modules that contain more than you need.

> Depending on something that carries baggage that you don't need can cause you troubles that you didn't expect.

> A change to the source code of op2 in OPS will force User1 to be recompiled and redeployed, even though nothing that it cared about has actually changed.

> Dynamically typed languages create systems that are more flexible and less tightly coupled than statically typed languages.

> The ISP is not merely a language issue — it is an architecture issue.

## Anti-Patterns & Fixes

- Fat Interface Dependency: A user depends on a class or module that contains operations it never calls, causing unnecessary recompilation and redeployment when unrelated operations change. Fix: Segregate the interface into smaller, user-specific interfaces so each user depends only on what it actually uses.
- Framework-Database Transitive Baggage: A system S depends on framework F which is bound to database D; changes or failures in unused features of D propagate to F and S. Fix: Prefer frameworks that are not coupled to specific databases, or isolate the dependency behind an abstraction layer so S does not transitively depend on D.
- Monolithic Module Inclusion: Importing or including a large module to access one feature drags in all other features as source-code dependencies. Fix: Break the module into focused units and import only the unit needed.

## When To Apply

Load this page when:

- Use this when designing a class or module that is consumed by multiple distinct callers that each use only a subset of its methods.
- Use this when a change to one part of a shared class causes unrelated consumers to be recompiled, retested, or redeployed.
- Use this when selecting a third-party framework and evaluating whether it drags in unneeded infrastructure dependencies (e.g., a specific database or messaging system).
- Use this when a downstream component is failing or being forced to redeploy due to changes in an upstream module it does not directly use.
- Use this when generating or scaffolding interfaces in statically typed languages (Java, C#, TypeScript) where unused method dependencies are enforced at compile time.
- Use this when a system S depends on framework F and you need to assess whether transitive dependencies of F could cause unexpected failures in S.

## Concrete Examples

- OPS class with op1, op2, op3 used by User1, User2, User3 respectively — User1 is forced to depend on op2 and op3 despite never calling them, solved by splitting into U1Ops, U2Ops, U3Ops interfaces.
- System S depending on framework F which is bound to database D — unused features in D can force redeployment of F and S, and failures in D can cascade to S.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 10: ISP: The Interface Segregation Principle**

An LLM coding agent generating code tends to produce large, convenient classes or import broad modules by default because it optimizes for completeness and minimal output, inadvertently creating fat interfaces that couple unrelated consumers. This is especially dangerous in statically typed codebases where the agent may generate a single service or facade class exposing all operations, causing every consumer to recompile on any change. Applying ISP explicitly in agent prompts and code-review steps forces the agent to decompose generated interfaces by caller role, preventing silent transitive dependency bloat across generated codebases.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
