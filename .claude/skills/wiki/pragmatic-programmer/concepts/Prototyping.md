---
title: Prototyping
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 7 pages
---

# Prototyping

> Consolidated from 7 related concept pages.

---

## Architectural Prototyping Use non code artifacts Post it notes whiteboards index

## Core Principle

Prototyping is a risk-reduction technique where cheap, incomplete, and deliberately limited artifacts—code or non-code—are built to answer specific questions and expose unknowns before committing to full implementation. The value is in the lessons learned, not the artifact produced, so details like correctness, robustness, and style are intentionally ignored. The critical discipline is ensuring all stakeholders understand prototype code is disposable; if that contract cannot hold, tracer bullets are the correct alternative.

## Key Heuristics

These are the load-bearing rules for this concept.

> Prototype to Learn

> Its value lies not in the code produced, but in the lessons learned.

> Prototypes can be deceptively attractive to people who don't know that they are just prototypes.

> You must make it very clear that this code is disposable, incomplete, and unable to be completed.

> You can build a great prototype of a new car out of balsa wood and duct tape, but you wouldn't try to drive it in rush-hour traffic.

> Anything that carries risk. Anything that hasn't been tried before, or that is absolutely critical to the final system. Anything unproven, experimental, or doubtful.

> If you find yourself in an environment where you cannot give up the details, then you need to ask yourself if you are really building a prototype at all.

## Anti-Patterns & Fixes

- Prototype Promotion: Stakeholders or management insist on deploying prototype code because it looks complete. Fix: Explicitly label prototypes as disposable before writing a single line; use tracer bullets instead if the culture cannot accept throwaway code.
- Detail-Laden Prototyping: Adding correctness, robustness, style, and completeness to a prototype defeats its purpose and wastes time. Fix: Deliberately ignore unimportant details—use dummy data, skip error handling, omit comments—and focus only on the specific question being answered.
- Code-Only Prototyping: Defaulting to code when the question is architectural or workflow-related. Fix: Use Post-it notes, whiteboards, or index cards to prototype architecture and dynamic logic without writing code.
- Wrong Tool for the Job: Using a prototype when the system requires production-quality incremental growth. Fix: Switch to tracer bullet development when details cannot be deferred or the codebase needs a solid framework to build upon.
- Language Mismatch in Prototyping: Using the production language for a prototype adds unnecessary overhead. Fix: Use a high-level scripting language to defer details and accelerate exploration.

## When To Apply

Load this page when:

- Use this when facing an architectural decision where component responsibilities, coupling, or data access paths are unclear before implementation begins.
- Use this when integrating a third-party tool, library, or external data source whose behavior is unproven in your context.
- Use this when a performance or computational approach is uncertain and needs validation before building full infrastructure around it.
- Use this when designing a user interface and needing stakeholder feedback before committing to implementation.
- Use this when a feature involves risk or is being attempted for the first time in the codebase.
- Use this when asked to generate a large block of speculative code—consider generating a minimal prototype targeting only the uncertain aspect instead.
- Use this when a project sponsor or non-technical stakeholder is likely to see generated code and may mistake exploratory output for production-ready deliverables.

## Concrete Examples

- Car manufacturers building clay models for wind tunnel testing and balsa wood models for art department review—each prototype tests one specific aspect.
- Post-it notes on a whiteboard used to prototype workflow and application logic without writing code.
- Architectural prototype using index cards or Post-it notes to evaluate component responsibilities, coupling, and data access paths across a whole system.
- Using Perl, Python, or Tcl as a high-level scripting language to prototype functionality faster than the production language allows.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Prototypes and Post-it Notes**

An LLM coding agent is prone to the Prototype Promotion anti-pattern at scale: generated code looks syntactically complete and confident, making it far more likely that consumers treat exploratory output as production-ready than they would a human's rough sketch. Additionally, an agent has no inherent cost pressure—it generates full implementations as easily as stubs—so it must explicitly be instructed to defer correctness, robustness, and style when the goal is learning, or it will default to over-engineering the prototype. Agents should tag all exploratory code outputs with explicit disposability markers and scope-limit generation to only the uncertain component being probed.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Disposable Code Contract Establish explicit shared understanding with all stakeh

