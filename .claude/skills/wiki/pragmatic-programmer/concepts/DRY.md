---
title: DRY
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 8 pages
---

# DRY

> Consolidated from 8 related concept pages.

---

## DRY Orthogonality Duality DRY minimizes duplication within a system orthogonalit

## Core Principle

Orthogonality means designing components so that changes in one have zero effect on others — independence and decoupling as explicit goals, not accidental outcomes. Orthogonal systems yield multiplicative productivity gains, localized bug containment, easier testing, and reduced vendor lock-in. The principle applies equally to code structure, team organization, toolkit selection, and documentation, and is best enforced by asking: how many modules must change for a single requirement change?

## Key Heuristics

These are the load-bearing rules for this concept.

> Eliminate Effects Between Unrelated Things

> If I dramatically change the requirements behind a particular function, how many modules are affected? In an orthogonal system, the answer should be 'one.'

> When components are isolated from one another, you know that you can change one without having to worry about the rest.

> If a module is sick, it is less likely to spread the symptoms around the rest of the system.

> Building unit tests is itself an interesting test of orthogonality. What does it take to build and link a unit test? Do you have to drag in a large percentage of the rest of the system just to get a test to compile or link?

> Don't rely on the properties of things you can't control.

> Your code is easier to understand and maintain if you explicitly pass any required context into your modules.

> If you use the principle of orthogonality, combined closely with the DRY principle, you'll find that the systems you develop are more flexible, more understandable, and easier to debug, test, and maintain.

## Anti-Patterns & Fixes

- GlobalDataCoupling: Referencing global data ties a component to every other component that shares it, creating hidden dependencies. Fix: Explicitly pass required context as parameters or constructor arguments instead of reading from globals or singletons.
- NonOrthogonalToolkitAdoption: Importing a library that forces you to access or create objects in special ways (e.g., RMI throwing location-aware exceptions everywhere) contaminates your codebase with third-party coupling. Fix: Choose toolkits that are transparent to calling code; isolate third-party interfaces to small boundary layers.
- OverlappingTeamResponsibilities: When multiple team members own the same code area, every change requires a whole-team meeting and creates confusion. Fix: Assign well-defined, non-overlapping responsibilities per subteam; measure orthogonality by counting people needed per change discussion.
- DuplicatedSimilarFunctions: Functions sharing start/end code with different central algorithms indicate structural problems and hidden coupling. Fix: Apply the Strategy pattern to extract the varying algorithm as an injectable component.
- ExternalPropertyAsIdentifier: Using an externally controlled value (e.g., phone number as customer ID) as an internal key couples your schema to outside change. Fix: Use internally controlled identifiers; isolate external identifiers behind an abstraction.
- ScatteredBugFixes: A bug fix that requires changes across multiple modules signals non-orthogonal design. Fix: Refactor to localize responsibility before or during the fix; track fix spread using source control metrics.

## When To Apply

Load this page when:

- Use this when adding a new feature requires modifying more than one unrelated module (e.g., changing a UI button also requires a database schema change).
- Use this when a bug fix causes other unrelated problems to appear elsewhere in the system.
- Use this when writing a unit test requires importing or instantiating a large portion of the rest of the system just to compile.
- Use this when integrating a third-party library that forces callers to handle implementation-specific concerns (e.g., network location, transaction boundaries) throughout the codebase.
- Use this when designing a new module and deciding what state it should own versus receive as parameters.
- Use this when a system needs to support a new interface (e.g., voice response added alongside GUI) and you want to avoid rewriting business logic.
- Use this when refactoring code that has grown complex and where every change seems to require compensating changes elsewhere.
- Use this when evaluating whether a singleton or shared object is appropriate for passing shared state between components.

## Concrete Examples

- Helicopter controls: lowering the collective pitch lever causes nose drop and left spiral, requiring simultaneous compensating inputs on stick and pedals — every control has secondary effects, illustrating non-orthogonal system complexity.
- Heating plant monitoring system: an orthogonal design allows adding voice/touchtone control alongside a GUI by changing only the UI modules, leaving plant-control logic untouched.
- RMI vs CORBA for distributed Java: RMI forces every caller to handle RemoteException (location-aware), violating orthogonality; CORBA hides location from calling code, preserving it.
- EJB transaction metadata: transaction boundaries declared as metadata outside application code, allowing the same code to run in different transaction environments — an orthogonal design for cross-cutting concerns.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Orthogonality**

