---
title: LLMOps and AI Agents — Overview
created: 2026-05-12
updated: 2026-05-12
type: overview
tags: [phase-2, llmops-ai-agents]
---

# LLMOps and AI Agents

> Phase 2 knowledge domain. 98 concept pages.

## What This Wiki Covers

This wiki encodes the core frameworks, heuristics, and agent-applicable patterns
from deep study of the Phase 2 curriculum: **LLMOps and AI Agents**.

It is not a book summary. It is a structured knowledge base — each page is a
named concept with full detail: principle, heuristics, anti-patterns, examples,
and AI-native application guidance.

## Core Themes

- **What Are AI Agents:** An agent is defined by a loop — perceive, reason, act, observe, repeat — not by the use of an LLM, which alone is just a stateless function call. Every agent regardless of complexity is built from fou...

- **Agentic Design Patterns:** This chapter defines the four foundational agentic design patterns — Tool Use, RAG, Planning, and Reflection — with sufficient depth to recognize, implement, and combine them. Each pattern addresses a...

- **Multi-Agent Orchestration:** Multi-agent systems become necessary when a task exceeds a single agent's context, requires domain specialization, benefits from parallelism, or demands failure isolation. This chapter defines five ca...

- **LLMOps Essentials:** LLMOps is the discipline of keeping LLM agents reliable and cost-efficient in production, structured as four mandatory layers: Context Engineering, Memory Architecture, Evaluation, and Observability &...

- **Building Your First Agent (Design, RAG, Evals, Guardrails):** This chapter provides an eight-step methodology for building a first agent that begins with defining the Job To Be Done in plain English — not with framework selection — and progresses through constra...

## Concept Index (quick nav)

All concepts in this wiki:

- [[4-5-Rebuild-Cycle-Iterative-pre-execution-validation-where-each-rebuild-pass-tar]] — 4-5 Rebuild Cycle: Iterative pre-execution validation where each rebuild pass targets a distinct error class (breaking changes, referential integrity, simulation failures, performance, permissions) before presenting to humans
- [[4-Layer-LLMOps-Stack-A-production-architecture-with-four-mandatory-layers-Contex]] — 4-Layer LLMOps Stack: A production architecture with four mandatory layers — Context Engineering (what the agent sees), Memory Architecture (what it remembers), Evaluation (how you know it works), and Observability & Guardrails (can you see and stop what's happening)
- [[5-Coordination-Questions-Framework-A-checklist-task-decomposition-communication-]] — 5 Coordination Questions Framework: A checklist (task decomposition, communication channel, failure strategy, human checkpoints, observability) for designing any multi-agent system
- [[Agent-Loop-PRAOR-The-perceive-reason-act-observe-repeat-cycle-that-distinguishes]] — Agent Loop (PRAOR): The perceive → reason → act → observe → repeat cycle that distinguishes agents from single LLM calls
- [[Agent-vs-LLM-Call-Distinction-A-plain-LLM-call-is-a-stateless-function-input-out]] — Agent vs. LLM Call Distinction: A plain LLM call is a stateless function (input → output); an agent is a stateful loop that adapts based on observed results
- [[AgentSessionAnalysisImprovementDeploy-Loop-The-core-metacognitive-cycle-where-an]] — Agent→Session→Analysis→Improvement→Deploy Loop: The core metacognitive cycle where an agent executes, stores full execution traces, aggregates sessions to find patterns, proposes improvements, gets human approval, then deploys — never skipping the approval gate
- [[Audit-Trail-as-Accountability-Layer-log-requirement-generated-artifact-validatio]] — Audit Trail as Accountability Layer: log requirement, generated artifact, validation results, approver identity, and timestamp so human engineers bear traceable responsibility
- [[Augment-Not-Replace-Clinical-Decision-Support-Agent-gathers-and-organizes-eviden]] — Augment-Not-Replace Clinical Decision Support: Agent gathers and organizes evidence ranked by alignment with physician impression, but retains zero override authority over the doctor's final judgment
- [[Autonomous-Coding-Agent-Loop-Clone-Analyze-Plan-Implement-Verify-run-tests-Creat]] — Autonomous Coding Agent Loop: Clone → Analyze → Plan → Implement → Verify (run tests) → Create PR → Await human review, with rollback at any failure point
- [[Bias-Detection-as-Architectural-Component-A-background-fairness-audit-process-us]] — Bias Detection as Architectural Component: A background fairness audit process (using the 4/5ths rule) that runs independently of the main ranking pipeline to surface disparate impact before it compounds
- [[Blocklist-Based-Safety-Validation-instead-of-proving-code-correct-intractable-pr]] — Blocklist-Based Safety Validation: instead of proving code correct (intractable), programmatically check for known-unsafe patterns and block on any match
- [[Canary-Deployment-Gradual-traffic-shifting-eg-1525100-with-metrics-monitoring-an]] — Canary Deployment: Gradual traffic shifting (e.g., 1%→5%→25%→100%) with metrics monitoring and automatic rollback thresholds
- [[Circuit-Breaker-Pattern-A-state-machine-CLOSEDOPENHALF-OPEN-that-automatically-d]] — Circuit Breaker Pattern: A state machine (CLOSED→OPEN→HALF_OPEN) that automatically disables a misbehaving agent and routes traffic away until recovery is confirmed
- [[Citation-Grounding-Requiring-every-LLM-response-to-cite-exact-document-section-a]] — Citation Grounding: Requiring every LLM response to cite exact document, section, and page number so users can verify and update sources
- [[Claim-Extraction-Verification-Loop-break-generated-responses-into-atomic-verifia]] — Claim Extraction + Verification Loop: break generated responses into atomic verifiable claims, check each against ground-truth policy documents, then decide send vs. escalate
- [[Client-Isolation-Layer-Per-client-policy-objects-enforce-tool-allowlists-data-re]] — Client Isolation Layer: Per-client policy objects enforce tool allowlists, data residency, concurrent workflow limits, and audit levels before any request reaches execution infrastructure
- [[Compliance-Access-Log-Pattern-immutable-append-only-audit-trail-recording-who-ac]] — Compliance Access Log Pattern: immutable, append-only audit trail recording who accessed what resource, when, under which agent, and whether it was approved
- [[Confidence-Gated-Escalation-Using-model-confidence-scores-as-routing-signals-rat]] — Confidence-Gated Escalation: Using model confidence scores as routing signals rather than final decisions — above threshold auto-act, below threshold escalate to next tier
- [[Confidence-Weighted-Voting-merge-agent-verdicts-by-scoring-each-as-verdict-weigh]] — Confidence-Weighted Voting: merge agent verdicts by scoring each as (verdict_weight × confidence), aggregating per verdict type, and selecting the highest aggregate
- [[Constraint-Surface-Definition-A-stable-rarely-changed-specification-of-what-the-]] — Constraint Surface Definition: A stable, rarely-changed specification of what the agent can observe, what actions it can take, and what it is forbidden from doing — distinct from the code that implements it
- [[Context-Budget-Model-A-token-allocation-framework-that-assigns-fixed-percentage-]] — Context Budget Model: A token-allocation framework that assigns fixed percentage budgets to each context component (system prompt first/non-negotiable, ~40% to retrieved docs, ~20% to tool results, remainder to conversation history) with recency-first pruning
- [[Context-Bus-Message-Bus-a-shared-publishsubscribe-context-store-that-decouples-a]] — Context Bus (Message Bus): a shared publish/subscribe context store that decouples agents from each other, letting each publish its output and read others' outputs without direct coupling
- [[Continuous-Eval-Loop-Scheduling-evaluation-to-run-on-recent-production-data-on-a]] — Continuous Eval Loop: Scheduling evaluation to run on recent production data on a recurring basis, comparing against a baseline and alerting when quality degrades beyond a threshold
- [[Convergence-Threshold-Model-Stop-iterating-when-a-sufficient-count-of-hypotheses]] — Convergence Threshold Model: Stop iterating when a sufficient count of hypotheses have been strongly supported or refuted; avoids infinite exploration by treating convergence as a first-class exit condition
- [[Cost-Attribution-Pipeline-token-usage-and-dollar-cost-attached-as-span-tags-at-t]] — Cost Attribution Pipeline: token usage and dollar cost attached as span tags at the LLM call level, enabling per-query, per-model, per-user cost breakdown
- [[Counterfactual-Training-Data-Pattern-Deliberately-including-negative-examples-pe]] — Counterfactual Training Data Pattern: Deliberately including negative examples (people not hired who would have succeeded, people hired who failed) to break selection bias in feedback loops
- [[DAG-Workflow-Construction-Workflow-steps-are-modeled-as-a-directed-acyclic-graph]] — DAG Workflow Construction: Workflow steps are modeled as a directed acyclic graph with explicit dependencies, enabling topological execution ordering, reproducibility, and auditability
- [[Decision-Gate-Framework-Break-automated-pipelines-into-explicit-gates-and-identi]] — Decision Gate Framework: Break automated pipelines into explicit gates and identify which gates legally or ethically require human decision-making vs. agent execution
- [[Escalation-Threshold-System-numeric-confidence-cutoffs-per-intent-that-trigger-h]] — Escalation Threshold System: numeric confidence cutoffs per intent that trigger human handoff when classification or verification confidence falls below threshold
- [[Event-DrivenReactive-Pattern-Independent-agents-that-respond-to-events-rather-th]] — Event-Driven/Reactive Pattern: Independent agents that respond to events rather than being explicitly called by an orchestrator
- [[Fan-OutFan-In-spawn-N-independent-agents-in-parallel-then-merge-their-results-wi]] — Fan-Out/Fan-In: spawn N independent agents in parallel, then merge their results with explicit conflict resolution logic
- [[Four-Component-Anatomy-Every-agent-is-composed-of-Sensors-LLM-Brain-Actuators-an]] — Four-Component Anatomy: Every agent is composed of Sensors, LLM Brain, Actuators, and Memory — removing any one breaks the agent
- [[Golden-Dataset-Regression-Testing-A-curated-set-of-verified-inputoutput-pairs-ru]] — Golden Dataset Regression Testing: A curated set of verified input/output pairs run on every system change to detect regressions before deployment
- [[Golden-Dataset-A-curated-human-validated-set-of-100-500-test-vectors-query-expec]] — Golden Dataset: A curated, human-validated set of 100-500 test vectors (query + expected output + metadata) representing the source of truth for agent behavior, versioned and monitored for staleness
- [[Graph-RAG-Graph-Retrieval-Augmented-Generation-traversing-a-knowledge-graph-of-d]] — Graph RAG (Graph Retrieval-Augmented Generation): traversing a knowledge graph of dependencies rather than doing text search, enabling true blast-radius and impact reasoning
- [[Guardrail-Layer-Architecture-A-three-layer-wrapper-around-agent-logic-with-indep]] — Guardrail Layer Architecture: A three-layer wrapper around agent logic with independent input guards, output guards, and tool-call guards—each capable of blocking independently
- [[Hierarchical-Orchestration-with-Human-in-the-Loop-Checkpoints-A-multi-agent-arch]] — Hierarchical Orchestration with Human-in-the-Loop Checkpoints: A multi-agent architecture where a task router classifies intent and delegates to specialized sub-agents, all feeding into a human approval gate before execution
- [[Hierarchical-Pattern-Nested-orchestrators-arranged-like-an-org-chart-for-enterpr]] — Hierarchical Pattern: Nested orchestrators arranged like an org chart for enterprise-scale or security-isolated domains
- [[Hybrid-PhysicsML-Modeling-Encoding-hard-physical-constraints-explicitly-in-code-]] — Hybrid Physics+ML Modeling: Encoding hard physical constraints explicitly in code rather than learning them from data, then layering ML on top for optimization within those constraints
- [[Hybrid-RAG-Dense-Sparse-RRF-Combines-BM25-lexical-search-with-dense-vector-embed]] — Hybrid RAG (Dense + Sparse + RRF): Combines BM25 lexical search with dense vector embeddings, merged via Reciprocal Rank Fusion, to handle both exact-term and semantic queries in specialized domains
- [[Hybrid-Retrieval-Pipeline-BM25-Dense-RRF-Combine-sparse-BM25-and-dense-embedding]] — Hybrid Retrieval Pipeline (BM25 + Dense + RRF): Combine sparse (BM25) and dense (embedding) retrieval with Reciprocal Rank Fusion and cross-encoder reranking to maximize recall and precision before generation
- [[HypothesisDesignExecuteValidateRefine-Loop-The-scientific-research-loop-for-expe]] — Hypothesis→Design→Execute→Validate→Refine Loop: The scientific research loop for experimenter agents, where each iteration generates a testable hypothesis, designs targeted experiments, runs them, validates against evidence, and refines the next hypothesis based on results
- [[Intent-Classification-Pipeline-classify-incoming-messages-into-typed-intents-wit]] — Intent Classification Pipeline: classify incoming messages into typed intents with confidence scores before routing to any handler
- [[Intent-Router-Handler-Registry-map-each-intent-to-a-dedicated-handler-with-its-o]] — Intent Router + Handler Registry: map each intent to a dedicated handler with its own required_info, guardrails, escalation_threshold, and auto-respond flag
- [[Job-To-Be-Done-JTBD-Define-the-agents-purpose-in-plain-English-by-specifying-who]] — Job To Be Done (JTBD): Define the agent's purpose in plain English by specifying who uses it, what they accomplish, what success looks like, and what failure costs — before choosing any technology
- [[LLM-as-Judge-Evaluation-Using-a-separate-LLM-call-to-score-agent-outputs-against]] — LLM-as-Judge Evaluation: Using a separate LLM call to score agent outputs against rubrics, enabling automated quality assessment beyond rule-based checks
- [[LLM-as-Judge-Using-a-separate-LLM-with-calibrated-criteria-specific-prompts-fait]] — LLM-as-Judge: Using a separate LLM with calibrated, criteria-specific prompts (faithfulness, groundedness, completeness, safety) to score agent outputs at scale, validated against human agreement rates
- [[Linear-DAG-Sequential-Pipeline-a-directed-acyclic-graph-where-each-stages-output]] — Linear DAG (Sequential Pipeline): a directed acyclic graph where each stage's output is the next stage's input, with explicit input/output contracts at each node
- [[Metadata-First-Filtering-Pre-filtering-a-structured-corpus-by-deterministic-meta]] — Metadata-First Filtering: Pre-filtering a structured corpus by deterministic metadata fields (grade, domain, code) before semantic search to reduce search space 10-100x
- [[Minimum-Safety-Architecture-A-six-check-gate-physical-feasibility-redundancy-saf]] — Minimum Safety Architecture: A six-check gate (physical feasibility, redundancy, safety margins, staged rollout, monitoring+rollback, human approval) that must be fully satisfied before any industrial agent executes a physical change
- [[Multi-Model-Routing-Classifying-input-type-first-then-routing-to-the-specialized]] — Multi-Model Routing: Classifying input type first, then routing to the specialized model best suited for that type (historical retrieval, physics simulation, or hybrid), rather than using a single model for all inputs
- [[Multi-Tier-Latency-Budget-Architecture-A-cascade-of-tiers-cache-5ms-personalizat]] — Multi-Tier Latency Budget Architecture: A cascade of tiers (cache <5ms, personalization <50ms, deep reasoning <500ms) where each tier handles progressively rarer but more complex cases, with Tier 1 satisfying ~95% of requests
- [[Observable-Agent-Pattern-Spans-Traces-Every-agent-decision-emits-structured-Open]] — Observable Agent Pattern (Spans + Traces): Every agent decision emits structured OpenTelemetry spans capturing what was decided, why, confidence level, and supporting evidence for post-hoc debuggability
- [[Orchestrator-Worker-Decomposition-one-planner-agent-breaks-a-complex-problem-int]] — Orchestrator-Worker Decomposition: one planner agent breaks a complex problem into independent subproblems, dispatches each to a specialist worker, collects results, and synthesizes a final answer
- [[Orchestrator-Worker-Pattern-One-orchestrator-decomposes-a-task-and-delegates-sub]] — Orchestrator-Worker Pattern: One orchestrator decomposes a task and delegates subtasks to specialized workers, then synthesizes results
- [[Parallel-Eval-Architecture-A-dedicated-evaluation-system-that-mirrors-the-agent-]] — Parallel Eval Architecture: A dedicated evaluation system that mirrors the agent system structure, running golden datasets through judge inference to produce metrics and deployment decisions in isolation from production traffic
- [[Parallel-Fan-OutFan-In-Pattern-A-task-is-split-into-independent-subtasks-execute]] — Parallel Fan-Out/Fan-In Pattern: A task is split into independent subtasks executed concurrently, then merged into one result
- [[Parallel-Screening-Pattern-Run-multiple-independent-compliancerisk-checks-simult]] — Parallel Screening Pattern: Run multiple independent compliance/risk checks simultaneously with a merge layer, so total latency equals the slowest single check rather than the sum of all checks
- [[Partial-Results-Doctrine-accept-and-use-incomplete-results-when-some-agents-time]] — Partial Results Doctrine: accept and use incomplete results when some agents timeout or fail, flagging missing agents for reprocessing rather than blocking on full completion
- [[Pattern-Selection-Framework-Decision-logic-mapping-task-properties-needs-private]] — Pattern Selection Framework: Decision logic mapping task properties (needs private knowledge, needs APIs, has multiple steps, accuracy-critical) to the appropriate subset of the four patterns
- [[Pattern-Threshold-Filtering-Only-act-on-failure-patterns-affecting-5-or-100-sess]] — Pattern Threshold Filtering: Only act on failure patterns affecting >5% (or >100 sessions) of the corpus; patterns below threshold are treated as noise and discarded
- [[Per-Agent-Timeout-apply-timeouts-individually-to-each-parallel-agent-so-fast-age]] — Per-Agent Timeout: apply timeouts individually to each parallel agent so fast agents return immediately while slow agents are awaited independently
- [[Planning-Pattern-Agent-explicitly-decomposes-a-complex-task-into-ordered-steps-b]] — Planning Pattern: Agent explicitly decomposes a complex task into ordered steps before executing, enabling replanning on failure rather than blindly looping tool calls
- [[Policy-Compliance-Gate-a-separate-post-generation-check-that-validates-tone-data]] — Policy Compliance Gate: a separate post-generation check that validates tone, data safety, and policy adherence before sending any response
- [[Production-Readiness-Checklist-An-executable-gate-keeping-checklist-that-blocks-]] — Production Readiness Checklist: An executable, gate-keeping checklist that blocks deployment if any of ~20 codified criteria fail
- [[Quality-Gate-Pattern-rejecting-or-halting-low-confidence-items-early-in-the-pipe]] — Quality Gate Pattern: rejecting or halting low-confidence items early in the pipeline to prevent garbage propagation through downstream stages
- [[Query-to-Structure-Parsing-Extracting-structured-metadata-grade-level-domain-con]] — Query-to-Structure Parsing: Extracting structured metadata (grade level, domain, concept) from natural language queries to enable deterministic filtering with semantic fallback
- [[QueryTrace-Schema-A-structured-per-query-log-capturing-retrieval-scores-rerankin]] — QueryTrace Schema: A structured per-query log capturing retrieval scores, reranking scores, token counts, latency, citations, and fallback status — enabling deterministic replay and debugging of any failure
- [[RAG-Pattern-Agent-retrieves-relevant-chunks-from-a-knowledge-base-before-generat]] — RAG Pattern: Agent retrieves relevant chunks from a knowledge base before generating an answer, grounding responses in evidence rather than training data alone
- [[Reciprocal-Rank-Fusion-RRF-A-rank-merging-algorithm-scoring-each-document-as-1kr]] — Reciprocal Rank Fusion (RRF): A rank-merging algorithm scoring each document as 1/(k+rank) across retrieval methods, boosting confidence when both sparse and dense agree
- [[Reflection-Pattern-Agent-critiques-its-own-output-before-returning-it-using-a-se]] — Reflection Pattern: Agent critiques its own output before returning it, using a separate critic pass to catch errors in long-form or accuracy-critical responses
- [[Reflection-vs-Learning-Separation-Treating-session-reflection-cheap-frequent-as-]] — Reflection vs. Learning Separation: Treating session reflection (cheap, frequent) as distinct from code/prompt changes (expensive, gated) so that observation never directly mutates agent behavior without an intervening approval step
- [[Safety-Threshold-Rule-require-agreement-from-2-agents-before-taking-the-highest-]] — Safety Threshold Rule: require agreement from 2+ agents before taking the highest-severity action, downgrading single-agent extremes to reduce false positives
- [[Sequential-Gate-Pattern-ordering-dependent-agents-so-compliancevalidation-agents]] — Sequential Gate Pattern: ordering dependent agents so compliance/validation agents run only after upstream agents publish results, enforcing data-dependency constraints without explicit orchestration logic
- [[Sequential-Pipeline-Pattern-Agents-arranged-as-an-assembly-line-where-each-stage]] — Sequential Pipeline Pattern: Agents arranged as an assembly line where each stage's output is the next stage's input
- [[Seven-Agent-Types-taxonomy-A-classification-of-agents-from-simple-reflex-no-memo]] — Seven Agent Types taxonomy: A classification of agents from simple-reflex (no memory) through model-based, goal-based, utility-based, to multi-agent orchestration patterns
- [[Shadow-Mode-Deployment-Running-a-new-agent-in-parallel-with-the-production-agent]] — Shadow Mode Deployment: Running a new agent in parallel with the production agent to validate agreement before full cutover
- [[Short-Circuit-Logic-skipping-intermediate-pipeline-stages-when-a-condition-eg-cr]] — Short-Circuit Logic: skipping intermediate pipeline stages when a condition (e.g., critical severity) makes them unnecessary, reducing latency
- [[Slice-Evaluation-Breaking-eval-results-down-by-difficulty-category-and-other-met]] — Slice Evaluation: Breaking eval results down by difficulty, category, and other metadata dimensions to reveal where an agent struggles rather than reporting a single aggregate metric
- [[Span-of-Control-Principle-An-orchestrator-managing-5-specialists-is-more-reliabl]] — Span-of-Control Principle: An orchestrator managing 5 specialists is more reliable than one managing 50 — reliability degrades super-linearly with breadth of control
- [[State-Persistence-per-Stage-storing-each-stages-durable-output-so-that-on-failur]] — State Persistence per Stage: storing each stage's durable output so that on failure, only the failed stage needs to be retried, not the full pipeline
- [[Structure-Aware-Chunking-Chunking-strategy-that-respects-document-hierarchy-chap]] — Structure-Aware Chunking: Chunking strategy that respects document hierarchy (chapters, sections, subsections) and preserves metadata (page numbers, section hierarchy) rather than splitting on raw token limits
- [[Structured-Logging-Schema-all-log-entries-are-JSON-objects-with-a-consistent-sch]] — Structured Logging Schema: all log entries are JSON objects with a consistent schema (timestamp, trace_id, span_id, level, message, tags) enabling machine-parseable querying
- [[Tenant-Context-Isolation-Thread-local-or-request-scoped-tenant-binding-that-auto]] — Tenant Context Isolation: Thread-local or request-scoped tenant binding that automatically filters all data access by tenant ID
- [[Three-Agent-Patterns-A-decision-framework-for-first-agents-Single-Agent-RAG-stat]] — Three Agent Patterns: A decision framework for first agents — Single-Agent RAG (static knowledge, independent queries), Conversational Router (multi-turn state, intent branching), and Narrow Action Agent (1-3 tool calls with sequential branching logic)
- [[Three-Gate-Approval-Pipeline-Generation-Formal-Validation-Human-Approval-where-e]] — Three-Gate Approval Pipeline: Generation → Formal Validation → Human Approval, where each gate has a distinct and non-overlapping responsibility (creative, rigorous, accountable)
- [[Three-Layer-Hierarchy-Intent-planner-Layer-1-disambiguates-user-goals-domain-wor]] — Three-Layer Hierarchy: Intent planner (Layer 1) disambiguates user goals, domain workflow orchestrators (Layer 2) plan multi-step DAGs, specialist tool agents (Layer 3) execute narrow actions against single integrations
- [[Three-Level-Evaluation-Plan-Evaluate-agents-at-component-level-does-each-piece-w]] — Three-Level Evaluation Plan: Evaluate agents at component level (does each piece work?), unit level (does each step produce sane output?), and end-to-end level (does the whole pipeline meet SLOs?)
- [[Tier-Based-Resource-Allocation-EnterprisePremiumStandard-tiers-map-deterministic]] — Tier-Based Resource Allocation: Enterprise/Premium/Standard tiers map deterministically to execution environments (on-premise VPC, dedicated cluster, shared cluster) driven by policy, not ad-hoc decisions
- [[Tiered-Alert-Severity-Model-alert-rules-classified-as-PAGEURGENTWARNINGINFO-mapp]] — Tiered Alert Severity Model: alert rules classified as PAGE/URGENT/WARNING/INFO mapped to escalation paths (PagerDuty → Jira ticket → log warning → log info)
- [[Tiered-Context-Windowing-Routing-requests-to-lightweightstandarddeep-agent-tiers]] — Tiered Context Windowing: Routing requests to lightweight/standard/deep agent tiers based on complexity signals, trading cost and latency against capability
- [[Tiered-Filtering-with-Escalation-A-5-tier-content-moderation-architecture-that-r]] — Tiered Filtering with Escalation: A 5-tier content moderation architecture that routes content through progressively more expensive checks (hash → rules → lightweight ML → heavy ML → human), ensuring cost scales with uncertainty rather than volume
- [[Tool-Use-Pattern-Agent-calls-external-functions-search-calculator-run-code-send-]] — Tool Use Pattern: Agent calls external functions (search, calculator, run_code, send_email) to extend beyond LLM knowledge, executing structured tool calls in a loop until a final answer is ready
- [[TraceSpan-Architecture-every-agent-request-is-a-tree-of-named-spans-capturing-la]] — Trace/Span Architecture: every agent request is a tree of named spans capturing latency, token counts, and cost at each operation node
- [[TraceSpan-Observability-Instrumenting-each-pipeline-stage-as-named-spans-within-]] — Trace/Span Observability: Instrumenting each pipeline stage as named spans within a request trace to enable latency diagnosis, cost attribution, and failure localization
- [[Verification-First-Action-Architecture-every-autonomous-action-must-have-an-obje]] — Verification-First Action Architecture: every autonomous action must have an objective verification layer (tests, safety checks, compile checks) before human review is even requested
- [[WorkTask-Contract-a-typed-dataclass-defining-task-id-worker-type-query-shared-co]] — WorkTask Contract: a typed dataclass defining task_id, worker_type, query, shared context, and expected_output_schema, enforcing interface contracts between orchestrator and workers
- [[Write-Once-Audit-Trail-immutable-timestamped-log-of-every-interaction-including-]] — Write-Once Audit Trail: immutable, timestamped log of every interaction including claims, verifications, escalation reasons, and system version for regulatory compliance

## How to Use This Wiki

**For agents:** Load the thin skill file (`output/skills/`) first.
The skill's concept map tells you which page to read for a given situation.
Read the concept page when you need depth — not the whole wiki.

**For humans:** Browse in Obsidian. Start here, follow wikilinks.
Use the graph view to see which concepts are most connected.

## Related Wikis

<!-- Populated after all book wikis are built -->