## Core Principle

Prototyping is a risk-reduction technique where cheap, incomplete, and deliberately limited artifacts—code or non-code—are built to answer specific questions and expose unknowns before committing to full implementation. The value is in the lessons learned, not the artifact produced, so details like correctness, robustness, and style are intentionally ignored. The critical discipline is ensuring all stakeholders understand prototype code is disposable; if that contract cannot hold, tracer bullets are the correct alternative.

## Key Heuristics

These are the load-bearing rules for this concept.

> Prototype to Learn

> Its value lies not in the code produced, but in the lessons learned.

> Prototypes can be deceptively attractive to people who don't know that they are just prototypes.

> You must make it very clear that this code is disposable, incomplete, and unable to be completed.

> You can build a great prototype of a new car out of balsa wood and duct tape, but you wouldn't try to drive it in rush-hour traffic.

> Anything that carries risk. Anything that hasn't been tried before, or that is absolutely critical to the final system. Anything unproven, experimental, or doubtful.

> If you find yourself in an environment where you cannot give up the details, then you need to ask yourself if you are really building a prototype at all.

## Anti-Patterns & Fixes

- Prototype Promotion: Stakeholders or management insist on deploying prototype code because it looks complete. Fix: Explicitly label prototypes as disposable before writing a single line; use tracer bullets instead if the culture cannot accept throwaway code.
- Detail-Laden Prototyping: Adding correctness, robustness, style, and completeness to a prototype defeats its purpose and wastes time. Fix: Deliberately ignore unimportant details—use dummy data, skip error handling, omit comments—and focus only on the specific question being answered.
- Code-Only Prototyping: Defaulting to code when the question is architectural or workflow-related. Fix: Use Post-it notes, whiteboards, or index cards to prototype architecture and dynamic logic without writing code.
- Wrong Tool for the Job: Using a prototype when the system requires production-quality incremental growth. Fix: Switch to tracer bullet development when details cannot be deferred or the codebase needs a solid framework to build upon.
- Language Mismatch in Prototyping: Using the production language for a prototype adds unnecessary overhead. Fix: Use a high-level scripting language to defer details and accelerate exploration.

## When To Apply

Load this page when:

- Use this when facing an architectural decision where component responsibilities, coupling, or data access paths are unclear before implementation begins.
- Use this when integrating a third-party tool, library, or external data source whose behavior is unproven in your context.
- Use this when a performance or computational approach is uncertain and needs validation before building full infrastructure around it.
- Use this when designing a user interface and needing stakeholder feedback before committing to implementation.
- Use this when a feature involves risk or is being attempted for the first time in the codebase.
- Use this when asked to generate a large block of speculative code—consider generating a minimal prototype targeting only the uncertain aspect instead.
- Use this when a project sponsor or non-technical stakeholder is likely to see generated code and may mistake exploratory output for production-ready deliverables.

## Concrete Examples

- Car manufacturers building clay models for wind tunnel testing and balsa wood models for art department review—each prototype tests one specific aspect.
- Post-it notes on a whiteboard used to prototype workflow and application logic without writing code.
- Architectural prototype using index cards or Post-it notes to evaluate component responsibilities, coupling, and data access paths across a whole system.
- Using Perl, Python, or Tcl as a high-level scripting language to prototype functionality faster than the production language allows.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Prototypes and Post-it Notes**

An LLM coding agent is prone to the Prototype Promotion anti-pattern at scale: generated code looks syntactically complete and confident, making it far more likely that consumers treat exploratory output as production-ready than they would a human's rough sketch. Additionally, an agent has no inherent cost pressure—it generates full implementations as easily as stubs—so it must explicitly be instructed to defer correctness, robustness, and style when the goal is learning, or it will default to over-engineering the prototype. Agents should tag all exploratory code outputs with explicit disposability markers and scope-limit generation to only the uncertain component being probed.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Prototype Over Diagram Validation Prefer showing users a working prototype over

