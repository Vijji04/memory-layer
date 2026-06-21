---
title: Data vs. Imperative DSL Taxonomy: Data languages produce static configuration structures (e.g., Windows .rc files, sendmail config); imperative languages execute control flow logic (e.g., screen-scraping scripts)
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/12-Domain-Languages.json]
contributing_chapters: ["12. Domain Languages"]
confidence: high
---

# Data vs. Imperative DSL Taxonomy: Data languages produce static configuration structures (e.g., Windows .rc files, sendmail config); imperative languages execute control flow logic (e.g., screen-scraping scripts)

> From chapter: *12. Domain Languages*

## Core Principle

Domain Languages argues that the vocabulary of a problem domain should directly shape the language used to program it — ranging from simple configuration DSLs to full imperative mini-languages with parsers. Tip 17, 'Program Close to the Problem Domain,' is the central directive: by inventing or embedding a language whose syntax mirrors domain concepts, developers raise abstraction level, enable non-programmers to read specifications, and allow maintenance changes without touching implementation internals. The chapter classifies DSL approaches (data vs. imperative, stand-alone vs. embedded), advises investing in readable grammars for longevity, and highlights domain-specific error reporting as a concrete benefit of the approach.

## Key Heuristics

These are the load-bearing rules for this concept.

> Program Close to the Problem Domain

> The limits of language are the limits of one's world.

> By coding at a higher level of abstraction, you are free to concentrate on solving domain problems, and can ignore petty implementation details.

> Given that most applications exceed their expected lifetimes, you're probably better off biting the bullet and adopting the more complex and readable language up front.

> The trade-off is extendibility and maintenance. While the code for parsing a 'real' language may be harder to write, it will be much easier for people to understand, and to extend in the future.

> If you are writing in the problem domain, you can also perform domain-specific validation, reporting problems in terms your users can understand.

> You can change your application's behavior by changing the scripts it reads, all without compiling. This can significantly simplify maintenance in a dynamic application domain.

## Anti-Patterns & Fixes

- Generic Error Messages in Domain Code: Using standard compiler-style errors like 'undeclared identifier' when a domain-specific language is violated. Fix: Implement domain-aware validation that reports errors using domain vocabulary, e.g., listing known valid format names.
- Overly Simple Grammar for Long-Lived Systems: Choosing a minimal, cryptic line-oriented format (like sendmail config) because it is easy to parse. Fix: Invest in a readable, extensible grammar upfront; the maintenance savings over the application's lifetime outweigh initial implementation cost.
- Coding in Implementation Domain Instead of Problem Domain: Writing low-level C logic to handle mainframe screen interactions instead of abstracting it. Fix: Create a mini-language (e.g., 'locate prompt', 'waitfor') that maintenance programmers can update without touching underlying code.
- Monolithic Requirements Without Domain Language: Capturing user requirements only in prose or general-purpose code. Fix: Listen for well-bounded user statements and distill them into a mini-language specification that can become executable.

## When To Apply

Load this page when:

- Use this when users can articulate system behavior in precise, bounded statements that repeat a consistent vocabulary (e.g., 'listen on X, translate to Y, retransmit on Z').
- Use this when a configuration or rules system will need to change frequently without requiring a full recompile-and-redeploy cycle.
- Use this when multiple secondary users (ops staff, testers, maintenance programmers) each have their own interaction model with the system that could be abstracted into a targeted mini-language.
- Use this when screen-scraping or integrating with a legacy system whose field layout may change, making a scriptable interaction layer preferable to hardcoded logic.
- Use this when a single schema or specification needs to generate multiple output artifacts (SQL, XML, C structs, web pages) to keep all representations in sync.
- Use this when domain validation errors in general-purpose language messages would be unintelligible to the domain experts who need to act on them.
- Use this when extending an existing language (e.g., Python) with domain objects is sufficient to express domain logic without building a parser from scratch.

## Concrete Examples

- X.25 switching mini-language: 'From X25LINE1 (Format=ABC123) { Put TELSTAR1...; Store DB; }' — a domain language for transaction routing that evolves to include conditional logic for negative balances.
- Sendmail configuration file: a thousand-line cryptic data language controlling mail routing, cited as a negative example of readability.
- Windows .rc resource file: a readable data language describing menus and dialog boxes that compiles to data structures.
- Screen-scraping mini-language: imperative scripts using 'locate prompt', 'type', 'waitfor', 'text_at' to control mainframe terminal interactions without hardcoding in C.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**12. Domain Languages**

An LLM coding agent tends to default to general-purpose language constructs even when the problem domain has a stable, expressible vocabulary — generating verbose, low-level code instead of proposing or using a DSL that would make future changes trivial. This chapter's framework should trigger an agent to first ask whether a mini-language or embedded DSL exists (or should be created) before writing imperative logic, preventing the anti-pattern of burying domain rules in implementation detail that no domain expert can maintain. Agents are also prone to emitting generic exception messages; domain-specific error reporting is a concrete output quality check an agent should apply whenever generating parsers or interpreters.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
