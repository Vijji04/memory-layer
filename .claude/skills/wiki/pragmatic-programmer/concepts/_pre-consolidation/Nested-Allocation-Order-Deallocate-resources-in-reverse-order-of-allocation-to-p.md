---
title: Nested Allocation Order: Deallocate resources in reverse order of allocation to prevent orphaned references; always allocate the same set of resources in the same order to prevent deadlock
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/How-to-Balance-Resources.json]
contributing_chapters: ["How to Balance Resources"]
confidence: high
---

# Nested Allocation Order: Deallocate resources in reverse order of allocation to prevent orphaned references; always allocate the same set of resources in the same order to prevent deadlock

> From chapter: *How to Balance Resources*

## Core Principle

Resource management requires that every allocation be paired with a deallocation owned by the same routine or object, preventing leaks caused by conditional logic, exceptions, or implicit coupling through shared state. Nested resources must be released in reverse-acquisition order, acquired in consistent order across sites, and encapsulated in language constructs (RAII, finally) that guarantee cleanup on all exit paths. Runtime balance checks and resource wrappers catch violations that static discipline misses.

## Key Heuristics

These are the load-bearing rules for this concept.

> Finish What You Start

> The routine or object that allocates a resource should be responsible for deallocating it.

> Deallocate resources in the opposite order to that in which you allocate them.

> When allocating the same set of resources in different places in your code, always allocate them in the same order.

> It is always a good idea to build code that actually checks that resources are indeed freed appropriately.

> Pragmatic Programmers trust no one, including ourselves.

## Anti-Patterns & Fixes

- Split Ownership via Global State: readCustomer opens a file and stores it in a global variable; writeCustomer closes it. A conditional branch that skips writeCustomer leaks the file handle until process exhaustion. Fix: Pass the file handle explicitly and open/close in the same routine (updateCustomer), making ownership unambiguous.
- Patch-the-Caller Anti-Pattern: Adding fclose(cFile) in the caller's else-branch to compensate for the missing close spreads resource management across three routines. Fix: Refactor so the single owning routine handles both open and close unconditionally.
- Duplicate Deallocation on Exception Paths: In C++, manually deleting a pointer both in the normal exit path and in a catch block violates DRY and creates a maintenance hazard. Fix: Use stack allocation, RAII wrapper classes, or auto_ptr/unique_ptr so the destructor handles cleanup in all paths.
- Unspecified Aggregate Deallocation Policy: Failing to declare who owns substructures in a composite data structure leads to either memory leaks or double-frees. Fix: Establish and document a semantic invariant (recursive delete, orphan, or refuse-if-nonempty) and implement it consistently via a dedicated allocation/deallocation module.
- Unverified Resource Balance: Assuming resources are freed without runtime checks allows leaks to accumulate silently in long-running processes. Fix: Implement resource wrappers that track allocations/deallocations and assert balance at known checkpoints (e.g., top of a request-processing loop).

## When To Apply

Load this page when:

- Use this when generating any code that opens a file, acquires a lock, allocates memory, or starts a transaction — verify the close/release is in the same scope as the open/acquire.
- Use this when a conditional branch might skip the deallocation path that was paired with an earlier allocation.
- Use this when generating C++ code that could throw exceptions — ensure RAII wrappers or stack objects are used so destructors fire on all exit paths.
- Use this when generating Java/Python/JS code with I/O or network resources — ensure finally/try-with-resources/context-manager patterns are used.
- Use this when generating code that allocates multiple resources — verify deallocation order is the reverse of allocation order.
- Use this when generating code that acquires multiple locks or shared resources — verify acquisition order is consistent across all call sites to prevent deadlock.
- Use this when generating or modifying a composite data structure — verify that an explicit ownership policy for substructure deallocation exists and is enforced.
- Use this when generating long-running service loops — add a resource balance checkpoint assertion at the top of the loop.

## Concrete Examples

- C example: readCustomer/writeCustomer sharing a global cFile variable, where a conditional update skips writeCustomer and causes 'too many open files' in production. Fixed by moving open/close into updateCustomer and passing the handle explicitly.
- C++ example: a Node pointer deleted in both the normal return path and a catch block, violating DRY. Fixed first by stack allocation, then by a NodeResource RAII wrapper class, then by auto_ptr.
- Java example: a temporary file that must be deleted on all exit paths (including exceptions and early returns), implemented cleanly with a finally block calling tmpFile.delete().

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**How to Balance Resources**

An LLM agent generating code is especially prone to split-ownership bugs because it writes functions in isolation or in sequence without a global view of resource lifetimes — it may generate an 'open' in one function and an 'close' in another without flagging the coupling, exactly replicating the readCustomer/writeCustomer anti-pattern. Agents also tend to add deallocation only on the 'happy path' they reason about first, missing exception paths or conditional branches that bypass cleanup. Applying 'Finish What You Start' as a generation constraint — always emit the paired release immediately after the acquire, in the same scope, before filling in intermediate logic — prevents these failure modes structurally.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
