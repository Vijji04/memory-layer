---
title: Observability and Cost Control
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, llmops, observability, tracing, cost, caching]
confidence: high
source_files: 1
---

# Observability and Cost Control

Your agent is running. Thousands of users interact with it daily. Something is wrong—but you don't know what. Is it slow? Expensive? Broken?

This is the observability problem. You cannot improve what you cannot see. And you cannot sustain what you cannot afford.

This chapter is about building visibility into agent systems and managing their cost. Not as an afterthought. As infrastructure.

## Trace and Span Architecture

An agent is a graph of operations. A span is an operation. A trace is the entire graph for one request.

```
REQUEST: "What's my account balance?"
│
├─ SPAN: input_validation (5ms)
│  └─ SPAN: detect_pii (2ms)
│
├─ SPAN: agent_reasoning (450ms)
│  ├─ SPAN: llm_call (400ms)
│  │  └─ input: 2,300 tokens
│  │  └─ output: 150 tokens
│  │  └─ model: claude-3-5-sonnet
│  │  └─ cost: $0.00089
│  │
│  ├─ SPAN: tool_selection (10ms)
│  │  └─ tool: get_account_balance
│  │
│  └─ SPAN: tool_execution (35ms)
│     ├─ SPAN: database_query (30ms)
│     │  └─ SELECT balance FROM accounts WHERE id=?
│     │  └─ rows_returned: 1
│     │
│     └─ SPAN: result_formatting (3ms)
│
├─ SPAN: output_validation (8ms)
│  └─ SPAN: guardrails_check (5ms)
│
└─ SPAN: response_formatting (2ms)

TOTAL LATENCY: 465ms
TOTAL COST: $0.00089
TOTAL TOKENS: 2,450 input + 150 output
```

Build infrastructure to capture this. Every function call that matters gets traced.

```python
# observability/tracing.py
import time
import json
from contextlib import contextmanager
from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

@dataclass
class Span:
    """A single operation within a request trace."""
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    operation_name: str
    start_time: float
    end_time: Optional[float]
    duration_ms: Optional[float]
    tags: Dict[str, Any]
    logs: list
    
    def finish(self):
        """Mark span as complete."""
        self.end_time = time.time()
        self.duration_ms = (self.end_time - self.start_time) * 1000
    
    def add_tag(self, key: str, value: Any):
        """Add metadata to span (not logged during execution)."""
        self.tags[key] = value
    
    def log(self, message: str, level: str = "info"):
        """Log event during span execution."""
        self.logs.append({
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message
        })
    
    def to_dict(self) -> Dict:
        return {
            "span_id": self.span_id,
            "trace_id": self.trace_id,
            "parent_span_id": self.parent_span_id,
            "operation_name": self.operation_name,
            "duration_ms": self.duration_ms,
            "tags": self.tags,
            "logs": self.logs
        }

class TraceContext:
    """
    Thread-local context for the current request trace.
    Allows any function to get/create spans without explicit parameter passing.
    """
    
    _local_storage = {}  # In production: use contextvars
    
    @classmethod
    def create_trace(cls, trace_id: str) -> "TraceContext":
        """Start a new trace."""
        ctx = TraceContext(trace_id=trace_id)
        cls._local_storage[trace_id] = ctx
        return ctx
    
    @classmethod
    def get_current(cls, trace_id: str) -> Optional["TraceContext"]:
        """Get current trace context."""
        return cls._local_storage.get(trace_id)
    
    def __init__(self, trace_id: str):
        self.trace_id = trace_id
        self.spans: Dict[str, Span] = {}
        self.root_span: Optional[Span] = None
        self.current_span_id: Optional[str] = None
    
    def start_span(
        self,
        operation_name: str,
        parent_span_id: Optional[str] = None
    ) -> Span:
        """Create and start a new span."""
        span_id = self._generate_span_id()
        
        span = Span(
            span_id=span_id,
            trace_id=self.trace_id,
            parent_span_id=parent_span_id or self.current_span_id,
            operation_name=operation_name,
            start_time=time.time(),
            end_time=None,
            duration_ms=None,
            tags={},
            logs=[]
        )
        
        self.spans[span_id] = span
        previous_span_id = self.current_span_id
        self.current_span_id = span_id
        
        return span
    
    def end_span(self, span: Span):
        """Mark span as finished."""
        span.finish()
        self.current_span_id = span.parent_span_id
    
    def _generate_span_id(self) -> str:
        """Create unique span ID."""
        return hashlib.md5(
            f"{self.trace_id}-{time.time()}".encode()
        ).hexdigest()[:16]
    
    def to_dict(self) -> Dict:
        """Export entire trace as dictionary."""
        return {
            "trace_id": self.trace_id,
            "spans": [span.to_dict() for span in self.spans.values()],
            "root_span_id": self.root_span.span_id if self.root_span else None
        }

@contextmanager
def traced(trace_id: str, operation_name: str):
    """
    Context manager for easy span creation.
    
    Usage:
        with traced("req_123", "llm_call"):
            response = llm.generate(...)
    """
    ctx = TraceContext.get_current(trace_id)
    if not ctx:
        ctx = TraceContext.create_trace(trace_id)
    
    span = ctx.start_span(operation_name)
    try:
        yield span
    finally:
        ctx.end_span(span)

# Usage example
def agent_handler(user_query: str) -> str:
    trace_id = generate_request_id()
    ctx = TraceContext.create_trace(trace_id)
    
    with traced(trace_id, "handle_user_request") as span:
        
        with traced(trace_id, "input_validation") as val_span:
            validate_input(user_query)
            val_span.add_tag("input_length", len(user_query))
        
        with traced(trace_id, "agent_reasoning") as agent_span:
            
            with traced(trace_id, "llm_inference") as llm_span:
                response = llm.generate(
                    model="claude-3-5-sonnet-20241022",
                    messages=[{"role": "user", "content": user_query}]
                )
                llm_span.add_tag("model", "claude-3-5-sonnet-20241022")
                llm_span.add_tag("input_tokens", response.usage.input_tokens)
                llm_span.add_tag("output_tokens", response.usage.output_tokens)
                llm_span.add_tag("cost_usd", calculate_cost(response))
            
            with traced(trace_id, "tool_execution") as tool_span:
                tool_result = execute_tool(response.tool_calls[0])
                tool_span.add_tag("tool_name", response.tool_calls[0].name)
                tool_span.add_tag("tool_result_length", len(str(tool_result)))
    
    # Export trace
    trace_data = ctx.to_dict()
    send_to_observability_backend(trace_data)
    
    return response.content
```

