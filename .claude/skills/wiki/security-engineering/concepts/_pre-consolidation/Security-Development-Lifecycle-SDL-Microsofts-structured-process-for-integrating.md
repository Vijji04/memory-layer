---
title: Security Development Lifecycle (SDL): Microsoft's structured process for integrating security practices—including threat modeling, code review, and testing—throughout the software development lifecycle
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Secure-Systems-Development.json]
contributing_chapters: ["Secure Systems Development"]
confidence: high
---

# Security Development Lifecycle (SDL): Microsoft's structured process for integrating security practices—including threat modeling, code review, and testing—throughout the software development lifecycle

> From chapter: *Secure Systems Development*

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
