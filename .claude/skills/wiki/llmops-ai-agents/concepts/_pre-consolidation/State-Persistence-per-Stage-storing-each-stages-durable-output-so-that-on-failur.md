---
title: State Persistence per Stage: storing each stage's durable output so that on failure, only the failed stage needs to be retried, not the full pipeline
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/Pattern-Sequential-Pipeline.json]
contributing_chapters: ["Pattern: Sequential Pipeline"]
confidence: high
---

# State Persistence per Stage: storing each stage's durable output so that on failure, only the failed stage needs to be retried, not the full pipeline

> From chapter: *Pattern: Sequential Pipeline*

## Core Principle

The Sequential Pipeline pattern structures processing as a linear DAG where each stage consumes the typed output of its predecessor, enabling strict dependency enforcement, per-stage failure recovery, and targeted observability. Key mechanisms include short-circuit routing for extreme conditions, quality gates to reject bad data early, durable intermediate state for partial retries, and Graph RAG for dependency-aware impact assessment. It is the correct pattern whenever stage N+1 is semantically invalid without the output of stage N.

## Key Heuristics

These are the load-bearing rules for this concept.

> Sequential beats parallel when: stages have strict dependencies. Output of N is input to N+1.

> Short-circuit logic saves latency: Critical alerts skip intermediate stages. Don't process normally if severity is max.

> Quality gates prevent garbage propagation: Reject low-confidence items early. Don't enrich bad data.

> State persistence enables recovery: Each stage's output is durable. Retry a single stage, not the full pipeline.

> Observability per stage is critical: Monitor where items get rejected. Bottleneck analysis requires per-stage metrics.

> Graph RAG for enrichment: Don't just search text. Traverse dependency graphs for true impact assessment.

> Normalization before mapping: Convert all units to SI first. Then mapping logic is cleaner (no conversion rules in framework logic).

> Compliance validation last: Don't flag missing disclosures until you have the full picture. Stage 5 is the audit gate.

## Anti-Patterns & Fixes

- Parallel execution of dependent stages: Running stages concurrently when later stages require prior stage output causes incorrect or empty inputs. Fix: enforce sequential execution with explicit data contracts passed forward.
- Enriching bad data: Passing low-confidence or invalid items through all pipeline stages wastes compute and produces unreliable outputs. Fix: add quality gates early to reject or quarantine bad data before enrichment.
- Full pipeline retry on failure: Restarting the entire pipeline when one stage fails discards already-completed work. Fix: persist each stage's output durably so only the failed stage needs to be re-run.
- Text-only RAG for relational impact: Using document similarity search to assess system dependencies misses structural relationships. Fix: use Graph RAG to traverse dependency graphs and find true downstream impact.
- No per-stage observability: Monitoring only end-to-end pipeline metrics hides where bottlenecks or rejection spikes occur. Fix: instrument each stage independently with latency, throughput, and rejection rate metrics.
- Embedding conversion logic inside framework mapping: Mixing unit conversion with framework-specific mapping logic creates coupling and duplication. Fix: normalize to canonical units in a dedicated stage before any framework mapping.

## When To Apply

Load this page when:

- Use this when each processing step requires the output of the previous step as its input (e.g., must enrich before classifying, must classify before recommending).
- Use this when you need to insert a human review or approval checkpoint between automated processing stages.
- Use this when a failure in one stage should allow retry of only that stage without reprocessing upstream work.
- Use this when you need per-stage monitoring to identify where items are being dropped, delayed, or rejected.
- Use this when impact or dependency analysis requires traversing a graph of relationships rather than searching text documents.
- Use this when processing high volumes of items (e.g., 100K+ alerts/day) and you need to track throughput and bottlenecks per stage.
- Use this when certain conditions (e.g., critical severity, zero confidence) should bypass intermediate stages and route directly to a final escalation step.
- Use this when data must be normalized to a canonical format before being mapped to multiple downstream schemas or compliance frameworks.

## Concrete Examples

- Deloitte cybersecurity triage pipeline: 5-stage sequential system (Enrichment → Classification → Impact Assessment via Graph RAG → Remediation Recommendation → Queue Routing) processing 100K+ daily security alerts
- ESG reporting pipeline: 5-stage system (Collect → Normalize → Map Frameworks → Generate Reports → Validate Compliance) producing GRI/CSRD/TCFD-compliant sustainability reports for enterprise clients

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Sequential Pipeline**

An LLM coding agent is prone to generating pipeline stages that silently ignore missing upstream outputs (e.g., treating None dest_asset as an empty string rather than halting), which propagates corrupt state without raising errors — a failure mode humans catch via code review but agents miss without explicit output contracts. Agents also tend to collapse sequential stages into a single monolithic function for brevity, eliminating the per-stage durability and observability that make the pattern valuable. Enforcing typed dataclass contracts at each stage boundary and explicit short-circuit conditions forces the agent to preserve the sequential structure and fail loudly on bad data.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
