---
title: Code Generators
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 5 pages
---

# Code Generators

> Consolidated from 5 related concept pages.

---

## Active Code Generation Using filters or code generators to derive multiple repre

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

## Active Code Generators Run each time output is needed producing disposable deriv

## Core Principle

Code generators enforce the DRY principle across contexts where information must appear in multiple forms: passive generators produce freestanding artifacts once (templates, conversions, precomputed tables), while active generators produce disposable derived files on every build from a single authoritative source. The key insight is that active code generation transforms schema/definition changes into compile-time errors rather than silent runtime drift, but only when integrated into the build pipeline. Generators need not be complex — simple input formats reduce generation to print statements — and their output need not be source code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Write Code That Writes Code

> Once built, it can be used throughout the life of the project at virtually no cost.

> With an active code generator, you can take a single representation of some piece of knowledge and convert it into all the forms your application needs.

> Whenever you find yourself trying to get two disparate environments to work together, you should consider using active code generators.

> Keep the input format simple, and the code generator becomes simple.

> Code generators needn't generate code — you can use code generators to write just about any output: HTML, XML, plain text.

> This scheme works only if you make the code generation part of the build process itself.

## Anti-Patterns & Fixes

- Manual Schema Mirroring: Coding data structures by hand to mirror a database schema duplicates knowledge in two places; when the schema changes the code silently diverges, causing runtime failures. Fix: Use an active code generator that derives structures directly from the schema and integrate it into the build so mismatches become compile-time errors.
- Duplicating Shared Types Across Languages: Manually defining the same message formats or data structures in multiple languages causes them to drift. Fix: Express the shared definition once in a language-neutral format and generate all language-specific implementations from it.
- Over-Engineering the Generator Parser: Building a complex input format makes the parser dominate generator complexity and maintenance cost. Fix: Keep input format simple so that the actual code generation reduces to straightforward print statements.
- Treating Active Generator Output as Source: Editing generated throw-away files directly means changes are lost on the next generation run. Fix: Treat active generator output as disposable; make all changes upstream in the generator or its input definition.

## When To Apply

Load this page when:

- Use this when the same structural information (e.g., enum values, schema columns, message fields) must appear in two or more places in the codebase or in different languages.
- Use this when a database schema change should automatically propagate to corresponding in-code data structures to prevent silent runtime errors.
- Use this when setting up a new project and every new source file needs boilerplate (copyright headers, package directives, comment blocks, class outlines).
- Use this when performing a one-time bulk conversion between two formats or languages where 90% automation is still a net win over fully manual conversion.
- Use this when two subsystems written in different programming languages need to share data structure definitions or message formats.
- Use this when runtime computation of a resource (e.g., trig lookup tables) is expensive and the values can be precomputed and emitted as source.
- Use this when repetitive typing of structurally identical code blocks is creating error-prone manual work that a template could eliminate.

## Concrete Examples

- Generating both a C header (.h with typedef enum) and a .c file (string name array) from a flat list of enumerated state names, enabling debug-friendly string representation.
- Converting 15 already-written troff book sections to LaTeX using a passive code generator (~90% accurate, remainder fixed by hand).
- Active code generator reading a database schema (create table statements) and producing C structs mirroring table layouts, integrated into the build process.
- Language-neutral message definition file (M/F/E syntax) used to simultaneously generate equivalent typedef structs in C and packed records in Pascal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Code Generators**

An LLM coding agent is itself a code generator, but without an explicit active generation pipeline it will re-derive the same structures independently each time they are needed — producing drift between a schema definition, its ORM models, its API response types, and its documentation. The passive/active distinction is especially critical for agents: passively generating code that is then silently edited in subsequent turns breaks the single-source guarantee, so agents must treat any output derived from a schema or shared definition as active (regenerable, never hand-edited) and flag it as such. Agents also tend to inline duplicated knowledge across files rather than building a generator, which is the exact anti-pattern this chapter targets; the trigger should be: if the agent is about to write structurally identical code in more than one place, it should instead emit a generator.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## JigTemplate Mental Model Like a woodworkers jig a code generator encodes correct