## Core Principle

Formal development methodologies (UML, waterfall, CASE tools, etc.) are tools to be used selectively and critically, not authorities to obey blindly — their diagrams are designers' interpretations, not verified requirements, and their adoption always carries a real productivity cost. Pragmatic developers extract the best elements from multiple methods, prefer working prototypes over formal diagrams for validation, and continuously refine their process rather than accepting any methodology's rigid confines as limits. Expensive tools and elaborate diagrams do not guarantee better designs; the developers wielding them are still fallible.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Be a Slave to Formal Methods

> Expensive Tools Do Not Produce Better Designs

> Never become a slave to a methodology: circles and arrows make poor masters.

> Blindly adopting any technique without putting it into the context of your development practices and capabilities is a recipe for disappointment.

> Never underestimate the cost of adopting new tools and methods. Be prepared to treat the first projects using these techniques as a learning experience.

> Never accept the rigid confines of a methodology as the limits of your world.

> All that paper is still just their fallible interpretation of requirements and design.

> If the philosophy is 'the class diagram is the application, the rest is mechanical coding,' you know you're looking at a waterlogged project team.

## Anti-Patterns & Fixes

- Methodology Worship: Treating a formal method (UML, waterfall, etc.) as authoritative truth rather than one tool among many, causing teams to follow diagrams that no longer reflect reality. Fix: Adopt methods critically, extract useful parts, and override the method when your context demands it.
- Diagram-as-Requirement Fallacy: Using formal diagrams (class diagrams, use cases) as a substitute for validated user requirements, when users cannot read or verify them. Fix: Show users working prototypes to gather real feedback instead of relying on designer-interpreted diagrams.
- Specialization Silo Trap: Formal methods encouraging separate groups for data modeling, architecture, and requirements gathering, leading to poor communication and wasted effort. Fix: Ensure team members understand how all components interact, where data lives, and what requirements are.
- Static Model Bias: Formal methods pushing developers toward static object/data relationships that inhibit the dynamic, metadata-driven systems good software requires. Fix: Prefer designing adaptable, dynamic systems using metadata to allow runtime behavior changes.
- Driftwood Chasing: Latching onto the latest methodology fad as a solution to struggling projects without addressing the underlying development problems. Fix: Diagnose root causes of project failure rather than switching methodologies; refine existing practices incrementally.
- Tool Cost Bias: Overvaluing output from expensive tools simply because of their cost. Fix: Evaluate tool output on its own merits, completely independent of what the tool cost.

## When To Apply

Load this page when:

- Use this when a team proposes adopting a new formal methodology (UML, CASE tools, etc.) mid-project as a fix for struggling delivery.
- Use this when evaluating whether to generate or follow a formal class diagram or architecture diagram as the primary specification for implementation.
- Use this when a stakeholder presents extensive formal documentation (use case diagrams, ER diagrams) and expects the agent to treat it as ground truth for requirements.
- Use this when deciding how much weight to give to an expensive or prestigious modeling tool's output versus direct user feedback.
- Use this when a project's process feels rigidly locked to a single methodology and is failing to adapt to emerging information.
- Use this when asked to implement a system described entirely by static object models without consideration for runtime flexibility or metadata-driven behavior.
- Use this when assessing the trade-off between adopting a new structured approach versus the productivity cost during the learning and adoption period.

## Concrete Examples

- Historical parade of methodologies: structured programming, chief programmer teams, CASE tools, waterfall, spiral model, Jackson, ER diagrams, Booch clouds, OMT, Objectory, Coad/Yourdon, and UML — each enjoying temporary popularity before replacement.
- Robert Glass's 1999 CACM article reviewing productivity/quality research across seven software development technologies (4GLs, structured techniques, CASE tools, formal methods, clean room, process models, OO), finding initial hype overblown and benefits delayed by adoption productivity drops.
- The shipwreck/driftwood metaphor: developers on failing projects swimming from one methodology fad to the next, remaining adrift regardless of which piece of flotsam they grab.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Circles and Arrows**

