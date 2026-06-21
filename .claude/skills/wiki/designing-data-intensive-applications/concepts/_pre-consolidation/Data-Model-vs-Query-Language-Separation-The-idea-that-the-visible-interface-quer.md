---
title: Data Model vs Query Language Separation: The idea that the visible interface (query language) and the underlying model (relational, document, graph) are distinct layers with independent tradeoffs
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-I-Foundations-of-Data-Systems.json]
contributing_chapters: ["Part I: Foundations of Data Systems"]
confidence: high
---

# Data Model vs Query Language Separation: The idea that the visible interface (query language) and the underlying model (relational, document, graph) are distinct layers with independent tradeoffs

> From chapter: *Part I: Foundations of Data Systems*

## Core Principle

Part I establishes the conceptual vocabulary and analytical frameworks for reasoning about any data system: reliability, scalability, and maintainability as evaluative lenses; data models, query languages, storage engines, and serialization formats as independently variable design dimensions. The section deliberately addresses single-machine fundamentals before tackling distributed complexity in Part II. Mastery of these foundations is prerequisite to making principled tradeoffs in system design.

## Key Heuristics

These are the load-bearing rules for this concept.

> Different storage engines are optimized for different workloads, and choosing the right one can have a huge effect on performance.

> Different models are appropriate to different situations.

> Schemas need to adapt over time.

> Reliability, scalability and maintainability — examine what we actually mean with these words and how we can try to achieve them.

## Anti-Patterns & Fixes

- One-Size-Fits-All Storage Engine: Defaulting to a single storage engine regardless of workload type. Fix: Evaluate whether the workload is read-heavy, write-heavy, or mixed and select the engine optimized for that pattern.
- Ignoring Schema Evolution in Serialization Choice: Choosing a data encoding format based only on current schema without considering future changes. Fix: Evaluate serialization formats (e.g., Avro, Protobuf, Thrift) explicitly on their schema migration and backward/forward compatibility guarantees.
- Treating Reliability/Scalability/Maintainability as Synonyms: Using these terms loosely or interchangeably leads to vague system requirements. Fix: Define each property precisely and separately when specifying or reviewing a system.
- Conflating Data Model with Query Language: Assuming a given query language implies a specific data model or vice versa. Fix: Evaluate data model and query language as independent dimensions when selecting a database.

## When To Apply

Load this page when:

- Use this when selecting a database for a new service and needing a framework to compare options across model, engine, and encoding dimensions.
- Use this when a system is underperforming and the cause may be a mismatch between storage engine choice and actual workload characteristics.
- Use this when designing a data schema that will need to evolve as application requirements change, requiring evaluation of serialization format compatibility.
- Use this when writing a system design document and needing precise definitions of reliability, scalability, and maintainability to anchor requirements.
- Use this when a distributed system design is being initiated and foundational single-machine concepts need to be established before addressing distributed-specific concerns.
- Use this when reviewing a data pipeline and needing to assess whether the encoding format supports backward and forward compatibility for schema changes.

## Concrete Examples

- Chapter 1 examines the specific meanings of reliability, scalability, and maintainability as concrete engineering goals.
- Chapter 2 compares multiple data models and query languages as the most visible difference between databases from a developer's perspective.
- Chapter 3 examines how databases lay out data on disk as a concrete illustration of storage engine internals.
- Chapter 4 examines how serialization formats handle schema changes over time as a concrete evaluation criterion.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Part I: Foundations of Data Systems**

An LLM coding agent is prone to defaulting to the most statistically common technology choice (e.g., PostgreSQL, JSON serialization) without evaluating workload fit, schema evolution needs, or scalability requirements — exactly the failure modes this framework prevents. By anchoring decisions to the RSM triad and explicit model/engine/encoding axes, an agent can be prompted to justify each technology choice against concrete criteria rather than pattern-matching to familiar stacks. This also prevents agents from conflating distinct concerns (e.g., treating a document store as a drop-in for a relational one) when generating infrastructure or data-layer code.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
