---
title: Three-Level Inspection Model: Security features must be evaluated at primary (untrained public), secondary (field expert with limited tools), and tertiary (lab expert with full equipment) inspection levels — secondary is the critical battleground
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Security-Printing-and-Seals.json]
contributing_chapters: ["Security Printing and Seals"]
confidence: high
---

# Three-Level Inspection Model: Security features must be evaluated at primary (untrained public), secondary (field expert with limited tools), and tertiary (lab expert with full equipment) inspection levels — secondary is the critical battleground

> From chapter: *Security Printing and Seals*

## Core Principle

Physical security seals and security printing illustrate that any protection system is only as strong as the humans who apply and inspect it, the full lifecycle over which it operates, and the layering of defenses against adversaries at all capability levels. The critical insight is that secondary inspection (field-level, motivated but resource-limited) is the real battleground, and defeating a seal is fundamentally about deceiving people rather than defeating hardware. These principles generalize directly to software supply chain integrity, credential systems, and any security mechanism that depends on human verification at any stage.

## Key Heuristics

These are the load-bearing rules for this concept.

> A seal is only as good as the man in whose briefcase it's carried.

> You can't make something secure if you don't know how to break it.

> Getting a counterfeit past a primary inspection is usually easy, while getting it past tertiary inspection is usually impossible if the product and the inspection process have been competently designed.

> Defeating seals is about fooling people, not beating hardware.

> Most commercially available sealing products are relatively easy to defeat, and this is particularly true when seal inspection is performed casually by people who are untrained, unmotivated or both.

> No matter how sophisticated the cryptography, a defeat for the seals can be a defeat for the system.

> It may be a more realistic goal to make credentials tamper evident rather than tamper proof.

> Think hard whether the people who apply and check the seals will perform their tasks faithfully and effectively; analyze motive, opportunity, skills, audit and accountability.

## Anti-Patterns & Fixes

- Titanic Effect (Over-Trust in Latest Technology): Designers place excessive faith in a single novel security technique (e.g., the UK window thread), assuming it cannot be defeated, and neglect defense-in-depth. Fix: Use multiple layered security features and assume any single technique will eventually be defeated; conduct hostile testing.
- Ignoring the Human Layer: Treating seal or credential security as purely a hardware/cryptography problem while ignoring that inspectors may be untrained, unmotivated, or corruptible. Fix: Explicitly model inspector motivation and competence; design for the weakest realistic inspector, not the ideal one.
- Pre-Installation Vulnerability Neglect: Assuming a security product is safe once deployed, without accounting for tampering during distribution before installation. Fix: Use tamper-evident packaging for the security product itself and establish trusted distribution chains.
- Single-Point Credential Trust: Relying solely on electronic reading of credentials (e.g., RFID cards) without visual inspection, making the system vulnerable to cloning attacks. Fix: Combine electronic verification with visual inspection of security printing on credentials.
- Broken Market Ignoring System-Level Issues: Deploying new technical countermeasures (nanoparticles, DNA markers, etc.) without addressing the systemic market and inspection failures that make existing countermeasures ineffective. Fix: Analyze and fix the system-level incentive and inspection failures before layering on new technology.
- Seal Applied by the Adversary: Allowing the entity being controlled (e.g., contract manufacturer) to apply the seal themselves, creating an obvious conflict of interest and defeat vector. Fix: Ensure seals are applied by a trusted independent party, or design the system so adversarial application is detectable.

## When To Apply

Load this page when:

- Use this when designing a software supply chain integrity check (e.g., code signing, artifact hashing) to ensure verification steps account for human inspector motivation and skill, not just cryptographic validity.
- Use this when implementing a license or credential verification system to ensure that cryptographic checks are complemented by additional tamper-evident signals that survive partial compromise.
- Use this when evaluating a dependency or third-party library inclusion process, to apply whole-life-cycle thinking: who controls the package from publication through installation and update?
- Use this when specifying threat models for authentication tokens or secure packaging of secrets (API keys, certificates) to categorize attacks by attacker capability (amateur, organized criminal, nation-state).
- Use this when designing audit logging or tamper-detection for configuration files or build artifacts, to ensure that tampering is detectable even if not preventable.
- Use this when reviewing a security feature that relies on a single novel mechanism, to check for Titanic Effect over-confidence and ensure defense-in-depth.
- Use this when assessing a system where the party being verified also controls part of the verification infrastructure (e.g., self-reported telemetry, contractor-managed monitoring), to identify adversarial application anti-patterns.
- Use this when building automated inspection pipelines for code or artifacts to map checks to primary/secondary/tertiary inspection levels and ensure secondary-level checks are the focus of adversarial hardening.

## Concrete Examples

- British banknote window thread forgery: criminals used hot stamping and white ink to simulate the embedded metal strip, forging tens of millions of pounds worth of notes over several years — defeating a feature designers believed was unforgeable.
- Mifare contactless card cloning: building entry control cards can be electronically cloned, meaning visual inspection of security printing on physical ID remains relevant even when electronic reading is present.
- Supernote controversy: near-perfect counterfeit US currency attributed to either North Korea or the CIA, designed to pass all inspections except bank counting machines, appearing only in tiny quantities in the hands of intelligence targets.
- Cold chain assurance: temperature loggers and chemical telltale strips on vaccine shipments that change their displayed barcode if the cold chain is broken — an example of automated primary-level tamper detection.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Security Printing and Seals**

An LLM coding agent is especially prone to the Titanic Effect: it will confidently implement a single cryptographic or hashing mechanism (e.g., HMAC signature on a config file) and treat that as sufficient, without modeling the human verification layer or the full lifecycle of the artifact. The agent also tends to treat credential or artifact verification as a binary pass/fail at one point in time, missing that the critical attack surface is the distribution and application phase before verification occurs. Applying this chapter's frameworks, an agent should be prompted to explicitly enumerate who applies, who checks, and what their incentives are — not just whether the cryptographic primitive is correct.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
