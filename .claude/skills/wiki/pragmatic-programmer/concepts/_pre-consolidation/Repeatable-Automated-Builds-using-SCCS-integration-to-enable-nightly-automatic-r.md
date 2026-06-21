---
title: Repeatable Automated Builds: using SCCS integration to enable nightly, automatic, regression-tested builds with no manual steps
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
sources: [extracts/pragmatic-programmer/Source-Code-Control.json]
contributing_chapters: ["Source Code Control"]
confidence: high
---

# Repeatable Automated Builds: using SCCS integration to enable nightly, automatic, regression-tested builds with no manual steps

> From chapter: *Source Code Control*

## Core Principle

Source code control systems serve as a project-wide time machine and audit trail, enabling rollback to any prior state, reproducible builds, release management, and concurrent collaboration. The core principle is that everything—source, docs, scripts, and build procedures—must always be under version control, with no exceptions for project size or duration. SCCS integration with automated builds further ensures consistency and repeatability across the entire software lifecycle.

## Key Heuristics

These are the load-bearing rules for this concept.

> Always Use Source Code Control

> Always. Even if you are a single-person team on a one-week project. Even if it's a 'throw-away' prototype.

> Make sure that everything is under source code control—documentation, phone number lists, memos to vendors, makefiles, build and release procedures, that little shell script that burns the CD master—everything.

> The build is repeatable because you can always rebuild the source as it existed on a given date.

> Those who cannot remember the past are condemned to repeat it.

## Anti-Patterns & Fixes

- SkippingSccsForSmallProjects: Developers skip version control for short-lived or solo projects, losing history and auditability. Fix: Always initialize a repository, even for one-week or throw-away work.
- SourceOnlyVersionControl: Teams only track .source files, leaving build scripts, docs, and release procedures unversioned and unreproducible. Fix: Commit every artifact that contributes to the project, including shell scripts, makefiles, and documentation.
- ManualBuilds: Relying on developers to manually copy code into build areas introduces inconsistency and human error. Fix: Integrate the SCCS with an automated build system that pulls from the repository.
- TeamNonAdoption: Waiting for the entire team to adopt SCCS before using it yourself. Fix: Maintain a private personal repository in parallel with whatever the team does, to protect your own work.
- NoReleaseTagging: Failing to tag or identify releases in the SCCS, making it impossible to reproduce a past release. Fix: Use SCCS release identification features every time you ship, so any past release can be regenerated independently.

## When To Apply

Load this page when:

- Use this when starting any new coding task, even a one-file script or prototype, to ensure all changes are tracked from the first commit.
- Use this when preparing a release, to tag the exact state of all files so the release can be reproduced at any future point.
- Use this when a bug is reported against a shipped version, to check out the branch corresponding to that release and apply a targeted fix without shipping in-progress development code.
- Use this when onboarding to a project without SCCS, to set up a private local repository as a safety net even if the team has no shared one.
- Use this when setting up CI/CD pipelines, to connect the build system to the SCCS so builds are automatic, nightly, and regression-tested.
- Use this when asked 'what changed in this file last week?' or 'who broke the build?', to query SCCS change history and diff outputs.
- Use this when generating any non-code artifact (documentation, build scripts, configuration), to ensure it is committed to the repository alongside source files.

## Concrete Examples

- Managing development branches: after a release, bug fixes go to the release branch while new development continues on the main trunk, with selected fixes merged back automatically.
- The text of the book itself being managed under source code control by the authors as an example of tracking non-code artifacts.
- Nightly automated builds pulling the latest source from the repository and running regression tests after developers have gone home.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Source Code Control**

An LLM coding agent generates many incremental code mutations across a session but typically operates statelessly, meaning each generation is a potential silent overwrite with no recoverable history unless SCCS is enforced externally. Without version control, an agent that produces a regressed or broken change has no mechanism to identify what it altered or roll back to the last working state. Agents should treat every file write as a commit candidate and must be configured to operate inside a repository so that diffs, blame, and rollback are available to the orchestrating system or human reviewer.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
