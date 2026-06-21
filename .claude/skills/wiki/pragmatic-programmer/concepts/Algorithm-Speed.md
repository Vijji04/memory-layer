---
title: Algorithm Speed
created: 2026-05-11
updated: 2026-05-11
type: concept
tags: [phase-1, pragmatic-programmer, concept]
confidence: high
consolidated_from: 3 pages
---

# Algorithm Speed

> Consolidated from 3 related concept pages.

---

## Big O Notation A mathematical approximation that expresses the upper bound on ho

## Core Principle

Algorithm Speed covers using Big O notation to estimate and bound how algorithms scale in time and memory, with common-sense rules mapping code structure (loops, recursion, divide-and-conquer) to complexity classes. The core pragmatic stance is to estimate complexity at write-time, test estimates empirically with real data at scale, and treat theoretical analysis as necessary but not sufficient — production environment behavior, not asymptotic class alone, is the final arbiter. Premature optimization and always choosing the fastest algorithm are both warned against; appropriateness to actual input size and constraints matters more.

## Key Heuristics

These are the load-bearing rules for this concept.

> Estimate the Order of Your Algorithms

> Test Your Estimates

> Whenever you find yourself writing a simple loop, you know that you have an O(n) algorithm. If that loop contains an inner loop, then you're looking at O(n²).

> If you have an algorithm that is O(n²), try to find a divide and conquer approach that will take you down to O(n log n).

> The only timing that counts is the speed of your code, running in the production environment, with real data.

> Be wary of premature optimization. It's always a good idea to make sure an algorithm really is a bottleneck before investing your precious time trying to improve it.

> A simple O(n) loop may well perform better than a complex, O(n log n) one for smaller values of n, particularly if the O(n log n) algorithm has an expensive inner loop.

> The fastest one is not always the best for the job.

## Anti-Patterns & Fixes

- PrematureOptimization: Investing time optimizing an algorithm before confirming it is actually a bottleneck, wasting effort on non-critical paths. Fix: Profile first, identify the actual bottleneck, then optimize.
- IgnoringScaleAssumptions: Testing code only on small datasets and assuming linear behavior will hold at scale, missing superlinear degradation. Fix: Test with input sizes that reflect production scale; plot timing curves across multiple input magnitudes.
- AlwaysChoosingFastestAlgorithm: Selecting a theoretically superior algorithm (e.g., quicksort over insertion sort) regardless of input size or setup cost, adding unnecessary complexity. Fix: Match algorithm choice to actual input size and constraints; for small n, simpler is often better.
- IgnoringPracticalSystemEffects: Relying on theoretical complexity alone without accounting for real-world factors like memory thrashing, cache behavior, or ordered vs. random input. Fix: Combine theoretical analysis with empirical profiling on real data in the production environment.
- NestedLoopComplacency: Writing nested loops without explicitly reasoning about the combined growth rate, assuming it will be 'fast enough'. Fix: Consciously identify O(n²) or worse patterns at write-time and evaluate whether input bounds make this acceptable.

## When To Apply

Load this page when:

- Use this when generating code that contains loops or recursive calls and the maximum input size is not yet verified to be bounded and small.
- Use this when choosing between two algorithmic approaches and one appears more complex but theoretically faster.
- Use this when asked to scale existing code from handling thousands of records to millions.
- Use this when writing nested loops where both loop bounds depend on external input (e.g., database record counts, user-provided lists).
- Use this when a generated solution passes unit tests on small test cases but has not been evaluated for production-scale input.
- Use this when implementing search, sort, or partitioning logic to identify which complexity class the approach falls into before committing to it.
- Use this when a combinatoric approach (permutations, subsets, brute-force search) is the naive solution and input size could grow beyond single digits.
- Use this when profiling reveals unexpected performance degradation and the cause needs to be traced to algorithmic complexity vs. system effects.

## Concrete Examples

- 1 second to process 100 records: projected times for 1,000 records across O(1), O(log n), O(n), O(n log n), O(n²), and O(2^n) — ranging from 1s to ~10^17 years.
- Binary search as an example of O(log n) sublinear algorithm that doesn't examine every candidate.
- Quicksort as O(n log n) average case but O(n²) worst case on sorted input, illustrating the gap between theoretical and practical behavior.
- Radix sort running out of real memory on a 64MB Pentium with >7 million numbers, causing swap usage and dramatic timing degradation — illustrating practical system effects overriding theoretical complexity.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**32. Algorithm Speed**

