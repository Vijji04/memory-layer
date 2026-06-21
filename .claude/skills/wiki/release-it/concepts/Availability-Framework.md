---
title: Availability Framework
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, release-it, concept]
confidence: high
consolidated_from: 4 pages
---

# Availability Framework

> Consolidated from 4 related concept pages.

---

## Cost vs Avoided Loss Framework Frame availability decisions in financial terms c

## Core Principle

Chapter 13 establishes that availability requirements must always be anchored in a financial cost-vs-avoided-loss calculation, because each additional '9' multiplies both implementation and operational costs. SLAs must be defined per business feature with precise synthetic-transaction monitoring specs rather than as a single vague system-wide promise, and must respect the SLA Inversion constraint imposed by external dependencies. Load balancing options form a spectrum from DNS round-robin (simple but health-unaware and Java-hostile) through reverse proxy to hardware load balancers, while clustering trades linear scalability for coordinated failover.

## Key Heuristics

These are the load-bearing rules for this concept.

> Divorcing a 'want' from its cost always leads to unrealistic desires.

> Each '9' of availability increases the implementation cost by about a factor of ten and the operational cost per year by about a factor of two.

> You cannot offer a better SLA than the worst of the external dependencies involved in a feature.

> It is not enough to write down, 'The system shall be available 99.9% of the time' on a piece of paper. Vagueness lurks behind every word of that sentence.

> DNS round-robin load balancing is inappropriate whenever the calling system is another long-running enterprise system. Anything built on Java will cache the first IP address received from DNS.

> Fully load-balanced farms scale close to linearly. Load-balanced clusters do not.

> I consider cluster servers a Band-Aid for applications that don't do it themselves.

## Anti-Patterns & Fixes

- Vague SLA Agreements: Writing 'the system shall be available 99.9% of the time' without defining what 'the system' is, how availability is measured, what constitutes success or failure, or what formula computes the percentage. Fix: Define SLAs per feature with explicit synthetic transaction monitoring specs, response time thresholds, success/failure response codes, sampling frequency, measurement locations, and the exact percentage formula.
- SLA Inversion: Promising an SLA to customers that is better than the SLA of an underlying third-party or external dependency. Fix: Cap the SLA for any feature at the worst SLA of all its external dependencies; treat external SLAs as pass-throughs at best.
- DNS Round-Robin for Enterprise Consumers: Using DNS round-robin when callers are long-running Java or enterprise systems that cache the first resolved IP address, defeating load balancing entirely. Fix: Use a reverse proxy or hardware load balancer that intercepts every request and has health-awareness.
- URL Rewriting Round-Robin: Using Apache-style URL rewriting so that 'www.example.com' becomes 'www7.example.com', allowing users to bookmark individual servers instead of the front-door address. Fix: Use a transparent reverse proxy that keeps the canonical hostname stable.
- SSL Termination at the Load Balancer (for scalability): Offloading SSL decryption to the hardware load balancer puts CPU work on the single bottleneck device rather than distributing it across the many web servers. Fix: Terminate SSL at the web servers when scalability is the concern; only centralize SSL at the load balancer when certificate management simplicity outweighs the capacity tradeoff.
- Requiring '5 Nines' Without Financial Justification: Stakeholders demanding maximum availability because it 'sounds cool and technical' without evaluating whether the lifecycle cost is justified by avoided losses. Fix: Present a cost table mapping each availability tier to downtime minutes, revenue at risk, and incremental implementation plus operational cost over the system lifespan.

## When To Apply

Load this page when:

- Use this when a stakeholder or product requirement specifies an availability target (e.g., '99.9%' or 'five nines') without accompanying financial justification — apply the Cost-vs-Avoided-Loss Framework to validate or challenge the target.
- Use this when drafting or reviewing a Service Level Agreement — apply the Feature-Level SLA Definition framework to decompose 'the system' into individual business functions with per-function monitoring specs.
- Use this when a feature relies on a third-party API or external service — apply the SLA Inversion Principle to cap the promised SLA at the external dependency's SLA.
- Use this when designing the load balancing layer for a horizontally scaled service — select among DNS round-robin, reverse proxy, and hardware load balancer based on health-awareness needs, protocol, and budget.
- Use this when a Java-based or long-running enterprise service needs to consume a load-balanced endpoint — exclude DNS round-robin and choose a reverse proxy or VIP-based hardware load balancer instead.
- Use this when deciding between a load-balanced farm and a cluster — apply the linear-vs-sublinear scaling heuristic to determine whether the coordination overhead of clustering is acceptable.
- Use this when an application lacks native clustering and active/passive failover is being proposed via a cluster server (e.g., Veritas, WSCS) — flag this as a scalability-limiting Band-Aid and evaluate whether redesigning for active/active is feasible.
- Use this when generating infrastructure-as-code or architecture diagrams that include availability guarantees — ensure synthetic transaction monitoring, health-check endpoints, and explicit SLA measurement formulas are included in the generated artifacts.

## Concrete Examples

- Hotel chain website SLA decomposition: property locator, online reservations, loyalty club subscription, and event bookings each get different SLA tiers based on revenue impact; loyalty club is a vendor pass-through SLA.
- 98% vs 99.99% availability cost table: $1,500/hour peak revenue site, 864 min/month downtime at 98% ($21,600 worst-case loss) vs 4 min/month at 99.99% ($108 loss), with $98,700 added lifecycle cost saving $1,289,520 over five years.
- DNS round-robin defeated by Java caching: any Java-based enterprise caller caches the first resolved IP address, sending all subsequent connections to the same host and completely defeating the load distribution.
- Apache URL rewriting round-robin causing users to bookmark individual servers (e.g., www7.example.com) instead of the canonical front-door address.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 13: Availability**

An LLM coding agent is especially prone to generating availability requirements as vague string literals ('the system shall be 99.9% available') without triggering the financial justification or SLA decomposition steps — this chapter's frameworks force the agent to instead emit structured, per-feature SLA artifacts with explicit monitoring specs. When generating infrastructure or deployment code, an agent may default to DNS round-robin (the simplest pattern to emit) without recognizing that any Java or long-lived service client in the stack will cache the DNS result and break load balancing entirely. Agents also tend to propagate a single top-level SLA through an entire dependency graph without applying the SLA Inversion check, silently generating contracts that promise more than any upstream vendor can deliver.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## CostCost Availability Trade off Frame availability requirements as a costbenefit

## Core Principle

Chapter 15 consolidates production-readiness design principles: use VIPs for clustered service access, run applications as unprivileged users, isolate secrets, separate plumbing from environment config, define availability at the feature level rather than system level, and ensure all admin operations are scriptable. The core argument is that ignoring these concerns during development merely defers their cost to production, where the cost is far higher and recurring. Load balancing and clustering decisions should be made early, driven by per-feature availability requirements negotiated as explicit cost trade-offs.

## Key Heuristics

These are the load-bearing rules for this concept.

> You can choose not to deal with these issues during development. If so, you will deal with them in production...time and time again.

> Not every system requires five nines of availability. The cost of greater availability increases radically at each level.

> Mixing [essential plumbing with environment-specific configuration] is the equivalent of putting the ejection seat button next to the radio tuner. Sooner or later, something bad will happen.

> Pretty Java desktop administration GUIs help the novice learn his way around, but nobody wants to click through the pretty GUI for the thousandth time.

> Be sure to use virtual IP addresses to access clustered services... Using the VIP allows the service provider to fail over without necessitating the reconfiguration of your system.

> Applications should be able to run as application users; they should not require root or Administrator permissions.

> Startup and shutdown should be nondisruptive to users, and any administration duty must be scriptable.

## Anti-Patterns & Fixes

- HardcodedServiceIPs: Connecting directly to a physical IP of a clustered service (e.g., database) so that any failover requires reconfiguring the consuming application. Fix: Always connect via a Virtual IP (VIP) that abstracts the physical endpoint.
- MixedConfigurationFiles: Bundling framework plumbing (e.g., Spring beans.xml) together with environment-specific config, making it easy for operators to accidentally alter critical settings. Fix: Separate essential plumbing config from environment-specific config into distinct files.
- RootRunningApplication: Running application processes as root or Administrator, creating unnecessary security risk. Fix: Create dedicated application users with least-privilege permissions.
- PlaintextSecretsInMainConfig: Storing sensitive parameters like database passwords or encryption keys in general configuration files. Fix: Isolate sensitive configuration into separate, access-controlled files.
- AdminFunctionsOnProductionNetwork: Exposing administrative and monitoring endpoints on the same network interface as production traffic. Fix: Bind administrative functions exclusively to the administration and monitoring network.
- GUI-OnlyAdministration: Designing admin workflows that require GUI interaction, making automation and repeated tasks inefficient. Fix: Ensure every administrative function is scriptable from the command line.

