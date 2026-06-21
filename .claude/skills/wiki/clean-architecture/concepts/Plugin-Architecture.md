---
title: Component Plugin Architecture: Dynamically linked files (.jar, .dll, shared libraries) that can be composed at runtime, making independent deployability the default rather than a heroic effort
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-12-Components.json]
contributing_chapters: ["Chapter 12: Components"]
confidence: high
---

# Plugin Architecture

## Component Plugin Architecture

# Component Plugin Architecture: Dynamically linked files (.jar, .dll, shared libraries) that can be composed at runtime, making independent deployability the default rather than a heroic effort

> From chapter: *Chapter 12: Components*

## Core Principle

Components are the atomic units of deployment—jar files, DLLs, shared libraries—and their defining property is that they must remain independently deployable and therefore independently developable. The chapter traces how 50 years of toolchain evolution (relocatable binaries, linkers, dynamic loading) progressively enabled this property, culminating in the plugin architecture that is now the default. Well-designed components preserve this independence regardless of whether they are ultimately deployed as a single executable, an archive, or dynamically loaded plugins.

## Key Heuristics

These are the load-bearing rules for this concept.

> Well-designed components always retain the ability to be independently deployable and, therefore, independently developable.

> Programs will grow to fill all available compile and link time.

> Components are the granule of deployment.

> These dynamically linked files, which can be plugged together at runtime, are the software components of our architectures.

> Component plugin architecture can be the casual default as opposed to the herculean effort it once was.

## Anti-Patterns & Fixes

- Monolithic Source Compilation: Including all library source directly in the application and compiling everything together. Fix: Separate library source into independently compiled and deployable binary components to reduce compile times and enable reuse.
- Fixed-Address Binary Coupling: Compiling programs to run at hard-coded memory addresses, making relocation impossible and causing fragmentation as programs grow. Fix: Use relocatable binaries with loader-resolved symbol references.
- Merged Link-and-Load Phase: Performing symbol resolution (slow) at load time when programs and libraries are large causes unacceptable startup delays. Fix: Pre-link into a relocatable executable offline; keep the load phase fast.
- Ambition Outpacing Infrastructure: Continuously growing program size erases toolchain speed gains, producing perpetual hour-long turnaround cycles. Fix: Decompose programs into small, independently compilable and linkable components so only changed units need reprocessing.

## When To Apply

Load this page when:

- Use this when deciding what granularity to use for packaging and shipping code (jar, DLL, shared library, gem) to ensure each unit can be deployed independently.
- Use this when a build is taking too long because too many modules are compiled or linked together, signaling the need to split into smaller independently deployable components.
- Use this when designing a plugin or extension system where third-party code must be loaded dynamically at runtime without recompiling the host application.
- Use this when determining the boundary between modules that should be versioned and released together versus modules that need independent release cycles.
- Use this when evaluating whether a proposed code change violates independent deployability by introducing hard compile-time dependencies across component boundaries.
- Use this when generating project scaffolding or build configuration to enforce that each component produces a single deployable artifact with well-defined external interfaces.

## Concrete Examples

- PDP-8 assembly program using *200 origin statement to fix load address at 200 octal, illustrating hard-coded memory layout and non-relocatable code.
- Early memory layout where function library was compiled to a fixed address (e.g., 2000 octal) and applications had to fit in remaining space, leading to fragmentation when apps grew.
- Minecraft .jar mod folder and ReSharper DLLs in Visual Studio as present-day examples of component plugin architecture in casual use.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 12: Components**

An LLM coding agent tends to generate large monolithic files or inline all dependencies into a single compilation unit because it operates on a per-prompt context rather than a deployment topology—mirroring the early 'include all library source' anti-pattern. This chapter's principle forces the agent to explicitly reason about deployment boundaries when generating code: each generated artifact must be independently buildable and releasable, not just syntactically correct. Failing to apply this causes agent-generated codebases to become tightly coupled blobs where a single change requires rebuilding and redeploying everything, eliminating the independent developability that makes component-based systems maintainable.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Plugin Architecture A

# Plugin Architecture: A design pattern where low-level detail modules (UI, database, devices) are plugged into high-level policy modules, making high-level code unaware of low-level implementations

> From chapter: *Chapter 5: Object-Oriented Programming*

## Core Principle

