---
title: Secure Development and Assurance
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 8 pages
---

# Secure Development and Assurance

> Consolidated from 8 related concept pages.

---

## Annual Loss Expectancy ALE Quantitative risk model calculating expected loss ann

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## DevSecOps Lifecycle as Assurance The software development lifecycle extended to

## Core Principle

Chapter 28 argues that the old model of security assurance — one-time pre-market evaluation against a static standard — is obsolete and was always more about liability deflection than actual security. Assurance is now a continuous, dynamic, and politically contested process requiring DevSecOps practices, long-term patch commitments, usability-aware design, and the merging of safety and security engineering as all devices become networked. The central imperative is that no system should ever be declared 'done': sustainability of security posture, not correctness at a point in time, is the operative goal.

## Key Heuristics

These are the load-bearing rules for this concept.

> One way is to make it so simple that there are obviously no deficiencies. The other way is to make it so complicated that there are no obvious deficiencies.

> We're never done, and nobody who says they are done should be trusted.

> Assurance is no longer static.

> The idea that a device should be secure because someone spent $100,000 getting an evaluation lab to test it five years ago would strike most people nowadays as quaint.

> Assurance is thus a political and economic process. It is also a dynamic process.

> You can't have safety without security.

> Too many researchers take the view that 'If it's not perfect, it's no good.'

## Anti-Patterns & Fixes

- Static Certification as Liability Shield: Vendors obtain a one-time evaluation certificate not to improve security but to deflect legal liability, after which security investment stagnates. Fix: Treat assurance as a continuous process with ongoing patching commitments and post-deployment monitoring.
- Protecting the Wrong Things: Teams invest in securing assets or boundaries that are not the actual risk surface due to neglected or vague policy definition. Fix: Explicitly define and validate the security policy before selecting mechanisms or building test suites.
- Usability-Ignorant Security Design: Systems designed for alert, experienced professionals fail in practice because ordinary users make errors or bypass controls entirely. Fix: Include usability testing as a first-class assurance activity and design mechanisms tolerant of human error.
- Insecure-by-Default Libraries: Developers use ECB mode encryption because it is the default in many crypto libraries, not because it is appropriate. Fix: Enforce secure defaults at the library/toolchain level and deprecate libraries that default to insecure modes.
- Over-Privileged Code: Developers run code with administrator privilege rather than configuring OS access controls because the controls are too complex. Fix: Make access control configuration simple enough that the secure path is the path of least resistance.
- Regulatory Capture: Vendors game evaluation systems and work to capture regulators, causing standards to reflect vendor interests rather than user risk. Fix: Maintain adversarial independence in evaluation bodies and require transparency of methodology.

## When To Apply

Load this page when:

- Use this when deciding whether a shipped codebase is 'secure enough' to release — the answer requires continuous monitoring commitments, not a one-time checklist.
- Use this when selecting a cryptographic library or security primitive — check that defaults are secure (e.g., not ECB mode) before accepting the library's out-of-box behavior.
- Use this when a system that was previously air-gapped or offline is being connected to the Internet — apply DevSecOps patching infrastructure before deployment, not after.
- Use this when writing or reviewing a security policy — verify that the policy identifies the correct assets and threat actors, not just the ones that are easy to protect.
- Use this when evaluating a third-party component with a security certification — treat the certification date and scope critically; a five-year-old Common Criteria cert is insufficient assurance for a live networked system.
- Use this when integrating safety-critical systems (automotive, medical, industrial) with network connectivity — both safety and security standards must be applied together, not separately.
- Use this when assessing how long a deployed system must be supported — sustainability requires a defined patch-support window and automated update infrastructure, not just initial correctness.

## Concrete Examples