An LLM coding agent is particularly prone to generating O(n²) or worse solutions because it pattern-matches to 'working' code from training data without explicitly reasoning about scale — a nested loop that passes tests on a 10-item fixture looks identical to one that will time out on 100,000 items. Agents also lack the human instinct to pause and ask 'how large can n get?' so they need explicit triggers to invoke complexity analysis before committing to an implementation. The empirical curve-fitting tip is especially valuable for agents: rather than trusting theoretical analysis alone, an agent should generate timing scaffolding alongside the algorithm to validate scaling behavior against real data.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Common Sense Estimation A pattern matching heuristic mapping code structure to c

## Core Principle

Algorithm Speed covers using Big O notation to estimate and bound how algorithms scale in time and memory, with common-sense rules mapping code structure (loops, recursion, divide-and-conquer) to complexity classes. The core pragmatic stance is to estimate complexity at write-time, test estimates empirically with real data at scale, and treat theoretical analysis as necessary but not sufficient — production environment behavior, not asymptotic class alone, is the final arbiter. Premature optimization and always choosing the fastest algorithm are both warned against; appropriateness to actual input size and constraints matters more.

## Key Heuristics

These are the load-bearing rules for this concept.

> Estimate the Order of Your Algorithms

> Test Your Estimates

> Whenever you find yourself writing a simple loop, you know that you have an O(n) algorithm. If that loop contains an inner loop, then you're looking at O(n²).

> If you have an algorithm that is O(n²), try to find a divide and conquer approach that will take you down to O(n log n).

> The only timing that counts is the speed of your code, running in the production environment, with real data.

> Be wary of premature optimization. It's always a good idea to make sure an algorithm really is a bottleneck before investing your precious time trying to improve it.

> A simple O(n) loop may well perform better than a complex, O(n log n) one for smaller values of n, particularly if the O(n log n) algorithm has an expensive inner loop.

> The fastest one is not always the best for the job.

## Anti-Patterns & Fixes

- PrematureOptimization: Investing time optimizing an algorithm before confirming it is actually a bottleneck, wasting effort on non-critical paths. Fix: Profile first, identify the actual bottleneck, then optimize.
- IgnoringScaleAssumptions: Testing code only on small datasets and assuming linear behavior will hold at scale, missing superlinear degradation. Fix: Test with input sizes that reflect production scale; plot timing curves across multiple input magnitudes.
- AlwaysChoosingFastestAlgorithm: Selecting a theoretically superior algorithm (e.g., quicksort over insertion sort) regardless of input size or setup cost, adding unnecessary complexity. Fix: Match algorithm choice to actual input size and constraints; for small n, simpler is often better.
- IgnoringPracticalSystemEffects: Relying on theoretical complexity alone without accounting for real-world factors like memory thrashing, cache behavior, or ordered vs. random input. Fix: Combine theoretical analysis with empirical profiling on real data in the production environment.
- NestedLoopComplacency: Writing nested loops without explicitly reasoning about the combined growth rate, assuming it will be 'fast enough'. Fix: Consciously identify O(n²) or worse patterns at write-time and evaluate whether input bounds make this acceptable.

## When To Apply

Load this page when:

- Use this when generating code that contains loops or recursive calls and the maximum input size is not yet verified to be bounded and small.
- Use this when choosing between two algorithmic approaches and one appears more complex but theoretically faster.
- Use this when asked to scale existing code from handling thousands of records to millions.
- Use this when writing nested loops where both loop bounds depend on external input (e.g., database record counts, user-provided lists).
- Use this when a generated solution passes unit tests on small test cases but has not been evaluated for production-scale input.
- Use this when implementing search, sort, or partitioning logic to identify which complexity class the approach falls into before committing to it.
- Use this when a combinatoric approach (permutations, subsets, brute-force search) is the naive solution and input size could grow beyond single digits.
- Use this when profiling reveals unexpected performance degradation and the cause needs to be traced to algorithmic complexity vs. system effects.

## Concrete Examples

- 1 second to process 100 records: projected times for 1,000 records across O(1), O(log n), O(n), O(n log n), O(n²), and O(2^n) — ranging from 1s to ~10^17 years.
- Binary search as an example of O(log n) sublinear algorithm that doesn't examine every candidate.
- Quicksort as O(n log n) average case but O(n²) worst case on sorted input, illustrating the gap between theoretical and practical behavior.
- Radix sort running out of real memory on a 64MB Pentium with >7 million numbers, causing swap usage and dramatic timing degradation — illustrating practical system effects overriding theoretical complexity.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**32. Algorithm Speed**

An LLM coding agent is particularly prone to generating O(n²) or worse solutions because it pattern-matches to 'working' code from training data without explicitly reasoning about scale — a nested loop that passes tests on a 10-item fixture looks identical to one that will time out on 100,000 items. Agents also lack the human instinct to pause and ask 'how large can n get?' so they need explicit triggers to invoke complexity analysis before committing to an implementation. The empirical curve-fitting tip is especially valuable for agents: rather than trusting theoretical analysis alone, an agent should generate timing scaffolding alongside the algorithm to validate scaling behavior against real data.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->