An LLM coding agent is particularly susceptible to treating any formal schema, diagram description, or structured specification handed to it as authoritative ground truth, effectively becoming a slave to whatever artifact it was given — the agent equivalent of 'the class diagram is the application.' This prevents the agent from questioning whether the diagram reflects actual user needs, detecting static model bias in the spec, or flagging that a dynamically configurable design would be superior. Applying this chapter, an agent should treat input specifications as one fallible interpretation to reason about critically, not as a verified contract to implement mechanically.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Prototype Speed Multiplier Text manipulation languages provide a 5 10x developme

## Core Principle

Text manipulation languages (Perl, Python, Ruby, awk, sed) are general-purpose power tools that let developers generate multiple artifacts from a single source, automate repetitive transformations, and prototype ideas at 5-10x the speed of conventional languages. The core discipline is applying the DRY principle through generation: one canonical definition produces SQL, code, docs, and config automatically, eliminating manual synchronization. Mastery of at least one such language is a force multiplier that makes an entire class of otherwise tedious or risky tasks fast and reliable.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 28: Learn a Text Manipulation Language

> Spending 30 minutes trying out a crazy idea is a whole lot better than spending five hours.

> Text manipulation languages are to programming what routers are to woodworking. They are noisy, messy, and somewhat brute force.

> Used properly, these tools have surprising finesse and subtlety. But they take time to master.

> These languages are important enabling technologies. Using them, you can quickly hack up utilities and prototype ideas—jobs that might take five or ten times as long using conventional languages.

## Anti-Patterns & Fixes

- Manual Multi-Artifact Synchronization: Maintaining SQL schema, C libraries, docs, and XML separately leads to drift and inconsistency. Fix: Generate all artifacts from a single canonical text source using a script, so changes propagate automatically.
- Copy-Paste Code into Docs: Duplicating code snippets into documentation virtually guarantees stale examples when source changes. Fix: Use a script to extract named segments directly from tested source files at format/build time.
- Manual Boilerplate Generation: Writing repetitive get/set methods by hand is tedious and error-prone. Fix: Use a text manipulation script to parse source files and auto-insert the correct method definitions for flagged variables.
- Overengineering Quick Transformations: Using a conventional compiled language for one-off data transformations multiplies effort 5-10x unnecessarily. Fix: Reach for a scripting/text-manipulation language for data conversion, prototyping, and glue tasks.

## When To Apply

Load this page when:

- Use this when you need to generate multiple different artifacts (SQL, code, docs, config) from a single source definition and want to keep them in sync.
- Use this when you need to transform or reformat large volumes of test or production data across multiple files and formats into a target schema.
- Use this when boilerplate code (e.g., accessors, interface bindings, wrappers) must be regenerated every time a header or schema changes.
- Use this when you want to extract, highlight, and embed live tested code snippets into documentation without manual copy-paste.
- Use this when prototyping or validating a crazy idea quickly and a 5-hour conventional implementation would kill the experiment.
- Use this when bridging two language ecosystems (e.g., C headers to Pascal units) requires parsing one language's constructs and emitting another's.
- Use this when generating HTML or structured documentation from source artifacts like database schemas, makefiles, or source code.

## Concrete Examples

- Perl scripts generated SQL DDL, flat data dictionary files, C libraries, integrity-check scripts, web pages, and XML all from a single plain-text database schema definition.
- A Perl script parsed Java source files and inserted get/set method definitions for all appropriately flagged member variables automatically.
- Perl knitted together tens of thousands of test data records from multiple files and formats into a relational database load format in a couple of hours, also surfacing consistency errors.
- A Perl script invoked at book-formatting time extracted named code segments from tested source files, applied syntax highlighting, and converted them to the typesetting language—enforcing DRY between book and code.
- A Perl script parsed C header files and generated Object Pascal units with record types and imported procedure definitions, integrated into the build so Pascal units auto-updated when C headers changed.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**19. Text Manipulation**

