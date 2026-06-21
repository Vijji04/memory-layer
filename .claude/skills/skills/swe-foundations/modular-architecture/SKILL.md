---
name: modular-architecture
description: "Use when making dependency management decisions, drawing component boundaries, applying SOLID principles, designing layered architectures, or evaluating whether a structural decision keeps options open vs. locks them in."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [architecture, solid, clean-architecture, boundaries, dependencies, components, swe-foundations]
    category: swe-foundations
    related_skills: [engineering-mindset, production-readiness, distributed-systems, agentic-swe-master]
---

# Modular Architecture & Boundaries

## When to Load

- Use this when a coding agent is about to choose a framework, database, or web server before domain logic exists
- Use this when agent-generated code imports ORM models, HTTP types, or framework objects inside business logic
- Use this when designing module, package, or component boundaries — deciding what belongs where
- Use this when a feature is getting slower to implement over time (productivity asymptote signal)
- Use this when an agent is asked to "just make it work quickly" and is about to skip structural discipline
- Use this when business rules are tangled with I/O, database calls, or HTTP handler code
- Use this when planning a microservices split — evaluating whether services truly decouple teams
- Use this when deciding how to pass data across a boundary (which side owns the data shape)
- Use this when evaluating a full system rewrite vs. incremental improvement
- Use this when an agent is about to couple a use case to a specific presenter, view, or delivery mechanism
- Use this when writing tests that are breaking because of structural coupling to production code
- Use this when team org chart is driving component boundaries

## Core Rules

> The goal of software architecture is to minimize the human resources required to build and maintain the required system.

> The only way to go fast is to go well. Making messes is always slower than staying clean.

> A good architect pretends decisions have not been made, and shapes the system such that those decisions can still be made later.

> Source code dependencies must point only inward, toward higher-level policies. Nothing in an inner circle can know anything about an outer circle.

> Good architects carefully separate details from policy, and decouple the policy from the details so thoroughly that the policy has no knowledge of the details.

> The longer you wait to make a decision, the more information you have with which to make it properly.

> A module should be responsible to one and only one actor — the single source of change that can demand it be modified.

> Components should not be forced to depend on things they don't use (ISP). Depend on stable abstractions, not volatile concrete implementations (DIP).

> Architecture should reveal intent — use cases, features, and actors should be visible in the top-level structure, not the framework choice.

> The web is a detail. The database is a detail. The framework is a detail. Keep them on the outside.

## The Dependency Rule (Most Critical)

All source code dependencies must point inward toward higher-level policy:

  [Entities] <- [Use Cases] <- [Interface Adapters] <- [Frameworks & Drivers]

Violations to catch immediately:
  - Use case importing a database model class
  - Entity method calling an HTTP client
  - Business rule knowing the name of a presenter or view
  - SQL query in a use case layer
  - Framework annotation on a domain object

## SOLID at Architecture Scale

SRP: Group by actor (source of change), not by technical function.
OCP: Extend behavior by adding new components behind existing interfaces, not by modifying existing ones.
LSP: Subtypes must be fully substitutable. When they aren't, isolate dispatch behind a factory.
ISP: Don't force modules to depend on interfaces they don't use.
DIP: Depend on abstractions at every boundary. Factories isolate the crossing point.

## Component Cohesion Principles

Cohesion (what goes together):
  REP: Release as a unit. Nothing goes in a component that isn't released together.
  CCP: Same actor, same component. Things that change together belong together.
  CRP: Don't force users to redeploy for changes they don't care about.

Coupling (what can depend on what):
  ADP: No cycles in the component dependency graph.
  SDP: Depend in the direction of stability.
  SAP: Stable components should be abstract.

## Boundary Types (weakest to strongest)

  1. Source-level monolith — same process, compile-time separation
  2. Deployment component — dynamically linked, separately versioned
  3. Local process — same machine, separate address spaces
  4. Service — network call, highest latency, strongest isolation

Rule: Use the weakest boundary that satisfies actual deployment needs.
Do not use services for development convenience — they carry real operational cost.

## Concept Map

Wiki root: $AGENTIC_SWE_WIKI_ROOT/clean-architecture/concepts/

| Concept | When to read |
|---------|-------------|
| Dependency-Rule.md | Any boundary crossing decision |
| SOLID-Principles.md | Class or module design, interface design |
| Component-Cohesion.md | Deciding what belongs in the same release unit |
| Component-Coupling.md | Dependency graph has cycles, or stability direction is wrong |
| Humble-Object-Pattern.md | Writing tests that must cross an architectural boundary |
| Package-Organization.md | Deciding folder/package structure for a new service |
| Boundaries-and-Plugins.md | Choosing where a framework or DB attaches to the system |
| Screaming-Architecture.md | Top-level folder structure should reveal use cases, not framework |

## Common Pitfalls

- **Premature Framework Commitment**: Framework chosen before domain model exists. Fix — treat frameworks as plugins; sketch domain use cases first, attach framework last.
- **Architecture-Design Split**: Treating high-level arch as separate from low-level design. Fix — they are one continuous discipline; design decisions are architectural decisions.
- **Big-Rewrite Overconfidence**: Full redesign replaces one mess with another. Fix — incremental improvement with enforced boundaries is safer.
- **Service Architecture Fallacy**: Microservices are inherently decoupled. Fix — services are deployment boundaries; coupling exists if cross-service data contracts are tight.
- **Structural Test Coupling**: Tests mirror production class structure one-to-one. Fix — test behavior, not structure; use a Testing API that bypasses structural detail.
- **Passing Row Structures Inward**: Returning a database row and passing it into use cases. Fix — define a data structure owned by the use case; adapter converts from row to that structure.

## Verification Checklist

- [ ] No inner circle imports anything from an outer circle
- [ ] Business rules contain no framework, database, or HTTP types
- [ ] Component dependency graph is acyclic
- [ ] Test coverage does not require reaching into implementation details
- [ ] Top-level package structure reveals use cases, not framework names
