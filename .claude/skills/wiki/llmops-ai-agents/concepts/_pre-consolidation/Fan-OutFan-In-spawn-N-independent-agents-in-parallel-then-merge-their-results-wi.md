---
title: Fan-Out/Fan-In: spawn N independent agents in parallel, then merge their results with explicit conflict resolution logic
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Pattern-Parallel-Fan-Out-Agents.json]
contributing_chapters: ["Pattern: Parallel Fan-Out Agents"]
confidence: high
---

# Fan-Out/Fan-In: spawn N independent agents in parallel, then merge their results with explicit conflict resolution logic

> From chapter: *Pattern: Parallel Fan-Out Agents*

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
