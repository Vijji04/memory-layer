---
title: Dependency Injection Boundary: All DI framework usage is confined to Main; dependencies are then distributed normally (without the framework) throughout the rest of the system
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, clean-architecture, concept]
sources: [extracts/clean-architecture/Chapter-26-The-Main-Component.json]
contributing_chapters: ["Chapter 26: The Main Component"]
confidence: high
---

# Dependency Injection Boundary: All DI framework usage is confined to Main; dependencies are then distributed normally (without the framework) throughout the rest of the system

> From chapter: *Chapter 26: The Main Component*

## Core Principle

The Main component is the system's lowest-level, dirtiest plugin: its sole responsibility is to instantiate and wire all factories, strategies, and global facilities using a DI framework, then hand control entirely to the high-level abstract portions of the system. Because Main is a plugin behind an architectural boundary, multiple Main components can exist for different environments or configurations without touching any application logic. Keeping all construction, configuration, and bootstrapping detail confined to Main protects higher-level components from dependency on concrete implementations.

## Key Heuristics

These are the load-bearing rules for this concept.

> Think of Main as the dirtiest of all the dirty components.

> The Main component is the ultimate detail—the lowest-level policy.

> Think of Main as a plugin to the application—a plugin that sets up the initial conditions and configurations, gathers all the outside resources, and then hands control over to the high-level policy of the application.

> Once [dependencies] are injected into Main, Main should distribute those dependencies normally, without using the framework.

> Since it is a plugin, it is possible to have many Main components, one for each configuration of your application.

> When you think about Main as a plugin component, sitting behind an architectural boundary, the problem of configuration becomes a lot easier to solve.

## Anti-Patterns & Fixes

- DI-Framework Leakage: Allowing the Dependency Injection framework to be used throughout the entire codebase rather than only in Main. Fix: Restrict all DI framework calls to Main; pass resolved dependencies manually to downstream components.
- Business Logic in Main: Placing application logic, domain rules, or processing inside the Main component. Fix: Main should only wire, configure, and delegate — all real logic belongs in higher-level components that Main calls into.
- Single Monolithic Main: Using one Main component for all environments (dev, test, prod, regions, customers), causing configuration entanglement. Fix: Create separate Main plugin implementations per deployment configuration.
- High-Level Awareness of Low-Level Details: Letting the main body of the application know about concrete class names, strings, or environment-specific data. Fix: Load all such dirty details in Main and pass only abstractions upward.

## When To Apply

Load this page when:

- Use this when designing the entry point of a new application and deciding where to place object construction and wiring logic.
- Use this when a Dependency Injection framework is being used and you need to decide how far its usage should propagate through the codebase.
- Use this when you need to support multiple deployment environments (dev, test, prod) or multiple customer/jurisdiction configurations from a single codebase.
- Use this when a low-level concrete class change is causing unnecessary recompilation or redeployment of higher-level modules.
- Use this when determining which component should own loading of configuration strings, environment data, or other 'dirty' setup details.
- Use this when applying Clean Architecture and deciding which layer is responsible for bootstrapping Factories, Strategies, and global facilities.

## Concrete Examples

- Hunt the Wumpus Main class: loads environment strings, shapes, cavern types, and adornments; uses HtwFactory.makeGame() with a class name string to avoid recompile coupling; creates the map and contains the main game loop before delegating all processing to higher-level components.
- HtwFactory.makeGame() called with the string 'htw.game.HuntTheWumpusFacade' so that changes to that dirtier class do not force Main to recompile or redeploy.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 26: The Main Component**

An LLM coding agent tends to scatter initialization logic, object construction, and DI wiring throughout generated files because it optimizes locally for each file it produces, lacking a global architectural view — this pattern gives the agent an explicit rule: all wiring belongs in one Main component. Agents are also prone to generating a single monolithic bootstrap that conflates dev/test/prod concerns; the Main-as-Plugin model gives the agent a concrete structural directive to generate separate Main implementations per configuration. Without this framework, an agent may inadvertently push framework-specific DI calls deep into domain or use-case layers, creating tight coupling that is hard to detect in review.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/clean-architecture/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
