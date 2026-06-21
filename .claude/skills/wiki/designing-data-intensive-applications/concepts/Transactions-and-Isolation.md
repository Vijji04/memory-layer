# Transactions-and-Isolation

## ACID: Atomicity, Consistency, Isolation, Durability — the four safety guarantees that transactions provide, each with distinct meanings and responsibilities (A/I/D are database properties; C is an application property)

---
title: ACID: Atomicity, Consistency, Isolation, Durability — the four safety guarantees that transactions provide, each with distinct meanings and responsibilities (A/I/D are database properties; C is an application property)
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-7-Transactions.json]
contributing_chapters: ["Chapter 7: Transactions"]
confidence: high
---


> From chapter: *Chapter 7: Transactions*

## Core Principle

Transactions group multiple reads and writes into an atomic unit that either fully commits or fully aborts, protecting applications from partial failures and concurrency anomalies. The ACID properties (Atomicity, Consistency, Isolation, Durability) define these guarantees, but implementations vary significantly — especially isolation — spanning a spectrum from read committed through snapshot isolation to full serializability, each with different trade-offs between correctness and performance. The chapter argues that transactions are not inherently incompatible with scale; the decision to weaken or abandon them should be driven by measured bottlenecks, not assumption.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.

> The ability to abort a transaction on error, and have all writes from that transaction discarded, is the defining feature of ACID atomicity. Perhaps abortability would have been a better term than atomicity.

> Atomicity, isolation and durability are properties of the database, whereas consistency (in the ACID sense) is a property of the application.

> ACID has unfortunately become mostly a marketing term.

> The truth is not that simple: like every other technical design choice, transactions have advantages and limitations.

> Transactions are not a law of nature; they were created with a purpose, namely in order to simplify the programming model for applications accessing a database.

> Both viewpoints [transactions as antithesis of scalability vs. transactions as essential for serious applications] are pure hyperbole.

## Anti-Patterns & Fixes

- Assuming ACID compliance is uniform: Claiming a system is 'ACID compliant' does not guarantee specific behaviors, especially around isolation, since implementations vary widely. Fix: Explicitly test and document the actual isolation level and behavior of the specific database in use.
- Abandoning transactions for scalability: NoSQL movement led many to drop transactions assuming they are incompatible with scale, leaving applications to handle partial failures manually. Fix: Evaluate actual performance bottlenecks before removing transactional guarantees; use weaker isolation levels rather than no transactions.
- Conflating the multiple meanings of 'consistency': The word consistency means replica consistency, linearizability (CAP), and application invariants (ACID) in different contexts, causing misunderstandings. Fix: Always qualify which type of consistency is meant in design discussions.
- Retrying aborted transactions blindly: Retrying without idempotency checks risks applying the same change twice, leading to duplicate or incorrect data. Fix: Ensure operations are idempotent or track which transactions have been committed before retrying.
- Using read committed isolation and assuming safety from all anomalies: Read committed prevents dirty reads/writes but still allows non-repeatable reads, read skew, and write skew. Fix: Use snapshot isolation or serializable isolation when application correctness requires consistent reads across multiple objects.
- Ignoring phantom reads in application logic: Inserting new rows that match a previously executed query predicate can violate invariants even under snapshot isolation. Fix: Use serializable isolation (SSI or 2PL with predicate locks) when correctness depends on the absence of matching rows.

## When To Apply

Load this page when:

- Use this when generating code that performs multi-step database writes that must all succeed or all fail (e.g., transferring funds between accounts, creating related records across tables).
- Use this when designing a system where multiple concurrent clients may read-modify-write the same records (e.g., incrementing counters, booking seats, updating inventory).
- Use this when choosing a database isolation level for an application and needing to understand which race conditions (dirty read, non-repeatable read, phantom read, write skew) each level prevents.
- Use this when an application must enforce invariants that span multiple rows or tables (e.g., ensuring account balances remain non-negative across a transfer).
- Use this when evaluating whether to use a NoSQL database without native transactions and needing to understand what correctness guarantees must be re-implemented at the application layer.
- Use this when debugging data anomalies that appear intermittently under concurrent load, such as lost updates or duplicate records.
- Use this when implementing retry logic for failed database operations to ensure retries do not cause duplicate side effects.
- Use this when a system requires long-running transactions or batch operations that must see a consistent snapshot of the database throughout their execution.

