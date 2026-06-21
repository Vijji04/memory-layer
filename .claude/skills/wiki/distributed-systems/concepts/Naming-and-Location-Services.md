---
title: Naming and Location Services
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, distributed-systems, concept]
confidence: high
consolidated_from: 6 pages
---

# Naming and Location Services

> Consolidated from 6 related concept pages.

---

## Attribute Based Naming Entities are described and queried by attribute value pai

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Flat Naming Entities are identified by opaque unstructured identifiers with no i

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Forwarding Pointer Chains When an entity moves it leaves a pointer at its old lo

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Hierarchical Location Service Network divided into nested non overlapping domain

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Name Identifier Address Trichotomy Three distinct abstraction levels human frien

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Structured Naming Name Space Naming Graph Entities are organized in a directed a

## Core Principle

Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them produces brittle systems that break on any infrastructure change. It surveys five mechanisms for resolving flat (opaque) identifiers to addresses (broadcast, forwarding pointers, home agents, DHTs, hierarchical search trees) and explains how structured naming graphs enable scalable, human-readable resolution via path traversal across distributed name servers. Attribute-based naming, while the most expressive, is the hardest to scale and requires DHT-backed distribution of descriptors to avoid centralized bottlenecks.

## Key Heuristics

These are the load-bearing rules for this concept.

> A name for an entity that is independent from its addresses is often much easier and more flexible to use. Such a name is called location independent.

> An identifier refers to at most one entity; each entity is referred to by at most one identifier; an identifier always refers to the same entity (i.e., it is never reused).

> An address is thus just a special kind of name: it refers to an access point of an entity.

> To check if two processes are referring to the same entity, it is sufficient to test if the two identifiers are equal.

> To avoid large chains of pointers, it is important to reduce chains periodically.

> This type of name resolution [attribute-based] is notoriously difficult, especially in combination with searching.

> How this distribution [of the naming system] is done plays a key role in the efficiency and scalability of the naming system.

## Anti-Patterns & Fixes

- Using Addresses as Names: Binding a service's identity to its IP address or port means any infrastructure move invalidates all references. Fix: Assign a stable, location-independent name and resolve it to the current address at runtime via a naming service.
- Reusing Identifiers: Reassigning an old identifier to a new entity breaks any cached reference and violates the uniqueness invariant. Fix: Treat identifiers as permanently retired once an entity is decommissioned; never recycle them.
- Unbounded Forwarding Pointer Chains: Each entity migration appends a hop, making resolution O(n) and fragile to intermediate failures. Fix: Periodically collapse chains by updating all pointers to point directly to the current location.
- Centralized Attribute Store: Storing all (attribute, value) descriptors in a single database enables exhaustive search but creates a scalability bottleneck and single point of failure. Fix: Map attribute-value pairs onto a DHT using space-filling curves to distribute load across nodes.
- Encoding Location in Structure: Structuring a name so that it encodes a specific server's physical location couples the name to infrastructure. Fix: Use logical path names in a naming graph where resolution is indirected through name servers that can be updated independently.

## When To Apply

Load this page when:

- Use this when designing a microservice registry where services must be discoverable after IP or host changes without updating all consumers.
- Use this when generating code that stores or compares resource references — ensure you distinguish opaque unique IDs from mutable addresses.
- Use this when implementing a distributed cache or DHT key scheme that must route lookups to the correct responsible node for a given identifier.
- Use this when a mobile or ephemeral resource (container, lambda, edge node) needs to remain reachable despite frequent address changes.
- Use this when building a search or discovery feature that queries entities by properties rather than by known name, requiring attribute-based resolution.
- Use this when scaffolding a hierarchical namespace (e.g., DNS-like zones, file system mounts, Kubernetes namespaces) and deciding how to distribute resolution authority across servers.
- Use this when auditing legacy code that uses raw IP addresses or hostnames as stable keys in configuration, databases, or inter-service calls.
- Use this when designing object migration in a distributed system and needing to decide between forwarding pointers, home-agent redirection, or DHT re-keying.

## Concrete Examples

- Telephone number as an address: a phone is an access point of a person; the number is the address; people have multiple numbers, and numbers change when moving cities or changing providers.
- Web service distributed across multiple servers: using any single server's IP as the service name is ambiguous and fragile; a single location-independent name (URL) resolves to whichever server is appropriate.
- Mobile computer assigned a new IP address after moving to a different network location, illustrating how access points (addresses) are mutable while the entity identity should remain stable.
- DNS as a structured naming system: a naming graph with labeled edges, path-name resolution traversing distributed name servers, and systematic delegation to the server responsible for each zone.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Naming**

An LLM coding agent is prone to hardcoding addresses or connection strings directly into generated code (conflating address with identity), which breaks the moment infrastructure changes — a failure a human developer would catch through operational experience. Agents also tend to reuse or sequentially increment identifiers when generating mock data or test fixtures, inadvertently violating the non-reuse invariant and causing ghost references in tests. Applying the Name-Identifier-Address Trichotomy as an explicit generation constraint forces the agent to emit indirection layers (service locators, environment-variable references, registry lookups) rather than baking in brittle location-specific values.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
