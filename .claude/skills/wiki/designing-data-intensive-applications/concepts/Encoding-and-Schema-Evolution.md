# Encoding-and-Schema-Evolution

## Backward/Forward Compatibility Duality: A two-directional compatibility model where backward compatibility means newer code can read older data, and forward compatibility means older code can read data written by newer code — both must be maintained simultaneously during rolling upgrades

---
title: Backward/Forward Compatibility Duality: A two-directional compatibility model where backward compatibility means newer code can read older data, and forward compatibility means older code can read data written by newer code — both must be maintained simultaneously during rolling upgrades
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-4-Encoding-and-Evolution.json]
contributing_chapters: ["Chapter 4: Encoding and Evolution"]
confidence: high
---


> From chapter: *Chapter 4: Encoding and Evolution*

## Core Principle

Data formats must support backward and forward compatibility because old and new code versions inevitably coexist during rolling upgrades and client deployments. Language-specific serialization formats are dangerous and non-evolvable; schema-driven binary formats (Thrift, Protocol Buffers, Avro) provide the strongest compatibility guarantees by encoding only field tags or resolving schemas at read time. The chapter establishes that encoding format choice is an architectural decision with long-term consequences for system evolvability, security, and operational simplicity.

## Key Heuristics

These are the load-bearing rules for this concept.

> Backward compatibility is normally not hard to achieve: as author of the newer code, you know the format of data written by older code, and so you can explicitly handle it. Forward compatibility can be trickier, because it requires older code to ignore additions made by a newer version of the code.

> For data that is used only internally within your organization, there is less pressure to use a lowest-common-denominator encoding format.

> It's generally a bad idea to use your language's built-in encoding for anything other than very transient purposes.

> The difficulty of getting different organizations to agree on anything outweighs most other concerns.

> With a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.

> Once you get into the terabytes, the choice of data format can have a big impact.

> Since they don't prescribe a schema, they need to include all object field names within the encoded data.

## Anti-Patterns & Fixes

- Language-Specific Serialization (e.g. Java Serializable, Python pickle): Ties data to one language, creates security vulnerabilities via arbitrary class instantiation, and neglects versioning and efficiency. Fix: Use language-agnostic formats like Protocol Buffers, Thrift, Avro, or JSON with explicit schemas.
- Using JSON/XML Numbers for Large Integers: Integers greater than 2^53 cannot be exactly represented in IEEE 754 double-precision float, causing silent data corruption in JavaScript consumers. Fix: Transmit large integers as decimal strings (as Twitter does with tweet IDs) or use a binary format with explicit integer types.
- Skipping Schemas for JSON/XML: Without schemas, correct interpretation of numbers, binary strings, and field types requires ad-hoc application code, making evolution error-prone. Fix: Use JSON Schema or XML Schema to enforce and document structure, or switch to a schema-driven binary format.
- Encoding Binary Data as Raw Bytes in JSON/XML: JSON and XML do not support binary strings natively. Fix: Encode binary data as Base64 text and annotate the schema to indicate the encoding, or use a binary format that natively supports byte sequences.
- Assuming Instantaneous Code Deployment: Treating schema changes as atomic across all nodes ignores the reality that old and new code versions coexist during rollouts. Fix: Design all schema changes to be simultaneously backward- and forward-compatible before deploying any code that depends on them.

## When To Apply

Load this page when:

- Use this when designing a data serialization format for a service that will undergo rolling deployments where multiple code versions run simultaneously.
- Use this when adding, renaming, or removing a field from a data schema shared between services or stored durably.
- Use this when choosing between JSON, Protocol Buffers, Thrift, or Avro for an internal microservice API.
- Use this when a service must read data written by a previous version of itself (e.g. reading old records from a database or message queue).
- Use this when a client application (mobile or desktop) may be running an older version than the server and must not crash on unknown fields.
- Use this when encoding data that crosses organizational boundaries and must remain interoperable across different language ecosystems.
- Use this when evaluating the security risk of deserializing data from an untrusted source using a language-native serialization library.
- Use this when a message queue or event log stores encoded messages that downstream consumers at different versions must be able to decode.

## Concrete Examples

