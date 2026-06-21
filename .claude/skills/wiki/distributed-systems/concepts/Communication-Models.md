---
title: Communication Models
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, distributed-systems, concept]
confidence: high
consolidated_from: 5 pages
---

# Communication Models

> Consolidated from 5 related concept pages.

---

## Message Oriented Middleware MOM A high level message queuing model supporting pe

## Core Principle

Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-server interaction) and Message-Oriented Middleware (enabling persistent, asynchronous, decoupled communication). Communication is classified along persistence (stored vs. transient) and synchrony (blocking vs. non-blocking) axes, and the right model depends on interaction pattern, availability requirements, and scale. For large-scale dissemination, epidemic and probabilistic flooding protocols offer robust, simple alternatives to deterministic tree-based multicasting.

## Key Heuristics

These are the load-bearing rules for this concept.

> Unless the primitive communication facilities of computer networks are replaced by something else, development of large-scale distributed applications is extremely difficult.

> The protocols that were developed as part of the OSI model were never widely used and are essentially dead. However, the underlying model itself has proved to be quite useful for understanding computer networks.

> An RPC aims at hiding most of the intricacies of message passing, and is ideal for client-server applications. However, realizing RPCs in a transparent manner is easier said than done.

> In many distributed applications, communication does not follow the rather strict pattern of client-server interaction. In those cases, it turns out that thinking in terms of messages is more appropriate.

> Message-oriented middleware models generally offer persistent asynchronous communication, and are used where RPCs are not appropriate.

> Probabilistic flooding by which a node forwards a message with a certain probability often proves to combine simplicity and efficiency, while being highly effective.

> Epidemic protocols have proven to be very simple and extremely robust. Apart from merely spreading messages, epidemic protocols can also be efficiently deployed for aggregating information across a large distributed system.

## Anti-Patterns & Fixes

- Raw Low-Level Message Passing at Application Layer: Directly using transport-layer primitives for distributed application communication leads to lack of distribution transparency and brittle, hard-to-maintain code. Fix: Use higher-level abstractions like RPC for request-response or MOM for decoupled messaging.
- Assuming Synchronous RPC for All Distributed Communication: Forcing synchronous RPC into non-client-server interaction patterns blocks senders unnecessarily and creates tight coupling. Fix: Use persistent asynchronous MOM when interaction patterns are irregular or receivers may be temporarily unavailable.
- Assuming Shared Memory Primitives in Distributed Contexts: Applying shared-memory concurrency patterns to distributed systems causes incorrect behavior since no shared memory exists across nodes. Fix: Redesign communication explicitly around message passing with defined protocols.
- Naive Flooding Without Probability Throttling: Forwarding every received message to all neighbors causes severe resource waste as nodes receive duplicates repeatedly. Fix: Use probabilistic flooding where each node forwards with a tuned probability to balance robustness and efficiency.
- Ignoring Death Certificates in Epidemic Deletion: Deleting an item without propagating a death certificate allows obsolete updates to resurrect deleted data when they arrive late. Fix: Maintain and re-spread death certificates so nodes can reject and suppress obsolete updates.

## When To Apply

Load this page when:

- Use this when designing an agent that calls external microservices and must choose between blocking RPC-style calls versus fire-and-forget async messaging.
- Use this when an agent needs to broadcast state updates or events to multiple downstream consumers and must decide between tree-based multicast, flooding, or gossip dissemination.
- Use this when an agent-to-agent communication pattern does not fit strict request-response (e.g., long-running tasks, offline receivers) and a queuing or MOM approach is needed.
- Use this when an agent must serialize and deserialize structured data across a network boundary and needs to correctly marshal parameters (stub pattern) to avoid type mismatches.
- Use this when designing retry and delivery guarantees for messages an agent sends, requiring a choice between persistent (store-and-forward) and transient communication models.
- Use this when an agent needs to aggregate distributed state (e.g., averaging metrics across nodes) and epidemic/gossip protocols offer a simpler and more robust alternative to centralized collection.
- Use this when an agent detects that a received update may be stale or conflicting and needs a protocol-level mechanism (e.g., death certificates) to suppress obsolete data propagation.