---

## Empirical Curve Fitting Running an algorithm with varying input sizes plotting r

## Core Principle

Algorithm Speed covers using Big O notation to estimate and bound how algorithms scale in time and memory, with common-sense rules mapping code structure (loops, recursion, divide-and-conquer) to complexity classes. The core pragmatic stance is to estimate complexity at write-time, test estimates empirically with real data at scale, and treat theoretical analysis as necessary but not sufficient — production environment behavior, not asymptotic class alone, is the final arbiter. Premature optimization and always choosing the fastest algorithm are both warned against; appropriateness to actual input size and constraints matters more.

## Key Heuristics

These are the load-bearing rules for this concept.

> Estimate the Order of Your Algorithms

> Test Your Estimates

> Whenever you find yourself writing a simple loop, you know that you have an O(n) algorithm. If that loop contains an inner loop, then you're looking at O(n²).

> If you have an algorithm that is O(n²), try to find a divide and conquer approach that will take you down to O(n log n).

> The only timing that counts is the speed of your code, running in the production environment, with real data.

> Be wary of premature optimization. It's always a good idea to make sure an algorithm really is a bottleneck before investing your precious time trying to improve it.

> A simple O(n) loop may well perform better than a complex, O(n log n) one for smaller values of n, particularly if the O(n log n) algorithm has an expensive inner loop.

> The fastest one is not always the best for the job.

## Anti-Patterns & Fixes

- PrematureOptimization: Investing time optimizing an algorithm before confirming it is actually a bottleneck, wasting effort on non-critical paths. Fix: Profile first, identify the actual bottleneck, then optimize.
- IgnoringScaleAssumptions: Testing code only on small datasets and assuming linear behavior will hold at scale, missing superlinear degradation. Fix: Test with input sizes that reflect production scale; plot timing curves across multiple input magnitudes.
- AlwaysChoosingFastestAlgorithm: Selecting a theoretically superior algorithm (e.g., quicksort over insertion sort) regardless of input size or setup cost, adding unnecessary complexity. Fix: Match algorithm choice to actual input size and constraints; for small n, simpler is often better.
- IgnoringPracticalSystemEffects: Relying on theoretical complexity alone without accounting for real-world factors like memory thrashing, cache behavior, or ordered vs. random input. Fix: Combine theoretical analysis with empirical profiling on real data in the production environment.
- NestedLoopComplacency: Writing nested loops without explicitly reasoning about the combined growth rate, assuming it will be 'fast enough'. Fix: Consciously identify O(n²) or worse patterns at write-time and evaluate whether input bounds make this acceptable.

## When To Apply

Load this page when:

- Use this when generating code that contains loops or recursive calls and the maximum input size is not yet verified to be bounded and small.
- Use this when choosing between two algorithmic approaches and one appears more complex but theoretically faster.
- Use this when asked to scale existing code from handling thousands of records to millions.
- Use this when writing nested loops where both loop bounds depend on external input (e.g., database record counts, user-provided lists).
- Use this when a generated solution passes unit tests on small test cases but has not been evaluated for production-scale input.
- Use this when implementing search, sort, or partitioning logic to identify which complexity class the approach falls into before committing to it.
- Use this when a combinatoric approach (permutations, subsets, brute-force search) is the naive solution and input size could grow beyond single digits.
- Use this when profiling reveals unexpected performance degradation and the cause needs to be traced to algorithmic complexity vs. system effects.

## Concrete Examples

- 1 second to process 100 records: projected times for 1,000 records across O(1), O(log n), O(n), O(n log n), O(n²), and O(2^n) — ranging from 1s to ~10^17 years.
- Binary search as an example of O(log n) sublinear algorithm that doesn't examine every candidate.
- Quicksort as O(n log n) average case but O(n²) worst case on sorted input, illustrating the gap between theoretical and practical behavior.
- Radix sort running out of real memory on a 64MB Pentium with >7 million numbers, causing swap usage and dramatic timing degradation — illustrating practical system effects overriding theoretical complexity.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**32. Algorithm Speed**

An LLM coding agent is particularly prone to generating O(n²) or worse solutions because it pattern-matches to 'working' code from training data without explicitly reasoning about scale — a nested loop that passes tests on a 10-item fixture looks identical to one that will time out on 100,000 items. Agents also lack the human instinct to pause and ask 'how large can n get?' so they need explicit triggers to invoke complexity analysis before committing to an implementation. The empirical curve-fitting tip is especially valuable for agents: rather than trusting theoretical analysis alone, an agent should generate timing scaffolding alongside the algorithm to validate scaling behavior against real data.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/pragmatic-programmer/` (Phase 1)
<!-- Add cross-book references after master wiki is built -->
