---
title: Requirements
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 7 pages
---

# Requirements

> Consolidated from 7 related concept pages.

---

## Diminishing Returns Threshold The recognition that specification detail has a po

## Core Principle

The Specification Trap is the failure mode where designers over-specify systems in the belief that exhaustive detail ensures quality, when in reality natural language cannot fully capture complex behavior, users don't know what they need until they see it, and over-prescription kills the implementation-time discoveries that produce the best code. The fix is to treat specification and implementation as a single continuous feedback loop, stop specifying at the point where programmer skill can take over, and use prototyping or tracer bullets to break specification spirals.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 57: Some Things Are Better Done than Described

> Specification and implementation are simply different aspects of the same process—an attempt to capture and codify a requirement

> It is naive to assume that a specification will ever capture every detail and nuance of a system or its requirement

> You reach a point of diminishing, or even negative, returns as the specifications get more and more detailed

> Be careful about building specifications layered on top of specifications, without any supporting implementation or prototyping; it's all too easy to specify something that can't be built

> The longer you allow specifications to be security blankets, protecting developers from the scary world of writing code, the harder it will be to move on

> Often, it is only during coding that certain options become apparent

## Anti-Patterns & Fixes

- Over-Specification: Pinning down every detail in excruciating detail under the belief that completeness equals thoroughness. Fix: Stop at the point where programmer skill can take over; leave room for implementation-time discoveries.
- Isolated Phase Development: Gathering requirements, writing specs, and starting coding in complete isolation from each other. Fix: Adopt a seamless approach where feedback from implementation and testing flows back into the specification process.
- Specification Spiral: Layering specifications on top of specifications with no supporting implementation or prototyping. Fix: Break the cycle with prototyping or tracer bullet development to validate specs against reality.
- Specification as Security Blanket: Using detailed specs to delay or avoid writing code. Fix: Recognize when specs are providing comfort rather than value and force a transition to coding.
- Natural Language Precision Fallacy: Attempting to eliminate all ambiguity through increasingly tortured language constructs. Fix: Accept that some behaviors are better demonstrated through prototypes, diagrams, or working code than described in text.

## When To Apply

Load this page when:

- Use this when a task description keeps growing in detail and you haven't written a single line of implementation code yet
- Use this when asked to produce a complete specification before any prototype or tracer implementation exists
- Use this when a specification document references and depends on other specification documents in layers without grounding in working code
- Use this when implementation reveals a simpler or more powerful approach than what the spec prescribes — surface the discovery rather than silently complying
- Use this when a requirement involves a procedural or experiential behavior that is extremely difficult to capture in language alone
- Use this when detecting that spec detail has crossed from clarifying intent to constraining valid implementation choices
- Use this when a user or stakeholder has signed off on a detailed spec but has not yet seen working software

## Concrete Examples

- The British Airways cockpit handover memorandum — an attempt to restate rules 'clearly' that produces incomprehensible circular language about Landing Pilot vs Non-Handling Pilot roles
- Describing how to tie shoelaces in writing — a task almost everyone can perform automatically but almost no one can specify precisely in natural language

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**The Specification Trap**

An LLM coding agent is especially susceptible to the specification trap because it can generate arbitrarily detailed pseudo-specs, interface contracts, and design documents instantly and fluently — creating the illusion of progress while deferring actual implementation. The agent failure mode is generating specification layers that sound authoritative but describe systems that cannot be built as written, or that over-constrain solutions and prevent discovery of better approaches that only emerge during coding. An LLM agent should treat its own generated specs as provisional scaffolding, immediately validate them against prototype implementations, and update the spec when implementation reveals superior alternatives.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Goal Driven Use Cases Cockburn Template Structured textual descriptions of syste

## Core Principle

Requirements are not pre-formed artifacts to collect but deeply buried truths that must be excavated from assumptions, policy, and politics. The core discipline is separating invariant needs from mutable business rules, avoiding overspecification into design or UI, and tracking all scope changes with their schedule impact. Abstractions (domain concepts, access models) outlast the specific policies and interfaces built on top of them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Gather Requirements—Dig for Them

