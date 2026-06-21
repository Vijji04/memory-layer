---
title: Pattern: Hierarchical Agent Systems
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, hierarchical, case-studies]
confidence: high
source_files: 1
---

# Pattern: Hierarchical Agent Systems

## Why Hierarchical Matters

A single agent can't handle enterprise complexity: 100+ tools, multiple domains (clinical, commercial, regulatory), different security boundaries, thousands of concurrent users.

Solution: **hierarchy**. Top-level orchestrator interprets user intent. Domain-specific orchestrators manage their subdomain. Specialist workers execute tasks.

The pattern:
- **Layer 1 (Enterprise):** Intent planner. "What does the user want?" Routes to domain.
- **Layer 2 (Domain):** Workflow orchestrators. "How do we achieve that in our domain?"
- **Layer 3 (Specialist):** Tool agents. "Execute this specific action."

Benefits:
- **Isolation:** Clinical data never reaches commercial agents.
- **Specialization:** Each domain agent knows its tools deeply.
- **Scale:** 1000s of users without deploying 1000s of agents.
- **Auditability:** Track decisions at each level.

---

## Case Study 1: Notion — Production Agentic Workflows

### Business Problem

Notion users want to automate complex workflows across 100+ integration targets (Slack, GitHub, Jira, Salesforce, custom webhooks, databases). Users range from non-technical (drag-drop automations) to power users (write custom JS).

Early attempts (2022-2023):
- **v1:** Single monolithic agent with 100 tools. Hallucinated wildly. Couldn't understand user intent.
- **v2:** Intent classification first, then route to domain agents. Still too broad.
- **v3:** Hierarchy of orchestrators. Better, but inconsistent.
- **v4:** Proper intent → workflow orchestrator → tool agents. Worked, but fragile.
- **v5 (current):** Robust hierarchy with clear contracts between layers.

### Why This Pattern Fits

- **User intent is ambiguous:** "Sync my contacts" could mean Slack→DB, GitHub→Notion, Salesforce→email. Intent planner disambiguates.
- **Workflow is multi-step:** Create ticket → notify team → update status. Workflow orchestrator handles coordination.
- **Tool agents are narrow:** Each agent knows one tool deeply (GitHub agent knows branches, PRs, issues; Slack agent knows channels, threads).
- **Failures are domain-scoped:** If Slack agent fails, it doesn't crash the whole system.

### Architecture Diagram

```
User: "When I star a GitHub repo, notify my Slack and create a Notion database entry"
    |
    v
[Layer 1: Intent Planner]
  Parse user intent
  Disambiguate intent
  Identify dependencies (GitHub → Slack + Notion)
  Output: Structured intent object
    |
    v
[Layer 2: Workflow Orchestrator]
  Plan multi-step workflow
  Identify triggers (GitHub star event)
  Build DAG: Trigger → Slack Notify → Notion Update
  Output: Workflow definition
    |
    v
[Layer 3: Specialist Tool Agents]
  GitHub Agent: Monitor repo stars (listen to webhook)
      |
      v
  Slack Agent: Post message to channel
      |
      v
  Notion Agent: Create/update database entry
    |
    v
Workflow Execution
```

### Implementation: Intent → Orchestrator → Tools

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import json
from datetime import datetime

class IntentType(Enum):
    SYNC = "sync"           # Keep two systems in sync
    NOTIFY = "notify"       # Send notifications
    AGGREGATE = "aggregate" # Collect data
    TRANSFORM = "transform" # Modify data
    CREATE = "create"       # Create new items

class ToolCategory(Enum):
    COMMUNICATION = "communication"  # Slack, Teams, Discord
    PROJECT_MANAGEMENT = "pm"        # Jira, GitHub, Linear
    DATA = "data"                    # Notion, Airtable, Postgres
    CRM = "crm"                      # Salesforce, HubSpot
    CLOUD = "cloud"                  # AWS, GCP, Azure

@dataclass
class UserIntent:
    """Intent planner output."""
    user_id: str
    raw_request: str
    intent_type: IntentType
    primary_tool: str      # e.g., "github"
    secondary_tools: List[str]  # e.g., ["slack", "notion"]
    trigger: str           # e.g., "on_star"
    action: str            # e.g., "notify"
    confidence: float
    disambiguation_questions: List[str]  # If confidence < 0.9

@dataclass
class WorkflowStep:
    """Single step in workflow DAG."""
    step_id: str
    agent_type: str         # e.g., "github_agent"
    action: str            # e.g., "listen_for_stars"
    input_params: Dict[str, Any]
    depends_on: List[str]  # step IDs this depends on
    timeout_seconds: float

