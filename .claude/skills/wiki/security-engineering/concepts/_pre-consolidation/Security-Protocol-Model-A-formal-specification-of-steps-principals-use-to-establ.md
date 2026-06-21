---
title: Security Protocol Model: A formal specification of steps principals use to establish trust relationships, written as T→G : T, {T,N}KT notation, making all actors, messages, and cryptographic bindings explicit
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Protocols.json]
contributing_chapters: ["Protocols"]
confidence: high
---

# Security Protocol Model: A formal specification of steps principals use to establish trust relationships, written as T→G : T, {T,N}KT notation, making all actors, messages, and cryptographic bindings explicit

> From chapter: *Protocols*

## Core Principle

Security protocols specify the steps principals use to establish trust, and are the meeting point of cryptography, access control, and system design. They are notoriously difficult to get right, failing through replay attacks, reflection attacks, middleperson attacks, assumption drift, and scope gaps in formal verification. The core lesson is to never design novel protocols without specialist help and public peer review, to make all assumptions and message contents fully explicit, and to re-evaluate protocols whenever their deployment environment changes.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is impossible to foresee the consequences of being clever.

> If it's provably secure, it probably isn't.

> Please don't design your own protocols; get a specialist to help, and ensure that your design is published for thorough peer review by the research community.

> Even specialists get the first versions of a protocol wrong (I have, more than once).

> It's a lot cheaper to fix the bugs before the protocol is actually deployed, both in terms of cash and in terms of reputation.

> The interpretation of a protocol should depend only on its content, not its context; so everything of importance (such as principals' names) should be stated explicitly in the messages.

> Randomness in protocol often helps robustness at other layers, since it makes it harder to do a whole range of attacks.

> Some of the most pernicious failures are caused by creeping changes in the environment for which a protocol was designed, so that the protection it gives is no longer relevant.

## Anti-Patterns & Fixes

- Static Serial Number as Password: Broadcasting a fixed serial number as authentication allows replay ('grabber') attacks. Fix: Use a nonce-based challenge-response or rolling code so each authentication message is unique and cannot be replayed.
- Insufficient Nonce/Key Length: Doubling password length from 16 to 32 bits while keeping the same static-code structure ('proudly advertised over 4 billion codes') still allows grabber attacks. Fix: Use cryptographic authentication with nonces, not just longer static codes.
- Key Strength Undermined by Short Derivation Input: Using 128-bit keys derived from a 16-bit device number gives only 16-bit effective security. Fix: Ensure the entropy of key derivation inputs matches the desired key strength end-to-end.
- Protocol Verified But Incompletely Scoped: SSL/TLS was formally verified in 1998, yet ~1 security bug per year was found afterward in unverified added features and implementation details. Fix: Treat formal verification as scoped, not total; re-verify when features are added and separately audit implementations.
- Assumption Drift: Designing a protocol under a reasonable threat model (e.g., hard-wired terminals) and continuing to use it after the environment changes (e.g., internet login) without reassessing threats. Fix: Explicitly document threat model assumptions and revisit them whenever deployment context changes.
- Relay Attack Blindness on Proximity Protocols: Keyless entry systems assumed key proximity was unforgeable; relay devices extended effective range, enabling theft. Fix: Include explicit distance-bounding or cryptographic proximity verification, not just signal presence.

## When To Apply

Load this page when:

- Use this when generating any authentication handshake or login protocol between two or more parties to ensure nonces, explicit principal names, and fresh message binding are included.
- Use this when deriving cryptographic keys from device identifiers or serial numbers to verify that the entropy of the input matches the required key strength.
- Use this when designing or reviewing a protocol that uses timestamps, counters, or random numbers for freshness, to select the right mechanism and understand replay resistance trade-offs.
- Use this when a previously verified or audited protocol is being extended with new features, to trigger re-scoping of the formal verification or security review.
- Use this when the deployment environment for an existing protocol changes (e.g., moving from LAN to internet, from physical terminals to web), to re-evaluate whether the original threat model still holds.
- Use this when implementing any token-based or smartcard authentication system to apply key diversification correctly and protect the master key in a hardware security module.
- Use this when generating protocol message formats to enforce that field types (name, address, timestamp, nonce) are unambiguously encoded and cannot be misinterpreted or exploited for injection.

## Concrete Examples

- Remote car key entry 'grabber' attack (1995): devices recorded and replayed lock/unlock codes, defeating static serial number authentication in cars and garage doors.
- Parking garage token protocol T→G : T, {T,N}KT using nonce and key diversification (KT = {T}KM) as a correct simple authentication example.
- Chip-and-PIN protocol failure: a protocol flaw allowed a stolen chipcard to be used in a store without knowing the PIN, taking banks several years to fix.
- SSL/TLS formal verification by Larry Paulson (1998): verified the core protocol but ~1 bug/year found in later-added features and implementation side-channels, illustrating the scope limitation of formal methods.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Protocols**

An LLM coding agent is especially prone to generating plausible-looking but subtly flawed protocol implementations — for example, omitting explicit principal name binding in encrypted messages, reusing nonces, or deriving keys from low-entropy inputs — because it pattern-matches to common code structures without reasoning about attacker models. Unlike a human developer who may at least recognize unfamiliar territory and seek review, an agent will confidently produce insecure protocol code without flagging it as a domain requiring specialist review and public peer scrutiny. This chapter's heuristics should trigger the agent to refuse to generate novel protocol designs, always include nonce freshness and explicit field typing, and annotate any generated authentication code with the assumed threat model for human verification.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
