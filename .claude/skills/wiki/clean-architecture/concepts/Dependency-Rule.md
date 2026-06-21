---
title: Dependency Rule Applied to Frameworks: Source code dependencies must point inward; frameworks must not be imported into inner architectural circles
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-32-Frameworks-Are-Details.json]
contributing_chapters: ["Chapter 32: Frameworks Are Details"]
confidence: high
---

# Dependency Rule

## Dependency Rule Applied

# Dependency Rule Applied to Frameworks: Source code dependencies must point inward; frameworks must not be imported into inner architectural circles

> From chapter: *Chapter 32: Frameworks Are Details*

## Core Principle

Frameworks are implementation details, not architectures — they belong in the outermost dependency circles and must never be coupled into core business logic or Entities. The developer-framework relationship is asymmetric: you take on all the risk of coupling while the framework author owes you nothing. The solution is to treat frameworks as late-bound, replaceable plugins by using proxies and adapters, restricting framework knowledge to the Main component and outer layers.

## Key Heuristics

These are the load-bearing rules for this concept.

> Frameworks are not architectures—though some try to be.

> Don't marry the framework!

> Keep it at arm's length. Treat the framework as a detail that belongs in one of the outer circles of the architecture. Don't let it into the inner circles.

> If the framework wants you to derive your business objects from its base classes, say no! Derive proxies instead, and keep those proxies in components that are plugins to your business rules.

> When you marry a framework to your application, you will be stuck with that framework for the rest of the life cycle of that application.

> Perhaps you can find a way to get the milk without buying the cow.

> You should not sprinkle @autowired annotations all throughout your business objects. Your business objects should not know about Spring.

## Anti-Patterns & Fixes

- FrameworkMarriage: Wrapping your entire architecture around a framework by deriving business objects from its base classes, tightly coupling core logic to framework internals. This makes the framework impossible to remove and causes friction as the product matures. Fix: Derive proxies or adapters that live in outer plugin layers, keeping business rules framework-agnostic.
- EntityContamination: Importing framework annotations or base classes directly into Entities or core business objects (e.g., @autowired on business classes). This violates the Dependency Rule and embeds a volatile detail into stable core logic. Fix: Restrict framework coupling to the Main component or outermost plugin layer.
- PrematureFrameworkCommitment: Adopting a framework at the start of a project without evaluating long-term fit, treating its conventions as architecture. Fix: 'Date' the framework first — use it behind an architectural boundary and delay full commitment as long as possible.
- FrameworkEvolutionLockIn: Assuming the framework will evolve in a direction aligned with your needs, leading to forced upgrades or loss of features. Fix: Isolate framework usage behind interfaces so that switching or upgrading affects only the outer layer.

## When To Apply

Load this page when:

- Use this when choosing whether to extend a framework's base class inside a domain model or Entity class.
- Use this when scaffolding a new service and deciding where to place framework-specific annotations (e.g., Spring @autowired, Django models.Model inheritance).
- Use this when a framework upgrade is breaking core business logic, indicating the framework has leaked into inner architectural layers.
- Use this when evaluating whether to adopt a new framework for a greenfield project and determining how deeply to integrate it.
- Use this when a newer, better framework appears and you need to assess migration cost — high cost signals the current framework was over-married.
- Use this when writing dependency injection wiring code and deciding which components should be aware of the DI container.
- Use this when a framework's conventions conflict with clean domain modeling (e.g., ORM requiring anemic entities with no-arg constructors).

## Concrete Examples

- Spring Framework @autowired annotations: the text warns against sprinkling @autowired throughout business objects, recommending injection be confined to the Main component instead.
- C++ STL and Java standard library cited as examples of frameworks you 'must marry' — unavoidable but still a deliberate decision to acknowledge.
- Spring used as a dependency injection framework injecting into Main — acceptable because Main is the 'dirtiest, lowest-level component in the architecture'.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 32: Frameworks Are Details**

An LLM coding agent defaults to idiomatic framework usage as seen in training data — scaffolding code that inherits from framework base classes, sprinkles framework annotations on domain objects, and structures the entire codebase around framework conventions, effectively marrying the framework by default on every generation. This is worse than human over-adoption because the agent has no long-term stake in the project and will not experience the maintenance pain, so it has no self-correcting feedback signal. Agents must be explicitly constrained to treat frameworks as outer-circle plugins and to generate adapter/proxy patterns rather than direct framework inheritance in core domain code.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Dependency Rule Orientation

# Dependency Rule Orientation: All source code dependencies point toward higher-level policy components; arrows point up in architectural diagrams toward the component with the highest-level policies

