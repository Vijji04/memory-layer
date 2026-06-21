---
title: Financial Security Controls
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, security-engineering, concept]
confidence: high
consolidated_from: 5 pages
---

# Financial Security Controls

> Consolidated from 5 related concept pages.

---

## Audit Trail with Immutability Records of who did what and when must be append on

## Core Principle

Banking and bookkeeping systems derive their integrity guarantees from double-entry bookkeeping (every transaction must produce a zero-sum balance), dual control (splitting responsibility so fraud requires collusion), and immutable audit trails — with confidentiality being secondary to record integrity. These controls, developed over centuries, are routinely undermined when computerised systems enforce them only at the UI layer while leaving the underlying data accessible to technical staff. The chapter maps the full payment stack from core banking ledgers through ATMs, card networks, and open banking, showing how fraud migrates to whichever layer has the weakest controls.

## Key Heuristics

These are the load-bearing rules for this concept.

> Debit the receiver, credit the giver.

> If the bank (or one of its branches) is ever out of balance, an alarm will go off, some processing will stop, and inspectors will start looking for the cause.

> A programmer who wants to add to their own account balance has to take the money from some other account, rather than just creating it out of thin air by tweaking the account master file.

> In banking and bookkeeping, confidentiality plays little role, but the integrity of records (and their immutability once made) is paramount.

> Most frauds need the collusion of two or more people.

> As EMV implementations get tightened up, we can expect fraud to move to the periphery: to the customer, via account takeover; to the merchant, via hacking attacks; and to the bank, via pre-issue frauds.

> Blaming ordinary customers for harm they suffer from systems designed by others is wrong.

## Anti-Patterns & Fixes

- UI-Only Separation of Duty: Separation-of-duty features are implemented as a skin in the user interface while the underlying data are open to manipulation by technical staff. Fix: Enforce access controls at the data layer (e.g., database permissions, cryptographic signing of records), not just in the application UI.
- Single-Database Ledger Collapse: All ledgers are just views of one single database, so someone with physical access and a database editing tool can bypass all bookkeeping controls. Fix: Enforce ledger separation at the storage and permission level, not only at the query/view level.
- Missing Audit on Sensitive Operations: One bank did not audit address changes, allowing a cashier to change a customer's address, issue an extra bank card, and change it back again. Fix: Log and audit every sensitive field change, not just financial transactions.
- Batch-Only Reconciliation: Performing balance checks only in overnight batch processes means errors and fraud can compound in real time before detection. Fix: Implement continuous or near-real-time balance reconciliation with automated alerting on any imbalance.
- Circumventing Legacy Controls in New Systems: Global-scale systems designed to circumvent the checks and balances that had evolved over centuries in local and manual systems create new fraud vectors. Fix: Explicitly map and reimplement each legacy control when building replacement systems, rather than assuming the old constraints no longer apply.

## When To Apply

Load this page when:

- Use this when designing a financial transaction processing system that must detect theft or manipulation by internal users (developers, DBAs, ops staff).
- Use this when implementing a ledger or accounting module and deciding whether to use a single unified database table or separate, independently reconcilable data structures.
- Use this when building an audit logging system for a payment or banking application and deciding which fields and operations must be logged.
- Use this when adding a privileged administrative operation (e.g., address change, account merge, card issuance) and determining whether it needs a second-approver workflow.
- Use this when migrating a legacy banking or bookkeeping system to a new platform and needing to preserve internal controls that were implicit in the old architecture.
- Use this when generating or reviewing code that modifies account balances, and needing to verify that every debit has a corresponding credit and the system cannot create value from nothing.
- Use this when designing access controls for a core banking database, specifically to ensure that application-layer role checks cannot be bypassed by direct database access.
- Use this when assessing compliance requirements (Sarbanes-Oxley, PCI DSS, Gramm-Leach-Bliley) and translating them into concrete technical control requirements.

## Concrete Examples

