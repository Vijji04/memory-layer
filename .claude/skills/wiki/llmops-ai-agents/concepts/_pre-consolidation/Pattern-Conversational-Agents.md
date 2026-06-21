---
title: Pattern: Conversational Agents
created: 2026-05-12
updated: 2026-05-12
type: concept
tags: [phase-2, llmops-ai-agents, concept, patterns, conversational, case-studies]
confidence: high
source_files: 1
---

# Pattern: Conversational Agents

When agents talk to customers—not engineers—everything changes. You need intent routing, stateful conversation, guardrails, and escalation logic. A single wrong response costs you a customer. This section covers three real systems handling millions of conversations, each with different constraints and failure modes.

The core challenge: **conversation state is precious and fragile**. Track it wrong and you'll repeat yourself. Route wrong and the customer gets transferred endlessly. Allow the wrong guardrail and you expose sensitive data or violate policy.

---

## Case Study 1: Booking.com — GenAI Agent for Partner-Guest Messaging

### The Business Problem

Booking.com connects 1.5M+ properties with 200M+ annual guests. Partners (hoteliers, property managers) need to communicate with guests at scale:

- "Guest asks if early check-in is available"
- "Guest requests dietary restrictions for breakfast"
- "Guest reports a maintenance issue"
- "Guest wants to extend their stay"

Handling this manually requires a small army of support staff. Booking built a **GenAI messaging agent** that:
1. Classifies incoming guest messages (intent)
2. Routes to the right response handler
3. Generates responses respecting property-specific policies
4. Checks tone and compliance
5. Either sends or escalates to human

The system processes millions of conversations daily across thousands of properties, each with unique policies.

### Why This Pattern Fits

**Conversational agents** solve the routing + guardrail problem:
- **Intent classification** routes messages to the right handler (maintenance, booking changes, customer service, etc.)
- **Policy checking** ensures responses comply with property rules and regulations
- **Tone guardrails** maintain brand voice and prevent off-tone responses
- **Escalation gates** catch edge cases (complaints, ambiguous requests) and send to humans

Booking's constraints:
- High volume (millions of messages)
- Latency-sensitive (guests expect response in <1 hour)
- High-stakes (false escalations hurt properties, missed escalations hurt guests)
- Policy diversity (each property has its own house rules)

### Architecture Diagram

```
┌─────────────────────────────────────────────────────┐
│  Guest Message (arrives in Booking.com inbox)       │
│  "Can I check in early? I have a meeting at 2pm"    │
└────────────────┬────────────────────────────────────┘
                 │
         ┌───────▼──────────────┐
         │ Intent Classifier    │
         │ (LLM)                │
         │                      │
         │ Intent: check_in     │
         │ Confidence: 0.95     │
         └───────┬──────────────┘
                 │
    ┌────────────▼───────────────┐
    │ Intent Router              │
    │ check_in → Booking handler │
    └────────────┬───────────────┘
                 │
    ┌────────────▼────────────────────┐
    │ Fetch Property Policies         │
    │                                │
    │ Early check-in allowed: 2pm     │
    │ Requires front desk approval: Y │
    │ Response template: friendly     │
    └────────────┬───────────────────┘
                 │
    ┌────────────▼──────────────────────────┐
    │ Generate Candidate Response           │
    │                                       │
    │ "We can arrange early check-in at     │
    │  2pm subject to availability. Our     │
    │  front desk will confirm when you     │
    │  arrive."                             │
    └────────────┬───────────────────────────┘
                 │
    ┌────────────▼────────────────┐
    │ Policy Compliance Check     │
    │                            │
    │ • Tone matches brand       │
    │ • No data leaks            │
    │ • Policy-compliant         │
    │ • PASS                     │
    └────────────┬───────────────┘
                 │
    ┌────────────▼────────────────┐
    │ Escalation Threshold Check  │
    │                            │
    │ Confidence > 0.8?          │
    │ Policy complaint? No       │
    │ Ambiguous? No              │
    │ → SEND (no escalation)    │
    └────────────┬───────────────┘
                 │
    ┌────────────▼────────────────┐
    │ Send Response to Guest      │
    │                            │
    │ ✓ Logged in conversation   │
    │ ✓ Timestamp recorded       │
    │ ✓ Metrics tracked          │
    └────────────────────────────┘
```

### Implementation: Key Components

#### 1. Intent Classification Pipeline

```python
from typing import List, Tuple, Dict
from enum import Enum
import anthropic

class MessageIntent(Enum):
    """All possible guest message intents."""
    CHECK_IN_REQUEST = "check_in_request"
    CHECKOUT_REQUEST = "checkout_request"
    BOOKING_MODIFICATION = "booking_modification"
    CANCELLATION = "cancellation_request"
    AMENITY_REQUEST = "amenity_request"
    MAINTENANCE_ISSUE = "maintenance_issue"
    COMPLAINT = "complaint"
    GENERAL_QUESTION = "general_question"
    AMBIGUOUS = "ambiguous"
    ESCALATION_NEEDED = "escalation_needed"

class IntentClassifier:
    """
    Classify guest messages into intents.
    
    Returns: (intent, confidence_score, reasoning)
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        self.intent_examples = {
            MessageIntent.CHECK_IN_REQUEST: [
                "Can I check in early?",
                "Is late check-in available?",
                "I'm arriving at 1am, is that okay?"
            ],
            MessageIntent.MAINTENANCE_ISSUE: [
                "The WiFi isn't working",
                "There's a leak in the bathroom",
                "The heating is broken"
            ],
            MessageIntent.COMPLAINT: [
                "This room is dirty",
                "The service was terrible",
                "I want a refund"
            ],
            MessageIntent.BOOKING_MODIFICATION: [
                "Can I extend my stay?",
                "I need to change my room type",
                "Can I modify my reservation?"
            ]
        }
    
    def classify(self, message: str, property_context: Dict = None) -> Dict:
        """
        Classify a guest message.
        
        Args:
            message: Guest message text
            property_context: Dict with property info (optional)
        
        Returns:
            {
                'intent': MessageIntent,
                'confidence': float (0-1),
                'reasoning': str,
                'alternative_intents': List[Tuple[MessageIntent, float]]
            }
        """
        
        # Build few-shot examples
        examples_text = ""
        for intent, examples in self.intent_examples.items():
            examples_text += f"\n{intent.value}:\n"
            for ex in examples:
                examples_text += f"  - {ex}\n"
        
        system_prompt = f"""You are an expert at understanding guest messages in a hotel booking system.

Classify the following guest message into one of these intents:
{examples_text}

Your response MUST be JSON:
{{
    "intent": "<intent>",
    "confidence": <0-1>,
    "reasoning": "<why this intent>",
    "alternative_intents": [
        {{"intent": "<alt_intent>", "confidence": <0-1>}}
    ]
}}

Be very confident (>0.8) only if the intent is clear.
If ambiguous, return lower confidence (<0.6).
If the message seems hostile or needs human intervention, return "escalation_needed"."""
        
        user_message = f"""Guest Message: "{message}"

Property Context: {property_context or 'None'}

Classify this message."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        # Parse response
        import json
        try:
            result = json.loads(response.content[0].text)
            
            return {
                'intent': MessageIntent(result['intent']),
                'confidence': result['confidence'],
                'reasoning': result['reasoning'],
                'alternative_intents': [
                    (MessageIntent(alt['intent']), alt['confidence'])
                    for alt in result.get('alternative_intents', [])
                ]
            }
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback if parsing fails
            return {
                'intent': MessageIntent.AMBIGUOUS,
                'confidence': 0.3,
                'reasoning': f"Failed to parse classification: {str(e)}",
                'alternative_intents': []
            }

# Usage
classifier = IntentClassifier()

result = classifier.classify(
    "Can I check in early? I have a meeting at 2pm",
    property_context={'name': 'Luxury Hotel NYC', 'check_in': '3pm'}
)

print(f"Intent: {result['intent'].value}")
print(f"Confidence: {result['confidence']:.2f}")
print(f"Reasoning: {result['reasoning']}")
```