- Twitter tweet IDs exceed 2^53 and cannot be exactly represented as JSON numbers in JavaScript, so Twitter's API returns each tweet ID twice: once as a JSON number and once as a decimal string.
- Java's built-in serialization (java.io.Serializable) is cited as notorious for bad performance and bloated encoding.
- Rolling upgrades: deploying a new server version to a few nodes at a time, requiring old and new code to coexist and handle each other's data formats.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 4: Encoding and Evolution**

An LLM coding agent is especially prone to generating language-native serialization (pickle, Java Serializable) as the path of least resistance when asked to 'save' or 'transmit' data, inadvertently creating security vulnerabilities and versioning dead-ends without flagging the tradeoffs. When generating data models or API schemas, an agent may not spontaneously add required/optional field annotations or tag numbers needed for safe evolution, because it lacks awareness of the multi-version deployment context unless explicitly prompted. This chapter's framework should be invoked by an agent whenever it generates any serialization, storage, or inter-service communication code, forcing it to explicitly reason about backward and forward compatibility before committing to a format.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Encoding Format Spectrum: A classification of data serialization formats from language-specific (most brittle, most convenient) to binary schema-driven (most compact, most evolvable) to human-readable text formats (most interoperable, least efficient)

---
title: Encoding Format Spectrum: A classification of data serialization formats from language-specific (most brittle, most convenient) to binary schema-driven (most compact, most evolvable) to human-readable text formats (most interoperable, least efficient)
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-4-Encoding-and-Evolution.json]
contributing_chapters: ["Chapter 4: Encoding and Evolution"]
confidence: high
---


> From chapter: *Chapter 4: Encoding and Evolution*

## Core Principle

Data formats must support backward and forward compatibility because old and new code versions inevitably coexist during rolling upgrades and client deployments. Language-specific serialization formats are dangerous and non-evolvable; schema-driven binary formats (Thrift, Protocol Buffers, Avro) provide the strongest compatibility guarantees by encoding only field tags or resolving schemas at read time. The chapter establishes that encoding format choice is an architectural decision with long-term consequences for system evolvability, security, and operational simplicity.

## Key Heuristics

These are the load-bearing rules for this concept.

> Backward compatibility is normally not hard to achieve: as author of the newer code, you know the format of data written by older code, and so you can explicitly handle it. Forward compatibility can be trickier, because it requires older code to ignore additions made by a newer version of the code.

> For data that is used only internally within your organization, there is less pressure to use a lowest-common-denominator encoding format.

> It's generally a bad idea to use your language's built-in encoding for anything other than very transient purposes.

> The difficulty of getting different organizations to agree on anything outweighs most other concerns.

> With a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.

> Once you get into the terabytes, the choice of data format can have a big impact.

> Since they don't prescribe a schema, they need to include all object field names within the encoded data.

## Anti-Patterns & Fixes

- Language-Specific Serialization (e.g. Java Serializable, Python pickle): Ties data to one language, creates security vulnerabilities via arbitrary class instantiation, and neglects versioning and efficiency. Fix: Use language-agnostic formats like Protocol Buffers, Thrift, Avro, or JSON with explicit schemas.
- Using JSON/XML Numbers for Large Integers: Integers greater than 2^53 cannot be exactly represented in IEEE 754 double-precision float, causing silent data corruption in JavaScript consumers. Fix: Transmit large integers as decimal strings (as Twitter does with tweet IDs) or use a binary format with explicit integer types.
- Skipping Schemas for JSON/XML: Without schemas, correct interpretation of numbers, binary strings, and field types requires ad-hoc application code, making evolution error-prone. Fix: Use JSON Schema or XML Schema to enforce and document structure, or switch to a schema-driven binary format.
- Encoding Binary Data as Raw Bytes in JSON/XML: JSON and XML do not support binary strings natively. Fix: Encode binary data as Base64 text and annotate the schema to indicate the encoding, or use a binary format that natively supports byte sequences.
- Assuming Instantaneous Code Deployment: Treating schema changes as atomic across all nodes ignores the reality that old and new code versions coexist during rollouts. Fix: Design all schema changes to be simultaneously backward- and forward-compatible before deploying any code that depends on them.