- A cashier at a bank exploited the absence of auditing on address changes: he changed a customer's address, issued an extra bank card, then changed the address back — the loophole went undetected because address changes were not audited.
- The Leo computer (1951) was the first non-military/academic computer and was used to do bookkeeping for the Lyons chain of coffee houses, illustrating that bookkeeping drove the entire computer industry.
- Clay token bullae from ~3300 BC Uruk: each unit of stored food was represented by a clay token sealed inside a baked clay envelope, broken only by the keeper in the presence of a witness — described as possibly the oldest known security protocol.
- James Ritty's 1879 'Incorruptible Cashier' cash register with bell and paper tape was invented because saloon employees stole from him, leading to NCR and eventually IBM.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Banking and Bookkeeping**

An LLM coding agent is particularly prone to the 'UI-Only Separation of Duty' anti-pattern: when asked to implement role-based access for a ledger, it will naturally generate application-layer checks (if/else on user role) while leaving the underlying database tables fully writable by any connection string — exactly the failure mode described for systems where 'the separation-of-duty features may be just a skin in the user interface.' Agents also tend to implement balance updates as single-table mutations rather than double-entry pairs, making it possible to create or destroy value without a corresponding counter-entry and breaking the zero-sum invariant that triggers fraud detection. The trigger for invoking this chapter's knowledge is any agent task involving account balances, ledger writes, or privileged financial operations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Double Entry Bookkeeping Every transaction is posted to two separate books as a

## Core Principle

Banking and bookkeeping systems derive their integrity guarantees from double-entry bookkeeping (every transaction must produce a zero-sum balance), dual control (splitting responsibility so fraud requires collusion), and immutable audit trails — with confidentiality being secondary to record integrity. These controls, developed over centuries, are routinely undermined when computerised systems enforce them only at the UI layer while leaving the underlying data accessible to technical staff. The chapter maps the full payment stack from core banking ledgers through ATMs, card networks, and open banking, showing how fraud migrates to whichever layer has the weakest controls.

## Key Heuristics

These are the load-bearing rules for this concept.

> Debit the receiver, credit the giver.

> If the bank (or one of its branches) is ever out of balance, an alarm will go off, some processing will stop, and inspectors will start looking for the cause.

> A programmer who wants to add to their own account balance has to take the money from some other account, rather than just creating it out of thin air by tweaking the account master file.

> In banking and bookkeeping, confidentiality plays little role, but the integrity of records (and their immutability once made) is paramount.

> Most frauds need the collusion of two or more people.

> As EMV implementations get tightened up, we can expect fraud to move to the periphery: to the customer, via account takeover; to the merchant, via hacking attacks; and to the bank, via pre-issue frauds.

> Blaming ordinary customers for harm they suffer from systems designed by others is wrong.

## Anti-Patterns & Fixes

- UI-Only Separation of Duty: Separation-of-duty features are implemented as a skin in the user interface while the underlying data are open to manipulation by technical staff. Fix: Enforce access controls at the data layer (e.g., database permissions, cryptographic signing of records), not just in the application UI.
- Single-Database Ledger Collapse: All ledgers are just views of one single database, so someone with physical access and a database editing tool can bypass all bookkeeping controls. Fix: Enforce ledger separation at the storage and permission level, not only at the query/view level.
- Missing Audit on Sensitive Operations: One bank did not audit address changes, allowing a cashier to change a customer's address, issue an extra bank card, and change it back again. Fix: Log and audit every sensitive field change, not just financial transactions.
- Batch-Only Reconciliation: Performing balance checks only in overnight batch processes means errors and fraud can compound in real time before detection. Fix: Implement continuous or near-real-time balance reconciliation with automated alerting on any imbalance.
- Circumventing Legacy Controls in New Systems: Global-scale systems designed to circumvent the checks and balances that had evolved over centuries in local and manual systems create new fraud vectors. Fix: Explicitly map and reimplement each legacy control when building replacement systems, rather than assuming the old constraints no longer apply.

## When To Apply

Load this page when:

- Use this when designing a financial transaction processing system that must detect theft or manipulation by internal users (developers, DBAs, ops staff).
- Use this when implementing a ledger or accounting module and deciding whether to use a single unified database table or separate, independently reconcilable data structures.
- Use this when building an audit logging system for a payment or banking application and deciding which fields and operations must be logged.
- Use this when adding a privileged administrative operation (e.g., address change, account merge, card issuance) and determining whether it needs a second-approver workflow.
- Use this when migrating a legacy banking or bookkeeping system to a new platform and needing to preserve internal controls that were implicit in the old architecture.
- Use this when generating or reviewing code that modifies account balances, and needing to verify that every debit has a corresponding credit and the system cannot create value from nothing.
- Use this when designing access controls for a core banking database, specifically to ensure that application-layer role checks cannot be bypassed by direct database access.
- Use this when assessing compliance requirements (Sarbanes-Oxley, PCI DSS, Gramm-Leach-Bliley) and translating them into concrete technical control requirements.