#### 2. Intent-Specific Handler Routing

```python
from typing import Callable, Dict
from dataclasses import dataclass
import anthropic

@dataclass
class IntentHandler:
    """Configuration for handling a specific intent."""
    intent: MessageIntent
    required_info: List[str]  # e.g., ['check_in_time', 'room_type']
    guardrails: List[str]     # e.g., ['no_promises_without_approval']
    can_auto_respond: bool
    escalation_threshold: float  # If confidence < this, escalate
    response_template: str

class MessageRouter:
    """
    Route classified messages to intent-specific handlers.
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
        
        self.handlers: Dict[MessageIntent, IntentHandler] = {
            MessageIntent.CHECK_IN_REQUEST: IntentHandler(
                intent=MessageIntent.CHECK_IN_REQUEST,
                required_info=['current_check_in_time', 'guest_arrival_time'],
                guardrails=['no_promises_without_approval', 'check_availability'],
                can_auto_respond=True,
                escalation_threshold=0.7,
                response_template="""Thank you for letting us know. Early check-in at {{time}} is {{status}}.
{{approval_message}}"""
            ),
            
            MessageIntent.COMPLAINT: IntentHandler(
                intent=MessageIntent.COMPLAINT,
                required_info=['complaint_type', 'severity'],
                guardrails=['empathize_first', 'no_auto_refunds'],
                can_auto_respond=False,  # Always escalate complaints
                escalation_threshold=1.0,
                response_template="""We sincerely apologize for {{issue}}. 
Our team will investigate immediately. A manager will contact you shortly."""
            ),
            
            MessageIntent.MAINTENANCE_ISSUE: IntentHandler(
                intent=MessageIntent.MAINTENANCE_ISSUE,
                required_info=['issue_type', 'urgency'],
                guardrails=['safety_first', 'immediate_response'],
                can_auto_respond=True,
                escalation_threshold=0.8,
                response_template="""Thank you for reporting this. Our maintenance team 
has been notified and will address {{issue}} {{urgency_time}}."""
            ),
            
            MessageIntent.BOOKING_MODIFICATION: IntentHandler(
                intent=MessageIntent.BOOKING_MODIFICATION,
                required_info=['modification_type', 'dates'],
                guardrails=['check_availability', 'rate_lock'],
                can_auto_respond=False,  # Requires availability check
                escalation_threshold=0.8,
                response_template="""We'd be happy to help with {{modification}}.
Please provide your booking details or contact our team."""
            ),
        }
    
    def route_and_respond(
        self,
        guest_message: str,
        intent_result: Dict,
        property_context: Dict
    ) -> Dict:
        """
        Route message to appropriate handler and generate response.
        
        Returns:
            {
                'should_send': bool,
                'response': str,
                'escalation_reason': str or None,
                'metadata': Dict
            }
        """
        intent = intent_result['intent']
        confidence = intent_result['confidence']
        
        # Get handler for this intent
        handler = self.handlers.get(intent)
        
        if not handler:
            return {
                'should_send': False,
                'response': None,
                'escalation_reason': f"No handler for intent {intent.value}",
                'metadata': {'intent': intent.value}
            }
        
        # Check escalation threshold
        if confidence < handler.escalation_threshold:
            return {
                'should_send': False,
                'response': None,
                'escalation_reason': f"Low confidence ({confidence:.2f} < {handler.escalation_threshold})",
                'metadata': {'intent': intent.value, 'confidence': confidence}
            }
        
        # Complaints and modifications always escalate
        if not handler.can_auto_respond:
            return {
                'should_send': False,
                'response': None,
                'escalation_reason': f"Intent {intent.value} requires human review",
                'metadata': {'intent': intent.value}
            }
        
        # Generate response using handler template + guardrails
        response = self._generate_response(
            guest_message,
            handler,
            property_context,
            intent_result
        )
        
        return {
            'should_send': True,
            'response': response,
            'escalation_reason': None,
            'metadata': {
                'intent': intent.value,
                'confidence': confidence,
                'handler': handler.intent.value
            }
        }
    
    def _generate_response(
        self,
        guest_message: str,
        handler: IntentHandler,
        property_context: Dict,
        intent_result: Dict
    ) -> str:
        """
        Generate response respecting guardrails.
        """
        guardrails_text = "\n".join([f"- {gr}" for gr in handler.guardrails])
        
        system_prompt = f"""You are a professional hotel guest services agent.

Property: {property_context.get('name')}
Intent: {handler.intent.value}
Reasoning: {intent_result['reasoning']}

GUARDRAILS (MUST FOLLOW):
{guardrails_text}

Generate a helpful, professional, empathetic response.
Keep it under 100 words. Be specific.
Use the template as a guide but customize for the guest's specific situation."""
        
        user_message = f"""Guest Message: "{guest_message}"

Template:
{handler.response_template}

Property Info: {property_context}

Generate response now."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return response.content[0].text

# Usage
router = MessageRouter()

routing_result = router.route_and_respond(
    guest_message="Can I check in early?",
    intent_result=classifier.classify("Can I check in early?"),
    property_context={
        'name': 'Grand Hotel NYC',
        'check_in': '3pm',
        'early_checkin_available': True,
        'early_checkin_fee': 'None'
    }
)

if routing_result['should_send']:
    print(f"SEND: {routing_result['response']}")
else:
    print(f"ESCALATE: {routing_result['escalation_reason']}")
```

#### 3. Policy Compliance & Tone Guardrails