## Concrete Examples

- Telephone call as an analogy for connection-oriented communication service requiring explicit setup and teardown.
- Dropping a letter in a mailbox as an analogy for connectionless communication requiring no prior setup.
- Email systems as an analogy for high-level message-queuing (MOM) persistent asynchronous communication.
- Death certificates in epidemic protocols: node P holds a certificate for data item x and re-spreads it upon receiving an obsolete update, preventing resurrection of deleted data.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Communication**

An LLM coding agent is prone to defaulting to synchronous RPC-style HTTP calls for all inter-service communication, failing to recognize when persistent async messaging (MOM) is architecturally required—particularly when generated code assumes the remote endpoint is always available. Agents also frequently omit stub-layer concerns like parameter marshaling, idempotency, and partial failure handling, producing code that works in happy-path unit tests but fails under real network conditions. Applying this chapter's taxonomy (persistent/transient, sync/async, RPC vs. MOM) as an explicit decision gate before generating communication code prevents these silent architectural mismatches.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## OSI Reference Model A seven layer abstraction that decomposes network communicat

## Core Principle

Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-server interaction) and Message-Oriented Middleware (enabling persistent, asynchronous, decoupled communication). Communication is classified along persistence (stored vs. transient) and synchrony (blocking vs. non-blocking) axes, and the right model depends on interaction pattern, availability requirements, and scale. For large-scale dissemination, epidemic and probabilistic flooding protocols offer robust, simple alternatives to deterministic tree-based multicasting.

## Key Heuristics

These are the load-bearing rules for this concept.

> Unless the primitive communication facilities of computer networks are replaced by something else, development of large-scale distributed applications is extremely difficult.

> The protocols that were developed as part of the OSI model were never widely used and are essentially dead. However, the underlying model itself has proved to be quite useful for understanding computer networks.

> An RPC aims at hiding most of the intricacies of message passing, and is ideal for client-server applications. However, realizing RPCs in a transparent manner is easier said than done.

> In many distributed applications, communication does not follow the rather strict pattern of client-server interaction. In those cases, it turns out that thinking in terms of messages is more appropriate.

> Message-oriented middleware models generally offer persistent asynchronous communication, and are used where RPCs are not appropriate.

> Probabilistic flooding by which a node forwards a message with a certain probability often proves to combine simplicity and efficiency, while being highly effective.

> Epidemic protocols have proven to be very simple and extremely robust. Apart from merely spreading messages, epidemic protocols can also be efficiently deployed for aggregating information across a large distributed system.

## Anti-Patterns & Fixes

- Raw Low-Level Message Passing at Application Layer: Directly using transport-layer primitives for distributed application communication leads to lack of distribution transparency and brittle, hard-to-maintain code. Fix: Use higher-level abstractions like RPC for request-response or MOM for decoupled messaging.
- Assuming Synchronous RPC for All Distributed Communication: Forcing synchronous RPC into non-client-server interaction patterns blocks senders unnecessarily and creates tight coupling. Fix: Use persistent asynchronous MOM when interaction patterns are irregular or receivers may be temporarily unavailable.
- Assuming Shared Memory Primitives in Distributed Contexts: Applying shared-memory concurrency patterns to distributed systems causes incorrect behavior since no shared memory exists across nodes. Fix: Redesign communication explicitly around message passing with defined protocols.
- Naive Flooding Without Probability Throttling: Forwarding every received message to all neighbors causes severe resource waste as nodes receive duplicates repeatedly. Fix: Use probabilistic flooding where each node forwards with a tuned probability to balance robustness and efficiency.
- Ignoring Death Certificates in Epidemic Deletion: Deleting an item without propagating a death certificate allows obsolete updates to resurrect deleted data when they arrive late. Fix: Maintain and re-spread death certificates so nodes can reject and suppress obsolete updates.

## When To Apply

Load this page when:

- Use this when designing an agent that calls external microservices and must choose between blocking RPC-style calls versus fire-and-forget async messaging.
- Use this when an agent needs to broadcast state updates or events to multiple downstream consumers and must decide between tree-based multicast, flooding, or gossip dissemination.
- Use this when an agent-to-agent communication pattern does not fit strict request-response (e.g., long-running tasks, offline receivers) and a queuing or MOM approach is needed.
- Use this when an agent must serialize and deserialize structured data across a network boundary and needs to correctly marshal parameters (stub pattern) to avoid type mismatches.
- Use this when designing retry and delivery guarantees for messages an agent sends, requiring a choice between persistent (store-and-forward) and transient communication models.
- Use this when an agent needs to aggregate distributed state (e.g., averaging metrics across nodes) and epidemic/gossip protocols offer a simpler and more robust alternative to centralized collection.
- Use this when an agent detects that a received update may be stale or conflicting and needs a protocol-level mechanism (e.g., death certificates) to suppress obsolete data propagation.

## Concrete Examples

- Telephone call as an analogy for connection-oriented communication service requiring explicit setup and teardown.
- Dropping a letter in a mailbox as an analogy for connectionless communication requiring no prior setup.
- Email systems as an analogy for high-level message-queuing (MOM) persistent asynchronous communication.
- Death certificates in epidemic protocols: node P holds a certificate for data item x and re-spreads it upon receiving an obsolete update, preventing resurrection of deleted data.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Communication**

An LLM coding agent is prone to defaulting to synchronous RPC-style HTTP calls for all inter-service communication, failing to recognize when persistent async messaging (MOM) is architecturally required—particularly when generated code assumes the remote endpoint is always available. Agents also frequently omit stub-layer concerns like parameter marshaling, idempotency, and partial failure handling, producing code that works in happy-path unit tests but fails under real network conditions. Applying this chapter's taxonomy (persistent/transient, sync/async, RPC vs. MOM) as an explicit decision gate before generating communication code prevents these silent architectural mismatches.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Persistent vs Transient Communication Taxonomy A classification axis where persi

## Core Principle

Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-server interaction) and Message-Oriented Middleware (enabling persistent, asynchronous, decoupled communication). Communication is classified along persistence (stored vs. transient) and synchrony (blocking vs. non-blocking) axes, and the right model depends on interaction pattern, availability requirements, and scale. For large-scale dissemination, epidemic and probabilistic flooding protocols offer robust, simple alternatives to deterministic tree-based multicasting.

## Key Heuristics

These are the load-bearing rules for this concept.

> Unless the primitive communication facilities of computer networks are replaced by something else, development of large-scale distributed applications is extremely difficult.

> The protocols that were developed as part of the OSI model were never widely used and are essentially dead. However, the underlying model itself has proved to be quite useful for understanding computer networks.

> An RPC aims at hiding most of the intricacies of message passing, and is ideal for client-server applications. However, realizing RPCs in a transparent manner is easier said than done.

> In many distributed applications, communication does not follow the rather strict pattern of client-server interaction. In those cases, it turns out that thinking in terms of messages is more appropriate.

> Message-oriented middleware models generally offer persistent asynchronous communication, and are used where RPCs are not appropriate.

> Probabilistic flooding by which a node forwards a message with a certain probability often proves to combine simplicity and efficiency, while being highly effective.

> Epidemic protocols have proven to be very simple and extremely robust. Apart from merely spreading messages, epidemic protocols can also be efficiently deployed for aggregating information across a large distributed system.

## Anti-Patterns & Fixes

- Raw Low-Level Message Passing at Application Layer: Directly using transport-layer primitives for distributed application communication leads to lack of distribution transparency and brittle, hard-to-maintain code. Fix: Use higher-level abstractions like RPC for request-response or MOM for decoupled messaging.
- Assuming Synchronous RPC for All Distributed Communication: Forcing synchronous RPC into non-client-server interaction patterns blocks senders unnecessarily and creates tight coupling. Fix: Use persistent asynchronous MOM when interaction patterns are irregular or receivers may be temporarily unavailable.
- Assuming Shared Memory Primitives in Distributed Contexts: Applying shared-memory concurrency patterns to distributed systems causes incorrect behavior since no shared memory exists across nodes. Fix: Redesign communication explicitly around message passing with defined protocols.
- Naive Flooding Without Probability Throttling: Forwarding every received message to all neighbors causes severe resource waste as nodes receive duplicates repeatedly. Fix: Use probabilistic flooding where each node forwards with a tuned probability to balance robustness and efficiency.
- Ignoring Death Certificates in Epidemic Deletion: Deleting an item without propagating a death certificate allows obsolete updates to resurrect deleted data when they arrive late. Fix: Maintain and re-spread death certificates so nodes can reject and suppress obsolete updates.

