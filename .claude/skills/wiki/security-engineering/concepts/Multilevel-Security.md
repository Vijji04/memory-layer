---
title: Multilevel Security
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 9 pages
---

# Multilevel Security

> Consolidated from 9 related concept pages.

---

## Bell LaPadula Lattice Equivalence Treats classification plus codeword compartmen

## Core Principle

Chapter 10 establishes that the primary boundary challenge in large systems is not preventing downward information flow (hierarchical secrecy) but preventing lateral flow between peer groups who should not share data. It surveys technical mechanisms — compartments, lattice models, RBAC, Chinese walls — and finds that the hard problems are almost always policy and incentive failures rather than mechanism failures: organizations lack motivation to implement fine-grained controls, anonymization is routinely overestimated, and side-channel leakage through metadata undermines primary controls. The chapter's core prescription is the 'fox' approach: deep application-specific adversarial thinking rather than reliance on any single universal security model.

## Key Heuristics

These are the load-bearing rules for this concept.

> If you centralise systems containing sensitive information, you create a more valuable asset and simultaneously give more people access to it. Just as the benefits of networks can scale more than linearly, so can the harms.

> The easy problem is setting up access controls in a direct care setting so that access to each record is limited to a sensible number of staff. Such systems can be designed by automating existing working practices.

> Multilateral security requires the 'fox' approach; you need to understand your application in detail, learn what's gone wrong in the past – and also be good at adversarial thinking if you want to anticipate what's likely to go wrong in future.

> The real problems facing users of intelligence systems have to do with combining data in different compartments, and downgrading it after sanitization. Lattice security models offer little help here.

> The policy goal is usually not to prevent information flowing 'down' a hierarchy but to prevent it flowing 'across' between smaller groups.

> Doctors, bankers and spies have all learned that as well as preventing overt information flows, they also have to prevent information leakage through side-channels such as billing data.

> The traditional approach to privacy, which might be summarised as 'consent or anonymise', is being undermined by growing complexity with many outsourced systems that are often opaque even to doctors (let alone patients).

## Anti-Patterns & Fixes

- Over-Centralization: Aggregating all sensitive data into one system to improve sharing simultaneously maximizes attacker value and insider threat surface. Fix: Partition data into compartments with incompatible labels; grant access only to the compartment relevant to a user's current task.
- Flat Access on Seniority: Granting cumulative access to many compartments as a reward for long service (e.g., Aldrich Ames) creates catastrophic insider threat potential. Fix: Enforce need-to-know per compartment regardless of seniority; regularly audit and revoke stale access.
- Treating Anonymization as a Privacy Silver Bullet: Building 'anonymised' databases of rich records assumes re-identification is impossible, but computer scientists have known since the 1980s this is far harder than it looks. Fix: Apply formal de-identification theory (e.g., k-anonymity, differential privacy) and assess re-identification risk before releasing aggregate data.
- Using the OS as a Sharing Mechanism After Labeling It for Isolation: Mandatory access control products used for compartmentation turn the OS into an isolation mechanism, making legitimate data combination across compartments operationally impossible. Fix: Design explicit, audited downgrade/sanitization workflows rather than relying purely on label-based blocking.
- Uniform Navy-Style Key Distribution: Operational necessity (a ship can be sent anywhere) forced all 800 US Navy ships onto the same cipher keys, which the Walker family then sold wholesale. Fix: Design for operational flexibility from the start with key hierarchies or per-mission keying rather than retrofitting uniformity.
- Ignoring Side-Channel Leakage: Restricting record content while leaving billing, scheduling, or referral metadata accessible leaks sensitive inferences (e.g., patient X paid specialist Y implies diagnosis). Fix: Apply boundary controls to all correlated metadata, not just primary record content.

## When To Apply

Load this page when:

- Use this when designing an API or database schema that must serve multiple organizational units where one unit should not see another's data (e.g., multi-tenant SaaS, federated health systems).
- Use this when implementing access control for a system where the same data store is accessed by users with conflicting interests (e.g., financial advisors whose clients compete with each other).
- Use this when a feature request asks for 'data sharing' between departments, teams, or organizations and the requester has not specified what lateral boundaries must be preserved.
- Use this when generating code that aggregates or exports records and the records contain quasi-identifiers that could enable re-identification even after obvious PII is stripped.
- Use this when building role-based access control and the role definitions are being inherited from organizational hierarchy rather than derived from actual data-access need.
- Use this when a logging, billing, or audit system is being designed alongside a privacy-sensitive primary system, as the metadata may leak as much as the primary data.
- Use this when a system's access model relies on a single classification level (e.g., 'Top Secret') without codeword-style compartments, and the user population with that level exceeds a small, well-audited group.
- Use this when evaluating whether a proposed 'anonymized' data release from a rich dataset is actually safe to publish externally.

## Concrete Examples

- Ultra codeword in WWII: Only a tiny compartment of Allied leaders and generals could access Enigma decrypts; Churchill received summaries in a locked dispatch box inaccessible to his own staff.
- Aldrich Ames CIA case: Long-service counterintelligence officer accumulated access to a large number of compartments and betrayed nearly the entire US agent network in Russia.
- Walker spy case: Operational necessity forced all 800 US Navy ships onto the same cipher keys, which were then sold wholesale to the Russians.
- UK Children's Database (ContactPoint): Parliament shut it down in 2010 after realizing that giving doctors, teachers, and social workers shared access to all children's data was both unsafe and illegal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Boundaries**

An LLM coding agent defaults to generating the simplest schema and access control that satisfies the stated functional requirement, which almost always means a flat, centralized model with role-based read permissions — exactly the over-centralization anti-pattern. The agent has no visibility into cross-unit conflict-of-interest risks or side-channel leakage through metadata it generates (e.g., audit logs, foreign keys, timestamps), so it will produce code that is functionally correct but structurally violates lateral boundary requirements. Agents must be explicitly prompted with compartment boundaries, conflict-of-interest rules, and metadata leakage constraints before generating any multi-tenant or multi-role data access layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Chinese Wall Model Separates conflicting interest data within a single organizat

## Core Principle

Chapter 10 establishes that the primary boundary challenge in large systems is not preventing downward information flow (hierarchical secrecy) but preventing lateral flow between peer groups who should not share data. It surveys technical mechanisms — compartments, lattice models, RBAC, Chinese walls — and finds that the hard problems are almost always policy and incentive failures rather than mechanism failures: organizations lack motivation to implement fine-grained controls, anonymization is routinely overestimated, and side-channel leakage through metadata undermines primary controls. The chapter's core prescription is the 'fox' approach: deep application-specific adversarial thinking rather than reliance on any single universal security model.

## Key Heuristics

These are the load-bearing rules for this concept.

> If you centralise systems containing sensitive information, you create a more valuable asset and simultaneously give more people access to it. Just as the benefits of networks can scale more than linearly, so can the harms.

> The easy problem is setting up access controls in a direct care setting so that access to each record is limited to a sensible number of staff. Such systems can be designed by automating existing working practices.

> Multilateral security requires the 'fox' approach; you need to understand your application in detail, learn what's gone wrong in the past – and also be good at adversarial thinking if you want to anticipate what's likely to go wrong in future.

> The real problems facing users of intelligence systems have to do with combining data in different compartments, and downgrading it after sanitization. Lattice security models offer little help here.

> The policy goal is usually not to prevent information flowing 'down' a hierarchy but to prevent it flowing 'across' between smaller groups.

> Doctors, bankers and spies have all learned that as well as preventing overt information flows, they also have to prevent information leakage through side-channels such as billing data.

> The traditional approach to privacy, which might be summarised as 'consent or anonymise', is being undermined by growing complexity with many outsourced systems that are often opaque even to doctors (let alone patients).

## Anti-Patterns & Fixes