An LLM coding agent can apply this chapter's principles by defaulting to script-based generation pipelines instead of emitting redundant artifacts separately—since agents are prone to generating multiple out-of-sync artifacts (schema, DTO, docs) in one shot with no link between them. The DRY-via-Generation pattern is especially critical for agents: rather than regenerating all downstream files from scratch on each invocation (risking drift), an agent should write and invoke a canonical generator script so the build itself enforces consistency. Agents also tend to over-engineer quick transformations into full programs; recognizing the 'prototype-speed multiplier' trigger should cause an agent to emit a short transformation script rather than a class hierarchy.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Prototype as Diagnostic Using a quick proof of concept on the most uncertain are

## Core Principle

Experienced developers have trained subconscious instincts that manifest as nagging doubt before a flawed start; these signals should be respected rather than overridden. The practical technique for distinguishing genuine blocking concerns from procrastination is to prototype the most uncertain area: boredom signals procrastination, while a moment of revelation signals a real foundational problem. The goal is to surface wrong premises cheaply before committing to full development.

## Key Heuristics

These are the load-bearing rules for this concept.

> Listen to Nagging Doubts—Start When You're Ready

> He who hesitates is sometimes saved.

> If you sit down to start typing and there's some nagging doubt in your mind, heed it.

> Software development is still not a science. Let your instincts contribute to your performance.

> When you feel a nagging doubt, or experience some reluctance when faced with a task, heed it.

> The last thing you want is to find yourself several weeks into serious development before remembering that you started out writing a prototype.

## Anti-Patterns & Fixes

- BlindStarting: Ignoring nagging doubts and diving into full development, causing wasted effort when a flawed premise is discovered late. Fix: Prototype the uncertain area first to surface fundamental issues early.
- ProcastinationMisread: Treating all hesitation as laziness and forcing a start, missing valid instinctual warnings. Fix: Use the prototype test — if you feel bored quickly, it was procrastination; if you hit a revelation, it was a real concern.
- PrototypeDrift: Beginning a prototype to investigate unease but drifting into treating it as real development, wasting weeks. Fix: Explicitly label and time-box prototypes; abandon them intentionally once the diagnostic purpose is served.
- AnnouncingUnease Without Evidence: Declaring 'I don't feel right about starting' with no tangible output, which is politically unacceptable and unproductive. Fix: Channel the unease into a concrete prototype that can surface actual problems.

## When To Apply

Load this page when:

- Use this when you are about to generate a large implementation but something about the requirements feels underspecified or contradictory.
- Use this when asked to scaffold a new module or project and the architecture or domain model is not yet clear.
- Use this when a task feels straightforward but edge cases or constraints keep surfacing during planning, suggesting a hidden premise is wrong.
- Use this when you have been given a specification and you cannot immediately identify a clean decomposition or starting point.
- Use this when the scope of a request is ambiguous and starting full implementation risks building in the wrong direction for many steps.
- Use this when you feel pressure to produce output quickly but lack confidence that the foundational approach is correct.

## Concrete Examples

- A diver on the high-board waiting for the perfect moment to jump, illustrating readiness calibration before committing.
- A conductor holding raised arms before the orchestra, waiting to sense the right moment to begin the piece.
- 'Inner tennis' coaching: hitting balls while verbalizing where they land relative to a target chair, training subconscious reflexes without conscious understanding — used as an analogy for accumulated developer instinct.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Not Until You're Ready**

An LLM agent lacks the human experience of accumulated instinct but can simulate readiness calibration by explicitly checking for specification gaps, contradictory constraints, or unclear success criteria before generating code — treating these as programmatic 'nagging doubts.' The key agent failure mode this prevents is confident hallucination: agents tend to fill underspecified gaps with plausible-sounding assumptions and proceed at full speed, producing large amounts of coherent but fundamentally wrong code. Applying the prototype-as-diagnostic pattern, an agent should generate a minimal proof-of-concept or ask targeted clarifying questions before committing to a full implementation path.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Prototype to Learn Build cheap disposable artifacts targeting specific risky or

