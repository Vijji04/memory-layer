---
title: Preconditions/Postconditions/Invariants Triad: The three-part contract structure where preconditions specify caller obligations, postconditions specify routine guarantees, and invariants specify always-true class-level conditions
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Design-by-Contract.json]
contributing_chapters: ["Design by Contract"]
confidence: high
---

# Preconditions/Postconditions/Invariants Triad: The three-part contract structure where preconditions specify caller obligations, postconditions specify routine guarantees, and invariants specify always-true class-level conditions

> From chapter: *Design by Contract*

## Core Principle

Design by Contract formalizes software module interactions by requiring explicit preconditions (caller obligations), postconditions (routine guarantees), and invariants (always-true conditions), making correctness a verifiable agreement rather than an assumption. Violations are bugs by definition, and the technique forces developers to reason about input domains and output promises at design time rather than discovering them through failure. DBC extends naturally to inheritance (via Liskov Substitution), loop correctness, and even dynamic agent negotiation, serving as both a design discipline and a runtime enforcement mechanism.

## Key Heuristics

These are the load-bearing rules for this concept.

> Be strict in what you will accept before you begin, and promise as little as possible in return.

> Design with Contracts. (Tip 31)

> If your contract indicates that you'll accept anything and promise the world in return, then you've got a lot of code to write!

> By not stating these things, you are back to programming by coincidence.

> Failure to live up to the contract is a bug. It is not something that should ever happen.

> It is the caller's responsibility to pass good data.

> ERR IN FAVOR OF THE CONSUMER. (example of a clear semantic invariant)

> If we can't use contracts by hand, we won't be able to use them automatically.

## Anti-Patterns & Fixes

- ProgrammingByCoincidence: Writing routines without specifying input domain, boundary conditions, or guarantees, leading to implicit and unverified assumptions. Fix: Enumerate preconditions, postconditions, and invariants explicitly at design time.
- UsingPreconditonsForUserInputValidation: Treating preconditions as a validation layer for external user input conflates caller-contract enforcement with input sanitization. Fix: Use preconditions only for internal module contracts; handle user input validation separately upstream.
- ContractViolationSilentFailure: Allowing a routine to silently proceed when its preconditions are violated, masking bugs. Fix: Raise exceptions or terminate the program when contract terms are breached.
- SubclassContractWeakening: Overriding base class methods in subclasses with narrower input acceptance or weaker output guarantees, violating LSP. Fix: Subclasses must accept at least as much input and guarantee at least as much output as the parent class contract specifies.
- AssertionsAsFullDBCSubstitute: Relying solely on runtime assertions to enforce contracts, missing inheritance propagation, 'old' value tracking, and library boundary checks. Fix: Use a DBC preprocessor or language with built-in DBC support; supplement assertions with explicit contract comments at minimum.
- MutableContractParameters: Allowing a method to modify its own input parameters, enabling circumvention of postcondition verification. Fix: Declare parameters as final (Java) or use @pre-value syntax to capture original values for postcondition checks.

## When To Apply

Load this page when:

- Use this when designing a public API or module interface to specify exactly what callers must provide and what the module guarantees in return.
- Use this when creating a subclass or implementing an interface to verify that the new type honors all behavioral contracts of its parent.
- Use this when debugging an unexpected failure at a module boundary to identify which party—caller or callee—violated the contract.
- Use this when writing a loop algorithm to define and verify a loop invariant that proves correctness at each iteration.
- Use this when encoding a non-negotiable system requirement (e.g., 'never double-charge a transaction') to establish a semantic invariant that guides all error-recovery design.
- Use this when integrating with external libraries to document and assert assumed preconditions and expected postconditions at the boundary.
- Use this when a function has complex input constraints or ordering requirements that cannot be captured by the type system alone.
- Use this when designing autonomous or multi-agent systems where components must negotiate capabilities and obligations dynamically.

## Concrete Examples

- iContract Java example: insertNode on a unique ordered list with @pre contains(aNode)==false and @post contains(aNode)==true, plus a forall invariant ensuring increasing node order.
- setFont contract using iContract: @pre f != null and @post getFont() == f, ensuring the font set is the font retrieved, enforcing LSP on AWT Component subclasses.
- Debit card transaction switch semantic invariant: 'ERR IN FAVOR OF THE CONSUMER'—errors must never result in a duplicate transaction charge, guiding all error-recovery design.
- Loop invariant example in Java: finding array maximum with invariant 'm = max(arr[0:i-1])' documented as a comment to prove correctness across iterations.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Design by Contract**

An LLM coding agent is especially prone to 'programming by coincidence'—generating plausible-looking implementations without ever explicitly reasoning about input domains, boundary conditions, or output guarantees, which are the exact failure modes DBC prevents. Unlike a human who might mentally track invariants, an agent generating a subclass or override has no automatic mechanism to check that it preserves the parent contract, making Liskov violations a silent and common output. Requiring agents to emit explicit precondition/postcondition annotations as part of every function they generate forces constraint reasoning upfront and creates machine-checkable artifacts that catch agent hallucinations at module boundaries.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