- Over-Centralization: Aggregating all sensitive data into one system to improve sharing simultaneously maximizes attacker value and insider threat surface. Fix: Partition data into compartments with incompatible labels; grant access only to the compartment relevant to a user's current task.
- Flat Access on Seniority: Granting cumulative access to many compartments as a reward for long service (e.g., Aldrich Ames) creates catastrophic insider threat potential. Fix: Enforce need-to-know per compartment regardless of seniority; regularly audit and revoke stale access.
- Treating Anonymization as a Privacy Silver Bullet: Building 'anonymised' databases of rich records assumes re-identification is impossible, but computer scientists have known since the 1980s this is far harder than it looks. Fix: Apply formal de-identification theory (e.g., k-anonymity, differential privacy) and assess re-identification risk before releasing aggregate data.
- Using the OS as a Sharing Mechanism After Labeling It for Isolation: Mandatory access control products used for compartmentation turn the OS into an isolation mechanism, making legitimate data combination across compartments operationally impossible. Fix: Design explicit, audited downgrade/sanitization workflows rather than relying purely on label-based blocking.
- Uniform Navy-Style Key Distribution: Operational necessity (a ship can be sent anywhere) forced all 800 US Navy ships onto the same cipher keys, which the Walker family then sold wholesale. Fix: Design for operational flexibility from the start with key hierarchies or per-mission keying rather than retrofitting uniformity.
- Ignoring Side-Channel Leakage: Restricting record content while leaving billing, scheduling, or referral metadata accessible leaks sensitive inferences (e.g., patient X paid specialist Y implies diagnosis). Fix: Apply boundary controls to all correlated metadata, not just primary record content.

## When To Apply

Load this page when:

- Use this when designing an API or database schema that must serve multiple organizational units where one unit should not see another's data (e.g., multi-tenant SaaS, federated health systems).
- Use this when implementing access control for a system where the same data store is accessed by users with conflicting interests (e.g., financial advisors whose clients compete with each other).
- Use this when a feature request asks for 'data sharing' between departments, teams, or organizations and the requester has not specified what lateral boundaries must be preserved.
- Use this when generating code that aggregates or exports records and the records contain quasi-identifiers that could enable re-identification even after obvious PII is stripped.
- Use this when building role-based access control and the role definitions are being inherited from organizational hierarchy rather than derived from actual data-access need.
- Use this when a logging, billing, or audit system is being designed alongside a privacy-sensitive primary system, as the metadata may leak as much as the primary data.
- Use this when a system's access model relies on a single classification level (e.g., 'Top Secret') without codeword-style compartments, and the user population with that level exceeds a small, well-audited group.
- Use this when evaluating whether a proposed 'anonymized' data release from a rich dataset is actually safe to publish externally.

## Concrete Examples

- Ultra codeword in WWII: Only a tiny compartment of Allied leaders and generals could access Enigma decrypts; Churchill received summaries in a locked dispatch box inaccessible to his own staff.
- Aldrich Ames CIA case: Long-service counterintelligence officer accumulated access to a large number of compartments and betrayed nearly the entire US agent network in Russia.
- Walker spy case: Operational necessity forced all 800 US Navy ships onto the same cipher keys, which were then sold wholesale to the Russians.
- UK Children's Database (ContactPoint): Parliament shut it down in 2010 after realizing that giving doctors, teachers, and social workers shared access to all children's data was both unsafe and illegal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Boundaries**

An LLM coding agent defaults to generating the simplest schema and access control that satisfies the stated functional requirement, which almost always means a flat, centralized model with role-based read permissions — exactly the over-centralization anti-pattern. The agent has no visibility into cross-unit conflict-of-interest risks or side-channel leakage through metadata it generates (e.g., audit logs, foreign keys, timestamps), so it will produce code that is functionally correct but structurally violates lateral boundary requirements. Agents must be explicitly prompted with compartment boundaries, conflict-of-interest rules, and metadata leakage constraints before generating any multi-tenant or multi-role data access layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Compartmentation layering codewords on top of classification levels to further r

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

---

