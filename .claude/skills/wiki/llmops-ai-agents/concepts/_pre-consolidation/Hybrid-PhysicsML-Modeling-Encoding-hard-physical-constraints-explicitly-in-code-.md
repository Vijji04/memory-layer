---
title: Hybrid Physics+ML Modeling: Encoding hard physical constraints explicitly in code rather than learning them from data, then layering ML on top for optimization within those constraints
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Domain-Deep-Dives-Media-Telecom-Government-Industrial.json]
contributing_chapters: ["Domain Deep Dives: Media, Telecom, Government, Industrial"]
confidence: high
---

# Hybrid Physics+ML Modeling: Encoding hard physical constraints explicitly in code rather than learning them from data, then layering ML on top for optimization within those constraints

> From chapter: *Domain Deep Dives: Media, Telecom, Government, Industrial*

## Core Principle

This chapter establishes domain-specific architectural patterns for high-scale, high-stakes agent deployments: tiered filtering for cost-proportional content moderation, multi-model routing for manufacturing optimization, and a mandatory six-check safety gate for industrial physical systems. The central insight is that agent architecture must match the cost and risk topology of the domain — uniform processing, single-model designs, and learned safety limits are all anti-patterns that cause either cost explosion or catastrophic failure. Human oversight is not optional but structurally embedded at the point where model confidence falls below the cost of being wrong.

## Key Heuristics

These are the load-bearing rules for this concept.

> You can't run GPT-4 on every post.

> Rules are centralized, versioned, auditable. When a rule changes, it propagates to all 1 billion posts being processed that day.

> This model is deliberately imprecise. It's a filter, not a classifier. False positives at this stage are cheap (escalate to Tier 4). False negatives are expensive (violating content goes live).

> The multimodal model doesn't make binary decisions. It scores confidence. If uncertain, escalate.

> Don't learn machine limits from data. Encode them explicitly: Max temperature, max pressure, rated power. These are safety-critical.

> Confidence ≠ Accuracy. A model can be confident and wrong.

> Agents generate recommendations. Humans implement them.

> Don't apply recommendations to 100% at once. Start with 1%, then 10%, then 100%. Monitor at each stage. Rollback if problems.

> Multiple signals agreeing = high confidence. Signals conflicting = investigate sensor health.

## Anti-Patterns & Fixes

- Uniform Processing: Running the same expensive model on every input regardless of complexity. Fix: Use tiered filtering so cost scales with uncertainty — cheap deterministic checks first, expensive models only on ambiguous cases.
- Learning Safety Limits from Data: Treating max temperature or rated power as something a model should infer from historical examples. Fix: Encode physical constraints explicitly as hard-coded invariants that cannot be overridden by model output.
- Binary Model Decisions: Having a model return 'violates' or 'safe' with no confidence signal. Fix: Return confidence scores and route low-confidence outputs to a higher tier or human review.
- Single-Model Architecture: Using one model for all input types (standard, premium, recycled materials). Fix: Classify the input type first, then route to the model best suited for that type.
- Bulk Rollout of Physical Changes: Applying an agent's recommendation to 100% of a physical system at once. Fix: Stage rollout at 1%, 10%, 100% with monitoring and rollback capability at each stage.
- Trusting a Single Sensor: Making decisions based on one sensor reading in industrial contexts. Fix: Fuse multiple signal types (temperature + vibration + power + acoustic); conflicting signals should trigger sensor health investigation, not a decision.

## When To Apply

Load this page when:

- Use this when designing a content moderation or classification pipeline that must process billions of items daily within a cost budget.
- Use this when an agent must decide whether to auto-act or escalate a decision, and the cost of false negatives greatly exceeds the cost of false positives.
- Use this when building an agent that operates on physical infrastructure (power grid, manufacturing equipment) and must validate safety before executing any recommendation.
- Use this when a single ML model is being asked to handle inputs that vary dramatically in type, rarity, or risk level (standard vs. premium vs. recycled materials).
- Use this when an agent's outputs will be applied to a real-world system where rollback is possible but catastrophic failure is not, requiring staged deployment.
- Use this when encoding domain constraints for industrial or physical systems — distinguishing between learned heuristics (ML-appropriate) and hard safety limits (must be explicit code).
- Use this when designing human-in-the-loop workflows and need to determine at what confidence threshold to escalate to human review versus auto-act.
- Use this when a moderation or classification policy depends on legal, cultural, or jurisdictional context that cannot be fully captured in training data.

## Concrete Examples

- Meta's 1 billion daily posts moderation system requiring 30 million daily decisions, addressed with a 5-tier filtering architecture from hash checks ($0.00001/post) to human review.
- Meta's tiered cost breakdown: Tier 1 hash deduplication at ~$1K/day vs. running heavy models on all posts at ~$5M/day, with Tier 4 heavy models running only on ~5% of posts.
- Manufacturing paper/pulp advisor routing standard batches to historical retrieval, premium batches to physics simulation, and recycled batches to a hybrid rules+ML model, reducing scrap rate from 8% to 3%.
- Iberdrola grid reconfiguration scenario requiring all six safety checks (physical feasibility, N-1 redundancy, safety margins, staged rollout, monitoring+rollback, human approval) before applying changes to 100 power lines.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Domain Deep Dives: Media, Telecom, Government, Industrial**

An LLM coding agent generating moderation or classification pipelines will tend to default to a single-model architecture because that's the simplest code to write — it won't naturally produce tiered cost-aware routing unless explicitly prompted. More critically, an LLM agent generating industrial control code is prone to treating all constraints as soft (learnable) rather than hard (inviolable), which means it may produce code where safety limits are thresholds in a config file rather than structural invariants, creating silent failure modes when those values are changed. The Minimum Safety Architecture and explicit physics-constraint encoding patterns directly prevent these agent-specific failure modes.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