@dataclass
class WorkflowDefinition:
    """Complete workflow plan."""
    workflow_id: str
    user_id: str
    intent: UserIntent
    steps: List[WorkflowStep]
    dag_order: List[str]   # Topologically sorted step IDs
    trigger_condition: str

@dataclass
class ToolResult:
    """Output from tool agent."""
    step_id: str
    agent_type: str
    success: bool
    result_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    execution_time_ms: float

@dataclass
class WorkflowExecution:
    """Execution trace."""
    workflow_id: str
    execution_id: str
    step_results: List[ToolResult]
    final_status: str  # "success", "partial", "failure"
    error_log: List[str]

class IntentPlanner:
    """Layer 1: Parse user intent."""
    
    async def parse_intent(self, user_id: str, raw_request: str) -> UserIntent:
        """
        Parse user intent from natural language.
        In reality: LLM call to extract structured intent.
        """
        await asyncio.sleep(0.2)
        
        request_lower = raw_request.lower()
        
        # Heuristic intent detection
        intent_type = IntentType.SYNC if "sync" in request_lower else \
                      IntentType.NOTIFY if "notify" in request_lower or "send" in request_lower else \
                      IntentType.CREATE if "create" in request_lower else \
                      IntentType.AGGREGATE
        
        # Tool detection
        primary_tool = None
        secondary_tools = []
        
        if "github" in request_lower:
            primary_tool = "github"
        if "slack" in request_lower:
            if primary_tool:
                secondary_tools.append("slack")
            else:
                primary_tool = "slack"
        if "notion" in request_lower:
            if primary_tool:
                secondary_tools.append("notion")
            else:
                primary_tool = "notion"
        
        # Trigger detection
        trigger = "manual"
        if "when" in request_lower or "if" in request_lower or "on" in request_lower:
            if "star" in request_lower:
                trigger = "on_star"
            elif "merge" in request_lower or "pr" in request_lower:
                trigger = "on_merge"
            elif "create" in request_lower:
                trigger = "on_create"
        
        # Action detection
        action = "notify" if intent_type == IntentType.NOTIFY else \
                 "sync" if intent_type == IntentType.SYNC else \
                 "create"
        
        confidence = 0.85 if primary_tool else 0.60
        
        return UserIntent(
            user_id=user_id,
            raw_request=raw_request,
            intent_type=intent_type,
            primary_tool=primary_tool,
            secondary_tools=secondary_tools,
            trigger=trigger,
            action=action,
            confidence=confidence,
            disambiguation_questions=[] if confidence > 0.9 else [
                "Which system is your source of truth?",
                "Who should be notified?"
            ]
        )

class WorkflowOrchestrator:
    """Layer 2: Plan multi-step workflows."""
    
    async def plan_workflow(self, intent: UserIntent) -> WorkflowDefinition:
        """
        Create a DAG of steps to achieve the intent.
        Determines order, dependencies, timeouts.
        """
        await asyncio.sleep(0.15)
        
        steps = []
        trigger_step_id = None
        
        # Step 1: Listen for trigger
        if intent.trigger != "manual":
            trigger_step_id = f"trigger_{intent.primary_tool}"
            steps.append(WorkflowStep(
                step_id=trigger_step_id,
                agent_type=f"{intent.primary_tool}_agent",
                action=f"listen_for_{intent.trigger}",
                input_params={
                    "user_id": intent.user_id,
                    "event_type": intent.trigger
                },
                depends_on=[],
                timeout_seconds=3600.0  # Long-lived listener
            ))
        
        # Step 2: Primary action
        primary_step_id = f"action_{intent.primary_tool}"
        steps.append(WorkflowStep(
            step_id=primary_step_id,
            agent_type=f"{intent.primary_tool}_agent",
            action=intent.action,
            input_params={
                "intent_type": intent.intent_type.value,
                "action": intent.action
            },
            depends_on=[trigger_step_id] if trigger_step_id else [],
            timeout_seconds=10.0
        ))
        
        # Steps 3+: Secondary actions (secondary tools)
        for tool in intent.secondary_tools:
            step_id = f"action_{tool}"
            steps.append(WorkflowStep(
                step_id=step_id,
                agent_type=f"{tool}_agent",
                action="process",
                input_params={
                    "tool": tool,
                    "action": intent.action
                },
                depends_on=[primary_step_id],  # Wait for primary to complete
                timeout_seconds=10.0
            ))
        
        # Topological sort
        dag_order = self._topological_sort([s.step_id for s in steps], 
                                          [s.depends_on for s in steps])
        
        workflow_id = f"wf_{intent.user_id}_{datetime.now().timestamp()}"
        
        return WorkflowDefinition(
            workflow_id=workflow_id,
            user_id=intent.user_id,
            intent=intent,
            steps=steps,
            dag_order=dag_order,
            trigger_condition=intent.trigger
        )
    
    def _topological_sort(self, step_ids: List[str], 
                         dependencies: List[List[str]]) -> List[str]:
        """Simple topological sort."""
        # In reality: use proper algorithm (Kahn's)
        result = []
        for step_id in step_ids:
            result.append(step_id)
        return result

