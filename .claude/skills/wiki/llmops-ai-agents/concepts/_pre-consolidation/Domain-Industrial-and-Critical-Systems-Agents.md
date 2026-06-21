---
title: Domain: Industrial and Critical Systems Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, domains, industrial, safety-critical, iot, case-studies]
confidence: high
source_files: 1
---

# Domain: Industrial and Critical Systems Agents

An agent tells a factory: "Increase production line speed by 15%."
The factory does it.
Three things might happen:
1. Production increases, everything works, margins improve
2. A bearing overheats, the line shuts down, you lose $2M in downtime
3. Worker gets injured because the line moved faster than expected

This is industrial: **Decisions have immediate physical consequences that hurt people or break things.**

Unlike finance ("wrong call costs money") or media ("wrong call spreads misinformation"), industrial decisions translate directly to:
- Safety: People get injured
- Equipment: Machines break
- Environment: Emissions, waste
- Quality: Bad products ship

## Domain Constraints

### 1. **IoT Sensor Data Is Noisy**
Industrial machines generate massive amounts of sensor data:
- Temperature sensors (± 2 degrees of error)
- Pressure gauges (sometimes stuck)
- Vibration sensors (pick up ambient noise)
- Current/power meters (fluctuate)

An agent trained on "normal vibration = 5.2 Hz" will fail when it's actually 5.2 ± 0.5 Hz due to sensor noise.

### 2. **Physical Laws Don't Break for ML**
A neural network can't violate physics. But it can recommend something that violates conservation of energy, fluid dynamics, or thermodynamics.

Example:
- Recommendation: "Increase pressure in this pipe by 40%"
- Physics reality: Pipe rated for max 60 bar, you're at 55 bar
- Agent doesn't know this (not in training data)
- Pipe bursts, damages equipment, kills someone

### 3. **Regulations Are Strict**
Industrial manufacturing is heavily regulated:
- OSHA (Occupational Safety): Equipment must be safe for workers
- EPA (Environmental): Emissions must be within limits
- Industry-specific (automotive, pharma, food): Additional rules
- Insurance requirements: Machine must operate within designed parameters

An agent that violates regulations makes the company liable, even if it improves efficiency.

### 4. **Legacy Systems Don't Have APIs**
Factories have equipment from 1995, 2005, 2015 running side-by-side.
Some have digital interfaces. Some are purely mechanical.
Some have sensors. Some have none.

You can't expect an agent to understand a 30-year-old hydraulic system without explicit encoding of its operating parameters.

### 5. **Human Workers Have Different Cognitive Loads**
The agent recommends something fast. Humans need to execute it.
- Can they physically do it? (Is it ergonomic?)
- Will they understand the instruction? (Is it clear?)
- Can they catch problems? (Are they watching or doing other tasks?)

A factory that optimizes for agent decisions without considering human execution will create accidents.

---

## Architecture Focus: IoT Sensor Integration + Physical Constraint Modeling

```
FACTORY FLOOR:
├─ 500+ sensors (temperature, pressure, vibration, power)
├─ 50+ machines (each with different operating parameters)
├─ 200+ workers (executing changes, catching problems)

        │
        ├─→ [SENSOR AGGREGATION]
        │   Stream all data to edge server
        │   Timestamp: Every 100ms
        │   Volume: ~5TB/month raw data
        │
        ├─→ [ANOMALY DETECTION] (Real-time)
        │   Rule: If temperature > 85°C (for this bearing)
        │          → Alert: Bearing might be overheating
        │   Rule: If vibration > 8 Hz AND duration > 5s
        │          → Alert: Possible imbalance
        │   (All rule-based, not ML for safety)
        │
        ├─→ [CONTEXTUAL ANALYSIS] (Historical)
        │   Compare current state to historical patterns
        │   "Last time we saw this pattern, X happened"
        │   Confidence: 80%
        │
        ├─→ [CONSTRAINT CHECK] (Symbolic)
        │   Physical constraints:
        │   - Pipe rated for 60 bar, currently at 55 bar
        │   - Bearing rated for 100°C, currently at 75°C
        │   - Motor rated for 3000 RPM, currently at 2800 RPM
        │   → All within safety margins
        │
        ├─→ [RECOMMENDATION GENERATION]
        │   "Increase pressure by 5% (from 55 to 58 bar)"
        │   Reasoning: Better flow, within safety margin
        │   Risk: LOW (3% margin to max)
        │   Time to implement: 2 minutes
        │
        ├─→ [HUMAN APPROVAL]
        │   Alert operator: "Recommendation ready for approval"
        │   Display: Current state, recommendation, risk level
        │   Operator can: Approve, Modify, Reject
        │
        └─→ [EXECUTION + MONITORING]
            Apply change in stages:
            Stage 1: Increase by 1%, wait 30 seconds, monitor
            Stage 2: Increase by 2% (total 3%), wait 30s
            Stage 3: Increase by 2% (total 5%), monitor for 2 minutes
            
            If any problem detected → Rollback immediately
```

