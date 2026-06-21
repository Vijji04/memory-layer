---
title: Production Hardening
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, llmops, guardrails, circuit-breakers, canary, rollback]
confidence: high
source_files: 1
---

# Production Hardening

You've built an agent. It works in your notebook. Now you're shipping it to production where thousands of users will interact with it. Maybe millions. They'll ask edge cases. They'll try to break it. The system will fail in ways you didn't anticipate.

This chapter is about hardening—building the safeguards that let you sleep at night when your agent is in production.

## The Guardrail Layer Architecture

A production agent is wrapped. Guards on the input side. Guards on the output side. Guards around tool calls.

```
┌─────────────────────────────────────────────────────────┐
│                   USER REQUEST                          │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│              INPUT GUARDRAILS                           │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────┐  │
│  │ Length Check   │→ │ PII Detection  │→ │ Topic    │  │
│  │ (max 5k chars) │  │ (redact SSN)   │  │ Filter   │  │
│  └────────────────┘  └────────────────┘  └──────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                  AGENT LOGIC                            │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────┐  │
│  │ Tool           │→ │ Tool Args      │→ │ Tool     │  │
│  │ Selection      │  │ Validation     │  │ Execution│  │
│  └────────────────┘  └────────────────┘  └──────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│             OUTPUT GUARDRAILS                           │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────┐  │
│  │ Hallucination  │→ │ PII Redaction  │→ │ Toxicity │  │
│  │ Detection      │  │ (remove SSN)   │  │ Filter   │  │
│  └────────────────┘  └────────────────┘  └──────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────┐
│                  RESPONSE TO USER                       │
└─────────────────────────────────────────────────────────┘
```

Each guardrail is independent. Each can block.

```python
# guardrails/guardrail_layer.py
from typing import Tuple, Optional
from enum import Enum
import re

class GuardrailResult(Enum):
    PASS = "pass"
    BLOCK = "block"
    REDACT = "redact"

class InputGuardrails:
    """Check user input before it reaches the agent."""
    
    def __init__(self):
        self.max_input_length = 5000
        self.blocked_topics = ["violence", "illegal activity"]
    
    def check_length(self, text: str) -> Tuple[GuardrailResult, Optional[str]]:
        """Reject absurdly long inputs."""
        if len(text) > self.max_input_length:
            return GuardrailResult.BLOCK, f"Input exceeds {self.max_input_length} characters"
        return GuardrailResult.PASS, None
    
    def check_pii(self, text: str) -> Tuple[GuardrailResult, Optional[str], str]:
        """
        Detect personally identifiable information.
        Block if sensitive data exposed (SSN, credit card, etc.)
        """
        # Social Security Number pattern
        ssn_pattern = r'\b\d{3}-\d{2}-\d{4}\b'
        # Credit card pattern (simplified)
        cc_pattern = r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b'
        
        if re.search(ssn_pattern, text):
            return GuardrailResult.BLOCK, "Social Security Number detected in input", text
        
        if re.search(cc_pattern, text):
            return GuardrailResult.BLOCK, "Credit card number detected in input", text
        
        return GuardrailResult.PASS, None, text
    
    def check_topic(self, text: str) -> Tuple[GuardrailResult, Optional[str]]:
        """
        Block certain topics (violence, illegal activity, etc.)
        """
        text_lower = text.lower()
        
        for blocked_topic in self.blocked_topics:
            if blocked_topic in text_lower:
                return GuardrailResult.BLOCK, f"Topic not permitted: {blocked_topic}"
        
        return GuardrailResult.PASS, None
    
    def run_all(self, user_input: str) -> Tuple[bool, Optional[str], str]:
        """
        Run all input guardrails.
        Return: (allowed, reason_if_blocked, potentially_modified_input)
        """
        # Length check
        result, reason = self.check_length(user_input)
        if result == GuardrailResult.BLOCK:
            return False, reason, user_input
        
        # PII check
        result, reason, modified = self.check_pii(user_input)
        if result == GuardrailResult.BLOCK:
            return False, reason, user_input
        
        # Topic check
        result, reason = self.check_topic(user_input)
        if result == GuardrailResult.BLOCK:
            return False, reason, user_input
        
        return True, None, user_input

class OutputGuardrails:
    """Check agent output before sending to user."""
    
    def __init__(self, judge: LLMJudge):
        self.judge = judge
    
    def check_hallucination(
        self,
        agent_output: str,
        knowledge_source: str
    ) -> Tuple[GuardrailResult, Optional[str]]:
        """
        Does output contain hallucinations?
        Use LLM judge to evaluate groundedness.
        """
        decision = self.judge.judge_groundedness(agent_output, knowledge_source)
        
        if decision.score < 0.7:
            return GuardrailResult.BLOCK, f"Output contains unsupported claims. Score: {decision.score:.2f}"
        
        return GuardrailResult.PASS, None
    
    def redact_pii(self, text: str) -> str:
        """
        Remove PII from output before sending to user.
        Don't block—redact.
        """
        # Redact SSN
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN]', text)
        
        # Redact credit card (keep last 4 digits for reference)
        text = re.sub(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{1,4}\b', '[CC: ****]', text)
        
        # Redact email addresses (in some contexts)
        # text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
        
        return text
    
    def check_toxicity(self, text: str) -> Tuple[GuardrailResult, Optional[str]]:
        """
        Does output contain hate speech, profanity, abuse?
        Block if severe.
        """
        # Simplified check—real implementation would use toxicity classifier
        toxic_words = ["hate", "kill", "slur"]
        
        text_lower = text.lower()
        for word in toxic_words:
            if word in text_lower:
                return GuardrailResult.BLOCK, "Output contains harmful language"
        
        return GuardrailResult.PASS, None
    
    def run_all(
        self,
        agent_output: str,
        knowledge_source: str
    ) -> Tuple[bool, Optional[str], str]:
        """
        Run all output guardrails.
        Redact before block (apply redactions first).
        """
        # Redact PII first
        output = self.redact_pii(agent_output)
        
        # Check hallucination
        result, reason = self.check_hallucination(output, knowledge_source)
        if result == GuardrailResult.BLOCK:
            return False, reason, output
        
        # Check toxicity
        result, reason = self.check_toxicity(output)
        if result == GuardrailResult.BLOCK:
            return False, reason, output
        
        return True, None, output

# Usage
input_guards = InputGuardrails()
output_guards = OutputGuardrails(judge=judge)

def handle_request(user_input: str) -> str:
    # Check input
    allowed, reason, clean_input = input_guards.run_all(user_input)
    if not allowed:
        logger.warning(f"Input blocked: {reason}")
        return "I can't help with that request."
    
    # Run agent
    agent_output = agent.run(clean_input)
    
    # Check output
    allowed, reason, clean_output = output_guards.run_all(agent_output, knowledge_source)
    if not allowed:
        logger.warning(f"Output blocked: {reason}")
        return "I ran into an issue. Please try again."
    
    return clean_output
```