> Work with a User to Think Like a User

> Abstractions Live Longer than Details

> Use a Project Glossary

> Requirements are not architecture. Requirements are not design, nor are they the user interface. Requirements are need.

> Good requirements documents remain abstract.

> Perfection is achieved, not when there is nothing left to add, but when there is nothing left to take away.

> The key to managing growth of requirements is to point out each new feature's impact on the schedule to the project sponsors.

## Anti-Patterns & Fixes

- RequirementsGathering: Treating requirements as pre-existing artifacts to collect rather than hidden truths buried under assumptions and politics. Fix: Actively dig—immerse yourself in the user's domain, observe actual workflows, and question every stated rule.
- HardcodedPolicy: Encoding current business rules (e.g., 'only supervisors can view records') as absolute requirements baked into logic. Fix: State the invariant requirement generically ('authorized users may access') and move the specific policy to metadata or configuration.
- Overspecification: Letting requirements documents drift into design or UI decisions (list box, gray background, front-end/back-end architecture). Fix: Keep requirements as minimal statements of business need; separate implementation suggestions as non-binding examples.
- RequirementsCreep (Boiled Frog): Accepting 'just one more feature' without tracking cumulative impact. Fix: Log every requirement change with sponsor approval and schedule delta so the fifteenth new feature this month is visible.
- VocabularyAmbiguity: Developers and users using the same word for different things or different words for the same thing. Fix: Maintain a shared project glossary accessible to all stakeholders and enforce consistent usage.
- Y2K-style AbstractionFailure: Automating existing business practices without questioning their embedded assumptions (e.g., two-digit years). Fix: Identify domain abstractions (DATE, CURRENCY) and specify invariant services around them rather than replicating current practice.

## When To Apply

Load this page when:

- Use this when a user or product spec states a requirement as a specific UI element (e.g., 'we need a dropdown') to determine whether the UI is the requirement or merely an example of satisfying the real need.
- Use this when implementing an access control or business rule that could change—separate the policy from the requirement and design for metadata-driven configuration.
- Use this when a spec embeds a domain concept (date, currency, measurement) directly in data formats or logic—extract it into an abstraction with its own services.
- Use this when scope is expanding mid-project to quantify the cumulative schedule and resource impact of each added feature before accepting it.
- Use this when domain terminology is ambiguous or inconsistent across stakeholders—create or consult a project glossary before naming variables, classes, or APIs.
- Use this when generating code from a spec that mixes requirements, policy, and design—decompose them before producing any implementation.
- Use this when producing or consuming a requirements document to verify that each statement is a need, not an architecture or UI decision.

## Concrete Examples

- Employee records access: 'Only supervisors and HR may view records' is policy; 'only authorized users may access' is the requirement—the former leads to hardcoded checks, the latter to a configurable access control system.
- Loan term selection: 'The system must let you choose a loan term' is a requirement; 'we need a list box' may or may not be, depending on whether the UI element is essential or merely illustrative.
- Brian Eno's mixing board (Wired, Jan 1999): A technically comprehensive mixer that failed because its interface ignored recording engineers' tactile, intuitive workflow—demonstrating that interface requirements must reflect existing skill sets.
- Y2K two-digit year: Analysts automated existing business practice without abstracting a DATE type, propagating a policy shortcut into an architectural flaw that violated DRY and failed to see beyond current practice.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**36. The Requirements Pit**

An LLM coding agent is especially prone to conflating policy with requirements because it pattern-matches on literal spec language—if a spec says 'only managers can delete records,' the agent will likely emit a hardcoded role check rather than a metadata-driven permission system. Agents also have no mechanism to push back on overspecified requirements (UI prescriptions, architectural mandates) and will faithfully implement them as constraints, baking in fragility. By explicitly decomposing inputs into requirement/policy/implementation layers before generating code, an agent avoids producing logic that is correct for today's policy but wrong for tomorrow's.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Project Glossary A single authoritative source defining all domain specific term

