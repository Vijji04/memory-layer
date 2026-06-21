---
title: Agent vs. LLM Call Distinction: A plain LLM call is a stateless function (input → output); an agent is a stateful loop that adapts based on observed results
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
sources: [extracts/llmops-ai-agents/What-Are-AI-Agents.json]
contributing_chapters: ["What Are AI Agents"]
confidence: high
---

# Agent vs. LLM Call Distinction: A plain LLM call is a stateless function (input → output); an agent is a stateful loop that adapts based on observed results

> From chapter: *What Are AI Agents*

## Core Principle

An agent is defined by a loop — perceive, reason, act, observe, repeat — not by the use of an LLM, which alone is just a stateless function call. Every agent regardless of complexity is built from four components: sensors (input), LLM brain (decisions), actuators (world-changing actions), and memory (state across steps). The central practical warning is the LLM Fallacy: running generated agent code that works is not the same as understanding it, and the inability to explain each line leaves the developer helpless when the agent behaves unexpectedly.

## Key Heuristics

These are the load-bearing rules for this concept.

> An agent observes its environment, reasons about what to do, takes an action, and then observes the result of that action — in a loop.

> A plain LLM call is like asking a cookbook author to write a recipe. An agent is like actually cooking — you are in the kitchen, adapting as you go.

> An agent that can only read and respond is a Q&A system, not a full agent. Actuators are what make an agent an agent.

> The loop means the agent can use information it did not have in the first response. It can observe, adapt, and try again.

> If you ask an LLM to write agent code for you and just copy-paste it, you will think you understand agents — but you will not.

> Always trace through every line of code yourself. Ask: 'Where is the perceive step? Where is the reason step?'

> Be able to look at a problem and say 'this is a multi-step looping task, we need an agent' or 'this is just classification, a single LLM call is fine.'

## Anti-Patterns & Fixes

- LLM Fallacy: Generating or copy-pasting agent code that runs successfully creates the illusion of understanding. When the agent breaks or behaves unexpectedly, there is no mental model to debug with. Fix: Trace every line manually, identify which loop phase each line belongs to, and ask 'what happens if I remove this line?' before moving on.
- Framework-First Learning: Starting with a framework quickstart before understanding the agent loop means you are building on concepts you do not own. Fix: Understand perceive → reason → act → observe as a mental model before touching any framework.
- Missing max_steps Guard: An agent loop without a step limit can run indefinitely, consuming tokens and compute. Fix: Always set a max_steps parameter and return a fallback message when the limit is reached.
- Sensors Without Actuators: Building an agent that can perceive and reason but cannot write, call APIs, or change state produces only a Q&A system. Fix: Explicitly define actuators (tools, API calls, writes) as a required architectural component.
- Stateless Reasoning: Failing to append both the LLM's decision and the tool result to memory means the next loop iteration has no context for what already happened. Fix: After every act step, append both the assistant response and the tool result to the memory list before re-entering the reason step.

## When To Apply

Load this page when:

- Use this when deciding whether a task requires an agent loop or a single LLM call — if the task requires using the result of one step to determine the next step, it needs the agent loop.
- Use this when implementing the core run() method of any agent class — the for loop, memory appends, tool dispatch, and final-answer check must all map to explicit loop phases.
- Use this when an agent keeps calling a tool repeatedly without terminating — check whether tool results are being appended to memory so the LLM can observe them in the next reasoning step.
- Use this when designing a new agent system from scratch — enumerate all four components (sensors, LLM brain, actuators, memory) explicitly before writing any code.
- Use this when choosing between agent types for a problem — classify by whether the task needs memory of state, goal planning, optimization across outcomes, or delegation to sub-agents.
- Use this when an agent reaches max_steps without answering — treat it as a signal that either the tool set is insufficient, the system prompt is under-constrained, or the task requires decomposition.
- Use this when reviewing generated agent code — verify that the perceive, reason, act, observe, and repeat phases are all present and correctly ordered before trusting the output.

## Concrete Examples

- Weather agent example: user asks 'What's the weather in Tokyo?' — agent calls weather_tool('Tokyo'), receives JSON result, then formats a final natural-language answer across 6 explicit loop steps
- Chef in a restaurant kitchen analogy: cooking a pasta primavera maps perceive/reason/act/observe/repeat to looking around, deciding order of operations, chopping, checking results, and moving to the next step
- SimpleAgent class: a minimal Python implementation showing memory list, max_steps loop, LLM generate call, tool dispatch, and memory append for both assistant response and tool result

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**What Are AI Agents**

An LLM coding agent generating agent code faces a specific failure mode: it can produce syntactically correct, runnable agent code that omits critical loop semantics — most commonly failing to append tool results back to memory, which causes the inner LLM to reason without observing its own prior actions, creating infinite or nonsensical loops. Unlike a human who notices when 'something feels wrong' during debugging, an LLM agent has no runtime introspection unless the reasoning trace is explicitly logged and fed back as context. Applying the Four-Component Anatomy as a generation checklist — verifying sensors, brain, actuators, and memory are all present and wired together — prevents the LLM from producing structurally incomplete agents that appear to work on the happy path but fail silently on any multi-step task.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