```python
from typing import List
import anthropic
import re

class ComplianceChecker:
    """
    Verify responses comply with property policies and regulations.
    
    Checks:
    - Tone/brand voice consistency
    - No promises without approval
    - No data leaks (PII)
    - Regulatory compliance (GDPR, CCPA)
    - No rate/price disclosure violations
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def check_response(
        self,
        response: str,
        property_context: Dict,
        intent: MessageIntent
    ) -> Dict:
        """
        Check if response is safe to send.
        
        Returns:
            {
                'is_compliant': bool,
                'violations': List[str],
                'tone_score': float (0-1),
                'data_leak_score': float (0-1),
                'policy_score': float (0-1)
            }
        """
        
        violations = []
        
        # 1. Data Leak Check (PII patterns)
        data_leaks = self._check_pii(response)
        if data_leaks:
            violations.append(f"PII Leak: {', '.join(data_leaks)}")
        
        # 2. Tone Check
        tone_result = self._check_tone(response, property_context)
        if tone_result['score'] < 0.6:
            violations.append(f"Tone Issue: {tone_result['issue']}")
        
        # 3. Policy Check
        policy_result = self._check_policy(response, intent, property_context)
        if not policy_result['compliant']:
            violations.append(f"Policy Violation: {policy_result['violation']}")
        
        is_compliant = len(violations) == 0
        
        return {
            'is_compliant': is_compliant,
            'violations': violations,
            'tone_score': tone_result.get('score', 1.0),
            'data_leak_score': 1.0 - min(len(data_leaks) * 0.3, 1.0),
            'policy_score': 1.0 if policy_result['compliant'] else 0.0,
            'details': {
                'tone': tone_result,
                'policy': policy_result,
                'pii': data_leaks
            }
        }
    
    def _check_pii(self, text: str) -> List[str]:
        """
        Detect PII in response (credit cards, email, phone, etc.).
        """
        leaks = []
        
        # Credit card pattern
        if re.search(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', text):
            leaks.append("credit_card_number")
        
        # Email
        if re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text):
            leaks.append("email_address")
        
        # Phone
        if re.search(r'(\+?1?[\s.-]?)?\(?[2-9]\d{2}\)?[\s.-]?[2-9]\d{2}[\s.-]?\d{4}', text):
            leaks.append("phone_number")
        
        # Passport
        if re.search(r'\b[A-Z]{2}\d{6,9}\b', text):
            leaks.append("passport_number")
        
        return leaks
    
    def _check_tone(self, response: str, property_context: Dict) -> Dict:
        """
        Check tone matches property brand.
        """
        brand_voice = property_context.get('brand_voice', 'professional')
        
        system_prompt = f"""Rate the tone of this hotel response.

Brand Voice: {brand_voice}
- 'luxury': formal, elegant, anticipatory
- 'casual': friendly, conversational, approachable
- 'professional': clear, efficient, helpful

Score 0-1 where:
1 = matches brand perfectly
0 = completely wrong tone

Respond with JSON:
{{"score": <0-1>, "issue": "<if score < 0.8, explain why>"}}"""
        
        response_obj = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            system=system_prompt,
            messages=[{"role": "user", "content": response}]
        )
        
        import json
        try:
            return json.loads(response_obj.content[0].text)
        except:
            return {'score': 0.7, 'issue': 'Could not parse tone analysis'}
    
    def _check_policy(
        self,
        response: str,
        intent: MessageIntent,
        property_context: Dict
    ) -> Dict:
        """
        Check if response violates hotel policies.
        """
        policies = {
            MessageIntent.CHECK_IN_REQUEST: "No promises without front desk approval",
            MessageIntent.COMPLAINT: "Empathize first; no commitments without manager approval",
            MessageIntent.BOOKING_MODIFICATION: "Check availability before confirming anything",
            MessageIntent.MAINTENANCE_ISSUE: "Always ask for room number if not provided"
        }
        
        policy = policies.get(intent, "")
        
        # Simple heuristic checks
        violations = []
        
        if intent == MessageIntent.CHECK_IN_REQUEST:
            if "will" in response.lower() and "can" not in response.lower():
                violations.append("Making promise without caveat")
        
        if intent == MessageIntent.COMPLAINT:
            if "refund" in response.lower() or "compensation" in response.lower():
                if "manager" not in response.lower() and "team" not in response.lower():
                    violations.append("Offering compensation without approval")
        
        return {
            'compliant': len(violations) == 0,
            'violation': violations[0] if violations else None,
            'policy': policy
        }

# Usage
checker = ComplianceChecker()

response = "Thank you for reporting this. We'll fix the WiFi immediately."

compliance = checker.check_response(
    response,
    property_context={'brand_voice': 'professional'},
    intent=MessageIntent.MAINTENANCE_ISSUE
)

if compliance['is_compliant']:
    print("✓ Response is safe to send")
else:
    print(f"✗ Violations: {compliance['violations']}")
```

#### 4. Escalation Logic & Human Handoff

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class EscalationTicket:
    """Escalation ticket for human review."""
    conversation_id: str
    guest_message: str
    agent_response: Optional[str]
    reason: str
    intent: MessageIntent
    confidence: float
    property_id: str
    priority: str  # 'low', 'medium', 'high', 'urgent'
    created_at: str

class EscalationManager:
    """
    Handle escalations: determine priority, route to right team, track SLA.
    """
    
    ESCALATION_RULES = {
        MessageIntent.COMPLAINT: {
            'priority_base': 'high',
            'sla_minutes': 15,
            'route_to': 'guest_services'
        },
        MessageIntent.MAINTENANCE_ISSUE: {
            'priority_base': 'medium',
            'sla_minutes': 30,
            'route_to': 'maintenance'
        },
        MessageIntent.CHECK_IN_REQUEST: {
            'priority_base': 'low',
            'sla_minutes': 120,
            'route_to': 'front_desk'
        },
        MessageIntent.BOOKING_MODIFICATION: {
            'priority_base': 'medium',
            'sla_minutes': 60,
            'route_to': 'reservations'
        }
    }
    
    def should_escalate(
        self,
        intent: MessageIntent,
        confidence: float,
        response: Optional[str] = None,
        compliance_result: Optional[Dict] = None
    ) -> bool:
        """
        Determine if message should escalate to human.
        """
        
        # Rule 1: Complaints always escalate
        if intent == MessageIntent.COMPLAINT:
            return True
        
        # Rule 2: Low confidence
        if confidence < 0.7:
            return True
        
        # Rule 3: Compliance issues
        if compliance_result and not compliance_result['is_compliant']:
            return True
        
        # Rule 4: Handler says can't auto-respond
        handler = MessageRouter().handlers.get(intent)
        if handler and not handler.can_auto_respond:
            return True
        
        return False
    
    def create_escalation(
        self,
        conversation_id: str,
        guest_message: str,
        reason: str,
        intent: MessageIntent,
        confidence: float,
        property_id: str,
        agent_response: Optional[str] = None
    ) -> EscalationTicket:
        """
        Create escalation ticket for human review.
        """
        rules = self.ESCALATION_RULES.get(
            intent,
            {'priority_base': 'medium', 'sla_minutes': 60, 'route_to': 'general'}
        )
        
        # Determine priority
        priority = rules['priority_base']
        if confidence < 0.5:
            priority = 'high'
        if 'urgent' in reason.lower() or 'safety' in reason.lower():
            priority = 'urgent'
        
        from datetime import datetime
        
        ticket = EscalationTicket(
            conversation_id=conversation_id,
            guest_message=guest_message,
            agent_response=agent_response,
            reason=reason,
            intent=intent,
            confidence=confidence,
            property_id=property_id,
            priority=priority,
            created_at=datetime.utcnow().isoformat()
        )
        
        # Log to escalation queue
        self._log_escalation(ticket, rules['route_to'])
        
        return ticket
    
    def _log_escalation(self, ticket: EscalationTicket, team: str):
        """
        Log escalation to appropriate team queue.
        """
        print(f"[ESCALATION] {ticket.priority.upper()}")
        print(f"  Team: {team}")
        print(f"  Intent: {ticket.intent.value}")
        print(f"  Reason: {ticket.reason}")
        print(f"  Conversation: {ticket.conversation_id}")

