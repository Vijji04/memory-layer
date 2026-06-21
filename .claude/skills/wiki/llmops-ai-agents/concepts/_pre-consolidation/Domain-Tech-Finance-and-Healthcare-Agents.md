---
title: Domain: Tech, Finance, and Healthcare Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, domains, tech, finance, healthcare, case-studies]
confidence: high
source_files: 3
---

# Domain: Tech, Finance, and Healthcare Agents

> Consolidated from 3 source files.

---

## Tech / Software Engineering: Building Agent Systems for Code, Trust, and Scale

## Domain Constraints

Software engineering is uniquely hostile to agent error. You're not just delivering wrong information — you're shipping broken code, corrupting git history, breaking CI/CD pipelines, or introducing security vulnerabilities that hit production in minutes.

**The core constraints:**
- **Code correctness is non-negotiable.** A 99% correct code change is 100% broken. This forces us toward deterministic output, heavy test coverage integration, and bounded autonomy.
- **Developer trust is earned through observability.** Engineers don't blindly trust AI. They need to see the reasoning chain, understand why a refactor happened, and manually review every step.
- **Security moves at every layer.** Dependencies, secrets, supply chain vulnerabilities. An agent that deploys code without checking for exposed API keys is a liability.
- **Platform economics matter.** 200-person teams can't afford per-dev-per-month costs for agentic infrastructure. The platform needs amortization.

---

## Architecture Focus

The pattern across successful tech companies isn't monolithic agents. It's **hierarchical orchestration with human-in-the-loop checkpoints**.

```
┌─────────────────────────────────────────────────┐
│  Agentic Task Router (classifies intent)        │
│  "refactor this function" → lightweight flow    │
│  "audit all S3 bucket configs" → deep audit     │
└──────────────┬──────────────────────────────────┘
               │
        ┌──────┴──────┬──────────┬────────────┐
        │             │          │            │
   ┌────▼───┐  ┌─────▼──┐  ┌──▼─────┐  ┌──▼──────┐
   │ Refactor│  │ Audit  │  │ Generate│  │ Patch  │
   │ Agent   │  │ Agent  │  │ Test    │  │ Agent  │
   └────┬───┘  └────┬───┘  └───┬────┘  └───┬─────┘
        │           │           │            │
        └─────────────────┬──────────────────┘
                          │
                  ┌───────▼────────┐
                  │ Human Approval │
                  │ (IDE or Web)   │
                  └────────────────┘
                          │
                  ┌───────▼────────┐
                  │  Git + Tests   │
                  │  (Auto-run)    │
                  └────────────────┘
```

**Key design principle:** Push observability into every agent. Each agent emits structured spans (via OpenTelemetry or Traces) that show:
- What the agent decided to change
- Why it made that decision
- Test results before human review
- Roll-back plans if something breaks

---

## Case Studies: Architecture + Design Decisions

### 1. Notion — Hierarchical Orchestration with 4-5 Rebuilds

**The Problem:** Notion's AI assistance needed to understand user intent in a deeply nested information architecture (databases → properties → rollups → formulas). A single "refactor workspace" instruction could affect thousands of blocks.

**Architecture Decision:**

```typescript
// Notion's orchestration pattern
interface NotionAgentic {
  intent: {
    type: "refactor" | "migrate" | "optimize-performance"
    scope: "block" | "database" | "workspace"
    constraints: {
      preserveViews: boolean
      backupFirst: boolean
      rollbackWindow: 60000 // 1 min window to undo
    }
  }
  
  pipeline: [
    { stage: "parse", agent: "intent-classifier" },
    { stage: "build", agent: "schema-analyzer", output: "change-graph" },
    { stage: "rebuild", iterations: 4, agent: "diff-validator" },
    { stage: "test", agent: "workspace-simulator" },
    { stage: "approval", type: "human-review" },
    { stage: "deploy", agent: "transactional-applier" }
  ]
}

// The "4-5 rebuilds" pattern: test the change multiple times
// before asking humans to approve it
async function hierarchicalApply(intent: NotionAgentic) {
  let changeGraph = await parseAndBuild(intent)
  
  // Rebuild #1: Detect breaking changes
  let breaking = await detectBreaking(changeGraph)
  if (breaking.length > 0) {
    changeGraph = await suggestMigration(breaking)
  }
  
  // Rebuild #2: Check referential integrity
  let orphans = await findOrphanedReferences(changeGraph)
  changeGraph = await relink(orphans)
  
  // Rebuild #3: Test on copy
  let testResult = await simulateOnTestCopy(changeGraph)
  if (testResult.failures > 0) {
    changeGraph = await fixFailures(testResult)
  }
  
  // Rebuild #4-5: Optimize performance, check permissions
  changeGraph = await optimizeIndexes(changeGraph)
  changeGraph = await addMissingPermissions(changeGraph)
  
  // NOW ask human
  return await presentForApproval(changeGraph)
}
```

**Why This Works:**
- The 4-5 rebuild cycle isn't overengineering. Each rebuild catches a different class of error.
- The "change graph" is immutable and fully traceable. You can see exactly what will change before execution.
- Rollback window is explicit: 60 seconds to undo. Beyond that, you need a more complex recovery.

**What to Learn:** Don't ship refactoring agents that skip the rebuild loop. The cost of rebuilds is cheap (simulator runs in memory). The cost of breaking a user's workspace is infinite.

---

### 2. Union / Flyte — Observable Agentic Systems with Traces and Spans

**The Problem:** ML workflow orchestration requires understanding agent decisions across distributed systems. You need to know: Which agent decided to retry? Why? What data did it see?

**Architecture Decision:**

```python
# Union's observable agent pattern
from dataclasses import dataclass
from opentelemetry import trace, metrics

@dataclass
class AgentDecision:
    agent_id: str
    decision_type: str  # "retry", "fallback", "escalate"
    confidence: float
    evidence: list[str]
    metadata: dict

class ObservableAgent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.tracer = trace.get_tracer(__name__)
        self.meter = metrics.get_meter(__name__)
    
    def decide(self, state: WorkflowState) -> AgentDecision:
        with self.tracer.start_as_current_span(
            f"{self.agent_id}.decide"
        ) as span:
            # Span automatically captures:
            # - start time, end time
            # - exceptions
            # - custom attributes
            
            span.set_attribute("state.id", state.workflow_id)
            span.set_attribute("state.stage", state.current_stage)
            
            decision = self._evaluate(state)
            
            # Log evidence as structured attributes
            for i, evidence in enumerate(decision.evidence):
                span.set_attribute(f"evidence.{i}", evidence)
            
            span.set_attribute("decision.type", decision.decision_type)
            span.set_attribute("decision.confidence", decision.confidence)
            
            # Metric: agent decision distribution
            self.meter.create_counter("agent.decisions").add(
                1,
                {
                    "agent": self.agent_id,
                    "type": decision.decision_type,
                    "confidence": "high" if decision.confidence > 0.8 else "low"
                }
            )
            
            return decision
    
    def _evaluate(self, state: WorkflowState) -> AgentDecision:
        # Actual decision logic
        if state.retry_count > 3:
            return AgentDecision(
                agent_id=self.agent_id,
                decision_type="escalate",
                confidence=0.99,
                evidence=[
                    f"Retried {state.retry_count} times",
                    f"Last error: {state.last_error}",
                    "Threshold exceeded"
                ],
                metadata={"error_pattern": "timeout"}
            )
        return AgentDecision(...)

# Usage: Wire agents into orchestration
class WorkflowOrchestrator:
    def execute(self, workflow: Workflow):
        retry_agent = ObservableAgent("retry-policy")
        fallback_agent = ObservableAgent("fallback-route")
        
        state = initialize_workflow(workflow)
        
        while not state.is_complete():
            stage_result = self.run_stage(state)
            
            if stage_result.failed:
                # Agents make decisions, not humans
                retry_decision = retry_agent.decide(state)
                if retry_decision.decision_type == "escalate":
                    fallback_decision = fallback_agent.decide(state)
                    state = await fallback_decision.execute()
                else:
                    state.retry_count += 1
                    state = await self.run_stage(state)
            else:
                state.advance()
        
        # At the end: full trace available to engineers
        # "Show me why this workflow took 4 retries"
        # Trace shows: agent decisions, confidence, evidence
        return state
```

**Why This Works:**
- Every agent decision is a span. You can query: "Show all decisions where confidence < 0.7"
- Distributed tracing means multi-service workflows show the full decision tree.
- Metrics are automatically aggregated: "retry agent escalates in 2% of cases" — that's actionable.

**What to Learn:** Observable agents > smarter agents. You'll spend 80% of your time debugging. Make that 80% faster by shipping observability from day one.

---

### 3. Slack — Scaling AI Dev Tools to 100K+ Teams

**The Problem:** Building AI assistance that works for a 5-person startup AND a 5000-person enterprise. Cost explodes. Latency explodes. Trust issues multiply.

**Architecture Decision:**

```python
# Slack's cost + latency optimization pattern

class ContextWindowing:
    """Different agents, different window sizes"""
    
    LIGHTWEIGHT = {
        "name": "slash-command-responder",
        "context_window": 4096,  # Fast, cheap
        "cost_per_token": 0.003,
        "p99_latency_ms": 250,
        "use_cases": [
            "Summarize thread",
            "Fix markdown in message",
            "Suggest emoji reaction"
        ]
    }
    
    STANDARD = {
        "name": "code-reviewer",
        "context_window": 16384,
        "cost_per_token": 0.01,
        "p99_latency_ms": 800,
        "use_cases": [
            "Review PR snippet",
            "Explain test failure",
            "Debug error log"
        ]
    }
    
    DEEP = {
        "name": "codebase-architect",
        "context_window": 100000,
        "cost_per_token": 0.05,
        "p99_latency_ms": 5000,
        "use_cases": [
            "Analyze full migration plan",
            "Cross-service refactoring",
            "Architectural decisions"
        ]
    }

class ContextSelector:
    """Route requests to right tier"""
    
    async def select(self, request: SlashCommand) -> str:
        """Classify → pick tier"""
        
        # Tier 1: Can this be answered with lightweight context?
        if self.is_low_complexity(request):
            return "LIGHTWEIGHT"
        
        # Tier 2: Does it need recent conversation?
        if self.needs_thread_context(request):
            return "STANDARD"
        
        # Tier 3: Does it need codebase knowledge?
        if self.needs_repo_context(request):
            return "DEEP"
        
        return "STANDARD"  # default
    
    def is_low_complexity(self, req: SlashCommand) -> bool:
        """Heuristics for routing"""
        complexity_signals = [
            len(req.text) < 100,  # Short request
            not req.mentions_code,
            not req.links_to_issue,
        ]
        return sum(complexity_signals) >= 2

# Cost model: Slack can't afford $0.05/request for 100M requests/day
# Solution: 80% of requests hit lightweight tier
# 19% hit standard tier
# 1% hit deep tier

# Monthly cost calculation
class SlackEconomics:
    def monthly_cost(self, requests_per_day: int):
        lightweight = requests_per_day * 0.80 * 0.003 * 30
        standard = requests_per_day * 0.19 * 0.01 * 30
        deep = requests_per_day * 0.01 * 0.05 * 30
        
        return lightweight + standard + deep

# 100M requests/day example
# Lightweight: 80M * 0.003 = $240K/month
# Standard: 19M * 0.01 = $190K/month
# Deep: 1M * 0.05 = $50K/month
# TOTAL: ~$480K/month
# Per team (500K teams): $1/month = customer acquisition cost

class AdaptiveAgent:
    """Agent that knows its constraints"""
    
    def __init__(self, tier: str):
        self.tier = tier
        self.context_limit = TIERS[tier]["context_window"]
        self.max_latency_ms = TIERS[tier]["p99_latency_ms"]
    
    async def respond(self, message: str, context: list[Message]):
        # Lightweight tier: just answer, no explanation
        if self.tier == "LIGHTWEIGHT":
            return await self.quick_answer(message)
        
        # Standard tier: answer + one follow-up question
        if self.tier == "STANDARD":
            answer = await self.thoughtful_answer(message, context[:10])
            return answer + self.suggest_follow_up(answer)
        
        # Deep tier: full analysis
        if self.tier == "DEEP":
            return await self.comprehensive_analysis(message, context)
```

