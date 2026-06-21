---
title: Discretionary Access Control (DAC): Protection left to the machine operator or user, allowing principals to manage their own file security; foundation of Unix/Windows permission systems
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
sources: [extracts/security-engineering/Access-Control.json]
contributing_chapters: ["Access Control"]
confidence: high
---

# Discretionary Access Control (DAC): Protection left to the machine operator or user, allowing principals to manage their own file security; foundation of Unix/Windows permission systems

> From chapter: *Access Control*

## Core Principle

Access control governs which principals can access which resources at every layer of a system stack, from hardware memory management up through OS, middleware, and application logic; controls grow more expressive but less reliable as they ascend the stack. The core mechanisms — access matrices, ACLs, capabilities, groups, and roles — all exist to enforce least privilege and limit blast radius from errors or malice, but they are systematically undermined by complexity, poor usability, and legacy assumptions of a cooperative user base. Most real-world access control failures trace to implementation bugs, administrative mistakes in large permission sets, or usability failures that cause developers to choose unsafe defaults.

## Key Heuristics

These are the load-bearing rules for this concept.

> Anything your computer can do for you it can potentially do for someone else.

> As we work up from the hardware through the operating system and middleware to the application layer, the controls become progressively more complex and less reliable.

> The main function of access control is to limit the damage that can be done by particular groups, users, and programs whether through error or malice.

> Most attacks involve the opportunistic exploitation of bugs; products that are complex, widely used, or both are particularly likely to have vulnerabilities found and turned into exploits.

> Many if not most technical security failures are due at least in part to the poor usability of the protection mechanisms that developers are expected to use.

> Access control matrices don't scale well: a bank with 50,000 staff and 300 applications would have a matrix of 15,000,000 entries, which might not only impose a performance overhead but also be vulnerable to administrators' mistakes.

## Anti-Patterns & Fixes

- Flat Access Control Matrix at Scale: Using a raw user-by-resource matrix for large organizations creates millions of entries, causing administrative errors and performance problems. Fix: Compress via groups/roles (compress users) or ACLs/capabilities (compress rights).
- Unrestricted Write Access to Sensitive Data: Allowing users or admins direct write access to files like account data bypasses integrity constraints (e.g., double-entry bookkeeping). Fix: Enforce write access only through a trusted intermediary program, using access triples (user, program, file).
- Duplicated Access Controls Across Layers Without Coherence: Implementing the same access-control logic redundantly at app, middleware, and OS layers without coordination produces inconsistency and gaps. Fix: Understand which layer owns each control and ensure higher layers supplement rather than silently contradict lower ones.
- Assuming Cooperative, Skilled, Trustworthy Users: Early OS security assumed a small community of known, mostly trustworthy users. Fix: Design for a hostile, unskilled, and potentially adversarial user population at internet scale.
- Granting Administrator Privileges by Default: Legacy applications that require admin privileges to run export excessive permissions to all their code paths. Fix: Use least-privilege sandboxing, virtualization, or compatibility shims rather than elevating the entire process.

## When To Apply

Load this page when:

- Use this when designing file or API permission systems and needing to decide between ACLs (per-resource lists) and capability tokens (per-principal tickets).
- Use this when a coding agent is scaffolding multi-tenant applications and must isolate one tenant's data from another's at the middleware or OS layer.
- Use this when generating database access logic that must enforce integrity constraints (e.g., balanced transactions), requiring write access only through a validated program interface rather than direct table access.
- Use this when assigning roles and groups in an IAM or RBAC system, needing to distinguish between a group (list of principals) and a role (set of permissions assumed temporarily).
- Use this when an application requests or grants broad permissions (e.g., admin, root, superuser) and a least-privilege alternative should be proposed instead.
- Use this when evaluating whether access controls at the application layer are redundant with or conflicting with OS-level or middleware-level controls.
- Use this when designing sandbox boundaries for plugins, third-party code, or user-submitted scripts that must not access host resources outside their designated domain.
- Use this when a system must support auditability, ensuring that audit trails are readable but not writable even by administrators.

## Concrete Examples

- Bank bookkeeping access matrix: Sam (admin), Alice (manager), Bob (auditor) with a separate 'Accounts Program' principal that is the only entity allowed to write to accounting data, enforcing double-entry integrity.
- Android phone treating apps from different companies as different users, protecting their data from each other — mirroring browser same-origin policy at the OS layer.
- Ship officer-of-the-watch as a canonical role example: exactly one watchkeeper at a time, with a formal handoff procedure, illustrating time-bounded assumption of a fixed permission set.
- Bank branch manager policy: 'transfers over $10m must be approved by two staff, one with rank at least manager and one with rank at least assistant accountant' — showing how groups and roles combine for separation-of-duty enforcement.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Access Control**

An LLM coding agent is prone to generating access control logic that is superficially correct but over-permissive — defaulting to broad roles, direct DB writes, or admin-level process privileges because those patterns appear most frequently in training data and resolve immediate functional requirements without raising errors. Unlike a human developer who may be prompted by a code review or security audit, an agent will not self-correct unless the policy constraints are explicitly present in the prompt or enforced by a linting/analysis tool. The ACL-vs-capability distinction and the principle of mediating writes through trusted programs (not granting direct file access) are particularly likely to be collapsed or ignored by an agent generating boilerplate CRUD or IAM scaffolding.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