## Concrete Examples

- A cashier at a bank exploited the absence of auditing on address changes: he changed a customer's address, issued an extra bank card, then changed the address back — the loophole went undetected because address changes were not audited.
- The Leo computer (1951) was the first non-military/academic computer and was used to do bookkeeping for the Lyons chain of coffee houses, illustrating that bookkeeping drove the entire computer industry.
- Clay token bullae from ~3300 BC Uruk: each unit of stored food was represented by a clay token sealed inside a baked clay envelope, broken only by the keeper in the presence of a witness — described as possibly the oldest known security protocol.
- James Ritty's 1879 'Incorruptible Cashier' cash register with bell and paper tape was invented because saloon employees stole from him, leading to NCR and eventually IBM.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Banking and Bookkeeping**

An LLM coding agent is particularly prone to the 'UI-Only Separation of Duty' anti-pattern: when asked to implement role-based access for a ledger, it will naturally generate application-layer checks (if/else on user role) while leaving the underlying database tables fully writable by any connection string — exactly the failure mode described for systems where 'the separation-of-duty features may be just a skin in the user interface.' Agents also tend to implement balance updates as single-table mutations rather than double-entry pairs, making it possible to create or destroy value without a corresponding counter-entry and breaking the zero-sum invariant that triggers fraud detection. The trigger for invoking this chapter's knowledge is any agent task involving account balances, ledger writes, or privileged financial operations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Dual Control Multi Party Authorisation MPA Split responsibility so that most fra

## Core Principle

Banking and bookkeeping systems derive their integrity guarantees from double-entry bookkeeping (every transaction must produce a zero-sum balance), dual control (splitting responsibility so fraud requires collusion), and immutable audit trails — with confidentiality being secondary to record integrity. These controls, developed over centuries, are routinely undermined when computerised systems enforce them only at the UI layer while leaving the underlying data accessible to technical staff. The chapter maps the full payment stack from core banking ledgers through ATMs, card networks, and open banking, showing how fraud migrates to whichever layer has the weakest controls.

## Key Heuristics

These are the load-bearing rules for this concept.

> Debit the receiver, credit the giver.

> If the bank (or one of its branches) is ever out of balance, an alarm will go off, some processing will stop, and inspectors will start looking for the cause.

> A programmer who wants to add to their own account balance has to take the money from some other account, rather than just creating it out of thin air by tweaking the account master file.

> In banking and bookkeeping, confidentiality plays little role, but the integrity of records (and their immutability once made) is paramount.

> Most frauds need the collusion of two or more people.

> As EMV implementations get tightened up, we can expect fraud to move to the periphery: to the customer, via account takeover; to the merchant, via hacking attacks; and to the bank, via pre-issue frauds.

> Blaming ordinary customers for harm they suffer from systems designed by others is wrong.

## Anti-Patterns & Fixes

- UI-Only Separation of Duty: Separation-of-duty features are implemented as a skin in the user interface while the underlying data are open to manipulation by technical staff. Fix: Enforce access controls at the data layer (e.g., database permissions, cryptographic signing of records), not just in the application UI.
- Single-Database Ledger Collapse: All ledgers are just views of one single database, so someone with physical access and a database editing tool can bypass all bookkeeping controls. Fix: Enforce ledger separation at the storage and permission level, not only at the query/view level.
- Missing Audit on Sensitive Operations: One bank did not audit address changes, allowing a cashier to change a customer's address, issue an extra bank card, and change it back again. Fix: Log and audit every sensitive field change, not just financial transactions.
- Batch-Only Reconciliation: Performing balance checks only in overnight batch processes means errors and fraud can compound in real time before detection. Fix: Implement continuous or near-real-time balance reconciliation with automated alerting on any imbalance.
- Circumventing Legacy Controls in New Systems: Global-scale systems designed to circumvent the checks and balances that had evolved over centuries in local and manual systems create new fraud vectors. Fix: Explicitly map and reimplement each legacy control when building replacement systems, rather than assuming the old constraints no longer apply.