class GitHubAgent:
    """Layer 3: Tool agent for GitHub."""
    
    async def listen_for_stars(self, user_id: str, **kwargs) -> ToolResult:
        """Start listening for repo star events."""
        import time
        start = time.time()
        await asyncio.sleep(0.3)  # Simulate setting up webhook listener
        
        return ToolResult(
            step_id=f"trigger_github",
            agent_type="github_agent",
            success=True,
            result_data={"listener_id": f"listener_{user_id}"},
            error_message=None,
            execution_time_ms=(time.time() - start) * 1000
        )
    
    async def sync(self, **kwargs) -> ToolResult:
        """Sync data from GitHub."""
        import time
        start = time.time()
        await asyncio.sleep(0.5)
        
        return ToolResult(
            step_id="action_github",
            agent_type="github_agent",
            success=True,
            result_data={
                "repos_synced": 5,
                "last_sync": datetime.now().isoformat()
            },
            error_message=None,
            execution_time_ms=(time.time() - start) * 1000
        )

class SlackAgent:
    """Layer 3: Tool agent for Slack."""
    
    async def process(self, **kwargs) -> ToolResult:
        """Send notification to Slack."""
        import time
        start = time.time()
        await asyncio.sleep(0.4)
        
        return ToolResult(
            step_id="action_slack",
            agent_type="slack_agent",
            success=True,
            result_data={
                "channel": "#notifications",
                "message_ts": "1234567890.000100"
            },
            error_message=None,
            execution_time_ms=(time.time() - start) * 1000
        )

class NotionAgent:
    """Layer 3: Tool agent for Notion."""
    
    async def process(self, **kwargs) -> ToolResult:
        """Create/update Notion entry."""
        import time
        start = time.time()
        await asyncio.sleep(0.3)
        
        return ToolResult(
            step_id="action_notion",
            agent_type="notion_agent",
            success=True,
            result_data={
                "page_id": "abc123xyz",
                "database": "Automation Log"
            },
            error_message=None,
            execution_time_ms=(time.time() - start) * 1000
        )

class NotionAgentSystem:
    """Orchestrates full hierarchy."""
    
    def __init__(self):
        self.intent_planner = IntentPlanner()
        self.workflow_orchestrator = WorkflowOrchestrator()
        
        # Layer 3 agents
        self.agents = {
            "github_agent": GitHubAgent(),
            "slack_agent": SlackAgent(),
            "notion_agent": NotionAgent(),
        }
    
    async def process_user_request(self, user_id: str, request: str) -> WorkflowExecution:
        """
        Full pipeline: Intent → Workflow → Execution.
        """
        
        print(f"[Layer 1] Parsing intent...")
        intent = await self.intent_planner.parse_intent(user_id, request)
        print(f"  Detected intent: {intent.intent_type.value}")
        print(f"  Primary tool: {intent.primary_tool}")
        print(f"  Secondary tools: {intent.secondary_tools}")
        print(f"  Confidence: {intent.confidence:.0%}")
        
        if intent.confidence < 0.9:
            print(f"  Disambiguation questions:")
            for q in intent.disambiguation_questions:
                print(f"    - {q}")
        
        print(f"\n[Layer 2] Orchestrating workflow...")
        workflow = await self.workflow_orchestrator.plan_workflow(intent)
        print(f"  Workflow ID: {workflow.workflow_id}")
        print(f"  Steps: {len(workflow.steps)}")
        for step in workflow.steps:
            print(f"    - {step.step_id} ({step.agent_type})")
        
        print(f"\n[Layer 3] Executing tools...")
        execution_id = f"exec_{datetime.now().timestamp()}"
        step_results = []
        
        for step_id in workflow.dag_order:
            # Find step definition
            step = next(s for s in workflow.steps if s.step_id == step_id)
            
            # Get agent
            agent_type = step.agent_type
            agent = self.agents.get(agent_type)
            
            if not agent:
                print(f"  ✗ {step_id}: No agent found")
                continue
            
            # Execute
            print(f"  → {step_id}...")
            
            if "listen" in step.action:
                result = await agent.listen_for_stars(user_id, **step.input_params)
            else:
                result = await agent.process(**step.input_params)
            
            step_results.append(result)
            
            if result.success:
                print(f"    ✓ Success ({result.execution_time_ms:.0f}ms)")
            else:
                print(f"    ✗ Failed: {result.error_message}")
        
        # Determine overall status
        failed = sum(1 for r in step_results if not r.success)
        final_status = "success" if failed == 0 else "partial" if failed < len(step_results) else "failure"
        
        execution = WorkflowExecution(
            workflow_id=workflow.workflow_id,
            execution_id=execution_id,
            step_results=step_results,
            final_status=final_status,
            error_log=[]
        )
        
        return execution