**Design decision**: Trace everything. Yes, it's overhead. But you can't optimize what you can't see. Sample spans in high-volume systems (trace 1% of requests in detail).

## Structured Logging

Traces are for the happy path. When things go wrong, you need logs. Make logs structured so they're machine-parseable.

```python
# observability/logging.py
import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime

class StructuredLogger:
    """
    JSON-structured logging for agents.
    Every log entry is a JSON object with consistent schema.
    """
    
    def __init__(self, name: str, service: str):
        self.name = name
        self.service = service
        self.handler = logging.getLogger(name)
    
    def log(
        self,
        level: str,
        message: str,
        trace_id: Optional[str] = None,
        span_id: Optional[str] = None,
        user_id: Optional[str] = None,
        **tags
    ):
        """
        Log a structured event.
        All logs follow consistent JSON schema.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service,
            "logger": self.name,
            "level": level.upper(),
            "message": message,
            "trace_id": trace_id,
            "span_id": span_id,
            "user_id": user_id,
            **tags  # Additional context
        }
        
        # Output as JSON
        self.handler.log(
            getattr(logging, level.upper()),
            json.dumps(log_entry)
        )
        
        return log_entry
    
    def info(self, message: str, **tags):
        return self.log("info", message, **tags)
    
    def error(self, message: str, exception: Optional[Exception] = None, **tags):
        entry = self.log("error", message, **tags)
        if exception:
            entry["exception"] = {
                "type": type(exception).__name__,
                "message": str(exception),
                "traceback": traceback.format_exc()
            }
        return entry
    
    def warning(self, message: str, **tags):
        return self.log("warning", message, **tags)

# Schema for agent-specific events
def log_agent_decision(
    logger: StructuredLogger,
    trace_id: str,
    agent_name: str,
    decision: str,
    confidence: float,
    alternatives_considered: int,
    latency_ms: float
):
    """Log when agent makes a significant decision."""
    logger.info(
        f"Agent decision",
        trace_id=trace_id,
        agent_name=agent_name,
        decision=decision,
        decision_confidence=confidence,
        alternatives_considered=alternatives_considered,
        latency_ms=latency_ms
    )

def log_tool_call(
    logger: StructuredLogger,
    trace_id: str,
    tool_name: str,
    input_args: Dict[str, Any],
    output: Any,
    latency_ms: float,
    success: bool
):
    """Log tool execution."""
    logger.info(
        f"Tool call",
        trace_id=trace_id,
        tool_name=tool_name,
        input_keys=list(input_args.keys()),
        output_length=len(str(output)),
        latency_ms=latency_ms,
        success=success
    )

def log_llm_call(
    logger: StructuredLogger,
    trace_id: str,
    model: str,
    input_tokens: int,
    output_tokens: int,
    cost_usd: float,
    latency_ms: float
):
    """Log LLM API call."""
    logger.info(
        f"LLM call",
        trace_id=trace_id,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        cost_usd=cost_usd,
        latency_ms=latency_ms
    )

# Usage
logger = StructuredLogger(name="agent_service", service="customer_support_agent")

log_llm_call(
    logger=logger,
    trace_id="req_abc123",
    model="claude-3-5-sonnet-20241022",
    input_tokens=2300,
    output_tokens=150,
    cost_usd=0.00089,
    latency_ms=450
)
```