> From chapter: *Layers and Boundaries*

## Core Principle

Architectural boundaries correspond to axes of independent change, and they exist at more granular levels than the classic UI/logic/data triad. The decision of whether to fully implement, partially implement, or ignore each boundary is not made once at project start but monitored continuously, with implementation triggered at the inflection point where the cost of adding the boundary exceeds the cost of its absence. APIs at each boundary are owned by the upstream, higher-level policy component, and all source-code dependencies point toward the highest-level policy.

## Key Heuristics

These are the load-bearing rules for this concept.

> Architectural boundaries exist everywhere. We, as architects, must be careful to recognize when they are needed.

> When you discover that you truly do need an architectural boundary where none exists, the costs and risks can be very high to add such a boundary.

> Over-engineering is often much worse than under-engineering.

> You don't simply decide at the start of a project which boundaries to implement and which to ignore. Rather, you watch.

> Your goal is to implement the boundaries right at the inflection point where the cost of implementing becomes less than the cost of ignoring.

> The API defined by those Boundary interfaces is owned by the upstream component.

> You must weigh the costs and determine where the architectural boundaries lie, and which should be fully implemented, and which should be partially implemented, and which should be ignored.

## Anti-Patterns & Fixes

- Premature Over-Abstraction (YAGNI Violation): Adding every conceivable architectural boundary upfront makes the system needlessly complex and expensive before the need is proven. Fix: Start with fewer boundaries, watch for friction, and add boundaries at the inflection point when ignoring them costs more than implementing them.
- Ignoring Boundaries Until Too Late: Deferring all boundary decisions indefinitely means that when a boundary becomes necessary, it is extremely expensive to retrofit even with good tests and refactoring discipline. Fix: Continuously monitor for early signs of friction (e.g., components becoming hard to change independently) and implement boundaries proactively at that signal.
- Implementer-Owned APIs: Letting the downstream/implementing component define the API couples higher-level policy to lower-level details. Fix: Always have the upstream, higher-level component define and own the API that lower-level components implement.
- Single-Axis Boundary Thinking: Assuming that one axis of variation (e.g., UI language) captures all the variation in a layer, missing other axes (e.g., communication mechanism). Fix: Explicitly enumerate all independent axes of change per component layer and evaluate whether each warrants its own boundary.
- Flat Three-Layer Thinking: Treating all systems as simply UI + Business Rules + Database, missing intermediate architectural layers. Fix: Decompose each layer by its axes of change and introduce intermediate API components (e.g., Language API, TextDelivery API) where independent variation is likely.

## When To Apply

Load this page when:

- Use this when designing a system where a core component (e.g., business logic) must remain unchanged while multiple implementations of a surrounding layer (e.g., multiple UIs or storage backends) are swapped in.
- Use this when a component is growing friction—changes to one part of the system unexpectedly require changes elsewhere—indicating a missing architectural boundary.
- Use this when deciding whether to introduce an interface or abstraction layer between two components that currently communicate directly.
- Use this when a system needs to scale to multiple delivery mechanisms (shell, SMS, chat, network) for the same underlying logic.
- Use this when refactoring a monolith and identifying which internal seams should become explicit API boundaries versus which can remain informal module boundaries.
- Use this when evaluating a micro-service split: determine if the candidate split corresponds to a genuine axis-of-change boundary (e.g., local move management vs. server-side player management).
- Use this when generating scaffolding or architecture for a new system and needing to decide how many layers and interfaces to create initially versus defer.

## Concrete Examples

- Hunt the Wumpus (1972) text adventure game used as a proxy for a large system: decomposed into GameRules, Language API (English/Spanish), TextDelivery (shell/SMS), and DataStorage (flash/cloud/RAM) with dual data streams.
- Revised Hunt the Wumpus with a Network component added to support multiplayer, splitting data flow into three streams all controlled by GameRules.
- MoveManagement vs. PlayerManagement split: MoveManagement runs locally on the player's computer while PlayerManagement is a remote micro-service, illustrating a full architectural boundary between two parts of what was originally one GameRules component.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Layers and Boundaries**

An LLM coding agent defaults to generating the simplest flat structure (UI + logic + DB) or, conversely, over-engineers every possible abstraction upfront because it lacks the temporal observation that triggers the inflection-point decision. The agent cannot 'watch the system evolve' and notice friction signals, so it must be explicitly prompted with current friction evidence or future variation axes before deciding boundary placement. Without this, the agent will either collapse all boundaries (producing a hard-to-extend monolith) or introduce gratuitous interface layers for every function, both of which are the anti-patterns this chapter warns against.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Dependency Rule The

