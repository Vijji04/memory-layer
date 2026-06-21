---
title: Distributed Systems — Overview
created: 2026-05-12
updated: 2026-05-12
type: overview
tags: [phase-2, distributed-systems]
---

# Distributed Systems

> Phase 2 knowledge domain. 53 concept pages.

## What This Wiki Covers

This wiki encodes the core frameworks, heuristics, and agent-applicable patterns
from deep study of the Phase 2 curriculum: **Distributed Systems**.

It is not a book summary. It is a structured knowledge base — each page is a
named concept with full detail: principle, heuristics, anti-patterns, examples,
and AI-native application guidance.

## Core Themes

- **Introduction:** A distributed system is a collection of independent nodes that must collaborate — via message passing through a middleware layer — to present a coherent single-system illusion to users. Core design ch...

- **Architectures:** Chapter 2 establishes that distributed systems require deliberate architectural organization at two levels: the logical software architecture (how components and connectors are structured into styles ...

- **Processes:** Chapter 3 establishes that distributed system performance and flexibility hinge on choosing the right process granularity: threads outperform processes for fine-grained concurrency by minimizing conte...

- **Communication:** Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-serve...

- **Naming:** Chapter 5 establishes that distributed naming requires separating three distinct concepts — location-independent names, unique non-reusable identifiers, and mutable addresses — because conflating them...

## Concept Index (quick nav)

All concepts in this wiki:

- [[Access-Control-Duality-Two-implementation-strategies-Access-Control-Lists-resour]] — Access Control Duality: Two implementation strategies — Access Control Lists (resource-side, per-user rights) vs. Capability Certificates (process-side, portable rights tokens with delegation support)
- [[Attribute-Based-Naming-Entities-are-described-and-queried-by-attribute-value-pai]] — Attribute-Based Naming: Entities are described and queried by (attribute, value) pairs, enabling description-driven lookup at the cost of expensive exhaustive search
- [[Causal-Consistency-operations-that-are-potentially-causally-dependent-on-each-ot]] — Causal Consistency: operations that are potentially causally dependent on each other are carried out in the order of that dependency
- [[Checkpoint-plus-Message-Logging-Recovery-Combines-periodic-state-snapshots-with-]] — Checkpoint-plus-Message-Logging Recovery: Combines periodic state snapshots with communication logs to enable replay-based recovery after crashes
- [[Client-Centric-Consistency-Models-ensures-a-single-possibly-mobile-client-always]] — Client-Centric Consistency Models: ensures a single (possibly mobile) client always sees its own writes reflected when it connects to a new replica, without requiring global consistency
- [[Client-Server-Architecture-Machines-divided-into-clients-that-send-requests-and-]] — Client-Server Architecture: Machines divided into clients that send requests and servers that process and return results, reflecting traditional modular software decomposition placed on different physical machines
- [[Client-Server-Distribution-Transparency-Framework-Clients-hide-communication-det]] — Client-Server Distribution Transparency Framework: Clients hide communication details, server location, replication, and failure recovery from users; servers handle iterative vs concurrent, stateless vs stateful, and single-entry-point cluster organization
- [[Clock-Synchronization-All-distributed-clock-sync-methods-exchange-clock-values-w]] — Clock Synchronization: All distributed clock sync methods exchange clock values while accounting for message transmission delays; accuracy is determined by how communication delay variations are handled
- [[Code-Migration-Model-Moving-computations-to-data-ship-code-to-client-reduces-com]] — Code Migration Model: Moving computations to data (ship code to client) reduces communication cost; two drivers are performance (reduce remote calls) and flexibility (dynamic client configuration without preinstallation)
- [[Concurrency-Transparency-Cost-Model-OS-enforced-process-isolation-address-space-]] — Concurrency Transparency Cost Model: OS-enforced process isolation (address space creation, MMU updates, TLB invalidation, potential disk swap) is the price of concurrency transparency; threads forego this transparency to avoid that cost
- [[Data-Centric-Consistency-Models-defines-consistency-guarantees-in-terms-of-what-]] — Data-Centric Consistency Models: defines consistency guarantees in terms of what all processes can observe when concurrently reading and writing shared data (e.g., sequential consistency, causal consistency)
- [[Dependability-Framework-Four-property-model-Availability-Reliability-Safety-Main]] — Dependability Framework: Four-property model (Availability, Reliability, Safety, Maintainability) for characterizing fault-tolerant distributed systems
- [[Distributed-Mutual-Exclusion-Algorithms-ensuring-at-most-one-process-at-a-time-a]] — Distributed Mutual Exclusion: Algorithms ensuring at most one process at a time accesses a shared resource, implementable via a central coordinator or fully distributed protocols
- [[Distributed-System-Definition-A-collection-of-autonomous-computing-elements-that]] — Distributed System Definition: A collection of autonomous computing elements that appears to its users as a single coherent system — combining node independence with perceived coherence
- [[Distribution-Transparency-Model-A-design-goal-to-hide-the-complexities-of-distri]] — Distribution Transparency Model: A design goal to hide the complexities of distribution (location, replication, failure, migration) from users and applications, with explicit acknowledgment that full transparency is unachievable
- [[Election-Algorithms-Protocols-by-which-a-group-of-distributed-processes-collecti]] — Election Algorithms: Protocols by which a group of distributed processes collectively designate one process as coordinator, especially when the current coordinator may crash
- [[Epidemic-Gossip-Protocols-Probabilistic-dissemination-protocols-inspired-by-dise]] — Epidemic (Gossip) Protocols: Probabilistic dissemination protocols inspired by disease spread, used for robust decentralized information propagation and aggregation across large distributed systems
- [[Event-Based-Architecture-Components-interact-by-publishing-and-subscribing-to-ev]] — Event-Based Architecture: Components interact by publishing and subscribing to events, enabling loose coupling and asynchronous coordination
- [[Failure-Taxonomy-Hierarchical-classification-of-faultserrorsfailures-with-five-p]] — Failure Taxonomy: Hierarchical classification of faults→errors→failures with five process-level failure types: crash, omission, timing, response, and Byzantine/arbitrary
- [[Flat-Naming-Entities-are-identified-by-opaque-unstructured-identifiers-with-no-i]] — Flat Naming: Entities are identified by opaque, unstructured identifiers with no inherent meaning; location requires external mechanisms like forwarding pointers, DHTs, or hierarchical search trees
- [[Forwarding-Pointer-Chains-When-an-entity-moves-it-leaves-a-pointer-at-its-old-lo]] — Forwarding Pointer Chains: When an entity moves, it leaves a pointer at its old location; resolution traverses the chain; chains must be periodically shortened to avoid degradation
- [[Four-Security-Threats-Model-Classifies-all-threats-as-Interception-Interruption-]] — Four Security Threats Model: Classifies all threats as Interception, Interruption, Modification, or Fabrication — covering unauthorized access, service disruption, data tampering, and data/activity generation respectively
- [[Gossip-Based-Coordination-Peer-sampling-aggregation-and-overlay-construction-ach]] — Gossip-Based Coordination: Peer-sampling, aggregation, and overlay construction achieved by regularly and randomly refreshing partial views of the network through gossip protocols
- [[Hierarchical-Location-Service-Network-divided-into-nested-non-overlapping-domain]] — Hierarchical Location Service: Network divided into nested non-overlapping domains, each with a directory node; upper-level nodes hold pointers to sub-domains containing the entity, top-level node knows all entities
- [[Lamport-Logical-Clocks-Each-event-e-is-assigned-a-globally-unique-logical-timest]] — Lamport Logical Clocks: Each event e is assigned a globally unique logical timestamp C(e) such that if event a happened before b, then C(a) < C(b), enabling global ordering without wall-clock agreement
- [[Layered-Architecture-Components-organized-in-layers-where-downcalls-to-lower-lay]] — Layered Architecture: Components organized in layers where downcalls to lower layers are the norm and upcalls are exceptional, enabling separation of concerns and replaceability
- [[Message-Oriented-Middleware-MOM-A-high-level-message-queuing-model-supporting-pe]] — Message-Oriented Middleware (MOM): A high-level message-queuing model supporting persistent and asynchronous communication, decoupling sender and receiver availability, analogous to email delivery
- [[Middleware-Layer-Model-Application-independent-protocols-communication-transacti]] — Middleware Layer Model: Application-independent protocols (communication, transactions, service composition, reliability) placed logically between the OS and distributed applications to achieve coherent collective behavior
- [[Name-Identifier-Address-Trichotomy-Three-distinct-abstraction-levels-human-frien]] — Name-Identifier-Address Trichotomy: Three distinct abstraction levels — human-friendly names (location-independent), true identifiers (unique, permanent, non-reused), and addresses (access-point-specific, mutable)
- [[OSI-Reference-Model-A-seven-layer-abstraction-that-decomposes-network-communicat]] — OSI Reference Model: A seven-layer abstraction that decomposes network communication into independently solvable problems, each layer offering services to the layer above via a defined interface
- [[Object-Based-Architecture-Software-components-are-objects-with-encapsulated-stat]] — Object-Based Architecture: Software components are objects with encapsulated state and interfaces, interacting via method calls, enabling modular distributed systems
- [[Open-vs-Closed-Group-Model-A-framework-for-managing-node-membership-open-groups-]] — Open vs. Closed Group Model: A framework for managing node membership — open groups allow any node to join and message freely; closed groups require explicit admission control and authentication
- [[Overlay-Network-Organization-Nodes-are-organized-into-a-logical-topology-structu]] — Overlay Network Organization: Nodes are organized into a logical topology (structured or unstructured) layered on top of the physical network, determining who can directly communicate with whom
- [[Paxos-Consensus-Algorithm-A-fault-tolerant-consensus-protocol-requiring-2k1-serv]] — Paxos Consensus Algorithm: A fault-tolerant consensus protocol requiring 2k+1 servers for k crash-fault tolerance and 3k+1 servers for k Byzantine-fault tolerance
- [[Peer-to-Peer-Overlay-Network-All-nodes-play-equal-roles-in-a-logical-network-whe]] — Peer-to-Peer Overlay Network: All nodes play equal roles in a logical network where each process maintains a local list of peers; structured overlays use deterministic routing while unstructured overlays require search algorithms
- [[Persistent-vs-Transient-Communication-Taxonomy-A-classification-axis-where-persi]] — Persistent vs. Transient Communication Taxonomy: A classification axis where persistent communication stores messages until delivered regardless of receiver availability, while transient requires the receiver to be active at send time
- [[Policy-Mechanism-Separation-Security-policy-describes-what-is-allowedprohibited-]] — Policy-Mechanism Separation: Security policy describes what is allowed/prohibited; security mechanisms (encryption, authentication, authorization, auditing) enforce that policy — these must be designed independently
- [[Primary-Based-Protocols-all-update-operations-are-forwarded-to-a-primary-copy-th]] — Primary-Based Protocols: all update operations are forwarded to a primary copy that orders and propagates them, simplifying ordering at the cost of a single coordination point
- [[Process-Group-Resilience-Multiple-identical-processes-cooperate-to-appear-as-a-s]] — Process Group Resilience: Multiple identical processes cooperate to appear as a single logical process so that individual failures are invisible to clients
- [[Process-vs-Thread-Granularity-Model-Processes-provide-full-isolation-via-separat]] — Process vs Thread Granularity Model: Processes provide full isolation via separate address spaces but at high cost; threads share a process address space with minimal context (processor registers + thread management info), trading isolation for performance
- [[Remote-Procedure-Call-RPC-A-communication-abstraction-that-hides-message-passing]] — Remote Procedure Call (RPC): A communication abstraction that hides message-passing complexity by making remote service calls appear as local procedure calls via client-side stubs that marshal parameters and unmarshal results
- [[Replicated-Write-Protocols-updates-are-forwarded-to-several-replicas-simultaneou]] — Replicated-Write Protocols: updates are forwarded to several replicas simultaneously, making correct ordering harder but potentially improving throughput and availability
- [[Resource-Centered-Architecture-System-organized-around-named-resources-eg-RESTwe]] — Resource-Centered Architecture: System organized around named resources (e.g., REST/web), where components interact by operating on addressable resources
- [[Sandbox-and-Protection-Domain-Model-Mobile-code-access-control-via-sandboxes-res]] — Sandbox and Protection Domain Model: Mobile code access control via sandboxes (restrictive but widely applied) or flexible protection domains for finer-grained control
- [[Scalability-Dimensions-Framework-Distinguishes-size-scalability-geographical-sca]] — Scalability Dimensions Framework: Distinguishes size scalability, geographical scalability, and administrative scalability as separate, sometimes conflicting, design concerns
- [[Secure-Channel-Framework-A-channel-providing-mutual-authentication-message-integ]] — Secure Channel Framework: A channel providing mutual authentication, message integrity, and confidentiality between communicating parties in a distributed system
- [[Security-Management-Triad-Covers-key-management-authorization-management-attribu]] — Security Management Triad: Covers key management, authorization management (attribute certificates, delegation), and secure naming as the operational backbone of a secure distributed system
- [[Sequential-Consistency-all-write-operations-are-seen-by-everyone-in-the-same-ord]] — Sequential Consistency: all write operations are seen by everyone in the same order, providing the semantics programmers expect in concurrent programming
- [[Structured-Naming-Name-Space-Naming-Graph-Entities-are-organized-in-a-directed-a]] — Structured Naming (Name Space / Naming Graph): Entities are organized in a directed acyclic graph where edges carry human-readable labels and path traversal performs name resolution, as exemplified by DNS
- [[Synchronous-vs-Asynchronous-Communication-Taxonomy-A-classification-axis-disting]] — Synchronous vs. Asynchronous Communication Taxonomy: A classification axis distinguishing whether the sender blocks until receipt/delivery/response (synchronous) or continues immediately after submission (asynchronous)
- [[Vector-Timestamps-An-extension-of-Lamport-timestamps-where-Ca-Cb-implies-event-a]] — Vector Timestamps: An extension of Lamport timestamps where C(a) < C(b) implies event a causally preceded b, capturing causal relationships between events
- [[Virtual-Synchrony-Model-Execution-model-that-introduces-epoch-boundaries-within-]] — Virtual Synchrony Model: Execution model that introduces epoch boundaries within which group membership is stable and messages are reliably delivered; no message can cross a boundary
- [[Virtualization-as-Portability-and-Isolation-Layer-Virtual-machines-process-VMs-l]] — Virtualization as Portability and Isolation Layer: Virtual machines (process VMs like JVM, or VM monitors) decouple applications from hardware, enabling concurrent execution, failure isolation, and heterogeneity-agnostic code migration

## How to Use This Wiki

**For agents:** Load the thin skill file (`output/skills/`) first.
The skill's concept map tells you which page to read for a given situation.
Read the concept page when you need depth — not the whole wiki.

**For humans:** Browse in Obsidian. Start here, follow wikilinks.
Use the graph view to see which concepts are most connected.

## Related Wikis

<!-- Populated after all book wikis are built -->