All logs go to a central system (ELK, Datadog, Splunk) where they're indexed and queryable.

## Dashboard Design: What to Monitor

Not all metrics are equal. Focus on metrics that answer business questions.

```python
# monitoring/dashboard_schema.py
from typing import List, Dict, Any

class DashboardWidget:
    """A single dashboard widget (graph, gauge, table)."""
    
    def __init__(self, title: str, metric_query: str, visualization: str):
        self.title = title
        self.metric_query = metric_query  # Query to backend (Prometheus, CloudWatch, etc.)
        self.visualization = visualization  # "line", "gauge", "heatmap", etc.

class Dashboard:
    """Production observability dashboard for an agent service."""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.widgets: List[DashboardWidget] = []
        self._setup_standard_widgets()
    
    def _setup_standard_widgets(self):
        """Create standard widgets every agent service needs."""
        
        # SUCCESS RATE
        self.add_widget(
            title="Success Rate",
            metric_query="rate(agent_requests_successful[5m]) / rate(agent_requests_total[5m])",
            visualization="gauge"
        )
        
        # LATENCY P50, P95, P99
        self.add_widget(
            title="Response Latency (ms)",
            metric_query=[
                "histogram_quantile(0.50, agent_latency_ms)",
                "histogram_quantile(0.95, agent_latency_ms)",
                "histogram_quantile(0.99, agent_latency_ms)"
            ],
            visualization="line"
        )
        
        # ERROR RATE
        self.add_widget(
            title="Error Rate",
            metric_query="rate(agent_errors_total[5m])",
            visualization="line"
        )
        
        # COST PER QUERY
        self.add_widget(
            title="Average Cost Per Query",
            metric_query="rate(agent_cost_usd_total[5m]) / rate(agent_requests_total[5m])",
            visualization="line"
        )
        
        # TOKEN USAGE
        self.add_widget(
            title="Tokens Per Query (Input + Output)",
            metric_query=[
                "rate(agent_tokens_input_total[5m]) / rate(agent_requests_total[5m])",
                "rate(agent_tokens_output_total[5m]) / rate(agent_requests_total[5m])"
            ],
            visualization="line"
        )
        
        # TOOL EXECUTION TIME BREAKDOWN
        self.add_widget(
            title="Tool Execution Time %",
            metric_query="rate(tool_execution_duration_ms[5m]) / rate(agent_total_duration_ms[5m])",
            visualization="pie"
        )
        
        # LLM CALL TIME BREAKDOWN
        self.add_widget(
            title="LLM Call Time %",
            metric_query="rate(llm_duration_ms[5m]) / rate(agent_total_duration_ms[5m])",
            visualization="pie"
        )
        
        # QUEUE DEPTH
        self.add_widget(
            title="Queued Requests",
            metric_query="agent_queue_depth",
            visualization="gauge"
        )
        
        # CACHE HIT RATE
        self.add_widget(
            title="Cache Hit Rate",
            metric_query="rate(cache_hits_total[5m]) / (rate(cache_hits_total[5m]) + rate(cache_misses_total[5m]))",
            visualization="gauge"
        )
    
    def add_widget(
        self,
        title: str,
        metric_query: str,
        visualization: str
    ):
        """Add a widget to the dashboard."""
        widget = DashboardWidget(title, metric_query, visualization)
        self.widgets.append(widget)

# Real dashboards from production systems
# Nearpod: Success rate per content type + per user segment
# Harvey: Cost per legal query + success by case type
# Cursor: Compilation latency + cache hit rates

# Create dashboard
dashboard = Dashboard("customer_support_agent")

# Print all metrics being tracked
for widget in dashboard.widgets:
    print(f"- {widget.title}")
```

