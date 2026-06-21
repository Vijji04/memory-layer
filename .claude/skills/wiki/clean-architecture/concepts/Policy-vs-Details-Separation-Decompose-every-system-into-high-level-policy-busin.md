---
title: Policy-vs-Details Separation: Decompose every system into high-level policy (business rules) and low-level details (IO, DB, frameworks, protocols); architect so policy has zero knowledge of details
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-15-What-Is-Architecture.json]
contributing_chapters: ["Chapter 15: What Is Architecture?"]
confidence: high
---

# Policy-vs-Details Separation: Decompose every system into high-level policy (business rules) and low-level details (IO, DB, frameworks, protocols); architect so policy has zero knowledge of details

> From chapter: *Chapter 15: What Is Architecture?*

## Core Principle

Software architecture is the shape given to a system—its component decomposition, arrangement, and communication patterns—whose primary purpose is to minimize lifetime cost and maximize programmer productivity by supporting development, deployment, operation, and maintenance. The central strategic principle is to separate high-level policy (business rules) from low-level details (databases, frameworks, protocols) so thoroughly that policy has no knowledge of details, allowing detail decisions to be deferred until maximum information is available. Good architecture does not primarily make the system work; it makes the system easy to change, understand, and deploy across its full life cycle.

## Key Heuristics

These are the load-bearing rules for this concept.

> The strategy behind that facilitation is to leave as many options open as possible, for as long as possible.

> The primary purpose of architecture is to support the life cycle of the system.

> The ultimate goal is to minimize the lifetime cost of the system and to maximize programmer productivity.

> A good architect pretends that the decision has not been made, and shapes the system such that those decisions can still be deferred or changed.

> Good architects carefully separate details from policy, and then decouple the policy from the details so thoroughly that the policy has no knowledge of the details and does not depend on the details in any way.

> The longer you wait to make those decisions, the more information you have with which to make them properly.

> Architecture should reveal operation.

> The primary cost of maintenance is in spelunking and risk.

## Anti-Patterns & Fixes

- Premature Framework Commitment: Adopting a web server, database, REST style, or DI framework early locks policy to details before requirements are clear. Fix: Write high-level policy to be agnostic of these details; inject or connect them at the boundary only when the decision can no longer be deferred.
- Component-Per-Team Architecture: Letting team org chart dictate component decomposition produces an architecture optimized for development schedules, not deployment or maintenance. Fix: Deliberately design components around domain boundaries and stable interfaces, independent of team headcount.
- Micro-Service Explosion: Adopting micro-services for development convenience without considering deployment leads to a daunting number of services with complex connection and timing configuration. Fix: Evaluate deployment costs early; prefer fewer services or a hybrid of services and in-process components when deployment complexity would dominate.
- Hard-Wired Physical Addressing: Encoding physical storage details (cylinder/head/sector) throughout business logic makes any hardware change require a full rewrite. Fix: Introduce a relative-address abstraction layer so high-level policy is agnostic of storage geometry.
- Architect-Off-Code Fallacy: Believing senior architects should stop coding and only manage design leads to architects who cannot feel the pain they inflict on the team. Fix: Architects must continue taking programming tasks to stay grounded in real implementation consequences.
- Architecture-for-Operation Over-Engineering: Over-investing in operation-optimized architecture when hardware scaling is cheap and developer time is expensive. Fix: Weight architectural investment toward development, deployment, and maintenance concerns first; use hardware to absorb operational inefficiencies.

## When To Apply

Load this page when:

- Use this when starting a greenfield service and tempted to immediately pick a database, web framework, or messaging protocol before domain logic is sketched out.
- Use this when a codebase is hard to change because business rules are tangled with IO, ORM calls, or HTTP handler code.
- Use this when planning a micro-services split and the number of proposed services is growing faster than the team's ability to deploy and monitor them.
- Use this when a system works in production but new feature development is slowing down dramatically due to fear of breakage (spelunking and risk signal).
- Use this when team structure is driving component boundaries rather than domain or stability considerations.
- Use this when a third-party framework or vendor decision has already been made and you need to isolate its blast radius from core policy.
- Use this when evaluating whether to refactor: determine whether poor architecture is hurting operation (cheap to fix with hardware) vs. development/maintenance (expensive, justifies refactor).
- Use this when designing interfaces between modules to decide which side should own the abstraction boundary.

## Concrete Examples

- Device Independence (1960s): Programs written for card readers had to be rewritten for magnetic tape; the lesson led to OS-level IO abstractions so the same program could target any unit-record device without change, illustrating policy-detail separation.
- Junk Mail Printing System: By directing OS IO to magnetic tape instead of the line printer, the same formatting program ran unchanged on five offline printers 24/7, demonstrating that deferring the device decision multiplied throughput without code modification.
- Physical Disk Addressing Anti-Pattern: A trucking union accounting system hard-wired cylinder/head/sector numbers throughout business logic; upgrading the disk required full data migration and code rewrites everywhere. The fix was a relative linear-address abstraction that isolated physical disk structure in one conversion routine.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 15: What Is Architecture?**

An LLM coding agent defaults to immediately instantiating concrete dependencies—choosing a specific ORM, HTTP library, or config format in the first code it generates—because it pattern-matches to common tutorial structures rather than deferring decisions. This collapses the Policy-vs-Details Separation before any domain logic exists, making every subsequent generation harder to redirect. Applying this chapter's framework, an agent should be explicitly prompted (or self-prompted) to generate core domain policy as pure functions or interfaces first, and to treat all IO, persistence, and framework wiring as placeholder stubs that are filled in only after the policy layer is stable and tested.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
