---
title: Threat Modeling
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 6 pages
---

# Threat Modeling

> Consolidated from 6 related concept pages.

---

## ABCD Threat Taxonomy DerekCharlieBrunoAbdurrahman A four tier attacker classific

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

---

## Abusability Analysis Extends usability thinking to adversarial use for any syste

## Core Principle

Security engineering requires identifying specific, realistic adversaries before designing defenses, since no system can resist all threats while remaining useful and affordable. The chapter provides a four-category taxonomy — spies, crooks, hackers, and bullies — and argues that adversary capabilities and tools migrate across categories over time, so even narrow-scope systems must understand the broader threat landscape. The central design obligation is to analyze not just usability but abusability: how any feature could be weaponized at scale by each adversary class.

## Key Heuristics

These are the load-bearing rules for this concept.

> Ideologues may deal with the world as they would wish it to be, but engineers deal with the world as it is.

> It's not enough to think about usability; you need to think about abusability too.

> You can't protect it against all possible threats and still expect it to do useful work at a reasonable cost.

> Even if spies aren't in your threat model today, the tools they use will quite often end up in the hands of the crooks too, sooner or later.

> Crime will evolve where it can scale.

> It's not enough to rely on patching and antivirus. You need to watch your network and keep good enough logs that when an infected machine is spotted you can tell whether it's a kid building a botnet or a targeted attacker.

> You need to make plans to respond to incidents, so you know who to call for forensics – and so your CEO isn't left gasping like a landed fish in front of the TV cameras.

## Anti-Patterns & Fixes

- Universal Threat Modeling: Attempting to defend against every possible adversary simultaneously. Goes wrong because it makes the system unusable and unaffordably expensive. Fix: Identify the most likely opponents for your specific system and scope defenses accordingly.
- Patch-and-AV Complacency: Relying solely on patching and antivirus as the security posture. Goes wrong because it provides no visibility into whether a compromise is opportunistic or targeted. Fix: Implement network monitoring and logging sufficient to distinguish botnet zombies from targeted attackers.
- Ignoring Insider Threats: Focusing only on external attackers. Goes wrong because a typical firm also faces dishonest insiders, and the same credentials/access that enable legitimate work enable insider fraud. Fix: Include insider threat scenarios explicitly in the threat model.
- Feature-Only Design: Designing systems purely for legitimate use cases without adversarial analysis. Goes wrong because any feature that enables scale for users also enables scale for attackers. Fix: For each capability, explicitly model how a bad actor would weaponize it at scale.
- Static Threat Assessment: Treating the threat model as fixed at design time. Goes wrong because adversary capabilities and tools migrate (e.g., spy tools become criminal tools) over a system's lifetime. Fix: Revisit threat models periodically and ask how the adversary landscape has shifted.
- Narrow Security Research Perspective: Security community dominated by a demographic that ignores personal/interpersonal threats like stalking and harassment. Goes wrong because these threats affect the majority of users. Fix: Include abuse scenarios affecting marginalized and non-technical users in security design.

## When To Apply

Load this page when:

- Use this when starting security design for a new system and needing to decide which threat classes to defend against and how much to invest in each.
- Use this when evaluating whether a proposed feature could be weaponized — apply abusability analysis before shipping.
- Use this when a system handles user-generated content or communications at scale, to assess whether the angry-mob / coordinated harassment attack surface has been modeled.
- Use this when building authentication or access control and needing to classify whether the threat is mass opportunistic attack, spear-phishing, or insider abuse.
- Use this when advising on logging and monitoring requirements — sufficient to distinguish opportunistic botnet infection from targeted persistent attack.
- Use this when a system involves financial transactions, credentials, or PII, to apply the criminal specialization model and understand which underground market roles could exploit it.
- Use this when a feature relies on trust in infrastructure providers (e.g., cloud APIs, email) and needing to assess whether state-level PRISM-style interception is a relevant threat.
- Use this when doing incident response planning — ensures the plan addresses forensics, communications, and identification of attacker sophistication level before an incident occurs.

## Concrete Examples