**Why This Works:**
- Tier system is explicit. Engineers know what they're getting.
- Cost scales sublinearly: most requests are cheap, rare requests are expensive.
- Users don't experience weird behavior ("Why is this sometimes slow?"). They chose the tier.

**What to Learn:** Don't try to build one agent for all use cases. Build a routing layer that maps intent → tier, and let agents be honest about their constraints.

---

### 4. LangChain — Production LLM Engineering Principles

**The Problem:** Framework for building agents that go to production. Not research, not Jupyter notebooks. Real users, real failure modes.

**Architecture Decision:**

```python
# LangChain's "runnable" pattern for production agents

from langchain.schema import Runnable
from typing import Any, Iterator

class ProducibleAgent(Runnable):
    """Agent that can be deployed without rewrites"""
    
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self._validators = []
        self._metrics = {}
    
    def add_input_validator(self, fn: Callable) -> "ProducibleAgent":
        """Input validation is PRODUCTION requirement"""
        self._validators.append(fn)
        return self
    
    def invoke(self, input: dict) -> dict:
        """Single invocation, sync"""
        # Validation BEFORE the agent runs
        for validator in self._validators:
            input = validator(input)
        
        result = self._execute(input)
        
        # Validation AFTER
        result = self._validate_output(result)
        
        return result
    
    def stream(self, input: dict) -> Iterator[dict]:
        """Streaming: agents emit thinking steps"""
        for step in self._execute_streaming(input):
            yield step
    
    def batch(self, inputs: list[dict]) -> list[dict]:
        """Batch: for high-throughput scenarios"""
        return [self.invoke(inp) for inp in inputs]
    
    def _execute(self, input: dict) -> dict:
        """Core agent logic"""
        raise NotImplementedError
    
    def _validate_output(self, result: dict) -> dict:
        """Catch agent hallucinations"""
        if result.get("type") == "code":
            # Security check: no shell exec
            if "subprocess" in result.get("code", ""):
                raise ValueError("Subprocess not allowed")
        
        return result

# Example: Code review agent
class CodeReviewAgent(ProducibleAgent):
    def __init__(self):
        super().__init__("code-reviewer", "1.0")
        
        # Add validators
        self.add_input_validator(self._validate_pr)
        self.add_input_validator(self._validate_diff_size)
    
    def _validate_pr(self, input: dict) -> dict:
        if "pr_id" not in input:
            raise ValueError("pr_id required")
        if "repo" not in input:
            raise ValueError("repo required")
        return input
    
    def _validate_diff_size(self, input: dict) -> dict:
        diff = input.get("diff", "")
        if len(diff) > 50000:
            # Too large: agent might lose context
            raise ValueError("Diff too large (>50KB)")
        return input
    
    def _execute(self, input: dict) -> dict:
        pr_id = input["pr_id"]
        diff = input["diff"]
        
        # Step 1: Parse diff
        files_changed = self._parse_diff(diff)
        
        # Step 2: Identify risky patterns
        concerns = []
        for file in files_changed:
            if "schema.sql" in file.name:
                concerns.append(f"Database migration: {file.name}")
            if file.has_security_concern():
                concerns.append(f"Security risk in {file.name}")
        
        # Step 3: Generate review
        review = {
            "pr_id": pr_id,
            "decision": "request_changes" if concerns else "approve",
            "concerns": concerns,
            "checklist": [
                {"item": "Tests added", "status": self._has_tests(diff)},
                {"item": "No hardcoded secrets", "status": self._no_secrets(diff)},
                {"item": "Backward compatible", "status": self._is_compatible(diff)},
            ]
        }
        
        return review

# Production deployment
def deploy_agent(agent: ProducibleAgent):
    """Agents can move between sync/async/batch without rewrites"""
    
    # As FastAPI endpoint
    app.post(f"/agents/{agent.name}")
    async def endpoint(input: dict):
        return await asyncio.to_thread(agent.invoke, input)
    
    # As background job
    celery.task(name=f"agent.{agent.name}")
    def background_job(input: dict):
        return agent.invoke(input)
    
    # As streaming endpoint
    app.post(f"/agents/{agent.name}/stream")
    async def stream_endpoint(input: dict):
        for step in agent.stream(input):
            yield json.dumps(step) + "\n"
```

**Why This Works:**
- The Runnable interface is the contract. Agents don't know if they're being called via HTTP, Celery, or directly.
- Validators are explicit. You can't forget to validate input because it's part of the interface.
- Streaming matters for UX. Users see the agent thinking instead of waiting 10 seconds.

**What to Learn:** A production agent is not a prompt. It's a validated, composable, multi-deployment interface. Build that from day 1.

---

### 5. Opendev — Terminal-Native Agent with 54% Context Reduction

**The Problem:** Developers live in terminals. Asking them to switch to a web UI to interact with an agent is friction. Also: LLM context is expensive. How do you run an agent on limited context?

**Architecture Decision:**

```bash
# Opendev's terminal-native pattern
# Installation: brew install opendev (or npm install -g opendev)

# Usage: agent is part of your shell
$ opendev "add error handling to this file"

# Agent runs in terminal, asks clarifying questions
# > Which function needs error handling? (multiple choice)
# > Should we use try-catch or Result type? (radio buttons)
# > Generate tests too? (y/n)

# Then: agent shows diff, asks approval, runs git add + commit

# Architecture: Context reduction through staged reasoning

class TerminalAgent:
    """Low-context agent that asks clarifying questions"""
    
    def __init__(self):
        self.max_context_tokens = 4096  # Cheap, fast
        self.stages = [
            "clarify",      # Ask questions to narrow scope
            "analyze",      # Read only relevant files
            "plan",         # Show plan before execution
            "execute",      # Apply changes
            "test",         # Run tests
            "commit",       # Ask user before committing
        ]
    
    async def handle(self, command: str):
        # Stage 1: Clarify intent with minimal context
        clarifications = await self.clarify(command)
        
        # User answers: "add error handling to auth.ts"
        # Now we KNOW the scope
        
        # Stage 2: Read only auth.ts (not whole codebase)
        relevant_files = await self.find_relevant(clarifications)
        
        # Still under token budget: auth.ts (200 lines) + imports
        
        # Stage 3: Show plan
        plan = await self.plan(relevant_files, clarifications)
        print("Plan:")
        for step in plan:
            print(f"  [ ] {step}")
        
        approved = await self.confirm("Proceed? (y/n)")
        if not approved:
            return
        
        # Stage 4-6: Execute with full context (now we know we need it)
        changes = await self.execute(relevant_files, plan)
        test_result = await self.test(changes)
        
        await self.commit(changes, test_result)
    
    async def clarify(self, command: str) -> dict:
        """Use minimal tokens to ask questions"""
        
        # Classify intent: add_feature, fix_bug, refactor, optimize
        intent = await self.classify(command)
        
        # Ask targeted questions
        if intent == "add_feature":
            questions = [
                "What's the feature name?",
                "Which module does it belong in?",
                "Add tests?",
            ]
        elif intent == "fix_bug":
            questions = [
                "What's broken?",
                "Where is the bug?",
                "Do you have a reproduction?",
            ]
        
        # Show UI: interactive prompts
        answers = await self.interactive_prompt(questions)
        
        return {
            "intent": intent,
            "answers": answers,
            "tokens_used": 150,  # Clarification is cheap
        }
    
    async def find_relevant(self, clarifications: dict) -> list[str]:
        """Smart file selection to stay under token budget"""
        
        answers = clarifications["answers"]
        intent = clarifications["intent"]
        
        # Heuristic: find files mentioned in answers
        files = await self.grep_in_repo(answers["target_module"])
        
        # Also find imports
        imports = await self.follow_imports(files)
        
        # Token estimate
        total_tokens = sum(
            len(f) // 4  # rough estimate: 4 chars per token
            for f in files + imports
        )
        
        if total_tokens > 3500:
            # Too many! Narrow further
            files = files[:5]  # Keep only most relevant
        
        return files
```

**Why This Works:**
- Terminal is the developer's native context. Minimize friction.
- Staged reasoning: cheap clarification reduces expensive analysis.
- 54% context reduction comes from "not analyzing the whole repo". Ask what you need first.

**What to Learn:** Context is a finite resource. Use it wisely: clarify intent cheap, then spend context tokens on what matters.

---

### 6. Forward-Deployed Engineering (OpenAI) + Zero-Code Harness Pattern

**The Problem:** Enterprise customers want custom agents, but don't want to pay for custom software engineers to build them. How do you make agents customizable without engineering?

**Architecture Decision:**

```python
# Zero-code agent harness pattern
# Inspired by OpenAI's forward-deployed engineering practice

@dataclass
class AgentHarness:
    """No code needed: configuration only"""
    
    name: str
    system_prompt: str  # The entire agent logic
    tools: list[str]    # Which actions can the agent take?
    constraints: dict   # Guardrails
    data_sources: list[str]  # Where does it read from?

# Example: Customer success agent
CUSTOMER_SUCCESS_AGENT = AgentHarness(
    name="customer-success",
    
    system_prompt="""
You are a customer success agent. Your job is to:
1. Respond to customer emails within 30 minutes
2. Route complex issues to humans
3. Suggest upsells based on usage

CONSTRAINTS:
- You can NEVER promise features not in our roadmap
- You can NEVER offer discounts > 10%
- You can NEVER commit to timeline without checking team availability

ROUTING RULES:
- If customer is angry (tone analysis): escalate to manager
- If problem is in 'known_issues.md': follow the fix
- If problem is not in knowledge base: escalate
    """,
    
    tools=[
        "read_email",
        "send_email",
        "query_customer_db",
        "check_roadmap",
        "escalate_to_human",
    ],
    
    constraints={
        "max_discount_percent": 10,
        "max_response_time_minutes": 30,
        "escalation_keywords": [
            "lawsuit",
            "regulatory",
            "security breach",
        ],
        "knowledge_base": "docs/known_issues.md",
    },
    
    data_sources=[
        "customer_db",
        "email_inbox",
        "roadmap.yaml",
    ],
)

# Deployment: zero custom code
class ZeroCodeDeployment:
    """Harness deploys without engineer involvement"""
    
    def deploy(self, harness: AgentHarness):
        # Generate agent from config
        agent = self.generate_agent(harness)
        
        # Wire up tools to data sources
        for tool_name in harness.tools:
            tool_config = self.load_tool_config(tool_name, harness)
            agent.register_tool(tool_name, tool_config)
        
        # Add guardrails
        agent.add_guardrail(
            name="discount_check",
            rule=f"discount <= {harness.constraints['max_discount_percent']}"
        )
        
        agent.add_guardrail(
            name="escalation_check",
            rule=f"escalate if message contains: {harness.constraints['escalation_keywords']}"
        )
        
        # Deploy
        return self.deploy_to_production(agent)

# What a customer changes without engineering:
# 1. System prompt: "Be more friendly" vs "Be direct"
# 2. Tools: Add/remove actions
# 3. Constraints: "max_discount_percent": 15
# 4. Data sources: "Connect to Salesforce instead of customer_db"

# What requires engineering:
# 1. Adding a NEW tool type (beyond the library)
# 2. Custom business logic beyond config
# 3. New guardrails beyond standard rules

# Result: Forward-deployed engineer spends 5 hours on setup
# Customer spends 20 minutes on configuration
# Updates happen daily, not quarterly
```