## Concrete Examples

- Two clients simultaneously incrementing a counter: each reads 42, both write 43, resulting in a lost update where the counter should be 44 but ends up at 43.
- An accounting system where credits and debits across all accounts must always be balanced — used as the canonical example of an application-defined consistency invariant.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Transactions**

An LLM coding agent is prone to generating multi-step database operations as sequential individual queries without wrapping them in transactions, silently creating partial-failure vulnerabilities that only manifest under concurrent load or crash scenarios. Agents are also likely to select default or low isolation levels without flagging write-skew or phantom-read risks, since these anomalies require understanding the full application invariant context — not just the local code block being generated. Applying this chapter's frameworks, an agent should always classify whether generated database operations require atomicity, identify the relevant race conditions for the access pattern, and explicitly select or recommend the appropriate isolation level.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Isolation Levels Hierarchy: A spectrum from weakest (read uncommitted) to strongest (serializable) isolation, each preventing different classes of race conditions at different performance costs

---
title: Isolation Levels Hierarchy: A spectrum from weakest (read uncommitted) to strongest (serializable) isolation, each preventing different classes of race conditions at different performance costs
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-7-Transactions.json]
contributing_chapters: ["Chapter 7: Transactions"]
confidence: high
---


> From chapter: *Chapter 7: Transactions*

## Core Principle

Transactions group multiple reads and writes into an atomic unit that either fully commits or fully aborts, protecting applications from partial failures and concurrency anomalies. The ACID properties (Atomicity, Consistency, Isolation, Durability) define these guarantees, but implementations vary significantly — especially isolation — spanning a spectrum from read committed through snapshot isolation to full serializability, each with different trade-offs between correctness and performance. The chapter argues that transactions are not inherently incompatible with scale; the decision to weaken or abandon them should be driven by measured bottlenecks, not assumption.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.

> The ability to abort a transaction on error, and have all writes from that transaction discarded, is the defining feature of ACID atomicity. Perhaps abortability would have been a better term than atomicity.

> Atomicity, isolation and durability are properties of the database, whereas consistency (in the ACID sense) is a property of the application.

> ACID has unfortunately become mostly a marketing term.

> The truth is not that simple: like every other technical design choice, transactions have advantages and limitations.

> Transactions are not a law of nature; they were created with a purpose, namely in order to simplify the programming model for applications accessing a database.

> Both viewpoints [transactions as antithesis of scalability vs. transactions as essential for serious applications] are pure hyperbole.

## Anti-Patterns & Fixes

- Assuming ACID compliance is uniform: Claiming a system is 'ACID compliant' does not guarantee specific behaviors, especially around isolation, since implementations vary widely. Fix: Explicitly test and document the actual isolation level and behavior of the specific database in use.
- Abandoning transactions for scalability: NoSQL movement led many to drop transactions assuming they are incompatible with scale, leaving applications to handle partial failures manually. Fix: Evaluate actual performance bottlenecks before removing transactional guarantees; use weaker isolation levels rather than no transactions.
- Conflating the multiple meanings of 'consistency': The word consistency means replica consistency, linearizability (CAP), and application invariants (ACID) in different contexts, causing misunderstandings. Fix: Always qualify which type of consistency is meant in design discussions.
- Retrying aborted transactions blindly: Retrying without idempotency checks risks applying the same change twice, leading to duplicate or incorrect data. Fix: Ensure operations are idempotent or track which transactions have been committed before retrying.
- Using read committed isolation and assuming safety from all anomalies: Read committed prevents dirty reads/writes but still allows non-repeatable reads, read skew, and write skew. Fix: Use snapshot isolation or serializable isolation when application correctness requires consistent reads across multiple objects.
- Ignoring phantom reads in application logic: Inserting new rows that match a previously executed query predicate can violate invariants even under snapshot isolation. Fix: Use serializable isolation (SSI or 2PL with predicate locks) when correctness depends on the absence of matching rows.

## When To Apply

Load this page when:

- Use this when generating code that performs multi-step database writes that must all succeed or all fail (e.g., transferring funds between accounts, creating related records across tables).
- Use this when designing a system where multiple concurrent clients may read-modify-write the same records (e.g., incrementing counters, booking seats, updating inventory).
- Use this when choosing a database isolation level for an application and needing to understand which race conditions (dirty read, non-repeatable read, phantom read, write skew) each level prevents.
- Use this when an application must enforce invariants that span multiple rows or tables (e.g., ensuring account balances remain non-negative across a transfer).
- Use this when evaluating whether to use a NoSQL database without native transactions and needing to understand what correctness guarantees must be re-implemented at the application layer.
- Use this when debugging data anomalies that appear intermittently under concurrent load, such as lost updates or duplicate records.
- Use this when implementing retry logic for failed database operations to ensure retries do not cause duplicate side effects.
- Use this when a system requires long-running transactions or batch operations that must see a consistent snapshot of the database throughout their execution.

## Concrete Examples

- Two clients simultaneously incrementing a counter: each reads 42, both write 43, resulting in a lost update where the counter should be 44 but ends up at 43.
- An accounting system where credits and debits across all accounts must always be balanced — used as the canonical example of an application-defined consistency invariant.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Transactions**

An LLM coding agent is prone to generating multi-step database operations as sequential individual queries without wrapping them in transactions, silently creating partial-failure vulnerabilities that only manifest under concurrent load or crash scenarios. Agents are also likely to select default or low isolation levels without flagging write-skew or phantom-read risks, since these anomalies require understanding the full application invariant context — not just the local code block being generated. Applying this chapter's frameworks, an agent should always classify whether generated database operations require atomicity, identify the relevant race conditions for the access pattern, and explicitly select or recommend the appropriate isolation level.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Serializable Snapshot Isolation (SSI): An optimistic concurrency control algorithm that detects write skew and phantom anomalies at commit time, providing full serializability with lower overhead than 2PL

---
title: Serializable Snapshot Isolation (SSI): An optimistic concurrency control algorithm that detects write skew and phantom anomalies at commit time, providing full serializability with lower overhead than 2PL
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-7-Transactions.json]
contributing_chapters: ["Chapter 7: Transactions"]
confidence: high
---


> From chapter: *Chapter 7: Transactions*

## Core Principle

Transactions group multiple reads and writes into an atomic unit that either fully commits or fully aborts, protecting applications from partial failures and concurrency anomalies. The ACID properties (Atomicity, Consistency, Isolation, Durability) define these guarantees, but implementations vary significantly — especially isolation — spanning a spectrum from read committed through snapshot isolation to full serializability, each with different trade-offs between correctness and performance. The chapter argues that transactions are not inherently incompatible with scale; the decision to weaken or abandon them should be driven by measured bottlenecks, not assumption.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.

> The ability to abort a transaction on error, and have all writes from that transaction discarded, is the defining feature of ACID atomicity. Perhaps abortability would have been a better term than atomicity.

> Atomicity, isolation and durability are properties of the database, whereas consistency (in the ACID sense) is a property of the application.

> ACID has unfortunately become mostly a marketing term.

> The truth is not that simple: like every other technical design choice, transactions have advantages and limitations.

> Transactions are not a law of nature; they were created with a purpose, namely in order to simplify the programming model for applications accessing a database.

> Both viewpoints [transactions as antithesis of scalability vs. transactions as essential for serious applications] are pure hyperbole.

## Anti-Patterns & Fixes

- Assuming ACID compliance is uniform: Claiming a system is 'ACID compliant' does not guarantee specific behaviors, especially around isolation, since implementations vary widely. Fix: Explicitly test and document the actual isolation level and behavior of the specific database in use.
- Abandoning transactions for scalability: NoSQL movement led many to drop transactions assuming they are incompatible with scale, leaving applications to handle partial failures manually. Fix: Evaluate actual performance bottlenecks before removing transactional guarantees; use weaker isolation levels rather than no transactions.
- Conflating the multiple meanings of 'consistency': The word consistency means replica consistency, linearizability (CAP), and application invariants (ACID) in different contexts, causing misunderstandings. Fix: Always qualify which type of consistency is meant in design discussions.
- Retrying aborted transactions blindly: Retrying without idempotency checks risks applying the same change twice, leading to duplicate or incorrect data. Fix: Ensure operations are idempotent or track which transactions have been committed before retrying.
- Using read committed isolation and assuming safety from all anomalies: Read committed prevents dirty reads/writes but still allows non-repeatable reads, read skew, and write skew. Fix: Use snapshot isolation or serializable isolation when application correctness requires consistent reads across multiple objects.
- Ignoring phantom reads in application logic: Inserting new rows that match a previously executed query predicate can violate invariants even under snapshot isolation. Fix: Use serializable isolation (SSI or 2PL with predicate locks) when correctness depends on the absence of matching rows.