## Core Principle

Requirements are not pre-formed artifacts to collect but deeply buried truths that must be excavated from assumptions, policy, and politics. The core discipline is separating invariant needs from mutable business rules, avoiding overspecification into design or UI, and tracking all scope changes with their schedule impact. Abstractions (domain concepts, access models) outlast the specific policies and interfaces built on top of them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Gather Requirements—Dig for Them

> Work with a User to Think Like a User

> Abstractions Live Longer than Details

> Use a Project Glossary

> Requirements are not architecture. Requirements are not design, nor are they the user interface. Requirements are need.

> Good requirements documents remain abstract.

> Perfection is achieved, not when there is nothing left to add, but when there is nothing left to take away.

> The key to managing growth of requirements is to point out each new feature's impact on the schedule to the project sponsors.

## Anti-Patterns & Fixes

- RequirementsGathering: Treating requirements as pre-existing artifacts to collect rather than hidden truths buried under assumptions and politics. Fix: Actively dig—immerse yourself in the user's domain, observe actual workflows, and question every stated rule.
- HardcodedPolicy: Encoding current business rules (e.g., 'only supervisors can view records') as absolute requirements baked into logic. Fix: State the invariant requirement generically ('authorized users may access') and move the specific policy to metadata or configuration.
- Overspecification: Letting requirements documents drift into design or UI decisions (list box, gray background, front-end/back-end architecture). Fix: Keep requirements as minimal statements of business need; separate implementation suggestions as non-binding examples.
- RequirementsCreep (Boiled Frog): Accepting 'just one more feature' without tracking cumulative impact. Fix: Log every requirement change with sponsor approval and schedule delta so the fifteenth new feature this month is visible.
- VocabularyAmbiguity: Developers and users using the same word for different things or different words for the same thing. Fix: Maintain a shared project glossary accessible to all stakeholders and enforce consistent usage.
- Y2K-style AbstractionFailure: Automating existing business practices without questioning their embedded assumptions (e.g., two-digit years). Fix: Identify domain abstractions (DATE, CURRENCY) and specify invariant services around them rather than replicating current practice.

## When To Apply

Load this page when:

- Use this when a user or product spec states a requirement as a specific UI element (e.g., 'we need a dropdown') to determine whether the UI is the requirement or merely an example of satisfying the real need.
- Use this when implementing an access control or business rule that could change—separate the policy from the requirement and design for metadata-driven configuration.
- Use this when a spec embeds a domain concept (date, currency, measurement) directly in data formats or logic—extract it into an abstraction with its own services.
- Use this when scope is expanding mid-project to quantify the cumulative schedule and resource impact of each added feature before accepting it.
- Use this when domain terminology is ambiguous or inconsistent across stakeholders—create or consult a project glossary before naming variables, classes, or APIs.
- Use this when generating code from a spec that mixes requirements, policy, and design—decompose them before producing any implementation.
- Use this when producing or consuming a requirements document to verify that each statement is a need, not an architecture or UI decision.

## Concrete Examples

- Employee records access: 'Only supervisors and HR may view records' is policy; 'only authorized users may access' is the requirement—the former leads to hardcoded checks, the latter to a configurable access control system.
- Loan term selection: 'The system must let you choose a loan term' is a requirement; 'we need a list box' may or may not be, depending on whether the UI element is essential or merely illustrative.
- Brian Eno's mixing board (Wired, Jan 1999): A technically comprehensive mixer that failed because its interface ignored recording engineers' tactile, intuitive workflow—demonstrating that interface requirements must reflect existing skill sets.
- Y2K two-digit year: Analysts automated existing business practice without abstracting a DATE type, propagating a policy shortcut into an architectural flaw that violated DRY and failed to see beyond current practice.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**36. The Requirements Pit**

