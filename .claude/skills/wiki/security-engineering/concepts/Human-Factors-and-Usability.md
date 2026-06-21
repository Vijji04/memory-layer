---
title: Human Factors and Usability
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 7 pages
---

# Human Factors and Usability

> Consolidated from 7 related concept pages.

---

## Affordances Gibson The physical or interface environment presents action possibi

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Behavioral Economics Heuristics and Biases People make systematically irrational

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Dual Process System 1 System 2 Fast intuitive System 1 thinking handles routine

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Human Machine Cognition Complementarity The principle that biometric systems sho

## Core Principle

Biometrics authenticate identity by measuring anatomy, physiology, or ingrained behavior, with three systems now deployed at scale: phone fingerprints, iris recognition, and face recognition. All biometric systems involve a tunable tradeoff between false-accept and false-reject rates, and published performance figures are routinely inflated by excluding hard-to-classify users; even the best current systems cannot simultaneously meet the banking industry's 1% fraud / 0.01% insult target. Weak biometrics can be adequate when embedded in strong social and legal context, while strong biometrics can fail when deployed without liveness detection, attended supervision, or consideration of human cognitive biases introduced by machine-assisted review.

## Key Heuristics

These are the load-bearing rules for this concept.

> Even a weak biometric like handwritten signature verification can be effective if it is well embedded in the social and legal matrix.

> Biometrics are usually more powerful in attended operation, where with good system design the relative strengths and weaknesses of the human and the machine may complement one another.

> Historically, many biometric systems achieved most of their effect by deterring criminals rather than actually identifying them.

> Context matters; even a weak biometric can be effective if well embedded in the social and legal matrix.

> Vendors typically exclude people without eyes from statistics on iris scanners and manual workers with worn fingertips from fingerprint statistics. This can lead to deceptive performance claims.

> UK banks set a target for biometrics of a fraud rate of 1% and an insult rate of 0.01%, which was beyond the state of the art in signature verification and fingerprint scanning – as indeed it still is.

> When a biometric becomes very widely used, there may be an increased risk of forgery in unattended operation: photographs of irises, fingerprint moulds and even good old-fashioned forged signatures must all be thought of in system design.

## Anti-Patterns & Fixes

- GoatExclusion: Vendors exclude hard-to-classify users (worn fingerprints, missing eyes) from benchmark statistics, making published EER figures unrealistically optimistic. Fix: Always test on the full target population including edge cases; demand performance figures that include excluded groups.
- UnattendedDeploymentOverconfidence: Deploying a biometric system designed for attended use in an unattended context without accounting for spoofing attacks (photo of iris, fingerprint mould). Fix: Explicitly model liveness detection and forgery risk as a function of attendance level during system design.
- HumanBiasFromComputerOutput: Presenting a human examiner with the computer's top-ranked match biases the examiner toward confirming the machine's answer. Fix: Present multiple matches (e.g., top 3 plus 2 poor matches) to preserve independent human judgment and test examiner alertness.
- StatisticalBenchmarkMisuse: Using equal error rate as the sole design metric ignores asymmetric real-world cost of fraud vs. insult. Fix: Define the operational fraud/insult rate targets first (e.g., fraud ≤1%, insult ≤0.01%), then tune the ROC operating point to meet both.
- ContextStrippedBiometrics: Deploying biometric authentication without the surrounding legal, procedural, and social framework that gives it deterrent and evidentiary value. Fix: Co-design the biometric mechanism with the liability, audit trail, and dispute-resolution processes around it.
- ForcingHumanAdaptation: Designing biometric UX that treats users as a nuisance who must adapt to the technology, degrading human performance. Fix: Design systems that work within social norms and support human cognition as advised by psychologists.

## When To Apply

Load this page when:

- Use this when designing an authentication system that must choose between biometric modalities (fingerprint, face, iris, voice) and needs to compare their error rate tradeoffs.
- Use this when configuring the sensitivity threshold of a biometric classifier and needing to balance false-accept (security risk) against false-reject (user friction).
- Use this when evaluating a vendor's published accuracy claims for a biometric SDK and needing to identify whether excluded populations inflate the reported performance.
- Use this when building a biometric pipeline that combines automated matching with a human review step and needing to avoid anchoring bias in the human reviewer.
- Use this when deploying a mobile biometric (e.g., fingerprint unlock) and needing to assess whether liveness detection is required to prevent spoofing by a stolen device.
- Use this when selecting an authentication mechanism for a high-value transaction flow and needing to understand whether legal liability shifts based on the mechanism chosen (PIN vs. signature vs. biometric).
- Use this when integrating a third-party biometric API and needing to establish what the equal error rate means operationally for your specific user population and threat model.
- Use this when designing a large-scale identity verification system and needing to account for the privacy, civil liberties, and regulatory constraints around biometric data storage.

## Concrete Examples

- India's Aadhaar project: iris codes and fingerprints enrolled for over one billion people, the world's largest biometric identity program.
- Tablet-based signature recognition achieving a best equal error rate of 1% only after excluding 'goats' — users whose templates do not classify well.
- UK banks' 1990s target of 1% fraud rate and 0.01% insult rate, which fingerprint and signature systems still cannot meet.
- Professional document examiners misattributing 6.5% of pairwise signature comparisons versus untrained controls at 38.3% error rate.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Biometrics**

