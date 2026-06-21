---
title: Programming by Coincidence
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 7 pages
---

# Programming by Coincidence

> Consolidated from 7 related concept pages.

---

## Accidents of Context A failure mode where code implicitly depends on environment

## Core Principle

Programming by Coincidence is the dangerous practice of writing code that appears to work without understanding why, relying on accidental successes, undocumented behaviors, and unverified assumptions. The antidote — Programming Deliberately — requires always knowing why code works, relying only on documented interfaces, explicitly testing assumptions, and documenting all contextual dependencies. Code written by coincidence is fragile, unfixable when it breaks, and increasingly dangerous as it accumulates.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Program by Coincidence

> Don't code blindfolded. Attempting to build an application you don't fully understand, or to use a technology you aren't familiar with, is an invitation to be misled by coincidences.

> Rely only on reliable things. Don't depend on accidents or assumptions. If you can't tell the difference in particular circumstances, assume the worst.

> For routines you call, rely only on documented behavior. If you can't, for whatever reason, then document your assumption well.

> Don't just test your code, but test your assumptions as well. Don't guess; actually try it.

> Don't be a slave to history. Don't let existing code dictate future code.

> Always be aware of what you are doing.

## Anti-Patterns & Fixes

- Coincidence-Driven Development: Writing code until it 'seems to work' without understanding why, then shipping it. The code breaks under different conditions and is unfixable because the original success was never understood. Fix: Before moving on, explicitly identify and verify why the code works, not just that it works.
- Spurious Call Accumulation: Adding redundant or incorrectly-ordered API calls (e.g., paint/invalidate/validate/revalidate/repaint/paintImmediately) until something works, then leaving them all in. Fix: Understand the correct calling contract of each API and use only the documented, necessary calls.
- Undocumented Behavior Reliance: Depending on error responses, boundary conditions, or side effects of a routine that its author never intended or documented. Fix: Only rely on the documented interface; if you must use undocumented behavior, explicitly document your assumption in code.
- Untested Assumptions: Treating causal relationships (X causes Y) as proven when they are merely observed. Fix: Write assertions or explicit tests that verify assumptions, making them part of the documented, executable specification.
- Context Lock-In: Writing utility modules that silently require a specific environment (GUI, locale, OS) without documenting or enforcing that requirement. Fix: Identify all environmental dependencies and either eliminate them or make them explicit contract preconditions.

## When To Apply

Load this page when:

- Use this when a code change fixes a bug but you cannot explain the mechanism by which it fixes it
- Use this when calling a third-party or library API and the behavior you are relying on is not in its official documentation
- Use this when code works in one environment but needs to be deployed in another (different OS, locale, resolution, or runtime)
- Use this when adding repeated or varied calls to the same API trying different combinations until output is correct
- Use this when an integration test passes but the reason for passage is unclear or the test only covers one narrow scenario
- Use this when inheriting legacy code and deciding whether to keep existing behavior or refactor, to avoid assuming existing behavior is intentional
- Use this when generating or scaffolding boilerplate code to ensure each generated piece is understood before being relied upon

## Concrete Examples

- A soldier probing a minefield with a bayonet, finding no mines, concluding it is safe, then marching forward and being blown up — illustrating false conclusions from limited probing
- Fred repeatedly adding code that 'seems to work' until the program inexplicably breaks and he cannot fix it because he never understood why it worked
- A sequence of GUI calls (paint, invalidate, validate, revalidate, repaint, paintImmediately) added iteratively until the screen renders, left in place because 'it works now'

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Programming by Coincidence**

An LLM coding agent is especially vulnerable to Programming by Coincidence because it generates plausible-looking code based on statistical pattern-matching rather than causal understanding — it can produce code that passes provided test cases by coincidence, relying on undocumented API behaviors or environment assumptions baked into its training data. Unlike a human who at least experienced the code working in a specific context, an agent may confidently emit spurious call sequences or context-dependent code with no flag that the reasoning is coincidental. This framework instructs an agent to explicitly verify each API call against documented contracts, surface all environmental assumptions as explicit preconditions, and refuse to move forward when the mechanism of correctness is unknown rather than when tests merely pass.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Accidents of Implementation A failure mode where code appears to work because of