## Cost Attribution: Which Agent/Tool is Most Expensive?

You can't manage what you can't measure. Break down costs by agent, by tool, by model.

```python
# cost/attribution.py
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class CostBreakdown:
    """Cost attributed to different dimensions."""
    total_cost_usd: float
    by_model: Dict[str, float]  # {"gpt-4": 12.50, "claude": 8.30}
    by_tool: Dict[str, float]   # {"database": 0.50, "web_search": 1.20}
    by_agent: Dict[str, float]  # {"support": 15.00, "sales": 5.00}
    by_hour: Dict[str, float]   # {ISO timestamp: cost}

class CostAttributor:
    """
    Track and attribute costs to agents, tools, and models.
    """
    
    def __init__(self, backend):
        self.backend = backend  # Query interface to logs/traces
    
    def breakdown_by_model(self, hours: int = 24) -> Dict[str, float]:
        """
        How much did each model cost in the last N hours?
        """
        query = f"""
        SELECT
            model,
            SUM(cost_usd) as total_cost
        FROM llm_calls
        WHERE timestamp > now() - INTERVAL '{hours} hours'
        GROUP BY model
        ORDER BY total_cost DESC
        """
        
        results = self.backend.query(query)
        return {row["model"]: row["total_cost"] for row in results}
    
    def breakdown_by_tool(self, hours: int = 24) -> Dict[str, float]:
        """
        How much did each tool cost?
        Some tools call external APIs (web search, maps) with per-call pricing.
        """
        query = f"""
        SELECT
            tool_name,
            SUM(cost_usd) as total_cost,
            COUNT(*) as call_count
        FROM tool_calls
        WHERE timestamp > now() - INTERVAL '{hours} hours'
        GROUP BY tool_name
        ORDER BY total_cost DESC
        """
        
        results = self.backend.query(query)
        return {row["tool_name"]: row["total_cost"] for row in results}
    
    def breakdown_by_agent(self, hours: int = 24) -> Dict[str, float]:
        """
        Total cost per agent.
        """
        query = f"""
        SELECT
            agent_name,
            SUM(cost_usd) as total_cost,
            COUNT(*) as request_count,
            SUM(cost_usd) / COUNT(*) as cost_per_request
        FROM agent_requests
        WHERE timestamp > now() - INTERVAL '{hours} hours'
        GROUP BY agent_name
        ORDER BY total_cost DESC
        """
        
        results = self.backend.query(query)
        return {
            row["agent_name"]: {
                "total": row["total_cost"],
                "per_request": row["cost_per_request"],
                "request_count": row["request_count"]
            }
            for row in results
        }
    
    def identify_cost_outliers(self, hours: int = 24, threshold: float = 2.0) -> list:
        """
        Find requests that were unusually expensive.
        These might indicate bugs or inefficiencies.
        """
        query = f"""
        SELECT
            request_id,
            trace_id,
            agent_name,
            cost_usd,
            tokens_used,
            latency_ms
        FROM agent_requests
        WHERE timestamp > now() - INTERVAL '{hours} hours'
        ORDER BY cost_usd DESC
        LIMIT 100
        """
        
        results = self.backend.query(query)
        
        # Calculate median cost
        costs = [r["cost_usd"] for r in results]
        median_cost = sorted(costs)[len(costs) // 2]
        
        # Flag outliers (> 2x median)
        outliers = [
            r for r in results
            if r["cost_usd"] > median_cost * threshold
        ]
        
        return outliers
    
    def cost_trend(self, days: int = 30) -> Dict[str, list]:
        """
        Cost over time. Is spending trending up or down?
        """
        query = f"""
        SELECT
            DATE(timestamp) as day,
            SUM(cost_usd) as daily_cost,
            COUNT(*) as request_count
        FROM agent_requests
        WHERE timestamp > now() - INTERVAL '{days} days'
        GROUP BY DATE(timestamp)
        ORDER BY day
        """
        
        results = self.backend.query(query)
        
        return {
            "daily_costs": [r["daily_cost"] for r in results],
            "daily_requests": [r["request_count"] for r in results],
            "cost_per_request": [
                r["daily_cost"] / r["request_count"]
                for r in results
            ]
        }

# Usage
attributor = CostAttributor(backend=prometheus_backend)

# Cost breakdown
print("\nCOST BREAKDOWN (last 24h):")
print("\nBy Model:")
for model, cost in attributor.breakdown_by_model().items():
    print(f"  {model}: ${cost:.2f}")

print("\nBy Tool:")
for tool, cost in attributor.breakdown_by_tool().items():
    print(f"  {tool}: ${cost:.2f}")

print("\nBy Agent:")
for agent, data in attributor.breakdown_by_agent().items():
    print(f"  {agent}: ${data['total']:.2f} ({data['cost_per_request']:.4f}/req)")

# Find cost anomalies
outliers = attributor.identify_cost_outliers(threshold=3.0)
if outliers:
    print(f"\nWARNING: Found {len(outliers)} unusually expensive requests:")
    for outlier in outliers[:5]:
        print(f"  {outlier['request_id']}: ${outlier['cost_usd']:.4f}")
```