An LLM coding agent is especially prone to conflating policy with requirements because it pattern-matches on literal spec language—if a spec says 'only managers can delete records,' the agent will likely emit a hardcoded role check rather than a metadata-driven permission system. Agents also have no mechanism to push back on overspecified requirements (UI prescriptions, architectural mandates) and will faithfully implement them as constraints, baking in fragility. By explicitly decomposing inputs into requirement/policy/implementation layers before generating code, an agent avoids producing logic that is correct for today's policy but wrong for tomorrow's.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Requirements Tracking Actively logging every requirement change with requester a

## Core Principle

Requirements are not pre-formed artifacts to collect but deeply buried truths that must be excavated from assumptions, policy, and politics. The core discipline is separating invariant needs from mutable business rules, avoiding overspecification into design or UI, and tracking all scope changes with their schedule impact. Abstractions (domain concepts, access models) outlast the specific policies and interfaces built on top of them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Gather Requirements—Dig for Them

> Work with a User to Think Like a User

> Abstractions Live Longer than Details

> Use a Project Glossary

> Requirements are not architecture. Requirements are not design, nor are they the user interface. Requirements are need.

> Good requirements documents remain abstract.

> Perfection is achieved, not when there is nothing left to add, but when there is nothing left to take away.

> The key to managing growth of requirements is to point out each new feature's impact on the schedule to the project sponsors.

## Anti-Patterns & Fixes

- RequirementsGathering: Treating requirements as pre-existing artifacts to collect rather than hidden truths buried under assumptions and politics. Fix: Actively dig—immerse yourself in the user's domain, observe actual workflows, and question every stated rule.
- HardcodedPolicy: Encoding current business rules (e.g., 'only supervisors can view records') as absolute requirements baked into logic. Fix: State the invariant requirement generically ('authorized users may access') and move the specific policy to metadata or configuration.
- Overspecification: Letting requirements documents drift into design or UI decisions (list box, gray background, front-end/back-end architecture). Fix: Keep requirements as minimal statements of business need; separate implementation suggestions as non-binding examples.
- RequirementsCreep (Boiled Frog): Accepting 'just one more feature' without tracking cumulative impact. Fix: Log every requirement change with sponsor approval and schedule delta so the fifteenth new feature this month is visible.
- VocabularyAmbiguity: Developers and users using the same word for different things or different words for the same thing. Fix: Maintain a shared project glossary accessible to all stakeholders and enforce consistent usage.
- Y2K-style AbstractionFailure: Automating existing business practices without questioning their embedded assumptions (e.g., two-digit years). Fix: Identify domain abstractions (DATE, CURRENCY) and specify invariant services around them rather than replicating current practice.

## When To Apply

Load this page when:

- Use this when a user or product spec states a requirement as a specific UI element (e.g., 'we need a dropdown') to determine whether the UI is the requirement or merely an example of satisfying the real need.
- Use this when implementing an access control or business rule that could change—separate the policy from the requirement and design for metadata-driven configuration.
- Use this when a spec embeds a domain concept (date, currency, measurement) directly in data formats or logic—extract it into an abstraction with its own services.
- Use this when scope is expanding mid-project to quantify the cumulative schedule and resource impact of each added feature before accepting it.
- Use this when domain terminology is ambiguous or inconsistent across stakeholders—create or consult a project glossary before naming variables, classes, or APIs.
- Use this when generating code from a spec that mixes requirements, policy, and design—decompose them before producing any implementation.
- Use this when producing or consuming a requirements document to verify that each statement is a need, not an architecture or UI decision.

## Concrete Examples

- Employee records access: 'Only supervisors and HR may view records' is policy; 'only authorized users may access' is the requirement—the former leads to hardcoded checks, the latter to a configurable access control system.
- Loan term selection: 'The system must let you choose a loan term' is a requirement; 'we need a list box' may or may not be, depending on whether the UI element is essential or merely illustrative.
- Brian Eno's mixing board (Wired, Jan 1999): A technically comprehensive mixer that failed because its interface ignored recording engineers' tactile, intuitive workflow—demonstrating that interface requirements must reflect existing skill sets.
- Y2K two-digit year: Analysts automated existing business practice without abstracting a DATE type, propagating a policy shortcut into an architectural flaw that violated DRY and failed to see beyond current practice.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**36. The Requirements Pit**