An LLM coding agent is especially prone to orthogonality violations because it generates code by pattern-matching across the entire visible context, making it natural to reach for global state, copy logic across functions, or wire components together directly rather than through clean interfaces. Unlike a human who feels the pain of tangled code over time, an agent has no such feedback loop — it will confidently produce a deeply coupled system in one pass without noticing the helicopter problem it just created. Applying orthogonality explicitly as a generation constraint (e.g., 'each function may only access state passed to it as arguments'; 'no module may import more than one layer below it') forces the agent to produce components that are testable and changeable in isolation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## DRY Principle Every piece of knowledge must have a single unambiguous authoritat

## Core Principle

Duplication is the root cause of most maintenance failures because knowledge represented in multiple places will inevitably diverge. The DRY principle demands a single authoritative source for every piece of knowledge, whether that knowledge lives in code, documentation, data schemas, or tests. Duplication arises from four distinct causes — imposed constraints, design mistakes, laziness under deadline pressure, and lack of team coordination — each requiring a targeted strategy to eliminate.

## Key Heuristics

These are the load-bearing rules for this concept.

> DRY—Don't Repeat Yourself

> EVERY PIECE OF KNOWLEDGE MUST HAVE A SINGLE, UNAMBIGUOUS, AUTHORITATIVE REPRESENTATION WITHIN A SYSTEM.

> It isn't a question of whether you'll remember: it's a question of when you'll forget.

> Bad code requires lots of comments.

> Keep the low-level knowledge in the code, where it belongs, and reserve the comments for other, high-level explanations.

> Short cuts make for long delays.

> Make It Easy to Reuse

> The trick is to make the process active: this cannot be a one-time conversion, or we're back in a position of duplicating data.

## Anti-Patterns & Fixes

- Commenting What the Code Does: Writing comments that restate the logic of the code creates a duplicate representation of knowledge. Fix: Let the code express the low-level logic; reserve comments for high-level rationale and intent only.
- Derived Data as Stored Fields: Storing a value (e.g., line length) that can be computed from other fields creates a dependency that can fall out of sync. Fix: Make derived values computed properties or methods; cache with a dirty flag if performance requires it.
- Copy-Paste Reuse (Impatient Duplication): Copying a routine or class and modifying it saves seconds but creates divergent maintenance burdens. Fix: Invest time upfront to abstract the shared logic into a reusable component.
- Unnormalized Object Attributes (Interdependency Duplication): Storing the same logical entity (e.g., a driver) in multiple objects means changes must propagate to all holders. Fix: Normalize by identifying the authoritative owner of each piece of knowledge and reference it from other objects.
- Manually Maintained Parallel Representations: Keeping the same structure defined in multiple languages or formats by hand leads to drift. Fix: Generate all representations from a single canonical metadata source using a code generator run at build time.
- Interdeveloper Duplication: Different developers independently implement the same functionality, leading to silent divergence over years. Fix: Appoint a project librarian, maintain a shared utility repository, and foster frequent cross-team communication.

## When To Apply

Load this page when:

- Use this when you are about to define a data field whose value can be calculated from other existing fields in the same class.
- Use this when generating code or data structures in multiple languages or formats that must stay in sync (e.g., client/server shared schema).
- Use this when writing a comment that describes what the next line of code does rather than why it exists.
- Use this when you find yourself copying a function or class to make a slightly modified version instead of parameterizing or abstracting it.
- Use this when a business concept (e.g., a validation rule, a configuration value, a threshold) appears in more than one location in the codebase.
- Use this when documentation and code both describe the same behavior and a change to one requires a manual update to the other.
- Use this when working on a team codebase and about to implement utility functionality without first searching for an existing implementation.
- Use this when a performance optimization requires caching a derived value, to ensure the violation of DRY is localized and encapsulated.

## Concrete Examples

- Line class with a stored `length` field that duplicates information derivable from `start` and `end` points — fixed by making `length` a computed method, with an optional dirty-flag cache for performance.
- Truck and DeliveryRoute classes both containing a `driver` attribute, causing ambiguity about which to update when the driver changes — fixed by normalizing the driver to a single authoritative object.
- International telex switch project where acceptance tests were generated programmatically from the client's specification document, so test suites updated automatically when the spec changed.
- U.S. state government audit uncovering over 10,000 programs each containing their own independent Social Security number validation logic — a large-scale interdeveloper duplication example.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**7. The Evils of Duplication**