# Usage in full conversation flow
def process_guest_message(
    message: str,
    conversation_id: str,
    property_context: Dict
):
    """
    End-to-end: classify -> route -> check -> escalate or send
    """
    
    classifier = IntentClassifier()
    router = MessageRouter()
    checker = ComplianceChecker()
    escalation_mgr = EscalationManager()
    
    # Step 1: Classify intent
    intent_result = classifier.classify(message, property_context)
    print(f"Intent: {intent_result['intent'].value} ({intent_result['confidence']:.2f})")
    
    # Step 2: Route and generate response
    routing_result = router.route_and_respond(
        message,
        intent_result,
        property_context
    )
    
    if routing_result['escalation_reason']:
        # Escalate: no response generated yet
        ticket = escalation_mgr.create_escalation(
            conversation_id=conversation_id,
            guest_message=message,
            reason=routing_result['escalation_reason'],
            intent=intent_result['intent'],
            confidence=intent_result['confidence'],
            property_id=property_context['id']
        )
        return {
            'action': 'escalate',
            'ticket': ticket,
            'message': f"Escalated to human ({routing_result['escalation_reason']})"
        }
    
    # Step 3: Check compliance
    response = routing_result['response']
    compliance = checker.check_response(
        response,
        property_context,
        intent_result['intent']
    )
    
    if not compliance['is_compliant']:
        # Fail-safe: escalate if compliance fails
        ticket = escalation_mgr.create_escalation(
            conversation_id=conversation_id,
            guest_message=message,
            reason=f"Compliance failed: {compliance['violations']}",
            intent=intent_result['intent'],
            confidence=intent_result['confidence'],
            property_id=property_context['id'],
            agent_response=response
        )
        return {
            'action': 'escalate',
            'ticket': ticket,
            'message': "Response failed compliance check, escalated to human"
        }
    
    # Step 4: Send response
    return {
        'action': 'send',
        'response': response,
        'message': "Response sent to guest"
    }

# Test
result = process_guest_message(
    message="Can I check in early at 1pm?",
    conversation_id="conv_12345",
    property_context={
        'id': 'prop_456',
        'name': 'Grand Hotel',
        'brand_voice': 'professional',
        'check_in': '3pm'
    }
)

print(f"\nResult: {result['action']}")
print(f"Message: {result['message']}")
```

### Design Decisions & Why

**1. Why Intent Classification First?**
- Routing depends on intent. Misclassify and you send the wrong response.
- Low confidence on intent → escalate. Better to be safe.
- Intent is stable; it doesn't change as you generate response.

**2. Why Template-Based Response Generation?**
- Templates ensure consistency and brand voice
- LLM fills in specifics (guest name, dates, issue type)
- Reduces hallucination (LLM can't invent new policies)
- Easier to audit (template + LLM delta is clear)

**3. Why Compliance Before Send?**
- Response generation can go wrong (promise without approval, leak data, wrong tone)
- Compliance check is a safety gate: if it fails, escalate immediately
- Violations are specific and actionable (PII, tone, policy)

**4. Why Always-Escalate Rules?**
- Complaints → always human. A complaint needs empathy and judgment.
- Modifications → always human. You need to check availability.
- These rules are non-negotiable; no auto-response is worth the risk.

**5. Why Track Confidence?**
- Confidence <0.7 suggests ambiguity. When in doubt, escalate.
- Confidence score explains to human why escalation happened.
- Useful for metrics: what % of intents need human follow-up?

### Key Takeaways

1. **Intent classification is the pivot point**: everything downstream (routing, guardrails, escalation) depends on getting it right. Low confidence → escalate.

2. **Policy compliance is not optional**: check for data leaks, tone mismatches, and policy violations before sending. Escalate on any failure.

3. **Escalation rules should be explicit**: document which intents/conditions require human review. Default to escalating when unsure.

4. **Guardrails are intent-specific**: check-in response has different guardrails than complaint response. Bake guardrails into handler config.

5. **Track metrics at every gate**: classification confidence, compliance pass rate, escalation rate. Use these to iterate on guardrails and handlers.

---

## Case Study 2: Anthology — AI Contact Center for University Students

### The Business Problem

Anthology serves 1,500+ universities and 50M+ students. Their student services systems handle:
- **Financial aid**: "Am I eligible? When will I receive aid? How much?"
- **Enrollment**: "What's my registration status? When can I register?"
- **Housing**: "Where's my housing assignment? Can I change dorms?"

Universities expect 24/7 support. A single human contact center can't handle 50M students. But student questions are high-stakes: missing financial aid deadlines costs students thousands. Enrollment holds destroy graduation timelines. **Emotional intelligence matters**—distressed students need empathy, not robotic responses.

Anthology built a **multi-agent contact center** where:
1. Voice/text intake captures intent and emotional state
2. Specialist agents handle different domains (financial aid, enrollment, etc.)
3. High-value or emotional questions route to humans
4. Complex multi-domain questions → orchestrator agent

### Why This Pattern Fits

**Multi-agent systems** solve the specialist problem:
- Each domain (financial aid, enrollment, housing) has specialized knowledge
- Specialist agents can enforce domain-specific rules and escalation logic
- Orchestrator routes complex questions to the right specialist
- Human escalation gate catches distressed students

The complexity: **domain separation with shared context**.
- Student's name and ID are needed everywhere
- Financial aid agent shouldn't access housing data
- But enrollment holds might prevent financial aid processing
- How do you pass context between specialists without data leaks?

### Architecture Diagram

```
┌──────────────────────────────────────────────┐
│     Student Query (Voice/Text)               │
│  "I haven't received my financial aid yet"   │
└──────────────────┬───────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  Intent Classifier  │
        │  + Emotional State  │
        │                     │
        │  Intent: financial  │
        │  Emotion: worried   │
        └──────────┬──────────┘
                   │
    ┌──────────────▼────────────────────┐
    │  Orchestrator Agent               │
    │                                   │
    │  Route to specialist:             │
    │  - Single domain? →               │
    │    Direct to specialist           │
    │  - Multi-domain? →                │
    │    Plan sequence of calls         │
    └──────────────┬────────────────────┘
                   │
    ┌──────────────▼──────────────────────────┐
    │  Financial Aid Specialist Agent        │
    │                                        │
    │  • Access: student id, aid status      │
    │  • Tools: check status, view amount    │
    │  • Policies: disbursement dates        │
    │  • Escalation: if holds, if emotional  │
    └──────────────┬───────────────────────┘
                   │
    ┌──────────────▼──────────────────┐
    │  Emotional Distress Check       │
    │                                 │
    │  Keyword: "haven't received"    │
    │  Tone: worried, urgent          │
    │  Resolution: complex (hold)     │
    │  → Escalate to human           │
    └──────────────┬──────────────────┘
                   │
    ┌──────────────▼────────────────────┐
    │  Human Agent Handoff             │
    │                                  │
    │  Context passed:                 │
    │  • Student history               │
    │  • What agent found              │
    │  • Why it escalated              │
    │  • Student's emotional state     │
    │                                  │
    │  Human provides:                 │
    │  • Empathy + explanation         │
    │  • Resolution path               │
    │  • Future-proofing               │
    └─────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Emotional State Detection