## When To Apply

Load this page when:

- Use this when designing a financial transaction processing system that must detect theft or manipulation by internal users (developers, DBAs, ops staff).
- Use this when implementing a ledger or accounting module and deciding whether to use a single unified database table or separate, independently reconcilable data structures.
- Use this when building an audit logging system for a payment or banking application and deciding which fields and operations must be logged.
- Use this when adding a privileged administrative operation (e.g., address change, account merge, card issuance) and determining whether it needs a second-approver workflow.
- Use this when migrating a legacy banking or bookkeeping system to a new platform and needing to preserve internal controls that were implicit in the old architecture.
- Use this when generating or reviewing code that modifies account balances, and needing to verify that every debit has a corresponding credit and the system cannot create value from nothing.
- Use this when designing access controls for a core banking database, specifically to ensure that application-layer role checks cannot be bypassed by direct database access.
- Use this when assessing compliance requirements (Sarbanes-Oxley, PCI DSS, Gramm-Leach-Bliley) and translating them into concrete technical control requirements.

## Concrete Examples

- A cashier at a bank exploited the absence of auditing on address changes: he changed a customer's address, issued an extra bank card, then changed the address back — the loophole went undetected because address changes were not audited.
- The Leo computer (1951) was the first non-military/academic computer and was used to do bookkeeping for the Lyons chain of coffee houses, illustrating that bookkeeping drove the entire computer industry.
- Clay token bullae from ~3300 BC Uruk: each unit of stored food was represented by a clay token sealed inside a baked clay envelope, broken only by the keeper in the presence of a witness — described as possibly the oldest known security protocol.
- James Ritty's 1879 'Incorruptible Cashier' cash register with bell and paper tape was invented because saloon employees stole from him, leading to NCR and eventually IBM.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Banking and Bookkeeping**

An LLM coding agent is particularly prone to the 'UI-Only Separation of Duty' anti-pattern: when asked to implement role-based access for a ledger, it will naturally generate application-layer checks (if/else on user role) while leaving the underlying database tables fully writable by any connection string — exactly the failure mode described for systems where 'the separation-of-duty features may be just a skin in the user interface.' Agents also tend to implement balance updates as single-table mutations rather than double-entry pairs, making it possible to create or destroy value without a corresponding counter-entry and breaking the zero-sum invariant that triggers fraud detection. The trigger for invoking this chapter's knowledge is any agent task involving account balances, ledger writes, or privileged financial operations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Layered Transaction Processing Journals capture raw transactions ledgers accumul

## Core Principle

Banking and bookkeeping systems derive their integrity guarantees from double-entry bookkeeping (every transaction must produce a zero-sum balance), dual control (splitting responsibility so fraud requires collusion), and immutable audit trails — with confidentiality being secondary to record integrity. These controls, developed over centuries, are routinely undermined when computerised systems enforce them only at the UI layer while leaving the underlying data accessible to technical staff. The chapter maps the full payment stack from core banking ledgers through ATMs, card networks, and open banking, showing how fraud migrates to whichever layer has the weakest controls.

## Key Heuristics

These are the load-bearing rules for this concept.

> Debit the receiver, credit the giver.

> If the bank (or one of its branches) is ever out of balance, an alarm will go off, some processing will stop, and inspectors will start looking for the cause.

> A programmer who wants to add to their own account balance has to take the money from some other account, rather than just creating it out of thin air by tweaking the account master file.

> In banking and bookkeeping, confidentiality plays little role, but the integrity of records (and their immutability once made) is paramount.

> Most frauds need the collusion of two or more people.

> As EMV implementations get tightened up, we can expect fraud to move to the periphery: to the customer, via account takeover; to the merchant, via hacking attacks; and to the bank, via pre-issue frauds.

> Blaming ordinary customers for harm they suffer from systems designed by others is wrong.

## Anti-Patterns & Fixes