## When To Apply

Load this page when:

- Use this when generating code that performs multi-step database writes that must all succeed or all fail (e.g., transferring funds between accounts, creating related records across tables).
- Use this when designing a system where multiple concurrent clients may read-modify-write the same records (e.g., incrementing counters, booking seats, updating inventory).
- Use this when choosing a database isolation level for an application and needing to understand which race conditions (dirty read, non-repeatable read, phantom read, write skew) each level prevents.
- Use this when an application must enforce invariants that span multiple rows or tables (e.g., ensuring account balances remain non-negative across a transfer).
- Use this when evaluating whether to use a NoSQL database without native transactions and needing to understand what correctness guarantees must be re-implemented at the application layer.
- Use this when debugging data anomalies that appear intermittently under concurrent load, such as lost updates or duplicate records.
- Use this when implementing retry logic for failed database operations to ensure retries do not cause duplicate side effects.
- Use this when a system requires long-running transactions or batch operations that must see a consistent snapshot of the database throughout their execution.

## Concrete Examples

- Two clients simultaneously incrementing a counter: each reads 42, both write 43, resulting in a lost update where the counter should be 44 but ends up at 43.
- An accounting system where credits and debits across all accounts must always be balanced — used as the canonical example of an application-defined consistency invariant.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Transactions**

An LLM coding agent is prone to generating multi-step database operations as sequential individual queries without wrapping them in transactions, silently creating partial-failure vulnerabilities that only manifest under concurrent load or crash scenarios. Agents are also likely to select default or low isolation levels without flagging write-skew or phantom-read risks, since these anomalies require understanding the full application invariant context — not just the local code block being generated. Applying this chapter's frameworks, an agent should always classify whether generated database operations require atomicity, identify the relevant race conditions for the access pattern, and explicitly select or recommend the appropriate isolation level.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Snapshot Isolation / MVCC: Each transaction reads from a consistent snapshot of the database at transaction start, using multi-version concurrency control to allow readers and writers to not block each other

---
title: Snapshot Isolation / MVCC: Each transaction reads from a consistent snapshot of the database at transaction start, using multi-version concurrency control to allow readers and writers to not block each other
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-7-Transactions.json]
contributing_chapters: ["Chapter 7: Transactions"]
confidence: high
---


> From chapter: *Chapter 7: Transactions*

## Core Principle

Transactions group multiple reads and writes into an atomic unit that either fully commits or fully aborts, protecting applications from partial failures and concurrency anomalies. The ACID properties (Atomicity, Consistency, Isolation, Durability) define these guarantees, but implementations vary significantly — especially isolation — spanning a spectrum from read committed through snapshot isolation to full serializability, each with different trade-offs between correctness and performance. The chapter argues that transactions are not inherently incompatible with scale; the decision to weaken or abandon them should be driven by measured bottlenecks, not assumption.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.

> The ability to abort a transaction on error, and have all writes from that transaction discarded, is the defining feature of ACID atomicity. Perhaps abortability would have been a better term than atomicity.

> Atomicity, isolation and durability are properties of the database, whereas consistency (in the ACID sense) is a property of the application.

> ACID has unfortunately become mostly a marketing term.

> The truth is not that simple: like every other technical design choice, transactions have advantages and limitations.

> Transactions are not a law of nature; they were created with a purpose, namely in order to simplify the programming model for applications accessing a database.

> Both viewpoints [transactions as antithesis of scalability vs. transactions as essential for serious applications] are pure hyperbole.

## Anti-Patterns & Fixes

