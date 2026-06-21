---
title: Parallel and Fan-Out Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
confidence: high
consolidated_from: 6 pages
---

# Parallel and Fan-Out Agents

> Consolidated from 6 related concept pages.

---

## Confidence Weighted Voting merge agent verdicts by scoring each as verdict weigh

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Fan OutFan In spawn N independent agents in parallel then merge their results wi

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Partial Results Doctrine accept and use incomplete results when some agents time

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Pattern Parallel Fan Out Agents

## Why Parallel Matters

You've got a problem that's embarrassingly parallelizable but needs synchronized results. A single sequential agent would be slow. Parallel agents execute independently, then merge their findings.

The pattern: **fan-out** (spawn agents in parallel) → **independent work** → **fan-in** (merge results with conflict resolution).

When to use:
- Problems decompose into independent subproblems
- Latency dominates—you need N things checked simultaneously
- Results must be reconciled (not just collected)
- Some agents failing shouldn't block others

---

## Case Study 1: Meta — Misinformation Detection at Scale

### Business Problem

Meta reviews 2B+ pieces of content daily across Facebook/Instagram. Human reviewers can't scale to that volume. They need to detect policy violations, misinformation, and harmful content *fast*.

Approach: spin up parallel fact-check, source credibility, policy violation, and context agents on each post. Each runs independently. Then **merge** their verdicts into a final decision.

Why parallel? Sequential checking would triple latency. Parallel hits all four checks simultaneously.

### Why This Pattern Fits

- Each agent (Fact-Check, Source Credibility, Policy, Context) is independent
- All four need to run on every piece of content
- Results must be merged with weighted confidence
- Timeout is acceptable; partial results inform the decision
- Cost scales with content volume; parallelism keeps per-item latency constant

### Architecture Diagram

```
Content Item
    |
    +--fan-out--> Fact-Check Agent
    |
    +--fan-out--> Source Credibility Agent
    |
    +--fan-out--> Policy Violation Agent
    |
    +--fan-out--> Context Agent
    |
    +--fan-in--> Merger (voting + confidence weighting)
    |
    +---> Decision: [Remove, Label, Pass]
    |
    +---> Audit Log
```

### Implementation: Confidence-Weighted Voting

Here's the core merge logic when agents disagree:

```python
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
import asyncio

class VerificationResult(Enum):
    REMOVE = "remove"
    LABEL = "label"
    PASS = "pass"

@dataclass
class AgentVerdictData:
    agent_name: str
    verdict: str  # "remove", "label", or "pass"
    confidence: float  # 0.0 to 1.0
    reasoning: str
    metadata: Dict[str, Any]

class ParallelMisinformationDetector:
    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout = timeout_seconds
        self.verdict_weights = {
            "remove": 3.0,      # Highest priority
            "label": 2.0,
            "pass": 1.0
        }
    
    async def fact_check_agent(self, content: str) -> AgentVerdictData:
        """
        Check content against known fact-check databases.
        Simulated delay represents calling external fact-check APIs.
        """
        await asyncio.sleep(0.8)  # Simulate API call
        
        # In reality: hit Snopes, PolitiFact, etc.
        is_misinformation = "false claim" in content.lower()
        
        return AgentVerdictData(
            agent_name="fact_check",
            verdict="remove" if is_misinformation else "pass",
            confidence=0.92 if is_misinformation else 0.88,
            reasoning="Matched against known misinformation dataset",
            metadata={"sources_checked": 47}
        )
    
    async def source_credibility_agent(self, content: str, source_url: str) -> AgentVerdictData:
        """
        Assess the credibility of the content source.
        """
        await asyncio.sleep(0.6)
        
        # In reality: graph analysis, editorial review history, etc.
        is_unreliable = "unreliable_domain" in source_url.lower()
        
        return AgentVerdictData(
            agent_name="source_credibility",
            verdict="label" if is_unreliable else "pass",
            confidence=0.85 if is_unreliable else 0.90,
            reasoning="Source domain reputation assessment",
            metadata={"domain_age_years": 3, "previous_violations": 2}
        )
    
    async def policy_violation_agent(self, content: str) -> AgentVerdictData:
        """
        Check if content violates platform policies.
        """
        await asyncio.sleep(0.7)
        
        # In reality: trained classifier over policy taxonomy
        violates_policy = "explicit hate speech" in content.lower()
        
        return AgentVerdictData(
            agent_name="policy_violation",
            verdict="remove" if violates_policy else "pass",
            confidence=0.95 if violates_policy else 0.92,
            reasoning="Policy violation classifier inference",
            metadata={"policy_category": "hate_speech", "model_version": "v2.3.1"}
        )
    
    async def context_agent(self, content: str, author_history: Dict) -> AgentVerdictData:
        """
        Assess content in context of author's history.
        """
        await asyncio.sleep(0.5)
        
        # In reality: author reputation score, history of violations
        author_risk = author_history.get("violation_count", 0) > 5
        
        return AgentVerdictData(
            agent_name="context",
            verdict="label" if author_risk else "pass",
            confidence=0.78 if author_risk else 0.81,
            reasoning="Author account risk assessment",
            metadata={"account_age_days": 180, "violation_count": author_history.get("violation_count", 0)}
        )
    
    async def parallel_check(
        self,
        content: str,
        source_url: str,
        author_history: Dict
    ) -> Dict[str, Any]:
        """
        Fan-out: spawn all agents in parallel.
        """
        try:
            verdicts = await asyncio.wait_for(
                asyncio.gather(
                    self.fact_check_agent(content),
                    self.source_credibility_agent(content, source_url),
                    self.policy_violation_agent(content),
                    self.context_agent(content, author_history),
                    return_exceptions=False
                ),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            # Partial failure—return what we have
            verdicts = await asyncio.gather(
                self.fact_check_agent(content),
                self.source_credibility_agent(content, source_url),
                self.policy_violation_agent(content),
                self.context_agent(content, author_history),
                return_exceptions=True
            )
            # Filter out exceptions, keep successful agents
            verdicts = [v for v in verdicts if not isinstance(v, Exception)]
        
        return self.merge_verdicts(verdicts, content)
    
    def merge_verdicts(self, verdicts: List[AgentVerdictData], content: str) -> Dict[str, Any]:
        """
        Fan-in: merge with confidence-weighted voting.
        
        Algorithm:
        1. Score each verdict by (verdict_weight * confidence)
        2. Aggregate across agents
        3. Select verdict with highest aggregate score
        4. Require 2+ agents agreeing on "remove" for automatic removal
        """
        if not verdicts:
            return {
                "final_decision": "pass",
                "confidence": 0.0,
                "reason": "No agents completed",
                "verdicts": []
            }
        
        # Calculate weighted scores
        verdict_scores = {}
        for v in verdicts:
            verdict_key = v.verdict
            weight = self.verdict_weights.get(verdict_key, 1.0)
            score = weight * v.confidence
            
            if verdict_key not in verdict_scores:
                verdict_scores[verdict_key] = {"score": 0.0, "count": 0, "agents": []}
            
            verdict_scores[verdict_key]["score"] += score
            verdict_scores[verdict_key]["count"] += 1
            verdict_scores[verdict_key]["agents"].append(v.agent_name)
        
        # Normalize by agent count for fair comparison
        for verdict_key in verdict_scores:
            verdict_scores[verdict_key]["score"] /= verdict_scores[verdict_key]["count"]
        
        # Safety rule: require 2+ agents for "remove"
        remove_votes = verdict_scores.get("remove", {}).get("count", 0)
        if remove_votes < 2:
            # Downgrade from "remove" to "label"
            if "remove" in verdict_scores:
                verdict_scores["remove"]["verdict_key"] = "label"
        
        # Pick the verdict with highest score
        best_verdict = max(
            verdict_scores.items(),
            key=lambda x: x[1]["score"]
        )
        
        final_decision = best_verdict[0]
        final_confidence = best_verdict[1]["score"]
        
        return {
            "final_decision": final_decision,
            "confidence": min(final_confidence, 1.0),
            "verdict_breakdown": {k: {
                "agents": v["agents"],
                "count": v["count"],
                "avg_confidence": v["score"]
            } for k, v in verdict_scores.items()},
            "individual_verdicts": [
                {
                    "agent": v.agent_name,
                    "verdict": v.verdict,
                    "confidence": v.confidence,
                    "reasoning": v.reasoning
                }
                for v in verdicts
            ],
            "audit_log": {
                "content_preview": content[:100],
                "total_agents": len(verdicts),
                "decision_timestamp": "2025-04-23T10:30:00Z"
            }
        }


# Example usage
async def main():
    detector = ParallelMisinformationDetector()
    
    content = "This is a false claim about vaccines"
    source = "https://unreliable_domain.com/article"
    author = {"violation_count": 0}
    
    result = await detector.parallel_check(content, source, author)
    
    print("=" * 60)
    print("CONTENT MODERATION DECISION")
    print("=" * 60)
    print(f"Decision: {result['final_decision'].upper()}")
    print(f"Confidence: {result['confidence']:.2%}")
    print()
    print("Agent Verdicts:")
    for verdict in result['individual_verdicts']:
        print(f"  {verdict['agent']:20} → {verdict['verdict']:10} ({verdict['confidence']:.0%})")
    print()
    print("Breakdown:")
    for verdict_type, data in result['verdict_breakdown'].items():
        print(f"  {verdict_type:10}: {data['count']} agents, avg confidence {data['avg_confidence']:.0%}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Key Design Decisions:**

1. **Timeout per agent, not global:** Each agent gets its timeout window. Slow agents don't block fast ones.

2. **Confidence weighting:** Agents with higher confidence influence the decision more. A 95% confident policy violation beats a 50% confident context concern.

3. **Safety threshold:** "Remove" decisions require agreement from 2+ agents. A single agent saying "remove" downgrades to "label" to reduce false positives.

4. **Partial results:** If some agents timeout, use what you have. 3 agent verdicts are better than 0.

5. **Verdict hierarchy:** Remove > Label > Pass. When in doubt, escalate to human review (label).

---

## Case Study 2: Amazon — Global Compliance Screening

### Business Problem

Amazon lists millions of products across 200+ countries. Each country has different regulations (EU GDPR, China data residency, India product bans, etc.). Screening every listing sequentially against 50+ regional compliance rules takes hours.

Parallel solution: fan-out to per-region compliance agents. Each agent checks regional regulations independently. Fan-in decides: block globally, block in region, approve everywhere, or flag for human review.

### Architecture Diagram

```
Product Listing
    |
    +--fan-out--> EU Compliance Agent (GDPR, CE Mark, RoHS)
    |
    +--fan-out--> China Compliance Agent (Data residency, CCC)
    |
    +--fan-out--> India Compliance Agent (Local sourcing, TDS)
    |
    +--fan-out--> Brazil Compliance Agent (LGPD, Local registration)
    |
    +--fan-out--> [+46 more regional agents in parallel]
    |
    +--fan-in--> ALL-MUST-PASS Merger
    |
    +---> Decision: [Global Block, Regional Block, Approve, Review Queue]