**Why This Works:**
- Config-first architecture means customers control their agent without engineering bottleneck.
- Constraints are explicit and checked before the agent even runs.
- Tools are composable: mix and match from a library.

**What to Learn:** Enterprise agents need to be customizable but safe. Build a harness that lets customers change behavior without touching code, then make guardrails part of the deployment contract.

---

## Key Design Question

**If you were designing agent infrastructure for a 200-person eng team, what would the shared platform look like?**

My answer:

```python
class EngineeringTeamPlatform:
    """Shared infrastructure for 200-person eng team"""
    
    def __init__(self):
        self.components = {
            # 1. Intent classification layer
            # Maps user command → lightweight/standard/deep tier
            "router": IntentRouter(),
            
            # 2. Agent library (pre-built, tested, audited)
            "agents": {
                "code_reviewer": CodeReviewAgent(),
                "test_generator": TestAgent(),
                "refactorer": RefactorAgent(),
                "security_auditor": SecurityAgent(),
                "documentation": DocAgent(),
            },
            
            # 3. Shared tools (secure, cached, fast)
            "tools": {
                "git": GitTool(cache=True),
                "codebase": CodebaseTool(index=True),
                "ci_cd": CICDTool(),
                "security_db": SecurityTooling(),
            },
            
            # 4. Observability (not an afterthought)
            "tracing": TracingBackend(),  # All decisions logged
            "metrics": MetricsBackend(),  # Agents tracked
            "alerting": AlertingBackend(),  # Failures trigger pages
            
            # 5. Guardrails (per team, per agent)
            "guardrails": GuardrailEngine(),
            
            # 6. Human-in-the-loop UI
            "approval": ApprovalUI(),  # Web + IDE plugin
        }
    
    def provision_team(self, team: Team):
        """Set up agents for a team"""
        
        # 1. Pick which agents they need
        team.agents = [
            self.agents["code_reviewer"],
            self.agents["test_generator"],
        ]
        
        # 2. Configure guardrails
        team.guardrails = {
            "can_commit_to_main": False,  # PR only
            "max_files_per_change": 10,
            "must_have_tests": True,
        }
        
        # 3. Set approval thresholds
        team.approval_thresholds = {
            "refactor_up_to_5_files": "auto",  # Self-approve
            "refactor_5_plus_files": "tech_lead",
            "schema_changes": "architect",
            "security_changes": "security_team",
        }
        
        # 4. Wire to tools
        team.tools = self.tools  # Shared cache, shared cost
        
        # 5. Enable observability
        team.traces = self.tracing.create_workspace(team.id)
        
        return team
```

**The platform's value:**

1. **Amortized cost:** Tools cached and shared. 200 people × cost reduction = sustainable.
2. **Trust through transparency:** All decisions traced. Engineers trust what they can see.
3. **Guardrails prevent catastrophe:** Wrong agents can't run on main branch.
4. **Human approval is fast:** Not blocking anything, but visible when needed.
5. **Learning:** Each team learns from other teams' traces.

---

## Cross-Domain Lessons

1. **Observability is non-negotiable in software.**
   - Every agent decision is a span.
   - Every span is queryable.
   - You debug by tracing, not by guessing.

2. **Context is a finite resource.**
   - Classify intent early and narrow the context window.
   - Don't analyze the whole repo. Ask what's relevant first.

3. **Deterministic > smart.**
   - A dumb agent that follows guardrails is more valuable than a smart agent that hallucinates.
   - Make guardrails part of the agent's DNA, not a wrapper.

4. **Humans aren't slow; friction is slow.**
   - Approval that takes 3 seconds is better than 3 minutes.
   - Terminal UI > web UI for developers.
   - Show diffs before asking for approval.

5. **Cost scales superlinearly with capability.**
   - Lightweight agents are 10x cheaper than deep analysis.
   - Route intelligently or go broke.

---

## Finance / FinTech: Agents That Move Money (Safely)

## Domain Constraints

Finance is the only domain where agent mistakes directly cost people money. Not metaphorically. Literally.

**The immutable constraints:**

- **Regulatory compliance is not a feature; it's the law.** Every transaction touches 3-4 regulatory regimes (AML, CFT, sanctions, PCI-DSS). An agent that violates any of them has exposed the company to fines measured in billions.
- **Audit trails are evidence.** When regulators ask "why did you move $500K to this account?", the answer can't be "the agent decided to". You need a complete chain: human request → agent decision (with reasoning) → system action → verification.
- **Fraud risk compounds with agent capability.** If your agent can move money, fraudsters will find ways to trick it. Social engineering, prompt injection, exploitation of edge cases.
- **Real-time requirements + safety are in tension.** Instant settlement is a competitive advantage. But instant + safe is hard. You can't take 48 hours to audit a transaction.

---

## Architecture Focus

The pattern across fintech companies isn't "faster agents". It's **defense-in-depth with automated rollback**.

```
┌─────────────────────────────────────────────────────────────┐
│ User Intent (API request with auth + context)              │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────▼───────────────┐
         │ Pre-flight Checks             │
         │ - Authentication (OAuth)      │
         │ - Account ownership verified  │
         │ - Velocity limits             │
         │ - Sanctions screening         │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │ Agent (narrow scope)          │
         │ - Validate recipient          │
         │ - Check daily limits          │
         │ - Verify amount matches user  │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │ Deterministic Rules Engine    │
         │ - Scenario: domestic transfer │
         │   → 0.1% reserve, auto-clear  │
         │ - Scenario: intl transfer     │
         │   → 2% reserve, manual audit  │
         │ - Scenario: unusual pattern   │
         │   → Escalate + HOLD           │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │ Post-Flight Verification      │
         │ - Did money actually move?    │
         │ - Does account math check out?│
         │ - Log to audit system         │
         └───────────────┬───────────────┘
                         │
         ┌───────────────▼───────────────┐
         │ Automated Rollback (if needed)│
         │ - Detect anomaly in next 60s  │
         │ - Reverse transaction         │
         │ - Notify user + compliance    │
         └───────────────────────────────┘
```

**Key insight:** The agent is a thin slice in a thick sandwich of verification. The agent is not the point; safety is.

---

## Case Studies: Architecture + Design Decisions

### 1. Stripe — Agentic Commerce Infrastructure

**The Problem:** Stripe serves millions of merchants. They need AI assistance with reconciliation, fraud detection, dispute resolution. But Stripe's liability means: one bad agent decision = millions in exposure.

**Architecture Decision:**

```python
# Stripe's "read-only then action" pattern

from dataclasses import dataclass
from enum import Enum

class TransactionRisk(Enum):
    LOW = 0.1       # Typical transaction
    MEDIUM = 0.5    # Unusual but plausible
    HIGH = 0.9      # Likely fraud
    BLOCKED = 1.0   # Agent cannot act

@dataclass
class FinanceAction:
    type: str  # "refund", "chargeback_response", "reconcile"
    amount: float
    metadata: dict
    requires_human: bool
    risk_level: TransactionRisk

class StripeSafeAgent:
    """Agent for commerce decisions"""
    
    def __init__(self):
        self.rules_engine = DeterministicRules()
        self.fraud_detector = AnomalyDetector()
        self.audit_logger = AuditLog()
    
    async def handle_dispute(self, dispute: Dispute) -> FinanceAction:
        """Dispute = customer says "I didn't authorize this charge"
        
        Agent's job: read the evidence and suggest action
        Agent's constraint: cannot execute; can only recommend
        """
        
        # Phase 1: READ ONLY - Gather intelligence
        evidence = await self.gather_evidence(dispute)
        
        evidence_summary = {
            "transaction": await self.get_transaction(dispute.transaction_id),
            "merchant_history": await self.get_merchant_risk_profile(
                dispute.merchant_id
            ),
            "customer_history": await self.get_customer_risk_profile(
                dispute.customer_id
            ),
            "chargeback_history": await self.get_chargeback_patterns(
                dispute.merchant_id
            ),
            "fraud_score": await self.fraud_detector.score(
                dispute.transaction_id
            ),
        }
        
        # Phase 2: REASONING - Agent analyzes evidence
        analysis = await self.analyze_dispute(evidence_summary)
        
        # This is where the agent lives: analyzing signals, not executing
        
        # Phase 3: RECOMMENDATION - What should a human decide?
        action = self.recommend_action(analysis, evidence_summary)
        
        # Phase 4: VERIFICATION - Before returning, check guardrails
        action = self.verify_action(action, dispute)
        
        # Audit log: Full decision trail
        await self.audit_logger.log({
            "dispute_id": dispute.id,
            "evidence": evidence_summary,
            "analysis": analysis,
            "recommendation": action,
            "timestamp": now(),
        })
        
        return action
    
    def recommend_action(self, analysis: dict, evidence: dict) -> FinanceAction:
        """Recommend action based on evidence + rules"""
        
        fraud_score = evidence["fraud_score"]
        merchant_risk = evidence["merchant_history"]["risk_level"]
        customer_risk = evidence["customer_history"]["risk_level"]
        
        # Deterministic rules: no magic thresholds
        if fraud_score > 0.95:
            return FinanceAction(
                type="issue_credit",
                amount=evidence["transaction"]["amount"],
                metadata={
                    "reason": "Fraud score exceeded threshold",
                    "score": fraud_score,
                },
                requires_human=True,  # Human always required for credit
                risk_level=TransactionRisk.LOW,  # Safe decision
            )
        
        if merchant_risk == "VERY_HIGH" and customer_risk == "LOW":
            return FinanceAction(
                type="investigate",
                amount=0,  # No financial action yet
                metadata={
                    "reason": "High-risk merchant + low-risk customer = investigate",
                    "merchant_id": evidence["transaction"]["merchant_id"],
                },
                requires_human=True,
                risk_level=TransactionRisk.MEDIUM,
            )
        
        # Default: neutral
        return FinanceAction(
            type="request_evidence",
            amount=0,
            metadata={
                "reason": "Insufficient signal. Request more from merchant.",
            },
            requires_human=True,
            risk_level=TransactionRisk.MEDIUM,
        )
    
    def verify_action(self, action: FinanceAction, dispute: Dispute) -> FinanceAction:
        """Guardrails: before we return, verify this is safe"""
        
        # Guardrail 1: Amount sanity check
        if action.amount > 1000000:  # $1M cap
            action.requires_human = True
            action.risk_level = TransactionRisk.HIGH
        
        # Guardrail 2: If recommendation is "credit", ALWAYS human approval
        if action.type in ["issue_credit", "full_refund"]:
            action.requires_human = True
        
        # Guardrail 3: If merchant is blocked, no action
        if self.rules_engine.is_merchant_blocked(dispute.merchant_id):
            action.type = "no_action"
            action.requires_human = True
        
        return action
    
    async def gather_evidence(self, dispute: Dispute) -> dict:
        """Read-only phase: no side effects"""
        
        # All queries are read-only SELECTs
        # No JOINs to avoid phantom reads
        # No mutations
        
        return {
            "transaction": await db.query(
                "SELECT * FROM transactions WHERE id = ?",
                dispute.transaction_id
            ),
            "merchant": await db.query(
                "SELECT * FROM merchants WHERE id = ?",
                dispute.merchant_id
            ),
            "disputes_by_merchant": await db.query(
                "SELECT COUNT(*) FROM disputes WHERE merchant_id = ?",
                dispute.merchant_id
            ),
        }

# Deployment: Audit trail is primary
class DisputeDecisionAudit:
    """Every decision is recorded forever"""
    
    async def log_decision(self, decision: FinanceAction, dispute: Dispute):
        # Write to immutable audit log
        audit_entry = {
            "timestamp": now(),
            "dispute_id": dispute.id,
            "action_type": decision.type,
            "action_amount": decision.amount,
            "requires_human": decision.requires_human,
            "risk_level": decision.risk_level,
            "reasoning": decision.metadata,
            # Critical: Who authorized this decision?
            "authorized_by": "stripe_dispute_agent_v3",
            "agent_version": "3.2.1",
            "model": "gpt-4-0125-preview",
        }
        
        # Write to tamper-proof log
        await self.immutable_log.append(audit_entry)
        
        # If human approval is needed, also log that
        if decision.requires_human:
            # Create task for human reviewer
            await self.task_queue.push({
                "type": "review_dispute_recommendation",
                "dispute_id": dispute.id,
                "recommendation": decision,
            })

# Cost of one dispute
# - Agent analysis: $0.05 (API call + processing)
# - Human review (if needed): $50 (labor)
# - Credit issued: up to $10K (company cost)
# Total liability: $10K+
# Therefore: Agent must be precise, human must be informed
```