- Assuming ACID compliance is uniform: Claiming a system is 'ACID compliant' does not guarantee specific behaviors, especially around isolation, since implementations vary widely. Fix: Explicitly test and document the actual isolation level and behavior of the specific database in use.
- Abandoning transactions for scalability: NoSQL movement led many to drop transactions assuming they are incompatible with scale, leaving applications to handle partial failures manually. Fix: Evaluate actual performance bottlenecks before removing transactional guarantees; use weaker isolation levels rather than no transactions.
- Conflating the multiple meanings of 'consistency': The word consistency means replica consistency, linearizability (CAP), and application invariants (ACID) in different contexts, causing misunderstandings. Fix: Always qualify which type of consistency is meant in design discussions.
- Retrying aborted transactions blindly: Retrying without idempotency checks risks applying the same change twice, leading to duplicate or incorrect data. Fix: Ensure operations are idempotent or track which transactions have been committed before retrying.
- Using read committed isolation and assuming safety from all anomalies: Read committed prevents dirty reads/writes but still allows non-repeatable reads, read skew, and write skew. Fix: Use snapshot isolation or serializable isolation when application correctness requires consistent reads across multiple objects.
- Ignoring phantom reads in application logic: Inserting new rows that match a previously executed query predicate can violate invariants even under snapshot isolation. Fix: Use serializable isolation (SSI or 2PL with predicate locks) when correctness depends on the absence of matching rows.

## When To Apply

Load this page when:

- Use this when generating code that performs multi-step database writes that must all succeed or all fail (e.g., transferring funds between accounts, creating related records across tables).
- Use this when designing a system where multiple concurrent clients may read-modify-write the same records (e.g., incrementing counters, booking seats, updating inventory).
- Use this when choosing a database isolation level for an application and needing to understand which race conditions (dirty read, non-repeatable read, phantom read, write skew) each level prevents.
- Use this when an application must enforce invariants that span multiple rows or tables (e.g., ensuring account balances remain non-negative across a transfer).
- Use this when evaluating whether to use a NoSQL database without native transactions and needing to understand what correctness guarantees must be re-implemented at the application layer.
- Use this when debugging data anomalies that appear intermittently under concurrent load, such as lost updates or duplicate records.
- Use this when implementing retry logic for failed database operations to ensure retries do not cause duplicate side effects.
- Use this when a system requires long-running transactions or batch operations that must see a consistent snapshot of the database throughout their execution.

## Concrete Examples

- Two clients simultaneously incrementing a counter: each reads 42, both write 43, resulting in a lost update where the counter should be 44 but ends up at 43.
- An accounting system where credits and debits across all accounts must always be balanced — used as the canonical example of an application-defined consistency invariant.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Transactions**

An LLM coding agent is prone to generating multi-step database operations as sequential individual queries without wrapping them in transactions, silently creating partial-failure vulnerabilities that only manifest under concurrent load or crash scenarios. Agents are also likely to select default or low isolation levels without flagging write-skew or phantom-read risks, since these anomalies require understanding the full application invariant context — not just the local code block being generated. Applying this chapter's frameworks, an agent should always classify whether generated database operations require atomicity, identify the relevant race conditions for the access pattern, and explicitly select or recommend the appropriate isolation level.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Two-Phase Locking (2PL): A pessimistic concurrency control mechanism where readers block writers and writers block readers, providing serializable isolation by preventing all race conditions via lock acquisition and release phases

---
title: Two-Phase Locking (2PL): A pessimistic concurrency control mechanism where readers block writers and writers block readers, providing serializable isolation by preventing all race conditions via lock acquisition and release phases
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-1, designing-data-intensive-applications, concept]
sources: [extracts/designing-data-intensive-applications/Chapter-7-Transactions.json]
contributing_chapters: ["Chapter 7: Transactions"]
confidence: high
---


> From chapter: *Chapter 7: Transactions*

## Core Principle

Transactions group multiple reads and writes into an atomic unit that either fully commits or fully aborts, protecting applications from partial failures and concurrency anomalies. The ACID properties (Atomicity, Consistency, Isolation, Durability) define these guarantees, but implementations vary significantly — especially isolation — spanning a spectrum from read committed through snapshot isolation to full serializability, each with different trade-offs between correctness and performance. The chapter argues that transactions are not inherently incompatible with scale; the decision to weaken or abandon them should be driven by measured bottlenecks, not assumption.