- Underwriters' Laboratories (UL): Founded 1894 by the US insurance industry to evaluate fire and security products; shows how third-party evaluation aligns incentives when one party bears the cost of failure.
- High-security lock bumping: Labs certified locks to resist picking in 2000 but said nothing about bumping attacks; by 2010 bumping was a major threat, illustrating how static standards fail to track evolving attack techniques.
- ECB mode as crypto default: Developers use ECB mode not by choice but because it is the default in many cryptographic libraries, propagating a known-insecure mode at scale.
- ML/deep neural networks trained on biased data: Vision systems trained mostly on photos of white people perform worse on darker-skinned individuals, raising the concern that autonomous vehicles could disproportionately harm Black pedestrians — illustrating the need for continuous safety assessment of AI systems.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Assurance and Sustainability**

An LLM coding agent faces a compounded version of the static-assurance anti-pattern: it generates code at a point in time based on training data, with no inherent mechanism for tracking newly discovered vulnerabilities, deprecated defaults, or evolved threat models in the deployed artifact. Agents are especially prone to the 'protecting the wrong things' failure because they optimize for satisfying the stated prompt rather than interrogating whether the stated policy reflects actual risk. To apply this chapter's lessons, an agent must be explicitly instructed to flag patching infrastructure requirements, reject insecure library defaults, and treat any generated security-sensitive code as requiring continuous review rather than one-time correctness.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Risk Register with Severity x Probability Scoring A structured method of listing

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Safety Security Convergence The merging of historically separate safety certific

## Core Principle

Chapter 28 argues that the old model of security assurance — one-time pre-market evaluation against a static standard — is obsolete and was always more about liability deflection than actual security. Assurance is now a continuous, dynamic, and politically contested process requiring DevSecOps practices, long-term patch commitments, usability-aware design, and the merging of safety and security engineering as all devices become networked. The central imperative is that no system should ever be declared 'done': sustainability of security posture, not correctness at a point in time, is the operative goal.

## Key Heuristics

These are the load-bearing rules for this concept.

> One way is to make it so simple that there are obviously no deficiencies. The other way is to make it so complicated that there are no obvious deficiencies.

> We're never done, and nobody who says they are done should be trusted.

> Assurance is no longer static.

> The idea that a device should be secure because someone spent $100,000 getting an evaluation lab to test it five years ago would strike most people nowadays as quaint.

> Assurance is thus a political and economic process. It is also a dynamic process.

> You can't have safety without security.

> Too many researchers take the view that 'If it's not perfect, it's no good.'

## Anti-Patterns & Fixes

- Static Certification as Liability Shield: Vendors obtain a one-time evaluation certificate not to improve security but to deflect legal liability, after which security investment stagnates. Fix: Treat assurance as a continuous process with ongoing patching commitments and post-deployment monitoring.
- Protecting the Wrong Things: Teams invest in securing assets or boundaries that are not the actual risk surface due to neglected or vague policy definition. Fix: Explicitly define and validate the security policy before selecting mechanisms or building test suites.
- Usability-Ignorant Security Design: Systems designed for alert, experienced professionals fail in practice because ordinary users make errors or bypass controls entirely. Fix: Include usability testing as a first-class assurance activity and design mechanisms tolerant of human error.
- Insecure-by-Default Libraries: Developers use ECB mode encryption because it is the default in many crypto libraries, not because it is appropriate. Fix: Enforce secure defaults at the library/toolchain level and deprecate libraries that default to insecure modes.
- Over-Privileged Code: Developers run code with administrator privilege rather than configuring OS access controls because the controls are too complex. Fix: Make access control configuration simple enough that the secure path is the path of least resistance.
- Regulatory Capture: Vendors game evaluation systems and work to capture regulators, causing standards to reflect vendor interests rather than user risk. Fix: Maintain adversarial independence in evaluation bodies and require transparency of methodology.

## When To Apply

Load this page when:

- Use this when deciding whether a shipped codebase is 'secure enough' to release — the answer requires continuous monitoring commitments, not a one-time checklist.
- Use this when selecting a cryptographic library or security primitive — check that defaults are secure (e.g., not ECB mode) before accepting the library's out-of-box behavior.
- Use this when a system that was previously air-gapped or offline is being connected to the Internet — apply DevSecOps patching infrastructure before deployment, not after.
- Use this when writing or reviewing a security policy — verify that the policy identifies the correct assets and threat actors, not just the ones that are easy to protect.
- Use this when evaluating a third-party component with a security certification — treat the certification date and scope critically; a five-year-old Common Criteria cert is insufficient assurance for a live networked system.
- Use this when integrating safety-critical systems (automotive, medical, industrial) with network connectivity — both safety and security standards must be applied together, not separately.
- Use this when assessing how long a deployed system must be supported — sustainability requires a defined patch-support window and automated update infrastructure, not just initial correctness.