An LLM coding agent is especially prone to conflating policy with requirements because it pattern-matches on literal spec language—if a spec says 'only managers can delete records,' the agent will likely emit a hardcoded role check rather than a metadata-driven permission system. Agents also have no mechanism to push back on overspecified requirements (UI prescriptions, architectural mandates) and will faithfully implement them as constraints, baking in fragility. By explicitly decomposing inputs into requirement/policy/implementation layers before generating code, an agent avoids producing logic that is correct for today's policy but wrong for tomorrow's.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Requirements vs Policy Separation Requirements express invariant needs authorize

## Core Principle

Requirements are not pre-formed artifacts to collect but deeply buried truths that must be excavated from assumptions, policy, and politics. The core discipline is separating invariant needs from mutable business rules, avoiding overspecification into design or UI, and tracking all scope changes with their schedule impact. Abstractions (domain concepts, access models) outlast the specific policies and interfaces built on top of them.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Gather Requirements—Dig for Them

> Work with a User to Think Like a User

> Abstractions Live Longer than Details

> Use a Project Glossary

> Requirements are not architecture. Requirements are not design, nor are they the user interface. Requirements are need.

> Good requirements documents remain abstract.

> Perfection is achieved, not when there is nothing left to add, but when there is nothing left to take away.

> The key to managing growth of requirements is to point out each new feature's impact on the schedule to the project sponsors.

## Anti-Patterns & Fixes

- RequirementsGathering: Treating requirements as pre-existing artifacts to collect rather than hidden truths buried under assumptions and politics. Fix: Actively dig—immerse yourself in the user's domain, observe actual workflows, and question every stated rule.
- HardcodedPolicy: Encoding current business rules (e.g., 'only supervisors can view records') as absolute requirements baked into logic. Fix: State the invariant requirement generically ('authorized users may access') and move the specific policy to metadata or configuration.
- Overspecification: Letting requirements documents drift into design or UI decisions (list box, gray background, front-end/back-end architecture). Fix: Keep requirements as minimal statements of business need; separate implementation suggestions as non-binding examples.
- RequirementsCreep (Boiled Frog): Accepting 'just one more feature' without tracking cumulative impact. Fix: Log every requirement change with sponsor approval and schedule delta so the fifteenth new feature this month is visible.
- VocabularyAmbiguity: Developers and users using the same word for different things or different words for the same thing. Fix: Maintain a shared project glossary accessible to all stakeholders and enforce consistent usage.
- Y2K-style AbstractionFailure: Automating existing business practices without questioning their embedded assumptions (e.g., two-digit years). Fix: Identify domain abstractions (DATE, CURRENCY) and specify invariant services around them rather than replicating current practice.

## When To Apply

Load this page when:

- Use this when a user or product spec states a requirement as a specific UI element (e.g., 'we need a dropdown') to determine whether the UI is the requirement or merely an example of satisfying the real need.
- Use this when implementing an access control or business rule that could change—separate the policy from the requirement and design for metadata-driven configuration.
- Use this when a spec embeds a domain concept (date, currency, measurement) directly in data formats or logic—extract it into an abstraction with its own services.
- Use this when scope is expanding mid-project to quantify the cumulative schedule and resource impact of each added feature before accepting it.
- Use this when domain terminology is ambiguous or inconsistent across stakeholders—create or consult a project glossary before naming variables, classes, or APIs.
- Use this when generating code from a spec that mixes requirements, policy, and design—decompose them before producing any implementation.
- Use this when producing or consuming a requirements document to verify that each statement is a need, not an architecture or UI decision.

## Concrete Examples