## When To Apply

Load this page when:

- Use this when designing an agent that calls external microservices and must choose between blocking RPC-style calls versus fire-and-forget async messaging.
- Use this when an agent needs to broadcast state updates or events to multiple downstream consumers and must decide between tree-based multicast, flooding, or gossip dissemination.
- Use this when an agent-to-agent communication pattern does not fit strict request-response (e.g., long-running tasks, offline receivers) and a queuing or MOM approach is needed.
- Use this when an agent must serialize and deserialize structured data across a network boundary and needs to correctly marshal parameters (stub pattern) to avoid type mismatches.
- Use this when designing retry and delivery guarantees for messages an agent sends, requiring a choice between persistent (store-and-forward) and transient communication models.
- Use this when an agent needs to aggregate distributed state (e.g., averaging metrics across nodes) and epidemic/gossip protocols offer a simpler and more robust alternative to centralized collection.
- Use this when an agent detects that a received update may be stale or conflicting and needs a protocol-level mechanism (e.g., death certificates) to suppress obsolete data propagation.

## Concrete Examples

- Telephone call as an analogy for connection-oriented communication service requiring explicit setup and teardown.
- Dropping a letter in a mailbox as an analogy for connectionless communication requiring no prior setup.
- Email systems as an analogy for high-level message-queuing (MOM) persistent asynchronous communication.
- Death certificates in epidemic protocols: node P holds a certificate for data item x and re-spreads it upon receiving an obsolete update, preventing resurrection of deleted data.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Communication**

An LLM coding agent is prone to defaulting to synchronous RPC-style HTTP calls for all inter-service communication, failing to recognize when persistent async messaging (MOM) is architecturally required—particularly when generated code assumes the remote endpoint is always available. Agents also frequently omit stub-layer concerns like parameter marshaling, idempotency, and partial failure handling, producing code that works in happy-path unit tests but fails under real network conditions. Applying this chapter's taxonomy (persistent/transient, sync/async, RPC vs. MOM) as an explicit decision gate before generating communication code prevents these silent architectural mismatches.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Remote Procedure Call RPC A communication abstraction that hides message passing

## Core Principle

Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-server interaction) and Message-Oriented Middleware (enabling persistent, asynchronous, decoupled communication). Communication is classified along persistence (stored vs. transient) and synchrony (blocking vs. non-blocking) axes, and the right model depends on interaction pattern, availability requirements, and scale. For large-scale dissemination, epidemic and probabilistic flooding protocols offer robust, simple alternatives to deterministic tree-based multicasting.

## Key Heuristics

These are the load-bearing rules for this concept.

> Unless the primitive communication facilities of computer networks are replaced by something else, development of large-scale distributed applications is extremely difficult.

> The protocols that were developed as part of the OSI model were never widely used and are essentially dead. However, the underlying model itself has proved to be quite useful for understanding computer networks.

> An RPC aims at hiding most of the intricacies of message passing, and is ideal for client-server applications. However, realizing RPCs in a transparent manner is easier said than done.

> In many distributed applications, communication does not follow the rather strict pattern of client-server interaction. In those cases, it turns out that thinking in terms of messages is more appropriate.

> Message-oriented middleware models generally offer persistent asynchronous communication, and are used where RPCs are not appropriate.

> Probabilistic flooding by which a node forwards a message with a certain probability often proves to combine simplicity and efficiency, while being highly effective.

> Epidemic protocols have proven to be very simple and extremely robust. Apart from merely spreading messages, epidemic protocols can also be efficiently deployed for aggregating information across a large distributed system.

## Anti-Patterns & Fixes