```python
from enum import Enum
from dataclasses import dataclass
import anthropic

class EmotionalState(Enum):
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    DISTRESSED = "distressed"
    ANGRY = "angry"
    SATISFIED = "satisfied"

@dataclass
class ConversationContext:
    """
    Track conversation state across agents.
    """
    student_id: str
    student_name: str
    conversation_history: List[str]
    intent: str
    emotional_state: EmotionalState
    escalation_reasons: List[str] = None
    resolved: bool = False

class EmotionalStateDetector:
    """
    Detect student's emotional state from input.
    
    Used to:
    - Adjust agent tone (empathetic vs efficient)
    - Trigger escalation (distressed → human)
    - Track student satisfaction
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def detect(self, text: str) -> Dict:
        """
        Analyze emotional state of student message.
        
        Returns:
            {
                'state': EmotionalState,
                'confidence': float,
                'signals': List[str],
                'urgency': str ('low', 'medium', 'high', 'critical')
            }
        """
        
        system_prompt = """Analyze the emotional state of a student's message.

Emotional states:
- NEUTRAL: factual, straightforward question
- CONCERNED: worried, wants clarification
- DISTRESSED: anxious, urgent, problem that affects their future
- ANGRY: frustrated, demanding, escalating
- SATISFIED: grateful, resolved

Respond with JSON:
{
    "state": "<STATE>",
    "confidence": <0-1>,
    "signals": ["<phrase1>", "<phrase2>"],
    "urgency": "<low|medium|high|critical>"
}

Critical urgency if: deadline passed, hold blocking graduation, no aid received yet.
High urgency if: missing deadline soon, uncertain about process.
"""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            system=system_prompt,
            messages=[{"role": "user", "content": text}]
        )
        
        import json
        try:
            result = json.loads(response.content[0].text)
            return {
                'state': EmotionalState(result['state'].lower().replace(' ', '_')),
                'confidence': result['confidence'],
                'signals': result.get('signals', []),
                'urgency': result.get('urgency', 'medium')
            }
        except:
            return {
                'state': EmotionalState.NEUTRAL,
                'confidence': 0.5,
                'signals': [],
                'urgency': 'medium'
            }

# Usage
detector = EmotionalStateDetector()

state = detector.detect("I haven't received my financial aid yet and I'm really worried. My tuition is due next week.")

print(f"Emotional State: {state['state'].value}")
print(f"Urgency: {state['urgency']}")
print(f"Signals: {', '.join(state['signals'])}")
```

#### 2. Specialist Agent Architecture

```python
from abc import ABC, abstractmethod
from typing import Optional

class SpecialistAgent(ABC):
    """
    Base class for domain-specific agents.
    """
    
    def __init__(self, domain: str, authorized_fields: List[str]):
        self.domain = domain
        self.authorized_fields = authorized_fields  # What data this agent can access
        self.client = anthropic.Anthropic()
    
    @abstractmethod
    def handle_query(self, query: str, context: ConversationContext) -> Dict:
        """
        Handle student query in this domain.
        
        Returns:
            {
                'response': str,
                'answer': str or None,
                'should_escalate': bool,
                'escalation_reason': str or None,
                'follow_up_agents': List[str]  # Other agents to consult
            }
        """
        pass
    
    def _check_authorization(self, student_id: str, field: str) -> bool:
        """
        Verify agent is authorized to access this student data.
        Privacy/compliance gate.
        """
        return field in self.authorized_fields

class FinancialAidAgent(SpecialistAgent):
    """
    Handles financial aid questions: eligibility, status, amounts, disbursement.
    """
    
    def __init__(self, aid_database):
        super().__init__(
            domain="financial_aid",
            authorized_fields=[
                'aid_status', 'aid_amount', 'eligibility', 
                'disbursement_date', 'holds', 'fafsa_status'
            ]
        )
        self.aid_db = aid_database
    
    def handle_query(self, query: str, context: ConversationContext) -> Dict:
        """
        Respond to financial aid question.
        """
        
        # Check what student is asking about
        classification = self._classify_query(query)
        
        # Fetch relevant student data
        student_aid = self.aid_db.get_student(context.student_id)
        
        # Detect escalation triggers
        escalation_reason = None
        
        # Trigger 1: Student is distressed
        if context.emotional_state in [EmotionalState.DISTRESSED, EmotionalState.ANGRY]:
            escalation_reason = "Student is distressed/angry, needs human support"
        
        # Trigger 2: Complex situation (holds, delays)
        if student_aid.get('status') == 'on_hold':
            escalation_reason = "Student has financial aid hold, needs specialist review"
        
        # Trigger 3: Aid not received and deadline is approaching
        if (student_aid.get('status') == 'pending' and 
            self._days_until_deadline() < 7):
            escalation_reason = "Aid not received, deadline imminent"
        
        if escalation_reason:
            return {
                'response': f"I understand this is urgent. Let me connect you with a specialist who can help.",
                'answer': None,
                'should_escalate': True,
                'escalation_reason': escalation_reason,
                'follow_up_agents': []
            }
        
        # Generate response
        response = self._generate_aid_response(classification, student_aid)
        
        return {
            'response': response,
            'answer': student_aid.get('amount'),
            'should_escalate': False,
            'escalation_reason': None,
            'follow_up_agents': []
        }
    
    def _classify_query(self, query: str) -> str:
        """Classify type of aid question."""
        if "when" in query.lower() or "received" in query.lower():
            return "status"
        if "how much" in query.lower() or "amount" in query.lower():
            return "amount"
        if "eligible" in query.lower():
            return "eligibility"
        return "general"
    
    def _generate_aid_response(self, query_type: str, student_aid: Dict) -> str:
        """Generate response with student's aid info."""
        
        if query_type == "status":
            status = student_aid.get('status', 'unknown')
            if status == 'disbursed':
                return f"Your financial aid of ${student_aid['amount']} was disbursed on {student_aid['disburse_date']}. Check your student account for details."
            elif status == 'pending':
                return f"Your aid is being processed. Expected disbursement: {student_aid['expected_disburse_date']}"
        
        if query_type == "amount":
            return f"Your financial aid package for this semester is ${student_aid['amount']}."
        
        return "Your financial aid status is available in your student portal."
    
    def _days_until_deadline(self) -> int:
        """Calculate days until tuition deadline."""
        from datetime import datetime
        # Simplified; in production, fetch from calendar
        return 10

class EnrollmentAgent(SpecialistAgent):
    """
    Handles enrollment: registration status, holds, course availability.
    """
    
    def __init__(self, enrollment_database):
        super().__init__(
            domain="enrollment",
            authorized_fields=[
                'registration_status', 'holds', 'course_schedule',
                'transcript', 'degree_progress'
            ]
        )
        self.enrollment_db = enrollment_database
    
    def handle_query(self, query: str, context: ConversationContext) -> Dict:
        """
        Handle enrollment-related query.
        """
        
        student_enrollment = self.enrollment_db.get_student(context.student_id)
        
        # Escalate if holds prevent registration
        if student_enrollment.get('has_holds'):
            holds = student_enrollment.get('holds', [])
            return {
                'response': f"You have holds preventing registration: {', '.join(holds)}. Let me connect you with enrollment services.",
                'answer': None,
                'should_escalate': True,
                'escalation_reason': f"Registration holds: {holds}",
                'follow_up_agents': []
            }
        
        # Otherwise, respond directly
        status = student_enrollment.get('registration_status')
        response = f"Your registration status is: {status}. You can register for {student_enrollment.get('term')}."
        
        return {
            'response': response,
            'answer': status,
            'should_escalate': False,
            'escalation_reason': None,
            'follow_up_agents': []
        }

# Usage
aid_agent = FinancialAidAgent(aid_database)

context = ConversationContext(
    student_id="stu_12345",
    student_name="Alex Chen",
    conversation_history=[],
    intent="financial_aid",
    emotional_state=EmotionalState.DISTRESSED
)

result = aid_agent.handle_query(
    "I haven't received my financial aid yet. My tuition is due next week.",
    context
)

if result['should_escalate']:
    print(f"ESCALATE: {result['escalation_reason']}")
else:
    print(f"ANSWER: {result['response']}")
```

