---
title: Passive Code Generators: Run once to produce a freestanding result that is then edited and maintained independently, used for templating, one-off conversions, and precomputed resources
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Code-Generators.json]
contributing_chapters: ["Code Generators"]
confidence: high
---

# Passive Code Generators: Run once to produce a freestanding result that is then edited and maintained independently, used for templating, one-off conversions, and precomputed resources

> From chapter: *Code Generators*

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