## Circuit Breakers: Fail Open, Recover Gracefully

When an agent starts misbehaving, you don't want it to fail millions of users. Circuit breakers trip automatically and route traffic elsewhere.

```python
# resilience/circuit_breaker.py
from enum import Enum
from datetime import datetime, timedelta
import time

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject new requests
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """
    Monitor agent health. Automatically disable misbehaving agents.
    
    Circuit breaker pattern:
    - CLOSED: Normal, requests go through
    - OPEN: Agent is broken, requests rejected immediately
    - HALF_OPEN: Agent might be fixed, let some requests through to test
    """
    
    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout_seconds: int = 60
    ):
        self.name = name
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.last_failure_time = None
        self.recovery_timeout = recovery_timeout_seconds
    
    def call(self, func, *args, **kwargs):
        """
        Execute function with circuit breaker protection.
        """
        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if self._should_attempt_recovery():
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker {self.name}: attempting recovery")
            else:
                raise CircuitBreakerOpen(f"Circuit {self.name} is open")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        """Reset on successful call."""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            logger.info(f"Circuit breaker {self.name}: recovered, closed")
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)
    
    def _on_failure(self):
        """Handle failure."""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        logger.warning(
            f"Circuit breaker {self.name}: failure {self.failure_count}/{self.failure_threshold}"
        )
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.error(f"Circuit breaker {self.name}: opened due to failures")
    
    def _should_attempt_recovery(self) -> bool:
        """Check if recovery timeout has passed."""
        if not self.last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout

class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open."""
    pass

# Usage
support_agent_breaker = CircuitBreaker(
    name="support_agent",
    failure_threshold=5,  # Trip after 5 consecutive failures
    recovery_timeout_seconds=60  # Try recovery after 60 seconds
)

def agent_handler(user_query: str) -> str:
    try:
        return support_agent_breaker.call(agent.run, user_query)
    except CircuitBreakerOpen:
        logger.error("Support agent circuit breaker is open")
        return "Our support system is temporarily unavailable. Please try again in a moment."
    except Exception as e:
        logger.error(f"Agent failed: {e}")
        return "An error occurred. Please try again."
```