## Fox vs Hedgehog Security Model the epistemic framing that hedgehog security one

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

---

## Hedgehog vs Fox Security Approach Multilevel security bets on one big correct me

## Core Principle

Chapter 10 establishes that the primary boundary challenge in large systems is not preventing downward information flow (hierarchical secrecy) but preventing lateral flow between peer groups who should not share data. It surveys technical mechanisms — compartments, lattice models, RBAC, Chinese walls — and finds that the hard problems are almost always policy and incentive failures rather than mechanism failures: organizations lack motivation to implement fine-grained controls, anonymization is routinely overestimated, and side-channel leakage through metadata undermines primary controls. The chapter's core prescription is the 'fox' approach: deep application-specific adversarial thinking rather than reliance on any single universal security model.

## Key Heuristics

These are the load-bearing rules for this concept.

> If you centralise systems containing sensitive information, you create a more valuable asset and simultaneously give more people access to it. Just as the benefits of networks can scale more than linearly, so can the harms.

> The easy problem is setting up access controls in a direct care setting so that access to each record is limited to a sensible number of staff. Such systems can be designed by automating existing working practices.

> Multilateral security requires the 'fox' approach; you need to understand your application in detail, learn what's gone wrong in the past – and also be good at adversarial thinking if you want to anticipate what's likely to go wrong in future.

> The real problems facing users of intelligence systems have to do with combining data in different compartments, and downgrading it after sanitization. Lattice security models offer little help here.

> The policy goal is usually not to prevent information flowing 'down' a hierarchy but to prevent it flowing 'across' between smaller groups.

> Doctors, bankers and spies have all learned that as well as preventing overt information flows, they also have to prevent information leakage through side-channels such as billing data.

> The traditional approach to privacy, which might be summarised as 'consent or anonymise', is being undermined by growing complexity with many outsourced systems that are often opaque even to doctors (let alone patients).

## Anti-Patterns & Fixes

- Over-Centralization: Aggregating all sensitive data into one system to improve sharing simultaneously maximizes attacker value and insider threat surface. Fix: Partition data into compartments with incompatible labels; grant access only to the compartment relevant to a user's current task.
- Flat Access on Seniority: Granting cumulative access to many compartments as a reward for long service (e.g., Aldrich Ames) creates catastrophic insider threat potential. Fix: Enforce need-to-know per compartment regardless of seniority; regularly audit and revoke stale access.
- Treating Anonymization as a Privacy Silver Bullet: Building 'anonymised' databases of rich records assumes re-identification is impossible, but computer scientists have known since the 1980s this is far harder than it looks. Fix: Apply formal de-identification theory (e.g., k-anonymity, differential privacy) and assess re-identification risk before releasing aggregate data.
- Using the OS as a Sharing Mechanism After Labeling It for Isolation: Mandatory access control products used for compartmentation turn the OS into an isolation mechanism, making legitimate data combination across compartments operationally impossible. Fix: Design explicit, audited downgrade/sanitization workflows rather than relying purely on label-based blocking.
- Uniform Navy-Style Key Distribution: Operational necessity (a ship can be sent anywhere) forced all 800 US Navy ships onto the same cipher keys, which the Walker family then sold wholesale. Fix: Design for operational flexibility from the start with key hierarchies or per-mission keying rather than retrofitting uniformity.
- Ignoring Side-Channel Leakage: Restricting record content while leaving billing, scheduling, or referral metadata accessible leaks sensitive inferences (e.g., patient X paid specialist Y implies diagnosis). Fix: Apply boundary controls to all correlated metadata, not just primary record content.

## When To Apply

Load this page when:

- Use this when designing an API or database schema that must serve multiple organizational units where one unit should not see another's data (e.g., multi-tenant SaaS, federated health systems).
- Use this when implementing access control for a system where the same data store is accessed by users with conflicting interests (e.g., financial advisors whose clients compete with each other).
- Use this when a feature request asks for 'data sharing' between departments, teams, or organizations and the requester has not specified what lateral boundaries must be preserved.
- Use this when generating code that aggregates or exports records and the records contain quasi-identifiers that could enable re-identification even after obvious PII is stripped.
- Use this when building role-based access control and the role definitions are being inherited from organizational hierarchy rather than derived from actual data-access need.
- Use this when a logging, billing, or audit system is being designed alongside a privacy-sensitive primary system, as the metadata may leak as much as the primary data.
- Use this when a system's access model relies on a single classification level (e.g., 'Top Secret') without codeword-style compartments, and the user population with that level exceeds a small, well-audited group.
- Use this when evaluating whether a proposed 'anonymized' data release from a rich dataset is actually safe to publish externally.

## Concrete Examples

- Ultra codeword in WWII: Only a tiny compartment of Allied leaders and generals could access Enigma decrypts; Churchill received summaries in a locked dispatch box inaccessible to his own staff.
- Aldrich Ames CIA case: Long-service counterintelligence officer accumulated access to a large number of compartments and betrayed nearly the entire US agent network in Russia.
- Walker spy case: Operational necessity forced all 800 US Navy ships onto the same cipher keys, which were then sold wholesale to the Russians.
- UK Children's Database (ContactPoint): Parliament shut it down in 2010 after realizing that giving doctors, teachers, and social workers shared access to all children's data was both unsafe and illegal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Boundaries**

An LLM coding agent defaults to generating the simplest schema and access control that satisfies the stated functional requirement, which almost always means a flat, centralized model with role-based read permissions — exactly the over-centralization anti-pattern. The agent has no visibility into cross-unit conflict-of-interest risks or side-channel leakage through metadata it generates (e.g., audit logs, foreign keys, timestamps), so it will produce code that is functionally correct but structurally violates lateral boundary requirements. Agents must be explicitly prompted with compartment boundaries, conflict-of-interest rules, and metadata leakage constraints before generating any multi-tenant or multi-role data access layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Mandatory Access Control MAC system enforced access rules that cannot be overrid

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

---

## Multilateral Security LatticeCompartment Model Controls information flow lateral

## Core Principle

Chapter 10 establishes that the primary boundary challenge in large systems is not preventing downward information flow (hierarchical secrecy) but preventing lateral flow between peer groups who should not share data. It surveys technical mechanisms — compartments, lattice models, RBAC, Chinese walls — and finds that the hard problems are almost always policy and incentive failures rather than mechanism failures: organizations lack motivation to implement fine-grained controls, anonymization is routinely overestimated, and side-channel leakage through metadata undermines primary controls. The chapter's core prescription is the 'fox' approach: deep application-specific adversarial thinking rather than reliance on any single universal security model.

## Key Heuristics

These are the load-bearing rules for this concept.

> If you centralise systems containing sensitive information, you create a more valuable asset and simultaneously give more people access to it. Just as the benefits of networks can scale more than linearly, so can the harms.

> The easy problem is setting up access controls in a direct care setting so that access to each record is limited to a sensible number of staff. Such systems can be designed by automating existing working practices.

> Multilateral security requires the 'fox' approach; you need to understand your application in detail, learn what's gone wrong in the past – and also be good at adversarial thinking if you want to anticipate what's likely to go wrong in future.

> The real problems facing users of intelligence systems have to do with combining data in different compartments, and downgrading it after sanitization. Lattice security models offer little help here.

> The policy goal is usually not to prevent information flowing 'down' a hierarchy but to prevent it flowing 'across' between smaller groups.

> Doctors, bankers and spies have all learned that as well as preventing overt information flows, they also have to prevent information leakage through side-channels such as billing data.

> The traditional approach to privacy, which might be summarised as 'consent or anonymise', is being undermined by growing complexity with many outsourced systems that are often opaque even to doctors (let alone patients).

## Anti-Patterns & Fixes