## Concrete Examples

- Underwriters' Laboratories (UL): Founded 1894 by the US insurance industry to evaluate fire and security products; shows how third-party evaluation aligns incentives when one party bears the cost of failure.
- High-security lock bumping: Labs certified locks to resist picking in 2000 but said nothing about bumping attacks; by 2010 bumping was a major threat, illustrating how static standards fail to track evolving attack techniques.
- ECB mode as crypto default: Developers use ECB mode not by choice but because it is the default in many cryptographic libraries, propagating a known-insecure mode at scale.
- ML/deep neural networks trained on biased data: Vision systems trained mostly on photos of white people perform worse on darker-skinned individuals, raising the concern that autonomous vehicles could disproportionately harm Black pedestrians — illustrating the need for continuous safety assessment of AI systems.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Assurance and Sustainability**

An LLM coding agent faces a compounded version of the static-assurance anti-pattern: it generates code at a point in time based on training data, with no inherent mechanism for tracking newly discovered vulnerabilities, deprecated defaults, or evolved threat models in the deployed artifact. Agents are especially prone to the 'protecting the wrong things' failure because they optimize for satisfying the stated prompt rather than interrogating whether the stated policy reflects actual risk. To apply this chapter's lessons, an agent must be explicitly instructed to flag patching infrastructure requirements, reject insecure library defaults, and treat any generated security-sensitive code as requiring continuous review rather than one-time correctness.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Safety Security Entanglement Model Safety and security are co emergent propertie

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Security Development Lifecycle SDL Microsofts structured process for integrating

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Static vs Dynamic Assurance The distinction between one off pre market evaluatio

## Core Principle

Chapter 28 argues that the old model of security assurance — one-time pre-market evaluation against a static standard — is obsolete and was always more about liability deflection than actual security. Assurance is now a continuous, dynamic, and politically contested process requiring DevSecOps practices, long-term patch commitments, usability-aware design, and the merging of safety and security engineering as all devices become networked. The central imperative is that no system should ever be declared 'done': sustainability of security posture, not correctness at a point in time, is the operative goal.

## Key Heuristics

These are the load-bearing rules for this concept.

> One way is to make it so simple that there are obviously no deficiencies. The other way is to make it so complicated that there are no obvious deficiencies.

> We're never done, and nobody who says they are done should be trusted.

> Assurance is no longer static.

> The idea that a device should be secure because someone spent $100,000 getting an evaluation lab to test it five years ago would strike most people nowadays as quaint.

> Assurance is thus a political and economic process. It is also a dynamic process.

> You can't have safety without security.

> Too many researchers take the view that 'If it's not perfect, it's no good.'

## Anti-Patterns & Fixes

- Static Certification as Liability Shield: Vendors obtain a one-time evaluation certificate not to improve security but to deflect legal liability, after which security investment stagnates. Fix: Treat assurance as a continuous process with ongoing patching commitments and post-deployment monitoring.
- Protecting the Wrong Things: Teams invest in securing assets or boundaries that are not the actual risk surface due to neglected or vague policy definition. Fix: Explicitly define and validate the security policy before selecting mechanisms or building test suites.
- Usability-Ignorant Security Design: Systems designed for alert, experienced professionals fail in practice because ordinary users make errors or bypass controls entirely. Fix: Include usability testing as a first-class assurance activity and design mechanisms tolerant of human error.
- Insecure-by-Default Libraries: Developers use ECB mode encryption because it is the default in many crypto libraries, not because it is appropriate. Fix: Enforce secure defaults at the library/toolchain level and deprecate libraries that default to insecure modes.
- Over-Privileged Code: Developers run code with administrator privilege rather than configuring OS access controls because the controls are too complex. Fix: Make access control configuration simple enough that the secure path is the path of least resistance.
- Regulatory Capture: Vendors game evaluation systems and work to capture regulators, causing standards to reflect vendor interests rather than user risk. Fix: Maintain adversarial independence in evaluation bodies and require transparency of methodology.

