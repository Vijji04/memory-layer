---
title: Multi-Principal Goal Conflict Model: Protection goals can be subtle, complex, and mutually contradictory across principals (e.g., one party wants accountability, another wants deniability)
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Beyond-Computer-Says-No.json]
contributing_chapters: ["Beyond Computer Says No"]
confidence: high
---

# Multi-Principal Goal Conflict Model: Protection goals can be subtle, complex, and mutually contradictory across principals (e.g., one party wants accountability, another wants deniability)

> From chapter: *Beyond Computer Says No*

## Core Principle

Security engineering has evolved from siloed technical disciplines into a systems field that treats human, economic, and institutional factors as co-equal with technical ones. A central insight is that many security failures are incentive failures — when the guardian and the cost-bearer are different parties, systemic weakness follows. Effective security design now requires modeling all principals, their conflicting goals, and the social and psychological context of real-world usage.

## Key Heuristics

These are the load-bearing rules for this concept.

> if Alice guards a system while Bob pays the cost of failure, you can expect trouble

> Security engineering is about ensuring that systems are predictably dependable in the face of all sorts of malice, from bombers to botnets.

> everyone needs to have a systems perspective in order to design components that can be integrated usefully into real products and services

> as attacks shift from the hard technology to the people who use it, systems must also be resilient to error, mischance and even coercion

> Conflicts between goals are common: where one principal wants accountability and another wants deniability, it's hard to please them both

> many persistent security failures are incentive failures at heart

## Anti-Patterns & Fixes

- Island Mentality: Designing security components in isolation within a single domain (e.g., only cryptography, only OS hardening) without understanding adjacent domains or integration points. Fix: Adopt a cross-disciplinary systems perspective; understand how your component interacts with human users, institutional processes, and other technical layers.
- Incentive Misalignment: Assigning security responsibility to a party who does not bear the cost of failure, creating moral hazard. Fix: Align guard incentives with failure costs — the party responsible for security should also absorb consequences of breaches.
- Technical Reductionism: Treating security as purely a technical problem, ignoring usability, psychology, and human error as attack surfaces. Fix: Explicitly model human behavior (staff, customers, users, bystanders) as part of the threat and resilience model.
- Single-Principal Assumption: Designing security systems as if all stakeholders share identical goals. Fix: Enumerate all principals, identify conflicting goals (e.g., accountability vs. deniability), and make tradeoffs explicit rather than hidden.

## When To Apply

Load this page when:

- Use this when designing an authentication or authorization system that will be used by real end-users at scale, requiring human-factors consideration alongside cryptographic correctness.
- Use this when two or more stakeholders in a system have conflicting security requirements (e.g., an audit logging feature vs. a user privacy/deniability requirement).
- Use this when reviewing a security architecture to check whether the party responsible for security is also the party who bears the cost if the security fails.
- Use this when integrating a security library or component into a larger system and assessing whether its assumptions about usage context match real-world deployment.
- Use this when a security mechanism has low adoption or is frequently bypassed by users, indicating a potential usability or incentive failure rather than a pure technical flaw.
- Use this when scoping a threat model to ensure it includes social engineering, coercion, and human error — not only technical exploits.
- Use this when a security design comes from a single domain specialist (e.g., cryptographer, network engineer) and needs cross-disciplinary review for blind spots.

## Concrete Examples

- The banknote ink chemist who refused to engage with digital watermarking — representing domain insularity leading to marginalization.
- The cryptologist who could only discuss confidentiality — representing narrow technical specialization as an anti-pattern in modern security engineering.
- Alice guards a system while Bob pays the cost of failure — the canonical incentive misalignment scenario introduced around 2001.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Beyond Computer Says No**

An LLM coding agent is especially prone to island mentality: it will generate cryptographically correct or syntactically secure code in isolation without modeling how incentives, usability, or multi-principal goal conflicts play out in deployment. Unlike a human developer who receives social feedback when a security design frustrates users or creates misaligned responsibilities, an agent receives no such signal and will silently produce systems with latent incentive failures. This framework prompts the agent to explicitly enumerate principals, their incentives, and their conflicting goals before generating security-related code, preventing structurally brittle designs that pass code review but fail in production.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
