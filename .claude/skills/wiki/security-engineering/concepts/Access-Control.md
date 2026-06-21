---
title: Access Control
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 8 pages
---

# Access Control

> Consolidated from 8 related concept pages.

---

## Access Control List ACL vs Capabilities ACLs store the access matrix column by c

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

---

## Access Control Matrix A two  or three dimensional model mapping principals users

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

---

## Discretionary Access Control DAC Protection left to the machine operator or user

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

---

## Groups and Roles Model Groups are lists of principals roles are fixed sets of ac

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

---

## Mandatory Access Control MAC Vendor  or OS controlled protection that limits wha

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

---

## Protection Domain A set of processes or threads sharing access to the same resou

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

---

## Role Based Access Control RBAC Assigns permissions based on organizational roles

## Core Principle

Chapter 10 establishes that the primary boundary challenge in large systems is not preventing downward information flow (hierarchical secrecy) but preventing lateral flow between peer groups who should not share data. It surveys technical mechanisms — compartments, lattice models, RBAC, Chinese walls — and finds that the hard problems are almost always policy and incentive failures rather than mechanism failures: organizations lack motivation to implement fine-grained controls, anonymization is routinely overestimated, and side-channel leakage through metadata undermines primary controls. The chapter's core prescription is the 'fox' approach: deep application-specific adversarial thinking rather than reliance on any single universal security model.

## Key Heuristics

These are the load-bearing rules for this concept.

> If you centralise systems containing sensitive information, you create a more valuable asset and simultaneously give more people access to it. Just as the benefits of networks can scale more than linearly, so can the harms.

> The easy problem is setting up access controls in a direct care setting so that access to each record is limited to a sensible number of staff. Such systems can be designed by automating existing working practices.

> Multilateral security requires the 'fox' approach; you need to understand your application in detail, learn what's gone wrong in the past – and also be good at adversarial thinking if you want to anticipate what's likely to go wrong in future.

> The real problems facing users of intelligence systems have to do with combining data in different compartments, and downgrading it after sanitization. Lattice security models offer little help here.

> The policy goal is usually not to prevent information flowing 'down' a hierarchy but to prevent it flowing 'across' between smaller groups.

> Doctors, bankers and spies have all learned that as well as preventing overt information flows, they also have to prevent information leakage through side-channels such as billing data.

> The traditional approach to privacy, which might be summarised as 'consent or anonymise', is being undermined by growing complexity with many outsourced systems that are often opaque even to doctors (let alone patients).

## Anti-Patterns & Fixes

- Over-Centralization: Aggregating all sensitive data into one system to improve sharing simultaneously maximizes attacker value and insider threat surface. Fix: Partition data into compartments with incompatible labels; grant access only to the compartment relevant to a user's current task.
- Flat Access on Seniority: Granting cumulative access to many compartments as a reward for long service (e.g., Aldrich Ames) creates catastrophic insider threat potential. Fix: Enforce need-to-know per compartment regardless of seniority; regularly audit and revoke stale access.
- Treating Anonymization as a Privacy Silver Bullet: Building 'anonymised' databases of rich records assumes re-identification is impossible, but computer scientists have known since the 1980s this is far harder than it looks. Fix: Apply formal de-identification theory (e.g., k-anonymity, differential privacy) and assess re-identification risk before releasing aggregate data.
- Using the OS as a Sharing Mechanism After Labeling It for Isolation: Mandatory access control products used for compartmentation turn the OS into an isolation mechanism, making legitimate data combination across compartments operationally impossible. Fix: Design explicit, audited downgrade/sanitization workflows rather than relying purely on label-based blocking.
- Uniform Navy-Style Key Distribution: Operational necessity (a ship can be sent anywhere) forced all 800 US Navy ships onto the same cipher keys, which the Walker family then sold wholesale. Fix: Design for operational flexibility from the start with key hierarchies or per-mission keying rather than retrofitting uniformity.
- Ignoring Side-Channel Leakage: Restricting record content while leaving billing, scheduling, or referral metadata accessible leaks sensitive inferences (e.g., patient X paid specialist Y implies diagnosis). Fix: Apply boundary controls to all correlated metadata, not just primary record content.