## Core Principle

Programming by Coincidence is the dangerous practice of writing code that appears to work without understanding why, relying on accidental successes, undocumented behaviors, and unverified assumptions. The antidote — Programming Deliberately — requires always knowing why code works, relying only on documented interfaces, explicitly testing assumptions, and documenting all contextual dependencies. Code written by coincidence is fragile, unfixable when it breaks, and increasingly dangerous as it accumulates.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Program by Coincidence

> Don't code blindfolded. Attempting to build an application you don't fully understand, or to use a technology you aren't familiar with, is an invitation to be misled by coincidences.

> Rely only on reliable things. Don't depend on accidents or assumptions. If you can't tell the difference in particular circumstances, assume the worst.

> For routines you call, rely only on documented behavior. If you can't, for whatever reason, then document your assumption well.

> Don't just test your code, but test your assumptions as well. Don't guess; actually try it.

> Don't be a slave to history. Don't let existing code dictate future code.

> Always be aware of what you are doing.

## Anti-Patterns & Fixes

- Coincidence-Driven Development: Writing code until it 'seems to work' without understanding why, then shipping it. The code breaks under different conditions and is unfixable because the original success was never understood. Fix: Before moving on, explicitly identify and verify why the code works, not just that it works.
- Spurious Call Accumulation: Adding redundant or incorrectly-ordered API calls (e.g., paint/invalidate/validate/revalidate/repaint/paintImmediately) until something works, then leaving them all in. Fix: Understand the correct calling contract of each API and use only the documented, necessary calls.
- Undocumented Behavior Reliance: Depending on error responses, boundary conditions, or side effects of a routine that its author never intended or documented. Fix: Only rely on the documented interface; if you must use undocumented behavior, explicitly document your assumption in code.
- Untested Assumptions: Treating causal relationships (X causes Y) as proven when they are merely observed. Fix: Write assertions or explicit tests that verify assumptions, making them part of the documented, executable specification.
- Context Lock-In: Writing utility modules that silently require a specific environment (GUI, locale, OS) without documenting or enforcing that requirement. Fix: Identify all environmental dependencies and either eliminate them or make them explicit contract preconditions.

## When To Apply

Load this page when:

- Use this when a code change fixes a bug but you cannot explain the mechanism by which it fixes it
- Use this when calling a third-party or library API and the behavior you are relying on is not in its official documentation
- Use this when code works in one environment but needs to be deployed in another (different OS, locale, resolution, or runtime)
- Use this when adding repeated or varied calls to the same API trying different combinations until output is correct
- Use this when an integration test passes but the reason for passage is unclear or the test only covers one narrow scenario
- Use this when inheriting legacy code and deciding whether to keep existing behavior or refactor, to avoid assuming existing behavior is intentional
- Use this when generating or scaffolding boilerplate code to ensure each generated piece is understood before being relied upon

## Concrete Examples

- A soldier probing a minefield with a bayonet, finding no mines, concluding it is safe, then marching forward and being blown up — illustrating false conclusions from limited probing
- Fred repeatedly adding code that 'seems to work' until the program inexplicably breaks and he cannot fix it because he never understood why it worked
- A sequence of GUI calls (paint, invalidate, validate, revalidate, repaint, paintImmediately) added iteratively until the screen renders, left in place because 'it works now'

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Programming by Coincidence**

An LLM coding agent is especially vulnerable to Programming by Coincidence because it generates plausible-looking code based on statistical pattern-matching rather than causal understanding — it can produce code that passes provided test cases by coincidence, relying on undocumented API behaviors or environment assumptions baked into its training data. Unlike a human who at least experienced the code working in a specific context, an agent may confidently emit spurious call sequences or context-dependent code with no flag that the reasoning is coincidental. This framework instructs an agent to explicitly verify each API call against documented contracts, surface all environmental assumptions as explicit preconditions, and refuse to move forward when the mechanism of correctness is unknown rather than when tests merely pass.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Implicit Assumptions Undocumented beliefs held by developers that drive code dec

## Core Principle