An LLM coding agent is especially prone to impatient and interdeveloper duplication because it generates code statelessly across calls — it cannot remember that it already defined a validation function in a prior context window and will silently reimplement it. Agents also tend to inline 'magic' derived values or repeat business logic across generated files rather than creating a single authoritative source, because generating self-contained code feels locally correct. Applying DRY means an agent must explicitly audit the existing codebase for canonical representations before generating new logic, and should prefer generating or extending abstractions over producing parallel implementations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## DRY Trigger Duplication discovered in code is a direct trigger condition for ref

## Core Principle

Refactoring is the continuous, disciplined process of reworking code structure as understanding evolves, using the gardening metaphor rather than construction to frame software as organic and always in need of tending. The core discipline requires separating refactoring from feature work, maintaining comprehensive tests, and taking small verifiable steps to avoid net harm. Deferring refactoring is a false economy—dependency accumulation makes later changes exponentially more costly, so the pragmatic rule is to refactor early and often.

## Key Heuristics

These are the load-bearing rules for this concept.

> Refactor Early, Refactor Often

> Don't try to refactor and add functionality at the same time.

> Make sure you have good tests before you begin refactoring. Run the tests as often as possible.

> Take short, deliberate steps... If you keep your steps small, and test after each step, you will avoid prolonged debugging.

> fail to refactor now, and there'll be a far greater time investment to fix the problem down the road—when there are more dependencies to reckon with.

> Don't live with broken windows.

> If it hurts now, but is going to hurt even more later, you might as well get it over with.

## Anti-Patterns & Fixes

- Deferring Refactoring Under Time Pressure: Developers skip refactoring citing deadlines, but this causes dependencies to grow around the problematic code, making future refactoring exponentially more expensive and dangerous. Fix: Schedule refactoring explicitly; treat deferred refactoring as a tracked debt with stakeholder visibility.
- Refactoring and Adding Features Simultaneously: Mixing new functionality with structural changes makes it impossible to isolate the source of bugs or regressions. Fix: Complete refactoring as a separate, isolated commit or phase before adding new behavior.
- Large-Scale Reckless Reworking: Ripping up vast quantities of code with wild abandon risks leaving the codebase in a worse state than before. Fix: Make many small, localized changes that collectively achieve the larger-scale structural improvement, testing after each step.
- Construction Metaphor Thinking: Treating software as a finished artifact after initial build, calling only for maintenance fixes. Fix: Adopt the gardening metaphor—continuously monitor, prune, split, and reorganize code as understanding evolves.
- Silent Refactoring of Shared Interfaces: Changing a module's interface or functionality without signaling breakage to dependent code. Fix: Ensure drastic interface changes break the build so old clients are immediately identified and updated.

## When To Apply

Load this page when:

- Use this when you discover duplicated logic or copy-pasted code blocks that violate the DRY principle.
- Use this when a routine has grown too large or is attempting to accomplish more than one coherent responsibility.
- Use this when requirements have drifted and existing code encodes outdated assumptions about the domain.
- Use this when two separate implementations of similar behavior could be merged into a common abstraction.
- Use this when a design smells non-orthogonal—changes in one module ripple unexpectedly into unrelated modules.
- Use this when performance analysis reveals that functionality must be relocated within the system architecture.
- Use this when a code section feels 'wrong' or produces friction every time it is read or modified.
- Use this when adding a new feature reveals that the existing structure makes the addition unnecessarily complex or duplicative.

## Concrete Examples

- State-based tax calculation code (Texas/Ohio/Maine) with repeated calc formula and mixed rate logic—used as an exercise to demonstrate structural refactoring need.
- Java Shape class with integer constants for SQUARE, CIRCLE, RIGHT_TRIANGLE that needs restructuring before adding more shape types—demonstrates refactoring for extensibility.
- Medical analogy: a code 'growth' that is cheap to remove while small but increasingly dangerous and expensive to remove as it spreads, used to justify early refactoring to management.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**33. Refactoring**

An LLM coding agent is particularly prone to the 'construction metaphor' failure mode: it generates code in a single pass optimized for the immediate prompt, treating the output as a finished artifact rather than a first draft requiring future tending. This means agents will silently propagate duplication and non-orthogonal design across files because they lack continuous awareness of the evolving codebase state. Agents should be explicitly triggered to run a refactoring pass before and after feature additions, treating refactoring as a mandatory, test-gated phase rather than an optional cleanup step.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## DRY at Team Scale Use a project librarian or focal point roles to prevent duplic

