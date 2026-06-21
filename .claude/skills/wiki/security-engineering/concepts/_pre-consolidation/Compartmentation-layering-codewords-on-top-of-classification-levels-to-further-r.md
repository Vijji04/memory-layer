---
title: Compartmentation: layering codewords on top of classification levels to further restrict access to named groups, requiring a principal to hold all attached codewords to read a document, typically implemented via discretionary access control
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Multilevel-Security.json]
contributing_chapters: ["Multilevel Security"]
confidence: high
---

# Compartmentation: layering codewords on top of classification levels to further restrict access to named groups, requiring a principal to hold all attached codewords to read a document, typically implemented via discretionary access control

> From chapter: *Multilevel Security*

## Core Principle

Multilevel Security defines a mandatory access control policy where data flows only upward through a clearance hierarchy (Unclassified → Top Secret) and principals may only read data at or below their clearance level, with compartments adding further need-to-know restrictions via codewords. The chapter's deeper contribution is the distinction between a precise, engineer-actionable security policy model and the vague organizational platitudes that masquerade as policy in most real organizations. MAC mechanisms developed for MLS have migrated into mainstream OS platforms (Android, iOS, Windows) for malware protection, but the core lesson is that the hedgehog approach of applying one rigid policy universally leads to overdesign—most security problems require the fox's many targeted solutions.

## Key Heuristics

These are the load-bearing rules for this concept.

> A security policy is a succinct description of what we're trying to achieve; it's driven by an understanding of the bad outcomes we wish to avoid and in turn drives the engineering.

> I will never use [the phrase 'security policy'] to refer to a collection of platitudes.

> Security engineering is usually in fox territory, but multilevel security is an example of the hedgehog approach.

> By trying to cast all security problems as hedgehog problems, MLS often leads to inappropriate security goals, policies and mechanisms.

> Information may only flow upwards, from confidential to secret to top secret, but never downwards – unless an authorized person takes a deliberate decision to declassify it.

> It is important for the practitioner to understand both their strengths and limitations, so that you can draw on the research literature when it's appropriate, and avoid being dragged into overdesign when it's not.

> Such ugly hacks have clear potential for abuse; at best they can help keep honest people from careless mistakes.

## Anti-Patterns & Fixes

- Vapid Policy Language: Writing security policies as vague organizational platitudes ('All staff shall obey this policy', 'need-to-know') that dodge who enforces what, how breaches are detected, and what users must actually do. Fix: Write a precise security policy model specifying which principals may access which data, under what conditions, and enforced by what mechanisms.
- Political Security Policy: Using security policy documents to balance organizational factions rather than to specify protection properties, resulting in language that is deliberately ambiguous. Fix: Separate organizational governance documents from technical security policy models; the policy model must be unambiguous and engineer-actionable.
- Browse-Down Workarounds: Allowing high-clearance users to view low-classification content via 'browse-down' systems (click navigation allowed, no text entry) as a convenience hack around MLS separation. Fix: Enforce strict network-level separation (e.g., SIPRNet vs. JWICS) and avoid one-way bridges except where formally analyzed.
- Hedgehog Overdesign: Forcing every security problem into a single rigid MAC/MLS framework even when the threat model does not require it, producing excessive complexity and unusable systems. Fix: Apply MLS/MAC narrowly where classification-level separation is the actual requirement; use targeted, problem-specific policies (fox approach) elsewhere.
- Mixing Policy Levels in One Document: Including organizational approval statements, mechanism descriptions, and access rules in the same document, obscuring what is a requirement vs. what is a control. Fix: Distinguish security policy model (what to achieve), security target (how a specific implementation achieves it), and protection profile (implementation-independent requirements for evaluation).

## When To Apply

Load this page when:

- Use this when designing an API or data store that must enforce that users at lower privilege tiers cannot read data tagged for higher privilege tiers (e.g., multi-tenant SaaS with tiered data sensitivity).
- Use this when an LLM agent is generating access control logic and must choose between user-overridable (DAC) and system-enforced (MAC) permission models for protecting sensitive resources.
- Use this when writing a security requirements document and need to distinguish between a precise, testable security policy model and vague placeholder language that merely defers decisions.
- Use this when architecting a system that aggregates data across classification or sensitivity boundaries and must decide whether and how to permit downward information flow.
- Use this when implementing label-based access control (e.g., tagging database rows with sensitivity levels) and need a formal model to validate that no read-up or write-down violations occur.
- Use this when evaluating whether to use SELinux, AppArmor, or platform MAC features (Android, iOS) to protect a privileged system component from being tampered with by less-trusted code.
- Use this when a system requirement says 'only users with need-to-know may access X' and the agent must translate that into a concrete, enforceable access control mechanism rather than an honor-system policy.
- Use this when designing compartmentalized data access where a principal must satisfy multiple independent conditions (clearance level AND all required codewords) to access a record.

## Concrete Examples

- US Executive Order 8381 (1940) establishing Restricted/Confidential/Secret classifications, later extended by Truman with Top Secret, as the origin of the MLS label hierarchy still used in NATO governments.
- The Office of Personnel Management breach (June 2015) in which Chinese intelligence stole clearance review data on ~20 million Americans including sexual partners and blackmail-relevant disclosures, illustrating the systemic risk of centralizing sensitive vetting data.
- SIPRNet vs. JWICS as real network-level MLS separation: SIPRNet handles Secret data behind crypto on standard equipment; JWICS handles Top Secret in physically shielded SCIFs.
- Royal Navy's failed 2009 phone ban and subsequent tracking of warships via Instagram by personnel aged 18-24, illustrating the gap between MLS policy and operational human behavior.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Multilevel Security**

An LLM coding agent is prone to generating access control code that mirrors the 'vapid policy' anti-pattern: producing placeholder checks like `if user.role == 'admin'` without encoding the actual lattice of who may read what at which sensitivity level, because the agent fills underspecified requirements with plausible-looking but non-enforceable logic. The MLS framework forces the agent to demand or infer a precise security policy model before generating enforcement code, preventing silent generation of DAC stubs where MAC is required. Additionally, agents tend toward hedgehog overdesign—applying the most complex available framework (full MLS label propagation) to simple permission problems—so the fox/hedgehog heuristic is a direct corrective for agent scope creep in security architecture generation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