- UI-Only Separation of Duty: Separation-of-duty features are implemented as a skin in the user interface while the underlying data are open to manipulation by technical staff. Fix: Enforce access controls at the data layer (e.g., database permissions, cryptographic signing of records), not just in the application UI.
- Single-Database Ledger Collapse: All ledgers are just views of one single database, so someone with physical access and a database editing tool can bypass all bookkeeping controls. Fix: Enforce ledger separation at the storage and permission level, not only at the query/view level.
- Missing Audit on Sensitive Operations: One bank did not audit address changes, allowing a cashier to change a customer's address, issue an extra bank card, and change it back again. Fix: Log and audit every sensitive field change, not just financial transactions.
- Batch-Only Reconciliation: Performing balance checks only in overnight batch processes means errors and fraud can compound in real time before detection. Fix: Implement continuous or near-real-time balance reconciliation with automated alerting on any imbalance.
- Circumventing Legacy Controls in New Systems: Global-scale systems designed to circumvent the checks and balances that had evolved over centuries in local and manual systems create new fraud vectors. Fix: Explicitly map and reimplement each legacy control when building replacement systems, rather than assuming the old constraints no longer apply.

## When To Apply

Load this page when:

- Use this when designing a financial transaction processing system that must detect theft or manipulation by internal users (developers, DBAs, ops staff).
- Use this when implementing a ledger or accounting module and deciding whether to use a single unified database table or separate, independently reconcilable data structures.
- Use this when building an audit logging system for a payment or banking application and deciding which fields and operations must be logged.
- Use this when adding a privileged administrative operation (e.g., address change, account merge, card issuance) and determining whether it needs a second-approver workflow.
- Use this when migrating a legacy banking or bookkeeping system to a new platform and needing to preserve internal controls that were implicit in the old architecture.
- Use this when generating or reviewing code that modifies account balances, and needing to verify that every debit has a corresponding credit and the system cannot create value from nothing.
- Use this when designing access controls for a core banking database, specifically to ensure that application-layer role checks cannot be bypassed by direct database access.
- Use this when assessing compliance requirements (Sarbanes-Oxley, PCI DSS, Gramm-Leach-Bliley) and translating them into concrete technical control requirements.

## Concrete Examples

- A cashier at a bank exploited the absence of auditing on address changes: he changed a customer's address, issued an extra bank card, then changed the address back — the loophole went undetected because address changes were not audited.
- The Leo computer (1951) was the first non-military/academic computer and was used to do bookkeeping for the Lyons chain of coffee houses, illustrating that bookkeeping drove the entire computer industry.
- Clay token bullae from ~3300 BC Uruk: each unit of stored food was represented by a clay token sealed inside a baked clay envelope, broken only by the keeper in the presence of a witness — described as possibly the oldest known security protocol.
- James Ritty's 1879 'Incorruptible Cashier' cash register with bell and paper tape was invented because saloon employees stole from him, leading to NCR and eventually IBM.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Banking and Bookkeeping**

An LLM coding agent is particularly prone to the 'UI-Only Separation of Duty' anti-pattern: when asked to implement role-based access for a ledger, it will naturally generate application-layer checks (if/else on user role) while leaving the underlying database tables fully writable by any connection string — exactly the failure mode described for systems where 'the separation-of-duty features may be just a skin in the user interface.' Agents also tend to implement balance updates as single-table mutations rather than double-entry pairs, making it possible to create or destroy value without a corresponding counter-entry and breaking the zero-sum invariant that triggers fraud detection. The trigger for invoking this chapter's knowledge is any agent task involving account balances, ledger writes, or privileged financial operations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Separation of Duty Different clerks or system roles handle different ledgers pre

## Core Principle

Banking and bookkeeping systems derive their integrity guarantees from double-entry bookkeeping (every transaction must produce a zero-sum balance), dual control (splitting responsibility so fraud requires collusion), and immutable audit trails — with confidentiality being secondary to record integrity. These controls, developed over centuries, are routinely undermined when computerised systems enforce them only at the UI layer while leaving the underlying data accessible to technical staff. The chapter maps the full payment stack from core banking ledgers through ATMs, card networks, and open banking, showing how fraud migrates to whichever layer has the weakest controls.

## Key Heuristics

These are the load-bearing rules for this concept.

> Debit the receiver, credit the giver.

> If the bank (or one of its branches) is ever out of balance, an alarm will go off, some processing will stop, and inspectors will start looking for the cause.