## Model Routing: Cheap vs. Smart

Not every query needs your best (and most expensive) model. Route based on difficulty.

```python
# routing/model_router.py
from typing import Optional
import anthropic
from enum import Enum

class ModelTier(Enum):
    FAST = "claude-3-5-haiku-20241022"        # $0.80/$4 per 1M tokens
    BALANCED = "claude-3-5-sonnet-20241022"   # $3/$15 per 1M tokens
    SMART = "claude-3-opus-20250219"          # $15/$60 per 1M tokens

class ModelRouter:
    """
    Route queries to appropriate model based on difficulty.
    Saves cost while maintaining quality.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def classify_difficulty(self, query: str) -> str:
        """
        Classify query as easy, medium, or hard.
        This is a fast classifier model call.
        """
        response = self.client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=10,
            messages=[{
                "role": "user",
                "content": f"""Classify this query as EASY, MEDIUM, or HARD.
                
EASY = factual lookup, no reasoning
MEDIUM = requires some reasoning or multi-step
HARD = complex reasoning, multiple sources, edge cases

Query: {query}

Respond with just: EASY, MEDIUM, or HARD"""
            }]
        )
        
        classification = response.content[0].text.strip().upper()
        return classification
    
    def select_model(self, query: str) -> str:
        """
        Route to appropriate model based on difficulty.
        """
        difficulty = self.classify_difficulty(query)
        
        routing_table = {
            "EASY": ModelTier.FAST.value,
            "MEDIUM": ModelTier.BALANCED.value,
            "HARD": ModelTier.SMART.value
        }
        
        model = routing_table.get(difficulty, ModelTier.BALANCED.value)
        
        return model
    
    def estimate_cost(
        self,
        query: str,
        expected_input_tokens: int = 2000,
        expected_output_tokens: int = 500
    ) -> Dict[str, float]:
        """
        Estimate cost for different models on this query.
        """
        model = self.select_model(query)
        
        # Pricing per 1M tokens (as of 2026)
        pricing = {
            ModelTier.FAST.value: {
                "input": 0.80,
                "output": 4.00
            },
            ModelTier.BALANCED.value: {
                "input": 3.00,
                "output": 15.00
            },
            ModelTier.SMART.value: {
                "input": 15.00,
                "output": 60.00
            }
        }
        
        costs = {}
        for tier, price_map in pricing.items():
            input_cost = (expected_input_tokens / 1_000_000) * price_map["input"]
            output_cost = (expected_output_tokens / 1_000_000) * price_map["output"]
            costs[tier] = input_cost + output_cost
        
        return costs

# Usage
router = ModelRouter()

query = "What's the weather in San Francisco?"
model = router.select_model(query)
print(f"Route to: {model}")

costs = router.estimate_cost(query)
print("\nCost estimates:")
for tier, cost in costs.items():
    print(f"  {tier}: ${cost:.4f}")
```