#### 3. Orchestrator for Multi-Domain Questions

```python
class OrchestratorAgent:
    """
    Route complex queries involving multiple domains.
    
    Example: "I haven't registered because of a hold, but I also
    haven't received my aid yet. What's blocking me?"
    
    This spans enrollment (holds) AND financial_aid.
    Orchestrator determines sequence and synthesizes answer.
    """
    
    def __init__(self, specialists: Dict[str, SpecialistAgent]):
        self.specialists = specialists  # {'financial_aid': agent, 'enrollment': agent, ...}
        self.client = anthropic.Anthropic()
    
    def handle_query(
        self,
        query: str,
        context: ConversationContext
    ) -> Dict:
        """
        Determine which specialists are needed, call them, synthesize result.
        """
        
        # Step 1: Plan which specialists to consult
        plan = self._plan_specialist_sequence(query, context)
        print(f"Specialist plan: {[s['domain'] for s in plan]}")
        
        # Step 2: Call each specialist in sequence
        specialist_results = []
        for step in plan:
            domain = step['domain']
            agent = self.specialists[domain]
            
            result = agent.handle_query(query, context)
            specialist_results.append({
                'domain': domain,
                'result': result
            })
            
            # Stop if escalation needed
            if result['should_escalate']:
                return {
                    'response': result['response'],
                    'should_escalate': True,
                    'escalation_reason': result['escalation_reason'],
                    'specialists_consulted': [s['domain'] for s in specialist_results]
                }
        
        # Step 3: Synthesize answers
        synthesis = self._synthesize_results(specialist_results, query)
        
        return {
            'response': synthesis,
            'should_escalate': False,
            'escalation_reason': None,
            'specialists_consulted': [s['domain'] for s in specialist_results]
        }
    
    def _plan_specialist_sequence(
        self,
        query: str,
        context: ConversationContext
    ) -> List[Dict]:
        """
        Determine order of specialists to consult.
        """
        
        # Simple heuristic: check for keywords
        plan = []
        
        if any(word in query.lower() for word in ['aid', 'fafsa', 'disburs']):
            plan.append({'domain': 'financial_aid', 'order': 1})
        
        if any(word in query.lower() for word in ['register', 'hold', 'enroll']):
            plan.append({'domain': 'enrollment', 'order': 2})
        
        if any(word in query.lower() for word in ['housing', 'dorm', 'room']):
            plan.append({'domain': 'housing', 'order': 3})
        
        # Sort by order
        return sorted(plan, key=lambda x: x['order']) if plan else [
            {'domain': 'financial_aid', 'order': 1}  # Default
        ]
    
    def _synthesize_results(
        self,
        specialist_results: List[Dict],
        query: str
    ) -> str:
        """
        Combine specialist answers into coherent response.
        """
        
        specialist_summaries = []
        for sr in specialist_results:
            domain = sr['domain']
            result = sr['result']
            specialist_summaries.append(
                f"{domain}: {result['response']}"
            )
        
        # Use LLM to synthesize
        system_prompt = """You are a student services coordinator.
Multiple specialists have provided information about a student's situation.
Synthesize their responses into a single, cohesive explanation that:
1. Addresses the student's original concern
2. Explains any interdependencies (e.g., hold blocks registration, which delays...</course>)
3. Provides a clear next step
4. Is empathetic and clear"""
        
        user_message = f"""Original question: {query}

Specialist inputs:
{chr(10).join(specialist_summaries)}

Synthesize into one coherent response."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        return response.content[0].text

# Usage
orchestrator = OrchestratorAgent({
    'financial_aid': aid_agent,
    'enrollment': enrollment_agent
})

result = orchestrator.handle_query(
    "I haven't registered because of a hold, but I also haven't received my aid yet. What's blocking me?",
    context
)

print(f"Response: {result['response']}")
print(f"Specialists consulted: {result['specialists_consulted']}")
```

### Design Decisions & Why

**1. Why Emotional State Detection?**
- Distressed students need different handling than casual inquiries
- Emotion is a reliable escalation signal (human support needed)
- Allows agent to adjust tone and prioritization

**2. Why Domain-Specific Agents?**
- Financial aid rules are complex and different from enrollment rules
- Data separation: housing agent shouldn't access financial data
- Easier to iterate (update aid logic without touching enrollment)
- Easier to audit (clear boundaries of responsibility)

**3. Why Orchestrator?**
- Some questions span multiple domains (holds + aid + graduation)
- Orchestrator determines sequence (do you check aid first or holds?)
- Synthesizes into single coherent answer
- Alternative: ask student "pick one domain" (bad UX)

**4. Why Escalation Thresholds by Domain?**
- Financial aid: escalate if holds, if deadline imminent, if distressed
- Enrollment: escalate if holds prevent registration
- Housing: escalate if assignment issue
- Each domain has different risk/escalation rules

### Key Takeaways

1. **Emotional state is a signal**: distressed students need human support. Don't force agents to handle emotional situations.

2. **Domain separation with shared context**: agents are specialists. They access only authorized data, but they share student ID and conversation history.

3. **Escalation rules are domain-specific**: financial aid escalates on different triggers than housing. Document these.

4. **Multi-domain questions need orchestration**: some questions require consulting multiple specialists. Orchestrator determines sequence and synthesizes.

5. **Always provide human exit ramp**: escalation should be warm (agent hands off, provides context). No "you've been transferred, starting over."

---

## Case Study 3: Alan — Healthcare Navigation Agent with Compliance Verification

### The Business Problem

Alan provides healthcare navigation for tens of thousands of patients. Common questions:

- "What's my coverage for physical therapy?"
- "Do I need pre-authorization for a specialist?"
- "What's my deductible?"
- "Is Dr. X in my network?"

Healthcare is heavily regulated. Every response must be:
1. **Accurate** (wrong info = patient pays out-of-pocket or goes uninsured)
2. **Compliant** (HIPAA, state regulations, regulatory disclosures)
3. **Auditable** (regulators can see why the agent said X)

A single wrong response could expose Alan to regulatory fines, patient lawsuits, and loss of licensure.

Alan built a **compliance-verified agent** where:
1. Agent answers coverage/claim questions
2. Compliance layer verifies response against policy documents
3. Response is either approved or escalated
4. Full audit trail is logged
5. Regulators can audit the reasoning

### Why This Pattern Fits

**Compliance verification** is non-negotiable in heavily regulated domains (healthcare, finance, legal). The pattern:

1. **Agent generates answer** (fast, LLM-based)
2. **Compliance layer checks answer** against source documents
3. **If verified**: send; if not: escalate
4. **Audit trail**: log source, reasoning, approval

This is different from the previous patterns:
- Rio Tinto (citation required, but not regulatory)
- Booking (guardrails for brand, not law)
- Anthology (emotional escalation, not regulatory)

Here, compliance is the primary gate. An answer without verification is worthless.

### Architecture Diagram

