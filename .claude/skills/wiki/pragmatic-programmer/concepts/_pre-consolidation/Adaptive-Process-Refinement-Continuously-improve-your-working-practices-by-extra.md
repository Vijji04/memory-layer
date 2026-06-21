---
title: Adaptive Process Refinement: Continuously improve your working practices by extracting the best elements from multiple methodologies and melding them into an evolving personal/team process
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Circles-and-Arrows.json]
contributing_chapters: ["Circles and Arrows"]
confidence: high
---

# Adaptive Process Refinement: Continuously improve your working practices by extracting the best elements from multiple methodologies and melding them into an evolving personal/team process

> From chapter: *Circles and Arrows*

## Core Principle

Formal development methodologies (UML, waterfall, CASE tools, etc.) are tools to be used selectively and critically, not authorities to obey blindly — their diagrams are designers' interpretations, not verified requirements, and their adoption always carries a real productivity cost. Pragmatic developers extract the best elements from multiple methods, prefer working prototypes over formal diagrams for validation, and continuously refine their process rather than accepting any methodology's rigid confines as limits. Expensive tools and elaborate diagrams do not guarantee better designs; the developers wielding them are still fallible.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Be a Slave to Formal Methods

> Expensive Tools Do Not Produce Better Designs

> Never become a slave to a methodology: circles and arrows make poor masters.

> Blindly adopting any technique without putting it into the context of your development practices and capabilities is a recipe for disappointment.

> Never underestimate the cost of adopting new tools and methods. Be prepared to treat the first projects using these techniques as a learning experience.

> Never accept the rigid confines of a methodology as the limits of your world.

> All that paper is still just their fallible interpretation of requirements and design.

> If the philosophy is 'the class diagram is the application, the rest is mechanical coding,' you know you're looking at a waterlogged project team.

## Anti-Patterns & Fixes

- Methodology Worship: Treating a formal method (UML, waterfall, etc.) as authoritative truth rather than one tool among many, causing teams to follow diagrams that no longer reflect reality. Fix: Adopt methods critically, extract useful parts, and override the method when your context demands it.
- Diagram-as-Requirement Fallacy: Using formal diagrams (class diagrams, use cases) as a substitute for validated user requirements, when users cannot read or verify them. Fix: Show users working prototypes to gather real feedback instead of relying on designer-interpreted diagrams.
- Specialization Silo Trap: Formal methods encouraging separate groups for data modeling, architecture, and requirements gathering, leading to poor communication and wasted effort. Fix: Ensure team members understand how all components interact, where data lives, and what requirements are.
- Static Model Bias: Formal methods pushing developers toward static object/data relationships that inhibit the dynamic, metadata-driven systems good software requires. Fix: Prefer designing adaptable, dynamic systems using metadata to allow runtime behavior changes.
- Driftwood Chasing: Latching onto the latest methodology fad as a solution to struggling projects without addressing the underlying development problems. Fix: Diagnose root causes of project failure rather than switching methodologies; refine existing practices incrementally.
- Tool Cost Bias: Overvaluing output from expensive tools simply because of their cost. Fix: Evaluate tool output on its own merits, completely independent of what the tool cost.

## When To Apply

Load this page when:

- Use this when a team proposes adopting a new formal methodology (UML, CASE tools, etc.) mid-project as a fix for struggling delivery.
- Use this when evaluating whether to generate or follow a formal class diagram or architecture diagram as the primary specification for implementation.
- Use this when a stakeholder presents extensive formal documentation (use case diagrams, ER diagrams) and expects the agent to treat it as ground truth for requirements.
- Use this when deciding how much weight to give to an expensive or prestigious modeling tool's output versus direct user feedback.
- Use this when a project's process feels rigidly locked to a single methodology and is failing to adapt to emerging information.
- Use this when asked to implement a system described entirely by static object models without consideration for runtime flexibility or metadata-driven behavior.
- Use this when assessing the trade-off between adopting a new structured approach versus the productivity cost during the learning and adoption period.

## Concrete Examples

- Historical parade of methodologies: structured programming, chief programmer teams, CASE tools, waterfall, spiral model, Jackson, ER diagrams, Booch clouds, OMT, Objectory, Coad/Yourdon, and UML — each enjoying temporary popularity before replacement.
- Robert Glass's 1999 CACM article reviewing productivity/quality research across seven software development technologies (4GLs, structured techniques, CASE tools, formal methods, clean room, process models, OO), finding initial hype overblown and benefits delayed by adoption productivity drops.
- The shipwreck/driftwood metaphor: developers on failing projects swimming from one methodology fad to the next, remaining adrift regardless of which piece of flotsam they grab.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Circles and Arrows**

An LLM coding agent is particularly susceptible to treating any formal schema, diagram description, or structured specification handed to it as authoritative ground truth, effectively becoming a slave to whatever artifact it was given — the agent equivalent of 'the class diagram is the application.' This prevents the agent from questioning whether the diagram reflects actual user needs, detecting static model bias in the spec, or flagging that a dynamically configurable design would be superior. Applying this chapter, an agent should treat input specifications as one fallible interpretation to reason about critically, not as a verified contract to implement mechanically.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