## When To Apply

Load this page when:

- Use this when generating service client code that connects to a database, cache, or external web service — ensure the connection target is a VIP, not a physical hostname.
- Use this when scaffolding application configuration files — separate framework/plumbing config from environment-specific parameters into distinct files.
- Use this when writing Dockerfile, systemd unit files, or process startup scripts — verify the process runs as a non-root application user.
- Use this when designing or generating an admin API or monitoring endpoint — bind it to a separate network interface or port from the production-facing API.
- Use this when defining availability SLAs or uptime requirements in architecture docs — prompt the user to specify per-feature availability rather than a single system-wide number, and to exclude external dependencies.
- Use this when generating startup and shutdown lifecycle hooks — ensure the procedure is graceful and non-disruptive, and that it can be triggered via script.
- Use this when storing secrets (passwords, API keys, encryption keys) in generated config — place them in a dedicated secrets file, not inline with general application config.

## Concrete Examples

- Spring's beans.xml file cited as an example of essential framework plumbing that should be kept separate from environment-specific configuration.
- Ejection seat button placed next to the radio tuner — used as an analogy for the danger of mixing plumbing config with environment config.
- Pretty Java desktop administration GUI cited as an example of a tool useful for onboarding but unsuitable for repeated production operations.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 15: Design Summary**

An LLM coding agent is especially prone to the anti-patterns here because it generates 'working' code by default — hardcoding IPs, embedding secrets in config, running as root — since these choices produce immediately functional output without triggering test failures. The agent must be explicitly prompted or constrained to apply VIP addressing, least-privilege users, and config separation, as it will not infer operational risk from passing unit tests. Additionally, agents generating infrastructure-as-code or deployment manifests will silently expose admin endpoints on public interfaces unless the separation of admin vs. production networks is a named constraint in the generation prompt.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Feature Level Availability Definition Define availability requirements per featu

## Core Principle

Chapter 15 consolidates production-readiness design principles: use VIPs for clustered service access, run applications as unprivileged users, isolate secrets, separate plumbing from environment config, define availability at the feature level rather than system level, and ensure all admin operations are scriptable. The core argument is that ignoring these concerns during development merely defers their cost to production, where the cost is far higher and recurring. Load balancing and clustering decisions should be made early, driven by per-feature availability requirements negotiated as explicit cost trade-offs.

## Key Heuristics

These are the load-bearing rules for this concept.

> You can choose not to deal with these issues during development. If so, you will deal with them in production...time and time again.

> Not every system requires five nines of availability. The cost of greater availability increases radically at each level.

> Mixing [essential plumbing with environment-specific configuration] is the equivalent of putting the ejection seat button next to the radio tuner. Sooner or later, something bad will happen.

> Pretty Java desktop administration GUIs help the novice learn his way around, but nobody wants to click through the pretty GUI for the thousandth time.

> Be sure to use virtual IP addresses to access clustered services... Using the VIP allows the service provider to fail over without necessitating the reconfiguration of your system.

> Applications should be able to run as application users; they should not require root or Administrator permissions.

> Startup and shutdown should be nondisruptive to users, and any administration duty must be scriptable.

## Anti-Patterns & Fixes

- HardcodedServiceIPs: Connecting directly to a physical IP of a clustered service (e.g., database) so that any failover requires reconfiguring the consuming application. Fix: Always connect via a Virtual IP (VIP) that abstracts the physical endpoint.
- MixedConfigurationFiles: Bundling framework plumbing (e.g., Spring beans.xml) together with environment-specific config, making it easy for operators to accidentally alter critical settings. Fix: Separate essential plumbing config from environment-specific config into distinct files.
- RootRunningApplication: Running application processes as root or Administrator, creating unnecessary security risk. Fix: Create dedicated application users with least-privilege permissions.
- PlaintextSecretsInMainConfig: Storing sensitive parameters like database passwords or encryption keys in general configuration files. Fix: Isolate sensitive configuration into separate, access-controlled files.
- AdminFunctionsOnProductionNetwork: Exposing administrative and monitoring endpoints on the same network interface as production traffic. Fix: Bind administrative functions exclusively to the administration and monitoring network.
- GUI-OnlyAdministration: Designing admin workflows that require GUI interaction, making automation and repeated tasks inefficient. Fix: Ensure every administrative function is scriptable from the command line.

