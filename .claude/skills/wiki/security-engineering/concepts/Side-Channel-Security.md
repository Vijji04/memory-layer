---
title: Side-Channel Security
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 5 pages
---

# Side-Channel Security

> Consolidated from 5 related concept pages.

---

## Covert vs Side Channel Distinction Side channels leak information accidentally v

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

---

## Differential Power Analysis DPA Attack framework that recovers cryptographic key

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

---

## Side Channel Attack Surface Model The recognition that cryptographic implementat

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

---

## Side Channel Taxonomy Five categories of unintended information leakage 1 radiat

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

---

## TempestEmission Security Emsec The study and mitigation of compromising electrom

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