async def main():
    system = NotionAgentSystem()
    
    print("=" * 70)
    print("NOTION AGENTIC AUTOMATION")
    print("=" * 70)
    
    request = "When I star a GitHub repo, notify my Slack team and create a Notion log entry"
    
    execution = await system.process_user_request("user_123", request)
    
    print(f"\n{'=' * 70}")
    print("EXECUTION SUMMARY")
    print(f"{'=' * 70}")
    print(f"Workflow: {execution.workflow_id}")
    print(f"Execution: {execution.execution_id}")
    print(f"Status: {execution.final_status.upper()}")
    print(f"\nStep Results:")
    for result in execution.step_results:
        status_icon = "✓" if result.success else "✗"
        print(f"  {status_icon} {result.step_id}: {result.execution_time_ms:.0f}ms")

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Three-layer hierarchy:** Intent (what?), Orchestrator (how?), Tools (do it).

2. **Intent confidence gates UI:** If confidence < 90%, ask clarifying questions before planning workflow.

3. **DAG construction:** Workflow orchestrator builds dependency graph. GitHub must complete before Slack notifies (so we have data to send).

4. **Tool agents are narrow:** Each agent knows one integration deeply. No cross-tool logic in the agent.

5. **Execution is traceable:** Each step has metadata: execution time, success, result data. Audit trail is automatic.

---

## Case Study 2: AstraZeneca — Enterprise-Scale Clinical + Commercial

### Business Problem

AstraZeneca operates agentic workflows across three domains:

1. **Clinical:** Trial data, patient safety, regulatory submissions (HIPAA, 21 CFR Part 11 compliant)
2. **Commercial:** Pricing, market analysis, sales forecasting (no patient data)
3. **Operations:** Supply chain, manufacturing, logistics (independent of clinical/commercial)

Challenge: 1000+ users across 21 countries. Each domain has different tools, security boundaries, and audit requirements. Clinical data must NEVER reach commercial agents.

Solution: Hierarchical architecture with security boundaries.

### Architecture Diagram

```
User Request
    |
    v
[Enterprise Orchestrator]
  Multi-tenant dispatch
  Security boundary enforcement
  Audit logging
    |
    +--→ [Clinical Domain Orchestrator]
    |    ├─→ Trial Data Agent
    |    ├─→ Patient Safety Agent
    |    └─→ Regulatory Agent
    |    (HIPAA-compliant, air-gapped)
    |
    +--→ [Commercial Domain Orchestrator]
    |    ├─→ Pricing Agent
    |    ├─→ Market Intelligence Agent
    |    └─→ Sales Forecast Agent
    |    (PII-free, segregated)
    |
    +--→ [Operations Domain Orchestrator]
         ├─→ Supply Chain Agent
         ├─→ Manufacturing Agent
         └─→ Logistics Agent
         (Cost-focused)
    |
    v
Results (domain-segregated)
```

### Implementation: Multi-Tenant with Security Boundaries

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from datetime import datetime
import json

class DataClassification(Enum):
    PUBLIC = "public"              # Can be shared
    INTERNAL = "internal"          # Company use only
    CONFIDENTIAL = "confidential"  # Restricted access
    REGULATED = "regulated"        # HIPAA, SOC2, etc.

class Domain(Enum):
    CLINICAL = "clinical"
    COMMERCIAL = "commercial"
    OPERATIONS = "operations"

@dataclass
class SecurityContext:
    """Define what data/tools a user can access."""
    user_id: str
    user_domain: Domain          # Primary domain
    other_domains: Set[Domain]   # Secondary access (if any)
    clearance_level: str         # "analyst", "manager", "director"
    region: str                  # "US", "EU", "APAC"
    is_clinician: bool           # Access to patient data?
    audit_required: bool

