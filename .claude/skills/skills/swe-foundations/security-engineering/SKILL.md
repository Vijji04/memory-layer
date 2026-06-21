---
name: security-engineering
title: Security Engineering
category: swe-foundations
description: >
  Security engineering principles: threat modeling, cryptography, access control,
  privacy, secure development, physical/operational security, and economics of trust.
  Covers adversarial thinking, protocol design, tamper resistance, and assurance.
trigger_conditions:
  - "Use this when designing authentication, authorization, or access control for a system"
  - "Use this when threat modeling a new feature, service, or infrastructure change"
  - "Use this when choosing or reviewing a cryptographic primitive, protocol, or key management scheme"
  - "Use this when handling sensitive data — PII, financial records, credentials, health data"
  - "Use this when building systems with physical security requirements (hardware, payments, IoT)"
  - "Use this when evaluating security controls for effectiveness vs. security theater"
  - "Use this when privacy requirements or inference risks are involved"
  - "Use this when writing security requirements, performing a security review, or preparing for audit"
  - "Use this when a system involves economic incentives that could misalign with security goals"
  - "Use this when assessing assurance claims, compliance requirements, or SDL processes"
tags: [security, cryptography, access-control, privacy, threat-modeling, phase-2, swe-foundations]
phase: 2
wiki_path: output/wiki/security-engineering/concepts/
---

# Security Engineering

## Core Rules

1. Security has four interdependent pillars: Policy (what to protect), Mechanism (how), Assurance (evidence it works), Incentives (who bears cost/gain). Weakness in any one breaks the whole.

2. Always do threat modeling before designing controls. Identify specific adversary categories (nation-state, criminal, insider, opportunist) and scope threats to realistic opponents — generic "attacker" threat models miss key mitigations and over-engineer for irrelevant threats.

3. Never confuse security theater with real protection. Visible controls that look strong but provide no actual resistance waste budget and create false confidence. Test controls against actual attack paths.

4. Access control belongs in the mechanism layer, not just policy. Choose DAC vs MAC vs RBAC based on trust model: DAC for user-controlled data, MAC for multi-level confidentiality, RBAC for organizational roles. TOCTTOU is a common implementation failure — check and use must be atomic.

5. Cryptography is a component, not a solution. Cryptographic strength is useless if key management fails, protocols have logic flaws, or side-channel leakage exposes secrets. Always evaluate the full stack: algorithm + mode + protocol + implementation + key lifecycle.

6. Human factors are not optional. Security mechanisms fail when cognitive load exceeds user capacity (Whitten-Tygar). Apply affordances, nudges, and choice architecture to make the secure path the path of least resistance.

7. Economics drives security outcomes. Misaligned incentives — where the party responsible for security doesn't bear the cost of failure — produce persistent vulnerabilities. Externalities, market lemons, and network lock-in all degrade security. Fix incentives before adding mechanisms.

8. Privacy is contextual integrity, not secrecy. Information flows are appropriate when they match the norms of the context in which data was shared. Re-identification risks exist even in aggregate statistical releases — apply differential privacy for query-based access.

9. Physical security follows Deter-Detect-Alarm-Delay-Respond. Each layer buys time for the next. Tamper-evident beats tamper-proof as a realistic goal — make attacks visible and expensive, not impossible.

10. For high-assurance systems: minimize the Trusted Computing Base (TCB). The smaller the component that must be trusted absolutely, the easier verification becomes. Hardware roots of trust (TPM, enclaves) anchor the chain.

11. Secure development is a lifecycle discipline, not a gate. SDL, DevSecOps, and continuous assurance require integrating threat modeling, static analysis, fuzz testing, and pen-testing at every phase — not just pre-release.

12. Side channels are real attack surfaces. Timing, power, EM emissions, and cache behavior leak cryptographic secrets even when algorithms are mathematically sound. For security-critical implementations, validate countermeasures (DPA resistance, constant-time code, TEMPEST shielding).

---

## Concept Map