## Key Heuristics

These are the load-bearing rules for this concept.

> It is better to have application programmers deal with performance problems due to overuse of transactions as bottlenecks arise, rather than always coding around the lack of transactions.

> The ability to abort a transaction on error, and have all writes from that transaction discarded, is the defining feature of ACID atomicity. Perhaps abortability would have been a better term than atomicity.

> Atomicity, isolation and durability are properties of the database, whereas consistency (in the ACID sense) is a property of the application.

> ACID has unfortunately become mostly a marketing term.

> The truth is not that simple: like every other technical design choice, transactions have advantages and limitations.

> Transactions are not a law of nature; they were created with a purpose, namely in order to simplify the programming model for applications accessing a database.

> Both viewpoints [transactions as antithesis of scalability vs. transactions as essential for serious applications] are pure hyperbole.

## Anti-Patterns & Fixes

- Assuming ACID compliance is uniform: Claiming a system is 'ACID compliant' does not guarantee specific behaviors, especially around isolation, since implementations vary widely. Fix: Explicitly test and document the actual isolation level and behavior of the specific database in use.
- Abandoning transactions for scalability: NoSQL movement led many to drop transactions assuming they are incompatible with scale, leaving applications to handle partial failures manually. Fix: Evaluate actual performance bottlenecks before removing transactional guarantees; use weaker isolation levels rather than no transactions.
- Conflating the multiple meanings of 'consistency': The word consistency means replica consistency, linearizability (CAP), and application invariants (ACID) in different contexts, causing misunderstandings. Fix: Always qualify which type of consistency is meant in design discussions.
- Retrying aborted transactions blindly: Retrying without idempotency checks risks applying the same change twice, leading to duplicate or incorrect data. Fix: Ensure operations are idempotent or track which transactions have been committed before retrying.
- Using read committed isolation and assuming safety from all anomalies: Read committed prevents dirty reads/writes but still allows non-repeatable reads, read skew, and write skew. Fix: Use snapshot isolation or serializable isolation when application correctness requires consistent reads across multiple objects.
- Ignoring phantom reads in application logic: Inserting new rows that match a previously executed query predicate can violate invariants even under snapshot isolation. Fix: Use serializable isolation (SSI or 2PL with predicate locks) when correctness depends on the absence of matching rows.

## When To Apply

Load this page when:

- Use this when generating code that performs multi-step database writes that must all succeed or all fail (e.g., transferring funds between accounts, creating related records across tables).
- Use this when designing a system where multiple concurrent clients may read-modify-write the same records (e.g., incrementing counters, booking seats, updating inventory).
- Use this when choosing a database isolation level for an application and needing to understand which race conditions (dirty read, non-repeatable read, phantom read, write skew) each level prevents.
- Use this when an application must enforce invariants that span multiple rows or tables (e.g., ensuring account balances remain non-negative across a transfer).
- Use this when evaluating whether to use a NoSQL database without native transactions and needing to understand what correctness guarantees must be re-implemented at the application layer.
- Use this when debugging data anomalies that appear intermittently under concurrent load, such as lost updates or duplicate records.
- Use this when implementing retry logic for failed database operations to ensure retries do not cause duplicate side effects.
- Use this when a system requires long-running transactions or batch operations that must see a consistent snapshot of the database throughout their execution.

## Concrete Examples

- Two clients simultaneously incrementing a counter: each reads 42, both write 43, resulting in a lost update where the counter should be 44 but ends up at 43.
- An accounting system where credits and debits across all accounts must always be balanced — used as the canonical example of an application-defined consistency invariant.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Chapter 7: Transactions**

An LLM coding agent is prone to generating multi-step database operations as sequential individual queries without wrapping them in transactions, silently creating partial-failure vulnerabilities that only manifest under concurrent load or crash scenarios. Agents are also likely to select default or low isolation levels without flagging write-skew or phantom-read risks, since these anomalies require understanding the full application invariant context — not just the local code block being generated. Applying this chapter's frameworks, an agent should always classify whether generated database operations require atomicity, identify the relevant race conditions for the access pattern, and explicitly select or recommend the appropriate isolation level.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/designing-data-intensive-applications/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->