## Core Principle

Prototyping is a risk-reduction technique where cheap, incomplete, and deliberately limited artifacts—code or non-code—are built to answer specific questions and expose unknowns before committing to full implementation. The value is in the lessons learned, not the artifact produced, so details like correctness, robustness, and style are intentionally ignored. The critical discipline is ensuring all stakeholders understand prototype code is disposable; if that contract cannot hold, tracer bullets are the correct alternative.

## Key Heuristics

These are the load-bearing rules for this concept.

> Prototype to Learn

> Its value lies not in the code produced, but in the lessons learned.

> Prototypes can be deceptively attractive to people who don't know that they are just prototypes.

> You must make it very clear that this code is disposable, incomplete, and unable to be completed.

> You can build a great prototype of a new car out of balsa wood and duct tape, but you wouldn't try to drive it in rush-hour traffic.

> Anything that carries risk. Anything that hasn't been tried before, or that is absolutely critical to the final system. Anything unproven, experimental, or doubtful.

> If you find yourself in an environment where you cannot give up the details, then you need to ask yourself if you are really building a prototype at all.

## Anti-Patterns & Fixes

- Prototype Promotion: Stakeholders or management insist on deploying prototype code because it looks complete. Fix: Explicitly label prototypes as disposable before writing a single line; use tracer bullets instead if the culture cannot accept throwaway code.
- Detail-Laden Prototyping: Adding correctness, robustness, style, and completeness to a prototype defeats its purpose and wastes time. Fix: Deliberately ignore unimportant details—use dummy data, skip error handling, omit comments—and focus only on the specific question being answered.
- Code-Only Prototyping: Defaulting to code when the question is architectural or workflow-related. Fix: Use Post-it notes, whiteboards, or index cards to prototype architecture and dynamic logic without writing code.
- Wrong Tool for the Job: Using a prototype when the system requires production-quality incremental growth. Fix: Switch to tracer bullet development when details cannot be deferred or the codebase needs a solid framework to build upon.
- Language Mismatch in Prototyping: Using the production language for a prototype adds unnecessary overhead. Fix: Use a high-level scripting language to defer details and accelerate exploration.

## When To Apply

Load this page when:

- Use this when facing an architectural decision where component responsibilities, coupling, or data access paths are unclear before implementation begins.
- Use this when integrating a third-party tool, library, or external data source whose behavior is unproven in your context.
- Use this when a performance or computational approach is uncertain and needs validation before building full infrastructure around it.
- Use this when designing a user interface and needing stakeholder feedback before committing to implementation.
- Use this when a feature involves risk or is being attempted for the first time in the codebase.
- Use this when asked to generate a large block of speculative code—consider generating a minimal prototype targeting only the uncertain aspect instead.
- Use this when a project sponsor or non-technical stakeholder is likely to see generated code and may mistake exploratory output for production-ready deliverables.

## Concrete Examples

- Car manufacturers building clay models for wind tunnel testing and balsa wood models for art department review—each prototype tests one specific aspect.
- Post-it notes on a whiteboard used to prototype workflow and application logic without writing code.
- Architectural prototype using index cards or Post-it notes to evaluate component responsibilities, coupling, and data access paths across a whole system.
- Using Perl, Python, or Tcl as a high-level scripting language to prototype functionality faster than the production language allows.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Prototypes and Post-it Notes**

An LLM coding agent is prone to the Prototype Promotion anti-pattern at scale: generated code looks syntactically complete and confident, making it far more likely that consumers treat exploratory output as production-ready than they would a human's rough sketch. Additionally, an agent has no inherent cost pressure—it generates full implementations as easily as stubs—so it must explicitly be instructed to defer correctness, robustness, and style when the goal is learning, or it will default to over-engineering the prototype. Agents should tag all exploratory code outputs with explicit disposability markers and scope-limit generation to only the uncertain component being probed.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Prototype vs Tracer Bullet Distinction Prototypes are throwaway explorations tha

