---
name: distributed-systems
description: "Use when designing, implementing, or debugging distributed services — architecture choices, consistency trade-offs, fault tolerance, coordination, naming, and security for multi-node systems."
version: 1.0.0
author: Ayush Singh
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [distributed-systems, consistency, fault-tolerance, coordination, replication, networking, security]
    related_skills: [data-systems-engineering, modular-architecture, swe-foundations]
---

# Distributed Systems

## When to Load

- Use this when designing a service that must span multiple machines and needs clear system-boundary definitions
- Use this when an agent generates inter-service calls without timeout, retry, or failure-handling logic
- Use this when choosing between centralized, peer-to-peer, or hybrid architectures for a new system
- Use this when selecting a communication mechanism (RPC, message passing, event bus, resource URLs) between distributed components
- Use this when designing a distributed cache, data store, or replication scheme and choosing consistency vs. performance trade-offs
- Use this when a distributed system must tolerate node failures and you need to choose the right fault-tolerance mechanism
- Use this when designing node membership, service discovery, or naming so services remain reachable after IP/host changes
- Use this when implementing distributed coordination — distributed locks, leader election, event ordering, or logical clocks
- Use this when adding security to inter-service communication (authentication, authorization, key distribution, sandboxing)
- Use this when debugging ordering anomalies, stale reads, or split-brain behavior in distributed services

## Core Rules

> A distributed system is a collection of autonomous computing elements that appears to its users as a single coherent system — maintaining that illusion is the core engineering challenge.

> There is no global clock. Never assume synchronized time across nodes for ordering events. Use Lamport clocks or vector timestamps to establish causal ordering instead.

> Distribution transparency has a performance price and can never be fully achieved. Explicitly decide which transparency properties (location, replication, failure) you are willing to expose to users versus hide.

> Redundancy is the only path to fault tolerance. A system that cannot continue when a node fails is not fault-tolerant — it is merely resilient to luck.

> Replacing a component can only be done safely if its interfaces remain untouched. Design components with well-defined required and provided interfaces from the start.

> An identifier is not an address. Use location-independent identifiers for entities; never hardcode IPs or hostnames as stable keys. Names that embed location break when things move.

> Weaker consistency is cheaper to implement. Sequential consistency is elegant but expensive. Choose the weakest model that still satisfies your correctness requirements (monotonic reads, writes-follow-reads, eventual).

> Security must be pervasive, not additive. A single design flaw can render all other security measures useless. Define a security policy before building mechanisms — mechanisms without policy cannot be audited.

> Coordination encapsulates synchronization. Mutual exclusion and leader election in distributed systems are always more expensive and more failure-prone than in single-node systems.

> By using 2k+1 servers, Paxos achieves k-fault tolerance. Handle arbitrary (Byzantine) failures requires 3k+1 servers. Know which failure model you are designing for before choosing a consensus algorithm.

> Epidemic (gossip) protocols are simple, robust, and highly scalable. When you need information dissemination, aggregation, or peer sampling at scale without central coordination, gossip is frequently the best tool.

> Access control always follows authentication. Never authorize before identity is verified. Use session keys bootstrapped by public-key cryptography; avoid long-lived shared symmetric keys.

## Concept Map

For deeper context, load these wiki pages:

