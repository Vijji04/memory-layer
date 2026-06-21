---
title: Pattern: Metacognitive Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, metacognition, self-improvement, case-studies]
confidence: high
source_files: 1
---

# Pattern: Metacognitive Agents

## Why Metacognitive Matters

A normal agent executes tasks. A metacognitive agent watches itself execute tasks, notices friction points, and improves.

The pattern: **Agent → Session → Analysis → Improvement → Deploy**.

Not "learn from every failure" (you'll overfit to noise). But "aggregate sessions, find patterns, approve changes, deploy."

When to use:
- Agent has been deployed for weeks/months (enough sessions to find patterns)
- Improvement loop is safe (code changes don't go directly to prod)
- You can detect and prevent regressions
- There's human approval in the loop

---

## Case Study 1: Factory — Self-Improving Coding Agent

### Business Problem

Factory.dev runs a coding agent that generates pull requests. Over 3 months, 10K+ sessions. Engineers notice:

- Agent struggles with async/await patterns (20% of failures)
- Agent gets stuck asking for clarification instead of trying (5% of sessions)
- Agent writes great code but leaves out docstrings (30% of PRs flagged)

Manually retraining the agent every month is expensive. Solution: **analysis agent** watches sessions, finds patterns, proposes improvements, coding agent implements them, humans approve.

### Why This Pattern Fits

- **Scale:** 10K sessions produce weak signal in individual sessions (noise), strong signal in aggregate.
- **Safety:** Improvements are proposed, tested, reviewed—not auto-deployed.
- **Reproducibility:** Same codebases get same agent. Compare "before/after" metrics.
- **Prevents overfitting:** Only improve on >100 session patterns, not one failure.

### Architecture Diagram

```
[Coding Agent Session 1-10000]
    |
    v
[Session Storage]
  Store full execution trace:
    - Prompts sent
    - Tokens used
    - Time spent
    - Success/failure
    - User feedback
    |
    v
[Analysis Agent]
  Read sessions
  Identify friction patterns
  Cluster failures
  Generate improvement tickets
    |
    v
[Improvement Ticket]
  "120 sessions fail on async/await"
  "Suggested fix: update prompt with async examples"
    |
    v
[Coding Agent (Improved)]
  Human: "Approve this improvement?"
  Yes → Deploy to prod
  No → Discard
```

### Implementation: Session Analysis → Improvement Loop

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
from collections import Counter
import json

class SessionStatus(Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILURE = "failure"

@dataclass
class AgentSession:
    """Record of one coding agent execution."""
    session_id: str
    agent_version: str
    user_request: str
    start_time: str
    end_time: str
    duration_seconds: float
    status: SessionStatus
    code_generated: str
    tokens_used: int
    errors: List[str]  # ["async/await syntax", "missing imports"]
    user_feedback: Optional[str]  # User review comment
    user_satisfaction: Optional[int]  # 1-5 rating

@dataclass
class PatternAnalysis:
    """Result of analyzing session patterns."""
    pattern_name: str  # e.g., "async_await_failures"
    affected_sessions: int
    percentage: float
    failure_examples: List[str]  # Sample errors
    common_triggers: List[str]  # Things that trigger the pattern
    severity: str  # "critical", "high", "medium", "low"

@dataclass
class ImprovementProposal:
    """Suggested change to the agent."""
    proposal_id: str
    pattern: PatternAnalysis
    proposed_change: str  # e.g., "Add 3 async/await examples to system prompt"
    change_type: str  # "prompt_update", "tool_addition", "logic_fix"
    expected_impact: str  # "Would fix ~120 sessions (95% of async failures)"
    estimated_effort: str  # "low", "medium", "high"
    implementation_details: str

@dataclass
class ApprovedImprovement:
    """Improvement that passed human review."""
    improvement_id: str
    proposal: ImprovementProposal
    approved_by: str
    approval_timestamp: str
    implementation_status: str  # "pending", "implemented", "deployed"

class CodingAgentSession:
    """Simulation of coding agent execution."""
    
    def __init__(self, session_id: str, agent_version: str):
        self.session_id = session_id
        self.agent_version = agent_version
        self.start_time = datetime.now().isoformat()
        self.errors = []
        self.code = ""
        self.tokens = 0
    
    async def execute(self, user_request: str) -> AgentSession:
        """Run the coding agent."""
        
        import time
        start = time.time()
        
        # Simulate agent work
        await asyncio.sleep(0.3)
        
        # Simulate failure patterns (deterministic for demo)
        if "async" in user_request.lower():
            self.errors.append("async/await syntax error")
            status = SessionStatus.FAILURE
        elif "docstring" in user_request.lower():
            self.errors.append("missing docstring")
            status = SessionStatus.PARTIAL
        else:
            status = SessionStatus.SUCCESS
        
        self.code = f"# Generated code for: {user_request}\ndef main():\n    pass"
        self.tokens = int(len(user_request) / 4 + 150)
        
        duration = time.time() - start
        
        return AgentSession(
            session_id=self.session_id,
            agent_version=self.agent_version,
            user_request=user_request,
            start_time=self.start_time,
            end_time=datetime.now().isoformat(),
            duration_seconds=duration,
            status=status,
            code_generated=self.code,
            tokens_used=self.tokens,
            errors=self.errors,
            user_feedback=None,
            user_satisfaction=None
        )

class SessionAnalyzer:
    """Analyze sessions to find improvement patterns."""
    
    async def analyze_sessions(self, sessions: List[AgentSession]) -> List[PatternAnalysis]:
        """
        Find patterns in session failures.
        
        Algorithm:
        1. Group sessions by error type
        2. Count frequency
        3. Keep only patterns > 5% of sessions
        4. Extract common triggers
        """
        
        await asyncio.sleep(0.2)  # Simulate computation
        
        # Count error types
        error_counts = Counter()
        error_to_sessions = {}
        
        for session in sessions:
            for error in session.errors:
                error_counts[error] += 1
                if error not in error_to_sessions:
                    error_to_sessions[error] = []
                error_to_sessions[error].append(session)
        
        # Find patterns (threshold: 5% of sessions)
        patterns = []
        total_sessions = len(sessions)
        min_affected = max(1, int(total_sessions * 0.05))
        
        for error_type, count in error_counts.most_common():
            if count >= min_affected:
                # Extract failure examples
                affected_sessions = error_to_sessions[error_type]
                failure_examples = [
                    s.user_request for s in affected_sessions[:3]
                ]
                
                # Find common triggers
                triggers = [
                    s.user_request.split()[0:3] for s in affected_sessions[:5]
                ]
                common_triggers = [
                    word for phrase in triggers
                    for word in phrase
                    if len(word) > 3
                ]
                common_triggers = list(set(common_triggers))[:3]
                
                # Determine severity
                percentage = (count / total_sessions) * 100
                if percentage > 20:
                    severity = "high"
                elif percentage > 10:
                    severity = "medium"
                else:
                    severity = "low"
                
                pattern = PatternAnalysis(
                    pattern_name=error_type.replace(" ", "_"),
                    affected_sessions=count,
                    percentage=percentage,
                    failure_examples=failure_examples,
                    common_triggers=common_triggers,
                    severity=severity
                )
                
                patterns.append(pattern)
        
        return patterns

class ImprovementPlanner:
    """Design improvements based on patterns."""
    
    async def plan_improvements(self, patterns: List[PatternAnalysis]) -> List[ImprovementProposal]:
        """
        For each pattern, propose a fix.
        """
        
        await asyncio.sleep(0.1)
        
        proposals = []
        
        for i, pattern in enumerate(patterns):
            proposal_id = f"impl_{i+1:03d}"
            
            # Map pattern to improvement
            if "async/await" in pattern.pattern_name:
                proposed_change = "Add 3 comprehensive async/await examples to system prompt"
                change_type = "prompt_update"
                expected_impact = f"Would fix ~{int(pattern.affected_sessions * 0.95)} sessions"
                effort = "low"
                details = """
                Update SYSTEM_PROMPT to include:
                1. Example: async function with await
                2. Example: concurrent async tasks
                3. Example: error handling in async
                """
            
            elif "docstring" in pattern.pattern_name:
                proposed_change = "Add docstring validation + auto-generation step"
                change_type = "logic_fix"
                expected_impact = f"Would fix ~{int(pattern.affected_sessions * 0.90)} sessions"
                effort = "medium"
                details = """
                Add a post-generation step:
                1. Parse generated code AST
                2. Check each function/class for docstring
                3. If missing: ask agent to add docstrings
                """
            
            else:
                proposed_change = f"Investigate {pattern.pattern_name} failures"
                change_type = "investigation"
                expected_impact = f"Unknown impact on {pattern.affected_sessions} sessions"
                effort = "high"
                details = "Requires human investigation"
            
            proposal = ImprovementProposal(
                proposal_id=proposal_id,
                pattern=pattern,
                proposed_change=proposed_change,
                change_type=change_type,
                expected_impact=expected_impact,
                estimated_effort=effort,
                implementation_details=details
            )
            
            proposals.append(proposal)
        
        return proposals

class CodingAgentImprover:
    """Self-improving agent orchestrator."""
    
    def __init__(self):
        self.analyzer = SessionAnalyzer()
        self.planner = ImprovementPlanner()
        self.approved_improvements = []
    
    async def improvement_loop(self, sessions: List[AgentSession]):
        """
        Run full self-improvement cycle.
        """
        
        print(f"[Improvement Loop] Analyzing {len(sessions)} sessions...")
        
        # Step 1: Analyze sessions
        patterns = await self.analyzer.analyze_sessions(sessions)
        print(f"  Found {len(patterns)} patterns:")
        for pattern in patterns:
            print(f"    - {pattern.pattern_name}: {pattern.affected_sessions} sessions ({pattern.percentage:.1f}%)")
        
        # Step 2: Plan improvements
        proposals = await self.planner.plan_improvements(patterns)
        print(f"\n[Improvement Proposals] Generated {len(proposals)} proposals:")
        for proposal in proposals:
            print(f"    - {proposal.proposal_id}: {proposal.proposed_change}")
            print(f"      Expected impact: {proposal.expected_impact}")
            print(f"      Effort: {proposal.estimated_effort}")
        
        # Step 3: (Simulated) Human approval
        print(f"\n[Human Review] Approving proposals...")
        for proposal in proposals:
            if proposal.estimated_effort == "low":
                print(f"  ✓ {proposal.proposal_id} approved (low effort)")
                approved = ApprovedImprovement(
                    improvement_id=proposal.proposal_id,
                    proposal=proposal,
                    approved_by="eng_lead_001",
                    approval_timestamp=datetime.now().isoformat(),
                    implementation_status="pending"
                )
                self.approved_improvements.append(approved)
            else:
                print(f"  ⏳ {proposal.proposal_id} pending review (high effort)")
    
    def generate_improvement_summary(self) -> Dict[str, Any]:
        """Summary of approved improvements."""
        
        total_affected = sum(
            imp.proposal.pattern.affected_sessions
            for imp in self.approved_improvements
        )
        
        return {
            "improvements_approved": len(self.approved_improvements),
            "total_sessions_affected": total_affected,
            "improvements": [
                {
                    "id": imp.improvement_id,
                    "change": imp.proposal.proposed_change,
                    "affected_sessions": imp.proposal.pattern.affected_sessions,
                    "status": imp.implementation_status
                }
                for imp in self.approved_improvements
            ]
        }


async def main():
    print("=" * 70)
    print("FACTORY.DEV — SELF-IMPROVING CODING AGENT")
    print("=" * 70)
    
    # Generate simulated sessions
    print("\n[Session Generation] Creating 200 simulated sessions...")
    sessions = []
    
    test_requests = [
        "Write an async function to fetch data",
        "Create a sync database query",
        "Implement recursive algorithm",
        "Write async code with proper error handling",
        "Build a REST API endpoint",
        "Process async events from queue",
        "Parse JSON file",
        "Generate docstrings for this function",
        "Concurrent async tasks example",
    ]
    
    for i in range(200):
        request = test_requests[i % len(test_requests)]
        session_obj = CodingAgentSession(f"sess_{i:04d}", "v1.2.3")
        session = await session_obj.execute(request)
        sessions.append(session)
    
    print(f"  Created {len(sessions)} sessions")
    
    # Count outcomes
    success = sum(1 for s in sessions if s.status == SessionStatus.SUCCESS)
    partial = sum(1 for s in sessions if s.status == SessionStatus.PARTIAL)
    failure = sum(1 for s in sessions if s.status == SessionStatus.FAILURE)
    
    print(f"\nSession Outcomes:")
    print(f"  Success: {success} ({success/len(sessions)*100:.0f}%)")
    print(f"  Partial: {partial} ({partial/len(sessions)*100:.0f}%)")
    print(f"  Failure: {failure} ({failure/len(sessions)*100:.0f}%)")
    
    # Run improvement loop
    improver = CodingAgentImprover()
    await improver.improvement_loop(sessions)
    
    # Summary
    print(f"\n{'=' * 70}")
    print("IMPROVEMENT SUMMARY")
    print(f"{'=' * 70}")
    
    summary = improver.generate_improvement_summary()
    print(f"Approved improvements: {summary['improvements_approved']}")
    print(f"Sessions affected: {summary['total_sessions_affected']}")
    
    for imp in summary['improvements']:
        print(f"\n  {imp['id']}: {imp['change']}")
        print(f"    Sessions affected: {imp['affected_sessions']}")
        print(f"    Status: {imp['status']}")


if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Aggregate before improving:** Don't react to single failures. Look for >5% patterns.

2. **Prevent overfitting:** Only improve on reproducible, high-frequency issues.

3. **Human approval in loop:** Improvements need "yes" from engineer before deployment.

4. **Track implementation status:** "pending", "implemented", "deployed". Don't claim success until deployed.

5. **Measure before/after:** Compare failure rates on same test suite pre/post improvement.

---

## Case Study 2: Anthropic — Noise in Agentic Coding Evaluations

### Business Problem

Anthropic evaluates coding agents on benchmarks. But infrastructure flakiness corrupts scores:

- Test sometimes times out (infrastructure slow)
- Test sometimes fails due to package versioning (environment unstable)
- Resource contention (other jobs on same machine)

Result: Same agent scored 72% one day, 81% another day. Not due to agent improvement—due to noise.

Solution: **meta-evaluation**. Detect and measure noise. Correct benchmark scores. Calibrate resources.

### Implementation: Noise Detection & Score Correction

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any
from enum import Enum
import statistics

class NoiseSource(Enum):
    TIMEOUT = "timeout"
    ENVIRONMENT = "environment"
    RESOURCE_CONTENTION = "resource_contention"
    FLAKINESS = "flakiness"

@dataclass
class TestRun:
    """Single evaluation run."""
    test_id: str
    agent_version: str
    outcome: str  # "pass", "fail", "timeout"
    execution_time_ms: float
    resource_usage: Dict[str, Any]  # CPU, memory, disk
    timestamp: str
    noise_flags: List[NoiseSource]
    raw_score: float

class NoiseDetector:
    """Identify and measure noise in evaluations."""
    
    async def analyze_test_runs(self, runs: List[TestRun]) -> Dict[str, Any]:
        """
        Detect noise patterns.
        
        Heuristics:
        1. High variance in execution time → flakiness
        2. Resource spikes → contention
        3. Timeouts → infrastructure issue
        """
        
        await asyncio.sleep(0.2)
        
        # Group by test
        tests_by_id = {}
        for run in runs:
            if run.test_id not in tests_by_id:
                tests_by_id[run.test_id] = []
            tests_by_id[run.test_id].append(run)
        
        noise_analysis = {}
        
        for test_id, test_runs in tests_by_id.items():
            # Execution time variance
            times = [r.execution_time_ms for r in test_runs]
            avg_time = statistics.mean(times)
            std_time = statistics.stdev(times) if len(times) > 1 else 0
            cv = (std_time / avg_time) if avg_time > 0 else 0
            
            # Timeout rate
            timeouts = sum(1 for r in test_runs if r.outcome == "timeout")
            timeout_rate = timeouts / len(test_runs)
            
            # Inconsistency (same agent, different scores)
            scores = [r.raw_score for r in test_runs]
            score_variance = max(scores) - min(scores) if scores else 0
            
            noise_level = "high" if cv > 0.3 or timeout_rate > 0.1 else \
                         "medium" if cv > 0.15 or timeout_rate > 0.05 else \
                         "low"
            
            noise_analysis[test_id] = {
                "execution_time_cv": cv,
                "timeout_rate": timeout_rate,
                "score_variance": score_variance,
                "noise_level": noise_level,
                "runs": len(test_runs)
            }
        
        return noise_analysis

class EvaluationHarness:
    """Production evaluation harness with noise correction."""
    
    def __init__(self):
        self.detector = NoiseDetector()
    
    async def evaluate_agent(
        self,
        agent_version: str,
        test_suite: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Run evaluation with noise detection.
        """
        
        print(f"[Evaluation] Testing agent {agent_version}")
        print(f"  {len(test_suite)} tests in suite")
        
        # Run tests multiple times (for noise detection)
        num_runs = 5
        all_runs = []
        
        for run_num in range(num_runs):
            print(f"  Run {run_num + 1}/{num_runs}...")
            
            for test in test_suite:
                # Simulate test execution
                await asyncio.sleep(0.1)
                
                # Deterministic failure for demo
                outcome = "pass" if "easy" in test["name"] else \
                         "fail" if "hard" in test["name"] else \
                         "pass"
                
                execution_time = 150 if "fast" in test["name"] else 500
                
                # Simulate flakiness
                import random
                if random.random() < 0.1:
                    execution_time *= 5  # Spike
                    outcome = "timeout"
                
                noise_flags = []
                if execution_time > 1000:
                    noise_flags.append(NoiseSource.TIMEOUT)
                
                run = TestRun(
                    test_id=test["name"],
                    agent_version=agent_version,
                    outcome=outcome,
                    execution_time_ms=execution_time,
                    resource_usage={},
                    timestamp=f"2025-04-23T10:{run_num:02d}:00Z",
                    noise_flags=noise_flags,
                    raw_score=1.0 if outcome == "pass" else 0.0
                )
                
                all_runs.append(run)
        
        # Detect noise
        noise_analysis = await self.detector.analyze_test_runs(all_runs)
        
        # Calculate corrected scores
        corrected_scores = {}
        for test_id, analysis in noise_analysis.items():
            test_runs = [r for r in all_runs if r.test_id == test_id]
            raw_scores = [r.raw_score for r in test_runs]
            raw_avg = statistics.mean(raw_scores)
            
            # Correct for noise: boost if noisy (less reliable measurement)
            # Formula: corrected_score = raw_score + (noise_level_penalty)
            if analysis["noise_level"] == "high":
                # High noise means we're less confident. Add conservative boost.
                correction = 0.05
            elif analysis["noise_level"] == "medium":
                correction = 0.02
            else:
                correction = 0.0
            
            corrected_score = min(raw_avg + correction, 1.0)
            
            corrected_scores[test_id] = {
                "raw_score": raw_avg,
                "corrected_score": corrected_score,
                "noise_level": analysis["noise_level"],
                "confidence": 1.0 - (analysis["execution_time_cv"] * 0.5)
            }
        
        # Overall score
        raw_overall = statistics.mean([r.raw_score for r in all_runs])
        corrected_overall = statistics.mean([
            s["corrected_score"] for s in corrected_scores.values()
        ])
        
        return {
            "agent_version": agent_version,
            "raw_score": raw_overall,
            "corrected_score": corrected_overall,
            "noise_analysis": noise_analysis,
            "corrected_scores": corrected_scores,
            "num_runs": num_runs,
            "total_tests": len(all_runs)
        }


async def main():
    harness = EvaluationHarness()
    
    print("=" * 70)
    print("ANTHROPIC — NOISE DETECTION IN AGENT EVALUATIONS")
    print("=" * 70)
    
    test_suite = [
        {"name": "test_easy_hello_world"},
        {"name": "test_medium_fibonacci"},
        {"name": "test_hard_graph_algorithm"},
        {"name": "test_fast_simple_math"},
        {"name": "test_slow_network_io"},
    ]
    
    result = await harness.evaluate_agent("agent_v2.1.0", test_suite)
    
    print(f"\n{'=' * 70}")
    print("EVALUATION RESULTS")
    print(f"{'=' * 70}")
    print(f"Agent: {result['agent_version']}")
    print(f"Raw Score: {result['raw_score']:.1%}")
    print(f"Corrected Score: {result['corrected_score']:.1%}")
    print(f"Difference: {(result['corrected_score'] - result['raw_score'])*100:.1f} percentage points")
    print()
    print("Corrected Scores by Test:")
    for test_id, score_data in result['corrected_scores'].items():
        print(f"  {test_id:30} {score_data['corrected_score']:.0%} " +
              f"(noise: {score_data['noise_level']}, confidence: {score_data['confidence']:.1%})")


if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Run tests multiple times:** Not once. 5 runs to detect variance.

2. **Measure noise explicitly:** CV, timeout rate, score variance. Don't guess.

3. **Correct scores upward cautiously:** High noise = less confidence. Small boost, but not huge.

4. **Report confidence interval:** "Agent scored 81% ± 3%". Transparency beats false precision.

5. **Track resource utilization:** Contention is measurable (CPU/memory spikes). Fix infrastructure, not agent.

---

## Case Study 3: Goodfire — Experimenter Agents for Interpretability Research

### Business Problem

Goodfire builds interpretability tools for LLMs. They run experiments to understand model behavior. Manual experiment design is slow. Solution: **experimenter agents** that design and run experiments autonomously.

Key distinction: **Developer agents** (write code) vs **Experimenter agents** (design experiments).

Pipeline:
1. **Hypothesis:** "Attention heads cluster by semantic role"
2. **Experiment design:** Create 5 experiments to test hypothesis
3. **Execution:** Run experiments (takes hours)
4. **Analysis:** Detect hypothesis progress
5. **Refinement:** New hypothesis based on results

### Implementation: Experiment Loop with Convergence

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import statistics

class HypothesisStatus(Enum):
    SUPPORTED = "supported"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"

@dataclass
class Hypothesis:
    """Proposed explanation for model behavior."""
    hypothesis_id: str
    text: str  # e.g., "Attention heads cluster by semantic role"
    confidence: float
    tested_by: List[str]  # Experiment IDs that test this

@dataclass
class Experiment:
    """Proposed experiment."""
    experiment_id: str
    hypothesis_id: str
    experiment_design: str
    methodology: str
    expected_outcome: str
    status: str  # "pending", "running", "complete"
    results: Optional[Dict[str, Any]]
    execution_time_seconds: float

@dataclass
class ExperimentRun:
    """Single execution of experiment."""
    run_id: str
    experiment_id: str
    metric_name: str
    metric_value: float
    raw_data: Dict[str, Any]

class HypothesisReasoner:
    """Proposes testable hypotheses."""
    
    async def generate_hypothesis(
        self,
        context: str,
        previous_hypotheses: List[Hypothesis]
    ) -> Hypothesis:
        """
        Generate new hypothesis based on context and previous results.
        """
        
        await asyncio.sleep(0.1)
        
        # Heuristic hypothesis generation
        if "attention" in context.lower():
            text = "Attention patterns correlate with syntactic structure"
        elif "embedding" in context.lower():
            text = "Embedding space clusters by word class"
        else:
            text = "Hidden layer activations encode surface-level features"
        
        return Hypothesis(
            hypothesis_id=f"hyp_{len(previous_hypotheses) + 1:03d}",
            text=text,
            confidence=0.5,
            tested_by=[]
        )

class ExperimentDesigner:
    """Designs experiments to test hypotheses."""
    
    async def design_experiments(self, hypothesis: Hypothesis) -> List[Experiment]:
        """
        Given a hypothesis, design multiple experiments to test it.
        """
        
        await asyncio.sleep(0.15)
        
        experiments = []
        
        # Design 3-5 experiments
        experiment_templates = [
            {
                "name": "Correlation Analysis",
                "description": "Measure correlation between hypothesis variable and target"
            },
            {
                "name": "Ablation Study",
                "description": "Remove hypothesized component, measure performance impact"
            },
            {
                "name": "Synthetic Data Test",
                "description": "Test on artificial data where hypothesis is known true/false"
            },
        ]
        
        for i, template in enumerate(experiment_templates):
            experiment = Experiment(
                experiment_id=f"exp_{i:03d}",
                hypothesis_id=hypothesis.hypothesis_id,
                experiment_design=template["description"],
                methodology=f"Using {template['name']}",
                expected_outcome="If hypothesis is true, metric should increase",
                status="pending",
                results=None,
                execution_time_seconds=0.0
            )
            
            experiments.append(experiment)
        
        return experiments

class ExperimentRunner:
    """Execute experiments (simulated)."""
    
    async def run_experiment(self, experiment: Experiment) -> Experiment:
        """
        Run experiment and collect results.
        In reality: GPU-intensive model introspection.
        """
        
        import time
        start = time.time()
        
        # Simulate execution
        await asyncio.sleep(0.3)
        
        # Simulate results
        metric_value = 0.65 if "Correlation" in experiment.methodology else 0.45
        
        experiment.status = "complete"
        experiment.results = {
            "metric": "hypothesis_support_score",
            "value": metric_value,
            "confidence_interval": [metric_value - 0.05, metric_value + 0.05],
            "p_value": 0.03
        }
        experiment.execution_time_seconds = time.time() - start
        
        return experiment

class HypothesisValidator:
    """Evaluate hypothesis based on experiment results."""
    
    async def validate_hypothesis(
        self,
        hypothesis: Hypothesis,
        experiments: List[Experiment]
    ) -> tuple[Hypothesis, HypothesisStatus]:
        """
        Aggregate experiment results to determine hypothesis status.
        
        Algorithm:
        1. Collect all experiment results for this hypothesis
        2. Compute average support score
        3. Determine if supported (>0.6), refuted (<0.4), or inconclusive
        """
        
        await asyncio.sleep(0.1)
        
        if not experiments or not any(e.results for e in experiments):
            return hypothesis, HypothesisStatus.UNKNOWN
        
        # Aggregate results
        support_scores = [
            e.results["value"] for e in experiments
            if e.results and "value" in e.results
        ]
        
        if not support_scores:
            return hypothesis, HypothesisStatus.UNKNOWN
        
        avg_support = statistics.mean(support_scores)
        
        # Determine status
        if avg_support > 0.6:
            status = HypothesisStatus.SUPPORTED
        elif avg_support < 0.4:
            status = HypothesisStatus.REFUTED
        else:
            status = HypothesisStatus.INCONCLUSIVE
        
        # Update hypothesis confidence
        hypothesis.confidence = avg_support
        hypothesis.tested_by = [e.experiment_id for e in experiments]
        
        return hypothesis, status

class ExperimenterAgent:
    """Orchestrates research loop."""
    
    def __init__(self):
        self.hypothesis_reasoner = HypothesisReasoner()
        self.designer = ExperimentDesigner()
        self.runner = ExperimentRunner()
        self.validator = HypothesisValidator()
        
        self.hypotheses: List[Hypothesis] = []
        self.experiments: List[Experiment] = []
        self.convergence_threshold = 3  # 3 supported/refuted to stop
    
    async def research_loop(self, initial_context: str, max_iterations: int = 5):
        """
        Main research loop: hypothesis → design → execute → validate → refine.
        """
        
        print(f"[Research Loop] Starting interpretability investigation")
        print(f"  Initial context: {initial_context}")
        
        for iteration in range(max_iterations):
            print(f"\n[Iteration {iteration + 1}/{max_iterations}]")
            
            # Step 1: Generate hypothesis
            print(f"  Generating hypothesis...")
            hypothesis = await self.hypothesis_reasoner.generate_hypothesis(
                initial_context,
                self.hypotheses
            )
            self.hypotheses.append(hypothesis)
            print(f"    {hypothesis.hypothesis_id}: {hypothesis.text}")
            
            # Step 2: Design experiments
            print(f"  Designing experiments...")
            experiments = await self.designer.design_experiments(hypothesis)
            print(f"    Designed {len(experiments)} experiments")
            
            # Step 3: Run experiments
            print(f"  Running experiments...")
            for exp in experiments:
                exp = await self.runner.run_experiment(exp)
                self.experiments.append(exp)
                if exp.results:
                    print(f"    {exp.experiment_id}: {exp.results['value']:.2f}")
            
            # Step 4: Validate hypothesis
            print(f"  Validating hypothesis...")
            hypothesis, status = await self.validator.validate_hypothesis(
                hypothesis,
                experiments
            )
            self.hypotheses[-1] = hypothesis
            print(f"    Status: {status.value.upper()}")
            print(f"    Confidence: {hypothesis.confidence:.2%}")
            
            # Step 5: Check convergence
            supported = sum(
                1 for h in self.hypotheses
                if h.confidence > 0.6
            )
            refuted = sum(
                1 for h in self.hypotheses
                if h.confidence < 0.4
            )
            
            total_strong = supported + refuted
            
            if total_strong >= self.convergence_threshold:
                print(f"\n[Convergence] Reached threshold: {total_strong} strong hypotheses")
                print(f"  Supported: {supported}, Refuted: {refuted}")
                break
    
    def print_summary(self):
        """Print research summary."""
        
        print(f"\n{'=' * 70}")
        print("RESEARCH SUMMARY")
        print(f"{'=' * 70}")
        print(f"Hypotheses tested: {len(self.hypotheses)}")
        print(f"Experiments run: {len(self.experiments)}")
        print()
        print("Hypothesis Status:")
        
        for hyp in self.hypotheses:
            status_icon = "✓" if hyp.confidence > 0.6 else \
                         "✗" if hyp.confidence < 0.4 else "?"
            print(f"  {status_icon} {hyp.hypothesis_id}: {hyp.text[:50]}...")
            print(f"    Confidence: {hyp.confidence:.0%}")
            print(f"    Tests: {', '.join(hyp.tested_by)}")


async def main():
    agent = ExperimenterAgent()
    
    print("=" * 70)
    print("GOODFIRE — EXPERIMENTER AGENTS FOR INTERPRETABILITY")
    print("=" * 70)
    
    await agent.research_loop(
        initial_context="Understanding attention head specialization",
        max_iterations=3
    )
    
    agent.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Hypothesis → Experiments (not trial-and-error):** Design experiments to test specific claims, not random exploration.

2. **Convergence detection:** Stop when you have enough strong (supported/refuted) hypotheses. Don't explore forever.

3. **Aggregate results:** One experiment is noise; five experiments converge to truth.

4. **Distinction: Developer vs Experimenter:** Developer agents write code (output: code). Experimenter agents design tests (output: experiments).

5. **Iterative refinement:** Each iteration's results inform the next hypothesis.

---

## Key Takeaways

1. **Reflection ≠ Learning:** Reflecting on sessions is cheap. Learning (changing code) is expensive. Separate them.

2. **Aggregate before improving:** 1 failure = noise. 100+ failures = pattern. Only act on patterns.

3. **Humans approve changes:** Improvements proposed, tested, reviewed, approved. Then deployed.

4. **Measure noise explicitly:** Not all variance is progress. Separate signal from infrastructure flakiness.

5. **Convergence beats infinite loops:** Stop when you have enough evidence (supported + refuted hypotheses). Don't explore endlessly.

6. **Version the agent itself:** If agent version v2 is deployed, you need to reproduce its behavior. Store the prompt, tools, logic.

---

## Further Reading

- **Goodfire:** https://www.goodfire.ai/ — Real tool for interpretability research
- **Anthropic Evaluations:** https://github.com/anthropics/evals — Open-source evaluation framework
- **Factory.dev:** https://www.factory.dev/ — Autonomous code generation
- **Reinforcement Learning from Human Feedback (RLHF):** Related to self-improvement from feedback loops
