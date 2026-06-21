---
title: Outline-First Writing: Plan what you want to say via an outline before writing, then refine until it accurately conveys the intended message
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/6-Communicate.json]
contributing_chapters: ["6. Communicate!"]
confidence: high
---

# Outline-First Writing: Plan what you want to say via an outline before writing, then refine until it accurately conveys the intended message

> From chapter: *6. Communicate!*

## Core Principle

Effective communication requires deliberate preparation: knowing your message, your audience's needs and moment, and choosing style and format accordingly — because even the best ideas are orphaned without it. The WISDOM acrostic provides a structured pre-communication checklist, while the two-way transaction model demands listening as actively as speaking. Written artifacts (documents, emails, code) must receive the same care as verbal communication, including presentation quality and timely follow-up.

## Key Heuristics

These are the load-bearing rules for this concept.

> It's Both What You Say and the Way You Say It

> Having the best ideas, the finest code, or the most pragmatic thinking is ultimately sterile unless you can communicate with other people. A good idea is an orphan without effective communication.

> Know what you want to say. Know your audience. Choose your moment. Choose a style. Make it look good. Involve your audience. Be a listener. Get back to people.

> Make what you're saying relevant in time, as well as in content.

> If you don't listen to them, they won't listen to you.

> Always respond to e-mails and voice mails, even if the response is simply 'I'll get back to you later.'

> We often find that the documents we produce end up being less important than the process we go through to produce them.

## Anti-Patterns & Fixes

- TechJargon Mismatch: Presenting technical depth to non-technical stakeholders ('a development geek glazes over the eyes of the vice president of marketing'), which alienates the audience and kills buy-in. Fix: Use the WISDOM acrostic to tailor content, framing, and vocabulary to each specific audience segment.
- Stream-of-Consciousness Writing: Starting a technical document by typing whatever comes to mind after 'Introduction' without a plan. Fix: Write an outline first, then ask 'Does this get across whatever I'm trying to say?' and refine before drafting.
- Ignoring Presentation Quality: Concentrating solely on content while neglecting visual and formatting quality of documents. Fix: Use style sheets, learn basic layout commands, check spelling both automatically and manually.
- Unanswered Requests: Failing to respond to emails or messages, leaving people feeling forgotten. Fix: Always reply, even if only to say 'I'll get back to you later.'
- Wrong Timing for Requests: Raising sensitive or resource-intensive topics when the audience is stressed, distracted, or emotionally unavailable. Fix: Assess the audience's current priorities and emotional state; ask 'Is this a good time to talk about...?' before diving in.
- Monologue Meetings: Treating meetings as one-directional broadcasts rather than dialogs, preventing genuine understanding. Fix: Ask questions, encourage summarization, and turn the meeting into a dialog.

## When To Apply

Load this page when:

- Use this when writing a technical proposal or design document that will be read by both engineers and non-technical stakeholders.
- Use this when generating a code review comment, PR description, or commit message that needs to convey intent to future developers.
- Use this when producing status reports, architecture summaries, or README files that must serve audiences with different levels of expertise.
- Use this when drafting an automated response, notification, or error message that users of varying sophistication will encounter.
- Use this when generating documentation and the agent must decide how much detail to include, what terminology to use, and what format to adopt.
- Use this when an agent must communicate a blocker, limitation, or trade-off decision to a human reviewer or orchestrating system.
- Use this when the agent needs to present multiple implementation options and must frame each option for a different decision-maker (e.g., cost-focused vs. performance-focused).

## Concrete Examples

- Pitching a Web-based bug reporting system to four different audiences — end users (24/7 access), marketing (sales boost), support managers (fewer staff needed, automation), and developers (new tech experience) — each with a different framing.
- An employee who distributed email criticisms of his boss without realizing the boss was on the distribution list, illustrating the permanence and reach of email.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**6. Communicate!**

An LLM coding agent generates outputs consumed by multiple audiences simultaneously — developers reading code, users reading docs, and orchestrators reading structured output — but defaults to a single uniform register, causing mismatch for all audiences. The WISDOM framework forces the agent to explicitly parameterize audience type before generating any communication artifact (docstring, PR description, error message), preventing the agent failure mode of technically-correct but contextually-inappropriate output. The 'involve your audience' principle also maps to agents surfacing early drafts or partial results for human feedback rather than generating a complete artifact in isolation.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
