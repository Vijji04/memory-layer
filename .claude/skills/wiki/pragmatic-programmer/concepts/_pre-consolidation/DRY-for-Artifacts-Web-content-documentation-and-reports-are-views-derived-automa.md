---
title: DRY for Artifacts: Web content, documentation, and reports are views derived automatically from the repository; they should never be maintained by hand separately
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Ubiquitous-Automation.json]
contributing_chapters: ["Ubiquitous Automation"]
confidence: high
---

# DRY for Artifacts: Web content, documentation, and reports are views derived automatically from the repository; they should never be maintained by hand separately

> From chapter: *Ubiquitous Automation*

## Core Principle

Ubiquitous Automation argues that every recurring project operation must be scripted and executed automatically rather than performed manually, because humans are inconsistent and unrepeatable while scripts are not. The chapter covers automating builds, code generation, regression testing, documentation publishing, and even administrative workflows using tools like make, cron, and scripting languages. The governing principle is that a project should be fully buildable, testable, and shippable from scratch with a single command, and all derived artifacts should be regenerated automatically from their canonical sources.

## Key Heuristics

These are the load-bearing rules for this concept.

> Don't Use Manual Procedures

> Civilization advances by extending the number of important operations we can perform without thinking.

> People just aren't as repeatable as computers are. Nor should we expect them to be.

> A shell script or batch file will execute the same instructions, in the same order, time after time.

> We want to check out, build, test, and ship with a single command.

> Misleading information is worse than no information at all.

> Let the computer do the repetitious, the mundane—it will do a better job of it than we would.

> Manual procedures leave consistency up to chance; repeatability isn't guaranteed, especially if aspects of the procedure are open to interpretation by different people.

## Anti-Patterns & Fixes

- Multi-Page Manual Install Instructions: Developers follow long click-by-click IDE setup guides, resulting in subtly different environments per machine and environment-specific bugs. Fix: Replace with a single automated setup script checked into source control.
- Memory-Dependent Scheduling: Relying on developers to remember when to run maintenance scripts causes tasks to be skipped or run inconsistently. Fix: Use cron or equivalent schedulers to run all recurring tasks unattended.
- IDE-Only Builds: Using only an IDE for builds makes it difficult to automate, hook in code generation, or run regression tests consistently. Fix: Use makefiles or equivalent build scripts even alongside IDEs.
- Hand-Maintained Documentation/Web Content: Keeping a project website or docs updated manually leads to stale, misleading content. Fix: Generate and publish all documentation automatically as part of the nightly build or check-in hook.
- Infrequent Test Runs: Not running regression tests regularly means broken code may not be discovered until months after the causative change. Fix: Run the full test suite automatically on every nightly build.
- Separate Final Build Process Undiscovered Until Ship Day: Leaving final build steps (ISO images, permission fixes, optimizations) untested until release. Fix: Automate final build steps with a dedicated make target (e.g., make final) and run them early and regularly.

## When To Apply

Load this page when:

- Use this when setting up a new project repository and deciding how builds, tests, and releases will be executed by team members.
- Use this when onboarding new developers requires following multi-step manual environment setup instructions.
- Use this when the same sequence of commands is typed repeatedly to build, test, or deploy the project.
- Use this when bugs appear on some developer machines but not others due to inconsistent environment configuration.
- Use this when project documentation or a team website must be kept in sync with the codebase.
- Use this when code review, approval workflows, or administrative paperwork is tracked manually and prone to being forgotten.
- Use this when a regression is discovered that traces back to a code change from weeks or months ago, indicating tests are not run on every build.
- Use this when generating derived artifacts (source files, headers, docs) from a canonical source such as XML or schema files.

## Concrete Examples

- Client site where system admins gave each developer multi-page IDE add-on installation instructions, resulting in every developer's machine being loaded slightly differently and environment-specific bugs.
- A crontab file scheduling nightly builds at 00:05, backups at 03:15 on weekdays, and expense reports at midnight on the first of each month.
- A makefile rule that takes a test.xml file, runs a Perl conversion script to produce test.java, then compiles it to test.class automatically when 'make test.class' is invoked.
- Embedding a '/* Status: needs_review */' marker in source files so a script can auto-detect files needing review, post a web page, send email, or schedule a calendar meeting.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Ubiquitous Automation**

An LLM coding agent is highly prone to generating setup steps, build instructions, or deployment procedures as prose or ad-hoc shell commands rather than encoding them in versioned, executable automation scripts—reproducing the exact anti-pattern of manual procedures. Unlike a human who might remember to run a script, an agent operating across sessions has no persistent memory, making content-driven and scheduled automation (cron, makefiles, CI pipelines) even more critical: the automation must be self-triggering, not agent-triggered. Agents should default to producing makefile targets, CI workflow files, or setup scripts as first-class artifacts, not README instructions, to ensure any future agent or human can achieve a correct result with a single command.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
