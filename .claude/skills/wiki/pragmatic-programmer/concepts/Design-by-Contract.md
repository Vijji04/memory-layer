---
title: Design by Contract
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 6 pages
---

# Design by Contract

> Consolidated from 6 related concept pages.

---

## Design by Contract DBC A technique by Bertrand Meyer that documents and enforces

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

---

## Design by Contract DbC A formalism using preconditions postconditions and invari

## Core Principle

This appendix catalogs canonical Internet resources for editors, compilers, languages, testing frameworks, version control systems, and documentation tools relevant to pragmatic software development. Key recurring themes include cross-platform portability, Design by Contract enforcement, automated testing, and parser/interface generation tooling. The chapter implicitly warns that all external references are temporally fragile, reinforcing the broader pragmatic principle of not depending on volatile external state.

## Key Heuristics

These are the load-bearing rules for this concept.

> They were valid at the time of writing, but (the Net being what it is) they may well be out of date by the time you read this.

> Emacs has a near-vertical learning curve, but repays handsomely once you've mastered it.

> vim is probably ported to the most platforms, and so would be a good choice of editor if you find yourself working in many different environments.

> Viper combines the best of both worlds [by making Emacs emulate vi].

> A process-oriented revision control tool that imposes project standards (such as verifying that checked-in code passes tests).

> SWIG connects programs written in C, C++, and Objective-C with a variety of high-level programming languages.

## Anti-Patterns & Fixes

- Hardcoded URL Dependency: Referencing specific URLs as stable resources causes breakage over time as the Net changes. Fix: Use authoritative domain roots or search by filename/project name rather than deep-linking to specific paths.
- Single-Platform Editor Lock-in: Committing to an editor that only works on one OS creates friction when working across environments. Fix: Choose cross-platform editors like vim (most widely ported) or Emacs for consistent tooling everywhere.
- Monolithic Language Binding: Writing code that tightly couples to a single language runtime makes integration with other systems impossible. Fix: Use interface generators like SWIG to expose C/C++ logic to high-level languages like Python or Perl.
- Manual Regression Testing: Hand-testing program interactions is error-prone and non-repeatable. Fix: Use tools like Expect to script and automate interaction with programs for consistent regression testing.
- No Contract Enforcement: Code without explicit precondition/postcondition checking silently propagates bad state. Fix: Apply Design by Contract tooling (iContract for Java, Nana for C/C++) to make invariants executable and checked at runtime.
- Unchecked Code Commits: Allowing code into version control without automated validation degrades codebase quality. Fix: Use process-oriented VCS tools like Aegis that enforce standards such as passing tests before check-in.

## When To Apply

Load this page when:

- Use this when selecting a code editor or IDE that must work consistently across Unix, Windows, and other environments.
- Use this when integrating C or C++ libraries into a Python, Perl, or Java codebase and needing a language bridge.
- Use this when setting up automated regression testing for a command-line application that requires interactive input/output scripting.
- Use this when enforcing Design by Contract constraints (preconditions, postconditions, invariants) in a Java or C/C++ project.
- Use this when configuring a version control system that should automatically reject commits failing test suites.
- Use this when choosing a parser generator for a Java project (javaCC) or a C project (bison) to process grammar specifications.
- Use this when building heterogeneous distributed systems that require objects written in different languages to communicate (CORBA/IIOP via OMG).
- Use this when generating API documentation directly from C++ headers or Java class files using a tool like DOC++.

## Concrete Examples

- iContract implements Design by Contract for Java as a preprocessor supporting preconditions, postconditions, invariants, and existential quantifiers.
- Expect (built on Tcl) is used to script regression testing by automating interaction with programs, and expectk wraps non-GUI apps with a windowing front end.
- The Beowulf Project builds high-performance computers from networked clusters of inexpensive Linux boxes.
- Aegis version control tool enforces that checked-in code must pass tests before acceptance, acting as a process-oriented gatekeeper.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Internet Resources**

An LLM coding agent cannot verify whether referenced URLs, library versions, or tool APIs remain valid at generation time, making it prone to hallucinating outdated endpoints, deprecated APIs, or nonexistent package names that were once correct. The Design by Contract and xUnit patterns are especially critical for agents: without enforced precondition/postcondition checking and automated test frameworks, an agent has no feedback loop to detect when its generated code violates implicit contracts or breaks existing behavior. Agents should be configured to prefer tool ecosystems with stable, programmatically queryable metadata (package registries, canonical documentation APIs) over hardcoded URLs, mirroring the chapter's own caveat about link rot.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Liskov Substitution Principle Subclasses must be usable through the base class i

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

---

## Loop Invariants Assertions that must hold before and after each loop iteration u

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

---

## PreconditionsPostconditionsInvariants Triad The three part contract structure wh

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

---

## Semantic Invariants Inviolate philosophical requirements central to the meaning

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