## Core Principle

Code generators enforce the DRY principle across contexts where information must appear in multiple forms: passive generators produce freestanding artifacts once (templates, conversions, precomputed tables), while active generators produce disposable derived files on every build from a single authoritative source. The key insight is that active code generation transforms schema/definition changes into compile-time errors rather than silent runtime drift, but only when integrated into the build pipeline. Generators need not be complex — simple input formats reduce generation to print statements — and their output need not be source code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Write Code That Writes Code

> Once built, it can be used throughout the life of the project at virtually no cost.

> With an active code generator, you can take a single representation of some piece of knowledge and convert it into all the forms your application needs.

> Whenever you find yourself trying to get two disparate environments to work together, you should consider using active code generators.

> Keep the input format simple, and the code generator becomes simple.

> Code generators needn't generate code — you can use code generators to write just about any output: HTML, XML, plain text.

> This scheme works only if you make the code generation part of the build process itself.

## Anti-Patterns & Fixes

- Manual Schema Mirroring: Coding data structures by hand to mirror a database schema duplicates knowledge in two places; when the schema changes the code silently diverges, causing runtime failures. Fix: Use an active code generator that derives structures directly from the schema and integrate it into the build so mismatches become compile-time errors.
- Duplicating Shared Types Across Languages: Manually defining the same message formats or data structures in multiple languages causes them to drift. Fix: Express the shared definition once in a language-neutral format and generate all language-specific implementations from it.
- Over-Engineering the Generator Parser: Building a complex input format makes the parser dominate generator complexity and maintenance cost. Fix: Keep input format simple so that the actual code generation reduces to straightforward print statements.
- Treating Active Generator Output as Source: Editing generated throw-away files directly means changes are lost on the next generation run. Fix: Treat active generator output as disposable; make all changes upstream in the generator or its input definition.

## When To Apply

Load this page when:

- Use this when the same structural information (e.g., enum values, schema columns, message fields) must appear in two or more places in the codebase or in different languages.
- Use this when a database schema change should automatically propagate to corresponding in-code data structures to prevent silent runtime errors.
- Use this when setting up a new project and every new source file needs boilerplate (copyright headers, package directives, comment blocks, class outlines).
- Use this when performing a one-time bulk conversion between two formats or languages where 90% automation is still a net win over fully manual conversion.
- Use this when two subsystems written in different programming languages need to share data structure definitions or message formats.
- Use this when runtime computation of a resource (e.g., trig lookup tables) is expensive and the values can be precomputed and emitted as source.
- Use this when repetitive typing of structurally identical code blocks is creating error-prone manual work that a template could eliminate.

## Concrete Examples

- Generating both a C header (.h with typedef enum) and a .c file (string name array) from a flat list of enumerated state names, enabling debug-friendly string representation.
- Converting 15 already-written troff book sections to LaTeX using a passive code generator (~90% accurate, remainder fixed by hand).
- Active code generator reading a database schema (create table statements) and producing C structs mirroring table layouts, integrated into the build process.
- Language-neutral message definition file (M/F/E syntax) used to simultaneously generate equivalent typedef structs in C and packed records in Pascal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Code Generators**

An LLM coding agent is itself a code generator, but without an explicit active generation pipeline it will re-derive the same structures independently each time they are needed — producing drift between a schema definition, its ORM models, its API response types, and its documentation. The passive/active distinction is especially critical for agents: passively generating code that is then silently edited in subsequent turns breaks the single-source guarantee, so agents must treat any output derived from a schema or shared definition as active (regenerable, never hand-edited) and flag it as such. Agents also tend to inline duplicated knowledge across files rather than building a generator, which is the exact anti-pattern this chapter targets; the trigger should be: if the agent is about to write structurally identical code in more than one place, it should instead emit a generator.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Language Neutral Representation Express shared knowledge in a simple language ag