**Why This Works:**

- Agent is deliberately passive. It gathers evidence and recommends. Humans execute.
- Every decision is traceable. "Why did we credit $1000?" → pull the dispute record → see evidence → see recommendation → see who approved.
- Guardrails are deterministic. If it's $1M, it's always human, no exceptions.

**What to Learn:** In finance, agents are advisors, not executors. The agent's value is not in speed; it's in consistent analysis that makes human review faster and better-informed.

---

### 2. Coinbase — Multi-Domain Agentic System (Support + Compliance + Dev)

**The Problem:** Coinbase operates at the intersection of:
- **Support domain:** Customers lost funds, need help, impatient.
- **Compliance domain:** Regulators asking why customer was allowed to move $5M.
- **Dev productivity domain:** Engineers need help shipping code without blocking on compliance.

These domains have OPPOSITE incentives. Speed vs. safety. How do you reconcile?

**Architecture Decision:**

```python
# Coinbase's "domain-specific agent" pattern
# Each domain gets its own agent with different constraints

from dataclasses import dataclass
from typing import Literal

@dataclass
class DomainContext:
    domain: Literal["support", "compliance", "dev_productivity"]
    constraints: dict
    audit_requirements: dict
    approval_thresholds: dict

# DOMAIN 1: Customer Support
SUPPORT_CONTEXT = DomainContext(
    domain="support",
    constraints={
        "max_refund_amount": 10000,  # Hard cap
        "max_response_time_seconds": 60,  # Speed matters
        "can_promise_investigation": True,
        "can_create_support_ticket": True,
    },
    audit_requirements={
        "every_decision_logged": True,
        "refunds_above_1000_need_log_reason": True,
    },
    approval_thresholds={
        "refund_under_1000": "auto",
        "refund_1000_to_10000": "human_review",
        "refund_over_10000": "blocked_for_agent",
    }
)

# DOMAIN 2: Compliance
COMPLIANCE_CONTEXT = DomainContext(
    domain="compliance",
    constraints={
        "max_response_time_seconds": None,  # Correctness > speed
        "must_cite_regulation": True,
        "must_show_confidence": True,
        "can_request_investigation": True,
        "cannot_approve_anything": True,  # Compliance agent advises only
    },
    audit_requirements={
        "every_decision_logged": True,
        "must_cite_source_document": True,
        "must_include_confidence_score": True,
    },
    approval_thresholds={
        "everything": "human_review",  # Compliance doesn't auto-approve
    }
)

# DOMAIN 3: Developer Productivity
DEV_CONTEXT = DomainContext(
    domain="dev_productivity",
    constraints={
        "max_response_time_seconds": 5,  # Blocking developer time
        "can_suggest_refactoring": True,
        "can_generate_tests": True,
        "cannot_commit_to_main": True,  # Always PR
        "cannot_bypass_ci_cd": True,
    },
    audit_requirements={
        "every_change_logged": True,
        "every_commit_shows_agent_reasoning": True,
    },
    approval_thresholds={
        "refactoring_small_scope": "auto",  # Trust engineers
        "refactoring_cross_module": "code_review",
        "schema_changes": "blocked_for_agent",
    }
)

class DomainSpecificAgent:
    """Agent adapts based on domain context"""
    
    def __init__(self, context: DomainContext):
        self.context = context
        self.domain = context.domain
    
    async def respond(self, request: str) -> dict:
        """Response changes based on domain"""
        
        if self.domain == "support":
            return await self.support_response(request)
        elif self.domain == "compliance":
            return await self.compliance_response(request)
        elif self.domain == "dev_productivity":
            return await self.dev_response(request)
    
    async def support_response(self, request: str) -> dict:
        """Fast, helpful, empathetic"""
        
        # "Customer says they sent $5K and didn't receive it"
        
        # Step 1: Fast analysis (under 2 seconds)
        transaction = await self.find_transaction(request)
        
        if transaction is None:
            # Helpful but not committal
            return {
                "response": "I can help you find this transaction. Can you provide: your wallet address, the recipient address, or the approximate time you sent it?",
                "action": "escalate_if_no_response_in_30min",
            }
        
        # Step 2: Suggest resolution (3-10 seconds)
        if transaction.status == "pending":
            return {
                "response": "I see your transaction is pending. This can take 10-30 minutes depending on network congestion. I'll monitor it and notify you when it completes.",
                "action": "monitor_transaction",
            }
        
        if transaction.status == "failed":
            amount = transaction.amount
            if amount <= 10000:
                return {
                    "response": f"Your transaction failed but we can refund the ${amount} immediately. Approving refund now.",
                    "action": "issue_refund",
                    "amount": amount,
                    "approval_type": "auto",  # Under threshold
                }
            else:
                return {
                    "response": f"Your transaction failed. We need to review this refund since it's ${amount}. A specialist will contact you within 1 hour.",
                    "action": "escalate_to_human",
                    "priority": "high",
                }
        
        # Audit: log what we did
        await self.audit_log.record({
            "domain": "support",
            "action": "respond_to_customer",
            "decision_trace": [
                f"Found transaction: {transaction.id}",
                f"Status: {transaction.status}",
                f"Decision: {decision_type}",
            ],
        })
    
    async def compliance_response(self, request: str) -> dict:
        """Precise, cited, auditable"""
        
        # "Is customer X allowed to move $10M to country Y?"
        
        # Step 1: Find regulations (slow, detailed)
        regulations = await self.find_applicable_regulations(
            customer_jurisdiction=request.customer_jurisdiction,
            target_jurisdiction=request.target_jurisdiction,
            amount=request.amount,
        )
        
        # Step 2: Analyze against each regulation
        analysis = []
        for regulation in regulations:
            result = await self.analyze_against_regulation(
                regulation,
                request
            )
            analysis.append({
                "regulation": regulation.name,
                "citation": regulation.url,
                "verdict": result.verdict,  # "allowed", "restricted", "prohibited"
                "confidence": result.confidence,  # 0.0-1.0
                "reasoning": result.reasoning,
            })
        
        # Step 3: Synthesize
        all_allowed = all(r.verdict == "allowed" for r in analysis)
        min_confidence = min(r.confidence for r in analysis)
        
        return {
            "response": f"Based on {len(analysis)} applicable regulations, this transaction is {'ALLOWED' if all_allowed else 'RESTRICTED'}. Confidence: {min_confidence:.0%}",
            "analysis": analysis,
            "requires_human_review": min_confidence < 0.8,  # Low confidence → escalate
            "recommendation": "INVESTIGATE_FURTHER" if not all_allowed else "PROCEED",
            "approval_type": "human_only",  # Compliance never auto-approves
        }
        
        # Audit: full trail for regulators
        await self.audit_log.record({
            "domain": "compliance",
            "request": request,
            "analysis": analysis,
            "synthesized_verdict": all_allowed,
            "confidence": min_confidence,
        })
    
    async def dev_response(self, request: str) -> dict:
        """Fast, helpful, non-blocking"""
        
        # "Generate tests for this function"
        
        # Step 1: Parse request (0.5s)
        code = request.code_snippet
        
        # Step 2: Analyze (2s)
        coverage = await self.analyze_coverage(code)
        
        # Step 3: Generate tests (3s)
        tests = await self.generate_tests(code, coverage)
        
        return {
            "response": f"Generated {len(tests)} tests covering {coverage.percent}% of the code",
            "tests": tests,
            "action": "create_pr_with_tests",
            "approval_type": "code_review",  # Developer reviews before merge
        }
        
        # Audit: log for context
        await self.audit_log.record({
            "domain": "dev_productivity",
            "action": "generate_tests",
            "code_location": code.path,
            "tests_generated": len(tests),
        })

# Key insight: Same company, three different agents
# Support agent is fast and helpful
# Compliance agent is slow and precise
# Dev agent is balanced
# All audit logs feed into one compliance system
```

**Why This Works:**

- Coinbase solves the speed vs. safety paradox by separating domains.
- Each domain has its own constraints and approval thresholds.
- All decisions are logged to one audit system for regulators.

**What to Learn:** In regulated industries, agents need to be transparent about their constraints. An agent that says "I might be wrong" is more trustworthy than one that's certain.

---

### 3. Holland Casino — Security-First AML Agent (Regulated Environment)

**The Problem:** Casinos are targets for money laundering. Holland Casino must screen every customer, every transaction, every pattern. Regulators audit every decision. Agent must never make a false negative (let through a bad actor).

**Architecture Decision:**

