---
title: Evaluation Frameworks
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept]
confidence: high
consolidated_from: 6 pages
---

# Evaluation Frameworks

> Consolidated from 6 related concept pages.

---

## Continuous Eval Loop Scheduling evaluation to run on recent production data on a

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Evaluation Frameworks

You're about to deploy an agent to production handling real user requests. Before you do, you need to answer a fundamental question: does it actually work? Not in your notebook—at scale, with real data, under realistic conditions.

This chapter is about building evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping. Think of it like continuous integration for agent behavior.

## The Evaluation Architecture

Your agent is a system. Your evaluation is a parallel system. They should look similar:

```
┌─────────────────────────────────────────────────────────┐
│                    AGENT SYSTEM                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Input      │→ │   Agent      │→ │   Output     │  │
│  │ Processing   │  │  Reasoning   │  │  Formatting  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   EVALUATION SYSTEM                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Golden     │→ │   Judge      │→ │   Metrics    │  │
│  │   Dataset    │  │   Inference  │  │   & Reports  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

The eval system runs on historical data (golden dataset), generates judgments (LLM-as-judge, human review, or deterministic rules), and produces metrics. These metrics feed back to inform deployment decisions.

### Why This Structure Matters

- **Isolation**: Eval doesn't interfere with production traffic
- **Reproducibility**: Run the same eval multiple times, get the same results
- **Scale**: Test against thousands of examples in parallel
- **Slice analysis**: Understand where your agent struggles
- **Automation**: Run before every deployment, not manually

## Golden Datasets: The Foundation

A golden dataset is your source of truth. It's curated examples with expected outputs. Think of it as test vectors for your agent.

```python
# schemas/golden_dataset.py
from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass, asdict
import json

@dataclass
class GoldenExample:
    """A single evaluation example with metadata."""
    id: str
    user_query: str
    expected_output: str
    tools_required: List[str]
    difficulty: str  # "easy", "medium", "hard"
    category: str    # "customer_support", "sales_inquiry", "complaint", etc.
    created_at: datetime
    version: int = 1
    is_stale: bool = False  # Mark examples that no longer reflect production
    human_reviewer_id: Optional[str] = None
    notes: str = ""
    
    def to_json(self) -> str:
        data = asdict(self)
        data['created_at'] = data['created_at'].isoformat()
        return json.dumps(data)

class GoldenDatasetManager:
    """Lifecycle management for golden datasets."""
    
    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.examples: dict[str, GoldenExample] = {}
    
    def add_example(self, example: GoldenExample) -> None:
        """Add a curated example to the dataset."""
        self.examples[example.id] = example
    
    def mark_stale(self, example_id: str, reason: str) -> None:
        """Mark an example as no longer representative of production."""
        if example_id in self.examples:
            self.examples[example_id].is_stale = True
            self.examples[example_id].notes = reason
    
    def get_active_examples(self, category: Optional[str] = None) -> List[GoldenExample]:
        """Retrieve examples that are still representative."""
        examples = [e for e in self.examples.values() if not e.is_stale]
        if category:
            examples = [e for e in examples if e.category == category]
        return examples
    
    def detect_staleness(self, drift_threshold: float = 0.15) -> List[str]:
        """
        Identify examples that may no longer be representative.
        Track how often current agent fails on them.
        """
        stale_ids = []
        for ex_id, example in self.examples.items():
            # Example strategy: if failure rate on this example exceeds
            # historical baseline by drift_threshold, mark as stale
            failure_rate = self._get_recent_failure_rate(ex_id)
            historical_rate = self._get_historical_failure_rate(ex_id)
            
            if failure_rate > historical_rate * (1 + drift_threshold):
                stale_ids.append(ex_id)
        
        return stale_ids
    
    def _get_recent_failure_rate(self, example_id: str) -> float:
        """Calculate failure rate over last 7 days."""
        # Query telemetry: how often did this query type fail recently?
        pass
    
    def _get_historical_failure_rate(self, example_id: str) -> float:
        """Calculate historical baseline failure rate."""
        pass
    
    def version_bump(self, example_id: str) -> None:
        """Increment version when expected output changes."""
        if example_id in self.examples:
            self.examples[example_id].version += 1