# Dependency Rule: The overriding rule that source code dependencies must point only inward, toward higher-level policies, so nothing in an inner circle can know anything about an outer circle

> From chapter: *Chapter 22: The Clean Architecture*

## Core Principle

The Clean Architecture unifies Hexagonal, DCI, and BCE approaches into a single concentric-layer model governed by one absolute rule: all source code dependencies must point inward toward higher-level policy, never outward. The four canonical layers — Entities, Use Cases, Interface Adapters, and Frameworks/Drivers — are crossed only via simple data structures and Dependency Inversion, ensuring business rules are testable and completely independent of databases, UIs, and frameworks. The payoff is that any external component can be replaced with minimal disruption to the core system.

## Key Heuristics

These are the load-bearing rules for this concept.

> Source code dependencies must point only inward, toward higher-level policies.

> Nothing in an inner circle can know anything at all about something in an outer circle.

> The name of something declared in an outer circle must not be mentioned by the code in an inner circle.

> When we pass data across a boundary, it is always in the form that is most convenient for the inner circle.

> The web is a detail. The database is a detail. We keep these things on the outside where they can do little harm.

> The innermost circle is the most general and highest level.

> By separating the software into layers and conforming to the Dependency Rule, you will create a system that is intrinsically testable.

## Anti-Patterns & Fixes

- Passing Row Structures Inward: Returning a database framework's native row/result object and passing it into inner layers, which forces inner circles to know about outer-circle data formats. Fix: Convert database results into simple, self-contained data structures before crossing the boundary inward.
- Direct Use Case to Presenter Call: A use case directly calling a presenter by name, which names an outer-circle entity inside an inner circle, violating the Dependency Rule. Fix: Define a 'use case output port' interface in the inner circle and have the presenter implement it via Dependency Inversion.
- Framework-Coupled Business Rules: Embedding business logic inside framework constructs (e.g., Rails models, Spring beans) so that entities cannot exist without the framework. Fix: Keep entities as plain objects with no framework imports; treat frameworks as tools in the outermost layer only.
- SQL Leaking Into Use Cases: Writing SQL queries or importing database libraries in the use case or entity layers. Fix: Restrict all SQL and persistence code to the Interface Adapters layer behind a DataAccessInterface abstraction.
- Passing Entity Objects Across Boundaries: Sending full Entity objects across architectural boundaries, coupling outer layers to inner-layer structures. Fix: Construct simple data transfer objects or plain structs containing only the data needed by the receiving layer.

## When To Apply

Load this page when:

- Use this when designing a new system and deciding how to organize code into packages, modules, or services so that business logic is not coupled to a framework.
- Use this when a use case needs to trigger a presenter or view update without the use case layer naming or importing any UI class.
- Use this when swapping a database engine (e.g., SQL to MongoDB) and needing to ensure business rules require zero changes.
- Use this when writing unit tests for business logic and needing to isolate rules from web servers, databases, and external APIs.
- Use this when a framework upgrade is breaking business logic, indicating that business rules were improperly coupled to framework internals.
- Use this when determining where in the codebase to place MVC components, SQL queries, or external API adapters.
- Use this when deciding what data shape to pass between a controller, a use case interactor, and a presenter in a web application.
- Use this when an external service or library becomes obsolete and you need to replace it with minimal impact on the rest of the system.

## Concrete Examples

- A web-based Java system where the Controller packages input into a plain Java object, passes it through InputBoundary to UseCaseInteractor, which calls DataAccessInterface and Entities, then passes OutputData through OutputBoundary to the Presenter, which builds a ViewModel of Strings and flags for the View.
- A use case that needs to call a presenter uses a 'use case output port' interface declared in the inner circle, with the outer-circle Presenter implementing that interface, so the dependency points inward despite the flow of control pointing outward.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 22: The Clean Architecture**

An LLM coding agent is highly prone to violating the Dependency Rule because it generates code by pattern-matching common framework idioms, which typically embed database models, ORM rows, or framework annotations directly into business logic. Without explicit architectural constraints, an agent will naturally produce the shortest path — e.g., passing a Django ORM object straight into a use case function — creating hidden coupling that is invisible in a single generation pass but catastrophic at replacement time. Agents should be instructed to define boundary interfaces and DTOs explicitly before generating any cross-layer calls, treating the Dependency Rule as a hard lint constraint rather than a stylistic preference.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->


## Dependency Rule in

# Dependency Rule in Component Graphs: Ensure all cross-boundary dependencies point toward higher-level policy components; use OCP (open arrows with flow, closed inheritance arrows against flow) to enforce this

> From chapter: *Chapter 33: Case Study: Video Sales*

