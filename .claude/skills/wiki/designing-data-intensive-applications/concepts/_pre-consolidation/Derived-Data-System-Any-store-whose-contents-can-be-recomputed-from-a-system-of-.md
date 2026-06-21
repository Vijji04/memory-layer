---
title: Derived Data System: Any store whose contents can be recomputed from a system of record, including caches, indexes, materialized views, and denormalized tables
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-III-Derived-Data.json]
contributing_chapters: ["Part III: Derived Data"]
confidence: high
---

# Derived Data System: Any store whose contents can be recomputed from a system of record, including caches, indexes, materialized views, and denormalized tables

> From chapter: *Part III: Derived Data*

## Core Principle

Part III introduces the foundational distinction between systems of record (authoritative, normalized, written first) and derived data systems (recomputable transformations such as caches, indexes, and materialized views). Real applications require multiple specialized datastores, making explicit dataflow design — knowing which system produces and which consumes each dataset — the central architectural discipline. The section previews batch and stream processing as the primary mechanisms for keeping derived data synchronized with its source.

## Key Heuristics

These are the load-bearing rules for this concept.

> If there is any discrepancy between another system and the system of record, then the value in the system of record is (by definition) the correct one.

> If you lose derived data, you can re-create it from the original source.

> Derived data is technically redundant, in the sense that it duplicates existing information. However, it is often essential for getting good performance on read queries.

> The distinction between system of record and derived data system depends not on the tool, but on how you use it in your application.

> By being clear about which data is derived from which other data, you can bring clarity to an otherwise confusing system architecture.

> Integrating disparate systems is one of the most important things that needs to be done in a non-trivial application.

## Anti-Patterns & Fixes

- Single-Database Assumption: Assuming one database can satisfy all access patterns leads to performance bottlenecks and architectural rigidity. Fix: Deliberately compose multiple specialized stores (OLTP, search index, cache, analytics) and define explicit dataflow between them.
- Vendor All-in-One Belief: Trusting a vendor claim that their product satisfies all needs causes neglect of integration concerns. Fix: Treat multi-system integration as a first-class architectural concern from the start.
- Implicit Dataflow: Not distinguishing which stores are authoritative versus derived causes confusion about which value to trust on conflict. Fix: Explicitly label each store as either a system of record or a derived system and document the transformation pipeline.
- Treating Derived Data as Authoritative: Writing mutations directly to a cache, index, or materialized view bypasses the system of record and creates inconsistency. Fix: Always write to the system of record first; let derived systems be populated through a defined derivation process.

## When To Apply

Load this page when:

- Use this when designing a service that needs both low-latency reads and durable writes, requiring a cache or read replica alongside a primary database.
- Use this when two datastores disagree on the value of the same entity and the correct value must be determined.
- Use this when adding a search index, materialized view, or recommendation engine on top of an existing transactional database.
- Use this when a new microservice needs to consume data originally owned by another service's database.
- Use this when deciding whether a derived dataset (e.g., a pre-aggregated analytics table) can be safely deleted or must be preserved.
- Use this when architecting ETL or streaming pipelines to ensure the directionality and ownership of data transformations is unambiguous.
- Use this when debugging a data inconsistency to identify which store is authoritative and which is stale derived data.

## Concrete Examples

- Cache as derived data: served from cache if present, falls back to the underlying database if missing, and can be fully reconstructed from the source.
- Recommendation system: predictive summary data derived from usage logs, representing a transformed view of raw event data.
- Denormalized values, indexes, and materialized views cited as canonical examples of derived data systems.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Part III: Derived Data**

An LLM coding agent is prone to generating code that writes to whichever store is most convenient in the local context (e.g., updating a cache directly) without respecting the system-of-record hierarchy, silently corrupting the authoritative source of truth. Agents also tend to scaffold single-database solutions by default, missing the need for explicit dataflow wiring between specialized stores. Applying this framework forces the agent to annotate each store it references as authoritative or derived and to route mutations correctly through the system of record before propagating to derived systems.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