```

### Implementation: All-Must-Pass vs. Majority Voting

```python
from typing import List, Optional
from enum import Enum
import asyncio
from dataclasses import dataclass
from datetime import datetime

class ComplianceStatus(Enum):
    APPROVED = "approved"
    BLOCKED = "blocked"
    FLAGGED = "flagged"
    REGIONAL_BLOCK = "regional_block"

@dataclass
class RegionalComplianceCheck:
    region_code: str  # "US", "EU", "CN", "IN", "BR"
    region_name: str
    status: ComplianceStatus
    violations: List[str]
    blocked_regulations: List[str]  # e.g., ["GDPR Article 5", "RoHS Directive"]
    reasoning: str
    checked_timestamp: str

class GlobalComplianceScreener:
    """
    All-must-pass logic: if ANY region blocks, the listing is either
    blocked globally or blocked in that region only.
    """
    
    def __init__(self, timeout_per_region: float = 3.0):
        self.timeout = timeout_per_region
        self.regions = {
            "US": {"name": "United States", "regulations": ["CPSC", "FTC", "FDA"]},
            "EU": {"name": "European Union", "regulations": ["GDPR", "CE", "RoHS", "WEEE"]},
            "CN": {"name": "China", "regulations": ["CCCID", "CCP", "Data Residency"]},
            "IN": {"name": "India", "regulations": ["FSSAI", "BIS", "Local sourcing"]},
            "BR": {"name": "Brazil", "regulations": ["LGPD", "ANVISA", "ABNT"]},
            "AU": {"name": "Australia", "regulations": ["ACCC", "TGA"]},
            "JP": {"name": "Japan", "regulations": ["METI", "PSE"]},
        }
    
    async def check_region(
        self,
        region_code: str,
        product_data: Dict[str, Any]
    ) -> RegionalComplianceCheck:
        """
        Simulate checking product against regional regulations.
        In reality: call regional regulatory APIs, consult local databases.
        """
        await asyncio.sleep(0.5 + (hash(region_code) % 30) / 100)  # Variable latency
        
        violations = []
        
        # Simulate violations
        if region_code == "EU" and "restricted_material" in product_data.get("materials", []):
            violations.append("RoHS Directive: Contains restricted substance (Lead)")
        
        if region_code == "IN" and product_data.get("origin") == "Foreign":
            violations.append("Local sourcing requirement: Min 30% domestic content")
        
        if region_code == "CN" and not product_data.get("ccc_certified"):
            violations.append("CCC Certification required for this product class")
        
        if region_code == "BR" and product_data.get("has_personal_data") and not product_data.get("lgpd_compliant"):
            violations.append("LGPD: No valid data processing agreement")
        
        status = ComplianceStatus.BLOCKED if violations else ComplianceStatus.APPROVED
        
        return RegionalComplianceCheck(
            region_code=region_code,
            region_name=self.regions[region_code]["name"],
            status=status,
            violations=violations,
            blocked_regulations=[v.split(":")[0] for v in violations],
            reasoning=f"Checked {len(self.regions[region_code]['regulations'])} regulations" +
                     (f"; {len(violations)} violations found" if violations else "; All passed"),
            checked_timestamp=datetime.now().isoformat()
        )
    
    async def screen_globally(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fan-out to all regions in parallel.
        """
        tasks = [
            self.check_region(region_code, product_data)
            for region_code in self.regions.keys()
        ]
        
        try:
            results = await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=False),
                timeout=self.timeout
            )
        except asyncio.TimeoutError:
            # Timeout is a block—err on side of caution
            results = await asyncio.gather(*tasks, return_exceptions=True)
            results = [r for r in results if not isinstance(r, Exception)]
        
        return self.merge_regional_decisions(results, product_data)
    
    def merge_regional_decisions(
        self,
        regional_checks: List[RegionalComplianceCheck],
        product_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        All-must-pass logic:
        
        Rules:
        1. If all regions approve → APPROVED
        2. If any region blocks → FLAGGED (for manual review)
           - Unless block is regional-only (e.g., EU bans lead, but US allows)
           - Then flag as REGIONAL_BLOCK, allow sale elsewhere
        3. If timeout or missing regions → FLAGGED
        
        The key insight: some regulations are **global** (e.g., child safety)
        while others are **regional** (e.g., GDPR only applies in EU).
        """
        
        blocked_regions = []
        approved_regions = []
        global_blockers = []
        
        for check in regional_checks:
            if check.status == ComplianceStatus.BLOCKED:
                blocked_regions.append(check)
                # Check if this is a global regulation
                global_blocking_regs = [
                    r for r in check.blocked_regulations
                    if self.is_globally_blocking(r)
                ]
                if global_blocking_regs:
                    global_blockers.extend(global_blocking_regs)
            else:
                approved_regions.append(check)
        
        # Determine final decision
        if global_blockers:
            # Global regulation violation → block worldwide
            final_status = ComplianceStatus.BLOCKED
            reason = f"Global compliance violation: {', '.join(global_blockers)}"
        elif blocked_regions:
            # Regional violations only → flag as regional block
            final_status = ComplianceStatus.REGIONAL_BLOCK
            blocked_list = ", ".join([c.region_code for c in blocked_regions])
            reason = f"Regional compliance violations in: {blocked_list}. Approve with regional restrictions."
        else:
            # All regions approved
            final_status = ComplianceStatus.APPROVED
            reason = "All regional regulations satisfied"
        
        if len(regional_checks) < len(self.regions):
            # Missing regions—escalate to review
            final_status = ComplianceStatus.FLAGGED
            reason += f" [Warning: {len(self.regions) - len(regional_checks)} regions timed out]"
        
        return {
            "product_id": product_data.get("id"),
            "final_decision": final_status.value,
            "decision_reason": reason,
            "regions_checked": len(regional_checks),
            "regions_approved": len(approved_regions),
            "regions_blocked": len(blocked_regions),
            "regional_details": {
                "approved": [
                    {
                        "region": c.region_code,
                        "name": c.region_name,
                        "timestamp": c.checked_timestamp
                    }
                    for c in approved_regions
                ],
                "blocked": [
                    {
                        "region": c.region_code,
                        "name": c.region_name,
                        "violations": c.violations,
                        "timestamp": c.checked_timestamp
                    }
                    for c in blocked_regions
                ]
            },
            "requires_manual_review": final_status in [
                ComplianceStatus.FLAGGED,
                ComplianceStatus.REGIONAL_BLOCK
            ],
            "review_queue": "escalation" if final_status == ComplianceStatus.FLAGGED else
                           "regional_review" if final_status == ComplianceStatus.REGIONAL_BLOCK else None
        }
    
    def is_globally_blocking(self, regulation: str) -> bool:
        """
        Some regulations apply globally (e.g., child safety).
        Others are regional (e.g., GDPR only in EU).
        """
        global_regulations = {
            "CPSC",           # US child safety
            "Prop 65",        # California toxicity
            "REACH",          # EU chemical safety (affects global supply)
            "conflict minerals",  # UN Conflict Minerals Regulation
            "child safety",
        }
        
        return any(reg in regulation for reg in global_regulations)


async def main():
    screener = GlobalComplianceScreener()
    
    product = {
        "id": "B0A1X2Y3Z4",
        "name": "Smart Home Device",
        "origin": "China",
        "materials": ["lead", "copper"],
        "ccc_certified": False,
        "has_personal_data": True,
        "lgpd_compliant": False,
    }
    
    result = await screener.screen_globally(product)
    
    print("=" * 70)
    print("GLOBAL COMPLIANCE SCREENING RESULT")
    print("=" * 70)
    print(f"Product: {product['name']} ({product['id']})")
    print(f"Decision: {result['final_decision'].upper()}")
    print(f"Regions Checked: {result['regions_checked']} / 7")
    print(f"Regions Approved: {result['regions_approved']}")
    print(f"Regions Blocked: {result['regions_blocked']}")
    print()
    print(f"Reason: {result['decision_reason']}")
    print()
    if result['regions_blocked'] > 0:
        print("Blocked Regions:")
        for blocked in result['regional_details']['blocked']:
            print(f"  {blocked['region']}: {', '.join(blocked['violations'])}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **All-must-pass by default:** If any region blocks, flag for review. Assume regulations are stricter than needed.

2. **Global vs. regional regulations:** Some regulations (child safety, conflict minerals) apply globally. Others (GDPR, local sourcing) are regional. Use separate logic.

3. **Timeout = block:** If a regional agent times out, treat as blocked. Regulatory compliance is not "best effort."

4. **Regional blocks don't kill global approval:** If EU blocks due to RoHS but US approves, allow sale in US with flag in EU.

5. **Missing regions = escalate:** Don't approve until all regions are checked.

---

## Case Study 3: Bloomberg Media — Multimodal Video Archive Analysis

### Business Problem

Bloomberg has 13 petabytes of video archives (30+ years of reporting). They need to:
- Transcribe audio → searchable text
- Extract named entities (companies, people, places)
- Classify topics (tech, finance, politics)
- Analyze visuals (logos, charts, on-screen graphics)

Sequential: 4 agents × 13PB = years of compute. Parallel: process all four simultaneously on each video.

### Architecture Diagram

```
Video File (MP4, MXF, ProRes)
    |
    +--fan-out--> Transcription Agent
    |             (Speech-to-Text, speaker diarization)
    |
    +--fan-out--> Entity Extraction Agent
    |             (NER over transcript)
    |
    +--fan-out--> Topic Classification Agent
    |             (Multi-label genre, sector, geography)
    |
    +--fan-out--> Visual Analysis Agent
    |             (OCR, logo detection, scene classification)
    |
    +--fan-in--> Metadata Assembler
    |
    +---> Content Index + Storage
```

### Implementation: Multimodal Pipeline with Partial Results

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import json

class AgentStatus(Enum):
    SUCCESS = "success"
    TIMEOUT = "timeout"
    ERROR = "error"
    PARTIAL = "partial"

@dataclass
class TranscriptionResult:
    status: AgentStatus
    transcript: Optional[str]
    speaker_segments: List[Dict[str, Any]]  # [{"speaker": "A", "start": 0.0, "end": 5.2, "text": "..."}]
    confidence: float
    duration_seconds: float

@dataclass
class EntityResult:
    status: AgentStatus
    entities: List[Dict[str, Any]]  # [{"text": "Apple", "type": "ORG", "confidence": 0.95, "mentions": 3}]
    entity_count: int
    unique_entities: int

@dataclass
class TopicResult:
    status: AgentStatus
    topics: List[Dict[str, Any]]  # [{"label": "Technology", "confidence": 0.89}]
    primary_topic: Optional[str]
    geographies: List[str]
    sectors: List[str]

@dataclass
class VisualResult:
    status: AgentStatus
    ocr_text: Optional[str]
    logos_detected: List[Dict[str, Any]]  # [{"brand": "Apple", "confidence": 0.92, "frame_times": [1.2, 3.4]}]
    scene_descriptions: List[str]
    has_graphics: bool
    graphics_count: int

class VideoAnalyzer:
    def __init__(self, timeout_per_agent: float = 30.0):
        self.timeout = timeout_per_agent
    
    async def transcription_agent(self, video_path: str) -> TranscriptionResult:
        """
        Speech-to-text with speaker diarization.
        In reality: call Whisper, Rev, or Otter API.
        """
        await asyncio.sleep(2.5)  # Simulate processing
        
        transcript = """
        Host: Welcome to Bloomberg Markets. I'm reporting from New York.
        Our top story today concerns Apple's supply chain disruptions.
        """.strip()
        
        return TranscriptionResult(
            status=AgentStatus.SUCCESS,
            transcript=transcript,
            speaker_segments=[
                {"speaker": "A", "start": 0.0, "end": 2.1, "text": "Welcome to Bloomberg Markets."},
                {"speaker": "A", "start": 2.1, "end": 8.5, "text": "Our top story today concerns Apple's supply chain disruptions."}
            ],
            confidence=0.94,
            duration_seconds=120.0
        )
    
    async def entity_extraction_agent(self, video_path: str) -> EntityResult:
        """
        Named Entity Recognition over transcript.
        In reality: run spaCy, transformers, or LLM-based NER.
        """
        await asyncio.sleep(0.8)
        
        entities = [
            {"text": "Apple", "type": "ORG", "confidence": 0.99, "mentions": 5},
            {"text": "New York", "type": "LOC", "confidence": 0.98, "mentions": 2},
            {"text": "Bloomberg", "type": "ORG", "confidence": 0.99, "mentions": 3},
            {"text": "supply chain", "type": "CONCEPT", "confidence": 0.92, "mentions": 2},
        ]
        
        return EntityResult(
            status=AgentStatus.SUCCESS,
            entities=entities,
            entity_count=sum(e["mentions"] for e in entities),
            unique_entities=len(entities)
        )
    
    async def topic_classification_agent(self, video_path: str) -> TopicResult:
        """
        Multi-label topic classification.
        In reality: trained transformer classifier.
        """
        await asyncio.sleep(1.2)
        
        topics = [
            {"label": "Technology", "confidence": 0.94},
            {"label": "Supply Chain", "confidence": 0.87},
            {"label": "Business News", "confidence": 0.92},
        ]
        
        return TopicResult(
            status=AgentStatus.SUCCESS,
            topics=topics,
            primary_topic="Technology",
            geographies=["United States", "Global"],
            sectors=["Technology Hardware", "Logistics"]
        )
    
    async def visual_analysis_agent(self, video_path: str) -> VisualResult:
        """
        OCR, logo detection, scene analysis.
        In reality: call Google Vision, AWS Rekognition, or YOLOv8.
        """
        await asyncio.sleep(1.8)
        
        logos = [
            {"brand": "Apple", "confidence": 0.96, "frame_times": [1.2, 3.4, 5.6]},
            {"brand": "Bloomberg", "confidence": 0.99, "frame_times": [0.0]},
        ]
        
        return VisualResult(
            status=AgentStatus.SUCCESS,
            ocr_text="APPLE | SUPPLY CHAIN | Q1 2025",
            logos_detected=logos,
            scene_descriptions=["Studio setting", "News anchor at desk", "Supply chain diagram"],
            has_graphics=True,
            graphics_count=2
        )
    
    async def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Fan-out: spawn all four agents in parallel.
        Use asyncio.gather with return_exceptions=True to handle partial failures.
        """
        
        # Race all agents
        transcription_task = asyncio.create_task(
            self._with_timeout(self.transcription_agent(video_path), "transcription")
        )
        entity_task = asyncio.create_task(
            self._with_timeout(self.entity_extraction_agent(video_path), "entity")
        )
        topic_task = asyncio.create_task(
            self._with_timeout(self.topic_classification_agent(video_path), "topic")
        )
        visual_task = asyncio.create_task(
            self._with_timeout(self.visual_analysis_agent(video_path), "visual")
        )
        
        # Wait for all (with exceptions caught)
        results = await asyncio.gather(
            transcription_task,
            entity_task,
            topic_task,
            visual_task,
            return_exceptions=True
        )
        
        return self.assemble_metadata(results, video_path)
    
    async def _with_timeout(self, coro, agent_name: str):
        """
        Timeout wrapper that sets status to TIMEOUT if it takes too long.
        """
        try:
            return await asyncio.wait_for(coro, timeout=self.timeout)
        except asyncio.TimeoutError:
            # Return partial result with timeout status
            if agent_name == "transcription":
                return TranscriptionResult(
                    status=AgentStatus.TIMEOUT,
                    transcript=None,
                    speaker_segments=[],
                    confidence=0.0,
                    duration_seconds=0.0
                )
            elif agent_name == "entity":
                return EntityResult(
                    status=AgentStatus.TIMEOUT,
                    entities=[],
                    entity_count=0,
                    unique_entities=0
                )
            elif agent_name == "topic":
                return TopicResult(
                    status=AgentStatus.TIMEOUT,
                    topics=[],
                    primary_topic=None,
                    geographies=[],
                    sectors=[]
                )
            elif agent_name == "visual":
                return VisualResult(
                    status=AgentStatus.TIMEOUT,
                    ocr_text=None,
                    logos_detected=[],
                    scene_descriptions=[],
                    has_graphics=False,
                    graphics_count=0
                )
    
    def assemble_metadata(
        self,
        results: List[Any],
        video_path: str
    ) -> Dict[str, Any]:
        """
        Fan-in: merge results into a single metadata document.
        Partial results are acceptable; flag which agents succeeded/failed.
        """
        
        transcription_result = results[0]
        entity_result = results[1]
        topic_result = results[2]
        visual_result = results[3]
        
        # Calculate overall success
        agent_statuses = {
            "transcription": transcription_result.status.value,
            "entity_extraction": entity_result.status.value,
            "topic_classification": topic_result.status.value,
            "visual_analysis": visual_result.status.value,
        }
        
        success_count = sum(1 for s in agent_statuses.values() if s == "success")
        completion_rate = success_count / 4
        
        # Build searchable metadata
        searchable_text = ""
        if transcription_result.status == AgentStatus.SUCCESS:
            searchable_text += transcription_result.transcript + " "
        if visual_result.status == AgentStatus.SUCCESS:
            searchable_text += (visual_result.ocr_text or "") + " "
        
        entity_mentions = {}
        if entity_result.status == AgentStatus.SUCCESS:
            for entity in entity_result.entities:
                entity_mentions[entity["text"]] = {
                    "type": entity["type"],
                    "mentions": entity["mentions"],
                    "confidence": entity["confidence"]
                }
        
        # Combine topics and geographies
        all_topics = []
        if topic_result.status == AgentStatus.SUCCESS:
            all_topics = [t["label"] for t in topic_result.topics]
        
        return {
            "video_path": video_path,
            "processing_status": "success" if completion_rate == 1.0 else "partial",
            "completion_rate": completion_rate,
            "agent_statuses": agent_statuses,
            
            # Indexable content
            "searchable_text": searchable_text.strip()[:5000],  # Truncate for storage
            "transcript": transcription_result.transcript if transcription_result.status == AgentStatus.SUCCESS else None,
            "speaker_segments": transcription_result.speaker_segments if transcription_result.status == AgentStatus.SUCCESS else [],
            
            # Entities
            "entities": entity_mentions,
            "entity_count": entity_result.entity_count if entity_result.status == AgentStatus.SUCCESS else 0,
            
            # Topics
            "topics": all_topics,
            "primary_topic": topic_result.primary_topic if topic_result.status == AgentStatus.SUCCESS else None,
            "geographies": topic_result.geographies if topic_result.status == AgentStatus.SUCCESS else [],
            "sectors": topic_result.sectors if topic_result.status == AgentStatus.SUCCESS else [],
            
            # Visual content
            "ocr_text": visual_result.ocr_text if visual_result.status == AgentStatus.SUCCESS else None,
            "logos": visual_result.logos_detected if visual_result.status == AgentStatus.SUCCESS else [],
            "scene_descriptions": visual_result.scene_descriptions if visual_result.status == AgentStatus.SUCCESS else [],
            
            # Metadata
            "indexed_at": "2025-04-23T10:30:00Z",
            "version": 1,
            "agents_available_for_reprocessing": [
                agent for agent, status in agent_statuses.items()
                if status in ["timeout", "error"]
            ]
        }


async def main():
    analyzer = VideoAnalyzer()
    result = await analyzer.analyze_video("/media/video_archive/20250101_bloomberg_markets.mp4")
    
    print("=" * 70)
    print("VIDEO METADATA ASSEMBLY")
    print("=" * 70)
    print(f"Video: {result['video_path']}")
    print(f"Processing Status: {result['processing_status']}")
    print(f"Agent Completion: {result['completion_rate']:.0%}")
    print()
    print("Agent Status Breakdown:")
    for agent, status in result['agent_statuses'].items():
        print(f"  {agent:25} → {status}")
    print()
    print(f"Primary Topic: {result['primary_topic']}")
    print(f"Topics: {', '.join(result['topics'])}")
    print(f"Geographies: {', '.join(result['geographies'])}")
    print()
    print(f"Entities ({result['entity_count']} mentions):")
    for entity_text, entity_data in list(result['entities'].items())[:5]:
        print(f"  {entity_text:20} ({entity_data['type']:10}) × {entity_data['mentions']}")
    print()
    if result['logos']:
        print("Logos Detected:")
        for logo in result['logos']:
            print(f"  {logo['brand']:20} (confidence: {logo['confidence']:.0%})")

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Timeout per agent, not per video:** If transcription takes 30s but entity extraction finishes in 2s, don't block. Return what's done.

2. **Partial results are valuable:** 3 agents' output is better than 0. Flag which agents timed out for manual reprocessing.

3. **Searchable text aggregation:** Combine transcript + OCR for full-text search. If one agent fails, search still works on the other's output.

4. **Reprocessing queue:** Track which agents failed. Retry just those agents on the next pass.

5. **Status propagation:** Mark videos as "partial" if not all agents completed. Don't claim full indexing when it's incomplete.

---

## Key Takeaways

1. **Parallelism beats sequential when:** Independent subproblems exist, latency dominates, and reconciliation is tractable.

2. **Merge strategies matter:** Voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

3. **Timeout handling is crucial:** Per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

4. **Partial results are fine:** Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

5. **Cost scales linearly:** N agents in parallel costs roughly N × cost of one agent (vs N² for sequential). 13PB of video becomes tractable.

6. **Consistency challenges emerge:** When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

---

## Further Reading

- **asyncio documentation:** https://docs.python.org/3/library/asyncio.html
- **Ray (distributed computing):** https://ray.io/ — scales parallel patterns to clusters
- **Temporal workflows:** https://temporal.io/ — production-grade task orchestration
- **OWASP Parallel Patterns:** Security considerations for concurrent agents

---

## Per Agent Timeout apply timeouts individually to each parallel agent so fast age

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Safety Threshold Rule require agreement from 2 agents before taking the highest

## Core Principle

The Fan-Out/Fan-In pattern spawns N independent specialist agents in parallel and merges their results using confidence-weighted voting, safety thresholds, and explicit conflict resolution to produce a single decision faster than any sequential approach. Robust implementations require per-agent (not global) timeouts, graceful handling of partial results, and full audit logging of individual verdicts. The merge strategy—not the agents themselves—is where correctness lives.

## Key Heuristics

These are the load-bearing rules for this concept.

> Parallelism beats sequential when: independent subproblems exist, latency dominates, and reconciliation is tractable.

> Better 75% of truth than 100% latency. Flag what's missing for reprocessing.

> Merge strategies matter: voting, confidence weighting, safety thresholds, and all-must-pass rules are equally important as the agents themselves.

> Timeout handling is crucial: per-agent timeouts (not global) let fast agents finish while waiting reasonably for slow ones.

> When agents disagree, you need explicit rules. Don't hide conflicts; expose them in audit logs.

> Cost scales linearly: N agents in parallel costs roughly N × cost of one agent (vs N² for sequential).

> A single agent saying 'remove' downgrades to 'label' to reduce false positives.

> Track which agents failed. Retry just those agents on the next pass.

## Anti-Patterns & Fixes

- Global Timeout Blocking: applying a single timeout to the entire gather call, causing fast agents' results to be discarded when one slow agent exceeds the limit. Fix: use per-agent timeouts with return_exceptions=True and filter out exceptions to preserve successful results.
- Sequential Checking: running independent checks one after another, tripling or worse latency unnecessarily. Fix: use asyncio.gather() or equivalent to spawn all independent agents simultaneously.
- All-or-Nothing Merge: refusing to emit a decision unless all agents complete, causing full pipeline stalls on partial failures. Fix: design merge_verdicts to handle any subset of agents and mark output as 'partial' with a reprocessing queue.
- Hidden Conflict: silently resolving agent disagreements without recording which agents said what. Fix: emit full verdict_breakdown and individual_verdicts in the audit log so conflicts are traceable.
- Single-Agent High-Severity Action: allowing one agent's 'remove' verdict to trigger removal without corroboration, causing high false-positive rates. Fix: enforce a minimum agent-agreement threshold (e.g., 2+) before acting on the highest-severity verdict.
- Uniform Confidence Weighting: treating a 95%-confident policy violation the same as a 50%-confident context concern. Fix: multiply verdict weight by confidence score before aggregating to let high-confidence signals dominate.

## When To Apply

Load this page when:

- Use this when a task decomposes into N independent subtasks that can run simultaneously and latency is the primary constraint.
- Use this when multiple specialized checkers (fact-check, policy, credibility, context) must all evaluate the same input and their verdicts must be reconciled into one decision.
- Use this when some agents may timeout or fail and the system must still produce a useful (possibly partial) output rather than erroring out.
- Use this when different agents may disagree and you need an explicit, auditable conflict-resolution mechanism rather than ad-hoc logic.
- Use this when processing high-volume items (millions of products, billions of content pieces) where per-item sequential latency is unacceptable.
- Use this when indexing or enriching multi-modal content (video, audio, text, images) where each modality requires a different processing pipeline that can run independently.
- Use this when regulatory or safety requirements demand that multiple independent checks corroborate before a high-severity action (removal, ban, block) is taken.

## Concrete Examples

- Meta content moderation: four parallel agents (Fact-Check, Source Credibility, Policy Violation, Context) evaluate each post simultaneously; a confidence-weighted voter merges verdicts into Remove/Label/Pass with a 2-agent minimum for removal.
- Amazon global compliance screening: per-region compliance agents run in parallel against a product listing, each checking country-specific regulations (EU GDPR, China data residency, India product bans), fanning in to a unified compliance decision.
- Bloomberg video archive indexing: four parallel agents (transcription, entity extraction, topic classification, visual analysis) process each video file simultaneously; results are merged into a searchable metadata record with partial-success handling and a reprocessing queue for failed agents.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Pattern: Parallel Fan-Out Agents**

An LLM coding agent generating fan-out code is particularly prone to accidentally serializing the parallel calls (e.g., awaiting each coroutine individually before gathering) or applying a single global timeout that silently discards all results on any slow agent—bugs that are non-obvious in generated code and only surface under load. The agent must also be explicitly prompted to implement merge logic with conflict resolution and audit logging, because LLM-generated stubs tend to stop at the gather() call and return raw results without reconciliation, leaving the hardest part of the pattern unimplemented.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