```
┌──────────────────────────────────────────┐
│    Patient Question                      │
│  "Is PT covered under my plan?"          │
└────────────────┬─────────────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │  Agent Answer Generation      │
    │ (LLM + Coverage DB)           │
    │                               │
    │  "Physical therapy is covered │
    │   at 80% after deductible.    │
    │   Requires referral from PCP" │
    └────────────┬──────────────────┘
                 │
    ┌────────────▼─────────────────────┐
    │ Compliance Verification Layer    │
    │                                  │
    │ 1. Extract claims in answer      │
    │    - "PT covered at 80%"         │
    │    - "After deductible"          │
    │    - "Requires PCP referral"     │
    │                                  │
    │ 2. Check against policy docs     │
    │    - Find: Section 5.2, PT       │
    │    - Verify: "80% coverage"      │
    │    - Verify: "Post-deductible"   │
    │    - Verify: "Requires referral" │
    │                                  │
    │ 3. All claims verified?          │
    │    YES → APPROVE                 │
    │    NO → FLAG violation           │
    └────────────┬────────────────────┘
                 │
    ┌────────────▼──────────────────┐
    │ If Approved: Send Response    │
    │                               │
    │ Response + citation:          │
    │ "PT covered at 80%            │
    │ (see policy section 5.2)      │
    │ Requires PCP referral         │
    │ (see policy section 5.2.1)"   │
    │                               │
    │ Audit entry:                  │
    │ - Patient ID                  │
    │ - Question                    │
    │ - Answer                      │
    │ - Verification source         │
    │ - Verified by: system v1.2    │
    │ - Timestamp                   │
    └────────────────────────────────┘
                 │
    ┌────────────▼────────────────────────┐
    │ If Failed: Escalate & Explain      │
    │                                    │
    │ Reason: Claim cannot be verified   │
    │ Claim: "PT requires referral"      │
    │ Problem: Not found in policy docs  │
    │                                    │
    │ Action: Route to human specialist  │
    │ Audit entry: marked as escalated   │
    └────────────────────────────────────┘
```

### Implementation: Key Components

#### 1. Answer Extraction and Claim Decomposition

```python
from typing import List, Tuple
import anthropic
import json

@dataclass
class Claim:
    """
    A single factual claim in an agent response.
    """
    text: str
    category: str  # 'coverage', 'requirement', 'exclusion', 'process'
    coverage_type: str  # 'PT', 'mental_health', 'ER', etc.
    confidence: float

class AnswerExtractor:
    """
    Extract factual claims from agent's response.
    
    Example:
        Response: "Physical therapy is covered at 80% after deductible. 
                   Requires PCP referral."
        
        Claims:
        - "PT covered at 80%"
        - "After deductible" 
        - "Requires PCP referral"
    """
    
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def extract_claims(self, response: str) -> List[Claim]:
        """
        Break response into individual, verifiable claims.
        """
        
        system_prompt = """Extract factual claims from a healthcare provider's response.

Each claim should be:
1. A single, specific assertion
2. Verifiable against policy documents
3. Categorized as: coverage (what's covered/excluded), 
   requirement (what's needed), process (how to access)

Respond with JSON:
{
    "claims": [
        {
            "text": "<claim>",
            "category": "<category>",
            "coverage_type": "<PT|ER|MH|...>",
            "confidence": <0-1>
        }
    ]
}

Example claims:
- "Physical therapy covered at 80%"
- "Requires pre-authorization"
- "Three visits per calendar year limit"
- "In-network providers only"
"""
        
        user_message = f"""Response to extract claims from:

{response}

Extract all factual claims."""
        
        response_obj = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        try:
            result = json.loads(response_obj.content[0].text)
            claims = [
                Claim(
                    text=c['text'],
                    category=c['category'],
                    coverage_type=c['coverage_type'],
                    confidence=c['confidence']
                )
                for c in result['claims']
            ]
            return claims
        except json.JSONDecodeError:
            # Fallback: extract sentences
            sentences = response.split('. ')
            return [
                Claim(text=s, category='unknown', coverage_type='unknown', confidence=0.5)
                for s in sentences if len(s) > 10
            ]

# Usage
extractor = AnswerExtractor()

response = """Physical therapy is covered at 80% after your deductible is met.
You'll need a referral from your primary care doctor.
Each year you get up to 30 visits covered."""

claims = extractor.extract_claims(response)
for claim in claims:
    print(f"Claim: {claim.text}")
    print(f"  Category: {claim.category}")
    print(f"  Coverage: {claim.coverage_type}")
```

#### 2. Compliance Verification Against Policy Documents

```python
from typing import Dict, List, Tuple

class ComplianceVerifier:
    """
    Verify extracted claims against policy documents.
    
    Process:
    1. For each claim, search policy docs
    2. Find relevant sections
    3. Check if claim matches policy
    4. Return: VERIFIED, CONTRADICTED, or NOT_FOUND
    """
    
    def __init__(self, policy_retriever):
        self.retriever = policy_retriever  # RAG system for policy docs
        self.client = anthropic.Anthropic()
    
    def verify_claim(
        self,
        claim: Claim,
        patient_plan: Dict
    ) -> Dict:
        """
        Verify a single claim against policy docs.
        
        Returns:
            {
                'claim': str,
                'status': 'VERIFIED' | 'CONTRADICTED' | 'NOT_FOUND',
                'source': str (section/page from policy),
                'verification_quote': str,
                'confidence': float
            }
        """
        
        # Step 1: Search policy for relevant sections
        search_results = self.retriever.retrieve(
            query=f"{claim.coverage_type} {claim.text}",
            plan_id=patient_plan['id'],
            top_k=5
        )
        
        if not search_results:
            return {
                'claim': claim.text,
                'status': 'NOT_FOUND',
                'source': None,
                'verification_quote': None,
                'confidence': 0.0
            }
        
        # Step 2: Use LLM to check if claim matches policy
        policy_text = "\n\n".join([
            f"[Section {r['section']}]\n{r['content']}"
            for r in search_results
        ])
        
        system_prompt = """Verify a healthcare claim against policy document excerpts.

For the claim provided, check if the policy documents:
1. SUPPORT the claim (coverage/requirement stated)
2. CONTRADICT the claim (coverage denied or different terms)
3. ARE SILENT on the claim (not mentioned)

Respond with JSON:
{
    "status": "VERIFIED|CONTRADICTED|NOT_FOUND",
    "verification_quote": "<exact quote from policy>",
    "section": "<section reference>",
    "confidence": <0-1>,
    "reasoning": "<why this status>"
}

Be very confident (>0.9) only if exact match or clear contradiction.
If paraphrased, lower confidence accordingly."""
        
        user_message = f"""Claim to verify:
"{claim.text}"

Coverage type: {claim.coverage_type}

Policy documents:
{policy_text}

Verify this claim."""
        
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        try:
            result = json.loads(response.content[0].text)
            return {
                'claim': claim.text,
                'status': result['status'],
                'source': result.get('section'),
                'verification_quote': result.get('verification_quote'),
                'confidence': result['confidence'],
                'reasoning': result.get('reasoning', '')
            }
        except json.JSONDecodeError:
            return {
                'claim': claim.text,
                'status': 'NOT_FOUND',
                'source': None,
                'verification_quote': None,
                'confidence': 0.0
            }
    
    def verify_response(
        self,
        claims: List[Claim],
        patient_plan: Dict
    ) -> Dict:
        """
        Verify all claims in response.
        
        Returns:
            {
                'overall_status': 'APPROVED' | 'ESCALATED',
                'verifications': List[Dict],
                'violations': List[str],
                'confidence': float (overall)
            }
        """
        
        verifications = []
        violations = []
        
        for claim in claims:
            verification = self.verify_claim(claim, patient_plan)
            verifications.append(verification)
            
            # Track violations
            if verification['status'] == 'CONTRADICTED':
                violations.append(
                    f"Claim contradicted: '{claim.text}' (policy says {verification['verification_quote']})"
                )
            elif verification['status'] == 'NOT_FOUND' and claim.confidence > 0.8:
                violations.append(
                    f"High-confidence claim not found in policy: '{claim.text}'"
                )
        
        # Overall status
        overall_status = 'APPROVED' if not violations else 'ESCALATED'
        overall_confidence = sum(v['confidence'] for v in verifications) / len(verifications) if verifications else 0.0
        
        return {
            'overall_status': overall_status,
            'verifications': verifications,
            'violations': violations,
            'confidence': overall_confidence
        }

# Usage
verifier = ComplianceVerifier(policy_retriever)

verification = verifier.verify_response(
    claims=claims,
    patient_plan={'id': 'plan_12345', 'name': 'PPO Gold'}
)

print(f"Status: {verification['overall_status']}")
if verification['violations']:
    print(f"Violations: {verification['violations']}")
else:
    print("All claims verified")
```