# Usage
manager = GoldenDatasetManager("/data/golden_datasets")
manager.add_example(GoldenExample(
    id="query_001",
    user_query="What's the status of my order #12345?",
    expected_output="Your order #12345 shipped on 2026-04-20. Tracking: ...",
    tools_required=["order_lookup", "shipping_status"],
    difficulty="easy",
    category="customer_support",
    created_at=datetime.now(),
    human_reviewer_id="alice@company.com"
))

# Detect which examples may be outdated
stale = manager.detect_staleness(drift_threshold=0.15)
for stale_id in stale:
    manager.mark_stale(stale_id, "Failure rate increased 15% above baseline")
```

**Key design decision**: Keep golden datasets small but representative. 100-500 examples is typical for most production agents. Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

## LLM-as-Judge: The Judge Prompt

The cleanest way to evaluate agent outputs at scale is to use another LLM as a judge. The catch: the judge itself introduces variability. You need to manage this.

```python
# eval/judge.py
import anthropic
from typing import NamedTuple
from enum import Enum

class JudgeDecision(NamedTuple):
    score: float  # 0.0 to 1.0
    reasoning: str
    passes: bool

class JudgeCriteria(Enum):
    FAITHFULNESS = "faithfulness"
    GROUNDEDNESS = "groundedness"
    COMPLETENESS = "completeness"
    SAFETY = "safety"

class LLMJudge:
    """
    Judge agent outputs against golden examples.
    Each criteria has a calibrated prompt.
    """
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.client = anthropic.Anthropic()
        self.model = model
    
    def judge_faithfulness(
        self,
        agent_output: str,
        knowledge_source: str,
        reference_answer: str
    ) -> JudgeDecision:
        """
        Does the agent output match what the knowledge source says?
        High faithfulness = agent doesn't hallucinate.
        """
        prompt = f"""You are evaluating whether an AI agent's response is faithful to its knowledge source.

KNOWLEDGE SOURCE:
{knowledge_source}

REFERENCE ANSWER (what a human expert would say):
{reference_answer}

AGENT'S OUTPUT:
{agent_output}

Evaluate on this scale:
- 1.0: Output is factually accurate and drawn entirely from the knowledge source
- 0.75: Output is mostly accurate but adds minor interpretation
- 0.5: Output mixes source material with unsourced claims (risky)
- 0.25: Output is mostly speculation not grounded in the source
- 0.0: Output is false or contradicts the source

Respond in JSON:
{{
  "score": <0.0-1.0>,
  "reasoning": "Why this score?"
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        result = json.loads(response.content[0].text)
        score = result["score"]
        reasoning = result["reasoning"]
        
        return JudgeDecision(
            score=score,
            reasoning=reasoning,
            passes=score >= 0.75
        )
    
    def judge_groundedness(
        self,
        agent_output: str,
        context_provided: str
    ) -> JudgeDecision:
        """
        Are all claims in the output traceable to the provided context?
        This catches hallucinations.
        """
        prompt = f"""You are evaluating whether an AI agent's response is grounded in the context provided.

CONTEXT PROVIDED TO AGENT:
{context_provided}

AGENT'S OUTPUT:
{agent_output}

For each claim in the agent's output:
1. Can it be traced to the provided context?
2. Is it a reasonable inference from the context?
3. Is it speculation or hallucination?

Score:
- 1.0: Every claim is directly supported or reasonably inferred
- 0.75: Most claims supported, minor unsourced details
- 0.5: Mixed sourced and unsourced claims
- 0.25: Mostly unsourced claims
- 0.0: Entirely fabricated