Programming by Coincidence is the dangerous practice of writing code that appears to work without understanding why, relying on accidental successes, undocumented behaviors, and unverified assumptions. The antidote — Programming Deliberately — requires always knowing why code works, relying only on documented interfaces, explicitly testing assumptions, and documenting all contextual dependencies. Code written by coincidence is fragile, unfixable when it breaks, and increasingly dangerous as it accumulates.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Program by Coincidence

> Don't code blindfolded. Attempting to build an application you don't fully understand, or to use a technology you aren't familiar with, is an invitation to be misled by coincidences.

> Rely only on reliable things. Don't depend on accidents or assumptions. If you can't tell the difference in particular circumstances, assume the worst.

> For routines you call, rely only on documented behavior. If you can't, for whatever reason, then document your assumption well.

> Don't just test your code, but test your assumptions as well. Don't guess; actually try it.

> Don't be a slave to history. Don't let existing code dictate future code.

> Always be aware of what you are doing.

## Anti-Patterns & Fixes

- Coincidence-Driven Development: Writing code until it 'seems to work' without understanding why, then shipping it. The code breaks under different conditions and is unfixable because the original success was never understood. Fix: Before moving on, explicitly identify and verify why the code works, not just that it works.
- Spurious Call Accumulation: Adding redundant or incorrectly-ordered API calls (e.g., paint/invalidate/validate/revalidate/repaint/paintImmediately) until something works, then leaving them all in. Fix: Understand the correct calling contract of each API and use only the documented, necessary calls.
- Undocumented Behavior Reliance: Depending on error responses, boundary conditions, or side effects of a routine that its author never intended or documented. Fix: Only rely on the documented interface; if you must use undocumented behavior, explicitly document your assumption in code.
- Untested Assumptions: Treating causal relationships (X causes Y) as proven when they are merely observed. Fix: Write assertions or explicit tests that verify assumptions, making them part of the documented, executable specification.
- Context Lock-In: Writing utility modules that silently require a specific environment (GUI, locale, OS) without documenting or enforcing that requirement. Fix: Identify all environmental dependencies and either eliminate them or make them explicit contract preconditions.

## When To Apply

Load this page when:

- Use this when a code change fixes a bug but you cannot explain the mechanism by which it fixes it
- Use this when calling a third-party or library API and the behavior you are relying on is not in its official documentation
- Use this when code works in one environment but needs to be deployed in another (different OS, locale, resolution, or runtime)
- Use this when adding repeated or varied calls to the same API trying different combinations until output is correct
- Use this when an integration test passes but the reason for passage is unclear or the test only covers one narrow scenario
- Use this when inheriting legacy code and deciding whether to keep existing behavior or refactor, to avoid assuming existing behavior is intentional
- Use this when generating or scaffolding boilerplate code to ensure each generated piece is understood before being relied upon

## Concrete Examples

- A soldier probing a minefield with a bayonet, finding no mines, concluding it is safe, then marching forward and being blown up — illustrating false conclusions from limited probing
- Fred repeatedly adding code that 'seems to work' until the program inexplicably breaks and he cannot fix it because he never understood why it worked
- A sequence of GUI calls (paint, invalidate, validate, revalidate, repaint, paintImmediately) added iteratively until the screen renders, left in place because 'it works now'

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Programming by Coincidence**

An LLM coding agent is especially vulnerable to Programming by Coincidence because it generates plausible-looking code based on statistical pattern-matching rather than causal understanding — it can produce code that passes provided test cases by coincidence, relying on undocumented API behaviors or environment assumptions baked into its training data. Unlike a human who at least experienced the code working in a specific context, an agent may confidently emit spurious call sequences or context-dependent code with no flag that the reasoning is coincidental. This framework instructs an agent to explicitly verify each API call against documented contracts, surface all environmental assumptions as explicit preconditions, and refuse to move forward when the mechanism of correctness is unknown rather than when tests merely pass.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Library vs Interwoven Code Distinction A framework that sits behind a tidy inter

## Core Principle

Code generators and wizards accelerate development but transfer ownership of complex, interwoven code to developers who may not understand it—creating fragile systems that cannot be debugged or maintained. The key distinction is that library code sits behind a clean interface and can be trusted as a black box, whereas wizard-generated code becomes part of the application itself and must be fully understood by whoever ships it. The core rule is never to ship or rely on code—regardless of its source—that you cannot explain line by line.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Use Wizard Code You Don't Understand