> A programmer who wants to add to their own account balance has to take the money from some other account, rather than just creating it out of thin air by tweaking the account master file.

> In banking and bookkeeping, confidentiality plays little role, but the integrity of records (and their immutability once made) is paramount.

> Most frauds need the collusion of two or more people.

> As EMV implementations get tightened up, we can expect fraud to move to the periphery: to the customer, via account takeover; to the merchant, via hacking attacks; and to the bank, via pre-issue frauds.

> Blaming ordinary customers for harm they suffer from systems designed by others is wrong.

## Anti-Patterns & Fixes

- UI-Only Separation of Duty: Separation-of-duty features are implemented as a skin in the user interface while the underlying data are open to manipulation by technical staff. Fix: Enforce access controls at the data layer (e.g., database permissions, cryptographic signing of records), not just in the application UI.
- Single-Database Ledger Collapse: All ledgers are just views of one single database, so someone with physical access and a database editing tool can bypass all bookkeeping controls. Fix: Enforce ledger separation at the storage and permission level, not only at the query/view level.
- Missing Audit on Sensitive Operations: One bank did not audit address changes, allowing a cashier to change a customer's address, issue an extra bank card, and change it back again. Fix: Log and audit every sensitive field change, not just financial transactions.
- Batch-Only Reconciliation: Performing balance checks only in overnight batch processes means errors and fraud can compound in real time before detection. Fix: Implement continuous or near-real-time balance reconciliation with automated alerting on any imbalance.
- Circumventing Legacy Controls in New Systems: Global-scale systems designed to circumvent the checks and balances that had evolved over centuries in local and manual systems create new fraud vectors. Fix: Explicitly map and reimplement each legacy control when building replacement systems, rather than assuming the old constraints no longer apply.

## When To Apply

Load this page when:

- Use this when designing a financial transaction processing system that must detect theft or manipulation by internal users (developers, DBAs, ops staff).
- Use this when implementing a ledger or accounting module and deciding whether to use a single unified database table or separate, independently reconcilable data structures.
- Use this when building an audit logging system for a payment or banking application and deciding which fields and operations must be logged.
- Use this when adding a privileged administrative operation (e.g., address change, account merge, card issuance) and determining whether it needs a second-approver workflow.
- Use this when migrating a legacy banking or bookkeeping system to a new platform and needing to preserve internal controls that were implicit in the old architecture.
- Use this when generating or reviewing code that modifies account balances, and needing to verify that every debit has a corresponding credit and the system cannot create value from nothing.
- Use this when designing access controls for a core banking database, specifically to ensure that application-layer role checks cannot be bypassed by direct database access.
- Use this when assessing compliance requirements (Sarbanes-Oxley, PCI DSS, Gramm-Leach-Bliley) and translating them into concrete technical control requirements.

## Concrete Examples

- A cashier at a bank exploited the absence of auditing on address changes: he changed a customer's address, issued an extra bank card, then changed the address back — the loophole went undetected because address changes were not audited.
- The Leo computer (1951) was the first non-military/academic computer and was used to do bookkeeping for the Lyons chain of coffee houses, illustrating that bookkeeping drove the entire computer industry.
- Clay token bullae from ~3300 BC Uruk: each unit of stored food was represented by a clay token sealed inside a baked clay envelope, broken only by the keeper in the presence of a witness — described as possibly the oldest known security protocol.
- James Ritty's 1879 'Incorruptible Cashier' cash register with bell and paper tape was invented because saloon employees stole from him, leading to NCR and eventually IBM.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Banking and Bookkeeping**

An LLM coding agent is particularly prone to the 'UI-Only Separation of Duty' anti-pattern: when asked to implement role-based access for a ledger, it will naturally generate application-layer checks (if/else on user role) while leaving the underlying database tables fully writable by any connection string — exactly the failure mode described for systems where 'the separation-of-duty features may be just a skin in the user interface.' Agents also tend to implement balance updates as single-table mutations rather than double-entry pairs, making it possible to create or destroy value without a corresponding counter-entry and breaking the zero-sum invariant that triggers fraud detection. The trigger for invoking this chapter's knowledge is any agent task involving account balances, ledger writes, or privileged financial operations.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/security-engineering/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
