---
name: engineering-mindset
description: "Use when a coding agent must make architectural, quality, or design decisions during implementation — calibrating trade-offs, communicating honestly, and maintaining integrity across iterations."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [phase-1, swe-foundations, ai-native, coding-agent, quality, pragmatism]
    category: swe-foundations
    related_skills: [modular-architecture, production-readiness, agentic-swe-master]
---

# Engineering Mindset and Code Quality

## When to Load

- Use this when a coding agent is asked to fix a small bug and must decide whether to also flag or address surrounding code smells it encounters
- Use this when generating a solution that technically satisfies the immediate requirement but may conflict with stated architectural principles or long-term maintainability
- Use this when an agent-generated change introduces a minor quality regression and the agent must decide whether to flag it or silently proceed
- Use this when determining how much test coverage, error handling, or documentation to include — calibrate to the stated context and stakes
- Use this when an agent is operating across multiple iterations of a codebase and must assess whether incremental changes are collectively drifting the system in a bad direction
- Use this when an agent must communicate a failure or limitation honestly rather than producing a plausible-sounding but incorrect output
- Use this when evaluating whether a proposed shortcut is a legitimate pragmatic decision or a false economy that increases long-term cost
- Use this when a coding agent has produced broken, incomplete, or late output and must communicate status honestly
- Use this when a dependency, API, or external tool fails and the agent must decide how to respond rather than simply reporting an error
- Use this when an agent realizes mid-task that it lacks knowledge to complete the commitment it accepted
- Use this when an agent is about to output a rationale for why a task cannot be completed — self-check for viable alternatives first
- Use this when discovering a poorly designed function or module while working on an unrelated task — flag or fix it, never ignore
- Use this when asked to add a feature to a codebase that already contains known technical debt — avoid compounding it

## Core Rules

> Think beyond the immediate problem — place it in its larger context. Without this larger context, pragmatic compromises become uninformed guesses.

> Take responsibility for everything you produce. Don't watch a project fall apart through neglect.

> Sometimes near-perfection is the only option, but often there are trade-offs. Know which situation you are in before committing to an approach.

> Learning is continuous. An agent that stops questioning its own assumptions has stopped improving.

> Provide options, not excuses. When something cannot be done as asked, the first output must be alternatives — never a dead end.

> The greatest weakness is the fear of appearing weak. Honesty about uncertainty is a feature, not a failure.

> We can be proud of our abilities, but must be honest about our shortcomings — our ignorance as well as our mistakes.

> When you make a mistake or an error in judgment, admit it honestly and offer options for recovery.

> A good enough solution today that actually ships beats a perfect solution that never arrives. But only if "good enough" was a deliberate choice, not an accident.

> Broken windows compound. One piece of clearly bad code left unfixed tells the next engineer that the quality bar is low. Don't be the first broken window.

## Concept Map

Wiki root: $AGENTIC_SWE_WIKI_ROOT/pragmatic-programmer/concepts/

| Concept | When to read |
|---------|-------------|
| Broken-Window-Theory.md | Quality is degrading incrementally, team tolerance for mess is rising |
| DRY.md | Duplicated logic spotted — decide whether to refactor or note as debt |
| Orthogonality.md | A change to one module is breaking unrelated modules |
| Estimation.md | Agent must give a time or complexity estimate |
| Design-by-Contract.md | Writing or reviewing preconditions, postconditions, invariants |
| Assertive-Programming.md | Agent is about to add defensive code — should it assert or handle? |
| Debugging.md | Diagnosing a confusing failure with multiple possible root causes |
| Decoupling-and-Law-of-Demeter.md | Module is reaching through too many layers to get data |
| Code-Generators.md | Repetitive boilerplate can be automated — evaluate if it's worth it |
| Algorithm-Speed.md | Performance matters — choose data structure and algorithm deliberately |
| Domain-Languages.md | Business logic is complex enough to warrant a DSL |
| Documentation.md | How much, where, and when to write documentation |
| Refactoring.md | Incremental improvement vs full rewrite decision |
| Tracer-Bullets.md | Building end-to-end slice before full implementation |

## Common Pitfalls

- **False economy**: Skipping tests, error handling, or documentation to ship faster. Fix — calculate the operational cost of the shortcut, not just the development cost. Shortcuts that cost more to maintain than they saved to build are not pragmatic.

- **Silent quality drift**: Each change is fine in isolation but collectively the system degrades. Fix — at every non-trivial change, ask: is the overall system better, worse, or the same after this change?

- **Dishonest status**: Reporting "almost done" or "should work" when the agent knows there are unresolved issues. Fix — give a concrete status with specific blockers. Vague optimism is a trust liability.

- **Responsibility avoidance**: Blaming the requirements, the library, the user. Fix — own the decision that led to the problem; offer the recovery path, not the excuse.

- **Context collapse**: Solving the immediate requirement perfectly while ignoring that it conflicts with a stated architectural principle. Fix — always check the task against stated constraints before finalizing.

## Verification Checklist

- [ ] Every generated output has been checked against stated architectural principles, not just functional requirements
- [ ] Any quality regression introduced has been flagged explicitly
- [ ] Status is reported with specific blockers, not vague progress claims
- [ ] All alternatives were considered before declaring a task impossible
- [ ] Broken windows encountered were either fixed or logged as explicit debt
