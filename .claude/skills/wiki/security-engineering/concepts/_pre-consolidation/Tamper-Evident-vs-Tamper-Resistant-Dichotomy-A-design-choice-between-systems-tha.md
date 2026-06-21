---
title: Tamper-Evident vs. Tamper-Resistant Dichotomy: A design choice between systems that make key extraction obvious after the fact (tamper-evident) versus systems from which keys cannot be readily extracted at all (tamper-resistant)
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Tamper-Resistance.json]
contributing_chapters: ["Tamper Resistance"]
confidence: high
---

# Tamper-Evident vs. Tamper-Resistant Dichotomy: A design choice between systems that make key extraction obvious after the fact (tamper-evident) versus systems from which keys cannot be readily extracted at all (tamper-resistant)

> From chapter: *Tamper Resistance*

## Core Principle

Tamper resistance is not a binary property but an evolving equilibrium between attack and defence, where the weakest link is almost always an interface — human, sensor, or system — rather than the cryptographic core itself. Effective tamper-resistant design requires defining a precise threat model, separating serviceable components from the security core, enforcing shared control procedures that cannot be shortcut, and recognising that hardware security modules are components in a larger system, not self-contained solutions. Security that relies on high technology without proportional critical thinking consistently fails.

## Key Heuristics

These are the load-bearing rules for this concept.

> The amount of careful, critical security thinking that has gone into a given security device, system or program is inversely proportional to the amount of high-technology it uses. — Roger Johnston

> It is relatively easy to build an encryption system that is secure if it is working as intended and is used correctly but it is still very hard to build a system that does not compromise its security in situations in which it is either misused or one or more of its sub-components fails. — Brian Gladman

> The goal was 'to reduce the street value of key material to zero'.

> Security is not some kind of magic pixie dust that you sprinkle on a system to cause bad things to not happen. You need to work out what bad things you want to stop.

> Tamper-resistant devices are more often a useful component than a full solution.

> Shared control is a serious security usability hazard.

> Security processors are typically vulnerable to attacks on interfaces (human, sensor or system) but can often deliver value in applications where we need to link processing to physical objects and to protect security state against scalable threats.

> Generic mechanisms fail again and again.

## Anti-Patterns & Fixes

- High-Tech Security Theatre: Assuming that more sophisticated technology automatically means more security. Fix: Apply critical security thinking proportional to the threat model, not the technology budget; evaluate the actual attack surface rather than the spec sheet.
- Shared Control Usability Failure: Giving both key components to a single person (e.g., an engineer) to avoid inconvenience, nullifying dual-custody. Fix: Enforce procedural and technical controls so that key components are physically and organisationally separated and cannot be presented to any single individual.
- Serviceable-Core Co-location: Mixing serviceable components (batteries, connectors) with the tamper-sensitive core, allowing a maintenance engineer to disable sensors on one visit and extract keys on the next. Fix: Physically segregate serviceable components from the potted, sensor-guarded cryptographic core.
- Cleartext Key Storage: Storing master keys as readable PROMs or paper printouts that can be pocketed or copied. Fix: Use split key components stored in separate safes under separate departmental control, combined only inside the HSM.
- Interface Trust Assumption: Trusting user-facing or system-facing interfaces of a secure module without independently validating inputs, allowing PIN block substitution, API abuse, or keystroke-logging attacks on entry. Fix: Validate all inputs at the hardware boundary; treat every interface as adversarial.
- Sprinkle-On Security: Bolting on smartcards or crypto modules to a system without defining what specific threats they address. Fix: Define the precise threat model and required protection property first, then select the appropriate tamper-resistance mechanism.

## When To Apply

Load this page when:

- Use this when designing or reviewing code that generates, stores, or transmits cryptographic key material on a device that could be physically accessed by an untrusted party.
- Use this when implementing a Hardware Security Module (HSM) API integration and deciding what operations must occur inside the module boundary versus in application code.
- Use this when writing firmware or bootloader code that depends on a TPM or secure enclave for attestation or key sealing.
- Use this when evaluating whether a tamper-resistant chip (smartcard, SIM, payment terminal) is the right architectural component for a given confidentiality or integrity requirement.
- Use this when implementing shared-secret or threshold key loading procedures and specifying the operational ceremony in code or documentation.
- Use this when assessing side-channel risks in cryptographic implementations running on embedded hardware (e.g., choosing constant-time algorithms, evaluating power analysis exposure).
- Use this when designing a supply-chain integrity check for hardware components or evaluating hardware Trojan detection requirements.
- Use this when specifying the threat model for a system that must operate in an unattended or adversarially-accessible physical environment (ATMs, vending machines, point-of-sale terminals).

## Concrete Examples

- IBM 4758 cryptoprocessor: first commercial product evaluated to FIPS 140-1 Level 4, featuring potted epoxy core, tamper-sensing mesh, EM shielding, and zeroizing SRAM — used as the canonical case study for HSM attack and defence cycles.
- Walker family espionage: US Navy key material sold to Russians for 20+ years, motivating the design goal of reducing 'the street value of key material to zero' through tamper-resistant and tamper-evident packaging.
- Dishonest engineer keystroke logger: an engineer got bank custodians to enter master key components into a laptop acting as a terminal with logging enabled, bypassing dual-custody entirely.
- Paper master keys in branch correspondence file: ATM master keys stored in a bank branch filing cabinet accessible to any staff member, illustrating how procedural failures negate hardware security.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Tamper Resistance**

An LLM coding agent is particularly prone to generating cryptographic key-handling code that silently violates tamper-resistance assumptions — for example, logging key material to standard output during debugging, storing keys in memory regions accessible to the host OS rather than inside an HSM boundary, or implementing dual-custody ceremonies as simple boolean flags that a single code path can bypass. Unlike a human engineer who experiences the physical inconvenience of custody procedures and may notice a maintenance engineer acting suspiciously, an agent has no physical context and will optimise for code that compiles and passes unit tests, not for operational security ceremonies that are hard to encode as tests. Agents should be explicitly prompted to identify every location where key material crosses a trust boundary and to enforce that cryptographic operations occur inside the hardware security boundary, never outside it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