```python
# Holland Casino's "fail-safe" pattern
# When in doubt, escalate

from enum import Enum

class RiskLevel(Enum):
    CLEAR = 0        # Customer is clearly legitimate
    INVESTIGATE = 1  # Customer needs investigation
    BLOCK = 2        # Customer is blocked (fraud/AML risk)
    ESCALATE = 3     # Unclear; human decision required

class AMLAgent:
    """Anti-Money Laundering agent: fail-safe by design"""
    
    async def screen_customer(self, customer: Customer) -> RiskLevel:
        """Determine if customer can proceed"""
        
        # Check 1: Known bad actors (sanctioned lists)
        if await self.check_sanctions_lists(customer):
            return RiskLevel.BLOCK  # Hard block
        
        # Check 2: Known good actors (frequent, clean history)
        if await self.is_trusted_customer(customer):
            return RiskLevel.CLEAR
        
        # Check 3: Red flags (unusual patterns)
        red_flags = await self.detect_red_flags(customer)
        
        if len(red_flags) == 0:
            return RiskLevel.CLEAR
        elif len(red_flags) <= 2 and all(f.severity == "low" for f in red_flags):
            return RiskLevel.INVESTIGATE  # Request more info
        elif any(f.severity == "high" for f in red_flags):
            return RiskLevel.ESCALATE  # Human decision
        else:
            return RiskLevel.ESCALATE  # When in doubt, escalate
    
    async def detect_red_flags(self, customer: Customer) -> list[dict]:
        """Red flag detection: comprehensive but conservative"""
        
        red_flags = []
        
        # Flag 1: Unusual source of funds
        wealth_source = await self.analyze_wealth_source(customer)
        if wealth_source.confidence < 0.7:
            red_flags.append({
                "flag": "unclear_source_of_funds",
                "severity": "high",
                "detail": f"Source of funds unclear. Confidence: {wealth_source.confidence:.0%}",
            })
        
        # Flag 2: Structuring (multiple small deposits to avoid threshold)
        deposits = await self.get_recent_deposits(customer)
        if self.detect_structuring(deposits):
            red_flags.append({
                "flag": "structuring",
                "severity": "high",
                "detail": "Pattern of small deposits suggests structuring",
            })
        
        # Flag 3: Unusual geography
        if await self.is_high_risk_jurisdiction(customer.jurisdiction):
            red_flags.append({
                "flag": "high_risk_jurisdiction",
                "severity": "medium",
                "detail": f"Customer is in {customer.jurisdiction}",
            })
        
        # Flag 4: Rapid transaction
        if customer.time_since_account_creation < timedelta(hours=1):
            red_flags.append({
                "flag": "rapid_transaction",
                "severity": "medium",
                "detail": "Large transaction within 1 hour of account creation",
            })
        
        # Conservative rule: If ANY high-severity flag, escalate
        return red_flags
    
    async def screen_transaction(
        self,
        customer: Customer,
        transaction: Transaction
    ) -> RiskLevel:
        """Screen each transaction, not just customers"""
        
        # Pre-check: Is customer blocked?
        customer_risk = await self.screen_customer(customer)
        if customer_risk == RiskLevel.BLOCK:
            return RiskLevel.BLOCK
        
        # Transaction-level checks
        if transaction.amount > 50000:  # Large threshold
            # Large transactions always warrant review
            return RiskLevel.INVESTIGATE
        
        if transaction.recipient_is_new_to_customer:
            # New recipient is always suspicious
            return RiskLevel.INVESTIGATE
        
        if transaction.is_unusual_time:  # 3am transaction
            return RiskLevel.INVESTIGATE
        
        # Default
        return RiskLevel.CLEAR
    
    async def audit_decision(self, decision: RiskLevel, customer: Customer):
        """Audit trail for regulators"""
        
        # Every decision is logged with full reasoning
        audit_record = {
            "timestamp": now(),
            "customer_id": customer.id,
            "decision": decision,
            "decision_timestamp": now(),
            
            # Full reasoning trail
            "sanctions_check": await self.check_sanctions_lists(customer),
            "red_flags": await self.detect_red_flags(customer),
            "trust_score": await self.calculate_trust_score(customer),
            
            # Who made final decision?
            "agent_version": "1.2.3",
            "model": "claude-3-sonnet",
            "reviewed_by": None,  # If human reviewed
        }
        
        # Write to immutable log
        await self.compliance_db.log_screening_decision(audit_record)
        
        # If ESCALATE, create task for compliance officer
        if decision == RiskLevel.ESCALATE:
            await self.create_compliance_task({
                "type": "review_customer_screening",
                "customer_id": customer.id,
                "agent_recommendation": decision,
                "priority": "high",
            })
        
        # If BLOCK, alert immediately
        if decision == RiskLevel.BLOCK:
            await self.alert_compliance_team({
                "severity": "critical",
                "message": f"Customer {customer.id} blocked by AML screening",
                "reason": audit_record["red_flags"],
            })

# Cost model
# - Correct block: $0 (prevented fraud)
# - Correct allow: $0 (legitimate customer)
# - False positive (block legitimate): -$1000+ (customer complaint, trust loss)
# - False negative (allow fraudster): -$1M+ (company liability, fine)
# Therefore: False negatives are unacceptable
# Strategy: Conservative. When in doubt, escalate.
```

**Why This Works:**

- Fail-safe by design: when confidence is low, escalate to human.
- Every decision is auditable. Regulators can see exactly why customer X was blocked.
- Red flags are specific and tracked. "Pattern of small deposits" is verifiable.

**What to Learn:** In high-stakes domains, agents should be asymmetric risk detectors, not deciders. Better to inconvenience a legitimate customer than to expose the company to compliance risk.

---

### 4. Digits — Autonomous Accounting Agents

**The Problem:** Accountants spend 60% of time on reconciliation. Agents should automate that. But: accounting ledgers are sacred. One wrong entry compounds into quarterly misstatement.

**Architecture Decision:**

```python
# Digits' "propose then verify" pattern

@dataclass
class AccountingEntry:
    date: datetime
    account: str  # e.g., "1000 Cash", "5010 Revenue"
    debit: float
    credit: float
    description: str
    supporting_document: str  # Receipt, invoice, etc.

class DigitsAgent:
    """Autonomous agent for accounting decisions"""
    
    async def reconcile_account(self, account_id: str, month: str) -> list[AccountingEntry]:
        """Agent proposes entries. Accountant approves."""
        
        # Phase 1: Gather evidence
        transactions = await self.fetch_bank_transactions(account_id, month)
        existing_entries = await self.fetch_ledger_entries(account_id, month)
        
        # Phase 2: Agent proposes entries for unmatched transactions
        proposals = []
        for txn in transactions:
            if not self.is_matched_to_entry(txn, existing_entries):
                # Unmatched transaction: agent proposes an entry
                proposal = await self.propose_entry(txn, account_id)
                proposals.append(proposal)
        
        # Phase 3: CRITICAL - Verify before returning
        # Don't return to accountant until we've verified
        verified_proposals = []
        for proposal in proposals:
            # Check 1: Does it balance?
            if proposal.debit != proposal.credit:
                continue  # Skip malformed entries
            
            # Check 2: Is account real?
            if not await self.account_exists(proposal.account):
                continue  # Skip entries to non-existent accounts
            
            # Check 3: Is amount reasonable?
            if proposal.debit > 10000000:  # $10M limit
                continue  # Oversized entries need manual review
            
            # Check 4: Is there supporting documentation?
            if not proposal.supporting_document:
                continue  # No documentation, skip
            
            verified_proposals.append(proposal)
        
        return verified_proposals
    
    async def propose_entry(
        self,
        transaction: Transaction,
        account_id: str
    ) -> AccountingEntry:
        """Agent suggests what entry to make"""
        
        # Step 1: Categorize transaction
        category = await self.categorize_transaction(transaction)
        
        # Step 2: Find matching account
        account = await self.find_matching_account(category)
        
        # Step 3: Construct entry
        entry = AccountingEntry(
            date=transaction.date,
            account=account.name,
            debit=transaction.amount if transaction.type == "income" else 0,
            credit=transaction.amount if transaction.type == "expense" else 0,
            description=f"Auto-matched: {transaction.description}",
            supporting_document=transaction.receipt_url,
        )
        
        return entry
    
    async def categorize_transaction(self, txn: Transaction) -> str:
        """Map transaction to accounting category"""
        
        # Use ML + rules to categorize
        
        # Rule-based first (fast, deterministic)
        if "AWS" in txn.description:
            return "cloud_infrastructure"
        if "Stripe" in txn.description:
            return "payment_processing"
        if txn.category_code in SALARY_CODES:
            return "payroll"
        
        # Otherwise, use ML
        ml_prediction = await self.ml_classifier.predict(txn.description)
        
        return ml_prediction.category

# Accountant workflow
class AccountantApprovalUI:
    """Accountant reviews agent proposals"""
    
    async def review_proposals(self, proposals: list[AccountingEntry]):
        """Accountant sees list of proposed entries"""
        
        # UI shows:
        # ┌─────────────────────────────────────┐
        # │ Date       | Account    | Dr  | Cr   │
        # ├─────────────────────────────────────┤
        # │ 2025-01-15 | 1000 Cash  | 500 | 0    │ ← from transaction
        # │ 2025-01-15 | 5010 Rev   | 0   | 500  │ ← auto-proposed by agent
        # │                                       │
        # │ [Approve] [Edit] [Reject]            │
        # └─────────────────────────────────────┘
        
        # Accountant can:
        # 1. Approve (one click)
        # 2. Edit (change account, amount, description)
        # 3. Reject (skip this entry)
        
        # What they CAN'T do:
        # - Bypass the double-entry rule
        # - Create entry without supporting document
        # - Post to non-existent account
        
        # The agent ensures the frame; accountant fills in details
    
    async def post_entries(self, entries: list[AccountingEntry]):
        """Post approved entries to ledger"""
        
        # Final verification (sanity check)
        for entry in entries:
            assert entry.debit + entry.credit > 0, "Entry must have amount"
            assert entry.debit == entry.credit, "Double-entry rule"
        
        # Post
        await self.ledger.post_entries(entries)
        
        # Audit trail: who approved? when? agent version?
        await self.audit_log.record({
            "entries": entries,
            "approved_by": self.accountant_id,
            "approved_at": now(),
            "agent_version": "2.1.0",
        })

# Result
# - Agent reduces time: 8 hours → 30 minutes per month
# - Accountant still makes final decision
# - Every entry is verifiable + auditable
# - False positive (agent suggests wrong category): Accountant catches, corrects, learns
```

**Why This Works:**

- Agent is a proposal engine, not an executor. Accountant always has final say.
- Guardrails prevent obviously wrong entries (double-entry rule, account existence).
- Speed comes from agent reducing the search space, not from bypassing verification.

**What to Learn:** In regulated domains, agents should be assistants that increase speed and consistency, not replace human judgment. The agent's job is to handle 90% of routine cases so humans can focus on the 10% that needs judgment.

---

## Key Design Question

**How do you design an agent that can move money but can NEVER move wrong amount to wrong account?**

My answer:

```python
class MoneyMovementAgent:
    """Agent for financial transactions: safety-first design"""
    
    async def execute_transfer(self, request: TransferRequest) -> Transaction:
        """Never moving wrong amount to wrong account"""
        
        # Phase 1: VALIDATE REQUEST (before agent even runs)
        validated = await self._validate_request(request)
        
        # Phase 2: AGENT DECISION (with heavy guardrails)
        decision = await self._make_transfer_decision(validated)
        
        # Phase 3: DRY RUN (simulate before executing)
        simulation = await self._simulate_transfer(decision)
        
        # Phase 4: VERIFY SIMULATION (check the dry run)
        await self._verify_simulation(simulation)
        
        # Phase 5: EXECUTE (only after all checks pass)
        transaction = await self._execute_transfer(decision)
        
        # Phase 6: VERIFY RESULT (did money actually move?)
        await self._verify_result(transaction)
        
        return transaction
    
    async def _validate_request(self, request: TransferRequest) -> dict:
        """Input validation: no surprises"""
        
        # Check 1: Sender is authenticated
        assert request.auth_token_valid, "Invalid authentication"
        
        # Check 2: Sender owns the account
        sender_account = await self.db.get_account(request.sender_id)
        assert sender_account.owner_id == request.user_id, "Account not owned by user"
        
        # Check 3: Recipient exists
        recipient = await self.db.get_account(request.recipient_id)
        assert recipient is not None, "Recipient account doesn't exist"
        
        # Check 4: Amount is positive
        assert request.amount > 0, "Amount must be positive"
        assert request.amount <= 10000000, "Amount exceeds limit"
        
        # Check 5: Sender has funds
        assert sender_account.balance >= request.amount, "Insufficient balance"
        
        return {
            "sender": sender_account,
            "recipient": recipient,
            "amount": request.amount,
        }
    
    async def _make_transfer_decision(self, validated: dict) -> dict:
        """Agent suggests transfer"""
        
        # Agent's job: decide if this transfer should proceed
        # Agent's constraint: agent has NO power to execute
        
        sender = validated["sender"]
        recipient = validated["recipient"]
        amount = validated["amount"]
        
        # Check 1: Is recipient trusted?
        recipient_risk = await self.fraud_detector.score(recipient)
        
        # Check 2: Is amount unusual for this sender?
        sender_history = await self.get_sender_history(sender.id)
        is_unusual = amount > sender_history.max_single_transfer * 2
        
        # Check 3: Is recipient in same region?
        same_region = sender.country == recipient.country
        
        # Decision
        should_transfer = (
            recipient_risk < 0.5 and
            (not is_unusual or same_region)
        )
        
        return {
            "should_transfer": should_transfer,
            "sender_id": sender.id,
            "recipient_id": recipient.id,
            "amount": amount,
            "reasoning": {
                "recipient_risk": recipient_risk,
                "is_unusual": is_unusual,
                "same_region": same_region,
            }
        }
    
    async def _simulate_transfer(self, decision: dict) -> dict:
        """Dry run: what WOULD happen if we executed?"""
        
        if not decision["should_transfer"]:
            return {"status": "blocked_by_agent"}
        
        sender_id = decision["sender_id"]
        recipient_id = decision["recipient_id"]
        amount = decision["amount"]
        
        # Simulate in memory (no side effects)
        sender_account = await self.db.get_account(sender_id)
        recipient_account = await self.db.get_account(recipient_id)
        
        simulated = {
            "sender_before": sender_account.balance,
            "sender_after": sender_account.balance - amount,
            "recipient_before": recipient_account.balance,
            "recipient_after": recipient_account.balance + amount,
        }
        
        return simulated
    
    async def _verify_simulation(self, simulation: dict):
        """Check that simulation is correct"""
        
        if simulation["status"] == "blocked_by_agent":
            return
        
        # Math check: does it balance?
        amount_sent = simulation["sender_before"] - simulation["sender_after"]
        amount_received = simulation["recipient_after"] - simulation["recipient_before"]
        
        assert amount_sent == amount_received, "Transfer doesn't balance"
        assert amount_sent > 0, "Transfer amount is zero"
        assert simulation["sender_after"] >= 0, "Sender would go negative"
    
    async def _execute_transfer(self, decision: dict) -> Transaction:
        """Actually move the money"""
        
        if not decision["should_transfer"]:
            raise ValueError("Agent rejected transfer")
        
        # Execute as atomic transaction
        # Database guarantees: if this succeeds, both debits/credits happened
        async with self.db.transaction():
            # Debit sender
            await self.db.debit_account(
                decision["sender_id"],
                decision["amount"]
            )
            
            # Credit recipient
            await self.db.credit_account(
                decision["recipient_id"],
                decision["amount"]
            )
            
            # Record transaction
            txn = Transaction(
                id=uuid4(),
                sender_id=decision["sender_id"],
                recipient_id=decision["recipient_id"],
                amount=decision["amount"],
                status="completed",
                timestamp=now(),
            )
            
            await self.db.log_transaction(txn)
        
        return txn
    
    async def _verify_result(self, txn: Transaction):
        """Post-transaction verification"""
        
        # Check 1: Is the transaction in the database?
        recorded = await self.db.get_transaction(txn.id)
        assert recorded is not None, "Transaction not recorded"
        
        # Check 2: Did sender's balance change?
        sender = await self.db.get_account(txn.sender_id)
        assert sender.transactions[-1].id == txn.id, "Transaction not in sender's history"
        
        # Check 3: Did recipient's balance change?
        recipient = await self.db.get_account(txn.recipient_id)
        assert recipient.transactions[-1].id == txn.id, "Transaction not in recipient's history"
        
        # Check 4: Can we reverse if needed (within 60s)?
        await self.queue_reversal_task(txn, timeout_seconds=60)
        
        return True

# The answer
# 1. Validate input (check accounts, amounts, permissions)
# 2. Agent makes RECOMMENDATION (not decision)
# 3. Simulate before execution (dry run)
# 4. Verify simulation (math checks)
# 5. Execute atomically (database guarantees)
# 6. Verify result (did money actually move?)
# 7. Enable rollback (60-second window)
# That's 7 checkpoints. Money can't go wrong.
```

---

## Cross-Domain Lessons

1. **Audit trails are features, not overhead.**
   - Every decision leaves a trace. That trace is the product, not the transfer.
   - If you can't explain why an agent made a decision, the agent is not fit for production.

2. **Fail-safe > fail-fast.**
   - When in doubt, escalate to human. Cost of human review is cheap.
   - Cost of false negative (fraud slips through) is catastrophic.

3. **Agents are advisors, not executors.**
   - The more money moves, the less the agent decides and the more the human verifies.
   - $100 transfer: agent decides. $1M transfer: agent advises, human decides.

4. **Constraints are part of the contract.**
   - Agent should openly state: "I can handle transfers under $10K. Beyond that, escalate."
   - Users respect honesty about limitations more than fake competence.

5. **Regulatory compliance is not a feature to add later.**
   - Design for audit from day 1. Every decision is loggable.
   - "Who made this decision?" should have a clear answer.

---

## Healthcare / Pharma: Agents That Augment Doctors (Not Replace)

## Domain Constraints

Healthcare is constrained by patient safety, not just regulation. An LLM hallucinating a drug interaction isn't a bug report; it's a life-or-death situation.

**The immutable constraints:**

- **Patient safety is non-negotiable.** The agent's job is to augment human judgment, not replace it. A doctor can override the agent, but the agent must never make unwarranted claims.
- **Explainability is mandatory.** "Because the model said so" is not medical reasoning. Doctors need to see sources, evidence, confidence scores. Black-box AI in healthcare is malpractice.
- **FDA compliance shapes everything.** If your agent influences treatment decisions, it's a medical device and requires FDA approval. That takes 2-3 years and costs millions.
- **Data is sacred.** HIPAA violations are criminal. Patient data cannot be used to improve models without explicit consent. No casual logging.

---

## Architecture Focus

The pattern across healthcare companies isn't "smarter agents". It's **verification-driven design with clinical validation**.

```
┌──────────────────────────────────┐
│ Doctor + Patient Context         │
│ (symptoms, history, meds, labs)  │
└────────────┬─────────────────────┘
             │
    ┌────────▼────────┐
    │ Clinical Agent  │
    │ (LLM + Rules)   │
    └────────┬────────┘
             │
    ┌────────▼────────────────────────────┐
    │ Evidence Retrieval                   │
    │ - PubMed citations                   │
    │ - Treatment guidelines (AMA, NHS)    │
    │ - Patient safety database            │
    └────────┬────────────────────────────┘
             │
    ┌────────▼────────────────────────────┐
    │ Confidence + Attribution             │
    │ - Source for every claim             │
    │ - Confidence score (0.0-1.0)         │
    │ - Uncertainty quantification         │
    └────────┬────────────────────────────┘
             │
    ┌────────▼────────────────────────────┐
    │ Doctor Review + Override             │
    │ - Doctor can reject recommendation   │
    │ - Doctor can see full evidence       │
    │ - Doctor documents their decision    │
    └────────┬────────────────────────────┘
             │
    ┌────────▼────────────────────────────┐
    │ Patient Safety Monitoring            │
    │ - Track outcomes                     │
    │ - Detect adverse events              │
    │ - Continuous model improvement       │
    └──────────────────────────────────────┘
```

**Key principle:** Doctor is always in the loop. Agent handles information gathering and synthesis. Doctor handles judgment.

---

## Case Studies: Architecture + Design Decisions

### 1. Medable — Clinical Trial Agentic AI Platform

**The Problem:** Clinical trials involve hundreds of sites, thousands of patients, millions of data points. Agents could speed up enrollment, screening, and monitoring. But: one missed adverse event = trial failure + potential patient harm + regulatory action.

**Architecture Decision:**

```python
# Medable's "verification at every gate" pattern

from dataclasses import dataclass
from enum import Enum

class TrialPhase(Enum):
    SCREENING = "screening"      # Identify eligible patients
    ENROLLMENT = "enrollment"    # Recruit and consent
    MONITORING = "monitoring"    # Track safety + compliance
    ANALYSIS = "analysis"        # Compute results

@dataclass
class PatientScreening:
    """Agent screens patient for trial eligibility"""
    patient_id: str
    inclusion_criteria: list[str]  # Must have all
    exclusion_criteria: list[str]  # Must have none
    agent_recommendation: str      # "eligible" or "ineligible"
    confidence: float              # 0.0-1.0
    evidence: list[str]            # Why? (EHR references)
    requires_manual_review: bool   # If confidence low

class MedableTrial:
    """Trial orchestration with safety gates"""
    
    async def screen_patient(
        self,
        patient_id: str,
        trial_id: str
    ) -> PatientScreening:
        """Can patient enroll in trial?"""
        
        # Phase 1: Load patient EHR
        ehr = await self.get_ehr(patient_id)
        
        # Phase 2: Load trial criteria
        trial = await self.get_trial(trial_id)
        
        # Phase 3: Agent evaluates inclusion
        screening = await self._evaluate_eligibility(ehr, trial)
        
        # Phase 4: CRITICAL - Verify before releasing to coordinator
        if screening.confidence < 0.8:
            screening.requires_manual_review = True
        
        # Phase 5: Manual review if needed
        if screening.requires_manual_review:
            # Clinical coordinator reviews EHR + agent reasoning
            coordinator_decision = await self.route_to_coordinator(
                screening, ehr, trial
            )
            screening.agent_recommendation = coordinator_decision
        
        return screening
    
    async def _evaluate_eligibility(
        self,
        ehr: dict,
        trial: dict
    ) -> PatientScreening:
        """Agent: does patient meet criteria?"""
        
        evidence = []
        confidence_signals = []
        
        # Inclusion 1: Age 18-65
        age = ehr["demographics"]["age"]
        if 18 <= age <= 65:
            evidence.append(f"Age {age} is within 18-65 range")
            confidence_signals.append(1.0)
        else:
            evidence.append(f"Age {age} is outside 18-65 range")
            confidence_signals.append(0.0)
        
        # Inclusion 2: Diagnosed with condition
        diagnosis = ehr["conditions"]
        has_condition = any(c in diagnosis for c in trial.target_conditions)
        if has_condition:
            evidence.append(f"Patient has {trial.target_conditions[0]}")
            confidence_signals.append(1.0)
        else:
            evidence.append(f"No diagnosis found in EHR for {trial.target_conditions}")
            confidence_signals.append(0.0)
        
        # Inclusion 3: Lab results in range
        labs = ehr["lab_results"][-1]  # Most recent
        lab_in_range = labs["creatinine"] < 1.5
        if lab_in_range:
            evidence.append(f"Creatinine {labs['creatinine']} is acceptable")
            confidence_signals.append(1.0)
        else:
            evidence.append(f"Creatinine {labs['creatinine']} is elevated")
            confidence_signals.append(0.0)
        
        # Exclusion 1: Pregnancy
        is_pregnant = ehr["pregnancy_status"] == "pregnant"
        if is_pregnant:
            evidence.append("Patient is pregnant (exclusion)")
            return PatientScreening(
                patient_id=ehr["id"],
                inclusion_criteria=trial.inclusion,
                exclusion_criteria=trial.exclusion,
                agent_recommendation="ineligible",
                confidence=1.0,  # Clear exclusion
                evidence=evidence,
                requires_manual_review=False,
            )
        
        # Exclusion 2: Active malignancy
        has_malignancy = any(c == "malignancy" for c in ehr["conditions"])
        if has_malignancy:
            evidence.append("Active malignancy (exclusion)")
            return PatientScreening(
                patient_id=ehr["id"],
                inclusion_criteria=trial.inclusion,
                exclusion_criteria=trial.exclusion,
                agent_recommendation="ineligible",
                confidence=1.0,  # Clear exclusion
                evidence=evidence,
                requires_manual_review=False,
            )
        
        # Synthesize
        all_included = all(cs == 1.0 for cs in confidence_signals[:3])
        
        recommendation = "eligible" if all_included else "ineligible"
        avg_confidence = sum(confidence_signals) / len(confidence_signals)
        
        return PatientScreening(
            patient_id=ehr["id"],
            inclusion_criteria=trial.inclusion,
            exclusion_criteria=trial.exclusion,
            agent_recommendation=recommendation,
            confidence=avg_confidence,
            evidence=evidence,
            requires_manual_review=avg_confidence < 0.8,
        )

# Coordinator workflow
class TrialCoordinator:
    """Coordinator reviews agent recommendations"""
    
    async def review_screening(
        self,
        screening: PatientScreening,
        ehr: dict
    ) -> str:
        """Human makes final decision"""
        
        # UI shows:
        # ┌──────────────────────────────────┐
        # │ Patient: John Doe                │
        # │ DOB: 1/15/1960 (64 years)        │
        # │                                  │
        # │ Agent recommendation: ELIGIBLE   │
        # │ Confidence: 85%                  │
        # │                                  │
        # │ Evidence:                        │
        # │ - Age 64 is within 18-65 range   │
        # │ - Diagnosis: Type 2 Diabetes     │
        # │ - Creatinine 1.2 is acceptable   │
        # │ - Not pregnant                   │
        # │ - No active malignancy           │
        # │                                  │
        # │ [Agree] [Disagree - why?]       │
        # └──────────────────────────────────┘
        
        # Coordinator can: agree (1-click) or override with reason
        
        user_decision = await self.get_user_decision()  # "agree" or "override"
        
        if user_decision == "agree":
            final_decision = screening.agent_recommendation
            override_reason = None
        else:
            # Coordinator overrides
            final_decision = await self.ask_for_reason("Why do you disagree?")
            override_reason = final_decision
        
        # Log: CRITICAL - Who made decision? Agent or human?
        await self.audit_log.record({
            "patient_id": screening.patient_id,
            "trial_id": self.trial_id,
            "agent_recommendation": screening.agent_recommendation,
            "agent_confidence": screening.confidence,
            "coordinator_decision": final_decision,
            "coordinator_override_reason": override_reason,
            "coordinator_id": self.coordinator_id,
            "timestamp": now(),
        })
        
        return final_decision

# Safety monitoring
class AdverseEventDetection:
    """Continuous monitoring during trial"""
    
    async def monitor_enrolled_patients(self, trial_id: str):
        """Watch for adverse events"""
        
        enrolled_patients = await self.get_enrolled_patients(trial_id)
        
        for patient in enrolled_patients:
            ehr = await self.get_latest_ehr(patient.id)
            
            # Check 1: Has patient reported new symptoms?
            new_symptoms = await self.detect_new_symptoms(ehr)
            
            # Check 2: Have labs changed dangerously?
            lab_changes = await self.detect_lab_anomalies(ehr)
            
            # Check 3: Is patient taking prohibited medications?
            prohibited_meds = await self.check_medication_interactions(ehr)
            
            if new_symptoms or lab_changes or prohibited_meds:
                # ALERT: Potential adverse event
                await self.alert_site_investigator({
                    "patient_id": patient.id,
                    "event_type": "potential_adverse_event",
                    "new_symptoms": new_symptoms,
                    "lab_changes": lab_changes,
                    "prohibited_meds": prohibited_meds,
                })
                
                # Escalate if serious
                if lab_changes.severity == "critical":
                    await self.escalate_to_principal_investigator(patient.id)
```

