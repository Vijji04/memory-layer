---
title: Intent Classification Pipeline: classify incoming messages into typed intents with confidence scores before routing to any handler
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Pattern-Conversational-Agents.json]
contributing_chapters: ["Pattern: Conversational Agents"]
confidence: high
---

# Intent Classification Pipeline: classify incoming messages into typed intents with confidence scores before routing to any handler

> From chapter: *Pattern: Conversational Agents*

## Core Principle

Conversational agents at scale require a pipeline of discrete, separable stages — intent classification, policy-aware response generation, compliance gating, and escalation logic — rather than a single LLM call. The critical architectural principle is that verification must be a separate gate after generation, operating on atomically extracted claims rather than whole responses, so violations are precise and auditable. In regulated or high-stakes domains, every interaction must be logged immutably with full provenance, and uncertainty must default to human escalation rather than automated response.

## Key Heuristics

These are the load-bearing rules for this concept.

> conversation state is precious and fragile — track it wrong and you'll repeat yourself, route wrong and the customer gets transferred endlessly

> A single wrong response costs you a customer

> Compliance verification is a separate gate: don't embed it in response generation. Extract, verify, then decide.

> Break responses into claims: each claim is individually verifiable. Makes violations precise.

> Use LLM for semantic matching: exact string matching fails in domains with terminology variation.

> Escalate on uncertainty: healthcare is high-stakes. When verification fails, escalate to human. Better safe than liable.

> Audit everything: write-once logs with timestamps, patient ID, question, response, verification result, and escalation reason.

> Better to escalate than make promise without verification — 'we verified' is defensible, 'we guessed' is not

## Anti-Patterns & Fixes

- EmbeddedComplianceCheck: bundling policy verification inside the response generation step means a single LLM call must both generate and validate — violations become invisible. Fix: run a dedicated post-generation compliance gate that checks tone, data leaks, and policy separately.
- MonolithicResponseVerification: checking the entire generated response as one unit makes it impossible to isolate which part is wrong. Fix: extract atomic claims first, verify each independently so violations are specific and actionable.
- KeywordMatchingForPolicyVerification: exact string matching fails when domain language is paraphrased (e.g., '80% coverage' vs. 'your cost is 20%'). Fix: use LLM-based semantic matching against policy documents.
- AlwaysAutoRespond: routing every classified intent to auto-respond ignores that some intents (complaints, booking modifications) require human approval or availability checks. Fix: set can_auto_respond=False and escalation_threshold=1.0 for high-risk intents.
- MutableAuditLogs: modifiable logs allow tampering and break regulatory chain-of-custody. Fix: use a write-once audit database with immutable timestamps and system version fields.
- SingleConfidenceThreshold: applying one global escalation threshold across all intents causes over-escalation on simple requests and under-escalation on dangerous ones. Fix: assign per-intent escalation_threshold values calibrated to each intent's risk level.

## When To Apply

Load this page when:

- Use this when building a customer-facing agent that must route messages to different handlers based on user intent at high volume
- Use this when an agent generates responses that must comply with external policy documents (insurance, property rules, regulations) before delivery
- Use this when the same agent serves many tenants (properties, plans) each with distinct policies that must be fetched and injected at runtime
- Use this when an LLM response in a regulated domain (healthcare, finance, legal) must be auditable and defensible to regulators
- Use this when designing escalation logic that needs to differentiate between high-confidence automatable intents and low-confidence or high-risk intents requiring human review
- Use this when you need to maintain conversation state across multiple turns without context loss or repetition
- Use this when a wrong automated response carries legal liability or direct customer harm, requiring a verification layer before send

## Concrete Examples

- Booking.com GenAI messaging agent: classifies guest messages (early check-in, maintenance, complaints), fetches property-specific policies, generates and compliance-checks responses, routes to human if escalation threshold not met — processing millions of messages daily across 1.5M+ properties
- Alan health insurance agent: answers patient coverage questions, extracts individual claims from responses, verifies each claim against policy documents via LLM semantic matching, logs full interaction to write-once audit database, escalates to healthcare specialist when any claim cannot be verified

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Conversational Agents**

An LLM coding agent building conversational systems is prone to collapsing the pipeline — generating a response and treating it as already validated, skipping the explicit compliance gate and claim-extraction steps that a human architect would draw as separate boxes. This is especially dangerous because the agent has no external sense of regulatory liability; it will produce plausible-sounding code that omits the write-once audit trail or sets can_auto_respond=True for complaint intents. The claim-extraction-then-verify pattern is also non-obvious to generate without explicit prompting, yet it is the key architectural move that makes LLM-generated answers defensible in high-stakes domains.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
