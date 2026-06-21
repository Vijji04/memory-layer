---
title: Metadata in Plain Text: even when raw data must be binary, storing metadata as plain text preserves human readability and tool accessibility
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/14-The-Power-of-Plain-Text.json]
contributing_chapters: ["14. The Power of Plain Text"]
confidence: high
---

# Metadata in Plain Text: even when raw data must be binary, storing metadata as plain text preserves human readability and tool accessibility

> From chapter: *14. The Power of Plain Text*

## Core Principle

Plain text is the most durable, interoperable, and tool-accessible format for storing knowledge because it is self-describing and independent of the application that created it. The primary costs are storage size and parse performance, but these are acceptable in most contexts and can be mitigated by storing at least metadata in plain text even when raw data must be binary. Plain text enables version control, diffing, scripting, partial parsing, and long-term data survival—making it the pragmatic default for any persistent knowledge representation.

## Key Heuristics

These are the load-bearing rules for this concept.

> Keep Knowledge in Plain Text

> Human-readable forms of data, and self-describing data, will outlive all other forms of data and the applications that created them. Period.

> The problem with most binary formats is that the context necessary to understand the data is separate from the data itself.

> Binary data may be more obscure than plain text, but it is no more secure.

> All software becomes legacy as soon as it's written.

> Plain text doesn't mean that the text is unstructured.

> With plain text, you can achieve a self-describing data stream that is independent of the application that created it.

## Anti-Patterns & Fixes

- OpaqueBinaryStorage: storing data in binary format divorces data from its meaning, requiring full application logic to parse and making it unrecoverable if the application is lost. Fix: store data as plain text with meaningful field names so partial knowledge of the format is sufficient to extract value.
- CrypticFieldNames: using labels like Field19=467abe provides no human-understandable context, making data effectively encrypted. Fix: use descriptive names like DrawingType=UMLActivityDrawing or <SSNO> tags so intent is self-evident.
- SecurityThroughObscurity: assuming binary format protects sensitive data from users. Fix: explicitly encrypt sensitive values like passwords and use secure hashes as checksums for configuration integrity—don't rely on format opacity for security.
- AllOrNothingBinaryParsing: binary formats require knowing all details of the entire format to parse successfully. Fix: use plain text so partial extraction is possible even with incomplete knowledge of the schema.

## When To Apply

Load this page when:

- Use this when designing a configuration file format and choosing between binary serialization and a text-based format.
- Use this when storing application state or data that may need to be recovered, migrated, or inspected years after the original application is retired.
- Use this when creating test fixtures or synthetic data to drive automated tests and needing to update them without special tooling.
- Use this when integrating with version control systems and needing diff-able, auditable change history for configuration or data files.
- Use this when extracting data from a legacy system with unknown or partially documented format.
- Use this when deciding where to store metadata about binary data such as telemetry or database internals.
- Use this when evaluating whether obscuring a file format provides meaningful security for sensitive configuration values.

## Concrete Examples

- Field19=467abe (opaque binary-style field) vs. DrawingType=UMLActivityDrawing (self-describing plain text field)
- myprop.uses_menus=FALSE vs. 0010010101110101 — boolean property stored as readable text vs. raw binary encoding
- Legacy data file containing Social Security numbers: <FIELD10>123-45-6789</FIELD10> vs. AC27123456789B11P — demonstrating human-readable vs. human-understandable distinction
- sendmail complex configuration file placed under source code control, diffed with diff/fc, and checksummed with sum

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**14. The Power of Plain Text**

An LLM coding agent frequently generates serialization code, configuration schemas, and data storage decisions; defaulting to binary formats (pickle, protobuf, custom structs) produces outputs that future agents or tools cannot inspect, debug, or recover without the exact schema version—plain text formats prevent silent knowledge loss between pipeline stages. When an agent writes test fixtures or inter-service data contracts in binary, downstream agents cannot validate, modify, or diff them without special tooling, creating a brittle chain; plain text ensures every agent in the pipeline can read and reason about shared data without needing out-of-band context.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