- NSA PRISM program: built as warranted law-enforcement wiretap infrastructure but used for mass foreign intelligence collection, unknown even to Google's own mail and security teams until Snowden revealed it in June 2013.
- GCHQ Tempora: tapped 200 transatlantic fibre optic cables in Cornwall alone, collecting up to 21 petabytes/day, retaining filtered content for 30 days — leveraging Britain's legacy 19th-century telegraph cable infrastructure.
- 1988 Internet Worm: a student experiment that escaped the lab, illustrating that early threats were accidental rather than criminal, and that the threat landscape was not always adversarial.
- Mid-2000s underground markets: enabled criminal division of labor — one gang writes malware, another harvests credentials, another cashes out — allowing cybercrime to scale like industrial manufacturing.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Who Is the Opponent?**

An LLM coding agent is particularly prone to the 'universal threat modeling' anti-pattern in reverse: it may generate code with no threat model at all, defaulting to happy-path assumptions because training data skews toward functional examples rather than adversarial ones. The agent also cannot intrinsically know which of the four adversary categories is relevant to the deployment context, so without explicit prompting it will omit authentication, rate limiting, or audit logging that would only make sense if a specific threat class were assumed. Most critically, an LLM agent has no concept of a system's lifetime — it will not flag that a design decision safe today may become exploitable when spy-grade tools migrate to criminal ecosystems, making explicit threat-model documentation in prompts essential.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Criminal Specialization Underground Market Model Describes how cybercrime indust

## Core Principle

Security engineering requires identifying specific, realistic adversaries before designing defenses, since no system can resist all threats while remaining useful and affordable. The chapter provides a four-category taxonomy — spies, crooks, hackers, and bullies — and argues that adversary capabilities and tools migrate across categories over time, so even narrow-scope systems must understand the broader threat landscape. The central design obligation is to analyze not just usability but abusability: how any feature could be weaponized at scale by each adversary class.

## Key Heuristics

These are the load-bearing rules for this concept.

> Ideologues may deal with the world as they would wish it to be, but engineers deal with the world as it is.

> It's not enough to think about usability; you need to think about abusability too.

> You can't protect it against all possible threats and still expect it to do useful work at a reasonable cost.

> Even if spies aren't in your threat model today, the tools they use will quite often end up in the hands of the crooks too, sooner or later.

> Crime will evolve where it can scale.

> It's not enough to rely on patching and antivirus. You need to watch your network and keep good enough logs that when an infected machine is spotted you can tell whether it's a kid building a botnet or a targeted attacker.

> You need to make plans to respond to incidents, so you know who to call for forensics – and so your CEO isn't left gasping like a landed fish in front of the TV cameras.

## Anti-Patterns & Fixes

- Universal Threat Modeling: Attempting to defend against every possible adversary simultaneously. Goes wrong because it makes the system unusable and unaffordably expensive. Fix: Identify the most likely opponents for your specific system and scope defenses accordingly.
- Patch-and-AV Complacency: Relying solely on patching and antivirus as the security posture. Goes wrong because it provides no visibility into whether a compromise is opportunistic or targeted. Fix: Implement network monitoring and logging sufficient to distinguish botnet zombies from targeted attackers.
- Ignoring Insider Threats: Focusing only on external attackers. Goes wrong because a typical firm also faces dishonest insiders, and the same credentials/access that enable legitimate work enable insider fraud. Fix: Include insider threat scenarios explicitly in the threat model.
- Feature-Only Design: Designing systems purely for legitimate use cases without adversarial analysis. Goes wrong because any feature that enables scale for users also enables scale for attackers. Fix: For each capability, explicitly model how a bad actor would weaponize it at scale.
- Static Threat Assessment: Treating the threat model as fixed at design time. Goes wrong because adversary capabilities and tools migrate (e.g., spy tools become criminal tools) over a system's lifetime. Fix: Revisit threat models periodically and ask how the adversary landscape has shifted.
- Narrow Security Research Perspective: Security community dominated by a demographic that ignores personal/interpersonal threats like stalking and harassment. Goes wrong because these threats affect the majority of users. Fix: Include abuse scenarios affecting marginalized and non-technical users in security design.

## When To Apply

Load this page when:

- Use this when starting security design for a new system and needing to decide which threat classes to defend against and how much to invest in each.
- Use this when evaluating whether a proposed feature could be weaponized — apply abusability analysis before shipping.
- Use this when a system handles user-generated content or communications at scale, to assess whether the angry-mob / coordinated harassment attack surface has been modeled.
- Use this when building authentication or access control and needing to classify whether the threat is mass opportunistic attack, spear-phishing, or insider abuse.
- Use this when advising on logging and monitoring requirements — sufficient to distinguish opportunistic botnet infection from targeted persistent attack.
- Use this when a system involves financial transactions, credentials, or PII, to apply the criminal specialization model and understand which underground market roles could exploit it.
- Use this when a feature relies on trust in infrastructure providers (e.g., cloud APIs, email) and needing to assess whether state-level PRISM-style interception is a relevant threat.
- Use this when doing incident response planning — ensures the plan addresses forensics, communications, and identification of attacker sophistication level before an incident occurs.

## Concrete Examples

- NSA PRISM program: built as warranted law-enforcement wiretap infrastructure but used for mass foreign intelligence collection, unknown even to Google's own mail and security teams until Snowden revealed it in June 2013.
- GCHQ Tempora: tapped 200 transatlantic fibre optic cables in Cornwall alone, collecting up to 21 petabytes/day, retaining filtered content for 30 days — leveraging Britain's legacy 19th-century telegraph cable infrastructure.
- 1988 Internet Worm: a student experiment that escaped the lab, illustrating that early threats were accidental rather than criminal, and that the threat landscape was not always adversarial.
- Mid-2000s underground markets: enabled criminal division of labor — one gang writes malware, another harvests credentials, another cashes out — allowing cybercrime to scale like industrial manufacturing.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Who Is the Opponent?**

An LLM coding agent is particularly prone to the 'universal threat modeling' anti-pattern in reverse: it may generate code with no threat model at all, defaulting to happy-path assumptions because training data skews toward functional examples rather than adversarial ones. The agent also cannot intrinsically know which of the four adversary categories is relevant to the deployment context, so without explicit prompting it will omit authentication, rate limiting, or audit logging that would only make sense if a specific threat class were assumed. Most critically, an LLM agent has no concept of a system's lifetime — it will not flag that a design decision safe today may become exploitable when spy-grade tools migrate to criminal ecosystems, making explicit threat-model documentation in prompts essential.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Four Category Adversary Taxonomy Classifies all threat actors into Spies state i

## Core Principle

Security engineering requires identifying specific, realistic adversaries before designing defenses, since no system can resist all threats while remaining useful and affordable. The chapter provides a four-category taxonomy — spies, crooks, hackers, and bullies — and argues that adversary capabilities and tools migrate across categories over time, so even narrow-scope systems must understand the broader threat landscape. The central design obligation is to analyze not just usability but abusability: how any feature could be weaponized at scale by each adversary class.

## Key Heuristics

These are the load-bearing rules for this concept.

> Ideologues may deal with the world as they would wish it to be, but engineers deal with the world as it is.

> It's not enough to think about usability; you need to think about abusability too.

> You can't protect it against all possible threats and still expect it to do useful work at a reasonable cost.

> Even if spies aren't in your threat model today, the tools they use will quite often end up in the hands of the crooks too, sooner or later.

> Crime will evolve where it can scale.

> It's not enough to rely on patching and antivirus. You need to watch your network and keep good enough logs that when an infected machine is spotted you can tell whether it's a kid building a botnet or a targeted attacker.

> You need to make plans to respond to incidents, so you know who to call for forensics – and so your CEO isn't left gasping like a landed fish in front of the TV cameras.

## Anti-Patterns & Fixes