## Core Principle

Pragmatic team principles are individual pragmatic practices applied collectively: no broken windows, DRY, orthogonality, and automation must be enforced at the team level with explicit role assignments (quality ownership, water tester, librarian, tool builder) rather than assumed. Teams should organize around functional areas mirroring code modularity, not job titles, to isolate change impact. A unified external voice and team identity amplify effectiveness, while strong technical and administrative leadership prevents autonomous teams from becoming chaotic.

## Key Heuristics

These are the load-bearing rules for this concept.

> Organize Around Functionality, Not Job Functions

> Quality can come only from the individual contributions of all team members.

> Teams as a whole should not tolerate broken windows—those small imperfections that no one fixes.

> It's even easier for teams as a whole to get boiled.

> The team speaks with one voice—externally. Internally, we strongly encourage lively, robust debate.

> Give each member the ability to shine in his or her own way. Give them just enough structure to support them... Then resist the temptation to add more paint.

> Automation is an essential component of every project team.

## Anti-Patterns & Fixes

- Quality Officer Delegation: Assigning one person to own quality causes everyone else to abdicate responsibility. Fix: Every team member owns quality; the team collectively enforces no broken windows.
- Waterfall Role Silos: Organizing teams by job function (analyst, coder, tester) creates hierarchy and prevents informed decision-making. Fix: Organize teams around functional areas of the system so each team owns end-to-end responsibility.
- Collective Blindness to Scope Creep: Teams assume someone else noticed a change, so no one acts on it. Fix: Explicitly appoint a 'chief water tester' to track new requirements, timeline changes, and environment shifts.
- Duplicated Work Across Team Members: Without coordination, multiple developers solve the same problem differently. Fix: Appoint a project librarian or domain focal points so people know who to consult before starting new work.
- Autonomous Teams Without Leadership: Creating self-organizing teams without technical and administrative heads leads to chaos. Fix: Ensure at least two heads—one technical (philosophy, arbitration, big picture) and one administrative (scheduling, reporting, external communication).
- Inconsistent External Communication: Teams that produce varied documentation and hold unstructured meetings appear incompetent. Fix: Develop a team brand, consistent documentation standards, and a unified external voice.

## When To Apply

Load this page when:

- Use this when a multi-agent or multi-model pipeline is generating code across different modules and duplication risk is high—assign a 'librarian' coordination step.
- Use this when an agent is operating in a long-running project context and must detect whether scope, requirements, or environment have silently shifted since the last checkpoint.
- Use this when coordinating output from multiple LLM agents that each own a subsystem—apply functional team organization so each agent's domain is orthogonal and changes in one don't cascade.
- Use this when agent-generated documentation, comments, or commit messages across a codebase are inconsistent in terminology or style—enforce a unified team voice via shared style rules.
- Use this when no automated build, test, or lint pipeline exists for an agent-assisted project—trigger automation setup before any further feature work.
- Use this when small code quality issues (formatting, dead code, minor TODOs) are accumulating without being addressed—invoke the no broken windows policy to resolve them before they compound.
- Use this when an agent is tasked with adding features and risks over-engineering—apply 'know when to stop adding paint' and check against original requirements.

## Concrete Examples

- Naming projects after off-the-wall things (killer parrots preying on sheep, optical illusions, mythical cities) and spending 30 minutes on a zany logo to build team identity.
- Appointing a 'chief water tester' to monitor for increased scope, decreased timescales, and new environment requirements not in the original agreement.
- Using a project librarian to coordinate documentation and code repositories as the first port of call for anyone looking for existing solutions.
- Assigning domain focal points (e.g., Mary for date handling, Fred for database schema) so developers know who to consult to avoid duplication.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**41. Pragmatic Teams**

An LLM coding agent operating across a multi-file or multi-session project is especially prone to the 'boiled frog' failure—it has no persistent awareness of accumulated scope drift, so it must explicitly re-check original requirements against current state at each invocation. Agents also naturally produce inconsistent terminology and structure across outputs (the anti-pattern of sullen, inconsistent teams), making automated style enforcement and a shared schema/glossary critical rather than optional. The DRY/librarian pattern is particularly vital for agents: without a coordination mechanism, multiple agent invocations will independently re-implement the same logic, producing the exact duplication the chapter warns against.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## DRY for Artifacts Web content documentation and reports are views derived automa

