---
title: Query Set Size Control: A threshold-based mechanism requiring that any query answer be computed from at least t records, preventing direct identification of individuals from small sets
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Inference-Control.json]
contributing_chapters: ["Inference Control"]
confidence: high
---

# Query Set Size Control: A threshold-based mechanism requiring that any query answer be computed from at least t records, preventing direct identification of individuals from small sets

> From chapter: *Inference Control*

## Core Principle

Inference control addresses the fundamental impossibility of reliably anonymizing rich personal datasets by stripping identifiers: auxiliary data, query composition (trackers), and aggregation attacks make re-identification easy in nearly all real-world cases. Differential privacy is the only framework with a solid mathematical foundation, but it is applicable mainly to well-structured query workloads like census statistics; for most commercial and medical datasets, the data are too rich and the threat model too open for any current technique to provide genuine anonymization. The chapter warns that the persistent belief in 'anonymization as magic solution'—driven by commercial and government incentives—leads to repeated privacy failures and that meaningful protection requires either formal differential privacy guarantees or radical data minimization.

## Key Heuristics

These are the load-bearing rules for this concept.

> 'Anonymized data' is one of those holy grails, like 'healthy ice-cream' or 'selectively breakable crypto'.

> This only works in some well-defined special cases, such as a national census – where we have a solid theory in the form of differential privacy. In most cases, the data are just too rich and re-identification of data subjects is easy.

> General trackers are usually easy to find. Provided the minimum query set size n is less than a quarter of the total number of statistics N, and there are no further restrictions on the type of queries that are allowed, then we can find formulae that provide general trackers.

> Query auditing turns out to be an NP-complete problem.

> The constant hype around big data and machine learning makes the education task harder, just as these technologies are making anonymity much harder still.

> A more robust privacy regulator would have told them to just install their own meters at their own transformers.

> Protection that is not precise will usually carry some cost in terms of the range of queries that the database can answer and may therefore degrade its usefulness.

## Anti-Patterns & Fixes

- Name-Stripping Anonymization: Believing that removing names and addresses makes data non-personal, ignoring the richness of remaining attributes that enable re-identification. Fix: Apply differential privacy or rigorous cell suppression with formal disclosure analysis; treat quasi-identifiers and attribute combinations as seriously as direct identifiers.
- Naive Query Set Size Threshold: Setting a minimum query set size t without also banning queries on sets of size N−t or handling subset relationships, leaving tracker attacks open. Fix: Enforce that query set sizes fall strictly between t and N−t, and check subset containment constraints across successive queries.
- Ignoring Aggregation Attacks: Publishing multiple low-sensitivity statistics that can be combined to reveal a high-sensitivity conclusion (e.g., average salary by gender in a small department). Fix: Audit all publishable query combinations, suppress complementary queries, and apply perturbation to prevent exact back-calculation.
- Privacy Theater via Contractual Plans: Approving privacy plans that nominally aggregate data but leave single-household feeders exposed in practice (e.g., smart meter data with 0.96% single-house feeders). Fix: Audit the actual data distribution before approving aggregation schemes; require sensor placement at the infrastructure level rather than consumer level.
- Repeating Solved Mistakes: Modern privacy system developers being unaware of 1970s–1980s inference control theory and repeating the same attacks. Fix: Ground any new anonymization implementation in Denning's 1982 work, the Adam/Wortman 1989 survey, and the FCSM disclosure limitation methodology before designing novel mechanisms.
- Tokenization as Anonymization: Treating tokenized or pseudonymized identifiers as equivalent to anonymization for compliance purposes. Fix: Recognize that tokenization is reversible and that re-identification via auxiliary data makes tokenized records still personal data under GDPR and similar frameworks.

## When To Apply

Load this page when:

- Use this when designing an API or database query interface that returns aggregate statistics over a dataset containing personal or sensitive records.
- Use this when a user asks to 'anonymize' a dataset by removing names, emails, or IDs before sharing or publishing it.
- Use this when implementing a privacy-preserving analytics pipeline and choosing how much noise to inject or which query types to allow.
- Use this when building a data release mechanism (e.g., census-style bulk export, research data portal) and needing to determine which cell counts or statistics must be suppressed.
- Use this when evaluating a third-party claim that a dataset has been de-identified and is safe to use without consent or data-sharing agreements.
- Use this when generating synthetic data and needing to reason about whether synthetic records can be used to reconstruct original records via membership inference.
- Use this when a coding task involves joining or correlating multiple 'anonymized' datasets that might share quasi-identifiers like age, zip code, or timestamps.
- Use this when implementing differential privacy mechanisms (Laplace/Gaussian noise, privacy budget tracking) to understand their formal guarantees and practical limits.

## Concrete Examples

- US Census up to the 1960s: one record in a thousand released on tape with names and addresses removed, noise added, extreme values (e.g., very high incomes in small villages) suppressed to prevent back-calculation.
- Cambridge University Computer Lab salary attack: two queries ('average salary professors?' and 'average salary male professors?') suffice to deduce the sole female professor's salary, illustrating the subset tracker vulnerability.
- New York Times December 2019 analysis: mobile-phone location history of 12 million Americans over a few months used to identify celebrities, police, Secret Service officers, and sex-industry customers without difficulty.
- UK smart meters privacy plan: a distribution network operator receiving half-hourly meter data for its region, where 0.96% of feeders serve only one house, making individual household consumption trivially identifiable despite nominal aggregation commitments.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Inference Control**

An LLM coding agent is especially prone to the name-stripping anti-pattern: when asked to 'anonymize data before sharing,' it will confidently drop PII columns and declare the task done, without reasoning about quasi-identifier combinations, tracker attacks, or the formal disclosure budget—mistakes that human developers at least occasionally catch through code review or policy checklists. An agent generating query interfaces or analytics APIs may also silently implement query set size thresholds without the complementary N−t bound or subset-containment checks, producing code that appears correct but is trivially broken by tracker sequences. Agents should be prompted to invoke differential privacy libraries (e.g., OpenDP, Google DP library) and to explicitly enumerate quasi-identifiers and query composition risks rather than treating identifier removal as sufficient.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