- Raw Low-Level Message Passing at Application Layer: Directly using transport-layer primitives for distributed application communication leads to lack of distribution transparency and brittle, hard-to-maintain code. Fix: Use higher-level abstractions like RPC for request-response or MOM for decoupled messaging.
- Assuming Synchronous RPC for All Distributed Communication: Forcing synchronous RPC into non-client-server interaction patterns blocks senders unnecessarily and creates tight coupling. Fix: Use persistent asynchronous MOM when interaction patterns are irregular or receivers may be temporarily unavailable.
- Assuming Shared Memory Primitives in Distributed Contexts: Applying shared-memory concurrency patterns to distributed systems causes incorrect behavior since no shared memory exists across nodes. Fix: Redesign communication explicitly around message passing with defined protocols.
- Naive Flooding Without Probability Throttling: Forwarding every received message to all neighbors causes severe resource waste as nodes receive duplicates repeatedly. Fix: Use probabilistic flooding where each node forwards with a tuned probability to balance robustness and efficiency.
- Ignoring Death Certificates in Epidemic Deletion: Deleting an item without propagating a death certificate allows obsolete updates to resurrect deleted data when they arrive late. Fix: Maintain and re-spread death certificates so nodes can reject and suppress obsolete updates.

## When To Apply

Load this page when:

- Use this when designing an agent that calls external microservices and must choose between blocking RPC-style calls versus fire-and-forget async messaging.
- Use this when an agent needs to broadcast state updates or events to multiple downstream consumers and must decide between tree-based multicast, flooding, or gossip dissemination.
- Use this when an agent-to-agent communication pattern does not fit strict request-response (e.g., long-running tasks, offline receivers) and a queuing or MOM approach is needed.
- Use this when an agent must serialize and deserialize structured data across a network boundary and needs to correctly marshal parameters (stub pattern) to avoid type mismatches.
- Use this when designing retry and delivery guarantees for messages an agent sends, requiring a choice between persistent (store-and-forward) and transient communication models.
- Use this when an agent needs to aggregate distributed state (e.g., averaging metrics across nodes) and epidemic/gossip protocols offer a simpler and more robust alternative to centralized collection.
- Use this when an agent detects that a received update may be stale or conflicting and needs a protocol-level mechanism (e.g., death certificates) to suppress obsolete data propagation.

## Concrete Examples

- Telephone call as an analogy for connection-oriented communication service requiring explicit setup and teardown.
- Dropping a letter in a mailbox as an analogy for connectionless communication requiring no prior setup.
- Email systems as an analogy for high-level message-queuing (MOM) persistent asynchronous communication.
- Death certificates in epidemic protocols: node P holds a certificate for data item x and re-spreads it upon receiving an obsolete update, preventing resurrection of deleted data.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Communication**

An LLM coding agent is prone to defaulting to synchronous RPC-style HTTP calls for all inter-service communication, failing to recognize when persistent async messaging (MOM) is architecturally required—particularly when generated code assumes the remote endpoint is always available. Agents also frequently omit stub-layer concerns like parameter marshaling, idempotency, and partial failure handling, producing code that works in happy-path unit tests but fails under real network conditions. Applying this chapter's taxonomy (persistent/transient, sync/async, RPC vs. MOM) as an explicit decision gate before generating communication code prevents these silent architectural mismatches.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Synchronous vs Asynchronous Communication Taxonomy A classification axis disting

## Core Principle

Distributed system communication must be built on layered protocol abstractions rather than raw message passing; the two dominant models are RPC (hiding message complexity for synchronous client-server interaction) and Message-Oriented Middleware (enabling persistent, asynchronous, decoupled communication). Communication is classified along persistence (stored vs. transient) and synchrony (blocking vs. non-blocking) axes, and the right model depends on interaction pattern, availability requirements, and scale. For large-scale dissemination, epidemic and probabilistic flooding protocols offer robust, simple alternatives to deterministic tree-based multicasting.

## Key Heuristics

These are the load-bearing rules for this concept.

> Unless the primitive communication facilities of computer networks are replaced by something else, development of large-scale distributed applications is extremely difficult.

> The protocols that were developed as part of the OSI model were never widely used and are essentially dead. However, the underlying model itself has proved to be quite useful for understanding computer networks.