### **Physical Constraint Modeling**

```python
class IndustrialConstraints(Agent):
    """
    Hard constraints from machine specifications.
    Not learned. Explicitly encoded.
    
    These are safety-critical.
    """
    
    MACHINE_SPECS = {
        "bearing_A3": {
            "max_temperature_c": 100,
            "max_pressure_bar": 80,
            "max_vibration_hz": 15,
            "operating_efficiency_range": (2500, 3500),  # RPM
            "lubrication_interval_hours": 500,
        },
        "pipe_section_12": {
            "rated_pressure_bar": 60,
            "rated_temperature_c": 120,
            "rated_flow_rate_liters_min": 200,
            "safety_factor": 1.5,  # Don't exceed 60/1.5 = 40 bar sustained
        }
    }
    
    def validate_recommendation(
        self,
        equipment: str,
        recommendation: OperationalChange
    ) -> ValidationResult:
        """
        Before an agent can recommend a change,
        prove it's physically safe.
        """
        
        specs = self.MACHINE_SPECS[equipment]
        
        # Current state (from sensors)
        current_temp = self.get_current_temperature(equipment)
        current_pressure = self.get_current_pressure(equipment)
        current_vibration = self.get_current_vibration(equipment)
        
        # Proposed state (from recommendation)
        proposed_temp = recommendation.temperature
        proposed_pressure = recommendation.pressure
        proposed_vibration = recommendation.vibration
        
        # Validation checks
        failures = []
        
        # Check 1: Temperature within limits?
        if proposed_temp > specs["max_temperature_c"]:
            failures.append(ValidationFailure(
                parameter="temperature",
                current=current_temp,
                proposed=proposed_temp,
                limit=specs["max_temperature_c"],
                margin_percent=((proposed_temp - specs["max_temperature_c"]) / specs["max_temperature_c"] * 100)
            ))
        else:
            # Calculate safety margin
            margin_to_max = specs["max_temperature_c"] - proposed_temp
            margin_percent = (margin_to_max / specs["max_temperature_c"]) * 100
            
            if margin_percent < 10:
                failures.append(ValidationFailure(
                    parameter="temperature",
                    severity="WARNING",
                    message=f"Only {margin_percent:.0f}% margin to max temperature"
                ))
        
        # Check 2: Pressure within limits?
        if proposed_pressure > specs["max_pressure_bar"]:
            failures.append(ValidationFailure(
                parameter="pressure",
                current=current_pressure,
                proposed=proposed_pressure,
                limit=specs["max_pressure_bar"]
            ))
        
        # Check 3: Vibration within limits?
        if proposed_vibration > specs["max_vibration_hz"]:
            failures.append(ValidationFailure(
                parameter="vibration",
                current=current_vibration,
                proposed=proposed_vibration,
                limit=specs["max_vibration_hz"]
            ))
        
        # Aggregate
        if failures:
            return ValidationResult(
                is_safe=False,
                failures=failures,
                recommendation="Do NOT apply this change. Exceeds safety limits."
            )
        else:
            return ValidationResult(
                is_safe=True,
                safety_margins={
                    "temperature": margin_percent,
                    "pressure": ((specs["max_pressure_bar"] - proposed_pressure) / specs["max_pressure_bar"] * 100),
                    "vibration": ((specs["max_vibration_hz"] - proposed_vibration) / specs["max_vibration_hz"] * 100),
                }
            )
```

### **Sensor Fusion + Context**