## Shadow Mode: New Agent Runs Alongside Old

Before shipping a new agent to all users, run it in shadow mode. It processes all real requests but doesn't affect user responses. You compare outputs offline.

```python
# deployment/shadow_mode.py
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import json

@dataclass
class ShadowResult:
    request_id: str
    user_query: str
    production_output: str
    shadow_output: str
    agreement: bool  # Do they match?
    timestamp: datetime
    
    def to_json(self) -> str:
        return json.dumps({
            "request_id": self.request_id,
            "user_query": self.user_query,
            "production_output": self.production_output,
            "shadow_output": self.shadow_output,
            "agreement": self.agreement,
            "timestamp": self.timestamp.isoformat()
        })

class ShadowModeRunner:
    """
    Run new agent in parallel with production agent.
    Compare outputs without affecting users.
    """
    
    def __init__(
        self,
        production_agent,
        shadow_agent,
        sample_rate: float = 1.0  # Run shadow on 100% of traffic initially
    ):
        self.production_agent = production_agent
        self.shadow_agent = shadow_agent
        self.sample_rate = sample_rate
        self.results = []
    
    def process_request(self, request_id: str, user_query: str) -> str:
        """
        Process request with production agent (blocks user).
        Also run shadow agent (non-blocking).
        """
        # Production response (what user sees)
        production_output = self.production_agent.run(user_query)
        
        # Shadow response (background, doesn't affect user)
        if self._should_sample():
            shadow_output = self.shadow_agent.run(user_query)
            
            # Compare
            agreement = self._outputs_agree(production_output, shadow_output)
            
            result = ShadowResult(
                request_id=request_id,
                user_query=user_query,
                production_output=production_output,
                shadow_output=shadow_output,
                agreement=agreement,
                timestamp=datetime.utcnow()
            )
            
            # Store for analysis
            self._store_result(result)
        
        # Always return production output to user
        return production_output
    
    def _should_sample(self) -> bool:
        """Determine if we should run shadow for this request."""
        return random.random() < self.sample_rate
    
    def _outputs_agree(self, output_a: str, output_b: str) -> bool:
        """
        Simple exact match. Real implementation would use semantic similarity.
        """
        return output_a.strip() == output_b.strip()
    
    def _store_result(self, result: ShadowResult):
        """Store shadow result for offline analysis."""
        self.results.append(result)
        # Also send to backend for analysis
        self._send_to_backend(result)
    
    def _send_to_backend(self, result: ShadowResult):
        """Send result to analysis backend."""
        pass
    
    def agreement_report(self, limit: int = 1000) -> Dict:
        """Generate agreement report between agents."""
        recent = self.results[-limit:]
        
        agreed = sum(1 for r in recent if r.agreement)
        agreement_rate = agreed / len(recent) if recent else 0
        
        disagreements = [r for r in recent if not r.agreement]
        
        return {
            "total_samples": len(recent),
            "agreement_rate": agreement_rate,
            "disagreements": [
                {
                    "request_id": d.request_id,
                    "query": d.user_query,
                    "production": d.production_output[:200],
                    "shadow": d.shadow_output[:200]
                }
                for d in disagreements[:10]  # Show top 10
            ]
        }
    
    def is_ready_for_canary(self, min_agreement_rate: float = 0.95) -> bool:
        """Can we promote shadow agent to canary?"""
        report = self.agreement_report(limit=1000)
        return report["agreement_rate"] >= min_agreement_rate

# Usage
shadow_runner = ShadowModeRunner(
    production_agent=current_agent,
    shadow_agent=new_agent,
    sample_rate=1.0  # Run new agent on all traffic
)

def handle_request(request_id: str, user_query: str):
    return shadow_runner.process_request(request_id, user_query)

# Every hour, check agreement
@schedule_hourly
def check_shadow_mode():
    report = shadow_runner.agreement_report()
    print(f"Shadow agreement rate: {report['agreement_rate']:.1%}")
    
    if shadow_runner.is_ready_for_canary(min_agreement_rate=0.95):
        print("New agent ready for canary deployment")
        # Proceed to canary rollout
```