> Using a wizard designed by a guru does not automatically make Joe developer equally expert.

> Wizards are a one-way street—they cut the code for you, and then move on.

> Eventually, it stops being the wizard's code and starts being Joe's. And no one should be producing code they don't fully understand.

> If you do use a wizard, and you don't understand all the code that it produces, you won't be in control of your own application.

## Anti-Patterns & Fixes

- Wizard Dependency Blindness: Accepting generated code wholesale without reading or understanding it, then being helpless when it needs to be debugged or adapted. Fix: Read every line of generated code; verify you understand it and could have written it yourself.
- Coincidental Functionality: Shipping wizard-generated code that appears to work but contains unneeded or misunderstood behavior. Fix: Audit generated output for relevance and correctness before integrating it.
- False Expertise Transfer: Assuming that using an expert-designed tool confers the expert's knowledge. Fix: Treat generated code as a learning artifact—study it, then own it consciously.
- Invisible Integration: Allowing generated code to be interwoven with hand-written logic without a clear interface boundary. Fix: Factor generated code behind clean interfaces where possible, or fully internalize it before coupling it to application logic.

## When To Apply

Load this page when:

- Use this when a scaffolding tool, code generator, or AI assistant produces boilerplate or skeleton code that will be merged directly into application logic.
- Use this when integrating a large block of auto-generated code whose every line has not been reviewed and understood.
- Use this when debugging a failure in code that was generated rather than hand-written and the root cause is unclear.
- Use this when a generated component needs to be modified or extended and the original generation tool is no longer available or applicable.
- Use this when evaluating whether to ship code produced by a wizard or code-generation pipeline under time pressure.
- Use this when generated code appears to work but contains patterns or structures the developer cannot explain.

## Concrete Examples

- Microsoft Visual C++ wizard generating over 1,200 lines of code for an MDI application with OLE container support from a single button click.
- Wizards used to create server components, implement Java beans, and handle network interfaces in complex infrastructure scenarios.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evil Wizards**

An LLM coding agent is itself the wizard: it generates code that becomes interwoven with the codebase, and the human or downstream agent accepting it faces the exact 'Joe developer' problem at scale—large volumes of plausible-looking code with no guaranteed understanding behind it. The critical failure mode is that an agent can chain-generate dependent code blocks, each accepted without review, creating deep layers of coincidental correctness that collapse unpredictably under changed requirements or edge cases. Agents must be prompted or constrained to produce code in auditable, interface-bounded units, and should flag generated segments that require owner comprehension before integration.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Programming Deliberately A discipline of always knowing why code works proceedin

## Core Principle

Programming by Coincidence is the dangerous practice of writing code that appears to work without understanding why, relying on accidental successes, undocumented behaviors, and unverified assumptions. The antidote — Programming Deliberately — requires always knowing why code works, relying only on documented interfaces, explicitly testing assumptions, and documenting all contextual dependencies. Code written by coincidence is fragile, unfixable when it breaks, and increasingly dangerous as it accumulates.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Program by Coincidence

> Don't code blindfolded. Attempting to build an application you don't fully understand, or to use a technology you aren't familiar with, is an invitation to be misled by coincidences.

> Rely only on reliable things. Don't depend on accidents or assumptions. If you can't tell the difference in particular circumstances, assume the worst.

> For routines you call, rely only on documented behavior. If you can't, for whatever reason, then document your assumption well.

> Don't just test your code, but test your assumptions as well. Don't guess; actually try it.

> Don't be a slave to history. Don't let existing code dictate future code.

> Always be aware of what you are doing.

## Anti-Patterns & Fixes