## Core Principle

Code generators enforce the DRY principle across contexts where information must appear in multiple forms: passive generators produce freestanding artifacts once (templates, conversions, precomputed tables), while active generators produce disposable derived files on every build from a single authoritative source. The key insight is that active code generation transforms schema/definition changes into compile-time errors rather than silent runtime drift, but only when integrated into the build pipeline. Generators need not be complex — simple input formats reduce generation to print statements — and their output need not be source code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Write Code That Writes Code

> Once built, it can be used throughout the life of the project at virtually no cost.

> With an active code generator, you can take a single representation of some piece of knowledge and convert it into all the forms your application needs.

> Whenever you find yourself trying to get two disparate environments to work together, you should consider using active code generators.

> Keep the input format simple, and the code generator becomes simple.

> Code generators needn't generate code — you can use code generators to write just about any output: HTML, XML, plain text.

> This scheme works only if you make the code generation part of the build process itself.

## Anti-Patterns & Fixes

- Manual Schema Mirroring: Coding data structures by hand to mirror a database schema duplicates knowledge in two places; when the schema changes the code silently diverges, causing runtime failures. Fix: Use an active code generator that derives structures directly from the schema and integrate it into the build so mismatches become compile-time errors.
- Duplicating Shared Types Across Languages: Manually defining the same message formats or data structures in multiple languages causes them to drift. Fix: Express the shared definition once in a language-neutral format and generate all language-specific implementations from it.
- Over-Engineering the Generator Parser: Building a complex input format makes the parser dominate generator complexity and maintenance cost. Fix: Keep input format simple so that the actual code generation reduces to straightforward print statements.
- Treating Active Generator Output as Source: Editing generated throw-away files directly means changes are lost on the next generation run. Fix: Treat active generator output as disposable; make all changes upstream in the generator or its input definition.

## When To Apply

Load this page when:

- Use this when the same structural information (e.g., enum values, schema columns, message fields) must appear in two or more places in the codebase or in different languages.
- Use this when a database schema change should automatically propagate to corresponding in-code data structures to prevent silent runtime errors.
- Use this when setting up a new project and every new source file needs boilerplate (copyright headers, package directives, comment blocks, class outlines).
- Use this when performing a one-time bulk conversion between two formats or languages where 90% automation is still a net win over fully manual conversion.
- Use this when two subsystems written in different programming languages need to share data structure definitions or message formats.
- Use this when runtime computation of a resource (e.g., trig lookup tables) is expensive and the values can be precomputed and emitted as source.
- Use this when repetitive typing of structurally identical code blocks is creating error-prone manual work that a template could eliminate.

## Concrete Examples

- Generating both a C header (.h with typedef enum) and a .c file (string name array) from a flat list of enumerated state names, enabling debug-friendly string representation.
- Converting 15 already-written troff book sections to LaTeX using a passive code generator (~90% accurate, remainder fixed by hand).
- Active code generator reading a database schema (create table statements) and producing C structs mirroring table layouts, integrated into the build process.
- Language-neutral message definition file (M/F/E syntax) used to simultaneously generate equivalent typedef structs in C and packed records in Pascal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Code Generators**

An LLM coding agent is itself a code generator, but without an explicit active generation pipeline it will re-derive the same structures independently each time they are needed — producing drift between a schema definition, its ORM models, its API response types, and its documentation. The passive/active distinction is especially critical for agents: passively generating code that is then silently edited in subsequent turns breaks the single-source guarantee, so agents must treat any output derived from a schema or shared definition as active (regenerable, never hand-edited) and flag it as such. Agents also tend to inline duplicated knowledge across files rather than building a generator, which is the exact anti-pattern this chapter targets; the trigger should be: if the agent is about to write structurally identical code in more than one place, it should instead emit a generator.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Passive Code Generators Run once to produce a freestanding result that is then e