**Why This Works:**

- Agent identifies eligible patients, but coordinator approves.
- Every decision is logged with agent confidence and coordinator override reason.
- Safety monitoring is continuous. Adverse events trigger alerts, not just analysis.

**What to Learn:** In clinical settings, agents should reduce cognitive load on coordinators, not replace their judgment. The agent's value is consistency (it evaluates every patient the same way), not correctness.

---

### 2. AstraZeneca — Enterprise Platform Across 21 Countries

**The Problem:** AstraZeneca operates in 21 countries, each with different regulations, languages, treatment guidelines. Building one agent per country is unmaintainable. How do you scale?

**Architecture Decision:**

```python
# AstraZeneca's "locale-aware agent" pattern

from dataclasses import dataclass

@dataclass
class LocaleContext:
    country: str
    language: str
    regulatory_body: str  # EMA, FDA, PMDA, etc.
    treatment_guidelines: str  # Which version?
    cultural_considerations: dict

class MultiCountryAgent:
    """Agent that respects local context"""
    
    def __init__(self):
        # Load guidelines for all 21 countries
        self.guidelines = {
            "US": self._load_fda_guidelines(),
            "EU": self._load_ema_guidelines(),
            "UK": self._load_mhra_guidelines(),
            "Japan": self._load_pmda_guidelines(),
            # ... etc
        }
    
    async def recommend_treatment(
        self,
        patient: dict,
        country: str,
        language: str,
    ) -> dict:
        """Recommendation changes by country"""
        
        # Step 1: Load locale context
        context = self.guidelines[country]
        
        # Step 2: Patient info (same across all countries)
        age = patient["age"]
        diagnosis = patient["diagnosis"]
        comorbidities = patient["comorbidities"]
        
        # Step 3: Country-specific treatment
        # Example: Drug A is approved in US/EU but not Japan
        
        if country == "US":
            # Use FDA-approved treatment
            recommendation = await self._recommend_us_treatment(patient, context)
        elif country == "EU":
            # Use EMA-approved treatment
            recommendation = await self._recommend_eu_treatment(patient, context)
        elif country == "Japan":
            # Use PMDA-approved treatment (different options)
            recommendation = await self._recommend_japan_treatment(patient, context)
        
        # Step 4: Localize response (language)
        if language == "ja":
            recommendation = await self._translate_to_japanese(recommendation)
        elif language == "de":
            recommendation = await self._translate_to_german(recommendation)
        
        return recommendation
    
    def _load_fda_guidelines(self) -> dict:
        """Load FDA treatment guidelines for US"""
        return {
            "approved_drugs": ["Drug A", "Drug B", "Drug C"],
            "contraindications": {
                "Drug A": ["Pregnancy", "Renal impairment"],
            },
            "standard_protocols": "FDA_APPROVED_2024",
        }
    
    def _load_pmda_guidelines(self) -> dict:
        """Load PMDA guidelines for Japan"""
        # PMDA might approve different drugs or different doses
        return {
            "approved_drugs": ["Drug A", "Drug D"],  # Note: no Drug C
            "contraindications": {
                "Drug A": ["Pregnancy", "Hepatic impairment"],  # Different!
            },
            "standard_protocols": "PMDA_APPROVED_2024",
            "cultural_notes": {
                "geriatric": "Japanese patients >75 often prefer lower doses",
            }
        }

# Deployment model
class GlobalDeployment:
    """Deploy once, localize everywhere"""
    
    def __init__(self):
        # One codebase, many configurations
        self.agent = MultiCountryAgent()
        self.endpoints = {}
    
    async def setup(self):
        """Wire up endpoints for all 21 countries"""
        
        countries = [
            "US", "UK", "Germany", "France", "Spain",
            "Japan", "Australia", "Canada", "Brazil", "India",
            # ... 11 more
        ]
        
        for country in countries:
            # Create endpoint
            self.endpoints[country] = FastAPI()
            
            @self.endpoints[country].post(f"/{country}/recommend")
            async def recommend(request: dict):
                return await self.agent.recommend_treatment(
                    request["patient"],
                    country=country,
                    language=request.get("language", self._default_language(country))
                )
            
            # This endpoint respects COUNTRY regulations automatically
            # No custom code per country
    
    def _default_language(self, country: str) -> str:
        """Default language for each country"""
        mapping = {
            "US": "en",
            "UK": "en",
            "Germany": "de",
            "France": "fr",
            "Japan": "ja",
        }
        return mapping.get(country, "en")

# Result
# - Same agent code runs everywhere
# - Different outputs per country (because guidelines differ)
# - 1000+ users across 21 countries
# - One model update pushes to all countries automatically
# - Configuration is version-controlled
```

**Why This Works:**

- Locale awareness is built into the agent, not bolted on.
- Different countries get different outputs (because medicine is different), same codebase.
- Updates are simple: new guideline → update config → rollout.

**What to Learn:** Global systems need to be locale-aware from architecture time, not patched later. Regulations are not obstacles; they're inputs to the system design.

---

### 3. Novartis — AI for Clinical Trial Transformation

**The Problem:** Clinical trials are slow (10 years average). Agents could speed patient recruitment, reduce dropout rates, and improve data quality. But: patient privacy is sacred.

**Architecture Decision:**

```python
# Novartis' "differential privacy" pattern
# Patient data stays in EHR; agent works with aggregates

@dataclass
class AggregatePatientData:
    """Agent sees averages, not individuals"""
    site_id: str
    enrollment_rate_per_week: float
    dropout_rate: float
    protocol_deviation_rate: float
    safety_event_rate: float
    demographic_summary: dict  # Aggregates only

class DifferentiallyPrivateAgent:
    """Agent learns from data without seeing individuals"""
    
    async def optimize_enrollment(
        self,
        trial_id: str,
        sites: list[str]
    ) -> dict:
        """Improve enrollment without accessing patient names"""
        
        recommendations = {}
        
        for site_id in sites:
            # Agent sees AGGREGATE data only
            aggregates = await self.get_aggregates(trial_id, site_id)
            
            # Analyze aggregates
            if aggregates.dropout_rate > 0.20:  # >20% dropout
                recommendations[site_id] = {
                    "action": "improve_retention",
                    "reason": f"Dropout rate {aggregates.dropout_rate:.0%}",
                    "suggestions": [
                        "Add support coordinator",
                        "Increase visit flexibility",
                        "Improve communication",
                    ]
                }
            
            if aggregates.enrollment_rate_per_week < 2:  # <2 patients/week
                recommendations[site_id]["action"] = "improve_recruitment"
                recommendations[site_id]["suggestions"].append(
                    "Screen more broadly"
                )
        
        return recommendations
    
    async def get_aggregates(
        self,
        trial_id: str,
        site_id: str
    ) -> AggregatePatientData:
        """Fetch site-level aggregate data"""
        
        # Query: Get counts, not individual records
        query = """
        SELECT 
            COUNT(*) as total_enrolled,
            COUNT(CASE WHEN status='dropout' THEN 1 END) / 
                COUNT(*) as dropout_rate,
            AVG(age) as avg_age,
            COUNT(CASE WHEN gender='F' THEN 1 END) / 
                COUNT(*) as pct_female
        FROM trial_enrollments
        WHERE trial_id = ? AND site_id = ?
        """
        
        result = await self.db.query(query, trial_id, site_id)
        
        # CRITICAL: Never return individual names, ages, or PHI
        return AggregatePatientData(
            site_id=site_id,
            enrollment_rate_per_week=result.total_enrolled / weeks_elapsed,
            dropout_rate=result.dropout_rate,
            demographic_summary={
                "avg_age": result.avg_age,
                "pct_female": result.pct_female,
            }
        )

# HIPAA compliance
class HIIPACompliant:
    """Ensures no patient data leaks"""
    
    async def log_agent_decision(self, decision: dict):
        """Log agent action without logging patient data"""
        
        # Allowed:
        audit_entry = {
            "timestamp": now(),
            "agent_action": decision["action"],
            "site_id": decision["site_id"],
            "reasoning": "Dropout rate too high",
        }
        
        # NOT allowed:
        # "Patient John Doe dropped out because..."
        # "3 patients from site 15 with condition X..."
        # Any individually identifiable information
        
        await self.audit_log.record(audit_entry)
```

**Why This Works:**

- Agent never touches individual patient data. Only aggregates.
- HIPAA compliance is automatic. No PHI, no violation.
- Privacy is a feature, not a constraint.