## Semantic Caching: Don't Repeat Expensive Calls

If you've already answered a question, don't ask again. Semantic caching understands that "What's my balance?" and "How much is in my account?" are the same.

```python
# caching/semantic_cache.py
import anthropic
from typing import Optional, Tuple
import hashlib

class SemanticCache:
    """
    Cache LLM responses using semantic similarity.
    Different phrasings of the same question get the same answer.
    """
    
    def __init__(self, similarity_threshold: float = 0.95):
        self.client = anthropic.Anthropic()
        self.similarity_threshold = similarity_threshold
        self.cache_store = {}  # {query_hash: (query, response)}
    
    def get_cached_response(self, user_query: str) -> Optional[str]:
        """
        Check if we've answered a similar question before.
        """
        for cached_query, cached_response in self.cache_store.values():
            similarity = self._compute_similarity(user_query, cached_query)
            
            if similarity > self.similarity_threshold:
                # Found a match
                return cached_response
        
        return None
    
    def _compute_similarity(self, query_a: str, query_b: str) -> float:
        """
        Use embeddings to compute semantic similarity.
        Real implementation: use embedding API (OpenAI, Anthropic, etc.)
        """
        # Placeholder: simple string similarity
        common_tokens = set(query_a.lower().split()) & set(query_b.lower().split())
        all_tokens = set(query_a.lower().split()) | set(query_b.lower().split())
        return len(common_tokens) / len(all_tokens) if all_tokens else 0
    
    def cache_response(self, query: str, response: str):
        """Store response for future cache hits."""
        query_hash = hashlib.md5(query.encode()).hexdigest()
        self.cache_store[query_hash] = (query, response)
    
    def invalidate_if_stale(self, query: str, max_age_hours: int = 24):
        """
        Remove cached response if it's too old.
        Some information changes: stock prices, weather, account balances.
        """
        # Track creation time of cached responses
        # If > max_age_hours old, remove
        pass

# Usage in agent
cache = SemanticCache(similarity_threshold=0.95)

def agent_handler(user_query: str) -> str:
    # Check cache first
    cached = cache.get_cached_response(user_query)
    if cached:
        return cached
    
    # Not cached, run agent
    response = agent.run(user_query)
    
    # Cache for future
    cache.cache_response(user_query, response)
    
    return response
```

## Drift Detection: Output Quality Degrading

Your agent was working yesterday. Today, something changed. Maybe the model got updated. Maybe your data changed. Drift detection catches this automatically.

```python
# monitoring/drift_detection.py
import numpy as np
from typing import List, Dict
from datetime import datetime, timedelta

class DriftDetector:
    """
    Detect when agent output quality degrades over time.
    Uses statistical methods to identify shifts in behavior.
    """
    
    def __init__(self, baseline_window_days: int = 7):
        self.baseline_window = baseline_window_days
        self.baseline_metrics = None
    
    def compute_baseline(self, metrics_history: List[Dict]) -> Dict[str, float]:
        """
        Compute baseline metrics from clean period.
        Run this on data before you deploy, to establish normal behavior.
        """
        # Filter to last N days
        cutoff = datetime.utcnow() - timedelta(days=self.baseline_window)
        recent = [m for m in metrics_history if m["timestamp"] > cutoff]
        
        baseline = {
            "success_rate_mean": np.mean([m["success_rate"] for m in recent]),
            "success_rate_std": np.std([m["success_rate"] for m in recent]),
            "latency_p99_mean": np.mean([m["latency_p99"] for m in recent]),
            "latency_p99_std": np.std([m["latency_p99"] for m in recent]),
            "cost_per_query_mean": np.mean([m["cost_per_query"] for m in recent]),
            "cost_per_query_std": np.std([m["cost_per_query"] for m in recent]),
        }
        
        self.baseline_metrics = baseline
        return baseline
    
    def detect_drift(
        self,
        recent_metrics: List[Dict],
        z_score_threshold: float = 3.0
    ) -> Dict[str, bool]:
        """
        Use Z-score test to detect if recent metrics deviate from baseline.
        Z-score of 3 = ~99.7% confidence something changed.
        """
        if not self.baseline_metrics:
            raise ValueError("Call compute_baseline() first")
        
        recent_mean_success = np.mean([m["success_rate"] for m in recent_metrics])
        recent_mean_latency = np.mean([m["latency_p99"] for m in recent_metrics])
        recent_mean_cost = np.mean([m["cost_per_query"] for m in recent_metrics])
        
        drifts = {}
        
        # Z-score for success rate
        z_success = (
            (recent_mean_success - self.baseline_metrics["success_rate_mean"]) /
            (self.baseline_metrics["success_rate_std"] + 0.001)  # Avoid division by zero
        )
        drifts["success_rate_drifted"] = abs(z_success) > z_score_threshold
        
        # Z-score for latency
        z_latency = (
            (recent_mean_latency - self.baseline_metrics["latency_p99_mean"]) /
            (self.baseline_metrics["latency_p99_std"] + 1.0)
        )
        drifts["latency_drifted"] = abs(z_latency) > z_score_threshold
        
        # Z-score for cost
        z_cost = (
            (recent_mean_cost - self.baseline_metrics["cost_per_query_mean"]) /
            (self.baseline_metrics["cost_per_query_std"] + 0.0001)
        )
        drifts["cost_drifted"] = abs(z_cost) > z_score_threshold
        
        return drifts

# Usage
detector = DriftDetector(baseline_window_days=7)

# Compute baseline from stable period
baseline = detector.compute_baseline(metrics_from_last_month)
print("Baseline metrics established")

# Every hour, check for drift
@schedule_hourly
def check_drift():
    recent_hour_metrics = fetch_metrics_from_last_hour()
    drifts = detector.detect_drift(recent_hour_metrics)
    
    if any(drifts.values()):
        alert("Drift detected", drifts)
```

