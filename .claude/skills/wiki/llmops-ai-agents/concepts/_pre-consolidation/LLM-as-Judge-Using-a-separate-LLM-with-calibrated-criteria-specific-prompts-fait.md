---
title: LLM-as-Judge: Using a separate LLM with calibrated, criteria-specific prompts (faithfulness, groundedness, completeness, safety) to score agent outputs at scale, validated against human agreement rates
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Evaluation-Frameworks.json]
contributing_chapters: ["Evaluation Frameworks"]
confidence: high
---

# LLM-as-Judge: Using a separate LLM with calibrated, criteria-specific prompts (faithfulness, groundedness, completeness, safety) to score agent outputs at scale, validated against human agreement rates

> From chapter: *Evaluation Frameworks*

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