## Core Principle

Ubiquitous Automation argues that every recurring project operation must be scripted and executed automatically rather than performed manually, because humans are inconsistent and unrepeatable while scripts are not. The chapter covers automating builds, code generation, regression testing, documentation publishing, and even administrative workflows using tools like make, cron, and scripting languages. The governing principle is that a project should be fully buildable, testable, and shippable from scratch with a single command, and all derived artifacts should be regenerated automatically from their canonical sources.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Use Manual Procedures

> Civilization advances by extending the number of important operations we can perform without thinking.

> People just aren't as repeatable as computers are. Nor should we expect them to be.

> A shell script or batch file will execute the same instructions, in the same order, time after time.

> We want to check out, build, test, and ship with a single command.

> Misleading information is worse than no information at all.

> Let the computer do the repetitious, the mundane—it will do a better job of it than we would.

> Manual procedures leave consistency up to chance; repeatability isn't guaranteed, especially if aspects of the procedure are open to interpretation by different people.

## Anti-Patterns & Fixes

- Multi-Page Manual Install Instructions: Developers follow long click-by-click IDE setup guides, resulting in subtly different environments per machine and environment-specific bugs. Fix: Replace with a single automated setup script checked into source control.
- Memory-Dependent Scheduling: Relying on developers to remember when to run maintenance scripts causes tasks to be skipped or run inconsistently. Fix: Use cron or equivalent schedulers to run all recurring tasks unattended.
- IDE-Only Builds: Using only an IDE for builds makes it difficult to automate, hook in code generation, or run regression tests consistently. Fix: Use makefiles or equivalent build scripts even alongside IDEs.
- Hand-Maintained Documentation/Web Content: Keeping a project website or docs updated manually leads to stale, misleading content. Fix: Generate and publish all documentation automatically as part of the nightly build or check-in hook.
- Infrequent Test Runs: Not running regression tests regularly means broken code may not be discovered until months after the causative change. Fix: Run the full test suite automatically on every nightly build.
- Separate Final Build Process Undiscovered Until Ship Day: Leaving final build steps (ISO images, permission fixes, optimizations) untested until release. Fix: Automate final build steps with a dedicated make target (e.g., make final) and run them early and regularly.

## When To Apply

Load this page when:

- Use this when setting up a new project repository and deciding how builds, tests, and releases will be executed by team members.
- Use this when onboarding new developers requires following multi-step manual environment setup instructions.
- Use this when the same sequence of commands is typed repeatedly to build, test, or deploy the project.
- Use this when bugs appear on some developer machines but not others due to inconsistent environment configuration.
- Use this when project documentation or a team website must be kept in sync with the codebase.
- Use this when code review, approval workflows, or administrative paperwork is tracked manually and prone to being forgotten.
- Use this when a regression is discovered that traces back to a code change from weeks or months ago, indicating tests are not run on every build.
- Use this when generating derived artifacts (source files, headers, docs) from a canonical source such as XML or schema files.

## Concrete Examples

- Client site where system admins gave each developer multi-page IDE add-on installation instructions, resulting in every developer's machine being loaded slightly differently and environment-specific bugs.
- A crontab file scheduling nightly builds at 00:05, backups at 03:15 on weekdays, and expense reports at midnight on the first of each month.
- A makefile rule that takes a test.xml file, runs a Perl conversion script to produce test.java, then compiles it to test.class automatically when 'make test.class' is invoked.
- Embedding a '/* Status: needs_review */' marker in source files so a script can auto-detect files needing review, post a web page, send email, or schedule a calendar meeting.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Ubiquitous Automation**

An LLM coding agent is highly prone to generating setup steps, build instructions, or deployment procedures as prose or ad-hoc shell commands rather than encoding them in versioned, executable automation scripts—reproducing the exact anti-pattern of manual procedures. Unlike a human who might remember to run a script, an agent operating across sessions has no persistent memory, making content-driven and scheduled automation (cron, makefiles, CI pipelines) even more critical: the automation must be self-triggering, not agent-triggered. Agents should default to producing makefile targets, CI workflow files, or setup scripts as first-class artifacts, not README instructions, to ensure any future agent or human can achieve a correct result with a single command.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## DRY via Generation Pattern Use text manipulation scripts as a single source of t

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