- Coincidence-Driven Development: Writing code until it 'seems to work' without understanding why, then shipping it. The code breaks under different conditions and is unfixable because the original success was never understood. Fix: Before moving on, explicitly identify and verify why the code works, not just that it works.
- Spurious Call Accumulation: Adding redundant or incorrectly-ordered API calls (e.g., paint/invalidate/validate/revalidate/repaint/paintImmediately) until something works, then leaving them all in. Fix: Understand the correct calling contract of each API and use only the documented, necessary calls.
- Undocumented Behavior Reliance: Depending on error responses, boundary conditions, or side effects of a routine that its author never intended or documented. Fix: Only rely on the documented interface; if you must use undocumented behavior, explicitly document your assumption in code.
- Untested Assumptions: Treating causal relationships (X causes Y) as proven when they are merely observed. Fix: Write assertions or explicit tests that verify assumptions, making them part of the documented, executable specification.
- Context Lock-In: Writing utility modules that silently require a specific environment (GUI, locale, OS) without documenting or enforcing that requirement. Fix: Identify all environmental dependencies and either eliminate them or make them explicit contract preconditions.

## When To Apply

Load this page when:

- Use this when a code change fixes a bug but you cannot explain the mechanism by which it fixes it
- Use this when calling a third-party or library API and the behavior you are relying on is not in its official documentation
- Use this when code works in one environment but needs to be deployed in another (different OS, locale, resolution, or runtime)
- Use this when adding repeated or varied calls to the same API trying different combinations until output is correct
- Use this when an integration test passes but the reason for passage is unclear or the test only covers one narrow scenario
- Use this when inheriting legacy code and deciding whether to keep existing behavior or refactor, to avoid assuming existing behavior is intentional
- Use this when generating or scaffolding boilerplate code to ensure each generated piece is understood before being relied upon

## Concrete Examples

- A soldier probing a minefield with a bayonet, finding no mines, concluding it is safe, then marching forward and being blown up — illustrating false conclusions from limited probing
- Fred repeatedly adding code that 'seems to work' until the program inexplicably breaks and he cannot fix it because he never understood why it worked
- A sequence of GUI calls (paint, invalidate, validate, revalidate, repaint, paintImmediately) added iteratively until the screen renders, left in place because 'it works now'

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Programming by Coincidence**

An LLM coding agent is especially vulnerable to Programming by Coincidence because it generates plausible-looking code based on statistical pattern-matching rather than causal understanding — it can produce code that passes provided test cases by coincidence, relying on undocumented API behaviors or environment assumptions baked into its training data. Unlike a human who at least experienced the code working in a specific context, an agent may confidently emit spurious call sequences or context-dependent code with no flag that the reasoning is coincidental. This framework instructs an agent to explicitly verify each API call against documented contracts, surface all environmental assumptions as explicit preconditions, and refuse to move forward when the mechanism of correctness is unknown rather than when tests merely pass.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Programming by Coincidence Writing or accepting code that works without understa

## Core Principle

Code generators and wizards accelerate development but transfer ownership of complex, interwoven code to developers who may not understand it—creating fragile systems that cannot be debugged or maintained. The key distinction is that library code sits behind a clean interface and can be trusted as a black box, whereas wizard-generated code becomes part of the application itself and must be fully understood by whoever ships it. The core rule is never to ship or rely on code—regardless of its source—that you cannot explain line by line.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Use Wizard Code You Don't Understand

> Using a wizard designed by a guru does not automatically make Joe developer equally expert.

> Wizards are a one-way street—they cut the code for you, and then move on.

> Eventually, it stops being the wizard's code and starts being Joe's. And no one should be producing code they don't fully understand.

> If you do use a wizard, and you don't understand all the code that it produces, you won't be in control of your own application.

## Anti-Patterns & Fixes

- Wizard Dependency Blindness: Accepting generated code wholesale without reading or understanding it, then being helpless when it needs to be debugged or adapted. Fix: Read every line of generated code; verify you understand it and could have written it yourself.
- Coincidental Functionality: Shipping wizard-generated code that appears to work but contains unneeded or misunderstood behavior. Fix: Audit generated output for relevance and correctness before integrating it.
- False Expertise Transfer: Assuming that using an expert-designed tool confers the expert's knowledge. Fix: Treat generated code as a learning artifact—study it, then own it consciously.
- Invisible Integration: Allowing generated code to be interwoven with hand-written logic without a clear interface boundary. Fix: Factor generated code behind clean interfaces where possible, or fully internalize it before coupling it to application logic.

## When To Apply

Load this page when:

- Use this when a scaffolding tool, code generator, or AI assistant produces boilerplate or skeleton code that will be merged directly into application logic.
- Use this when integrating a large block of auto-generated code whose every line has not been reviewed and understood.
- Use this when debugging a failure in code that was generated rather than hand-written and the root cause is unclear.
- Use this when a generated component needs to be modified or extended and the original generation tool is no longer available or applicable.
- Use this when evaluating whether to ship code produced by a wizard or code-generation pipeline under time pressure.
- Use this when generated code appears to work but contains patterns or structures the developer cannot explain.

## Concrete Examples

- Microsoft Visual C++ wizard generating over 1,200 lines of code for an MDI application with OLE container support from a single button click.
- Wizards used to create server components, implement Java beans, and handle network interfaces in complex infrastructure scenarios.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evil Wizards**

An LLM coding agent is itself the wizard: it generates code that becomes interwoven with the codebase, and the human or downstream agent accepting it faces the exact 'Joe developer' problem at scale—large volumes of plausible-looking code with no guaranteed understanding behind it. The critical failure mode is that an agent can chain-generate dependent code blocks, each accepted without review, creating deep layers of coincidental correctness that collapse unpredictably under changed requirements or edge cases. Agents must be prompted or constrained to produce code in auditable, interface-bounded units, and should flag generated segments that require owner comprehension before integration.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Wizard Code Ownership Transfer Generated code starts as the wizards but becomes

## Core Principle

Code generators and wizards accelerate development but transfer ownership of complex, interwoven code to developers who may not understand it—creating fragile systems that cannot be debugged or maintained. The key distinction is that library code sits behind a clean interface and can be trusted as a black box, whereas wizard-generated code becomes part of the application itself and must be fully understood by whoever ships it. The core rule is never to ship or rely on code—regardless of its source—that you cannot explain line by line.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Use Wizard Code You Don't Understand

> Using a wizard designed by a guru does not automatically make Joe developer equally expert.

> Wizards are a one-way street—they cut the code for you, and then move on.

> Eventually, it stops being the wizard's code and starts being Joe's. And no one should be producing code they don't fully understand.

> If you do use a wizard, and you don't understand all the code that it produces, you won't be in control of your own application.

## Anti-Patterns & Fixes

- Wizard Dependency Blindness: Accepting generated code wholesale without reading or understanding it, then being helpless when it needs to be debugged or adapted. Fix: Read every line of generated code; verify you understand it and could have written it yourself.
- Coincidental Functionality: Shipping wizard-generated code that appears to work but contains unneeded or misunderstood behavior. Fix: Audit generated output for relevance and correctness before integrating it.
- False Expertise Transfer: Assuming that using an expert-designed tool confers the expert's knowledge. Fix: Treat generated code as a learning artifact—study it, then own it consciously.
- Invisible Integration: Allowing generated code to be interwoven with hand-written logic without a clear interface boundary. Fix: Factor generated code behind clean interfaces where possible, or fully internalize it before coupling it to application logic.

## When To Apply

Load this page when:

- Use this when a scaffolding tool, code generator, or AI assistant produces boilerplate or skeleton code that will be merged directly into application logic.
- Use this when integrating a large block of auto-generated code whose every line has not been reviewed and understood.
- Use this when debugging a failure in code that was generated rather than hand-written and the root cause is unclear.
- Use this when a generated component needs to be modified or extended and the original generation tool is no longer available or applicable.
- Use this when evaluating whether to ship code produced by a wizard or code-generation pipeline under time pressure.
- Use this when generated code appears to work but contains patterns or structures the developer cannot explain.

## Concrete Examples

- Microsoft Visual C++ wizard generating over 1,200 lines of code for an MDI application with OLE container support from a single button click.
- Wizards used to create server components, implement Java beans, and handle network interfaces in complex infrastructure scenarios.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evil Wizards**

An LLM coding agent is itself the wizard: it generates code that becomes interwoven with the codebase, and the human or downstream agent accepting it faces the exact 'Joe developer' problem at scale—large volumes of plausible-looking code with no guaranteed understanding behind it. The critical failure mode is that an agent can chain-generate dependent code blocks, each accepted without review, creating deep layers of coincidental correctness that collapse unpredictably under changed requirements or edge cases. Agents must be prompted or constrained to produce code in auditable, interface-bounded units, and should flag generated segments that require owner comprehension before integration.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