## When To Apply

Load this page when:

- Use this when designing an API or database schema that must serve multiple organizational units where one unit should not see another's data (e.g., multi-tenant SaaS, federated health systems).
- Use this when implementing access control for a system where the same data store is accessed by users with conflicting interests (e.g., financial advisors whose clients compete with each other).
- Use this when a feature request asks for 'data sharing' between departments, teams, or organizations and the requester has not specified what lateral boundaries must be preserved.
- Use this when generating code that aggregates or exports records and the records contain quasi-identifiers that could enable re-identification even after obvious PII is stripped.
- Use this when building role-based access control and the role definitions are being inherited from organizational hierarchy rather than derived from actual data-access need.
- Use this when a logging, billing, or audit system is being designed alongside a privacy-sensitive primary system, as the metadata may leak as much as the primary data.
- Use this when a system's access model relies on a single classification level (e.g., 'Top Secret') without codeword-style compartments, and the user population with that level exceeds a small, well-audited group.
- Use this when evaluating whether a proposed 'anonymized' data release from a rich dataset is actually safe to publish externally.

## Concrete Examples

- Ultra codeword in WWII: Only a tiny compartment of Allied leaders and generals could access Enigma decrypts; Churchill received summaries in a locked dispatch box inaccessible to his own staff.
- Aldrich Ames CIA case: Long-service counterintelligence officer accumulated access to a large number of compartments and betrayed nearly the entire US agent network in Russia.
- Walker spy case: Operational necessity forced all 800 US Navy ships onto the same cipher keys, which were then sold wholesale to the Russians.
- UK Children's Database (ContactPoint): Parliament shut it down in 2010 after realizing that giving doctors, teachers, and social workers shared access to all children's data was both unsafe and illegal.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Boundaries**

An LLM coding agent defaults to generating the simplest schema and access control that satisfies the stated functional requirement, which almost always means a flat, centralized model with role-based read permissions — exactly the over-centralization anti-pattern. The agent has no visibility into cross-unit conflict-of-interest risks or side-channel leakage through metadata it generates (e.g., audit logs, foreign keys, timestamps), so it will produce code that is functionally correct but structurally violates lateral boundary requirements. Agents must be explicitly prompted with compartment boundaries, conflict-of-interest rules, and metadata leakage constraints before generating any multi-tenant or multi-role data access layer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## TOCTTOU Time of Check to Time of Use A class of concurrency attack where securit

## Core Principle

Distributed systems security fails most often not from cryptographic weakness but from concurrency bugs, stale security state, and naming ambiguity — problems that have had known solutions in computer science for decades. The core design disciplines are: treat security state propagation as expensive and design tiered revocation accordingly; use atomicity or pre-authorization locks to prevent TOCTTOU attacks; and scope identifiers narrowly to a single purpose to avoid cross-system naming collisions. Fault tolerance mechanisms must account for Byzantine (adversarial) failure, not just random failure, and systems must be designed to degrade gracefully and recover cleanly when security state is corrupted.

## Key Heuristics

These are the load-bearing rules for this concept.

> A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable.

> Many security breaches are concurrency failures of one kind or another; systems use old data, make updates inconsistently or in the wrong order, or assume that data are consistent when they aren't or even can't be.

> Revoking compromised credentials quickly and on a global scale is expensive.

> It's always a good idea for engineers to study failures; we learn more from the one bridge that falls down than from the thousand that don't.

> As systems scale, it becomes less realistic to rely on names that are simple, interchangeable and immutable.

> The simplest solution is often to assign each principal a unique identifier used for no other purpose, such as a bank account number or a system logon name.

> Many secure distributed systems have incurred large costs, or developed serious vulnerabilities, because their designers ignored the basics of how to build (and how not to build) distributed systems. Most of these basics have been in computer science textbooks for a generation.

