---
title: Options-Over-Excuses Framework: When something goes wrong, replace excuse-making with a structured enumeration of actionable alternatives to salvage or improve the situation
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/The-Cat-Ate-My-Source-Code.json]
contributing_chapters: ["The Cat Ate My Source Code"]
confidence: high
---

# Options-Over-Excuses Framework: When something goes wrong, replace excuse-making with a structured enumeration of actionable alternatives to salvage or improve the situation

> From chapter: *The Cat Ate My Source Code*

## Core Principle

This chapter establishes that pragmatic programmers actively own their commitments, honestly admit mistakes and ignorance, and always respond to failure with options rather than excuses. Responsibility is a deliberate agreement that requires upfront risk analysis and contingency planning, not just best-effort execution. The core discipline is replacing blame and excuse with a structured pivot to what can be done.

## Key Heuristics

These are the load-bearing rules for this concept.

> Provide Options, Don't Make Lame Excuses

> The greatest of all weaknesses is the fear of appearing weak.

> We can be proud of our abilities, but we must be honest about our shortcomings—our ignorance as well as our mistakes.

> When you make a mistake (as we all do) or an error in judgment, admit it honestly and try to offer options.

> Don't blame someone or something else, or make up an excuse.

> Before you approach anyone to tell them why something can't be done, is late, or is broken, stop and listen to yourself.

> If there was a risk that the vendor wouldn't come through for you, then you should have had a contingency plan.

## Anti-Patterns & Fixes

- Blame Deflection: Attributing failures to vendors, languages, management, or coworkers instead of owning the outcome. Fix: Acknowledge your role in the failure and immediately pivot to presenting concrete options for resolution.
- Excuse-Making Without Alternatives: Saying something 'can't be done' without offering what can be done. Fix: Enumerate salvage options—refactoring, prototyping, better testing, automation, or requesting additional resources.
- Unmitigated Risk Acceptance: Committing to responsibilities without identifying risks beyond your control or forming contingency plans. Fix: Analyze risks upfront, establish contingencies, and reserve the right to decline impossible commitments.
- No Backup / Single Point of Failure Complacency: Assuming infrastructure (e.g., disk, source control) won't fail and having no recovery plan. Fix: Automate backups and redundancy as a non-negotiable baseline before accepting responsibility for a deliverable.

## When To Apply

Load this page when:

- Use this when a coding agent has produced broken, incomplete, or late output and must communicate status to a user or orchestrating system.
- Use this when a dependency, API, or external tool fails and the agent must decide how to respond rather than simply reporting an error.
- Use this when an agent realizes mid-task that it lacks the knowledge or capability to complete the commitment it accepted.
- Use this when an agent is about to output a rationale for why a task cannot be completed, requiring a self-check for viable alternatives first.
- Use this when an agent accepted a task without flagging known risks and those risks have materialized, requiring honest acknowledgment and a recovery plan.
- Use this when an agent must decide whether to accept a new task that has a high probability of failure due to ambiguous requirements or missing context.

## Concrete Examples

- A disk crash destroys all source code with no backup, and the developer must tell their boss—the 'cat ate my source code' scenario.
- A vendor fails to deliver, and the developer had no contingency plan, illustrating unmitigated risk.
- Talking through an excuse to a rubber duck on your monitor or a cat before voicing it to a manager, to test whether it sounds reasonable.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**The Cat Ate My Source Code**

An LLM coding agent cannot rely on 'I didn't know' as an excuse—it should proactively flag uncertainty before committing to a task rather than silently producing incorrect output and then rationalizing it. A key agent failure mode this prevents is confidently delivering broken code while deflecting by attributing failure to ambiguous requirements or tool errors, rather than surfacing options like requesting clarification, generating a prototype, or recommending additional test coverage. The 'run through the conversation in your mind' heuristic maps directly to an agent doing a self-consistency check on its output before delivery, catching lame outputs before they reach the user.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