**What to Learn:** In healthcare, agents can be powerful without being creepy. Use aggregates and differential privacy to let agents learn from data without access to individuals.

---

### 4. Alan — Healthcare Customer Service with Compliance

**The Problem:** Customers call with health questions. Some are simple ("Where's my claim?"). Some are complex ("Can I take this drug with that drug?"). Agents could handle tier 1, route tier 2 to humans.

**Architecture Decision:**

```python
# Alan's "tier-based routing" pattern

from enum import Enum

class CallTier(Enum):
    SIMPLE = 1     # Agent handles: "Where is my claim?"
    COMPLEX = 2    # Agent suggests, human approves: "Drug interaction?"
    CRITICAL = 3   # Human only: emergency/safety

class AlanHealthcareAgent:
    """Customer service agent that knows its limits"""
    
    async def handle_call(self, customer_id: str, question: str) -> dict:
        """Route based on complexity"""
        
        # Step 1: Classify the question
        tier = await self.classify_question(question)
        
        # Step 2: Handle based on tier
        if tier == CallTier.SIMPLE:
            return await self.handle_simple(customer_id, question)
        elif tier == CallTier.COMPLEX:
            return await self.handle_complex(customer_id, question)
        elif tier == CallTier.CRITICAL:
            return await self.escalate_to_human(customer_id, question)
    
    async def classify_question(self, question: str) -> CallTier:
        """What tier of response is needed?"""
        
        # Simple questions: Claims, coverage, eligibility
        simple_keywords = [
            "claim status",
            "coverage",
            "deductible",
            "premium",
            "benefits",
        ]
        
        if any(kw in question.lower() for kw in simple_keywords):
            return CallTier.SIMPLE
        
        # Complex questions: Drug interactions, side effects
        complex_keywords = [
            "can i take",
            "side effects",
            "interaction",
            "medication",
            "allergy",
        ]
        
        if any(kw in question.lower() for kw in complex_keywords):
            return CallTier.COMPLEX
        
        # Critical: Emergency, urgent, high-risk
        if any(kw in question.lower() for kw in ["emergency", "ER", "hospital", "severe"]):
            return CallTier.CRITICAL
        
        return CallTier.COMPLEX  # Default: assume complex
    
    async def handle_simple(self, customer_id: str, question: str) -> dict:
        """Claims + coverage questions: agent is confident"""
        
        # Look up customer policy
        policy = await self.db.get_policy(customer_id)
        
        # Answer directly
        if "claim status" in question.lower():
            claims = await self.db.get_claims(customer_id)
            pending = [c for c in claims if c.status == "pending"]
            
            response = f"You have {len(pending)} pending claims. "
            if pending:
                response += f"Oldest is from {pending[0].date}."
            
            return {
                "response": response,
                "agent_handled": True,
                "confidence": 0.95,
                "requires_human": False,
            }
        
        return {
            "response": "I didn't understand that. Let me connect you with a specialist.",
            "agent_handled": False,
            "requires_human": True,
        }
    
    async def handle_complex(self, customer_id: str, question: str) -> dict:
        """Drug interactions: agent researches, human approves"""
        
        # Extract drugs from question
        # "Can I take Lisinopril with Metformin?"
        
        drugs = await self.extract_drugs(question)
        
        if not drugs:
            return {
                "response": "I didn't catch which medications. Can you list them?",
                "requires_human": True,
            }
        
        # Research interaction
        interaction = await self.check_drug_interaction(drugs[0], drugs[1])
        
        # Agent's research (with sources)
        research = {
            "drugs": drugs,
            "known_interaction": interaction.severity != "none",
            "severity": interaction.severity,  # "none", "mild", "moderate", "severe"
            "source": interaction.source,  # "FDA", "NIH", "UpToDate"
            "agent_confidence": 0.9,
        }
        
        # Agent suggests response, human approves
        if interaction.severity == "severe":
            # Agent cannot recommend anything; escalate
            return {
                "response": f"There's a potential SEVERE interaction between {drugs[0]} and {drugs[1]}. A pharmacist will review this and call you within 1 hour.",
                "research": research,
                "requires_human": True,
                "escalation_level": "urgent",
            }
        else:
            # Agent can suggest, but flag for human review
            return {
                "response": f"Research shows {interaction.severity} interaction between {drugs[0]} and {drugs[1]}. {interaction.recommendation}",
                "research": research,
                "requires_human": True,  # Always, for drug interactions
                "escalation_level": "normal",
            }
    
    async def extract_drugs(self, question: str) -> list[str]:
        """Parse question to find drug names"""
        
        # Simple approach: match against known drugs
        known_drugs = await self.load_drug_database()
        
        drugs_found = []
        for drug in known_drugs:
            if drug.lower() in question.lower():
                drugs_found.append(drug)
        
        return drugs_found

# Human review workflow
class PharmacistReview:
    """Pharmacist approves complex recommendations"""
    
    async def review_interaction(self, research: dict):
        """Pharmacist makes final call"""
        
        # UI shows:
        # ┌──────────────────────────────────┐
        # │ Lisinopril + Metformin           │
        # │                                  │
        # │ Agent research:                  │
        # │ - Known interaction: YES         │
        # │ - Severity: MODERATE             │
        # │ - Source: FDA + UpToDate         │
        # │                                  │
        # │ Recommendation:                  │
        # │ "Both are commonly taken         │
        # │  together. Monitor blood         │
        # │  pressure and kidney function"   │
        # │                                  │
        # │ [Approve] [Edit] [Escalate]     │
        # └──────────────────────────────────┘
        
        # Pharmacist: approve (1-click) or edit
        decision = await self.get_decision()
        
        # Send to customer
        if decision == "approve":
            await self.send_response_to_customer()
        else:
            await self.edit_and_send()
```

**Why This Works:**

- Simple questions: agent answers (fast).
- Complex questions: agent researches, human approves (safe).
- Critical questions: human only (patient safety first).

**What to Learn:** Tiered routing lets agents be both fast and safe. The agent knows its limits and escalates when needed.

---

## Key Design Question

**How do you design an agent that helps a doctor but can never replace a doctor's judgment?**

My answer:

```python
class AugmentingAgent:
    """Agent designed to augment, not replace"""
    
    async def support_diagnosis(
        self,
        patient: dict,
        doctor_impression: str,
    ) -> dict:
        """Agent gathers evidence; doctor decides"""
        
        # Phase 1: Doctor makes initial impression
        # (doctor has examined patient, ordered tests)
        
        # Phase 2: Agent gathers supporting evidence
        evidence = await self.gather_evidence(patient)
        
        # Phase 3: Agent presents evidence with confidence
        presentation = await self.present_evidence(
            evidence,
            doctor_impression,
        )
        
        # Phase 4: Doctor uses or ignores agent's evidence
        # (agent has no power to override doctor)
        
        return presentation
    
    async def gather_evidence(self, patient: dict) -> dict:
        """Agent researches, doesn't diagnose"""
        
        symptoms = patient["chief_complaint"]
        
        # Example: Patient presents with chest pain
        
        differential = {
            "ACS (acute coronary syndrome)": {
                "likelihood_given_presentation": 0.35,
                "evidence_for": [
                    "Substernal chest pain radiating to left arm",
                    "Associated with exertion",
                ],
                "evidence_against": [
                    "Normal troponin (though serial troponin needed)",
                ],
                "next_steps": [
                    "Serial troponin (3 hours)",
                    "EKG with ST changes",
                    "Cardiology consultation if elevated",
                ],
                "sources": [
                    "ACC/AHA Guidelines 2023",
                    "NEJM: Chest Pain Evaluation",
                ],
            },
            "Pulmonary Embolism": {
                "likelihood_given_presentation": 0.15,
                "evidence_for": [
                    "Acute chest pain",
                    "Shortness of breath",
                ],
                "evidence_against": [
                    "No leg swelling or pain",
                    "Normal oxygen saturation",
                ],
                "next_steps": [
                    "D-dimer if clinical suspicion",
                    "CTA chest if D-dimer elevated",
                ],
                "sources": [
                    "ACEP PE Guidelines",
                ],
            },
            "Musculoskeletal": {
                "likelihood_given_presentation": 0.30,
                "evidence_for": [
                    "Sharp pain with palpation",
                    "Reproducible with movement",
                ],
                "evidence_against": [
                    "Associated with exertion",
                ],
                "next_steps": [
                    "Reassurance",
                    "NSAIDs",
                    "Follow-up if symptoms persist",
                ],
                "sources": [
                    "Primary care guidelines",
                ],
            },
        }
        
        return differential
    
    async def present_evidence(
        self,
        evidence: dict,
        doctor_impression: str,
    ) -> dict:
        """Present findings to doctor"""
        
        # CRITICAL: Order by how well they match doctor's impression
        # Don't contradict; augment
        
        # If doctor thinks "ACS", put ACS first
        # But show all differentials
        
        ranked = self._rank_by_alignment(evidence, doctor_impression)
        
        presentation = {
            "doctor_impression": doctor_impression,
            "agent_analysis": "For reference, here are differential diagnoses based on the presentation",
            "differentials": ranked,
            "disclaimer": "This is clinical decision support, not a diagnosis. The physician's clinical judgment is final.",
            "next_actions_summary": self._synthesize_next_steps(ranked),
        }
        
        return presentation
    
    def _rank_by_alignment(self, evidence: dict, doctor_impression: str) -> list:
        """Rank differentials by match to doctor's impression"""
        
        # If doctor thinks ACS, put ACS first (it aligns with their thinking)
        # Then list others for completeness
        
        ranked = sorted(
            evidence.items(),
            key=lambda x: (
                # First: does it match doctor's impression?
                1 if doctor_impression.lower() in x[0].lower() else 0,
                # Second: likelihood
                -x[1]["likelihood_given_presentation"],
            ),
            reverse=True,
        )
        
        return [{"condition": k, **v} for k, v in ranked]
    
    def _synthesize_next_steps(self, differentials: list) -> list:
        """What should doctor do next?"""
        
        all_steps = []
        for diff in differentials:
            all_steps.extend(diff.get("next_steps", []))
        
        # Remove duplicates, preserve order
        seen = set()
        unique_steps = []
        for step in all_steps:
            if step not in seen:
                unique_steps.append(step)
                seen.add(step)
        
        return unique_steps

# Key principle: The agent's output should REDUCE the doctor's cognitive load
# Not by deciding for them, but by organizing information

# Example: Without agent, doctor thinks:
# "Chest pain... could be ACS, PE, MSK, anxiety, GERD, pleurisy...
#  Let me think through each one..."

# With agent, doctor sees:
# "Here's evidence for each. Here's what to do next for each.
#  Which one do you think it is?"

# Agent saves time without removing judgment
```

---

## Cross-Domain Lessons

1. **Explainability is the feature, not an afterthought.**
   - Doctor needs to see sources for every recommendation.
   - "Because the model said so" is not acceptable.
   - Confidence scores matter.

2. **Agents augment doctors; they never replace doctors.**
   - Even the best diagnostic AI should serve as decision support.
   - Doctor can always override. Agent can never override doctor.
   - The bond of trust between doctor and patient is sacred.

3. **Patient privacy is non-negotiable.**
   - Use aggregates, not individuals.
   - Use differential privacy.
   - If you access patient data, you have regulatory liability.

4. **Clinical validation is required.**
   - Agent's performance must be proven in prospective trials, not just retrospective.
   - FDA classification determines what's required.
   - Internal evals are not enough.

5. **Continuous monitoring saves lives.**
   - Adverse events must trigger alerts, not just logs.
   - Escalation paths must be clear and fast.
   - Safety > speed.