## When To Apply

Load this page when:

- Use this when generating service client code that connects to a database, cache, or external web service — ensure the connection target is a VIP, not a physical hostname.
- Use this when scaffolding application configuration files — separate framework/plumbing config from environment-specific parameters into distinct files.
- Use this when writing Dockerfile, systemd unit files, or process startup scripts — verify the process runs as a non-root application user.
- Use this when designing or generating an admin API or monitoring endpoint — bind it to a separate network interface or port from the production-facing API.
- Use this when defining availability SLAs or uptime requirements in architecture docs — prompt the user to specify per-feature availability rather than a single system-wide number, and to exclude external dependencies.
- Use this when generating startup and shutdown lifecycle hooks — ensure the procedure is graceful and non-disruptive, and that it can be triggered via script.
- Use this when storing secrets (passwords, API keys, encryption keys) in generated config — place them in a dedicated secrets file, not inline with general application config.

## Concrete Examples

- Spring's beans.xml file cited as an example of essential framework plumbing that should be kept separate from environment-specific configuration.
- Ejection seat button placed next to the radio tuner — used as an analogy for the danger of mixing plumbing config with environment config.
- Pretty Java desktop administration GUI cited as an example of a tool useful for onboarding but unsuitable for repeated production operations.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 15: Design Summary**

An LLM coding agent is especially prone to the anti-patterns here because it generates 'working' code by default — hardcoding IPs, embedding secrets in config, running as root — since these choices produce immediately functional output without triggering test failures. The agent must be explicitly prompted or constrained to apply VIP addressing, least-privilege users, and config separation, as it will not infer operational risk from passing unit tests. Additionally, agents generating infrastructure-as-code or deployment manifests will silently expose admin endpoints on public interfaces unless the separation of admin vs. production networks is a named constraint in the generation prompt.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Feature Level SLA Definition Define availability SLAs per discrete business feat

## Core Principle

Chapter 13 establishes that availability requirements must always be anchored in a financial cost-vs-avoided-loss calculation, because each additional '9' multiplies both implementation and operational costs. SLAs must be defined per business feature with precise synthetic-transaction monitoring specs rather than as a single vague system-wide promise, and must respect the SLA Inversion constraint imposed by external dependencies. Load balancing options form a spectrum from DNS round-robin (simple but health-unaware and Java-hostile) through reverse proxy to hardware load balancers, while clustering trades linear scalability for coordinated failover.

## Key Heuristics

These are the load-bearing rules for this concept.

> Divorcing a 'want' from its cost always leads to unrealistic desires.

> Each '9' of availability increases the implementation cost by about a factor of ten and the operational cost per year by about a factor of two.

> You cannot offer a better SLA than the worst of the external dependencies involved in a feature.

> It is not enough to write down, 'The system shall be available 99.9% of the time' on a piece of paper. Vagueness lurks behind every word of that sentence.

> DNS round-robin load balancing is inappropriate whenever the calling system is another long-running enterprise system. Anything built on Java will cache the first IP address received from DNS.

> Fully load-balanced farms scale close to linearly. Load-balanced clusters do not.

> I consider cluster servers a Band-Aid for applications that don't do it themselves.

## Anti-Patterns & Fixes