@dataclass
class UserRequest:
    """Input to enterprise orchestrator."""
    user_id: str
    request_text: str
    security_context: SecurityContext

@dataclass
class DomainRequest:
    """Routed to domain orchestrator."""
    domain: Domain
    security_context: SecurityContext
    request_text: str
    allowed_tools: List[str]

@dataclass
class ExecutionLog:
    """Audit trail."""
    user_id: str
    request_id: str
    domain: Domain
    actions: List[Dict[str, Any]]
    timestamp: str
    data_classifications_touched: List[DataClassification]
    compliance_check_passed: bool

class SecurityEnforcer:
    """Enforces data boundaries."""
    
    def __init__(self):
        self.domain_tools = {
            Domain.CLINICAL: {
                "trial_data": DataClassification.REGULATED,
                "patient_safety": DataClassification.REGULATED,
                "regulatory": DataClassification.CONFIDENTIAL,
            },
            Domain.COMMERCIAL: {
                "pricing": DataClassification.CONFIDENTIAL,
                "market_intelligence": DataClassification.INTERNAL,
                "sales_forecast": DataClassification.CONFIDENTIAL,
            },
            Domain.OPERATIONS: {
                "supply_chain": DataClassification.INTERNAL,
                "manufacturing": DataClassification.INTERNAL,
                "logistics": DataClassification.INTERNAL,
            }
        }
        
        # Cross-domain restrictions
        self.forbidden_flows = [
            (Domain.CLINICAL, Domain.COMMERCIAL),  # Clinical → Commercial FORBIDDEN
            (Domain.COMMERCIAL, Domain.CLINICAL),  # Commercial → Clinical FORBIDDEN
        ]
    
    def validate_domain_access(
        self,
        security_context: SecurityContext,
        target_domain: Domain
    ) -> bool:
        """Can this user access this domain?"""
        
        if security_context.user_domain == target_domain:
            return True
        
        if target_domain in security_context.other_domains:
            # Check if cross-domain flow is forbidden
            for source, dest in self.forbidden_flows:
                if security_context.user_domain == source and target_domain == dest:
                    return False
            return True
        
        return False
    
    def get_allowed_tools(
        self,
        security_context: SecurityContext,
        target_domain: Domain
    ) -> List[str]:
        """What tools can this user access in this domain?"""
        
        if not self.validate_domain_access(security_context, target_domain):
            return []
        
        tools = self.domain_tools.get(target_domain, {})
        
        # Further restrict by clearance level
        if security_context.clearance_level == "analyst":
            # Analysts can only read; no write/delete
            return [t for t in tools.keys() if "read" in t or "view" in t]
        
        return list(tools.keys())
    
    def audit_request(
        self,
        user_id: str,
        target_domain: Domain,
        security_context: SecurityContext
    ) -> bool:
        """Log request for compliance."""
        
        # Clinical domain always requires audit
        if target_domain == Domain.CLINICAL:
            return True
        
        # Confidential data access requires audit
        tools = self.domain_tools.get(target_domain, {})
        for tool_classification in tools.values():
            if tool_classification == DataClassification.REGULATED:
                return True
        
        return False

class EnterpriseOrchestrator:
    """Layer 1: Route across domains with security."""
    
    def __init__(self):
        self.security_enforcer = SecurityEnforcer()
        self.request_counter = 0
    
    async def route_request(self, user_request: UserRequest) -> Dict[str, Any]:
        """
        Route user request to appropriate domain.
        Enforce security boundaries.
        """
        self.request_counter += 1
        request_id = f"req_{self.request_counter}"
        
        print(f"[Enterprise] Received request from {user_request.user_id}")
        print(f"  Request: {user_request.request_text[:60]}...")
        print(f"  Domain: {user_request.security_context.user_domain.value}")
        
        # Determine target domain
        target_domain = user_request.security_context.user_domain
        
        # Validate access
        if not self.security_enforcer.validate_domain_access(
            user_request.security_context,
            target_domain
        ):
            print(f"  ✗ Access DENIED to {target_domain.value}")
            return {"error": "Unauthorized access", "request_id": request_id}
        
        print(f"  ✓ Access granted to {target_domain.value}")
        
        # Check audit requirement
        requires_audit = self.security_enforcer.audit_request(
            user_request.user_id,
            target_domain,
            user_request.security_context
        )
        
        if requires_audit:
            print(f"  → Audit logging enabled for this request")
        
        # Get allowed tools
        allowed_tools = self.security_enforcer.get_allowed_tools(
            user_request.security_context,
            target_domain
        )
        
        print(f"  Allowed tools: {', '.join(allowed_tools)}")
        
        # Route to domain orchestrator
        domain_request = DomainRequest(
            domain=target_domain,
            security_context=user_request.security_context,
            request_text=user_request.request_text,
            allowed_tools=allowed_tools
        )
        
        return {
            "request_id": request_id,
            "domain_request": domain_request,
            "requires_audit": requires_audit
        }