An LLM coding agent generating biometric authentication code faces a critical failure mode: it will default to published benchmark EER figures (which exclude goats and edge cases) when configuring thresholds, systematically underestimating real-world false-accept rates for diverse user populations. Unlike a human engineer who iterates through user testing, the agent has no feedback loop to discover that its threshold is tuned for an unrepresentative sample. Additionally, when an agent scaffolds a human-in-the-loop review pipeline on top of a biometric matcher, it will typically pass only the top-ranked match to the reviewer — inadvertently encoding the anchoring anti-pattern — rather than presenting multiple candidates to preserve independent judgment.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Nudge Choice Architecture The way choices are presented systematically influence

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Security Usability Principle Whitten Tygar Security mechanisms fail when the cog

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Skill Rule Knowledge Error Stack Human errors in system operation fall into thre

## Core Principle

Security failures are predominantly psychological rather than purely technical: deception exploits predictable cognitive error patterns (slips, rule misapplication, and misconceptions), and security mechanisms fail when their correct use is harder than their incorrect use. The chapter argues that security engineers must internalize cognitive psychology, social psychology, and behavioral economics to design systems where safe behavior is the path of least resistance. The AI-native implication is that security APIs and defaults must be engineered to fail loudly on misuse, because neither human developers nor LLM agents reliably detect silent security errors.

## Key Heuristics

These are the load-bearing rules for this concept.

> Only amateurs attack machines; professionals target people.

> For an ideal technology, good use would be easier than bad use.

> To err is human — the predictable varieties of human error are rooted in the very nature of cognition.

> Humans are incapable of securely storing high-quality cryptographic keys, and they have unacceptable speed and accuracy when performing cryptographic operations.

> Deception, of various kinds, is now the principal mechanism used to defeat online security.

> As designers learn how to forestall the easier technical attacks, psychological manipulation of system users or operators becomes ever more attractive.

> You need to ensure that dangerous actions, such as installing software, require action sequences that are quite different from routine ones.

> Programs often appear to work even when protection mechanisms are used in quite mistaken ways.

## Anti-Patterns & Fixes

- Miller's Law Misapplication: Limiting all menu choices to 5 because short-term memory holds 7±2 items, ignoring that visual scanning and echoic memory are different faculties. Fix: Apply cognitive limits to the specific modality in use — visual menus can scale larger; spoken menus should stay at 3-4 items.
- Security-Hostile API Design: Designing access control and security APIs that are hard to understand and fidgety to use, causing programmers to misuse them. Programs appear to work even with incorrect protection mechanisms, so errors propagate via copy-paste. Fix: Design security APIs with safe defaults and make incorrect usage fail loudly at compile/test time.
- Routine-Action Danger Conflation: Making dangerous actions (e.g., installing software, granting permissions) use the same interaction pattern as routine actions (e.g., clicking OK on pop-ups), enabling capture errors. Fix: Require qualitatively different action sequences for high-risk operations.
- Post-Completion Error Trap: ATM-style flows that deliver the primary goal (cash) before the cleanup action (returning the card), causing users to abandon the cleanup step. Fix: Sequence flows so cleanup actions precede or gate delivery of the primary reward.
- Deceptive URL Rule Exploitation: Attackers exploit the heuristic 'look for the bank name in the URL' by prepending the trusted name (e.g., www.citibank.secureauthentication.com), bypassing users' rule-based checks. Fix: Train users and design UIs to highlight the registrable domain specifically, not just check for name presence.
- Scary-Interface Suppression: The computer industry deliberately makes computers seem non-threatening, which reduces users' appropriate wariness of online threats. Fix: Surface contextual risk signals at the moment of potential harm — e.g., highlight when a site is newly registered or when a file requests elevated permissions.

## When To Apply

Load this page when:

- Use this when designing an authentication flow or permission dialog to ensure that the secure path has lower friction than the insecure bypass.
- Use this when generating security API usage code — verify that incorrect usage patterns (wrong key type, missing signature check) produce explicit errors, not silent misbehavior.
- Use this when writing error messages or security warnings to ensure they are not dismissed as routine noise (avoiding habituation/warning fatigue).
- Use this when designing a multi-step sensitive operation (e.g., fund transfer, admin privilege escalation) to ensure the action sequence is distinct from everyday UI interactions.
- Use this when evaluating a URL parsing or link-display component to confirm the registrable domain is the visually prominent element, not just whether a trusted name appears anywhere.
- Use this when scaffolding a developer-facing security integration (OAuth, JWT, TLS config) to check that the default configuration is secure, not merely functional.
- Use this when generating code that copies authentication or encryption patterns from examples, to audit whether those examples encode known misconceptions about public/private key roles or signature verification.

## Concrete Examples

- Why Johnny Can't Encrypt (Whitten & Tygar): College students failed to correctly use PGP because they did not understand the distinction between public/private keys, encryption, and signatures — demonstrating cognitive-level security failure.
- Citibank phishing URL (www.citibank.secureauthentication.com): Attackers exploit the rule-based heuristic of looking for a bank's name in the URL rather than parsing the domain's actual registrant position.
- ATM card-return sequencing: ATMs that dispense cash before returning the card suffer higher card-abandonment rates due to post-completion error — the primary goal is achieved and the cleanup step is forgotten.
- Typosquatting: Attackers register domains visually similar to popular ones to harvest users who make slip-level typing errors, exploiting skill-level human error.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Psychology and Usability**

An LLM coding agent is especially prone to rule-level and cognitive-level errors described in this chapter: it will copy security patterns from training data that 'appear to work' even when protection mechanisms are used incorrectly (e.g., verifying a JWT signature with the public key embedded in the token itself), and it has no post-completion awareness — it will generate the happy-path code and omit cleanup steps like token invalidation or session teardown. Unlike a human who might notice a UI feels wrong, an LLM agent has no affordance perception and will not flag that a dangerous action uses the same code path as a routine one; it must be explicitly prompted to audit action-sequence distinctiveness and to test security API misuse paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