## When To Apply

Load this page when:

- Use this when deciding whether a shipped codebase is 'secure enough' to release — the answer requires continuous monitoring commitments, not a one-time checklist.
- Use this when selecting a cryptographic library or security primitive — check that defaults are secure (e.g., not ECB mode) before accepting the library's out-of-box behavior.
- Use this when a system that was previously air-gapped or offline is being connected to the Internet — apply DevSecOps patching infrastructure before deployment, not after.
- Use this when writing or reviewing a security policy — verify that the policy identifies the correct assets and threat actors, not just the ones that are easy to protect.
- Use this when evaluating a third-party component with a security certification — treat the certification date and scope critically; a five-year-old Common Criteria cert is insufficient assurance for a live networked system.
- Use this when integrating safety-critical systems (automotive, medical, industrial) with network connectivity — both safety and security standards must be applied together, not separately.
- Use this when assessing how long a deployed system must be supported — sustainability requires a defined patch-support window and automated update infrastructure, not just initial correctness.

## Concrete Examples

- Underwriters' Laboratories (UL): Founded 1894 by the US insurance industry to evaluate fire and security products; shows how third-party evaluation aligns incentives when one party bears the cost of failure.
- High-security lock bumping: Labs certified locks to resist picking in 2000 but said nothing about bumping attacks; by 2010 bumping was a major threat, illustrating how static standards fail to track evolving attack techniques.
- ECB mode as crypto default: Developers use ECB mode not by choice but because it is the default in many cryptographic libraries, propagating a known-insecure mode at scale.
- ML/deep neural networks trained on biased data: Vision systems trained mostly on photos of white people perform worse on darker-skinned individuals, raising the concern that autonomous vehicles could disproportionately harm Black pedestrians — illustrating the need for continuous safety assessment of AI systems.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Assurance and Sustainability**

An LLM coding agent faces a compounded version of the static-assurance anti-pattern: it generates code at a point in time based on training data, with no inherent mechanism for tracking newly discovered vulnerabilities, deprecated defaults, or evolved threat models in the deployed artifact. Agents are especially prone to the 'protecting the wrong things' failure because they optimize for satisfying the stated prompt rather than interrogating whether the stated policy reflects actual risk. To apply this chapter's lessons, an agent must be explicitly instructed to flag patching infrastructure requirements, reject insecure library defaults, and treat any generated security-sensitive code as requiring continuous review rather than one-time correctness.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Two Questions Framework Every secure system development effort must continuously

## Core Principle

Secure systems development has no silver bullet: it requires fox knowledge—thousands of specific practices spanning risk management, threat modeling, organizational design, and safety-security integration. Risk must be systematically quantified via tools like ALE and risk registers, but practitioners must recognize when numbers reflect data versus guesswork versus politics. Security and safety are co-emergent properties that must be designed in from the start, and organizational incentive failures are as dangerous as technical ones.

## Key Heuristics

These are the load-bearing rules for this concept.

> There is no silver bullet — no magic formula that makes an intrinsically hard job easy.

> The fox knows many things; the hedgehog one big thing. Managing secure development is fox knowledge rather than hedgehog knowledge.

> Both safety and security are emergent properties that really have to be baked in from the beginning.

> Developers with a clean, expressive set of specific security requirements can build a very tight machine. They don't have to be security gurus, but they have to understand what they're trying to build and how it should work.

> Success is about attitudes and work practices as well as skills.

> ALEs may be of some value, but you need to understand what parts are based on data, what parts on guesswork, and what parts on office politics.

> Too much of the typical firm's resilience budget has been captured by compliance, safety theatre and security theatre.

## Anti-Patterns & Fixes