class ClinicalDomainOrchestrator:
    """Domain orchestrator for clinical."""
    
    async def orchestrate(self, domain_request: DomainRequest) -> Dict[str, Any]:
        """Route to clinical agents."""
        
        print(f"\n[Clinical Orchestrator] Processing clinical request")
        print(f"  Allowed tools: {', '.join(domain_request.allowed_tools)}")
        
        # Clinical workflows are heavily regulated
        if "trial_data" in domain_request.allowed_tools:
            print(f"  → Clinical Trial Data Agent")
        if "patient_safety" in domain_request.allowed_tools:
            print(f"  → Patient Safety Agent")
        if "regulatory" in domain_request.allowed_tools:
            print(f"  → Regulatory Submissions Agent")
        
        return {
            "domain": "clinical",
            "status": "executed",
            "agents_called": [t for t in domain_request.allowed_tools]
        }

class CommercialDomainOrchestrator:
    """Domain orchestrator for commercial."""
    
    async def orchestrate(self, domain_request: DomainRequest) -> Dict[str, Any]:
        """Route to commercial agents."""
        
        print(f"\n[Commercial Orchestrator] Processing commercial request")
        print(f"  Allowed tools: {', '.join(domain_request.allowed_tools)}")
        
        # Commercial workflows focus on business metrics
        if "pricing" in domain_request.allowed_tools:
            print(f"  → Pricing Agent")
        if "market_intelligence" in domain_request.allowed_tools:
            print(f"  → Market Intelligence Agent")
        if "sales_forecast" in domain_request.allowed_tools:
            print(f"  → Sales Forecast Agent")
        
        return {
            "domain": "commercial",
            "status": "executed",
            "agents_called": [t for t in domain_request.allowed_tools]
        }

class OperationsDomainOrchestrator:
    """Domain orchestrator for operations."""
    
    async def orchestrate(self, domain_request: DomainRequest) -> Dict[str, Any]:
        """Route to operations agents."""
        
        print(f"\n[Operations Orchestrator] Processing operations request")
        print(f"  Allowed tools: {', '.join(domain_request.allowed_tools)}")
        
        if "supply_chain" in domain_request.allowed_tools:
            print(f"  → Supply Chain Agent")
        if "manufacturing" in domain_request.allowed_tools:
            print(f"  → Manufacturing Agent")
        if "logistics" in domain_request.allowed_tools:
            print(f"  → Logistics Agent")
        
        return {
            "domain": "operations",
            "status": "executed",
            "agents_called": [t for t in domain_request.allowed_tools]
        }

class AstraZenecaAgentSystem:
    """Complete multi-tenant agentic system."""
    
    def __init__(self):
        self.enterprise = EnterpriseOrchestrator()
        self.orchestrators = {
            Domain.CLINICAL: ClinicalDomainOrchestrator(),
            Domain.COMMERCIAL: CommercialDomainOrchestrator(),
            Domain.OPERATIONS: OperationsDomainOrchestrator(),
        }
    
    async def process_request(self, user_request: UserRequest) -> Dict[str, Any]:
        """Full request processing with security."""
        
        # Enterprise routing
        routing_result = await self.enterprise.route_request(user_request)
        
        if "error" in routing_result:
            return routing_result
        
        domain_request = routing_result["domain_request"]
        target_domain = domain_request.domain
        
        # Domain orchestration
        orchestrator = self.orchestrators[target_domain]
        domain_result = await orchestrator.orchestrate(domain_request)
        
        # Audit logging
        if routing_result["requires_audit"]:
            print(f"\n[Audit] Logged request {routing_result['request_id']}")
            print(f"  User: {user_request.user_id}")
            print(f"  Domain: {target_domain.value}")
            print(f"  Timestamp: {datetime.now().isoformat()}")
        
        return {
            "request_id": routing_result["request_id"],
            "domain_result": domain_result,
            "audited": routing_result["requires_audit"]
        }