## Canary Deployment: Gradual Traffic Ramp

Don't flip a switch and send 100% traffic to the new agent. Ramp gradually: 1% → 5% → 25% → 100%. At each step, monitor metrics.

```python
# deployment/canary.py
from enum import Enum
from typing import Dict, Optional
import time

class CanaryStage(Enum):
    STAGE_1 = 0.01    # 1% traffic
    STAGE_2 = 0.05    # 5% traffic
    STAGE_3 = 0.25    # 25% traffic
    STAGE_4 = 1.0     # 100% traffic

class CanaryDeployment:
    """
    Gradually ramp new agent to 100% traffic.
    Monitor metrics at each stage.
    Rollback if problems detected.
    """
    
    def __init__(
        self,
        production_agent,
        canary_agent,
        initial_stage: CanaryStage = CanaryStage.STAGE_1
    ):
        self.production_agent = production_agent
        self.canary_agent = canary_agent
        self.current_stage = initial_stage
        self.stage_start_time = time.time()
        self.metrics_baseline = {}
    
    def route_request(self, request_id: str, user_query: str) -> str:
        """
        Route request to canary or production based on current stage.
        """
        traffic_ratio = self.current_stage.value
        
        # Deterministic routing: same user always routes same way
        user_hash = hash(request_id) % 100
        
        if user_hash < (traffic_ratio * 100):
            # Route to canary
            return self.canary_agent.run(user_query)
        else:
            # Route to production
            return self.production_agent.run(user_query)
    
    def check_metrics(self) -> Dict[str, float]:
        """
        Get current metrics for canary stage.
        Compare against production baseline.
        """
        return {
            "success_rate": self._get_success_rate(),
            "error_rate": self._get_error_rate(),
            "latency_p99": self._get_latency_p99(),
            "cost_per_query": self._get_cost_per_query()
        }
    
    def should_advance_stage(self) -> bool:
        """
        Determine if we should advance to next stage.
        Metrics must be within acceptable bounds.
        """
        metrics = self.check_metrics()
        
        # Success rate within 2% of baseline
        baseline_success = self.metrics_baseline.get("success_rate", 0.95)
        if metrics["success_rate"] < baseline_success * 0.98:
            return False
        
        # Error rate below threshold
        if metrics["error_rate"] > 0.05:
            return False
        
        # Latency not degraded more than 10%
        baseline_latency = self.metrics_baseline.get("latency_p99", 5000)
        if metrics["latency_p99"] > baseline_latency * 1.10:
            return False
        
        # All checks passed
        return True
    
    def should_rollback(self) -> bool:
        """
        Determine if we need to rollback canary.
        Stricter thresholds than stage advancement.
        """
        metrics = self.check_metrics()
        
        # Success rate collapsed
        baseline_success = self.metrics_baseline.get("success_rate", 0.95)
        if metrics["success_rate"] < baseline_success * 0.90:
            return True
        
        # Error rate spiked
        if metrics["error_rate"] > 0.10:
            return True
        
        # Latency degraded significantly
        baseline_latency = self.metrics_baseline.get("latency_p99", 5000)
        if metrics["latency_p99"] > baseline_latency * 1.50:
            return True
        
        return False
    
    def advance_stage(self):
        """Move to next deployment stage."""
        stages = list(CanaryStage)
        current_idx = stages.index(self.current_stage)
        
        if current_idx < len(stages) - 1:
            self.current_stage = stages[current_idx + 1]
            logger.info(f"Advanced canary to {self.current_stage.value:.0%} traffic")
    
    def rollback(self):
        """Roll back to production-only."""
        self.current_stage = CanaryStage.STAGE_1
        # Switch canary agent back to old version
        logger.error("Canary rolled back to stage 1")
    
    def _get_success_rate(self) -> float:
        """Query metrics backend."""
        pass
    
    def _get_error_rate(self) -> float:
        pass
    
    def _get_latency_p99(self) -> float:
        pass
    
    def _get_cost_per_query(self) -> float:
        pass

# Deployment orchestration
canary = CanaryDeployment(
    production_agent=agent_v1_2_4,
    canary_agent=agent_v1_2_5,
    initial_stage=CanaryStage.STAGE_1
)

# Capture baseline metrics before starting canary
canary.metrics_baseline = canary.check_metrics()

@schedule_every_5_minutes
def canary_monitor():
    # Check if we should advance
    if canary.current_stage == CanaryStage.STAGE_4:
        # Already at 100%, done
        return
    
    # Check for rollback first
    if canary.should_rollback():
        logger.critical("Canary metrics degraded, rolling back")
        canary.rollback()
        alert("Canary deployment rolled back")
        return
    
    # Check for advancement
    if canary.should_advance_stage():
        # Wait minimum time in stage (e.g., 30 minutes)
        if time.time() - canary.stage_start_time > 1800:
            canary.advance_stage()
            canary.stage_start_time = time.time()
            alert(f"Canary advanced to {canary.current_stage.value:.0%}")
```