- Silver Bullet Chasing: Adopting a single methodology (e.g., Agile, Orange Book compliance) as the complete solution to secure development, ignoring the thousand small things that actually matter. Fix: Treat security as fox knowledge—accumulate and apply many specific practices rather than following one doctrine.
- ALE Theater: Security consultants list all conceivable threats, attach arbitrary probabilities, compute inflated ALEs, then back-calculate numbers to fit the CISO's pre-approved budget. Fix: Clearly label which ALE entries are data-driven vs. guesswork vs. politically motivated; use insurance quotes as a sanity check.
- Risk Register Captured by Loudest Stakeholder: Risk prioritization gets distorted by powerful internal groups (e.g., security agencies dominating pandemic preparedness budgets). Fix: Assign explicit senior ownership of each risk and use structured cross-functional risk committees to counterbalance capture.
- Safety-Security Siloing: Teaching and practicing security separately from safety engineering, missing the complex entanglement between the two. Fix: Integrate safety and security engineering from requirements through design, recognizing accidents create attack surfaces and attacks create safety hazards.
- Compliance Over Risk Management: Directing the majority of security development effort toward satisfying audit checklists rather than actual threat mitigation. Fix: Design feedback mechanisms that measure real risk reduction, not checklist completion, and assign accountability for residual risk.
- Ignoring Organizational Behavior as a Threat: Treating insider threats only as malicious actors while ignoring perverse incentives, toxic cultures, and high staff turnover as systemic security risks. Fix: Audit organizational incentive structures as part of the security review; treat management failures as a category of insider threat.

## When To Apply

Load this page when:

- Use this when defining security requirements for a new system, to ensure specifications are specific and actionable enough that developers without deep security expertise can implement them correctly.
- Use this when performing a threat modeling exercise, to apply ALE methodology and distinguish data-driven risk estimates from guesswork before prioritizing mitigations.
- Use this when a project is adopting a new development methodology (Agile, DevSecOps, etc.) and stakeholders treat it as a complete security solution, to reframe it as one tool among many.
- Use this when integrating a safety-critical component (automotive, medical device, aviation software) with a security-sensitive system, to identify where safety failures create attack surfaces and vice versa.
- Use this when reviewing whether security controls are compliance-driven or risk-driven, to redirect effort from security theater toward actual threat mitigation.
- Use this when building or auditing a risk register, to check that high-probability/low-drama risks are not being systematically underweighted relative to low-probability/high-drama risks that attract political attention.
- Use this when onboarding a development team to a security-sensitive project, to establish that security and safety properties must be designed in from the start, not retrofitted.

## Concrete Examples

- UK National Risk Register (2017) rated pandemic influenza at severity 5 / likelihood 4 (750,000 potential deaths), yet pandemic preparedness was underfunded relative to terrorism because the National Security Council was dominated by intelligence agencies.
- Bank ALE table: SWIFT fraud ($50M × 0.005 = $250K ALE), ATM fraud large ($250K × 0.2 = $100K), ATM fraud small ($20K × 0.5 = $10K), teller cash theft ($3,240 × 200 = $648K ALE)—showing common small losses can dominate rare large ones.
- University risk register example: 'loss of research contract income due to economic downturn' scored 5 (severity) × 4 (probability) = 20, mitigated to 16 by a rule restricting contract income to hiring contract staff only.
- Cambridge undergraduate curriculum reform (2017): security and software engineering courses were merged because real-world systems require both, and separating them produced graduates unprepared for their entanglement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Secure Systems Development**

An LLM coding agent is particularly prone to the Silver Bullet and ALE Theater anti-patterns: it will confidently apply a single known security pattern (e.g., input sanitization) as if it addresses all threats, and will generate plausible-sounding risk scores without any grounding in real incident data. Unlike a human developer who accumulates fox knowledge through experience, an agent must be explicitly prompted to enumerate the full threat space, flag which mitigations are data-supported vs. heuristic, and check whether safety and security requirements have been co-analyzed—or it will silently optimize for compliance appearance over actual risk reduction.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