async def main():
    system = AstraZenecaAgentSystem()
    
    print("=" * 70)
    print("ASTRAZENECA MULTI-DOMAIN AGENTIC SYSTEM")
    print("=" * 70)
    
    # Clinical user accessing clinical domain
    clinical_context = SecurityContext(
        user_id="dr_smith_001",
        user_domain=Domain.CLINICAL,
        other_domains=set(),
        clearance_level="director",
        region="US",
        is_clinician=True,
        audit_required=True
    )
    
    clinical_request = UserRequest(
        user_id="dr_smith_001",
        request_text="Analyze adverse events from trial XYZ-456",
        security_context=clinical_context
    )
    
    print("\n--- Request 1: Clinical User ---")
    result1 = await system.process_request(clinical_request)
    
    # Commercial user trying to access clinical domain (should fail)
    commercial_context = SecurityContext(
        user_id="sales_mgr_002",
        user_domain=Domain.COMMERCIAL,
        other_domains=set(),
        clearance_level="manager",
        region="EU",
        is_clinician=False,
        audit_required=False
    )
    
    clinical_request_by_commercial = UserRequest(
        user_id="sales_mgr_002",
        request_text="Get trial data for pricing",
        security_context=commercial_context
    )
    
    print("\n--- Request 2: Commercial User (trying clinical) ---")
    result2 = await system.process_request(clinical_request_by_commercial)
    
    # Operator accessing operations domain
    ops_context = SecurityContext(
        user_id="ops_analyst_003",
        user_domain=Domain.OPERATIONS,
        other_domains=set(),
        clearance_level="analyst",
        region="APAC",
        is_clinician=False,
        audit_required=False
    )
    
    ops_request = UserRequest(
        user_id="ops_analyst_003",
        request_text="Check supply chain status",
        security_context=ops_context
    )
    
    print("\n--- Request 3: Operations User ---")
    result3 = await system.process_request(ops_request)

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Data classification drives security:** REGULATED data can't flow to COMMERCIAL domain. Audit logs automatically.

2. **Forbidden flows:** Clinical ↔ Commercial is bidirectionally forbidden. No exceptions.

3. **Clearance-based access:** Analysts can't write; directors can. Granular per-user.

4. **Audit is automatic:** No human review needed to enable audit; rules do it.

5. **Domain orchestrators are independent:** Each domain knows its tools. No cross-domain coupling.

---

## Case Study 3: PwC — AI Managed Services for Dozens of Clients

### Business Problem

PwC offers AI consulting to 50+ enterprise clients. Each client has:
- Different tools (Salesforce vs. SAP)
- Different policies (some require on-premise agents)
- Different data isolation needs (healthcare vs. finance)
- Different SLAs (tier-1 clients get faster execution)

Monolithic agent per client doesn't scale. Solution: shared PwC orchestrator + client-specific agent policies.

### Implementation: Client Isolation Layer

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum

class ClientTier(Enum):
    STANDARD = "standard"     # Shared compute
    PREMIUM = "premium"       # Dedicated resources
    ENTERPRISE = "enterprise" # On-premise agents + VPN

@dataclass
class ClientPolicy:
    """Per-client configuration."""
    client_id: str
    client_name: str
    tier: ClientTier
    allowed_tools: List[str]
    max_concurrent_workflows: int
    data_residency: str  # "US", "EU", "ON_PREMISE"
    require_encryption: bool
    audit_level: str  # "basic", "full", "forensic"

@dataclass
class ClientRequest:
    """Request scoped to client."""
    client_id: str
    policy: ClientPolicy
    request_text: str
    user_id: str

class ClientIsolationLayer:
    """Multi-tenant isolation for PwC clients."""
    
    def __init__(self):
        self.client_policies = {
            "acme_corp": ClientPolicy(
                client_id="acme_corp",
                client_name="ACME Corporation",
                tier=ClientTier.ENTERPRISE,
                allowed_tools=["salesforce", "custom_crm", "analytics"],
                max_concurrent_workflows=10,
                data_residency="US",
                require_encryption=True,
                audit_level="forensic"
            ),
            "healthtech_inc": ClientPolicy(
                client_id="healthtech_inc",
                client_name="HealthTech Inc",
                tier=ClientTier.PREMIUM,
                allowed_tools=["ehr_system", "analytics"],
                max_concurrent_workflows=5,
                data_residency="EU",  # GDPR
                require_encryption=True,
                audit_level="full"
            ),
            "fintech_startup": ClientPolicy(
                client_id="fintech_startup",
                client_name="FinTech Startup",
                tier=ClientTier.STANDARD,
                allowed_tools=["accounting_software", "analytics"],
                max_concurrent_workflows=2,
                data_residency="US",
                require_encryption=False,
                audit_level="basic"
            ),
        }
    
    async def scope_request_to_client(
        self,
        client_id: str,
        request_text: str,
        user_id: str
    ) -> ClientRequest:
        """Wrap request with client policy."""
        
        policy = self.client_policies.get(client_id)
        if not policy:
            raise ValueError(f"Unknown client: {client_id}")
        
        print(f"[Isolation Layer] Scoping request to {policy.client_name}")
        print(f"  Tier: {policy.tier.value}")
        print(f"  Data residency: {policy.data_residency}")
        print(f"  Allowed tools: {', '.join(policy.allowed_tools)}")
        
        return ClientRequest(
            client_id=client_id,
            policy=policy,
            request_text=request_text,
            user_id=user_id
        )