- Employee records access: 'Only supervisors and HR may view records' is policy; 'only authorized users may access' is the requirement—the former leads to hardcoded checks, the latter to a configurable access control system.
- Loan term selection: 'The system must let you choose a loan term' is a requirement; 'we need a list box' may or may not be, depending on whether the UI element is essential or merely illustrative.
- Brian Eno's mixing board (Wired, Jan 1999): A technically comprehensive mixer that failed because its interface ignored recording engineers' tactile, intuitive workflow—demonstrating that interface requirements must reflect existing skill sets.
- Y2K two-digit year: Analysts automated existing business practice without abstracting a DATE type, propagating a policy shortcut into an architectural flaw that violated DRY and failed to see beyond current practice.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**36. The Requirements Pit**

An LLM coding agent is especially prone to conflating policy with requirements because it pattern-matches on literal spec language—if a spec says 'only managers can delete records,' the agent will likely emit a hardcoded role check rather than a metadata-driven permission system. Agents also have no mechanism to push back on overspecified requirements (UI prescriptions, architectural mandates) and will faithfully implement them as constraints, baking in fragility. By explicitly decomposing inputs into requirement/policy/implementation layers before generating code, an agent avoids producing logic that is correct for today's policy but wrong for tomorrow's.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Seamless Spec to Implementation Treating requirements gathering design and imple

## Core Principle

The Specification Trap is the failure mode where designers over-specify systems in the belief that exhaustive detail ensures quality, when in reality natural language cannot fully capture complex behavior, users don't know what they need until they see it, and over-prescription kills the implementation-time discoveries that produce the best code. The fix is to treat specification and implementation as a single continuous feedback loop, stop specifying at the point where programmer skill can take over, and use prototyping or tracer bullets to break specification spirals.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 57: Some Things Are Better Done than Described

> Specification and implementation are simply different aspects of the same process—an attempt to capture and codify a requirement

> It is naive to assume that a specification will ever capture every detail and nuance of a system or its requirement

> You reach a point of diminishing, or even negative, returns as the specifications get more and more detailed

> Be careful about building specifications layered on top of specifications, without any supporting implementation or prototyping; it's all too easy to specify something that can't be built

> The longer you allow specifications to be security blankets, protecting developers from the scary world of writing code, the harder it will be to move on

> Often, it is only during coding that certain options become apparent

## Anti-Patterns & Fixes

- Over-Specification: Pinning down every detail in excruciating detail under the belief that completeness equals thoroughness. Fix: Stop at the point where programmer skill can take over; leave room for implementation-time discoveries.
- Isolated Phase Development: Gathering requirements, writing specs, and starting coding in complete isolation from each other. Fix: Adopt a seamless approach where feedback from implementation and testing flows back into the specification process.
- Specification Spiral: Layering specifications on top of specifications with no supporting implementation or prototyping. Fix: Break the cycle with prototyping or tracer bullet development to validate specs against reality.
- Specification as Security Blanket: Using detailed specs to delay or avoid writing code. Fix: Recognize when specs are providing comfort rather than value and force a transition to coding.
- Natural Language Precision Fallacy: Attempting to eliminate all ambiguity through increasingly tortured language constructs. Fix: Accept that some behaviors are better demonstrated through prototypes, diagrams, or working code than described in text.

## When To Apply

Load this page when:

- Use this when a task description keeps growing in detail and you haven't written a single line of implementation code yet
- Use this when asked to produce a complete specification before any prototype or tracer implementation exists
- Use this when a specification document references and depends on other specification documents in layers without grounding in working code
- Use this when implementation reveals a simpler or more powerful approach than what the spec prescribes — surface the discovery rather than silently complying
- Use this when a requirement involves a procedural or experiential behavior that is extremely difficult to capture in language alone
- Use this when detecting that spec detail has crossed from clarifying intent to constraining valid implementation choices
- Use this when a user or stakeholder has signed off on a detailed spec but has not yet seen working software

## Concrete Examples

- The British Airways cockpit handover memorandum — an attempt to restate rules 'clearly' that produces incomprehensible circular language about Landing Pilot vs Non-Handling Pilot roles
- Describing how to tie shoelaces in writing — a task almost everyone can perform automatically but almost no one can specify precisely in natural language

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**The Specification Trap**