```python
class SensorFusionAgent(Agent):
    """
    Raw sensor data is noisy. Fuse multiple sensors for context.
    
    Don't trust a single temperature sensor.
    Look at: temperature + vibration + power consumption + acoustic emissions.
    
    If they all agree, confidence is high.
    If they disagree, something is wrong (sensor failure? real anomaly?).
    """
    
    def diagnose_bearing_health(self, equipment: str) -> BearingHealthReport:
        """
        Multiple signals for bearing health.
        Single signal is ambiguous.
        """
        
        signals = {
            "temperature": self.get_temperature(equipment),
            "vibration": self.get_vibration(equipment),
            "acoustic_emission": self.get_acoustic(equipment),
            "power_consumption": self.get_power(equipment),
            "lubrication_age": self.get_lubrication_hours(equipment)
        }
        
        # Assess each signal
        assessments = {
            "temperature": self.assess_temperature(signals["temperature"]),
            # "normal", "elevated", "critical"
            
            "vibration": self.assess_vibration(signals["vibration"]),
            # "low", "moderate", "high", "very_high"
            
            "acoustic": self.assess_acoustic(signals["acoustic_emission"]),
            # "quiet", "moderate", "noisy"
        }
        
        # Consensus: What's the most likely state?
        consensus = self.consensus_diagnosis(assessments)
        
        # Confidence: Do signals agree?
        if all(a == consensus for a in assessments.values()):
            confidence = 0.95  # All signals agree
        elif 2 out of 3 agree:
            confidence = 0.70  # Majority agree, one might be faulty
        else:
            confidence = 0.40  # Signals conflict, something is wrong
        
        # Confidence too low? Investigate sensor health
        if confidence < 0.50:
            sensor_health_check = self.check_sensor_health(equipment)
            return BearingHealthReport(
                consensus=consensus,
                confidence=confidence,
                warning="Conflicting sensor signals. Sensor malfunction possible.",
                sensor_check=sensor_health_check,
                recommendation="Investigate sensor reliability before trusting assessment"
            )
        
        # High confidence: Make recommendation
        if consensus == "critical":
            return BearingHealthReport(
                consensus=consensus,
                confidence=confidence,
                recommendation="STOP PRODUCTION. Bearing likely failing.",
                expected_failure_time="< 4 hours",
                action="Schedule maintenance immediately"
            )
        elif consensus == "elevated":
            return BearingHealthReport(
                consensus=consensus,
                confidence=confidence,
                recommendation="Increase monitoring. Schedule maintenance within 48 hours.",
                expected_failure_time="< 2 weeks"
            )
        else:
            return BearingHealthReport(
                consensus=consensus,
                confidence=confidence,
                recommendation="Normal operation. Continue routine maintenance schedule."
            )
```

---

## Case Studies: Where Physical Consequences Matter

### **Case Study 1: Toyota's Supply Chain Visibility with IBM**

**The Problem**
Toyota manufactures 10 million vehicles per year. Each car has ~30,000 parts.
If one supplier delays, the whole line stops. Cost: $500K per hour of downtime.

