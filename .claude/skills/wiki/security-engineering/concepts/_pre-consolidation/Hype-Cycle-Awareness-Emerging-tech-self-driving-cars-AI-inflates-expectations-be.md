---
title: Hype Cycle Awareness: Emerging tech (self-driving cars, AI) inflates expectations beyond near-term feasibility; engineers must separate hype-driven timelines from engineering reality
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/New-Directions.json]
contributing_chapters: ["New Directions?"]
confidence: high
---

# Hype Cycle Awareness: Emerging tech (self-driving cars, AI) inflates expectations beyond near-term feasibility; engineers must separate hype-driven timelines from engineering reality

> From chapter: *New Directions?*

## Core Principle

Chapter 25 argues that the frontier security problems — autonomous vehicles, adversarial ML, privacy technologies, and electronic elections — all share a common structure: they fail not due to purely technical bugs but because they operate at the boundary between deterministic machines and unpredictable human society. The chapter documents the gap between hype-cycle predictions and operational reality (e.g., self-driving cars, AI timelines) and identifies the key engineering challenges as adversarial robustness of ML, emergent failures from subsystem integration, and sociotechnical threat models that extend beyond the software stack. It closes with a call to reallocate security investment away from politically driven 'security theater' toward rational, evidence-based risk management and long-term software sustainability.

## Key Heuristics

These are the load-bearing rules for this concept.

> Connecting the world meant that we also connected all the bad things and all the bad people, and now every social and political problem is expressed in software.

> If you campaign for liberty you're likely to find yourself drinking in bad company at the wrong end of the bar.

> The inability to infer the intentions of other drivers became a limiting factor.

> Each new assistive technology takes years to optimise and debug, and it's not straightforward to combine a dozen of them into an autopilot.

> The hype cycle passed, as it always does.

> We spend much of our social resilience budget on surveillance systems, when we should have been spending it on public health instead.

> Claims about system security properties are often thinly veiled assertions of power and control.

## Anti-Patterns & Fixes

- Hype-Driven Autonomy Timelines: Predicting full autonomy by arbitrary near-term dates (Musk: 2018, Brin: 2017) without accounting for the irreducible unpredictability of human actors. Fix: Ground timeline estimates in demonstrated capability under adversarial real-world conditions, not lab benchmarks.
- Security Theater Allocation: Spending security budget on visible, politically motivated controls rather than on highest-impact risk reduction. Fix: Use formal risk registers and empirical failure data to allocate protective resources rationally.
- Naive ML Deployment: Treating deep neural networks as reliable pattern matchers without adversarial robustness testing, allowing false pattern detection or adversarial manipulation. Fix: Apply adversarial ML analysis (e.g., Papernot's framework) before deployment in security-sensitive contexts.
- Monolithic Autopilot Assembly: Assuming that combining many independently validated assistive subsystems (ABS, ACC, AEB, LKA) trivially yields a safe full autopilot. Fix: Treat emergent interactions between subsystems as a distinct engineering and security problem requiring integration-level testing.
- Planned Obsolescence for Safety-Critical Software: Treating security patches as a 3-5 year consumer lifecycle issue when embedded software in cars, fridges, and infrastructure must be maintained for 20+ years. Fix: Design software architectures and vendor contracts that support long-term patching from the outset.
- Underspecified Threat Modeling for Human-Machine Boundaries: Modeling threats only from technical adversaries while ignoring politically motivated actors operating upstream/downstream of the technical system (e.g., election interference beyond the voting machine itself). Fix: Extend threat models to include the full sociotechnical lifecycle and non-technical attack vectors.

## When To Apply

Load this page when:

- Use this when designing or auditing an ML-based decision system that will operate in adversarial environments where inputs may be deliberately manipulated.
- Use this when building an autonomous or semi-autonomous system that must interact with unpredictable human actors (other drivers, pedestrians, voters) rather than a controlled environment.
- Use this when integrating multiple independently developed safety or security subsystems into a unified pipeline, where emergent interaction failures are likely.
- Use this when estimating delivery timelines for AI-powered features — hype cycle awareness prevents committing to timelines that ignore human-complexity failure modes.
- Use this when specifying software lifecycle requirements for embedded systems in consumer goods, vehicles, or infrastructure that must receive security patches for a decade or more.
- Use this when performing threat modeling for election systems, privacy tools, or any platform where politically motivated actors operate outside the software stack itself.
- Use this when evaluating vendor security certifications or third-party assurance claims, to account for vendor capture of evaluation processes and conflicts of interest.

## Concrete Examples

- Waymo's limited self-driving service in a 50-square-mile area of Phoenix (2020): unavailable in rain or dust storms, requiring real-time human monitoring — illustrating the gap between hype and operational reality.
- DARPA Grand Challenge (2004-2007): million-dollar prize for desert and urban self-driving, which bootstrapped a research community and led to Sebastian Thrun's Stanford robot Stanley using probabilistic ML for terrain and obstacle handling.
- Tesla Autopilot (2014): first commercial self-driving product, delivered as an over-the-air update, enabling freeway and stop-start traffic control but still far from full autonomy despite CEO predictions.
- Automatic Emergency Braking (AEB) false alarm problem: AEB activating unnecessarily when the car ahead slows to turn, because the system cannot infer driver intent — illustrating human unpredictability as a hard limit on automation.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**New Directions?**

An LLM coding agent is particularly vulnerable to the adversarial ML anti-pattern: it may generate ML pipeline code that lacks any adversarial robustness testing or input validation, treating model outputs as ground truth rather than as attack surfaces. Agents also tend to combine subsystems (e.g., assembling microservices, chaining tool calls) without modeling emergent security failures at integration boundaries — the same failure mode as naively composing automotive assistive technologies. Additionally, an agent estimating feasibility of AI features may reproduce hype-cycle optimism from its training data, recommending architectures that assume capabilities not yet demonstrated under real-world adversarial conditions.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
