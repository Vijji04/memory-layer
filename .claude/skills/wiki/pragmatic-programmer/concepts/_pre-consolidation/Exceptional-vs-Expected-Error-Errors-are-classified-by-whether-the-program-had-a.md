---
title: Exceptional vs. Expected Error: Errors are classified by whether the program had a reasonable prior expectation — truly unexpected events warrant exceptions; predictable failure cases warrant return codes or boolean returns
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/When-to-Use-Exceptions.json]
contributing_chapters: ["When to Use Exceptions"]
confidence: high
---

# Exceptional vs. Expected Error: Errors are classified by whether the program had a reasonable prior expectation — truly unexpected events warrant exceptions; predictable failure cases warrant return codes or boolean returns

> From chapter: *When to Use Exceptions*

## Core Principle

Exceptions should be reserved for truly unexpected events, not used as general-purpose control flow; the test is whether removing all handlers would break normal program logic. For predictable failure conditions, conventional return values or error handlers are more appropriate, keeping normal flow readable and modules loosely coupled. Misusing exceptions produces the same readability and maintainability problems as spaghetti code.

## Key Heuristics

These are the load-bearing rules for this concept.

> Use Exceptions for Exceptional Problems

> Exceptions should rarely be used as part of a program's normal flow; exceptions should be reserved for unexpected events.

> Assume that an uncaught exception will terminate your program and ask yourself, 'Will this code still run if I remove all the exception handlers?' If the answer is 'no,' then maybe exceptions are being used in nonexceptional circumstances.

> An exception represents an immediate, nonlocal transfer of control—it's a kind of cascading goto.

> Programs that use exceptions as part of their normal processing suffer from all the readability and maintainability problems of classic spaghetti code.

## Anti-Patterns & Fixes

- Deeply Nested Return-Code Pyramid: Using cascading if/else blocks around every operation to check return codes, obscuring normal logic flow. Fix: Use try/catch blocks to consolidate error handling in one place, letting the happy path read linearly.
- Exceptions as Normal Control Flow: Raising exceptions for conditions that are foreseeable and routine (e.g., a user-specified file that may not exist). Fix: Use return values or boolean returns for expected failure conditions; reserve exceptions for truly unexpected states.
- Single-Return-Statement Dogma: Forcing all error handling through a single return point leads to deeply nested, unreadable code. Fix: Allow multiple returns or use exception handling to keep normal flow clean.
- Tight Coupling via Exception Propagation: Routines and callers become tightly coupled when exceptions are used pervasively as signaling mechanisms. Fix: Use error handlers or wrapper classes to register error callbacks, reducing coupling between caller and callee.

## When To Apply

Load this page when:

- Use this when deciding whether a failed file open should throw an exception or return a boolean/error code.
- Use this when generating code that reads from a network socket or external resource and needs error handling without obscuring the main logic.
- Use this when a file or resource is expected to always exist (e.g., a system config file) and its absence represents a true program fault.
- Use this when a user-provided input (filename, URL, etc.) may legitimately not resolve, making failure a predictable condition rather than an exceptional one.
- Use this when wrapping RMI or remote calls that always require exception handling, to avoid polluting all call sites with boilerplate.
- Use this when reviewing generated code to check whether exceptions are being thrown and caught as a substitute for if/else logic.
- Use this when working in a language without native exception support (e.g., C) and considering whether to simulate exceptions with longjmp/setjmp.

## Concrete Examples

- Deeply nested socket.read() calls using return codes and if/else, versus the same logic rewritten with try/catch to isolate IOException handling.
- Opening /etc/passwd (expected to exist on Unix) with FileInputStream — exception is warranted because absence is unexpected.
- Opening a user-specified file from the command line — exception is not warranted; the routine returns false if the file does not exist, using a conventional error return.
- RMI client-server application where every remote call must handle RemoteException — solved by wrapping remote objects in a non-remote class that uses error handler registration.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**When to Use Exceptions**

LLM agents tend to over-apply exceptions uniformly — either throwing exceptions on every error condition (including predictable ones like missing user files) or swallowing exceptions silently to keep generated code 'clean.' This chapter prevents agents from generating spaghetti-by-exception code where try/catch blocks substitute for simple conditional logic, and from creating tight coupling between generated modules through unnecessary exception propagation. Agents should apply the remove-all-handlers test when reviewing generated error handling to distinguish exceptional from expected failure paths.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