## When To Apply

Load this page when:

- Use this when designing a data serialization format for a service that will undergo rolling deployments where multiple code versions run simultaneously.
- Use this when adding, renaming, or removing a field from a data schema shared between services or stored durably.
- Use this when choosing between JSON, Protocol Buffers, Thrift, or Avro for an internal microservice API.
- Use this when a service must read data written by a previous version of itself (e.g. reading old records from a database or message queue).
- Use this when a client application (mobile or desktop) may be running an older version than the server and must not crash on unknown fields.
- Use this when encoding data that crosses organizational boundaries and must remain interoperable across different language ecosystems.
- Use this when evaluating the security risk of deserializing data from an untrusted source using a language-native serialization library.
- Use this when a message queue or event log stores encoded messages that downstream consumers at different versions must be able to decode.

## Concrete Examples

- Twitter tweet IDs exceed 2^53 and cannot be exactly represented as JSON numbers in JavaScript, so Twitter's API returns each tweet ID twice: once as a JSON number and once as a decimal string.
- Java's built-in serialization (java.io.Serializable) is cited as notorious for bad performance and bloated encoding.
- Rolling upgrades: deploying a new server version to a few nodes at a time, requiring old and new code to coexist and handle each other's data formats.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 4: Encoding and Evolution**

An LLM coding agent is especially prone to generating language-native serialization (pickle, Java Serializable) as the path of least resistance when asked to 'save' or 'transmit' data, inadvertently creating security vulnerabilities and versioning dead-ends without flagging the tradeoffs. When generating data models or API schemas, an agent may not spontaneously add required/optional field annotations or tag numbers needed for safe evolution, because it lacks awareness of the multi-version deployment context unless explicitly prompted. This chapter's framework should be invoked by an agent whenever it generates any serialization, storage, or inter-service communication code, forcing it to explicitly reason about backward and forward compatibility before committing to a format.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Rolling Upgrade / Staged Rollout: A deployment strategy where new code versions are deployed to a subset of nodes at a time, requiring that old and new code versions coexist and interoperate without breaking the system

---
title: Rolling Upgrade / Staged Rollout: A deployment strategy where new code versions are deployed to a subset of nodes at a time, requiring that old and new code versions coexist and interoperate without breaking the system
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-4-Encoding-and-Evolution.json]
contributing_chapters: ["Chapter 4: Encoding and Evolution"]
confidence: high
---


> From chapter: *Chapter 4: Encoding and Evolution*

## Core Principle

Data formats must support backward and forward compatibility because old and new code versions inevitably coexist during rolling upgrades and client deployments. Language-specific serialization formats are dangerous and non-evolvable; schema-driven binary formats (Thrift, Protocol Buffers, Avro) provide the strongest compatibility guarantees by encoding only field tags or resolving schemas at read time. The chapter establishes that encoding format choice is an architectural decision with long-term consequences for system evolvability, security, and operational simplicity.

## Key Heuristics

These are the load-bearing rules for this concept.

> Backward compatibility is normally not hard to achieve: as author of the newer code, you know the format of data written by older code, and so you can explicitly handle it. Forward compatibility can be trickier, because it requires older code to ignore additions made by a newer version of the code.

> For data that is used only internally within your organization, there is less pressure to use a lowest-common-denominator encoding format.

> It's generally a bad idea to use your language's built-in encoding for anything other than very transient purposes.

> The difficulty of getting different organizations to agree on anything outweighs most other concerns.

> With a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.

> Once you get into the terabytes, the choice of data format can have a big impact.

> Since they don't prescribe a schema, they need to include all object field names within the encoded data.

## Anti-Patterns & Fixes

