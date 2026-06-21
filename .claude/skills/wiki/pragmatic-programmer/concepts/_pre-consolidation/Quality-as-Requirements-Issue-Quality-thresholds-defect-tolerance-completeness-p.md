---
title: Quality as Requirements Issue: Quality thresholds (defect tolerance, completeness, polish) must be specified and agreed upon with users as explicit requirements, not assumed by the developer
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Good-Enough-Software.json]
contributing_chapters: ["Good-Enough Software"]
confidence: high
---

# Quality as Requirements Issue: Quality thresholds (defect tolerance, completeness, polish) must be specified and agreed upon with users as explicit requirements, not assumed by the developer

> From chapter: *Good-Enough Software*

## Core Principle

Good-Enough Software reframes quality as a negotiable, explicit requirement rather than an absolute ideal, arguing that software meeting agreed-upon standards delivered promptly is more valuable than delayed perfection. Developers must involve users in setting quality thresholds and must recognize when further refinement yields diminishing or negative returns. 'Good enough' does not mean sloppy—it means disciplined alignment between what is built and what is actually required.

## Key Heuristics

These are the load-bearing rules for this concept.

> Make Quality a Requirements Issue

> Great software today is often preferable to perfect software tomorrow.

> Don't spoil a perfectly good program by overembellishment and over-refinement.

> The scope and quality of the system you produce should be specified as part of that system's requirements.

> You can discipline yourself to write software that's good enough—good enough for your users, for future maintainers, for your own peace of mind.

> It would be unprofessional to ignore these users' requirements simply to add new features to the program, or to polish up the code just one more time.

> It is equally unprofessional to promise impossible time scales and to cut basic engineering corners to meet a deadline.

## Anti-Patterns & Fixes

- Infinite Refinement Loop: Developer keeps polishing and adding features beyond what users need, delaying delivery and often degrading coherence. Fix: Treat quality level as a stated requirement; stop when that requirement is met.
- Unilateral Quality Decisions: Developer assumes the required quality level without consulting users, either over-delivering (late) or under-delivering (shoddy). Fix: Explicitly negotiate quality thresholds with stakeholders as part of requirements gathering.
- Corner-Cutting Under Deadline: Promising impossible timelines and then gutting engineering fundamentals to ship. Fix: Push back on unrealistic schedules; 'good enough' means meeting real requirements, not skipping foundational correctness.
- Perfectionism Paralysis: Withholding usable software while pursuing a perfect version, denying users early feedback that would improve the final product. Fix: Release working software early to capture user feedback via tracer-bullet iterations.

## When To Apply

Load this page when:

- Use this when deciding whether to add more features or polish before shipping a working implementation that already meets stated requirements.
- Use this when a user or stakeholder has not specified a quality level and you must decide how much testing, refactoring, or optimization to apply.
- Use this when under time or budget pressure and determining which quality attributes (performance, robustness, polish) can be relaxed versus which are non-negotiable.
- Use this when iteratively generating code and facing the question of whether another refinement pass will improve or over-complicate the solution.
- Use this when a system is functional but imperfect, to decide whether to ship or continue refining.
- Use this when working on safety-critical or widely-distributed library code, as a reminder that 'good enough' thresholds are domain-dependent and may be very strict.

## Concrete Examples

- A U.S. company orders 100,000 ICs from a Japanese manufacturer specifying a 1-in-10,000 defect rate; the manufacturer ships the defective units separately in a small labeled box, illustrating precise quality control that software rarely achieves.
- Pacemakers, the space shuttle, and widely-disseminated low-level libraries cited as domains where quality requirements are stringent and 'good enough' thresholds are very high.
- Programming compared to painting: overworking a canvas with layer upon layer ruins the piece, just as over-refining code obscures its clarity.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Good-Enough Software**

An LLM coding agent is prone to two opposite failure modes this chapter directly addresses: it may keep regenerating or refining code indefinitely without a stopping criterion, or it may ship a superficially complete solution that cuts corners on correctness because no explicit quality threshold was provided. Unlike a human who feels fatigue or external time pressure, an agent has no intrinsic stopping signal and must be given explicit quality requirements as part of its prompt/task specification. Applying this framework means the agent should surface quality trade-offs to stakeholders rather than silently deciding, and should halt refinement once stated requirements are provably met rather than optimizing unboundedly.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