- output/wiki/distributed-systems/concepts/Distributed-System-Fundamentals.md — autonomy, coherence, open vs closed groups
- output/wiki/distributed-systems/concepts/Distribution-Transparency.md — access/location/replication/failure transparency, cost model
- output/wiki/distributed-systems/concepts/Scalability.md — size/geographical/administrative scalability, scaling techniques
- output/wiki/distributed-systems/concepts/System-Architecture-Styles.md — layered, object-based, resource-centered, event-based, client-server
- output/wiki/distributed-systems/concepts/Overlay-Networks-and-Peer-to-Peer.md — structured/unstructured overlays, DHTs, Chord, CAN
- output/wiki/distributed-systems/concepts/Middleware.md — distribution transparency layer, wrappers, interceptors, adaptive middleware
- output/wiki/distributed-systems/concepts/Processes-and-Threads.md — process vs thread granularity, concurrency transparency, thread models
- output/wiki/distributed-systems/concepts/Virtualization.md — VMs for portability and isolation, containers vs full VMs
- output/wiki/distributed-systems/concepts/Code-Migration.md — weak vs strong mobility, sender vs receiver-initiated migration
- output/wiki/distributed-systems/concepts/Client-Side-Distribution-Transparency.md — client-side stubs, distribution hiding, thin vs fat clients
- output/wiki/distributed-systems/concepts/Communication-Models.md — OSI model, RPC, MOM/message queues, persistent vs transient, sync vs async
- output/wiki/distributed-systems/concepts/Gossip-Protocols.md — epidemic spreading, anti-entropy, rumor spreading, aggregation
- output/wiki/distributed-systems/concepts/Naming-and-Location-Services.md — flat/structured/attribute naming, DNS-like hierarchies, forwarding pointers, DHT-based location
- output/wiki/distributed-systems/concepts/Coordination-and-Clocks.md — clock sync (NTP/Berkeley), Lamport timestamps, vector clocks, distributed mutex, election algorithms (bully/ring)
- output/wiki/distributed-systems/concepts/Consistency-Models.md — sequential/causal/entry consistency, client-centric models (monotonic read/write, read-your-writes)
- output/wiki/distributed-systems/concepts/Replication-Protocols.md — primary-based (remote-write/local-write), replicated-write (active replication, quorum)
- output/wiki/distributed-systems/concepts/Fault-Tolerance.md — dependability (availability/reliability/safety/maintainability), failure taxonomy, process groups, Paxos, virtual synchrony, checkpointing
- output/wiki/distributed-systems/concepts/Security-in-Distributed-Systems.md — four threat categories, policy-mechanism separation, secure channels, ACLs vs capabilities, key management, sandboxing

## Common Pitfalls

- Assuming zero latency: Fix — treat every remote call as potentially slow; design with timeouts, retries, and circuit breakers from day one.
- Assuming a reliable network: Fix — build retry logic, idempotent operations, and explicit delivery guarantees (at-most-once vs at-least-once vs exactly-once).
- Using wall-clock time for distributed event ordering: Fix — use Lamport logical clocks or vector timestamps; wall clocks can drift by tens of milliseconds.
- Designing security as a bolt-on layer: Fix — define a security policy (what is allowed, by whom, to what) before selecting any security mechanism.
- Choosing strong consistency everywhere: Fix — audit each data path for the weakest acceptable consistency model; pay the synchronization cost only where correctness demands it.
- Using long-lived shared symmetric keys: Fix — bootstrap session keys with public-key cryptography; rotate regularly; revoke compromised keys via certificate mechanisms.
- Assuming nodes have a fixed address: Fix — use location-independent identifiers; build a naming layer that resolves identifiers to current addresses dynamically.
- Treating Byzantine failures like crash-stop failures: Fix — the fault-tolerance mechanism changes: crash-stop needs 2k+1 servers; Byzantine needs 3k+1 with a different consensus protocol.

## AI-Native Application

LLM coding agents reliably fail on distributed systems work in three specific ways:

1. False network assumptions — generated code defaults to treating network calls as local function calls: no timeouts, no retries, no partial-failure handling. Agents should audit every generated remote call against the eight fallacies of distributed computing before finalizing code.

2. Consistency model blindness — agents default to "strong consistency" without analyzing cost. When generating caching, replication, or coordination logic, agents must explicitly state the consistency model chosen and justify it against the performance and availability requirements.

3. Security mechanism without security policy — agents generate encryption, token checks, and ACLs without first specifying what the policy is (who can do what to whom). Mechanisms without auditable policy are unverifiable. Agents must define the security policy as a structured artifact before generating any security-related code.

## Verification Checklist

- [ ] Every inter-service call has explicit timeout + retry strategy
- [ ] Event ordering requirements resolved to clock model (wall / Lamport / vector)
- [ ] Consistency model named and justified for each replicated data path
- [ ] Failure model stated (crash-stop vs Byzantine) before choosing consensus algorithm
- [ ] All entity references use location-independent identifiers, not IPs/hostnames
- [ ] Security policy document exists before any security mechanism is implemented
- [ ] Authentication happens before authorization — never reversed
- [ ] Fault-tolerance degree (k failures tolerated) is stated, and replica count matches (2k+1 or 3k+1)