> You need to scope naming carefully, understand who controls the names on which you rely, work out how slippery they are, and design your system to be dependable despite their limitations.

## Anti-Patterns & Fixes

- Global Instant Revocation Assumption: Assuming that revoking a credential (key, certificate, card) propagates instantly everywhere. Fix: Design tiered or asynchronous revocation with defined staleness tolerances and fallback behaviors for each trust tier.
- Overloaded Identifiers: Making a single name or ID serve multiple purposes across systems, cultures, or jurisdictions — causing failures when one function is revoked or systems are merged. Fix: Assign each principal a unique identifier used for no other purpose.
- Centralization as Silver Bullet: Centralizing credential management to cut costs without accounting for single-point-of-compromise risk (e.g., Diginotar). Fix: Combine centralization with robust incident response, fast revocation paths, and redundant certificate authorities.
- Ignoring TOCTTOU in Business Logic: Checking security state (permissions, credentials, balances) at one time and acting on a cached result later, without re-validation. Fix: Re-check security state atomically at the point of action, or use locking/pre-authorization to hold state between check and use.
- Assuming Name Stability Across Systems: Treating names (URLs, usernames, device IDs) as immutable and globally unambiguous when merging systems or operating at scale. Fix: Scope names explicitly, document their authority and mutability, and design logic to tolerate name changes or collisions.
- Redundancy Without Byzantine Awareness: Adding replication for fault tolerance without considering that replicas can be compromised and conspire, increasing attack surface. Fix: Apply Byzantine fault-tolerant consensus protocols and cryptographic verification across replicas.

## When To Apply

Load this page when:

- Use this when designing an authorization or permissions check that reads state from a database or cache before performing a privileged operation — check for TOCTTOU vulnerability.
- Use this when implementing credential revocation (tokens, API keys, certificates) in a distributed system — apply tiered propagation with explicit staleness budgets rather than assuming instant global consistency.
- Use this when two systems with different user identity or naming schemes are being integrated or merged — audit identifier semantics before assuming equivalence.
- Use this when adding replication or redundancy to a security-sensitive service — evaluate whether Byzantine failure (compromised replica) is in scope and whether consensus mechanisms are needed.
- Use this when a service depends on a third-party identity provider or certificate authority — model the failure scenario where that provider is compromised and design a recovery path.
- Use this when designing a distributed transaction that spans multiple services (e.g., booking, payment, inventory) — identify all points where stale or inconsistent security state could be exploited.
- Use this when building a callback or notification system for security state changes — verify the publish-register-notify model is correctly implemented so relying parties are informed before acting on stale state.
- Use this when generating unique identifiers for users, sessions, or resources in a new system — ensure each identifier is purpose-scoped and not reused across unrelated functions.

## Concrete Examples

- Unix 'mkdir' vulnerability: a privileged two-phase operation could be attacked mid-execution by renaming the target object between phases — a classic TOCTTOU race condition.
- IBM OS/360 file permission check: file permissions were checked on first read, but the file was read again after — an attacker could swap the file between the two reads.
- Payment card floor limits: merchant terminals process low-value transactions offline against a stale hot-card list, escalating to online verification only for larger amounts — a tiered stand-in processing architecture.
- Diginotar CA compromise (2011): Iranian hackers compromised a Dutch certificate authority, generated fake Gmail certificates for man-in-the-middle attacks on activists, and the delayed revocation response caused Dutch public services to go offline for days.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Distributed Systems Security**

An LLM coding agent is especially prone to generating TOCTTOU vulnerabilities because it writes check-then-act patterns naturally (read permission, then perform action) without inserting atomic guards or re-validation at the use point — the human intuition that 'something could change between those two lines' is often absent. Agents also tend to generate overloaded identifiers (reusing usernames or emails as foreign keys across tables) because the pattern is common in training data, violating the principle of purpose-scoped unique identifiers. When generating distributed system scaffolding, agents may omit Byzantine failure considerations entirely, producing replication logic that assumes all replicas are honest — a safe assumption for availability but dangerous for security.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