## Rollback Strategies: The Agent Already Made Decisions

Your agent doesn't just respond—it makes decisions. It calls tools. It modifies data. What happens when you roll back and the old agent sees the new state?

```python
# deployment/rollback.py
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SourceOfTruth:
    """Track what the agent did so we can reason about rollbacks."""
    version: str
    request_id: str
    timestamp: datetime
    actions_taken: list  # [{"tool": "transfer_funds", "amount": 500}, ...]
    
    def can_rollback(self) -> bool:
        """Can this action be safely undone?"""
        for action in self.actions_taken:
            if not self._is_reversible(action):
                return False
        return True
    
    def _is_reversible(self, action: Dict[str, Any]) -> bool:
        """Determine if action can be reversed."""
        tool = action.get("tool")
        
        # Some actions are reversible
        reversible_tools = ["create_order", "transfer_funds", "send_email"]
        
        # Some are not (e.g., deletion)
        irreversible_tools = ["delete_record", "close_account"]
        
        if tool in reversible_tools:
            return True
        if tool in irreversible_tools:
            return False
        
        # Unknown tool—assume irreversible
        return False

class RollbackManager:
    """
    Manage rollback when deploying new agent version.
    """
    
    def __init__(self, audit_log_backend):
        self.audit_log = audit_log_backend
        self.source_of_truth = {}
    
    def record_action(
        self,
        version: str,
        request_id: str,
        tool_name: str,
        tool_args: Dict[str, Any],
        result: Any
    ):
        """Record every action agent took."""
        action = {
            "tool": tool_name,
            "args": tool_args,
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        if request_id not in self.source_of_truth:
            self.source_of_truth[request_id] = SourceOfTruth(
                version=version,
                request_id=request_id,
                timestamp=datetime.utcnow(),
                actions_taken=[]
            )
        
        self.source_of_truth[request_id].actions_taken.append(action)
    
    def plan_rollback(self, from_version: str, to_version: str) -> Dict[str, Any]:
        """
        Plan rollback from one version to another.
        Identify which requests may be affected.
        """
        # Find all requests handled by from_version
        affected_requests = [
            req_id for req_id, sot in self.source_of_truth.items()
            if sot.version == from_version
        ]
        
        # Separate reversible from irreversible
        reversible = [
            req_id for req_id in affected_requests
            if self.source_of_truth[req_id].can_rollback()
        ]
        
        irreversible = [
            req_id for req_id in affected_requests
            if not self.source_of_truth[req_id].can_rollback()
        ]
        
        return {
            "from_version": from_version,
            "to_version": to_version,
            "total_affected": len(affected_requests),
            "reversible": len(reversible),
            "irreversible": len(irreversible),
            "irreversible_examples": irreversible[:10],
            "can_safely_rollback": len(irreversible) == 0
        }
    
    def execute_rollback(self, from_version: str) -> Dict[str, int]:
        """
        Execute rollback for reversible actions.
        Manual intervention required for irreversible ones.
        """
        affected_requests = [
            req_id for req_id, sot in self.source_of_truth.items()
            if sot.version == from_version
        ]
        
        reversed_count = 0
        failed_count = 0
        
        for req_id in affected_requests:
            sot = self.source_of_truth[req_id]
            
            if not sot.can_rollback():
                logger.warning(f"Cannot rollback request {req_id}: irreversible actions")
                failed_count += 1
                continue
            
            # Reverse each action in reverse order
            try:
                for action in reversed(sot.actions_taken):
                    self._reverse_action(action)
                reversed_count += 1
            except Exception as e:
                logger.error(f"Failed to rollback {req_id}: {e}")
                failed_count += 1
        
        return {
            "reversed": reversed_count,
            "failed": failed_count,
            "manual_review_required": failed_count
        }
    
    def _reverse_action(self, action: Dict[str, Any]):
        """Reverse a single action."""
        tool = action["tool"]
        
        if tool == "create_order":
            # Cancel order
            cancel_order(action["result"]["order_id"])
        elif tool == "transfer_funds":
            # Transfer back
            transfer_funds(
                from_account=action["args"]["to_account"],
                to_account=action["args"]["from_account"],
                amount=action["args"]["amount"]
            )
        # ... etc
        else:
            raise ValueError(f"Don't know how to reverse {tool}")

# Usage
rollback_mgr = RollbackManager(audit_log_backend=postgres)

# When agent creates an order
def create_order(user_id: str, items: list) -> str:
    order_id = agent.tools["create_order"](items)
    
    rollback_mgr.record_action(
        version="v1.2.5",
        request_id=request_id,
        tool_name="create_order",
        tool_args={"items": items},
        result={"order_id": order_id}
    )
    
    return order_id

# Plan rollback before executing
rollback_plan = rollback_mgr.plan_rollback(from_version="v1.2.5", to_version="v1.2.4")
if rollback_plan["can_safely_rollback"]:
    logger.info("Rollback is safe")
else:
    logger.warning(f"{rollback_plan['irreversible']} requests have irreversible actions")
    # Flag for manual review
```