## Core Principle

Prototyping is a risk-reduction technique where cheap, incomplete, and deliberately limited artifacts—code or non-code—are built to answer specific questions and expose unknowns before committing to full implementation. The value is in the lessons learned, not the artifact produced, so details like correctness, robustness, and style are intentionally ignored. The critical discipline is ensuring all stakeholders understand prototype code is disposable; if that contract cannot hold, tracer bullets are the correct alternative.

## Key Heuristics

These are the load-bearing rules for this concept.

> Prototype to Learn

> Its value lies not in the code produced, but in the lessons learned.

> Prototypes can be deceptively attractive to people who don't know that they are just prototypes.

> You must make it very clear that this code is disposable, incomplete, and unable to be completed.

> You can build a great prototype of a new car out of balsa wood and duct tape, but you wouldn't try to drive it in rush-hour traffic.

> Anything that carries risk. Anything that hasn't been tried before, or that is absolutely critical to the final system. Anything unproven, experimental, or doubtful.

> If you find yourself in an environment where you cannot give up the details, then you need to ask yourself if you are really building a prototype at all.

## Anti-Patterns & Fixes

- Prototype Promotion: Stakeholders or management insist on deploying prototype code because it looks complete. Fix: Explicitly label prototypes as disposable before writing a single line; use tracer bullets instead if the culture cannot accept throwaway code.
- Detail-Laden Prototyping: Adding correctness, robustness, style, and completeness to a prototype defeats its purpose and wastes time. Fix: Deliberately ignore unimportant details—use dummy data, skip error handling, omit comments—and focus only on the specific question being answered.
- Code-Only Prototyping: Defaulting to code when the question is architectural or workflow-related. Fix: Use Post-it notes, whiteboards, or index cards to prototype architecture and dynamic logic without writing code.
- Wrong Tool for the Job: Using a prototype when the system requires production-quality incremental growth. Fix: Switch to tracer bullet development when details cannot be deferred or the codebase needs a solid framework to build upon.
- Language Mismatch in Prototyping: Using the production language for a prototype adds unnecessary overhead. Fix: Use a high-level scripting language to defer details and accelerate exploration.

## When To Apply

Load this page when:

- Use this when facing an architectural decision where component responsibilities, coupling, or data access paths are unclear before implementation begins.
- Use this when integrating a third-party tool, library, or external data source whose behavior is unproven in your context.
- Use this when a performance or computational approach is uncertain and needs validation before building full infrastructure around it.
- Use this when designing a user interface and needing stakeholder feedback before committing to implementation.
- Use this when a feature involves risk or is being attempted for the first time in the codebase.
- Use this when asked to generate a large block of speculative code—consider generating a minimal prototype targeting only the uncertain aspect instead.
- Use this when a project sponsor or non-technical stakeholder is likely to see generated code and may mistake exploratory output for production-ready deliverables.

## Concrete Examples

- Car manufacturers building clay models for wind tunnel testing and balsa wood models for art department review—each prototype tests one specific aspect.
- Post-it notes on a whiteboard used to prototype workflow and application logic without writing code.
- Architectural prototype using index cards or Post-it notes to evaluate component responsibilities, coupling, and data access paths across a whole system.
- Using Perl, Python, or Tcl as a high-level scripting language to prototype functionality faster than the production language allows.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Prototypes and Post-it Notes**

An LLM coding agent is prone to the Prototype Promotion anti-pattern at scale: generated code looks syntactically complete and confident, making it far more likely that consumers treat exploratory output as production-ready than they would a human's rough sketch. Additionally, an agent has no inherent cost pressure—it generates full implementations as easily as stubs—so it must explicitly be instructed to defer correctness, robustness, and style when the goal is learning, or it will default to over-engineering the prototype. Agents should tag all exploratory code outputs with explicit disposability markers and scope-limit generation to only the uncertain component being probed.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
