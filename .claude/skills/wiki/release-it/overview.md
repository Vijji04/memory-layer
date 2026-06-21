---
title: Production-Ready Systems — Overview
created: 2026-05-12
updated: 2026-05-12
type: overview
tags: [phase-1, release-it]
---

# Production-Ready Systems

> Phase 1 knowledge domain. 82 concept pages.

## What This Wiki Covers

This wiki encodes the core frameworks, heuristics, and agent-applicable patterns
from deep study of the Phase 1 curriculum: **Production-Ready Systems**.

It is not a book summary. It is a structured knowledge base — each page is a
named concept with full detail: principle, heuristics, anti-patterns, examples,
and AI-native application guidance.

## Core Themes

- **Chapter 1: Introduction:** Chapter 1 argues that software design is systematically incomplete because it targets QA correctness rather than production survivability, and that this gap has measurable multi-million-dollar financi...

- **Chapter 2: Case Study: The Exception That Grounded An Airline:** A single uncaught SQLException in a JDBC finally block — where stmt.close() threw during a post-failover socket error, preventing conn.close() from executing — leaked connections until the entire pool...

- **Chapter 3: Introducing Stability:** Chapter 3 establishes that production stability requires designing systems to expect and contain failures rather than prevent them, using the crack propagation metaphor to explain how small failures a...

- **Chapter 4: Stability Antipatterns:** Chapter 4 catalogs eleven stability antipatterns — recurring design and coding mistakes that create, accelerate, or multiply system failures — with integration points and unbounded result sets as the ...

- **Chapter 5: Stability Patterns:** Chapter 5 presents eight stability patterns — including Timeouts, Circuit Breaker, Test Harness, and Decoupling Middleware — as the constructive counterparts to the antipatterns in Chapter 4, each des...

## Concept Index (quick nav)

All concepts in this wiki:

- [[ActiveActive-vs-ActivePassive-Clustering-Activeactive-clusters-achieve-both-scal]] — Active/Active vs Active/Passive Clustering: Active/active clusters achieve both scalability and redundancy; active/passive clusters achieve only redundancy and are a Band-Aid for applications not designed for distributed operation
- [[Automated-Data-Collection-for-Post-Mortem-A-pattern-of-pre-scripted-non-intrusiv]] — Automated Data Collection for Post-Mortem: A pattern of pre-scripted, non-intrusive data capture (thread dumps, DB snapshots) that enables root cause analysis without prolonging the outage
- [[Bulkheads-A-stability-pattern-borrowed-from-ship-design-that-partitions-systems-]] — Bulkheads: A stability pattern borrowed from ship design that partitions systems to contain failures and prevent total loss
- [[CDN-as-Emergency-Traffic-Governor-Using-a-Content-Delivery-Network-not-just-for-]] — CDN as Emergency Traffic Governor: Using a Content Delivery Network not just for caching but as a real-time throttle, IP blocker, and static-content shield to absorb launch-day traffic surges without application-layer changes
- [[Cache-Sizing-and-Invalidation-Strategy-Bounding-cache-memory-monitoring-hit-rate]] — Cache Sizing and Invalidation Strategy: Bounding cache memory, monitoring hit rates, and choosing an invalidation mechanism (clock, calendar, event) appropriate to the scale of the deployment
- [[Capacity-Definition-Framework-Capacity-maximum-sustainable-throughput-for-a-give]] — Capacity Definition Framework: Capacity = maximum sustainable throughput for a given workload while maintaining acceptable per-transaction response time — a multi-variable measure, not a fixed number
- [[Cascade-Failure-Propagation-A-systems-model-describing-how-a-single-localized-bu]] — Cascade Failure Propagation: A systems model describing how a single localized bug can exhaust shared resources and propagate failure outward to all dependent systems
- [[Cascading-Capacity-Mismatch-Model-When-upstream-systems-have-orders-of-magnitude]] — Cascading Capacity Mismatch Model: When upstream systems have orders-of-magnitude more threads than downstream systems, a traffic surge causes a cascade collapse; capacity ratios must be modeled end-to-end
- [[Chain-of-Failure-Model-Outages-are-chains-of-dependent-events-where-failure-in-o]] — Chain of Failure Model: Outages are chains of dependent events where failure in one layer increases probability of failure in adjacent layers, making combined failure far more probable than independent probabilities suggest
- [[Circuit-Breaker-Pattern-Wrap-dangerous-remote-calls-in-a-stateful-component-that]] — Circuit Breaker Pattern: Wrap dangerous remote calls in a stateful component that trips 'open' after repeated failures, short-circuiting calls until the system recovers
- [[Circuit-Breaker-A-stability-pattern-that-trips-open-to-stop-cascading-failures-w]] — Circuit Breaker: A stability pattern that trips open to stop cascading failures when downstream calls fail, then resets after a timeout period
- [[Clean-Start-up-Sequence-A-pattern-requiring-applications-to-complete-all-initial]] — Clean Start-up Sequence: A pattern requiring applications to complete all initialization (connections, pools, dependencies) before accepting any work, analogous to a store opening only when all staff are ready
- [[Common-Dependency-Hypothesis-A-diagnostic-model-where-simultaneous-failures-acro]] — Common Dependency Hypothesis: A diagnostic model where simultaneous failures across multiple independent systems point to a shared upstream dependency as the root cause
- [[Configuration-Override-Layering-A-level-of-indirection-pattern-where-production-]] — Configuration Override Layering: A level-of-indirection pattern where production-specific properties are maintained in a separate override structure so each deployment does not overwrite environment-specific config, and each differing property exists in exactly one place
- [[Configuration-Separation-Model-A-design-principle-separating-production-tunable-]] — Configuration Separation Model: A design principle separating production-tunable properties from internal application wiring so administrators can never accidentally break object associations
- [[Connection-Pool-Management-Three-strategies-for-managing-database-connections-in]] — Connection Pool Management: Three strategies for managing database connections in web systems — per-page (one connection per full page request), per-fragment (each fragment manages its own connection), and hybrid (fragment-level connections bound to a page-level transaction)
- [[Connection-Pool-as-Throttle-A-dedicated-resource-pool-for-a-downstream-dependenc]] — Connection Pool as Throttle: A dedicated resource pool for a downstream dependency acts as a tunable choke point — setting its max to zero effectively disables that integration path without a full redeploy
- [[Conways-Law-Organizations-which-design-systems-are-constrained-to-produce-design]] — Conway's Law: Organizations which design systems are constrained to produce designs whose structure are copies of the communication structures of those organizations — used both prescriptively (shape comms to shape software) and descriptively (map software to understand real org structure)
- [[Cookie-as-State-Mechanism-cookies-were-designed-for-small-identifiers-100-bytes-]] — Cookie as State Mechanism: cookies were designed for small identifiers (<100 bytes) for session management, not for storing serialized objects or persistent data
- [[Cost-vs-Avoided-Loss-Framework-Frame-availability-decisions-in-financial-terms-c]] — Cost-vs-Avoided-Loss Framework: Frame availability decisions in financial terms — compare the lifecycle cost of each additional '9' of availability against the monthly revenue loss avoided by the reduced downtime
- [[CostCost-Availability-Trade-off-Frame-availability-requirements-as-a-costbenefit]] — Cost/Cost Availability Trade-off: Frame availability requirements as a cost/benefit (really cost/cost) negotiation with sponsors, recognizing that availability cost increases radically at each level
- [[Crack-Propagation-Model-Failures-start-as-small-cracks-at-one-component-and-prop]] — Crack Propagation Model: Failures start as small cracks at one component and propagate through tightly coupled systems; stability design is about stopping crack propagation, not preventing the initial crack
- [[Crumple-Zone-Crackstoppers-Pattern-Deliberately-design-certain-components-to-fai]] — Crumple Zone / Crackstoppers Pattern: Deliberately design certain components to fail first in order to protect indispensable features, analogous to automotive crumple zones absorbing crash energy away from passengers
- [[Cynical-Requirements-Examination-the-practice-of-viewing-system-requirements-and]] — Cynical Requirements Examination: the practice of viewing system requirements and dependencies with deliberate suspicion to surface hidden failure modes
- [[Cynical-Software-Model-Enterprise-software-must-expect-bad-things-to-happen-neve]] — Cynical Software Model: Enterprise software must expect bad things to happen, never be surprised by failure, and put up internal barriers to protect itself from both external and internal failures
- [[Decoupling-Middleware-Pattern-Choose-message-oriented-or-asynchronous-middleware]] — Decoupling Middleware Pattern: Choose message-oriented or asynchronous middleware to remove temporal and spatial coupling between systems, preventing cascading failures
- [[Design-for-Production-Engineering-software-systems-with-operational-lifecycle-co]] — Design for Production: Engineering software systems with operational lifecycle costs, uptime, and real-world stresses as primary constraints, not just functional correctness or QA passage
- [[DrivingFollowing-Variables-Model-Capacity-is-analyzed-by-identifying-external-dr]] — Driving/Following Variables Model: Capacity is analyzed by identifying external driving variables (e.g., requests/second) and the internal following variables (CPU, RAM, I/O) that respond to them, tracing causal chains across layers
- [[Dynamic-Reconfiguration-over-Full-Restart-Changing-component-level-config-and-re]] — Dynamic Reconfiguration over Full Restart: Changing component-level config and restarting only that component (stopService/startService) is far faster than restarting entire servers under load
- [[Early-Decision-Crystallization-The-principle-that-the-earliest-architectural-dec]] — Early Decision Crystallization: The principle that the earliest architectural decisions (system boundaries, decomposition) become locked into team structure and funding, making them the hardest to reverse despite being made with the least information
- [[Environmental-Awareness-Model-The-principle-that-systems-must-artificially-radia]] — Environmental Awareness Model: The principle that systems must artificially radiate information (like a ship's diesel engine does naturally) because software runs in faceless boxes with no ambient signals — transparency must be deliberately built in
- [[Fail-Fast-Pattern-Validate-preconditions-at-the-entry-point-of-a-request-and-ret]] — Fail Fast Pattern: Validate preconditions at the entry point of a request and return an immediate error rather than accepting work you cannot complete
- [[Feature-Level-Availability-Definition-Define-availability-requirements-per-featu]] — Feature-Level Availability Definition: Define availability requirements per feature or function rather than for the system as a whole, with explicit exclusions for external system failures
- [[Feature-Level-SLA-Definition-Define-availability-SLAs-per-discrete-business-feat]] — Feature-Level SLA Definition: Define availability SLAs per discrete business feature or function rather than for 'the system' as a whole, because different features have different revenue impact and different external dependency chains
- [[Four-Perspectives-of-Transparency-A-framework-dividing-system-observability-into]] — Four Perspectives of Transparency: A framework dividing system observability into historical trending, predictive forecasting, present status, and instantaneous behavior — each serving different constituencies with different tools and urgency levels
- [[Garbage-Collector-Generational-Model-Understanding-eden-survivor-and-tenured-gen]] — Garbage Collector Generational Model: Understanding eden, survivor, and tenured generations in the JVM GC to tune heap ratios and avoid GC-induced slowdowns
- [[Highly-Interactive-Complexity-A-system-condition-where-enough-moving-parts-and-h]] — Highly Interactive Complexity: A system condition where enough moving parts and hidden internal dependencies exist that operators' mental models are incomplete or wrong, causing well-intentioned actions to trigger unexpected harmful linkages
- [[Horizontal-vs-Vertical-Scalability-Model-Systems-scale-either-by-adding-homogene]] — Horizontal vs. Vertical Scalability Model: Systems scale either by adding homogeneous servers behind a load balancer (horizontal/shared-nothing) or by upgrading existing servers (vertical), with different cost and ceiling implications
- [[Impulse-vs-Stress-Framework-Impulses-are-rapid-shocks-flash-traffic-bulk-queue-d]] — Impulse vs. Stress Framework: Impulses are rapid shocks (flash traffic, bulk queue dumps) while stresses are sustained forces (slow upstream dependency); each requires different defensive design
- [[Integration-Points-as-Stability-Risk-Every-socket-pipe-process-or-remote-call-is]] — Integration Points as Stability Risk: Every socket, pipe, process, or remote call is a potential hang or crash vector; the number of integration points is proportional to systemic fragility
- [[Ivory-Tower-Architecture-The-anti-model-where-architects-issue-top-down-decrees-]] — Ivory Tower Architecture: The anti-model where architects issue top-down decrees disconnected from implementation realities, optimizing for abstract perfection over operational survivability
- [[Load-Balancing-Taxonomy-A-hierarchy-of-load-balancing-approaches-DNS-round-robin]] — Load Balancing Taxonomy: A hierarchy of load balancing approaches (DNS round-robin → reverse proxy → hardware load balancer) each operating at different OSI layers with increasing control, health-awareness, and cost
- [[Multihomed-Server-Architecture-A-server-with-multiple-IP-addresses-on-separate-n]] — Multihomed Server Architecture: A server with multiple IP addresses on separate networks for production, backup, admin, and other traffic, each with distinct security and performance requirements
- [[Multiplier-Effect-Leverage-Identifying-where-costs-are-borne-N-times-vs-where-be]] — Multiplier Effect Leverage: Identifying where costs are borne N times vs. where benefits are gained once, to find architectural leverage points worth optimizing
- [[Multiplier-Effect-per-connection-or-per-request-costs-that-seem-trivial-become-c]] — Multiplier Effect: per-connection or per-request costs that seem trivial become critical capacity killers when multiplied across concurrent users, server instances, and request frequency
- [[Network-Traffic-Segmentation-The-design-principle-of-partitioning-backup-admin-a]] — Network Traffic Segmentation: The design principle of partitioning backup, admin, and production traffic onto separate network interfaces or VLANs to isolate security domains and prevent congestion
- [[Obvious-Configuration-Principle-Separate-essential-plumbing-configuration-from-e]] — Obvious Configuration Principle: Separate essential plumbing configuration from environment-specific configuration to minimize operator error
- [[OpsDB-Pattern-A-dedicated-operational-database-that-stores-both-system-metrics-a]] — OpsDB Pattern: A dedicated operational database that stores both system metrics and business metrics over time, enabling correlation, anomaly investigation, and capacity forecasting without hitting production transactional databases
- [[Password-Vaulting-Storing-credentials-in-encrypted-files-to-reduce-the-security-]] — Password Vaulting: Storing credentials in encrypted files to reduce the security surface to a single encryption key rather than multiple plaintext files
- [[Per-Application-User-Isolation-Each-major-application-runs-under-its-own-OS-user]] — Per-Application User Isolation: Each major application runs under its own OS user account so that a compromise of one application cannot directly access another's resources
- [[Pragmatic-Architecture-A-style-of-architecture-where-the-architect-works-alongsi]] — Pragmatic Architecture: A style of architecture where the architect works alongside coders, prioritizes operational dynamics over abstract elegance, and knows which components need replacement as stress factors change
- [[Precompute-vs-Dynamic-Decision-Model-A-framework-for-deciding-when-to-precompute]] — Precompute-vs-Dynamic Decision Model: A framework for deciding when to precompute and cache content vs. generate it dynamically, based on change frequency vs. access frequency
- [[Principle-of-Least-Privilege-A-process-should-have-the-lowest-level-of-privilege]] — Principle of Least Privilege: A process should have the lowest level of privilege needed to accomplish its task — never root or Administrator for application software
- [[Privilege-Separation-A-technique-where-a-process-deliberately-downgrades-its-own]] — Privilege Separation: A technique where a process deliberately downgrades its own permissions after completing tasks that require elevated access, making the downgrade a one-way trip
- [[Pulse-Monitoring-Vital-Signs-Sampling-Continuously-sample-key-system-metrics-lat]] — Pulse Monitoring / Vital Signs Sampling: Continuously sample key system metrics (latency, thread counts, session counts, order rates) so operators internalize 'normal' and can smell anomalies instantly
- [[QA-Production-Topology-Matching-A-framework-for-identifying-and-closing-gaps-bet]] — QA-Production Topology Matching: A framework for identifying and closing gaps between QA and production environments, focusing on topology (number and connectivity of nodes) rather than just configuration file differences
- [[QA-vs-Production-Topology-Gap-The-structural-divergence-between-test-environment]] — QA-vs-Production Topology Gap: The structural divergence between test environments and production environments (different firewalls, instance counts, hostnames) that causes systems built to pass QA to fail in production
- [[Queue-and-Retry-Model-Instead-of-immediate-retry-on-timeout-queue-the-failed-ope]] — Queue-and-Retry Model: Instead of immediate retry on timeout, queue the failed operation for delayed retry to avoid compounding user wait time and hitting the same failure again
- [[Recovery-Oriented-Computing-ROC-Accept-that-failures-are-inevitable-focus-on-dam]] — Recovery-Oriented Computing (ROC): Accept that failures are inevitable; focus on damage containment, automatic fault detection, and component-level restartability rather than eliminating all failure sources
- [[Resource-Pool-Contention-Model-throughput-collapses-exponentially-once-thread-co]] — Resource Pool Contention Model: throughput collapses exponentially once thread count exceeds pool size, creating a 'knee' curve where additional threads add zero value
- [[Restore-First-Incident-Response-A-prioritization-model-where-restoring-service-a]] — Restore-First Incident Response: A prioritization model where restoring service always takes precedence over investigation and root cause analysis during an active outage
- [[Route-per-Integration-Point-Tracking-Maintaining-explicit-records-spreadsheet-or]] — Route-per-Integration-Point Tracking: Maintaining explicit records (spreadsheet or database) of destination name, address, and desired route for every remote integration point
- [[SLA-Inversion-Principle-You-cannot-contractually-offer-a-better-SLA-than-the-wor]] — SLA Inversion Principle: You cannot contractually offer a better SLA than the worst SLA of any external dependency involved in delivering that feature
- [[SLA-Inversion-A-framework-recognizing-that-a-systems-effective-SLA-is-bounded-by]] — SLA Inversion: A framework recognizing that a system's effective SLA is bounded by the weakest dependency in its call chain
- [[Scriptable-Operations-Mandate-All-administrative-duties-must-be-automatable-via-]] — Scriptable Operations Mandate: All administrative duties must be automatable via scripts; GUI tools are for learning, not for repeated production operations
- [[Session-Bloat-Anti-Pattern-Placing-large-objects-full-shopping-carts-full-search]] — Session Bloat Anti-Pattern: Placing large objects (full shopping carts, full search results) in serialized sessions, which destroys session-failover scalability and forces disabling of the failover mechanism entirely
- [[Stability-Antipatterns-Framework-a-set-of-named-patterns-that-amplify-transient-]] — Stability Antipatterns Framework: a set of named patterns that amplify transient failures and accelerate systemic cracks, to be identified and avoided
- [[Stability-Antipatterns-vs-Patterns-Map-A-named-interaction-graph-mapping-antipat]] — Stability Antipatterns vs. Patterns Map: A named interaction graph mapping antipatterns (e.g., Cascading Failures, Blocked Threads) to countermeasure patterns (e.g., Timeouts, Circuit Breaker, Bulkheads)
- [[Stability-Patterns-Framework-countermeasures-applied-judiciously-to-specific-ide]] — Stability Patterns Framework: countermeasures applied judiciously to specific identified threats to keep systems running under adverse conditions
- [[Steady-State-A-stability-pattern-requiring-systems-to-manage-their-own-resources]] — Steady State: A stability pattern requiring systems to manage their own resources (logs, data, caches) without human intervention to avoid slow degradation
- [[Systems-Thinking-Senge-Capacity-requires-thinking-in-dynamic-variables-change-ov]] — Systems Thinking (Senge): Capacity requires thinking in dynamic variables, change over time, and interrelated connections rather than linear projection
- [[Technology-Frontier-The-zone-where-highly-interactive-complexity-and-tight-coupl]] — Technology Frontier: The zone where highly interactive complexity and tight coupling together accelerate minor cracks into full-blown system failures
- [[Test-Harness-Pattern-Use-a-dedicated-fake-server-that-simulates-real-failure-mod]] — Test Harness Pattern: Use a dedicated fake server that simulates real failure modes (slow responses, dropped connections, garbage data) to test non-functional resilience behavior in isolation
- [[Theory-of-Constraints-Goldratt-A-management-framework-identifying-that-system-th]] — Theory of Constraints (Goldratt): A management framework identifying that system throughput is limited by a single bottleneck that must be found and exploited before optimizing elsewhere
- [[Theory-of-Constraints-ToC-In-every-system-exactly-one-constraint-determines-capa]] — Theory of Constraints (ToC): In every system, exactly one constraint determines capacity; optimizing any non-bottleneck resource does not increase throughput
- [[Tight-Coupling-Propagation-The-mechanism-by-which-a-failure-in-one-component-rad]] — Tight Coupling Propagation: The mechanism by which a failure in one component radically increases stress on connected components, causing crack propagation or multiplication across system boundaries
- [[Timeouts-Pattern-Stop-waiting-for-a-response-after-a-threshold-period-to-prevent]] — Timeouts Pattern: Stop waiting for a response after a threshold period to prevent blocked threads and cascading failures across integration points
- [[Transparency-Perspectives-A-multi-layer-observability-framework-covering-histori]] — Transparency Perspectives: A multi-layer observability framework covering historical trending, predictions, present status, instantaneous behavior, and dashboard views
- [[Vicious-Cycle-Pattern-resource-contention-causes-slower-transactions-which-cause]] — Vicious Cycle Pattern: resource contention causes slower transactions, which cause more contention, which causes throughput to drop exponentially as response time rises
- [[Virtual-IP-Address-Migration-An-IP-address-not-tied-to-a-specific-NIC-that-can-b]] — Virtual IP Address Migration: An IP address not tied to a specific NIC that can be moved between cluster nodes to enable high availability for non-natively-clustered applications
- [[Yesterdays-Weather-Forecasting-A-predictive-model-attributed-to-Beck-and-Fowler-]] — Yesterday's Weather Forecasting: A predictive model (attributed to Beck and Fowler) where tomorrow's system behavior is predicted by extrapolating past measurements, valid within a defined domain of applicability and invalidated by each new application release
- [[Zero-One-Many-Principle-The-rule-that-the-only-sensible-multiplicities-in-comput]] — Zero-One-Many Principle: The rule that the only sensible multiplicities in computer science are 0, 1, and many — meaning QA must run more than one instance wherever production runs a cluster, not just one

## How to Use This Wiki

**For agents:** Load the thin skill file (`output/skills/`) first.
The skill's concept map tells you which page to read for a given situation.
Read the concept page when you need depth — not the whole wiki.

**For humans:** Browse in Obsidian. Start here, follow wikilinks.
Use the graph view to see which concepts are most connected.

## Related Wikis

<!-- Populated after all book wikis are built -->