## Four Categories of Duplication Imposed Inadvertent Impatient and Interdeveloper

## Core Principle

Duplication is the root cause of most maintenance failures because knowledge represented in multiple places will inevitably diverge. The DRY principle demands a single authoritative source for every piece of knowledge, whether that knowledge lives in code, documentation, data schemas, or tests. Duplication arises from four distinct causes — imposed constraints, design mistakes, laziness under deadline pressure, and lack of team coordination — each requiring a targeted strategy to eliminate.

## Key Heuristics

These are the load-bearing rules for this concept.

> DRY—Don't Repeat Yourself

> EVERY PIECE OF KNOWLEDGE MUST HAVE A SINGLE, UNAMBIGUOUS, AUTHORITATIVE REPRESENTATION WITHIN A SYSTEM.

> It isn't a question of whether you'll remember: it's a question of when you'll forget.

> Bad code requires lots of comments.

> Keep the low-level knowledge in the code, where it belongs, and reserve the comments for other, high-level explanations.

> Short cuts make for long delays.

> Make It Easy to Reuse

> The trick is to make the process active: this cannot be a one-time conversion, or we're back in a position of duplicating data.

## Anti-Patterns & Fixes

- Commenting What the Code Does: Writing comments that restate the logic of the code creates a duplicate representation of knowledge. Fix: Let the code express the low-level logic; reserve comments for high-level rationale and intent only.
- Derived Data as Stored Fields: Storing a value (e.g., line length) that can be computed from other fields creates a dependency that can fall out of sync. Fix: Make derived values computed properties or methods; cache with a dirty flag if performance requires it.
- Copy-Paste Reuse (Impatient Duplication): Copying a routine or class and modifying it saves seconds but creates divergent maintenance burdens. Fix: Invest time upfront to abstract the shared logic into a reusable component.
- Unnormalized Object Attributes (Interdependency Duplication): Storing the same logical entity (e.g., a driver) in multiple objects means changes must propagate to all holders. Fix: Normalize by identifying the authoritative owner of each piece of knowledge and reference it from other objects.
- Manually Maintained Parallel Representations: Keeping the same structure defined in multiple languages or formats by hand leads to drift. Fix: Generate all representations from a single canonical metadata source using a code generator run at build time.
- Interdeveloper Duplication: Different developers independently implement the same functionality, leading to silent divergence over years. Fix: Appoint a project librarian, maintain a shared utility repository, and foster frequent cross-team communication.

## When To Apply

Load this page when:

- Use this when you are about to define a data field whose value can be calculated from other existing fields in the same class.
- Use this when generating code or data structures in multiple languages or formats that must stay in sync (e.g., client/server shared schema).
- Use this when writing a comment that describes what the next line of code does rather than why it exists.
- Use this when you find yourself copying a function or class to make a slightly modified version instead of parameterizing or abstracting it.
- Use this when a business concept (e.g., a validation rule, a configuration value, a threshold) appears in more than one location in the codebase.
- Use this when documentation and code both describe the same behavior and a change to one requires a manual update to the other.
- Use this when working on a team codebase and about to implement utility functionality without first searching for an existing implementation.
- Use this when a performance optimization requires caching a derived value, to ensure the violation of DRY is localized and encapsulated.

## Concrete Examples

- Line class with a stored `length` field that duplicates information derivable from `start` and `end` points — fixed by making `length` a computed method, with an optional dirty-flag cache for performance.
- Truck and DeliveryRoute classes both containing a `driver` attribute, causing ambiguity about which to update when the driver changes — fixed by normalizing the driver to a single authoritative object.
- International telex switch project where acceptance tests were generated programmatically from the client's specification document, so test suites updated automatically when the spec changed.
- U.S. state government audit uncovering over 10,000 programs each containing their own independent Social Security number validation logic — a large-scale interdeveloper duplication example.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**7. The Evils of Duplication**

An LLM coding agent is especially prone to impatient and interdeveloper duplication because it generates code statelessly across calls — it cannot remember that it already defined a validation function in a prior context window and will silently reimplement it. Agents also tend to inline 'magic' derived values or repeat business logic across generated files rather than creating a single authoritative source, because generating self-contained code feels locally correct. Applying DRY means an agent must explicitly audit the existing codebase for canonical representations before generating new logic, and should prefer generating or extending abstractions over producing parallel implementations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Uniform Access Principle All services offered by a module should be available th