#### 3. Audit Trail & Regulatory Logging

```python
from datetime import datetime
from dataclasses import asdict
import json

@dataclass
class AuditEntry:
    """
    Complete record of an agent interaction for regulatory audit.
    """
    timestamp: str
    patient_id: str
    patient_plan_id: str
    question: str
    agent_response: str
    claims: List[dict]
    verifications: List[dict]
    overall_status: str
    escalated_to_human: bool
    escalation_reason: str = None
    human_agent_id: str = None
    final_response: str = None
    agent_system_version: str = None
    verifier_version: str = None

class AuditLogger:
    """
    Log all interactions for regulatory compliance.
    
    Allows regulators to:
    - Verify answers against policy
    - Check escalation decisions
    - Audit agent behavior
    """
    
    def __init__(self, audit_db):
        self.audit_db = audit_db  # Write-once audit database
    
    def log_interaction(
        self,
        patient_id: str,
        plan_id: str,
        question: str,
        agent_response: str,
        claims: List[Claim],
        verification_result: Dict,
        escalated: bool,
        escalation_reason: str = None
    ) -> str:
        """
        Log complete interaction.
        
        Returns: audit_entry_id (for reference)
        """
        
        entry = AuditEntry(
            timestamp=datetime.utcnow().isoformat(),
            patient_id=patient_id,
            patient_plan_id=plan_id,
            question=question,
            agent_response=agent_response,
            claims=[asdict(c) for c in claims],
            verifications=verification_result['verifications'],
            overall_status=verification_result['overall_status'],
            escalated_to_human=escalated,
            escalation_reason=escalation_reason,
            agent_system_version="alan-agent-v2.1",
            verifier_version="alan-verifier-v1.5"
        )
        
        # Write to audit database
        audit_id = self.audit_db.write(asdict(entry))
        
        return audit_id
    
    def get_audit_trail(
        self,
        patient_id: str = None,
        date_range: Tuple[str, str] = None
    ) -> List[AuditEntry]:
        """
        Retrieve audit trail for regulatory review.
        
        Filtering by patient (for patient requests) or date (for audit).
        """
        
        query = {}
        if patient_id:
            query['patient_id'] = patient_id
        if date_range:
            query['timestamp'] = {'$gte': date_range[0], '$lte': date_range[1]}
        
        entries = self.audit_db.query(query)
        return entries

# Usage in complete flow
def handle_patient_question(
    question: str,
    patient_id: str,
    plan_id: str,
    agent,
    extractor,
    verifier,
    audit_logger
):
    """
    End-to-end: generate answer -> verify -> audit -> respond
    """
    
    # Step 1: Agent generates response
    agent_response = agent.answer_question(question, plan_id)
    
    # Step 2: Extract claims
    claims = extractor.extract_claims(agent_response)
    
    # Step 3: Verify claims
    verification = verifier.verify_response(claims, {'id': plan_id})
    
    # Step 4: Log to audit trail
    audit_id = audit_logger.log_interaction(
        patient_id=patient_id,
        plan_id=plan_id,
        question=question,
        agent_response=agent_response,
        claims=claims,
        verification_result=verification,
        escalated=(verification['overall_status'] == 'ESCALATED'),
        escalation_reason=verification['violations'][0] if verification['violations'] else None
    )
    
    # Step 5: Decide on response
    if verification['overall_status'] == 'APPROVED':
        # All claims verified; send response with citations
        final_response = f"""{agent_response}

---
This response is verified against your policy {plan_id}.
Audit reference: {audit_id}"""
        
        return {
            'action': 'send',
            'response': final_response,
            'audit_id': audit_id
        }
    
    else:
        # Escalate: claims not verified
        return {
            'action': 'escalate',
            'reason': f"Unable to verify: {verification['violations']}",
            'audit_id': audit_id,
            'escalate_to': 'healthcare_specialist'
        }

# Test
result = handle_patient_question(
    question="Is PT covered under my plan?",
    patient_id="pat_12345",
    plan_id="plan_67890",
    agent=alan_agent,
    extractor=extractor,
    verifier=verifier,
    audit_logger=audit_logger
)

if result['action'] == 'send':
    print(f"Response: {result['response']}")
else:
    print(f"Escalated: {result['reason']}")
```

### Design Decisions & Why

**1. Why Claim Extraction Before Verification?**
- Breaks response into verifiable units (easier to check)
- If one claim fails, others might pass (granular verification)
- Makes violations specific and actionable (not "response is wrong")
- Audit shows exactly which claim was problematic

**2. Why LLM-Based Verification (Not Just Keyword Matching)?**
- Healthcare language is complex and paraphrased
- "Coverage at 80%" vs "Your cost is 20%" mean the same thing
- LLM can match meaning, not just exact strings
- Alternative (rule-based) would require exhaustive policy encoding

**3. Why Confidence Thresholds?**
- Some claims are paraphrased (lower confidence)
- Some claims are exact quotes (higher confidence)
- Low confidence + NOT_FOUND = escalate (safer)
- Allows quantified risk assessment

**4. Why Write-Once Audit?**
- Regulatory requirement: audit trail cannot be modified
- Write-once prevents tampering
- Timestamp every interaction
- Chain of custody is unbreakable

**5. Why Escalate on Failed Verification?**
- Better to escalate than make promise without verification
- Human specialist can confirm with patient (if ambiguous)
- Regulatory liability: "we verified" is defensible, "we guessed" is not

### Key Takeaways

1. **Compliance verification is a separate gate**: don't embed it in response generation. Extract, verify, then decide.

2. **Break responses into claims**: each claim is individually verifiable. Makes violations precise.

3. **Use LLM for semantic matching**: exact string matching fails in domains with terminology variation.

4. **Audit everything**: write-once logs with timestamps, patient ID, question, response, verification result, and escalation reason.

5. **Escalate on uncertainty**: healthcare is high-stakes. When verification fails, escalate to human. Better safe than liable.