## Alerting: What Wakes You Up at 2am

Not all problems are equal. Some need immediate attention. Others can wait for business hours.

```python
# monitoring/alerting.py
from enum import Enum
from typing import Callable

class Severity(Enum):
    PAGE = "page"      # Wake up now (PagerDuty)
    URGENT = "urgent"  # High priority ticket
    WARNING = "warning"  # Log and monitor
    INFO = "info"      # Note for later

class AlertRule:
    """A single alerting rule."""
    
    def __init__(
        self,
        name: str,
        condition: Callable[[dict], bool],  # When to alert
        severity: Severity,
        message: str
    ):
        self.name = name
        self.condition = condition
        self.severity = severity
        self.message = message

# Define alerting rules for agent system
ALERT_RULES = [
    # CRITICAL: Success rate collapsed
    AlertRule(
        name="success_rate_critical",
        condition=lambda m: m["success_rate"] < 0.50,
        severity=Severity.PAGE,
        message="Success rate <50%! Agent is broken."
    ),
    
    # CRITICAL: Cost exploded
    AlertRule(
        name="cost_anomaly",
        condition=lambda m: m["cost_per_query"] > m.get("cost_baseline", 1.0) * 5,
        severity=Severity.PAGE,
        message="Cost per query 5x normal. Check for infinite loops."
    ),
    
    # URGENT: Latency degradation
    AlertRule(
        name="latency_degradation",
        condition=lambda m: m["latency_p99"] > 30000,  # 30 seconds
        severity=Severity.URGENT,
        message="P99 latency >30s. Performance degraded."
    ),
    
    # WARNING: Error rate rising
    AlertRule(
        name="error_rate_rising",
        condition=lambda m: m["error_rate"] > 0.10,
        severity=Severity.WARNING,
        message="Error rate >10%. Monitor for issues."
    ),
    
    # WARNING: Model tokens increasing
    AlertRule(
        name="token_inflation",
        condition=lambda m: m["tokens_per_query"] > m.get("token_baseline", 2000) * 1.3,
        severity=Severity.WARNING,
        message="Tokens per query increased 30%. Prompts getting longer?"
    ),
    
    # INFO: Cache hit rate declining
    AlertRule(
        name="cache_hit_declining",
        condition=lambda m: m["cache_hit_rate"] < 0.20,
        severity=Severity.INFO,
        message="Cache hit rate <20%. Consider cache strategy."
    ),
]

def evaluate_alerts(current_metrics: dict) -> list:
    """Evaluate all alert rules against current metrics."""
    triggered = []
    
    for rule in ALERT_RULES:
        try:
            if rule.condition(current_metrics):
                triggered.append({
                    "rule_name": rule.name,
                    "severity": rule.severity,
                    "message": rule.message
                })
        except Exception as e:
            logger.error(f"Alert rule {rule.name} failed: {e}")
    
    return triggered

@schedule_every_minute
def alert_monitor():
    current_metrics = fetch_current_metrics()
    triggered_alerts = evaluate_alerts(current_metrics)
    
    for alert in triggered_alerts:
        if alert["severity"] == Severity.PAGE:
            # PagerDuty
            send_to_pagerduty(alert)
        elif alert["severity"] == Severity.URGENT:
            # Create ticket
            create_jira_ticket(alert)
        elif alert["severity"] == Severity.WARNING:
            # Log warning
            logger.warning(alert["message"])
        else:
            # Just log
            logger.info(alert["message"])
```

