---
title: Good Enough Software
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 4 pages
---

# Good Enough Software

> Consolidated from 4 related concept pages.

---

## Good Enough Software A discipline of producing software that satisfies stated re

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

---

## Good Enough Software Calibrate quality level to context near perfection when req

## Core Principle

The Pragmatic Philosophy chapter establishes that great developers are defined by attitude and context-awareness rather than technical skill alone: they own their outcomes, think beyond the immediate problem, resist both entropy and complacency, and calibrate quality to actual requirements. The chapter introduces named frameworks — responsibility, entropy control, good-enough calibration, knowledge portfolio, and change strategy — that serve as the operating philosophy for all subsequent practices. Pragmatism is not cutting corners; it is making intelligent, informed trade-offs grounded in a clear understanding of the larger system.

## Key Heuristics

These are the load-bearing rules for this concept.

> Think beyond the immediate problem, always trying to place it in its larger context, always trying to be aware of the bigger picture.

> Without this larger context, how can you be pragmatic? How can you make intelligent compromises and informed decisions?

> Take responsibility for everything they do.

> Pragmatic Programmers won't sit idly by and watch their projects fall apart through neglect.

> Sometimes near-perfection is the only option, but often there are trade-offs involved.

> Learning is a continuous and ongoing process.

## Anti-Patterns & Fixes

- Tunnel Vision: Solving the immediate problem without considering broader context, leading to solutions that conflict with system-wide goals or introduce downstream debt. Fix: Always ask what larger system or goal the current problem sits inside before writing a line of code.
- Blame Deflection (Cat Ate My Source Code): Attributing failures to external causes instead of owning outcomes, which blocks learning and erodes trust. Fix: Accept responsibility, communicate honestly about mistakes, and course-correct proactively.
- Neglect-Driven Entropy: Allowing small code quality issues to accumulate unchecked until the codebase becomes unmaintainable. Fix: Address broken windows (small defects, bad designs) immediately before entropy spreads.
- Boiled Frog Syndrome: Ignoring gradual negative change — creeping scope, slow performance degradation, incremental security weakening — because each step seems minor. Fix: Periodically step back to evaluate cumulative drift, not just the latest delta.
- Perfectionism Misapplication: Applying near-perfection standards uniformly regardless of context, wasting resources where good-enough is sufficient. Fix: Explicitly determine the required quality level for each deliverable based on its context and trade-offs.
- Static Knowledge Base: Relying on a fixed set of skills and knowledge acquired at one point in time. Fix: Treat knowledge as a portfolio requiring active, continuous investment and diversification.

## When To Apply

Load this page when:

- Use this when a coding agent is asked to fix a small bug and must decide whether to also flag or address surrounding code smells it encounters.
- Use this when generating a solution that technically satisfies the immediate requirement but may conflict with stated architectural principles or long-term maintainability.
- Use this when an agent-generated change introduces a minor quality regression and the agent must decide whether to flag it or silently proceed.
- Use this when determining how much test coverage, error handling, or documentation to include — calibrate to the stated context and stakes of the software.
- Use this when an agent is operating across multiple iterations of a codebase and must assess whether incremental changes are collectively drifting the system in a bad direction.
- Use this when an agent must communicate a failure or limitation honestly rather than producing a plausible-sounding but incorrect output.
- Use this when evaluating whether a proposed shortcut or trade-off is a legitimate pragmatic decision or a false economy that increases long-term cost.

## Concrete Examples

- The Cat Ate My Source Code: named section illustrating the failure mode of not taking responsibility for outcomes.
- Stone Soup and Boiled Frogs: a dual example — the stone soup story as a strategy for instigating change, and the boiled frog as a cautionary tale about ignoring gradual negative change.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**A Pragmatic Philosophy**

An LLM coding agent is especially prone to narrow-context optimization — it will produce code that perfectly satisfies the literal prompt while silently violating architectural intent, accumulating entropy, or over-engineering for the wrong quality target. The Radical Responsibility and Bigger Picture frameworks force the agent to treat each generation as an accountable act with downstream consequences, not a stateless token prediction. Specifically, the Boiled Frog anti-pattern maps directly to multi-turn agent sessions where each individual change looks acceptable but cumulative drift is invisible unless the agent is explicitly prompted to audit it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Know When to Stop Recognizing the inflection point where additional refinement d

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

---

## Quality as Requirements Issue Quality thresholds defect tolerance completeness p

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