OO's most important contribution is not encapsulation or inheritance (both of which existed in C) but safe, convenient polymorphism, which enables dependency inversion: the ability to point any source code dependency opposite to the flow of control. This gives architects absolute control over module boundaries, enabling plugin architectures where high-level business rules are completely independent of low-level details like UI and databases. Independent source code dependencies yield independent deployability and developability — the practical payoff of OO design.

## Key Heuristics

These are the load-bearing rules for this concept.

> OO is the ability, through the use of polymorphism, to gain absolute control over every source code dependency in the system.

> OO imposes discipline on indirect transfer of control.

> The low-level details are relegated to plugin modules that can be deployed and developed independently from the modules that contain high-level policies.

> Any source code dependency, no matter where it is, can be inverted.

> Software architects working in systems written in OO languages have absolute control over the direction of all source code dependencies in the system. They are not constrained to align those dependencies with the flow of control.

> If the modules in your system can be deployed independently, then they can be developed independently by different teams.

> The business rules, the UI, and the database can be compiled into three separate components or deployment units that have the same dependencies as the source code.

## Anti-Patterns & Fixes

- SourceDependencyFollowsControlFlow: Structuring code so that source code dependencies mirror the runtime call chain (main -> high-level -> mid-level -> low-level), which couples every layer to the next and prevents independent deployment. Fix: Insert interfaces at boundaries so high-level modules depend on abstractions, not concrete lower-level modules.
- ManualFunctionPointerPolymorphism: Using raw C-style function pointers to achieve dispatch without enforced conventions, leading to uninitialized pointers and untraceable bugs. Fix: Use OO language polymorphism (virtual functions, interfaces) to make dispatch safe and implicit.
- BusinessRulesDependingOnUI/DB: Writing business logic that directly imports or references UI or database modules, making the core of the system non-deployable without its peripherals. Fix: Invert dependencies so UI and database depend on business rule interfaces, not the reverse.
- WeakEncapsulationReliance: Assuming OO languages provide strong encapsulation by default (e.g., putting private member declarations in headers in C++, or not separating interfaces in Java/C#), exposing implementation details to clients. Fix: Rely on explicit interface types and dependency inversion for information hiding rather than trusting language-level access modifiers alone.

## When To Apply

Load this page when:

- Use this when designing the boundary between business logic and a database or UI layer to decide which direction the dependency should point.
- Use this when a change in a low-level module (e.g., a data store or third-party library) is causing ripple recompilation or redeployment of unrelated high-level modules.
- Use this when adding a new device, service, or implementation variant and you want the existing high-level code to require zero changes.
- Use this when decomposing a system into independently deployable components (e.g., separate JAR files, DLLs, or microservices) and determining which component should own each interface definition.
- Use this when two teams need to develop against a shared boundary concurrently without blocking each other — introduce an interface owned by the high-level module.
- Use this when evaluating whether to use an abstract interface vs. a direct import/dependency in a module that is supposed to represent high-level policy.
- Use this when a calling module must not be recompiled when the called module's implementation changes.

## Concrete Examples

- C point.h/point.c: Perfect encapsulation achieved in C using forward declarations in a header and implementation hidden in a .c file — showing encapsulation predates OO.
- C NamedPoint masquerading as Point: Manually mimicking inheritance in C by ensuring the first two fields of NamedPoint match Point's layout, allowing unsafe casting — showing inheritance predates OO.
- UNIX FILE struct with function pointers (open, close, read, write, seek): Demonstrates polymorphism via explicit function pointer tables in C, showing polymorphism predates OO but is dangerous without language enforcement.
- Copy program reading from STDIN/writing to STDOUT: Illustrates device-independent polymorphic behavior where new IO devices (handwriting recognizer, speech synthesizer) require zero changes to the copy program.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 5: Object-Oriented Programming**

An LLM coding agent, when generating multi-module systems, defaults to following the call graph with its import/dependency graph — high-level modules directly import low-level ones — because that is the most statistically common pattern in training data. This produces architectures where business logic is tightly coupled to database or framework code, making generated systems hard to test, extend, or redeploy independently. Applying dependency inversion as an explicit generation constraint — defining interfaces owned by high-level modules and having low-level modules implement them — prevents the agent from producing the most common but architecturally damaging coupling pattern.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Plugin Architecture Core

# Plugin Architecture: Core business rules are kept independent of optional or variable components (GUI, database, frameworks) which plug into the core rather than being coupled to it

> From chapter: *Chapter 17: Boundaries: Drawing Lines*

## Core Principle

Architecture is the discipline of drawing boundary lines that isolate core business rules from variable infrastructure details (databases, GUIs, frameworks), with all dependency arrows pointing inward toward the business rules. The primary value of these boundaries is deferring irreversible technology decisions until real requirements justify them, thereby minimizing wasted effort from premature coupling. The Plugin Architecture pattern operationalizes this by treating every non-core component as a dependency that plugs into stable business abstractions, creating firewalls that prevent infrastructure changes from propagating into domain logic.

## Key Heuristics

These are the load-bearing rules for this concept.

> A good system architecture is one in which decisions like these are rendered ancillary and deferrable.

> The goal of an architect is to minimize the human resources required to build and maintain the required system.

> What saps this kind of people-power? Coupling—and especially coupling to premature decisions.

> Boundaries are drawn where there is an axis of change. The components on one side of the boundary change at different rates, and for different reasons, than the components on the other side.

> You draw lines between things that matter and things that don't.

> The IO is irrelevant.

> Arranging our systems into a plugin architecture creates firewalls across which changes cannot propagate.

> The SRP tells us where to draw our boundaries.

## Anti-Patterns & Fixes

- Premature Topology Adoption: Committing to a distributed three-tier architecture before validating that distribution is required, multiplying development effort for infrastructure that never gets used. Fix: Treat deployment topology as a deferred decision; write business logic first and let topology emerge from real requirements.
- Enterprise Architecture Overreach: Imposing a full SOA domain-service model on a small system, forcing every trivial feature through a bureaucratic service mesh. Fix: Start with the simplest structure that isolates business rules; add service layers only when proven necessary by scale or team boundaries.
- GUI-as-System Confusion: Defining the system in terms of its interface and demanding visible UI before core logic is validated. Fix: Build and test the business rule model independently of any UI; treat the GUI as a plugin that depends on the model, not the reverse.
- Framework Coupling: Baking a web framework, ORM, or DI container into core business logic so that the business rules cannot be tested or deployed without those tools. Fix: Place an interface or abstraction layer between business logic and any framework; the framework depends on you, not you on it.
- Premature Database Commitment: Choosing and integrating a database engine before business rules are stable, causing schema churn and slow tests throughout early development. Fix: Introduce a data-access interface (e.g., WikiPage) and use in-memory or stub implementations until persistence requirements are understood.

## When To Apply

Load this page when:

- Use this when scaffolding a new service or application and deciding which external dependencies (database, HTTP framework, message broker) to wire in at project start.
- Use this when a change to a UI component, database schema, or third-party library requires editing core business logic files.
- Use this when writing tests for business logic that are slow because they require a running database, web server, or external service.
- Use this when a simple feature addition requires changes in many layers or many files across unrelated modules.
- Use this when choosing between implementing a feature directly versus routing it through an existing service abstraction layer.
- Use this when generating code for a domain model and deciding where to place data-access or persistence logic.
- Use this when evaluating whether to adopt a framework, ORM, or architectural pattern early in a project.

## Concrete Examples

- Company P: Built a three-tier Java web app with serialization and marshaling across tiers for every feature, yet never deployed on more than a single server—paying the full distributed-system cost permanently with no benefit.
- Company W: An 'architect' imposed enterprise SOA with a ServiceRegistry and inter-service messaging on a small fleet-management business, making even adding a contact field require multi-service orchestration and fake data.
- FitNesse: Deferred database decision for 18 months by placing data access behind a WikiPage interface, using MockWikiPage then InMemoryPage then FileSystemWikiPage, ultimately never needing MySQL despite keeping the option open.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 17: Boundaries: Drawing Lines**

An LLM coding agent defaults to generating fully-wired, concrete implementations—importing an ORM, instantiating a web framework, and coupling business logic to infrastructure in the very first files it produces—because its training data is dominated by complete, runnable examples rather than architecturally staged ones. This chapter's patterns prevent the agent from front-loading irreversible technology choices that inflate the cost of every subsequent generation task. Specifically, an agent should generate interface/abstract boundaries first and defer concrete adapter implementations, mirroring the FitNesse stub-then-implement sequence, so that generated business logic remains testable and replaceable regardless of what infrastructure the agent assumed.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Plugin Architecture for

# Plugin Architecture for Low-Level Components: Lower-level components are designed as plugins to higher-level ones, so the high-level component knows nothing of the low-level implementation

> From chapter: *Policy and Level*

## Core Principle

Every software program is a set of policies, and those policies differ in their level — defined as distance from system inputs and outputs. High-level policies are more stable and important; low-level policies are volatile and urgent. Good architecture separates policies by level, organizes them into a DAG of components, and ensures all compile-time dependencies point toward higher-level components regardless of data flow direction, so that trivial I/O changes never destabilize core business logic.

## Key Heuristics

These are the load-bearing rules for this concept.

> A strict definition of 'level' is 'the distance from the inputs and outputs.'

> In a good architecture, the direction of those dependencies is based on the level of the components that they connect. In every case, low-level components are designed so that they depend on high-level components.

> We want source code dependencies to be decoupled from data flow and coupled to level.

> Higher-level policies—those that are farthest from the inputs and outputs—tend to change less frequently, and for more important reasons, than lower-level policies.

> Lower-level policies—those that are closest to the inputs and outputs—tend to change frequently, and with more urgency, but for less important reasons.

> Keeping these policies separate, with all source code dependencies pointing in the direction of the higher-level policies, reduces the impact of change.

> Lower-level components should be plugins to the higher-level components.

> Policies that change for the same reasons, and at the same times, are at the same level and belong together in the same component.

## Anti-Patterns & Fixes

- High-Level-Depends-on-Low-Level: Writing a top-level function (e.g., encrypt()) that directly calls low-level I/O functions (readChar, writeChar) causes the core business logic to be coupled to peripheral concerns. Fix: Introduce interfaces (CharReader, CharWriter) that the high-level component depends on; let low-level concrete classes (ConsoleReader, ConsoleWriter) implement those interfaces, inverting the dependency.
- Data-Flow-Mirrored-Dependencies: Structuring source code dependencies to follow the data flow direction rather than the level hierarchy entangles stable policies with volatile ones. Fix: Allow data to flow through components in one direction while source code dependencies point in the opposite direction toward higher-level components.
- Mixing Policies of Different Levels in One Component: Grouping policies that change for different reasons and at different times into the same component causes frequent, low-urgency I/O changes to destabilize important business logic. Fix: Separate policies by their rate and reason of change, placing them in distinct components connected by directed dependencies.
- Concrete I/O Coupled to Core Algorithm: Directly referencing concrete I/O classes inside the encryption or business logic layer makes the core policy non-reusable across contexts. Fix: Wrap I/O behind abstractions owned by the high-level component so the encryption policy is usable in any I/O context.

## When To Apply

Load this page when:

- Use this when designing a new module that has both core business logic and I/O handling, to decide which direction dependencies should point.
- Use this when a change to a peripheral concern (file format, UI, device driver) is breaking or requiring modification to core logic.
- Use this when deciding whether two classes or modules should be co-located in the same component or separated into different components.
- Use this when tracing why a stable, rarely-changed algorithm is being forced to recompile or redeploy when low-level infrastructure changes.
- Use this when generating a new feature end-to-end and needing to determine the correct layering so that high-level policy files do not import low-level implementation files.
- Use this when evaluating whether an existing architecture's dependency graph is a valid DAG with correct directional flow.
- Use this when introducing a new I/O mechanism (e.g., switching from file to network input) and needing to ensure zero changes to core business logic.

## Concrete Examples

- Simple encryption program: reads characters from an input device, translates them using a table, and writes translated characters to an output device — used to illustrate incorrect vs. correct dependency direction.
- Incorrect encrypt() function that directly calls readChar() and writeChar(), demonstrating a high-level function incorrectly depending on low-level I/O functions.
- Correct class diagram with Encrypt class depending on CharReader and CharWriter interfaces, while ConsoleReader and ConsoleWriter implement those interfaces — showing all dependencies crossing the boundary pointing inward.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Policy and Level**

An LLM coding agent, when generating end-to-end feature code in a single pass, will naturally mirror data flow in its import/dependency structure — writing high-level functions that directly call low-level I/O utilities — because the shortest, most literal code path matches data flow. This chapter's framework prevents that failure mode by requiring the agent to explicitly invert dependencies through interfaces whenever it identifies a level boundary. Agents must treat 'distance from I/O' as a first-class architectural signal when deciding which module owns an interface definition and which module depends on it.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