## Rate Limiting and Quota Management

Your agent calls LLM APIs. Those APIs have limits. You also want to limit users (prevent abuse).

```python
# rate_limiting/quota_manager.py
from typing import Dict, Tuple
from datetime import datetime, timedelta
import threading

class QuotaState:
    """Track quota for a user or agent."""
    
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        self.requests: list[float] = []
        self.lock = threading.Lock()
    
    def is_allowed(self) -> bool:
        """Check if request is within quota."""
        with self.lock:
            now = datetime.utcnow().timestamp()
            cutoff = now - self.window_seconds
            
            # Remove old requests outside the window
            self.requests = [r for r in self.requests if r > cutoff]
            
            # Check if we're over limit
            if len(self.requests) >= self.limit:
                return False
            
            # Record this request
            self.requests.append(now)
            return True
    
    def available_in(self) -> float:
        """How long until quota resets (seconds)?"""
        if not self.requests:
            return 0
        
        cutoff = datetime.utcnow().timestamp() - self.window_seconds
        oldest_request = self.requests[0]
        
        if oldest_request < cutoff:
            return 0
        
        return oldest_request - cutoff + 0.1

class RateLimiter:
    """
    Rate limit users and agents.
    Different limits for different tiers.
    """
    
    def __init__(self):
        self.per_user_quotas: Dict[str, QuotaState] = {}
        self.per_agent_quotas: Dict[str, QuotaState] = {}
    
    def check_user_quota(self, user_id: str) -> Tuple[bool, Optional[str]]:
        """
        Check if user is within quota.
        Typical: 100 requests per hour per user.
        """
        if user_id not in self.per_user_quotas:
            self.per_user_quotas[user_id] = QuotaState(
                limit=100,
                window_seconds=3600
            )
        
        quota = self.per_user_quotas[user_id]
        
        if not quota.is_allowed():
            reset_in = quota.available_in()
            return False, f"Rate limit exceeded. Try again in {reset_in:.0f} seconds."
        
        return True, None
    
    def check_agent_quota(self, agent_name: str) -> Tuple[bool, Optional[str]]:
        """
        Check if agent is within quota for calling LLM API.
        Typical: 10,000 requests per hour per agent.
        """
        if agent_name not in self.per_agent_quotas:
            self.per_agent_quotas[agent_name] = QuotaState(
                limit=10000,
                window_seconds=3600
            )
        
        quota = self.per_agent_quotas[agent_name]
        
        if not quota.is_allowed():
            reset_in = quota.available_in()
            return False, f"Agent quota exhausted. Reset in {reset_in:.0f} seconds."
        
        return True, None
    
    def check_all_quotas(self, user_id: str, agent_name: str) -> Tuple[bool, Optional[str]]:
        """
        Check both user and agent quotas.
        Either can block.
        """
        allowed, reason = self.check_user_quota(user_id)
        if not allowed:
            return False, reason
        
        allowed, reason = self.check_agent_quota(agent_name)
        if not allowed:
            return False, reason
        
        return True, None

# Usage
rate_limiter = RateLimiter()

def handle_request(user_id: str, user_query: str) -> str:
    allowed, reason = rate_limiter.check_all_quotas(
        user_id=user_id,
        agent_name="support_agent"
    )
    
    if not allowed:
        return f"Error: {reason}"
    
    return agent.run(user_query)
```

