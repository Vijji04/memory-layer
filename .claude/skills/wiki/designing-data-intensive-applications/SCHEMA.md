---
domain: Data-Intensive Systems Engineering
book_slug: designing-data-intensive-applications
phase: 1
created: 2026-05-12
---

# Wiki Schema — Data-Intensive Systems Engineering

## Domain
Engineering knowledge extracted from Phase 1 study: Data-Intensive Systems Engineering.
This wiki covers the concepts, heuristics, and frameworks from this domain.
It is an agent-readable knowledge base — not a book summary.

## Conventions
- File names: PascalCase for concept pages (e.g. `DRY.md`, `DesignByContract.md`)
- Every page has YAML frontmatter (title, created, updated, type, tags, sources, confidence)
- Use [[wikilinks]] to link between concept pages (minimum 2 outbound links per page)
- `index.md` lists every concept page with one-line summary — update on every change
- `log.md` is append-only — every ingest, update, and query is logged
- Raw source: `output/extracts/designing-data-intensive-applications/` — immutable, never modify

## Tag Taxonomy
- phase-1: all pages in this wiki
- designing-data-intensive-applications: all pages in this wiki
- concept: concept/framework pages
- heuristic: pages that are primarily rule collections
- anti-pattern: pages focused on failure modes
- agent-pattern: pages with strong AI-native applicability

## Page Thresholds
- Create a page when a named concept appears as a core framework in 1+ chapters
- Add to an existing page when a later book chapter mentions the same concept
- Split a page when it exceeds 200 lines
- Do NOT create a page for passing mentions

## Update Policy
When new information from another book conflicts with a claim here:
1. Add both claims with source citations
2. Set `contested: true` in frontmatter
3. Note in master wiki cross-refs