Traditional approach: Weekly supplier status reports (by then, it's too late).
Goal: Real-time visibility. Alert 1-2 weeks before supply breaks.

**The Solution: IoT Sensors + Predictive Models**

```
SUPPLIER'S WAREHOUSE:
├─ Inventory levels (RFID tags)
├─ Production rates (sensor on assembly line)
├─ Quality metrics (defect detection camera)
├─ Shipping readiness (packing line status)

        │
        ├─→ [REAL-TIME MONITORING]
        │   If inventory drops below 2-week buffer:
        │   → Alert: "Component X at risk in 10 days"
        │
        ├─→ [PREDICTIVE MODEL]
        │   Given current production rate, inventory level, seasonal demand:
        │   "When will this supplier run out of stock?"
        │   Prediction: "14 days" (with confidence 85%)
        │
        ├─→ [ESCALATION ROUTING]
        │   14 days out:
        │   → Notify Toyota procurement (low urgency)
        │   → Supplier increases production
        │
        │   7 days out:
        │   → Notify Toyota executive
        │   → Start looking for backup supplier
        │
        │   2 days out:
        │   → URGENT: Halt production plan
        │   → Activate emergency supplier
        │
        └─→ [PREVENTION]
            Better than reacting: Predict earlier
```

**Key Design: Confidence + Uncertainty Quantification**

```python
class SupplyChainPredictor(Agent):
    """
    Predictions are probabilistic, not certain.
    Must communicate uncertainty.
    """
    
    def predict_stockout(
        self,
        supplier: Supplier,
        component: Component
    ) -> StockoutPrediction:
        
        # Current state
        inventory = supplier.get_inventory(component)
        daily_production = supplier.get_production_rate(component)
        daily_demand = self.get_demand_forecast(component)
        
        # Calculation
        net_daily_change = daily_production - daily_demand
        days_to_stockout = inventory / abs(net_daily_change) if net_daily_change < 0 else float('inf')
        
        # Uncertainty factors
        uncertainty_sources = {
            "demand_forecast": 0.15,  # ±15% error in demand prediction
            "production_variability": 0.10,  # ±10% in production rate
            "supplier_communication_lag": 1,  # 1 day delay in data update
            "seasonal_variation": 0.20 if is_peak_season else 0.05
        }
        
        # Confidence interval
        confidence_interval = self.calculate_confidence(
            prediction=days_to_stockout,
            uncertainty_sources=uncertainty_sources
        )
        # Result: "Stockout in 14 days (±3 days, 85% confidence)"
        
        # Alert logic
        alerts = []
        
        if days_to_stockout < 14:
            alerts.append(Alert(
                level="LOW",
                message="Monitor closely. May need to adjust production schedule.",
                action="Weekly check-ins with supplier"
            ))
        
        if days_to_stockout < 7:
            alerts.append(Alert(
                level="MEDIUM",
                message="Supply at risk. Consider activating backup supplier.",
                action="Daily check-ins. Prepare contingency plan."
            ))
        
        if days_to_stockout < 2:
            alerts.append(Alert(
                level="CRITICAL",
                message="Imminent stockout. Execute contingency now.",
                action="Switch to backup supplier. Halt dependent production."
            ))
        
        return StockoutPrediction(
            days_to_stockout=days_to_stockout,
            confidence_interval=confidence_interval,
            confidence_percent=85,
            alerts=alerts,
            recommendation={
                "if_14_plus_days": "Continue normal operations",
                "if_7_to_14_days": "Begin contingency preparation",
                "if_2_to_7_days": "Activate backup supplier",
                "if_less_than_2_days": "Emergency procurement"
            }
        )
```

**Real Numbers**
- System reduced unplanned production halts by 60%
- Average lead time on procurement: 2 weeks → 4 days
- Cost savings: ~$100M/year (fewer emergency suppliers, better negotiation)
- Accuracy: Predictions within ±2 days for 85% of cases

---

### **Case Study 2: Iberdrola's IT Ops Multi-Agent for Electrical Grid**

**The Problem**
Iberdrola manages Spain's electricity grid. The grid has:
- 47,000 km of power lines
- 2,000+ substations
- Real-time demand (people turning on lights, factories ramping up)
- Real-time supply (renewables go offline if clouds pass)

One misconfiguration = blackout affecting millions.

**The Solution: Multi-Agent Coordination for Grid Reconfiguration**

```
GRID STATE (every 5 seconds):
├─ Real-time demand (MW)
├─ Real-time supply (wind, solar, hydro, thermal)
├─ Line loading (% of capacity)
├─ Frequency (must stay near 50 Hz)
├─ Voltage (must stay within ±10%)

        │
        ├─→ [DEMAND FORECASTER AGENT]
        │   Predict: What will demand be in 15 minutes?
        │   Based on: Time of day, weather, historical patterns
        │   Confidence: 95% (15 minutes is short)
        │
        ├─→ [SUPPLY FORECASTER AGENT]
        │   Predict: What will wind/solar supply be in 15 minutes?
        │   Based on: Cloud cover, wind speed, time of day
        │   Confidence: 70% (weather is unpredictable)
        │
        ├─→ [FEASIBILITY AGENT]
        │   Question: Can we meet forecasted demand with forecasted supply?
        │   If yes: Continue
        │   If no: Need to activate additional capacity
        │
        ├─→ [GRID RECONFIGURATION AGENT]
        │   Question: Which thermal plants should we activate?
        │   Which lines should we balance?
        │   Minimize cost, maximize efficiency
        │
        ├─→ [SAFETY VALIDATION AGENT]
        │   Check: Does the new configuration violate constraints?
        │   Constraints:
        │   - No line exceeds 85% of capacity
        │   - Frequency stays 49.5-50.5 Hz
        │   - Voltage stays within limits
        │   - All regions have N-1 redundancy
        │     (if one line fails, rest of grid stays up)
        │
        └─→ [HUMAN AUTHORIZATION]
            Operator approves reconfiguration
            → [EXECUTION AGENT]
            → Apply changes in sequence (not all at once)
            → Monitor for cascading effects
            → Rollback if problems
```

**Key Design: Symbolic Validation Before Any Change**

```python
class GridReconfigurationValidator(Agent):
    """
    Physical constraint: Grid must stay stable during AND after changes.
    Can't just calculate the final state.
    Must verify the transition is safe.
    """
    
    def validate_reconfiguration(
        self,
        current_config: GridConfiguration,
        proposed_config: GridConfiguration
    ) -> ValidationResult:
        
        # Check 1: Is final state feasible?
        final_state_feasible = self.check_feasibility(proposed_config)
        if not final_state_feasible:
            return ValidationResult(
                is_safe=False,
                reason="Proposed configuration is infeasible"
            )
        
        # Check 2: Can we reach final state from current state?
        transition_sequence = self.plan_transition(current_config, proposed_config)
        
        for step_number, step_config in enumerate(transition_sequence):
            # During transition, some constraints might be violated temporarily
            # That's OK, as long as we don't violate safety limits
            
            violations = self.check_constraints(step_config)
            
            for violation in violations:
                if violation.is_safety_critical:
                    # Can't violate safety constraints even temporarily
                    return ValidationResult(
                        is_safe=False,
                        reason=f"Step {step_number + 1} violates safety: {violation.description}",
                        recommendation="Choose different reconfiguration path"
                    )
                else:
                    # Non-critical violations are temporary discomfort (e.g., brief overvoltage)
                    # Log them but don't block
                    pass
        
        # Check 3: Is there redundancy maintained at all steps?
        for step_config in transition_sequence:
            if not self.has_n_minus_1_redundancy(step_config):
                return ValidationResult(
                    is_safe=False,
                    reason="Transition removes redundancy",
                    recommendation="Add backup line before reconfiguring"
                )
        
        return ValidationResult(
            is_safe=True,
            transition_sequence=transition_sequence,
            estimated_time_to_complete="3 minutes"
        )
```

**Real Numbers**
- Grid frequency stability: ±0.02 Hz (within spec)
- No blackouts caused by agent misconfigurations (100% record)
- Renewable energy integration: 50% of supply (and growing)
- Costs: Agents reduced manual operations by 40%

---

### **Case Study 3: Snorkel AI's Insurance Underwriting**

**The Problem**
Insurance underwriting traditionally needs human review:
- Customer applies for coverage
- Underwriter reviews claim history, health records, lifestyle
- Underwriter decides: Approve, Deny, or Offer Alternative Terms

This is slow (weeks to months) and subjective (different underwriters = different decisions).

**The Solution: Programmatic Data Labeling + ML**

Snorkel's insight: You don't need a perfect model. You need a consistent model that humans can verify.

```
Insurance Application
├─ Policy type (life, health, auto)
├─ Customer data
├─ Claim history
├─ Health records (if relevant)
├─ Lifestyle signals (social media, commercial data)

        │
        ├─→ [RULE-BASED SCREENING]
        │   If age > 75 AND applying for life insurance:
        │   → Send to human expert (age-related complexity)
        │
        │   If no claim history AND good credit score:
        │   → Likely approve (low risk)
        │
        │   If multiple claims in last 2 years:
        │   → Send to human (possible claim pattern)
        │
        ├─→ [DATA LABELING FUNCTIONS] (Snorkel)
        │   Instead of single model with single answer,
        │   run multiple "labeling functions" that each vote
        │
        │   Function 1: "If age < 30 AND no claims → Likely approve"
        │              Confidence: 90%
        │
        │   Function 2: "If BMI > 35 AND applying for life insurance
        │              → Likely higher premium"
        │              Confidence: 80%
        │
        │   Function 3: "If recent surgery in last 6 months
        │              → Uncertain, need human review"
        │              Confidence: 40% (explicitly uncertain)
        │
        ├─→ [AGGREGATION]
        │   Combine votes from labeling functions
        │   Weight by confidence
        │   Generate recommendation: APPROVE, DENY, HUMAN_REVIEW
        │
        └─→ [HUMAN REVIEW FOR UNCERTAIN CASES]
            Where ML confidence < 70%:
            → Human underwriter decides
            → Human decision feeds back into model training
            → Model improves over time
```

**Key Design: Uncertainty-Driven Escalation**

```python
class InsuranceUnderwriter(Agent):
    """
    Don't optimize for binary accuracy (approve/deny).
    Optimize for: "Do I know enough to decide?"
    
    If confidence is low, escalate to human.
    """
    
    def underwrite_application(
        self,
        application: InsuranceApplication
    ) -> UnderwritingDecision:
        
        # Run multiple labeling functions
        votes = {
            "age_risk": self.assess_age_risk(application),
            # Returns: (recommendation, confidence)
            # E.g., (APPROVE, 0.85) or (DENY, 0.60) or (REVIEW, 0.40)
            
            "health_risk": self.assess_health_risk(application),
            "lifestyle_risk": self.assess_lifestyle_risk(application),
            "claim_history": self.assess_claim_history(application),
        }
        
        # Aggregate
        confidences = {k: v[1] for k, v in votes.items()}
        recommendations = {k: v[0] for k, v in votes.items()}
        
        avg_confidence = sum(confidences.values()) / len(confidences)
        
        if avg_confidence > 0.85:
            # High confidence: Make decision
            final_recommendation = self.majority_vote(recommendations)
            
            return UnderwritingDecision(
                recommendation=final_recommendation,
                confidence=avg_confidence,
                reasoning={k: f"{recommendations[k]} (confidence {confidences[k]:.0%})"
                          for k in recommendations}
            )
        
        elif avg_confidence > 0.60:
            # Medium confidence: Escalate with context
            return UnderwritingDecision(
                recommendation="HUMAN_REVIEW",
                confidence=avg_confidence,
                context_for_human={
                    "votes": recommendations,
                    "confidence_breakdown": confidences,
                    "uncertain_areas": [k for k, c in confidences.items() if c < 0.70],
                    "likely_decision": self.majority_vote(recommendations)
                }
            )
        
        else:
            # Low confidence: Full human review
            return UnderwritingDecision(
                recommendation="EXPERT_REVIEW",
                reason="Insufficient confidence across all factors",
                escalate_to="Senior underwriter"
            )
```

**Real Numbers**
- 60% of applications approved automatically (vs. 30% before)
- Processing time: 3 days → 4 hours for auto-approved
- Human review time: Reduced 40% (they focus on complex cases)
- Consistency: Agreements between underwriters increased 25%
- Customer satisfaction: 88% (faster decisions, clear reasoning)

---

### **Case Study 4: Georgia-Pacific's Manufacturing RAG + Multi-Model**

**The Problem**
Georgia-Pacific manufactures tissue products (paper towels, napkins).
Production depends on:
- Raw material quality (wood pulp)
- Machine settings (temperature, pressure, speed)
- Environmental conditions (humidity)
- Quality metrics (thickness, softness, strength)

If machine settings are wrong, they waste $50K in raw materials and lose customer contracts.

**The Solution: RAG (Retrieval-Augmented Generation) + Multi-Model Routing**

```
NEW BATCH ARRIVING:
├─ Material specs (quality, moisture content)
├─ Environmental conditions (temperature, humidity)
├─ Customer specs (thickness tolerance, softness target)

        │
        ├─→ [MATERIAL DATABASE RETRIEVAL]
        │   Retrieve: Historical batches with similar material specs
        │   Learn: What settings worked for this material?
        │   Confidence: Based on how similar the historical batch is
        │
        ├─→ [MACHINE SIMULATION]
        │   Given: Material specs + settings
        │   Predict: Temperature profile, moisture levels, output quality
        │   Model: Physics + ML (hybrid)
        │
        ├─→ [QUALITY PREDICTION]
        │   Estimate: Will output meet customer specs?
        │   Estimate: Scrap rate (% of output that's unusable)
        │
        ├─→ [RECOMMENDATION ENGINE]
        │   "For this material, recommend settings: T=145°C, speed=800 m/min"
        │   Reasoning: "Historical batch #4521 was similar, these settings worked"
        │   Risk: "5% predicted scrap rate (within tolerance)"
        │
        └─→ [HUMAN APPROVAL]
            Operator reviews:
            - Recommended settings
            - Historical analogs
            - Risk assessment
            - Approves or modifies
```

**Key Design: Multi-Model Routing**

Different batches need different approaches:

```python
class ManufacturingAdvisor(Agent):
    """
    Not a single model. Multiple models. Route to the best one.
    """
    
    def get_production_settings(
        self,
        material_batch: MaterialBatch,
        customer_specs: CustomerSpecs
    ) -> ProductionSettings:
        
        # Step 1: Classify batch type
        batch_type = self.classify_batch(material_batch)
        # "Standard", "Premium", "Recycled", "Blended", "Rare"
        
        # Step 2: Route to appropriate model/advisor
        if batch_type == "Standard":
            # Use historical retrieval (we have lots of data)
            advisor = self.get_historical_advisor()
            result = advisor.recommend(material_batch, customer_specs)
        
        elif batch_type == "Premium":
            # Rare, expensive material. Use physics simulation.
            advisor = self.get_physics_simulator()
            result = advisor.recommend(material_batch, customer_specs)
        
        elif batch_type == "Recycled":
            # Unpredictable. Use hybrid: Rules + ML
            advisor = self.get_hybrid_advisor()
            result = advisor.recommend(material_batch, customer_specs)
        
        # Step 3: Validate recommendation
        validation = self.validate_settings(result.settings, material_batch)
        
        if validation.is_safe:
            return ProductionSettings(
                settings=result.settings,
                reasoning=result.reasoning,
                confidence=result.confidence,
                predicted_scrap_rate=result.predicted_scrap,
                approval_required=result.confidence < 0.80
            )
        else:
            return ProductionSettings(
                settings=None,
                reasoning=result.reasoning,
                warning=validation.failure_reason,
                approval_required=True,
                escalate_to="Shift supervisor"
            )
```

**Real Numbers**
- Scrap rate reduced: 8% → 3%
- Production throughput: +12% (fewer errors, less downtime)
- Material waste: $2M savings/year
- Customer complaints: 40% reduction (better consistency)

---

## The Key Design Question: What's the Minimum Safety Architecture?

**Scenario**: Iberdrola's grid agent wants to recommend reconfiguring 100 power lines.

**Question**: Before applying this, what must be proven?

**Answer** (in order of importance):

1. **Physical Feasibility**
   - Can we reach the proposed state from the current state?
   - Will we stay within operational limits during transition?

2. **Redundancy Maintenance**
   - If any single line fails during transition, does the grid stay stable?
   - (N-1 redundancy: Grid works even if one component fails)

3. **Safety Margin**
   - What's the margin to failure for each constraint?
   - No constraint should be closer than 10% to limit

4. **Staged Rollout**
   - Can we apply changes incrementally?
   - Can we stop at any step and rollback if needed?

5. **Monitoring + Automatic Rollback**
   - What signals indicate the change went wrong?
   - If detected, rollback in < 1 second

6. **Human Approval**
   - Is the final decision made by a human who understands the implications?
   - Is there an audit trail?

```python
class SafetyArchitecture(Agent):
    """
    Minimum requirements before any industrial agent can change anything.
    """
    
    def is_safe_to_execute(self, recommendation: Recommendation) -> bool:
        
        checks = [
            self.is_physically_feasible(recommendation),
            self.maintains_redundancy(recommendation),
            self.has_safety_margins(recommendation),
            self.can_be_staged(recommendation),
            self.has_monitoring_and_rollback(recommendation),
            self.has_human_approval(recommendation),
        ]
        
        return all(checks)
```

If even one check fails, don't execute.

---

## Cross-Domain Lessons

### **1. Sensor Data Is Noisy—Fuse Multiple Signals**
Don't trust a single temperature sensor. Use temperature + vibration + power + acoustic.
Multiple signals agreeing = high confidence.
Signals conflicting = investigate sensor health.

### **2. Physics Constraints Must Be Explicit**
Don't learn machine limits from data.
Encode them explicitly: Max temperature, max pressure, rated power.
These are safety-critical.

### **3. Staged Rollout Is Mandatory for Physical Systems**
Don't apply recommendations to 100% at once.
Start with 1%, then 10%, then 100%.
Monitor at each stage. Rollback if problems.

### **4. Confidence ≠ Accuracy**
A model can be confident and wrong.
Implement uncertainty quantification.
If confidence < threshold, escalate to human.

### **5. Humans Execute Recommendations**
Agents generate recommendations. Humans implement them.
Make sure humans can:
- Understand the recommendation
- Spot problems in execution
- Stop the process if something goes wrong

---

## Further Reading

- Snorkel AI papers on programmatic labeling
- Toyota's "Supply Chain Risk Management" papers
- Iberdrola's "Grid Modernization" white papers
- NIST "Cybersecurity Framework" (applies to industrial control systems)
- IEEE "Industrial Automation Standards"
