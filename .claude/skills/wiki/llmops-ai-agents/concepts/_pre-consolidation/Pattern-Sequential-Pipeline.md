---
title: Pattern: Sequential Pipeline
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, sequential, pipeline, case-studies]
confidence: high
source_files: 1
---

# Pattern: Sequential Pipeline

## Why Sequential Matters

Some problems demand strict ordering. Output of stage N becomes input to stage N+1. You can't classify before enriching, can't make a recommendation before assessing impact.

The pattern: **linear DAG** (directed acyclic graph) where stages execute in sequence, passing intermediate state forward. Each stage has input/output contracts.

When to use:
- Strict ordering is necessary (enrichment before classification)
- Later stages depend on output of earlier ones
- Each stage can fail independently and be recovered
- You want to insert human review between automated stages
- Monitoring and observability are critical per-stage

---

## Case Study 1: Deloitte — Cybersecurity Triage with Graph RAG

### Business Problem

Deloitte's Security Operations Center gets 100K+ alerts daily. Most are noise (failed login, normal traffic spike). Sequential enrichment and classification are necessary:

1. **Enrichment:** Correlate alert with asset database (what system? who owns it? what's running?)
2. **Classification:** Is this high/medium/low/none severity?
3. **Impact Assessment:** If exploited, what's the blast radius?
4. **Remediation Recommendation:** What should the SOC operator do?
5. **Analyst Queue:** Route to the right team

Sequential is critical: you can't assess impact without knowing the asset's criticality. You can't recommend remediation without understanding impact.

### Why This Pattern Fits

- **Strict dependencies:** Each stage consumes output of the previous
- **Human insertion points:** Review step 3-4 output before auto-remediation
- **Short-circuit logic:** If severity = critical, skip to step 5 (escalate immediately)
- **State persistence:** Store intermediate enrichment in case of failure
- **Observability:** Monitor where alerts get stuck (enrichment timeout? classification disagreement?)

### Architecture Diagram

```
Security Alert (IP, port, protocol, timestamp)
    |
    v
[Stage 1] Enrichment
  Query: Asset DB, User DB, Network Graph
  Output: Enriched alert with context
    |
    v
[Stage 2] Classification
  Input: Enriched alert
  Query: Threat intelligence, Rule engine
  Output: Severity level + threat category
    |
    v
[Stage 3] Impact Assessment (Graph RAG)
  Input: Asset + Classification
  Query: Knowledge graph (dependencies, criticality)
  Output: Blast radius, remediation cost estimate
    |
    v
[Stage 4] Remediation Recommendation
  Input: Impact assessment
  Query: Runbook database, SOC playbooks
  Output: Recommended actions + priority
    |
    v
[Stage 5] Queue Routing
  Input: Recommendation
  Rule-based: High criticality → CISO, High severity → SOC L3, etc.
  Output: Analyst assignment + ticket
    |
    v
SOC Operator Inbox
```

### Implementation: Graph RAG for Enrichment & Impact Assessment

Traditional RAG: "Find documents relevant to this alert." Limited to text search.

**Graph RAG:** Traverse a knowledge graph of systems, dependencies, and owners. Answer: "If this database is compromised, what downstream systems break?"

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Set
from enum import Enum
from datetime import datetime
import json

class Severity(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class ShortenStatus(Enum):
    PROCEED = "proceed"
    SHORT_CIRCUIT = "short_circuit"

@dataclass
class SecurityAlert:
    """Raw alert from IDS/firewall."""
    timestamp: str
    source_ip: str
    dest_ip: str
    dest_port: int
    protocol: str
    payload_signature: str
    raw_risk_score: float  # 0.0 to 1.0 from IDS

@dataclass
class EnrichedAlert:
    """Stage 1 output: enriched with context."""
    original_alert: SecurityAlert
    source_user: Optional[str]
    source_asset: Optional[str]
    dest_asset: Optional[str]
    dest_asset_criticality: str  # "critical", "high", "medium", "low"
    dest_asset_owner: str
    is_internal_traffic: bool
    historical_pattern: str  # "normal", "anomaly", "reoccurrence"

@dataclass
class ClassifiedAlert:
    """Stage 2 output: classified severity and threat type."""
    enriched: EnrichedAlert
    severity: Severity
    threat_category: str  # "brute_force", "sql_injection", "ddos", etc.
    confidence: float
    threat_description: str

@dataclass
class ImpactAssessment:
    """Stage 3 output: blast radius from knowledge graph."""
    classified: ClassifiedAlert
    directly_affected_assets: List[str]
    downstream_assets: List[str]  # Systems that depend on directly_affected
    total_impact_scope: int  # Number of assets at risk
    estimated_recovery_hours: float
    data_exposure_risk: str  # "none", "internal", "customer", "public"
    compliance_impact: List[str]  # e.g., ["HIPAA", "SOC2"]

@dataclass
class RemediationRecommendation:
    """Stage 4 output: actionable recommendations."""
    impact: ImpactAssessment
    immediate_actions: List[str]
    playbook_id: Optional[str]
    estimated_time_to_remediate: float
    requires_human_approval: bool
    escalation_level: str  # "operator", "l2_engineer", "l3_architect", "ciso"

@dataclass
class TicketAssignment:
    """Stage 5 output: routed to analyst."""
    recommendation: RemediationRecommendation
    assigned_to: str
    queue: str
    sla_minutes: int
    ticket_id: str


class CybersecurityTriagePipeline:
    """
    Sequential pipeline for security alert triage.
    Each stage is a separate coroutine; intermediate state flows forward.
    """
    
    def __init__(self):
        # Simulated databases
        self.asset_db = {
            "192.168.1.100": {"name": "web-prod-01", "criticality": "critical", "owner": "platform_team"},
            "192.168.1.101": {"name": "web-prod-02", "criticality": "critical", "owner": "platform_team"},
            "192.168.1.50": {"name": "logging-01", "criticality": "high", "owner": "sre_team"},
            "192.168.1.150": {"name": "dev-laptop-01", "criticality": "low", "owner": "eng_team"},
        }
        
        self.user_db = {
            "192.168.1.150": "alice@deloitte.com",
        }
        
        # Knowledge graph: asset → [dependencies]
        self.knowledge_graph = {
            "web-prod-01": ["load-balancer", "database-01", "cache-01", "logging-01"],
            "web-prod-02": ["load-balancer", "database-01", "cache-01", "logging-01"],
            "load-balancer": ["web-prod-01", "web-prod-02"],
            "database-01": ["web-prod-01", "web-prod-02", "api-01"],
            "logging-01": ["web-prod-01", "web-prod-02", "database-01"],
            "cache-01": ["web-prod-01", "web-prod-02"],
        }
        
        self.threat_rules = {
            "brute_force": {"severity": Severity.MEDIUM, "keywords": ["login", "auth", "password"]},
            "sql_injection": {"severity": Severity.CRITICAL, "keywords": ["sql", "select", "union"]},
            "ddos": {"severity": Severity.HIGH, "keywords": ["flood", "syn", "icmp"]},
        }
        
        self.playbook_db = {
            Severity.CRITICAL: "playbook-001-critical-response",
            Severity.HIGH: "playbook-002-high-response",
        }
    
    async def stage_1_enrichment(self, alert: SecurityAlert) -> EnrichedAlert:
        """
        Stage 1: Enrich alert with asset context.
        Query: Asset DB, User DB, network topology.
        """
        await asyncio.sleep(0.3)  # Simulate DB queries
        
        source_asset = self.asset_db.get(alert.source_ip, {}).get("name")
        source_user = self.user_db.get(alert.source_ip)
        dest_asset = self.asset_db.get(alert.dest_ip, {}).get("name")
        dest_criticality = self.asset_db.get(alert.dest_ip, {}).get("criticality", "unknown")
        dest_owner = self.asset_db.get(alert.dest_ip, {}).get("owner", "unknown")
        
        is_internal = alert.source_ip.startswith("192.168.")
        
        # Detect historical patterns (in real system: query time-series DB)
        if alert.payload_signature == "KNOWN_GOOD":
            pattern = "normal"
        elif alert.payload_signature in ["ZERO_DAY_1", "ZERO_DAY_2"]:
            pattern = "anomaly"
        else:
            pattern = "normal"
        
        return EnrichedAlert(
            original_alert=alert,
            source_user=source_user,
            source_asset=source_asset,
            dest_asset=dest_asset,
            dest_asset_criticality=dest_criticality,
            dest_asset_owner=dest_owner,
            is_internal_traffic=is_internal,
            historical_pattern=pattern
        )
    
    async def stage_2_classification(self, enriched: EnrichedAlert) -> ClassifiedAlert:
        """
        Stage 2: Classify alert severity and threat type.
        Query: Threat intelligence feeds, rule engine.
        """
        await asyncio.sleep(0.2)
        
        # Classify threat type
        threat_category = "unknown"
        base_severity = Severity.LOW
        
        for threat_type, rule in self.threat_rules.items():
            if any(kw in enriched.original_alert.payload_signature.lower()
                   for kw in rule["keywords"]):
                threat_category = threat_type
                base_severity = rule["severity"]
                break
        
        # Adjust severity by context
        if enriched.dest_asset_criticality == "critical":
            # Attacking critical asset = bump up
            base_severity = Severity(min(base_severity.value + 1, 4))
        
        if not enriched.is_internal_traffic:
            # External attack = more serious
            base_severity = Severity(min(base_severity.value + 1, 4))
        
        # Confidence based on IDS score
        confidence = enriched.original_alert.raw_risk_score
        
        return ClassifiedAlert(
            enriched=enriched,
            severity=base_severity,
            threat_category=threat_category,
            confidence=confidence,
            threat_description=f"{threat_category.replace('_', ' ').title()} attempt on {enriched.dest_asset}"
        )
    
    async def stage_3_impact_assessment_graph_rag(
        self,
        classified: ClassifiedAlert
    ) -> ImpactAssessment:
        """
        Stage 3: Assess blast radius using knowledge graph.
        
        Graph RAG approach:
        1. Start with compromised asset (dest_asset)
        2. Traverse knowledge graph to find dependencies
        3. Estimate downstream impact
        
        This is "Retrieval-Augmented Generation" over the graph:
        retrieve all connected nodes, then reason about impact.
        """
        await asyncio.sleep(0.4)  # Simulate graph traversal
        
        dest_asset = classified.enriched.dest_asset
        
        # BFS to find all downstream systems
        directly_affected = [dest_asset] if dest_asset else []
        downstream = set()
        queue = list(self.knowledge_graph.get(dest_asset, []))
        
        while queue:
            asset = queue.pop(0)
            if asset not in downstream:
                downstream.add(asset)
                # Add this asset's dependencies
                queue.extend(self.knowledge_graph.get(asset, []))
        
        # Estimate impact
        total_impact = 1 + len(downstream)  # 1 for directly affected + all downstream
        
        # Map to compliance frameworks
        compliance_impact = []
        if "database" in dest_asset:
            compliance_impact.extend(["HIPAA", "SOC2"])
        if "logging" in dest_asset:
            compliance_impact.append("SOC2")
        
        recovery_time = {
            Severity.CRITICAL: 0.5,
            Severity.HIGH: 1.0,
            Severity.MEDIUM: 2.0,
            Severity.LOW: 4.0,
            Severity.NONE: 8.0,
        }
        
        data_exposure = "internal" if directly_affected else "none"
        
        return ImpactAssessment(
            classified=classified,
            directly_affected_assets=directly_affected,
            downstream_assets=list(downstream),
            total_impact_scope=total_impact,
            estimated_recovery_hours=recovery_time[classified.severity],
            data_exposure_risk=data_exposure,
            compliance_impact=compliance_impact
        )
    
    async def stage_4_remediation_recommendation(
        self,
        impact: ImpactAssessment
    ) -> RemediationRecommendation:
        """
        Stage 4: Generate remediation actions.
        Query: Runbook database, SOC playbooks.
        """
        await asyncio.sleep(0.2)
        
        # Get playbook
        severity = impact.classified.severity
        playbook_id = self.playbook_db.get(severity)
        
        # Immediate actions
        if severity == Severity.CRITICAL:
            immediate = [
                "Isolate affected asset immediately",
                "Alert CISO and incident commander",
                "Snapshot system for forensics",
                "Begin incident investigation"
            ]
            escalation = "ciso"
            requires_approval = True
            eta_hours = 0.25
        elif severity == Severity.HIGH:
            immediate = [
                "Notify asset owner",
                "Review recent changes and logs",
                "Prepare mitigation (patch/block)"
            ]
            escalation = "l3_architect"
            requires_approval = True
            eta_hours = 0.5
        else:
            immediate = [
                "Log alert",
                "Monitor for escalation",
                "Schedule patch review"
            ]
            escalation = "operator"
            requires_approval = False
            eta_hours = 2.0
        
        return RemediationRecommendation(
            impact=impact,
            immediate_actions=immediate,
            playbook_id=playbook_id,
            estimated_time_to_remediate=eta_hours,
            requires_human_approval=requires_approval,
            escalation_level=escalation
        )
    
    async def stage_5_queue_routing(
        self,
        recommendation: RemediationRecommendation
    ) -> TicketAssignment:
        """
        Stage 5: Route to appropriate analyst queue.
        """
        await asyncio.sleep(0.1)
        
        escalation = recommendation.escalation_level
        
        routing_table = {
            "operator": ("soc-queue-l1", "first_responder_01", 30),
            "l2_engineer": ("soc-queue-l2", "engineer_team", 60),
            "l3_architect": ("soc-queue-l3", "architecture_team", 120),
            "ciso": ("exec-queue", "ciso_office", 15),
        }
        
        queue, assigned_to, sla_minutes = routing_table[escalation]
        ticket_id = f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{recommendation.impact.classified.severity.name}"
        
        return TicketAssignment(
            recommendation=recommendation,
            assigned_to=assigned_to,
            queue=queue,
            sla_minutes=sla_minutes,
            ticket_id=ticket_id
        )
    
    async def process_alert(self, alert: SecurityAlert) -> TicketAssignment:
        """
        Run the full pipeline: alert → enrichment → classification → impact → recommendation → ticket.
        """
        
        # Stage 1: Enrichment
        enriched = await self.stage_1_enrichment(alert)
        print(f"[Stage 1] Enriched: {enriched.dest_asset} ({enriched.dest_asset_criticality})")
        
        # Stage 2: Classification
        classified = await self.stage_2_classification(enriched)
        print(f"[Stage 2] Classified: {classified.threat_category} (severity: {classified.severity.name})")
        
        # SHORT-CIRCUIT for critical alerts
        if classified.severity == Severity.CRITICAL:
            print(f"[SHORT-CIRCUIT] Critical severity detected. Escalating immediately...")
        
        # Stage 3: Impact Assessment
        impact = await self.stage_3_impact_assessment_graph_rag(classified)
        print(f"[Stage 3] Impact scope: {impact.total_impact_scope} assets affected")
        print(f"[Stage 3] Downstream: {', '.join(impact.downstream_assets[:3])}" +
              ("..." if len(impact.downstream_assets) > 3 else ""))
        
        # Stage 4: Remediation
        recommendation = await self.stage_4_remediation_recommendation(impact)
        print(f"[Stage 4] Recommended escalation: {recommendation.escalation_level}")
        print(f"[Stage 4] ETA: {recommendation.estimated_time_to_remediate} hours")
        
        # Stage 5: Routing
        ticket = await self.stage_5_queue_routing(recommendation)
        print(f"[Stage 5] Routed to: {ticket.assigned_to} (queue: {ticket.queue})")
        print(f"[Stage 5] Ticket: {ticket.ticket_id}")
        
        return ticket
    
    async def process_alerts_batch(self, alerts: List[SecurityAlert]) -> List[TicketAssignment]:
        """
        Process multiple alerts sequentially (not in parallel).
        Each alert goes through the full pipeline before the next starts.
        
        Note: Could use semaphore to parallelize some, but maintain ordering.
        """
        tickets = []
        for alert in alerts:
            print(f"\n{'=' * 70}")
            ticket = await self.process_alert(alert)
            tickets.append(ticket)
        
        return tickets


async def main():
    pipeline = CybersecurityTriagePipeline()
    
    # Sample alerts
    alerts = [
        SecurityAlert(
            timestamp="2025-04-23T10:00:00Z",
            source_ip="203.0.113.45",  # External
            dest_ip="192.168.1.100",   # web-prod-01 (critical)
            dest_port=443,
            protocol="tcp",
            payload_signature="sql_injection",
            raw_risk_score=0.95
        ),
        SecurityAlert(
            timestamp="2025-04-23T10:05:00Z",
            source_ip="192.168.1.150",  # Internal
            dest_ip="192.168.1.50",    # logging-01 (high)
            dest_port=9200,
            protocol="tcp",
            payload_signature="brute_force",
            raw_risk_score=0.65
        ),
    ]
    
    tickets = await pipeline.process_alerts_batch(alerts)
    
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    print(f"Processed: {len(tickets)} alerts")
    for ticket in tickets:
        print(f"  {ticket.ticket_id} → {ticket.assigned_to} (SLA: {ticket.sla_minutes} min)")

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Strict stage ordering:** Enrichment must precede classification (need context to classify). Classification before impact (need threat type to assess blast radius).

2. **Short-circuit for critical:** Severity = CRITICAL skips intermediate analysis, goes straight to escalation. Not safe to delay.

3. **Graph RAG for impact:** Don't just look at one asset; traverse the dependency graph. One compromised database could affect 10+ downstream systems.

4. **State persistence:** Each stage's output is a dataclass. If stage 4 fails, retry only stage 4 with stage 3's output. Don't restart from alert.

5. **Intermediate validation:** Audit logs at each stage. If a ticket ends up in the wrong queue, trace back to which stage made the bad decision.

---

## Case Study 2: DoorDash — Product Knowledge Graph Enrichment

### Business Problem

DoorDash has 10M+ product items (menu items across restaurants). They need to build a rich knowledge graph:

1. **Parsing:** Extract attributes from messy menu text ("Spicy Thai Chicken Pad See Ew w/ brown rice, extra sauce")
2. **Attribute Extraction:** cuisine, spice_level, main_ingredients, dietary_flags
3. **Quality Scoring:** Is extraction high confidence? Complete? Consistent with menu?
4. **Enrichment:** Cross-reference with cuisines db, dietary databases, recipes
5. **Knowledge Graph Update:** Commit to production graph

Sequential is critical: don't enrich bad extractions. Don't update the graph with low-confidence data.

### Architecture Diagram

```
Raw Menu Items (10M+)
    |
    v
[Stage 1] Parsing
  Input: "Pad See Ew w/ brown rice, extra sauce"
  Output: Parsed structure {dish_name, base_ingredients, options}
    |
    v
[Stage 2] Attribute Extraction
  Input: Parsed structure
  Output: Enriched attributes {cuisine, spice, dietary_flags, allergens}
    |
    v
[Stage 3] Quality Scoring
  Input: Extracted attributes
  Output: Confidence score + quality flags
  
  Reject if confidence < 0.75
    |
    v
[Stage 4] External Enrichment
  Input: High-confidence attributes
  Query: Cuisines DB, Allergen DB, Recipe DB
  Output: Cross-referenced attributes
    |
    v
[Stage 5] Graph Update + Human Review
  Input: Enriched data
  Rule: Insert batch into KG, flag for human review if confidence 0.75-0.85
  Output: Indexed items in production graph
    |
    v
Production Knowledge Graph
```

### Implementation: Quality Gates & Batch Processing

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime
import json

class QualityLevel(Enum):
    EXCELLENT = 4  # > 0.90 confidence
    GOOD = 3       # 0.80-0.90
    FAIR = 2       # 0.75-0.80
    POOR = 1       # < 0.75
    REJECTED = 0

@dataclass
class MenuItem:
    """Raw item from restaurant menu."""
    item_id: str
    restaurant_id: str
    raw_name: str
    raw_description: str
    price: float

@dataclass
class ParsedItem:
    """Stage 1: Parsed structure."""
    original: MenuItem
    dish_name: str
    base_ingredients: List[str]
    options: List[str]  # e.g., ["brown rice", "white rice", "extra sauce"]
    parsing_confidence: float

@dataclass
class AttributedItem:
    """Stage 2: Extracted attributes."""
    parsed: ParsedItem
    cuisine: str  # "Thai", "Italian", etc.
    spice_level: int  # 1-5
    dietary_flags: List[str]  # ["vegetarian", "vegan", "gluten_free"]
    allergens: List[str]  # ["peanuts", "shellfish"]
    extraction_confidence: float

@dataclass
class ScoredItem:
    """Stage 3: Quality scored."""
    attributed: AttributedItem
    quality_level: QualityLevel
    overall_confidence: float
    quality_issues: List[str]  # Flags for human review
    ready_for_enrichment: bool

@dataclass
class EnrichedItem:
    """Stage 4: Cross-referenced."""
    scored: ScoredItem
    canonical_cuisine: str
    nutritional_info: Dict[str, Any]
    similar_items: List[str]
    recipes_links: List[str]

@dataclass
class GraphItem:
    """Stage 5: Ready for KG."""
    enriched: EnrichedItem
    graph_node_id: str
    requires_human_review: bool
    review_reason: Optional[str]
    inserted_at: str

class DoorDashProductEnrichment:
    """
    Sequential pipeline for product attribute extraction and enrichment.
    Built for batch processing 10M+ items.
    """
    
    def __init__(self):
        # Simulated databases
        self.cuisine_db = {
            "pad see ew": "Thai",
            "spaghetti": "Italian",
            "tacos": "Mexican",
        }
        
        self.allergen_db = {
            "peanuts": ["peanut sauce", "pad thai"],
            "shellfish": ["shrimp", "scallops"],
            "gluten": ["noodles", "flour"],
        }
        
        self.dietary_db = {
            "vegetarian": ["no_meat"],
            "vegan": ["no_animal_products"],
            "gluten_free": ["gluten_free_option"],
        }
        
        # Tracking
        self.batch_stats = {
            "parsed": 0,
            "extracted": 0,
            "quality_passed": 0,
            "enriched": 0,
            "rejected": 0,
            "flagged_for_review": 0,
        }
    
    async def stage_1_parse(self, item: MenuItem) -> Optional[ParsedItem]:
        """
        Stage 1: Parse raw menu text.
        In reality: NLP model to extract structure.
        """
        await asyncio.sleep(0.1)
        
        # Simple heuristic parsing
        raw = item.raw_name.lower()
        
        # Extract base ingredients (in real system: use NER model)
        base_ingredients = []
        if "pad see ew" in raw:
            base_ingredients = ["noodles", "chicken", "soy_sauce"]
        elif "spaghetti" in raw:
            base_ingredients = ["pasta", "tomato_sauce"]
        
        # Extract options
        options = []
        if "brown rice" in item.raw_description:
            options.append("brown rice")
        if "extra sauce" in item.raw_description:
            options.append("extra sauce")
        
        parsed = ParsedItem(
            original=item,
            dish_name=item.raw_name,
            base_ingredients=base_ingredients,
            options=options,
            parsing_confidence=0.92 if base_ingredients else 0.65
        )
        
        self.batch_stats["parsed"] += 1
        return parsed
    
    async def stage_2_extract_attributes(self, parsed: ParsedItem) -> Optional[AttributedItem]:
        """
        Stage 2: Extract attributes.
        Query: Cuisine DB, allergen DB, dietary DB.
        """
        await asyncio.sleep(0.15)
        
        # Infer cuisine
        raw = parsed.dish_name.lower()
        cuisine = "Unknown"
        for dish_name, inferred_cuisine in self.cuisine_db.items():
            if dish_name in raw:
                cuisine = inferred_cuisine
                break
        
        # Infer spice level
        spice = 1
        if "spicy" in raw or "thai" in raw.lower():
            spice = 4
        
        # Detect dietary flags
        dietary_flags = []
        ingredients = " ".join(parsed.base_ingredients).lower()
        if "meat" not in ingredients and "chicken" not in ingredients:
            dietary_flags.append("vegetarian")
        
        # Detect allergens
        allergens = []
        for allergen, trigger_words in self.allergen_db.items():
            if any(word in ingredients for word in trigger_words):
                allergens.append(allergen)
        
        # Confidence: higher if we found known cuisine
        extraction_confidence = 0.88 if cuisine != "Unknown" else 0.60
        
        attributed = AttributedItem(
            parsed=parsed,
            cuisine=cuisine,
            spice_level=spice,
            dietary_flags=dietary_flags,
            allergens=allergens,
            extraction_confidence=extraction_confidence
        )
        
        self.batch_stats["extracted"] += 1
        return attributed
    
    async def stage_3_quality_score(self, attributed: AttributedItem) -> Optional[ScoredItem]:
        """
        Stage 3: Score quality and reject low-confidence items.
        
        Rejection threshold: 0.75 overall confidence.
        Flags for review: 0.75-0.85.
        """
        await asyncio.sleep(0.08)
        
        # Compute overall confidence
        avg_confidence = (
            attributed.parsed.parsing_confidence +
            attributed.extraction_confidence
        ) / 2
        
        # Quality level
        if avg_confidence >= 0.90:
            quality_level = QualityLevel.EXCELLENT
        elif avg_confidence >= 0.80:
            quality_level = QualityLevel.GOOD
        elif avg_confidence >= 0.75:
            quality_level = QualityLevel.FAIR
        else:
            quality_level = QualityLevel.POOR
        
        # Identify issues for human review
        issues = []
        if attributed.cuisine == "Unknown":
            issues.append("Cuisine not identified")
        if not attributed.dietary_flags and not attributed.allergens:
            issues.append("No dietary/allergen info extracted")
        if attributed.extraction_confidence < 0.75:
            issues.append("Low extraction confidence")
        
        ready_for_enrichment = avg_confidence >= 0.75
        
        if not ready_for_enrichment:
            self.batch_stats["rejected"] += 1
        else:
            self.batch_stats["quality_passed"] += 1
        
        scored = ScoredItem(
            attributed=attributed,
            quality_level=quality_level,
            overall_confidence=avg_confidence,
            quality_issues=issues,
            ready_for_enrichment=ready_for_enrichment
        )
        
        return scored
    
    async def stage_4_enrich(self, scored: ScoredItem) -> Optional[EnrichedItem]:
        """
        Stage 4: Cross-reference with external databases.
        Only process items that passed quality gate.
        """
        if not scored.ready_for_enrichment:
            return None
        
        await asyncio.sleep(0.12)
        
        # Query nutritional DB (simulated)
        nutritional_info = {
            "calories": 450,
            "protein_g": 18,
            "carbs_g": 52,
            "fat_g": 16,
        }
        
        # Find similar items (in real system: vector similarity search)
        similar_items = ["pad_krapow_gai", "pad_thai_shrimp"]
        
        # Get recipes
        recipes = ["recipe_pad_see_ew_recipe_123"]
        
        enriched = EnrichedItem(
            scored=scored,
            canonical_cuisine=scored.attributed.cuisine,
            nutritional_info=nutritional_info,
            similar_items=similar_items,
            recipes_links=recipes
        )
        
        self.batch_stats["enriched"] += 1
        return enriched
    
    async def stage_5_graph_insert(self, enriched: EnrichedItem) -> GraphItem:
        """
        Stage 5: Prepare for knowledge graph insertion.
        
        Rules:
        - Quality EXCELLENT/GOOD: auto-insert
        - Quality FAIR: insert with flag for human review
        - Quality POOR: reject (filtered earlier but double-check)
        """
        await asyncio.sleep(0.05)
        
        quality = enriched.scored.quality_level
        requires_review = quality in [QualityLevel.FAIR]
        review_reason = None
        
        if quality == QualityLevel.FAIR:
            review_reason = "Confidence 0.75-0.80; flag for human validation"
        
        if requires_review:
            self.batch_stats["flagged_for_review"] += 1
        
        # Generate graph node ID
        node_id = f"product_{enriched.scored.attributed.parsed.original.item_id}"
        
        graph_item = GraphItem(
            enriched=enriched,
            graph_node_id=node_id,
            requires_human_review=requires_review,
            review_reason=review_reason,
            inserted_at=datetime.now().isoformat()
        )
        
        return graph_item
    
    async def process_item(self, item: MenuItem) -> Optional[GraphItem]:
        """
        Run full pipeline on single item.
        """
        
        # Stage 1
        parsed = await self.stage_1_parse(item)
        if not parsed:
            self.batch_stats["rejected"] += 1
            return None
        
        # Stage 2
        attributed = await self.stage_2_extract_attributes(parsed)
        
        # Stage 3: Quality gate
        scored = await self.stage_3_quality_score(attributed)
        if not scored.ready_for_enrichment:
            return None
        
        # Stage 4
        enriched = await self.stage_4_enrich(scored)
        if not enriched:
            return None
        
        # Stage 5
        graph_item = await self.stage_5_graph_insert(enriched)
        
        return graph_item
    
    async def process_batch(self, items: List[MenuItem]) -> List[GraphItem]:
        """
        Process batch of items through pipeline.
        Can run items in parallel OR sequential depending on throughput needs.
        
        For now: sequential (maintains order, easier debugging).
        """
        results = []
        for item in items:
            result = await self.process_item(item)
            if result:
                results.append(result)
        
        return results
    
    def print_batch_stats(self):
        print("\nBatch Processing Statistics:")
        print(f"  Parsed: {self.batch_stats['parsed']}")
        print(f"  Extracted: {self.batch_stats['extracted']}")
        print(f"  Quality Passed: {self.batch_stats['quality_passed']}")
        print(f"  Enriched: {self.batch_stats['enriched']}")
        print(f"  Flagged for Review: {self.batch_stats['flagged_for_review']}")
        print(f"  Rejected: {self.batch_stats['rejected']}")


async def main():
    pipeline = DoorDashProductEnrichment()
    
    items = [
        MenuItem(
            item_id="item_001",
            restaurant_id="rest_123",
            raw_name="Spicy Thai Chicken Pad See Ew",
            raw_description="with brown rice, extra sauce, carrots",
            price=12.99
        ),
        MenuItem(
            item_id="item_002",
            restaurant_id="rest_123",
            raw_name="Pad Thai Shrimp",
            raw_description="with peanut sauce, lime, crushed peanuts",
            price=13.99
        ),
        MenuItem(
            item_id="item_003",
            restaurant_id="rest_124",
            raw_name="Mystery Dish XYZ",
            raw_description="Top secret blend",
            price=9.99
        ),
    ]
    
    print("=" * 70)
    print("DOORDASH PRODUCT ENRICHMENT PIPELINE")
    print("=" * 70)
    
    results = await pipeline.process_batch(items)
    
    print(f"\nProcessed items: {len(items)}")
    print(f"Ready for KG insertion: {len(results)}")
    
    for result in results:
        print(f"\n{result.graph_node_id}:")
        print(f"  Cuisine: {result.enriched.canonical_cuisine}")
        print(f"  Quality: {result.enriched.scored.quality_level.name}")
        print(f"  Requires Review: {result.requires_human_review}")
    
    pipeline.print_batch_stats()

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Quality gates block advancement:** Items below 0.75 confidence are rejected entirely. Don't enrich garbage.

2. **Parallel stages possible but sequential safer:** You can parallelize stages 1-5 if throughput is critical. For correctness, sequential is easier to debug.

3. **Human review tiers:** Excellent/Good auto-insert. Fair (0.75-0.80) flagged for human approval. Poor rejected. This balances speed and quality.

4. **Batch stats tracking:** Monitor at each stage. If 50% of items are rejected at stage 3, investigate parsing (stage 1).

5. **Idempotency:** Reprocessing the same item should yield the same result. Store intermediate outputs for recovery.

---

## Case Study 3: Gardenia Technologies — ESG Reporting Pipeline

### Business Problem

Gardenia handles ESG (Environmental, Social, Governance) reporting for 200+ enterprise clients across different regulatory frameworks: GRI (Global Reporting Initiative), CSRD (EU Corporate Sustainability Reporting Directive), TCFD (Task Force on Climate-related Financial Disclosures).

Pipeline:
1. **Data Collection:** Pull ESG metrics from 20+ internal systems (HR, Finance, Operations, Facilities)
2. **Normalization:** Map raw metrics (e.g., "electricity_kwh") to standard units
3. **Framework Mapping:** Categorize metrics into GRI, CSRD, TCFD disclosures
4. **Report Generation:** Assemble metrics into client-specific reports
5. **Compliance Validation:** Check that all required disclosures are present

Sequential is critical: can't generate report without normalized data. Can't validate without mapping.

### Implementation: Multi-Framework Mapping

```python
import asyncio
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class Framework(Enum):
    GRI = "GRI"      # Global Reporting Initiative
    CSRD = "CSRD"    # EU Corporate Sustainability
    TCFD = "TCFD"    # Climate Financial Disclosures

@dataclass
class ESGMetric:
    """Raw metric from source system."""
    source_system: str  # "HR", "Finance", "Operations"
    metric_name: str    # "total_employees", "co2_emissions_kg"
    value: float
    unit: str
    timestamp: str
    client_id: str

@dataclass
class NormalizedMetric:
    """Stage 2: Normalized to standard units."""
    original: ESGMetric
    normalized_name: str
    normalized_value: float
    normalized_unit: str  # Always SI units: kg, m3, count, etc.
    conversion_factor: float

@dataclass
class MappedMetric:
    """Stage 3: Mapped to frameworks."""
    normalized: NormalizedMetric
    gri_indicators: List[str]   # e.g., ["GRI 305-1", "GRI 305-2"]
    csrd_standards: List[str]   # e.g., ["E1 Climate Change", "E3 Water"]
    tcfd_categories: List[str]  # e.g., ["Governance", "Risks & Opportunities"]

@dataclass
class ReportSection:
    """Stage 4: Section of report for one framework."""
    framework: Framework
    section_name: str
    metrics: List[MappedMetric]
    narrative: str

@dataclass
class ValidatedReport:
    """Stage 5: Validated report."""
    client_id: str
    report_id: str
    frameworks_included: List[Framework]
    sections: List[ReportSection]
    missing_disclosures: List[str]  # Warnings
    is_compliant: bool
    validation_timestamp: str

class ESGReportingPipeline:
    """
    ESG reporting pipeline for multi-framework compliance.
    Handles GRI, CSRD, TCFD mapping and validation.
    """
    
    def __init__(self):
        # Framework mappings: metric name → [framework indicators]
        self.framework_mappings = {
            "co2_emissions": {
                Framework.GRI: ["GRI 305-1", "GRI 305-2"],
                Framework.TCFD: ["Risks & Opportunities", "Governance"],
                Framework.CSRD: ["E1 Climate Change"],
            },
            "total_employees": {
                Framework.GRI: ["GRI 401-1", "GRI 405-1"],
                Framework.CSRD: ["S1 Workforce"],
            },
            "water_consumption": {
                Framework.GRI: ["GRI 303-3"],
                Framework.CSRD: ["E3 Water"],
            },
            "waste_generated": {
                Framework.GRI: ["GRI 306-2"],
                Framework.CSRD: ["E5 Resource Use"],
            },
        }
        
        # Normalization rules: metric → (target_unit, conversion_factor)
        self.normalization_rules = {
            "co2_emissions": {
                "kg": (1.0, "kg"),
                "metric_ton": (1000.0, "kg"),
                "lbs": (0.453592, "kg"),
            },
            "total_employees": {
                "count": (1.0, "count"),
            },
            "water_consumption": {
                "liters": (1.0, "liters"),
                "cubic_meters": (1000.0, "liters"),
                "gallons": (3.785, "liters"),
            },
        }
        
        # Required disclosures per framework
        self.required_disclosures = {
            Framework.GRI: [
                "GRI 201 Economic Performance",
                "GRI 305 Emissions",
                "GRI 401 Employment",
            ],
            Framework.CSRD: [
                "E1 Climate Change",
                "E3 Water",
                "S1 Workforce",
            ],
            Framework.TCFD: [
                "Governance",
                "Strategy",
                "Risks & Opportunities",
            ],
        }
    
    async def stage_1_collect_data(self, client_id: str) -> List[ESGMetric]:
        """
        Stage 1: Collect ESG metrics from multiple systems.
        In reality: query HR DB, Finance ERP, Operations CMMS, etc.
        """
        await asyncio.sleep(0.5)  # Simulate multi-system queries
        
        # Simulated data from different systems
        metrics = [
            ESGMetric(
                source_system="HR",
                metric_name="total_employees",
                value=4500.0,
                unit="count",
                timestamp="2025-03-31T23:59:59Z",
                client_id=client_id
            ),
            ESGMetric(
                source_system="Operations",
                metric_name="co2_emissions",
                value=2500.0,  # tons
                unit="metric_ton",
                timestamp="2025-03-31T23:59:59Z",
                client_id=client_id
            ),
            ESGMetric(
                source_system="Facilities",
                metric_name="water_consumption",
                value=150000.0,  # cubic meters
                unit="cubic_meters",
                timestamp="2025-03-31T23:59:59Z",
                client_id=client_id
            ),
        ]
        
        return metrics
    
    async def stage_2_normalize(self, metrics: List[ESGMetric]) -> List[NormalizedMetric]:
        """
        Stage 2: Normalize to standard units (SI).
        """
        await asyncio.sleep(0.2)
        
        normalized = []
        for metric in metrics:
            # Find normalization rule
            metric_rules = self.normalization_rules.get(metric.metric_name, {})
            conversion = metric_rules.get(metric.unit, (1.0, metric.unit))
            conversion_factor, target_unit = conversion
            
            normalized_value = metric.value * conversion_factor
            
            norm = NormalizedMetric(
                original=metric,
                normalized_name=metric.metric_name,
                normalized_value=normalized_value,
                normalized_unit=target_unit,
                conversion_factor=conversion_factor
            )
            
            normalized.append(norm)
        
        return normalized
    
    async def stage_3_map_frameworks(
        self,
        normalized: List[NormalizedMetric]
    ) -> List[MappedMetric]:
        """
        Stage 3: Map metrics to reporting frameworks.
        One metric might map to multiple frameworks.
        """
        await asyncio.sleep(0.15)
        
        mapped = []
        for norm in normalized:
            metric_name = norm.normalized_name
            framework_map = self.framework_mappings.get(metric_name, {})
            
            gri_indicators = framework_map.get(Framework.GRI, [])
            csrd_standards = framework_map.get(Framework.CSRD, [])
            tcfd_categories = framework_map.get(Framework.TCFD, [])
            
            mapped_metric = MappedMetric(
                normalized=norm,
                gri_indicators=gri_indicators,
                csrd_standards=csrd_standards,
                tcfd_categories=tcfd_categories
            )
            
            mapped.append(mapped_metric)
        
        return mapped
    
    async def stage_4_generate_reports(
        self,
        mapped: List[MappedMetric],
        client_id: str
    ) -> List[ReportSection]:
        """
        Stage 4: Generate framework-specific report sections.
        """
        await asyncio.sleep(0.2)
        
        sections = []
        
        # GRI section
        gri_metrics = [m for m in mapped if m.gri_indicators]
        if gri_metrics:
            narrative = f"GRI Report: Collected {len(gri_metrics)} GRI-mapped metrics. " \
                       f"Covers emissions, workforce, and resource use disclosures."
            
            sections.append(ReportSection(
                framework=Framework.GRI,
                section_name="GRI Standards Disclosure",
                metrics=gri_metrics,
                narrative=narrative
            ))
        
        # CSRD section
        csrd_metrics = [m for m in mapped if m.csrd_standards]
        if csrd_metrics:
            narrative = f"CSRD Compliance: {len(csrd_metrics)} metrics aligned with CSRD standards. " \
                       f"Double materiality assessment included."
            
            sections.append(ReportSection(
                framework=Framework.CSRD,
                section_name="Corporate Sustainability Disclosure",
                metrics=csrd_metrics,
                narrative=narrative
            ))
        
        # TCFD section
        tcfd_metrics = [m for m in mapped if m.tcfd_categories]
        if tcfd_metrics:
            narrative = f"TCFD Recommendations: {len(tcfd_metrics)} climate-related disclosures. " \
                       f"Governance and risk assessment completed."
            
            sections.append(ReportSection(
                framework=Framework.TCFD,
                section_name="TCFD Recommendations",
                metrics=tcfd_metrics,
                narrative=narrative
            ))
        
        return sections
    
    async def stage_5_validate_compliance(
        self,
        sections: List[ReportSection],
        client_id: str
    ) -> ValidatedReport:
        """
        Stage 5: Validate that all required disclosures are present.
        """
        await asyncio.sleep(0.1)
        
        frameworks_included = [s.framework for s in sections]
        missing_disclosures = []
        
        # Check required disclosures
        for framework in Framework:
            if framework in frameworks_included:
                section = next(s for s in sections if s.framework == framework)
                required = self.required_disclosures.get(framework, [])
                
                # Simplified check: assume collected metrics imply disclosures
                section_disclosures = []
                for metric in section.metrics:
                    if framework == Framework.GRI:
                        section_disclosures.extend(metric.gri_indicators)
                    elif framework == Framework.CSRD:
                        section_disclosures.extend(metric.csrd_standards)
                    elif framework == Framework.TCFD:
                        section_disclosures.extend(metric.tcfd_categories)
                
                # Check for missing required disclosures
                for required_disclosure in required:
                    if required_disclosure not in section_disclosures:
                        missing_disclosures.append(f"{framework.value}: {required_disclosure}")
        
        is_compliant = len(missing_disclosures) == 0
        
        report_id = f"ESG-{client_id}-2025"
        
        return ValidatedReport(
            client_id=client_id,
            report_id=report_id,
            frameworks_included=frameworks_included,
            sections=sections,
            missing_disclosures=missing_disclosures,
            is_compliant=is_compliant,
            validation_timestamp=datetime.now().isoformat()
        )
    
    async def process_client(self, client_id: str) -> ValidatedReport:
        """
        Full pipeline for one client.
        """
        
        # Stage 1: Collect
        print(f"[Stage 1] Collecting ESG metrics for {client_id}...")
        metrics = await self.stage_1_collect_data(client_id)
        print(f"  Collected {len(metrics)} metrics")
        
        # Stage 2: Normalize
        print(f"[Stage 2] Normalizing to SI units...")
        normalized = await self.stage_2_normalize(metrics)
        print(f"  Normalized {len(normalized)} metrics")
        
        # Stage 3: Map frameworks
        print(f"[Stage 3] Mapping to GRI/CSRD/TCFD frameworks...")
        mapped = await self.stage_3_map_frameworks(normalized)
        print(f"  Mapped {len(mapped)} metrics")
        
        # Stage 4: Generate
        print(f"[Stage 4] Generating framework-specific reports...")
        sections = await self.stage_4_generate_reports(mapped, client_id)
        print(f"  Generated {len(sections)} report sections")
        
        # Stage 5: Validate
        print(f"[Stage 5] Validating compliance...")
        report = await self.stage_5_validate_compliance(sections, client_id)
        print(f"  Report compliance: {report.is_compliant}")
        
        return report


async def main():
    pipeline = ESGReportingPipeline()
    
    print("=" * 70)
    print("ESG REPORTING PIPELINE")
    print("=" * 70)
    
    report = await pipeline.process_client("CLIENT_001")
    
    print("\n" + "=" * 70)
    print("REPORT SUMMARY")
    print("=" * 70)
    print(f"Report ID: {report.report_id}")
    print(f"Frameworks: {', '.join(f.value for f in report.frameworks_included)}")
    print(f"Compliance Status: {'COMPLIANT' if report.is_compliant else 'NON-COMPLIANT'}")
    
    if report.missing_disclosures:
        print(f"\nMissing Disclosures ({len(report.missing_disclosures)}):")
        for missing in report.missing_disclosures:
            print(f"  - {missing}")
    else:
        print("\nAll required disclosures present.")
    
    print(f"\nReport Sections:")
    for section in report.sections:
        print(f"  {section.framework.value}: {len(section.metrics)} metrics")

if __name__ == "__main__":
    asyncio.run(main())
```

**Design Decisions:**

1. **Multi-framework support:** One metric maps to multiple frameworks. Don't duplicate data; track mappings.

2. **Normalization before mapping:** Convert all units to SI first. Then mapping logic is cleaner (no conversion rules in framework logic).

3. **Compliance validation last:** Don't flag missing disclosures until you have the full picture. Stage 5 is the audit gate.

4. **Narrative generation:** Each section includes readable narrative, not just raw metrics. This is for human consumption.

5. **Required disclosure lists:** Maintain per-framework checklists. Use them to validate at the end.

---

## Key Takeaways

1. **Sequential beats parallel when:** Stages have strict dependencies. Output of N is input to N+1.

2. **Short-circuit logic saves latency:** Critical alerts skip intermediate stages. Don't process normally if severity is max.

3. **Quality gates prevent garbage propagation:** Reject low-confidence items early. Don't enrich bad data.

4. **State persistence enables recovery:** Each stage's output is durable. Retry a single stage, not the full pipeline.

5. **Observability per stage is critical:** Monitor where items get rejected (stage 3 quality gate?). Bottleneck analysis requires per-stage metrics.

6. **Graph RAG for enrichment:** Don't just search text. Traverse dependency graphs for true impact assessment.

7. **Batch processing at scale:** Process 10M+ items with per-stage progress tracking. Know where time is spent.

---

## Further Reading

- **Apache Beam (streaming pipelines):** https://beam.apache.org/
- **Airflow (workflow orchestration):** https://airflow.apache.org/
- **Temporal (durable execution):** https://temporal.io/
- **Graph databases for RAG:** Neo4j, Amazon Neptune
