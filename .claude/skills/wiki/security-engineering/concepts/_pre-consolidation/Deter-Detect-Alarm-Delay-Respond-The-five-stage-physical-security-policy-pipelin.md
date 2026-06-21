---
title: Deter-Detect-Alarm-Delay-Respond: The five-stage physical security policy pipeline that drives design and testing of entry controls and alarms, applicable analogously to digital systems
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Locks-and-Alarms.json]
contributing_chapters: ["Locks and Alarms"]
confidence: high
---

# Deter-Detect-Alarm-Delay-Respond: The five-stage physical security policy pipeline that drives design and testing of entry controls and alarms, applicable analogously to digital systems

> From chapter: *Locks and Alarms*

## Core Principle

Chapter 13 establishes that physical and logical security share the same underlying engineering discipline — threat modeling, layered defense, and availability-centric policy — and that alarm systems are the canonical case study for availability as the dominant security property. The ABCD attacker taxonomy and Deter-Detect-Alarm-Delay-Respond framework provide structured tools for calibrating controls to real threat tiers rather than convenient low-skill assumptions. The central lesson is that security failures most often arise from neglecting availability, over-trusting perimeter defenses, misidentifying the attacker tier, and failing to manage integration across specialist subsystems.

## Key Heuristics

These are the load-bearing rules for this concept.

> It's enough to defeat a burglar alarm to make it stop working, or even just to persuade the guards that it has become unreliable.

> Security isn't a scalar. It doesn't make sense to ask 'Is device X secure?' without a context: 'secure against whom and in what environment?'

> The outermost perimeter defenses are the ones that you'd most like to rely on, but also the ones on which the least reliance can be placed.

> Failure to understand the threat model — designing for Charlie and hoping to keep out Bruno — causes many real-life failures.

> You can't just leave the technical aspects of a security engineering project to specialist subcontractors, as critical stuff will always fall down between the cracks.

> About 90% of computer security research was about confidentiality, about 9% about authenticity and 1% about availability. But actual attacks — and companies' infosec expenditures — are often the other way round.

> Only about 20% of threats get through if you test screeners several times per checkpoint per shift, but this rises to 60–75% if you only test once.

> One must look at the overall system — from deterrence through detection, alarm, delay and response.

## Anti-Patterns & Fixes

- Confidentiality-Bias: Over-investing in confidentiality and authentication while neglecting availability, mirroring the historic 90/9/1 research split. Fix: Audit security designs explicitly for availability requirements; model denial-of-service as a primary threat vector, not an afterthought.
- Threshold Miscalibration (Designing for Charlie): Setting security controls to stop low-skill attackers while the real threat is a higher-tier adversary. Fix: Explicitly name the target attacker tier in threat models and verify that controls are tested against that tier.
- Visible-Only Deterrence: Installing conspicuous alarms that simply displace crime to neighbors rather than catching criminals. Fix: Use covert or network-effect deterrents (like Lojack) that increase capture probability and deter crime area-wide.
- Perimeter-Only Trust: Treating the outermost defense as the most reliable layer and neglecting inner defenses. Fix: Design with defense-in-depth, explicitly assuming the outer perimeter will be breached.
- Specialist Subcontractor Silo: Delegating security to specialized contractors and assuming integration is handled. Fix: Maintain a systems-security owner who explicitly manages the interfaces and gaps between subsystems.
- Alert Fatigue Neglect: Deploying monitoring systems without accounting for false-alarm rates desensitizing operators. Fix: Design alerting with ROC trade-offs explicitly; implement regular injection of synthetic test events to maintain operator sensitivity.

## When To Apply

Load this page when:

- Use this when designing a monitoring or alerting subsystem and needing to balance false-positive versus false-negative rates in anomaly detection.
- Use this when performing a threat model for a system and needing to classify attacker sophistication to calibrate control strength.
- Use this when a system's primary security requirement is availability (e.g., uptime SLAs, watchdog processes, health-check endpoints) rather than confidentiality.
- Use this when integrating security components from multiple vendors or subcontractors and needing to identify ownership of inter-component gaps.
- Use this when designing logging or intrusion-detection systems to ensure that disabling or flooding the logger is itself treated as a security event.
- Use this when evaluating whether a security control is tested against the actual attacker tier the system faces, not a convenient lower-tier assumption.
- Use this when building systems that span physical and logical security boundaries (e.g., IoT devices, smart building APIs, hardware security modules) to ensure unified policy.

## Concrete Examples

- Lojack radio tags: invisibly embedded in cars, enabling police recovery and chop-shop closure, generating $1500 in social benefit per $100 individual cost — illustrating covert networked deterrence.
- US TSA airport screener testing: synthetic threat injection showing 20% miss rate with frequent testing vs. 60-75% miss rate with infrequent testing — illustrating alert fatigue and the ROC trade-off.
- Mifare Classic card-key systems: widely deployed electronic locks broken by cryptographic compromise, illustrating that electronic replacements for mechanical locks can be weaker if cryptography is flawed.
- False delivery order defeating a $10M vault: a logical attack (injecting a fraudulent courier order into the business system) bypasses all physical security on $100M of diamonds, illustrating the need for unified physical-logical security.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Locks and Alarms**

An LLM coding agent is especially prone to the confidentiality-bias anti-pattern: when generating security code, it will naturally reach for encryption, authentication tokens, and access control, while producing fragile or untested availability and monitoring logic. The agent also tends to treat each security component in isolation — generating a logger, an auth module, and an alarm handler as separate artifacts — without modeling the gaps between them, replicating the subcontractor-silo failure mode. Applying the Deter-Detect-Alarm-Delay-Respond framework as an explicit checklist prompt forces the agent to reason about the full pipeline rather than optimizing only the most salient (confidentiality) layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