## Core Principle

This chapter applies SRP and the Dependency Rule to a concrete video-sales system by first identifying four actors as the primary sources of change, then partitioning components so each actor's code is isolated, and finally structuring dependencies so all cross-boundary arrows point toward higher-level policy. Component granularity is established at the build level for maximum flexibility, while deployment grouping remains a separate, adjustable decision. The two axes of separation — actor identity and policy level — together ensure that changes in one part of the system do not ripple unpredictably into others.

## Key Heuristics

These are the load-bearing rules for this concept.

> According to the Single Responsibility Principle, these four actors will be the four primary sources of change for the system.

> We want to partition the system such that a change to one actor does not affect any of the other actors.

> All dependencies cross the boundary lines in one direction, and they always point toward the components containing the higher-level policy.

> The using relationships (open arrows) point with the flow of control, and the inheritance relationships (closed arrows) point against the flow of control.

> I would certainly break the compile and build environment up this way, so that I could build independent deliverables like that. I would also reserve the right to combine all those deliverables into a smaller number of deliverables if necessary.

> Once you have structured the code this way, you can mix and match how you want to actually deploy the system.

> The different reasons correspond to the actors; the different rates correspond to the different levels of policy.

## Anti-Patterns & Fixes

- MonolithicActorBlob: Mixing code that serves different actors in the same component so that a change for one actor (e.g., Viewer pricing logic) forces redeployment or risks breaking another actor (e.g., Admin catalog management). Fix: Partition components per actor at the compile/build level, even if you later combine them into coarser deployment units.
- PrematureDeploymentCollapsing: Deciding too early to ship everything as one deployable, losing the ability to independently deploy components that change at different rates. Fix: Build at fine-grained component granularity first; only merge deliverables as a deliberate, reversible deployment decision.
- SkippingAbstractUseCases: Duplicating nearly identical use case logic (e.g., View Catalog as Viewer vs. View Catalog as Purchaser) instead of recognizing shared structure. Fix: Introduce an abstract use case and corresponding abstract classes in a shared component; concrete use cases inherit and extend.
- DependencyDirectionViolation: Allowing low-level detail components (views, controllers) to be depended upon by high-level policy components (interactors), causing detail changes to ripple into business rules. Fix: Apply the Dependency Rule — all cross-boundary arrows must point toward higher-level policy; use inheritance inversion (OCP) where flow of control opposes the required dependency direction.
- IncompleteActorIdentification: Beginning component design before identifying all primary actors, leading to partitions that do not align with real sources of change. Fix: Perform explicit use-case analysis first, name all actors, then derive component boundaries from those actors.

## When To Apply

Load this page when:

- Use this when designing the initial architecture of a multi-stakeholder system and you need to decide how to partition components.
- Use this when two use cases appear nearly identical and you must decide whether to unify them or keep them separate.
- Use this when choosing how many .jar/.dll/.whl deployment artifacts to produce from a codebase that has already been logically partitioned.
- Use this when a change requested by one user role (e.g., business license pricing) risks breaking or requiring redeployment of code used by a different role (e.g., individual streaming).
- Use this when drawing or reviewing a component dependency diagram to verify that all arrows across architectural boundaries point toward higher-level policy.
- Use this when scaffolding a new feature and you need to determine which existing component it belongs to based on which actor it serves.
- Use this when refactoring a system that has grown monolithic and you need a principled way to identify seams for splitting it.

## Concrete Examples

- A video sales website (modeled on cleancoders.com) with four actors — Viewer, Purchaser, Author, and Administrator — each with distinct use cases such as streaming/downloading videos, uploading content, and managing catalog and pricing.
- View Catalog as Viewer and View Catalog as Purchaser both inherit from an abstract View Catalog use case, implemented as abstract classes in a shared Catalog View / Catalog Presenter component.
- A preliminary component architecture (Figure 33.2) partitioned into per-actor views, presenters, interactors, and controllers, each as a potential separate .jar or .dll, with options to merge into 5, 3, or 2 deployment artifacts.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 33: Case Study: Video Sales**

An LLM coding agent, when asked to implement a feature, will typically generate code into the most convenient existing file or class rather than respecting actor-based component boundaries — silently coupling, say, Viewer logic with Admin logic. This chapter's actor-partitioning discipline gives the agent an explicit decision rule: before writing any code, identify which actor the feature serves and place it in that actor's component. Additionally, agents tend to flatten dependency graphs (importing whatever is convenient), so the Dependency Rule must be stated as a hard constraint in the agent's instructions to prevent low-level detail modules from being imported by high-level policy modules.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