| Concept Page | What It Covers |
|---|---|
| Security-Foundations | PMAI framework, security theater detection, hack-as-loophole, vulnerability taxonomy |
| Threat-Modeling | Adversary taxonomy, threat scoping, abusability analysis, ABCD threat categories |
| Human-Factors-and-Usability | Skill-Rule-Knowledge errors, affordances, dual-process cognition, nudge design |
| Protocol-Security | Protocol robustness principles, formal verification, key derivation, forward secrecy |
| Cryptography | Perfect secrecy, symmetric vs asymmetric, modes of operation, concrete security |
| Advanced-Cryptographic-Engineering | HSMs, enclaves, TANSTAAFL tradeoffs, crypto-policy entanglement |
| Access-Control | ACL vs capabilities, DAC/MAC/RBAC, protection domains, TOCTTOU |
| Multilevel-Security | Bell-LaPadula, MLS/IFC, compartmentation, Chinese Wall, multilateral security |
| Privacy-and-Inference-Control | Differential privacy, cell suppression, tracker attacks, re-identification waves |
| Economics-of-Security | Misaligned incentives, externalities, market lemons, network lock-in |
| Physical-Security | CPTED, defensible space, deter-detect-alarm-delay-respond, ROC tradeoffs |
| Financial-Security-Controls | Double-entry bookkeeping, dual control, separation of duty, audit trails |
| Metering-and-Token-Security | Key diversification, token binding, grey-listing, offline fraud tolerance |
| Critical-Systems-Security | Shared control, permissive action links, defense in depth, subliminal channels |
| Security-Printing-and-Seals | Three-level inspection, whole life-cycle assurance, predator-prey coevolution |
| Biometrics | EER, ROC tradeoffs, attended vs unattended operation, goats exclusion |
| Tamper-Resistance | FIPS 140 levels, attack-defense arms race, hardware roots of trust |
| Side-Channel-Security | Side-channel taxonomy, DPA attacks, TEMPEST/EMSEC, covert vs side channels |
| Network-Security | Zero Trust/BeyondCorp, deperimeterization, certificate transparency, power-law vulnerability |
| Mobile-and-Phone-Security | Network vs device compromise duality, ecosystem-level security lifting, exploitation cycle |
| Electronic-Warfare | EW priority inversion, electronic warfare triad, hybrid warfare coordination |
| DRM-and-IP-Protection | DRM encryption+license, traitor tracing, watermarking, trusted rendering pipeline |
| Emerging-Technology-Threats | Adversarial ML, hype cycle, complexity boundary, AI/autonomous vehicle threats |
| Surveillance-and-Privacy-Policy | Surveillance capitalism, crypto wars, GDPR localisation, security industrial complex |
| Secure-Development-and-Assurance | SDL, DevSecOps, risk registers, ALE, safety-security convergence |
| Distributed-Architecture-Security | Byzantine failure model, naming scope, publish-register-notify, tiered stand-in processing |

---

## Anti-Patterns

- Deploying crypto without key management: Adding AES/RSA without planning key rotation, revocation, and storage is not security — it creates a false sense of protection. Fix: define the full key lifecycle (generation, distribution, storage, rotation, revocation) before choosing an algorithm.

- Treating compliance as security: Passing a checklist audit does not mean the system is secure. Compliance measures lag real threats. Fix: run threat models against current adversaries, not against the compliance framework's threat model.

- Building security as a perimeter: Treating the network boundary as the trust boundary fails the moment one internal host is compromised. Fix: implement Zero Trust — authenticate and authorize every request, assume breach, segment microscopically.

- Ignoring human factors: Security mechanisms that add friction get bypassed. Password rotation policies produce weak passwords; complex UIs get disabled. Fix: apply usability testing to security controls; measure actual user behavior against assumed behavior.

- Specifying but not enforcing separation of duty: Requiring SoD in policy but implementing it in a single database account negates the control. Fix: enforce SoD at the mechanism layer — different credentials, different processes, different audit trails.

- Over-engineering against low-probability threats: Spending heavily on nation-state-grade protections for systems facing only opportunist attackers misallocates budget. Fix: match control strength to realistic adversary category; use threat model to prioritize.

- Assuming encryption hides timing: Even with strong encryption, variable response times leak information about data content or processing path. Fix: add constant-time operations and noise for timing-sensitive paths; consider statistical side-channel testing.

- Treating assurance as one-time: A security assessment done at release provides no evidence about the system's security six months later after code changes and new threats. Fix: implement continuous assurance — automated SAST/DAST in CI, periodic pen-tests, red-team exercises.

---

## Verification Checklist

- [ ] Threat model names specific adversary categories with realistic capabilities
- [ ] Access control model matches trust requirements (DAC / MAC / RBAC chosen deliberately)
- [ ] Cryptographic design covers full stack: algorithm + mode + protocol + key management
- [ ] Security controls pass abusability analysis — tested for adversarial use, not just normal use
- [ ] Human factors reviewed: cognitive load, affordances, nudges toward secure defaults
- [ ] Economic incentives aligned: who bears cost of failure is who controls security
- [ ] Privacy flows reviewed for contextual integrity; statistical releases use differential privacy
- [ ] Assurance plan defined: SDL integration, test types, cadence, and ownership
- [ ] Side channels considered for cryptographic implementations
- [ ] Audit trails append-only, tamper-evident, and covering relevant actors and actions