- Universal Threat Modeling: Attempting to defend against every possible adversary simultaneously. Goes wrong because it makes the system unusable and unaffordably expensive. Fix: Identify the most likely opponents for your specific system and scope defenses accordingly.
- Patch-and-AV Complacency: Relying solely on patching and antivirus as the security posture. Goes wrong because it provides no visibility into whether a compromise is opportunistic or targeted. Fix: Implement network monitoring and logging sufficient to distinguish botnet zombies from targeted attackers.
- Ignoring Insider Threats: Focusing only on external attackers. Goes wrong because a typical firm also faces dishonest insiders, and the same credentials/access that enable legitimate work enable insider fraud. Fix: Include insider threat scenarios explicitly in the threat model.
- Feature-Only Design: Designing systems purely for legitimate use cases without adversarial analysis. Goes wrong because any feature that enables scale for users also enables scale for attackers. Fix: For each capability, explicitly model how a bad actor would weaponize it at scale.
- Static Threat Assessment: Treating the threat model as fixed at design time. Goes wrong because adversary capabilities and tools migrate (e.g., spy tools become criminal tools) over a system's lifetime. Fix: Revisit threat models periodically and ask how the adversary landscape has shifted.
- Narrow Security Research Perspective: Security community dominated by a demographic that ignores personal/interpersonal threats like stalking and harassment. Goes wrong because these threats affect the majority of users. Fix: Include abuse scenarios affecting marginalized and non-technical users in security design.

## When To Apply

Load this page when:

- Use this when starting security design for a new system and needing to decide which threat classes to defend against and how much to invest in each.
- Use this when evaluating whether a proposed feature could be weaponized — apply abusability analysis before shipping.
- Use this when a system handles user-generated content or communications at scale, to assess whether the angry-mob / coordinated harassment attack surface has been modeled.
- Use this when building authentication or access control and needing to classify whether the threat is mass opportunistic attack, spear-phishing, or insider abuse.
- Use this when advising on logging and monitoring requirements — sufficient to distinguish opportunistic botnet infection from targeted persistent attack.
- Use this when a system involves financial transactions, credentials, or PII, to apply the criminal specialization model and understand which underground market roles could exploit it.
- Use this when a feature relies on trust in infrastructure providers (e.g., cloud APIs, email) and needing to assess whether state-level PRISM-style interception is a relevant threat.
- Use this when doing incident response planning — ensures the plan addresses forensics, communications, and identification of attacker sophistication level before an incident occurs.

## Concrete Examples

- NSA PRISM program: built as warranted law-enforcement wiretap infrastructure but used for mass foreign intelligence collection, unknown even to Google's own mail and security teams until Snowden revealed it in June 2013.
- GCHQ Tempora: tapped 200 transatlantic fibre optic cables in Cornwall alone, collecting up to 21 petabytes/day, retaining filtered content for 30 days — leveraging Britain's legacy 19th-century telegraph cable infrastructure.
- 1988 Internet Worm: a student experiment that escaped the lab, illustrating that early threats were accidental rather than criminal, and that the threat landscape was not always adversarial.
- Mid-2000s underground markets: enabled criminal division of labor — one gang writes malware, another harvests credentials, another cashes out — allowing cybercrime to scale like industrial manufacturing.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Who Is the Opponent?**

An LLM coding agent is particularly prone to the 'universal threat modeling' anti-pattern in reverse: it may generate code with no threat model at all, defaulting to happy-path assumptions because training data skews toward functional examples rather than adversarial ones. The agent also cannot intrinsically know which of the four adversary categories is relevant to the deployment context, so without explicit prompting it will omit authentication, rate limiting, or audit logging that would only make sense if a specific threat class were assumed. Most critically, an LLM agent has no concept of a system's lifetime — it will not flag that a design decision safe today may become exploitable when spy-grade tools migrate to criminal ecosystems, making explicit threat-model documentation in prompts essential.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Threat Model Evaluation Two question framework 1 Is the threat model realistic 2

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

## Threat Model Scoping The practice of identifying specific likely opponents for a

## Core Principle

Security engineering requires identifying specific, realistic adversaries before designing defenses, since no system can resist all threats while remaining useful and affordable. The chapter provides a four-category taxonomy — spies, crooks, hackers, and bullies — and argues that adversary capabilities and tools migrate across categories over time, so even narrow-scope systems must understand the broader threat landscape. The central design obligation is to analyze not just usability but abusability: how any feature could be weaponized at scale by each adversary class.

## Key Heuristics

These are the load-bearing rules for this concept.

> Ideologues may deal with the world as they would wish it to be, but engineers deal with the world as it is.

> It's not enough to think about usability; you need to think about abusability too.

> You can't protect it against all possible threats and still expect it to do useful work at a reasonable cost.

> Even if spies aren't in your threat model today, the tools they use will quite often end up in the hands of the crooks too, sooner or later.

> Crime will evolve where it can scale.