## Data Isolation in Multi-Tenant Systems

If you're running agents for multiple customers (SaaS), you need strict data isolation.

```python
# multi_tenancy/tenant_isolation.py
from typing import Optional
from functools import wraps

class TenantContext:
    """Thread-local context for current tenant."""
    _current_tenant = None
    
    @classmethod
    def set_current(cls, tenant_id: str):
        cls._current_tenant = tenant_id
    
    @classmethod
    def get_current(cls) -> Optional[str]:
        return cls._current_tenant

def require_tenant(func):
    """
    Decorator: enforce that tenant context is set before executing.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        tenant_id = TenantContext.get_current()
        if not tenant_id:
            raise PermissionError("Tenant context not set")
        return func(*args, **kwargs)
    return wrapper

class TenantIsolatedDataStore:
    """
    All data access goes through this.
    Automatically filters by tenant.
    """
    
    def __init__(self, backend):
        self.backend = backend
    
    @require_tenant
    def get_customer_record(self, customer_id: str) -> dict:
        """
        Get customer record for current tenant.
        Raises error if customer belongs to different tenant.
        """
        tenant_id = TenantContext.get_current()
        
        # Always include tenant in query
        record = self.backend.query(
            "SELECT * FROM customers WHERE id=? AND tenant_id=?",
            [customer_id, tenant_id]
        )
        
        if not record:
            raise ValueError(f"Customer {customer_id} not found")
        
        # Double-check tenant owns this record
        if record["tenant_id"] != tenant_id:
            raise PermissionError("Cross-tenant access denied")
        
        return record
    
    @require_tenant
    def get_knowledge_base(self) -> str:
        """
        Get tenant-specific knowledge base.
        Each tenant sees only their own data.
        """
        tenant_id = TenantContext.get_current()
        
        kb = self.backend.get(
            f"knowledge_base:{tenant_id}"
        )
        
        return kb or ""
    
    @require_tenant
    def get_guardrails_config(self) -> dict:
        """
        Get tenant-specific guardrail configuration.
        Different tenants can have different rules.
        """
        tenant_id = TenantContext.get_current()
        
        config = self.backend.query(
            "SELECT * FROM guardrail_configs WHERE tenant_id=?",
            [tenant_id]
        )
        
        return config or {}

# Usage
data_store = TenantIsolatedDataStore(backend=postgres)

def api_handler(request):
    tenant_id = request.headers.get("X-Tenant-ID")
    
    # Set tenant context for this request
    TenantContext.set_current(tenant_id)
    
    try:
        # All data access automatically filters by tenant
        customer = data_store.get_customer_record(request.customer_id)
        kb = data_store.get_knowledge_base()
        
        response = agent.run(
            user_query=request.query,
            knowledge_base=kb
        )
        
        return response
    
    finally:
        # Clear tenant context
        TenantContext.set_current(None)
```

## Load Testing Agents

Before launch, stress test. Can your agent handle 1000 concurrent users? 10,000?

