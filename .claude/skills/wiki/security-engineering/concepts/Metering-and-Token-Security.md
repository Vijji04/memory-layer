---
title: Metering and Token Security
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 5 pages
---

# Metering and Token Security

> Consolidated from 5 related concept pages.

---

## Grey listing vs Black listing Stage token invalidation grey list on issueprint b

## Core Principle

Monitoring and metering systems face a distinctive threat model: the monitored party physically controls the device and is motivated to make it under- or over-report, while the system must often operate offline and at massive scale with cheap hardware. The core engineering discipline is preventing wholesale fraud through key diversification, per-device token binding, and statistical anomaly detection — not eliminating every petty attack. Digital transformations of metering succeed when they enable new business models (utility prepayment) and fail when they merely replicate analogue functions without addressing the stakeholder and threat-model realities (tachographs).

## Key Heuristics

These are the load-bearing rules for this concept.

> Management is that for which there is no algorithm. Where there is an algorithm, it's administration.

> To defeat a burglar alarm it is sufficient to make it appear unreliable. Meters add further subtleties.

> Most people won't cheat unless someone makes it seem easy and safe by industrialising it.

> To maximise revenue, petty fraud should be at least slightly inconvenient and — more importantly — there should be mechanisms to prevent anyone forging tickets at scale.

> Two-digit MACs are enough to detect systematic abuse before it becomes significant.

> The German system tried to stop you printing the stamp more than once, while the British system more realistically tries to stop you using it more than once.

> Many of the monitoring devices are in the hands of opponents.

> Ship it Tuesday and get it right by version 3.

## Anti-Patterns & Fixes

