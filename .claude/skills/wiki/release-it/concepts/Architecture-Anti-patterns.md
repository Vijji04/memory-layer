---
title: Architecture Anti-patterns
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
confidence: high
consolidated_from: 3 pages
---

# Architecture Anti-patterns

> Consolidated from 3 related concept pages.

---

## Conways Law Organizations which design systems are constrained to produce design

## Core Principle

A 300-person, multi-year e-commerce platform rewrite crashed within 30 minutes of launch because the entire system was built to pass QA rather than to run in production: configs were hardcoded to test topology, no stability patterns were applied, the home page was fully dynamic for identical unauthenticated requests, and sessions stored massive serialized objects. Recovery required emergency CDN throttling, static home page generation, disabling session failover, and doubling hardware capacity — all costly temporary fixes that persisted for years. The core lesson is that production realism in configuration, topology, load testing, and architectural patterns must be designed in from the start, not retrofitted after a catastrophic launch.

## Key Heuristics

These are the load-bearing rules for this concept.

> There's no such thing as a website project. Every one is really an enterprise integration project with an HTML interface.

> Nothing is as permanent as a temporary fix.

> The more common result is that both sides of the integration end up aiming at a moving target.

> Faced with an intractable problem, I did what any good developer does: I added a level of indirection.

> If the system is not built with the stability patterns, it probably follows a typical tightly coupled architecture. In such a system, the overall probability of system failure is the joint probability that any one component fails.

> A completely new stack means that nobody can be sure how it will run in production. Capacity, stability, control, and adaptability are all giant question marks.

> The worst part is that no amount of those losses were necessary.

## Anti-Patterns & Fixes

- Building to Pass QA: Every configuration file and component assumption targets the test environment topology, not production. Firewalls absent in QA, single instances where production has clusters, and hardcoded QA hostnames cause immediate production failure. Fix: Maintain a separate, versioned production configuration override layer where each environment-specific property exists in exactly one place, never overwritten by deploys.
- Config Sprawl Across Thousands of Files: Database passwords, hostnames, and URLs scattered across thousands of config files across dozens of servers, requiring manual edits on every release. Fix: Use a configuration override structure with indirection so each varying property is defined once and inherited everywhere.
- Fully Dynamic Home Page With No Caching: Home page requiring 1,000+ database transactions per render and served identically millions of times daily because personalization was never actually implemented. Fix: Detect unauthenticated/unidentified users and serve a pre-built static copy, reserving dynamic rendering only for identified users where personalization is actually possible.
- Session Bloat: Storing entire shopping carts and full search result sets (up to 2,000 items) in serialized session objects, making session failover unsustainably expensive. Fix: Store only minimal identifiers (user ID, cart ID, search keywords, page index) in session; retrieve full data from backing store on demand.
- Penny-Wise QA Network Topology: Omitting production-level firewalls and network gear from QA to save costs, resulting in applications that assume QA topology and break when production firewalls are present. Fix: Mirror production network topology in QA even at added cost; the cost of failed deployments and downtime exceeds the hardware savings.
- Big-Bang Commerce Stack Replacement: Replacing all systems simultaneously means no production baseline exists, all integration points are untested under real load, and failure modes are completely unknown at launch. Fix: Where possible, replace incrementally; at minimum, invest heavily in production-realistic load testing and stability patterns before launch.

## When To Apply

Load this page when:

- Use this when deploying a newly built system to production for the first time and needing to validate that configuration files are environment-aware rather than hardcoded to test topology.
- Use this when designing a configuration management strategy for an application with many integration points across multiple environments (dev, QA, staging, production).
- Use this when a high-traffic page is being rendered fully dynamically but the output is identical for all unauthenticated users — consider static pre-generation.
- Use this when designing session storage for a web application to evaluate what data belongs in the session versus in a backing data store.
- Use this when planning a load test to determine whether the test environment's topology (firewall rules, instance counts, network gear) is sufficiently representative of production.
- Use this when an application uses a CDN and you need to plan launch-day traffic management, throttling, or bot-blocking strategies without application-layer code changes.
- Use this when evaluating the risk profile of a full-stack replacement project versus incremental migration, specifically to enumerate unknown production failure modes.
- Use this when an org structure has multiple teams working on tightly integrated systems, to predict where interface gaps or moving-target integration problems will emerge (Conway's Law diagnostic).

## Concrete Examples

- A major retailer's complete e-commerce platform replacement (15 applications, 500+ integration points, 300+ person team) crashed at 250,000 concurrent sessions within 30 minutes of launch due to QA-targeted configs and no stability patterns.
- The CDN accidentally went live the Saturday before the Monday launch due to a metadata entry error, exposing a partially loaded new site to real customers and taking orders for two hours before being identified and reversed.
- The home page required 1,000+ database transactions to build and was served 5 million times daily identically to unauthenticated users; a static pre-generation script was deployed as an emergency fix.
- Sessions contained full serialized shopping carts and up to 2,000 search results, making session failover unworkable; failover was disabled, causing customers mid-checkout to lose their sessions when an instance went down.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Case Study: Trampled by Your Own Customers**

An LLM coding agent is especially prone to the 'building to pass QA' failure mode because it generates configuration, connection strings, and topology assumptions based on the context it is given — which is almost always the development or test environment. Without explicit prompting to parameterize every environment-specific value and model production topology differences (firewalls, clustering, credentials), an agent will hardcode test assumptions throughout generated code. Additionally, an agent asked to implement features like personalization or session management will default to maximal data inclusion in sessions and fully dynamic rendering, exactly the patterns that caused catastrophic scaling failure here; agents must be explicitly constrained to minimal-session and cache-first patterns as default outputs.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Early Decision Crystallization The principle that the earliest architectural dec

## Core Principle

Chapter 1 argues that software design is systematically incomplete because it targets QA correctness rather than production survivability, and that this gap has measurable multi-million-dollar financial consequences. The earliest architectural decisions — made with the least information — crystallize into team structure and are hardest to reverse, so they must account for operational lifecycle costs, not just build costs. Pragmatic architecture, as opposed to ivory-tower abstraction, treats software design as a fusion of technical and financial decision-making aimed at systems that survive contact with the real world.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't avoid one-time development expenses at the cost of recurring operational expenses.

> Team assignments are the first draft of the architecture.

> Release 1.0 is the beginning of your software's life, not the end of the project.

> Design and architecture decisions are also financial decisions.

> Production is the only place to learn how the software will respond to real-world stimuli.

> Systems spend much more of their life in operation than in development.

> Different alternatives often have similar implementation costs but radically different lifecycle costs.

## Anti-Patterns & Fixes

- QA-Optimized Design: Software is built only to pass functional tests and survive the artificial realm of QA, leaving it unprepared for production load, hostile users, and long-term operations. Fix: Design explicitly for production conditions — uptime, operational cost, failure modes, and real user behavior.
- Ivory Tower Architecture: Architects issue technology mandates disconnected from coder and user realities, producing systems that are elegant but fragile and expensive to operate. Fix: Adopt pragmatic architecture — work with coders, peel back abstractions when they don't fit, and prioritize operational dynamics.
- Development Cost Optimization at Operational Cost Expense: Teams make decisions that reduce one-time build cost while incurring recurring operational costs, appearing rational under fixed-budget project measurement but destroying long-term value. Fix: Evaluate decisions against full lifecycle cost, not just project-phase cost.
- Late-Stage Operability Investment: Operability, availability, and resilience are treated as features to add after functional completion rather than architectural constraints from the start. Fix: Incorporate stability and operational requirements as first-class design constraints from initial architecture decisions.

## When To Apply

Load this page when:

- Use this when generating an initial system architecture or selecting a decomposition strategy, to ensure early decisions account for operational lifecycle costs and reversibility.
- Use this when choosing between two implementation approaches with similar build cost but potentially different operational costs (e.g., managed service vs. self-hosted, synchronous vs. async).
- Use this when designing for a stated scale requirement (e.g., '25,000 concurrent users') to verify the design targets production stress, not just QA-passable functionality.
- Use this when estimating the ROI of an infrastructure or reliability investment (e.g., automated deployment, circuit breakers) to frame it as avoided operational cost.
- Use this when a system has passed QA and is being evaluated for production readiness, as a reminder that QA passage is a necessary but insufficient signal.
- Use this when team structure or service ownership is being defined, since org boundaries will crystallize into architectural boundaries.
- Use this when reviewing a design that prioritizes abstract elegance or 'company standards' compliance over concrete operational requirements.

## Concrete Examples

- Ford Pinto analogy: a car prone to exploding when hit in just the right way, used to illustrate software that passes QA but fails catastrophically in production edge cases.
- Chevy Vega analogy: a car whose front end broke off on the company's own test track, illustrating that even internal testing can miss fundamental structural failures.
- Automated build and release system: spending $5,000 to avoid downtime during releases saves $200,000 over five years (4,000% ROI), illustrating one-time vs. recurring cost tradeoff.
- 98% vs 99.99% uptime: at $100,000/hour downtime cost, the difference across one year exceeds $17 million, illustrating the financial magnitude of availability design decisions.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 1: Introduction**

An LLM coding agent defaults to generating code that satisfies stated functional requirements and passes visible test cases — the exact QA-optimized anti-pattern this chapter warns against. Agents will readily optimize for code that compiles and appears correct without modeling failure modes, operational costs, or long-term lifecycle implications unless explicitly prompted with production constraints. This chapter's frameworks should trigger agents to ask: 'What is the cost of this design decision over 3-5 years of operation?' and 'What happens to this code under hostile, high-scale, or degraded conditions?' before finalizing any architectural choice.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Ivory Tower Architecture The anti model where architects issue top down decrees

## Core Principle

Chapter 1 argues that software design is systematically incomplete because it targets QA correctness rather than production survivability, and that this gap has measurable multi-million-dollar financial consequences. The earliest architectural decisions — made with the least information — crystallize into team structure and are hardest to reverse, so they must account for operational lifecycle costs, not just build costs. Pragmatic architecture, as opposed to ivory-tower abstraction, treats software design as a fusion of technical and financial decision-making aimed at systems that survive contact with the real world.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't avoid one-time development expenses at the cost of recurring operational expenses.

> Team assignments are the first draft of the architecture.

> Release 1.0 is the beginning of your software's life, not the end of the project.

> Design and architecture decisions are also financial decisions.

> Production is the only place to learn how the software will respond to real-world stimuli.

> Systems spend much more of their life in operation than in development.

> Different alternatives often have similar implementation costs but radically different lifecycle costs.

## Anti-Patterns & Fixes

- QA-Optimized Design: Software is built only to pass functional tests and survive the artificial realm of QA, leaving it unprepared for production load, hostile users, and long-term operations. Fix: Design explicitly for production conditions — uptime, operational cost, failure modes, and real user behavior.
- Ivory Tower Architecture: Architects issue technology mandates disconnected from coder and user realities, producing systems that are elegant but fragile and expensive to operate. Fix: Adopt pragmatic architecture — work with coders, peel back abstractions when they don't fit, and prioritize operational dynamics.
- Development Cost Optimization at Operational Cost Expense: Teams make decisions that reduce one-time build cost while incurring recurring operational costs, appearing rational under fixed-budget project measurement but destroying long-term value. Fix: Evaluate decisions against full lifecycle cost, not just project-phase cost.
- Late-Stage Operability Investment: Operability, availability, and resilience are treated as features to add after functional completion rather than architectural constraints from the start. Fix: Incorporate stability and operational requirements as first-class design constraints from initial architecture decisions.

## When To Apply

Load this page when:

- Use this when generating an initial system architecture or selecting a decomposition strategy, to ensure early decisions account for operational lifecycle costs and reversibility.
- Use this when choosing between two implementation approaches with similar build cost but potentially different operational costs (e.g., managed service vs. self-hosted, synchronous vs. async).
- Use this when designing for a stated scale requirement (e.g., '25,000 concurrent users') to verify the design targets production stress, not just QA-passable functionality.
- Use this when estimating the ROI of an infrastructure or reliability investment (e.g., automated deployment, circuit breakers) to frame it as avoided operational cost.
- Use this when a system has passed QA and is being evaluated for production readiness, as a reminder that QA passage is a necessary but insufficient signal.
- Use this when team structure or service ownership is being defined, since org boundaries will crystallize into architectural boundaries.
- Use this when reviewing a design that prioritizes abstract elegance or 'company standards' compliance over concrete operational requirements.

## Concrete Examples

- Ford Pinto analogy: a car prone to exploding when hit in just the right way, used to illustrate software that passes QA but fails catastrophically in production edge cases.
- Chevy Vega analogy: a car whose front end broke off on the company's own test track, illustrating that even internal testing can miss fundamental structural failures.
- Automated build and release system: spending $5,000 to avoid downtime during releases saves $200,000 over five years (4,000% ROI), illustrating one-time vs. recurring cost tradeoff.
- 98% vs 99.99% uptime: at $100,000/hour downtime cost, the difference across one year exceeds $17 million, illustrating the financial magnitude of availability design decisions.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 1: Introduction**

An LLM coding agent defaults to generating code that satisfies stated functional requirements and passes visible test cases — the exact QA-optimized anti-pattern this chapter warns against. Agents will readily optimize for code that compiles and appears correct without modeling failure modes, operational costs, or long-term lifecycle implications unless explicitly prompted with production constraints. This chapter's frameworks should trigger agents to ask: 'What is the cost of this design decision over 3-5 years of operation?' and 'What happens to this code under hostile, high-scale, or degraded conditions?' before finalizing any architectural choice.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
