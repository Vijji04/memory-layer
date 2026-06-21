---
title: App-titude Test: Kent Beck's three-stage model (make it work, make it right, make it fast) used to diagnose why embedded code stagnates at 'make it work' and never achieves long-term structural health
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-29-Clean-Embedded-Architecture.json]
contributing_chapters: ["Chapter 29: Clean Embedded Architecture"]
confidence: high
---

# App-titude Test: Kent Beck's three-stage model (make it work, make it right, make it fast) used to diagnose why embedded code stagnates at 'make it work' and never achieves long-term structural health

> From chapter: *Chapter 29: Clean Embedded Architecture*

## Core Principle

Clean embedded architecture requires treating hardware and operating systems as swappable details hidden behind HAL and OSAL boundary layers, so that domain and application logic remain pure software with no firmware dependencies. The core diagnostic is testability: if code can only be verified on the physical target, the architecture has failed. Firmware is defined not by storage medium but by dependency structure—any code, embedded or not, that cannot be separated from its execution platform is firmware and will resist change.

## Key Heuristics

These are the load-bearing rules for this concept.

> Although software does not wear out, it can be destroyed from within by unmanaged dependencies on firmware and hardware.

> Stop writing so much firmware and give your code a chance at a long useful life.

> Software and firmware intermingling is an anti-pattern. Code exhibiting this anti-pattern will resist changes.

> A clean embedded architecture is a testable embedded architecture.

> Treat the operating system as a detail and protect against OS dependencies.

> Limit header file contents to function declarations as well as the constants and struct names that are needed by the function.

> The fewer places where code knows the details, the fewer places where code will have to be tracked down and modified.

> If you define an OSAL, you can also encourage your applications to have a common structure.

## Anti-Patterns & Fixes

- Firmware Infection: Business logic and hardware-interaction code are mixed in the same files or functions, making the entire codebase change-resistant when hardware evolves. Fix: Introduce a HAL that owns all hardware-touching code; domain logic depends only on the HAL interface.
- Target-Only Testing: Code is structured so it can only be tested on the physical embedded target, creating a bottleneck that slows all development. Fix: Apply layering with HAL and OSAL so that domain and application logic can be compiled and tested off-target on a host machine.
- SQL/Platform Burial (Non-embedded Firmware): Non-embedded developers embed SQL, Android API calls, or platform specifics throughout business logic, creating the same firmware problem without hardware. Fix: Isolate all platform and persistence calls behind interfaces so business logic has no direct dependency on them.
- Repeated Conditional Compilation (#ifdef Sprawl): Using #ifdef BOARD_V2 or similar guards thousands of times across a codebase to handle hardware variants, violating DRY and making the codebase unmaintainable. Fix: Use the HAL to hide hardware type as a detail; resolve variants at link time or via runtime binding instead of scattered preprocessor directives.
- Cluttered Interface Headers: Placing implementation-specific data structures, constants, and typedefs in header files that serve as interfaces, creating unwanted transitive dependencies. Fix: Restrict headers to function declarations and only the types/constants required by those function signatures.

## When To Apply

Load this page when:

- Use this when generating embedded C/C++ code that mixes ISR handlers, domain calculations, and peripheral I/O operations in the same file or translation unit.
- Use this when writing code that directly calls RTOS APIs (e.g., xTaskCreate, osDelay) inside business logic or domain model code.
- Use this when a codebase uses #ifdef TARGET or #ifdef BOARD_X more than once to conditionally compile hardware-specific behavior.
- Use this when asked to add a feature to embedded code and the only way to verify correctness is to flash and run on physical hardware.
- Use this when porting an embedded application from one microcontroller family or RTOS to another and determining what must change.
- Use this when designing the file and module structure of a new embedded project before any code is written.
- Use this when a system engineer's specification is being reverse-engineered from existing embedded source code because no clean separation exists between behavior and hardware.

## Concrete Examples

- A communications subsystem transitioning from TDM to VoIP where business call-handling logic was so entangled with TDM hardware specifics that the legacy code itself became the spec—no separation existed and the product could not be untangled.
- A message processor/dispatcher that resided in the same file as UART hardware interaction code, polluting protocol logic with serial port details and preventing reuse across hardware platforms.
- A small embedded system with ~17 functions in one file spanning ISRs, RPM calculation, flash storage, sensor zeroing, and sleep—grouped only by accident of authorship, not by concern or testability.
- Telecom application where the preprocessor directive #ifdef BOARD_V2 appeared several thousand times, representing an extreme DRY violation due to repeated conditional compilation for hardware variants.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 29: Clean Embedded Architecture**

An LLM coding agent defaults to the path of least resistance—generating working code that calls hardware registers, RTOS primitives, or platform SDKs directly inside the same functions that implement business rules, because that is the pattern most prevalent in training data for embedded systems. This produces code that passes the App-titude test but is structurally firmware: it cannot be unit-tested off-target, cannot be ported without pervasive rewrites, and accumulates #ifdef debt rapidly. Agents should explicitly be directed to emit HAL and OSAL interface declarations first, then implement domain logic against those interfaces, treating any concrete hardware or OS call as a detail that belongs only in the lowest layer—never inlined into logic that could otherwise have a long useful life.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