> An RPC aims at hiding most of the intricacies of message passing, and is ideal for client-server applications. However, realizing RPCs in a transparent manner is easier said than done.

> In many distributed applications, communication does not follow the rather strict pattern of client-server interaction. In those cases, it turns out that thinking in terms of messages is more appropriate.

> Message-oriented middleware models generally offer persistent asynchronous communication, and are used where RPCs are not appropriate.

> Probabilistic flooding by which a node forwards a message with a certain probability often proves to combine simplicity and efficiency, while being highly effective.

> Epidemic protocols have proven to be very simple and extremely robust. Apart from merely spreading messages, epidemic protocols can also be efficiently deployed for aggregating information across a large distributed system.

## Anti-Patterns & Fixes

- Raw Low-Level Message Passing at Application Layer: Directly using transport-layer primitives for distributed application communication leads to lack of distribution transparency and brittle, hard-to-maintain code. Fix: Use higher-level abstractions like RPC for request-response or MOM for decoupled messaging.
- Assuming Synchronous RPC for All Distributed Communication: Forcing synchronous RPC into non-client-server interaction patterns blocks senders unnecessarily and creates tight coupling. Fix: Use persistent asynchronous MOM when interaction patterns are irregular or receivers may be temporarily unavailable.
- Assuming Shared Memory Primitives in Distributed Contexts: Applying shared-memory concurrency patterns to distributed systems causes incorrect behavior since no shared memory exists across nodes. Fix: Redesign communication explicitly around message passing with defined protocols.
- Naive Flooding Without Probability Throttling: Forwarding every received message to all neighbors causes severe resource waste as nodes receive duplicates repeatedly. Fix: Use probabilistic flooding where each node forwards with a tuned probability to balance robustness and efficiency.
- Ignoring Death Certificates in Epidemic Deletion: Deleting an item without propagating a death certificate allows obsolete updates to resurrect deleted data when they arrive late. Fix: Maintain and re-spread death certificates so nodes can reject and suppress obsolete updates.

## When To Apply

Load this page when:

- Use this when designing an agent that calls external microservices and must choose between blocking RPC-style calls versus fire-and-forget async messaging.
- Use this when an agent needs to broadcast state updates or events to multiple downstream consumers and must decide between tree-based multicast, flooding, or gossip dissemination.
- Use this when an agent-to-agent communication pattern does not fit strict request-response (e.g., long-running tasks, offline receivers) and a queuing or MOM approach is needed.
- Use this when an agent must serialize and deserialize structured data across a network boundary and needs to correctly marshal parameters (stub pattern) to avoid type mismatches.
- Use this when designing retry and delivery guarantees for messages an agent sends, requiring a choice between persistent (store-and-forward) and transient communication models.
- Use this when an agent needs to aggregate distributed state (e.g., averaging metrics across nodes) and epidemic/gossip protocols offer a simpler and more robust alternative to centralized collection.
- Use this when an agent detects that a received update may be stale or conflicting and needs a protocol-level mechanism (e.g., death certificates) to suppress obsolete data propagation.

## Concrete Examples

- Telephone call as an analogy for connection-oriented communication service requiring explicit setup and teardown.
- Dropping a letter in a mailbox as an analogy for connectionless communication requiring no prior setup.
- Email systems as an analogy for high-level message-queuing (MOM) persistent asynchronous communication.
- Death certificates in epidemic protocols: node P holds a certificate for data item x and re-spreads it upon receiving an obsolete update, preventing resurrection of deleted data.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Communication**

An LLM coding agent is prone to defaulting to synchronous RPC-style HTTP calls for all inter-service communication, failing to recognize when persistent async messaging (MOM) is architecturally required—particularly when generated code assumes the remote endpoint is always available. Agents also frequently omit stub-layer concerns like parameter marshaling, idempotency, and partial failure handling, producing code that works in happy-path unit tests but fails under real network conditions. Applying this chapter's taxonomy (persistent/transient, sync/async, RPC vs. MOM) as an explicit decision gate before generating communication code prevents these silent architectural mismatches.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/distributed-systems/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