- Over-Centralization: Aggregating all sensitive data into one system to improve sharing simultaneously maximizes attacker value and insider threat surface. Fix: Partition data into compartments with incompatible labels; grant access only to the compartment relevant to a user's current task.
- Flat Access on Seniority: Granting cumulative access to many compartments as a reward for long service (e.g., Aldrich Ames) creates catastrophic insider threat potential. Fix: Enforce need-to-know per compartment regardless of seniority; regularly audit and revoke stale access.
- Treating Anonymization as a Privacy Silver Bullet: Building 'anonymised' databases of rich records assumes re-identification is impossible, but computer scientists have known since the 1980s this is far harder than it looks. Fix: Apply formal de-identification theory (e.g., k-anonymity, differential privacy) and assess re-identification risk before releasing aggregate data.
- Using the OS as a Sharing Mechanism After Labeling It for Isolation: Mandatory access control products used for compartmentation turn the OS into an isolation mechanism, making legitimate data combination across compartments operationally impossible. Fix: Design explicit, audited downgrade/sanitization workflows rather than relying purely on label-based blocking.
- Uniform Navy-Style Key Distribution: Operational necessity (a ship can be sent anywhere) forced all 800 US Navy ships onto the same cipher keys, which the Walker family then sold wholesale. Fix: Design for operational flexibility from the start with key hierarchies or per-mission keying rather than retrofitting uniformity.
- Ignoring Side-Channel Leakage: Restricting record content while leaving billing, scheduling, or referral metadata accessible leaks sensitive inferences (e.g., patient X paid specialist Y implies diagnosis). Fix: Apply boundary controls to all correlated metadata, not just primary record content.

## When To Apply

Load this page when:

- Use this when designing an API or database schema that must serve multiple organizational units where one unit should not see another's data (e.g., multi-tenant SaaS, federated health systems).
- Use this when implementing access control for a system where the same data store is accessed by users with conflicting interests (e.g., financial advisors whose clients compete with each other).
- Use this when a feature request asks for 'data sharing' between departments, teams, or organizations and the requester has not specified what lateral boundaries must be preserved.
- Use this when generating code that aggregates or exports records and the records contain quasi-identifiers that could enable re-identification even after obvious PII is stripped.
- Use this when building role-based access control and the role definitions are being inherited from organizational hierarchy rather than derived from actual data-access need.
- Use this when a logging, billing, or audit system is being designed alongside a privacy-sensitive primary system, as the metadata may leak as much as the primary data.
- Use this when a system's access model relies on a single classification level (e.g., 'Top Secret') without codeword-style compartments, and the user population with that level exceeds a small, well-audited group.
- Use this when evaluating whether a proposed 'anonymized' data release from a rich dataset is actually safe to publish externally.

## Concrete Examples

- Ultra codeword in WWII: Only a tiny compartment of Allied leaders and generals could access Enigma decrypts; Churchill received summaries in a locked dispatch box inaccessible to his own staff.
- Aldrich Ames CIA case: Long-service counterintelligence officer accumulated access to a large number of compartments and betrayed nearly the entire US agent network in Russia.
- Walker spy case: Operational necessity forced all 800 US Navy ships onto the same cipher keys, which were then sold wholesale to the Russians.
- UK Children's Database (ContactPoint): Parliament shut it down in 2010 after realizing that giving doctors, teachers, and social workers shared access to all children's data was both unsafe and illegal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Boundaries**

An LLM coding agent defaults to generating the simplest schema and access control that satisfies the stated functional requirement, which almost always means a flat, centralized model with role-based read permissions — exactly the over-centralization anti-pattern. The agent has no visibility into cross-unit conflict-of-interest risks or side-channel leakage through metadata it generates (e.g., audit logs, foreign keys, timestamps), so it will produce code that is functionally correct but structurally violates lateral boundary requirements. Agents must be explicitly prompted with compartment boundaries, conflict-of-interest rules, and metadata leakage constraints before generating any multi-tenant or multi-role data access layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Multilevel Security MLS Information Flow Control IFC a mandatory access control

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

---

## Security Policy Model a succinct one page or less statement of protection proper

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