Respond in JSON:
{{
  "score": <0.0-1.0>,
  "unsupported_claims": ["claim1", "claim2"],
  "reasoning": "Why this score?"
}}
"""
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}]
        )
        
        import json
        result = json.loads(response.content[0].text)
        
        return JudgeDecision(
            score=result["score"],
            reasoning=result["reasoning"],
            passes=result["score"] >= 0.75
        )
    
    def calibrate_judge(self, calibration_set: List[dict]) -> float:
        """
        Run judge on a set of examples where human ground truth is known.
        Return agreement rate with human reviewers.
        
        This tells you: how much do we trust this judge?
        """
        agreements = 0
        total = 0
        
        for example in calibration_set:
            agent_output = example["agent_output"]
            human_judgment = example["human_judgment"]  # True/False
            knowledge_source = example["knowledge_source"]
            
            decision = self.judge_faithfulness(
                agent_output,
                knowledge_source,
                example["reference_answer"]
            )
            
            judge_passes = decision.passes
            total += 1
            
            if judge_passes == human_judgment:
                agreements += 1
        
        agreement_rate = agreements / total if total > 0 else 0
        return agreement_rate

# Usage
judge = LLMJudge()

# Calibrate on known examples
calibration = [
    {
        "agent_output": "The order shipped on 2026-04-20",
        "human_judgment": True,
        "knowledge_source": "Order #123 shipped 2026-04-20 via FedEx",
        "reference_answer": "Order shipped on April 20"
    }
]

agreement = judge.calibrate_judge(calibration)
print(f"Judge agreement with humans: {agreement * 100:.1f}%")

# Now run judge on actual eval
decision = judge.judge_groundedness(
    agent_output="The customer's billing address is in California",
    context_provided="Customer account: John Doe, 123 Oak St, San Francisco, CA"
)
print(f"Groundedness score: {decision.score}")
print(f"Passes: {decision.passes}")
```

**Why multiple judges**: Different judges may disagree on the same output. That's not a bug—it's a feature. When judge disagreements happen, escalate to human review. Track which examples cause judge disagreement (these are the hard ones).

## Slice-Level Evaluation

Not all user queries are equal. Your agent may perform brilliantly on easy queries but fail on hard ones. Slice evaluation breaks down metrics by meaningful dimensions.

```python
# eval/slicing.py
from dataclasses import dataclass
from typing import Callable, Dict, List
import numpy as np

@dataclass
class EvalSlice:
    name: str
    filter_fn: Callable[[dict], bool]  # Which examples belong in this slice?
    min_size: int = 5  # Don't report on slices < N examples

class SliceEvaluator:
    """
    Evaluate agent performance broken down by meaningful slices.
    Answers: "Does the agent perform equally across demographics?"
    """
    
    def __init__(self, slices: List[EvalSlice]):
        self.slices = slices
    
    def evaluate_slices(
        self,
        examples: List[dict],
        eval_results: Dict[str, dict]
    ) -> Dict[str, dict]:
        """
        Run eval on each slice independently.
        Returns metrics per slice.
        """
        slice_results = {}
        
        for slice_def in self.slices:
            # Filter examples for this slice
            slice_examples = [e for e in examples if slice_def.filter_fn(e)]
            
            if len(slice_examples) < slice_def.min_size:
                continue
            
            # Collect eval results for this slice
            slice_scores = []
            for example in slice_examples:
                example_id = example["id"]
                if example_id in eval_results:
                    score = eval_results[example_id].get("score", 0)
                    slice_scores.append(score)
            
            # Compute metrics for this slice
            if slice_scores:
                slice_results[slice_def.name] = {
                    "count": len(slice_examples),
                    "mean_score": np.mean(slice_scores),
                    "min_score": np.min(slice_scores),
                    "max_score": np.max(slice_scores),
                    "stddev": np.std(slice_scores),
                    "pass_rate": sum(1 for s in slice_scores if s >= 0.75) / len(slice_scores)
                }
        
        return slice_results

# Define slices for a customer support agent
slices = [
    EvalSlice(
        name="easy_queries",
        filter_fn=lambda ex: ex["difficulty"] == "easy"
    ),
    EvalSlice(
        name="hard_queries",
        filter_fn=lambda ex: ex["difficulty"] == "hard"
    ),
    EvalSlice(
        name="billing_issues",
        filter_fn=lambda ex: "billing" in ex["category"].lower()
    ),
    EvalSlice(
        name="technical_issues",
        filter_fn=lambda ex: "technical" in ex["category"].lower()
    ),
    # Demographic slices (if tracking user properties)
    EvalSlice(
        name="new_customers",
        filter_fn=lambda ex: ex.get("customer_tenure_days", 999) < 30
    ),
    EvalSlice(
        name="vip_customers",
        filter_fn=lambda ex: ex.get("customer_tier") == "vip"
    )
]

evaluator = SliceEvaluator(slices)

# After running eval on all examples:
slice_metrics = evaluator.evaluate_slices(golden_examples, eval_results)

# Print results
for slice_name, metrics in slice_metrics.items():
    print(f"\n{slice_name}:")
    print(f"  Examples: {metrics['count']}")
    print(f"  Mean score: {metrics['mean_score']:.2f}")
    print(f"  Pass rate: {metrics['pass_rate']:.1%}")
    print(f"  Score range: [{metrics['min_score']:.2f}, {metrics['max_score']:.2f}]")

# Alert if any slice performs significantly worse than others
avg_score = np.mean([m["mean_score"] for m in slice_metrics.values()])
for slice_name, metrics in slice_metrics.items():
    if metrics["mean_score"] < avg_score * 0.85:
        print(f"WARNING: {slice_name} performing 15% below average")
```

**Why this matters**: A 90% overall pass rate hides a lot of pain. If your agent passes 100% on easy queries but only 60% on hard ones, you need to know that. Slices surface these imbalances.

## Regression Testing: Old vs. New

Every time you deploy a new agent version, you're making a bet. The new version should be better or at least not worse. Regression testing validates this.

```python
# eval/regression.py
from typing import NamedTuple
from datetime import datetime

class RegressionReport(NamedTuple):
    baseline_version: str
    candidate_version: str
    baseline_score: float
    candidate_score: float
    score_delta: float
    regressions: int  # Examples that got worse
    improvements: int  # Examples that got better
    wins_needed: int  # How many examples does new version need to win to beat baseline?

class RegressionTester:
    """
    Compare old agent version against new version.
    Detect capability regressions before deployment.
    """
    
    def __init__(self, baseline_version: str, candidate_version: str):
        self.baseline_version = baseline_version
        self.candidate_version = candidate_version
    
    def compare(
        self,
        baseline_results: Dict[str, float],  # {example_id: score}
        candidate_results: Dict[str, float]
    ) -> RegressionReport:
        """
        Compare two agents on the same evaluation set.
        Report differences.
        """
        all_examples = set(baseline_results.keys()) & set(candidate_results.keys())
        
        regressions = 0
        improvements = 0
        score_deltas = []
        
        for example_id in all_examples:
            baseline_score = baseline_results[example_id]
            candidate_score = candidate_results[example_id]
            delta = candidate_score - baseline_score
            
            score_deltas.append(delta)
            
            if delta < -0.1:  # Regression threshold: 10% drop
                regressions += 1
            elif delta > 0.1:  # Improvement threshold
                improvements += 1
        
        baseline_mean = np.mean(list(baseline_results.values()))
        candidate_mean = np.mean(list(candidate_results.values()))
        
        # How many examples need to improve to compensate for regressions?
        wins_needed = max(0, regressions - improvements)
        
        return RegressionReport(
            baseline_version=self.baseline_version,
            candidate_version=self.candidate_version,
            baseline_score=baseline_mean,
            candidate_score=candidate_mean,
            score_delta=candidate_mean - baseline_mean,
            regressions=regressions,
            improvements=improvements,
            wins_needed=wins_needed
        )
    
    def should_deploy(self, report: RegressionReport, threshold: float = -0.02) -> bool:
        """
        Decision logic: should we deploy the new version?
        
        Args:
            report: Regression test report
            threshold: Allow deployment if score delta >= threshold (-2% by default)
        
        Returns:
            True if safe to deploy
        """
        # Hard veto: if we have catastrophic regressions
        if report.regressions > len(report.baseline_version) * 0.05:
            return False
        
        # Allow deployment if score improved or barely declined
        if report.score_delta >= threshold:
            return True
        
        # If we're declining but have more improvements than regressions, OK
        if report.improvements > report.regressions:
            return True
        
        return False

# Usage in CI/CD pipeline
tester = RegressionTester(
    baseline_version="v1.2.4",
    candidate_version="v1.2.5"
)

report = tester.compare(baseline_results, candidate_results)

print(f"Baseline: {report.baseline_score:.3f}")
print(f"Candidate: {report.candidate_score:.3f}")
print(f"Delta: {report.score_delta:+.3f}")
print(f"Regressions: {report.regressions} | Improvements: {report.improvements}")

if not tester.should_deploy(report):
    print("DEPLOY BLOCKED: Too many regressions")
    exit(1)
else:
    print("REGRESSION TEST PASSED: Safe to deploy")
```

## Continuous Evaluation in Production

Offline evaluation is important but incomplete. Production is messy. Real users ask edge case queries. Real data distributions shift. You need to continuously evaluate live traffic.

```python
# prod/continuous_eval.py
import random
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ProductionEvaluator:
    """
    Sample live production requests, run evals on them.
    This is your early warning system for drift.
    """
    
    def __init__(self, sample_rate: float = 0.01):
        """
        Args:
            sample_rate: Fraction of production requests to evaluate
                        1% is typical. Higher = more accurate but more cost.
        """
        self.sample_rate = sample_rate
    
    def should_evaluate_request(self, request_id: str) -> bool:
        """
        Deterministic sampling: same request ID always maps to same decision.
        This avoids "lucky" batches where we only eval the easy cases.
        """
        return hash(request_id) % 100 < (self.sample_rate * 100)
    
    def evaluate_request(
        self,
        request_id: str,
        user_query: str,
        agent_output: str,
        tools_called: List[str],
        latency_ms: float,
        judge: LLMJudge
    ) -> Optional[dict]:
        """
        Run full eval on a production request.
        This is async—don't block user response.
        """
        if not self.should_evaluate_request(request_id):
            return None
        
        try:
            # Async eval—queue this for background processing
            eval_job = {
                "request_id": request_id,
                "user_query": user_query,
                "agent_output": agent_output,
                "tools_called": tools_called,
                "latency_ms": latency_ms,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "pending"
            }
            
            # Queue for async processing (e.g., Celery, SQS)
            self._queue_eval_job(eval_job)
            
            return eval_job
        
        except Exception as e:
            logger.error(f"Eval job failed for request {request_id}: {e}")
            return None
    
    def _queue_eval_job(self, job: dict) -> None:
        """Send to background job queue."""
        # In real code: celery.send_task("eval.run_eval", args=[job])
        pass
    
    def detect_regression_in_production(self, window_hours: int = 24) -> Optional[str]:
        """
        Compare eval metrics from past 24 hours vs. baseline.
        Alert if we've drifted.
        """
        recent_evals = self._fetch_evals_in_window(window_hours)
        baseline_metrics = self._fetch_baseline_metrics()
        
        if not recent_evals:
            return None
        
        recent_score = np.mean([e["score"] for e in recent_evals if "score" in e])
        baseline_score = baseline_metrics["mean_score"]
        
        # Threshold: 5% drop triggers alert
        if recent_score < baseline_score * 0.95:
            return (
                f"Production regression detected. "
                f"Baseline: {baseline_score:.3f}, Recent: {recent_score:.3f}"
            )
        
        return None
    
    def _fetch_evals_in_window(self, hours: int) -> List[dict]:
        """Query eval results from last N hours."""
        pass
    
    def _fetch_baseline_metrics(self) -> dict:
        """Get historical baseline metrics."""
        pass

# Usage in agent handler
def handle_user_request(user_query: str):
    request_id = generate_request_id()
    
    # Run agent
    agent_output = agent.run(user_query)
    
    # If sampled, queue eval (doesn't block response)
    evaluator.evaluate_request(
        request_id,
        user_query,
        agent_output,
        tools_called=agent.tools_called,
        latency_ms=agent.latency_ms,
        judge=judge
    )
    
    return agent_output

# Check for regressions every hour
def regression_monitor():
    while True:
        alert = evaluator.detect_regression_in_production(window_hours=24)
        if alert:
            logger.warning(alert)
            # Send to monitoring system (Datadog, PagerDuty, etc.)
        
        time.sleep(3600)
```

## Core Eval Metrics

What numbers should you be tracking?

```python
# metrics/definitions.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class EvalMetric:
    name: str
    description: str
    ideal_direction: str  # "up" or "down"
    alert_threshold: float
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "ideal_direction": self.ideal_direction
        }

# Standard metrics for most agents
STANDARD_METRICS = {
    "task_success_rate": EvalMetric(
        name="task_success_rate",
        description="Fraction of queries where agent achieved user goal",
        ideal_direction="up",
        alert_threshold=0.85
    ),
    "faithfulness": EvalMetric(
        name="faithfulness",
        description="Agent output matches knowledge sources (no hallucinations)",
        ideal_direction="up",
        alert_threshold=0.80
    ),
    "groundedness": EvalMetric(
        name="groundedness",
        description="All claims traceable to provided context",
        ideal_direction="up",
        alert_threshold=0.80
    ),
    "latency_p50": EvalMetric(
        name="latency_p50",
        description="Median response time (ms)",
        ideal_direction="down",
        alert_threshold=5000
    ),
    "latency_p99": EvalMetric(
        name="latency_p99",
        description="99th percentile response time (ms)",
        ideal_direction="down",
        alert_threshold=15000
    ),
    "cost_per_query": EvalMetric(
        name="cost_per_query",
        description="Average LLM token cost per query",
        ideal_direction="down",
        alert_threshold=0.10  # $0.10 per query
    ),
    "tokens_per_query": EvalMetric(
        name="tokens_per_query",
        description="Average input+output tokens consumed",
        ideal_direction="down",
        alert_threshold=8000
    ),
    "tool_call_accuracy": EvalMetric(
        name="tool_call_accuracy",
        description="Agent called correct tools (no spurious calls)",
        ideal_direction="up",
        alert_threshold=0.90
    )
}

# Compute all metrics from eval results
def compute_metrics(eval_results: List[dict]) -> Dict[str, float]:
    """
    Given eval results from all examples, compute summary metrics.
    """
    metrics = {}
    
    # Success rate
    successes = sum(1 for r in eval_results if r.get("passes", False))
    metrics["task_success_rate"] = successes / len(eval_results)
    
    # Faithfulness
    faithfulness_scores = [r.get("faithfulness_score", 0) for r in eval_results]
    metrics["faithfulness"] = np.mean(faithfulness_scores)
    
    # Groundedness
    groundedness_scores = [r.get("groundedness_score", 0) for r in eval_results]
    metrics["groundedness"] = np.mean(groundedness_scores)
    
    # Latency
    latencies = [r.get("latency_ms", 0) for r in eval_results]
    metrics["latency_p50"] = np.percentile(latencies, 50)
    metrics["latency_p99"] = np.percentile(latencies, 99)
    
    # Cost
    costs = [r.get("cost_usd", 0) for r in eval_results]
    metrics["cost_per_query"] = np.mean(costs)
    
    # Token usage
    token_counts = [r.get("tokens_used", 0) for r in eval_results]
    metrics["tokens_per_query"] = np.mean(token_counts)
    
    # Tool accuracy
    tool_correct = sum(1 for r in eval_results if r.get("tool_selection_correct", True))
    metrics["tool_call_accuracy"] = tool_correct / len(eval_results)
    
    return metrics
```

## Anti-Patterns: What Goes Wrong

### Anti-Pattern 1: Evaluating Only Happy Path

Don't just test the cases that work. Test boundary conditions.

```python
# BAD: Only testing normal cases
golden_examples = [
    {"query": "What's my balance?", "expected": "Your balance is $500"},
    {"query": "How much can I withdraw?", "expected": "You can withdraw up to $500"},
]

# GOOD: Explicit coverage of edge cases
golden_examples = [
    # Normal cases
    {"query": "What's my balance?", "expected": "Your balance is $500"},
    # Edge cases
    {"query": "", "expected": "I need more information"},  # Empty query
    {"query": "a" * 10000, "expected": "Query too long"},  # Extremely long input
    {"query": "DROP TABLE users;", "expected": "I can't help with that"},  # Injection attempt
    # Boundary conditions
    {"query": "Balance for account", "expected": "Which account?"},  # Ambiguous
]
```

### Anti-Pattern 2: Judge Overfitting

Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

```python
# BAD: Judge creates golden standard, then evaluates against it
judge = LLMJudge()
golden_examples = judge.generate_examples()  # Judge-generated
eval_results = judge.evaluate(golden_examples)  # Judge-evaluated
# Result: Artificially high scores. Judge agrees with itself.

# GOOD: Separate data curation from evaluation
# Golden dataset curated by humans (domain experts, customer service team)
# Judge is independent system that evaluates against human-curated standard
domain_experts = ["alice@company.com", "bob@company.com"]
golden_examples = collect_from_experts(domain_experts)
eval_results = judge.evaluate(golden_examples)
```

### Anti-Pattern 3: Metrics without Context

Don't report "success rate 92%" without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

```python
# BAD
print(f"Agent success rate: {success_rate:.1%}")

# GOOD
slice_results = evaluator.evaluate_slices(golden_examples, eval_results)
print("Agent success rate by slice:")
for slice_name, metrics in slice_results.items():
    print(f"  {slice_name}: {metrics['pass_rate']:.1%}")

print(f"Overall: {np.mean([m['pass_rate'] for m in slice_results.values()]):.1%}")
```

### Anti-Pattern 4: Static Eval

Running eval once, before deployment. But production is dynamic. Your agent's world changes.

```python
# BAD: One-time evaluation
eval_results = run_eval(agent, golden_dataset)
if eval_results.mean_score > 0.85:
    deploy(agent)

# GOOD: Continuous evaluation feedback loop
@schedule_hourly
def continuous_eval():
    # Eval on recent production data
    recent_queries = fetch_production_queries(hours=1)
    eval_results = run_eval(agent, recent_queries)
    
    # Compare against baseline
    if eval_results.mean_score < baseline * 0.95:
        alert("Production quality degrading")
    
    # Update baseline
    update_baseline(eval_results)
```

## Checklist: Before Deploying an Agent

- [ ] Golden dataset curated by domain experts (not synthetic)
- [ ] Judge calibrated: agreement with humans > 80%
- [ ] Slice evaluation run: agent performs consistently across difficulty/category
- [ ] Regression test passed: new version not worse than baseline
- [ ] Production eval configured: sampling rate chosen, infrastructure ready
- [ ] Metrics defined: what does success look like for this agent?
- [ ] Alerting rules set: when do we escalate?
- [ ] Baseline captured: we know what "normal" looks like

You cannot improve what you cannot measure. Build evaluation infrastructure first.

---

## Golden Dataset A curated human validated set of 100 500 test vectors query expec

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## LLM as Judge Using a separate LLM with calibrated criteria specific prompts fait

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Parallel Eval Architecture A dedicated evaluation system that mirrors the agent

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->

---

## Slice Evaluation Breaking eval results down by difficulty category and other met

## Core Principle

Evaluation must be built as parallel, always-on infrastructure—not a pre-deploy checklist—consisting of a human-curated golden dataset, a calibrated LLM judge validated against human agreement rates above 80%, and slice-level metrics that reveal category- and difficulty-specific failure modes. The four critical anti-patterns are testing only happy paths, letting the judge generate its own ground truth, reporting decontextualized aggregate metrics, and running evaluation only once. Continuous eval on production samples with baseline comparison and alerting is the production-grade standard.

## Key Heuristics

These are the load-bearing rules for this concept.

> Build evaluation as first-class infrastructure. Not an afterthought. Not a test file you run once before shipping.

> Think of it like continuous integration for agent behavior.

> Keep golden datasets small but representative. 100-500 examples is typical for most production agents.

> Every example in the dataset should be curated by a human or derived from actual production logs. Don't generate them synthetically.

> Don't use the same judge to create the golden dataset and then evaluate against it. You'll get a feedback loop that optimizes for the judge, not for reality.

> Don't report 'success rate 92%' without context. 92% on what? Easy queries? Hard ones? Recent data or stale?

> You cannot improve what you cannot measure. Build evaluation infrastructure first.

## Anti-Patterns & Fixes

- EvaluatingOnlyHappyPath: Testing only normal cases means you never discover failures at boundaries, edge inputs, or adversarial conditions. Fix: Explicitly add empty queries, extremely long inputs, injection attempts, and ambiguous queries to the golden dataset.
- JudgeOverfitting: Using the same LLM judge to both generate the golden dataset and evaluate against it creates a self-referential feedback loop that produces artificially high scores optimized for the judge rather than reality. Fix: Have domain experts curate the golden dataset independently from the judge used to evaluate.
- MetricsWithoutContext: Reporting a single aggregate success rate obscures where the agent fails—easy vs. hard queries, one category vs. another, recent vs. stale data. Fix: Always report slice-level metrics broken down by difficulty, category, and recency alongside the aggregate.
- StaticEval: Running evaluation once before deployment ignores that production is dynamic—agent behavior, data distributions, and user queries change over time. Fix: Schedule continuous evaluation on recent production samples, compare against a rolling baseline, and trigger alerts when scores degrade beyond a threshold.

## When To Apply

Load this page when:

- Use this when preparing to deploy an agent to production and needing to verify it works at scale under realistic conditions, not just in a notebook.
- Use this when setting up CI/CD for an agent system and needing evaluation to run automatically before every deployment.
- Use this when an agent's output quality is suspected to have degraded after a model update, prompt change, or data shift.
- Use this when building a scoring system and needing to decide whether to use LLM-as-judge, deterministic rules, or human review.
- Use this when eval scores look suspiciously high and you need to check whether the judge was used to generate the golden data it is evaluating against.
- Use this when reporting agent performance to stakeholders and needing to ensure metrics are contextualized by slice, difficulty, and category.
- Use this when golden dataset examples begin showing unexpectedly high failure rates, indicating the examples may no longer reflect current production patterns.

## Concrete Examples

- GoldenExample dataclass for an order status query: user asks 'What's the status of my order #12345?', expected output references shipment date and tracking, tools_required includes order_lookup and shipping_status, difficulty easy, category customer_support.
- LLMJudge.calibrate_judge: runs judge on a calibration set where human ground truth is known (agent output 'The order shipped on 2026-04-20' vs. human judgment True) and returns agreement rate.
- Injection attempt edge case in golden dataset: query 'DROP TABLE users;' with expected output 'I can't help with that' illustrating adversarial coverage.
- Continuous eval scheduled hourly: fetches recent production queries, runs eval, compares score against baseline * 0.95 threshold, alerts on degradation, and updates baseline.

## AI-Native Application

How this concept changes when the coder is an LLM agent:

**Evaluation Frameworks**

An LLM coding agent building other agents is at acute risk of judge overfitting—it will naturally generate synthetic golden examples and then evaluate against them using the same model family, producing self-validating scores that mask real failures. Additionally, an LLM agent may treat evaluation as a one-time gate rather than infrastructure, generating a single test run rather than a scheduled continuous loop, which means silent quality degradation after deployment goes undetected. This framework forces the agent to treat golden data curation and judge calibration as separate, human-anchored concerns, preventing the agent from closing the feedback loop on itself.

## Related Concepts

<!-- Add [[wikilinks]] to related concept pages after all pages are built -->

## Appears In

- `output/wiki/llmops-ai-agents/` (Phase 2)
<!-- Add cross-book references after master wiki is built -->
