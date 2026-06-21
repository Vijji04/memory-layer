---
title: Protocol Security
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 5 pages
---

# Protocol Security

> Consolidated from 5 related concept pages.

---

## Formal Verification of Protocols Using theorem provers eg Isabelle or model chec

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

---

## Forward Secrecy via Ephemeral Keys The Signal protocol design principle that key

## Core Principle

Advanced cryptographic components—FDE, Signal, Tor, HSMs, enclaves, and blockchains—serve as trusted platforms for complex systems, but each carries substantial hidden complexity, performance costs, and inevitable entanglement with policy and liability that make them far messier than their mathematical foundations suggest. Real-world deployments consistently show that features added over time break security properties, that capable adversaries exploit implementation gaps years after attacks are published, and that 'trustless' systems in practice concentrate trust in developers, miners, or hardware vendors. The chapter's core lesson is TANSTAAFL: cryptography is not magic, and the decision to deploy an advanced crypto mechanism must weigh its full costs against its actual—not assumed—threat model.

## Key Heuristics

These are the load-bearing rules for this concept.

> Whoever thinks his problem can be solved using cryptography, doesn't understand his problem and doesn't understand cryptography.

> Give me a rock on which to stand, and I will move the world.

> TANSTAAFL: there ain't no such thing as a free lunch.

> Even the simplest of encryption products has a significant entanglement with compliance, is much more complex under the hood than you might think at first glance, usually imposes some performance penalty, and can be vulnerable to a capable opponent – even years after the relevant attacks have been published.

> The real consensus is not cryptographic but social; it's the consensus of the developers.

> If you can extract the master secret key from an SGX chip, you can break the whole ecosystem.

> A cryptocurrency can go on acquiring features until they break it, and smart contracts can help the process along.

## Anti-Patterns & Fixes

- Tick-Box Encryption Compliance: Encrypting S3 buckets because auditors demand it, when the actual failure mode is misconfigured access controls, not physical theft. Fix: Identify the real threat model before selecting a cryptographic control; encryption addresses confidentiality from physical access, not logical access misconfiguration.
- FDE as Magic Insurance: Assuming full-disk encryption eliminates all risk and therefore not reporting lost devices, even when the password may have been observed. Fix: Treat FDE as one layer of defense, not a complete solution; enforce incident reporting regardless of encryption status.
- Feature Creep Breaking Cryptosystems: HSMs and blockchains acquiring ever more features until those features introduce exploitable attack surfaces. Fix: Freeze the API surface of cryptographic components early and resist feature additions; use separate non-crypto components for new functionality.
- Third-Party FDE Over Platform-Integrated FDE: Using standalone third-party encryption products that lack integration with trusted boot, key management, and recovery. Fix: Use vendor-integrated FDE (BitLocker, FileVault) which coordinates with TPM, secure boot, and key escrow workflows.
- Long-Lived Key Material in Messaging: Relying on a single long-lived private key in a messaging app, exposing all past communications if the device is compromised. Fix: Implement forward secrecy with ephemeral per-session keys as Signal does, so key compromise has bounded impact.
- Ideological Trustlessness Without Engineering Reality: Claiming smart contracts or DEXs are trustless while hard-coding admin keys for emergency intervention. Fix: Be explicit about trust assumptions; document privileged intervention paths rather than obscuring them behind decentralization rhetoric.

## When To Apply

Load this page when:

- Use this when designing a system that stores sensitive data at rest and you must choose between software FDE, hardware FDE, or cloud bucket encryption.
- Use this when implementing a messaging or communication protocol and must decide how to handle key compromise and device loss scenarios.
- Use this when selecting or integrating an HSM, enclave (SGX/TrustZone), or blockchain as a trust anchor for a payment or authentication system.
- Use this when a compliance requirement mandates encryption and you need to evaluate whether the prescribed control actually addresses the real threat.
- Use this when architecting a cryptographic API and must decide how many features or operations to expose through a single interface.
- Use this when evaluating whether a decentralized cryptographic system (blockchain, Tor, Signal) can be safely updated or patched after deployment.
- Use this when a system design claims to be 'trustless' and you need to audit the actual trust assumptions embedded in it.
- Use this when assessing the total cost of deploying an advanced cryptographic component including performance overhead, maintenance, and regulatory liability.

## Concrete Examples

- Cold boot attacks (2008, Princeton): DRAM frozen to recover transient FDE keys, defeating all major FDE products of the time and remaining a threat on many machines.
- Android factory reset flaw (2015): Most OEMs so poorly engineered factory reset that FDE keys and credentials could be recovered from second-hand devices.
- Third-party FDE market failure (2019, Meijer & van Gastel): Three products holding 60% of FDE market were insecure; BitLocker disabled itself when they were present.
- EncroChat crypto phone: Hidden partition containing encrypted chat and VOIP apps, sold to criminals as a covert communications platform.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Advanced Cryptographic Engineering**

An LLM coding agent is especially prone to the 'magic crypto' anti-pattern: when asked to add security to a system, it will reach for well-known cryptographic primitives (AES encryption, TLS, JWT signing) and apply them correctly at the code level while completely missing whether they address the actual threat model—exactly the failure the Needham-Lampson quote warns against. Agents also tend to generate cryptographic integrations that work in isolation but fail at platform boundaries (key derivation from weak passwords, no TPM binding, no forward secrecy), because they optimize for the local code correctness visible in context rather than the system-wide trust assumptions that require architectural knowledge. This chapter's framework of TANSTAAFL cost accounting and policy entanglement is particularly important for agents to internalize, since agents rarely flag the operational, compliance, and liability costs of cryptographic choices they generate.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Key Diversification Key Derivation Deriving per device keys from a master key KT

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

---

## Protocol Robustness Principles Design rules requiring that protocol interpretati

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

---

## Security Protocol Model A formal specification of steps principals use to establ

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
