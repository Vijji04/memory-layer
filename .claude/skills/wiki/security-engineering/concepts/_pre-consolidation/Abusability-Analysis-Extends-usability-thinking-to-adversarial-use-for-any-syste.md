---
title: Abusability Analysis: Extends usability thinking to adversarial use — for any system feature, ask how it could be weaponized or scaled as an attack vector, not just how legitimate users will interact with it
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Who-Is-the-Opponent.json]
contributing_chapters: ["Who Is the Opponent?"]
confidence: high
---

# Abusability Analysis: Extends usability thinking to adversarial use — for any system feature, ask how it could be weaponized or scaled as an attack vector, not just how legitimate users will interact with it

> From chapter: *Who Is the Opponent?*

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