- Vague SLA Agreements: Writing 'the system shall be available 99.9% of the time' without defining what 'the system' is, how availability is measured, what constitutes success or failure, or what formula computes the percentage. Fix: Define SLAs per feature with explicit synthetic transaction monitoring specs, response time thresholds, success/failure response codes, sampling frequency, measurement locations, and the exact percentage formula.
- SLA Inversion: Promising an SLA to customers that is better than the SLA of an underlying third-party or external dependency. Fix: Cap the SLA for any feature at the worst SLA of all its external dependencies; treat external SLAs as pass-throughs at best.
- DNS Round-Robin for Enterprise Consumers: Using DNS round-robin when callers are long-running Java or enterprise systems that cache the first resolved IP address, defeating load balancing entirely. Fix: Use a reverse proxy or hardware load balancer that intercepts every request and has health-awareness.
- URL Rewriting Round-Robin: Using Apache-style URL rewriting so that 'www.example.com' becomes 'www7.example.com', allowing users to bookmark individual servers instead of the front-door address. Fix: Use a transparent reverse proxy that keeps the canonical hostname stable.
- SSL Termination at the Load Balancer (for scalability): Offloading SSL decryption to the hardware load balancer puts CPU work on the single bottleneck device rather than distributing it across the many web servers. Fix: Terminate SSL at the web servers when scalability is the concern; only centralize SSL at the load balancer when certificate management simplicity outweighs the capacity tradeoff.
- Requiring '5 Nines' Without Financial Justification: Stakeholders demanding maximum availability because it 'sounds cool and technical' without evaluating whether the lifecycle cost is justified by avoided losses. Fix: Present a cost table mapping each availability tier to downtime minutes, revenue at risk, and incremental implementation plus operational cost over the system lifespan.

## When To Apply

Load this page when:

- Use this when a stakeholder or product requirement specifies an availability target (e.g., '99.9%' or 'five nines') without accompanying financial justification — apply the Cost-vs-Avoided-Loss Framework to validate or challenge the target.
- Use this when drafting or reviewing a Service Level Agreement — apply the Feature-Level SLA Definition framework to decompose 'the system' into individual business functions with per-function monitoring specs.
- Use this when a feature relies on a third-party API or external service — apply the SLA Inversion Principle to cap the promised SLA at the external dependency's SLA.
- Use this when designing the load balancing layer for a horizontally scaled service — select among DNS round-robin, reverse proxy, and hardware load balancer based on health-awareness needs, protocol, and budget.
- Use this when a Java-based or long-running enterprise service needs to consume a load-balanced endpoint — exclude DNS round-robin and choose a reverse proxy or VIP-based hardware load balancer instead.
- Use this when deciding between a load-balanced farm and a cluster — apply the linear-vs-sublinear scaling heuristic to determine whether the coordination overhead of clustering is acceptable.
- Use this when an application lacks native clustering and active/passive failover is being proposed via a cluster server (e.g., Veritas, WSCS) — flag this as a scalability-limiting Band-Aid and evaluate whether redesigning for active/active is feasible.
- Use this when generating infrastructure-as-code or architecture diagrams that include availability guarantees — ensure synthetic transaction monitoring, health-check endpoints, and explicit SLA measurement formulas are included in the generated artifacts.

## Concrete Examples

- Hotel chain website SLA decomposition: property locator, online reservations, loyalty club subscription, and event bookings each get different SLA tiers based on revenue impact; loyalty club is a vendor pass-through SLA.
- 98% vs 99.99% availability cost table: $1,500/hour peak revenue site, 864 min/month downtime at 98% ($21,600 worst-case loss) vs 4 min/month at 99.99% ($108 loss), with $98,700 added lifecycle cost saving $1,289,520 over five years.
- DNS round-robin defeated by Java caching: any Java-based enterprise caller caches the first resolved IP address, sending all subsequent connections to the same host and completely defeating the load distribution.
- Apache URL rewriting round-robin causing users to bookmark individual servers (e.g., www7.example.com) instead of the canonical front-door address.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 13: Availability**

An LLM coding agent is especially prone to generating availability requirements as vague string literals ('the system shall be 99.9% available') without triggering the financial justification or SLA decomposition steps — this chapter's frameworks force the agent to instead emit structured, per-feature SLA artifacts with explicit monitoring specs. When generating infrastructure or deployment code, an agent may default to DNS round-robin (the simplest pattern to emit) without recognizing that any Java or long-lived service client in the stack will cache the DNS result and break load balancing entirely. Agents also tend to propagate a single top-level SLA through an entire dependency graph without applying the SLA Inversion check, silently generating contracts that promise more than any upstream vendor can deliver.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/release-it/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