## Core Principle

Code generators enforce the DRY principle across contexts where information must appear in multiple forms: passive generators produce freestanding artifacts once (templates, conversions, precomputed tables), while active generators produce disposable derived files on every build from a single authoritative source. The key insight is that active code generation transforms schema/definition changes into compile-time errors rather than silent runtime drift, but only when integrated into the build pipeline. Generators need not be complex — simple input formats reduce generation to print statements — and their output need not be source code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Write Code That Writes Code

> Once built, it can be used throughout the life of the project at virtually no cost.

> With an active code generator, you can take a single representation of some piece of knowledge and convert it into all the forms your application needs.

> Whenever you find yourself trying to get two disparate environments to work together, you should consider using active code generators.

> Keep the input format simple, and the code generator becomes simple.

> Code generators needn't generate code — you can use code generators to write just about any output: HTML, XML, plain text.

> This scheme works only if you make the code generation part of the build process itself.

## Anti-Patterns & Fixes

- Manual Schema Mirroring: Coding data structures by hand to mirror a database schema duplicates knowledge in two places; when the schema changes the code silently diverges, causing runtime failures. Fix: Use an active code generator that derives structures directly from the schema and integrate it into the build so mismatches become compile-time errors.
- Duplicating Shared Types Across Languages: Manually defining the same message formats or data structures in multiple languages causes them to drift. Fix: Express the shared definition once in a language-neutral format and generate all language-specific implementations from it.
- Over-Engineering the Generator Parser: Building a complex input format makes the parser dominate generator complexity and maintenance cost. Fix: Keep input format simple so that the actual code generation reduces to straightforward print statements.
- Treating Active Generator Output as Source: Editing generated throw-away files directly means changes are lost on the next generation run. Fix: Treat active generator output as disposable; make all changes upstream in the generator or its input definition.

## When To Apply

Load this page when:

- Use this when the same structural information (e.g., enum values, schema columns, message fields) must appear in two or more places in the codebase or in different languages.
- Use this when a database schema change should automatically propagate to corresponding in-code data structures to prevent silent runtime errors.
- Use this when setting up a new project and every new source file needs boilerplate (copyright headers, package directives, comment blocks, class outlines).
- Use this when performing a one-time bulk conversion between two formats or languages where 90% automation is still a net win over fully manual conversion.
- Use this when two subsystems written in different programming languages need to share data structure definitions or message formats.
- Use this when runtime computation of a resource (e.g., trig lookup tables) is expensive and the values can be precomputed and emitted as source.
- Use this when repetitive typing of structurally identical code blocks is creating error-prone manual work that a template could eliminate.

## Concrete Examples

- Generating both a C header (.h with typedef enum) and a .c file (string name array) from a flat list of enumerated state names, enabling debug-friendly string representation.
- Converting 15 already-written troff book sections to LaTeX using a passive code generator (~90% accurate, remainder fixed by hand).
- Active code generator reading a database schema (create table statements) and producing C structs mirroring table layouts, integrated into the build process.
- Language-neutral message definition file (M/F/E syntax) used to simultaneously generate equivalent typedef structs in C and packed records in Pascal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Code Generators**

An LLM coding agent is itself a code generator, but without an explicit active generation pipeline it will re-derive the same structures independently each time they are needed — producing drift between a schema definition, its ORM models, its API response types, and its documentation. The passive/active distinction is especially critical for agents: passively generating code that is then silently edited in subsequent turns breaks the single-source guarantee, so agents must treat any output derived from a schema or shared definition as active (regenerable, never hand-edited) and flag it as such. Agents also tend to inline duplicated knowledge across files rather than building a generator, which is the exact anti-pattern this chapter targets; the trigger should be: if the agent is about to write structurally identical code in more than one place, it should instead emit a generator.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