## Governance: Access, Data, Compliance

In regulated industries (finance, healthcare, legal), you need more than observability. You need accountability.

```python
# governance/access_control.py
from enum import Enum
from typing import Optional

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

class AccessLog:
    """
    Log every agent action that touches data.
    Who accessed what, when, why?
    """
    
    def __init__(self, storage_backend):
        self.backend = storage_backend
    
    def log_access(
        self,
        user_id: str,
        agent_name: str,
        action: str,  # "read", "write", "delete"
        resource_type: str,  # "customer_record", "transaction", etc.
        resource_id: str,
        classification: DataClassification,
        approved: bool,
        reason: Optional[str] = None
    ):
        """
        Immutable log entry for compliance.
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "agent_name": agent_name,
            "action": action,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "classification": classification.value,
            "approved": approved,
            "reason": reason
        }
        
        # Write to immutable log (cannot be deleted/modified)
        self.backend.write_immutable(entry)
        
        if not approved:
            # Alert if access denied
            logger.warning(f"Access denied: {user_id} tried {action} on {resource_id}")

class ComplianceChecker:
    """
    Enforce data access policies.
    """
    
    def __init__(self, policy_engine):
        self.policy_engine = policy_engine
    
    def can_access(
        self,
        user_id: str,
        resource_id: str,
        resource_type: str,
        action: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if user is allowed to access resource.
        Returns (allowed, reason_if_denied)
        """
        # Check role-based access control
        user_role = self.policy_engine.get_user_role(user_id)
        
        # Check if action allowed for this role on this resource type
        allowed = self.policy_engine.check_permission(
            role=user_role,
            resource_type=resource_type,
            action=action
        )
        
        if not allowed:
            return False, f"User role {user_role} not permitted {action} on {resource_type}"
        
        # Check if resource is restricted to specific users/teams
        owner = self.policy_engine.get_resource_owner(resource_id)
        if owner != user_id and user_role != "admin":
            return False, f"Resource {resource_id} restricted to owner {owner}"
        
        return True, None

# Usage
access_log = AccessLog(storage_backend=postgres)
compliance = ComplianceChecker(policy_engine=opa_engine)

def agent_read_customer_record(user_id: str, customer_id: str):
    """
    Agent wants to read customer record.
    Check compliance before allowing.
    """
    allowed, denial_reason = compliance.can_access(
        user_id=user_id,
        resource_id=customer_id,
        resource_type="customer_record",
        action="read"
    )
    
    access_log.log_access(
        user_id=user_id,
        agent_name="support_agent",
        action="read",
        resource_type="customer_record",
        resource_id=customer_id,
        classification=DataClassification.CONFIDENTIAL,
        approved=allowed,
        reason=denial_reason
    )
    
    if not allowed:
        raise PermissionError(denial_reason)
    
    return fetch_customer_record(customer_id)
```

## Checklist: Before Going Live

- [ ] Traces/spans defined: every critical path is instrumented
- [ ] Structured logging schema: consistent JSON logging
- [ ] Dashboard created: can operators understand system health?
- [ ] Cost attribution working: can you see where money goes?
- [ ] Model routing implemented: cheap queries use cheap models
- [ ] Alerting rules defined: who gets notified when?
- [ ] Baseline metrics captured: you know what "normal" looks like
- [ ] Drift detection configured: early warning system active
- [ ] Caching strategy: high-value queries cached to save cost
- [ ] Compliance logging: audit trail for regulated data

You cannot improve what you cannot see. Build observability first.