```python
# testing/load_test.py
import concurrent.futures
import time
from typing import List
from dataclasses import dataclass

@dataclass
class LoadTestResult:
    total_requests: int
    successful: int
    failed: int
    latencies: List[float]
    
    @property
    def success_rate(self) -> float:
        return self.successful / self.total_requests if self.total_requests > 0 else 0
    
    @property
    def p50_latency(self) -> float:
        sorted_latencies = sorted(self.latencies)
        return sorted_latencies[len(sorted_latencies) // 2]
    
    @property
    def p99_latency(self) -> float:
        sorted_latencies = sorted(self.latencies)
        return sorted_latencies[int(len(sorted_latencies) * 0.99)]

def load_test_agent(
    agent,
    num_requests: int = 1000,
    num_workers: int = 10,
    test_queries: List[str] = None
) -> LoadTestResult:
    """
    Stress test agent with concurrent requests.
    """
    if test_queries is None:
        test_queries = [
            "What's my account balance?",
            "How do I reset my password?",
            "Can I export my data?",
        ] * (num_requests // 3)
    
    results = {
        "successful": 0,
        "failed": 0,
        "latencies": []
    }
    
    def single_request(query):
        start = time.time()
        try:
            agent.run(query)
            latency = (time.time() - start) * 1000  # ms
            results["latencies"].append(latency)
            results["successful"] += 1
        except Exception as e:
            logger.error(f"Request failed: {e}")
            results["failed"] += 1
    
    # Run requests in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [
            executor.submit(single_request, test_queries[i % len(test_queries)])
            for i in range(num_requests)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            future.result()
    
    return LoadTestResult(
        total_requests=num_requests,
        successful=results["successful"],
        failed=results["failed"],
        latencies=results["latencies"]
    )

# Run load test
result = load_test_agent(
    agent=agent,
    num_requests=1000,
    num_workers=10
)

print(f"Success rate: {result.success_rate:.1%}")
print(f"P50 latency: {result.p50_latency:.0f}ms")
print(f"P99 latency: {result.p99_latency:.0f}ms")

if result.success_rate < 0.99:
    raise AssertionError("Success rate too low for production")

if result.p99_latency > 5000:
    raise AssertionError("P99 latency too high")
```

## Production Readiness Checklist

Before you deploy:

```python
# deployment/readiness_check.py

PRODUCTION_READINESS = [
    # Guardrails
    ("Input guardrails implemented", lambda: input_guards is not None),
    ("Output guardrails implemented", lambda: output_guards is not None),
    ("PII detection enabled", lambda: input_guards.check_pii is not None),
    
    # Resilience
    ("Circuit breaker configured", lambda: circuit_breaker is not None),
    ("Rate limiting enabled", lambda: rate_limiter is not None),
    ("Fallback strategy defined", lambda: has_fallback_agent()),
    
    # Observability
    ("Tracing enabled", lambda: tracing_backend is configured),
    ("Structured logging configured", lambda: logger is not None),
    ("Dashboard created", lambda: metrics_dashboard is not None),
    ("Alerting rules defined", lambda: len(ALERT_RULES) > 0),
    
    # Deployment
    ("Shadow mode tested", lambda: shadow_runner.agreement_report()["agreement_rate"] > 0.95),
    ("Canary deployment ready", lambda: canary is not None),
    ("Rollback plan documented", lambda: rollback_plan is not None),
    
    # Data
    ("Data isolation configured", lambda: TenantContext is not None),
    ("Audit logging enabled", lambda: audit_log is not None),
    
    # Testing
    ("Load test passed", lambda: load_test_result.success_rate > 0.99),
    ("Load test latency acceptable", lambda: load_test_result.p99_latency < 5000),
    ("Golden dataset curated", lambda: len(golden_dataset) >= 100),
    ("Evaluation metrics green", lambda: eval_metrics["success_rate"] > 0.90),
    
    # Documentation
    ("Runbook written", lambda: runbook is not None),
    ("On-call handoff complete", lambda: oncall_team is trained),
]

def check_readiness() -> Dict[str, bool]:
    """Run all production readiness checks."""
    results = {}
    
    for check_name, check_fn in PRODUCTION_READINESS:
        try:
            results[check_name] = check_fn()
        except Exception as e:
            logger.error(f"Check failed: {check_name}: {e}")
            results[check_name] = False
    
    return results

# Run before deployment
readiness = check_readiness()

all_passed = all(readiness.values())
failed = [name for name, passed in readiness.items() if not passed]

if not all_passed:
    print("DEPLOYMENT BLOCKED:")
    for name in failed:
        print(f"  [ ] {name}")
    exit(1)
else:
    print("ALL CHECKS PASSED. READY FOR PRODUCTION.")
```

---

## Checklist: Before Going Live

- [ ] Guardrails layer implemented: input, output, tool execution
- [ ] Circuit breaker configured: automatic trip on failures
- [ ] Shadow mode: new agent validated against production
- [ ] Canary deployment: gradual rollout with metrics monitoring
- [ ] Rollback plan: know which actions are reversible
- [ ] Rate limiting: per-user and per-agent quotas
- [ ] Data isolation: multi-tenant isolation enforced
- [ ] Load testing: passed with >99% success rate
- [ ] Production readiness: all checklist items green

You are now ready to run an agent at scale. The infrastructure you've built will keep it running even when things go wrong.