- Language-Specific Serialization (e.g. Java Serializable, Python pickle): Ties data to one language, creates security vulnerabilities via arbitrary class instantiation, and neglects versioning and efficiency. Fix: Use language-agnostic formats like Protocol Buffers, Thrift, Avro, or JSON with explicit schemas.
- Using JSON/XML Numbers for Large Integers: Integers greater than 2^53 cannot be exactly represented in IEEE 754 double-precision float, causing silent data corruption in JavaScript consumers. Fix: Transmit large integers as decimal strings (as Twitter does with tweet IDs) or use a binary format with explicit integer types.
- Skipping Schemas for JSON/XML: Without schemas, correct interpretation of numbers, binary strings, and field types requires ad-hoc application code, making evolution error-prone. Fix: Use JSON Schema or XML Schema to enforce and document structure, or switch to a schema-driven binary format.
- Encoding Binary Data as Raw Bytes in JSON/XML: JSON and XML do not support binary strings natively. Fix: Encode binary data as Base64 text and annotate the schema to indicate the encoding, or use a binary format that natively supports byte sequences.
- Assuming Instantaneous Code Deployment: Treating schema changes as atomic across all nodes ignores the reality that old and new code versions coexist during rollouts. Fix: Design all schema changes to be simultaneously backward- and forward-compatible before deploying any code that depends on them.

## When To Apply

Load this page when:

- Use this when designing a data serialization format for a service that will undergo rolling deployments where multiple code versions run simultaneously.
- Use this when adding, renaming, or removing a field from a data schema shared between services or stored durably.
- Use this when choosing between JSON, Protocol Buffers, Thrift, or Avro for an internal microservice API.
- Use this when a service must read data written by a previous version of itself (e.g. reading old records from a database or message queue).
- Use this when a client application (mobile or desktop) may be running an older version than the server and must not crash on unknown fields.
- Use this when encoding data that crosses organizational boundaries and must remain interoperable across different language ecosystems.
- Use this when evaluating the security risk of deserializing data from an untrusted source using a language-native serialization library.
- Use this when a message queue or event log stores encoded messages that downstream consumers at different versions must be able to decode.

## Concrete Examples

- Twitter tweet IDs exceed 2^53 and cannot be exactly represented as JSON numbers in JavaScript, so Twitter's API returns each tweet ID twice: once as a JSON number and once as a decimal string.
- Java's built-in serialization (java.io.Serializable) is cited as notorious for bad performance and bloated encoding.
- Rolling upgrades: deploying a new server version to a few nodes at a time, requiring old and new code to coexist and handle each other's data formats.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 4: Encoding and Evolution**

An LLM coding agent is especially prone to generating language-native serialization (pickle, Java Serializable) as the path of least resistance when asked to 'save' or 'transmit' data, inadvertently creating security vulnerabilities and versioning dead-ends without flagging the tradeoffs. When generating data models or API schemas, an agent may not spontaneously add required/optional field annotations or tag numbers needed for safe evolution, because it lacks awareness of the multi-version deployment context unless explicitly prompted. This chapter's framework should be invoked by an agent whenever it generates any serialization, storage, or inter-service communication code, forcing it to explicitly reason about backward and forward compatibility before committing to a format.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Schema Evolution Compatibility Matrix: The set of rules governing which field additions, removals, and type changes are safe under each encoding format (Thrift, Protocol Buffers, Avro), determining what constitutes a backward- or forward-compatible schema change

---
title: Schema Evolution Compatibility Matrix: The set of rules governing which field additions, removals, and type changes are safe under each encoding format (Thrift, Protocol Buffers, Avro), determining what constitutes a backward- or forward-compatible schema change
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-4-Encoding-and-Evolution.json]
contributing_chapters: ["Chapter 4: Encoding and Evolution"]
confidence: high
---


> From chapter: *Chapter 4: Encoding and Evolution*

## Core Principle

Data formats must support backward and forward compatibility because old and new code versions inevitably coexist during rolling upgrades and client deployments. Language-specific serialization formats are dangerous and non-evolvable; schema-driven binary formats (Thrift, Protocol Buffers, Avro) provide the strongest compatibility guarantees by encoding only field tags or resolving schemas at read time. The chapter establishes that encoding format choice is an architectural decision with long-term consequences for system evolvability, security, and operational simplicity.

## Key Heuristics

These are the load-bearing rules for this concept.

> Backward compatibility is normally not hard to achieve: as author of the newer code, you know the format of data written by older code, and so you can explicitly handle it. Forward compatibility can be trickier, because it requires older code to ignore additions made by a newer version of the code.