An LLM coding agent is especially susceptible to the specification trap because it can generate arbitrarily detailed pseudo-specs, interface contracts, and design documents instantly and fluently — creating the illusion of progress while deferring actual implementation. The agent failure mode is generating specification layers that sound authoritative but describe systems that cannot be built as written, or that over-constrain solutions and prevent discovery of better approaches that only emerge during coding. An LLM agent should treat its own generated specs as provisional scaffolding, immediately validate them against prototype implementations, and update the spec when implementation reveals superior alternatives.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Straightjacket Effect The phenomenon where overly prescriptive specifications re

## Core Principle

The Specification Trap is the failure mode where designers over-specify systems in the belief that exhaustive detail ensures quality, when in reality natural language cannot fully capture complex behavior, users don't know what they need until they see it, and over-prescription kills the implementation-time discoveries that produce the best code. The fix is to treat specification and implementation as a single continuous feedback loop, stop specifying at the point where programmer skill can take over, and use prototyping or tracer bullets to break specification spirals.

## Key Heuristics

These are the load-bearing rules for this concept.

> Tip 57: Some Things Are Better Done than Described

> Specification and implementation are simply different aspects of the same process—an attempt to capture and codify a requirement

> It is naive to assume that a specification will ever capture every detail and nuance of a system or its requirement

> You reach a point of diminishing, or even negative, returns as the specifications get more and more detailed

> Be careful about building specifications layered on top of specifications, without any supporting implementation or prototyping; it's all too easy to specify something that can't be built

> The longer you allow specifications to be security blankets, protecting developers from the scary world of writing code, the harder it will be to move on

> Often, it is only during coding that certain options become apparent

## Anti-Patterns & Fixes

- Over-Specification: Pinning down every detail in excruciating detail under the belief that completeness equals thoroughness. Fix: Stop at the point where programmer skill can take over; leave room for implementation-time discoveries.
- Isolated Phase Development: Gathering requirements, writing specs, and starting coding in complete isolation from each other. Fix: Adopt a seamless approach where feedback from implementation and testing flows back into the specification process.
- Specification Spiral: Layering specifications on top of specifications with no supporting implementation or prototyping. Fix: Break the cycle with prototyping or tracer bullet development to validate specs against reality.
- Specification as Security Blanket: Using detailed specs to delay or avoid writing code. Fix: Recognize when specs are providing comfort rather than value and force a transition to coding.
- Natural Language Precision Fallacy: Attempting to eliminate all ambiguity through increasingly tortured language constructs. Fix: Accept that some behaviors are better demonstrated through prototypes, diagrams, or working code than described in text.

## When To Apply

Load this page when:

- Use this when a task description keeps growing in detail and you haven't written a single line of implementation code yet
- Use this when asked to produce a complete specification before any prototype or tracer implementation exists
- Use this when a specification document references and depends on other specification documents in layers without grounding in working code
- Use this when implementation reveals a simpler or more powerful approach than what the spec prescribes — surface the discovery rather than silently complying
- Use this when a requirement involves a procedural or experiential behavior that is extremely difficult to capture in language alone
- Use this when detecting that spec detail has crossed from clarifying intent to constraining valid implementation choices
- Use this when a user or stakeholder has signed off on a detailed spec but has not yet seen working software

## Concrete Examples

- The British Airways cockpit handover memorandum — an attempt to restate rules 'clearly' that produces incomprehensible circular language about Landing Pilot vs Non-Handling Pilot roles
- Describing how to tie shoelaces in writing — a task almost everyone can perform automatically but almost no one can specify precisely in natural language

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**The Specification Trap**

An LLM coding agent is especially susceptible to the specification trap because it can generate arbitrarily detailed pseudo-specs, interface contracts, and design documents instantly and fluently — creating the illusion of progress while deferring actual implementation. The agent failure mode is generating specification layers that sound authoritative but describe systems that cannot be built as written, or that over-constrain solutions and prevent discovery of better approaches that only emerge during coding. An LLM agent should treat its own generated specs as provisional scaffolding, immediately validate them against prototype implementations, and update the spec when implementation reveals superior alternatives.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
