---
title: Facade Pattern: Define a boundary via a single Facade class that proxies all service calls, sacrificing dependency inversion for simplicity
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-24-Partial-Boundaries.json]
contributing_chapters: ["Chapter 24: Partial Boundaries"]
confidence: high
---

# Facade Pattern: Define a boundary via a single Facade class that proxies all service calls, sacrificing dependency inversion for simplicity

> From chapter: *Chapter 24: Partial Boundaries*

## Core Principle

Partial boundaries are deliberate architectural placeholders that preserve the option for full separation without incurring full deployment and administration costs; the three main forms are Skip The Last Step (full code, single deployment), One-Dimensional Boundary (Strategy pattern, one-way inversion), and Facade (no inversion, simplest form). Each form trades isolation strength for implementation cost, and all are vulnerable to degradation over time if the expected full boundary never materializes. The architect's responsibility is to choose the appropriate form for each boundary candidate and actively prevent the erosion of whatever isolation level was chosen.

## Key Heuristics

These are the load-bearing rules for this concept.

> Full-fledged architectural boundaries are expensive. They require reciprocal polymorphic Boundary interfaces, Input and Output data structures, and all of the dependency management necessary to isolate the two sides into independently compilable and deployable components.

> In many situations, a good architect might judge that the expense of such a boundary is too high—but might still want to hold a place for such a boundary in case it is needed later.

> YAGNI: 'You Aren't Going to Need It.' Architects, however, sometimes look at the problem and think, 'Yeah, but I might.'

> Without reciprocal interfaces, nothing prevents this kind of backchannel other than the diligence and discipline of the developers and architects.

> It is one of the functions of an architect to decide where an architectural boundary might one day exist, and whether to fully or partially implement that boundary.

> Each can also be degraded if that boundary never materializes.

## Anti-Patterns & Fixes

- Boundary Erosion Over Time: A partial boundary that is never promoted to full status gradually accumulates wrong-direction dependencies (as happened with FitNesse's web and wiki components), making eventual separation expensive. Fix: Periodically audit dependency direction across partial boundaries and enforce crossing rules via tooling (e.g., ArchUnit), not just developer discipline.
- Premature Full Boundary: Implementing a complete, independently deployable boundary (with version tracking, release management, multi-component overhead) when the separation may never be needed, wasting significant engineering effort. Fix: Start with a partial boundary (Skip The Last Step or Strategy pattern) and promote to full only when deployment independence is actually required.
- Facade Transitive Coupling: Using the Facade pattern causes the Client to have a transitive dependency on all underlying service classes; any service change forces client recompilation and backchannels are trivially easy to introduce. Fix: Prefer the Strategy/One-Dimensional boundary when stronger isolation is needed, or accept the Facade only for low-churn, low-coupling scenarios.
- Backchannel Creation in One-Dimensional Boundaries: Without reciprocal interfaces, developers bypass the Strategy interface and directly reference ServiceImpl, defeating the boundary. Fix: Use static analysis or module/package visibility rules to prevent direct access to implementation classes.

## When To Apply

Load this page when:

- Use this when designing a module that might need to become an independently deployable service in the future, but current requirements don't justify the full boundary overhead.
- Use this when a team is early in a project and wants to preserve architectural options without committing to multi-component release management.
- Use this when generating a new service class and deciding whether to introduce an interface layer — apply the Strategy pattern as a low-cost one-dimensional boundary placeholder.
- Use this when a codebase shows cross-cutting dependencies that violate intended module separation, to diagnose whether a partial boundary has degraded.
- Use this when evaluating whether to refactor a Facade into a full boundary, by assessing whether transitive recompilation or backchannel dependencies have become a real problem.
- Use this when scaffolding a plugin or extension point that may be optional now but architecturally significant later — Skip The Last Step keeps the extension seam alive without deployment complexity.
- Use this when an agent is asked to add a feature that touches a boundary region — to decide whether to honor the existing partial boundary structure or propose a promotion to full boundary.

## Concrete Examples

- FitNesse web server component: designed as separable from the wiki/testing component using Skip The Last Step, packaged as a single downloadable jar. Over time the separation weakened as wrong-direction dependencies accumulated.
- Strategy pattern as One-Dimensional Boundary: a ServiceBoundary interface used by Client and implemented by ServiceImpl, illustrated in Figure 24.1, with a dotted arrow showing the backchannel risk.
- Facade pattern as simplest boundary: a Facade class listing all services as methods and delegating to underlying service classes, illustrated in Figure 24.2, with Client holding transitive dependencies on all service classes.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 24: Partial Boundaries**

An LLM coding agent, when generating new modules, defaults to flat or fully-coupled implementations because it optimizes for immediate correctness rather than future architectural flexibility — it will not spontaneously introduce boundary placeholders unless explicitly instructed. The agent also cannot detect boundary erosion across a conversation context, so a partial boundary it creates in one session may be silently violated in a later session when it generates code that directly references implementation classes rather than the interface. Applying this chapter means an agent should be prompted with explicit boundary-preservation rules (e.g., 'always reference ServiceBoundary, never ServiceImpl directly') and should flag any generated dependency that crosses a known partial boundary in the wrong direction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