> It's not enough to rely on patching and antivirus. You need to watch your network and keep good enough logs that when an infected machine is spotted you can tell whether it's a kid building a botnet or a targeted attacker.

> You need to make plans to respond to incidents, so you know who to call for forensics – and so your CEO isn't left gasping like a landed fish in front of the TV cameras.

## Anti-Patterns & Fixes

- Universal Threat Modeling: Attempting to defend against every possible adversary simultaneously. Goes wrong because it makes the system unusable and unaffordably expensive. Fix: Identify the most likely opponents for your specific system and scope defenses accordingly.
- Patch-and-AV Complacency: Relying solely on patching and antivirus as the security posture. Goes wrong because it provides no visibility into whether a compromise is opportunistic or targeted. Fix: Implement network monitoring and logging sufficient to distinguish botnet zombies from targeted attackers.
- Ignoring Insider Threats: Focusing only on external attackers. Goes wrong because a typical firm also faces dishonest insiders, and the same credentials/access that enable legitimate work enable insider fraud. Fix: Include insider threat scenarios explicitly in the threat model.
- Feature-Only Design: Designing systems purely for legitimate use cases without adversarial analysis. Goes wrong because any feature that enables scale for users also enables scale for attackers. Fix: For each capability, explicitly model how a bad actor would weaponize it at scale.
- Static Threat Assessment: Treating the threat model as fixed at design time. Goes wrong because adversary capabilities and tools migrate (e.g., spy tools become criminal tools) over a system's lifetime. Fix: Revisit threat models periodically and ask how the adversary landscape has shifted.
- Narrow Security Research Perspective: Security community dominated by a demographic that ignores personal/interpersonal threats like stalking and harassment. Goes wrong because these threats affect the majority of users. Fix: Include abuse scenarios affecting marginalized and non-technical users in security design.

## When To Apply

Load this page when:

- Use this when starting security design for a new system and needing to decide which threat classes to defend against and how much to invest in each.
- Use this when evaluating whether a proposed feature could be weaponized — apply abusability analysis before shipping.
- Use this when a system handles user-generated content or communications at scale, to assess whether the angry-mob / coordinated harassment attack surface has been modeled.
- Use this when building authentication or access control and needing to classify whether the threat is mass opportunistic attack, spear-phishing, or insider abuse.
- Use this when advising on logging and monitoring requirements — sufficient to distinguish opportunistic botnet infection from targeted persistent attack.
- Use this when a system involves financial transactions, credentials, or PII, to apply the criminal specialization model and understand which underground market roles could exploit it.
- Use this when a feature relies on trust in infrastructure providers (e.g., cloud APIs, email) and needing to assess whether state-level PRISM-style interception is a relevant threat.
- Use this when doing incident response planning — ensures the plan addresses forensics, communications, and identification of attacker sophistication level before an incident occurs.

## Concrete Examples

- NSA PRISM program: built as warranted law-enforcement wiretap infrastructure but used for mass foreign intelligence collection, unknown even to Google's own mail and security teams until Snowden revealed it in June 2013.
- GCHQ Tempora: tapped 200 transatlantic fibre optic cables in Cornwall alone, collecting up to 21 petabytes/day, retaining filtered content for 30 days — leveraging Britain's legacy 19th-century telegraph cable infrastructure.
- 1988 Internet Worm: a student experiment that escaped the lab, illustrating that early threats were accidental rather than criminal, and that the threat landscape was not always adversarial.
- Mid-2000s underground markets: enabled criminal division of labor — one gang writes malware, another harvests credentials, another cashes out — allowing cybercrime to scale like industrial manufacturing.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Who Is the Opponent?**

An LLM coding agent is particularly prone to the 'universal threat modeling' anti-pattern in reverse: it may generate code with no threat model at all, defaulting to happy-path assumptions because training data skews toward functional examples rather than adversarial ones. The agent also cannot intrinsically know which of the four adversary categories is relevant to the deployment context, so without explicit prompting it will omit authentication, rate limiting, or audit logging that would only make sense if a specific threat class were assumed. Most critically, an LLM agent has no concept of a system's lifetime — it will not flag that a design decision safe today may become exploitable when spy-grade tools migrate to criminal ecosystems, making explicit threat-model documentation in prompts essential.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