> For data that is used only internally within your organization, there is less pressure to use a lowest-common-denominator encoding format.

> It's generally a bad idea to use your language's built-in encoding for anything other than very transient purposes.

> The difficulty of getting different organizations to agree on anything outweighs most other concerns.

> With a bit of care, backward/forward compatibility and rolling upgrades are quite achievable.

> Once you get into the terabytes, the choice of data format can have a big impact.

> Since they don't prescribe a schema, they need to include all object field names within the encoded data.

## Anti-Patterns & Fixes

- Language-Specific Serialization (e.g. Java Serializable, Python pickle): Ties data to one language, creates security vulnerabilities via arbitrary class instantiation, and neglects versioning and efficiency. Fix: Use language-agnostic formats like Protocol Buffers, Thrift, Avro, or JSON with explicit schemas.
- Using JSON/XML Numbers for Large Integers: Integers greater than 2^53 cannot be exactly represented in IEEE 754 double-precision float, causing silent data corruption in JavaScript consumers. Fix: Transmit large integers as decimal strings (as Twitter does with tweet IDs) or use a binary format with explicit integer types.
- Skipping Schemas for JSON/XML: Without schemas, correct interpretation of numbers, binary strings, and field types requires ad-hoc application code, making evolution error-prone. Fix: Use JSON Schema or XML Schema to enforce and document structure, or switch to a schema-driven binary format.
- Encoding Binary Data as Raw Bytes in JSON/XML: JSON and XML do not support binary strings natively. Fix: Encode binary data as Base64 text and annotate the schema to indicate the encoding, or use a binary format that natively supports byte sequences.
- Assuming Instantaneous Code Deployment: Treating schema changes as atomic across all nodes ignores the reality that old and new code versions coexist during rollouts. Fix: Design all schema changes to be simultaneously backward- and forward-compatible before deploying any code that depends on them.

## When To Apply

Load this page when:

- Use this when designing a data serialization format for a service that will undergo rolling deployments where multiple code versions run simultaneously.
- Use this when adding, renaming, or removing a field from a data schema shared between services or stored durably.
- Use this when choosing between JSON, Protocol Buffers, Thrift, or Avro for an internal microservice API.
- Use this when a service must read data written by a previous version of itself (e.g. reading old records from a database or message queue).
- Use this when a client application (mobile or desktop) may be running an older version than the server and must not crash on unknown fields.
- Use this when encoding data that crosses organizational boundaries and must remain interoperable across different language ecosystems.
- Use this when evaluating the security risk of deserializing data from an untrusted source using a language-native serialization library.
- Use this when a message queue or event log stores encoded messages that downstream consumers at different versions must be able to decode.

## Concrete Examples

- Twitter tweet IDs exceed 2^53 and cannot be exactly represented as JSON numbers in JavaScript, so Twitter's API returns each tweet ID twice: once as a JSON number and once as a decimal string.
- Java's built-in serialization (java.io.Serializable) is cited as notorious for bad performance and bloated encoding.
- Rolling upgrades: deploying a new server version to a few nodes at a time, requiring old and new code to coexist and handle each other's data formats.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 4: Encoding and Evolution**

An LLM coding agent is especially prone to generating language-native serialization (pickle, Java Serializable) as the path of least resistance when asked to 'save' or 'transmit' data, inadvertently creating security vulnerabilities and versioning dead-ends without flagging the tradeoffs. When generating data models or API schemas, an agent may not spontaneously add required/optional field annotations or tag numbers needed for safe evolution, because it lacks awareness of the multi-version deployment context unless explicitly prompted. This chapter's framework should be invoked by an agent whenever it generates any serialization, storage, or inter-service communication code, forcing it to explicitly reason about backward and forward compatibility before committing to a format.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Schema Evolution and Encoding Compatibility: The framework for evaluating data serialization formats by how well they handle changing application requirements over time

---
title: Schema Evolution and Encoding Compatibility: The framework for evaluating data serialization formats by how well they handle changing application requirements over time
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Part-I-Foundations-of-Data-Systems.json]
contributing_chapters: ["Part I: Foundations of Data Systems"]
confidence: high
---


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