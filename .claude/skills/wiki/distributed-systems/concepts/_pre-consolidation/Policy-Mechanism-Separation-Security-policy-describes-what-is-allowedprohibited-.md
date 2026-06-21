---
title: Policy-Mechanism Separation: Security policy describes what is allowed/prohibited; security mechanisms (encryption, authentication, authorization, auditing) enforce that policy — these must be designed independently
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, distributed-systems, concept]
sources: [extracts/distributed-systems/Security.json]
contributing_chapters: ["Security"]
confidence: high
---

# Policy-Mechanism Separation: Security policy describes what is allowed/prohibited; security mechanisms (encryption, authentication, authorization, auditing) enforce that policy — these must be designed independently

> From chapter: *Security*

## Core Principle

Security in distributed systems requires pervasive, policy-driven design across secure channels (authentication, integrity, confidentiality), access control (ACLs or certificates, post-authentication), and security management (key distribution, delegation, revocation). The four threat categories — interception, interruption, modification, fabrication — provide a complete taxonomy for threat modeling, while the mechanisms of encryption, authentication, authorization, and auditing form the enforcement toolkit. A single unaddressed design flaw can nullify all other security measures, making systematic policy-first design non-negotiable.

## Key Heuristics

These are the load-bearing rules for this concept.

> A single design flaw with respect to security may render all security measures useless.

> Security needs to be pervasive throughout a system.

> Building all kinds of security mechanisms into a system does not really make sense unless it is known how those mechanisms are to be used, and against what.

> Access control always takes place after a process has been authenticated.

> The main benefit of using certificates is that a process can easily pass its ticket to another process, that is, delegate its access rights.

> Certificates, however, have the drawback that they are often difficult to revoke.

> Current practice shows the use of public-key cryptography for distributing short-term shared secret keys [session keys].

> A practical solution is to name an object by taking the hash of its public key, along with a human-readable label (which should also be securely bound to the object).

## Anti-Patterns & Fixes

- AdHocSecurityWithoutPolicy: Adding security mechanisms without a defined security policy means you cannot know what you are protecting or whether mechanisms are correctly applied. Fix: Define a security policy first — specifying exactly which actions entities are allowed or prohibited — then design mechanisms to enforce it.
- AuthenticationBeforeAuthorization-Inversion: Performing authorization checks before identity is verified leads to granting rights to unverified principals. Fix: Always authenticate first, then authorize.
- PermanentSharedKeyUsage: Using long-lived symmetric keys for all communication increases exposure window if a key is compromised. Fix: Use public-key cryptography only to exchange short-lived session keys; use session keys for actual communication.
- UnboundHumanFriendlyNames: Using human-readable names without cryptographic binding allows name-to-object substitution attacks. Fix: Bind names to objects by hashing the object's public key and securely associating the human-readable label.
- UnrestrictedMobileCode: Running mobile code (agents) without access control boundaries allows arbitrary resource access. Fix: Apply sandbox or protection domain mechanisms to constrain what mobile code can access.
- IrrevocableCertificateDelegation: Relying solely on certificates for access control without a revocation plan leaves access open even after rights should have been removed. Fix: Pair certificate-based authorization with a revocation mechanism or use short-lived certificates.

## When To Apply

Load this page when:

- Use this when designing inter-service communication in a distributed system and needing to decide how to protect messages in transit (choose secure channel with mutual authentication + confidentiality).
- Use this when generating code that grants a process access to a resource and needing to decide between ACLs and capability certificates (consider revocability vs. delegation needs).
- Use this when writing code that accepts or executes mobile/agent code from external sources (apply sandbox or protection domain access control before execution).
- Use this when implementing a naming or lookup service and needing to bind a name to an object securely (hash the public key and bind the human-readable label cryptographically).
- Use this when a service needs to verify a caller's identity before performing work on their behalf (implement authentication step before any authorization or business logic).
- Use this when distributing cryptographic keys between services (use public-key cryptography to bootstrap a short-lived session key, not for bulk encryption).
- Use this when evaluating whether a system is secure holistically (audit all four threat categories: interception, interruption, modification, fabrication — and verify policy coverage for each).
- Use this when an agent needs to delegate its access rights to a sub-process or downstream service (use certificate-based delegation with a nonce-challenge proof of secret ownership).

## Concrete Examples

- A nonce N encrypted with a public key S+proxy is sent to Bob; Bob decrypts and returns N to prove he holds the private key S-proxy and is the rightful certificate holder — demonstrating secure delegation.
- Denial-of-service attacks are classified as the 'interruption' threat type, where a malicious party makes a service inaccessible to others.
- Breaking into a password file to add an unauthorized entry is given as an example of the 'fabrication' threat.
- Replaying previously sent messages to gain unauthorized access is cited as an example of fabrication-based attack.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Security**

An LLM coding agent is especially prone to generating code that implements security mechanisms (e.g., encryption, token checks) without first encoding a security policy, producing the 'AdHocSecurityWithoutPolicy' anti-pattern at scale across many generated files. Agents also tend to inline long-lived secrets or symmetric keys directly rather than generating session-key negotiation flows, and may omit authentication gates before authorization logic since they pattern-match to common code snippets that skip this step. Applying the Policy-Mechanism Separation framework forces the agent to explicitly represent what is permitted before generating any enforcement code, and the Four Threats Model provides a checklist the agent can systematically verify generated components against.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
