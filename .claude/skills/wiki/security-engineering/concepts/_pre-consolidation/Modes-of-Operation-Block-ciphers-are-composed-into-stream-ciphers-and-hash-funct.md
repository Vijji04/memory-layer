---
title: Modes of Operation: Block ciphers are composed into stream ciphers and hash functions via modes of operation, each with different error propagation, pattern concealment, and integrity protection properties
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Cryptography.json]
contributing_chapters: ["Cryptography"]
confidence: high
---

# Modes of Operation: Block ciphers are composed into stream ciphers and hash functions via modes of operation, each with different error propagation, pattern concealment, and integrity protection properties

> From chapter: *Cryptography*

## Core Principle

Cryptography provides the mathematical foundation for secure systems but is extremely difficult to implement correctly, with most failures arising from misuse of strong primitives rather than weakness in the primitives themselves. The central engineering discipline is selecting appropriate algorithms, modes, and key management practices — especially avoiding insecure defaults like ECB mode and never designing custom cryptographic constructions. The overriding heuristic is 'don't roll your own': use established libraries, standard modes (preferring authenticated encryption), and always pair confidentiality with integrity protection.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't roll your own! Don't design your own protocols, or your own ciphers; and don't write your own crypto code unless you absolutely have to.

> Designing crypto is a bit like juggling chainsaws; it's just too easy to make fatal errors.

> Never use ECB mode unless you really understand what you're doing.

> We rarely get anything for nothing in cryptology, and the price of the perfect secrecy of the one-time pad is that it fails completely to protect message integrity.

> It's not enough for the keystream to appear 'random' in the sense of passing the standard statistical randomness tests: it must also have the property that an opponent who gets his hands on even quite a lot of keystream symbols should not be able to predict any more of them.

> Cryptography has often been used to protect the wrong things, or to protect them in the wrong way.

> A lot of systems fail because popular crypto libraries encourage programmers to use inappropriate modes of operation by exposing unsafe defaults.

## Anti-Patterns & Fixes

- ECB Mode Usage: Using Electronic Codebook mode encrypts identical plaintext blocks to identical ciphertext blocks, leaking patterns. Fix: Use a secure mode such as CBC, CTR, or GCM instead.
- Rolling Your Own Crypto: Designing custom ciphers, protocols, or writing crypto primitives from scratch introduces subtle, fatal errors even for experts. Fix: Use well-vetted libraries and standard algorithms; get peer review if custom work is unavoidable.
- One-Time Pad Without Integrity Protection: Relying on OTP for confidentiality while ignoring that it offers zero message integrity protection allows trivial bit-flip manipulation of ciphertext. Fix: Always pair confidentiality mechanisms with authentication/integrity checks (e.g., authenticated encryption).
- Reusing a One-Time Pad Key: Using the same key material more than once for a stream cipher destroys its security guarantees, enabling XOR-based plaintext recovery. Fix: Ensure key material is never reused; destroy it after use.
- Weak Pseudorandom Keystream: Using a keystream generator that passes statistical randomness tests but is computationally predictable from partial keystream exposure. Fix: Use a cryptographically secure pseudorandom number generator (CSPRNG) for keystream generation.
- Unsafe Library Defaults: Accepting the default mode of operation provided by APIs like Microsoft CAPI, which defaults to ECB. Fix: Explicitly specify a secure mode of operation when calling any cryptographic API.

## When To Apply

Load this page when:

- Use this when selecting an encryption mode for a block cipher in a new implementation to avoid defaulting to ECB.
- Use this when a developer or agent is tempted to implement a custom cipher, hash function, or cryptographic protocol from scratch.
- Use this when generating or seeding random numbers for cryptographic purposes to ensure a CSPRNG is used, not a standard statistical RNG.
- Use this when implementing a stream cipher or OTP-based system to verify that key material is never reused across messages.
- Use this when designing a system that encrypts data without also authenticating it, to add integrity protection (e.g., switching to AEAD/GCM).
- Use this when evaluating whether a chosen cryptographic primitive (cipher, hash, signature scheme) is appropriate for the threat model of the system.
- Use this when integrating a third-party crypto library to audit its default configurations and override any insecure defaults explicitly.

## Concrete Examples

- Julius Caesar's cipher: shifting letters by a fixed key (D for A, etc.), broken by Bernardo Provenzano in 2006 when Italian police deciphered his intercepted messages using the same technique.
- Vigenère cipher broken via Kasiski's method: repeated ciphertext patterns ('KIOV' after 9 letters, 'NU' after 6) reveal the keyword length, enabling frequency analysis on each positional subsequence.
- One-time pad spy example: ciphertext DGTYI BWPJA can be decrypted to either 'heil hitler' or 'hang hitler' depending on key, demonstrating perfect secrecy but also showing bit-flip manipulation to produce 'hang hitler' by changing one ciphertext character.
- Microsoft CAPI nudging engineers toward ECB mode as the default, illustrating how unsafe library defaults lead to weak real-world deployments.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Cryptography**

An LLM coding agent is especially prone to reproducing crypto anti-patterns from training data — including ECB mode, homebrew cipher logic, or non-CSPRNG randomness — because these patterns appear frequently in tutorials and legacy codebases. Unlike a human who can consult an expert, an agent may confidently emit plausible-looking but cryptographically broken code with no visible warning signs; enforcing hard rules like 'never ECB, always authenticated encryption, always use standard library primitives' as pre-generation constraints is critical. Agents also tend to omit integrity/authentication layers when only asked for 'encryption,' making the OTP integrity failure pattern and the encrypt-then-MAC discipline especially important to bake into agent-level defaults.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
