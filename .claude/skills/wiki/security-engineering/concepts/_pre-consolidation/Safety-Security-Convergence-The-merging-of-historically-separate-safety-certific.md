---
title: Safety-Security Convergence: The merging of historically separate safety certification ecosystems (healthcare, aerospace, automotive) with security engineering as devices become networked
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Assurance-and-Sustainability.json]
contributing_chapters: ["Assurance and Sustainability"]
confidence: high
---

# Safety-Security Convergence: The merging of historically separate safety certification ecosystems (healthcare, aerospace, automotive) with security engineering as devices become networked

> From chapter: *Assurance and Sustainability*

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
