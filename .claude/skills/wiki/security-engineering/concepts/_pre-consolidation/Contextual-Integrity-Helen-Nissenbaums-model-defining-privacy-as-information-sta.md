---
title: Contextual Integrity: Helen Nissenbaum's model defining privacy as information staying within its originating context; violations occur when data crosses context boundaries
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Side-Channels.json]
contributing_chapters: ["Side Channels"]
confidence: high
---

# Contextual Integrity: Helen Nissenbaum's model defining privacy as information staying within its originating context; violations occur when data crosses context boundaries

> From chapter: *Side Channels*

## Core Principle

Side channels are unintended information leakage paths — electromagnetic emissions, power/timing variation, shared CPU microarchitecture, physical sensors, and social re-identification — that have caused multi-billion dollar security failures independent of whether cryptographic protocols were correctly implemented. The field is characterized by systematic underestimation of scalable new side channels and overinvestment in legacy ones, and complexity growth in hardware and software guarantees the attack surface will expand. A security engineer must be able to triage which side channels are plausible given the adversary model and system architecture, because correct and verified code provides no protection against them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Optimisation consists of taking something that works and replacing it with something that almost works but is cheaper.

> We have known about side channels for years but have consistently underestimated the importance of some, while spending unreasonable sums on defending against others.

> No matter how well it is protected by encryption and access controls while in transit or storage, most highly confidential information comes into being either as speech or as keystrokes on a laptop or phone.

> It's hard to predict which side channels will scale up to become another billion-dollar issue, but it's a good bet that some of them will.

> More than twenty years after timing attacks came along, you still can't rely on either certified products or big brand names to withstand them.

> Policymakers and the tech industry have both pretended for years to believe that de-identification of sensitive data such as medical records makes it non-sensitive — this is emphatically not the case.

> Which side channels pose a real threat will of course depend on the application, and most of them will remain of academic interest most of the time. But occasionally, they'll bite.

## Anti-Patterns & Fixes

- Assuming Verification Implies Side-Channel Safety: CPU designers assumed verified hardware did what the manual said and there was no point looking for bugs. Fix: treat formal verification and side-channel analysis as orthogonal — verified correctness says nothing about information leakage through timing, power, or speculative paths.
- De-identification Theater: Treating anonymized or de-identified datasets as non-sensitive and suitable for open use. Fix: assume re-identification is possible via auxiliary data; apply privacy-by-design and data minimization rather than relying on anonymization as a compliance shield.
- Symmetric Threat Spending: Spending billions shielding against Tempest when often nobody was listening, while underestimating scalable software side channels. Fix: perform threat modeling to rank side channels by scalability and adversary capability before committing resources.
- Shared Resource Blindness: Assuming co-located processes cannot observe each other through shared CPU caches, memory buses, or execution pipelines. Fix: treat shared hardware resources as potential covert channels; use process isolation, constant-time algorithms, and hardware partitioning where feasible.
- Optimization Without Security Accounting: Performance optimizations (speculative execution, branch prediction) introduce side channels not present in the original design. Fix: include side-channel analysis as a required step in the performance optimization review process.
- Trusting Certification Labels for Timing Safety: Relying on Common Criteria EAL4+ or similar certifications as evidence of resistance to timing attacks. Fix: independently verify constant-time properties of cryptographic implementations; certifications do not cover side-channel attack surfaces.

## When To Apply

Load this page when:

- Use this when implementing cryptographic primitives (AES, RSA, ECDSA) to ensure operations run in constant time and do not branch or index based on secret values.
- Use this when designing a multi-tenant system where processes share CPU, cache, or memory resources and one tenant must not infer another's secrets.
- Use this when evaluating whether an anonymized or pseudonymized dataset can be safely published or shared with third parties.
- Use this when adding performance optimizations (caching, speculative computation, branch prediction hints) to security-sensitive code paths.
- Use this when selecting or configuring hardware security modules (HSMs), TPMs, or smartcards for cryptographic key storage, to verify timing-attack resistance.
- Use this when designing APIs or systems that return error messages or latency differences that could reveal whether a secret value matched.
- Use this when auditing mobile or IoT applications that request access to accelerometers, gyroscopes, microphones, or cameras alongside sensitive data processing.
- Use this when collecting or aggregating user behavioral data (location history, communications metadata) that may enable re-identification of nominally anonymous records.

## Concrete Examples

- Spectre and Meltdown (2018): speculative execution exploited to allow one process to read another process's cryptographic keys from CPU state.
- Differential Power Analysis on smartcards (late 1990s): all banking smartcards on sale were found vulnerable, delaying deployment by 2-3 years.
- The Great Seal bug (1946): USSR-planted resonant cavity microphone hidden in a wooden seal gift to the US ambassador, activated by external microwave illumination and undiscovered for 6 years.
- IBM Selectric typewriter bugs in US Moscow embassy (1984): 16 bugs discovered that stored keystrokes and transmitted them in bursts.
- Wim van Eck (1985): demonstrated reconstruction of a VDU display at a distance using a modified television set, bringing Tempest to public attention.
- STM TPM timing attack (2019): ECDSA keys extracted from a Common Criteria EAL4+-certified TPM via timing side channel, enabling a real VPN product attack.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Side Channels**

An LLM coding agent is particularly prone to generating cryptographic or authentication code that is functionally correct but not constant-time — for example, using early-return string comparisons or table lookups indexed by secret bytes — because training data contains far more examples optimized for correctness and readability than for side-channel resistance. Agents also routinely generate code that shares execution context, caches, or memory with untrusted co-tenants without flagging this as a side-channel risk. The key agent-specific failure mode is that the agent cannot observe runtime power traces or timing distributions, so it must be explicitly prompted to apply side-channel-safe patterns (e.g., `hmac.compare_digest` instead of `==`, bitsliced implementations) rather than inferring the need from functional requirements alone.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