- Universal Master Key in Terminals: Using a single master key stored in every vending terminal means one stolen terminal exposes the whole system. Fix: Use key diversification so each terminal or meter has a unique derived key; store master keys only in central hardware security modules.
- Enforcing Print-Once Instead of Use-Once: Blocking a second print of a token (e.g., German Stampit) punishes legitimate users when printers fail and incentivizes workarounds like photocopying. Fix: Grey-list on print, black-list only when the token is confirmed used at the point of redemption.
- Online-Only Validation: Requiring a live network connection for every token redemption makes the system fragile; outages block legitimate users (can't board bus, use ski lift, etc.). Fix: Design for offline replay/forgery detection using per-device cryptographic tokens with embedded serial numbers.
- Signature Over MAC for High-Throughput Verification: Using public-key signatures on postal indicia seemed elegant but is computationally expensive for sorting machines processing thousands of items per minute. Fix: Use MACs with diversified keys when verification is centralized and offline-batch; reserve signatures only where non-repudiation across untrusted parties is strictly required.
- Ignoring Insider Threat as the Real Attack Surface: Designing postal or metering security primarily against external forgers while the real threat is insiders (e.g., postal employees bribed to inject mail). Fix: Model the actual threat (internal fraud, bribed staff) explicitly and design controls — audit trails, statistical anomaly detection — that address it.
- Copying Payment Network Mechanisms Without Redesign: Adapting payment network protocols directly to metering/IoT without re-examining assumptions leads to vulnerabilities because metering has pervasive mutual mistrust, physically exposed devices, and adversarial custodians. Fix: Treat each new metering application as requiring fresh threat modeling even when borrowing cryptographic primitives.

## When To Apply

Load this page when:

- Use this when designing a prepayment or token-based system where tokens must be validated offline without a live server connection.
- Use this when implementing key management for a large fleet of IoT or embedded devices where physical compromise of individual units is a realistic threat.
- Use this when building a system that must detect fraud at scale (wholesale abuse) rather than eliminate every individual instance of petty abuse.
- Use this when a metering or monitoring device will be physically in the custody of the party being measured (i.e., the adversary controls the hardware).
- Use this when choosing between MACs and digital signatures for high-throughput batch verification where the verifier is a trusted central server.
- Use this when designing token invalidation logic that must be robust to client-side failures (network loss, printer jam, app crash) without penalizing legitimate users.
- Use this when modeling threats for a system that has both external attackers and motivated insider threats (staff, operators) with physical access.
- Use this when evaluating whether an existing security mechanism from one domain (e.g., payment cards) can be reused in a new IoT/metering context.

## Concrete Examples

- STS prepayment electricity meters: 20-digit magic-number tokens tied to individual meters via key diversification, deployed across 68 million meters in 98 countries, originated from South Africa's electrification of townships under Mandela.
- German Stampit postal system: enforced print-once semantics, causing users to photocopy stamps when printers failed — contrasted with UK system that grey-lists on print and only blacklists on confirmed postal use.
- James Watt's sealed revolution counter: early metering system where inspectors periodically read tamper-evident mechanical counters to bill customers for engine royalties — historical precedent for tamper-resistant metering.
- Tachographs in trucks/coaches: digital replacement of analogue speed/hours recorders, cited as a failed digital transformation because entrenched stakeholders prevented disruptive process change, leaving the system doing the same job less well.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Monitoring and Metering**

An LLM coding agent is likely to default to the most academically 'correct' cryptographic primitive (e.g., public-key signatures for non-repudiation, online validation for freshness) without accounting for the physical deployment constraints — low-cost hardware, offline operation, devices in adversary hands — that make simpler mechanisms like MACs with key diversification strictly superior. Agents also tend to model the attacker as an external party and miss the insider-threat pattern (bribed staff, device owners manipulating their own meters), which changes the entire threat model and required controls. The grey-list/black-list distinction is precisely the kind of subtle operational nuance an agent will collapse into a simpler boolean that creates user-penalizing failure modes under normal error conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Key Diversification Derive per device keys by encrypting a device ID under a mas

## Core Principle

Monitoring and metering systems face a distinctive threat model: the monitored party physically controls the device and is motivated to make it under- or over-report, while the system must often operate offline and at massive scale with cheap hardware. The core engineering discipline is preventing wholesale fraud through key diversification, per-device token binding, and statistical anomaly detection — not eliminating every petty attack. Digital transformations of metering succeed when they enable new business models (utility prepayment) and fail when they merely replicate analogue functions without addressing the stakeholder and threat-model realities (tachographs).

## Key Heuristics

These are the load-bearing rules for this concept.

> Management is that for which there is no algorithm. Where there is an algorithm, it's administration.

> To defeat a burglar alarm it is sufficient to make it appear unreliable. Meters add further subtleties.

> Most people won't cheat unless someone makes it seem easy and safe by industrialising it.

> To maximise revenue, petty fraud should be at least slightly inconvenient and — more importantly — there should be mechanisms to prevent anyone forging tickets at scale.

> Two-digit MACs are enough to detect systematic abuse before it becomes significant.

> The German system tried to stop you printing the stamp more than once, while the British system more realistically tries to stop you using it more than once.

> Many of the monitoring devices are in the hands of opponents.

> Ship it Tuesday and get it right by version 3.

## Anti-Patterns & Fixes

- Universal Master Key in Terminals: Using a single master key stored in every vending terminal means one stolen terminal exposes the whole system. Fix: Use key diversification so each terminal or meter has a unique derived key; store master keys only in central hardware security modules.
- Enforcing Print-Once Instead of Use-Once: Blocking a second print of a token (e.g., German Stampit) punishes legitimate users when printers fail and incentivizes workarounds like photocopying. Fix: Grey-list on print, black-list only when the token is confirmed used at the point of redemption.
- Online-Only Validation: Requiring a live network connection for every token redemption makes the system fragile; outages block legitimate users (can't board bus, use ski lift, etc.). Fix: Design for offline replay/forgery detection using per-device cryptographic tokens with embedded serial numbers.
- Signature Over MAC for High-Throughput Verification: Using public-key signatures on postal indicia seemed elegant but is computationally expensive for sorting machines processing thousands of items per minute. Fix: Use MACs with diversified keys when verification is centralized and offline-batch; reserve signatures only where non-repudiation across untrusted parties is strictly required.
- Ignoring Insider Threat as the Real Attack Surface: Designing postal or metering security primarily against external forgers while the real threat is insiders (e.g., postal employees bribed to inject mail). Fix: Model the actual threat (internal fraud, bribed staff) explicitly and design controls — audit trails, statistical anomaly detection — that address it.
- Copying Payment Network Mechanisms Without Redesign: Adapting payment network protocols directly to metering/IoT without re-examining assumptions leads to vulnerabilities because metering has pervasive mutual mistrust, physically exposed devices, and adversarial custodians. Fix: Treat each new metering application as requiring fresh threat modeling even when borrowing cryptographic primitives.

## When To Apply

Load this page when:

- Use this when designing a prepayment or token-based system where tokens must be validated offline without a live server connection.
- Use this when implementing key management for a large fleet of IoT or embedded devices where physical compromise of individual units is a realistic threat.
- Use this when building a system that must detect fraud at scale (wholesale abuse) rather than eliminate every individual instance of petty abuse.
- Use this when a metering or monitoring device will be physically in the custody of the party being measured (i.e., the adversary controls the hardware).
- Use this when choosing between MACs and digital signatures for high-throughput batch verification where the verifier is a trusted central server.
- Use this when designing token invalidation logic that must be robust to client-side failures (network loss, printer jam, app crash) without penalizing legitimate users.
- Use this when modeling threats for a system that has both external attackers and motivated insider threats (staff, operators) with physical access.
- Use this when evaluating whether an existing security mechanism from one domain (e.g., payment cards) can be reused in a new IoT/metering context.

## Concrete Examples

- STS prepayment electricity meters: 20-digit magic-number tokens tied to individual meters via key diversification, deployed across 68 million meters in 98 countries, originated from South Africa's electrification of townships under Mandela.
- German Stampit postal system: enforced print-once semantics, causing users to photocopy stamps when printers failed — contrasted with UK system that grey-lists on print and only blacklists on confirmed postal use.
- James Watt's sealed revolution counter: early metering system where inspectors periodically read tamper-evident mechanical counters to bill customers for engine royalties — historical precedent for tamper-resistant metering.
- Tachographs in trucks/coaches: digital replacement of analogue speed/hours recorders, cited as a failed digital transformation because entrenched stakeholders prevented disruptive process change, leaving the system doing the same job less well.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Monitoring and Metering**

An LLM coding agent is likely to default to the most academically 'correct' cryptographic primitive (e.g., public-key signatures for non-repudiation, online validation for freshness) without accounting for the physical deployment constraints — low-cost hardware, offline operation, devices in adversary hands — that make simpler mechanisms like MACs with key diversification strictly superior. Agents also tend to model the attacker as an external party and miss the insider-threat pattern (bribed staff, device owners manipulating their own meters), which changes the entire threat model and required controls. The grey-list/black-list distinction is precisely the kind of subtle operational nuance an agent will collapse into a simpler boolean that creates user-penalizing failure modes under normal error conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Offline First Fraud Tolerance Accept that small scale fraud is inevitable offlin

## Core Principle

Monitoring and metering systems face a distinctive threat model: the monitored party physically controls the device and is motivated to make it under- or over-report, while the system must often operate offline and at massive scale with cheap hardware. The core engineering discipline is preventing wholesale fraud through key diversification, per-device token binding, and statistical anomaly detection — not eliminating every petty attack. Digital transformations of metering succeed when they enable new business models (utility prepayment) and fail when they merely replicate analogue functions without addressing the stakeholder and threat-model realities (tachographs).

## Key Heuristics

These are the load-bearing rules for this concept.

> Management is that for which there is no algorithm. Where there is an algorithm, it's administration.

> To defeat a burglar alarm it is sufficient to make it appear unreliable. Meters add further subtleties.

> Most people won't cheat unless someone makes it seem easy and safe by industrialising it.

> To maximise revenue, petty fraud should be at least slightly inconvenient and — more importantly — there should be mechanisms to prevent anyone forging tickets at scale.

> Two-digit MACs are enough to detect systematic abuse before it becomes significant.

> The German system tried to stop you printing the stamp more than once, while the British system more realistically tries to stop you using it more than once.

> Many of the monitoring devices are in the hands of opponents.

> Ship it Tuesday and get it right by version 3.

## Anti-Patterns & Fixes

- Universal Master Key in Terminals: Using a single master key stored in every vending terminal means one stolen terminal exposes the whole system. Fix: Use key diversification so each terminal or meter has a unique derived key; store master keys only in central hardware security modules.
- Enforcing Print-Once Instead of Use-Once: Blocking a second print of a token (e.g., German Stampit) punishes legitimate users when printers fail and incentivizes workarounds like photocopying. Fix: Grey-list on print, black-list only when the token is confirmed used at the point of redemption.
- Online-Only Validation: Requiring a live network connection for every token redemption makes the system fragile; outages block legitimate users (can't board bus, use ski lift, etc.). Fix: Design for offline replay/forgery detection using per-device cryptographic tokens with embedded serial numbers.
- Signature Over MAC for High-Throughput Verification: Using public-key signatures on postal indicia seemed elegant but is computationally expensive for sorting machines processing thousands of items per minute. Fix: Use MACs with diversified keys when verification is centralized and offline-batch; reserve signatures only where non-repudiation across untrusted parties is strictly required.
- Ignoring Insider Threat as the Real Attack Surface: Designing postal or metering security primarily against external forgers while the real threat is insiders (e.g., postal employees bribed to inject mail). Fix: Model the actual threat (internal fraud, bribed staff) explicitly and design controls — audit trails, statistical anomaly detection — that address it.
- Copying Payment Network Mechanisms Without Redesign: Adapting payment network protocols directly to metering/IoT without re-examining assumptions leads to vulnerabilities because metering has pervasive mutual mistrust, physically exposed devices, and adversarial custodians. Fix: Treat each new metering application as requiring fresh threat modeling even when borrowing cryptographic primitives.

## When To Apply

Load this page when:

- Use this when designing a prepayment or token-based system where tokens must be validated offline without a live server connection.
- Use this when implementing key management for a large fleet of IoT or embedded devices where physical compromise of individual units is a realistic threat.
- Use this when building a system that must detect fraud at scale (wholesale abuse) rather than eliminate every individual instance of petty abuse.
- Use this when a metering or monitoring device will be physically in the custody of the party being measured (i.e., the adversary controls the hardware).
- Use this when choosing between MACs and digital signatures for high-throughput batch verification where the verifier is a trusted central server.
- Use this when designing token invalidation logic that must be robust to client-side failures (network loss, printer jam, app crash) without penalizing legitimate users.
- Use this when modeling threats for a system that has both external attackers and motivated insider threats (staff, operators) with physical access.
- Use this when evaluating whether an existing security mechanism from one domain (e.g., payment cards) can be reused in a new IoT/metering context.

## Concrete Examples

- STS prepayment electricity meters: 20-digit magic-number tokens tied to individual meters via key diversification, deployed across 68 million meters in 98 countries, originated from South Africa's electrification of townships under Mandela.
- German Stampit postal system: enforced print-once semantics, causing users to photocopy stamps when printers failed — contrasted with UK system that grey-lists on print and only blacklists on confirmed postal use.
- James Watt's sealed revolution counter: early metering system where inspectors periodically read tamper-evident mechanical counters to bill customers for engine royalties — historical precedent for tamper-resistant metering.
- Tachographs in trucks/coaches: digital replacement of analogue speed/hours recorders, cited as a failed digital transformation because entrenched stakeholders prevented disruptive process change, leaving the system doing the same job less well.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Monitoring and Metering**

An LLM coding agent is likely to default to the most academically 'correct' cryptographic primitive (e.g., public-key signatures for non-repudiation, online validation for freshness) without accounting for the physical deployment constraints — low-cost hardware, offline operation, devices in adversary hands — that make simpler mechanisms like MACs with key diversification strictly superior. Agents also tend to model the attacker as an external party and miss the insider-threat pattern (bribed staff, device owners manipulating their own meters), which changes the entire threat model and required controls. The grey-list/black-list distinction is precisely the kind of subtle operational nuance an agent will collapse into a simpler boolean that creates user-penalizing failure modes under normal error conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Statistical Balancing for Loss Detection Compare feeder meter readings against s

## Core Principle

Monitoring and metering systems face a distinctive threat model: the monitored party physically controls the device and is motivated to make it under- or over-report, while the system must often operate offline and at massive scale with cheap hardware. The core engineering discipline is preventing wholesale fraud through key diversification, per-device token binding, and statistical anomaly detection — not eliminating every petty attack. Digital transformations of metering succeed when they enable new business models (utility prepayment) and fail when they merely replicate analogue functions without addressing the stakeholder and threat-model realities (tachographs).

## Key Heuristics

These are the load-bearing rules for this concept.

> Management is that for which there is no algorithm. Where there is an algorithm, it's administration.

> To defeat a burglar alarm it is sufficient to make it appear unreliable. Meters add further subtleties.

> Most people won't cheat unless someone makes it seem easy and safe by industrialising it.

> To maximise revenue, petty fraud should be at least slightly inconvenient and — more importantly — there should be mechanisms to prevent anyone forging tickets at scale.

> Two-digit MACs are enough to detect systematic abuse before it becomes significant.

> The German system tried to stop you printing the stamp more than once, while the British system more realistically tries to stop you using it more than once.

> Many of the monitoring devices are in the hands of opponents.

> Ship it Tuesday and get it right by version 3.

## Anti-Patterns & Fixes

- Universal Master Key in Terminals: Using a single master key stored in every vending terminal means one stolen terminal exposes the whole system. Fix: Use key diversification so each terminal or meter has a unique derived key; store master keys only in central hardware security modules.
- Enforcing Print-Once Instead of Use-Once: Blocking a second print of a token (e.g., German Stampit) punishes legitimate users when printers fail and incentivizes workarounds like photocopying. Fix: Grey-list on print, black-list only when the token is confirmed used at the point of redemption.
- Online-Only Validation: Requiring a live network connection for every token redemption makes the system fragile; outages block legitimate users (can't board bus, use ski lift, etc.). Fix: Design for offline replay/forgery detection using per-device cryptographic tokens with embedded serial numbers.
- Signature Over MAC for High-Throughput Verification: Using public-key signatures on postal indicia seemed elegant but is computationally expensive for sorting machines processing thousands of items per minute. Fix: Use MACs with diversified keys when verification is centralized and offline-batch; reserve signatures only where non-repudiation across untrusted parties is strictly required.
- Ignoring Insider Threat as the Real Attack Surface: Designing postal or metering security primarily against external forgers while the real threat is insiders (e.g., postal employees bribed to inject mail). Fix: Model the actual threat (internal fraud, bribed staff) explicitly and design controls — audit trails, statistical anomaly detection — that address it.
- Copying Payment Network Mechanisms Without Redesign: Adapting payment network protocols directly to metering/IoT without re-examining assumptions leads to vulnerabilities because metering has pervasive mutual mistrust, physically exposed devices, and adversarial custodians. Fix: Treat each new metering application as requiring fresh threat modeling even when borrowing cryptographic primitives.

## When To Apply

Load this page when:

- Use this when designing a prepayment or token-based system where tokens must be validated offline without a live server connection.
- Use this when implementing key management for a large fleet of IoT or embedded devices where physical compromise of individual units is a realistic threat.
- Use this when building a system that must detect fraud at scale (wholesale abuse) rather than eliminate every individual instance of petty abuse.
- Use this when a metering or monitoring device will be physically in the custody of the party being measured (i.e., the adversary controls the hardware).
- Use this when choosing between MACs and digital signatures for high-throughput batch verification where the verifier is a trusted central server.
- Use this when designing token invalidation logic that must be robust to client-side failures (network loss, printer jam, app crash) without penalizing legitimate users.
- Use this when modeling threats for a system that has both external attackers and motivated insider threats (staff, operators) with physical access.
- Use this when evaluating whether an existing security mechanism from one domain (e.g., payment cards) can be reused in a new IoT/metering context.

## Concrete Examples

- STS prepayment electricity meters: 20-digit magic-number tokens tied to individual meters via key diversification, deployed across 68 million meters in 98 countries, originated from South Africa's electrification of townships under Mandela.
- German Stampit postal system: enforced print-once semantics, causing users to photocopy stamps when printers failed — contrasted with UK system that grey-lists on print and only blacklists on confirmed postal use.
- James Watt's sealed revolution counter: early metering system where inspectors periodically read tamper-evident mechanical counters to bill customers for engine royalties — historical precedent for tamper-resistant metering.
- Tachographs in trucks/coaches: digital replacement of analogue speed/hours recorders, cited as a failed digital transformation because entrenched stakeholders prevented disruptive process change, leaving the system doing the same job less well.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Monitoring and Metering**

An LLM coding agent is likely to default to the most academically 'correct' cryptographic primitive (e.g., public-key signatures for non-repudiation, online validation for freshness) without accounting for the physical deployment constraints — low-cost hardware, offline operation, devices in adversary hands — that make simpler mechanisms like MACs with key diversification strictly superior. Agents also tend to model the attacker as an external party and miss the insider-threat pattern (bribed staff, device owners manipulating their own meters), which changes the entire threat model and required controls. The grey-list/black-list distinction is precisely the kind of subtle operational nuance an agent will collapse into a simpler boolean that creates user-penalizing failure modes under normal error conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Token Binding Tie each prepayment token to a unique meter ID and include a seria

## Core Principle

Monitoring and metering systems face a distinctive threat model: the monitored party physically controls the device and is motivated to make it under- or over-report, while the system must often operate offline and at massive scale with cheap hardware. The core engineering discipline is preventing wholesale fraud through key diversification, per-device token binding, and statistical anomaly detection — not eliminating every petty attack. Digital transformations of metering succeed when they enable new business models (utility prepayment) and fail when they merely replicate analogue functions without addressing the stakeholder and threat-model realities (tachographs).

## Key Heuristics

These are the load-bearing rules for this concept.

> Management is that for which there is no algorithm. Where there is an algorithm, it's administration.

> To defeat a burglar alarm it is sufficient to make it appear unreliable. Meters add further subtleties.

> Most people won't cheat unless someone makes it seem easy and safe by industrialising it.

> To maximise revenue, petty fraud should be at least slightly inconvenient and — more importantly — there should be mechanisms to prevent anyone forging tickets at scale.

> Two-digit MACs are enough to detect systematic abuse before it becomes significant.

> The German system tried to stop you printing the stamp more than once, while the British system more realistically tries to stop you using it more than once.

> Many of the monitoring devices are in the hands of opponents.

> Ship it Tuesday and get it right by version 3.

## Anti-Patterns & Fixes

- Universal Master Key in Terminals: Using a single master key stored in every vending terminal means one stolen terminal exposes the whole system. Fix: Use key diversification so each terminal or meter has a unique derived key; store master keys only in central hardware security modules.
- Enforcing Print-Once Instead of Use-Once: Blocking a second print of a token (e.g., German Stampit) punishes legitimate users when printers fail and incentivizes workarounds like photocopying. Fix: Grey-list on print, black-list only when the token is confirmed used at the point of redemption.
- Online-Only Validation: Requiring a live network connection for every token redemption makes the system fragile; outages block legitimate users (can't board bus, use ski lift, etc.). Fix: Design for offline replay/forgery detection using per-device cryptographic tokens with embedded serial numbers.
- Signature Over MAC for High-Throughput Verification: Using public-key signatures on postal indicia seemed elegant but is computationally expensive for sorting machines processing thousands of items per minute. Fix: Use MACs with diversified keys when verification is centralized and offline-batch; reserve signatures only where non-repudiation across untrusted parties is strictly required.
- Ignoring Insider Threat as the Real Attack Surface: Designing postal or metering security primarily against external forgers while the real threat is insiders (e.g., postal employees bribed to inject mail). Fix: Model the actual threat (internal fraud, bribed staff) explicitly and design controls — audit trails, statistical anomaly detection — that address it.
- Copying Payment Network Mechanisms Without Redesign: Adapting payment network protocols directly to metering/IoT without re-examining assumptions leads to vulnerabilities because metering has pervasive mutual mistrust, physically exposed devices, and adversarial custodians. Fix: Treat each new metering application as requiring fresh threat modeling even when borrowing cryptographic primitives.

## When To Apply

Load this page when:

- Use this when designing a prepayment or token-based system where tokens must be validated offline without a live server connection.
- Use this when implementing key management for a large fleet of IoT or embedded devices where physical compromise of individual units is a realistic threat.
- Use this when building a system that must detect fraud at scale (wholesale abuse) rather than eliminate every individual instance of petty abuse.
- Use this when a metering or monitoring device will be physically in the custody of the party being measured (i.e., the adversary controls the hardware).
- Use this when choosing between MACs and digital signatures for high-throughput batch verification where the verifier is a trusted central server.
- Use this when designing token invalidation logic that must be robust to client-side failures (network loss, printer jam, app crash) without penalizing legitimate users.
- Use this when modeling threats for a system that has both external attackers and motivated insider threats (staff, operators) with physical access.
- Use this when evaluating whether an existing security mechanism from one domain (e.g., payment cards) can be reused in a new IoT/metering context.

## Concrete Examples

- STS prepayment electricity meters: 20-digit magic-number tokens tied to individual meters via key diversification, deployed across 68 million meters in 98 countries, originated from South Africa's electrification of townships under Mandela.
- German Stampit postal system: enforced print-once semantics, causing users to photocopy stamps when printers failed — contrasted with UK system that grey-lists on print and only blacklists on confirmed postal use.
- James Watt's sealed revolution counter: early metering system where inspectors periodically read tamper-evident mechanical counters to bill customers for engine royalties — historical precedent for tamper-resistant metering.
- Tachographs in trucks/coaches: digital replacement of analogue speed/hours recorders, cited as a failed digital transformation because entrenched stakeholders prevented disruptive process change, leaving the system doing the same job less well.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Monitoring and Metering**

An LLM coding agent is likely to default to the most academically 'correct' cryptographic primitive (e.g., public-key signatures for non-repudiation, online validation for freshness) without accounting for the physical deployment constraints — low-cost hardware, offline operation, devices in adversary hands — that make simpler mechanisms like MACs with key diversification strictly superior. Agents also tend to model the attacker as an external party and miss the insider-threat pattern (bribed staff, device owners manipulating their own meters), which changes the entire threat model and required controls. The grey-list/black-list distinction is precisely the kind of subtle operational nuance an agent will collapse into a simpler boolean that creates user-penalizing failure modes under normal error conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