class PwCPlatformOrchestrator:
    """Central PwC AI platform serving 50+ clients."""
    
    def __init__(self):
        self.isolation_layer = ClientIsolationLayer()
        self.client_queues = {}  # Per-client execution queues
    
    async def handle_client_request(
        self,
        client_id: str,
        request_text: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Handle request from one client."""
        
        # Isolate request to client
        client_request = await self.isolation_layer.scope_request_to_client(
            client_id, request_text, user_id
        )
        
        # Check concurrent workflow limit
        queue = self.client_queues.get(client_id, [])
        if len(queue) >= client_request.policy.max_concurrent_workflows:
            print(f"  ✗ Workflow limit reached for {client_request.policy.client_name}")
            return {"error": "Workflow limit exceeded", "client_id": client_id}
        
        print(f"  ✓ Request queued for execution")
        
        # Select execution environment based on tier
        if client_request.policy.tier == ClientTier.ENTERPRISE:
            execution_env = "on_premise_vpc"
            print(f"  → Executing on client's on-premise VPC")
        elif client_request.policy.tier == ClientTier.PREMIUM:
            execution_env = "dedicated_pwc_cluster"
            print(f"  → Executing on dedicated PwC infrastructure")
        else:
            execution_env = "shared_pwc_cluster"
            print(f"  → Executing on shared PwC infrastructure")
        
        # Simulate execution
        await asyncio.sleep(0.5)
        
        return {
            "client_id": client_id,
            "status": "executed",
            "execution_env": execution_env,
            "audit_level": client_request.policy.audit_level
        }

async def main():
    platform = PwCPlatformOrchestrator()
    
    print("=" * 70)
    print("PWC AI MANAGED SERVICES PLATFORM")
    print("=" * 70)
    
    # Enterprise client (on-premise)
    print("\n--- Request 1: ACME Corp (Enterprise) ---")
    result1 = await platform.handle_client_request(
        "acme_corp",
        "Analyze Q1 sales pipeline",
        "user_acme_001"
    )
    
    # Premium client (GDPR)
    print("\n--- Request 2: HealthTech Inc (Premium) ---")
    result2 = await platform.handle_client_request(
        "healthtech_inc",
        "Extract de-identified patient summaries",
        "user_healthtech_001"
    )
    
    # Standard tier client
    print("\n--- Request 3: FinTech Startup (Standard) ---")
    result3 = await platform.handle_client_request(
        "fintech_startup",
        "Reconcile accounts",
        "user_fintech_001"
    )

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Client policy drives execution:** Where to run? How many concurrent? What audit level?

2. **Tier-based resource allocation:** Enterprise gets dedicated, premium gets priority, standard gets shared.

3. **Concurrent workflow limits:** Prevent one client from starving others.

4. **Data residency enforcement:** EU clients run in EU region (GDPR compliance).

5. **Audit level auto-scales:** Forensic audit for healthcare, basic for startups.

---

## Key Takeaways

1. **Hierarchy solves scale:** 1000+ users with reasonable infrastructure through architectural layers.

2. **Security boundaries are hard to retrofit:** Design them in from the beginning (don't add later).

3. **Intent planning is the bottleneck:** Get intent right, and the rest is straightforward routing.

4. **DAG construction enables reproducibility:** Same workflow produces same results. Testable and auditable.

5. **Span of control matters:** A orchestrator managing 5 specialists is more reliable than one managing 50.

6. **Cross-domain flows are dangerous:** Forbid them by default. Explicit allowlisting only.

---

## Further Reading

- **The Art of Readable Code:** Chapter on complexity and hierarchy
- **Google SRE Book:** Sections on distributed system design
- **Kubernetes API design:** Multi-tenant resource isolation
- **Zero Trust Architecture (NIST):** Security boundary design