## Core Principle

Duplication is the root cause of most maintenance failures because knowledge represented in multiple places will inevitably diverge. The DRY principle demands a single authoritative source for every piece of knowledge, whether that knowledge lives in code, documentation, data schemas, or tests. Duplication arises from four distinct causes — imposed constraints, design mistakes, laziness under deadline pressure, and lack of team coordination — each requiring a targeted strategy to eliminate.

## Key Heuristics

These are the load-bearing rules for this concept.

> DRY—Don't Repeat Yourself

> EVERY PIECE OF KNOWLEDGE MUST HAVE A SINGLE, UNAMBIGUOUS, AUTHORITATIVE REPRESENTATION WITHIN A SYSTEM.

> It isn't a question of whether you'll remember: it's a question of when you'll forget.

> Bad code requires lots of comments.

> Keep the low-level knowledge in the code, where it belongs, and reserve the comments for other, high-level explanations.

> Short cuts make for long delays.

> Make It Easy to Reuse

> The trick is to make the process active: this cannot be a one-time conversion, or we're back in a position of duplicating data.

## Anti-Patterns & Fixes

- Commenting What the Code Does: Writing comments that restate the logic of the code creates a duplicate representation of knowledge. Fix: Let the code express the low-level logic; reserve comments for high-level rationale and intent only.
- Derived Data as Stored Fields: Storing a value (e.g., line length) that can be computed from other fields creates a dependency that can fall out of sync. Fix: Make derived values computed properties or methods; cache with a dirty flag if performance requires it.
- Copy-Paste Reuse (Impatient Duplication): Copying a routine or class and modifying it saves seconds but creates divergent maintenance burdens. Fix: Invest time upfront to abstract the shared logic into a reusable component.
- Unnormalized Object Attributes (Interdependency Duplication): Storing the same logical entity (e.g., a driver) in multiple objects means changes must propagate to all holders. Fix: Normalize by identifying the authoritative owner of each piece of knowledge and reference it from other objects.
- Manually Maintained Parallel Representations: Keeping the same structure defined in multiple languages or formats by hand leads to drift. Fix: Generate all representations from a single canonical metadata source using a code generator run at build time.
- Interdeveloper Duplication: Different developers independently implement the same functionality, leading to silent divergence over years. Fix: Appoint a project librarian, maintain a shared utility repository, and foster frequent cross-team communication.

## When To Apply

Load this page when:

- Use this when you are about to define a data field whose value can be calculated from other existing fields in the same class.
- Use this when generating code or data structures in multiple languages or formats that must stay in sync (e.g., client/server shared schema).
- Use this when writing a comment that describes what the next line of code does rather than why it exists.
- Use this when you find yourself copying a function or class to make a slightly modified version instead of parameterizing or abstracting it.
- Use this when a business concept (e.g., a validation rule, a configuration value, a threshold) appears in more than one location in the codebase.
- Use this when documentation and code both describe the same behavior and a change to one requires a manual update to the other.
- Use this when working on a team codebase and about to implement utility functionality without first searching for an existing implementation.
- Use this when a performance optimization requires caching a derived value, to ensure the violation of DRY is localized and encapsulated.

## Concrete Examples

- Line class with a stored `length` field that duplicates information derivable from `start` and `end` points — fixed by making `length` a computed method, with an optional dirty-flag cache for performance.
- Truck and DeliveryRoute classes both containing a `driver` attribute, causing ambiguity about which to update when the driver changes — fixed by normalizing the driver to a single authoritative object.
- International telex switch project where acceptance tests were generated programmatically from the client's specification document, so test suites updated automatically when the spec changed.
- U.S. state government audit uncovering over 10,000 programs each containing their own independent Social Security number validation logic — a large-scale interdeveloper duplication example.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**7. The Evils of Duplication**

An LLM coding agent is especially prone to impatient and interdeveloper duplication because it generates code statelessly across calls — it cannot remember that it already defined a validation function in a prior context window and will silently reimplement it. Agents also tend to inline 'magic' derived values or repeat business logic across generated files rather than creating a single authoritative source, because generating self-contained code feels locally correct. Applying DRY means an agent must explicitly audit the existing codebase for canonical representations before generating new logic, and should prefer generating or extending abstractions over producing parallel implementations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
